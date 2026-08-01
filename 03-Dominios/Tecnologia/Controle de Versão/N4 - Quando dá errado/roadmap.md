---
title: "Roadmap — N4 Quando dá errado"
created: 2026-07-31
updated: 2026-08-01
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — N4 Quando dá errado

Roadmap do sub-galho `Controle de Versão/N4 - Quando dá errado` (galho-folha). **Escrita completa em 2026-07-31 — 5/5 notas.** **M1 (mídia) completo em 2026-08-01.**

**Nível:** folha (uma entrada por nota). **Público:** técnico. **Fase:** Magus nas 5.

**Papel no domínio:** o nível de emergência. Escrito para ser útil sob pânico — cada nota abre pelo sintoma e dá a resposta antes da explicação.

**Legenda:** ✅ escrita + enriquecida · 🔶 escrita, falta enriquecer · 📋 desenhada · ⬜ não iniciada.

## Notas

| # | Nota | Estado | Pendências |
|---|------|--------|-----------|
| — | `index.md` | ➖ MOC | — |
| 22 | A árvore de decisão do desfazer | ✅ escrita + M1 | — |
| 23 | `reflog` — nada se perde de fato | ✅ escrita + M1 | — |
| 24 | Reescrever história com segurança | ✅ escrita + M1 | — |
| 25 | Segredos no histórico | ✅ escrita + M1 | — |
| 26 | Configurar o Git a seu favor | ✅ escrita + M1 | — |

## Decisões de escrita registradas

- **Nota 25 inverte a prioridade que a maioria dos tutoriais ensina:** a primeira ação num vazamento é **rotacionar**, não limpar o histórico. A limpeza é apresentada como higiene/conformidade, não como medida de segurança — com a justificativa de que ela é cara, disruptiva e não alcança cópias, forks e o cache da plataforma. Inclui o fato pouco conhecido de que o GitHub mantém os objetos acessíveis até chamado no suporte.
- **`filter-branch` desaconselhado explicitamente** em favor de `git filter-repo` (posição da própria documentação do Git).
- **O furo do `--force-with-lease` documentado** (nota 24): um `fetch` em segundo plano — comum em IDEs — atualiza a referência remota e neutraliza a proteção. Solução: `--force-if-includes`, aplicado automaticamente desde o Git 2.30 quando `--force-with-lease` é usado sem argumento.
- **Nota 24 desaconselha reescrever durante revisão aberta** — comentários de PR perdem a âncora e o "ver o que mudou desde a última revisão" quebra. Encaminha para squash no merge (nota 12).
- **Nota 23 quantifica a janela de recuperação** (90 / **30** / 14 dias) em vez de dizer "por um tempo", e ensina a regra de resgate: no pânico, use só comandos que **acrescentam** ponteiro (`switch -c`, `branch`, `tag`), nunca `reset`.
- **Nota 26 fecha um buraco aberto na nota 01:** `textconv` no `.gitattributes` faz o Git gerar diff legível de `.docx` e PDF. A limitação anunciada no início do domínio ganha solução no fim — deliberado, e vale manter se as notas forem reordenadas.

## Ganchos quitados neste nível

| Gancho aberto em | Quitado por |
|---|---|
| árvore de decisão do desfazer (04, 20) | 22 |
| reflog e objetos órfãos (17, 18, 19, 21, 22) | 23 |
| `fsck --lost-found` (18, 20) | 23 |
| `--force-with-lease` (11) | 24 |
| a regra de ouro na prática (11, 21) | 24 |
| `git add -p` → commit atômico (14) | 24 (via `--fixup`) |
| segredos no histórico (06, 15) | 25 |
| "ignorar não é proteger" (06) | 25 |
| blob grande inchando o repo (17) | 25 |
| `rerere` e config a favor (21) | 26 |
| hooks como mecanismo do Git (26 vs Tooling e Build) | 26 |
| "o Git não compara Word/PDF" (01) | 26 (`textconv`) |

## Ganchos ainda abertos daqui

| Gancho | Nota que quita |
|---|---|
| `--subdirectory-filter` / separar repositório (25) | 29 — Cirurgia de repositório |
| `bisect` para achar o commit que quebrou (24, via `--exec`) | 32 |
| Git LFS e repositórios grandes (25) | 27 |

## Próximos passos

1. ✅ **M1 — mídia**: completo — todas as notas deste nível têm vídeo embutido e verificado por `yt-dlp`. Estado consolidado do domínio no [[03-Dominios/Tecnologia/Controle de Versão/roadmap|roadmap do domínio]].
2. ✅ **Dicionário do domínio** — criado 2026-07-31; os termos deste nível já entraram.
3. ⬜ Avaliar um broto sobre **assinatura de commits** (GPG/SSH/Sigstore) — hoje aparece só de passagem na 24 e na 26.
