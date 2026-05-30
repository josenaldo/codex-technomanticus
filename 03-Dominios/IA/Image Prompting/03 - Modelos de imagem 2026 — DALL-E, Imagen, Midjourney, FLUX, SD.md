---
title: "03 - Modelos de imagem 2026 — DALL-E, Imagen, Midjourney, FLUX, SD"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - image-prompting
  - prompt-engineering
  - ia
  - models
publish: true
aliases:
  - Modelos de imagem 2026
  - Image model landscape
---

# 03 - Modelos de imagem 2026 — DALL-E, Imagen, Midjourney, FLUX, SD

> [!abstract] TL;DR
> Em 2026, seis modelos cobrem 90% dos casos práticos: **DALL-E 3** (OpenAI, integrado com ChatGPT, segue instrução bem), **Imagen 3** (Google, photorealismo + texto), **Midjourney v6.1** (assinatura mensal, qualidade artística, estilo consistente), **FLUX.1** (Black Forest Labs, pro fechado + dev/schnell open-source com qualidade próxima da MJ), **Stable Diffusion 3.5** (Stability AI, open-source, ecossistema de LoRAs e ControlNet) e **Ideogram 2** (especialista em texto-na-imagem). Cada um tem ponto forte e fraco; decisão por entregável segue regra simples (poster com texto → Ideogram/Imagen, photorealístico → DALL-E/Imagen, artístico → Midjourney, OSS self-host → FLUX/SD). Releases novos saem rápido — fonte de verdade pra deploy é doc oficial.

> [!warning] Estado 2025-2026, sujeito a mudança
> Esta nota reflete o landscape de fim de 2025 / início de 2026 — Midjourney v6.1 atual com v7 rumored, Imagen 3 atual, FLUX.1 família estável. Provider lança versão nova a cada poucos meses. Antes de deploy, valide capabilities atuais no doc oficial.

## Tabela comparativa

| Modelo | Provider | Open weights | Custo | Best for | Worst at | Notas |
|--------|----------|--------------|-------|----------|----------|-------|
| **DALL-E 3** | OpenAI | Fechado | API por imagem (~$0.04-0.08 standard/HD) | Segue instruções específicas, texto razoável, integração com ChatGPT | Photorealismo extremo, estilo artístico consistente | Disponível via API e ChatGPT; bom default pra quem está em fluxo OpenAI |
| **Imagen 3** | Google | Fechado | API por imagem via Vertex AI | Photorealismo, renderização de texto, qualidade fotográfica | Estilos artísticos exóticos | Acessível via Gemini API e Vertex AI; alguns modos exigem allowlist |
| **Midjourney v6.1** | Midjourney | Fechado | Assinatura ($10-120/mês) | Qualidade artística, estilo consistente via `--sref`, controle fino | API oficial limitada (Discord-first, web app maduro) | Padrão de fato pra trabalho artístico/branded; v7 rumored mas tratá-lo como especulativo |
| **FLUX.1 [pro]** | Black Forest Labs | Fechado | API (~$0.05/imagem) | Qualidade próxima da MJ, prompt adherence forte | Estilo artístico distintivo da MJ | Top-tier comercial open-ish; via fal.ai, Replicate, BFL API |
| **FLUX.1 [dev]** | Black Forest Labs | **Aberto** (non-commercial) | Self-host (compute próprio) ou ~$0.02-0.03 hosted | Customização via LoRA, controle, OSS responsável | Photorealismo extremo | Pode rodar em GPU consumer (24GB VRAM ideal); base pra fine-tunes |
| **FLUX.1 [schnell]** | Black Forest Labs | **Aberto** (Apache 2.0) | Self-host barato ou ~$0.003/imagem | Velocidade (4 steps), iteração rápida, comercial | Qualidade abaixo de dev/pro | Boa pra prototipagem em volume |
| **Stable Diffusion 3.5 Large** | Stability AI | **Aberto** | Self-host (compute) ou hosted | Customização extrema (LoRAs, ControlNet, IP-Adapter), comunidade enorme | Qualidade base abaixo de FLUX dev | Padrão de fato pra OSS; ecossistema vasto em Civitai/HuggingFace |
| **Ideogram 2** | Ideogram | Fechado | Web app + API | **Texto-na-imagem** (posters, signs, letras corretas) | Imagens sem texto (não é vantagem) | Especialista; ideal pra poster, infográfico, asset com tipografia |

## Forças e fraquezas por modelo

### DALL-E 3 (OpenAI)
**Forte:** segue instruções específicas literalmente — "logo no canto superior direito, texto centralizado no meio, paleta dark mode" funciona melhor que na média. Texto razoável. Integração com ChatGPT facilita iteração conversacional. Edit mode (inpainting) integrado.
**Fraco:** photorealismo extremo (vence Imagen). Estilo artístico marcante (vence Midjourney). Aspect ratios limitados (1:1, 16:9, 9:16, sem 4:5 nativo em alguns endpoints).

### Imagen 3 (Google)
**Forte:** photorealismo e fidelidade fotográfica. Renderização de texto está entre as melhores. Acesso via Vertex AI permite uso enterprise com SLA.
**Fraco:** estilos artísticos não-fotográficos saem mais genéricos. Filtros de segurança agressivos podem bloquear prompts inofensivos. Disponibilidade regional irregular.

### Midjourney v6.1
**Forte:** qualidade artística que vira marca registrada. `--sref <url>` e `--cref` permitem consistência de estilo e personagem entre gerações. Comunidade enorme com prompts/estilos compartilháveis. Controle fino (`--ar`, `--stylize`, `--chaos`, `--weird`).
**Fraco:** API oficial limitada — uso em pipeline automatizado historicamente passou por Discord bots ou terceiros não-oficiais. Texto na imagem é fraco (melhorou em v6 mas ainda atrás de Ideogram). Assinatura mensal, não pay-per-use.

### FLUX.1 [pro/dev/schnell]
**Forte:** prompt adherence (segue instrução) considerada melhor que MJ em muitos benchmarks. Versão `[dev]` é aberta (non-commercial) e roda em GPU consumer com VRAM razoável. Schnell é a versão rápida (4 steps) pra iteração. Já existe modo edição (FLUX.1 Tools — Fill/Depth/Canny/Redux).
**Fraco:** estilo artístico distintivo da MJ não está aí. Texto em imagem melhorou mas ainda inferior a Ideogram. Documentação oficial ainda em maturação.

### Stable Diffusion 3.5
**Forte:** ecossistema. LoRAs pra praticamente qualquer estilo. ControlNet pra controle de pose/edge/depth. IP-Adapter pra reference image. Ferramentas como Automatic1111, ComfyUI, InvokeAI dão controle granular. Comunidade Civitai.
**Fraco:** qualidade base sem fine-tunes está atrás de FLUX dev. Curva de aprendizado alta (modelos, samplers, schedulers, CFG, LoRAs). Para hosted hands-off, não é o default — vai pra FLUX ou Imagen.

### Ideogram 2
**Forte:** texto na imagem é o caso de uso. Posters, signs, lettering, infográficos com tipografia legível. Em 2026, ainda lidera essa subcategoria com Imagen 4 (quando disponível) e FLUX dev encostando.
**Fraco:** fora do caso "texto na imagem", é mediano. Não é escolha pra hero artístico ou mockup fotorealista.

## Decision tree por entregável

Atalho mental pra decidir, mesmo sem benchmark próprio:

```
Tem texto crítico na imagem (poster, infográfico, signage)?
├── Sim
│   ├── Volume alto, automação?    → Imagen 3 (Vertex) ou FLUX dev
│   └── One-off, qualidade máxima? → Ideogram 2
│
└── Não
    │
    ├── Photorealismo (mockup, capa fotográfica, produto)?
    │   ├── Closed ok                → Imagen 3 ou DALL-E 3
    │   └── Self-host                → FLUX dev (com LoRA realístico) ou SD 3.5
    │
    ├── Artístico distintivo (hero blog, capa de podcast, ilustração de marca)?
    │   ├── Assinatura ok            → Midjourney v6.1
    │   └── OSS / pipeline           → FLUX dev (qualidade próxima)
    │
    ├── Pipeline automatizado em volume (geração programática)?
    │   ├── Custo importa            → FLUX schnell ou SD 3.5
    │   └── Qualidade importa        → FLUX pro
    │
    └── Mockup conceitual rápido (design review, brainstorm)?
        └── DALL-E 3 (via ChatGPT, iteração conversacional)
```

## Modos de edição: além do "text-to-image"

Geração from-scratch é só uma feature; produção real usa muito edição:

- **Inpaint (mask + new content):** pinte máscara sobre região, peça novo conteúdo só ali. DALL-E (Edit mode), FLUX.1 Fill, SD Inpaint via ControlNet.
- **Outpaint (expand canvas):** estende borda da imagem. DALL-E Edit, FLUX, SD.
- **Image-to-image (i2i):** imagem base + prompt → variação. Praticamente todos os modelos.
- **ControlNet (SD/FLUX):** controla pose, edge, depth, segmentação. Forte na pipeline de produção, especialmente pra mockups com layout exato.
- **Reference image (`--cref` em MJ, IP-Adapter em SD, Redux em FLUX):** preserva personagem ou estilo entre gerações.

Modos de edição merecem nota própria; nota [[06 - Iteração visual — controlled changes]] cobre o essencial pra controle de iteração.

## Fontes

- **OpenAI** — *Image generation guide* ([docs](https://platform.openai.com/docs/guides/images)). DALL-E 3 capabilities e edit mode.
- **Google** — *Imagen on Vertex AI* ([docs](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview)). Imagen 3 e text rendering.
- **Midjourney** — *Documentation* ([docs](https://docs.midjourney.com/)). Parâmetros, `--sref`, `--cref`, `--ar`.
- **Black Forest Labs** — *FLUX.1 docs* ([docs](https://docs.bfl.ai/)). FLUX família pro/dev/schnell e FLUX.1 Tools.
- **Stability AI** — *Stable Diffusion 3.5* ([docs](https://stability.ai/stable-image)). SD 3.5 Large/Medium.
- **Ideogram** — *Docs* ([docs](https://docs.ideogram.ai/)). Texto-na-imagem.

## Veja também

- [[02 - Deliverable-first, não scene-first]] — decisão de modelo segue decisão de entregável
- [[04 - Anatomia de um prompt visual — canvas, composição, estilo]] — vocabulário comum aos modelos
- [[05 - Templates por entregável — poster, infográfico, mockup, thumbnail]] — modelo recomendado por entregável
- [[06 - Iteração visual — controlled changes]] — inpainting, image-to-image, ControlNet
