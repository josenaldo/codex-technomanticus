---
title: "Compressão e pruning de informação"
created: 2026-05-02
updated: 2026-06-19
type: concept
progress: backlog
status: growing
publish: true
tags:
  - context-engineering
  - ia
  - prompting
  - compactacao
aliases:
  - Compactação de contexto
  - Context compression
  - Prompt compaction
---

# Compressão e pruning de informação

> [!abstract] TL;DR
> Em sessões longas, a [[Dicionário de IA#Context window|janela de contexto]] satura — não pelo limite hard, mas pela [[03 - Context rot e atenção diluída|atenção diluída]]. As duas técnicas centrais para combater isso: **compressão** (resumir o que ainda é relevante) e **pruning** (remover ativamente o que não é mais). Anthropic implementou *compaction* nativa no Claude Code — ela preserva decisões arquiteturais e bugs em aberto, e descarta tool outputs redundantes. A boa notícia: as técnicas são as mesmas que [[Economia de Tokens|reduzem custo]]. Você ganha qualidade *e* dinheiro.

## Compressão vs pruning vs eviction

| Técnica | O que faz | Quando ativa |
|---|---|---|
| **Compressão** | Mantém a informação, em forma reduzida | Threshold de tokens |
| **Pruning** | Remove informação considerada irrelevante | Filtro contínuo ou pré-LLM |
| **Eviction** | Remove a informação mais antiga (FIFO ou LRU) | Limite hard |

A maioria dos sistemas robustos combina os três.

## Compressão (compaction)

> [!quote] Anthropic — Effective Context Engineering (2025)
> *"Compaction is the practice of taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary."*

### Como Claude Code implementa

1. Quando a janela aproxima do limite, dispara [[Dicionário de IA#context compaction|compactação]]
2. Envia o histórico para o próprio modelo com prompt de sumarização
3. Modelo gera resumo preservando:
   - Decisões arquiteturais
   - Bugs em aberto
   - Detalhes de implementação importantes
4. Modelo descarta:
   - Tool outputs redundantes
   - Mensagens já resolvidas
5. Continua a sessão com **resumo + 5 arquivos mais recentemente acessados**

### Tipos de compressão

| Tipo | Como funciona | Trade-off |
|---|---|---|
| **Sumarização auto-LLM** | Modelo resume o próprio histórico | Perda fina + custo de inferência |
| **Sumarização extractiva** | Seleciona spans importantes do histórico | Sem perda, mas menos compacto |
| **Compactação estrutural** | Converte para formato denso (tabela, JSON) | Preciso, mas exige schema |
| **Hierarchical** | Resumo de resumos | Bom para muito longo prazo |

### Quando comprimir

- **Threshold absoluto** — ao atingir 70-80% da janela
- **Threshold de turno** — a cada N turnos (ex: 50)
- **Trigger explícito** — usuário ou agente pede `/compact`
- **Mudança de fase** — ao terminar uma sub-tarefa

> [!warning] Compactação custa tokens
> Compactar 100K tokens tipicamente envia 100K input + recebe 5-10K output. Não é grátis — mas o ganho de qualidade e o custo evitado nos turnos seguintes superam.

## Pruning (poda ativa)

Diferente de compressão (que **mantém** em forma reduzida), pruning **remove** informação julgada irrelevante.

### Critérios comuns

- **Idade** — descartar mensagens com mais de N turnos
- **Relevância** — TF-IDF, embeddings: remover o que não combina com a tarefa atual
- **Marcação explícita** — agente decide "isso já não importa"
- **Estática** — `.cursorignore`, `.claudeignore`, regex de paths

### Pruning de tool outputs

Pattern essencial em agentes:

```
Turno 1: read_file("src/api.py")  → 12K tokens de output
Turno 2: read_file("src/db.py")   → 8K tokens de output
Turno 3: read_file("src/api.py")  → MESMO conteúdo

Sem pruning: histórico contém 32K tokens de file contents
Com pruning: substitui leituras antigas por referência ("já lido no turno 1")
```

### Pruning de imagens / outputs grandes

Imagens consomem 1-2K tokens cada. Após o agente descrever ou usar, **substitua a imagem pela descrição** no histórico. Mesmo padrão para PDFs, planilhas grandes, screenshots.

## Sliding window — o caso especial

```mermaid
graph LR
    A[Mensagem 1] -.descartada.-> X((⊘))
    B[Mensagem 2] -.descartada.-> X
    C[Mensagem 50] --> D[Janela]
    E[Mensagem 51] --> D
    F[Mensagem 52] --> D
    G[Última] --> D
```

Mantém os **últimos N turnos** + system prompt + memória persistente. Simples, eficiente, mas perde contexto antigo. Bom para chats casuais; **insuficiente** para agentes que precisam recordar decisões iniciais.

## Padrão híbrido recomendado

```python
def compact_history(history, budget=50_000):
    static = history[:2]              # primeiros 2 turnos = "setup"
    recent = history[-10:]            # últimos 10 = "memória curta"
    middle = history[2:-10]           # tudo entre = candidato a compactar

    if total_tokens(static + recent) > budget:
        recent = sliding_window(recent, max_tokens=budget * 0.6)

    middle_summary = summarize_with_llm(middle, target=2_000)

    return static + [middle_summary] + recent
```

## Onde a compaction não basta (long-running)

Tudo acima resolve *uma* sessão que satura. Mas e um agente que cruza **várias** janelas de contexto — um coding agent rodando em loop por horas? Aqui a compaction sozinha trinca. A própria Anthropic é direta sobre isso:

> [!quote] Anthropic — Effective harnesses for long-running agents (nov/2025)
> *"compaction isn't sufficient. Out of the box, even a frontier coding model like Opus 4.5 running on the Claude Agent SDK in a loop across multiple context windows will fall short."*

O problema é de **continuidade**, não de tamanho. Comprimir converte 100K em 10K, mas o resumo ainda vive *dentro* da conversa — e a cada janela nova ele é re-resumido, perdendo nuance de resumo em resumo. O que falta é um estado que sobreviva *fora* da janela, intacto, que a próxima instância possa reler do zero. A receita prescrita é uma tríade de artefatos **estruturados e duráveis** que fazem a ponte entre janelas:

1. **Lista de features/requisitos em JSON** — o backlog do que precisa existir, como dado, não como prosa.
2. **Arquivo de progresso** (`claude-progress.txt`) — o "onde eu parei", para reconstruir o estado de trabalho ao iniciar com uma janela fresca.
3. **Histórico git inicial** — para rastrear e poder reverter mudanças (o undo durável do agente).

Por que JSON e não Markdown para os requisitos? Porque o modelo **tem menos probabilidade de modificá-lo indevidamente** — a rigidez do schema vira uma trava contra a tentação de "melhorar" o checklist no meio do caminho. Markdown convida edição; JSON resiste a ela. É a mesma intuição da *compactação estrutural* lá em cima, agora aplicada não ao histórico, mas ao **contrato** entre janelas.

> [!info] A analogia do turno de plantão
> Pense num hospital trocando de turno. A compaction é o médico que sai resumindo de cabeça o que aconteceu — útil, mas some quando ele vai embora. A tríade durável é o **prontuário**: a lista de problemas (JSON), a evolução do dia (`claude-progress.txt`) e o registro do que foi feito e pode ser desfeito (git). O próximo plantonista não depende da memória de ninguém — ele lê o prontuário. Anthropic chega a observar uma *"context anxiety"* no Sonnet 4.5: o agente que, sem âncora durável, gasta atenção se preocupando com o que pode ter esquecido.

Em síntese: *"finding a way for agents to quickly understand the state of work when starting with a fresh context window... accomplished with the `claude-progress.txt` file alongside the git history."* Onde a compaction acaba — na borda da janela — começa o [[03-Dominios/IA/Anatomia de Agents/11 - Harness engineering — a terceira camada|harness engineering]]: não é mais o que cabe no contexto, é o andaime que persiste *entre* contextos. A instanciação prática disso vive em [[03-Dominios/IA/Claude Code/Mental Model/09 - O harness como terceira camada|O harness como terceira camada]].

## Métricas para acompanhar

| Métrica | Alvo |
|---|---|
| **Compactação rate** | 5-10x (100K → 10-20K) |
| **Loss em testes gold** | <5% (medido com benchmark NIAH na sessão) |
| **Custo de compactação / mês** | <10% do custo total |
| **Frequência de compactação** | A cada 30-50 turnos em sessões longas |

## Armadilhas

- **Compactar cedo demais** — perde nuance que ainda seria útil
- **Compactar tarde demais** — já entrou em [[03 - Context rot e atenção diluída|context rot]]
- **Não preservar decisões críticas** — modelo "esquece" arquitetura combinada
- **Compactar tool outputs ativos** — agente perde resultado que ainda usa
- **Sem teste contra gold** — qualidade da compressão degrada silenciosa

## Veja também

- [[03 - Context rot e atenção diluída]]
- [[05 - Camadas de contexto — persistente, temporal, transiente]]
- [[Economia de Tokens|08 - Compactação de histórico em agentes]]
- [[Economia de Tokens|06 - Context pruning — o que remover do prompt]]
- [[10 - Structured state tracking]]

## Referências

- **Anthropic** — *Effective context engineering for AI agents* (2025).
- **Anthropic** — [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (nov/2025). Nota curta.
- **Claude Cookbook** — *Context engineering: memory, compaction, and tool clearing* (2026).
- **Bojie Li** — *Claude's Context Engineering Secrets* (dez 2025).
- **Sebastian Raschka** — *Components of A Coding Agent* (2025).
