---
title: "Locking — optimistic (@Version) e pessimistic"
created: 2026-06-09
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - persistencia
  - magus
  - locking
  - transacao
aliases:
  - "optimistic locking"
  - "pessimistic locking"
  - "@Version"
---

# Locking — optimistic (@Version) e pessimistic

> [!abstract] TL;DR
> Para evitar **lost update** em acesso concorrente: use **optimistic locking** (`@Version`) quando conflitos são raros — o banco detecta a colisão no commit e lança `OptimisticLockException` (a aplicação faz retry); use **pessimistic locking** (`SELECT ... FOR UPDATE`) quando conflitos são frequentes ou o custo de retry é alto — o banco serializa o acesso bloqueando a linha até o fim da transação.

---

## O que é

Locking é o conjunto de mecanismos que impedem que duas transações simultâneas sobrescrevam os dados uma da outra sem perceber.

O JPA/Hibernate oferece dois modelos:

| Modelo | Mecanismo | Quando detecta o conflito |
|---|---|---|
| **Optimistic** | Coluna `version` + `WHERE version = ?` no `UPDATE` | No momento do commit |
| **Pessimistic** | `SELECT ... FOR UPDATE` (lock de banco) | No momento da leitura |

---

## Por que importa

Sem locking, aplicações multi-usuário sofrem **lost update**: dois usuários leem o mesmo registro, cada um altera sua cópia em memória e o último a salvar sobrescreve silenciosamente as mudanças do primeiro. O resultado é inconsistência de dados sem nenhum erro visível.

Em entrevistas sêniores, a pergunta quase sempre é: "como você garante consistência sem travar o banco inteiro?" A resposta começa aqui.

---

## Como funciona

### Lost update: o problema que o locking resolve

Cenário clássico — dois atendentes ajustam o limite de crédito de um `Account` ao mesmo tempo:

```
T1: SELECT balance FROM account WHERE id = 1  → $100
T2: SELECT balance FROM account WHERE id = 1  → $100
T1: UPDATE account SET balance = $60 WHERE id = 1   (sacou $40)
T2: UPDATE account SET balance = $80 WHERE id = 1   (depositou $20)
-- Resultado final: $80. O saque de T1 sumiu.
```

Ambas as transações rodavam em `READ COMMITTED` (o padrão na maioria dos bancos), que não previne lost update por si só.

---

### Optimistic — `@Version`, `OptimisticLockException`, retry

**Ideia:** nunca bloqueia. Versiona a linha e deixa o banco rejeitar quem chegar atrasado.

#### Mapeamento

```java
@Entity
public class Account {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String owner;
    private BigDecimal balance;

    @Version
    private Long version;   // Hibernate gerencia; nunca altere manualmente

    // getters / setters / construtor
}
```

> [!info] Tipos suportados
> `int`, `Integer`, `long`, `Long`, `short`, `Short` e `java.sql.Timestamp`. O tipo `Long` é o mais usado por não sofrer overflow em sistemas de longa duração.

#### O que o Hibernate gera

A cada `UPDATE`, o Hibernate produz automaticamente:

```sql
UPDATE account
SET    balance = ?, version = 2
WHERE  id = 1
AND    version = 1   -- ← coluna de versão na condição
```

Se outro commit incrementou `version` para `2` antes deste chegar, `executeUpdate()` retorna **0 linhas afetadas** — e o Hibernate lança `jakarta.persistence.OptimisticLockException`.

#### Fluxo visual

```
T1: lê Account{id=1, version=1}
T2: lê Account{id=1, version=1}
T1: UPDATE ... WHERE version=1  → 1 linha afetada  ✓ version vira 2
T2: UPDATE ... WHERE version=1  → 0 linhas afetadas → OptimisticLockException ✗
```

O contexto de persistência de T2 é descartado. A aplicação precisa tratar o erro e fazer **retry** (recarregar a entidade e repetir a operação).

---

### Pessimistic — `@Lock(PESSIMISTIC_WRITE)`, `SELECT ... FOR UPDATE`, deadlock e ordem de aquisição

**Ideia:** bloqueia a linha no `SELECT`, garantindo que ninguém mais a modifique enquanto a transação estiver aberta.

#### SQL gerado

```sql
SELECT * FROM account WHERE id = 1 FOR UPDATE
```

Qualquer outra transação que tente `SELECT ... FOR UPDATE` na mesma linha fica **bloqueada** até que a primeira faça commit ou rollback.

> [!warning] Variações por banco
> PostgreSQL e MySQL geram `FOR UPDATE`. SQL Server gera `WITH (UPDLOCK, ROWLOCK)`. O Hibernate abstrai isso via `LockModeType`.

#### `LockModeType` — os modos principais

| Modo | SQL gerado | Uso |
|---|---|---|
| `PESSIMISTIC_READ` | `FOR SHARE` / `LOCK IN SHARE MODE` | Impede escrita, permite leitura concorrente |
| `PESSIMISTIC_WRITE` | `FOR UPDATE` | Impede escrita e leitura com lock |
| `PESSIMISTIC_FORCE_INCREMENT` | `FOR UPDATE` + incrementa `version` | Combina pessimistic + optimistic |

#### Deadlock e ordem de aquisição

Deadlock ocorre quando duas transações esperam uma pela outra:

```
T1: lock(account id=1) → espera lock(account id=2)
T2: lock(account id=2) → espera lock(account id=1)
```

**Regra de ouro:** sempre adquira locks na **mesma ordem** — por exemplo, em ordem crescente de `id`:

```java
// Correto: ambas as transações seguem a mesma ordem
Long smallerId = Math.min(idA, idB);
Long largerId  = Math.max(idA, idB);
accountRepo.findByIdForUpdate(smallerId);
accountRepo.findByIdForUpdate(largerId);
```

Sem essa disciplina, o banco detecta o deadlock e aborta uma das transações com `PessimisticLockException` (ou `DeadlockLoserDataAccessException` no Spring).

---

### Quando usar cada um

| Situação | Recomendação |
|---|---|
| Conflitos raros (maioria das operações web) | Optimistic (`@Version`) |
| Conflitos frequentes (filas, inventários disputados) | Pessimistic (`PESSIMISTIC_WRITE`) |
| Custo de retry muito alto (operação longa) | Pessimistic |
| Transação longa que atravessa múltiplas requests HTTP | Optimistic (evita manter lock aberto) |
| Leitura que **precisa** garantir que ninguém altere antes da sua escrita | Pessimistic |

---

## Na prática

### Entidade com `@Version`

```java
import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name = "account")
public class Account {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String owner;

    @Column(nullable = false)
    private BigDecimal balance;

    @Version
    private Long version;

    public Account() {}

    public Account(String owner, BigDecimal balance) {
        this.owner   = owner;
        this.balance = balance;
    }

    public void debit(BigDecimal amount) {
        if (balance.compareTo(amount) < 0) {
            throw new IllegalStateException("Saldo insuficiente");
        }
        this.balance = this.balance.subtract(amount);
    }

    // getters
}
```

### Repository com lock pessimista

```java
import jakarta.persistence.LockModeType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;

public interface AccountRepository extends JpaRepository<Account, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT a FROM Account a WHERE a.id = :id")
    java.util.Optional<Account> findByIdForUpdate(Long id);
}
```

### Service com retry para `OptimisticLockException`

```java
import jakarta.persistence.OptimisticLockException;
import org.springframework.orm.ObjectOptimisticLockingFailureException;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AccountService {

    private final AccountRepository repo;

    public AccountService(AccountRepository repo) {
        this.repo = repo;
    }

    /**
     * Tenta debitar com retry automático em caso de conflito optimistic.
     * Requer spring-retry no classpath e @EnableRetry na configuração.
     */
    @Retryable(
        retryFor  = { ObjectOptimisticLockingFailureException.class,
                      OptimisticLockException.class },
        maxAttempts = 3,
        backoff = @Backoff(delay = 100, multiplier = 2)
    )
    @Transactional
    public void debit(Long accountId, java.math.BigDecimal amount) {
        Account account = repo.findById(accountId)
            .orElseThrow(() -> new IllegalArgumentException("Account não encontrada"));
        account.debit(amount);
        // Hibernate detecta a mudança no flush; lança OptimisticLockException
        // se version não bater mais
    }

    /**
     * Versão manual (sem spring-retry): lida explicitamente com o conflito.
     */
    @Transactional
    public void debitPessimistic(Long accountId, java.math.BigDecimal amount) {
        Account account = repo.findByIdForUpdate(accountId)
            .orElseThrow(() -> new IllegalArgumentException("Account não encontrada"));
        account.debit(amount);
        // Sem risco de lost update: linha bloqueada desde o SELECT
    }
}
```

---

## Armadilhas

### (1) Esquecer `@Version` em entidade editável de forma concorrente

Sem `@Version`, o Hibernate gera `UPDATE ... WHERE id = ?` sem a coluna de versão. Lost updates acontecem silenciosamente — sem exceção, sem log, sem rastro. Toda entidade que pode ser alterada por múltiplos usuários ao mesmo tempo deve ter `@Version`.

### (2) Deadlock por ordem de aquisição inconsistente

Se dois fluxos de código travam as mesmas linhas em ordens diferentes, o banco detecta o ciclo de espera e aborta uma transação. A disciplina de sempre adquirir locks em ordem determinística (ex.: `id` crescente) é simples, mas precisa ser uma convenção explícita da equipe — o Hibernate não faz isso automaticamente.

### (3) Pessimistic onde optimistic bastaria

`SELECT ... FOR UPDATE` segura um lock de banco pela duração da transação. Em sistemas com muita concorrência, isso cria filas de espera, aumenta o tempo de resposta e pode gerar deadlocks. Usar pessimistic indiscriminadamente em operações onde conflitos são raros é a maneira mais fácil de matar a escalabilidade da aplicação sem motivo.

---

## Em entrevista

### Frase pronta (inglês)

> "Optimistic locking works by adding a `@Version` column to the entity. On every update, Hibernate appends `AND version = ?` to the `WHERE` clause; if zero rows are affected, it means someone else committed first and Hibernate throws `OptimisticLockException` — which we catch and retry. Pessimistic locking issues a `SELECT FOR UPDATE`, holding a database-level lock for the duration of the transaction, so no other writer can interfere. I reach for optimistic when conflicts are rare — typical for most web scenarios — and for pessimistic when contention is high or a retry would be too expensive. In both cases, consistent lock-acquisition order is essential to avoid deadlocks."

### Vocabulário

| Português | Inglês |
|---|---|
| Bloqueio otimista | Optimistic locking |
| Bloqueio pessimista | Pessimistic locking |
| Atualização perdida | Lost update |
| Versionamento de entidade | Entity versioning |
| Impasse | Deadlock |
| Contenção | Contention |
| Colisão de versão | Version conflict |
| Retentar operação | Retry |

---

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] ← conflito de escrita
- [[03-Dominios/Ciência/Banco de Dados/index|Banco de dados]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@Version (optimistic locking)|@Version (optimistic locking)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#pessimistic locking|pessimistic locking]]

---

## Referências

- Hibernate ORM User Guide — Locking: <https://docs.hibernate.org/orm/current/userguide/html_single/Hibernate_User_Guide.html>
- Vlad Mihalcea — "Optimistic vs. Pessimistic Locking": <https://vladmihalcea.com/optimistic-vs-pessimistic-locking/>
- Vlad Mihalcea — "A Beginner's Guide to Database Locking and the Lost Update Phenomena": <https://vladmihalcea.com/a-beginners-guide-to-database-locking-and-the-lost-update-phenomena/>
- Jakarta Persistence 3.2 Specification — Section 3.4 (Locking and Concurrency): <https://jakarta.ee/specifications/persistence/3.2/>
