---
title: "Roadmap — N2 Colaborar"
created: 2026-07-31
updated: 2026-07-31
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — N2 Colaborar

Roadmap do sub-galho `Controle de Versão/N2 - Colaborar` (galho-folha). **Escrita completa em 2026-07-31 — 5/5 notas.** Falta enriquecimento de mídia (M1).

**Nível:** folha (uma entrada por nota).

**Público:** equipe de software (o estreitamento anunciado desde o N0 se completa aqui). Fase: Adepto nas 5.

**Legenda:** ✅ escrita + enriquecida · 🔶 escrita, falta enriquecer · 📋 desenhada · ⬜ não iniciada.

## Notas

| # | Nota | Estado | Pendências |
|---|------|--------|-----------|
| — | `index.md` | ➖ MOC | — |
| 12 | Pull requests e a cultura de code review | 🔶 escrita | M1 |
| 13 | Estratégias de branching | 🔶 escrita | M1 |
| 14 | Anatomia de um bom commit | 🔶 escrita | M1 |
| 15 | GitHub como plataforma | 🔶 escrita | M1 |
| 16 | `gh` CLI e automação do fluxo | 🔶 escrita | M1 |

## Monólitos consumidos neste bloco

| Monólito | Destino | Feito |
|---|---|---|
| `Tecnologia/Infraestrutura/GitHub CLI.md` (45K, 2006 linhas) | **movido** para `Controle de Versão/GitHub CLI.md`, `type: reference`, com callout no topo apontando pra nota 16 como capítulo. Filename preservado, então os shortlinks `[[GitHub CLI]]` do vault continuam resolvendo. Infra ganhou callout de saída no `index.md` e no `Infraestrutura.md` | ✅ |
| `Tecnologia/Ferramentas/Versionamento.md` (9.8K) | **podado** para tronco: callout + tabela "para onde foi cada coisa" (12 linhas de redirecionamento). **Preservadas** as seções "Na prática (da minha experiência)" e "How to explain in English" — material de entrevista, não de trilha, e o domínio novo não incorpora relato pessoal do autor | ✅ |

## Decisões de escrita registradas

- **Nota 12 aposta em "tamanho é o fator dominante"** como tese central, com tabela de faixas de linhas. É a única afirmação do nível apoiada em estudo empírico (SmartBear/Cisco) e a que mais muda prática.
- **Nota 13 trata Git Flow com respeito**, não como piada: explica por que existiu, por que caiu em desuso, e — pela lente do consultor de legado — o que fazer ao encontrá-lo (perguntar *"o que hoje ainda depende disso?"*, não *"por que usam isso?"*). Inclui a seção "o que você vai encontrar no legado" com o diagnóstico `git branch -r --sort=-committerdate`.
- **Nota 14 desaconselha Conventional Commits sem automação** — armadilha explícita de "cerimônia vazia". E apresenta `git add -p` como o comando que torna commit atômico viável na prática.
- **Nota 15 para na fronteira de Operação**: Actions aparece só como *contrato do repositório* (eventos, checkout raso, permissões de token, tag→release); pipeline, deploy e ambientes ficam em `Engenharia/Operação`. Também traz `CITATION.cff`, que serve o público acadêmico herdado do N0.
- **Nota 16 é capítulo, não catálogo** — o catálogo é a referência migrada. Destaque para `gh pr checkout` como o comando que transforma revisão de leitura em revisão de execução.

## Ganchos deixados para notas futuras

| Gancho | Nota que quita |
|---|---|
| rebase como mecanismo (12, 13) | 21 — Merge e rebase por dentro |
| clone raso e histórico completo em CI (15) | 30 — Git no CI/CD e GitOps |
| segredo vazado → rotação (15) | 25 — Segredos no histórico |
| `git add -p` e reescrita de história (14) | 24 — Reescrever história com segurança |
| ramos fósseis no legado (13) | 31/33 — ler história e forense |

## Próximos passos

1. ⬜ **M1 — mídia**: 1 vídeo YouTube com legenda verificada (yt-dlp) por nota. Aqui pode ser em inglês, dado o público.
2. ⬜ **Dicionário do domínio**: PR, code review, squash, trunk-based, semver, Conventional Commits, ruleset, CODEOWNERS.
3. ⬜ Avaliar se a referência `GitHub CLI.md` merece uma passada de atualização (é de abril/2026 e o `gh` muda rápido).
