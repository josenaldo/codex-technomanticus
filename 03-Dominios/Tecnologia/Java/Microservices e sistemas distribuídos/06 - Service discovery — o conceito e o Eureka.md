---
title: "Service discovery — o conceito e o Eureka"
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
  - "Service discovery"
  - "Eureka"
---

# Service discovery — o conceito e o Eureka

> [!abstract] TL;DR
> Em microsserviços, instâncias sobem, descem e mudam de endereço o tempo todo (escala automática, deploy, falha). **Service discovery** é o mecanismo que responde à pergunta "onde está o `order-service` agora?" sem que ninguém precise codificar IPs na mão. A peça central é o **service registry** — uma lista telefônica viva onde cada instância se cadastra ao subir e prova que continua viva por **heartbeat**. Há dois sabores: **client-side discovery** (o próprio cliente consulta o registry e escolhe a instância) e **server-side discovery** (uma infra no meio resolve por você). O **Netflix Eureka** é o registry client-side clássico do mundo Spring — e, ao contrário de Hystrix, Ribbon e Zuul, **não entrou em maintenance mode**: segue mantido na linha 5.0.x do Spring Cloud Netflix.

## O que é

Service discovery é o conjunto de mecanismos que permite a um serviço **descobrir o endereço de rede de outro serviço em tempo de execução**, em vez de depender de hosts e portas fixos.

Pense numa **lista telefônica**. Você não decora o número de todo mundo nem cola num papel que envelhece: você abre a lista, procura pelo nome e o número atual aparece. Quem muda de número se reinscreve; quem some é tirado da lista. O **service registry** é exatamente essa lista — só que para serviços, e atualizada de segundo em segundo.

Por que isso é necessário? Num monólito, chamar outra parte do sistema é uma chamada de método: tudo vive no mesmo processo. Em microsserviços, cada chamada vira uma chamada de rede para um endereço que **não é estável**:

- O orquestrador (Kubernetes, ECS, Nomad) sobe e derruba **instâncias** o tempo todo.
- Escala automática multiplica réplicas de um serviço sob carga.
- Deploys substituem instâncias antigas por novas, com IPs diferentes.
- Falhas removem instâncias sem aviso.

Hardcodar `http://192.168.1.42:8080` é assinar um atestado de fragilidade. Discovery resolve a indireção: o cliente fala em **nome lógico** (`payment-service`) e o sistema traduz para um endereço vivo no momento da chamada.

## Por que importa

Sem discovery, você cai em um destes buracos:

- **Endereços fixos** que quebram a cada deploy ou escala.
- **Arquivos de configuração** com listas de hosts que envelhecem e exigem redeploy a cada mudança de topologia.
- **Balanceadores manuais** que alguém precisa reconfigurar à mão sempre que a frota muda.

Discovery automatiza a pergunta "quem está vivo e onde?". Isso é pré-requisito direto para três coisas que você vai ver nas próximas notas:

- **Load balancing** entre instâncias de um mesmo serviço (a lista de candidatos vem do registry — ver [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer|Spring Cloud LoadBalancer]]).
- **Resiliência**: instâncias mortas saem da lista, então você para de mandar tráfego para o vazio.
- **Elasticidade**: réplicas novas entram na lista assim que ficam prontas e começam a receber tráfego sem intervenção humana.

Em entrevista, a frase que ancora tudo é: *discovery transforma endereço de rede em detalhe de runtime, não em configuração estática*.

## Como funciona

### Client-side discovery vs server-side discovery

Os dois modelos diferem em **quem decide qual instância recebe a chamada**.

**Client-side discovery**: o cliente consulta o registry diretamente, recebe a **lista de instâncias** vivas de `payment-service` e **escolhe uma** (round-robin, aleatório, por latência). O cliente carrega a lógica de balanceamento.

```text
[order-service] --consulta--> [Service Registry]
       |  <--lista de instâncias--
       |
       +--escolhe uma e chama--> [payment-service #2]
```

- Prós: menos saltos de rede (o cliente fala direto com a instância escolhida); o cliente pode usar estratégias espertas de escolha.
- Contras: cada cliente precisa de uma biblioteca de discovery; a lógica de balanceamento fica espalhada por todas as linguagens/serviços.
- Exemplos: **Netflix Eureka** + Spring Cloud LoadBalancer.

**Server-side discovery**: o cliente chama um **endereço estável** (um balanceador ou gateway) e **a infraestrutura resolve** qual instância concreta atende. O cliente não conhece o registry; ele só conhece o ponto de entrada.

```text
[order-service] --chama nome estável--> [LB / proxy] --resolve--> [payment-service #2]
                                              |
                                              +--lê o registry internamente
```

- Prós: cliente burro e portável (qualquer linguagem, zero biblioteca de discovery); balanceamento centralizado.
- Contras: um salto extra de rede; o resolvedor vira peça crítica de infra.
- Exemplos: o `Service` do **Kubernetes** (DNS + kube-proxy/iptables/IPVS), balanceadores de nuvem, AWS ELB.

> [!tip] A escolha não é só técnica, é de plataforma
> Se você roda em Kubernetes, a plataforma **já faz server-side discovery** via `Service` e DNS interno. Empilhar Eureka por cima costuma ser redundância (ver Armadilhas). Eureka brilha quando você **não** tem um orquestrador que resolva endereços por você — VMs cruas, ambientes híbridos, ou bases legadas Spring Cloud já investidas nele.

### O service registry

O **service registry** é o banco de dados vivo de "quem está no ar". Toda forma de discovery depende dele, explícito (Eureka, Consul) ou embutido na plataforma (etcd por trás do Kubernetes). Ele tem três responsabilidades:

1. **Registro (registration)**: uma instância, ao subir, se cadastra com seus metadados — host, porta, URL de health check, nome lógico do serviço.
2. **Renovação (renewal / heartbeat)**: a instância manda sinais periódicos provando que continua viva. Se os sinais param, a instância é considerada morta.
3. **Expiração (eviction)**: instâncias que pararam de renovar são removidas da lista após um prazo (TTL), para que ninguém receba endereço de fantasma.

O registry pode ser um serviço dedicado (o caso do Eureka Server) ou um cluster de registries replicados entre si para não virar ponto único de falha.

### Eureka: server, client e heartbeat

O **Netflix Eureka** implementa o modelo client-side. Ele tem duas metades:

- **Eureka Server**: a aplicação que guarda o registry. Você sobe uma app Spring Boot anotada com `@EnableEurekaServer`. Em produção, vários servers se replicam (peer awareness) para tolerar falhas.
- **Eureka Client**: a biblioteca que cada microsserviço embute. Ela faz três coisas: registra a instância no server ao subir, **renova o lease por heartbeat** periodicamente, e **busca o registry** (fetch) para descobrir outros serviços, mantendo uma cópia local em cache.

O ciclo de vida, em registro Feynman:

- A instância sobe e **grita "estou aqui!"** (registro) com seus metadados.
- A cada **30 segundos por padrão** ela manda um **batimento** (`leaseRenewalIntervalInSeconds`, default 30s) dizendo "ainda vivo".
- Se os batimentos param, o lease **expira** e o server tira a instância da lista.
- Como cliente, server e o cache local precisam **convergir** os mesmos metadados, uma instância nova pode levar **até 3 heartbeats** para ficar visível a todos — propagação não é instantânea.

> [!info] Self-preservation (auto-preservação)
> O Eureka Server tem um modo de proteção: se ele para de receber heartbeats **de muitas instâncias de uma vez** (acima de um limiar), ele **suspeita de problema de rede dele próprio**, não de morte em massa real dos serviços. Em vez de despejar todo mundo da lista, ele **congela o registry** e para de expirar instâncias até a situação normalizar. A ideia: é melhor servir alguns endereços possivelmente velhos do que esvaziar a lista por causa de um soluço de rede e derrubar o sistema inteiro. O comportamento de aquecimento na subida do server se ajusta por `eureka.server.defaultOpenForTrafficCount` (e `waitTimeInMsWhenSyncEmpty`, do Netflix Eureka, que o Spring Cloud não considera por padrão no boot).
>
> Fonte: [docs.spring.io — Spring Cloud Netflix reference, linha 5.0.x](https://docs.spring.io/spring-cloud-netflix/reference/spring-cloud-netflix.html) (consultado em 2026-06-12).

> [!check] Eureka NÃO está em maintenance mode
> Em 2018 o Spring Cloud colocou vários módulos Netflix em **maintenance mode** (sem features novas, só correções críticas): **Archaius, Hystrix, Ribbon, Turbine e Zuul**. A documentação é explícita: *"This does not include the Eureka [...] module"*. **Eureka server e client seguem ativamente mantidos**, hoje na linha **5.0.x** do Spring Cloud Netflix (trem de release Oakwood).
>
> Fonte: [cloud.spring.io — Modules in maintenance mode](https://cloud.spring.io/spring-cloud-netflix/multi/multi__modules_in_maintenance_mode.html) (consultado em 2026-06-12).

## Na prática

Um microsserviço cliente que se registra e descobre outros via Eureka. A anotação `@EnableDiscoveryClient` é agnóstica de implementação (vale para Eureka, Consul etc.); com o starter do Eureka no classpath, o registro é automático.

```java
package com.example.order;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@EnableDiscoveryClient
@SpringBootApplication
public class OrderServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
    }
}
```

Configuração do `order-service` apontando para o Eureka Server e ajustando o batimento:

```yaml
spring:
  application:
    name: order-service        # nome lógico que aparece no registry

eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/   # endereço do Eureka Server
    register-with-eureka: true   # esta instância se cadastra
    fetch-registry: true         # e baixa o registry para descobrir outros
  instance:
    prefer-ip-address: true
    lease-renewal-interval-in-seconds: 30   # heartbeat a cada 30s (default)
    lease-expiration-duration-in-seconds: 90 # server expira após 90s sem batimento
```

O `payment-service` teria um `application.yml` análogo, só mudando `spring.application.name`. A partir daí, o `order-service` chama o outro **pelo nome lógico** (`http://payment-service/...`) em vez de IP — a resolução é feita pelo cliente de discovery somada ao load balancer.

O Eureka Server, por sua vez, é uma app mínima:

```java
package com.example.registry;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

@EnableEurekaServer
@SpringBootApplication
public class EurekaServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}
```

## Armadilhas

### (1) Rodar Eureka quando o Kubernetes já resolve

**Sintoma**: você sobe Eureka Server num cluster Kubernetes, e agora tem **dois** sistemas de discovery competindo — o `Service`/DNS do k8s (server-side, sempre ativo) e o Eureka (client-side). Resultado: complexidade dobrada, duas fontes de verdade que divergem, e debugging de "por que o tráfego foi parar nessa instância?" vira pesadelo.

```yaml
# Anti-padrão num cluster k8s: empilhar Eureka sobre o discovery nativo
eureka:
  client:
    service-url:
      defaultZone: http://eureka-server:8761/eureka/
```

**Fix**: em Kubernetes, prefira o **server-side discovery nativo** — chame `http://payment-service` (nome do `Service`) e deixe o DNS interno resolver. Eureka faz sentido fora de orquestradores que já resolvem endereços, ou em migrações de bases Spring Cloud legadas. Ver [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/07 - Discovery — Consul e Kubernetes-native|Discovery: Consul e Kubernetes-native]].

### (2) Heartbeat e TTL mal configurados = instâncias zumbis

**Sintoma**: você baixa o intervalo de renovação mas esquece de ajustar o tempo de expiração — ou os deixa frouxos demais. Uma instância **morre**, mas o server demora muito para expirar o lease. Durante esse intervalo, clientes continuam recebendo o endereço do morto e tomam timeouts e erros de conexão. São as **instâncias zumbis**: na lista, mas mortas.

```yaml
eureka:
  instance:
    lease-renewal-interval-in-seconds: 30
    lease-expiration-duration-in-seconds: 300  # 5 min para expirar — frouxo demais!
```

**Fix**: mantenha a expiração coerente com o intervalo de renovação (a regra de bolso é expirar após ~3 batimentos perdidos; com renovação de 30s, expiração de 90s). Não baixe o intervalo de heartbeat sem reduzir a expiração junto. E lembre da latência intrínseca: até a propagação convergir, **uma instância pode levar até 3 heartbeats para aparecer ou sumir** — discovery client-side é eventualmente consistente, não instantâneo.

### (3) Entender self-preservation errado

**Sintoma**: em teste ou ambiente pequeno, você derruba algumas instâncias e o Eureka Server **continua mostrando-as como vivas**. Você conclui que "o Eureka está bugado" e desativa proteções no susto — ou, pior, em produção você desliga self-preservation e um soluço de rede esvazia o registry, derrubando o sistema todo.

```yaml
# Em produção, desligar sem entender as consequências é arriscado:
eureka:
  server:
    enable-self-preservation: false
```

**Fix**: entenda que self-preservation é **proteção contra falsa morte em massa** — quando o server perde heartbeats de muitas instâncias de uma vez, ele assume problema de rede **dele** e congela a lista em vez de despejar todo mundo. Em ambientes de **desenvolvimento** com poucas instâncias, o limiar dispara fácil e atrapalha o teste; aí faz sentido desligar **só em dev**. Em produção, entenda o trade-off antes de mexer: prefira ajustar os limiares a desligar a proteção.

## Em entrevista

### Frase pronta (inglês)

> Service discovery solves a basic problem in microservices: instances come and go constantly, so I can't hardcode network addresses. A **service registry** keeps a live list of healthy instances — each one registers on startup and proves it's alive through a periodic **heartbeat**. There are two flavors: in **client-side discovery**, the client queries the registry and picks an instance itself, which is what Netflix Eureka does together with a client-side load balancer; in **server-side discovery**, the client just hits a stable endpoint and the infrastructure resolves the instance, which is what Kubernetes Services do natively. I'd reach for Eureka outside an orchestrator or in legacy Spring Cloud systems, and lean on native server-side discovery when I'm already on Kubernetes. One thing worth knowing: Eureka's **self-preservation** mode protects the registry from evicting everything during a network glitch, and Eureka itself — unlike Hystrix, Ribbon and Zuul — is still actively maintained, not in maintenance mode.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| registro de serviço | service registry |
| descoberta no cliente | client-side discovery |
| descoberta no servidor | server-side discovery |
| batimento | heartbeat |
| auto-preservação | self-preservation |
| instância | instance |
| renovação de lease | lease renewal |
| despejo / expiração | eviction |

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/07 - Discovery — Consul e Kubernetes-native|Discovery: Consul e Kubernetes-native]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer|Spring Cloud LoadBalancer]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/04 - Panorama do Spring Cloud — e o que morreu|Panorama do Spring Cloud]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

> Os galhos 17 e 18 da trilha aprofundam temas de plataforma e operação de microsserviços (planejado) e ainda não têm notas para linkar aqui.

## Referências

- Spring Cloud Netflix — Reference Documentation (linha 5.0.x, trem Oakwood): registro, heartbeat com `leaseRenewalIntervalInSeconds` (default 30s), propagação em até 3 heartbeats, warmup via `eureka.server.defaultOpenForTrafficCount`. <https://docs.spring.io/spring-cloud-netflix/reference/spring-cloud-netflix.html> (consultado em 2026-06-12).
- Spring Cloud Netflix — Modules in maintenance mode: Archaius, Hystrix, Ribbon, Turbine e Zuul entraram em maintenance mode; **Eureka explicitamente excluído** ("This does not include the Eureka [...] module"). <https://cloud.spring.io/spring-cloud-netflix/multi/multi__modules_in_maintenance_mode.html> (consultado em 2026-06-12).
