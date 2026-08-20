---
title: "Panorama do Spring Cloud — e o que morreu"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - microservices
  - iniciado
  - spring-cloud
aliases:
  - "Panorama do Spring Cloud"
  - "Spring Cloud release train"
---

# Panorama do Spring Cloud — e o que morreu

> [!abstract] TL;DR
> O **Spring Cloud** não é uma biblioteca única: é um **guarda-chuva** de projetos (Config, Gateway, LoadBalancer, OpenFeign, Circuit Breaker, Consul, Kubernetes…) versionados em conjunto por um **release train** com nome de estação de metrô de Londres. O trem mais novo é o **2025.1.x "Oakwood"** (alinhado ao **Spring Boot 4.0.x**), coexistindo com o **2025.0.x "Northfields"** (Spring Boot **3.5.x**), ainda mantido. O que mais confunde recém-chegados é o **passado morto**: o stack Netflix de 2015 — **Zuul 1**, **Ribbon** e **Hystrix** — foi **removido** do Spring Cloud no trem **2020.0.0 "Ilford"** (GA jan/2021). Substitutos modernos: Zuul→**Spring Cloud Gateway**, Ribbon→**Spring Cloud LoadBalancer**, Hystrix→**Resilience4j** (via Spring Cloud Circuit Breaker), Sleuth→**Micrometer Tracing**. Mas atenção: **Eureka NÃO morreu** — segue vivo e mantido. "O Netflix stack morreu" é meia-verdade perigosa.

## O que é

O Spring Cloud é um conjunto de ferramentas que resolve os problemas recorrentes de **sistemas distribuídos** em cima do Spring Boot: configuração centralizada, descoberta de serviços, roteamento de borda (gateway), balanceamento de carga no cliente, resiliência (circuit breaker), rastreamento distribuído, mensageria. Cada um desses é um **projeto independente** com seu próprio repositório e número de versão.

O elo que costura todos eles é o **release train** — o conceito central desta nota.

> [!info] Por que "trem"?
> Imagine uma estação de metrô. O "trem" parte com vários vagões (os projetos) que combinam entre si. Você não escolhe a versão de cada vagão individualmente; você embarca no **trem inteiro**, e o Spring garante que aquela combinação de versões foi testada junta. Cada trem ganha um **codinome de estação de metrô de Londres** em ordem alfabética (Ilford, Jubilee, Kilburn, Leyton, Moorgate, Northfields, Oakwood…). Desde 2020 o nome técnico virou um ano: `2020.0.x`, `2025.1.x` etc.

Concretamente: você não declara `spring-cloud-config:4.3.0` e `spring-cloud-gateway:4.3.0` à mão. Você importa **um único BOM** (`spring-cloud-dependencies`) com a versão do trem, e ele resolve a versão certa de cada módulo.

## Por que importa

Três motivos práticos:

1. **Compatibilidade com o Boot.** Cada trem é casado com uma **geração específica do Spring Boot**. Errar essa amarração é a causa nº 1 de `NoSuchMethodError` e `ClassNotFoundException` em runtime. Saber "qual trem pra qual Boot" é conhecimento de sobrevivência.
2. **O cemitério.** Metade dos tutoriais de microsserviços Java que você encontra na web ainda ensinam **Zuul, Ribbon e Hystrix** — componentes **removidos há anos**. Reconhecer o que está morto evita escrever código que nem compila no Spring Cloud atual.
3. **Mapa do galho.** O Spring Cloud é a espinha dorsal das próximas notas deste galho. Saber quem é quem (Gateway, LoadBalancer, Circuit Breaker, Config) é o índice mental do resto da trilha.

## Como funciona

### O release train (Oakwood / Northfields e o baseline de Boot)

O release train versiona dezenas de projetos como uma unidade. A amarração com o Spring Boot é a informação crítica. Pela tabela oficial do projeto (spring.io/projects/spring-cloud, consultada jun/2026):

| Release train | Codinome | Baseline Spring Boot | Situação |
| --- | --- | --- | --- |
| **2025.1.x** | **Oakwood** | **4.0.x** | Mais recente |
| **2025.0.x** | **Northfields** | **3.5.x** | Mantido |
| 2024.0.x | Moorgate | 3.4.x | Mantido |
| 2023.0.x | Leyton | 3.2.x / 3.3.x | Mantido |
| 2022.0.x | Kilburn | 3.0.x / 3.1.x | Fim de vida |
| 2021.0.x | Jubilee | 2.6.x / 2.7.x | Fim de vida |
| 2020.0.x | **Ilford** | 2.4.x / 2.5.x | Fim de vida (o trem da grande remoção) |

O **Oakwood** é a virada de era: acompanha o **Spring Boot 4 / Spring Framework 7**, com os módulos do Spring Cloud na linha **5.0.x** (ex.: Spring Cloud Netflix 5.0.2), Jackson 3 e anotações de nulidade **JSpecify**. O **Northfields** segue como a opção estável sobre o **Boot 3.5.x** — Boot 4 já saiu, mas o ramo 3.x continua mantido. Os dois coexistem: a migração para Boot 4/Oakwood é uma escolha, não uma obrigação imediata.

> [!tip] Regra de bolso da escolha do trem
> Olhe primeiro a sua versão do **Spring Boot**; ela determina o trem. Boot 4.0.x → Oakwood; Boot 3.5.x → Northfields; Boot 3.4.x → Moorgate. Nunca o contrário.

### Os projetos principais (quem é quem)

Cada linha aponta a nota futura deste galho (algumas planejadas):

| Projeto | Faz o quê | Onde aprofunda |
| --- | --- | --- |
| **Spring Cloud Config** | Configuração centralizada e externa | (planejado) |
| **Spring Cloud Gateway** | Gateway / roteamento de borda (sucessor do Zuul) | (planejado) |
| **Spring Cloud LoadBalancer** | Balanceamento de carga **no cliente** (sucessor do Ribbon) | [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer\|Spring Cloud LoadBalancer]] |
| **Spring Cloud OpenFeign** | Cliente HTTP declarativo entre serviços | (planejado) |
| **Spring Cloud Circuit Breaker** | Abstração de resiliência (back-end: Resilience4j) | [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker\|Circuit Breaker]] |
| **Spring Cloud Netflix (Eureka)** | Service discovery (**Eureka segue vivo**) | [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka\|Service discovery e Eureka]] |
| **Spring Cloud Consul** | Discovery + config via HashiCorp Consul | (planejado) |
| **Spring Cloud Kubernetes** | Discovery + config usando primitivas do K8s | (planejado) |

> [!info] Tracing virou "core"
> O antigo **Spring Cloud Sleuth** **não** está mais nesta lista. Com o Spring Boot 3, o rastreamento distribuído migrou para o **Micrometer Tracing** (via Observation API), agora parte do núcleo de observabilidade do Spring — não é mais um módulo do Spring Cloud. Aprofunda em [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|Tracing distribuído]].

### O que morreu — e o substituto de cada um

Em 2018 o Netflix anunciou que vários de seus componentes OSS entravam em **maintenance mode** (sem novas features). O Spring Cloud seguiu o movimento e, no trem **2020.0.0 "Ilford"** (GA **27/01/2021**, RC em dez/2020), **removeu** os módulos de fato — eles deixaram de existir no classpath.

| Morreu (Netflix, removido) | Substituto oficial | Projeto Spring Cloud |
| --- | --- | --- |
| **Zuul 1** (gateway) | **Spring Cloud Gateway** | spring-cloud-gateway |
| **Ribbon** (client-side LB) | **Spring Cloud LoadBalancer** | spring-cloud-loadbalancer |
| **Hystrix** (circuit breaker) | **Resilience4j** | spring-cloud-circuitbreaker (Resilience4j) |
| **Archaius / Turbine** | — (sem porte direto) | (descontinuados) |
| **Spring Cloud Sleuth** (tracing) | **Micrometer Tracing** | (movido para o core do Boot 3) |

A página oficial de maintenance mode do Spring Cloud Netflix lista **Archaius, Hystrix (e dashboard/stream), Ribbon, Turbine (e turbine-stream) e Zuul** como em manutenção. A partir do trem 2020.0.0, os artefatos `spring-cloud-netflix-ribbon`, `-hystrix`, `-zuul` (e seus starters) foram **removidos** do release train.

> [!warning] "Maintenance mode" não é "ainda usável de boa"
> Em manutenção significa: sem features novas, só correções críticas de bug/segurança — **enquanto durou**. Para Zuul/Ribbon/Hystrix isso já evoluiu para **removido**. Você não consegue mais puxar o starter do Zuul num projeto Spring Cloud atual.

### Eureka segue vivo

O ponto que mais gera confusão: **nem tudo do Netflix morreu**. O **Eureka** (servidor e cliente de service discovery) **não está em maintenance mode** e segue **ativamente mantido** dentro do Spring Cloud Netflix (módulo na linha **5.0.x** no Oakwood — p.ex. **5.0.2**; **4.3.0** no Northfields). Só o conjunto **Archaius / Hystrix / Ribbon / Turbine / Zuul** está em manutenção/removido.

> [!example] Feynman: a casa do Netflix
> Pense no "Netflix stack" como uma casa antiga com cinco cômodos. Quatro foram demolidos (Zuul, Ribbon, Hystrix, Turbine/Archaius) e substituídos por construções novas no lote ao lado (Gateway, LoadBalancer, Resilience4j). **Um cômodo continua de pé, reformado e em uso: o Eureka.** Dizer "demoliram a casa" está errado — demoliram parte dela.

## Na prática

Mapa mental projeto × estado:

```text
PROJETO                       ESTADO        SUBSTITUTO / OBSERVAÇÃO
-----------------------------------------------------------------------------
Eureka (discovery)            VIVO          mantido (Netflix 5.0.x @ Oakwood)
Spring Cloud Gateway          VIVO          sucessor do Zuul
Spring Cloud LoadBalancer     VIVO          sucessor do Ribbon
Spring Cloud Circuit Breaker  VIVO          back-end: Resilience4j
Spring Cloud Config           VIVO          config centralizada
Spring Cloud OpenFeign        VIVO          cliente HTTP declarativo
Micrometer Tracing            VIVO          sucessor do Sleuth (core do Boot 3+)
-----------------------------------------------------------------------------
Zuul 1                        MORTO         -> Spring Cloud Gateway
Ribbon                        MORTO         -> Spring Cloud LoadBalancer
Hystrix                       MORTO         -> Resilience4j
Archaius / Turbine            MORTO         -> sem porte direto
Spring Cloud Sleuth           APOSENTADO    -> Micrometer Tracing
```

A amarração de versões vem de **um único import** no `pom.xml` — o BOM `spring-cloud-dependencies` com a versão do trem. Daí em diante, cada starter entra **sem versão** (o BOM resolve):

```xml
<!-- Escolha do trem: aqui o Northfields (Spring Boot 3.5.x) -->
<properties>
  <spring-cloud.version>2025.0.2</spring-cloud.version>
</properties>

<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.cloud</groupId>
      <artifactId>spring-cloud-dependencies</artifactId>
      <version>${spring-cloud.version}</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <!-- Sem versão: o BOM do trem resolve a combinação testada -->
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-gateway</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-circuitbreaker-resilience4j</artifactId>
  </dependency>
</dependencies>
```

> [!note] Para Oakwood / Boot 4
> Troque a propriedade para a versão do trem **2025.1.x** (Oakwood) e suba o `spring-boot-starter-parent` para **4.0.x**. Boot e trem andam juntos — não misture Boot 3.5 com Oakwood nem Boot 4 com Northfields.

## Armadilhas

### (1) Usar Zuul / Ribbon / Hystrix hoje

Tutoriais de 2017–2019 ainda dominam os resultados de busca e ensinam `spring-cloud-starter-netflix-zuul`, `-ribbon` e `-hystrix`. **Esses artefatos foram removidos no trem 2020.0.0 "Ilford" (jan/2021)** e não existem mais nos trens atuais — a dependência simplesmente não resolve. Use os sucessores: **Gateway** (no lugar do Zuul), **LoadBalancer** (no lugar do Ribbon) e **Resilience4j** via Circuit Breaker (no lugar do Hystrix). Se um exemplo importa qualquer um dos três, é sinal de que está desatualizado.

### (2) Achar que "o Spring Cloud morreu junto com o Netflix stack"

A narrativa "o Netflix abandonou o OSS, então Spring Cloud está morto" é **falsa**. O que entrou em manutenção/foi removido foi um **subconjunto** específico (Zuul/Ribbon/Hystrix/Turbine/Archaius). O Spring Cloud está **muito vivo**: o trem **Oakwood** acabou de acompanhar o **Spring Boot 4** (Jackson 3, JSpecify). E mesmo dentro do Netflix, o **Eureka segue mantido**. Generalizar de "Hystrix morreu" para "Spring Cloud morreu" é erro de escopo.

### (3) Casar trem com a versão errada do Boot

Importar o BOM do **Oakwood (2025.1.x)** num projeto **Spring Boot 3.5** (ou Northfields num projeto Boot 4) produz incompatibilidades binárias sutis — compila, mas estoura em runtime. **Olhe sempre a tabela de baseline** antes de fixar a versão do trem: Boot 4.0.x → Oakwood; Boot 3.5.x → Northfields.

### (4) Confundir Resilience4j com um "Hystrix 2"

Resilience4j **não** é uma continuação do Hystrix — é uma biblioteca independente, modular e baseada em programação funcional. A versão **estável** mais recente é a linha **2.x** (**2.4.0**, mar/2025). Se algum gerador de respostas afirmar que existe um "Resilience4j 3.x estável", **desconfie** — não há 3.x estável publicado.

## Em entrevista

### Frase pronta (inglês)

> Spring Cloud is an umbrella of projects versioned together as a **release train**, with each train pinned to a specific Spring Boot generation — the latest is **Oakwood (2025.1.x)** on Boot 4, coexisting with **Northfields (2025.0.x)** on Boot 3.5. The legacy Netflix components — **Zuul, Ribbon, and Hystrix** — were moved to **maintenance mode** and then **removed** in the **2020.0.0 "Ilford"** train, so today you use **Spring Cloud Gateway**, **Spring Cloud LoadBalancer**, and **Resilience4j** (through Spring Cloud Circuit Breaker) instead, and **Micrometer Tracing** replaced Sleuth. One nuance people get wrong: **Eureka is still alive and maintained** — only that specific subset of Netflix modules was deprecated, not service discovery itself.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| trem de release (projetos versionados em bloco) | release train |
| descoberta de serviço(s) | service discovery |
| disjuntor (isola dependências falhas) | circuit breaker |
| balanceamento de carga no cliente | client-side load balancing |
| modo de manutenção (só correções críticas, sem features) | maintenance mode |
| depreciado (marcado para remoção futura) | deprecated |
| removido (já não existe no classpath) | removed / dropped |
| versão-base de compatibilidade (a geração do Boot do trem) | baseline |
| manifesto que fixa versões compatíveis de um bloco | BOM (Bill of Materials) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|Service discovery e Eureka]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer|Spring Cloud LoadBalancer]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Circuit Breaker (Resilience4j)]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|Tracing distribuído]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Spring Cloud — página do projeto e tabela de release trains. spring.io/projects/spring-cloud (consultado em 12/06/2026)
- Spring Cloud Release — Supported Versions (wiki). github.com/spring-cloud/spring-cloud-release/wiki/Supported-Versions (consultado em 12/06/2026)
- Spring Cloud Netflix — Modules in maintenance mode. cloud.spring.io/spring-cloud-netflix/multi/multi__modules_in_maintenance_mode.html (consultado em 12/06/2026)
- Spring Cloud 2020.0.0 (Ilford) Release Notes — remoção de Ribbon/Hystrix/Zuul; GA 27/01/2021. github.com/spring-cloud/spring-cloud-release/wiki (consultado em 12/06/2026)
- "Observability with Spring Boot 3" — Micrometer Tracing como sucessor do Sleuth. spring.io/blog/2022/10/12/observability-with-spring-boot-3 (consultado em 12/06/2026)
- Resilience4j — releases (estável 2.4.0, 14/03/2025). github.com/resilience4j/resilience4j/releases (consultado em 12/06/2026)
