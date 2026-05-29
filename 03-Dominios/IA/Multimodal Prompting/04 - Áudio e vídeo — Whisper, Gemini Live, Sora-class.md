---
title: "04 - Áudio e vídeo — Whisper, Gemini Live, Sora-class"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - multimodal
  - prompt-engineering
  - ia
  - audio
  - video
publish: true
aliases:
  - Audio prompting
  - Video prompting
  - Whisper
  - Gemini Live
---

# 04 - Áudio e vídeo — Whisper, Gemini Live, Sora-class

> [!abstract] TL;DR
> Áudio tem dois caminhos: transcrever com Whisper (barato, robusto, é o baseline padrão pra podcast/reunião) ou enviar direto pro modelo multimodal (Gemini Pro, GPT-4o, Claude voice — mais caro, preserva entonação e contexto sonoro). Vídeo é dominado pelo Gemini (até ~2h em alguns tiers, frames + áudio integrados). Geração de vídeo (Sora-class) sai do escopo desta nota mas é citada porque muda o que faz sentido transcrever. Tempo real (voz/vídeo bidirecional) usa APIs separadas: Gemini Live, GPT-4o Realtime, Claude voice mode. Use cases: resumo de reunião, Q&A em podcast, análise de code walkthrough, tutorial review.

## Áudio — dois caminhos

### Caminho 1 — Whisper como baseline

Whisper (OpenAI) é o tokenizador de áudio do mercado em 2026: barato, robusto a sotaque e ruído, multilíngue (~100 idiomas). Continua sendo o default pra:

- Transcrição de podcast / reunião / webinar
- Subtitulagem
- Pipeline batch onde você só quer o texto

Preço típico (2026): ~$0.006 por minuto. Para uma reunião de 1h, ~$0.36. Modelos open-weight (Whisper-large-v3, distil-whisper) rodam local de graça.

```python
from openai import OpenAI

client = OpenAI()

with open("reuniao.mp3", "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        language="pt",
        response_format="verbose_json",   # inclui timestamps
        timestamp_granularities=["segment"],
    )

print(transcript.text)
for seg in transcript.segments:
    print(f"[{seg.start:.1f}s] {seg.text}")
```

`verbose_json` com `timestamp_granularities=["segment"]` ou `["word"]` retorna timestamps — essenciais pra "qual minuto fulano falou X".

Pipeline típico: Whisper transcreve → LLM texto (Claude/GPT/Gemini) resume, extrai action items, gera Q&A.

### Caminho 2 — Áudio direto no modelo

Modelos multimodais aceitam áudio como input nativo. Diferença pra Whisper + texto: o modelo "escuta" — não só lê a transcrição. Captura entonação, hesitação, sobreposição de vozes, sons de fundo.

- **Gemini 2.x Pro / Flash** — áudio até ~8h em alguns tiers; cobra ~32 tokens por segundo (Pro) ou menos em Flash.
- **GPT-4o** — áudio nativo via Realtime API ou chat completions com input de áudio.
- **Claude voice (Anthropic)** — modo de voz lançado em 2025/2026; menos exposto via API pública, mais em produtos Anthropic.

Quando faz sentido pular Whisper:

- Pergunta exige tom/emoção (entrevista de UX, análise de pitch comercial).
- Áudio curto (<10min) onde a sobrecarga de transcrever + chamar texto não compensa.
- Multilíngue com troca de idioma no meio (Whisper às vezes erra a virada).

Quando Whisper segue ganhando:

- Volume grande (podcasts em massa, archive).
- Precisão de transcrição importa mais que análise (subtitulagem).
- Pipeline offline ou self-hosted (custo zero com Whisper local).

### Code — Gemini com áudio direto

```python
from google import genai
from google.genai import types
from pathlib import Path

client = genai.Client()

# Upload via Files API para áudios maiores
audio_file = client.files.upload(file="podcast.mp3")

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
        audio_file,
        (
            "Este é um episódio de podcast sobre arquitetura de software. "
            "Liste os 5 principais argumentos do convidado e, para cada um, "
            "indique se ele defendeu com convicção ou com hesitação. "
            "Cite o minuto de cada argumento."
        ),
    ],
)

print(response.text)
```

O modelo escuta tom de voz, hesitação, pausas — sinais que a transcrição textual perderia.

## Tempo real — voz e vídeo bidirecionais

Pra casos onde latência <300ms é requisito (assistente de voz, tutor que conversa, copiloto que ouve enquanto você fala):

- **Gemini Live API** — WebSocket bidirecional, áudio e vídeo combinados, vozes nativas.
- **OpenAI Realtime API** — sucessor do "assistant voice", WebSocket, integração com tools em tempo real.
- **Anthropic voice mode** — disponível em produtos Claude.

Esses não substituem Whisper + LLM em pipeline batch — são pra UX conversacional. Custo por minuto é significativamente maior que Whisper + chamada de texto.

Esqueleto Gemini Live (Python):

```python
from google import genai
import asyncio

client = genai.Client()

async def main():
    async with client.aio.live.connect(
        model="gemini-2.5-flash-live",
        config={"response_modalities": ["AUDIO"]},
    ) as session:
        # Envia áudio do mic em chunks
        await session.send_realtime_input(audio=mic_chunk)
        # Recebe áudio de volta em streaming
        async for response in session.receive():
            if response.data:
                play(response.data)

asyncio.run(main())
```

Detalhes de captura de mic e playback ficam fora — varia por plataforma.

## Vídeo — Gemini como referência

Gemini é o player dominante em vídeo de input em 2026:

- **Gemini 2.x Pro** — até ~2h de vídeo em alguns tiers, processado como frames + áudio.
- **Gemini 2.x Flash** — vídeos menores, mais rápido.

Tokenização: ~258 tokens por frame (Gemini extrai ~1 frame por segundo por default) + áudio. Vídeo de 10 minutos ≈ 600 frames ≈ 155k tokens.

```python
from google import genai
from google.genai import types

client = genai.Client()

video_file = client.files.upload(file="tutorial.mp4")

# Aguardar processamento (vídeo demora a indexar)
import time
while video_file.state == "PROCESSING":
    time.sleep(2)
    video_file = client.files.get(name=video_file.name)

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
        video_file,
        (
            "Este é um tutorial de Vim. Liste os comandos demonstrados, "
            "na ordem em que aparecem, com o timestamp de cada um. "
            "Se o instrutor mostra um comando mas não explica, marque [não explicado]."
        ),
    ],
)

print(response.text)
```

Para vídeo curto (<20 MB), `Part.from_bytes(data=video_bytes, mime_type="video/mp4")` inline também funciona.

OpenAI e Anthropic, em 2026, dependem de extração de frames externa (você extrai N frames com ffmpeg, manda como sequência de imagens). É possível, mas perde sincronia com áudio.

## Sora-class e geração de vídeo

Modelos como Sora (OpenAI), Veo (Google), Runway Gen-3 e Pika geram vídeo a partir de texto ou imagem. Fora do escopo desta nota (esta trilha é sobre **input**), mas afeta as decisões aqui:

- Vídeo gerado precisa de QA — você manda o vídeo de volta pra um modelo multimodal pra avaliar fidelidade ao prompt, artifacts, consistência temporal.
- Edição assistida — modelo lê o vídeo gerado e sugere ajustes textuais pra próxima rodada.

## Use cases comuns

### Resumo de reunião

Pipeline padrão: Zoom → MP3 → Whisper (`verbose_json`) → Claude/GPT com transcrição + timestamps → action items por participante. Custo ~$0.50 por reunião de 1h.

### Q&A em podcast

Whisper transcreve, modelo texto responde com citação de timestamp. Pra podcast onde tom importa (entrevistas, debate), Gemini áudio direto.

### Análise de code walkthrough

Vídeo de dev no IDE narrando bug → Gemini lê tela + áudio, identifica linha do bug, sugere fix. Pipeline texto sozinho perderia o que está sendo apontado visualmente.

### Tutorial review

Vídeo educacional → Gemini lista os tópicos cobertos, conceitos não explicados, ordem didática. Útil pra curadoria de conteúdo.

### Suporte por voz

Realtime API (OpenAI ou Gemini Live) com tools integradas — usuário fala, modelo escuta, chama API interna, responde por voz.

## Limites e custos

| Modalidade | Provider | Limite típico | Custo de input |
|---|---|---|---|
| Áudio | Whisper | sem limite (chunked) | ~$0.006/min |
| Áudio | Gemini 2.x Pro | ~8h por arquivo | ~32 tokens/s |
| Áudio | GPT-4o (realtime) | streaming | ~$100/1M tokens áudio in |
| Vídeo | Gemini 2.x Pro | ~2h | ~258 tokens/frame + áudio |
| Vídeo | Gemini 2.x Flash | menor | barato |
| Vídeo bidirecional | Gemini Live | streaming | tier-específico |

Esses números mudam frequentemente. Confira o doc do provider antes de bater orçamento.

## Boas práticas

- **Use Whisper como baseline.** Só pule pra áudio direto se a tarefa exige tom/contexto sonoro.
- **Peça timestamps no prompt.** "Cite o minuto/segundo" — sem isso o modelo invoca "no início" / "no final".
- **Pré-corte vídeo longo.** Mande só os 10min relevantes em vez do vídeo inteiro de 1h.
- **Áudio em mono, 16kHz pra Whisper.** Estéreo e 48kHz não dão ganho de acurácia, dobram o tamanho.
- **Cache de upload (Files API).** Reuse o mesmo `file_id` em múltiplas perguntas sobre o mesmo arquivo.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #17.
- **OpenAI** — *Whisper / speech-to-text* ([docs](https://platform.openai.com/docs/guides/speech-to-text)). Modelos, formatos, timestamps.
- **OpenAI** — *Realtime API* ([docs](https://platform.openai.com/docs/guides/realtime)). Voz bidirecional.
- **Google** — *Gemini API — Audio* ([docs](https://ai.google.dev/gemini-api/docs/audio)). Tokenização e limites.
- **Google** — *Gemini API — Video* ([docs](https://ai.google.dev/gemini-api/docs/vision#video)). Frame rate, duração.
- **Google** — *Live API* ([docs](https://ai.google.dev/gemini-api/docs/live)). Streaming bidirecional.

## Veja também

- [[02 - Imagens como input — screenshots, charts, mockups]] — frames de vídeo são imagens
- [[03 - PDFs e documentos — extração e análise]] — PDF é outro doc longo com lógica análoga
- [[06 - Como dizer ao modelo o tipo de leitura]] — "transcreva" vs "resuma" vs "extraia action items" muda muito
- [[07 - Limites e armadilhas multimodais]] — onde transcrição e leitura de vídeo falham
