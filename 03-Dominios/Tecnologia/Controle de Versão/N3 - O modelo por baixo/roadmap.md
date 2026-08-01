---
title: "Roadmap — N3 O modelo por baixo"
created: 2026-07-31
updated: 2026-07-31
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — N3 O modelo por baixo

Roadmap do sub-galho `Controle de Versão/N3 - O modelo por baixo` (galho-folha). **Escrita completa em 2026-07-31 — 5/5 notas.** Mídia (M1) parcial — ver roadmap do domínio.

**Nível:** folha (uma entrada por nota).

**Público:** técnico. Fases: 17-19 Adepto, 20-21 Magus.

**Papel no domínio:** é o **ponto de virada**. Não introduz comando novo — reexplica N0-N2 como mecanismo, e quita a maior parte dos ganchos deixados nos três níveis anteriores.

**Legenda:** ✅ escrita + enriquecida · 🔶 escrita, falta enriquecer · 📋 desenhada · ⬜ não iniciada.

## Notas

| # | Nota | Fase | Estado | Pendências |
|---|------|------|--------|-----------|
| — | `index.md` | — | ➖ MOC | — |
| 17 | Tudo tem hash — o modelo de objetos | Adepto | 🔶 escrita | — |
| 18 | Commit é snapshot, não diff — o DAG | Adepto | 🔶 escrita | — |
| 19 | Refs, HEAD e branch como ponteiro | Adepto | 🔶 escrita | — |
| 20 | O index por dentro | Magus | 🔶 escrita | — |
| 21 | Merge e rebase por dentro | Magus | 🔶 escrita | — |

## Material próprio incorporado

- **Nota 19** redesenha em Mermaid a **sequência "Entendendo o branch"** do `workshop-git` (Tomo 7) — 9 slides originais condensados em **7 passos**, do primeiro commit à divergência, e reexplicados em termos de arquivos de 41 bytes. É a peça central do nível.
- **Nota 21** redesenha os diagramas de **merge × rebase** do Tomo 8, acrescentando o commit órfão (`C4` ao lado de `C4'`), que o material original não mostrava e que é o que explica a regra de ouro.
- **Nota 17** desenvolve *"Tudo tem checksum SHA-1"* e *"Git só adiciona dados"* do `curso-git-github` (Tomo 6) — as duas frases que, no material original, abriam o bloco "Subindo de nível".
- **Nota 18** desenvolve *"Snapshots x diferenças"* do `workshop-git` (Tomo 2).

## Ganchos quitados neste nível

| Gancho aberto em | Quitado por |
|---|---|
| three-way merge / ancestral comum (09) | 21 |
| rebase como mecanismo (11, 12, 13) | 21 |
| a regra de ouro do rebase (11, 12) | 21 |
| "o Git só adiciona dados" (04) | 17, 18 |
| por que `--amend` cria commit novo (04) | 17 |
| por que ramificar é instantâneo (08) | 19 |
| por que apagar ramo não perde trabalho (08) | 19 |
| `origin/main` é fotografia local (11) | 19 |
| tag não vai no push / não mover tag (14) | 19 |
| por que `--force` apaga trabalho alheio (11) | 19, 21 |
| o que a área de preparação é, afinal (03) | 20 |
| a tabela do `reset` soft/mixed/hard (04) | 20 (prepara a 22) |

## Ganchos ainda abertos daqui

| Gancho | Nota que quita |
|---|---|
| `reflog` e objetos órfãos (17, 18, 19, 21) | 23 |
| árvore de decisão do `reset` (20) | 22 |
| `rerere` e config a favor (21) | 26 |
| reescrever histórico para remover blob grande (17) | 25 |
| `fsck --lost-found` (18, 20) | 23 |

## Decisões de escrita registradas

- **`zdiff3` recomendado explicitamente** (nota 21) — mostra a base junto dos dois lados no conflito; a configuração mais subestimada do Git e a que mais ajuda quem sofre com conflito.
- **A afirmação "commit é snapshot" foi qualificada com honestidade** (nota 18): conceitualmente snapshot, fisicamente com compressão por delta no packfile. Separar modelo de armazenamento evita que o leitor descubra depois e ache que foi enganado.
- **SHA-1 tratado sem alarmismo** (nota 17): colisão SHAttered é real, mas o Git tem detecção embutida desde 2.13 e SHA-256 existe desde 2.29 com adoção baixa por interoperabilidade incompleta. Conclusão honesta: você vai usar SHA-1 e está tudo bem.
- **Inversão de `--ours`/`--theirs` durante rebase** documentada como armadilha (nota 21) — erro clássico e caro, raramente ensinado.

## Próximos passos

1. 🔶 **M1 — mídia**: ver o estado consolidado no [[03-Dominios/Tecnologia/Controle de Versão/roadmap|roadmap do domínio]] (25/34 embutidos e verificados em 2026-07-31).
2. ✅ **Dicionário do domínio** — criado 2026-07-31; os termos deste nível já entraram.
3. ⬜ Considerar um broto sobre **packfiles e `git gc`** se o assunto crescer — hoje ele aparece como callout na 17 e na 18.
