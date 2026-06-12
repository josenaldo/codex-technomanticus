---
title: "Actuator e observabilidade"
created: 2026-06-08
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - spring
  - magus
  - actuator
  - boot
aliases:
  - "Spring Actuator"
  - "Actuator"
---

# Actuator e observabilidade

> [!abstract] TL;DR
> O Spring Boot Actuator expõe endpoints HTTP (e JMX) que revelam o estado interno da aplicação em produção: saúde, métricas, beans, configurações, loggers e muito mais. Por padrão, apenas `/health` e `/info` ficam expostos via HTTP — todos os outros precisam ser habilitados explicitamente em `management.endpoints.web.exposure.include`. Métricas são coletadas via **Micrometer**, uma fachada que desacopla o código de qualquer backend (Prometheus, Datadog, InfluxDB…). Em ambientes Kubernetes, os endpoints `/actuator/health/liveness` e `/actuator/health/readiness` permitem que o orquestrador saiba se o pod deve ser reiniciado ou retirado de serviço.

## O que é

O **Spring Boot Actuator** é o módulo responsável por tornar a aplicação **observável em produção**. Ele adiciona endpoints de gerenciamento que permitem inspecionar e, em alguns casos, modificar o comportamento da aplicação em tempo de execução — sem precisar reimplantá-la.

A dependência é adicionada declarando o starter:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

O Actuator não é apenas um conjunto de URLs úteis. Ele é a ponte entre a aplicação e as ferramentas de operação: sistemas de monitoramento, plataformas de orquestração (Kubernetes), dashboards de métricas (Grafana), alertas (Alertmanager) e pipelines de observabilidade. Observabilidade distribuída completa — rastreamento distribuído, OpenTelemetry, correlação de traces — é tema do Galho 17: veja o [[03-Dominios/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|panorama de observabilidade de operação]] e o [[03-Dominios/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|OpenTelemetry Collector]].

## Por que importa

Sem o Actuator, a única forma de saber se uma aplicação está saudável é esperar ela cair ou receber uma reclamação do usuário. Com ele, a plataforma de operação pode:

- Checar a saúde proativamente antes de enviar tráfego (`/health`).
- Ajustar o nível de log em produção sem reiniciar (`/loggers`).
- Inspecionar quais beans foram criados e por quê (`/beans`, `/conditions`).
- Coletar métricas de JVM, pool de conexões, filas, tempos de resposta e qualquer medida de negócio que você instrumentar.

Para o nível **magus**, o ponto crítico não é saber que os endpoints existem, e sim entender **o que expor, para quem, e como instrumentar métricas de negócio** que vão além das métricas de infraestrutura geradas automaticamente.

Segurança de endpoints (autenticação e autorização do Actuator) é tema do galho [[03-Dominios/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Segurança]].

## Como funciona

### Endpoints principais

O Actuator registra uma série de endpoints no path `/actuator` (configurável). Cada endpoint tem um ID e pode ser habilitado/desabilitado e exposto ou não via HTTP ou JMX de forma independente.

| Endpoint          | O que faz                                                      |
|-------------------|----------------------------------------------------------------|
| `/health`         | Status de saúde da aplicação e de seus componentes            |
| `/info`           | Informações arbitrárias sobre a aplicação (versão, build…)    |
| `/metrics`        | Catálogo de métricas e valores individuais via `/metrics/{nome}` |
| `/loggers`        | Lista e altera dinamicamente o nível de log por logger        |
| `/conditions`     | Relatório de avaliação das condições de auto-configuration    |
| `/beans`          | Todos os beans registrados no `ApplicationContext`            |
| `/env`            | Propriedades de ambiente (filtradas para segredos)            |
| `/configprops`    | Propriedades de configuração ligadas a `@ConfigurationProperties` |
| `/mappings`       | Todos os request mappings registrados nos controllers         |
| `/prometheus`     | Métricas no formato Prometheus (requer `micrometer-registry-prometheus`) |
| `/threaddump`     | Snapshot das threads da JVM                                   |
| `/heapdump`       | Heap dump (arquivo binário)                                   |
| `/startup`        | Passos e tempos da inicialização da aplicação                 |
| `/httpexchanges`  | Histórico de trocas HTTP recentes (requer bean `HttpExchangeRepository`) |

> [!warning] Padrão seguro
> No Boot 3.x, apenas `health` e `info` são expostos via HTTP por padrão. Todos os demais precisam ser habilitados explicitamente — esse é o comportamento oposto do Boot 1.x, onde tudo ficava exposto por padrão.

### Exposição e segurança dos endpoints

A configuração de exposição controla **quais** endpoints ficam acessíveis via HTTP (ou JMX). Há duas dimensões ortogonais:

- **Habilitado** (`management.endpoint.<id>.enabled`): o endpoint existe ou não.
- **Exposto** (`management.endpoints.web.exposure.include/exclude`): o endpoint responde via HTTP.

```yaml
management:
  endpoints:
    web:
      base-path: /actuator            # path base (padrão: /actuator)
      exposure:
        include: "health,info,metrics,loggers,prometheus"
        # exclude: "env,beans"        # opcional: remove da exposição
  endpoint:
    health:
      show-details: when-authorized   # never | always | when-authorized
```

Para expor todos os endpoints (útil em ambiente de desenvolvimento):

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

> [!danger] Produção
> Nunca exponha `*` em produção sem proteção por autenticação. Endpoints como `/env`, `/heapdump` e `/beans` expõem informações sensíveis. Proteção com Spring Security é abordada no galho [[03-Dominios/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Segurança]].

### Health groups, liveness e readiness (Kubernetes)

O endpoint `/health` é composto de **`HealthIndicator`s** que o Actuator agrega automaticamente: banco de dados, broker de mensagens, disco, Redis e outros dependendo dos starters presentes.

Para ambientes Kubernetes, o Boot 3.x oferece dois **subgrupos de saúde** nativos que mapeiam diretamente para os probes do Kubernetes:

| Probe         | Endpoint                       | Significado                                          |
|---------------|--------------------------------|------------------------------------------------------|
| **Liveness**  | `/actuator/health/liveness`    | A aplicação está viva? Falha → Kubernetes reinicia o pod |
| **Readiness** | `/actuator/health/readiness`   | A aplicação está pronta para receber tráfego? Falha → Kubernetes remove o pod do balanceador |

Para ativar os probes:

```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true
  health:
    livenessState:
      enabled: true
    readinessState:
      enabled: true
```

> [!tip] Diferença crítica
> **Liveness** responde "o processo está funcionando" — se falhar, o pod é reiniciado. **Readiness** responde "consigo processar requisições agora" — se falhar durante uma janela de manutenção ou sobrecarga temporária, o pod é removido do balanceador mas **não** reiniciado. Confundir os dois causa reinicializações desnecessárias ou serviço degradado invisível.

**Custom `HealthIndicator`** permite injetar a sua própria verificação no status de `/health`. Basta implementar a interface `HealthIndicator` (ou estender `AbstractHealthIndicator`) e registrá-la como bean:

```java
@Component
public class OrderQueueHealthIndicator extends AbstractHealthIndicator {

    private final OrderQueueClient queueClient;

    public OrderQueueHealthIndicator(OrderQueueClient queueClient) {
        this.queueClient = queueClient;
    }

    @Override
    protected void doHealthCheck(Health.Builder builder) {
        long pending = queueClient.countPendingOrders();
        if (pending < 10_000) {
            builder.up()
                   .withDetail("pendingOrders", pending);
        } else {
            builder.down()
                   .withDetail("pendingOrders", pending)
                   .withDetail("threshold", 10_000);
        }
    }
}
```

O nome do indicador deriva do nome do bean: `orderQueue` → aparece em `/actuator/health` como `"orderQueue": { "status": "UP" }`.

### Micrometer como fachada de métricas

O **Micrometer** é a camada de abstração de métricas do Spring Boot — o equivalente ao SLF4J, mas para instrumentação. O código da aplicação registra medidas em termos de conceitos do Micrometer (`Counter`, `Timer`, `Gauge`, `DistributionSummary`), e o Micrometer delega para o backend configurado sem que o código de negócio precise saber qual é.

Backends suportados (cada um com seu próprio starter de registro): Prometheus, Datadog, InfluxDB, New Relic, CloudWatch, Dynatrace, Graphite, entre outros.

**Exemplo com Prometheus** (backend mais comum em ambientes open-source):

```xml
<!-- pom.xml -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "health,prometheus"
  metrics:
    tags:
      application: orders-service      # tag global em todas as métricas
      environment: production
```

Com essa configuração, `/actuator/prometheus` expõe todas as métricas no formato de texto que o Prometheus sabe raspar (`scrape`). O Prometheus coleta periodicamente, o Grafana visualiza.

Métricas geradas automaticamente incluem: JVM (heap, GC, threads), pool de conexões JDBC (`HikariCP`), tempo de resposta HTTP, consumo de CPU/memória do processo e métricas de cache (se presente).

## Na prática

**Configuração mínima de produção** com saúde detalhada e métricas para Prometheus:

```yaml
management:
  endpoints:
    web:
      base-path: /actuator
      exposure:
        include: "health,info,metrics,loggers,prometheus"
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true
  health:
    livenessState:
      enabled: true
    readinessState:
      enabled: true
  metrics:
    tags:
      application: orders-service
```

**Custom `HealthIndicator`** verificando a disponibilidade de um serviço externo:

```java
@Component
public class PaymentGatewayHealthIndicator extends AbstractHealthIndicator {

    private final PaymentGatewayClient gateway;

    public PaymentGatewayHealthIndicator(PaymentGatewayClient gateway) {
        this.gateway = gateway;
    }

    @Override
    protected void doHealthCheck(Health.Builder builder) {
        boolean reachable = gateway.ping();
        if (reachable) {
            builder.up().withDetail("gateway", "reachable");
        } else {
            builder.down().withDetail("gateway", "unreachable");
        }
    }
}
```

**Métrica de negócio** com Micrometer — contagem de pedidos processados:

```java
@Service
public class OrderService {

    private final Counter ordersProcessed;

    public OrderService(MeterRegistry registry) {
        this.ordersProcessed = Counter.builder("orders.processed")
                .description("Total de pedidos processados com sucesso")
                .tag("channel", "api")
                .register(registry);
    }

    public void processOrder(Order order) {
        // lógica de processamento…
        ordersProcessed.increment();
    }
}
```

## Armadilhas

**1. Expor todos os endpoints sem autenticação**

```yaml
# ERRADO em produção
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

Endpoints como `/env` listam variáveis de ambiente (incluindo senhas), `/heapdump` entrega o heap inteiro da JVM, e `/loggers` permite mudar o nível de log remotamente. Em produção, exponha apenas o necessário e proteja com Spring Security ([[03-Dominios/Java/Segurança/index|Galho 12 — Segurança]]).

**Fix**: listar explicitamente os endpoints necessários e colocar o path de gerenciamento em uma porta separada (`management.server.port=8081`) que não seja acessível externamente.

---

**2. Colocar lógica pesada dentro de `HealthIndicator`**

```java
// ERRADO — query completa a cada chamada ao /health
@Override
protected void doHealthCheck(Health.Builder builder) {
    long count = repository.countAll(); // SELECT COUNT(*) em tabela grande
    builder.up().withDetail("totalOrders", count);
}
```

O endpoint `/health` é chamado a cada probe do Kubernetes (tipicamente a cada 10-30 segundos). Queries caras ou I/O bloqueante degradam a aplicação e podem causar timeouts no próprio health check.

**Fix**: limite o `HealthIndicator` a verificações rápidas (ping, `SELECT 1`, contagem em cache). Se precisar de informação agregada, use `/metrics` com uma gauge atualizada assincronamente.

---

**3. Confundir liveness com readiness**

```yaml
# ERRADO — usar o mesmo endpoint para liveness e readiness
livenessProbe:
  httpGet:
    path: /actuator/health
readinessProbe:
  httpGet:
    path: /actuator/health
```

Se o `HealthIndicator` de um banco de dados downstream falhar, o Kubernetes vai reiniciar o pod achando que ele está morto — quando na verdade ele só está aguardando o banco voltar.

**Fix**: use `/actuator/health/liveness` para liveness (apenas estado interno do processo) e `/actuator/health/readiness` para readiness (dependências externas que afetam a capacidade de servir requisições).

## Em entrevista

### Frase pronta (inglês)

- "Spring Boot Actuator exposes management endpoints over HTTP — the most important ones in production are `/health` for liveness and readiness probes, `/metrics` backed by Micrometer, and `/loggers` for on-the-fly log level changes. By default, only `health` and `info` are exposed; anything else must be explicitly included."

- "Micrometer is to metrics what SLF4J is to logging: a vendor-neutral facade. You instrument with `Counter`, `Timer`, and `Gauge` in your code, and swap backends — Prometheus, Datadog, InfluxDB — just by changing the registry on the classpath."

- "In Kubernetes, liveness and readiness are semantically different. Liveness failure restarts the pod; readiness failure removes it from the load balancer without restarting. Confusing them causes either unnecessary restarts or invisible degraded service."

### Vocabulário

| Termo PT                         | Termo EN                       |
|----------------------------------|--------------------------------|
| Sonda de vivacidade              | Liveness probe                 |
| Sonda de prontidão               | Readiness probe                |
| Indicador de saúde               | Health indicator               |
| Fachada de métricas              | Metrics facade                 |
| Raspagem (de métricas)           | Scraping                       |
| Contador                         | Counter                        |
| Temporizador / cronômetro        | Timer                          |
| Medidor / indicador de nível     | Gauge                          |
| Grupo de saúde                   | Health group                   |
| Endpoint de gerenciamento        | Management endpoint            |
| Exposição de endpoints           | Endpoint exposure              |
| Observabilidade                  | Observability                  |

## Veja também

- [[03-Dominios/Java/Spring Core e Boot/16 - SpringApplication e o embedded server|SpringApplication e o embedded server]]
- [[03-Dominios/Java/Spring Core e Boot/14 - Conditional beans — @Conditional e os @ConditionalOn|Conditional beans]]
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- Verbete: [[03-Dominios/Java/Dicionário de Java#Spring Actuator|Spring Actuator]]

## Referências

- [Spring Boot Actuator — documentação oficial (Boot 3.x)](https://docs.spring.io/spring-boot/reference/actuator/index.html)
- [Micrometer — documentação oficial](https://micrometer.io/docs)
- [Spring Boot — Liveness and Readiness Probes](https://docs.spring.io/spring-boot/reference/actuator/endpoints.html#actuator.endpoints.kubernetes-probes)
- [Micrometer Registry Prometheus](https://micrometer.io/docs/registry/prometheus)
