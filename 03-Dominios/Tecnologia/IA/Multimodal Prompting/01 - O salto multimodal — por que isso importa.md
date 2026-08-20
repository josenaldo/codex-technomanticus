---
title: "01 - O salto multimodal — por que isso importa"
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
publish: true
aliases:
  - Salto multimodal
  - Multimodal-native vs text-only
---

# 01 - O salto multimodal — por que isso importa

> [!abstract] TL;DR
> Em 2026, modelo de fronteira é multimodal nativo — Claude 4 (Opus, Sonnet, Haiku), GPT-5 e GPT-4.1, Gemini 2.x. O gargalo deixou de ser capacidade do modelo e virou hábito do engenheiro, que ainda monta pipeline OCR + extração + LLM-só-texto quando podia mandar a imagem direto. Multimodal nativo bate text-only em três frentes: não perde sinal na conversão (layout, hierarquia visual, gráficos, cor de status), encurta o pipeline (menos código, menos modos de falha) e desbloqueia casos onde a evidência **é** visual (acessibilidade, design review, debugging de UI, planilha com gráfico). Esta nota cobre o quê, por quê, e o anti-padrão "me dá só o texto" que ainda domina.

> [!question]- Vale o custo extra em tokens de imagem — quando multimodal nativo é melhor do que OCR?
> Depende do que a tarefa precisa ver. Se o documento tem layout relevante (coluna, tabela, hierarquia visual, gráfico, cor de status), multimodal nativo é melhor porque OCR lineariza o layout e perde esses sinais. O token por imagem é mais caro por chamada, mas o custo total por tarefa resolvida corretamente tende a cair — porque erro silencioso de OCR (CPF lido como "0PF", coluna desalinhada) gera retrabalho e correção manual que nunca aparece na conta de tokens. O threshold pragmático: use OCR + retrieval quando o documento é puramente textual ou quando o volume torna o token por imagem proibitivo (> 100 mil páginas). Use multimodal nativo quando layout, gráfico ou elemento visual importa pra tarefa.

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

Outro ângulo: o erro silencioso tem custo diferente do erro visível. Pipeline OCR produz respostas que parecem corretas mas não são — o modelo alucina coerentemente sobre input quebrado e entrega JSON que "fecha" sem estar certo. Multimodal nativo, quando falha, tende a sinalizar a incerteza ("Não consigo ler claramente essa região") em vez de chutar. Isso muda o modo de detecção de erro: de auditoria post-hoc (descobrir que as extrações de 3 semanas estavam erradas) para falha rápida e explícita que permite retry imediato.

Essa mudança de "erro silencioso" para "erro visível" é, em muitos casos, o maior benefício operacional de multimodal nativo — não a acurácia média, mas a previsibilidade da falha.

## Tokens visuais — como o modelo processa imagem

Entender como o modelo "vê" imagem ajuda a entender as limitações.

Na maioria dos modelos multimodais (incluindo Claude e GPT-4.1):

1. **A imagem é dividida em patches.** Um encoder visual (ViT — Vision Transformer, ou derivado) divide a imagem em regiões fixas (ex: 14×14 px por patch) e gera um embedding por patch.
2. **Esses embeddings são projetados pro espaço do LLM.** Um MLP adapta o espaço visual pro espaço de token do decoder de texto.
3. **A sequência resultante entra no contexto junto com o texto.** O modelo "vê" imagem e texto no mesmo passe de atenção.

Implicação prática: **resolução importa, mas tem limite de retorno**. Imagem grande → mais patches → mais tokens → mais custo. Claude e OpenAI têm "detail modes" (`high` / `low`):

| Mode | Quando usar | Custo |
|---|---|---|
| `low` | Imagem com poucos detalhes, busca rápida, pré-filtro | ~85 tokens (OpenAI) |
| `high` (auto) | Leitura de texto na imagem, tabela, diagrama técnico | Até 1000+ tokens dependendo do tamanho |
| PDF nativo (Claude) | Documentos com múltiplas páginas; preserva layout | ~1500-2000 tokens/página |

A lição: não mandar imagem em `high` por default sem verificar se `low` basta. Pra thumbnail ou ícone, `low` é suficiente. Pra leitura de extrato bancário, `high` é necessário.

## Escolhendo a modalidade certa

Matriz de decisão rápida:

| Caso | Modalidade ideal | Por que não text-only |
|---|---|---|
| Screenshot de bug / UI | Imagem (`high`) | Layout e estado visual são a evidência |
| Extrato bancário PDF | PDF nativo | Layout de tabela e alinhamento importam |
| Transcrição de entrevista | Áudio → Whisper ou GPT-4o Realtime | Evita perda de tom e paralingüística |
| Planilha com gráfico | Imagem (`high`) | Gráfico desaparece no OCR |
| Diagrama de arquitetura (whiteboard) | Imagem | Setas e conexões espaciais não são texto |
| Artigo de blog em markdown | Texto puro | Nenhum sinal visual — OCR não perde nada |
| Vídeo de demo / walkthrough | Vídeo nativo (Gemini) | Contexto temporal + visual + áudio juntos |
| Formulário preenchido | PDF / imagem | Layout de campo-valor não sobrevive ao OCR |

Para texto puro sem estrutura visual, OCR + LLM texto é igualmente bom e mais barato. Para qualquer coisa com layout, hierarquia visual, ou elemento não-textual, multimodal nativo é o caminho.

## Custo por modalidade — referência rápida

Estimativas de 2026 (verificar documentação atualizada — preços mudam):

| Modalidade | Provider | Custo aproximado | Nota |
|---|---|---|---|
| Imagem `low` | OpenAI GPT-4.1 | ~85 tokens de input | Thumbnail, ícone, pré-filtro |
| Imagem `high` | OpenAI GPT-4.1 | 85 + 170 por tile 512px | Imagem 1024×1024 ≈ 765 tokens |
| Imagem | Claude Sonnet | ~1600 tokens | Custo flat pra maioria das imagens |
| PDF página | Claude (document) | ~1500-2000 tokens/página | Preserva layout nativo |
| Áudio (Whisper) | OpenAI | $0.006/min | Separado do LLM |
| Vídeo ~10min | Gemini 1.5 Pro | ~200K tokens context | Vídeo consome contexto rápido |

Regra prática: **uma imagem high-detail ≈ 300-1500 palavras de texto em custo de token**. É bastante. Por isso, pré-filtrar com `low` antes de escalar pra `high` é uma boa prática em pipelines de alto volume: classifique com `low` se a imagem tem conteúdo relevante, depois processe com `high` só as que passarem.

Uma heurística útil pra documentos: se você consegue resolver o problema mandando só a página relevante (não o PDF inteiro), use imagem em vez de PDF. Mandar 50 páginas quando a informação está na página 3 é desperdício de contexto que o modelo vai ter que ignorar.

## Multimodal em código — padrão cross-provider

A estrutura de request varia por provider, mas o padrão lógico é o mesmo: lista de content parts com `type: image | text | document`.

**Claude (Anthropic SDK):**

```python
import anthropic, base64

with open("page.png", "rb") as f:
    img_b64 = base64.standard_b64encode(f.read()).decode()

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {"type": "base64", "media_type": "image/png", "data": img_b64},
            },
            {"type": "text", "text": "Quais são os valores na coluna 'Total'?"},
        ],
    }],
)
```

**OpenAI SDK:**

```python
import openai, base64

client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}", "detail": "high"}},
            {"type": "text", "text": "Quais são os valores na coluna 'Total'?"},
        ],
    }],
)
```

A diferença principal: Claude usa `source.type: base64` + `media_type`; OpenAI usa `data URI` inline no `image_url`. Para URL pública, ambos aceitam URL diretamente — `source.type: url` (Claude) ou `image_url.url: "https://..."` (OpenAI). LiteLLM abstrai os dois formatos se quiser trocar de provider sem mudar código.

## Armadilhas comuns

> [!warning] Token por imagem parece mais caro mas o cálculo correto é por tarefa resolvida
> A métrica que importa não é "custo desta chamada" mas "custo de processar N documentos com qualidade X". Pipeline OCR tem custo de infra de OCR, tratamento de erros de leitura, lógica de extração de tabela, e debug quando alucina. Multimodal nativo paga mais em token mas elimina camadas inteiras do pipeline. Meça antes de concluir que OCR é mais barato.

> [!warning] Mandar imagem sem instrução do que ler — o modelo faz o best-effort que pode ser irrelevante
> Imagem sem contexto leva o modelo a descrever visualmente o que vê. Se a tarefa é "extrair o total da NF", o prompt precisa dizer exatamente isso. Multimodal sem instrução de leitura é como passar um documento pra alguém sem dizer o que você quer saber. Ver [[06 - Como dizer ao modelo o tipo de leitura]] para o padrão correto.

> [!warning] Assumir que multimodal nativo funciona igual em todos os providers
> Claude, GPT-4.1 e Gemini têm capacidades diferentes: Claude não processa áudio nem vídeo nativamente (2026); Gemini processa. PDFs: Claude tem PDF nativo via `document` source; OpenAI usa Files API; Gemini aceita PDF direto. Quem documenta pra Claude e testa no Gemini (ou vice-versa) vai encontrar comportamentos distintos pra mesma imagem — especialmente em densidade de texto e orientação.

## Como explicar em inglês

**Interview quote:** *"Multimodal-native beats text-only pipelines on three fronts: it preserves signal that OCR drops — layout, visual hierarchy, charts, color-coded status — it shortens the pipeline and reduces failure modes, and it unlocks tasks where the evidence is inherently visual. The real cost comparison isn't tokens per call; it's cost per correctly resolved task."*

| Português | Inglês |
|---|---|
| Modelo multimodal nativo | Multimodal-native model |
| Pipeline OCR + extração + LLM | OCR-plus-extraction pipeline (text-only) |
| Perda de sinal visual | Visual signal loss |
| Hierarquia visual | Visual hierarchy |
| Tokens visuais / patches de imagem | Visual tokens / image patches |
| Modo de detalhe de imagem (low / high) | Image detail mode (low / high) |
| Custo por tarefa resolvida | Cost per correctly resolved task |
| Anti-padrão "me dá só o texto" | "Give me just the text" anti-pattern |
| Documento puramente textual sem layout | Text-only document with no layout |

## O que vem a seguir

Com o salto multimodal contextualizado, a nota 02 entra na modalidade mais usada na prática: **imagens como input**. Você vai ver como diferentes tipos de imagem (screenshot, chart, mockup, foto) exigem abordagens distintas, como calcular custo de tokens por imagem em Claude e OpenAI, e quais prompts extraem mais sinal de cada tipo.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #17 (Multimodal Prompting). Espinha dorsal da trilha.
- **Roboflow** — [*When to use multimodal LLMs vs. computer vision models*](https://blog.roboflow.com/) — comparativo prático de custo vs acurácia por caso de uso.
- **Anthropic** — *Vision* ([docs](https://docs.anthropic.com/en/docs/build-with-claude/vision)). Capabilities e limites do Claude.
- **OpenAI** — *Vision guide* ([docs](https://platform.openai.com/docs/guides/vision)). Como GPT-4o/5 leem imagem.
- **Google** — *Gemini API — Document understanding* ([docs](https://ai.google.dev/gemini-api/docs/document-processing)). Multimodal nativo no Gemini.
- **LiteLLM** — [*Multimodal proxy*](https://docs.litellm.ai/docs/providers/anthropic#vision) — abstração cross-provider pra chamadas multimodais.

## Quando multimodal nativo ainda não é suficiente

Multimodal nativo não resolve tudo. Casos onde o pipeline ainda vai exigir pré-processamento:

- **Documento rotacionado ou skewed:** modelo multimodal pode ler texto inclinado, mas a acurácia cai. Pre-processar com deskew (OpenCV, ImageMagick) antes de enviar ainda ajuda.
- **Imagem de resolução muito baixa ou comprimida:** JPEG com muito artefato de compressão afeta NER (Named Entity Recognition) visual do modelo. Upscale antes de enviar — mas cuidado com alucinação de upscaler que "inventa" pixels.
- **Tabela com mais de ~100 colunas:** modelos têm dificuldade com tabelas muito largas em uma única imagem. Dividir a imagem em crops por seção vertical e reassemblar as extrações no código.
- **Handwriting muito irregular:** reconhecimento de letra manual ainda é pior do que texto impresso. Modelo multimodal ajuda mas não elimina o erro; revisar por amostragem.
- **Documentos com múltiplos idiomas misturados na mesma página:** pode confundir NER, especialmente pra línguas com scripts diferentes (árabe + inglês + japonês na mesma página).

Conhecer os limites é tão importante quanto conhecer os casos de uso — define onde o pipeline ainda precisa de lógica adicional.

## Veja também

- [[02 - Imagens como input — screenshots, charts, mockups]] — a modalidade mais comum, com tokens por provider
- [[03 - PDFs e documentos — extração e análise]] — quando PDF nativo bate OCR
- [[04 - Áudio e vídeo — Whisper, Gemini Live e geração]] — modalidades além da imagem
- [[05 - Tabelas e spreadsheets como input estruturado]] — caso especial de layout-heavy
- [[06 - Como dizer ao modelo o tipo de leitura]] — multimodal sem instrução de leitura é desperdício
- [[07 - Limites e armadilhas multimodais]] — onde multimodal nativo falha
- [[Dicionário de IA#Multimodal|Dicionário: Multimodal]], [[Dicionário de IA#OCR|Dicionário: OCR]]
