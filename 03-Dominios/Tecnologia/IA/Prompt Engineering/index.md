---
title: "Prompt Engineering"
type: moc
publish: true
tags:
  - prompt-engineering
  - ia
  - moc
created: 2026-05-28
updated: 2026-05-28
aliases:
  - Engenharia de Prompts
---

# Prompt Engineering

Em 2025, Karpathy declarou que *"prompt engineering morreu"*. A frase pegou — e foi mal lida. O que morreu foi o **prompt como bala de prata**: a ideia de que a frase mágica, isolada, resolve qualquer tarefa. O **ofício do prompt** segue muito vivo — agora como uma camada bem-definida dentro de um sistema maior. Esta trilha trata Prompt Engineering como a camada **dentro** do Prompt Layer do [[AI Engineering Stack]]. [[Context Engineering]] é o superset que cuida do ambiente informacional inteiro; não substitui o ofício do prompt, contém-no. Aqui você aprende as primitivas: especificidade, roles, few-shot, constraints, iteração disciplinada, prompts para reasoning models, e o catálogo de anti-patterns que denunciam IA.

> [!info] Pré-requisitos
> [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/01 - O que é um LLM|01 - O que é um LLM]], [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/02 - Tokens e tokenização|02 - Tokens e tokenização]] e [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/06 - A janela de contexto|03 - A janela de contexto]] são suficientes. Familiaridade com [[Context Engineering]] ajuda a ver onde esta trilha se encaixa, mas não é obrigatória.

> [!warning] Não é "prompt vs context"
> Esta trilha **não** compete com [[Context Engineering]]. Prompt Engineering é uma camada dentro do Prompt Layer; Context Engineering é a disciplina mais larga que orquestra prompt + retrieval + memória + tools. Quem só faz prompt sem pensar em context produz demos; quem só pensa em context sem afiar o prompt entrega sistemas vagos. As duas trilhas se complementam.

## Comece por aqui

Trilha sequencial recomendada — fundamentos → técnicas centrais → controle fino → cultura.

### Bloco 1 — Fundamentos (2 notas)

Por que o ofício importa e qual a primeira disciplina a internalizar.

- [[01 - Por que prompt engineering ainda importa]] — a tese "prompt engineering morreu", o que de fato morreu, o que segue vivo, onde mora no stack
- [[02 - Especificidade — a primeira disciplina]] — o salto de qualidade vem antes de qualquer técnica avançada

### Bloco 2 — Técnicas Centrais (3 notas)

As alavancas que entregam ROI maior por linha de prompt.

- [[03 - Roles e personas — escolhendo o juízo do modelo]] — steering via prior de treino, template completo de role
- [[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy]] — artefato canônico, cláusula por cláusula
- [[05 - Few-shot examples — exemplos como contrato]] — por que exemplos batem instruções abstratas, princípios anti-poison

### Bloco 3 — Controle Fino (3 notas)

Da expressão de comportamento ao controle disciplinado de output e iteração.

- [[06 - Constraints declarativas — boundaries como engenharia]] — 8 dimensões, template, diferença vs guardrails de sistema
- [[07 - Iteration patterns — keep, change, do-not]] — anti-pattern "try again, make it better"
- [[08 - Reasoning models — audit trail, não chain-of-thought]] — o que mudou em o3/R1/Gemini Thinking

### Bloco 4 — Cultura (1 nota)

A higiene que separa output de IA de output assinável.

- [[09 - Anti-patterns e tells de IA — o que evitar]] — catálogo de frases bandeira-vermelha, como bloquear via constraints

## Rotas alternativas

### Rota mínima (preciso melhorar prompts hoje)
*"Não quero trilha inteira — me dê o essencial pra subir qualidade amanhã"*

[[02 - Especificidade — a primeira disciplina]] → [[03 - Roles e personas — escolhendo o juízo do modelo]] → [[06 - Constraints declarativas — boundaries como engenharia]] → [[09 - Anti-patterns e tells de IA — o que evitar]]

### Rota Karpathy (vim pelo mega-prompt)
*"Quero entender o prompt do Karpathy e onde ele se encaixa"*

[[01 - Por que prompt engineering ainda importa]] → [[03 - Roles e personas — escolhendo o juízo do modelo]] → [[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy]] → [[06 - Constraints declarativas — boundaries como engenharia]]

### Rota reasoning (uso o3 / R1 / Gemini Thinking)
*"Modelos com pensamento mudaram meu workflow — como ajustar?"*

[[08 - Reasoning models — audit trail, não chain-of-thought]] → [[02 - Especificidade — a primeira disciplina]] → [[06 - Constraints declarativas — boundaries como engenharia]] → [[07 - Iteration patterns — keep, change, do-not]]

### Rota cultural (quero output que não pareça IA)
*"Meus textos saem com cara de ChatGPT — quero higiene"*

[[09 - Anti-patterns e tells de IA — o que evitar]] → [[06 - Constraints declarativas — boundaries como engenharia]] → [[05 - Few-shot examples — exemplos como contrato]] → [[03 - Roles e personas — escolhendo o juízo do modelo]]

## Leituras recomendadas

| Fonte | Tipo | Cobertura |
|-------|------|-----------|
| **@hooeem** — *Become an AI Engineer*, caps 2-8 | Thread / artigo | Trilha inteira (espinha dorsal) |
| **Schulhoff et al.** — *The Prompt Report* ([arxiv:2406.06608](https://arxiv.org/abs/2406.06608), 2024) | Survey acadêmico | Notas 02, 03, 05, 08 |
| **OpenAI** — *Prompt Engineering Guide* | Doc oficial | Notas 02, 05, 06 |
| **Anthropic** — *Prompt Engineering docs* | Doc oficial | Notas 02, 03, 06 |
| **Karpathy** — System prompt circulado em 2025 | Artefato | Nota 04 |

## Veja também

- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/03 - Prompt Layer|AI Engineering Stack — Prompt Layer]] — onde esta trilha se encaixa na arquitetura
- [[Context Engineering]] — o superset; prompt é uma das fontes de contexto
- [[03-Dominios/Tecnologia/IA/Context Engineering/15 - Técnicas de prompting — zero-shot, few-shot, CoT, ToT|Context Engineering — Técnicas de prompting]] — taxonomia adjacente
- [[Anatomia dos LLMs]] — pré-requisito conceitual
- [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/15 - Reasoning models e chain-of-thought|Reasoning models e chain-of-thought]] — o "porquê" da nota 08
- [[Segurança e Guardrails]] — onde constraints declarativas terminam e guardrails de sistema começam

## Todas as notas

```dataview
LIST
FROM "03-Dominios/Tecnologia/IA/Prompt Engineering"
WHERE type != "moc"
SORT file.name ASC
```
