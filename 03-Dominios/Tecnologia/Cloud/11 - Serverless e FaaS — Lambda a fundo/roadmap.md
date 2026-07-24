---
title: "Roadmap — Serverless e FaaS (Lambda a fundo)"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Serverless e FaaS (galho 11)

Roadmap-folha do galho `Cloud/11 - Serverless e FaaS — Lambda a fundo`. Bloco 3 (Serverless e arquiteturas modernas) — **galho que abre o bloco**. Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - O que é serverless, de verdade
- **Estado:** ✅ feita · fase: Iniciado · 243 linhas
- **Escopo:** modelo mental sem o mal-entendido do nome (server-invisible-to-you, não server-does-not-exist), os 4 elementos (sem provisionar/patch/escalar, execução sob demanda, pay-per-use real, escala auto do zero), FaaS vs serverless amplo (BaaS, bancos serverless, containers serverless), espectro de compute (bare metal→VM→VM elástica→container→função) com tabela de responsabilidade, VM-vs-Lambda em código, ciclo de vida (cold/warm), o que serverless NÃO resolve; AWS Lambda (Firecracker, 2014) ↔ DO Functions (Nimbella+OpenWhisk, 2022).

#### 02 - Anatomia de uma função Lambda
- **Estado:** ✅ feita · fase: Adepto · 415 linhas · mecânica (19 blocos de código)
- **Escopo:** handler (assinatura event/context, Python/Node), objetos event e context, runtimes gerenciados + custom runtime API, deployment package (zip 50MB direct/250MB unzipped vs imagem 10GB) + layers, execution role IAM (trust policy lambda, least privilege — fronteira galho 4), limites (timeout default 3s/máx 900s, memória 128-10240MB com CPU proporcional, /tmp 512MB-10GB efêmero, payload 6MB sync/**1MB async**); Lambda ↔ DO Functions (handler main, memória 128MB-1GB padrão 256MB).

#### 03 - O modelo de eventos: triggers e integrações
- **Estado:** ✅ feita · fase: Adepto · 370 linhas
- **Escopo:** serverless é reativo — os 3 modelos de invocação (síncrono request-response/API GW; assíncrono event/S3-SNS-EventBridge, 202 + retry 2x + DLQ; poll-based/event source mapping para SQS/Kinesis/DynamoDB Streams/Kafka), event sources um a um (o que cada um manda no event), event source mapping (batch size/window, ParallelizationFactor 1-10, partial batch response ReportBatchItemFailures), tratamento de erro por modelo (poison message trava shard até 1 dia), DLQ vs on-failure destination; DO só web + scheduled trigger (cron, private preview, 3/conta). Fronteira→Comunicação (conceito de fila) e galho 13 (mensageria a fundo).

#### 04 - Cold start, concurrency e performance
- **Estado:** ✅ feita · fase: Adepto · 386 linhas · nota central
- **Escopo:** ciclo de vida do execution environment (Init 10s/Invoke/Shutdown 0-2000ms), cold vs warm start (<1% das invocações, <100ms->1s), reuso de ambiente quente (conexão DB/SDK fora do handler = otimização), modelo de escala (1 ambiente = 1 request; burst 1000 ambientes/10s por função; account limit 1000/região default, 900 unreserved), reserved concurrency (garante+limita) vs provisioned concurrency (pré-aquece, mata cold start, custa), memória↔CPU (1769MB≈1vCPU, Power Tuning), throttling (429 sync/retry async); DO 120 concorrentes/namespace, sem provisioned concurrency.

#### 05 - Pricing, limites e operação
- **Estado:** ✅ feita · fase: Adepto · 373 linhas
- **Escopo:** modelo de custo (requisições + GB-segundos = memória×tempo arredondado 1ms), fórmula com exemplo trabalhado, free tier (1M req + 400k GB-s), a matemática do pay-per-use (barato em rajada, explode em carga alta constante), ponto de virada Lambda vs EC2 reservada (~5-6M req/mês no perfil ilustrativo), impacto da memória no custo (ARM/Graviton mais barato ~19-20%), custos escondidos (provisioned concurrency, data transfer, CloudWatch logs), versionamento ($LATEST vs versões imutáveis), aliases (prod/staging, weighted alias canary), deploy/rollback; GB-s ↔ GiB-s DO (free 90k, US$0,0000185/GiB-s). Honestidade: pricing AWS renderiza via JS (tabela x86/arm não extraída, tratada como conhecimento estável + [!info]).

#### 06 - Quando serverless faz (e não faz) sentido
- **Estado:** ✅ feita · fase: Magus · 381 linhas · **FECHA o galho**
- **Escopo:** árvore de decisão serverless vs container gerenciado vs VM (eixos: padrão de carga rajada/constante, duração <>15min, cold start tolerável, estado stateless/stateful, controle de hardware), matriz de limiares numéricos ancorada nas notas anteriores, a decisão não é permanente (produto cresce → cálculo vira), casos onde FaaS brilha (glue code, API tráfego variável, processamento de evento, cron, fan-out, MVP) vs anti-padrões (long-running >15min, latência crítica constante, throughput alto constante, estado pesado, controle de hardware, lift-and-shift), lock-in (event model/IAM/ferramental, Serverless Framework/SST de raspão), ponte pro Bloco 3 (galhos 12-15); DO pende pra container/App Platform mais cedo. Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Escrito em 2 ondas de 3 agentes (01-03, depois 04-06); orquestrador commitou serialmente (`d54292f`, `2e6ee4d`, `<fecho>`). 0 wikilinks quebrados no gate.
- **Achado factual relevante:** payload assíncrono do Lambda hoje é **1 MB** na doc oficial (não os 256 KB que circulam em fontes antigas) — capturado e marcado [!info] na nota 02. Nenhuma nota carregou o valor obsoleto (grep "256" confirmou só usos legítimos: memória padrão DO e o próprio callout de correção).
- **Contraste mecânica-vs-critério reconfirmado:** nota de mecânica pura (02: 415, 19 blocos) fecha alto; notas de performance/custo/síntese (04: 386, 05: 373) na banda com densidade real; nota de abertura/mapa (01: 243) topou abaixo do piso de Iniciado SEM padding — cobre o escopo (espectro, VM-vs-Lambda, responsabilidade, o-que-não-é). Aceito; piso é alvo, não gate.
- Capstone (06) fechou 381 (<banda 400-460 dos capstones anteriores) mas denso: ~6350 palavras, comparável ao capstone do galho 9 (~6285); menos quebras de linha por ser síntese em prosa. 4 Mermaid incl. a árvore de decisão central. Aceito como síntese, não inflado.
- Honestidade de paridade DO capturada: DO Functions é OpenWhisk-based, escopo enxuto — só web/scheduled trigger (nota 03), 120 concorrentes/namespace sem provisioned concurrency (nota 04), memória máx 1GB (nota 02), ecossistema menor; a árvore de decisão pende pra container/App Platform mais cedo na DO (nota 06).
- Pricing AWS renderiza via JS (mesma armadilha do galho 8/S3) — WebFetch não extraiu a tabela x86/arm; tratado com valores conhecidos + [!info] pra conferir na calculadora.
- Fronteiras: conceito de fila/event-driven → Comunicação; mensageria gerenciada a fundo → galho 13; IaC → galho 16; observabilidade → galho 17; FinOps → galho 19 (todos prosa, galhos não existem).
