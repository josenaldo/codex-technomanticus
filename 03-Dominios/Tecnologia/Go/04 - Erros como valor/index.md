---
title: "Go — Erros como valor"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - erros
  - error-handling
aliases:
  - Galho 4 Go
---
# Go — Erros como valor

> [!abstract] TL;DR
> Galho 4 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — o modelo de tratamento de erros que dispensa exceções. 8 notas em 3 fases: o tipo `error`, criação e comparação de erros (Iniciado); wrapping e a cadeia de erros, erros customizados e o par `panic`/`recover` (Adepto); estratégias de tratamento, o contraste com exceções e padrões usados em produção (Magus). Ao fim, você trata erro como valor de retorno explícito — não como fluxo de controle escondido.
>
> Aqui o Go mostra outra aposta central de design: **erro é valor, não exceção** — `if err != nil` é o idioma, não um smell, e `panic`/`recover` existe para falhas irrecuperáveis, não para controle de fluxo comum. Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — o contrato básico

1. [[01 - Erros são valores — o tipo error]] — a interface `error`, `if err != nil`, por que Go rejeitou exceções
2. [[02 - Criando e comparando erros]] — `errors.New`, `fmt.Errorf`, erros sentinela, comparação por igualdade

### Adepto — construindo a cadeia

3. [[03 - Error wrapping e a cadeia de erros]] — `%w`, `errors.Is`, `errors.Unwrap`, preservando contexto
4. [[04 - Erros customizados]] — tipos de erro próprios, `errors.As`, erros com dados estruturados
5. [[05 - panic e recover]] — quando entrar em pânico, recuperação, o limite entre erro e falha fatal

### Magus — julgamento em produção

6. [[06 - Estratégias de tratamento de erro]] — onde tratar, onde propagar, logging vs retorno, erros de borda
7. [[07 - Erros vs exceções]] — comparação com Java/Python/JS, trade-offs da explicitação
8. [[08 - Padrões de erro em produção]] — sentinelas de pacote, erros de domínio, observabilidade de falhas

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/03 - Interfaces e composição/index|Interfaces e composição]]
- Próximo galho: **Coleções e dados** (galho 5) — slices, maps e as estruturas de dados idiomáticas de Go
