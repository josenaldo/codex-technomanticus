---
title: "Kubernetes"
created: 2026-04-01
updated: 2026-04-11
type: concept
status: evergreen
tags:
  - infraestrutura
  - devops
  - entrevista
publish: false
---

# Kubernetes

Deep dive em **Kubernetes (K8s)** — orquestração de containers em escala. Arquitetura, objetos core, deploy patterns, networking, storage, observabilidade e práticas de produção. Para fundamentos de containers, ver [[Docker]]. Para Linux, ver [[Linux]]. Para CI/CD, ver [[CI-CD]].

## O que é

**Kubernetes (K8s)** é uma plataforma open-source de orquestração de containers criada pelo **Google (2014)**, inspirada no Borg interno. Hoje é o **padrão de facto** para rodar containers em produção — AWS EKS, Google GKE, Azure AKS, e clusters on-premise.

**O que K8s faz:**

- **Scheduling** — decide onde cada container roda
- **Self-healing** — reinicia containers que morrem, reagenda em nós saudáveis
- **Auto-scaling** — escala horizontalmente (réplicas) ou verticalmente (recursos)
- **Load balancing** — distribui tráfego entre réplicas
- **Rolling updates** — deploy sem downtime
- **Service discovery** — containers se acham por nome DNS
- **Config e secrets** — gerenciamento centralizado
- **Storage orchestration** — montagem de volumes persistentes

**Por que K8s e não Docker Compose:**

- Compose é single-host, K8s é multi-host
- Compose não tem self-healing real nem scheduling distribuído
- Compose não tem auto-scaling
- Compose não tem rolling updates nativos
- K8s é mais complexo, mas é o que a indústria adotou

Em entrevistas, o que diferencia um senior em Kubernetes:

1. **Arquitetura do control plane** — api-server, etcd, scheduler, controller-manager
2. **Objetos core** — Pod, ReplicaSet, Deployment, Service, Ingress, ConfigMap, Secret
3. **Networking** — CNI, Services (ClusterIP/NodePort/LoadBalancer), Ingress, NetworkPolicy
4. **Storage** — PV, PVC, StorageClass, StatefulSet
5. **Resource management** — requests, limits, QoS classes, HPA, VPA
6. **Health checks** — liveness, readiness, startup probes
7. **Deployment strategies** — RollingUpdate, Recreate, Blue-Green, Canary
8. **RBAC e segurança** — ServiceAccount, Role, RoleBinding, NetworkPolicy, Pod Security
9. **Observabilidade** — logs, metrics (Prometheus), tracing
10. **Ecossistema** — Helm, Kustomize, ArgoCD, operators

---

## Arquitetura

Um cluster K8s tem dois tipos de nós: **control plane** (cérebro) e **worker nodes** (executam containers).

```
┌───────────────────────────────────────────────────────────────┐
│                     Control Plane (Master)                     │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────────┐      │
│  │  kube-       │  │  etcd       │  │  kube-scheduler  │      │
│  │  apiserver   │  │  (state)    │  │  (placement)     │      │
│  └──────┬───────┘  └─────────────┘  └──────────────────┘      │
│         │          ┌──────────────────────┐                    │
│         │          │ kube-controller-mgr  │                    │
│         │          │ (reconciliation)     │                    │
│         │          └──────────────────────┘                    │
│         │          ┌──────────────────────┐                    │
│         │          │ cloud-controller-mgr │                    │
│         │          └──────────────────────┘                    │
└─────────┼──────────────────────────────────────────────────────┘
          │
          │ (worker nodes se registram aqui)
          │
┌─────────┴──────────────────────────────────────────────────────┐
│                    Worker Nodes                                  │
│  ┌────────────────────┐  ┌────────────────────┐                │
│  │   Node 1           │  │   Node 2           │                │
│  │  ┌──────────────┐  │  │  ┌──────────────┐  │                │
│  │  │   kubelet    │  │  │  │   kubelet    │  │                │
│  │  └──────────────┘  │  │  └──────────────┘  │                │
│  │  ┌──────────────┐  │  │  ┌──────────────┐  │                │
│  │  │  kube-proxy  │  │  │  │  kube-proxy  │  │                │
│  │  └──────────────┘  │  │  └──────────────┘  │                │
│  │  ┌──────────────┐  │  │  ┌──────────────┐  │                │
│  │  │  container   │  │  │  │  container   │  │                │
│  │  │  runtime     │  │  │  │  runtime     │  │                │
│  │  │ (containerd) │  │  │  │ (containerd) │  │                │
│  │  └──────────────┘  │  │  └──────────────┘  │                │
│  │  [ Pods rodando ]  │  │  [ Pods rodando ]  │                │
│  └────────────────────┘  └────────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

### Control plane components

**`kube-apiserver`** — o único ponto de entrada. Todas as operações (kubectl, controllers, kubelet) passam por aqui. Valida e persiste no etcd.

**`etcd`** — banco de dados distribuído consistente (Raft). Guarda todo o estado do cluster. **Backup de etcd = backup do cluster inteiro.**

**`kube-scheduler`** — decide em qual node cada Pod vai rodar, baseado em recursos disponíveis, taints/tolerations, affinity, etc.

**`kube-controller-manager`** — loop de reconciliação. Compara estado desejado (specs) com estado real e age (ex.: ReplicaSet controller mantém N réplicas).

**`cloud-controller-manager`** — integra com cloud providers (ELB na AWS, etc.).

### Worker node components

**`kubelet`** — agent em cada node. Recebe specs de Pods e executa via container runtime. Reporta status ao apiserver.

**`kube-proxy`** — implementa Services (networking rules via iptables/IPVS/eBPF).

**Container runtime** — containerd (default moderno), CRI-O, ou Docker (deprecated em K8s 1.24+).

### O modelo declarativo

K8s é **declarativo**: você descreve o que quer (desired state), K8s reconcilia continuamente.

```
Você diz: "quero 3 réplicas desse app"
   ↓
apiserver guarda spec no etcd
   ↓
controller-manager percebe (watch)
   ↓
scheduler assign Pods a nodes
   ↓
kubelet recebe, cria containers
   ↓
Se um Pod morre → controller vê diff → recria
```

**Convergence.** Você nunca diz "crie um container". Você diz "deve haver 3". K8s cuida do resto.

---

## Objetos core

### Pod

**A unidade mínima em K8s.** Um Pod é um grupo de 1+ containers que **compartilham** network namespace e storage volumes.

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: my-pod
    labels:
        app: web
spec:
    containers:
        - name: app
          image: nginx:1.27-alpine
          ports:
              - containerPort: 80
          resources:
              requests:
                  memory: "64Mi"
                  cpu: "100m"
              limits:
                  memory: "128Mi"
                  cpu: "500m"
```

**Regra crítica:** você raramente cria Pods diretamente. Use um **Deployment** (ou StatefulSet/DaemonSet/Job). Pods são efêmeros — morrem, não voltam.

**Multi-container pod:** patterns comuns:

- **Sidecar** — logging agent, service mesh proxy (Envoy), auth proxy
- **Init containers** — rodam **antes** dos containers principais
- **Adapter** — normaliza output de outro container

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: app-with-sidecar
spec:
    initContainers:
        - name: wait-for-db
          image: busybox
          command: ['sh', '-c', 'until nc -z db 5432; do sleep 1; done']
    containers:
        - name: app
          image: myapp:1.0
        - name: log-shipper
          image: fluent/fluent-bit
```

### ReplicaSet

Mantém N réplicas de um Pod. **Você raramente usa direto** — Deployment gerencia ReplicaSets por você.

### Deployment

**O objeto mais comum.** Gerencia ReplicaSets e orquestra rolling updates.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: myapp
    labels:
        app: myapp
spec:
    replicas: 3
    selector:
        matchLabels:
            app: myapp
    strategy:
        type: RollingUpdate
        rollingUpdate:
            maxSurge: 1        # quantos extras durante update
            maxUnavailable: 0   # quantos podem estar down
    template:
        metadata:
            labels:
                app: myapp
        spec:
            containers:
                - name: myapp
                  image: myapp:1.2.3
                  ports:
                      - containerPort: 8080
                  resources:
                      requests:
                          memory: "256Mi"
                          cpu: "250m"
                      limits:
                          memory: "512Mi"
                          cpu: "500m"
                  livenessProbe:
                      httpGet:
                          path: /healthz
                          port: 8080
                      initialDelaySeconds: 30
                      periodSeconds: 10
                  readinessProbe:
                      httpGet:
                          path: /ready
                          port: 8080
                      initialDelaySeconds: 5
                      periodSeconds: 5
```

**Rolling update:**

```bash
kubectl set image deployment/myapp myapp=myapp:1.2.4
# ou edite o YAML e kubectl apply -f

# Ver progresso
kubectl rollout status deployment/myapp

# Histórico
kubectl rollout history deployment/myapp

# Rollback
kubectl rollout undo deployment/myapp
kubectl rollout undo deployment/myapp --to-revision=3
```

**Strategies:**

- **RollingUpdate** (default) — substitui Pods gradualmente. Zero downtime.
- **Recreate** — mata todos, depois cria novos. Downtime, mas necessário se versões são incompatíveis.

### Service

Rede estável para conjunto de Pods. Pods morrem e IPs mudam; Services têm IP estável.

```yaml
apiVersion: v1
kind: Service
metadata:
    name: myapp
spec:
    selector:
        app: myapp      # encontra pods por label
    ports:
        - port: 80       # porta do Service
          targetPort: 8080  # porta do Pod
    type: ClusterIP      # default
```

**Tipos de Service:**

| Tipo | O que faz | Uso |
| --- | --- | --- |
| **ClusterIP** (default) | IP interno, só acessível dentro do cluster | Comunicação entre services |
| **NodePort** | Expõe em porta alta em cada node | Dev/test, raramente prod |
| **LoadBalancer** | Provisiona LB do cloud (ELB, etc.) | Exposição externa |
| **ExternalName** | CNAME para serviço externo | Integração com recursos externos |
| **Headless** (`clusterIP: None`) | Retorna IPs dos Pods diretamente via DNS | StatefulSets |

**DNS:** cada Service tem nome DNS `<service>.<namespace>.svc.cluster.local`. Dentro do mesmo namespace, só `<service>` funciona.

### Ingress

Roteamento HTTP/HTTPS de tráfego externo para Services. **Um para cluster**, muitas regras.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
    name: myapp-ingress
    annotations:
        cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
    ingressClassName: nginx
    tls:
        - hosts:
              - app.medespecialista.com
          secretName: app-tls
    rules:
        - host: app.medespecialista.com
          http:
              paths:
                  - path: /
                    pathType: Prefix
                    backend:
                        service:
                            name: frontend
                            port:
                                number: 80
                  - path: /api
                    pathType: Prefix
                    backend:
                        service:
                            name: api
                            port:
                                number: 8080
```

**Ingress precisa de um controller** — nginx-ingress, traefik, HAProxy, AWS ALB Ingress Controller, Istio Gateway. Sem controller instalado, Ingress YAML não faz nada.

### ConfigMap e Secret

**ConfigMap** — configuração não-sensível:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
    name: app-config
data:
    LOG_LEVEL: info
    DATABASE_URL: postgres://db.default.svc.cluster.local/app
    app.properties: |
        server.port=8080
        spring.jpa.show-sql=true
```

**Secret** — credenciais (base64 encoded, **não** criptografado por default):

```yaml
apiVersion: v1
kind: Secret
metadata:
    name: db-credentials
type: Opaque
data:
    username: dXNlcg==       # base64 de "user"
    password: cGFzc3dvcmQ=    # base64 de "password"
```

```bash
# Criar do CLI
kubectl create secret generic db-creds \
    --from-literal=username=user \
    --from-literal=password=pass
```

**Uso em Pod:**

```yaml
spec:
    containers:
        - name: app
          image: myapp
          envFrom:
              - configMapRef:
                    name: app-config
              - secretRef:
                    name: db-credentials
          env:
              - name: API_KEY
                valueFrom:
                    secretKeyRef:
                        name: api-secret
                        key: key
          volumeMounts:
              - name: config
                mountPath: /etc/config
    volumes:
        - name: config
          configMap:
              name: app-config
```

**Cuidado com Secrets:** base64 não é criptografia. Use:

- **Encrypted etcd** (cloud providers fazem isso)
- **Sealed Secrets** (Bitnami) — criptografa no Git
- **External Secrets Operator** — sincroniza com Vault/AWS Secrets Manager
- **Vault Agent Injector** — secrets injetados em runtime

### Namespace

Divisão lógica do cluster. Isola recursos, limites, políticas.

```bash
kubectl create namespace staging
kubectl get pods -n staging
kubectl config set-context --current --namespace=staging
```

**Namespaces default:**

- `default` — onde tudo vai sem `-n`
- `kube-system` — componentes do K8s
- `kube-public` — público (raramente usado)
- `kube-node-lease` — node heartbeats

**Uso:** separar environments (dev, staging, prod), times, features.

### StatefulSet

Para workloads com **identidade persistente** — bancos de dados, Kafka, ZooKeeper.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
    name: postgres
spec:
    serviceName: postgres       # headless service
    replicas: 3
    selector:
        matchLabels:
            app: postgres
    template:
        spec:
            containers:
                - name: postgres
                  image: postgres:16
                  volumeMounts:
                      - name: data
                        mountPath: /var/lib/postgresql/data
    volumeClaimTemplates:
        - metadata:
              name: data
          spec:
              accessModes: ["ReadWriteOnce"]
              resources:
                  requests:
                      storage: 10Gi
```

**Diferenças vs Deployment:**

- **Nomes estáveis:** `postgres-0`, `postgres-1`, `postgres-2`
- **Volumes persistentes** por Pod (PVC template)
- **Ordem garantida** de startup (0 → 1 → 2)
- **Headless Service** para DNS individual

**Regra:** use StatefulSet **apenas** se precisar de identidade persistente. Para apps stateless, Deployment é mais simples.

### DaemonSet

Roda um Pod **em cada node** (ou nodes selecionados). Uso típico: agentes de logging, monitoring, storage plugins.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
    name: log-collector
spec:
    selector:
        matchLabels:
            app: log-collector
    template:
        spec:
            containers:
                - name: fluent-bit
                  image: fluent/fluent-bit
```

### Job e CronJob

**Job** — roda até completar (batch, migrações):

```yaml
apiVersion: batch/v1
kind: Job
metadata:
    name: db-migration
spec:
    backoffLimit: 3
    template:
        spec:
            restartPolicy: OnFailure
            containers:
                - name: migrate
                  image: myapp:1.0
                  command: ["./migrate.sh"]
```

**CronJob** — agendado:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
    name: backup
spec:
    schedule: "0 3 * * *"    # todo dia 3am
    jobTemplate:
        spec:
            template:
                spec:
                    restartPolicy: OnFailure
                    containers:
                        - name: backup
                          image: backup-tool:1.0
```

---

## Probes — health checks

Três tipos, cada um com propósito específico:

### Liveness probe

**"O container está vivo?"** Se falhar → K8s reinicia o container.

**Uso:** detectar deadlocks, estados irrecuperáveis.

```yaml
livenessProbe:
    httpGet:
        path: /healthz
        port: 8080
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3
```

### Readiness probe

**"O container está pronto para receber tráfego?"** Se falhar → K8s remove do Service endpoints (não mata).

**Uso:** app ainda está inicializando, dependency temporariamente indisponível.

```yaml
readinessProbe:
    httpGet:
        path: /ready
        port: 8080
    initialDelaySeconds: 5
    periodSeconds: 5
```

**Diferença crítica:** liveness **reinicia**, readiness **remove do load balancer**. Não confunda.

### Startup probe (K8s 1.16+)

**"Ainda está iniciando?"** Enquanto startup probe não retorna OK, liveness e readiness são **desabilitadas**.

**Uso:** apps que demoram muito para iniciar (Java com JVM warmup, carregamento de ML models).

```yaml
startupProbe:
    httpGet:
        path: /healthz
        port: 8080
    failureThreshold: 30     # 30 * periodSeconds = tempo total
    periodSeconds: 10
```

### Probe types

```yaml
# HTTP
httpGet:
    path: /healthz
    port: 8080
    httpHeaders:
        - name: X-Custom-Header
          value: foo

# TCP
tcpSocket:
    port: 5432

# Command
exec:
    command: ["sh", "-c", "pg_isready -U postgres"]

# gRPC (K8s 1.24+)
grpc:
    port: 9090
    service: "my.service"
```

---

## Resource management

### Requests e limits

```yaml
resources:
    requests:
        memory: "256Mi"
        cpu: "250m"     # 0.25 CPU
    limits:
        memory: "512Mi"
        cpu: "500m"     # 0.5 CPU
```

**Requests** — garantia mínima. Scheduler usa para decidir onde colocar o Pod.

**Limits** — máximo. Se ultrapassar:

- **CPU** — throttled (limitado, não morre)
- **Memory** — OOM killed

**Unidades:**

- CPU: `1` = 1 core, `500m` = 0.5 core, `100m` = 0.1 core
- Memory: `256Mi` (mebibytes), `1Gi` (gibibytes), `512M` (megabytes)

### QoS classes

K8s classifica Pods baseado em requests/limits:

| Classe | Condição | Eviction |
| --- | --- | --- |
| **Guaranteed** | Todos os containers têm `requests == limits` (tanto CPU quanto memory) | Último a ser evicted |
| **Burstable** | Pelo menos um container tem requests, mas != limits | Meio |
| **BestEffort** | Sem requests nem limits | Primeiro a ser evicted |

**Recomendação:** use `Guaranteed` ou `Burstable` em produção. Sempre defina `requests`.

### Horizontal Pod Autoscaler (HPA)

Escala réplicas baseado em métricas:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
    name: myapp-hpa
spec:
    scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: myapp
    minReplicas: 2
    maxReplicas: 10
    metrics:
        - type: Resource
          resource:
              name: cpu
              target:
                  type: Utilization
                  averageUtilization: 70
        - type: Resource
          resource:
              name: memory
              target:
                  type: Utilization
                  averageUtilization: 80
```

**HPA precisa de metrics-server** instalado no cluster.

**Custom metrics** (via Prometheus Adapter): escalar baseado em requests/s, queue depth, latência, etc.

### Vertical Pod Autoscaler (VPA)

Ajusta requests/limits automaticamente. Menos usado que HPA.

### Pod Disruption Budget (PDB)

Garante mínimo de réplicas durante operações de manutenção:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
    name: myapp-pdb
spec:
    minAvailable: 2     # ou maxUnavailable: 1
    selector:
        matchLabels:
            app: myapp
```

---

## Networking

### Cluster networking model

K8s impõe 3 requisitos:

1. **Todos os Pods podem se comunicar** sem NAT
2. **Todos os nodes podem se comunicar** com os Pods
3. **Cada Pod tem IP próprio** (no cluster)

Implementado via **CNI (Container Network Interface)** plugins: Calico, Cilium, Flannel, Weave, AWS VPC CNI.

**Em 2026, Cilium (eBPF-based) é o mais popular** em clusters novos — performance melhor, observability built-in, NetworkPolicies avançadas.

### Service discovery via DNS

Cada Service tem um FQDN:

```
<service>.<namespace>.svc.cluster.local
```

Exemplos:

- `postgres.default.svc.cluster.local`
- `api.production.svc.cluster.local`
- Dentro do mesmo namespace: `postgres`
- Mesmo cluster: `postgres.default`

### NetworkPolicy

Firewall no nível de Pods. Por default, **tudo é permitido**. NetworkPolicies negam o que não é explicitamente allowed.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
    name: api-policy
spec:
    podSelector:
        matchLabels:
            app: api
    policyTypes:
        - Ingress
        - Egress
    ingress:
        - from:
              - podSelector:
                    matchLabels:
                        app: frontend
          ports:
              - protocol: TCP
                port: 8080
    egress:
        - to:
              - podSelector:
                    matchLabels:
                        app: postgres
          ports:
              - protocol: TCP
                port: 5432
        - to:
              - namespaceSelector: {}
          ports:
              - protocol: UDP
                port: 53      # DNS
```

**Regra de segurança em produção:** default-deny + políticas explícitas.

### Service mesh (Istio, Linkerd)

Adiciona recursos avançados via sidecar proxy (Envoy):

- **mTLS automático** entre serviços
- **Traffic management** (canary, A/B, shifting)
- **Observability** (tracing, metrics distributed)
- **Circuit breaking** e retries

**Custo:** complexidade significativa, overhead de CPU/memória, learning curve.

**Quando usar:** muitos serviços (>20), requisitos de segurança (mTLS), traffic management complexo. Para apps pequenos, **overhead não se justifica**.

---

## Storage

### PersistentVolume (PV) e PersistentVolumeClaim (PVC)

**PV** — volume de fato (disco EBS, NFS, etc.). Criado pelo admin ou dinamicamente.

**PVC** — request de storage pelo usuário. "Preciso de 10Gi, ReadWriteOnce".

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
    name: data-pvc
spec:
    accessModes:
        - ReadWriteOnce
    resources:
        requests:
            storage: 10Gi
    storageClassName: standard
```

**Access modes:**

- **ReadWriteOnce (RWO)** — um node lê/escreve. Mais comum.
- **ReadOnlyMany (ROX)** — múltiplos nodes leem
- **ReadWriteMany (RWX)** — múltiplos nodes leem/escrevem. Precisa de filesystem distribuído (NFS, CephFS).
- **ReadWriteOncePod (RWOP)** — apenas um Pod (K8s 1.29+)

### StorageClass

Define como PVs são provisionados dinamicamente:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
    name: fast-ssd
provisioner: ebs.csi.aws.com
parameters:
    type: gp3
    iops: "3000"
    throughput: "125"
reclaimPolicy: Delete
allowVolumeExpansion: true
```

### CSI drivers

Container Storage Interface — plugins para diversos backends: AWS EBS, GCP PD, Azure Disk, Ceph, Longhorn, etc.

---

## Config management

### Kubectl — basics

```bash
# Contextos
kubectl config get-contexts
kubectl config use-context my-cluster
kubectl config current-context

# Namespace default do contexto
kubectl config set-context --current --namespace=staging

# Aplicar manifests
kubectl apply -f deployment.yaml
kubectl apply -f ./k8s/        # diretório inteiro
kubectl apply -k ./overlays/prod/  # Kustomize

# Ver recursos
kubectl get pods
kubectl get pods -o wide
kubectl get pods -A          # todos namespaces
kubectl get deployments,services,configmaps

# Descrever
kubectl describe pod myapp-xyz
kubectl describe deployment myapp

# Logs
kubectl logs myapp-xyz
kubectl logs myapp-xyz -c sidecar
kubectl logs -f myapp-xyz
kubectl logs myapp-xyz --previous
kubectl logs -l app=myapp --all-containers

# Exec
kubectl exec -it myapp-xyz -- sh
kubectl exec -it myapp-xyz -c app -- bash

# Port forward
kubectl port-forward pod/myapp-xyz 8080:80
kubectl port-forward svc/myapp 8080:80
kubectl port-forward deployment/myapp 8080:80

# Delete
kubectl delete pod myapp-xyz
kubectl delete -f deployment.yaml
kubectl delete deployment myapp --cascade=foreground

# Scale
kubectl scale deployment myapp --replicas=5

# Rollout
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp

# Debug
kubectl debug pod/myapp-xyz -it --image=busybox
kubectl debug node/node-1 -it --image=ubuntu

# Explain
kubectl explain pod.spec.containers
kubectl explain deployment --recursive

# Dry-run (validar sem aplicar)
kubectl apply -f file.yaml --dry-run=client
kubectl apply -f file.yaml --dry-run=server
```

### Kustomize

Gerenciador de configuração built-in no kubectl. Overlay-based, sem templating.

```
k8s/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── replicas-patch.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── prod/
        ├── kustomization.yaml
        └── replicas-patch.yaml
```

```yaml
# base/kustomization.yaml
resources:
    - deployment.yaml
    - service.yaml

# overlays/prod/kustomization.yaml
resources:
    - ../../base
replicas:
    - name: myapp
      count: 5
images:
    - name: myapp
      newTag: 1.2.3
configMapGenerator:
    - name: app-config
      literals:
          - LOG_LEVEL=warn
```

```bash
kubectl apply -k overlays/prod
```

**Vantagem:** sem templating, YAML validado pelo K8s, composável.

### Helm

Package manager do K8s. Templates + values.

```
my-chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── charts/          # dependências
```

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: {{ .Release.Name }}
spec:
    replicas: {{ .Values.replicaCount }}
    template:
        spec:
            containers:
                - name: app
                  image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
                  ports:
                      - containerPort: {{ .Values.service.port }}
```

```bash
helm install myapp ./my-chart --values values-prod.yaml
helm upgrade myapp ./my-chart --set image.tag=1.2.4
helm rollback myapp 1
helm uninstall myapp
```

**Helm vs Kustomize:**

| | Helm | Kustomize |
| --- | --- | --- |
| Abordagem | Template-based | Overlay-based |
| Curva | Média | Baixa |
| Validação | Após template | YAML direto |
| Releases | Sim | Não |
| Ecosystem | Enorme | Menor |
| Uso | Pacotes redistribuíveis | Config interna |

**Em 2026:** ambos são válidos. Use **Helm** para charts públicos (Nginx Ingress, Cert Manager, Prometheus). Use **Kustomize** para seus próprios manifests.

### GitOps — ArgoCD / Flux

Git como fonte de verdade. Controller observa repositório e aplica no cluster.

**Fluxo:**

```
Developer → PR → Review → Merge →
    ArgoCD observa git → Detecta diff → Sincroniza cluster
```

**Vantagens:**

- Audit trail (git log)
- Rollback via git revert
- Self-healing (controller reverte mudanças manuais)
- Declarativo end-to-end

**ArgoCD** é o mais popular em 2026. Interface web ótima, multi-cluster, suporte a Helm/Kustomize.

---

## RBAC e segurança

### Role-Based Access Control

K8s controla quem pode fazer o quê via **Role** (permissões em namespace) ou **ClusterRole** (permissões cluster-wide), bound via **RoleBinding** ou **ClusterRoleBinding**.

```yaml
# Role
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
    namespace: production
    name: pod-reader
rules:
    - apiGroups: [""]
      resources: ["pods"]
      verbs: ["get", "watch", "list"]

---
# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
    namespace: production
    name: read-pods
subjects:
    - kind: User
      name: alice
      apiGroup: rbac.authorization.k8s.io
    - kind: ServiceAccount
      name: my-sa
      namespace: production
roleRef:
    kind: Role
    name: pod-reader
    apiGroup: rbac.authorization.k8s.io
```

### ServiceAccount

Identidade para Pods (não users humanos). Cada Pod tem um SA default, ou você especifica:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
    name: my-app-sa
    namespace: production

---
apiVersion: apps/v1
kind: Deployment
metadata:
    name: myapp
spec:
    template:
        spec:
            serviceAccountName: my-app-sa
```

**Uso:** apps que precisam falar com a API do K8s (operators, controllers). Princípio de mínimo privilégio.

### Pod Security Standards

Substituiu PodSecurityPolicy (deprecated). 3 níveis:

- **Privileged** — sem restrições
- **Baseline** — evita escalation, mas permite user workloads
- **Restricted** — baseline + hardened (non-root, read-only root FS, etc.)

```yaml
apiVersion: v1
kind: Namespace
metadata:
    name: my-ns
    labels:
        pod-security.kubernetes.io/enforce: restricted
```

**Recomendação:** use `restricted` em produção, `baseline` em dev.

### Security Context

```yaml
spec:
    securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
        seccompProfile:
            type: RuntimeDefault
    containers:
        - name: app
          securityContext:
              allowPrivilegeEscalation: false
              capabilities:
                  drop: ["ALL"]
              readOnlyRootFilesystem: true
```

---

## Observabilidade

### Logs

**K8s não agrega logs nativamente.** Padrão: container escreve em stdout/stderr → kubelet armazena → agente coleta.

**Stack comum:**

- **Fluent Bit** / **Fluentd** — coleta
- **Elasticsearch** / **Loki** — armazena
- **Kibana** / **Grafana** — visualiza

```bash
# Logs rápidos
kubectl logs pod/myapp
kubectl logs -l app=myapp --all-containers --prefix
kubectl logs deployment/myapp -f
stern myapp        # ferramenta para tailing multi-pod
```

### Metrics — Prometheus

De facto padrão. Coleta métricas via HTTP pull.

**Stack:**

- **Prometheus** — coleta e armazena
- **kube-state-metrics** — métricas sobre objetos K8s
- **node-exporter** — métricas de hardware
- **Grafana** — dashboards
- **Alertmanager** — alertas

Aplicações expõem `/metrics` endpoint (Spring Boot Actuator + Micrometer, Node prom-client, etc.).

Ver [[Spring Boot]] (Actuator) para detalhes.

### Tracing — OpenTelemetry

Trace distribuído de requests através de múltiplos serviços.

**Stack:**

- **OpenTelemetry SDK** na aplicação
- **OpenTelemetry Collector** (agent)
- **Jaeger** ou **Tempo** — backend

### Observability operators

- **kube-prometheus-stack** (Helm) — Prometheus + Grafana + Alertmanager + exporters
- **Loki** — logs
- **Tempo** — traces
- **OpenTelemetry Operator**

---

## Deployment strategies

### Rolling update (default)

```yaml
strategy:
    type: RollingUpdate
    rollingUpdate:
        maxSurge: 25%
        maxUnavailable: 0
```

K8s substitui Pods gradualmente. Zero downtime se `maxUnavailable: 0`.

### Recreate

```yaml
strategy:
    type: Recreate
```

Mata todos, depois cria novos. **Downtime** — usar quando versões são incompatíveis (schema DB).

### Blue-Green

Duas versões rodando, switch de Service label:

```
Blue (v1, 10 replicas) ← 100% tráfego
Green (v2, 10 replicas)

# Deploy v2, valida, aponta Service para Green
# Rollback = aponta de volta para Blue
```

**Vantagens:** rollback instantâneo, testes em produção.
**Desvantagens:** 2x recursos durante transição.

**Ferramentas:** Argo Rollouts, Flagger.

### Canary

Pequena porcentagem de tráfego vai para nova versão, gradualmente aumenta:

```
Stable v1 (90% tráfego, 9 replicas)
Canary v2 (10% tráfego, 1 replica)
```

**Benefícios:** minimiza blast radius, permite validar em produção.

**Ferramentas:** Argo Rollouts, Flagger, service mesh (Istio, Linkerd).

```yaml
# Argo Rollouts example
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
    name: myapp
spec:
    replicas: 10
    strategy:
        canary:
            steps:
                - setWeight: 10
                - pause: {duration: 5m}
                - setWeight: 25
                - pause: {duration: 5m}
                - setWeight: 50
                - pause: {duration: 10m}
                - setWeight: 100
```

---

## Troubleshooting

### Pod em Pending

```bash
kubectl describe pod myapp-xyz
```

**Causas comuns:**

- Sem recursos (CPU/memory requests maiores que nodes disponíveis)
- Taints não tolerados
- Affinity rules impossíveis
- PVC não pode ser provisionado
- ImagePullBackOff (imagem não existe ou sem credenciais)

### Pod em CrashLoopBackOff

```bash
kubectl logs myapp-xyz --previous
kubectl describe pod myapp-xyz
```

**Causas:**

- App crasha no startup (config errado, dependência indisponível)
- Liveness probe failing (ou probe config errado)
- OOMKilled — memory limit muito baixo
- Signal not handled

### OOMKilled

```bash
kubectl describe pod myapp-xyz | grep -A 5 "Last State"
```

**Fix:** aumentar `memory` limit, ou otimizar o app.

### Service sem endpoints

```bash
kubectl get endpoints my-service
```

Se vazio, selector não está casando com labels dos Pods.

```bash
kubectl get pods --show-labels
kubectl get svc my-service -o yaml | grep selector
```

### Ingress não funciona

1. Ingress controller instalado?
2. `ingressClassName` correto?
3. DNS apontando para LB do Ingress?
4. TLS cert válido?

### Slow rolling update

- `maxSurge` e `maxUnavailable` muito conservadores
- Readiness probe demorada
- Resource limits muito apertados

---

## Patterns de produção

### 1. Resource requests obrigatórios

Nunca deploye sem requests. Scheduler precisa para alocar corretamente.

### 2. Probes bem configurados

- **Liveness** — apenas para detectar deadlocks reais (não falha transiente)
- **Readiness** — para ready state real (DB conectado, cache quente)
- **Startup** — apps com startup lento

### 3. Graceful shutdown

```yaml
spec:
    terminationGracePeriodSeconds: 60
    containers:
        - name: app
          lifecycle:
              preStop:
                  exec:
                      command: ["/bin/sh", "-c", "sleep 15"]   # drain window
```

App captura SIGTERM e fecha graceful.

### 4. Pod anti-affinity

Espalha réplicas por nodes diferentes (HA):

```yaml
affinity:
    podAntiAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                  matchLabels:
                      app: myapp
              topologyKey: kubernetes.io/hostname
```

### 5. PDB + HPA

Garantir disponibilidade durante manutenção + auto-scaling.

### 6. GitOps

Tudo versionado. Sem `kubectl edit` em produção.

### 7. Network Policies default-deny

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
    name: default-deny-all
spec:
    podSelector: {}
    policyTypes:
        - Ingress
        - Egress
```

Depois adiciona políticas explícitas.

### 8. Immutable tags

Use `myapp:1.2.3`, não `myapp:latest`. Ou melhor, digest `myapp@sha256:...`.

---

## Armadilhas comuns

- **`latest` em imagens** — sem reprodutibilidade
- **Sem requests/limits** — QoS BestEffort, primeiro a ser evicted
- **Liveness como readiness** — app é morto quando deveria ser removido do LB
- **Probe sem `initialDelaySeconds`** — probe falha durante startup
- **PVC `ReadWriteOnce` com multi-replica Deployment** — só funciona em 1 node
- **Rolling update sem readiness probe** — K8s acha que pod está pronto, envia tráfego cedo
- **`maxUnavailable: 25%`** com 2 replicas — 1 fica down
- **Services sem selector** — não encontra Pods
- **ConfigMap/Secret não remountado em update** — precisa reiniciar Pod (ou usar reloader)
- **Secret em plain YAML no git** — usar Sealed Secrets ou External Secrets
- **Deploy em namespace errado** — context/namespace errado
- **Kubectl apply sem `-k` em Kustomize** — manifest só, sem overlays
- **`kubectl delete` em produção** — risco alto, use GitOps
- **Sem PDB** — drain do node bem tira tudo
- **Sem pod anti-affinity** — todas as réplicas no mesmo node
- **Recursos iguais para dev e prod** — dev over-provisioned, prod under
- **Memory limit muito baixo** — OOMKilled
- **CPU throttling não monitorado** — app lento sem OOM
- **Ingress sem TLS** — tráfego inseguro
- **NetworkPolicy muito restritiva** — quebra DNS (precisa allowar kube-dns)
- **StatefulSet em vez de Deployment quando não precisa** — complexidade desnecessária
- **HPA sem metrics-server** — não funciona
- **Edit manual em vez de git** — drift
- **Sem monitoring de costs** — surprise cloud bill
- **Cluster muito pequeno** — pods pending frequentemente
- **`default` namespace para tudo** — sem isolamento

---

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
- [[System Design]] — K8s em architecture
- [[Spring Boot]] — apps Java em K8s
- [[Node.js]] — apps Node em K8s
- [[WSL, Docker e Kubernetes]] — setup em Windows
- [[Banco de dados]] — StatefulSets, operators
- [[Arquitetura de Software]] — microservices patterns
