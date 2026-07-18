---
title: "Roteamento"
type: concept
fase: Iniciado
tags:
  - go
  - http
  - roteamento
  - servemux
  - stdlib
publish: true
created: 2026-07-18
updated: 2026-07-18
---

# Roteamento

> [!abstract] TL;DR
> `http.ServeMux` é o roteador da stdlib: um mapa de padrões de URL para `http.Handler`. Até Go 1.21, ele só casava por prefixo de path — sem verbo HTTP, sem parâmetros de rota — o que empurrava quase todo projeto real para um framework (Gin, Chi, Echo) só para ter `GET /users/{id}`. O Go 1.22 mudou isso: o mux ganhou **sintaxe de método** (`"GET /users/{id}"`), **wildcards de path** (`{id}`, `{path...}`) e uma API para ler o valor capturado — `r.PathValue("id")`. Isso não mata os frameworks (eles ainda ganham em middleware ergonômico, grupos de rota e extras), mas muda a pergunta: hoje, para uma API pequena a média, a resposta pode legitimamente ser "a stdlib já basta".

## O problema que o roteador resolve

Um servidor HTTP recebe requisições para dezenas de caminhos diferentes — `/`, `/users`, `/users/42`, `/health`, `/api/posts`. Sem roteador, você escreveria um único handler gigante com um `switch` manual em `r.URL.Path`:

```go
func handler(w http.ResponseWriter, r *http.Request) {
    switch {
    case r.URL.Path == "/":
        homeHandler(w, r)
    case r.URL.Path == "/health":
        healthHandler(w, r)
    case strings.HasPrefix(r.URL.Path, "/users/"):
        userHandler(w, r) // e agora, extrair o ID manualmente da string?
    default:
        http.NotFound(w, r)
    }
}
```

Isso compila e funciona, mas cresce mal: cada rota nova é mais um `case`, extrair `42` de `/users/42` vira manipulação de string à mão, e não há como dizer "só aceito `GET` aqui, `POST` deve dar 405". Um **roteador** (*router*, ou *multiplexer* — daí o nome `ServeMux`) resolve exatamente isso: você registra padrões, ele decide qual handler chamar para cada requisição, e você para de escrever `switch` manual.

## `http.ServeMux`: o roteador da stdlib

A nota anterior já usou `http.ServeMux` sem se deter nele. Ele é o tipo que implementa `http.Handler` fazendo despacho — recebe uma requisição, decide qual handler registrado deve tratá-la, e delega:

```mermaid
flowchart LR
    Req["Requisição\nGET /users/42"] --> Mux["http.ServeMux"]
    Mux -->|"casa \"GET /users/{id}\""| H1["userHandler"]
    Mux -->|"casa \"/health\""| H2["healthHandler"]
    Mux -->|"nenhum padrão casa"| H3["404 Not Found"]

    style Mux fill:#4A90D9,color:#fff
    style H1 fill:#F5A623,color:#000
```

O registro acontece com `Handle` (recebe um `http.Handler`) ou `HandleFunc` (recebe uma função com a assinatura `func(w, r)`, que o Go converte automaticamente para `http.HandlerFunc`):

```go
mux := http.NewServeMux()
mux.HandleFunc("/health", healthHandler)
mux.HandleFunc("/users/", usersHandler)

http.ListenAndServe(":8080", mux)
```

Até aqui, nada mudou desde as primeiras versões de Go — esse é o `ServeMux` "clássico", e ele continua existindo do jeito que sempre existiu. A mudança real está em **como os padrões podem ser escritos** a partir do Go 1.22.

## O novo mux de 1.22: método e wildcards

> [!info] Novidade de Go 1.22 (fevereiro de 2024)
> Antes do 1.22, um padrão de `ServeMux` era só um caminho — `"/users/"` — e casava **qualquer verbo HTTP** nesse prefixo. Extrair `42` de `/users/42` exigia código manual (`strings.TrimPrefix`, `strings.Split`). O Go 1.22 estendeu a sintaxe de padrão para incluir método HTTP e segmentos nomeados (wildcards), sem quebrar nenhum padrão antigo — código pré-1.22 continua compilando e casando do mesmo jeito.

A partir do 1.22, um padrão de rota pode ter três partes: `MÉTODO PATH-COM-WILDCARDS`.

```go
mux := http.NewServeMux()

mux.HandleFunc("GET /users/{id}", getUser)
mux.HandleFunc("POST /users", createUser)
mux.HandleFunc("DELETE /users/{id}", deleteUser)
mux.HandleFunc("GET /files/{path...}", serveFile)

http.ListenAndServe(":8080", mux)
```

Três mecanismos novos, todos na mesma sintaxe de string:

- **Método HTTP como prefixo** — `"GET /users/{id}"` só casa requisições `GET`. Uma requisição `POST` no mesmo path, sem um padrão `POST` registrado, recebe automaticamente `405 Method Not Allowed` — não `404`. Antes do 1.22, isso exigia checar `r.Method` manualmente dentro do handler.
- **Wildcard nomeado de um segmento** — `{id}` casa exatamente um segmento de path (tudo entre duas barras) e dá nome a ele para leitura posterior.
- **Wildcard de múltiplos segmentos** — `{path...}` (com reticências) casa o **restante** do path, incluindo barras adicionais; só é válido no fim do padrão. Útil para servir arquivos ou proxies onde o "resto do caminho" é o dado relevante.

```mermaid
flowchart TB
    P["\"GET /users/{id}\""] --> M["GET"]
    P --> Path["/users/{id}"]
    M -.->|"filtra por verbo\nHTTP"| M
    Path -.->|"{id} = wildcard\nde 1 segmento"| Path

    style M fill:#4A90D9,color:#fff
    style Path fill:#F5A623,color:#000
```

## Lendo o valor capturado: `PathValue`

Registrar `{id}` no padrão só declara *onde* o valor está — para lê-lo dentro do handler, o `*http.Request` ganhou o método `PathValue`:

```go
func getUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id") // string — sempre string, conversão é responsabilidade sua

    n, err := strconv.Atoi(id)
    if err != nil {
        http.Error(w, "id inválido", http.StatusBadRequest)
        return
    }

    fmt.Fprintf(w, "usuário %d", n)
}
```

`r.PathValue("id")` devolve o segmento capturado como `string` — sempre string, porque o roteador não sabe (nem tenta adivinhar) se `{id}` representa um número, um UUID ou um slug. Se `id` não existir no padrão que casou, `PathValue` devolve string vazia — não há pânico, não há erro; é responsabilidade do handler validar.

## Especificidade: quem ganha quando dois padrões casam?

Um detalhe que a documentação da stdlib trata com cuidado: quando mais de um padrão registrado poderia casar a mesma requisição, o `ServeMux` escolhe o **mais específico**, não o primeiro registrado nem o último. Um padrão sem wildcard (`"/users/admin"`) é mais específico que um com wildcard no mesmo lugar (`"/users/{id}"`), então a ordem de `HandleFunc` não importa:

```go
mux.HandleFunc("GET /users/{id}", getUser)
mux.HandleFunc("GET /users/admin", getAdmin) // mais específico — vence mesmo registrado depois

// GET /users/admin → getAdmin (não getUser com id="admin")
// GET /users/42    → getUser, id="42"
```

Essa regra existe justamente para tornar `ServeMux` previsível sem exigir que você preste atenção na ordem de registro — comportamento diferente de roteadores que casam a primeira rota registrada que bater, onde a ordem de `app.get(...)` importa (padrão comum em Express, por exemplo).

## Quando o mux da stdlib basta

Com método e wildcards no lugar, a pergunta "preciso de um framework de roteamento?" ganhou uma resposta genuinamente diferente da era pré-1.22. `ServeMux` cobre bem:

- APIs REST simples a médias, com rotas por recurso (`GET /posts/{id}`, `POST /posts`, `PATCH /posts/{id}`) sem hierarquia profunda de grupos.
- Projetos onde middleware pode ser composto manualmente (nota 04 deste galho) sem precisar da ergonomia de `.Use()` de um framework.
- Times que priorizam **zero dependência externa** — o mux é `net/http`, sempre compatível, sem risco de abandono de terceiros.

Onde a stdlib ainda fica curta, e um framework (nota 05) compensa o custo da dependência:

- **Grupos de rota com prefixo compartilhado** (`/api/v1/...` aplicado a dezenas de rotas de uma vez) — `ServeMux` não tem essa sintaxe nativa; você repete o prefixo em cada padrão ou compõe manualmente.
- **Middleware encadeável com sintaxe dedicada** — a stdlib exige compor `http.Handler`s à mão (nota 04 mostra como); frameworks oferecem `.Use(middleware)` com API própria.
- **Validação e binding automático de corpo/query** — Gin e Echo têm binding de JSON para struct com tags, mensagens de erro prontas; a stdlib exige decodificar manualmente.
- Projetos que já têm o ecossistema de um framework (testes, geração de docs OpenAPI, plugins) amarrado ao seu roteador específico.

> [!warning] `{id}` não valida nada — só captura
> Um wildcard casa qualquer segmento não vazio, incluindo `{id}` = `"abc"` ou `{id}` = `"../../etc"`. `PathValue` nunca valida tipo nem sanitiza — a validação (é número? é um UUID válido? existe no banco?) é sempre responsabilidade do handler. Tratar `PathValue` como dado confiável sem validar é o mesmo erro clássico de tratar query string ou corpo de request como confiável.

> [!warning] Padrão sem barra final e com barra final casam coisas diferentes
> `"/users"` casa **só** `/users` exato. `"/users/"` (com barra final, sem wildcard) casa `/users/` e qualquer coisa abaixo, como um prefixo — comportamento herdado do `ServeMux` pré-1.22. Registrar `"/users"` esperando que ele cubra `/users/42` é um erro comum de quem ainda não migrou mentalmente para os wildcards com nome.

> [!warning] Wildcard sempre ocupa o segmento inteiro — não dá para casar só uma parte
> `{id}` casa um segmento completo entre barras — não é possível escrever algo como `"/users/user-{id}"` esperando que `{id}` capture só o sufixo de `user-42`. Quem vem de expressões regulares ou de roteadores que aceitam padrões parciais dentro de um segmento (alguns frameworks JS aceitam) estranha essa rigidez. A saída, quando o formato do segmento importa, é capturar o segmento inteiro com `{id}` e fazer o parsing manual dentro do handler (`strings.TrimPrefix(r.PathValue("id"), "user-")`).

## Lente cross-stack

| Vindo de | Equivalente ao `ServeMux` novo |
|---|---|
| Node/Express | `app.get('/users/:id', handler)` — sintaxe de parâmetro nomeado é quase idêntica, mas Express casa pela ordem de registro, não por especificidade |
| Python/Flask | `@app.route('/users/<int:id>')` — Flask converte tipo no próprio padrão; `ServeMux` sempre entrega string, conversão é manual |
| Java/Spring | `@GetMapping("/users/{id}")` — mesmíssima ideia de path variable, mas Spring resolve tipo e injeta via reflection; aqui é `PathValue` + `strconv` explícito |

A ideia central — path template com segmento nomeado, valor lido por chave — é praticamente universal entre roteadores web modernos. O que muda é o quanto cada stack automatiza a conversão de tipo e a validação; Go, como de costume, prefere deixar isso explícito no seu código.

## Casos práticos

**1. API mínima com CRUD parcial, só stdlib:**

```go
package main

import (
    "fmt"
    "net/http"
    "strconv"
)

func main() {
    mux := http.NewServeMux()

    mux.HandleFunc("GET /users/{id}", getUser)
    mux.HandleFunc("POST /users", createUser)
    mux.HandleFunc("DELETE /users/{id}", deleteUser)

    http.ListenAndServe(":8080", mux)
}

func getUser(w http.ResponseWriter, r *http.Request) {
    id, err := strconv.Atoi(r.PathValue("id"))
    if err != nil {
        http.Error(w, "id inválido", http.StatusBadRequest)
        return
    }
    fmt.Fprintf(w, "GET usuário %d", id)
}

func createUser(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "usuário criado")
}

func deleteUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    fmt.Fprintf(w, "usuário %s removido", id)
}
```

**2. Wildcard de múltiplos segmentos**, servindo um caminho de arquivo arbitrário:

```go
mux.HandleFunc("GET /static/{path...}", func(w http.ResponseWriter, r *http.Request) {
    caminho := r.PathValue("path") // ex.: "css/estilo.css" para GET /static/css/estilo.css
    fmt.Fprintf(w, "servindo arquivo: %s", caminho)
})
```

**3. Method não permitido devolve 405 automaticamente:**

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "ok")
})

// POST /health, sem padrão POST registrado para esse path:
// → 405 Method Not Allowed, automático, sem código extra no handler.
```

## Como explicar em inglês

> `http.ServeMux` is the standard library's HTTP router — it maps URL patterns to handlers. Before Go 1.22, patterns were plain path prefixes with no method matching and no way to capture path segments, which pushed most real APIs toward a third-party router just to get `GET /users/:id`-style routing. Go 1.22 extended the pattern syntax directly in `net/http`: a pattern can now start with an HTTP method (`"GET /users/{id}"`), and path segments can be named wildcards (`{id}`) or a trailing catch-all (`{path...}`). The captured value is read inside the handler with `r.PathValue("id")`, always as a string — type conversion and validation stay explicit, Go's usual preference. When two registered patterns could match the same request, `ServeMux` picks the more specific one regardless of registration order. For small to medium REST APIs, this new mux is often enough on its own; frameworks still earn their keep for route grouping, chainable middleware syntax, and automatic request binding.

| Termo PT | Termo EN |
|---|---|
| roteador | router |
| multiplexador | multiplexer / mux |
| padrão de rota | route pattern |
| curinga / segmento nomeado | wildcard / path parameter |
| valor de caminho | path value |
| casar (uma rota) | to match (a route) |
| especificidade | specificity |
| catch-all | catch-all wildcard |

## O que vem a seguir

Registrar rota e capturar `{id}` resolve "para onde a requisição vai" — mas dentro do handler ainda falta o essencial: ler o corpo da requisição, decodificar JSON, escrever uma resposta estruturada com o status certo, tratar erros de forma consistente. A [[03 - Request e Response|nota 03]] entra em `*http.Request` e `http.ResponseWriter` a fundo — o par que todo handler já usou de leve nesta nota e na anterior, agora sem atalhos.

## Veja também

- [[01 - O servidor HTTP da stdlib|01 — O servidor HTTP da stdlib]] — `http.Handler`, `http.HandlerFunc` e o ciclo de vida da requisição que o `ServeMux` despacha
- [[03 - Request e Response|03 — Request e Response]] — próxima nota do galho
- [[05 - Frameworks — Gin, Chi, Echo|05 — Frameworks — Gin, Chi, Echo]] — quando o mux da stdlib não basta, o que cada framework agrega
- [[03-Dominios/Tecnologia/Go/index|Trilha Go]]

## Fontes

- The Go Authors. *net/http package documentation — ServeMux*. pkg.go.dev. https://pkg.go.dev/net/http#ServeMux (acessado em 2026-07-18)
- The Go Authors. *Go 1.22 Release Notes — Enhanced routing patterns*. go.dev. https://go.dev/doc/go1.22#enhanced_routing_patterns (acessado em 2026-07-18)
- Jub0bs / The Go Blog. *Routing Enhancements for Go 1.22*. go.dev/blog. https://go.dev/blog/routing-enhancements (acessado em 2026-07-18)
- Go by Example. *HTTP Servers*. gobyexample.com. https://gobyexample.com/http-servers (acessado em 2026-07-18)
