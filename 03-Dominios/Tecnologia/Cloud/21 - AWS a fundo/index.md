---
title: "Cloud — AWS a fundo (consolidação)"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - aws
aliases:
  - "AWS a fundo"
  - "Galho 21 - AWS a fundo"
---

# AWS a fundo — consolidação

> [!abstract] TL;DR
> Galho 21 da trilha Cloud, e o que **abre o Bloco 5 (Provedores e maestria)**. Os vinte galhos anteriores te deram os primitivos — IAM, compute, rede, armazenamento, bancos, serverless, mensageria, borda, IaC, observabilidade, segurança, FinOps, resiliência — sempre com a lente dupla AWS↔DigitalOcean. Este galho vira a câmera pra AWS sozinha e responde a pergunta que os primitivos, isolados, não respondem: **a AWS não é um produto — é um continente de ~240 serviços**, e o valor sênior não está em decorar cada um, mas em navegar a amplitude. O galho abre com o **porquê** (a filosofia que explica por que a AWS cresceu assim), segue pro **o quê importa** (o núcleo de ~25 serviços que resolve 90% dos casos, e como filtrar o resto), pro **como operar** (console, CLI, SDK, IaC — as quatro portas), pros **big rocks** que a trilha ainda não cobriu (Cognito, Athena, Step Functions e cia), pro **como compor** (as sete correntes idiomáticas que a plataforma empurra), e fecha com um **capstone** que amarra tudo num checklist mental e num caso de entrevista trabalhado. 6 notas, 2 fases, lente dupla AWS ↔ DigitalOcean mantida do início ao fim.

## Sobre este galho

Este é o primeiro dos dois galhos de consolidação por provedor do Bloco 5 — o par que fecha a trilha antes do panorama multi-cloud e da certificação. Diferente dos galhos 1-20, que ensinam um primitivo de cada vez, este galho ensina a **lente meta**: por que a AWS existe do jeito que existe, como separar sinal de ruído no catálogo inteiro, como efetivamente tocar a plataforma no dia a dia, quais big rocks importantes ficaram fora da trilha por não terem primitivo próprio, e como pensar — de ponta a ponta — como um arquiteto AWS sênior desenha um sistema novo.

O fio condutor sobe do porquê à decisão. Primeiro a **filosofia**: três forças históricas (primitivos componíveis, API-first, two-pizza teams) que explicam por que o catálogo tem duzentos e tantos itens em vez de uma dúzia. Depois o **filtro**: um framework de quatro perguntas pra separar o núcleo de ~25 serviços que carrega 80% de qualquer arquitetura real do resto, que é cauda longa consultada sob demanda. Depois a **operação**: as quatro portas de entrada (console, CLI, SDK, IaC) e a escada de maturidade que uma equipe sobe entre elas. Depois os **big rocks**: os serviços grandes o bastante pra merecer nome próprio — Cognito, Step Functions, Athena/Glue, SageMaker/Bedrock — que não couberam nos primitivos dos galhos anteriores. Depois a **composição**: as sete correntes idiomáticas (eventos, serverless-first, IAM permeando tudo, multi-AZ como piso, múltiplas contas, tags, Well-Architected) que explicam por que arquiteturas AWS tendem a se parecer entre si. E fecha com o **capstone**: um checklist de sete perguntas e um caso de entrevista completo — desenhar um encurtador de URL — mostrando o raciocínio verbalizado, com uma dose final de honestidade sobre quando a resposta certa é não usar a AWS.

**Audiência primária:** quem terminou (ou está terminando) os galhos 1-20 desta trilha e sente o "susto do console" ao abrir a lista completa de serviços da AWS pela primeira vez — sem saber o que memorizar, o que ignorar, ou como operar tudo isso além do console. **Audiência secundária:** quem já usa AWS no trabalho mas nunca formalizou o filtro sinal/ruído, a diferença entre as quatro portas de operação, ou o "jeito idiomático" que a plataforma empurra — e quer levar esse raciocínio pra uma entrevista de system design.

> [!info] Fronteira
> Este galho **não reensina** os primitivos — IAM (galho 4), compute (galhos 5-6), rede (galho 7), armazenamento (galho 8), bancos (galho 9), serverless (galho 11), mensageria (galho 13), IaC (galho 16), observabilidade (galho 17), segurança (galho 18), FinOps (galho 19) e resiliência (galho 20) já cobriram cada um a fundo, com lente dupla AWS↔DigitalOcean. Também não é um catálogo enciclopédico dos 240+ serviços — isso é a documentação oficial. O que este galho ensina é a **lente meta**: por que o catálogo é como é, como filtrá-lo, como operá-lo, o que faltou de big rocks, e como pensar como arquiteto diante de um problema novo. O contraste sistemático com a curadoria enxuta da DigitalOcean é o galho 22 (DigitalOcean a fundo), que aprofunda o lado oposto da mesma moeda.

## Adepto

1. [[03-Dominios/Tecnologia/Cloud/21 - AWS a fundo/03 - Operar a AWS — console, CLI, SDK e IaC|03 — Operar a AWS — console, CLI, SDK e IaC]] — as quatro portas de entrada pra mesma API de controle (console, CLI, SDK, IaC), quando usar cada uma, `aws configure` clássico vs. IAM Identity Center (SSO) com credenciais temporárias, CloudFormation vs. CDK, e a escada de maturidade console→IaC; `doctl` e o App Spec da DO.
2. [[03-Dominios/Tecnologia/Cloud/21 - AWS a fundo/04 - Os big rocks que faltaram|04 — Os big rocks que faltaram]] — os serviços importantes que a trilha não cobriu por não terem primitivo próprio: Cognito (identidade de usuário final), Step Functions (orquestração), Athena e Glue (SQL serverless sobre data lake), SageMaker e Bedrock (ML e IA generativa gerenciadas), e um mapa dos menores (Lambda@Edge, Systems Manager, Cost Explorer, WAF/Shield); lacunas reais na DO.

## Magus

3. [[03-Dominios/Tecnologia/Cloud/21 - AWS a fundo/01 - A filosofia da amplitude|01 — A filosofia da amplitude — por que a AWS tem 240 serviços]] — por que a AWS cresceu para ~240 serviços: primitivos pequenos e componíveis vs. plataforma opinada, "tudo é uma API primeiro" (o memorando de Bezos de 2002), working backwards e o two-pizza team, o mapa de camadas do catálogo, e o preço da amplitude (paradoxo da escolha); a curadoria oposta da DigitalOcean.
4. [[03-Dominios/Tecnologia/Cloud/21 - AWS a fundo/02 - Sinal e ruído no catálogo|02 — Sinal e ruído no catálogo]] — o núcleo de ~25 serviços em oito categorias que resolve a esmagadora maioria dos sistemas reais, os quatro sinais de ruído (reembalagem de primitivo, duplicação "com IA", modo manutenção, nicho de cliente enterprise) e o framework de avaliação rápida de quatro perguntas pra qualquer serviço novo; o catálogo enxuto da DO como "o núcleo, pré-filtrado".
5. [[03-Dominios/Tecnologia/Cloud/21 - AWS a fundo/05 - O jeito AWS de arquitetar|05 — O jeito AWS de arquitetar]] — as sete correntes idiomáticas que a plataforma empurra: eventos em vez de chamada síncrona, serverless-first pra carga variável, IAM permeando cada interação, multi-AZ como piso e multi-region como exceção, múltiplas contas como fronteira de blast radius, tags como espinha de custo, e Well-Architected como bússola; dois exemplos trabalhados e as armadilhas de seguir a corrente por reflexo.
6. [[03-Dominios/Tecnologia/Cloud/21 - AWS a fundo/06 - Capstone — pensar como arquiteto AWS|06 — Capstone — pensar como arquiteto AWS]] — síntese do galho num checklist mental de sete perguntas e um caso de entrevista de ponta a ponta (desenhar um encurtador de URL), verbalizando trade-offs; fecha com honestidade sobre quando a resposta certa é não usar a AWS. Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — o porquê, o filtro, a operação, os big rocks, a composição idiomática, e o capstone de decisão no fim.

### Já uso AWS no trabalho, quero a lente sênior

02 (o filtro sinal/ruído que formaliza o que você já faz por instinto) → 05 (as sete correntes, pra nomear o que você segue sem perceber) → 06 (o checklist e o caso de entrevista, pra levar isso pra uma sala de system design).

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Cloud/21 - AWS a fundo" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework/index|Well-Architected Framework]] — Galho 3, a bússola conceitual (os 6 pilares) que a Corrente 7 da nota 05 retoma como síntese
- [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Identidade e acesso (IAM)]] — Galho 4, o IAM que a Corrente 3 da nota 05 mostra permeando toda interação serviço-a-serviço
- O galho 22 (DigitalOcean a fundo) aplica a mesma lente de consolidação ao lado oposto da moeda — curadoria enxuta em vez de amplitude — e ainda está em construção nesta trilha.
