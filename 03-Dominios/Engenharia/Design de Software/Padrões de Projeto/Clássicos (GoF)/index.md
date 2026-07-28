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
> Os **23 padrões do Gang of Four** (1994) — criacionais, estruturais e comportamentais —
> tratados como **catálogo de consulta** para o sênior, com uma lente que a maioria dos tutoriais
> ignora: cada padrão em **Java, TypeScript, Python e Go**, mostrando como os recursos da linguagem
> mudam (ou **dissolvem**) a implementação, e uma seção **Armadilhas** reforçada sobre **quando NÃO
> usar**. Primeira família do galho-pai [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/roadmap|Padrões de Projeto]].

## Sobre esta família

Este não é um curso linear: é um **repertório**. Cada nota é autocontida — dá para pular direto no
padrão que você procura. As **fases** ordenam por *centralidade/frequência* (não por dificuldade):
**Iniciado** = os que todo dev encontra primeiro; **Adepto** = o catálogo de trabalho do dia a dia;
**Magus** = os situacionais mais a síntese de discernimento sênior.

**A lente do catálogo:** muitos padrões do GoF são contornos para lacunas das linguagens de 1994.
Onde a linguagem moderna preenche a lacuna (funções de primeira classe, módulos, *pattern matching*,
argumentos nomeados), o padrão encolhe — às vezes até sumir. Reconhecer isso é o que separa aplicar
um padrão de empilhar cerimônia.

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

*Em construção.* Estruturais (Adapter, Decorator, Facade, Proxy, Composite) e comportamentais de uso
diário (Strategy, Observer, Command, Template Method, State, Chain of Responsibility, Iterator).

## Magus — situacionais e síntese

*Em construção.* Mediator, Visitor, os padrões raros (Bridge/Flyweight/Memento/Interpreter),
reconhecer GoF nos frameworks e a síntese "quando NÃO usar".

## Rotas alternativas

### Entrevista internacional
01 → 12 (Strategy) → 10 (Proxy) → 22 (frameworks) → 23 (quando não usar). O vocabulário, o padrão que mais cai, o que o framework aplica, e o discernimento sênior.

### Só os criacionais
01 → 02 → 03 → 04 → 05 → 06. A primeira família inteira, na ordem.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Clássicos (GoF)"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/roadmap|Padrões de Projeto]] — o galho-pai e as outras cinco famílias.
- [[03-Dominios/Engenharia/Design de Software/index|Design de Software]] — o domínio.
- [[03-Dominios/Engenharia/Design de Software/SOLID/index|SOLID]] · [[03-Dominios/Engenharia/Design de Software/Orientação a Objetos/index|Orientação a Objetos]]
