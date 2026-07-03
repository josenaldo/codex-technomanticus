---
title: "04 - Anatomia de um prompt visual — canvas, composição, estilo"
created: 2026-05-28
updated: 2026-07-03
type: concept
status: growing
fase: Iniciado
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
> Todo prompt visual eficaz tem quatro camadas: **canvas** (formato, aspect ratio, resolução), **composição** (hierarquia, focal point, espaço negativo), **estilo** (linguagem visual, paleta, mood) e **texto** (palavras embutidas, posição, hierarquia).
> Cada camada tem vocabulário próprio que os modelos reconhecem.
> A regra do default: quando você escreve sem cobrir as quatro, o modelo escolhe default genérico; quando cobre todas, converge rápido.
> Esta nota dá o vocabulário preciso por camada, com exemplo de prompt completo dissecado em cada uma.

> [!question]- Qual é a ordem certa de escrever as quatro camadas? E se eu não souber o estilo que quero?
> A ordem mais produtiva é Canvas → Composição → Estilo → Texto: cada camada depende da anterior (você não define composição sem saber o canvas; o texto é a camada mais dependente do estilo). Se não souber o estilo: comece com um estilo "âncora" genérico (`flat illustration`) e itere só a camada de estilo enquanto congela as outras três. Mudar tudo ao mesmo tempo faz com que você não saiba o que causou o resultado. Quando travar, volte ao deliverable (nota 02): o estilo deve servir ao entregável, não ao gosto pessoal. Um hero tech-blog pede `flat-isometric corporate-modern`; um post de redes sociais pode pedir `bold graphic`, `pop art`; uma capa de ebook pode pedir `editorial photography`. O deliverable resolve o estilo 80% das vezes.

## As quatro camadas

Você abre o Midjourney com o tema já decidido — "preciso de um hero pra post de blog sobre IA" — e nada além disso, e trava na caixa de prompt: digita o tema, aperta enter, e a imagem sai com composição arbitrária, paleta que não bate com a marca, texto ilegível quando você pediu. O problema não é o modelo; é que "tema" cobre só uma fração do que uma imagem precisa pra existir — faltam decisões sobre o retângulo onde ela vive, a disposição dos elementos dentro dele, a linguagem visual e o texto embutido. Se você não decide essas quatro coisas, o modelo decide por você, e o resultado é o default genérico da camada que ficou muda. A tabela abaixo nomeia as quatro camadas e a pergunta que cada uma responde.

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

### Ângulo e ponto de vista (câmera)

O ângulo altera radicalmente a hierarquia e o peso emocional da imagem, independente do conteúdo:

- **`eye level`** — neutro, jornalístico, mais próximo ao observador
- **`low angle`** / `worm's eye view` — sujeito imponente, heroico, em posição de poder
- **`high angle`** / `bird's eye view` / `overhead` — sujeito vulnerável, panorâmico, documentário
- **`dutch angle`** — câmera inclinada, tensão, desorientação
- **`straight-on, flat`** — frontal absoluto, editorial, UI mockup
- **`three-quarter view`** — perspectiva isométrica leve, popular em ilustração de produto
- **`top-down`** — vista de cima, flat lay, overhead, dashboard
- **`45° angle`** — equilíbrio entre frontal e lateral

Para entregáveis tech (hero, infográfico, diagrama), `top-down` e `isometric` dominam porque permitem mostrar múltiplas camadas sem profundidade ambígua. Para entregáveis de pessoas ou narrativa, `eye level` é o default neutro.

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

## Combinando camadas — defaults por deliverable

Quando você não sabe o que colocar em cada camada, estes defaults cobrem 80% dos casos comuns:

| Deliverable | Canvas | Composição | Estilo |
|-------------|--------|------------|--------|
| Hero de blog (tech) | 16:9, 1792×1024 | Subject esquerda, negative space direita | flat-isometric, dark mode, corporate-modern |
| Thumbnail YouTube | 16:9, 1280×720 | Centered, bold, high contrast | bold graphic, 2-3 cores, sem texto sutil |
| Story/Reels | 9:16 | Top 60% visual, bottom 40% texto/CTA | modern, brand palette |
| Social card (LinkedIn) | 4:5 ou 1:1 | Centered ou left-aligned | corporate-clean, brand colors |
| Poster evento | A3 / 11:17 | Top-heavy, hierarquia 3 níveis | depende da marca; editorial ou bold |
| Capa e-book | 2:3 | Subject ocupa 70%, título ocupa 30% inferior | editorial, contraste alto |
| Banner LinkedIn/GitHub | 8:2.7 | Wide, landscape, negspace central ou lateral | minimalista, azul/tech, sem elemento central |
| Carousel slide | 1:1 ou 4:5 | Grid ou half/half | consistente com slide 1 (usar --sref ou IP-Adapter) |

Esses defaults não substituem a nota do template (nota 05) — use pra rascunho rápido, depois refine com o template completo.

## Camada 4: Texto

A camada mais difícil em 2026 — modelos ainda erram. Ideogram, Imagen 3 (e Imagen 4 quando disponível) e FLUX dev lideram; DALL-E 3 razoável; Midjourney fraco; SD 3.5 inconsistente.

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

## Exercício: construindo o prompt camada a camada

Ponto de partida: "preciso de um hero pra post sobre segurança de APIs".

**Passo 1 — Canvas:** qual canal? Post de blog. Ratio: `16:9`. Resolução: `1792×1024`. Vai ter overlay de título → negative space direita `~35%`.

**Passo 2 — Composição:** subject à esquerda, guarda direita pra overlay. Subject = escudo digital abstrato ou cadeado luminoso, não pessoa. `left-aligned subject, negative space at right`. Sem texto na imagem.

**Passo 3 — Estilo:** tech, B2B, dark mode. `flat-isometric illustration, dark mode palette — midnight blue #0F1B2D base, neon green #00FF88 accent`. Mood: `corporate-modern-tech`. Sem stock photo vibe, sem clipart.

**Passo 4 — Texto:** `no text in image`. Decisão: overlay externo no Figma.

**Prompt final (montado das 4 camadas):**

> "Hero image for a tech blog post, 16:9 canvas, negative space at right ~35% for title overlay. Left-aligned subject: abstract glowing shield with circuit-board texture — flat-isometric illustration style. Dark mode palette: midnight blue #0F1B2D base, neon green #00FF88 accent. Mood: corporate-modern-tech. No text in image. No people. No generic SaaS icons."

O resultado já chega muito mais próximo do brief do que "hero sobre segurança de APIs, estilo moderno".

## O hábito a internalizar

Antes de mandar o prompt, releia mentalmente:

1. **Canvas** — defini aspect ratio?
2. **Composição** — defini onde fica o hero e onde é espaço negativo?
3. **Estilo** — defini paleta, tipo de ilustração, mood?
4. **Texto** — defini se tem ou não, e se tem, onde e quais palavras?

Faltou alguma? O modelo vai escolher por você. Se faltou de propósito, ok. Se faltou por preguiça, vai ter que iterar mais.

## Armadilhas comuns

> [!warning] Definir estilo com um adjetivo vago — "futurista", "moderno", "bonito"
> "Futurista" pode ser cyberpunk neon, space opera, retrofuturismo dos anos 70, minimalismo sci-fi ou tech corporativo azul. O modelo chuta. "Bonito" não é instrução — é esperança. Cada adjetivo de estilo ambíguo que você usa transfere a decisão criativa para o modelo. A correção é específica: `flat-isometric, dark mode, midnight blue + ciano, corporate-modern-tech` em vez de "futurista". Se você não souber o estilo, comece com um âncora genérico e itere só a camada de estilo. Um adjetivo específico por dimensão (tipo de ilustração, paleta, mood, era) é suficiente pra calibrar o output.

> [!warning] Omitir o espaço negativo quando o deliverable vai receber overlay
> Hero com overlay de título, thumbnail com texto, social card com CTA — todos precisam de espaço onde o texto vai ficar. Se o prompt não descreve `negative space at right ~35%` ou equivalente, o modelo enche o canvas. Você então tenta inpaint pra criar espaço, ou vai pro Figma cortar o que o modelo gerou. O lugar correto pra essa instrução é no prompt, não na iteração. Antes de enviar qualquer prompt de entregável com overlay, pergunte: "onde vai sentar o texto?" Se não sabe, define primeiro.

> [!warning] Pedir texto longo ou múltiplos blocos sem Figma como etapa de produção
> Modelos de imagem em 2026 ainda erram texto: palavras trocadas, letras fundidas, frases cortadas no meio. Ideogram e Imagen 3 são os melhores, mas mesmo eles falham em blocos com mais de ~30-40 caracteres ou múltiplos textos simultâneos. O padrão produtivo: texto curto (título único, sigla, uma frase) → modelo pode entregar; texto médio a longo (subtítulo + body + caption) → gerar background sem texto + tipografar no Figma/Canva. Aceitar isso como fluxo de produção normal, não como limitação a contornar, economiza horas de iteração.

## Como explicar em inglês

**Interview quote:** *"Every visual prompt has four layers: canvas, composition, style, and text. Canvas sets the bounding rectangle and aspect ratio; composition defines where elements live and how negative space works; style specifies the visual language — illustration type, palette, mood, aesthetic era; and text handles embedded words, position, and typographic intent. Leaving any layer unspecified means the model picks a generic default. Covering all four — with specific vocabulary each model recognizes — is what makes prompts converge in fewer iterations."*

| Português | Inglês |
|---|---|
| Canvas (formato, proporção) | Canvas (format, aspect ratio) |
| Composição (hierarquia visual) | Composition (visual hierarchy) |
| Estilo (linguagem visual) | Style (visual language) |
| Paleta de cor específica | Specific color palette |
| Espaço negativo pra overlay | Negative space for text overlay |
| Tipo de ilustração (flat, isometric, 3D) | Illustration type (flat, isometric, 3D) |
| Mood / atmosfera | Mood / atmosphere |
| Era estética (âncora de estilo) | Aesthetic era (style anchor) |
| Texto embutido na imagem | Embedded text in image |
| Intenção tipográfica (sem fonte específica) | Typographic intent (no specific font) |

## O que vem a seguir

Com a anatomia das quatro camadas mapeada, a nota 05 aplica esse vocabulário em templates por entregável: cada tipo de deliverable (poster, infográfico, mockup, thumbnail, hero, e-book, banner) tem defaults recomendados para cada uma das quatro camadas — para que você não parta do zero toda vez que abrir um projeto novo.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #16 (Image Prompting).
- **Midjourney** — *Documentation* ([docs](https://docs.midjourney.com/)). Parâmetros `--ar`, vocabulário aceito.
- **OpenAI** — *Image generation guide* ([docs](https://platform.openai.com/docs/guides/images)). DALL-E 3 e descrição textual de canvas.
- **Ideogram** — *Prompt guide* ([docs](https://ideogram.ai/docs)). Texto embutido e paleta.
- **Canva Design School** — *Composition fundamentals*. Vocabulário compositivo.

## Veja também

- [[02 - Deliverable-first, não scene-first]] — as camadas se conectam ao template canônico
- [[03 - Modelos de imagem 2026 — DALL-E, Imagen, Midjourney, FLUX, SD]] — qual modelo suporta melhor a camada de texto
- [[05 - Templates por entregável — poster, infográfico, mockup, thumbnail]] — templates aplicam as quatro camadas por tipo de entregável
- [[06 - Iteração visual — controlled changes]] — qual camada mudar quando o output não bate
- [[07 - Geração de diagramas e ilustrações técnicas]] — limites da camada texto em diagramas
- [[Dicionário de IA#Aspect ratio|Dicionário: Aspect ratio]]
- [[Dicionário de IA#Composição visual|Dicionário: Composição visual]]
- [[Dicionário de IA#Espaço negativo|Dicionário: Espaço negativo]]
- [[Dicionário de IA#Flat illustration|Dicionário: Flat illustration]]
- [[Dicionário de IA#Isometric|Dicionário: Isometric]]
