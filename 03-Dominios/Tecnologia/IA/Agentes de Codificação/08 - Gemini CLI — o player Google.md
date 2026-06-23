---
title: "Gemini CLI — o player Google"
created: 2026-05-02
updated: 2026-05-02
type: concept
progress: backlog
status: seedling
publish: true
tags:
  - agentes-codificacao
  - ia
  - ferramentas
aliases:
  - Gemini CLI
  - Google AI agent
  - Gemini Code
---

# Gemini CLI — o player Google

> [!abstract] TL;DR
> Gemini CLI é a ferramenta de terminal do Google DeepMind para codificação assistida por IA, baseada nos modelos Gemini. Em 2026, oferece contexto ultra-longo (até 2M tokens), multimodal nativo (pode analisar screenshots e diagramas), e integração com GCP. Posiciona-se entre Claude Code (reasoning) e Copilot (ecossistema), com o diferencial de preço agressivo via Gemini Flash e Flash-Lite para tarefas de rotina.

## O que é

**Gemini CLI** é um agente de codificação em terminal que usa modelos Gemini (Flash, Pro) para assistir desenvolvimento de software. Assim como Claude Code, opera no terminal com capacidade de ler/editar arquivos, executar comandos, e iterar.

## Por que importa

- **Contexto ultra-longo** — 1M-2M [[Dicionário de IA#Token|tokens]] permite processar codebases inteiros sem RAG
- **Multimodal** — pode analisar screenshots, diagramas UML, e wireframes como input
- **Preço** — Gemini Flash é 6x mais barato que Claude Sonnet para input

## Como funciona

### Diferenciais

| Feature                   | Gemini CLI    | Claude Code               | Cursor            |
| ------------------------- | ------------- | ------------------------- | ----------------- |
| **[[Dicionário de IA#Context window\|Contexto máximo]]**       | 2M tokens     | 200k (Sonnet) / 1M (Opus) | 200k-1M           |
| **Multimodal**            | ✅ Nativo      | ⚠️ Limitado                | ⚠️ Limitado        |
| **Custo (input/MTok)**    | $0.50 (Flash) | $3.00 (Sonnet)            | Depende do modelo |
| **Reasoning para código** | ★★★★          | ★★★★★                     | ★★★★              |
| **Integração GCP**        | ★★★★★         | ★                         | ★                 |

### GEMINI.md — configuração de projeto

```markdown
# GEMINI.md

## Projeto
Backend FastAPI com PostgreSQL.

## Regras
- Siga PEP 8
- Type hints em todas as funções
- Docstrings em formato Google
- Testes com pytest

## Contexto
- Deploy em Cloud Run
- CI via Cloud Build
```

### Multimodal na prática

```bash
# Analisar screenshot de UI e gerar componente
gemini "Analise este wireframe e crie o componente React" --image wireframe.png

# Debugar via screenshot de erro
gemini "O que está errado neste erro?" --image error-screenshot.png
```

## Quando usar

| Cenário                              | Gemini CLI             | Melhor alternativa |
| ------------------------------------ | ---------------------- | ------------------ |
| Codebase muito grande (>500k tokens) | ✅ Ideal                | Claude Opus (1M)   |
| Análise de screenshots/diagramas     | ✅ Ideal                | —                  |
| Projeto GCP/Firebase                 | ✅ Ideal                | —                  |
| Reasoning profundo para código       | ⚠️ Bom                  | Claude Code        |
| Custo-sensitivo                      | ✅ Flash é muito barato | —                  |

## Armadilhas

- **"Contexto grande = melhor"** — 2M tokens de contexto sem curadoria dilui a atenção. Use retrieval seletivo mesmo com contexto largo.
- **Reasoning inferior a Claude** — para debugging e refactoring complexo, Claude Code com Sonnet/Opus é consistentemente superior em benchmarks de coding.
- **Ecossistema imaturo** — menos plugins, extensões e comunidade comparado a Cursor e Claude Code.

## Veja também

- [[05 - Claude Code — terminal-first agent]] — concorrente com melhor reasoning
- [[04 - Cursor — AI-native IDE]] — alternativa IDE
- [[10 - OpenCode — o harness open source]] — alternativa open-source

## Referências

- **Google DeepMind** — *Gemini CLI Documentation* (2026). Referência oficial.
- **Google Cloud** — *Gemini for Developers* (2026). Integração com GCP.
