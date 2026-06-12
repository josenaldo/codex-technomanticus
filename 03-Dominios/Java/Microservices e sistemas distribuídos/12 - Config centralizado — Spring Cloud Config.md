---
title: "Config centralizado — Spring Cloud Config"
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
  - config
aliases:
  - "Spring Cloud Config"
  - "Config centralizado"
---

# Config centralizado — Spring Cloud Config

> [!abstract] TL;DR
> O **Spring Cloud Config** tira a configuração de dentro do jar e a coloca num lugar central — um **Config Server** que lê de um backend versionado (Git, Vault, JDBC). Cada serviço vira um **Config Client** que, no boot, puxa suas propriedades pela coordenada `{application}/{profile}/{label}`. Quando o config muda, beans anotados com `@RefreshScope` se reconstroem ao chamar `/actuator/refresh` — sem restart. Para difundir esse refresh por dezenas de instâncias de uma vez, entra o **Spring Cloud Bus**, que propaga o evento por um broker (RabbitMQ/Kafka). É a materialização do fator "config no ambiente" dos 12 fatores: uma fonte de verdade, externa ao código.

## O que é

Imagine vinte serviços, cada um com seu `application.yml`. A URL do banco mudou. Sem config central, você edita vinte arquivos, refaz vinte builds, redeploya vinte serviços. É frágil e lento.

O Spring Cloud Config resolve isso com **suporte server-side a configuração externalizada**: existe um lugar central que mapeia, ponto a ponto, as abstrações `Environment` e `PropertySource` do Spring. O **Config Server** expõe a configuração por HTTP; qualquer aplicação — em qualquer linguagem — pode consumi-la, porque a interface é REST.

Dois papéis:

- **Config Server**: serviço Spring Boot que lê a configuração de um **backend** (Git por padrão, mas também Vault, JDBC, S3, Redis, etc.) e a serve por HTTP.
- **Config Client**: cada microserviço, que no boot busca suas propriedades no server e as injeta no próprio `Environment` — como se estivessem num arquivo local.

A configuração é endereçada por três variáveis:

- `{application}` — vem de `spring.application.name` no cliente;
- `{profile}` — vem de `spring.profiles.active` (ex.: `dev`, `prod`);
- `{label}` — uma versão server-side; no backend Git, é o branch, tag ou commit (default `main`, com fallback para `master`).

## Por que importa

O fator III dos [[03-Dominios/Java/Microservices e sistemas distribuídos/03 - Os 12 fatores e o serviço cloud-native|Os 12 fatores]] manda **guardar config no ambiente**, separada do código, para que o mesmo artefato rode em qualquer ambiente só trocando a config. O Spring Cloud Config é uma das formas de cumprir esse fator no ecossistema Spring — talvez a mais explícita.

O que ele te dá de concreto:

- **Fonte única de verdade**: toda a config dos serviços vive num só lugar, idealmente versionado.
- **Histórico e auditoria**: se o backend é Git, cada mudança de config é um commit — você sabe quem mudou o quê e quando, e pode reverter.
- **Refresh sem restart**: trocar um timeout ou um feature flag não exige redeploy; um `POST /actuator/refresh` basta para os beans relevantes relerem o valor.
- **Promoção por ambiente**: o mesmo serviço sobe em `dev`, `staging` e `prod` apenas com `{profile}` diferente — o artefato é imutável.

A pergunta natural — "mas o Kubernetes já tem ConfigMap e Secret, pra que isso?" — é legítima e está no trade-off mais abaixo.

## Como funciona

### Config Server e os backends

O Config Server é uma app Spring Boot anotada com `@EnableConfigServer`. Ele não guarda config: ele a **lê de um backend** e a serve. Os backends mais comuns:

- **Git (default)**: a config vive num repositório Git. Cada arquivo (`pedidos.yml`, `pedidos-prod.yml`, `application.yml`) é uma `PropertySource`. Ganha versionamento, branches como `{label}` e ferramental de PR/review de graça. A URI aceita placeholders — `https://git.exemplo.com/config/{application}` dá um repo por serviço.
- **Vault**: backend voltado a **segredos**. O server lê valores do HashiCorp Vault em vez de (ou além de) arquivos planos. A *ótica operacional* disso — como operar Vault, rotação de segredos, secrets management de produção — é território do **Galho 17 (planejado)**; aqui só registramos que Vault é um backend possível para o mecanismo de config.
- **JDBC**: a config mora numa tabela de banco relacional. Útil quando a equipe já tem governança forte de banco e prefere SQL a Git para configuração.

Há ainda S3, Redis, MongoDB, Secrets Manager e **repositórios compostos** (combinar Git + Vault, por exemplo: arquivos planos no Git, segredos no Vault).

A URL de consulta segue o padrão `/{application}/{profile}/{label}`. Um `GET /pedidos/prod/main` devolve a config efetiva do serviço `pedidos`, perfil `prod`, branch `main`.

### Config Client e `@RefreshScope`

No cliente, a forma moderna de conectar é o **Config Data import** do Spring Boot, sem `bootstrap.yml`:

```properties
spring.config.import=optional:configserver:http://localhost:8888
```

O prefixo `optional:` é a decisão de criticidade:

- `optional:configserver:...` — a app **sobe mesmo** se o server estiver fora (fail-soft);
- `configserver:...` (sem `optional:`) — a app **falha no boot** se não alcançar o server (fail-fast).

Há `retry` configurável (`max-attempts`, `initial-interval`, etc.) e suporte a múltiplas URLs do server, para alta disponibilidade.

O **refresh** é o que torna a config viva. Beans anotados com `@RefreshScope` não são singletons comuns: ao receber um evento de refresh, o Spring **descarta a instância atual e recria o bean** na próxima vez que ele for usado, relendo o `Environment` já atualizado. O gatilho é o endpoint do Actuator:

```bash
curl -X POST http://localhost:8080/actuator/refresh
```

Sem `@RefreshScope`, o valor injetado por `@Value` ou `@ConfigurationProperties` fica "congelado" no que foi lido no boot — voltaremos a isso nas armadilhas.

### Spring Cloud Bus e o contraste com ConfigMap do k8s

`/actuator/refresh` resolve **uma instância**. Se o serviço `pedidos` tem dez réplicas, você teria que chamar o endpoint dez vezes. O **Spring Cloud Bus** elimina esse trabalho manual: ele conecta as instâncias por um **broker de mensagens** (RabbitMQ ou Kafka, via Spring Cloud Stream) e expõe `/actuator/busrefresh`. Uma chamada nesse endpoint emite um `RefreshRemoteApplicationEvent` no broker; **todas** as instâncias inscritas o recebem e se refrescam.

Dá para fechar o laço com **push notifications**: provedores de Git (GitHub, GitLab, Bitbucket, etc.) chamam o endpoint `/monitor` do server via webhook quando há commit na config; o server traduz isso num evento de bus e dispara o refresh automaticamente. Resultado: `git push` na config → frota inteira atualizada, sem intervenção.

> [!question] E o ConfigMap/Secret do Kubernetes, então?
> O k8s já oferece **config nativa**: `ConfigMap` para valores e `Secret` para dados sensíveis, montados como variáveis de ambiente ou arquivos no pod. Onde fica o Spring Cloud Config?

O trade-off, sem dogma:

- **A favor do Spring Cloud Config**: versionamento e auditoria de config como Git de primeira classe; `@RefreshScope` para refrescar **bean a bean** sem reiniciar o pod; portabilidade para fora do k8s (VMs, bare metal, outro orquestrador). A semântica de `{application}/{profile}/{label}` é rica e específica de Spring.
- **A favor do ConfigMap/Secret nativo**: zero infraestrutura extra — você não opera mais um serviço (o Config Server) que pode virar ponto único de falha; integra com o ciclo de vida do pod; Secrets têm suporte nativo a cifragem em repouso e RBAC. Em plataformas k8s-first, recarregar config costuma significar **recriar o pod** (rollout), o que é simples e auditável por si só.

Em projetos novos rodando inteiramente em Kubernetes, a config nativa frequentemente é suficiente e mais leve. O Spring Cloud Config brilha em ambientes híbridos, legados ou onde o refresh granular sem restart é um requisito real.

## Na prática

**Config Server** (`application.yml`), apontando para um backend Git:

```yaml
server:
  port: 8888

spring:
  application:
    name: config-server
  cloud:
    config:
      server:
        git:
          uri: https://git.exemplo.com/plataforma/config-repo
          default-label: main
          try-master-branch: true
          # um repo por serviço: uri: https://git.exemplo.com/config/{application}
```

A classe de entrada:

```java
@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}
```

No `config-repo`, um arquivo por serviço/perfil. Ex.: `pedidos-prod.yml`:

```yaml
pedidos:
  timeout-ms: 2000
  max-itens: 50
```

**Config Client** (serviço `pedidos`), em `application.yml`:

```yaml
spring:
  application:
    name: pedidos
  profiles:
    active: prod
  config:
    import: "optional:configserver:http://localhost:8888"

management:
  endpoints:
    web:
      exposure:
        include: refresh, busrefresh
```

Um bean que relê a config no refresh:

```java
@Component
@RefreshScope
public class PedidosConfig {

    @Value("${pedidos.timeout-ms}")
    private int timeoutMs;

    public int getTimeoutMs() {
        return timeoutMs;
    }
}
```

Trocou `pedidos.timeout-ms` no Git e quer aplicar agora, em toda a frota:

```bash
# uma instância só:
curl -X POST http://pedidos-1:8080/actuator/refresh

# todas as instâncias, via Spring Cloud Bus:
curl -X POST http://pedidos-1:8080/actuator/busrefresh
```

## Armadilhas

### (1) Segredo em Git plano, sem cifragem nem Vault

Commitar senha, token ou chave em texto puro no repositório de config é o erro clássico: qualquer um com acesso de leitura ao repo — e ao seu **histórico** — vê o segredo, mesmo depois de você "removê-lo" num commit posterior. O Config Server oferece cifragem (`{cipher}...`) e o backend Vault existe justamente para segredos. A *operação* desse Vault em produção é do **Galho 17 (planejado)**; o ponto aqui é não tratar dado sensível como propriedade comum.

### (2) Refresh sem `@RefreshScope`: o bean não atualiza

Você muda o valor no Git, chama `/actuator/refresh`, o endpoint responde com sucesso — e o comportamento não muda. Causa quase sempre: o bean que usa a propriedade **não tem `@RefreshScope`**. Beans singleton comuns leem o `@Value` uma vez, no boot, e ficam com aquele valor para sempre. Só beans em refresh scope (ou `@ConfigurationProperties`, que tem tratamento próprio) releem do `Environment` atualizado. O endpoint funcionar não garante que o bento certo foi marcado.

### (3) Config Server como SPOF, sem fallback local

Se o cliente usa `configserver:...` em modo **fail-fast** e o Config Server está fora no exato momento do boot — durante um deploy em cascata, por exemplo — a app **não sobe**. Centralizar tudo num único server cria um ponto único de falha no caminho crítico de inicialização. Mitigações: `optional:` para degradar com elegância (a app sobe com defaults locais), `retry` para tolerar indisponibilidade transitória, e múltiplas instâncias do server atrás de um balanceador. Centralização sem rede de proteção transfere a fragilidade do código para a infraestrutura.

## Em entrevista

### Frase pronta (inglês)

> Spring Cloud Config externalizes configuration into a central Config Server that reads from a versioned backend like Git, Vault, or JDBC, and each microservice acts as a Config Client that pulls its properties by application, profile, and label. When a property changes, beans annotated with `@RefreshScope` are rebuilt on a `POST` to `/actuator/refresh`, so I can change a value without redeploying. To propagate that refresh across every instance at once, I add Spring Cloud Bus, which broadcasts the refresh event over a message broker such as RabbitMQ or Kafka. On a Kubernetes-only stack I'd weigh this against native ConfigMaps and Secrets, which avoid running an extra server but typically refresh config by recreating the pod rather than per-bean.

### Vocabulário

| Português | Inglês |
| --- | --- |
| configuração centralizada | centralized config |
| escopo de refresh | refresh scope |
| propriedade | property |
| ambiente | environment |
| segredo | secret |
| backend de config | config backend |
| ponto único de falha | single point of failure |
| ele falha rápido | it fails fast |

## Veja também

- [[03-Dominios/Java/Microservices e sistemas distribuídos/03 - Os 12 fatores e o serviço cloud-native|Os 12 fatores]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/04 - Panorama do Spring Cloud — e o que morreu|Panorama do Spring Cloud]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Spring Cloud Config — Reference Documentation. https://docs.spring.io/spring-cloud-config/reference/ (Config Server, backends Git/Vault/JDBC, Config Client, push notifications e Bus)
- Spring Cloud Config — Config Client. https://docs.spring.io/spring-cloud-config/reference/client.html (`spring.config.import`, `optional:`/fail-fast, retry, múltiplas URIs)
- Spring Cloud Config — Git Backend. https://docs.spring.io/spring-cloud-config/reference/server/environment-repository/git-backend.html (`spring.cloud.config.server.git.uri`, placeholders, `default-label`/`try-master-branch`)
- Spring Cloud Config — Push Notifications and Spring Cloud Bus. https://docs.spring.io/spring-cloud-config/reference/server/push-notifications-and-bus.html (`/monitor`, `/actuator/busrefresh`, brokers RabbitMQ/Kafka)
