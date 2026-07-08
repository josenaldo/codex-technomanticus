---
title: "Roadmap — Entrega e release"
created: 2026-07-08
type: meta
publish: false
tags:
  - meta
  - roadmap
  - operacao
---

# Roadmap — Entrega e release (sub-galho 2)

Roadmap-folha do sub-galho `Operação/2 - Entrega e release`. Fase **Adepto** (alvo ~440-540 linhas / 5-6k palavras). Spec: [[00-Meta/specs/2026-07-08-operacao-devops-trilha-design]]. EXEMPLAR: [[1 - O ofício de operar/01 - O que é operar um sistema]].

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

#### 01 - Pipeline de CI-CD como decisão de design   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto
- **Escopo:** estágios, gates, fast-feedback, trade-off velocidade×segurança, o que automatizar e o que barrar, pipeline como código.
- **Fronteira:** reforço de [[CI-CD]] (ferramenta) sob ótica de design; linka testes [[Testes JS]].
- **Fontes:** Continuous Delivery (Humble & Farley); DevOps Handbook; docs GitHub Actions.
- **Resultado:** 280 linhas / 6246 palavras; 3 Mermaid (inc. estágios+gates), 3 [!warning], 3 [!question]-. Verificado: links e URLs ok.

#### 02 - Deployment strategies   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto
- **Escopo:** rolling / blue-green / canary / shadow; trade-offs (custo, risco, rollback speed); quando cada.
- **Fronteira:** **casa canônica** — [[Kubernetes]]/[[CI-CD]] apontam pra cá no fechamento.
- **Fontes:** Argo Rollouts; AWS/Google deployment docs; Martin Fowler (BlueGreenDeployment/CanaryRelease).
- **Resultado:** 283 linhas / 5053 palavras; 3 Mermaid (por estratégia), 3 [!warning], 3 [!question]-. Casa canônica de deploy strategies. Verificado: links e URLs ok.

#### 03 - Progressive delivery e rollback   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto
- **Escopo:** feature flags como kill switch, canary automatizado health-gated, rollback automático, decoupling deploy≠release.
- **Fronteira:** aprofunda o deploy≠release da SG1-03; linka 02.
- **Fontes:** LaunchDarkly/Flagsmith; Argo Rollouts (analysis); posts de progressive delivery.
- **Resultado:** 242 linhas / 5611 palavras; 2 Mermaid (inc. canary health-gated), 3 [!warning], 4 [!question]-. Verificado: links e URLs ok.

#### 04 - Migrations de banco em produção   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto
- **Escopo:** expand/contract (parallel change), schema change zero-downtime, backfill, o deploy que quebra o schema antigo, migrations vs rollback.
- **Fronteira:** reforço de [[03-Dominios/Ciência/Banco de Dados/index|Banco de Dados]] sob ótica de release.
- **Fontes:** Fowler (ParallelChange/evolutionary db); docs Flyway/Liquibase; posts (GitHub/Stripe zero-downtime migrations).
- **Resultado:** 268 linhas / 5148 palavras; 3 Mermaid (inc. expand→migrate→contract), 3 [!warning], 4 [!question]-. Fontes: gh-ost/PlanetScale/Stripe. Verificado: links e URLs ok.

#### 05 - GitOps e Infrastructure as Code   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto
- **Escopo:** declarativo vs imperativo, drift, repo como fonte da verdade, reconciliation loop; Terraform/Ansible conceitual (onde encaixam), não tutorial.
- **Fronteira:** reforço de [[CI-CD]]; Cloud fica fora. Terraform aprofundado = broto futuro.
- **Fontes:** OpenGitOps/Argo CD/Flux docs; HashiCorp (IaC); Weaveworks (GitOps origin).
- **Resultado:** 253 linhas / 5618 palavras; 3 Mermaid (inc. reconciliation loop), 3 [!warning], 4 [!question]-. Verificado: links e URLs ok.

#### 06 - Secrets e configuração em produção   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto · **FECHA o sub-galho**
- **Escopo:** secret management, rotação, nunca commitar segredo, injeção em runtime, secret vs config; Vault/sealed-secrets/cloud KMS conceitual.
- **Fronteira:** aprofunda o fator Config do 12-Factor (SG1-02); linka Segurança se aplicável.
- **Fontes:** HashiCorp Vault docs; Kubernetes Secrets/External Secrets; OWASP secrets management.
- **Resultado:** 279 linhas / 6421 palavras; 2 Mermaid (push-protection→rotação, injeção runtime), 4 [!warning], 3 [!question]-. Verificado: links e URLs ok.
