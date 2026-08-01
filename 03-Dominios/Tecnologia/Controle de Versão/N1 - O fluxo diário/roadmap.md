---
title: "Roadmap — N1 O fluxo diário"
created: 2026-07-31
updated: 2026-08-01
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — N1 O fluxo diário

Roadmap do sub-galho `Controle de Versão/N1 - O fluxo diário` (galho-folha). **Escrita completa em 2026-07-31 — 6/6 notas.** **M1 (mídia) completo em 2026-08-01.**

**Nível:** folha (uma entrada por nota).

**Público:** ainda amplo (exemplos acadêmicos), mas o vocabulário começa a se aproximar do de equipes de software. Fases: 06-09 Iniciado, 10-11 Adepto.

**Legenda:** ✅ escrita + enriquecida · 🔶 escrita, falta enriquecer · 📋 desenhada · ⬜ não iniciada.

## Notas

| # | Nota | Fase | Estado | Pendências |
|---|------|------|--------|-----------|
| — | `index.md` | — | ➖ MOC | — |
| 06 | Ignorar arquivos — o `.gitignore` e suas regras | Iniciado | ✅ escrita + M1 | — |
| 07 | Ler o histórico — `log` e `diff` | Iniciado | ✅ escrita + M1 | — |
| 08 | Branches na prática | Iniciado | ✅ escrita + M1 | — |
| 09 | Conflito — por que acontece e como resolver | Iniciado | ✅ escrita + M1 | — |
| 10 | Guardar trabalho pela metade — stash e worktrees | Adepto | ✅ escrita + M1 | — |
| 11 | Sincronizar com o time | Adepto | ✅ escrita + M1 | — |

## Decisões de escrita registradas

- **Material próprio incorporado:** metáfora das múltiplas linhas temporais (`escrita-sem-medo`) na 08; "Resolução de conflitos" (workshop Tomo 7) na 09; múltiplos remotos (workshop Tomo 5) e **pendrive como servidor Git** (curso Tomo 6) na 11 — este último como `[!example]`, e é o melhor exercício do nível.
- **`switch` como forma primária**, com `checkout` explicado como a forma antiga (nota 08).
- **Ordem deliberada 08 → 09:** conflito vem logo depois de branch porque é a consequência direta do merge; adiar geraria medo acumulado.
- **Recomendação contra-corrente na nota 10:** commit "wip" é apresentado como *melhor* que stash na maioria dos casos, e worktree como melhor que ambos quando a interrupção é longa. Justificativa: stash é invisível e a pilha é global.
- **`--force` tratado como interdição neste nível** (nota 11), com `--force-with-lease` apenas nomeado e adiado para o N4. O leitor sai sabendo que forçar não é resolver.
- **`pull --rebase` recomendado sem explicar o mecanismo** (nota 11), com aviso explícito de que a explicação vem no N3. Dívida conceitual assumida e registrada.
- **Dica de escrita acadêmica recorrente:** "uma frase por linha" (nota 07) e "um arquivo por capítulo" (nota 09) — as duas coisas que mais reduzem conflito e melhoram diff em trabalho de texto.

## Ganchos deixados para notas futuras

| Gancho | Nota que quita |
|---|---|
| three-way merge / ancestral comum (09) | 21 — Merge e rebase por dentro |
| a regra de ouro do rebase (11) | 24 — Reescrever história com segurança |
| `--force-with-lease` (11) | 24 |
| reflog para branch apagada com `-D` (08) | 23 — `reflog` |
| segredos no histórico (06) | 25 |
| estratégias de ramificação em equipe (08) | 13 — Estratégias de branching |
| `git blame` / pickaxe (07) | 31 — Ler história de verdade |

## Próximos passos

1. ✅ **M1 — mídia**: completo — todas as notas deste nível têm vídeo embutido e verificado por `yt-dlp`. Estado consolidado do domínio no [[03-Dominios/Tecnologia/Controle de Versão/roadmap|roadmap do domínio]].
2. ✅ **Dicionário do domínio** — criado 2026-07-31; os termos deste nível já entraram.
3. ⬜ `/plantar-duvidas` + `/colher-duvidas` no par N0+N1, que é a unidade compartilhável.
