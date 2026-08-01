---
title: "Infraestrutura"
type: moc
publish: true
created: 2026-05-21
updated: 2026-05-21
status: seedling
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
> Estante de infraestrutura — Docker, Kubernetes, CI/CD, observabilidade, Nginx, Linux, ambientes WSL e plataformas de cloud (Digital Ocean). Material de plataforma e operação.

Esta estante junta o que sustenta as aplicações depois que elas saem da máquina do dev: empacotamento em containers, orquestração, automação de entrega, observabilidade, servidores web/proxy reverso, sistema operacional e provedores de cloud. Cobre também o ambiente local em WSL, usado como ponte entre Windows e Linux.

## Conteúdo

- [[Infraestrutura]] — visão geral da estante
- [[Docker]] — containers e empacotamento
- [[Kubernetes]] — orquestração de containers
- [[CI-CD]] — integração e entrega contínuas
- [[Observabilidade]] — logs, métricas e tracing
- [[Nginx]] — servidor web e proxy reverso
- [[Linux]] — sistema operacional Linux
- [[Terminal]] — uso de terminal
- [[Comandos Docker e WSL]] — comandos práticos de Docker e WSL
- [[Configurando Ambiente Linux no WSL]] — setup de ambiente Linux dentro do WSL
- [[WSL, Docker e Kubernetes]] — integração entre WSL, Docker e Kubernetes
- [[Docker credential helpers]] — credential helpers do Docker
- [[Digital Ocean]] — provedor de cloud Digital Ocean
- [[03-Dominios/Tecnologia/Infraestrutura/Linux/index|Linux (galho)]] — notas operacionais de Linux

> [!info] Git e GitHub saíram desta estante (2026-07-31)
> Esta estante é sobre **o que sustenta a aplicação depois que ela sai da máquina do dev** — containers, orquestração, proxy, SO, provedor. Git é sobre o **histórico do código**, antes de rodar, e por isso ganhou domínio próprio: [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] (7 níveis, do tutorial operacional ao modelo interno). O antigo `GitHub CLI.md` daqui virou a **referência de consulta** daquele domínio, e o capítulo que ensina o fluxo é a nota 16 do nível 2.

## Veja também

- [[03-Dominios/Tecnologia/Terminal/index|Terminal]]
- [[03-Dominios/Tecnologia/Cloud/index|Cloud]]
- [[Senda Devops]]
