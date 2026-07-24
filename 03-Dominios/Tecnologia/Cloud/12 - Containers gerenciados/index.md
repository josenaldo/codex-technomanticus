---
title: "Cloud — Containers gerenciados"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - containers
  - ecs
  - fargate
  - kubernetes
aliases:
  - "Containers gerenciados"
  - "Galho 12 - Containers gerenciados"
---

# Containers gerenciados

> [!abstract] TL;DR
> Galho 12 da trilha Cloud, Bloco 3. O galho anterior mostrou o extremo "sem servidor nenhum" — uma função que nasce e morre por invocação. O Galho 5 mostrou o outro extremo — uma VM inteira, sob seu controle total. Este galho ocupa o **meio-termo do espectro de compute**: rodar um container em produção sem gerenciar o servidor por baixo dele. O fio condutor sobe do mapa (o que "gerenciado" assume, concretamente — scheduler, registry, health check, escala) ao caminho AWS-nativo (ECS e o modelo de tarefas, depois Fargate a fundo), passa pelo caminho PaaS da DigitalOcean (App Platform), toca Kubernetes gerenciado de raspão (EKS/DOKS, só a fronteira com o control plane), e fecha com o capstone que reabre a árvore de decisão do Galho 11 — agora com a caixa "container gerenciado" aberta em quatro sabores próprios. 6 notas, 3 fases, lente dupla AWS ↔ DigitalOcean.

## Sobre este galho

Container gerenciado é o degrau que a trilha ainda não tinha nomeado: nem a VM crua que você opera à mão, nem a função que o provedor faz nascer e morrer por invocação, mas um processo empacotado numa imagem que o provedor agenda, monitora, reinicia e escala — sem você tocar num scheduler, num daemon de restart ou num script de health check escrito à unha. Este galho não reensina Docker nem o que é um container — isso é ofício de Operação. O que ele cobre é a fatia de infraestrutura que se soma ao container quando você o leva pra produção na nuvem pública.

O fio condutor sobe do mapa à árvore fina. Primeiro o *quê* — o que "gerenciado" resolve concretamente (scheduling, health check, escala, service discovery, integração com load balancer), o registry como pré-requisito, e o panorama dos quatro caminhos que AWS e DigitalOcean oferecem dentro do mesmo degrau. Depois a *mecânica AWS* em duas notas: o modelo de tasks do ECS (task definition, task, service, cluster, as duas roles IAM), e o Fargate por dentro (billing por vCPU/GB-segundo, `awsvpc`, Fargate Spot). Depois o *caminho PaaS* — App Platform como PaaS opinativo, buildpacks vs Dockerfile, e a reviravolta do App Runner fechado a novos clientes. Depois *Kubernetes gerenciado de raspão* — só a fronteira: onde termina o control plane que o provedor opera e começa o workload que é seu, sem entrar em Deployments, Helm ou operators (isso é Operação). E por fim o *capstone*, que reabre a árvore VM/container/serverless do Galho 11 e a completa com a sub-árvore "qual sabor de container", nomeando o lock-in de cada escolha.

**Audiência primária:** quem já decidiu "vou rodar um container em produção" mas nunca comparou, com critério, ECS clássico contra Fargate contra App Platform contra Kubernetes gerenciado — e não sabe qual pergunta fazer pra escolher entre eles. **Audiência secundária:** quem já usa um desses serviços mas nunca formalizou a diferença entre execution role e task role, o teto de custo do Fargate contra EC2, ou o motivo de existir uma "zona compartilhada" de nós entre o control plane gerenciado e o workload que é seu.

> [!info] Fronteira
> **Container, imagem, camadas e Docker por dentro** pertencem ao domínio [[03-Dominios/Engenharia/Operação/index|Operação]], não retomados aqui. **Kubernetes como disciplina completa** — manifests, Deployments, Services, Helm, operators, GitOps — também é dono de Operação; este galho toca EKS/DOKS só o suficiente pra decidir "quando" e "por que", nunca "como operar um cluster". **Mensageria gerenciada** (SQS/SNS/EventBridge a fundo) é o próximo galho desta trilha, e é pra onde o capstone deste galho aponta a ponte final. Este galho trata o container em produção — registry, scheduler, os quatro sabores de gerenciamento, e a árvore de decisão completa — e linka essas fronteiras em vez de reexplicá-las.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/12 - Containers gerenciados/01 - O que é um container gerenciado|01 — O que é um container gerenciado]] — o mapa do galho: o container registry (ECR/DOCR), o espectro VM crua → container numa VM operada à mão → container gerenciado → função, as cinco responsabilidades que "gerenciado" assume (scheduling, health check, escala, service discovery, load balancer), e o panorama dos quatro caminhos (ECS/Fargate/EKS na AWS, App Platform/DOKS na DO).

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/12 - Containers gerenciados/02 - ECS e o modelo de tarefas|02 — ECS e o modelo de tarefas]] — o Amazon ECS por dentro: as três camadas (task definition, task, service) e o cluster, execution role vs task role, os dois launch types (EC2 vs Fargate), o rolling deployment e o service auto scaling, network mode (`awsvpc` vs `bridge`), e o loop de debug de uma task que morre sem avisar; paralelo honesto com o App Platform (que não tem cluster nem duas roles).
3. [[03-Dominios/Tecnologia/Cloud/12 - Containers gerenciados/03 - Fargate a fundo|03 — Fargate a fundo]] — Fargate como launch type serverless do ECS: capacidade por task (não por nó), a tabela fechada de combos CPU/memória, `awsvpc` obrigatório e ENI própria por task, billing por vCPU-segundo/GB-segundo, Fargate Spot (até 70% off, aviso de 2 min), o trade-off real Fargate vs EC2 launch type, e o tempo de provisionamento de task (que não é cold start de função).
4. [[03-Dominios/Tecnologia/Cloud/12 - Containers gerenciados/04 - App Platform e o caminho PaaS|04 — App Platform e o caminho PaaS]] — o caminho PaaS da DigitalOcean: os cinco tipos de component (services/workers/jobs/static_sites/databases), buildpacks vs Dockerfile, deploy automático a cada `git push`, scaling horizontal/vertical e TLS gerenciado por padrão; a reviravolta do App Runner fechado a novos clientes e a migração recomendada pro ECS Express Mode; o teto explícito do PaaS (sem rede fina, sem sidecar, sem orquestração complexa).
5. [[03-Dominios/Tecnologia/Cloud/12 - Containers gerenciados/05 - Kubernetes gerenciado de raspão|05 — Kubernetes gerenciado de raspão]] — só a fronteira: o que o control plane gerenciado (API server, etcd, scheduler) tira do seu colo, a zona compartilhada dos node groups/node pools, EKS vs ECS por eixos concretos (portabilidade, curva, custo do control plane), DOKS como a versão enxuta (control plane grátis, HA opcional por US$ 40/mês), e a comparação de custo de um cluster pequeno em cada provedor.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/12 - Containers gerenciados/06 - Container vs VM vs serverless (capstone)|06 — Container vs VM vs serverless]] — a grande árvore de decisão em duas camadas: primeiro VM vs container gerenciado vs serverless (reabrindo e completando a árvore do Galho 11, agora com o eixo de maturidade operacional do time), depois — dentro de "container gerenciado" — qual sabor escolher (ECS EC2, Fargate, EKS/DOKS, App Platform/ECS Express Mode), com o mapa de lock-in de cada um e a ponte final pra mensageria gerenciada. Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — o mapa, os dois caminhos AWS (ECS, Fargate), o caminho PaaS da DO, Kubernetes de raspão, e a árvore de decisão completa no fim.

### Já uso container em produção, quero fechar as lacunas

02 (a diferença entre execution role e task role que toda revisão de segurança cobra) → 05 (quando EKS/DOKS realmente compensa contra ECS/App Platform) → 06 (a árvore fina que amarra tudo com o mapa de lock-in).

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Cloud/12 - Containers gerenciados" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/index|Serverless e FaaS — Lambda a fundo]] — Galho 11, a árvore de decisão que este galho reabre e completa no capstone
- [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/index|Compute I — máquinas virtuais]] — Galho 5, o outro extremo do espectro de compute que este galho ocupa o meio
- [[03-Dominios/Engenharia/Operação/index|Operação]] — dono de Docker, container por dentro, e Kubernetes como disciplina completa (manifests, Helm, operators, GitOps)
