---
title: "Roadmap — IA (raiz do domínio)"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — IA (raiz do domínio)

Roadmap **raiz do domínio**: mapeia o **estado de cada galho** (não as notas dos galhos) e as **notas soltas** logo abaixo de `IA/`. Cada galho tem o próprio `roadmap.md` mapeando suas notas (e, se for galho-pai, seus sub-galhos).

**Domínio:** `03-Dominios/Tecnologia/IA`
**Nível:** raiz (contém galhos)
**Rastreio multi-nível:** raiz → galho → (sub-galho) → nota. Cada nível mapeia só o nível imediatamente abaixo.

> [!note] Auditoria de reconciliação — 2026-07-03. Cruzamento de contagem de notas, mapeamento entrada-do-roadmap↔arquivo e git (último commit de nota por galho) confirmou que **os 21 roadmaps de galho estão estruturalmente atuais**. O medo anterior ("vários ⬜ já foram enriquecidos por commits posteriores") **não se materializou**: nenhuma nota de galho pendente foi alterada após o diagnóstico de 30/06 — só os 3 galhos já ✅ (Ferramentas 01/07, Evaluation e Structured Outputs 02/07) tiveram commits posteriores. Os estados ⬜/✅ abaixo são fiéis. Banner falso de Anatomia dos LLMs corrigido nesta data. Nenhum galho exige re-diagnóstico.

> [!note] Passe de material externo — 2026-08-20. Comparação do domínio com o board Excalidraw *IA do Zero ao Sênior* (Gabriel Dias), fichado em [[2026-ia-do-zero-ao-senior-trilha-visual]]. O board não acrescentou cobertura — o domínio é bem maior que ele —, mas expôs **duas lacunas reais e seis heurísticas ausentes**. Resultado: 2 notas novas (Segurança 13 · Prompt injection, e Evaluation 09 · Abstenção), 6 enriquecimentos cirúrgicos em notas já ✅ (Anatomia de Agents 06, Prompt Engineering 03, RAG 12, Economia de Tokens 09, Anatomia dos LLMs 02, Context Engineering 03), 1 bloco novo + 1 rota no galho de Segurança, e 1 senda + 1 programa de 90 dias no `index.md` do domínio. Todos registrados nos roadmaps de galho. **Lição de método:** duas das seis "lacunas" que eu tinha listado por grep estavam erradas — o tema existia com outro fraseado. Confirme no arquivo antes de escrever, não no resultado do grep.

## Como o rastreio funciona

- **Galho-folha** (só notas): `roadmap.md` mapeia suas notas, uma entrada por nota.
- **Galho-pai** (contém sub-galhos): `roadmap.md` mapeia o estado dos sub-galhos + suas notas diretas.
- **Raiz (este arquivo):** mapeia o estado dos galhos + as notas soltas de `IA/`.
- Ao fechar/mexer num galho, atualizam-se os roadmaps do **galho**, dos **filhos** e dos **pais** (sobe e desce a árvore).

**Legenda de estado:** ✅ completo (0 ⬜) · 📋 diagnosticado, enriquecimento pendente · 🔶 parcial · ⬜ não diagnosticado · ⚪ especial/fora do fluxo · `%` = (✅ + ➖) / total.

## Galhos

| # | Galho | Notas | ⬜ | ➖ | ✅ | % | Estado | roadmap |
|---|-------|------:|---:|---:|---:|--:|--------|---------|
| 1 | [[Anatomia dos LLMs]] | 24 | 0 | 1 | 23 | 100% | ✅ completo (2026-07-03) | ✅ |
| 2 | [[Anatomia de Agents]] | 11 | 0 | 0 | 11 | 100% | ✅ completo (2026-07-03, fan-out ≤3 verificado) | ✅ |
| 3 | [[Spec-Driven Development]] | 12 | 0 | 0 | 12 | 100% | ✅ completo (2026-07-03, fan-out ≤3 verificado) | ✅ |
| 4 | [[Economia de Tokens]] | 22 | 0 | 2 | 20 | 100% | ✅ completo (2026-07-04, 20/20 via fan-out ≤3 verificado; 05·09 dispensadas) | ✅ |
| 5 | [[Context Engineering]] | 16 | 0 | 9 | 7 | 100% | ✅ completo (2026-07-03) | ✅ |
| 6 | [[Agentes de Codificação]] | 18 | 0 | 3 | 15 | 100% | ✅ completo (2026-07-05, 15/15 acionáveis via fan-out ≤3 verificado; 02·04·16 dispensadas) | ✅ |
| 7 | [[AI Engineering Stack]] | 13 | 0 | 1 | 12 | 100% | ✅ completo (2026-07-06, 12/12 acionáveis via fan-out ≤3 verificado) | ✅ |
| 8 | [[RAG e Vector Databases]] | 13 | 0 | 1 | 12 | 100% | ✅ completo (2026-07-06, 12/12 acionáveis via fan-out ≤3 verificado; nota 13 com desvio de piso registrado) | ✅ |
| 9 | [[MCP]] | 10 | 0 | 0 | 10 | 100% | ✅ completo (2026-07-06, 10/10 via fan-out ≤3 verificado) | ✅ |
| 10 | [[Segurança e Guardrails]] | 13 | 0 | 0 | 13 | 100% | ✅ completo (2026-07-06 + **nota 13 em 2026-08-20**, que abre o Bloco 5 — segurança de runtime; caducidade EU AI Act resolvida — Digital Omnibus adiou high-risk) | ✅ |
| 11 | [[Memória de Agentes]] | 24 | 0 | 7 | 17 | 100% | ✅ completo (2026-07-07, 14/14 acionáveis via fan-out ≤3 verificado; caducidade das notas de implementação atualizada via web) | ✅ |
| 12 | [[Prompt Engineering]] | 9 | 0 | 2 | 7 | 100% | ✅ completo (2026-07-03) | ✅ |
| 13 | [[Structured Outputs]] | 8 | 0 | 1 | 7 | 100% | ✅ completo (2026-07-02) | ✅ |
| 14 | [[Evaluation]] | 9 | 0 | 4 | 5 | 100% | ✅ completo (2026-07-01 + **nota 09 Abstenção em 2026-08-20**) | ✅ |
| 15 | [[Observability]] | 8 | 0 | 5 | 3 | 100% | ✅ completo (2026-07-03) | ✅ |
| 16 | [[Multimodal Prompting]] | 7 | 0 | 2 | 5 | 100% | ✅ completo (2026-07-03 — notas 04/05 refeitas com pesquisa real após reprovação) | ✅ |
| 17 | [[Image Prompting]] | 7 | 0 | 3 | 4 | 100% | ✅ completo (2026-07-03) | ✅ |
| 18 | [[Improvement Loop]] | 7 | 0 | 4 | 3 | 100% | ✅ completo (2026-07-03) | ✅ |
| 19 | [[Ferramentas de IA]] | 5 | 0 | 0 | 5 | 100% | ✅ completo (2026-07-01) | ✅ |
| 20 | [[Claude Code]] | 55 (6 sub-galhos) | 0 | 1 | 54 | 100% | ✅ completo (2026-07-08, 6/6 sub-galhos enriquecidos via fan-out ≤3 verificado) | ✅ (galho-pai) |
| 21 | [[O Lado Sombrio da IA]] | 1 + glosas | 0 | 0 | 1 | 100% | ✅ completo (2026-07-09) — nota Débito cognitivo enriquecida | ✅ |
| 22 | [[Evolução da Engenharia de IA]] | 9 | 0 | 0 | 9 | 100% | ✅ completo 2026-07-23 (historiografia prompt→graph); escrito 07-20, fidelidade+nota 09 07-21, `/verificar-nota`+enriquecimento (inglês/armadilhas/fontes/mídia) 07-23; 4 imagens ✅; nota-satélite prática em Claude Code/Workflows/12; galho aberto por design (próxima camada = nota 10) | ✅ |

## Notas soltas (logo abaixo de IA/)

| Nota | Tipo | Estado |
|------|------|--------|
| `Dicionário de IA.md` | glossary | ➖ saudável (diagnóstico 30/06) |
| `Modelo de Maturidade AI - Steve Yegge.md` | nota solta | ✅ revisada (471 linhas, TL;DR presente, updated 2026-07-09) |
| `Biblioteca de Desenvolvimento com IA.md` | reference | ⬜ stub (diagnóstico 30/06) |
| `index.md` | MOC do domínio | ➖ não precisa |

## Tabela-resumo (agregado dos galhos)

| Métrica | Valor |
|---------|-------|
| Galhos totais | 21 |
| ✅ completos | 21 (Anatomia dos LLMs, Anatomia de Agents, Spec-Driven Development, Economia de Tokens, Context Engineering, Prompt Engineering, Structured Outputs, Evaluation, Observability, Multimodal Prompting, Image Prompting, Improvement Loop, Ferramentas de IA, Agentes de Codificação, AI Engineering Stack, RAG e Vector Databases, MCP, Segurança e Guardrails, Memória de Agentes, Claude Code — 2026-07-08, **O Lado Sombrio da IA — 2026-07-09**) |
| 📋 diagnosticados, enriquecimento pendente | 0 |
| ⬜ não diagnosticados | 0 |
| ⚪ especiais | 0 |
| Notas soltas diretas | 4 |
| Notas totais (galhos-folha diagnosticados) | ~289 (234 + 55 de Claude Code) |

> **IA 100% diagnosticado em 2026-07-02** — todos os 21 galhos têm `roadmap.md`. Último buraco (Claude Code, galho-pai de 6 sub-galhos = 55 notas) fechado via workflow de fan-out (48 notas em ~2,4 min).

---

## Próximos passos

1. ~~**Diagnosticar Claude Code**~~ ✅ **feito (2026-07-02)** — 6 sub-galhos, 55 notas, todos com `roadmap.md`. Ver `Claude Code/roadmap.md`.
2. ~~**Re-diagnosticar Anatomia dos LLMs**~~ ✅ **desnecessário (auditoria 03/07)** — o roadmap já está pós-reformulação e mapeia 1:1 para os arquivos; banner defasado corrigido.
3. ~~**Reconciliar os 📋**~~ ✅ **feito (auditoria 03/07)** — git confirmou que nenhuma nota de galho pendente mudou após o diagnóstico de 30/06; estados ⬜/✅ fiéis. Próximo movimento em cada galho é **enriquecimento** (`/enriquecer-galho`), não re-diagnóstico.
4. ~~**O Lado Sombrio da IA**~~ ✅ nota Débito cognitivo diagnosticada; cluster mantém glosas na raiz (não promover), mas agora tem `roadmap.md`.
5. **Passe de material externo (2026-08-20)** ✅ feito — ver banner no topo. Pendência consciente: o **Bloco 5 de Segurança e Guardrails tem 1 nota só**; se crescer para ~5, graduar a galho próprio pela convenção broto → galho.
