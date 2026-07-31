---
title: "HTTP: métodos, status e headers"
created: 2026-06-18
updated: 2026-06-18
type: concept
fase: adepto
status: evergreen
publish: false
tags:
  - ciencia-da-computacao
  - redes
  - protocolos
  - http
  - entrevista
---

# HTTP: métodos, status e headers

> [!abstract] Resumo em uma linha
> HTTP é um protocolo de aplicação no qual o cliente envia um pedido formal (método + caminho + headers + corpo) e o servidor responde com um status numérico e seus próprios headers e corpo — stateless por natureza, ele empurra todo o estado (sessão, cache, autenticação) para os headers.

Imagine que você precisa pedir um documento a um cartório por carta. Você escreve: "Quero a segunda via da certidão nº 42" (o que você quer), assina e identifica quem é você (os headers), e talvez anexe um formulário preenchido (o corpo). O cartório responde com um carimbo: "Deferido", "Não existe esse documento", "Você não tem procuração". HTTP é exatamente isso — cartas formais com regras rígidas de formato e um vocabulário fixo de carimbos.

A parte difícil não é a sintaxe. É a **semântica**: o que cada método *promete*, o que cada status *significa de verdade*, e quais headers *mudam o comportamento* do outro lado. É aí que mora a maioria dos bugs e quase todas as perguntas de entrevista.

> [!note] Esta nota é sobre a semântica do HTTP — o dia a dia
> Como o HTTP/1.1, /2 e /3 movem bytes pela rede é assunto de [[07 - A evolução do HTTP]]. A criptografia do `https://` é [[05 - TLS e HTTPS]]. Aqui ficamos no andar de cima: métodos, status, headers.

## A anatomia de um request

Um request HTTP tem três partes, sempre nessa ordem: a **request line**, os **headers** e (opcionalmente) o **body**.

```http
GET /usuarios/42 HTTP/1.1
Host: api.exemplo.com
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
User-Agent: curl/8.4.0

```

A primeira linha é a única obrigatória em termos estruturais: `MÉTODO CAMINHO VERSÃO`. Depois vêm os headers, um por linha, no formato `Nome: valor`. Uma linha em branco encerra os headers. Se houver corpo (num POST, por exemplo), ele vem depois dessa linha em branco.

Repare que o `GET` acima não tem corpo. Faz sentido — você está *pedindo* algo, não *enviando* nada.

## A anatomia de um response

A resposta espelha o request: **status line**, **headers**, **body**.

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 58
Cache-Control: max-age=300

{"id": 42, "nome": "Ada Lovelace", "ativo": true}
```

A status line é `VERSÃO CÓDIGO FRASE`. O código (`200`) é o que importa para a máquina; a frase (`OK`) é cortesia para humanos. O `Content-Type` diz ao cliente *como interpretar* os bytes do corpo, e o `Content-Length` diz *quantos* bytes esperar.

> [!tip] Leia uma troca HTTP inteira com `curl -v`
> `curl -v https://api.exemplo.com/usuarios/42` mostra as linhas com `>` (o que você mandou) e `<` (o que voltou). É a forma mais rápida de ver request e response crus, com todos os headers. Antes de abrir o DevTools, abra o terminal.

Vamos ver a conversa completa, com o handshake de headers visível.

Diagrama abaixo: uma troca request/response típica, destacando quais headers vão de cada lado.

```mermaid
sequenceDiagram
    participant C as Cliente
    participant S as Servidor
    C->>S: GET /usuarios/42 HTTP/1.1
    Note over C,S: Host, Accept, Authorization
    S-->>C: HTTP/1.1 200 OK
    Note over C,S: Content-Type, Content-Length, Cache-Control
    C->>S: POST /usuarios HTTP/1.1
    Note over C,S: Content-Type + corpo JSON
    S-->>C: HTTP/1.1 201 Created
    Note over C,S: Location: /usuarios/43
```

Leitura do diagrama: o cliente nunca "abre uma sessão" — cada par request/response é autocontido. O `Authorization` precisa viajar em *todo* request, porque o servidor esquece quem você é assim que responde. Note o `201 Created` com `Location` apontando para o recurso recém-criado: é o servidor dizendo "criei, está aqui o endereço".

## Métodos: o verbo do pedido

O método declara a *intenção* da operação. Existem duas propriedades que dominam qualquer conversa séria sobre métodos: **safe** e **idempotente**.

**Safe** (seguro): o método é essencialmente *somente leitura*. O cliente não pede — e não espera — nenhuma mudança de estado no servidor. `GET`, `HEAD` e `OPTIONS` são safe. Isso não quer dizer que o servidor *fisicamente* não possa fazer nada (ele pode logar a requisição); quer dizer que o cliente não é responsável por nenhum efeito colateral.

**Idempotente**: aplicar o método N vezes tem o mesmo efeito *no estado do servidor* que aplicá-lo uma vez. Esta é a propriedade que sustenta os **retries**. Se uma resposta se perde na rede, posso reenviar um `PUT` sem medo de duplicar — o estado final é o mesmo. Reenviar um `POST`? Talvez eu acabe com dois pedidos de compra.

> [!tip] Idempotência é a licença para o retry automático
> Toda política de retry com backoff, circuit breaker, timeout — assunto de [[14 - Resiliência de rede]] — depende dessa propriedade. Você só pode retransmitir cegamente o que é idempotente. `POST` exige uma chave de idempotência (um header que o servidor usa pra detectar duplicatas) para virar seguro pra retry.

Diagrama abaixo: a relação de inclusão entre safe e idempotente.

```mermaid
flowchart TD
    A["Todos os métodos"] --> B["Idempotentes<br/>GET HEAD PUT DELETE OPTIONS"]
    B --> C["Safe / somente-leitura<br/>GET HEAD OPTIONS"]
    A --> D["Não-idempotentes<br/>POST PATCH"]
```

Leitura do diagrama: todo método safe é também idempotente (se não muda nada, repetir não muda nada). Mas o inverso é falso: `PUT` e `DELETE` *mudam* estado, e ainda assim são idempotentes. `POST` e `PATCH` ficam de fora dos dois círculos.

| Método  | Safe | Idempotente | Tem corpo no request? | Para quê |
|---------|------|-------------|-----------------------|----------|
| GET     | sim  | sim         | não (em geral)        | Ler um recurso |
| HEAD    | sim  | sim         | não                   | Como GET, mas só os headers (sem corpo na resposta) |
| OPTIONS | sim  | sim         | não                   | Descobrir capacidades/permissões (usado no preflight de CORS) |
| POST    | não  | **não**     | sim                   | Criar recurso, disparar processamento |
| PUT     | não  | sim         | sim                   | Substituir o recurso inteiro |
| PATCH   | não  | **não** (na prática) | sim          | Atualizar *parcialmente* o recurso |
| DELETE  | não  | sim         | às vezes              | Remover o recurso |

### A pegadinha do PATCH

`PUT` é idempotente porque você manda o recurso *completo*: "o usuário 42 agora é exatamente isto". Mandar isso dez vezes deixa o usuário no mesmo estado.

`PATCH` é o problema clássico de entrevista. A RFC define `PATCH` como **não idempotente**, e por boa razão: o corpo de um PATCH descreve uma *transformação*, não um estado final. Se o patch for `{"saldo": "+10"}` (incremente em 10), aplicar dez vezes some 100, não 10. Mesmo um patch que *parece* idempotente (`{"nome": "Ada"}`) não tem garantia formal — o servidor pode ter regras que tornam a operação dependente do estado anterior.

> [!warning] PATCH "parece" idempotente, mas a especificação não garante
> Não conte com a idempotência do PATCH para retries automáticos. Se precisa de retry seguro num update parcial, ou use `PUT` (estado completo), ou adicione uma chave de idempotência explícita. Tratar PATCH como idempotente "porque o meu sempre é" é como dirigir sem cinto porque você nunca bateu.

### PUT × POST × PATCH

- **POST `/usuarios`**: "crie um usuário novo". O *servidor* escolhe a URL do recurso criado (devolvida em `Location`). Não idempotente — dois POSTs criam dois usuários.
- **PUT `/usuarios/42`**: "faça o usuário 42 ser exatamente este objeto". O *cliente* dita a URL. Cria se não existe, substitui se existe. Idempotente.
- **PATCH `/usuarios/42`**: "aplique esta mudança parcial ao usuário 42". Só os campos enviados mudam.

## Status codes: o carimbo da resposta

Todo response carrega um código de três dígitos. O primeiro dígito define a *família*, e ele já te diz quase tudo:

- **1xx** — Informativo. Provisório (raro no dia a dia; `100 Continue`, `101 Switching Protocols`).
- **2xx** — Sucesso. Deu certo.
- **3xx** — Redirecionamento. "O que você quer está em outro lugar / não mudou".
- **4xx** — Erro do *cliente*. Você errou: pedido malformado, sem permissão, recurso inexistente.
- **5xx** — Erro do *servidor*. Ele errou: bug, sobrecarga, dependência fora.

A fronteira 4xx/5xx é semântica e importa: ela diz *de quem é a culpa*. Um 4xx significa "não adianta repetir o mesmo pedido". Um 5xx significa "o pedido pode estar certo; tente de novo".

Diagrama abaixo: a árvore de decisão que o servidor percorre ao escolher um status.

```mermaid
flowchart TD
    Start["Chegou um request"] --> Auth{"Cliente está<br/>autenticado?"}
    Auth -->|"não tem credencial"| C401["401 Unauthorized"]
    Auth -->|sim| Perm{"Tem permissão<br/>pra isso?"}
    Perm -->|não| C403["403 Forbidden"]
    Perm -->|sim| Exists{"Recurso<br/>existe?"}
    Exists -->|não| C404["404 Not Found"]
    Exists -->|sim| Valid{"Pedido é<br/>válido?"}
    Valid -->|"sintaxe ruim"| C400["400 Bad Request"]
    Valid -->|"semântica ruim"| C422["422 Unprocessable"]
    Valid -->|sim| Server{"Servidor<br/>conseguiu processar?"}
    Server -->|"bug interno"| C500["500 Internal Error"]
    Server -->|"upstream falhou"| C502["502 / 503 / 504"]
    Server -->|sim| C2xx["2xx Sucesso"]
```

Leitura do diagrama: a ordem das checagens não é arbitrária. Autenticação vem antes de autorização (não dá pra saber se você *pode* algo sem saber *quem* você é), e ambas vêm antes de mexer no recurso. É por isso que um endpoint protegido devolve 401 mesmo para um recurso inexistente: ele recusa antes de chegar perto do banco.

### Os códigos que todo dev precisa saber

| Código | Nome | Quando |
|--------|------|--------|
| 200 | OK | Sucesso com corpo (resposta de GET, por exemplo) |
| 201 | Created | Recurso criado; mande `Location` apontando pra ele |
| 204 | No Content | Sucesso *sem* corpo (DELETE bem-sucedido, PUT sem retorno) |
| 301 | Moved Permanently | Mudou de URL pra sempre; atualize seus links |
| 302 | Found | Redirecionamento temporário |
| 304 | Not Modified | "Seu cache ainda vale" — resposta a request condicional |
| 400 | Bad Request | Sintaxe inválida; o servidor nem conseguiu parsear |
| 401 | Unauthorized | Falta autenticação (veja abaixo) |
| 403 | Forbidden | Autenticado, mas sem permissão (veja abaixo) |
| 404 | Not Found | Recurso não existe |
| 409 | Conflict | Conflito de estado (ex.: edição concorrente, recurso já existe) |
| 422 | Unprocessable Entity | Sintaxe ok, mas semântica/validação falhou (e-mail inválido) |
| 429 | Too Many Requests | Rate limit estourado |
| 500 | Internal Server Error | Bug genérico no servidor |
| 502 | Bad Gateway | Proxy recebeu resposta inválida do upstream |
| 503 | Service Unavailable | Servidor temporariamente fora (sobrecarga, manutenção) |
| 504 | Gateway Timeout | Proxy esperou demais pelo upstream |

> [!note] 304 e o cache
> O `304 Not Modified` é a peça central do cache de revalidação: o cliente pergunta "ainda vale?" com `If-None-Match`/`If-Modified-Since`, e o servidor responde `304` sem corpo, economizando banda. O mecanismo completo (`ETag`, `Cache-Control`, validação vs. expiração) está em [[08 - Caching HTTP]].

### 401 × 403: a confusão clássica

Esses dois são *o* tropeço de iniciante, e a entrevista adora cobrar.

- **401 Unauthorized** = **autenticação**. "Não sei quem você é." Faltou credencial, ou ela é inválida/expirada. A correção é *fazer login / mandar um token válido*. A RFC exige que o 401 venha com o header `WWW-Authenticate`, dizendo qual esquema usar — é o servidor *convidando* você a se identificar.
- **403 Forbidden** = **autorização**. "Sei quem você é, mas você não pode." A credencial é válida; o problema é permissão. Fazer login de novo *não resolve nada* — um usuário comum nunca virará admin só re-autenticando.

> [!warning] A regra de bolso do 401 vs 403
> Se *mandar credenciais melhores* resolveria o problema → **401**. Se não resolveria (você simplesmente não tem direito) → **403**. O nome "Unauthorized" do 401 é um erro histórico infeliz: ele é sobre autentic**ação**, não autoriz**ação**.

### 502 × 503 × 504: os erros de gateway

Quando há um proxy/load balancer na frente da sua aplicação (o caso normal em produção), a família 5xx se refina:

- **502 Bad Gateway** — o proxy *recebeu* uma resposta do servidor de trás, mas ela era inválida/corrompida. Em geral: a app crashou e devolveu lixo.
- **503 Service Unavailable** — o servidor está temporariamente indisponível por escolha: sobrecarga, manutenção, sem capacidade. Costuma vir com `Retry-After`.
- **504 Gateway Timeout** — o proxy *esperou* uma resposta do upstream e ela não chegou a tempo. A app está lenta ou travada, não morta.

A distinção é diagnóstico puro: 502 = "respondeu errado", 503 = "recusou agora, tente depois", 504 = "demorou demais".

### 429 e o Retry-After

`429 Too Many Requests` é o servidor dizendo "calma". Ele frequentemente acompanha o header `Retry-After`, que diz quantos segundos esperar (ou uma data) antes de tentar de novo. Um cliente educado *respeita* esse header — ignorá-lo e martelar o servidor é receita pra ser banido. O mesmo `Retry-After` aparece em `503`.

## Headers essenciais

Headers são os metadados da carta. Alguns que você encontra todo dia:

- **Host** — diz *qual site* você quer, mesmo que vários compartilhem o mesmo IP (virtual hosting). Como um único servidor pode hospedar `a.com` e `b.com` no mesmo endereço, o servidor precisa do `Host` pra saber qual atender. Por isso ele virou **obrigatório** no HTTP/1.1.
- **Content-Type** — o formato do corpo: `application/json`, `text/html`, `multipart/form-data`. Sem ele, o outro lado adivinha (e adivinha errado).
- **Content-Length × Transfer-Encoding: chunked** — duas formas de delimitar o corpo. `Content-Length: 58` diz o tamanho exato de antemão. `Transfer-Encoding: chunked` envia o corpo em pedaços, sem saber o total no início (streaming, respostas geradas dinamicamente). Os dois são mutuamente exclusivos.
- **Authorization** — onde vai a credencial, tipicamente `Authorization: Bearer <token>`. Como o HTTP é stateless, esse header viaja em *todo* request protegido.
- **Accept** — content negotiation: o cliente diz quais formatos aceita (`Accept: application/json`), e o servidor escolhe o melhor que sabe produzir.
- **User-Agent** — identifica o cliente (navegador, lib, bot).

> [!note] Headers de cache e CORS moram em notas próprias
> `Cache-Control`, `ETag`, `Expires`, `Vary` — o sistema de cache do HTTP — estão em [[08 - Caching HTTP]]. Já `Access-Control-Allow-Origin`, `Origin`, e a dança do preflight com `OPTIONS` vivem em [[09 - CORS e a same-origin policy]]. Aqui só sinalizamos que existem.

## Stateless — e como cookies/sessão trapaceiam

Eis a verdade incômoda: **o HTTP não tem memória**. Cada request é uma carta nova, sem contexto. O servidor responde e esquece. Isso é uma decisão de design deliberada — servidores stateless escalam horizontalmente sem suar, porque qualquer instância pode atender qualquer request.

Mas a web *parece* ter memória: você faz login uma vez e fica logado. Como? Cookies e tokens *reintroduzem* o estado por cima de um protocolo que não o tem.

```mermaid
sequenceDiagram
    participant B as Browser
    participant S as Servidor
    B->>S: POST /login (usuario + senha)
    S-->>B: 200 OK + Set-Cookie: sid=abc, HttpOnly, Secure
    Note over B: browser guarda o cookie
    B->>S: GET /perfil + Cookie: sid=abc
    S-->>B: 200 OK (servidor reconhece a sessão)
```

Leitura do diagrama: o `Set-Cookie` na resposta do login instrui o browser a guardar um identificador. Em cada request seguinte, o browser anexa `Cookie: sid=abc` automaticamente, e o servidor reconstrói "quem é você" a partir dele. O estado não está no HTTP — está numa tabela do servidor (ou num token assinado), referenciada pelo cookie.

Atributos importantes do `Set-Cookie`:

- **HttpOnly** — JavaScript não consegue ler o cookie (defesa contra XSS roubar a sessão).
- **Secure** — o cookie só viaja por HTTPS.
- **SameSite** — controla se o cookie acompanha requests cross-site (defesa contra CSRF).

> [!note] Isto é uma pincelada, não uma nota de autenticação
> Os mecanismos de auth (JWT, OAuth, fluxos de sessão) têm vida própria. Aqui o ponto é só: o HTTP é stateless por baixo, e o estado é um truque construído sobre headers.

## REST × HTTP: não confunda o protocolo com o estilo

Última armadilha conceitual, e talvez a mais comum. **HTTP é o protocolo. REST é um estilo arquitetural que se *apoia* no HTTP.**

REST (Representational State Transfer) é um conjunto de *convenções*: modelar coisas como recursos com URLs (`/usuarios/42`), usar os métodos HTTP segundo a semântica deles (GET lê, DELETE remove), apoiar-se nos status codes. Mas REST não é HTTP, e HTTP não é REST. Você pode usar HTTP de forma não-RESTful (uma RPC que faz tudo via POST em `/api`), e poderia teoricamente fazer REST sobre outro transporte.

> [!tip] Onde cada parte de REST mora no Codex
> A comparação de REST com GraphQL e gRPC *enquanto estilos de comunicação* é de [[10 - REST, GraphQL e gRPC]]. Já o *design* de uma API REST — versionamento, paginação, formato do contrato de erro, HATEOAS, naming de endpoints — é território de [[API Design]]. Esta nota cobre só a camada HTTP que está embaixo de tudo isso. Não duplique; linke.

## Em entrevista

A few framings that land well in English.

- "HTTP is a stateless, request/response application protocol. Every message is self-contained — the server forgets you after each response, which is exactly why it scales horizontally."
- "The two properties that matter for methods are *safe* (read-only, no state change) and *idempotent* (N calls equal one call). GET, PUT and DELETE are idempotent; POST and PATCH are not."
- "Idempotency is what licenses automatic retries. If a response is lost, I can safely re-send a PUT. To make POST retry-safe I add an idempotency key."
- "The classic gotcha: PATCH is *not* idempotent per the spec, because its body describes a transformation, not a final state."
- "401 means I don't know who you are — fix it with credentials. 403 means I know you but you can't — re-authenticating won't help. The rule of thumb: if better credentials would fix it, it's 401."
- "Among 5xx behind a proxy: 502 is a bad upstream response, 503 is temporarily unavailable, 504 is an upstream timeout."

### Vocabulário

- método seguro → safe method
- método idempotente → idempotent method
- chave de idempotência → idempotency key
- código de status → status code
- redirecionamento → redirect
- negociação de conteúdo → content negotiation
- sem estado → stateless
- corpo da requisição → request body
- cabeçalho → header
- hospedagem virtual → virtual hosting
- nova tentativa → retry
- limite de taxa → rate limit

> [!info] Lastro
> - [RFC 9110 — HTTP Semantics (IETF Datatracker)](https://datatracker.ietf.org/doc/html/rfc9110) — a especificação consolidada de métodos, status e a definição formal de safe e idempotente; confirma que OPTIONS, HEAD, GET, PUT e DELETE são idempotentes e POST/PATCH não.
> - [MDN — 403 Forbidden](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/403) — referência sobre a distinção autenticação (401) vs. autorização (403) e o papel do header `WWW-Authenticate`.
> - [Auth0 — Forbidden (403), Unauthorized (401), or What Else?](https://auth0.com/blog/forbidden-unauthorized-http-status-codes/) — discussão prática da regra de bolso "credenciais melhores resolveriam?".

## Veja também

- [[07 - A evolução do HTTP]] — como os bytes viajam (HTTP/1.1, /2, /3); aqui foi a semântica
- [[08 - Caching HTTP]] — `Cache-Control`, `ETag`, `304` e revalidação em detalhe
- [[09 - CORS e a same-origin policy]] — os headers de origem e o preflight com OPTIONS
- [[10 - REST, GraphQL e gRPC]] — estilos de comunicação sobre (e além de) HTTP
- [[05 - TLS e HTTPS]] — a camada de criptografia abaixo do `https://`
- [[14 - Resiliência de rede]] — retries, timeouts e por que idempotência é pré-requisito
- [[API Design]] — versionamento, paginação, contrato de erro e HATEOAS
- [[15 - Redes em entrevista]] — drill de perguntas, incluindo 401×403 e idempotência
- [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]]
