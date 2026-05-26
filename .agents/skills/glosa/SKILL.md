---
name: glosa
description: >
   Cria fichamento (Glosa) de artigo web a partir de URL. Use quando o usuário pedir pra fichar/catalogar/registrar um artigo, falar em "ficha de leitura", "fichamento", "glosa", invocar /glosa, ou compartilhar uma URL de artigo pedindo registro. Não suporta PDFs, vídeos do YouTube, podcasts ou tweets — nesses casos, avise e aborte.
---

# Skill: glosa

Cria um fichamento estruturado ("Glosa") de um artigo web em `02-Glosas/<ano>-<slug>.md` e remove o link correspondente de `01-Pergaminhos/entradas.md` se ele estava lá.

## Quando usar

Ative quando o usuário:

- Invoca `/glosa <url>`
- Compartilha uma URL e pede ficha/glosa/fichamento/catálogo/registro
- Diz "fichar esse link", "fazer ficha de leitura", "registrar esse artigo", "catalogar isso"
- Menciona "Pergaminhos" e quer processar um link em ficha

## Quando NÃO usar (e o que fazer)

| Situação                          | Resposta                                                                 |
| --------------------------------- | ------------------------------------------------------------------------ |
| URL é YouTube/Vimeo               | Avise: vídeo não está no MVP. Sugira manter o link em Pergaminhos.       |
| URL termina em `.pdf`             | Avise: PDF não está no MVP. Sugira manter o link em Pergaminhos.         |
| URL é Spotify/podcast             | Avise: podcast não está no MVP. Sugira manter o link em Pergaminhos.     |
| URL é tweet/post de rede social   | Avise: rede social não está no MVP. Sugira manter o link em Pergaminhos. |
| URL é malformada (não HTTP/HTTPS) | Erro: peça uma URL válida.                                               |

## Fluxo de execução

1. **Validar URL.** Deve ser HTTP/HTTPS bem-formada. Se não, erro e abortar.
2. **Detectar tipo.** Domínios `youtube.com`, `youtu.be`, `vimeo.com`, `open.spotify.com`, `twitter.com`, `x.com` → tipo não suportado, avise e aborte. URL terminando em `.pdf` → não suportado, avise e aborte. Demais → assume HTML.
3. **WebFetch.** Use a tool WebFetch com prompt:

   > "Extraia do artigo as seguintes informações: título exato, autor (nome completo se disponível, senão handle/nome de pena), nome do site/publicação, data de publicação no formato YYYY-MM-DD, idioma do conteúdo (`pt` ou `en`), e o body do artigo em markdown limpo. Retorne em formato estruturado, claramente rotulado por campo."

4. **Tratar falhas de fetch.** Se WebFetch retorna erro (404, paywall, timeout, conteúdo < 500 chars sugerindo bloqueio), reporte ao usuário e aborte sem escrever arquivo.
5. **Gerar conteúdo da ficha:**
   - **TL;DR**: 1 a 3 frases em PT-BR sintetizando o argumento principal do artigo
   - **Pontos-chave**: 5 a 7 bullets em PT-BR fiéis ao texto (sem inferências externas)
   - **Citações**: 3 a 5 trechos verbatim **na língua original do artigo**, escolhidos pela carga semântica (definições, dados, frases de impacto)
   - **Tags**: 3 a 5 tags em kebab-case sem acento, baseadas no conteúdo
   - **Meu comentário**: SEMPRE deixe como placeholder literal `*Escreva aqui sua reação, surpresas, discordâncias.*`. Nunca preencha automaticamente.
   - **Ver também**: SEMPRE deixe vazio (apenas `-`)
6. **Calcular slug.** Normalize o título para ASCII kebab-case, max 60 chars. Remova acentos, pontuação, e palavras vazias do português ("de", "da", "do", "o", "a", "e", "em") se necessário pra caber em 60 chars.
7. **Calcular filename.** `<ano-de-leitura>-<slug>.md`. Ano de leitura = ano corrente.
8. **Resolver colisão.** Se `02-Glosas/<filename>.md` já existe, tente `<filename>-2.md`, `<filename>-3.md`, etc. Avise o usuário: "Atenção: pode ser duplicata semântica de uma Glosa existente."
9. **Escrever arquivo.** Use Write tool em `02-Glosas/<filename>.md` com o template (seção "Template do arquivo" abaixo) preenchido.
10. **Limpar Pergaminhos.** Leia `01-Pergaminhos/entradas.md` linha por linha. Para cada linha, verifique se contém a URL como substring (cobrindo os formatos `<url>`, `[texto](url)`, e URL crua). Se encontrar, remova a linha inteira. Use Edit tool com `old_string` = linha completa, `new_string` = "" (string vazia). Se Edit falhar com new_string vazio, alternativa: ler todo o arquivo, filtrar linhas, reescrever com Write.
11. **Reportar ao usuário.** Uma destas duas mensagens conforme o caso:
    - `Glosa criada: 02-Glosas/<filename>.md. Link removido de Pergaminhos: ✓`
    - `Glosa criada: 02-Glosas/<filename>.md. Link não estava em Pergaminhos.`

## Template do arquivo

Estrutura completa que a skill escreve. Substitua `<placeholders>` pelos valores extraídos.

```markdown
---
title: "<título exato do artigo>"
aliases: ["<título exato do artigo>"]
source: <url>
author: <autor>
site: <nome do site>
published: <YYYY-MM-DD ou vazio se não detectado>
read: <hoje YYYY-MM-DD>
type: glosa
status: lido
tags: [<tag1>, <tag2>, <tag3>]
lang: <pt ou en>
publish: false
---

# <título> — <autor>

## TL;DR

<1 a 3 frases em PT-BR>

## Pontos-chave

- <bullet 1>
- <bullet 2>
- <bullet 3>
- <bullet 4>
- <bullet 5>

## Citações

> "<citação 1 na língua original>"

> "<citação 2 na língua original>"

> "<citação 3 na língua original>"

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
```

## Convenções rígidas

- **PT-BR** em TL;DR, Pontos-chave, Meu comentário, Ver também
- **Língua original** em Citações
- **Tags**: kebab-case ASCII, 3-5 por ficha
- **`publish: false`** sempre (Glosas não vão pro site público)
- **`status: lido`** no momento da criação
- **`Meu comentário`** sempre placeholder vazio — nunca preencher

## Edge cases (tabela)

| Caso                                 | Comportamento                                                                 |
| ------------------------------------ | ----------------------------------------------------------------------------- |
| URL malformada                       | Erro + abortar; não escreve arquivo                                           |
| WebFetch retorna 404/paywall/timeout | Reporte erro com mensagem clara; não escreve arquivo                          |
| Conteúdo extraído < 500 chars        | Alerta sobre paywall ou extração parcial; pergunte se deve seguir mesmo assim |
| Tipo não suportado (PDF/YouTube/etc) | Avise tipo; sugira manter em Pergaminhos; não escreve arquivo                 |
| Idioma não detectado                 | Default `lang: en` (heurística para artigos técnicos)                         |
| Data publicação não detectada        | `published:` vazio no frontmatter; mencione no relatório final                |
| Autor não detectado                  | `author: "(desconhecido)"`                                                    |
| Slug colide no mesmo ano             | Sufixo `-2`, `-3`...; alerta de possível duplicata                            |
| URL em Pergaminhos não bate exato    | Match por substring contendo a URL; remove linha inteira                      |
| Remoção deixa header de seção vazio  | Mantenha o header; o autor remove na próxima revisão manual                   |
