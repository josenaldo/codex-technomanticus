---
title: "Segurança e Guardrails"
type: moc
publish: true
tags:
  - seguranca-ia
  - ia
  - moc
created: 2026-05-02
updated: 2026-05-02
---

# Segurança e Guardrails

Código gerado por IA tem **45% de risco em testes de segurança** (Veracode 2025). Não é "vai melhorar com modelo maior" — Veracode mostrou: tamanho do modelo **não correlaciona** com segurança. Slopsquat virou vetor real de supply chain. Cursor/Claude wipou banco de produção em 9 segundos quando descuidado. EU AI Act torna-se obrigatório em agosto de 2026. Esta trilha mapeia: **(1) o problema** (vulnerabilidades sistemáticas, slopsquat, [[Dicionário de IA#Hallucination|alucinações]]), **(2) defesa em profundidade** (pirâmide de validação, SAST/SCA, sandboxing, prompting), **(3) processo** (review humano, testes imutáveis, métricas), **(4) compliance** (AI Act, GDPR, roadmap de adoção), e **(5) a segurança de runtime** da feature de IA em produção — prompt injection e o que o agente pode fazer depois de ler algo não confiável.

> [!info] Pré-requisitos
> Recomendado ter passado por [[Agentes de Codificação]] (Trilha 2 — para entender ferramentas), [[Context Engineering]] (Trilha 4 — para [[Dicionário de IA#Guardrail|guardrails]] determinísticos), e [[Spec-Driven Development]] (Trilha 5 — para validação contínua). Esta trilha é a **camada final** que protege o que as outras trilhas constroem.

> [!warning] Esta trilha é tempo-sensitive
> Datas críticas: **EU AI Act totalmente aplicável em 2 de agosto de 2026**. Fim de suporte de Amazon Q Developer em 30 de abril de 2027. Pesquisa de slopsquat e vulnerabilities **muda mensalmente**. Verificar fontes recentes ao adotar.

## Comece por aqui

Trilha sequencial recomendada — problema → defesa → processo → compliance.

### Bloco 1 — O Problema (3 notas)

A premissa: AI code é untrusted. Os ataques específicos de IA (slopsquat) e os bugs específicos (alucinações).

- [[01 - Código gerado por IA é untrusted]] — Veracode 45%, Java 72%, XSS em 86%, segurança não melhora com escala
- [[02 - Slopsquatting — o ataque via alucinação]] — Seth Larson, react-codeshift case (jan 2026), 237 repos infectados
- [[03 - Alucinações em código — APIs fantasma e parâmetros inexistentes]] — bug interno vs bug supply chain, mitigação via type check + schema

### Bloco 2 — Defesa em Profundidade (4 notas)

A pirâmide de validação e suas camadas: automação massiva, guardrails determinísticos, prompting, e o sandbox que protege fisicamente.

- [[04 - A pirâmide de validação AI]] — automação 90% / guardrails 5-10% / humano 1-5%
- [[05 - SAST e SCA para código AI]] — Semgrep + Snyk + CodeQL, regra dos 78%, CWE prioritários
- [[06 - Permissões e sandboxing]] — least privilege, OS-level, network isolation, caso Cursor wipou DB
- [[07 - Security-focused prompting]] — threat models, listas negativas, schema enforcement, padrões que funcionam

### Bloco 3 — Processo e Governança (3 notas)

O que humano deve revisar (e o que não). Testes imutáveis. Métricas honestas.

- [[08 - Code review de código AI — o que muda]] — divisão automação/humano, red flags, comprehension gate aplicado
- [[09 - Testes imutáveis — a barreira que o agente não pode reescrever]] — anti-pattern do agente reescrevendo testes, soluções via path-deny
- [[10 - Métricas de qualidade AI — defect escape rate, rework ratio]] — DER, rework, MTTD, VIR, AIAD, vanity metrics a evitar

### Bloco 4 — Compliance e Futuro (2 notas)

EU AI Act + GDPR como arquitetura. O roadmap de 12 semanas para adoção progressiva.

- [[11 - Governance as architecture — EU AI Act, GDPR, licenças]] — datas-chave, obrigações, retenção, licenças (AGPL via slopsquat)
- [[12 - O roadmap de segurança para times]] — plano de adoção em 3 fases × 4 semanas

### Bloco 5 — A outra segurança: a feature de IA em runtime (1 nota)

> [!important] Duas seguranças, um galho
> Os blocos 1 a 4 tratam da segurança do **código que a IA escreve** — o risco entra pelo commit, e a defesa é SAST, review, sandbox de execução, compliance. Este bloco trata da segurança da **feature de IA rodando em produção** — o risco entra por um dado que o modelo lê, e a defesa é permissão de ferramenta, allowlist e arquitetura de agente. São ameaças diferentes, com atacantes e mitigações diferentes, e é útil não confundi-las. Ambas moram aqui porque quem responde por elas no time é a mesma pessoa.

- [[13 - Prompt injection — quando o dado vira instrução]] — direta vs indireta, a trifecta letal, as 6 camadas de defesa, os 6 padrões arquiteturais, EchoLeak (CVE-2025-32711)

## Rotas alternativas

### Rota emergencial (já estou em fogo)
*"Tive incidente em prod por código AI — preciso reagir"*

[[01 - Código gerado por IA é untrusted]] → [[04 - A pirâmide de validação AI]] → [[05 - SAST e SCA para código AI]] → [[06 - Permissões e sandboxing]] → [[12 - O roadmap de segurança para times]]

### Rota arquiteto (defender antes de adotar)
*"Vou implementar agentes — preciso desenhar a defesa"*

[[01 - Código gerado por IA é untrusted]] → [[04 - A pirâmide de validação AI]] → [[06 - Permissões e sandboxing]] → [[07 - Security-focused prompting]] → [[09 - Testes imutáveis — a barreira que o agente não pode reescrever]]

### Rota runtime (vou colocar um agente em produção)
*"Meu agente lê e-mail, ticket ou web — o que pode dar errado?"*

[[13 - Prompt injection — quando o dado vira instrução]] → [[06 - Permissões e sandboxing]] → [[04 - A pirâmide de validação AI]] → [[03-Dominios/Tecnologia/IA/Context Engineering/12 - Guardrails determinísticos|Guardrails determinísticos]] → [[03-Dominios/Tecnologia/IA/Observability/02 - Anatomia de um trace LLM|Anatomia de um trace LLM]]

### Rota compliance (precisamos passar em auditoria)
*"EU AI Act está chegando — o que muda?"*

[[11 - Governance as architecture — EU AI Act, GDPR, licenças]] → [[10 - Métricas de qualidade AI — defect escape rate, rework ratio]] → [[12 - O roadmap de segurança para times]]

### Rota supply chain (proteger contra slopsquat)
*"Estou preocupado com pacotes maliciosos via AI"*

[[02 - Slopsquatting — o ataque via alucinação]] → [[03 - Alucinações em código — APIs fantasma e parâmetros inexistentes]] → [[05 - SAST e SCA para código AI]] → [[06 - Permissões e sandboxing]]

### Rota processo (refinar review e métricas)
*"Time já tem CI básico — quero subir o nível"*

[[08 - Code review de código AI — o que muda]] → [[09 - Testes imutáveis — a barreira que o agente não pode reescrever]] → [[10 - Métricas de qualidade AI — defect escape rate, rework ratio]]

### Rota líder técnico (apresentar a stakeholders)
*"Preciso justificar investimento em AI security"*

[[01 - Código gerado por IA é untrusted]] (números) → [[10 - Métricas de qualidade AI — defect escape rate, rework ratio]] (medição) → [[11 - Governance as architecture — EU AI Act, GDPR, licenças]] (compliance) → [[12 - O roadmap de segurança para times]] (plano)

## Leituras recomendadas

| Fonte | Tipo | Cobertura |
|-------|------|-----------|
| *Veracode — 2025 GenAI Code Security Report* | Relatório | Notas 01, 03, 05 |
| *DryRun Security — Top 10 AI SAST Tools for 2026* | Comparativo | Nota 05 |
| *Trend Micro — Slopsquatting* | Análise | Nota 02 |
| *Snyk — Package Hallucinations* | Guia | Nota 02 |
| *Anthropic — Engineering Claude Code Sandboxing* | Engenharia | Nota 06 |
| *NVIDIA — Practical Security Guidance for Sandboxing Agentic Workflows* | Guia | Notas 06, 12 |
| *EU Commission — AI Act regulatory framework* | Legal | Nota 11 |
| *artificialintelligenceact.eu* | Análise jurídica | Nota 11 |
| *OWASP Top 10 for LLM Applications* | Padrão | Trilha inteira |
| *USENIX Security Symposium* | Pesquisa acadêmica | Nota 02 |

## Veja também

- [[Agentes de Codificação]] — onde os ataques aterram (Cursor, Claude Code, etc.)
- [[Context Engineering]] — guardrails determinísticos, control plane
- [[Spec-Driven Development]] — validação contínua, testes imutáveis, fase Validate
- [[Economia de Tokens]] — kill switches em sessões, hard limits
- [[Memória de Agentes]] — riscos específicos de memory poisoning, PII leak
