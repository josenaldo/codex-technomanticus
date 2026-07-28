---
title: "Roadmap — Acesso a Dados"
created: 2026-07-28
type: meta
publish: false
tags:
  - meta
  - roadmap
  - design-de-software
  - acesso-a-dados
  - persistencia
---

# Roadmap — Acesso a Dados (galho-folha, construção)

Roadmap da família `03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Acesso a Dados`. Galho-**folha em modo construção**: uma entrada por nota **a escrever**. Pai: [[Padrões de Projeto/roadmap|Padrões de Projeto]]. Fontes: Fowler (*PoEAA*), J2EE Core Patterns, literatura NoSQL/DDD.

## Escopo desta família

Os padrões de **acesso a dados** — como um objeto conversa com o armazenamento (banco relacional, NoSQL). Cobre a **lógica de negócio × dados** (Transaction Script, Domain Model, Table Module), os **padrões de fonte de dados** (DAO, Active Record, Data Mapper, gateways, Repository), a **maquinaria de ORM** (Unit of Work, Identity Map, Lazy Load, Query Object) e o **impacto do NoSQL** (agregado, single-table, polyglot). Eixo dorsal: **Active Record × Data Mapper**, as duas filosofias rivais.

**Fora de escopo (movidos):** Cache-Aside, sharding, read-replicas → são infra/resiliência (família 6 Nuvem e Resiliência) e [[03-Dominios/Tecnologia/Cloud/index|Cloud]], não acesso a dados.

## Anatomia de cada nota

Padrão-capítulo, como no GoF, **com a lente adaptada**: em acesso a dados o contraste interessante não é sintaxe de linguagem, é **qual ecossistema de ORM encarna qual padrão** —

- **Active Record** → Rails, Django ORM, Laravel Eloquent
- **Data Mapper** → Hibernate/JPA, SQLAlchemy, Doctrine, Ent (Go)
- **Repository** → Spring Data; **Query Object** → Criteria/QueryDSL/Specifications, SQLAlchemy expression
- **TS**: Prisma (mapper-ish), TypeORM (Active Record *ou* Data Mapper)

Estrutura: cenário → ideia (Mermaid) → **como os ORMs/ecossistemas o encarnam** → **quando NÃO usar / usos equivocados (Armadilhas reforçada)** → inglês + PT↔EN → O que vem a seguir → Fontes. Cada entrada **autocontida** (catálogo de consulta); redundância com Java/Dados é aceitável, cross-link como "aprofunde".

**Esquema `fase:`:** por centralidade/tema (Iniciado = lógica de negócio + entrada; Adepto = mapper/ORM; Magus = NoSQL/nuvem).

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Notas de conteúdo | 15 |
| Iniciado | 6 |
| Adepto | 7 |
| Magus | 2 |
| ✅ escritas | 6 |
| ⬜ pendentes | 9 |
| % concluído | 40% |
| Scaffolding | index.md criado (2026-07-28) |

---

## Notas — Iniciado (onde mora a lógica + entrada)

#### 01 - Panorama do acesso a dados   [substantivo]
- **Estado:** ✅ escrita (2026-07-28) · fase: iniciado · 142 linhas
- **Escopo:** o problema (descasamento objeto↔relacional / *impedance mismatch*); o mapa da família; a lente cross-ORM; **Active Record × Data Mapper** como eixo dorsal; como usar o catálogo. Mermaid do mapa.
- **Resultado:** impedance mismatch como origem; Mermaid mapa da família (4 grupos); tabela AR×DM (dorsal); lente cross-ORM explicada; ORM esconde-não-elimina o atrito; 3 armadilhas. Aprovada.

#### 02 - Transaction Script   [substantivo]
- **Estado:** ✅ escrita (2026-07-28) · fase: iniciado · 117 linhas
- **Escopo:** lógica procedural por caso de uso, direto no banco. Simples e honesto p/ CRUD. **Armadilha:** duplicação e apodrecimento quando a regra cresce; anemia. Quando ainda é a resposta certa.
- **Resultado:** roteiro por caso de uso; escolha legítima (não erro); Mermaid TS×DM; quando é certo (CRUD/pouca lógica) e quando apodrece (duplicação); 3 armadilhas (God method, lógica no controller). Aprovada.

#### 03 - Domain Model   [substantivo]
- **Estado:** ✅ escrita (2026-07-28) · fase: iniciado · 115 linhas
- **Escopo:** lógica rica nos objetos (par do Rich Domain Model — linka [[10 - Rich vs Anemic Domain Model]] em OO). Quando compensa a complexidade. **Armadilha:** domain model anêmico (getters/setters + service faz tudo).
- **Resultado:** regra mora com os dados; Mermaid anêmico×rico; quer Data Mapper (domínio ignorante do banco); coração do DDD; 3 armadilhas (anêmico, domínio-conhece-banco, over-eng em CRUD). Aprovada.

#### 04 - Table Module   [substantivo]
- **Estado:** ✅ escrita (2026-07-28) · fase: iniciado · 111 linhas
- **Escopo:** **um objeto por tabela** operando sobre um Record Set (o "objeto que representa a tabela"). .NET DataSet/DataTable. Meio-termo entre Transaction Script e Domain Model. Raro fora de .NET. **Armadilha:** confundir com Domain Model (um objeto POR registro).
- **Resultado:** 1 objeto por tabela × 1 por registro (Mermaid); habitat .NET/Record Set; honesto sobre raridade (legado .NET); 3 armadilhas (confundir c/ DM, fora do ecossistema, God object). Aprovada.

#### 05 - DAO (Data Access Object)   [substantivo]
- **Estado:** ✅ escrita (2026-07-28) · fase: iniciado · 122 linhas
- **Escopo:** interface de acesso (J2EE Core Patterns); separa persistência do resto. Vivíssimo em legado enterprise. **Armadilha central:** DAO anêmico que só repassa pro ORM — camada inútil sobre Spring Data. DAO × Repository.
- **Resultado:** interface esconde a fonte (Mermaid multi-fonte); tabela DAO×Repository (J2EE×DDD, Spring Data borra a linha); quando é redundante (só repassa); 3 armadilhas (anêmico, vaza fonte, God interface/ISP). Aprovada.

#### 06 - Active Record   [substantivo]
- **Estado:** ✅ escrita (2026-07-28) · fase: iniciado · 119 linhas
- **Escopo:** objeto = linha + persistência embutida (`user.save()`). Rails, Django ORM, Eloquent, TypeORM (modo AR). Produtivo p/ CRUD. **Armadilha central:** vira God object, acopla domínio ao esquema do banco, difícil de testar sem banco. AR × Data Mapper (o grande debate).
- **Resultado:** o objeto sabe se salvar; lente cross-ORM (Rails/Django/Eloquent; Java NÃO); Mermaid fusão dados+regra+persistência; 3 armadilhas (fat model, testabilidade, acoplamento ao esquema). Aprovada. **Fecha o bloco Iniciado da família 2.**

## Notas — Adepto (mapper, repository e maquinaria ORM)

#### 07 - Gateways (Row/Table Data Gateway + Record Set)   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** wrappers finos sobre **uma linha** (Row Data Gateway) ou **uma tabela** (Table Data Gateway); Record Set como resultado tabular. Legado, .NET/JDBC cru. Onde aparecem e por que minguaram (ORMs os absorveram).
- **Resultado:** —

#### 08 - Data Mapper   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** camada que move dados entre objetos e banco **mantendo-os ignorantes um do outro**. Hibernate/JPA, SQLAlchemy, Doctrine, Ent. O rival do Active Record (domínio puro × produtividade). **Armadilha:** complexidade, leaky abstraction (o mapper vaza), N+1.
- **Resultado:** —

#### 09 - Repository   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** coleção-em-memória sobre o mapper; esconde a query atrás de uma interface tipo coleção. Spring Data, DDD. **Armadilha:** repository genérico que vaza `IQueryable`/`Criteria`; repository sobre Active Record (redundante); explosão de métodos `findByXAndY`.
- **Resultado:** —

#### 10 - Unit of Work   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** rastreia mudanças na operação de negócio e persiste tudo numa transação. Hibernate `Session`, JPA `EntityManager`, SQLAlchemy `Session`. **Armadilha:** sessão longa demais, `flush` em hora surpresa, `OSIV` (open-session-in-view).
- **Resultado:** —

#### 11 - Identity Map   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** garante **uma instância por linha** dentro da sessão (o cache de 1º nível do Hibernate). Evita objetos duplicados e inconsistentes. **Armadilha:** dado obsoleto (stale) na sessão, consumo de memória, surpresa em long-running.
- **Resultado:** —

#### 12 - Lazy Load   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** carregar sob demanda via **proxy** (linka [[10 - Proxy]] do GoF). Tipos (lazy initialization, virtual proxy, value holder, ghost). **Armadilha central:** o **N+1**, `LazyInitializationException` fora da sessão. Fetch join / batch como saída.
- **Resultado:** —

#### 13 - Query Object   [substantivo]
- **Estado:** ⬜ a escrever · fase: adepto
- **Escopo:** query como **objeto** (não string SQL). JPA Criteria, QueryDSL, Spring Data Specifications, SQLAlchemy expression language. Componível, type-safe. **Armadilha:** over-abstração onde SQL direto/nomeado seria mais claro; queries ilegíveis.
- **Resultado:** —

## Notas — Magus (NoSQL e nuvem remodelam o acesso)

#### 14 - Modelagem por agregado e single-table design   [substantivo]
- **Estado:** ⬜ a escrever · fase: magus
- **Escopo:** NoSQL inverte o design — **query-first**, desnormalização, agregado (DDD) como unidade de consistência. Single-table design no DynamoDB. **Armadilha central:** modelar NoSQL como relacional (normalizar, joins na aplicação); access patterns não pensados antes.
- **Resultado:** —

#### 15 - Polyglot persistence e materialized views   [substantivo]
- **Estado:** ⬜ a escrever · fase: magus
- **Escopo:** o banco certo para cada carga (relacional + documento + chave-valor + busca); read models / materialized views (encosta em CQRS — linka [[14 - Command]] e família 5 Eventos). **Armadilha:** complexidade operacional, consistência eventual mal gerida, "poliglota" prematuro.
- **Resultado:** —

---

## Próximos passos

1. ⬜ Escrever 01 → 15 na ordem, via `/escrever-nota`. `/checkpoint` a cada bloco de fase (após 06, após 13, após 15).
2. ⬜ Criar `index.md` da família (MOC por fase + rotas + dataview) ao ter ≥ bloco Iniciado.
3. ⬜ Ao fechar 15: atualizar roadmap-pai (família 2 ✅) + [[00-Meta/Roadmap]] central; abrir família 3 (Integração Empresarial / EIP).
