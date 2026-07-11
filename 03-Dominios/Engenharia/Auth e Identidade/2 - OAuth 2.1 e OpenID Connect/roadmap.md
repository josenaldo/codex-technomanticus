---
title: "Roadmap — OAuth 2.1 e OpenID Connect"
created: 2026-07-10
type: meta
publish: false
tags:
  - meta
  - roadmap
  - auth-identidade
---

# Roadmap — OAuth 2.1 e OpenID Connect (sub-galho 2)

Roadmap-folha do sub-galho `Auth e Identidade/2 - OAuth 2.1 e OpenID Connect`. Fase **Adepto** (densidade ~5-7k palavras/nota). Baseline **OAuth 2.1 draft-15** (caducidade: revisar quando virar RFC). Spec: [[00-Meta/specs/2026-07-10-auth-identidade-trilha-design]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 6 |
| ⬜ pendente | 0 |
| ✅ feita | 6 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - OAuth — o problema da delegação   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** password anti-pattern (~2006); papéis (RO/client/AS/RS) no exemplo persistente Agenda Já/Google Calendar; scopes; confidential vs public client; história 1.0→2.0→2.1; "OAuth não é autenticação" (confused deputy).
- **Resultado:** 296 linhas / 6.322 palavras; 2 Mermaid, 4 [!warning], `## Casos práticos` (web vs mobile). 11 fontes (RFC 6749/6750, oauth.net, Duende, Auth0, BeyondTrust/AWS confused deputy, Google Calendar scopes). Prosa densa (linhas < gate mecânico de 400, palavras no alvo).

#### 02 - Authorization Code + PKCE — o fluxo canônico   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto · **EXEMPLAR do sub-galho**
- **Escopo:** front vs back channel; fluxo request a request com URLs reais; PKCE (verifier/challenge/S256, RFC 7636→obrigatório universal via 2.1/RFC 9700, downgrade attack); state vs nonce; exact redirect URI matching (caso Booking.com); morte do implicit (contexto CORS) e do ROPC; code de uso único.
- **Resultado:** 330 linhas / 5.633 palavras; 4 Mermaid (incl. sequenceDiagram completo e ataque de interception), 4 [!warning]. 14 fontes (draft-15, RFC 7636/9700/8252/6749, PortSwigger, ACM/Booking.com). **Decisão de honestidade:** caso "state ausente" sem case study nomeado (report Slack/H1 era não-explorável — não citado).

#### 03 - OpenID Connect — identidade sobre OAuth   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** ID token vs access token (o erro de mandar ID token pra API); claims/scopes padrão; userinfo vs claims no token; discovery; dynamic client registration (menção); logout federado (RP-initiated, front vs back-channel); "Sign in with" na prática (GitHub não é OIDC); OIDC vs SAML.
- **Resultado:** 342 linhas / 6.443 palavras; 3 Mermaid, 3 [!warning]; abertura com o zero-day Sign in with Apple (Bhavuk Jain, US$100k). 12 fontes (specs openid.net ×5, Google Identity, Auth0, Microsoft).

#### 04 - Grants de máquina e fluxos especiais   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** client credentials (M2M; client_secret vs private_key_jwt vs mTLS); device flow (RFC 8628, device code phishing documentado Volexity/Microsoft); token exchange (RFC 8693, act claim, delegação vs impersonation, exemplo orders→inventory); sender-constrained (mTLS RFC 8705, DPoP RFC 9449 + adoção 2026).
- **Resultado:** 313 linhas / ~6.100 palavras; 6 Mermaid, 4 [!warning], 2 [!info] de fronteira (PKI/Segurança 11; service mesh/Operação). 19 fontes. **Débito leve:** tabela de decisão "qual grant pra qual cenário" ficou implícita (candidata a enriquecimento).

#### 05 - Tokens em produção   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** access curto (trade-off TTL); refresh rotation + reuse detection (família revogada); revogação RFC 7009 vs introspection RFC 7662 (cache); opaque vs JWT no RS (tabela honesta); storage no browser (localStorage = pior, ranking); BFF como consenso 2026 (draft browser-based-apps rev.27 — 3 arquiteturas); a ironia de voltar pra sessão/cookie.
- **Resultado:** 345 linhas / 6.954 palavras; 4 Mermaid (incl. reuse detection e arquitetura BFF), 4 [!warning], `## Casos práticos` (2 cenários). 13 fontes (RFC 9700/7009/7662, draft rev.27 jul/2026, OWASP, Curity, Auth0, Okta).

#### 06 - SSO corporativo — SAML, federação e SCIM   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto · **FECHA o sub-galho**
- **Escopo:** federação (1 SaaS × N IdPs); SAML 2.0 (assertions, SP- vs IdP-initiated, metadata, ACS); XSW e comment injection (Duo/GitHub 2018, CVEs por lib); SAML vs OIDC honesto; SCIM 2.0 (RFC 7643/7644, deprovisioning como segurança); JIT vs SCIM; SSO tax; enterprise readiness (SSO+SCIM+audit).
- **Resultado:** 383 linhas / 7.078 palavras; 6 Mermaid (incl. 3 sequenceDiagram), 4 [!warning]. 18 fontes (OASIS, RFCs, sso.tax, advisories Duo/GitHub, WorkOS/Clerk/Scott Brady). Aponta pro SG3 (index ainda não criado — resolve no seeding).
