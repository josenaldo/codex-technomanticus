---
title: "Keycloak"
type: moc
publish: true
tags:
  - auth
  - identidade
  - keycloak
  - idp
  - moc
created: 2026-07-11
---

# Keycloak — Auth e Identidade

O IdP self-hosted de referência. Depois de aprender os protocolos ([[2 - OAuth 2.1 e OpenID Connect/index|OAuth/OIDC]]), a autorização ([[3 - Autorização e multi-tenancy/index|multi-tenancy]]) e como implementar em cada stack ([[4 - Auth nos stacks/index|Auth nos stacks]]), este sub-galho (fase **Magus**) mostra o **build vs buy** na prática: um Authorization Server pronto que emite os tokens que os stacks consomem. Baseline **Keycloak 26.x**.

## Notas

1. [[01 - Keycloak — realms, clients e flows]]
2. [[02 - Keycloak em produção]]
3. [[03 - Integrando os stacks com Keycloak]]

## Veja também

- [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]] — o galho-pai
- [[4 - Auth nos stacks/index|Auth nos stacks]] — os clientes que integram com este IdP
- [[3 - Autorização e multi-tenancy/03 - Multi-tenancy e organizações|Multi-tenancy e organizações]] — o que Keycloak Organizations aterrissa
