---
title: "Os 12 fatores e o serviço cloud-native"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - microservices
  - iniciado
  - arquitetura
aliases:
  - "Os 12 fatores"
  - "Twelve-Factor App"
  - "12-factor"
---

# Os 12 fatores e o serviço cloud-native

> [!abstract] TL;DR
> Os **12 fatores** (Twelve-Factor App) são uma metodologia de 2011, escrita por **Adam Wiggins** a partir da experiência da Heroku, para construir serviços que rodam bem na nuvem. Pensa no seu serviço como um processo **sem estado** (stateless), que lê sua **configuração do ambiente**, trata banco e fila como **recursos anexados** (backing services), pode ser **descartado** a qualquer momento (disposability) e **escreve logs no stdout** como um fluxo de eventos. Esses cinco — config, backing services, stateless, disposability, logs — são o coração arquitetural. A parte de empacotar e implantar (build/release/run, containers) é território do galho de empacotamento e entrega, planejado.

## O que é

A **Twelve-Factor App** é um conjunto de doze regras de bom comportamento para aplicações que vivem na nuvem. Adam Wiggins e a equipe da Heroku publicaram o manifesto em 2011 (o texto foi revisado depois, em 2017) depois de ver milhares de aplicações subirem e quebrarem na plataforma. Eles destilaram os padrões que separavam os serviços que escalavam tranquilos dos que davam dor de cabeça.

Pense nos 12 fatores como um **checklist de higiene** para um serviço. Cada fator é uma frase imperativa: "armazene config no ambiente", "execute o app como processos sem estado", "trate logs como fluxos de eventos". Nenhum deles fala de framework ou linguagem específica — são princípios de arquitetura que valem para Java, Go, Python ou qualquer outra coisa.

Por que isso importa para microservices? Porque um microservice **é** justamente esse tipo de serviço: pequeno, replicável, descartável, configurado de fora. Os 12 fatores são a cartilha de como cada peça do seu sistema distribuído deve se comportar para que a orquestração (escalar, reiniciar, mover de máquina) funcione sem surpresas.

Mais tarde, em 2016, **Kevin Hoffman** escreveu **Beyond the Twelve-Factor App**, atualizando e ampliando a lista para a era dos containers e do cloud-native moderno (adicionando fatores como telemetria e segurança/autenticação). Aqui ficamos no manifesto original; basta saber que existe essa continuação.

## Por que importa

O contrato implícito de um serviço cloud-native é simples: **a plataforma pode me criar, matar, replicar e mover a qualquer hora, e eu não posso reclamar.** Os 12 fatores são as condições que tornam esse contrato possível.

- Se a config está **no ambiente** e não no jar, a mesma imagem do serviço roda em dev, staging e produção mudando só variáveis. Não preciso recompilar para trocar o host do banco.
- Se o processo é **stateless**, o orquestrador pode subir dez réplicas atrás de um load balancer e qualquer uma atende qualquer requisição. Escala horizontal vira só "aumente o número de instâncias".
- Se o serviço é **descartável**, posso fazer deploy rolando réplicas novas e derrubando as velhas sem perder requisição.
- Se os **logs vão para o stdout**, a plataforma coleta tudo de forma uniforme, sem cada serviço inventar seu próprio arquivo e sua própria rotação.

Sem isso, você tem um serviço que "só roda na minha máquina", guarda sessão na memória, escreve log num caminho fixo do disco e precisa de carinho manual para reiniciar — exatamente o oposto do que um sistema distribuído precisa.

## Como funciona

### Os 12 fatores

Esta é a lista canônica, com os nomes exatos do manifesto:

| #     | Fator                | Em uma linha                                              |
| ----- | -------------------- | -------------------------------------------------------- |
| I     | **Codebase**         | Um codebase versionado, muitos deploys                   |
| II    | **Dependencies**     | Declare e isole dependências explicitamente              |
| III   | **Config**           | Armazene config no ambiente                              |
| IV    | **Backing Services** | Trate serviços de apoio como recursos anexados           |
| V     | **Build, Release, Run** | Separe estritamente as etapas de build e run          |
| VI    | **Processes**        | Execute o app como um ou mais processos sem estado       |
| VII   | **Port Binding**     | Exporte serviços via port binding                        |
| VIII  | **Concurrency**      | Escale horizontalmente pelo modelo de processos          |
| IX    | **Disposability**    | Maximize robustez com startup rápido e shutdown gracioso |
| X     | **Dev/Prod Parity**  | Mantenha dev, staging e produção o mais parecidos possível |
| XI    | **Logs**             | Trate logs como fluxos de eventos                        |
| XII   | **Admin Processes**  | Rode tarefas administrativas como processos pontuais     |

> [!note] Fronteira do empacotamento e entrega
> O fator **V (Build, Release, Run)** e tudo que cerca containers e pipeline de implantação são tratados a fundo no galho de empacotamento e entrega de microservices, ainda **(planejado)**. Aqui só os mencionamos. Nesta nota o foco é a **arquitetura do serviço em execução**, não como ele é empacotado e implantado.

### Os fatores arquiteturais em destaque

Cinco fatores definem o formato do serviço enquanto ele roda. São esses que você desenha quando esboça a arquitetura de um microservice.

#### Config (III) — configuração no ambiente

O manifesto manda **separar estritamente config de código**. Tudo que muda entre ambientes (URL do banco, credenciais, endpoint de uma API externa, feature flags) sai do código e vira **variável de ambiente**.

O teste de cheirinho do manifesto é elegante: *o codebase poderia ser tornado open source a qualquer momento sem vazar nenhuma credencial?* Se a senha do banco está num `application.yml` commitado, a resposta é não.

Repare que isso **não** quer dizer "jogue toda configuração interna em env var". Coisas que não mudam entre deploys — como o mapeamento de rotas ou a fiação de módulos do framework — continuam no código. Env var é para o que **varia por deploy**.

#### Backing Services (IV) — recursos anexados

Um **backing service** é qualquer serviço que o app consome pela rede: banco de dados, fila de mensagens (RabbitMQ, Kafka), cache (Redis, Memcached), serviço de e-mail, API de terceiros (S3, um gateway de pagamento). O fator diz: trate todos como **recursos anexados**, plugados via configuração.

A ideia-chave é que o código **não distingue** entre um serviço local e um de terceiros. Trocar um MySQL que você mesmo administra por um RDS gerenciado deve ser só mudar a URL na config — zero alteração de código. O recurso é "anexado" ou "desanexado" do deploy como quem pluga um cabo. Isso dá um acoplamento frouxo que vale ouro: um banco que falhou pode ser substituído por uma réplica sem mexer no serviço.

#### Processes (VI) — processos sem estado

Este é o fator mais importante para escala. O serviço roda como processos **stateless e share-nothing**: cada instância não guarda nada entre requisições que não possa perder.

> [!warning] Sticky sessions são proibidas
> O manifesto é taxativo: *"Sticky sessions são uma violação do twelve-factor e nunca devem ser usadas ou confiáveis."* Sessão de usuário vai para um datastore externo (Redis, banco), nunca para a memória do processo.

Cache de uma única transação dentro do processo é tolerável, mas o app **nunca assume** que algo em memória ou disco estará lá na próxima requisição — porque escala horizontal e reinícios mandam a próxima requisição para outra instância. Todo estado persistente é delegado a um backing service. É a combinação **stateless + backing service** que permite subir N réplicas idênticas atrás de um balanceador.

#### Disposability (IX) — descartabilidade

Os processos são **descartáveis**: podem ser iniciados ou parados a qualquer momento. Isso exige duas coisas:

- **Startup rápido** — idealmente segundos. Quanto mais rápido um processo sobe, mais ágil é escalar e mover serviços entre máquinas.
- **Shutdown gracioso** — ao receber um `SIGTERM` do gerenciador de processos, o serviço para de aceitar requisições novas, deixa as em andamento terminarem, e sai. Um worker de fila devolve o job não processado para a fila (NACK no RabbitMQ) antes de morrer.

E há a robustez contra **morte súbita**: hardware falha, o processo morre sem aviso. Por isso jobs devem ser **idempotentes** ou reentrantes, e a fila deve devolver o trabalho de quem desconectou. Quem está acostumado com microservices reconhece aqui o princípio do *crash-only design*: projetar para morrer e renascer limpo, sempre.

#### Logs (XI) — fluxo de eventos

Logs são um **fluxo de eventos ordenados no tempo**, não arquivos. O fator é sobre o que o app **não** faz: ele *nunca se preocupa com roteamento ou armazenamento* dos seus logs.

Cada processo escreve no `stdout`, sem buffer, e pronto. Quem captura, agrega, roteia e armazena é o **ambiente de execução** (a plataforma, o agregador de logs). O mesmo fluxo bruto pode ser visto em tempo real no terminal durante o desenvolvimento, arquivado, ou mandado para uma ferramenta de análise. O serviço fica blissfully ignorante de para onde o log vai — e é exatamente isso que se quer num sistema distribuído com dezenas de réplicas.

## Na prática

Um `order-service` cloud-native lê toda a sua config do ambiente. No `application.yml` (Spring Boot), você nunca crava o valor — referencia a variável de ambiente, com um default só para desenvolvimento local:

```yaml
# application.yml — config vem do ambiente (fator III)
server:
  port: ${SERVER_PORT:8080}

spring:
  application:
    name: order-service
  datasource:
    # backing service como recurso anexado (fator IV):
    # trocar de host = trocar a env var, sem recompilar
    url: ${ORDER_DB_URL:jdbc:postgresql://localhost:5432/orders}
    username: ${ORDER_DB_USER:orders}
    password: ${ORDER_DB_PASSWORD}   # sem default: obrigatório vir do ambiente
  data:
    redis:
      # sessão e cache externos, porque o processo é stateless (fator VI)
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}

logging:
  pattern:
    # logs vão para o stdout; o ambiente coleta (fator XI)
    console: "%d{ISO8601} %-5level [%X{traceId}] %logger{36} - %msg%n"
```

E o serviço em si é **stateless**: nada de guardar o carrinho ou a sessão num `Map` em memória.

```java
@RestController
@RequestMapping("/orders")
class OrderController {

    private final OrderService orders;     // delega persistência ao banco
    private final SessionStore sessions;   // backing service (Redis), não memória

    OrderController(OrderService orders, SessionStore sessions) {
        this.orders = orders;
        this.sessions = sessions;
    }

    @PostMapping
    OrderView place(@RequestBody OrderRequest req,
                    @RequestHeader("X-Session") String sessionId) {
        // estado de sessão vem de um backing service, não da memória local:
        // qualquer réplica atrás do balanceador atende esta requisição
        Cart cart = sessions.load(sessionId);
        return orders.place(cart, req);    // grava no banco (recurso anexado)
    }
}
```

Como nenhuma das dez réplicas guarda estado próprio, o orquestrador escala horizontalmente (fator VIII) só aumentando o número de instâncias, e um `SIGTERM` derruba qualquer uma sem perda (fator IX).

## Armadilhas

### (1) Estado na memória do processo

O serviço guarda sessão, carrinho ou cache "para ir mais rápido" num campo de instância:

```java
// ❌ quebra stateless (VI), escala (VIII) e disposability (IX)
private final Map<String, Cart> carrinhos = new ConcurrentHashMap<>();
```

Funciona perfeitamente com **uma** instância. Aí você sobe a segunda réplica, o balanceador manda a próxima requisição do mesmo usuário para ela, e o carrinho "sumiu". A solução de gente desesperada é ligar **sticky sessions** no balanceador — que o manifesto proíbe explicitamente. E quando essa instância morre (deploy, falha), o carrinho de quem estava nela evapora.

**Fix:** mova o estado para um backing service externo (Redis, banco). O processo só orquestra; o estado mora fora dele.

```java
// ✅ estado num recurso anexado; qualquer réplica atende, qualquer uma pode morrer
Cart cart = sessions.load(sessionId);   // Redis
```

### (2) Config cravada no jar em vez do ambiente

A senha do banco e a URL de produção vão direto no `application.yml` commitado:

```yaml
# ❌ viola Config (III): credencial no código, config por ambiente impossível
spring:
  datasource:
    url: jdbc:postgresql://prod-db.interno:5432/orders
    password: S3nh4Pr0duc40
```

Dois problemas. Primeiro, a credencial vazou no Git para sempre (falha o teste do "poderia ser open source?"). Segundo, para rodar em staging você precisa **recompilar** com outro valor — a mesma imagem não serve para dois ambientes, o que joga fora metade do benefício de ser cloud-native.

**Fix:** referencie a variável de ambiente e injete o segredo na hora do deploy (via secret manager / variáveis da plataforma).

```yaml
# ✅ config no ambiente: mesma imagem em dev, staging e prod
spring:
  datasource:
    url: ${ORDER_DB_URL}
    password: ${ORDER_DB_PASSWORD}
```

### (3) Logar em arquivo com caminho fixo

O serviço configura um `FileAppender` apontando para `/var/log/order-service/app.log`.

Num servidor único isso funcionava. Em N réplicas efêmeras, cada uma escreve seu próprio arquivo num disco que some quando a réplica morre, e ninguém consegue ver o fluxo agregado.

**Fix:** escreva no `stdout` e deixe o ambiente de execução coletar, agregar e rotear (fator XI). O serviço não decide para onde o log vai.

## Em entrevista

### Frase pronta (inglês)

> The Twelve-Factor App methodology, written by Adam Wiggins at Heroku in 2011, is my mental checklist for designing a cloud-native service. For the architecture of the running process, the factors I care about most are config in the environment, backing services as attached resources, stateless processes, disposability, and logs as event streams. Keeping a service stateless and reading its config from environment variables is what lets the orchestrator scale it horizontally and replace any instance without losing a request. Kevin Hoffman's "Beyond the Twelve-Factor App" from 2016 extends the list for the container era, but the original five architectural factors are still the ones I reach for first.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| fator | factor |
| sem estado | stateless |
| serviço de apoio (banco, fila, cache, API externa como recursos anexados) | backing service / attached resource |
| descartabilidade (startup rápido, shutdown gracioso com `SIGTERM`) | disposability |
| paridade dev-prod | dev/prod parity |
| fluxo de eventos (logs no stdout, coletados pelo ambiente) | event stream |
| escalar horizontalmente | scale out / scale horizontally |
| separação de config e código | separation of config from code |

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/01 - O que são microservices e a tese honesta|O que são microservices]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/12 - Config centralizado — Spring Cloud Config|Config centralizado]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Wiggins, Adam. **The Twelve-Factor App**. 2011 (rev. 2017). <https://12factor.net/>
  - III. Config — <https://12factor.net/config>
  - IV. Backing Services — <https://12factor.net/backing-services>
  - VI. Processes — <https://12factor.net/processes>
  - IX. Disposability — <https://12factor.net/disposability>
  - XI. Logs — <https://12factor.net/logs>
- Hoffman, Kevin. **Beyond the Twelve-Factor App**. O'Reilly, 2016. (Atualização do manifesto para a era cloud-native / containers.)
