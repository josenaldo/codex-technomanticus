---
title: "05 - Tabelas e spreadsheets como input estruturado"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - multimodal
  - prompt-engineering
  - ia
  - tabular-data
publish: true
aliases:
  - Tabular input
  - Spreadsheet prompting
  - Tabela como input
---

# 05 - Tabelas e spreadsheets como input estruturado

> [!abstract] TL;DR
> Tabela pro LLM tem três modos: como texto (CSV/Markdown colado no prompt — o modelo parsea), como imagem (screenshot — boa pra tabelas com merged cells, charts, layout visual) e como ferramenta (modelo lê arquivo via code interpreter, pandas, ou tool customizado). Texto ganha em precisão de valor; imagem ganha em layout e gráfico; ferramenta ganha em dataset grande onde computação importa. Pra dataset grande, pattern padrão: pandas `describe()` + sample de 10 linhas = contexto suficiente sem mandar 1M de células. Tabela é onde mais se ganha combinando modalidades — relatório financeiro com texto + tabela + gráfico merece todos os três caminhos juntos.

## Os três modos

### Modo 1 — Texto (CSV, Markdown, JSON)

Cola a tabela formatada no prompt. O modelo parsea internamente.

**Quando ganha:**
- Dataset pequeno (até ~100 linhas).
- Você precisa de valores exatos preservados (financeiro, datas, IDs).
- O ganho de layout visual é zero (tabela retangular simples).

**Quando perde:**
- Tabela com merged cells, hierarquia visual, cores de status.
- Dataset grande (1k+ linhas consomem contexto).
- Há gráficos junto que importam pro raciocínio.

Formato no prompt:

```
| Cliente | Faturamento | Status   |
|---------|-------------|----------|
| Acme    | 120000      | ativo    |
| Globex  | 87000       | inativo  |
| Initech | 95000       | ativo    |
```

Markdown é mais legível pro modelo que CSV puro, mas ambos funcionam. Para JSON estruturado:

```python
import json

data = [
    {"cliente": "Acme", "faturamento": 120000, "status": "ativo"},
    {"cliente": "Globex", "faturamento": 87000, "status": "inativo"},
]

prompt = f"""Analise os clientes abaixo (JSON):

{json.dumps(data, indent=2, ensure_ascii=False)}

Liste os clientes inativos com faturamento acima da mediana dos ativos."""
```

### Modo 2 — Imagem (screenshot)

Mande print da planilha ou PDF renderizado.

**Quando ganha:**
- Tabela com merged cells, células coloridas, hierarquia de header complexa.
- Gráfico embutido (barra, pizza, linha) que importa pra resposta.
- Documento original tem layout (relatório anual, dashboard).
- Você precisa que o modelo "veja" formatação condicional (status verde/vermelho).

**Quando perde:**
- Precisão numérica fina (modelo pode ler "12345" como "1234s" em imagem ruim).
- Tabela muito densa (texto pequeno deteriora extração).

Pra screenshot de planilha, prefira PNG em alta resolução, com zoom razoável (linhas legíveis a olho nu).

### Modo 3 — Tool / code interpreter

Modelo executa código (geralmente Python com pandas/polars) sobre o arquivo. Pra isso usa:

- **OpenAI** — Code Interpreter (Assistants/Responses API) ou tool customizado que executa `pandas`.
- **Anthropic** — tool customizado executando Python (sandbox seu).
- **Gemini** — Code Execution tool nativa.

**Quando ganha:**
- Dataset grande (10k+ linhas).
- Tarefa exige computação (agregação, join, groupby, regressão).
- Quer reproducibilidade — código é evidência da resposta.

**Quando perde:**
- Tarefa não envolve computação ("explique essa coluna").
- Dataset pequeno onde texto direto resolve.
- Quer baixa latência (executar código adiciona tempo).

## Pattern padrão pra dataset grande — describe + sample

Quando o dataset é grande mas você só precisa que o modelo entenda o **shape**, não que processe cada linha:

```python
import pandas as pd

df = pd.read_csv("vendas_2025.csv")  # 250k linhas

# Resumo estatístico de cada coluna
summary = df.describe(include="all").to_markdown()

# Amostra estratificada
sample = df.sample(10, random_state=42).to_markdown(index=False)

prompt = f"""Esta é uma tabela de vendas de 2025 com 250k linhas.

Resumo estatístico das colunas:
{summary}

Amostra de 10 linhas:
{sample}

Pergunta: existe sazonalidade clara? Quais hipóteses você teria sobre os outliers
de faturamento?
"""
```

Esse pattern entrega ~50-100 linhas de contexto pro modelo, contra 250k linhas brutas. O modelo "vê" o dataset sem ler cada célula. Use code interpreter / tool pra verificar hipóteses depois.

Variante com mais sinal: junte `describe()` + top-5 valores únicos por coluna categórica + 10 linhas de exemplo.

## Code — três providers, três modos

### Anthropic — tabela como imagem

```python
import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

# Screenshot do dashboard do Looker
img_b64 = base64.standard_b64encode(Path("dashboard.png").read_bytes()).decode()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": img_b64,
                },
            },
            {
                "type": "text",
                "text": (
                    "Esta é uma página de relatório financeiro. Extraia em JSON: "
                    "os 3 KPIs do topo (nome, valor, variação YoY), e os dados "
                    "exatos do gráfico de barras (mês, valor). Cite formatação "
                    "condicional (verde/vermelho) quando aparecer."
                ),
            },
        ],
    }],
)

print(response.content[0].text)
```

### OpenAI — Code Interpreter rodando pandas

```python
from openai import OpenAI

client = OpenAI()

# Upload do arquivo
file = client.files.create(
    file=open("vendas_2025.csv", "rb"),
    purpose="assistants",
)

response = client.responses.create(
    model="gpt-5",
    tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
    input=[{
        "role": "user",
        "content": [
            {"type": "input_file", "file_id": file.id},
            {
                "type": "input_text",
                "text": (
                    "Carregue este CSV de vendas com pandas. Mostre describe() das "
                    "colunas numéricas, conte valores únicos das categóricas, e "
                    "identifique outliers de faturamento (>2 desvios da média). "
                    "Retorne um gráfico de boxplot por categoria."
                ),
            },
        ],
    }],
)

print(response.output_text)
```

O modelo escreve código, executa no sandbox, lê o resultado e responde.

### Gemini — tabela como texto Markdown

```python
from google import genai

client = genai.Client()

# Tabela pequena via texto Markdown
table_md = """
| Mês | Receita | Custo  | Margem |
|-----|---------|--------|--------|
| Jan | 120000  | 85000  | 29%    |
| Fev | 135000  | 92000  | 32%    |
| Mar | 118000  | 89000  | 25%    |
| Abr | 142000  | 88000  | 38%    |
""".strip()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        f"Tabela trimestral:\n\n{table_md}",
        (
            "1. Qual mês teve a melhor margem percentual? "
            "2. Se o custo de Abril seguisse o padrão dos meses anteriores "
            "(média Jan-Mar), qual teria sido a margem?"
        ),
    ],
)

print(response.text)
```

## Caso composto — relatório financeiro

Cenário real: relatório trimestral em PDF, com texto narrativo, tabelas, gráficos. Como mandar pro modelo?

Combinação que funciona em 2026:

1. **Capa e narrativa** → PDF nativo (ver [[03 - PDFs e documentos — extração e análise]]).
2. **Tabelas críticas com valores que importam** → também via texto Markdown, redundante mas mais preciso.
3. **Gráficos** → o PDF nativo já cobre, mas se quiser análise específica, mande o screenshot do gráfico isolado em high detail.
4. **Dataset bruto subjacente (se tiver acesso)** → CSV via code interpreter pra validar números.

Mistura assim:

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": [
            {"type": "document", "source": {"type": "base64",
                "media_type": "application/pdf", "data": pdf_b64}},
            {"type": "text", "text":
                "Tabela 4 (em texto, valores exatos):\n\n" + tabela_md},
            {"type": "image", "source": {"type": "base64",
                "media_type": "image/png", "data": grafico_b64}},
            {"type": "text", "text":
                "Analise: a narrativa do PDF é consistente com os números da "
                "Tabela 4 e o gráfico? Sinalize discrepâncias com a página/seção."
            },
        ],
    }],
)
```

Vale o custo de token extra quando a resposta precisa ser auditável.

## Comparativo dos três modos

| Critério | Texto | Imagem | Tool |
|---|---|---|---|
| Precisão numérica | Alta | Média | Alta |
| Captura layout | Não | Sim | Não |
| Captura gráfico | Não | Sim | Sim (gera) |
| Dataset grande | Ruim | Ruim | Ótimo |
| Setup | Trivial | Trivial | Médio |
| Custo | Baixo | Médio-alto | Alto |
| Auditável | Sim | Não tanto | Sim (código) |

## Boas práticas

- **Default = texto Markdown.** Só vá pra imagem ou tool quando o caso justifica.
- **Não cole 10k linhas.** Use `describe()` + sample. Se precisar processar, use tool.
- **Combine quando o documento é misto.** Relatório financeiro merece PDF + texto + imagem.
- **Numere as tabelas no prompt.** "Tabela 1", "Tabela 2" facilita referência cruzada.
- **Cuidado com CSV de português.** Vírgula como separador decimal quebra parsing — converta antes pra `.` ou explicite no prompt.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #17.
- **Pandas** — `DataFrame.describe()`, `to_markdown()`. Ferramenta padrão pra contexto compacto.
- **OpenAI** — *Code Interpreter* ([docs](https://platform.openai.com/docs/assistants/tools/code-interpreter)). Tool rodando pandas dentro do modelo.
- **Google** — *Code Execution* ([docs](https://ai.google.dev/gemini-api/docs/code-execution)). Equivalente no Gemini.

## Veja também

- [[02 - Imagens como input — screenshots, charts, mockups]] — screenshot de tabela é caso particular
- [[03 - PDFs e documentos — extração e análise]] — tabela dentro de PDF nativo
- [[03-Dominios/Tecnologia/IA/Structured Outputs/02 - JSON Schema como contrato]] — pra forçar shape no output de extração
- [[06 - Como dizer ao modelo o tipo de leitura]] — "extraia" vs "analise" vs "resuma" mudam o output
- [[07 - Limites e armadilhas multimodais]] — leitura de tabela em imagem tem armadilhas próprias
