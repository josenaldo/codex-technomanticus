---
title: "Purpose Layer — o que o sistema é"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - ai-engineering-stack
  - ia
  - purpose
publish: true
aliases:
  - Purpose Layer
  - Camada de propósito
---

# Purpose Layer — o que o sistema é

> [!abstract] TL;DR
> A Purpose Layer responde "o que esse sistema é?" antes que qualquer prompt seja escrito. Define system name, primary job, usuário-alvo, output principal, critérios de sucesso e — fundamental — o que o sistema **não faz**. Sem essa camada, todas as outras decisões viram opinião: você não tem critério pra recusar um pedido fora de escopo, pra escolher entre dois prompts, pra dizer se o output ficou bom. Sistemas sem Purpose Layer explícita acabam tentando fazer tudo e fazem mal.

## O que é esta camada

A Purpose Layer é o **documento fundador** do sistema de IA. Ela existe antes do código, antes do prompt, antes da escolha de modelo. Responde quem é o usuário, qual o trabalho que está sendo automatizado, o que o sistema produz e — crucialmente — onde estão as fronteiras.

O template mínimo (adaptado do thread @hooeem):

```yaml
system_name: <nome curto e específico>
primary_job: <uma frase com verbo no infinitivo>
user: <persona concreta, não "todo mundo">
main_output: <artefato único que o sistema entrega>
success_criteria:
  - <critério mensurável 1>
  - <critério mensurável 2>
  - <critério mensurável 3>
not_in_scope:
  - <o que o sistema explicitamente NÃO faz>
  - <onde ele encaminha pra outro sistema ou humano>
```

A regra do `not_in_scope` é o que separa Purpose Layer bem-feita de mission statement vazio. Sistema que tem só `primary_job` e nenhum `not_in_scope` vai aceitar tudo.

## Decisões-chave

1. **Granularidade do `primary_job`.** "Ajudar o usuário com escrita" é vago demais — não dá critério. "Gerar resumo de artigo técnico em 200 palavras com 3 takeaways" é específico — dá pra avaliar. Quanto mais estreita a primária, mais fácil tudo a jusante.

2. **Persona única vs múltiplas.** Tentar servir analista, gerente e estagiário com o mesmo sistema gera prompts mornos. Escolha uma persona; se duas surgem, são dois sistemas.

3. **`not_in_scope` como contrato.** O que o sistema rejeita é tão definidor quanto o que ele aceita. Listar 3-5 categorias do que **não** faz evita escopo elástico em produção.

4. **Critérios de sucesso mensuráveis.** Se um critério não pode ser traduzido pra rubrica ([[09 - Evaluation Layer]]), ele não é critério — é desejo. Reescreva até virar mensurável.

5. **Quem assina o doc.** Em time, o Purpose Layer vira fonte única de verdade. Mudança nele cascateia em mudança de prompt, eval, guardrail. Trate como spec versionada.

## Onde aprofundar no Codex

- **[[Spec-Driven Development]]** — a Fase Specify é a versão completa e formalizada da Purpose Layer. Ler especialmente [[03-Dominios/Tecnologia/IA/Spec-Driven Development/04 - Fase Specify — definindo outcomes e constraints|Fase Specify]].
- **[[03-Dominios/Tecnologia/IA/Anatomia de Agents/01 - O que é um agent|O que é um agent]]** — discussão de quando a "primary_job" justifica um agent vs workflow.

## Veja também

- [[01 - As 11 camadas — visão geral]]
- [[03 - Prompt Layer]] — a próxima camada usa o `primary_job` como espinha do system prompt
- [[09 - Evaluation Layer]] — os `success_criteria` viram rubrica aqui

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 1 (Purpose layer template).
- **Anthropic** — [*Building effective agents*](https://www.anthropic.com/engineering/building-effective-agents). Discute "knowing when (and when not) to use agents" — a mesma pergunta que a Purpose Layer formaliza.
