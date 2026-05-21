---
title: "Hacks de trincheira — Claude, Gemini e Copilot em 2026"
created: 2026-05-08
updated: 2026-05-11
type: concept
status: seedling
publish: true
tags:
  - economia-tokens
  - ia
  - claude
  - gemini
  - copilot
---

# Hacks de trincheira — Claude, Gemini e Copilot em 2026

> [!abstract] TL;DR
> Em maio de 2026, economizar tokens não é mais uma questão de "prompt engineering" genérico, mas de entender as mecânicas proprietárias de cada provedor. O Claude foca em controle de raciocínio, o Gemini em persistência de cache e o Copilot em governança de créditos. Esta nota compila as manobras táticas de maior ROI para cada ecossistema.

---

## 🛡️ Claude (Anthropic): Controle e Raciocínio

O Claude 4.x introduziu custos explícitos para o "monólogo interno" (thinking tokens) e reduziu o TTL do cache para 5 minutos.

### 1. O "Thinking Budget" (/effort)
Para tarefas de baixo valor (escrever testes, documentar código, converter tipos), use o comando `/effort low`.
*   **O Hack:** Isso limita o número de tokens de raciocínio que o modelo gera. Em tarefas mecânicas, o raciocínio profundo é desperdício de dinheiro.

### 2. Caveman Protocol (Protocolo Homem das Cavernas)
Adicione no topo do seu `CLAUDE.md`:
> "Responda como um homem das cavernas. Sem polidez, sem explicações inúteis. Apenas o código e resultados essenciais."
*   **Impacto:** Reduz tokens de saída (os mais caros) em até 70%. Ideal para fix de lint e refactorings rápidos.

### 3. RTK (Rust Token Killer)
Integre o RTK como um hook de terminal. Ele comprime a saída de ferramentas como `git diff` e `npm install` antes de serem enviadas ao Claude.
*   **Dica:** Sessões intensas de debug são as que mais sangram tokens. O RTK remove o "ruído" dos logs e mantém apenas o sinal.

### 4. /statusline (Visibilidade em Tempo Real)
Ative o `/statusline` no Claude Code para ver tokens, custo, modelo e status do cache em tempo real na linha de status do terminal.
*   **O Hack:** É o sinal mais rápido para decidir a hora certa de rodar `/compact` ou `/clear` — antes de o contexto explodir e forçar um restart caro.

### 5. Serena (Otimização Agressiva de Tokens)
**Serena** (GitHub: `oraios/serena`) é uma ferramenta externa que intercepta e otimiza fluxos de tokens de forma agressiva, sem exigir mudanças manuais no código de prompt.
*   **Quando usar:** Projetos onde o custo está alto e as técnicas manuais (pruning, compactação, caching) já foram esgotadas. Serena atua como uma camada adicional de compressão.

---

## 🔬 Caso Real: Auditoria de Projeto MedEspecialista API (Maio 2026)

> Sessão de otimização aplicada em um projeto Node.js real com 1.900+ testes e histórico extenso de sessões. As ações abaixo foram executadas em sequência após análise com `rtk gain` e `ccusage blocks --breakdown`.

### Diagnóstico pré-otimização

| Indicador | Valor observado | Problema |
| :--- | :--- | :--- |
| Cache hit rate (sessões recentes) | 15–63% (média ~40%) | Alto; instável demais — sinal de contexto não estático |
| Maior arquivo de memória | 299 linhas / 35 KB | Carregado em toda sessão; continha histórico de commits e contagem de testes progressiva |
| `effortLevel` global | `"xhigh"` | Forçava raciocínio estendido até em tarefas mecânicas (lint, boilerplate) |
| Entradas em permissions.allow (local) | 25 | Incluía 3 one-offs de sessões antigas com paths hardcoded |
| `.claudeignore` | Ausente | Claude podia ler `node_modules/`, `coverage/`, logs por acidente |

---

### Ação 1 — Limpeza de permissões (`settings.local.json`)

**O que:** Removidas 3 entradas one-off com UUIDs e paths hardcoded (`wc -l 82fa7381...`, `ls -lh 82fa7381...`, `grep -rln TutorContent...`). Consolidados `gh issue *` + `gh api *` + `gh project *` em uma entrada `Bash(gh:*)`.

**Resultado:** 25 → 22 entradas.

**Por que importa:** Entradas de sessões passadas não são removidas automaticamente. Com o tempo, o arquivo acumula lixo que comunica permissões obsoletas e torna a revisão de segurança mais difícil. Wildcards `gh:*` cobrem todos os subcomandos futuros sem crescimento do arquivo.

---

### Ação 2 — Poda agressiva de memória

**O que:** `project-metrics-redesign-progress.md` reduzido de 299 linhas para ~50. Removido: hashes de commit por onda, progressão de contagem de testes (1690 → 1956 linha a linha), detalhes de stories já entregues.

**Mantido:** estado atual (Onda 5 ENTREGUE), follow-ups pendentes, decisões vivas, setup de worktrees, links para specs e planos.

**Por que importa:** Histórico de commits pertence ao `git log`, não à memória do Claude. Cada linha de memória é carregada em toda sessão que usa o projeto. 250 linhas removidas = menos contexto estático queimado por conversa.

**Regra derivada:** Memória de projeto deve responder "o que está pendente e por quê?" — não "o que aconteceu?"

---

### Ação 3 — Atualização de memória conflitante

**O que:** `project-appshell-blocked.md` dizia "frontend aguarda Mantine 9". Mas `project-codebase-convergence.md` indicava que a migração estava concluída. Memória atualizada para refletir o estado real: o bloqueio agora é convergência de código (copy-paste entre admin e frontend).

**Por que importa:** Memórias conflitantes forçam o modelo a gastar tokens de raciocínio reconciliando contradições. Uma memória errada é pior que nenhuma — ela produz sugestões incoerentes e perguntas desnecessárias.

**Regra derivada:** Memórias com datas relativas ou referências a "aguarda X" devem ser revisadas proativamente ao retomar um projeto.

---

### Ação 4 — Remoção de `effortLevel: xhigh`

**O que:** Removida a chave `"effortLevel": "xhigh"` do `~/.claude/settings.json` global.

**Por que importa:** `xhigh` força raciocínio estendido (thinking tokens) em **toda** tarefa — incluindo `find`, linting, geração de boilerplate e discovery. Thinking tokens custam o mesmo que tokens de output e são invisíveis no contexto visível. Sem a chave, o modelo calibra o esforço pela complexidade da tarefa.

**Impacto esperado:** Redução significativa de thinking tokens em tarefas mecânicas, mantendo raciocínio profundo quando necessário (o modelo decide).

---

### Ação 5 — Criação de `.claudeignore`

**O que:** Criado `/api/.claudeignore` excluindo: `node_modules/`, `dist/`, `coverage/`, `*.lock`, `*.log`, `.tmp/`.

**Por que importa:** Sem este arquivo, exploração de codebase pelo Claude pode acidentalmente incluir arquivos gerados em leituras de diretório. Um único `package-lock.json` tem ~50k tokens. `coverage/` pode ter centenas de arquivos HTML de relatório.

**Analogia:** É o equivalente do `.gitignore` para o contexto do Claude — define o que não deve ser "visto" durante a navegação do projeto.

---

### Ação 6 — Instrução de concisão no `CLAUDE.md` (Caveman Protocol adaptado)

**O que:** Adicionada seção "Response Style" ao final do `CLAUDE.md` do projeto:
```
Durante implementação: one sentence per update, no trailing summaries.
State results and blockers — skip reasoning narration. The diff speaks for itself.
Durante planejamento ou documentação: full detail is appropriate.
```

**Por que importa:** Sem instrução explícita, o Claude por padrão encerra respostas de implementação com sumários do que foi feito, narração do processo de raciocínio e validações de "parece certo?". Esses tokens de cortesia são caros e irrelevantes para quem revisa um diff.

**A chave:** A instrução distingue explicitamente os dois modos. Planejamento e documentação **não** são afetados — o detalhe é preservado onde tem valor.

---

### Resultado consolidado

| Ação | Impacto direto |
| :--- | :--- |
| Permissions cleanup | -3 entradas one-off; wildcard cobre todos os subcomandos gh futuros |
| Memory pruning | -250 linhas de contexto estático por sessão |
| Memory conflict fix | Elimina tokens gastos reconciliando estado conflitante |
| effortLevel removido | Thinking tokens calibrados por tarefa, não forçados ao máximo |
| .claudeignore | Previne leituras acidentais de arquivos gerados (até 50k tokens/acidente) |
| Caveman Protocol | Redução estimada de 40-70% nos tokens de output durante implementação |

---

## 💎 Gemini (Google): Persistência de Contexto

O Gemini 3.1 Pro lidera em economia para bases de código gigantescas graças ao seu modelo de cache persistente.

### 1. Context Caching de Longo Prazo (24h)
Diferente do Claude, o Gemini permite "congelar" 1M de tokens no cache por até 24h.
*   **O Hack:** Se você vai trabalhar o dia todo no mesmo projeto, ative o cache persistente. Você paga uma taxa de "escrita" e uma pequena taxa de "aluguel" por hora, mas economiza 90% em cada pergunta feita ao longo do dia.

### 2. XML Scoping
O Gemini responde melhor a tags XML do que a Markdown para instruções complexas em janelas de contexto grandes.
*   **O Hack:** Envolva contextos diferentes em tags: `<legacy_code>`, `<new_requirements>`, `<constraints>`. Isso reduz a taxa de alucinação e, consequentemente, a necessidade de re-prompts caros para correção.

### 3. Flash-Lite Sandwich
Para tarefas massivas (ex: analisar 100 arquivos em busca de um padrão):
1. Use **Gemini Pro** para criar um "Mapa de Busca" (contexto pequeno).
2. Passe esse mapa para o **Gemini Flash-Lite** realizar a extração.
*   **Economia:** O Flash-Lite custa quase zero comparado ao Pro.

---

## 🐙 GitHub Copilot & Codex: Governança de Créditos

Com o faturamento baseado em uso (AI Credits) em vigor desde junho de 2026, cada request no VS Code tem um custo direto.

### 1. Content Exclusion Estratégico
Configure o `.github/copilot-exclusion` para bloquear pastas de `build/`, `node_modules/`, `dist/` e arquivos de log.
*   **Por que:** O Copilot tenta ler o contexto ao redor do cursor. Se ele ler um arquivo de build de 200k tokens por acidente, você paga por isso.

### 2. Modular Rules (.cursor/rules/)
Não use um arquivo de regras global gigante. Use regras escopadas por extensão ou pasta.
*   **O Hack:** Se você está editando um CSS, o Copilot não precisa carregar as regras de arquitetura do backend. Regras modulares garantem que o prompt de sistema seja o menor possível.

### 3. Plan Mode antes do Agent Mode
Nunca dispare o "Agent Mode" (que sai editando arquivos) sem antes rodar um "Plan Mode".
*   **Dica:** Validar o plano consome ~2k tokens. Um agente em loop errado pode consumir 200k tokens em 30 segundos de "tentativa e erro".

---

## Tabela de Decisão de Motor (Maio 2026)

| Necessidade | Motor Recomendado | Estratégia de Economia |
| :--- | :--- | :--- |
| **Refactor Complexo** | Claude 4.7 Opus | /effort high + /compact a cada 10 turns |
| **Análise de Repo Inteiro** | Gemini 3.1 Pro | Cache Persistente (TTL 24h) |
| **Boilerplate e Testes** | Gemini 2.0 Flash | Flash-Lite para documentação |
| **Codificação Diária** | Claude 4.5 Sonnet | RTK + Caveman Protocol |

## Veja também
- [[09 - Model routing — modelo certo para a tarefa]]
- [[10 - Sub-agentes especializados]]
- [[05 - Prompt caching na prática]]
