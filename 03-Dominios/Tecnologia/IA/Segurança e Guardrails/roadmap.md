---
title: "Roadmap — Segurança e Guardrails"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Segurança e Guardrails

Diagnóstico migrado de guia/roadmap - ia.md (28/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Segurança e Guardrails`

> [!warning] Diagnóstico de 28/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho. ⚠️ Este galho tem alerta regulatório adicional: a nota 11 (EU AI Act) tem prazo de caducidade em 2026-08-02 — checar se ainda reflete "lei ainda não aplicável" ou se precisa virar "lei já aplicável".

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado)
**Piso de linhas:** aplicável — Iniciado ≥300

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 12 |
| ⬜ pendente | 12 |
| ➖ não precisa | 0 |
| ✅ feita | 0 |
| 🔄 em andamento | 0 |
| % concluído | 0% |

---

## Notas

#### 01 - Código gerado por IA é untrusted   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 201 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2
- **Score:** 10/12
- **Plano de execução:**
  - Expandir "A janela de risco" com exemplos reais de incidentes, expandir "Onde a indústria está", ou adicionar seção "Como montar um pipeline mínimo" para atingir ≥300 linhas
  - Adicionar URLs reais às referências (Veracode, BusinessWire, Help Net Security)
- **Resultado:** —

#### 02 - Slopsquatting — o ataque via alucinação   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 251 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar seção "Impacto real — o que os estudos medem" (dados USENIX) e/ou aprofundar "Por que LLMs alucinam tanto pacote" para atingir ≥300 linhas
  - Adicionar URLs reais às referências (Trend Micro, Socket.dev, Snyk, Aikido, Mend.io, USENIX, Cloudsmith)
- **Resultado:** —

#### 03 - Alucinações em código — APIs fantasma e parâmetros inexistentes   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 283 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário concreto antes de "Os 5 tipos" (ativa E2 e sobe o piso)
  - Adicionar URLs reais às referências (Veracode 2025, Trend Micro, OWASP LLM Top 10, Pydantic docs)
- **Resultado:** —

#### 04 - A pirâmide de validação AI   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 250 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar seção "Casos reais de falha na pirâmide" com 2-3 exemplos de incidentes por camada ausente, ou expandir "Anti-patterns" com 2 itens adicionais
  - Adicionar URLs reais às referências (Veracode 2025, DryRun Security, NVIDIA blog, Anthropic engineering blog, OWASP LLM Top 10)
- **Resultado:** —

#### 05 - SAST e SCA para código AI   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 291 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2, E3
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário concreto (ativa E2 e sobe piso)
  - Adicionar URLs reais às referências (DryRun Security, Veracode 2025, Semgrep docs, Socket.dev, OWASP LLM Top 10)
  - Adicionar diagrama Mermaid (pipeline CI/CD SAST+SCA ou árvore de decisão de ferramentas) — ativa E3 e contribui para o piso
- **Resultado:** —

#### 06 - Permissões e sandboxing   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 324 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs reais às referências (Anthropic Claude Code docs, Truefoundry blog, Adversa AI CVE post, NVIDIA whitepaper, Docker docs, Startup Fortune)
  - Opcional: snippet mostrando o resultado de deny rule contornada (bubblewrap Permission denied)
- **Resultado:** —

#### 07 - Security-focused prompting   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 306 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2, E2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar URLs reais às referências (Veracode 2025, Anthropic Best Practices, OWASP LLM Top 10 2025, Augment Code docs, Microsoft Security blog)
  - Adicionar parágrafo de abertura com cenário concreto entre o TL;DR e "O que NÃO funciona"
- **Resultado:** —

#### 08 - Code review de código AI — o que muda   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 285 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário concreto antes do `[!abstract]`
  - Adicionar URLs reais às referências (Anthropic Best Practices, GitHub AI code review post, Augment Code docs, Atlassian AI assistants blog, Plus8Soft Comprehension Gate)
- **Resultado:** —

#### 09 - Testes imutáveis — a barreira que o agente não pode reescrever   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 322 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs reais às referências (Anthropic Best Practices, Augment Code docs, Martin Fowler Spec by Example, GitHub Spec Kit)
  - P1 (código-com-falha) inaplicável para nota de prática/guardrail — não forçar
- **Resultado:** —

#### 10 - Métricas de qualidade AI — defect escape rate, rework ratio   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 281 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs reais às referências (dora.dev, GitClear AI impact on code quality, METR, Veracode State of Software Security)
  - Adicionar Mermaid mostrando evolução temporal das 5 métricas (xychart ou timeline antes/depois de intervenção) para atingir o piso
- **Resultado:** —

#### 11 - Governance as architecture — EU AI Act, GDPR, licenças   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 237 linhas reais · fase: Iniciado · status: seedling ⚠️ caducidade regulatória
- **Núcleo/gaps:** E1, L2
- **Score:** 9/12
- **Plano de execução:**
  - Expandir "Para code generation especificamente", "High-risk AI systems" e "Para times brasileiros" (status do PL 2338/2023, comparativo LGPD × GDPR × AI Act) — meta +65 linhas para atingir o piso
  - Quebrar o TL;DR em ≥3 linhas distintas: deadline/impacto imediato, obrigações práticas para code generation, consequência de não fazer (€35M / 7% de faturamento global) — ativa E1
  - Adicionar URLs reais às referências (digital-strategy.ec.europa.eu, artificialintelligenceact.eu)
  - ⚠️ Caducidade regulatória: prazo "2 de agosto de 2026" vence em ~33 dias (a partir de 2026-06-30) — adicionar `[!warning]` de caducidade avisando que após 2026-08-02 a nota precisa ser atualizada para o modo "lei já aplicável" (enforcement, primeiras multas, comunicados da Comissão Europeia)
- **Resultado:** —

#### 12 - O roadmap de segurança para times   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** ~316 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs reais às 5 referências (Veracode 2025 GenAI Report, DryRun Security SAST Tools 2026, Anthropic Best Practices for Claude Code, NVIDIA Sandboxing Guidance, EUR-Lex EU AI Act)
- **Resultado:** —
