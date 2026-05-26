---
title: "Compressão de tool definitions"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - economia-tokens
  - ia
  - custos
aliases:
  - Tool compression
  - Compressão de schemas
  - Tool definitions optimization
---

# Compressão de tool definitions

> [!abstract] TL;DR
> [[Dicionário de IA#tool definition|Tool definitions]] (schemas JSON que descrevem ferramentas disponíveis para o agente) consomem 500-5000 [[Dicionário de IA#Token|tokens]] por chamada e são reenviadas em CADA request. Com 10 tools, isso pode significar 3-5k tokens de input "invisíveis" que custam dinheiro a cada turn. Comprimir descriptions, remover campos opcionais redundantes, e limitar o número de tools ativas pode reduzir esse custo em 50-70% sem degradar a capacidade do [[Dicionário de IA#Agent|agente]].

## O que é

Quando um agente tem acesso a ferramentas (read_file, write_file, bash, etc.), as definições dessas ferramentas são incluídas no prompt como JSON schemas. O modelo precisa "ler" essas definições em cada chamada para saber quais tools usar e como.

## Como funciona

### O custo oculto das tools

Exemplo: Claude Code com 15 ferramentas → ~4000 tokens de tool definitions por chamada.

Em uma sessão de 50 turns:

- 50 × 4000 = 200.000 tokens de input gastos apenas em tool definitions
- Com Claude Sonnet ($3/MTok): **$0.60** só em tools — sem nenhuma resposta útil

### Técnicas de compressão

#### 1. Descriptions concisas

```json
// ❌ Verboso (85 tokens)
{
  "name": "read_file",
  "description": "Reads the complete contents of a file from the local filesystem. This tool supports reading text files as well as some binary files such as images and videos. The file path must be an absolute path to ensure correct file resolution.",
  "input_schema": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "The absolute path to the file that should be read from the local filesystem. Must be a valid, existing file path."
      }
    },
    "required": ["path"]
  }
}

// ✅ Comprimido (28 tokens)
{
  "name": "read_file",
  "description": "Read file. Absolute path.",
  "input_schema": {
    "type": "object",
    "properties": {
      "path": {"type": "string"}
    },
    "required": ["path"]
  }
}
```

**Economia: ~67% menos tokens por tool.**

#### 2. Lazy loading de tools

Em vez de incluir todas as tools em cada chamada, incluir apenas as relevantes para a fase atual:

| Fase          | Tools necessárias                | Tools removidas     |
| ------------- | -------------------------------- | ------------------- |
| Análise       | read_file, list_dir, grep_search | write_file, bash    |
| Implementação | read_file, write_file            | browser, search_web |
| Teste         | bash, read_file                  | write_file, browser |

#### 3. Agrupamento de tools similares

```json
// ❌ 3 tools separadas (300 tokens)
"tools": [
  {"name": "read_file", ...},
  {"name": "list_dir", ...},
  {"name": "grep_search", ...}
]

// ✅ 1 tool com ação (120 tokens)
"tools": [{
  "name": "filesystem",
  "description": "File operations: read, list, search",
  "input_schema": {
    "properties": {
      "action": {"enum": ["read", "list", "search"]},
      "path": {"type": "string"},
      "query": {"type": "string"}
    }
  }
}]
```

### Impacto real

| Cenário                            | Tokens/turn em tools | Economia |
| ---------------------------------- | -------------------- | -------- |
| Sem otimização (15 tools verbosas) | ~5000                | Baseline |
| Descriptions comprimidas           | ~2000                | 60%      |
| + Lazy loading (5 tools/turn)      | ~700                 | 86%      |
| + Agrupamento                      | ~400                 | 92%      |

## Armadilhas

- **Comprimir demais degrada o modelo** — descriptions curtas demais confundem o modelo sobre quando usar a tool. Teste antes de comprimir tudo.
- **Lazy loading requer lógica extra** — precisa de um sistema que decida quais tools incluir em cada chamada.
- **Agrupamento pode confundir** — se a tool agrupada tem muitos parâmetros, o modelo pode chamá-la incorretamente.

## Veja também

- [[05 - Prompt caching na prática]] — tool definitions são cacheáveis
- [[06 - Context pruning — o que remover do prompt]] — pruning geral
- [[02 - Anatomia do gasto — input, output e reasoning]] — onde tools aparecem no breakdown

## Referências

- **Anthropic** — *Tool Use Best Practices* (2026). Guia de definição de tools.
