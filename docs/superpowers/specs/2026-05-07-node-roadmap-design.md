---
title: "Spec — Roadmap Node Senior (Tronco e Galhos)"
date: 2026-05-07
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Roadmap Node Senior

## 1. Contexto e motivação

O Codex Technomanticus tem um deep dive monolítico em `03-Dominios/JavaScript/Backend/Node.js.md` (~26K, `publish: false`, status `evergreen`) que cobre desde arquitetura V8/libuv até troubleshooting em produção. É denso, panorâmico, e funciona como referência pessoal — mas é privado, monolítico, e a profundidade de cada tema é limitada pelo formato.

Em paralelo existe uma pasta `03-Dominios/Node/` recém-criada com um MOC vazio (`index.md`, `publish: true`, status `seedling`) esperando ser povoada.

A tensão é clara: o conteúdo precisa **florescer**. Conceitos que merecem nota própria estão amassados em uma seção; armadilhas que merecem cheatsheet visual estão soltas em parágrafo; vocabulário de entrevista internacional não tem onde morar.

**Metáfora orientadora deste roadmap:** o `Node.js.md` monolítico é o **tronco**. Esta trilha **enriquece o tronco até ele dar galhos**. Cada galho é uma sub-trilha temática. Cada nota atômica é uma folha. À medida que um galho amadurece, a seção correspondente do tronco é podada — substituída por um callout com wikilink. No final, o tronco pode virar um MOC ou continuar como visão panorâmica privada coexistindo com galhos públicos. Essa decisão emerge depois do primeiro galho fechar.

**Gatilho imediato:** a percepção de que muita gente usa Node todo dia mas só começa a entender a stack quando aprende como o event loop funciona — e que `async/await` não é mágica de performance. Esse é o conteúdo do **galho 1 (Runtime e Event Loop)**, ponto de entrada natural pra todos os outros galhos.

## 2. Objetivo

Definir o roadmap de 6 sub-trilhas temáticas (galhos) que progressivamente enriquecem e substituem o deep dive monolítico, estabelecendo:

- **Padrões editoriais comuns** herdados por todas as sub-trilhas (frontmatter, estrutura de nota, idioma, audiência, restrições)
- **Estrutura de blocos** de cada um dos 6 galhos (sem nomear notas individuais — isso fica pro spec específico de cada galho)
- **Dependências** entre galhos
- **Política de poda do tronco** à medida que galhos fecham
- **Critério de "galho fechado"**

Este roadmap **não detalha** o nota-a-nota das sub-trilhas. Cada sub-trilha ganha seu próprio spec quando for o momento de executá-la. A única exceção é a **sub-trilha #1 (Runtime e Event Loop)**, que tem spec completo coexistindo: `2026-05-07-node-runtime-event-loop-design.md`.

## 3. Escopo

### Em escopo

- 6 sub-trilhas (galhos) progressivamente publicadas em `03-Dominios/Node/<Nome do Galho>/`
- Padrões editoriais comuns que toda sub-trilha herda
- Política de poda do `JavaScript/Backend/Node.js.md` à medida que galhos fecham
- Critérios de aceitação aplicáveis a qualquer galho

### Fora de escopo

- **Detalhamento nota-a-nota** dos galhos 2-6 — cada um ganha seu spec quando começar
- **Refactor estrutural do tronco** antes do galho 1 fechar — a decisão sobre o que fazer com o tronco emerge da experiência de podar uma vez
- **Versão em inglês** das notas — derivação futura, projeto separado
- **Migração do conteúdo de `03-Dominios/Node/Ferramentas Node.md`** — esse placeholder fica intocado por enquanto; pode virar parte do galho 4 ou ganhar trilha própria
- **Cobertura de Bun, Deno** como runtimes alternativos — escopo é Node.js especificamente; menções pontuais quando relevante (ex: Web Streams interop)

## 4. Audiência e barra de qualidade

**Audiência primária:** dev senior em preparação para entrevista internacional. Já trabalha com Node há anos, conhece o básico de event loop e async/await, mas precisa **dominar fluentemente** o vocabulário, ser capaz de explicar mecânicas internas em inglês, e reconhecer os patterns idiomáticos modernos. Para esse público, cada nota tem seção "Em entrevista" obrigatória.

**Audiência secundária:** o mesmo dev em produção, debugando "comportamentos estranhos" (latência subindo, requests travando, memory leaks). Para esse público, cada galho tem rotas alternativas no MOC priorizando troubleshooting.

**Barra de qualidade:** ao terminar um galho, o leitor deve conseguir:

1. Explicar em inglês o conceito central do galho com vocabulário preciso
2. Identificar 3-5 armadilhas concretas que o galho cobre
3. Reproduzir os padrões idiomáticos do galho em código próprio
4. Diagnosticar problemas relacionados ao tema do galho em produção

## 5. Os 6 galhos

### Galho 1 — Runtime e Event Loop

**Escopo.** O "motor" do Node. Como Node é single-threaded mas atende milhares de conexões. Anatomia da thread JS (call stack, queues), V8 + libuv + thread pool, fases do event loop, microtasks vs macrotasks, timers, async/await em profundidade (incluindo o mito "async = performance"), bloqueio do event loop e diagnóstico.

**Blocos:** Mental model · Event loop deep dive · async/await em profundidade · Bloqueio e diagnóstico · Fechamento.

**Dependências:** nenhuma. Base de todos os outros galhos.

**Poda do tronco:** seções "Arquitetura", "Single-threaded com non-blocking I/O", "Event loop phases — detalhado", "Event loop blocking" (em Troubleshooting), parte de "Armadilhas comuns" relacionada a bloqueio.

**Spec próprio:** `2026-05-07-node-runtime-event-loop-design.md`.

### Galho 2 — Paralelismo

**Escopo.** As 3 formas de fugir do single-thread. Worker Threads (CPU-bound, comunicação via `postMessage`/`MessageChannel`, lifecycle, `SharedArrayBuffer` + `Atomics`), Cluster (HTTP scaling, primary/worker), `child_process` (`exec` vs `spawn` vs `fork`, IPC), e a "decision tree" de quando cada um. Inclui comparação com orquestradores (PM2, K8s) e por que `cluster` é menos usado em prod moderna.

**Blocos:** Worker Threads · Cluster · child_process · SharedArrayBuffer/Atomics · Decision tree · Fechamento.

**Dependências:** Galho 1 (precisa entender event loop pra entender por que fugir dele).

**Poda do tronco:** seção "Worker Threads, cluster, child_process — as 3 formas de paralelismo".

### Galho 3 — Streams

**Escopo.** Abstração fundamental do Node pra processar dados sem carregar tudo em memória. 4 tipos (Readable, Writable, Duplex, Transform), backpressure, `pipeline` vs `.pipe()`, async iteration (`for await of`), Web Streams interop (Node ↔ Web), padrões práticos (line parser, CSV → JSONL, fetch streaming).

**Blocos:** Os 4 tipos · Backpressure · pipeline e error propagation · Async iteration · Web Streams · Padrões práticos · Fechamento.

**Dependências:** Galho 1 (event loop, especialmente pra entender backpressure).

**Poda do tronco:** seções "Streams — deep dive", "Backpressure", "Web Streams vs Node streams", "Stream patterns".

### Galho 4 — Frameworks e arquitetura

**Escopo.** Trade-offs entre Express, Fastify, NestJS, Hono. Quando cada um, padrões idiomáticos de cada, Clean Architecture em Node (camadas, DI manual vs com NestJS, hexagonal). Inclui middleware/pipeline, error handling estruturado (problem details), versionamento de API.

**Blocos:** Express idiomático · Fastify · NestJS · Hono e edge runtimes · Clean Architecture em Node · Comparação cross-framework · Fechamento.

**Dependências:** Galho 1 (event loop). Idealmente Galho 3 (streams) e Galho 5 (observability) prontos antes, mas não obrigatório.

**Poda do tronco:** seções "Frameworks", "Error Handling".

### Galho 5 — Observability e produção

**Escopo.** Como manter Node em produção saudável. Profiling (`--inspect`, clinic.js doctor/bubble/flame, autocannon), logging estruturado (pino, correlation IDs), métricas (Prometheus, OpenTelemetry, Node-specific metrics), graceful shutdown (SIGTERM, drain), circuit breaker (opossum), connection pool tuning, memory leak detection (heap snapshots, `--expose-gc`).

**Blocos:** Profiling · Logging estruturado · Métricas e tracing · Graceful shutdown · Circuit breaker e resiliência · Connection pool · Memory leak detection · Fechamento.

**Dependências:** Galho 1. Galho 4 facilita exemplos.

**Poda do tronco:** seções "Connection pool exausto", "Memory leak", "Graceful shutdown", "Circuit breaker", parte de "Event loop blocking".

### Galho 6 — Segurança e supply chain

**Escopo.** Segurança específica de Node. `npm audit` + Snyk, supply chain (lockfile, npm provenance, sigstore, malicious packages), secrets (env, vault, sops), input validation (zod/joi), rate limiting, sandbox (`vm` module, `isolated-vm`, SES), `Permission Model` nativo (Node 20+).

**Blocos:** Supply chain (npm) · Secrets management · Input validation · Rate limiting e DoS protection · Sandbox e isolation · Permission Model nativo · Fechamento.

**Dependências:** nenhuma técnica direta. Pode ser feito a qualquer momento depois do Galho 1.

**Poda do tronco:** Node.js.md tem pouco sobre segurança hoje — esse galho mais **adiciona** que poda. Item da meta-nota "8. Security" do tronco vira seção mais robusta apontando pras notas.

## 6. Ordem sugerida

1. **Galho 1 (Runtime e Event Loop)** — agora, base de tudo
2. **Galho 2 (Paralelismo)** ou **Galho 3 (Streams)** — qual estiver mais quente
3. **Galho 5 (Observability)** — depois que 1+2+3 deram base pra explicar diagnóstico
4. **Galho 4 (Frameworks)** — quando for útil pra projeto/entrevista específicos
5. **Galho 6 (Segurança)** — pode entrar entre quaisquer outros, é independente

A ordem é sugestão, não compromisso. Galhos podem ser reordenados quando a necessidade real (entrevista marcada, bug em prod, projeto específico) puxar um deles pra frente.

## 7. Padrões editoriais herdados

Toda sub-trilha herda os seguintes padrões. Onde uma sub-trilha precise desviar, o desvio é justificado no spec próprio.

### Localização e nomenclatura

- Pasta `03-Dominios/Node/<Nome do Galho>/`
- Numeração local dentro de cada galho (`01 - <título>.md`, `02 - ...`)
- MOC do galho em `<Nome do Galho>.md` na raiz da pasta (homônimo da pasta) com rotas alternativas
- MOC central `03-Dominios/Node/index.md` atualizado a cada galho que fecha

### Frontmatter padrão por nota

```yaml
---
title: "<título sem prefixo numérico>"
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
type: concept
status: seedling
publish: true
tags:
  - node
  - <galho-tag: event-loop, paralelismo, streams, frameworks, observability, security>
  - <conceito-tag: 1-3 tags específicas>
aliases:
  - <opcional>
---
```

MOCs usam `type: moc`.

### Estrutura padrão por nota

```markdown
# <Título>

> [!abstract] TL;DR
> <2-4 linhas. Conceito central + regra prática + por que importa.>

## O que é

## Por que importa

## Como funciona

## Na prática

## Armadilhas

## Em entrevista

## Veja também
```

Variações são permitidas quando o conteúdo pedir (ex: nota de fechamento pode ter "Cheatsheet" no lugar de "Como funciona"). Esqueleto serve de referência, não de gabarito rígido.

**Tamanho típico:** 200-500 linhas por nota.

### Idioma e tom

- **PT-BR exclusivo** nesta fase
- Termos técnicos mantidos em inglês (event loop, microtask, backpressure, etc.) — não traduzir o que o ecossistema não traduz
- Seção "Em entrevista" tem **frase pronta em inglês** + **vocabulário-chave** com tradução
- Tom técnico mas acessível, com TL;DR sempre presente

### Versões assumidas

- **Node 22 LTS** (stable, 2024-2025) e **Node 24** (current, 2025-2026)
- **V8 12.x** (Node 22) e **V8 13.x** (Node 24)
- **libuv 1.x**
- **TypeScript 5.x** quando code samples usam TS

Versões assumidas são declaradas no frontmatter quando relevante (ex: nota sobre Permission Model do Node 20+ menciona explicitamente).

### Code samples

- TypeScript moderno preferencialmente
- JavaScript quando o conceito for naturalmente JS (ex: explicar runtime, exemplos pedagógicos curtos)
- Comentários em PT-BR onde didáticos
- Exemplos testados quando possível (Node REPL, scripts standalone, TypeScript Playground)

### Wikilinks

- Densidade alta
- Sempre que possível, linkar pra:
  - `[[Node.js]]` (tronco) — `JavaScript/Backend/Node.js.md`
  - `[[JavaScript Fundamentals]]` (event loop básico, closures, async)
  - `[[TypeScript]]` quando code samples usam TS
  - Outras notas do mesmo galho
  - Notas de outros galhos quando o conceito conectar

### Restrição absoluta de fabricação

A memória [Nunca inventar dados sobre o usuário](/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/feedback_no_fabrication.md) é regra inegociável.

**Nenhuma nota pode atribuir ao autor experiências profissionais, projetos, clientes, métricas ou casos não-vividos.** A seção "Na prática" usa:

- "Padrão observado em libs do ecossistema (Express, Fastify, NestJS)"
- "Caso típico em microserviços I/O-bound"
- "Armadilha comum reportada na comunidade"
- Citações com fonte verificável (docs oficiais, talks identificadas, repos públicos)
- Hipotéticos explícitos ("Imagine um servidor que processa uploads...")

Quando faltar contexto factual, **PERGUNTAR antes de escrever** — nunca preencher com plausibilidade.

## 8. Política de poda do tronco

Cada sub-trilha, ao fechar, executa uma **task de poda** do `JavaScript/Backend/Node.js.md`:

1. **Identificar** seções do tronco que correspondem ao escopo do galho
2. **Substituir** cada seção por callout `[!nota]` com 2-3 linhas de resumo + wikilink pras notas atômicas:

```markdown
> [!nota] Migrado para galho próprio
> Conceito X foi expandido em [[Nome do galho]]. Veja em particular [[01 - ...]], [[02 - ...]], [[03 - ...]].
```

3. **Atualizar** o "Veja também" do tronco linkando o MOC do galho
4. **Não apagar** nada do histórico Git — mudança via commit, sempre reversível

A decisão final sobre o destino do tronco (vira MOC enxuto? continua como visão panorâmica? vira deprecated?) é tomada **depois do galho 1 fechar** com base em:

- Quanto sobrou após a poda
- Se o que sobrou ainda tem valor coeso ou virou retalho
- Se faz sentido o tronco ser publicável (`publish: true`) ou ficar privado como visão pessoal

## 9. Critérios de "galho fechado"

Um galho está fechado quando:

1. Todas as notas do galho existem em `03-Dominios/Node/<Nome do Galho>/` com frontmatter completo e `publish: true`
2. MOC do galho tem todas as notas linkadas + 2+ rotas alternativas + dataview de "Todas as notas do galho"
3. Cada nota satisfaz a rubrica padrão:
   - TL;DR existe e é compreensível em <30 segundos
   - 2+ wikilinks pra outras notas + 1+ wikilink pro tronco ou nota de fundamento
   - 3+ code samples quando aplicável (notas conceituais puras podem ter menos)
   - Seção "Em entrevista" presente, com pelo menos 1 frase pronta em inglês
   - Seção "Armadilhas" presente, com pelo menos 2 armadilhas concretas
   - Frontmatter completo (`publish: true`, `status: seedling`, tags básicas + específicas)
   - Versões assumidas declaradas se relevante
   - PT-BR natural; termos técnicos em inglês mantidos
   - **Zero atribuição de experiência pessoal ao autor**
   - Nenhuma alegação técnica não-trivial sem fonte ou code sample que comprove
4. Tronco podado: seções correspondentes substituídas por callouts + wikilinks
5. MOC central `03-Dominios/Node/index.md` atualizado linkando o novo galho
6. Quartz publica sem erros (`npm run quartz build` ou equivalente)

## 10. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Galho 1 vira muito grande (>15 notas) e atrasa demais | Spec do galho 1 já fixa em 12 notas + 1 MOC; se inflar, separa em sub-galho 1a/1b |
| Padrões editoriais ficam desatualizados conforme galhos progridem | Roadmap é documento vivo; atualizar após cada galho fechar com aprendizados |
| Tronco fica com retalhos confusos depois da primeira poda | Decisão sobre destino do tronco emerge após galho 1 — não tentar resolver agora |
| Notas atômicas duplicarem conteúdo entre galhos (ex: backpressure aparece em Streams e Observability) | Cada galho tem dono claro do conceito; outros galhos linkam, não re-explicam |
| Ordem dos galhos mudar muito (ex: galho 4 ser puxado pra antes do 3) | Ordem é sugestão; cada galho ganha spec próprio quando começar, com revalidação de dependências |
| Galho 6 (Segurança) virar conteúdo desatualizado rapidamente | Versões assumidas declaradas; revisar frontmatter `updated` a cada 6 meses |
| Notas ficarem genéricas demais (estilo "tutorial qualquer") | Restrição de fabricação força "Na prática" a ser ancorado em fonte ou hipotético explícito; rubrica exige frase em inglês concreta na "Em entrevista" |

## 11. Próximos passos

1. **Aprovação deste roadmap** + spec da sub-trilha #1 (`2026-05-07-node-runtime-event-loop-design.md`)
2. **Plano de execução do galho 1** via skill `superpowers:writing-plans`
3. **Execução do galho 1** via `superpowers:subagent-driven-development` ou `superpowers:executing-plans`
4. **Poda do tronco** correspondente ao galho 1
5. **Revisão do roadmap** com aprendizados do galho 1 antes de iniciar galho 2

## 12. Documentos relacionados

- `2026-05-07-node-runtime-event-loop-design.md` — spec detalhado da sub-trilha #1
- Plano de execução (criado depois): `docs/superpowers/plans/2026-05-07-node-runtime-event-loop-execution.md`
- Tronco a ser podado: `03-Dominios/JavaScript/Backend/Node.js.md`
- MOC central: `03-Dominios/Node/index.md`
- Spec de referência (formato análogo): `2026-04-26-typescript-react-design.md`
