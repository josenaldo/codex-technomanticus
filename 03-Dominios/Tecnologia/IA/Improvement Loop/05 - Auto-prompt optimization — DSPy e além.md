---
title: "05 - Auto-prompt optimization — DSPy e além"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: Iniciado
progress: in_progress
tags:
  - improvement-loop
  - ia
  - dspy
  - auto-prompt
  - otimizacao
publish: true
aliases:
  - DSPy
  - Auto-prompt
  - Compilador de prompts
---

# 05 - Auto-prompt optimization — DSPy e além

> [!abstract] TL;DR
> Auto-prompt optimization transforma prompt de "string artesanal" em "programa compilado": você declara o que quer (Signatures de input/output em DSPy), declara a métrica de sucesso (eval function), o compilador otimiza a versão final do prompt contra exemplos. **DSPy** (Stanford, Khattab et al., 2023) é o framework de referência em 2026: Signatures, Modules, Compilers (BootstrapFewShot, MIPRO, COPRO). Vizinhos: **APE** (Zhou et al., 2023) gera candidatos via LLM-meta-prompter, **OPRO** (Yang et al., 2023) trata LLM como otimizador iterativo, **promptbreeder** (Fernando et al., 2023) usa evolução. Quando auto-prompt vence: pipeline com várias chamadas LM, eval claro, iteração repetida. Quando manual vence: one-shot alto-risco, edge-case que exige judgment, ausência de eval confiável. Estado 2026: real e crescente em produção, mas longe de "default" — muito uso ainda é experimental ou em pipeline acadêmico.

> [!question]- Compensa aprender DSPy hoje ou o espaço vai consolidar num único vencedor em breve?
> Em 2026 vale aprender DSPy mesmo com o espaço em movimento — por duas razões. Primeira: os conceitos (Signature, Module, Compiler, eval function como critério) vão migrar pra qualquer framework que vença, da mesma forma que aprender React ensina component-based thinking que vale em Vue/Svelte também. Segunda: DSPy já tem community e integração com Langfuse, Weaviate, e outros produção-tier, o que sugere que a adoção vai crescer antes de qualquer consolidação. O risco de aprender DSPy agora é tempo de setup — não é risco de apostada errada no framework. Se você vai recompilar prompts contra modelos novos mais de uma vez no próximo ano, o investimento já paga.

## Por que existe

Prompt engineering manual é caro (tempo do humano), inconsistente (cada engenheiro com seu estilo) e mal escala (10 prompts × 5 modelos × 3 versões = matriz que explode). Auto-prompt parte da premissa: **se você consegue definir uma métrica de sucesso, dá pra otimizar o prompt em vez de artesanar**.

Analogias úteis (com cautela):

- *Compilador de software*: você escreve em linguagem de alto nível (Signature), compilador gera código de baixo nível (prompt) otimizado pra a target.
- *AutoML*: em vez de tunar hiperparâmetros à mão, você define busca + métrica + dataset, e algoritmo encontra a melhor combinação.

Diferença pro caso de prompt: a "linguagem de alto nível" ainda inclui muita ambiguidade (descrição em PT/EN), e o "compilador" ainda depende de muitos shots da LM. Não é compilação clássica — é otimização orientada por exemplos e eval function.

## DSPy — Signatures, Modules, Compilers

[**DSPy**](https://github.com/stanfordnlp/dspy) (Khattab et al., 2023) é o framework de referência em 2026. Três abstrações centrais:

### Signature — o "tipo" do prompt

Declaração de input/output do passo LM, sem dizer **como** prompted:

```python
import dspy

class SummarizeArticle(dspy.Signature):
    """Resuma um artigo em 3 bullets factuais."""
    article: str = dspy.InputField(desc="texto do artigo")
    summary: list[str] = dspy.OutputField(desc="exatamente 3 bullets factuais")
```

Signature é spec, não prompt. O prompt vai ser gerado/otimizado depois.

### Module — a chamada LM com a signature

Module instancia a Signature numa chamada concreta:

```python
class Summarizer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(SummarizeArticle)

    def forward(self, article: str):
        return self.generate(article=article)

summarizer = Summarizer()
result = summarizer(article="...")
# result.summary = ["bullet 1", "bullet 2", "bullet 3"]
```

O `dspy.ChainOfThought` é um padrão de module que adiciona reasoning antes do output. Outros: `dspy.Predict` (direto), `dspy.ReAct` (com tool use).

### Compiler — otimiza o prompt contra exemplos + eval function

```python
# 1. Dataset com exemplos rotulados (ou só inputs, dependendo do compiler)
trainset = [
    dspy.Example(article="...", summary=["...", "...", "..."]).with_inputs("article"),
    # ... mais exemplos
]

# 2. Eval function — diz quão boa é uma resposta
def evaluate_summary(example, pred, trace=None) -> bool:
    # Pred é o output do module; example é o ground truth
    if len(pred.summary) != 3:
        return False
    # Critério qualquer: cobertura, faithfulness, factualidade...
    return judge_with_llm(article=example.article, summary=pred.summary)

# 3. Compila — testa few-shot variations, escolhe a melhor
from dspy.teleprompt import BootstrapFewShot

teleprompter = BootstrapFewShot(metric=evaluate_summary, max_bootstrapped_demos=4)
compiled_summarizer = teleprompter.compile(summarizer, trainset=trainset)

# 4. Usa compiled como qualquer module — agora com few-shot otimizado
result = compiled_summarizer(article="...")
```

O `BootstrapFewShot` é o compiler mais simples: roda o module sem few-shot no trainset, mantém os casos que passam no eval, usa eles como few-shot. Outros compilers mais sofisticados:

- **MIPRO / MIPROv2** — otimiza instruções **e** few-shot demos via busca bayesiana sobre o espaço de prompts; um dos mais usados em 2026
- **COPRO** — otimiza só a instrução (texto do system) via meta-prompter
- **BootstrapFinetune** — combina prompt otimizado com fine-tune

Diferença prática:

| Compiler | Otimiza | Custo de compilação | Quando |
|---|---|---|---|
| `BootstrapFewShot` | Apenas few-shot demos | Baixo | Start; dataset pequeno |
| `MIPRO`/`MIPROv2` | Instruções + few-shot | Médio-alto | Quando vale investir mais; melhor performance |
| `COPRO` | Apenas instrução | Médio | Quando dataset não tem ground truth pra few-shot |

## Vizinhos do DSPy

### APE — Automatic Prompt Engineer

[Zhou et al., 2023](https://arxiv.org/abs/2211.01910) — APE usa um LLM-meta-prompter pra gerar candidatos de prompt a partir de input/output examples, depois ranqueia os candidatos por eval. Mais simples conceitualmente que DSPy: gera prompt → testa → escolhe melhor.

Pesquisa fundadora; em 2026 a maior parte da implementação prática migrou pra DSPy ou framework similar com primitives mais expressivas.

### OPRO — LLMs as Optimizers

[Yang et al., 2023](https://arxiv.org/abs/2309.03409) — OPRO trata o LLM como otimizador iterativo: o meta-prompt mostra "aqui estão prompts já tentados e seus scores, sugira o próximo". O modelo aprende a partir do histórico do próprio experimento.

Forte em domínios onde o gradient de "o que melhora" é capturável em natural language. Menos usado em produção (custo de iteração + dependência do meta-modelo).

### Promptbreeder

[Fernando et al., 2023](https://arxiv.org/abs/2309.16797) — usa evolução genética sobre população de prompts: mutações (LLM reescreve um prompt), seleção (eval ranqueia), próximo geração. Pesquisa interessante, adoção em produção tímida.

## Quando auto-prompt vence

Cenários onde o trabalho de configurar auto-prompt paga:

| Cenário | Por quê |
|---|---|
| **Pipeline com várias chamadas LM** | Otimizar 5 prompts à mão = 5x o esforço; DSPy otimiza tudo junto contra eval end-to-end |
| **Eval function clara e barata** | BootstrapFewShot precisa rodar eval várias vezes; eval caro = compilação cara |
| **Otimização repetida (modelo novo)** | Mudou de Sonnet pra Opus? Recompila em vez de re-engenheirar 5 prompts à mão |
| **Dataset com ground truth disponível** | Ground truth viabiliza few-shot selection automática |
| **Tolerância pra prompt "feio"** | Compiler pode gerar prompts longos e estranhos; aceitar isso é parte do contrato |

## Quando manual vence

Cenários onde artesanato vence:

| Cenário | Por quê |
|---|---|
| **One-shot alto-risco** | Investir em DSPy pra um prompt = overkill |
| **Edge case que exige judgment** | Compiler otimiza pro caso médio; edge precisa tuning explícito |
| **Eval function frágil ou ausente** | Sem eval, compiler não sabe pra onde otimizar |
| **Restrições de schema rígidas** | Compiler pode adicionar "ruído" no prompt que quebra schema em casos não cobertos pelo eval |
| **Prompt safety-critical** | Cada token do prompt importa; compiler escolher por você é arriscado |
| **Iteração rápida com produto/PM** | Auto-compila é assíncrono; conversa rápida é manual |

## Quando combinar — auto + manual

Em produção real, raramente é puro auto ou puro manual. Pattern recomendado:

```
1. Humano escreve Signature + base prompt + eval function (parte criativa, alto-nível)
2. DSPy compila few-shot e instruções contra eval (parte chata, alto-volume)
3. Humano revisa o prompt compilado, descarta partes problemáticas, ajusta
4. Recompila com a versão revisada como base
5. Promove se eval em produção confirma
```

A humano define o **espaço** (Signature, métrica), o compilador busca **dentro** do espaço.

## Eval function — o ponto mais crítico do setup

Auto-prompt é só tão bom quanto sua eval function. Se eval mede a coisa errada, compiler vai gerar o prompt errado. Princípios:

- **Eval rápido** — vai rodar centenas de vezes durante compilação; segundos importam
- **Eval estável** — variância baixa entre runs
- **Eval cobre o objetivo final** — não otimize só sintaxe; cubra semântica e edge cases
- **Eval bate com métrica de prod** — eval que diverge de métrica de prod = ganha eval, perde prod

Quando ground truth não existe, LLM-as-judge ([[03-Dominios/Tecnologia/IA/Evaluation/04 - LLM-as-judge — quando e como]]) viabiliza eval automatizado pra DSPy. Cuidado: judge enviesado vira prompt enviesado.

## Como DSPy encaixa no ciclo eval → diff → ship

DSPy não substitui o ciclo — ele automatiza **um passo** do ciclo:

```
Ciclo canônico:         Com DSPy:
1. Observability  →     (sem mudança: humano monitora)
2. Eval mede      →     (sem mudança: golden set + judge)
3. Diff (hipótese →     DSPy faz o diff automaticamente:
   vira mudança)        compiler gera candidato vs baseline
4. A/B test       →     (sem mudança: canary ainda é necessário)
5. Ship           →     (sem mudança: champion-challenger decide)
```

O passo 3 era "humano escreve prompt candidato baseado em hipótese". Com DSPy, o passo 3 vira "humano define Signature + trainset, compiler gera candidato". O candidato gerado ainda precisa passar pelo A/B (passo 4) e pelo champion-challenger (passo 5).

O ganho real: em vez de um único candidato por ciclo (custo humano de escrever prompt), DSPy pode gerar e avaliar dezenas de candidatos em paralelo, escolhendo o melhor antes do A/B. Mais candidatos testados = maior chance de encontrar o ótimo no espaço de prompts.

## Estado 2026

Realidade honesta:

- **DSPy é estável e amplamente conhecido** em comunidade de IA, com adoção crescente em pipeline acadêmico e em algumas equipes de produção. Não é "tooling de produção default" como um framework web maduro.
- **Ferramentas competidoras / complementares** estão surgindo (TextGrad, frameworks proprietários de labs); o espaço ainda está se consolidando.
- **Auto-prompt em produção** costuma cobrir partes do pipeline (e.g., compilar few-shot pra uma signature crítica) em vez de todo o sistema.
- **Tradeoff conhecido** — prompts gerados por compiler costumam ser mais longos e menos legíveis que prompts artesanais. Tolerar isso é parte do custo.

A escolha "DSPy ou não" em 2026 é típica de adoção de tecnologia em transição: time pequeno em produto early, manual basta; time que vai recompilar contra modelos novos a cada trimestre, vale aprender DSPy mesmo com overhead inicial.

**DSPy integra com o ecossistema existente:**
- Langfuse: instrumentação de trace + versionamento de prompt compilado
- Weaviate, Qdrant, Pinecone: retrieval DSPy via `dspy.Retrieve` 
- MLflow / Weights & Biases: experimentos de compilação logados pra comparação

**Custo real de compilação:**
Compilar com `BootstrapFewShot` em dataset de 50 exemplos + modelo Sonnet ≈ ~100-200 chamadas de API, custo estimado $2-10 dependendo do modelo e tamanho dos exemplos. `MIPRO` com bayesian search pode ser 5-10x isso. Compensa calcular o custo de compilação antes de incluir num pipeline frequente.

## Anti-padrões

- **DSPy sem eval function** — compiler precisa de métrica; sem ela, gera lixo otimizado
- **Eval function que mede a coisa errada** — compiler diverge da métrica de produção
- **Acoplar DSPy ao código sem fallback pra prompt artesanal** — quando compilação quebra ou modelo muda, sem fallback você fica parado
- **Compilar uma vez e esquecer** — modelo muda, distribuição muda, recompila periodicamente
- **DSPy como prata bala em problema mal definido** — se o objetivo é difícil de medir, DSPy não resolve, agrava
- **Confiar 100% no prompt compilado em prod safety-critical** — humano deve auditar antes de promover
- **Ignorar custo de compilação** — MIPRO com dataset grande + modelo caro = compilação cara

## Armadilhas comuns

> [!warning] Usar DSPy sem eval function — compilar sem métrica é otimizar em direção desconhecida
> DSPy sem eval function é como compilar código sem saber o que o programa deve fazer. O `BootstrapFewShot` sem `metric` vai usar um fallback genérico ou simplesmente não filtrar os few-shots — e você vai promover um prompt "compilado" que ninguém avaliou. A eval function não precisa ser perfeita pra começar; ela precisa ser melhor que nada. Um LLM-as-judge simples que responde "pass/fail" com critério claro já é suficiente pra primeira compilação. A evolução natural é: eval simples (boolean) → eval com score (float 0-1) → eval por dimensão (faithfulness, completeness, format). Não espere a eval perfeita pra começar — compile com a que você tem, mede em prod, calibra.

> [!warning] Tratar o prompt compilado como caixa-preta — e não entender o que foi gerado
> Compiler pode gerar prompts longos, repetitivos, com few-shots questionáveis e linguagem que nenhum humano escolheria. A tentação é "mas funciona no eval" — e promover sem ler. O problema: prompts muito longos têm custo, latência e comportamento inesperado em distribuição diferente do trainset. Além disso, prompts gerados podem ter comportamento emergente (vieses do few-shot, instruções que conflitam) que só aparecem em edge cases. O protocolo mínimo: antes de promover um prompt compilado, ler o prompt gerado inteiramente, rodar manualmente em 5-10 casos variados, e confirmar que o comportamento é o esperado — não só que o score passou.

> [!warning] Compilar uma vez e nunca recompilar — prompt compilado degrada com o tempo
> O prompt compilado foi otimizado contra um modelo específico (e.g., `claude-sonnet-4-5`) com uma distribuição específica de trainset. Quando o modelo do provider atualiza (mesmo minor snapshot), ou quando a distribuição de input muda significativamente, o prompt compilado pode regredir sem que ninguém perceba — porque não tem mecanismo de recompilação periódica. Recompilar não é "refazer do zero" — é rodar o compiler com o mesmo Signature e uma versão atualizada do trainset, que costuma ser rápido se a infrastructure já está montada. Cadência razoável: recompila quando troca de modelo, quando eval score em prod cai abaixo do threshold, ou trimestralmente como manutenção preventiva.

## Como explicar em inglês

**Interview quote:** *"Auto-prompt optimization treats prompts as compiled artifacts rather than handcrafted strings. You declare the task semantics via a Signature — input and output types with descriptions — and a success metric, and the compiler like DSPy's BootstrapFewShot or MIPRO searches the space of few-shot combinations and instructions to find the version that maximizes your metric. The key insight is that if you can measure it, you can optimize it. It pays when you have multiple LM calls in a pipeline, a clear and cheap eval function, and repeated optimization needs — like recompiling against a new model."*

| Português | Inglês |
|---|---|
| Otimização automática de prompt | Auto-prompt optimization |
| Compilador de prompts | Prompt compiler |
| Assinatura de input/output | Signature (input/output declaration) |
| Módulo LM | Language Model module |
| Função de avaliação | Eval function / metric |
| Conjunto de treinamento de exemplos | Training set / trainset |
| Seleção automática de few-shots | Few-shot bootstrapping |
| Otimização de instrução (texto do system) | Instruction optimization |
| Recompilação (modelo ou trainset novo) | Recompilation |
| Prompt compilado vs artesanal | Compiled prompt vs handcrafted prompt |

## O que vem a seguir

Auto-prompt cobre a otimização do diff. A nota 06 fecha um outro ângulo do loop: **capturar o sinal de feedback do usuário** — thumbs up/down, re-prompt rate, abandonment — e transformá-lo em sinal estruturado que alimenta o trainset, o golden set, e as decisões de qual área do pipeline otimizar.

## Fontes

- **Khattab, Singhvi, Maheshwari et al.** — *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines* ([arxiv:2310.03714](https://arxiv.org/abs/2310.03714)). Paper original.
- **DSPy** — [documentação oficial](https://dspy.ai/) e [repositório](https://github.com/stanfordnlp/dspy).
- **Khattab et al.** — *In-Context Learning for Extreme Multi-Label Classification* ([arxiv:2401.12178](https://arxiv.org/abs/2401.12178)). Uso de DSPy em problema concreto.
- **Zhou et al.** — *Large Language Models Are Human-Level Prompt Engineers* (APE, [arxiv:2211.01910](https://arxiv.org/abs/2211.01910)).
- **Yang et al.** — *Large Language Models as Optimizers* (OPRO, [arxiv:2309.03409](https://arxiv.org/abs/2309.03409)).
- **Fernando et al.** — *Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution* ([arxiv:2309.16797](https://arxiv.org/abs/2309.16797)).
- **Opsahl-Ong et al.** — *Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs* (MIPROv2, [arxiv:2406.11695](https://arxiv.org/abs/2406.11695)).
- **Liang et al.** — *HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering* ([arxiv:1809.09600](https://arxiv.org/abs/1809.09600)). Benchmark usado pra avaliar DSPy no paper original.
- **Langfuse** — [*DSPy integration*](https://langfuse.com/docs/integrations/dspy). Como logar traces de compilação DSPy no Langfuse.
- **Omar Khattab** — [*DSPy in production*](https://www.youtube.com/watch?v=41EfOY0Ldkc). Talk de 2024 sobre uso real de DSPy em produto.
- **TextGrad** — [*TextGrad: Automatic Differentiation via Text*](https://textgrad.com/). Abordagem rival/complementar pra auto-otimização de pipeline LLM.

## Veja também

- [[01 - O ciclo eval → diff → ship]] — auto-prompt é uma forma de gerar o diff (passo 3)
- [[02 - A-B testing de prompts]] — compilou um candidato, ainda precisa A/B antes de ship
- [[03-Dominios/Tecnologia/IA/Evaluation/04 - LLM-as-judge — quando e como]] — judge é frequentemente a eval function que DSPy chama
- [[03-Dominios/Tecnologia/IA/Evaluation/02 - Golden datasets — como construir]] — dataset que alimenta o compiler
- [[Prompt Engineering]] — o ofício que auto-prompt automatiza parcialmente
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/12 - Improvement Layer]] — onde auto-prompt entra na camada
- [[06 - Capturando feedback do usuário como sinal]] — fonte do sinal que alimenta o trainset do compiler
- [[03 - Prompt versioning — semver para prompts]] — prompt compilado também precisa de versão semântica
- [[Dicionário de IA#DSPy|Dicionário: DSPy]]
- [[Dicionário de IA#Signature (DSPy)|Dicionário: Signature DSPy]]
- [[Dicionário de IA#Teleprompter|Dicionário: Teleprompter (DSPy)]]
- [[Dicionário de IA#Auto-prompt|Dicionário: Auto-prompt optimization]]
- [[Dicionário de IA#BootstrapFewShot|Dicionário: BootstrapFewShot]]
