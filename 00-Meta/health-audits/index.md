---
title: "Health Audits"
type: moc
publish: false
created: 2026-06-03
updated: 2026-06-03
status: seedling
tags:
  - moc
  - health-audit
aliases:
  - Health Audits
---
# Health Audits

> [!abstract] TL;DR
> Auditorias de saúde do vault geradas pelo script `00-Meta/scripts/health-audit.py` (auto, sexta). Verificam estrutura canônica, skill drift, links pendentes, notas órfãs, frontmatter ausente e glosas estagnadas.

Esta pasta arquiva os relatórios do health-audit — auditoria estrutural complementar à `/revisao-semanal` (que cuida de conteúdo e trajetória). Cada relatório é gerado por `python3 00-Meta/scripts/health-audit.py` e gravado como `<YYYY-MM-DD>.md`. Notas privadas (`publish: false`) — não vão pro site público.

## Conteúdo

Relatórios datados gerados dinamicamente pelo script. Não listados aqui.

## Veja também

- [[00-Meta/revisoes/index|Revisões Semanais]] — revisão de conteúdo & trajetória
- [[skills]] — catálogo de skills do vault
