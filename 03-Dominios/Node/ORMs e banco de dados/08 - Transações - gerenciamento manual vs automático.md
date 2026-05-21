---
title: "Transações - gerenciamento manual vs automático"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - orm
  - transações
  - banco-de-dados
aliases:
  - Transações Node
  - Gerenciamento de transações ORM
---

# Transações - gerenciamento manual vs automático

> [!abstract] TL;DR
> Uma transação agrupa operações de banco em uma unidade **ACID** — tudo persiste ou nada persiste. Em Node, cada ORM expõe dois modos: **gerenciado** (callback com commit/rollback automático) e **manual** (controle explícito). **Prisma** usa `prisma.$transaction([...])` para batches sem dependência ou `prisma.$transaction(async (tx) => {...})` para lógica interativa. **TypeORM** usa `dataSource.transaction(async (manager) => {...})` ou `QueryRunner` manual, que exige `release()` no `finally`. **Sequelize** usa `sequelize.transaction(async (t) => {...})` e requer `{ transaction: t }` em cada operação. **Drizzle** usa `db.transaction(async (tx) => {...})` — todas as queries dentro devem usar `tx`, nunca `db`. Confira [[03-Dominios/Node/ORMs e banco de dados/index]] para o panorama completo do Galho 6.

## Como funciona

### O que é uma transação

Uma **transação de banco de dados** é um conjunto de operações tratado como unidade indivisível: ou todas as operações são concluídas e persistidas, ou nenhuma produz efeito. O banco garante essa semântica pelo ciclo **BEGIN → operações → COMMIT** (ou **ROLLBACK** em caso de erro).

O acrônimo **ACID** descreve as quatro propriedades que tornam transações confiáveis:

| Propriedade | Definição |
| --- | --- |
| **Atomicity** | Tudo ou nada — se qualquer operação falha, todas as mudanças são revertidas |
| **Consistency** | Transição de um estado válido para outro, respeitando constraints e regras do schema |
| **Isolation** | Transações concorrentes não interferem umas nas outras |
| **Durability** | Após COMMIT, as mudanças persistem mesmo em caso de crash imediato do servidor |

O ciclo de vida em SQL serve de referência para o que os ORMs abstraem:

```sql
-- Ciclo básico de uma transação em PostgreSQL
BEGIN;

INSERT INTO transactions (from_account_id, to_account_id, amount)
VALUES (1, 2, 500.00);

UPDATE accounts SET balance = balance - 500.00 WHERE id = 1;
UPDATE accounts SET balance = balance + 500.00 WHERE id = 2;

-- Se qualquer operação falhar → ROLLBACK desfaz tudo desde o BEGIN
COMMIT;
```

**Quando transações são necessárias:**

- Múltiplas tabelas com dependência lógica (transferência financeira: débito + crédito + registro)
- Criação de entidades compostas (pedido + itens + reserva de estoque)
- Fluxos onde falha parcial deixaria dados inconsistentes

**Custo de transações:** transações adquirem locks nas linhas modificadas e os mantêm até COMMIT ou ROLLBACK. Transações longas bloqueiam outras transações concorrentes nas mesmas linhas e aumentam o risco de deadlock. Regra prática: transações devem ser curtas — apenas as operações necessárias, sem chamadas HTTP ou I/O externo enquanto os locks estão abertos.

**Níveis de isolamento:**

| Nível | Dirty Read | Non-Repeatable Read | Phantom Read |
| --- | --- | --- | --- |
| Read Uncommitted | possível | possível | possível |
| **Read Committed** (padrão PostgreSQL) | impossível | possível | possível |
| Repeatable Read | impossível | impossível | possível |
| Serializable | impossível | impossível | impossível |

- **Dirty read:** ler dados de uma transação que ainda não fez COMMIT — se ela fizer ROLLBACK, você leu dados que nunca existiram permanentemente
- **Non-repeatable read:** ler a mesma linha duas vezes na mesma transação e obter resultados diferentes porque outra transação fez COMMIT entre as leituras
- **Phantom read:** executar a mesma query de lista duas vezes e obter linhas diferentes porque outra transação inseriu ou removeu registros

### Transações em Prisma

O Prisma oferece dois modos via `$transaction`: **batch sequencial** (array de `PrismaPromise`) e **interativo** (callback com cliente isolado `tx`).

```typescript
// transactions/prisma-batch.ts
import { prisma } from '../prisma';

// Modo BATCH — array de PrismaPromise sem dependências entre operações
// Mais rápido: todas as queries enviadas na mesma round-trip ao banco
// Não usar quando o resultado de uma operação alimenta a próxima
export async function criarUsuarioComPerfil(
  nome: string,
  email: string,
  bio: string,
): Promise<void> {
  await prisma.$transaction([
    prisma.user.create({ data: { name: nome, email } }),
    prisma.profile.create({ data: { bio, userEmail: email } }),
  ]);
  // Se qualquer operação falhar → rollback de ambas
}
```

```typescript
// transactions/prisma-interativa.ts
import { Prisma } from '@prisma/client';
import { prisma } from '../prisma';

// Modo INTERATIVO — callback com tx (Prisma Client isolado para a transação)
// Use quando o resultado de uma operação alimenta a próxima
// NUNCA use prisma.model dentro do callback — use apenas tx
export async function transferirCreditos(
  fromUserId: number,
  toUserId: number,
  quantidade: number,
): Promise<void> {
  await prisma.$transaction(
    async (tx) => {
      const usuarioOrigem = await tx.user.findUniqueOrThrow({
        where: { id: fromUserId },
        select: { id: true, credits: true },
      });

      if (usuarioOrigem.credits < quantidade) {
        throw new Error('Créditos insuficientes'); // → rollback automático
      }

      await tx.user.update({
        where: { id: fromUserId },
        data: { credits: { decrement: quantidade } },
      });

      await tx.user.update({
        where: { id: toUserId },
        data: { credits: { increment: quantidade } },
      });

      await tx.creditTransfer.create({
        data: { fromUserId, toUserId, amount: quantidade },
      });
    },
    {
      maxWait: 5_000,   // ms para aguardar conexão disponível no pool (padrão: 2000ms)
      timeout: 15_000,  // ms máximo para a transação inteira durar (padrão: 5000ms)
      isolationLevel: Prisma.TransactionIsolationLevel.RepeatableRead,
    },
  );
}
```

> [!tip] Batch vs interativa no Prisma
> Use **batch** quando as operações são independentes entre si. Use **interativa** quando precisar ler dados antes de decidir o que escrever (verificar saldo antes de debitar, verificar estoque antes de reservar). O batch é mais performático — envia todas as queries numa única round-trip; a interativa mantém uma conexão aberta durante todo o callback.

### Transações em TypeORM

O TypeORM oferece dois modos: **`dataSource.transaction()`** (gerenciado, commit/rollback automático) e **`QueryRunner`** (manual, com controle explícito do ciclo de vida).

```typescript
// transactions/typeorm-gerenciado.ts
import { DataSource } from 'typeorm';
import { Account } from '../entities/account.entity';
import { TransactionRecord } from '../entities/transaction-record.entity';

// Modo GERENCIADO — manager é um EntityManager isolado para a transação
// NÃO use repositories injetados — eles usam conexão diferente e ficam fora da transação
export async function transferirSaldo(
  dataSource: DataSource,
  fromAccountId: string,
  toAccountId: string,
  valor: number,
): Promise<void> {
  await dataSource.transaction(async (manager) => {
    const contaOrigem = await manager.findOne(Account, {
      where: { id: fromAccountId },
      lock: { mode: 'pessimistic_write' }, // SELECT FOR UPDATE
    });
    const contaDestino = await manager.findOne(Account, {
      where: { id: toAccountId },
    });

    if (!contaOrigem || !contaDestino) throw new Error('Conta não encontrada');
    if (contaOrigem.balance < valor) throw new Error('Saldo insuficiente');

    contaOrigem.balance -= valor;
    contaDestino.balance += valor;

    await manager.save(contaOrigem);
    await manager.save(contaDestino);
    await manager.save(TransactionRecord, {
      fromAccountId,
      toAccountId,
      amount: valor,
      executedAt: new Date(),
    });
    // Saiu sem erro → commit automático
  });
}
```

```typescript
// transactions/typeorm-query-runner.ts
import { DataSource, QueryRunner } from 'typeorm';
import { Order } from '../entities/order.entity';
import { Stock } from '../entities/stock.entity';

// Modo MANUAL com QueryRunner — controle granular do ciclo de vida
// OBRIGATÓRIO: queryRunner.release() no finally para devolver conexão ao pool
export async function criarPedidoComBaixaDeEstoque(
  dataSource: DataSource,
  produtoId: string,
  usuarioId: string,
  quantidade: number,
): Promise<Order> {
  const queryRunner: QueryRunner = dataSource.createQueryRunner();
  await queryRunner.connect();
  await queryRunner.startTransaction(); // BEGIN

  try {
    const estoque = await queryRunner.manager.findOne(Stock, {
      where: { productId: produtoId },
      lock: { mode: 'pessimistic_write' },
    });

    if (!estoque || estoque.quantity < quantidade) {
      throw new Error('Estoque insuficiente');
    }

    estoque.quantity -= quantidade;
    await queryRunner.manager.save(estoque);

    const pedido = queryRunner.manager.create(Order, {
      userId: usuarioId,
      productId: produtoId,
      quantity: quantidade,
    });
    const pedidoSalvo = await queryRunner.manager.save(pedido);

    await queryRunner.commitTransaction(); // COMMIT
    return pedidoSalvo;
  } catch (error) {
    await queryRunner.rollbackTransaction(); // ROLLBACK
    throw error;
  } finally {
    // SEMPRE no finally: libera a conexão de volta ao pool
    // Omitir esgota o pool silenciosamente sob carga
    await queryRunner.release();
  }
}
```

> [!warning] QueryRunner: `release()` obrigatório no `finally`
> O `QueryRunner` mantém uma conexão dedicada do pool. Se `release()` estiver apenas no `try` — e não no `finally` — a conexão vaza toda vez que há erro. Com volume de requisições, o pool se esgota e todas as novas requisições ficam travadas com `ConnectionTimeoutError`.

### Transações em Sequelize

O Sequelize oferece modo **gerenciado** (callback com commit/rollback automático) e **não gerenciado** (commit e rollback explícitos). Em ambos os modos, `{ transaction: t }` deve ser passado a cada operação individualmente.

```typescript
// transactions/sequelize-gerenciada.ts
import { Transaction } from 'sequelize';
import { sequelize } from '../database';
import { Account } from '../models/account';
import { TransferRecord } from '../models/transfer-record';

// Modo GERENCIADO — commit/rollback automático baseado no resultado do callback
// { transaction: t } em TODAS as operações — omitir faz a operação sair da transação
export async function transferirFundos(
  fromAccountId: number,
  toAccountId: number,
  valor: number,
): Promise<void> {
  await sequelize.transaction(async (t: Transaction) => {
    const contaOrigem = await Account.findOne({
      where: { id: fromAccountId },
      transaction: t,
      lock: Transaction.LOCK.UPDATE, // SELECT FOR UPDATE
    });
    const contaDestino = await Account.findOne({
      where: { id: toAccountId },
      transaction: t,
    });

    if (!contaOrigem || !contaDestino) {
      throw new Error('Conta não encontrada'); // → rollback automático
    }
    if (contaOrigem.dataValues.balance < valor) {
      throw new Error('Saldo insuficiente'); // → rollback automático
    }

    await contaOrigem.decrement('balance', { by: valor, transaction: t });
    await contaDestino.increment('balance', { by: valor, transaction: t });
    await TransferRecord.create(
      { fromAccountId, toAccountId, amount: valor },
      { transaction: t },
    );
    // Saiu sem erro → commit automático
  });
}
```

```typescript
// transactions/sequelize-nao-gerenciada.ts
import { sequelize } from '../database';
import { User } from '../models/user';

// Modo NÃO GERENCIADO — commit e rollback explícitos
// Útil quando a decisão de commit ou rollback depende de lógica fora do callback
export async function importarUsuariosEmLote(
  usuarios: Array<{ name: string; email: string }>,
): Promise<User[]> {
  const t = await sequelize.startUnmanagedTransaction(); // Sequelize ≥ 6.29
  try {
    const criados = await User.bulkCreate(usuarios, { transaction: t });
    await t.commit();
    return criados;
  } catch (error) {
    await t.rollback();
    throw error;
  }
}
```

### Transações em Drizzle

O Drizzle usa `db.transaction(async (tx) => {...})` onde `tx` é um client isolado. Todas as queries dentro do callback devem usar `tx` — queries feitas via `db` dentro do callback usam uma conexão diferente e ficam fora da transação.

```typescript
// transactions/drizzle-transfer.ts
import { eq, sql } from 'drizzle-orm';
import { db } from '../database';
import { accounts, transferRecords } from '../schema';

// db.transaction recebe callback com tx — use tx, nunca db, dentro do callback
export async function transferirSaldo(
  fromAccountId: string,
  toAccountId: string,
  valor: number,
): Promise<void> {
  await db.transaction(async (tx) => {
    const [contaOrigem] = await tx
      .select()
      .from(accounts)
      .where(eq(accounts.id, fromAccountId))
      .for('update'); // SELECT FOR UPDATE

    if (!contaOrigem || contaOrigem.balance < valor) {
      tx.rollback(); // lança TransactionRollbackError — não retorna, sai por exceção
    }

    // Use tx em TODAS as queries — nunca db dentro do callback
    await tx
      .update(accounts)
      .set({ balance: sql`${accounts.balance} - ${valor}` })
      .where(eq(accounts.id, fromAccountId));

    await tx
      .update(accounts)
      .set({ balance: sql`${accounts.balance} + ${valor}` })
      .where(eq(accounts.id, toAccountId));

    await tx.insert(transferRecords).values({
      fromAccountId,
      toAccountId,
      amount: valor,
      transferredAt: new Date(),
    });
  });
}
```

```typescript
// transactions/drizzle-savepoint.ts
import { db } from '../database';
import { orders, orderItems, notifications } from '../schema';

// Transações aninhadas criam SAVEPOINTs no PostgreSQL
// Permite rollback parcial sem reverter a transação externa
export async function criarPedidoComNotificacao(
  usuarioId: string,
  itens: Array<{ productId: string; quantity: number; price: number }>,
): Promise<string> {
  return db.transaction(async (tx) => {
    const [pedido] = await tx
      .insert(orders)
      .values({ userId: usuarioId, status: 'pending' })
      .returning({ id: orders.id });

    for (const item of itens) {
      await tx.insert(orderItems).values({ orderId: pedido.id, ...item });
    }

    // tx.transaction() cria SAVEPOINT interno
    // Se a notificação falhar, apenas o savepoint é revertido
    // O pedido e seus itens permanecem intactos na transação externa
    try {
      await tx.transaction(async (sp) => {
        await sp.insert(notifications).values({
          userId: usuarioId,
          type: 'order_created',
          payload: JSON.stringify({ orderId: pedido.id }),
        });
      });
    } catch {
      // Falha na notificação não cancela o pedido — tolerância a falhas intencional
    }

    return pedido.id;
  });
}
```

## Quando usar

| Cenário | Abordagem recomendada |
| --- | --- |
| Múltiplas tabelas com dependência (pedido + estoque) | Modo gerenciado de qualquer ORM |
| Leitura condicional antes de escrita (verificar saldo) | Prisma interativa, TypeORM `dataSource.transaction`, Sequelize gerenciada, Drizzle `db.transaction` |
| Batch de inserts independentes | Prisma `$transaction([...])`, Sequelize `bulkCreate` com `{ transaction: t }` |
| Rollback parcial com savepoints | Drizzle `tx.transaction()` aninhado, Sequelize não gerenciada |
| Controle de nível de isolamento | TypeORM `queryRunner.startTransaction('SERIALIZABLE')`, Prisma `isolationLevel`, Sequelize `{ isolationLevel }` |
| Injeção de repositórios TypeORM (NestJS) | Injete `DataSource` no service, use `dataSource.transaction()` — repositórios injetados ficam fora da transação |
| Publicar evento + atualizar banco | Outbox pattern — persiste evento na mesma transação, publicação desacoplada |

> [!tip] Regra de ouro
> Se duas ou mais operações precisam ser atômicas — ou todas ocorrem ou nenhuma — use uma transação. Transações longas bloqueiam outras operações: mantenha-as curtas e sem I/O externo (HTTP calls, filas) enquanto os locks estão abertos.

## Armadilhas comuns

### 1. Esquecer `{ transaction: t }` em operações Sequelize

Em Sequelize, a transação não é propagada implicitamente — cada operação precisa receber `{ transaction: t }` explicitamente. Uma operação sem esse parâmetro usa a conexão padrão do pool e executa **fora da transação**, mesmo dentro do callback gerenciado. O bug é silencioso: a operação sem transação persiste mesmo que o restante seja revertido por erro.

```typescript
// PROBLEMA — Account.update sem { transaction: t } persiste fora da transação
await sequelize.transaction(async (t) => {
  await Account.findOne({ where: { id: 1 }, transaction: t }); // dentro ✓
  await Account.update({ balance: 0 }, { where: { id: 1 } });  // FORA ✗
  throw new Error('rollback'); // reverte o findOne, mas o update já persistiu
});

// CORRETO
await sequelize.transaction(async (t) => {
  await Account.findOne({ where: { id: 1 }, transaction: t });
  await Account.update({ balance: 0 }, { where: { id: 1 }, transaction: t }); // dentro ✓
  throw new Error('rollback'); // reverte ambas as operações
});
```

### 2. Prisma `$transaction` interativa com timeout insuficiente

O timeout padrão é **5 segundos**. Em ambientes com latência ao banco (serverless, cold start), isso causa `Transaction already closed: A commit cannot be executed on a closed transaction`. Ajuste `maxWait` (aguardar conexão do pool) e `timeout` (duração máxima total) para o ambiente real.

```typescript
// PROBLEMA — timeout padrão de 5s insuficiente em serverless
await prisma.$transaction(async (tx) => {
  await tx.order.create({ data: pedidoData });
  await tx.stock.update({ where: stockQuery, data: stockData });
});

// CORRETO — ajuste timeouts para o ambiente real
await prisma.$transaction(
  async (tx) => {
    await tx.order.create({ data: pedidoData });
    await tx.stock.update({ where: stockQuery, data: stockData });
  },
  { maxWait: 5_000, timeout: 15_000 },
);
```

### 3. QueryRunner TypeORM sem `release()` no `finally`

`release()` no `try` faz a conexão vazar ao pool toda vez que há erro — com volume de requisições, o pool se esgota e requisições ficam bloqueadas com `ConnectionTimeoutError`. O `finally` garante a liberação independente do resultado.

### 4. Usar `db` em vez de `tx` dentro de `db.transaction()` no Drizzle

Queries via `db` dentro do callback usam conexão diferente e executam fora da transação. A transação commitará ou fará rollback apenas das operações feitas via `tx`.

### 5. I/O externo dentro de transações

Chamadas HTTP (APIs de pagamento, webhooks, notificações) dentro de uma transação mantêm os locks durante todo o tempo do I/O externo — potencialmente centenas de milissegundos. Isso bloqueia outras transações concorrentes nas mesmas linhas. Use o **Outbox pattern**: persista o evento em uma tabela `outbox` na mesma transação e processe a publicação assincronamente.

## Em entrevista

### "What is a database transaction and what does ACID mean?"

> A transaction is a unit of work that groups multiple operations into an atomic sequence — either all succeed and are committed, or none take effect. ACID describes the four guarantees that make transactions reliable: Atomicity means all-or-nothing, so if any operation fails, all changes are rolled back. Consistency means the transaction moves the database from one valid state to another, respecting all schema constraints. Isolation means concurrent transactions don't see each other's in-progress changes — each sees the database in a consistent state regardless of what other transactions are doing simultaneously. Durability means once committed, the changes survive even an immediate server crash. In Node, each ORM exposes a managed mode — Prisma's `$transaction(async (tx) => {})`, TypeORM's `dataSource.transaction(async (manager) => {})`, Sequelize's `sequelize.transaction(async (t) => {})`, Drizzle's `db.transaction(async (tx) => {})` — where commit and rollback happen automatically based on whether the callback throws.

### "What is the difference between optimistic and pessimistic locking, and when do you use each?"

> Pessimistic locking acquires an exclusive row lock at read time using `SELECT FOR UPDATE`, holding it until the transaction commits. This prevents concurrent transactions from modifying the locked rows, making it safe when conflicts are frequent — financial transfers where multiple concurrent operations may target the same account balance. The trade-off is reduced concurrency and deadlock risk. Optimistic locking reads without a lock, but before committing the update it verifies the data hasn't changed since the read — typically by checking a version counter or timestamp. If the data was modified by another transaction, the update fails and the caller retries. This is appropriate when conflicts are rare, such as editing a user profile. In TypeORM, optimistic locking is built in via the `@VersionColumn()` decorator — the ORM automatically increments the version on each update and rejects updates where the version in the database no longer matches the version that was read.

## Vocabulário

| Português | English |
| --- | --- |
| Transação | Transaction |
| Atomicidade | Atomicity |
| Consistência | Consistency |
| Isolamento | Isolation |
| Durabilidade | Durability |
| Nível de isolamento | Isolation level |
| Leitura suja | Dirty read |
| Leitura não repetível | Non-repeatable read |
| Leitura fantasma | Phantom read |
| Bloqueio pessimista | Pessimistic locking |
| Bloqueio otimista | Optimistic locking |
| Ponto de salvamento | Savepoint |
| Impasse | Deadlock |
| Padrão de caixa de saída | Outbox pattern |
| Vazamento de conexão | Connection pool leak |

## Veja também

- [[03-Dominios/Node/ORMs e banco de dados/index]] — panorama completo do Galho 6
- [[06 - N+1 queries - detecção e DataLoader]] — performance e batching de queries
- [[07 - Migrations e versionamento de schema]] — versionamento e deploy de schema
- [[09 - Paginação - offset, cursor e keyset]] — paginação eficiente em APIs Node
- [[10 - Cheatsheet e decision tree de ORMs]] — comparativo final e decision tree

## Fontes

- [Prisma — Transactions and batch queries](https://www.prisma.io/docs/orm/prisma-client/queries/transactions)
- [TypeORM — Transactions](https://typeorm.io/transactions)
- [Sequelize — Transactions](https://sequelize.org/docs/v6/other-topics/transactions/)
- [Drizzle ORM — Transactions](https://orm.drizzle.team/docs/transactions)
- [PostgreSQL — Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
