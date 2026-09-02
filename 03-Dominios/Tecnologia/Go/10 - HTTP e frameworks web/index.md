---
title: "Go — HTTP e frameworks web"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - http
  - web
  - backend
aliases:
  - Galho 10 Go
---
# Go — HTTP e frameworks web

> [!abstract] TL;DR
> Galho 10 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — como Go vira servidor web. 8 notas em 3 fases: o servidor HTTP embutido na stdlib e roteamento (Iniciado); request/response, middleware, os três frameworks de mercado (Gin, Chi, Echo) e o idioma REST em Go (Adepto); clientes HTTP e como servir em produção com timeouts e limites (Magus). Ao fim, você sabe por que Go dispensa framework pra montar um servidor decente — e quando escolher um mesmo assim.

Aqui o Go mostra outra aposta de design: `net/http` já é um servidor web completo e idiomático, sem depender de terceiros — os frameworks existem pra conveniência (roteamento com parâmetros, agrupamento de middleware), não pra suprir uma lacuna estrutural.

## Notas por fase

### Iniciado — o servidor que já vem pronto

1. [[01 - O servidor HTTP da stdlib]] — `http.ListenAndServe`, `http.Handler`, `HandlerFunc`, `http.Server` e seus campos
2. [[02 - Roteamento]] — `http.ServeMux` (inclusive o roteamento por método/padrão do Go 1.22+), por que a stdlib bastava e quando não basta mais

### Adepto — modelando a requisição

3. [[03 - Request e Response]] — `http.Request` (body, headers, query, context), `http.ResponseWriter`, JSON de entrada/saída
4. [[04 - Middleware]] — o padrão `func(http.Handler) http.Handler`, encadeamento, logging/recovery/auth como middleware
5. [[05 - Frameworks — Gin, Chi, Echo]] — o que cada um resolve além da stdlib, trade-offs, quando escolher qual
6. [[06 - REST idiomático em Go]] — convenções de rota, status codes, tratamento de erro em handler, versionamento

### Magus — servindo de verdade

7. [[07 - Clientes HTTP]] — `http.Client`, timeouts, retry, connection pooling, `context` propagado no client
8. [[08 - Servindo em produção — timeouts e limites]] — `ReadTimeout`/`WriteTimeout`/`IdleTimeout`, graceful shutdown, limites de tamanho de body, rate limiting

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Próximo galho: **Persistência** (galho 11) — `database/sql`, pool, pgx, sqlc, GORM, migrations

