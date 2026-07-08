---
title: "Roadmap — Rodar em produção"
created: 2026-07-08
type: meta
publish: false
tags:
  - meta
  - roadmap
  - operacao
---

# Roadmap — Rodar em produção (sub-galho 3)

Roadmap-folha do sub-galho `Operação/3 - Rodar em produção`. Fase **Adepto→Magus** (alvo ~460-560 linhas / 5-7k palavras). Spec: [[00-Meta/specs/2026-07-08-operacao-devops-trilha-design]]. EXEMPLAR: [[1 - O ofício de operar/01 - O que é operar um sistema]].

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

#### 01 - Containers em produção   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto
- **Escopo:** imutabilidade, imagem mínima/segura, container como unidade de deploy, o que NÃO colocar num container, one-process, resource footprint.
- **Fronteira:** reforço de [[Docker]]; **fronteira Java G17** (Jib/distroless/Buildpacks é lá).
- **Fontes:** docs Docker/OCI; Google distroless; CNCF; 12-Factor (referência SG1-02).
- **Resultado:** 255 linhas / 4870 palavras; 2 Mermaid, 3 [!warning], 3 [!question]-. Fronteira Java G17 (Jib/distroless) respeitada. Verificado: links e URLs ok.

#### 02 - O contrato de produção do Kubernetes   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto→Magus
- **Escopo:** probes (liveness/readiness/startup), requests/limits, QoS, HPA, PDB, graceful shutdown (SIGTERM/preStop) — a **ótica operacional**.
- **Fronteira:** reforço de [[Kubernetes]]; **fronteira Java G17** (mesmo contrato, ótica JVM lá).
- **Fontes:** Kubernetes docs (probes, resources, PDB); Google Borg paper; posts SRE.
- **Resultado:** 300 linhas / 5327 palavras; 4 Mermaid (3 probes, graceful shutdown), 3 [!warning], 4 [!question]-. Fronteira Java G17 respeitada. Verificado: links e URLs ok.

#### 03 - Zero-downtime e alta disponibilidade   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto→Magus
- **Escopo:** rolling sem derrubar, connection draining, readiness gating, réplicas + anti-affinity, spread por zona, o deploy que perde requests.
- **Fronteira:** linka SG2-02 (deploy strategies) e a nota 02 (probes).
- **Fontes:** Kubernetes docs (rolling update, PDB, topology spread); posts de zero-downtime.
- **Resultado:** 280 linhas / 5483 palavras; 3 Mermaid (corrida SIGTERM×endpoint, gantt grace, spread zonas), 3 [!warning], 4 [!question]-. Verificado: links e URLs ok.

#### 04 - Escala e capacidade   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Magus
- **Escopo:** autoscaling (HPA/VPA/cluster autoscaler/KEDA), capacity planning, o custo de escalar, load shedding, back-of-envelope de capacidade, over/under-provisioning.
- **Fronteira:** reforço de estimativas do System Design sob ótica de operação.
- **Fontes:** Kubernetes autoscaling docs; Google SRE (handling overload); KEDA.
- **Resultado:** 284 linhas / 6299 palavras; 3 Mermaid (3 camadas autoscaling), 3 [!warning], 3 [!question]-. Fontes: HPA/VPA/CA/KEDA/Karpenter, SRE overload/load-shedding. Verificado: links e URLs ok.

#### 05 - Rede e borda em produção   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto→Magus
- **Escopo:** ingress/reverse proxy, TLS termination, rate limiting na borda, health checks do LB, service mesh (breve), north-south vs east-west.
- **Fronteira:** reforço de [[Nginx]]; fronteira System Design (CDN/LB conceitual).
- **Fontes:** Nginx/Ingress-nginx docs; Kubernetes Service/Ingress; Envoy; posts de mesh.
- **Resultado:** 285 linhas / 5680 palavras; 3 Mermaid (N-S vs E-W, TLS renewal, mTLS sidecar), 3 [!warning], 3 [!question]-. Gateway API + service mesh + ambient. Verificado: links e URLs ok.

#### 06 - Resiliência operacional   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Magus · **FECHA o sub-galho**
- **Escopo:** timeouts, retries com backoff, circuit breaker, bulkhead, graceful degradation — **sob a ótica de quem opera** (config, tuning, o que observar, onde mora: app vs mesh).
- **Fronteira:** **reforço** de [[05 - Circuit Breaker e resiliência]] (System Design) — ótica de operação, não de design.
- **Fontes:** Nygard *Release It!*; AWS Builders' Library; Istio/Envoy resilience; Google SRE (addressing cascading failures).
- **Resultado:** 277 linhas / 6977 palavras; 4 Mermaid (cascata + intervenção dos padrões), 6 [!warning], 5 [!question]-. Ótica de operar (tuning/observar/app-vs-mesh). Verificado: links e URLs ok.
