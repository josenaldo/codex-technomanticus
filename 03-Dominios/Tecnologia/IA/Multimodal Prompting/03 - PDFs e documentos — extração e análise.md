---
title: "03 - PDFs e documentos — extração e análise"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: iniciado
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
> Em 2026, três caminhos cobrem PDF: nativo (Claude, Gemini, OpenAI Files), página-a-página como imagem, e híbrido (PageIndex pra escolher páginas + multimodal pra ler). PDF nativo trata o documento como sequência de páginas-imagem + texto extraído internamente — o modelo vê layout, gráfico, tabela e texto no mesmo passo. Funciona bem até ~100 páginas (Claude) ou docs muito grandes (Gemini). Acima disso, PageIndex como retrieval ([[03-Dominios/Tecnologia/IA/RAG e Vector Databases/13 - PageIndex — RAG vectorless por árvore de documentos]]) escolhe páginas relevantes e o LLM multimodal lê só essas. OCR + texto puro segue válido pra docs sem layout relevante, mas perdeu o trono como default.

> [!question]- Qual a diferença real entre mandar o PDF nativo vs converter cada página em PNG e mandar como imagem?
> Resultado final tende a ser muito similar pra documentos com texto digital limpo, porque internamente o provider converte o PDF em imagens de qualquer forma. A diferença prática está em três pontos: (1) conveniência — PDF nativo não exige código de renderização (PyMuPDF, pdf2image); (2) custo de token por página — PDF nativo em Claude tem custo fixo ~1500-2000 tokens/página que pode ser menor ou maior que a imagem equivalente dependendo do DPI; (3) controle — renderizando você escolhe DPI (200 costuma ser bom pra texto), cropping exato, e tem a imagem como artefato auditável. Para documentos com handwriting, PDF nativo tende a ser melhor porque o provider pode usar texto interno extraído como âncora. Para debug e compliance, imagem renderizada é preferível porque você vê exatamente o que o modelo recebeu.

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

Cobre PDFs financeiros, jurídicos, regulatórios e livros sem comprar vector DB. Ver [[03-Dominios/Tecnologia/IA/RAG e Vector Databases/13 - PageIndex — RAG vectorless por árvore de documentos]] pro pipeline completo de retrieval; aqui o foco é o passo final de leitura multimodal.

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

**Estrutura de prompt recomendada pra extração de documento:**

```
Você está analisando [tipo do documento: contrato, extrato, NF, laudo].

Extraia os seguintes campos em JSON:
- [campo_1]: [descrição de o que é e como identificar]
- [campo_2]: ...

Regras:
- Se um campo não aparecer no documento, retorne null.
- Para cada campo encontrado, inclua "pagina": N indicando a página de origem.
- Se um valor for ilegível, retorne "ilegivel" (não adivinhe).
- Não invente campos não listados.
```

Esse template — tipo do doc explícito + campos descritos + null como opção + citação de página + proibição de invenção — cobre as principais fontes de erro de extração em documento.

**Cache de arquivo pra múltiplas queries no mesmo PDF:**

Quando você vai fazer várias perguntas diferentes sobre o mesmo documento (ex: primeiro extrai campos, depois verifica compliance, depois gera resumo), re-enviar o PDF inteiro em cada chamada é caro. Prefer:
- **Anthropic prompt caching** — adiciona `cache_control: {"type": "ephemeral"}` ao bloco `document`; o PDF fica em cache por 5 minutos na camada ephemeral.
- **Gemini Files API** — faça upload uma vez, reutilize o `file.uri` em múltiplas chamadas sem re-subir os bytes.

## Armadilhas comuns

> [!warning] Mandar o PDF inteiro quando só uma página importa — custo e latência desnecessários
> PDF nativo em Claude custa ~1500-2000 tokens por página. Um relatório de 200 páginas onde a pergunta é sobre a página 47 custa ~300-400k tokens de input para ler o doc inteiro — caro e lento. O padrão certo é retrieval-first: PageIndex identifica as páginas relevantes, multimodal lê só essas. Pra documentos abaixo de 30 páginas com perguntas que podem se referir a qualquer parte, PDF nativo inteiro é razoável. Acima disso, retrieval-first.

> [!warning] Usar OCR + texto como default em 2026 — documentos com layout perdem sinal crítico
> Muitos pipelines criados em 2022-2023 usam `pdfplumber` / `pdfminer` / `Textract` + LLM texto e funcionam "bem o suficiente". Mas "bem o suficiente" oculta a perda silenciosa de layout: tabelas ficam linearizadas, cabeçalhos viram texto plano, a tabela de um contrato que tem colunas "parte A / parte B / obrigação" vira uma string sem estrutura. O modelo raciocina em cima de input degradado e pode tirar conclusões erradas. Antes de deixar o pipeline OCR no ar, teste com PDF nativo e compare acurácia de extração em 10 documentos representativos.

> [!warning] Não citar a página no prompt — modelo extrai sem referência e torna o output não-auditável
> "Extraia os campos do contrato" sem pedir referência de página entrega um JSON limpo que parece correto mas que você não consegue verificar. Se o model alucinação uma data de vigência, você não sabe nem em que página procurar. Sempre peça: "Cite a página de cada campo extraído." O modelo passa a incluir `"pagina": 12` junto com cada valor, o que transforma qualquer discrepância em auditoria de 30 segundos em vez de revisão completa do documento.

## Como explicar em inglês

**Interview quote:** *"For document-heavy workflows in 2026, we default to native PDF — Claude, Gemini, and OpenAI Files all handle it without us writing rendering code. For large documents over 100 pages, we use PageIndex to identify relevant pages first, then pass only those pages to the multimodal model. We always ask the model to cite the page number for each extracted field — that makes hallucinations auditable in seconds."*

| Português | Inglês |
|---|---|
| PDF nativo (suporte nativo do provider) | Native PDF support |
| Extração de campos de documento | Document field extraction |
| Renderização de página como imagem | Rendering page as image |
| Chunk de páginas com overlap | Page chunk with overlap |
| Retrieval por árvore de índice (PageIndex) | Structural retrieval / PageIndex |
| Citar a página de cada campo | Cite the page number per field |
| OCR + texto puro | OCR-plus-text pipeline |
| Upload via Files API | Files API upload |
| Custo por token de PDF | Token cost per PDF page |

## O que vem a seguir

Com PDFs e documentos cobertos, a nota 04 entra em **áudio e vídeo** — as modalidades com maior custo de contexto e onde a escolha de provider (Whisper vs GPT-4o Realtime vs Gemini nativo) faz mais diferença do que em qualquer outra. Geração de áudio e vídeo também aparecem brevemente, mas o foco é no uso como input.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #17.
- **Anthropic** — *PDF support* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support)). Limites e tokenização.
- **Google** — *Gemini API — Document understanding* ([docs](https://ai.google.dev/gemini-api/docs/document-processing)).
- **OpenAI** — *Files API* ([docs](https://platform.openai.com/docs/api-reference/files)). Upload e referência por `file_id`.
- **PyMuPDF (fitz)** — biblioteca padrão pra render/cortar PDF em Python.

## Veja também

- [[02 - Imagens como input — screenshots, charts, mockups]] — quando mandar página renderizada como imagem
- [[03-Dominios/Tecnologia/IA/RAG e Vector Databases/13 - PageIndex — RAG vectorless por árvore de documentos]] — retrieval estrutural pra documentos grandes
- [[05 - Tabelas e spreadsheets como input estruturado]] — tabela dentro de PDF tem caminhos próprios
- [[06 - Como dizer ao modelo o tipo de leitura]] — "extraia X" vs "analise Y" mudam o output do mesmo PDF
- [[07 - Limites e armadilhas multimodais]] — onde leitura de PDF falha
