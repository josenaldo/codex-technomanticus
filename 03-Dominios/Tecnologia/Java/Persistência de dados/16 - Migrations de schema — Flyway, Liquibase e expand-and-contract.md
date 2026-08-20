---
title: "Migrations de schema — Flyway, Liquibase e expand-and-contract"
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
  - migrations
aliases:
  - "Flyway"
  - "Liquibase"
  - "expand-and-contract"
---

# Migrations de schema — Flyway, Liquibase e expand-and-contract

> [!abstract] TL;DR
> Versione o schema com **Flyway** (SQL versionado, arquivos `V<n>__<desc>.sql`) ou **Liquibase** (changelog declarativo em XML/YAML/JSON/SQL com rollback integrado) — nunca confie no `ddl-auto=update` em produção. Para alterar uma tabela grande sem downtime, aplique **expand-and-contract**: adicione a coluna primeiro, preencha os dados existentes (*backfill*) e só depois imponha a restrição — tudo em migrations separadas.

---

## O que é

*Schema migration* é o processo de evoluir o esquema relacional de um banco de dados de forma controlada, rastreável e reproduzível.

**Flyway** e **Liquibase** são as duas ferramentas dominantes no ecossistema JVM para isso. Ambas registram cada mudança aplicada em uma tabela de controle e garantem que o banco de dados em produção sempre reflita exatamente o conjunto de scripts versionados no repositório de código.

**Expand-and-contract** é um padrão de deployment seguro para mudanças destrutivas ou de alto impacto (renomear coluna, adicionar restrição `NOT NULL`) em tabelas que não podem ser bloqueadas — comum em sistemas de alta disponibilidade.

---

## Por que importa

- O banco de dados muda com o código; sem versionamento de schema, o deploy vira um ato manual propenso a erros e difícil de auditar.
- Em entrevistas de nível sênior, espera-se que o candidato saiba a diferença entre Flyway e Liquibase, conheça as armadilhas do `ddl-auto=update` em produção e consiga descrever como fazer uma migração zero-downtime.
- Expand-and-contract aparece com frequência em discussões de CI/CD, blue-green deployment e feature flags, porque é a ponte entre *schema change* e *application change* sem corte de serviço.

---

## Como funciona

### Por que versionar o schema — e por que não confiar no `ddl-auto=update` em produção

O Hibernate oferece `spring.jpa.hibernate.ddl-auto=update`, que detecta diferenças entre as entidades Java e o banco e aplica `ALTER TABLE` automaticamente. Em desenvolvimento local isso é conveniente; em produção é perigoso:

- Não há registro auditável do que foi alterado nem quando.
- Rollback é impossível — o Hibernate não gera `ALTER TABLE` inverso.
- Colunas obsoletas não são removidas (drift silencioso de schema).
- Ambientes distintos (staging, produção, DR) podem divergir sem aviso.

A alternativa é tratar o schema como código: cada mudança é um arquivo versionado, revisado em PR, aplicado de forma idempotente e registrado numa tabela de controle.

### Flyway — SQL puro, versionamento simples, `flyway_schema_history`

O Flyway varre um diretório de migrações (padrão: `src/main/resources/db/migration/`) e aplica os arquivos que ainda não estão registrados na tabela `flyway_schema_history`.

**Convenção de nomes:**

| Prefixo | Tipo | Exemplo |
|---------|------|---------|
| `V` | Versionada — executa uma única vez, em ordem crescente | `V1__create_orders.sql` |
| `R` | Repetível — reexecuta sempre que o checksum muda | `R__create_views.sql` |
| `U` | Undo — reverte uma migration versionada (requer Flyway Teams) | `U1__create_orders.sql` |

O separador entre versão e descrição são **dois underscores** (`__`). A versão pode ser inteira ou decimal: `V1`, `V1.1`, `V2`.

A tabela `flyway_schema_history` registra, para cada migration aplicada: versão, descrição, tipo, script, **checksum**, instalada por, instalada em, tempo de execução e status de sucesso. O checksum é calculado no conteúdo do arquivo; qualquer alteração posterior é detectada na próxima execução do `migrate` e a aplicação falha com erro de validação.

**Integração com Spring Boot:** adicionar `org.flywaydb:flyway-core` ao classpath ativa a auto-configuração. O `migrate` é executado durante o startup, antes de qualquer bean JPA ser inicializado. Propriedades relevantes:

```yaml
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: false   # true apenas ao adotar Flyway num banco existente
    validate-on-migrate: true    # padrão: valida checksums antes de migrar
```

### Liquibase — changelog declarativo, múltiplos formatos, rollback integrado

O Liquibase organiza as mudanças num **changelog** (arquivo raiz) composto por **changesets**. Cada changeset tem `id` e `author` (mais o caminho do arquivo) como identificador composto único — esse trio é registrado na tabela `DATABASECHANGELOG`.

O Liquibase suporta quatro formatos para os changelogs:

- **SQL** — arquivo com cabeçalho `--liquibase formatted sql` e changesets delimitados por `--changeset author:id`.
- **XML** — formato mais verboso, mas com suporte completo a todos os Change Types e rollback automático.
- **YAML** — menos verboso que XML, igualmente portável.
- **JSON** — mesma semântica do YAML, em sintaxe JSON.

Changelogs raiz que usam `include`/`includeAll` precisam ser XML, YAML ou JSON (não SQL puro).

**Exemplo de changelog SQL:**

```sql
--liquibase formatted sql

--changeset dev:1
CREATE TABLE orders (
    id         BIGSERIAL PRIMARY KEY,
    customer   VARCHAR(255) NOT NULL,
    total      NUMERIC(10, 2),
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
--rollback DROP TABLE orders;

--changeset dev:2
ALTER TABLE orders ADD COLUMN status VARCHAR(50);
--rollback ALTER TABLE orders DROP COLUMN status;
```

A coluna `MD5SUM` da `DATABASECHANGELOG` armazena o checksum de cada changeset. Se o conteúdo for alterado após a aplicação, o Liquibase detecta na próxima execução e falha (por padrão).

**Rollback declarativo:** changelogs em XML/YAML/JSON oferecem rollback automático para change types como `createTable` e `addColumn`. Para SQL puro e operações destrutivas (`dropTable`), o rollback precisa ser declarado explicitamente com `--rollback` ou `<rollback>`. Antes de executar, use `rollback-sql` para pré-visualizar o SQL gerado.

**Integração com Spring Boot:** adicionar `org.liquibase:liquibase-core` ao classpath ativa a auto-configuração. O changelog padrão é `db/changelog/db.changelog-master.yaml`. Propriedades relevantes:

```yaml
spring:
  liquibase:
    enabled: true
    change-log: classpath:db/changelog/db.changelog-master.yaml
```

### Flyway vs Liquibase — quando usar cada um

| Critério | Flyway | Liquibase |
|----------|--------|-----------|
| Formato | SQL puro (mais próximo do DBA) | XML/YAML/JSON/SQL (portável) |
| Rollback | Manual (undo migrations, versão paga) ou roll-forward | Declarativo e automático para XML/YAML/JSON |
| Tracking | `flyway_schema_history` | `DATABASECHANGELOG` |
| Complexidade | Menor curva de aprendizado | Mais funcionalidades (preconditions, contexts, labels) |
| Portabilidade cross-DB | Depende do SQL escrito | Change types abstraem o dialeto |

Use **Flyway** quando a equipe prefere SQL explícito e a regra de rollback é roll-forward. Use **Liquibase** quando rollback declarativo é obrigatório ou quando o projeto precisa suportar múltiplos bancos com um único changelog.

### Regras de ouro das migrations

1. **Nunca editar uma migration já aplicada.** O Flyway verifica o checksum e falha; o Liquibase verifica o MD5SUM e também falha. Crie uma nova migration com a correção.
2. **Roll-forward como estratégia primária de rollback.** Em vez de reverter o banco, crie uma nova migration que desfaz o efeito da anterior. Mais seguro, auditável e compatível com dados que já chegaram depois da migration problemática.
3. **Baseline apenas na adoção em banco existente.** `baseline-on-migrate: true` (Flyway) ou o comando `baseline` (Liquibase) marca o estado atual do banco como ponto de partida. Use apenas uma vez, ao onboar a ferramenta num banco que já tem schema.
4. **Migrations são imutáveis após o merge na branch principal.** Trate-as como commits — podem ser lidas, mas nunca reescritas.

### Expand-and-contract — mudança em tabela grande sem downtime

`ALTER TABLE ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'pending'` em uma tabela com milhões de linhas pode bloquear todas as escritas por segundos ou minutos, dependendo do banco. O padrão expand-and-contract evita isso quebrando a mudança em três fases deployadas separadamente:

**Fase 1 — Expand (adicionar nullable):**

```sql
-- V10__expand_add_status.sql
ALTER TABLE orders ADD COLUMN status VARCHAR(50);
```

A coluna chega sem restrição. O novo código da aplicação começa a preencher `status` em novas linhas, mas suporta `null` no código legado ainda em execução (blue-green ou rolling restart).

**Fase 2 — Backfill (preencher linhas existentes):**

```sql
-- V11__backfill_orders_status.sql
UPDATE orders SET status = 'legacy' WHERE status IS NULL;
```

Em tabelas muito grandes, o backfill pode ser feito em lotes (`WHERE id BETWEEN x AND y`) para não bloquear. Após o backfill, todo o código novo já está lendo `status` corretamente.

**Fase 3 — Contract (impor a restrição):**

```sql
-- V12__contract_status_not_null.sql
ALTER TABLE orders ALTER COLUMN status SET NOT NULL;
```

Agora é seguro impor `NOT NULL` — não existe mais nenhuma linha com `null`. Para índices, use `CREATE INDEX CONCURRENTLY` (PostgreSQL) para construir o índice sem lock exclusivo:

```sql
-- V13__index_orders_status.sql
CREATE INDEX CONCURRENTLY idx_orders_status ON orders(status);
```

O deploy sequencial garante que em nenhum momento a aplicação antiga e a nova entrem em conflito com o schema — cada fase é compatível com ambas as versões do código.

---

## Na prática

### Estrutura de pastas — Flyway

```
src/main/resources/
└── db/
    └── migration/
        ├── V1__create_orders.sql
        ├── V2__create_customers.sql
        ├── V3__add_product_sku.sql
        └── R__refresh_order_summary_view.sql
```

### Migration inicial — Flyway

```sql
-- V1__create_orders.sql
CREATE TABLE orders (
    id          BIGSERIAL PRIMARY KEY,
    customer_id BIGINT       NOT NULL,
    total       NUMERIC(10,2),
    created_at  TIMESTAMP    NOT NULL DEFAULT now()
);

CREATE TABLE order_items (
    id         BIGSERIAL PRIMARY KEY,
    order_id   BIGINT       NOT NULL REFERENCES orders(id),
    product_id BIGINT       NOT NULL,
    quantity   INT          NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL
);
```

### Expand-and-contract em três migrations

```sql
-- V10__expand_add_order_status.sql
ALTER TABLE orders ADD COLUMN status VARCHAR(50);
```

```sql
-- V11__backfill_order_status.sql
UPDATE orders SET status = 'legacy' WHERE status IS NULL;
```

```sql
-- V12__contract_order_status_not_null.sql
ALTER TABLE orders ALTER COLUMN status SET NOT NULL;
ALTER TABLE orders ADD CONSTRAINT chk_order_status
    CHECK (status IN ('pending','confirmed','shipped','delivered','cancelled','legacy'));
```

### Configuração Spring Boot — Flyway

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/orders_db
    username: app_user
    password: ${DB_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate        # valida, nunca altera — Flyway cuida do DDL
    open-in-view: false
  flyway:
    enabled: true
    locations: classpath:db/migration
    validate-on-migrate: true
    baseline-on-migrate: false
```

---

## Armadilhas

### (1) `ddl-auto=update` em produção — drift silencioso e sem auditoria

`update` aplica mudanças sem registro, sem rollback e sem revisão. Em um deploy errado, pode alterar o schema de forma irreversível antes que alguém perceba. A configuração correta em produção é `validate` (falha se o schema divergir das entidades) ou `none` (Flyway/Liquibase controla tudo). Em desenvolvimento, `create-drop` ou `update` são aceitáveis, mas devem ser explicitamente descartados antes do merge.

### (2) Editar uma migration já aplicada — checksum quebrado

O Flyway calcula o checksum do conteúdo de cada arquivo `.sql`. Se o arquivo for editado após ter sido aplicado em qualquer ambiente, o `validate-on-migrate: true` (padrão) fará o startup da aplicação falhar com `FlywayValidateException`. O Liquibase tem comportamento equivalente via MD5SUM na `DATABASECHANGELOG`. A única solução correta é **criar uma nova migration** com o conteúdo desejado. Se o erro já aconteceu em desenvolvimento, use `flyway repair` para recalcular os checksums — mas nunca em produção sem entender o impacto.

### (3) `ALTER TABLE ADD COLUMN NOT NULL` em tabela grande — lock na tabela inteira

No PostgreSQL, adicionar uma coluna `NOT NULL` sem `DEFAULT` exige uma reescrita da tabela inteira. Com um `DEFAULT` constante, versões modernas do PostgreSQL (≥11) evitam a reescrita, mas ainda podem ser problemáticas em tabelas com muitas linhas em bancos mais conservadores. A solução é o padrão expand-and-contract: adicionar nullable, fazer backfill e depois impor a restrição — em três migrations separadas e deployadas separadamente. Índices em tabelas grandes devem usar `CREATE INDEX CONCURRENTLY` para não bloquear leituras e escritas durante a criação.

---

## Em entrevista

### Frase pronta (inglês)

"Both Flyway and Liquibase solve schema versioning, but they have different philosophies: Flyway is SQL-first — you write plain `.sql` files with a version prefix like `V1__create_orders.sql`, and it tracks what's been applied in the `flyway_schema_history` table. Liquibase is changelog-first — you declare changes in XML, YAML, JSON, or SQL and it generates the SQL for you, with built-in declarative rollback for modeled change types. In production, I always disable `ddl-auto=update` and let the migration tool own the schema. For zero-downtime changes on large tables, I follow expand-and-contract: add the column as nullable, backfill existing rows in a second migration, and then enforce the constraint in a third — deployed in separate releases so both the old and new application code stay compatible throughout."

### Vocabulário

| Português | English |
|-----------|---------|
| Migração de schema | Schema migration |
| Controle de versão de banco | Database versioning / database change management |
| Reversão | Rollback |
| Expandir e contrair | Expand and contract |
| Preenchimento retroativo | Backfill |
| Tempo de inatividade | Downtime |
| Deriva de schema | Schema drift |
| Avançar em vez de reverter | Roll forward (instead of rollback) |

---

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/02 - A entidade JPA — @Entity, @Id e geração de chave|A entidade JPA]]
- [[03-Dominios/Ciência/Banco de Dados/index|Banco de dados]]
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/API Design|API Design]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Flyway|Flyway]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Liquibase|Liquibase]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#expand-and-contract|expand-and-contract]]

---

## Referências

- Redgate Flyway Documentation — Migrate command: https://documentation.red-gate.com/fd/migrate-277578887.html
- Redgate Flyway Documentation — SQL Migrations: https://documentation.red-gate.com/fd/migrations-271585107.html
- Liquibase Documentation — Changelog concepts: https://docs.liquibase.com/concepts/changelogs/home.html
- Liquibase Documentation — SQL format: https://docs.liquibase.com/start/get-started/liquibase-sql.html
- Liquibase Documentation — DATABASECHANGELOG table: https://docs.liquibase.com/concepts/tracking-tables/databasechangelog-table.html
- Liquibase Documentation — Rollback by tag: https://docs.liquibase.com/commands/rollback/rollback-by-tag.html
- Spring Boot Reference — SQL Databases: https://docs.spring.io/spring-boot/reference/data/sql.html
