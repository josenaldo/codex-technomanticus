---
title: "Testes"
created: 2026-04-01
updated: 2026-04-09
type: concept
status: evergreen
tags:
  - fundamentos
  - entrevista
publish: false
---

# Testes

Práticas e ferramentas para verificar que o software funciona como esperado — e **continua** funcionando após mudanças. Para um senior, escrever testes é fácil; **desenhar uma estratégia de testes** que equilibra confiança, velocidade e custo de manutenção é o que diferencia.

## O que é

Um teste automatizado é um programa que executa outro programa e verifica que o resultado corresponde ao esperado. A função estratégica dos testes não é só "pegar bugs" — é:

1. **Dar velocidade** — permite refatorar sem medo
2. **Documentar comportamento esperado** — testes são spec executável
3. **Dar confiança em deploys** — você só faz deploy contínuo se confia na suíte
4. **Forçar bom design** — código difícil de testar é código mal desenhado

Em entrevistas de senior, espera-se que você argumente sobre **quais tipos de teste usar**, **quando**, e **por quê** — não apenas liste frameworks.

---

## Pirâmide, troféu e outras formas

### Pirâmide de testes (Mike Cohn)

```text
        /  E2E  \         ← poucos, lentos, frágeis
       /---------\
      / Integração \      ← moderados, testam contratos
     /--------------\
    /   Unitários    \   ← muitos, rápidos, isolados
```

A intuição: muitos testes rápidos na base; poucos testes caros no topo.

### Testing Trophy (Kent C. Dodds)

```text
           /  E2E  \
          /---------\
         / Integração \    ← o "corpo" do troféu
        /--------------\
       /   Unitários    \
      /------------------\
     /  Análise estática  \  ← linting, types
```

Valoriza mais integração e análise estática (tipagem, lint). Faz mais sentido em frontend moderno com React + TypeScript, onde o compilador pega muita coisa antes de qualquer teste rodar.

### Quando cada forma importa

- **Backend Java/Spring puro:** pirâmide clássica funciona bem
- **Frontend React + TS + Testing Library:** troféu é mais adequado — integração (renderizar componente + interagir) é o melhor ROI
- **Lógica algorítmica pesada:** quase tudo unitário
- **Microserviços com contratos:** adicione contract tests entre serviços

> **Regra prática:** a proporção não é dogma. A pergunta certa é "**qual teste eu quero que falhe quando este bug aparecer?**". Se a resposta é "um teste rápido que só olha esta função" → unit. Se é "um teste que valida que o endpoint funciona ponta-a-ponta com o banco real" → integração.

---

## Tipos de teste

### Unitários

Testam uma **unidade** (classe, função, módulo) em **isolamento**, com dependências mockadas.

**Propriedades desejáveis:**

- **Rápidos** (milissegundos)
- **Determinísticos** — mesmo input, mesmo output, sempre
- **Independentes** — rodam em qualquer ordem, sem estado compartilhado
- **Legíveis** — nome e corpo contam a história

**Bom para:** lógica de negócio pura, algoritmos, validações, transformações de dados, regras de domínio.

**Ruim para:** queries SQL, integração com APIs externas, fluxos que envolvem muitos objetos reais.

### Integração

Testam a **colaboração entre componentes reais** — tipicamente o sistema + banco real, + fila real, + cache real (via Testcontainers).

**Bom para:**

- Validar que repositórios JPA produzem SQL correto
- Endpoints HTTP com o stack completo (controller → service → repository → banco)
- Fluxos assíncronos com Kafka/RabbitMQ
- Interação com Redis, S3, etc.

**Em Spring:** `@SpringBootTest` + `@Testcontainers`. Mais lentos (segundos), mas muito mais confiança.

### E2E (End-to-End)

Testam o **fluxo completo do usuário**, normalmente via browser (Playwright, Cypress) ou HTTP ponta-a-ponta. Valida que backend, frontend, banco, filas, integrações externas todas colaboram.

**Bom para:** fluxos críticos de negócio (login, checkout, onboarding).

**Ruim para:** tudo o mais. E2E é caro, lento, frágil. Mantenha uma dúzia que cobre o caminho crítico.

### Contract Tests

Quando serviço A depende de serviço B, um **contract test** garante que ambos concordam sobre a forma da mensagem — sem precisar subir ambos. **Ferramentas:** Pact, Spring Cloud Contract.

**Bom para:** microserviços com APIs internas, evolução coordenada de cliente e servidor.

### Smoke Tests

Um mínimo de testes que roda após deploy pra garantir que "o sistema sobe e responde". Em 30 segundos. Não é profundidade, é sinal de vida.

### Property-based tests

Em vez de escrever casos específicos, você declara uma **propriedade** que deve valer para **qualquer** input, e o framework gera centenas de inputs aleatórios tentando quebrar. Ferramentas: JQwik (Java), fast-check (JS/TS), Hypothesis (Python).

```java
@Property
void soma_é_comutativa(@ForAll int a, @ForAll int b) {
    assertThat(a + b).isEqualTo(b + a);
}
```

Ótimo para: lógica matemática, parsers, serializadores, invariantes de domínio.

### Mutation tests

A suíte de testes **é suficiente**? O teste de mutação altera seu código (muda `>` para `>=`, remove `return`, etc.) e verifica se algum teste falha. Se nenhum falhar, seus testes não estão detectando regressões nessa linha. Ferramenta: **PITest** em Java.

### Snapshot tests

Grava o output esperado na primeira execução; compara com rodadas futuras. Útil para: componentes React, estruturas grandes, respostas de API. **Cuidado:** snapshots sem revisão humana viram "aceite tudo". Use com critério.

### Performance tests / Load tests

- **Microbenchmarks:** JMH em Java — medidas precisas de funções
- **Load tests:** k6, Gatling, JMeter — simulam usuários concorrentes
- **Stress tests:** empurram até quebrar, para descobrir limites

### Chaos tests

Injetam falhas propositalmente (matar instâncias, latência, perda de pacotes) para validar resiliência. Netflix Chaos Monkey. Para equipes maduras com infra distribuída.

### Security tests

SAST (Static), DAST (Dynamic), dependency scanning (Dependabot, Snyk, OWASP Dependency Check). Cada vez mais parte de CI.

---

## Padrão AAA (Arrange-Act-Assert)

Estrutura padrão de um teste legível:

```java
@Test
void deve_aprovar_pedido_dentro_do_limite() {
    // Arrange
    var cliente = ClienteFactory.preferencial();
    var pedido = new Pedido(cliente, Money.of(500));

    // Act
    pedido.aprovar();

    // Assert
    assertThat(pedido.status()).isEqualTo(Status.APROVADO);
    assertThat(pedido.aprovadoEm()).isNotNull();
}
```

Equivalente em BDD: **Given-When-Then**. A estrutura é a mesma; o vocabulário muda para ficar mais próximo do stakeholder.

### Nome do teste

Deve contar o que e quando, sem precisar ler o corpo. Convenções comuns:

- `deve_X_quando_Y()` — `deve_lançar_excecao_quando_saldo_insuficiente`
- `methodUnderTest_scenario_expectedBehavior()` — `approve_overLimit_throws`
- `should X when Y` em BDD

---

## Test Doubles

Termo genérico para "qualquer coisa que substitui uma dependência real em testes" (Gerard Meszaros).

| Tipo | O que faz | Quando usar |
| --- | --- | --- |
| **Dummy** | Objeto passado mas nunca usado | Preencher parâmetros obrigatórios |
| **Stub** | Retorna valores pré-definidos | Controlar respostas de dependências |
| **Spy** | Wrapper real que registra chamadas | Verificar interações sem substituir |
| **Mock** | Verifica chamadas e comportamento esperado | Testar contrato com colaboradores |
| **Fake** | Implementação funcional simplificada | In-memory DB, fake HTTP server |

### Mock vs Stub — a distinção que confunde

- **Stub:** teste verifica **estado** após a ação. "O objeto X ficou como esperado?" O stub só **alimenta** o teste com dados.
- **Mock:** teste verifica **interação**. "A classe chamou `emailService.send()` corretamente?" O mock **verifica chamadas**.

> **Regra prática:** prefira **state-based testing** (verifique estado final) a **interaction-based testing** (verifique chamadas). Testes baseados em interação acoplam-se à implementação e quebram em refactors.

### Fakes são subestimados

Um `FakeUserRepository` com um `HashMap<Long, User>` interno dá quase todo o benefício de um mock **sem** o acoplamento a chamadas específicas. Em muitos casos, um fake é mais robusto e mais legível que um mock.

### Mockito na prática (Java)

```java
@ExtendWith(MockitoExtension.class)
class PedidoServiceTest {

    @Mock PedidoRepository repo;
    @Mock NotificationService notifier;
    @InjectMocks PedidoService service;

    @Test
    void deve_enviar_notificacao_ao_criar_pedido() {
        var pedido = new Pedido(/* ... */);
        when(repo.save(any())).thenReturn(pedido);

        service.criar(pedido);

        verify(notifier).notificarCriacao(pedido);
    }
}
```

**Anti-patterns com Mockito:**

- **Mockar tudo** incluindo POJOs simples (Value Objects). Use o real.
- **`when(a).thenReturn(b).thenReturn(c)...`** em cadeias longas — sinal de over-mocking.
- **Mockar a classe que você está testando** (`@Spy` no próprio SUT) — praticamente sempre errado.
- **`verifyNoMoreInteractions()`** tornar testes rígidos demais.

---

## TDD (Test-Driven Development)

### O ciclo Red-Green-Refactor

1. **Red:** escreva um teste que descreve o comportamento desejado. Rode — ele falha (a feature não existe).
2. **Green:** escreva **o mínimo** código que faz o teste passar. Não otimize ainda.
3. **Refactor:** melhore o código (extrair métodos, renomear, remover duplicação) mantendo **todos os testes verdes**.

Repita em ciclos de minutos.

### O que TDD te força a fazer

- **Pensar no design antes da implementação** — o teste vira o primeiro "cliente" do seu código, revelando se a API é boa
- **Escrever código testável** — desacoplado, com dependências injetadas
- **Resolver o problema certo** — se você não consegue escrever o teste, não entendeu o requisito
- **Ter feedback rápido** — não escreve 300 linhas sem saber se funciona

### Quando TDD brilha

- **Lógica de negócio não-trivial** — regras de cálculo, validações complexas
- **Bug fixing** — primeiro escreva o teste que reproduz o bug, depois corrija
- **API pública** — desenhar contrato antes da implementação
- **Refactoring** — testes são a rede de segurança

### Quando TDD atrapalha

- **Exploração / prototipagem** — quando você não sabe ainda o que quer construir
- **Código puramente declarativo** (configurações, mapeamentos simples)
- **UIs visuais** — TDD não valida se "ficou bonito"
- **Glue code trivial** — testar um controller que só delega para o service é overhead

**Posição pragmática:** TDD quando o design ainda não está claro ou a lógica é complexa; "test-after" focado em edge cases quando o caminho é óbvio.

---

## Como escrever bons testes

### F.I.R.S.T

- **F**ast — milissegundos
- **I**ndependent — rodam em qualquer ordem, sem estado compartilhado
- **R**epeatable — mesmo resultado em qualquer ambiente
- **S**elf-validating — passa ou falha, sem inspeção manual
- **T**imely — escritos no momento certo (preferencialmente antes do código, via TDD)

### Um teste = uma razão para falhar

Se um teste falha, você deveria saber imediatamente **o que quebrou**. Se um teste tem 20 assertions verificando 5 comportamentos diferentes, ele falha e você não sabe qual regra quebrou.

**Prefira múltiplos testes focados a um teste gigante.**

### Teste comportamento, não implementação

```java
// Ruim: acoplado à implementação interna
verify(repository).findById(1L);
verify(repository).save(any());
verify(cache).put("user:1", any());

// Bom: verifica o resultado observável
User updated = service.updateName(1L, "Novo Nome");
assertThat(updated.getName()).isEqualTo("Novo Nome");
```

**Regra:** se você refatorar o código mantendo o comportamento igual e o teste quebrar, o teste está errado.

### Nomes descritivos

O nome do teste é documentação executável. "test1" e "testCreate" são inúteis. Use frases que explicam o cenário e a expectativa.

### Fixtures e Factories

**Não repita setup** em todos os testes. Extraia para:

- **Fixtures** — estado inicial compartilhado
- **Factories / Builders** — construtores de objetos de teste com defaults sensatos
- **Object Mothers** — factories nomeadas por persona (`ClienteFactory.preferencial()`, `ClienteFactory.inadimplente()`)

```java
public class PedidoFactory {
    public static Pedido pedidoAprovado() {
        return new Pedido(/* defaults razoáveis */, Status.APROVADO);
    }

    public static Pedido pedidoComValorAcimaDoLimite() {
        return new Pedido(/* ... */, Money.of(100_000));
    }
}
```

### Evite lógica condicional em testes

Testes com `if`, `for`, `try/catch` são difíceis de ler e podem esconder bugs. Se você precisa, algo no design está errado ou o teste é grande demais.

### Testes como documentação

Um test class bem nomeado com testes claros é melhor documentação que qualquer README desatualizado. Priorize legibilidade.

---

## Testes flaky e como evitar

Teste **flaky** é aquele que às vezes passa, às vezes falha, sem mudança no código. É a pior praga de uma suíte de testes — destrói a confiança.

### Causas comuns

- **Dependência de ordem** — teste A deixa estado que teste B espera
- **Timing / race conditions** — `Thread.sleep(100)` em vez de `Awaitility`
- **Estado compartilhado** — variáveis estáticas, banco não limpo entre testes
- **Datas e timezones** — `LocalDate.now()` muda dependendo de quando roda
- **Ordem de iteração** — `HashMap` não garante ordem; se o teste assume, quebra
- **Rede externa** — qualquer chamada a serviço externo é flaky por natureza
- **Paralelismo** — testes que não toleram execução paralela
- **Dependências de sistema** — arquivos, portas, locales

### Mitigações

- **Isole** — cada teste limpa o estado que cria
- **Controle o tempo** — injete `Clock` em vez de chamar `LocalDateTime.now()` direto
- **Mocks para rede externa** — WireMock, MockWebServer
- **Testcontainers** para banco — cada teste tem DB limpo
- **Awaitility** para esperar condições assíncronas, não `sleep`
- **Marque e corrija** — teste flaky vai para quarentena imediata; arrumar vem depois

---

## Coverage (cobertura)

Porcentagem do código exercitado pelos testes. Ferramentas: **JaCoCo** (Java), **Istanbul/nyc** (JS/TS).

### Tipos

- **Line coverage** — quantas linhas foram executadas
- **Branch coverage** — quantos caminhos de if/switch foram exercitados
- **Method coverage** — quantos métodos foram chamados

### Armadilhas

- **100% coverage ≠ código testado.** Um teste pode executar a linha sem verificar nada — `@Test void test() { service.doStuff(); }` tem 100% line coverage e zero assertions.
- **Coverage como métrica única** incentiva testes inúteis — pessoas escrevem testes sem asserções só pra bater a meta.
- **Meta 100% é desperdício** — algumas linhas (getters/setters, código gerado, DTOs) não compensa testar.

### Uso sensato

- **70-85%** costuma ser um bom ponto de equilíbrio
- **Foque em branch coverage** mais que line — garante que os caminhos são exercitados
- **Cubra o que importa**: lógica de negócio, edge cases, regras complexas. Não persiga coverage em código trivial
- **Combine com mutation testing** (PITest) para saber se os testes realmente verificam algo

---

## Edge cases que todo senior precisa lembrar

- **Input vazio** — string vazia, lista vazia, mapa vazio
- **Null** — em qualquer parâmetro que aceite, explícito ou implícito
- **Valores no limite** — 0, -1, `Integer.MAX_VALUE`, `Long.MIN_VALUE`
- **Overflow** — soma que transborda o tipo
- **Concorrência** — múltiplas threads chamando simultaneamente
- **Unicode** — emojis, combinação de caracteres, right-to-left
- **Timezones** — horário de verão, fuso oposto
- **Datas** — 29 de fevereiro, fim do mês, ano bissexto
- **Duplicatas** — lista com elementos iguais, chaves duplicadas
- **Ordem inversa** — dados em ordem reversa ou aleatória
- **Tamanhos extremos** — 1 elemento, milhões de elementos
- **Caracteres especiais** — aspas, barras, SQL injection
- **Erros de rede** — timeout, 500, conexão fechada
- **Recursos esgotados** — pool cheio, disco cheio, memória
- **Concorrência + falha parcial** — rollback, compensação

---

## Ferramentas por stack

### Java / Spring Boot

- **JUnit 5** — framework base
- **AssertJ** — assertions fluentes (`assertThat(x).isEqualTo(y)`)
- **Mockito** — mocking
- **Testcontainers** — PostgreSQL, Redis, Kafka, qualquer Docker image em testes de integração
- **Spring Boot Test** — `@SpringBootTest`, `@WebMvcTest`, `@DataJpaTest`
- **MockMvc** — testes de controllers
- **WireMock** — mock de HTTP externo
- **Awaitility** — esperar condições assíncronas sem `Thread.sleep`
- **JQwik** — property-based testing
- **PITest** — mutation testing
- **JMH** — microbenchmarks
- **REST-assured** — testes de API REST expressivos

### JavaScript / TypeScript

- **Vitest** — rápido, compatível com Vite, ESM nativo (recomendado para projetos novos)
- **Jest** — tradicional, amplo ecossistema
- **Testing Library** — testes de React focados em comportamento do usuário ("find by label", "click by text")
- **MSW (Mock Service Worker)** — intercepta requisições HTTP em testes
- **Playwright** — E2E moderno, rápido, multi-browser
- **Cypress** — E2E clássico, ótima DX
- **fast-check** — property-based testing
- **Storybook + Chromatic** — visual regression testing de componentes

### Outros

- **k6 / Gatling / JMeter** — load testing
- **Pact / Spring Cloud Contract** — contract testing
- **Snyk / Dependabot / OWASP** — security scanning

---

## Testes em CI/CD

Testes só entregam valor se rodam em todo commit. Integração típica:

1. **Pre-commit hook** — linter + formatação (rápido)
2. **Pipeline em PR** — unit + integration + análise estática (alguns minutos)
3. **Após merge no main** — suíte completa + E2E + security scan
4. **Deploy** — smoke tests após subir em staging/prod

**Regras:**

- **Rapidez importa.** Pipeline lento = todo mundo desabilita testes.
- **Paralelize** o que conseguir. JUnit 5, Jest, Vitest suportam.
- **Falha rápido** (`fail-fast`) ao detectar problema claro.
- **Quarantine** para flaky tests enquanto você investiga — nunca deixe a suíte ficar vermelha "normalmente".
- **Não ignore warnings** do lint/types no CI.

---

## Armadilhas comuns

- **Testar implementação, não comportamento** — quebra em todo refactor
- **Over-mocking** — mocka todas as dependências e acaba testando os mocks
- **Under-mocking** — testes de unit batem em banco, rede, filesystem (viram integração lenta)
- **Testes flaky** aceitos como normais
- **Coverage como métrica única** — incentiva asserções vazias
- **Ignorar edge cases** — testa só o "happy path"
- **Setup gigante** — cada teste tem 50 linhas de fixtures inline
- **Assertions fracas** — `assertTrue(result != null)` em vez de verificar o conteúdo
- **Nomes inúteis** — `test1`, `testShouldWork`
- **Um teste com 20 assertions** — quando falha, você não sabe por quê
- **Compartilhamento de estado** entre testes — ordem começa a importar
- **Não testar concorrência** em código multi-thread
- **Escrever testes depois da implementação e só pra bater coverage** — você perde o benefício do TDD de design
- **Confiar em mocks de libs de terceiros** — muitos bugs vêm de "achei que a lib funcionava assim"
- **Esquecer de testar o caminho de erro** — exceções, rollback, compensação
- **`@Transactional` em testes que testam concorrência** — invalida o cenário

---

## Na prática (da minha experiência)

> No MedEspecialista, o stack padrão é **JUnit 5 + AssertJ + Mockito + Testcontainers**. Unit tests para lógica de domínio (especialmente cálculos de comissão e regras de agenda), integration tests com PostgreSQL real via Testcontainers para repositórios e endpoints. CI/CD no GitHub Actions roda tudo em paralelo — a suíte de ~800 testes leva ~3 minutos. **Regra: PR sem teste não é revisado.**
>
> **Um caso onde TDD me salvou:** a regra de cálculo de comissão tinha cinco condições e múltiplas exceções por especialidade. Comecei escrevendo testes para cada cenário (com Object Mothers) antes de qualquer implementação. O resultado: ao escrever o quinto teste, percebi que minha abstração inicial estava errada — refatorei e recomecei sem medo, porque os testes anteriores pegavam qualquer quebra.
>
> **Um caso onde TDD atrapalharia:** uma tela de cadastro com 30 campos e validações padrão. Aqui, o pragmatismo venceu: implementei direto e escrevi testes depois focando em edge cases (campos nulos, máximo de caracteres, formatos inválidos).
>
> **Sobre mocks vs fakes:** migrei de `@Mock UserRepository` com `when().thenReturn()` por todo lado para uma implementação `InMemoryUserRepository extends UserRepository` com `HashMap`. Ficou **muito mais legível** e os testes pararam de quebrar em refatorações que só mudavam a ordem de chamadas.
>
> **Sobre testes flaky:** tive uma suíte com 3 testes flaky por race condition em código assíncrono. A primeira reação foi adicionar `Thread.sleep(500)`. Funcionou... até o CI lento falhar de novo. A solução certa foi `Awaitility.await().atMost(5, SECONDS).until(() -> condição)`. Regra que criei: **nunca `sleep` em teste. Nunca.**
>
> **Sobre Testcontainers:** mudou completamente como eu escrevo testes de integração. Antes, tinha um PostgreSQL local "de teste" que drift-ava do de produção. Com Testcontainers, cada PR tem um PostgreSQL idêntico ao de produção, subido em segundos, descartado depois. Zero configuração compartilhada, zero drift.

---

## How to explain in English

> "My testing philosophy is pragmatic: I want fast feedback loops and high confidence in production, not coverage theater. In a Spring Boot project, that means JUnit 5 with AssertJ and Mockito for unit tests, and Testcontainers for integration tests that use real PostgreSQL, real Redis, real Kafka — whatever the production stack uses.
>
> I follow the testing pyramid as a guideline, not a rule. The real question I ask is: 'when this bug appears in production, what kind of test do I want to have caught it?' Logic bugs in isolated business rules — unit tests. Wiring bugs in controllers and repositories — integration tests. Critical user flows — a small set of E2E tests. I don't write E2E for everything; they're too slow and too flaky to maintain at scale.
>
> I use TDD when the design is unclear or the logic is complex, because writing the test first forces me to design the API before the implementation. For straightforward CRUD, I write the code first and the tests right after, focusing on edge cases — empty input, nulls, boundary values, unicode, timezones.
>
> One principle I hold strongly: test behavior, not implementation. If I can refactor the internals and the tests break, the tests are wrong. I prefer state-based assertions over interaction verification, and I prefer fakes — small in-memory implementations — over deeply mocked dependencies. A `FakeRepository` with a HashMap is often more robust and more readable than a Mockito mock.
>
> And on flaky tests: zero tolerance. A flaky test destroys confidence in the entire suite. When I find one, it goes to quarantine immediately and gets fixed — not re-run until it happens to pass. I never use `Thread.sleep` in tests; I use `Awaitility` or a controlled Clock."

### Frases úteis em entrevista

- "I'd start with the pyramid as a baseline, but adjust based on where the risk actually lives."
- "I prefer state-based testing over interaction-based — it couples less to the implementation."
- "I'd use Testcontainers for this so the test hits a real PostgreSQL instead of an in-memory H2 that drifts from production."
- "This is a good candidate for property-based testing because the invariant is clear."
- "I'd write the test first here — the logic is complex enough that designing the API through the test saves rework."
- "For flaky tests, I quarantine first and investigate. We never ship a suite that's 'usually green'."
- "100% coverage is a false signal — I aim for meaningful coverage of business logic and edge cases."

### Key vocabulary

- teste unitário → unit test
- teste de integração → integration test
- teste ponta a ponta → end-to-end test (E2E)
- teste de contrato → contract test
- teste de fumaça → smoke test
- teste de carga → load test
- teste de mutação → mutation test
- teste baseado em propriedades → property-based test
- cobertura de código → code coverage
- objeto simulado → mock
- dublê de teste → test double
- falso positivo → false positive
- teste intermitente → flaky test
- ambiente de teste → test environment
- suíte de testes → test suite
- fixture / acessório → fixture
- arranjo-ação-verificação → arrange-act-assert
- desenvolvimento guiado por testes → test-driven development (TDD)
- refatoração → refactoring
- integração contínua → continuous integration (CI)
- entrega contínua → continuous delivery (CD)
- caso extremo → edge case
- caminho feliz → happy path
- quarentena → quarantine

---

## Recursos

### Livros

- *xUnit Test Patterns* — Gerard Meszaros (a bíblia de test doubles e padrões)
- *Growing Object-Oriented Software, Guided by Tests* — Freeman & Pryce (GOOS — clássico de TDD)
- *Working Effectively with Legacy Code* — Michael Feathers (como testar código que não foi pensado para testes)
- *Unit Testing: Principles, Practices, and Patterns* — Vladimir Khorikov (muito bom sobre o que é um bom teste)
- *Test-Driven Development: By Example* — Kent Beck (o livro que começou tudo)

### Online

- [Testing Trophy — Kent C. Dodds](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
- [Mocks Aren't Stubs — Martin Fowler](https://martinfowler.com/articles/mocksArentStubs.html)
- [Testcontainers docs](https://testcontainers.com/)
- [Awaitility](https://github.com/awaitility/awaitility)
- [Testing Library principles](https://testing-library.com/docs/guiding-principles)

### Vídeo

> [!info] Aplicando Arquitetura Hexagonal com testes de integração e unidade
> [https://www.youtube.com/live/DWsxTJpxaOo?si=Pdtll7mDoe9wQJ9z](https://www.youtube.com/live/DWsxTJpxaOo?si=Pdtll7mDoe9wQJ9z)

## Veja também

- [[Testes em Java]]
- [[Orientação a Objetos]]
- [[Spring Boot]]
- [[Arquitetura de Software]]
