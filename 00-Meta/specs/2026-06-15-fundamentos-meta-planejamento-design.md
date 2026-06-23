---
title: "Meta-planejamento do domínio Fundamentos — roster de galhos"
created: 2026-06-15
type: spec
status: draft
publish: false
tags:
  - meta
  - spec
  - fundamentos
  - planejamento
---

# Meta-planejamento do domínio Fundamentos

## Contexto e objetivo

O domínio `03-Dominios/Ciência/` reúne os fundamentos de Ciência da Computação
e Engenharia de Software que **sobrevivem à troca de linguagem, framework ou stack**.
Hoje ele está exatamente onde a trilha Java estava antes dos galhos: seis notas
monolíticas, maduras (`evergreen`) mas planas, **todas no teto de ~600 linhas** — o
limite de divisão estabelecido para o vault.

Este spec é o **meta-planejamento do domínio**: não constrói nenhum galho, apenas
crava *quais* galhos o domínio terá, *como* se relacionam, *onde* ficam as fronteiras
com domínios vizinhos, e *em que ordem* serão desenvolvidos. Cada galho é, depois,
um sub-projeto próprio com seu ciclo de spec → plano → implementação.

**Objetivo do usuário:** o domínio é guiado pela lente de **foundation completa de CC**
(completude conceitual). A preparação para entrevistas de Senior Fullstack internacional
cai como **subconjunto natural** — a Fase 1 da `04-Sendas/Senda Entrevistas` ("o que
qualquer senior precisa articular com clareza") fica inteiramente coberta pela Camada A
abaixo. O critério de inclusão, porém, é completude do fundamento, não o que cai em
entrevista.

## Estado atual (ponto de partida)

Sob `03-Dominios/Ciência/`:

| Nota | Linhas | Status | Destino |
| --- | --- | --- | --- |
| Estruturas de Dados | 620 | evergreen | refatorar → galho 1 |
| Algoritmos | 601 | evergreen | refatorar → galho 2 |
| Orientação a Objetos | 554 | evergreen | refatorar → galho 3 |
| Banco de dados | 616 | evergreen | refatorar → galho 4 |
| Redes e Protocolos | 652 | evergreen | refatorar → galho 5 |
| Testes | 583 | evergreen | refatorar → galho 6 |
| O programa como teoria | 67 | evergreen | absorver → galho 12 |
| Abstrações que vazam | 134 | seedling | absorver → galho 12 |
| Dicionário de Fundamentos | — | seedling | transversal (mantém) |
| Fundamentos.md / index.md | — | moc | MOC do domínio (reescrever) |

Há ainda uma nota **Teoria do Sistema** registrada na memória como destinada a
Fundamentos (origem: cluster "O Lado Sombrio da IA") — também absorvida pelo galho 12.

## Princípios de estrutura

1. **Modelo de galhos (mesmo do Java):** galhos *flat* sob `03-Dominios/Ciência/`,
   cada galho = uma pasta dedicada de notas atômicas. Padrão tronco/galhos: o monólito
   é podado em sub-trilha de notas atômicas, com callouts no tronco apontando para os galhos.
2. **Três fases de aprendizado:** notas de cada galho organizadas em Iniciado / Adepto / Magus
   (júnior / pleno / senior), com frontmatter `fase:` e MOC do galho agrupado por fase.
3. **Notas atômicas:** dividir quando uma nota cobre 2+ tópicos ou passa de ~600 linhas.
4. **Regra de fronteira (anti-duplicação):** *o que já tem domínio próprio não entra em
   Fundamentos.* Fundamentos no máximo linka para a estante dona. Consequência direta:
   **Design Patterns** e **Arquitetura de Software** permanecem em `03-Dominios/Engenharia/Arquitetura/`
   (já existem lá); Fundamentos não os duplica.

## Roster de galhos

Todo o domínio é **planejado** — os 15 galhos abaixo entram na fila de execução das
próximas semanas. As camadas indicam natureza e sequência, não "agora vs. talvez".

### Camada A — refatorar monólitos existentes

Conteúdo maduro já existe (colher do monólito). São os interview-critical (Fase 1 da
Senda Entrevistas, marcados ★).

1. **Estruturas de Dados** ★ — COMPLETO (galho de 13 notas)
2. **Algoritmos** (inclui análise e complexidade) ★ — COMPLETO (galho de 14 notas)
3. **Orientação a Objetos** ★
4. **SOLID** ★ — *spin-off do galho OO (2026-06-17): SOLID virou galho próprio, irmão de OO.*
5. **Banco de Dados** ★
6. **Redes e Protocolos** ★
7. **Testes** ★

> Decisão (2026-06-17): ao refatorar o monólito de OO, **SOLID** foi extraído como galho
> próprio (8 notas), e não como sub-seção de OO — os cinco princípios rendem fundo e têm
> identidade didática própria. O galho OO mantém os 4 pilares, composição vs herança,
> acoplamento/coesão, modelagem tática (Entity/VO, Rich vs Anemic) e a divergência cross-language;
> linka para SOLID, Design Patterns e Arquitetura. Ver
> `2026-06-17-galho-orientacao-a-objetos-plan.md` e `2026-06-17-galho-solid-plan.md`.

### Camada B — novos galhos teóricos (sem casa em outro domínio)

7. **Paradigmas de Programação** — imperativo, OO, funcional, lógico, declarativo;
   imutabilidade, efeitos colaterais. (cai parcialmente em entrevista)
8. **Concorrência e Paralelismo** (conceitual) — race conditions, deadlock,
   mutex/semáforo, modelos (atores / CSP / memória compartilhada). Distinto do galho
   Java-específico de concorrência. ★
9. **Sistemas Operacionais** — processos, threads, scheduling, memória virtual, I/O,
   filesystems. (não colide com Infraestrutura, que é *usar* o SO, não a teoria) (parcial)
10. **Teoria da Computação** — autômatos, linguagens formais, computabilidade,
    complexidade P/NP. (raro em entrevista, fundamento real) (raro)
11. **Matemática para Computação** — matemática discreta: lógica, conjuntos, combinatória,
    grafos, probabilidade. (raro)

> Decisão: 10 e 11 são **dois galhos distintos**, não um. Matemática é ferramenta;
> Teoria da Computação é uma teoria sobre os limites do computável.

### Camada C — novo galho meta/autoral

12. **Complexidade de Software** — ver detalhamento abaixo. **Será o primeiro galho a
    ser implementado.** (parcial)

### Camada D — novos galhos (implementar depois dos demais)

13. **Organização de Computadores** — representação binária, arquitetura de von Neumann,
    hierarquia de memória, cache.
14. **Segurança Conceitual** — criptografia, hashing, autenticação/autorização (conceito).
15. **Compiladores e Linguagens** — análise léxica, parsing, AST, interpretação vs. compilação.

### Transversal

- **Dicionário de Fundamentos** — glossário do domínio (`type: glossary`), cresce junto
  com os galhos via `/verbete`.

## Galho 12 — Complexidade de Software (detalhamento)

### Decisão de nome

O galho foi inicialmente chamado de "Engenharia de Software", mas esse nome **promete
demais**: a disciplina inteira inclui processos, estimativa, requisitos, métricas, CI/CD
e testes — boa parte já mora em outro domínio (Testes = galho 6, CI/CD = Infraestrutura)
ou nem é fundamento. O nome reabriria a "gaveta de bugigangas".

A espinha real do galho é *o que torna software difícil de construir e manter, e como
raciocinamos sobre isso* — isto é, **complexidade**. Nome escolhido: **Complexidade de
Software** (aliases aceitáveis: "A Complexidade do Software", "Complexidade no Software").

**Teste de inclusão do galho:** *isso ajuda a entender ou gerenciar a complexidade do
software?* Se não responde, não entra.

**Linhagem canônica (ossatura):** Brooks, *No Silver Bullet* (essencial vs. acidental —
texto-âncora); Ousterhout, *A Philosophy of Software Design* (complexidade como
problema-raiz, carga cognitiva, deep modules); Moseley & Marks, *Out of the Tar Pit*
(complexidade do estado); Hickey, *Simple Made Easy* (simples ≠ fácil).

### Sub-eixos e assuntos

1. **Natureza & entendimento** — software como artefato sociotécnico; conhecimento tácito
   (Naur, `O programa como teoria`); **rendição cognitiva** (cruza com o cluster "O Lado
   Sombrio da IA" e com o projeto de blog "débito cognitivo").
2. **Complexidade essencial vs. acidental** — Brooks; *Out of the Tar Pit* (estado);
   simplicidade como valor (Hickey).
3. **Abstração & seus limites** — Lei das Abstrações Vazadas (Spolsky, `Abstrações que
   vazam`); deep vs. shallow modules (Ousterhout).
4. **Carga cognitiva & legibilidade** — carga cognitiva no código; princípio da menor
   surpresa; obscuridade; métricas (complexidade ciclomática — com ressalva de overlap leve).
5. **As dívidas** (eixo próprio) — débito técnico · **débito cognitivo** · débito de intenção.
6. **Decaimento, evolução & sistemas** — entropia de software / *bit rot* / *broken
   windows* / big ball of mud; manutenção e legado como gestão de complexidade no tempo;
   pensamento sistêmico, feedback, emergência (`Teoria do Sistema`); **Lei de Conway**.

### Migração de conteúdo

Ao construir o galho 12, três notas hoje soltas na raiz de Fundamentos são absorvidas
como notas-âncora dos sub-eixos: `O programa como teoria` (sub-eixo 1), `Abstrações que
vazam` (sub-eixo 3), `Teoria do Sistema` (sub-eixo 6). O MOC do domínio é atualizado para
apontá-las dentro do galho.

## Sequência de execução

Ordem aprovada (override da sugestão A-first):

1. **Camada C — galho 12 (Complexidade de Software)** — primeiro. Mais autoral, cruza
   com o blog de débito cognitivo e com o cluster do Lado Sombrio da IA.
2. **Camada A (galhos 1–6)** — refatoração dos monólitos; interview-critical e com
   conteúdo já disponível para colher.
3. **Camada B (galhos 7–11)** — construção teórica nova.
4. **Camada D (galhos 13–15)** — construção nova restante.

## Fora de escopo

- **Design Patterns** e **Arquitetura de Software** — permanecem em `03-Dominios/Engenharia/Arquitetura/`
  (regra anti-duplicação). System Design, API Design, Mensageria e Event Storming idem.
- Processos/metodologia (scrum, estimativa, requisitos) — não são fundamento stack-agnóstico;
  fora do galho 12 e do domínio.
- Implementação de qualquer galho — cada um é sub-projeto próprio (spec → plano → build).

## Critério de "pronto" deste meta-plano

Este spec está pronto quando: (a) a roster dos 15 galhos está cravada e aprovada;
(b) as fronteiras com Arquitetura/Infraestrutura estão registradas; (c) o nome e o
escopo do galho 12 estão definidos; (d) a sequência de execução está acordada. O próximo
passo concreto é abrir o sub-projeto do **galho 12 (Complexidade de Software)** com seu
próprio ciclo de brainstorm/plano.
