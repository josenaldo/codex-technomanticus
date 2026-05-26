---
title: "Workflow do Codex"
created: 2026-04-27
updated: 2026-04-28
type: how-to
status: seedling
tags:
  - guia
  - meta
publish: false
---

# Workflow do Codex Technomanticus

Como o material flui entre as 5 zonas do vault. Para o mapa estático das zonas, veja [[Como usar este vault]].

## O pipeline cognitivo

```text
captura → destilação → integração → curadoria
Pergaminhos → Glosas → Domínios → Sendas
```

1. **Captura.** Você acha um link interessante → cola em `01-Pergaminhos/entradas.md`, sob uma seção temática (`# Tema`).
2. **Destilação.** Lê o artigo → invoca `/glosa <url>` → ficha aparece em `02-Glosas/<ano>-<slug>.md`.
3. **Limpeza automática.** A skill `/glosa` remove o link de `01-Pergaminhos/entradas.md` se ele estava lá.
4. **Integração** (opcional, sob demanda). Se um artigo merece estudo profundo, você o relê e extrai notas atômicas pra `03-Dominios/<área>/`.
5. **Curadoria** (opcional). Pra preparar entrevista ou estudo focado, você sequencia notas de Domínios numa Senda em `04-Sendas/Senda <Tema>.md`.

A integração e curadoria não são obrigatórias — uma Glosa pode viver sozinha. Só promova o conteúdo quando ele realmente vai ser estudado ou referenciado.

## Skill `/glosa` — fichamento automático

A skill `/glosa` automatiza o passo "captura → destilação" do pipeline.

**Invocação:**

- `/glosa <url>` — slash command, forma canônica
- `Claude, fiche esse link: <url>` — linguagem natural

**O que faz (5 passos):**

1. Faz `WebFetch` da URL e extrai título, autor, site, data, idioma, body.
2. Gera draft em PT-BR (TL;DR, Pontos-chave, Tags) e seleciona Citações verbatim na língua original.
3. Deixa **Meu comentário** vazio com placeholder — campo onde a ficha vira sua.
4. Escreve em `02-Glosas/<ano>-<slug>.md` (em colisão de slug, sufixo `-2`, `-3`).
5. Remove o link de `01-Pergaminhos/entradas.md` se ele estava lá.

**Edge cases (skill avisa e aborta):**

- PDFs (URL `.pdf`)
- YouTube/Vimeo (vídeos)
- Spotify/podcasts
- Twitter/X (rede social)
- URL malformada

## Convenções do fluxo

- **Filename de Glosas**: `<ano>-<slug-kebab-case>.md` (ex: `2026-ai-now-writes-97-of-my-code.md`). Em colisão de slug no mesmo ano: sufixo `-2`, `-3`, etc.
- **Sendas**: 1 arquivo por senda, no formato `Senda <Tema>.md` em `04-Sendas/` (flat, sem subpastas).
- **Idioma das seções autorais** de Glosas (TL;DR, Pontos-chave, Meu comentário, Ver também): PT-BR.
- **Idioma das citações**: língua original do artigo.

Convenções gerais de escrita (status, tags, atomicidade, filename de Domínios) estão em [[Convenções de escrita]]. Boas práticas de linking estão em [[Wikilinks e MOCs]].

## Sinais de que o pipeline está travado

- `01-Pergaminhos/entradas.md` cresce sem parar → pause leitura nova e processe o backlog.
- Glosa parada há semanas com **Meu comentário** vazio → ou processe ou apague (não vale guardar fichamento sem reação sua).
- Domínio com MOC desatualizado em relação às notas dentro dele → o índice mente.

Rotinas de manutenção em [[Manutenção do vault]].
