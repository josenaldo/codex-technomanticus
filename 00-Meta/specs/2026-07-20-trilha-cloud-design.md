---
title: "Design — Trilha Cloud"
type: spec
created: 2026-07-20
updated: 2026-07-20
status: growing
publish: false
tags:
  - meta
  - spec
  - roadmap
  - cloud
aliases:
  - Design Trilha Cloud
  - Spec Cloud
---

# Design — Trilha Cloud

> [!abstract] TL;DR
> Construir o domínio **Cloud** em `03-Dominios/Tecnologia/Cloud/` como trilha completa "do zero" (escala Java/Python/Go): **24 galhos + capstone**, notas atômicas em 3 fases (Iniciado/Adepto/Magus), padrão capítulo. **Espinha conceitual-neutra** com **lente dupla AWS↔DigitalOcean** nota a nota, **Azure/GCP como camada de tradução** (tabela de 4 colunas + galho panorama), e o **Well-Architected Framework** como bússola que costura a trilha inteira. Fecha o buraco 🚫 "Cloud sem domínio próprio" do Roadmap mestre.

## Contexto e decisão de escopo

Cloud é hoje um **buraco real (🚫)** do grimório: existe só a `Senda Cloud` (uma lista de links AWS) e cobertura de raspão pela trilha de Operação. É o próximo item de *construção nova* (Tier 1) do Roadmap mestre após Go — e o de maior valor para o objetivo de entrevistas internacionais remotas.

**Perfil-alvo:** Senior Fullstack (maduro em Java/Node/Python/Go), prep para entrevistas internacionais. **Ponto de partida real:** trabalha principalmente com **DigitalOcean há ~2 anos**; sabe pouco de cloud de forma sistemática/formal.

**Drivers, em ordem de prioridade (decisão do usuário): C → B → A.**
- **C — Aprender do zero (primário):** material autossuficiente, escala Java/Python, "começar como se não soubesse nada", cobrindo o mapa inteiro. Define a trilha como *full-scale enciclopédica*.
- **B — Aprofundar o trabalho atual:** ancorar no que ele já faz em DigitalOcean; AWS como a "cloud de referência" mais robusta.
- **A — Entrevista sênior:** arquitetura provider-neutra + Well-Architected + vocabulário AWS que o entrevistador espera; entra como profundidade (fase Magus) e no capstone/certificação.

## Decisões-âncora do design (aprovadas no brainstorming)

1. **Escala full-scale**, como Java/Python/Go — trilha "do zero", não galho enxuto para poliglota.
2. **Provedores — espinha conceitual-neutra + lente dupla:** cada galho ensina o *conceito* primeiro e mostra concretamente nos dois provedores hands-on: *"em AWS é S3, em DO é Spaces"* — a lente cross-stack da trilha Go, aplicada a provedores. AWS = vocabulário-padrão; DO = "e como eu já faço isso hoje". Mais um toque de consolidação por provedor no Bloco 5.
3. **Azure + GCP — camada de tradução (não hands-on):**
   - **Tabela de 4 colunas** (Conceito · AWS · Azure · GCP · DO) nos galhos de primitivos, fixando conceito + mapa de nomes.
   - **Galho dedicado "Panorama multi-cloud e portabilidade"** (Magus) com a filosofia de cada provedor, lock-in vs portabilidade, e o vocabulário de entrevista.
   - Serve o driver A sem inflar a trilha com prática de provedores que o usuário não usa.
4. **Well-Architected Framework como bússola:** os 6 pilares (operational excellence, security, reliability, performance efficiency, cost optimization, sustainability) costuram a trilha; galhos de arquitetura/operação amarram de volta a um pilar.
5. **Certificação como galho dedicado:** AWS Solutions Architect Associate (SAA-C03), no padrão Java-OCP / Python-PCEP-PCAP; mapeia a trilha ao blueprint do exame e serve o driver A.

## Fronteiras com trilhas existentes (regra anti-duplicação)

Linha divisória canônica:

- **Cloud = a plataforma e seus serviços.** *O que* a nuvem oferece e *como arquitetar* com isso: os primitivos (compute/storage/rede/identidade), o modelo de serviço (IaaS→FaaS→SaaS), serverless/Lambda, responsabilidade compartilhada, a **economia da cloud (FinOps)**, o **Well-Architected Framework**, e o específico de AWS/DO. **Território sem dono hoje no vault.**
- **[[03-Dominios/Engenharia/Operação/index|Operação (DevOps/SRE)]] = a disciplina de operar**, provider-neutra (SRE, SLO, deploy strategies, incident response). Cloud *usa* essas práticas mas não as reensina — aponta pra lá via callout. Onde Operação pergunta *"como opero isso com responsabilidade?"*, Cloud pergunta *"o que a AWS/DO me oferece e como desenho em cima?"*.
- **[[03-Dominios/Engenharia/Arquitetura/index|System Design]] / [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] = os conceitos abstratos** (o que é um LB, uma fila, um CDN, sharding). Cloud mostra a **encarnação gerenciada** (ELB, SQS, CloudFront) e linka de volta. Ex.: o *conceito* de fila fica em Comunicação; *quando/como usar SQS/SNS gerenciado* entra em Cloud (galho 13).
- **Galhos "Cloud-native e produção"** de Java/Python/Go (empacotamento, contrato K8s, JVM-no-container) permanecem donos do *lado da aplicação*; Cloud é dona do *lado da plataforma*.

Postura: Cloud é **econômica** nas fronteiras (linka, não reexplica), e **generosa** só onde é dona de fato (primitivos, serverless, FinOps, Well-Architected, específico de provedor).

## Roster de galhos (24 + capstone)

### Bloco 1 — Modelo mental e fundamentos (Iniciado)
1. **O que é a nuvem, de verdade** — capex→opex, modelos de serviço (IaaS/PaaS/**FaaS**/SaaS/CaaS), modelos de deploy (public/private/hybrid/multi), elasticidade, a virada mental.
2. **Anatomia de um provedor** — conta/organização, **regions & availability zones**, edge locations, plano de controle vs plano de dados, console/CLI/SDK/API, **modelo de responsabilidade compartilhada**.
3. **Well-Architected Framework** — os 6 pilares como modelo mental de arquitetar; a bússola da trilha.
4. **Identidade e acesso (IAM)** — o primeiro serviço de verdade: users/groups/roles/policies, least privilege, IAM AWS vs DO. Segurança começa aqui.

### Bloco 2 — Os primitivos (Iniciado→Adepto)
5. **Compute I — máquinas virtuais** — EC2/Droplets, tipos de instância, imagens/AMIs, user data, lifecycle, pricing (on-demand/reserved/spot).
6. **Compute II — elasticidade e balanceamento** — auto scaling groups, load balancers (ALB/NLB, DO LB), health checks; encarnação gerenciada do LB de System Design.
7. **Rede na nuvem (VPC)** — subnets pública/privada, route tables, internet/NAT gateway, security groups, NACLs, VPC peering, DO VPC. O galho mais importante e mais temido.
8. **Armazenamento (object/block/file)** — S3/Spaces (durabilidade, classes de acesso, versioning, lifecycle), EBS/Volumes, EFS.
9. **Bancos gerenciados** — RDS/Managed DB, réplicas, Multi-AZ, backups; NoSQL (DynamoDB); cache (ElastiCache/Redis). Ponte→System Design/Dados.
10. **DNS, CDN e borda** — Route53/DO DNS, CloudFront/CDN, TLS/certificados (ACM). Ponte→System Design (CDN).

### Bloco 3 — Serverless e arquiteturas modernas (Adepto)
11. **Serverless / FaaS — Lambda a fundo** — triggers, cold start, concurrency, timeout, memória/pricing, modelo de eventos; DO Functions.
12. **Containers gerenciados** — ECS/Fargate, App Platform (DO), quando container vs VM vs serverless; ponte→Operação (K8s), EKS/DOKS de raspão.
13. **Mensageria e eventos gerenciados** — SQS/SNS/EventBridge; event-driven na cloud; ponte→Comunicação (conceito de fila lá, serviço gerenciado aqui).
14. **API Gateway e edge de aplicação** — API Gateway, throttling, autorização; ponte→Comunicação (rate limiting) e Auth.
15. **Arquiteturas serverless e event-driven** — juntar tudo: fan-out, orquestração (Step Functions), serverless data pipeline, quando serverless faz (e não faz) sentido.

### Bloco 4 — Operar, sustentar, governar (Adepto→Magus)
16. **Infrastructure as Code** — Terraform (multi-cloud) + nativo (CloudFormation), state, módulos; ponte→Operação (GitOps/IaC).
17. **Observabilidade na cloud** — CloudWatch (logs/métricas/alarms), X-Ray, o que é específico do provedor; ponte→Operação (observabilidade).
18. **Segurança na cloud a fundo** — shared responsibility na prática, KMS/Secrets Manager, encryption at rest/in transit, VPC security, compliance, threat model cloud; ponte→Segurança/Auth.
19. **FinOps — a economia da cloud** — cost optimization pillar a fundo: pricing models, budgets/alerts, tags, right-sizing, spot/reserved, "por que a conta explodiu". **Território exclusivo da Cloud; ouro pra sênior.**
20. **Resiliência e continuidade** — Multi-AZ vs multi-region, RTO/RPO, estratégias de backup/DR; ponte→Operação (reliability)/System Design.

### Bloco 5 — Provedores e maestria (Magus)
21. **AWS a fundo — consolidação** — mapa de serviços, filosofia AWS (amplitude), navegação console/CLI, os "big rocks" que faltaram.
22. **DigitalOcean a fundo — consolidação** — o que o DO faz diferente/melhor (DX, pricing previsível, App Platform), quando DO basta e quando "cresce pra AWS". Ancora no que o usuário já faz.
23. **Panorama multi-cloud e portabilidade** — filosofia Azure (enterprise/Microsoft) e GCP (dados/K8s/rede), tabela de tradução completa dos 4 provedores, lock-in vs portabilidade, K8s como camada de portabilidade.
24. **Certificação — AWS Solutions Architect Associate (SAA-C03)** — mapeia a trilha ao blueprint do exame; domínios do exame, formato, estratégia de prova. Padrão Java-OCP / Python-PCEP-PCAP.

### Capstone
**Arquitetar um SaaS na cloud do zero** — pega um sistema real e desenha aplicando os 6 pilares do Well-Architected, com lente de entrevista ("desenhe X na AWS"): escolha de compute, rede/VPC, dados, resiliência multi-AZ, segurança/IAM, e o trade-off de custo. Fecha a trilha amarrando os 24 galhos.

## Artefatos de domínio

- `index.md` — MOC do domínio, galhos agrupados por bloco e por fase.
- `Dicionário.md` (`type: glossary`) — termos cloud (region, AZ, VPC, IAM role, cold start, blast radius, egress, etc.).
- `Biblioteca.md` (`type: reference`) — recursos externos; **absorve o conteúdo da atual `04-Sendas/Senda Cloud.md`** (AWS Architecture Center, Well-Architected, whitepapers, treinamentos) + equivalentes DO/Azure/GCP.
- `roadmap.md` — roadmap recursivo do domínio (raiz→galho→nota), no padrão vault.

## Sequência de construção sugerida

Bloco a bloco, na ordem numérica (1→5 → capstone). Fundamentos (1–4) primeiro por serem pré-requisito de tudo; IAM (4) cedo porque segurança permeia. Primitivos (5–10) formam a base concreta. Serverless (11–15) e governança (16–20) assumem os primitivos. Consolidação por provedor + cert + capstone (21–24 + capstone) fecham no nível Magus.

Cada galho segue o ciclo do vault: escrever notas no padrão capítulo (sem gate de aprovação por nota) → verificar-nota → depois, passada de enriquecimento de mídia (M1).

## Não-objetivos (YAGNI)

- **Não** reensinar SRE/deploy strategies/incident response (vive em Operação — linka).
- **Não** reensinar conceitos abstratos de LB/fila/CDN/sharding (vive em System Design/Comunicação — mostra a encarnação gerenciada e linka).
- **Não** dar tratamento hands-on a Azure/GCP — só tradução/comparação.
- **Não** virar trilha de Kubernetes (vive em Infraestrutura/Operação — Cloud toca EKS/DOKS de raspão em containers gerenciados).
- **Não** cobrir enriquecimento de mídia agora (passada M1 posterior, como nas outras trilhas escritas-mas-não-enriquecidas).

## Atualização do Roadmap mestre

Ao concluir (ou ao iniciar), mover **Cloud** de "Tier 1 — construção nova (🚫)" para a seção de Tecnologia com estado 🟢/✅, e riscar o item em "Coberturas ausentes a considerar".
