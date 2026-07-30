---
title: "Roadmap de Trilhas"
type: moc
publish: true
created: 2026-06-25
updated: 2026-07-28
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
| [[03-Dominios/Tecnologia/Python/index\|Python]] | ✅ | **COMPLETA 2026-07-12**: 19 galhos, 202 notas, 3 fases (escala Java — Core/OO/Collections/Funcional/Tipagem/Concorrência/Async/Web-APIs/Persistência/Mensageria/Microservices/Observabilidade/Cloud-native/CPython internals/Segurança/Testes/Arquitetura/Build/Certificação PCEP-PCAP) |
| [[03-Dominios/Tecnologia/Go/index\|Go]] | 🟢 | **Trilha completa (2026-07-18):** 21 galhos + capstone, 163 notas em 3 fases, padrão capítulo, lente cross-stack. Fecha o último backend sem trilha (Java 18 · Node 8 · Python 19 · **Go 21**). Falta só enriquecimento de mídia (M1). |

### IA, Terminal, Infra, RPA

| Trilha | Estado | Nota |
| ------ | ------ | ---- |
| [[03-Dominios/Tecnologia/IA/index\|IA]] | 🟡 | 21 galhos; **diagnóstico nota-a-nota COMPLETO (30/06): 237 notas, ~84% no gate ≥9/12, 47 já fechadas** — plano detalhado em `guia/roadmap - ia`; ver [[#Enriquecimento do domínio IA]] |
| [[03-Dominios/Tecnologia/Terminal/index\|Terminal]] | ✅ | 7 galhos, 78 notas |
| [[03-Dominios/Tecnologia/Cloud/index\|Cloud]] | ✅ | **COMPLETA 2026-07-24**: 24 galhos + capstone do domínio, 146 notas, lente dupla AWS↔DigitalOcean. Blocos: modelo mental/fundamentos (1-4) · primitivos (5-10) · serverless (11-15) · operar/governar (16-20: IaC/Observabilidade/Segurança/FinOps/Resiliência) · provedores e maestria (21 AWS a fundo · 22 DigitalOcean a fundo · 23 multi-cloud/portabilidade · 24 Certificação SAA-C03) · capstone "Arquitetar um SaaS na cloud do zero". Galhos 12-24 via workflow de fan-out. **M1 (mídia) ✅ completo 2026-07-25 — 217 vídeos YouTube (legenda verificada) em 144 notas.** Domínio 100% fechado. |
| [[03-Dominios/Tecnologia/Infraestrutura/index\|Infraestrutura]] | 🟡 | só galho Linux; falta Docker, Kubernetes, Nginx (a *prática* já vive na Operação; a *plataforma* na Cloud) |
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
| Claude Code | 71 | em curso | 🟡 construção/enriquecimento ativo | Sub-domínio próprio (Mental Model · Configuração · Hooks e Guardrails · Skills e MCP · Workflows · Time e Automação), com roadmaps por sub-galho. WIP corrente do vault (13/07). |

> **Diagnóstico nota-a-nota CONCLUÍDO (30/06):** todas as 237 notas (19 galhos + 3 soltas) auditadas, uma por vez, contra a régua das skills. Plano detalhado por nota + síntese de padrões transversais em `00-Meta/guia/roadmap - ia.md`. Status acima reflete o estado real (não o selo "completo" antigo, que se baseava em contagem bruta de linhas). Próximo passo é **executar** as mudanças propostas, galho a galho — priorizando o que é barato e de alto ganho (E2 abertura-problema, E1 TL;DR, L2 URLs) e a caducidade urgente (Ferramentas de IA, Segurança 11/EU AI Act).
>
> **Padrões transversais (top gaps):** E2 abertura sem cenário · E1 TL;DR raso · E3 diagramas em ASCII (não Mermaid) · L2 refs sem URL · E5 bridge nos galhos antigos · conteúdo real <piso mascarado por linhas em branco · caducidade nas notas de ferramenta/modelo.

---

## 2. Engenharia — o diferencial de Senior

| Trilha                                                                                  | Estado | Nota                                                                                                                           |
| --------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| [[03-Dominios/Engenharia/Design de Software/index\|Design de Software]]                 | 🟡     | OO ✅ (13) + SOLID ✅ (8). **Design Patterns escalou de "1 galho" para galho-pai [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/roadmap\|Padrões de Projeto]]** (catálogo de consulta p/ sênior/legado, lente cross-linguagem Java/TS/Python/Go, peso no "quando NÃO usar"): 6 famílias, ~90-100 notas, construção sequencial. **Famílias 1 (Clássicos/GoF) 23/23 + 2 (Acesso a Dados) 15/15 + 3 (Integração Empresarial/EIP) 14/14 + 4 (Aplicação Corporativa/PoEAA não-dados) 14/14 COMPLETAS** (2026-07-28 a 30) — 66 notas, 4 de 6 famílias. A família 4 adotou **lente arqueológica** (era × hoje) com seção "A ressurreição" por nota. Monólito `Design Patterns.md` podado. Próxima: família 5 (Arquitetura de Eventos). |
| [[03-Dominios/Engenharia/Segurança/index\|Segurança]]                                   | 🟡     | 23 notas; consolidar                                                                                                           |
| [[03-Dominios/Engenharia/Testes/index\|Testes]]                                         | 🟡     | 17 notas (geral/conceitual) — **falta a vertente "Testes no ecossistema JS"** (Vitest, Jest, Testing Library, Playwright, MSW) |
| [[03-Dominios/Engenharia/Complexidade de Software/index\|Complexidade de Software]]     | 🟡     | 17 notas                                                                                                                       |
| [[03-Dominios/Engenharia/Arquitetura/index\|Arquitetura / System Design]]               | 🟢     | Trilha System Design completa: 4 sub-galhos (Framework/Building blocks/Padrões/Walkthroughs) + capstone, 27 notas (2026-07-07) |
| [[03-Dominios/Engenharia/Comunicação entre Sistemas/index\|Comunicação entre Sistemas]] | 🟢     | Trilha completa: 4 sub-galhos (Panorama/Síncrona/Confiabilidade/Assíncrona) + capstone, 22 notas + 1 (2026-07-09)              |
| [[03-Dominios/Engenharia/Operação/index\|Operação (DevOps/SRE)]]                        | 🟢     | Trilha completa: 4 sub-galhos (Ofício/Entrega-release/Rodar-em-prod/Observar-responder) + capstone, 23 notas (2026-07-08)      |
| [[03-Dominios/Engenharia/Dados/index\|Dados (Data Engineering)]]                        | 🟢     | Trilha completa: 4 sub-galhos (Fundamentos/Modelagem/Pipelines/Qualidade-governança) + capstone, 19 notas (2026-07-13)         |
| [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index\|Arqueologia e Restauração de Software]] | 🟢 | **Ofício central (consultor de legado).** Escrita completa: 28 notas + capstone (código legado → mentalidade → forense → rede de segurança → seams/Mikado/Strangler Fig → dimensão política → firefighting/compliance). Falta só enriquecimento de mídia (M1). |
| [[03-Dominios/Engenharia/UX/index\|UX]] | 🟢 | **Domínio COMPLETO (iniciado 2026-07-28, concluído 2026-07-29).** 8 sub-galhos + capstone, **49 notas**; galho-irmão [[03-Dominios/Tecnologia/Ferramentas de Design/index\|Tecnologia/Ferramentas de Design]] fechado, **9 notas**. **Total: 58 notas.** Cada nota com M1 (mídia verificada) obrigatório — 4 buracos honestos de busca real (notas 06, 16, 31, 43) + 1 pendência reabrível no capstone (busca não realizada, cota de `WebSearch` esgotada). Ver [[03-Dominios/Engenharia/UX/index\|índice]] e o [[03-Dominios/Engenharia/UX/roadmap\|roadmap]]. |

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

### Backlog atual por prioridade (reconciliado 2026-07-13)

> [!important] Fonte de verdade do que falta
> As Ondas A–D abaixo são registro histórico (majoritariamente concluídas). Este bloco em tiers é a **visão forward-looking** do que resta, priorizada pelos objetivos: entrevistas internacionais + ofício de consultor de legado + completude do grimório.

**Tier 1 — construção nova (buracos reais 🚫)**
- ~~**UX** — sem domínio, sem senda, sem tag sistemática antes de 2026-07-28.~~ ✅ **domínio COMPLETO (iniciado 2026-07-28, concluído 2026-07-29)**: [[03-Dominios/Engenharia/UX/index|Engenharia/UX]] (8 sub-galhos + capstone, **49 notas**) + [[03-Dominios/Tecnologia/Ferramentas de Design/index|Tecnologia/Ferramentas de Design]] (galho-irmão volátil, fechado, **9 notas**). **Total: 58 notas.** Fecha o **último buraco de construção nova do Tier 1** (Go ✅ · Cloud ✅ · Acessibilidade ✅ · **UX ✅**). Público-alvo: o fractional engineer full-cycle (cliente ≠ usuário; escala de um). Ordem de execução seguida: SG1 → SG2 → SG4 → SG6 → SG5 → SG3 → SG7 → SG8 → Ferramentas de Design → capstone. M1 (mídia verificada) obrigatório em toda nota, alinhado ao padrão de Acessibilidade — 4 buracos honestos + 1 pendência reabrível no capstone. Ver [[00-Meta/specs/2026-07-28-dominio-ux-design|design do domínio]] e o [[03-Dominios/Engenharia/UX/roadmap|roadmap]].
- ~~**Go** — 3 notas stub~~ ✅ **Trilha completa (2026-07-18):** 21 galhos + capstone, 163 notas. Paridade de stack backend atingida (Java · Node · Python · Go). Fronteira nativa de gRPC em [[03-Dominios/Engenharia/Comunicação entre Sistemas/index\|Comunicação]] (galho 12). Resta só enriquecimento de mídia (M1).
- ~~**Cloud (AWS/GCP)** — sem domínio próprio construído~~ ✅ **COMPLETA 2026-07-24**: `Tecnologia/Cloud`, 24 galhos + capstone, 146 notas, lente dupla AWS↔DigitalOcean. Alto valor para entrevista sênior remota — agora coberto a fundo (Well-Architected, primitivos, serverless, FinOps, SAA-C03). Resta só M1 (mídia).
- ~~**Acessibilidade (a11y)** — tema de entrevista por si só, hoje diluído como fase do HTML~~ ✅ **domínio próprio 100% COMPLETO (escrito + enriquecido) 2026-07-28**: `Tecnologia/Acessibilidade`, 4 sub-galhos + capstone, **21 notas**, progressão *entender → construir → auditar → sustentar*, lente dupla WCAG↔ofício. Terceiro dos quatro buracos de construção nova do Tier 1 (Go ✅ · Cloud ✅ · **a11y ✅** · UX ✅, este último fechado 2026-07-29 — ver acima). Cada nota com vídeo YouTube verificado + inglês + armadilhas. Ver [[03-Dominios/Tecnologia/Acessibilidade/index|índice]].

**Tier 2 — consolidação de 🟡 (conteúdo existe, falta virar trilha atômica em 3 fases)**
- **Design de Software** — OO ✅ + SOLID ✅. **EM CURSO (2026-07-28):** o antigo "galho de Design Patterns" foi promovido a galho-pai **[[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/roadmap|Padrões de Projeto]]** — um **catálogo de consulta** para o sênior (inclusive legado), com lente cross-linguagem (Java/TS/Python/Go) e peso no "quando NÃO usar". **6 famílias** (Clássicos/GoF · Acesso a Dados · Integração Empresarial/EIP · Aplicação Corporativa/PoEAA · Arquitetura de Eventos · Nuvem e Resiliência), ~90-100 notas, construção **sequencial**. Roadmaps montados; **3 de 6 famílias COMPLETAS (52 notas)**: **família 1 Clássicos (GoF) 23/23** (3 fases, lente cross-linguagem); **família 2 Acesso a Dados 15/15** (lente cross-ORM, eixo dorsal Active Record × Data Mapper); **família 3 Integração Empresarial/EIP 14/14 (2026-07-29)** (lente Camel/Spring Integration, fio condutor "smart endpoints, dumb pipes", fronteira cravada com Comunicação entre Sistemas — EIP cataloga padrões nomeados, Comunicação fica com infra). Monólito `Design Patterns.md` **podado** (virou o index do galho-pai, alias `Design Patterns`). Próxima: **família 4 (Aplicação Corporativa/PoEAA não-dados)**. Rosters das 6 famílias no roadmap-pai (anti-drift).
- **Segurança** (23 notas) — consolidar em trilha.
- **Testes conceitual** (17 notas) — vertente JS já feita à parte ([[03-Dominios/Tecnologia/Testes JS/index\|Testes JS]]); falta atomizar o conceitual.
- **Complexidade de Software** (17 notas) — consolidar.
- **Infraestrutura** (só galho Linux) — Docker/K8s/Nginx como *tecnologia* (a *prática* já vive na Operação).

**Tier 3 — Carreira (contínuo, fecha a candidatura)**
- **Entrevistas** (6 notas) — behavioral/STAR, system design practice, negociação. **Maior ROI imediato** para o objetivo de entrevistas internacionais (alimentado pela mentoria GCA).
- **Inglês** (4 notas + GCA) — articulação técnica em inglês.

**Tier 4 — enriquecimento, não tema novo**
- **IA** (351 notas) — diagnóstico nota-a-nota pronto; falta *executar* correções (E2 abertura · E1 TL;DR · L2 URLs · ASCII→Mermaid · caducidade). Ver [[#Enriquecimento do domínio IA]].
- **Enriquecimento de mídia (M1)** dos galhos escritos-mas-não-enriquecidos: Arqueologia, Web Performance, Testes JS, Go. (**Cloud** ✅ M1 completo 2026-07-25 — 217 vídeos em 144 notas. **Acessibilidade** ✅ enriquecimento completo 2026-07-28 — 21 vídeos verificados + inglês + armadilhas.)
- **RPA** (6 notas stub) — nicho, baixa prioridade.

### Onda A — Tripé Frontend (prioridade máxima)
1. ✅ **JavaScript (core)** — **CONCLUÍDA 2026-06-25** (26 notas, 3 fases): closures, protótipos & `this`, coerção, async no nível da linguagem, iterators/generators, módulos, metaprogramação, ES2026. Base que o índice do TypeScript referencia.
2. ✅ **React** — domínio multi-galho **COMPLETO 2026-06-27**: React core (26) + Design Patterns (12) + Next.js (16, baseline Next 15) + Ecossistema (13, server state/client state/forms/UI/tables/charts). TypeScript com React (15) e Charts já existiam.
3. 🧱→✅ **HTML** — semântica, forms, acessibilidade (ARIA/a11y), SEO, metadados. *(A a11y ganhou domínio próprio em 2026-07-27 — ver [[03-Dominios/Tecnologia/Acessibilidade/index|Acessibilidade]]; HTML/07-08 viram porta de entrada.)*
4. 🧱→✅ **CSS** — box model, flex/grid, cascade & specificity, responsivo, design tokens.
5. ✅ **Plataforma Web** — **CONCLUÍDA 2026-06-28**: 7 galhos (DOM/Eventos/Rendering/Web APIs/Storage/Workers/Networking), ~54 notas, 3 fases.

### Onda B — Reformas e consolidações
6. ✅ **Reforma do Node** — **CONCLUÍDA 2026-06-29**: 8 galhos, 95 notas reformadas no padrão capítulo (fase/Mermaid/Casos práticos/Armadilhas comuns/O que vem a seguir).
7. ✅ **Testes no ecossistema JS** — **CONCLUÍDA 2026-07-06** (escrita 18/18): galho [[03-Dominios/Tecnologia/Testes JS/index|Testes JS]] (Vitest, Testing Library, MSW, Playwright, coverage, flaky, CI), 3 fases, instrumentando `Engenharia/Testes` (conceitual). Falta só enriquecimento de mídia (M1).

### Onda C — Profundidade de Senior (system design & operação)
8. 🟢 **Arquitetura / System Design** — ✅ trilha de entrevista sênior completa (2026-07-07): 4 sub-galhos + capstone, 27 notas. Framework (5) · Building blocks (7: escala/caching/SQL-NoSQL/sharding+consistent-hashing/filas/CAP/CDN) · Padrões recorrentes (6: pub-sub/CQRS/ES/rate-limiting/circuit-breaker/gateway) · Walkthroughs (8 Magus: URL shortener/feed/chat/rate-limiter/notification/file-storage/crawler/KV-store) · Capstone (conduzir a entrevista). Monólito `System Design.md` podado → index.md vira o MOC.
9. 🟢 **Operação (DevOps/SRE)** — ✅ trilha completa (2026-07-08): 4 sub-galhos + capstone, 23 notas, em `Engenharia/Operação`. O ofício de operar (4: DevOps/SRE, 12-Factor, ciclo de deploy, confiabilidade) · Entrega e release (6: pipeline/deploy-strategies/progressive-delivery/migrations/GitOps-IaC/secrets) · Rodar em produção (6: containers/contrato-K8s/zero-downtime/escala/rede-borda/resiliência) · Observar e responder (6 Magus: observabilidade/SLO-error-budget/alerting/incident-response/postmortems/debugging-chaos) · Capstone (anatomia de um incidente). Casa canônica; monólitos Infraestrutura (K8s/CI-CD/Observabilidade) ganharam callouts apontando pra cá.
10. 🟢 **Comunicação entre Sistemas** — ✅ trilha completa (2026-07-09): 4 sub-galhos + capstone, 22 notas, em `Engenharia/Comunicação entre Sistemas`. Pesquisa prévia Full Cycle 3.0/4.0. Panorama e decisão (5: contrato/acoplamento, RPC clássico e onde sobrevive, era REST/GraphQL/gRPC, tempo real, emergentes+framework) · Comunicação síncrona (6: REST modelagem/maturidade/HATEOAS, contrato de resposta/RFC9457, paginação/filtros/auth, GraphQL, gRPC, decisão final) · Confiabilidade do contrato (5: idempotência, versionamento, caching HTTP, rate limiting como contrato, webhooks) · Comunicação assíncrona (6: sync vs async, fila vs stream, garantias de entrega, Outbox/Saga, legado enterprise, CloudEvents/AsyncAPI) · Capstone (desenhando a comunicação de um e-commerce do zero). `API Design.md` virou tronco podado; `Mensageria/*.md` ganharam callouts apontando pra cá.
11. 🟢 **Auth e Identidade** — ✅ trilha completa (2026-07-11): 5 sub-galhos + capstone, 25 notas, em `Engenharia/Auth e Identidade`. Baseline OAuth 2.1 draft-15 · Keycloak 26.x. Fundamentos de identidade (5 Iniciado: mapa AuthN/AuthZ, sessões/cookies, JWT, senhas/MFA, passkeys/WebAuthn) · OAuth 2.1 e OIDC (6 Adepto: delegação, Authorization Code+PKCE, OIDC, grants de máquina, tokens em produção/BFF, SSO/SAML/SCIM) · Autorização e multi-tenancy (4: RBAC/ABAC/ReBAC, Zanzibar/OpenFGA/policy-as-code, multi-tenancy/orgs, autorização de API) · Auth nos stacks (6 Magus: Spring[ponte], Django, FastAPI, Express[ponte], NestJS, Go/Gin) · Keycloak (3: realms/clients/flows, produção/Organizations/HA, integração com os stacks) · Capstone (desenhando a identidade de um SaaS B2B do zero). Segurança 12/13 e Comunicação SG2-03 ganharam callouts apontando pra cá; pontes não reexplicam Java/Segurança (18) nem Node/Segurança.

### Onda D — Carreira (em paralelo, contínuo)
12. 🟡 **Entrevistas** — behavioral/STAR, system design practice, coding strategy.
13. 🟡 **Inglês** — articulação técnica (alimentado pela mentoria GCA).

### Coberturas ausentes a considerar (🚫 hoje sem trilha)
- ~~**Cloud** (AWS/GCP) — há `Senda Cloud`, mas sem domínio próprio construído.~~ → **domínio próprio COMPLETO em 2026-07-24** (✅): `Tecnologia/Cloud`, 24 galhos + capstone, 146 notas, lente dupla AWS↔DigitalOcean. Ver a tabela IA/Terminal/Infra/Cloud acima e o Tier 1.
- ~~**Auth & Identidade** (OAuth2/OIDC/JWT/sessões) — espalhado em Segurança; merece foco.~~ → **trilha própria COMPLETA em 2026-07-11** (🟢): `Engenharia/Auth e Identidade`, 5 sub-galhos + capstone, 25 notas. Ver item 11 da Onda C.
- ~~**Python** — só stubs rasos~~ → **COMPLETA em 2026-07-12** (✅): 19 galhos, 202 notas, 3 fases (escala Java). Ver Backend/Runtime acima.
- ~~**Go** — segue stub em `Tecnologia/Go/`~~ → **COMPLETA em 2026-07-18** (🟢): 21 galhos + capstone, 163 notas, 3 fases (escala Java/Python). Stubs `Go.md`/`Go Backend.md` excluídos. Fecha o último backend sem trilha. Ver Backend/Runtime (Tier 1) acima.
- ~~**Web Performance & Core Web Vitals**~~ → **domínio próprio iniciado em 2026-07-05** (🟡): `Tecnologia/Web Performance/`, 4 galhos (*medir → carregar → responder → sustentar*). **escrita COMPLETA — 4 galhos, 32/32 notas** (Medição & CWV · Carregamento · Runtime & Rendering · Produção), 3 fases, padrão capítulo (falta só a rodada de enriquecimento de mídia, M1). Ver [[03-Dominios/Tecnologia/Web Performance/index|índice do domínio]] e o [[03-Dominios/Tecnologia/Web Performance/roadmap|roadmap]].
- ~~**Acessibilidade (a11y)** — entra como fase do HTML, mas é tema de entrevista por si só.~~ → **domínio próprio, escrita COMPLETA em 2026-07-27** (🟢): `Tecnologia/Acessibilidade`, 4 sub-galhos (Fundamentos/Construir/Auditar/Sustentar) + capstone, 21 notas, 3 fases. Último buraco de construção nova do Tier 1 fechado. Resta só M1 (mídia). Ver o Tier 1 acima.

---

## Veja também

- [[04-Sendas/Sendas|Sendas]] — ordens de leitura que consomem estas trilhas
- [[04-Sendas/Senda Frontend|Senda Frontend]] · [[04-Sendas/Senda Entrevistas|Senda Entrevistas]]
- Planos detalhados por trilha/galho: pasta `00-Meta/specs/`
- [[00-Meta/guia/pipeline/Domínios|Pipeline: Domínios]]
