---
title: "Galho Anatomia dos LLMs — reformulação, enriquecimento e vídeos"
created: 2026-06-20
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - ia
  - anatomia-llm
---

# Galho Anatomia dos LLMs — reformulação, enriquecimento e vídeos

## Contexto

Diferente dos galhos de Fundamentos (refator de monólito → notas atômicas), este é uma
**reformulação de um galho já existente e já atômico**: `03-Dominios/Tecnologia/IA/Anatomia dos LLMs/`
(20 notas: 01–19 + "02b"). Três motores:

1. **Defeito de ordem (confirmado com o usuário).** Hoje a janela de contexto (03) vem *antes* do
   transformer (04) — invertido: a nota 03 precisa explicar o *porquê* dos limites (atenção, custo
   quadrático, lost-in-the-middle), que só fazem sentido depois do transformer.
2. **Notas resumidas demais.** As 20 notas têm 133–382 linhas (vs. 23–57K bytes/nota em Estruturas
   de Dados). O usuário relata dificuldade de compreensão **por falta de detalhe e didática**, não
   por excesso. O teto de 2400 dá folga para aprofundar de verdade.
3. **Faltam complementos em vídeo.** O vault só usa vídeo como link solto (Sendas, Mestres); nunca
   embutido como complemento didático dentro da nota.

## Decisão conceitual aprovada

Reordenar o Bloco 1 para a cadeia de dependências real, e **inserir uma nota nova de Completação**
entre o transformer e a janela:

> tokens → embeddings → **transformer** → **completação (loop autoregressivo)** → **janela de contexto**

Justificativa da ordem (Transformer → Completação → Janela, escolhida sobre Completação→Transformer):
completação é "o transformer rodado em loop" — você precisa ver o que *uma* passada produz (logits)
antes de explicar, sem hand-wave, o loop que amostra deles. A janela vem por último porque seu
limite é consequência da atenção (custo quadrático) + do loop (KV cache linear).

### Nota nova — "05 - Completação — o loop autoregressivo"

- **Assume e linka** (não reexplica): forward pass do transformer (nota 04), softmax-como-função
  (callout da nota 04), prefill/decode/KV cache (notas 04 e 06). Anti-duplicação vira link
  (regra do usuário: redundância entre notas é reforço, mas mecânica pesada fica num dono só).
- **Possui** (buraco atual do galho):
  - Camada de saída: o vetor de **logits** sobre o vocabulário (hoje só acenado na nota 02) →
    softmax → distribuição de probabilidade. "Mesmo softmax da atenção, agora sobre o vocabulário."
  - **Estratégias de amostragem**: greedy, top-k, top-p (nucleus), temperatura *como parâmetro de
    sampling* (hoje temperatura só aparece como dureza do softmax de atenção; `top_p` só numa tabela
    de API). Ninguém é dono disso — é o miolo da nota.
  - **Controle do loop**: token de parada (EOS), max tokens, quando para.
  - Enquadramento "prompt → completion / tudo é completação de texto".
- **Diagrama Mermaid central**: ciclo logits → softmax → sample → append → repeat até EOS.

## Renumeração (01 → 21)

Limpa o "02b" e abre espaço para Completação. Sequência final de **21 notas**.

| Novo | Nota | Antes |
|---|---|---|
| 01 | O que é um LLM | 01 |
| 02 | Tokens e tokenização | 02 |
| 03 | Embeddings — do token ao vetor | 02b |
| 04 | Atenção e o mecanismo transformer | 04 |
| **05** | **Completação — o loop autoregressivo** | **nova** |
| 06 | A janela de contexto | 03 |
| 07 | Panorama de modelos 2026 | 05 |
| 08 | Modelos chineses — DeepSeek, Qwen, Kimi, GLM | 06 |
| 09 | Dense vs Mixture-of-Experts | 07 |
| 10 | Modelos locais e self-hosting | 08 |
| 11 | APIs de LLM — anatomia de uma chamada | 09 |
| 12 | Pricing de APIs — como calcular custos | 10 |
| 13 | Prompt caching e otimizações de API | 11 |
| 14 | Streaming, batching e latência | 12 |
| 15 | Reasoning models e chain-of-thought | 13 |
| 16 | Fine-tuning vs prompting vs RAG | 14 |
| 17 | O futuro dos LLMs — tendências 2026-2027 | 15 |
| 18 | Como LLMs são treinados — pretraining, SFT, RLHF | 16 |
| 19 | Evaluation de LLMs em produção | 17 |
| 20 | Compressão de modelos — quantização e destilação | 18 |
| 21 | Fine-tuning na prática — LoRA, QLoRA, DPO | 19 |

**Custo:** toda nota de 03 pra frente muda de número. Todos os wikilinks de entrada
(`[[03 - A janela de contexto]]` etc.) quebram — na MOC, nas Sendas, no Dicionário de IA, e em
outras trilhas. Conserto na fase de fechamento (ver Wikilinks).

## Padrão por nota (herdado de Estruturas de Dados + pedidos do usuário)

- **Teto de prosa = 2400 linhas, SÓ NESTE GALHO** (decisão do usuário 2026-06-20, igual ED 2026-06-17):
  não é alvo, é **permissão** — cada nota vai tão fundo quanto o tema honestamente render, sem padding.
  **Linhas de código/diagramas NÃO contam.** Notas-intro (01, 07, 17) ficam leves; transformer,
  completação, janela, treino, MoE podem ir fundo.
- **Salto didático (o foco real do pedido):** registro Feynman — analogias concretas, perguntas
  retóricas em callouts, exemplos numéricos passo-a-passo, "resumo em 1 linha". **Cada conceito hoje
  citado de raspão ganha explicação de verdade** (logits, sampling, RoPE, MoE routing, RLHF/DPO,
  quantização, etc.). Referência do registro-alvo: a nota de embeddings (atual "02b") e os callouts
  de KV cache da nota da janela (atual 03), que já trazem o tom Feynman desejado.
- **3–5 diagramas Mermaid** por nota onde ajudam.
- **Split quando estourar 2400:** quebrar em "NN Conceito" + nota irmã, flagando o split.
- **Anti-duplicação vira link** (regra do usuário): mecânica pesada (prefill/decode/KV cache) tem um
  dono (04/06); as outras linkam. Redundância conceitual leve é reforço, não se poda.
- **Frontmatter:** manter convenção do galho — `type: concept`, `status: growing|evergreen`,
  `progress`, `publish: true`, tags `anatomia-llm/ia/tokens`, aliases EN+PT. **Sem campo `fase:`**
  (este galho organiza por Blocos, não por iniciado/adepto/magus).

## Vídeos (decisões do usuário 2026-06-20)

- **Embed inline como complemento do texto, não rodapé.** Onde o vídeo ilumina o ponto, embutir o
  player ali (sintaxe Obsidian `![](url)`, que o Quartz renderiza). Pode embutir **2–3 vídeos numa
  mesma nota** quando cada um cobre uma parte do tópico. Pensar no vídeo como parte da explicação.
- **Seção "Ver mais" ao fim** mantida: lista curada de vídeos/playlists complementares, cada um com
  **breve descrição** do que agrega.
- **Idioma:** PT-BR e EN, desde que **tenham legenda**. EN é bem-vindo, especialmente grandes nomes
  (Karpathy, Addy Osmani, 3Blue1Brown, Jay Alammar, Raschka…).
- **Método de pesquisa e vetagem:** WebSearch + `yt-dlp` (mesma engine da `/glosa-video`) para achar
  candidatos por tópico, baixar **legendas + descrição**, e **vetar por relevância/atualidade
  (priorizar 2024–2026)/qualidade do canal ANTES de embutir** — nunca colar vídeo sem ter "lido" a
  legenda. Produz um inventário curado por tópico antes de tocar nas notas.
- **Legenda alimenta o texto:** o conteúdo aprendido nas legendas dos vídeos pode entrar no
  enriquecimento das notas quando agregar (citando a fonte), não só ser linkado.
- **Mestres novos:** se a pesquisa revelar autores com acervo relevante ainda não fichados em
  `00-Meta/mestres/`, **adicionar à lista de mestres** usando o `Template - Mestre completo`
  (não stub; links verificados via web — convenção do projeto Mestres). Candidatos prováveis:
  Addy Osmani, 3Blue1Brown (Grant Sanderson), Jay Alammar, Sebastian Raschka. Karpathy já existe.

## Preservação (rígido)

- Qualquer experiência REAL do usuário embutida nas notas atuais é intocável e **nunca se fabrica
  nova** (regra anti-fabricação). Na dúvida, perguntar.
- Fontes, vocabulário bilíngue ("How to explain in English"), talking points e rotas alternativas da
  MOC atual são preservados e atualizados, não descartados.

## Wikilinks (fase de fechamento)

1. `grep -rn "\[\[0X - <título antigo>" .` para cada nota renumerada → mapear ocorrências.
2. Atualizar referências por número em: `index.md` do galho, `04-Sendas/Senda IA.md`,
   `Dicionário de IA.md`, outras trilhas de IA, e qualquer MOC de domínio.
3. Rodar a skill `verificar-wikilinks` na pasta do galho + nas Sendas para pegar o que escapou.
4. Conferir a regra do Quartz (folder-link exige index.md) — o galho já tem index.md.

## Convenções

- `publish: true` nas notas (convenção do galho IA, diferente de Fundamentos).
- Feynman didático; fontes/honestidade em toda afirmação factual; **sem assinatura de Claude nos
  commits**; direto na `main`, push manual.
- Verbetes novos no `Dicionário de IA.md` conforme termos surgem (logit, sampling, top-k/top-p,
  greedy decoding, EOS, etc.), em ordem alfabética.

## Sequência de execução

1. **Scaffold estrutural** — renomear/renumerar os 20 arquivos (03→06, 05→07, … 19→21; 02b→03);
   escrever a nota nova **05 - Completação**; atualizar `index.md` (nova ordem, Bloco 1 reescrito,
   dataview). Commit.
2. **Pesquisa profunda de vídeos** — rodada de research por tópico (WebSearch + yt-dlp; vetar por
   legenda/descrição). Produz inventário curado: por nota, vídeos-hero a embutir + "Ver mais" +
   mestres novos a fichar. Sem editar notas ainda.
3. **Enriquecimento nota a nota** — aplicar as lentes da `enriquecer-nota` com o teto de 2400,
   embutindo os vídeos vetados e incorporando conteúdo de legenda quando agregar. Por escala
   (21 notas), rodar em **lotes via subagentes**, com as lentes globais fixadas por este plano
   (em vez de aprovação interativa nota-a-nota); só decisões notáveis sobem (ex.: split de nota).
4. **Mestres** — fichar os mestres novos descobertos (Template - Mestre completo, links verificados).
5. **Fechamento** — consertar wikilinks (grep + `verificar-wikilinks`); verbetes no Dicionário;
   atualizar MOCs de domínio e `Senda IA`; commit final; fechar a MOC em `growing`.
