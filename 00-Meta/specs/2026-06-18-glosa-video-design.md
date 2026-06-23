---
title: "Design — Skill /glosa-video"
created: 2026-06-18
type: design
status: draft
tags: [skill, glosa, video, fichamento, design]
---

# Design — Skill `/glosa-video`

## Problema

Consumo muito conteúdo em vídeo (YouTube), mas o ciclo de fichamento do vault
(`/glosa` → `/promover-glosa` → `/sintetizar-glosas` → `/arquivar-glosas`) só
cobre artigos web. A própria `/glosa` **recusa** URLs de YouTube ("vídeo não está
no MVP"). Resultado: vídeo fica fora do meu sistema de conhecimento.

`/glosa-video` faz pro vídeo o que `/glosa` faz pro artigo: gera um fichamento
estruturado em `02-Glosas/`, que vira objeto de conhecimento por si só e pluga
no ciclo de glosas existente. O valor é o fichamento — aproveitá-lo numa nota de
domínio é opcional e fica pro fluxo downstream (`/promover-glosa`).

## Princípios

1. **Espelhar `/glosa`.** Mesmo template, mesmas convenções rígidas, mesmo
   ciclo de vida. Quem conhece `/glosa` entende `/glosa-video` na hora.
2. **Adaptações só onde vídeo difere de texto.** Fonte via `yt-dlp` em vez de
   `WebFetch`; timestamps; metadados de canal/duração; mini-índice de capítulos.
3. **Propor, não decidir pelo usuário.** `Meu comentário` nunca é preenchido.
   `Ver também` sugere, mas o dono valida.
4. **Sem dependências novas instaladas.** `yt-dlp` roda via `uvx` (o `uv` já
   está na máquina). Nada de instalar global, nada de site de terceiros.

## Inputs

```
/glosa-video <url> [pasta-alvo]
```

- `<url>` — **obrigatório**. Playlist OU vídeo único do YouTube
  (`youtube.com/watch`, `youtu.be`, `youtube.com/playlist`).
- `[pasta-alvo]` — **opcional**. Dica de domínio pra estreitar a busca de "Ver
  também" (ex: `03-Dominios/Tecnologia/IA/Anatomia dos LLMs`). Se omitido, a skill escaneia
  o vault inteiro e sugere as notas de melhor encaixe por tags/tema.

## Detecção de tipo de input

| Padrão de URL                         | Tratamento                                  |
| ------------------------------------- | ------------------------------------------- |
| `.../playlist?list=...`               | Playlist → N glosas + 1 glosa-índice        |
| `.../watch?v=...` ou `youtu.be/...`   | Vídeo único → 1 glosa                        |
| `.../watch?v=...&list=...`            | Vídeo dentro de playlist → trata como único (usa `v`, ignora `list`) salvo se o usuário pedir a playlist |
| Não-YouTube / malformada              | Erro. Sugere `/glosa` (artigo) ou manter em Pergaminhos |

## Pipeline de execução

1. **Validar URL.** HTTP/HTTPS bem-formada e domínio YouTube. Senão, erro +
   abortar (sem escrever arquivo).
2. **Resolver lista de vídeos.**
   - Playlist: `uvx yt-dlp --flat-playlist --print "%(id)s | %(title)s" <url>`
   - Vídeo único: lista de um item.
3. **Por vídeo — baixar metadados + legendas:**
   - Metadados: `uvx yt-dlp --skip-download --print
     "%(id)s|%(title)s|%(channel)s|%(upload_date)s|%(duration)s" <video_url>`
   - Legendas: inspecionar fontes com `--list-subs` e baixar a melhor como
     `.vtt` em `/tmp/glosavideo-%(id)s.%(ext)s`. **Prioridade de seleção:**
     1. **Manual** (`--write-subs`) na língua original do vídeo — costuma ter
        melhor qualidade que a automática (pontuação correta, sem erros de ASR).
     2. **Manual** em qualquer outro idioma disponível.
     3. **Automática** (`--write-auto-subs`) na língua original (`pt-orig`
        quando existir) → `pt` → qualquer idioma disponível (ex: `en`).
   - **Qualquer idioma serve.** O conteúdo sintetizado (TL;DR, Pontos-chave,
     Momentos-chave) sai sempre em **PT-BR** — traduzindo quando a legenda for de
     outro idioma. As **Citações preservam a língua original** da legenda.
4. **Limpar VTT → texto puro.** Remover header `WEBVTT`/`Kind`/`Language`,
   timestamps, tags `<c>`/`<00:00.000>`, linhas em branco e linhas duplicadas
   (auto-captions repetem cada linha). Manter mapa `texto → primeiro timestamp`
   pra ancorar citações e capítulos.
5. **Gerar conteúdo da glosa** (ver "Conteúdo gerado" abaixo).
6. **Calcular slug + filename.** `<ano-corrente>-<slug>.md`, slug ASCII
   kebab-case ≤ 60 chars (mesma normalização do `/glosa`).
7. **Resolver colisão.** `-2`, `-3`… + alerta de possível duplicata.
8. **Escrever** em `02-Glosas/<filename>.md`.
9. **Limpar Pergaminhos.** Se a URL do vídeo estiver em
   `01-Pergaminhos/entradas.md`, remover a linha (match por substring).
10. **Playlist:** após as N glosas, escrever a **glosa-índice** (ver abaixo).
11. **Descartar** os `.vtt` de `/tmp`.
12. **Reportar** arquivos criados + status de limpeza do Pergaminhos.

## Conteúdo gerado (por vídeo)

- **TL;DR** — 1-3 frases PT-BR sintetizando o argumento do vídeo.
- **Pontos-chave** — 5-7 bullets PT-BR fiéis à transcrição (sem inferência externa).
- **Momentos-chave** *(novo, vídeo-nativo)* — mini-índice de capítulos:
  `- [mm:ss] — tópico`. 4-10 marcos.
- **Citações** — 3-5 trechos verbatim **na língua original**, cada um com
  `[mm:ss]` do ponto no vídeo.
- **Meu comentário** — SEMPRE placeholder literal, nunca preenchido.
- **Ver também** *(adaptado)* — auto-sugestão de 1-4 wikilinks pras notas
  existentes de melhor encaixe (busca por tags/tema no `[pasta-alvo]` ou vault).
  Marcado como sugestão; o dono valida. Se nada bate, deixa `-`.

## Frontmatter

Espelha `/glosa` + campos de vídeo (`channel`, `duration`, `video_id`).
Inclui `progress: backlog` (presente nas glosas reais, não no template antigo).

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
lang: <pt ou en>
publish: false
---
```

## Template do arquivo (vídeo único)

```markdown
# <título> — <canal>

> [!info] Vídeo
> [▶ Assistir no YouTube](<url>) · <duração> · <canal>

## TL;DR

<1 a 3 frases PT-BR>

## Pontos-chave

- <bullet 1>
- ...

## Momentos-chave

- [00:00] — <tópico>
- [mm:ss] — <tópico>

## Citações

> "<citação 1 na língua original>" — [mm:ss]

> "<citação 2 na língua original>" — [mm:ss]

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

- [[<nota sugerida 1>]] <!-- sugestão automática; validar -->
```

## Glosa-índice (só pra playlist)

Arquivo `02-Glosas/<ano>-<playlist-slug>-serie.md`, `type: glosa`, que amarra a
série. Não é promovível por si só — é um MOC leve dentro de `02-Glosas/`.

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
...

## Ver também

- [[<nota/MOC de domínio relacionado>]] <!-- sugestão; validar -->
```

## Convenções rígidas (herdadas do /glosa)

- **PT-BR** em TL;DR, Pontos-chave, Momentos-chave, Meu comentário, Ver também.
- **Língua original** nas Citações.
- **Tags** kebab-case ASCII, 3-5 por ficha.
- **`publish: false`** sempre. **`status: lido`** na criação.
- **`Meu comentário`** sempre placeholder vazio — nunca preencher.

## Tech (validado de ponta a ponta em 2026-06-18)

- `uvx yt-dlp` funciona sem instalação (versão testada: 2026.06.09).
- Playlist-alvo do MVP tem 6 vídeos (canal do Sandeco), **originais em PT**
  (`pt-orig`), legendas baixam limpas como `.vtt`.
- **Caveats não-fatais:** avisos de "No supported JavaScript runtime" e de
  "impersonation" aparecem mas **não impedem** o download das legendas.
- **Sem `ffmpeg`:** não converter pra `.srt` (`--convert-subs` falha). Parsear
  o `.vtt` direto — é texto puro.

## Edge cases

| Caso                                  | Comportamento                                                    |
| ------------------------------------- | --------------------------------------------------------------- |
| URL malformada / não-YouTube          | Erro + abortar; sugere `/glosa` ou Pergaminhos                   |
| Vídeo sem nenhuma legenda             | Reporta e pula esse vídeo (na playlist, segue os demais)        |
| Existe legenda manual                 | Prefere a manual à automática (melhor qualidade)               |
| Só legenda automática                 | Usa a automática (caso comum); nota isso no relatório           |
| Legenda só em idioma estrangeiro      | Usa mesmo assim; sintetiza em PT-BR (traduz), cita no original; `lang` = idioma do vídeo |
| Idioma não detectado                  | Default `lang: en`                                              |
| Data de upload ausente                | `published:` vazio; menciona no relatório                       |
| Canal ausente                         | `author: "(desconhecido)"`, `channel:` vazio                   |
| Slug colide no ano                    | Sufixo `-2`, `-3`…; alerta de possível duplicata                |
| URL do vídeo em Pergaminhos           | Remove linha (match substring), igual `/glosa`                  |
| "Ver também" sem match                | Deixa `-` vazio                                                 |
| Playlist com 1 vídeo                  | Trata como vídeo único; sem glosa-índice                        |
| `yt-dlp` indisponível / `uvx` falha   | Erro claro com o comando que falhou; não escreve arquivo        |

## Distribuição

Skill espelhada em **dois repos** (como as outras do ciclo de glosa):

- `codex-technomanticus/.agents/skills/glosa-video/SKILL.md` (público)
- `codex-technomanticus-apocrypha/.agents/skills/glosa-video/SKILL.md` (privado)

Conteúdo idêntico. Atualizar `CLAUDE.md`/`AGENTS.md` de ambos pra listar o
comando junto do `/glosa`.

## Fora de escopo (YAGNI)

- Não edita notas de domínio (só cria glosas).
- Não baixa o vídeo (só legendas).
- Não usa Whisper/transcrição própria (legendas do YouTube bastam).
- Não gera legenda quando o vídeo não tem nenhuma (não transcreve áudio).
  Tradução do conteúdo sintetizado, sim — citações ficam no original.
- Não resolve canais/usuários inteiros (`@canal`) — só playlist ou vídeo.

## Sequência sugerida de implementação

1. Escrever `SKILL.md` no CT seguindo este design.
2. Rodar a skill na playlist-alvo (6 vídeos do Sandeco) → validar as 6 glosas +
   índice contra as notas da Anatomia dos LLMs.
3. Ajustar o template/heurísticas conforme o resultado real.
4. Espelhar pro CTA + atualizar os dois `CLAUDE.md`/`AGENTS.md`.
