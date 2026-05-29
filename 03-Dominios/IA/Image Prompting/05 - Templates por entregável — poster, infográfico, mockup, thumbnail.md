---
title: "05 - Templates por entregável — poster, infográfico, mockup, thumbnail"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - image-prompting
  - prompt-engineering
  - ia
  - templates
publish: true
aliases:
  - Templates por entregável
  - Image prompting cookbook
---

# 05 - Templates por entregável — poster, infográfico, mockup, thumbnail

> [!abstract] TL;DR
> Cada tipo de entregável tem template estável que economiza horas de iteração. Esta nota traz seis templates prontos: **poster**, **infográfico**, **carousel slide**, **thumbnail YouTube**, **mockup mobile/desktop** e **hero image (README/blog)**. Cada um vem com (1) decisões implícitas (canvas, hierarquia, restrições), (2) prompt completo de exemplo nas quatro camadas e (3) modelo recomendado em 2026. Aproveite copiando e adaptando — não decorando.

## Como usar os templates

Cada template segue a estrutura da nota [[04 - Anatomia de um prompt visual — canvas, composição, estilo]]:

- **Canvas** já fixado pelo tipo de entregável
- **Composição** com hierarquia típica
- **Estilo** parametrizável (paleta, tipo de ilustração)
- **Texto** com posição e hierarquia típicas

Você substitui o conteúdo variável (`<...>`) e ajusta estilo conforme marca/contexto.

## Template 1: Poster (evento, anúncio, recrutamento)

### Decisões implícitas
- Canvas portrait (11×17 print, ou 2:3 / 9:16 digital)
- Hierarquia top-down: título topo → hero centro → info rodapé
- Espaço pra título grande (poster vive de longe)
- Texto crítico (precisa ser legível)
- Modelo: **Ideogram 2** (one-off) ou **Imagen 3** (volume)

### Prompt template

> "Poster pra `<evento/anúncio>`. Canvas portrait `<11:17 print | 2:3 | 9:16>`, alta resolução. Composição top-heavy: título grande no topo (~15-20% da altura), hero centralizado no meio (~50-60%), informações secundárias no rodapé (~15-20%). Hero: `<descrição visual abstrata ou metáfora — ex: 'network neural fluido em gradiente azul/violeta'>`. Texto: título '`<TÍTULO>`' em bold sans-serif, branco sobre fundo escuro; subtítulo '`<subtítulo>`' 40% do tamanho do título; rodapé com `<data>` · `<local>` em sans-serif limpo. Paleta: `<dark mode midnight blue + ciano | pastel + coral | monochrome>`. Mood: `<corporate-modern | playful | editorial>`. Sem stock photo vibe. Sem moldura decorativa."

### Exemplo preenchido

> "Poster pra hackathon de IA. Canvas portrait 11:17, alta resolução. Composição top-heavy: título grande no topo (~18% da altura), hero centralizado no meio (~55%), informações secundárias no rodapé (~17%). Hero: cluster abstrato de nós conectados em gradiente fluido azul/violeta, sensação de rede neural. Texto: título 'AI HACK 2026' em bold sans-serif geométrica, branco sobre fundo dark; subtítulo 'Build the impossible in 48h' 35% do tamanho; rodapé 'March 15-17 · São Paulo' em sans-serif limpa. Paleta: dark midnight blue base + ciano #00D4FF accent. Mood: corporate-modern-tech. Sem stock photo vibe. Sem moldura decorativa."

## Template 2: Infográfico

### Decisões implícitas
- Canvas square (1:1) ou vertical (4:5, 9:16)
- Multi-seção, leitura top-down
- Ícones + texto curto por seção
- Texto **muito** crítico (e historicamente quebra)
- Modelo: **Ideogram 2** ou geração de background sem texto + tipografia no Figma

### Prompt template (versão híbrida — mais confiável em 2026)

> "Background pra infográfico de `<tópico>`. Canvas `<1:1 | 4:5 | 9:16>`. Composição: layout em `<N seções verticais separadas por divisores sutis | grid 2×2 | spiral>`. Cada seção tem espaço pra ícone à esquerda e texto curto à direita. Estilo: flat illustration, paleta `<dark mode | pastel | monochrome>`, mood limpo e educacional. Sem texto na imagem (texto será adicionado no Figma). Sem ícones genéricos de SaaS — quero `<descrição de ícones específicos>`."

### Exemplo preenchido

> "Background pra infográfico sobre 'As 11 camadas do AI Engineering Stack'. Canvas 4:5 portrait. Composição: layout em 11 fileiras horizontais separadas por linhas sutis, cada uma com espaço pra ícone à esquerda (~15% da largura) e texto curto à direita (~60% da largura), margem 25% pra título no topo. Estilo: flat illustration, paleta dark mode (midnight blue base + ciano accent), mood limpo, técnico-editorial. Sem texto na imagem (será adicionado no Figma). Ícones: cada um relacionado a camada de software (ex: documento pra prompt, banco de dados pra context, peça de engrenagem pra tool)."

## Template 3: Carousel slide (LinkedIn / Instagram)

### Decisões implícitas
- Canvas 1:1 ou 4:5
- Um takeaway por slide
- Template consistente entre slides da série
- Texto curto, grande, alto contraste
- Modelo: **Ideogram 2** (texto) ou **Midjourney** com `--sref` (estilo consistente)

### Prompt template

> "Slide `<N>` de carousel sobre `<tópico>`. Canvas 4:5 portrait, 1080×1350. Composição: número do slide pequeno no canto superior `<esquerdo | direito>`; takeaway central grande em 1-2 linhas; ilustração de apoio à `<direita | abaixo>`; rodapé com nome do autor e CTA pequenos. Texto principal: '`<takeaway curto, max 60 chars>`' em bold sans-serif, alto contraste. Estilo: `<flat illustration | minimalist | editorial>`, paleta `<...>`, consistente com restante do carousel. Sem fundos floridos. Sem stock photo. `<--sref <url> pra MJ se reutilizando estilo>`."

### Exemplo preenchido

> "Slide 3/7 de carousel sobre 'Como escolher modelo de IA'. Canvas 4:5 portrait, 1080×1350. Composição: '3/7' pequeno no canto superior direito; takeaway central grande em 1-2 linhas; ilustração de balança de pratos à direita; rodapé com '@josenaldo' e seta '→' pra próximo slide. Texto principal: 'Custo vs qualidade' em bold sans-serif geométrica, branco sobre fundo dark blue. Estilo: flat illustration, paleta dark mode midnight blue + amarelo accent, consistente com slides anteriores. Sem fundos floridos. Sem stock photo."

## Template 4: Thumbnail YouTube

### Decisões implícitas
- Canvas 16:9 obrigatório
- Alta legibilidade em 120×68px (preview)
- Hero grande (face, objeto ou ícone) + texto bold curto
- Cores saturadas, contraste forte
- Modelo: **Ideogram 2** (texto) ou **Imagen 3**

### Prompt template

> "Thumbnail YouTube pra vídeo '`<título do vídeo>`'. Canvas 16:9 landscape, 1280×720. Composição: hero grande à `<esquerda | direita>` ocupando ~50% do canvas; texto grande bold no espaço restante. Hero: `<descrição — objeto ou cena que ancora o tópico>`. Texto: '`<TEXTO CURTO MAX 4-5 PALAVRAS>`' em sans-serif extra-bold, cor `<branca | amarela | vermelha>` com outline `<preto | escuro>` pra contraste em qualquer fundo. Paleta: alta saturação, contraste forte. Mood: clickable mas honesto (sem clickbait visual extremo). Sem rosto humano se não for o autor; sem setas vermelhas falsas."

### Exemplo preenchido

> "Thumbnail YouTube pra vídeo 'RAG sem Vector Database'. Canvas 16:9 landscape, 1280×720. Composição: hero à esquerda (~50%) — pilha de documentos digitais conectados por linhas fluidas; texto grande bold na metade direita. Hero: documentos translúcidos em gradiente azul, sensação de árvore de retrieval. Texto: 'RAG SEM VECTOR DB' em sans-serif extra-bold, cor amarela com outline preto. Paleta: alta saturação, fundo dark blue → preto gradient. Mood: clickable mas honesto. Sem rosto humano. Sem setas vermelhas falsas."

## Template 5: Mockup mobile/desktop

### Decisões implícitas
- Canvas 16:9 (desktop) ou 9:16 (mobile)
- Device frame realístico (laptop, smartphone)
- Tela com conteúdo plausível
- Lighting e contexto ambiental
- Modelo: **DALL-E 3** ou **Imagen 3** (photorealismo)

### Prompt template

> "Mockup `<mobile | desktop>` photorealístico do app '`<nome>`'. Canvas `<9:16 portrait | 16:9 landscape>`. Composição: device frame `<iPhone 15 Pro genérico | MacBook Pro genérico>` centralizado, ângulo `<frontal | levemente angulado | 3/4>`. Tela exibe: `<descrição da UI — ex: 'app de chat com bolhas de mensagem, header com nome do usuário, lista de conversas'>`. Estilo: photorealistic product shot, lighting `<studio limpo | natural diurno | dramático>`, fundo `<plain neutral | desk com elementos sutis | gradient suave>`. Sem texto legível nos elementos da UI (vai ser editado depois). Sem branding de Apple/Google explícito (device genérico)."

### Exemplo preenchido

> "Mockup mobile photorealístico do app 'EstudeMe'. Canvas 9:16 portrait. Composição: smartphone genérico centralizado, ângulo levemente angulado 3/4. Tela exibe: dashboard de estudo com card de plano de estudo no topo, lista de flashcards abaixo, botão flutuante de 'iniciar sessão' no canto inferior direito. Estilo: photorealistic product shot, lighting studio limpo soft, fundo gradient suave azul-acinzentado. Sem texto legível na UI (placeholder edit depois). Sem branding Apple/Google explícito."

## Template 6: Hero image (README / blog post)

### Decisões implícitas
- Canvas 16:9 wide (ou 21:9 ultra-wide pra README)
- Abstrato ou conceitual (deixa overlay funcionar)
- Espaço negativo pra texto/logo
- Coerente com tom do projeto
- Modelo: **Midjourney v6.1** (artístico) ou **FLUX dev** (open-source com qualidade próxima)

### Prompt template

> "Hero image pra `<README do projeto X | post de blog sobre Y>`. Canvas 16:9 landscape, `<1920×1080 | 2560×1080 ultra-wide>`. Composição: focal point à `<esquerda 40% | direita 40% | centro>`; ~`<35-40%>`% do canvas livre como espaço negativo pra overlay de título. Subject: `<descrição — abstrato ou metafórico, evitar literalidade>`. Estilo: `<flat-isometric illustration | abstract digital art | minimalist tech illustration>`, paleta `<...>`, mood `<corporate-modern | editorial | playful-tech>`. Sem texto na imagem. Sem stock photo vibe. Sem pessoas se não for caso específico."

### Exemplo preenchido

> "Hero image pra post de blog sobre 'Prompt Engineering não morreu'. Canvas 16:9 landscape, 1920×1080. Composição: focal point à esquerda 40%; ~40% à direita livre como espaço negativo pra overlay de título. Subject: balança visual entre uma pena (tipografia clássica, prompt artesanal) e um servidor abstrato (engenharia de sistema) — em equilíbrio, não em conflito. Estilo: editorial digital illustration, paleta sépia + azul-profundo, mood editorial-técnico. Sem texto na imagem. Sem stock photo vibe. Sem pessoas. `--ar 16:9 --stylize 250` se Midjourney."

## Recapitulação rápida

| Entregável | Canvas típico | Modelo recomendado | Crítico |
|------------|---------------|--------------------|---------|
| Poster | 11:17 / 2:3 / 9:16 | Ideogram / Imagen | Texto grande legível |
| Infográfico | 1:1 / 4:5 / 9:16 | Ideogram + Figma | Hierarquia + texto curto |
| Carousel slide | 1:1 / 4:5 | Ideogram / MJ `--sref` | Consistência entre slides |
| Thumbnail | 16:9 | Ideogram / Imagen | Legibilidade em 120×68px |
| Mockup | 9:16 / 16:9 | DALL-E 3 / Imagen | Photorealism + device frame |
| Hero | 16:9 / 21:9 | Midjourney / FLUX dev | Espaço negativo pra overlay |

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #16 (Image Prompting). Templates inspirados na estrutura apresentada.
- **Midjourney** — *Documentation* ([docs](https://docs.midjourney.com/)). `--ar`, `--stylize`, `--sref`.
- **Ideogram** — *Docs* ([docs](https://docs.ideogram.ai/)). Texto-na-imagem.
- **OpenAI** — *Image generation guide* ([docs](https://platform.openai.com/docs/guides/images)). DALL-E 3 sizes e prompts estruturados.

## Veja também

- [[02 - Deliverable-first, não scene-first]] — template canônico que estes templates derivam
- [[03 - Modelos de imagem 2026 — DALL-E, Imagen, Midjourney, FLUX, SD]] — escolha de modelo por template
- [[04 - Anatomia de um prompt visual — canvas, composição, estilo]] — vocabulário usado nos templates
- [[06 - Iteração visual — controlled changes]] — como ajustar quando o primeiro output não bate
