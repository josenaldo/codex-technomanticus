---
title: "Python — Segurança"
created: 2026-07-11
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 11 - Segurança"
---

# Segurança

> [!abstract] TL;DR
> Galho 11 da trilha Python: a camada de segurança aplicada aos frameworks web do Galho 10 — injeção (SQL/template/comando/deserialização), XSS e CSRF nos frameworks Python, validação de input como controle de segurança (não só de forma), secrets e configuração segura, segurança de dependências (supply chain), rate limiting/proteção contra abuso, fechando com hardening da API do Galho 10 (autenticação real, correção de vulnerabilidades, secrets em produção). Fase Adepto→Magus; 9 notas. Terceiro galho do bloco "Backend e arquitetura" (9-13).

## Sobre este galho

Este galho **não reensina** o que já existe em profundidade em outras trilhas do vault — ele aponta pra lá e foca no que é específico da aplicação Python. Três fronteiras cravadas desde o início:

**Fronteira 1 — Autenticação/autorização (JWT, OAuth2, sessões):** já coberta em profundidade na trilha [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]], sub-galho 4 ("Auth nos stacks"), com notas dedicadas a [[03-Dominios/Engenharia/Auth e Identidade/4 - Auth nos stacks/02 - Python — Django|Python — Django]] e [[03-Dominios/Engenharia/Auth e Identidade/4 - Auth nos stacks/03 - Python — FastAPI|Python — FastAPI]] (JWT com `pyjwt`, `OAuth2PasswordBearer`, hashing de senha com `pwdlib`, integração com IdP via `PyJWKClient`). Este galho referencia essas notas e foca em COMO plugar essa autenticação na API REST do Galho 10 (nota 05) e no hardening do capstone (nota 09) — não reexplica o mecanismo JWT/OAuth2.

**Fronteira 2 — Conceitos criptográficos e OWASP genéricos:** já cobertos em [[03-Dominios/Engenharia/Segurança/index|Engenharia/Segurança]] (hashing criptográfico, PKI, classes de vulnerabilidade, gestão de chaves e segredos, autenticação/autorização conceituais). Este galho é a APLICAÇÃO Python desses conceitos, não a teoria.

**Fronteira 3 — Validação com Pydantic:** já coberta em profundidade no [[03-Dominios/Tecnologia/Python/Web e APIs REST/index|Galho 10]] (nota 03). Aqui a validação é revisitada sob a lente de SEGURANÇA (o que ela previne e o que ela não previne), não repetindo a mecânica do `BaseModel`/`Field`.

**Audiência:** quem já fecha o núcleo da linguagem, persistência (9) e a camada web (10), e precisa saber onde uma API Python real quebra em produção — e como blindar.

## Adepto

1. [[01 - OWASP Top 10 aplicado a Python web — o mapa|01 — OWASP Top 10 aplicado a Python web: o mapa]]
2. [[02 - Injeção — SQL, template, comando e deserialização insegura|02 — Injeção: SQL, template, comando e deserialização insegura]]
3. [[03 - XSS e CSRF nos frameworks Python|03 — XSS e CSRF nos frameworks Python]]
4. [[04 - Validação de input como controle de segurança|04 — Validação de input como controle de segurança]]
5. [[05 - Autenticação e autorização na prática — a ponte com Auth e Identidade|05 — Autenticação e autorização na prática: a ponte com Auth e Identidade]]

## Adepto→Magus

6. [[06 - Secrets e configuração segura|06 — Secrets e configuração segura]]
7. [[07 - Segurança de dependências e supply chain|07 — Segurança de dependências e supply chain]]

## Magus

8. [[08 - Rate limiting e proteção contra abuso|08 — Rate limiting e proteção contra abuso]]
9. [[09 - Capstone — hardening da API do Galho 10|09 — Capstone: hardening da API do Galho 10]] — recapitula o galho.

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/index|Web e APIs REST]] — Galho 10 (a API que este galho blinda)
- [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]] — deep-dive de autenticação/autorização/protocolo, incl. implementação Django/FastAPI (SG4)
- [[03-Dominios/Engenharia/Segurança/index|Segurança (Engenharia)]] — conceitos criptográficos e OWASP genéricos, agnósticos de linguagem
- [[03-Dominios/Tecnologia/Java/Segurança/index|Java — Segurança]] — trilha irmã, mesmo papel (Spring Security)
