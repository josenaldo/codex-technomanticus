---
title: "Multimodal Prompting"
type: moc
publish: true
tags:
  - multimodal
  - prompt-engineering
  - ia
  - moc
created: 2026-05-28
updated: 2026-05-28
aliases:
  - Multimodal
  - Vision Prompting
---

# Multimodal Prompting

Em 2026, modelos de fronteira já são multimodais nativos — o gargalo é o engenheiro ainda dar só texto. Esta trilha cobre como fornecer imagens, PDFs, áudio, vídeo e dados estruturados pro modelo, e como **dirigir o tipo de leitura** que ele faz desses inputs. A tese central: enviar a modalidade certa, no nível de resolução certo, com a instrução de leitura certa, destrava casos que pipelines OCR/Whisper-pra-texto não resolvem — e custa menos no agregado, mesmo o token de imagem sendo mais caro.

> [!info] Pré-requisitos
> [[Anatomia dos LLMs/05 - Panorama de modelos 2026]] cobre quais famílias suportam o quê (Claude 4 family, GPT-5 family, Gemini 2.x) e dá vocabulário pra ler as notas seguintes sem cair em "Claude 4.5+" fantasma. Familiaridade básica com [[Prompt Engineering]] ajuda mas não é obrigatória.

> [!warning] Provider muda; modalidade nativa muda mais ainda
> Limites de tamanho, formatos aceitos e custo por imagem/página/segundo mudam quase a cada release. As notas trazem ordens de grandeza estáveis em 2026, mas a fonte de verdade pra deploy é o doc oficial do provider — sempre.

## Comece por aqui

Trilha sequencial recomendada — do porquê, passando pelas modalidades, até a técnica de dirigir a leitura e os limites.

### Bloco 1 — Por quê (1 nota)

Por que multimodal nativo bate pipeline OCR/Whisper + texto, e por que o anti-padrão "me dá só o texto" ainda é a regra em 2026.

- [[01 - O salto multimodal — por que isso importa]] — o salto entre "modelos que recebem texto" e "modelos que veem o documento"; casos que pipelines text-only não resolvem; o gargalo é hábito do engenheiro

### Bloco 2 — Por modalidade (4 notas)

Cada modalidade tem sua tabela de tokens, suas armadilhas e seu padrão de uso. SDK real Anthropic, OpenAI, Google em todas as notas.

- [[02 - Imagens como input — screenshots, charts, mockups]] — tipos de tarefa (descrição, extração, comparação, debug, classificação), tokenização por provider, code Python real
- [[03 - PDFs e documentos — extração e análise]] — PDF nativo (Claude, Gemini, OpenAI Files), estratégia página-a-página, híbrido com PageIndex
- [[04 - Áudio e vídeo — Whisper, Gemini Live e geração]] — transcrição barata vs input direto, voz em tempo real, vídeo nativo no Gemini
- [[05 - Tabelas e spreadsheets como input estruturado]] — três modos (texto, imagem, tool), pattern Pandas describe + sample, quando cada um ganha

### Bloco 3 — Técnica e controle (1 nota)

A técnica que mais muda output sem mudar input: dizer o tipo de leitura.

- [[06 - Como dizer ao modelo o tipo de leitura]] — descritiva, analítica, extrativa, comparativa, diagnóstica, avaliativa; template com Focus/Ignore/Output; pares before/after

### Bloco 4 — Limites (1 nota)

O lado feio: alucinação visual, OCR ruim em handwriting, leitura de cor capenga, raciocínio espacial fraco, custo e latência.

- [[07 - Limites e armadilhas multimodais]] — falhas concretas e quando voltar pra pipeline tradicional

## Leituras recomendadas

| Fonte | Tipo | Cobertura |
|-------|------|-----------|
| **@hooeem** — *Become an AI Engineer*, cap #17 | Thread / artigo | Espinha dorsal da trilha — todas as notas |
| **Anthropic** — *Vision* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/vision)) | Doc oficial | Notas 02, 03 — tokens por imagem, PDF nativo |
| **OpenAI** — *Vision guide* ([docs](https://platform.openai.com/docs/guides/vision)) | Doc oficial | Nota 02 — low/high detail, tile billing |
| **Google** — *Gemini API — Vision* ([docs](https://ai.google.dev/gemini-api/docs/vision)) | Doc oficial | Notas 02, 03, 04 — imagem, PDF, vídeo |
| **OpenAI** — *Whisper* ([docs](https://platform.openai.com/docs/guides/speech-to-text)) | Doc oficial | Nota 04 — transcrição barata como baseline |
| **Google** — *Gemini Live API* ([docs](https://ai.google.dev/gemini-api/docs/live)) | Doc oficial | Nota 04 — áudio/vídeo em tempo real |
| **Anthropic** — *PDF support* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support)) | Doc oficial | Nota 03 — PDF nativo Claude |

## Veja também

- [[Prompt Engineering]] — esta trilha estende prompt engineering pra modalidades além de texto
- [[AI Engineering Stack]] — multimodal é uma decisão de Input Layer e Context Layer
- [[Anatomia dos LLMs/05 - Panorama de modelos 2026]] — quais famílias suportam o quê
- [[RAG e Vector Databases/13 - PageIndex — RAG vectorless por árvore de documentos]] — combinação PageIndex (retrieval) + multimodal (leitura) cobre PDFs longos sem vector DB

## Todas as notas

```dataview
LIST
FROM "03-Dominios/IA/Multimodal Prompting"
WHERE type != "moc"
SORT file.name ASC
```
