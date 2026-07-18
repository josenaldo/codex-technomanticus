---
title: "Go — Microservices e arquitetura"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - arquitetura
  - microservices
  - design
aliases:
  - Galho 14 Go
---
# Go — Microservices e arquitetura

> [!abstract] TL;DR
> Galho 14 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — sai do "sei escrever um handler" pra "sei estruturar um serviço". 8 notas em 3 fases: project layout idiomático (Iniciado); organização interna, injeção de dependência, configuração e arquitetura hexagonal/clean (Adepto); resiliência, comunicação entre serviços e a síntese de um serviço bem estruturado (Magus). Ao fim, você monta o esqueleto de um microserviço Go de produção, não só suas peças isoladas.

Os galhos anteriores deram os ingredientes — HTTP, persistência, gRPC, mensageria. Este galho é sobre arrumação: como organizar pacotes, injetar dependências sem framework mágico, isolar domínio de infraestrutura, e fazer chamadas entre serviços que não quebram no primeiro timeout. Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — o esqueleto

1. [[01 - Project layout — cmd, internal, pkg]] — convenção `cmd/`, `internal/`, `pkg/`, por que Go não tem "framework de projeto"

### Adepto — organizando o serviço

2. [[02 - Organizando um serviço]] — separação por camada vs por feature, onde mora cada coisa
3. [[03 - Dependency injection]] — injeção manual via construtor, sem container mágico, interfaces como pontos de extensão
4. [[04 - Configuração]] — env vars, flags, arquivos, precedência e validação de config
5. [[05 - Arquitetura hexagonal e clean em Go]] — ports & adapters, domínio isolado de infra, idiomatismo Go vs pureza arquitetural

### Magus — comunicação e síntese

6. [[06 - Resiliência — circuit breaker, retry, timeout]] — falhas em cascata, backoff, quando parar de tentar
7. [[07 - Comunicação entre serviços]] — sync vs async, HTTP vs gRPC vs fila, contratos entre serviços
8. [[08 - Um serviço bem estruturado]] — síntese: um esqueleto completo juntando as notas anteriores

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/13 - Mensageria/index|Mensageria]]
- Próximo galho: **Testes** (galho 15) — onde esse esqueleto ganha cobertura e confiança
