---
title: "02 - Deliverable-first, não scene-first"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - image-prompting
  - prompt-engineering
  - ia
  - deliverable-first
publish: true
aliases:
  - Deliverable-first
  - Scene-first vs deliverable-first
---

# 02 - Deliverable-first, não scene-first

> [!abstract] TL;DR
> A diferença entre image prompt que funciona e image prompt que dá voltas mora numa virada simples: descreva o **entregável** (poster, infográfico, slide, thumbnail, mockup, hero), não a **cena**. Cena ("dois empreendedores apertando a mão em escritório moderno") deixa o modelo escolher tudo o que importa pra entregável: formato, hierarquia, audiência, espaço pra texto. Entregável ("poster 11×17 pra evento de tecnologia, título 'AI Summit 2026' no topo, hero abstrato no centro, data e local rodapé") carrega essas constraints embutidas. O modelo já entra calibrado. O template @hooeem (Goal / Deliverable / Canvas / Audience / Subject / Composition / Style / Text / Constraints / Iteration) operacionaliza essa virada.

## Por que scene-first falha

O prompt "scene-first" descreve o que está acontecendo na imagem como se fosse roteiro:

> "Two business people shaking hands in a modern office, sunlight coming through window, laptop on desk, professional atmosphere."

Problemas:

1. **Sem âncora de formato.** O modelo escolhe um aspect ratio default (1:1 no DALL-E, 1:1 no Midjourney sem `--ar`). Se você precisava de 16:9 pro hero do post, foi pro lixo.
2. **Sem hierarquia.** O modelo distribui peso visual uniforme; tudo importa igual. Hero claro? Subtítulo? Espaço pra overlay? Inexistente.
3. **Sem decisão de canal.** O mesmo "two business people" funciona como capa de ebook, slide de deck, thumbnail YouTube ou banner LinkedIn? Cada um quer composição diferente.
4. **Sem texto.** Se você precisa de título embutido, o modelo não sabe.
5. **Iteração às cegas.** Não saiu como queria — mas qual variável mudar? Aspect ratio? Estilo? Composição? Vira reroll.

Resultado típico: 5 a 15 gerações até chegar perto, com 60-70% delas inutilizáveis por motivo de formato.

## Por que deliverable-first funciona

Prompt "deliverable-first" começa pelo objeto:

> "Poster pra evento de tecnologia 'AI Summit 2026'. Canvas vertical 11×17. Hero abstrato (network neural fluido em gradiente azul/violeta) ocupa centro. Título 'AI Summit 2026' em sans-serif bold no topo, branco sobre fundo escuro, ocupa ~15% da altura. Subtítulo 'Building the next decade' abaixo do título, 50% do tamanho. Data e local ('March 15-17 · São Paulo') no rodapé centralizado. Espaço negativo nas laterais. Estilo: limpo, corporativo-moderno, paleta dark mode."

A diferença não é só tamanho — é estrutura. O entregável carrega:

- **Formato** (11×17 vertical) → o modelo já entra com aspect ratio certo
- **Hierarquia** (hero centro, título topo, info rodapé) → distribuição de peso visual
- **Audiência implícita** (evento de tecnologia → vibe corporativa-moderna)
- **Canal implícito** (poster → portrait, alta densidade, sobrevive de longe e de perto)
- **Texto** (palavras exatas, posição, tamanho relativo)

O modelo perde menos graus de liberdade. As gerações convergem. A iteração vira: "tá quase — só o tamanho do título; mantenha o resto".

## O template canônico (Goal / Deliverable / Canvas / Audience / Subject / Composition / Style / Text / Constraints / Iteration)

Versão do template apresentado por @hooeem, com gloss curto em cada campo:

### Goal
Pra que serve esta imagem. Não é "um poster bonito" — é "promover o AI Summit 2026 em redes sociais e print". A meta enquadra todas as decisões abaixo.

### Deliverable
O tipo do entregável. Vocabulário curto: `poster | infográfico | slide | thumbnail YouTube | mockup mobile | mockup desktop | hero README | hero blog | carousel slide | social card | ebook cover | sticker | icon`. Esse é o anchor mais importante — modelos modernos têm prior forte pra cada palavra.

### Canvas
Aspect ratio + orientação + resolução-alvo. Exemplos: `16:9 landscape`, `9:16 portrait (story)`, `1:1 square`, `11:17 portrait print`, `4:5 portrait (Instagram feed)`. Modelos como Midjourney usam `--ar 16:9`; DALL-E e Imagen aceitam descrição textual ou parâmetro.

### Audience
Pra quem é. Engenheiro sênior? Recrutador? Audiência geral de LinkedIn? Comunidade open-source? Isso afeta tom visual: sério/lúdico, técnico/abstrato, denso/limpo.

### Subject
O que aparece. Aqui sim entra a "cena" — mas como **subordinada** ao entregável, não como protagonista. "Network neural fluido em gradiente" no exemplo do poster.

### Composition
Hierarquia visual. Onde fica cada elemento. "Hero centro, título topo, info rodapé". Use vocabulário de composição: `rule of thirds`, `centered`, `top-heavy`, `left-aligned`, `negative space at right`. O modelo entende essas convenções.

### Style
Linguagem visual. Paleta de cor (`dark mode`, `pastel`, `monochrome blue`), tipo de ilustração (`flat`, `isometric`, `3D rendered`, `watercolor`, `photorealistic`, `vector`), mood (`corporate-modern`, `playful`, `vintage`, `cyberpunk`). Quanto mais específico, melhor.

### Text
Palavras exatas que devem aparecer, com posição e tamanho relativo. Em 2026, texto ainda é o ponto fraco da maioria dos modelos (Ideogram, Imagen 4 e FLUX lideram). Se texto é crítico, escolha modelo ou pré-aceite que vai rodar texto no Figma/Canva depois.

### Constraints
O que **não** pode aparecer. "Sem pessoas", "sem stock photo vibe", "sem texto borrado", "sem moldura/borda decorativa". Modelos respondem melhor a constraints explícitas que a tom geral.

### Iteration
Plano de iteração — qual variável você mudaria primeiro se o output não bater. Não vai no prompt, mas vai no seu caderno (ou no Keep/Change/Do-not da próxima geração — ver [[06 - Iteração visual — controlled changes]]).

## Comparação lado a lado

Mesmo objetivo: hero pra post de blog sobre RAG.

### Versão scene-first (anti-padrão)

> "Librarian in a library full of books with computer chips, neural network glowing around, futuristic mood."

Output esperado: 1:1, bibliotecário central, sem espaço pra título, cores aleatórias, retrato estilo render genérico. Uso direto no post: zero.

### Versão deliverable-first

> "Hero image pra post de blog técnico sobre RAG (Retrieval-Augmented Generation). Canvas 16:9 landscape, 1920×1080. Audiência: engenheiros de IA. Subject: metáfora visual de bibliotecário-IA — figura abstrata sugerindo arquivista digital, com elementos de busca e conexão. Composição: figura à esquerda ocupando ~40% do canvas, espaço negativo à direita pra overlay de título. Estilo: ilustração vetorial flat, paleta azul-profundo + ciano, mood técnico-elegante, sem ser corporativo genérico. Sem texto na imagem. Sem stock photo vibe. Sem bibliotecário humano realista."

Output esperado: 16:9, hero à esquerda, espaço à direita, paleta consistente. Uso direto no post: alta probabilidade.

## Quando scene-first é ok

Casos onde "descrever a cena" basta:

- **Exploração inicial.** Você não sabe o que quer ainda; quer ver opções.
- **Imagem de uso único, descartável.** Ilustração rápida pra apresentação interna que ninguém vai revisar.
- **Estudo de estilo.** Está testando como um modelo responde a um conceito; output não vai virar entregável final.

Pra qualquer entregável que sai pro mundo (post público, README, deck pra cliente, asset de marketing), volte pro template deliverable-first.

## O hábito a internalizar

Antes de escrever o prompt, responda em voz alta:

1. O que estou entregando? (poster, hero, thumbnail, ...)
2. Em que formato? (aspect ratio, resolução)
3. Pra quem? (audiência)
4. Onde vai aparecer? (canal — README, Twitter, deck)

Só depois descreva o subject. Esse hábito de quatro perguntas previne 80% do retrabalho de image prompting.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #16 (Image Prompting). Template canônico Goal/Deliverable/Canvas/etc.
- **OpenAI** — *Image generation guide* ([docs](https://platform.openai.com/docs/guides/images)). Recomendações de prompt estruturado pro DALL-E.

## Veja também

- [[01 - Image prompting como engenharia]] — por que a virada metodológica importa
- [[04 - Anatomia de um prompt visual — canvas, composição, estilo]] — desdobra cada campo do template em técnica
- [[05 - Templates por entregável — poster, infográfico, mockup, thumbnail]] — templates prontos por tipo de entregável
- [[06 - Iteração visual — controlled changes]] — como ajustar quando o primeiro output não bate
