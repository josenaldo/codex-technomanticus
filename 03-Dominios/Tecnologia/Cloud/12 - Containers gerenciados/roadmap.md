---
title: "Roadmap — Containers gerenciados"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Containers gerenciados (galho 12)

Roadmap-folha do galho `Cloud/12 - Containers gerenciados`. Bloco 3 (Serverless e arquiteturas modernas) — segundo galho do bloco, na sequência do Galho 11 (Serverless e FaaS). Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - O que é um container gerenciado
- **Estado:** ✅ feita · fase: Iniciado · 252 linhas
- **Escopo:** o problema (`docker run` local não responde onde/restart/escala/tráfego/service discovery), o container registry (ECR scan-on-push/lifecycle/replicação vs DOCR três planos/20GB camada/100GB imagem), o espectro de 4 degraus (VM crua → container numa VM operada → container gerenciado → função), as cinco responsabilidades que "gerenciado" assume em tabela (scheduling, health check/restart, escala, service discovery, load balancer), panorama dos quatro caminhos (ECS+EC2/Fargate/EKS na AWS; App Platform/DOKS na DO) com árvore, snippets de task definition JSON vs app spec YAML lado a lado, tabela de tradução 4 provedores; fecha nomeando fronteira com Operação (Docker/K8s a fundo).

#### 02 - ECS e o modelo de tarefas
- **Estado:** ✅ feita · fase: Adepto · 336 linhas
- **Escopo:** as três camadas (task definition = blueprint versionado por family:revisão, task = instância rodando, service = guardião do desiredCount com rolling deployment), anatomia de task definition em JSON (containerDefinitions/portMappings/awsvpc/environment vs secrets/logConfiguration/healthCheck), execution role (pull de imagem + logs, antes da task existir) vs task role (permissão da app em runtime) com sequenceDiagram e link pra IAM (galho 4), launch types EC2 vs Fargate, comandos `register-task-definition`/`create-service`/`update-service` reais, service auto scaling via target tracking, loop de debug de task morta (stoppedReason → CannotPullContainerError/ResourceInitializationError/health check), tabela de network mode (awsvpc/bridge/host/none), paralelo honesto com App Platform (sem cluster, sem duas roles, sem launch type).

#### 03 - Fargate a fundo
- **Estado:** ✅ feita · fase: Adepto · 236 linhas
- **Escopo:** Fargate como launch type serverless do ECS (não substitui ECS, é um jeito de rodar tasks), capacidade por task em tabela fechada de combos CPU/memória (256→16384 unidades, Firecracker por baixo), `awsvpc` obrigatório com ENI própria por task (security group por task, não por instância), pricing por vCPU-segundo + GB-segundo com exemplo calculado (~$1,17/dia pra 1vCPU+2GB), Fargate Spot (até 70% off, aviso de 2 min, capacity provider strategy com base+weight), duas identidades IAM (executionRoleArn vs taskRoleArn) por task, tabela Fargate vs EC2 launch type (bin packing, custo em escala, startup), task startup time (dezenas de segundos, não cold start de função), paralelo honesto com App Platform (PaaS opinativo vs primitiva de execução), tabela Azure/GCP só vocabulário.

#### 04 - App Platform e o caminho PaaS
- **Estado:** ✅ feita · fase: Adepto · 269 linhas
- **Escopo:** App Platform como PaaS (linhagem Heroku 2007, lançado pela DO em 2020), cinco tipos de component em tabela (services/workers/jobs/static_sites/databases) com app spec YAML completo de exemplo, buildpacks (Cloud Native Buildpacks/CNB) vs Dockerfile como escolha dentro do PaaS, ciclo de deploy automático (`deploy_on_push`, 5 passos), scaling horizontal (`instance_count` até 250) vs vertical (`instance_size_slug`) com autoscaling CPU (exige dedicada) ou requisição/P95 (até 100 instâncias), TLS gerenciado por padrão (Let's Encrypt), caso prático "zero ao ar em 5 min", lente dupla com App Runner — **reviravolta: App Runner fechado a novos clientes, recomendação oficial é ECS Express Mode** (imagem pronta, não builda de source), tabela comparativa App Platform/App Runner/ECS Express Mode, teto explícito do PaaS (rede fina, sidecars/service mesh, runtime de baixo nível, orquestração complexa, portabilidade).

#### 05 - Kubernetes gerenciado de raspão
- **Estado:** ✅ feita · fase: Adepto · 260 linhas
- **Escopo:** só a fronteira do que o provedor gerencia (analogia síndico/prédio/apartamento), diagrama de 3 zonas (control plane do provedor / zona compartilhada de node groups-node pools / workloads seus), EKS (Kubernetes certificado upstream, managed node groups vs self-managed vs Fargate profiles, `eksctl create cluster`, IRSA, upgrades com suporte ~14 meses), DOKS (mesmo K8s upstream, `doctl kubernetes cluster create`, Cluster Autoscaler + HPA, auto-upgrade opinativo), pricing control plane (EKS US$0,10/h fixo vs DOKS grátis padrão/US$40/mês HA) com diagrama comparativo de resiliência multi-AZ, EKS vs ECS por eixos em tabela + árvore de decisão + exemplo fintech antes/depois de requisito de portabilidade, conta completa de cluster pequeno nos dois provedores (~US$180-200 EKS vs ~US$84 DOKS), diferença de CNI (VPC CNI vs Cilium/eBPF) citada sem aprofundar; fronteira forte e explícita com Operação (Deployments/Helm/GitOps fora do escopo).

#### 06 - Container vs VM vs serverless (capstone)
- **Estado:** ✅ feita · fase: Magus · 259 linhas · **FECHA o galho**
- **Escopo:** reabre a árvore de decisão do capstone do Galho 11 (VM/container/serverless, 6 eixos numéricos) e acrescenta o eixo de maturidade operacional do time em tabela; abre a caixa "container gerenciado" numa árvore fina própria (ECS Express Mode/App Platform vs Fargate vs EKS/DOKS vs ECS EC2) com tabela de controle/simplicidade/portabilidade/custo dos 4 sabores; 3 padrões onde container vence (app stateless de longa duração, >15min, portabilidade, sidecars) + 4 anti-padrões; mapa de lock-in em 3 níveis (alto: serverless/ECS clássico/App Platform; médio: Fargate; baixo: EKS/DOKS) com a ironia estrutural nomeada (container não é uniformemente portável); comandos lado a lado dos 4 sabores (App Platform/Express Mode/Fargate clássico/kubectl); tabela-síntese das 6 notas do galho; dois casos práticos retomados (fintech AWS antes/depois de portabilidade; startup 100% DO); ponte final pro próximo galho (mensageria gerenciada — SQS/SNS/EventBridge a fundo).

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Galho escrito integralmente em 2026-07-24, na sequência direta do Galho 11 (Serverless e FaaS), abrindo a segunda metade do "meio-termo do espectro de compute" que o capstone do Galho 11 já havia antecipado.
- **Reviravolta factual capturada:** o AWS App Runner foi fechado a novos clientes — a AWS recomenda oficialmente o ECS Express Mode como caminho PaaS-lite atual. Isso muda a lente dupla da nota 04 e reaparece na árvore fina do capstone (06); registrado com [!warning] explícito na nota 04, não tratado como nota de rodapé.
- **Achado factual de custo:** control plane do EKS cobra US$0,10/hora sempre (~US$73/mês); DOKS é grátis no padrão, com HA opcional a US$40/mês — a comparação completa (não só control plane) inverte a intuição rápida "EKS é só um pouco mais caro"; a conta de cluster pequeno na nota 05 (~US$180-200 EKS vs ~US$84 DOKS) torna isso concreto.
- Honestidade de paridade DO capturada em cada nota: DOCR sem scan-on-push documentado (nota 01), App Platform sem equivalente a Fargate Spot (nota 03), DOKS sem IRSA/EKS Auto Mode equivalente (nota 05), sem "Fargate da DO" na árvore fina do capstone (06).
- Fronteira com Operação mantida estrita e repetida em todas as notas: Docker/imagem/camadas nunca reexplicados; Kubernetes como disciplina (Deployments, Services, Helm, operators, GitOps) explicitamente fora do escopo, nomeado com [!info] Fronteira na nota 05 e no capstone.
- Ponte de saída do capstone (06) aponta pro próximo galho da trilha — mensageria gerenciada (SQS/SNS/EventBridge a fundo) — ainda não escrito; galho 13 não existe no vault no momento deste roadmap.
