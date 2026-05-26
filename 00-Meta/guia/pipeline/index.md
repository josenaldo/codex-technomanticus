---
title: "Pipeline do Codex — Visão geral"
type: moc
publish: true
created: 2026-05-04
updated: 2026-05-04
tags:
  - guia
  - vault
  - canon
  - pipeline
---

# Pipeline do Codex — Visão geral

O Codex Technomanticus é um grimório vivo: o conhecimento entra como link bruto, amadurece em fichamento, consolida em corpus, e é navegado por mapas. Este documento dá a visão de alto nível do pipeline; cada etapa tem documento próprio nesta subpasta.

## As quatro zonas

| Zona | Pasta | Papel |
|---|---|---|
| 1. Pergaminhos | `01-Pergaminhos/` | Captura inicial: inbox, links soltos, ideias cruas. |
| 2. Glosas | `02-Glosas/` | Fichamentos de materiais externos consumidos. |
| 3. Domínios | `03-Dominios/` | Corpus do conhecimento. **Centro gravitacional do vault**. |
| 4. Sendas | `04-Sendas/` | Mapas curatoriais — fluxogramas de leitura sobre os domínios. |

## Pipeline de alimentação

```text
Pergaminhos → Glosas → Domínios
   ↓             ↓         ↑
captura     fichamento  consolidação
                            ↑
                          Sendas (mapas transversais)
```

A seta de Sendas pra Domínios é dupla: sendas **consomem** notas dos domínios (referenciando wikilinks), mas não alimentam os domínios.

## Princípios

1. **Domínios são estantes; sendas são fluxograma.** Domínios guardam o conhecimento; sendas dizem em que ordem ler.
2. **Glosa é leitura, nota é conhecimento.** Coisas diferentes — glosa permanece como artefato datado, nota nasce como síntese atemporal.
3. **Materiais externos são convites.** Vivem dentro de notas de domínio (callout `[!convite]`), não nas sendas. Quando consumidos, viram glosas.
4. **Progresso é estado de estudo.** Campo `progresso` no frontmatter rastreia o estado pessoal de cada nota/glosa, ortogonal ao `status` (maturidade do conteúdo).

## Documentos por etapa

- [[Pergaminhos]] — etapa 1: captura inicial.
- [[Glosas]] — etapa 2: fichamento e promoção.
- [[Domínios]] — etapa 3: corpus de conhecimento.
- [[Sendas]] — mapas de leitura.

## Ver também

- [[Como usar este vault]]
- [[Convenções de escrita]]
- [[Decisões do vault]]
- [[workflow]]
- [[Wikilinks e MOCs]]
