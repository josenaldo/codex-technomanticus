---
title: "Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly"
created: 2026-06-09
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - persistencia
  - magus
  - transacao
aliases:
  - "@Transactional"
  - "propagação de transação"
  - "transações no Spring"
---

# Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly

> [!abstract] TL;DR
> `@Transactional` define a **fronteira do caso de uso** na camada Service: tudo dentro do método ou commita junto, ou reverte junto. Pra dominar isso na prática você precisa de quatro botões: **propagação** (como uma transação se relaciona com outra já em curso), **isolamento** (o quanto ela enxerga das transações concorrentes), **rollback rules** (quem dispara a reversão — e o ponto que mais derruba gente: *checked exception NÃO faz rollback por default*) e **readOnly** (desabilita o dirty checking pra leituras). O *mecanismo* que faz tudo isso acontecer — o proxy AOP que envolve o bean — é assunto do Galho 8; aqui o foco é o **comportamento**.

## O que é

`@Transactional` é uma anotação declarativa que demarca onde uma transação de banco **começa** e **termina**. Você a coloca num método (ou na classe) da camada Service e o Spring garante que, quando o método retorna normalmente, a transação **commita**; quando ele lança uma exceção que dispara rollback, a transação **reverte** — desfazendo todas as escritas feitas no caminho.

A palavra-chave é **declarativa**: você não escreve `connection.commit()` nem `connection.rollback()` em lugar nenhum. Você *declara* a intenção ("este método é uma unidade transacional") e a infraestrutura cuida do `begin`/`commit`/`rollback` por baixo. Isso mantém o código de negócio limpo de APIs de transação.

Cada `@Transactional` carrega um punhado de atributos que ajustam *como* essa fronteira se comporta. Os quatro que importam no dia a dia: `propagation`, `isolation`, as **rollback rules** (`rollbackFor`/`noRollbackFor` + o default) e `readOnly` (mais `timeout` como coadjuvante).

## Por que importa

A transação é o lugar onde "consistência" deixa de ser um conceito e vira código. Um caso de uso típico — "registrar um pedido" — toca várias tabelas: cria o `Order`, debita o estoque do `Product`, lança um registro financeiro no `Account`. Se o débito de estoque falhar no meio, você **não** pode deixar o `Order` criado órfão. A transação é o que transforma essas N escritas numa operação atômica: tudo ou nada.

Errar a configuração transacional produz os bugs mais traiçoeiros que existem, porque eles **não estalam na sua cara** — eles corrompem dados silenciosamente em produção. Um `rollbackFor` esquecido faz uma operação que "deveria" reverter commitar pela metade. Uma transação na camada errada (no Controller em vez do Service) deixa a fronteira ampla demais. Uma propagação mal escolhida faz uma auditoria sumir junto com o rollback do negócio que ela deveria registrar.

Em entrevista sênior, "o que faz rollback por default?" e "o que acontece se você chama um método `@Transactional` de dentro da mesma classe?" são perguntas de eliminação. Quem sabe, sabe; quem decora a anotação sem entender o comportamento, tropeça.

## Como funciona

### Propagação — como uma transação se relaciona com outra em curso

**Propagação** responde: "quando este método é chamado, *já existe* uma transação ativa? E aí, o que eu faço?". O valor é definido em `@Transactional(propagation = Propagation.X)`.

- **`REQUIRED`** (o **default**): junta-se à transação existente se houver uma; senão, cria uma nova. É o que você quer 95% do tempo. Vários métodos Service chamando uns aos outros compartilham **uma única** transação física.
- **`REQUIRES_NEW`**: **sempre** cria uma transação nova e independente, suspendendo a de fora se ela existir. A transação interna commita ou reverte **por conta própria**, sem amarração com a externa. Caso clássico: **auditoria/log** que precisa persistir *mesmo que o negócio reverta* — você quer registrar "tentativa de criar Order falhou" e esse registro não pode sumir no rollback do `Order`.
- **`NESTED`**: cria um **savepoint** dentro da transação atual. Se a parte aninhada falhar, faz rollback **só até o savepoint**, preservando o que veio antes; o commit final ainda depende da transação externa. Diferente de `REQUIRES_NEW`, não é uma transação física separada — é um ponto de retorno parcial (exige suporte a savepoints no driver/banco).
- **`MANDATORY`**: exige que já exista uma transação; se não houver, **lança exceção**. Útil pra métodos que *jamais* devem rodar sozinhos.
- **`SUPPORTS`**: usa a transação se houver uma; senão, roda sem transação. Não força nada.
- **`NOT_SUPPORTED`**: roda **fora** de qualquer transação, suspendendo a atual se existir.
- **`NEVER`**: lança exceção se *houver* uma transação ativa. O oposto de `MANDATORY`.

A diferença entre `REQUIRES_NEW` e `NESTED` é a pegadinha favorita: `REQUIRES_NEW` é uma transação **independente** (commita sozinha, sobrevive ao rollback de fora); `NESTED` é um **savepoint** dentro da mesma transação (o commit ainda é da externa).

### Isolamento — o quanto a transação enxerga das concorrentes

**Isolamento** controla quanto uma transação vê das alterações **não confirmadas** (ou confirmadas durante seu curso) de outras transações rodando em paralelo. Os quatro níveis padrão da ANSI, do mais frouxo ao mais rígido:

- **`READ_UNCOMMITTED`**: enxerga escritas não commitadas de outras transações (*dirty reads*). Quase nunca usado.
- **`READ_COMMITTED`**: só enxerga dados já commitados; evita dirty reads. É o **default do PostgreSQL**.
- **`REPEATABLE_READ`**: além disso, garante que reler a mesma linha dá o mesmo resultado dentro da transação. É o **default do MySQL/InnoDB**.
- **`SERIALIZABLE`**: o mais rígido — transações concorrentes se comportam como se rodassem em sequência. Máxima consistência, menor concorrência.

Você define com `@Transactional(isolation = Isolation.READ_COMMITTED)`. O default (`Isolation.DEFAULT`) **delega ao banco** — por isso é crucial saber qual é o default do seu SGBD.

> [!note] A teoria mora em Banco de dados
> Os *fenômenos* que cada nível previne — dirty read, non-repeatable read, phantom read — e o trade-off concorrência × consistência são teoria de banco de dados, não de Spring. Veja [[03-Dominios/Ciência/Banco de dados|Banco de dados]]. Aqui interessa apenas *como acionar* o nível pela anotação e qual é o default da sua plataforma.

Detalhe operacional: `isolation`, `timeout` e `readOnly` só fazem sentido quando a propagação **abre** uma transação física — ou seja, `REQUIRED` (quando inicia uma nova) ou `REQUIRES_NEW`. Se o método apenas se junta a uma transação já existente, esses atributos são ignorados (e o Spring pode até alertar dependendo da config).

### Rollback rules — quem dispara a reversão

Esta é **a** seção que separa quem entende de quem decora. O comportamento **default** do Spring:

> Qualquer `RuntimeException` (unchecked) ou `Error` dispara rollback. Qualquer **checked `Exception` NÃO dispara rollback** — a transação **commita** normalmente.

Leia de novo: se o seu método lança uma checked exception (uma que estende `Exception` mas não `RuntimeException`), o Spring **commita a transação** assim mesmo. Isso surpreende quase todo mundo, porque a intuição diz "lançou exceção → desfaz tudo". No Spring, não — não por default.

Pra mudar isso por método, use os atributos:

- **`rollbackFor`**: lista de tipos de exceção que *devem* causar rollback (tipicamente uma checked sua). Ex.: `@Transactional(rollbackFor = Exception.class)`.
- **`noRollbackFor`**: o inverso — exceções que *não* devem reverter, mesmo sendo unchecked.

As regras customizadas **sobrescrevem** o default apenas pros tipos listados; pro resto, o default continua valendo.

Além das regras por tipo, há o gatilho **programático**: a partir de qualquer ponto você pode marcar a transação corrente como "condenada" via `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()`. Isso força o rollback no fim do método **sem** lançar exceção. Cuidado com o efeito colateral clássico: se um método interno marca `setRollbackOnly` e o método externo *engole* a exceção e tenta commitar, o Spring lança `UnexpectedRollbackException` ("Transaction silently rolled back because it has been marked as rollback-only").

### `readOnly`, timeout e a transação na camada Service

**`readOnly = true`** sinaliza que a transação só **lê**, nunca escreve. O ganho não é só semântico: com JPA/Hibernate, uma transação readOnly **desabilita o dirty checking** — o provider não tira *snapshots* das entidades carregadas pra comparar no flush, porque sabe que não vai haver flush. Em consultas que trazem muitas entidades, isso economiza memória e CPU. O banco também pode aplicar otimizações próprias para conexões somente-leitura.

**`timeout`** (em segundos) limita quanto a transação pode durar antes de ser abortada — uma rede de segurança contra locks longos travando o sistema. Como `isolation`, só vale quando a propagação abre transação física.

**Onde colocar a anotação?** Na camada **Service**, não no Controller nem no Repository. O Service é onde mora o *caso de uso* — a unidade de trabalho que precisa ser atômica. O padrão idiomático: anote a **classe** com `@Transactional(readOnly = true)` (leitura é o caso comum e o mais barato) e **sobrescreva** os métodos de escrita com `@Transactional` (read-write). Configuração no nível de método **tem precedência** sobre a da classe.

> [!warning] O mecanismo é do Galho 8
> Tudo isso funciona porque o Spring envolve seu bean num **proxy AOP** que intercepta a chamada, abre a transação antes do método e commita/reverte depois. *Como* esse proxy é construído e *por que* ele tem limites (self-invocation, métodos `final`/`private`) é assunto de [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies (o mecanismo)]]. Esta nota cobre o **comportamento**, não a maquinaria.

## Na prática

Camada Service com leitura como default na classe e escrita sobrescrevendo o método. A auditoria roda em `REQUIRES_NEW` pra sobreviver a um rollback do negócio. A criação do pedido declara `rollbackFor` pra que uma checked exception também reverta.

```java
import jakarta.persistence.EntityManager;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true) // default da classe: leitura, sem dirty checking
public class OrderService {

    private final OrderRepository orders;
    private final ProductRepository products;
    private final AuditService audit;

    public OrderService(OrderRepository orders,
                        ProductRepository products,
                        AuditService audit) {
        this.orders = orders;
        this.products = products;
        this.audit = audit;
    }

    // método de leitura: herda readOnly = true da classe
    public Order findById(Long id) {
        return orders.findById(id)
                .orElseThrow(() -> new OrderNotFoundException(id));
    }

    // sobrescreve com read-write E rollbackFor pra checked exception também reverter
    @Transactional(rollbackFor = InsufficientStockException.class, timeout = 10)
    public Order placeOrder(Long customerId, Long productId, int qty)
            throws InsufficientStockException {

        Product product = products.findById(productId)
                .orElseThrow(() -> new ProductNotFoundException(productId));

        if (product.getStock() < qty) {
            // checked exception: SEM rollbackFor, a tx commitaria assim mesmo!
            audit.record("STOCK_FAIL", "produto " + productId);
            throw new InsufficientStockException(productId, qty);
        }

        product.decreaseStock(qty);              // dirty checking faz o UPDATE
        Order order = new Order(customerId, productId, qty);
        orders.save(order);
        audit.record("ORDER_PLACED", "pedido " + order.getId());
        return order;
    }
}
```

```java
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuditService {

    private final AuditRepository auditRepo;

    public AuditService(AuditRepository auditRepo) {
        this.auditRepo = auditRepo;
    }

    // REQUIRES_NEW: transação independente — o registro persiste
    // MESMO que a transação de OrderService dê rollback depois.
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void record(String event, String detail) {
        auditRepo.save(new AuditEntry(event, detail));
    }
}
```

No exemplo, `placeOrder` declara `rollbackFor = InsufficientStockException.class` — uma **checked exception**. Sem isso, lançar `InsufficientStockException` faria o Spring **commitar** a transação (o default ignora checked). Já a auditoria em `REQUIRES_NEW` commita independentemente: o registro `STOCK_FAIL` sobrevive porque roda em transação física separada.

## Armadilhas

### (1) Checked exception não faz rollback por default

A pegadinha número um. Um método `@Transactional` lança uma **checked exception** e você espera que tudo seja revertido — mas a transação **commita**, deixando dados pela metade.

```java
@Transactional // SEM rollbackFor
public void transfer(Long from, Long to, BigDecimal amount) throws InsufficientFundsException {
    Account source = accounts.findById(from).orElseThrow();
    source.debit(amount);                 // UPDATE acontece
    if (source.getBalance().signum() < 0) {
        throw new InsufficientFundsException(); // checked → NÃO reverte!
    }
    accounts.findById(to).orElseThrow().credit(amount);
}
```

Aqui o débito é commitado mesmo lançando a exceção — o `Account` de origem fica com saldo errado e o destino nunca recebe. **Fix:** `@Transactional(rollbackFor = Exception.class)` (ou o tipo específico). Regra de bolso: se você usa checked exceptions de negócio, **sempre** declare `rollbackFor`.

### (2) Self-invocation não passa pelo proxy

Chamar um método `@Transactional` a partir de **outro método da mesma classe** (via `this.metodo()`) **não** ativa a transação daquele método.

```java
@Service
public class ReportService {
    public void run() {
        loadData(); // self-invocation: @Transactional de loadData é IGNORADO
    }

    @Transactional(readOnly = true)
    public void loadData() { /* ... */ }
}
```

A chamada `loadData()` é `this.loadData()`, que vai direto ao objeto real — **sem** passar pelo proxy que aplicaria a transação. O *porquê* disso (o proxy só intercepta chamadas externas ao bean) está em [[03-Dominios/Tecnologia/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]]. Soluções: extrair o método para outro bean, ou injetar uma referência ao próprio proxy.

### (3) `@Transactional` em método `private` ou `final` é ignorado

O proxy só consegue interceptar métodos que ele consegue sobrescrever/envolver. Métodos **`private`** nunca são interceptados (a anotação é silenciosamente ignorada). Métodos **`final`** não podem ser sobrescritos por um proxy baseado em subclasse (CGLIB), então também escapam.

```java
@Service
public class CustomerService {
    @Transactional
    private void archive(Customer c) { /* ... */ } // privado: anotação ignorada!

    @Transactional
    public final void deactivate(Customer c) { /* ... */ } // final: idem, em proxy CGLIB
}
```

Nenhum dos dois roda transacional. Mantenha métodos `@Transactional` **`public`** (ou ao menos não-`private` e não-`final`). O *motivo* mecânico — como o proxy é gerado e o que ele consegue interceptar — está no Galho 8, em [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies (o mecanismo)]].

## Em entrevista

### Frase pronta (inglês)

> In Spring, `@Transactional` only rolls back automatically on unchecked exceptions — that is, `RuntimeException` and `Error`. A checked exception does **not** trigger a rollback by default; the transaction commits as if nothing went wrong, which silently corrupts data if you're not aware of it. To make a checked exception roll back, I declare `rollbackFor` on the annotation, or I mark the current transaction with `setRollbackOnly()` programmatically. For propagation, `REQUIRED` is the default and reuses an active transaction, while `REQUIRES_NEW` suspends the outer one and runs an independent transaction — I use that for audit logging that must survive even when the business transaction rolls back.

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| propagação | propagation |
| nível de isolamento | isolation level |
| reversão | rollback |
| exceção verificada | checked exception |
| somente leitura | read-only |
| nova transação | new transaction |
| ponto de salvamento | savepoint |
| confirmar (a transação) | commit |
| fronteira da transação | transaction boundary |

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/03 - O persistence context e os estados da entidade|O persistence context e os estados da entidade]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/13 - Locking — optimistic (@Version) e pessimistic|Locking]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies (o mecanismo)]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/11 - JTA — transações na plataforma|JTA (a demarcação, na spec)]]
- [[03-Dominios/Ciência/Banco de dados|Banco de dados]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@Transactional (propagação)|@Transactional (propagação)]]

## Referências

- Spring Framework Reference — Declarative Transaction Management: https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative.html
- Spring Framework Reference — Using `@Transactional`: https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html
