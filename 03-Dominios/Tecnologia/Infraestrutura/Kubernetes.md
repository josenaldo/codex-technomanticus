---
title: "Kubernetes"
created: 2026-04-01
updated: 2026-08-04
type: reference
progress: done
status: evergreen
tags:
  - infraestrutura
  - devops
  - entrevista
publish: false
---

# Kubernetes

> [!info] Tronco podado — o capítulo virou galho
> Esta nota era um monólito de referência técnica de 1612 linhas, o maior da estante de Infraestrutura. Em 2026-08-04 ela foi **podada**: o conteúdo conceitual virou o galho [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/index|Kubernetes]], com 22 notas em 3 fases sob a lente *o loop de reconciliação* — o Kubernetes não executa comandos, converge estado. O que permanece aqui é o material que **não pertence ao galho**: o relato de experiência do autor e o material de articulação em inglês, ambos preservados na íntegra.

## Onde cada assunto foi parar

| Assunto que estava aqui | Onde está agora |
|---|---|
| O que é Kubernetes, quando usar | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/01 - O problema que orquestração resolve\|01 — O problema que orquestração resolve]] |
| O modelo declarativo | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/02 - O loop de reconciliação\|02 — O loop de reconciliação]] |
| Pod | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/03 - O Pod, a unidade que não é o container\|03 — O Pod, a unidade que não é o container]] |
| ReplicaSet, Deployment | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/04 - Deployment e ReplicaSet\|04 — Deployment e ReplicaSet]] |
| Service | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/05 - Service\|05 — Service]] |
| Namespace | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/06 - Namespaces, labels e selectors\|06 — Namespaces, labels e selectors]] |
| `kubectl`, comandos e API | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/07 - kubectl é um cliente de API\|07 — kubectl é um cliente de API]] |
| ConfigMap e Secret, config management | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/08 - ConfigMap e Secret\|08 — ConfigMap e Secret]] |
| Storage — PV, PVC, StorageClass | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/09 - Armazenamento\|09 — Armazenamento: PV, PVC e StorageClass]] |
| StatefulSet | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/10 - StatefulSet\|10 — StatefulSet]] |
| DaemonSet, Job e CronJob | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/11 - Job, CronJob e DaemonSet\|11 — Job, CronJob e DaemonSet]] |
| Scheduling, afinidade, taints | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/12 - Scheduling\|12 — Scheduling]] |
| RBAC e segurança | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/13 - RBAC e ServiceAccount\|13 — RBAC e ServiceAccount]] |
| Helm, Kustomize | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/14 - Helm e Kustomize\|14 — Helm e Kustomize]] |
| Ingress | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/15 - Ingress e a borda do cluster\|15 — Ingress e a borda do cluster]] |
| Arquitetura, control plane components | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/16 - O control plane por dentro\|16 — O control plane por dentro]] |
| Worker node components, probes | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/17 - O kubelet e o nó\|17 — O kubelet e o nó]] + [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/02 - O contrato de produção do Kubernetes\|Operação: o contrato de produção]] |
| CRDs e extensão da API | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/18 - A API como sistema extensível\|18 — A API como sistema extensível: CRDs]] |
| Operators | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/19 - Operators\|19 — Operators]] |
| Networking do cluster | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/20 - Rede do cluster por dentro\|20 — Rede do cluster por dentro]] |
| Troubleshooting | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/21 - Depurar um cluster\|21 — Depurar um cluster]] |
| Patterns de produção | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/22 - Capstone - do zero ao cluster\|22 — Capstone: do zero ao cluster]] |
| Resource management, requests e limits | [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/12 - Scheduling\|12 — Scheduling]] (a decisão do scheduler) + [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/17 - O kubelet e o nó\|17 — O kubelet e o nó]] (QoS e despejo) |
| **Horizontal Pod Autoscaler (HPA)** | [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/04 - Escala e capacidade\|Operação: escala e capacidade]] — **cortado do galho de propósito**, ver o callout no index |
| Deployment strategies | [[03-Dominios/Engenharia/Operação/2 - Entrega e release/02 - Deployment strategies\|Operação: deployment strategies]] + [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/03 - Zero-downtime e alta disponibilidade\|zero-downtime]] |
| Observabilidade | [[03-Dominios/Engenharia/Operação/4 - Observar e responder/index\|Operação: observar e responder]] |
| Armadilhas comuns | distribuídas na seção `## Armadilhas comuns` de cada nota do galho |

## Na prática (da minha experiência)

> **MedEspecialista — Kubernetes em produção:**
>
> Cluster gerenciado (EKS / GKE / AKS dependendo do ambiente). Stack básica:
>
> - **Deployments** para apps stateless
> - **StatefulSets** para PostgreSQL, Redis, Kafka
> - **HPA** em todos os Deployments de API
> - **PDB** mínimo de 2 réplicas
> - **Pod anti-affinity** para espalhar por AZs
> - **NetworkPolicies** default-deny + explicit allows
> - **Pod Security Standards: restricted** em todos os namespaces
> - **cert-manager** para TLS automático via Let's Encrypt
> - **nginx-ingress** como Ingress controller
> - **External Secrets Operator** para sincronizar com AWS Secrets Manager
> - **kube-prometheus-stack** para métricas
> - **Loki** para logs
> - **OpenTelemetry** para traces → Jaeger
> - **ArgoCD** para GitOps
>
> **Patterns que padronizei:**
>
> **1. Kustomize overlays:** `base/` + `overlays/{dev,staging,prod}/`. ArgoCD sincroniza cada overlay em seu cluster.
>
> **2. Secrets fora do git:** External Secrets Operator pulling de AWS Secrets Manager. Manifests em git só referenciam.
>
> **3. Probes diferenciadas:** startup probe para Java (lento), readiness checa DB + cache, liveness só verifica se processo está vivo.
>
> **4. Graceful shutdown sempre:** `terminationGracePeriodSeconds: 60`, app captura SIGTERM, Spring Boot com `server.shutdown=graceful`, Node com `process.on('SIGTERM')`.
>
> **5. Resource limits baseados em profiling:** nada de chute. Uso Grafana para ver CPU/memory real, configuro requests em 80% do p95 uso.
>
> **6. Namespaces por environment + app:** `dev-medespecialista`, `staging-medespecialista`, `prod-medespecialista`. Ou subdividir por domínio se muitos microserviços.
>
> **7. Deploys via GitOps:** ArgoCD. `kubectl apply` manual proibido em produção. Rollback = git revert.
>
> **Incidente memorável — CrashLoopBackOff no deploy:**
>
> Deploy de Spring Boot começou a dar CrashLoopBackOff em produção. Logs mostravam OOMKilled. Causa: nova feature aumentou uso de memória, mas memory limit continuou o mesmo. JVM heap era `-Xmx` alto, container matava. Fix: `JAVA_OPTS="-XX:MaxRAMPercentage=75"` para JVM respeitar limit do container automaticamente. Aumentei `memory.limits` também.
>
> **Outro — probe quebrada após deploy:**
>
> App subiu, mas Pods ficavam "Not Ready". Endpoints vazios, Service não roteava. Causa: readiness probe apontava para endpoint que tinha sido renomeado de `/healthz` para `/actuator/health`. Probe falhava, K8s removia do LB. Fix óbvio, mas demorou para descobrir porque `kubectl logs` mostrava app healthy. **Lição:** readiness probe deve usar o mesmo endpoint de monitoring, documentado como API estável.
>
> **Terceiro — NetworkPolicy quebrando DNS:**
>
> Adicionei NetworkPolicy restritiva sem allowar kube-dns. Apps começaram a falhar em resolver `postgres.default.svc.cluster.local`. Fix: adicionar regra de egress para o namespace `kube-system` na porta 53 (UDP e TCP). **Lição:** NetworkPolicies default-deny são boas, mas sempre allowar DNS.
>
> **A lição principal:** Kubernetes é poderoso mas tem muitas partes móveis. Invista em observability desde o dia 1 (Prometheus + Grafana + logs centralizados), use GitOps para evitar drift, pratique com um cluster local (kind, k3d, minikube) antes de tocar produção, e **nunca confie em 'funciona na minha máquina'** — teste no cluster real.

---

## How to explain in English

> "Kubernetes is the de facto standard for running containers at scale. What I value is the declarative model — I describe the desired state in YAML, and Kubernetes continuously reconciles reality to match. Self-healing, rolling updates, and service discovery come for free.
>
> My baseline for any production deployment: Deployments with 3+ replicas, resource requests and limits, liveness and readiness probes that target different concerns (liveness catches deadlocks, readiness gates traffic), anti-affinity to spread replicas across nodes, Pod Disruption Budgets to guarantee minimum availability, and graceful shutdown handlers.
>
> For configuration, I use Kustomize for my own manifests with base and overlays per environment, and Helm for upstream charts like Prometheus or Cert Manager. Secrets never live in git — I use External Secrets Operator syncing from AWS Secrets Manager or Vault.
>
> Everything goes through GitOps with ArgoCD. Developers merge to main, ArgoCD detects the diff and applies. No manual `kubectl apply` in production. Rollbacks are `git revert`. This gives me full audit trail and prevents configuration drift.
>
> For observability, I run kube-prometheus-stack for metrics and alerts, Loki for logs, and OpenTelemetry for distributed tracing. Applications expose a `/metrics` endpoint for Prometheus to scrape, and I build Grafana dashboards for each service plus cluster-level dashboards for capacity planning.
>
> For security: Pod Security Standards at `restricted` level, non-root containers, read-only root filesystems where possible, NetworkPolicies with default-deny and explicit allows, RBAC minimum privilege, and image scanning in CI with Trivy.
>
> The pitfalls I watch for: resource limits that are too tight causing OOMKilled, probes that are too aggressive causing false failures, using `latest` tags, secrets in plain YAML, missing Pod anti-affinity so all replicas end up on one node, and the classic — NetworkPolicies that break DNS because they forgot to allow kube-system port 53."

### Frases úteis em entrevista

- "Kubernetes is declarative — I describe desired state, it reconciles reality."
- "Deployment for stateless, StatefulSet for stateful — use Deployment whenever possible."
- "Liveness restarts, readiness gates traffic. Don't confuse them."
- "Resource requests aren't optional — QoS depends on them."
- "Rolling updates with `maxUnavailable: 0` for zero-downtime deploys."
- "Pod anti-affinity spreads replicas across nodes for HA."
- "GitOps with ArgoCD — no manual kubectl apply in production."
- "Kustomize for my manifests, Helm for upstream charts."
- "Secrets via External Secrets Operator, never in git."
- "Pod Security Standards at `restricted` level in production."
- "NetworkPolicies default-deny with explicit allows — including DNS."
- "HPA based on real metrics, not just CPU."
- "Graceful shutdown with preStop hook and terminationGracePeriodSeconds."

### Key vocabulary

- plano de controle → control plane
- nó trabalhador → worker node
- agendador → scheduler
- conjunto de réplicas → ReplicaSet
- implantação → Deployment
- serviço → Service
- ingresso → Ingress
- espaço de nomes → namespace
- rolagem → rolling update
- reversão → rollback
- escalonamento horizontal → horizontal pod autoscaling
- sonda de vivacidade → liveness probe
- sonda de prontidão → readiness probe
- rótulo → label
- seletor → selector
- afinidade de pod → pod affinity
- anti-afinidade → anti-affinity
- dreno → drain (node)
- interferência → drift

---

## Recursos

### Documentação oficial

- [Kubernetes Docs](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)

### Livros e cursos

- **Kubernetes Up & Running** — Kelsey Hightower, Brendan Burns (3rd edition)
- **Kubernetes in Action** — Marko Lukša (2nd edition)
- **The Kubernetes Book** — Nigel Poulton
- [CNCF Kubernetes Hardening Guide](https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-083a)
- **Full Stack Open Part 12** — containers & K8s (gratuito, Universidade de Helsinki)

### Certificações

- **CKA** (Certified Kubernetes Administrator) — operations-focused
- **CKAD** (Certified Kubernetes Application Developer) — dev-focused
- **CKS** (Certified Kubernetes Security Specialist) — security

### Ferramentas

- [kubectl](https://kubernetes.io/docs/reference/kubectl/) — CLI oficial
- [k9s](https://k9scli.io/) — TUI para Kubernetes (essencial)
- [kubectx / kubens](https://github.com/ahmetb/kubectx) — switch rápido de contexto/namespace
- [stern](https://github.com/stern/stern) — multi-pod log tailing
- [lens](https://k8slens.dev/) — IDE gráfico para K8s
- [kind](https://kind.sigs.k8s.io/) — K8s local em Docker
- [k3d](https://k3d.io/) — K3s em Docker (mais leve)
- [minikube](https://minikube.sigs.k8s.io/) — cluster local
- [helm](https://helm.sh/) — package manager
- [kustomize](https://kustomize.io/) — config management
- [argocd](https://argo-cd.readthedocs.io/) — GitOps
- [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
- [cert-manager](https://cert-manager.io/) — TLS certificates
- [external-secrets-operator](https://external-secrets.io/)
- [trivy](https://trivy.dev/) — security scanning
- [kubescape](https://kubescape.io/) — security posture

### Blogs

- [Kubernetes Blog](https://kubernetes.io/blog/)
- [CNCF Blog](https://www.cncf.io/blog/)
- [Learnk8s](https://learnk8s.io/) — tutoriais de alta qualidade
- [Brendan Burns' articles](https://brendanburns.com/)

---

## Veja também

- [[Docker]] — containers base
- [[Linux]] — foundation
- [[Nginx]] — ingress controller
- [[CI-CD]] — deploy automatizado
- [[03-Dominios/Engenharia/Arquitetura/System Design/index|System Design]] — K8s em architecture
- [[Spring Boot]] — apps Java em K8s
- [[Node.js]] — apps Node em K8s
- [[WSL, Docker e Kubernetes]] — setup em Windows
- [[03-Dominios/Ciência/Banco de Dados/index|Banco de Dados]] — StatefulSets, operators
- [[Arquitetura de Software]] — microservices patterns
