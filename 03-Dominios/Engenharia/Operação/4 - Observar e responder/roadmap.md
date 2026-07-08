---
title: "Roadmap — Observar e responder"
created: 2026-07-08
type: meta
publish: false
tags:
  - meta
  - roadmap
  - operacao
---

# Roadmap — Observar e responder (sub-galho 4)

Roadmap-folha do sub-galho `Operação/4 - Observar e responder`. Fase **Magus** (o coração da trilha; alvo ~480-560 linhas / 6-7k palavras). Spec: [[00-Meta/specs/2026-07-08-operacao-devops-trilha-design]]. EXEMPLAR: [[1 - O ofício de operar/01 - O que é operar um sistema]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 6 |
| ⬜ pendente | 0 |
| ✅ feita | 6 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - Observabilidade como prática   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Magus
- **Escopo:** não "o que é log/métrica" — como instrumentar pra responder perguntas não-antecipadas; 3 pilares aplicados, cardinalidade, structured logging, correlação, monitoring vs observability, known-unknowns vs unknown-unknowns.
- **Fronteira:** reforço de [[Observabilidade]] (ferramenta) sob ótica de prática.
- **Fontes:** Charity Majors/Honeycomb; Google SRE (Monitoring); OpenTelemetry.
- **Resultado:** 282 linhas / 5645 palavras; 4 Mermaid (3 pilares + trace_id, wide-events), 3 [!warning], 5 [!question]-. Monitoring vs observability, cardinalidade, OTel. Verificado: links e URLs ok.

#### 02 - SLI, SLO e error budgets   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Magus
- **Escopo:** escolher SLI, definir SLO, error budget como orçamento de risco e contrato dev↔ops, burn rate, error budget policy (congelar deploys).
- **Fronteira:** **casa canônica** — [[Observabilidade]] aponta pra cá. Introduzido no SG1-04.
- **Fontes:** Google SRE Book + Workbook (SLOs, Implementing SLOs); artigos de SLO.
- **Resultado:** 327 linhas / 5852 palavras; 4 Mermaid (inc. burn do budget), 3 [!warning], 4 [!question]-. Casa canônica; cálculo numérico + error budget policy. Verificado: links e URLs ok.

#### 03 - Alerting que não gera fadiga   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Magus
- **Escopo:** alertar em sintoma não causa, RED/USE, page vs ticket, alert fatigue, symptom-based alerting, runbooks acionáveis, SLO burn-rate alerts.
- **Fronteira:** linka 01 e 02.
- **Fontes:** Google SRE (Alerting on SLOs, monitoring philosophy); Rob Ewaschuk "My Philosophy on Alerting".
- **Resultado:** 305 linhas / 6617 palavras; 2 Mermaid (causa vs sintoma, multi-burn-rate), 3 [!warning], 5 [!question]-. Verificado: links e URLs ok.

#### 04 - Incident response e on-call   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Magus · **cola SRE central (novo no vault)**
- **Escopo:** o processo ao vivo — papéis (Incident Commander), severidades, comunicação, mitigar antes de root cause, on-call saudável (rotação, compensação, handoff).
- **Fronteira:** novo; linka postmortem (05).
- **Fontes:** Google SRE (Managing Incidents, Being On-Call); PagerDuty Incident Response; Atlassian.
- **Resultado:** 298 linhas / 6587 palavras; 4 Mermaid (fluxo, ICS, papéis, comms), 4 [!warning], 4 [!question]-. Cola SRE nova. Verificado: links e URLs ok.

#### 05 - Postmortems e cultura blameless   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Magus
- **Escopo:** timeline, contributing factors, action items, blameless (por que culpar piora a confiabilidade), o postmortem como aprendizado organizacional, near-miss.
- **Fronteira:** linka 04.
- **Fontes:** Google SRE (Postmortem Culture); Etsy/Morgue; John Allspaw (blameless postmortems).
- **Resultado:** 244 linhas / 6348 palavras; 2 Mermaid, 3 [!warning], 3 [!question]-. Just culture (Dekker), LFI, near-miss. Verificado: links e URLs ok.

#### 06 - Debugging de produção e chaos engineering   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Magus · **FECHA o sub-galho**
- **Escopo:** investigar sob pressão com observabilidade (o arquétipo troubleshoot); chaos engineering como investir em confiança antes do incidente; game days.
- **Fronteira:** **reforço** do arquétipo troubleshoot de [[01 - O que é System Design e o que a entrevista avalia]]; linka resiliência (SG3-06).
- **Fontes:** Principles of Chaos Engineering; Netflix Chaos Monkey/Simian Army; Google SRE (Testing for Reliability); Gremlin.
- **Resultado:** 238 linhas / 5807 palavras; 2 Mermaid (funil investigação, loop chaos), 3 [!warning], 4 [!question]-. FECHA a escrita. Verificado: links e URLs ok.
