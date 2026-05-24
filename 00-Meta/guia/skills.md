---
title: "Skills do vault (Codex)"
created: 2026-05-24
updated: 2026-05-24
type: how-to
status: seedling
tags:
  - guia
  - meta
  - skills
publish: false
---

# Skills do vault (Codex)

Catálogo das **14 skills** salvas em `.agents/skills/` — expostas ao Claude Code pelo symlink `.claude/skills → ../.agents/skills`. Dividem-se em dois grupos:

- **8 skills autorais** (PT-BR), construídas pro pipeline deste vault.
- **6 ferramentas de terceiros** (utilitários genéricos de Obsidian/web), versionadas no repo.

Skills globais do Claude Code (Anthropic, superpowers) não estão aqui — só o que vive neste repositório.

Cada skill é um arquivo `SKILL.md` invocado por slash command (`/<nome>`) ou linguagem natural correspondente. O Claude Code carrega o conteúdo quando o gatilho é acionado e executa os passos descritos.

Para o pipeline geral do vault, veja [[workflow]]. Para o mapa das zonas, [[Como usar este vault]].

## Mapa por domínio

| Domínio                                | Skills                                                                                   | Quando entra no fluxo                                       |
| -------------------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **Fichamento de leitura (Glosas)**     | `/glosa`, `/arquivar-glosas`, `/acordar-glosas`, `/promover-glosa`, `/sintetizar-glosas` | Captura → destilação → integração de artigos web            |
| **Enriquecimento e manutenção**        | `/enriquecer-nota`, `/verificar-wikilinks`                                               | Refino de notas + higiene de links antes de publicar        |
| **Glossários (transversal)**           | `/verbete`                                                                               | Adicionar termo a qualquer glossário do vault               |
| **Ferramentas instaladas (terceiros)** | `defuddle`, `deadlink`, `obsidian-markdown`, `obsidian-bases`, `obsidian-cli`, `json-canvas` | Utilitários genéricos acionados sob demanda                 |

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

Enriquece uma nota do vault em cinco fases: **identificar alvo → analisar → planejar → confirmar → executar**. Nunca edita sem confirmação prévia.

- Adiciona wikilinks para termos já presentes no dicionário do domínio, cria verbetes ausentes (via `/verbete`), busca referências externas e atualiza frontmatter.
- **Sem `path`:** pergunta qual nota enriquecer. **Com `path`:** usa o arquivo indicado (relativo à raiz do vault).
- **Instrução complementar:** texto livre como contexto extra — foco temático, URLs a incorporar, ênfase numa seção.
- **Quando usar:** "enriquecer", "melhorar", "atualizar" ou "revisar" uma nota.

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
2. **Atualiza esta página** com a entrada nova no domínio correto (e ajusta a contagem no topo).
3. Se a skill é parte do pipeline principal, atualiza também [[workflow]].
4. Se a skill é nova no fluxo central do vault, considera um atalho no `CLAUDE.md` raiz.

## Veja também

- [[Como usar este vault]] — mapa estático das zonas do vault.
- [[workflow]] — pipeline cognitivo + a skill `/glosa` no fluxo.
- [[00-Meta/guia/pipeline/index|Pipeline]] — ciclo de vida das notas (Pergaminhos → Glosas → Domínios → Sendas).
- [[Manutenção do vault]] — rotinas de higiene onde `/arquivar-glosas` e `/verificar-wikilinks` entram.
