---
title: "Clássicos (GoF)"
created: 2026-07-28
updated: 2026-07-28
type: moc
status: growing
publish: true
tags:
  - moc
  - design-de-software
  - design-patterns
  - gof
aliases:
  - Clássicos GoF
  - Design Patterns GoF
  - Padrões GoF
  - Galho - Clássicos GoF
---

# Clássicos (GoF)

> [!abstract] TL;DR
> Os **23 padrões do Gang of Four** (1994) — criacionais, estruturais e comportamentais — tratados como **catálogo de consulta** para o sênior, com uma lente que a maioria dos tutoriais ignora: cada padrão em **Java, TypeScript, Python e Go**, mostrando como os recursos da linguagem mudam (ou **dissolvem**) a implementação, e uma seção **Armadilhas** reforçada sobre **quando NÃO usar**. Primeira família do galho-pai [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/index|Padrões de Projeto]].

## Sobre esta família

Este não é um curso linear: é um **repertório**. Cada nota é autocontida — dá para pular direto no padrão que você procura. As **fases** ordenam por *centralidade/frequência* (não por dificuldade): **Iniciado** = os que todo dev encontra primeiro; **Adepto** = o catálogo de trabalho do dia a dia; **Magus** = os situacionais mais a síntese de discernimento sênior.

**A lente do catálogo:** muitos padrões do GoF são contornos para lacunas das linguagens de 1994. Onde a linguagem moderna preenche a lacuna (funções de primeira classe, módulos, *pattern matching*, argumentos nomeados), o padrão encolhe — às vezes até sumir. Reconhecer isso é o que separa aplicar um padrão de empilhar cerimônia.

**Fronteiras (linka, não duplica):**
- **Princípios** que os padrões materializam → [[03-Dominios/Engenharia/Design de Software/SOLID/index|SOLID]] (OCP, DIP).
- **OO como craft** (encapsulamento, composição, polimorfismo) → [[03-Dominios/Engenharia/Design de Software/Orientação a Objetos/index|Orientação a Objetos]].
- **Padrões de acesso a dados, integração, apresentação, eventos e nuvem** → famílias irmãs no galho-pai.
- **Forma macro do sistema** (serviços, fronteiras) → [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura]].

## Iniciado — fundamentos e criacionais

1. [[01 - O que são Design Patterns]] — vocabulário, GoF, as 3 categorias, e a lente cross-linguagem do catálogo.
2. [[02 - Singleton]] — a instância única e por que é estado global disfarçado; o módulo/pacote como singleton nativo.
3. [[03 - Factory Method]] — delegar *qual classe* criar; a fábrica que encolhe para uma função.
4. [[04 - Abstract Factory]] — famílias de objetos que variam em bloco; o criacional mais raro em backend.
5. [[05 - Builder]] — objeto complexo passo a passo; named args / functional options tornam-no redundante.
6. [[06 - Prototype]] — criar clonando; cópia rasa vs profunda em cada linguagem.

## Adepto — estruturais e comportamentais de trabalho

**Estruturais:**
7. [[07 - Adapter]] — casar interfaces; tipagem estrutural (Go/TS) dissolve o adapter de declaração.
8. [[08 - Decorator]] — comportamento empilhável por composição; o `@` da linguagem é primo, não o mesmo.
9. [[09 - Facade]] — API simples sobre subsistema; o padrão que a linguagem *não* dissolve.
10. [[10 - Proxy]] — controlar acesso; a base da AOP e a pegadinha do `@Transactional` interno.
11. [[11 - Composite]] — árvore parte-todo; OO vs tipo-soma funcional.

**Comportamentais:**
12. [[12 - Strategy]] — algoritmos intercambiáveis; o caso-ouro de "vira função".
13. [[13 - Observer]] — notificação um-para-muitos; base do event-driven.
14. [[14 - Command]] — requisição como objeto; enfileirar, logar, desfazer.
15. [[15 - Template Method]] — esqueleto por herança; Go funde com Strategy.
16. [[16 - State]] — comportamento por estado interno; FSM vs enum/sealed.
17. [[17 - Chain of Responsibility]] — cadeia de handlers; a base do middleware.
18. [[18 - Iterator]] — percorrer sem expor; o padrão mais absorvido pelas linguagens.

## Magus — situacionais e síntese

19. [[19 - Mediator]] — coordenar interações entre colegas; teia N² → estrela.
20. [[20 - Visitor]] — operações sem tocar os tipos; o caso-ouro que *pattern matching* aposenta.
21. [[21 - Padrões raros (Bridge, Flyweight, Memento, Interpreter)]] — os quatro que a prática quase aposentou, e onde ainda vivem.
22. [[22 - Reconhecer GoF nos frameworks]] — os padrões que você já usa sem perceber (Spring/JPA).
23. [[23 - Quando NÃO usar - anti-patterns e discernimento sênior]] — a síntese: partir do problema, não do padrão.

## Rotas alternativas

### Entrevista internacional
01 → 12 (Strategy) → 10 (Proxy) → 22 (frameworks) → 23 (quando não usar). O vocabulário, o padrão que mais cai, o que o framework aplica, e o discernimento sênior.

### Só os criacionais
01 → 02 → 03 → 04 → 05 → 06. A primeira família inteira, na ordem.

## Veja também

- [[03-Dominios/Engenharia/Design de Software/index|Design de Software]] — o domínio.
- [[03-Dominios/Engenharia/Design de Software/SOLID/index|SOLID]] · [[03-Dominios/Engenharia/Design de Software/Orientação a Objetos/index|Orientação a Objetos]]
