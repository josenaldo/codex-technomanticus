---
title: "Go — gRPC e protobuf"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - grpc
  - protobuf
  - rpc
aliases:
  - Galho 12 Go
---
# Go — gRPC e protobuf

> [!abstract] TL;DR
> Galho 12 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — RPC binário e tipado como alternativa ao REST/JSON. 7 notas em 3 fases: por que gRPC e Protocol Buffers como IDL (Iniciado); geração de código, servidor/cliente e os 4 modos de streaming (Adepto); interceptors/metadata/erros e operar gRPC em produção (Magus). Ao fim, você desenha e opera serviços gRPC em Go com contrato versionado e streaming bidirecional.

Go é a linguagem nativa do gRPC — o próprio framework nasceu no Google lado a lado com Go, e o ecossistema (protoc-gen-go, grpc-go) é o mais maduro entre todas as linguagens. Este galho troca o contrato solto de JSON/REST por um contrato forte em `.proto`, com serialização binária eficiente e streaming de primeira classe. Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — o contrato

1. [[01 - Por que gRPC e onde Go brilha]] — HTTP/2, binário vs texto, quando gRPC vale a troca por REST/JSON
2. [[02 - Protocol Buffers]] — sintaxe `.proto`, tipos escalares, mensagens aninhadas, evolução de schema

### Adepto — construindo o serviço

3. [[03 - Gerando código Go]] — `protoc`, `protoc-gen-go`, `protoc-gen-go-grpc`, o que sai gerado
4. [[04 - Servidor e cliente gRPC]] — implementar o serviço, subir o servidor, chamar via cliente stub
5. [[05 - Streaming]] — os 4 modos: unário, server-streaming, client-streaming, bidirecional

### Magus — gRPC de produção

6. [[06 - Interceptors, metadata e erros]] — middleware unário/streaming, contexto entre chamadas, `status`/`codes`
7. [[07 - gRPC em produção]] — TLS, health checking, reflection, load balancing, gateway REST (grpc-gateway)

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/11 - Persistência/index|Persistência]]
- Próximo galho: **Mensageria** (galho 13) — onde a comunicação síncrona ponto-a-ponto do gRPC dá lugar a filas e eventos assíncronos
