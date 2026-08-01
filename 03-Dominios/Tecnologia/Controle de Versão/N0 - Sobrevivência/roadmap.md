---
title: "Roadmap — N0 Sobrevivência"
created: 2026-07-31
updated: 2026-08-01
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — N0 Sobrevivência

Roadmap do sub-galho `Controle de Versão/N0 - Sobrevivência` (galho-folha). **Escrita completa em 2026-07-31 — 5/5 notas.** **M1 (mídia) completo em 2026-08-01.**

**Nível:** folha (uma entrada por nota).

**Público:** geral — estudante/acadêmico que precisa parar de perder arquivos. Não pressupõe programação. Exemplos primários em documentos (`.docx`, `.tex`, `.bib`), não em código.

**Legenda:** ✅ escrita + enriquecida · 🔶 escrita, falta enriquecer · 📋 desenhada · ⬜ não iniciada.

## Notas

| # | Nota | Linhas | Estado | Pendências |
|---|------|-------:|--------|-----------|
| — | `index.md` | 40 | ➖ MOC | — |
| 01 | O problema que o Git resolve | ~300 | ✅ escrita + M1 | — |
| 02 | Instalar e configurar o Git | ~200 | ✅ escrita + M1 | — |
| 03 | Seu primeiro repositório | ~215 | ✅ escrita + M1 | — |
| 04 | Desfazer sem susto | ~180 | ✅ escrita + M1 | — |
| 05 | GitHub — colocar o repositório na nuvem | ~210 | ✅ escrita + M1 | — |

## Decisões de escrita registradas

- **Notas mais curtas que a régua do vault (~440-540 linhas), de propósito.** O público é iniciante e não-programador; densidade acima disso vira barreira. O padrão capítulo é mantido (abertura-problema, mecanismo, armadilhas, ponte), só que com escopo menor por nota.
- **Callout `[!tip] Pratique` em todas as 5**, apontando pro exercício específico (Learn Git Branching PT-BR níveis 1-2, Visualizing Git, GitHub Skills) — nunca pra home do site.
- **`main`, `switch`/`restore`** em vez de `master`/`checkout`, com nota explicando que material antigo (inclusive o do autor) usa a forma antiga.
- **Terminal apresentado como escolha, não pressuposto** — GUIs mencionadas com a justificativa honesta de por que o material ensina comandos.
- **Segurança tratada sem alarmismo**: o único comando genuinamente perigoso do nível (`git restore` sem `--staged`) tem callout dedicado; o resto é apresentado como reversível.
- **Ganchos deixados de propósito** para notas futuras: `.gitignore` (06) citado como solução em 3 armadilhas; árvore de decisão do desfazer (22); reflog (23); segredos no histórico (25); Git LFS (27); regra de ouro do rebase (24).

## Próximos passos

1. ✅ **M1 — mídia**: completo — todas as notas deste nível têm vídeo embutido e verificado por `yt-dlp`. Estado consolidado do domínio no [[03-Dominios/Tecnologia/Controle de Versão/roadmap|roadmap do domínio]].
2. ✅ **Dicionário do domínio** — criado 2026-07-31; os termos deste nível já entraram.
3. ⬜ Passada de `/plantar-duvidas` + `/colher-duvidas` depois que o N1 existir — o teste real do N0 é ser lido por alguém que nunca usou Git.
