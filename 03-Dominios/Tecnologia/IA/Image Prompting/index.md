---
title: "Image Prompting"
type: moc
publish: true
tags:
  - image-prompting
  - prompt-engineering
  - ia
  - moc
created: 2026-05-28
updated: 2026-05-28
aliases:
  - Geração de Imagens
  - Image Generation
---

# Image Prompting

Quando engenheiro gera imagem, o objetivo raramente é arte — é **entregável**: hero do README, thumbnail do post, mockup pra design review, infográfico pra deck, ilustração conceitual de arquitetura, asset de social media. Image Prompting é a disciplina de produzir esses entregáveis de forma reprodutível, com modelos como DALL-E, Imagen, Midjourney, FLUX, Stable Diffusion e Ideogram. A tese central da trilha: **deliverable-first, não scene-first** — descreva o entregável (formato, hierarquia, audiência, texto), não a cena. Image Prompting tem seu próprio ofício, separado de Prompt Engineering pra modelos de texto: canvas, composição, estilo e texto são as quatro alavancas, e cada entregável tem um template estável que vale a pena reaproveitar.

> [!info] Pré-requisitos
> Nenhum — esta trilha é auto-contida. Familiaridade com [[Prompt Engineering]] ajuda como mentalidade ("iteração disciplinada", "constraints declarativas"), mas todas as primitivas visuais são introduzidas aqui.

> [!warning] Modelos de imagem mudam mais rápido que LLMs
> Versões e capacidades de modelos de imagem (DALL-E 3, Imagen 3, Midjourney v6.1, FLUX.1, SD 3.5, Ideogram 2) refletem o estado de 2025-2026. Releases novos saem a cada poucos meses, com ganhos especialmente em renderização de texto e fidelidade. Doc oficial do provider é a fonte de verdade pra deploy.

## Comece por aqui

Trilha sequencial recomendada — mentalidade primeiro, depois ferramentas, depois técnica, depois casos técnicos.

### Bloco 1 — Mentalidade (2 notas)

A virada conceitual que faz a diferença entre "vê o que sai" e "entregável previsível".

- [[01 - Image prompting como engenharia]] — por que geração de imagem é engenharia quando o objetivo é entregável, não arte; casos de uso reais do dia do engenheiro
- [[02 - Deliverable-first, não scene-first]] — o erro mais comum (descrever cena) vs o padrão que funciona (descrever entregável); template canônico Goal / Deliverable / Canvas / Audience / Subject / Composition / Style / Text / Constraints / Iteration

### Bloco 2 — Ferramentas (1 nota)

O landscape de modelos em 2026 e quando escolher cada um.

- [[03 - Modelos de imagem 2026 — DALL-E, Imagen, Midjourney, FLUX, SD]] — tabela comparativa, decision tree por entregável, modos de edição

### Bloco 3 — Técnica (3 notas)

As quatro camadas do prompt visual, os templates por entregável e como iterar sem perder o controle.

- [[04 - Anatomia de um prompt visual — canvas, composição, estilo]] — canvas (formato), composição (hierarquia), estilo (linguagem visual), texto (e seus limites)
- [[05 - Templates por entregável — poster, infográfico, mockup, thumbnail]] — seis templates prontos com prompt completo e modelo recomendado
- [[06 - Iteração visual — controlled changes]] — Keep/Change/Do-not adaptado pra imagem, inpainting, image-to-image, ControlNet

### Bloco 4 — Casos técnicos (1 nota)

Onde geração de imagem funciona e onde ainda não — honesto sobre o estado de 2026.

- [[07 - Geração de diagramas e ilustrações técnicas]] — onde modelos de imagem ajudam em conteúdo técnico, onde Mermaid/Excalidraw/PlantUML ainda ganham, padrão híbrido

## Leituras recomendadas

| Fonte | Tipo | Cobertura |
|-------|------|-----------|
| **@hooeem** — *Become an AI Engineer*, cap #16 | Thread / artigo | Espinha dorsal da trilha — todas as notas |
| **OpenAI** — *Image generation guide* ([docs](https://platform.openai.com/docs/guides/images)) | Doc oficial | Notas 03, 04 — DALL-E 3, edit mode |
| **Midjourney** — *Documentation* ([docs](https://docs.midjourney.com/)) | Doc oficial | Notas 03, 04 — parâmetros, estilos, aspect ratio |
| **Black Forest Labs** — *FLUX.1 docs* ([docs](https://docs.bfl.ai/)) | Doc oficial | Notas 03, 06 — FLUX pro/dev/schnell, fill/inpaint |
| **Stability AI** — *Stable Diffusion 3.5* ([docs](https://stability.ai/stable-image)) | Doc oficial | Nota 03 — SD self-hosted, LoRAs, ControlNet |
| **Google** — *Imagen on Vertex AI* ([docs](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview)) | Doc oficial | Notas 03, 04 — Imagen 3, text rendering |
| **Ideogram** — *Docs* ([docs](https://docs.ideogram.ai/)) | Doc oficial | Nota 04 — texto em imagem como especialidade |

## Veja também

- [[Prompt Engineering]] — mentalidade comum: iteração disciplinada, constraints, especificidade
- [[Multimodal Prompting]] — input visual no LLM; complementa esta trilha (que cobre output visual)
- [[AI Engineering Stack]] — image generation é uma decisão de Output Layer
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/05 - Output Layer]] — onde image generation se encaixa no stack
