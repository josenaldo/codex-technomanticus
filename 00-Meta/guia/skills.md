---
title: "Skills do vault (Codex)"
created: 2026-05-24
updated: 2026-06-24
type: how-to
status: seedling
tags:
  - guia
  - meta
  - skills
publish: false
---

# Skills do vault (Codex)

Catálogo das **20 skills** salvas em `.agents/skills/` — expostas ao Claude Code pelo symlink `.claude/skills → ../.agents/skills`. Dividem-se em dois grupos:

- **14 skills autorais** (PT-BR), construídas pro pipeline deste vault.
- **6 ferramentas de terceiros** (utilitários genéricos de Obsidian/web), versionadas no repo.

Skills globais do Claude Code (Anthropic, superpowers) não estão aqui — só o que vive neste repositório.

Cada skill é um arquivo `SKILL.md` invocado por slash command (`/<nome>`) ou linguagem natural correspondente. O Claude Code carrega o conteúdo quando o gatilho é acionado e executa os passos descritos.

Para o pipeline geral do vault, veja [[workflow]]. Para o mapa das zonas, [[Como usar este vault]].

## Mapa por domínio

| Domínio                                | Skills                                                                                       | Quando entra no fluxo                                   |
| -------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| **Fichamento de leitura (Glosas)**     | `/glosa`, `/arquivar-glosas`, `/acordar-glosas`, `/promover-glosa`, `/sintetizar-glosas`     | Captura → destilação → integração de artigos web        |
| **Escrita e qualidade**                | `/escrever-nota`, `/verificar-nota`, `/adicionar-midia`                                      | Criação de notas + gate de qualidade + enriquecimento com mídia |
| **Enriquecimento e manutenção**        | `/enriquecer-nota`, `/plantar-duvidas`, `/colher-duvidas`, `/verificar-wikilinks`            | Refino de notas + dúvidas de leitura + higiene de links |
| **Glossários (transversal)**           | `/verbete`                                                                                   | Adicionar termo a qualquer glossário do vault           |
| **Revisão & Meta**                     | `/revisao-semanal`                                                                           | Relatório semanal (release notes) do trabalho no vault  |
| **Ferramentas instaladas (terceiros)** | `defuddle`, `deadlink`, `obsidian-markdown`, `obsidian-bases`, `obsidian-cli`, `json-canvas` | Utilitários genéricos acionados sob demanda             |

---

## Escrita e qualidade

Pipeline de criação e verificação de notas de domínio. Três skills formam um ciclo: `/escrever-nota`
cria com padrão "capítulo de livro"; `/verificar-nota` audita o resultado; `/adicionar-midia` enriquece
com fontes multimídia. O mesmo ciclo se aplica quando `/enriquecer-nota` ativa o Modo B (elevação
estrutural de notas antigas).

O eixo intelectual de tudo é a **Técnica Feynman**: escrever como quem ensina, não como quem cataloga.
Problema-primeiro, analogia antes da técnica, mecanismo explicado (por quê, não só o quê), pergunta
do leitor antecipada.

### `/escrever-nota [path] [instrução]`

Cria nota nova de domínio do zero. **Núcleo mínimo obrigatório** (frontmatter, TL;DR, abertura com
problema, mecanismo, O que vem a seguir, fontes) + **menu de seções opcionais** escolhido por tema
(diagramas Mermaid, casos práticos, armadilhas, inglês, código, teoria). Sem template rígido — cada
tema escolhe o que faz sentido.

- **Registro Feynman explícito** em cada seção de conteúdo: problema-primeiro, analogia concreta,
  por quê (não só o quê), pergunta retórica do leitor, resumo em 1 linha.
- **Pesquisa antes de escrever** (3-5 fontes autoritativas por WebSearch).
- **Confirmação antes de salvar** — mostra rascunho completo.
- **Invoca `/verificar-nota`** automaticamente ao final como gate de qualidade.
- **Quando usar:** "criar nota", "escrever nota sobre X", "nova nota", "começar o galho Y".

### `/verificar-nota [path]`

Constraint-skill: audita a qualidade estrutural de uma nota contra o padrão do vault. **Não edita.**
Reporta score por seção e sugere qual skill usar para corrigir cada item faltando.

Cinco seções auditadas:

- **ESTRUTURA** (8 itens): TL;DR denso, abertura com problema, diagrama Mermaid, casos práticos,
  "O que vem a seguir", seção de inglês, tabela PT↔EN, armadilhas comuns.
- **PROFUNDIDADE** (3 itens): código com falha, mecanismo explicado, teoria subjacente (Magus).
- **TAMANHO** (1 item por fase): ≥300 linhas (Iniciado), ≥400 (Adepto), ≥500 (Magus).
- **LINKS** (2 itens): wikilink cross-galho, referência externa.
- **MÍDIA** (1 item): callout `[!tip]` com vídeo/podcast.

Score de aprovação: ≥9/12 ✓. Score crítico: <6/12 → ativa Modo B em `/enriquecer-nota`.

- **Quando usar:** "verificar nota", "auditar qualidade", "gate de qualidade". Roda automaticamente
  após `/escrever-nota` e na Fase 0 do `/enriquecer-nota`.

### `/adicionar-midia [path] [instrução]`

Pesquisa vídeos (YouTube) e podcasts (com transcrição disponível), baixa legendas via `uvx yt-dlp`,
analisa relevância e embute os aprovados como callouts `[!tip]` na nota.

- **Regra de ouro:** nunca embutir sem ter lido a transcrição. Sem legenda = descarta.
- **Podcasts:** EN apenas, transcrição obrigatória.
- **Score de relevância** (0-10): alinhamento, profundidade, qualidade pedagógica. Threshold: ≥7.
- **Máximo 2 mídias por nota** (exceção: capstone >600 linhas → até 3).
- **Quando usar:** "adicionar vídeo", "embutir vídeo", "buscar vídeo sobre X", "podcast sobre X".
  Também invocada pela lente Mídia do `/enriquecer-nota`.

---

## Fichamento de leitura (Glosas)

Fluxo de fichamento de artigos web: capturar bruto → arquivar inativos → reativar quando precisar → promover ao status de nota de domínio. É a coluna vertebral da automação do vault (passos "captura → destilação → integração" do [[workflow]]).

### `/glosa <url>`

Cria fichamento (Glosa) de artigo web a partir de URL, em `02-Glosas/<ano>-<slug>.md`.

- **Quando usar:** pedir pra fichar/catalogar/registrar um artigo, falar em "ficha de leitura", "fichamento", "glosa", ou compartilhar uma URL pedindo registro.
- **Não suporta:** PDFs, vídeos (YouTube/Vimeo), podcasts (Spotify) ou tweets/redes sociais — nesses casos, avisa e aborta.
- **Output:** ficha com frontmatter completo, TL;DR e Pontos-chave em PT-BR, citações verbatim na língua original, e **Meu comentário** vazio (o campo onde a ficha vira sua).
- **Limpeza automática:** remove o link de `01-Pergaminhos/entradas.md` se ele estava lá.

### `/arquivar-glosas`

Move glosas inativas há mais de 30 dias em `02-Glosas/` raiz pra `02-Glosas/Arquivadas/<ano>/`. Pede confirmação antes de mover.

- **Critério de inatividade:** `hoje - max(updated, mtime) > 30 dias`.
- **Aplica-se a TODAS** as glosas na raiz, independente de `progresso`. Glosas em `Promovidas/` não são afetadas.
- **Não deleta** — só move pra `Arquivadas/`.
- **Quando usar:** "arquivar glosas antigas", "limpar glosas paradas".

### `/acordar-glosas <criterio>`

Reativa glosas previamente arquivadas em `02-Glosas/Arquivadas/<ano>/`.

- Move pra raiz `02-Glosas/`, reseta `progresso: andamento`, atualiza `updated`.
- **Filtros aceitos:** slug, `tag:<X>`, assunto (busca textual) ou modo interativo.
- **Não mexe em `Promovidas/`** — glosas promovidas são histórico imutável.
- **Quando usar:** "reativar glosas sobre X", "tirar glosas do arquivo", "acordar glosas pra estudar X".

### `/promover-glosa <slug>`

Promove **uma glosa** em `02-Glosas/` para uma nota nova em `03-Dominios/`.

- Cria a nota usando `Template - Nota`, com a TL;DR da glosa como ponto de partida e `## Fontes` populada com wikilink pra glosa.
- Move a glosa pra `02-Glosas/Promovidas/<ano>/`, atualiza `promovida_em` no frontmatter.
- **Aceita** slug, wikilink ou modo interativo (lista glosas com `progresso` em `andamento`/`feito`).
- **Quando usar:** "promover glosa", "criar nota a partir dessa glosa", "esta glosa merece nota".

### `/sintetizar-glosas <criterio>`

Consolida **várias glosas em UMA nota nova** de domínio.

- Prepara o esqueleto da nota com `## Fontes` populada com wikilinks pras N glosas selecionadas; **não** escreve a síntese em prosa — esse trabalho cognitivo fica com você.
- Move cada glosa pra `02-Glosas/Promovidas/<ano>/`, atualiza `promovida_em` em cada uma.
- **Filtros:** `tag:<X>`, assunto, ou modo interativo.
- **Quando usar:** "sintetizar glosas sobre X", "consolidar essas glosas em uma nota".

---

## Enriquecimento e manutenção

Skills que atuam sobre notas já existentes em `03-Dominios/` — refinando conteúdo e garantindo a integridade dos links antes da publicação via Quartz.

### `/enriquecer-nota [path] [instrução]`

Enriquece uma nota com **5 lentes selecionáveis** (profundidade, lacunas, novidade com fonte, conexões, mídia), filtradas por um **subagente crítico calibrado pela fase**. 8 fases: **diagnosticar → identificar alvo → escolher lentes → analisar → criticar → planejar → executar → reportar**. Nunca edita sem confirmação; reescritas aparecem como diff.

**Dois modos de operação** (escolhidos automaticamente pela Fase 0 com `/verificar-nota`):
- **Modo A — Incremental** (score ≥6/12): enriquece conteúdo via lentes selecionadas.
- **Modo B — Elevação** (score <6/12): reconstrói seções estruturais ausentes com Registro Feynman, depois enriche. Para notas antigas e fracas (ex: notas do período inicial do vault).

- Adiciona wikilinks para termos já presentes no dicionário do domínio, cria verbetes ausentes (via `/verbete`), busca referências externas e atualiza frontmatter.
- **Lente Mídia** delega para `/adicionar-midia` ao final da execução.
- **Sem `path`:** pergunta qual nota enriquecer. **Com `path`:** usa o arquivo indicado (relativo à raiz do vault).
- **Quando usar:** "enriquecer", "melhorar", "atualizar" ou "revisar" uma nota.

O loop de dúvidas de leitura é um **par simétrico**: `/plantar-duvidas` (preventiva) encontra a confusão; `/colher-duvidas` (resolutiva) a transforma em texto melhor. Ambas operam sobre callouts `> [!duvida]` — matéria-prima transitória que **não deve sobreviver a um `git push`**.

### `/plantar-duvidas [path]`

A ponta **preventiva**: lê a nota/galho como um iniciante e **planta** callouts `> [!duvida]` nos pontos que travam o aprendizado — peças sem encaixe ("lista de ingredientes"), saltos de dependência, essencial escondido em callout colapsado.

- **Só planta, não resolve** — a resolução é da `/colher-duvidas`, rodada em seguida.
- Escreve a pergunta **na voz do iniciante** (calibrada pela `fase:` da nota); confirma antes de gravar; não altera o conteúdo.
- **Quando usar:** "plantar dúvidas", "ler como cético/iniciante", "achar os pontos confusos antes de eu travar".

### `/colher-duvidas [path] [dúvidas soltas]`

A ponta **resolutiva**: varre os `> [!duvida]` da nota/galho (ou dúvidas ditas na conversa) e, para cada um, faz a **decisão editorial** — **consertar o fluxo** (dúvida essencial) ou promover a um `> [!question]` polido (tangente legítima). Fecha o loop **capturar → colher → evoluir** do padrão [[Convenções de escrita|capítulo de livro]].

- Plano com diff; nunca edita sem confirmar.
- Regra de ouro: callout é para o *interessante saber*; o fluxo é para o *preciso saber* — nunca remendar conceito central num FAQ.
- **`[!duvida]` é transitório** — renderiza no site; colha antes do `git push`.
- **Quando usar:** "colher dúvidas", "evoluir a nota com minhas dúvidas", ou depois de travar num capítulo durante o estudo.

### `/verificar-wikilinks <pasta>`

Detecta e corrige wikilinks/links markdown quebrados, aplicando a **regra do Quartz**: `[[Pasta]]` só funciona se a pasta tiver `index.md`.

- Roda um detector Python (`scripts/check_wikilinks.py`) que gera um relatório JSON; a skill lê o JSON, agrupa as quebras por motivo e propõe um plano de correção.
- **Quando usar:** após renomear/mover notas, antes de publicar no site Quartz; ou "checar links quebrados", "auditar wikilinks", "consertar links da MOC".
- **Difere de `deadlink`:** esta cuida de links *internos* do vault; `deadlink` audita URLs *externas* (HTTP).

---

## Glossários (transversal)

### `/verbete <termo>[: <definição>]`

Adiciona um verbete a um glossário de domínio do vault.

- **Modo manual:** termo + definição fornecidos → insere direto em ordem alfabética na seção correta.
- **Modo pesquisa** (mais comum): só o termo → pesquisa, propõe definição, confirma com você antes de inserir.
- **Localiza o glossário-alvo** pelo frontmatter `type: glossary`. Aceita hint (ex: "adiciona ao Dicionário de IA").
- **Idempotente:** termo já existente → aborta sem modificar, mostra a definição atual.
- **Usado por outras skills:** `/enriquecer-nota` delega a criação de verbetes ausentes aqui.

---

## Revisão & Meta

Skill de observabilidade do próprio vault — não produz conhecimento, **resume** o que foi produzido. Roda automática por cron, mas o relatório é a *entrada* da reflexão do usuário, não a reflexão.

### `/revisao-semanal`

Gera um relatório semanal em **formato release notes** do que foi trabalhado no vault, gravado em `00-Meta/revisoes/<ano>/YYYY-Www.md` (sempre `publish: false` — meta privado, fora do site).

- **Sinal primário:** `git log` + diffs do obsidian-git (não depende de daily notes). Janela **resiliente a gaps** — "desde o último relatório" (fallback 7 dias), então um sábado perdido é coberto pela semana seguinte.
- **Ruído tratado:** commits `vault backup: <timestamp>` são ignorados como narrativa; o changelog vem dos arquivos alterados, agrupados por zona/domínio.
- **Pesagem do sinal:** Glosas = o que leu/fichou; Domínios = o que produziu/integrou; notas diárias = trabalho do dia-a-dia; Sendas = só referência (não conta como aprendizado). **Nenhum domínio privilegiado.**
- **4 lentes de insight:** 💡 conhecimento (conexões, sínteses possíveis), 🧗 dificuldades & retrabalho (churn, `fix`/`revert`, stash), ⚠️ alertas & dívidas (incompletude de conteúdo — **não** duplica auditoria estrutural), 🎯 conselhos & próximos passos (des-ancorado de domínio, lê `index.md` como "norte").
- **Report-only:** NUNCA escreve em arquivos de conteúdo (ex: `01-Pergaminhos/entradas.md`). Conselhos vivem só no relatório; o usuário promove o que quiser manualmente.
- **Agendada:** cron local de sábado via `00-Meta/scripts/revisao-semanal.sh` → `claude -p "/revisao-semanal"` headless. Também invocável manualmente.
- **Quando usar:** "revisão da semana", "resumo do que trabalhei", "release notes da semana".

Complementada pelo `00-Meta/scripts/health-audit.py` (auditoria estrutural — links, órfãs, frontmatter, skill drift), agendado na sexta. Veja [[Manutenção do vault]].

---

## Ferramentas instaladas (skills de terceiros)

Utilitários genéricos versionados em `.agents/skills/`. Não são autorais do vault, mas estão disponíveis e o Claude Code os aciona automaticamente quando o contexto bate.

| Skill                | O que faz                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| **`defuddle`**       | Extrai markdown limpo de páginas web via Defuddle CLI, removendo navegação e clutter (economiza tokens). Preferida ao WebFetch pra páginas comuns; **não** pra URLs `.md`. |
| **`deadlink`**       | Varre sites e arquivos atrás de links quebrados, com detalhe de status HTTP. Para auditar URLs externas.     |
| **`obsidian-markdown`** | Cria/edita Obsidian Flavored Markdown: wikilinks, embeds, callouts, properties e demais sintaxes específicas. |
| **`obsidian-bases`** | Cria/edita arquivos `.base` (views, filtros, fórmulas, summaries) — visões tipo banco de dados das notas.    |
| **`obsidian-cli`**   | Interage com uma instância do Obsidian rodando via CLI (ler, criar, buscar, gerenciar notas; e dev de plugins/temas). |
| **`json-canvas`**    | Cria/edita arquivos `.canvas` (nós, arestas, grupos) — mapas mentais e fluxogramas no padrão JSON Canvas 1.0. |

---

## Convenções gerais

- **Localização:** todas as skills vivem em `.agents/skills/<nome>/SKILL.md`. O Claude Code as enxerga pelo symlink `.claude/skills → ../.agents/skills`.
- **Invocação:** slash command (`/<nome>`) ou linguagem natural — cada `SKILL.md` autoral tem seção "Quando usar" com gatilhos.
- **Confirmação antes de mexer:** skills destrutivas ou de larga escala (`/arquivar-glosas`, `/enriquecer-nota`, `/sintetizar-glosas`) pedem confirmação antes de mover/editar arquivos.
- **Idempotência:** skills que mantêm índices ou glossários (`/verbete`) não destroem trabalho ao re-rodar — termo existente aborta sem modificar.
- **Trabalho cognitivo fica com o usuário:** `/glosa` deixa **Meu comentário** vazio; `/sintetizar-glosas` não escreve a síntese em prosa. A skill prepara o scaffold, você pensa.
- **Histórico imutável:** glosas em `02-Glosas/Promovidas/` (promovidas) não são tocadas por `/acordar-glosas` nem `/arquivar-glosas`.

## Manutenção

Quando adicionar/remover uma skill autoral:

1. Edita `.agents/skills/<nova-skill>/SKILL.md`.
2. **Atualiza esta página** com a entrada nova no domínio correto (ajusta contagem no topo: 20 total, 14 autorais).
3. Se a skill é parte do pipeline principal, atualiza também [[workflow]].
4. Se a skill é nova no fluxo central do vault, considera um atalho no `CLAUDE.md` raiz.

## Veja também

- [[Como usar este vault]] — mapa estático das zonas do vault.
- [[workflow]] — pipeline cognitivo + a skill `/glosa` no fluxo.
- [[00-Meta/guia/pipeline/index|Pipeline]] — ciclo de vida das notas (Pergaminhos → Glosas → Domínios → Sendas).
- [[Manutenção do vault]] — rotinas de higiene onde `/arquivar-glosas` e `/verificar-wikilinks` entram.
