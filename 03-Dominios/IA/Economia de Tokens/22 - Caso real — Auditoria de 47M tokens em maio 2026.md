---
title: "Caso real — Auditoria de 47M tokens em maio 2026"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
progresso: andamento
publish: true
tags:
  - economia-tokens
  - ia
  - custos
  - auditoria
  - claude-code
aliases:
  - Caso real 47M tokens
  - Auditoria maio 2026
  - Caso 47M
---

# Caso real — Auditoria de 47M tokens em maio 2026

> [!abstract] TL;DR
> Auditoria de uso pessoal em maio de 2026: **47.2M tokens em 32 dias, 73.3% em Opus 4.7**. Cinco vetores de gasto identificados via `ccusage blocks` e `rtk gain`: hook RTK desligado em quase todas as sessões (sangrando ~2.1M tokens), sessões de 8h+ sem `/clear`, abuso de `general-purpose` em buscas simples, default invertido para Opus em vez de Sonnet, e contexto >150k em 85% do uso. Fix mais barato e maior impacto: reativar o hook RTK no `settings.json`. Plano por ROI fecha a economia projetada em ~60-80% sem perda de capacidade.

## Contexto

Auditoria executada em **maio de 2026** sobre meu uso pessoal do [[03-Dominios/IA/Claude Code/index|Claude Code]] em projetos de produção (entre eles, MedEspecialista API com 1.900+ testes). A motivação foi uma fatura próxima do teto do plano e a percepção subjetiva de que o uso estava "fora de calibração".

**Ferramentas usadas no diagnóstico:**

- `ccusage` ([[04 - Monitoramento — ccusage, Langfuse, dashboards|nota 04]]) — breakdown diário, por modelo, por janela de billing de 5h
- `rtk gain` — relatório de comandos passados por [[21 - Hacks de trincheira — Claude, Gemini e Copilot em 2026#3. RTK (Rust Token Killer)|RTK]] vs comandos crus
- Inspeção de `settings.json` global e de projeto pra checar hooks ativos
- Leitura dos logs JSONL locais do Claude Code

**Foto inicial:**

| Indicador | Valor | Diagnóstico |
| --- | --- | --- |
| Tokens em 32 dias | 47.2M | Multiplicador principal: mix de modelo |
| Distribuição por modelo | 73.3% Opus 4.7 | Invertido em relação ao policy declarada |
| Comandos Bash totais | 23.908 | Volume normal pra uso intenso |
| Comandos via RTK | 65 (0.3%) | **Hook desligado em quase todas as sessões** |
| Subagentes (% do uso) | 54% | `general-purpose` sozinho = 8% |
| Subagentes `superpowers:*` | 19% | Skills carregam instruções pesadas |
| Sessões com contexto >150k | 85% | Sessões longas sem `/clear` |

## Os cinco vetores

### Vetor 1 — Hook RTK desligado (~2.1M tokens vazando)

Dos 23.908 comandos Bash, só **65 (0.3%)** passaram pelo [[21 - Hacks de trincheira — Claude, Gemini e Copilot em 2026#3. RTK (Rust Token Killer)|RTK]]. Quando funciona (4.927 comandos numa sessão isolada), economia medida foi de **85.6%**. Fora dele, o sangramento foi concentrado em:

| Comando | Frequência | Tokens estimados |
| --- | --- | --- |
| `git log` | 4.025× | 639K |
| `grep -rn` | 2.545× | 376K |
| `find` | 1.368× | 230K |
| `ls -la` | 1.460× | 111K |
| `tail -30` | 1.095× | 265K |

**Causa raiz:** o hook RTK do Claude Code que reescreve `git status` → `rtk git status` estava ausente do `settings.json` de alguns projetos, ou falhando silenciosamente. Verificação:

```bash
rtk --version && which rtk
cat ~/.claude/settings.json | grep -i rtk
cat /home/josenaldo/repos/medespecialista/api/.claude/settings.json 2>/dev/null | grep -i rtk
```

**Fix:** garantir o hook RTK em `settings.json` global + projetos ativos. Esforço: 5 minutos. Economia projetada: ~2.1M tokens/30 dias.

### Vetor 2 — Sessões de 8h+ sem `/clear`

Em um dia típico de pico, 88% do uso veio de duas sessões longas. Mesmo com [[Dicionário de IA#Prompt caching|prompt caching]] ativo, cada turno relê 150k+ de contexto. O `auto-compact` está ligado, mas dispara tarde demais — quando ele aciona, o estrago já foi feito.

Esse é o vetor descrito conceitualmente em [[03 - Por que agentes gastam tanto#1. Acumulação de contexto turno-a-turno|Vetor 1 de "Por que agentes gastam tanto"]], só que medido na prática.

**Fix (hábito, não config):**

- `/clear` ao trocar de tarefa — quase nunca precisei do histórico anterior
- `/compact` proativo quando o contexto passa de ~100k, sem esperar o auto
- Auditar background loops esquecidos (skill `loop` em modo dynamic dorme caro)

### Vetor 3 — Subagentes inflados (54% do uso)

Cada [[10 - Sub-agentes especializados|subagente]] é uma chamada Claude separada com contexto próprio. `general-purpose` sozinho consumiu **8%**, e os subagentes `superpowers:*` somados **19%** — cada skill desse plugin carrega instruções pesadas além de rodar seus próprios agentes.

**Fix:**

- Pra **buscas de código:** usar `Explore` (read-only, mais barato) em vez de `general-purpose`
- Pra **investigação simples (1-2 arquivos):** Bash/Grep direto, sem delegar
- Reservar `general-purpose` pra investigações genuinamente multi-passo
- Auditar quais skills `superpowers:*` realmente valem o custo — usar só quando o framework é necessário, não pra tarefa atômica

### Vetor 4 — Default invertido (73.3% em Opus)

Meu `CLAUDE.md` declara: *"Standard (Sonnet) é default, Opus só pra refactor arquitetural/ADR"*. A prática estava invertida — sessões antigas em Opus eram continuadas por inércia, e novas sessões abriam em Opus por hábito.

Esse é o erro genérico mapeado em [[09 - Model routing — modelo certo para a tarefa|Model routing]], aplicado a um caso pessoal: o policy existe, mas não é aplicado.

**Fix:**

- `/model sonnet` como default em sessões novas
- Manter Opus pra: ADRs, decisões cross-layer, debugging difícil, planejamento complexo
- Tarefas que **não** precisam de Opus: testes, lint, docs, JSDoc, traduções, fix de import, criar componente seguindo padrão

### Vetor 5 — Contexto >150k em 85% do uso

Casado com Vetor 2. O cache atenua, mas não zera — toda saída de tool re-entra no contexto e infla a próxima rodada. Sintoma clássico de "[[16 - Auditoria de consumo#1. Tools verbosos sem filtro|tools verbosos sem filtro]]" e "[[16 - Auditoria de consumo#2. Histórico não compactado em sessão longa|histórico não compactado]]" do checklist de top offenders.

**Fix:**

- `Read` em arquivo grande: usar `offset`/`limit` em vez de ler 2000 linhas
- Comandos de saída grande (test runs, find, git log): usar `rtk` (filtra) ou `head`/`tail` específico
- Investigações com muita saída: delegar pra `Explore` (saída fica isolada, retorna só o resumo)

## Plano de economia, por ROI

| # | Ação | Esforço | Economia estimada |
| --- | --- | --- | --- |
| 1 | Reativar hook RTK em todas as sessões | 5 min | ~2.1M tokens/30 dias |
| 2 | Default `/model sonnet`, Opus sob demanda | 0 min | ~40-60% por sessão típica |
| 3 | `/clear` ao trocar tarefa, `/compact` proativo | hábito | ~30% em sessões longas |
| 4 | Trocar `general-purpose` por `Explore` em buscas | hábito | ~5-8% direto |
| 5 | Reduzir paralelismo (queue 4+ sessões) | hábito | ~36% suavizado |
| 6 | Auditar plugin `superpowers` — qual skill realmente vale? | 30 min | até 19% |

**Ordem importa:** #1 é o único de fix técnico — 5 minutos de trabalho, impacto direto e mensurável. Os outros são hábito e exigem disciplina de sessão.

## Nota sobre paralelismo (36%)

Estava rodando 4+ sessões simultâneas "desde de manhã" — várias features em paralelo via [[03-Dominios/IA/Claude Code/Workflows/06 - Sessões paralelas|tmux + worktrees]]. Isso aparece nos números como aceleração do consumo dentro da janela de billing de 5h.

**Todas as sessões dividem o mesmo limite semanal.** Se as sessões não precisam ser simultâneas (ex: uma está esperando review enquanto outra implementa), preferir **serial** — mesmo trabalho entregue, custo distribuído mais uniformemente nas janelas de billing, e o cache de prompt é melhor aproveitado dentro de cada janela.

## O que aprendi

1. **Hook silencioso = economia silenciosamente perdida.** Sem `rtk gain` na cadência mensal, nunca teria detectado que o hook RTK estava inativo em projetos onde eu *achava* que estava rodando. Lição: monitorar a ferramenta de monitoramento.
2. **Policy escrito ≠ policy aplicado.** Ter `"Sonnet é default"` no `CLAUDE.md` não fez Sonnet ser o default. Defaults importam mais que regras escritas — `/model sonnet` no início da sessão tem mais peso que qualquer parágrafo em memória.
3. **Subagentes não são grátis.** O hábito de delegar pra `general-purpose` "por garantia" custa mais que abrir o arquivo direto. A pergunta certa é "essa tarefa precisa de contexto próprio?", não "isso parece complexo o suficiente pra delegar?".
4. **Auditoria é hábito, não evento.** O custo só pulou no radar porque a fatura assustou. Cadência mensal de `ccusage` + `rtk gain` teria detectado os 5 vetores antes de a fatura escalar — exatamente o ponto de [[16 - Auditoria de consumo]].

## Veja também

- [[03 - Por que agentes gastam tanto]] — o framework conceitual dos vetores diagnosticados aqui
- [[04 - Monitoramento — ccusage, Langfuse, dashboards]] — ferramentas usadas no diagnóstico
- [[09 - Model routing — modelo certo para a tarefa]] — Vetor 4 explicado em geral
- [[10 - Sub-agentes especializados]] — Vetor 3 explicado em geral
- [[16 - Auditoria de consumo]] — workflow genérico de auditoria; esta nota é uma aplicação
- [[18 - Playbook de economia — checklist completo]] — checklist mestre que organiza estes fixes
- [[21 - Hacks de trincheira — Claude, Gemini e Copilot em 2026]] — outro caso real (MedEspecialista) com ângulo de memória/permissões

## Referências

- `ccusage` — [GitHub ryoppippi/ccusage](https://github.com/ryoppippi/ccusage)
- RTK (Rust Token Killer) — uso interno como hook do Claude Code
