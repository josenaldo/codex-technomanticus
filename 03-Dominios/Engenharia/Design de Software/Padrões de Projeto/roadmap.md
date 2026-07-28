---
title: "Roadmap — Padrões de Projeto"
created: 2026-07-28
type: meta
publish: false
tags:
  - meta
  - roadmap
  - design-de-software
  - padroes-de-projeto
---

# Roadmap — Padrões de Projeto (galho-pai)

Roadmap do galho `03-Dominios/Engenharia/Design de Software/Padrões de Projeto`. Galho-**pai**: mapeia o estado dos sub-galhos (famílias de padrões). Cada família tem (terá) seu próprio `roadmap.md` folha. Origem: sessão de brainstorming de 2026-07-28 (Tier 2 do [[00-Meta/Roadmap]], consolidação de Design de Software).

> [!abstract] O que é este galho
> Um **catálogo de consulta** de padrões de projeto e de arquitetura de aplicação, para um sênior de plantão — inclusive (e especialmente) em **sistemas legados**. Não é uma trilha linear de aprendizado: é um repertório onde se **procura** um padrão. Por isso, cada entrada é **autocontida** (dá pra entender sem sair do galho) e alguma **redundância** com outros galhos do vault é aceitável e desejada — o catálogo não pode depender de galhos que evoluem em ritmo próprio.

## Princípios de design do galho

1. **Catálogo independente.** Cada nota de padrão se sustenta sozinha: cenário → ideia → implementação → quando não usar. Cross-links são *"aprofunde aqui"*, nunca dependência.
2. **Lente cross-linguagem.** Todo padrão é mostrado em **Java, TypeScript, Python e Go**, comentando como os recursos da linguagem mudam a implementação — e **quando a linguagem torna o padrão desnecessário** (ex.: Strategy vira função; Go sem herança dissolve Template Method; pattern matching mata Visitor).
3. **Peso no "quando NÃO usar".** Todo mundo ensina quando usar. Aqui a seção **Armadilhas** é recheada: usos equivocados, o custo de aplicar cedo demais, o sinal de abstração prematura. É o diferencial do galho.
4. **Redundância = reforço** (convenção do vault: nunca deduplicar assunto repetido entre notas; linkar). Onde uma família encosta em galho já pronto (Comunicação, Cloud, Operação), a entrada é autocontida **e reconhece** a casa profunda.

## Estado dos sub-galhos (famílias)

**Legenda:** ✅ completo · 📋 roadmap pronto, escrita pendente · 🔶 parcial · ⬜ não planejado em detalhe · `%` = (✅+➖)/total.

| # | Família | Fonte canônica | Notas (est.) | Sobreposição | Estado | roadmap |
|---|---------|----------------|-------------:|--------------|--------|---------|
| 1 | **Clássicos (GoF)** | Gang of Four (1994) | 23 | baixa | ✅ **COMPLETA 23/23** (2026-07-28) | [[Padrões de Projeto/Clássicos (GoF)/roadmap\|folha]] |
| 2 | **Acesso a Dados** | Fowler PoEAA + J2EE + NoSQL | 15 | média (Java/Dados) | ✅ **COMPLETA 15/15** (2026-07-28) | [[Padrões de Projeto/Acesso a Dados/roadmap\|folha]] |
| 3 | **Integração Empresarial (EIP)** | Hohpe & Woolf | ~14 | baixa | ⬜ roster provisório abaixo | a criar |
| 4 | **Aplicação Corporativa** | Fowler PoEAA (não-dados) | ~14 | baixa | ⬜ roster provisório abaixo | a criar |
| 5 | **Arquitetura de Eventos** | EDA moderna | ~10 | **alta** (Comunicação) | ⬜ roster provisório abaixo | a criar |
| 6 | **Nuvem e Resiliência** | Azure/AWS Cloud Design Patterns | ~14 | **alta** (Cloud/Operação) | ⬜ roster provisório abaixo | a criar |

**Total estimado:** ~90-100 notas de conteúdo + scaffolding (index/roadmap por família). Escala de domínio; **construção sequencial**, família a família.

## Ordem de execução

Sequência escolhida (valor pro ofício de legado primeiro, maior sobreposição por último):

1. **Clássicos (GoF)** — ✅ completa. 2. **Acesso a Dados** — ✅ completa.
2. **Integração Empresarial (EIP)** ← **próxima** → 4. **Aplicação Corporativa** (o coração do valor-legado; cobertura quase toda nova).
3. **Arquitetura de Eventos** → 6. **Nuvem e Resiliência** por último (maior sobreposição, menor valor marginal — entradas autocontidas + link).

**Disciplina de custo:** escrita sequencial, uma nota por vez via `/escrever-nota`; `/checkpoint` entre blocos; **sem fan-out massivo** (regra pessoal do usuário). Cada família = seu próprio ciclo brainstorm→roadmap-folha→escrita quando chegar a vez dela.

---

## Rosters provisórios das famílias 2-6

> Capturados agora para **evitar drift** na tarefa longa. São provisórios — cada família ganha roadmap-folha detalhado (fases, escopo por nota, custo) quando for a vez dela.

### Família 2 — Acesso a Dados (15) — **CORTE FECHADO 2026-07-28**, ver [[Padrões de Projeto/Acesso a Dados/roadmap|roadmap-folha]]
Iniciado: 01 Panorama · 02 Transaction Script · 03 Domain Model · 04 Table Module (Service Layer como seção) · 05 DAO · 06 Active Record.
Adepto: 07 Gateways (Row/Table Data Gateway + Record Set) · 08 Data Mapper · 09 Repository · 10 Unit of Work · 11 Identity Map · 12 Lazy Load · 13 Query Object.
Magus: 14 agregado + single-table (DynamoDB) · 15 polyglot persistence + materialized views.
**Lente adaptada:** cross-ORM (AR=Rails/Django/Eloquent; Data Mapper=Hibernate/SQLAlchemy/Doctrine; Repository=Spring Data), não cross-linguagem pura. Eixo dorsal: **Active Record × Data Mapper**.
**Movidos p/ fora:** Cache-Aside · sharding · read-replicas → família 6 (Nuvem e Resiliência) / Cloud (não são acesso a dados).

### Família 3 — Integração Empresarial / EIP (~14)
Subset curado dos 65 de Hohpe & Woolf: **Message Channel** · **Message** · **Pipes and Filters** · roteamento (**Content-Based Router**, **Message Filter**, **Recipient List**, **Splitter**, **Aggregator**, **Resequencer**) · **Message Translator/Normalizer** · **Canonical Data Model** · endpoints (**Polling vs Event-Driven Consumer**, **Competing Consumers**, **Idempotent Receiver**) · **Guaranteed Delivery** · **Dead Letter Channel** · **Message Bus vs Broker**. Alto valor legado (ESBs, MOM, Camel/MuleSoft).

### Família 4 — Aplicação Corporativa / PoEAA não-dados (~14)
Apresentação web: **MVC** · **Page Controller** · **Front Controller** · **Application Controller** · **Template View** · **Transform View** · **Two-Step View**.
Distribuição: **Remote Facade** · **DTO** · **Service Layer**.
Concorrência offline: **Optimistic Offline Lock** · **Pessimistic Offline Lock** · **Coarse-Grained Lock**.
Session state: **Client/Server/Database Session State**.
Base: **Gateway** · **Mapper** · **Layer Supertype** · **Separated Interface** · **Registry** · **Value Object** · **Money** · **Special Case** · **Plugin** · **Service Stub**.

### Família 5 — Arquitetura de Eventos (~10)
**Event Notification** · **Event-Carried State Transfer** · **Event Sourcing** · **CQRS** · **Saga** (choreography vs orchestration) · **Process Manager** · **Outbox** · **Idempotent Consumer / Inbox** · **Domain Events** · **Event Collaboration**.
> Sobreposição alta com [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] (assíncrona). Entrada de catálogo autocontida + link "aprofunde".

### Família 6 — Nuvem e Resiliência (~14)
**Circuit Breaker** · **Retry** · **Timeout** · **Bulkhead** · **Rate Limiting / Throttling** · **Cache-Aside** · **Ambassador** · **Sidecar** · **Anti-Corruption Layer** · **Strangler Fig** · **Gatekeeper** · **Valet Key** · **Leader Election** · **Health Endpoint Monitoring**.
> Sobreposição alta com [[03-Dominios/Tecnologia/Cloud/index|Cloud]] e [[03-Dominios/Engenharia/Operação/index|Operação]]. Strangler Fig / ACL também vivem na [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index|Arqueologia]]. Entrada autocontida + link.

---

## Pendências transversais / decisões em aberto

- **Notas meta-catálogo do galho-pai (capstone):** "Reconhecer patterns nos frameworks" e "Quando NÃO usar: discernimento sênior" começam **escopadas em GoF** (família 1, notas 22-23). Quando ≥2 famílias existirem, avaliar graduá-las a **capstone do galho-pai** que generaliza pra todas as famílias, em vez de repetir por família.
- **`fase:` vs sequência:** GoF adota fases (Iniciado/Adepto/Magus) por **centralidade/frequência** do padrão, não como gate de aprendizado — é catálogo. Famílias-referência (2-6) podem ser SEM fase (sequência). Decidir por família no roadmap-folha.
- **Poda do monólito (no fim da família 1):** `Design Patterns.md` (631 ln, `publish:false`) é a matéria-prima da família GoF. Ao fechar GoF, podar em stub/redirect. **8 notas linkam `[[Design Patterns]]`** (SOLID 01/03/index, OO 06/07/12/13/index) — preservar a resolução: ou manter stub `Design Patterns.md` com callout → índice do galho-pai, ou dar alias "Design Patterns" ao `index.md` da família GoF (atenção à regra do Quartz: folder-link exige index.md; padrão tronco→galhos do vault).
- **`index.md` do galho-pai + das famílias:** criar quando houver conteúdo (evitar links pendentes / quebra Quartz). Rastreado como passo.

## Próximos passos

1. ✅ Roadmap do galho-pai (este arquivo) + roadmap-folha da família GoF criados (2026-07-28).
2. ✅ [[00-Meta/Roadmap]] central atualizado com a decisão das 6 famílias (2026-07-28).
3. ✅ Escrever a família **Clássicos (GoF)** — **COMPLETA 23/23 (2026-07-28)**; `index.md` da família criado, todas as fases linkadas.
4. ✅ Monólito `Design Patterns.md` **podado** (2026-07-28, opção a): virou este `index.md` do galho-pai, com alias `Design Patterns`; 8 inbound links resolvem via alias; refs full-path do galho Python reapontadas p/ o index da GoF; índice do domínio atualizado.
5. ✅ `index.md` deste galho-pai criado (MOC das 6 famílias).
6. ✅ Família **Acesso a Dados** — **COMPLETA 15/15 (2026-07-28)**; Iniciado 01-06, Adepto 07-13, Magus 14-15; `index.md` da família com todas as fases linkadas; roadmap-folha 100%.
7. ⬜ **Próxima família: Integração Empresarial (EIP)** — novo ciclo brainstorm leve + roadmap-folha detalhado (roster provisório na seção acima).
8. ⬜ **Capstone do galho-pai:** com 2 famílias fechadas, reavaliar graduar as notas 22-23 do GoF (frameworks / quando NÃO usar) a capstone que generaliza pras famílias — decisão em aberto na seção de pendências.
