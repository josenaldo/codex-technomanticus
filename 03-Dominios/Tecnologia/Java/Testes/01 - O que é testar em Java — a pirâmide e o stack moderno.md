---
title: "O que é testar em Java — a pirâmide e o stack moderno"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - testes
  - iniciado
  - junit
aliases:
  - "testes em Java"
  - "pirâmide de testes"
  - "stack de testes Java"
---

# O que é testar em Java — a pirâmide e o stack moderno

> [!abstract] TL;DR
> Testar em Java hoje é um **stack** (JUnit 5 / AssertJ / Mockito / Testcontainers / Spring Boot Test) montado sobre uma **pirâmide** — muitos testes de unidade na base, alguns de integração no meio, poucos end-to-end no topo. Este é o galho de **convergência**: ele não introduz uma camada nova da aplicação, ele *testa* o que os Galhos 1–12 construíram. Cada técnica de teste aponta de volta para o galho da coisa que está sendo testada — você testa concorrência porque aprendeu concorrência, testa endpoints reativos porque aprendeu WebFlux, e assim por diante.

## O que é

Testar em Java significa escrever código que executa o seu código de produção e **verifica automaticamente** que ele se comporta como o esperado — sem ninguém clicando numa tela ou lendo um log. A diferença entre o "testar Java" de 2010 e o de hoje não é o conceito, é o **ferramental** e a **disciplina**.

Por volta de 2010, o stack típico era JUnit 4 com asserções via `assertEquals` e matchers do Hamcrest (`assertThat(x, is(equalTo(y)))`), mocks com EasyMock ou Mockito ainda jovem, e — para qualquer coisa que tocasse banco — um H2 *in-memory* fingindo ser o Postgres de produção. Funcionava, mas tinha custos escondidos: o H2 mente sobre dialeto SQL, JUnit 4 era monolítico (um único runner por classe), e a sintaxe de asserção era verbosa e pouco legível.

O stack moderno (baseline **Spring Boot 3.x / Java 17+**) é outra história:

- **JUnit 5** (Jupiter) requer Java 17+ em runtime e é modular — Platform (lança os testes), Jupiter (modelo de escrita) e Vintage (roda testes JUnit 3/4 legados, e é em si um módulo de migração).
- **AssertJ** substitui Hamcrest com asserções fluentes e auto-descritivas (`assertThat(x).isEqualTo(y)`).
- **Mockito** para test doubles.
- **Testcontainers** sobe o **Postgres de verdade** num container Docker, aposentando o H2.
- **Spring Boot Test** amarra tudo em contexto de aplicação real.

## Por que importa

Para um desenvolvedor **senior**, dominar o stack de testes é tão importante quanto dominar a linguagem. Código sem testes é código que ninguém ousa mudar — e a habilidade que separa o senior do pleno é justamente a de **evoluir sistemas com segurança**. Testes são a rede que torna o *refactoring* possível.

Em **entrevista**, isso aparece sempre. Praticamente toda entrevista de backend Java passa pela pergunta *"qual é a sua estratégia de testes?"* ou *"como você garante que esse código está correto?"*. A resposta esperada de um senior não é "eu escrevo uns testes" — é uma narrativa coerente sobre a pirâmide, sobre o que cada camada testa, sobre quando usar mock e quando usar Testcontainers, e sobre o que *não* vale a pena testar. Quem só sabe escrever um `@Test` que chama um método não passa nesse filtro.

## Como funciona

### A pirâmide: muitos unit, alguns integration, poucos E2E (não inverter)

A **pirâmide de testes** é uma heurística de proporção. Da base ao topo:

- **Base — testes de unidade**: rápidos (milissegundos), isolados, sem rede nem disco. Testam uma classe/método com colaboradores mockados. Você quer *muitos* deles.
- **Meio — testes de integração**: testam várias peças juntas (ex.: serviço + repositório + banco real via Testcontainers, ou um endpoint via `@SpringBootTest`). Mais lentos. Você quer *alguns*.
- **Topo — testes end-to-end (E2E)**: sobem o sistema inteiro e exercitam fluxos completos. Lentos e frágeis. Você quer *poucos*.

A regra prática comum é manter a maior parte da suíte na base (frequentemente citada como algo na faixa de 70–80% de testes de unidade), mas isso é uma **heurística de design**, não uma medição — a proporção exata depende do sistema. O princípio inviolável é a **forma**: base larga, topo estreito.

> [!warning] Não inverte a pirâmide
> Quando a maioria dos testes é `@SpringBootTest` ou E2E, você tem o **cone de sorvete** (a pirâmide de cabeça pra baixo): suíte lenta, CI demorado, testes frágeis. É a armadilha nº 1 deste galho.

### O stack moderno: JUnit 5, AssertJ, Mockito, Testcontainers, Spring Boot Test

O ponto-chave para projetos Spring: o `spring-boot-starter-test` já **traz JUnit 5, AssertJ, Mockito, Hamcrest e JSONassert juntos** — você adiciona uma dependência só (escopo `test`) e ganha o núcleo do stack.

| Ferramenta | Propósito |
| --- | --- |
| **JUnit 5** (Jupiter) | Runner e modelo de escrita: `@Test`, `@BeforeEach`, lifecycle, parametrização |
| **AssertJ** | Asserções fluentes e legíveis: `assertThat(x).isEqualTo(y)` |
| **Mockito** | Test doubles (mocks/stubs/spies) para isolar a unidade sob teste |
| **Testcontainers** | Sobe dependências reais (Postgres, Kafka, Redis) em containers Docker no teste |
| **Spring Boot Test** | Integração com o contexto Spring: `@SpringBootTest`, slices (`@WebMvcTest`, `@DataJpaTest`), `MockMvc` |

### Ferramentas deprecated que você ainda encontra (JUnit 4, Hamcrest, H2, PowerMock)

Você vai topar com essas em código legado — saiba reconhecê-las e por que migrar:

- **JUnit 4** — anterior à arquitetura modular do JUnit 5. Roda hoje via o engine **Vintage** (que a própria documentação trata como apoio temporário de migração). Sinais: `import org.junit.Test` (sem `jupiter`), `@RunWith`, `@Before`.
- **Hamcrest** — matchers no estilo `assertThat(x, is(equalTo(y)))`. Ainda vem no starter por compatibilidade, mas AssertJ é o caminho moderno: mais legível e com melhor autocomplete.
- **H2 in-memory** — banco fingindo ser o de produção. Mente sobre dialeto SQL e comportamento transacional. Testcontainers sobe o banco *de verdade* e elimina a classe inteira de bugs "passou no H2, quebrou em prod".
- **PowerMock** — mockava `static`, `final` e construtores via manipulação de bytecode. Hoje o próprio Mockito faz isso (`mockStatic`), e a necessidade de PowerMock costuma sinalizar um design difícil de testar.

### A convergência: Testes testa os Galhos 1-12 (cada slice/técnica linka o galho da camada testada)

Este galho é **transversal**. Ele não vive sozinho — cada técnica de teste existe para verificar algo que outro galho construiu:

- Testar **lógica de domínio** pura → verifica o que você modelou com a linguagem (Galhos iniciais).
- Testar **concorrência** (condições de corrida, `CompletableFuture`, virtual threads) → linka o galho de concorrência.
- Testar **camada web / endpoints** → linka Spring MVC; usa `@WebMvcTest` + `MockMvc`.
- Testar **persistência** → linka JPA/Hibernate; usa `@DataJpaTest` + Testcontainers.
- Testar **código reativo** (`Mono`/`Flux`) → linka o [[03-Dominios/Tecnologia/Java/index|Galho 11 (Programação Reativa)]]; usa `StepVerifier`.

A leitura mental certa: *"para cada coisa que aprendi a construir, há uma técnica de teste correspondente"*. Por isso este galho vem perto do fim da trilha — ele colhe a safra dos anteriores.

## Na prática

Um teste mínimo de unidade com JUnit 5 + AssertJ, seguindo o padrão **AAA** (Arrange-Act-Assert, ou *given/when/then*). O `OrderService` aqui é neutro — calcula o total de um pedido:

```java
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

class OrderServiceTest {

    private final OrderService service = new OrderService();

    @Test
    void shouldCalculateTotalForMultipleItems() {
        // given (Arrange) — montamos a entrada
        Order order = new Order();
        order.addItem(new Item("Keyboard", 100), 2);
        order.addItem(new Item("Mouse", 50), 1);

        // when (Act) — exercitamos exatamente uma ação
        int total = service.calculateTotal(order);

        // then (Assert) — verificamos o resultado com AssertJ
        assertThat(total).isEqualTo(250);
    }
}
```

Repare em três coisas: o nome do método **descreve o comportamento** (`shouldCalculate...`), os três blocos AAA são visíveis, e a asserção `assertThat(...).isEqualTo(...)` se lê quase como uma frase em inglês. Nenhum mock aqui — `OrderService` é pura lógica de domínio, então é um teste de unidade puro, da base da pirâmide.

## Armadilhas

### (1) Inverter a pirâmide

Encher a suíte de `@SpringBootTest` (que sobe o contexto Spring inteiro) porque "assim testa de verdade" parece robusto, mas destrói a velocidade da suíte.

**Exemplo:** um time põe `@SpringBootTest` em 200 classes de teste. Cada uma sobe o contexto da aplicação; a suíte leva 12 minutos. O CI fica lento, os desenvolvedores param de rodar os testes localmente e começam a **desligar testes** ("comento esse pra mergear logo") — a rede de segurança apodrece.

**Fix:** mantenha a base larga. A maior parte da lógica testa como **unidade pura** (sem Spring). Use *slices* (`@WebMvcTest`, `@DataJpaTest`) para subir só a fatia necessária, e reserve `@SpringBootTest` completo para os poucos testes de fluxo que realmente precisam do contexto inteiro.

### (2) "Coverage alto = qualidade"

Cobertura de linha (*line coverage*) mede quais linhas *executaram* durante os testes — não se o resultado foi **verificado**.

**Exemplo:** um teste chama `service.process(order)` dentro de um `try`, não lança exceção, e termina sem nenhum `assertThat`. A ferramenta de cobertura marca 100% das linhas de `process` como cobertas. O método poderia retornar lixo que o teste passaria igual — ele só confirma que o código *não explodiu*, não que está *correto*.

**Fix:** trate cobertura como detector de *zonas não testadas*, nunca como prova de qualidade. Toda asserção precisa verificar comportamento. Para medir a *força real* da suíte, o próximo passo é o **mutation testing** (ex.: PIT), que injeta defeitos no código e checa se algum teste falha — se nenhum falhar, o teste é teatro. (Mutation testing é tema de uma nota da fase adepto deste galho.)

## Em entrevista

### Frase pronta (inglês)

> "My testing strategy follows the test pyramid: a wide base of fast unit tests, a smaller layer of integration tests, and very few end-to-end tests. On the JVM I rely on JUnit 5 with AssertJ for readable assertions and Mockito to isolate units, and I bring in Testcontainers for integration tests so I'm verifying against a real database instead of an in-memory fake. I treat code coverage as a signal for untested areas, not as a quality metric — what matters is that every test actually asserts on behavior."

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| pirâmide de testes | test pyramid |
| teste de unidade | unit test |
| teste de integração | integration test |
| asserção | assertion |
| cobertura de código | code coverage |
| dublê de teste / mock | test double / mock |
| teste fim a fim | end-to-end test |
| suíte de testes | test suite |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/02 - JUnit 5 — anatomia, lifecycle e o padrão AAA|JUnit 5]]
- [[03-Dominios/Tecnologia/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade|Capstone de testes]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- JUnit 5 User Guide — https://docs.junit.org/current/user-guide/
- Spring Boot Reference — Testing — https://docs.spring.io/spring-boot/reference/testing/index.html
