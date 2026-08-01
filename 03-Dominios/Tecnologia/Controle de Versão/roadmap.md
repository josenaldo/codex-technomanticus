---
title: "Roadmap — Controle de Versão"
created: 2026-07-31
updated: 2026-07-31
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Controle de Versão

Roadmap do domínio `03-Dominios/Tecnologia/Controle de Versão` (raiz de domínio / galho-pai). Rastreia o **estado dos sub-galhos**. **ESCRITA COMPLETA — 34/34 notas em 2026-07-31.** Domínio aberto no mesmo dia (Tier 0); estrutura **revisada** para progressão em 7 níveis (operacional → modelo), após análise do material próprio do autor. Fonte do roster: `index.md` + [[00-Meta/specs/2026-07-31-dominio-controle-de-versao-design|design 2026-07-31]].

**Nível:** raiz de domínio (contém sub-galhos).

**Legenda de estado:** ✅ completo (escrito + enriquecido) · 🔶 em construção · 📋 desenhado, não iniciado · ⬜ só esboçado no design · `%` = notas escritas / total.

## Notas diretas (logo abaixo desta pasta)

| Nota | Tipo | Estado |
|------|------|--------|
| `index.md` | MOC | ➖ não precisa |
| `Biblioteca de Controle de Versão.md` | reference | ✅ criada 2026-07-31 (bloco internacional + bloco PT-BR; links verificados por HTTP) |
| `GitHub CLI.md` | reference | ✅ migrada de `Infraestrutura/` em 2026-07-31 (2006 linhas, `type: reference`); capítulo é a nota 16 |
| `Dicionário de Controle de Versão.md` | glossary | ✅ criado 2026-07-31 (~100 verbetes, 8 seções) |
| `34 - Capstone - assumir um repositório desconhecido.md` | Capstone | 🔶 **escrito 2026-07-31** (falta M1) |

## Sub-galhos (ordem de construção = ordem de leitura)

| Nível | Sub-galho | Notas | Escritas | % | Estado | roadmap |
|---|-----------|------:|---------:|--:|--------|---------|
| N0 | Sobrevivência | 5 | 5 | 100% | 🔶 **escrita completa 2026-07-31** (falta M1) | `N0 - Sobrevivência/roadmap.md` |
| N1 | O fluxo diário | 6 | 6 | 100% | 🔶 **escrita completa 2026-07-31** (falta M1) | `N1 - O fluxo diário/roadmap.md` |
| N2 | Colaborar | 5 | 5 | 100% | 🔶 **escrita completa 2026-07-31** (falta M1) | `N2 - Colaborar/roadmap.md` |
| N3 | O modelo por baixo | 5 | 5 | 100% | 🔶 **escrita completa 2026-07-31** (falta M1) | `N3 - O modelo por baixo/roadmap.md` |
| N4 | Quando dá errado | 5 | 5 | 100% | 🔶 **escrita completa 2026-07-31** (falta M1) | `N4 - Quando dá errado/roadmap.md` |
| N5 | Repositórios reais | 4 | 4 | 100% | 🔶 **escrita completa 2026-07-31** (falta M1) | `N5 - Repositórios reais/roadmap.md` |
| N6 | O repositório como testemunha | 3 | 3 | 100% | 🔶 **escrita completa 2026-07-31** (falta M1) | `N6 - O repositório como testemunha/roadmap.md` |

> Ao contrário dos outros domínios do vault, aqui **a ordem de construção é a ordem de leitura**. O material vai ser compartilhado com colegas, então cada nível precisa ser publicável e útil sozinho antes do próximo existir — não dá pra escrever o N6 primeiro.

## Tabela-resumo (agregado)

| Métrica | Valor |
|---------|-------|
| Sub-galhos (níveis) | 7 |
| ✅ completos (escrito + M1) | 0 |
| 🔶 escritos, falta M1 | **7 — todos** |
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

1. ✅ **N0 — Sobrevivência** (5 notas): **escrita completa 2026-07-31**. Público geral (estudante/acadêmico), exemplos em documentos, não em código. Falta só M1.
2. ✅ **N1 — O fluxo diário** (6 notas): **escrita completa 2026-07-31**. Falta só M1.
3. ✅ **N2 — Colaborar** (5 notas): **escrita completa 2026-07-31**. `GitHub CLI.md` migrado e `Versionamento.md` podado. Falta só M1.
4. ✅ **N3 — O modelo por baixo** (5 notas): **escrita completa 2026-07-31**. Ponto de virada; a sequência de branching do `workshop-git` foi redesenhada em 7 passos Mermaid na nota 19. Falta só M1.
5. ✅ **N4 — Quando dá errado** (5 notas): **escrita completa 2026-07-31**. Falta só M1.
6. ✅ **N5 — Repositórios reais** (4 notas): **escrita completa 2026-07-31**.
7. ✅ **N6 — O repositório como testemunha** (3 notas): **escrita completa 2026-07-31**.
8. ✅ **Capstone** (34): **escrito 2026-07-31** — roteiro de 4 horas, costura os 7 níveis.
9. 🔶 **M1 — mídia**: **25/34 embutidos e verificados**; 9 pendentes por bloqueio do YouTube — candidatos levantados na seção M1 abaixo.
10. ✅ **Dicionário de Controle de Versão** — criado 2026-07-31.
11. ✅ **Ponte de volta**: callouts inseridos em Arqueologia (index, notas 07, 09 e 28) apontando as contrapartes instrumentais.

---

## M1 — mídia (estado em 2026-07-31)

**25 de 34 notas com vídeo embutido e verificado por `yt-dlp`** (título, canal, duração e existência de legenda conferidos no momento da inserção). Notas 01-22, 24, 25 e 26.

**9 pendentes.** A verificação foi interrompida porque o YouTube passou a exigir autenticação (`Sign in to confirm you're not a bot`) após o volume de consultas. Os candidatos abaixo **já foram levantados por busca**, mas **não foram verificados** — não embutir sem passar o gate de `yt-dlp` (título + legenda), sob risco de link morto.

| Nota | Candidatos (ordem de preferência) |
|---|---|
| 23 — reflog | `fyhYSl-ACPc` (CodeLucky) · `NN-8kP7nClA` (Shakil Tech) · `8g8He9xl2yw` (Sachin Walia) — o candidato original `hsAPjNZHv-E` (Train To Code) **foi descartado: sem legenda pt/en** |
| 27 — Monorepo e polyrepo | `jOVWHIDvpe8` (Bryant Son, sparse-checkout + filter) · `LMG_-uJVdsw` (GitLab) · `RcqLV1lU408` (GitHub Universe 2020) |
| 28 — Submódulos e subtrees | `JESI498HSMA` (Philomatics, *Why everyone hates git submodules*) · `8Z4Cmhji_FQ` (GitKraken) |
| 29 — Cirurgia de repositório | `kBMTLIWkYVQ` (anthonywritescode, split com filter-repo) · `vTguH2ixWLg` (Foxenj) · `P5r_jONyuHo` (Dan Gitschooldude) |
| 30 — Git no CI/CD e GitOps | `f5EpcWp0THw` (TechWorld with Nana) · `dIaX5IhRqkI` (DevOps Journey) |
| 31 — Ler história de verdade | `8uuueHkWy-E` (anthonywritescode, *how I use git blame*) · `z3oJjQvg3mQ` · `OH3w6RBXgEE` |
| 32 — bisect | `3cwWssglZuQ` (Nick Janetakis) · `z-AkSXDqodc` (GitKraken) |
| 33 — Forense de repositório | `7FApEq8wum4` (GOTO 2016, **Adam Tornhill** — o autor da fonte da nota) · `ymAyzlgN9_8` (Pure Performance, com Tornhill) |
| 34 — Capstone | `OzwQXGLWI0g` (Boccara, *7 Techniques to understand Legacy Code*) · `jqHXJ3O7WGw` (ForrestKnight) |

**Critérios usados nas 25 já embutidas:** vídeo em **PT-BR** nas notas 01-09 e 14 (público geral / iniciante); inglês a partir do N2, onde o material bom é majoritariamente anglófono. Callout `[!tip]` inserido **antes** do `[!tip] Pratique`, com uma frase dizendo o que aquele vídeo acrescenta à nota — nunca "veja também este vídeo".

> [!important] Convenção de prática (decidida 2026-07-31)
> Toda nota de **N0 a N4** fecha com callout `[!tip] Pratique` apontando pro **nível/exercício específico** da [[03-Dominios/Tecnologia/Controle de Versão/Biblioteca de Controle de Versão|Biblioteca]] — nunca pra home do site. A nota entrega o modelo; o simulador entrega a repetição.
