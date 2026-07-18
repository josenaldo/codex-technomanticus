---
title: "Por que generics — o problema antes de 1.18"
type: concept
fase: Iniciado
tags:
  - go
  - generics
  - interface
  - type-assertion
  - historia-da-linguagem
publish: true
created: 2026-07-18
updated: 2026-07-18
---

# Por que generics — o problema antes de 1.18

> [!abstract] TL;DR
> Antes do Go 1.18 (março de 2022), escrever uma função `Max` que funcionasse para `int`, `float64` e qualquer outro numérico exigia escolher entre dois males: **duplicar código** — uma função `MaxInt`, outra `MaxFloat64`, uma para cada tipo — ou aceitar `interface{}` e recuperar o tipo concreto em runtime com **type assertion**, perdendo verificação do compilador e pagando custo de alocação/boxing. Nenhuma das duas é elegante; ambas eram o preço de uma linguagem sem parâmetros de tipo. A comunidade Go resistiu a generics por **anos** — Rob Pike e companhia temiam a complexidade que templates C++ e generics Java trouxeram para essas linguagens — até que o peso da duplicação real, em bibliotecas e código de produção, pesou mais que o medo da complexidade. O resultado, depois de mais de uma década de propostas rejeitadas, foi um design deliberadamente mais simples que o de outras linguagens: **type parameters** com **constraints**, assunto da próxima nota.

## O problema, com as mãos na massa

Imagine que você precisa de uma função que devolve o maior de dois números. Para `int`, é trivial:

```go
func MaxInt(a, b int) int {
    if a > b {
        return a
    }
    return b
}
```

Funciona. Só que amanhã você também precisa comparar `float64`:

```go
func MaxFloat64(a, b float64) float64 {
    if a > b {
        return a
    }
    return b
}
```

O corpo das duas funções é **idêntico** — só o tipo muda. Depois vem `int64`, depois `float32`, depois um tipo próprio como `Duracao` (um `type Duracao int64` do seu domínio). Cada tipo novo que precisa de "o maior entre dois valores" força uma função nova, com o mesmo `if a > b { return a }; return b` copiado e colado, mudando só a assinatura.

Isso não é hipotético: antes do Go 1.18, o próprio pacote padrão sofria disso. A biblioteca `math` tinha `math.Max(a, b float64) float64`, mas não havia uma versão para `int` — quem precisasse comparar inteiros escrevia a própria função, ou usava a saída alternativa que a próxima seção explora.

> [!question]- Por que não usar só `float64` em tudo e converter?
> Dá pra fazer — `MaxInt(a, b int) int { return int(MaxFloat64(float64(a), float64(b))) }` — mas troca um problema por outro: conversões implícitas de `int` para `float64` perdem precisão em inteiros grandes (acima de 2^53), e você paga o custo de duas conversões a cada chamada só para reaproveitar uma função. É gambiarra, não solução.

## Saída 1: duplicar a função por tipo

A primeira saída — a que o exemplo acima já mostrou — é aceitar a duplicação. Para cada tipo que precisa de `Max`, escreva uma função nova:

```go
func MaxInt(a, b int) int {
    if a > b {
        return a
    }
    return b
}

func MaxInt64(a, b int64) int64 {
    if a > b {
        return a
    }
    return b
}

func MaxFloat32(a, b float32) float32 {
    if a > b {
        return a
    }
    return b
}

func MaxFloat64(a, b float64) float64 {
    if a > b {
        return a
    }
    return b
}
```

Isso compila, é rápido em runtime (nenhuma indireção, nenhum boxing — cada função opera diretamente sobre o tipo concreto) e o compilador verifica tudo em tempo de compilação. O problema não é performance, é **manutenção**: quatro funções para manter em sincronia, quatro lugares para corrigir se o algoritmo de comparação mudar (por exemplo, para tratar `NaN` em `float64` de forma especial), e o padrão se multiplica para cada estrutura de dados genérica que você queira escrever — uma pilha (`Stack`) de `int`, outra de `string`, outra de `Pedido`; uma lista encadeada por tipo; um `Set` por tipo.

Bibliotecas de container antes de 1.18 viviam exatamente desse dilema. Quem precisava de uma pilha genérica de verdade tinha duas escolhas ruins: reescrever a pilha para cada tipo de elemento, ou aceitar a saída 2.

## Saída 2: `interface{}` e type assertion

A segunda saída usa o fato de que, em Go, `interface{}` (ou seu apelido moderno, `any`, introduzido também no 1.18 como sinônimo) aceita **qualquer valor** de qualquer tipo. Uma função que recebe `interface{}` não precisa saber, em tempo de compilação, qual tipo concreto vai chegar:

```go
func Max(a, b interface{}) interface{} {
    switch a := a.(type) {
    case int:
        b := b.(int)
        if a > b {
            return a
        }
        return b
    case float64:
        b := b.(float64)
        if a > b {
            return a
        }
        return b
    default:
        panic("tipo não suportado")
    }
}
```

Uma função só, para todos os tipos — resolve a duplicação da saída 1. Mas o preço aparece em três frentes:

```mermaid
flowchart TB
    A["func Max(a, b interface{}) interface{}"] --> B["compila com qualquer tipo,\nmesmo os errados"]
    A --> C["type switch / type assertion\nem runtime"]
    A --> D["boxing: valor + tipo\nalocado no heap"]

    B --> E["Max(3, \"oi\") só falha\nno panic, em produção"]
    C --> F["custo de CPU a cada chamada\npara descobrir o tipo real"]
    D --> G["custo de memória e GC\nque MaxInt nunca paga"]

    style A fill:#4A90D9,color:#fff
    style E fill:#D0021B,color:#fff
    style F fill:#F5A623,color:#000
    style G fill:#F5A623,color:#000
```

**1. Perda de verificação em tempo de compilação.** `Max(3, "oi")` compila sem erro nenhum — `interface{}` aceita `int` e `string` igualmente bem. O `default: panic(...)` só dispara quando esse código *roda*, possivelmente em produção, possivelmente muito depois de escrito. A promessa central de uma linguagem estaticamente tipada — "se compilou, essa classe de erro não existe" — desaparece exatamente na função que devia ser mais genérica e reutilizável.

**2. Custo de runtime da type assertion.** Cada `a.(int)` ou `case int:` dentro de um type switch exige que o runtime **consulte o tipo dinâmico** guardado dentro do valor de interface e compare com o tipo esperado. Não é grátis — é trabalho que `MaxInt` simplesmente não faz, porque já sabe o tipo em tempo de compilação.

**3. Boxing.** Um valor de interface em Go não é só o dado puro — é um par (ponteiro para os dados, informação de tipo). Quando um `int` (que cabe numa word de máquina, sem indireção nenhuma) é atribuído a uma variável `interface{}`, o runtime frequentemente precisa **alocar esse `int` no heap** para guardar um ponteiro estável dentro do par de interface — é o que a comunidade chama de *boxing*. Isso significa pressão adicional sobre o garbage collector em código que, com tipos concretos, nunca alocaria nada.

> [!warning] `interface{}` genérico não é "generics de graça" — é um trade-off, não um substituto
> É tentador ler `func Max(a, b interface{}) interface{}` como "generics manuais". Não são a mesma coisa: generics de verdade preservam a checagem de tipo em compilação e não pagam boxing nem type assertion em runtime — o compilador gera (ou especializa) código para o tipo concreto usado em cada chamada. `interface{}` empurra tudo isso para runtime. A diferença entre as duas abordagens é exatamente o que motivou a adição de generics à linguagem.

## Por que a comunidade resistiu — e por que cedeu

Go foi lançada em 2009 **sem** generics, por decisão deliberada, não por falta de tempo. Os criadores da linguagem — Rob Pike, Robert Griesemer, Ken Thompson — já tinham visto o que templates fizeram com a legibilidade e os tempos de compilação de C++, e o que generics trouxeram de complexidade adicional para Java (erasure, wildcards, `? extends T`). A aposta inicial de Go era que **simplicidade** — poucas features, ortogonais, fáceis de aprender inteiras — valia mais que expressividade genérica.

Por quase uma década, a resposta oficial a "quando teremos generics?" foi alguma versão de "estamos pesquisando, mas não encontramos um design que valha a complexidade que adiciona". Múltiplas propostas foram publicadas e descartadas — incluindo tentativas baseadas em `contracts` (uma sintaxe alternativa a *constraints*, testada e depois abandonada em favor do design final). O próprio [design draft de generics](https://go.dev/blog/generics-proposal), publicado pela equipe Go, é explícito sobre o histórico de tentativas rejeitadas.

O que mudou não foi a filosofia — foi o peso acumulado do problema real. Bibliotecas de containers (filas, pilhas, árvores, sets), funções utilitárias sobre slices e maps, e código de infraestrutura interno do próprio ecossistema Go estavam repetindo o dilema `MaxInt`/`MaxFloat64` ou `interface{}` em milhares de lugares. A dor de duplicar código, ou de pagar o custo de runtime e a perda de segurança de tipo do `interface{}`, cresceu mais rápido que o medo de repetir os erros de C++ e Java.

O Go 1.18, lançado em março de 2022, chegou com um design que tenta explicitamente evitar as duas armadilhas conhecidas: sem *type erasure* como Java (o compilador sabe os tipos concretos em cada instanciação), e sem a explosão de complexidade sintática de C++ (sem especialização de template arbitrária, sem SFINAE). O trade-off consciente foi aceitar uma feature **mais restrita** — generics que resolvem o problema de `Max`/containers sem abrir a porta para metaprogramação elaborada.

> [!info] Generics — Go 1.18, março de 2022
> Foi a mudança mais significativa na sintaxe da linguagem desde o lançamento em 2009. Antes dela, a resposta canônica da FAQ oficial para "Go vai ter generics?" era um "talvez, ainda pesquisando" que durou treze anos.

## Vindo de outras linguagens

| Linguagem | Como resolvia isso antes de ter generics (ou resolve, se nunca teve) |
|---|---|
| Java | Sempre teve generics desde o 1.5 (2004) — mas com *type erasure*: `List<String>` vira `List` em bytecode, sem reificação real |
| Python | Duck typing: `max(a, b)` funciona para qualquer tipo com `__gt__`, sem checagem estática — o oposto do dilema Go, porque nunca houve tipagem estática obrigando a escolher |
| TypeScript | Generics desde o início do projeto, inspirados em C#/Java, com inferência de tipo mais flexível que a de Go |
| C | Sem generics — resolve com macros de pré-processador (`#define MAX(a,b) ((a) > (b) ? (a) : (b))`) ou com `void*` cru, versão ainda mais perigosa do `interface{}` do Go, sem checagem de tipo nenhuma |

O caso de Go antes do 1.18 fica mais perto do C do que se costuma admitir: `interface{}` é um `void*` com um pouco mais de disciplina (guarda a informação de tipo, permite type assertion segura em vez de reinterpretação crua de bytes), mas o espírito — "abra mão de tipo estático para ganhar reuso" — é o mesmo.

## Como explicar em inglês

> Before Go 1.18 (released March 2022), writing a function that worked across multiple types meant choosing between two unattractive options: duplicating the function once per type (`MaxInt`, `MaxFloat64`, and so on — correct and fast, but a maintenance burden that multiplied with every generic data structure you wrote), or accepting `interface{}` and recovering the concrete type at runtime via type assertion — which traded away compile-time type safety, paid a runtime cost for the type switch itself, and often triggered heap allocation ("boxing") for values that would otherwise live entirely on the stack. Go's designers resisted adding generics for over a decade, wary of the complexity templates brought to C++ and the type-erasure trade-offs of Java generics. What eventually tipped the balance was the accumulated real-world cost of duplication and `interface{}` workarounds across the ecosystem — not a change in philosophy about simplicity.

| Termo PT | Termo EN |
|---|---|
| genéricos | generics |
| duplicação de código | code duplication |
| asserção de tipo | type assertion |
| troca de tipo (switch) | type switch |
| boxing | boxing |
| apagamento de tipo | type erasure |
| tipo dinâmico | dynamic type |
| parâmetro de tipo | type parameter |
| restrição | constraint |

## O que vem a seguir

A dor está mapeada: duplicação de um lado, `interface{}` com type assertion do outro. A [[02 - Type parameters — a sintaxe|próxima nota]] mostra a saída que o Go 1.18 trouxe — **type parameters**, a sintaxe `func Max[T ...](a, b T) T` que permite escrever a função uma única vez, com verificação de tipo preservada em tempo de compilação e sem o custo de runtime do `interface{}`.

## Veja também

- [[02 - Type parameters — a sintaxe|02 — Type parameters — a sintaxe]] — próxima nota do galho, a solução para o problema descrito aqui
- [[03 - Constraints|03 — Constraints]] — como restringir quais tipos um type parameter aceita
- [[03-Dominios/Tecnologia/Go/index|Trilha Go]]

## Fontes

- The Go Authors. *Type Parameters Proposal*. go.dev. https://go.dev/blog/generics-proposal (acessado em 2026-07-18)
- The Go Authors. *An Introduction To Generics*. go.dev. https://go.dev/blog/intro-generics (acessado em 2026-07-18)
- The Go Authors. *The Go Programming Language Specification — Type parameter declarations*. go.dev. https://go.dev/ref/spec#Type_parameter_declarations (acessado em 2026-07-18)
- The Go Authors. *Go 1.18 Release Notes*. go.dev. https://go.dev/doc/go1.18 (acessado em 2026-07-18)
- The Go Authors. *A Tour of Go — Generics*. go.dev. https://go.dev/tour/generics/1 (acessado em 2026-07-18)
