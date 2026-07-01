---
title: "Roadmap IA — plano de enriquecimento nota a nota"
created: 2026-06-29
updated: 2026-06-29
type: plan
status: growing
publish: false
tags:
  - meta
  - plan
  - ia
  - roadmap
---

# Roadmap IA — plano de enriquecimento nota a nota

Plano detalhado de acompanhamento do enriquecimento do domínio **IA** (`03-Dominios/Tecnologia/IA/`).
Cada galho tem uma seção com **uma entrada por nota**: estado atual, se precisa de mudança, e quais
mudanças são propostas. O estado **por galho** (resumo) vive no `Roadmap.md`; o detalhe **por nota**
vive aqui.

> [!info] Como este documento é construído
> Análise feita **nota a nota, um subagente por vez** (sem fan-out). Cada subagente lê uma nota,
> audita contra a régua das skills (abaixo) e grava a entrada dela aqui. Ao fechar um galho, o
> estado-resumo é registrado no `Roadmap.md`.

## Régua de análise (skills `escrever-nota` / `verificar-nota` / `enriquecer-nota`)

A régua **não é mais** "todas as seções obrigatórias". É **núcleo mínimo + opcionais caso-a-caso**,
medida por um gate de score.

**Núcleo mínimo (sempre exigido):**
1. Frontmatter completo (`fase:` é núcleo na convenção nova — ver ressalva do galho)
2. TL;DR `> [!abstract]` com ≥3 linhas densas
3. Abertura com problema/cenário real (não começa com definição)
4. Corpo técnico explicando o **mecanismo** (por quê, não só o quê)
5. **O que vem a seguir** — ponte narrativa pra próxima nota (≠ lista "Ver mais")
6. Fontes

**Opcionais (avaliadas por tema, vetadas pelo crítico — NÃO se força em toda nota):**
Diagrama Mermaid · Tabela comparativa · Casos práticos · Armadilhas comuns (`[!warning]`) ·
Código com falha · Como explicar em inglês + tabela PT↔EN · Fundamento teórico (Magus) ·
Veja também · Callouts pedagógicos (`[!question]-`, `[!example]`) · Resumo em 1 linha.

**Gate `verificar-nota`:** score ≥9/12 = aprovada (com isenções por fase/tipo/broto). Itens E4
(casos), E6/E7 (inglês), E8 (armadilhas), M1 (mídia) contam pro score mas são caso-a-caso.

**Dúvidas:** `/plantar-duvidas` → `/colher-duvidas` é **passada pós-nota**, rodada depois da nota
pronta — não faz parte do núcleo de escrita/enriquecimento.

### Template da entrada por nota

```
#### NN - Título
- **Estado:** <N> linhas · fase: <X|ausente> · status: <y>
- **Núcleo:** TL;DR <✓/✗> · Abertura-problema <✓/✗> · Corpo-mecanismo <✓/✗> · O que vem a seguir <✓/✗> · Fontes <✓/✗>
- **Opcionais presentes:** <lista>
- **Score verificar-nota (estimado):** N/12
- **Precisa mudança:** SIM / NÃO
- **Mudanças propostas:**
  - <ação concreta ou "—">
```

---

## Tabela-mestre dos galhos

| # | Galho | Notas | Análise nota-a-nota | Estado-resumo (→ Roadmap.md) |
|---|-------|-------|---------------------|------------------------------|
| 1 | Anatomia dos LLMs | 24 | ✅ analisado (29/06) | Todas ≥9/12; 23 pedem ajuste (só 04 fechada). Falta bridge E5 em ~22 + Armadilhas→`[!warning]` em ~17 |
| 2 | Anatomia de Agents | 11 | ✅ analisado (30/06) | 4 notas <gate (8/12), 5 em 9, 2 em 10; nenhuma fechada. E5 ausente em TODAS · E8 em ~9 · L2 em 5 |
| 3 | Spec-Driven Development | 12 | ✅ analisado (30/06) | TODAS <gate (1×4, 4×5, 5×6, 2×7). E5 + L2(URLs) + E6/E7(inglês) ausentes em quase todas; galho mais cru |
| 4 | Economia de Tokens | 22 | ✅ analisado (30/06) | Bimodal: 01–04 cruas (5–7/12, sem fase) vs 05–22 fortes (≥9; ET-05=12/12). Gaps do corpo: L1/L2/piso. 2 não precisam mudança |
| 5 | Context Engineering | 16 | ✅ analisado (30/06) | Mais consistente: todas ≥9 (1×9,7×10,7×11,1×12); 9 não precisam mudança. Gaps só polimento: L1/L2/piso/P1 |
| 6 | Agentes de Codificação | 18 | ✅ analisado (30/06) | Sólido: todas ≥9 (2×9,11×10,5×11); 3 não precisam mudança. Gap sistêmico E5 (ponte não aponta pra próxima nota); fase ausente na 01; caducidade nas tools |
| 7 | AI Engineering Stack | 13 | ✅ analisado (30/06) | TODAS 11/12 (núcleo íntegro, P1 inaplicável). Mas conteúdo real <piso na maioria (rodapé em branco infla wc -l); higiene: seedling na 13, inglês duplicado na 02 |
| 8 | RAG e Vector Databases | 13 | ✅ analisado (30/06) | 2×8(<gate),3×9,6×10,2×11; só 11 fechada. Gaps: E2 (abertura) · L2 (URLs) · conteúdo real <piso em 8/13 |
| 9 | MCP | 10 | ✅ analisado (30/06) | 3×8(<gate: 01/04/05),5×9,1×10,1×11; nenhuma fechada. L2 universal (refs em itálico) · E2 · E1 (TL;DR raso) |
| 10 | Segurança e Guardrails | 12 | ✅ analisado (30/06) | 2×8(<gate: 05,07),1×9,9×10; nenhuma fechada. L2 universal (refs sem URL) · conteúdo real <piso · E2/E1 |
| 11 | Memória de Agentes | 24 | ✅ analisado (30/06) | Mais sólido do lote 28/06: 1×8(24),3×9,15×10,5×11; 7 não precisam mudança. Gap dominante E2 (abre "X é...") · caducidade nas implementações |
| 12 | Prompt Engineering | 9 | ✅ analisado (30/06) | 1×7(<gate: 09),2×9,4×10,2×11; 2 não precisam mudança. Gap: conteúdo real <piso (04/08/09 curtas) · E1 · L2 |
| 13 | Structured Outputs | 8 | ✅ analisado (30/06) | 1×8(<gate: 06),1×9,5×10,1×11; 1 não precisa mudança. Gaps: conteúdo real <piso (5/8) · E3 ausente · caducidade API |
| 14 | Evaluation | 8 | ✅ analisado (30/06) | 1×8(<gate: 02),2×9,4×10,1×11; 3 não precisam mudança. Gaps leves: E3 (Mermaid) · E2/E1 |
| 15 | Observability | 8 | ✅ analisado (30/06) | Nenhuma <gate (1×9,6×10,1×11); 4 não precisam mudança. Gap dominante E3 (Mermaid ausente, ASCII) · conteúdo <piso em 02/04 |
| 16 | Multimodal Prompting | 7 | ✅ analisado (30/06) | 2×8(<gate: 02,04),2×9,3×10; 2 não precisam mudança. Gaps: E2 (abertura) · E1 · E3 · conteúdo <piso na 07 |
| 17 | Image Prompting | 7 | ✅ analisado (30/06) | Nenhuma <gate (4×9,3×10); 3 não precisam mudança. Gaps leves: E2 (abertura 03/04/05) · E1 · conteúdo <piso em 03/04/05 |
| 18 | Improvement Loop | 7 | ✅ analisado (30/06) | Nenhuma <gate (2×9,5×10); 4 não precisam mudança. Gaps leves: E3 (Mermaid/ASCII) · E2 (02/04) · conteúdo <piso em 04/06 |
| 19 | Ferramentas de IA | 5 | ✅ analisado (30/06) | 5 notas-referência grandes; 1×8(<gate: Claude),4×9. TL;DR `[!abstract]` ausente nas 5 · caducidade pesada (preços/modelos) · E3 ASCII |
| 20 | O Lado Sombrio da IA | 1 | ⬜ fora de escopo | cluster crítico |
| 21 | Claude Code | 0 | ⬜ vazio | — |
| — | Notas soltas (raiz IA) | 3 | ✅ analisado (30/06) | Dicionário saudável · Yegge sem TL;DR/fase · Biblioteca stub |

> **Diagnóstico do domínio CONCLUÍDO em 2026-06-30** — 237 notas (19 galhos + 3 soltas). Fora de escopo: O Lado Sombrio da IA (cluster crítico) e Claude Code (vazio).

---

## Padrões transversais (síntese 30/06)

Distribuição global: **~84% das notas no gate (≥9/12)**; 34 abaixo. 2 notas 12/12 (Economia de Tokens 05, Context Engineering 06). Galho mais forte: **Memória de Agentes / Context Engineering**. Mais cru: **Spec-Driven Development** (todas <gate). 47 notas já fechadas (não precisam mudança).

**Gaps recorrentes, do mais comum ao menos:**

1. **E2 — abertura sem cenário** (abre com "X é…" em vez de problema). O mais difundido, sobretudo nos galhos `fase: Iniciado` (Memória, Multimodal, Image, Structured, MCP, Segurança). Conserto barato e de alto ganho didático.
2. **E1 — TL;DR raso** (1 linha em vez de ≥3 no `[!abstract]`). Universal em Ferramentas de IA; comum em MCP, Prompt Eng., Image, Evaluation.
3. **E3 — diagramas em ASCII, não Mermaid.** Universal nos galhos do lote 28/06 (Evaluation, Observability, Improvement Loop, Structured Outputs).
4. **L2 — referências sem URL clicável** (citadas em prosa/itálico). Universal em Segurança e Guardrails e MCP; frequente em SDD, Anatomia LLMs, RAG.
5. **E5 — bridge "O que vem a seguir"** ausente ou apontando para notas relacionadas em vez da PRÓXIMA da sequência. Concentrado nos galhos antigos (Anatomia dos LLMs, Anatomia de Agents, Agentes de Codificação); resolvido nos de 28/06.
6. **Conteúdo real < piso** mascarado por **linhas em branco no rodapé** que inflam o `wc -l`. O selo "completo" de vários galhos se baseou na contagem bruta. Pior em AI Engineering Stack e RAG.
7. **E8 — armadilhas em bullet/tabela** em vez de `[!warning]` individuais. Marcante em Anatomia dos LLMs, Anatomia de Agents, SDD.
8. **Caducidade** (preços/versões/modelos/datas). Pior em **Ferramentas de IA** (envelhece mais rápido), depois notas de ferramenta/modelo/panorama por todo o domínio; alerta regulatório urgente em Segurança 11 (EU AI Act, prazo 02/08/2026).
9. **Higiene pontual:** seção duplicada (AI Eng. Stack 02 inglês, Observability 01 "Veja também", Codex/Copilot armadilhas), `status: seedling` em notas já crescidas, premissa possivelmente caduca (Structured Outputs 05: Anthropic structured output nativo).

**Régua de leitura:** `fase:` é usado por quase todos os galhos (Iniciado, piso ≥300) — exceto **Anatomia dos LLMs**, **Anatomia de Agents** e **Spec-Driven Development**, organizados por sequência/Blocos sem `fase:` (decisão de spec); nesses, a ausência de `fase:` NÃO é gap. Notas 01 de Economia de Tokens e Agentes de Codificação são exceção: deveriam ter `fase:` e não têm.

---

## 1. Anatomia dos LLMs

> Galho reformulado pelo spec `00-Meta/specs/2026-06-20-galho-anatomia-llms-reformulacao-plan.md`.
> **Ressalva de `fase:`**: o spec decidiu organizar este galho por **Blocos**, não por fase
> (Iniciado/Adepto/Magus). Avaliar a bridge "O que vem a seguir" (núcleo) é prioridade; a decisão
> sobre adotar `fase:` aqui está pendente com o usuário.

### Notas

#### 01 - O que é um LLM
- **Estado:** 217 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid, inglês+PT↔EN, mídia embutida ([!tip] com 2 vídeos), tabelas comparativas (fases/categorias/glossário), armadilhas (lista simples), resumo em 1 linha, Veja também
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Converter a seção "Armadilhas" (4 itens como lista simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 10/12
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## O que é" (ex: engenheiro recebendo uma API key pela primeira vez sem saber o que há por baixo) — ativa E2 e eleva score para 11/12
#### 02 - Tokens e tokenização
- **Estado:** 254 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart BPE), tabelas comparativas (variantes × aspectos; tokenizadores na prática; subword × character × word), casos práticos (strawberry, SolidGoldMagikarp, custo multilíngue), armadilhas (lista com 5 itens — mas sem callouts `[!warning]`), inglês + tabela PT↔EN, resumo em 1 linha ("Tokens em uma frase"), Veja também, mídia embutida ([!tip] com vídeo Guanabara), callout [!example] (SolidGoldMagikarp), callout [!info] (vocabulário)
- **Score verificar-nota (estimado):** 9/12 — falham E2 (abertura sem problema/cenário real), E8 (armadilhas como lista simples, sem `[!warning]` individuais), P1 (sem código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Converter a seção "Armadilhas" (5 itens em lista bullet) para callouts `[!warning]` individuais — ativa E8 e eleva score para 10/12
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## O que é" (ex: "Você enviou 500 palavras para a API e a resposta veio com 600 tokens — como isso é possível?") — ativa E2 e eleva score para 11/12
#### 03 - Embeddings — do token ao vetor
- **Estado:** 197 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid (espaço vetorial 2D + flowchart do pipeline), inglês + tabela PT↔EN (11 termos), armadilhas (4 itens — lista simples, sem `[!warning]`), resumo em 1 linha ("Embeddings em uma frase"), wikilink cross-galho (RAG/VectorDB), callout `[!question]-` (cosseno vs distância), `[!info]`, `[!tip]`, mídia embutida (vídeo Sandeco), casos práticos (aritmética rei-rainha + busca semântica/RAG)
- **Score verificar-nota (estimado):** 10/12 — falham E8 (armadilhas sem `[!warning]` individuais) e P1 (sem código-com-falha — inaplicável para nota conceitual pura)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Converter os 4 itens da seção "## Armadilhas" (atualmente lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
#### 04a - KV cache, prefill e decode — a física da inferência (broto)
- **Estado:** 197 linhas · fase: Magus · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid, inglês + tabela PT↔EN (10 termos), 1× [!warning], casos práticos (H100 budget, Llama 2 vs 3, TTFT, batching), tabela comparativa (prefill × decode; custo quadrático O(n²)), 2× [!question]- pedagógicos, [!tip] (metáfora), fórmula LaTeX, Veja também
- **Score verificar-nota (estimado):** 9/12 (broto — piso de linhas isento)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção ou parágrafo narrativo "O que vem a seguir" apontando para o próximo broto da sequência (04b — MHA/MQA/GQA/MLA) — fecha o único item de núcleo faltante (E5) e eleva score para 10/12
  - Opcional: expandir o único [!warning] existente ("cache é por-request") para ≥3 callouts `[!warning]` individuais (ex: "dobrar contexto ≠ dobrar custo de compute", "TTFT e throughput não são correlacionados") — ativa E8 e eleva score para 11/12
#### 04 - Atenção e o mecanismo transformer
- **Estado:** 442 linhas · fase: Adepto (presente — spec prevê ausência, mas nota a tem) · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (3×), tabelas (Q/K/V + multi-head + PT↔EN), casos práticos (correferência animal/ele + cálculo numérico), 3 [!warning], inglês + tabela PT↔EN (11 termos), callouts pedagógicos ([!question]-, [!example], [!info], [!tip]), resumo em 1 linha, Veja também, mídia embutida (vídeo 3Blue1Brown)
- **Score verificar-nota (estimado):** 11/12
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 04b - Encolhendo o KV cache — MHA, MQA, GQA, MLA (broto)
- **Estado:** 209 linhas · fase: Magus · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 4× Mermaid (grafo evolutivo MHA→MLA, MQA, GQA, pipeline MLA + xychart comparativo), tabela comparativa (KV cache por variante), inglês + tabela PT↔EN (10 termos), [!question]- (uptraining GQA), [!tip] (intuição MLA), wikilinks cross-galho (08 DeepSeek, 09 Dense/MoE), referências arxiv (3 papers primários), Veja também (4 wikilinks internos + 3 vídeos em "Ver mais")
- **Score verificar-nota (estimado):** 9/12 (broto — piso isento) — falham E5 (sem ponte narrativa para 04c), E8 (sem [!warning] na nota inteira), P1 (sem código)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (após o comparativo final) apontando para 04c — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Adicionar ≥3 callouts `[!warning]` com armadilhas concretas (ex: "GQA exige uptraining — não é drop-in replacement", "MLA adiciona custo de up-projection a cada step de decode — monitorar latência", "MQA degrada perceptivelmente em raciocínio multi-ângulo em modelos grandes") — ativa E8 e eleva score para 11/12
#### 04c - Atenção eficiente — FlashAttention, sparse e híbrida (broto)
- **Estado:** 221 linhas · fase: Magus · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 5× Mermaid (hierarquia GPU, tiling, atenção sparse vs full, arquitetura híbrida, attention sinks), tabela comparativa (N tokens × tamanho QKᵀ; otimizações × complexidade), inglês + tabela PT↔EN (11 termos), 1× [!warning] (dosagem camadas locais), 2× [!question]- pedagógicos (por que gargalo é memória; FA4 mais rápido), casos práticos (StreamingLLM 4M tokens, Gemma 2, GPT-OSS, FlashAttention H100), fórmulas LaTeX, Veja também, mídia embutida (vídeo Umar Jamil via [!tip] implícito na seção dedicada)
- **Score verificar-nota (estimado):** 9/12 (broto — piso isento) — falham E5 (sem ponte narrativa para 05 Completação), E8 (apenas 1 [!warning], precisa ≥3), P1 (sem código-com-falha — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (após "Veja também" ou antes das referências) apontando para [[05 - Completação — o loop autoregressivo]] — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Adicionar ≥2 callouts `[!warning]` adicionais com armadilhas concretas (ex: "FlashAttention elimina o gargalo de memória do prefill, mas não muda a latência de decode para geração token a token — equívoco comum ao justificar uso de FA em inferência interativa"; "NSA e DSA requerem retreino completo — não são drop-in replacements para modelos existentes") — ativa E8 e eleva score para 11/12
#### 05 - Completação — o loop autoregressivo
- **Estado:** 231 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid (flowchart loop autoregressivo, xychart temperatura, graph LR top-p vs top-k), tabela comparativa (temperatura × probabilidade; PT↔EN 10 termos), 3 cenários práticos de produção (não-determinismo, truncamento, loops de repetição), 2× [!warning], inglês + tabela PT↔EN, callouts pedagógicos ([!info], [!note], [!example], [!tip]), seção armadilhas (5 itens), fórmula LaTeX (softmax), Veja também, Ver mais (3 links externos com vídeos/papers)
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Converter a seção "## Armadilhas" (5 itens como lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12 (já há 2 callouts [!warning] inline; a seção dedicada ficou como lista)
#### 06 - A janela de contexto
- **Estado:** 428 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 6× Mermaid (mindmap importância, graph LR input/output, graph prefill×decode, mindmap degrada, xychart curva U, graph ciclo agentes), tabela comparativa (modelos 2026 com context/output; cenários de uso; input×output tokens; PT↔EN 12 termos), inglês + tabela PT↔EN, 2× [!warning] (distinção crítica + limite nominal), [!danger] (bola de neve em agentes), [!abstract] inline (ideia central), múltiplos [!info] pedagógicos, [!question]- (Lost in the Middle vs recency vs attention sink), [!tip] (analogia holofote; toolbox Mermaid), [!example] (posição × ocupação), [!note], [!summary], wikilinks cross-galho (notas 12, 13, 14 + Dicionário de IA), referências extensas (10+ papers/posts com links)
- **Score verificar-nota (estimado):** 9/12 — falham E5 (sem ponte narrativa para 07 Panorama de modelos), E8 (seção Armadilhas em lista bullet simples, sem `[!warning]` individuais; só 2 callouts [!warning] no corpo), P1 (sem código-com-falha — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais" ou antes de "## Referências") apontando para [[07 - Panorama de modelos 2026]] — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter a seção "## Armadilhas" (5 itens como lista bullet) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
#### 07 - Panorama de modelos 2026
- **Estado:** 242 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 4× Mermaid (xychart curva de preços, graph TD anatomia do mercado, graph LR tarefa simples×difícil, graph TD mapa de decisão, xychart custo de sessão), tabelas comparativas (OpenAI/Anthropic/Google/Open-Weight × preço+context; SWE-bench; custo por tarefa real), inglês + tabela PT↔EN (11 termos), 1× [!warning] ("Benchmarks são guia, não verdade"), [!question]- (queda de preços), seção "Armadilhas comuns" (lista bullet com 5 itens), Veja também (4 wikilinks), Ver mais (3 links externos com descrição), wikilinks cross-galho (Dicionário de IA, notas 08/09/12/17)
- **Score verificar-nota (estimado):** 9/12 — falham E5 (sem ponte narrativa; "Veja também" com link para 08 não conta), E8 (armadilhas como lista bullet simples, sem `[!warning]` individuais; só 1 callout inline), P1 (sem código-com-falha — inaplicável para nota-panorama)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais") apontando para [[08 - Modelos chineses — DeepSeek, Qwen, Kimi, GLM]] com motivação narrativa (ex: por que os players chineses open-weight merecem um capítulo próprio) — fecha E5 (núcleo faltante) e eleva score para 10/12
  - Converter a seção "## Armadilhas comuns" (5 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
  - Nota com altíssima densidade de dados com data de validade (preços $/MTok, scores SWE-bench, versões de modelos): adicionar `[!warning]` ou `[!info]` de caducidade no topo da seção "Os grandes players" avisando que preços e benchmarks mudam mensalmente e o leitor deve conferir em Artificial Analysis
#### 08 - Modelos chineses — DeepSeek, Qwen, Kimi, GLM
- **Estado:** 233 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid (xychart custos + graph TD decisão), tabela comparativa (4 modelos × 7 critérios + PT↔EN 8 termos), inglês + tabela PT↔EN, casos práticos (choque jan/2025, capitalização Nvidia, setup Ollama/SiliconFlow), seção Armadilhas (5 itens — lista bullet, sem `[!warning]`), 2× código funcional (bash Ollama + bash SiliconFlow), Veja também, Ver mais (3 links externos)
- **Score verificar-nota (estimado):** 9/12 — falham E5 (sem ponte narrativa para 09 Dense vs MoE; "Veja também" não conta), E8 (5 armadilhas como lista bullet simples, sem callouts `[!warning]` individuais), P1 (sem código-com-falha — inaplicável para nota conceitual/comparativa)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" antes de "## Ver mais" apontando para [[09 - Dense vs Mixture-of-Experts]] com motivação (ex: por que MoE é a espinha da eficiência chinesa — conecta diretamente ao custo 5-20x menor) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter a seção "## Armadilhas" (5 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
  - Nota tem altíssima densidade de dados com data de validade (versões DeepSeek V4, Qwen 3.6, Kimi K2.6, GLM-5.1; preços $0.27/$0.9/1M tokens): considerar adicionar `[!info]` de caducidade na seção "## Comparativo" avisando que versões e preços mudam rapidamente
#### 09 - Dense vs Mixture-of-Experts
- **Estado:** 292 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 4× Mermaid (dense FFN, routing MoE, load balancing, paradoxo memória), exemplo numérico passo-a-passo, tabela comparativa (modelos reais 2026 + dense vs MoE × 5 critérios + PT↔EN 11 termos), 4× [!warning] (memória, "MoE melhor em tudo", parâmetros totais vs ativos, qualidade do router), inglês + tabela PT↔EN, [!question]- pedagógico (custo do router; parâmetros no FFN), 2× vídeos embutidos (Jay Alammar + Maarten Grootendorst), Veja também, Ver mais
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais") apontando para [[10 - Modelos locais e self-hosting]] com motivação concreta (ex: agora que você entende por que MoE precisa de toda a VRAM carregada, o próximo passo é calcular quanto hardware você precisa para rodar um modelo localmente — e como MoE muda essa conta) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Adicionar pelo menos 1 wikilink cross-galho (ex: para [[Economia de Tokens]] ou [[RAG e Vector Databases]]) para ativar L1 e elevar score para 11/12
#### 10 - Modelos locais e self-hosting
- **Estado:** 222 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid (xychart VRAM + graph TD decisão Ollama/vLLM/llama.cpp), tabelas comparativas (hardware × VRAM; Apple Silicon; cenários self-host; custo mensal), inglês + tabela PT↔EN (9 termos), 1× [!warning] (custo escondido), seção Armadilhas (5 itens — lista bullet simples), código funcional bash (Ollama + vLLM), Veja também (4 wikilinks internos — incluindo cross-galho para Dicionário de IA), Ver mais (3 links externos)
- **Score verificar-nota (estimado):** 9/12 — falham E5 (sem ponte narrativa para 11; "Veja também" com link não conta), E8 (seção Armadilhas em lista bullet simples, sem `[!warning]` individuais; apenas 1 callout no corpo), P1 (código funcional presente mas sem código-com-falha — inaplicável para nota de setup)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais") apontando para `[[11 - APIs de LLM — anatomia de uma chamada]]` com motivação (ex: agora que você sabe calcular quanto hardware precisa e quando self-host vale, o caminho alternativo — consumir um modelo via API — merece o mesmo nível de entendimento da sua anatomia interna) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter a seção "## Armadilhas" (5 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
#### 11 - APIs de LLM — anatomia de uma chamada
- **Estado:** 259 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid (xychart custo acumulado por turn + sequenceDiagram ciclo de agente), tabelas comparativas (campos do request × impacto em tokens; roles × consumo; temperature × comportamento; campo usage × significado; jornada 7 estágios da chamada), inglês + tabela PT↔EN (10 termos), seção Armadilhas (5 itens — lista bullet simples, sem `[!warning]`), casos práticos (custo acumulativo turn 50 = 280k tokens, temperatura por tipo de tarefa, ciclo Claude Code), wikilinks cross-galho (notas 13, 14, Dicionário de IA), Veja também, Ver mais (3 links externos)
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais" ou antes de "## Veja também") apontando para [[12 - Pricing de APIs — como calcular custos]] com motivação concreta (ex: agora que você entende o que cada campo do request consome, o próximo passo é traduzir esse consumo em dinheiro — e descobrir por que duas chamadas idênticas em número de tokens podem ter custo muito diferente) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter a seção "## Armadilhas" (5 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
  - Adicionar ao menos 1 exemplo de código-com-falha (ex: request Anthropic sem `max_tokens` retornando erro 400, ou array `messages` com roles fora de ordem causando erro de validação) — ativa P1 e eleva score para 12/12
#### 12 - Pricing de APIs — como calcular custos
- **Estado:** 220 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid (graph LR fórmula custo, xychart-beta custo acumulado agente, graph TD custos ocultos), tabelas comparativas (preços por provider/tier; escalada por turn; mecanismos de desconto; custos ocultos; simulação dia de dev; ferramentas de monitoramento), 5× [!warning] (callouts individuais: escala, verbosidade output, assimetria no cálculo, reasoning tokens invisíveis, limite do caching), inglês + tabela PT↔EN (10 termos), casos práticos (agente com fatura $2.400, simulação 50 turns = $13.50, engenheiro 8h = $25.28), [!question]- pedagógico (por que output custa mais), checklist de boas práticas
- **Score verificar-nota (estimado):** 10/12 — falham E5 (sem ponte narrativa para nota 13; "Veja também" com link não conta), L2 (referências sem URLs — fontes nomeadas mas sem hiperlinks clicáveis)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Veja também") apontando para [[13 - Prompt caching e otimizações de API]] com motivação concreta (ex: agora que você sabe calcular o custo, o próximo passo é aprender a reduzi-lo — e o prompt caching é a alavanca com maior ROI, cortando até 90% do custo de input em chamadas repetitivas) — fecha E5 (único item de núcleo faltante) e eleva score para 11/12
  - Adicionar URLs reais às referências (Anthropic pricing page, OpenAI pricing, artificialanalysis.ai, costgoat.com) — ativa L2 e eleva score para 12/12
  - Adicionar `[!warning]` de caducidade no topo da "## Tabela de preços (maio 2026)" avisando que preços e modelos mudam mensalmente e o leitor deve conferir em Artificial Analysis ou no dashboard do provider — nota tem alta densidade de dados com data de validade (preços $/MTok, nomes de modelos como GPT-5.4, Gemini 3.1 Pro)
#### 13 - Prompt caching e otimizações de API
- **Estado:** 273 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid (sequenceDiagram KV cache, graph TD model routing, xychart-beta custo por provider), tabela comparativa (caching por provider + Batch API + impacto combinado), inglês + tabela PT↔EN (11 termos), casos práticos ($2.700 fatura real + 5k chamadas/dia + simulação por provider), seção Armadilhas (5 itens — lista bullet simples, sem `[!warning]`), código funcional (Anthropic JSON + OpenAI JSON + Google Python + Batch API + compressão de tools), wikilinks cross-galho (Dicionário de IA, notas 11/12/14), Ver mais (3 links externos com URL), Veja também
- **Score verificar-nota (estimado):** 9/12 — falham E5 (sem ponte narrativa para 14; "Veja também" com link não conta), E8 (5 armadilhas como lista bullet simples, sem callouts `[!warning]` individuais), P1 (código funcional presente mas sem código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais" ou "## Veja também") apontando para [[14 - Streaming, batching e latência]] com motivação concreta (ex: agora que você sabe reduzir o custo por token, o próximo vetor de otimização é a latência — e o streaming muda fundamentalmente como o usuário percebe a resposta, mesmo sem alterar um centavo do custo) — fecha E5 (único item de núcleo faltante) e eleva score para 10/12
  - Converter a seção "## Armadilhas" (5 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
#### 14 - Streaming, batching e latência
- **Estado:** 247 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 5× Mermaid (trilemma, prefill/decode, percepção TTFT xychart, speculative decoding, inferência desagregada), tabelas comparativas (fases × bottleneck; métricas × thresholds; tipos de batching; otimizações × ganho; cenários streaming/batching), inglês + tabela PT↔EN (11 termos), 1× [!warning] (P99 latency), seção Armadilhas (5 itens — lista bullet simples, sem `[!warning]` individuais), [!question]- pedagógico (streaming deixa mais rápido?), código SSE funcional, wikilink cross-galho (Dicionário de IA), Ver mais (3 links externos com URL), Veja também, Referências
- **Score verificar-nota (estimado):** 9/12 — falham E5 (sem ponte narrativa para 15 Reasoning models; "Veja também" não conta), E8 (apenas 1 callout `[!warning]`; seção Armadilhas em lista bullet simples), P1 (sem código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais") apontando para [[15 - Reasoning models e chain-of-thought]] com motivação concreta (ex: streaming e batching otimizam a inferência de modelos que geram tokens imediatamente — mas e quando o modelo precisa "pensar" antes de responder? Os reasoning models introduzem uma fase de raciocínio interno que muda completamente o perfil de TTFT e TPOT) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter a seção "## Armadilhas" (5 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
#### 15 - Reasoning models e chain-of-thought
- **Estado:** 225 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid (graph TD reasoning vs standard, 2× xychart-beta qualidade vs thinking + custo por modo), 2× tabela comparativa (sem/com reasoning; CoT prompting vs reasoning models; quando usar/não usar), inglês + tabela PT↔EN (9 termos), 1× [!warning] inline (CoT obsolescendo), seção Armadilhas (5 itens — lista bullet simples), código funcional JSON (OpenAI usage + Anthropic thinking config), wikilinks cross-galho (notas 12, 07, 01), Ver mais (3 links externos com URL), Veja também
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais") apontando para [[16 - Fine-tuning vs prompting vs RAG]] com motivação concreta (ex: agora que você entende quando ativar reasoning e como o modelo "pensa", o próximo passo é uma questão ainda mais fundamental — quando o reasoning nativo não basta e você precisa adaptar o próprio modelo: fine-tuning, prompting avançado e RAG são as três alavancas, e a escolha entre elas define o custo e a escalabilidade do sistema) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter a seção "## Armadilhas" (5 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
#### 16 - Fine-tuning vs prompting vs RAG
- **Estado:** 245 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 5× Mermaid (flowchart prompting, graph RAG, graph fine-tuning, árvore de decisão, xychart tempo de setup), tabelas comparativas (técnicas × camada/persistência/custo; comparativo 8 critérios; custo/setup simplificado), inglês + tabela PT↔EN (9 termos), 4 cenários práticos, seção Armadilhas (5 itens — lista bullet, sem `[!warning]`), wikilinks cross-galho (Dicionário de IA: RAG, fine-tuning, vector store, Hallucination; nota 21), Ver mais (3 links externos com URL), Veja também
- **Score verificar-nota (estimado):** 9/12 — falham E5 (sem ponte narrativa para 17; "Veja também" com link não conta), E8 (5 armadilhas como lista bullet simples, sem callouts `[!warning]` individuais), P1 (sem código-com-falha — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais") apontando para [[17 - O futuro dos LLMs — tendências 2026-2027]] com motivação concreta (ex: agora que você sabe quando adaptar um modelo existente, o próximo passo é entender para onde os próprios modelos estão indo — multimodalidade, contextos gigantes, modelos menores e mais capazes, e o que isso muda nas decisões de arquitetura) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter a seção "## Armadilhas" (5 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
#### 17 - O futuro dos LLMs — tendências 2026-2027
- **Estado:** 224 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 4× Mermaid (timeline autonomia, graph hybrid Transformer+SSM, xychart custo frontier, graph context engineering), tabelas comparativas (eras de autonomia; contexto × trade-off; multimodal 2024→2027; preços por ano; debates), inglês + tabela PT↔EN (11 termos), 2× [!question]- pedagógicos (autonomia real; skills obsoletas?), casos práticos (preço/task $5→$0.20, Devin/Claude Code/GitHub Copilot Agents, DeepSeek V2 choque de eficiência), wikilinks cross-galho (Dicionário de IA, notas 04/07/01/08), Ver mais (3 links externos com URL)
- **Score verificar-nota (estimado):** 9/12 — falham E5 (sem ponte narrativa para 18; "Veja também" com link não conta), E8 (4 armadilhas em lista bullet simples, sem `[!warning]` individuais), P1 (sem código — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais") apontando para [[18 - Como LLMs são treinados — pretraining, SFT, RLHF]] com motivação concreta (ex: as tendências que você acabou de ver — agentes, contexto infinito, modelos mais eficientes — só fazem sentido pleno quando você entende como esses modelos chegam à capacidade que têm; o próximo capítulo desce para o nível do treinamento) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter a seção "## Armadilhas" (4 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
  - Nota tem alta densidade de dados com data de validade (projeções para 2027, preços $/MTok por ano, versões DeepSeek V4/Qwen 3.6, afirmações como "em 2026 a taxa de falha caiu"): adicionar `[!warning]` ou `[!info]` de caducidade nas seções de tabela (especialmente "Tendência 4" e "Tendência 1") avisando que preços, versões e benchmarks envelhecem rápido
#### 18 - Como LLMs são treinados — pretraining, SFT, RLHF
- **Estado:** 256 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid (pipeline graph + RLHF loop + xychart volume por estágio), tabelas comparativas (4× por estágio: dados/custo/duração + escalada do treinamento + comparativo de modelos + quando fazer fine-tune), inglês + tabela PT↔EN (10 termos), 1× [!warning] (RLHF como causa de comportamentos chatos), 1× [!info], casos práticos (comparação de comportamento pretraining vs assistente, RLHF side effects, cenários de fine-tune), wikilinks cross-galho (Dicionário de IA, nota 06, nota 15, nota 16, nota 21), Ver mais (3 links externos com URL)
- **Score verificar-nota (estimado):** 9/12 — falham E5 (sem ponte narrativa para 19; "Veja também" com link não conta), E8 (apenas 1 [!warning]; precisa ≥3), P1 (sem código-com-falha — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais") apontando para [[19 - Evaluation de LLMs em produção]] com motivação concreta (ex: agora que você sabe como o modelo foi treinado e por que se comporta assim, o próximo passo é medir se ele está se saindo bem — avaliação em produção é o elo que fecha o ciclo treinamento → deploy → melhoria) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Adicionar ≥2 callouts `[!warning]` adicionais com armadilhas concretas (ex: "Fine-tuning não adiciona conhecimento — só ajusta comportamento; para conhecimento novo use RAG"; "DPO parece mais simples mas é sensível à qualidade do dataset de preferências — garbage in, garbage out") — ativa E8 (totaliza ≥3) e eleva score para 11/12
#### 19 - Evaluation de LLMs em produção
- **Estado:** 325 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid (graph TB 4 pilares + xychart ROI custo vs bug), inglês + tabela PT↔EN (12 termos), 1× [!warning] (LLM-as-judge — 4 sub-itens), [!tip] (A/B > golden set), [!example] (diagnóstico de maturidade), código funcional (YAML golden set + Python LLM-as-judge + Python Langfuse + pseudocode A/B), tabelas comparativas (tipos de tarefa × métrica; ferramentas 2026; métricas-alvo), wikilinks cross-galho (Dicionário de IA, nota 06, nota 18), Ver mais (3 links externos com URL), Veja também
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais") apontando para [[20 - Compressão de modelos — quantização e destilação]] com motivação concreta (ex: evaluation fecha o ciclo de medir — o próximo vetor de melhoria é reduzir o modelo em si; quantização e destilação permitem cortar custo e latência sem trocar de provider) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter a seção "## Anti-patterns" (6 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 (o único callout existente cobre LLM-as-judge; a seção de anti-patterns não usa callouts) e eleva score para 11/12
#### 20 - Compressão de modelos — quantização e destilação
- **Estado:** 227 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 4× Mermaid (graph INT4 bins, xychart VRAM por formato, graph professor→aluno, graph pipeline destilar+quantizar), tabelas comparativas (formatos GGUF/GPTQ/AWQ/NF4; bits×qualidade×melhor-via; situação×técnica), 5× [!warning] (INT4 degrada raciocínio, destilação tem custo, aluno herda vícios, quantizar modelos pequenos dói mais, ToS de API fechada), inglês + tabela PT↔EN (11 termos), casos práticos (Llama 3 70B: FP16→INT4; DistilBERT 97% BERT com 40% tamanho; T5 770M ≈ PaLM 540B), [!tip] resumo em 1 linha, wikilinks cross-galho (Dicionário de IA, notas 01/09/10/16/19/21), Ver mais (3 links externos com URL), referências com URLs (Google Research blog)
- **Score verificar-nota (estimado):** 10/12 — falham E5 (sem ponte narrativa para 21; wikilink em "Veja também" não conta) e P1 (sem código-com-falha — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Ver mais" ou "## Veja também") apontando para [[21 - Fine-tuning na prática — LoRA, QLoRA, DPO]] com motivação concreta (ex: agora que você sabe comprimir um modelo já pronto, o próximo passo é adaptá-lo a um domínio específico sem retreinar do zero — e o QLoRA faz exatamente isso: fine-tuna sobre um base já quantizado em INT4, combinando as duas técnicas desta nota num único pipeline de especialização barata) — fecha E5, único item de núcleo faltante, e eleva score para 11/12
#### 21 - Fine-tuning na prática — LoRA, QLoRA, DPO
- **Estado:** 243 linhas · fase: ausente (por decisão do spec — galho usa Blocos) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 4× Mermaid (LoRA graph LR, QLoRA TD, RLHF vs DPO, pipeline flowchart), tabelas comparativas (Por que fine-tuning; Quando usar qual), inglês + tabela PT↔EN (11 termos), casos práticos (RTX 3090 + 65B em 1 GPU, ferramentas 2026, pipeline típica), 1× [!warning] inline (fine-tuning ensina forma, não fatos), [!tip] resumo em 1 linha, [!question]- pedagógico (posto baixo), Veja também (4 wikilinks internos), Ver mais (3 links externos com URL), referências com URLs arxiv (4 papers primários)
- **Score verificar-nota (estimado):** 9/12 — falham E5 (última nota do galho, sem fechamento narrativo nem ponte para outros galhos de IA), E8 (seção "Armadilhas" com 7 itens em lista bullet simples, apenas 1 [!warning] inline), P1 (sem código-com-falha — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (por ser a última nota do galho) com fechamento do ciclo: o leitor acaba de ver como modelos são adaptados — o próximo passo natural é compreender agentes, RAG ou context engineering, com ponte explícita para esses galhos (ex: [[Anatomia de Agents]], [[RAG e Vector Databases]], [[Context Engineering]]) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter a seção "## Armadilhas" (7 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12

---

## 2. Anatomia de Agents

> Galho também sem `fase:` (organizado por sequência conceitual). Régua: núcleo mínimo + opcionais caso-a-caso.

### Notas

#### 01 - O que é um agent
- **Estado:** 190 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** 4× Mermaid (xychart chamadas LLM, graph TB anatomia mínima, flowchart LR determinístico vs autônomo, quadrantChart autonomia×previsibilidade), tabela comparativa (quando usar/não usar agent), casos práticos (cenário 3h da manhã + exemplos research/coding agent), 1× [!warning] (anti-pattern agent prematuro), 1× [!tip] (10 sinais de senior), inglês + tabela PT↔EN (12 termos), Veja também
- **Score verificar-nota (estimado):** 8/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Ver mais") apontando para [[02 - O loop ReAct e native tool use]] com motivação concreta (ex: agora que você sabe o que define um agent — o LLM decidindo o próximo step em runtime —, o próximo passo é ver o mecanismo exato desse loop: o padrão ReAct e como as tool calls nativas transformaram a teoria em prática de produção) — fecha E5, único item de núcleo faltante, e eleva score para 9/12
  - Adicionar URLs reais às referências na seção "## Referências" (Anthropic Building Effective Agents, OpenAI Practical Guide, ReAct paper em arxiv, Lilian Weng blog) — ativa L2 e eleva score para 10/12
  - Adicionar ≥2 callouts `[!warning]` adicionais com armadilhas concretas (ex: "Chamar pipeline de agent não elimina fragilidade — o blast radius da falha pode ser maior porque o LLM tem mais superfície de decisão"; "max_steps sem limite é a forma mais comum de fatura inesperada em produção") — ativa E8 (totaliza ≥3) e eleva score para 11/12
#### 02 - O loop ReAct e native tool use
- **Estado:** 277 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid (graph LR loop, sequenceDiagram App/LLM/Tool, xychart passos por padrão), tabela comparativa (stop reasons × ação; padrões além de ReAct; PT↔EN 11 termos), casos práticos (bug de produção com timeout + self-correction loop), 4 pitfalls narrativos (### sem callouts [!warning]), código funcional Python (hello world agent + self-correction), inglês + tabela PT↔EN, wikilinks cross-galho (Context Engineering, Anatomia dos LLMs, nota 11 harness), fontes com URL (arxiv:2210.03629, preprints 10.20944, arXiv:2603.25723), [!caution] (maturidade das fontes), [!info] (pitfalls → disciplina), [!summary] em 1 linha, Veja também, Ver mais
- **Score verificar-nota (estimado):** 9/12 — falham E5 (sem ponte narrativa para 03 Tool design; "Veja também" não conta), E8 (4 pitfalls como ### prosa, sem callouts `[!warning]` individuais), P1 (sem código-com-falha — o bug da abertura é narrado, não mostrado como snippet)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Como explicar em inglês" ou antes de "## Ver mais") apontando para [[03 - Tool design — princípios e categorias]] com motivação concreta (ex: o loop ReAct define o ritmo do agent — mas a qualidade de cada passo depende de como as tools são desenhadas; descrições vagas, schemas ambíguos e ausência de mensagens de erro são os vetores mais comuns de falha silenciosa num loop que funciona corretamente) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter os 4 pitfalls da seção "## Pitfalls do loop" (atualmente ### com prosa) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
  - Opcional: extrair o snippet do bug descrito na abertura (handler sem branch para `end_turn`) como bloco de código-com-falha explícito seguido do fix correto — ativa P1 e eleva score para 12/12
#### 03 - Tool design — princípios e categorias
- **Estado:** 264 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid (xychart compactação, quadrantChart risco×reversibilidade, flowchart categorizador), inglês + tabela PT↔EN (12 termos), 1× [!warning] + 1× [!danger], código-com-falha (padrão # Errado / # Certo em 3 blocos), tabela comparativa (5 categorias × exemplo+uso; métricas com thresholds), casos práticos (agent de suporte 55%→97% seleção correta), anti-patterns (lista bullet), wikilinks cross-galho (Segurança e Guardrails, Economia de Tokens, Agentes de Codificação/MCP)
- **Score verificar-nota (estimado):** 10/12 — falham E5 (sem ponte narrativa para 04 Memory; "Veja também" não conta) e E8 (apenas 1 `[!warning]`; seção "Anti-patterns" em lista bullet simples, `[!danger]` não supre)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Ver mais" ou "## Veja também") apontando para `[[04 - Memory em agents]]` com motivação concreta (ex: agora que você sabe como projetar cada tool para que o agent escolha certo, a próxima peça é a memória — porque sem ela o agent recomeça do zero a cada conversa, refazendo tool calls já executadas e perdendo contexto que determinou decisões anteriores) — fecha E5 e eleva score para 11/12
  - Converter a seção "## Anti-patterns" (5 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 (totaliza ≥3 junto com o `[!warning]` existente) e eleva score para 12/12
#### 04 - Memory em agents
- **Estado:** 219 linhas · fase: ausente · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** 3× Mermaid (graph TB tipos de memória, xychart-beta custo com/sem compactação, graph LR curto×longo prazo), tabela comparativa (tipos × onde mora × vida útil × tamanho), inglês + tabela PT↔EN (12 termos), casos práticos (sessão de debugging 180K tokens; custo por requisição), árvore de decisão (que memória usar), seção Anti-patterns (5 itens — lista bullet, sem [!warning]), wikilink cross-galho [[Memória de Agentes]] (L1 ✓), Veja também, Ver mais
- **Score verificar-nota (estimado):** 8/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Como explicar em inglês" ou "## Ver mais") apontando para [[05 - Planning — plan-then-execute, dynamic, hierarchical]] com motivação concreta (ex: a memória define o que o agent lembra entre passos — o planning define o que ele faz com esse conhecimento; sem um plano estruturado, ter memória apenas significa acumular contexto sem direção) — fecha E5 e eleva score para 9/12
  - Converter a seção "## Anti-patterns" (5 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 10/12
  - Adicionar URLs reais às referências do "## Ver mais" (MemGPT: https://arxiv.org/abs/2310.08560; Lilian Weng: https://lilianweng.github.io/posts/2023-06-23-agent/) — ativa L2 e eleva score para 11/12
#### 05 - Planning — plan-then-execute, dynamic, hierarchical
- **Estado:** 249 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** 3× Mermaid (graph TB comparativo de estratégias, xychart conclusão dentro do escopo, flowchart decisão de estratégia, sequenceDiagram plan-then-execute), tabela heurística (sinais × estratégia), tabela métricas (4 KPIs com alvos), casos práticos (JWT migration story + debug /payments + lançamento feature X), anti-patterns (lista bullet com 6 itens), inglês + tabela PT↔EN (11 termos), wikilinks cross-galho (Spec-Driven Development, Agentes de Codificação), Veja também, Ver mais
- **Score verificar-nota (estimado):** 8/12 — falham E5 (sem seção narrativa "O que vem a seguir"; link em "Veja também" não conta), E8 (anti-patterns como lista bullet simples, sem callouts `[!warning]`), P1 (sem código-com-falha — inaplicável para nota conceitual), L2 (arxiv IDs presentes mas sem URLs clicáveis https://)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Ver mais") apontando para [[06 - Multi-agent — orchestrator e sub-agents]] com motivação concreta (ex: planning resolve o problema de um agent sem âncora — mas quando a tarefa é grande demais para um único agent, o próximo passo é a orquestração: dividir o trabalho em sub-agents coordenados, o que exige um nível diferente de planejamento hierárquico) — fecha E5, único item de núcleo faltante, e eleva score para 9/12
  - Converter a seção "## Anti-patterns" (6 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 10/12
  - Adicionar URLs reais às referências do "## Ver mais" e "## Referências" (arxiv:2305.04091 → https://arxiv.org/abs/2305.04091; arxiv:2305.10601 → https://arxiv.org/abs/2305.10601; Anthropic Building Effective Agents com URL) — ativa L2 e eleva score para 11/12
#### 06 - Multi-agent — orchestrator e sub-agents
- **Estado:** 267 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 5× Mermaid (graph TB orquestrador, flowchart árv. decisão single×multi, sequenceDiagram orquestração, xychart-beta overhead × complexidade, flowchart contexto único?), tabelas comparativas (implementações 2026 por stack + métricas com alvos), inglês + tabela PT↔EN (12 termos), 1× [!warning] (regra de ouro do handoff), 1× [!tip] (single > multi), código-com-falha (# Errado / # Certo — handoff de histórico), código especialização por modelo, anti-patterns (lista bullet), wikilinks cross-galho (Dicionário de IA, Context Engineering, Spec-Driven Development, Economia de Tokens), Veja também, Ver mais
- **Score verificar-nota (estimado):** 10/12 — falham E5 (sem ponte narrativa para 07 Frameworks 2026; "Veja também"/"Ver mais" não contam) e L2 (referências sem URLs clicáveis — apenas "github.com/openai/swarm" mencionado como texto)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Ver mais") apontando para [[07 - Frameworks 2026]] com motivação concreta (ex: agora que você entende quando usar multi-agent e como projetar a orquestração, o próximo passo é ver quais frameworks de 2026 implementam esse padrão nativamente — e o que cada um sacrifica em expressividade, observabilidade e custo de coordenação) — fecha E5, único item de núcleo faltante, e eleva score para 11/12
  - Adicionar URLs reais às referências no "## Ver mais" e "## Referências" (Anthropic Building Effective Agents, Claude Agent SDK docs, Augment Code CIV, VeriMAP EACL 2026, OpenAI Swarm github.com/openai/swarm) — ativa L2 e eleva score para 12/12
  - Opcional: converter a seção "## Anti-patterns" (6 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 (totaliza ≥3 com o [!warning] existente); nota já aprovada sem isso
#### 07 - Frameworks 2026
- **Estado:** 319 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid (flowchart decisão, xychart semanas até prod, quadrantChart controle×velocidade), tabelas comparativas (7 frameworks × 4 critérios + métricas de adoção), inglês + tabela PT↔EN (11 termos), casos práticos (história LangChain 6 semanas + estimativas por stack), código funcional (4 blocos — Claude SDK, LangGraph, CrewAI, Pydantic AI), seção Anti-patterns (lista bullet), Veja também, Ver mais com URLs
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Ver mais") apontando para [[08 - Patterns comuns de agents]] com motivação concreta (ex: agora que você sabe escolher ou recusar um framework, o próximo passo é ver os patterns que qualquer stack precisa implementar — com ou sem framework; orquestração, retry, handoff e observabilidade aparecem sempre, e entender o pattern antes do framework evita o acoplamento cego) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter a seção "## Anti-patterns" (5 itens em lista bullet simples) para callouts `[!warning]` individuais — ativa E8 e eleva score para 11/12
  - Adicionar `[!info]` ou `[!warning]` de caducidade no topo da seção "## O panorama em uma tabela" avisando que rankings de popularidade, posicionamentos e estimativas de tempo-até-produção envelhecem em ~6 meses no ecossistema de 2026 — **nota de panorama com alta densidade de dados com data de validade** (popularidade LangGraph, versões Claude Agent SDK/Pydantic AI, estimativas em semanas)
#### 08 - Patterns comuns de agents
- **Estado:** 251 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid (graph TB 6 patterns, xychart-beta latência por pattern, flowchart LR simples→médio→complexo), tabela comparativa (heurística rápida sinal × pattern), inglês + tabela PT↔EN (11 termos), 1× [!warning] composto (5 itens over-engineering agrupados), código funcional Python (workflow híbrido), casos práticos (demo triagem de tickets 8s vs 0,3s na abertura + exemplos por pattern), [!question] (heurística rápida), [!quote] Anthropic, Veja também, Ver mais (3 referências nomeadas sem URL)
- **Score verificar-nota (estimado):** 8/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Ver mais") apontando para nota 09 do galho (Evaluation de agents) com motivação concreta — fecha E5 (único item de núcleo faltante) e eleva score para 9/12
  - Expandir o único `[!warning]` composto (5 sub-itens agrupados sob um único callout) em ≥3 callouts `[!warning]` individuais com título descritivo — ativa E8 e eleva score para 10/12
  - Adicionar URLs reais às referências em "## Ver mais" e "## Referências" (Anthropic Building Effective Agents, OpenAI Practical Guide, LangChain blog supervisor patterns) — ativa L2 e eleva score para 11/12
#### 09 - Evaluation de agents
- **Estado:** 278 linhas · fase: ausente · status: growing
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (2 diagramas) · Casos práticos (≥2) · Inglês · PT↔EN · Anti-patterns (bullets, não [!warning]) · LLM-as-judge
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção "O que vem a seguir" (antes de "## Ver mais") com ponte narrativa para nota 10 (Workflow vs Agent — quando usar cada um) — fecha E5, único item de núcleo faltante
  - Converter os 6 bullets de "## Anti-patterns" em ≥3 callouts `[!warning]` individuais com título descritivo — ativa E8 e eleva score para 10/12
#### 10 - Workflow vs Agent — quando usar cada um
- **Estado:** 190 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid (graph TD árvore de decisão + xychart-beta 5 dimensões), pseudo-code templates (workflow receita + agent loop), tabela comparativa (PT↔EN 11 termos), casos práticos (abertura 3 semanas + exemplos por categoria), inglês + tabela PT↔EN, seção "Custos e riscos" (5 bullets — sem `[!warning]`), padrão híbrido (orchestrator-workers), wikilinks cross-galho (Dicionário de IA, Agentes de Codificação, Economia de Tokens, notas 06/09, AI Engineering Stack), Ver mais (3 referências com fonte nomeada), fontes com URL (Building Effective Agents), Veja também
- **Score verificar-nota (estimado):** 9/12 — falham E5 (sem ponte narrativa para 11 Harness engineering; "Veja também" não conta), E8 (5 riscos em lista bullet simples na seção "## Custos e riscos", sem callouts `[!warning]` individuais), P1 (pseudo-code funcional/ilustrativo presente, sem código-com-falha — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Ver mais") com ponte para [[11 - Harness engineering — a terceira camada]] com motivação concreta (ex: agora que você sabe quando escolher workflow ou agent, a próxima decisão é onde esse código vive — o harness é a camada que envolve o loop do agent com retry, tracing, cost guard e human-in-the-loop; sem ele, a decisão workflow-vs-agent fica no papel e os riscos de custo e loop infinito desta nota se materializam em produção) — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Converter a seção "## Custos e riscos" (5 bullets: tokens, avaliação, loops infinitos, debug difícil, falhas criativas) para callouts `[!warning]` individuais com título descritivo — ativa E8 e eleva score para 11/12
#### 11 - Harness engineering — a terceira camada
- **Estado:** 217 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: growing / progress: done
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 4× Mermaid (graph LR três eras, graph TB anatomia harness, graph TD 6 dimensões analíticas, xychart-beta SWE-bench harnesses), tabela de taxonomias (6 linhas × 4 colunas), tabela de mapeamento vault (9 funções × galho), inglês + tabela PT↔EN (11 termos), casos práticos (v1→v2 regression 12% na abertura; SWE-bench 8%→55% mesmo modelo), 1× [!warning] ("O harness NÃO é uma quarta forma"), 1× [!caution] (honestidade sobre preprint), [!question]- pedagógico (por que tantas taxonomias), [!info] (analogia CPU/SO), [!example] (onde isto morde no vault), [!summary], wikilinks cross-galho (Context Engineering, Memória de Agentes, Evaluation, Claude Code, MCP, Segurança e Guardrails, Observability), fontes com URL (5 referências externas com hiperlinks)
- **Score verificar-nota (estimado):** 9/12 — falham E5 (última nota do galho, sem fechamento narrativo nem ponte para outros galhos de IA; "Veja também" não conta), E8 (apenas 1 callout `[!warning]`, precisa ≥3), P1 (sem código-com-falha — inaplicável para nota conceitual pura)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Como explicar em inglês" ou antes de "## Ver mais"), por ser a última nota do galho: fechar o ciclo do galho Anatomia de Agents e abrir pontes explícitas para os galhos que aprofundam as dimensões do harness (ex: "você acabou de ver que o harness é a costura entre os galhos — Context Engineering cuida do budget, Memória de Agentes externaliza o estado, Evaluation fecha o loop de melhoria; escolha o próximo galho pelo ponto de maior fricção no seu sistema atual") — fecha E5, único item de núcleo faltante, e eleva score para 10/12
  - Adicionar ≥2 callouts `[!warning]` adicionais com armadilhas concretas (ex: "Build to delete — um hook escrito pra compensar limitação do modelo anterior pode trabalhar contra o próximo; documente o motivo de cada compensação, não só o quê"; "Benchmarks sem HarnessCard medem variável confundida: o scaffold pode explicar mais do ganho do que o modelo — checar antes de atribuir melhoria ao 'modelo novo'") — ativa E8 (totaliza ≥3) e eleva score para 11/12

---

## 3. Spec-Driven Development

> Galho sem `fase:` (sequência conceitual). Régua: núcleo mínimo + opcionais caso-a-caso.

### Notas

#### 01 - O problema do vibe coding em produção
- **Estado:** 401 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 5× Mermaid (loop vibe coding, xychart produtividade vibe×SDD, graph tech debt exponencial, graph LR vibe vs SDD, mindmap vulnerabilidades), tabelas comparativas (sintomas×mecanismo×consequência; contexto OK/não para vibe; SDD resolve; paradoxo do tempo; distribuição de tempo em equipes), casos práticos (startup fintech 4 devs + bug breach em julho, analogia empreiteiro, analogia compilador), 5× [!warning] (Veracode 45%, Salesforce Ben 2026, Gartner 67%, CIO context drift, IBM breach $4.88M), [!question] diagnóstico rápido, [!example] casos, [!note] insights, [!quote] Augment Code, checklist interativo de diagnóstico de equipe
- **Score verificar-nota (estimado):** 7/12 — falham E5 (sem seção "O que vem a seguir" nomeando nota 02 explicitamente — a frase "as próximas notas desta trilha" é genérica), E6 (sem seção "Como explicar em inglês"), E7 (sem tabela PT↔EN), P1 (sem código — inaplicável para nota conceitual), L2 (referências sem URLs clicáveis — arxiv:2512.11922 e demais fontes listadas sem https://)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Veja também") apontando explicitamente para [[02 - O que é Spec-Driven Development]] com motivação concreta (ex: "entendido o problema e seus mecanismos, o passo seguinte é nomear a solução com precisão — o que exatamente é SDD, o que o distingue de metodologias anteriores e por que a definição importa antes de qualquer ferramenta ou processo") — fecha E5 e eleva score para 8/12
  - Adicionar seção "Como explicar em inglês" com tabela PT↔EN cobrindo os termos centrais da nota (vibe coding, tech debt, spec, context drift, acceptance criteria, regression, blast radius, velocity mismatch, code review, hallucination) — ativa E6+E7 e eleva score para 10/12
  - Adicionar URLs reais às referências (arxiv:2512.11922 → https://arxiv.org/abs/2512.11922; Veracode report em https://www.veracode.com/resources/state-of-software-security; GitClear em https://www.gitclear.com; Augment Code post com URL) — ativa L2 e eleva score para 11/12
#### 02 - O que é Spec-Driven Development
- **Estado:** 401 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** 4× Mermaid, múltiplas tabelas comparativas (SDD×waterfall, SDD×TDD×BDD, quando SDD compensa), casos práticos (≥4: spec→testes, timeline 2025-2026, checklist de adoção, pipeline nas ferramentas), wikilink cross-galho ([[Context Engineering]]), [!quote] Augment Code, [!note] (analogia do arquiteto)
- **Score verificar-nota (estimado):** 6/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Veja também") apontando explicitamente para [[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source]] com motivação concreta (ex: "o espectro spec-optional → spec-as-source foi introduzido nesta nota — a nota 03 desce ao nível de cada ponto: o que muda na prática ao migrar de spec-anchored para spec-first, e quando o custo do rigor adicional compensa") — fecha E5 (núcleo faltante) e eleva score para 7/12
  - Adicionar URLs reais às referências da seção "## Referências" (GitHub Blog Spec Kit, Augment Code guide, Microsoft for Developers, Martin Fowler análise comparativa, Amazon Kiro launch, OpenSpec v0.3, DeepLearning.AI course) — ativa L2 e eleva score para 8/12
  - Adicionar ≥3 callouts `[!warning]` individuais com armadilhas concretas (ex: "spec sem acceptance criteria mensuráveis vira documentação decorativa — o agente preencherá a ambiguidade com alucinação plausível"; "spec fora do repositório quebra a rastreabilidade — Notion/Confluence/Google Docs tornam impossível correlacionar mudança de requisito com mudança de código"; "misturar outcomes com decisões técnicas contamina a spec — 'usar Stripe com webhook idempotente' pertence ao Plan, não à Specify") — ativa E8 e eleva score para 9/12
  - Adicionar seção "Como explicar em inglês" com tabela PT↔EN cobrindo os termos centrais (especificação/specification, contrato/contract, critério de aceitação/acceptance criteria, source of truth, fora do escopo/out-of-scope, versionamento/versioning, artefato/artifact, validação/validation, entregável/deliverable, rastreabilidade/traceability) — ativa E6+E7 e eleva score para 11/12
#### 03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source
- **Estado:** 399 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** 2× Mermaid (graph LR espectro + xychart custo acumulado 12 meses), tabelas comparativas (4 níveis × custo; sinais de nível errado; fatores organizacionais × nível recomendado), casos práticos (OAuth nos 3 níveis + mistura de níveis por área + jornada de evolução mês a mês), wikilink cross-galho ([[Dicionário de IA#vibe coding]]), 2× [!tip] (gatilhos para subir + regra prática), código funcional (markdown spec-anchored + YAML spec-as-source)
- **Score verificar-nota (estimado):** 6/12 — passam E1 E2 E3 E4 P2 L1; falham E5 E6 E7 E8 P1 L2
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Veja também") apontando para [[04 - Fase Specify — definindo outcomes e constraints]] com motivação concreta (ex: "agora que você sabe em qual nível operar, o próximo passo é entrar na prática: a Fase Specify é onde o rigor escolhido se materializa em outcomes mensuráveis, constraints explícitos e acceptance criteria que o agente pode validar") — fecha E5 (núcleo faltante) e eleva score para 7/12
  - Adicionar URLs reais às referências — atualmente 20+ fontes listadas sem hiperlinks (ex: GitHub Blog → https://github.blog/ai-and-ml/github-copilot/spec-driven-development-with-ai/; Kiro → https://kiro.dev; Tessl → https://tessl.io; Martin Fowler → URL do post no martinfowler.com) — fecha L2 (núcleo Fontes faltante) e eleva score para 8/12
  - Adicionar ≥3 callouts `[!warning]` individuais com armadilhas concretas (ex: "spec-as-source sem cultura de spec-anchored estabelecida falha por orfanamento da automação — o time sabe como rodar o gerador mas não como escrever a spec que vai nele"; "spec-first em projetos com mudança frequente vira documentação de comissão em 3-6 meses — agente em sessões futuras usa spec desatualizada como contexto, produzindo código que contradiz o que já existe"; "mistura de níveis sem registro arquitetural explícito gera inconsistência silenciosa — qual área usa qual nível deve estar documentada e revisada periodicamente") — ativa E8 e eleva score para 10/12
  - Adicionar seção "Como explicar em inglês" com tabela PT↔EN cobrindo os termos centrais (spec estática/static spec · spec viva/living spec · spec como fonte/spec-as-source · fonte autoritativa/authoritative source · critério de aceitação/acceptance criteria · drift de spec/spec drift · rastreabilidade/traceability · código derivado/derived code · checklist de aceitação/acceptance checklist · versionamento/versioning) — ativa E6+E7 e eleva score para 12/12
#### 04 - Fase Specify — definindo outcomes e constraints
- **Estado:** 407 linhas · fase: ausente · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** Mermaid (4×: xychart custo por fase, mindmap NFRs, 2× graph comunicação PM↔Eng↔Agente), tabelas comparativas (4 níveis Specify/Plan/Tasks/Implement; 6 elementos canônicos; AC vago×verificável; anti-patterns; métricas de qualidade), casos práticos (spec completa "Refund de pagamentos" + machine-readable YAML + AC vago vs verificável), 1× [!warning] (spec gerada por IA), [!note], [!tip] (teste "explica para outro engenheiro"), wikilinks cross-galho (Context Engineering nota 11)
- **Score verificar-nota (estimado):** 7/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Veja também") apontando para [[05 - Fase Design e Plan — arquitetura e decomposição]] com motivação concreta (ex: "agora que a spec define o quê e o porquê com precisão, o próximo passo é traduzir esses outcomes e constraints em arquitetura — a Fase Design e Plan decide o como, e faz isso com acesso ao contexto exato que você acabou de escrever") — fecha E5 (núcleo faltante) e eleva score para 8/12
  - Adicionar URLs reais a pelo menos 1 referência — ex: Augment Code → https://augmentcode.com/blog/what-is-spec-driven-development ou GitHub Spec Kit → https://github.blog/ai-and-ml/github-copilot/spec-driven-development-with-ai/ — fecha L2 (núcleo Fontes) e eleva score para 9/12
  - Adicionar ≥2 callouts `[!warning]` adicionais com armadilhas concretas (ex: "spec correta mas sem out-of-scope declarado permite que o agente expanda o escopo silenciosamente"; "open questions não documentadas são decididas pelo agente com inferências plausíveis mas não validadas pelo PM") — ativa E8 (totaliza ≥3) e eleva score para 10/12
#### 05 - Fase Design e Plan — arquitetura e decomposição
- **Estado:** 420 linhas · fase: ausente · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** Mermaid (2×: componentes graph LR + DAG tasks), tabelas comparativas (6+: Specify×Plan, NFR×constraint, granularidade, múltiplos plans, revisores, anti-patterns, métricas), casos práticos (ADR exemplo, task T1 completa, pattern produtivo humano+LLM, narrativa de plan), callouts pedagógicos ([!tip] regra 2-4h, [!example] ×2), template canônico
- **Score verificar-nota (estimado):** 5/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" antes de "## Veja também" apontando para [[06 - Fase Implement — execução disciplinada]] com motivação concreta (ex: "agora que o plan está aprovado — ADRs fechados, contratos definidos, DAG de tasks com acceptance criteria — o próximo capítulo é executar esse plan de forma disciplinada; a Fase Implement define como o agente usa esses documentos como contexto imutável durante o código") — fecha E5 e eleva score para 6/12
  - Adicionar URLs reais a pelo menos 1 referência — ex: Microsoft → https://devblogs.microsoft.com/develop-from-the-cloud/spec-driven-development-with-github-copilot/ ou Nygard ADR → https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions — fecha L2 (também fecha o núcleo Fontes) e eleva score para 7/12
  - Converter seção "## Anti-patterns" (atualmente tabela com 7 itens) para callouts `[!warning]` individuais (ex: "Plan que vira pseudocódigo invade Implement", "Tasks de 8h sem AC: agente decide when done subjetivamente", "NFRs sem mapeamento técnico viram surpresa em prod") — ativa E8 e eleva score para 8/12
  - Adicionar wikilink cross-galho em seção pertinente (ex: no parágrafo de contratos de interface → [[Context Engineering]] ou no parágrafo sobre tasks como contexto → [[Economia de Tokens]]) — ativa L1 e eleva score para 9/12 (gate)
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (8-10 termos: spec/plan/ADR/task/acceptance criteria/decomposition/dependency/interface/component/constraint) — ativa E6 + E7 e eleva score para 11/12
#### 06 - Fase Implement — execução disciplinada
- **Estado:** 393 linhas · fase: ausente · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** 5× Mermaid (regra de ouro, spec drift detection, loop diagnóstico, review de código, commit rastreável), tabelas comparativas (vibe vs SDD, contexto por fonte, anti-patterns, métricas da fase), casos práticos (Python pytest com 3 ACs mapeados da spec, commit message rastreável, estrutura de diretório projeto/specs/plan/src), código funcional (Python pytest + commit message)
- **Score verificar-nota (estimado):** 5/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção "## O que vem a seguir" com parágrafo narrativo apontando para [[07 - Fase Validate — spec como contrato executável]] — fecha E5 (núcleo faltante) e eleva score para 6/12
  - Adicionar URLs reais a pelo menos 1 referência (ex: Forsgren et al. *Accelerate* → https://itrevolution.com/accelerate-book ou DORA 2025 → https://dora.dev/research) — fecha Fontes do núcleo (L2) e eleva score para 7/12
  - Converter a tabela "## Anti-patterns da fase Implement" (8 itens) para callouts `[!warning]` individuais (ex: "Pular tasks — fazer várias juntas", "Não escrever teste antes de implementar", "Decidir silenciosamente casos não cobertos pela spec") — ativa E8 e eleva score para 8/12
  - Adicionar wikilink cross-galho em parágrafo pertinente (ex: seção "Carregar o contexto certo" → [[Context Engineering]] ou seção "Sessões por task" → [[Economia de Tokens]]) — ativa L1 e eleva score para 9/12 (gate)
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (10-12 termos: spec/plan/task/acceptance criteria/test-first/spec drift/atomic task/scope creep/commit traceability/spec-anchored) — ativa E6 + E7 e eleva score para 11/12
#### 07 - Fase Validate — spec como contrato executável
- **Estado:** 395 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: evergreen · progress: complete
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (1× graph LR dos 5 gates), casos práticos (5+ exemplos: pytest AC marking, k6 NFR gate, drift detector Python, GitHub Actions pipeline completo, living-spec PR workflow, tabela de métricas com alvos), código funcional (YAML CI + Python pytest + bash grep + pseudocódigo drift detector — nenhum com falha), tabelas comparativas (ferramentas 2026, living-spec PR, NFR gates executáveis, anti-patterns × consequência, métricas × sinal de problema), [!tip] (LLM critic como gate auxiliar)
- **Score verificar-nota (estimado):** 6/12 — passam E1 E2 E3 E4 P2; falham E5 (sem ponte narrativa para 08 Ferramentas SDD; "Veja também" com links intra-galho não conta), E6 (sem seção "Como explicar em inglês"), E7 (sem tabela PT↔EN), E8 (anti-patterns em tabela, nenhum callout `[!warning]` na nota inteira), P1 (código funcional mas sem código-com-falha — inaplicável para nota de processo), L1 (wikilinks só dentro do galho SDD — sem cross-galho para Economia de Tokens, Context Engineering, etc.), L2 (14 referências nomeadas sem URLs clicáveis — arxiv:2512.08769 e demais sem https://)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Veja também") apontando para [[08 - Ferramentas SDD — Kiro, Spec Kit, OpenSpec, Tessl]] com motivação concreta (ex: "você acabou de ver os 5 gates que tornam a spec executável como contrato de CI — o próximo passo é ver quais ferramentas de 2026 implementam esses gates nativamente, e o que Kiro, Spec Kit, OpenSpec e Tessl sacrificam em flexibilidade ou custo de adoção") — fecha E5 (único item de núcleo faltante) e eleva score para 7/12
  - Adicionar URLs reais a ≥1 referência (ex: arxiv:2512.08769 → https://arxiv.org/abs/2512.08769; k6 → https://k6.io; OWASP Zap → https://owasp.org/www-project-zap/) — ativa L2 e eleva score para 8/12
  - Converter a tabela "## Anti-patterns na fase Validate" (7 itens) para callouts `[!warning]` individuais com título descritivo — ativa E8 e eleva score para 9/12 (gate)
  - Adicionar wikilink cross-galho em parágrafo pertinente (ex: seção "Gate 3 NFR" → [[Economia de Tokens]] para NFR de custo; ou seção "Drift gate" → [[Context Engineering]] dado que drift = contexto stale) — ativa L1 e eleva score para 10/12
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (10-12 termos: validação/validation, contrato executável/executable contract, critério de aceitação/acceptance criteria, desvio/drift, cobertura/coverage, pipeline de CI/CI pipeline, gate de qualidade/quality gate, NFR/non-functional requirement, detecção de drift/drift detection, especificação viva/living spec) — ativa E6+E7 e eleva score para 12/12
#### 08 - Ferramentas SDD — Kiro, Spec Kit, OpenSpec, Tessl
- **Estado:** 361 linhas · fase: ausente (galho não usa `fase:` — correto) · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** Mermaid (2×), tabelas comparativas (múltiplas), casos práticos (AWS Industries Blog + tabelas Quando usar por ferramenta), código funcional (CLI + YAML + Markdown)
- **Score verificar-nota (estimado):** 6/12 — E5 ausente (só "Veja também", não conta), E6/E7 ausentes (sem inglês/PT↔EN), E8 ausente (sem callouts `[!warning]`), P1 ausente (sem código-com-falha), L2 ausente (referências sem URLs clicáveis)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Veja também") apontando para [[09 - SDD com agentes — coordinator, implementor, validator]] com motivação concreta (ex: você escolheu a ferramenta — o próximo nível é entender como os agentes se dividem o trabalho dentro dela; coordinator, implementor e validator são os papéis que fazem o pipeline SDD funcionar em modo autônomo) — fecha E5 (núcleo faltante) e eleva score para 7/12
  - Adicionar URLs reais nas referências (github.com/github/spec-kit, kiro.dev, martinfowler.com, etc.) — ativa L2 e eleva score para 8/12
  - Adicionar ≥3 callouts `[!warning]` com armadilhas concretas (ex: "Kiro e Spec Kit em paralelo causam conflito de convenção — escolha um por projeto"; "Tessl exige domínio formalmente modelável: domínio criativo ou exploratório trava na definição da spec antes de gerar código"; "Kiro sem steering files perde o principal diferencial — configurar .kiro/steering/ antes de começar é obrigatório") — ativa E8 e eleva score para 9/12 (gate)
  - Nota contém dados com data de validade (⚠️ validade ~trimestral): contagem de stars do Spec Kit (88k, abr/2026); previsão end-of-support Q Developer (30/abr/2027); recomendação datada "jun 2026". Adicionar `[!warning]` de caducidade na seção "## GitHub Spec Kit" e em "## A recomendação de start"
#### 09 - SDD com agentes — coordinator, implementor, validator
- **Estado:** 419 linhas · fase: ausente (galho sem `fase:` — não é falha) · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** 2× Mermaid (graph TB CIV + xychart-beta tokens), tabelas comparativas (implementações por stack + métricas de saúde CIV + anti-patterns), casos práticos (feature de reembolso end-to-end completa), 1× [!warning] (validator com prompt genérico), [!tip] (matemática do isolamento), [!quote] VeriMAP, código funcional Python (coordinator loop + implementor + validator com Anthropic SDK), código YAML (tasks.yml DAG completo com T1-T5), variantes avançadas (hierarchical + specialist + LLM critic encadeado), Veja também
- **Score verificar-nota (estimado):** 5/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Veja também") apontando para [[10 - Integração com context engineering — specs como contexto persistente]] com motivação concreta (ex: "o coordinator injeta contexto isolado em cada implementor — mas como persistir spec, plan e estado do DAG entre sessões de forma que o context engineering não duplique o que o SDD já define? A nota 10 resolve o acoplamento entre as duas disciplinas") — fecha E5 (núcleo faltante) e eleva score para 6/12
  - Adicionar URLs reais nas referências (arxiv:2512.08769 → https://arxiv.org/abs/2512.08769; Anthropic Claude Agent SDK → https://docs.anthropic.com/en/docs/agents; Kiro custom subagents → https://kiro.dev/docs/agents/) — fecha L2 (núcleo Fontes faltante) e eleva score para 7/12
  - Adicionar ≥2 callouts `[!warning]` adicionais com armadilhas concretas (ex: "DAG com paralelo_safe: true em tasks que compartilham arquivo gera race condition silenciosa — escopo de arquivos no tasks.yml deve ser mutuamente exclusivo entre tasks paralelas"; "Coordinator que recebe transcrição completa dos implementors perde o isolamento de contexto — handoff deve ser só o veredicto estruturado do validator, nunca o histórico de raciocínio") — ativa E8 (totaliza ≥3) e eleva score para 8/12
  - Adicionar wikilink cross-galho em parágrafo pertinente (ex: na seção "Custo de tokens: CIV vs single-agent" → [[Economia de Tokens]] ou na menção de "context rot" no parágrafo da arquitetura CIV → [[Context Engineering]]) — ativa L1 e eleva score para 9/12 (gate)
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (10-12 termos: coordenador/coordinator, implementador/implementor, validador/validator, grafo acíclico dirigido/directed acyclic graph, isolamento de contexto/context isolation, tarefa/task, critério de aceitação/acceptance criterion, paralelismo/parallelism, replanejamento/replanning, escalonamento/escalation) — ativa E6+E7 e eleva score para 11/12
#### 10 - Integração com context engineering — specs como contexto persistente
- **Estado:** 401 linhas · fase: ausente · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** Mermaid (2×: graph TB camadas + sequenceDiagram CIV), casos práticos (outbox/Redis inconsistência, compactação ingênua, Augment Code case study −64% tokens), tabelas comparativas (SDD × pilares de context eng; AGENTS.md × spec; papel CIV × contexto; anti-patterns; métricas sem/com SDD), 1× [!warning] (spec stale), 1× [!tip] (spec não compacta), código funcional (Python builder de contexto, YAML drift gate, pseudocódigo JIT retrieval), wikilinks internos (notas 03 e 09 do mesmo galho), Veja também
- **Score verificar-nota (estimado):** 6/12 — falham E5 (sem ponte narrativa; "Veja também" não conta), E6 (sem seção inglês), E7 (sem tabela PT↔EN), E8 (apenas 1 [!warning]; anti-patterns em tabela, não callouts), P1 (sem código-com-falha), L1 (links são intra-galho SDD, sem wikilink para galho Context Engineering), L2 (referências sem URLs)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo "O que vem a seguir" (antes de "## Veja também") apontando para [[11 - Guia de implementação SDD — do zero ao projeto]] com motivação concreta (ex: agora que você entende como SDD e context engineering se integram teoricamente, o próximo passo é colocar isso em prática — o guia de implementação traduz os princípios desta nota em passos concretos, do primeiro spec até o drift gate em CI) — fecha E5 (núcleo faltante mais crítico) e eleva score para 7/12
  - Adicionar URLs nas referências: pelo menos Kiro (kiro.dev/docs/steering-files), Anthropic (docs.anthropic.com/context-engineering), Augment Code (augmentcode.com/blog) — ativa L2 e eleva score para 8/12
  - Adicionar wikilink cross-galho para o galho [[Context Engineering]] em parágrafo pertinente (ex: na seção "A correspondência entre SDD e context engineering" ao mencionar "Context engineering tem quatro pilares") — ativa L1 e eleva score para 9/12 (gate)
  - Converter a tabela "Anti-patterns na integração" (8 itens) para ≥3 callouts `[!warning]` individuais com as armadilhas mais críticas (ex: "Spec gigantesca >3K tokens", "Compactação que toca spec", "Spec depois do código retroativa falsa") — ativa E8 e eleva score para 10/12
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (10-12 termos: especificação/specification, contexto persistente/persistent context, recuperação cirúrgica/JIT retrieval, compactação/compaction, âncora de contexto/context anchor, região protegida/protected region, drift de especificação/spec drift, arquivo de agentes/agents file, tarefa/task, memória externa/external memory) — ativa E6+E7 e eleva score para 12/12
#### 11 - Guia de implementação SDD — do zero ao projeto
- **Estado:** 431 linhas · fase: ausente (galho não usa `fase:`) · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** casos práticos (health check, brownfield incremental, CIV), tabelas comparativas (fit/quando não adotar/resistências do time/métricas de saúde SDD/sinais de sucesso e falha), 1× [!warning] (não pular etapas para spec-as-source), 1× [!question] (SDD faz sentido?), código funcional (bash specify-cli + YAML CI + markdown templates AGENTS.md/PR/workflow)
- **Score verificar-nota (estimado):** 4/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com problema/cenário antes de "## Pré-requisitos" (ex: "Você leu sobre SDD, faz sentido — mas como começa na prática? Instala um CLI? Escreve uma spec agora? Treina o time antes ou depois?") — ativa E2
  - Adicionar seção narrativa "O que vem a seguir" antes de "## Veja também" apontando para [[12 - Debates — spec-as-source vs pragmatismo]] com motivação concreta (ex: depois de 12 semanas de adoção, o debate que volta com força é se vale subir para spec-as-source — e as opiniões do campo são fortes nos dois lados) — ativa E5
  - Adicionar URLs reais às referências (GitHub Blog, Microsoft for Developers, Augment Code, Zencoder, DeepLearning.AI/JetBrains, BMAD, Hashrocket) — ativa L2
  - Expandir para ≥3 callouts `[!warning]` individuais (já há 1 sobre pular etapas; adicionar: "adoção parcial contamina o restante — se um dev ignora a spec, o CIV falha silenciosamente"; "spec retroativa descreve o comportamento atual, incluindo os bugs — revise com cuidado antes de assumir como spec desejada"; "task grande demais quebra a regra das 3h — CIV falha por timeout ou contexto insuficiente") — ativa E8
  - Adicionar ≥1 diagrama Mermaid (ex: flowchart das semanas 0→12 ou sequenceDiagram spec→plan→tasks→implement→gate) — ativa E3
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN (~10 termos: especificação/specification, critério de aceitação/acceptance criterion, desvio/drift, âncora/anchor, validação/validation, tarefa/task, granularidade/granularity, adoção incremental/incremental adoption, retroativa/retroactive, manutenção de spec/spec maintenance) — ativa E6+E7
#### 12 - Debates — spec-as-source vs pragmatismo
- **Estado:** 401 linhas · fase: ausente (galho não usa fase:) · status: evergreen
- **Núcleo:** TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** Mermaid (xychart ROI por contexto), tabelas comparativas (×6: waterfall×SDD, SDD×BDD×TDD, quando não usar, casos de falha, convergência defensores×céticos, híbridos), casos práticos (ROI Augment Code 6 meses, crise Salesforce Ben 2026, 3 padrões híbridos)
- **Score verificar-nota (estimado):** 5/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção "O que vem a seguir" com ponte narrativa para outros galhos de IA (ex: os três princípios — intent explícito, validação mecânica, contexto persistente — reaparecem em [[Agentes de Codificação]], [[Context Engineering]] e [[Prompt Engineering]]; fechar o ciclo apontando quais galhos aplicam esses princípios na prática) — fecha E5 (núcleo), eleva score para 6/12
  - Adicionar URLs reais às 14 referências (arxiv:2512.11922, arxiv:2506.14981, Andrej Karpathy, Salesforce Ben, Augment Code, Martin Fowler, Simon Willison, ThoughtWorks Radar, Stack Overflow Developer Survey 2026) — ativa L2, eleva score para 7/12
  - Adicionar ≥1 wikilink cross-galho para outro galho de IA na "Posição de fechamento" ou no corpo (ex: [[Agentes de Codificação]] ao mencionar multi-agent, [[Context Engineering]] ao mencionar contexto persistente) — ativa L1, eleva score para 8/12
  - Converter ≥3 limites/armadilhas (ex: "specs gigantescas que ninguém lê", "gates muito rígidos em fase de adoção", "adoção forçada sem buy-in") da seção "Quando o método te trai" para callouts `[!warning]` individuais — ativa E8, eleva score para 9/12

---

## 4. Economia de Tokens

> Galho **usa `fase:`** (05–22 = Adepto; 01–04 SEM fase). Régua aplica `fase:` como núcleo e **piso de linhas por fase** (Adepto ≥400 = T2). Notas 01–04 sem `fase:` = gap a registrar.

### Notas

#### 01 - O problema — por que tokens custam dinheiro
- **Estado:** 122 linhas · fase: AUSENTE (gap) · status: evergreen
- **Núcleo:** Frontmatter+fase ✗ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** Mermaid (graph TD custo prefill/decode), tabela comparativa (fases × recurso; input/output por provider; 5 vilões × % gasto), casos práticos (cenário real 8h de trabalho com custo por fase), armadilhas (lista bullet — sem callouts [!warning]), Veja também
- **Score verificar-nota (estimado):** 5/12 — falham E2 (abertura inicia com definição "O que é"), E5 (sem ponte narrativa; "Veja também" não conta), E6 (sem seção inglês), E7 (sem tabela PT↔EN), E8 (armadilhas como lista bullet, sem [!warning] individuais), P1 (sem código-com-falha), L2 (referências sem URLs)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar `fase: Iniciado` ao frontmatter — fecha o gap de fase das notas 01-04 deste galho
  - Adicionar abertura com cenário/problema concreto antes de "## O que é" (ex: engenheiro que recebe fatura de $25 no fim do dia sem entender de onde veio) — ativa E2
  - Adicionar seção/parágrafo narrativo "O que vem a seguir" apontando para `[[02 - Anatomia do gasto — input, output e reasoning]]` com motivação (ex: agora que você sabe que tokens custam por causa do hardware, o próximo passo é decompor o gasto em input, output e reasoning — cada um com perfil de custo distinto) — ativa E5
  - Converter "## Armadilhas" (4 itens em lista bullet) para callouts `[!warning]` individuais — ativa E8
  - Adicionar URLs reais às referências (anthropic.com/pricing e artificialanalysis.ai) — ativa L2
#### 02 - Anatomia do gasto — input, output e reasoning
- **Estado:** 111 linhas · fase: AUSENTE (gap — provavelmente Iniciado) · status: evergreen
- **Núcleo:** Frontmatter+fase ✗ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✗
- **Opcionais presentes:** Mermaid (graph TD ciclo de gasto em agentes), tabela comparativa (4 métricas de eficiência: CHR/SNR/TTA/Reasoning Overhead), código JSON (anatomy de chamada real), casos práticos (cenário 94% cache hit + custo dominado por reasoning)
- **Score verificar-nota (estimado):** 5/12 — falham E1 (TL;DR com apenas 1 linha; precisa ≥3), E5 (sem ponte narrativa para nota 03; "Veja também" não conta), E6 (sem seção inglês), E7 (sem tabela PT↔EN), E8 (4 armadilhas como lista numerada, sem callouts `[!warning]` individuais), P1 (sem código-com-falha), L2 (sem fontes externas com URL)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar `fase: Iniciado` ao frontmatter — fecha o gap de fase (núcleo crítico)
  - Expandir TL;DR para ≥3 linhas densas (atual: 1 linha longa) — ativa E1; sugestão: separar em 3 linhas — (1) as três faturas distintas, (2) o mecanismo de preço diferenciado, (3) a implicação prática de onde está a maior alavanca
  - Adicionar seção/parágrafo narrativo "O que vem a seguir" antes de "## Veja também" apontando para `[[03 - Por que agentes gastam tanto]]` com motivação (ex: agora que você sabe que input, output e reasoning têm perfis de custo distintos, o próximo passo é ver como esses três vetores se amplificam em loops de agente — onde cada iteração adiciona os três ao mesmo tempo) — ativa E5
  - Converter "## Armadilhas Técnicas" (4 itens numerados) para callouts `[!warning]` individuais — ativa E8
  - Adicionar fonte externa com URL (ex: anthropic.com/pricing, artificialanalysis.ai ou openai.com/pricing) — ativa L2
  - Expandir o corpo da nota de 111 para ≥300 linhas (Iniciado): a nota cobre corretamente os mecanismos, mas está comprimida; adicionar seção inglês + PT↔EN (ativa E6/E7), expandir casos práticos com mais exemplos numéricos concretos (custo total de uma chamada com reasoning runaway), e adicionar pelo menos um exemplo de "código-com-falha" (ex: JSON sem `thinking_budget` resultando em custo 100× maior)
#### 03 - Por que agentes gastam tanto
- **Estado:** 120 linhas · fase: AUSENTE (gap — provavelmente Iniciado) · status: evergreen
- **Núcleo:** Frontmatter+fase ✗ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** tabela comparativa (turno × tokens acumulados), [!example] (single-shot vs agente vs agente otimizado), wikilinks cross-galho (Dicionário de IA; [[03 - Context rot e atenção diluída]])
- **Score verificar-nota (estimado):** 7/12 — falham E3 (sem Mermaid), E5 (sem ponte narrativa para 04 Monitoramento), E6/E7 (sem inglês + PT↔EN), E8 (sem [!warning]; armadilhas em prosa), P1 (sem código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar `fase: Iniciado` ao frontmatter — fecha gap de fase (núcleo crítico) e ativa verificação de piso (Iniciado ≥300 linhas)
  - Adicionar seção narrativa "O que vem a seguir" antes de "## Veja também" com ponte para nota 04 (Monitoramento) — fecha E5 (núcleo faltante)
  - Converter armadilhas dos 5 vetores (retries silenciosos, rabbit holes, tool verbosity) para ≥3 callouts `[!warning]` individuais — ativa E8
  - Adicionar diagrama Mermaid (ex: xychart ou sequenceDiagram da acumulação turno-a-turno) — ativa E3; com E5+E8 já fechados isso leva o score para 10/12
  - Expandir de 120 para ≥300 linhas (piso Iniciado): adicionar seção "Como explicar em inglês" + tabela PT↔EN com termos-chave (agentic loop, context window, tool definition, rabbit hole, retry) — ativa E6/E7 e eleva score para 12/12
#### 04 - Monitoramento — ccusage, Langfuse, dashboards
- **Estado:** 312 linhas · fase: AUSENTE (gap — galho usa `fase:`, nota deveria ter) · status: growing / progress: in_progress
- **Núcleo:** Frontmatter+fase ✗ (gap) · TL;DR ✓ · Abertura-problema ✗ (começa com definição "Monitoramento de tokens é...") · Corpo-mecanismo ✓ · O que vem a seguir ✗ (só "Veja também" com link — não conta) · Fontes ✓
- **Opcionais presentes:** tabelas comparativas (providers · ferramentas · métricas · alertas), 1× [!warning] (Helicone maintenance mode), [!tip] (PII em spans OTel), seção Armadilhas (7 itens — lista bullet, sem `[!warning]` individuais), código funcional (bash ccusage · Python Helicone · Python Langfuse · Python Phoenix · Python OTel · Python webhook · Python log_usage), wikilinks cross-galho (Dicionário de IA, notas 02/05/15)
- **Score verificar-nota (estimado):** 5/12 — aprovados: E1(TL;DR), E4(casos), P2(mecanismo), L1(cross-galho), L2(fontes com URL) · falham: E2(abertura-problema), E3(Mermaid), E5(O que vem a seguir), E6(inglês), E7(PT↔EN), E8(armadilhas ≥3 [!warning]), P1(código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar `fase: Iniciado` ao frontmatter — fecha gap de fase (núcleo crítico); nota tem 312 linhas, acima do piso Iniciado (≥300)
  - Adicionar seção narrativa "O que vem a seguir" (antes de "## Veja também") com ponte para [[05 - Prompt caching na prática]] — fecha E5 (núcleo faltante); ex: "Agora que você sabe o que monitorar e com quais ferramentas, o próximo passo é aprender a reduzir o que você mede — e prompt caching é a alavanca com maior ROI"
  - Adicionar parágrafo de abertura com cenário/problema real antes de "## O que é" — fecha E2; ex: "Você otimizou os prompts, adicionou caching, cortou tool definitions — mas sua fatura do mês ainda explodiu. Sem dados por sessão e por tarefa, você está voando às cegas"
  - Converter a seção "## Armadilhas" (7 itens em lista bullet) para callouts `[!warning]` individuais — fecha E8; priorizar: "Monitorar só o total", "Helicone em novos projetos" (já tem [!warning] inline), "Prompts com PII em spans OTel"
  - Adicionar pelo menos 1 diagrama Mermaid — fecha E3; sugestão: `xychart-beta` mostrando custo por camada (provider · sessão · trace) ou `sequenceDiagram` do ciclo ccusage→dashboard→alerta; com E2+E5+E8+E3 fechados o score sobe para 9/12 (gate)
  - Adicionar seção "Como explicar em inglês" + tabela PT↔EN — fecha E6/E7 (ex: observability · trace · span · generation · cache hit rate · anomaly detection · cost creep · billing window); eleva score para 11/12
  - Atenção: datas de validade — ccusage 18.0.11 (abril 2026), Helicone maintenance mode (2026), convenções OTel GenAI em status `experimental`; adicionar `[!info]` de caducidade nas seções com versões específicas
#### 05 - Prompt caching na prática
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid, tabelas comparativas, casos práticos (4), armadilhas (4× [!warning]), código-com-falha (Caso 4 — timestamp invalida cache), inglês + tabela PT↔EN (12 termos), checklist de implementação, Estado da arte, [!tip] com URL externa, Veja também
- **Score verificar-nota (estimado):** 12/12
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 06 - Context pruning — o que remover do prompt
- **Estado:** 403 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid, tabela comparativa (taxonomia de poluição + impacto por técnica), 6× [!warning] individuais (paradoxo da segurança, podar demais, sumarização que apaga decisões, falta de teste de impacto, CLAUDE.md como diário, lock files no retrieval), casos práticos (4: review de PR, debugging 60+ turns, monorepo .cursorignore, CLAUDE.md 420→80 linhas), código-com-falha (exemplos "# Ruim:" em 4 blocos de código), inglês + tabela PT↔EN (14 termos), [!tip] com 2 mídias externas (YouTube + SE Daily), Estado da arte (junho 2026), checklist, Veja também
- **Score verificar-nota (estimado):** 11/12 — falha L1 (wikilinks em "Veja também" são todos dentro do mesmo galho; nenhum cross-galho explícito)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar 1 wikilink cross-galho no corpo da nota — ex: ao mencionar "lost in the middle" (linha ~33) linkar para [[06 - A janela de contexto]] (galho Anatomia dos LLMs), ou ao tratar semantic chunking/retrieval selectivo linkar para o galho RAG e Vector Databases — ativa L1 e eleva score para 12/12
#### 07 - Compressão de tool definitions
- **Estado:** 399 linhas (piso Adepto ≥400: NÃO — falta 1 linha) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (pie chart distribuição de tokens), 4 casos práticos, 6× [!warning] individuais, código-com-falha (blocos ❌/✅ em 4 seções), inglês + tabela PT↔EN (10 termos), checklist (13 itens), Estado da arte (junho 2026), tabela comparativa (impacto acumulado das técnicas; lazy loading por fase), [!tip] com mídia externa (YouTube)
- **Score verificar-nota (estimado):** 11/12 — falha L1 (todos os wikilinks em "Veja também" são dentro do mesmo galho Economia de Tokens; nenhum cross-galho)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar ≥1 wikilink cross-galho no corpo da nota — ex: ao mencionar MCP na seção "Estado da arte" linkar para o galho MCP, ou ao tratar lazy loading por tipo de agente linkar para [[Anatomia de Agents]], ou ao mencionar structured outputs como alternativa a tools linkar para [[Structured Outputs]] — ativa L1 e eleva score para 12/12; qualquer adição de conteúdo encaminha a nota para ≥400 linhas, fechando o piso Adepto
#### 08 - Compactação de histórico em agentes
- **Estado:** 384 linhas (piso Adepto ≥400: não) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (1×), código funcional (5 blocos Python/bash), tabelas comparativas (3×), casos práticos (4×), armadilhas (4× [!warning]), inglês + tabela PT↔EN (10 termos), [!tip] com vídeo MemGPT, Veja também, Checklist, seção Estado da arte
- **Score verificar-nota (estimado):** 11/12 — falha P1 (código-com-falha; todos os blocos de código são funcionais — inaplicável para nota de estratégia)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir a seção "## Estado da arte" ou "## Casos práticos" com ~20 linhas de conteúdo substantivo (ex: detalhar o padrão LangMem ou expandir o Caso 4 com métricas concretas do time) — fecha o único problema real: piso Adepto (384 < 400)
#### 09 - Model routing — modelo certo para a tarefa
- **Estado:** 405 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (1× flowchart routing), tabela comparativa (pirâmide de tiers × casos + economia por distribuição), casos práticos (4 casos reais com métricas), 4× [!warning] (routing errado → retry; monitorar qualidade; latência do classifier; cascading com prompts rígidos), código funcional (3 implementações: classifier LLM + cascading + regras determinísticas + routing por fase), inglês + tabela PT↔EN (10 termos), checklist, Estado da arte (junho 2026), wikilinks cross-galho ([[08 - Compactação de histórico em agentes]])
- **Score verificar-nota (estimado):** 11/12 — falha P1 (todos os blocos de código são funcionais; inaplicável para nota de estratégia de infraestrutura)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 10 - Sub-agentes especializados
- **Estado:** 276 linhas (piso Adepto ≥400: NÃO passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (sequenceDiagram), tabelas comparativas (múltiplas), casos práticos (4), armadilhas 4× [!warning], código funcional Python async, inglês + tabela PT↔EN (10 termos), [!tip] mídia (vídeo), Veja também, Checklist
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir a nota de 276 → ≥400 linhas para atingir o piso Adepto — aprofundar "Estado da arte" (junho 2026) e enriquecer casos práticos com mais contexto e números concretos
  - Adicionar parágrafo de abertura com cenário/problema concreto antes da tabela "Sub-agente vs model routing" (ex: engenheiro cujo agente de análise de codebase explodiu o contexto a $18 por run antes de descobrir sub-agentes) — fecha E2
  - Adicionar URLs clicáveis nas Fontes (ex: `https://docs.anthropic.com/en/docs/agents-and-tools/tool-use`, arxiv para Wu et al., `https://blog.langchain.dev/`) — fecha L2
#### 11 - Semantic caching
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart pipeline), tabelas comparativas (prompt vs semantic caching; embedding models; vector DBs; TTL; casos de uso; métricas; PT↔EN), 4× [!warning] (threshold baixo; TTL longo; sem medição de false positives; embedding diferente dev/prod), casos práticos (4 casos detalhados com números), inglês + tabela PT↔EN (10 termos), código funcional (3 implementações: Redis, GPTCache, Qdrant), checklist, estado da arte, [!tip] com mídia, Veja também, wikilinks cross-galho
- **Score verificar-nota (estimado):** 11/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar exemplo de código-com-falha (ex: lookup Redis com índice não criado retornando erro, ou threshold 0.85 servindo "cancelar assinatura" como hit para "suspender assinatura") — fecha P1 e eleva score para 12/12
#### 12 - Batch API — economia em volume
- **Estado:** 467 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (sequenceDiagram), tabela comparativa (Quando usar vs não usar + Pricing por provider), casos práticos (4 casos), armadilhas (6× [!warning] individuais), código funcional Python (Anthropic + OpenAI) + YAML CI/CD, inglês + tabela PT↔EN (10 termos), checklist, [!tip] mídia, Veja também
- **Score verificar-nota (estimado):** 10/12 — falham P1 (sem código-com-falha; apenas código funcional), L2 (fontes citam domínios como texto corrido, sem markdown hyperlinks clicáveis)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs clicáveis às fontes (ex: `[Message Batches API](https://docs.anthropic.com/en/api/creating-message-batches)`) — ativa L2 e eleva score para 11/12
  - Adicionar exemplo de código-com-falha (ex: batch com `custom_id` duplicado causando colisão de resultados, ou `max_tokens` omitido gerando erro 400 na Anthropic) — ativa P1 e eleva score para 12/12
#### 13 - Respostas concisas — controlar output tokens
- **Estado:** 376 linhas (piso Adepto ≥400: NÃO) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (1×), tabelas comparativas (preços por provedor, impacto financeiro, quando NÃO pedir concisão), casos práticos (4×), armadilhas (4× `[!warning]` individuais), inglês + tabela PT↔EN (10 termos), checklist, código funcional (6 blocos com ❌/✅), Veja também, [!tip] com URL YouTube
- **Score verificar-nota (estimado):** 11/12 — falha P1 (❌/✅ é antipattern, não erro de runtime); L2 parcial (URL genérica no [!tip]; fontes sem hiperlinks clicáveis)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir nota para ≥400 linhas para atingir piso Adepto — adicionar profundidade em "Estado da arte" (ex: structured outputs forçados via parâmetro de API, impacto do instruction following melhorado em 2026) ou ampliar "Casos práticos" com mais 1 cenário; sem padding
  - Adicionar exemplo de código-com-falha explícito (ex: `max_tokens=300` truncando resposta sem monitorar `stop_reason`, causando resultado incompleto silencioso em produção) — ativa P1 e eleva score para 12/12
  - Substituir URL genérica `https://youtube.com/anthropic` no `[!tip]` por URL de vídeo ou post real (ex: Anthropic Prompt Engineering Guide com link direto) — consolida L2 com fonte verificável
#### 14 - Thinking budget — controlar reasoning tokens
- **Estado:** 427 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (1×), tabelas comparativas (ROI por domínio + alternativas ao thinking), código funcional Python (calibração por task type + monitoramento + análise de saturação), 4× `[!warning]`, casos práticos (4), inglês + PT↔EN (10 termos), checklist (11 itens), seção thinking assimétrico multi-agente
- **Score verificar-nota (estimado):** 10/12 — falham P1 (código funcional mas sem exemplo de código-com-falha explícito) e L1 (wikilinks em "Veja também" todos dentro do mesmo galho Economia de Tokens)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar ao menos 1 wikilink cross-galho no corpo da nota (ex: ao mencionar "modelos de raciocínio" na seção "Estado da arte", linkar para `[[15 - Reasoning models e chain-of-thought]]` do galho Anatomia dos LLMs, ou para `[[Dicionário de IA]]`) — ativa L1 e eleva score para 11/12
  - Substituir URL genérica `https://youtube.com/anthropic` no `[!tip]` por URL de vídeo ou post real verificável (ex: Simon Willison simonwillison.net/2025/... ou Anthropic docs direto) — consolida L2 com fonte confiável
  - Opcional: adicionar exemplo de código-com-falha (ex: thinking ativado para task de classificação simples, exibindo custo $1.50 por chamada trivial sem ganho de qualidade — código que mostra o anti-pattern antes de mostrar a correção) — ativa P1 e eleva score para 12/12
#### 15 - Orçamento e hard limits
- **Estado:** 399 linhas (piso Adepto ≥400: não — 1 linha abaixo) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart 2 camadas), tabelas comparativas (budget por perfil, providers, kill switches), casos práticos (4 casos reais), armadilhas (4× [!warning] individuais), código-com-falha (anti-pattern sem max_tokens + correção), inglês + tabela PT↔EN (10 termos), checklist, [!tip] com mídia, Veja também
- **Score verificar-nota (estimado):** 11/12 — falha L1 (sem wikilink cross-galho; "Veja também" aponta apenas para notas do mesmo galho)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar 1 wikilink cross-galho no "Veja também" ou inline no corpo (ex: ao mencionar agentes em loop na seção Kill switches, linkar `[[Anatomia de Agents]]`; ou acrescentar `[[Dicionário de IA]]` ao "Veja também") — ativa L1, eleva score para 12/12 e empurra a nota acima de 400 linhas se adicionado como item no "Veja também"
#### 16 - Auditoria de consumo
- **Estado:** 398 linhas (piso Adepto ≥400: não — faltam 2 linhas) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart), tabelas comparativas (auditoria vs monitoramento · ferramentas · cadência), 4× [!warning] individuais, casos práticos (4 casos nomeados), código funcional (Python atribuição + Langfuse audit script), inglês + tabela PT↔EN (10 termos), checklist, relatório de auditoria template, seção "Estado da arte"
- **Score verificar-nota (estimado):** 10/12 — falham P1 (sem código-com-falha; só código funcional) e L1 (sem wikilink cross-galho; todos os links apontam para notas do próprio galho Economia de Tokens)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar 1 wikilink cross-galho no corpo ou em "Veja também" (ex: ao descrever agentes em loop na seção de retries, linkar `[[Anatomia de Agents]]`; ou acrescentar `[[Dicionário de IA]]` no "Veja também") — ativa L1, eleva score para 11/12, e provavelmente ultrapassa o piso de 400 linhas com custo mínimo de edição
#### 17 - ROI de IA — quando o agente vale o custo
- **Estado:** 397 linhas (piso Adepto ≥400: não — 3 linhas abaixo) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid · tabelas comparativas (hora×tokens, métricas de valor, vanity metrics, ROI por tipo de task, alternativas de budget, cadência, plano vs API) · 4 casos práticos ([!example] + 4 seção Casos) · 4× [!warning] individuais · código Python funcional (calculate_roi + ROITracker) · inglês + tabela PT↔EN · [!tip] com mídia · checklist · Veja também
- **Score verificar-nota (estimado):** 10/12 — falham P1 (código funcional, sem código-com-falha — inaplicável para nota econômica) e L2 (seção Fontes tem 4 referências bibliográficas sem URLs diretas; [!tip] traz search URL do YouTube, não fonte real)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs diretas às 4 referências da seção "## Fontes" (GitHub Research Copilot study, METR 2025, Stack Overflow Survey 2026, MIT Sloan Kalliamvakou 2025) — ativa L2, eleva score para 11/12 e supre as 3 linhas que faltam para o piso Adepto de 400
#### 18 - Playbook de economia — checklist completo
- **Estado:** 353 linhas (piso Adepto ≥400: não passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗ (4 referências sem URLs clicáveis; [!tip] tem link YouTube de busca genérica, não fonte real)
- **Opcionais presentes:** Mermaid (flowchart 5 fases), código Python funcional (diagnose_optimization_priority), tabelas comparativas (quick reference sintoma→técnica + impacto acumulado estimado), 4× [!warning] individuais, inglês + tabela PT↔EN (10 termos), 4 casos práticos, [!tip] com mídia, Veja também
- **Score verificar-nota (estimado):** 9/12 — falham P1 (código funcional presente, sem código-com-falha), L1 (wikilinks apenas dentro do próprio galho, sem cross-galho), L2 (Fontes sem URLs clicáveis reais)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs clicáveis às 4 referências da seção "## Fontes" (docs.anthropic.com, helicone.ai/docs, simonwillison.net, leanpub.com) — ativa L2, eleva score para 10/12 e contribui para o piso de 400 linhas
  - Adicionar ≥1 wikilink cross-galho (ex: `[[Dicionário de IA]]`, `[[Anatomia de Agents]]` ou nota de outro galho que se beneficie de referenciar o playbook) — ativa L1 e eleva score para 11/12
  - Nota tem 353 linhas, 47 abaixo do piso Adepto de 400 — as duas mudanças acima somadas devem aproximar ou cruzar o piso; se não, expandir "Estado da arte" ou aprofundar um caso prático
#### 19 - Planos e tiers — Max, Pro, API, Enterprise
- **Estado:** 372 linhas (piso Adepto ≥400: não passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗ (domínios mencionados, sem hiperlinks clicáveis)
- **Opcionais presentes:** Mermaid (1 flowchart TD), tabelas comparativas (7+), casos práticos (4), armadilhas ([!warning] × 4), código funcional Python (calculate_breakeven + litellm), inglês + tabela PT↔EN (10 termos), [!tip] (mídia YouTube), Veja também, checklist de decisão
- **Score verificar-nota (estimado):** 10/12 — falham P1 (código-com-falha; inaplicável para nota conceitual/cálculo) e L2 (fontes sem URLs clicáveis como markdown links)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar hiperlinks clicáveis às 4 referências da seção "## Fontes" (anthropic.com/pricing, openai.com/pricing, ai.google.dev/pricing, docs.litellm.ai) — ativa L2, eleva score para 11/12
  - Nota tem 372 linhas, 28 abaixo do piso Adepto de 400 — expandir a seção "Estado da arte — junho 2026" (deflação de planos, multi-modal, Enterprise para times menores) ou aprofundar um caso prático com cálculo numérico; ambas as mudanças somadas devem cruzar o piso
  - Tabelas de preços (Pro $20, Max $100/$200, OpenAI Pro $200, Gemini Advanced $20) têm ALTA data de validade (válidas em junho 2026) — adicionar `[!warning]` ou `[!info]` de caducidade antes de cada bloco de tabela por provider avisando que preços e planos mudam e o leitor deve verificar no site oficial antes de decidir
#### 20 - O futuro — tokens cada vez mais baratos
- **Estado:** 288 linhas (piso Adepto ≥400: não passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ (vai direto à comparação histórica, sem cenário/problema do leitor) · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓ (YouTube URL presente; domínios citados nas referências sem hiperlinks clicáveis)
- **Opcionais presentes:** 2× Mermaid (xychart-beta deflação + flowchart paradoxo do volume), tabelas comparativas (preços por período/provider + o que muda vs não muda + implicações por técnica), 4× armadilhas [!warning] individuais, casos práticos (4: early adopter vs late, routing 2024→2026, self-hosted vs API, edge inference pré-triagem), inglês + tabela PT↔EN (10 termos), [!tip] mídia YouTube, checklist de ação
- **Score verificar-nota (estimado):** 10/12 — falham E2 (abertura sem cenário/problema real) e P1 (sem código-com-falha — inaplicável para nota de tendências)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## A queda de preço mais rápida na história da tecnologia" (ex: "Você está planejando o orçamento de IA para o próximo semestre e recebe uma tabela com projeções de preço que parecem impossíveis — será que tokens realmente continuam caindo assim?") — ativa E2 e eleva score para 11/12
  - Nota tem 288 linhas, 112 abaixo do piso Adepto de 400 — adicionar parágrafo de abertura + callout de caducidade + expandir "Estado da arte" ou aprofundar um caso prático (números reais de custo de operação de agente em 2027 projetado) deve aproximar ou cruzar o piso
  - Nota tem ALTA densidade de dados com data de validade (tabela de preços $/MTok por período, projeções 2027-2028, seção "Estado da arte — junho 2026", afirmações sobre GPT-5/Claude 5): adicionar `[!warning]` ou `[!info]` de caducidade antes da tabela de preços e antes da seção "Estado da arte" avisando que preços e versões de modelos mudam mensalmente e o leitor deve verificar em Artificial Analysis
  - Adicionar URLs clicáveis às 4 referências da seção "## Fontes" (artificialanalysis.ai, ben-evans.com, github.com/vipulnaik, semianalysis.com) — consolida L2 como hiperlink real (atualmente só domínio em prosa)
#### 21 - Hacks de trincheira — Claude, Gemini e Copilot em 2026
- **Estado:** 409 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (1×), casos práticos (4 casos com números medidos), armadilhas (4× [!warning] individuais), inglês + tabela PT↔EN (10 termos), tabela comparativa (decisão por tipo de task), checklist, [!tip] com mídia (YouTube search), código funcional (bash, JSON, Python)
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar ≥1 wikilink cross-galho (ex: para [[Anatomia de Agents]] ou [[Agentes de Codificação]]) — ativa L1 e eleva score para 10/12; os 4 wikilinks de "Veja também" são todos intra-galho
  - Adicionar URLs Markdown clicáveis às 4 fontes da seção "## Fontes" — substituir domain+path em prosa por `[texto](https://url-real)` real — ativa L2 e eleva score para 11/12
  - Sinalizar dados com data de validade: "Tabela de decisão (junho 2026)" cita modelos (Claude Opus 4, Gemini 2.5 Pro, Claude Sonnet 4.6), preços ($0.10/MTok Flash-Lite, $2.50/MTok Gemini Pro) e seção "Estado da arte — junho 2026" — adicionar `[!warning]` ou `[!info]` de caducidade antes da tabela e antes de "Estado da arte" avisando que preços, versões e features mudam rapidamente; o modelo de AI Credits Copilot ("desde junho de 2026") também tem validade
#### 22 - Caso real — Auditoria de 47M tokens em maio 2026
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart 5 vetores), tabela de perfil de referência, 4 casos práticos rotulados, 4× [!warning], inglês + tabela PT↔EN (10 termos), [!tip] com link YouTube, checklist de auditoria mensal, tabela de plano por ROI, tabela de resultados esperados, código bash (diagnóstico e fixes), Python script de diagnóstico de saída pesada
- **Score verificar-nota (estimado):** 10/12 — falham L1 (sem wikilink cross-galho; "Veja também" aponta só para notas do mesmo galho), P1 (sem código-com-falha — inaplicável para nota de caso real)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar ≥1 wikilink cross-galho na seção "O que vem a seguir" ou "Veja também" (ex: [[Anatomia de Agents]], [[Context Engineering]], [[Agentes de Codificação]] ou outro galho de IA que aplica diretamente as técnicas descritas aqui) — ativa L1 e eleva score para 11/12

---

## 5. Context Engineering

> Galho **usa `fase:` Adepto** em todas. Régua aplica `fase:` + piso ≥400 (T2).

### Notas

#### 01 - De prompt engineering a context engineering
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗ (referências sem URLs clicáveis)
- **Opcionais presentes:** Mermaid (graph LR evolução), tabelas comparativas (4×), casos práticos (5 casos), armadilhas (5× `[!warning]`), inglês + tabela PT↔EN (21 termos), wikilinks cross-galho (`[[Agentes de Codificação]]` + wikilinks internos ao galho), checklist de primeiros passos, seção fine-tuning vs CE, seção métricas de qualidade de contexto
- **Score verificar-nota (estimado):** 10/12 — falham P1 (sem código-com-falha — inaplicável para nota conceitual) e L2 (referências sem URLs)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs reais às referências (tweet Karpathy, memo Lutke/Shopify, doc Anthropic "Building effective agents", Bytebytego guide, paper "Lost in the Middle" arxiv) — ativa L2 e eleva score para 11/12
#### 02 - Os quatro pilares — prompt, context, intent, specification
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid (pirâmide hierárquica + ciclo de maturidade), tabelas comparativas (4 pilares × 5 critérios + ações sobre contexto + quando cada pilar basta), 4 casos práticos, 4× `[!warning]` individuais, inglês + tabela PT↔EN (13 termos), checklist de maturidade por pilar, `[!info]` pedagógico
- **Score verificar-nota (estimado):** 10/12 — falham P1 (sem código-com-falha — inaplicável para nota conceitual pura) e L2 (Referências listam fontes sem URLs clicáveis)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs reais às referências (post Karpathy "Software Is Changing (Again)", Anthropic "Building effective agents", Braintrust "Evals-driven development", NIST AI RMF, EU AI Act, Hamel Husain "Your AI Product Needs Evals") — ativa L2 e eleva score para 11/12
#### 03 - Context rot e atenção diluída
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (graph LR curva U + tabela de atenção + timeline de incidente), tabelas comparativas (rot vs overflow; contextos de risco; sintomas; mitigações; custo; medição; checklist), casos práticos (4: agente de refatoração, RAG e-commerce, pair programming, multi-agent), 4× [!warning] individuais, inglês + tabela PT↔EN (14 termos), [!quote], [!example], [!info], [!tip] (mídia embutida), wikilinks cross-galho (Economia de Tokens, Context Engineering), fontes com URLs (arxiv × 5 + externos × 3)
- **Score verificar-nota (estimado):** 11/12 — falha apenas P1 (sem código-com-falha; inaplicável para nota conceitual)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 04 - Context pipelines — montagem dinâmica
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (pipeline graph), tabelas comparativas (5 fontes; spectrum retrieval; 4 operações; engines comerciais), casos práticos (4: code review, chatbot telecom, análise financeira, multi-agent), armadilhas (6× [!warning]), inglês + tabela PT↔EN (14 termos), código funcional Python (build_context), [!example] (Claude Code híbrido), [!tip] (métrica pipeline health + vídeo AI Engineer), Veja também
- **Score verificar-nota (estimado):** 11/12 — falha só P1 (código-com-falha ausente; o Python presente é exemplo funcional, não anti-pattern com falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 05 - Camadas de contexto — persistente, temporal, transiente
- **Estado:** 402 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (graph TB 4 camadas), tabelas comparativas (implementações por sistema; tabela de decisão; métricas de saúde por camada), casos práticos (4: RH, análise financeira, e-commerce, code review), 5× armadilhas [!warning] individuais, inglês + tabela PT↔EN (13 termos), código Python funcional (ContextManager 4 camadas), [!tip] com mídia (vídeo YouTube com URL), [!question]- pedagógico, Veja também
- **Score verificar-nota (estimado):** 11/12 — falha só P1 (código-com-falha ausente; a nota justifica explicitamente a ausência — o anti-padrão é não ter ContextManager algum)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 06 - Dynamic retrieval beyond RAG
- **Estado:** 385 linhas (piso Adepto ≥400: não passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid, 4 casos práticos, inglês, tabela PT↔EN, 5 [!warning], código ingênuo vs. JIT, [!tip] mídia, Veja também, L1 wikilink cross-galho ([[RAG e Vector Databases]])
- **Score verificar-nota (estimado):** 12/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Nota tem 385 linhas — 15 abaixo do piso Adepto (≥400). Expandir qualquer seção existente (ex.: "Estado da arte" ou "Métricas") com ~15 linhas de substância para cruzar o limite formal.
#### 07 - Compressão e pruning de informação
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (sliding window), tabelas comparativas (3+), 4 casos práticos, 5× [!warning] individuais, código Python (compact_history), inglês + tabela PT↔EN (14 termos), [!tip] mídia (Bojie Li), [!quote] (Anthropic), [!info] (analogia plantão), métricas de eficácia, estado da arte 2026, Veja também, wikilinks cross-galho (notas 03/04/05/08/10/13), múltiplas fontes com URL
- **Score verificar-nota (estimado):** 11/12 — falha apenas P1 (sem código-com-falha intencional — inaplicável para nota conceitual)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 08 - Memória agentica — self-editing memory
- **Estado:** 413 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid (flowchart self-editing + sequenceDiagram sessão completa), tabela comparativa (players jun/2026 + riscos específicos + métricas de saúde), 4 casos práticos (coding assistant + suporte técnico + research agent + memory poisoning controlado), 5× [!warning] individuais (governança + auto-salvar sem critério + TTL + buffer de sessão + deduplicação), código Python funcional (Letta memory blocks + implementação mínima sem framework), inglês + tabela PT↔EN (13 termos), [!tip] mídia (busca YouTube Letta talk), [!quote] (MemGPT paper Packer et al.), estado da arte jun/2026, Veja também, referências (6 fontes — github/arxiv/vendors)
- **Score verificar-nota (estimado):** 10/12 — falham P1 (sem código-com-falha — inaplicável para nota conceitual) e L1 (sem wikilink cross-galho para o galho Memória de Agentes)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - Opcional: adicionar wikilink cross-galho para uma nota do galho [[Memória de Agentes]] na seção "Veja também" ou no corpo — ativa L1 e eleva score para 11/12
#### 09 - Shared memory em multi-agent
- **Estado:** 389 linhas (piso Adepto ≥400: não passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (graph TB com 3 padrões), 4 casos práticos (pipeline conteúdo + code review paralelo + suporte triagem + research financeiro), 4 [!warning] individuais (histórico bruto + estado concorrente + sem audit trail + acoplamento implícito), código Python funcional (Swarm handoff + LangGraph TypedDict + handoff payload + pubsub), inglês + tabela PT↔EN (12 termos), [!tip] mídia (YouTube LangGraph), comparativo de frameworks (tabela 6 frameworks jun/2026), estado da arte jun/2026, métricas de saúde (tabela 5 métricas), Veja também, referências (6 fontes)
- **Score verificar-nota (estimado):** 10/12 — falham P1 (sem código-com-falha pedagógico — inaplicável para nota conceitual) e L1 (todos os wikilinks são intra-galho CE; sem wikilink cross-galho)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Piso: nota tem 389 linhas, 11 abaixo do piso Adepto (≥400) — acrescentar ~15 linhas de conteúdo substantivo (ex.: expandir "Estado da arte" ou adicionar sub-item em "Quando NÃO usar")
  - L1: adicionar ao menos 1 wikilink cross-galho no corpo ou em "Veja também" — candidatos: [[Concorrência]] (race conditions), [[Anatomia dos LLMs]] (janela de contexto), ou qualquer nota de domínio fora de Context Engineering
#### 10 - Structured state tracking
- **Estado:** 406 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart de operação), tabela comparativa (Markdown × JSON × DB), casos práticos (4 casos), 4× [!warning] individuais, inglês + tabela PT↔EN (12 termos), [!tip] com fonte externa, Veja também
- **Score verificar-nota (estimado):** 10/12 — falham P1 (código-com-falha — inaplicável para nota conceitual) e L1 (sem wikilink cross-galho; todos os links apontam para notas do próprio galho CE)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 11 - Skills e instructions como contexto
- **Estado:** 361 linhas (piso Adepto ≥400: não passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Inglês + tabela PT↔EN (11 termos), 4× [!warning] (armadilhas), 4 casos práticos, tabelas comparativas (skills vs instructions + métricas de eficácia), código funcional (AGENTS.md template + Spark skill + monorepo hierarquia + security requirements), [!info], [!tip] com URL externa (augmentcode.com/blog), Veja também
- **Score verificar-nota (estimado):** 10/12 — falham E3 (diagramas são ASCII em code blocks, não Mermaid) e P1 (sem código-com-falha — todos os exemplos são funcionais)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Nota tem 361 linhas, abaixo do piso Adepto (≥400): expandir com 1-2 casos práticos adicionais ou converter os diagramas ASCII (separação de camadas, cross-tool 80/20, hierarquia global→projeto→diretório) para diagramas ```mermaid reais — ativa E3, eleva score para 11/12 e encosta no piso
  - Adicionar 1 exemplo de código-com-falha concreto (ex: AGENTS.md com regras contraditórias — "Use named exports" em `AGENTS.md` vs "Use default exports" em `CLAUDE.md` — e o comportamento não-determinístico resultante) — ativa P1 e eleva score para 12/12
#### 12 - Guardrails determinísticos
- **Estado:** 347 linhas (piso Adepto ≥400: não passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (1× control plane), casos práticos (4×: suporte e-commerce, coding agent, fintech Lean 4, geração conteúdo), inglês + tabela PT↔EN (12 termos), 4× [!warning] (armadilhas individuais), tabelas comparativas (pre/post-LLM guardrails, three-tier control, frameworks, métricas), código funcional Python (three-tier + allowlist), [!tip] (frameworks + mídia busca YouTube), [!info] (Lean 4 estado da arte), [!quote] (Salesforce + CIO Magazine), Veja também
- **Score verificar-nota (estimado):** 9/12 — falham P1 (código-com-falha ausente; exemplos são funcionais), L1 (sem wikilink para galho Segurança e Guardrails), L2 (referências sem URLs clicáveis; arxiv com IDs mas sem links; [!tip] tem link de busca YouTube, não fonte direta)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Nota tem 347 linhas, abaixo do piso Adepto (≥400): expandir seção "Estado da arte" ou "Métricas de eficácia" com mais contexto ou converter o único Mermaid em 2-3 diagramas (ex: sequenceDiagram de ataque por prompt injection bloqueado pelo pre-LLM + flowchart do three-tier) — encosta no piso e ativa E3 adicional
  - Adicionar URLs às referências: CIO Magazine (cio.com), Arthur AI (arthur.ai/blog), arxiv como links `https://arxiv.org/abs/2604.01483` — ativa L2 e eleva score para 10/12
  - Adicionar wikilink cross-galho para o galho Segurança e Guardrails (ex: `[[Segurança e Guardrails/index]]` ou nota relevante) em "Veja também" — ativa L1 e eleva score para 11/12
#### 13 - Entropia e qualidade de contexto
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart ciclo de melhoria), tabelas comparativas (alta/baixa entropia + métricas + "sala bagunçada" + PT↔EN), 4× [!warning] individuais, casos práticos (4 casos: chatbot suporte, RAG doc extensa, agent financeiro, test gold CI/CD), inglês + tabela PT↔EN (12 termos), código funcional Python (noise_floor_test + test_suite), YAML CI/CD gate, wikilinks cross-galho (notas 03/04/06/07/08), fonte externa com URL (FlowHunt), callout [!example], callout [!quote], Veja também
- **Score verificar-nota (estimado):** 11/12 — único item faltante: P1 (código-com-falha — inaplicável para nota conceitual sem cenário de código quebrado)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 14 - Context engineering na prática — setup completo
- **Estado:** 552 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart arquitetura), 4 casos práticos, 4× [!warning] (armadilhas individuais), inglês + tabela PT↔EN (12 termos), checklist [!example], tabela comparativa (métricas antes/depois + sinais de expansão), código funcional (Python pipeline, mem0, guardrails, JSON MCP), [!tip] com link externo, Veja também
- **Score verificar-nota (estimado):** 11/12 — único item faltante: P1 (código-com-falha — inaplicável para nota de setup sem cenário de quebra)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 15 - Técnicas de prompting — zero-shot, few-shot, CoT, ToT
- **Estado:** 435 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart heurística de escolha), tabela comparativa (técnicas × quando/custo/ganho), casos práticos (4), armadilhas (4× [!warning]), inglês + tabela PT↔EN (12 termos), código funcional (self-consistency Python + structured outputs Python + skill SKILL.md), [!tip] callouts pedagógicos
- **Score verificar-nota (estimado):** 10/12 — falham P1 (código presente mas sem exemplo de falha) e L1 (nenhum wikilink cross-galho: todos os links internos são dentro do próprio galho Context Engineering; não há link para o galho Prompt Engineering nem para outros galhos)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar wikilink para o galho Prompt Engineering (galho 12) na seção "Veja também" ou na abertura do TL;DR — ativa L1 e eleva score para 11/12. A nota cobre as técnicas base; o galho PE aprofunda técnicas avançadas; a ponte é natural e relevante para o leitor
  - Adicionar exemplo de código-com-falha na seção Few-shot — ex: 3 exemplos da mesma classe (3× "bug") seguidos da query, mostrando que o modelo classifica tudo como bug; depois versão corrigida com exemplos diversificados — ativa P1 e eleva score para 12/12
#### 16 - Agent skills marketplace e SKILL.md
- **Estado:** 474 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart decisão skill×AGENTS.md×hardcoded), 4× casos práticos (glosa Codex · security cross-project · onboarding · versioning+rollback), 4× `[!warning]` individuais (skill 10K+ tokens · third-party sem auditoria · description vaga · misturar com AGENTS.md), inglês + tabela PT↔EN (12 termos), tabelas comparativas (AGENTS.md×SKILL.md · SKILL.md×prompt template · ecossistema 2026 · métricas), wikilinks cross-galho (notas 11/14/15 · Agentes de Codificação · Anatomia dos LLMs), `[!tip]` com URL externa (docs.anthropic.com)
- **Score verificar-nota (estimado):** 11/12 — apenas P1 ausente (código-com-falha, inaplicável para nota conceitual)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma

---

## 6. Agentes de Codificação

> Galho **usa `fase:`** (01 SEM fase = gap; 02–18 = Adepto). Régua aplica `fase:` + piso ≥400 (Adepto). Muitas notas de ferramentas (Cursor/Claude Code/Copilot/etc.) — atenção a caducidade.

### Notas

#### 01 - De autocomplete a agentes autônomos
- **Estado:** 405 linhas · fase: AUSENTE (gap — galho usa `fase:`, nota 01 deveria ser Iniciado) · status: growing
- **Núcleo:** Frontmatter+fase ✗ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid (progressão de autonomia, mindmap competências, categorias de ferramentas), tabelas comparativas (estágios × exemplos; categorias × autonomia; tarefas × estrelas; histórico timeline), 5 cenários práticos, 7× [!warning], inglês + tabela PT↔EN (12 termos), wikilinks cross-galho (Dicionário de IA: tool use, Comprehension gate, background agent, etc.), 2× [!question]-, [!summary], [!info], mídia embutida ([!tip] vídeo Karpathy — Sequoia Capital)
- **Score verificar-nota (estimado):** 11/12 — falha P1 (sem código-com-falha — inaplicável para nota conceitual pura)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar `fase: Iniciado` ao frontmatter — único gap de núcleo; o conteúdo da nota é muito sólido e não precisa de mudanças estruturais
#### 02 - Vibe coding vs engenharia disciplinada
- **Estado:** 409 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid, tabelas comparativas (múltiplas), casos práticos (4 cenários), 7× [!warning], inglês + tabela PT↔EN (13 termos), [!question]-, [!tip], [!info], [!example], [!caution], [!summary], wikilinks cross-galho (Context Engineering + Anatomia de Agents), Veja também
- **Score verificar-nota (estimado):** 11/12 — P1 (código-com-falha) ausente; inaplicável para nota conceitual/postura
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 03 - O comprehension gate
- **Estado:** 409 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing / progress: done
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid, inglês + tabela PT↔EN (10 termos), 5× [!warning] individuais (seção Armadilhas), 4 casos práticos (cenários 1–4), tabelas comparativas (níveis de risco, red flags, métricas DORA), [!question]- pedagógicos (gate torna mais lento? atrofia program comprehension?), [!tip] (vídeo CodeHead + entrevista EN), [!info] callouts, [!summary], wikilinks cross-galho (Dicionário de IA), fontes externas com URL (StepTo, Metacto, IEEE-ISTAS arxiv, CACM, arXiv:2604/2511)
- **Score verificar-nota (estimado):** 10/12 — falham E5 (seção "O que vem a seguir" existe mas aponta para notas 14/16/18, não para nota 04 Cursor) e P1 (sem código-com-falha — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Reescrever parágrafo de abertura da seção "## O que vem a seguir" para nomear explicitamente [[04 - Cursor — AI-native IDE]] como próxima nota da sequência, com motivação narrativa (ex: "o gate é uma prática de revisão — mas certas ferramentas facilitam ou dificultam aplicá-lo; o Cursor foi construído ao redor do IDE como ponto central do loop humano-agente, e é a primeira ferramenta que coloca o gate dentro do fluxo de desenvolvimento"); manter as pontes para 14/16/18 como contexto adicional — ativa E5 e eleva score para 11/12
#### 04 - Cursor — AI-native IDE
- **Estado:** 410 linhas (piso Adepto ≥400: PASSA) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart Agent Mode loop), 6 cenários práticos, 7× [!warning] individuais, inglês + tabela PT↔EN (10 termos), tabelas comparativas (features/planos/modelos/atalhos), código funcional (.cursorrules + .cursorignore), [!tip] com mídia (vídeo Fireship + tip de entrevista), [!info] (2×), Veja também, wikilinks cross-galho (notas 02/03/05/06/07/11/14/15 + Dicionário de IA)
- **Score verificar-nota (estimado):** 11/12 — P1 (código-com-falha) ausente; inaplicável para nota de ferramenta/IDE
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
- **Aviso data de validade:** Nota tem alta densidade de fatos caducáveis — ARR US$500M, preços de planos (Hobby/Pro/Business em 2026), nomes de modelos (Claude Sonnet 4.5, Opus 4, GPT-4.1, Gemini 2.5 Pro), timeline histórica (Series B jan/2025). A nota foi atualizada em 2026-06-27; monitorar ao enriquecer se esses dados continuam válidos.
#### 05 - Claude Code — terminal-first agent
- **Estado:** 408 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (loop agentic + 2× tabela de modos/hooks), 5 casos práticos, 6× [!warning] individuais, inglês + tabela PT↔EN (10 termos), tabelas comparativas (modos/hooks/permissions/modelos/Cursor vs Claude Code), código funcional (CLAUDE.md + hooks.json + permissions bash + CI/CD + tmux + MCP + workflow), [!question]- pedagógicos (2×), [!tip] com mídia (vídeo Best Practices Anthropic + tip de entrevista), Veja também, wikilinks cross-galho (Dicionário de IA + notas 02/03/04/10/11/14/15/16)
- **Score verificar-nota (estimado):** 10/12 — falham E5 (seção "O que vem a seguir" existe mas aponta para notas 10/14/15/11, não para nota 06 — GitHub Copilot e Copilot Agents) · P1 (sem código-com-falha; inaplicável para nota de ferramenta)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo de abertura em "O que vem a seguir" apontando para [[06 - GitHub Copilot e Copilot Agents]] como próximo passo imediato do galho — a nota atual descreve o agente terminal da Anthropic; a seguinte entra no maior ecossistema de codificação IA do mercado (integração nativa no VS Code, JetBrains e GitHub Actions), com modelo de distribuição e casos de uso radicalmente diferentes; fechar E5 eleva score para 11/12
  - Aviso de data de validade: tabela "Custo e modelos" (preços US$/MTok de Haiku 4.5, Sonnet 4.6, Opus 4), seção "Por que importa" ("melhor reasoning do mercado em 2026"), e tabela Histórico (marco opusplan 2026) têm alta densidade de dados caducáveis — adicionar `[!info]` de caducidade ou monitorar ao enriquecer
#### 06 - GitHub Copilot e Copilot Agents
- **Estado:** 409 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (fluxo issue→PR), tabelas comparativas (Agent Mode vs Copilot Agents; tiers Free/Individual/Business/Enterprise; concorrentes; histórico; cenários de uso; privacidade por plano), casos práticos (4 casos detalhados), armadilhas (5× `[!warning]` individuais), inglês + tabela PT↔EN (10 termos), código funcional (FIM; copilot-instructions.md; Agent Mode loop), 2× `[!question]-` pedagógicos, `[!tip]` (mídia + frase de impacto), Veja também
- **Score verificar-nota (estimado):** 10/12 — falham E5 (seção "O que vem a seguir" existe mas não aponta para nota 07; só referencia 04/05/12/14/15) e P1 (sem código-com-falha — inaplicável para nota de ferramenta/comparativa)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar ponte narrativa em "O que vem a seguir" apontando para [[07 - Windsurf e Cascade]] como próxima ferramenta do galho — seção existe mas avança o leitor para notas fora de sequência (04, 05, 12, 14, 15); inserir parágrafo curto motivando por que Windsurf/Cascade é o passo seguinte natural (ex: agora que você conhece o assistente mais integrado ao GitHub, o próximo capítulo mostra uma abordagem diferente — um IDE AI-native construído sobre VS Code mas com agentes de longa duração via Cascade, sem depender do ecossistema Microsoft) — fecha E5 e eleva score para 11/12
  - Sinalizar data de validade: tabela "Tiers de funcionalidade" (preços $10/$19/$39/seat), seção "Por que importa" ("30 milhões de devs em 2026"), tabela "Quando usar Copilot" e Histórico (versões de modelos como Claude 3.5 Sonnet e Gemini 1.5 Pro) têm alta densidade de dados caducáveis — adicionar `[!info]` de caducidade ou nota de rodapé nas seções de pricing e multi-model
#### 07 - Windsurf e Cascade
- **Estado:** 403 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (Cascade loop flowchart), tabela comparativa (Windsurf vs Cursor × 9 critérios; preços; histórico; quando usar; privacidade), casos práticos (4 casos: refactoring incremental, OAuth2 multi-file, debug com tool calls visíveis, time com orçamento limitado), 5× [!warning] (armadilhas individuais), inglês + tabela PT↔EN (10 termos), 2× [!question]- pedagógico, [!tip] mídia embutida (Kevin Hou + frase de impacto), código funcional (.windsurfrules + log Cascade), Veja também
- **Score verificar-nota (estimado):** 9/12 — falham E5 (seção "O que vem a seguir" existe mas discute futuro do produto Windsurf sob a OpenAI, não é ponte narrativa para nota 08 Gemini CLI), L1 (sem wikilink cross-galho — todos os links apontam para notas do mesmo galho), P1 (sem código-com-falha — inaplicável para nota de ferramenta/conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E5 — Substituir ou complementar a seção "O que vem a seguir" com parágrafo de ponte narrativa para [[08 - Gemini CLI — o player Google]]: a seção atual discute o futuro do produto (cenários OpenAI), não conduz o leitor para a próxima nota. Adicionar parágrafo que motive a transição — ex: "o Windsurf partiu de um IDE-first e integrou agentes; a próxima ferramenta inverte a direção: o Gemini CLI nasce no terminal, sem IDE, e mostra como o Google entra no espaço de codificação assistida pela linha de comando — uma aposta diferente sobre onde o dev passa mais tempo" — fecha E5 e eleva score para 10/12
  - L1 — Sem wikilink cross-galho: adicionar ao menos 1 link para nota de domínio diferente — candidatos naturais: Dicionário de IA (se houver termo relevante como "agentic loop"), ou nota do galho Economia de Tokens (para o argumento de custo de créditos premium) — eleva score para 11/12
  - Data de validade parcialmente sinalizada: TL;DR e `[!warning]` de aquisição cobrem a incerteza pós-OpenAI (✓), mas a tabela "Modelo de preços" (linhas ~55–61, preços $15/$35/$30/seat) não tem aviso explícito de caducidade — adicionar `[!info]` antes da tabela sinalizando que preços e tiers podem ter mudado pós-aquisição e recomendando verificar em windsurf.com
#### 08 - Gemini CLI — o player Google
- **Estado:** 409 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (loop agentic), tabela comparativa (concorrentes + preços + quando usar), casos práticos (6 casos), armadilhas (7× [!warning]), inglês + tabela PT↔EN, mídia embutida ([!tip] YouTube), [!question]- pedagógico, Veja também, seção Privacidade e segurança
- **Score verificar-nota (estimado):** 10/12 — falham E5 (seção "O que vem a seguir" existe mas fala sobre futuro do produto, não faz ponte para nota 09 Aider) e P1 (sem código-com-falha; inaplicável para nota de ferramenta)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E5 — Converter o final da seção "O que vem a seguir" (atualmente focada em evolução do produto: Vertex AI, MCP, Gemini 3.x) para incluir parágrafo de bridge narrativa para [[09 - Aider — o pair programmer de terminal]]: ex: "Enquanto o Gemini CLI representa a aposta do Google — ecossistema GCP, contexto gigante, multimodal — existe uma alternativa que parte de premissas opostas: o Aider nasce da comunidade open-source, funciona com qualquer modelo (Sonnet, GPT-4, até locais), e foca em edição cirúrgica de código a partir de diff. A próxima nota explora esse caminho." — fecha E5 e eleva score para 11/12
  - Data de validade — tabela "Modelo de preços" (preços Gemini 2.5 Pro $1.25/$2.50, Flash $0.15/$0.30, Gemini 2.0 Flash $0.10) não tem aviso explícito de caducidade; adicionar `[!info]` antes da tabela sinalizando que preços mudam e recomendando verificar em ai.google.dev/pricing
#### 09 - Aider — o pair programmer de terminal
- **Estado:** 409 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (1×), 5 casos práticos, inglês + tabela PT↔EN (10 termos), 5× [!warning] individuais, código funcional bash/YAML (sem falha), tabela comparativa (concorrentes × 7 critérios + quando usar × 9 cenários), [!question]- (2×), [!tip] (mídia vídeo + frase de impacto), Veja também (4 wikilinks internos)
- **Score verificar-nota (estimado):** 10/12 — falham E5 (seção "O que vem a seguir" existe mas fala do futuro do Aider como produto, sem bridge narrativa para [[10 - OpenCode — o harness open source]]; "Veja também" não conta) e P1 (sem código-com-falha — inaplicável para nota de setup/workflow)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E5 (núcleo) — A seção "O que vem a seguir" cobre tendências do produto Aider (Architect Mode, MCP, CI/CD) mas não faz ponte para a próxima nota. Adicionar parágrafo final de bridge narrativa para [[10 - OpenCode — o harness open source]], ex: "O Aider representa o polo 'controle total' do espectro — um dev, um terminal, diffs aprovados um a um, sem lock-in de vendor. A próxima nota explora outro CLI open-source que parte de premissas parecidas mas empurra mais longe a autonomia: o OpenCode." — fecha E5 e eleva score para 11/12.
  - Data de validade — A armadilha "Sem suporte nativo a MCP (ainda)" (linha ~359) está explicitamente datada em 2026 e pode mudar; o callout já sinaliza isso com "(ainda)", mas é o item mais sujeito a caducar rapidamente. Verificar a cada revisão do galho se o Aider implementou MCP.
#### 10 - OpenCode — o harness open source
- **Estado:** 409 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (arquitetura harness), tabelas comparativas (quando usar × harness OSS; OpenCode/Cline/Claude Code/Cursor × 9 critérios), casos práticos (5: custo DeepSeek, SSH remoto, auditoria segurança, experimentação de modelos, Cline+MCP hub), armadilhas (5× `[!warning]` individuais), inglês + tabela PT↔EN (10 termos), `[!question]-` pedagógico (qualidade do harness), `[!tip]` mídia (vídeo Cline VS Code), código funcional (bash OpenCode install + JSON Cline settings + JSON Continue multi-model), Veja também
- **Score verificar-nota (estimado):** 10/12 — falham E5 (seção "O que vem a seguir" cobre tendências futuras do mercado, não faz ponte narrativa para nota 11) · P1 (sem código-com-falha — stretch para nota de ferramentas)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E5 (núcleo) — A seção "O que vem a seguir" (linhas 372-383) cobre tendências gerais (MCP, orchestration, memória persistente) mas encerra sem bridge para nota 11. Adicionar parágrafo de fechamento dentro da seção, ex: "Tudo isso converge para uma questão prática: dado o ecossistema de harnesses open-source mapeado aqui, como escolher qual ferramenta usar para qual tarefa? A próxima nota monta o guia de decisão: Comparativo — qual ferramenta para qual tarefa." — fecha E5 (núcleo faltante) e eleva score para 11/12.
  - ⚠️ Data de validade — múltiplos dados com vida curta: stars do Cline ("58k+"), versões no histórico (OpenCode Abr/2025, Roo Code Jan/2025), preço DeepSeek implícito. Adicionar `[!info]` de caducidade na seção "## Histórico" avisando que stars e versões mudam mensalmente.
#### 11 - Comparativo — qual ferramenta para qual tarefa
- **Estado:** 408 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (graph TD mapa de decisão), tabelas comparativas (mega-comparativo por capacidade, por perfil, por tarefa, por custo, matriz de decisão rápida), 6 cenários práticos (fintech/compliance, dev indie, DevOps CI/CD, refactoring legado, pesquisa de modelos, air-gapped), 7× `[!warning]` (benchmarks, ferramenta única, custo acumulado, troca constante, hype, onboarding, modo agêntico para chat), inglês + tabela PT↔EN (17 termos), `[!tip]` com frase de impacto para entrevistas, `[!question]-` × 2, mídia embutida (vídeo Brandon Hancock via `[!tip]`)
- **Score verificar-nota (estimado):** 9/12 — falham E5 (seção "O que vem a seguir" existe mas discute tendências gerais e bridgeia para nota 18; não aponta para nota 12 Multi-agent), P1 (sem código-com-falha — inaplicável para nota comparativa), L1 (sem wikilink cross-galho; todos os links apontam para dentro do mesmo galho Agentes de Codificação)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E5 (núcleo) — A seção "## O que vem a seguir" (linhas 359–378) cobre tendências futuras do ecossistema mas não transiciona para a nota seguinte. Adicionar parágrafo de fechamento explícito, ex: "Entender o menu de ferramentas é a metade da equação. A outra metade é saber quando combinar várias delas num pipeline coerente — o que leva diretamente à próxima nota: [[12 - Multi-agent — workflows com múltiplos agentes]]." — fecha E5 (único item de núcleo faltante) e eleva score para 10/12.
  - L1 (opcional) — Adicionar ao menos 1 wikilink cross-galho, ex: ao citar custo de tokens na seção "## Por custo mensal", linkar para a nota de Economia de Tokens; ao mencionar Gemini CLI processando codebases longas, linkar para o galho RAG e Vector Databases. Eleva score para 11/12.
  - ⚠️ Data de validade — nota com altíssima densidade de dados perecíveis: preços de assinatura e tokens (tabela "Por custo mensal", verificável em 6 meses), rankings de capacidade (mega-comparativo pode mudar a cada lançamento), projeções "em 2027" e "em 2028" (Cenário 6 e seção O que vem a seguir). Considerar adicionar `[!info]` de caducidade antes da tabela de custos mensais e do mega-comparativo avisando que preços e rankings mudam com frequência.
#### 12 - Multi-agent — workflows com múltiplos agentes
- **Estado:** 408 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 6× Mermaid, 5 casos práticos, 5× [!warning], inglês + tabela PT↔EN (14 termos), tabela comparativa (cenário × padrão), [!question]- pedagógico (2×), [!tip] com frase de impacto para entrevistas, código funcional (bash + JSON), wikilinks cross-galho (notas 05/06/13/16/17), Veja também, referências extensas com URLs
- **Score verificar-nota (estimado):** 10/12 — falham E5 (seção "O que vem a seguir" existe mas bridgeia para notas 16 e 17, não para nota 13 Devin; link para 13 está apenas no "Veja também", que não conta) e P1 (código funcional presente mas sem código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E5 (núcleo) — A seção "## O que vem a seguir" (linhas 362–383) cobre tendências futuras e menciona notas 16 e 17, mas não bridgeia para a nota seguinte do galho. Adicionar parágrafo de fechamento explícito, ex: "Antes de dominar as tendências de orquestração, vale entender como um agente individual funciona internamente — e o que acontece quando se retira o humano do loop completamente. É exatamente isso que [[13 - Devin e agentes autônomos cloud]] explora: agentes que operam em cloud sem supervisão contínua, implementando o padrão hierárquico de forma nativa." — fecha E5 e eleva score para 11/12.
#### 13 - Devin e agentes autônomos cloud
- **Estado:** 405 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart plan-act-observe), tabela comparativa (ecossistema 2026 + autônomo vs interativo + tarefas × resultado), 6 casos práticos (triage de bugs em lote, migração Spring Boot, geração de docs, testes de regressão, fix de CVEs, seed data), 6× [!warning] callouts, inglês + tabela PT↔EN (18 termos), [!question]- pedagógicos (3×), [!tip] (frase de impacto + vídeo embutido), 12 referências com URL
- **Score verificar-nota (estimado):** 10/12 — falham E5 (seção "O que vem a seguir" existe mas trata de tendências futuras do mercado, não é ponte narrativa para nota 14) e P1 (sem código-com-falha — inaplicável para nota de ferramenta/produto)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E5 (núcleo) — A seção "## O que vem a seguir" (linha 338) cobre roadmap tecnológico 2026-2028 mas não bridgeia para nota 14. Adicionar parágrafo de fechamento narrativo antes de "## Veja também", ex: "Saber delegar uma task para um agente cloud é metade do trabalho — a outra metade é configurar o ambiente em que ele opera. A [[14 - agents.md e configuração de projeto]] mostra como estruturar o repositório, o CLAUDE.md e as ferramentas disponíveis para que agentes autônomos (e interativos) trabalhem com o contexto que precisam." — fecha E5 e eleva score para 11/12.
  - Nota com alta densidade de fatos com data de validade (taxa SWE-bench ~40-55%; tabela de ferramentas com scores por player; afirmações "em 2026"); adicionar `[!info]` de caducidade no início da seção "## O ecossistema em 2026" avisando que scores SWE-bench e market share evoluem rapidamente — sinaliza ao leitor quando revisar.
#### 14 - agents.md e configuração de projeto
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (2× — flowchart carregamento + graph hierarquia), tabela comparativa (ferramentas × arquivo; ferramentas cross-tool), 4 casos práticos, 5× [!warning] callouts, código funcional (exemplos sem/com CLAUDE.md + estruturas markdown + checklist), inglês + tabela PT↔EN (12 termos), [!question]- (2×), mídia ([!tip] vídeo embutido), Veja também, Checklist de configuração
- **Score verificar-nota (estimado):** 10/12 — falham E5 (seção "O que vem a seguir" existe mas trata de tendências futuras do mercado — geração automática, CI, memória persistente, multi-agent — sem bridge narrativa para nota 15 MCP) e P1 (código funcional presente mas sem código-com-falha explícito — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E5 (núcleo) — A seção "## O que vem a seguir" (linha 359) cobre evolução futura dos arquivos de config mas não bridgeia para nota 15. Adicionar parágrafo de fechamento antes de "## Veja também", ex: "Enquanto o CLAUDE.md define o que o agente sabe sobre o projeto, ele ainda é um arquivo estático — você escreve regras e o agente aplica nas próximas sessões. O próximo passo é dar ao agente acesso dinâmico a ferramentas e contexto sob demanda: é exatamente o que o [[15 - MCP — o protocolo universal]] resolve, criando um protocolo padrão para que qualquer agente descubra e chame qualquer ferramenta em tempo real." — fecha E5, único item de núcleo faltante, e eleva score para 11/12.
#### 15 - MCP — o protocolo universal
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (2×: graph TB primitivas + sequenceDiagram tool invocation), tabelas comparativas (papéis Host/Client/Server; transportes; servers populares; quando usar/não usar), casos práticos (4: Postgres EXPLAIN, triagem issues GitHub, MCP custom legado, CI/CD loop), armadilhas (5× [!warning]: tokens de contexto, credenciais, permissões, tratamento de erro, over-engineering), inglês + tabela PT↔EN (12 termos), frase de impacto [!tip] para entrevistas, código funcional TypeScript (server custom com tool+resource+error handling = P1 satisfeito), [!question]- pedagógico (scripts vs MCP), mídia embutida [!tip] (vídeo James Briggs)
- **Score verificar-nota (estimado):** 10/12 — falham E5 (seção "O que vem a seguir" existe mas narra o roadmap do ecossistema MCP, não é ponte narrativa para nota 16) e L1 (sem wikilink cross-galho para o galho MCP dedicado — galho 9)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de bridge no início ou no final da seção "## O que vem a seguir" apontando explicitamente para `[[16 - O loop agentic — plan, act, observe]]` com motivação concreta (ex: "Agora que você tem ferramentas conectadas via MCP, o próximo passo é entender como o agente decide quando e como usá-las — o loop plan/act/observe é o mecanismo que orquestra tool invocations como as do MCP em sequências de ação coerentes") — fecha E5 e eleva score para 11/12
  - Adicionar wikilink cross-galho para o galho MCP dedicado (galho 9) em "## Veja também" (ex: nota âncora ou index do galho MCP) — fecha L1 e eleva score para 12/12
#### 16 - O loop agentic — plan, act, observe
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid (flowchart loop + sequenceDiagram hooks), tabelas comparativas múltiplas (fatores de planejamento, tools por tipo/risco, falhas comuns, arquiteturas, controles por agente, técnicas de otimização, PT↔EN 12 termos), 4 casos práticos (debugar onde quebrou, Plan Mode, loop infinito, monitoramento em tempo real), 6× [!warning] individuais, inglês + tabela PT↔EN, wikilinks cross-galho (Dicionário de IA, notas 05/12/15/17), [!tip] com mídia (vídeo Yannic Kilcher + URL), checklist de uso saudável, Veja também
- **Score verificar-nota (estimado):** 11/12 — só falta P1 (código-com-falha; inaplicável para nota operacional/conceitual)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 17 - Human-in-the-loop — quando (não) confiar
- **Estado:** 401 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid, tabelas comparativas (espectro de autonomia + matriz de risco + por fase + PT↔EN 18 termos), 7× [!warning], casos práticos (4 casos + 1 sub-caso), código funcional (settings.json + hooks.json + CLAUDE.md), checklist de configuração, [!tip] com frase de impacto para entrevista
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Reescrever o parágrafo final (ou adicionar parágrafo) da seção "## O que vem a seguir" para conectar narrativamente à nota 18 (Benchmarks e avaliação — SWE-bench): a seção atual discute o futuro do HITL em geral (HITL adaptativo, revisão assistida, auditoria proativa) mas não aponta para a próxima nota — adicionar gancho que conecte "como decidir quanta autonomia dar ao agente" à necessidade de medir capacidade real com benchmarks como SWE-bench, fechando E5 e elevando score para 11/12
  - Opcional: adicionar exemplo de código-com-falha (P1) — ex: hook com regex incorreto que deveria bloquear `rm -rf` mas não bloqueia por falta de aspas ou wildcard mal formado — ativaria P1 e elevaria score para 12/12
#### 18 - Benchmarks e avaliação — SWE-bench e além
- **Estado:** 402 linhas (piso Adepto ≥400: passa) · fase: Adepto · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid (flowchart protocolo SWE-bench + ciclo Lei de Goodhart), tabelas comparativas (versões SWE-bench, leaderboard maio 2026, scaffold × impacto, limitações, benchmarks alternativos, regras estatísticas, scorecard interno, armadilhas, PT↔EN 14 termos), 4 casos práticos (startup, time upgrade, pesquisador, CTO ROI), 5× [!warning], inglês + tabela PT↔EN, checklist de avaliação responsável, seção "Como avaliar para o SEU codebase" (passo a passo), [!tip] com vídeo Princeton NLP (URL), Veja também, Referências com URLs
- **Score verificar-nota (estimado):** 11/12 — falha só P1 (sem código-com-falha; inaplicável para nota conceitual/benchmark)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar `[!warning]` de caducidade no início da seção "## Leaderboard atual (maio 2026)" avisando que modelos, versões e scores mudam mensalmente e o leitor deve conferir em swebench.com ou Artificial Analysis — nota tem altíssima densidade de dados com data de validade (versões "Claude Opus 4.6", "GPT-5.4", "Gemini 3.1 Pro", "DeepSeek V4", "Qwen 3.6 Plus" e scores percentuais atribuídos a eles)
  - Opcional: ampliar o fechamento de "## O que vem a seguir" com gancho para outro galho IA adjacente (ex: [[Galho Evaluation]] ou [[Galho Observability]]) — a seção já fecha o ciclo do galho com solidez (aponta para notas 07, 11, 13 + 3 tendências), mas como é a última nota do galho uma ponte cross-galho tornaria a leitura ainda mais encadeada

---

## 7. AI Engineering Stack

> Galho **usa `fase:`** (01–12 = Iniciado, piso ≥300; 13 = Adepto, piso ≥400). Já enriquecido 27/06 — diagnóstico de confirmação.

### Notas

#### 01 - As 11 camadas — visão geral
- **Estado:** 308 linhas (piso Iniciado ≥300: passa — ~228 linhas de prosa + ~80 linhas em branco no final) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (graph TB 11 camadas), tabela comparativa (11 camadas × pergunta × artefato + maturidade por nível), casos práticos (2 cenários e-commerce: sem blueprint vs com blueprint), armadilhas (4× [!warning] individuais), inglês + tabela PT↔EN (15 termos), [!question]- pedagógico, Veja também (6 wikilinks cross-galho)
- **Score verificar-nota (estimado):** 11/12 — falha P1 (código-com-falha: inaplicável para nota conceitual de visão geral)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 02 - Purpose Layer — o que o sistema é
- **Estado:** 305 linhas (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart sem/com Purpose Layer), casos práticos (2 cenários e-commerce), armadilhas (3× [!warning] individuais), inglês + tabela PT↔EN (8 termos), [!question]- pedagógico, Veja também (4 wikilinks cross-galho)
- **Score verificar-nota (estimado):** 11/12 — falha P1 (código-com-falha: inaplicável para nota conceitual pura)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Remover a seção "Como explicar em inglês" duplicada (aparece duas vezes: linhas ~138 e ~159); manter a segunda versão (mais completa, com tabela PT↔EN) e excluir a primeira
#### 03 - Prompt Layer
- **Estado:** 305 linhas totais (~204 de conteúdo efetivo; linhas 205-305 são em branco) · piso Iniciado ≥300: NÃO passa (conteúdo efetivo ~204 linhas) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart "Prompt Layer vaga vs estruturada"), casos práticos (2 cenários — Q&A jurídico com prompt crescente + reconstrução com template), armadilhas (3× [!warning] individuais: versionamento, confusão Prompt/Context, forbidden_actions como única defesa), inglês + tabela PT↔EN (10 termos), [!question]- pedagógico (Prompt vs Guardrail Layer), Veja também (4 wikilinks internos)
- **Score verificar-nota (estimado):** 11/12 — falha P1 (sem código-com-falha; YAML templates presentes são funcionais, não ilustram falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Purgar as ~100 linhas em branco no fim do arquivo (linhas 205-305) — não conta para o piso, mas causa confusão na contagem
  - Adicionar exemplo de código-com-falha: system prompt minimalista que causa comportamento inesperado em produção (ex: prompt sem `uncertainty_behavior` → modelo inventa resposta em vez de escalar; mostrar a saída problemática e a versão corrigida) — ativa P1 e eleva score para 12/12, além de acrescentar ~30-40 linhas ao conteúdo efetivo
  - Expandir "Decisões-chave" ou "Anatomia" com ao menos 1 exemplo trabalhado adicional para aproximar o conteúdo efetivo do piso de 300 linhas (faltam ~96 linhas de conteúdo real)
#### 04 - Context Layer
- **Estado:** 190 linhas (piso Iniciado ≥300: não passa — linhas 191–305 são branco) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart sem/com Context Layer), casos práticos (2 cenários: context rot em pair programming + contexto dinâmico em marketing), armadilhas (3× [!warning] individuais: context rot, confusão Context/Retrieval, source material bruto), inglês + tabela PT↔EN (9 termos), [!question]- pedagógico (diferença Context vs Retrieval Layer), wikilink cross-galho ([[Context Engineering]]), Veja também (4 wikilinks internos)
- **Score verificar-nota (estimado):** 11/12 — falha P1 (sem código-com-falha; inaplicável para nota conceitual pura)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir o conteúdo efetivo de ~190 para ≥300 linhas — faltam ~110 linhas de prosa real; candidatos: aprofundar "Decisões-chave" com exemplos trabalhados (ex: pull vs push com comparativo de custo por chamada), adicionar subseção "Context pipelines na prática" (compressão periódica, expiração por horizonte, reset por unidade de trabalho), ou um terceiro cenário prático em "Casos práticos"
  - Purgar as ~115 linhas em branco no fim do arquivo (linhas 191–305) — não contam para o piso mas inflam a contagem visual
#### 05 - Output Layer
- **Estado:** 201 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (1×), casos práticos (2×), armadilhas (3× [!warning]), inglês + tabela PT↔EN (9 termos), tabela comparativa (instruction-only vs structured outputs), [!question]- pedagógico, wikilinks cross-galho ([[Structured Outputs]]), fontes com URL (OpenAI + Anthropic)
- **Score verificar-nota (estimado):** 11/12 — falha P1 (sem código-com-falha; apenas exemplos funcionais)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir de 201 para ≥300 linhas de conteúdo real (faltam ~99 linhas) — candidatos: adicionar subseção "Validação pós-output" (o que fazer quando o output sai fora do schema mesmo com structured outputs), aprofundar "Decisões-chave" com exemplos trabalhados de schema rígido vs leve, ou adicionar terceiro cenário prático (ex: sistema de geração de código com output como ação direta)
  - Adicionar ≥1 bloco de código-com-falha (ex: parser Python quebrando quando o modelo coloca prosa antes do `{`; ou Pydantic rejeitando campo extra inesperado) — ativa P1 e eleva score para 12/12
  - Purgar as ~105 linhas em branco no fim do arquivo (linhas 202–306) — não contam para o piso mas inflam a contagem visual
#### 06 - Retrieval Layer
- **Estado:** 241 linhas reais (piso Iniciado ≥300: NÃO) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart sem/com retrieval), casos práticos (2 cenários), 3× [!warning] individuais, inglês + tabela PT↔EN (9 termos), tabela comparativa (retrieval vs fine-tuning), wikilinks cross-galho (RAG e Vector Databases · Context Engineering), [!question]- pedagógico, [!summary], [!info], [!example] (fallback sequência)
- **Score verificar-nota (estimado):** 11/12 — falha apenas P1 (sem código-com-falha — inaplicável para nota de política/conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir de 241 para ≥300 linhas de conteúdo real (faltam ~59 linhas) — candidatos: aprofundar "Métricas de qualidade do retrieval" com exemplos numéricos concretos (ex: recall@5 = 3/5 vs precision@5 = 3/5 em cenário de compliance), adicionar Cenário 3 em "Casos práticos" (ex: conflito entre fontes desatualizadas em sistema jurídico — qual `conflict_rule` se aplica), ou expandir "Implementações comuns" com snippet de hybrid search + reranker em Python (BM25 → embedding → cross-encoder)
  - Purgar as ~62 linhas em branco no fim do arquivo (linhas 242–303) — não contam para o piso mas inflam a contagem visual
#### 07 - Tool Layer
- **Estado:** 219 linhas reais (piso Iniciado ≥300: NÃO) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart sem/com Tool Layer), casos práticos (2 cenários — email produção + blast radius por categoria), 3× [!warning] individuais (expor todas as tools, falha sem política, tool design negligenciado), inglês + tabela PT↔EN (10 termos), [!question]- pedagógico (tools vs chamadas convencionais), [!info] (blast radius como critério), wikilinks cross-galho (Anatomia de Agents · MCP)
- **Score verificar-nota (estimado):** 11/12 — falha apenas P1 (sem código-com-falha — inaplicável para nota de política/conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir de 219 para ≥300 linhas de conteúdo real (faltam ~81 linhas) — candidatos: (a) adicionar Cenário 3 em "Casos práticos" mostrando tool failure handling na prática (ex: `create_ticket` retorna 500, agent improvisa e duplica o ticket — e como a política de retry+fallback teria evitado); (b) aprofundar "Tool design é trabalho de engenharia" com snippet de schema bem vs mal descrito lado a lado (YAML), ativando também P1 (código-com-falha) e elevando score para 12/12; (c) expandir "Categorias de tools" com exemplos concretos de cada categoria em código (nome de função + assinatura tipada)
#### 08 - Workflow vs Agent Layer
- **Estado:** 201 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart workflow vs agent), casos práticos (2 cenários), armadilhas (3× [!warning]), inglês + tabela PT↔EN (10 termos), checklist de decisão, [!summary] (regra de ouro), [!question]- pedagógico, Veja também, wikilinks cross-galho
- **Score verificar-nota (estimado):** 11/12 — falha apenas P1 (sem código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir de 201 para ≥300 linhas de conteúdo real (faltam ~99 linhas) — candidatos: (a) adicionar Cenário 3 em "Casos práticos" mostrando um caso limítrofe — tarefa que começou como workflow, divergiu e migrou para agent, com o custo da migração; (b) adicionar seção de ferramentas/frameworks que implementam a distinção (LangGraph para agent, Prefect/Temporal para workflow) com exemplo de como cada um codifica a decisão arquitetural; (c) adicionar snippet código-com-falha (ex: loop agentic sem kill switch esgotando o contexto de 200k tokens em produção — TypeError ou ContextLengthExceeded) — ativa P1 e eleva score para 12/12
#### 09 - Evaluation Layer
- **Estado:** 199 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart sem/com Evaluation Layer), casos práticos (2 cenários), 3× [!warning], inglês + parágrafo EN, tabela PT↔EN (10 termos), [!question]- pedagógico, [!info], wikilinks cross-galho ([[Evaluation]], [[Anatomia de Agents]], [[RAG e Vector Databases]]), Veja também
- **Score verificar-nota (estimado):** 11/12 — falta apenas P1 (código-com-falha; inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir de 199 para ≥300 linhas de conteúdo real (faltam ~101 linhas) — candidatos: (a) adicionar seção "Ferramentas de eval" com comparativo entre Braintrust, PromptFoo, LangSmith e Ragas, cada uma com 2-3 linhas de contexto de uso; (b) expandir "Tipos de eval" com exemplos concretos de código YAML/JSON para reference-based e reference-free; (c) adicionar Cenário 3 em "Casos práticos" cobrindo eval de sistema RAG (recall@k, faithfulness, answer relevance) — conecta ao wikilink cross-galho já existente
#### 10 - Guardrail Layer
- **Estado:** 199 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart sem/com Guardrail Layer), casos práticos (2 cenários), 3× [!warning], inglês + parágrafo EN, tabela PT↔EN (10 termos), [!question]- pedagógico, [!info] (falso positivo vs negativo), wikilinks cross-galho ([[Segurança e Guardrails]], [[Context Engineering]]), Veja também
- **Score verificar-nota (estimado):** 11/12 — falta apenas P1 (código-com-falha; inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir de 199 para ≥300 linhas de conteúdo real (faltam ~101 linhas) — candidatos: (a) adicionar seção "Ferramentas de guardrail" com comparativo entre NeMo Guardrails, Guardrails AI e LangChain moderation, cada uma com 2-3 linhas de contexto de uso e quando escolher; (b) expandir "Calibrando thresholds" com exemplo concreto de log de disparo e ajuste de threshold em YAML; (c) adicionar Cenário 3 em "Casos práticos" cobrindo guardrail de PII em sistema de saúde (redação de CPF/CRM antes do modelo ver, verificação no output) — conecta ao wikilink cross-galho [[Segurança e Guardrails]]
#### 11 - Logging Layer
- **Estado:** 211 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart sem/com Logging Layer), casos práticos (2 cenários), 3× [!warning], inglês + seção EN completa, tabela PT↔EN (10 termos), [!question]- pedagógico, [!example] (dashboard mínimo), wikilinks cross-galho ([[Observability]] — galho dedicado, L1 ✓), fontes com URL (OpenTelemetry + Langfuse)
- **Score verificar-nota (estimado):** 11/12 — falta apenas P1 (código-com-falha; inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir de 211 para ≥300 linhas de conteúdo real (faltam ~89 linhas) — candidatos: (a) adicionar seção "Ferramentas de logging" comparando OpenTelemetry GenAI, Langfuse, Phoenix e Datadog com 2-3 linhas de contexto de uso por ferramenta e quando escolher cada uma; (b) expandir cada um dos 3 [!warning] com parágrafo adicional de resolução concreta (o que fazer, não só o que evitar); (c) adicionar Cenário 3 em "Casos práticos" cobrindo a estratégia de sampling em sistema de alto volume (100% erros + amostra de sucessos), conectando diretamente à seção "Decisões-chave" item 4
#### 12 - Improvement Layer
- **Estado:** 203 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart sem/com Improvement Layer), casos práticos (2 cenários), inglês + tabela PT↔EN (9 termos), 3× `[!warning]` individuais, `[!info]` (regra de triagem), `[!question]-` pedagógico, wikilink cross-galho L1 (`[[Improvement Loop]]`), fontes com URLs L2 (hamel.dev + docs.anthropic.com)
- **Score verificar-nota (estimado):** 11/12 — falta P1 (código-com-falha; inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir de 203 para ≥300 linhas de conteúdo real (faltam ~97 linhas) — candidatos: (a) expandir cada um dos 3 `[!warning]` com parágrafo de resolução concreta (o que fazer, não só o que evitar); (b) adicionar Cenário 3 em "Casos práticos" cobrindo drift detection automático num sistema de alto volume (alertas de score + threshold); (c) adicionar subseção "Ferramentas" dentro de "Decisões-chave" comparando Langfuse, Phoenix e Datadog GenAI como clientes do loop
#### 13 - Setup completo — do zero ao sistema de produção
- **Estado:** ~390 linhas reais (piso Adepto ≥400: não passa — borderline, ~10 linhas abaixo; candidata à isenção de capstone por ser a última nota do galho) · fase: Adepto · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart ordem de construção), `[!question]-` pedagógico (por que ordem ≠ numérica), casos práticos extensos (11 passos com AI Weekly Newsletter Generator), 3× `[!warning]` individuais (armadilhas), inglês + tabela PT↔EN (10 termos), wikilinks cross-galho múltiplos (Evaluation/RAG/Anatomia de Agents/Segurança e Guardrails/Observability/Context Engineering/Improvement Loop), checklist de pré-produção (10 itens), `[!info]`, `[!note]`
- **Score verificar-nota (estimado):** 11/12 — falta P1 (código-com-falha; inaplicável para recipe conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir ~10 linhas para atingir o piso de 400 — candidatos: (a) adicionar um 4º `[!warning]` na seção "Armadilhas comuns" cobrindo "começar a construir todas as camadas ao mesmo tempo antes de validar a Purpose Layer" (erro sistêmico não coberto pelos três existentes); (b) expandir o checklist final com sub-itens de rollback — OU aplicar isenção de capstone (é a última nota do galho, funciona como recipe de fechamento do ciclo)
  - Corrigir `status: seedling` → `growing` no frontmatter — a nota está substancialmente completa (11/12, núcleo integral, seção de ponte para outros galhos)

---

## 8. RAG e Vector Databases

> Galho **usa `fase: Iniciado`** em todas (piso ≥300). Já enriquecido 27/06 — diagnóstico de confirmação. Checar conteúdo real (rodapé em branco pode inflar contagem, como no galho 7).

### Notas

#### 01 - O que é RAG e quando usar
- **Estado:** 187 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Mermaid (2×: decision tree + pilares de qualidade), tabela comparativa (RAG vs fine-tuning vs long context), inglês + tabela PT↔EN (10 termos), armadilhas (3× `[!warning]`), `[!question]-` pedagógico (RAG vs fine-tuning), `[!tip]` (citação de fontes + "O que diferencia um senior"), casos práticos (multi-tenant, compliance, context-stuffing benchmark), Veja também
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir a nota para ≥300 linhas de conteúdo real — atualmente 187 linhas reais; as ~119 finais são branco; o piso Iniciado não passa
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## A definição operacional" (ex: engenheiro que recebe uma pergunta sobre um documento interno e o LLM alucina porque não tem acesso aos dados da empresa) — ativa E2 e eleva score para 10/12
  - Adicionar URLs reais às referências (Pinecone Learn RAG, Anthropic Contextual Retrieval blog, Lewis et al. arXiv:2005.11401, Eugene Yan blog) — ativa L2 e eleva score para 11/12
#### 02 - Anatomia do pipeline RAG
- **Estado:** 244 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗ (sem URLs)
- **Opcionais presentes:** Mermaid (graph TB), tabelas (latência/custo/métricas), casos práticos (SQL, prompt template, cálculo de custo), 3× [!warning] individuais, inglês + tabela PT↔EN (10 termos), [!question]- pedagógico, Veja também
- **Score verificar-nota (estimado):** 9/12 — falham E2 (sem abertura-problema), L2 (referências sem URLs), P1 (sem código-com-falha — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## As duas fases" (ex: engenheiro com sistema RAG que responde errado — identifica que o retrieval trouxe chunks irrelevantes, não o LLM) — ativa E2 e eleva score para 10/12
  - Adicionar URLs reais às referências (Anthropic Contextual Retrieval blog, Pinecone Learn RAG, LlamaIndex docs) — ativa L2 e eleva score para 11/12
  - Expandir conteúdo para ≥300 linhas reais (gap de ~56 linhas) — ângulo natural: seção de debugging end-to-end ("minha resposta está ruim: como isolo qual passo quebrou?") ou caso prático completo com código real de indexing + query
#### 03 - Embeddings — representação semântica
- **Estado:** 228 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Mermaid (1×, flowchart encoder→vetor), tabelas comparativas (modelos 2026 × dims/custo; dims × qualidade/latência; dense vs sparse; métricas alvo; anti-patterns), casos práticos (cálculo de custo indexing + query, matryoshka truncamento), 4× [!warning] individuais (lock-in, trocar modelo sem re-indexar, texto bruto sem pré-processamento, multilíngue desigual), inglês + tabela PT↔EN (10 termos), seção técnica de entrevista com fala modelo, [!tip] (default 2026), [!question]- pedagógico (cosseno vs euclidiana), código funcional Python (matryoshka truncamento)
- **Score verificar-nota (estimado):** 10/12 — falham E2 (sem abertura com problema/cenário; nota abre com TL;DR → código → "## A intuição"), L2 (referências sem URLs clicáveis — só nomes/títulos), P1 (sem código-com-falha — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com problema/cenário antes de "## A intuição" (ex: engenheiro tentando busca semântica com LIKE no banco e obtendo resultados irrelevantes — a intuição de por que vetores resolvem isso) — ativa E2, eleva score para 11/12, e contribui com ~10 linhas em direção ao piso
  - Adicionar URLs reais às referências (openai.com/docs/embeddings, voyageai.com/docs, cohere.com/docs/embed, huggingface.co/spaces/mteb/leaderboard, arxiv.org/abs/2004.04906 para DPR) — ativa L2 e eleva score para 12/12
  - Expandir conteúdo para ≥300 linhas reais (gap ~72 linhas) — ângulo natural: seção "Avaliando embeddings" (benchmarks MTEB × realidade do domínio, golden set de pares relevantes, pitfall do "MTEB não é o seu dado") ou caso prático completo de escolha de modelo para PT-BR com comparativo de qualidade domain-specific
  - Observação L1: nota tem wikilinks cross-galho para Dicionário de IA mas NÃO linka para [[03 - Embeddings — do token ao vetor]] (Anatomia dos LLMs) — adicionar menção em "Veja também" para fechar a bridge semântica entre os dois galhos
#### 04 - Chunking — onde 50% da qualidade vive
- **Estado:** ~252 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗ (sem URLs)
- **Opcionais presentes:** casos práticos (contextual FastAPI, validação, metadata), inglês + PT↔EN (10 termos), 3× [!warning], [!question]-, [!tip], código funcional (Python/JSON), tabelas comparativas, "Veja também"
- **Score verificar-nota (estimado):** 8/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## A regra de ouro" (ex: engenheiro que indexa 100k docs, queries voltam com resultados irrelevantes — e o culpado é o chunking, não o modelo de embedding) — ativa E2, eleva score para 9/12
  - Adicionar URLs reais às referências (anthropic.com/research/contextual-retrieval, python.langchain.com/docs/text_splitters, docs.llamaindex.ai) — ativa L2, eleva score para 10/12
  - Expandir conteúdo para ≥300 linhas reais (gap ~48 linhas) — ângulo natural: seção "Erros reais de chunking" com casos documentados (tabela quebrada em produção, PDF multi-coluna, código Python fragmentado entre função) ou aprofundamento do contextual chunking com snippet Anthropic API real
#### 05 - Vector databases — pgvector, Pinecone, Qdrant
- **Estado:** 299 linhas reais (piso Iniciado ≥300: não passa — 1 linha curta) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (heurística de escolha), tabelas comparativas (opções × critérios; index types; performance × escala; custo × hosting), 3× [!warning] individuais, código funcional (pgvector SQL + Pinecone Python + Qdrant Python + Weaviate Python), inglês + tabela PT↔EN (10 termos), [!question]- pedagógico, anti-patterns, métricas, Veja também
- **Score verificar-nota (estimado):** 9/12 — falham E2 (sem parágrafo de abertura narrativa antes do corpo técnico — TL;DR enquadra o problema mas não conta como abertura), P1 (sem código-com-falha), L2 (referências com domínios em itálico, sem URLs clickáveis `https://…`)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## O que vector DB faz" (ex: engenheiro que escolhe Pinecone no início do projeto, migra para pgvector depois porque já tinha Postgres — e percebe que perdeu semanas à toa; ou time que confunde qualidade do vector DB com qualidade do RAG) — ativa E2, fecha único item de núcleo faltante, e resolve o piso (eleva linhas reais para ≥300), eleva score para 10/12
  - Converter referências de domínios em itálico para URLs clickáveis reais (`https://github.com/pgvector/pgvector`, `https://docs.pinecone.io`, `https://qdrant.tech/documentation`, `https://weaviate.io/developers`, `https://ann-benchmarks.com`) — ativa L2, eleva score para 11/12
  - Adicionar `[!warning]` de caducidade antes da tabela "## Custo típico (1M chunks, 1M queries/mês)" sinalizando que preços mudam com frequência e o leitor deve verificar direto nos sites dos providers — nota de ferramentas com preços específicos ($25-300/mês) datados
#### 06 - Retrieval — hybrid search, BM25, query rewriting
- **Estado:** 306 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗ (5 referências sem URLs clicáveis)
- **Opcionais presentes:** inglês + tabela PT↔EN (10 termos), 3× [!warning], tabela comparativa (falhas do vector por caso), código funcional (RRF Python, weighted score, LLM rewrite, HyDE, multi-query, metadata SQL, pipeline completo), [!question]- pedagógico, casos práticos, seção "Quando NÃO precisa de hybrid", Métricas com tabela, Anti-patterns, Veja também
- **Score verificar-nota (estimado):** 10/12 — falham E3 (sem Mermaid) · L2 (referências sem URLs)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs clicáveis às 5 referências da seção "## Referências" (Anthropic Contextual Retrieval 2024, HyDE arxiv 2212.10496, RRF paper Cormack 2009, Pinecone hybrid guide, BM25 Robertson 1994) — ativa L2 e fecha o único item de núcleo faltante, elevando score para 11/12
  - Opcional: adicionar 1× Mermaid com flowchart do pipeline completo (rewrite → HyDE → hybrid top-50 → RRF → rerank → top-k) — ativa E3 e eleva score para 12/12
#### 07 - Reranking — Cohere, Voyage, cross-encoders
- **Estado:** 146 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗ (referências sem URLs clicáveis; apenas "github.com/…" sem https://)
- **Opcionais presentes:** Mermaid · Tabela comparativa · Casos práticos (Anthropic Contextual Retrieval + 2 blocos de código) · 3× [!warning] · Inglês + tabela PT↔EN · [!question]- · Wikilink cross-galho
- **Score verificar-nota (estimado):** 10/12 — falham P1 (sem código-com-falha) · L2 (sem URL real nas referências)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir conteúdo para atingir piso de 300 linhas reais (nota tem 146 — precisa ~154 linhas adicionais): aprofundar seção de métricas com exemplos numéricos reais, adicionar seção sobre domain-specific fine-tuning de rerankers, expandir "Filtragem antes de rerank" com pipeline completo comentado
  - Adicionar URLs clicáveis às referências (Anthropic Contextual Retrieval: https://www.anthropic.com/news/contextual-retrieval; BGE: https://github.com/FlagOpen/FlagEmbedding) — fecha L2
  - Opcional: adicionar bloco P1 mostrando código com falha (rerank sem hybrid → garbage in, garbage out com output ilustrativo)
#### 08 - Generation — passar contexto ao LLM com citação
- **Estado:** 352 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Inglês (E6) ✓ · PT↔EN (E7, 10 termos) ✓ · Casos práticos (E4, patterns/code) ✓ · Armadilhas ≥3 [!warning] (E8) ✓ · Wikilink cross-galho (L1) ✓ · [!question]- pedagógico · [!tip] (tiering + "não sei") · tabelas comparativas (faithfulness, modelos, latência, métricas, output formats) · código funcional (Pydantic, Python, prompts)
- **Score verificar-nota (estimado):** 8/12 — falham E2 (abertura-problema: nota vai de TL;DR direto para "## A estrutura do prompt" sem parágrafo de cenário visível), E3 (sem Mermaid), P1 (sem código-com-falha), L2 (referências sem URLs clicáveis — arXiv ids presentes mas não linkados)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura visível (não colapsável) antes de "## A estrutura do prompt" descrevendo um cenário concreto de falha (ex: "Você recuperou os 5 chunks certos, mas a resposta misturou contexto com conhecimento de treinamento sem avisar o usuário — é aqui que RAG sem citação vira chatbot disfarçado") — fecha E2 (núcleo faltante) e eleva score para 9/12
  - Adicionar URLs clicáveis às referências (ex: Liu et al. → https://arxiv.org/abs/2307.03172; Asai et al. → https://arxiv.org/abs/2310.11511; Yan et al. → https://arxiv.org/abs/2401.15884; Anthropic Citations API → https://www.anthropic.com/news/introducing-citations) — fecha L2 e eleva score para 10/12
  - Opcional: adicionar 1 diagrama Mermaid (ex: sequenceDiagram do pipeline retrieve→rerank→extract→generate→verify) — fecha E3 e eleva score para 11/12
#### 09 - Evaluation de RAG
- **Estado:** 325 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (1×), casos práticos (golden set YAML, CI pipeline YAML, A/B test Python), 3× [!warning] individuais (armadilhas comuns), inglês + tabela PT↔EN (10 termos), [!question]- pedagógico, [!example] (diagnóstico de maturidade), código funcional (Ragas Python + CI YAML + A/B Python), tabelas comparativas (tools alternativas + métricas-alvo), wikilink cross-galho L1 (Evaluation + 10 - RAG vs long context)
- **Score verificar-nota (estimado):** 10/12 — falham E2 (sem parágrafo de abertura com cenário/problema; nota vai direto TL;DR→callouts→mecanismo) e L2 (referências sem URLs https:// — só domínios e títulos de paper)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura (2-3 frases) antes do TL;DR ou logo após o `# Evaluation de RAG` apresentando o cenário: "você deployou um RAG, as respostas parecem boas nos testes manuais, mas em produção surgem erros sutis — e você não sabe se o problema está no retrieval, no reranking ou no generation" — ativa E2 e eleva score para 11/12
  - Adicionar URLs completas (https://) às referências: `https://docs.ragas.io`, `https://www.trulens.org`, `https://deepeval.com`, `https://arxiv.org/abs/2309.15217` (paper RAGAS), `https://eugeneyan.com` (Eugene Yan) — ativa L2 e eleva score para 12/12
#### 10 - RAG vs long context vs fine-tuning
- **Estado:** 240 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Mermaid (decision tree flowchart), 3× tabela comparativa (aspectos, custo, decisão prática), 3× [!example] casos reais, 3× [!warning] armadilhas, [!question]- (long context vs RAG), Como explicar em inglês + tabela PT↔EN (10 termos), Anti-patterns, Métricas para comparar, Veja também
- **Score verificar-nota (estimado):** 10/12 — falham P1 (sem código-com-falha — inaplicável para nota conceitual) e L2 (referências sem URLs clicáveis)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs completas à seção "## Referências" (ex: `https://platform.openai.com/docs/guides/fine-tuning`, `https://docs.anthropic.com/en/docs/build-with-claude/context-windows`, `https://eugeneyan.com/writing/llm-patterns/`, `https://ai-engineering.ai`) — ativa L2 e eleva score para 11/12
  - Expandir corpo com ~65 linhas reais para atingir piso Iniciado de 300: aprofundar a seção "Híbridos" com um fluxo passo-a-passo (escolha inicial → golden set → critérios de adição de componente) e adicionar [!question]- pedagógico sobre quando híbrido prematuro vira dívida técnica
#### 11 - Padrões avançados — Graph RAG, Agentic RAG, multi-hop
- **Estado:** 341 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (3×), tabela comparativa (métricas×custo, quando usar/não usar), casos práticos (multi-hop query example, custo por padrão, domínios de uso), `[!warning]` (3×), `[!tip]`, `[!question]-`, inglês+PT↔EN (10 termos + bloco interview), código funcional Python e pseudocode, wikilinks cross-galho ([[Anatomia de Agents]], [[Context Engineering]], [[Memória de Agentes]]), Veja também
- **Score verificar-nota (estimado):** 11/12
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 12 - Setup completo — checklist de produção
- **Estado:** 339 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Mermaid (gantt 4 fases), 3× `[!warning]` individuais, inglês+PT↔EN (10 termos + bloco interview), `[!question]-` (por que a ordem importa), código funcional SQL (schema pgvector + hybrid RRF) + Python (pipeline async), tabela comparativa (métricas-alvo de produção), checklists interativos por fase ([ ]), Veja também
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de `## Stack recomendada` (ex: equipe que deployou RAG "funcionando em dev" e levou um colapso em produção por ausência de fallback e sem evaluation) — ativa E2 e eleva score para 11/12
  - Adicionar URLs reais às referências do `## Referências` (Anthropic Contextual Retrieval blog, Eugene Yan blog, Pinecone production guide, Chip Huyen AI Engineering) — ativa L2 e eleva score para 12/12
#### 13 - PageIndex — RAG vectorless por árvore de documentos
- **Estado:** 174 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling / progress: backlog
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (1×), tabela comparativa (RAG vetorial vs PageIndex), casos práticos (quando usar/não usar com cenários concretos + FinanceBench 98,7%), armadilhas (3× [!warning] individuais), inglês + tabela PT↔EN (10 termos), wikilinks cross-galho (Memória de Agentes, Dicionário de IA), [!question]- pedagógico, Veja também
- **Score verificar-nota (estimado):** 11/12 (P1 código-com-falha ausente — inaplicável para nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Nota está 126 linhas abaixo do piso Iniciado (≥300): expandir "## Como funciona" com exemplo de nó JSON real mostrando a estrutura da árvore (title/node_id/start_index/end_index/summary/nodes), e expandir "## Relação com padrões avançados" detalhando o mecanismo de cada família (Agentic RAG, Hierarchical retrieval, Long-context RAG) com diferencial concreto — principal gap
  - Atualizar `status: seedling` e `progress: backlog` para refletir o estado real da nota (conteúdo já maduro)

---

## 9. MCP

> Galho **usa `fase: Iniciado`** (piso ≥300). Enriquecido 28/06 (lote do padrão completo). Checar conteúdo real.

### Notas

#### 01 - O que é MCP e por que importa
- **Estado:** 191 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** inglês + tabela PT↔EN (10 termos), 3× [!warning], tabela comparativa (function calling vs MCP), casos práticos (3 cenários "quando MCP brilha"), [!question]- pedagógico, [!tip] (top 10 senior), [!info] (stewardship), Veja também
- **Score verificar-nota (estimado):** 8/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Piso: 191 linhas reais < 300 (Iniciado) — expandir ~110 linhas adicionando seção de casos práticos detalhados (ex: walkthrough de um MCP server mínimo com anotação do que cada primitivo representa no código) ou expandindo "## Quando MCP brilha/NÃO é a resposta" com exemplos narrados
  - TL;DR tem apenas 1 linha longa — expandir para ≥3 linhas densas no callout `[!abstract]` — ativa E1 e eleva score 8→9
  - Adicionar ≥1 diagrama Mermaid (ex: sequenceDiagram client↔server mostrando handshake list_tools + tool_call, ou graph LR da topologia N×M→N+M com labels) — ativa E3 e eleva score para 10/12
  - Converter referências para hyperlinks clicáveis (`[modelcontextprotocol.io](https://modelcontextprotocol.io)`, `[github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)`, `[awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)`) — ativa L2 e eleva score para 11/12
#### 02 - Os três primitivos — Tools, Resources, Prompts
- **Estado:** 303 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** tabela comparativa (6 critérios × 3 primitivos + métricas de server), tabela PT↔EN (10 termos), inglês + bloco de entrevista, 3× [!warning] (tudo-como-tool · nomes ambíguos · prompt-como-tool), P1 código-com-falha (3 anti-patterns com correto ao lado), casos práticos (GitHub MCP server end-to-end), discovery flow, [!question]- pedagógico (por que 3 primitivos)
- **Score verificar-nota (estimado):** 9/12 — falham E2 (corpo começa direto em "## A tríade" + bloco ASCII, sem parágrafo narrativo de problema), E3 (só ASCII art, sem bloco ```mermaid```), L2 (referências nomeiam fontes mas não têm URLs clicáveis)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo narrativo de abertura (antes de "## A tríade") com cenário de problema concreto — ex: "Você está desenhando um MCP server e coloca tudo como Tool. Funciona, mas o LLM chama a tool do schema do banco a cada turno, desperdiçando budget e adicionando latência. Qual é o erro?" — ativa E2 e eleva score para 10/12
  - Converter referências para hyperlinks clicáveis (`[modelcontextprotocol.io](https://modelcontextprotocol.io/docs/concepts/tools)`, `[Building MCP servers](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)`, `[Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)`) — ativa L2 e eleva score para 11/12
  - Adicionar diagrama Mermaid (ex: `graph LR` comparando quem invoca cada primitivo: LLM → Tool, Client → Resource, LLM/User → Prompt) — ativa E3 e eleva score para 12/12
#### 03 - Arquitetura cliente-servidor
- **Estado:** 354 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (3×: graph LR, sequenceDiagram, graph TD decisão), tabela comparativa (latências por transport), casos práticos (anti-patterns + discovery patterns + configuração por client), armadilhas (3× [!warning] individuais), inglês + tabela PT↔EN (10 termos), [!question]- pedagógico (abertura), código funcional (JSON-RPC + config JSON por client), Veja também
- **Score verificar-nota (estimado):** 9/12 — falham P1 (sem código-com-falha — inaplicável para nota conceitual), L1 (sem wikilink cross-galho para outro galho IA), L2 (referências com domínios mas sem links Markdown clicáveis)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Converter referências para hyperlinks Markdown clicáveis (`[modelcontextprotocol.io/spec](https://modelcontextprotocol.io/spec)`, `[jsonrpc.org](https://www.jsonrpc.org/specification)`, `[MCP Inspector](https://github.com/modelcontextprotocol/inspector)`) — ativa L2 e eleva score para 10/12
  - Adicionar ao menos 1 wikilink cross-galho (ex: `[[Context Engineering]]` ou `[[Agentes de Codificação]]`) em seção relevante (ex: capabilities negotiation remete a agentes, stdio remete a Claude Code) — ativa L1 e eleva score para 11/12
#### 04 - MCP servers oficiais e populares
- **Estado:** 284 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** [!question]- pedagógico, tabelas comparativas (múltiplas: recursos/onde achar, categorias, avaliação, métricas), casos práticos (stack Codex + defaults fullstack + anti-patterns), 3× [!warning] + 1× [!danger], inglês + tabela PT↔EN (10 termos), código funcional (JSON config + bash desinstalação), Veja também
- **Score verificar-nota (estimado):** 8/12 — falham E2 (sem abertura-problema; nota abre direto no TL;DR sem cenário/narrativa), E3 (sem Mermaid), P1 (sem código-com-falha), L2 (referências como texto simples — sem links Markdown clicáveis com URL)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com cenário/problema concreto antes do TL;DR (ex: "Você precisa conectar seu agente ao GitHub, Postgres e Slack — escrever três servers do zero levaria semanas; mas provavelmente tudo já existe") — ativa E2 e eleva score para 9/12 (passa o gate)
  - Converter referências para links Markdown clicáveis (`[punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)`, `[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)`, `[mcp.so](https://mcp.so)`, `[smithery.ai](https://smithery.ai)`) — ativa L2 e eleva score para 10/12
  - Adicionar 1 diagrama Mermaid (ex: flowchart de decisão `install vs build`) — ativa E3 e eleva score para 11/12
  - Sinalizar caducidade: catálogo de servers envelhece rápido — adicionar `[!warning]` no topo de "## Categorias principais (2026)" avisando que nomes de packages, URLs e status de manutenção mudam com frequência; verificar no marketplace antes de instalar
  - Expansão de conteúdo cobre o gap do piso: abertura + Mermaid + callout de caducidade já adicionam as ~20 linhas que faltam para ≥300
#### 05 - Construindo um MCP server local
- **Estado:** 421 linhas totais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ (1 linha densa, regra pede ≥3) · Abertura-problema ✗ (salta direto para Setup mínimo sem parágrafo intro) · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗ (URLs em itálico `*github.com/...*`, sem links Markdown clicáveis)
- **Opcionais presentes:** [!question]- · casos Bom/Ruim e Errado/Certo (E4) · Como explicar em inglês (E6) · tabela PT↔EN (E7) · 3× [!warning] (E8) · código-com-falha Ruim/Errado (P1) · wikilink cross-galho Anatomia de Agents (L1)
- **Score verificar-nota (estimado):** 8/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir [!abstract] TL;DR para ≥3 linhas (quebrar em 3 bullets: o que é, como funciona, o que importa de verdade) — ativa E1, eleva score para 9/12 (passa o gate)
  - Adicionar parágrafo de abertura após TL;DR e antes de "## Setup mínimo", descrevendo o cenário/problema concreto (ex: "Você quer expor seu banco de dados ou APIs internas para agentes — sem reescrever a integração em cada client") — ativa E2, eleva score para 10/12
  - Converter referências para links Markdown clicáveis com `https://` (MCP Python SDK, TypeScript SDK, Inspector, tutorial Anthropic) — ativa L2, eleva score para 11/12
  - (Opcional) Adicionar diagrama Mermaid mostrando o fluxo stdio: client → subprocess → server → tools — ativa E3, eleva score para 12/12
#### 06 - MCP remoto — HTTP + SSE para times
- **Estado:** 376 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Mermaid (arquitetura load-balancer), casos práticos (Docker/K8s/Cloudflare Workers/rate-limit/auth), 3× [!warning] (sem health check · dev vs prod · audit log só em erro), inglês + tabela PT↔EN (10 termos), tabela de custo por setup, tabela métricas-alvo, [!question]- (riscos de rede vs stdio), código funcional (Python FastMCP+SSE · Starlette auth · K8s YAML · Dockerfile), wikilinks cross-galho (Segurança e Guardrails), Veja também
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura narrativo antes de "## Quando partir para HTTP+SSE" descrevendo o cenário-problema concreto (ex: "Cinco devs do time precisam do mesmo servidor de banco de dados — cada um spawna um subprocess? Em produção isso se torna ingerenciável") — ativa E2, eleva score para 10/12
  - Converter referências para links Markdown clicáveis com `https://` (ex: `[MCP Spec — Transports](https://modelcontextprotocol.io/docs/concepts/transports)`, `[Smithery](https://smithery.ai)`, Cloudflare Workers for MCP) — ativa L2, eleva score para 11/12
  - (Opcional) Adicionar exemplo de código-com-falha (ex: client tentando conectar sem header `Authorization` e recebendo 401, ou server sem TLS servindo em `http://` e sendo rejeitado por client moderno) — ativa P1, eleva score para 12/12
#### 07 - Segurança em MCP
- **Estado:** 327 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid, casos práticos (3 cautionary tales), armadilhas 3× [!warning], código funcional + exemplos de ataque (injection/exfiltração), inglês + tabela PT↔EN, [!question]- pedagógico, [!example] checklist, tabela de métricas, wikilinks cross-galho (Segurança e Guardrails + Anatomia de Agents), OWASP Top 10 mapping, Anti-patterns, tools banidas
- **Score verificar-nota (estimado):** 11/12 — falha L2 (referências sem URLs completas com https://)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Converter as 4 referências finais para links Markdown clicáveis com `https://` (ex: `[OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)`, `[MCP Spec — Security](https://modelcontextprotocol.io/spec/security)`) — ativa L2 e eleva score para 12/12
#### 08 - Ecossistema 2026 — clients e integrações
- **Estado:** ~327 linhas reais (371 total, ~44 em branco) (piso Iniciado ≥300: passa) · fase: Iniciado · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ (1 linha comprimida — abaixo de ≥3 linhas separadas) · Abertura-problema ✗ (vai direto para tabelas após TL;DR, sem parágrafo narrativo de cenário) · Corpo-mecanismo ✓ (seção "Maturação do protocolo 2026" + MCP Tasks + code-execution explicam o porquê) · O que vem a seguir ✓ (seção narrativa genuína → nota 09) · Fontes ✓ (múltiplas URLs reais em Referências)
- **Opcionais presentes:** Mermaid (1× sequenceDiagram MCP Tasks), tabelas comparativas (clients por vendor + métricas de adoção + PT↔EN), inglês + entrevista técnica (seção "Como explicar em inglês"), PT↔EN (10 termos), 3× [!warning] individuais (Tasks experimental · discovery overhead · marketplace trust), anti-patterns (lista), casos práticos (4 casos — internal API, onboarding docs, operações com aprovação, vault pessoal), [!info]/[!note]/[!tip] pedagógicos, wikilinks cross-galho (Anatomia de Agents, Agentes de Codificação), código funcional (Smithery JSON + LangChain/LlamaIndex/Vercel Python/TS)
- **Score verificar-nota (estimado):** 9/12 — falham E1 (TL;DR em 1 linha, não ≥3), E2 (abertura-problema ausente), P1 (código presente mas sem exemplo de falha — inaplicável para nota de panorama)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir `[!abstract]` de 1 parágrafo comprimido para ≥3 linhas separadas (ex: linha 1 — protocolo virou inter-vendor; linha 2 — quem adotou e o ecossistema de 3000+ servers; linha 3 — o que mudou em 2026: Tasks + code-execution + managed hosting) — ativa E1 e eleva score para 10/12
  - Adicionar parágrafo de abertura com cenário antes de `## Os clients que falam MCP` (ex: "Você avalia qual client MCP adotar para a equipe. Em 2024 havia incompatibilidades entre ferramentas; em 2026 há um padrão inter-vendor com 15+ clients. Por que o consenso emergiu tão rápido?") — ativa E2 e eleva score para 11/12
  - Sinalizar caducidade: adicionar `[!warning]` ou `[!info]` de validade na seção `## Métricas de adoção (2026)` (números 3000+, 100K-1M installs/mês, 80% coding agents) — nota de panorama de ecossistema envelhece rápido; leitor deve conferir Awesome MCP Servers e smithery.ai para dados atuais
#### 09 - Casos comuns no mercado
- **Estado:** 320 linhas reais (piso Iniciado ≥300: passa ✓) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 5 casos práticos reais (telecom, SaaS B2B, solo dev, Codex), 3× [!warning] individuais, tabelas comparativas (por caso), código funcional (Python + JSON), inglês + tabela PT↔EN (10 termos), [!question]- pedagógico, patterns nomeados (3 patterns)
- **Score verificar-nota (estimado):** 10/12 — falham E3 (sem Mermaid), L2 (3 referências sem URL clicável; só nomes e descrições)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs reais às referências (ex: Anthropic blog, github.com/punkpeye/awesome-mcp-servers, blog.cloudflare.com/remote-model-context-protocol-servers-on-cloudflare/) — ativa L2 e eleva score para 11/12
  - Opcional: adicionar 1 diagrama Mermaid mostrando os 5 casos como graph (ex: `graph TD MCP --> Caso1 & Caso2 & Caso3 & Caso4 & Caso5`) — ativa E3 e eleva score para 12/12
#### 10 - Setup completo + best practices
- **Estado:** ~393 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✗ · Fontes ✓
- **Opcionais presentes:** Mermaid (Gantt 4 fases), código ❌/✅ (P1), inglês + tabela PT↔EN (10 termos), 3× [!warning] (armadilhas), [!tip] (7 princípios), [!question]- pedagógico, tabelas comparativas (métricas-alvo + Quando expandir), wikilinks cross-galho (Anatomia de Agents, Dicionário de IA#tracing)
- **Score verificar-nota (estimado):** 9/12 — falham E2 (nota abre direto em "Stack recomendada" sem parágrafo-cenário), E5 (última nota do galho; "Veja também" não conta; falta fechamento de ciclo ou ponte para outro galho), L2 (referências sem URLs clicáveis — formato *modelcontextprotocol.io/spec* sem https://)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção ou parágrafo narrativo "O que vem a seguir" após "## Referências" fechando o ciclo do galho MCP (ex: "Você agora tem o mapa completo — do protocolo aos primitivos, do server local ao deploy em produção. O próximo passo natural é cruzar esse conhecimento com...") e apontando para galhos relacionados (ex: [[Agentes de Codificação]], [[Economia de Tokens]]) — ativa E5 e eleva score para 10/12
  - Adicionar URLs reais nas referências (ex: `https://modelcontextprotocol.io/spec`, `https://github.com/modelcontextprotocol/python-sdk`, `https://docs.anthropic.com/en/docs/agents-and-tools/mcp`, `https://github.com/modelcontextprotocol/inspector`) — ativa L2 e eleva score para 11/12
  - Opcional: adicionar parágrafo de abertura com cenário/problema antes de "## Stack recomendada" (ex: "Você tem um MCP server que funciona no Inspector local. Agora a pergunta é: como chegar de 'funciona no Inspector' para 'está em produção para toda a equipe'?") — ativa E2 e eleva score para 12/12

---

## 10. Segurança e Guardrails

> Galho **usa `fase: Iniciado`** (piso ≥300). Enriquecido 28/06. Checar conteúdo real.

### Notas

#### 01 - Código gerado por IA é untrusted
- **Estado:** 201 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Mermaid (1×), tabelas comparativas (CWEs, linguagens, junior vs LLM, tentativas falhas), casos práticos (Veracode 2025 data), armadilhas (3× [!warning] individuais), inglês + tabela PT↔EN, [!question]-, [!danger], [!info], wikilinks cross-galho (Dicionário de IA, Context Engineering)
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir conteúdo real até ≥300 linhas (faltam ~100): aprofundar "## A janela de risco" com exemplos reais de incidentes, expandir "## Onde a indústria está" com dados adicionais, ou adicionar seção "## Como montar um pipeline mínimo" — ativa o piso e ancora a nota como base da trilha
  - Adicionar URLs reais às referências (Veracode blog, BusinessWire, Help Net Security): trocar texto simples por `[Texto](URL)` — ativa L2 e eleva score para 11/12
#### 02 - Slopsquatting — o ataque via alucinação
- **Estado:** 251 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Mermaid (flowchart mecânica do ataque), casos práticos (react-codeshift jan/2026 + USENIX research), tabela comparativa (tipos de slopsquat × multiplicadores de escala), armadilhas (3× `[!warning]`), inglês completo + tabela PT↔EN (10 termos), `[!question]-` (typosquatting vs slopsquatting), `[!example]` (react-codeshift), `[!quote]` (USENIX + Claude CLI), código funcional (bash detecção + yaml allowlist + npm ci), wikilinks cross-galho (Dicionário de IA, nota 06 Permissões, nota 12 Roadmap)
- **Score verificar-nota (estimado):** 10/12 — falham P1 (sem código-com-falha explícito) e L2 (referências sem URLs clicáveis)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Nota está abaixo do piso Iniciado (251 < 300 linhas reais — faltam ~50): adicionar seção "## Impacto real — o que os estudos medem" expandindo os dados do USENIX (taxa de alucinação por modelo, % de repetição entre prompts similares) e/ou aprofundar "## Por que LLMs alucinam tanto pacote" com exemplos de conflation no dataset de treino — sobe piso sem diluir qualidade
  - Adicionar URLs reais às referências (Trend Micro, Socket.dev, Snyk, Aikido, Mend.io, USENIX, Cloudsmith têm páginas web rastreáveis) — ativa L2 e eleva score para 11/12
#### 03 - Alucinações em código — APIs fantasma e parâmetros inexistentes
- **Estado:** 283 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓ (sem URLs)
- **Opcionais presentes:** Mermaid, casos práticos (5 tipos com código-com-falha), inglês + tabela PT↔EN (10 termos), 3× [!warning], [!question]-, [!tip], tabelas comparativas (causas + camadas de validação + métricas + anti-patterns), wikilink cross-galho (Spec-Driven Development)
- **Score verificar-nota (estimado):** 10/12 — falham E2 (abertura-problema: nota vai do TL;DR direto para seções sem parágrafo de cenário) e L2 (referências nomeadas sem URLs clicáveis)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Nota está abaixo do piso Iniciado (283 < 300): adicionar parágrafo de abertura com cenário concreto antes de "## Os 5 tipos" (ex: "Você recebeu código gerado pela IA que parece impecável — compila, os testes passam — e só em produção você descobre que `response.json_safe()` nunca existiu na biblioteca") — ativa E2, sobe piso e eleva score para 11/12
  - Adicionar URLs reais às referências (Veracode 2025 GenAI Report, Trend Micro Slopsquatting post, OWASP LLM Top 10 site, Pydantic docs) — ativa L2 e eleva score para 12/12
#### 04 - A pirâmide de validação AI
- **Estado:** 250 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (flowchart pirâmide), YAML pipeline (CI workflow completo), tabelas comparativas (ferramentas × camada 1; guardrails × camada 2; falhas × sintomas × fix; métricas × alvo), 4× [!warning] individuais ("review fatigue", "camada 1 lenta", "LLM como validador", "SAST único vendor"), inglês completo + tabela PT↔EN (10 termos), [!question]- pedagógico (por que pirâmide ≠ checklist), casos práticos (100 PRs/semana → 2.000 revisões manuais; roadmap de 12 semanas), seção anti-patterns (6 itens), implementação progressiva semana-a-semana, Veja também, Referências
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir conteúdo real até ≥300 linhas (faltam ~50): adicionar seção "## Casos reais de falha na pirâmide" com 2-3 exemplos concretos de incidentes onde ausência de uma camada resultou em vazamento em produção, ou expandir "## Anti-patterns" com 2 padrões adicionais — sobe piso sem diluir qualidade
  - Adicionar URLs reais às referências (Veracode 2025 GenAI Report, DryRun Security site, NVIDIA blog, Anthropic engineering blog, OWASP LLM Top 10 site) — ativa L2 e eleva score para 11/12
#### 05 - SAST e SCA para código AI
- **Estado:** 291 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** [!question]- pedagógico, tabelas comparativas (SAST×SCA; tools; CWEs; métricas; pipeline), código funcional (Semgrep YAML, Snyk bash, CodeQL YAML, pipeline GitHub Actions completo), 3× [!warning] individuais, inglês + tabela PT↔EN (10 termos), casos práticos (slopsquat, regra dos 78%, AI-fix loop), [!tip] (Socket.dev), [!info] (AI-assisted remediation), L1 cross-galho (Spec-Driven Development)
- **Score verificar-nota (estimado):** 8/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com cenário/problema concreto antes da primeira seção (ex: "Você confiou no gerador de código e foi direto para produção — semanas depois o pentest encontrou SQL injection em 3 endpoints gerados pelo LLM, todos com parametrização esquecida") — ativa E2 e eleva score para 9/12 (passa gate); também expande o piso de linhas
  - Adicionar URLs reais às referências (DryRun Security blog, Veracode 2025 GenAI Code Security Report, Semgrep docs, Socket.dev site, OWASP LLM Top 10) — ativa L2 (núcleo ausente) e eleva score para 10/12
  - Adicionar 1 diagrama Mermaid (ex: flowchart do pipeline CI/CD SAST+SCA, ou graph TD árvore de decisão "qual ferramenta para qual camada") — ativa E3 e eleva score para 11/12; contribui para atingir piso de 300 linhas
#### 06 - Permissões e sandboxing
- **Estado:** 324 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (graph TB least privilege), tabelas comparativas (escopos, Layer 3, Git, setup por nível), casos práticos (banco wipado 9s, CVE-2026-25723 bypass 50 subcomandos), 3× `[!warning]` individuais, código funcional (JSON permissions, bwrap, YAML allowlist, bash subcommand), inglês + tabela PT↔EN (10 termos), `[!question]-` pedagógico, `[!danger]` (2×), `[!tip]`, `[!example]` checklist, dual-mode plan/agent, Veja também
- **Score verificar-nota (estimado):** 10/12 — falham P1 (sem código-com-falha explícito; exemplos de config OK mas sem snippet mostrando o erro resultante) · L2 (8 referências sem URLs clicáveis)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs reais às referências (Anthropic Claude Code docs, Truefoundry blog, Adversa AI CVE post, NVIDIA whitepaper, Docker docs, Startup Fortune article) — ativa L2 e eleva score para 11/12
  - Opcional: adicionar 1 snippet mostrando o que acontece quando a deny rule é contornada (ex: saída de bubblewrap com Permission denied ao tentar escrever em `~/.ssh/`) — ativa P1 e eleva score para 12/12
#### 07 - Security-focused prompting
- **Estado:** 306 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** inglês (seção "Como explicar em inglês"), tabela PT↔EN (10 termos), 3× [!warning], [!question]-, casos práticos (6 patterns com código), templates reusáveis, tabela comparativa (pré-LLM vs pós-LLM), seção Métricas, AGENTS.md embed
- **Score verificar-nota (estimado):** 8/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs reais nas referências (Veracode 2025 GenAI Code Security Report, Anthropic Best practices docs, OWASP LLM Top 10 2025, Augment Code docs, Microsoft Security blog) — ativa L2 e eleva score para 9/12 (passa o gate)
  - Adicionar parágrafo de abertura com problema/cenário concreto entre o TL;DR e `## O que NÃO funciona` (ex: PR chegando no code review com SQL concatenação apesar de o dev ter pedido "escreva código seguro" ao modelo) — ativa E2 e eleva score para 10/12
#### 08 - Code review de código AI — o que muda
- **Estado:** 285 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Mermaid (graph TB 3 camadas), tabela comparativa (review tradicional vs IA), casos práticos (routing config, métricas-alvo por tipo de PR), 4× `[!warning]` individuais (sinais de alerta, LGTM pattern, agente fez, merge after), inglês + tabela PT↔EN (10 termos), `[!question]-` pedagógico, checklist reutilizável, YAML routing, seção Métricas, Anti-patterns, Comprehension gate aplicado, Veja também
- **Score verificar-nota (estimado):** 10/12 — falham E2 (sem parágrafo de abertura com problema/cenário antes do TL;DR; nota abre direto no callout abstract) · L2 (5 referências sem URLs clicáveis)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura (2-3 frases) com cenário concreto antes do `> [!abstract]` (ex: PR enorme chegando ao tech lead às 18h — ele aprova sem ler porque o CI está verde; no dia seguinte, SQL injection em produção) — ativa E2 e eleva score para 11/12
  - Adicionar URLs reais às referências (Anthropic Best practices for Claude Code, GitHub AI code review post, Augment Code docs, Atlassian AI assistants blog, Plus8Soft Comprehension Gate post) — ativa L2 e eleva score para 12/12
  - As duas mudanças acima também ajudam a ultrapassar o piso de 300 linhas reais (atualmente 285)
#### 09 - Testes imutáveis — a barreira que o agente não pode reescrever
- **Estado:** 322 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (2×), casos práticos (múltiplos exemplos de código por tipo de teste), armadilhas (3× [!warning] individuais), inglês + tabela PT↔EN (10 termos), wikilink cross-galho ([[Spec-Driven Development|07 - Fase Validate...]])
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs reais às referências (Anthropic Best practices, Augment Code docs, Martin Fowler Spec by Example, GitHub Spec Kit) — ativa L2 e eleva score para 11/12
  - P1 (código-com-falha) é inaplicável para nota de prática/guardrail — não forçar
#### 10 - Métricas de qualidade AI — defect escape rate, rework ratio
- **Estado:** 281 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗ (referências sem URL — sem nenhum link externo clicável)
- **Opcionais presentes:** casos práticos (história dos dashboards + timeline semana a semana), [!warning] ×3 + [!danger] ×1, inglês + tabela PT↔EN (10 termos), [!question]- pedagógico, código bash (pseudo-script rework ratio), wikilinks cross-galho (Economia de Tokens, Dicionário de IA), Veja também
- **Score verificar-nota (estimado):** 10/12 (falham E3 Mermaid · P1 código-com-falha · L2 fonte com URL)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs reais às referências (ex: https://dora.dev, https://gitclear.com/content/ai_impact_on_code_quality, https://metr.org, Veracode State of Software Security) — fecha Fontes (núcleo) e ativa L2, elevando score para 11/12
  - Expandir nota para ≥300 linhas reais: adicionar Mermaid mostrando evolução temporal das 5 métricas (xychart ou timeline antes/depois de intervenção) — atinge o piso Iniciado e ativa E3, elevando score para 12/12
#### 11 - Governance as architecture — EU AI Act, GDPR, licenças
- **Estado:** 237 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Mermaid, tabela comparativa, casos práticos, 5× [!warning], código funcional (YAML CI), inglês + tabela PT↔EN, Veja também, [!question]-
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Piso: 237 linhas reais (63 abaixo do mínimo) — expandir "Para code generation especificamente" com cenários práticos de como preencher cada campo da tabela de auditoria, "High-risk AI systems" com exemplo de produto real que cai na categoria e o que o time teria que fazer, e "Para times brasileiros" com status do PL 2338/2023 e comparativo prático LGPD × GDPR × AI Act; meta: +65 linhas de conteúdo real
  - E1: TL;DR tem apenas 1 linha de conteúdo no callout (parágrafo único) — quebrar em ≥3 linhas distintas: (1) deadline e impacto imediato, (2) obrigações práticas para code generation (log de modelo/spec/revisão/diff), (3) consequência de não fazer (€35M / 7% de faturamento global)
  - L2: Referências sem URLs clicáveis — adicionar hyperlinks reais (ex: `https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai`, `https://artificialintelligenceact.eu`)
  - Caducidade regulatória: o prazo "2 agosto de 2026" vence em ~33 dias (a partir de 2026-06-30) — adicionar `[!warning]` de caducidade no bloco de datas-chave avisando que após 2026-08-02 a nota precisa ser atualizada para o modo "lei já aplicável" (status do enforcement, primeiras orientações/multas, comunicados da Comissão Europeia)
#### 12 - O roadmap de segurança para times
- **Estado:** ~316 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Mermaid (Gantt 12 semanas), tabelas comparativas (sinais de adoção/falha · adaptações por tamanho de time · manutenção pós-adoção), 4× [!warning] individuais, inglês + tabela PT↔EN (10 termos), wikilinks cross-galho (alucinações/prompting/testes/sandbox/métricas/governance), [!tip] inline, [!question]- pedagógico, código funcional (YAML CI + pre-commit)
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar URLs reais às 5 referências da seção "## Referências" (Veracode 2025 GenAI Report · DryRun Security SAST Tools 2026 · Anthropic Best Practices for Claude Code · NVIDIA Sandboxing Guidance · EUR-Lex EU AI Act) — ativa L2 (único item de núcleo faltante) e eleva score para 11/12

---

## 11. Memória de Agentes

> Galho **usa `fase: Iniciado`** em todas (piso ≥300). Enriquecido 28/06. Notas 10–19 são de implementações (caducidade). Checar conteúdo real.

### Notas

#### 01 - O que é memória em IA
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (3×), tabelas comparativas (linha do tempo do campo + dimensões de design), casos práticos (≥6 exemplos reais: ChatGPT Memory, Claude Projects, Letta, Mem0, LLM Wiki Pattern, A-MEM + exemplo concreto PostgreSQL), armadilhas 5× [!warning], inglês + tabela PT↔EN (12 termos), [!question]-, [!summary], callouts pedagógicos ([!info], [!note])
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir o TL;DR de 1 linha compacta para ≥3 linhas distintas — ativa E1 e eleva score para 11/12 (ex: separar em 3 linhas: o problema da amnésia nativa do LLM · o que é memória persistente e por que é o foco da trilha · o loop write-manage-read como padrão universal do campo)
  - P1 (código-com-falha) inaplicável para nota puramente conceitual — não forçar; score efetivo após TL;DR = 11/12
#### 02 - O problema das janelas de contexto
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 2× Mermaid (xychart curva U lost-in-the-middle + flowchart heurística contexto vs memória vs RAG), 5× [!warning] individuais (armadilhas 1-5), tabela comparativa (custo por turno; bom-para/ruim-para), inglês + tabela PT↔EN (11 termos), casos práticos (sessão 20 turnos ≈ $3,20; simulação 1.000 usuários/dia), wikilinks cross-galho (Dicionário de IA: Context window, KV cache, Token, attention, Prompt caching), [!question]- dúvidas, [!tip] (4 problemas estruturais), [!info] (GPT-5.5, break-even), [!note], [!summary], Veja também, Referências (8 fontes com URL)
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Converter a abertura de `## O que é` para iniciar com cenário/problema antes da definição — atualmente abre com "Janela de contexto é o número de tokens..." (padrão "X é..."); bastaria um parágrafo de 2-3 linhas antes (ex: "Você acabou de dar ao agente um histórico de 6 meses de projeto e ele esqueceu tudo na próxima chamada. Por quê?") para ativar E2 e elevar score para 11/12
  - P1 (código-com-falha) inaplicável para nota puramente conceitual — não forçar; score efetivo após abertura = 11/12
#### 03 - Taxonomia da memória (episódica, semântica, procedural)
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid (grafo taxonomia, diagrama agente de coding, flowchart decisão de substrato) · Tabela comparativa (4 tipos × 5 dimensões) · Casos práticos (agente de coding com os 3 tipos + análise de frameworks em 2026) · 5× [!warning] individuais · Como explicar em inglês + tabela PT↔EN (11 termos) · [!question]- · wikilinks cross-galho (Dicionário de IA, 18 Generative Agents, 19 A-MEM) · Veja também
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## O que é" — atualmente a seção abre com "A taxonomia clássica vem do psicólogo Endel Tulving..." (padrão "X é/vem de..."); bastam 2-3 linhas antes (ex: "Você tem três engenheiros discutindo 'memória do agente' e cada um fala de uma coisa diferente — chat history, knowledge base e CLAUDE.md. Todos têm razão; nenhum está falando do mesmo tipo de memória.") — ativa E2 e fecha o único item de núcleo faltante, elevando score para 11/12
  - P1 (código-com-falha) inaplicável para nota puramente conceitual — não forçar
#### 04 - RAG vs memória de longo prazo
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid, tabela comparativa (9 dimensões), 4× [!warning], casos práticos (≥2: analista SaaS + write-step), inglês + tabela PT↔EN (15 termos), pseudocódigo (write-step + manage-step), [!question]-, [!tip] (interview quote), resumo em 1 linha, Veja também
- **Score verificar-nota (estimado):** 11/12 — P1 (código-com-falha) inaplicável para nota conceitual/arquitetural
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 05 - Beyond RAG - quando RAG não basta
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (3×), casos práticos (≥2 por cenário), 5× [!warning], inglês + tabela PT↔EN (14 termos), wikilinks cross-galho, [!question]-, [!summary], [!tip], Veja também, referências com URLs completas
- **Score verificar-nota (estimado):** 11/12
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 06 - O LLM Wiki Pattern (gist do Karpathy)
- **Estado:** 300 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid, tabela comparativa RAG×LLM Wiki (11 dimensões), casos práticos (escala Karpathy ~400k palavras + exemplo de ingest passo-a-passo), 5× [!warning] (armadilhas com callouts individuais), inglês + tabela PT↔EN (17 termos), [!question]- (3 dúvidas/lacunas), [!summary] resumo de 3 parágrafos, [!tip] (2 callouts: compiler analogy + interview quote), wikilinks cross-galho (Dicionário de IA, RAG, implementações 10–13), Veja também, Referências com URLs completas
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com problema/cenário concreto antes de "## O que é" (a dor existe na nota — "Pesquisadores relatavam gastar 20–30% de cada sessão apenas re-explicando o que já havia sido discutido" — mas está enterrada na seção "## O contexto histórico"; trazê-la para o início como cenário-gancho ativa E2 e eleva score para 11/12)
#### 07 - Por que Obsidian e markdown como substrato
- **Estado:** 302 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (mindmap + stateDiagram-v2 + 2× graph LR), 5× [!warning] (armadilhas individuais), inglês + tabela PT↔EN (10 termos), casos práticos ([!example] trade-off + ciclo de vida da nota + naming convention), wikilinks cross-galho (Dicionário de IA, Karpathy), [!question]-, [!info], [!tip]
- **Score verificar-nota (estimado):** 10/12 — falham E2 (seção "## O que é" abre com "Substrato… é o formato físico" — padrão "X é") · P1 (inaplicável — nota conceitual)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## O que é" (ex: engenheiro que conectou um LLM a uma base de conhecimento em vector DB e percebeu que não conseguia abrir, revisar ou versionar o que o agente havia escrito) — ativa E2 e eleva score para 11/12
#### 08 - Arquitetura de um sistema de memória
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 5× Mermaid (pipeline de memória, quadrantChart write×read, graph LR mecanismos com custo, graph LR write-manage-read loop, tabela de frequência×operação), 5× [!warning] (4 armadilhas individuais + manutenção sem evaluation), [!example] checklist de arquitetura, [!tip] interview quote, [!question]- (2 lacunas), inglês + tabela PT↔EN (10 termos), casos práticos (5× nos 5 mecanismos), tabela comparativa (operação×frequência×custo), wikilinks cross-galho (RAG, Dicionário de IA, 9+ notas internas), Veja também, 3 fontes com URL (arxiv 2603.07670, gist Karpathy, arxiv 2304.03442)
- **Score verificar-nota (estimado):** 11/12 — P1 (código-com-falha: inaplicável para nota conceitual de arquitetura)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 09 - Panorama de implementações (abril 2026)
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** 3× Mermaid (famílias, fluxograma de escolha, espectro produção), tabela comparativa (síntese 12 implementações + família 1 detalhada), 4× [!warning] (armadilhas individuais), casos práticos (MemPalace vs Letta; cenários do fluxograma), inglês + PT↔EN (10 termos), [!question]- dúvidas de leitura, [!info] (nota sobre símbolos + LoCoMo), [!tip] (artefato vivo + interview quote), Veja também
- **Score verificar-nota (estimado):** 10/12 — E2 ✗ (abertura descritiva), P1 ✗ (inaplicável para nota-panorama)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Caducidade (⚠ panorama datado abril/2026): adicionar `[!warning]` de caducidade visível no topo do corpo (antes de `## O que é`) sinalizando que a tabela e o panorama são instantâneos de abril de 2026 — Armadilha 4 já menciona isso ao final, mas o aviso precisa aparecer logo ao abrir a nota para quem não lê até o fim
  - E2 Abertura-problema: `## O que é` abre de forma descritiva ("Esta nota é um mapa de mercado..."); adicionar parágrafo de entrada com cenário concreto (ex: desenvolvedor que se depara com uma dúzia de frameworks de memória e não sabe por onde começar) antes da descrição — ativa E2 e eleva score para 11/12
#### 10 - LLM-knowledge-base (Wendel) — direto do gist
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ (1 linha de conteúdo após o header, precisa ≥3) · Abertura-problema ✗ (seção "O que é" abre com "LLM-knowledge-base é...", não com cenário/problema) · Corpo-mecanismo ✓ · O que vem a seguir ✓ (ponte narrativa clara para nota 11 OpenKB) · Fontes ✓ (URLs no bloco de Referências)
- **Opcionais presentes:** Mermaid (4×: flowchart 4-stage, busca híbrida, claims lifecycle, tree ASCII), tabela comparativa (gist→módulos CLI), casos práticos (bash session completa, claims states, when-to-use/not-use), E6 inglês + E7 tabela PT↔EN (18 termos + frases de entrevista), E8 armadilhas (4× `[!warning]`: referência vs produto, KB_DATA_DIR, AGPL-3.0, lint sem schema), L1 wikilink cross-galho (RAG e Vector Databases, Dicionário de IA), caducidade sinalizada inline em prosa (seção Anatomia técnica, abril/2026)
- **Score verificar-nota (estimado):** 9/12 — falham E1 (TL;DR 1 linha), E2 (abertura-definição), P1 (sem código-com-falha; inaplicável para nota de referência)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E1 TL;DR: expandir para ≥3 linhas de conteúdo — separar em 3 sentenças ou bullets (conceito, mecanismo 4-stage, posicionamento como referência-não-SaaS) — eleva score para 10/12
  - E2 Abertura-problema: adicionar parágrafo de entrada com cenário concreto antes de "## O que é" (ex: "você leu o gist do Karpathy e quer ver o pattern em código executável — onde está a implementação de referência?") — ativa E2, eleva score para 11/12
  - Caducidade (⚠ detalhes de abril/2026): promover o aviso inline da seção "## Anatomia técnica" para um callout `[!warning]` ou `[!info]` visível logo no topo dessa seção (311 testes, cobertura por módulo, versão do stack podem ter mudado)
#### 11 - OpenKB — wiki compilada com PageIndex
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid, Casos práticos, Armadilhas (4× [!warning]), Inglês + tabela PT↔EN, Veja também, [!question]-, Tabelas comparativas
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E2 Abertura-problema: reescrever abertura de "## O que é" para abrir com problema/cenário concreto em vez de "OpenKB se apresenta como..." — eleva score para 11/12
  - Caducidade (⚠ criado 2026-05-06, versão `openkb 0.1.3` alpha): verificar se o pacote avançou além da 0.1.3, atualizar versões e roadmap listados na seção "## Anatomia técnica" se necessário
#### 12 - graphify — knowledge graph de raw
- **Estado:** 308 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid, tabela comparativa (markdown vs KG), casos práticos (bash + MCP + entrevista), armadilhas ×3 [!warning], código de uso correto (não de falha), inglês + tabela PT↔EN, [!question]- dúvidas, [!tip] interview quote, Veja também
- **Score verificar-nota (estimado):** 9/12 — E1 TL;DR ✗ (2 linhas físicas, não ≥3) · E2 abertura-problema ✗ ("graphify é uma versão..." = X é Y) · P1 código-com-falha ✗
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E1 TL;DR: expandir o callout `[!abstract]` para ≥3 linhas físicas — sugestão: separar em 3 parágrafos (o que é / diferencial do substrato gráfico / saídas + cuidados)
  - E2 Abertura-problema: reescrever abertura de "## O que é" para abrir com cenário/problema — ex. "Você tem uma pasta `/raw` com código, papers, vídeos e screenshots misturados. Como o assistente de código encontra o que importa sem ler tudo?" — em vez de "graphify é uma versão…"
  - ⚠ Caducidade: nota criada e atualizada em 2026-04-26 (repo ativo, branch `v5`); verificar se versão, linguagens suportadas (~25) e integração de IDEs listadas na "## Anatomia técnica" ainda batem com o README atual antes de citar em decisão técnica
#### 13 - basic-memory — MCP nativo Obsidian
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (graph LR), Tabela PT↔EN (10 itens), Casos práticos (3 padrões + [!example]), [!warning] x4, Código com exemplo (não com falha), Inglês + Interview quote ([!tip]), Veja também, [!question]-, [!info] x2
- **Score verificar-nota (estimado):** 10/12 (E1✓ E2✗ E3✓ E4✓ E5✓ E6✓ E7✓ E8✓ P1✗ P2✓ L1✓ L2✓)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E2 Abertura-problema: reescrever o primeiro parágrafo de "## O que é" para abrir com cenário/problema — ex.: "Você quer que seu assistente de IA lembre de decisões de projetos entre sessões sem repassar contexto toda vez. O desafio: a memória precisa ser legível por humanos, portátil e sem lock-in. `basic-memory` resolve isso..." — em vez de "`basic-memory` é um servidor MCP que..."
  - ⚠ Caducidade: nota criada e atualizada em 2026-04-26 (2 meses atrás); verificar contagem de estrelas (anotada como 2.929 em abril/2026), versão atual (última mencionada: v0.19.x), novas tools MCP ou mudanças na Cloud antes de citar em decisão técnica
#### 14 - Letta (ex-MemGPT)
- **Estado:** 228 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (2 diagramas) · Casos práticos (2) · Armadilhas (7 [!warning]) · Inglês + tabela PT↔EN · Checklist de adoção · Veja também · [!question]-
- **Score verificar-nota (estimado):** 10/12 (falha E2 abertura-problema; falha P1 código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Piso: nota tem 228 linhas reais; faltam ~72 para atingir o piso de Iniciado (300). Expandir seções existentes ou adicionar nova seção (ex.: "Comparação Letta vs self-host tradicional" ou aprofundar sleep-time agents com exemplo de código).
  - E2 Abertura-problema: "## O que é" abre com "Letta é um framework..." — padrão "X é...". Reescrever para abrir com o problema ("Seu agent precisa lembrar decisões de semanas atrás sem que o desenvolvedor escreva heurísticas de retenção — como transferir essa responsabilidade para o próprio modelo?").
  - ⚠ Caducidade (implementação): note menciona modelos `Opus 4.5` e `GPT-5.2` como recomendações de abril/2026, pricing com tiers específicos, e estrelas no GitHub ("mais de 22 mil em abril/2026"). A nota tem `updated: 2026-06-28` mas vários dados internos continuam datados de abril/2026 — verificar leaderboard de modelos, pricing atual e contagem de estrelas antes de citar em decisão técnica.
#### 15 - Mem0 — vetorial + grafo
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa — por 1 linha) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (2 diagramas) · Tabela comparativa (2) · Casos práticos (4: saúde, código, suporte, pesquisa) · Armadilhas (7× [!warning]) · Código Python (3 blocos) · Inglês + tabela PT↔EN · Veja também · [!question]- · [!info]
- **Score verificar-nota (estimado):** 10/12 (faltam E2 abertura-problema e P1 código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - E2 Abertura-problema: "## O que é" abre com "`mem0` é um framework para..." — padrão "X é...". Reescrever para abrir com o problema ("Seu agent acumula 10 sessões de conversa e, na 11ª, esquece que o usuário pediu respostas curtas — porque a janela estourou. Como extrair automaticamente só o que importa e recuperar na hora certa?").
  - P1 Código-com-falha: adicionar exemplo concreto de uso incorreto com consequência — ex. chamar `memory.add` sem tratar o custo de extração em produção de alto volume, ou confiar no output de `memory.search` sem verificar `user_id` correto.
  - ⚠ Caducidade (implementação): dados de abril/2026 (54k stars no GitHub, pricing com tiers específicos, ~24 integrações, score LongMemEval 93,4% auto-reportado, remoção do graph store externo). A nota tem `updated: 2026-06-28`, mas os dados internos continuam datados de abril/2026 — verificar changelog do SDK, pricing atual e estado do graph store externo antes de citar em decisão técnica.
#### 16 - Zep e Graphiti — knowledge graph temporal
- **Estado:** 317 linhas totais (sem blanks no fim; piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (×2) · Tabela comparativa (×2) · Casos práticos (CRM João + config FalkorDB) · Armadilhas ([!warning] ×6) · Inglês + tabela PT↔EN · [!question]- · [!tip] interview quote
- **Score verificar-nota (estimado):** 10/12 (faltam E2 abertura-problema, P1 código-com-falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - ⚠ Caducidade (implementação): seção "Anatomia técnica" declara "verificado em abril de 2026" — versões de backends (Neo4j 5.26+, FalkorDB 1.1.2, Kuzu 0.11.2), pricing Zep Cloud e estado do MCP server podem ter mudado; verificar changelog antes de citar em decisão técnica.
  - Opcional E2: abertura da seção "O que é" abre com "Graphiti é um framework…" (estilo definitional); converter para cenário-problema seria melhoria de leitura, mas não bloqueia aprovação.
  - Opcional P1: adicionar exemplo de uso incorreto com consequência (ex.: omitir `reference_time` e perder o benefício bi-temporal, ou alimentar texto sem timestamps e receber apenas ingestion time).
#### 17 - MemPalace (Milla Jovovich)
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (×2), tabela comparativa, casos práticos (Quando usar/não usar), armadilhas [!warning] (×6), inglês + tabela PT↔EN, Veja também, [!question]-, [!tip]
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - ⚠ Caducidade (implementação): nota trata de projeto lançado em abril/2026 com "breaking changes esperáveis" e discrepância 29 vs 20 MCP tools documentada; agora é junho/2026 — verificar changelog oficial e auditoria `lhl/agentic-memory` antes de citar estado técnico em decisão real.
  - Opcional E2: seção "O que é" abre com "MemPalace é um sistema de memória persistente…" (estilo definitional); converter para cenário-problema (ex.: "Você precisa que o agent lembre da decisão de ontem sem mandar o histórico inteiro no prompt…") seria melhoria de leitura; não bloqueia aprovação.
  - Opcional P1: adicionar exemplo de uso com falha concreta (ex.: habilitar AAAK sem ler o 12,4pp drop e ser surpreendido pela degradação, ou comparar 170-token startup com custo end-to-end de outro framework — categoria errada).

#### 18 - Generative Agents (Park, Stanford 2023)
- **Estado:** 301 linhas totais (sem vazias no fim) (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (múltiplos diagramas), Tabela comparativa, Casos práticos, 4× [!warning] armadilhas, Inglês + tabela PT↔EN, [!question]-, [!tip] interview quote, Veja também, wikilinks cross-galho
- **Score verificar-nota (estimado):** 11/12 (falta P1 — código com falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 19 - A-MEM — Zettelkasten dinâmico
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (3 diagramas) · Tabela comparativa (3 tabelas) · Casos práticos (cenário Memória A→B) · Armadilhas (4 [!warning]) · Inglês + tabela PT↔EN · [!question]- · [!tip] interview quote
- **Score verificar-nota (estimado):** 11/12 — ausente: P1 código-com-falha
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 20 - Surveys e estado da arte 2026
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ (1 linha no callout, precisa ≥3) · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (5 mecanismos), tabela comparativa (agent memory × LLM memorization + benchmarks), casos práticos por mecanismo, 3×[!warning], inglês (seção + framing de entrevista), tabela PT↔EN, [!question]-, 2×[!tip]
- **Score verificar-nota (estimado):** 10/12 (falha em E1 TL;DR e P1 código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir o `[!abstract]` TL;DR de 1 para ≥3 linhas distintas (ponto 1: maturidade institucional com MemAgents; ponto 2: cinco mecanismos como consenso; ponto 3: distinção agent memory × LLM memorization)
  - Sinalizar caducidade: a seção "ICLR 2026 Workshop MemAgents" usa futuro ("Acontece em 27 de abril de 2026") mas o evento já ocorreu (hoje: 2026-06-30); reescrever no passado e, se disponíveis, adicionar referência a papers ou talks publicados pós-evento
#### 21 - Comparativo crítico (LongMemEval)
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (quadrantChart), Tabela comparativa, Casos práticos (6 perfis), Armadilhas (5 [!warning]), PT↔EN, Veja também, [!question]-
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Reformular a abertura da seção "O que é o LongMemEval": o primeiro parágrafo começa com "[LongMemEval] é um benchmark..." (padrão "X é..."); substituir por um cenário-problema ("Imagine precisar comparar sistemas de memória sem saber se os números do marketing são comparáveis...") antes da definição formal
#### 22 - Críticas, limitações e armadilhas
- **Estado:** 300 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Armadilhas (7× [!warning]) · Casos práticos (MemPalace, AAAK, Mem0g, Letta, Zep…) · Inglês + tabela PT↔EN · [!question]- · Tabela comparativa (Direito ao esquecimento por framework) · Checklist consolidado
- **Score verificar-nota (estimado):** 9/12 (E1✓ E2✗ E3✗ E4✓ E5✓ E6✓ E7✓ E8✓ P1✗ P2✓ L1✓ L2✓)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Reformular abertura da seção "O que é": abre com "Esta nota é uma análise crítica…" (padrão "X é…" / meta-descrição). Substituir pelo cenário-problema — ex.: "Você acabou de ver um score de 96,6% num benchmark e está prestes a citar em entrevista. O paper crítico que aponta que o número vem de armazenamento verbatim + ChromaDB default — não da inovação anunciada — está na sua fila de leitura. Esta nota é o que acontece quando você lê esse paper antes de falar." — e só então a descrição do que a nota faz.
#### 23 - Guia de implementação do zero
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** [!question]- dúvidas · 5× [!warning] armadilhas · [!tip] com tabela PT↔EN e interview quotes · seção "Como explicar em inglês" · checklist de "pronto para produção"
- **Score verificar-nota (estimado):** 10/12 (faltam E3 Mermaid e P1 código-com-falha, ambos opcionais)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 24 - Aplicações comerciais e modelo de negócio
- **Estado:** 300 linhas reais (piso Iniciado ≥300: passa, na margem) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Tabela comparativa (3×) · Casos práticos · Armadilhas (5 [!warning]) · Inglês + tabela PT↔EN · [!question]- · [!tip] Interview quote · Veja também
- **Score verificar-nota (estimado):** 8/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar ≥1 URL externa real nas Referências (L2 falha): citar URL de produto digital comparável (ex: Nick Milo LYT Kit em Gumroad ou página pública do livro de Forte) — move o score para 9/12
  - Refatorar abertura da seção "O que é": mover a dor central ("Conhecimento técnico sem caminho de monetização vira hobby") para o primeiro parágrafo, antes da descrição dos três modelos — a abertura atual é expositiva, não problema-primeiro (E2 falha)
  - Caducidade: preços, faixas e análise de amadurecimento de mercado são de 2026 — inserir nota de revisão periódica (sugerido: revisitar a cada 12 meses ou quando houver mudança relevante no ecossistema PKM + IA)

---

## 12. Prompt Engineering

> Galho **usa `fase: Iniciado`** (piso ≥300). Enriquecido 28/06. Checar conteúdo real.

### Notas

#### 01 - Por que prompt engineering ainda importa
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Tabela comparativa, [!warning] ×3, inglês + tabela PT↔EN, [!question]-, [!tip], Veja também, wikilinks cross-galho
- **Score verificar-nota (estimado):** 10/12 (ausentes: E3 Mermaid, P1 código-com-falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 02 - Especificidade — a primeira disciplina
- **Estado:** 304 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (before/after + por tipo de tarefa), 3 [!warning], código-com-falha (prompt vago), inglês + tabela PT↔EN, [!question]-, wikilinks cross-galho (Anatomia dos LLMs, Structured Outputs), fonte externa com URL (arxiv:2406.06608)
- **Score verificar-nota (estimado):** 11/12 (falta Mermaid)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 03 - Roles e personas — escolhendo o juízo do modelo
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (tabela + 2 exemplos preenchidos) · armadilhas 3×[!warning] · inglês + tabela PT↔EN · [!question]- · [!tip] checklist · wikilink cross-galho (AI Engineering Stack) · fonte externa com URL (arxiv:2406.06608)
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir TL;DR de 1 parágrafo/linha para ≥3 linhas `>` distintas dentro do callout [!abstract] (E1 ✗)
#### 04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy
- **Estado:** 171 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (Quando usar/NÃO usar + diálogos) · armadilhas 3×[!warning] · inglês + tabela PT↔EN · [!question]- · wikilink cross-galho ([[Andrej Karpathy]])
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir corpo para atingir ≥300 linhas de conteúdo real (atual: 171; faltam ~130 linhas): aprofundar seção de mecanismo RLHF, adicionar Mermaid de "caminhos de fuga × cláusulas", expandir exemplos práticos ou adicionar seção de variante domain-specific com case concreto
  - Expandir TL;DR de 1 linha para ≥3 linhas `>` distintas dentro do callout [!abstract] (E1 ✗)
#### 05 - Few-shot examples — exemplos como contrato
- **Estado:** 211 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling / in_progress
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos ✓ · armadilhas 3× [!warning] ✓ · código-com-falha ✓ · inglês ✓ · PT↔EN ✓ · wikilink cross-galho ✓ · fonte externa com URL ✓
- **Score verificar-nota (estimado):** 11/12 (falta apenas E3 Mermaid)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir conteúdo real de 211 → ≥300 linhas: adicionar diagrama Mermaid do fluxo de decisão (zero-shot → few-shot → fine-tuning) ou expandir seção "Como escolher exemplos" com case concreto end-to-end (resolve E3 e sobe contagem)
#### 06 - Constraints declarativas — boundaries como engenharia
- **Estado:** 294 linhas reais (piso Iniciado ≥300: não passa — faltam 6 linhas) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Mermaid ✗ · Tabela comparativa ✓ · Casos práticos ✓ · Armadilhas [!warning] ✓ (3) · Código-com-falha ✓ (RUIM/BOM) · Inglês ✓ · Tabela PT↔EN ✓ · Veja também ✓ · [!question]- ✓ · [!tip] ✓
- **Score verificar-nota (estimado):** 10/12 (falta E2 abertura-problema e L2 fonte externa com URL)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Converter fontes para links markdown com URL completo (ex: `[Anthropic — Provide system prompts](https://docs.anthropic.com/...)`) — resolve L2 e adiciona ≥2 linhas
  - Adicionar abertura-problema antes de "O que é uma constraint declarativa": 2-3 linhas descrevendo a frustração concreta ("você diz 'seja conciso' e o modelo escreve cinco parágrafos") — resolve E2 e empurra sobre o piso 300
#### 07 - Iteration patterns — keep, change, do-not
- **Estado:** 297 linhas reais (piso Iniciado ≥300: não — 3 linhas abaixo) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗
- **Opcionais presentes:** Mermaid ✗ · Casos práticos ✓ (code review / schema / plano de projeto) · 3× [!warning] ✓ · Código-com-falha ✓ (bloco "RUIM") · Inglês + PT↔EN ✓ · [!question]- ✓ · [!tip] ✓
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Converter fontes para links markdown com URL completo (ex: `[Anthropic — Iterating on prompts](https://docs.anthropic.com/...)`) — resolve L2
  - Expandir TL;DR de 1 para 3 linhas explícitas (cada ponto em linha própria) ou adicionar 3 linhas de conteúdo em qualquer seção — empurra sobre o piso 300
#### 08 - Reasoning models — audit trail, não chain-of-thought
- **Estado:** 201 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** tabela comparativa, casos práticos, 3× [!warning], seção inglês, tabela PT↔EN, código API (Claude + o3), checklist, wikilinks cross-galho
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir conteúdo em ~100 linhas reais para atingir piso Iniciado ≥300 (prioridade máxima)
  - Expandir TL;DR de 1 parágrafo corrido para ≥3 linhas explícitas (bullets ou linhas separadas) — resolve E1
  - Adicionar pelo menos 1 caso prático com prompt incorreto vs. correto (exemplo trabalhado) — contribui pro piso e reforça E4
#### 09 - Anti-patterns e tells de IA — o que evitar
- **Estado:** 184 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling / in_progress
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ (2 linhas no arquivo; precisa ≥3) · Abertura-problema ✗ (entra direto em H2 sem abertura) · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✗ (domínio sem URL markdown clicável)
- **Opcionais presentes:** Tabela comparativa (quando os padrões são OK) · Bloco de código (template Do-not) · [!warning] ×3 · [!question]- · Inglês passagem · Tabela PT↔EN · Veja também
- **Score verificar-nota (estimado):** 7/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir nota para ≥300 linhas de conteúdo real (faltam ~116 linhas): adicionar 2 casos práticos trabalhados — prompt original com tell vs. reescrita sem tell (reforça E4 e cobre P1)
  - Expandir TL;DR para ≥3 linhas de arquivo (atualmente 1 parágrafo compacto numa única linha)
  - Adicionar abertura-problema antes do primeiro H2 — cenário concreto (ex.: "você recebe um draft e percebe que parece ChatGPT")
  - Corrigir L2: substituir `(docs.anthropic.com)` por URL markdown completo `[Style guidelines](https://docs.anthropic.com/...)` e verificar se @hooeem tem link disponível

---

## 13. Structured Outputs

> Galho **usa `fase: Iniciado`** (piso ≥300). Enriquecido 28/06. Notas de API (caducidade). Checar conteúdo real.

### Notas

#### 01 - O problema do output não estruturado
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling / in_progress
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (tabela de cenários + exemplo de fatura com 5 problemas), armadilhas (3 [!warning]), código-com-falha (parser defensivo Python), inglês (seção + tabela PT↔EN), wikilink cross-galho (AI Engineering Stack), checklist antes de seguir, [!question]- pré-requisitos
- **Score verificar-nota (estimado):** 11/12 — falta apenas Mermaid (E3)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma (opcional: adicionar diagrama Mermaid da taxonomia de falhas ou do pipeline texto→schema→semântica)
#### 02 - JSON Schema como contrato
- **Estado:** 241 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** [!question]- · [!warning] ×3 · Tabela comparativa (provider limits) · Casos práticos (schema canônico @hooeem + patterns) · Inglês + tabela PT↔EN · Veja também · wikilink cross-galho (Dicionário de IA)
- **Score verificar-nota (estimado):** 9/12 (E1✓ E2✗ E3✗ E4✓ E5✓ E6✓ E7✓ E8✓ P1✗ P2✓ L1✓ L2✓)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Aumentar volume: 241 linhas reais ficam ~60 abaixo do piso Iniciado (300); expandir com exemplo de schema inválido (P1 código-com-falha) ou adicionar seção de caso prático end-to-end (classificação de bug ou extração de entidade) — ganha piso e P1 simultaneamente
  - Corrigir abertura-problema: seção "JSON Schema 101" abre com "JSON Schema é uma especificação…" (padrão "X é…"); reescrever para começar com o cenário que motiva o schema antes da definição formal
#### 03 - Function calling como mecanismo de output
- **Estado:** 215 linhas reais (300 total − 85 em branco; piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos Pattern A/B · 3× [!warning] · inglês + tabela PT↔EN · [!question]- · checklist de implementação · diagnóstico de falha · wikilinks cross-galho (Anatomia de Agents, MCP, loop ReAct)
- **Score verificar-nota (estimado):** 10/12 (ausentes: E3 Mermaid, P1 código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir para ≥300 linhas reais: adicionar diagrama Mermaid do fluxo (prompt → tool definition → provider validation → tool_use block → output) — resolve E3 e soma ~15 linhas reais
  - Adicionar exemplo P1 de código-com-falha: trecho sem `tool_choice` forçado mostrando que o modelo responde em texto livre e o parse falha — resolve P1 e soma ~15-20 linhas reais; junto com o Mermaid empurra para ~245 e ainda falta mais; considerar expandir "A anatomia" com diagrama de sequência ou adicionar caso end-to-end (extração de invoice) que acrescente ~40-50 linhas de conteúdo denso
#### 04 - OpenAI Structured Outputs — strict mode
- **Estado:** 302 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (3 formas: response_format / parse() / tools) · armadilhas (3 [!warning]) · inglês + tabela PT↔EN · wikilink cross-galho (nota 19 Anatomia dos LLMs) · tabela comparativa (response_format vs tools)
- **Score verificar-nota (estimado):** 10/12 (faltam E3 Mermaid · P1 código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - ⚠️ CADUCIDADE — nota de API: modelos listados (gpt-4.1, gpt-5, gpt-5-mini, gpt-5-thinking, o3, o4) e limites numéricos (100 props, 5 níveis, 500 enum values, 15000 chars) mudam com frequência; verificar contra docs OpenAI atuais antes de enriquecer
  - Adicionar diagrama Mermaid do fluxo de constrained decoding (schema → grammar → decoder → token válido → output) — resolve E3 (~15 linhas)
  - Adicionar exemplo P1 de código-com-falha: trecho com `strict: false` ou sem `additionalProperties: false` em objeto aninhado, mostrando o erro de schema que o SDK rejeita — resolve P1 (~15-20 linhas)
#### 05 - Anthropic tool use para forçar formato
- **Estado:** 311 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (Python + TypeScript + cenários when-to-use), armadilhas (3× [!warning]), inglês + tabela PT↔EN, [!question]- prereqs, Veja também, wikilinks cross-galho (Anatomia dos LLMs + Anatomia de Agents)
- **Score verificar-nota (estimado):** 10/12 (faltam E3 Mermaid e P1 código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - CADUCIDADE: a afirmação central "Anthropic não tem API dedicada de structured output" pode estar desatualizada — Anthropic lançou suporte nativo a structured outputs (beta) em 2025; verificar se a nota deve absorver esse novo caminho ou restringir escopo ao mecanismo de tool use explicitamente
  - Adicionar diagrama Mermaid do fluxo (tool_choice forçado → bloco tool_use → extração input → validação) — resolve E3 (~12-15 linhas)
  - Adicionar P1: snippet curto mostrando falha real (ex: sem `tool_choice` explícito, resposta em texto livre; ou `stop_reason == "max_length"` com bloco incompleto) — resolve P1 (~10-15 linhas)
#### 06 - Gemini structured output
- **Estado:** 229 linhas reais (piso Iniciado ≥300: **não passa**) · fase: Iniciado · status: seedling / in_progress · ⚠️ Nota de API — google-genai SDK e linha Gemini 2.x evoluem rápido; revisar compatibilidade a cada trimestre
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** E4 casos práticos (4 exemplos de código) · E6 inglês · E7 tabela PT↔EN · E8 armadilhas (3 [!warning]) · [!question]- pré-leitura
- **Score verificar-nota (estimado):** 8/12 (E2 abertura-problema ✗ · E3 Mermaid ✗ · P1 código-com-falha ✗ · L1 wikilink cross-galho ✗)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com problema/cenário antes de "## O mecanismo" (ex.: "Você vem da OpenAI e quer trocar de provider — o schema que funcionava não roda no Gemini porque os tipos estão em caixa alta. Por quê?") — resolve E2, adiciona ~12 linhas
  - Adicionar diagrama Mermaid do fluxo: `GenerateContentConfig` (response_mime_type + response_schema) → SDK → `response.parsed` (Pydantic) / `response.text` (fallback) — resolve E3, adiciona ~14 linhas
  - Adicionar snippet de código-com-falha: schema com tipos em caixa baixa (`"type": "object"`) gerando `response.parsed == None` e `response.text` com shape incorreto; ao lado, a versão corrigida com `"OBJECT"` — resolve P1, adiciona ~15 linhas
  - Adicionar ao menos um wikilink cross-galho (ex.: para nota de Fundamentos sobre APIs ou para o galho Anatomia dos LLMs) — resolve L1
  - As adições acima somam ~41 linhas de conteúdo real, elevando para ~270 — ainda abaixo de 300; considerar expandir seção "Boas práticas" com exemplo de `model_config = ConfigDict(extra="forbid")` em Pydantic (~15 linhas) para atingir o piso
#### 07 - Validação e retry — Pydantic, Zod
- **Estado:** 277 linhas reais (piso Iniciado ≥300: não) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Tabela comparativa · Casos práticos · 3 × [!warning] · Código Python e TS · Inglês + tabela PT↔EN · [!question]- · Veja também
- **Score verificar-nota (estimado):** 10/12 (falta: E3 Mermaid · P1 Código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir a seção "Boas práticas" com exemplo de `model_config = ConfigDict(extra="forbid")` para rejeitar campos extras e um parágrafo sobre validar o schema em ambiente de desenvolvimento (~20–25 linhas) — eleva o conteúdo real para ≥300 e fecha o piso Iniciado
#### 08 - Streaming de structured outputs
- **Estado:** ~230 linhas reais (piso Iniciado ≥300: não passa — total com brancos 303, mas reais ~230) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Casos práticos (seção "Quando faz sentido", 6+ cenários) · 3× [!warning] armadilhas · Inglês (parágrafo entrevista) · Tabela PT↔EN (10 termos) · [!question]- pré-requisitos · Wikilinks cross-galho (Anatomia dos LLMs, AI Engineering Stack) · Tabela comparativa (validação em streaming)
- **Score verificar-nota (estimado):** 10/12 (faltam E3 Mermaid e P1 código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar diagrama Mermaid de fluxo de decisão entre os 3 caminhos (Caminho 1 → Caminho 2 → Caminho 3), ~15–20 linhas — fecha E3 e eleva linhas reais
  - Adicionar snippet de código-com-falha na seção "Armadilhas comuns" (ex.: chamada ingênua a `JSON.parse(chunk)` sem buffer, mostrando o erro), ~10–15 linhas — fecha P1
  - As duas mudanças juntas elevam o conteúdo real para ≥270–280; considerar expandir 1 parágrafo em "Validação em streaming" para cruzar ≥300

---

## 14. Evaluation

> Galho **usa `fase: Iniciado`** (piso ≥300). Enriquecido 28/06. Checar conteúdo real.

### Notas

#### 01 - Eval-driven development — a disciplina
- **Estado:** ~302 linhas totais / ~230 não-brancas (piso Iniciado ≥300: não — passa em total, não em conteúdo real) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ (1 linha longa — borderline ≥3) · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** tabela TDD↔EDD, PT↔EN, casos práticos (≥3), 3×[!warning], [!tip], [!question]-, inglês
- **Score verificar-nota (estimado):** 10/12 (E3 Mermaid ✗ · P1 código-com-falha ✗)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar diagrama Mermaid do fluxo EDD (antes→depois, ou ciclo eval/prompt/baseline) para suprir E3 e adensar a nota visualmente
  - Expandir 2-3 seções existentes (ex.: "Maturidade EDD" com exemplos concretos por nível, ou "EDD em times" com mini-caso) para cruzar o piso de ~300 linhas de conteúdo não-branco
  - Expandir TL;DR para ≥3 linhas explícitas no callout (atualmente 1 linha muito longa)
#### 02 - Golden datasets — como construir
- **Estado:** 284 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ (1 linha longa, não ≥3) · Abertura-problema ✗ (primeira seção abre "Estrutura mínima:" — definitional) · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** tabelas comparativas · casos práticos (YAML ×3) · armadilhas [!warning] ×3 · inglês + tabela PT↔EN · [!question]- · [!tip] · wikilinks cross-galho
- **Score verificar-nota (estimado):** 8/12 (E1✗ E2✗ E3✗ E4✓ E5✓ E6✓ E7✓ E8✓ P1✗ P2✓ L1✓ L2✓)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir TL;DR para ≥3 linhas explícitas no callout (atualmente 1 linha muito longa — resolve E1)
  - Adicionar parágrafo de abertura-problema antes de "## O que é um golden set": descrever a dor concreta (como "o prompt melhorou… ou será que piorou?") que motiva o golden set — resolve E2 e adiciona linhas
  - As duas ações acima somadas devem empurrar a nota para ≥300 linhas de conteúdo e elevar o score para ≥9/12
#### 03 - Scoring rubrics e critérios
- **Estado:** 324 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** tabela comparativa, casos práticos, armadilhas (3 [!warning]), inglês + tabela PT↔EN, Veja também, [!question]-
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir o callout `[!abstract]` TL;DR para ≥3 linhas markdown de corpo (atualmente é 1 parágrafo numa única linha — resolve E1 e eleva score para 10/12)
#### 04 - LLM-as-judge — quando e como
- **Estado:** 333 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** código (anatomia mínima + pseudo-casos de viés), casos práticos (LMSYS Chatbot Arena), [!warning] ×3, inglês + tabela PT↔EN, [!question]-, wikilinks cross-galho (Anatomia dos LLMs, RAG)
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura narrativo (2-3 linhas) entre o título e a seção "Quando faz sentido" — apresentar o problema concreto (o gargalo de eval subjetivo em escala: humano não revisa mil outputs por iteração) antes de entrar nas listas; elimina a entrada abrupta em "Aplica:" e resolve E2
#### 05 - Regression testing em LLMs
- **Estado:** 317 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** [!question]-, tabela comparativa (string diff vs semantic diff), tabela de calibração de threshold, casos práticos (2: cenário de sprint + bug de prod), [!warning] x3, código-com-falha (string diff equivocado + pseudocode Python + bash de rebless), inglês + tabela PT↔EN, Veja também
- **Score verificar-nota (estimado):** 11/12 (falta: Mermaid)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 06 - Frameworks 2026 — Promptfoo, Braintrust, Langfuse, Patronus, Phoenix
- **Estado:** 439 linhas totais / ~240 não-vazias (piso Iniciado ≥300: passa — sem trailing blanks) · fase: Iniciado · status: seedling / in_progress
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid (2 diagramas), Tabela comparativa (2), Casos práticos (6 snippets de código, um por framework), 3× [!warning], Inglês + tabela PT↔EN, [!question]-, Decision tree em bloco de código
- **Score verificar-nota (estimado):** 10/12 (E2 abertura-problema ✗, P1 código-com-falha ✗)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - Melhoria opcional (E2): adicionar parágrafo de abertura antes de "## A taxonomia dos cinco" enquadrando o problema ("O mercado de eval explodiu — como escolher entre tantos frameworks?"), evitando salto abrupto do TL;DR para a taxonomia
  - Caducidade: nenhuma identificada — frameworks citados (Promptfoo, Langfuse, Braintrust, Patronus, Phoenix) e modelos nos snippets (claude-sonnet-4-6, gpt-5) estão ativos em 2026-06; artigo de Hamel Husain "2024+" compatível
#### 07 - Eval em CI-CD
- **Estado:** ~365 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (YAML completo, cálculo de custo, quarentena), armadilhas (3× [!warning]), inglês + tabela PT↔EN, wikilink cross-galho (Anatomia dos LLMs/19)
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 08 - Eval por contexto — LLM, RAG, agent, prompt
- **Estado:** ~276 linhas de conteúdo real pós-frontmatter (piso Iniciado ≥300: borderline/passa — 326 linhas de corpo, ~50 blanks internos) · fase: Iniciado · status: growing
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Tabela comparativa · Casos práticos (≥2) · Armadilhas (3× [!warning]) · [!example] · [!caution] · Inglês · PT↔EN · Veja também · [!question]-
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma

---

## 15. Observability

> Galho **usa `fase: Iniciado`** (piso ≥300). Enriquecido 28/06. Notas de ferramentas (caducidade). Checar conteúdo real.

### Notas

#### 01 - Por que LLMs precisam de observabilidade
- **Estado:** 302 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** tabelas comparativas, casos práticos, 3× [!warning], código Python (mínimo viável), inglês + tabela PT↔EN, [!question]-, [!tip] checklist, tabela de maturidade, tabela de sampling
- **Score verificar-nota (estimado):** 10/12 (falta E3 Mermaid; P1 código-com-falha — o código Python existente é funcional, não um exemplo de falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Remover a segunda seção `## Veja também` duplicada (linhas 296-301 do arquivo): a primeira (linhas 280-287) é mais completa e já inclui todos os links; manter apenas ela
#### 02 - Anatomia de um trace LLM
- **Estado:** 242 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Mermaid ✗ · Tabela comparativa ✓ · Casos práticos ✓ · Armadilhas 3× [!warning] ✓ · Código (funcional, sem falha) ✓ · Inglês + tabela PT↔EN ✓ · Veja também ✓ · [!question]- ✓ · Checklist [!tip] ✓
- **Score verificar-nota (estimado):** 9/12 (E1✓ E2✗ E3✗ E4✓ E5✓ E6✓ E7✓ E8✓ P1✗ P2✓ L1✓ L2✓)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura-problema (E2) logo após o TL;DR e antes de "Os três níveis da hierarquia": cenário concreto que situe o problema antes de nomear a solução — ex: "um agent respondeu errado; como você investiga se não há hierarquia de spans?" — isso também acrescenta ~15 linhas ao volume
  - Adicionar diagrama Mermaid (E3) da árvore sessão→trace→spans para substituir o bloco ASCII — ganha E3 e +10 linhas de conteúdo real
  - Com as duas ações acima, o volume sobe de 242 para ~267 — ainda abaixo de 300; completar com um bloco P1 "código-com-falha" mostrando o anti-padrão de criar trace_id novo a cada LLM call (já descrito em [!warning] mas sem código) — isso fecha o piso e marca P1
#### 03 - Langfuse — open-source standard
- **Estado:** 302 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (Cloud vs self-host, research-agent, LangChain/LlamaIndex), armadilhas (3 [!warning]: flush, score-rubric, PII), inglês + tabela PT↔EN, [!question]-, Veja também
- **Score verificar-nota (estimado):** 10/12 (faltam E3 Mermaid, P1 código-com-falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - Substituir diagrama ASCII da arquitetura por Mermaid `graph LR` — fecha E3 sem adicionar conteúdo novo
  - Adicionar bloco P1 "código-com-falha" mostrando anti-padrão de criar `trace_id` novo a cada LLM call (já descrito no [!warning] de flush, mas sem código) — fecha P1 e sobe para 12/12
  - Caducidade (nota de ferramenta): Langfuse faz releases mensais; revisar free-tier (50k obs/mês), preços e versões do SDK a cada ~3 meses
#### 04 - Helicone, Phoenix, OpenLLMetry — alternativas
- **Estado:** 204 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Tabela comparativa · Casos práticos (≥2 por ferramenta) · 3× [!warning] · Inglês + tabela PT↔EN · [!question]- · Veja também
- **Score verificar-nota (estimado):** 10/12 (faltam E3 Mermaid e P1 código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar ~100 linhas de conteúdo real para atingir piso ≥300: candidatos são (a) diagrama Mermaid de decisão "qual ferramenta escolher" (fecha E3), (b) bloco P1 "código-com-falha" mostrando anti-padrão (ex: criar nova instrumentação sem reusar tracer_provider, ou misturar schemas OpenInference+OTel GenAI no mesmo projeto), (c) expandir seção "Combinações comuns" com exemplo de stack completa e fluxo de dados
  - Caducidade (catálogo de ferramentas): pricing (Helicone 10k/mês, Langfuse 50k obs/mês, Arize Phoenix Cloud) e trajetória dos projetos (releases, atividade GitHub, modelo de negócio) podem caducar em 3-6 meses — revisar antes de enriquecer ou reusar em contexto real
#### 05 - Versionamento de prompts
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Casos práticos (≥2 blocos de código), Armadilhas (3 [!warning]), Inglês + tabela PT↔EN, P1 código-com-falha (anti-pattern hardcoded), L1 wikilink cross-galho (Evaluation/07), L2 fontes externas com URL, [!question]-
- **Score verificar-nota (estimado):** 11/12 — falta só E3 Mermaid
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 06 - Session replay e debugging
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (capture/state/diff replay com código) · armadilhas (3× [!warning]) · inglês + tabela PT↔EN · wikilinks cross-galho · [!question]-
- **Score verificar-nota (estimado):** 10/12 (ausentes: E3 Mermaid · P1 código-com-falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 07 - Métricas que importam — latência, custo, qualidade
- **Estado:** 301 linhas (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** tabela comparativa · casos práticos (breakdown de custo, SLO) · armadilhas (3× [!warning]) · inglês + tabela PT↔EN · Veja também · [!question]-
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 08 - Privacy e PII em logs
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Tabela comparativa · Casos práticos (código Python + integração Langfuse) · Armadilhas (3× [!warning]) · Inglês + tabela PT↔EN · Veja também · [!question]-
- **Score verificar-nota (estimado):** 10/12 (faltam E3 Mermaid e P1 código-com-falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma

---

## 16. Multimodal Prompting

> Galho **usa `fase: Iniciado`** (piso ≥300). Enriquecido 28/06. Checar conteúdo real.

### Notas

#### 01 - O salto multimodal — por que isso importa
- **Estado:** 301 linhas totais / 146 linhas não-em-branco (piso Iniciado ≥300 total: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ (1 linha de conteúdo no callout, piso ≥3) · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** [!question]-, casos práticos (6), [!warning] (3), código com anti-padrão, tabela de custo por modalidade, tabela de decisão por caso, inglês com interview quote, tabela PT↔EN, Veja também, wikilinks cross-galho
- **Score verificar-nota (estimado):** 10/12 (falham E1-TL;DR e E3-Mermaid)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir TL;DR de 1 linha longa para ≥3 linhas separadas no callout [!abstract] (split dos pontos: estado do mercado / o gargalo / vantagens multimodal)
#### 02 - Imagens como input — screenshots, charts, mockups
- **Estado:** 311 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** tabela comparativa, casos práticos (5 tipos), 3 [!warning], código 3 providers, inglês + tabela PT↔EN, [!question]-, Veja também
- **Score verificar-nota (estimado):** 8/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir TL;DR de 1 bloco para ≥3 linhas separadas no [!abstract] (ex: estado do mercado / os 5 tipos de tarefa / regra de resolução/custo)
  - Adicionar parágrafo de abertura-problema antes de "## Cinco tipos de tarefa visual" — um cenário concreto (ex: screenshot de bug, mockup de revisão) que justifique por que a escolha de provider/detalhe importa antes de apresentar a taxonomia
#### 03 - PDFs e documentos — extração e análise
- **Estado:** 305 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** tabela comparativa, casos práticos (3 blocos de código reais), armadilhas [!warning] (3x), inglês + PT↔EN, veja também, [!question]-
- **Score verificar-nota (estimado):** 10/12 (faltam: E3 Mermaid, P1 código-com-falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 04 - Áudio e vídeo — Whisper, Gemini Live e geração
- **Estado:** 303 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (5 use cases), armadilhas (3 [!warning]), inglês + tabela PT↔EN, [!question]- com análise custo-benefício, código (3 snippets Python funcionais), tabela comparativa de limites/custos
- **Score verificar-nota (estimado):** 8/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - (E2) Adicionar parágrafo de abertura com problema/cenário antes do primeiro `##` — a nota vai direto pras seções sem contextualizar o leitor no desafio prático
  - (L1) Adicionar wikilink cross-galho (ex: para nota de outro galho do domínio IA, não apenas notas internas do Multimodal Prompting)
  - (Caducidade) "Claude voice sem API pública estável até maio/2026" — verificar se ainda é verdade e atualizar se necessário
  - (Opcional/E3) Mermaid do pipeline Whisper→LLM vs áudio-direto ajudaria a visualizar a decisão
#### 05 - Tabelas e spreadsheets como input estruturado
- **Estado:** 354 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** [!question], casos práticos (caso composto), inglês + tabela PT↔EN, 3 [!warning], wikilink cross-galho
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - (E2/Núcleo) Adicionar parágrafo de abertura com cenário concreto antes do TL;DR — ex: "Você tem uma planilha de 500 linhas e quer que o modelo a analise. Cola tudo no prompt? Manda print? Usa Code Interpreter? A escolha errada custa tokens, precisão ou os dois." O TL;DR e o [!question] existentes cobrem bem, mas a nota não tem abertura narrativa antes deles.
  - (P1/Opcional) Adicionar exemplo de código-com-falha para ilustrar o erro de colar CSV grande ou não avisar sobre separador BR — reforça as armadilhas com evidência de código quebrado
#### 06 - Como dizer ao modelo o tipo de leitura
- **Estado:** 300 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** [!question]-, casos before/after (3 pares), armadilhas (3 [!warning]), inglês, tabela PT↔EN, wikilinks cross-galho, Veja também
- **Score verificar-nota (estimado):** 10/12 (sem Mermaid · sem código-com-falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 07 - Limites e armadilhas multimodais
- **Estado:** 221 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos, [!warning] ×3, [!question]-, inglês + tabela PT↔EN, código (não é "com falha"), checklist, tabela comparativa, wikilinks cross-galho
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura narrativo (5-8 linhas) entre o `[!question]-` e a `## 1. Alucinação visual`, descrevendo o cenário: equipe em produção que descobriu multimodal, foi mandando print de tudo e viu o custo e as falhas explodirem — contextualiza o catálogo antes de entrar nele
  - Adicionar diagrama Mermaid (≈15 linhas) mapeando as 9 categorias de falha em dois eixos: tipo (percepção vs raciocínio vs custo/infra) e mitigabilidade (alta / parcial / baixa) — obtém E3, adiciona ~15 linhas reais e ajuda cruzar o piso de 300

---

## 17. Image Prompting

> Galho **usa `fase: Iniciado`** (piso ≥300). Enriquecido 28/06. Notas de modelos (caducidade). Checar conteúdo real.

### Notas

#### 01 - Image prompting como engenharia
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Tabela comparativa · Casos práticos (7 tipos) · 3× [!warning] · Código Python (resize/crop) · Inglês + tabela PT↔EN · [!question]- · Veja também
- **Score verificar-nota (estimado):** 10/12 (ausentes: E3 Mermaid, P1 código-com-falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 02 - Deliverable-first, não scene-first
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Casos práticos (≥2) · Armadilhas (3 [!warning]) · Inglês + tabela PT↔EN · Código Python (helper) · Vocabulário de âncoras visuais · Tabela canvas/aspect ratio · Exercício passo a passo
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir o `[!abstract]` TL;DR de 2 linhas markdown para ≥3 (quebrar o parágrafo único em pelo menos 3 linhas de citação `> `); como está, o callout tem só header + 1 linha de texto, abaixo do mínimo formal
#### 03 - Modelos de imagem 2026 — DALL-E, Imagen, Midjourney, FLUX, SD
- **Estado:** 236 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Tabela comparativa · `[!question]-` · Decision tree (ASCII) · Código (3 snippets API) · Armadilhas (4 × `[!warning]`) · Inglês + PT↔EN · Veja também
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar abertura com problema/cenário (~10-15 linhas) antes da tabela comparativa: o leitor salta direto da TL;DR para a tabela sem contexto de "por que tantos modelos existem" ou "o custo real de escolher errado" — cobre E2 e contribui para o piso
  - Converter o decision tree ASCII (linhas 76-98) para um diagrama Mermaid `flowchart TD` equivalente — cobre E3 e adiciona ~20 linhas de estrutura
  - Com essas duas mudanças o piso de 236→~270 sobe mas ainda fica abaixo de 300; completar com ~1 caso prático trabalhado (entregável real → modelo escolhido → prompt enviado → resultado) para atingir o piso — cobre P1 (código-com-falha/resultado-ruim como variante)
  - Atualizar `[!warning]` de caducidade: mencionar Imagen 4 (referenciado em linha 67 como "quando disponível" — já lançado em 2026), FLUX.1.1 Pro Ultra, e que Midjourney disponibilizou web API oficial em 2025 (altera a armadilha "pipeline via Discord bot")
#### 04 - Anatomia de um prompt visual — canvas, composição, estilo
- **Estado:** 282 linhas reais (piso Iniciado ≥300: não) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ (1 corpo linha; precisa ≥3) · Abertura-problema ✗ (abre direto em tabela, sem parágrafo de cenário/problema) · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓ (4 URLs externas)
- **Opcionais presentes:** Tabela comparativa · Casos práticos (2 exemplos trabalhados) · Armadilhas (3 × [!warning]) · Inglês + PT↔EN · [!question]- · Veja também
- **Score verificar-nota (estimado):** 9/12 (falham E2 abertura-problema, E3 Mermaid, P1 código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir TL;DR para ≥3 linhas de corpo (atualmente 1 linha densa; quebrar em 3 linhas curtas com as 4 camadas + a regra do default)
  - Substituir abertura de tabela por parágrafo-problema de 3-4 linhas (ex: "Você abre o Midjourney sem saber o que digitar além do tema...") antes da tabela "As quatro camadas"
  - Essas duas mudanças já devem elevar o conteúdo para ≥300 linhas e zerar as lacunas de núcleo
#### 05 - Templates por entregável — poster, infográfico, mockup, thumbnail
- **Estado:** 216 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (8 templates com exemplo preenchido), armadilhas (3 × [!warning]), inglês (interview quote + tabela PT↔EN), Veja também, [!question]-, tabela comparativa (Recapitulação rápida)
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar abertura com problema/cenário antes de "Como usar os templates" (2-3 §§ que enquadrem a dor: sem template você reescreve o mesmo brief do zero para cada entregável, erra o canvas, erra a hierarquia — o que a nota resolve)
  - Expandir via diagrama Mermaid de decisão (qual template escolher por canal/canvas) para +15-20 linhas reais e ganhar E3
  - As duas ações juntas devem levar a nota acima de 300 linhas reais e zerar as lacunas de núcleo
#### 06 - Iteração visual — controlled changes
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Casos práticos (≥2), Armadilhas (3×[!warning]), Inglês+tabela PT↔EN, Código (inpainting DALL-E e FLUX), Wikilink cross-galho, Veja também, [!question]-
- **Score verificar-nota (estimado):** 10/12 (ausentes: E3 Mermaid, P1 código-com-falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 07 - Geração de diagramas e ilustrações técnicas
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (≥2), armadilhas (3 [!warning]), inglês + tabela PT↔EN, código funcional (Python/Anthropic SDK), tabela comparativa de ferramentas, [!question]-
- **Score verificar-nota (estimado):** 10/12 (faltam: E3 Mermaid embutido na nota, P1 código-com-falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma

---

## 18. Improvement Loop

> Galho **usa `fase: Iniciado`** (piso ≥300). Enriquecido 28/06. Checar conteúdo real.

### Notas

#### 01 - O ciclo eval → diff → ship
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Tabela comparativa · Casos práticos (≥2) · Armadilhas (3× [!warning]) · Inglês + PT↔EN · Veja também · [!question]- · Código (eval loop em Python) · Wikilinks cross-galho (AI Engineering Stack)
- **Score verificar-nota (estimado):** 10/12 (faltam: E3 Mermaid — tem ASCII art em vez de diagrama Mermaid; P1 código-com-falha — código presente é exemplo funcional, não anti-padrão executável)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 02 - A-B testing de prompts
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (≥2) · armadilhas (3 [!warning]) · inglês + tabela PT↔EN · [!question]- · código Python (Langfuse) · wikilinks cross-galho · tabelas comparativas
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar parágrafo de abertura com problema/cenário entre o TL;DR e a primeira seção ("A unidade de teste"): a nota abre direto em tabela sem situar o leitor no problema que o A/B resolve.
#### 03 - Prompt versioning — semver para prompts
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (heurísticas de quando bumpar), armadilhas (3× [!warning]), inglês (quote + tabela PT↔EN), código CI (GitHub Actions YAML), tabela comparativa (registry patterns), wikilink cross-galho (Observability/05)
- **Score verificar-nota (estimado):** 10/12 (ausentes: E3 Mermaid, P1 código-com-falha)
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 04 - Champion-challenger em produção
- **Estado:** 266 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (feature flag + routing + YAML + rollback code) · armadilhas (3× [!warning]) · inglês + tabela PT↔EN · [!question]- · Veja também · wikilinks cross-galho
- **Score verificar-nota (estimado):** 9/12 (ausentes: E2 abertura-problema, E3 Mermaid, P1 código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar abertura-problema (2-3 parágrafos narrativos antes de "A mecânica básica"): problema de "como shipar um novo prompt sem quebrar prod" → por que A/B simples não basta → o que champion-challenger resolve. Isso resolve E2 e sobe o piso para ≥300 linhas simultaneamente.
  - Expandir TL;DR para ≥3 linhas raw de corpo (reformatar o parágrafo único em blocos separados por dimensão: setup / critérios / rollback / anti-padrão).
  - Converter o diagrama ASCII (linhas 32-67) para Mermaid flowchart (resolve E3).
#### 05 - Auto-prompt optimization — DSPy e além
- **Estado:** 301 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (tabelas "quando vence"), armadilhas (3× [!warning]), inglês com interview quote, tabela PT↔EN, [!question]-, Veja também, código funcional (Python DSPy)
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma
#### 06 - Capturando feedback do usuário como sinal
- **Estado:** 221 linhas reais (piso Iniciado ≥300: não passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** [!question]- · Tabela comparativa (explícito/implícito/weighting) · Casos práticos · 3× [!warning] · Código (solução) · Inglês + tabela PT↔EN · Veja também · Wikilinks cross-galho
- **Score verificar-nota (estimado):** 10/12 (faltam E3 Mermaid e P1 código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Expandir ~79 linhas de conteúdo real para atingir piso ≥300: adicionar diagrama Mermaid do pipeline coleta→agregação→triagem→backlog (fluxo já existe como texto, só visualizar) + trecho de código-com-falha (endpoint sem `trace_id` como anti-padrão, seguido da versão corrigida)
#### 07 - Eval gates em CI — quando bloquear merge
- **Estado:** 374 linhas reais (piso Iniciado ≥300: passa) · fase: Iniciado · status: seedling
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✓ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (tabelas + blocos YAML/Python), armadilhas (3 × [!warning]), inglês + tabela PT↔EN, [!question]-, wikilinks cross-galho
- **Score verificar-nota (estimado):** 10/12
- **Precisa mudança:** NÃO
- **Mudanças propostas:**
  - — nenhuma

---

## 19. Ferramentas de IA

> Galho de **notas-referência por ferramenta** (não trilha sequencial): Claude/Codex/Gemini/Copilot + Comparativo. `fase: Iniciado` mas grandes (626–909 l) — piso OK. Foco: caducidade (versões/preços) + se "inglês" é isenção intencional. "O que vem a seguir" pode não se aplicar a nota-referência.

### Notas

#### Claude (nota-referência)
- **Estado:** 910 linhas · fase: Iniciado · status: evergreen
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✗ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** tabela comparativa · casos práticos (5) · armadilhas (3 [!warning]) · inglês (How to explain in English) · PT↔EN · [!question]- · wikilinks cross-galho · fonte externa com URL
- **Score verificar-nota (estimado):** 8/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar `> [!abstract]` TL;DR com ≥3 linhas logo após o título (ausente — ponto mais fácil de corrigir)
  - Reescrever abertura para partir de problema/cenário ("Quando o time decide adotar um LLM de produção, a decisão de qual usar...") em vez de "Claude é uma das três famílias..." — abertura atual é "X é..." sem gancho de problema
  - Opcional: adicionar diagrama Mermaid do ecossistema (5 superfícies) ou do fluxo de tiering (Haiku→Sonnet→Opus) — único opcional de valor ainda ausente
  - Observação: seção "Armadilhas comuns" duplica conteúdo entre 3 callouts `[!warning]` e a lista numerada com os mesmos pontos — considerar unificar
- **Caducidade:** preços dos modelos (Opus ~$15/$75 · Sonnet ~$3/$15 · Haiku ~$0.80/$4) mudam a cada família lançada — ponto mais volátil; TTL de cache ("~5 minutos") é detalhe de implementação não documentado oficialmente; versão pinada `claude-sonnet-4-6-20260315` na tabela pode ficar obsoleta; package name `claude_agent_sdk` no snippet Python não está confirmado como nome real do SDK público
#### Codex (nota-referência)
- **Estado:** 627 linhas · fase: Iniciado · status: evergreen
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Casos práticos · Armadilhas `[!warning]` · Inglês (seção How to explain) · PT↔EN tabela · Cross-galho (Veja também) · Código de exemplo
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Converter o blockquote de abertura (linha 20) em `[!abstract]` com ≥3 linhas — único item núcleo ausente
  - Converter o diagrama de arquitetura em ` ```text ``` ` (linha 66-93) para Mermaid `flowchart TD`
  - Verificar e corrigir URLs de docs (`developers.openai.com/codex` e `/codex/skills/`) — OpenAI migrou documentação para `platform.openai.com`; links provavelmente mortos
  - Unificar seção "Armadilhas comuns": os 3 callouts `[!warning]` duplicam os mesmos pontos da lista numerada abaixo — manter callouts, remover lista redundante
- **Caducidade:** URLs `developers.openai.com/codex` e `developers.openai.com/codex/skills/` são o ponto mais crítico (alta chance de 404); estimativas de custo ("$25+ por task com o3", "$50-100/mês") voláteis; modelos citados na tabela (GPT-4.1, o1, o3) corretos em 2026 mas com vida curta; afirmação "AGENTS.md virou padrão de facto cross-tool" é claim de tendência sem fonte — monitorar
#### Comparativo de LLMs (nota-referência)
- **Estado:** 729 linhas · fase: Iniciado · status: evergreen
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** casos práticos (5 cases), inglês (pitch + deeper version + talking points), PT↔EN, armadilhas ([!warning] ×3), cross-galho (wikilinks ricos), fonte com URL (múltiplas)
- **Score verificar-nota (estimado):** 9/12 (faltam: TL;DR [!abstract], Mermaid, código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar TL;DR `> [!abstract]` ≥3 linhas logo após o H1 — item de núcleo mínimo ausente (único gap crítico)
  - Converter os 4 fluxogramas em blocos ` ```text ``` ` (Framework de decisão, Padrões 1-4) para Mermaid `flowchart TD` — ganha E3 e melhora leitura visual
  - Unificar seção "Armadilhas comuns": os 3 callouts `[!warning]` duplicam os pontos 1-3 da lista numerada abaixo — manter callouts, remover lista redundante
- **Caducidade:** tabela de preços por 1M tokens (seção "Custo 2026, aproximado") é o ponto mais volátil — valores mudam a cada lançamento; ranking de qualidade de código "em abril 2026" datado; linha "Fine-tuning: Claude: Não (em breve?)" pode ter mudado; afirmações de desconto de caching (−90% Claude, −50% GPT) requerem verificação periódica
#### Gemini (nota-referência)
- **Estado:** 636 linhas · fase: Iniciado · status: evergreen
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Casos práticos, Armadilhas `[!warning]`, Inglês, PT↔EN, Código (funcional), Cross-galho
- **Score verificar-nota (estimado):** 9/12
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Converter o blockquote inicial em `> [!abstract]` com ≥3 linhas sintetizando para que serve, diferenciais e quando usar — atende E1 (núcleo mínimo faltante)
  - Adicionar pelo menos um diagrama Mermaid (ex: `flowchart TD` de decisão "quando usar qual modelo" ou "Gemini CLI vs Vertex AI vs API direta") — atende E3
  - Remover duplicação entre os 3 callouts `[!warning]` e os pontos 1-3 da lista numerada em "Armadilhas comuns" — manter callouts, remover lista redundante
- **Caducidade:** tabela de preços (linha ~234, marcada "2026, aproximado") é o ponto mais volátil — valores mudam a cada release; "Recomendação prática em abril/2026" (linha ~266) está datada explicitamente; modelo "Gemini 2.5 Code" listado pode ter sido renomeado ou descontinuado; claims de contexto 2M tokens e Flash-Lite pricing requerem verificação periódica
#### GitHub Copilot (nota-referência)
- **Estado:** 706 linhas · fase: Iniciado · status: evergreen
- **Núcleo:** Frontmatter+fase ✓ · TL;DR ✗ · Abertura-problema ✓ · Corpo-mecanismo ✓ · O que vem a seguir ✓ · Fontes ✓
- **Opcionais presentes:** Casos práticos (5 cenários) · Armadilhas `[!warning]` (3 callouts) · Inglês (seção "How to explain in English") · Tabela PT↔EN · Código com exemplos (CLI, YAML, Markdown)
- **Score verificar-nota (estimado):** 9/12 (faltam E1 TL;DR, E3 Mermaid, P1 código-com-falha)
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar `> [!abstract]` TL;DR com ≥3 linhas logo após o título (núcleo mínimo ausente — item mais urgente)
  - Adicionar 1 diagrama Mermaid — sugestão: fluxo dos modos de operação (Completion → Chat → Edit → Agent → Workspace) ou pipeline de contexto do IDE
  - Remover duplicação entre os 3 callouts `[!warning]` e os 10 itens da lista numerada em "Armadilhas comuns" — manter callouts, remover lista redundante
- **Caducidade:** tabela de planos (~linha 295) com preços aproximados ("~$10/mês", "~$19/mês", "~$39/user/mês") é o ponto mais volátil — GitHub altera planos e preços com frequência; lista de modelos disponíveis (~linha 253: "GPT-4.1, GPT-4o, Claude Sonnet 4.x, Gemini 2.5") pode estar desatualizada; `github/copilot-review-action@v1` na seção de Actions pode ter mudado de versão ou API; Copilot Workspace estava em preview/beta em 2024-2025 e pode ter mudado de nome ou features

---

## Notas soltas (raiz IA)

> Artefatos especiais na raiz do domínio IA, NÃO notas de trilha. A régua "capítulo de livro" se aplica de forma reduzida: **Dicionário** (type: glossary) é isento de inglês/abertura-problema; **Biblioteca** (type: reference) é um MOC de recursos; só **Maturidade Yegge** (type: concept) é nota de conteúdo plena.

#### Biblioteca de Desenvolvimento com IA (reference)
- **Estado:** 41 linhas · type: reference · fase: N/A · status: seedling
- **Diagnóstico:** Cumpre o papel de biblioteca do domínio: organizada em três seções claras (Indispensáveis / Vozes individuais / Repositórios curados) mais um callout de lacuna. Todos os links externos em formato markdown válido; wikilinks internos apontam para verbetes do Dicionário de IA com âncora correta. Nota curta mas sem padding — cada entrada tem descrição útil e não há conteúdo de enchimento. Status seedling é apropriado para o tamanho atual. Ponto fraco: ainda não tem seção de ferramentas/plataformas (LLMOps, evals, observabilidade) nem de vídeos ou cursos — lacunas óbvias para um domínio tão rico.
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar seção "Ferramentas e plataformas" com entradas para Langfuse, Arize Phoenix, Weights & Biases (LLM monitoring) — já cobertos no Dicionário mas sem referência bibliográfica na Biblioteca
  - Adicionar seção "Vídeos e cursos" com ao menos 2-3 entradas (ex.: DeepLearning.AI short courses, Andrej Karpathy no YouTube)
  - Atualizar status: seedling → growing após expansão
- **Caducidade:** Link para Sourcegraph blog (Steve Yegge) pode estar quebrado ou redirecionado — Yegge mudou de empresa em 2025; verificar antes de enriquecer
#### Modelo de Maturidade AI - Steve Yegge (concept)
- **Estado:** ~350 linhas · type: concept · fase: ausente · status: growing
- **Diagnóstico:** Nota de conteúdo plena e substancial: cobre os 8 estágios com mecanismo, sinal típico, ganho e limite por estágio; tem tabela-mapa, seção de transições práticas, críticas ao modelo e heurística final. Wikilinks com full path corretos; referências com URL presentes. Dois gaps estruturais: (1) ausência de `[!abstract]` com TL;DR na abertura — abre direto em prosa sem resumo de 1-2 linhas; (2) `fase:` ausente no frontmatter — para concept solto na raiz é justificável como N/A, mas deveria ser explícito. Defeito menor: linha 350 tem um bullet dangling (`-` sem conteúdo) na seção "Veja também". URL "The Death of the Junior Developer" aponta para `webflow.sourcegraph.com`, padrão distinto dos demais links Sourcegraph — pode estar incorreto ou ser redirect.
- **Precisa mudança:** SIM
- **Mudanças propostas:**
  - Adicionar `fase: N/A` no frontmatter (concept solto, fora de galho)
  - Inserir callout `[!abstract]` com TL;DR de 2 linhas logo após o H1
  - Remover bullet dangling na última linha da seção "Veja também"
  - Verificar e corrigir URL de "The Death of the Junior Developer" (domínio `webflow.sourcegraph.com` diverge dos demais)
- **Caducidade:** Yegge publicou a série em 2024-2025 e deixou a Sourcegraph em 2025 — links do blog Sourcegraph podem ter sido redirecionados ou removidos; o próprio modelo de 8 estágios foi escrito num momento em que agentes autônomos estavam emergindo e pode precisar de atualização com a maturação do ecossistema (ex.: background agents, multi-agent frameworks) em 2026
#### Dicionário de IA (glossary)
- **Estado:** ~518 linhas · type: glossary · fase: N/A · status: seedling
- **Diagnóstico:** Glossário saudável e extenso: ~15 seções temáticas com cobertura ampla (agents, coding agents, context engineering, evals, LLMs, MCP, memória, observabilidade, RAG, segurança, modelos de sequência, spec-driven, economia de tokens, tooling, fundamentos). Frontmatter coerente (aliases incluem PT e EN, `updated: 2026-06-27`). Ordem alfabética dos verbetes respeitada dentro de cada seção. Nenhum verbete duplicado ou quebrado identificado. Os 5 TODOs explícitos na seção "Human Factors" (débito de compreensão, rendição cognitiva, deskilling, psicose da IA, tokenmaxxing) estão corretamente marcados como candidatos — não são bugs, são backlog documentado. Único ponto estético: status seedling subestima um glossário de 518 linhas e ~100 verbetes, mas é escolha do autor.
- **Precisa mudança:** NÃO (manutenção contínua, sem reforma estrutural)
- **Mudanças propostas:**
  - Promover os 5 TODOs pendentes em Human Factors via `/verbete` em sessões futuras (prioridade: rendição cognitiva e deskilling, mais relevantes para o contexto do vault)
  - Considerar upgrade de status: seedling → growing após promover ao menos 3 dos TODOs
- **Caducidade:** Verbetes com datas explícitas (2026) estão bem cravados; entradas de regulamentação (EU AI Act cronograma, LGPD multas) têm datas de aplicação que podem evoluir com atualizações legislativas; verbete FlashAttention cita v4/Hot Chips 2025 — acompanhar versões futuras
