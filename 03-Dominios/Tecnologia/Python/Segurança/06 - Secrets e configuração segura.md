---
title: "Secrets e configuração segura"
created: 2026-07-11
type: concept
fase: adepto→magus
status: seedling
publish: true
tags:
  - python
  - seguranca
  - secrets
  - configuracao
aliases:
  - "Gestão de secrets em Python"
  - "Configuração segura em Python"
  - "pydantic-settings"
---

# Secrets e configuração segura

> [!abstract] TL;DR
> Secret hardcoded no código-fonte é o erro de segurança mais comum e mais caro em Python — porque o git é um grafo imutável, e um segredo commitado **permanece no histórico para sempre**, mesmo depois de "removido" num commit posterior. A defesa em profundidade tem quatro camadas: variáveis de ambiente como padrão de configuração (`os.environ`, `python-dotenv` em desenvolvimento), `.env` no `.gitignore` **desde o primeiro commit**, secret scanning automatizado (`detect-secrets`/`gitleaks`) barrando o segredo antes dele entrar no repositório, e `pydantic-settings` como camada de configuração tipada que falha rápido se faltar algo obrigatório. Se um segredo já vazou, a ordem de resposta é sempre a mesma: **rotacionar primeiro** — limpar o histórico depois, se ainda fizer sentido.

## O commit "só pra testar"

Segunda-feira, 9h da manhã. Um dev novo no time abre um projeto Django recém-criado, roda `django-admin startproject`, e se depara com a linha que o próprio Django gerou:

```python
# settings.py
SECRET_KEY = "django-insecure-k#8x2m$p9q!w5e@r7t3y6u1i0o4a8s2d6f9g3h7"
```

O comentário mental é automático: "isso aqui é só pra rodar local, depois eu troco". O projeto sobe, os testes passam, o code review do PR de setup inicial aprova em cinco minutos — ninguém olha `settings.py` linha por linha num PR de scaffold, todo mundo sabe que é boilerplate gerado. Três sprints depois, o projeto vai pra produção. Ninguém trocou a `SECRET_KEY`. Ela segue lá, idêntica, visível pra qualquer pessoa com acesso de leitura ao repositório — e, pior, ela assina cada sessão de usuário, cada token de reset de senha, cada mensagem CSRF da aplicação.

Essa não é uma história hipotética de manual de segurança. É o padrão mais comum de vazamento de secret em projetos Python, e ele tem duas variações igualmente frequentes:

1. **O `SECRET_KEY` de scaffold que nunca foi trocado** — o cenário acima. O framework gera um valor de desenvolvimento pra você poder rodar `runserver` sem configurar nada; a suposição implícita é que você troca antes de produção, mas nada no fluxo *força* essa troca.
2. **O `.env` commitado por acidente** — um dev cria o projeto, escreve `DATABASE_URL=postgres://user:senha@host/db` num `.env` pra testar localmente, roda `git add .` antes de criar o `.gitignore`, e o primeiro commit do repositório já nasce com a senha do banco dentro. O `.gitignore` chega no commit seguinte — tarde demais.

Os dois casos compartilham a mesma causa raiz: **a configuração sensível nasceu junto com o código, no mesmo commit, sem nenhuma barreira entre "eu escrevi isso" e "isso está permanentemente no histórico do git".** Esta nota existe para construir essa barreira — em quatro camadas, da mais barata (variável de ambiente) à mais rigorosa (scanning automatizado + configuração tipada com fail-fast).

> [!question]- Por que ninguém percebe até ser tarde demais?
> Porque o custo de errar é diferido e o custo de corrigir "depois" parece baixo — até você descobrir que "depois" não existe pra git. Enquanto o projeto roda só em desenvolvimento, um `SECRET_KEY` fraco ou uma senha em texto puro não causam nenhum sintoma visível: os testes passam, a aplicação funciona, ninguém é atacado porque ninguém sabe que aquele repositório existe. O problema só aparece quando o código sai do ambiente controlado — vai pra produção, o repositório se torna público, alguém dá fork, ou um bot de scanning encontra o padrão `SECRET_KEY = "..."` numa busca automatizada no GitHub. Nesse momento, a "correção fácil de depois" já não é fácil: o segredo está espalhado por todo clone, fork e mirror que existiu desde o primeiro push.

## Por que hardcoded é o erro mais caro: a permanência do git

O git não é um banco de dados de chave-valor que você edita e pronto. É um **grafo imutável de snapshots**. Cada commit aponta pro estado anterior; nada nunca é sobrescrito, só encadeado. Isso é uma propriedade excelente para rastreabilidade de código — e uma armadilha fatal para segredos.

O cenário clássico de "eu já resolvi isso" que na verdade não resolveu nada:

```bash
# Commit 1: SECRET_KEY hardcoded entra no repositório
git add settings.py
git commit -m "setup inicial do projeto"

# Semanas depois, alguém percebe o problema
git rm settings.py  # errado: isso não apaga do histórico
# edita settings.py para ler de variável de ambiente
git add settings.py
git commit -m "remove secret hardcoded"
```

Depois desse segundo commit, `settings.py` no *working tree* está limpo — quem clona o repositório hoje e olha o arquivo não vê o segredo. Mas `git log -p -- settings.py` ainda mostra o valor original no diff do primeiro commit. `git show <hash-do-commit-1>` ainda revela a chave completa. Qualquer clone feito entre o commit 1 e o commit 2 tem o segredo em `.git/objects` para sempre, independente do que aconteça nos commits seguintes.

> [!warning] Remover do histórico não desfaz o vazamento — ROTACIONE primeiro
> Existem ferramentas para reescrever o histórico do git e apagar um blob específico de todos os commits — `git filter-repo` (a ferramenta atual recomendada; `git filter-branch` está deprecated) e o BFG Repo-Cleaner. Elas funcionam tecnicamente: depois de rodadas, o segredo não existe mais em nenhum commit do repositório reescrito. **Mas isso não desfaz o vazamento.** Se o repositório já foi clonado por qualquer pessoa, tem um fork, está espelhado num CI, ou é público, o segredo antigo continua existindo em cópias que você não controla e não consegue reescrever remotamente. Reescrever o histórico local não alcança essas cópias. A única ação que efetivamente neutraliza o vazamento é **trocar o valor do segredo** — gerar uma nova `SECRET_KEY`, rotacionar a credencial do banco, revogar a chave de API antiga. Depois disso, limpar o histórico ainda tem valor (higiene, compliance, reduzir ruído para scanners futuros), mas é secundário — e só faz sentido se o repositório realmente precisa continuar existindo com esse histórico. A ordem correta é sempre: **rotacionar primeiro, limpar histórico depois, se ainda fizer sentido.**

O tempo de exposição costuma ser menor do que a intuição sugere. Bots automatizados varrem commits públicos do GitHub em tempo real, procurando padrões conhecidos de chave (prefixos de API key da AWS, tokens do GitHub, strings de conexão de banco). Um segredo commitado num repositório público pode ser encontrado e explorado em minutos — às vezes antes mesmo do dev perceber que fez o commit errado. [[03-Dominios/Engenharia/Segurança/18 - Gestão de chaves e segredos|A nota de Gestão de chaves e segredos, em Engenharia/Segurança]], documenta o caso Uber 2016 — uma chave AWS hardcoded num repositório *privado* (não nem público) resultou em 57 milhões de registros vazados e US$148 milhões em multas. Repositório privado não é proteção suficiente; é só uma camada a mais de obscuridade, não de segurança real.

## Camada 1 — variáveis de ambiente como padrão

A primeira defesa é estrutural: **secrets nunca são valores literais no código**. Eles são lidos de variáveis de ambiente, que existem fora do repositório e não são versionadas.

```python
# Vulnerável: valor literal no código
SECRET_KEY = "django-insecure-k#8x2m$p9q!w5e@r7t3y6u1i0o4a8s2d6f9g3h7"
DATABASE_URL = "postgres://admin:senha123@db.producao.com:5432/app"

# Corrigido: lido de variável de ambiente
import os

SECRET_KEY = os.environ["SECRET_KEY"]  # levanta KeyError se não existir — falha explícita
DATABASE_URL = os.environ["DATABASE_URL"]
```

A diferença entre `os.environ["SECRET_KEY"]` e `os.environ.get("SECRET_KEY")` importa mais do que parece à primeira vista. `os.environ[...]` levanta `KeyError` imediatamente se a variável não existir — a aplicação recusa a subir sem o segredo configurado. `os.environ.get(...)` retorna `None` silenciosamente, o que empurra o problema pra mais tarde (um `TypeError` obscuro na primeira query ao banco, ou pior, um `None` sendo usado como se fosse uma string válida). Para configuração obrigatória, `os.environ[...]` (ou um default explícito documentado via `os.getenv("DEBUG", "false")` para configuração opcional) é o padrão mais seguro:

```python
import os

# Obrigatório: falha rápido e claro se faltar
DATABASE_URL = os.environ["DATABASE_URL"]

# Opcional: tem default sensato e documentado
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

Em produção, a variável de ambiente é injetada pelo orquestrador — Kubernetes Secrets, variáveis de ambiente do serviço no Heroku/Railway/ECS, ou um secret manager que popula o ambiente do processo no boot. O código Python nunca sabe *de onde* o valor veio; ele só lê `os.environ`. Essa indireção é o que permite trocar de "arquivo `.env` local" para "Vault em produção" sem mudar uma linha de código de aplicação.

### `python-dotenv` para desenvolvimento local

Configurar quinze variáveis de ambiente manualmente toda vez que você abre um terminal novo é inviável na prática. O padrão para desenvolvimento é o pacote `python-dotenv`, que lê um arquivo `.env` na raiz do projeto e popula `os.environ` a partir dele — sem que esse arquivo jamais chegue ao git.

```python
# no ponto de entrada da aplicação (main.py, manage.py, ou settings.py)
from dotenv import load_dotenv

load_dotenv()  # lê o .env na raiz do projeto e popula os.environ

import os
SECRET_KEY = os.environ["SECRET_KEY"]
```

```bash
# .env (NUNCA commitado)
SECRET_KEY=uma-chave-forte-gerada-so-para-este-ambiente
DATABASE_URL=postgres://dev:dev@localhost:5432/app_dev
DEBUG=true
```

```bash
# .env.example (ESTE sim é commitado — documenta as chaves esperadas, sem valores reais)
SECRET_KEY=
DATABASE_URL=
DEBUG=
```

O padrão `.env` (real, com valores, ignorado pelo git) + `.env.example` (template vazio, commitado, documentando quais variáveis a aplicação espera) resolve dois problemas de uma vez: cada dev configura seu próprio `.env` local sem depender de segredo compartilhado por Slack ou e-mail, e qualquer pessoa nova no time sabe exatamente quais variáveis precisa preencher só olhando o `.env.example`.

> [!tip] `load_dotenv()` não sobrescreve variáveis já definidas por padrão
> Por padrão, `load_dotenv()` não sobrescreve uma variável de ambiente que já existe no processo (comportamento controlado pelo parâmetro `override`, que é `False` por padrão). Isso é intencional: em CI e produção, as variáveis de ambiente reais (injetadas pelo orquestrador) sempre têm prioridade sobre um `.env` que porventura exista no filesystem por engano. `load_dotenv()` é seguro de deixar no código de produção — se não houver `.env` no filesystem, ele simplesmente não faz nada.

## `.env` no `.gitignore` desde o primeiro commit

O erro do "`.env` commitado por acidente" tem uma causa mecânica simples: o `.gitignore` foi criado *depois* do primeiro `git add .`. A ordem certa é inversa — o `.gitignore` (com `.env` já dentro dele) precisa existir **antes** do primeiro commit, não depois.

```bash
# Ordem correta ao iniciar um projeto novo
mkdir meu-projeto && cd meu-projeto
git init

# .gitignore é o PRIMEIRO arquivo, antes de qualquer código
cat > .gitignore << 'EOF'
.env
.env.*
!.env.example
__pycache__/
*.pyc
.venv/
EOF
git add .gitignore
git commit -m "gitignore inicial"

# só agora começa a escrever o resto do projeto
echo "SECRET_KEY=dev-key-local" > .env
# ... resto do setup
```

Repare no padrão `.env.*` seguido de `!.env.example` — isso ignora qualquer arquivo `.env.producao`, `.env.staging` etc. que apareça no futuro, mas mantém uma exceção explícita para o template documentado. É um detalhe pequeno que evita a recorrência do mesmo erro em ambientes adicionais que o projeto ganha conforme cresce.

> [!warning] `.gitignore` não protege o que já foi commitado
> Adicionar `.env` ao `.gitignore` **depois** que ele já foi commitado uma vez não remove o arquivo do histórico — só impede commits *futuros* daquele arquivo. Se você perceber que um `.env` real já está em algum commit anterior, o problema já é o cenário da seção anterior: rotacione todo segredo que estava naquele arquivo, e só depois considere limpar o histórico.

## O que fazer quando um secret já vazou

Quando a prevenção falha e um segredo aparece num commit — seja porque o `.gitignore` chegou tarde, seja porque alguém colou uma chave de API direto num arquivo de código para "testar rápido" — a resposta segue uma ordem fixa, não uma lista de opções equivalentes:

```mermaid
flowchart TD
    A["Secret detectado em um commit\n(scanner, revisão manual, alerta de bot)"] --> B{"O segredo já foi\npush para um remoto\ncompartilhado?"}
    B -->|"Não — só local,\nainda não commitado"| C["git reset / edita o arquivo\nantes de commitar"]
    B -->|"Sim — já está\nno histórico remoto"| D["ROTACIONE o segredo AGORA\n(gera novo valor, revoga o antigo)"]
    D --> E["Atualize a configuração\nem todos os ambientes\ncom o novo valor"]
    E --> F{"O repositório precisa\ncontinuar existindo\ncom esse histórico?"}
    F -->|"Sim"| G["git filter-repo / BFG\npara limpar o histórico\n(higiene, não é a defesa real)"]
    F -->|"Não / não vale o custo"| H["Deixa o histórico como está —\no segredo antigo já está morto,\nlimpar é só cosmético"]
    G --> I["Notifica o time,\nregistra o incidente"]
    H --> I

    style D fill:#c0392b,color:#fff
    style A fill:#e67e22,color:#fff
```

> [!info] Leitura do diagrama
> O ramo crítico é o da direita: assim que o segredo passa a existir num commit já enviado a um remoto compartilhado (mesmo que privado), a única ação que realmente resolve o problema é a rotação — tudo o que vem depois (limpar histórico, notificar time) é auditoria e higiene, não neutralização do risco. Se o segredo nunca saiu da sua máquina (ainda não teve `push`), o problema é mais barato: basta corrigir antes de enviar.

Checklist de resposta, na ordem certa:

1. **Trate o segredo como comprometido, mesmo sem evidência de uso indevido.** Não espere confirmação de que alguém explorou a chave — o custo de rotacionar um segredo saudável é baixo; o custo de não rotacionar um segredo vazado pode ser catastrófico.
2. **Rotacione imediatamente.** Gere um novo `SECRET_KEY`, troque a senha do banco, revogue a chave de API antiga no provedor e emita uma nova. Esse é o passo que efetivamente elimina o risco — e é frequentemente o que as pessoas esquecem de fazer primeiro, indo direto para "vou limpar o git".
3. **Propague o novo valor para todos os ambientes** que dependiam do antigo — variáveis de ambiente de produção, staging, CI, e os `.env` locais de quem trabalha no projeto.
4. **Avalie se vale limpar o histórico do git** (`git filter-repo`, BFG Repo-Cleaner). Só faça isso depois da rotação, e só se o repositório tiver vida útil longa pela frente — reescrever histórico de um repositório com múltiplos colaboradores exige coordenação (todo mundo precisa re-clonar ou fazer force-pull), então o custo operacional às vezes não compensa o ganho de higiene, especialmente se o segredo já está morto.
5. **Registre o incidente** — mesmo internamente, sem processo formal de compliance. Um registro simples ("vazou X, rotacionado em Y, causa raiz Z") ajuda a identificar padrões recorrentes e justifica investir em prevenção automatizada, que é o assunto da próxima seção.

## Camada 2 — secret scanning automatizado

Depender de disciplina humana para nunca commitar um segredo é uma aposta perdida em qualquer time com mais de uma pessoa e mais de uma semana de prazo apertado. A defesa que efetivamente escala é **detecção automatizada antes do commit acontecer**.

```mermaid
sequenceDiagram
    participant Dev as Desenvolvedor
    participant Hook as pre-commit hook<br/>(detect-secrets / gitleaks)
    participant Repo as Repositório local
    participant CI as CI/CD
    participant Prod as Produção

    Dev->>Hook: git commit (arquivo com secret)
    alt Hook detecta padrão de secret
        Hook-->>Dev: commit BLOQUEADO<br/>"possível secret detectado"
        Dev->>Dev: remove o secret,<br/>usa variável de ambiente
        Dev->>Hook: git commit (corrigido)
        Hook-->>Repo: commit aceito
    else Hook falha em detectar (falso negativo)
        Hook-->>Repo: commit aceito (secret entrou)
        Repo->>CI: push / pull request
        CI->>CI: gate de secret scanning no CI
        alt CI detecta
            CI-->>Dev: build falha,<br/>PR bloqueado
        else CI também não detecta
            CI->>Prod: deploy com secret exposto
            Note over Prod: bot externo de scanning<br/>pode encontrar em minutos
        end
    end
```

> [!info] Leitura do diagrama
> A defesa em profundidade tem duas barreiras, não uma: o pre-commit hook roda na máquina do dev, antes até do commit existir localmente com o secret registrado — é a barreira mais barata, porque interrompe o problema antes dele nascer. O gate de CI é a segunda barreira, pega o que passou pelo hook (dev sem o hook instalado, hook desatualizado, `--no-verify` usado por pressa). Se as duas falharem, o segredo chega a produção e o jogo muda de "prevenção" para "resposta a incidente" — a seção anterior.

### `detect-secrets`

O `detect-secrets`, mantido pelo time de engenharia da Yelp, escaneia o código em busca de padrões de alta entropia e assinaturas conhecidas de credencial (chaves AWS, tokens do Slack, chaves privadas RSA, etc.). Funciona por *baseline*: você gera um arquivo `.secrets.baseline` que registra os "falsos positivos conhecidos" (ex: uma chave de exemplo na documentação), e o hook falha se aparecer qualquer coisa **nova** que não esteja no baseline.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ["--baseline", ".secrets.baseline"]
```

```bash
# Gerando o baseline pela primeira vez
detect-secrets scan > .secrets.baseline

# Auditando o que foi encontrado (marca falso positivo vs. real)
detect-secrets audit .secrets.baseline
```

### `gitleaks`

O `gitleaks` é uma alternativa (às vezes usada em conjunto) escrita em Go, focada em regex de alta precisão para formatos conhecidos de credencial, com suporte nativo a escanear todo o histórico de um repositório de uma vez — útil tanto como pre-commit hook quanto como auditoria retroativa de um repositório já existente.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
```

```bash
# Auditoria retroativa de todo o histórico — útil ao adotar a ferramenta
# num repositório que já existe há tempo, para descobrir vazamentos passados
gitleaks detect --source . --log-opts="--all"
```

### O mesmo scanner como gate de CI

O pre-commit hook protege quem tem o hook instalado localmente — o que nem sempre é todo mundo (alguém clona o repo, esquece de rodar `pre-commit install`, ou comita com `--no-verify` sob pressão de prazo). Por isso, o mesmo scanner deve rodar de novo no CI, como gate que bloqueia o merge:

```yaml
# .github/workflows/security.yml
name: Secret scanning
on: [pull_request]

jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # histórico completo, não só o commit atual
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

> [!tip] Duas barreiras, não uma
> Pre-commit hook sozinho tem furos (dev sem o hook, `--no-verify`); gate de CI sozinho detecta tarde (o segredo já passou pela máquina do dev, já está no histórico local, e o feedback demora minutos em vez de segundos). Rodar o scanner nos dois pontos — hook local *e* gate de CI — fecha os furos de cada camada individual com a outra.

## Camada 3 — configuração tipada com `pydantic-settings`

Ler `os.environ["ALGO"]` espalhado por vários arquivos funciona, mas tem três problemas: nada garante o *tipo* do valor (toda variável de ambiente é string — `"false"` não vira `bool` sozinho), não há um lugar único que documente toda a configuração da aplicação, e um erro de configuração só aparece quando aquela variável específica é lida pela primeira vez em runtime — possivelmente minutos depois do processo subir, no meio de uma requisição de usuário.

`pydantic-settings` (o pacote `BaseSettings`, que migrou para fora do Pydantic core na v2) resolve os três problemas de uma vez: define a configuração como uma classe Pydantic normal, carrega valores automaticamente de variáveis de ambiente (e opcionalmente de um `.env`), valida o tipo de cada campo, aceita defaults explícitos para o que é opcional, e — o ganho mais importante — **falha na inicialização**, não no meio de uma requisição, se faltar algo obrigatório.

```python
# config.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Obrigatórios: sem default — Pydantic levanta ValidationError
    # na inicialização se a env var não existir
    database_url: str
    secret_key: str

    # Opcional: tem default explícito e documentado
    debug: bool = False
    allowed_hosts: list[str] = Field(default_factory=lambda: ["localhost"])


# instanciado uma única vez, no boot da aplicação
settings = Settings()
```

```python
# uso em qualquer lugar da aplicação
from config import settings

if settings.debug:
    ...

engine = create_engine(settings.database_url)
```

Se `DATABASE_URL` ou `SECRET_KEY` não estiverem definidas no ambiente (nem no `.env`), a linha `settings = Settings()` levanta `pydantic.ValidationError` imediatamente, listando exatamente quais campos faltam:

```
pydantic_core._pydantic_core.ValidationError: 2 validation errors for Settings
database_url
  Field required [type=missing, ...]
secret_key
  Field required [type=missing, ...]
```

Isso é **fail-fast**: o processo se recusa a subir com configuração incompleta, em vez de subir "quase funcionando" e quebrar na primeira requisição que toca o banco de dados — que pode ser em produção, às 3h da manhã, sem ninguém olhando. A diferença prática entre "o deploy falhou no boot, com mensagem clara" e "a aplicação está no ar mas retorna 500 pra todo mundo" é enorme em termos de tempo de detecção e diagnóstico.

`pydantic-settings` também converte tipos automaticamente — `DEBUG=true` no ambiente vira `True` booleano no campo `debug: bool`, sem o `.lower() == "true"` manual que `os.getenv` exige. E porque é uma classe Pydantic normal, ganha de graça tudo que o Pydantic já oferece: validadores customizados (`@field_validator`), campos aninhados, e serialização para debug (`settings.model_dump()` — com cuidado de nunca logar isso em produção, já que ele expõe os valores reais).

> [!question]- `pydantic-settings` substitui `python-dotenv`?
> Não completamente — eles resolvem problemas complementares. `python-dotenv` (via `load_dotenv()`) popula `os.environ` a partir de um arquivo `.env`; `pydantic-settings` lê de `os.environ` (e opcionalmente também sabe ler direto de um `.env` via `env_file` na config, sem precisar de `load_dotenv()` explícito) e adiciona validação de tipo e estrutura em cima. Na prática, projetos que já usam `pydantic-settings` costumam configurar `env_file=".env"` direto na classe `Settings` e dispensam o `python-dotenv` como dependência separada — é uma simplificação razoável, não uma regra rígida.

## Camada 4 — o próximo degrau: secret managers de produção

Env vars e `.env` resolvem bem o problema até um certo ponto de escala. Quando a aplicação cresce — múltiplos serviços, múltiplos ambientes, exigência de auditoria de quem acessou qual segredo e quando, necessidade de rotação automática sem redeploy manual — a resposta passa a ser um **secret manager dedicado**: HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager (ou o equivalente Azure Key Vault).

Esses sistemas acrescentam o que uma variável de ambiente simples não oferece: rotação automática de credenciais com TTL curto, log de auditoria de cada leitura do segredo, segredos *dinâmicos* (gerados sob demanda e expirados em minutos, em vez de um valor estático de vida longa), e integração com identidade do workload (o processo se autentica ao vault com uma identidade efêmera — IAM role, service account — em vez de já nascer com o segredo em mãos).

Esse é conteúdo de infraestrutura, não de código de aplicação Python — a nota [[03-Dominios/Engenharia/Segurança/18 - Gestão de chaves e segredos|Gestão de chaves e segredos, em Engenharia/Segurança]], desenvolve a fundo o modelo de envelope encryption (KEK/DEK), HSM, e o padrão de injeção de segredos em runtime via Vault Agent Injector ou External Secrets Operator no Kubernetes. Vale a leitura quando o projeto sair do estágio de "algumas env vars num `.env`" para "múltiplos serviços em produção com requisito de compliance". Para o escopo desta trilha — desenvolvimento de aplicações Python — as camadas 1 a 3 (env vars, scanning, `pydantic-settings`) cobrem o que a maioria dos projetos precisa antes de justificar a complexidade operacional de rodar um Vault próprio.

## Armadilhas comuns

> [!warning] "É só um projeto de teste, não importa"
> **O que acontece:** um projeto começa como protótipo descartável, com secrets hardcoded "porque vai jogar fora mesmo" — e seis meses depois está em produção, com o mesmo `SECRET_KEY` de scaffold que ninguém trocou. **Por quê:** a decisão de "isso não importa" é tomada num momento em que de fato não importa (projeto local, sem dados reais) — mas o código não sabe que mudou de contexto quando alguém o promove pra produção sem revisão de segurança. **Como evitar:** tratar as quatro camadas desta nota como padrão desde o primeiro commit, independente de o projeto parecer descartável. O custo de fazer certo desde o início é marginal; o custo de descobrir tarde é alto.

> [!warning] Confiar que "repositório privado" é proteção suficiente
> **O que acontece:** um time decide que não precisa de env vars ou scanning porque o repositório é privado — "só a gente tem acesso". **Por quê:** repositório privado reduz a superfície de exposição, mas não elimina: qualquer colaborador com acesso de leitura vê o segredo, um fork acidental ou uma integração de CI mal configurada pode expor o conteúdo, e o caso Uber 2016 é a prova de que "privado" não impediu 57 milhões de registros vazados. **Como evitar:** tratar "privado" como uma camada a mais de defesa em profundidade, nunca como substituto das outras. As mesmas práticas (env vars, scanning, `pydantic-settings`) valem para repositório privado e público.

> [!warning] Logar a configuração inteira "para debug"
> **O que acontece:** alguém adiciona `logger.info(f"config: {settings}")` ou `print(settings.model_dump())` para depurar um problema de configuração, e esquece de remover — a `SECRET_KEY` e a `DATABASE_URL` completas passam a aparecer em todo log da aplicação, inclusive em ferramentas de observabilidade com acesso amplo (Datadog, Splunk, CloudWatch). **Por quê:** logs têm um público muito mais amplo do que o código-fonte — qualquer pessoa com acesso ao dashboard de observabilidade vê o segredo, sem precisar nem tocar no repositório. **Como evitar:** nunca serializar o objeto `Settings` inteiro em log. Se precisar depurar, logue campo a campo, excluindo explicitamente os sensíveis, ou use um `SecretStr` do Pydantic (que mascara o valor em `repr()`/`str()` por padrão, exigindo `.get_secret_value()` explícito para acessar o valor real).

## Como explicar em inglês

> "The most expensive mistake in Python configuration is hardcoding a secret directly in source, because git history is immutable — once a credential lands in a commit, deleting the file in a later commit doesn't remove it from history, and if the repo was ever cloned or is public, that copy is out of your control. My default is environment variables read via `os.environ`, `python-dotenv` for local development with a `.env` that's gitignored from the very first commit, and `pydantic-settings` for typed, validated configuration that fails fast at startup instead of failing mid-request. On top of that I run automated secret scanning — `detect-secrets` or `gitleaks` — as both a pre-commit hook and a CI gate, so a leaked credential is caught before it ever reaches a shared branch. And if something does leak: the fix is never 'remove the commit' — it's rotate the credential immediately, treat it as compromised regardless of evidence of misuse, and only then consider cleaning history if the repo's lifespan justifies the coordination cost."

| PT | EN |
|----|----|
| segredo hardcoded | hardcoded secret |
| variável de ambiente | environment variable |
| histórico imutável do git | immutable git history |
| rotacionar (um segredo) | to rotate (a secret) |
| segredo comprometido | compromised secret |
| varredura de segredos | secret scanning |
| gancho de pre-commit | pre-commit hook |
| gate de CI | CI gate |
| configuração tipada | typed configuration |
| falhar rápido / fail-fast | fail-fast |
| gerenciador de segredos | secret manager |
| segredo dinâmico | dynamic secret |

## Checklists

**Preventivo — antes que um segredo vaze:**

- [ ] `.gitignore` com `.env` criado **antes** do primeiro commit do projeto, não depois
- [ ] `.env.example` commitado como template, sem valores reais
- [ ] Nenhum valor de secret literal em código — tudo lido via `os.environ`/`pydantic-settings`
- [ ] `python-dotenv` (ou `env_file` do `pydantic-settings`) configurado para desenvolvimento local
- [ ] `detect-secrets` ou `gitleaks` instalado como pre-commit hook
- [ ] O mesmo scanner rodando como gate de CI, bloqueando merge se detectar
- [ ] Configuração da aplicação centralizada numa classe `Settings(BaseSettings)`, com campos obrigatórios sem default
- [ ] Nenhum log ou `print` serializando o objeto de configuração inteiro

**Resposta a incidente — se um segredo já vazou:**

- [ ] Trate o segredo como comprometido, mesmo sem evidência de exploração
- [ ] Rotacione o segredo imediatamente — gere novo valor, revogue o antigo no provedor
- [ ] Propague o novo valor para todos os ambientes que dependiam do antigo
- [ ] Avalie se vale a pena limpar o histórico do git (`git filter-repo`/BFG) — só depois da rotação, e só se o custo de coordenação (todo mundo re-clonar) compensar
- [ ] Registre o incidente — o quê vazou, quando foi rotacionado, causa raiz
- [ ] Se ainda não havia scanning automatizado, instale agora — esse é o momento em que a lição fica mais barata de aprender

## Fontes

- **Pydantic** — [*pydantic-settings — Settings Management*](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — documentação oficial de `BaseSettings`, `SettingsConfigDict`, `env_file` e validação.
- **Yelp** — [*detect-secrets*](https://github.com/Yelp/detect-secrets) — repositório oficial, uso como pre-commit hook e workflow de baseline/audit.
- **Gitleaks** — [*gitleaks.io*](https://gitleaks.io/) — documentação da ferramenta, configuração de pre-commit hook e GitHub Action.
- **OWASP** — [*OWASP Top 10:2021 — A05 Security Misconfiguration*](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/) — categoria sob a qual secrets mal configurados se enquadram no mapa do [[01 - OWASP Top 10 aplicado a Python web — o mapa|galho]].
- **OWASP Cheat Sheet Series** — [*Secrets Management Cheat Sheet*](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) — anti-padrões e defesas em camadas para gestão de segredos.
- Ver também [[03-Dominios/Engenharia/Segurança/18 - Gestão de chaves e segredos|Gestão de chaves e segredos]] (Engenharia/Segurança) para o modelo completo de KEK/DEK, HSM/KMS, dynamic secrets e o caso Uber 2016, tratado ali em profundidade e apenas referenciado aqui.

Consultado em 2026-07-11.
