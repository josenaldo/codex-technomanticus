---
title: "Go — Cloud-native e produção"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - cloud-native
  - deploy
aliases:
  - Galho 18 Go
  - Cloud-native Go
---
# Go — Cloud-native e produção

> [!abstract] TL;DR
> Galho 18 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — por que Go é a linguagem nativa da era dos containers. 8 notas em 3 fases: o binário estático e cross-compilation (Iniciado); build flags/embed, imagens Docker mínimas, graceful shutdown e o contrato com Kubernetes (Adepto); secrets em produção e o pipeline do commit ao deploy (Magus). Ao fim, você empacota e opera um serviço Go como um sênior — imagem de poucos MB, shutdown limpo, probes honestas.

Docker, Kubernetes e Terraform são escritos em Go por um motivo: um binário autocontido de poucos MB é o cidadão perfeito de um container. Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — o artefato

1. [[01 - O binário estático]] — `CGO_ENABLED=0`, static linking, por que Go é ideal para containers
2. [[02 - Cross-compilation]] — `GOOS`/`GOARCH`, compilar para Linux/ARM de qualquer máquina

### Adepto — empacotar e operar

3. [[03 - Build flags e versionamento]] — `-ldflags -X`, `-s -w`, `//go:embed` para assets
4. [[04 - Docker — imagens mínimas]] — multi-stage, distroless e `scratch`, imagem de poucos MB
5. [[05 - Graceful shutdown]] — SIGINT/SIGTERM, `srv.Shutdown(ctx)`, drenar in-flight
6. [[06 - Contrato com Kubernetes]] — liveness/readiness probes, config via env, 12-factor

### Magus — produção de verdade

7. [[07 - Configuração e secrets em produção]] — env vs secrets montados, não logar segredos, reload
8. [[08 - Do commit ao deploy — CI-CD]] — vet/test-race/lint/build no CI, goreleaser, do PR ao cluster

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/17 - Runtime interno/index|Runtime interno]]
- Próximo galho: **Segurança** (galho 19) — crypto, TLS, validação e supply chain em código Go
