---
title: "Roadmap — Infraestrutura"
created: 2026-08-02
updated: 2026-08-08
type: meta
publish: false
tags:
  - meta
  - roadmap
  - infraestrutura
---

# Roadmap — Infraestrutura

Roadmap do domínio `03-Dominios/Tecnologia/Infraestrutura` (raiz de domínio / galho-pai). Rastreia o **estado dos galhos**. Domínio aberto como **Tier 2** em 2026-08-02, com escopo já fechado desde 2026-07-31 (a sessão que tirou Git daqui e o promoveu a domínio próprio). Design: [[00-Meta/specs/2026-08-02-dominio-infraestrutura-design|design do domínio]].

**Nível:** raiz de domínio (contém galhos).

**Lente do domínio:** a ferramenta por dentro, para quem já vai operá-la — o mecanismo que permite prever o comportamento, não o tutorial de comando.

**Legenda:** ✅ completo (escrito + M1) · 🔶 escrito, falta M1 · 📋 desenhado, não iniciado · ⬜ stub.

## Galhos (ordem de construção)

| # | Galho | Lente | Notas | Escritas | Estado | roadmap |
|---|-------|-------|------:|---------:|--------|---------|
| 1 | Docker | a imagem como artefato | 18 | 18 | 🔶 **escrita completa 2026-08-02** (falta M1) | `Docker/roadmap.md` |
| 2 | Kubernetes | o loop de reconciliação | 22 | 22 | 🔶 **escrita completa 2026-08-04** (falta M1) | `Kubernetes/roadmap.md` |
| 3 | Nginx | o ciclo de vida de uma request | 16 | 16 | 🔶 **escrita completa 2026-08-08** (falta M1) | `Nginx/roadmap.md` |
| 4 | Linux | o sistema como o processo o vê | 16 | 9 | 🔶 **aberto 2026-08-12** — blocos 1-4 escritos (01-09) | `Linux/roadmap.md` |

A ordem coloca o pré-requisito conceitual antes (Docker antes de Kubernetes) e a base absoluta por último: Linux é o galho que mais se sobrepõe a Terminal e a Ciência/SO, e se beneficia de ser escrito depois que os outros três cravaram suas fronteiras.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Galhos | 4 |
| ✅ completos (escrito + M1) | 0 |
| 🔶 escritos, falta M1 | 3 (Docker, Kubernetes, Nginx) |
| 📋 desenhados, não iniciados | 0 |
| 🔶 em construção | 1 (Linux, 9/16) |
| Notas escritas | 56 de ~71-74 previstas |

## Contrato de fronteira

O sanduíche de quatro camadas é normativo para todos os galhos e está reproduzido no `index.md` do domínio e no de cada galho.

| Camada | Casa | Pergunta |
|---|---|---|
| Mecanismo | `Ciência/Sistemas Operacionais 13` | como o isolamento funciona no kernel |
| **A ferramenta** | **este domínio** | como a ferramenta funciona por dentro |
| O ofício | `Engenharia/Operação` | o que muda quando é produção |
| A plataforma | `Tecnologia/Cloud 12` | quando alguém gerencia por você |

A fronteira é renegociada **nota a nota, não em bloco**: onde a vizinha já disse melhor, linka-se; onde ela pressupõe, preenche-se aqui e ela ganha callout de volta.

## Estado dos monólitos

| Arquivo | Linhas originais | Estado |
|---|---:|---|
| `Docker.md` | 1298 | ✅ **podado 2026-08-02** → 174 linhas; preserva `Na prática (da minha experiência)` e `How to explain in English` |
| `Kubernetes.md` | 1612 | ✅ **podado 2026-08-04** → 222 linhas |
| `Nginx.md` | 1285 | ✅ **podado 2026-08-08** → 198 linhas; preserva `Na prática (da minha experiência)` e `How to explain in English` |
| `Linux.md` | 1118 | semente do galho 4, intacto |
| `CI-CD.md` | 1309 | fica podado apontando para Operação (decisão de 2026-07-08) |
| `Observabilidade.md` | 1407 | idem |
| `Infraestrutura.md` | 46 | absorvido pelo `index.md` |

## Pendências

- **Galhos 1-3 (Docker, Kubernetes, Nginx):** M1 (mídia) — passada posterior, com busca e verificação de ID **centrais via `yt-dlp`**, nunca delegadas a subagente. São 56 notas.
- **Galho 4 (Linux):** ✅ **aberto em 2026-08-12** com [[00-Meta/specs/2026-08-12-galho-linux-design|spec de design própria]] — levantamento de fronteira contra **quatro** vizinhos (Ciência/SO, Terminal, Operação e os galhos 1-3 deste domínio), roster de 16 notas em 3 fases, construção em 7 blocos. **Bloco 1 escrito** (01-03). A regra dura do galho: nenhuma nota reabre mecanismo de kernel — linka e segue.
- **Artefatos de domínio:** `Dicionário de Infraestrutura` e `Biblioteca de Infraestrutura` — criar quando os quatro galhos estiverem escritos e o vocabulário estabilizado.

## Notas de execução

- Domínio aberto em 2026-08-02, na sequência direta do fechamento de Controle de Versão.
- **O achado que definiu a lente:** o levantamento de fronteira, feito antes do roster, mostrou que o vault já operava essas ferramentas declarando explicitamente que não as ensinava. O domínio é esse pressuposto, escrito.
- Galho 1 executado em 7 blocos com gate por bloco, subagentes Sonnet (teto de 3 por bloco) e duas paradas de revisão. Plano em [[00-Meta/specs/2026-08-02-galho-docker-plano|plano do galho Docker]].
