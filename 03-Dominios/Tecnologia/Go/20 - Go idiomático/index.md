---
title: "Go — Go idiomático"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - idiomatico
  - estilo
aliases:
  - Galho 20 Go
  - Go idiomático
---
# Go — Go idiomático

> [!abstract] TL;DR
> Galho 20 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — a síntese de tudo: escrever Go que não parece Java (ou Python, ou Node) escrito em Go. 7 notas em 3 fases: Effective Go, a cultura do "less is more" e naming (Iniciado); composição na prática, anti-patterns de quem vem de OO e as ferramentas (go vet/golangci-lint) (Adepto); code review e o "Go way" (Magus). Este galho não reintroduz conceitos — releva os galhos anteriores pela lente da idiomaticidade.

Não é um galho de features novas: é onde interfaces pequenas, erros como valor, composição e simplicidade viram cultura. Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — a cultura

1. [[01 - Effective Go e a cultura]] — os princípios, "less is more", clareza sobre esperteza
2. [[02 - Naming e organização]] — nomes curtos no contexto do package, `MixedCaps`, getters sem `Get`

### Adepto — o ofício

3. [[03 - Composição sobre herança na prática]] — embedding + interfaces pequenas no lugar de hierarquias
4. [[04 - Erros comuns de quem vem de OO]] — anti-patterns: interfaces grandes, getters/setters, packages `util`
5. [[05 - go vet, golangci-lint e ferramentas]] — `go vet`, staticcheck, golangci-lint, gofmt como lei

### Magus — o padrão sênior

6. [[06 - Code review em Go]] — o "Go Code Review Comments", o que revisar, cultura de review
7. [[07 - Escrevendo Go que não parece Java]] — síntese: o "Go way", deixar a linguagem pequena trabalhar

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/19 - Segurança/index|Segurança]]
- Próximo galho: **Preparação para entrevista de Go** (galho 21) — consolidar tudo para o loop de entrevista
