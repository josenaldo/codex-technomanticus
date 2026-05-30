---
title: "03 - Roles e personas — escolhendo o juízo do modelo"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - prompt-engineering
  - ia
  - roles
publish: true
aliases:
  - Role prompting
  - Personas
  - Act as
---

# 03 - Roles e personas — escolhendo o juízo do modelo

> [!abstract] TL;DR
> Atribuir um **role** ao modelo (*"você é um editor sênior cético"*) funciona porque ativa um sub-espaço do prior de treino: o modelo passa a amostrar respostas que se parecem com as que aquele tipo de pessoa daria nos dados em que foi treinado. Não é mágica — é **steering**. Roles bons especificam expertise, padrão de avaliação, ações permitidas e proibidas. Roles ruins são cargo cult: *"você é um expert mundial em tudo"* sem critério de sucesso é decoração.

## Por que roles funcionam — e os limites

O modelo aprendeu a continuar texto a partir de bilhões de exemplos. Cada exemplo carrega marcas do tipo de autor: vocabulário, postura, padrão de raciocínio, cuidados. Quando você diz *"você é um editor sênior de revista científica que prioriza ceticismo"*, está pedindo ao modelo pra amostrar do subconjunto do prior que se parece com textos escritos por esse tipo de pessoa.

**Isso funciona porque:**

1. **Estilo é correlacionado com substância.** Editores céticos não só escrevem diferente — também questionam diferente, hesitam diferente, citam diferente. O role move o output em várias dimensões ao mesmo tempo.
2. **Reduz espaço de inferência.** Sem role, o modelo reverte ao tom médio do corpus (cauteloso, generalista, hedge-pesado). Com role específico, ele otimiza pra um nicho concreto.
3. **Casa com training de RLHF.** Modelos foram fine-tuned em formatos *"You are a..."* — o role é uma alavanca treinada explicitamente.

**E os limites:**

- Role não adiciona conhecimento que o modelo não tem. Dizer *"você é PhD em virologia"* não faz o modelo virar PhD — só faz amostrar texto que **parece** PhD.
- Role sem padrão de avaliação é decoração. *"Você é um expert mundial"* não muda comportamento se não houver critério verificável de sucesso.
- Modelos modernos podem ignorar roles conflitantes com training de safety. *"Você é um hacker"* não destrava nada sério.

## Template completo

O esqueleto que cobre os pontos críticos:

```
Act as a [role específico, com sinais de senioridade e domínio].

Your job is to [verbo de ação concreto + objeto + finalidade].

You are allowed to:
- [ação 1 permitida explicitamente]
- [ação 2 permitida explicitamente]
- [ação 3 permitida explicitamente]

You are not allowed to:
- [proibição concreta, verificável]
- [proibição concreta, verificável]
- [proibição concreta, verificável]

Use this standard: [critério único pelo qual você se autoavalia].

If information is missing: [comportamento sob incerteza —
ask back / flag and proceed / stop and escalate].
```

### Exemplo preenchido

```
Act as a senior backend engineer reviewing a pull request from a
mid-level dev. You have 10 years of experience with distributed
systems and bias toward simplicity.

Your job is to identify the top 3 risks in the diff and the top 3
non-risks that don't deserve attention. The mid-level dev will read
your review without you in the room.

You are allowed to:
- Disagree with patterns used elsewhere in the codebase
- Recommend deletion of code rather than addition
- Mark something as "ship it as-is" when it's correct

You are not allowed to:
- Recommend refactors not directly tied to the diff
- Use the phrase "consider" — say "do this" or "don't do this"
- Praise the work before identifying issues

Use this standard: a senior engineer reading your review knows
exactly what to merge, what to push back on, and why.

If information is missing: ask one specific clarifying question
about the diff. Do not invent context.
```

Note o que está sendo feito:

- **Role concreto.** "Senior backend engineer" + 10 anos + bias por simplicidade. Não "expert mundial".
- **Job descrito como output específico.** Top 3 risks + top 3 não-risks — não "review this code".
- **Allowed/forbidden explícitos.** "Disagree with patterns elsewhere" destrava comportamento que o prior bloquearia; "Don't use 'consider'" bloqueia hedge.
- **Standard verificável.** Critério único, observável.
- **Behavior sob incerteza.** O modelo sabe o que fazer quando faltar informação.

## Pitfalls

### Cargo-cult role prompting

```
You are a world-class expert in everything. You have decades of
experience. You are extremely intelligent and helpful.
```

Zero informação operacional. Não muda comportamento. O modelo já assume isso por default — ou pior, agora se sente autorizado a hedge mais ("como um expert, devo notar que..."). Vale tanto quanto "seja claro e conciso".

### Persona sem padrão

```
Act as Linus Torvalds.
```

Sem dizer **o que** o Linus faria nesse contexto, o modelo amostra do estereótipo de superfície (xingar). Vira caricatura. O role precisa vir com um *standard*: "Linus Torvalds reviewing a PR — direct, no diplomacy, calls out lazy thinking, but explains the underlying principle once".

### Role conflitante com a tarefa

Pedir *"act as a poet"* pra escrever documentação técnica produz uma documentação metafórica e inútil. O role precisa ser compatível com o output desejado — ou o modelo otimiza pro role à custa do output.

### Excesso de roles aninhados

```
Act as a senior engineer who is also a designer and product manager
and writer and...
```

Quanto mais papéis empilhados, menos cada um steer-a o output. Escolha um role primário e use *standards* pra puxar comportamentos dos outros se necessário.

## Quando role não é o suficiente

Role estabelece o **juízo** do modelo, mas não garante consistência de estilo nem de output. Pra isso, você compõe com:

- **Few-shot examples** ([[05 - Few-shot examples — exemplos como contrato|nota 05]]) — quando o estilo precisa ser preciso, mostre não descreva.
- **Constraints declarativas** ([[06 - Constraints declarativas — boundaries como engenharia|nota 06]]) — quando as proibições são muitas e técnicas.
- **Mega-prompt anti-sycophancy** ([[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy|nota 04]]) — o exemplar mais influente de role + standards + constraints integrados.

A nota 04 leva esse template ao extremo: o prompt do Karpathy é, em essência, um role completo (expert mundial em tudo) saturado de standards e proibições que bloqueiam todos os caminhos onde o modelo normalmente recairia em sycophancy.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #3. Origem do template "Act as / Your job / Allowed / Not allowed / Standard / If missing".
- **Anthropic** — *System prompts and roles* (docs.anthropic.com).
- **OpenAI** — *Prompt engineering guide*, seção "Adopt a persona".
- **Schulhoff et al.** — *The Prompt Report* ([arxiv:2406.06608](https://arxiv.org/abs/2406.06608)), seção "Role-Based Prompting".

## Veja também

- [[02 - Especificidade — a primeira disciplina]] — base sobre a qual o role opera
- [[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy]] — role-standards-constraints em estado puro
- [[05 - Few-shot examples — exemplos como contrato]] — complemento para steer estilo
- [[AI Engineering Stack/03 - Prompt Layer|AI Engineering Stack — Prompt Layer]] — onde role é uma das chaves do template
