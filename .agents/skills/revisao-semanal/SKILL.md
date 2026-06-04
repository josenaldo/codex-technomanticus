---
name: revisao-semanal
description: Gera um relatório semanal em formato release notes do que foi trabalhado no vault (git log + diffs), com 4 lentes de insight (conhecimento, dificuldades/retrabalho, alertas, conselhos & próximos passos). Grava em `00-Meta/revisoes/<ano>/YYYY-Www.md`. Aciona com "/revisao-semanal", "revisão da semana", "resumo do que trabalhei essa semana", "release notes da semana", ou disparada por cron de sábado. Report-only — NUNCA escreve em arquivos de conteúdo (ex: entradas.md). Portável: nada hardcoded por vault; lê a identidade do grimório em runtime.
---

# Skill: revisao-semanal

Gera um relatório semanal em formato _release notes_ do que foi trabalhado no vault na última janela, derivando o changelog do `git log` e aplicando quatro lentes de insight. O relatório é a **entrada** da reflexão do usuário, não a reflexão — então extrai o máximo de insight útil sozinho. **Report-only:** escreve apenas o relatório; nunca toca em arquivos de conteúdo.

## Quando usar

- Usuário invoca `/revisao-semanal`.
- Usuário diz "revisão da semana", "resumo do que trabalhei", "release notes da semana".
- Disparada pelo cron de sábado (`claude -p "/revisao-semanal"`).

## Quando NÃO usar

- Auditoria estrutural (links quebrados, órfãs, frontmatter) → isso é o `health-audit.py` / `/verificar-wikilinks`, não esta skill.
- Quando o usuário quer promover trabalho pro pipeline → use `/promover-glosa`, `/sintetizar-glosas` (esta skill só sugere, não executa).

## Argumentos

Sem argumentos. A janela é resolvida automaticamente.

## Fluxo de execução

1. **Resolver a janela (resiliente a gaps):**
   - Listar relatórios existentes: `ls 00-Meta/revisoes/*/*.md 2>/dev/null`.
   - Se houver, pegar o mais recente e ler `periodo_fim` do frontmatter → `since = periodo_fim`.
   - Se não houver nenhum, `since =` 7 dias atrás (`date -d '7 days ago' +%F`) e marcar no corpo que é a **primeira revisão**.
   - `until =` hoje (`date +%F`).
   - Label da semana = semana ISO da data-fim: `date -d <until> +%G-W%V` → ex. `2026-W23`.

2. **Coletar o sinal objetivo (git):**

   ```bash
   git log --since="$since" --until="$until" --pretty=format:'%h|%ad|%s' --date=short
   git log --since="$since" --until="$until" --numstat --pretty=format:'%H'
   git log --since="$since" --until="$until" --diff-filter=A --name-only --pretty=format:
   git log --since="$since" --until="$until" --diff-filter=D --name-only --pretty=format:
   git log --since="$since" --until="$until" --diff-filter=R --name-status --pretty=format:
   ```

   - Agregar linhas +/− por arquivo (numstat) → **churn**.
   - **Ignorar mensagens `vault backup: <timestamp>`** como narrativa; derivar o changelog dos arquivos alterados.

3. **Classificar arquivos por zona/sinal:**
   - `02-Glosas/**` → **o que o usuário leu/fichou**.
   - `03-Dominios/**` (TODOS os domínios, nenhum privilegiado) → **o que produziu/integrou**.
   - **Notas diárias** → ler `.obsidian/daily-notes.json` (`folder`, `format`; default raiz + `YYYY-MM-DD`); se ausente mas `daily-notes` estiver em `.obsidian/core-plugins.json`, assumir raiz+`YYYY-MM-DD`; checar também `.obsidian/plugins/periodic-notes/data.json`. Arquivos casando = **trabalho do dia-a-dia**.
   - `04-Sendas/**` → só referência; entra no changelog se mudou, **não** conta como aprendizado.
   - `00-Meta/**`, `docs/**` → meta-trabalho; só changelog.

4. **Ler conteúdo das notas de maior churn** (não todas) via `git diff` ou `Read`, para alimentar as lentes de insight com substância real.

5. **Aplicar as 4 lentes:**
   - **💡 Insights de conhecimento:** temas recorrentes e conexões entre domínios nas notas tocadas; sínteses possíveis (ex: "3 notas tocaram RAG → candidata a `/sintetizar-glosas`").
   - **🧗 Dificuldades & retrabalho:** churn alto, commits `fix`/`revert`, trabalho recuperado de stash → onde houve atrito.
   - **⚠️ Alertas & dívidas:** notas criadas mas curtas/sem conclusão, headings vazios, TODOs no diff, notas sem título. **Não** repetir auditoria estrutural — foco em incompletude de conteúdo.
   - **🎯 Conselhos & próximos passos:** des-ancorado de domínio. Ler `index.md` (manifesto do grimório) como "norte" = cultivar evergreen via glosas→domínios. Avaliar: glosas maduras pra `/promover-glosa`/`/sintetizar-glosas`; domínios que ganharam massa; lacunas; o que ler/produzir a seguir. **Só no relatório.**

6. **Escrever o relatório** em `00-Meta/revisoes/<ano>/YYYY-Www.md` (criar `<ano>/` com `mkdir -p`). Usar o nome do vault (do `# título` em `index.md`, ou o basename do diretório-raiz) no header do release. As 4 lentes são SEMPRE renderizadas; se uma não tiver achado, escrever "nada digno de nota".

7. **Reportar ao usuário** (no chat, quando interativo) o path do relatório e o TL;DR.

## Formato do relatório

Frontmatter:

```yaml
---
title: "Revisão Semanal — 2026-W23"
type: revisao
publish: false
semana: 2026-W23
periodo_inicio: 2026-06-01
periodo_fim: 2026-06-07
created: 2026-06-07
tags:
  - meta
  - revisao-semanal
---
```

> **Sempre `publish: false`** — relatórios de revisão são privados e não vão pro site público (Quartz publica quando `publish` é `true` ou ausente).

Corpo:

```markdown
# <Vault> — Release 2026.W23  (01–07 jun)

> [!abstract] TL;DR
> 1–2 frases: foco da semana + achado mais importante.

## 📦 Changelog
### ✨ Adicionado
### 📝 Refinado
### 🗑 Arquivado/Movido
_Rodapé: N commits · M arquivos · +X/−Y linhas_

## 💡 Insights de conhecimento
## 🧗 Dificuldades & retrabalho
## ⚠️ Alertas & dívidas
## 🎯 Conselhos & próximos passos
```

## Edge cases

| Caso | Comportamento |
|---|---|
| Janela vazia (sem commits) | Relatório curto: "sem atividade registrada nesta janela" |
| Sem relatório anterior | Janela de 7 dias + nota "primeira revisão" |
| Re-run no mesmo período | Sobrescrever o arquivo da semana (idempotente) |
| Run headless falha (auth/claude) | Falha visível no `.cron.log`; relatório só é escrito no passo final, então nada é corrompido |
| Lente sem achado | Renderizar a seção com "nada digno de nota" |

## Convenções

- **Report-only:** NUNCA escreve em `01-Pergaminhos/entradas.md` nem em qualquer arquivo de conteúdo. Conselhos vivem só no relatório.
- **`publish: false`** em todo relatório — conteúdo meta privado, fora do site.
- **Nenhum domínio privilegiado:** a análise gravita em torno de glosas + domínios + notas diárias trabalhados.
- **Ruído do git:** `vault backup: <timestamp>` não vira narrativa.
- **Portável:** nada hardcoded por vault; a identidade vem de `index.md` e a pasta de daily notes vem da config do Obsidian em runtime.
