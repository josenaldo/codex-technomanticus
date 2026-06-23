---
title: "Orientação a Objetos"
created: 2026-06-17
updated: 2026-06-17
type: moc
status: growing
publish: true
tags:
  - fundamentos
  - orientacao-a-objetos
  - entrevista
  - moc
aliases:
  - Orientação a Objetos
  - Orientação a objetos
  - OO
  - OOP
  - Object-Oriented Programming
  - Galho - Orientação a Objetos
---

# Orientação a Objetos

> [!abstract] TL;DR
> Galho de Fundamentos sobre o paradigma que organiza software em **objetos** que encapsulam estado
> e comportamento e colaboram por mensagens. O diferencial de um senior não é recitar os quatro
> pilares — é demonstrar **quando aplicar, quando não aplicar**, reconhecer anti-patterns, e saber
> que o modelo OO **muda de forma** conforme a linguagem. Interview-critical.

## Sobre este galho

Este galho é o dono dos **fundamentos de OO**: os quatro pilares (encapsulamento, abstração,
herança, polimorfismo), interfaces e classes abstratas, **composição sobre herança**, acoplamento e
coesão, a modelagem tática de objetos (identidade/igualdade, imutabilidade, Rich vs Anemic Domain
Model), os anti-patterns clássicos, e como o paradigma diverge entre linguagens.

**Fronteiras (linka, não duplica):**
- **SOLID** tem galho próprio → [[03-Dominios/Engenharia/SOLID/index|SOLID]]. Aqui fica
  `Acoplamento e coesão` (08), que o SOLID referencia.
- **Design Patterns** (catálogo GoF) → [[Design Patterns]]. Aqui ensinamos o *material bruto*
  (composição + polimorfismo), não os padrões nomeados.
- **DDD estratégico** (Aggregate, Bounded Context, Domain Event) → [[Arquitetura de Software]]. Aqui
  fica só a modelagem **tática** de objeto.

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção
"Em entrevista" com frases prontas em inglês e vocabulário técnico.

## Iniciado — objetos, classes e os pilares

1. [[01 - O que é Orientação a Objetos]] — objeto (estado/comportamento/identidade), mensagens (Alan Kay) vs classes, classe/objeto/instância.
2. [[02 - Encapsulamento]] — esconder estado, interface pública, invariantes; getter/setter como encapsulamento falso.
3. [[03 - Abstração]] — modelar pelo que faz, não como; níveis de abstração; abstração ≠ interface.
4. [[04 - Herança]] — is-a, override, fragile base class, acoplamento; hierarquias rasas.
5. [[05 - Polimorfismo]] — subtipo/late binding, paramétrico (generics), ad-hoc (overload); dynamic dispatch.

## Adepto — interfaces, composição e design

6. [[06 - Interfaces e classes abstratas]] — contrato vs implementação parcial; tipagem nominal vs estrutural.
7. [[07 - Composição sobre herança]] — has-a vs is-a, delegação, quando herança serve.
8. [[08 - Acoplamento e coesão]] — baixo acoplamento, alta coesão, Law of Demeter, Tell Don't Ask.

## Magus — modelagem rica, paradigma e síntese

9. [[09 - Identidade, igualdade e imutabilidade]] — Entity vs Value Object, contrato equals/hashCode, imutabilidade.
10. [[10 - Rich vs Anemic Domain Model]] — comportamento junto dos dados; DDD tático vs estratégico.
11. [[11 - Como o modelo OO difere entre linguagens]] — Go sem herança, Python MRO, JS prototypes, nominal vs estrutural.
12. [[12 - Anti-patterns de OO]] — God Class, Anemic, Feature Envy, Primitive Obsession, Refused Bequest.
13. [[13 - OO na prática e em entrevista]] — OO como ferramenta não religião, armadilhas, prep bilíngue, cheat-sheet.

## Rotas alternativas

### Entrevista internacional
01 → 02 → 04 → 05 → 07 → 10 → 13. Os pilares que sempre caem, composição, modelo rico e o capstone.

### Os quatro pilares
01 → 02 → 03 → 04 → 05. A fundação conceitual em ordem.

### Design pragmático
06 → 07 → 08 → 12. Interfaces, composição, acoplamento/coesão e os anti-patterns a evitar.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Engenharia/Orientação a Objetos"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Ciência/index|Fundamentos (MOC do domínio)]]
- [[03-Dominios/Engenharia/SOLID/index|SOLID]] — os cinco princípios de design OO
- [[Design Patterns]] — o catálogo GoF construído sobre estes fundamentos
- [[Arquitetura de Software]] — DDD estratégico e SOLID no nível de módulo/serviço
- [[Dicionário de Fundamentos]]
