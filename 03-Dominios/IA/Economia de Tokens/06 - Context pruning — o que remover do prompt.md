---
title: "Context pruning — o que remover do prompt"
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
  - Context pruning
  - Poda de contexto
  - Prompt trimming
---

# Context pruning — o que remover do prompt

> [!abstract] TL;DR
> Context pruning é remover deliberadamente informação do prompt que não contribui para a tarefa atual. Isso reduz custo de input, melhora a qualidade (menos distração), e acelera a resposta (menos tokens para processar). As técnicas vão desde filtrar arquivos irrelevantes até sumarizar histórico antigo e truncar outputs de ferramentas. A regra é: se o modelo não precisa para responder à pergunta atual, não deveria estar no contexto.

## O que é

**Context pruning** (poda de contexto) é o processo de identificar e remover tokens do input que não são necessários para a tarefa em andamento. É a contrapartida do "mais contexto = melhor resposta" — na verdade, contexto irrelevante dilui a atenção do modelo e aumenta custo.

## Como funciona

### O que remover

| O que está no contexto                 | Precisa?                         | Ação                                  |
| -------------------------------------- | -------------------------------- | ------------------------------------- |
| System prompt + regras                 | ✅ Sempre                         | Manter (cachear)                      |
| Tool definitions                       | ✅ Se tools são necessárias       | Manter (comprimir schemas)            |
| Arquivo inteiro (500 linhas)           | ❌ Se só 20 linhas são relevantes | **Enviar só as linhas relevantes**    |
| Histórico de 50 turns                  | ❌ Turns antigos                  | **Sumarizar** blocos antigos          |
| Output longo de ferramenta             | ❌ Se 90% é irrelevante           | **Filtrar via RTK** ou truncar        |
| Erros de compilação (full stack trace) | ❌ Stack completo                 | **Filtrar** para as linhas relevantes |
| Instruções de projeto (CLAUDE.md)      | ⚠️ Se estiver muito grande        | **Manter enxuto**, apenas o essencial |
| Arquivos abertos (Git uncommitted)     | ⚠️ Se forem irrelevantes          | **Commitar/Fechar** arquivos          |
| Arquivo de lock (package-lock.json)    | ❌ Nunca relevante                | **Excluir** via .cursorignore         |

### Técnicas de pruning

#### 1. Retrieval seletivo (em vez de arquivo inteiro)

```
❌ Ruim: "Aqui está todo o auth.service.ts (500 lines)"
✅ Bom:  "Aqui estão as linhas 45-78 de auth.service.ts (função validateToken)"
```
Use `read_file` com `offset` e `limit` sempre que possível.

#### 2. Filtragem Dinâmica com RTK
O **RTK** (Runtime Tool Kit) permite interceptar comandos como `git status`, `git log` ou `grep` e filtrar sua saída antes que ela chegue ao LLM.
*   `git status` (cru) → pode listar 50 arquivos irrelevantes.
*   `rtk git status` → lista apenas os arquivos que importam para o contexto atual.

#### 3. Higiene de Projeto e Git
*   **CLAUDE.md:** Instruções de projeto são enviadas em cada turno. Se o seu `CLAUDE.md` tem 500 linhas de histórico do projeto, você está perdendo tokens. Mantenha-o focado em *regras de engenharia*.
*   **Commits frequentes:** Agentes costumam "olhar" para o `git status` e arquivos modificados. Se você tem 20 arquivos alterados mas está trabalhando em apenas 1, o agente pode acabar lendo contexto desnecessário. Commite ou faça stash do que não é relevante para a tarefa atual.

#### 4. Sumarização de histórico

```
❌ Ruim: Reenviar 40 turns completos (200k tokens)
✅ Bom:  Sumarizar turns 1-30 em 1k tokens + manter turns 31-40 completos
```

Agentes como Claude Code fazem isso automaticamente com "context compaction".

#### 3. Truncamento de tool outputs

```
❌ Ruim: Incluir 500 linhas de output de npm test
✅ Bom:  "5 testes passaram, 2 falharam: test_auth_login (line 34: expected 200, got 401)"
```

#### 4. .cursorignore / exclusão de indexação

```gitignore
# .cursorignore
node_modules/
dist/
build/
*.lock
*.log
coverage/
.git/
```

#### 5. Externalização de artefatos

Em vez de manter arquivos grandes no contexto, referenciá-los externamente:

```
❌ Ruim: "Aqui está a spec completa do projeto (50k tokens)"
✅ Bom:  "A spec está em docs/spec.md. Leia as seções relevantes quando necessário."
```

O agente busca sob demanda, lendo apenas as seções necessárias.

### Impacto em custo e qualidade

| Técnica                     | Redução de tokens   | Impacto na qualidade          |
| --------------------------- | ------------------- | ----------------------------- |
| Retrieval seletivo          | 60-80% por arquivo  | ✅ Melhora (mais focado)       |
| Sumarização de histórico    | 70-90% no histórico | ⚠️ Pode perder detalhes        |
| Truncamento de tool outputs | 50-80% por output   | ✅ Melhora (menos ruído)       |
| .cursorignore               | 20-40% global       | ✅ Melhora (menos irrelevante) |
| Externalização              | 80-95% por artefato | ⚠️ Depende do retriever        |

## Checklist

- [ ] .cursorignore / .gitignore configurados
- [ ] Agente configurado para enviar trechos, não arquivos inteiros
- [ ] Sumarização de histórico ativada (context compaction)
- [ ] Tool outputs truncados para informação essencial
- [ ] Artefatos grandes externalizados (referência, não inline)

## Armadilhas

- **Podar demais** — remover contexto crítico faz o modelo alucinar. O equilíbrio é arte.
- **Não testar o impacto** — meça qualidade antes e depois de pruning. Use probe questions.
- **Sumarização que perde contexto** — resumo ruim de histórico faz o agente "esquecer" decisões anteriores. Use summarizers que preservam decisões e artefatos.

## Veja também

- [[05 - Prompt caching na prática]] — cachear o que sobra depois de podar
- [[08 - Compactação de histórico em agentes]] — sumarização detalhada
- [[02 - Anatomia do gasto — input, output e reasoning]] — o que está inflando

## Referências

- **Machine Learning Mastery** — *Context Engineering for Agents* (2026). Técnicas de pruning.
- **JetBrains** — *Context Compaction in IDEs* (2026). Abordagem de IDEs AI.
