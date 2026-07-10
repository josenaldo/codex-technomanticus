---
title: "Auth e Identidade"
type: moc
publish: true
tags:
  - auth
  - identidade
  - moc
created: 2026-07-10
---

# Auth e Identidade — quem pode o quê

A disciplina de **identidade digital**: provar quem o usuário é (autenticação), decidir o que ele pode fazer (autorização) e sustentar isso em produção — sessões, JWT, OAuth 2.1, OIDC, passkeys, SSO corporativo, RBAC/ReBAC e o IdP self-hosted (Keycloak). Trilha em 3 fases (Iniciado → Adepto → Magus), organizada em cinco sub-galhos + um capstone.

> [!info] Onde isto se encaixa
> Esta trilha é o **deep-dive de protocolo e implementação**. O conceito neutro de autenticação/autorização vive em [[12 - Autenticação|Segurança 12]] e [[13 - Autorização e controle de acesso|Segurança 13]]; a criptografia por trás (hashing, assinaturas, PKI) em [[06 - Hashing criptográfico|Segurança 06]], [[10 - MAC, HMAC e assinaturas digitais|Segurança 10]] e [[11 - PKI e certificados|Segurança 11]]; auth como decisão de contrato de API em [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]]. Nos stacks, [[03-Dominios/Tecnologia/Java/Segurança/index|Java/Segurança]] (Spring Security, 18 notas) e [[03-Dominios/Tecnologia/Node/Segurança/index|Node/Segurança]] já cobrem o chão — as notas daqui são **pontes que completam**, não repetição.

## Sub-galhos

### 1 · Fundamentos de identidade *(Iniciado)*
O vocabulário e os blocos: AuthN vs AuthZ, sessões e cookies, JWT, senhas e MFA, passkeys.
- [[1 - Fundamentos de identidade/index|Fundamentos de identidade]]

### 2 · OAuth 2.1 e OpenID Connect *(Adepto)*
Os protocolos que o mercado fala: delegação, Authorization Code + PKCE, OIDC, grants de máquina, tokens em produção, SSO corporativo.
- [[2 - OAuth 2.1 e OpenID Connect/index|OAuth 2.1 e OpenID Connect]]

### 3 · Autorização e multi-tenancy *(Adepto → Magus)*
Autenticado ≠ autorizado: RBAC/ABAC/ReBAC, Zanzibar e policy-as-code, organizações B2B, autorização de API.
- [[3 - Autorização e multi-tenancy/index|Autorização e multi-tenancy]]

### 4 · Auth nos stacks *(Magus)*
Implementação guiada: Spring Boot, Django, FastAPI, Express, NestJS e Go (Gin).
- [[4 - Auth nos stacks/index|Auth nos stacks]]

### 5 · Keycloak *(Magus)*
O IdP self-hosted de referência: realms, clients e flows; produção (Organizations, passkeys, HA); integração com todos os stacks.
- [[5 - Keycloak/index|Keycloak]]

### ★ Capstone *(Magus)*
Desenhando a identidade de um SaaS B2B do zero: build vs buy, sessão vs token vs BFF, rollout de passkeys, SSO enterprise, RBAC+ReBAC por organização.
- Capstone (a escrever ao final da trilha)

## Como usar esta trilha

Leia na ordem 1 → 2 → 3 se está começando: os fundamentos dão o vocabulário, o OAuth/OIDC dá os protocolos, a autorização fecha o modelo mental. Os sub-galhos 4 e 5 são consulta dirigida: vá direto à nota do **seu stack** e à do Keycloak quando for implementar. O capstone costura tudo num walkthrough de decisão.

## Recursos

### Specs e RFCs
- [OAuth 2.1 (draft)](https://oauth.net/2.1/) — a baseline de 2026: PKCE universal, implicit e password grant removidos
- [RFC 9700 — OAuth 2.0 Security BCP](https://www.rfc-editor.org/rfc/rfc9700) — as práticas que o 2.1 consolida
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [WebAuthn Level 3 (W3C)](https://www.w3.org/TR/webauthn-3/) · [webauthn.guide](https://webauthn.guide/)
- [NIST SP 800-63B — Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)

### Livros
- *OAuth 2 in Action* — Justin Richer & Antonio Sanso (o livro do protocolo)
- *API Security in Action* — Neil Madden (tokens, sessões e autorização de API na prática)
- *Solving Identity Management in Modern Applications* — Yvonne Wilson & Abhishek Hingnikar (o panorama IAM)

### Online
- [Keycloak docs](https://www.keycloak.org/documentation) — baseline 26.x
- [Spring Security reference](https://docs.spring.io/spring-security/reference/) · [django-allauth](https://docs.allauth.org/) · [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/) · [better-auth](https://www.better-auth.com/) · [NestJS Security](https://docs.nestjs.com/security/authentication) · [coreos/go-oidc](https://github.com/coreos/go-oidc)
- [OpenFGA docs](https://openfga.dev/docs) — fine-grained authorization (Zanzibar)

## Veja também

- [[03-Dominios/Engenharia/Segurança/index|Segurança]] — o domínio conceitual que esta trilha instrumenta
- [[03-Dominios/Tecnologia/Java/Segurança/index|Java/Segurança]] — Spring Security em profundidade (18 notas)
- [[03-Dominios/Tecnologia/Node/Segurança/index|Node/Segurança]] — JWT, OIDC e RBAC no Node
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — auth como decisão de contrato
- [[03-Dominios/Engenharia/index|Engenharia]] — o domínio
