---
title: "@DataJpaTest — testando repositories"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - testes
  - adepto
  - spring-test
  - datajpatest
aliases:
  - "@DataJpaTest"
  - "TestEntityManager"
---

# @DataJpaTest — testando repositories

> [!abstract] TL;DR
> `@DataJpaTest` carrega só a camada JPA e testa repositories em transação com rollback automático; o `TestEntityManager` prepara o estado (persist/flush) sem passar pelo seu repositório. Por default ele troca o datasource por um H2 embutido — rápido, mas mentiroso. Em produção-grade você desliga essa troca (`@AutoConfigureTestDatabase(replace = Replace.NONE)`) e aponta pra um Postgres real via Testcontainers, pra não colher falso-positivo de dialeto.

## O que é

`@DataJpaTest` é um *slice* de teste do Spring Boot focado na persistência. Em vez de subir o `ApplicationContext` inteiro (controllers, services, beans de configuração, segurança), ele restringe o component scan e carrega só o necessário pra exercitar JPA: `@Entity`, configuração do Spring Data JPA e os repositories. Beans comuns (`@Component`, `@ConfigurationProperties`) ficam de fora.

A ideia é responder uma pergunta cirúrgica: **meus repositories mapeiam e consultam o banco como eu espero?** Sem o peso de um teste de integração full-stack, mas com um `EntityManager` de verdade por trás — não um mock.

Onde ele se encaixa na pirâmide de testes: acima do teste unitário puro (que mockaria o repository) e abaixo do teste de integração full (`@SpringBootTest`, que sobe a aplicação inteira). É um teste de integração *estreito* — integra com o banco, mas só com o banco. Esse foco é o que o torna barato o suficiente pra rodar a cada commit sem virar gargalo do pipeline.

Os repositories e as derived queries testados aqui são os do Galho 10 — veja [[03-Dominios/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]]. Esta nota não re-explica o que é um repository: ela mostra como **testá-lo**.

## Por que importa

Um repository é a fronteira entre o seu código Java e o SQL que o banco realmente roda. É exatamente o ponto onde a abstração mais vaza: nome de método errado vira query errada, mapeamento de coluna errado vira `NULL` silencioso, função específica de Postgres simplesmente não existe noutro banco.

Testar isso com mock não vale nada — você estaria testando o mock, não a query. `@DataJpaTest` dá o meio-termo certo: rápido o bastante pra rodar a cada commit, real o bastante pra pegar erro de mapeamento e de query. E o slice mantém o teste honesto: se ele passa, é porque a *camada de persistência* funciona, não porque algum bean de service mascarou o problema.

A armadilha — e o motivo desta nota ser densa — é que o "rápido" default (H2) e o "real" (Postgres) divergem o suficiente pra um teste verde te dar falsa confiança. Saber quando trocar é a diferença entre um teste que protege e um que ilude.

Há ainda um ângulo de design que `@DataJpaTest` força à tona: como o slice exclui services e beans de aplicação, um repository que insiste em depender deles simplesmente não testa. O teste vira, de quebra, um detector de acoplamento errado — se você não consegue exercitar a camada de persistência isolada, é porque ela não está isolada de fato. Esse é um dos motivos pelos quais a comunidade trata o slice não só como ferramenta de verificação, mas como pressão arquitetural saudável.

## Como funciona

### @DataJpaTest carrega só a camada JPA

Ao anotar a classe de teste com `@DataJpaTest`, o Spring Boot monta um contexto mínimo: configuração do Spring Data JPA, varredura de `@Entity`, os repositories e um `EntityManager` gerenciado. Controllers, services e a maioria dos beans de aplicação **não** entram. É o mesmo princípio de slice de [[03-Dominios/Java/Testes/08 - Spring Boot Test e os slices — o contexto de teste|Spring Boot Test e os slices]]: cada slice restringe o component scan a uma fatia e carrega um conjunto enxuto de auto-configurações.

Consequência prática: se o seu repository depende de algum bean que está fora do slice, o teste falha ao subir o contexto — e isso é um sinal, não um bug. Repository não deveria depender de service.

Por baixo, o slice é só uma meta-anotação: ele agrega um conjunto de auto-configurações relacionadas a JPA e marca a classe como transacional. Você não precisa decorar a lista — o ponto é entender que o que entra no contexto é deliberadamente pequeno, e que esse enxugamento é a fonte tanto da velocidade quanto da disciplina arquitetural que o teste impõe.

### TestEntityManager: persist / flush sem passar pelo repositório

`@DataJpaTest` injeta um bean especial: o `TestEntityManager`. Ele é um wrapper de teste sobre o `EntityManager` da JPA, com uma API mais conveniente:

- `persist(entity)` — insere a entidade no contexto de persistência;
- `flush()` — força a sincronização das mudanças pendentes pro banco (dispara o `INSERT`/`UPDATE` agora);
- `find(Class, id)` — busca por chave primária.

A razão de existir é **isolar o arranjo (arrange) da verificação (assert)**. Você prepara o estado do banco com o `TestEntityManager` (caminho independente) e depois exercita o *repository* sob teste. Se usasse o próprio repository pra inserir e pra ler, um bug no `save` poderia esconder um bug no `findBy...`. Separar as duas pontas evita esse ponto cego.

Um detalhe que vale internalizar: o `persist` do `TestEntityManager` retorna a entidade já gerenciada, com o ID gerado preenchido. Por isso o padrão idiomático é `Customer c = em.persist(new Customer(...))` — você captura a referência pra usar o ID na consulta do act. E há um companheiro útil, `em.persistFlushFind(...)`, que persiste, dá flush e relê a entidade do banco numa tacada só, garantindo que você está olhando o que o banco materializou, não o objeto que você mesmo construiu em memória.

### Transação + rollback automático por teste

Cada método de teste sob `@DataJpaTest` roda **dentro de uma transação que sofre rollback ao final**. Você insere dados, consulta, faz asserts — e quando o teste termina, tudo é desfeito. O banco volta ao estado anterior.

Isso dá dois ganhos: testes não interferem uns nos outros (sem ordem de execução frágil) e o banco fica limpo sem teardown manual. O preço é uma pegadinha sutil: como nada é commitado, comportamentos que só ocorrem *no commit* (alguns triggers, certas constraints adiadas) não disparam. E entre o `persist` e a query, a JPA pode segurar o `INSERT` em memória — daí a necessidade do `flush()` (veja Armadilha 3).

Tecnicamente, esse rollback vem do mesmo mecanismo do `@Transactional` do Spring em testes: o slice marca a classe como transacional e o framework reverte ao final por padrão. Se, num caso raro, você *precisar* que um teste específico commite (ciente de que terá de limpar a sujeira), existe a anotação `@Commit` no método — mas tratá-la como saída de emergência, não como hábito. O default de rollback é uma feature, não uma limitação a contornar.

### H2 default vs banco real (Replace.NONE + Testcontainers)

Por default, `@DataJpaTest` **substitui o seu datasource configurado por um banco embutido em memória** (tipicamente H2). É rápido e não exige infra — ótimo pra feedback de segundos.

O problema: H2 não é Postgres. Funções específicas (`jsonb`, operadores de array, `ON CONFLICT`, tipos custom) ou simplesmente diferenças de dialeto fazem uma query passar no H2 e quebrar em produção. Pra eliminar esse risco você desliga a substituição:

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
```

Com `Replace.NONE`, o Spring Boot **não** troca o datasource pelo embutido — ele usa o que você apontar. Combinado com [[03-Dominios/Java/Testes/11 - Testcontainers — infra real em testes|Testcontainers]] (um Postgres real efêmero num container), você testa contra o mesmo banco que roda em produção, com dialeto idêntico. É a diferença entre "passou no H2" e "vai funcionar".

O trade-off é honesto: o H2 sobe em milissegundos, o container leva segundos pra iniciar. A prática madura é não escolher um *ou* outro de forma religiosa, e sim por contexto — H2 onde a query é trivial e portável (CRUD por chave, derived queries simples), Postgres real onde há recurso específico de dialeto, `@Query` nativa, ou JSONB. O container, com reuso ligado, amortiza o custo de boot ao longo da suíte, então o segundo a mais raramente domina o tempo total do build.

### A interação traiçoeira com o cache de primeiro nível

Há uma sutileza que decorre de testar dentro de uma única transação: o `EntityManager` mantém um *cache de primeiro nível* (a identidade do contexto de persistência). Se você `persist` uma entidade e depois lê pelo `find`, pode receber **o mesmo objeto em memória** — sem nenhuma ida ao banco. O teste fica verde, mas não provou que o mapeamento pro banco está correto; provou só que o objeto que você criou continua na memória.

Isso é especialmente perigoso ao validar mapeamentos não triviais (conversores, colunas geradas pelo banco, defaults). A defesa é `em.flush()` seguido de `em.clear()` — o `clear` esvazia o contexto, forçando a próxima leitura a buscar de verdade no banco e materializar a entidade do zero. É a diferença entre "o objeto ainda está aqui" e "o banco gravou e devolveu o que eu esperava". Esse mesmo cuidado se conecta à Armadilha 3, que trata da outra face do mesmo write-behind.

## Na prática

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:16-alpine");

    @Autowired
    OrderRepository orderRepository;

    @Autowired
    TestEntityManager em;

    @Test
    void findByCustomerId_retornaPedidosDoCliente() {
        // arrange: prepara o estado SEM passar pelo repositório sob teste
        Customer alice = em.persist(new Customer("Alice"));
        em.persist(new Order(alice, BigDecimal.valueOf(120.00)));
        em.persist(new Order(alice, BigDecimal.valueOf(35.50)));

        Customer bob = em.persist(new Customer("Bob"));
        em.persist(new Order(bob, BigDecimal.valueOf(9.99)));

        em.flush(); // força o INSERT antes da query — sem isso, a derived query não enxerga os dados

        // act: exercita a derived query do repository (Galho 10)
        List<Order> pedidosDaAlice = orderRepository.findByCustomerId(alice.getId());

        // assert
        assertThat(pedidosDaAlice).hasSize(2);
        assertThat(pedidosDaAlice)
            .extracting(Order::getCustomer)
            .containsOnly(alice);
    }
}
```

Pontos a notar:

- `@ServiceConnection` (Spring Boot 3.1+) liga o container ao datasource automaticamente — sem `@DynamicPropertySource` manual. Antes dessa anotação, era preciso registrar `spring.datasource.url/username/password` à mão a partir dos getters do container; hoje o slice descobre tudo pela própria imagem.
- O `static` no container é proposital: um único Postgres é reaproveitado por todos os métodos da classe (escopo de classe), em vez de subir um container por teste. Como cada teste faz rollback, o banco volta limpo sem precisar de container novo.
- O arrange usa `em.persist(...)`; o act usa `orderRepository`. Pontas separadas, ponto cego eliminado.
- `em.flush()` antes da query é deliberado — não decorativo (ver Armadilha 3).

O que é `findByCustomerId` e como a derived query vira SQL não está aqui de propósito: é assunto de [[03-Dominios/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]] e de [[03-Dominios/Java/Persistência de dados/09 - Consultas com @Query — JPQL, native e @Modifying|Consultas com @Query]].

### O que vale a pena cobrir num teste de repository

Nem toda query merece teste — testar o `findById` que o `JpaRepository` te dá de graça é redundante (você estaria testando o Spring Data, não o seu código). O retorno está nas queries que **você** escreveu:

- **Derived queries não triviais** — combinações de `And`/`Or`/`Between`/`OrderBy`, onde o nome do método é fácil de errar e o erro vira SQL silenciosamente diferente do que você quis.
- **`@Query` JPQL e nativas** — qualquer SQL escrito à mão é candidato número um, porque ali não há rede de proteção de geração automática.
- **Mapeamentos delicados** — conversores (`@Convert`), enums, colunas geradas pelo banco, relacionamentos com cascata. Aqui o `flush` + `clear` (ver "Como funciona") é essencial pra forçar o round-trip ao banco.
- **Casos de borda de dados** — resultado vazio, múltiplos resultados, `NULL` em coluna opcional. É onde derived queries costumam surpreender.

Quando o alvo é o **mapeamento** (e não a query), o padrão muda um pouco: persista, dê `flush`, limpe o contexto e releia, pra garantir que o que você inspeciona veio do banco:

```java
@Test
void mapeamentoDeStatus_persisteELeDoBanco() {
    Order salvo = em.persist(new Order(/* ... */));
    em.flush();   // empurra o INSERT pro banco
    em.clear();   // esvazia o cache de primeiro nível

    // agora a leitura vai REALMENTE ao banco e materializa do zero
    Order recarregado = orderRepository.findById(salvo.getId()).orElseThrow();
    assertThat(recarregado.getStatus()).isEqualTo(OrderStatus.NEW);
}
```

Sem o `clear`, o `findById` poderia devolver o mesmo objeto que você acabou de criar — e o teste passaria sem nunca ter validado o round-trip de fato.

## Armadilhas

### (1) H2 default escondendo bug de dialeto

O `@DataJpaTest` troca o seu Postgres por um H2 em memória sem você pedir. Aí uma query que usa recurso específico do Postgres passa no teste e explode em produção.

```java
// repository (Galho 10) — usa operador @> de JSONB do Postgres
@Query(value = "SELECT * FROM orders WHERE metadata @> :filter", nativeQuery = true)
List<Order> findByMetadataContains(@Param("filter") String filter);
```

No H2 esse operador não existe (ou se comporta diferente) — o teste verde te dá confiança que produção vai desmentir na primeira request.

**Fix:** `@AutoConfigureTestDatabase(replace = Replace.NONE)` + Testcontainers com a imagem `postgres` exata. O teste passa a rodar contra o mesmo dialeto da produção. Se for usar H2, que seja consciente e só pra queries triviais.

Vale notar que o H2 oferece *modos de compatibilidade* (`MODE=PostgreSQL`, por exemplo) que emulam parte do dialeto. É um paliativo útil, mas perigoso: ele cobre a sintaxe comum e mente exatamente nos cantos que importam (tipos custom, operadores de JSONB, comportamento de `NULL` em índices únicos). Tratar modo de compatibilidade como equivalente ao banco real é trocar um falso-positivo óbvio por um sutil. Quando o custo de errar é alto, container real, sem meio-termo.

### (2) assumir commit

Como cada teste roda em transação com rollback ao final, é tentador achar que o dado "ficou salvo". Não ficou — ele é desfeito quando o método termina.

```java
@Test
void salvaPedido() {
    orderRepository.save(new Order(/* ... */));
    // ao fim do teste: ROLLBACK. nada foi commitado, nada vazou pro próximo teste.
}
```

Dois efeitos colaterais: (a) você não pode "deixar dado pronto" pra outro teste depender — cada teste arranja o seu; (b) lógica que só dispara no commit (certos triggers, constraints `DEFERRED`) não é exercitada aqui.

**Fix:** trate cada teste como hermético — arrange completo dentro dele. Se precisa testar comportamento de commit real, isso é um teste de integração full (`@SpringBootTest`), não um slice de JPA.

Não confunda `flush` com commit: o `flush` empurra o SQL pro banco *dentro* da transação corrente (a query passa a enxergar o dado), mas a transação continua aberta e ainda sofre rollback ao final. Comportamento que depende literalmente do `COMMIT` — um trigger `AFTER ... ON COMMIT`, validação de constraint adiada, um listener `@TransactionalEventListener(phase = AFTER_COMMIT)` — nunca dispara sob `@DataJpaTest`. Querer "consertar" isso forçando commit no teste quebra o isolamento e contamina os testes seguintes; o caminho certo é mudar de ferramenta, não burlar o slice.

### (3) testar uma derived query sem `em.flush()` antes

Entre `em.persist(...)` e a sua query, a JPA pode segurar o `INSERT` no contexto de persistência (write-behind). A derived query roda direto no banco — e o banco ainda não viu os dados.

```java
@Test
void findByCustomerId_semFlush_falha() {
    Customer c = em.persist(new Customer("Alice"));
    em.persist(new Order(c, BigDecimal.TEN));
    // SEM em.flush() aqui

    List<Order> pedidos = orderRepository.findByCustomerId(c.getId());
    assertThat(pedidos).hasSize(1); // FALHA: vem vazio, o INSERT ainda não foi pro banco
}
```

A query enxerga zero linhas porque o `persist` continua só em memória. O detalhe traiçoeiro é a inconsistência: operações que passam pelo `EntityManager` (como `em.find` por ID) *podem* achar a entidade pelo cache de primeiro nível, enquanto uma derived query — que vira SQL e vai ao banco — não acha nada. Você acaba com um teste que "às vezes funciona", dependendo de qual caminho de leitura ele usa, o que é pior do que uma falha limpa e constante.

**Fix:** chame `em.flush()` depois de arranjar o estado e antes de exercitar o repository. Isso força o `INSERT` pro banco, e a query passa a enxergar os dados. Se quiser garantir também que você está lendo do banco e não do cache de primeiro nível (ver seção acima), acrescente `em.clear()` após o `flush`.

A regra de bolso que fecha a seção: **arrange → `flush` (→ `clear` se for validar mapeamento) → act → assert**. Internalizar essa sequência elimina de uma vez as armadilhas 2 e 3, que são apenas duas faces da mesma natureza diferida da transação JPA.

## Em entrevista

### Frase pronta (inglês)

> `@DataJpaTest` is a Spring Boot test slice that loads only the JPA layer — the repositories and a real `EntityManager` — so I can verify mappings and queries without spinning up the whole context. Each test runs in a transaction that rolls back at the end, which keeps tests isolated and the database clean without manual teardown. I use the `TestEntityManager` to arrange state independently from the repository under test, calling `flush` before the query so it actually hits the database. By default the slice swaps in an in-memory H2, but on production-grade code I set `@AutoConfigureTestDatabase(replace = Replace.NONE)` and point it at a real Postgres through Testcontainers, so I'm testing against the same dialect that runs in production instead of getting a false positive from H2.

### Vocabulário

| Termo (EN) | Significado |
|---|---|
| test slice | recorte do contexto que carrega só uma camada |
| auto-configured test | teste com infra montada automaticamente pelo Spring Boot |
| rolls back at the end | desfaz a transação ao final de cada teste |
| in-memory embedded database | banco em memória (H2) substituído por default |
| dialect | variações de SQL/funções específicas de cada banco |
| false positive | teste que passa, mas esconde um defeito real |
| `flush` | força a escrita pendente pro banco antes da consulta |
| `Replace.NONE` | desliga a troca do datasource pelo embutido |
| first-level cache | cache do contexto de persistência por transação |
| arrange / act / assert | preparar estado / exercitar / verificar |

## Veja também

- [[03-Dominios/Java/Testes/11 - Testcontainers — infra real em testes|Testcontainers]]
- [[03-Dominios/Java/Testes/08 - Spring Boot Test e os slices — o contexto de teste|Spring Boot Test e os slices]]
- [[03-Dominios/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]]
- [[03-Dominios/Java/Persistência de dados/09 - Consultas com @Query — JPQL, native e @Modifying|Consultas com @Query]]
- [[03-Dominios/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]]

## Referências

- Spring Boot Reference — Testing: Auto-configured Data JPA Tests (`@DataJpaTest`): https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html
