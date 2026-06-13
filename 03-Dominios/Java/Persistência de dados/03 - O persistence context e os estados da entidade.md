---
title: "O persistence context e os estados da entidade"
created: 2026-06-09
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - persistencia
  - iniciado
  - jpa
  - hibernate
aliases:
  - "persistence context"
  - "estados da entidade"
---

# O persistence context e os estados da entidade

> [!abstract] TL;DR
> O persistence context é um cache de 1º nível associado à transação corrente: cada entidade carregada dentro dele tem **identidade garantida** — buscar o mesmo `Order` duas vezes executa apenas 1 SQL e retorna a **mesma referência Java**. Além disso, qualquer mudança num campo de uma entidade **managed** é detectada automaticamente pelo **dirty checking** e vira um `UPDATE` no commit — sem precisar chamar `save()`.

## O que é

O **persistence context** (contexto de persistência) é o espaço onde o JPA rastreia entidades durante uma transação. No Hibernate, ele é implementado pela `Session`; no JPA padrão, pelo `EntityManager`.

Pense nele como uma **sala de operações temporária**: tudo que entra fica sob vigilância constante. Se qualquer atributo mudar, o JPA detecta e prepara o SQL de atualização na hora certa — o **flush**.

Esse contexto funciona como o **cache de 1º nível**: dentro de uma mesma transação, a mesma entidade é representada por exatamente **um objeto na memória**. Não importa quantas vezes você consulte o mesmo `Order` por ID: o banco recebe apenas uma query, e as chamadas subsequentes retornam o objeto já presente no contexto.

Ao lado do cache, o persistence context também define os **estados da entidade** — o ciclo de vida que vai da criação ao descarte de um objeto.

## Por que importa

Entender o persistence context responde a três dúvidas clássicas:

1. **Por que não preciso chamar `save()` depois de alterar uma entidade carregada?** — Porque ela está **managed**: o dirty checking já cuida do `UPDATE`.
2. **Por que a mesma query executada duas vezes retorna o mesmo objeto?** — Porque o contexto garante identidade; o segundo acesso nem vai ao banco.
3. **Por que recebo `LazyInitializationException` fora de uma transação?** — Porque ao fechar a transação, o contexto é destruído e as entidades ficam **detached** — esse problema é detalhado na nota sobre fetch strategies (veja "Veja também").

Esses três pontos são favoritos em entrevistas técnicas para posições sênior.

## Como funciona

### Os 4 estados e as transições

Uma entidade Java pode estar em exatamente um desses quatro estados em relação ao persistence context:

| Estado | Descrição |
|---|---|
| **Transient** (novo) | Objeto criado com `new`, sem ID e sem vínculo com nenhum contexto. |
| **Managed** (persistente) | Associado ao contexto ativo; qualquer mudança será sincronizada no flush. |
| **Detached** (destacado) | Já foi managed, mas o contexto foi fechado ou o objeto foi desvinculado. ID existe, mas mudanças não são rastreadas. |
| **Removed** (removido) | Marcado para deleção; será excluído no próximo flush. |

Diagrama das transições:

```text
         new Order()
              │
              ▼
        ┌──────────┐
        │ TRANSIENT │
        └──────────┘
              │ persist() / save() [id null]
              ▼
        ┌──────────┐  detach() / close() / clear()
        │  MANAGED  │ ─────────────────────────────► ┌──────────┐
        └──────────┘                                  │ DETACHED │
              ▲                                       └──────────┘
              │ merge() / save() [id existe]               │
              └────────────────────────────────────────────┘
              │
              │ remove()
              ▼
        ┌─────────┐
        │ REMOVED │
        └─────────┘
              │ flush / commit
              ▼
         (deletado no banco)
```

As operações de transição são:

- **`persist()`** — transient → managed (agenda `INSERT`)
- **`merge()`** — detached → managed (copia estado para uma instância gerenciada; pode gerar `UPDATE`)
- **`remove()`** — managed → removed (agenda `DELETE`)
- **`detach()`** — managed → detached (desvincula sem deletar)

### Persistence context = cache de 1º nível (identidade: `o1 == o2`)

Dentro de uma transação, o contexto garante que a mesma linha do banco seja representada por **um único objeto Java**. Isso é chamado de **identidade de entidade**.

Consequência prática: se você busca o `Order` de ID 42 duas vezes na mesma transação, o banco recebe **um único `SELECT`**; a segunda chamada consulta o contexto interno e retorna a mesma referência.

```java
@Transactional
public void demonstrarIdentidade(Long id) {
    Order o1 = orderRepository.findById(id).orElseThrow();
    Order o2 = orderRepository.findById(id).orElseThrow();

    // true — mesma referência; segundo findById não gerou SQL
    assert o1 == o2;
}
```

### Dirty checking: por que você não chama `save()` em entidade managed

O Hibernate tira um "snapshot" do estado de cada entidade managed no momento em que ela entra no contexto. No flush, ele compara o estado atual com o snapshot. Se houver diferença, gera um `UPDATE` automaticamente — sem que o código precise chamar `save()` ou qualquer método explícito.

Esse mecanismo se chama **dirty checking** (verificação de sujeira).

Regra prática: se a entidade foi carregada **dentro** da transação corrente, ela já está managed. Alterar um campo dela é suficiente para que a mudança persista no commit.

### `save()` do Spring Data: persist ou merge? E quando ocorre o flush?

O `CrudRepository.save()` (implementado por `SimpleJpaRepository`) segue esta lógica:

- **ID nulo** → entidade considerada nova → chama `entityManager.persist()` → agenda `INSERT`
- **ID preenchido** → entidade considerada existente → chama `entityManager.merge()` → pode gerar `UPDATE` ou `SELECT` + `UPDATE`

O **flush** — sincronização das mudanças pendentes com o banco — acontece em três momentos:

1. **No commit da transação** (modo padrão `AUTO`)
2. **Antes de uma query JPQL/HQL** (para garantir dados consistentes na consulta)
3. **Explicitamente** via `entityManager.flush()` ou `repository.flush()`

## Na prática

O trecho abaixo demonstra identidade de objeto e dirty checking num método transacional real:

```java
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class OrderService {

    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    @Transactional
    public void processOrder(Long orderId) {

        // Primeira busca — executa SELECT no banco
        Order o1 = orderRepository.findById(orderId).orElseThrow();

        // Segunda busca — NÃO executa SELECT (cache de 1º nível)
        Order o2 = orderRepository.findById(orderId).orElseThrow();

        // Identidade garantida: mesma referência Java
        System.out.println(o1 == o2); // true

        // Mudança de campo — dirty checking detecta no flush
        o1.setStatus(OrderStatus.PROCESSING);

        // NÃO é necessário chamar orderRepository.save(o1)
        // O Hibernate compara o snapshot e gera UPDATE automaticamente no commit
    }
}
```

Ao final do método, o Hibernate compara o estado atual de `o1` com o snapshot original. Detecta que `status` mudou e emite:

```sql
UPDATE orders SET status = 'PROCESSING' WHERE id = ?
```

Nenhum `save()` foi chamado.

## Armadilhas

### (1) Chamar `save()` em entidade já managed

Chamar `orderRepository.save(order)` em uma entidade que já está managed é **redundante** — não causa erro, mas o `merge()` interno faz uma cópia desnecessária e pode disparar um `SELECT` extra para recarregar o estado antes de mesclar.

```java
// ERRADO — save() desnecessário; dirty checking já cuida do UPDATE
@Transactional
public void updateStatus(Long id) {
    Order order = orderRepository.findById(id).orElseThrow();
    order.setStatus(OrderStatus.DONE);
    orderRepository.save(order); // redundante e potencialmente prejudicial
}

// CORRETO — apenas alterar o campo; o flush no commit gerará o UPDATE
@Transactional
public void updateStatus(Long id) {
    Order order = orderRepository.findById(id).orElseThrow();
    order.setStatus(OrderStatus.DONE);
    // fim do método → commit → flush → UPDATE gerado automaticamente
}
```

### (2) Esperar que mudanças persistam sem transação ativa

Fora de um contexto transacional, não existe persistence context. Tentar manipular entidades managed sem uma transação lança `javax.persistence.TransactionRequiredException` (ou `jakarta.persistence.TransactionRequiredException`).

```java
// ERRADO — sem @Transactional; lança TransactionRequiredException no persist/merge
public void createOrderSemTransacao(Order order) {
    orderRepository.save(order); // falha se não houver transação ativa
}

// CORRETO — transação garante que o persistence context existe
@Transactional
public void createOrder(Order order) {
    orderRepository.save(order);
}
```

### (3) Acessar associação lazy em entidade detached

Quando a transação termina, o persistence context é fechado e as entidades tornam-se **detached**. Tentar navegar por uma associação mapeada como `LAZY` nesse estado lança `LazyInitializationException`.

Esse é um dos erros mais comuns em aplicações Spring e merece atenção especial — mas o assunto é aprofundado na nota de fetch strategies (veja "Veja também"). Aqui basta saber: **entidade detached não tem contexto; qualquer acesso lazy explode**.

## Em entrevista

### Frase pronta (inglês)

"The persistence context acts as a first-level cache tied to the current transaction: loading the same entity twice issues only one SQL and returns the same Java reference. Any field change on a managed entity is automatically detected by dirty checking and translated into an UPDATE at flush time — no explicit save() call needed. When the transaction closes, entities become detached and lazy associations can no longer be initialized."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Contexto de persistência | Persistence context |
| Entidade gerenciada | Managed entity |
| Entidade destacada | Detached entity |
| Verificação de mudanças | Dirty checking |
| Descarga / sincronização | Flush |
| Cache de primeiro nível | First-level cache |
| Estado transitório | Transient state |
| Estado removido | Removed state |

## Veja também

- [[03-Dominios/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]]
- [[03-Dominios/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Fetch strategies e a LazyInitializationException]]
- [[03-Dominios/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade|EntityManager e o ciclo de vida da entidade]]
- [[03-Dominios/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#persistence context (1º nível)|persistence context]]

## Referências

- Hibernate ORM User Guide — Persistence Contexts, Entity States, Dirty Checking, Flushing: https://docs.hibernate.org/orm/current/userguide/html_single/Hibernate_User_Guide.html
- Spring Data JPA Reference — Persisting Entities, save() semantics (persist vs merge): https://docs.spring.io/spring-data/jpa/reference/jpa/entity-persistence.html
