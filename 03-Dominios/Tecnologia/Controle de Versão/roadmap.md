---
title: "Roadmap — Controle de Versão"
created: 2026-07-31
updated: 2026-08-01
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Controle de Versão

Roadmap do domínio `03-Dominios/Tecnologia/Controle de Versão` (raiz de domínio / galho-pai). Rastreia o **estado dos sub-galhos**. **DOMÍNIO COMPLETO — escrita 34/34 em 2026-07-31, M1 (mídia) 34/34 em 2026-08-01.** Domínio aberto no mesmo dia (Tier 0); estrutura **revisada** para progressão em 7 níveis (operacional → modelo), após análise do material próprio do autor. Fonte do roster: `index.md` + [[00-Meta/specs/2026-07-31-dominio-controle-de-versao-design|design 2026-07-31]].

**Nível:** raiz de domínio (contém sub-galhos).

**Legenda de estado:** ✅ completo (escrito + enriquecido) · 🔶 em construção · 📋 desenhado, não iniciado · ⬜ só esboçado no design · `%` = notas escritas / total.

## Notas diretas (logo abaixo desta pasta)

| Nota | Tipo | Estado |
|------|------|--------|
| `index.md` | MOC | ➖ não precisa |
| `Biblioteca de Controle de Versão.md` | reference | ✅ criada 2026-07-31 (bloco internacional + bloco PT-BR; links verificados por HTTP) |
| `GitHub CLI.md` | reference | ✅ migrada de `Infraestrutura/` em 2026-07-31 (2006 linhas, `type: reference`); capítulo é a nota 16 |
| `Dicionário de Controle de Versão.md` | glossary | ✅ criado 2026-07-31 (~100 verbetes, 8 seções) |
| `34 - Capstone - assumir um repositório desconhecido.md` | Capstone | ✅ **completo** (escrito 2026-07-31 · M1 2026-08-01) |

## Sub-galhos (ordem de construção = ordem de leitura)

| Nível | Sub-galho | Notas | Escritas | % | Estado | roadmap |
|---|-----------|------:|---------:|--:|--------|---------|
| N0 | Sobrevivência | 5 | 5 | 100% | ✅ **completo** (escrita 2026-07-31 · M1 2026-08-01) | `N0 - Sobrevivência/roadmap.md` |
| N1 | O fluxo diário | 6 | 6 | 100% | ✅ **completo** (escrita 2026-07-31 · M1 2026-08-01) | `N1 - O fluxo diário/roadmap.md` |
| N2 | Colaborar | 5 | 5 | 100% | ✅ **completo** (escrita 2026-07-31 · M1 2026-08-01) | `N2 - Colaborar/roadmap.md` |
| N3 | O modelo por baixo | 5 | 5 | 100% | ✅ **completo** (escrita 2026-07-31 · M1 2026-08-01) | `N3 - O modelo por baixo/roadmap.md` |
| N4 | Quando dá errado | 5 | 5 | 100% | ✅ **completo** (escrita 2026-07-31 · M1 2026-08-01) | `N4 - Quando dá errado/roadmap.md` |
| N5 | Repositórios reais | 4 | 4 | 100% | ✅ **completo** (escrita 2026-07-31 · M1 2026-08-01) | `N5 - Repositórios reais/roadmap.md` |
| N6 | O repositório como testemunha | 3 | 3 | 100% | ✅ **completo** (escrita 2026-07-31 · M1 2026-08-01) | `N6 - O repositório como testemunha/roadmap.md` |

> Ao contrário dos outros domínios do vault, aqui **a ordem de construção é a ordem de leitura**. O material vai ser compartilhado com colegas, então cada nível precisa ser publicável e útil sozinho antes do próximo existir — não dá pra escrever o N6 primeiro.

## Tabela-resumo (agregado)

| Métrica | Valor |
|---------|-------|
| Sub-galhos (níveis) | 7 |
| ✅ completos (escrito + M1) | **7 — todos** |
| 🔶 escritos, falta M1 | **0** |
| 📋 desenhados, não iniciados | **0** |
| Notas totais | 33 + capstone = **34** |
| Notas escritas | **34 (100%)** ✅ |

---

## Material a consumir

### Repositórios próprios do autor (analisados 2026-07-31)

Estrutura pedagógica já validada em sala + diagramas e narrativas próprias. Mapa de aproveitamento **item a item** na spec de design.

| Repo | Ano | Aproveitamento principal |
|---|---|---|
| [`workshop-git`](https://github.com/josenaldo/workshop-git) | 2016 | 9 tomos; **sequência de 9 diagramas de branching** → nota 19; merge×rebase → 21; desfazer → 22; múltiplos remotes → 11; tags → 14 |
| [`curso-git-github`](https://github.com/josenaldo/curso-git-github) | 2017 | narrativa histórica ("O dia em que rasguei o CD") → 01; *"Git só adiciona dados"* + SHA-1 → 17/23; **pendrive como servidor Git** → 11 |
| [`escrita-sem-medo-com-git-e-github`](https://github.com/josenaldo/escrita-sem-medo-com-git-e-github) | 2021 | abertura pelo problema + "EPI" + **"o que o Git NÃO faz"** → 01; **"máquina do tempo com múltiplas linhas temporais"** → 08 |
| [`aprendendo-git-e-github`](https://github.com/josenaldo/aprendendo-git-e-github) | 2023 | mapa de recursos PT-BR → **já incorporado na Biblioteca** |

> [!warning] Ressalvas de atualização
> O material de 2016-17 usa **GitKraken/TortoiseGit** como fio condutor (hoje: CLI + Lazygit → vira menção de uma linha na 02), **`master`** (escrever `main`) e **`git checkout`** pra tudo (ensinar `switch`/`restore`, com `checkout` explicado como o comando antigo que faz as duas coisas). Link do GirlsTechTalkClub está **404** — já removido do mapa.

### Material do vault

| Arquivo | Destino |
|---|---|
| `Ferramentas/Versionamento.md` | ✅ **podado 2026-07-31** — tronco com tabela de redirecionamento; seções de entrevista preservadas |
| `Infraestrutura/GitHub CLI.md` | ✅ **migrado 2026-07-31** para `Controle de Versão/GitHub CLI.md` como referência; Infra com callout de saída |

---

## Próximos passos

1. ✅ **N0 — Sobrevivência** (5 notas): **completo** — escrita 2026-07-31, M1 2026-08-01. Público geral (estudante/acadêmico), exemplos em documentos, não em código.
2. ✅ **N1 — O fluxo diário** (6 notas): **completo** — escrita 2026-07-31, M1 2026-08-01.
3. ✅ **N2 — Colaborar** (5 notas): **completo** — escrita 2026-07-31, M1 2026-08-01. `GitHub CLI.md` migrado e `Versionamento.md` podado.
4. ✅ **N3 — O modelo por baixo** (5 notas): **completo** — escrita 2026-07-31, M1 2026-08-01. Ponto de virada; a sequência de branching do `workshop-git` foi redesenhada em 7 passos Mermaid na nota 19.
5. ✅ **N4 — Quando dá errado** (5 notas): **completo** — escrita 2026-07-31, M1 2026-08-01.
6. ✅ **N5 — Repositórios reais** (4 notas): **completo** — escrita 2026-07-31, M1 2026-08-01.
7. ✅ **N6 — O repositório como testemunha** (3 notas): **completo** — escrita 2026-07-31, M1 2026-08-01.
8. ✅ **Capstone** (34): **escrito 2026-07-31, M1 2026-08-01** — roteiro de 4 horas, costura os 7 níveis.
9. ✅ **M1 — mídia**: **34/34 embutidos e verificados** (25 em 2026-07-31, 9 em 2026-08-01, quando o bloqueio do YouTube caiu). Ver a seção M1 abaixo.
10. ✅ **Dicionário de Controle de Versão** — criado 2026-07-31.
11. ✅ **Ponte de volta**: callouts inseridos em Arqueologia (index, notas 07, 09 e 28) apontando as contrapartes instrumentais.

---

## M1 — mídia (✅ completo em 2026-08-01)

**34 de 34 notas com vídeo embutido e verificado por `yt-dlp`** (título, canal, duração e existência de legenda conferidos no momento da inserção).

As 25 primeiras foram feitas em 2026-07-31; a rodada parou porque o YouTube passou a exigir autenticação (`Sign in to confirm you're not a bot`). Em **2026-08-01 o bloqueio tinha caído** e as **9 restantes** (23, 27-34) foram verificadas e embutidas a partir dos candidatos já levantados. Todos os 13 IDs consultados existiam e tinham legenda `en` — nenhum candidato precisou ser descartado nesta rodada.

| Nota | Vídeo embutido | Canal | Duração |
|---|---|---|---|
| 23 — reflog | `fyhYSl-ACPc` — *How to Recover Lost Commits with Git Reflog* | CodeLucky | 3:39 |
| 27 — Monorepo e polyrepo | `jOVWHIDvpe8` — *Optimize checkout and clone time... sparse-checkout and filter* | Bryant Son | 9:48 |
| 28 — Submódulos e subtrees | `JESI498HSMA` — *Why everyone hates git submodules* | Philomatics | 8:15 |
| 29 — Cirurgia de repositório | `kBMTLIWkYVQ` — *splitting a monorepo with git filter-branch / filter-repo* | anthonywritescode | 16:37 |
| 30 — Git no CI/CD e GitOps | `f5EpcWp0THw` — *What is GitOps, How GitOps works and Why it's so useful* | TechWorld with Nana | 11:33 |
| 31 — Ler história de verdade | `8uuueHkWy-E` — *how I use git blame* | anthonywritescode | 6:09 |
| 32 — bisect | `3cwWssglZuQ` — *Using git bisect to Help Find Which Commit Broke Something* | Nick Janetakis | 14:08 |
| 33 — Forense de repositório | `7FApEq8wum4` — *Treat Your Code as a Crime Scene* | GOTO 2016 (**Adam Tornhill**, autor da fonte da nota) | 48:43 |
| 34 — Capstone | `OzwQXGLWI0g` — *7 Techniques to understand Legacy Code* (Jonathan Boccara) | The Legacy of SoCraTes | 51:04 |

> Candidatos alternativos que ficaram de reserva, caso algum link morra: 23 `NN-8kP7nClA` · 27 `LMG_-uJVdsw`, `RcqLV1lU408` · 28 `8Z4Cmhji_FQ` · 29 `vTguH2ixWLg`, `P5r_jONyuHo` · 30 `dIaX5IhRqkI` · 32 `z-AkSXDqodc` · 33 `ymAyzlgN9_8` · 34 `jqHXJ3O7WGw`. O candidato original da 23, `hsAPjNZHv-E` (Train To Code), segue descartado por não ter legenda pt/en.

**Critérios usados nas 25 primeiras — e mantidos nas 9 finais:** vídeo em **PT-BR** nas notas 01-09 e 14 (público geral / iniciante); inglês a partir do N2, onde o material bom é majoritariamente anglófono. Callout `[!tip]` inserido **antes** do `[!tip] Pratique`, com uma frase dizendo o que aquele vídeo acrescenta à nota — nunca "veja também este vídeo".

> [!important] Convenção de prática (decidida 2026-07-31)
> Toda nota de **N0 a N4** fecha com callout `[!tip] Pratique` apontando pro **nível/exercício específico** da [[03-Dominios/Tecnologia/Controle de Versão/Biblioteca de Controle de Versão|Biblioteca]] — nunca pra home do site. A nota entrega o modelo; o simulador entrega a repetição.
