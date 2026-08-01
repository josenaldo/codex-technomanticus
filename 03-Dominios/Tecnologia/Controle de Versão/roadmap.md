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
| `Dicionário de Controle de Versão.md` | glossary | ⬜ pendente — termos do N0 já prontos pra virar verbetes |
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
9. ⬜ **M1 — mídia** (vídeo YouTube com legenda verificada por nota) — **única pendência de construção do domínio**.
10. ⬜ **Dicionário de Controle de Versão** — os termos de todos os níveis.
11. ⬜ **Ponte de volta**: callouts em `Engenharia/Arqueologia e Restauração de Software` apontando o N6 como instrumental.

> [!important] Convenção de prática (decidida 2026-07-31)
> Toda nota de **N0 a N4** fecha com callout `[!tip] Pratique` apontando pro **nível/exercício específico** da [[03-Dominios/Tecnologia/Controle de Versão/Biblioteca de Controle de Versão|Biblioteca]] — nunca pra home do site. A nota entrega o modelo; o simulador entrega a repetição.
