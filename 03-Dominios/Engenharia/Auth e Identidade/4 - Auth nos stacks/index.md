---
title: "Auth nos stacks"
type: moc
publish: true
tags:
  - auth
  - identidade
  - spring
  - django
  - fastapi
  - express
  - nestjs
  - gin
  - moc
created: 2026-07-11
---

# Auth nos stacks — Auth e Identidade

A exceção deliberada da trilha: depois de conceito ([[1 - Fundamentos de identidade/index|fundamentos]]), protocolo ([[2 - OAuth 2.1 e OpenID Connect/index|OAuth/OIDC]]) e decisão ([[3 - Autorização e multi-tenancy/index|autorização]]), este sub-galho (fase **Magus**) mostra **implementação guiada, uma nota por stack**. Formato comum: mapa das opções do ecossistema → fluxo recomendado 2026 (sessão web + API com OIDC) → código essencial (não boilerplate) → integração com IdP externo (ponte pro [[5 - Keycloak/index|Keycloak]]) → armadilhas do stack.

Duas notas são **pontes**: Spring já é coberto pelas 18 notas de [[03-Dominios/Tecnologia/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|Java/Segurança]] e Express/Node por [[03-Dominios/Tecnologia/Node/Segurança/04 - JWT e autenticação com jsonwebtoken|Node/Segurança 04-06]] — aqui elas mapeiam e completam lacunas, nunca re-tutorializam.

## Notas

1. [[01 - Java — Spring Security e Spring Authorization Server]]
2. [[02 - Python — Django]]
3. [[03 - Python — FastAPI]]
4. [[04 - Node — Express]]
5. [[05 - Node — NestJS]]
6. [[06 - Go — Gin]]

## Veja também

- [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]] — o galho-pai
- [[3 - Autorização e multi-tenancy/index|Autorização e multi-tenancy]] — a decisão que estas notas implementam
- [[5 - Keycloak/index|Keycloak]] — o IdP externo que estas notas integram
