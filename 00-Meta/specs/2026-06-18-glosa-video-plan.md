# Skill `/glosa-video` — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar a skill `/glosa-video`, que ficha vídeos/playlists do YouTube em `02-Glosas/` no formato da `/glosa`, e validá-la fichando a playlist-alvo da Anatomia dos LLMs.

**Architecture:** Skill é um `SKILL.md` (prompt operacional) no padrão das demais do vault. Usa `uvx yt-dlp` pra metadados + legendas, sintetiza conteúdo em PT-BR, grava glosas `type: glosa` que plugam no ciclo existente (`/promover-glosa`, etc.). Sem código executável: o "teste" de cada tarefa é rodar comandos reais e conferir o output contra o spec.

**Tech Stack:** Markdown (Obsidian Flavored), `uvx yt-dlp` (v2026.06.09 validada), bash (grep/sed/awk pra limpar VTT).

**Spec:** `00-Meta/specs/2026-06-18-glosa-video-design.md`

## Global Constraints

- Skill espelhada **idêntica** em CT (`codex-technomanticus`) e CTA (`codex-technomanticus-apocrypha`), em `.agents/skills/glosa-video/SKILL.md`.
- Glosas gravadas em `02-Glosas/<ano-corrente>-<slug>.md`; slug ASCII kebab-case ≤ 60 chars.
- Frontmatter: `type: glosa`, `progress: backlog`, `status: lido`, `publish: false`. Campos de vídeo: `channel`, `video_id`, `duration`.
- **PT-BR** em TL;DR, Pontos-chave, Momentos-chave, Meu comentário, Ver também. **Citações na língua original** da legenda.
- `Meu comentário` SEMPRE placeholder literal — nunca preenchido.
- Sem instalar nada global: `yt-dlp` só via `uvx`. Sem `ffmpeg`: parsear `.vtt`, nunca converter pra `.srt`.
- Seleção de legenda: **manual** (língua original) → manual (outro idioma) → automática (`pt-orig`→`pt`→qualquer).
- Vault commita direto na `main` (convenção observada nos commits). **Commitar só quando o usuário autorizar.**

---

### Task 1: Autorar `SKILL.md` no CT

**Files:**
- Create: `codex-technomanticus/.agents/skills/glosa-video/SKILL.md`

**Interfaces:**
- Produces: a skill `/glosa-video`. Consumida por nenhuma outra task em código; Tasks 2-3 a executam manualmente.

- [ ] **Step 1: Criar o arquivo `SKILL.md`** com exatamente este conteúdo:

````markdown
---
name: glosa-video
description: >
   Cria fichamento (Glosa) de vídeo do YouTube a partir de URL — vídeo único ou playlist. Baixa legendas via yt-dlp, sintetiza em PT-BR e grava em `02-Glosas/` no mesmo formato da /glosa, com timestamps. Use quando o usuário invocar /glosa-video, compartilhar URL de YouTube pedindo ficha/glosa/fichamento, ou disser "fichar esse vídeo", "glosar essa playlist", "registrar esse vídeo". Complementa a /glosa, que recusa YouTube. Suporta legendas manuais e automáticas em qualquer idioma (traduz o conteúdo pro PT-BR; cita no original).
---

# Skill: glosa-video

Cria fichamento(s) ("Glosa") de vídeo do YouTube em `02-Glosas/<ano>-<slug>.md`, espelhando a skill `/glosa` (que cobre artigos web e recusa YouTube). Para playlists, gera uma glosa por vídeo mais uma glosa-índice da série. Remove o link do vídeo de `01-Pergaminhos/entradas.md` se estiver lá.

## Quando usar

- `/glosa-video <url> [pasta-alvo]`
- Compartilhar URL de YouTube (`youtube.com`, `youtu.be`) pedindo ficha/glosa/fichamento
- "fichar esse vídeo", "glosar essa playlist", "registrar esse vídeo no vault"

## Quando NÃO usar (e o que fazer)

| Situação                       | Resposta                                                        |
| ------------------------------ | -------------------------------------------------------------- |
| URL não-YouTube (artigo web)   | Redirecione pra `/glosa`.                                       |
| URL de PDF / Spotify / tweet   | Não suportado; sugira manter o link em Pergaminhos.            |
| URL malformada (não HTTP/S)    | Erro: peça uma URL válida.                                      |
| Vídeo sem nenhuma legenda      | Reporte; não há transcrição pra fichar (não transcrevemos áudio). |

## Dependência: yt-dlp via uvx

Todos os comandos usam `uvx yt-dlp` (não instalar global; o `uv` já está na máquina). Se `uvx` falhar, reporte o comando exato que falhou e aborte sem escrever arquivo. Avisos de "No supported JavaScript runtime" e "impersonation" são **não-fatais** — o download das legendas funciona mesmo assim.

## Fluxo de execução

1. **Validar URL.** HTTP/HTTPS + domínio YouTube. Senão, aplicar tabela "Quando NÃO usar".
2. **Detectar tipo:**
   - `.../playlist?list=...` → playlist (N glosas + índice).
   - `.../watch?v=...` ou `youtu.be/...` → vídeo único.
   - `.../watch?v=...&list=...` → vídeo único (usa `v`, ignora `list`), salvo pedido explícito pela playlist.
3. **Resolver lista de vídeos** (playlist):
   ```bash
   uvx yt-dlp --flat-playlist --print "%(id)s | %(title)s" "<url>"
   ```
4. **Por vídeo — metadados:**
   ```bash
   uvx yt-dlp --skip-download --print "%(id)s|%(title)s|%(channel)s|%(upload_date)s|%(duration_string)s" "https://youtube.com/watch?v=<id>"
   ```
   Converter `upload_date` (`YYYYMMDD`) → `YYYY-MM-DD`.
5. **Por vídeo — escolher e baixar legenda.** Listar fontes:
   ```bash
   uvx yt-dlp --list-subs --skip-download "https://youtube.com/watch?v=<id>"
   ```
   Escolher por prioridade: (1) manual na língua original; (2) manual em qualquer idioma; (3) automática `pt-orig`→`pt`→qualquer. Baixar:
   ```bash
   # manual:
   uvx yt-dlp --skip-download --write-subs     --sub-langs "<lang>" --sub-format vtt -o "/tmp/glosavideo-%(id)s.%(ext)s" "https://youtube.com/watch?v=<id>"
   # automática:
   uvx yt-dlp --skip-download --write-auto-subs --sub-langs "<lang>" --sub-format vtt -o "/tmp/glosavideo-%(id)s.%(ext)s" "https://youtube.com/watch?v=<id>"
   ```
6. **Limpar VTT → texto** (pra síntese):
   ```bash
   grep -vE '^WEBVTT|^Kind:|^Language:|-->|^[[:space:]]*$|align:|position:' "/tmp/glosavideo-<id>.<lang>.vtt" | sed -E 's/<[^>]*>//g' | awk '!seen[$0]++'
   ```
   Para **timestamps** (citações e Momentos-chave), consultar as linhas de cue cruas do `.vtt` (`HH:MM:SS.mmm --> ...`) e achar o tempo do trecho escolhido. Formatar como `[mm:ss]` (ou `[h:mm:ss]` se ≥ 1h).
7. **Gerar conteúdo** (ver "Conteúdo gerado").
8. **Slug + filename.** `<ano-corrente>-<slug>.md`. Normalizar título pra ASCII kebab-case ≤ 60 chars (remover acentos, pontuação, stopwords PT se precisar caber).
9. **Resolver colisão.** Existe? Tentar `-2`, `-3`… e avisar: "pode ser duplicata semântica".
10. **Escrever** `02-Glosas/<filename>.md` com o template.
11. **Limpar Pergaminhos.** Ler `01-Pergaminhos/entradas.md`; remover linha que contenha a URL como substring (formatos `<url>`, `[txt](url)`, URL crua).
12. **Playlist:** após as N glosas, escrever a glosa-índice (ver template). Vídeo único: pular este passo.
13. **Descartar** os `.vtt` de `/tmp` (`rm -f /tmp/glosavideo-*.vtt`).
14. **Reportar:** arquivos criados + status da limpeza do Pergaminhos + qualquer vídeo pulado.

## Conteúdo gerado (por vídeo)

- **TL;DR** — 1-3 frases PT-BR com o argumento do vídeo.
- **Pontos-chave** — 5-7 bullets PT-BR fiéis à transcrição (sem inferência externa).
- **Momentos-chave** — 4-10 marcos `- [mm:ss] — tópico` (capítulos).
- **Citações** — 3-5 trechos verbatim **na língua original**, cada um com `[mm:ss]`.
- **Meu comentário** — placeholder literal, nunca preenchido.
- **Ver também** — 1-4 wikilinks pras notas existentes de melhor encaixe. Buscar em `[pasta-alvo]` (se dado) ou no vault, por interseção de tags/tema. Marcar como sugestão (`<!-- sugestão; validar -->`). Sem match → `-`.

## Template do arquivo (vídeo)

```markdown
---
title: "<título exato do vídeo>"
aliases: ["<título exato do vídeo>"]
source: <url do vídeo>
author: <canal>
site: YouTube
channel: <canal>
video_id: <id>
duration: <hh:mm:ss>
published: <YYYY-MM-DD do upload, ou vazio>
read: <hoje YYYY-MM-DD>
type: glosa
progress: backlog
status: lido
tags: [<tag1>, <tag2>, <tag3>]
lang: <idioma original do vídeo>
publish: false
---

# <título> — <canal>

> [!info] Vídeo
> [▶ Assistir no YouTube](<url>) · <duração> · <canal>

## TL;DR

<1 a 3 frases PT-BR>

## Pontos-chave

- <bullet 1>
- <bullet 2>
- <bullet 3>
- <bullet 4>
- <bullet 5>

## Momentos-chave

- [00:00] — <tópico>
- [mm:ss] — <tópico>

## Citações

> "<citação 1 na língua original>" — [mm:ss]

> "<citação 2 na língua original>" — [mm:ss]

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

- [[<nota sugerida>]] <!-- sugestão; validar -->
```

## Template da glosa-índice (só playlist)

Arquivo `02-Glosas/<ano>-<playlist-slug>-serie.md`:

```markdown
---
title: "<título da playlist> (série)"
source: <url da playlist>
site: YouTube
type: glosa
progress: backlog
status: lido
tags: [<tags comuns da série>, serie]
lang: pt
publish: false
---

# <título da playlist> — série

> [!info] Playlist · <N> vídeos · <canal>
> [▶ Ver no YouTube](<url da playlist>)

## TL;DR

<o que a série cobre, 1-3 frases>

## Vídeos

1. [[<ano>-<slug-1>]] — <uma linha>
2. [[<ano>-<slug-2>]] — <uma linha>

## Ver também

- [[<nota/MOC de domínio relacionado>]] <!-- sugestão; validar -->
```

## Convenções rígidas (herdadas de /glosa)

- PT-BR no conteúdo sintetizado; língua original nas Citações.
- Tags kebab-case ASCII, 3-5 por ficha.
- `publish: false` sempre; `status: lido` na criação.
- `Meu comentário` sempre placeholder vazio.

## Edge cases

| Caso                              | Comportamento                                                  |
| --------------------------------- | ------------------------------------------------------------- |
| URL malformada / não-YouTube      | Tabela "Quando NÃO usar"; não escreve arquivo                 |
| Vídeo sem nenhuma legenda         | Reporta e pula (na playlist, segue os demais)                 |
| Existe legenda manual             | Prefere a manual à automática                                  |
| Só automática                     | Usa automática; nota no relatório                             |
| Legenda só em idioma estrangeiro  | Sintetiza em PT-BR (traduz), cita no original; `lang` do vídeo |
| Idioma não detectado              | Default `lang: en`                                            |
| Upload date ausente               | `published:` vazio; menciona no relatório                     |
| Canal ausente                     | `author: "(desconhecido)"`, `channel:` vazio                 |
| Slug colide no ano                | Sufixo `-2`, `-3`…; alerta de duplicata                       |
| Ver também sem match              | Deixa `-`                                                     |
| Playlist com 1 vídeo              | Trata como vídeo único; sem glosa-índice                      |
| `uvx`/`yt-dlp` falha              | Reporta comando que falhou; não escreve arquivo              |
````

- [ ] **Step 2: Validar estrutura do arquivo** (gate)

Run:
```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
F=.agents/skills/glosa-video/SKILL.md
grep -c "^name: glosa-video" $F
for s in "## Quando usar" "## Fluxo de execução" "## Conteúdo gerado" "## Template do arquivo" "## Template da glosa-índice" "## Edge cases"; do grep -qF "$s" $F && echo "OK: $s" || echo "FALTA: $s"; done
for f in "type: glosa" "progress: backlog" "video_id" "Momentos-chave" "uvx yt-dlp --flat-playlist" "--write-auto-subs"; do grep -qF "$f" $F && echo "OK: $f" || echo "FALTA: $f"; done
```
Expected: `1` na primeira linha; todas as linhas começando com `OK:`, nenhuma com `FALTA:`.

- [ ] **Step 3: Commit** (quando o usuário autorizar)

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
git add .agents/skills/glosa-video/SKILL.md 00-Meta/specs/2026-06-18-glosa-video-design.md 00-Meta/specs/2026-06-18-glosa-video-plan.md
git commit -m "feat(skills): adiciona /glosa-video — fichamento de vídeos do YouTube"
```

---

### Task 2: Smoke-test em um vídeo

Valida o pipeline ponta a ponta num único vídeo antes de processar a playlist inteira. Usa o vídeo de Tokens (`Am73u_4y0ok`), cuja legenda `pt-orig` já foi validada.

**Files:**
- Create (output): `codex-technomanticus/02-Glosas/2026-tokens-explicados-segredo-chatgpt.md` (nome final pode variar pelo slug)

**Interfaces:**
- Consumes: o `SKILL.md` da Task 1.

- [ ] **Step 1: Executar a skill** seguindo o Fluxo de execução do `SKILL.md`, com:
  `/glosa-video https://youtube.com/watch?v=Am73u_4y0ok 03-Dominios/Tecnologia/IA/Anatomia dos LLMs`

- [ ] **Step 2: Validar a glosa gerada** (gate)

Run:
```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
G=$(ls -t 02-Glosas/2026-*.md | head -1); echo "Glosa: $G"
grep -qE "^type: glosa$"        "$G" && echo "OK type"        || echo "FALHA type"
grep -qE "^progress: backlog$"  "$G" && echo "OK progress"    || echo "FALHA progress"
grep -qE "^video_id: Am73u_4y0ok" "$G" && echo "OK video_id"  || echo "FALHA video_id"
grep -qE "^channel: "           "$G" && echo "OK channel"     || echo "FALHA channel"
grep -qE "^duration: "          "$G" && echo "OK duration"    || echo "FALHA duration"
for s in "## TL;DR" "## Pontos-chave" "## Momentos-chave" "## Citações" "## Meu comentário" "## Ver também"; do grep -qF "$s" "$G" && echo "OK: $s" || echo "FALHA: $s"; done
grep -qF "*Escreva aqui sua reação" "$G" && echo "OK comentário-placeholder" || echo "FALHA comentário"
grep -qE '\[[0-9]+:[0-9]{2}\]' "$G" && echo "OK timestamps" || echo "FALHA timestamps"
```
Expected: todas as linhas `OK ...`.

- [ ] **Step 3: Conferência humana de qualidade**

Ler a glosa e confirmar: TL;DR fiel ao vídeo; citações batem com a fala; "Ver também" sugere `[[02 - Tokens e tokenização]]`; nenhum timestamp absurdo (> duração). Ajustar heurísticas do `SKILL.md` se algo falhar e repetir Steps 1-2.

- [ ] **Step 4: Limpar `/tmp`**

```bash
rm -f /tmp/glosavideo-*.vtt
```

- [ ] **Step 5: Commit** (quando o usuário autorizar)

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
git add 02-Glosas/
git commit -m "glosa(video): Tokens Explicados (Sandeco) — smoke-test /glosa-video"
```

---

### Task 3: Processar a playlist-alvo (6 vídeos + índice)

**Files:**
- Create (output): 5 glosas restantes em `codex-technomanticus/02-Glosas/2026-*.md` (a de Tokens já veio na Task 2)
- Create (output): `codex-technomanticus/02-Glosas/2026-<playlist-slug>-serie.md`

**Interfaces:**
- Consumes: o `SKILL.md` da Task 1.

- [ ] **Step 1: Executar a skill na playlist**
  `/glosa-video https://youtube.com/playlist?list=PLbmt8d_ueDMVMW1Iu4OcmlQGisGhxAmMy 03-Dominios/Tecnologia/IA/Anatomia dos LLMs`

  A skill pula a glosa do vídeo já fichado na Task 2 (colisão de slug → reaproveitar, não duplicar) e gera as 5 restantes + a glosa-índice.

- [ ] **Step 2: Validar contagem e índice** (gate)

Run:
```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
echo "Glosas de vídeo (espera 6):"; grep -lE "^site: YouTube$" 02-Glosas/2026-*.md | grep -v serie | wc -l
SERIE=$(ls 02-Glosas/2026-*serie.md 2>/dev/null); echo "Índice: $SERIE"
echo "Vídeos linkados no índice (espera 6):"; grep -cE '^[0-9]+\. \[\[' "$SERIE"
```
Expected: `6` glosas de vídeo; arquivo índice existe; `6` links no índice.

- [ ] **Step 3: Validar wikilinks de "Ver também"** (gate)

Run (confere que cada wikilink sugerido aponta pra arquivo existente):
```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
grep -hoE '\[\[[^]]+\]\]' 02-Glosas/2026-*.md | sed -E 's/\[\[//;s/\]\]//;s/#.*//;s/\|.*//' | sort -u | while read n; do
  [ -n "$n" ] && { find . -name "$n.md" | grep -q . && echo "OK: $n" || echo "QUEBRADO: $n"; }
done
```
Expected: nenhum `QUEBRADO:` (ou, se houver, são notas-novas sugeridas pela lacuna — verificar manualmente, ex: Embeddings).

- [ ] **Step 4: Conferência humana**

Ler as 6 glosas + índice. Confirmar mapeamento esperado: Tokens→`[[02 - Tokens e tokenização]]`; Attention/ordem das palavras→`[[04 - Atenção e o mecanismo transformer]]`; "múltiplas mentes"→`[[07 - Dense vs Mixture-of-Experts]]`; **Embeddings → sem nota; "Ver também" deve sinalizar a lacuna** (sugestão de nota nova, não wikilink quebrado silencioso).

- [ ] **Step 5: Limpar `/tmp` e commit** (quando o usuário autorizar)

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
rm -f /tmp/glosavideo-*.vtt
git add 02-Glosas/
git commit -m "glosa(video): playlist Anatomia das LLMs (Sandeco) — 6 vídeos + índice"
```

---

### Task 4: Espelhar no CTA e registrar comando

**Files:**
- Create: `codex-technomanticus-apocrypha/.agents/skills/glosa-video/SKILL.md` (cópia idêntica)
- Modify: `codex-technomanticus/README.md` (seção da skill `/glosa`, ~linha 66)
- Modify: `codex-technomanticus-apocrypha/AGENTS.md` (lista de skills, ~linha 31)
- Modify: `codex-technomanticus-apocrypha/CLAUDE.md` (seção "Glossários e notas")

**Interfaces:**
- Consumes: o `SKILL.md` finalizado da Task 1 (após ajustes das Tasks 2-3).

- [ ] **Step 1: Copiar a skill pro CTA**

```bash
mkdir -p /home/josenaldo/repos/personal/codex-technomanticus-apocrypha/.agents/skills/glosa-video
cp /home/josenaldo/repos/personal/codex-technomanticus/.agents/skills/glosa-video/SKILL.md \
   /home/josenaldo/repos/personal/codex-technomanticus-apocrypha/.agents/skills/glosa-video/SKILL.md
```

- [ ] **Step 2: Verificar identidade** (gate)

```bash
diff /home/josenaldo/repos/personal/codex-technomanticus/.agents/skills/glosa-video/SKILL.md \
     /home/josenaldo/repos/personal/codex-technomanticus-apocrypha/.agents/skills/glosa-video/SKILL.md && echo "IDÊNTICOS"
```
Expected: `IDÊNTICOS` (sem diff).

- [ ] **Step 3: Registrar no `AGENTS.md` do CTA**

Adicionar a linha logo após `- /glosa — Cria fichamento de artigo web a partir de URL.`:
```markdown
- `/glosa-video` — Cria fichamento de vídeo/playlist do YouTube a partir de URL.
```

- [ ] **Step 4: Registrar no `CLAUDE.md` do CTA**

Na seção "Glossários e notas", trocar a linha do ciclo de glosas por uma que inclua `/glosa-video`:
```markdown
- `/glosa`, `/glosa-video`, `/promover-glosa`, `/sintetizar-glosas`, `/arquivar-glosas`, `/acordar-glosas` — Ciclo de fichamento de leitura (texto e vídeo).
```

- [ ] **Step 5: Documentar no `README.md` do CT**

Na seção "Captura e destilação — skill `/glosa`" (~linha 66), acrescentar um parágrafo:
```markdown
- Para vídeos do YouTube, use `/glosa-video <url>` — baixa as legendas (via `yt-dlp`), sintetiza em PT-BR e gera a glosa com timestamps. Aceita vídeo único ou playlist (gera uma glosa por vídeo + um índice da série).
```

- [ ] **Step 6: Commit nos dois repos** (quando o usuário autorizar)

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git add README.md && git commit -m "docs: registra skill /glosa-video no README"
cd /home/josenaldo/repos/personal/codex-technomanticus-apocrypha && git add .agents/skills/glosa-video/SKILL.md AGENTS.md CLAUDE.md && git commit -m "feat(skills): espelha /glosa-video e registra comando"
```

---

## Self-Review

**Spec coverage:**
- Inputs (playlist/vídeo/pasta-alvo) → Task 1 Fluxo passos 1-2. ✓
- Pipeline (resolver/baixar/limpar/gerar/escrever/limpar Pergaminhos) → Task 1 Fluxo 3-14. ✓
- Conteúdo gerado + timestamps + Momentos-chave → Task 1. ✓
- Frontmatter de vídeo + glosa-índice → Task 1 templates. ✓
- Seleção de legenda (manual>auto, multi-idioma, tradução) → Task 1 Fluxo 5 + Edge cases. ✓
- Ver também auto-sugerido → Task 1 Conteúdo gerado + Task 3 Step 3-4. ✓
- Lacuna (Embeddings) → Task 3 Step 4. ✓
- Distribuição CT+CTA + registro → Task 4. ✓
- Validação na playlist-alvo → Tasks 2-3. ✓

**Placeholder scan:** SKILL.md completo embutido; comandos exatos; sem TBD/TODO. ✓

**Type consistency:** caminhos `.agents/skills/glosa-video/SKILL.md`, IDs e comandos `uvx yt-dlp` idênticos entre tasks. Filename de output em Task 2 é estimado (slug real definido na execução) — marcado explicitamente. ✓
