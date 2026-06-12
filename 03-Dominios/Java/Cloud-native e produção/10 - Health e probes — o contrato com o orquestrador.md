---
title: "Health e probes — o contrato com o orquestrador"
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
  - actuator
aliases:
  - "Health probes"
  - "Liveness e readiness"
---

# Health e probes — o contrato com o orquestrador

> [!abstract] TL;DR
> O endpoint `/actuator/health` do **Spring Boot Actuator** é o ponto onde o orquestrador (Kubernetes) pergunta à sua aplicação como ela está. Em um cluster, o Actuator auto-ativa dois grupos de health (`management.endpoint.health.probes.enabled` é `true` por padrão): a **liveness probe** (`/actuator/health/liveness`) responde "estou vivo?" — se falhar, o pod é reiniciado; a **readiness probe** (`/actuator/health/readiness`) responde "posso atender agora?" — se falhar, o pod é tirado do balanceamento sem reinício. A regra de ouro: **liveness nunca depende de checagem externa** (DB fora do ar não deve disparar reinício em loop). Não existe startup probe dedicado no Spring Boot — para boot lento, reusa-se a liveness via configuração do Kubernetes. Estados `DOWN` e `OUT_OF_SERVICE` retornam HTTP `503`.

## O que é

Um **probe** é uma sonda: o Kubernetes faz uma requisição HTTP periódica a um caminho da sua aplicação e interpreta o resultado para decidir o que fazer com o pod. O **Spring Boot Actuator** expõe esses caminhos prontos.

O endpoint base é `/actuator/health`. Sobre ele, o Boot constrói dois **grupos de health** voltados a Kubernetes:

- `/actuator/health/liveness` — a **sonda de vivacidade** (liveness probe).
- `/actuator/health/readiness` — a **sonda de prontidão** (readiness probe).

Esses grupos são alimentados pela abstração `ApplicationAvailability`, que mantém dois estados internos:

- `LivenessState`: `CORRECT` (a aplicação está viva e não deve ser reiniciada) ou `BROKEN` (está quebrada e deve ser reiniciada).
- `ReadinessState`: `ACCEPTING_TRAFFIC` (pronta para receber requisições) ou `REFUSING_TRAFFIC` (não deve receber tráfego agora).

> [!info] Fronteira com o Galho 8
> O **mecanismo** do Actuator — como a auto-configuração descobre health indicators, como os endpoints são expostos, como a observabilidade se encaixa — é assunto do Galho 8. Veja [[03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade|Actuator e observabilidade (Galho 8)]]. Esta nota trata do **uso operacional**: como esse mecanismo vira o contrato HTTP que o orquestrador consome em produção.

## Por que importa

Sem probes, o Kubernetes só sabe se o **processo** está rodando — não se a **aplicação** está saudável. Um pod pode estar com o processo vivo mas travado (deadlock, heap esgotado) e continuar recebendo tráfego, devolvendo erro a cada requisição. Probes fecham essa lacuna.

A distinção liveness/readiness é o coração do contrato:

- **Liveness** responde a pergunta de sobrevivência. Falha aqui = "este pod não tem mais conserto, reinicie". O orquestrador mata e recria o container.
- **Readiness** responde a pergunta de roteamento. Falha aqui = "estou vivo, mas não me mande tráfego ainda". O orquestrador tira o pod do `Service` (load balancer) sem reiniciá-lo; quando voltar a `ACCEPTING_TRAFFIC`, ele reentra no pool.

Confundir as duas é a fonte das piores falhas em produção. Uma liveness probe que checa o banco transforma uma indisponibilidade momentânea do DB em um **reinício em cascata** de toda a frota — exatamente quando você menos quer perder capacidade.

## Como funciona

### O endpoint `/actuator/health` e a exposição

Por padrão, o único endpoint do Actuator exposto sobre HTTP é o `health`. Isso é controlado por `management.endpoints.web.exposure.include`, cujo valor padrão é apenas `health`. Tudo o mais (`env`, `beans`, `metrics`, `heapdump`...) fica fechado até você incluir explicitamente.

Esse padrão restritivo é uma decisão de segurança: o contrato com o orquestrador precisa só do `health`, e expor o resto por engano vaza informação. Ampliar a exposição é uma escolha consciente, nunca o default.

### Liveness vs. readiness: os grupos, os estados e o auto-ligamento

A flag `management.endpoint.health.probes.enabled` tem default `true`, e os grupos de probe **auto-ativam** quando o Boot detecta que está rodando em um ambiente Kubernetes. Você raramente precisa ligá-los à mão; basta o ambiente.

Os dois caminhos mapeiam diretamente para os estados de `ApplicationAvailability`:

| Caminho | Estado fonte | Valores |
| --- | --- | --- |
| `/actuator/health/liveness` | `LivenessState` | `CORRECT` / `BROKEN` |
| `/actuator/health/readiness` | `ReadinessState` | `ACCEPTING_TRAFFIC` / `REFUSING_TRAFFIC` |

Durante o ciclo de vida da aplicação, o Boot transiciona esses estados sozinho: ao subir, a liveness vira `CORRECT` assim que o contexto está pronto, mas a readiness só vira `ACCEPTING_TRAFFIC` quando o servidor web começa de fato a aceitar requisições. No shutdown, a readiness volta a `REFUSING_TRAFFIC` antes de o servidor parar — é assim que o graceful shutdown drena tráfego.

### Sem startup probe dedicado e o `add-additional-paths`

O Spring Boot **não oferece um startup probe próprio**. Para aplicações de boot lento, a recomendação é **reusar a liveness HTTP probe** como startup probe na configuração do Kubernetes — com um `failureThreshold` alto o suficiente para cobrir a partida —, de modo que o orquestrador não mate o pod antes de ele terminar de subir.

Quando o Actuator roda em uma **porta de gerenciamento separada** (`management.server.port`), as probes ficam isoladas da porta principal. Para expô-las também na porta da aplicação, use `management.endpoint.health.probes.add-additional-paths: true`, que publica `/livez` (liveness) e `/readyz` (readiness) na porta principal do servidor.

Sobre os estados de health e seus códigos HTTP: `UP` e `UNKNOWN` retornam `200`; `DOWN` e `OUT_OF_SERVICE` retornam `503`. É o `503` que o Kubernetes lê como falha de probe.

| Estado de health | HTTP |
| --- | --- |
| `UP` | 200 |
| `UNKNOWN` | 200 |
| `DOWN` | 503 |
| `OUT_OF_SERVICE` | 503 |

## Na prática

Configuração do `application.yml` para um `order-service` rodando em Kubernetes:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health  # padrão; explícito por clareza, nunca "*" em prod
  endpoint:
    health:
      probes:
        enabled: true              # default true; auto-ativa em k8s
        add-additional-paths: true # publica /livez e /readyz na porta principal
      group:
        readiness:
          # readiness PODE checar dependências críticas para atender tráfego
          include: readinessState,db
        liveness:
          # liveness NUNCA depende de check externo
          include: livenessState
      show-details: when-authorized
```

Probes no `Deployment` do Kubernetes apontando para os grupos do Actuator:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  template:
    spec:
      containers:
        - name: order-service
          image: registry.example/order-service:1.0.0
          ports:
            - containerPort: 8080
          # boot lento: reusa a liveness como startup probe
          startupProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            failureThreshold: 30
            periodSeconds: 10        # tolera ~5 min de partida
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            periodSeconds: 10
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            periodSeconds: 10
            failureThreshold: 3
```

## Armadilhas

### (1) Liveness checando o banco → reinício em cascata

Incluir um health indicator de banco no grupo `liveness` é o erro clássico. Quando o DB fica indisponível por alguns segundos, **todas** as réplicas falham a liveness ao mesmo tempo, o Kubernetes reinicia **todas** elas, e o reinício simultâneo derruba qualquer chance de recuperação graciosa. Você transformou uma instabilidade momentânea do banco em uma queda total da aplicação. Liveness só deve refletir o estado interno do processo (`livenessState`), nunca dependência externa.

### (2) Readiness sem checar dependências essenciais

O espelho do erro anterior. Se a readiness não verifica as dependências sem as quais o serviço não consegue atender (por exemplo, um pool de conexões ainda não inicializado), o pod entra no balanceador antes de estar realmente pronto e devolve erro às primeiras requisições. Readiness **pode e deve** checar o que é crítico para servir tráfego — é o lugar certo para essas verificações, justamente porque a falha não reinicia o pod, só o tira do roteamento.

### (3) Expor todos os endpoints (`*`) em produção

Trocar o default `health` por `management.endpoints.web.exposure.include: "*"` por conveniência abre `env`, `beans`, `heapdump`, `mappings` e companhia. Em produção isso vaza configuração, variáveis de ambiente e até dumps de memória para quem alcançar a porta. Exponha só o necessário; se precisar de outros endpoints, inclua-os nominalmente e proteja-os com autenticação.

## Em entrevista

### Frase pronta (inglês)

In Spring Boot, the Actuator's `/actuator/health` endpoint is the contract between the application and the orchestrator. When running on Kubernetes the framework auto-enables two probe groups: the liveness probe answers "am I alive?" — if it fails, the pod is restarted — while the readiness probe answers "can I serve traffic right now?" — if it fails, the pod is removed from the load balancer without a restart. The cardinal rule is that the liveness probe must never depend on an external check such as the database; otherwise a brief outage would trigger a cascading restart of the whole fleet. Spring Boot has no dedicated startup probe, so for slow-starting apps you reuse the liveness HTTP probe as a startup probe with a high failure threshold, and `DOWN` or `OUT_OF_SERVICE` states map to HTTP 503, which Kubernetes reads as a failed probe.

### Vocabulário

| Português | Inglês |
| --- | --- |
| sonda de vivacidade | liveness probe |
| sonda de prontidão | readiness probe |
| disponibilidade da aplicação | application availability |
| recusando tráfego | refusing traffic |
| reinício em cascata | cascading restart |
| exposição de endpoint | endpoint exposure |

## Veja também

- [[03-Dominios/Java/Cloud-native e produção/11 - Config e recursos no Kubernetes|Config e recursos no Kubernetes]]
- [[03-Dominios/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|Graceful shutdown e deploy sem downtime]]
- [[03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade|Actuator e observabilidade (Galho 8)]]
- [[03-Dominios/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Spring Boot Reference — Actuator Endpoints, seção Kubernetes Probes: <https://docs.spring.io/spring-boot/reference/actuator/endpoints.html>
