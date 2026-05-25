---
title: "Tokens e tokenização"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - anatomia-llm
  - ia
  - tokens
aliases:
  - Tokenization
  - BPE
  - Byte Pair Encoding
---

# Tokens e tokenização

> [!abstract] TL;DR
> Tokens são as unidades atômicas que LLMs processam — não caracteres, não palavras, mas pedaços intermediários de texto definidos por um algoritmo de compressão chamado BPE. Uma palavra comum como "the" é 1 token; "tokenização" pode ser 3. Entender tokenização é pré-requisito para entender custos, limites de contexto e por que seu prompt às vezes gasta mais do que esperado.

## O que é

**Tokenização** é o processo de converter texto bruto (strings de caracteres) em sequências de **[[Dicionário de IA#Token|tokens]]** — unidades numéricas que o modelo realmente processa. Cada token é mapeado para um ID inteiro no vocabulário do modelo.

Um token **não é** uma palavra. Dependendo do tokenizador:

- `"hello"` → 1 token
- `"tokenização"` → 3 tokens (`"token"`, `"iza"`, `"ção"`)
- `" "` (espaço) → geralmente embutido no token seguinte
- `"😊"` → 1-2 tokens (byte-level BPE resolve Unicode nativamente)

O vocabulário típico de um LLM moderno tem entre **32.000 e 200.000 tokens**.

## Por que importa

Tokens são a unidade de **tudo** em [[Dicionário de IA#LLM (Large Language Model)|LLMs]]:

1. **Custo** — APIs cobram por milhão de tokens (input e output separadamente)
2. **Limite de contexto** — a janela de contexto é medida em tokens, não em palavras ou caracteres
3. **Velocidade** — cada token gerado exige uma passada completa pelo modelo
4. **Qualidade** — tokenização ruim (quebras em pontos estranhos) degrada a capacidade do modelo de entender o texto

**Regra prática para inglês:** 1 token ≈ 4 caracteres ≈ 0.75 palavras. Para português, a proporção é pior: ~1 token ≈ 3 caracteres, porque diacríticos e sufixos aumentam a fragmentação.

## Como funciona

### Byte Pair Encoding (BPE)

O algoritmo mais usado em LLMs modernos. É um método de compressão iterativo e determinístico.

#### Passo a passo

1. **Inicialização** — começar com um vocabulário base de todos os bytes individuais (256 entries)
2. **Contagem** — escanear o corpus de treinamento e contar a frequência de todos os pares adjacentes de tokens
3. **Merge** — fundir o par mais frequente em um novo token e adicioná-lo ao vocabulário
4. **Repetição** — repetir passos 2-3 até atingir o tamanho de vocabulário desejado (ex: 100k)

#### Exemplo concreto

```
Corpus: "aab aab aac"
Vocab inicial: {a, b, c, espaço}

Iteração 1: par mais frequente = "aa" → merge → novo token "aa"
  Corpus: "aa b aa b aa c"

Iteração 2: par mais frequente = "aa b" → merge → novo token "aab"
  Corpus: "aab aab aa c"

(continua até atingir vocab size)
```

### Variantes de tokenização

| Método                      | Usado por             | Características                                                               |
| --------------------------- | --------------------- | ----------------------------------------------------------------------------- |
| **Byte-Level BPE**          | GPT-4, Llama 3/4      | Opera em bytes, não caracteres. Resolve qualquer Unicode sem "unknown tokens" |
| **SentencePiece (Unigram)** | T5, modelos Google    | Modelo probabilístico que encontra a segmentação mais provável                |
| **WordPiece**               | BERT, modelos antigos | Similar a BPE mas usa likelihood em vez de frequência                         |
| **Tiktoken**                | OpenAI (GPT-3.5+)     | Implementação otimizada de BPE em Rust, usada pela API                        |

### Impacto da tokenização no custo

```
Frase em inglês: "The quick brown fox" → 4 tokens
Frase em português: "A raposa marrom rápida" → ~7 tokens
Frase em japonês: "素早い茶色の狐" → ~8-10 tokens
```

Isso significa que **usar LLMs em idiomas não-ingleses custa mais** — o tokenizador foi treinado predominantemente em texto inglês, então tem mais merges para padrões ingleses.

### Tokenizadores na prática

Para contar tokens antes de enviar para a API:

| Provider    | Ferramenta                                                             | Uso                                                          |
| ----------- | ---------------------------------------------------------------------- | ------------------------------------------------------------ |
| OpenAI      | `tiktoken` (Python)                                                    | `tiktoken.encoding_for_model("gpt-4").encode("texto")`       |
| Anthropic   | Estimativa via API                                                     | Resposta inclui `usage.input_tokens` e `usage.output_tokens` |
| Google      | `count_tokens()` API                                                   | Endpoint dedicado para contagem                              |
| Open-source | `tokenizers` (HuggingFace)                                             | Biblioteca universal para qualquer tokenizador               |
| Visual      | [platform.openai.com/tokenizer](https://platform.openai.com/tokenizer) | Visualização interativa                                      |

## Comparativo

| Aspecto                      | Character-level | Word-level   | **Subword (BPE)**  |
| ---------------------------- | --------------- | ------------ | ------------------ |
| **Vocab size**               | ~256            | 100k+        | 32k–200k           |
| **Palavras desconhecidas**   | Nenhuma         | Muitas (OOV) | Nenhuma            |
| **Comprimento da sequência** | Muito longo     | Curto        | Otimizado          |
| **Cobertura de idiomas**     | Total           | Limitada     | Total (byte-level) |
| **Uso em LLMs modernos**     | Raro            | Legado       | **Padrão**         |

## Armadilhas

- **"1 token = 1 palavra"** — falso. Uma palavra longa ou incomum pode ser 3-5 tokens. Palavras curtas e comuns geralmente são 1 token.
- **Ignorar a contagem antes de enviar** — sem contar tokens, é impossível prever custo e saber se cabe na janela de contexto. Use tiktoken ou equivalente.
- **Tokenização cross-language** — modelos treinados predominantemente em inglês gastam 1.5x–3x mais tokens em outros idiomas. Isso impacta custo e eficiência de contexto.
- **"Tokens de código são iguais a tokens de texto"** — código tende a ser mais eficiente por ter padrões repetitivos (keywords, indentação). Mas strings e comentários longos consomem tanto quanto texto natural.
- **Não considerar tokens especiais** — tokens como `<|start|>`, `<|end|>`, separadores de role consomem espaço no contexto sem serem visíveis ao usuário.

## Veja também

- [[01 - O que é um LLM]] — contexto geral dos modelos
- [[03 - A janela de contexto]] — como tokens definem os limites do que o modelo "vê"
- [[10 - Pricing de APIs — como calcular custos]] — impacto direto da contagem de tokens no bolso

## Referências

- **Sennrich, Haddow, Birch** — *Neural Machine Translation of Rare Words with Subword Units* (2016). Paper original do BPE para NLP.
- **OpenAI** — *Tiktoken* (GitHub). Implementação de referência do tokenizador GPT.
- **HuggingFace** — *Tokenizers library*. Biblioteca universal para BPE, WordPiece, Unigram.
- **Karpathy, Andrej** — *Let's build the GPT tokenizer* (YouTube, 2024). Implementação de BPE do zero em ~2h.
