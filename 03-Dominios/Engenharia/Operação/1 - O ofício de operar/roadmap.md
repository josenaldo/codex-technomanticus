---
title: "Roadmap — O ofício de operar"
created: 2026-07-08
type: meta
publish: false
tags:
  - meta
  - roadmap
  - operacao
---

# Roadmap — O ofício de operar (sub-galho 1)

Roadmap-folha do sub-galho `Operação/1 - O ofício de operar`. Fase **Iniciado→Adepto** (enquadramento; POV de quem já conhece as ferramentas). Spec: [[00-Meta/specs/2026-07-08-operacao-devops-trilha-design]]. EXEMPLAR de estrutura até a trilha ter o seu: [[1 - Framework de entrevista/01 - O que é System Design e o que a entrevista avalia]].

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

#### 01 - O que é operar um sistema   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Iniciado · **EXEMPLAR da trilha** · expandida (v1 210ln/3.6k → reforçada)
- **Escopo:** gap dev→prod; DevOps (Three Ways) e SRE ("implements DevOps", toil 50%) como respostas; "you build it, you run it"; 4 métricas DORA (clusters Elite→Low); "anatomia de um dia operando".
- **Fronteira:** enquadra a trilha; POV = quem já conhece as ferramentas.
- **Fontes:** Google SRE Book (intro/toil); dora.dev + State of DevOps 2023/2024; DevOps Handbook; Accelerate.
- **Resultado:** 262 linhas / 4917 palavras; 3 Mermaid (muro dev/ops, Three Ways, espectro concerns), 3 [!warning], 4 [!question]-. Verificado: links e URLs ok.

#### 02 - O contrato de uma app operável (12-Factor)   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto
- **Escopo:** 12-Factor como contrato de operabilidade; aprofunda Config/Logs/Processes/Disposability/Build-release-run/Parity/Backing-services; crítica moderna (Beyond the 12-Factor, era K8s).
- **Fronteira:** linka config de [[Node.js]]/[[Spring Boot]] e statelessness do System Design. Secrets → SG2-06; graceful shutdown → SG3.
- **Fontes:** 12factor.net; Beyond the Twelve-Factor App (IBM/Pivotal); Google Cloud "twelve to sixteen factor".
- **Resultado:** 297 linhas / 5051 palavras; 4 Mermaid (inc. build→release→run), 3 [!warning], 3 [!question]-. Verificado: links e URLs ok.

#### 03 - O ciclo de vida de um deploy   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto
- **Escopo:** build (artefato imutável) → release (artefato+config) → deploy → tráfego → observação; deploy ≠ release; rollback 1ª classe; DORA (deploy frequente = mais seguro). Mapa que os SG2/3/4 detalham.
- **Fronteira:** visão macro; deployment strategies em detalhe → SG2-02; observabilidade → SG4.
- **Fontes:** Continuous Delivery (Humble & Farley); dora.dev; Argo Rollouts; Flagsmith/Octopus (deploy≠release).
- **Resultado:** 244 linhas / 4810 palavras; 3 Mermaid (inc. pipeline commit→observação mapeando os sub-galhos), 3 [!warning], 3 [!question]-. Verificado: links e URLs ok.

#### 04 - Confiabilidade como feature   [substantivo]
- **Estado:** ✅ feita (2026-07-08) · fase: Adepto · **FECHA o sub-galho**
- **Escopo:** confiabilidade como feature projetada; tabela dos noves + custo exponencial; por que 100% é meta errada; SLA/SLO/SLI conceitual; error budget como ponte confiabilidade×velocidade (cálculo fica no SG4).
- **Fronteira:** prepara o SG4 (SLO/error budget); não aprofunda o cálculo (é lá).
- **Fontes:** Google SRE Book (Embracing Risk / SLOs) + SRE Workbook; tabela de uptime; outage AWS us-east-1 (out/2025).
- **Resultado:** 243 linhas / 5083 palavras; 4 Mermaid (inc. curva custo×noves), 3 [!warning], 3 [!question]-. Verificado: links e URLs ok.
