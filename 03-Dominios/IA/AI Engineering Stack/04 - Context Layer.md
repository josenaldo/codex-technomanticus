---
title: "Context Layer"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - ai-engineering-stack
  - ia
  - context
publish: true
aliases:
  - Context Layer
  - Camada de contexto
---

# Context Layer

> [!abstract] TL;DR
> A Context Layer responde **o que o modelo precisa saber** pra tomar boas decisões nesta tarefa específica. Diferente do Prompt Layer (que define comportamento), aqui entram goal da sessão, audience, contexto do projeto, source material, preferências, restrições, histórico de decisões e modos conhecidos de falha. É a camada onde [[Context Engineering]] vive — montada dinamicamente, em camadas, com [[Dicionário de IA#context rot|context rot]] em mente.

## O que é esta camada

A Context Layer é o **ambiente informacional** carregado pro modelo a cada tarefa. Não é estática (como o system prompt) nem externa (como retrieval) — é o conjunto curado de informação que **esta** execução precisa.

Template mínimo (adaptado do thread @hooeem):

```yaml
goal: <objetivo específico desta sessão>
audience: <pra quem o output vai>
project_context: <restrições e estado do projeto>
source_material: <documentos relevantes; pode ser referência por id>
preferences: <tom, exemplos a evitar, padrões da casa>
constraints: <limites técnicos, prazo, orçamento de tokens>
decision_history: <decisões anteriores que ainda valem>
known_failure_modes: <onde sistemas anteriores erraram>
```

A diferença prática: o **Prompt Layer** é o mesmo em mil chamadas; o **Context Layer** muda a cada chamada (ou cada sessão).

## Decisões-chave

1. **O que persiste, o que é transiente.** [[Context Engineering/05 - Camadas de contexto — persistente, temporal, transiente|Camadas de contexto]] separa o que vive por longo tempo (preferências do usuário) do que dura uma sessão (decision_history) do que dura um turn (source_material citado agora).

2. **Pull vs push.** Empurrar todo o material relevante de uma vez infla a janela e produz [[Dicionário de IA#context rot|context rot]]. Puxar só quando preciso (JIT retrieval, ver [[Context Engineering/06 - Dynamic retrieval beyond RAG|JIT retrieval]]) preserva atenção.

3. **Compressão vs fidelidade.** Documento longo pode ser passado bruto, resumido por outro LLM ou indexado pra retrieval. Compressão perde nuance; bruto consome tokens. A escolha depende do quanto cada nuance importa.

4. **Decision history.** Em sessões longas (especialmente com agents), o histórico de decisões anteriores é parte do contexto. Sem ele, o agente "esquece" o que já tentou e repete o mesmo erro.

5. **Known failure modes como contexto.** Listar onde o sistema costuma errar (no próprio contexto) reduz a recorrência. É auto-prompt-engineering: "anteriormente você falhou em X; preste atenção".

## Onde aprofundar no Codex

- **[[Context Engineering]]** — trilha inteira. Especialmente [[Context Engineering/04 - Context pipelines — montagem dinâmica|Context pipelines]] e [[Context Engineering/05 - Camadas de contexto — persistente, temporal, transiente|Camadas de contexto]].
- **[[Anatomia dos LLMs/03 - A janela de contexto|A janela de contexto]]** — limite físico.
- **[[Dicionário de IA#Context window|Dicionário: Context window]]**.

## Veja também

- [[03 - Prompt Layer]] — comportamento vs aqui (conhecimento)
- [[06 - Retrieval Layer]] — uma das fontes do Context Layer
- [[05 - Output Layer]] — Context informa Output mas não o substitui

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 3 (Context layer template).
- **Anthropic** — [*Effective context engineering for AI agents*](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (2025).
- **Karpathy, Andrej** — *Tweet on context engineering* (jun 2025). "LLM é a CPU, janela de contexto é a RAM, você é o OS."
