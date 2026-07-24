---
title: "Roadmap — Mensageria e eventos gerenciados"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Mensageria e eventos gerenciados (galho 13)

Roadmap-folha do galho `Cloud/13 - Mensageria e eventos gerenciados`. Bloco 3 (Serverless e arquiteturas modernas). Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - Por que mensageria na nuvem
- **Estado:** ✅ feita · fase: Iniciado · 168 linhas
- **Escopo:** o problema do acoplamento síncrono (Checkout→E-mail direto: falha periférica vira indisponibilidade central), a alternativa assíncrona e o que ela compra (desacoplamento no tempo, buffer/absorção de pico, resiliência a falha parcial — ao preço de consistência eventual), os três sabores conceituais com diagramas Mermaid (fila = 1 produtor/N workers/1 vence; tópico/pub-sub = fan-out, todo assinante recebe; event bus = roteamento por conteúdo), o que "gerenciado" tira do prato (sem VM, sem patch, sem cluster — troca por liberdade de configuração fina), tabela de tradução Azure/GCP; AWS tem SQS+SNS+EventBridge+Amazon MQ, DigitalOcean só tem Managed Kafka (nenhuma paridade de fila/pub-sub/event-bus dedicado).

#### 02 - SQS a fundo
- **Estado:** ✅ feita · fase: Adepto · 321 linhas · mecânica (11 blocos de código/CLI)
- **Escopo:** anatomia do ciclo SendMessage/ReceiveMessage/DeleteMessage com receipt handle, visibility timeout (padrão 30s, 0-12h) como mecanismo central e a regra prática (timeout > tempo de processamento, com folga), long polling (WaitTimeSeconds 1-20) vs short polling, Standard (throughput quase ilimitado, best-effort) vs FIFO (`MessageGroupId`, 300 msg/s sem batching / 3.000 com batching por partição, dedupe 5min) com caso prático de escolha, dead-letter queue (`maxReceiveCount`, redrive policy, `StartMessageMoveTask`), retenção (padrão 4 dias, máx 14 dias)/delay queues (até 15min)/tamanho de mensagem (1 MiB padrão, 2GB via Extended Client), batching (até 10 msgs/chamada), idempotência como responsabilidade do consumidor (esqueleto Python/boto3), integração com Lambda via event source mapping; DO sem equivalente — Managed Kafka é modelo fundamentalmente diferente (log append-only vs fila com visibility timeout).

#### 03 - SNS e pub-sub
- **Estado:** ✅ feita · fase: Adepto · 248 linhas
- **Escopo:** tópico gerenciado como ponto de fan-out (push, não pull — diferença estrutural com SQS), tipos de assinatura (SQS, Lambda, HTTP/S, email, SMS, push, Firehose, terceiros), Standard vs FIFO topic (FIFO só integra com SQS FIFO, não entrega ordenado direto pra Lambda/HTTP), o padrão canônico SNS→múltiplas SQS ("fanout to SQS queues for asynchronous processing") e por que a fila dá durabilidade, message filtering via filter policy (JSON por atributo ou por corpo da mensagem), message attributes/raw message delivery/DLQ por assinatura (retry até 100.015 tentativas em 23 dias pra endpoints AWS-managed), caso A2P (CloudWatch Alarm → email+SMS+SQS), tabela SNS vs SQS (push/pull, fan-out/fila-de-trabalho), código CLI completo (criar tópico, assinar, publicar, filtrar, fan-out); DO sem equivalente nativo — Managed Kafka ou chamar Functions direto (perde o desacoplamento).

#### 04 - EventBridge e o event bus
- **Estado:** ✅ feita · fase: Adepto · 259 linhas
- **Escopo:** roteador de eventos por conteúdo (event pattern casa o JSON inteiro, não só atributos anexados como SNS), os três tipos de bus (default/custom/partner), regra = event pattern + até 5 targets (limite soft, 2.048 bytes de pattern, evento máx 256KB), operadores de pattern (numeric/prefix/exists/anything-but/$or), input transformer (InputPathsMap+InputTemplate) pra desacoplar formato do consumidor, `PutEvents` (até 10 eventos/chamada), EventBridge Scheduler (cron gerenciado, até 1M schedules/conta, sintaxe rate()/cron()), partner event sources (Datadog/Zendesk/PagerDuty/Shopify/Auth0), schema registry/discovery, EventBridge Pipes (ponto-a-ponto com filtro+enrichment), archive+replay; tabela comparativa SNS vs EventBridge (filtro raso por atributo vs regra sobre corpo inteiro; fan-out em massa vs até 5 targets; sem cron/SaaS/replay vs nativo); DO só tem scheduled triggers (private preview, 3/conta) — sem bus, sem roteamento condicional, sem archive/replay.

#### 05 - Padrões event-driven na cloud
- **Estado:** ✅ feita · fase: Adepto · 290 linhas · nota-síntese (amarra as 3 anteriores)
- **Escopo:** história de abertura (fan-out direto SNS→3 Lambdas, um consumidor lento contamina o sistema e esconde a falha) motivando os 5 padrões: fan-out durável (SNS→SQS, não SNS→Lambda direto — a régua: fila é default quando consumidor pode ficar lento/indisponível/processar em lote), idempotência via escrita condicional DynamoDB (`ConditionExpression`, código Python, armadilha de gravar a chave depois do efeito em vez de antes), ordenação seletiva (standard vs FIFO na AWS, custo real em throughput, EventBridge sem garantia de ordem alguma), outbox na cloud (quem faz o papel do relay — Lambda agendado via EventBridge Scheduler, AWS DMS via CDC/WAL, EventBridge Pipes), DLQ strategy (poison message, `maxReceiveCount`, CloudWatch Alarm obrigatório, redrive só após confirmar causa raiz — com caso prático de redrive irrefletido repetindo o erro), retry/backoff via visibility timeout, choreography (EventBridge/SNS→SQS) vs orchestration (Step Functions, prévia do próximo galho); casos práticos (fintech com vazamento de fraude por semanas; redrive sem investigar causa raiz), seção "Em entrevista", bloco EN; DO sem equivalente nativo a nenhuma das peças de apoio (DynamoDB/CloudWatch/DMS/Step Functions) — tabela de 5 padrões x AWS x DO.

#### 06 - Escolher o serviço de mensageria (capstone)
- **Estado:** ✅ feita · fase: Magus · 180 linhas · **FECHA o galho**
- **Escopo:** a pergunta-eixo (distribuir trabalho vs publicar um fato) e a árvore de decisão de 4 perguntas (trabalho→SQS Standard/FIFO; N assinantes→SNS/SNS→SQS; roteamento por conteúdo/SaaS/cron→EventBridge; stream ordenado replayável→Kinesis/MSK; senão→API síncrona), a distinção-chave fila (serviço é dono do cursor) vs stream (você é dono do cursor, retenção 24h-365d Kinesis), Kinesis (shard-based, nativo, sem broker) vs MSK (Kafka de verdade, KRaft, Provisioned/Serverless — escolha é portabilidade/ecossistema, não performance), tabela comparativa completa dos 6 serviços (modelo/ordering/retenção/escala/caso de uso/custo), diagrama de arquitetura real compondo EventBridge+SNS+SQS+Kinesis num e-commerce, anti-padrões (fila pra request-response síncrono, EventBridge pra streaming, ignorar idempotência), ponte pro próximo galho (API Gateway, orquestração Step Functions); DO honesta — só Managed Kafka cobre a fatia de streaming, nada cobre fila/pub-sub/event-bus leve. Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Notas 01-06 já existiam no repositório ao gerar este roadmap (galho escrito previamente); este roadmap foi criado retroativamente lendo as 6 notas na íntegra para extrair fase, linhas e escopo fiel.
- Todos os wikilinks internos verificados por `ls` antes de gravar: `Cloud/index.md`, `Cloud/11 .../03 - O modelo de eventos...md`, `Comunicação entre Sistemas/index.md` — todos existentes.
- Fronteiras confirmadas nas próprias notas: conceito de mensageria/idempotência/ordenação/outbox/saga → Comunicação entre Sistemas (trilha-mãe, citada em quase toda nota); os mesmos 3 serviços como *fonte de evento* do Lambda → galho 11 nota 03 (linkado em 01, 02 e 04); orquestração explícita (Step Functions) e API Gateway → próximo(s) galho(s) da trilha Cloud (mencionados em prosa nas notas 05 e 06, galhos ainda não existem nesta árvore).
- Lente dupla AWS↔DigitalOcean é a mais assimétrica encontrada na trilha até aqui: a DO não tem equivalente nativo a SQS, SNS ou EventBridge — só Managed Kafka (tratado como banco gerenciado, não como produto de mensageria) e Functions scheduled triggers (private preview, 3/conta). Todas as 6 notas nomeiam essa lacuna explicitamente em vez de forçar paridade.
- Achados factuais capturados com [!info] "Verificado 2026-07-24": SQS payload 1 MiB (não 256 KB, valor obsoleto que ainda circula), SQS FIFO throughput 300/3.000 msg/s por partição, SNS retry ~100.015 tentativas em 23 dias pra endpoints AWS-managed, EventBridge 5 targets/rule e evento máx 256KB, Kinesis retenção 24h-365d e limites de shard, MSK usa KRaft (não ZooKeeper).
