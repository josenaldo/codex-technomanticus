---
title: "Umar Jamil"
created: 2026-06-25
type: reference
publish: true
tags:
  - mestre
  - ia
  - llm
---

# Umar Jamil

Engenheiro e educador — especialista em implementar papers de LLMs do zero em PyTorch, com vídeos longos e densos que cobrem LLaMA, Mistral, Mamba e outros modelos arquitetura a arquitetura.

| Canal | Link |
|-------|------|
| YouTube | https://www.youtube.com/@umarjamilai |
| GitHub | https://github.com/hkproj |
| LinkedIn | |
| Site / Blog | |
| Bluesky / X | |

## Por que acompanhar

Umar Jamil é o criador de um canal no YouTube com um nicho muito específico e valioso: implementar, do zero em PyTorch, as arquiteturas dos modelos de linguagem mais importantes — LLaMA 2/3, Mistral, Mamba, transformers com KV cache — com explicações linha a linha. Os vídeos são longos (2-4 horas), sem cortes de conveniência, e o código resultante está disponível no GitHub como material de referência.

Para quem quer entender *como* um modelo de linguagem funciona na memória — como o KV cache cresce, como GQA reduz cabeças de atenção, como Mamba elimina a atenção — os vídeos do Jamil são o recurso mais próximo de "abrir o código-fonte de um LLM e passar linha por linha". Referência direta para [[04a - KV cache, prefill e decode — a física da inferência]], [[04b - Encolhendo o KV cache — MHA, MQA, GQA, MLA]] e [[04c - Atenção eficiente — FlashAttention, sparse e híbrida]].

## Conteúdo recomendado

- [*Coding LLaMA 2 from scratch in PyTorch*](https://www.youtube.com/watch?v=oM4VmoabDAI) — implementação completa do LLaMA 2 com RoPE, GQA e KV cache; referência para [[04b - Encolhendo o KV cache — MHA, MQA, GQA, MLA]].
- [*Mamba and State Space Models*](https://www.youtube.com/watch?v=8Q_tqwpTpVU) — implementação do Mamba do zero, com comparação explícita com transformers e atenção; referência para [[04c - Atenção eficiente — FlashAttention, sparse e híbrida]].
- [GitHub hkproj](https://github.com/hkproj) — repositório com implementações de LLaMA, Mistral, transformers e outros modelos em PyTorch limpo, sem dependências de frameworks.
