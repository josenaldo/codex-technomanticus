---
title: "Roadmap de Trilhas"
type: moc
publish: true
created: 2026-06-25
updated: 2026-06-29
status: growing
tags:
  - moc
  - meta
  - roadmap
  - planejamento
aliases:
  - Roadmap
  - Roadmap de Trilhas
  - Plano de Trilhas
---

# Roadmap de Trilhas

> [!abstract] TL;DR
> Esta é a **fonte única de verdade da ordem de construção** do grimório — o que já existe como trilha atômica, o que ainda é monólito/stub, e o que falta por completo para o perfil-alvo: **Senior Fullstack Developer** (backend Java/Spring + frontend TS/React), prep para entrevistas internacionais remotas.
>
> **Não confundir com as [[04-Sendas/Sendas|Sendas]]**: Senda = *ordem de leitura* curatorial de um tema; Roadmap = *ordem de construção* do vault. As Sendas consomem o que este Roadmap produz.

> [!info] Como manter este arquivo
> Ao concluir/criar uma trilha, mova-a de seção e atualize o `updated:`. Cada item linka o índice do domínio. Estado é avaliado por: existem notas atômicas numeradas em 3 fases (Iniciado/Adepto/Magus)? Ou é só um monólito `.md`?

## Legenda de estado

| Ícone | Estado | Significado |
| ----- | ------ | ----------- |
| ✅ | **Construída** | Trilha atômica em 3 fases, padrão capítulo, enriquecida |
| 🟡 | **Parcial** | Existe estrutura/galhos, mas incompleta ou precisa de reforma |
| 🧱 | **Monólito** | Conteúdo existe como 1 nota gigante; falta atomizar em trilha |
| ⬜ | **Stub/vazio** | Quase nada; precisa ser escrita do zero |
| 🚫 | **Sem cobertura** | Tema que um fullstack precisa e o vault não tem |

---

## 1. Tecnologia — o stack do dia a dia

### Frontend (o maior buraco para o perfil fullstack)

| Trilha | Estado | Nota |
| ------ | ------ | ---- |
| [[03-Dominios/Tecnologia/TypeScript/index\|TypeScript]] | ✅ | 27 notas, 3 fases |
| [[03-Dominios/Tecnologia/Tooling e Build/index\|Tooling e Build]] | ✅ | 26 notas, concluída 2026-06-25 |
| [[03-Dominios/Tecnologia/JavaScript/index\|JavaScript (core)]] | ✅ | 26 notas, 3 fases, concluída 2026-06-25 (monólito aposentado em stub) |
| [[03-Dominios/Tecnologia/React/index\|React]] | ✅ | domínio multi-galho **COMPLETO** (2026-06-27): **React core ✅** (26) + **Design Patterns ✅** (12) + **Next.js ✅** (16, baseline Next 15) + **Ecossistema ✅** (13, server state/client state/forms/UI/tables/charts) + TypeScript com React (15) + Charts (sub-área) |
| [[03-Dominios/Tecnologia/HTML/index\|HTML]] | ✅ | 12 notas, 3 fases (Iniciado/Adepto/Magus), concluída 2026-06-27 (monólito aposentado) |
| [[03-Dominios/Tecnologia/CSS/index\|CSS]] | ✅ | 13 notas, 3 fases (Iniciado/Adepto/Magus), concluída 2026-06-27 (monólitos aposentados) |
| [[03-Dominios/Tecnologia/Plataforma Web/index\|Plataforma Web]] | ✅ | **COMPLETA 2026-06-28**: 7 galhos (DOM/Eventos/Rendering/Web APIs/Storage/Workers/Networking), ~54 notas, 3 fases |

### Backend / Runtime

| Trilha | Estado | Nota |
| ------ | ------ | ---- |
| [[03-Dominios/Tecnologia/Java/index\|Java (Senior)]] | ✅ | 18 galhos incl. Certificação OCP |
| [[03-Dominios/Tecnologia/Node/index\|Node]] | ✅ | 8 galhos reformados — **Reforma do Node CONCLUÍDA 2026-06-29**: 95 notas (78 enriquecidas + 3 escritas do zero), todas em 3 fases, padrão capítulo com Mermaid/Casos práticos/Armadilhas |
| [[03-Dominios/Tecnologia/Go/index\|Go]] | ⬜ | stub (3 notas) |
| [[03-Dominios/Tecnologia/Python/index\|Python]] | ⬜ | stub (4 notas) |

### IA, Terminal, Infra, RPA

| Trilha | Estado | Nota |
| ------ | ------ | ---- |
| [[03-Dominios/Tecnologia/IA/index\|IA]] | 🟡 | 21 galhos; **diagnóstico nota-a-nota COMPLETO (30/06): 237 notas, ~84% no gate ≥9/12, 47 já fechadas** — plano detalhado em `guia/roadmap - ia`; ver [[#Enriquecimento do domínio IA]] |
| [[03-Dominios/Tecnologia/Terminal/index\|Terminal]] | ✅ | 7 galhos, 78 notas |
| [[03-Dominios/Tecnologia/Infraestrutura/index\|Infraestrutura]] | 🟡 | só galho Linux; falta Docker, Kubernetes, Nginx, Cloud |
| [[03-Dominios/Tecnologia/RPA/index\|RPA]] | ⬜ | stub (6 notas) |

#### Enriquecimento do domínio IA

> **Padrão completo de enriquecimento** (cristalizado no lote de 28/06): `fase:` no frontmatter · `[!question]-` após o TL;DR · seção "Armadilhas comuns" com 3 `[!warning]` · seção "Como explicar em inglês" (quote + tabela PT↔EN ≥5 linhas) · bridge "O que vem a seguir" · piso de linhas (Iniciado ≥300 / Adepto ≥400 / Magus ≥500).
>
> Galhos enriquecidos **antes** de 28/06 passaram por um padrão mais leve (estrutura + `fase:`, sem todos os elementos) — por isso os 6 parciais. Auditoria de conteúdo (grep dos marcadores + contagem de linhas) em 2026-06-29.
>
> **Régua revisada (2026-06-29):** as skills `escrever-nota`/`verificar-nota`/`enriquecer-nota` agora separam **núcleo mínimo** (TL;DR · abertura-problema · corpo-mecanismo · **O que vem a seguir** · Fontes · frontmatter) de **opcionais caso-a-caso** (Armadilhas, inglês, casos, `[!question]`, mídia — medidas por gate de score ≥9/12). `fase:` e piso de linhas valem onde o galho adota fases. **Plantar/colher dúvidas é passada pós-nota.** O diagnóstico **nota a nota** de cada galho de IA vive em `00-Meta/guia/roadmap - ia.md`.

| Galho | Notas | Enriquecido | Status | O que falta |
| ----- | ----- | ----------- | ------ | ----------- |
| AI Engineering Stack | 13 | 27/06 | ✅ qualidade alta — diagnóstico nota-a-nota FEITO (30/06), ver `guia/roadmap - ia` | TODAS 11/12 (núcleo íntegro; só P1 inaplicável). **Porém**: conteúdo real <piso na maioria (≥300 Iniciado) — ~100 linhas em branco no rodapé inflam o `wc -l` e mascararam isso. Higiene: `status:seedling` na 13, seção "inglês" duplicada na 02. |
| RAG e Vector Databases | 13 | 27/06 | 🟡 diagnóstico nota-a-nota FEITO (30/06) — ver `guia/roadmap - ia` | Mais cru que o esperado: 2×8 (<gate: 04, 08), 3×9, 6×10, 2×11; só RAG-11 fechada. Gaps frequentes: **E2 (abre sem cenário)** · **L2 (refs sem URL)** · conteúdo real <piso ≥300 em 8/13 (rodapé em branco infla wc -l). `fase: Iniciado` em todas. |
| MCP | 10 | 28/06 | 🟡 diagnóstico nota-a-nota FEITO (30/06) — ver `guia/roadmap - ia` | Mais fraco que o "completo" sugeria: 3×8 (<gate: 01/04/05), 5×9, 1×10, 1×11; nenhuma fechada. Gaps: **L2 universal** (refs em itálico, não links clicáveis) · E2 (abertura sem cenário) · E1 (TL;DR de 1 linha em 01/05/08) · E3 (ASCII, não Mermaid). `fase: Iniciado`. |
| Segurança e Guardrails | 12 | 28/06 | 🟡 diagnóstico nota-a-nota FEITO (30/06) — ver `guia/roadmap - ia` | 2×8 (<gate: 05, 07), 1×9, 9×10; nenhuma fechada. **L2 universal** (TODAS as 12 com refs sem URL) · conteúdo real <piso em várias · E2/E1 secundários · caducidade regulatória na 11 (prazo 02/08/2026). `fase: Iniciado`. |
| Memória de Agentes | 24 | 28/06 | ✅ qualidade alta — diagnóstico nota-a-nota FEITO (30/06), ver `guia/roadmap - ia` | Mais sólido do lote 28/06: 1×8 (24), 3×9, 15×10, 5×11; **7 não precisam mudança**. Notas escritas quase no piso exato (~300–301 l). Gap dominante **E2** (abre "X é..." em quase todas) · caducidade nas notas de implementação (09–17/20/24) · MA-14 com 73 linhas em branco (<piso). `fase: Iniciado`. |
| Prompt Engineering | 9 | 28/06 | 🟡 diagnóstico nota-a-nota FEITO (30/06) — ver `guia/roadmap - ia` | 1×7 (<gate: 09), 2×9, 4×10, 2×11; 2 não precisam mudança (01, 02). Gap dominante: **conteúdo real <piso** (04/08/09 com 171–201 l, rodapé em branco) · E1 (TL;DR raso) · E2 · L2. `fase: Iniciado`. |
| Structured Outputs | 8 | 28/06 | 🟡 diagnóstico nota-a-nota FEITO (30/06) — ver `guia/roadmap - ia` | 1×8 (<gate: 06), 1×9, 5×10, 1×11; 1 não precisa mudança (01). Gaps: **conteúdo real <piso** (5/8) · **E3 (Mermaid ausente)** quase universal · caducidade de API em 04/05/06 (SO-05: checar se Anthropic já tem structured output nativo). `fase: Iniciado`. |
| Evaluation | 8 | 28/06 | ✅ qualidade boa — diagnóstico nota-a-nota FEITO (30/06), ver `guia/roadmap - ia` | 1×8 (<gate: 02), 2×9, 4×10, 1×11; 3 não precisam mudança (05/07/08). Gaps leves: **E3 (Mermaid ausente)** comum · E2/E1 (TL;DR raso na 02/03) · conteúdo real <piso em 01/02. `fase: Iniciado`. |
| Observability | 8 | 28/06 | ✅ qualidade boa — diagnóstico nota-a-nota FEITO (30/06), ver `guia/roadmap - ia` | Sólido: nenhuma <gate (1×9, 6×10, 1×11); 4 não precisam mudança. Gap dominante: **E3 (Mermaid ausente** — diagramas em ASCII art) · conteúdo real <piso em 02/04 · "Veja também" duplicado na 01. `fase: Iniciado`. |
| Multimodal Prompting | 7 | 28/06 | 🟡 diagnóstico nota-a-nota FEITO (30/06) — ver `guia/roadmap - ia` | 2×8 (<gate: 02, 04), 2×9, 3×10; 2 não precisam mudança (03/06). Gaps: **E2 (abertura)** comum · E1 (TL;DR raso 01/02) · E3 (Mermaid ausente) · conteúdo <piso na 07 · caducidade na 04. `fase: Iniciado`. |
| Image Prompting | 7 | 28/06 | ✅ qualidade boa — diagnóstico nota-a-nota FEITO (30/06), ver `guia/roadmap - ia` | Nenhuma <gate (4×9, 3×10); 3 não precisam mudança (01/06/07). Gaps leves: **E2 (abertura)** em 03/04/05 · E1 (TL;DR raso 02/04) · conteúdo real <piso em 03/04/05 · caducidade na 03 (modelos). `fase: Iniciado`. |
| Improvement Loop | 7 | 28/06 | ✅ qualidade boa — diagnóstico nota-a-nota FEITO (30/06), ver `guia/roadmap - ia` | Nenhuma <gate (2×9, 5×10); 4 não precisam mudança (01/03/05/07). Gaps leves: **E3 (Mermaid — diagramas em ASCII)** universal · E2 (02/04) · conteúdo real <piso em 04/06. `fase: Iniciado`. |
| Ferramentas de IA | 5 | 28/06 | 🟡 diagnóstico nota-a-nota FEITO (30/06) — ver `guia/roadmap - ia` | 5 notas-referência grandes (626–910 l), não trilha. 1×8 (<gate: Claude), 4×9. Achado universal: **TL;DR `[!abstract]` ausente/informal nas 5** (núcleo) + **caducidade pesada** (preços/modelos/datas em TODAS — envelhecem mais rápido do domínio) + E3 (ASCII) + armadilhas duplicadas (Codex/Copilot). `fase: Iniciado`. (Roadmap antes dizia 6 notas; são 5.) |
| Agentes de Codificação | 18 | 27/06 | 🟡 diagnóstico nota-a-nota FEITO (30/06) — ver `guia/roadmap - ia` | Sólido: TODAS ≥9 (2×9, 11×10, 5×11); 3 não precisam mudança. Gap **sistêmico E5**: "O que vem a seguir" existe mas aponta pro futuro-do-produto/notas relacionadas, não pra PRÓXIMA nota da sequência (~13 notas). Mais: `fase:` ausente na 01 · caducidade nas notas de ferramenta (Cursor/Copilot/Windsurf/Devin/benchmarks) · L1 em algumas. P1 inaplicável. |
| Context Engineering | 16 | 27/06 | 🟡 diagnóstico nota-a-nota FEITO (30/06) — ver `guia/roadmap - ia` | **Galho mais consistente**: TODAS ≥9 (1×9, 7×10, 7×11, 1×12); **9 não precisam mudança**. `fase: Adepto` em todas. Gaps residuais só polimento: L1 (cross-galho) · L2 (URLs nas refs) · piso ≥400 por poucas linhas em ~5 · P1 majoritariamente inaplicável. |
| Economia de Tokens | 22 | 27/06 | 🟡 diagnóstico nota-a-nota FEITO (30/06) — ver `guia/roadmap - ia` | **Bimodal**: intro 01–04 crua (SEM `fase:`, ~110–310 l, 5–7/12, falta E2/E5/inglês) vs corpo 05–22 forte (`fase: Adepto`, todas ≥9; ET-05 = **12/12**). Gaps do corpo: L1 (cross-galho) · L2 (URLs nas refs) · piso ≥400 por 1–28 l em várias · caducidade em 04/08/19/20/21. Distr.: 3×5,1×7,3×9,7×10,7×11,1×12. |
| Spec-Driven Development | 12 | 27/06 | 🟡 diagnóstico nota-a-nota FEITO (30/06) — ver `guia/roadmap - ia` | **Galho mais cru: TODAS as 12 <gate** (1×4, 4×5, 5×6, 2×7). Notas longas (~400 l) e ricas, mas faltam sistematicamente: bridge **E5** (todas) · URLs nas refs/L2 (todas) · seção de **inglês** E6/E7 (quase todas) · Anti-patterns→`[!warning]` · cross-galho L1. `fase:` ausente (galho por sequência). |
| Anatomia de Agents | 11 | 25/06 | 🟡 diagnóstico nota-a-nota FEITO (30/06) — ver `guia/roadmap - ia` | Mais cru que LLMs: 4 notas <gate (8/12: 01/04/05/08), 5 em 9, 2 em 10; nenhuma fechada. Falta: bridge **"O que vem a seguir"** em TODAS as 11 · Anti-patterns→`[!warning]` em ~9 · URLs nas refs (L2) em 5. `fase:` ausente (galho por sequência). |
| Anatomia dos LLMs | 24 | 24/06 | 🟡 diagnóstico nota-a-nota FEITO (29/06) — ver `guia/roadmap - ia` | Núcleo OK: todas ≥9/12 (04 = 11/12, única sem pendência). Falta: bridge **"O que vem a seguir"** em ~22 notas (têm "Veja também", falta a ponte narrativa) · converter Armadilhas→`[!warning]` em ~17 · `[!info]` de caducidade em 07/08/12/17. `fase:` ausente por decisão do spec (galho por Blocos). |
| O Lado Sombrio da IA | 1 | — | ⬜ fora de escopo | cluster crítico fora das trilhas (só "Débito cognitivo") |
| Claude Code | 0 | — | ⬜ fora de escopo | pasta vazia |

> **Diagnóstico nota-a-nota CONCLUÍDO (30/06):** todas as 237 notas (19 galhos + 3 soltas) auditadas, uma por vez, contra a régua das skills. Plano detalhado por nota + síntese de padrões transversais em `00-Meta/guia/roadmap - ia.md`. Status acima reflete o estado real (não o selo "completo" antigo, que se baseava em contagem bruta de linhas). Próximo passo é **executar** as mudanças propostas, galho a galho — priorizando o que é barato e de alto ganho (E2 abertura-problema, E1 TL;DR, L2 URLs) e a caducidade urgente (Ferramentas de IA, Segurança 11/EU AI Act).
>
> **Padrões transversais (top gaps):** E2 abertura sem cenário · E1 TL;DR raso · E3 diagramas em ASCII (não Mermaid) · L2 refs sem URL · E5 bridge nos galhos antigos · conteúdo real <piso mascarado por linhas em branco · caducidade nas notas de ferramenta/modelo.

---

## 2. Engenharia — o diferencial de Senior

| Trilha                                                                                  | Estado | Nota                                                                                                                           |
| --------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| [[03-Dominios/Engenharia/Design de Software/index\|Design de Software]]                 | 🟡     | 25 notas, 2 galhos (SOLID, OO, Patterns)                                                                                       |
| [[03-Dominios/Engenharia/Segurança/index\|Segurança]]                                   | 🟡     | 23 notas; consolidar                                                                                                           |
| [[03-Dominios/Engenharia/Testes/index\|Testes]]                                         | 🟡     | 17 notas (geral/conceitual) — **falta a vertente "Testes no ecossistema JS"** (Vitest, Jest, Testing Library, Playwright, MSW) |
| [[03-Dominios/Engenharia/Complexidade de Software/index\|Complexidade de Software]]     | 🟡     | 17 notas                                                                                                                       |
| [[03-Dominios/Engenharia/Arquitetura/index\|Arquitetura / System Design]]               | 🟡     | 7 notas — **crítico para entrevista senior; aprofundar**                                                                       |
| [[03-Dominios/Engenharia/Comunicação entre Sistemas/index\|Comunicação entre Sistemas]] | 🟡     | 8 notas (API design, REST/GraphQL/gRPC, mensageria)                                                                            |
| [[03-Dominios/Engenharia/Operação/index\|Operação (DevOps/SRE)]]                        | ⬜      | 1 nota — **CI/CD, deploy, observabilidade, on-call: buraco grande para fullstack**                                             |
| [[03-Dominios/Engenharia/Dados/index\|Dados (Data Engineering)]]                        | ⬜      | 1 nota — modelagem, pipelines, analytics                                                                                       |

---

## 3. Ciência — fundamentos (camada madura)

> Domínio **Fundamentos** essencialmente completo: 11 trilhas atômicas (Algoritmos, Estruturas de Dados, Banco de Dados, Redes e Protocolos, Sistemas Operacionais, Concorrência, Paradigmas, Teoria da Computação, Complexidade, Organização de Computadores, Compiladores, Matemática). Manutenção/enriquecimento conforme necessário, não construção nova.

---

## 4. Carreira — o que fecha a candidatura

| Trilha | Estado | Nota |
| ------ | ------ | ---- |
| [[03-Dominios/Carreira/Entrevistas/index\|Entrevistas]] | 🟡 | 6 notas — falta behavioral (STAR), system design practice, negociação |
| [[03-Dominios/Carreira/Inglês/index\|Inglês]] | 🟡 | 4 notas + mentoria GCA; articulação técnica em inglês |
| [[03-Dominios/Carreira/Empreendedorismo/index\|Empreendedorismo]] | 🟡 | 23 notas, 1 galho |

---

## 5. O que falta para um Fullstack completo — backlog priorizado

> [!todo] Ordem de construção sugerida
> A lógica: fechar primeiro o **tripé frontend** (a maior lacuna do perfil, já que backend Java está maduro), depois subir para **system design / operação** (profundidade de senior), e em paralelo as **reformas** de consolidação.

### Onda A — Tripé Frontend (prioridade máxima)
1. ✅ **JavaScript (core)** — **CONCLUÍDA 2026-06-25** (26 notas, 3 fases): closures, protótipos & `this`, coerção, async no nível da linguagem, iterators/generators, módulos, metaprogramação, ES2026. Base que o índice do TypeScript referencia.
2. ✅ **React** — domínio multi-galho **COMPLETO 2026-06-27**: React core (26) + Design Patterns (12) + Next.js (16, baseline Next 15) + Ecossistema (13, server state/client state/forms/UI/tables/charts). TypeScript com React (15) e Charts já existiam.
3. 🧱→✅ **HTML** — semântica, forms, acessibilidade (ARIA/a11y), SEO, metadados.
4. 🧱→✅ **CSS** — box model, flex/grid, cascade & specificity, responsivo, design tokens.
5. ✅ **Plataforma Web** — **CONCLUÍDA 2026-06-28**: 7 galhos (DOM/Eventos/Rendering/Web APIs/Storage/Workers/Networking), ~54 notas, 3 fases.

### Onda B — Reformas e consolidações
6. ✅ **Reforma do Node** — **CONCLUÍDA 2026-06-29**: 8 galhos, 95 notas reformadas no padrão capítulo (fase/Mermaid/Casos práticos/Armadilhas comuns/O que vem a seguir).
7. 🟡 **Testes no ecossistema JS** — galho/trilha específica (Vitest, Jest, Testing Library, Playwright, MSW), ligando a `Engenharia/Testes` (conceitual) e à nota 19 de Tooling (`node:test`). **← PRÓXIMO**

### Onda C — Profundidade de Senior (system design & operação)
8. 🟡 **Arquitetura / System Design** — escalar de 7 notas para trilha de entrevista (CAP, sharding, caching, filas, consistência, design exercises).
9. ⬜ **Operação (DevOps/SRE)** — CI/CD, containers em produção, observabilidade, deploy strategies, incident response.
10. 🟡 **Comunicação entre Sistemas** — API design (REST/GraphQL/gRPC), versionamento, mensageria, idempotência.

### Onda D — Carreira (em paralelo, contínuo)
11. 🟡 **Entrevistas** — behavioral/STAR, system design practice, coding strategy.
12. 🟡 **Inglês** — articulação técnica (alimentado pela mentoria GCA).

### Coberturas ausentes a considerar (🚫 hoje sem trilha)
- **Cloud** (AWS/GCP) — há `Senda Cloud`, mas sem domínio próprio construído.
- **Auth & Identidade** (OAuth2/OIDC/JWT/sessões) — espalhado em Segurança; merece foco.
- **Web Performance & Core Web Vitals** — tangenciado em Tooling nota 17; falta a ótica de produto.
- **Acessibilidade (a11y)** — entra como fase do HTML, mas é tema de entrevista por si só.

---

## Veja também

- [[04-Sendas/Sendas|Sendas]] — ordens de leitura que consomem estas trilhas
- [[04-Sendas/Senda Frontend|Senda Frontend]] · [[04-Sendas/Senda Entrevistas|Senda Entrevistas]]
- Planos detalhados por trilha/galho: pasta `00-Meta/specs/`
- [[00-Meta/guia/pipeline/Domínios|Pipeline: Domínios]]
