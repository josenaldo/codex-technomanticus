---
title: "OAuth 2.1 e OpenID Connect"
type: moc
publish: true
tags:
  - auth
  - identidade
  - oauth
  - oidc
  - moc
created: 2026-07-10
---

# OAuth 2.1 e OpenID Connect — Auth e Identidade

Os protocolos que o mercado fala. Depois dos [[1 - Fundamentos de identidade/index|fundamentos]], este sub-galho (fase **Adepto**) cobre a camada de **delegação e federação**: por que OAuth existe (e por que não é autenticação), o fluxo canônico com PKCE, o OIDC por cima, os grants de máquina, o que fazer com tokens em produção e o SSO corporativo que fecha contratos B2B. Baseline **OAuth 2.1** — o mundo pós-implicit.

## Notas

1. [[01 - OAuth — o problema da delegação]]
2. [[02 - Authorization Code + PKCE — o fluxo canônico]]
3. [[03 - OpenID Connect — identidade sobre OAuth]]
4. [[04 - Grants de máquina e fluxos especiais]]
5. [[05 - Tokens em produção]]
6. [[06 - SSO corporativo — SAML, federação e SCIM]]

## Veja também

- [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]] — o galho-pai
- [[1 - Fundamentos de identidade/index|Fundamentos de identidade]] — sessões, JWT e passkeys que estes protocolos usam
- [[3 - Autorização e multi-tenancy/index|Autorização e multi-tenancy]] — o que acontece depois do token
- [[12 - OAuth2 e OIDC Client e os grant types|Java/Segurança 12]] — a implementação Spring destes fluxos
