---
title: "Métricas em produção — Micrometer e Prometheus"
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
  - observabilidade
  - prometheus
aliases:
  - "Micrometer"
  - "Prometheus"
---

# Métricas em produção — Micrometer e Prometheus

> [!abstract] TL;DR
> **Micrometer** (1.17.x) é a **fachada de métricas** da JVM: você instrumenta o código contra uma API neutra — `Counter`, `Gauge`, `Timer`, `DistributionSummary` — e escolhe o **registry** (Prometheus, OTLP, Datadog…) só no classpath, sem tocar na instrumentação. É o "SLF4J das métricas". No Spring Boot, basta a dependência `micrometer-registry-prometheus` para o Actuator passar a expor `/actuator/prometheus`, um endpoint texto no formato de scrape. O **Prometheus** (3.12) é o lado de fora: ele opera por **pull/scrape** — *ele* faz requisições HTTP periódicas a esse endpoint (configurado em `scrape_configs` com `metrics_path: /actuator/prometheus`), não a aplicação que empurra. Cada métrica é nome + **tags** (labels), o que dá um modelo dimensional para filtrar e agregar. A armadilha que derruba produção é **cardinalidade**: nunca use `user-id`, UUID ou e-mail como tag — cada valor vira uma série temporal nova e explode a memória do Prometheus.

## O que é

São duas peças que se encaixam, uma de cada lado da fronteira HTTP.

**Micrometer** é uma **fachada de observabilidade vendor-neutral** — a própria documentação se compara ao SLF4J, mas para métricas em vez de logs. Você programa contra uma API única; qual backend recebe os dados é uma decisão de dependência, não de código.

**Prometheus** é o sistema de monitoramento que **coleta e armazena** as métricas como séries temporais e permite consultá-las (via PromQL). Ele não recebe dados empurrados: ele vai buscar (*scrape*) os números nos alvos instrumentados.

> [!info] Fronteira com o Galho 8
> O **mecanismo** do Actuator — como a auto-configuração descobre o `MeterRegistry`, como os endpoints são expostos e protegidos, como a infraestrutura de observabilidade se monta — é assunto do Galho 8. Veja [[03-Dominios/Tecnologia/Java/Spring Core e Boot/17 - Actuator e observabilidade|Actuator e observabilidade (Galho 8)]]. Esta nota trata do **uso operacional**: como esse mecanismo vira o endpoint `/actuator/prometheus` que o Prometheus raspa em produção, e como instrumentar métricas de domínio.

## Por que importa

Logs respondem "o que aconteceu nesta requisição?". Métricas respondem "como está o sistema **agregado** ao longo do tempo?" — taxa de pedidos por segundo, latência no percentil 99, número de conexões abertas, profundidade de uma fila. São números baratos de coletar e armazenar porque são agregados, não eventos individuais.

A fachada existe para **proteger seu investimento de instrumentação**. Você espalha `Counter` e `Timer` pelo código uma vez. Se amanhã a empresa migra de Prometheus para OTLP, ou roda os dois em paralelo, você troca a dependência do registry — a instrumentação não muda uma linha. Acoplar o código diretamente a um cliente Prometheus seria o equivalente a escrever `System.out.println` em vez de logar contra uma fachada: funciona, até a hora de trocar o backend.

O modelo **pull** do Prometheus também importa operacionalmente. Como é o Prometheus que inicia a conexão, ele sabe na hora se um alvo está *de pé* (o scrape responde) ou *fora* (o scrape falha) — a própria coleta vira um sinal de saúde. E aplicações novas só precisam expor o endpoint; quem decide raspar é a configuração central, não cada serviço.

## Como funciona

### Micrometer: a fachada e os registries

A API do Micrometer expõe quatro instrumentos (*meters*) principais:

- **`Counter`** — um valor que só **sobe**. Conta ocorrências: pedidos processados, erros, mensagens publicadas.
- **`Gauge`** — um valor **instantâneo** que sobe e desce. Mede estado: itens numa fila, conexões ativas, memória usada.
- **`Timer`** — mede **duração e frequência** de eventos curtos: latência de um endpoint, tempo de uma chamada externa. Registra contagem, soma e (opcionalmente) percentis.
- **`DistributionSummary`** — como o `Timer`, mas para **distribuições de qualquer grandeza** que não seja tempo: tamanho de payload, valor de um pedido.

Todo meter carrega um nome (`order.placed`) e zero ou mais **tags** (pares chave/valor, ex.: `region=us-east-1`). As tags são o que torna o modelo **dimensional**: você emite `http.server.requests` uma vez e depois fatia por `status`, `method`, `uri` na consulta.

O **registry** é o destino. O `MeterRegistry` é a abstração; cada implementação (`PrometheusMeterRegistry`, `OtlpMeterRegistry`, `DatadogMeterRegistry`…) sabe traduzir os meters para o formato daquele backend. No Spring Boot, a auto-configuração monta um `MeterRegistry` **composto** e adiciona um registry para cada `micrometer-registry-{sistema}` que encontrar no classpath. Daí a frase: **a dependência é a configuração**.

> [!tip] A analogia do SLF4J
> SLF4J é uma API de log; Logback/Log4j2 são as implementações que decidem para onde o log vai. Micrometer é a API de métricas; os registries (Prometheus, OTLP…) são as implementações que decidem para onde a métrica vai. Em ambos os casos, seu código fala com a fachada e ignora o backend.

### O endpoint `/actuator/prometheus` e o formato de scrape

Quando `micrometer-registry-prometheus` está no classpath, o Spring Boot Actuator passa a oferecer o endpoint **`/actuator/prometheus`**. Ele não é JSON: devolve **texto puro** no formato que o Prometheus entende para raspar — uma linha por série, com nome, tags entre chaves e valor:

```text
# HELP order_placed_total Total de pedidos criados
# TYPE order_placed_total counter
order_placed_total{region="us-east-1",} 1834.0
http_server_requests_seconds_count{method="GET",status="200",uri="/orders",} 9210.0
```

Esse endpoint **não vem exposto por padrão** — como qualquer endpoint além de `health`, você precisa incluí-lo explicitamente em `management.endpoints.web.exposure.include`. Como **expor** e **proteger** endpoints é mecanismo do Actuator, isso fica no Galho 8; aqui basta saber que `prometheus` precisa entrar nessa lista.

### Prometheus: o modelo pull/scrape

O ponto que mais confunde quem vem de outros sistemas: **o Prometheus puxa, a aplicação não empurra**. Em intervalos regulares (ex.: a cada 15s), o servidor Prometheus faz um `GET` no `metrics_path` de cada alvo e ingere o que vier. A aplicação só **expõe** os números; ela nunca abre conexão com o Prometheus.

A configuração de quem raspar e onde vive no `prometheus.yml`, dentro de `scrape_configs`. Cada *job* descreve um conjunto de alvos (`targets`), o caminho (`metrics_path`) e o intervalo. Para um app Spring Boot, o caminho é `/actuator/prometheus`.

O modelo de dados é **multidimensional**: cada amostra é `nome_da_métrica{label1="v1", label2="v2"} valor`. Os labels do Prometheus correspondem 1:1 às tags do Micrometer — a fachada traduz uma na outra.

> [!info] Pushgateway: a exceção, não a regra
> Jobs efêmeros (um *batch* que roda e morre antes de qualquer scrape) podem **empurrar** para um **Pushgateway** intermediário, que o Prometheus depois raspa. É uma exceção para processos de vida curta — o caminho normal de um serviço *long-running* é sempre pull.

## Na prática

Configuração do Prometheus (`prometheus.yml`) raspando um serviço Spring Boot. Domínio neutro: um `order-service`.

```yaml
# prometheus.yml — o Prometheus raspa o app, não o contrário
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "order-service"
    metrics_path: "/actuator/prometheus"
    static_configs:
      - targets: ["order-service:8080"]
```

Do lado da aplicação (`application.yml`), só é preciso expor o endpoint e (opcionalmente) anexar tags comuns a todas as métricas:

```yaml
# application.yml — expõe o endpoint e adiciona tags globais
management:
  endpoints:
    web:
      exposure:
        include: health,prometheus
  metrics:
    tags:
      application: order-service   # tag comum em TODA métrica
      region: us-east-1
```

Métrica de domínio com `MeterRegistry`. Injete o registry pelo construtor e crie um `Counter` e um `Timer`:

```java
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.stereotype.Service;

@Service
public class OrderService {

    private final Counter ordersPlaced;
    private final Timer checkoutTimer;

    public OrderService(MeterRegistry registry) {
        // Counter: tag de baixa cardinalidade (canal tem poucos valores possíveis)
        this.ordersPlaced = Counter.builder("order.placed")
                .description("Pedidos criados com sucesso")
                .tag("channel", "web")
                .register(registry);

        // Timer: mede latência do checkout
        this.checkoutTimer = Timer.builder("order.checkout.duration")
                .description("Tempo do fluxo de checkout")
                .register(registry);
    }

    public Order placeOrder(Cart cart) {
        // record(...) cronometra o bloco e contabiliza a duração
        return checkoutTimer.record(() -> {
            Order order = process(cart);
            ordersPlaced.increment();   // +1 no contador
            return order;
        });
    }

    private Order process(Cart cart) {
        // ... regra de negócio
        return new Order();
    }
}
```

No Prometheus, `order_placed_total` e `order_checkout_duration_seconds_count` aparecem prontos para consulta, já com as tags `application`, `region` e `channel`.

## Armadilhas

### (1) Cardinalidade explosiva — tag com user-id, UUID ou e-mail

Esta é a falha que mais derruba produção. Cada **combinação distinta de valores de tag** vira uma **série temporal separada** no Prometheus, com seu próprio custo de memória e disco. Uma tag `channel` com 3 valores cria 3 séries — tranquilo. Uma tag `userId` com 2 milhões de usuários cria 2 milhões de séries por métrica — o Prometheus incha e pode cair (*cardinality explosion*).

Regra: tags são para dimensões de **baixa cardinalidade e conjunto finito** (status HTTP, região, tipo de operação). Nunca use identificadores únicos (UUID, user-id, e-mail, request-id, URL com path variável não normalizado). Se você precisa rastrear um caso individual, isso é trabalho de **log** ou **trace**, não de métrica.

### (2) Expor `/actuator/prometheus` sem proteção

O endpoint Prometheus revela a topologia interna do serviço: nomes de métricas de negócio, volumes, latências, às vezes tags reveladoras. Exposto sem autenticação numa rede acessível, vira reconhecimento gratuito para um atacante. O endpoint só deve ser alcançável pelo próprio Prometheus — tipicamente numa porta de management interna, atrás de network policy, e/ou autenticado. Como configurar isso é mecanismo do Actuator (Galho 8); a armadilha operacional é **assumir que "só métricas" é inofensivo** e deixar aberto.

### (3) Confundir pull/scrape com push

Quem vem de StatsD, Datadog agent ou similares espera **empurrar** métricas para um coletor. No Prometheus o fluxo é o inverso: você **expõe** e ele **puxa**. O sintoma de não entender isso é procurar onde configurar "o host do Prometheus para enviar os dados" — esse campo não existe no app. Se as métricas não aparecem, o problema quase nunca é a aplicação enviando errado; é o `scrape_configs` do Prometheus apontando para o alvo/porta/caminho errado, ou o endpoint não exposto. O Pushgateway é a única exceção, e só para jobs efêmeros (ver acima).

## Em entrevista

### Frase pronta (inglês)

> In Spring Boot, I instrument the application with **Micrometer**, which acts as a vendor-neutral **metrics facade** — like SLF4J, but for metrics. I write against its API using counters, gauges, and timers, and the choice of backend is just a classpath dependency: adding `micrometer-registry-prometheus` makes Actuator expose the `/actuator/prometheus` endpoint in scrape format. **Prometheus** then collects the data with a **pull model**: it scrapes that HTTP endpoint on an interval defined in `scrape_configs`, rather than the app pushing metrics out. The thing I'm most careful about is **cardinality** — I never put high-cardinality values like user IDs or UUIDs in tags, because every distinct combination becomes a new time series and can blow up the Prometheus server.

### Vocabulário

| Português | Inglês |
| --- | --- |
| fachada de métricas | metrics facade |
| registro (de métricas) | registry |
| raspagem / coleta | scrape |
| contador | counter |
| medidor | gauge |
| cronômetro | timer |
| cardinalidade | cardinality |
| modelo de puxar | pull model |
| série temporal | time series |
| rótulo / etiqueta | label / tag |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|Observabilidade de operação]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/15 - Dashboards e alertas — Grafana|Dashboards e alertas (Grafana)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/16 - OpenTelemetry Collector e sampling de produção|OpenTelemetry Collector e sampling]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/17 - Actuator e observabilidade|Actuator (Galho 8)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- [Micrometer — Reference Documentation](https://docs.micrometer.io/micrometer/reference/) — fachada vendor-neutral, registries, meter types (counter/gauge/timer/distribution summary), modelo dimensional/tags; versão 1.17.x.
- [Prometheus — Overview](https://prometheus.io/docs/introduction/overview/) — modelo pull/scrape sobre HTTP, modelo de dados nome + labels, Pushgateway para jobs efêmeros.
- [Spring Boot — Actuator Metrics](https://docs.spring.io/spring-boot/reference/actuator/metrics.html) — integração com Micrometer, endpoint `/actuator/prometheus`, dependência `micrometer-registry-prometheus`, `scrape_configs` com `metrics_path`, métricas customizadas com `MeterRegistry`/`Counter`/`Timer`, common tags.
