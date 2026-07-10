---
title: "Roadmap — Fundamentos de identidade"
created: 2026-07-10
type: meta
publish: false
tags:
  - meta
  - roadmap
  - auth-identidade
---

# Roadmap — Fundamentos de identidade (sub-galho 1)

Roadmap-folha do sub-galho `Auth e Identidade/1 - Fundamentos de identidade`. Fase **Iniciado** (alvo de densidade ~440-540 linhas). Spec: [[00-Meta/specs/2026-07-10-auth-identidade-trilha-design]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 5 |
| ⬜ pendente | 0 |
| ✅ feita | 5 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - Identidade, autenticação e autorização — o mapa   [substantivo]
- **Estado:** ✅ feita (2026-07-10) · fase: Iniciado · **EXEMPLAR do galho** (padrão a copiar)
- **Escopo:** IAM como disciplina; AuthN vs AuthZ vs accounting (AAA); fatores (know/have/are) e o que é MFA de verdade; CIAM vs workforce identity; identidade como superfície de ataque nº 1; mapa da trilha.
- **Resultado:** 314 linhas / 5.298 palavras; 4 Mermaid, 4 [!warning], 3 [!question]-; abertura problema-first (IDOR multi-tenant); callout [!info] instrumenta-não-substitui Segurança 12/13. Fontes fortes (Verizon DBIR 2026, OWASP Top 10:2025, NIST 800-63B/-4, CISA, FIDO). Sem débitos.

#### 02 - Sessões e cookies — auth stateful   [substantivo]
- **Estado:** ✅ feita (2026-07-10) · fase: Iniciado
- **Escopo:** session ID server-side; cookie flags (HttpOnly/Secure/SameSite, __Host-/__Secure-); CSRF (synchronizer/double-submit, Fetch Metadata); session fixation e rotação; idle vs absolute timeout; stores (Redis vs sticky); quando sessão ainda é a resposta certa em 2026.
- **Resultado:** 342 linhas / ~5.478 palavras; 4 Mermaid (incl. sequenceDiagram login e ataque CSRF), 5 [!warning], 5 [!question]-. Fontes: OWASP (Session Mgmt/CSRF/Fixation), MDN. Sem débitos.

#### 03 - JWT e a família de tokens   [substantivo]
- **Estado:** ✅ feita (2026-07-10) · fase: Iniciado
- **Escopo:** anatomia header/payload/signature; JWS vs JWE; HS256 vs RS256/ES256/EdDSA (árvore de decisão); claims registradas; validação correta (4 checagens); JWKS/rotação; alg=none, confusão RS→HS, kid injection (CVEs reais); stateless vs revogável; tokens opacos.
- **Resultado:** 377 linhas / ~5.724 palavras; 3 Mermaid, 3 [!warning] com CVEs, callout [!info] ponte pra Java/Seg 08 e Node/Seg 04. Fontes: RFC 7519/7515/7516/7517/7662/8725, PortSwigger, Auth0. Wikilinks forward pra SG2-05 (intencional).

#### 04 - Senhas e MFA — o legado que não morre   [substantivo]
- **Estado:** ✅ feita (2026-07-10) · fase: Iniciado
- **Escopo:** argon2id > bcrypt (72 bytes) > scrypt/PBKDF2, nunca MD5/SHA puro; NIST 800-63B rev.4 (comprimento > complexidade, sem rotação forçada); credential stuffing + HIBP/k-anonymity; TOTP (RFC 6238); SMS fraco (SIM swap); MFA fatigue (Uber 2022); recovery como elo fraco; lockout vs DoS.
- **Resultado:** 355 linhas / ~6.950 palavras; 4 Mermaid, 7 [!warning], 2 [!info] de fronteira (Segurança 06, System Design rate limiting). 15 fontes (OWASP ×4, NIST, RFC 6238, HIBP, PHC/Argon2, LinkedIn 2012, Uber 2022, CISA). **Débito leve:** sem heading formal `## Casos práticos` (exemplo trabalhado está na narrativa); sem mídia (gancho p/ /adicionar-midia).

#### 05 - Passkeys e WebAuthn — o presente sem senha   [substantivo]
- **Estado:** ✅ feita (2026-07-10) · fase: Iniciado · **FECHA o sub-galho**
- **Escopo:** FIDO2 = CTAP2 + WebAuthn (papéis); par de chaves por origin (por que mata phishing); cerimônias create/get (attestation vs assertion); discoverable credentials + conditional UI; synced vs device-bound; adoção 2026 (FIDO: 5B passkeys); rollout gradual; downgrade attack; limitações honestas.
- **Resultado:** 361 linhas / ~6.200 palavras; 6 Mermaid (2 sequenceDiagram de cerimônia), 4 [!warning], tabela PT↔EN 12 linhas. 15 fontes (W3C WebAuthn L3, webauthn.guide, FIDO Alliance 2026, web.dev, Yubico, Proofpoint). Aponta pro SG2 (index ainda não criado — resolve no seeding do SG2).
