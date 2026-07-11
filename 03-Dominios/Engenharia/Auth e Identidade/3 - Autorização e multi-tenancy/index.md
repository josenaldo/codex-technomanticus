---
title: "Autorização e multi-tenancy"
type: moc
publish: true
tags:
  - auth
  - identidade
  - autorizacao
  - rbac
  - rebac
  - multi-tenancy
  - moc
created: 2026-07-11
---

# Autorização e multi-tenancy — Auth e Identidade

Autenticado ≠ autorizado. Depois de [[2 - OAuth 2.1 e OpenID Connect/index|provar quem é o usuário]], vem a pergunta mais difícil: **quem pode o quê**. Este sub-galho (fase **Adepto→Magus**) cobre os três modelos de autorização (RBAC, ABAC, ReBAC), o mundo fine-grained inaugurado pelo paper Zanzibar (OpenFGA, policy-as-code), o corte de **multi-tenancy** que define o SaaS B2B, e como tudo isso aterrissa na autorização de API na prática.

## Notas

1. [[01 - RBAC, ABAC e ReBAC — os três modelos]]
2. [[02 - Fine-grained authorization — Zanzibar e policy-as-code]]
3. [[03 - Multi-tenancy e organizações]]
4. [[04 - Autorização de API na prática]]

## Veja também

- [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]] — o galho-pai
- [[2 - OAuth 2.1 e OpenID Connect/index|OAuth 2.1 e OpenID Connect]] — de onde vem o token que estas regras avaliam
- [[5 - Keycloak/index|Keycloak]] — Organizations aterrissa a multi-tenancy deste sub-galho
- [[13 - Autorização e controle de acesso|Segurança 13]] — o conceito neutro que este sub-galho aprofunda
