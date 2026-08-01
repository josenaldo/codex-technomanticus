---
title: "Roadmap — N6 O repositório como testemunha"
created: 2026-07-31
updated: 2026-07-31
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — N6 O repositório como testemunha

Roadmap do sub-galho `Controle de Versão/N6 - O repositório como testemunha` (galho-folha). **Escrita completa em 2026-07-31 — 3/3 notas.** O capstone (34) fica na raiz do domínio.

**Nível:** folha. **Público:** técnico / consultor de legado. **Fase:** Magus nas 3.

**Papel no domínio:** é o sub-galho que **justifica o domínio existir**. Instrumento da arqueologia de software; a fronteira com `Engenharia/Arqueologia e Restauração de Software` é declarada em callout no `index.md` e reafirmada na 33 e no capstone.

**Legenda:** ✅ escrita + enriquecida · 🔶 escrita, falta enriquecer.

## Notas

| # | Nota | Estado | Pendências |
|---|------|--------|-----------|
| — | `index.md` | ➖ MOC | — |
| 31 | Ler história de verdade | 🔶 escrita | M1 |
| 32 | `bisect` — achar o commit que quebrou | 🔶 escrita | M1 |
| 33 | Forense de repositório | 🔶 escrita | M1 |
| 34 | Capstone (na raiz do domínio) | 🔶 escrita | M1 |

## Decisões de escrita registradas

- **Nota 31 dá o truque mais útil da investigação**: `git log --merges --ancestry-path <hash>..HEAD` para achar o PR pelo qual um commit entrou — o caminho do código de volta ao *porquê*. E trata o `.git-blame-ignore-revs` como prática a adotar **no mesmo dia** de qualquer reformatação em massa.
- **`blame` explicitamente desaconselhado como atribuição de culpa** (nota 31) — argumento duplo: ele mostra quem tocou por último (não quem decidiu), e o uso punitivo destrói a disposição do time de mexer em código antigo.
- **Nota 32 conecta bisect à disciplina de commit** numa tabela de pré-requisitos: história completa, commits atômicos, todo commit compilando. Fecha o argumento de que a higiene dos níveis 1-2 não é estética — é o que torna a busca binária possível.
- **Código de saída 125** (`skip` automático) e **script fora do repositório** documentados — dois detalhes que quebram o `bisect run` de quem tenta pela primeira vez.
- **Nota 33 tem uma seção inteira sobre o que os dados NÃO dizem** — contagem de commits não mede produtividade, hotspot não é veredito, migrações distorcem contagens. Métrica de repositório é fácil de usar mal, e o material é compartilhável.
- **`quadrantChart` evitado** no diagrama de hotspots por risco de render; substituído por `graph TB` com os quatro casos. Decisão a repetir enquanto não houver validação do tipo no vault.
- **Capstone estruturado por hora** (4 blocos), com tabela final de "o que você deve ter" e tabela de costura dos 7 níveis. Fecha com um `[!warning]` sobre o **limite honesto**: o repositório registra o que foi feito, não o que se pretendia — e confundir as duas coisas leva a diagnósticos corretos e politicamente suicidas.

## Ganchos quitados

| Gancho aberto em | Quitado por |
|---|---|
| `blame` / pickaxe (07) | 31 |
| ramos fósseis no legado (13) | 31, capstone |
| `bisect` para achar o commit que quebrou (24) | 32 |
| forense e hotspots (design do domínio) | 33 |
| ponte instrumento ↔ método com Arqueologia | index do N6, 33, capstone |

## Próximos passos

1. ⬜ **M1 — mídia**: 1 vídeo por nota + capstone.
2. ⬜ **Dicionário**: pickaxe, hotspot, acoplamento temporal, ilha de conhecimento, bus factor, `--ancestry-path`, `blame.ignoreRevsFile`.
3. ⬜ **Ponte de volta**: acrescentar callouts em `Engenharia/Arqueologia e Restauração de Software` apontando para o N6 como instrumental — a fronteira está declarada deste lado, falta o outro.
4. ⬜ Avaliar broto sobre **code-maat / CodeScene na prática** (rodar as análises de verdade) se o assunto crescer.
