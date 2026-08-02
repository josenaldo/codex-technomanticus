---
title: "Infraestrutura"
type: moc
publish: true
created: 2026-05-21
updated: 2026-08-02
status: growing
tags:
  - moc
  - infraestrutura
  - devops
aliases:
  - Estante Infraestrutura
  - Infra
---
# Infraestrutura

> [!abstract] TL;DR
> Domínio das **ferramentas que sustentam a aplicação depois que ela sai da máquina do dev**: Docker, Kubernetes, Nginx e Linux. A lente é *a ferramenta por dentro, para quem já vai operá-la* — não tutorial de comando, mas o mecanismo que permite prever o comportamento. Quatro galhos em construção sequencial; o primeiro, [[03-Dominios/Tecnologia/Infraestrutura/Docker/index|Docker]], fechou a escrita em 2026-08-02 com 18 notas em 3 fases.

## Por que este domínio existe

O vault já operava essas ferramentas sem nunca as ensinar, e dizia isso com todas as letras: [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/01 - Containers em produção|Containers em produção]] abria declarando que assumia que você já sabia escrever um Dockerfile; [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/02 - O contrato de produção do Kubernetes|O contrato de produção do Kubernetes]] assumia Pod, Deployment e Service conhecidos; [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/05 - Rede e borda em produção|Rede e borda em produção]] usava Nginx como Ingress sem ensinar uma linha de configuração de Nginx. Este domínio é esse pressuposto, escrito.

> [!info] Fronteira — o sanduíche de quatro camadas
> A mesma tecnologia aparece em quatro casas do vault, e cada uma responde a uma pergunta diferente. Onde a camada vizinha cobre melhor, aqui se linka em vez de repetir.
>
> | Camada | Casa | Pergunta que responde |
> |---|---|---|
> | Mecanismo | [[03-Dominios/Ciência/Sistemas Operacionais/13 - Virtualização e containers\|Ciência/Sistemas Operacionais]] | como o isolamento funciona no kernel |
> | **A ferramenta** | **este domínio** | **como a ferramenta funciona por dentro** |
> | O ofício | [[03-Dominios/Engenharia/Operação/index\|Engenharia/Operação]] | o que muda quando é produção |
> | A plataforma | [[03-Dominios/Tecnologia/Cloud/index\|Tecnologia/Cloud]] | quando alguém gerencia por você |

## Galhos

| Galho | Lente | Estado |
|---|---|---|
| [[03-Dominios/Tecnologia/Infraestrutura/Docker/index\|Docker]] | a imagem como artefato | ✅ **escrita completa 2026-08-02** — 18 notas, 3 fases; falta M1 (mídia) |
| Kubernetes | o loop de reconciliação | 📋 desenhado, não iniciado — ~22-25 notas |
| Nginx | o ciclo de vida de uma request | 📋 desenhado, não iniciado — ~10-12 notas |
| [[03-Dominios/Tecnologia/Infraestrutura/Linux/index\|Linux]] | o sistema como o processo o vê | 🔶 stub (1 nota) — reforma prevista, ~15-18 notas |

A ordem de construção é **Docker → Kubernetes → Nginx → Linux**: o pré-requisito conceitual vem antes, e a base absoluta fica por último, porque é a que mais se sobrepõe a [[03-Dominios/Tecnologia/Terminal/index|Terminal]] e a Ciência, e se beneficia de ter as outras fronteiras já cravadas. Ver o [[00-Meta/specs/2026-08-02-dominio-infraestrutura-design|design do domínio]] e o [[03-Dominios/Tecnologia/Infraestrutura/roadmap|roadmap]].

## Troncos podados

Notas de referência que já foram monólitos e hoje redirecionam para os galhos ou para a casa canônica do assunto.

- [[03-Dominios/Tecnologia/Infraestrutura/Docker.md|Docker (tronco)]] — podado em 2026-08-02; preserva o relato de experiência do autor e o material de articulação em inglês
- [[Kubernetes]] · [[Nginx]] · [[Linux]] — ainda monólitos, sementes dos galhos 2, 3 e 4
- [[CI-CD]] e [[Observabilidade]] — apontam para [[03-Dominios/Engenharia/Operação/index|Engenharia/Operação]], casa canônica da *prática* (decisão de 2026-07-08)
- [[Digital Ocean]] — aponta para [[03-Dominios/Tecnologia/Cloud/index|Cloud]], galho 22
- [[Terminal]] — aponta para [[03-Dominios/Tecnologia/Terminal/index|Tecnologia/Terminal]]
- [[Infraestrutura]] — a antiga visão geral da estante, absorvida por este índice

## Referências de ambiente local

Material de configuração de máquina, que não vira galho e permanece como consulta.

- [[Comandos Docker e WSL]] · [[Configurando Ambiente Linux no WSL]] · [[WSL, Docker e Kubernetes]] · [[Docker credential helpers]]

> [!info] Git e GitHub saíram desta estante (2026-07-31)
> Esta estante é sobre **o que sustenta a aplicação depois que ela sai da máquina do dev** — containers, orquestração, proxy, SO, provedor. Git é sobre o **histórico do código**, antes de rodar, e por isso ganhou domínio próprio: [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] (7 níveis, do tutorial operacional ao modelo interno). O antigo `GitHub CLI.md` daqui virou a **referência de consulta** daquele domínio, e o capítulo que ensina o fluxo é a nota 16 do nível 2.

## Veja também

- [[03-Dominios/Tecnologia/Terminal/index|Terminal]] — a ergonomia do shell; aqui é o sistema por baixo dele
- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] — a mesma tecnologia, gerenciada por um provedor
- [[03-Dominios/Engenharia/Operação/index|Engenharia/Operação]] — o ofício de rodar isso em produção
- [[Senda Devops]]
