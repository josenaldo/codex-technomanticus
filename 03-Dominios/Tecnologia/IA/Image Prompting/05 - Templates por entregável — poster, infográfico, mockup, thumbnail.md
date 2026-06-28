---
title: "05 - Templates por entregável — poster, infográfico, mockup, thumbnail"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: Iniciado
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

> [!question]- Preciso de um template que não está aqui — como criar um novo do zero?
> Siga o mesmo processo dos templates desta nota: (1) identifique o **Canal** (onde vai aparecer) → deriva o canvas; (2) determine a **Hierarquia** (o que é mais importante visualmente — lema, CTA, imagem?) → deriva composição; (3) levante as **Constraints implícitas** do canal (thumbnail precisa ser legível a 120px, story precisa de safe zone de 15% nas bordas, etc.); (4) escolha o modelo com base em se texto é crítico (Ideogram/Imagen) ou estilo importa mais (Midjourney/FLUX). Esses 4 campos viram o esqueleto do template. Depois teste com 3-5 variações, identifique o que sempre varia (conteúdo) vs o que sempre fica (canvas, estrutura), e isso é o seu template.

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

## Template 7: E-book / curso — capa

### Decisões implícitas
- Canvas 6:9 portrait (cover proporcional a livro)
- Hierarquia: título dominante, subtítulo abaixo, autor no rodapé
- Imagem de fundo compatível com texto sobre ela
- Modelo: **Imagen 3** (photorealismo) ou **Midjourney** (artístico)

### Prompt template

> "Capa de `<e-book | curso online>` sobre `<tópico>`. Canvas 6:9 portrait, ~1600×2400 alta resolução. Composição: imagem de fundo que cobre o canvas inteiro com overlay de gradiente suave (topo escuro → centro claro → base escura) pra permitir texto sobre ela. Fundo: `<descrição visual abstrata ou fotográfica relacionada ao tópico>`. O gradiente não aparece na imagem — é pra ser adicionado em pós-processamento. Estilo: `<photorealistic hero | editorial abstract | flat tech>`, paleta `<...>`, mood `<profissional | acolhedor | técnico>`. Sem texto na imagem. Sem logotipos. Sem marcas d'água."

### Exemplo preenchido

> "Capa de e-book sobre 'Engenharia de Prompt — Do básico ao sistema'. Canvas 6:9 portrait, 1600×2400 alta resolução. Composição: imagem de fundo com labirinto abstrato de linhas de código e circuitos em perspectiva, plano central com gradiente sutil do escuro ao claro. Estilo: editorial tech illustration, paleta dark mode azul-profundo + dourado/âmbar como accent, mood técnico-elegante. Sem texto na imagem. Sem logotipos. Sem marcas d'água."

## Template 8: Banner de perfil LinkedIn / GitHub

### Decisões implícitas
- Canvas 8:2.7 (4:1 aproximado) — 1584×396 LinkedIn; 1280×640 GitHub
- Horizontal muito largo e baixo
- Texto focal (nome, cargo, slogan) à esquerda; visual à direita
- Modelo: **Midjourney** ou **FLUX dev** (qualidade + espaço negativo)

### Prompt template

> "Banner de perfil `<LinkedIn | GitHub>` para `<pessoa/empresa>`. Canvas `<1584:396 | 1280:640>` landscape muito horizontal. Composição: metade esquerda com espaço para texto (fundo limpo, gradiente pra esquerda ou plain); metade direita com ilustração ou visual abstrato. Visual: `<descrição>`. Estilo: `<flat | abstract | editorial>`, paleta `<...>`, mood profissional. Sem texto na imagem. Sem frame/borda explícita. Não ocupar os 10% das extremidades superiores/inferiores (área pode ser cortada em mobile)."

### Exemplo preenchido

> "Banner de perfil LinkedIn para desenvolvedor fullstack especializado em IA. Canvas 1584×396 landscape muito horizontal. Composição: metade esquerda fundo dark blue limpo pra overlay de texto; metade direita com rede de nós interconectados em gradiente azul/ciano saindo da direita pra o centro. Estilo: flat digital art, paleta dark mode (navy + ciano + branco), mood profissional-tech. Sem texto na imagem. Sem borda. Não cortar os 10% das extremidades."

## Recapitulação rápida

| Entregável | Canvas típico | Modelo recomendado | Crítico |
|------------|---------------|--------------------|---------|
| Poster | 11:17 / 2:3 / 9:16 | Ideogram / Imagen | Texto grande legível |
| Infográfico | 1:1 / 4:5 / 9:16 | Ideogram + Figma | Hierarquia + texto curto |
| Carousel slide | 1:1 / 4:5 | Ideogram / MJ `--sref` | Consistência entre slides |
| Thumbnail | 16:9 | Ideogram / Imagen | Legibilidade em 120×68px |
| Mockup | 9:16 / 16:9 | DALL-E 3 / Imagen | Photorealism + device frame |
| Hero | 16:9 / 21:9 | Midjourney / FLUX dev | Espaço negativo pra overlay |
| Capa e-book | 6:9 | Imagen 3 / Midjourney | Compatível com texto sobre ela |
| Banner perfil | 8:2.7 | Midjourney / FLUX dev | Espaço negativo esquerdo; safe zone |

## Constraints universais — copie em qualquer template

Conjunto de constraints que funcionam independente do entregável, eliminando os erros mais comuns sem pensar:

**Anti-stock:**
```
Sem stock photo vibe. Sem pessoas genéricas de foto de banco de imagens.
Sem handshakes, meeting rooms ou laptops abertos desnecessariamente.
```

**Anti-clutter:**
```
Sem texto na imagem (será adicionado em pós-processamento).
Sem moldura ou borda decorativa. Sem watermark ou logo de preview.
Sem background florido. Sem elementos visuais não-relacionados ao tópico.
```

**Anti-IA-óbvio:**
```
Sem estética típica de IA generativa sem briefing (sem glowing orbs,
sem chrome textures aleatórias, sem anatomia distorcida).
Estilo determinístico e intencionalmente escolhido.
```

**Pro-qualidade:**
```
Alta resolução. Render limpo. Sem artefato de compressão.
Linha limpa onde há ilustração vetorial. Gradiente suave onde há fundo.
```

Copie o bloco inteiro nos prompts até internalizar — depois mantenha só o que for relevante pro entregável.

## Adaptando templates a brand guidelines

Templates desta nota assumem zero brand. Em projetos reais, você tem paleta, tipografia e tom de voz fixos. O processo de adaptação é simples — substitua os campos variáveis por valores fixos da brand:

1. **Paleta** → substitua `<paleta>` pelas cores hex da brand: `paleta marca (azul #1A56FF + branco #FFFFFF + dark navy #0B1930)`.
2. **Estilo de ilustração** → se a brand tem linguagem visual definida ("flat with soft shadows", "isometric 3D", "editorial photography"), coloque no campo Style.
3. **Mood** → traduza o brand voice pra adjetivos visuais: "inovador e acessível" → `"clean, approachable, not corporate-boring"`.
4. **Constraints de marca** → adicione constraints que protegem o brand: "Sem pessoas a não ser que sejam diversas e não-stock", "Sem ícones genéricos", "Sem gradiente que não seja o aprovado".

O resultado é um **brand template** — mais restrito que os templates genéricos desta nota, mas mais confiável de usar sem revisão manual extensa.

### Exemplo: brand guide → constraint do prompt

| Brand guide diz | Constraint no prompt |
|---|---|
| "Paleta: azul #1A56FF e laranja #FF6B35" | `paleta azul #1A56FF + laranja #FF6B35 como accent` |
| "Ilustração: flat sem gradiente" | `flat illustration, sem gradiente` |
| "Nunca usar imagens de rostos" | `Sem pessoas ou rostos na imagem` |
| "Tom: técnico mas humano" | `mood: tech-editorial, não corporate-genérico` |
| "Tipografia: Inter bold pra título" | `Sem texto na imagem — tipografia adicionada no Figma com Inter Bold` |

Dez minutos convertendo a brand guide em constraints de prompt economiza uma hora de revisão por asset.

## Checklist antes de gerar

Antes de clicar em "gerar", as cinco perguntas que previnem retrabalho:

- [ ] O **deliverable** está no prompt? (poster, thumbnail, hero, etc.)
- [ ] O **canvas/aspect ratio** está definido?
- [ ] A **hierarquia visual** está clara? (o que é principal, o que é secundário)
- [ ] O texto está marcado? Vai gerar junto (Ideogram/Imagen) ou vai ser overlay (constraint "Sem texto na imagem")?
- [ ] As **constraints** estão listadas? (sem stock photo vibe, sem texto borrado, sem moldura, etc.)

Se algum campo está vago, preencha antes de gerar — não depois de reroll.

## Armadilhas comuns

> [!warning] Usar template de poster pra thumbnail YouTube — hierarquia completamente diferente
> Poster lê-se de longe em formato portrait, com hierarquia top-heavy (título topo, hero centro, info rodapé). Thumbnail lê-se em 120×68px em landscape, com hero grande e texto de 3-4 palavras em letras enormes. Usar o template errado gera um thumbnail com hierarquia de poster — título pequeno no topo, hero centralizado sem espaço para legibilidade mínima. Sempre associe o template ao canal antes de escrever o prompt. A tabela de Recapitulação desta nota é o atalho.

> [!warning] Omitir "Sem texto na imagem" quando o texto vai ser adicionado depois — modelo injeta texto quebrado
> Quando você vai sobrepor texto em pós-processamento (Figma, Canva, Pillow), não dizer "sem texto na imagem" faz o modelo gerar texto no visual — muitas vezes ilegível, errado ou em posição que conflita com o overlay planejado. Sempre inclua a constraint quando o fluxo for: gerador → background limpo → overlay manual. A única exceção é quando você quer que o modelo tente renderizar o texto (Ideogram/Imagen), sabendo que vai revisar.

> [!warning] Especificar marca comercial real no device frame do mockup — modelo injeta logo da Apple/Google
> "iPhone 15 com logo da Apple visível" viola os termos de uso de vários providers (OpenAI, Google). Além disso, o modelo frequentemente distorce logos de marca registrada (símbolo da maçã virado, proporção errada). O padrão seguro é sempre "smartphone genérico" ou "device frame minimalista similar a smartphone de tela grande" — você captura o visual sem a marca. Se o mockup precisa de brand real, faça em Figma com device frame licenciado.

## Como explicar em inglês

**Interview quote:** *"For each deliverable type — poster, infographic, thumbnail, mockup, hero — there's a stable template that encodes the implicit decisions: canvas, hierarchy, text placement, constraints. Using the wrong template for the channel is the most common mistake: a poster prompt produces a bad thumbnail because portrait hierarchy breaks landscape readability. The template pre-loads those constraints so you only customize content."*

| Português | Inglês |
|---|---|
| Template por entregável | Deliverable template |
| Canvas fixado pelo entregável | Canvas determined by deliverable |
| Hierarquia top-heavy (topo pesado) | Top-heavy hierarchy |
| Espaço negativo pra overlay de texto | Negative space for text overlay |
| Device frame genérico | Generic device frame |
| Texto será adicionado em pós | Text to be added in post-processing |
| Safe zone das extremidades | Edge safe zone |
| Consistência entre slides de carousel | Consistency across carousel slides |
| Legibilidade em thumbnail pequeno | Readability at small thumbnail size |

## O que vem a seguir

Com os templates dominados, a nota 06 entra em **iteração visual disciplinada** — o que fazer quando o primeiro output não bate com o template esperado. Keep/Change/Do-not como framework, inpainting para correções locais, e quando aceitar "próximo" em vez de reroll infinito.

O ciclo completo é: (1) definir entregável e escolher template (nota 02 + esta nota); (2) adaptar o template ao contexto/brand; (3) gerar e avaliar contra o template; (4) iterar com disciplina (nota 06). Templates sem iteração disciplinada ainda geram retrabalho — e iteração sem template vira reroll cego.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #16 (Image Prompting). Templates inspirados na estrutura apresentada.
- **Midjourney** — *Documentation* ([docs](https://docs.midjourney.com/)). `--ar`, `--stylize`, `--sref` para consistência de estilo entre slides.
- **Ideogram** — *Docs* ([docs](https://docs.ideogram.ai/)). Texto-na-imagem.
- **OpenAI** — *Image generation guide* ([docs](https://platform.openai.com/docs/guides/images)). DALL-E 3 sizes e prompts estruturados.
- **Google** — *Imagen 3 on Vertex AI* ([docs](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview)). Aspect ratios e prompt guide.
- **Black Forest Labs** — *FLUX.1 docs* ([docs](https://docs.bfl.ai/)). FLUX.1 Tools Fill/Depth/Canny para edição de templates.
- **LinkedIn** — *Image size guide* ([help center](https://www.linkedin.com/help/linkedin/answer/a556015)). Tamanhos por tipo de post/banner.

## Veja também

- [[01 - Image prompting como engenharia]] — o brief como especificação (upstream desta nota)
- [[02 - Deliverable-first, não scene-first]] — template canônico que estes templates derivam
- [[03 - Modelos de imagem 2026 — DALL-E, Imagen, Midjourney, FLUX, SD]] — escolha de modelo por template
- [[04 - Anatomia de um prompt visual — canvas, composição, estilo]] — vocabulário usado nos templates
- [[06 - Iteração visual — controlled changes]] — como ajustar quando o primeiro output não bate
- [[07 - Geração de diagramas e ilustrações técnicas]] — templates para diagramas técnicos
- [[Dicionário de IA#Canvas visual|Dicionário: Canvas visual]]
- [[Dicionário de IA#Hierarquia visual|Dicionário: Hierarquia visual]]
