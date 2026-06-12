---
title: "Discovery — Consul e Kubernetes-native"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - microservices
  - adepto
  - discovery
aliases:
  - "Consul"
  - "Spring Cloud Kubernetes"
---

# Discovery — Consul e Kubernetes-native

> [!abstract] TL;DR
> O Eureka resolveu o *service discovery* num mundo onde a aplicação carregava o peso do registro. Mas ele não é a única — nem sempre a melhor — opção. Duas alternativas dominam o ecossistema atual:
> - **HashiCorp Consul** (`spring-cloud-starter-consul-discovery`): um registry externo e poliglota que vai *muito além* de discovery. Resolve serviços por **HTTP API e DNS**, faz **health checks** ativos, e ainda guarda configuração num **KV store**. É o "canivete suíço" para frotas heterogêneas (não só Java).
> - **Spring Cloud Kubernetes**: quando você já roda no k8s, **a própria infra já é o registry**. O Kubernetes registra Pods em `Service`/`Endpoints` por conta própria. A app só consulta — via **API server** (`DiscoveryClient`) ou via **DNS nativo do cluster** (modo *server-side*, FQDN tipo `pedidos.default.svc.cluster.local`).
> A distinção que importa (vinda da [[03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|nota 06]]) é **client-side vs server-side**: o Eureka é client-side (a app pergunta ao registry e escolhe a instância). O modo nativo do k8s é server-side — **a infra resolve**, e a app nem sabe que existe discovery.

## O que é

Na [[03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|nota 06]] vimos o *problema* do discovery — instâncias que aparecem, somem e trocam de IP — e a *primeira solução* da casa Spring: o **Netflix Eureka**, um registry client-side onde cada serviço se registra e consulta uma lista para escolher com quem falar.

Esta nota é sobre as **alternativas ao Eureka**. Porque o Eureka tem dois limites desconfortáveis:

1. Ele é **Java-cêntrico**. Numa frota poliglota (um serviço em Go, outro em Node, outro em Python), fazer todo mundo falar o protocolo do Eureka é fricção.
2. Ele **duplica trabalho que a infra moderna já faz**. Se você roda em Kubernetes, o orquestrador *já registra e resolve serviços por você*. Rodar um Eureka por cima é reinventar a roda — e ainda manter mais uma peça de pé.

As duas respostas são:

- **HashiCorp Consul** — um registry de propósito geral, externo à app e agnóstico de linguagem. Discovery é só *uma* de suas funções; ele também é **KV store** (configuração distribuída) e plataforma de health checking.
- **Spring Cloud Kubernetes** — a ponte entre o `DiscoveryClient` do Spring e o discovery *que o Kubernetes já oferece de fábrica*. Aqui a app não roda nenhum registry: ela consulta o que o cluster sabe.

> [!info] O escopo desta nota
> Operar e instalar Kubernetes em produção — como subir um cluster, configurar `Service`, `Ingress`, etc. — é assunto do **Galho 17 (planejado)**. Aqui olhamos o discovery **pela ótica da aplicação Java**: como o código Spring descobre os outros serviços. A operação do cluster fica de fora de propósito.

## Por que importa

Escolher o mecanismo de discovery não é trocar uma dependência por outra equivalente. Cada opção **muda quem carrega a responsabilidade**.

Pense numa analogia de portaria de prédio. O **Eureka** é como cada morador manter sua própria lista de telefones atualizada: quando alguém muda de apartamento, todos precisam atualizar a lista. Funciona, mas dá trabalho e a lista de cada um pode estar defasada. O **Consul** é contratar uma central telefônica externa que vale para o prédio inteiro — inclusive para visitantes que não falam o "idioma interno" do condomínio (serviços não-Java). E o **Kubernetes nativo** é o prédio ter um *interfone embutido na parede*: você disca o número do apartamento e a infra do prédio conecta — ninguém precisa manter lista nenhuma, porque o sistema do prédio *já sabe* quem mora onde.

A consequência prática:

- Com **Consul**, você ganha um registry robusto e poliglota, mas adiciona **uma peça de infraestrutura para operar** (o cluster Consul, com seu protocolo de consenso Raft).
- Com **Kubernetes nativo**, você **não adiciona peça nenhuma** — reaproveita o que o cluster já faz. Por isso muita gente, ao migrar para k8s, **aposenta o Eureka inteiro**. Discovery deixa de ser problema da aplicação.

Saber qual encaixa no seu contexto é o que evita os dois erros clássicos: rodar um Eureka *desnecessário* dentro do Kubernetes, ou tentar fazer um registry externo competir com o DNS do cluster.

## Como funciona

### Consul — discovery via HTTP API, DNS e health checks

O **Consul** é um produto da HashiCorp que roda como um **cluster de agentes** externos à sua aplicação. Esses agentes se comunicam por um *gossip protocol* e mantêm consistência via **protocolo de consenso Raft** — ou seja, ele é projetado para ser confiável mesmo com falhas de nós.

Do lado Spring, você adiciona o starter:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-consul-discovery</artifactId>
</dependency>
```

O fluxo é parecido com o do Eureka no formato, mas diferente no motor:

1. **Registro.** Ao subir, a app se registra no agente Consul informando metadados: host, porta, *service ID*, *service name* e *tags*. Os defaults vêm do `Environment` — o nome é `${spring.application.name}`, a porta é `${server.port}`.

2. **Health check.** Por padrão, o Consul cria um **HTTP Health Check** que bate em `/actuator/health` **a cada 10 segundos**. Se o check falha, a instância é marcada como *critical* e some das consultas de discovery. Há também o modo **TTL** (*heartbeat*), em que é a *aplicação* que manda o batimento ao Consul, em vez de o Consul ir buscar.

3. **Descoberta.** O Spring Cloud Consul usa a **HTTP API** do Consul para registro e descoberta. No código, você usa o mesmo `DiscoveryClient` abstrato do Spring Cloud Commons — o mesmo da nota 06:

   ```java
   @Autowired
   private DiscoveryClient discoveryClient;

   public String urlDaLoja() {
       List<ServiceInstance> instancias = discoveryClient.getInstances("LOJA");
       return instancias.isEmpty() ? null : instancias.get(0).getUri().toString();
   }
   ```

   Mas o Consul tem um truque extra: ele **também expõe discovery por DNS**. Qualquer aplicação — inclusive **não-Spring, não-Java** — pode resolver um serviço via interface DNS do Consul, sem falar a HTTP API. É isso que o torna poliglota de verdade.

> [!tip] Consul não é "só discovery" — é também o KV store
> O Consul carrega um **armazenamento chave-valor** (*key-value store*) embutido. Isso significa que ele faz dois trabalhos que no mundo Spring costumam ser ferramentas separadas: o discovery (papel do Eureka) **e** a configuração centralizada (papel do Spring Cloud Config — ver [[03-Dominios/Java/Microservices e sistemas distribuídos/12 - Config centralizado — Spring Cloud Config|nota 12]]). Existe um starter irmão, `spring-cloud-starter-consul-config`, que lê propriedades do KV store. Confundir "Consul" com "só um Eureka melhor" é subaproveitá-lo — voltamos a isso nas Armadilhas.

### Spring Cloud Kubernetes — o discovery que a infra já oferece

Quando a app roda **dentro** de um cluster Kubernetes, o cenário muda de figura. O Kubernetes, por conta própria, mantém objetos `Service` e `Endpoints` que mapeiam um nome lógico para o conjunto de Pods vivos. **Ele já é um registry.** O Spring Cloud Kubernetes só **liga o `DiscoveryClient` do Spring a esse registry nativo**.

Há duas formas de consultar — e essa é a parte que confunde:

**Forma 1 — via API server (`DiscoveryClient` baseado no Kubernetes).** A app consulta o **API server do Kubernetes** para listar `Service`/`Endpoints` por nome. Você adiciona um dos starters de implementação:

```xml
<!-- cliente Fabric8 -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-kubernetes-fabric8</artifactId>
</dependency>

<!-- ou o cliente Java oficial do Kubernetes -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-kubernetes-client</artifactId>
</dependency>
```

E habilita com `@EnableDiscoveryClient`. Aqui o `DiscoveryClient` se comporta como qualquer outro — `getInstances("pedidos")` devolve as instâncias — mas a fonte da verdade é o **API server**, não um Eureka.

**Forma 2 — discovery nativo do Kubernetes (server-side, via DNS).** Esta é a abordagem mais "k8s puro". Em vez de a app *consultar* qualquer registry, ela simplesmente **chama o serviço pelo nome DNS** que o Kubernetes resolve sozinho:

```
{nome-do-servico}.{namespace}.svc.cluster.local:{porta}
```

Esse é o **nome de domínio totalmente qualificado** (*FQDN*) de um `Service`. O DNS interno do cluster (CoreDNS) resolve esse nome para um IP virtual estável do `Service`, e o k8s faz o balanceamento por baixo. A app não tem `DiscoveryClient` consultando nada — ela só faz:

```java
restTemplate.getForObject("http://pedidos.default.svc.cluster.local/api", String.class);
```

Esse é o modelo **server-side**: a resolução acontece *fora* da aplicação, na infraestrutura. A vantagem extra é a **compatibilidade com service mesh** — ferramentas como o Istio se inserem exatamente nessa camada de rede, e só funcionam plenamente se você deixar a infra resolver, em vez de a app escolher a instância sozinha.

> [!info] Como desligar o cloud-platform do Spring
> O Spring Cloud Kubernetes auto-ativa o comportamento de discovery quando detecta que está rodando num cluster. Para desligar explicitamente (por exemplo, ao rodar a mesma app fora do k8s), use `spring.main.cloud-platform=NONE`.

### Quando cada um — Consul vs Kubernetes nativo vs Eureka

Não há "vencedor" universal; há **contexto**.

| Cenário | Escolha natural | Por quê |
|---|---|---|
| Frota só-Java, sem orquestrador, controle total | **Eureka** (nota 06) | Simples, integração Spring direta, client-side |
| Frota **poliglota** (Go/Node/Python + Java), fora do k8s | **Consul** | Discovery por DNS *e* HTTP API; ainda dá KV store de brinde |
| Você **já roda em Kubernetes** | **Spring Cloud Kubernetes (nativo)** | A infra já é o registry; não adicione peças. Discovery vira server-side e casa com service mesh |
| K8s, mas você quer a abstração `DiscoveryClient` no código | **Spring Cloud Kubernetes (API server)** | Mantém o código portável (`getInstances`), com a fonte sendo o k8s |

A regra de bolso: **se a plataforma já resolve o problema, não suba uma peça para resolvê-lo de novo.** Rodar Eureka dentro de Kubernetes é o anti-padrão mais comum dessa área.

## Na prática

### Consul discovery + (opcionalmente) config

```yaml
spring:
  application:
    name: servico-pedidos
  cloud:
    consul:
      host: localhost        # host do agente Consul
      port: 8500             # porta do agente Consul
      discovery:
        enabled: true        # liga o discovery
        register: true       # registra esta app no Consul
        service-name: ${spring.application.name}
        instance-id: ${spring.application.name}:${server.port}
        health-check-path: /actuator/health
        health-check-interval: 10s
        # heartbeat (TTL) — a app é quem manda o batimento, em vez de o Consul buscar
        heartbeat:
          enabled: false
        metadata:
          zona: leste
```

Para *desligar* discovery ou registro sem remover o starter:

```yaml
spring:
  cloud:
    consul:
      discovery:
        enabled: false   # não consulta o Consul para discovery
        register: false  # sobe sem se registrar (ex.: ferramenta de batch)
```

### Kubernetes — DiscoveryClient via API server

```yaml
spring:
  application:
    name: servico-pedidos
  main:
    cloud-platform: kubernetes   # NONE para desligar fora do cluster
```

```java
@SpringBootApplication
@EnableDiscoveryClient
public class PedidosApplication {
    public static void main(String[] args) {
        SpringApplication.run(PedidosApplication.class, args);
    }
}
```

```java
@Service
class ClienteEstoque {

    private final DiscoveryClient discoveryClient;

    ClienteEstoque(DiscoveryClient discoveryClient) {
        this.discoveryClient = discoveryClient;
    }

    URI enderecoDoEstoque() {
        // "estoque" é o nome do Service no Kubernetes
        return discoveryClient.getInstances("estoque").stream()
                .findFirst()
                .map(ServiceInstance::getUri)
                .orElseThrow();
    }
}
```

### Kubernetes — discovery nativo (server-side, sem DiscoveryClient)

Aqui não há configuração de discovery na app: você fala com o **FQDN** do `Service` e deixa o DNS do cluster resolver.

```java
@Service
class ClienteEstoqueNativo {

    private final RestClient restClient;

    ClienteEstoqueNativo(RestClient.Builder builder) {
        // FQDN do Service "estoque" no namespace "default"
        this.restClient = builder
                .baseUrl("http://estoque.default.svc.cluster.local")
                .build();
    }

    String consultar(String sku) {
        return restClient.get()
                .uri("/itens/{sku}", sku)
                .retrieve()
                .body(String.class);
    }
}
```

Repare: **nenhuma anotação de discovery, nenhum registry**. A infra resolve `estoque.default.svc.cluster.local`. Isso é o server-side em estado puro.

## Armadilhas

### (1) Dois discoveries concorrendo — Eureka *e* Kubernetes ao mesmo tempo

A migração para o k8s costuma deixar **resíduos do Eureka** no `pom.xml` e no `application.yml`. O resultado é uma app que tenta se registrar no Eureka *e* consultar o k8s — duas fontes da verdade competindo, comportamento ambíguo, e uma peça (o Eureka Server) que você ainda mantém de pé sem precisar.

**Sintoma:** `getInstances(...)` às vezes traz instâncias do registry errado; chamadas falham de forma intermitente.

**Correção:** ao adotar Kubernetes nativo, **remova o `spring-cloud-starter-netflix-eureka-client`** e desmonte o Eureka Server. Discovery passa a ser responsabilidade da plataforma. Não deixe os dois mecanismos ligados ao mesmo tempo.

### (2) Ignorar o DNS nativo do k8s e duplicar o que o cluster já faz

Rodar um Consul (ou Eureka) **dentro** do Kubernetes "porque é o que a gente sempre usou" é o erro arquitetural mais caro dessa área. O cluster **já** mantém `Service`/`Endpoints` e resolve por DNS. Subir um registry por cima significa:

- mais uma peça de infra para operar, monitorar e atualizar;
- duas fontes da verdade que podem divergir (o Pod morreu para o k8s, mas o registry externo ainda acha que está vivo);
- atrito desnecessário com service mesh, que espera a resolução server-side.

**Correção:** se a plataforma é Kubernetes, **comece pelo DNS nativo / Spring Cloud Kubernetes**. Só adote um registry externo se houver um motivo concreto (ex.: serviços *fora* do cluster que também precisam ser descobertos).

### (3) Achar que Consul é "só discovery" — é também KV/config

Quem chega ao Consul vindo do Eureka tende a tratá-lo como "um Eureka melhor" e parar aí. Mas o Consul é **discovery + health checking + key-value store** num produto só. Ignorar o **KV store** leva a um setup redundante: você sobe Consul para discovery *e* um Spring Cloud Config Server separado para configuração — quando o próprio Consul poderia fazer os dois (via `spring-cloud-starter-consul-config`).

**Correção:** ao escolher Consul, decida *conscientemente* o papel dele. Se ele já está de pé, considere usá-lo também como fonte de configuração (ver [[03-Dominios/Java/Microservices e sistemas distribuídos/12 - Config centralizado — Spring Cloud Config|nota 12]]) antes de adicionar mais uma peça. Menos componentes, menos coisa para quebrar.

## Em entrevista

### Frase pronta (inglês)

> Eureka isn't the only option for service discovery, and it's often not the best one. If I have a polyglot fleet, I prefer **HashiCorp Consul**, which exposes discovery over both an **HTTP API and DNS**, runs active **health checks**, and even doubles as a **key-value store** for centralized configuration. But when I'm already running on Kubernetes, my default is **Spring Cloud Kubernetes** with **k8s-native discovery** — the cluster already registers Pods in Services and Endpoints, so I let the infrastructure resolve services by their **fully qualified domain name**, like `orders.default.svc.cluster.local`. That's the **server-side** model: the app doesn't query a registry, it just calls the DNS name and the platform routes it. Running a separate Eureka *inside* Kubernetes is duplicated work — I'd remove it.

### Vocabulário

| Português | Inglês | Nota |
|---|---|---|
| descoberta nativa do k8s | k8s-native discovery | resolução feita pela própria infra do cluster |
| armazenamento chave-valor | key-value store | o "extra" do Consul, usado para config |
| verificação de saúde | health check | Consul bate em `/actuator/health` por padrão |
| nome de domínio totalmente qualificado | fully qualified domain name (FQDN) | ex.: `svc.namespace.svc.cluster.local` |
| lado servidor | server-side | a infra resolve; a app não escolhe a instância |
| servidor de API (do k8s) | API server | fonte consultada pelo `DiscoveryClient` baseado em k8s |
| registro de serviço | service registry | o catálogo de instâncias vivas (Eureka, Consul, ou o k8s) |

## Veja também

- [[03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|Service discovery e Eureka]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer|Spring Cloud LoadBalancer]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/12 - Config centralizado — Spring Cloud Config|Config centralizado]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Spring Cloud Consul — Service Discovery. https://docs.spring.io/spring-cloud-consul/reference/discovery.html
- Spring Cloud Kubernetes — DiscoveryClient for Kubernetes. https://docs.spring.io/spring-cloud-kubernetes/reference/discovery-client.html
- Spring Cloud Kubernetes — Kubernetes Native Service Discovery. https://docs.spring.io/spring-cloud-kubernetes/reference/discovery-kubernetes-native.html
