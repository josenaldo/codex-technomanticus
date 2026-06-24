---
title: "AI Engineering Stack"
type: moc
publish: true
tags:
  - ai-engineering-stack
  - ia
  - moc
  - arquitetura
created: 2026-05-28
updated: 2026-06-24
aliases:
  - AI Engineer Stack
  - Stack de Engenharia de IA
  - As 11 camadas
---

# AI Engineering Stack

Construir sistemas com [[Dicionário de IA#LLM (Large Language Model)|LLM]] em produção não é escrever um prompt melhor — é montar um stack de onze camadas, cada uma com uma decisão própria. Da camada de **propósito** (o que o sistema é) até a camada de **melhoria** (como ele evolui), passando por prompt, contexto, retrieval, tools, output, workflow vs agent, evaluation, guardrails e logging. Esta trilha é o atlas dessas camadas: cada nota responde o que a camada resolve, quais são as decisões-chave e onde no Codex você aprofunda. É um **tronco integrador** — não substitui as trilhas específicas, conecta todas elas em uma vista de cima.

> [!info] Pré-requisitos
> Conhecimento básico de [[Anatomia dos LLMs]] e [[Anatomia de Agents]]. Útil ter passado por [[Context Engineering]] e [[Spec-Driven Development]] antes — essas trilhas alimentam, respectivamente, a Context Layer e a Purpose Layer.

> [!tip] Como ler esta trilha
> As notas 02 a 12 cobrem cada camada em profundidade: problema que resolve, template YAML da camada, decisões-chave em prosa, casos práticos, armadilhas e vocabulário PT↔EN. Quando quiser ir ainda mais fundo, siga o wikilink "Onde aprofundar" para a trilha especializada. A nota 13 (Setup completo) costura tudo num exemplo end-to-end — todas as 11 camadas aplicadas a um único sistema.

## Comece por aqui

Trilha sequencial: panorama → cada camada uma a uma → recipe end-to-end.

### Bloco 1 — Panorama (1 nota)

A foto de cima das 11 camadas, com diagrama mostrando como elas se conectam.

- [[01 - As 11 camadas — visão geral]] — quais são, em que ordem se montam, como o feedback flui

### Bloco 2 — Camadas de definição (3 notas)

O que o sistema é, como ele se comporta e o que ele sabe.

- [[02 - Purpose Layer — o que o sistema é]] — system name, primary job, success criteria
- [[03 - Prompt Layer]] — role, job, standards, allowed/forbidden actions
- [[04 - Context Layer]] — goal, audience, project context, source material

### Bloco 3 — Camadas de execução (4 notas)

O que o sistema produz, de onde puxa conhecimento, o que pode fazer, e se é workflow ou agent.

- [[05 - Output Layer]] — formato, seções obrigatórias, confidence
- [[06 - Retrieval Layer]] — quando puxar conhecimento externo, hierarquia de fontes
- [[07 - Tool Layer]] — tools disponíveis, approval policy, failure handling
- [[08 - Workflow vs Agent Layer]] — quando construir um, quando o outro

### Bloco 4 — Camadas de controle (3 notas)

Como medir, restringir e registrar o sistema.

- [[09 - Evaluation Layer]] — rubrica, threshold, automatic failure
- [[10 - Guardrail Layer]] — proibições, escalation, kill switches
- [[11 - Logging Layer]] — o que registrar de cada run

### Bloco 5 — Loop de evolução (2 notas)

Como o sistema deixa de ser one-off e vira sistema vivo.

- [[12 - Improvement Layer]] — feedback estruturado, versionamento de prompt
- [[13 - Setup completo — do zero ao sistema de produção]] — recipe walkthrough de um exemplo

## Rotas alternativas

### Rota arquiteto (desenhar antes de codar)
*"Vou começar um sistema novo do zero — quero o blueprint"*

[[01 - As 11 camadas — visão geral]] → [[02 - Purpose Layer — o que o sistema é]] → [[08 - Workflow vs Agent Layer]] → [[13 - Setup completo — do zero ao sistema de produção]]

### Rota refactor (já tenho um sistema, quero formalizar)
*"Já tenho um protótipo rodando — quero auditar contra o stack"*

[[01 - As 11 camadas — visão geral]] → [[09 - Evaluation Layer]] → [[10 - Guardrail Layer]] → [[11 - Logging Layer]] → [[12 - Improvement Layer]]

### Rota produção (vou colocar em prod amanhã)
*"O sistema funciona em dev — preciso endurecer pra prod"*

[[10 - Guardrail Layer]] → [[09 - Evaluation Layer]] → [[11 - Logging Layer]] → [[13 - Setup completo — do zero ao sistema de produção]]

### Rota agentic (vou construir um agent)
*"Já decidi que é agent — quero o caminho específico"*

[[08 - Workflow vs Agent Layer]] → [[07 - Tool Layer]] → [[04 - Context Layer]] → [[09 - Evaluation Layer]] → [[10 - Guardrail Layer]]

## Leituras recomendadas

| Fonte                                                     | Tipo     | Cobertura                    |
| --------------------------------------------------------- | -------- | ---------------------------- |
| *@hooeem — Become an AI Engineer (thread)*                | Thread X | Trilha inteira (chapter #18) |
| *Anthropic — Effective context engineering for AI agents* | Artigo   | Notas 04, 06                 |
| *Anthropic — Building effective agents*                   | Artigo   | Notas 07, 08                 |
| *OpenAI — Structured Outputs guide*                       | Doc      | Nota 05                      |
| *Lilian Weng — LLM-powered Autonomous Agents*             | Artigo   | Notas 07, 08                 |
| *Eugene Yan — Evals are all you need*                     | Artigo   | Nota 09                      |
| *NIST — AI Risk Management Framework*                     | Spec     | Nota 10                      |
| *OpenTelemetry GenAI Semantic Conventions*                | Spec     | Nota 11                      |

## Veja também

- [[Context Engineering]] — Context Layer aprofundada
- [[Anatomia de Agents]] — Tool Layer e Workflow vs Agent aprofundados
- [[MCP]] — protocolo concreto da Tool Layer
- [[Spec-Driven Development]] — Purpose Layer formalizada como spec
- [[RAG e Vector Databases]] — Retrieval Layer aprofundada
- [[Segurança e Guardrails]] — Guardrail Layer aprofundada

## Todas as notas

```dataview
LIST
FROM "03-Dominios/Tecnologia/IA/AI Engineering Stack"
WHERE type != "moc"
SORT file.name ASC
```
