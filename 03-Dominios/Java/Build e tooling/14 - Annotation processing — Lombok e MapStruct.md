---
title: "Annotation processing — Lombok e MapStruct"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - build
  - adepto
  - lombok
  - mapstruct
aliases:
  - "annotation processing"
  - "Lombok"
  - "MapStruct"
---

# Annotation processing — Lombok e MapStruct

> [!abstract] TL;DR
> **Annotation processing** (APT) é um mecanismo do compilador Java (`javax.annotation.processing`) que lê anotações no código-fonte e **gera código novo em tempo de compilação** — sem reflection, sem custo de runtime. **Lombok** usa esse gancho para eliminar boilerplate (`@Getter`, `@Data`, `@Builder`), mas manipula a AST do compilador (não é APT "de livro"). **MapStruct** gera mappers `Entity ↔ DTO` em compile-time. Quando os dois rodam juntos, é **obrigatório** o `lombok-mapstruct-binding` no `annotationProcessorPaths` — senão o MapStruct roda antes do Lombok gerar os getters e o mapper sai vazio/com `null`.

## O que é

Quando você escreve `@Override`, `@Deprecated` ou `@Entity`, o compilador `javac` não trata a anotação como um comentário decorativo: ela é um dado estruturado que pode ser **lido e processado durante a compilação**. O **annotation processing** (também chamado de **APT**, _Annotation Processing Tool_) é a API que expõe esse momento. Um _annotation processor_ é uma classe que implementa `javax.annotation.processing.Processor` (normalmente estendendo `AbstractProcessor`), declara quais anotações observa e é chamada pelo `javac` em **rodadas** (_rounds_) para inspecionar o código e, opcionalmente, **gerar novos arquivos**.

A ideia-chave: o trabalho acontece **em compile-time, não em runtime**. Em vez de descobrir a estrutura de uma classe via _reflection_ a cada execução (custo de CPU, surpresas em `GraalVM native-image`), o código já nasce escrito e compilado. Frameworks inteiros se apoiam nisso — Dagger, Micronaut, Hibernate Metamodel — e, no nosso recorte, **Lombok** e **MapStruct**.

## Por que importa

Em entrevista sênior, a pergunta raramente é "o que faz `@Data`?". É "o que acontece quando MapStruct e Lombok não conversam?" ou "por que `@Data` em uma entidade JPA é uma armadilha?". Dominar APT separa quem **cola anotação** de quem **entende a pipeline de compilação**:

- **Performance e nativo**: gerar código em compile-time evita reflection em runtime — essencial para tempo de _startup_ e para `native-image`.
- **Diagnóstico de bugs sutis**: mapper que retorna `null` em todos os campos, parâmetros que "perdem o nome" em runtime, `LazyInitializationException` que aparece só em produção — todos têm raiz na pipeline de processors.
- **Ordem importa**: processors rodam em sequência e em rodadas; entender isso explica por que o `lombok-mapstruct-binding` existe.

## Como funciona

### APT — o gancho do compilador

O `javac` executa os processors em **rodadas**. Em cada rodada, ele entrega ao processor o conjunto de elementos anotados (`RoundEnvironment`), o processor pode gerar novos arquivos via `Filer`, e esses arquivos geram **uma nova rodada** (porque podem conter mais anotações). O ciclo termina quando nenhuma rodada nova produz código.

Um processor "ortodoxo" **só adiciona** arquivos novos — ele não reescreve o código que você digitou. Os processors são descobertos via `ServiceLoader` (arquivo `META-INF/services/javax.annotation.processing.Processor`) e, em build moderno, são declarados explicitamente no `annotationProcessorPaths` do `maven-compiler-plugin`.

### Lombok — boilerplate via AST

**Lombok** é o ponto fora da curva. Ele se registra como annotation processor, mas **não gera arquivos novos**: ele **modifica a AST** (árvore sintática) que o compilador está montando, injetando métodos diretamente na classe que você escreveu. Por isso `@Data` em `Order` faz aparecer `getId()`, `setId()`, `equals()`, `hashCode()` e `toString()` no `.class` final — sem nenhum arquivo `OrderGenerated.java`.

Esse truque de mexer na AST é o que dá o atrito de Lombok com algumas ferramentas (analisadores que leem só o fonte não veem os getters) e o que torna a **ordem em relação a outros processors** relevante.

Anotações comuns: `@Getter`/`@Setter`, `@Data` (junta getters/setters/`equals`/`hashCode`/`toString`/construtor de campos obrigatórios), `@Builder`, `@Value`, `@AllArgsConstructor`/`@NoArgsConstructor`, `@Slf4j`. O comportamento global do projeto se configura num arquivo **`lombok.config`** na raiz (ou por diretório).

Versões cravadas: **Lombok 1.18.46** (lançado em 22/abr/2026). Suporte a **JDK 21** desde 1.18.30, **JDK 25** desde 1.18.40 e **JDK 26** desde a própria 1.18.46.

### MapStruct — e o atrito do binding

**MapStruct** é APT ortodoxo: lê uma interface `@Mapper` e **gera a classe de implementação** (`OrderMapperImpl`) que copia campo a campo entre `Order` e `OrderDTO`. Como o código é gerado em compile-time, o mapeamento é **só atribuições diretas** — rápido, sem reflection. Com `@Mapper(componentModel = "spring")`, a implementação vira um `@Component`, injetável como qualquer bean. Versão estável: **MapStruct 1.6.3 GA** (09/nov/2024); existe a **1.7.0.Beta1** (01/fev/2026).

O atrito surge porque MapStruct precisa **enxergar os getters/setters** das classes-fonte para gerar o mapeamento — e, em uma classe Lombok, esses métodos **só existem depois que o Lombok mexeu na AST**. Se o MapStruct rodar antes, ele vê uma classe sem accessors e gera um mapper que não copia nada (campos vêm `null`).

A ponte é o **`lombok-mapstruct-binding`** — uma dependência introduzida no Lombok **1.18.16** (out/2020), declarada no `annotationProcessorPaths`. Ela coordena os dois processors para que o Lombok gere os accessors **antes** do MapStruct ler a classe. Sem ela, o resultado é o clássico "mapper vazio". A **ordem** em que os processors aparecem em `annotationProcessorPaths` também importa.

## Na prática

Configuração do `maven-compiler-plugin` com os três artefatos no `annotationProcessorPaths` — Lombok, MapStruct e o binding — mais a flag `-parameters`:

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <compilerArgs>
      <arg>-parameters</arg>
    </compilerArgs>
    <annotationProcessorPaths>
      <!-- A ordem importa: Lombok antes do MapStruct -->
      <path>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>1.18.46</version>
      </path>
      <path>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok-mapstruct-binding</artifactId>
        <version>0.2.0</version>
      </path>
      <path>
        <groupId>org.mapstruct</groupId>
        <artifactId>mapstruct-processor</artifactId>
        <version>1.6.3.Final</version>
      </path>
    </annotationProcessorPaths>
  </configuration>
</plugin>
```

Uma classe de domínio com Lombok e um mapper MapStruct (domínios neutros):

```java
package com.example.order;

import lombok.Data;
import lombok.Builder;

@Data
@Builder
public class Order {
    private Long id;
    private String customerName;
    private long totalCents;
}
```

```java
package com.example.order;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface OrderMapper {

    @Mapping(source = "totalCents", target = "amountInCents")
    OrderDTO toDto(Order order);

    Order toEntity(OrderDTO dto);
}
```

O `lombok.config` na raiz do projeto, que padroniza o comportamento do Lombok:

```properties
# Para a config parar de subir na árvore de diretórios neste ponto
config.stopBubbling = true

# Marca os métodos gerados como @lombok.Generated (cobertura, SpotBugs ignoram)
lombok.addLombokGeneratedAnnotation = true

# Proíbe @Data em favor de anotações mais explícitas (opcional, mas recomendado)
# lombok.data.flagUsage = WARNING
```

## Armadilhas

### (1) Lombok + MapStruct sem o binding → mapper vazio / nulls

Sem o `lombok-mapstruct-binding` no `annotationProcessorPaths`, o MapStruct pode rodar **antes** de o Lombok gerar os getters/setters. O resultado: o `OrderMapperImpl` é gerado, compila sem erro, mas **todos os campos saem `null`** (ou o `OrderDTO` vem zerado). É um bug silencioso — não há _stack trace_, só dado faltando. Solução: adicionar o binding **e** garantir a ordem (Lombok antes do `mapstruct-processor`).

### (2) `-parameters` faltando — nomes de parâmetro perdidos

Por padrão, o `javac` **não preserva os nomes dos parâmetros** no bytecode (eles viram `arg0`, `arg1`). MapStruct e vários frameworks (Spring, Jackson com `@JsonCreator`) usam o nome do parâmetro para casar campos. Sem `-parameters` no `compilerArgs`, o mapeamento por nome quebra e você é forçado a anotar tudo com `@Mapping`/`@Param` explícito. A flag deve estar no `maven-compiler-plugin` (ou `Gradle` equivalente).

### (3) Lombok `@Data` em entidade JPA → `equals`/`hashCode`/`toString` tocam lazy

`@Data` (e `@EqualsAndHashCode`/`@ToString`) gera `equals`/`hashCode`/`toString` usando **todos os campos**, incluindo relações `@OneToMany`/`@ManyToOne` mapeadas como _lazy_. Ao chamar `equals()` ou logar a entidade fora de uma sessão aberta, o proxy lazy é tocado → `LazyInitializationException`; dentro da sessão, dispara queries em cascata (problema de performance). Em entidade JPA, prefira `@Getter`/`@Setter` pontuais e `equals`/`hashCode` baseados só no identificador. O detalhe profundo de JPA mora em outro galho — veja [[03-Dominios/Java/Backend/Spring Boot|Spring Boot (Galho 8 — Lombok no contexto de JPA)]].

## Em entrevista

### Frase pronta (inglês)

> Annotation processing lets the compiler read annotations and generate code at compile time, so there is no runtime reflection cost. Lombok removes boilerplate by editing the compiler's AST, while MapStruct generates `Entity`-to-`DTO` mappers as plain assignments. When you run both together, you must add `lombok-mapstruct-binding` to the annotation processor path; otherwise MapStruct runs before Lombok generates the getters and produces an empty mapper full of nulls. I also enable the `-parameters` flag so parameter names survive into the bytecode for name-based mapping.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| Processamento de anotações | Annotation processing (APT) |
| Tempo de compilação | Compile-time |
| Código boilerplate | Boilerplate code |
| Árvore sintática (AST) | Abstract Syntax Tree (AST) |
| Geração de código | Code generation |
| Mapeador (Entidade ↔ DTO) | Mapper (Entity ↔ DTO) |
| Carregamento tardio | Lazy loading |
| Ordem dos processors | Processor ordering |

## Veja também

- [[03-Dominios/Java/Build e tooling/02 - Maven — POM, coordenadas e lifecycle|Maven — o modelo]]
- [[03-Dominios/Java/Build e tooling/05 - Gradle — build script, tasks e configurations|Gradle — o modelo]]
- [[03-Dominios/Java/Backend/Spring Boot|Spring Boot (Galho 8 — Lombok no contexto de JPA)]]
- [[03-Dominios/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Project Lombok — site oficial e changelog: https://projectlombok.org/ (v1.18.46, 22/abr/2026; suporte JDK 21/25/26; `lombok-mapstruct-binding` desde 1.18.16)
- MapStruct — site oficial e documentação de referência: https://mapstruct.org/ (1.6.3 GA, 09/nov/2024; 1.7.0.Beta1, 01/fev/2026)
- `javax.annotation.processing` — Java SE API (Annotation Processing)
