---
title: "Roadmap — Multimodal Prompting"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Multimodal Prompting

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Multimodal Prompting`

> [!warning] Diagnóstico de 30/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado)
**Piso de linhas:** aplicável — Iniciado ≥300

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 7 |
| ⬜ pendente | 0 |
| ➖ não precisa | 2 |
| ✅ feita | 5 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - O salto multimodal — por que isso importa   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 301 linhas totais / 146 linhas não-em-branco · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1, E3
- **Score:** 10/12
- **Plano de execução:**
  - Expandir TL;DR de 1 linha longa para ≥3 linhas separadas no callout [!abstract] (split: estado do mercado / o gargalo / vantagens multimodal)
- **Resultado:** ✅ verificado PASS (2026-07-03): plano aplicado + auditoria cética passou.

#### 02 - Imagens como input — screenshots, charts, mockups   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 311 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1, E2, E3, P1
- **Score:** 8/12
- **Plano de execução:**
  - Expandir TL;DR de 1 bloco para ≥3 linhas separadas no [!abstract] (ex: estado do mercado / os 5 tipos de tarefa / regra de resolução/custo)
  - Adicionar abertura-problema antes de "## Cinco tipos de tarefa visual" — cenário concreto (screenshot de bug, mockup de revisão) que justifique a escolha de provider/detalhe antes da taxonomia
- **Resultado:** ✅ verificado WARN (2026-07-03): plano aplicado + auditoria cética passou. — WARN: ressalvas menores (ver relatório da sessão)

#### 03 - PDFs e documentos — extração e análise   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 305 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 04 - Áudio e vídeo — Whisper, Gemini Live e geração   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03, refação pós-reprovação)
- **Estado:** 318 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, L1, P1
- **Score:** 8/12
- **Plano de execução:**
  - (E2) Adicionar parágrafo de abertura com problema/cenário antes do primeiro `##` — a nota vai direto pras seções sem contextualizar o desafio prático
  - (L1) Adicionar wikilink cross-galho (não só notas internas do Multimodal Prompting)
  - (Caducidade) Verificar se "Claude voice sem API pública estável até maio/2026" ainda é verdade e atualizar
  - (Opcional/E3) Mermaid do pipeline Whisper→LLM vs áudio-direto, para visualizar a decisão
- **Resultado:** ✅ refeita com PESQUISA REAL (não o burst reprovado). E2: abertura com cenário de reunião de negociação. E3: Mermaid da decisão transcrever-vs-escutar. L1: cross-galho → [[Economia de Tokens/01 - O problema — por que tokens custam dinheiro]]. **Caducidade corrigida (web-verificado 03/07):** Claude Voice Mode existe (app + Claude Code desde mar/2026) mas é **input-only/ditado** — não é áudio-como-mídia nem API de voz bidirecional; removido o erro de listá-lo junto a Gemini Live/OpenAI Realtime. Zero fabricação.

#### 05 - Tabelas e spreadsheets como input estruturado   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03, refação pós-reprovação)
- **Estado:** 402 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - (E2/Núcleo) Adicionar abertura com cenário concreto antes do TL;DR — ex: planilha de 500 linhas, cola tudo no prompt ou manda print ou usa Code Interpreter, e a escolha errada custa tokens/precisão
  - (P1/Opcional) Adicionar exemplo de código-com-falha (colar CSV grande, ignorar separador BR) para reforçar as armadilhas com evidência de código quebrado
- **Resultado:** ✅ E2: abertura com cenário da planilha de 500 linhas + eixo de decisão. E3: Mermaid dos três modos. **P1 com EVIDÊNCIA REAL (pandas 3.0 rodado localmente):** o CSV BR (sep `;`, decimal `,`) lido com defaults **NÃO lança `ParserError`** — vira 1 coluna só (silencioso); com `sep=';'` mas sem `decimal=','`, `.sum()` concatena string (`'12,504,90'`) sem erro. Corrige a suposição do burst reprovado (que afirmava ParserError). Outputs conferidos, zero fabricação.

#### 06 - Como dizer ao modelo o tipo de leitura   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 300 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 07 - Limites e armadilhas multimodais   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 221 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar abertura narrativa (5-8 linhas) entre o `[!question]-` e a `## 1. Alucinação visual` — cenário de equipe em produção que descobriu multimodal, mandou print de tudo, e viu custo e falhas explodirem
  - Adicionar diagrama Mermaid (≈15 linhas) mapeando as 9 categorias de falha em dois eixos: tipo (percepção/raciocínio/custo-infra) e mitigabilidade (alta/parcial/baixa) — cobre E3 e ajuda a cruzar o piso de 300
- **Resultado:** ✅ verificado PASS (2026-07-03): plano aplicado + auditoria cética passou.
