---
title: "Padrões de Projeto"
created: 2026-07-28
updated: 2026-07-28
type: moc
status: growing
publish: true
tags:
  - moc
  - design-de-software
  - design-patterns
  - padroes-de-projeto
aliases:
  - Padrões de Projeto
  - Design Patterns
  - Catálogo de Padrões
  - Padrões de Projeto (catálogo)
---

# Padrões de Projeto

> [!abstract] TL;DR
> Um **catálogo de consulta** de padrões de projeto e de arquitetura de aplicação, para o sênior de
> plantão — inclusive (e especialmente) em **sistemas legados**. Não é uma trilha linear: é um
> repertório onde se **procura** um padrão. Cada nota é **autocontida**, mostra o padrão em **Java,
> TypeScript, Python e Go** (comentando como a linguagem muda ou **dissolve** o padrão) e traz uma
> seção **Armadilhas** reforçada sobre **quando NÃO usar** — o ângulo que quase ninguém cobre.

## Sobre este galho

Os padrões estão organizados em **famílias**, por fonte e por escala. A primeira — os 23 clássicos do
Gang of Four — está completa; as demais são construídas em sequência. Como é catálogo de consulta,
alguma **redundância** com outros galhos do vault (Comunicação, Cloud, Operação) é aceitável e
desejada: o catálogo não pode depender de galhos que evoluem em ritmo próprio.

> Este índice é o herdeiro do antigo monólito `Design Patterns.md` (aposentado em 2026-07-28). O
> alias **Design Patterns** resolve para cá.

## Famílias

| # | Família | Fonte | Estado |
| --- | --- | --- | --- |
| 1 | [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Clássicos (GoF)/index\|Clássicos (GoF)]] | Gang of Four (1994) | ✅ **completa** — 23 notas |
| 2 | [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Acesso a Dados/index\|Acesso a Dados]] | Fowler PoEAA + J2EE + NoSQL/cloud | ✅ **completa** — 15 notas |
| 3 | [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Integração Empresarial (EIP)/index\|Integração Empresarial (EIP)]] | Hohpe & Woolf | ✅ **completa** — 14 notas |
| 4 | **Aplicação Corporativa** | Fowler PoEAA (não-dados) | ⬜ planejada (~14) |
| 5 | **Arquitetura de Eventos** | EDA moderna | ⬜ planejada (~10) |
| 6 | **Nuvem e Resiliência** | Azure/AWS Cloud Design Patterns | ⬜ planejada (~14) |

Estado detalhado e rosters em [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/roadmap|roadmap do galho-pai]].

## A lente do catálogo

Muitos padrões do GoF são contornos para lacunas das linguagens de 1994. Onde a linguagem moderna
preenche a lacuna — funções de primeira classe (Strategy vira função), *pattern matching* (mata o
Visitor), módulos (o Singleton evapora), argumentos nomeados (dispensa o Builder) —, o padrão
**encolhe**, às vezes até sumir. E o outro lado: o **framework** frequentemente já implementou o
padrão por você (`@Transactional` é Proxy, `@Service` é Facade). Reconhecer os dois movimentos é o
que separa aplicar um padrão de empilhar cerimônia.

**Comece por:** [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Clássicos (GoF)/01 - O que são Design Patterns|O que são Design Patterns]].

## Fronteiras (linka, não duplica)

- **Princípios** que os padrões materializam → [[03-Dominios/Engenharia/Design de Software/SOLID/index|SOLID]] (OCP, DIP).
- **OO como craft** → [[03-Dominios/Engenharia/Design de Software/Orientação a Objetos/index|Orientação a Objetos]].
- **Forma macro do sistema** (serviços, fronteiras) → [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura]].

## Recursos

### Livros
- *Design Patterns: Elements of Reusable Object-Oriented Software* — Gamma, Helm, Johnson, Vlissides (GoF, o clássico dos 23).
- *Head First Design Patterns* — Freeman & Robson (acessível, didático).
- *Patterns of Enterprise Application Architecture* — Martin Fowler (padrões de aplicação, base das famílias 2 e 4).
- *Enterprise Integration Patterns* — Hohpe & Woolf (base da família 3).
- *Refactoring* — Martin Fowler (quando aplicar padrões via refactoring).
- *Effective Java* — Joshua Bloch (Item 1 static factory; Item 2 Builder; Item 3 Singleton; Item 13 clone).

### Online
- [Refactoring Guru — Design Patterns](https://refactoring.guru/design-patterns) — catálogo visual com exemplos em várias linguagens.
- [Source Making — Design Patterns](https://sourcemaking.com/design_patterns) — descrições práticas.
- [Azure Architecture — Cloud Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/) — base da família 6.

## Veja também

- [[03-Dominios/Engenharia/Design de Software/index|Design de Software]] — o domínio.
- [[03-Dominios/Engenharia/Design de Software/SOLID/index|SOLID]] · [[03-Dominios/Engenharia/Design de Software/Orientação a Objetos/index|Orientação a Objetos]]
- [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura]] — a forma macro do sistema.
