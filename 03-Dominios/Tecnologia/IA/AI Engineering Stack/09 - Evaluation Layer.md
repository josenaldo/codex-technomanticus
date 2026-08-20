---
title: "Evaluation Layer"
created: 2026-05-28
updated: 2026-07-06
type: concept
status: seedling
fase: iniciado
tags:
  - ai-engineering-stack
  - ia
  - evaluation
publish: true
aliases:
  - Evaluation Layer
  - Camada de avaliação
---

# Evaluation Layer

> [!abstract] TL;DR
> A Evaluation Layer responde **como saber se o output está bom** — de forma reproduzível, não por intuição. É uma rubrica de múltiplas dimensões (acurácia, completude, utilidade, aderência ao formato, qualidade da fonte) aplicada a um dataset curado. Sem evals, "ficou melhor" vira sentimento; com evals, vira número comparável. A regra que separa sistemas maduros de demos: o sistema que itera com sinal melhora. O que itera no escuro não sabe se está melhorando ou piorando.

> [!question]- Como você sabe se uma mudança no sistema melhorou ou piorou?
> Sem evals, a resposta é: você não sabe. Você tem impressões, você tem feedback de dois colegas, você tem o instinto do PM. Em produção com milhares de chamadas por dia, isso é como navegar um navio sem instrumentos — você sente que está indo na direção certa até bater nos recifes. A Evaluation Layer é o painel de instrumentos que transforma "parece melhor" em "melhorou X% na dimensão Y sem regredir em Z".

## O problema que a Evaluation Layer resolve

Você mudou o system prompt. O modelo parece responder melhor. Você mostra para dois colegas — um acha que melhorou, o outro acha que piorou. Como você decide?

Sem a Evaluation Layer, a resposta é: por intuição, por votação, ou pela opinião do stakeholder mais vocal na reunião. Isso funciona para um protótipo com 10 casos de uso testados manualmente. Não funciona para um sistema em produção com 10.000 chamadas por dia e 200 tipos de input diferentes.

A Evaluation Layer cria o **sinal** que permite iterar com objetividade. Sem ela, você não sabe se uma mudança de modelo, prompt ou retrieval melhorou ou piorou a qualidade do sistema. Com ela, você tem um número: a mudança moveu o score de 3.2 para 3.7 nas métricas que importam para o negócio, e não regrediu em nenhuma das condições de falha automática.

## Sem Evaluation Layer vs com Evaluation Layer

```mermaid
flowchart LR
    subgraph "Sem Evaluation Layer"
        A1["Mudança no sistema\n(prompt/modelo/retrieval)"]
        A2["Teste manual\npor 2-3 pessoas"]
        A3["Deploy baseado\nem intuição"]
        A4["Regressão detectada\nem produção tarde"]
    end

    subgraph "Com Evaluation Layer"
        B1["Mudança no sistema\n(prompt/modelo/retrieval)"]
        B2["Regression eval\nno PR (automático)"]
        B3["Score comparado\ncom baseline"]
        B4["Deploy com sinal\nde qualidade verificado"]
    end

    A1 --> A2 --> A3 --> A4
    B1 --> B2 --> B3 --> B4

    style A4 fill:#fff5f5,stroke:#ff6b6b
    style B4 fill:#f0fff4,stroke:#51cf66
```

## O que é esta camada

A Evaluation Layer é a **régua** do sistema — mede qualidade do output de forma reproduzível para que mudanças possam ser comparadas com objetividade.

Template mínimo (adaptado do thread @hooeem):

```yaml
evaluation:
  success_criteria: "<herda do Purpose Layer — traduzido em dimensões mensuráveis>"
  scoring_rubric:
    accuracy: "1-5: alinhamento factual com fontes verificáveis"
    completeness: "1-5: todas as partes da pergunta foram respondidas"
    usefulness: "1-5: o output é acionável para o usuário-alvo"
    format_adherence: "1-5: segue o contrato definido na Output Layer"
    source_quality: "1-5: fontes citadas são adequadas e verificáveis"
    specificity: "1-5: resposta concreta, não genérica"
    risk_control: "1-5: sem conteúdo proibido ou potencialmente prejudicial"
  pass_threshold: "média ≥4 E nenhuma dimensão <3"
  automatic_failure_conditions:
    - "vazamento de PII"
    - "chamada de tool proibida pela Guardrail Layer"
    - "formato de output inválido (breaking change no schema)"
```

Três tipos de eval se complementam: **(a) reference-based** — compara com ground truth (bom para Q&A com resposta conhecida); **(b) reference-free** — checa propriedades intrínsecas do output (bom para verificar formato, tom, ausência de PII); **(c) LLM-as-judge** — outro modelo aplica a rubrica (bom para dimensões qualitativas em escala).

## Decisões-chave

**1. Dataset de eval é o fundamento.** Sem dataset, não há eval — só impressão. Comece com 20-50 exemplos curados manualmente, cobrindo casos fáceis, médios, difíceis, edge cases e regressões conhecidas (casos que já falharam em produção). O dataset cresce com cada incidente real: todo output problemático reportado em produção vira um caso no dataset de regressão.

**2. Rubrica com definições operacionais.** "Acurácia: 4" tem que significar a mesma coisa quando dois avaliadores diferentes aplicam a rubrica. Definições vagas degeneram para "achismo escala 1-5". Cada ponto da escala precisa de um descritor específico: "4 = informação correta com uma imprecisão menor que não afeta a conclusão".

**3. LLM-as-judge exige calibração.** Usar outro LLM para aplicar a rubrica é poderoso para escalar evals além do que revisão humana consegue cobrir — mas exige calibração contra humano em uma amostra representativa. Sem calibração, você tem dois modelos concordando entre si, não dois avaliadores chegando ao mesmo critério.

**4. Automatic failure conditions como ponte com Guardrail.** Condições que zeram a nota total — PII exposto, tool proibida chamada, schema quebrado — são o link formal entre Evaluation Layer e Guardrail Layer. Uma `automatic_failure_condition` na Evaluation é um guardrail de qualidade; se acontece com frequência, vira um guardrail de prevenção.

**5. Frequência: CI/CD de evals.** Eval que roda só "no final do projeto" não dá sinal útil. O padrão de maturidade: regression eval em cada PR (30-50 casos rápidos para checar que nada regrediu) + full eval semanalmente + live eval amostral em produção (amostragem de 1-5% dos outputs reais para monitoramento contínuo).

## Casos práticos

### Cenário 1 — O sistema que "melhorou" mas não melhorou

Time atualiza o system prompt de um assistente de redação. Avaliação manual por dois membros: ambos acham melhor. Lançam em produção. Duas semanas depois, a métrica de "usuário editou a resposta antes de usar" subiu de 40% para 65% — o sistema piorou para os usuários.

O problema: avaliação manual por dois revisores é uma amostra de tamanho 2 em 10.000 outputs. Os dois casos que avaliaram eram fáceis; os casos difíceis — onde o sistema regrediu — não foram testados.

Com a Evaluation Layer: dataset de regressão com 80 casos (incluindo os casos difíceis históricos), rubrica com dimensão "especificidade" (que a mudança de prompt degradou), regression eval no PR. A mudança teria sido bloqueada antes do lançamento.

### Cenário 2 — LLM-as-judge em escala

Sistema de suporte técnico que recebe 5.000 tickets por dia. Revisão humana de 1% = 50 casos/dia — suficiente para calibração, insuficiente para detectar degradação estatística.

Solução: rubrica definida pela equipe, calibrada contra 200 casos com avaliação humana (acordo inter-avaliador ≥80%). LLM-as-judge aplica a rubrica em 100% dos tickets (500 por hora, custo marginal baixo). Dashboard mostra scores por dimensão, por tipo de ticket, por horário. Alertas disparam quando qualquer dimensão cai >10% vs semana anterior.

A calibração é o que valida o judge. Sem ela, o dashboard seria um número que ninguém confia.

### Cenário 3 — Avaliação de um sistema RAG

Sistema de busca corporativa: usuário pergunta em linguagem natural, o sistema recupera trechos de documentos internos e o modelo gera a resposta com base neles. A rubrica genérica (acurácia, completude) não captura o problema mais comum desse tipo de sistema: **a resposta pode estar bem escrita e ainda assim inventar algo que não está nos documentos recuperados**, ou recuperar os documentos errados e gerar uma resposta boa para a pergunta errada.

RAG tem uma falha em duas camadas — retrieval e geração — e por isso a eval precisa medir as duas separadamente. Avaliar só a resposta final mistura os dois problemas: uma resposta ruim pode ser culpa do retrieval (documento certo nunca chegou ao contexto) ou da geração (documento certo chegou, mas o modelo ignorou ou distorceu). Três métricas cobrem essa distinção:

- **Recall@k** — dos documentos relevantes que existem na base, quantos apareceram entre os top-*k* recuperados? Mede a camada de retrieval isoladamente: se o recall@5 é 60%, quatro em cada dez perguntas nunca tiveram o documento certo nem chegando ao modelo — nenhuma melhora de prompt resolve isso, o problema é no índice ou no retriever.
- **Faithfulness** (fidelidade) — a resposta gerada está sustentada pelo contexto recuperado, ou o modelo alucinou algo que não está lá? Mede a camada de geração: mesmo com o documento certo recuperado, o modelo pode extrapolar, generalizar demais ou inventar um detalhe que soa plausível.
- **Answer relevance** (relevância da resposta) — a resposta responde à pergunta feita, mesmo que factualmente correta? Um sistema pode ser fiel ao contexto (não alucina) e mesmo assim devolver uma resposta correta mas tangencial, que não resolve o que o usuário perguntou.

```yaml
evaluation_rag:
  retrieval:
    metric: "recall_at_k"
    k: 5
    pass_threshold: 0.85
    calculo: "documentos_relevantes_recuperados / total_documentos_relevantes_na_base"
  generation:
    faithfulness:
      metric: "faithfulness_score"
      metodo: "llm_as_judge"
      pass_threshold: 0.9
      pergunta_ao_judge: "cada afirmação da resposta está sustentada por um trecho do contexto recuperado?"
    answer_relevance:
      metric: "answer_relevancy_score"
      metodo: "llm_as_judge"
      pass_threshold: 0.8
      pergunta_ao_judge: "a resposta resolve a pergunta original, ou é tangencial?"
  automatic_failure_conditions:
    - "resposta cita fonte que não está entre os documentos recuperados"
    - "recall@5 < 0.5 na amostra (falha sistêmica de retrieval, não pontual)"
```

Diagnóstico prático: se o recall@k está baixo, o problema é de indexação/chunking/embedding — mexer no prompt de geração não ajuda. Se o recall@k está alto mas a faithfulness está baixa, o problema é o modelo ignorando o contexto — o retrieval está fazendo o trabalho dele, a geração não. Separar as métricas por camada é o que evita a armadilha de "aumentar o *k*" (recuperar mais documentos) quando o problema real era o modelo alucinando em cima do que já tinha.

Exemplo concreto: recall@5 em 0.92 (o retrieval quase sempre traz o documento certo) e faithfulness em 0.55 significam que o time deveria investigar o prompt de geração e o comportamento do modelo diante do contexto — não gastar tempo trocando de embedding model ou reindexando a base, porque o retrieval já está funcionando.

## Armadilhas comuns

> [!warning] Lançar sem dataset de eval
> "Vamos criar o dataset depois de ver os primeiros dados reais" é a armadilha mais comum. Sem dataset, você não tem baseline para comparar; sem baseline, você não sabe se os dados reais representam melhora ou degradação. O dataset mínimo viável — 20-50 casos curados à mão — deve existir antes do primeiro lançamento em ambiente compartilhado.

> [!warning] Rubrica sem definições operacionais
> "Utilidade: 1-5" sem descritor por ponto é "opinião: 1-5". Dois revisores vão dar notas diferentes para o mesmo output porque "utilidade" significa coisas diferentes para eles. O esforço de escrever os descritores antes de avaliar os primeiros casos é o que transforma a rubrica em métrica comparável.

> [!warning] LLM-as-judge sem calibração
> Usar GPT-4 para avaliar outputs de Claude (ou vice-versa) sem calibração contra avaliação humana é transferir o viés do judge para a métrica. Modelos têm viés em direção ao seu próprio estilo de output. Calibre o judge contra humano antes de confiar no número que ele produz.

## Como montar o dataset mínimo viável

O maior bloqueio na prática não é a rubrica — é "de onde vêm os exemplos do dataset?". Resposta em três passos:

**Passo 1 — Colete casos da fase de design.** Antes de ter dados reais, você tem a definição do propósito do sistema (Purpose Layer). Liste os 10-15 casos de uso mais frequentes que o sistema deve resolver. Escreva 2-4 exemplos por caso de uso — input + output esperado ou critérios de avaliação.

**Passo 2 — Adicione casos difíceis e edge cases.** Para cada caso de uso principal, adicione ao menos um caso que está no limite do escopo ("não sei" esperado), um caso ambíguo, e um caso que parece fácil mas tem um gotcha. Esses são os casos que vão revelar regressões quando o sistema mudar.

**Passo 3 — Alimente com incidentes reais.** Cada vez que um output problemático chega da produção: capture o input, o output ruim, e anote o que deveria ter sido diferente. Esse caso entra imediatamente no dataset de regressão. Com o tempo, o dataset vira a memória histórica de falhas do sistema — e cada rodada de evals garante que esses erros não se repitam.

> [!info] 20 casos bem curados > 200 casos aleatórios
> Dataset de qualidade vem de seleção deliberada, não de volume. Um dataset com 20 casos representando as dimensões críticas do sistema dá sinal mais confiável do que 200 outputs de produção aleatórios sem curadoria.

## Tipos de eval e quando usar cada um

Cada tipo de eval tem força em domínios diferentes. Na prática, um sistema maduro usa os três em combinação:

**Reference-based eval:** você tem a resposta certa. Usado para Q&A sobre documentação interna, extração de informação de contrato, classificação de intent onde o label existe. Alta objetividade, mas exige ground truth — o que nem sempre é viável.

Exemplo de caso no dataset (extração de campos de um contrato, com ground truth conhecido):

```json
{
  "id": "contract-extraction-042",
  "input": "Extraia parte contratante, valor e prazo do contrato anexo.",
  "expected_output": {
    "parte_contratante": "Acme Ltda.",
    "valor": "R$ 45.000,00",
    "prazo": "12 meses"
  },
  "match_type": "exact_field",
  "tolerance": {
    "valor": "aceita variação de formatação (R$45000 == R$ 45.000,00)"
  }
}
```

A métrica é objetiva porque existe um gabarito: o output é comparado campo a campo contra `expected_output`, sem depender de julgamento subjetivo sobre "o quão boa" a resposta é.

O campo `tolerance` no exemplo acima existe porque "igual" nem sempre é igualdade de string — "R$45000" e "R$ 45.000,00" são o mesmo valor com formatação diferente. Reference-based sem tolerância vira frágil: qualquer variação cosmética no formato conta como erro, inflando falsos negativos.

Esse cuidado — decidir o que conta como "acertou" — é parte do desenho do dataset, não um detalhe de implementação a ser resolvido depois.

**Reference-free eval:** você checa propriedades do output sem saber a resposta certa. Formato válido (JSON parseable, campos obrigatórios presentes), ausência de PII, comprimento dentro do range esperado, linguagem detectada. Automatizável por código, sem custo de model.

Exemplo de regra reference-free (checagem de schema e PII, sem precisar saber qual é a "resposta certa"):

```yaml
check: "formato_e_seguranca"
output_type: "json"
rules:
  - schema_valido: true          # JSON parseia e tem os campos obrigatórios
  - campos_obrigatorios:
      - "resposta"
      - "fontes"
  - ausencia_de_pii: true        # regex/NER não detecta CPF, e-mail, telefone
  - comprimento_max_tokens: 500
  - idioma_detectado: "pt-BR"
falha_automatica_se: "qualquer regra acima falhar"
```

Note a diferença estrutural: aqui não existe `expected_output` — a checagem é sobre propriedades do output em si (parseia? tem PII? está no idioma certo?), não sobre acertar um valor específico. É por isso que reference-free eval é barato de escalar: roda 100% do tráfego, sem custo de modelo, porque é só código validando forma.

**LLM-as-judge:** um modelo aplica a rubrica em escala. Poderoso para dimensões qualitativas (utilidade, clareza, tom). Exige: (a) prompt de judge bem especificado com a rubrica completa e definições por ponto; (b) calibração contra avaliação humana em amostra representativa para validar que o judge e humanos concordam; (c) monitoramento de deriva — o judge também pode mudar com atualizações de modelo.

## Ferramentas de eval

A rubrica e o dataset são o desenho; a ferramenta é o que roda isso em CI/CD e mantém o histórico comparável entre execuções. Nenhuma ferramenta substitui o trabalho de definir dataset e rubrica — elas só automatizam a execução, o versionamento e a visualização dos resultados.

Pergunta que costuma aparecer em entrevista técnica: "por que não escrever isso em uma planilha e rodar um script?" Dá para começar assim — e muitos times começam. O que a ferramenta especializada resolve, à medida que o sistema cresce, é o histórico comparável (versão N vs versão N-1 do mesmo caso), a integração nativa com CI/CD (falhar o build automaticamente) e o dashboard compartilhado entre quem escreve prompt e quem revisa qualidade.

**Braintrust** — plataforma focada em avaliação e experimentação para times de produto. Registra cada "experimento" (uma rodada de eval contra uma versão do sistema) e compara score a score contra o baseline anterior, caso a caso. O diferencial é o *diffing* visual: você vê exatamente quais casos do dataset pioraram e o output completo do antes/depois, não só um número agregado. Bom fit quando o time quer decidir "posso lançar essa mudança de prompt?" com base em regressão caso a caso, não só média.

**PromptFoo** — ferramenta open-source, config-driven (YAML), pensada para rodar como um linter de prompts dentro do CI/CD. Você declara os casos de teste, os "asserts" (regras reference-free, similaridade semântica, ou chamada a um LLM-as-judge) e o PromptFoo roda a matriz de prompts × modelos × casos, falhando o build se o score cair abaixo do threshold. Encaixa naturalmente no fluxo "regression eval em cada PR" descrito nas Decisões-chave, porque é CLI-first e não exige um serviço externo rodando.

**LangSmith** — parte do ecossistema LangChain, mas usável com qualquer stack. Foco em observabilidade + eval integrados: cada trace de execução do sistema (chamadas de modelo, tool calls, retrieval) pode virar automaticamente um caso de dataset, e o eval roda sobre o histórico real de produção, não só sobre casos curados manualmente. Bom fit quando o sistema já usa LangChain/LangGraph e o time quer eval e logging na mesma superfície (ver [[11 - Logging Layer]]).

**Ragas** — biblioteca especializada em avaliação de sistemas **RAG**. Implementa como código pronto as métricas que, feitas à mão, exigiriam reimplementar cálculo de recall, precision e detecção de alucinação contra o contexto recuperado: `faithfulness`, `answer_relevancy`, `context_precision`, `context_recall`. Ragas não substitui a rubrica de negócio (utilidade, tom) — ele cobre especificamente a fatia RAG do sistema, e por isso costuma aparecer combinado com Braintrust/PromptFoo/LangSmith, que cobrem o resto do pipeline.

> [!info] A ferramenta não escolhe por você — o dataset e a rubrica escolhem a ferramenta
> Um time com sistema RAG maduro tipicamente combina duas peças: Ragas para as métricas de retrieval (recall@k, faithfulness) e PromptFoo ou Braintrust para a rubrica de negócio (utilidade, tom, aderência ao formato) rodando em CI/CD. Escolher a ferramenta antes de ter dataset e rubrica definidos é resolver o problema errado primeiro.

| Ferramenta | Foco principal | Onde encaixa melhor |
|---|---|---|
| Braintrust | Diffing caso a caso entre versões | Decidir "posso lançar essa mudança?" com regressão visual |
| PromptFoo | Config-driven (YAML), CLI-first | Regression eval automatizado dentro do CI/CD, por PR |
| LangSmith | Observabilidade + eval na mesma superfície | Stacks já em LangChain/LangGraph; trace vira caso de dataset |
| Ragas | Métricas específicas de RAG | Recall@k, faithfulness, answer relevance de sistemas de retrieval |

## Como explicar em inglês

The Evaluation Layer is the measurement system of the AI stack. It defines how to determine whether the system's output is good — through a scoring rubric applied to a curated dataset, not through intuition or manual spot-checks. The key insight: teams that iterate with evaluation scores improve predictably; teams that iterate by gut feel don't know whether they're improving or degrading. The three types of eval — reference-based, reference-free, and LLM-as-judge — complement each other. LLM-as-judge scales quality assessment beyond what human review can cover, but only after calibration against human judgment.

Think of it as the difference between a pilot flying by feel versus flying with instruments. Both might make it on a clear day — but only the pilot with instruments can fly in fog, hand off to another pilot, or know exactly what went wrong when something goes wrong. The Evaluation Layer is the instrument panel for your AI system.

In interviews, the signal question is usually: "how would you evaluate whether your system is working?" A weak answer describes manual review. A strong answer describes a rubric with specific dimensions tied to the purpose of the system, a dataset strategy (including how you collect cases from production incidents), and the role of LLM-as-judge versus reference-based eval for different types of outputs.

> *"Evals are not about catching every bug — they're about making sure you know when your system is getting better or worse."* — Eugene Yan, Evals are all you need

| PT | EN |
|----|----|
| Camada de avaliação | Evaluation Layer |
| Rubrica de avaliação | Scoring rubric |
| Conjunto de dados de avaliação | Evaluation dataset |
| LLM como juiz | LLM-as-judge |
| Avaliação de referência | Reference-based evaluation |
| Avaliação sem referência | Reference-free evaluation |
| Avaliação de regressão | Regression evaluation |
| Condição de falha automática | Automatic failure condition |
| Limiar de aprovação | Pass threshold |
| Acordo inter-avaliador | Inter-rater agreement |

## O que vem a seguir

A Evaluation Layer mede qualidade — mas medir não previne. Para o sistema parar ativamente antes de produzir output prejudicial, a próxima camada é a **Guardrail Layer**: checks determinísticos que interceptam input, output e tool calls por código, independentemente do que o modelo decidiu gerar.

Depois de Evaluation e Guardrail, a Logging Layer fecha o bloco de controle: registra tudo que passou pelas duas para que o Improvement Loop tenha dados para trabalhar.

- [[10 - Guardrail Layer]] — o que o sistema não pode fazer (imposição por código)
- [[Evaluation]] — trilha completa: datasets, LLM-as-judge, métricas por tipo de sistema

## Onde aprofundar

- **[[Evaluation]]** — trilha completa dedicada (8 notas).
- **[[Anatomia de Agents]]** → [[09 - Evaluation de agents]] — particularidades quando o sistema é agentic.
- **[[RAG e Vector Databases]]** → [[09 - Evaluation de RAG]] — recall, precision@k, faithfulness.

## Veja também

- [[02 - Purpose Layer — o que o sistema é]] — `success_criteria` descem daqui
- [[05 - Output Layer]] — a rubrica aplica sobre o que sai do modelo
- [[10 - Guardrail Layer]] — `automatic_failure_conditions` são guardrails de qualidade
- [[11 - Logging Layer]] — scores de eval entram nos logs para análise

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 8 (Evaluation layer template). X/Twitter, 2025.
- **Eugene Yan** — [*Evals are all you need*](https://eugeneyan.com/writing/evals/). Argumento por evals como vantagem competitiva sustentável.
- **Hamel Husain** — [*Your AI product needs evals*](https://hamel.dev/blog/posts/evals/). Guia prático de como começar com dataset mínimo.
