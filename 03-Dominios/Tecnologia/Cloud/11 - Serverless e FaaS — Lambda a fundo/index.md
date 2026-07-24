---
title: "Cloud — Serverless e FaaS (Lambda a fundo)"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - serverless
  - lambda
  - faas
aliases:
  - "Serverless e FaaS"
  - "Galho 11 - Serverless e FaaS"
---

# Serverless e FaaS — Lambda a fundo

> [!abstract] TL;DR
> Galho 11 da trilha Cloud, e o que **abre o Bloco 3 (Serverless e arquiteturas modernas)**. O Bloco 2 assumiu, do início ao fim, que *você* provisiona e opera os primitivos — a VM, o load balancer, o banco. Este galho quebra essa premissa: e se você não gerenciasse nem o servidor? O galho sobe de baixo pra cima com o AWS Lambda como estudo de caso: primeiro o **modelo mental** (o que "sem servidor" realmente significa, e o que não significa), depois a **anatomia** de uma função (handler, event/context, runtime, limites, execution role), depois o **modelo de eventos** que a alimenta (síncrono, assíncrono, poll-based; os event sources), depois a **performance e escala** (cold start, concurrency, provisioned concurrency, memória↔CPU), depois o **custo e a operação** (GB-segundo, o ponto de virada vs VM, versionamento e aliases), e fecha com a **árvore de decisão** honesta: dado um problema real, serverless faz (ou não faz) sentido? 6 notas, 3 fases, lente dupla AWS Lambda ↔ DigitalOcean Functions.

## Sobre este galho

Serverless é o modelo operacional que empurra a linha da responsabilidade compartilhada o mais longe possível para o lado do provedor: você entrega só o código de uma função, e o provedor decide onde, quando e em que máquina ela roda — nascendo e morrendo por invocação, sem capacidade reservada, sem custo por ociosidade. Este galho não vende serverless como bala de prata; ensina a mecânica a fundo *e* separa com honestidade onde FaaS brilha do que ele só finge resolver.

O fio condutor sobe do modelo à decisão. Primeiro o *porquê e o quê* — o modelo mental, o espectro de compute (VM → container → função), o que serverless não é (não é grátis, não elimina cold start, não serve pra tudo). Depois a *mecânica* em três notas: a anatomia da função (handler, event, context, deployment package, layers, execution role, limites), o modelo de eventos (os três modos de invocação e os event sources que disparam uma Lambda), e a performance (o ciclo de vida do ambiente de execução, cold vs warm start, o modelo de escala, reserved vs provisioned concurrency, o acoplamento memória↔CPU). Depois o *custo e a operação* — a fórmula GB-segundo, o ponto de virada onde uma VM reservada volta a vencer, versionamento e aliases para deploy seguro. E por fim a *decisão* — a árvore serverless vs container vs VM, os casos onde brilha e os anti-padrões, o lock-in, e a ponte para o resto do Bloco 3.

**Audiência primária:** quem sabe que Lambda existe mas nunca decidiu, com intenção, entre serverless e um container/VM, nem entende por que a primeira requisição é lenta ou por que a fatura às vezes explode. **Audiência secundária:** quem já usa Lambda mas nunca formalizou o modelo de escala (1 request = 1 ambiente), a diferença reserved vs provisioned concurrency, ou o ponto de virada de custo contra capacidade reservada.

> [!info] Fronteira
> O **conceito de fila, pub/sub e event-driven** vive em [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]]; os **serviços gerenciados de mensageria** (SQS/SNS/EventBridge a fundo) são o Galho 13 desta trilha; **IaC** (empacotar/deployar a função) é o Galho 16; **observabilidade** (medir cold start/latência) é o Galho 17; **FinOps** (otimização de custo a fundo) é o Galho 19. Este galho trata a função em si — sua anatomia, seus gatilhos, sua performance e seu custo — e linka essas fronteiras em vez de reexplicá-las.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/01 - O que é serverless, de verdade|01 — O que é serverless, de verdade]] — o modelo mental sem o mal-entendido do nome: execução sob demanda, pay-per-use real, o espectro de compute (VM → container → função), FaaS vs serverless amplo, e o que serverless *não* resolve; AWS Lambda ↔ DO Functions (OpenWhisk).

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/02 - Anatomia de uma função Lambda|02 — Anatomia de uma função Lambda]] — a mecânica por dentro: handler, objetos event e context, runtimes gerenciados vs custom, deployment package (zip vs imagem) e layers, execution role (IAM), e os limites que definem a caixa (timeout 15min, memória 128MB-10GB, /tmp efêmero, payload).
3. [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/03 - O modelo de eventos: triggers e integrações|03 — O modelo de eventos: triggers e integrações]] — serverless é reativo: os três modelos de invocação (síncrono, assíncrono, poll-based/event source mapping), os event sources (API Gateway, S3, SQS, SNS, EventBridge, Streams), o tratamento de erro por modelo (retry, DLQ, poison message travando a shard); DO só web/scheduled trigger.
4. [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/04 - Cold start, concurrency e performance|04 — Cold start, concurrency e performance]] — o que separa usar de entender Lambda: o ciclo de vida do ambiente (Init/Invoke/Shutdown), cold vs warm start, o modelo de escala (1 request = 1 ambiente, burst 1000/10s), reserved vs provisioned concurrency, o acoplamento memória↔CPU, throttling.
5. [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/05 - Pricing, limites e operação|05 — Pricing, limites e operação]] — quanto custa e quando explode: a fórmula GB-segundo com exemplo trabalhado, o ponto de virada Lambda vs EC2 reservada, os custos escondidos (provisioned concurrency, data transfer, logs), versionamento ($LATEST vs versões), aliases e canary; GB-s ↔ GiB-s da DO.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/06 - Quando serverless faz (e não faz) sentido|06 — Quando serverless faz (e não faz) sentido]] — a árvore de decisão serverless vs container gerenciado vs VM (por padrão de carga, duração, cold start, estado, controle de hardware), os casos onde FaaS brilha e os anti-padrões, o lock-in, e a ponte para o resto do Bloco 3 (containers, mensageria, API Gateway, arquiteturas event-driven). Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — o modelo, a anatomia, os gatilhos, a performance, o custo, e a decisão de arquitetura no fim.

### Já uso Lambda, quero fechar as lacunas

04 (o modelo de escala e a diferença reserved vs provisioned concurrency que toda entrevista cobra) → 05 (o ponto de virada de custo contra uma VM reservada) → 06 (a árvore que separa serverless de container e VM sem hesitar).

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/index|Compute I — máquinas virtuais]] — Galho 5, a VM que serverless contrasta a cada passo
- [[03-Dominios/Tecnologia/Cloud/06 - Compute II — elasticidade e balanceamento/index|Compute II — elasticidade e balanceamento]] — Galho 6, a elasticidade de VM que serverless tenta substituir
- [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Identidade e acesso (IAM)]] — Galho 4, a execution role que a função assume
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — o conceito de fila e event-driven que os triggers deste galho encarnam
