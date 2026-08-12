---
title: "Roadmap — Docker"
created: 2026-08-02
updated: 2026-08-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - infraestrutura
  - docker
---

# Roadmap — Docker (galho 1 de Infraestrutura)

Roadmap-folha do galho `Tecnologia/Infraestrutura/Docker`. Primeiro galho do domínio, aberto em 2026-08-02. Design: [[00-Meta/specs/2026-08-02-dominio-infraestrutura-design|design do domínio]] · Plano: [[00-Meta/specs/2026-08-02-galho-docker-plano|plano de execução]].

**Lente:** a imagem como artefato — tudo é consequência de a imagem ser imutável e em camadas.

**Legenda:** ✅ escrita + M1 · 🔶 escrita, falta M1 · 📋 desenhada, não escrita · ⬜ não iniciada.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 18 |
| 📋 desenhadas | 0 |
| 🔶 escritas | 18 |
| ✅ completas | 0 |
| % escrito | **100% (18/18)** ✅ |
| M1 (mídia) | passada posterior, após a escrita |

## Notas

| # | Nota | Fase | Estado | Bloco do plano |
|---|------|------|--------|----------------|
| 01 | O problema que o container resolve | Iniciado | 🔶 | 1 |
| 02 | A anatomia de uma imagem | Iniciado | 🔶 | 1 |
| 03 | O ciclo de vida de um container | Iniciado | 🔶 | 1 |
| 04 | O Dockerfile como receita de camadas | Iniciado | 🔶 | 1 |
| 05 | Build e cache — por que seu build está lento | Iniciado | 🔶 | 2 |
| 06 | Dados que sobrevivem ao container | Iniciado | 🔶 | 2 |
| 07 | Rede no Docker | Iniciado | 🔶 | 2 |
| 08 | ENTRYPOINT, CMD e o container que não morre direito | Adepto | 🔶 | 3 |
| 09 | Multi-stage e imagens mínimas | Adepto | 🔶 | 3 |
| 10 | BuildKit por dentro | Adepto | 🔶 | 3 |
| 11 | Compose como ambiente de desenvolvimento | Adepto | 🔶 | 3 |
| 12 | Registry | Adepto | 🔶 | 4 |
| 13 | Segurança da imagem e do runtime | Adepto | 🔶 | 4 |
| 14 | Debugar um container | Adepto | 🔶 | 4 |
| 15 | Docker por dentro | Magus | 🔶 | 5 |
| 16 | O ecossistema além do Docker | Magus | 🔶 | 5 |
| 17 | Docker em CI e na máquina de dev | Magus | 🔶 | 5 |
| 18 | Capstone — empacotar uma app do zero | Magus | 🔶 | 6 |

## Material a consumir

| Fonte | Onde | Aproveitamento |
|---|---|---|
| `Infraestrutura/Docker.md` | 1298 linhas, `publish: false` | semente principal — rica em código e já organizada por assunto; vira tronco podado no bloco 7 |
| `Infraestrutura/Comandos Docker e WSL.md` | 431 linhas | referência solta de ambiente local; permanece, não vira nota |
| `Infraestrutura/Docker credential helpers.md` | 83 linhas | citado pela nota 12 (registry), permanece como referência |

> [!warning] Regra de conteúdo
> As seções `Na prática (da minha experiência)` e `How to explain in English` do monólito são **relato pessoal do autor e material de entrevista**. Elas ficam no tronco podado e **não migram** para as notas do galho. Nada sobre a experiência do autor pode ser inventado nas notas.

## Fronteiras a respeitar

| Vizinho | Fica lá | Fica aqui |
|---|---|---|
| `Ciência/SO 13` | namespaces, cgroups, runc, OCI, escape de container | como o Docker usa isso; a cadeia daemon → containerd → runc |
| `Operação 3-01` | imagem de produção como disciplina (imutabilidade, digest, política de não-root) | como a imagem é construída; cache; camadas |
| `Cloud 12` | ECS, Fargate, App Platform, Kubernetes gerenciado | o Docker que você mesmo opera |
| `Terminal/TUIs` | Lazydocker e a ergonomia | o que a TUI está manipulando por baixo |
| `Java`/`Go`/`Python` cloud-native | o Dockerfile daquela linguagem | o Dockerfile como mecanismo, agnóstico de stack |
| `Java/Testes 11`, `Testes JS` | Testcontainers como prática de teste | Docker em CI como mecanismo (nota 17) |

## Pendências

- **Escrita:** ✅ **18/18 completa em 2026-08-02** (blocos 1-6 do plano).
- **M1 (mídia):** passada posterior. Busca e verificação de ID **centrais via `yt-dlp`** — nunca delegadas a subagente.
- **Poda do monólito e callouts de volta:** bloco 7 do plano.

## Notas de execução

- Galho aberto em 2026-08-02 como primeiro do domínio Infraestrutura, na sequência direta do fechamento de Controle de Versão.

## M1 — mídia embutida e descartes

**Rodadas de 2026-08-09 e 2026-08-12: 14 de 18 notas (78%).** Todas as transcrições foram baixadas e lidas antes de embutir — a regra deste galho proíbe inserir com metadados apenas, e o candidato da nota 15 esperava exatamente isso desde a passada anterior.

| Nota | Vídeo | ID | Canal | Âncora |
|---|---|---|---|---|
| 02 | Building a Container Image — OCI, UnionFS, Overlay | `hhQ6uc2bp2s` | Ryan Hay, 17 min | 15:05 |
| 05 | How Dockerfile Layers/Caching Work | `RP-z4dqRTZA` | Benjamin Porter, 8 min | — |
| 06 | Docker Volumes explained in 6 minutes | `p2PH_YPCsis` | TechWorld with Nana, 6 min | — |
| 07 | Docker Networking Tutorial (todos os drivers) | `fBRgw5dyBd4` | Anton Putra, 20 min | — |
| 09 | Docker Image BEST Practices — From 1.2GB to 10MB | `t779DVjCKCs` | Better Stack, 7 min | — |
| 10 | BuildKit: A Modern Builder Toolkit on containerd | `yd0lvUXitxY` | CNCF, Tõnis Tiigi & Akihiro Suda, 35 min | — |
| 11 | How To Use Docker To Make Local Development A Breeze | `zkMRWDQV4Tg` | ArjanCodes, 22 min | — |
| 13 | The Route To Rootless Containers | `qXG_cChQgUg` | Container Camp, Claudia Beresford, 30 min | — |
| 15 | Containers From Scratch | `8fi7uSYlOdc` | GOTO 2018, Liz Rice, 43 min | 32:54 |
| 01 | Contêineres, Docker e Kubernetes (**PT-BR**) | `wxLvvMxzc1Q` | HipstersPontoTube/Alura, Giovanni Bassi, 13 min | — |
| 04 | Dockerfile Tutorial — Docker in Practice | `WmcdMiyqfZs` | TechWorld with Nana, 24 min | — |
| 14 | Debugging Docker Containers with exec e logs | `tLK9nNFHWH8` | TechWorld with Nana, 10 min | — |
| 16 | Podman vs Docker in 2026 | `SIvoAOpXZPg` | Better Stack, 6 min | — |
| 17 | docker: fast CI rebuilds with --cache-from | `77j6JFBTmTc` | anthonywritescode, 6 min | — |

> [!info] Duas escolhas que valem registro
> **Nota 10 é fonte primária:** Tõnis Tiigi é o autor do BuildKit. A palestra nomeia o grafo pelo nome do projeto (**LLB**), mostra que o Dockerfile é apenas *um frontend* entre possíveis, e quantifica o argumento da nota com números medidos — 139 s no construtor antigo, 31 s no BuildKit, 3,29 s com cache mount.
>
> **Nota 15 fechou o candidato que estava parado desde a passada anterior.** A palestra da Liz Rice começa exatamente onde a nota para: onde o texto diz *"`runc` chama `clone()`, escreve no cgroup e faz `pivot_root()`"*, ela escreve esse código ao vivo. O ponto de inserção escolhido na passada anterior se confirmou correto.
>
> **Ressalvas de idade registradas dentro dos callouts:** `8fi7uSYlOdc` usa **cgroups v1** e escreve direto em `/sys/fs/cgroup/pids/…` — a hierarquia unificada do v2 é o padrão atual, então os caminhos envelheceram e o conceito não; `yd0lvUXitxY` é anterior ao BuildKit virar o construtor **padrão** do Docker Engine (23.0), então a moldura de "como habilitar" caducou.

## Notas sem vídeo, e por quê

| Nota | Situação |
|---|---|
| 03 — O ciclo de vida de um container | Melhores resultados com 17, 15, 380 e 1.125 visualizações. Sem candidato |
| 08 — ENTRYPOINT, CMD e o container que não morre direito | Resultados com 66, 17 e 7 visualizações; dois em italiano e russo. Assunto excelente, material inexistente. Sem candidato |
| 12 — Registry | `RgZyX-e6W9E` (67 mil views) é sobre publicar no GHCR especificamente, não sobre o mecanismo de registry. Encaixe parcial demais |
| 18 — Capstone | Os candidatos são tutoriais de empacotamento **amarrados a um framework** (.NET, Node, React). Escolher um deles enviesaria um capstone que é deliberadamente agnóstico. `rIrNIzy6U_g` (Fireship, *100+ Docker Concepts*, 1,5 mi de views) foi considerado como revisão geral e reprovado: é enumeração rápida, não percurso |

> [!success] O ângulo PT-BR funcionou na primeira tentativa
> A hipótese estava parada desde o galho Nginx, levantada e nunca testada. A nota 01 tinha só candidatos fracos em inglês — o melhor com 1:39 de duração — e o vídeo do **HipstersPontoTube com Giovanni Bassi** (13 min, 82 mil views) resolveu, com dois exemplos que material em inglês não costuma trazer: a dor de *toolchain* na compilação cruzada para ARM, e rodar uma aplicação .NET de 2002 num container Windows sem instalar nada — este último conversando direto com a seção "Por que aplicações legadas resistem".
>
> **Recomendação para os outros dois galhos:** as notas sem vídeo do Nginx (03, 04, 05, 09, 10, 11, 12, 16) e do Kubernetes (04, 06, 22) nunca foram buscadas em PT-BR. Vale uma rodada antes de declarar ausência de material.
