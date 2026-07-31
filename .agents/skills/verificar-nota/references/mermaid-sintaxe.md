# Sintaxe Mermaid — erros que quebram o render

Referência de apoio ao item **S1** da `/verificar-nota`.

Um diagrama com erro de sintaxe não degrada: ele **não renderiza**. No Obsidian aparece a caixa
vermelha de erro; no Quartz, o bloco vira código cru.

> [!important] Prefira o validador ao olho
> Rode `scripts/validar-mermaid.mjs` — ele executa o parser do Mermaid de verdade e é a única
> checagem confiável. Use as regras abaixo para *consertar* o que ele acusar, não para auditar
> à mão.
>
> ```bash
> node .agents/skills/verificar-nota/scripts/validar-mermaid.mjs <arquivo-ou-pasta>
> ```
>
> Primeira execução: `cd .agents/skills/verificar-nota/scripts && npm install`

Todas as regras foram verificadas contra **Mermaid 11.16** e derivadas dos 92 blocos que estavam
de fato quebrados neste vault (de 3.949 auditados em 2026-07-27).

---

## Regra de ouro

**Na dúvida, envolva o rótulo em aspas duplas e dê um ID ao nó.** `A["texto (qualquer coisa)"]`
resolve a maioria dos casos: parênteses, colchetes, `<>`, `@`, `#`.

As exceções — onde aspas *não* salvam — estão marcadas abaixo.

---

## R1 — `;` em `sequenceDiagram` (causa nº 1)

`;` é separador de statement. Vale para mensagens, `Note` e alias de `participant`.

```
❌ A->>B: BEGIN; INSERT pedido; COMMIT
❌ Note over A: processa sozinho; saldo 100 -> 50
❌ participant Loop as for i := 0; i < len(s)

✅ A->>B: BEGIN, INSERT pedido, COMMIT
✅ Note over A: processa sozinho — saldo 100 -> 50
```

**Corolário:** entidades HTML terminam em `;`, então **toda entidade HTML quebra um
sequenceDiagram**. Use o caractere Unicode direto.

```
❌ A->>B: X mudou &rarr; ABORT        ✅ A->>B: X mudou → ABORT
❌ Note over A,B: TCP &mdash; TLS     ✅ Note over A,B: TCP — TLS
```

Setas literais (`->`, `-->`) e parênteses **funcionam** em mensagens — não precisa evitá-los.

## R2 — Palavras reservadas como ID de nó

Silencioso e traiçoeiro: o parser acusa uma linha *distante* da culpada.

| Diagrama | ID proibido | Porque |
|---|---|---|
| `sequenceDiagram` | `Loop` | colide com a construção `loop … end` |
| `sequenceDiagram` | `Alt`, `Opt`, `Par`, `Rect`, `Critical`, `Break`, `End` | idem |
| `flowchart` / `graph` | `graph` | colide com a declaração do diagrama |

O rótulo visível não muda se você renomear o ID e mantiver o alias:

```
❌ participant Loop as Event Loop
✅ participant EvLoop as Event Loop
```

## R3 — Parênteses em rótulo de flowchart sem aspas

```
❌ A[epoll — O(1) por evento]           ✅ A["epoll — O(1) por evento"]
❌ Step -->|coro.send(None)| Coro       ✅ Step -->|"coro.send(None)"| Coro
```

Acentos funcionam em rótulos (`A["Configuração"]`). Em **IDs**, use só ASCII sem espaço nem acento.

## R4 — Aspas dentro de rótulo

`\"` **não** é escape válido. Use aspas simples por dentro das duplas.

```
❌ B["addr = \"\", timeout = 0"]        ✅ B["addr = '', timeout = 0"]
❌ P["\"GET /users/{id}\""]             ✅ P["'GET /users/{id}'"]
❌ L1['"10"'] --> L2['"100"']           ✅ L1["10"] --> L2["100"]
```

Aspas simples **não** delimitam rótulo em Mermaid — só as duplas.

## R5 — Backticks (markdown string)

Backtick abre modo markdown-string, frágil com `${}`, `<>` e `()`. Backtick duplo quebra sempre.

```
❌ TL["`` `${Method} ${Path}` ``\n(template literal)"]
✅ TL["'${Method} ${Path}'\n(template literal)"]
```

## R6 — `style` / `classDef` fora de flowchart

`sequenceDiagram`, `mindmap` e `quadrantChart` **não suportam** `style`. A linha não colore nada e
ainda derruba o diagrama inteiro. Remova-a — não há equivalente nesses tipos.

## R7 — `mindmap`: folha com caracteres especiais precisa de ID

Aqui aspas sozinhas **não** bastam — é preciso `id["texto"]`.

```
❌ :has() parent selector        ❌ ":has() parent selector"
✅ n1[":has() parent selector"]
```

Preserve `root((Texto))` como está — trocar a forma da raiz descaracteriza o mapa.

## R8 — `quadrantChart`: sem `(` e sem `:`

Aspas **não** salvam; reescreva o texto.

```
❌ quadrant-1 Ideal (raro)              ✅ quadrant-1 Ideal — raro
❌ title Ablation: believability        ✅ title Ablation — believability
```

## R9 — `stateDiagram`: hífen em ID de estado

```
❌ running --> shutting-down: terminate
✅ running --> shutting_down: terminate
```

Cuidado ao corrigir em massa: `stateDiagram-v2` na primeira linha **deve** manter o hífen.

## R10 — `subgraph` com vírgula no nome

Espaço no nome é permitido; **vírgula e hífen** não.

```
❌ subgraph Incremental - um major por vez, testado
✅ subgraph inc["Incremental — um major por vez, testado"]
```

## R11 — Rótulo de seta vazio e setas malformadas

```
❌ ES2017 -->|""| ES2020        ✅ ES2017 --> ES2020
❌ USE2 -- sim → EMIT2[...]     ✅ USE2 -- sim --> EMIT2[...]
❌ Env -.->|"texto"--> Mount    ✅ Env -.->|"texto"| Mount
```

Atenção: `→` (Unicode) não é seta de Mermaid — só enfeite dentro de rótulo.

## R12 — Tipos de diagrama inexistentes

`bar` não existe. Para gráfico de barras use `xychart-beta`:

```
xychart-beta
    title "Ablation — believability relativa"
    x-axis ["Completa", "Sem reflection", "Sem planning"]
    y-axis "Believability" 0 --> 100
    bar [100, 62, 71]
```

## R13 — `classDiagram`: `:` dentro do label da relação

```
❌ Pagavel <|.. Boleto : "implements (Java: nominal)"
✅ Pagavel <|.. Boleto : "implements (Java — nominal)"
```

---

## Regras obsoletas — não aplique

Testadas e **aprovadas** no parser 11.16. Se algum guia recomendar isso, ignore:

| Suposta regra | Realidade em Mermaid 11.x |
|---|---|
| `A[1. Percepção]` quebra ("Unsupported markdown: list") | Parseia normalmente |
| `subgraph Kafka Broker` (espaço sem aspas) quebra | Parseia normalmente (só vírgula/hífen quebram) |
| `Z[end]` minúsculo quebra | Parseia normalmente |
| `\n` no rótulo quebra; só `<br/>` serve | **Ambos funcionam** — o vault usa `\n` em milhares de nós |
| `<` e `>` no rótulo quebram | Funcionam, com ou sem aspas |
| `style A fill:#fff,color:#000` (vírgula) quebra | Funciona (em flowchart — ver R6) |
| Parênteses em mensagem de sequenceDiagram quebram | Funcionam |

---

## Procedência

Este documento **não** reproduz as regras de
[axton-obsidian-visual-skills](https://github.com/axtonliu/axton-obsidian-visual-skills): das três
que ele propõe, duas foram reprovadas no parser 11.16 (viraram linhas da tabela de obsoletas) e a
terceira prescrevia trocar parênteses por delimitadores CJK (`「」`), inadequado em PT-BR.

R1–R13 foram derivadas empiricamente: rodando o parser sobre os 3.949 blocos Mermaid do vault,
isolando cada uma das 92 falhas por bisecção de prefixo e confirmando cada causa em teste
controlado.
