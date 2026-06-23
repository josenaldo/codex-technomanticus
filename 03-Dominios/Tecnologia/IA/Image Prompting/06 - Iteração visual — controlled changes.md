---
title: "06 - Iteração visual — controlled changes"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - image-prompting
  - prompt-engineering
  - ia
  - iteration
publish: true
aliases:
  - Iteração visual
  - Controlled visual changes
---

# 06 - Iteração visual — controlled changes

> [!abstract] TL;DR
> Iteração em image prompting é o mesmo princípio da iteração em prompt engineering pra texto: **uma mudança por vez, com hipótese explícita**. O padrão `Keep: / Change: / Do not:` adaptado pra imagem economiza horas. Quando muda demais de uma vez, perde a referência do que funcionou. Além de re-prompting, modelos modernos oferecem ferramentas de edição cirúrgica: inpainting (mudar só uma região), image-to-image (variação controlada), reference image (`--cref`, IP-Adapter), e ControlNet (controlar pose/edge/depth). Esta nota cobre o padrão Keep/Change/Do-not pra imagem e as principais ferramentas de edição em 2026.

## O princípio: uma mudança por vez

Erro mais comum em iteração visual:

> Output 1 sai. Você muda aspect ratio + paleta + composição + estilo + adiciona texto, tudo de uma vez. Output 2 sai diferente.

Se o output 2 está melhor, **qual mudança fez a diferença?** Você não sabe. Se está pior, qual reverter? Também não.

Princípio: muda uma variável por vez, sabendo qual hipótese está testando. Vem direto de [[Prompt Engineering]] — o ofício é o mesmo, modalidade diferente.

## O padrão Keep / Change / Do not (adaptado pra imagem)

Versão pra imagem do padrão do prompt engineering. Depois de cada geração:

```
Keep:
- <o que está funcionando — vou preservar>

Change:
- <a hipótese: vou mudar X esperando Y>

Do not:
- <o que apareceu indesejado — proíbo na próxima>
```

### Exemplo concreto

**Geração 1** com prompt do template de hero:

> "Hero pra post sobre RAG. Canvas 16:9. Hero à esquerda 40%, espaço negativo direita. Subject: bibliotecário-IA abstrato. Estilo flat-isometric, paleta dark blue + ciano. Sem texto."

Output: aspect ratio bom, espaço negativo ok, mas o "bibliotecário-IA" virou figura humana literal e o estilo saiu mais 3D que flat.

**Iteração 2:**

```
Keep:
- 16:9, hero à esquerda, espaço negativo à direita ✓
- Paleta dark blue + ciano ✓

Change:
- "Bibliotecário-IA" → "estante de livros translúcida com fluxo de luz por entre prateleiras"
  (hipótese: subject mais abstrato reduz a tendência de gerar pessoa)

Do not:
- Pessoas
- Renderização 3D fotorealístico (quero flat-isometric estrito)
```

Próximo prompt incorpora as mudanças cirurgicamente. Output 3 converge ou revela qual hipótese estava errada.

## Mesma sessão vs nova sessão (chat-based vs API)

### Em modelo chat-based (ChatGPT + DALL-E, Gemini + Imagen)

Mantém o contexto. Você diz "mesma coisa, mas em paleta pastel" e o modelo entende o referente. Vantagem: rapidez. Desvantagem: contexto de chat pode contaminar — modelo arrasta detalhes de tentativas anteriores que você não pediu.

Quando trocar pra novo chat:
- Mais de ~10 iterações sobre o mesmo asset
- Output começa a degradar sem motivo aparente
- Quer "limpar a mesa" e voltar ao prompt fresco

### Em modelo via API (FLUX, SD, Imagen API, Midjourney)

Cada chamada é stateless (exceto quando você passa `seed` ou `image_reference`). O prompt é a única memória. Vantagem: reprodutibilidade. Desvantagem: você reescreve o prompt inteiro a cada iteração.

Truque: versione seus prompts em arquivo (`prompts/hero-rag-v3.txt`). Diff entre v2 e v3 mostra exatamente o que mudou.

## Ferramentas de edição cirúrgica

Em 2026, geração from-scratch é só parte da produção. Edição cirúrgica resolve casos que reroll não resolveria.

### Inpainting (mudar só uma região)

Você pinta máscara sobre a região a mudar; o modelo regenera só ali, preservando o resto.

- **DALL-E Edit (OpenAI):** UI no ChatGPT permite selecionar região e descrever a mudança. API via `images.edit` aceita máscara PNG.
- **FLUX.1 Fill (BFL):** modelo dedicado de inpaint/outpaint.
- **SD Inpaint via ControlNet ou Automatic1111/ComfyUI:** controle granular, com peso configurável.

Caso clássico: hero ficou perfeito menos pela cara do personagem. Inpaint só a cara em vez de regenerar tudo.

### Outpainting (estender o canvas)

Imagem está boa mas você precisa de mais espaço à direita pra overlay. Outpainting estende. Mesma família de ferramentas (DALL-E Edit, FLUX Fill, SD Outpaint).

### Image-to-image (i2i)

Você dá uma imagem base + prompt → variação. O modelo preserva estrutura geral, modifica detalhes.

- **`strength`** (também chamado `denoise`) controla quanto preserva: 0.1 = quase idêntico, 0.9 = quase from-scratch
- Útil pra: refinar versão que tá quase boa, transformar sketch em arte final, "mesma cena, outra paleta"

### Reference image (preservar personagem/estilo)

- **Midjourney `--sref <url>`:** preserva *estilo* da imagem de referência.
- **Midjourney `--cref <url>`:** preserva *personagem* da imagem de referência.
- **SD IP-Adapter:** equivalente em SD; preserva conceito visual.
- **FLUX.1 Redux:** modelo do BFL pra variação preservando referência.

Caso clássico: 7 slides de carousel precisam estar visualmente consistentes. Gere o slide 1, use como `--sref` nos próximos.

### ControlNet (controle estrutural — SD e FLUX)

ControlNet permite forçar estrutura específica:
- **Canny / edge:** força os contornos.
- **Depth:** força a profundidade.
- **OpenPose:** força a pose humana.
- **Segmentation:** força regiões semânticas.
- **Scribble:** sketch como input.

Caso clássico: mockup precisa ter exatamente esse layout de UI. Sketch o wireframe; ControlNet canny garante que o modelo respeite.

## Padrão de iteração por tipo de problema

| Problema com o output | Ferramenta | Por quê |
|----------------------|------------|---------|
| Subject saiu errado, resto ok | Inpaint na região | Não reroll global |
| Estilo certo, paleta errada | Re-prompt mudando só paleta | Mudança simples |
| Quase perfeito, falta espaço | Outpaint | Estende, não regenera |
| Quero variações do mesmo conceito | i2i com `strength` 0.5 | Mantém DNA, varia |
| Precisa consistência entre N peças | `--sref` (MJ) ou IP-Adapter (SD) | Estilo coeso |
| Layout estrutural exato | ControlNet (SD/FLUX) | Força estrutura |
| Tipografia importante (texto preciso) | Gerar background sem texto + Figma | Modelo erra texto |

## A armadilha das 30 iterações

Tendência humana: vai iterando, vai iterando, e cada vez fica mais distante do output que era "bom o bastante" 5 iterações atrás. Sintomas:

- Você não consegue lembrar qual versão estava mais perto do brief
- Cada iteração introduz problema novo
- O brief original ficou turvo

Antídotos:

1. **Salvar versões.** Cada output vai pra pasta com prompt versionado. `hero-rag/v01-base.png`, `hero-rag/v01.prompt.txt`.
2. **Diff entre prompts.** Antes de mandar v8, compare com v7. Se mudou 5 coisas, recue.
3. **Reler o brief.** Volte ao Goal/Deliverable do template canônico. A v3 cumpria o brief? Se sim, é ela.
4. **Time-box.** Defina 5 ou 10 tentativas. Se não convergiu, mude estratégia (modelo diferente, brief simplificado, edição manual).

## O hábito a internalizar

Antes de cada iteração, escreva o `Keep / Change / Do not` em texto curto. Mesmo que pra você mesmo num scratchpad. Esse hábito força a articular hipótese e proíbe a mudança caótica.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #16 (Image Prompting). Padrão de iteração.
- **OpenAI** — *Image generation guide* ([docs](https://platform.openai.com/docs/guides/images)). DALL-E Edit mode.
- **Black Forest Labs** — *FLUX.1 Tools* ([docs](https://docs.bfl.ai/)). Fill, Depth, Canny, Redux.
- **Midjourney** — *Documentation* ([docs](https://docs.midjourney.com/)). `--sref`, `--cref`.
- **Stability AI** — *ControlNet docs* ([docs](https://stability.ai/stable-image)). Controle estrutural.

## Veja também

- [[03-Dominios/Tecnologia/IA/Prompt Engineering/07 - Iteration patterns — keep, change, do-not]] — padrão original em texto, fonte do adaptado aqui
- [[05 - Templates por entregável — poster, infográfico, mockup, thumbnail]] — ponto de partida das iterações
- [[07 - Geração de diagramas e ilustrações técnicas]] — onde a iteração visual encontra limite real
