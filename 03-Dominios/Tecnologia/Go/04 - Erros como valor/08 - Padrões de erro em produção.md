---
title: "Padrões de erro em produção"
type: concept
fase: magus
tags:
  - go
  - erros
  - errors-join
  - logging-estruturado
  - api-design
  - producao
publish: true
created: 2026-07-18
updated: 2026-07-18
---

# Padrões de erro em produção

> [!abstract] TL;DR
> Sete notas atrás você aprendeu que `error` é só um valor. Esta nota fecha o galho tratando esse valor como parte do **contrato público** da sua API — o que você expõe em `error` é tão promessa de compatibilidade quanto qualquer struct ou assinatura de função. `errors.Join` (Go 1.20) resolve o problema de "preciso reportar mais de um erro do mesmo resultado" — validação de formulário, `Close()` que falha depois que a operação principal já falhou — produzindo um único `error` que `errors.Is`/`errors.As` continuam percorrendo normalmente. Erros bem desenhados carregam dados estruturados (não só texto) para alimentar `log/slog` sem parsing de string. E a regra de ouro: erro que atravessa a fronteira do seu módulo nunca deve vazar detalhes internos — nem tipo concreto não-exportado, nem stack trace de biblioteca terceira, nem paths de arquivo do seu disco.

## O problema: seu erro é uma promessa que você não pode quebrar

Imagine que você mantém um pacote `billing` usado por seis times diferentes. Uma função sua retorna `error`. Um desses times, num code review de sexta-feira, decide fazer isto:

```go
if err != nil {
    var insufFundsErr *billing.InsufficientFundsError
    if errors.As(err, &insufFundsErr) {
        // oferece parcelamento
    }
}
```

Funciona, compila, passa no CI. Seis meses depois você refatora `billing` internamente — troca `*InsufficientFundsError` por um `sentinel` genérico `ErrPayment`, porque parecia mais simples. O código do outro time quebra silenciosamente: `errors.As` para de casar, o parcelamento nunca é oferecido, e ninguém recebe erro de compilação avisando — o `errors.As` continua compilando, só passa a retornar `false` sempre. Você não versionou uma função nem um struct exportado. Você versionou, sem perceber, um **tipo de erro** — e quebrou o contrato do mesmo jeito que quebraria removendo um campo de struct público.

Esse é o ângulo que faltava nas seis notas anteriores. Elas ensinaram o mecanismo — `error` é interface, `%w` encadeia, `errors.Is`/`As` percorrem a cadeia, `panic`/`recover` são coisa distinta, cada estratégia de tratamento tem seu lugar. Esta nota assume que você já sabe operar as peças e faz a pergunta que só aparece em produção: **o que você expõe em `error` é API, e API pública se projeta, não se improvisa**.

```mermaid
flowchart TB
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    A["Erro interno da função"] --> B{"Vai atravessar\na fronteira do pacote?"}
    B -->|"Sim — é API pública"| C["Projete: tipo exportado?\nsentinel exportado?\nsó string?"]
    B -->|"Não — fica interno"| D["Livre para mudar\nsem quebrar ninguém"]
    C --> E["Documente no godoc\ncomo parte do contrato"]
    C --> F["Mudar depois =\nbreaking change"]

    class C destaque
    class F neutro
```

## Erro como parte da API pública

O ponto de partida é simples de enunciar e fácil de esquecer no dia a dia: **todo `error` que uma função exportada pode retornar é parte do seu contrato público**, no mesmo sentido que os parâmetros e o tipo de retorno são. Isso vale em três camadas, cada uma com um nível diferente de compromisso:

1. **"A função pode falhar"** — o compromisso mínimo. Documentado só pela presença de `error` na assinatura. Quebrar isso (deixar de retornar erro nunca) não é breaking change; passar a retornar erro num caso que antes tinha sucesso, é.
2. **"O erro, às vezes, é um sentinel específico"** — `var ErrNotFound = errors.New("not found")`, exportado, testável com `errors.Is(err, pkg.ErrNotFound)`. Documente no godoc da função quais sentinels ela pode retornar. Remover um sentinel exportado, ou parar de retorná-lo num caso onde antes era retornado, quebra qualquer chamador que fez `errors.Is` contra ele.
3. **"O erro, às vezes, carrega dados estruturados"** — um tipo exportado como `*InsufficientFundsError` com campos (`Requested`, `Available`), testável com `errors.As`. Esse é o compromisso mais caro de manter: o chamador pode estar lendo campos específicos do struct, não só checando a presença do erro.

A regra prática, que a própria [documentação do pacote `errors`](https://pkg.go.dev/errors) reforça ao tratar sentinels e tipos como cidadãos de primeira classe: **decida deliberadamente, para cada função exportada, em qual dessas três camadas ela vive** — e documente essa decisão no comentário godoc, do mesmo jeito que você documentaria os parâmetros. "Retorna erro se `id` não existir" é uma frase de godoc incompleta se você quer que o chamador use `errors.Is(err, ErrNotFound)`; a frase completa é "retorna um erro que satisfaz `errors.Is(err, ErrNotFound)` se `id` não existir".

```go
// Get busca o usuário pelo id.
//
// Se o usuário não existir, o erro retornado satisfaz
// errors.Is(err, ErrNotFound). Se a validação do id falhar,
// o erro satisfaz errors.As para *ValidationError.
func Get(id string) (*User, error) {
    if !isValidID(id) {
        return nil, &ValidationError{Field: "id", Reason: "formato inválido"}
    }
    u, ok := store[id]
    if !ok {
        return nil, fmt.Errorf("get %q: %w", id, ErrNotFound)
    }
    return u, nil
}
```

> [!warning] Erro não exportado dentro de erro exportado ainda vaza tipo
> Se `ValidationError` embeda ou envolve um erro de uma dependência interna (ex.: um parser de terceiros), e você usa `%w` ingenuamente, `errors.As` do chamador pode acabar casando contra o tipo do parser interno — que você nunca quis expor. A [[04 - Erros customizados|nota 04]] já mostrou como desenhar tipos de erro; aqui o ponto extra é perguntar, antes de dar `%w` num erro de dependência: "esse tipo concreto é algo que quero que vire parte do meu contrato público, para sempre"? Se não, envolva com `fmt.Errorf("processing config: %v", err)` — `%v` em vez de `%w` — para achatar a cadeia e impedir `errors.As` de alcançar o tipo interno.

## `errors.Join`: quando um resultado tem mais de um erro

Todo o galho, até aqui, tratou "uma operação, um erro". Mas isso não cobre situações reais e comuns: validar um formulário com cinco campos e querer reportar os cinco problemas de uma vez, não só o primeiro; ou fechar múltiplos recursos (`os.Open` de três arquivos) onde mais de um `Close()` pode falhar independentemente.

Antes do Go 1.20, a saída era artesanal — concatenar strings, criar um slice de erros e um tipo `MultiError` próprio, perder a compatibilidade com `errors.Is`/`errors.As` no processo a menos que você reimplementasse `Is`/`As` manualmente. A [Go 1.20 release notes](https://go.dev/doc/go1.20) resolveu isso na biblioteca padrão com `errors.Join`:

> [!info] `errors.Join` — Go 1.20
> `func Join(errs ...error) error` combina múltiplos erros num único valor `error`. Erros `nil` no meio da lista são ignorados. Se todos forem `nil`, `Join` retorna `nil`. O erro resultante tem `Unwrap() []error` — não `Unwrap() error` como o wrapping simples — e é justamente essa assinatura que ensina `errors.Is`/`errors.As` a percorrer **múltiplas** cadeias de causa a partir de um único valor.

```go
func ValidarFormulario(f Formulario) error {
    var erros []error

    if f.Nome == "" {
        erros = append(erros, fmt.Errorf("campo nome: %w", ErrCampoObrigatorio))
    }
    if f.Email == "" {
        erros = append(erros, fmt.Errorf("campo email: %w", ErrCampoObrigatorio))
    }
    if f.Idade < 0 {
        erros = append(erros, fmt.Errorf("campo idade: %w", ErrValorInvalido))
    }

    return errors.Join(erros...)
}
```

```go
err := ValidarFormulario(f)
if err != nil {
    fmt.Println(err)
    // campo nome: obrigatório
    // campo email: obrigatório
}

if errors.Is(err, ErrCampoObrigatorio) {
    // true se PELO MENOS UM dos erros unidos satisfizer ErrCampoObrigatorio
}
```

`err.Error()` já formata cada erro unido numa linha própria, separadas por `\n` — não é preciso montar essa string na mão. E `errors.Is`/`errors.As`, sem código extra seu, atravessam a árvore inteira de erros unidos, retornando `true` assim que **qualquer um** dos ramos casar.

```mermaid
flowchart TB
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    J["errors.Join(e1, e2, e3)"]
    J --> E1["e1: campo nome"]
    J --> E2["e2: campo email"]
    J --> E3["e3: campo idade"]
    E1 -.->|"Unwrap() []error"| J
    E2 -.->|"Unwrap() []error"| J
    E3 -.->|"Unwrap() []error"| J

    Q["errors.Is(err, ErrCampoObrigatorio)"] -.->|"percorre todos os ramos"| J

    class J destaque
    class Q neutro
```

O segundo caso de uso clássico — múltiplos `Close()` — aparece direto na própria [documentação do pacote `errors`](https://pkg.go.dev/errors#Join):

```go
func ProcessarArquivos(paths []string) (err error) {
    var arquivos []*os.File
    defer func() {
        for _, f := range arquivos {
            err = errors.Join(err, f.Close())
        }
    }()

    for _, p := range paths {
        f, abrirErr := os.Open(p)
        if abrirErr != nil {
            return errors.Join(err, abrirErr)
        }
        arquivos = append(arquivos, f)
    }

    // ... processa arquivos ...
    return nil
}
```

Repare no padrão: `err = errors.Join(err, f.Close())` acumula erros de fechamento **sem descartar** um erro anterior que já estivesse em `err` — o mesmo problema que a [[05 - panic e recover|nota 05]] tocou de raspão ao falar de `defer` engolindo erro de `Close()`. `errors.Join(nil, algumErro)` retorna só `algumErro`; `errors.Join(err, nil)` retorna só `err`; os dois juntos combinam.

> [!warning] `errors.Join` não substitui `fmt.Errorf("...: %w", err)` — são ferramentas para problemas diferentes
> Wrapping com `%w` (nota 03) modela **uma cadeia de causa** — "isto falhou porque aquilo falhou", uma relação hierárquica de um único erro raiz. `errors.Join` modela **uma coleção de erros irmãos, sem relação de causa entre si** — cinco campos de formulário inválidos não "causaram" um ao outro, são falhas paralelas e independentes do mesmo resultado. Usar `Join` para uma cadeia de causa perde a semântica de "A por causa de B"; usar `%w` repetidamente para acumular erros paralelos perde erros anteriores a cada `Errorf` novo. Escolha pelo formato do problema: hierarquia → `%w`; coleção → `Join`.

## Logging estruturado de erro: parar de vazar contexto em string

Um erro bem desenhado, com sentinel e tipo customizado, ainda pode virar um pesadelo de observabilidade se o único lugar onde ele chega for um `log.Println(err.Error())`. Você perde a estrutura: `err.Error()` é uma string plana ("get user 42: not found"), e sistemas de observabilidade modernos (Datadog, Grafana Loki, CloudWatch Logs Insights) trabalham melhor com campos separados — `user_id=42`, `error_type=not_found` — do que fazendo regex em cima de mensagem livre.

> [!info] `log/slog` — Go 1.21
> A biblioteca padrão ganhou um logger estruturado nativo em 1.21, documentado na [Go 1.21 release notes](https://go.dev/doc/go1.21) e no [pacote `log/slog`](https://pkg.go.dev/log/slog). Antes disso, projetos usavam bibliotecas de terceiros (`zap`, `zerolog`, `logrus`) para log estruturado — `slog` não as substitui necessariamente em todo lugar, mas dá uma opção na stdlib que qualquer módulo pode assumir sem dependência extra.

O ponto de conexão entre "erro bem desenhado" e "log estruturado" é este: se seu erro carrega dados em campos (como `*ValidationError{Field, Reason}` da seção anterior), esses mesmos campos podem virar atributos do log, em vez de serem só interpolados numa string:

```go
type ValidationError struct {
    Field  string
    Reason string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("campo %s: %s", e.Field, e.Reason)
}

// No ponto de tratamento — não na função que gerou o erro:
if err != nil {
    var ve *ValidationError
    if errors.As(err, &ve) {
        slog.Error("validação falhou",
            "field", ve.Field,
            "reason", ve.Reason,
            "error", err,
        )
    } else {
        slog.Error("erro inesperado", "error", err)
    }
}
```

`slog.Error` recebe pares chave-valor — não uma string formatada — e o backend configurado (JSON handler, por exemplo) grava `field` e `reason` como campos pesquisáveis, independentes da mensagem textual. Isso é só um teaser: o galho 16 desta trilha trata log estruturado, correlação de trace e integração com backends de observabilidade em profundidade — a costura entre "erro bem tipado" e "log estruturado" aqui é intencionalmente breve, o bastante para você não terminar este galho achando que erro e log são assuntos desconectados.

```mermaid
sequenceDiagram
    participant F as "Função que falha"
    participant C as "Chamador (ponto de tratamento)"
    participant L as "slog"
    participant O as "Backend de observabilidade"

    F->>C: retorna &ValidationError{Field, Reason}
    C->>C: errors.As(err, &ve)
    C->>L: slog.Error("validação falhou", "field", ve.Field, "reason", ve.Reason)
    L->>O: JSON estruturado, campos pesquisáveis
    Note over O: busca por field="email" funciona<br/>sem parsear string de erro
```

> [!warning] Não logue o mesmo erro em cada camada que ele atravessa
> Um erro que sobe de `repository` → `service` → `handler` HTTP, se cada camada faz `slog.Error(err)` antes de repropagar, produz três (ou mais) linhas de log para uma única falha — poluindo o volume de logs e dificultando correlação. A regra prática: logue erro **uma vez**, no ponto onde ele é finalmente tratado ou vira resposta ao usuário (normalmente a borda — handler HTTP, worker de fila, `main`). Camadas intermediárias só envolvem com contexto (`%w`) e repropagam; não logam.

## Não vazar internals: a fronteira do módulo importa

O tema que amarra tudo nesta nota: qualquer erro que sai do seu módulo — atravessa uma API HTTP, uma resposta de gRPC, ou simplesmente a fronteira pública de um pacote Go que você distribui — precisa ser **filtrado**, não repassado cru.

Três formas concretas de vazamento, das mais sutis às mais óbvias:

**1. Tipo concreto não-exportado escapando via `%w`.** Se sua função pública envolve um erro de uma dependência interna com `%w`, o tipo concreto dessa dependência agora é alcançável via `errors.As` por qualquer chamador — mesmo que você nunca tenha documentado ou pretendido isso. Trocar a dependência interna depois quebra silenciosamente quem fez `errors.As` contra o tipo antigo.

**2. Mensagem de erro com paths de arquivo, credenciais parciais ou detalhes de infraestrutura.** `fmt.Errorf("conectando a postgres://user:senha@10.0.4.12:5432/prod: %w", err)` — se esse erro alcança um log agregador com acesso amplo, ou pior, uma resposta HTTP de erro ao cliente, você vazou topologia interna de rede e possivelmente credencial. A regra: erro que cruza a borda do processo (resposta HTTP, por exemplo — tema do galho 10 desta trilha, sobre APIs HTTP e REST) carrega uma mensagem **genérica e segura** para o cliente, com o erro completo e detalhado indo só para o log interno.

**3. Stack trace ou erro de terceiro repassado sem tradução.** Se `pkg.Foo()` chama uma biblioteca terceira e propaga o erro dela sem qualquer wrapping, seu pacote acabou de acoplar seus chamadores ao tipo de erro de uma dependência que você pode querer trocar depois. Envolva com um tipo ou sentinel seu — mesmo que a mensagem final inclua `%v` do erro original para debug — para manter o contrato sob seu controle.

```go
// Vazamento: tipo concreto de driver de banco escapa da API pública
func (r *Repo) Get(id string) (*User, error) {
    row := r.db.QueryRow(...)
    var u User
    if err := row.Scan(&u.Name); err != nil {
        return nil, err // *pgconn.PgError vaza cru — chamador acopla ao driver
    }
    return &u, nil
}

// Filtrado: contrato próprio, driver escondido
func (r *Repo) Get(id string) (*User, error) {
    row := r.db.QueryRow(...)
    var u User
    if err := row.Scan(&u.Name); err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, fmt.Errorf("get user %q: %w", id, ErrNotFound)
        }
        return nil, fmt.Errorf("get user %q: %w", id, ErrRepositorio)
    }
    return &u, nil
}
```

A segunda versão expõe só `ErrNotFound` e `ErrRepositorio` — dois sentinels que você controla, documenta e mantém estáveis — em vez do tipo interno do driver de banco (`pgconn.PgError`, `sqlite3.Error`, o que for). Trocar de driver de banco depois não quebra ninguém que consome `Repo`.

> [!warning] "Não vazar internals" não é o mesmo que "esconder informação de debug"
> A regra é sobre a **fronteira pública** — o que atravessa para outro módulo, outro time, ou o cliente HTTP. Dentro do seu próprio processo, no log interno, o erro original (com `%w` e toda a cadeia) deve continuar acessível — é exatamente ele que `errors.Is`/`As` e o log estruturado da seção anterior usam para diagnóstico. Filtrar na fronteira pública e preservar detalhe no log interno não são objetivos conflitantes; são a mesma disciplina aplicada em dois lugares diferentes.

## Lente cross-stack

| Vindo de | Em Go, isso vira |
|---|---|
| Java: `throws IOException, SQLException` na assinatura (checked exceptions documentam o contrato) | Comentário godoc dizendo quais sentinels/tipos `errors.Is`/`As` a função pode satisfazer — mesma intenção, sem suporte do compilador |
| Java: exceção customizada estende `RuntimeException` com campos próprios | Struct que implementa `error`, com campos exportados (nota 04) — carrega dados estruturados igual |
| Python: `raise ExceptionGroup([e1, e2, e3])` (3.11+) para agrupar exceções paralelas | `errors.Join(e1, e2, e3)` (Go 1.20) — mesma motivação, chegou em Go um pouco antes |
| Node: `logger.error({ err, userId, field })` com objeto estruturado | `slog.Error("msg", "err", err, "userId", id, "field", f)` — pares chave-valor em vez de objeto, mesma ideia de campo pesquisável |
| Qualquer linguagem: "nunca devolva a stack trace crua pro cliente HTTP" | Mesma regra, sem exceção — mensagem genérica pro cliente, detalhe completo só no log interno |

## Como explicar em inglês

> Once an error crosses a package or API boundary, it stops being an implementation detail and becomes part of your public contract — exactly like a function signature. Wrapping an internal error with `%w` and exposing it accidentally makes callers able to `errors.As` against a type you never meant to promise. `errors.Join`, added in Go 1.20, solves the "more than one error from the same operation" problem — form validation, multiple `Close()` calls in a deferred cleanup — by producing a single `error` whose `Unwrap() []error` keeps `errors.Is` and `errors.As` working across every joined branch. For observability, attach structured fields to `log/slog` calls instead of interpolating error details into a flat string — it's what lets a backend search by field, not regex a message. And at any boundary that leaves your process — an HTTP response, a public API — never forward a raw internal error: strip it down to a stable sentinel or your own error type, and keep the full detail for internal logs only.

| Termo PT | Termo EN |
|---|---|
| erro como parte da API pública | error as part of the public API |
| contrato de erro | error contract |
| erro unido / erros unidos | joined error |
| erros irmãos, sem relação de causa | sibling errors, no causal relation |
| log estruturado | structured logging |
| campo pesquisável | searchable field |
| vazar internals | leak internals |
| fronteira do módulo/processo | module/process boundary |

## O que vem a seguir

Este galho fechou o ciclo completo de erros em Go — do `error` como interface simples até o desenho de contratos de erro para produção. O próximo passo natural é olhar para o que esses erros costumam envolver: dados. O **Galho 5 — Coleções e dados** entra em slices, maps, arrays e as garantias (e armadilhas) de cada um — a base de dados sobre a qual quase todo código Go, incluindo o tratamento de erro que você acabou de estudar, realmente opera.

## Veja também

- [[01 - Erros são valores — o tipo error|01 — Erros são valores — o tipo error]] — fundação: `error` como interface, o ponto de partida deste galho
- [[03 - Error wrapping e a cadeia de erros|03 — Error wrapping e a cadeia de erros]] — `%w`, `errors.Is`/`As`, a cadeia que `errors.Join` estende para múltiplos ramos
- [[04 - Erros customizados|04 — Erros customizados]] — desenho de tipos de erro com campos, retomado aqui sob a lente de API pública
- [[05 - panic e recover|05 — panic e recover]] — `defer` acumulando erro de `Close()`, tema que volta no exemplo de `errors.Join`
- [[06 - Estratégias de tratamento de erro|06 — Estratégias de tratamento de erro]] — onde tratar vs. onde propagar, pré-requisito da regra "logue uma vez, na borda"
- [[07 - Erros vs exceções|07 — Erros vs exceções]] — comparação de modelo que esta nota assume como pano de fundo
- [[03-Dominios/Tecnologia/Go/index|Trilha Go]]

## Fontes

- The Go Authors. *Go 1.20 Release Notes — errors.Join*. go.dev. https://go.dev/doc/go1.20 (acessado em 2026-07-18)
- The Go Authors. *Package errors*. pkg.go.dev. https://pkg.go.dev/errors (acessado em 2026-07-18)
- The Go Authors. *Go 1.21 Release Notes — log/slog*. go.dev. https://go.dev/doc/go1.21 (acessado em 2026-07-18)
- The Go Authors. *Package log/slog*. pkg.go.dev. https://pkg.go.dev/log/slog (acessado em 2026-07-18)
- The Go Authors. *Working with Errors in Go 1.13*. go.dev/blog. https://go.dev/blog/go1.13-errors (acessado em 2026-07-18)
- Go by Example. *Errors*. gobyexample.com. https://gobyexample.com/errors (acessado em 2026-07-18)
