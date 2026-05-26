---
title: "Spec — Sub-trilha Streams (Galho 3)"
date: 2026-05-08
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Sub-trilha "Streams" (Galho 3)

## 1. Contexto e motivação

Esta é a **terceira sub-trilha** (galho 3) do roadmap descrito em `2026-05-07-node-roadmap-design.md`. Pressupõe leitura desse roadmap — a metáfora tronco/galhos, os padrões editoriais comuns, e a política de poda do `Node.js.md` monolítico não são repetidos aqui.

Streams são a **abstração fundamental** do Node para processar dados em chunks sem carregar tudo em memória. Aparecem em todo lugar: `fs.createReadStream`, HTTP requests/responses, `process.stdin`/`stdout`, sockets TCP, zlib, crypto, parsers. Mas a maioria dos devs Node usa streams **apenas via APIs prontas** — sem entender backpressure, sem distinguir os 4 tipos, sem saber por que `.pipe()` é antipattern moderno.

O contraste relevante para senior:

- **Pleno**: usa streams quando uma lib pede; copia padrões de Stack Overflow; bug aparece em prod ("memory cresce sem parar") e culpa é difusa
- **Senior**: entende backpressure como mecânica explícita; sabe que `.pipe()` não propaga erros e usa `pipeline` (`stream/promises`); sabe quando preferir async iteration; usa Web Streams quando portabilidade importa

Em 2026, há **três modelos de streams convivendo**:

1. **Node Streams clássico** — APIs maduras, integração profunda com `fs`/`net`/`http`/`zlib`
2. **Web Streams** — padrão WHATWG, default em browser/Deno/Bun/Cloudflare Workers; Node suporta interop desde v18
3. **Async iteration** — `for await of` sobre Readable, idioma moderno que esconde modos flowing/paused

O senior não escolhe um e ignora os outros — sabe quando cada um é a escolha certa.

A sub-trilha existe para dar ao leitor:

1. **Mental model** dos 4 tipos + backpressure como conceito explícito
2. **Domínio operacional** das APIs maduras (Readable/Writable/Duplex/Transform internals)
3. **Idioma moderno** (async iteration, Web Streams interop)
4. **Padrões práticos** (line parser, CSV → JSONL, fetch streaming, multipart upload)
5. **Performance e tuning** — onde streams ganham/perdem
6. **Vocabulário em inglês** para entrevista internacional

## 2. Objetivo

Produzir **12 notas atômicas + 1 MOC** (13 arquivos) em `03-Dominios/Node/Streams/`, todas `publish: true`, em PT-BR, cobrindo do mental model dos 4 tipos ao tuning de performance, passando pelos padrões idiomáticos de 2026 (async iteration, Web Streams).

A trilha precisa ser:

- **Atômica** — cada nota linkável e citável separadamente
- **Híbrida em camadas** — TL;DR + corpo técnico, no padrão do roadmap
- **Complementar aos galhos anteriores** — pressupõe galho 1 (event loop, bloqueio); galho 2 (paralelismo) é referência cruzada quando workers consomem/produzem streams
- **Idiomática 2026** — Node 22 LTS / 24, `stream/promises` mainstream, Web Streams como opção real para apps portáveis
- **Orientada a entrevistas internacionais** — cada nota tem "Em entrevista" com frase pronta em inglês + vocabulário; rota alternativa "entrevista" no MOC

## 3. Escopo

### Em escopo

- 13 arquivos markdown em `03-Dominios/Node/Streams/`
- Todos com `publish: true`
- Idioma: PT-BR; termos técnicos em inglês mantidos (stream, backpressure, pipeline, transform, etc.)
- Wikilinks densos para `[[Node.js]]` (tronco), `[[Runtime e Event Loop]]` (galho 1, em particular notas 04 e 10), `[[Paralelismo]]` (galho 2) onde workers + streams se cruzam
- Pesquisa baseada em fontes primárias (Node docs, WHATWG spec, talks de Matteo Collina)
- Tasks de poda do tronco executadas ao fechar o galho

### Fora de escopo

- **Worker Threads consumindo streams** — preview no galho 2 (notas 03/04); aqui só menção pontual
- **Frameworks que abstraem streams** (multer para upload, busboy, etc.) — vão pro galho 4
- **Observability de streams em produção** (métricas de throughput, latency por chunk) — galho 5
- **Streams customizados em performance crítica de C++/N-API** — fora do escopo do galho; foco no JS-side
- **Comparação aprofundada Node Streams vs Bun/Deno streams** — menções pontuais; comparação detalhada é fora
- **Audio/video processing pipelines complexos** — Streams são a base, mas casos específicos (FFmpeg pipelines, MediaStream) ficam fora
- **GraphQL subscriptions sobre streams** — caso muito específico; fora

## 4. Audiência e barra de qualidade

**Audiência primária:** dev senior em prep para entrevista internacional. Já trabalha com Node há anos, usa `fs.createReadStream` e `pipeline` quando precisa, mas não consegue **explicar com vocabulário preciso** o que é backpressure, por que `.pipe()` é antipattern, ou quando preferir Web Streams.

**Audiência secundária:** o mesmo dev em produção, debugando memory growth de um endpoint que processa CSVs grandes ou throughput baixo de uma pipeline de transform.

**Barra de qualidade:** ao terminar a sub-trilha, o leitor deve **compreender ao nível exigido de um senior** — decidir, justificar, reconhecer patterns e armadilhas em code review. Concretamente, deve conseguir:

1. Explicar em inglês os 4 tipos de stream (Readable, Writable, Duplex, Transform) com exemplos canônicos de cada
2. Definir backpressure com vocabulário preciso e identificar código que ignora a sinalização (`.write()` retornando false sem respeitar `'drain'`)
3. Justificar por que `pipeline()` substituiu `.pipe()` em código moderno (error propagation, cleanup automático)
4. Reconhecer quando usar async iteration (`for await of`) vs `pipeline` vs implementar custom Transform
5. Diferenciar Node Streams de Web Streams e justificar quando preferir cada um (portabilidade vs integração com APIs Node)
6. Identificar object mode em uma stream e saber por que ele muda o behavior (chunks são objetos, não Buffer/string)
7. Reconhecer pelo menos 5 armadilhas de streams ao revisar PR (sem await em `pipeline`, `.pipe()` sem error handler, transform sync que bloqueia, etc.)
8. Implementar mentalmente um line parser (`Transform` que quebra chunks em linhas) — não para escrever from scratch em entrevista, mas para descrever a abordagem
9. Citar `pipeline` (`stream/promises`) como API moderna canônica e `Readable.from(iterable)` como atalho moderno
10. Tunar `highWaterMark` quando faz diferença e saber que na maioria dos casos o default está certo

## 5. Estrutura da sub-trilha (13 arquivos)

### MOC

| # | Arquivo | Propósito |
|---|---|---|
| — | `Streams.md` | MOC do galho. Trilha sequencial 01→12 + 5 rotas alternativas. Dataview. Linka pro MOC central, tronco, galhos 1 e 2. |

### Bloco A — Mental model (2 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 01 | `01 - Por que streams.md` | Motivação | Quando usar streams: arquivos/payloads grandes (>100MB), throughput sustentado, processamento em chunks, backpressure-aware. Alternativas: buffer everything (memória explode em payload grande); paginação (latência alta em response, complexidade no client). Trade-offs: complexidade, debugging mais difícil, error handling não-trivial. Conexão com galho 1 (não bloquear event loop) e galho 2 (workers podem produzir/consumir streams via `transferList`). |
| 02 | `02 - Os 4 tipos - Readable, Writable, Duplex, Transform.md` | Visão geral comparativa | Tabela rica: tipo · interface · uso · exemplos canônicos. Readable: `fs.createReadStream`, `process.stdin`, HTTP response, `Readable.from(iterable)`. Writable: `fs.createWriteStream`, `process.stdout`, HTTP request. Duplex: `net.Socket` (read e write **independentes**, dois canais). Transform: zlib, crypto, parsers (Duplex onde write→leitura é a transformação). Quando cada um. Apontador pras notas detalhadas (03-05). |

### Bloco B — Tipos aprofundados (3 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 03 | `03 - Readable streams.md` | Modos, eventos, internals | **Modo flowing** (`'data'` listener; chunks empurrados pra você) vs **paused** (`.read()` puxa; default em Node moderno). Eventos: `data`, `end`, `error`, `close`, `readable`. Implementação custom: subclass `Readable` + `_read(size)` + `push(chunk)` / `push(null)` (end). `Readable.from(iterable)` — atalho moderno para qualquer iterable virar stream. Object mode (`{ objectMode: true }`). Erro handling e cleanup. |
| 04 | `04 - Writable streams.md` | Write, drain, internals | API: `.write(chunk, encoding?, cb?)` retorna **boolean** (false = backpressure, deve parar até `'drain'`). `.end()` finaliza. `.cork()/.uncork()` para batching. Eventos: `drain`, `finish`, `error`, `close`, `pipe`/`unpipe`. Implementação custom: subclass `Writable` + `_write(chunk, enc, cb)` + `_writev(chunks, cb)` para batching otimizado. Object mode. Padrões: contar bytes escritos, sinks de logger. |
| 05 | `05 - Duplex e Transform.md` | Quando cada, exemplos canônicos | **Duplex**: read e write independentes — TCP socket (lê do peer, escreve pro peer; dois canais lógicos). **Transform**: subclasse de Duplex onde a escrita feeds a leitura através de uma transformação (zlib, crypto, parsers). Implementação custom de Transform: `_transform(chunk, enc, cb)` + opcional `_flush(cb)` para emitir last bytes. Object mode em Transform: line parser, CSV → JSON, etc. Diferença prática: Duplex tem dois buffers separados; Transform tem o "fluxo" que conecta entrada→saída. |

### Bloco C — Backpressure e pipeline (2 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 06 | `06 - Backpressure.md` | Mecânica e por que importa | Definição: produtor mais rápido que consumidor enche o buffer interno → memória cresce. `highWaterMark` é o limite por stream (default 16KB binary, 16 objetos object mode). `.write()` retorna `false` quando passa do limite — **deve parar de escrever** até evento `'drain'`. Code sample manual de backpressure correto vs incorreto (com leak demonstrado). Sem respeitar: memory growth → OOM em produção. Como `pipeline` cuida disso automaticamente. Conexão com galho 1 (event loop não-bloqueado, mas memória sob pressão). |
| 07 | `07 - pipeline vs pipe - error handling.md` | API moderna | `.pipe()` é antipattern moderno por 2 razões: (1) não propaga erros — falha em transform deixa source aberto; (2) cleanup inconsistente em error case. `pipeline()` (callback) e `pipeline()` de `stream/promises` (await) cuidam de cleanup, error propagation, e suportam `AbortSignal`. Code sample side-by-side: `.pipe()` com leak silencioso vs `pipeline()` com cleanup correto. Múltiplos transforms na pipeline (composição). `finished()` como helper para esperar single stream end. |

### Bloco D — Streams modernos (2 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 08 | `08 - Async iteration de streams.md` | for await of + AsyncIterator | `for await (const chunk of readable) { ... }` — sintaxe moderna que lida com backpressure automaticamente (consume chunk → próxima iteração). Equivalência semântica com modo paused. Async generators como source: `Readable.from(asyncGenerator())`. Quando preferir async iter sobre `pipeline`: lógica de processamento síncrono por chunk; controle preciso. Quando preferir `pipeline`: pipelines compostos com múltiplos transforms. `AbortSignal` em iteration. Cuidado: error em loop precisa try/catch explícito. |
| 09 | `09 - Web Streams - interop com padrão universal.md` | Node ↔ Web Streams | Node suporta Web Streams desde v18. APIs interop: `Readable.fromWeb(webReadable)`, `Readable.toWeb(nodeReadable)`. `fetch()` retorna Web Stream em `response.body` (mesmo em Node moderno). Web Streams API: `getReader()`, `pipeTo()`, `pipeThrough()`, `tee()`. Quando preferir Web Streams: portabilidade (browser, Deno, Bun, Cloudflare Workers, Edge). Quando preferir Node Streams: integração madura com `fs`/`net`/`http`/`zlib`, ecossistema (libraries). Diferenças mais sutis: encoding, error handling, async iter. |

### Bloco E — Padrões e fechamento (3 notas)

| # | Arquivo | Propósito | Conteúdo-chave |
|---|---|---|---|
| 10 | `10 - Padrões práticos.md` | Recipes do dia a dia | **Line parser** (Transform que quebra chunks em linhas, lidando com last-line-incomplete via buffer interno). **CSV → JSONL** (compose Transforms: line parser → CSV parser → JSON.stringify + newline). **Multipart upload streaming** (sem buffer everything do request body; usar busboy ou parser custom em Transform). **fetch streaming** (consumir `response.body` chunk a chunk; bom pra LLM streaming, SSE, downloads grandes). **Stream tee** (`stream.PassThrough` + clone para 2 consumers). Cada padrão em 30-50 linhas, com 1 caveat e 1 referência. |
| 11 | `11 - Performance e tuning.md` | Onde streams ganham/perdem | Quando streams **não** ajudam: payloads pequenos (overhead > benefício); transforms síncronos triviais; casos com lookups paralelos por chunk (use `Promise.all` em batches). `highWaterMark` tuning: subir pra throughput em I/O sustentado, baixar pra latência em pipes interativos. Sync transforms vs async (sync é mais rápido mas pode bloquear event loop em transforms longas). Buffer pool em transforms hot. Princípios > números absolutos (benchmarks ficam datados). 1-2 benchmarks ilustrativos com setup descrito. |
| 12 | `12 - Armadilhas, regras práticas, cheatsheet.md` | Síntese | Top 10 armadilhas (não respeitar backpressure no `.write()`; `.pipe()` sem error handler; esquecer `.end()` em writable; recursão em `_transform`; object mode esquecido; `pipeline` sem `await`; transform síncrono que bloqueia; missing `_flush` em parsers; `Readable.from` com iterable que crasha; passing 0-byte chunk como signal). Cheatsheet: 4 tipos × atributos. Decision tree "qual API usar". Vocabulário PT→EN consolidado. Apontador pra galho 5 (Observability — métricas de stream em produção). |

## 6. Padrão estrutural por nota

Toda nota segue o padrão herdado do roadmap:

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
  - <conceito-tag específica>
aliases:
  - <opcional>
---

# <Título>

> [!abstract] TL;DR
> <2-4 linhas em PT-BR. Conceito + regra prática + por que importa.>

## O que é

## Por que importa

## Como funciona

## Na prática

## Armadilhas

## Em entrevista

## Veja também
```

**Variações permitidas:**

- **Nota 12 (cheatsheet):** estrutura tópica — lista de armadilhas + tabelas + decision tree. Não tem narrativa "Como funciona".
- **Nota 10 (Padrões práticos):** estrutura tópica também — cada padrão em sua sub-seção compacta.
- **MOC (`Streams.md`):** estrutura própria — abertura + Comece por aqui + 5 rotas alternativas + dataview. `type: moc`.

**Tamanho típico:** 200-500 linhas. Notas conceituais densas (06 backpressure, 09 Web Streams) podem ir até 600 quando o tema pedir.

## 7. Rotas alternativas no MOC

### Rota completa
Sequencial 01 → 12. Recomendada na primeira leitura.

### Rota entrevista internacional
01 → 02 → 03 → 04 → 06 → 07 → 09. Foco em "explicar streams pra entrevistador". Cobre motivação, 4 tipos, Readable/Writable, backpressure, pipeline, Web Streams.

### Rota produção
01 → 06 → 07 → 10 → 11 → 12. Foco em "escrever streams sem bugs em prod". Cobre motivação, backpressure, pipeline, padrões, performance, armadilhas.

### Rota async-first (2026 stack)
02 → 08 → 09 → 10. Foco em streams modernos com async iter + Web Streams.

### Rota implementing custom streams
03 → 04 → 05 → 06 → 11. Pra quem vai escrever Transform/Duplex próprio (raro mas crítico quando precisa).

## 8. Fontes principais

### Referências canônicas

- [Node.js docs — Stream](https://nodejs.org/api/stream.html)
- [Node.js docs — Web Streams API](https://nodejs.org/api/webstreams.html)
- [WHATWG Streams Standard](https://streams.spec.whatwg.org/)
- [MDN — Streams API](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API)
- [Node.js docs — `pipeline`](https://nodejs.org/api/stream.html#streampipelinesource-transforms-destination-callback)

### Referências de produção

- [pino](https://github.com/pinojs/pino) — referência canônica de stream-based logging
- [busboy](https://github.com/mscdex/busboy) — multipart parser sobre streams
- [csv-parser](https://github.com/mafintosh/csv-parser) — CSV parser sobre Transform

### Talks e artigos

- Matteo Collina — talks sobre streams (autor do `pipeline`, mantenedor histórico do módulo); buscar a mais recente
- Anna Henningsen — posts/talks sobre internals
- Robert Nagy — posts sobre Web Streams interop em Node

### A buscar conforme necessidade

- Discussões recentes sobre Web Streams como default em apps portáveis (2026)
- Posts sobre performance de streams em casos reais (CSV processing, image pipeline)
- Issues do `nodejs/node` documentando mudanças em streams entre versões 22-24

## 9. Decisões editoriais

- **Idioma:** PT-BR exclusivo nesta fase
- **Tom:** técnico mas acessível; TL;DR sempre presente
- **Versões assumidas:** Node 22 LTS e Node 24; `stream/promises` mainstream; Web Streams interop estável
- **Frontmatter:** `publish: true`, `status: seedling`, tags `[node, streams, <conceito>]`
- **Wikilinks:** densidade alta para `[[Node.js]]` (tronco), `[[Runtime e Event Loop]]` (galho 1), `[[Paralelismo]]` (galho 2 onde aplicável), e entre as 12 notas
- **Code samples:** mistura — JavaScript pra exemplos pedagógicos curtos, TypeScript pra exemplos realistas de produção
- **Inglês:** apenas em "Em entrevista" e em termos técnicos do ecossistema (stream, backpressure, pipeline, transform, etc.)

## 10. Tasks de poda do tronco

Ao fechar o galho, executar no `03-Dominios/JavaScript/Backend/Node.js.md`:

1. Substituir seção **`### Streams — deep dive`** por callout `[!nota]` apontando pra `[[Streams]]` (MOC) + `[[02 - Os 4 tipos - Readable, Writable, Duplex, Transform]]` + `[[03 - Readable streams]]` + `[[04 - Writable streams]]` + `[[05 - Duplex e Transform]]`
2. Substituir seção **`### Backpressure`** por callout apontando pra `[[06 - Backpressure]]`
3. Substituir seção **`### Web Streams vs Node streams`** por callout apontando pra `[[09 - Web Streams - interop com padrão universal]]`
4. Substituir seção **`### Stream patterns`** por callout apontando pra `[[10 - Padrões práticos]]`
5. Adicionar `[[Streams]]` no `## Veja também` do tronco como **terceiro bullet** (após `[[Runtime e Event Loop]]` e `[[Paralelismo]]`)
6. Atualizar `updated:` no frontmatter do tronco
7. Atualizar `03-Dominios/Node/index.md` (MOC central) adicionando `[[Streams]]` na seção "Galhos da trilha Node Senior"

Nota: poda mais agressiva que galho 2 (4 seções vs 1).

## 11. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Sobreposição entre nota 03 (Readable) e 08 (async iteration) | 03 cobre flowing/paused/internals; 08 foca em `for await of` e AsyncIterators (idioma moderno). Linhas claras. |
| Web Streams vs Node Streams como assunto político | Nota 09 declara explicitamente "use Web Streams quando portabilidade importar; Node Streams quando integração com APIs Node maduras (`fs`, `net`) for crítica". Sem dogma. |
| Nota 11 (Performance) ficar especulativo / desatualizar | Focar em **princípios** (overhead constante; chunks pequenos perdem; transforms sync compostos podem bloquear) com 1-2 benchmarks ilustrativos. Não em números absolutos. |
| Nota 10 (Padrões práticos) virar tutorial-zão e explodir | Cada padrão em 30-50 linhas máximo, sem refatorar pra biblioteca. Foco em "este é o pattern, copie e adapte". |
| Custom streams (notas 03/04/05 internals) ficar denso demais | Aceitar 500-600 linhas se justificado; o tema é central pra senior interview. Conteúdo "Em entrevista" foca em **explicar a API**, não implementar from scratch. |
| Confusão entre Duplex e Transform | Nota 05 dedica seção específica a "Diferença prática" com exemplo lado-a-lado. |

## 12. Critérios de aceitação

A sub-trilha está completa quando:

1. Todos os 13 arquivos existem em `03-Dominios/Node/Streams/`
2. Todos têm frontmatter completo com `publish: true`
3. MOC `Streams.md` tem 12 notas linkadas + 5 rotas alternativas + dataview
4. Cada nota satisfaz a rubrica padrão:
   - TL;DR em callout `[!abstract]`
   - 2+ wikilinks pra outras notas do galho + 1+ wikilink pra `[[Node.js]]` (tronco) ou galho anterior
   - 3+ code samples em JS ou TS
   - Seção "Em entrevista" com 1+ frase pronta em inglês + vocabulário-chave
   - Seção "Armadilhas" com 2+ armadilhas concretas
   - Frontmatter completo (`publish: true`, `status: seedling`, tags `[node, streams, <conceito>]`)
   - PT-BR natural; termos técnicos em inglês mantidos
   - **Zero atribuição de experiência pessoal ao autor**
5. Tasks de poda do tronco (seção 10) executadas
6. MOC central `03-Dominios/Node/index.md` atualizado
7. Quartz publica corretamente
8. Pelo menos 4 notas têm code sample testável em script standalone (ex: line parser minimal, fetch streaming, pipeline com 3 transforms)

## 13. Plano de execução

O plano detalhado vai em `docs/superpowers/plans/2026-05-08-node-streams-execution.md` (gerado pela skill `superpowers:writing-plans` após aprovação deste spec).

A ordem de execução recomendada:

1. MOC (esqueleto) + 01 + 02 (mental model)
2. 03 + 04 + 05 (tipos aprofundados — base do galho)
3. 06 + 07 (backpressure + pipeline — central pra produção)
4. 08 + 09 (async iter + Web Streams — modernos)
5. 10 + 11 (padrões + performance)
6. 12 (fechamento, agrega)
7. Pass final no MOC
8. Tasks de poda do tronco (1 task atômica final)
9. Atualização do MOC central

## 14. Documentos relacionados

- `2026-05-07-node-roadmap-design.md` — roadmap macro dos 6 galhos (este spec é sub-trilha #3)
- `2026-05-07-node-runtime-event-loop-design.md` — spec do galho 1
- `2026-05-07-node-paralelismo-design.md` — spec do galho 2
- Plano de execução do galho 3 (criado depois): `2026-05-08-node-streams-execution.md`
- Tronco a ser podado: `03-Dominios/JavaScript/Backend/Node.js.md`
- MOC central: `03-Dominios/Node/index.md`
- Galhos anteriores fechados: `03-Dominios/Node/Runtime e Event Loop/`, `03-Dominios/Node/Paralelismo/`
