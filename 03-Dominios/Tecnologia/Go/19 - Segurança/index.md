---
title: "Go — Segurança"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - seguranca
  - security
aliases:
  - Galho 19 Go
  - Segurança em Go
---
# Go — Segurança

> [!abstract] TL;DR
> Galho 19 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — o que Go dá de graça (memory safety) e o que continua sendo sua responsabilidade. 8 notas em 3 fases: o panorama de segurança (Iniciado); crypto na stdlib, TLS, validação de input e govulncheck/supply chain (Adepto); secrets, secure coding patterns e AuthN/AuthZ em serviços (Magus). Ao fim, você escreve serviços Go que resistem aos ataques comuns e faz a ponte com a trilha Auth e Identidade.

Go elimina classes inteiras de bug de memória, mas validação, cripto correta, TLS e supply chain seguem por sua conta.

## Notas por fase

### Iniciado — o panorama

1. [[01 - Segurança em Go — o panorama]] — memory safety de graça, o que ainda é responsabilidade do dev

### Adepto — as defesas concretas

2. [[02 - crypto na stdlib]] — `crypto/*`, hashing, HMAC, senhas com bcrypt/argon2, nunca rolar sua cripto
3. [[03 - TLS em Go]] — `crypto/tls`, servidor e cliente HTTPS, verificação de certificado, mTLS
4. [[04 - Validação e sanitização de input]] — validar tudo, queries parametrizadas, escaping de template
5. [[05 - govulncheck e supply chain]] — `govulncheck`, `go.sum`, GOPROXY/GOSUMDB, auditar dependências

### Magus — endurecimento e identidade

6. [[06 - Secrets e configuração segura]] — nunca hardcode, não vazar em logs, rotação, superfície de vazamento
7. [[07 - Secure coding patterns]] — comparação timing-safe, `crypto/rand`, overflow, defesa em profundidade
8. [[08 - AuthN e AuthZ em serviços Go]] — JWT, middleware de auth, RBAC; ponte para a trilha Auth e Identidade

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/18 - Cloud-native e produção/index|Cloud-native e produção]]
- Próximo galho: **Go idiomático** (galho 20) — a síntese: escrever Go que não parece Java escrito em Go
