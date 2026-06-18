---
title: "Galho Paradigmas de Programação — design e plano (Fundamentos, Camada B)"
created: 2026-06-18
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - paradigmas
---

# Galho Paradigmas de Programação — design e plano

## Contexto
PRIMEIRO galho da Camada B do meta-plano de Fundamentos
(`2026-06-15-fundamentos-meta-planejamento-design.md`), depois da Camada A inteira FECHADA (7 galhos,
2026-06-18). Diferente da Camada A, **NÃO há monólito nem semente solta** — é construção teórica NOVA.
Escopo do spec-mãe (galho 7): "imperativo, OO, funcional, lógico, declarativo; imutabilidade, efeitos
colaterais. (cai parcialmente em entrevista)". Roster aprovado pelo usuário em 2026-06-18 (expandido p/ 16).

## Decisão de fronteira (a chave — rígido, anti-duplicação)
- **OO já tem galho próprio** (`03-Dominios/Fundamentos/Orientação a Objetos/`). Aqui OO entra como **um
  paradigma entre vários** (objetos = estado + mensagens; como se compara ao imperativo e ao funcional) —
  **linka [[Orientação a Objetos]]** pros 4 pilares, NÃO os reensina.
- **Concorrência conceitual** será galho próprio (Camada B, galho 8, ainda NÃO existe). Atores/CSP/memória
  compartilhada NÃO são aprofundados aqui — só mencionados em PROSA (sem wikilink quebrado), ligando
  imutabilidade ↔ concorrência. O paralelismo aparece como *benefício* da pureza, não como tema.
- **Programação Reativa** tem galho Java próprio → **linka [[Programação Reativa]]**; aqui fica o conceito
  de paradigma reativo/dataflow, não o ferramental (Reactor/WebFlux).
- **Funcional no Java/TS** → linka `[[03-Dominios/Java/Collections e Streams/index|Streams]]` e
  `[[TypeScript]]` pro ferramental concreto; o galho é stack-agnóstico.
- **SOLID** → linka `[[SOLID]]`. **Complexidade de Software** (simplicidade, raciocínio sobre estado) →
  linka `[[Complexidade de Software]]`.

## Roster de notas (16; expandido de 13 a pedido do usuário)

### Iniciado — o mapa e os mundos base
1. **O que é um paradigma de programação** *(âncora)* — paradigma = modelo mental / conjunto de conceitos,
   NÃO linguagem; linguagens são multi-paradigma; a grande divisão imperativo × declarativo; por que molda
   como você pensa o problema. Forward-link às vizinhas.
2. **O paradigma imperativo** — estado mutável + comandos + controle de fluxo; modelo de von Neumann;
   procedural / programação estruturada (Dijkstra, "Go To Statement Considered Harmful"); o paradigma default.
3. **O paradigma orientado a objetos** — OO *como paradigma* (estado + troca de mensagens, abstração de
   dados, Alan Kay); como se relaciona ao imperativo. **Linka [[Orientação a Objetos]]**; não reensina pilares.
4. **O paradigma declarativo** — dizer O QUE, não COMO; o guarda-chuva (funcional, lógico, SQL, HTML/CSS,
   config, build tools); o motor decide o como. Liga com a face declarativa do SQL ([[Banco de Dados]]).

### Adepto — o mergulho funcional (o paradigma que mais "cai" hoje)
5. **O paradigma funcional** — funções como cidadãs de primeira classe, HOF, funções como valores; por que
   FP saiu do nicho e virou mainstream. A essência (os recursos vêm nas notas seguintes).
6. **Composição e recursão** — composição de funções (pipe/compose), estilo point-free, recursão como fluxo
   de controle, tail-call, fold/reduce como o "motor" que substitui o loop.
7. **Funções puras e efeitos colaterais** — pureza, transparência referencial; por que pureza facilita
   raciocínio, teste e paralelismo; o problema dos efeitos colaterais; empurrar efeitos pra borda
   (functional core / imperative shell).
8. **Imutabilidade e estado** — dados imutáveis, structural sharing, persistent data structures; por que
   imutabilidade mata classes de bug (aliasing, e ajuda concorrência — menção em prosa); o custo e como
   linguagens otimizam.
9. **Avaliação preguiçosa, currying e aplicação parcial** — lazy evaluation, thunks, streams infinitas;
   currying / aplicação parcial; como esses recursos mudam o que dá pra expressar.
10. **Tipos algébricos, pattern matching e erros sem exceção** — ADTs (sum/product types), pattern matching
    exaustivo, Option/Maybe e Either/Result (erro sem null/exceção), railway-oriented programming; o
    "M-word" (monad) explicado sem susto (Option/Either já são mônadas).

### Magus — os outros estilos, os tipos e a síntese
11. **O paradigma lógico** — fatos + regras + unificação + backtracking (Prolog); declarativo levado ao
    extremo; onde aparece hoje (Datalog, constraint solving, inferência de tipos, regras de negócio).
12. **Programação reativa e dataflow** — streams/observables, FRP, propagação automática de mudança;
    push × pull; **linka [[Programação Reativa]]**; quando o estilo reativo vale (e quando complica).
13. **Sistemas de tipos** *(eixo transversal, não um paradigma)* — estático × dinâmico, inferência, forte ×
    fraca, nominal × estrutural, gradual typing; como o sistema de tipos sustenta cada paradigma (FP ama
    tipos ricos). Linka `[[TypeScript]]` e a estante Java.
14. **Linguagens multi-paradigma** — Java/JS/Python/Scala/Rust/Kotlin misturam estilos; o paradigma é
    escolha por problema, não por linguagem; "paradigma é ferramenta, não religião".
15. **Programação funcional na prática** — map/filter/reduce, imutabilidade por padrão, pipelines; como um
    time imperativo adota FP gradualmente; armadilhas (over-abstração, performance, dogmatismo).
16. **Capstone: paradigmas na prática e em entrevista** — escolher o paradigma por problema, comparar os
    estilos, "How to explain in English", vocabulário PT→EN, armadilhas consolidadas, recursos.

## Padrão por nota (idêntico aos galhos da Camada A)
- PT-BR, registro Feynman (analogias, perguntas retóricas, callouts, frases curtas, resumo em 1 linha);
  teto 2400 (permissão; código não conta). Banda honesta ~300–470 ln.
- **3–5 diagramas Mermaid** por nota onde ajudam, cada um com lead-in + "leitura do diagrama". Bons aqui:
  `flowchart` (imperativo × declarativo, composição de funções, functional core/imperative shell, árvore de
  decisão de paradigma), `sequenceDiagram` (push × pull reativo, unificação Prolog), `stateDiagram-v2`
  (mutável × imutável), tabelas (comparação de paradigmas, tipos). **Sem `xychart-beta`**. Símbolos LITERAIS
  na prosa; entidades HTML SÓ em rótulos Mermaid entre aspas. Exemplos de código em múltiplas linguagens
  são ilustrativos e mínimos (e NÃO contam no limite).
- **Seção final "Em entrevista"** — frases EN + vocabulário PT→EN. (Galho é "parcial" em entrevista, mas
  mantém a seção para consistência.)
- Fontes verificadas na web (WebSearch); callout `> [!info] Lastro` de honestidade.
- Atomicidade: linka vizinhas em vez de duplicar. `NN - Título.md` flat. `publish: false` nas notas;
  `publish: true` só no `index.md`. Frontmatter `fase:`, `type: concept`, `status: evergreen`, tags.
- **NUNCA fabricar** experiências/dados do usuário. ESTE galho é teórico — provavelmente NÃO usa experiências
  em 1ª pessoa (não há monólito com elas). Se um exemplo precisar de contexto, use cenário genérico, nunca
  invente cliente/projeto real ([[feedback-no-fabrication]]).

## Tronco e MOC
- Pasta `03-Dominios/Fundamentos/Paradigmas/` com `index.md` (MOC, `type: moc`, `status: growing`,
  `publish: true`, agrupado por fase, rotas alternativas, dataview, "Veja também").
- Alias do `index.md`: **"Paradigmas"** + **"Paradigmas de Programação"** + **"Programming Paradigms"** +
  **"Paradigmas de programação"**. (Galho novo — sem links de entrada a herdar, mas alias prepara o terreno.)
- Entra no MOC do domínio em DOIS arquivos: `Fundamentos/index.md` e `Fundamentos.md` (adicionar a linha;
  hoje não há entrada de Paradigmas).

## Convenções de execução
- Subagent-driven, um subagente por nota, escrita em UMA chamada Write, house-style completo no prompt.
- Disparar por fase (Iniciado, Adepto, Magus), revisando armadilhas e commitando entre fases.
- Commits direto na main, SEM push, SEM Co-Authored-By ([[feedback-commits]]).

## Sequência de construção
1. Scaffold `Paradigmas/index.md` + aliases. Commit.
2. Notas Iniciado (01–04), Adepto (05–10), Magus (11–16), uma por subagente. Commit por fase.
3. Adicionar a entrada no MOC do domínio (`Fundamentos/index.md` + `Fundamentos.md`).
4. Checar armadilhas; verificar alvos externos; verificar NN-links internos; atualizar memória
   `project-fundamentos-meta-plan` (Camada B iniciada, Paradigmas COMPLETO). Próximo: Concorrência conceitual (★).
