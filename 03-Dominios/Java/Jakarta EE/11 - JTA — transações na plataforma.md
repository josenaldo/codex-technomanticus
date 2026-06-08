---
title: "JTA — transações na plataforma"
created: 2026-06-07
updated: 2026-06-07
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - jakarta-ee
  - magus
  - jta
aliases:
  - "JTA"
  - "Jakarta Transactions"
  - "@Transactional Jakarta"
---

# JTA — transações na plataforma

> [!abstract] TL;DR
> **JTA (Jakarta Transactions, 2.0 no EE 11)** é a especificação que coordena transações na plataforma — o contrato de *demarcação* (onde a transação começa e termina) e *coordenação* (garantir atomicidade). Você demarca de dois jeitos: **declarativo** (`@Transactional` + `Transactional.TxType`, implementado como um **interceptor CDI**) ou **programático** (`UserTransaction`: `begin`/`commit`/`rollback`). A regra de rollback do `@Transactional` é o ponto que todo mundo erra: por padrão **`RuntimeException` e subclasses fazem rollback; checked exceptions NÃO** — e `rollbackOn`/`dontRollbackOn` ajustam isso. Quando há **dois recursos** (banco + fila, dois bancos) entra **XA / two-phase commit**, com seu custo de latência e bloqueio. Aviso de fronteira: o `@Transactional` do **Spring** é *outra* annotation, homônima, pro mesmo problema — assunto dos Galhos 8/10 (planejados); aqui só desambiguamos.

---

## O que é

Transação é a velha promessa do **ACID** num verbo: ou **tudo** acontece, ou **nada** acontece. Debitar de uma conta e creditar em outra; baixar estoque e gravar o pedido; persistir uma entidade e publicar um evento. Se o segundo passo falha, o primeiro não pode "ficar de pé". Esse é o problema que a transação resolve, e **JTA é a especificação que define como a plataforma Jakarta EE coordena isso**.

JTA não persiste nada por conta própria — ela não é JDBC nem [[09 - JPA — a especificação de persistência|JPA]]. JTA é o **contrato de demarcação e coordenação**: define *quem* abre uma transação, *quem* a confirma ou desfaz, *como* múltiplos recursos transacionais se alistam (*enlist*) sob a mesma transação, e *como* o container amarra tudo isso de forma declarativa. A versão cravada para esta trilha é **Jakarta Transactions 2.0**, parte do **Jakarta EE 11** (a renomeação `javax.transaction` → `jakarta.transaction` veio na migração coberta em [[02 - De Java EE a Jakarta EE]]).

> [!warning] Desambiguação imediata: dois `@Transactional` homônimos
> Existe `jakarta.transaction.Transactional` (esta nota) e existe um `@Transactional` do **Spring** (`org.springframework.transaction.annotation.Transactional`). São **annotations diferentes, de specs/frameworks diferentes**, que resolvem o **mesmo problema** com semânticas parecidas mas **não idênticas** (a regra de rollback default, inclusive, difere entre as duas). Esta nota é **exclusivamente** sobre a annotation do Jakarta. O `@Transactional` do Spring é assunto dos **Galhos 8/10 (planejado)** — aqui não explicamos como o Spring implementa. Sempre que ler `@Transactional` daqui pra frente, leia "o do `jakarta.transaction`".

---

## Por que importa

Transação é onde **bug vira prejuízo**. Um `NullPointerException` numa tela de relatório é chato; o mesmo `NullPointerException` no meio de uma transferência bancária, com o débito já feito e o crédito ainda não, é **dinheiro evaporando**. Por isso o comportamento de rollback não é detalhe: é a diferença entre um sistema correto e um sistema que perde dados silenciosamente sob carga.

Há três razões para um sênior dominar JTA mesmo trabalhando com frameworks que "escondem" tudo isso:

1. **O modelo CMT/BMT explica o que TODO framework declarativo faz por baixo.** Container-Managed Transactions (declarativo, `@Transactional`) versus Bean-Managed Transactions (programático, `UserTransaction`) são as duas únicas formas de demarcar. Quando você entende o interceptor que abre/fecha a transação ao redor do seu método, entende por que `@Transactional` do Spring, `@Transactional` do Jakarta e até o `@Transactional` de outros frameworks têm as mesmas armadilhas — porque todos são **interceptação ao redor da chamada**.

2. **A regra de rollback é a fonte nº 1 de bugs de consistência.** "Lancei uma exceção, por que a transação não desfez?" é uma pergunta diária. A resposta — checked não faz rollback por padrão — está na spec, não na intuição.

3. **XA / 2PC é pergunta clássica de system design.** "Como você garante consistência entre o banco e a fila de mensagens?" testa se você sabe que two-phase commit *existe*, *funciona*, e *custa caro* — e que muitas vezes a resposta sênior é **evitar** 2PC com padrões como outbox (ver a seção sobre XA e two-phase commit, adiante; mensageria é assunto do Galho 14 planejado).

---

## Como funciona

### O problema: atomicidade entre operações, e quem coordena

Imagine um método que faz duas escritas: grava um `Order` e baixa o estoque de um `Product`. Sem transação, cada `INSERT`/`UPDATE` é confirmado isoladamente — se a segunda escrita estoura, a primeira **já foi**. Você precisa de uma fronteira que diga "essas operações são um bloco; confirme as duas juntas ou nenhuma".

Quem desenha e impõe essa fronteira é o **container** (o servidor de aplicação Jakarta EE). Ele oferece um **`TransactionManager`** (interface interna, `jakarta.transaction.TransactionManager`) que orquestra o ciclo de vida da transação e a representa internamente como um objeto **`Transaction`** (`jakarta.transaction.Transaction`). Você, na maioria dos casos, **não toca** nessas interfaces de baixo nível — elas são para frameworks e para o container. O desenvolvedor de aplicação interage por dois caminhos: o **declarativo** (`@Transactional`, CMT) ou o **programático** (`UserTransaction`, BMT). Existe ainda a **`TransactionSynchronizationRegistry`** (`jakarta.transaction.TransactionSynchronizationRegistry`), usada para registrar *callbacks* (`Synchronization`) que rodam antes/depois do commit — útil para frameworks que precisam de um gancho no `beforeCompletion`/`afterCompletion`, mas raramente usada direto em código de aplicação.

> [!note] Dois recursos, um coordinator
> Quando a transação envolve **um único recurso** (só o banco, via JPA), o commit é simples: um `COMMIT` SQL. Quando envolve **dois ou mais recursos** (banco + fila, dois bancos), o container vira **coordinator** de um protocolo distribuído — o two-phase commit, detalhado adiante.

### Programático — BMT (`UserTransaction`)

No modelo **Bean-Managed Transactions (BMT)**, *você* demarca a transação na mão, via a interface **`UserTransaction`** (`jakarta.transaction.UserTransaction`). Os métodos centrais, conforme o Javadoc da spec:

- **`begin()`** — "cria uma nova transação e a associa à thread atual";
- **`commit()`** — "completa a transação associada à thread atual";
- **`rollback()`** — "desfaz a transação associada à thread atual";
- **`setRollbackOnly()`** — marca a transação para que seu único desfecho possível seja rollback;
- **`getStatus()`** — obtém o status da transação corrente;
- **`setTransactionTimeout(int seconds)`** — ajusta o timeout das transações iniciadas pela thread.

O controle manual **vale a pena** quando a fronteira da transação não bate com a fronteira do método: você quer confirmar uma parte do trabalho cedo, ou abrir e fechar várias transações curtas dentro de um único método (um *batch*, por exemplo), ou tomar a decisão de commit/rollback com base em lógica que não cabe na regra de exceção. O preço é que **você é responsável** por chamar `commit`/`rollback` em todos os caminhos — inclusive nos de erro. Esquecer um `rollback` num `catch` deixa a transação pendurada.

### Declarativo — CMT (`@Transactional` + `TxType`)

No modelo **Container-Managed Transactions (CMT)**, você **não** chama `begin`/`commit`. Você **anota** o método (ou a classe) com `@Transactional` e o container demarca por você. A annotation `jakarta.transaction.Transactional` é implementada como um **interceptor CDI**: o container coloca um *proxy* entre o chamador e o seu bean, e esse interceptor abre a transação antes do método, decide commit ou rollback depois, e — crucialmente — só roda **quando a chamada atravessa o proxy** (guarde isto; volta nas Armadilhas). O mecanismo de interceptação é o mesmo de [[13 - CDI avançado — interceptors, decorators e extensões]].

O elemento `value` da annotation é um **`Transactional.TxType`**, que controla a relação do método com a transação corrente. Os seis valores, conforme a spec (comportamento *fora* / *dentro* de uma transação ativa):

| `TxType` | Sem transação ativa | Com transação ativa |
|---|---|---|
| `REQUIRED` *(default)* | abre uma nova e a completa | junta-se à transação corrente |
| `REQUIRES_NEW` | abre uma nova e a completa | **suspende** a corrente, abre uma nova, completa, e **retoma** a suspensa |
| `MANDATORY` | lança `TransactionalException` (com `TransactionRequiredException`) | executa na transação corrente |
| `SUPPORTS` | executa **sem** transação | executa na transação corrente |
| `NOT_SUPPORTED` | executa sem transação | **suspende** a corrente, executa sem transação, e **retoma** a suspensa |
| `NEVER` | executa sem transação | lança `TransactionalException` (com `InvalidTransactionException`) |

`REQUIRED` é o default e cobre a grande maioria dos casos: "quero estar numa transação; reaproveite uma se existir, senão crie". `REQUIRES_NEW` é o que você usa quando um trecho precisa **sobreviver ao rollback** do chamador (auditoria, log persistente). `MANDATORY`/`NEVER` são guardas de contrato ("este método *exige*/*proíbe* transação ambiente"). `SUPPORTS`/`NOT_SUPPORTED` são casos de borda (operações de leitura ou trabalho que não pode estar numa transação, como certas chamadas externas).

### Rollback — a regra exata da spec

Aqui está o ponto que mais cai em entrevista e mais quebra em produção. O Javadoc do `@Transactional` é literal:

> [!quote] Regra de rollback (Javadoc de `jakarta.transaction.Transactional`)
> *"By default checked exceptions do not result in the transactional interceptor marking the transaction for rollback and instances of `RuntimeException` and its subclasses do."*

Traduzindo o contrato exato:

- **`RuntimeException` e suas subclasses → rollback automático** (unchecked). `Error` também marca rollback.
- **Checked exceptions → NÃO fazem rollback por padrão.** Se você lança uma `IOException` ou uma exceção de negócio checked, a transação **comita** mesmo assim, a menos que você diga o contrário.

Para customizar, a annotation tem dois elementos:

- **`rollbackOn`** — *"can be set to indicate exceptions that must cause the interceptor to mark the transaction for rollback"* (force rollback também em certas checked);
- **`dontRollbackOn`** — *"can be set to indicate exceptions that must not cause the interceptor to mark the transaction for rollback"* (impede rollback de certas unchecked).
- Se ambos listarem a mesma exceção, *"`dontRollbackOn` takes precedence"*.

Exemplo: `@Transactional(rollbackOn = OrderRejectedException.class)` faz uma exceção checked de negócio desfazer a transação.

Além disso, dentro de uma transação você pode marcá-la para rollback **sem lançar exceção**, via `setRollbackOnly()` (em `UserTransaction` ou na `TransactionSynchronizationRegistry`). A partir daí, qualquer tentativa de commit vira rollback — útil quando você detecta uma condição inválida mas quer continuar executando para, digamos, registrar diagnóstico antes de devolver o controle.

### `@TransactionScoped` — um bean vivo durante a transação

A spec define o escopo CDI **`@TransactionScoped`** (`jakarta.transaction.TransactionScoped`). Um bean nesse escopo nasce quando a transação corrente começa e morre quando ela termina — **uma instância por transação ativa**. É o "primo transacional" dos escopos vistos em [[05 - CDI — escopos e contextos]] (`@RequestScoped`, `@SessionScoped` etc.): o contexto que o delimita é a *transação*, não a requisição ou a sessão. Serve para acumular estado que faz sentido apenas dentro de uma transação (um agregador de eventos a publicar no commit, por exemplo). Acessar um bean `@TransactionScoped` **fora** de uma transação ativa lança `ContextNotActiveException`.

### XA e two-phase commit

Tudo acima assume **um recurso** (o banco). E quando a transação precisa abranger **dois**? Gravar o `Order` no banco **e** publicar uma mensagem numa fila, atomicamente — ou os dois acontecem, ou nenhum. Aí entra o **X/Open XA**: a JTA integra com o padrão industrial X/Open Distributed Transaction Processing através da interface **`XAResource`** (descrita na spec como *"a Java mapping of the industry standard XA interface based on the X/Open CAE Specification"*). Cada recurso transacional (datasource XA, broker XA) expõe um `XAResource` que se alista (*enlist*) na transação corrente.

Com dois `XAResource` alistados, o commit vira o **two-phase commit (2PC)**, com o `TransactionManager` no papel de **coordinator**:

```text
Fase 1 — PREPARE
  coordinator → recurso A: prepare?   A → "ready" (votou commit, já durável)
  coordinator → recurso B: prepare?   B → "ready"
Fase 2 — COMMIT
  coordinator → recurso A: commit     A → ok
  coordinator → recurso B: commit     B → ok
(se QUALQUER recurso votar "no" na fase 1 → coordinator manda ROLLBACK a todos)
```

A garantia é forte: na fase 1, cada recurso *promete* que consegue commitar (e durabiliza essa promessa); só na fase 2 todos confirmam. Se um vota "não", todos desfazem.

> [!caution] O custo do 2PC é real
> Two-phase commit paga em **latência** (dois round-trips por recurso) e, pior, em **bloqueio**: entre o prepare e o commit, os recursos seguram locks e ficam num estado *in-doubt*. Se o coordinator cai nessa janela, os recursos ficam pendurados esperando a decisão — daí a complexidade do *recovery* e do log do coordinator. Por isso, em system design, a resposta sênior frequentemente é **evitar 2PC**: usar um único recurso quando possível, ou padrões de consistência eventual como **outbox** / sagas para o caso banco-mais-mensageria. O detalhamento de mensageria e desses padrões é assunto do **Galho 14 (planejado)**; aqui basta saber que 2PC existe, é correto, é caro, e tem alternativas.

---

## Na prática

Um serviço CMT que orquestra duas escritas, com auditoria que sobrevive a rollback, mais um exemplo de BMT completo:

```java
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;

@ApplicationScoped
public class OrderService {

    @Inject EntityManager em;
    @Inject AuditService auditService;

    // TxType.REQUIRED é o default — explícito aqui só para deixar claro.
    @Transactional(Transactional.TxType.REQUIRED)
    public void placeOrder(Order order, Customer customer) {
        em.persist(order);                 // escrita 1, dentro da transação
        debitStock(order);                 // escrita 2, MESMA transação

        // Auditoria via referência INJETADA → passa pelo interceptor.
        auditService.record("ORDER_PLACED", customer.getId());

        // Se algo abaixo lançar RuntimeException, persist + debitStock
        // são desfeitos juntos (rollback automático em unchecked).
    }

    // ARMADILHA evitada: este método é chamado por placeOrder() via
    // referência ao bean (this), então o interceptor de placeOrder já
    // está ativo. NÃO é uma self-invocation problemática porque NÃO
    // tem @Transactional próprio — apenas participa da transação corrente.
    private void debitStock(Order order) {
        Product p = em.find(Product.class, order.getProductId());
        p.setStock(p.getStock() - order.getQuantity());
    }
}

@ApplicationScoped
class AuditService {

    @Inject EntityManager em;

    // Auditoria precisa SOBREVIVER a um rollback do chamador:
    // transação independente, comitada à parte.
    @Transactional(Transactional.TxType.REQUIRES_NEW)
    public void record(String action, Long customerId) {
        AuditLog log = new AuditLog(action, customerId);
        em.persist(log);   // comita mesmo que placeOrder() faça rollback depois
    }
}
```

Forçando rollback de uma exceção de negócio **checked** (que por padrão NÃO desfaria):

```java
import jakarta.transaction.Transactional;

@Transactional(rollbackOn = OrderRejectedException.class)
public void confirm(Order order) throws OrderRejectedException {
    if (!order.isValid()) {
        // checked → por padrão comitaria; rollbackOn força o rollback.
        throw new OrderRejectedException(order.getId());
    }
    order.setStatus(Status.CONFIRMED);
}
```

BMT — controle manual com `UserTransaction`, try/catch completo:

```java
import jakarta.annotation.Resource;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.inject.Inject;
import jakarta.transaction.UserTransaction;
import jakarta.transaction.Status;

@ApplicationScoped
public class BatchImporter {

    @Resource UserTransaction utx;   // injetado pelo container
    @Inject EntityManager em;

    public void importBatch(java.util.List<Order> orders) {
        try {
            utx.begin();                       // demarcação manual
            for (Order o : orders) {
                em.persist(o);
            }
            utx.commit();                      // confirma tudo de uma vez
        } catch (Exception e) {
            try {
                // só faz rollback se ainda houver transação ativa
                if (utx.getStatus() != Status.STATUS_NO_TRANSACTION) {
                    utx.rollback();            // VOCÊ é responsável pelo desfecho
                }
            } catch (Exception rollbackEx) {
                // logar; rollback que falha é situação grave (in-doubt)
            }
            throw new RuntimeException("Falha no import de pedidos", e);
        }
    }
}
```

Self-invocation que **NÃO** passa pelo interceptor (o bug clássico):

```java
@ApplicationScoped
public class ReportService {

    @Transactional
    public void generateAll() {
        // Chamada via 'this' → NÃO atravessa o proxy CDI.
        // O @Transactional de generateOne() é IGNORADO:
        // generateOne() roda na transação de generateAll(), não na sua.
        for (Long id : ids()) {
            generateOne(id);          // <-- interceptor de generateOne NÃO roda
        }
    }

    @Transactional(Transactional.TxType.REQUIRES_NEW)
    public void generateOne(Long id) {
        // Esperava ser uma transação nova por item; não é, quando
        // chamado internamente. Ver Armadilha (1).
    }
}
```

---

## Armadilhas

### (1) Self-invocation de método `@Transactional`

O `@Transactional` é um **interceptor CDI**, e interceptors só rodam quando a chamada **atravessa o proxy**. Uma chamada de um método do bean para **outro método do mesmo bean** (`this.outroMetodo()`) não passa pelo proxy — vai direto ao objeto real. Resultado: o `@Transactional` (ou o `REQUIRES_NEW`) do método interno é **silenciosamente ignorado**.

```java
@Transactional
public void a() {
    b();   // self-invocation: o @Transactional(REQUIRES_NEW) de b() NÃO roda
}
@Transactional(Transactional.TxType.REQUIRES_NEW)
public void b() { /* ... */ }
```

**Fix:** chame `b()` através de uma **referência injetada** (injete o próprio bean, ou mova `b()` para outro bean injetado) — assim a chamada atravessa o proxy. Ou **repense o desenho**: se dois métodos precisam de transações diferentes, provavelmente são responsabilidades diferentes, em beans diferentes. Mesma raiz do problema visto em [[05 - CDI — escopos e contextos]] e [[13 - CDI avançado — interceptors, decorators e extensões]].

### (2) Assumir rollback automático em checked exception

Por padrão da spec, **checked exceptions NÃO disparam rollback**. Lançar uma exceção de negócio checked do meio de um método transacional deixa a transação **comitar** com o trabalho parcial dentro.

```java
@Transactional
public void transfer(Account a, Account b, long amount) throws InsufficientFundsException {
    a.debit(amount);                       // já aplicado
    if (b.isFrozen())
        throw new InsufficientFundsException();   // checked → COMITA mesmo assim!
    b.credit(amount);
}
```

**Fix:** declare `rollbackOn` explicitamente — `@Transactional(rollbackOn = InsufficientFundsException.class)` — ou faça a exceção de negócio ser unchecked (`extends RuntimeException`) se a semântica for sempre "abortar".

### (3) Misturar BMT e CMT no mesmo componente

Usar `UserTransaction` (BMT) e `@Transactional` (CMT) **no mesmo bean** gera comportamento confuso: o container não sabe se você quer demarcar na mão ou se ele deve fazê-lo, e as duas demarcações brigam pela mesma transação na thread.

```java
@Transactional                       // container demarca...
public void confuso() {
    utx.begin();                     // ...e você também? Comportamento indefinido.
}
```

**Fix:** **um modelo de demarcação por componente**. Decida: ou o bean é CMT (só `@Transactional`, sem tocar em `UserTransaction`), ou é BMT (só `UserTransaction`, sem `@Transactional`). Nunca os dois juntos.

### (4) `REQUIRES_NEW` em cascata sem perceber

`REQUIRES_NEW` suspende a transação corrente e abre **uma independente**. Encadear vários `REQUIRES_NEW` (A chama B chama C, todos `REQUIRES_NEW`, todos atravessando proxies de fato) cria transações aninhadas **que comitam separadamente** — e um rollback lá no fundo pode deixar **commits parciais** de cima já confirmados, surpreendendo quem esperava atomicidade do conjunto.

```java
@Transactional(Transactional.TxType.REQUIRES_NEW)  // tx independente 1
void outer() { inner(); /* via referência injetada */ }

@Transactional(Transactional.TxType.REQUIRES_NEW)  // tx independente 2
void inner() { /* comita à parte; rollback aqui NÃO desfaz outer */ }
```

**Fix:** **mapeie os limites transacionais conscientemente.** Use `REQUIRES_NEW` apenas onde a independência é *intencional* (auditoria, log que deve sobreviver). Se o conjunto precisa ser atômico, use `REQUIRED` para que tudo compartilhe a mesma transação.

---

## Em entrevista

### Frase pronta (inglês)

> "Jakarta Transactions — JTA 2.0 — is the platform's transaction demarcation and coordination contract. You demarcate either declaratively, with the `@Transactional` annotation implemented as a CDI interceptor, or programmatically through `UserTransaction` with explicit `begin`, `commit`, and `rollback`. The detail that trips most people up is the rollback rule: by default, unchecked exceptions — `RuntimeException` and its subclasses — mark the transaction for rollback, while checked exceptions do not, and you tune that with `rollbackOn` and `dontRollbackOn`. When a unit of work spans more than one resource, JTA integrates with X/Open XA to run a two-phase commit, where the transaction manager acts as coordinator across prepare and commit phases — correct, but costly in latency and locking, which is why senior designs often avoid it in favor of single-resource or eventual-consistency patterns."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Demarcação de transação | Transaction demarcation |
| Transação gerenciada pelo container (CMT) | Container-managed transaction |
| Transação gerenciada pelo bean (BMT) | Bean-managed transaction |
| Desfazer / reverter | Roll back / rollback |
| Confirmar / efetivar | Commit |
| Marcar para rollback | Mark for rollback |
| Exceção verificada / não-verificada | Checked / unchecked exception |
| Commit em duas fases | Two-phase commit (2PC) |
| Alistar recurso | Enlist a resource |
| Coordenador de transação | Transaction coordinator |
| Transação suspensa | Suspended transaction |

---

## Veja também

- [[05 - CDI — escopos e contextos]]
- [[10 - EntityManager e o ciclo de vida da entidade]]
- [[13 - CDI avançado — interceptors, decorators e extensões]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência (Galho 4)]]
- [[03-Dominios/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#JTA (Jakarta Transactions)|JTA (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#@Transactional (Jakarta)|@Transactional (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#CMT / BMT|CMT / BMT (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#two-phase commit (2PC / XA)|two-phase commit (Dicionário)]]

---

## Referências

- [Jakarta Transactions 2.0 — Specification Page](https://jakarta.ee/specifications/transactions/2.0/) — acesso 2026-06-07
- [Jakarta Transactions 2.0 — Specification Document (HTML)](https://jakarta.ee/specifications/transactions/2.0/jakarta-transactions-spec-2.0.html) — acesso 2026-06-07
- [Jakarta Transactions 2.0 — `@Transactional` Javadoc (`jakarta.transaction`)](https://jakarta.ee/specifications/transactions/2.0/apidocs/jakarta/transaction/Transactional.html) — acesso 2026-06-07
- [Jakarta Transactions 2.0 — `Transactional.TxType` Javadoc](https://jakarta.ee/specifications/transactions/2.0/apidocs/jakarta/transaction/Transactional.TxType.html) — acesso 2026-06-07
- [Jakarta Transactions 2.0 — `UserTransaction` Javadoc](https://jakarta.ee/specifications/transactions/2.0/apidocs/jakarta/transaction/UserTransaction.html) — acesso 2026-06-07
- [Jakarta EE Specifications Index](https://jakarta.ee/specifications/) — acesso 2026-06-07
