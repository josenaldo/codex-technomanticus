---
title: "Tool Layer"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - ai-engineering-stack
  - ia
  - tools
publish: true
aliases:
  - Tool Layer
  - Camada de ferramentas
---

# Tool Layer

> [!abstract] TL;DR
> A Tool Layer define **o que o modelo pode fazer no mundo** — calculadora, busca, query no banco, criar arquivo, mandar email. Decide quais tools estão disponíveis, quando usar cada uma, quais exigem aprovação humana, quais são proibidas, e o que acontece quando uma falha. Cada tool é uma porta de saída do "modelo" pro sistema real — e cada porta carrega risco. Sem essa camada bem desenhada, agentes fazem coisas erradas em produção e o time descobre depois.

## O que é esta camada

A Tool Layer é onde o modelo deixa de ser pura geração de texto e passa a **agir**. Cada tool é uma função tipada que o modelo pode chamar, com schema de entrada, schema de saída, e — implícito — efeito colateral.

Template mínimo (adaptado do thread @hooeem):

```yaml
available_tools:
  - name: <nome>
    when_to_use: <condições>
    when_not_to_use: <antípodas>
allowed_without_approval:
  - <tools de leitura sem efeito>
requires_approval:
  - <tools com efeito reversível>
forbidden:
  - <tools com efeito irreversível ou de alto risco>
tool_failure_behavior: <retry N vezes | fallback pra tool X | escalate>
```

A trilha [[MCP]] descreve o protocolo que padroniza o **transporte** de tools entre modelo e cliente; [[Anatomia de Agents/03 - Tool design — princípios e categorias|Tool design]] descreve **como** desenhar uma tool bem.

## Decisões-chave

1. **Quantas tools expor.** Modelos lidam mal com listas muito longas de tools — a escolha vira ruidosa, latência sobe. Regra prática: ≤10 tools por contexto. Acima disso, agrupe ou use sub-agentes especializados.

2. **Tools de leitura vs escrita.** Leitura (search, get, read) costuma ser segura sem aprovação. Escrita (write, send, delete, deploy) precisa de gradação — por valor, por irreversibilidade, por blast radius.

3. **Política de aprovação.** Três níveis comuns: (a) auto-approve — modelo decide e age; (b) confirm — modelo propõe, usuário confirma; (c) plan-then-execute — modelo escreve plano, usuário aprova plano inteiro. Quanto mais alto o risco, mais alto o nível.

4. **Failure handling.** Tool falha (timeout, 500, schema mismatch). Sem política, o modelo improvisa — às vezes chama de novo, às vezes inventa o resultado. Política explícita (retry com backoff, fallback, escalate) reduz comportamento errático.

5. **Tool design.** Tool com schema mal-feito gera alucinação de parâmetro ([[Segurança e Guardrails/03 - Alucinações em código — APIs fantasma e parâmetros inexistentes|APIs fantasma]]). Descrições claras, exemplos no schema, erros informativos — é trabalho de engenharia, não detalhe.

## Onde aprofundar no Codex

- **[[Anatomia de Agents/03 - Tool design — princípios e categorias|03 - Tool design]]** — princípios de desenho.
- **[[MCP]]** — protocolo padrão pra transportar tools.
- **[[Anatomia de Agents/02 - O loop ReAct e native tool use|O loop ReAct]]** — como o modelo decide chamar tool.

## Veja também

- [[08 - Workflow vs Agent Layer]] — agents usam tools dinamicamente; workflows usam pra passos fixos
- [[10 - Guardrail Layer]] — tools proibidas, blast radius
- [[11 - Logging Layer]] — registrar toda tool call

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 6 (Tool layer template).
- **Anthropic** — [*Tool use with Claude*](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview).
- **OpenAI** — [*Function calling*](https://platform.openai.com/docs/guides/function-calling).
