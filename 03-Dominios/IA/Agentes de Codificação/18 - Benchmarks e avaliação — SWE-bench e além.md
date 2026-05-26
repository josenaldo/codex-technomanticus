---
title: "Benchmarks e avaliação — SWE-bench e além"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - agentes-codificacao
  - ia
  - ferramentas
aliases:
  - SWE-bench
  - AI coding benchmarks
  - Avaliação de agentes
---

# Benchmarks e avaliação — SWE-bench e além

> [!abstract] TL;DR
> SWE-bench é o benchmark de referência para avaliar [[Dicionário de IA#Coding agent|agentes de codificação]] — mede a capacidade de resolver issues reais de repositórios open-source. Em maio de 2026, os melhores agentes resolvem ~72% das issues na versão Verified (um subconjunto curado). Mas benchmarks são guias, não verdade — o mesmo modelo com scaffolding diferente pode ter scores muito diferentes. Para o engenheiro individual, o que importa é performance no SEU codebase, não no SWE-bench.

## O que é

**SWE-bench** (Software Engineering Benchmark) é um dataset criado pela Princeton que contém issues reais de repositórios populares do GitHub com seus respectivos patches (soluções). O agente recebe a issue e o repositório, e deve gerar um patch que resolva o problema.

## Por que importa

- É o **padrão da indústria** para comparar agentes — todos os provedores publicam scores
- Mede capacidade **end-to-end** — não só gerar código, mas entender o problema, navegar o codebase, e gerar um fix correto
- Os resultados influenciam decisões de compra e adoção

## Como funciona

### Versões do SWE-bench

| Versão                 | Issues | Dificuldade          | Uso                      |
| ---------------------- | ------ | -------------------- | ------------------------ |
| **SWE-bench Full**     | 2,294  | Variada              | Pesquisa acadêmica       |
| **SWE-bench Verified** | 500    | Curada por humanos   | Comparação entre agentes |
| **SWE-bench Lite**     | 300    | Filtragem automática | Prototipagem rápida      |

### Scores atuais (maio 2026)

| Agente/Modelo                   | SWE-bench Verified | Notas                           |
| ------------------------------- | ------------------ | ------------------------------- |
| Claude Opus 4.6 + best scaffold | ~72%               | Líder                           |
| GPT-5.4 + OpenAI scaffold       | ~69%               | Forte                           |
| Gemini 3.1 Pro                  | ~65%               | Melhora com contexto longo      |
| DeepSeek V4                     | ~63%               | Impressionante para open-weight |
| Qwen 3.6 Plus                   | ~61%               | Melhor em workflows agentic     |
| Devin                           | ~55-60%            | Scaffold autônomo               |

> [!warning] Scaffolding importa MAIS que o modelo
> O mesmo Claude Opus pode ter scores variando de 50% a 72% dependendo do scaffolding (como o codebase é indexado, quais ferramentas estão disponíveis, como os prompts são construídos). Comparar modelos sem controlar o scaffold é comparar maçãs com laranjas.

### Limitações dos benchmarks

| Limitação               | Explicação                                                                                           |
| ----------------------- | ---------------------------------------------------------------------------------------------------- |
| **Selection bias**      | Issues do SWE-bench são de repos Python maduros (Django, scikit-learn). Não representam TODO coding. |
| **Scaffold dependency** | Score depende do harness tanto quanto do modelo                                                      |
| **Snapshot temporal**   | Issues são de 2019-2024. Modelos treinados em dados mais recentes podem ter visto os patches.        |
| **Não mede qualidade**  | Um patch que resolve a issue pode introduzir novos bugs. O benchmark não verifica regressão.         |
| **Não mede workflow**   | Mede resultado final, não o processo. Não captura se o agente é bom para trabalho interativo.        |

### Além do SWE-bench

| Benchmark               | O que mede                                | Foco                               |
| ----------------------- | ----------------------------------------- | ---------------------------------- |
| **HumanEval+**          | Geração de funções a partir de docstring  | Coding puro (sem contexto de repo) |
| **MBPP**                | Problemas de programação básicos          | Capacidade fundamental             |
| **LMSYS Chatbot Arena** | Preferência humana em respostas           | Qualidade percebida                |
| **Aider Polyglot**      | Edit performance em múltiplas linguagens  | Edição multi-linguagem             |
| **Terminal-Bench**      | Performance em tarefas de terminal/DevOps | Agentes de terminal                |
| **Seu próprio projeto** | Performance real no seu codebase          | O que realmente importa            |

### Como avaliar para o SEU codebase

1. **Crie sua mini-suite** — pegue 10-20 issues resolvidas do seu repositório
2. **Teste cada ferramenta** — dê a issue para o agente e veja se ele resolve
3. **Meça o que importa:**
   - Taxa de resolução (resolve sem ajuda?)
   - Qualidade do código (segue seus padrões?)
   - Custo (quantos [[Dicionário de IA#Token|tokens]] gastou?)
   - Tempo (quanto tempo levou?)
4. **Compare ferramentas no seu contexto** — SWE-bench diz que Opus > GPT-5, mas no SEU projeto com SEU stack, pode ser diferente

## Armadilhas

- **"72% no SWE-bench = resolve 72% dos meus bugs"** — falso. Seu codebase, suas linguagens, sua complexidade são diferentes.
- **Escolher modelo apenas por benchmark** — benchmarks são indicadores, não decisores. Teste no seu contexto.
- **Ignorar scaffolding** — o mesmo modelo em tools diferentes tem performance muito diferente.
- **Benchmark gaming** — provedores otimizam para SWE-bench. Performance "real" pode ser menor.
- **Não medir custo-benefício** — um modelo que resolve 5% mais issues mas custa 3x mais pode não valer.

## Veja também

- [[05 - Panorama de modelos 2026]] — (Trilha 1) scores por modelo
- [[11 - Comparativo — qual ferramenta para qual tarefa]] — decisão prática
- [[13 - Devin e agentes autônomos cloud]] — quem lidera nos benchmarks

## Referências

- **Jimenez et al.** — *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* (Princeton, 2024). Paper original.
- **SWE-bench** — *Leaderboard* (swebench.com). Rankings atualizados.
- **Artificial Analysis** — *Coding Model Benchmark* (2026). Comparativo independente.
