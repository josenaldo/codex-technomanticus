---
title: "Roadmap — Autorização e multi-tenancy"
created: 2026-07-11
type: meta
publish: false
tags:
  - meta
  - roadmap
  - auth-identidade
---

# Roadmap — Autorização e multi-tenancy (sub-galho 3)

Roadmap-folha do sub-galho `Auth e Identidade/3 - Autorização e multi-tenancy`. Fase **Adepto→Magus** (densidade ~5-7k palavras/nota). Spec: [[00-Meta/specs/2026-07-10-auth-identidade-trilha-design]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 4 |
| ⬜ pendente | 0 |
| ✅ feita | 4 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - RBAC, ABAC e ReBAC — os três modelos   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** os três modelos com exemplo persistente (SaaS de documentos); roles agregam → role explosion → ABAC (atributos em runtime, PDP) → ReBAC (grafo de relacionamentos); GitHub e Google Drive como casos reais de ReBAC; AWS IAM tags como ABAC; consenso 2026 híbrido RBAC coarse + ReBAC fine. ReBAC apresentado só conceitualmente (deep-dive fica na 02).
- **Resultado:** 296 linhas / ~5.376 palavras; 5 Mermaid (RBAC, role explosion, ABAC/PDP, ReBAC, comparativo), 22 fontes. Callout "Em entrevista" com diálogo fraco/forte, tabela PT↔EN (13 termos). Fronteiras respeitadas (Segurança 13, Java/Seg 14, Node/Seg 06 linkadas, não reexplicadas).

#### 02 - Fine-grained authorization — Zanzibar e policy-as-code   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** paper Zanzibar (tuplas objeto#relação@usuário, zookies, new-enemy problem); OpenFGA (CNCF Incubating out/2025, DSL + check), SpiceDB, Ory Keto, Permify; policy-as-code OPA/Rego e AWS Cedar; PEP/PDP/PIP; trade-off central (PDP externo) vs embutido (latência/disponibilidade/staleness).
- **Resultado:** 352 linhas / ~5.526 palavras; 4 Mermaid (tuplas+check, revogação c/ zookie, PEP/PDP/PIP, central vs embutido), 16 fontes. Código essencial (modelo OpenFGA DSL + policy Rego mínima). **Débito leve:** sem `[!info]` de caducidade dedicado (versões cravadas inline via footnote); palavras no limite inferior do alvo (mantido denso, sem padding).

#### 03 - Multi-tenancy e organizações   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** tenant como fronteira de identidade; modelo de organizações (usuário ∈ N orgs, membership, roles por org, convite + org switcher) no exemplo "Projeta"; isolamento em 3 eixos (dados: DB/schema/row-level+RLS; identidade: realm vs org; propagação: subdomínio/claim + tenant resolution); caso do e-mail duplicado em 2 empresas. Prepara Keycloak Organizations sem tutorial.
- **Resultado:** 361 linhas / ~6.688 palavras; 6 Mermaid (antipadrão, ER users/orgs/memberships, convite+switcher, isolamento de dados, realm-vs-Organizations, tenant resolution), 19 fontes, `[!info]` de caducidade Keycloak. Tabela PT↔EN (15 termos).

#### 04 - Autorização de API na prática   [substantivo]
- **Estado:** ✅ feita (2026-07-11) · fase: Magus · **FECHA o sub-galho**
- **Escopo:** claims design (scopes/roles coarse no token vs permissions fine via PDP lookup; antipadrão do token gigante — limites de header + staleness); enforcement em 2 camadas (gateway coarse + serviço fine, defense-in-depth); propagação de identidade (token reuse problem, token exchange RFC 8693, draft identity-chaining/ID-JAG jun/2026, phantom token, split token, mTLS/SPIFFE); audit trail (decision events vs policy-change events). Exemplo "Projeta" ponta a ponta. Costura 01-03; linka Comunicação SG2-03/SG2-04.
- **Resultado:** 329 linhas / ~6.628 palavras; 5 Mermaid (token gigante, split token/escopos, gateway→serviço, token exchange, phantom vs split), 21 fontes (inclui OpenID AuthZEN 1.0 jul/2026). Sem débitos.
