---
title: "Roadmap — Observabilidade na cloud"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Observabilidade na cloud (galho 17)

Roadmap-folha do galho `Cloud/17 - Observabilidade na cloud`. Bloco 4. Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 6 |
| ⬜ pendente | 0 |
| ✅ feita | 6 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |
| M1 (mídia) | pendente — enriquecimento futuro |

---

## Notas

#### 01 - Por que observabilidade na cloud
- **Estado:** ✅ feita · fase: Iniciado · 152 linhas
- **Escopo:** o sistema distribuído opaco (o pedido que sumiu entre seis peças gerenciadas da arquitetura serverless do galho 15), monitoramento (perguntas que você já sabia fazer) vs. observabilidade (perguntas que você não previu), os três pilares (logs = eventos discretos, métricas = pulso ao longo do tempo, traces = caminho de um request), o desafio específico da nuvem, o panorama de ferramentas, tabela de tradução entre provedores, armadilhas, honestidade sobre o que falta; AWS CloudWatch+X-Ray ↔ DO Monitoring (sem tracing).

#### 02 - CloudWatch a fundo
- **Estado:** ✅ feita · fase: Adepto · 335 linhas
- **Escopo:** três serviços debaixo de um nome (Logs+Metrics+Alarms), log groups/streams e retenção, log virando stream em tempo real, JSON estruturado em vez de texto solto, consultando logs como dado (Logs Insights), métricas (namespace/dimensions/resolução), standard 1min vs. high-resolution 1seg, degradação da retenção (dado velho vira agregado, não some), Embedded Metric Format (métrica de graça dentro do log), statistics e metric math, alarmes (do threshold à ação), dashboards/metric filters/Contributor Insights, a armadilha do custo (cada peça cobrada separadamente); CloudWatch vs. DigitalOcean Monitoring, nota lateral Azure/GCP, circuito mínimo ponta a ponta.

#### 03 - Tracing distribuído
- **Estado:** ✅ feita · fase: Adepto · 256 linhas
- **Escopo:** o pedido que sumiu entre três serviços (retomando o capstone do galho 15), o que só o tracing responde, um ID que atravessa tudo, o header por baixo do capô, o serviço gerenciado X-Ray (segments/subsegments), por que nem todo pedido vira trace (sampling), como o trace nasce, debugando o pedido sumido com o service map, o padrão que não amarra em ninguém (OpenTelemetry), armadilhas; X-Ray vs. DigitalOcean (sem equivalente — Jaeger/Tempo próprio ou SaaS terceiro), nota lateral Azure/GCP.

#### 04 - Alarmes, SLO e resposta
- **Estado:** ✅ feita · fase: Adepto · 332 linhas
- **Escopo:** dado sem ação é decoração, o instinto de "alarmar em tudo" e o alert fatigue, o filtro de todo alarme bom (sintoma que o usuário sente, não causa interna), por que uma janela só engana, combinar sinais pra reduzir ruído (composite alarms AND/OR), detecção de anomalia como alternativa ao threshold fixo, do alarme até a pessoa/script (SNS → e-mail/Slack/PagerDuty/Lambda de auto-remediação), os sinais que importam, SLO/SLI/error budget de raspão, onde a cloud para (fronteira→Operação); lente AWS↔DigitalOcean (monitoring mais simples, sem composite alarms), nota lateral Azure/GCP.

#### 05 - Observabilidade de serverless e o específico do provedor
- **Estado:** ✅ feita · fase: Adepto · 243 linhas
- **Escopo:** observar uma caixa que só existe por 100ms (sem host, sem ssh), o que a AWS dá de graça em Lambda, logs START/END/REPORT, quando REPORT não basta, X-Ray e o preço do lock-in, nativo cômodo vs. OTel neutro, a armadilha de logar demais em escala, casos práticos (filtrando cold starts direto do CloudWatch; Logs Insights pra achar a REPORT mais lenta), monitoring básico sem X-Ray na DO, tabela de nomes pra tradução mental; conveniência do CloudWatch/X-Ray automático como armadilha de lock-in é o fio central da nota.

#### 06 - Operar a observabilidade (capstone)
- **Estado:** ✅ feita · fase: Magus · 311 linhas · **FECHA o galho**
- **Escopo:** um sistema que você não pode abrir (retomando a arquitetura de referência do galho 15: API Gateway→Lambda→DynamoDB→SNS→2×SQS), a arquitetura instrumentada peça por peça (o que logar/medir/tracear em cada uma), a estratégia dos três pilares numa arquitetura real, rastreando o pedido perdido ponta a ponta com trace_id costurando tudo (o exercício do pager às 3 da manhã), o custo de operar observabilidade, nativo/OpenTelemetry/SaaS como escolha final, a lente dupla honesta até o fim (AWS vs. DigitalOcean); ponte→galho 18.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Notas escritas fora deste fechamento (roadmap gerado a posteriori, a partir do conteúdo já existente em disco); nenhuma nota foi lida/alterada por esta rodada, só auditada (frontmatter, headings, contagem de linhas).
- Contagem de linhas via `wc -l`: 152/335/256/332/243/311 — banda consistente com galhos anteriores da trilha (Iniciado mais enxuto, capstone denso mas não inflado).
- Todas as 6 notas com `status: seedling`, `publish: true`, `fase` coerente com a posição na sequência (Iniciado→Adepto×4→Magus).
- Wikilinks de fronteira verificados por `ls`: `15 - Arquiteturas serverless e event-driven/index.md` existe; `03-Dominios/Engenharia/Operação/index.md` existe; `03-Dominios/Tecnologia/Cloud/index.md` existe. Nenhum wikilink pra nota inexistente.
- Fronteiras confirmadas no próprio corpo das notas: SLO/error budget/resposta a incidente → Operação (nota 04 já linka); FinOps/custo a fundo → galho 19 (ainda não existe, tratado em prosa); arquitetura instrumentada = a do galho 15 (notas 01, 03 e 06 retomam explicitamente o pedido "sumido").
