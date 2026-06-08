---
title: "EntityManager e o ciclo de vida da entidade"
created: 2026-06-07
updated: 2026-06-07
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - jakarta-ee
  - adepto
  - jpa
aliases:
  - "EntityManager"
  - "Persistence context"
  - "Ciclo de vida da entidade"
---

# EntityManager e o ciclo de vida da entidade

> [!abstract] TL;DR
> O `EntityManager` é a interface central da Jakarta Persistence — e o que ele de fato opera é um **persistence context**: um conjunto de entidades gerenciadas que funciona como **cache de identidade** (mesmo id → mesma instância) e **unit of work** (acumula mudanças e sincroniza com o banco no flush). Toda entidade está em um de **4 estados** — *new*, *managed*, *detached*, *removed* — e as operações da API (`persist`, `merge`, `remove`, `find`, `detach`, `refresh`) são **transições entre esses estados**. Quem entende o diagrama de estados entende 80% dos "bugs de JPA": `merge` que não salvou, UPDATE que nunca rodou, `LazyInitializationException`. Esta nota cobra o **contrato da spec 3.2**; como o provider implementa (e como otimizar) é assunto do Galho 10 (planejado).

---

## O que é

Na nota [[09 - JPA — a especificação de persistência]] vimos o contrato estático: `@Entity`, mapeamentos, relacionamentos, a persistence unit. Mas anotar uma classe não persiste nada. Quem **executa** a persistência — quem transforma objetos em linhas e linhas em objetos, em tempo de execução — é o **`EntityManager`** (`jakarta.persistence.EntityManager`), a interface central da spec.

Só que a melhor forma de entender o `EntityManager` **não é** pela lista de métodos. É pelo conceito que ele administra por baixo: o **persistence context**.

> [!important] O persistence context é o protagonista
> O javadoc da Persistence 3.2 define: um persistence context é *"um conjunto de instâncias de entidade no qual, para qualquer identidade persistente, existe no máximo uma instância de entidade"*. Em outras palavras: é um **espaço de trabalho** onde cada linha do banco tem **no máximo um representante em memória**, e onde toda mudança feita nesses representantes é **rastreada** até a hora de sincronizar com o banco. O `EntityManager` é a alça; o persistence context é o balde.

Esse espaço de trabalho dá ao `EntityManager` dois papéis simultâneos:

1. **Cache de identidade** — dentro do mesmo contexto, dois `find` pelo mesmo id retornam **a mesma instância** (`==`, não só `equals`);
2. **Unit of work** — mudanças nas entidades gerenciadas são acumuladas e viram SQL **de uma vez**, no momento do *flush* (tipicamente o commit da transação).

E toda entidade, em relação a um persistence context, está em um de **quatro estados** definidos pela spec — *new*, *managed*, *detached*, *removed*. A API inteira do `EntityManager` é, no fundo, uma máquina de transições entre esses estados.

---

## Por que importa

Aqui vai uma afirmação forte, mas defensável: **quase todo bug clássico de JPA é uma transição de estado mal entendida.**

- *"Chamei `merge` e a mudança sumiu"* → você mutou o **argumento** do `merge` (que continua detached) em vez do **retorno** (que é a managed);
- *"Por que meu UPDATE não rodou?"* → a entidade estava **detached** (ou não havia transação ativa), então o dirty checking não tinha o que rastrear;
- *"`LazyInitializationException` ao serializar pra JSON"* → você acessou uma associação lazy **depois** que a entidade ficou detached / o contexto fechou;
- *"Salvei duas vezes e duplicou"* / *"`EntityExistsException` do nada"* → `persist` numa entidade que não era *new*.

Nenhum desses bugs se resolve "tentando outro método até funcionar". Todos se resolvem olhando o diagrama de estados e perguntando: **em que estado essa entidade está agora, e o que essa operação faz nesse estado?**

### Em entrevista

O ciclo de vida da entidade é presença quase garantida em entrevista de vaga Java com persistência. As variações são previsíveis: *"qual a diferença entre `persist` e `merge`?"*, *"o que é uma entidade detached?"*, *"quando o SQL realmente executa?"*. A resposta senior desenha o diagrama de estados (mentalmente ou no quadro) e responde **a partir dele** — em vez de decorar comportamentos método a método. E sabe separar o que é **contrato da spec** do que é comportamento do provider.

---

## Como funciona

### O persistence context — identidade e unit of work

Os dois papéis do persistence context merecem ser desdobrados, porque cada um sustenta uma garantia diferente:

**Identidade.** Dentro de um persistence context, *"para qualquer identidade persistente existe no máximo uma instância de entidade"* (javadoc 3.2). Consequência prática: se você faz `em.find(Order.class, 42L)` duas vezes no mesmo contexto, recebe **o mesmo objeto** — a segunda chamada nem precisa ir ao banco, porque o contexto já tem o representante daquele id. Isso elimina o problema de "duas cópias da mesma linha com estados divergentes" *dentro* do contexto.

**Unit of work.** As entidades managed são **observadas**: o provider compara o estado delas com o estado que foi carregado/persistido e, na hora do flush, gera os `INSERT`/`UPDATE`/`DELETE` correspondentes. Você não chama "update" — não existe `em.update()` na API. Você **muta o objeto managed**, e a sincronização acontece como consequência. É por isso que JPA é descrita como persistência **transparente**: o código de negócio mexe em objetos; o SQL é efeito colateral gerenciado.

Pergunta retórica útil: *se não existe `update()`, como o provider sabe o que mudou?* Resposta: **dirty checking** — assunto de um H3 mais abaixo. Por ora, segure a ideia: managed = vigiada; fora do contexto = invisível.

### Os 4 estados e as transições

A spec define os estados assim (javadoc 3.2, parafraseado):

| Estado | Tem identidade persistente? | Associada a um contexto? | Destino no banco |
|---|---|---|---|
| **New** | não | não | nenhum (objeto Java comum) |
| **Managed** | sim | sim | sincronizada no flush |
| **Detached** | sim | **não** | nenhum — mudanças não são rastreadas |
| **Removed** | sim | sim | `DELETE` agendado para o flush/commit |

E as transições, conforme o capítulo de operações do `EntityManager` da spec:

```text
                persist()                       remove()
 ┌─────────┐ ───────────────► ┌─────────────┐ ───────────────► ┌─────────────┐
 │   NEW   │                  │   MANAGED   │                  │   REMOVED   │
 └─────────┘                  │             │ ◄─────────────── └─────────────┘
                              │  refresh()  │     persist()           │
                              │  (recarrega │                         │
                              │   do banco) │                    flush/commit
                              └─────────────┘                         │
                                  ▲      │                            ▼
              find() / query      │      │  detach() / clear()   (DELETE no
              merge(detached) ────┘      │  close() / fim da       banco)
              (retorna a managed)        │  tx (contexto
                                         ▼  transaction-scoped)
                                  ┌─────────────┐
                                  │  DETACHED   │
                                  └─────────────┘
```

Lendo o diagrama, operação por operação:

- **`persist(entity)`** — *new* → *managed*. A entidade passa a ter o `INSERT` agendado. Cascateia para associações com `cascade=PERSIST`. Em uma entidade que **já existe** (detached), o contrato manda falhar com `EntityExistsException` (que pode estourar na hora ou no flush/commit, dependendo de quando o provider detecta).
- **`find(Class, id)`** — carrega (do contexto, se já estiver lá; do banco, se não) e retorna uma entidade **managed**. Retorna `null` se não existe. Queries (JPQL) também devolvem entidades managed.
- **`merge(entity)`** — copia o estado de uma *new* ou *detached* para dentro do contexto e **retorna a instância managed**. Detalhe crucial no próximo H3.
- **`remove(entity)`** — *managed* → *removed*; o `DELETE` acontece no flush/commit. Em entidade **detached**, lança `IllegalArgumentException` — você não pode remover o que o contexto não conhece. Um `persist` numa *removed* a "ressuscita" de volta a *managed*.
- **`detach(entity)`** — ejeta a entidade do contexto imediatamente; ela vira *detached* e mudanças futuras nela são ignoradas. `clear()` faz isso com **todas** as entidades do contexto; `close()` (e o fim da transação, num contexto transaction-scoped) tem o mesmo efeito prático.
- **`refresh(entity)`** — *managed* → *managed*, mas **recarregando o estado do banco** e descartando mudanças ainda não flushadas. Exige entidade managed (`IllegalArgumentException` caso contrário); se a linha sumiu do banco, `EntityNotFoundException`.

Dois utilitários completam o quadro: **`contains(entity)`** responde se a instância está managed no contexto atual — ótimo para depurar estado; e a transição "silenciosa" mais importante do diagrama é a que **ninguém chama**: quando a transação termina num contexto transaction-scoped, **todas as entidades managed viram detached**. É daí que nascem os bugs da camada web (Armadilha 3).

### A semântica do `merge` — o retorno é o que vale

O `merge` é a operação mais mal-entendida da API, então vale parar nela. A assinatura já dá a pista:

```java
<T> T merge(T entity);
```

Ela **retorna algo** — e isso não é cosmético. Conforme a spec: o estado da entidade detached é **copiado** para uma instância managed correspondente (a que já está no contexto, ou uma carregada/criada para isso), e *"a operação merge retorna a instância managed para a qual o estado foi mesclado"*.

Traduzindo em consequências:

- O **argumento** do `merge` **não muda de estado** — segue detached (ou new), exatamente como entrou;
- O **retorno** é **outra instância** (no caso geral), e é **ela** que está managed e sob dirty checking;
- Toda mutação feita no argumento **depois** do `merge` cai no vazio.

Uma analogia: `merge` é como entregar um manuscrito numa editora. A editora **fotocopia** o conteúdo para o exemplar oficial dela (a managed) e te devolve **o exemplar oficial**. Rabiscar o seu manuscrito original depois disso não altera o que vai ser publicado. Se quiser continuar editando, edite o exemplar que a editora te devolveu.

```java
Order detached = ...;            // veio de outra request, cache, DTO...
Order managed = em.merge(detached);
managed.setStatus("PAID");       // ✅ rastreado — vira UPDATE no flush
detached.setStatus("CANCELLED"); // ❌ limbo — ninguém está olhando
```

`merge` também funciona com instância *new* (cria uma managed nova com aquele estado) e cascateia via `cascade=MERGE`. Em uma instância **removed**, lança `IllegalArgumentException`.

### Flush e dirty checking — quando o SQL acontece

Aqui mora a segunda surpresa de quem chega na JPA vindo de SQL manual: **chamar `persist`/`merge`/`remove` não executa SQL na hora** (como contrato geral — o provider tem alguma latitude). Essas operações mudam o **estado no contexto**; a sincronização com o banco acontece no **flush**.

Quando o flush acontece, segundo a spec, depende do `FlushModeType`:

| `FlushModeType` | Quando o contexto é flushado |
|---|---|
| **`AUTO`** (default) | No **commit** da transação; **antes da execução de queries** cujo resultado seria afetado pelo estado pendente; e antes de `refresh` |
| **`COMMIT`** | Apenas no **commit** da transação |

Além disso, a aplicação pode forçar a sincronização a qualquer momento com **`flush()`** explícito (que exige transação ativa — `TransactionRequiredException` sem ela).

O flush "antes de query" do modo `AUTO` é mais sutil do que parece: ele existe para que **uma query JPQL enxergue as mudanças pendentes do próprio contexto**. Se você persistiu um `Order` e na linha seguinte roda `SELECT o FROM Order o`, o provider flusha o `INSERT` pendente antes de executar a query — senão a query "não veria" o que você acabou de criar. É o contexto garantindo consistência consigo mesmo.

E o **dirty checking**? É o nome do mecanismo pelo qual o provider descobre, na hora do flush, **quais entidades managed mudaram** desde que entraram no contexto — e gera os `UPDATE` correspondentes. No nível da spec, o que está contratado é o **resultado**: *"o estado das entidades managed é sincronizado com o banco"* no flush, sem que a aplicação chame nada além de setters. **Como** o provider detecta as mudanças (snapshots, bytecode enhancement, etc.) é decisão de implementação — e território do Galho 10 (planejado).

> [!tip] Resumo em uma linha
> `persist`/`remove`/setters mudam **o plano**; `flush` (no commit, antes de query, ou explícito) **executa o plano**.

### JPQL e `TypedQuery` — consultando entidades, não tabelas

`find` resolve busca por id; para o resto existe a **Jakarta Persistence Query Language (JPQL)** — uma linguagem de consulta **orientada a entidades**: você seleciona objetos e navega atributos/associações, não tabelas e colunas. `SELECT o FROM Order o WHERE o.customer.name = :name` fala de classes e campos Java; o provider traduz para o SQL do dialeto de quem estiver por baixo.

A porta de entrada é o próprio `EntityManager`:

```java
TypedQuery<Order> q = em.createQuery(
    "SELECT o FROM Order o WHERE o.status = :status", Order.class);
q.setParameter("status", "OPEN");
List<Order> open = q.getResultList();
```

Pontos do contrato que valem fixar:

- **`createQuery(jpql, resultClass)`** retorna um **`TypedQuery<T>`** — a variante tipada, que evita casts e é a forma recomendada; `createQuery(jpql)` sem classe retorna a `Query` crua;
- **Parâmetros nomeados** (`:status`) com `setParameter("status", valor)` — prefira-os a parâmetros posicionais (`?1`) por legibilidade, e jamais concatene valores na string (mesma lição do SQL injection de sempre);
- **Terminadores**: `getResultList()` (lista, possivelmente vazia), `getSingleResult()` (exatamente um — `NoResultException` se zero, `NonUniqueResultException` se vários), e **`getSingleResultOrNull()`** — novidade da **spec 3.2** (confirmada no javadoc: *Since 3.2*), que devolve `null` em vez de exceção quando não há resultado (mas mantém `NonUniqueResultException` para múltiplos);
- `getResultStream()`, `setMaxResults(n)` e `setFirstResult(n)` completam o básico de consumo e paginação;
- Entidades retornadas por query ficam **managed** no contexto — sujeitas a dirty checking como qualquer outra.

Existe também a **Criteria API** — construção de queries via objetos Java tipados em vez de strings, útil para consultas dinâmicas; fica aqui como uma menção: o modelo conceitual (entidades, contexto, flush) é o mesmo.

### Quem gerencia o `EntityManager` — container vs aplicação

Até aqui falamos do `EntityManager` como se ele caísse do céu. A spec define **dois regimes** de obtenção e gerenciamento:

**Container-managed** — o regime padrão dentro de um servidor Jakarta EE. O container cria, gerencia e fecha o `EntityManager` por você; a aplicação só o **injeta**:

```java
@PersistenceContext
EntityManager em;
```

Nesse regime, as transações são **JTA** (demarcadas pelo container — tipicamente uma transação por método de negócio) e o persistence context default é **transaction-scoped**: nasce com a transação, morre com ela — e na morte, todas as managed viram **detached**. Existe a variante **extended** (persistence context que sobrevive a múltiplas transações), mas o caso comum — e o que você deve assumir por default — é o transaction-scoped.

**Application-managed** — a aplicação assume o ciclo: cria o `EntityManager` a partir de uma `EntityManagerFactory` e é responsável por **fechá-lo** (`close()`):

```java
EntityManagerFactory emf = Persistence.createEntityManagerFactory("loja");
EntityManager em = emf.createEntityManager();
// ... usar ...
em.close();
```

É o regime típico fora do container (Java SE, testes) com transações **resource-local**, demarcadas manualmente via **`EntityTransaction`** (`em.getTransaction().begin()` / `commit()` / `rollback()`).

A regra de bolso do contrato: **JTA = container demarca, você injeta e não fecha; resource-local = você cria, demarca via `EntityTransaction` e fecha.** Misturar os regimes — chamar `getTransaction()` num `EntityManager` JTA, por exemplo — é erro (`IllegalStateException`). A história completa de transações na plataforma — propagação, rollback, `@Transactional` — é a nota [[11 - JTA — transações na plataforma]].

---

## Na prática

Uma sessão completa, em regime application-managed (para deixar as transações explícitas e visíveis), percorrendo as transições do diagrama:

```java
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.EntityTransaction;
import jakarta.persistence.Persistence;
import jakarta.persistence.TypedQuery;
import java.util.List;

public class EntityLifecycleTour {

    public static void main(String[] args) {
        EntityManagerFactory emf =
                Persistence.createEntityManagerFactory("loja");
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();

        // ── 1. NEW → MANAGED: persist ───────────────────────────────
        tx.begin();
        Order order = new Order();          // NEW: objeto Java comum
        order.setStatus("OPEN");
        em.persist(order);                  // MANAGED: INSERT agendado
        tx.commit();                        // flush → INSERT executa aqui

        // ── 2. Dirty checking: mutação SEM update explícito ────────
        tx.begin();
        Order found = em.find(Order.class, order.getId()); // MANAGED
        found.setStatus("PAID");            // nenhum em.update() — não existe
        tx.commit();                        // flush detecta a mudança → UPDATE

        // ── 3. DETACHED: mutação que cai no vazio ──────────────────
        tx.begin();
        Order o2 = em.find(Order.class, order.getId());    // MANAGED
        em.detach(o2);                      // DETACHED: fora do contexto
        o2.setStatus("CANCELLED");          // ignorado — ninguém rastreia
        tx.commit();                        // flush: NENHUM SQL para o2

        // ── 4. DETACHED → MANAGED: merge (use o RETORNO!) ──────────
        tx.begin();
        Order managed = em.merge(o2);       // copia estado → retorna a MANAGED
        managed.setStatus("SHIPPED");       // ✅ rastreado (o2 segue detached)
        tx.commit();                        // flush → UPDATE com SHIPPED

        // ── 5. JPQL com TypedQuery e parâmetro nomeado ─────────────
        TypedQuery<Order> q = em.createQuery(
                "SELECT o FROM Order o WHERE o.status = :status",
                Order.class);
        q.setParameter("status", "SHIPPED");
        List<Order> shipped = q.getResultList();   // entidades MANAGED

        em.close();
        emf.close();
    }
}
```

Repare nos três momentos didáticos: o passo 2 **não tem** chamada de "save/update" — a mutação da managed basta; o passo 3 mostra a mutação **silenciosamente perdida** numa detached (o bug mais traiçoeiro da lista, porque não dá erro nenhum); e o passo 4 trabalha **com o retorno** do `merge`, nunca com o argumento.

Em ambiente container-managed, o mesmo código de negócio encolhe: `@PersistenceContext EntityManager em;` injetado, transação JTA demarcada pelo container, sem `begin`/`commit`/`close` manuais — as transições de estado são **exatamente as mesmas**.

---

## Armadilhas

### (1) Mutar o argumento do `merge` e descartar o retorno

O clássico dos clássicos. `merge` **não** torna o argumento managed — ele **copia** o estado para uma managed e **a retorna**. Quem ignora o retorno fica editando um objeto que ninguém observa:

```java
// ❌ mudança no limbo
em.merge(detachedOrder);
detachedOrder.setStatus("PAID");   // detached — nunca vira UPDATE

// ✅ trabalhe com a instância retornada
Order managed = em.merge(detachedOrder);
managed.setStatus("PAID");         // managed — UPDATE no flush
```

**Fix:** trate `merge` como uma função: o valor útil é o **retorno**. Reatribua (`order = em.merge(order);`) e siga a vida com a managed.

### (2) Esperar UPDATE sem transação ativa

Dirty checking só se materializa em SQL **no flush**, e flush exige transação. Mutar uma entidade managed fora de transação (ou nunca commitar) deixa as mudanças eternamente "no plano":

```java
// ❌ sem transação: a mudança nunca flusha
Order o = em.find(Order.class, 42L);
o.setStatus("PAID");               // e... nada. Nenhum UPDATE, nunca.

// ✅ demarque a transação
tx.begin();
Order o2 = em.find(Order.class, 42L);
o2.setStatus("PAID");
tx.commit();                       // flush no commit → UPDATE
```

**Fix:** toda escrita acontece **dentro** de uma transação — `EntityTransaction` no resource-local, JTA no container (e aí o sintoma muda: operações de escrita fora de transação lançam `TransactionRequiredException`, o que pelo menos avisa).

### (3) `LazyInitializationException` — acessar associação lazy com a entidade detached

O nome da exceção é do vocabulário dos providers, mas a **causa é pura máquina de estados**: uma associação `LAZY` é uma promessa — *"eu carrego quando você acessar"* — que **só o persistence context pode cumprir**. Quando a entidade vira detached (contexto fechou, transação acabou), a promessa fica sem fiador:

```java
// na camada de serviço (transação ativa)
Order o = em.find(Order.class, 42L);   // MANAGED; items é LAZY, não carregada
// ... transação commita, contexto transaction-scoped fecha → o vira DETACHED

// na camada web, serializando pra JSON
o.getItems().size();                   // 💥 associação não inicializada,
                                       // e não há mais contexto pra carregá-la
```

**Fix conceitual (nível desta nota):** acesse/inicialize a associação **enquanto a entidade está managed** — dentro da transação/contexto. As estratégias concretas de carregamento e seus trade-offs são assunto do Galho 10 (planejado); aqui o que importa é o diagnóstico: *a entidade estava detached, e lazy só funciona managed*.

### (4) Persistence context inflando em processamento em lote

O contexto é um cache de identidade que **só cresce**: cada entidade persistida/carregada fica managed até o fim. Num loop de 500 mil inserts, isso significa 500 mil objetos retidos em memória **e** um dirty checking cada vez mais caro a cada flush (mais managed = mais entidades para verificar):

```java
// ❌ contexto vira um balão: memória + flushes progressivamente caros
tx.begin();
for (int i = 0; i < 500_000; i++) {
    em.persist(new Order());
}
tx.commit();

// ✅ drene o contexto periodicamente
tx.begin();
for (int i = 0; i < 500_000; i++) {
    em.persist(new Order());
    if (i % 50 == 0) {
        em.flush();    // sincroniza os INSERTs pendentes
        em.clear();    // esvazia o contexto (tudo vira detached)
    }
}
tx.commit();
```

**Fix:** `flush()` + `clear()` em intervalos regulares — ambos são API da spec, nada de provider. Lembre que após o `clear()` **todas** as entidades viram detached; se precisar continuar mexendo em alguma, recarregue-a (`find`) ou faça `merge`.

---

## Em entrevista

### Frase pronta (inglês)

> "The EntityManager manages a persistence context, which plays two roles: an identity map — within one context, one persistent identity maps to at most one instance — and a unit of work that tracks changes to managed entities and synchronizes them on flush. Every entity is in one of four states — new, managed, detached, or removed — and operations like persist, merge, remove, and detach are just transitions between those states. The classic pitfalls all come down to state: merge returns the managed copy while the argument stays detached, dirty checking only turns into SQL when a flush happens inside an active transaction, and a LazyInitializationException simply means you touched a lazy association after the entity became detached. Once you reason from the state diagram instead of memorizing method behaviors, most JPA bugs become trivial to diagnose."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| contexto de persistência | persistence context |
| ciclo de vida da entidade | entity lifecycle |
| entidade gerenciada | managed entity |
| entidade desanexada | detached entity |
| unidade de trabalho | unit of work |
| mapa de identidade | identity map |
| verificação de sujeira (rastreio de mudanças) | dirty checking |
| sincronização com o banco | flush |
| transação resource-local | resource-local transaction |

---

## Veja também

- [[09 - JPA — a especificação de persistência]] — o contrato estático: `@Entity`, mapeamentos, persistence unit;
- [[11 - JTA — transações na plataforma]] — quem demarca a transação que faz o flush acontecer;
- [[03-Dominios/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#EntityManager|EntityManager (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#persistence context|persistence context (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#dirty checking|dirty checking (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#JPQL|JPQL (Dicionário)]]

---

## Referências

- [Jakarta Persistence 3.2 — Specification](https://jakarta.ee/specifications/persistence/3.2/) — acesso em 2026-06-07
- [Jakarta Persistence 3.2 — Specification Document (HTML)](https://jakarta.ee/specifications/persistence/3.2/jakarta-persistence-spec-3.2) — acesso em 2026-06-07
- [Jakarta Persistence 3.2 — Javadoc: `EntityManager`](https://jakarta.ee/specifications/persistence/3.2/apidocs/jakarta.persistence/jakarta/persistence/entitymanager) — acesso em 2026-06-07
- [Jakarta Persistence 3.2 — Javadoc: `TypedQuery`](https://jakarta.ee/specifications/persistence/3.2/apidocs/jakarta.persistence/jakarta/persistence/typedquery) — acesso em 2026-06-07
