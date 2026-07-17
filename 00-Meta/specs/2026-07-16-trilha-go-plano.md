---
title: "Plano de Execução — Trilha Go"
type: spec
created: 2026-07-16
updated: 2026-07-16
status: growing
publish: false
tags:
  - meta
  - spec
  - roadmap
  - go
aliases:
  - Plano Trilha Go
---

# Plano de Execução — Trilha Go

> **Design de origem:** [[2026-07-16-trilha-go-design|Design — Trilha Go]]. Este plano detalha a construção. A trilha corre em granularidade de **galho** (um por vez, direto na `main`); cada galho é detalhado em notas quando chega a vez dele.

**Objetivo:** Construir a trilha Go em `03-Dominios/Tecnologia/Go/` — 21 galhos + capstone, notas atômicas em 3 fases, padrão capítulo com lente cross-stack.

**Arquitetura:** Galhos flat numerados (`01 - ...` a `21 - ...`) sob `Tecnologia/Go/`. Cada nota é escrita via `/escrever-nota`, auditada por `/verificar-nota`, commitada. Cada galho tem `roadmap.md`. `index.md` é o MOC da trilha.

**Tech Stack (do vault):** Obsidian Flavored Markdown · skills `/escrever-nota` · `/verificar-nota` · `/enriquecer-nota` · `/diagnosticar-galho` · Mermaid · Dataview.

## Restrições globais (valem para TODA nota)

- **Padrão capítulo:** TL;DR (`[!abstract]`) → abertura-problema (cenário, não "X é...") → mecanismo com ≥1 diagrama Mermaid → casos práticos → armadilhas comuns (`[!warning]`) → "O que vem a seguir" (bridge para a PRÓXIMA nota) → Fontes (com URLs).
- **Registro Feynman:** analogias, perguntas retóricas, resumo em 1 linha; parágrafos curtos; sem padding.
- **Lente cross-stack:** onde ajudar, tabela/callout "vindo de Java/Node/Python, em Go é assim" — recurso, nunca pré-requisito.
- **Fases:** `fase: Iniciado|Adepto|Magus` no frontmatter. Piso subordinado ao padrão capítulo (Iniciado ~300+ / Adepto ~400+ / Magus ~500+).
- **Versão-base:** Go 1.23+ (marcar caducidade com `[!info]` onde a API é recente — ex.: loop var 1.22, `slog` 1.21, generics 1.18).
- **Frontmatter:** `title`, `type: concept`, `fase`, `tags` (incl. `go`), `publish: true`, `created`/`updated`.
- **Commits:** um commit por nota (ou por par coeso), path explícito, sem assinatura Claude. Push manual.

---

## Fase 0 — Andaime da trilha (antes do galho 1)

### Task 0: Reestruturar a pasta Go e criar o MOC

**Files:**
- Modify: `03-Dominios/Tecnologia/Go/index.md` (vira MOC da trilha)
- Modify: `03-Dominios/Tecnologia/Go/Go Backend.md` (marca como tronco podado; conteúdo migra ao longo dos galhos)
- Create: `03-Dominios/Tecnologia/Go/roadmap.md` (roadmap-pai da trilha)

- [ ] **Passo 1:** Reescrever `index.md` como MOC da trilha: TL;DR, tabela dos 21 galhos + capstone (com estado ⬜/🟡/✅), seção "Como ler" (ordem dos blocos), Veja também. Não remover o arquivo (regra Quartz).
- [ ] **Passo 2:** Adicionar callout `[!info]` no topo de `Go Backend.md` marcando-o como material legado cujo conteúdo está sendo migrado para os galhos (com links para 9/11/16/18 conforme forem criados).
- [ ] **Passo 3:** Criar `roadmap.md` (galho-pai) via template `00-Meta/templates/Template - Roadmap.md`, listando os 21 galhos como sub-galhos ⬜ não diagnosticados.
- [ ] **Passo 4:** Commit: `git add 03-Dominios/Tecnologia/Go/{index,roadmap}.md "03-Dominios/Tecnologia/Go/Go Backend.md"` → `docs(go): andaime da trilha — MOC + roadmap-pai + poda do Go Backend`.

---

## Galho 1 — Fundamentos e sintaxe (DETALHADO)

**Pasta:** `03-Dominios/Tecnologia/Go/01 - Fundamentos e sintaxe/`
**Meta:** ~8 notas em 3 fases. Fundar a linguagem para quem nunca viu Go.

**Fronteiras (o que NÃO vai aqui):**
- Value vs pointer *semantics de métodos* → galho 2 (aqui só o mecanismo `*`/`&`).
- Interfaces → galho 3. Erros a fundo → galho 4. Slices/maps a fundo → galho 5. Goroutines → bloco 2.

**Roster de notas:**

| # | Nota | Fase | Escopo |
|---|------|------|--------|
| 01 | O que é Go e o modelo de compilação | Iniciado | filosofia/história, compilação estática, binário autocontido, `go run`/`go build`, `package main`/`func main`, primeiro programa |
| 02 | Variáveis, tipos básicos e zero values | Iniciado | `var`/`:=`, numéricos/bool/string, `const`/`iota`, **zero values**, conversões explícitas (sem coerção implícita) |
| 03 | Controle de fluxo | Iniciado | `if` (com init statement), `for` (o único loop, 4 formas), `switch` (sem fallthrough, com condições), `defer` (intro) |
| 04 | Funções | Adepto | múltiplos retornos, named returns, variadic, funções como valores, closures, `defer` a fundo (ordem LIFO) |
| 05 | Pacotes, imports e visibilidade | Adepto | `package`, imports, **exported/unexported (maiúscula)**, `init()`, organização de arquivos |
| 06 | Módulos e o toolchain | Adepto | `go mod init/tidy`, semantic versioning, `go.sum`, `go fmt`/`vet`/`build`/`run`, GOPATH→modules |
| 07 | Ponteiros e o modelo de memória | Magus | `*`/`&`, quando usar ponteiro, value vs reference na passagem, sem aritmética de ponteiro, `new` |
| 08 | Idiomático desde o início | Magus | gofmt como lei, naming conventions (curto, MixedCaps), "accept interfaces" teaser, o "less is more", erros comuns de quem vem de Java/Node/Python |

**MOC do galho:** `03-Dominios/Tecnologia/Go/01 - Fundamentos e sintaxe/index.md` agrupando por fase.
**Roadmap do galho:** `.../01 - Fundamentos e sintaxe/roadmap.md`.

### Ciclo por nota (repetir para 01→08)

- [ ] **Passo A — Escrever:** `/escrever-nota "03-Dominios/Tecnologia/Go/01 - Fundamentos e sintaxe/0N - <título>"` com o escopo da linha da tabela. Padrão capítulo + restrições globais.
- [ ] **Passo B — Gate:** `/verificar-nota` na nota recém-criada.
- [ ] **Passo C — Ajustar:** se o gate apontar lacuna (falta Mermaid, abertura sem cenário, TL;DR raso, refs sem URL), corrigir inline.
- [ ] **Passo D — Commit:** `git add "<path da nota>"` → `feat(go): galho 1 nota 0N — <título>` (path explícito, sem assinatura).

### Fecho do galho 1

- [ ] **Passo E:** Criar/atualizar `index.md` do galho (MOC por fase) e `roadmap.md` do galho (8/8 ✅).
- [ ] **Passo F:** Atualizar `roadmap.md`-pai da trilha (galho 1 ✅) e o MOC `Go/index.md`.
- [ ] **Passo G:** Migrar do `Go Backend.md` o que pertence a este galho (nada específico no galho 1; a maior parte vai para 9/11/16/18).
- [ ] **Passo H:** Commit de fecho: `docs(go): fecha galho 1 — Fundamentos e sintaxe (8/8) + roadmaps`.

---

## Galhos 2–21 + Capstone (a detalhar na vez de cada um)

Cada galho, quando chegar sua vez, ganha uma seção como a do galho 1 (roster de notas por fase + fronteiras + ciclo). Roster macro dos temas em [[2026-07-16-trilha-go-design|Design]]. Sequência:

- [ ] **Galho 2:** Tipos, structs e métodos
- [ ] **Galho 3:** Interfaces e composição
- [ ] **Galho 4:** Erros como valor
- [ ] **Galho 5:** Coleções e dados
- [ ] **Galho 6:** Generics
- [ ] **Galho 7:** Goroutines e o scheduler
- [ ] **Galho 8:** Channels e select
- [ ] **Galho 9:** Sincronização e context ← migra goroutine leak / singleflight / context do `Go Backend.md`
- [ ] **Galho 10:** net/http e web frameworks
- [ ] **Galho 11:** Persistência ← migra connection pool / N+1 do `Go Backend.md`
- [ ] **Galho 12:** gRPC e protobuf (fronteira com Comunicação entre Sistemas)
- [ ] **Galho 13:** Mensageria
- [ ] **Galho 14:** Microservices e arquitetura ← migra circuit breaker do `Go Backend.md`
- [ ] **Galho 15:** Testes
- [ ] **Galho 16:** Observabilidade ← migra pprof / OTel do `Go Backend.md`
- [ ] **Galho 17:** Runtime interno
- [ ] **Galho 18:** Cloud-native e produção ← migra graceful shutdown do `Go Backend.md`
- [ ] **Galho 19:** Segurança
- [ ] **Galho 20:** Go idiomático
- [ ] **Galho 21:** Preparação para entrevista de Go
- [ ] **Capstone:** Construir um serviço Go de produção do zero

## Fecho da trilha

- [ ] Mover Go para ✅ no [[00-Meta/Roadmap|Roadmap mestre]] (Backend/Runtime + backlog Tier 1).
- [ ] Criar memória `project_trilha_go.md` + linha no `MEMORY.md`.
- [ ] Confirmar `Go Backend.md` totalmente migrado (ou reduzido a tronco podado com callouts).
