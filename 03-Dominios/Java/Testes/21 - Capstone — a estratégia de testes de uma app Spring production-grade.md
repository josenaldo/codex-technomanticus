---
title: "Capstone — a estratégia de testes de uma app Spring production-grade"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - testes
  - magus
aliases:
  - "Capstone de testes"
  - "estratégia de testes"
---

# Capstone — a estratégia de testes de uma app Spring production-grade

> [!abstract] TL;DR
> Uma suíte production-grade segue a **pirâmide**: muitos testes unitários rápidos na base, *slices* de Spring pra cada camada no meio, integração com **Testcontainers** acima e pouquíssimos E2E no topo. Use **AssertJ** pra asserções legíveis, mocke só os colaboradores que importam (não tudo), troque `Thread.sleep` por **Awaitility** em código assíncrono, e vá além do "verde": **mutation testing** mede se os testes pegam bug de verdade e **fitness functions** (ArchUnit) protegem a arquitetura. Cada decisão deste galho converge numa estratégia acionável — esta nota é o mapa.

## O que é

Os vinte verbetes anteriores deste galho cobriram ferramentas e técnicas isoladas: JUnit, AssertJ, Mockito, os *slices* do Spring, Testcontainers, Awaitility, StepVerifier, PIT, ArchUnit, Pact. Cada um resolve um problema pontual.

Mas saber usar cada ferramenta não é o mesmo que ter uma **estratégia**. Estratégia é a camada de decisão acima das ferramentas: quanto investir em cada nível, onde parar de testar, o que sacrificar quando o tempo aperta. É o que distingue um time que tem "uns testes" de um time cuja suíte é um ativo confiável que sustenta deploys diários.

O objetivo deste capstone é **consolidar tudo numa estratégia única e acionável**: dada uma aplicação Spring real (digamos, um `OrderService` com controllers REST, repositories JPA, chamadas a APIs externas e código assíncrono), em que nível você testa cada coisa, com qual ferramenta, e como você mantém a suíte rápida e confiável ao longo dos anos.

A resposta não é "teste tudo do mesmo jeito". É uma **distribuição deliberada** de esforço pela pirâmide, mais um conjunto de hábitos que separam uma suíte que ajuda de uma que atrapalha.

Vale separar dois objetivos que a suíte serve ao mesmo tempo, porque eles puxam decisões diferentes. O primeiro é **confiança pra mudar**: um conjunto de testes verdes que te deixa refatorar sem medo de quebrar comportamento. O segundo é **feedback rápido**: o vermelho tem que aparecer em segundos, não em minutos, senão o ciclo de desenvolvimento trava. A pirâmide existe justamente porque esses dois objetivos brigam — testes mais "completos" (E2E) dão mais confiança mas matam o feedback. A estratégia é equilibrar: muita confiança barata na base, um teto de confiança cara só onde o risco justifica.

## A pirâmide na prática

A pirâmide de testes é uma **heurística de distribuição**, não uma lei. A regra prática comum é concentrar a maior parte dos testes na base (baratos e rápidos) e ter cada vez menos conforme se sobe (caros e lentos):

| Nível | Proporção (regra prática) | Característica |
| --- | --- | --- |
| Unit | ~70-80% | Sem Spring, milissegundos cada |
| Integration / slice | ~15-25% | Sobem contexto parcial ou Testcontainers |
| E2E | ~2-5% | Sistema inteiro, lentos e frágeis |

> [!warning] Os números são heurística, não estatística
> "70-80% unit" é uma **regra prática comum**, não uma medição de quantos projetos fazem isso. Trate como ponto de partida pra calibrar, não como meta a bater. O que importa é o formato: base larga, topo estreito.

**Tempo de suíte alvo** (também heurística de saúde):

- Os testes unitários devem rodar em **menos de 30 segundos** localmente — rápido o bastante pra rodar a cada save.
- A suíte completa no CI (incluindo Testcontainers) deve fechar em **menos de 10 minutos** — passar disso e os devs começam a ignorar o vermelho.

Quando a pirâmide está invertida (muitos `@SpringBootTest`, poucos unit), a suíte fica lenta, o feedback demora, e o time perde a confiança nela. A forma da pirâmide é, ela mesma, uma fitness function.

Há um corolário econômico aqui que vale internalizar: o **custo de um teste não é só escrevê-lo, é mantê-lo**. Cada teste que sobe contexto, mexe em banco ou bate em rede é uma linha que vai ficar mais lenta, mais frágil e mais cara de diagnosticar conforme a base cresce. Um teste unitário, ao contrário, é praticamente grátis de rodar e raramente quebra por motivo errado. Por isso a base larga não é só "mais rápida" — ela é a parte da suíte que **continua barata sob escala**. Quando você se pega escrevendo o décimo `@SpringBootTest` pra checar uma regrinha de validação, é sinal de que aquela lógica devia estar isolada num colaborador testável por unit.

Uma forma de auditar a saúde da pirâmide no seu projeto: olhe o tempo agregado por tipo de teste no relatório do CI. Se os testes de integração somam mais minutos que os unitários, ou se o tempo total cresce mais rápido que o número de features, a pirâmide está pendendo pro lado errado.

## O que testar em qual nível

A pergunta operacional é: "dado este pedaço de código, qual o menor nível de teste que me dá confiança?". Suba só quando precisar.

- **Unit (base)** — lógica de negócio pura. Sem Spring, sem contexto. Instancie a classe à mão: `new OrderService(mockRepository, mockPricer)`. Mocke os colaboradores com Mockito. Aqui mora a regra "o desconto não pode passar de 50%", "pedido sem itens é inválido". Rápido, focado, à prova de refactor de infraestrutura.
- **Slice (meio-baixo)** — uma camada técnica isolada. `@WebMvcTest` pra serialização/rotas/validação de um controller (sem subir o banco). `@DataJpaTest` pra mapeamento JPA e queries de um repository (com banco real ou em memória). O *slice* sobe só os beans daquela fatia, então é muito mais rápido que o contexto completo.
- **Integração (meio-alto)** — várias camadas conversando de verdade. `@SpringBootTest` + **Testcontainers** subindo um Postgres real. Aqui você verifica que controller → service → repository → banco funciona ponta a ponta, com o dialeto SQL real e as transações reais.
- **E2E (topo)** — o sistema inteiro pelo HTTP, do jeito que o cliente usa. Caro e frágil. Reserve **só pros fluxos críticos de negócio** (ex.: "criar pedido e receber confirmação de pagamento"). Não tente cobrir variações de validação aqui — isso é trabalho de unit/slice.

Um exemplo de como a mesma regra de negócio se distribui pelos níveis, num `OrderService`:

- A regra "pedido sem itens é inválido" → **unit**, com `new OrderService(...)` e um mock do repository. Rápido, dezenas de variações.
- "POST /orders com corpo malformado retorna 400" → **slice** (`@WebMvcTest`): testa serialização e validação do controller, sem banco.
- "criar pedido persiste a linha e o total calculado bate" → **integração** (`@SpringBootTest` + Testcontainers): controller, service, repository e Postgres real.
- "cliente cria pedido, paga e recebe confirmação" → **E2E**: um único fluxo feliz, ponta a ponta.

Repare que a *mesma feature* aparece em vários níveis, mas cada nível verifica um aspecto diferente — e a maior parte das variações (todos os jeitos de um pedido ser inválido) vive na base barata, não no topo caro. Esse é o padrão a internalizar: **empurre a combinatória pra baixo**.

## A convergência numa tabela

Cada tipo de coisa que você testa tem uma ferramenta canônica e um galho da trilha que a aprofunda:

| O que testar | Ferramenta / slice | Galho dono |
| --- | --- | --- |
| Controller REST (rotas, JSON, validação) | `@WebMvcTest` + `MockMvc` | Galho 9 (Spring MVC) |
| Repository / mapeamento JPA | `@DataJpaTest` | Galho 10 (Spring Data) |
| Endpoint / pipeline reativo | `StepVerifier` + `@WebFluxTest` | Galho 11 (Programação Reativa) |
| Segurança (acesso, roles) | `@WithMockUser` + Spring Security Test | Galho 12 (Spring Security) |
| Contexto / slice / wiring do Spring | Spring Boot Test | Galho 8 (Spring Boot) |
| Código assíncrono (espera de efeito) | Awaitility | Galho 4 (Concorrência) |

Repare que **testar bem é testar cada camada com a ferramenta que entende aquela camada**. Não há uma ferramenta única; há uma para cada fronteira.

Isso também explica por que tantas técnicas deste galho existem em paralelo: elas não competem, elas cobrem fronteiras diferentes. AssertJ e Mockito (galhos 3 e 6-7) são transversais — você os usa em qualquer nível. Os *slices* (galhos 8-10) são o miolo Spring. Testcontainers (galho 11) é o que torna a integração honesta. E as técnicas "além do verde" — mutation testing, JMH, ArchUnit, Pact (galhos 17-20) — não testam *funcionalidade*, testam **propriedades da própria suíte e da arquitetura**: "meus testes pegam bug?", "isto é rápido?", "a dependência respeita as camadas?", "o contrato bate?". Uma estratégia production-grade combina os três blocos: ferramentas transversais + slices por camada + verificações de propriedade.

## Combate à flakiness

Um teste *flaky* (que passa e falha sem mudança de código) é pior que nenhum teste: ele treina o time a ignorar o vermelho. Os hábitos que mais protegem:

- **Nunca `Thread.sleep` pra esperar efeito assíncrono.** Dormir um tempo fixo é uma aposta: rápido demais quebra em CI lento, lento demais arrasta a suíte. Use **Awaitility** — ele faz *polling* até a condição virar verdadeira (ou estourar timeout), adaptando-se à máquina.
- **Testes independentes de ordem.** Cada teste prepara o próprio estado e limpa atrás de si. Se a suíte só passa numa ordem específica, há acoplamento escondido (estado estático, banco não resetado). Rode em ordem aleatória de propósito pra caçar isso.
- **Testcontainers, não "na minha máquina".** Depender do Postgres instalado no laptop de cada dev (versão X aqui, Y ali) é fonte clássica de flakiness. O container fixa a versão e a configuração pra todo mundo, inclusive o CI.
- **Investigue flaky, não "roda de novo que passa".** Reexecutar até passar mascara um bug real (condição de corrida, dependência de relógio, ordem). Trate cada flaky como defeito a diagnosticar — geralmente ele aponta um problema de concorrência ou de isolamento que também existe em produção.
- **Fixe o relógio e o fuso.** Testes que dependem de `LocalDate.now()` ou do *timezone* da máquina passam hoje e quebram à meia-noite ou no servidor em UTC. Injete um `Clock` controlável e fixe o fuso, em vez de ler o relógio do sistema dentro da lógica.

A flakiness merece atenção desproporcional porque o custo dela é **social**, não técnico. Um time que aprende a ignorar o vermelho perde a única coisa que a suíte oferece: o sinal de que algo quebrou. Um único teste instável que ninguém conserta erode a confiança em toda a suíte — as pessoas passam a presumir que o vermelho é "aquele flaky de sempre" e deixam passar regressões reais. Por isso a regra de ouro é: **flaky entra na fila de defeitos com prioridade de bug, não fica como "depois eu vejo"**.

## Cheatsheet nota → problema

Quando bater uma dúvida concreta durante o desenvolvimento, este índice aponta o verbete que a resolve:

| Problema / pergunta | Nota do galho |
| --- | --- |
| Como começo? Qual a pirâmide e o stack? | [[03-Dominios/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno\|nota 01]] |
| Como escrevo um teste JUnit 5 (lifecycle, AAA)? | [[03-Dominios/Java/Testes/02 - JUnit 5 — anatomia, lifecycle e o padrão AAA\|nota 02]] |
| Como faço asserções legíveis? | [[03-Dominios/Java/Testes/03 - AssertJ — fluent assertions\|nota 03]] |
| Como rodo o mesmo teste com vários inputs? | [[03-Dominios/Java/Testes/04 - Testes parametrizados e organização\|nota 04]] |
| Como evito setup duplicado e construtores enormes? | [[03-Dominios/Java/Testes/05 - Test data builders e fixtures\|nota 05]] |
| Como mocko colaboradores? | [[03-Dominios/Java/Testes/06 - Mockito — mocks, stubbing e matchers\|nota 06]] |
| Como verifico interações / capturo argumentos? | [[03-Dominios/Java/Testes/07 - Mockito — verify, ArgumentCaptor e quando NÃO mockar\|nota 07]] |
| Qual slice do Spring uso? | [[03-Dominios/Java/Testes/08 - Spring Boot Test e os slices — o contexto de teste\|nota 08]] |
| Como testo um controller? | [[03-Dominios/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc\|nota 09]] |
| Como testo um repository? | [[03-Dominios/Java/Testes/10 - @DataJpaTest — testando repositories\|nota 10]] |
| Como uso banco real no teste? | [[03-Dominios/Java/Testes/11 - Testcontainers — infra real em testes\|nota 11]] |
| Como testo o fluxo inteiro? | [[03-Dominios/Java/Testes/12 - Testes de integração ponta a ponta\|nota 12]] |
| Como testo endpoint protegido? | [[03-Dominios/Java/Testes/13 - Testando a segurança\|nota 13]] |
| Como testo código assíncrono? | [[03-Dominios/Java/Testes/14 - Testando código assíncrono — Awaitility\|nota 14]] |
| Como testo Mono/Flux? | [[03-Dominios/Java/Testes/15 - Testando código reativo — StepVerifier e @WebFluxTest\|nota 15]] |
| Como mocko uma API externa? | [[03-Dominios/Java/Testes/16 - Mockando HTTP externo — WireMock e MockRestServiceServer\|nota 16]] |
| Meus testes pegam bug de verdade? | [[03-Dominios/Java/Testes/17 - Mutation testing — PIT e cobertura honesta\|nota 17]] |
| Como meço performance corretamente? | [[03-Dominios/Java/Testes/18 - Performance — JMH e microbenchmarks\|nota 18]] |
| Como protejo a arquitetura? | [[03-Dominios/Java/Testes/19 - Fitness functions — ArchUnit (testes de arquitetura)\|nota 19]] |
| Como garanto contrato entre serviços? | [[03-Dominios/Java/Testes/20 - Contract testing — Pact\|nota 20]] |

## Armadilhas

São erros de **raciocínio**, não de sintaxe — armadilhas que parecem boas práticas até quebrarem.

### (1) "Coverage alto = código bem testado"

A intuição: o relatório diz 90% de cobertura de linhas, logo a suíte é boa. O problema: **line coverage só mede quais linhas executaram, não se algum teste falharia caso a linha estivesse errada**. Você pode "cobrir" uma linha sem fazer uma única asserção sobre o efeito dela. Cobertura vira teatro.

**Fix:** complemente com **mutation testing** (PIT, ver nota 17). O PIT altera o código (inverte um `>`, troca um `+` por `-`) e checa se algum teste fica vermelho. Se o teste passa com o código sabotado, ele não testava nada de útil. Mutation score é cobertura *honesta*.

### (2) "Quando na dúvida, use `@SpringBootTest`"

A intuição: subir o contexto inteiro garante que tudo funciona junto, então é o teste "mais completo". O problema: cada `@SpringBootTest` sobe (ou reusa) um ApplicationContext caro. Quando ele vira o teste padrão pra tudo — inclusive lógica que rodaria em milissegundos como unit — a suíte **inverte a pirâmide**: fica lenta, o feedback demora minutos, e os devs param de rodar localmente. Uma suíte que ninguém roda não pega bug nenhum.

**Fix:** suba o menor nível que dá confiança. Lógica de negócio → unit sem Spring. Camada técnica → *slice* (`@WebMvcTest`, `@DataJpaTest`). Reserve `@SpringBootTest` pros testes de integração que **realmente** precisam de várias camadas reais conversando.

### (3) "H2 em memória serve no lugar do Postgres"

A intuição: o H2 é rápido e zero-config, então é um banco "bom o bastante" pros testes de repository. O problema: o **dialeto SQL do H2 diverge do Postgres** — tipos (`jsonb`, arrays), funções, comportamento de `upsert`, *constraints*, modo de compatibilidade. O teste passa verde no H2 e a query quebra em produção: **falso-positivo**, o pior tipo de resultado de teste.

**Fix:** teste contra o **mesmo banco da produção** com **Testcontainers** (nota 11). Um container de Postgres na versão real elimina a classe inteira de bugs "passou no teste, quebrou em prod" causados por divergência de dialeto.

### (4) "Mockar tudo deixa o teste 'puro'"

A intuição: se eu mocko todos os colaboradores, o teste fica isolado e rápido — o ideal de teste unitário. O problema: mockar demais transforma o teste num **espelho da implementação**. Você acaba afirmando "o service chamou `repository.save()` uma vez" em vez de "o pedido foi de fato persistido". Aí qualquer refactor inocente (trocar `save` por `saveAll`) quebra o teste sem que nenhum comportamento tenha mudado — testes que quebram por motivo errado são tão nocivos quanto os que não pegam bug.

**Fix:** mocke **fronteiras**, não vizinhos. Mocke o que é caro, não-determinístico ou externo (rede, relógio, gateway de pagamento). Para colaboradores baratos e determinísticos, use a implementação real ou suba o *slice* certo. A nota 07 detalha exatamente quando **não** mockar.

## Em entrevista

### Frase pronta (inglês)

> "My testing strategy follows the test pyramid: the bulk of the suite is fast unit tests for business logic, instantiated without Spring so they run in milliseconds. Above that I use Spring's test slices — `@WebMvcTest` for controllers, `@DataJpaTest` for repositories — and a focused layer of integration tests with Testcontainers, so I'm running against the same Postgres version as production instead of an in-memory database that lies about the SQL dialect. I keep end-to-end tests for a handful of critical flows only, because they're slow and brittle. Beyond green tests, I lean on mutation testing to check whether the tests would actually catch a regression, and on ArchUnit fitness functions to keep architectural boundaries from eroding over time. And I never use `Thread.sleep` for async — Awaitility polls for the condition, which kills a whole class of flaky tests."

O entrevistador raramente quer ouvir nomes de ferramentas soltos. Ele quer ver que você **prioriza** — que entende o *trade-off* entre confiança e velocidade, que sabe onde parar de testar, e que pensa na suíte como algo que precisa continuar útil daqui a três anos, não só verde hoje. Ancore a resposta na pirâmide, cite uma ou duas técnicas "além do verde" (mutation testing, ArchUnit) pra mostrar maturidade, e termine com um hábito concreto anti-flakiness. Isso sinaliza senioridade sem precisar recitar APIs.

### Vocabulário

| Termo (inglês) | Tradução / sentido |
| --- | --- |
| test pyramid | pirâmide de testes (distribuição de esforço por nível) |
| test slice | fatia de teste (contexto Spring parcial) |
| flaky test | teste instável (passa/falha sem mudança) |
| mutation testing | teste de mutação (cobertura honesta) |
| fitness function | função de aptidão (teste automatizado de atributo arquitetural) |
| false positive | falso-positivo (teste verde escondendo bug) |
| feedback loop | ciclo de feedback (rapidez do verde/vermelho) |
| contract test | teste de contrato (acordo entre serviços) |

## Veja também

- [[03-Dominios/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno|O que é testar em Java]]
- [[03-Dominios/Java/Testes/12 - Testes de integração ponta a ponta|Testes de integração ponta a ponta]]
- [[03-Dominios/Java/Testes/17 - Mutation testing — PIT e cobertura honesta|Mutation testing — PIT]]
- [[03-Dominios/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]]

Galhos seguintes da trilha — observabilidade (Galho 14, planejado), mensageria (Galho 16, planejado) e deploy/cloud (Galho 17, planejado) — vão exigir suas próprias estratégias de teste, mas a base da pirâmide construída aqui permanece a mesma.

Se você for ler uma nota só depois desta, leia a [[03-Dominios/Java/Testes/17 - Mutation testing — PIT e cobertura honesta|17 (mutation testing)]]: é o verbete que mais muda a forma como você enxerga a própria suíte, porque transforma "tenho testes" em "sei que meus testes funcionam". É o passo que separa cobertura de teatro de cobertura de verdade.

## Referências

- Spring Boot Reference — Testing: https://docs.spring.io/spring-boot/reference/testing/index.html
