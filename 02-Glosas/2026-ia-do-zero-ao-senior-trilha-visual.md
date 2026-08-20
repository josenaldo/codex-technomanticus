---
title: "IA do Zero ao Sênior — Trilha Completa (board Excalidraw)"
aliases: ["IA do Zero ao Sênior", "Trilha Gabriel Dias"]
source: https://app.excalidraw.com/l/8JV6z3OmEvu/8GgtBGSpQGS
author: Gabriel Dias
site: Excalidraw+ (workspace GabrielOnRails)
published: 2026
read: 2026-08-16
type: glosa
progress: in_progress
status: lido
tags: [ia, trilha, pedagogia, eval, prompt-injection, abstencao, roadmap-90-dias, material-visual]
lang: pt-BR
publish: false
---

# IA do Zero ao Sênior — Trilha Completa (Gabriel Dias)

> [!info] Sobre esta glosa
> Fichamento de um board Excalidraw público com 36 quadros (34 aulas + mapa + biblioteca), de autoria de **Gabriel Dias** ([linkedin.com/in/gabriel-tech](https://linkedin.com/in/gabriel-tech) · [github.com/GabrielOnRails](https://github.com/GabrielOnRails)). O conteúdo integral é dele; aqui ficam apenas as teses, os números e os links, em forma condensada, para servir de material de comparação com o domínio [[03-Dominios/Tecnologia/IA/index|IA]] do Codex. Acesso ao original é por sala colaborativa read-only do Excalidraw+.

## TL;DR

Trilha visual de 34 aulas em 6 módulos, desenhada para levar alguém de "não sei nada" até "constrói e mede" — o autor declara explicitamente que o teto é o **nível 2 (constrói e mede)**, e que nível 3 (arquitetura em produção) está fora do escopo. O valor do material para o Codex não está na cobertura, que é menor que a do domínio IA, e sim em três decisões pedagógicas: **todo conceito fecha com um exemplo numérico**, a espinha organizadora é **maturidade** (entender → conversar → construir → confiar → sênior → profissional) em vez de assunto, e o fecho é um **roadmap de 90 dias com entrega obrigatória** a cada 30 dias, não com leitura.

## A estrutura em 6 módulos

| Módulo | Nome | Aulas | O corte |
| --- | --- | --- | --- |
| 1 | Como a máquina funciona | 1.1 a 1.8 | mecânica do LLM, do token à janela |
| 2 | Conversar com a máquina | 2.1 a 2.6 | prompt como especificação |
| 3 | Construir com a máquina | 3.1 a 3.8 | API, custo, tools, agente, MCP, RAG |
| 4 | Confiar na máquina | 4.1 a 4.5 | eval, judge, tracing, injection, abstenção |
| 5 | Nível sênior | 5.1 a 5.6 | as decisões de trade-off |
| 6 | Virar profissional | 6.1 a 6.2 | roadmap de 90 dias + biblioteca |

Anatomia fixa de cada quadro: título, tese de uma linha, 3-4 blocos conceituais, **caixa amarela com o exemplo concreto**, rodapé azul com material externo gratuito, rodapé cinza com navegação anterior/próxima/mapa.

## Módulo 1 — Como a máquina funciona

- **1.1 IA, ML, Deep Learning, LLM** — quatro caixas, uma dentro da outra. IA preditiva mora nas caixas 2-3; LLM é IA generativa. Material: Karpathy, *Intro to Large Language Models*.
- **1.2 Token: a unidade que se paga** — regra de bolso: 1 token ≈ 4 caracteres ≈ 0,75 palavra em inglês; **em português, 1,5 a 2 tokens por palavra** (o mesmo texto custa mais em PT que em EN). Saída custa ~4x a entrada. O caso "quantos R tem em morango" não é burrice: é falta de olho para caractere. Material: tiktokenizer.
- **1.3 Embedding: sentido vira número** — `vetor(rei) − vetor(homem) + vetor(mulher) ≈ vetor(rainha)`; similaridade de cosseno; 768 a 3.072 dimensões. Exemplo: "cancelar assinatura" vs artigo "Encerramento de plano" — busca por palavra-chave dá zero, embedding dá cosseno 0,89. Material: Jay Alammar, *The Illustrated Word2vec*.
- **1.4 Prever a próxima palavra** — não existe banco de respostas, existe distribuição de probabilidade num loop autoregressivo. Cada palavra lida é uma passada inteira pela rede.
- **1.5 Attention: a ideia de 2017** — Q/K/V como três perguntas por palavra. Antes (RNN/LSTM) lia em ordem e esquecia o começo; depois, olha tudo ao mesmo tempo e **paraleliza**, que foi o que destravou a escala. Material: 3Blue1Brown, *Attention in transformers*.
- **1.6 Pré-treino, SFT e RLHF** — as três fases e o que cada uma resolve. O exemplo bom: um base model perguntado "qual é a capital da França?" responde *"Qual é a capital da Alemanha? Qual é a capital da Itália?"* — ele completa a lista. Depois de SFT+RLHF: "Paris". **O conhecimento era idêntico; mudou o comportamento.** Material: Karpathy, *Deep Dive into LLMs*.
- **1.7 Temperatura e alucinação** — 0 para extração/classificação/JSON, 0,7 padrão de conversa, 1,2+ só brainstorm. A tese forte: *"alucinação não é bug, é o objetivo de treino funcionando como foi projetado"* — o modelo não tem o estado "não sei", e a distribuição sempre existe. Os 5 antídotos: grounding, citação conferível, autorizar o "não sei", validar em código o que é validável, temperatura 0 em tarefa factual. Exemplo: 3 referências acadêmicas pedidas, 2 existiam, a terceira tinha autor real, revista real e DOI bem formado — *"a resposta falsa tem exatamente o mesmo formato da verdadeira"*. Material: Lilian Weng, *Extrinsic Hallucinations in LLMs*.
- **1.8 Janela de contexto** — a API é stateless, tudo é reenviado a cada chamada. *Lost in the middle*: começo e fim pesam mais, instrução crítica vai no fim. **"Contexto é RAM, não HD."** Calibração: 200k tokens ≈ 150k palavras ≈ 2 livros; 1M ≈ 10 livros. A pergunta certa nunca é "cabe?", é "o que precisa estar aqui para esta tarefa?".

## Módulo 2 — Conversar com a máquina

- **2.1 Anatomia de um prompt** — seis blocos sempre na mesma ordem: papel/contexto, tarefa, regras/limites, exemplos, formato da saída, dado de entrada (por último, dentro de tag — *é dado, não instrução*). **Regra de ordem que quase ninguém sabe:** prompt normal = instrução primeiro, dado por último; documento longo (acima de ~10 mil tokens) = documento primeiro, pergunta no fim, porque o fim da janela pesa mais.
- **2.2 System, user, assistant** — system é lei, user é o pedido do turno, assistant é onde cabe o **prefill** (escrever no lugar do modelo para forçar o começo da resposta: `{` empurra para JSON, `1.` empurra para lista — "é controle grátis"). Bug clássico: pôr "responda sempre em português" na primeira mensagem do usuário; funciona 3 turnos e some no turno 12, porque era sugestão perdida no histórico, não lei.
- **2.3 Few-shot** — sweet spot em 3 a 5 exemplos; 20+ tem retorno decrescente e custo crescente. Escolha do exemplo: cubra o caso difícil, use o formato exato de volta, inclua um caso ambíguo, **nunca deixe dois exemplos se contradizerem**. Se a regra diz 3 bullets e o exemplo tem 5, *o exemplo ganha, sempre*. Exemplo: classificação de ticket, zero-shot ~71% (e inventava categoria fora da spec), com 3 exemplos ~94% — custo do ganho: 40 minutos, zero linha de código.
- **2.4 Chain-of-thought e reasoning** — o modelo pensa escrevendo; cada token gerado é computação a mais que volta ao contexto. **Não use** em classificar/extrair/traduzir/formatar, nem quando latência ou custo importam. Exemplo: R$ 120 com 15% de desconto e depois 10% de cashback — direto o modelo junta os percentuais e erra; passo a passo, acerta.
- **2.5 Saída estruturada (JSON)** — "o momento em que o prompt deixa de ser conversa e vira contrato de API". Schema garante forma, não garante verdade — valide com Zod/Pydantic mesmo assim. Dois campos que salvam: `confianca` e `nao_encontrado`. Armadilha: `max_tokens` curto corta o JSON no meio. Exemplo: extração de nota fiscal, texto livre + regex ~82% com layout novo quebrando todo mês; schema + validação ~97%, e **o ganho maior não foi a precisão, foi passar a falhar de forma visível**.
- **2.6 Os 7 anti-padrões** — pedir sem contexto; só dizer o que não fazer; prompt gigante sem estrutura; exemplo que contradiz a regra; delegar o que é tarefa de código (contar, somar, data de hoje, câmbio); acreditar em "seja preciso" (*"adjetivo não é instrução; 'não alucine' não faz efeito nenhum"*); prompt não versionado (*"isso não é sistema, é sorte"*). Bônus: pedir 5 coisas num turno só.

## Módulo 3 — Construir com a máquina

- **3.1 Primeira chamada de API** — 4 erros de estreante: chave no código; esquecer que a API é stateless; não tratar 429/529 com backoff exponencial; chamar direto do frontend. Projeto sugerido: script que lê os títulos das PRs da semana e escreve o resumo da sprint.
- **3.2 Custo, latência e cache** — `custo = (tokens_entrada × preço_entrada) + (tokens_saída × preço_saída)`, saída ~4x. TTFT vs total; *"streaming não deixa mais rápido, deixa mais rápido de perceber"*. **Ordem do prompt para o cache acertar:** estático primeiro (system + tools + exemplos + documento base), dinâmico no fim (pergunta + dados do turno). Inverter isso significa pagar preço cheio em toda chamada.
- **3.3 Escolher o modelo certo** — *"benchmark não é a sua tarefa; o modelo certo é o menor que passa no seu teste"*. Processo em 4 passos: 20 casos reais com gabarito → rodar nos 3 candidatos → comparar acerto, custo por caso e latência p95 na mesma tabela → ficar com o menor que passa. Armadilhas: leaderboard mede a tarefa dele; deixe o nome do modelo em configuração, nunca no código; testar 3 exemplos no chat é impressão, não avaliação. Exemplo: classificador com 200k chamadas/mês, topo de linha ~96% vs modelo pequeno com 5 exemplos ~94% a uma ordem de grandeza menos — *"a resposta vem do produto, nunca do benchmark"*.
- **3.4 Tool use** — *"o modelo não executa nada; ele pede, e o seu código decide se atende"*. **A descrição da ferramenta é prompt**: diga o que faz, quando usar, quando NÃO usar, o que retorna. 5 ferramentas bem descritas valem mais que 30 confusas. Segurança: trate a saída do modelo como input de usuário anônimo; ação irreversível precisa de confirmação explícita e teto.
- **3.5 O loop agêntico** — "a diferença entre chatbot e agente cabe dentro de um while". Os 5 ingredientes: objetivo claro, ferramentas, memória do que já foi feito, **critério de parada explícito** e **limite de passos e de custo** — *"sem o 4 e o 5 você não tem agente: tem loop infinito com cartão de crédito cadastrado"*. Não use agente quando o fluxo é fixo.
- **3.6 MCP** — 3 assistentes × 5 sistemas = 15 integrações vira 5 servidores. As 3 primitivas: tools, resources, prompts. (O próprio board foi desenhado por um agente via MCP do Excalidraw.)
- **3.7 RAG** — indexação offline + consulta por pergunta. A frase que resume: **"RAG não é busca, é montagem de contexto"** — você não procura um documento para o usuário ler, escolhe o que entra na janela. Por que em vez de fine-tuning: atualiza na hora, dá citação, respeita permissão.
- **3.8 Por que o seu RAG é ruim** — os 5 defeitos e a **ordem de ataque: chunking → híbrido → rerank → contexto**. (1) chunking burro — corte por seção/parágrafo com 10-15% de sobreposição; (2) só busca vetorial — embedding erra em código, sigla, SKU, nome próprio; use BM25 + vetor; (3) sem rerank — passe 20 pelo reranker, mande 5; (4) chunk que não se explica — *contextual retrieval*, prefixe cada pedaço com uma linha que o situa; (5) nenhuma medição — meça `recall@k`, porque se o trecho certo não está entre os k, não existe prompt que salve. Exemplo: recall@5 de 38% → ~85% sem mudar uma vírgula do prompt. *"Quando o RAG erra, o culpado quase nunca é o modelo. É a recuperação."*

## Módulo 4 — Confiar na máquina

O módulo que mais interessa ao Codex, porque agrupa por **maturidade** cinco coisas que no vault estão em galhos separados.

- **4.1 Eval: o gargalo real** — *"sem medir, você não faz engenharia de IA; faz aposta com data de entrega"*. Primeiro dataset: **30 casos** = 20 reais + 5 de borda + 5 que NÃO deveriam ser respondidos, em três colunas (entrada, saída esperada, **por que este caso existe**). Um CSV resolve. Medir: acerto, taxa de formato inválido, taxa de afirmação sem fonte, custo por caso, latência p95 — tudo na mesma tabela, uma linha por versão. Os 3 erros que matam: dataset sintético bonito, medir só o caminho feliz, rodar uma vez e nunca mais (*"eval é CI, não é relatório"*). Material: Hamel Husain, *Your AI product needs evals*.
- **4.2 LLM-as-judge** — a rubrica é o segredo: critério vago = juiz aleatório, critério observável = juiz reprodutível. Vieses assumidos: posição, verbosidade, self-preference. Mitigação: comparar A vs B em vez de nota absoluta, alternar a ordem, **pedir a justificativa ANTES da nota**. Calibração: rotule 30 casos à mão, meça concordância; abaixo de 80% o problema é a rubrica. *"Juiz não calibrado é pior do que nenhum: entrega número errado com aparência de rigor científico."* O uso certo é triagem em escala, não veredito final. Material: Eugene Yan, *LLM-evaluators*.
- **4.3 Tracing** — *"quando o agente erra, você precisa ver o que ele viu, não adivinhar"*. Sempre logar: o prompt final já montado (não o template), a resposta bruta, ferramenta + argumento + retorno, tokens/custo/latência por passo, versão do prompt e do modelo. Métricas de agente: taxa de conclusão, passos por tarefa, custo por tarefa resolvida, p95, % encaminhado para humano. Exemplo: uma tool devolvia 40 mil tokens de JSON cru que voltavam ao contexto a cada passo; resumir para 15 campos derrubou o custo por tarefa em ~70%. Material: Langfuse.
- **4.4 Prompt injection** — *"se o modelo lê, alguém pode escrever. Dado nunca é instrução — mas o modelo não sabe disso."* As **6 camadas de defesa**: (1) separe dado externo em tag e declare no system que ali não há instrução válida; (2) menor privilégio — o agente que LÊ e-mail não precisa da ferramenta de ENVIAR; (3) allowlist de destino e ação, teto de valor, nada de wildcard; (4) aprovação humana para ação irreversível; (5) sanitize a saída (HTML escape, SQL parametrizado, comando não executado); (6) trace de tudo, senão você nem fica sabendo que foi atacado. A tese: **"não existe patch de prompt para prompt injection; existe arquitetura"** — a defesa é limitar o estrago possível. RAG também é superfície: quem escreve num documento indexado escreve no seu prompt. Exemplo: currículo com texto branco em fundo branco mandando aprovar o candidato — o recrutador não vê, o parser lê, o modelo obedece. Material: Simon Willison, série sobre prompt injection.
- **4.5 Ensinar a dizer "não sei"** — *"o comportamento mais valioso e menos implementado"*. Por que ele não faz sozinho: o treino premia resposta útil, e "não sei" quase nunca foi a opção preferida pelo avaliador na fase de RLHF — logo, **se você quer abstenção, precisa pedir, dar formato e recompensá-la no eval**. Implementação: autorizar no system (`NAO_ENCONTRADO`), exigir campo `confianca`, definir limiar e o que acontece abaixo dele, e dar uma saída digna (encaminhar para humano é sucesso do produto, não falha do agente). Registre a taxa de encaminhamento como métrica de produto — *"se ela for exatamente 0%, desconfie"*. E **inclua no golden dataset casos que não têm resposta na base**, onde a resposta certa é "não sei": sem eles, você está otimizando o time para chutar com confiança.

## Módulo 5 — Nível sênior

- **5.1 Prompt vs RAG vs Fine-tuning** — o diagnóstico começa perguntando o que está faltando. **Falta conhecimento** → RAG. **Falta forma** → few-shot + saída estruturada; só depois, com 500+ exemplos bons, fine-tuning. **Falta capacidade** → modelo melhor ou modo de raciocínio (*"fine-tuning não cria capacidade nova"*). **Sobra custo/latência** → modelo menor + few-shot, ou destilação — a única situação em que o fine-tuning costuma pagar a própria conta. Regra prática: *"9 em cada 10 casos que parecem fine-tuning são RAG mal diagnosticado"*.
- **5.2 Fine-tuning: LoRA e QLoRA** — LoRA treina ~0,1% a 1% dos pesos e produz adapters de poucos MB; QLoRA é LoRA sobre modelo quantizado em 4 bits e cabe numa GPU de consumidor. FAZ formato, tom, jargão, tarefa estreita; NÃO faz fato novo confiável. Risco: esquecimento catastrófico. **80% do esforço é limpar dado, não treinar** — 500 a 5.000 exemplos bons valem mais que 100 mil ruins. Exemplo: extração de 12 campos de laudo, de prompt de 4.000 tokens com ~91% para prompt de 200 tokens com acerto parecido — *"o ganho veio de eliminar o prompt gigante, não de ensinar o assunto"*.
- **5.3 Context engineering** — *"prompt engineering escreve frases; context engineering decide o que ocupa a janela"*. As 4 técnicas: compaction, subagente em contexto separado, just-in-time retrieval, resumir retorno de ferramenta. Os princípios: contexto é orçamento e não depósito; todo token compete por atenção; **informação repetida ou contraditória é pior que informação ausente**; o fim da janela pesa mais; e o teste antes de acrescentar qualquer coisa — *"isso muda a próxima decisão do modelo?"*.
- **5.4 Multi-agente: quando vale** — **a escada, um degrau por vez**: (1) um agente com boas ferramentas — resolve a maioria, comece e fique aqui; (2) cadeia fixa; (3) roteador; (4) paralelo fan-out/fan-in; (5) orquestrador + subagentes. Vale quando é paralelizável e read-heavy com partes independentes; não vale com estado compartilhado ou escrita coordenada. Custo real: em geral uma ordem de grandeza mais token que um chat. **A regra que economiza meses: "se um agente com ferramentas boas não resolve, dois agentes com ferramentas ruins também não vão resolver"**.
- **5.5 Rodar local: quantização e VRAM** — `memória ≈ nº parâmetros × bytes por parâmetro` + 20-30% de overhead e KV cache. 8B em 4 bits ≈ 5 GB (notebook); 32B em 4 bits ≈ 20 GB; 70B em 4 bits ≈ 40 GB. 8 bits tem perda quase imperceptível, 4 bits perda pequena. Regra: **modelo maior em 4 bits costuma bater modelo menor em fp16 no mesmo orçamento de memória**. Faz sentido com dado que não pode sair, volume altíssimo de tarefa simples, offline/edge.
- **5.6 Por dentro do Transformer** — o mapa completo em 5 etapas: tokenização → embedding + posição → N blocos idênticos (attention multi-head, feed-forward, residual + norm) → camada de saída (logit por token do vocabulário) → softmax e amostragem, e volta ao passo 1. *"Não existe banco de dados, não existe regra escrita, não existe busca."*

## Módulo 6 — Virar profissional

**6.1 Roadmap de 90 dias** — o artefato mais distintivo do material: três blocos de 30 dias, cada um com uma entrega obrigatória e uma meta comportamental.

| Dias | Foco | Entrega | Meta |
| --- | --- | --- | --- |
| 1-30 | fundamento | um script que faz sozinho uma tarefa chata sua | perder o medo da API |
| 31-60 | construir | algo que outra pessoa usa sem você do lado | construir, não só conversar |
| 61-90 | confiar | um texto contando o que aprendeu, com números | defender decisão técnica com dado |

E o caminho para virar carreira em vez de hobby: escolher uma tarefa repetitiva do próprio time, **medir o baseline antes**, automatizar 80% e deixar os 20% difíceis para o humano, apresentar com número. O fecho: *"Quem mostra número vira referência. Quem mostra demo vira curiosidade."*

**6.2 Biblioteca essencial** — 12 materiais gratuitos, agrupados em fundamentos / construir / confiar. Regra de consumo: 1 vídeo de fundamento → 1 doc de prática → 1 projeto seu, e **nenhum material novo antes de aplicar o anterior em código que roda**.

## Links citados no board

Fundamentos: Karpathy [*Intro to LLMs*](https://youtube.com/watch?v=zjkBMFhNj_g) e [*Deep Dive into LLMs*](https://youtube.com/watch?v=7xTGNNLPyMI) · 3Blue1Brown [*But what is a GPT?*](https://youtube.com/watch?v=wjZofJX0v4M) e [*Attention, visually explained*](https://youtube.com/watch?v=eMlx5fFNoYc) · Jay Alammar [*Illustrated Word2vec*](https://jalammar.github.io/illustrated-word2vec) e [*Illustrated Transformer*](https://jalammar.github.io/illustrated-transformer) · [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762) · [tiktokenizer](https://tiktokenizer.vercel.app) · Lilian Weng sobre [alucinação](https://lilianweng.github.io/posts/2024-07-07-hallucination) e [agentes autônomos](https://lilianweng.github.io/posts/2023-06-23-agent).

Construir: Anthropic — [get started](https://docs.claude.com/en/docs/get-started), [prompt engineering](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview), [system prompts](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts), [multishot](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting), [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking), [structured outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs), [prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching), [tool use](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview), [building effective agents](https://anthropic.com/engineering/building-effective-agents), [contextual retrieval](https://anthropic.com/news/contextual-retrieval), [multi-agent research system](https://anthropic.com/engineering/built-multi-agent-research-system), [courses](https://github.com/anthropics/courses), [cookbooks](https://github.com/anthropics/claude-cookbooks) · [MCP](https://modelcontextprotocol.io) · [Pinecone — vector database](https://pinecone.io/learn/vector-database) · [promptingguide.ai](https://promptingguide.ai) · [artificialanalysis.ai](https://artificialanalysis.ai) · [Ollama](https://ollama.com) · [HF PEFT](https://huggingface.co/docs/peft/index) · [Chip Huyen](https://huyenchip.com/2023/04/11/llm-engineering.html) · [nanoGPT](https://github.com/karpathy/nanoGPT).

Confiar: [Hamel Husain — evals](https://hamel.dev/blog/posts/evals) · [Eugene Yan — LLM-evaluators](https://eugeneyan.com/writing/llm-evaluators) · [Langfuse](https://langfuse.com/docs) · [Promptfoo](https://promptfoo.dev/docs/intro) · [Simon Willison — prompt injection](https://simonwillison.net/series/prompt-injection) · [OWASP Top 10 for LLM Apps](https://genai.owasp.org/llm-top-10).

## O que isto muda no Codex

Comparado ao domínio [[03-Dominios/Tecnologia/IA/index|IA]] (22 galhos, ~300 notas), a cobertura deste board é menor — ele não toca em Spec-Driven Development, Memória de Agentes, harness engineering, Improvement Loop, Image/Multimodal Prompting nem economia de tokens com profundidade. O aproveitamento é metodológico e pontual:

1. **Lacuna de dono — prompt injection.** O tema aparece disperso em `Segurança e Guardrails/01`, `/07` e `Context Engineering/12`, mas não tem nota canônica, apesar de o índice do domínio listá-lo entre os 8 erros recorrentes. As 6 camadas de defesa da aula 4.4 servem de esqueleto.
2. **Lacuna real — abstenção.** "Ensinar a dizer não sei" tem uma única menção no domínio inteiro (`Evaluation/02`). O ângulo do RLHF (o treino premiou resposta útil, logo abstenção precisa ser pedida, formatada e recompensada no eval) costura Evaluation ↔ Structured Outputs ↔ Guardrails.
3. **Escopo do galho de segurança.** As 12 notas de `Segurança e Guardrails` tratam de segurança **do código gerado por IA**; segurança **da feature de IA em runtime** (injection, allowlist de tool, menor privilégio, aprovação humana) não tem casa. São duas seguranças sob um nome só.
4. **Espinha por maturidade.** O módulo "confiar" agrupa eval + judge + tracing + injection + abstenção como *estágio*, antes do nível sênior. No Codex, Evaluation é a trilha 13 de 17 e Improvement Loop a 17 — o que ele chama de gargalo real está no fim da fila. Sugere uma senda transversal nova.
5. **Exemplo com número como gate.** Nenhuma aula fecha sem um caso antes/depois quantificado. É o complemento que falta ao [[Padrão capítulo de livro]]: profundidade conceitual o Codex já tem; o que falta é o leitor sair sabendo *quanto vale*.
6. **Roadmap com entrega, não com leitura.** As sendas do Codex dizem o que ler; nenhuma diz o que precisa estar **rodando** no fim.

## Veja também

- [[03-Dominios/Tecnologia/IA/index|Domínio IA]] — a formação completa do Codex
- [[03-Dominios/Tecnologia/IA/Evaluation/index|Evaluation]] · [[03-Dominios/Tecnologia/IA/Segurança e Guardrails/index|Segurança e Guardrails]] · [[03-Dominios/Tecnologia/IA/Observability/index|Observability]]
