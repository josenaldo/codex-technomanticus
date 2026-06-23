---
title: "Galho Testes — design e plano (Fundamentos, Camada A)"
created: 2026-06-18
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - testes
---

# Galho Testes — design e plano

## Contexto
Sétimo e ÚLTIMO galho da Camada A do meta-plano de Fundamentos
(`2026-06-15-fundamentos-meta-planejamento-design.md`), depois de Estruturas de Dados, Algoritmos, OO,
SOLID, Banco de Dados e Redes e Protocolos (todos COMPLETOS). Refatora o monólito
`03-Dominios/Ciência/Testes.md` (584 ln, evergreen) no padrão tronco/galhos + 3 fases.
Interview-critical (★). Roster aprovado pelo usuário em 2026-06-18 (expandido p/ 16 notas).

A semente é o monólito inteiro: função estratégica, pirâmide/troféu, tipos de teste, test doubles, TDD,
F.I.R.S.T/AAA, flaky tests, coverage, edge cases, CI/CD, armadilhas, e 5 experiências reais do usuário
(preservar, [[feedback-no-fabrication]]).

## Decisão de fronteira (a chave — rígido)
Este galho é **stack-agnóstico**: a TEORIA e ESTRATÉGIA de testes (o que testar, qual tipo, por quê).
O ferramental concreto JÁ tem dono e NÃO é reimplementado aqui — só linkado via callout/tabela:
- **Java** (JUnit 5, AssertJ, Mockito, Testcontainers, Spring Boot Test, MockMvc, WireMock, Awaitility,
  JQwik, PITest, JMH, REST-assured) → `[[Testes em Java]]` e o galho `03-Dominios/Tecnologia/Java/Testes/index`.
- **JavaScript/TS** (Vitest, Jest, Testing Library, MSW, Playwright, Cypress, fast-check) →
  `[[Testes em JavaScript]]`.
As notas raciocinam sobre conceitos; exemplos de código são ilustrativos e mínimos, sempre com o ponteiro
pro galho de stack que aprofunda o ferramental.

## Outras fronteiras (linka, não duplica)
- **Complexidade de Software** — testes como rede de segurança contra entropia/bit rot →
  `[[03-Dominios/Engenharia/Complexidade de Software/14 - Manutenção e evolução|Manutenção e evolução]]`
  forward-linka pra cá; aqui mencionamos a relação sem reescrever a tese.
- **OO / SOLID** — "código difícil de testar é código mal desenhado" (DIP, injeção de dependência) →
  `[[03-Dominios/Engenharia/SOLID/index|SOLID]]` / `[[03-Dominios/Engenharia/Orientação a Objetos/index|OO]]`.
- **Arquitetura** — hexagonal/ports&adapters como design testável → `[[Arquitetura de Software]]`.
- **Redes** — resiliência/chaos como teste de falha → `[[03-Dominios/Ciência/Redes e Protocolos/index|Redes]]`.

## Preservação (rígido) — experiências REAIS, relocadas do monólito ([[feedback-no-fabrication]])
- **Stack MedEspecialista** (JUnit 5 + AssertJ + Mockito + Testcontainers; suíte ~800 testes em ~3 min no
  GitHub Actions; "PR sem teste não é revisado") → **nota 15 (CI/CD)** + eco no capstone (filosofia).
- **TDD salvou** — regra de comissão com 5 condições; ao escrever o 5º teste percebeu abstração errada,
  refatorou sem medo → **nota 09 (TDD na prática)**.
- **TDD atrapalharia** — tela de cadastro com 30 campos/validações padrão; implementou direto + test-after
  focado em edge cases → **nota 09**.
- **Mock → Fake** — migrou de `@Mock UserRepository` com `when().thenReturn()` para `InMemoryUserRepository`
  com `HashMap`; mais legível, parou de quebrar em refactor → **nota 06 (comportamento, não implementação)**.
- **Flaky → Awaitility** — 3 testes flaky por race em código async; `Thread.sleep(500)` mascarou até o CI
  lento falhar; solução `Awaitility.await().atMost(...)`; regra "nunca sleep em teste" → **nota 11 (flaky)**.
- **Testcontainers vs H2** — PostgreSQL local "de teste" drift-ava de produção; Testcontainers deu Postgres
  idêntico ao de prod por PR, zero drift → **nota 07 (integração)**.

## Roster de notas (16; pode crescer/encolher por split)

### Iniciado
1. **O que são testes e por que testar** *(âncora)* — teste automatizado como programa que verifica programa;
   função estratégica (velocidade/refactor sem medo, spec executável, confiança de deploy, força bom design);
   as duas faces em entrevista (estratégia × técnica). Forward-link às vizinhas.
2. **A pirâmide de testes e suas variações** — unit/integração/E2E; pirâmide (Cohn) × troféu (Dodds) ×
   ampulheta (anti-pattern); "qual teste eu quero que falhe quando este bug aparecer?"; proporção por contexto.
3. **Anatomia de um bom teste** — AAA / Given-When-Then, naming (deve_X_quando_Y), um teste = uma razão pra
   falhar, F.I.R.S.T, sem lógica condicional, testes como documentação.
4. **Testes unitários** — unidade/isolamento/determinismo/independência; bom × ruim pra unit; fixtures,
   factories e object mothers (setup sem repetição).

### Adepto
5. **Test doubles: dummy, stub, spy, mock, fake** — a taxonomia de Meszaros (tabela); mock × stub
   (estado × interação); o que cada dublê resolve.
6. **Testar comportamento, não implementação** — state-based × interaction-based; over/under-mocking;
   por que fakes são subestimados (fake > mock); refactor-safety. *(exp real: mock → fake InMemoryRepository)*
7. **Testes de integração** — colaboração entre componentes reais (banco/fila/cache); Testcontainers como
   conceito; o drift do ambiente (H2 × Postgres real). *(exp real: Testcontainers vs H2)*
8. **TDD: o ciclo Red-Green-Refactor** — red (teste falha) → green (mínimo pra passar) → refactor (verde);
   o que TDD força (design antes, código testável, problema certo, feedback rápido).
9. **TDD na prática** — quando brilha (lógica não-trivial, bug fix com teste-primeiro, API pública, refactor)
   × quando atrapalha (exploração, glue trivial, UI visual); posição pragmática (test-after focado em edge
   cases). *(exp real: comissão 5 condições; tela 30 campos)*
10. **Técnicas de teste e edge cases** — caixa-preta × caixa-branca; equivalence partitioning, boundary
    value analysis, decision tables, state-transition testing; o checklist de edge cases (vazio/null/limites/
    overflow/unicode/timezone/datas/duplicatas/concorrência/recursos esgotados); testar o caminho de erro.
11. **Testes flaky** — causas (ordem/timing/estado compartilhado/datas/HashMap/rede/paralelismo); mitigações
    (isolar, `Clock` injetável, mocks de rede, container limpo, esperar condição não tempo); quarentena;
    "nunca `sleep` em teste". *(exp real: Awaitility)*

### Magus
12. **Coverage e mutation testing** — line/branch/method; 100% ≠ testado (coverage theater, asserções vazias);
    branch > line; alvo sensato (70–85%); mutation testing (PITest) como o complemento honesto ("seus testes
    realmente verificam algo?").
13. **Além do básico: property-based, snapshot, contract, smoke** — a "long tail" de tipos; property-based
    (declarar invariante, gerador acha contraexemplo); snapshot (e o risco do "aceite tudo"); contract
    (Pact/Spring Cloud Contract entre serviços); smoke (sinal de vida pós-deploy). Quando cada um vale.
14. **Performance, carga, caos e segurança** — microbenchmark (JMH) × load (k6/Gatling) × stress × chaos
    (Chaos Monkey); security tests (SAST/DAST/dependency scanning). O que cada um mede; para que maturidade.
15. **Testes em CI/CD** — a esteira (pre-commit → PR → main → deploy/smoke); paralelização, fail-fast,
    quarentena na esteira, não ignorar warnings; rapidez como requisito (pipeline lento = testes desligados).
    *(exp real: suíte ~800 testes/~3 min, "PR sem teste não é revisado")*
16. **Capstone: estratégia de testes em entrevista** — desenhar uma estratégia de testes pra um sistema dado;
    o checklist de edge cases consolidado; "How to explain in English" (monólogo preservado); vocabulário
    PT→EN; armadilhas consolidadas; recursos. *(eco da filosofia/stack real)*

## Padrão por nota (idêntico aos galhos anteriores)
- PT-BR, registro Feynman (analogias, perguntas retóricas, callouts, frases curtas, resumo em 1 linha);
  teto 2400 (permissão; código não conta). Banda honesta ~300–470 ln (capstone pode ir além).
- **3–5 diagramas Mermaid** por nota onde ajudam, cada um com lead-in + "leitura do diagrama". Bons para
  testes: `flowchart` (pirâmide/troféu, ciclo TDD red-green-refactor, decisão "qual teste/qual dublê",
  esteira CI/CD), `stateDiagram-v2` (state-transition testing), tabelas (test doubles, edge cases, coverage).
  **Sem `xychart-beta`** (não renderiza). Símbolos LITERAIS na prosa; entidades HTML SÓ em rótulos Mermaid
  entre aspas. Checar `[[` partido por quebra de linha e wikilink pra nota inexistente.
- **Seção final "Em entrevista"** — frases EN + vocabulário PT→EN.
- Fontes verificadas na web (WebSearch); callout `> [!info] Lastro` de honestidade.
- Atomicidade: linka vizinhas em vez de duplicar. `NN - Título.md` flat. `publish: false` nas notas;
  `publish: true` só no `index.md`. Frontmatter `fase:`, `type: concept`, `status: evergreen`, tags.
- **NUNCA fabricar** experiências/dados do usuário; preservar e relocar as 5 experiências reais (mapa acima).

## Tronco e MOC
- Pasta `03-Dominios/Engenharia/Testes/` com `index.md` (MOC, `type: moc`, `status: growing`,
  `publish: true`, agrupado por fase, rotas alternativas, dataview, "Veja também").
- Alias do `index.md`: **"Testes"** + **"Testes de Software"** + **"Testing"** + **"Testes Automatizados"**
  para resolver os ~9 links de entrada (Spring Boot, API Design, Senda Entrevistas, Testes em JavaScript,
  Complexidade/14, índice, README, Fundamentos/index, Fundamentos.md).
- A entrada Testes entra no MOC do domínio em DOIS arquivos: `Fundamentos/index.md` e `Fundamentos.md`
  (trocar a linha `[[Testes]]` por link ao `…/Testes/index`).

## Convenções de execução
- Subagent-driven, um subagente por nota, escrita em UMA chamada Write, house-style completo no prompt.
- Disparar por fase (Iniciado, Adepto, Magus), revisando armadilhas e commitando entre fases.
- Commits direto na main, SEM push, SEM Co-Authored-By ([[feedback-commits]]).

## Sequência de construção
1. Scaffold `Testes/index.md` + aliases. Commit.
2. Notas Iniciado (01–04), Adepto (05–11), Magus (12–16), uma por subagente. Relocar as experiências reais.
   Commit por fase.
3. Apontar os 2 MOCs do domínio ao galho.
4. `git rm` do monólito `Testes.md`; checar armadilhas; verificar alvos externos; fechar MOCs; atualizar
   memória `project-fundamentos-meta-plan` (marcar Testes COMPLETO → **Camada A FECHADA**).
