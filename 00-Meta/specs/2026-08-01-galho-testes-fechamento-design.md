---
title: "Galho Testes — passe de fechamento (diagnóstico, fronteira, enriquecimento, mídia)"
created: 2026-08-01
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - engenharia
  - testes
---

# Galho Testes — passe de fechamento

## Contexto e correção de registro

O Roadmap central listava, no **Tier 2 — consolidação de 🟡**:

> **Testes conceitual** (17 notas) — vertente JS já feita à parte; falta atomizar o conceitual.

**Isso está errado.** O galho `03-Dominios/Engenharia/Testes/` **já é** trilha atômica em 3 fases desde
2026-06-18 — construído pelo spec [[00-Meta/specs/2026-06-18-galho-testes-plan|2026-06-18-galho-testes-plan]],
que refatorou o monólito `Ciência/Testes.md` (584 ln) em 16 notas. As "17 notas" são **16 notas + o `index.md`**.

É o mesmo erro de registro encontrado em [[03-Dominios/Engenharia/Complexidade de Software/index|Complexidade de Software]]
em 2026-07-31 — inclusive com o mesmo número enganoso (17). Lição recorrente: **o Roadmap central não é
fonte de verdade sobre estado de galho**; o `roadmap.md` do galho é (ver [[project-roadmap-tree]]).

### Estado medido (grep, 2026-08-01)

| Sinal | Estado |
|---|---|
| Notas `NN - Título.md` + `fase:` no frontmatter | ✅ 16/16 — Iniciado 01-04 · Adepto 05-11 · Magus 12-16 |
| MOC `index.md` agrupado por fase, com aliases | ✅ |
| Diagramas Mermaid | ✅ 3–6 por nota (média ~4) |
| `## Em entrevista` | ✅ 15/16 (a 16 **é** a nota de entrevista) |
| `## Fontes` / callout Lastro | ✅ 16/16 |
| Wikilinks por nota | ✅ 10–22 (40 no capstone) |
| Capstone | ✅ já existe — nota 16 |
| Experiências reais do usuário | ✅ preservadas conforme o spec de origem |
| `## O que vem a seguir` | 🚫 **0/16** |
| `## Armadilhas comuns` (como seção) | 🚫 **0/16** — os `[!warning]` existem soltos, 1–5 por nota |
| `## Inglês` / tabela PT↔EN | 🚫 só na 16 |
| Mídia (vídeo verificado) | 🚫 **0/16** |
| `publish:` | 🚫 `false` em 16/16 (só o `index.md` é `true`) |
| `roadmap.md` do galho | 🚫 não existe |

**Não falta**: atomizar, capstone, conteúdo, fontes ou diagramas. Falta **casca, fronteira, mídia e registro**.

## Escopo

**Recorte:** passe de fechamento sobre um galho cujo miolo já está bom. Não é consolidação.

**Dentro:**
1. Diagnóstico → `roadmap.md` do galho.
2. Decisão de fronteira em nível de galho (o galho como centro stack-agnóstico que **despacha**).
3. Enriquecimento nota a nota via suíte canônica (casca + conexões + mídia numa visita só).
4. Publicação, roadmap 17/17, correção do Tier 2, memória.

**Fora:**
- Reescrever o miolo das notas.
- Criar notas novas (o roster de 16 está fechado).
- Reabrir as vertentes de stack — só reciprocidade de ponte onde faltar.
- Absorver ferramental: a fronteira "linka, não duplica" do spec de origem **permanece rígida**.

## O achado de fronteira (a razão do "pacote completo")

Levantamento de inbound/outbound em 2026-08-01. **A relação é assimétrica.**

**Inbound — forte.** Já apontam pra cá: **Testes JS** (14 notas), **Python/Testes** (8), **Arqueologia**
(01, 06, 10, 11, 12 + index), React core/25, Tooling e Build (01, 19), Paradigmas (07, 15),
Matemática/05, Carreira/Entrevistas/08, Complexidade/14, UX/47, Padrões GoF/04, `Ciência/index`,
`Engenharia/index`, Senda Entrevistas, README, index raiz.

**Outbound — cego.** O galho cita apenas `[[Testes em Java]]` (20×), `[[Testes em JavaScript]]` (8×) —
dois monólitos-ponte — e `Java/Testes/index` **1×**. Menções a:

- **Testes JS** (galho de 18 notas) → **zero**
- **Python/Testes** (galho de 9 notas) → **zero**
- **Go/15 - Testes** → **zero**
- **Arqueologia e Restauração de Software** → **zero**
- **Engenharia/Operação** → **zero**
- **Acessibilidade/14 (testes de a11y)** → **zero**

Causa: todas essas vertentes nasceram **depois** de 2026-06-18. O `index.md` do galho ainda lista, em
"Fronteiras", só Java e JavaScript.

**Nenhum wikilink quebrado** — os 4 alvos nomeados (`Testes em Java`, `Testes em JavaScript`,
`Arquitetura de Software`, `Dicionário de Ciência da Computação`) resolvem.

**Consequência de design:** o galho é o hub conceitual de um cluster grande e não se comporta como hub.
Corrigir isso é decisão **de galho**, não de nota — por isso entra na fase 0 e é gravada no `roadmap.md`
como diretriz por nota, em vez de deixar 16 subagentes redescobrirem a fronteira (o modo de falha
observado no galho de Go: agentes alucinam wikilinks vizinhos).

## Arquitetura da execução — a suíte canônica

```
/diagnosticar-galho  Engenharia/Testes     → roadmap.md (uma entrada executável por nota)
        ↓
/enriquecer-galho    Engenharia/Testes     → coordena; lê/escreve o roadmap; ccusage; ≤3 subagentes
        ↓  (por nota, 16×)
/enriquecer-nota     NN - Título.md        → Fase 0 diagnostica → Modo A (incremental)
        ├─ lentes Profundidade / Lacunas / Novidade-com-fonte  (crítico calibrado pela fase:)
        ├─ lente Conexões   ← executa o alvo de fronteira já decidido na fase 0
        └─ lente Mídia → /adicionar-midia   ← M1, legendas via uvx yt-dlp
        ↓
/verificar-nota      (gate, invocado pela própria skill ao fim)
```

**Por que a suíte e não passes separados:** casca, conexões e mídia viram **lentes da mesma visita**.
A nota é aberta uma vez e sai fechada, em vez de ser reaberta três vezes.

**Governança:** `/enriquecer-galho` roda em Opus/opusplan como coordenação pura — nunca enriquece direto.
Subagentes herdam Sonnet. Teto de **≤3 subagentes** por rodada. **Sem workflow / sem fan-out massivo**
(ver [[feedback-fan-out-excessivo]]).

## Diretrizes por fase da execução

### Fase 0 — Diagnóstico + decisão de fronteira

1. Rodar `/diagnosticar-galho` em `03-Dominios/Engenharia/Testes` → gera `roadmap.md`.
2. **Ajuste de régua** (lição de Complexidade: o checklist genérico do `verificar-nota` sub-avalia galho
   conceitual). Registrar no `roadmap.md`, **nunca** preencher seção pra cumprir agenda
   (ver [[feedback-regua-galho-teorico]]):
   - `## Em entrevista` conta como seção-lente local do galho.
   - Piso de linhas **não** se aplica — vigora o padrão capítulo de livro ([[feedback-padrao-capitulo-livro]]).
   - "Casos práticos" só onde o caso é real; **jamais fabricar** experiência do usuário
     ([[feedback-no-fabrication]]).
3. **Gravar a diretriz de fronteira por nota no `roadmap.md`**, para a lente Conexões apenas executar:

| Nota | Alvo de despacho a acrescentar |
|---|---|
| 02 pirâmide | Testes JS/01 (cenário JS) · Operação (onde a pirâmide encontra a esteira) |
| 04 unitários | Python/Testes/01-03 · Go/15 · Testes JS/02-04 |
| 05 test doubles | Testes JS/06 (Vitest) · Python/Testes/04 (`unittest.mock`) · Testes JS/09 (MSW) |
| 06 comportamento | Testing Library (Testes JS/07) — a filosofia é a mesma tese |
| 07 integração | Python/Testes/05-06 · Testcontainers (Java/Testes) · Go/15/05 |
| 10 edge cases | Matemática/05 (técnicas de prova) — já linka pra cá, falta volta |
| 11 flaky | Testes JS/16 |
| 12 coverage | Testes JS/12 · Python/Testes/07 |
| 13 além do básico | Testes JS/11 (snapshot) · Acessibilidade/14 (testes de a11y) |
| 14 performance/caos | Operação (observabilidade, chaos) · Web Performance |
| 15 CI/CD | Testes JS/17 · Python/Testes/09 · **Operação** (esteira, casa canônica) |
| 16 capstone | tabela consolidada conceito → ferramenta, por stack |

4. **Eixo Arqueologia — mão dupla (prioridade).** Hoje unidirecional e é o link de maior valor pro ofício
   de consultor de legado ([[user-profile]]). Arqueologia **10** (a rede de segurança primeiro),
   **11** (approval e golden master testing), **12** (seams e quebra de dependência) apontam pra cá; o
   galho não devolve. Alvos naturais: nota **01** (por que testar → legado sem rede), **06**
   (comportamento vs implementação → characterization tests), **13** (approval/golden master pertence à
   família "além do básico").
5. **Atualizar a seção "Fronteiras" do `index.md`** com a tabela conceito → ferramenta por stack
   (Java · JS/TS · Python · Go), substituindo a lista de dois itens.

### Fase 1 — Enriquecimento nota a nota

Rodar `/enriquecer-galho`, que despacha `/enriquecer-nota` por nota. Entregas por nota:

- **`## O que vem a seguir`** (0/16) — ponte narrativa em prosa. A da **04** marca Iniciado→Adepto; a da
  **11** marca Adepto→Magus; a da **16** aponta pra fora do galho.
- **`## Armadilhas comuns`** (0/16) — os `[!warning]` existentes (1–5/nota) são **movidos, não duplicados**.
  Piso de ≥3. Casos magros conhecidos: **13** (1 warning). A **16** é **exceção declarada** — já tem
  `## 7. Armadilhas consolidadas`; não duplicar.
- **`## Inglês` + tabela PT↔EN** nas 15 — com nuance de uso real, não tradução seca. A **16** já concentra
  o vocabulário consolidado e permanece como está.
- **Conexões** — executar o alvo de fronteira da tabela acima (decidido, não descoberto pelo subagente).
- **Mídia** — ver fase 2.

**Cadência:** parar e commitar por fase da trilha — **Iniciado (01-04)**, **Adepto (05-11)**,
**Magus (12-16)**. Commits direto na `main`, **sem push**, **sem Co-Authored-By**
([[feedback-commits]]), com stage de paths **explícitos** e conferência de `git diff --cached`
([[feedback-git-commit-hygiene]] — a working tree tem trabalho paralelo do usuário).

### Fase 2 — M1 (mídia)

Não é um passe separado: roda **dentro da mesma visita da fase 1**, como lente Mídia da `/enriquecer-nota`,
que invoca `/adicionar-midia`. Está numerado à parte só porque tem regra própria.

A skill baixa legenda com `uvx yt-dlp` e analisa relevância antes de embutir — verificação por construção.

> **Trava dura:** um ID de YouTube só entra na nota se o `yt-dlp` **baixou legenda de fato**. Download que
> falha vira **buraco declarado**, nunca vídeo "provável". ID de YouTube é o dado que subagente mais
> alucina (lição de Complexidade e de Acessibilidade).

Meta: 16/16, com ausências declaradas onde não houver material de peso.

### Fase 3 — Fecho

1. `publish: true` nas 16 notas. **Nota:** o Quartz aparentemente ignora o campo e publica tudo que existe
   no vault público — logo isto é **alinhamento de metadado**, não abertura de exposição nova
   ([[feedback-quartz-publish-ignorado]]).
2. `roadmap.md` do galho em 17/17 ✅.
3. **Corrigir o item do Tier 2 no Roadmap central** — trocar "falta atomizar o conceitual" pelo registro
   real, no mesmo formato usado em Complexidade de Software.
4. `/verificar-wikilinks` no galho (pastas exigem `/index` — armadilha que apareceu em Complexidade).
5. Atualizar memória: criar `project_galho_testes` e ajustar o índice.

## Critérios de conclusão

- [ ] `roadmap.md` existe e fecha 17/17
- [ ] `## O que vem a seguir` em 16/16
- [ ] `## Armadilhas comuns` com ≥3 `[!warning]` em 15/16 (16 = exceção declarada)
- [ ] `## Inglês` + tabela PT↔EN em 15/16
- [ ] Despacho por stack presente no `index.md`, no capstone e nas 12 notas da tabela de fronteira
- [ ] Eixo Arqueologia recíproco (01, 06, 13)
- [ ] Mídia 16/16 ou ausência declarada por escrito
- [ ] `publish: true` em 16/16
- [ ] Zero wikilinks quebrados
- [ ] Tier 2 do Roadmap central corrigido
- [ ] Memória atualizada

## Riscos

| Risco | Mitigação |
|---|---|
| Subagente alucina wikilink vizinho (visto em Go) | Alvos de fronteira **decididos na fase 0** e gravados no roadmap; o subagente executa, não descobre |
| Subagente alucina ID de YouTube | Trava do `yt-dlp`: sem legenda baixada, sem vídeo |
| Duplicar armadilhas em vez de mover | Instrução explícita de **mover**; a 16 é exceção declarada |
| Absorver ferramental e furar a fronteira | Fronteira "linka, não duplica" reafirmada; exemplos de código seguem mínimos e ilustrativos |
| Estouro de custo | ≤3 subagentes, sem workflow, parada por fase, ccusage pela `/enriquecer-galho` |
| `git add` varrer trabalho paralelo do usuário | Stage explícito + `git diff --cached` antes de cada commit |
