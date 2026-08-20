---
title: "02 - Deliverable-first, não scene-first"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: iniciado
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

> [!question]- O template tem 10 campos — preciso preencher todos? E em que ordem?
> Não. Campos obrigatórios são Deliverable, Canvas e Subject — com esses três o modelo sai do default e entrega algo utilizável. Os demais adicionam precisão incremental. A ordem importa: (1) Deliverable ancora tudo; (2) Canvas define formato antes de descrever conteúdo; (3) Subject descreve o que aparece; (4) Composition e Style refinam o visual; (5) Text e Constraints fecham. Goal e Audience são contexto mental — ajudam você a decidir os outros campos, mas raramente precisam ir literalmente no prompt. Iteration nunca vai no prompt. Regra prática: 5 campos bem preenchidos batem 10 campos vagos.

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
Palavras exatas que devem aparecer, com posição e tamanho relativo. Em 2026, texto ainda é o ponto fraco da maioria dos modelos (Ideogram, Imagen 4 quando disponível e FLUX lideram). Se texto é crítico, escolha modelo ou pré-aceite que vai rodar texto no Figma/Canva depois.

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

## Canvas e aspect ratio — tabela de referência

Errar o canvas é o erro mais barato de evitar — e um dos mais comuns. Referência rápida por canal:

| Canal / uso | Aspect ratio | Dimensões típicas | Notas |
|---|---|---|---|
| Hero blog / README | 16:9 | 1920×1080 | Landscape, espaço pra título overlay |
| Thumbnail YouTube | 16:9 | 1280×720 mín | Texto deve ser visível em 120px de altura |
| Post Instagram (feed) | 1:1 ou 4:5 | 1080×1080 ou 1080×1350 | 4:5 ocupa mais tela no feed mobile |
| Story Instagram / TikTok | 9:16 | 1080×1920 | Portrait full-screen |
| Post LinkedIn | 1.91:1 | 1200×628 | Landscape com espaço textual |
| Capa de e-book | 6:9 | 1600×2400 | Portrait livro |
| Poster print A4 | √2:1 | 2480×3508 (300dpi) | Portrait A4 |
| Slide (16:9) | 16:9 | 1920×1080 ou 2560×1440 | Landscape, margens maiores que blog |
| Card social quadrado | 1:1 | 1080×1080 | Mínimo seguro pra todas as redes |
| Open Graph (SEO) | 1.91:1 | 1200×630 | Thumbnail em links compartilhados |

Antes de escrever o prompt, fixe o canvas. Mudar após a geração exige inpainting (outpaint das bordas) ou recorte, que raramente termina sem retrabalho.

## Construindo o prompt passo a passo — exercício

Conversão de scene-first pra deliverable-first em 5 passos explícitos:

**Cena original:** "A robot reading a book in a cozy library."

**Passo 1 — Deliverable:** O que é isso? Um hero image pra post de blog sobre IA e aprendizado.

**Passo 2 — Canvas:** Post de blog → 16:9, 1920×1080.

**Passo 3 — Subject:** A metáfora do robô-lendo segue, mas como asset pra 16:9 — robô à esquerda, espaço à direita pra título overlay.

**Passo 4 — Style:** Blog técnico-educativo → ilustração flat, paleta quente (laranja/âmbar + creme), sem fotorealismo.

**Passo 5 — Constraints:** Sem texto na imagem. Sem biblioteca real (só prateleiras abstratas). Sem clutter no fundo.

**Prompt resultante:**

```
Hero image para post de blog técnico sobre IA e aprendizado.
Canvas 16:9, 1920×1080.
Subject: robô abstrato e amigável lendo livro aberto, estilo flat illustration.
Composição: robô ocupa terço esquerdo do canvas, prateleiras de livros estilizadas ao fundo,
espaço negativo creme no terço direito para overlay de título.
Estilo: flat illustration, paleta âmbar/laranja + creme + azul suave, mood educativo-acolhedor.
Sem texto na imagem. Sem fotorealismo. Sem clutter no fundo.
```

O processo leva 2-3 minutos mas elimina 4-8 rerolls. A regra é: tempo de pensar antes de gerar é mais barato que tempo de retrabolhar depois. Para um entregável simples (blog hero), 5 minutos de planejamento de prompt economizam 20-30 minutos de iteração às cegas.

## Vocabulário de estilo — âncoras visuais por categoria

Lista de descritores que funcionam como âncora e reduzem ambiguidade. Use combinações:

### Estilo de ilustração
`flat design` | `isometric` | `3D rendered (Cinema 4D style)` | `vector illustration` | `watercolor` | `ink drawing` | `pixel art` | `low-poly` | `cel-shaded` | `photorealistic` | `concept art` | `editorial illustration`

### Paleta de cor
`dark mode (fundo #0d1117)` | `pastel muted` | `monochrome blue` | `limited palette (3 cores)` | `earth tones` | `neon on dark` | `warm cream + amber` | `cool slate + cyan`

### Mood/atmosfera
`corporate-clean` | `playful-educational` | `technical-precise` | `vintage-editorial` | `cyberpunk` | `brutalist` | `soft-modern` | `editorial magazine`

### Composição
`rule of thirds` | `centered subject` | `left-heavy, right negative space` | `top-heavy` | `full bleed` | `framed (white border)` | `diagonal composition` | `golden ratio crop`

Combine uma de cada categoria: `flat design, limited palette (azul + ciano + branco), corporate-clean, left-heavy` é um estilo determinístico que o modelo vai replicar de forma consistente entre gerações.

## Template em código — helper de prompt

Para pipelines que geram imagens programaticamente, encapsular o template em uma função elimina o risco de esquecer campos obrigatórios:

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ImageBrief:
    deliverable: str           # "hero blog", "thumbnail YouTube", "poster A4"
    canvas: str                # "16:9", "1:1", "9:16", "A4 portrait"
    subject: str               # descrição do conteúdo visual
    composition: Optional[str] = None
    style: Optional[str] = None
    text_in_image: Optional[str] = None
    constraints: list[str] = field(default_factory=list)

    def to_prompt(self) -> str:
        parts = [
            f"{self.deliverable.capitalize()}.",
            f"Canvas: {self.canvas}.",
            f"Subject: {self.subject}.",
        ]
        if self.composition:
            parts.append(f"Composição: {self.composition}.")
        if self.style:
            parts.append(f"Estilo: {self.style}.")
        if self.text_in_image:
            parts.append(f"Texto na imagem: {self.text_in_image}.")
        if self.constraints:
            parts.append("Constraints: " + "; ".join(self.constraints) + ".")
        return " ".join(parts)


# Uso
brief = ImageBrief(
    deliverable="Hero image para post de blog técnico sobre RAG",
    canvas="16:9, 1920×1080",
    subject="bibliotecário-IA abstrato, figura sugerindo arquivista digital com elementos de busca",
    composition="figura à esquerda em ~40% do canvas, espaço negativo à direita para overlay de título",
    style="flat illustration, paleta azul-profundo + ciano, mood técnico-elegante",
    constraints=["sem texto na imagem", "sem stock photo vibe", "sem bibliotecário humano realista"],
)

print(brief.to_prompt())
```

Output do `to_prompt()` vai direto no campo `prompt` de qualquer API de geração. A vantagem do dataclass: campos obrigatórios (deliverable, canvas, subject) geram `TypeError` se omitidos — o helper força a disciplina deliverable-first no próprio tipo.

## Armadilhas comuns

> [!warning] Preencher Subject primeiro e depois tentar encaixar o resto — destrói o benefício do deliverable-first
> O instinto de todo mundo ao imaginar uma imagem é descrever o que vê na cabeça — a cena. O deliverable-first exige inverter: defina o objeto (poster, hero, thumbnail) antes de descrever o visual. Se você começa escrevendo "um robô lendo um livro..." e só depois pensa "vai ser um hero de blog 16:9", o prompt vai priorizar a cena e ignorar o formato — e você vai ajustar via reroll em vez de via estrutura. A ordem correta: Deliverable → Canvas → Subject. Sempre.

> [!warning] Esquecer o Canvas e deixar o modelo escolher o aspect ratio — incompatibilidade com o canal
> DALL-E sem parâmetro de size gera 1:1 default. Midjourney sem `--ar` gera 1:1. Imagen sem aspect_ratio gera 1:1. Um hero de blog precisa de 16:9. Um story precisa de 9:16. Um poster precisa de portrait vertical. Se você não especificar o Canvas, vai receber 1:1 que não se encaixa em nenhum canal sem crop ou borda — que destrói a composição que o modelo gerou. Canvas é um dos dois campos obrigatórios (junto com Deliverable). Nunca omita.

> [!warning] Descrever o estilo em termos de sentimento ("aconchegante", "moderno", "elegante") sem ancora visual — modelo interpreta diferente do que você pensa
> "Aconchegante" pra um modelo pode ser laranja e madeira. Pra você pode ser azul e minimalista. "Moderno" pode ser flat design ou glassmorphism ou brutalism. Sentimentos como adjective de estilo são ambíguos. Sempre siga com uma ancora visual: "aconchegante — paleta âmbar, textura de madeira, iluminação suave de lamparina" ou "moderno — flat design, paleta limited, sem textura, tipografia sans-serif". A ancora elimina a ambiguidade sem banir o sentimento.

## Como explicar em inglês

**Interview quote:** *"Deliverable-first image prompting means you anchor the prompt to the artifact — poster, hero, thumbnail — before describing the visual content. The deliverable carries implicit constraints: format, hierarchy, audience, text space. Scene-first prompts lose 60-70% of generations to format mismatch. The template has 10 fields; you need at least Deliverable, Canvas, and Subject to converge faster."*

| Português | Inglês |
|---|---|
| Deliverable-first prompting | Deliverable-first prompting |
| Prompt orientado a cena | Scene-first prompt |
| Canvas / aspect ratio | Canvas / aspect ratio |
| Hierarquia visual | Visual hierarchy |
| Espaço negativo pra overlay de título | Negative space for title overlay |
| Composição (terço esquerdo, centro, rodapé) | Composition (left third, center, footer) |
| Constraints do entregável | Deliverable constraints |
| Reroll / regenar | Reroll / regenerate |
| Iteração convergente | Convergent iteration |

## O que vem a seguir

Com deliverable-first como mentalidade central, a nota 03 mapeia **quais modelos existem em 2026** e como a escolha de modelo segue a escolha de entregável — poster com texto vai pra Ideogram, photorealismo vai pra Imagen 3, artístico vai pra Midjourney, pipeline OSS vai pra FLUX.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #16 (Image Prompting). Template canônico Goal/Deliverable/Canvas/etc.
- **OpenAI** — *Image generation guide* ([docs](https://platform.openai.com/docs/guides/images)). Recomendações de prompt estruturado pro DALL-E.
- **Midjourney** — *Prompting guide* ([docs](https://docs.midjourney.com/hc/en-us/articles/360049775151-Prompting)). Vocabulário de composição e estilo.
- **Ideogram** — *Prompting tips* ([docs](https://docs.ideogram.ai/)). Técnicas pra texto-na-imagem via prompt estruturado.
- **Black Forest Labs** — *FLUX.1 prompt guide* ([docs](https://docs.bfl.ai/)). Prompt adherence e parâmetros de controle.

## Veja também

- [[01 - Image prompting como engenharia]] — por que a virada metodológica importa
- [[03 - Modelos de imagem 2026 — DALL-E, Imagen, Midjourney, FLUX, SD]] — modelo certo para cada entregável
- [[04 - Anatomia de um prompt visual — canvas, composição, estilo]] — desdobra cada campo do template em técnica
- [[05 - Templates por entregável — poster, infográfico, mockup, thumbnail]] — templates prontos por tipo de entregável
- [[06 - Iteração visual — controlled changes]] — como ajustar quando o primeiro output não bate
- [[07 - Geração de diagramas e ilustrações técnicas]] — quando deliverable-first não é suficiente
- [[Dicionário de IA#Deliverable-first|Dicionário: Deliverable-first]]
- [[Dicionário de IA#Canvas visual|Dicionário: Canvas visual]]
- [[Dicionário de IA#Aspect ratio|Dicionário: Aspect ratio]]
- [[Dicionário de IA#Constraints de prompt|Dicionário: Constraints de prompt]]
- [[Dicionário de IA#Hierarquia visual|Dicionário: Hierarquia visual]]
- [[Dicionário de IA#Composição visual|Dicionário: Composição visual]]
