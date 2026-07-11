---
title: "Roadmap — Keycloak"
created: 2026-07-11
type: meta
publish: false
tags:
  - meta
  - roadmap
  - auth-identidade
---

# Roadmap — Keycloak (sub-galho 5)

Roadmap-folha do sub-galho `Auth e Identidade/5 - Keycloak`. Fase **Magus**. Baseline **Keycloak 26.x** (26.6 estável / 26.7). Spec: [[00-Meta/specs/2026-07-10-auth-identidade-trilha-design]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 3 |
| ⬜ pendente | 0 |
| ✅ feita | 3 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - Keycloak — realms, clients e flows   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** build vs buy; modelo mental (realm=fronteira de isolamento / client confidential vs public / user / realm roles vs client roles / group / client scopes + protocol mappers); realm de exemplo Acme SaaS end-to-end; authentication flows (executions/requirements REQUIRED/ALTERNATIVE/CONDITIONAL, step-up); admin console vs Admin REST API (curl + Terraform/IaC); temas (menção).
- **Resultado:** 315 linhas / ~5.230 palavras; 2 Mermaid (hierarquia de recursos; flow com executions), 14 fontes. `[!info]` caducidade Keycloak 26.6/26.7. Código essencial (client config, curl Admin API). Organizations/HA delegados à nota 02. **Nota:** corrigido artefato de copy-paste em bloco Mermaid durante a escrita.

#### 02 - Keycloak em produção   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** Organizations (multi-tenancy B2B no realm, admin roles FGAP 26.7 — aterrissa SG3-03); passkeys nativos (26.4+, conditional UI, discoverable); SCIM (preview 26.7 + extensão scim-for-keycloak); HA/Infinispan (embedded vs external, Multi-cluster v2 26.7 sem cache externo); reverse proxy (hostname v2, --proxy-headers); upgrade sem downtime (rolling/Operator); SPI/extensões (--optimized + rebuild); build-vs-buy honesto (Auth0/WorkOS/Cognito/Zitadel + TCO).
- **Resultado:** 407 linhas / ~7.000 palavras; 5 Mermaid, 24 fontes. Múltiplos `[!info]` de caducidade (preview features marcadas). Observabilidade/K8s delegado a Operação.

#### 03 - Integrando os stacks com Keycloak   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Magus · **FECHA o sub-galho**
- **Escopo:** "um IdP, N stacks"; fluxo de referência SPA+BFF+API (sequenceDiagram); como cada stack se pluga (Spring resource server, FastAPI JWKS, NestJS/Express OIDC client/BFF, Gin go-oidc) com wikilink pro SG4 + trecho-chave; tabela comparativa (5 stacks incl. Django); mapeamento realm_access/resource_access → authorities; armadilhas (aud ausente por default, clock skew, cache JWKS).
- **Resultado:** 346 linhas / ~4.650 palavras; 3 Mermaid, 14 fontes. **Achado:** nest-keycloak-connect/keycloak-connect sem manutenção → recomenda openid-client puro (`[!warning]`). Costura SG4↔SG5; aponta pro capstone.
