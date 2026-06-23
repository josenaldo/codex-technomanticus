---
title: "O Lado Sombrio da IA"
type: moc
publish: true
created: 2026-05-26
updated: 2026-05-26
status: seedling
tags:
  - moc
  - ia
  - lado-sombrio-ia
aliases:
  - O Lado Sombrio da IA
  - Lado Sombrio da IA
  - Impactos Negativos da IA
  - Custos Humanos da IA
---

# O Lado Sombrio da IA

> [!abstract] TL;DR
> Galho que reúne os **custos humanos, cognitivos e sociais** da adoção de IA no desenvolvimento de software — o que não aparece nas métricas de velocidade. É o complemento crítico à formação: enquanto as 10 trilhas ensinam a *usar* IA, este galho cataloga o que ela *cobra*.

Este galho fica **fora das 10 trilhas** porque é uma camada transversal e crítica, não um módulo de competência. Ele se distingue de [[03-Dominios/Tecnologia/IA/Segurança e Guardrails/index|Segurança e Guardrails]] por um eixo: lá o risco é **técnico** (prompt injection, código untrusted, sandboxing); aqui o custo é **humano e sistêmico** — o que a IA faz com a mente, a competência, a saúde e o ecossistema de quem a usa.

Três sub-temas organizam o galho:

## Erosão cognitiva e de competência

Como a IA corrói o entendimento e a habilidade — em nível de projeto e de carreira.

- [[Débito cognitivo]] — erosão do entendimento compartilhado em nível de projeto (Storey)
- TODO: **Débito de compreensão** — gap entre volume de código e o quanto alguém entende (Osmani) · glosa: [[02-Glosas/2026-comprehension-debt-hidden-cost-ai-generated-code|Comprehension debt]]
- TODO: **Rendição cognitiva** — aceitar a saída da IA como resposta própria, sem juízo independente (Osmani) · glosa: [[02-Glosas/2026-cognitive-surrender|Cognitive surrender]]
- TODO: **Deskilling — o impacto na formação de júniors** · glosa: [[02-Glosas/2026-how-ai-assistance-impacts-formation-coding-skills|How AI assistance impacts the formation of coding skills]]

## Saúde psicológica

O custo da IA sobre o bem-estar de quem desenvolve.

- TODO: **Saúde mental e burnout** — especialmente em seniors
- TODO: **Psicose da IA** — efeitos do uso intensivo de chatbots
- TODO: **Tokenmaxxing** — a otimização compulsiva de uso/custo como sintoma

## Dano ao ecossistema

Externalidades da IA sobre a comunidade e os bens comuns do software.

- TODO: **Erosão do open source** — abandonware gerado por IA esvaziando projetos abertos · glosa: [[02-Glosas/2026-ai-generated-abandonware-is-hollowing-out-open-source|AI-generated abandonware is hollowing out open source]]
- TODO: **The AI vampire** · glosa: [[02-Glosas/2026-the-ai-vampire|The AI vampire]]

## Fundamento

- [[O programa como teoria]] — a tese de Naur (em [[03-Dominios/Ciência/index|Ciência da Computação]]) que dá a base teórica para entender o que se perde no débito cognitivo.
- [[03-Dominios/Engenharia/Complexidade de Software/index|Complexidade de Software]] — o galho que trata as três dívidas (técnica, cognitiva, **intenção**) sob a lente geral/atemporal; este galho da IA as trata sob a lente dos custos da IA.

## Veja também

- [[03-Dominios/Tecnologia/IA/index|IA — Formação Engenheiro de IA]] — o domínio que este galho complementa criticamente
- [[03 - O comprehension gate|Comprehension gate]] · [[02 - Vibe coding vs engenharia disciplinada|Vibe coding vs engenharia disciplinada]] — práticas de defesa
- [[03-Dominios/Tecnologia/IA/Segurança e Guardrails/index|Segurança e Guardrails]] — o eixo de risco técnico (complementar)

---

*Dataview — notas deste galho:*

```dataview
LIST
FROM "03-Dominios/Tecnologia/IA/O Lado Sombrio da IA"
WHERE type != "moc"
SORT file.name ASC
```
