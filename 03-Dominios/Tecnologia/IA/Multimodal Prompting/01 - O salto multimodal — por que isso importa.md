---
title: "01 - O salto multimodal — por que isso importa"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - multimodal
  - prompt-engineering
  - ia
publish: true
aliases:
  - Salto multimodal
  - Multimodal-native vs text-only
---

# 01 - O salto multimodal — por que isso importa

> [!abstract] TL;DR
> Em 2026, modelo de fronteira é multimodal nativo — Claude 4 (Opus, Sonnet, Haiku), GPT-5 e GPT-4.1, Gemini 2.x. O gargalo deixou de ser capacidade do modelo e virou hábito do engenheiro, que ainda monta pipeline OCR + extração + LLM-só-texto quando podia mandar a imagem direto. Multimodal nativo bate text-only em três frentes: não perde sinal na conversão (layout, hierarquia visual, gráficos, cor de status), encurta o pipeline (menos código, menos modos de falha) e desbloqueia casos onde a evidência **é** visual (acessibilidade, design review, debugging de UI, planilha com gráfico). Esta nota cobre o quê, por quê, e o anti-padrão "me dá só o texto" que ainda domina.

## O salto

Em 2026, "multimodal" deixou de ser feature premium. É default nos flagships:

- **Claude Opus 4.6, Sonnet 4.6, Haiku 4.5** — imagem nativa (até 100 imagens por chamada), PDF nativo (até ~100 páginas), sem áudio/vídeo nativos
- **GPT-5.4, GPT-4.1** — imagem nativa (low/high detail), áudio via Whisper ou GPT-4o Realtime, PDF via Files API
- **Gemini 3.1 Pro, Gemini 3 Flash** — imagem, áudio, vídeo e PDF nativos; vídeo até ~2h em algumas tiers
- **Open-weight** — Qwen 3.6-VL, Llama 4 multimodal variants

O que mudou em relação a 2023-2024 não foi só "agora vê imagem" — foi: vê imagem **no mesmo passe** do texto. Imagem entra como sequência de tokens visuais, intercalada com tokens de texto, no mesmo contexto. Sem etapa intermediária, sem OCR separado, sem "primeiro descreve depois pergunta".

## Por que multimodal-native bate pipeline text-only

Pipeline tradicional pra "perguntar coisas sobre uma página":

```
PDF → OCR (Tesseract / Textract / Unstructured)
    → Extração de tabela (Camelot / pdfplumber)
    → Concatenação em string
    → LLM (texto)
```

Pipeline multimodal-native:

```
PDF → LLM (multimodal)
```

A diferença não é só linhas de código. É **perda de sinal** em cada etapa do pipeline tradicional:

1. **Layout vira ruído.** OCR retorna texto linear; o modelo perde "esse número está numa caixa vermelha", "essa linha é o cabeçalho", "essa coluna alinha com aquela". Em planilha financeira, isso é a metade da informação.
2. **Hierarquia visual desaparece.** Título, subtítulo, callout, nota de rodapé — tudo vira texto plano. O modelo perde "isso é uma nota legal, não o corpo do contrato".
3. **Elementos não-textuais somem.** Gráficos, ícones, cores de status (verde/vermelho em dashboard), traços conectando caixas em diagrama — OCR não captura. O modelo decide com base em metade.
4. **Erros de OCR contaminam.** "Iva" virou "1va", "0" virou "O", "rn" virou "m". O modelo argumenta em cima de input quebrado e alucina pra fechar.

Multimodal-native pula essas perdas. O custo em token por imagem é maior, mas o pipeline encurta, os modos de falha diminuem, e os casos antes impossíveis viram triviais.

## Casos que multimodal nativo desbloqueia

Lista não-exaustiva — todos casos vistos em produção em 2025-2026:

### Design review e acessibilidade

Mockup do Figma como PNG → "Liste os problemas de acessibilidade: contraste, hierarquia de heading, alvos de toque pequenos, labels de form ausentes". O modelo vê o mockup como um humano veria, identifica contraste insuficiente em texto sobre fundo, percebe que o botão primário e secundário têm a mesma cor.

### Debugging de UI

Screenshot do bug → "O dropdown não fecha quando clico fora. Aqui está o estado quando abre. O que está errado no z-index ou na hierarquia de overlay?". O modelo vê que o dropdown está atrás de outro elemento, sugere fix.

### Planilha com gráfico

Print do Excel ou Google Sheets → "Esse gráfico mostra crescimento de 30% MoM. Mas o eixo Y começa em 1000, não em zero. Refaça a leitura assumindo eixo Y honesto". Modelo vê o gráfico, percebe a manipulação visual, recalcula. Pipeline OCR perderia o gráfico inteiro.

### Diagrama de arquitetura

Foto do whiteboard → "Esse é o desenho da nossa arquitetura. Liste os serviços, as conexões, e me diga quais setas não fecham o ciclo (componentes orfãos)". Modelo lê texto manuscrito + estrutura espacial das caixas + setas.

### Documento com formulário

PDF de form preenchido → "Extraia todos os campos preenchidos e seus valores". Sem OCR. Sem template específico. O modelo identifica que "Nome: ____" é label, "João" é valor.

### Code walkthrough em vídeo

Vídeo de 10min do dev mostrando bug no IDE → Gemini direto, sem transcrever áudio separado. Modelo vê o cursor, o erro, escuta a narração, conecta os dois.

## O anti-padrão "me dá só o texto"

Em 2026, ainda é comum ver:

```python
# Anti-padrão
text = ocr_pdf(path)
response = llm.invoke(f"Analise: {text}")
```

Em vez de:

```python
# Multimodal-native
response = llm.invoke([
    {"type": "image", "source": {"data": pdf_b64}},
    {"type": "text", "text": "Analise."}
])
```

Por que persiste:

1. **Hábito.** Pipeline antigo funciona "bem o bastante" pra casos simples. O dev nunca precisou voltar pra reavaliar.
2. **Stack travado em LangChain antigo.** Abstrações que assumem `str` como input do prompt.
3. **Crença de que "imagem é caro".** Token por imagem **é** mais caro que token de texto equivalente, mas o cálculo correto é por tarefa resolvida, não por token consumido. Pipeline OCR consome desenvolvimento, manutenção, erros silenciosos e retrabalho.
4. **Fear of unknown.** "Não sei direito quanto custa" — então fica no que sabe.

Quando o anti-padrão é defensável:

- **Documento puramente textual sem layout relevante.** Romance, artigo de blog em texto puro. OCR não perde nada porque não tinha nada visual.
- **Volume gigantesco com tolerância a erro.** Indexar 10 milhões de páginas pra busca. Custo por imagem torna-se proibitivo. Use OCR + retrieval, depois multimodal só pra páginas relevantes (ver [[03 - PDFs e documentos — extração e análise]]).
- **Compliance que exige cadeia de custódia textual.** Auditoria que precisa do `.txt` extraído como artefato separado.

Em todos os outros casos, em 2026, o default deveria ser multimodal-native.

## O custo de fazer errado

Cenário típico: imagine um time analisando extratos bancários PDF com pipeline OCR + LLM-só-texto. Acerto em valores tende a ficar na faixa de 70-85% — número que parece bom até alguém auditar. Migrar pra modelo multimodal-native (PDF nativo no Claude, Gemini ou OpenAI Files) costuma subir esse acerto pra 95%+, porque preserva contexto visual (caixas, alinhamento de colunas, posição de campo) que o OCR linear perdia. O token por documento sobe; o custo agregado (incluindo retrabalho manual em erro silencioso) tende a cair porque erro silencioso vira erro detectável — modelo às vezes responde "não consigo ler essa região" em vez de chutar.

A lição: medir custo por tarefa resolvida corretamente, não custo por token consumido.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #17 (Multimodal Prompting). Espinha dorsal da trilha.
- **Anthropic** — *Vision* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/vision)). Capabilities e limites do Claude.
- **OpenAI** — *Vision guide* ([docs](https://platform.openai.com/docs/guides/vision)). Como GPT-4o/5 leem imagem.
- **Google** — *Gemini API — Document understanding* ([docs](https://ai.google.dev/gemini-api/docs/document-processing)). Multimodal nativo no Gemini.

## Veja também

- [[02 - Imagens como input — screenshots, charts, mockups]] — a modalidade mais comum, com tokens por provider
- [[03 - PDFs e documentos — extração e análise]] — quando PDF nativo bate OCR
- [[06 - Como dizer ao modelo o tipo de leitura]] — multimodal sem instrução de leitura é desperdício
- [[07 - Limites e armadilhas multimodais]] — onde multimodal nativo falha
