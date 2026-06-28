---
title: "02 - Imagens como input — screenshots, charts, mockups"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: Iniciado
progress: in_progress
tags:
  - multimodal
  - prompt-engineering
  - ia
  - vision
publish: true
aliases:
  - Vision input
  - Image prompting
---

# 02 - Imagens como input — screenshots, charts, mockups

> [!abstract] TL;DR
> Imagem é a modalidade não-textual mais usada em 2026. Cinco tipos de tarefa cobrem 90% dos casos: descrição, extração, comparação, debug e classificação. O custo varia muito por provider — Anthropic cobra por área (até ~1600 tokens em max-res), OpenAI separa "low detail" (~85 tokens) de "high detail" (~85 + 170 por tile 512x512), Gemini cobra constante (~258 tokens por imagem em tiers normais). Resolução alta nem sempre é necessária; mande low detail quando a tarefa é classificação grossa, high detail só pra leitura de texto pequeno ou gráfico denso. Templates por tarefa no fim da nota.

> [!question]- Como saber se devo usar `detail: low` ou `detail: high` no OpenAI — e existe equivalente no Claude e Gemini?
> A decisão gira em torno de **o que a tarefa precisa ler**. Use `low` (85 tokens fixos) quando você só precisa classificar o tipo de imagem, gerar alt text genérico, ou filtrar se a imagem contém determinado elemento — a resolução de 512×512 que o `low` usa é suficiente pra essas tarefas. Use `high` quando precisa ler texto pequeno (campo de formulário, número em gráfico, código em screenshot), comparar detalhes finos, ou fazer diagnóstico de UI. No Claude, não existe parâmetro de detalhe explícito — o modelo recebe a imagem em resolução original e decide internamente; reduzir o tamanho antes de enviar tem efeito equivalente ao `low`. No Gemini, imagens abaixo de ~768×768 são upscaled internamente; acima de 3072×3072 são redimensionadas — a tokenização constante (~258) se mantém na maioria dos casos.

## Cinco tipos de tarefa visual

Toda chamada multimodal com imagem cai em um destes — útil pra decidir a resolução, o prompt e o modelo:

### 1. Descrição

"O que está nesta imagem?" Pra alt text, indexação, classificação preliminar. Tolerante a low detail. Modelos pequenos servem (Haiku, GPT-4.1 nano, Gemini Flash-Lite).

### 2. Extração

"Liste todos os campos preenchidos neste formulário." Pra OCR-as-a-service, captura de dados de docs. Exige high detail se o texto for pequeno. Modelos médios ou grandes (Sonnet, GPT-4.1, Gemini Flash).

### 3. Comparação

"Compare estes dois designs e liste diferenças." Pra design review, before/after, A/B visual. Exige consistência de leitura entre as duas imagens — modelos grandes (Opus, GPT-5, Gemini Pro) são mais confiáveis.

### 4. Debug / diagnóstico

"O dropdown está aparecendo atrás do modal. O que está errado?" Pra UI debugging, code review visual. Exige raciocínio sobre causa visual. Modelos grandes; reasoning models (o4-mini, gpt-5-thinking, Sonnet com extended thinking) ajudam.

### 5. Classificação estruturada

"Esse mockup viola alguma das 10 heurísticas de Nielsen? Para cada, indique sim/não com evidência." Cruzamento de descrição + análise + structured output. Modelos médios bastam, combinados com [[03-Dominios/Tecnologia/IA/Structured Outputs/02 - JSON Schema como contrato|JSON Schema]] no output.

## Custo por imagem — números de 2026

Tokens por imagem variam por provider, modelo e tier. Ordens de grandeza estáveis:

### Anthropic Claude

Tokens por imagem dependem da área (largura × altura) em pixels:

```
tokens ≈ (largura × altura) / 750
```

- 1092 × 1092 (max-res recomendada) → ~1600 tokens
- 512 × 512 → ~350 tokens
- 256 × 256 → ~90 tokens

Acima de 1568 px, o provider redimensiona automaticamente. Imagens "altas" longas (screenshots de página web) podem custar mais — mande cortado, não enviar a página inteira.

### OpenAI (GPT-4o, GPT-5, GPT-4.1)

Dois modos no parâmetro `detail`:

- **`low`** — fixo em **85 tokens**, equivalente a downscale pra 512×512. Use pra classificação grossa, descrição preliminar.
- **`high`** — **85 tokens base + 170 tokens por tile 512×512**. Uma imagem 1024×1024 = 85 + (4 tiles × 170) = 765 tokens.

Sem especificar `detail`, o default é `auto`, que escolhe baseado no tamanho — geralmente `high`. Para baixar custo, force `low` explicitamente.

### Google Gemini

Mais simples: **~258 tokens por imagem** em gemini-2.x normais, independente de tamanho (até o limite máximo). Imagens maiores que 3072×3072 são redimensionadas; menores que 768×768 são upscaled. Em Gemini 3.x Pro com input "high resolution mode", o custo pode subir, mas a regra base é constante.

### Comparativo

| Provider | 256×256 | 1024×1024 | Detalhe controlável? |
|---|---|---|---|
| Anthropic | ~90 tokens | ~1400 tokens | Não — por área |
| OpenAI low | 85 tokens | 85 tokens | Sim (`detail: low`) |
| OpenAI high | ~425 tokens | ~765 tokens | Sim (`detail: high`) |
| Gemini | 258 tokens | 258 tokens | Pouco |

Implicação: pra **classificação em massa** (milhares de imagens), OpenAI `low` é o mais barato. Pra **leitura de detalhe** (extração de texto pequeno, gráfico denso), Anthropic em max-res ou Gemini Pro são as opções mais consistentes.

## Code real — três providers

### Anthropic (Claude)

```python
import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

image_bytes = Path("mockup.png").read_bytes()
image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_b64,
                },
            },
            {
                "type": "text",
                "text": "Liste problemas de acessibilidade visíveis neste mockup."
            },
        ],
    }],
)

print(response.content[0].text)
print(f"Tokens: {response.usage.input_tokens} in / {response.usage.output_tokens} out")
```

URL também funciona — substitua o bloco `source` por `{"type": "url", "url": "https://..."}`.

### OpenAI (GPT-4o, GPT-5)

```python
from openai import OpenAI
import base64
from pathlib import Path

client = OpenAI()

image_bytes = Path("mockup.png").read_bytes()
image_b64 = base64.b64encode(image_bytes).decode("utf-8")

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_b64}",
                    "detail": "high",   # ou "low", "auto"
                },
            },
            {
                "type": "text",
                "text": "Liste problemas de acessibilidade visíveis neste mockup.",
            },
        ],
    }],
)

print(response.choices[0].message.content)
print(f"Tokens: {response.usage.prompt_tokens} in / {response.usage.completion_tokens} out")
```

URL direta também aceita — passe `image_url.url` apontando pra HTTPS público.

### Google Gemini

```python
from google import genai
from google.genai import types
from pathlib import Path

client = genai.Client()

image_bytes = Path("mockup.png").read_bytes()

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
        types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/png",
        ),
        "Liste problemas de acessibilidade visíveis neste mockup.",
    ],
)

print(response.text)
print(f"Tokens: {response.usage_metadata.prompt_token_count} in / "
      f"{response.usage_metadata.candidates_token_count} out")
```

Pra imagens grandes ou reutilizáveis, o Gemini tem **Files API** — upload uma vez, referencie por `name` em múltiplas chamadas.

## Templates por tarefa

### Descrição (alt text, indexação)

```
Descreva esta imagem em uma frase clara, otimizada para alt text.
Foque em: o que é, função visual, conteúdo principal.
Não invente detalhes que não consegue ver com clareza.
```

### Extração estruturada

```
Extraia os seguintes campos desta imagem de formulário:
- nome
- email
- telefone
- assunto
- mensagem

Se um campo estiver vazio ou ilegível, marque como null. Não invente.
Retorne em JSON com exatamente esses campos.
```

Combine com strict mode (ver [[03-Dominios/Tecnologia/IA/Structured Outputs/04 - OpenAI Structured Outputs — strict mode]]) pra garantir shape.

### Comparação

```
Compare as duas imagens (A é a primeira, B a segunda).
Liste:
1. Diferenças visíveis e relevantes (estrutura, cores, tipografia, layout)
2. Qual versão tem melhor hierarquia visual e por quê
3. Se houver elementos em A ausentes em B, sinalize

Ignore: diferenças causadas por anti-aliasing ou compressão.
```

Mande as duas imagens na mesma mensagem, em ordem.

### Debug de UI

```
Esta é uma captura de tela de bug em uma aplicação web.

Comportamento esperado: <descreva>
Comportamento observado: <descreva>

Analise a imagem e proponha hipóteses ordenadas pelo grau de evidência visual,
da mais provável pra menos provável. Para cada hipótese, indique o que da imagem
sustenta a hipótese.
```

A nota [[06 - Como dizer ao modelo o tipo de leitura]] aprofunda esse padrão.

## Boas práticas

- **Corte antes de mandar.** Screenshot de página web inteira gasta tokens em rodapé e header irrelevantes. Mande só a região de interesse.
- **Mande PNG, não JPG, pra texto.** JPG introduz artifact de compressão que confunde leitura de texto pequeno.
- **Use `detail: low` no OpenAI quando puder.** Pra classificação binária ou descrição grossa, low detail entrega 85 tokens fixos.
- **Suba pra max-res no Anthropic só quando necessário.** Tokens crescem com a área — 2x dimensão = 4x tokens.
- **Não envie 50 imagens em uma chamada se puder pré-filtrar.** Use modelo barato pra triagem, modelo bom pra análise final.

## Armadilhas comuns

> [!warning] Mandar screenshot da página inteira quando só a área relevante importa — custo desnecessário e distração
> Screenshot de página web com header, navbar, footer, e coluna lateral manda ao modelo 60-70% de informação irrelevante — e o modelo pode "distrair" com esses elementos ao analisar o conteúdo que interessa. Além do custo maior (mais pixels = mais tokens no Anthropic), o output tende a mencionar elementos irrelevantes. Sempre corte antes de mandar. No Python: PIL + `image.crop((x1, y1, x2, y2))`. Em CLI: `convert input.png -crop 800x600+100+50 output.png`. O model que recebe a região exata de interesse produz output mais focado.

> [!warning] Usar PNG sempre quando JPG seria suficiente — ou o contrário
> PNG é sem perda — ideal quando a imagem tem texto, código, interface de produto, ícone, gráfico com valores exatos. Para screenshots de UI, PNG é certo. JPG com compressão alta introduz artifact que confunde leitura de texto pequeno: "1va" em vez de "1/a", "O" em vez de "0". Por outro lado, mandar imagem fotográfica (rosto, cena, produto físico) como PNG sem necessidade infla o tamanho sem ganho de leitura — JPG quality 85 é suficiente pra fotos onde texto não precisa ser lido com precisão.

> [!warning] Não especificar `detail: low` na OpenAI quando a tarefa permite — custo 9x sem ganho
> Default do OpenAI quando você não passa `detail` é `auto`, que geralmente resolve pra `high` em imagens de tamanho padrão. Uma imagem 1024×1024 em `high` custa ~765 tokens; a mesma em `low` custa 85 tokens. Para pipelines de classificação, triagem, ou alt text onde low detail é suficiente, não especificar `detail` significa pagar ~9x por chamada. Em produção com 10k imagens/dia, a diferença é centenas de dólares por mês. Sempre declare explicitamente: `"detail": "low"` ou `"detail": "high"` — não deixe o `auto` decidir.

## Como explicar em inglês

**Interview quote:** *"For image inputs in 2026, we match resolution to task: classification uses OpenAI's detail-low at 85 tokens flat, reading small text uses high detail or Anthropic max-res. We always crop to the region of interest before sending — it reduces token cost and improves output focus. Our templates always include a null option for unreadable fields to prevent hallucination."*

| Português | Inglês |
|---|---|
| Imagem como input | Image as input |
| Modo de detalhe baixo / alto | Low / high detail mode |
| Corte de imagem antes de enviar | Image crop before sending |
| Tokens por área de imagem | Tokens per image area |
| PNG sem perda vs JPG com compressão | Lossless PNG vs compressed JPEG |
| Extração estruturada de imagem | Structured image extraction |
| Comparação visual (before/after) | Visual comparison (before/after) |
| Debug de UI via screenshot | UI debugging via screenshot |
| Classificação grossa (pré-filtro) | Coarse classification (pre-filter) |

## O que vem a seguir

Com imagens dominadas, a nota 03 entra em **PDFs e documentos** — que são sequências de páginas-imagem mas têm caminhos nativos em Claude, Gemini e OpenAI que simplificam o pipeline. A decisão de mandar o PDF nativo vs renderizar página por página como imagem é a principal bifurcação que a próxima nota resolve.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #17. Espinha conceitual.
- **Anthropic** — *Vision* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/vision)). Tabela de tokens por área.
- **OpenAI** — *Vision guide* ([docs](https://platform.openai.com/docs/guides/vision)). Cálculo de low/high detail.
- **Google** — *Gemini API — Vision* ([docs](https://ai.google.dev/gemini-api/docs/vision)). Image part API, Files API.

## Veja também

- [[01 - O salto multimodal — por que isso importa]] — contexto da modalidade
- [[03 - PDFs e documentos — extração e análise]] — quando enviar página como imagem vs como PDF nativo
- [[05 - Tabelas e spreadsheets como input estruturado]] — quando enviar tabela como imagem vs como texto
- [[06 - Como dizer ao modelo o tipo de leitura]] — a técnica que mais muda output
- [[07 - Limites e armadilhas multimodais]] — onde a leitura de imagem falha
