---
title: "O que é a camada de persistência — Spring Data, JPA e Hibernate"
created: 2026-06-09
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - persistencia
  - iniciado
  - jpa
aliases:
  - "camada de persistência"
  - "Spring Data JPA"
  - "ORM em Java"
---

# O que é a camada de persistência — Spring Data, JPA e Hibernate

> [!abstract] TL;DR
> A persistência num backend Spring não é uma coisa só — é uma **pilha de camadas**. O **Spring Data JPA** elimina o boilerplate de repositório sobre a **spec JPA (Jakarta Persistence)**, que é só um contrato (Galho 7); o **Hibernate** é quem de fato implementa esse contrato e fala JDBC com o banco. Esta nota é a **assinatura da tripla fronteira**: o `@Transactional` que abre a transação roda sobre o proxy AOP (Galho 8), e a borda HTTP devolve **DTO** (Galho 9) — nunca a entidade gerenciada. Aqui a gente operacionaliza e linka; a spec e o AOP são re-explicados nos seus galhos.

## O que é

"Camada de persistência" é o nome genérico para o pedaço do backend que transforma objetos Java em linhas de tabela e vice-versa. No ecossistema Spring isso aparece empilhado, cada andar resolvendo um problema diferente:

```text
┌─────────────────────────────────────────────┐
│  Seu código                                  │
│  (services, OrderRepository, entidade Order) │
└───────────────────┬─────────────────────────┘
                    │  você chama métodos de repositório
                    ▼
┌─────────────────────────────────────────────┐
│  Spring Data JPA                             │
│  gera a implementação do repositório         │
│  (JpaRepository, query methods derivados)    │
└───────────────────┬─────────────────────────┘
                    │  delega para a API padrão
                    ▼
┌─────────────────────────────────────────────┐
│  JPA / Jakarta Persistence (a ESPECIFICAÇÃO) │
│  EntityManager, @Entity, @Id — só o contrato │
└───────────────────┬─────────────────────────┘
                    │  é implementada por um provider
                    ▼
┌─────────────────────────────────────────────┐
│  Hibernate ORM (a IMPLEMENTAÇÃO)             │
│  gera SQL, gerencia o persistence context    │
└───────────────────┬─────────────────────────┘
                    │  fala JDBC
                    ▼
┌─────────────────────────────────────────────┐
│  JDBC  →  driver  →  banco relacional        │
└─────────────────────────────────────────────┘
```

O que cada andar resolve:

- **Spring Data JPA** — escreve a implementação do repositório por você. Você declara uma _interface_ e o Spring sintetiza o CRUD e as consultas a partir do nome dos métodos.
- **JPA (Jakarta Persistence)** — é só a **especificação**: define `@Entity`, `@Id`, `EntityManager`, a linguagem de consulta (JPQL). Não roda nada sozinha; é um contrato.
- **Hibernate ORM** — é o **provider** que implementa esse contrato: gera o SQL, gerencia o persistence context, traduz objeto ↔ tabela (o tal do _object-relational mapping_).
- **JDBC** — a camada de driver que o Hibernate usa para conversar com o banco de fato.

## Por que importa

É a camada de dados de **quase todo backend Spring**. Praticamente qualquer feature que persiste algo passa por aqui.

Em entrevista, dois pontos caem com frequência:

1. **"Spec vs. implementação"** — saber que JPA é o contrato e Hibernate é o provider. Quem troca os dois de lugar entrega que decorou nomes sem entender a separação.
2. **"O que o Spring Data esconde"** — explicar que o repositório que você nunca implementou é gerado em runtime sobre o `EntityManager` do JPA, que por sua vez é o Hibernate por baixo.

Entender a pilha também te dá o vocabulário para descer um andar quando precisar (escrever JPQL na mão, ou cair em SQL nativo) sem se perder.

## Como funciona

### JPA: a especificação (Galho 7) — o contrato `@Entity`/`@Id`

JPA (hoje **Jakarta Persistence**, pacote `jakarta.persistence.*` no Spring Boot 3) é uma **especificação**: um documento + um conjunto de interfaces e anotações. Ela define o vocabulário — `@Entity`, `@Id`, `@Column`, `EntityManager`, JPQL — mas **não executa nada**. É um contrato que diz "um provider que se diga compatível com JPA tem que oferecer isso aqui".

Os detalhes de `@Entity`, dos estados de entidade e da JPQL são do **Galho 7** — aqui só linkamos: [[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA (a spec)]].

### Hibernate: a implementação (o que você usa 99% do tempo quando diz "JPA")

O **Hibernate ORM** é o _provider_ que implementa a spec JPA — e historicamente foi a maior influência sobre a própria spec (a primeira versão de JPA foi inspirada no sucesso do Hibernate). Ele é quem realmente:

- gera o SQL a partir das suas entidades e queries,
- gerencia o **persistence context** (o cache de primeiro nível e o tracking de mudanças),
- traduz objeto ↔ linha de tabela — o _object-relational mapping_.

No Spring Boot, quando você adiciona o starter de JPA, o **Hibernate vem como provider padrão**. Por isso, na prática, dizer "estou usando JPA" quase sempre significa "estou usando Hibernate através da API JPA". A baseline desta trilha é **Hibernate ORM 6.x** (a família estável mais recente já é a 7.x, com Spring Boot 4.x — citado como mais recente, mas o baseline aqui é Boot 3.x / Hibernate 6.x).

### Spring Data JPA: a camada que elimina o boilerplate do repositório

Sem Spring Data, escrever um repositório significa injetar um `EntityManager` e implementar `findById`, `findAll`, `save`, `delete`... à mão, em toda entidade. O **Spring Data JPA** mata esse boilerplate: você declara uma **interface** que estende `JpaRepository`, e o Spring **sintetiza a implementação em runtime**.

Além do CRUD pronto, ele deriva consultas a partir do **nome do método** (_query methods_): `findByCustomerId(Long id)` vira uma query sem você escrever JPQL. Os detalhes de `JpaRepository` e dos query methods derivados ficam na nota [[03-Dominios/Tecnologia/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]].

### A tripla fronteira: a spec (Galho 7), o mecanismo do `@Transactional` (Galho 8), a borda/DTO (Galho 9)

Esta nota fica no cruzamento de três galhos anteriores — e o segredo é **não re-explicar nenhum**, só conectar:

- **Galho 7 — a spec.** `@Entity`, `@Id`, `EntityManager` e os estados da entidade são contrato JPA. Linkar: [[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA (a spec)]].
- **Galho 8 — o `@Transactional`.** A transação que envolve o `save` não é mágica do JPA: é um **proxy AOP** do Spring que abre a transação antes do método e faz commit/rollback depois. O mecanismo é o do Galho 8: [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies]].
- **Galho 9 — a borda/DTO.** A entidade `Order` é um objeto **gerenciado** pelo persistence context; ela não deve vazar para o JSON da resposta HTTP. A borda serializa um **DTO**, não a entidade — assunto do Galho 9: [[03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON (DTO na borda)]].

## Na prática

A entidade mínima e o repositório que você nunca implementa:

```java
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String customer;
    private int quantity;

    // construtores, getters e setters omitidos
}
```

```java
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

// Você declara a interface. O Spring Data gera a implementação em runtime.
public interface OrderRepository extends JpaRepository<Order, Long> {

    // CRUD (save, findById, findAll, deleteById...) já vem de graça.

    // Query method derivado: o Spring monta a consulta pelo nome do método.
    List<Order> findByCustomer(String customer);
}
```

A dependência que liga toda a pilha (Spring Data JPA + provider Hibernate + JDBC), no `pom.xml`:

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <!-- driver do banco; exemplo com H2 para desenvolvimento -->
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>runtime</scope>
    </dependency>
</dependencies>
```

O `spring-boot-starter-data-jpa` já traz, transitivamente, o **Spring Data JPA**, a **API Jakarta Persistence** e o **Hibernate** como provider — a pilha inteira do diagrama vem nesse único starter.

## Armadilhas

### (1) Dizer "JPA é o Hibernate"

Confundir o **contrato** com a **implementação**. JPA é a especificação (um conjunto de interfaces e anotações); Hibernate é um provider que a implementa — existem outros (ex.: EclipseLink).

Exemplo do erro:

```text
"Vou usar JPA, então o Hibernate é só um nome alternativo pra mesma coisa."
```

Não é: você poderia trocar o provider por EclipseLink mantendo o mesmo código JPA. **Fix:** trate JPA como _spec_ e Hibernate como a _implementação_ que o Boot pluga por padrão.

### (2) Achar que "Spring Data É a JPA"

Spring Data JPA **não** é a JPA — é uma **camada acima** dela. Ela gera repositórios sobre o `EntityManager` do JPA, mas você pode usar JPA puro (injetando o `EntityManager` direto) sem nenhum Spring Data.

Exemplo do erro:

```text
"Removi o Spring Data, então perdi o JPA e o Hibernate junto."
```

Falso: sem Spring Data você ainda tem JPA + Hibernate; só perde os repositórios derivados e volta a escrever DAO na mão. **Fix:** posicione mentalmente o Spring Data como o andar de _conveniência_ no topo da pilha, não como a fundação.

## Em entrevista

### Frase pronta (inglês)

> In a Spring backend, persistence is a layered stack, not a single thing. JPA — Jakarta Persistence — is only the **specification**: it defines `@Entity`, the `EntityManager` and JPQL, but it doesn't run anything by itself, so you always need a provider, and that provider is almost always **Hibernate**, which generates the SQL and manages the persistence context. **Spring Data JPA** sits one layer above the spec: it removes the repository boilerplate by synthesizing the implementation of a `JpaRepository` interface at runtime, including query methods derived from method names. The trade-off is that this convenience hides what's happening underneath — the transaction is actually an AOP proxy, and the managed entity should be mapped to a DTO at the edge rather than serialized directly — so the caveat is that you still need to understand the layers you're standing on to debug or tune them.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| camada de persistência | persistence layer |
| especificação | specification |
| implementação / provider | implementation / provider |
| repositório | repository |
| mapeamento objeto-relacional | object-relational mapping |
| boilerplate | boilerplate |
| contexto de persistência | persistence context |
| entidade gerenciada | managed entity |

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/03 - O persistence context e os estados da entidade|O persistence context e os estados da entidade]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA (a spec)]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON (DTO na borda)]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Spring Data JPA|Spring Data JPA (verbete)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Hibernate|Hibernate (verbete)]]

## Referências

- [Spring Data JPA — Reference Documentation](https://docs.spring.io/spring-data/jpa/reference/) — Spring Data JPA como suporte de repositório sobre a Jakarta Persistence API; eliminação do boilerplate de DAO.
- [Hibernate ORM](https://hibernate.org/orm/) — Hibernate como framework de object-relational mapping e implementação da especificação Jakarta Persistence; família de versão atual.
