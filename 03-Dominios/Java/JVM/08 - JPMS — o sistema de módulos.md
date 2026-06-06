---
title: "JPMS — o sistema de módulos"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - jvm
  - adepto
  - jpms
  - modulos
aliases:
  - "JPMS"
  - "module-info"
  - "Sistema de módulos"
  - "Java Platform Module System"
---

# JPMS — o sistema de módulos

> [!abstract] TL;DR
> O **JPMS** (Java Platform Module System, Java 9 — JEP 261) torna dependências e API pública **explícitas e checadas em compile e runtime**: um módulo declara o que precisa (`requires`) e o que expõe (`exports`); o resto fica encapsulado. O próprio JDK foi modularizado — e é daí que vem aquele `--add-opens` que seu framework exige: ele está tentando acessar internos que o JDK agora fecha por padrão. A boa notícia é que o classpath convive: a maioria das apps Spring roda no classpath como "unnamed module" sem escrever uma linha de `module-info.java`. Módulos são **opt-in**, não uma migração obrigatória.

## O que é

O JPMS introduziu um nível de agrupamento acima de pacotes e abaixo de JARs: o **módulo**. Cada módulo é uma unidade com **identidade** (nome), **dependências** declaradas (`requires`) e **API pública** explícita (`exports`). O que não é exportado não existe para quem está de fora — sem reflexo, sem acesso de compile, sem acesso de runtime.

Antes do JPMS, o classpath era literalmente um saco sem fundo: qualquer tipo de qualquer JAR era acessível a qualquer outro. Isso causava dois problemas crônicos:

- **JAR Hell**: versões conflitantes de uma mesma lib, carregadas em ordem imprevisível.
- **Acoplamento a internos da JDK**: código usando `sun.misc.Unsafe`, classes de `com.sun.*` e outros tipos que a Oracle nunca garantiu como API estável.

O JPMS resolve o segundo com **strong encapsulation** (encapsulamento forte): os pacotes internos do JDK só são acessíveis se explicitamente exportados. Isso afeta todo mundo — mesmo quem nunca escrever um `module-info.java`.

O classpath não desapareceu: JARs sem `module-info.java` continuam funcionando como antes, reunidos no **unnamed module**. Módulos são uma escolha, não uma imposição.

## Por que importa

**Strong encapsulation afeta TODO MUNDO, mesmo sem escrever module-info.** A partir do Java 16 (JEP 396), o acesso reflexivo a internos do JDK passou a ser bloqueado por padrão — o Java 17 (JEP 403) deu o passo seguinte, removendo a válvula `--illegal-access` por completo, sem possibilidade de retrocompatibilidade. Frameworks como Hibernate, Jackson, Spring e Lombok acessam fields e construtores privados de classes do JDK via reflection. Quando você atualiza o JDK e a aplicação explode com `InaccessibleObjectException` ou `IllegalAccessException`, isso é o JPMS fazendo o trabalho dele. Entender o mecanismo é a diferença entre resolver o problema em dois minutos e passar horas caçando a causa.

**Em entrevista**, perguntas sobre "Java 9+" invariavelmente tocam em JPMS. As armadilhas mais comuns: achar que o classpath morreu (não morreu), confundir `opens` com `exports` (são coisas diferentes — uma é para reflection, a outra é para compile/runtime direto), e não saber explicar o que um automatic module é.

**Em migração de legado**, o JPMS impõe um caminho gradual: unnamed module → automatic modules → módulos explícitos. Saber onde cada lib da stack está nesse caminho é pré-requisito para qualquer migração séria.

## Como funciona

### `module-info.java` (requires / requires transitive / exports / exports ... to)

O arquivo `module-info.java` fica na raiz do source tree e define o módulo. As diretivas principais:

```java
module com.example.orders {

    // Dependências diretas — o compilador e a JVM checam se os módulos estão presentes
    requires java.base;            // implícito: todo módulo requer java.base
    requires java.sql;
    requires com.example.catalog;

    // Dependência transitiva: quem depende de orders automaticamente "lê" com.example.domain
    // Útil quando um tipo de com.example.domain aparece na API pública de orders
    requires transitive com.example.domain;

    // Exporta o pacote para todos os módulos
    exports com.example.orders.api;

    // Exporta o pacote apenas para um módulo específico (amigo de módulo)
    exports com.example.orders.internal to com.example.admin;
}
```

**Diferença entre `requires` e `requires transitive`:** se `orders` usa `com.example.domain` apenas internamente, `requires` basta. Se um método público de `orders` retorna ou recebe um tipo de `com.example.domain`, então quem usa `orders` também precisa enxergar `com.example.domain` — e `requires transitive` evita que cada consumidor tenha que declarar a dependência explicitamente.

O compilador e a JVM verificam em startup que todos os módulos requeridos estão presentes e que não há ambiguidades. Isso elimina a surpresa do classpath em que uma versão errada de uma lib silenciosamente vencia outra.

### `opens` e reflection (por que Hibernate/Jackson precisam; opens vs exports)

`exports` concede acesso em **compile e runtime** aos tipos públicos de um pacote. Mas não permite reflection sobre membros privados.

`opens` concede acesso **em runtime via reflection** a **todos** os tipos e membros de um pacote — incluindo privados. Frameworks de injeção de dependência, ORMs e bibliotecas de serialização dependem exatamente disso para instanciar objetos e acessar fields sem getters.

```java
module com.example.orders {
    requires com.example.persistence;

    exports com.example.orders.api;

    // Abre o pacote de model para o módulo de persistência acessar via reflection
    // (ex.: Hibernate lendo @Column em fields privados)
    opens com.example.orders.model to com.example.persistence;

    // Abre para qualquer módulo — usar com cuidado
    opens com.example.orders.dto;
}
```

A distinção prática:

| Diretiva | Acesso compile | Acesso runtime (direto) | Reflection (privados) |
|----------|:--------------:|:------------------------:|:---------------------:|
| `exports pkg` | Sim | Sim | Não |
| `opens pkg` | Não | Não | Sim |
| `exports` + `opens` | Sim | Sim | Sim |

Quando o framework precisa de ambos (acessar os tipos e usar reflection), você usa as duas diretivas para o mesmo pacote.

### Services (uses / provides ... with — ServiceLoader de primeira classe)

O JPMS eleva o mecanismo de **service provider (ServiceLoader)** para nível de linguagem. Um módulo que consome um serviço declara `uses`; um módulo que implementa declara `provides ... with`:

```java
// Módulo consumidor
module com.example.orders {
    uses com.example.payments.PaymentGateway;
}

// Módulo provedor — não precisa exportar o pacote de implementação
module com.example.payments.stripe {
    requires com.example.payments;
    provides com.example.payments.PaymentGateway
        with com.example.payments.stripe.StripeGateway;
}
```

Em runtime, o consumidor usa `ServiceLoader`:

```java
ServiceLoader<PaymentGateway> loader = ServiceLoader.load(PaymentGateway.class);
loader.findFirst().ifPresent(gw -> gw.charge(order));
```

O desacoplamento é total: o módulo de pedidos não conhece o módulo Stripe — só a interface. Durante a resolução do módulo graph, a JVM inclui automaticamente todos os provedores dos serviços declarados com `uses`, garantindo que estarão disponíveis em runtime.

### Convivendo com o classpath (unnamed module, automatic modules, Automatic-Module-Name)

O JPMS foi projetado para coexistir com o mundo pré-módulos:

**Unnamed module:** todos os JARs no classpath — incluindo JARs que já têm `module-info.java` — são reunidos em um único módulo sem nome. Ele lê todos os módulos nomeados, mas nenhum módulo nomeado pode declarar `requires` nele (sem nome = sem endereço). Dentro do unnamed module, tudo é acessível a tudo, exatamente como no classpath clássico.

**Automatic modules:** um JAR sem `module-info.java` colocado no **module path** (não classpath) vira um automatic module. Ele recebe um nome derivado do filename do JAR — hífens viram pontos, sufixo de versão é removido. Por exemplo, `guava-32.1.jar` → módulo `guava`. Automatic modules podem ser requeridos por módulos explícitos, e leem (implicitamente) todos os outros módulos.

**O risco do automatic module sem `Automatic-Module-Name`:** o nome derivado do filename é instável. Se a lib lançar `guava-33.0.jar`, o nome muda. Se o module-info do seu módulo diz `requires guava;` e amanhã o JAR chama `com.google.guava`, seu build quebra. A solução: preferir libs que declaram `Automatic-Module-Name` no `MANIFEST.MF`:

```text
Automatic-Module-Name: com.google.guava
```

Com esse atributo, o nome é estável e independente do nome do arquivo. Libs que ainda não têm o atributo são candidatas a ficar no classpath (unnamed module) até migrarem para módulos explícitos.

### Strong encapsulation (da era --illegal-access ao deny por default no Java 17/JEP 403 — --add-opens e --add-exports como válvulas)

A transição para strong encapsulation foi gradual — e deliberada:

| Versão | Comportamento |
|--------|---------------|
| Java 9–15 | `--illegal-access=permit` por padrão: acesso reflexivo a internos do JDK gerava aviso mas funcionava |
| Java 16 | `--illegal-access=deny` por padrão: acesso bloqueado, flag ainda existia para reverter |
| **Java 17** (JEP 403) | `--illegal-access` **removida**: não existe mais. Acesso a internos do JDK via reflection é bloqueado sem exceção |

Em 2026, com Java 21+ como baseline de mercado, strong encapsulation é a realidade. Os frameworks modernos já se adaptaram — mas configs herdadas ou libs antigas ainda disparam o problema.

As duas válvulas de escape:

**`--add-exports módulo/pacote=módulo-destino`** — exporta o pacote em runtime (equivalente a um `exports` temporário):

```bash
java --add-exports java.base/sun.nio.ch=ALL-UNNAMED -jar app.jar
```

**`--add-opens módulo/pacote=módulo-destino`** — abre o pacote para reflection em runtime (equivalente a um `opens` temporário):

```bash
java --add-opens java.base/java.lang=ALL-UNNAMED -jar app.jar
```

`ALL-UNNAMED` como destino aplica ao unnamed module e a todos os automatic modules — o caso mais comum quando o código que precisa do acesso está no classpath.

Essas flags são o que frameworks Spring Boot, Hibernate e outros colocam em suas documentações de "requisitos de JDK". Elas são válvulas de emergência — corretas para módulos que não são seus e que ainda não adicionaram `opens`. Para módulos que você controla, a solução limpa é adicionar `opens` no `module-info.java`.

### `jlink` (runtime enxuto sob medida — menção curta como payoff)

Um dos payoffs do JDK modular: `jlink` cria uma distribuição de runtime contendo apenas os módulos necessários para a sua aplicação. Em vez de empacotar o JDK completo (~300 MB), o runtime gerado inclui só o que o module graph requer — resultando em imagens de **30–60 MB** em aplicações simples. Relevante para containers e imagens Docker enxutas; requer que a aplicação e todas as suas dependências sejam módulos explícitos.

## Na prática

Um `module-info.java` completo de uma aplicação hipotética de pedidos:

```java
module com.example.orders {

    // Dependências diretas
    requires java.sql;
    requires java.logging;

    // Transitivo: Order e OrderItem são parte da API pública
    requires transitive com.example.domain;

    // Framework de persistência hipotético
    requires com.example.persistence;

    // API pública: acessível para compile e runtime
    exports com.example.orders.api;
    exports com.example.orders.events;

    // Abre o pacote de entidades para o framework de persistência
    // acessar fields privados via reflection (ex.: mapeamento de colunas)
    opens com.example.orders.model to com.example.persistence;

    // Abre DTOs para serialização (ex.: biblioteca de JSON hipotética)
    opens com.example.orders.dto to com.example.json;

    // Serviços consumidos e fornecidos
    uses com.example.payments.PaymentGateway;
    provides com.example.notifications.OrderEventListener
        with com.example.orders.internal.DefaultOrderEventListener;
}
```

O erro clássico ao esquecer o `opens` — o framework tenta acessar um field via reflection e a JVM recusa:

```text
java.lang.reflect.InaccessibleObjectException: Unable to make field private
  java.lang.String com.example.orders.model.Order.customerId accessible:
  module com.example.orders does not "opens com.example.orders.model"
  to module com.example.persistence
    at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(...)
    at java.base/java.lang.reflect.Field.checkCanSetAccessible(...)
```

Os dois fixes possíveis:

**Fix 1 — módulo é seu:** adicionar `opens` no `module-info.java`:

```java
opens com.example.orders.model to com.example.persistence;
```

**Fix 2 — módulo não é seu** (lib de terceiro, código legado sem module-info): adicionar a flag na linha de comando:

```bash
java --add-opens com.example.orders/com.example.orders.model=com.example.persistence \
     -jar orders-service.jar
```

Em Spring Boot e outros frameworks, essa flag costuma aparecer em `JAVA_TOOL_OPTIONS` ou no `Dockerfile`. O Fix 2 é legítimo como medida temporária enquanto a lib não adiciona `opens` — não é gambiarra, é a válvula de escape projetada para esse caso.

## Armadilhas

### (1) Esquecer `opens` para o pacote que o framework acessa via reflection

**O problema:** o módulo exporta o pacote (para acesso de tipo) mas não o abre (para reflection). O código compila sem erros — o problema só aparece em runtime, quando o framework tenta acessar um field ou construtor privado:

```text
InaccessibleObjectException: Unable to make field private ...Order.customerId
  accessible: module com.example.orders does not "opens com.example.orders.model"
```

Frameworks de ORM, injeção de dependência e serialização são os casos mais comuns. A confusão nasce porque `exports` parece suficiente — mas `exports` não abre membros privados.

**Fix:**

```java
// No module-info.java do módulo que contém as entidades:
opens com.example.orders.model to com.example.persistence;

// Ou, se o módulo de destino não for conhecido (classpath / unnamed):
opens com.example.orders.model;
```

---

### (2) Depender de automatic module sem `Automatic-Module-Name`

**O problema:** ao modularizar a aplicação, você declara `requires guava;` porque o JAR `guava-32.1.jar` virou o automatic module `guava` no module path. Quando a lib lança `guava-33.0.jar` o nome continua `guava` — mas se o mantenedor mudar o nome do arquivo ou migrar para módulo explícito com nome diferente (`com.google.guava`), seu `module-info.java` quebra na compilação. O nome derivado de filename é uma promessa que a lib nunca fez.

**Fix:** antes de adicionar `requires` para uma lib como automatic module, verifique se o JAR declara `Automatic-Module-Name` no `META-INF/MANIFEST.MF`:

```bash
jar tf guava-32.1.jar | grep MANIFEST
jar xf guava-32.1.jar META-INF/MANIFEST.MF && grep Automatic-Module-Name META-INF/MANIFEST.MF
```

Se não declarar, a escolha mais segura é manter a lib no classpath (unnamed module) e não depender dela como módulo nomeado — até que a lib faça a migração corretamente.

---

### (3) Split packages — o mesmo pacote em dois módulos

**O problema:** o sistema de módulos proíbe que dois módulos distintos exportem o mesmo pacote. Se `module-a` e `module-b` ambos contêm `com.example.util`, a resolução do módulo graph falha com erro em startup — não em runtime aleatório:

```text
Error occurred during initialization of boot layer
java.lang.LayerInstantiationException: Package com.example.util in both
  module-a and module-b
```

Isso é mais comum em migrações: um pacote utilitário copiado para dois módulos durante a refatoração, ou uma lib que separou um pacote em dois JARs sem renomear.

**Fix:** reorganizar os pacotes para que cada um pertença a exatamente um módulo. Em projetos multi-módulo Maven/Gradle, auditar os pacotes antes de converter para módulos JPMS é passo obrigatório.

---

### (4) Achar que o classpath morreu

**O problema:** o JPMS foi lançado em 2017 e ainda hoje é comum encontrar a afirmação "o classpath foi descontinuado". Na prática: **a maioria das aplicações Spring Boot, Micronaut e Quarkus em produção em 2026 roda no classpath**, no unnamed module, sem um único `module-info.java`. O classpath funciona exatamente como antes — o que mudou é que o JDK em si agora tem módulos, e a strong encapsulation afeta o acesso aos internos do JDK mesmo para código no classpath.

Escrever módulos JPMS é uma decisão arquitetural — com benefícios reais de encapsulamento e habilitando `jlink` — mas **não é pré-requisito para usar Java 9+** nem "o jeito moderno" obrigatório de estruturar aplicações. Forçar módulos JPMS em código legado sem necessidade clara gera esforço de migração sem retorno proporcional.

**Fix:** avalie o custo-benefício. Módulos JPMS fazem mais sentido em frameworks, libs de plataforma e aplicações onde o isolamento de API e o tamanho do runtime são requisitos. Para a maioria das apps de negócio, o classpath com JDK atualizado é a resposta correta.

## Em entrevista

### Frase pronta (inglês)

> "JPMS, introduced in Java 9 as JEP 261, adds a module layer above packages: each module explicitly declares what it requires and what it exports, and the JVM enforces those boundaries at startup and at runtime. The key insight is that the JDK itself was modularized, which is why strong encapsulation now affects everyone — even code that never writes a module-info.java will hit InaccessibleObjectException if a framework tries to reflectively access JDK internals that are no longer open by default."

> "The --add-opens and --add-exports flags are the designed escape hatches for that situation: you use them when you don't own the module that needs to open, as a bridge until the library or framework catches up. For modules you do own, the clean solution is an opens directive in module-info.java scoped to the specific consuming module."

> "It's also worth being precise about the classpath: the unnamed module keeps it alive, so most Spring Boot applications run on the classpath today without any module-info.java, and that's perfectly valid. Automatic modules and jlink are the two stepping stones worth knowing — automatic modules let you depend on non-modular JARs from modular code during migration, and jlink lets you produce a stripped-down runtime image once everything is a named module."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| sistema de módulos | module system / JPMS |
| descritor de módulo | module descriptor |
| encapsulamento forte | strong encapsulation |
| módulo sem nome | unnamed module |
| módulo automático | automatic module |
| nome de módulo automático | Automatic-Module-Name |
| grafo de módulos | module graph |
| divisão de pacotes | split packages |
| abrir para reflection | open for reflection / opens directive |
| válvula de escape | escape hatch (--add-opens / --add-exports) |
| runtime sob medida | custom runtime image (via jlink) |
| resolução de módulos | module resolution |

## Veja também

- [[01 - A JVM — o que é e o pipeline de execução]]
- [[05 - Classloading e o delegation model]]
- [[14 - Performance da JVM — síntese]]
- [[03-Dominios/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#JPMS (module-info)|JPMS (Dicionário)]]

## Referências

- [JPMS Introduction — dev.java/learn/modules/intro/](https://dev.java/learn/modules/intro/)
- [Strong Encapsulation — dev.java/learn/modules/strong-encapsulation/](https://dev.java/learn/modules/strong-encapsulation/)
- [The Unnamed Module — dev.java/learn/modules/unnamed-module/](https://dev.java/learn/modules/unnamed-module/)
- [Services in JPMS — dev.java/learn/modules/services/](https://dev.java/learn/modules/services/)
- JEP 261: Module System (Java 9) — implementação do JPMS
- JEP 403: Strongly Encapsulate JDK Internals (Java 17) — remoção de `--illegal-access`, strong encapsulation sem válvula de retrocompatibilidade
