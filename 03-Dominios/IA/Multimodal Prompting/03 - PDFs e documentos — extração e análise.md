---
title: "03 - PDFs e documentos — extração e análise"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - multimodal
  - prompt-engineering
  - ia
  - pdf
publish: true
aliases:
  - PDF multimodal
  - Document understanding
---

# 03 - PDFs e documentos — extração e análise

> [!abstract] TL;DR
> Em 2026, três caminhos cobrem PDF: nativo (Claude, Gemini, OpenAI Files), página-a-página como imagem, e híbrido (PageIndex pra escolher páginas + multimodal pra ler). PDF nativo trata o documento como sequência de páginas-imagem + texto extraído internamente — o modelo vê layout, gráfico, tabela e texto no mesmo passo. Funciona bem até ~100 páginas (Claude) ou docs muito grandes (Gemini). Acima disso, PageIndex como retrieval ([[RAG e Vector Databases/13 - PageIndex — RAG vectorless por árvore de documentos]]) escolhe páginas relevantes e o LLM multimodal lê só essas. OCR + texto puro segue válido pra docs sem layout relevante, mas perdeu o trono como default.

## Três caminhos

### Caminho 1 — PDF nativo

O provider trata o PDF como input nativo. Você manda os bytes do PDF, o modelo vê página por página com layout e texto preservados, e você não escreve nada além do prompt.

- **Anthropic Claude** — até **100 páginas** ou 32 MB por chamada, na família Claude 4.x (Opus 4.6, Sonnet 4.6, Haiku 4.5). Cada página vira ~1500-2000 tokens (combinação de imagem + texto extraído internamente). Suporta base64 e URL.
- **Google Gemini** — suporta PDFs muito grandes (até centenas de páginas em Gemini 2.x Pro). Tokenização por página similar a uma imagem (~258 tokens) + texto extraído.
- **OpenAI** — via **Files API** (upload e referencia por `file_id`) ou Assistants/Responses API. PDF é convertido internamente em imagens + texto.

### Caminho 2 — Página-a-página como imagem

Quando o PDF é pequeno (1-3 páginas) ou você só precisa de uma página específica, mande como imagem. Já está coberto na [[02 - Imagens como input — screenshots, charts, mockups]]. Vantagem: zero dependência de feature "PDF nativo"; funciona em qualquer modelo vision. Desvantagem: você renderiza o PDF (PyMuPDF, pdf2image), gerencia bytes, calcula custo manualmente.

### Caminho 3 — Híbrido (PageIndex + multimodal)

Pra documento longo (>100 páginas) onde só algumas páginas importam:

1. Gerar árvore PageIndex do documento (sumário enriquecido com intervalos de página).
2. LLM navega a árvore por raciocínio, identifica as N páginas relevantes pra query.
3. Renderiza só essas páginas como imagem, manda em chamada multimodal.

Cobre PDFs financeiros, jurídicos, regulatórios e livros sem comprar vector DB. Ver [[RAG e Vector Databases/13 - PageIndex — RAG vectorless por árvore de documentos]] pro pipeline completo de retrieval; aqui o foco é o passo final de leitura multimodal.

## Code — Claude com PDF nativo

```python
import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

pdf_bytes = Path("contrato.pdf").read_bytes()
pdf_b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_b64,
                },
            },
            {
                "type": "text",
                "text": (
                    "Extraia em JSON: partes contratantes, vigência (datas de "
                    "início e fim), valor total, cláusulas de rescisão. Cite a "
                    "página de cada campo."
                ),
            },
        ],
    }],
)

print(response.content[0].text)
print(f"Tokens: {response.usage.input_tokens} in / {response.usage.output_tokens} out")
```

Para URL pública, troque o bloco `source` por `{"type": "url", "url": "https://..."}`. Claude faz fetch e processa.

## Code — Gemini com PDF nativo

```python
from google import genai
from google.genai import types
from pathlib import Path

client = genai.Client()

# Upload via Files API (recomendado para PDFs grandes ou reutilizáveis)
file = client.files.upload(file="contrato.pdf")

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
        file,
        (
            "Extraia em JSON: partes contratantes, vigência, valor total, "
            "cláusulas de rescisão. Cite a página de cada campo."
        ),
    ],
)

print(response.text)
print(f"Tokens: {response.usage_metadata.prompt_token_count} in")
```

Para PDFs pequenos (<20 MB), inline também funciona:

```python
pdf_bytes = Path("contrato.pdf").read_bytes()

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
        types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
        "Extraia...",
    ],
)
```

## Code — OpenAI via Files API

```python
from openai import OpenAI

client = OpenAI()

# Upload do PDF
file = client.files.create(
    file=open("contrato.pdf", "rb"),
    purpose="user_data",
)

response = client.responses.create(
    model="gpt-5",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_file", "file_id": file.id},
            {
                "type": "input_text",
                "text": (
                    "Extraia em JSON: partes contratantes, vigência, valor "
                    "total, cláusulas de rescisão. Cite a página."
                ),
            },
        ],
    }],
)

print(response.output_text)
```

A API Responses (sucessora do Chat Completions pra usos multimodais complexos) trata `input_file` de forma nativa.

## Quando cada caminho ganha

| Cenário | Recomendado |
|---|---|
| Contrato de 20 páginas, extração de campos | PDF nativo (Claude ou Gemini) |
| Relatório financeiro de 200 páginas, perguntas pontuais | PageIndex + multimodal nas páginas relevantes |
| Página de form preenchida (1 página) | Página como imagem |
| Indexar 50k PDFs para busca | OCR + texto + vector DB (depois multimodal só nas top-K) |
| PDF com handwriting | Multimodal nativo (OCR tradicional perde) |
| PDF puramente textual (e-book sem layout) | OCR + texto puro (mais barato, sem perda) |

## Estratégia página-a-página para documentos grandes

Quando você ultrapassa o limite de PDF nativo (>100 páginas em Claude, doc gigante em Gemini), divida:

```python
import fitz  # PyMuPDF

doc = fitz.open("livro.pdf")
chunks = []
chunk_size = 20  # páginas por chunk

for i in range(0, len(doc), chunk_size):
    sub = fitz.open()
    sub.insert_pdf(doc, from_page=i, to_page=min(i + chunk_size - 1, len(doc) - 1))
    pdf_bytes = sub.tobytes()
    chunks.append(pdf_bytes)

# Cada chunk vai como uma chamada Claude separada
# Resultados consolidados depois
```

Cuidado: se a informação atravessa fronteira de chunk (uma tabela divide entre página 20 e 21), perde contexto. Solução: chunks com overlap (último página do chunk anterior repete no próximo).

## Quando página-como-imagem bate PDF-nativo

Cenários onde renderizar a página em PNG e mandar como imagem é melhor que PDF nativo:

- **Modelo só tem vision, não suporta PDF.** Modelos open-weight, modelos antigos.
- **Só preciso de UMA página específica.** Não faz sentido subir o PDF inteiro.
- **Quero controle de resolução fina.** PDF nativo decide a renderização internamente; imagem permite escolher DPI exato.
- **Compliance ou debug.** Quero ver o que o modelo "viu" — a imagem renderizada é evidência.

Renderização com PyMuPDF:

```python
import fitz

doc = fitz.open("contrato.pdf")
page = doc[7]  # página 8
pix = page.get_pixmap(dpi=200)  # 200 DPI é bom para texto
pix.save("page_8.png")
```

Depois manda `page_8.png` como imagem (ver [[02 - Imagens como input — screenshots, charts, mockups]]).

## Boas práticas

- **Use PDF nativo como default em 2026.** OCR + texto puro só pra casos onde layout não importa.
- **Cite a página no prompt.** "Cite a página de cada campo extraído" — força o modelo a usar a referência espacial, reduz alucinação.
- **Pra docs gigantes, retrieval primeiro.** PageIndex ou hierarchical chunking pra escolher páginas; multimodal pra ler.
- **Não compare PDF nativo vs OCR no benchmark errado.** Acerto de extração de tabela formatada: nativo ganha. Acerto de texto corrido: empate. Custo: OCR ganha. Tempo de dev: nativo ganha por largo.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #17.
- **Anthropic** — *PDF support* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support)). Limites e tokenização.
- **Google** — *Gemini API — Document understanding* ([docs](https://ai.google.dev/gemini-api/docs/document-processing)).
- **OpenAI** — *Files API* ([docs](https://platform.openai.com/docs/api-reference/files)). Upload e referência por `file_id`.
- **PyMuPDF (fitz)** — biblioteca padrão pra render/cortar PDF em Python.

## Veja também

- [[02 - Imagens como input — screenshots, charts, mockups]] — quando mandar página renderizada como imagem
- [[RAG e Vector Databases/13 - PageIndex — RAG vectorless por árvore de documentos]] — retrieval estrutural pra documentos grandes
- [[05 - Tabelas e spreadsheets como input estruturado]] — tabela dentro de PDF tem caminhos próprios
- [[06 - Como dizer ao modelo o tipo de leitura]] — "extraia X" vs "analise Y" mudam o output do mesmo PDF
- [[07 - Limites e armadilhas multimodais]] — onde leitura de PDF falha
