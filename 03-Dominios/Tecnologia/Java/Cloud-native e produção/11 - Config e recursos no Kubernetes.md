---
title: "Config e recursos no Kubernetes"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - cloud-native
  - adepto
  - kubernetes
  - config
aliases:
  - "ConfigMap e Secret"
  - "Resource limits"
---

# Config e recursos no Kubernetes

> [!abstract] TL;DR
> O Kubernetes injeta config no seu app por **variáveis de ambiente** e **arquivos**, vindos de **ConfigMap** (não sensível) e **Secret** (sensível). O Spring Boot lê essas variáveis de ambiente direto pelas suas propriedades graças ao **relaxed binding**: `ORDER_DB_URL` vira `order.db.url` sem você escrever uma linha de glue code. Além da config, o Deployment declara **requests e limits** de CPU/memória — e o `limits.memory` é a fonte de verdade que a JVM lê via `MaxRAMPercentage`. Sua tarefa como dev é **consumir esse contrato**, não administrar o cluster.

## O que é

Imagine que você aluga um apartamento. Você não decide a voltagem da tomada, a pressão da água ou o horário do elevador de serviço — essas regras estão **afixadas no ambiente** pela administração do prédio. Você, inquilino, apenas **lê** essas regras e se adapta a elas. Você não administra o prédio.

Seu app rodando no Kubernetes é exatamente esse inquilino. A config — URL do banco, senha, feature flags, quanto de memória ele pode usar — não vem hardcoded na imagem Docker. Ela vem **do ambiente**, injetada pelo orquestrador no momento em que o container sobe. Esse é o princípio "config no ambiente" do [[03-Dominios/Tecnologia/Java/Cloud-native e produção/01 - Production-ready e cloud-native — a tese honesta|twelve-factor]]: a mesma imagem roda em dev, staging e produção, mudando só o que o ambiente afixa.

No Kubernetes, quem afixa essas regras são dois objetos:

- **ConfigMap** — armazena config **não confidencial** em pares chave-valor (URLs, timeouts, flags). Não oferece sigilo nem criptografia.
- **Secret** — armazena dados **sensíveis** (senhas, tokens, chaves). Conceitualmente é um ConfigMap "com cuidados extras" (acesso restrito, codificação base64, criptografia em repouso quando o cluster está configurado para isso).

Ambos viram, do ponto de vista do app, ou **variáveis de ambiente** ou **arquivos montados num diretório**. É só isso que seu app enxerga.

> [!note] Foco desta nota
> Aqui olhamos para a **ótica do app que consome o contrato**. Operar o cluster — `kubectl`, `Service`, `Ingress`, operators, `HPA` (autoescalonamento) — e operar um sistema de secrets de produção (Vault e afins) ficam **fora de escopo**. São responsabilidades de infraestrutura/plataforma, não do código Java.

## Por que importa

Em entrevista para vaga sênior, "como você externaliza config" é pergunta quase certa, e a resposta separa quem entende cloud-native de quem só sabe rodar `java -jar`. Três motivos práticos:

1. **Portabilidade.** Uma imagem, todos os ambientes. Se a config estivesse na imagem, você precisaria de uma imagem por ambiente — um pesadelo de build e de auditoria.
2. **Segurança.** Senha não pode estar no `application.yml` versionado no Git. Ela tem que vir de um Secret, injetado só em runtime, visível só para quem precisa.
3. **Estabilidade sob pressão.** Sem `requests` e `limits` corretos, seu pod ou é morto por `OOMKill` (estourou a memória) ou estrangula vizinhos consumindo CPU sem teto. E se a JVM não souber respeitar o `limits.memory`, ela calcula o heap como se tivesse a máquina inteira — e morre (ver [[03-Dominios/Tecnologia/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]]).

## Como funciona

### Variáveis de ambiente e relaxed binding

O jeito mais simples de o app receber config é por variável de ambiente. O Kubernetes injeta `ORDER_DB_URL=jdbc:postgresql://...` no container, e o Spring Boot resolve isso **automaticamente** para a propriedade `order.db.url`.

Esse mapeamento é o **relaxed binding** (vinculação relaxada). A regra é mecânica:

1. Tudo para minúsculo: `ORDER_DB_URL` → `order_db_url`
2. Underscore vira ponto: `order_db_url` → `order.db.url`
3. Casa com a propriedade canônica `order.db.url`

Por que existe? Porque a maioria dos sistemas operacionais **não permite ponto** em nome de variável de ambiente. Você não consegue exportar `order.db.url` como env var — mas consegue `ORDER_DB_URL`. O relaxed binding é a ponte entre o mundo de env vars (UPPER_SNAKE) e o mundo de propriedades Spring (kebab/dot).

> [!tip] A consequência prática
> Você **não escreve glue code**. Não há `System.getenv("ORDER_DB_URL")` espalhado pelo código. Você declara a propriedade canônica (de preferência em **kebab-case**, `order.db.url`) em `@ConfigurationProperties` ou `@Value`, e o ambiente preenche. O mesmo nome canônico casa com `application.yml`, com `--order.db.url=` na linha de comando e com `ORDER_DB_URL` no ambiente.

```java
@ConfigurationProperties("order.db")
public class OrderDbProperties {
    private String url;      // preenchido por ORDER_DB_URL
    private String username; // preenchido por ORDER_DB_USERNAME
    // getters/setters
}
```

### ConfigMap e Secret mapeados para o app

O ConfigMap/Secret existe no cluster; o Deployment **liga** esse objeto ao container. Há dois modos de consumo que importam para o dev Java:

- **Como variáveis de ambiente** — via `env` (uma chave por vez, com `configMapKeyRef`/`secretKeyRef`) ou `envFrom` (importa **todas** as chaves do objeto de uma vez, com `configMapRef`/`secretRef`). O `envFrom` é o mais usado: derrama o ConfigMap inteiro como env vars, e o relaxed binding cuida do resto.
- **Como arquivos montados** — o objeto vira um diretório onde cada chave é um arquivo. Útil para arquivos de propriedades inteiros ou certificados. Vantagem: arquivos montados **atualizam sozinhos** quando o ConfigMap muda; env vars não — env var é fixada no startup do pod e só muda com restart.

A escolha entre ConfigMap e Secret é por **sensibilidade do dado**, não por formato. URL pública e timeout → ConfigMap. Senha do banco e token de API → Secret. O app consome os dois do mesmo jeito (env var ou arquivo); a diferença de tratamento é toda do lado do cluster.

### Resource limits e MaxRAMPercentage

Além da config funcional, o Deployment declara **quanto de recurso** o container pode usar. São dois números por recurso:

- **`requests`** — o mínimo garantido. O scheduler usa isso para decidir em qual nó cabe o pod. É a reserva.
- **`limits`** — o teto rígido. Estourar `limits.memory` resulta em **OOMKill** (o kernel mata o processo). Estourar `limits.cpu` resulta em **throttling** (o processo é desacelerado, não morto).

O ponto crítico para Java: a JVM moderna (Java 10+, container-aware) lê o **`limits.memory`** do cgroup e dimensiona o heap a partir dele. A flag que controla a fração é a `-XX:MaxRAMPercentage`. Se `limits.memory` é 1Gi e `MaxRAMPercentage=75.0`, a JVM mira ~768Mi de heap, deixando o resto para metaspace, threads, buffers off-heap e o próprio overhead nativo.

> [!warning] A relação que mata em produção
> O `limits.memory` é a **fonte de verdade**. A JVM o respeita via `MaxRAMPercentage`. Quem fixa `-Xmx` num valor **maior ou igual** ao `limits.memory` quebra essa relação: a JVM acha que pode usar mais memória do que o cgroup permite, cresce o heap, e o kernel a mata por OOM antes de qualquer `OutOfMemoryError` Java aparecer. A regra de ouro é deixar o `limits.memory` mandar e usar `MaxRAMPercentage` — detalhado em [[03-Dominios/Tecnologia/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]].

## Na prática

Deployment **ilustrativo** de um `order-service`. Repare como ele junta as três peças: **probes** (o contrato de saúde — ver nota 10), **resources** (requests/limits) e **config** (via `envFrom` puxando ConfigMap e Secret).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
        - name: order-service
          image: registry.example.com/order-service:1.4.0
          ports:
            - containerPort: 8080
          # --- Config injetada do ambiente ---
          env:
            # heap dimensionado a partir do limits.memory
            - name: JAVA_TOOL_OPTIONS
              value: "-XX:MaxRAMPercentage=75.0"
          envFrom:
            - configMapRef:
                name: order-service-config   # config não sensível
            - secretRef:
                name: order-service-secrets  # senhas, tokens
          # --- Teto de recursos ---
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"   # fonte de verdade do heap da JVM
          # --- Contrato de saúde com o orquestrador ---
          startupProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            failureThreshold: 30
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            periodSeconds: 10
```

E o ConfigMap que o `envFrom` consome. Cada chave aqui vira uma variável de ambiente no container, e o relaxed binding a transforma em propriedade Spring:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-service-config
data:
  ORDER_DB_URL: "jdbc:postgresql://orders-db:5432/orders"  # -> order.db.url
  ORDER_DB_USERNAME: "order_app"                            # -> order.db.username
  ORDER_PAYMENT_TIMEOUT_MS: "3000"                          # -> order.payment.timeout-ms
  LOGGING_LEVEL_COM_EXAMPLE_ORDER: "INFO"                   # -> logging.level.com.example.order
```

Note que `ORDER_DB_PASSWORD` **não** está aqui — ela mora no Secret `order-service-secrets`, puxado pelo `secretRef`. O app consome as duas fontes de forma idêntica; só a procedência muda.

## Armadilhas

### (1) Pôr segredo num ConfigMap

ConfigMap **não oferece sigilo**. Os dados ficam em claro, qualquer um com acesso de leitura ao namespace os enxerga, e eles podem vazar em backups e dumps do etcd. Colocar senha, token ou chave privada num ConfigMap é o erro de segurança mais comum de quem está aprendendo. Senha vai em **Secret**, sempre. A regra mental: se você ficaria desconfortável vendo aquilo num `kubectl describe configmap` impresso no Slack, é Secret.

### (2) `-Xmx` brigando com o `limits.memory`

Fixar `-Xmx2g` num container com `limits.memory: 1Gi` é pedir OOMKill. A JVM vai tentar crescer o heap até 2Gi, o cgroup corta em 1Gi, o kernel mata o processo — e você nem vê um `OutOfMemoryError` no log, só o pod reiniciando misteriosamente. Deixe o `limits.memory` ser a fonte de verdade e dimensione com `-XX:MaxRAMPercentage`. Detalhado em [[03-Dominios/Tecnologia/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]].

### (3) Config sensível logada no startup

Frameworks e libs adoram logar a configuração efetiva ao subir ("starting with config: ..."). Se você tem `order.db.password` vindo de env var e algum log de debug despeja o ambiente ou as propriedades resolvidas, sua senha vai parar no agregador de logs em texto claro — onde times inteiros têm acesso. Cuidado redobrado com endpoints que expõem ambiente (como o `/actuator/env` do Spring Boot, que mascara segredos conhecidos mas não tudo) e com logs de nível DEBUG em produção. Trate o ambiente como potencialmente sensível e nunca o logue inteiro.

## Em entrevista

### Frase pronta (inglês)

In a Kubernetes environment, I externalize all configuration following the twelve-factor principle: the same container image runs everywhere, and the environment supplies the config. Non-sensitive values live in a **ConfigMap** and secrets live in a **Secret**, both injected into the container as environment variables — usually via `envFrom` — or mounted as files. Spring Boot's **relaxed binding** picks these up automatically, so an environment variable like `ORDER_DB_URL` maps straight to the `order.db.url` property with no glue code. On the resource side, I always declare **requests and limits**, and I let `limits.memory` be the source of truth for the heap by sizing it with `-XX:MaxRAMPercentage` instead of a hardcoded `-Xmx`, which otherwise fights the cgroup limit and gets the pod OOM-killed.

### Vocabulário

| Português | Inglês |
| --- | --- |
| mapa de configuração | ConfigMap |
| segredo | Secret |
| requisições e limites | requests and limits |
| vinculação relaxada | relaxed binding |
| variável de ambiente | environment variable |
| config externalizada | externalized config |
| morto por falta de memória | OOM-killed |
| estrangulamento (de CPU) | throttling |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/01 - Production-ready e cloud-native — a tese honesta|Production-ready e cloud-native (a tese)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/10 - Health e probes — o contrato com o orquestrador|Health e probes]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|Graceful shutdown e deploy sem downtime]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Spring Boot Reference — Externalized Configuration / Relaxed Binding: https://docs.spring.io/spring-boot/reference/features/external-config.html
- Kubernetes Documentation — ConfigMaps: https://kubernetes.io/docs/concepts/configuration/configmap/
- Kubernetes Documentation — Secrets: https://kubernetes.io/docs/concepts/configuration/secret/
- Kubernetes Documentation — Resource Management for Pods and Containers: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
