---
title: "SOLID"
created: 2026-06-17
updated: 2026-06-17
type: moc
status: growing
publish: true
tags:
  - engenharia
  - solid
  - orientacao-a-objetos
  - entrevista
  - moc
aliases:
  - SOLID
  - Princípios SOLID
  - SOLID Principles
  - Galho - SOLID
---

# SOLID

> [!abstract] TL;DR
> Galho de Engenharia sobre os cinco princípios de design orientado a objetos — **S**RP, **O**CP, **L**SP, **I**SP, **D**IP — que, aplicados juntos, levam a código flexível, testável e evolutivo. Não são regras religiosas: são **heurísticas cujas exceções você deve conhecer**. Interview-critical.

## Sobre este galho

Spin-off do galho [[03-Dominios/Engenharia/Design de Software/Orientação a Objetos/index|Orientação a Objetos]]: os cinco princípios de Robert C. Martin (Uncle Bob) rendem fundo o suficiente para terem galho próprio. A meta comum dos cinco é **baixo acoplamento e alta coesão** — por isso o galho referencia [[08 - Acoplamento e coesão]] (no galho OO), que é seu pré-requisito conceitual.

**Fronteiras (linka, não duplica):**
- **SOLID aplicado à arquitetura** (nível módulo/serviço) → [[Arquitetura de Software]]. Aqui é o nível objeto/classe.
- **Design Patterns** → [[Design Patterns]]. OCP e DIP usam patterns como exemplo; não ensinamos o catálogo.

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista" com frases prontas em inglês e vocabulário técnico.

## Iniciado — o princípio e os dois primeiros

1. [[01 - O que é SOLID]] — cinco heurísticas (não dogma), história (Uncle Bob), a meta comum.
2. [[02 - SRP - Responsabilidade Única]] — uma única razão para mudar; eixos de mudança.
3. [[03 - OCP - Aberto-Fechado]] — aberto para extensão, fechado para modificação; switch vs polimorfismo.

## Adepto — os três últimos

4. [[04 - LSP - Substituição de Liskov]] — subtipos substituíveis; design by contract; Rectangle/Square.
5. [[05 - ISP - Segregação de Interfaces]] — várias interfaces pequenas vs uma grande.
6. [[06 - DIP - Inversão de Dependência]] — depender de abstrações; inverter a seta de dependência.

## Magus — aplicação e crítica

7. [[07 - DIP na prática - DI e IoC]] — injeção de dependência, Inversão de Controle, containers, testabilidade.
8. [[08 - SOLID em xeque]] — over-engineering, SOLID vs simplicidade (Ousterhout), SOLID na arquitetura, em entrevista.

## Rotas alternativas

### Entrevista internacional
01 → 02 → 06 → 07 → 08. O acrônimo, o SRP, a inversão de dependência, DI na prática e a leitura crítica.

### Os cinco em ordem
01 → 02 → 03 → 04 → 05 → 06. Um princípio por nota, na ordem do acrônimo.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Engenharia/Design de Software/SOLID"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Ciência/index|Fundamentos (MOC do domínio)]]
- [[03-Dominios/Engenharia/Design de Software/Orientação a Objetos/index|Orientação a Objetos]] — os pilares e o design OO que SOLID refina
- [[08 - Acoplamento e coesão]] — a meta que os cinco princípios perseguem
- [[Arquitetura de Software]] — SOLID no nível de módulo e serviço
- [[Design Patterns]] — padrões que materializam OCP e DIP
- [[Dicionário de Ciência da Computação]]
