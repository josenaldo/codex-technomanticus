---
title: "04 - Anatomia de um prompt visual — canvas, composição, estilo"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - image-prompting
  - prompt-engineering
  - ia
  - prompt-anatomy
publish: true
aliases:
  - Anatomia de prompt visual
  - Camadas do prompt visual
---

# 04 - Anatomia de um prompt visual — canvas, composição, estilo

> [!abstract] TL;DR
> Todo prompt visual eficaz tem quatro camadas: **canvas** (formato, aspect ratio, resolução), **composição** (hierarquia, focal point, espaço negativo), **estilo** (linguagem visual, paleta, mood) e **texto** (palavras embutidas, posição, hierarquia). Cada camada tem vocabulário próprio que os modelos reconhecem. Quando você escreve sem cobrir as quatro, o modelo escolhe default genérico; quando cobre todas, converge rápido. Esta nota dá o vocabulário preciso por camada, com exemplo de prompt completo dissecado em cada uma.

## As quatro camadas

| Camada | Pergunta | Decisões |
|--------|----------|----------|
| **Canvas** | Em que retângulo? | Aspect ratio, orientação, resolução, padding |
| **Composição** | Onde fica o quê? | Hierarquia, focal point, regra dos terços, espaço negativo, framing |
| **Estilo** | Que linguagem visual? | Paleta, tipo de ilustração, mood, era estética |
| **Texto** | Que palavras aparecem? | Conteúdo, posição, tamanho relativo, intent tipográfico |

A diferença entre prompt amador e prompt utilizável é cobrir as quatro com intenção, não deixar default escolher por você.

## Camada 1: Canvas

Define o retângulo onde a imagem vive. É a primeira coisa que o modelo decide; se você não diz, ele assume.

### Aspect ratio comum

| Ratio | Uso típico | Parâmetro MJ | Notas |
|-------|------------|--------------|-------|
| `1:1` | Avatar, Instagram feed, ícone, post quadrado | `--ar 1:1` (default) | Universal |
| `16:9` | Hero blog/README, thumbnail YouTube, slide widescreen | `--ar 16:9` | Padrão "web hero" |
| `9:16` | Story (Instagram/TikTok), reels, mobile portrait, poster | `--ar 9:16` | Vertical mobile |
| `4:5` | Instagram feed portrait, LinkedIn post | `--ar 4:5` | Maximiza real estate em feed |
| `3:2` | Foto tradicional (35mm) | `--ar 3:2` | Bom pra mockup fotográfico |
| `1.91:1` | Twitter/X card, OG image | `--ar 1.91:1` | Específico social card |
| `11:17` | Poster impresso (legal) | `--ar 11:17` ou descrever | Portrait print |
| `2:3` | Capa de ebook, cartaz | `--ar 2:3` | Portrait |

### Como expressar canvas no prompt

- **Midjourney:** `--ar 16:9` no fim do prompt.
- **DALL-E 3:** texto explícito ("landscape 16:9") + parâmetro `size` na API (`1792x1024`, `1024x1024`, `1024x1792`).
- **Imagen 3:** parâmetro `aspectRatio` na API ou descrição textual ("widescreen 16:9 landscape").
- **FLUX/SD:** parâmetros `width` e `height` (números) na API ou UI.

### Padding e safe area

Pra entregáveis que vão receber overlay (texto, logo, CTA), descreva espaço negativo no prompt:

> "...com espaço negativo à direita pra overlay de título; ~30% do canvas livre"

Sem isso, o modelo enche tudo e você não tem onde colocar o overlay.

## Camada 2: Composição

Define onde cada elemento mora dentro do canvas. Vocabulário compositivo é estável entre modelos.

### Padrões compositivos que os modelos entendem

- **`centered composition`** — focal point centro
- **`rule of thirds`** — focal point em interseção 1/3-2/3
- **`top-heavy`** — peso visual no topo (típico de poster)
- **`bottom-heavy`** — peso visual no rodapé
- **`left-aligned subject, negative space at right`** — útil pra hero com overlay
- **`symmetrical`** — espelhamento, formal
- **`asymmetrical balance`** — peso compensado com intenção
- **`leading lines`** — linhas que guiam o olho
- **`overhead view`** / `top-down` / `bird's eye view`
- **`low angle`** / `worm's eye view`
- **`close-up`** / `wide shot` / `medium shot`
- **`extreme close-up`** / `macro`

### Hierarquia visual

Diga ao modelo qual elemento é o primário, secundário, terciário. "Hero ocupa 60% central; subtítulo abaixo, 20% da largura; tag pequena no rodapé" funciona melhor que "tudo na imagem".

### Framing

- **`framed by foliage`** / `framed by architecture` — moldura natural dentro da imagem
- **`vignette`** — escurecimento de bordas
- **`bokeh background`** — fundo desfocado
- **`depth of field`** — controle de profundidade

### Espaço negativo

`negative space at top right pra overlay text` é cláusula que economiza muita iteração. Sem isso, o modelo enche.

## Camada 3: Estilo

A linguagem visual. Onde "scene-first" mais erra (diz "futurista" e deixa o resto pro modelo), deliverable-first é cirúrgico.

### Tipo de ilustração

- **`flat illustration`** — vetorial sem profundidade, populares em SaaS/B2B
- **`isometric`** — 3D estilizado em projeção isométrica, popular em tech
- **`3D rendered`** / `3D render` / `octane render` — fotorrealístico CG
- **`photorealistic`** / `photograph` — fotografia
- **`watercolor`** / `oil painting` / `gouache` — pintura tradicional
- **`line art`** / `pen and ink` / `engraving` — traço
- **`vector illustration`** — limpo, escalável (SVG vibe)
- **`pixel art`** / `8-bit` / `16-bit` — retrô digital
- **`anime`** / `manga` — animação japonesa
- **`comic book`** / `graphic novel` — quadrinhos
- **`concept art`** — arte de produção
- **`technical illustration`** — diagramas estilizados

### Paleta de cor

Específica: `dark mode palette, midnight blue and violet`, `pastel palette with coral and mint`, `monochrome blue`, `high-contrast black and yellow`, `warm earth tones`.

Vaga (e não funciona bem): `colorful`, `nice colors`, `vibrant`.

### Mood / atmosfera

- **`corporate-modern`** — limpo, profissional, frio
- **`playful`** — descontraído
- **`vintage`** / `retro` — anos 70/80/90
- **`cyberpunk`** — neon, futurista distópico
- **`minimalist`** — espaço, contenção
- **`maximalist`** — denso, ornamentado
- **`brutalist`** — direto, sem ornamento
- **`dreamy`** / `ethereal` — etéreo
- **`gritty`** / `grunge` — texturizado

### Era estética (atalho potente)

`80s sci-fi`, `Y2K aesthetic`, `Bauhaus`, `Art Deco`, `Memphis design`, `Swiss design`, `Brutalist web`. Modelos têm prior forte pra essas eras.

## Camada 4: Texto

A camada mais difícil em 2026 — modelos ainda erram. Ideogram, Imagen 3/4 e FLUX dev lideram; DALL-E 3 razoável; Midjourney fraco; SD 3.5 inconsistente.

### Como pedir texto

1. **Cite as palavras exatas entre aspas no prompt.**
   > `the text "AI Summit 2026" at the top in bold sans-serif`
2. **Indique posição.**
   > `top center, occupying ~15% of height`
3. **Indique hierarquia (se múltiplo).**
   > `main title large; subtitle 50% size; tagline at bottom 30%`
4. **Indique intenção tipográfica (não exige fonte específica).**
   > `bold sans-serif, modern, geometric` ou `serif, classical, editorial` ou `handwritten script, casual`

### O limite atual

Mesmo com Ideogram, palavras com mais de ~30 caracteres começam a quebrar. Múltiplos blocos de texto (parágrafo + título + caption) raramente saem perfeitos numa só geração. Padrão prático em 2026:

- Texto **curto e único** (título de poster, "SALE", "404") → modelo gera direto
- Texto **médio** (título + subtítulo) → modelo gera, retoca tipografia no Figma/Canva
- Texto **longo ou múltiplos blocos** (infográfico denso) → gerar background sem texto + tipografar no Figma

Não fingir que o modelo resolve tudo — economiza horas.

## Exemplo: prompt dissecado nas quatro camadas

Goal: hero pra post de blog sobre "AI Engineering Stack — 11 camadas".

Prompt:

> "Hero image pra post de blog técnico. **Canvas: 16:9 landscape, 1920×1080**, espaço negativo à direita 35% pra overlay de título. **Composição:** isometric stack de 11 camadas translúcidas empilhadas verticalmente, à esquerda do canvas; rule of thirds (stack no terço esquerdo); leading lines do stack guiam pro espaço vazio à direita. **Estilo:** flat-isometric illustration, paleta dark mode (midnight blue #0F1B2D base, ciano #00D4FF accent, magenta #FF006E destaque ocasional), mood corporate-modern-tech, sem stock photo vibe. **Texto:** sem texto na imagem (vai ser overlay separado no Figma). Sem pessoas. Sem ícones genéricos de SaaS."

Dissecação:

- **Canvas:** 16:9, 1920×1080, 35% negative space à direita
- **Composição:** isometric stack, esquerda do canvas, rule of thirds, leading lines
- **Estilo:** flat-isometric, paleta dark mode específica com hex, mood corporate-modern-tech
- **Texto:** sem texto (overlay externo); constraints explícitas (sem pessoas, sem ícones SaaS genéricos)

Cada camada é decisão explícita. O modelo entra calibrado em vez de chutar.

## O hábito a internalizar

Antes de mandar o prompt, releia mentalmente:

1. **Canvas** — defini aspect ratio?
2. **Composição** — defini onde fica o hero e onde é espaço negativo?
3. **Estilo** — defini paleta, tipo de ilustração, mood?
4. **Texto** — defini se tem ou não, e se tem, onde e quais palavras?

Faltou alguma? O modelo vai escolher por você. Se faltou de propósito, ok. Se faltou por preguiça, vai ter que iterar mais.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #16 (Image Prompting).
- **Midjourney** — *Documentation* ([docs](https://docs.midjourney.com/)). Parâmetros `--ar`, vocabulário aceito.
- **OpenAI** — *Image generation guide* ([docs](https://platform.openai.com/docs/guides/images)). DALL-E 3 e descrição textual de canvas.

## Veja também

- [[02 - Deliverable-first, não scene-first]] — as camadas se conectam ao template canônico
- [[05 - Templates por entregável — poster, infográfico, mockup, thumbnail]] — templates aplicam as quatro camadas por tipo de entregável
- [[06 - Iteração visual — controlled changes]] — qual camada mudar quando o output não bate
- [[07 - Geração de diagramas e ilustrações técnicas]] — limites da camada texto em diagramas
