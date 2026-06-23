---
title: "Complexidade de Software"
created: 2026-06-16
updated: 2026-06-16
type: moc
status: growing
publish: true
tags:
  - engenharia
  - complexidade-de-software
  - moc
aliases:
  - Complexidade de Software
  - Galho 12 - Complexidade de Software
  - A Complexidade do Software
---

# Complexidade de Software

> [!abstract] TL;DR
> Galho 12 de Engenharia. O estudo daquilo que torna software difícil de construir e
> manter — complexidade essencial vs. acidental, os limites da abstração, carga cognitiva,
> as três dívidas (técnica, cognitiva, intenção) e o decaimento dos sistemas no tempo. A
> espinha: *o que ajuda a entender ou gerenciar a complexidade do software?*

## Sobre este galho

Cobre a complexidade como o problema central do software, de ponta a ponta: por que software
é difícil (Brooks, Tar Pit, Hickey, Naur), os mecanismos com que a gerenciamos e onde eles
falham (abstração, information hiding, módulos, carga cognitiva), as três dívidas do Triple
Debt Model (Storey) e a gestão da complexidade no tempo e no todo (entropia, manutenção,
pensamento sistêmico, Lei de Conway).

**Não cobre:** Design Patterns e estilos arquiteturais (ficam em [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura]]);
as manifestações AI-specific dos débitos (ficam em [[03-Dominios/Tecnologia/IA/O Lado Sombrio da IA/index|O Lado Sombrio da IA]],
sob a lente da IA — este galho trata sob a lente geral/atemporal, cross-linkado).

## Iniciado

1. [[01 - A complexidade como problema central]] — a dificuldade-raiz do software; Brooks, No Silver Bullet.
2. [[02 - Complexidade essencial vs. acidental]] — a distinção de Brooks; estado e Out of the Tar Pit.
3. [[03 - Simplicidade não é facilidade]] — Hickey, Simple Made Easy; complecting.
4. [[04 - O programa como teoria]] — Naur, theory-building; conhecimento tácito.

## Adepto

5. [[05 - Abstração - a ferramenta central]] — information hiding (Parnas); esconder decisões voláteis.
6. [[06 - Abstrações que vazam]] — Spolsky, Lei das Abstrações Vazadas; Lei de Hyrum.
7. [[07 - Módulos profundos e rasos]] — Ousterhout, A Philosophy of Software Design.
8. [[08 - Carga cognitiva e legibilidade]] — cognitive load; menor surpresa; obscuridade.
9. [[09 - As três dívidas do software]] — Triple Debt Model (Storey): técnica/cognitiva/intenção.
10. [[10 - Dívida técnica]] — Cunningham; juros; atalhos no código.
11. [[11 - Dívida cognitiva]] — erosão do entendimento compartilhado (perspectiva geral).
12. [[12 - Dívida de intenção]] — Storey/Osmani/Fowler; externalizar rationale.

## Magus

13. [[13 - Entropia de software e decaimento]] — bit rot, broken windows, big ball of mud.
14. [[14 - Manutenção e evolução]] — legado como gestão de complexidade no tempo.
15. [[15 - Pensamento sistêmico]] — feedback, emergência, parte vs. todo.
16. [[16 - Lei de Conway]] — complexidade organizacional ↔ arquitetural.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Engenharia/Complexidade de Software"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Ciência/index|Fundamentos (MOC do domínio)]]
- [[03-Dominios/Tecnologia/IA/O Lado Sombrio da IA/index|O Lado Sombrio da IA]] — os débitos sob a lente da IA
- [[Dicionário de Ciência da Computação]]
