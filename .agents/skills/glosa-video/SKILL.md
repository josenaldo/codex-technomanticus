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
- **Momentos-chave** — capítulos reais do vídeo como `- [mm:ss] — tópico`, tipicamente 4-12 (mais se o vídeo for um passo-a-passo longo).
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
