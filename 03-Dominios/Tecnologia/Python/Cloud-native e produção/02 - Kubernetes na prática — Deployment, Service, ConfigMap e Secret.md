---
title: "Kubernetes na prática — Deployment, Service, ConfigMap e Secret"
created: 2026-07-12
type: concept
fase: magus
status: seedling
publish: true
tags:
  - python
  - kubernetes
  - producao
  - cloud-native
aliases:
  - "Deployment Kubernetes Python"
  - "Service ClusterIP Python"
  - "ConfigMap e Secret Python"
  - "Manifests Kubernetes FastAPI"
---

# Kubernetes na prática — Deployment, Service, ConfigMap e Secret

> [!abstract] TL;DR
> A imagem Docker de 180 MB que o [[03-Dominios/Tecnologia/Python/Observabilidade e produção/07 - Deploy básico — Dockerfile e CI-CD|Galho 17 nota 07]] produziu não roda sozinha em lugar nenhum — alguém precisa dizer a um cluster **quantas cópias** subir, **como** rotear tráfego até elas, e **de onde** vêm as variáveis de ambiente que a aplicação espera. Essas três perguntas — mais uma quarta, sobre o que fazer com dado sensível — têm nomes fixos no Kubernetes: `Deployment` (réplicas + template do Pod + probes que consomem o contrato `/health`/`/ready` do [[03-Dominios/Tecnologia/Python/Observabilidade e produção/06 - Health checks e probes|Galho 17 nota 06]]), `Service` (o DNS interno estável que substitui a URL fixa que o [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/05 - Service discovery na prática|Galho 15 nota 05]] já usou), `ConfigMap` (variáveis não sensíveis) e `Secret` (variáveis sensíveis — com o aviso desconfortável de que "Secret" só quer dizer base64, não criptografia). Esta nota aplica os quatro aos dois serviços da trilha — Tarefas e Notificações — com YAML real, funcional, comentado linha a linha onde importa.

## A cena: a imagem existe, mas "rodar em produção" ainda não significa nada

O time do serviço de Tarefas termina o [[03-Dominios/Tecnologia/Python/Observabilidade e produção/index|Galho 17]] com um artefato de verdade: uma imagem Docker de 180 MB, publicada em `ghcr.io/org/tarefas-service:a3f9c21`, testada, rodando como usuário não-root, com `/health` e `/ready` respondendo corretamente. `docker run` funciona perfeitamente na máquina de qualquer desenvolvedor. Mas "funciona no meu Docker local" e "está em produção" são coisas categoricamente diferentes — produção significa múltiplas réplicas (uma cópia sozinha é um ponto único de falha), significa um endereço estável que outros serviços conseguem alcançar mesmo quando réplicas sobem e descem, significa variáveis de ambiente injetadas sem hardcode na imagem, e significa que dado sensível — a credencial do Postgres, o `client_secret` OAuth2 que o [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/04 - Cliente de API Gateway — autenticação serviço-a-serviço|Galho 15 nota 04]] usa para chamar o serviço de Notificações — nunca aparece em texto claro num arquivo versionado no Git.

Nenhuma dessas quatro coisas é responsabilidade do `Dockerfile`. Elas são responsabilidade de quatro objetos do Kubernetes, declarados em YAML, aplicados ao cluster via `kubectl apply` (ou, na prática de produção, via um pipeline de GitOps que este galho não desenvolve). O resto desta nota percorre os quatro, nessa ordem: `Deployment` primeiro, porque é o objeto que de fato faz o Pod existir; `Service` em seguida, porque só faz sentido depois que existe algo para apontar; `ConfigMap` e `Secret` por último, porque ambos são consumidos *de dentro* do `Deployment` — a ordem de leitura reflete a ordem de dependência real entre as peças.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9", "primaryBorderColor": "#2E5C8A", "lineColor": "#4A90D9"}}}%%
flowchart TB
    subgraph CFG["Config — lida pelo Deployment"]
        CM["ConfigMap<br/>LOG_LEVEL, ENVIRONMENT"]
        SEC["Secret<br/>DATABASE_URL, OAUTH2_CLIENT_SECRET"]
    end

    DEP["Deployment<br/>tarefas-service<br/>replicas: 3"]
    P1["Pod 1"]
    P2["Pod 2"]
    P3["Pod 3"]
    SVC["Service (ClusterIP)<br/>tarefas-service.default.svc.cluster.local"]
    CLIENT["notificacoes-service<br/>(cliente httpx)"]

    CM -->|"envFrom: configMapRef"| DEP
    SEC -->|"envFrom: secretRef"| DEP
    DEP -->|"cria e mantém"| P1
    DEP --> P2
    DEP --> P3
    SVC -->|"roteia via label selector"| P1
    SVC --> P2
    SVC --> P3
    CLIENT -->|"DNS estável, IPs mudam"| SVC

    style DEP fill:#4A90D9,color:#fff
    style SVC fill:#7ED321,color:#000
    style SEC fill:#F5A623,color:#000
```

O diagrama acima já entrega a leitura inteira desta nota em uma imagem: `ConfigMap`/`Secret` alimentam o `Deployment`, o `Deployment` mantém um conjunto de Pods vivos, e o `Service` é a fachada estável — o único endereço que qualquer cliente, dentro ou fora do cluster, precisa conhecer — por trás da qual os Pods individuais podem nascer, morrer e ser substituídos sem que ninguém do lado de fora perceba.

> [!question]- Por que não existe um objeto único "app Python rodando"?
> Porque cada objeto resolve um problema ortogonal aos outros, e separar essas responsabilidades é o que torna o sistema operável em partes. `Deployment` decide *quantas* réplicas e *como* elas sobem; `Service` decide *como alcançá-las*; `ConfigMap`/`Secret` decidem *de onde vem a configuração*. Um time pode trocar o `Service` de `ClusterIP` para outro tipo sem tocar no `Deployment`; pode girar um Secret sem rebuildar a imagem; pode escalar réplicas sem reconfigurar rede nenhuma. A separação — a mesma filosofia de responsabilidade única que qualquer código bem desenhado já segue — é deliberada, não um acidente de design do Kubernetes.

## Deployment: réplicas, template do Pod e o contrato dos probes

Um `Deployment` não cria Pods diretamente — ele declara um **estado desejado** ("eu quero 3 réplicas deste template de Pod rodando sempre") e delega a um controller interno do Kubernetes a tarefa de reconciliar a realidade com essa declaração, continuamente, sem intervenção manual. Se um Pod morre (nó falha, processo trava, alguém deleta manualmente por engano), o controller do `Deployment` percebe a divergência entre "3 desejadas" e "2 existentes" e cria um Pod novo, sem que ninguém precise rodar nenhum comando.

```yaml
# deployment-tarefas.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tarefas-service
  labels:
    app: tarefas-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tarefas-service
  template:
    metadata:
      labels:
        app: tarefas-service
    spec:
      containers:
        - name: tarefas-service
          image: ghcr.io/org/tarefas-service:a3f9c21
          ports:
            - containerPort: 8000

          # --- Config injetada do ambiente (seções seguintes) ---
          envFrom:
            - configMapRef:
                name: tarefas-service-config
            - secretRef:
                name: tarefas-service-secrets

          # --- Contrato de saúde — consome os endpoints do Galho 17 nota 06 ---
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10

          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 2
            periodSeconds: 5
            failureThreshold: 3
```

Três blocos merecem atenção deliberada. Primeiro, `spec.selector.matchLabels` e `spec.template.metadata.labels` precisam **casar exatamente** — é assim que o `Deployment` sabe quais Pods são "seus", e é o mesmo par de labels que o `Service`, na próxima seção, vai reusar para saber para onde rotear tráfego. Segundo, a imagem referenciada — `ghcr.io/org/tarefas-service:a3f9c21` — usa a tag pelo `github.sha`, não `latest`, exatamente a decisão que o [[03-Dominios/Tecnologia/Python/Observabilidade e produção/07 - Deploy básico — Dockerfile e CI-CD|pipeline CI/CD do Galho 17]] já fixou: cada Pod criado por este manifest roda um commit rastreável, nunca "o que quer que `latest` signifique agora". Terceiro — e o ponto novo que este galho acrescenta ao que o Galho 17 já ensinou — os blocos `livenessProbe`/`readinessProbe` são a peça de infraestrutura que finalmente **consome** o contrato que a [[03-Dominios/Tecnologia/Python/Observabilidade e produção/06 - Health checks e probes|nota 06 do Galho 17]] deixou pronto no código: o mesmo YAML que aquela nota já mostrou como exemplo de "para onde isso vai" agora está, de fato, dentro de um `Deployment` real.

> [!tip] `readinessProbe` mais frequente e mais tolerante que `livenessProbe` não é acidente
> Repare nos números: `readinessProbe` verifica a cada 5 segundos e só age depois de 3 falhas seguidas (`failureThreshold: 3`); `livenessProbe` verifica a cada 10 segundos, sem `failureThreshold` explícito (o padrão do Kubernetes é 3, mas com intervalo maior, o efeito é uma reação mais lenta). A assimetria é proposital, e já foi justificada em profundidade na [[03-Dominios/Tecnologia/Python/Observabilidade e produção/06 - Health checks e probes|nota 06 do Galho 17]]: falha de readiness só tira o Pod da rotação de tráfego (reversível, barato, vale reagir rápido), falha de liveness mata e recria o processo (destrutivo, caro se disparado por um blip passageiro, vale ser mais conservador).

> [!warning] Esquecer o `livenessProbe`/`readinessProbe` no Deployment não é "modo simples" — é modo sem rede de segurança
> **O que acontece:** sem essas duas seções, o Kubernetes volta ao comportamento mais primitivo possível — considerar o Pod "pronto" assim que a porta TCP aceita conexão, o mesmo cenário que o incidente de abertura da [[03-Dominios/Tecnologia/Python/Observabilidade e produção/06 - Health checks e probes|nota 06 do Galho 17]] já descreveu em detalhe: pods recém-criados recebem tráfego antes do pool de conexão com o banco terminar de abrir, e um processo travado num deadlock nunca é reiniciado automaticamente, porque nada está checando se ele ainda responde. **Por quê:** o `Deployment`, por si só, só sabe reconciliar *quantidade* de Pods — ele não sabe, sem esses dois blocos, distinguir "Pod de pé mas ainda aquecendo" de "Pod genuinamente pronto para tráfego real", nem "processo travado" de "processo saudável". Os endpoints `/health`/`/ready` existem no código exatamente para dar essa informação ao orquestrador; sem os blocos de probe no manifest, o código expõe o contrato, mas ninguém o lê. **Como evitar:** todo `Deployment` de produção declara os dois blocos, apontando para os endpoints já construídos no Galho 17 — não há custo real em declará-los (os endpoints já existem), só o risco de esquecer.

## Service: DNS interno estável — o que substitui a URL fixa via httpx

Um `Deployment` mantém Pods vivos, mas cada Pod tem seu próprio IP interno, que **muda** toda vez que aquele Pod é substituído — um rolling update, um nó que falha, um `kubectl delete pod` acidental, qualquer um desses eventos troca o IP de baixo do tapete. Nenhum cliente deveria guardar o IP de um Pod específico — seria como guardar o número de telefone de um funcionário específico em vez do número geral da empresa. O `Service` resolve exatamente isso: dá um **nome DNS estável** a um conjunto de Pods que muda o tempo todo.

```yaml
# service-tarefas.yaml
apiVersion: v1
kind: Service
metadata:
  name: tarefas-service
spec:
  type: ClusterIP
  selector:
    app: tarefas-service
  ports:
    - port: 80
      targetPort: 8000
```

O `spec.selector` — `app: tarefas-service` — é o elo com o `Deployment` da seção anterior: qualquer Pod que carregue essa label (todos os Pods criados pelo `Deployment`, porque o `template.metadata.labels` já declarou essa mesma label) entra automaticamente na lista de destinos deste `Service`, sem nenhuma referência explícita ao nome do `Deployment`. `type: ClusterIP` — o padrão, quando `type` é omitido — expõe o `Service` só dentro do cluster, o caso certo para comunicação serviço-a-serviço; expor um serviço para fora do cluster (`LoadBalancer`, `NodePort`, ou um `Ingress` por cima de um `ClusterIP`) é uma decisão de borda que este galho não desenvolve, porque nenhum dos dois serviços da trilha recebe tráfego externo direto — só o `notificacoes-service` recebendo chamadas do `tarefas-service`, e o `tarefas-service` recebendo tráfego de algum gateway já coberto no [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/04 - Cliente de API Gateway — autenticação serviço-a-serviço|Galho 15 nota 04]].

Uma vez aplicado, esse `Service` ganha um nome DNS resolvível dentro do cluster: `tarefas-service.default.svc.cluster.local` (ou, dentro do mesmo namespace `default`, o encurtamento `tarefas-service` já basta). Esse nome não muda nunca, enquanto o objeto `Service` existir — é exatamente o mecanismo que a [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/05 - Service discovery na prática|nota 05 do Galho 15]] já descreveu em profundidade, do ponto de vista do cliente Python que consome esse DNS.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9", "primaryBorderColor": "#2E5C8A", "lineColor": "#D0021B"}}}%%
sequenceDiagram
    participant Tarefas as tarefas-service<br/>(código Python)
    participant DNS as CoreDNS
    participant Svc as Service<br/>notificacoes-service
    participant PodA as Pod A
    participant PodB as Pod B

    Note over Tarefas: httpx.Client(base_url=<br/>settings.notificacoes_service_url)
    Tarefas->>DNS: resolve notificacoes-service.default.svc.cluster.local
    DNS-->>Tarefas: IP virtual do Service
    Tarefas->>Svc: GET /clientes/42/canal
    Svc->>PodA: roteia (kube-proxy)
    PodA-->>Tarefas: 200 OK

    Note over PodA,PodB: rolling update substitui Pod A<br/>o nome DNS não muda

    Tarefas->>Svc: próxima chamada
    Svc->>PodB: roteia pro Pod novo
    PodB-->>Tarefas: 200 OK
```

> [!question]- Isso muda alguma coisa no código Python que já existe?
> Nada. É esse o ponto central que a [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/05 - Service discovery na prática|nota 05 do Galho 15]] já entregou: o `httpx.Client` do `tarefas-service` recebe `notificacoes_service_url` de uma variável de configuração — antes dessa nota, essa variável já podia apontar para `http://notificacoes-service.default.svc.cluster.local` em produção e `http://localhost:8001` em desenvolvimento, mesmo sem o manifest `Service` estar aplicado ainda. O que esta nota acrescenta é o **objeto de cluster que faz esse nome DNS existir de verdade** — antes dele, a URL na configuração apontava para um nome que ninguém resolvia; depois dele, o mesmo nome resolve para Pods reais e vivos, sem tocar em uma linha do cliente HTTP.

Substituir uma URL fixa (um IP hardcoded, ou um endereço que aponta para uma única instância) pela URL do `Service` é o que elimina o cenário mais comum de acoplamento acidental entre serviços: sem o `Service`, qualquer replanejamento de infraestrutura — mover o `notificacoes-service` para outro nó, escalar de 2 para 5 réplicas, substituir um Pod que caiu — quebraria a URL fixa que o `tarefas-service` guardou. Com o `Service`, o nome nunca muda; só o conjunto de IPs por trás dele muda, e essa mudança é absorvida inteiramente pelo `kube-proxy` e pelo CoreDNS, uma camada abaixo de qualquer código Python.

## ConfigMap: variáveis de ambiente não sensíveis

Um `ConfigMap` guarda pares chave-valor de configuração que **não** precisam de sigilo — nível de log, nome do ambiente, timeouts não críticos, feature flags. É um objeto simples, sem criptografia nem controle de acesso especial além do RBAC padrão do namespace.

```yaml
# configmap-tarefas.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tarefas-service-config
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  NOTIFICACOES_SERVICE_URL: "http://notificacoes-service.default.svc.cluster.local"
```

Repare que a própria URL do `Service` da seção anterior — a que a [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/05 - Service discovery na prática|nota 05 do Galho 15]] já leu via `pydantic_settings.BaseSettings`, com `notificacoes_service_url` como o nome canônico da propriedade — entra aqui como uma chave de `ConfigMap`, não hardcoded em lugar nenhum do código. É a mesma peça de configuração descrita naquela nota, só que agora vinda de um objeto do cluster em vez de um `.env` local — o código Python nunca soube (e não precisa saber) a diferença entre as duas origens, porque ambas chegam da mesma forma: uma variável de ambiente lida por `Settings`.

O `Deployment` da primeira seção já referenciou este `ConfigMap` inteiro via `envFrom.configMapRef` — cada chave em `data` vira, automaticamente, uma variável de ambiente dentro do container, sem precisar listar uma por uma no manifest do `Deployment`. A alternativa — `env` com `configMapKeyRef`, chave por chave — existe e é útil quando só uma ou duas variáveis específicas de um `ConfigMap` maior são necessárias, mas `envFrom` é o padrão mais comum quando o `ConfigMap` já foi desenhado especificamente para um único serviço, como no exemplo acima.

> [!tip] `ConfigMap` não é o lugar para lógica condicional — só valores
> É tentador tratar o `ConfigMap` como um lugar para "configuração complexa" — um JSON aninhado, uma lista de regras. Funciona tecnicamente (o valor de uma chave pode ser qualquer string, inclusive um blob JSON inteiro), mas cada camada de complexidade dentro de um valor de `ConfigMap` é uma camada que o `pydantic-settings` do lado Python precisa parsear manualmente, perdendo a validação automática que campos simples (`LOG_LEVEL: str`, `ENVIRONMENT: Literal["production", "staging", "development"]`) já ganham de graça. Prefira múltiplas chaves simples a uma chave complexa sempre que a decisão for sua.

## Secret: variáveis sensíveis — e o aviso sobre o que "Secret" realmente significa

Um `Secret` tem a mesma forma de um `ConfigMap` — pares chave-valor, consumidos do mesmo jeito pelo `Deployment` — mas existe para dado que não pode aparecer em texto claro num manifest versionado: a string de conexão do Postgres com credencial embutida, o `client_secret` OAuth2 que o `tarefas-service` usa para autenticar contra o `notificacoes-service`, exatamente o segredo que a [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/04 - Cliente de API Gateway — autenticação serviço-a-serviço|nota 04 do Galho 15]] já mostrou como `CLIENT_SECRET`, ali comentado como "em produção, vem de um secret manager" — este `Secret` do Kubernetes é exatamente esse "secret manager" prometido naquela nota, agora de fato configurado.

```yaml
# secret-tarefas.yaml
apiVersion: v1
kind: Secret
metadata:
  name: tarefas-service-secrets
type: Opaque
data:
  DATABASE_URL: cG9zdGdyZXNxbDovL2FwcF91c2VyOnMzY3IzdEBwb3N0Z3Jlcy1wcmltYXJ5OjU0MzIvdGFyZWZhcw==
  OAUTH2_CLIENT_SECRET: czNncjNkby1kby1vcmRlcnMtc2VydmljZQ==
```

À primeira vista, os valores em `data` parecem criptografados — uma string ilegível, cheia de caracteres aparentemente aleatórios. Não são. `cG9zdGdyZXNxbDovL2FwcF91c2VyOnMzY3IzdEBwb3N0Z3Jlcy1wcmltYXJ5OjU0MzIvdGFyZWZhcw==` é, literalmente, `postgresql://app_user:s3cr3t@postgres-primary:5432/tarefas` codificado em **base64** — reversível por qualquer pessoa com `echo '<valor>' | base64 -d` no terminal, sem chave nenhuma, sem senha nenhuma.

> [!warning] `Secret` do Kubernetes não é criptografia — é ofuscação, e a distinção importa de verdade
> **O que acontece:** um time trata um `Secret` como se fosse um cofre — "está no objeto `Secret`, está seguro" — e comete o mesmo erro do exemplo `data` acima: qualquer pessoa (ou processo, ou pipeline) com permissão de leitura no namespace roda `kubectl get secret tarefas-service-secrets -o yaml`, copia o valor de `DATABASE_URL`, decodifica com um comando de uma linha, e tem a credencial do banco em texto claro. Um `Secret` versionado por engano num repositório Git — o erro mais comum, porque o YAML *parece* seguro à primeira vista — expõe a credencial pra qualquer um com acesso ao histórico do repositório, para sempre, mesmo depois de removido de um commit posterior. **Por quê:** base64 é uma **codificação**, não uma cifra — existe para garantir que dados binários arbitrários caibam num campo de texto YAML, não para esconder o conteúdo de quem tem os bytes em mãos. O Kubernetes, por padrão, também não criptografa `Secret`s em repouso no `etcd` (o banco de dados interno do cluster) a menos que o cluster tenha sido explicitamente configurado com **encryption at rest** — uma configuração de operação de cluster, fora do escopo desta nota, e frequentemente esquecida em clusters gerenciados por times pequenos. **Como evitar:** tratar `Secret` do Kubernetes como "um `ConfigMap` com controle de acesso um pouco mais restrito por padrão (RBAC), não como cofre criptografado" é a mentalidade correta. Para segurança real de segredos em produção, as ferramentas certas são outras: **Sealed Secrets** (Bitnami) — criptografa o `Secret` *antes* dele entrar no Git, e só o controller dentro do cluster consegue decifrar, tornando seguro versionar o YAML criptografado — ou um **External Secrets Operator**, que busca o valor real de um cofre externo (AWS Secrets Manager, HashiCorp Vault, Google Secret Manager) em runtime e o materializa como `Secret` nativo do Kubernetes só dentro do cluster, nunca no Git. Nenhuma das duas é desenvolvida a fundo aqui — ambas resolvem exatamente esse problema, e a escolha entre elas depende de infraestrutura que já existe no time (se já há um Vault, External Secrets Operator; se não, Sealed Secrets tem menos peças móveis).

> [!question]- Então por que o Kubernetes molda `Secret` como um objeto separado de `ConfigMap`, se a proteção real é praticamente a mesma?
> Porque o `Secret`, apesar de não ser criptografia forte por padrão, ainda carrega proteções que o `ConfigMap` não tem: o Kubernetes evita logar o conteúdo de `Secret`s em alguns comandos (`kubectl describe pod` mostra os *nomes* das chaves de um Secret montado, nunca os valores, ao contrário de um `ConfigMap`, cujo conteúdo aparece integralmente), o controle de RBAC costuma ser configurado de forma mais restrita para o recurso `secrets` do que para `configmaps`, e o objeto sinaliza intenção — qualquer engenheiro lendo o manifest sabe, pelo `kind: Secret`, que aquele dado exige cuidado redobrado, mesmo antes de entender os detalhes de codificação. É proteção de superfície e de convenção, não criptografia — mas não é zero, e não invalida o aviso anterior: para dado genuinamente sensível em produção, `Secret` puro nunca é suficiente sozinho.

O `Deployment` consome o `Secret` exatamente como consome o `ConfigMap` — mesmo `envFrom`, agora com `secretRef` em vez de `configMapRef`:

```yaml
          envFrom:
            - configMapRef:
                name: tarefas-service-config
            - secretRef:
                name: tarefas-service-secrets
```

Do ponto de vista do código Python, a distinção entre `ConfigMap` e `Secret` desaparece completamente — ambos chegam como variáveis de ambiente comuns, lidas pelo mesmo `pydantic_settings.BaseSettings` que a [[03-Dominios/Tecnologia/Python/Segurança/06 - Secrets e configuração segura|nota 06 do Galho 11]] já construiu. A diferença de tratamento é toda do lado do cluster — quem pode ler o objeto, como ele é (ou não) protegido em repouso — nunca do lado da aplicação.

## O manifest completo — tarefas-service, ponta a ponta

Juntando os quatro objetos das seções anteriores num único arquivo (na prática, geralmente separados em arquivos distintos ou geridos por Helm/Kustomize, mas concatenados aqui para leitura em sequência):

```yaml
# tarefas-service.yaml — manifest completo, funcional

apiVersion: v1
kind: ConfigMap
metadata:
  name: tarefas-service-config
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  NOTIFICACOES_SERVICE_URL: "http://notificacoes-service.default.svc.cluster.local"

---
apiVersion: v1
kind: Secret
metadata:
  name: tarefas-service-secrets
type: Opaque
data:
  DATABASE_URL: cG9zdGdyZXNxbDovL2FwcF91c2VyOnMzY3IzdEBwb3N0Z3Jlcy1wcmltYXJ5OjU0MzIvdGFyZWZhcw==
  OAUTH2_CLIENT_SECRET: czNncjNkby1kby1vcmRlcnMtc2VydmljZQ==

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tarefas-service
  labels:
    app: tarefas-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tarefas-service
  template:
    metadata:
      labels:
        app: tarefas-service
    spec:
      containers:
        - name: tarefas-service
          image: ghcr.io/org/tarefas-service:a3f9c21
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: tarefas-service-config
            - secretRef:
                name: tarefas-service-secrets
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 2
            periodSeconds: 5
            failureThreshold: 3

---
apiVersion: v1
kind: Service
metadata:
  name: tarefas-service
spec:
  type: ClusterIP
  selector:
    app: tarefas-service
  ports:
    - port: 80
      targetPort: 8000
```

O separador `---` entre cada bloco é a sintaxe padrão do YAML para múltiplos documentos num único arquivo — `kubectl apply -f tarefas-service.yaml` cria os quatro objetos numa única chamada. A ordem no arquivo não importa para o Kubernetes (ele resolve dependências entre objetos independentemente da posição no YAML), mas a ordem escolhida aqui — `ConfigMap`/`Secret` primeiro, `Deployment` depois, `Service` por último — segue a mesma lógica de leitura desta nota inteira: config antes de quem a consome, rede depois de quem ela expõe.

O serviço de Notificações segue exatamente o mesmo padrão de quatro objetos — `notificacoes-service-config`, `notificacoes-service-secrets`, um `Deployment` com seu próprio `image`/`replicas`, e um `Service` cujo nome (`notificacoes-service`) é justamente o hostname que o `ConfigMap` do `tarefas-service`, acima, já referenciou em `NOTIFICACOES_SERVICE_URL`. Repetir o YAML completo do segundo serviço aqui seria redundância mecânica — a estrutura é idêntica, só nomes e valores mudam.

> [!question]- Isso é o suficiente para produção de verdade?
> Não, e esta nota não finge que é. `resources.requests`/`resources.limits` (o que acontece quando um Pod excede memória, o **OOMKill**), estratégia de `RollingUpdate` para zero downtime durante um deploy, e autoscaling baseado em métrica ainda faltam — são, respectivamente, o assunto das três notas seguintes deste galho. O que esta nota entrega é a base mínima funcional: um serviço que sobe com múltiplas réplicas, tem um endereço estável, recebe configuração correta e é monitorado pelos probes certos — o alicerce sobre o qual as próximas três notas constroem.

## Verificando que os quatro objetos de fato funcionam juntos

Depois de `kubectl apply -f tarefas-service.yaml`, um punhado de comandos confirma que a cadeia inteira — config chegando ao container, probes sendo consultados, DNS resolvendo — está de fato funcionando, não só declarada em YAML:

```bash
# Os Pods existem e passaram no readinessProbe?
# READY 3/3 significa: 3 réplicas, todas prontas para tráfego.
kubectl get pods -l app=tarefas-service

# As variáveis de ambiente chegaram no container, vindas do
# ConfigMap e do Secret via envFrom?
kubectl exec deploy/tarefas-service -- env | grep -E "LOG_LEVEL|ENVIRONMENT|DATABASE_URL"

# O Service tem endpoints (IPs de Pods saudáveis) por trás dele?
# Uma lista vazia aqui, mesmo com Pods "Running", é sinal de que
# o selector do Service não bate com as labels do template do Pod.
kubectl get endpoints tarefas-service

# O DNS interno resolve o nome do Service a partir de dentro do
# cluster? (rodado de dentro de outro Pod, ou um Pod de debug)
kubectl run debug --rm -it --image=busybox -- nslookup tarefas-service.default.svc.cluster.local
```

> [!warning] `kubectl get endpoints` vazio com Pods "Running" é o sintoma mais comum de um selector errado
> **O que acontece:** os Pods sobem, `kubectl get pods` mostra `Running` e `READY 3/3` — mas `kubectl get endpoints tarefas-service` devolve uma lista vazia, e nenhum tráfego chega aos Pods através do `Service`. **Por quê:** o `Service.spec.selector` não bate exatamente com as labels em `Deployment.spec.template.metadata.labels` — um erro de digitação (`app: tarefas` no `Service` contra `app: tarefas-service` no `Deployment`), ou um label a mais/a menos de um dos dois lados. O `Service` não avisa desse descasamento com um erro explícito; ele só nunca encontra Pods que casem com o `selector`, e a lista de `endpoints` fica silenciosamente vazia. **Como evitar:** manter `Service.spec.selector` e `Deployment.spec.template.metadata.labels` como a mesma fonte — na prática, copiar o valor exato, nunca reescrever de memória — e sempre confirmar com `kubectl get endpoints` depois de aplicar um `Service` novo, antes de assumir que "aplicou sem erro" significa "está roteando tráfego".

## ConfigMap vs Secret: mesma forma, tratamento diferente

Vale fixar numa tabela a diferença de tratamento entre os dois objetos, já que a forma de consumo — via `envFrom`, do lado do `Deployment` — é idêntica, e é fácil confundir "consumido igual" com "protegido igual":

| Aspecto | ConfigMap | Secret |
| --- | --- | --- |
| Codificação dos valores | Texto claro | Base64 (não é criptografia) |
| Visível em `kubectl describe` | Sim, valores completos | Não, só nomes das chaves |
| Criptografia em repouso no etcd | Nunca (não se aplica) | Só se o cluster tiver `encryption at rest` configurado explicitamente |
| Uso típico | `LOG_LEVEL`, `ENVIRONMENT`, URL de outro `Service` | Credencial de banco, `client_secret` OAuth2, chave de API |
| Seguro para versionar YAML puro no Git | Sim | **Não** — só a versão criptografada por Sealed Secrets, ou nenhuma versão (External Secrets Operator busca em runtime) |
| Consumo pelo `Deployment` | `envFrom.configMapRef` | `envFrom.secretRef` |

A leitura mais importante da tabela é a penúltima linha: um `ConfigMap` pode viver tranquilamente versionado, em texto claro, no mesmo repositório Git que guarda o resto dos manifests — não há nada ali que precise de proteção. Um `Secret` bruto, no formato mostrado nesta nota, **não pode** — mesmo que o base64 pareça, à primeira vista, oferecer alguma proteção visual. É essa linha que justifica a existência de Sealed Secrets e External Secrets Operator como complemento, não substituto, do objeto `Secret` nativo.

## Casos práticos

### Cenário 1: rolling update de uma tag antiga para uma nova

O time do serviço de Notificações termina um fix e publica uma imagem nova via o pipeline do [[03-Dominios/Tecnologia/Python/Observabilidade e produção/07 - Deploy básico — Dockerfile e CI-CD|Galho 17 nota 07]] — a tag muda de `ghcr.io/org/notificacoes-service:7c1a90d` para `ghcr.io/org/notificacoes-service:e42f3b1`. Atualizar o campo `image` no `Deployment` (via `kubectl set image` ou reaplicando o YAML com a tag nova) dispara, automaticamente, uma substituição gradual dos Pods — o controller do `Deployment` cria Pods novos com a imagem nova, espera o `readinessProbe` de cada um passar antes de considerá-lo pronto, e só então remove um Pod antigo da rotação. Nenhum comando adicional é necessário para esse comportamento básico acontecer — ele é o padrão de qualquer `Deployment`, mesmo sem configuração explícita de estratégia de rollout; o ajuste fino desse comportamento (quantos Pods novos sobem de uma vez, quantos antigos podem ficar indisponíveis simultaneamente) é o assunto da [[04 - Rolling deploy sem downtime no Kubernetes|nota 04 deste galho]].

### Cenário 2: girar (rotate) o `client_secret` OAuth2 sem rebuildar a imagem

O `client_secret` que o `Secret` `tarefas-service-secrets` guarda, referenciado pela [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/04 - Cliente de API Gateway — autenticação serviço-a-serviço|nota 04 do Galho 15]], precisa ser trocado periodicamente por política de segurança — um giro (rotation) de credencial. Como o valor vem inteiramente do `Secret`, e nunca da imagem Docker, girar essa credencial não exige rebuildar nem republicar a imagem: basta atualizar o `Secret` no cluster (`kubectl apply -f secret-tarefas.yaml` com o valor novo, já codificado em base64) e reiniciar os Pods existentes para que peguem a variável de ambiente atualizada — env vars são fixadas no momento em que o container sobe, então um `Secret` atualizado sozinho não propaga para Pods já rodando, só para os próximos que subirem. É exatamente esse desacoplamento entre "o que está na imagem" e "o que vem do ambiente" que o [[03-Dominios/Tecnologia/Python/Segurança/06 - Secrets e configuração segura|Galho 11 nota 06]] já justificou como princípio de configuração segura — e é a mesma razão pela qual a credencial nunca deveria estar hardcoded na imagem para começo de conversa.

## Em entrevista

Uma pergunta comum de entrevista sênior é "descreva os objetos básicos do Kubernetes que você usaria para colocar um serviço HTTP em produção" — e a resposta fraca cita os nomes sem explicar a relação entre eles ("Deployment, Service, ConfigMap, Secret" como uma lista solta). A resposta forte nomeia a relação de dependência: `ConfigMap`/`Secret` alimentam o `Deployment` via `envFrom`; o `Deployment` reconcilia um número desejado de réplicas contra a realidade, consultando `livenessProbe`/`readinessProbe` para decidir quando reiniciar versus quando só pausar tráfego; o `Service` dá a esse conjunto de Pods, que muda o tempo todo, um nome DNS que nunca muda. E sabe apontar, sem que perguntem, o aviso sobre `Secret`: base64 não é criptografia, e produção de verdade usa Sealed Secrets ou um External Secrets Operator por cima — um candidato que trata `Secret` como "seguro por definição" revela que nunca leu a própria documentação da ferramenta que diz usar.

## Síntese

Quatro objetos, quatro responsabilidades que não se sobrepõem: `Deployment` mantém um número de réplicas do Pod vivo, consultando os endpoints `/health`/`/ready` que o código Python já expõe desde o Galho 17 para decidir entre reiniciar (liveness) e pausar tráfego (readiness); `Service` dá a esse conjunto de Pods instável um nome DNS estável, a mesma peça que a nota de Service Discovery do Galho 15 já descreveu do lado do cliente — aqui, finalmente, o objeto de cluster que faz esse nome existir de verdade; `ConfigMap` guarda o que não precisa de sigilo; `Secret` guarda o que precisa, com o aviso essencial de que "Secret" no Kubernetes é ofuscação em base64, não criptografia — segurança real de segredo em produção exige Sealed Secrets ou um External Secrets Operator por cima, ferramentas que resolvem exatamente essa lacuna sem exigir que o time reinvente gestão de cofre do zero. Os dois serviços da trilha — Tarefas e Notificações — agora têm manifests completos e funcionais; o que ainda falta — dimensionamento de recursos, deploy sem downtime, autoscaling — é o assunto das três notas seguintes.

## Como explicar em inglês

> "A Kubernetes deployment for an HTTP service rests on four objects with non-overlapping responsibilities. The `Deployment` reconciles a desired replica count against reality, and consults `livenessProbe`/`readinessProbe` — pointed at `/health` and `/ready` endpoints the application code already exposes — to decide between restarting a pod (liveness) and just pulling it out of traffic rotation (readiness). The `Service` gives that constantly-changing set of pods a stable DNS name — `tarefas-service.default.svc.cluster.local` — so no client ever hardcodes a pod IP. `ConfigMap` and `Secret` both feed the `Deployment` as environment variables via `envFrom`, split by sensitivity rather than format. The one thing worth being explicit about in an interview: Kubernetes `Secret` is base64-encoded, not encrypted — anyone with read access to the namespace, or a `Secret` accidentally committed to Git, can decode it in one command. Real secret management in production means Sealed Secrets or an External Secrets Operator sitting on top of the native `Secret` object, not relying on it alone."

| PT | EN |
|----|----|
| Réplica | Replica |
| Modelo de Pod | Pod template |
| Rótulo / seletor | Label / selector |
| Verificação de vivacidade | Liveness probe |
| Verificação de prontidão | Readiness probe |
| Nome DNS estável | Stable DNS name |
| Mapa de configuração | ConfigMap |
| Segredo | Secret |
| Codificação (não criptografia) | Encoding (not encryption) |
| Criptografia em repouso | Encryption at rest |
| Segredo selado | Sealed Secret |
| Operador de segredos externos | External Secrets Operator |

## O que vem a seguir

Com o `Deployment` e o `Service` no lugar, os Pods do serviço de Tarefas sobem, recebem configuração correta e são monitorados pelos probes certos — mas nada, ainda, impede que um Pod consuma toda a memória do nó onde roda, nem garante que o kernel mate esse processo de forma previsível quando isso acontece.

- [[03 - Recursos e limites — requests, limits e OOMKill|03 — Recursos e limites: requests, limits e OOMKill]] — `resources.requests`/`resources.limits` no mesmo bloco `containers` desta nota, e o que muda quando um Pod excede o `limits.memory`.

## Veja também

- [[index|Cloud-native e produção (Galho 18)]] — MOC deste galho.
- [[01 - Panorama — orquestrar de verdade|01 — Panorama: orquestrar de verdade]] — mapa do galho e por que orquestrar de fato é diferente do contrato que o código já expõe.
- [[03-Dominios/Tecnologia/Python/Observabilidade e produção/06 - Health checks e probes|Galho 17 nota 06 — Health checks e probes]] — o contrato `/health`/`/ready` que os `livenessProbe`/`readinessProbe` desta nota consomem.
- [[03-Dominios/Tecnologia/Python/Observabilidade e produção/07 - Deploy básico — Dockerfile e CI-CD|Galho 17 nota 07 — Deploy básico: Dockerfile e CI/CD]] — a imagem Docker que o `Deployment` desta nota referencia.
- [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/05 - Service discovery na prática|Galho 15 nota 05 — Service discovery na prática]] — o lado cliente do DNS interno que o `Service` desta nota faz existir de verdade.
- [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/04 - Cliente de API Gateway — autenticação serviço-a-serviço|Galho 15 nota 04 — Cliente de API Gateway]] — o `client_secret` OAuth2 que o `Secret` desta nota agora armazena de fato.
- [[03-Dominios/Tecnologia/Python/Segurança/06 - Secrets e configuração segura|Galho 11 nota 06 — Secrets e configuração segura]] — `pydantic-settings`, o lado Python que lê tanto `ConfigMap` quanto `Secret` da mesma forma.
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/11 - Config e recursos no Kubernetes|Java — Config e recursos no Kubernetes]] — trilha irmã, mesmo par ConfigMap/Secret, ótica de relaxed binding do Spring Boot em vez de pydantic-settings.

## Fontes

- Kubernetes. *Deployments*. kubernetes.io. https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ (acessado em 2026-07-12) — semântica de `replicas`, `selector`, template do Pod, e como o controller reconcilia estado desejado.
- Kubernetes. *Service*. kubernetes.io. https://kubernetes.io/docs/concepts/services-networking/service/ (acessado em 2026-07-12) — tipos de `Service` (`ClusterIP` e demais), como o `selector` conecta `Service` a Pods.
- Kubernetes. *ConfigMaps*. kubernetes.io. https://kubernetes.io/docs/concepts/configuration/configmap/ (acessado em 2026-07-12) — consumo via `envFrom`/`env`, arquivos montados, limitações de tamanho.
- Kubernetes. *Secrets*. kubernetes.io. https://kubernetes.io/docs/concepts/configuration/secret/ (acessado em 2026-07-12) — `type: Opaque`, codificação base64 (não criptografia), proteções de RBAC e exibição em `kubectl describe`.
- Kubernetes. *Configure Liveness, Readiness and Startup Probes*. kubernetes.io. https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/ (acessado em 2026-07-12) — sintaxe de `livenessProbe`/`readinessProbe`, `initialDelaySeconds`/`periodSeconds`/`failureThreshold`.
- Bitnami. *Sealed Secrets*. github.com/bitnami-labs/sealed-secrets. https://github.com/bitnami-labs/sealed-secrets (acessado em 2026-07-12) — criptografia de `Secret` antes de versionar no Git, mencionado sem desenvolver a fundo.
- External Secrets Operator. *Documentation*. external-secrets.io. https://external-secrets.io/latest/ (acessado em 2026-07-12) — sincronização de `Secret` nativo a partir de um cofre externo (Vault, AWS Secrets Manager), mencionado sem desenvolver a fundo.
- [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/05 - Service discovery na prática|Service discovery na prática]] — Galho 15 nota 05, DNS interno do Kubernetes Service do lado do cliente.
- [[03-Dominios/Tecnologia/Python/Observabilidade e produção/06 - Health checks e probes|Health checks e probes]] — Galho 17 nota 06, contrato `/health`/`/ready` consumido pelos probes desta nota.

Consultado em 2026-07-12.
