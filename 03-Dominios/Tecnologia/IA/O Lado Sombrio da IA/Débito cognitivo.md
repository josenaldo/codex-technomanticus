---
title: "Débito cognitivo"
created: 2026-05-26
updated: 2026-05-26
type: concept
progress: backlog
status: seedling
tags:
  - ia
  - lado-sombrio-ia
  - debito-cognitivo
aliases:
  - Débito cognitivo
  - Dívida cognitiva
  - Cognitive debt
publish: true
---

# Débito cognitivo

A erosão, ao longo do tempo, do entendimento que uma equipe compartilha sobre o sistema que constrói — o risco que a IA generativa desloca do código para a mente das pessoas.

> [!abstract] TL;DR
> **Débito cognitivo** é a erosão progressiva do entendimento compartilhado de uma equipe sobre o que um sistema faz, por que as decisões foram tomadas e como mudá-lo. Diferente do débito técnico (que vive no código) e da carga cognitiva (momentânea), é uma propriedade de **nível de projeto**. A IA generativa o acelera: ela barateia produzir estrutura mais rápido do que o entendimento consegue estabilizar. Termo desenvolvido por Margaret-Anne Storey (2026), apoiado na tese de [[O programa como teoria|Naur de que um programa é uma teoria]].

## O que é

Débito cognitivo é o que acontece quando um time perde, gradualmente, a [[O programa como teoria|teoria do sistema]]: a capacidade de explicar o que o programa faz, como as intenções foram implementadas e como alterá-lo com segurança. Código limpo e testes verdes não impedem que as pessoas "percam o fio da meada".

É um conceito de **nível de projeto**, que captura como o entendimento se deteriora ao longo do tempo — não um estado momentâneo de um indivíduo.

## Débito cognitivo × débito técnico × carga cognitiva

| Conceito | Onde vive | Natureza |
| --- | --- | --- |
| **Débito técnico** | no código | atalhos estruturais que cobram juros em manutenção |
| **Carga cognitiva** | no indivíduo, no momento | esforço mental exigido por uma tarefa agora |
| **Débito cognitivo** | na mente coletiva, ao longo do tempo | erosão do entendimento compartilhado em nível de projeto |

A distinção é o ponto-chave: você pode zerar o débito técnico (código impecável, gerado por IA) e ainda assim acumular débito cognitivo, porque ninguém detém mais a teoria do que foi construído.

## Por que a IA acelera

À medida que a IA reduz o atrito *técnico* de produzir código, o **entendimento compartilhado** vira o gargalo da performance. A IA baixa o custo de gerar estrutura, fazendo o sistema evoluir mais rápido do que a teoria humana consegue estabilizar. Adicionar mais agentes pode piorar: aumenta overhead de coordenação e decisões invisíveis — um eco do *Mythical Man-Month* de Brooks. **Velocidade sem entendimento não é sustentável.**

## Sinais de alerta

> [!warning] Sintomas de débito cognitivo acumulando
> - Hesitação em mudar o código por medo de quebrar algo que ninguém entende
> - Dependência crescente do "conhecimento tribal" de uma ou duas pessoas
> - O sistema virando caixa-preta — funciona, mas o "porquê" se perdeu
> - Onboarding cada vez mais lento
> - Fadiga e estresse da equipe ao mexer em áreas opacas

## Mitigação

- **[[03 - O comprehension gate|Comprehension gate]]:** exigir que ao menos um humano entenda cada mudança gerada por IA *antes* do merge.
- **Documentar o porquê, não só o quê:** decisões e alternativas descartadas, não apenas o que o código faz.
- **Checkpoints de reconstrução de entendimento:** code reviews, retrospectivas, sessões de knowledge-sharing.
- **Práticas que reconstroem teoria compartilhada:** pair programming, refactoring, TDD — e o *"make the hard change easy"* de Kent Beck.
- **Specs como artefatos vivos:** só funcionam se o time engaja ativamente com elas, não como documento morto.

## Fontes

- [[02-Glosas/2026-cognitive-debt-hidden-risk-ai-driven-software-development|Cognitive debt: The hidden risk in AI-driven software development — Margaret-Anne Storey (DX)]]

## Veja também

- [[11 - Dívida cognitiva]] — **o mesmo conceito sob a lente geral/atemporal** (em [[03-Dominios/Engenharia/Complexidade de Software/index|Complexidade de Software]]); esta nota é o recorte da *aceleração por IA*
- [[O programa como teoria]] — a base teórica (Naur): o que exatamente se perde quando há débito cognitivo
- [[03 - O comprehension gate|Comprehension gate]] — a barreira de code review que defende a teoria mudança a mudança
- [[02 - Vibe coding vs engenharia disciplinada|Vibe coding vs engenharia disciplinada]] — o contexto que gera o débito
- [[02-Glosas/2026-comprehension-debt-hidden-cost-ai-generated-code|Comprehension debt — Addy Osmani]] — conceito vizinho (gap código × entendimento)
- [[02-Glosas/2026-cognitive-surrender|Cognitive surrender — Addy Osmani]] — a postura individual que alimenta o débito
