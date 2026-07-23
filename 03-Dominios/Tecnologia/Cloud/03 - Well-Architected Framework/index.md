---
title: "Cloud — Well-Architected Framework"
created: 2026-07-20
updated: 2026-07-23
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
aliases:
  - "Well-Architected Framework"
  - "Galho 3 - Well-Architected Framework"
---

# Well-Architected Framework

> [!abstract] TL;DR
> Galho 3 da trilha Cloud, Bloco 1: a bússola de critério arquitetural que atravessa o domínio inteiro. Os seis pilares do AWS Well-Architected Framework — excelência operacional, segurança, confiabilidade, eficiência de performance, otimização de custo e sustentabilidade — e o fato central que fecha o galho: os pilares se contradizem entre si, e arquitetar é escolher deliberadamente qual cede terreno para qual. 7 notas, 2 fases.

## Sobre este galho

Formalizado pela AWS em 2015 a partir de práticas internas que já rodavam desde 2012, o Well-Architected Framework não é uma lista de conformidade — é um conjunto de perguntas que uma review de arquitetura deveria fazer, pilar por pilar, antes de declarar um desenho pronto. Este galho percorre os seis pilares um a um: como o time opera e evolui o sistema, como identidade e defesa em profundidade substituem o perímetro físico, o que separa durabilidade de disponibilidade, como medir performance em vez de teorizar sobre ela, como tornar custo uma variável de design e não um item de planilha trimestral, e — no pilar mais recente, adicionado em 2021 — como right-sizing e escolha de região também são decisões de sustentabilidade. A última nota fecha o galho com o assunto mais valioso dele: os seis pilares puxam a arquitetura em direções que se contradizem, e um arquiteto sênior escolhe e documenta o trade-off, não finge que dá para maximizar todos ao mesmo tempo.

**Audiência primária:** quem já tem a mecânica dos Galhos 1-2 e precisa do critério para avaliar (ou defender) uma arquitetura em revisão. **Audiência secundária:** quem se prepara para entrevista de arquitetura em nuvem — os seis pilares são vocabulário-padrão de entrevista técnica sênior.

Este galho é a bússola conceitual; a aplicação prática de cada pilar em serviços concretos vem nos Blocos 2-5. A identidade — pilar de Segurança em ação — é aprofundada no [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Galho 4]].

## Iniciado

1. [[01 - Por que existe um framework de arquitetura|01 — Por que existe um framework de arquitetura]] — origem em 2015, os seis pilares, a review sem culpa.

## Adepto

2. [[02 - Excelência operacional|02 — Excelência operacional]] — arquitetura desenhada para ser operada, observada e mudada com segurança.
3. [[03 - Segurança|03 — Segurança]] — identidade como o novo perímetro, os sete princípios de design.
4. [[04 - Confiabilidade|04 — Confiabilidade]] — recuperação automática, durabilidade vs disponibilidade.
5. [[05 - Eficiência de performance|05 — Eficiência de performance]] — medir vence teorizar; viés de familiaridade como inimigo do pilar.
6. [[06 - Otimização de custo|06 — Otimização de custo]] — custo como variável visível e deliberada do design, não corte reativo.

## Magus

7. [[07 - Sustentabilidade e os trade-offs entre pilares|07 — Sustentabilidade e os trade-offs entre pilares]] — o sexto pilar (2021) e a tensão irredutível entre os seis. Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06 → 07. Percurso linear recomendado — cada pilar se apoia no vocabulário do anterior.

### Prep de entrevista — só os seis pilares

01 (skim) → 03 → 04 → 06 → 07 (os pilares mais cobrados em entrevista de arquitetura, e o trade-off entre eles é a resposta que separa sênior de pleno).

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/01 - O que é a nuvem, de verdade/index|O que é a nuvem, de verdade]] — Galho 1
- [[03-Dominios/Tecnologia/Cloud/02 - Anatomia de um provedor/index|Anatomia de um provedor]] — Galho 2
- [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Identidade e acesso (IAM)]] — Galho 4
