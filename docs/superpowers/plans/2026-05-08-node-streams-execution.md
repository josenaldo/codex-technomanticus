---
title: "Plano — Execução da Sub-trilha Streams (Galho 3)"
date: 2026-05-08
status: ready
type: plan
publish: false
---

# Sub-trilha Streams — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produzir 12 notas atômicas + 1 MOC em `03-Dominios/Node/Streams/`, em PT-BR, todas `publish: true`, cobrindo do mental model dos 4 tipos ao tuning de performance, passando por backpressure, pipeline, async iteration, Web Streams interop e padrões práticos — para um dev senior em prep para entrevista internacional. Ao final, podar 4 seções do tronco `JavaScript/Backend/Node.js.md` e atualizar o MOC central de `03-Dominios/Node/index.md`.

**Architecture:** Sub-trilha sequencial em 5 blocos (Mental model → Tipos aprofundados → Backpressure e pipeline → Streams modernos → Padrões e fechamento) + 1 MOC com 5 rotas alternativas. Pressupõe galho 1 (Runtime e Event Loop) como pré-requisito, com referências cruzadas pro galho 2 (Paralelismo) onde workers + streams se cruzam. Cada nota é atômica, segue estrutura híbrida (TL;DR + corpo técnico), com code samples em JS ou TS (Node 22 LTS / 24, `stream/promises` mainstream, Web Streams interop estável), e seção "Em entrevista" para preparação internacional.

**Tech Stack:** Markdown + Obsidian Flavored Markdown (wikilinks, callouts, dataview), Quartz para publicação no site público (josenaldo.github.io). Sem código a executar como sistema — code samples didáticos validáveis via `node script.js` ou `node --experimental-strip-types script.ts` quando útil. Bibliografia âncora: Node docs (`stream`, `webstreams`), WHATWG Streams Standard, MDN Streams API, talks de Matteo Collina.

---

## ⚠️ Restrição absoluta — fabricação

A memória [Nunca inventar dados sobre o usuário](/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/feedback_no_fabrication.md) é regra inegociável. **Nenhuma nota pode atribuir ao autor experiências profissionais, projetos, clientes, métricas ou casos não-vividos.**

A seção "Na prática" de cada nota usa:

- "Padrão observado em libs do ecossistema (pino, busboy, csv-parser)"
- "Caso típico em pipelines de processamento de arquivos"
- "Armadilha comum reportada na comunidade"
- Citações com fonte verificável (docs oficiais, talks identificadas, repos públicos)
- Hipotéticos explícitos ("Imagine um endpoint que recebe upload de CSV...")

Quando faltar contexto factual, **PERGUNTAR antes de escrever** — nunca preencher com plausibilidade.

---

## File Structure

13 arquivos novos em `03-Dominios/Node/Streams/`:

```
03-Dominios/Node/Streams/
├── Streams.md                                                    # MOC (Task 1)
├── 01 - Por que streams.md                                       # Task 2
├── 02 - Os 4 tipos - Readable, Writable, Duplex, Transform.md    # Task 3
├── 03 - Readable streams.md                                      # Task 4
├── 04 - Writable streams.md                                      # Task 5
├── 05 - Duplex e Transform.md                                    # Task 6
├── 06 - Backpressure.md                                          # Task 7
├── 07 - pipeline vs pipe - error handling.md                     # Task 8
├── 08 - Async iteration de streams.md                            # Task 9
├── 09 - Web Streams - interop com padrão universal.md            # Task 10
├── 10 - Padrões práticos.md                                      # Task 11
├── 11 - Performance e tuning.md                                  # Task 12
└── 12 - Armadilhas, regras práticas, cheatsheet.md               # Task 13
```

**Final integration (Task 14, 15, 16):**
- Pass final no MOC inserindo todos os wikilinks + dataview
- Poda do tronco `03-Dominios/JavaScript/Backend/Node.js.md` (4 seções)
- Atualização do MOC central `03-Dominios/Node/index.md` + verificação de build do Quartz

---

## Template padrão (definido uma vez, aplicado a todas as 12 notas)

```markdown
---
title: "<título sem prefixo numérico>"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - <tag específica: readable, writable, transform, backpressure, pipeline, web-streams, etc>
aliases:
  - <opcional: alternativas naturais de busca>
---

# <Título>

> [!abstract] TL;DR
> <2-4 linhas em PT-BR direto. Define o conceito-chave + a regra prática + por que importa.>

## O que é

<1-3 parágrafos definindo o conceito da nota. Pressupõe leitura de [[Runtime e Event Loop]] (galho 1).>

## Por que importa

<O problema que isso resolve no dia a dia.>

## Como funciona

<Aprofundamento técnico com code samples em JS ou TS. Mostrar o pattern, depois variações. Edge cases.>

## Na prática

<Exemplo realista. Sem fabricar experiência do autor — usar "padrão observado em X", "lib Y faz isso", hipotéticos explícitos.>

## Armadilhas

<Gotchas específicos. Mínimo 2 itens.>

## Em entrevista

<Frase pronta em inglês. Vocabulário-chave (PT → EN). Pergunta típica + resposta defensiva.>

## Veja também

- [[Outra nota da trilha]]
- [[Runtime e Event Loop]] — galho 1 (pré-requisito)
- [[Node.js]] — tronco
```

### Variações permitidas

- **Nota 10 (Padrões práticos):** estrutura tópica — cada padrão (line parser, CSV → JSONL, multipart, fetch streaming, tee) em sua sub-seção compacta de 30-50 linhas.
- **Nota 12 (Armadilhas, cheatsheet):** estrutura tópica — lista de armadilhas + tabelas + decision tree compactada.
- **MOC (`Streams.md`):** estrutura própria — abertura + Comece por aqui + 5 rotas alternativas + dataview. `type: moc`.

### Critérios de qualidade (rubrica aplicada por nota)

- [ ] TL;DR em callout `[!abstract]`, 2-4 linhas, compreensível em <30s
- [ ] 2+ wikilinks pra outras notas do galho + 1+ wikilink pra `[[Node.js]]` (tronco) ou galho anterior
- [ ] 3+ code samples em JS ou TS (notas conceituais 01, 02 podem ter menos)
- [ ] Seção "Em entrevista" com pelo menos 1 frase pronta em inglês + vocabulário-chave (mínimo 4 termos PT→EN)
- [ ] Seção "Armadilhas" com pelo menos 2 armadilhas concretas
- [ ] Frontmatter completo (`publish: true`, `status: seedling`, tags `[node, streams, <específica>]`)
- [ ] Versões assumidas declaradas se relevante (Node 22 LTS / 24)
- [ ] PT-BR natural; termos técnicos em inglês mantidos (stream, backpressure, pipeline, transform, etc.)
- [ ] **Zero atribuição de experiência pessoal ao autor** (regra absoluta)
- [ ] Nenhuma alegação técnica não-trivial sem fonte ou code sample que comprove

---

## Bibliografia centralizada

### Referências canônicas

- **Node.js docs — Stream:** `https://nodejs.org/api/stream.html`
- **Node.js docs — Web Streams API:** `https://nodejs.org/api/webstreams.html`
- **WHATWG Streams Standard:** `https://streams.spec.whatwg.org/`
- **MDN — Streams API:** `https://developer.mozilla.org/en-US/docs/Web/API/Streams_API`
- **Node.js docs — `pipeline`:** `https://nodejs.org/api/stream.html#streampipelinesource-transforms-destination-callback`
- **Node.js docs — `stream/promises`:** `https://nodejs.org/api/stream.html#streampromisespipeline-source-transforms-destination-options`

### Referências de produção

- **pino:** `https://github.com/pinojs/pino` — stream-based logging
- **busboy:** `https://github.com/mscdex/busboy` — multipart parser
- **csv-parser:** `https://github.com/mafintosh/csv-parser` — CSV parser

### Notas no vault

- `03-Dominios/JavaScript/Backend/Node.js.md` — tronco (4 seções a podar)
- `03-Dominios/Node/index.md` — MOC central
- `03-Dominios/Node/Runtime e Event Loop/` — galho 1 (em particular notas 04 fases do event loop, 10 bloqueio)
- `03-Dominios/Node/Paralelismo/` — galho 2 (workers + streams cruzam em postMessage + transferList)

### A buscar conforme necessidade

- Discussões 2026 sobre Web Streams como default em apps portáveis
- Posts sobre performance de streams em casos reais
- Talks recentes de Matteo Collina

---

## Task 0: Pré-flight

**Files:**
- Create: `03-Dominios/Node/Streams/` (diretório)

- [ ] **Step 1: Criar o diretório**

```bash
mkdir -p "03-Dominios/Node/Streams"
ls -la "03-Dominios/Node/Streams"
```

Esperado: diretório vazio.

- [ ] **Step 2: Confirmar memórias críticas**

```bash
cat /home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/MEMORY.md | grep -iE "fabrica|invent|tronco|galho"
```

Esperado: linhas referenciando `feedback_no_fabrication.md` e `project_tronco_galhos_pattern.md`. Se faltar `no_fabrication`, BLOCKED. Se faltar `tronco_galhos`, registrar e prosseguir.

- [ ] **Step 3: Sanity check do tronco — 4 seções a podar**

```bash
grep -nE "^### Streams|^### Backpressure|^### Web Streams|^### Stream patterns" "03-Dominios/JavaScript/Backend/Node.js.md"
```

Esperado: 4 matches. Anotar números de linha de cada uma:
- `### Streams — deep dive`
- `### Backpressure`
- `### Web Streams vs Node streams`
- `### Stream patterns`

Se algum nome divergir do esperado, anotar exatamente como aparece.

- [ ] **Step 4: Confirmar wikilinks dos galhos anteriores resolvem**

```bash
ls "03-Dominios/Node/Runtime e Event Loop/" | wc -l   # esperado 13
ls "03-Dominios/Node/Paralelismo/" | wc -l            # esperado 13
ls "03-Dominios/Node/index.md"                        # esperado existir
ls "03-Dominios/JavaScript/Backend/Node.js.md"        # esperado existir
```

Notas referenciadas com mais frequência no galho 3:
- `[[Runtime e Event Loop]]` (MOC galho 1)
- `[[10 - Bloqueio do event loop - sintomas e causas]]` (galho 1)
- `[[Paralelismo]]` (MOC galho 2)
- `[[04 - Comunicação entre workers - postMessage e MessageChannel]]` (galho 2)
- `[[Node.js]]` (tronco)

Confirmar que existem.

- [ ] **Step 5: Sanity check das fontes-âncora**

WebFetch em paralelo:

```
https://nodejs.org/api/stream.html
https://nodejs.org/api/webstreams.html
https://streams.spec.whatwg.org/
https://github.com/pinojs/pino
```

Confirmar acesso. Se alguma falhar, registrar e usar fontes alternativas.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat(node-streams): create directory for Streams sub-trail"
```

(Sem `Co-Authored-By` — regra do usuário.)

---

## Task 1: MOC esqueleto

**Files:**
- Create: `03-Dominios/Node/Streams/Streams.md`

- [ ] **Step 1: Criar MOC**

Criar `03-Dominios/Node/Streams/Streams.md` com este conteúdo (substituir `\`\`\`` por triple backticks reais — escapes apenas neste plano):

```markdown
---
title: "Streams"
created: 2026-05-08
updated: 2026-05-08
type: moc
status: seedling
publish: true
tags:
  - node
  - streams
  - moc
aliases:
  - Node Streams
  - Galho 3 - Streams
---

# Streams

> [!abstract] TL;DR
> Galho 3 da trilha Node Senior. Cobre a abstração fundamental do Node para processar dados sem carregar tudo em memória: 4 tipos (Readable, Writable, Duplex, Transform), backpressure, pipeline vs pipe, async iteration moderna, Web Streams interop, padrões práticos (line parser, CSV → JSONL, fetch streaming) e tuning de performance. Pré-requisito: galho 1 (Runtime e Event Loop).

## Sobre este galho

(introdução curta — preencher na Task 14)

## Comece por aqui — trilha completa (12 notas)

### Bloco A — Mental model

1. [[01 - Por que streams]]
2. [[02 - Os 4 tipos - Readable, Writable, Duplex, Transform]]

### Bloco B — Tipos aprofundados

3. [[03 - Readable streams]]
4. [[04 - Writable streams]]
5. [[05 - Duplex e Transform]]

### Bloco C — Backpressure e pipeline

6. [[06 - Backpressure]]
7. [[07 - pipeline vs pipe - error handling]]

### Bloco D — Streams modernos

8. [[08 - Async iteration de streams]]
9. [[09 - Web Streams - interop com padrão universal]]

### Bloco E — Padrões e fechamento

10. [[10 - Padrões práticos]]
11. [[11 - Performance e tuning]]
12. [[12 - Armadilhas, regras práticas, cheatsheet]]

## Rotas alternativas

### Rota entrevista internacional

01 → 02 → 03 → 04 → 06 → 07 → 09. Foco em "explicar streams pra entrevistador".

### Rota produção

01 → 06 → 07 → 10 → 11 → 12. Foco em "escrever streams sem bugs em prod".

### Rota async-first (2026 stack)

02 → 08 → 09 → 10. Streams modernos com async iter + Web Streams.

### Rota implementing custom streams

03 → 04 → 05 → 06 → 11. Pra quem vai escrever Transform/Duplex próprio.

## Todas as notas

\`\`\`dataview
TABLE status, updated
FROM "03-Dominios/Node/Streams"
WHERE type = "concept"
SORT file.name ASC
\`\`\`

## Veja também

- [[03-Dominios/Node/index|Node.js (MOC central)]]
- [[Node.js]] — tronco (deep dive panorâmico)
- [[Runtime e Event Loop]] — galho 1 (pré-requisito)
- [[Paralelismo]] — galho 2 (referência cruzada onde workers + streams)
```

- [ ] **Step 2: Verificar**

- `type: moc` presente
- `publish: true` presente
- 12 notas em 5 blocos (A, B, C, D, E)
- 4 rotas alternativas (entrevista, produção, async-first, custom streams) + "Comece por aqui" implícito como completa
- Dataview path: `"03-Dominios/Node/Streams"`
- Wikilinks pro MOC central, tronco, galho 1, galho 2

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Node/Streams/Streams.md"
git commit -m "feat(node-streams): add MOC skeleton for Streams branch"
```

---

## Task 2: Nota 01 — Por que streams

**Files:**
- Create: `03-Dominios/Node/Streams/01 - Por que streams.md`

**Conteúdo-chave do spec (Bloco A):**

> Quando usar streams: arquivos/payloads grandes (>100MB), throughput sustentado, processamento em chunks, backpressure-aware. Alternativas: buffer everything (memória explode); paginação (latência alta). Trade-offs: complexidade, debugging mais difícil, error handling não-trivial.

- [ ] **Step 1: Síntese (sem WebFetch necessária)**

Esta é a nota de framing. Reler galho 1 nota 10 (Bloqueio do event loop) e nota 04 do galho 2 (postMessage + transferList) para wikilinks corretos e vocabulário coeso.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Por que streams"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - mental-model
aliases:
  - Quando usar streams
  - Streams motivação
---
```

- [ ] **Step 3: Escrever a nota completa (250-400 linhas, em PT-BR)**

- **TL;DR** (callout `[!abstract]`): Streams são a abstração do Node para processar dados em chunks sem carregar tudo em memória. Use quando o payload é grande (>100MB), o throughput é sustentado, ou backpressure precisa ser respeitado. Alternativas mais simples (buffer everything, paginação) ganham em casos pequenos; streams ganham em casos grandes ou de longa duração.
- **## O que é:** definição prática. Stream = sequência de chunks que pode ser produzida ou consumida sem materializar tudo de uma vez. Os 4 tipos disponíveis em Node (preview da nota 02). Diferença com array completo (memória vs throughput).
- **## Por que importa:** o problema concreto. Endpoint que recebe upload de 5GB → buffer everything = OOM. Pipeline de processamento de CSV → carregar tudo = latência absurda. Streaming de fetch (LLM responses, SSE) → buffer everything quebra a UX.
- **## Como funciona:** comparação **buffer vs stream** com code samples:
  - Buffer everything: `const data = await fs.readFile('big.csv'); processCSV(data);` — memória O(N)
  - Stream: `await pipeline(createReadStream('big.csv'), parser, writer);` — memória O(chunkSize)
- Code sample mostrando memory growth quando buffer everything é usado em loop. Diagrama mental: produtor → buffer interno → consumidor.
- **## Na prática:** quando NÃO usar streams (e usar alternativa):
  - Payload pequeno (<10MB) — overhead de stream > benefício
  - Lógica que precisa ver todo o dataset de uma vez (sort global, dedup global) — buffer
  - Quando latência ponta-a-ponta importa mais que throughput — buffer + paginação
  - Quando você só vai compor 1 transformação simples — buffer + array methods
- **## Armadilhas (3+):**
  1. Usar stream em payload pequeno — overhead inútil
  2. Confundir "streaming" no protocolo HTTP com "Node Streams" — relacionados mas não iguais
  3. Achar que stream resolve memória mas ignorar backpressure — memória cresce no buffer interno
- **## Em entrevista:**
  - Frase pronta: "Node Streams are the canonical way to process data in chunks without loading everything into memory. The motivation is concrete: large file processing, sustained throughput on a server, and respecting backpressure between fast producers and slow consumers. They're not always the right answer — for small payloads, the overhead exceeds the benefit, and for operations that need a global view of the data, you need the full buffer anyway. The signal that you should reach for streams is when memory or latency under load is the bottleneck."
  - Vocabulário (5+): chunk (chunk), throughput (throughput), backpressure (backpressure), produtor/consumidor (producer/consumer), latência (latency).
- **## Veja também:**
  - `[[02 - Os 4 tipos - Readable, Writable, Duplex, Transform]]`
  - `[[06 - Backpressure]]`
  - `[[07 - pipeline vs pipe - error handling]]`
  - `[[Runtime e Event Loop]]` (galho 1)
  - `[[10 - Bloqueio do event loop - sintomas e causas]]` (galho 1)
  - `[[Paralelismo]]` (galho 2)
  - `[[Node.js]]` (tronco)

- [ ] **Step 4: Verificar rubrica** (standard)

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Streams/01 - Por que streams.md"
git commit -m "feat(node-streams): add note 01 — Por que streams"
```

---

## Task 3: Nota 02 — Os 4 tipos

**Files:**
- Create: `03-Dominios/Node/Streams/02 - Os 4 tipos - Readable, Writable, Duplex, Transform.md`

### Step 1: Pesquisa-âncora

```
WebFetch: https://nodejs.org/api/stream.html
```

### Step 2: Frontmatter

```yaml
---
title: "Os 4 tipos: Readable, Writable, Duplex, Transform"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - mental-model
  - readable
  - writable
  - duplex
  - transform
aliases:
  - 4 tipos de stream
  - Visão geral streams
---
```

### Step 3: Escrever (300-450 linhas, PT-BR)

- **TL;DR:** Node tem 4 tipos de stream: Readable (fonte: `fs.createReadStream`, HTTP response, `process.stdin`), Writable (destino: `fs.createWriteStream`, HTTP request, `process.stdout`), Duplex (read e write **independentes**: TCP socket), Transform (Duplex onde write→leitura é a transformação: zlib, crypto, parsers).
- **## O que é:** cada tipo definido em 1-2 frases + interface básica + exemplos canônicos.
- **## Por que importa:** confundir Duplex com Transform leva a implementações erradas. Confundir Readable com iterable mata performance.
- **## Como funciona:** **tabela canônica** (estrela da nota):

  | Tipo | Interface | Direção | Exemplos canônicos |
  |---|---|---|---|
  | Readable | `.read()`, evento `'data'`, `for await of` | source → consumer | `fs.createReadStream`, `process.stdin`, `http.IncomingMessage` (response no client, request no server), `Readable.from(iterable)` |
  | Writable | `.write()`, `.end()`, evento `'drain'` | producer → sink | `fs.createWriteStream`, `process.stdout`, `http.OutgoingMessage` (request no client, response no server) |
  | Duplex | Readable + Writable independentes | dois canais | `net.Socket`, `tls.TLSSocket` |
  | Transform | Duplex onde input→output é transformação | source → transform → consumer | `zlib.createGzip()`, `crypto.createCipheriv()`, parsers customizados |

- Code sample mínimo de cada (5-10 linhas).
- **## Na prática:** decidir qual tipo usar:
  - Vou ler de algo (file, network, stdin) → Readable
  - Vou escrever pra algo (file, network, stdout) → Writable
  - Comunicação bidirecional independente (TCP) → Duplex
  - Transformar bytes/objetos no meio de pipeline → Transform
- **## Armadilhas (3+):**
  1. Confundir Duplex com Transform — Duplex tem dois canais separados; Transform conecta entrada→saída
  2. Achar que `Readable.from(array)` é stream "real" — é, mas overhead pode não compensar pra arrays pequenos
  3. Tentar usar Transform pra coisa que precisa estado global (ex: sort) — Transform processa chunk a chunk
- **## Em entrevista:**
  - Frase pronta: "Node has four stream types. Readable is a source — `fs.createReadStream`, HTTP responses, `process.stdin`. Writable is a sink — `fs.createWriteStream`, HTTP requests, `process.stdout`. Duplex is read and write **independently** — the canonical example is a TCP socket: you read from the peer, write to the peer, two separate logical channels. Transform is a Duplex where what you write feeds the read side after a transformation — zlib, crypto, parsers."
  - Vocabulário (6+): fonte (source), sumidouro (sink), canal (channel), transformador (transform), bidirecional (bidirectional), stream pipeline.
- **## Veja também:**
  - `[[01 - Por que streams]]`
  - `[[03 - Readable streams]]`
  - `[[04 - Writable streams]]`
  - `[[05 - Duplex e Transform]]`
  - `[[Node.js]]` (tronco)

### Step 4: Rubric (standard)

### Step 5: Commit

```bash
git add "03-Dominios/Node/Streams/02 - Os 4 tipos - Readable, Writable, Duplex, Transform.md"
git commit -m "feat(node-streams): add note 02 — Os 4 tipos"
```

---

## Task 4: Nota 03 — Readable streams

**Files:**
- Create: `03-Dominios/Node/Streams/03 - Readable streams.md`

### Step 1: Pesquisa-âncora

```
WebFetch: https://nodejs.org/api/stream.html#readable-streams
```

### Step 2: Frontmatter

```yaml
---
title: "Readable streams"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - readable
aliases:
  - Readable
  - Modo flowing
  - Modo paused
---
```

### Step 3: Escrever (350-500 linhas, PT-BR)

- **TL;DR:** Readable tem 2 modos: flowing (`'data'` listener; chunks empurrados) e paused (`.read()` puxa; default em Node moderno). Eventos: `data`, `end`, `error`, `close`, `readable`. Implementação custom: subclass `Readable` + `_read(size)` + `push(chunk)` / `push(null)` (sinal de end). `Readable.from(iterable)` é o atalho moderno.
- **## O que é:** API de Readable detalhada.
- **## Por que importa:** modo errado = bugs sutis (perder eventos, vazar memória, não respeitar backpressure).
- **## Como funciona:**
  1. **Flowing mode** — adicionar listener de `'data'` automaticamente coloca em flowing:
     ```javascript
     readable.on('data', (chunk) => process(chunk));
     readable.on('end', () => done());
     ```
  2. **Paused mode** — chamar `.read()` puxa próximo chunk (ou null se nada ainda):
     ```javascript
     readable.on('readable', () => {
       let chunk;
       while ((chunk = readable.read()) !== null) {
         process(chunk);
       }
     });
     ```
  3. **Implementação custom:**
     ```javascript
     import { Readable } from 'node:stream';
     class CounterReadable extends Readable {
       constructor(max) { super(); this.i = 0; this.max = max; }
       _read() {
         if (this.i >= this.max) this.push(null);
         else this.push(`${this.i++}\n`);
       }
     }
     ```
  4. **`Readable.from(iterable)`** — atalho moderno:
     ```javascript
     const r = Readable.from(['line1\n', 'line2\n']);
     // ou async generator
     async function* gen() { for (const x of items) yield process(x); }
     const r = Readable.from(gen());
     ```
  5. **Object mode:**
     ```javascript
     class JsonReadable extends Readable {
       constructor(items) { super({ objectMode: true }); this.items = items; this.i = 0; }
       _read() {
         if (this.i >= this.items.length) this.push(null);
         else this.push(this.items[this.i++]);
       }
     }
     ```
- **## Na prática:** padrão observado:
  - `Readable.from(iterable)` é o default para criar Readable em código moderno
  - Subclass + `_read` é raramente necessário (libs maduras já existem)
  - Modo paused com `.read()` é raro fora de libs internas; preferir async iteration (nota 08)
- **## Armadilhas (3+):**
  1. Adicionar `'data'` listener depois de stream começar a emitir → perde chunks iniciais
  2. Não tratar `'error'` → fatal em Node 22+
  3. Esquecer `push(null)` em `_read` → stream nunca termina
  4. `_read` síncrono que sempre tem dados → loop infinito sem yield
- **## Em entrevista:**
  - Frase pronta: "A Readable stream is a source of chunks. It has two modes: flowing, where you attach a `'data'` listener and chunks are pushed to you; and paused, where you call `.read()` to pull. Modern Node code rarely uses either directly — `for await of` is the canonical idiom in 2026, and it handles backpressure automatically. To create a Readable from an iterable, `Readable.from()` is the one-liner. To implement a custom Readable, subclass and define `_read(size)`, calling `push(chunk)` for each chunk and `push(null)` to signal end."
  - Vocabulário (5+): modo flowing (flowing mode), modo paused (paused mode), empurrar chunk (push chunk), puxar chunk (pull chunk), modo objeto (object mode).
- **## Veja também:**
  - `[[02 - Os 4 tipos - Readable, Writable, Duplex, Transform]]`
  - `[[04 - Writable streams]]`
  - `[[06 - Backpressure]]`
  - `[[08 - Async iteration de streams]]`
  - `[[Node.js]]` (tronco)

### Step 4: Rubric (standard, code samples mínimo 4)

### Step 5: Commit

```bash
git add "03-Dominios/Node/Streams/03 - Readable streams.md"
git commit -m "feat(node-streams): add note 03 — Readable streams"
```

---

## Task 5: Nota 04 — Writable streams

**Files:**
- Create: `03-Dominios/Node/Streams/04 - Writable streams.md`

### Step 1: Pesquisa-âncora

```
WebFetch: https://nodejs.org/api/stream.html#writable-streams
```

### Step 2: Frontmatter

```yaml
---
title: "Writable streams"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - writable
  - backpressure
aliases:
  - Writable
  - Drain event
  - Cork
---
```

### Step 3: Escrever (350-500 linhas, PT-BR)

- **TL;DR:** Writable expõe `.write(chunk, encoding?, cb?)` que retorna **boolean** (false = backpressure, deve parar até `'drain'`). `.end()` finaliza. `.cork()`/`.uncork()` para batching. Eventos: `drain`, `finish`, `error`, `close`, `pipe`/`unpipe`. Implementação custom: subclass `Writable` + `_write(chunk, enc, cb)` + opcional `_writev(chunks, cb)`.
- **## O que é:** API de Writable detalhada.
- **## Por que importa:** ignorar o boolean de `.write()` = vazamento de memória clássico (buffer interno cresce sem limite).
- **## Como funciona:**
  1. **API básica:**
     ```javascript
     ws.write('data\n');           // retorna true se ok, false se backpressure
     ws.end('last chunk\n');       // finaliza
     ws.on('drain', () => /*...*/);
     ws.on('finish', () => /*...*/);
     ```
  2. **Respeitando backpressure:**
     ```javascript
     function writeMany(ws, items) {
       let i = 0;
       function next() {
         while (i < items.length) {
           if (!ws.write(items[i++])) {
             return ws.once('drain', next);
           }
         }
         ws.end();
       }
       next();
     }
     ```
  3. **`cork()`/`uncork()` para batching:**
     ```javascript
     ws.cork();
     ws.write('a');
     ws.write('b');
     ws.write('c');
     process.nextTick(() => ws.uncork()); // emite tudo de uma vez
     ```
  4. **Implementação custom:**
     ```javascript
     import { Writable } from 'node:stream';
     class LoggingWritable extends Writable {
       _write(chunk, enc, cb) {
         console.log('chunk:', chunk.toString());
         cb();
       }
     }
     ```
  5. **`_writev` para batching otimizado:**
     ```javascript
     class BatchedWritable extends Writable {
       _writev(chunks, cb) {
         // chunks é array de { chunk, encoding }
         // emitir de uma vez (DB batch insert, etc.)
         cb();
       }
     }
     ```
- **## Na prática:** padrão observado:
  - `pipeline()` cuida de backpressure automaticamente — manual só em código de baixo nível
  - `cork()`/`uncork()` em hot path para reduzir syscalls
  - `_writev` quando destino suporta batching (DB writes, batched HTTP)
- **## Armadilhas (3+):**
  1. Ignorar boolean de `.write()` → vazamento de memória
  2. Esquecer `.end()` → nunca emite `'finish'`, consumer fica esperando
  3. `cork()` sem `uncork()` → buffer interno cresce sem flush
  4. `_write` síncrono pesado → bloqueia event loop
- **## Em entrevista:**
  - Frase pronta: "A Writable stream is a sink. The interface is `.write(chunk)` and `.end()`. The critical detail seniors get right and juniors miss: `.write()` returns a boolean — if it returns false, you must stop writing until the `'drain'` event fires, otherwise the internal buffer grows unbounded and you leak memory. Implementing a custom Writable means subclassing and defining `_write(chunk, encoding, callback)`. For batching to a destination that supports it, override `_writev` instead. `cork()` and `uncork()` let you accumulate writes for a flush in a single tick."
  - Vocabulário (5+): sumidouro (sink), evento drain (drain event), retroalimentação (backpressure), encalhar (cork), descarregar (uncork).
- **## Veja também:**
  - `[[03 - Readable streams]]`
  - `[[05 - Duplex e Transform]]`
  - `[[06 - Backpressure]]`
  - `[[07 - pipeline vs pipe - error handling]]`
  - `[[Node.js]]` (tronco)

### Step 4: Rubric

### Step 5: Commit

```bash
git add "03-Dominios/Node/Streams/04 - Writable streams.md"
git commit -m "feat(node-streams): add note 04 — Writable streams"
```

---

## Task 6: Nota 05 — Duplex e Transform

**Files:**
- Create: `03-Dominios/Node/Streams/05 - Duplex e Transform.md`

### Step 1: Pesquisa-âncora

```
WebFetch: https://nodejs.org/api/stream.html#class-streamduplex
WebFetch: https://nodejs.org/api/stream.html#class-streamtransform
```

### Step 2: Frontmatter

```yaml
---
title: "Duplex e Transform"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - duplex
  - transform
aliases:
  - Duplex
  - Transform
  - _transform
  - _flush
---
```

### Step 3: Escrever (350-500 linhas, PT-BR)

- **TL;DR:** Duplex tem read e write **independentes** (TCP socket: lê do peer, escreve pro peer; dois canais lógicos). Transform é Duplex onde a escrita feeds a leitura através de uma transformação (`zlib`, `crypto`, parsers). Implementação custom de Transform: `_transform(chunk, enc, cb)` + opcional `_flush(cb)`.
- **## O que é:** distinção precisa entre os dois.
- **## Por que importa:** confundir Duplex com Transform = implementação errada. Duplex tem dois buffers separados; Transform tem fluxo conectado.
- **## Como funciona:**
  1. **Duplex (independente):** TCP socket exemplo
     ```javascript
     // ws://server: socket.write(msg) → peer; socket.on('data', ...) ← peer
     // os canais são INDEPENDENTES
     ```
  2. **Transform (entrada→saída conectadas):**
     ```javascript
     import { Transform } from 'node:stream';
     class ToUpperCase extends Transform {
       _transform(chunk, enc, cb) {
         this.push(chunk.toString().toUpperCase());
         cb();
       }
     }
     ```
  3. **`_flush` para emit final:**
     ```javascript
     class LineParser extends Transform {
       buffer = '';
       _transform(chunk, enc, cb) {
         this.buffer += chunk.toString();
         const lines = this.buffer.split('\n');
         this.buffer = lines.pop() || ''; // última linha pode estar incompleta
         for (const line of lines) this.push(line + '\n');
         cb();
       }
       _flush(cb) {
         if (this.buffer) this.push(this.buffer);  // emite o que sobrou
         cb();
       }
     }
     ```
  4. **Object mode em Transform** — onde line parsers, CSV → JSON, etc. moram:
     ```javascript
     class JsonParse extends Transform {
       constructor() { super({ objectMode: true }); }
       _transform(line, enc, cb) {
         try { this.push(JSON.parse(line)); cb(); }
         catch (e) { cb(e); }
       }
     }
     ```
- **## Na prática:** padrões observados:
  - Transform compostos via pipeline: `pipeline(source, lineParser, jsonParse, processor, sink)`
  - `_flush` essencial em parsers (último chunk pode não terminar na fronteira)
  - Object mode + Transform = idioma para processamento estruturado
- **## Armadilhas (3+):**
  1. Esquecer `_flush` em parser → último chunk perdido
  2. `cb(error)` esquecido → erro não propaga
  3. Chamar `cb` antes de `push` → ordem confusa em alguns casos
  4. Confundir Duplex com Transform — Duplex tem 2 buffers; Transform tem 1 fluxo
- **## Em entrevista:**
  - Frase pronta: "Duplex and Transform both implement read and write, but they're conceptually different. Duplex has **two independent channels** — the canonical example is a TCP socket where you read from the peer and write to the peer through separate logical buffers. Transform is a Duplex where what you write feeds the read side after a transformation — `zlib.createGzip()` is the classic example. To implement a custom Transform, you subclass and define `_transform(chunk, encoding, callback)`, optionally `_flush(callback)` to emit any remaining state at end."
  - Vocabulário (5+): canal duplo (duplex channel), transformação (transformation), fluxo encadeado (chained flow), descarga final (flush), modo objeto (object mode).
- **## Veja também:**
  - `[[02 - Os 4 tipos - Readable, Writable, Duplex, Transform]]`
  - `[[03 - Readable streams]]`
  - `[[04 - Writable streams]]`
  - `[[06 - Backpressure]]`
  - `[[10 - Padrões práticos]]`
  - `[[Node.js]]` (tronco)

### Step 4: Rubric

### Step 5: Commit

```bash
git add "03-Dominios/Node/Streams/05 - Duplex e Transform.md"
git commit -m "feat(node-streams): add note 05 — Duplex e Transform"
```

---

## Task 7: Nota 06 — Backpressure

**Files:**
- Create: `03-Dominios/Node/Streams/06 - Backpressure.md`

### Step 1: Pesquisa-âncora

```
WebFetch: https://nodejs.org/api/stream.html#buffering
WebFetch: https://nodejs.org/en/learn/modules/backpressuring-in-streams
```

### Step 2: Frontmatter

```yaml
---
title: "Backpressure"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - backpressure
  - performance
aliases:
  - Retroalimentação
  - drain event
  - highWaterMark
---
```

### Step 3: Escrever (400-550 linhas, PT-BR — tema central)

- **TL;DR:** Backpressure = sinal explícito do consumer dizendo "estou cheio, pare de produzir". Em Node, a sinalização é o boolean retornado por `.write()` (false = pare; espere `'drain'`). `highWaterMark` define o limite (default 16KB binary, 16 objects). Sem respeitar backpressure: buffer interno cresce → memory growth → OOM.
- **## O que é:** mecânica explícita.
- **## Por que importa:** vazamento de memória mais comum em Node app que processa dados em streams.
- **## Como funciona:**
  1. **`highWaterMark`:** limite do buffer interno por stream
  2. **Sinal:** `.write()` retorna false quando buffer atinge limite
  3. **Pausa:** parar de chamar `.write()` até `'drain'` event
  4. **Code sample CORRETO** vs **INCORRETO** (com leak demonstrado):
     ```javascript
     // INCORRETO — ignora backpressure
     for (const chunk of milhoesDeChunks) {
       ws.write(chunk);  // buffer interno cresce sem parar
     }
     
     // CORRETO — respeita backpressure
     async function writeAll(ws, chunks) {
       for (const chunk of chunks) {
         if (!ws.write(chunk)) {
           await new Promise(resolve => ws.once('drain', resolve));
         }
       }
       ws.end();
     }
     ```
  5. **`pipeline()` resolve isso automaticamente** — code sample lado a lado
- **## Na prática:** quando você implementa custom:
  - Sempre respeitar boolean de `.write()`
  - `pipeline()` é a forma idiomática (não chamar `.write()` manualmente)
  - Em writers customizados, o sinal sai via `cb()` em `_write` (chamar quando consumiu)
- **## Armadilhas (3+):**
  1. Ignorar boolean de `.write()` em loop → memory growth
  2. `for (const x of arr) ws.write(x)` em arr grande → leak silencioso
  3. Achar que `pipeline` não tem backpressure — tem, ela só esconde
  4. Tunar `highWaterMark` muito alto sem medir → mascara bug, não resolve
- **## Em entrevista:**
  - Frase pronta: "Backpressure is the mechanism by which a slow consumer signals back to a fast producer to slow down. In Node Streams, the signal is the boolean returned by `.write()` — if it returns false, you have to stop writing until the `'drain'` event fires. Ignoring this signal is the most common cause of memory leaks in stream-based code: the internal buffer grows unbounded. The `highWaterMark` defines the threshold — default 16KB for binary streams, 16 for object mode. The modern idiom is `pipeline()` from `stream/promises`, which handles backpressure automatically. Manual `.write()` is only needed in low-level code."
  - Vocabulário (6+): retroalimentação (backpressure), marca d'água alta (high water mark), evento drain (drain event), buffer interno (internal buffer), memória crescente (memory growth), saturar (saturate).
- **## Veja também:**
  - `[[04 - Writable streams]]`
  - `[[07 - pipeline vs pipe - error handling]]`
  - `[[11 - Performance e tuning]]`
  - `[[Runtime e Event Loop]]` (galho 1)
  - `[[Node.js]]` (tronco)

### Step 4: Rubric (standard)

### Step 5: Commit

```bash
git add "03-Dominios/Node/Streams/06 - Backpressure.md"
git commit -m "feat(node-streams): add note 06 — Backpressure"
```

---

## Task 8: Nota 07 — pipeline vs pipe

**Files:**
- Create: `03-Dominios/Node/Streams/07 - pipeline vs pipe - error handling.md`

### Step 1: Pesquisa-âncora

```
WebFetch: https://nodejs.org/api/stream.html#streampipelinesource-transforms-destination-callback
WebFetch: https://nodejs.org/api/stream.html#streampromisespipeline-source-transforms-destination-options
```

### Step 2: Frontmatter

```yaml
---
title: "pipeline vs pipe: error handling"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - pipeline
  - error-handling
aliases:
  - pipe antipattern
  - stream/promises
  - finished
---
```

### Step 3: Escrever (350-500 linhas, PT-BR)

- **TL;DR:** `.pipe()` é antipattern moderno: não propaga erros (transform falha → source fica aberto, leak); cleanup inconsistente. `pipeline()` (callback ou `stream/promises` async) cuida de cleanup, error propagation, e suporta `AbortSignal`. Use `pipeline` por default; `.pipe()` apenas em código legacy ou casos específicos.
- **## O que é:** as duas APIs.
- **## Por que importa:** `.pipe()` em código novo é red flag de code review; é a fonte de bugs de cleanup mais comum.
- **## Como funciona:**
  1. **`.pipe()` clássico (problemático):**
     ```javascript
     // Source → transform → destination
     source.pipe(transform).pipe(destination);
     // Se transform falhar: destination fica aberto, source não para. LEAK.
     ```
  2. **`pipeline()` callback:**
     ```javascript
     import { pipeline } from 'node:stream';
     pipeline(source, transform, destination, (err) => {
       if (err) console.error('Pipeline failed:', err);
       else console.log('Pipeline succeeded');
     });
     ```
  3. **`pipeline()` async (mainstream em 2026):**
     ```javascript
     import { pipeline } from 'node:stream/promises';
     try {
       await pipeline(source, transform, destination);
       console.log('done');
     } catch (err) {
       console.error('failed:', err);
     }
     ```
  4. **Múltiplos transforms na pipeline:**
     ```javascript
     await pipeline(
       createReadStream('input.csv'),
       lineParser,
       csvParser,
       jsonStringify,
       createWriteStream('output.jsonl'),
     );
     ```
  5. **`AbortSignal` para cancelar:**
     ```javascript
     const ctrl = new AbortController();
     setTimeout(() => ctrl.abort(), 5000);  // cancel after 5s
     await pipeline(source, transform, destination, { signal: ctrl.signal });
     ```
  6. **`finished()` para esperar single stream:**
     ```javascript
     import { finished } from 'node:stream/promises';
     await finished(stream);  // resolve quando stream termina (ou rejeita em erro)
     ```
- **## Na prática:** regra de ouro:
  - Default: `await pipeline(...)` de `node:stream/promises`
  - Loops com lógica entre chunks: `for await of` (nota 08)
  - `.pipe()`: apenas em código legacy ou quando você **explicitamente** sabe que vai escutar `'error'` em todas as streams
- **## Armadilhas (3+):**
  1. `.pipe()` sem error handler em CADA stream → leak silencioso
  2. `pipeline` async sem `await` → promise rejeitada cai em `unhandledRejection`
  3. `AbortSignal` sem `.signal` no options object → erro silencioso
  4. Misturar `.pipe()` com `pipeline()` → ambíguo, evitar
- **## Em entrevista:**
  - Frase pronta: "`.pipe()` is an antipattern in modern Node code. The reason is concrete: it doesn't propagate errors. If a transform stream fails mid-pipeline, the source stream stays open, the destination stays open, and you leak file descriptors and memory. The replacement is `pipeline()` — there's a callback version and a promise version in `node:stream/promises`. The promise version is the 2026 idiom: `await pipeline(source, transform, destination)`. It handles cleanup, error propagation, and accepts an `AbortSignal` for cancellation. For waiting on a single stream to finish, `finished()` from the same module is the helper."
  - Vocabulário (5+): pipeline, propagação de erro (error propagation), limpeza (cleanup), sinal de aborto (AbortSignal), legado (legacy).
- **## Veja também:**
  - `[[06 - Backpressure]]`
  - `[[08 - Async iteration de streams]]`
  - `[[10 - Padrões práticos]]`
  - `[[12 - Armadilhas, regras práticas, cheatsheet]]`
  - `[[Node.js]]` (tronco)

### Step 4: Rubric

### Step 5: Commit

```bash
git add "03-Dominios/Node/Streams/07 - pipeline vs pipe - error handling.md"
git commit -m "feat(node-streams): add note 07 — pipeline vs pipe"
```

---

## Task 9: Nota 08 — Async iteration de streams

**Files:**
- Create: `03-Dominios/Node/Streams/08 - Async iteration de streams.md`

### Step 1: Pesquisa-âncora

```
WebFetch: https://nodejs.org/api/stream.html#consuming-readable-streams
```

### Step 2: Frontmatter

```yaml
---
title: "Async iteration de streams"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - async-iteration
  - for-await-of
aliases:
  - for await of stream
  - AsyncIterator stream
  - Readable.from generator
---
```

### Step 3: Escrever (350-500 linhas, PT-BR)

- **TL;DR:** `for await (const chunk of readable) { ... }` consome stream chunk a chunk com backpressure automático (consume → próxima iteração). Equivalente semântico ao modo paused. Async generators viram source via `Readable.from(asyncGen())`. Use async iter quando precisar de controle preciso por chunk; use `pipeline` para pipelines compostos.
- **## O que é:** Readable é AsyncIterable, então `for await of` funciona.
- **## Por que importa:** idioma moderno, mais legível que callbacks ou modo flowing manual.
- **## Como funciona:**
  1. **Consumindo Readable:**
     ```javascript
     import { createReadStream } from 'node:fs';
     for await (const chunk of createReadStream('big.txt', 'utf8')) {
       processChunk(chunk);
     }
     ```
  2. **Async generator como source:**
     ```javascript
     import { Readable } from 'node:stream';
     async function* fetchAll(urls) {
       for (const url of urls) {
         const r = await fetch(url);
         yield await r.text();
       }
     }
     const stream = Readable.from(fetchAll(urls));
     ```
  3. **Backpressure automático em `for await of`:** o loop só pede o próximo quando o body atual termina.
  4. **Error handling:** try/catch ao redor do `for await`:
     ```javascript
     try {
       for await (const chunk of stream) {
         await processChunk(chunk);
       }
     } catch (err) {
       console.error('stream failed:', err);
     }
     ```
  5. **`AbortSignal`:**
     ```javascript
     const ctrl = new AbortController();
     for await (const chunk of stream.iterator({ signal: ctrl.signal })) {
       /* ... */
     }
     ```
  6. **Comparação com `pipeline`:**
     - `pipeline(source, transform, dest)` — composição declarativa, melhor pra pipes longos
     - `for await of` — controle imperativo, melhor pra lógica condicional por chunk
- **## Na prática:** padrões:
  - Chunks com lógica de filtro/agregação por chunk → async iter
  - Pipelines composição linear → `pipeline`
  - Async generator pra fontes complexas (fetchs sequenciais, DB cursors)
- **## Armadilhas (3+):**
  1. Esquecer try/catch — erro vira `unhandledRejection`
  2. Misturar `'data'` listener + `for await of` → comportamento indefinido
  3. `await` em loop quebrado por exception → stream pode ficar half-consumed
  4. Achar que async iter "é mais lento" — overhead é mínimo em cargas reais
- **## Em entrevista:**
  - Frase pronta: "Readable streams in Node are AsyncIterable, so `for await (const chunk of readable)` is the idiomatic consumer pattern in 2026. It handles backpressure automatically — the loop only requests the next chunk after the body of the current iteration completes. To create a Readable from an async generator, `Readable.from(asyncGenerator())` is the one-liner. Choose async iteration when you need imperative control per chunk; choose `pipeline()` when you're composing a linear sequence of transforms."
  - Vocabulário (4+): iteração assíncrona (async iteration), gerador assíncrono (async generator), composição declarativa (declarative composition), controle imperativo (imperative control).
- **## Veja também:**
  - `[[03 - Readable streams]]`
  - `[[07 - pipeline vs pipe - error handling]]`
  - `[[09 - Web Streams - interop com padrão universal]]`
  - `[[10 - Padrões práticos]]`
  - `[[Node.js]]` (tronco)

### Step 4: Rubric

### Step 5: Commit

```bash
git add "03-Dominios/Node/Streams/08 - Async iteration de streams.md"
git commit -m "feat(node-streams): add note 08 — Async iteration"
```

---

## Task 10: Nota 09 — Web Streams interop

**Files:**
- Create: `03-Dominios/Node/Streams/09 - Web Streams - interop com padrão universal.md`

### Step 1: Pesquisa-âncora

```
WebFetch: https://nodejs.org/api/webstreams.html
WebFetch: https://streams.spec.whatwg.org/
```

### Step 2: Frontmatter

```yaml
---
title: "Web Streams: interop com padrão universal"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - web-streams
  - interop
  - portability
aliases:
  - Web Streams API
  - ReadableStream
  - WritableStream
---
```

### Step 3: Escrever (400-550 linhas, PT-BR)

- **TL;DR:** Node suporta Web Streams (padrão WHATWG) desde v18. APIs interop: `Readable.fromWeb(webReadable)`, `Readable.toWeb(nodeReadable)`. `fetch()` retorna Web Stream em `response.body`. Use Web Streams quando portabilidade importa (browser, Deno, Bun, Cloudflare Workers, Edge); use Node Streams quando integração madura com `fs`/`net`/`http`/`zlib` for crítica.
- **## O que é:** padrão WHATWG `ReadableStream`, `WritableStream`, `TransformStream`.
- **## Por que importa:** em 2026, código portátil entre runtimes (Node, browser, Deno, Bun, Edge) usa Web Streams. Node Streams ainda é mainstream em apps Node-only.
- **## Como funciona:**
  1. **Web Stream básico:**
     ```javascript
     const stream = new ReadableStream({
       start(controller) {
         controller.enqueue('a');
         controller.enqueue('b');
         controller.close();
       },
     });
     const reader = stream.getReader();
     while (true) {
       const { done, value } = await reader.read();
       if (done) break;
       console.log(value);
     }
     ```
  2. **Interop Node ↔ Web:**
     ```javascript
     import { Readable } from 'node:stream';
     const nodeStream = createReadStream('file.txt');
     const webStream = Readable.toWeb(nodeStream);
     // ou inverso
     const back = Readable.fromWeb(webStream);
     ```
  3. **`fetch()` retorna Web Stream:**
     ```javascript
     const r = await fetch('https://example.com/big.json');
     for await (const chunk of r.body) {  // Web Stream é AsyncIterable
       process(chunk);
     }
     ```
  4. **`pipeTo` e `pipeThrough`:**
     ```javascript
     await source.pipeTo(destination);
     const transformed = source.pipeThrough(transformStream);
     ```
  5. **`tee()` para dois consumers:**
     ```javascript
     const [stream1, stream2] = source.tee();
     ```
  6. **`TransformStream`:**
     ```javascript
     const upperCase = new TransformStream({
       transform(chunk, controller) {
         controller.enqueue(chunk.toUpperCase());
       },
     });
     ```
- **## Na prática:** decisão pragmática 2026:
  - **Use Web Streams quando:** código deve rodar em multi-runtime (Cloudflare Worker + Node API), consumindo `fetch()` body, ou novo módulo sem deps Node-specific
  - **Use Node Streams quando:** integração com `fs`/`net`/`http`/`zlib` ou ecossistema de libs (pino, busboy, csv-parser)
  - **Interop quando crossing boundary:** ex: `fetch()` body → process com Node Transform → escrever em `fs.createWriteStream` (use `Readable.fromWeb`)
- **## Armadilhas (3+):**
  1. Achar que Web Streams substitui Node Streams completamente — não, complementam
  2. Esquecer que `fetch()` retorna Web Stream — tentar usar `.pipe()` falha
  3. `tee()` em Web Stream com consumers de velocidades diferentes — mais lento determina o avanço
  4. APIs sutilmente diferentes: encoding, error handling, cancelation
- **## Em entrevista:**
  - Frase pronta: "Web Streams are the WHATWG standard — `ReadableStream`, `WritableStream`, `TransformStream`. Node has supported them since v18, with interop helpers: `Readable.fromWeb` and `Readable.toWeb`. The choice between Web Streams and Node Streams in 2026 is pragmatic: use Web Streams when the code needs to run portably — Cloudflare Workers, Deno, Bun, browser. Use Node Streams when you're integrating with mature Node-specific APIs like `fs`, `net`, or `zlib`. The most common interop scenario is consuming `fetch()` response bodies, which are Web Streams even in Node, and piping them into Node sinks."
  - Vocabulário (5+): padrão universal (universal standard), portabilidade (portability), interoperabilidade (interop), fronteira de runtime (runtime boundary), encadeamento (piping).
- **## Veja também:**
  - `[[02 - Os 4 tipos - Readable, Writable, Duplex, Transform]]`
  - `[[08 - Async iteration de streams]]`
  - `[[10 - Padrões práticos]]`
  - `[[Node.js]]` (tronco)

### Step 4: Rubric

### Step 5: Commit

```bash
git add "03-Dominios/Node/Streams/09 - Web Streams - interop com padrão universal.md"
git commit -m "feat(node-streams): add note 09 — Web Streams interop"
```

---

## Task 11: Nota 10 — Padrões práticos

**Files:**
- Create: `03-Dominios/Node/Streams/10 - Padrões práticos.md`

### Step 1: Pesquisa-âncora

```
WebFetch: https://github.com/mafintosh/csv-parser
WebFetch: https://github.com/mscdex/busboy
```

### Step 2: Frontmatter

```yaml
---
title: "Padrões práticos"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - patterns
  - line-parser
  - csv
aliases:
  - Stream patterns
  - line parser
  - CSV streaming
  - fetch streaming
---
```

### Step 3: Escrever (350-500 linhas, PT-BR — estrutura tópica)

Estrutura tópica: cada padrão em sub-seção compacta de 30-50 linhas.

- **TL;DR:** Recipes do dia a dia: line parser, CSV → JSONL, multipart upload, fetch streaming, stream tee. Cada um em sua sub-seção; foco em "este é o pattern, copie e adapte".
- **## O que é:** índice dos padrões cobertos.
- **## Padrão 1: Line parser** (Transform que quebra chunks em linhas)
  - Code sample completo (~20 linhas)
  - Cuidado: last-line-incomplete via buffer interno + `_flush`
- **## Padrão 2: CSV → JSONL** (compose Transforms)
  - Code sample com pipeline: file → line parser → CSV split → JSON.stringify → JSONL output
- **## Padrão 3: Multipart upload streaming** (sem buffer everything do request body)
  - Usar `busboy` com Express/Fastify
  - Code sample minimal de upload de arquivo grande
- **## Padrão 4: fetch streaming** (consumir `response.body` chunk a chunk)
  - Bom pra LLM streaming, SSE, downloads grandes
  - Code sample: `for await (const chunk of (await fetch(url)).body) {...}`
- **## Padrão 5: Stream tee** (`stream.PassThrough` + clone para 2 consumers)
  - Code sample para "send to S3 and to local file simultaneously"
- **## Padrão 6 (bônus): Multiplexing N streams em 1**
  - Concatenar `Readable.from`-able sources num único stream com merge ordering
- **## Na prática:** quando inventar pattern customizado vs usar lib (`csv-parser`, `busboy`, `pino`).
- **## Armadilhas (3+):**
  1. Line parser sem `_flush` → última linha perdida
  2. Multipart sem stream → buffer everything no body do request
  3. `tee` com consumers de velocidades muito diferentes → lento bloqueia o rápido
- **## Em entrevista:**
  - Frase pronta: "Common stream patterns in production: a line parser is a Transform with an internal buffer that splits chunks on newlines, with `_flush` to emit any partial last line. CSV-to-JSONL is just a pipeline of Transforms — line parser, CSV split, `JSON.stringify`, write to file with newlines. For multipart uploads, libraries like `busboy` give you Transforms that parse the body chunk by chunk without buffering. For `fetch()` streaming, the response body is a Web Stream that you can iterate with `for await of`. For sending the same data to multiple sinks, `tee()` or `PassThrough` clones the stream."
  - Vocabulário (5+): line parser, multipart, streaming de fetch (fetch streaming), bifurcação (tee), multiplexação (multiplexing), buffer interno (internal buffer).
- **## Veja também:**
  - `[[03 - Readable streams]]`
  - `[[04 - Writable streams]]`
  - `[[05 - Duplex e Transform]]`
  - `[[07 - pipeline vs pipe - error handling]]`
  - `[[08 - Async iteration de streams]]`
  - `[[09 - Web Streams - interop com padrão universal]]`
  - `[[Node.js]]` (tronco)

### Step 4: Rubric (standard, code samples mínimo 5 — um por padrão)

### Step 5: Commit

```bash
git add "03-Dominios/Node/Streams/10 - Padrões práticos.md"
git commit -m "feat(node-streams): add note 10 — Padrões práticos"
```

---

## Task 12: Nota 11 — Performance e tuning

**Files:**
- Create: `03-Dominios/Node/Streams/11 - Performance e tuning.md`

### Step 1: Pesquisa-âncora

Sem WebFetch específica — síntese sobre performance principles.

### Step 2: Frontmatter

```yaml
---
title: "Performance e tuning"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - performance
  - tuning
  - highWaterMark
aliases:
  - Stream performance
  - highWaterMark tuning
  - Stream benchmarks
---
```

### Step 3: Escrever (350-500 linhas, PT-BR)

- **TL;DR:** Streams têm overhead constante; pra payloads pequenos (<10MB) o buffer-everything ganha. Em transforms síncronos triviais, custo de stream supera benefício. `highWaterMark` raramente precisa de tuning — default está certo na maioria dos casos. Princípios > benchmarks (números envelhecem).
- **## O que é:** quando streams ganham e quando perdem.
- **## Por que importa:** "vou usar streams porque é melhor" sem medir é cargo cult; senior mede ou justifica.
- **## Como funciona:**
  1. **Quando streams NÃO ajudam:**
     - Payloads pequenos (<10MB): overhead > benefício
     - Transform sync trivial: custo de Transform > custo de map em array
     - Operações que precisam de view global (sort total, dedup): você precisa do buffer mesmo
     - Lookups paralelos por chunk: difícil paralelizar dentro de stream
  2. **`highWaterMark` tuning:**
     - Default 16KB binary, 16 objects — está certo na maioria dos casos
     - Subir: throughput sustentado em I/O lento (ex: rede com latência alta)
     - Baixar: pipeline interativo de baixa latência (ex: SSE)
     - Code sample de comparação
  3. **Sync vs async transforms:**
     - Sync transform é mais rápido (sem overhead de Promise)
     - Mas transform síncrono longo bloqueia event loop
     - Regra: transform sync se < ~1ms; async (callback ou await em `_transform`) se mais
  4. **Princípios > benchmarks:**
     - Overhead de stream é ~constante por chunk
     - Throughput depende de chunk size e fork de operações
     - Sempre medir antes de tunar
  5. **Benchmark ilustrativo (se cabe):**
     - Setup descrito (Node version, hardware classe, payload size)
     - Conclusão genérica (streams ganham acima de X MB)
- **## Na prática:** patterns:
  - Default `highWaterMark` na maioria dos casos
  - Subir só quando profile mostra que buffer está vazio com producer fast
  - Stream + Worker Thread (galho 2) quando transform é CPU-bound
- **## Armadilhas (3+):**
  1. Tunar `highWaterMark` sem medir — pode mascarar bug, não resolver
  2. Achar que stream é sempre mais rápido — overhead em casos pequenos
  3. Transform síncrono que demora >1ms → bloqueio invisível do loop
  4. Misturar sync e async transforms na mesma pipeline sem entender custo
- **## Em entrevista:**
  - Frase pronta: "Stream performance is counterintuitive. There's a constant overhead per chunk, so for small payloads, buffer-everything is faster. The signal that streams win is sustained throughput on large payloads. The `highWaterMark` is the threshold for the internal buffer — default 16KB binary, 16 objects in object mode — and it rarely needs tuning. Synchronous transforms are faster than async ones because there's no Promise overhead, but a synchronous transform that takes longer than a millisecond blocks the event loop, which can cascade across all requests. The rule of thumb: measure before tuning, and reach for streams when memory or sustained throughput is the bottleneck, not by default."
  - Vocabulário (5+): overhead constante (constant overhead), throughput sustentado (sustained throughput), tunagem (tuning), transformação síncrona (sync transform), bloqueio invisível (invisible blocking).
- **## Veja também:**
  - `[[06 - Backpressure]]`
  - `[[10 - Padrões práticos]]`
  - `[[12 - Armadilhas, regras práticas, cheatsheet]]`
  - `[[Runtime e Event Loop]]` (galho 1)
  - `[[Paralelismo]]` (galho 2 — Worker Thread + stream)
  - `[[Node.js]]` (tronco)

### Step 4: Rubric

### Step 5: Commit

```bash
git add "03-Dominios/Node/Streams/11 - Performance e tuning.md"
git commit -m "feat(node-streams): add note 11 — Performance e tuning"
```

---

## Task 13: Nota 12 — Armadilhas e cheatsheet

**Files:**
- Create: `03-Dominios/Node/Streams/12 - Armadilhas, regras práticas, cheatsheet.md`

### Step 1: Síntese das 11 notas anteriores

Reler todas e extrair as armadilhas mais críticas. Síntese sem WebFetch.

### Step 2: Frontmatter

```yaml
---
title: "Armadilhas, regras práticas, cheatsheet"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - streams
  - cheatsheet
  - armadilhas
  - referencia
aliases:
  - Cheatsheet streams
  - Armadilhas Node streams
---
```

### Step 3: Escrever (300-450 linhas, PT-BR — estrutura tópica)

- **TL;DR:** Cheatsheet de fechamento. Top 10 armadilhas, tabela 4 tipos × atributos, decision tree "qual API usar", vocabulário PT→EN, próximos galhos.

- **## Top 10 armadilhas** — lista numerada com (a) descrição 1 linha, (b) exemplo curto, (c) fix 1 linha:
  1. Não respeitar boolean de `.write()` → memory leak. Fix: `if (!ws.write(x)) await once(ws, 'drain')`
  2. `.pipe()` sem error handler em CADA stream → leak silencioso. Fix: `await pipeline(...)` de `stream/promises`
  3. Esquecer `.end()` em writable → consumer espera para sempre. Fix: sempre `.end()` ou `pipeline()` que cuida
  4. Recursão em `_transform` → stack overflow. Fix: nunca chamar `this._transform` recursivamente
  5. Object mode esquecido em parser → chunks viram strings concatenadas. Fix: `super({ objectMode: true })` no constructor
  6. `pipeline` async sem `await` → unhandledRejection. Fix: sempre `await pipeline(...)`
  7. Transform síncrono >1ms → bloqueio invisível do event loop. Fix: async (callback ou await em `_transform`)
  8. Missing `_flush` em parser → último chunk perdido. Fix: implementar `_flush(cb)` que emite buffer
  9. `Readable.from` com iterable que crasha → stream não trata throw da iteration. Fix: try/catch no generator ou error handler
  10. Passar 0-byte chunk como signal de fim → não é convenção; usar `push(null)`
  11. (bônus) `tee()` Web Stream com consumers desbalanceados → lento bloqueia rápido

- **## Cheatsheet — 4 tipos × 5 atributos:**

  | Atributo | Readable | Writable | Duplex | Transform |
  |---|---|---|---|---|
  | API principal | `.read()`, `for await of` | `.write()`, `.end()` | ambos | herda Duplex |
  | Implementação custom | `_read(size)` + `push(chunk)` | `_write(chunk, enc, cb)` | `_read` + `_write` | `_transform`, opt `_flush` |
  | Eventos chave | `data`, `end`, `error` | `drain`, `finish`, `error` | union dos anteriores | union dos anteriores |
  | Exemplo canônico | `fs.createReadStream` | `fs.createWriteStream` | `net.Socket` | `zlib.createGzip()` |
  | Atalho moderno | `Readable.from(iter)` | `pipeline(...)` | — | — |

- **## Decision tree compactada — "qual API usar":**

  ```
  Vou consumir stream?
  ├─ Loop com lógica condicional por chunk → for await of
  ├─ Pipeline composta de transforms → pipeline (stream/promises)
  └─ Single stream, esperar terminar → finished()
  
  Vou criar stream?
  ├─ De um array/iterable → Readable.from(iter)
  ├─ De async generator → Readable.from(asyncGen())
  ├─ Custom logic → subclass Readable + _read
  └─ Stream universal multi-runtime → ReadableStream (Web Streams)
  
  Vou transformar dados?
  ├─ Pipeline simples → Transform + pipeline
  ├─ Universal multi-runtime → TransformStream (Web Streams)
  └─ Lógica condicional → for await of + processamento
  ```

- **## Vocabulário PT→EN consolidado** (mínimo 18 termos): chunk, throughput, retroalimentação (backpressure), evento drain (drain event), encalhar (cork), descarregar (uncork), modo flowing (flowing mode), modo paused (paused mode), modo objeto (object mode), pilha de chamadas (call stack), pipeline, propagação de erro (error propagation), limpeza (cleanup), sinal de aborto (AbortSignal), sumidouro (sink), fonte (source), bifurcar (tee), multiplexação (multiplexing), padrão universal (universal standard), portabilidade (portability), interoperabilidade (interop), stream síncrono (sync stream).

- **## Próximos galhos:**
  - Pra **observar streams em produção**: galho 5 (Observability) — métricas de throughput, latência por chunk, pool monitoring
  - Pra **frameworks que abstraem streams** (multer, busboy integrados): galho 4 (Frameworks)
  - Pra **isolamento e sandbox de streams** (rate limit, validação): galho 6 (Segurança)

- **## Veja também** (12+ wikilinks): MOC, todas as 11 notas, Node.js (tronco), Runtime e Event Loop (galho 1), Paralelismo (galho 2)

### Step 4: Rubric adaptada

```
[ ] TL;DR no callout [!abstract]
[ ] Top 10 armadilhas (mínimo) com exemplo + fix
[ ] Cheatsheet 4 tipos × 5 atributos
[ ] Decision tree compactada (qual API usar)
[ ] Vocabulário PT→EN com 18+ termos
[ ] Wikilinks: 12+ (todas as notas + MOC + tronco + galhos 1 e 2)
[ ] Frontmatter completo (tags inclui cheatsheet)
[ ] Sem fabricação
```

### Step 5: Commit

```bash
git add "03-Dominios/Node/Streams/12 - Armadilhas, regras práticas, cheatsheet.md"
git commit -m "feat(node-streams): add note 12 — Armadilhas, cheatsheet"
```

---

## Task 14: Pass final no MOC

**Files:**
- Modify: `03-Dominios/Node/Streams/Streams.md`

- [ ] **Step 1: Confirmar 12 notas existem**

```bash
ls "03-Dominios/Node/Streams/" | wc -l
# Esperado: 13 (12 notas + MOC)
```

- [ ] **Step 2: Substituir placeholder de intro**

Em `Streams.md`, substituir `(introdução curta — preencher na Task 14)` por:

```markdown
Este galho cobre **streams em Node** — abstração fundamental para processar dados em chunks sem carregar tudo em memória. Inclui o mental model dos 4 tipos (Readable, Writable, Duplex, Transform), backpressure como mecânica explícita, `pipeline` como API moderna que substitui `.pipe()`, async iteration com `for await of`, Web Streams interop (padrão universal de 2026), padrões práticos (line parser, CSV → JSONL, fetch streaming, multipart upload) e tuning de performance.

Pré-requisito: galho 1 ([[Runtime e Event Loop]]) — pressupõe entender event loop e bloqueio. Galho 2 ([[Paralelismo]]) é referência cruzada onde workers + streams se cruzam (`postMessage` + `transferList` para zero-copy).

**Audiência primária:** dev senior em prep para entrevista internacional. Cada nota tem seção "Em entrevista" com frase pronta em inglês + vocabulário.

**Audiência secundária:** o mesmo dev em produção, debugando memory growth em endpoint que processa CSVs grandes ou throughput baixo de pipeline de transform.
```

- [ ] **Step 3: Verificar 12 wikilinks**

```bash
ls "03-Dominios/Node/Streams/"
```

Confirmar todos os 12 nomes de nota + `Streams.md` (MOC). Se algum estiver faltando ou com nome diferente, BLOCKED.

- [ ] **Step 4: Verificar dataview path**

Confirmar `"03-Dominios/Node/Streams"` no bloco dataview (não outro caminho).

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Node/Streams/Streams.md"
git commit -m "feat(node-streams): finalize MOC with all wikilinks and intro"
```

---

## Task 15: Poda do tronco (4 seções)

**Files:**
- Modify: `03-Dominios/JavaScript/Backend/Node.js.md`

Esta é a poda mais agressiva (4 seções, vs 1 no galho 2 e 5 no galho 1).

- [ ] **Step 1: Localizar 4 seções**

```bash
grep -nE "^### Streams — deep dive|^### Backpressure|^### Web Streams vs Node streams|^### Stream patterns" "03-Dominios/JavaScript/Backend/Node.js.md"
```

Esperado: 4 matches. Anotar números de linha. **Cuidado:** as 4 seções são consecutivas em ordem (Streams deep dive → Backpressure → Web Streams → Stream patterns), todas dentro de `## Como funciona`. Após elas vem outra seção (provavelmente `### npm e Package Management` ou similar).

Se algum nome divergir, ajustar.

- [ ] **Step 2: Substituir `### Streams — deep dive`**

Substituir TODO o conteúdo dessa seção por:

```markdown
### Streams — deep dive

> [!nota] Migrado para galho próprio
> Os 4 tipos de stream foram expandidos em [[Streams]] (galho 3). Veja em particular [[02 - Os 4 tipos - Readable, Writable, Duplex, Transform]] (visão geral comparativa), [[03 - Readable streams]] (Readable detalhado), [[04 - Writable streams]] (Writable detalhado) e [[05 - Duplex e Transform]] (Duplex vs Transform).
```

- [ ] **Step 3: Substituir `### Backpressure`**

```markdown
### Backpressure

> [!nota] Migrado para galho próprio
> Backpressure como mecânica explícita foi expandido em [[06 - Backpressure]] no galho [[Streams]].
```

- [ ] **Step 4: Substituir `### Web Streams vs Node streams`**

```markdown
### Web Streams vs Node streams

> [!nota] Migrado para galho próprio
> Interop Node ↔ Web Streams foi expandido em [[09 - Web Streams - interop com padrão universal]] no galho [[Streams]].
```

- [ ] **Step 5: Substituir `### Stream patterns`**

```markdown
### Stream patterns

> [!nota] Migrado para galho próprio
> Padrões práticos (line parser, CSV → JSONL, fetch streaming, multipart, tee) foram expandidos em [[10 - Padrões práticos]] no galho [[Streams]]. Decision tree e armadilhas em [[12 - Armadilhas, regras práticas, cheatsheet]].
```

- [ ] **Step 6: Adicionar `[[Streams]]` no `## Veja também` do tronco**

Como **terceiro bullet** (após `[[Runtime e Event Loop]]` e `[[Paralelismo]]`):

```markdown
- [[Streams]] — galho 3 da trilha Node Senior; abstração fundamental para processar dados em chunks (4 tipos, backpressure, pipeline, async iter, Web Streams, padrões práticos)
```

- [ ] **Step 7: Atualizar `updated:` no frontmatter do tronco**

Mudar para `updated: 2026-05-08`.

- [ ] **Step 8: Commit**

```bash
git add "03-Dominios/JavaScript/Backend/Node.js.md"
git commit -m "refactor(node): prune trunk Node.js.md, link to Streams branch"
```

---

## Task 16: MOC central + verificação final

**Files:**
- Modify: `03-Dominios/Node/index.md`

- [ ] **Step 1: Atualizar MOC central**

Em `03-Dominios/Node/index.md`, na seção "Galhos da trilha Node Senior", adicionar como **terceiro bullet**:

```markdown
- [[Streams]] — galho 3: abstração fundamental para processar dados em chunks (4 tipos, backpressure, pipeline, async iter, Web Streams, padrões práticos, performance)
```

Atualizar `updated: 2026-05-08`.

- [ ] **Step 2: Commit MOC central**

```bash
git add "03-Dominios/Node/index.md"
git commit -m "feat(node-streams): wire branch into central Node MOC"
```

- [ ] **Step 3: Verificação final**

```bash
# 1. 13 arquivos no diretório
ls "03-Dominios/Node/Streams/" | wc -l
# Esperado: 13

# 2. Todos com publish: true
grep -l "publish: true" "03-Dominios/Node/Streams/"*.md | wc -l
# Esperado: 13

# 3. Total de linhas do galho
wc -l "03-Dominios/Node/Streams/"*.md | tail -1

# 4. Tronco tem 9 callouts (5 do galho 1 + 1 do galho 2 + 4 do galho 3 = 10) — wait, 5+1+4 = 10, not 9
grep -c "Migrado para galho próprio" "03-Dominios/JavaScript/Backend/Node.js.md"
# Esperado: 10 (5 do galho 1 + 1 do galho 2 + 4 do galho 3)

# 5. MOC central linka pros 3 galhos
grep -E "Runtime e Event Loop|Paralelismo|Streams" "03-Dominios/Node/index.md" | grep -v "^#" | wc -l
# Esperado: pelo menos 3 matches
```

Reportar resultados.

- [ ] **Step 4: Closing commit**

```bash
git commit --allow-empty -m "chore(node-streams): close branch Galho 3 — Streams

12 atomic notes + MOC published in 03-Dominios/Node/Streams/.
Trunk Node.js.md pruned (4 sections — most aggressive yet). Central
Node MOC updated. All acceptance criteria from
2026-05-08-node-streams-design.md met."
```

**Sem `Co-Authored-By`.**

- [ ] **Step 5: Quartz status**

CI workflow `.github/workflows/trigger-site-deploy.yaml` dispara em push pra main. Confirmar arquivo existe; sem build local.

```bash
ls /home/josenaldo/repos/personal/codex-technomanticus/.github/workflows/ 2>/dev/null
```

---

## Pós-execução

1. **Atualizar memória** se aprendizado novo apareceu (galho 3 tem peculiaridades — poda mais agressiva, padrões tópicos em mais de uma nota)
2. **Revisar `2026-05-07-node-roadmap-design.md`** — após 3 galhos, política de poda está consistente. Pode ser hora de avaliar destino do tronco
3. **Próximo galho** — escolher entre Galho 4 (Frameworks), Galho 5 (Observability), Galho 6 (Segurança)

---

## Self-review do plano

- **Spec coverage:**
  - 12 nomes de nota do spec seção 5 cobertos por Tasks 2-13 ✓
  - MOC criado em Task 1, finalizado em Task 14 ✓
  - 5 rotas alternativas presentes no MOC esqueleto ✓
  - Tasks de poda (4 seções, spec seção 10): cobertas em Task 15 ✓
  - Atualização do MOC central: Task 16 ✓
  - Critérios de aceitação (spec seção 12): checklist em Task 16 step 3 ✓
  - Bibliografia (spec seção 8): centralizada no topo + WebFetch específico em cada Task ✓
  - Restrição de fabricação: bloco no topo + na rubrica ✓

- **Placeholder scan:** O único `(introdução curta — preencher na Task 14)` é placeholder INTENCIONAL com instrução explícita de substituição ✓

- **Type consistency:** títulos batem entre Tasks 1 (MOC esqueleto), 2-13 (criação), 14 (pass final), 15 (poda do tronco). Wikilinks consistentes ✓

- **Coesão com galhos anteriores:** wikilinks pra `[[Runtime e Event Loop]]`, `[[Paralelismo]]`, `[[10 - Bloqueio do event loop - sintomas e causas]]` aparecem nas notas certas ✓
