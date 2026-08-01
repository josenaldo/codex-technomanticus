---
title: "Roadmap — N5 Repositórios reais"
created: 2026-07-31
updated: 2026-08-01
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — N5 Repositórios reais

Roadmap do sub-galho `Controle de Versão/N5 - Repositórios reais` (galho-folha). **Escrita completa em 2026-07-31 — 4/4 notas.** **M1 (mídia) completo em 2026-08-01.**

**Nível:** folha. **Público:** técnico. **Fase:** Magus nas 4.

**Papel no domínio:** o nível de quem herda projeto. Vizinho mais próximo do ofício de legado; peso em "quando NÃO fazer", porque as decisões aqui são caras de reverter.

**Legenda:** ✅ escrita + enriquecida · 🔶 escrita, falta enriquecer · 📋 desenhada.

## Notas

| # | Nota | Estado | Pendências |
|---|------|--------|-----------|
| — | `index.md` | ➖ MOC | — |
| 27 | Monorepo e polyrepo | ✅ escrita + M1 | — |
| 28 | Submódulos e subtrees | ✅ escrita + M1 | — |
| 29 | Cirurgia de repositório | ✅ escrita + M1 | — |
| 30 | Git no CI/CD e GitOps | ✅ escrita + M1 | — |

## Decisões de escrita registradas

- **Nota 27 separa três problemas que costumam ser tratados como um** (histórico grande / árvore grande / binários grandes), cada um com remédio próprio — e trata **clone raso como a resposta errada** para quase tudo, exceto CI, porque amputa `blame`/`bisect`/`describe`. Clone parcial é apresentado como o substituto correto.
- **Nota 27 reformula a pergunta monorepo × polyrepo**: o que decide não é preferência, é quantas mudanças atravessam fronteira de componente por semana.
- **Nota 28 apresenta a terceira opção primeiro na conclusão** — publicar pacote versionado resolve melhor que submódulo ou subtree na maioria dos casos. Submódulo é descrito como "preciso e pouco perdoante", não como ruim.
- **Nota 29 põe a coordenação acima da técnica**: `clone --mirror` antes de tudo, janela combinada, e um `MIGRACAO.md` no repositório resultante — este último é um artefato de arqueologia, deixado deliberadamente para quem herdar o repositório daqui a anos.
- **Nota 30 delimita a fronteira com Operação de forma explícita** (callout `[!info] Onde este domínio para`): aqui só o contrato do lado do repositório; pipeline, deploy, ambientes e operação de Argo CD/Flux ficam em `Engenharia/Operação`. GitOps aparece pelos 4 princípios da CNCF e pelas consequências **para o repositório** (histórico como auditoria, revert como rollback, segredos exigindo resposta explícita).

## Ganchos quitados neste nível

| Gancho aberto em | Quitado por |
|---|---|
| Git LFS e repositórios grandes (25) | 27 |
| bare repo / repositório sem árvore (11) | 29 (via `--mirror`) |
| `--subdirectory-filter` / separar repositório (25) | 29 |
| clone raso e história completa em CI (15) | 30 |
| GitOps e o contrato repo↔pipeline (15) | 30 |
| tag como gatilho de release (14) | 30 |

## Próximos passos

1. ✅ **M1 — mídia**: completo — todas as notas deste nível têm vídeo embutido e verificado por `yt-dlp`. Estado consolidado do domínio no [[03-Dominios/Tecnologia/Controle de Versão/roadmap|roadmap do domínio]].
2. ✅ **Dicionário do domínio** — criado 2026-07-31; os termos deste nível já entraram.
3. ⬜ Avaliar broto sobre **migração SVN→Git em repositório sem `stdlayout`** se o assunto voltar — hoje é um parágrafo na 29.
