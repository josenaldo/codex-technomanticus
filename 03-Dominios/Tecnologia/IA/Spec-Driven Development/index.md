---
title: "Spec-Driven Development"
type: moc
publish: true
tags:
  - sdd
  - ia
  - moc
created: 2026-05-02
updated: 2026-05-02
---

# Spec-Driven Development

A resposta direta da indústria, em 2025-2026, ao tech debt do **[[Dicionário de IA#vibe coding|vibe coding]]**. Não é "voltar a waterfall" — é reconhecer que [[Dicionário de IA#LLM (Large Language Model)|LLMs]] **precisam de contrato explícito** para gerar código previsível. Specs viram source of truth, código vira artefato derivado e validado. Pipeline canônico em 4 fases (Specify → Plan → Tasks → Implement) com validação contínua. GitHub Spec Kit virou padrão open source; Kiro é a aposta da Amazon; OpenSpec brilha em brownfield. Esta trilha mapeia o problema, o método, as ferramentas, e o pragmatismo de adoção — incluindo quando **não** usar SDD.

> [!info] Pré-requisitos
> Recomendado ter passado por [[Agentes de Codificação]] (Trilha 2 — para entender o problema concreto), [[Economia de Tokens]] (Trilha 3 — pra entender o custo do retrabalho), e idealmente [[Context Engineering]] (Trilha 4 — specs são camada de contexto). SDD opera no topo dessas disciplinas.

> [!warning] Não é uma metodologia universal
> SDD é resposta calibrada a um problema específico. Para protótipos, hackathons, ou exploração inicial, **vibe coding é melhor**. Esta trilha enfatiza tanto **quando usar** quanto **quando não usar**.

## Comece por aqui

Trilha sequencial recomendada — problema → método → pipeline → ferramentas → prática.

### Bloco 1 — O Problema e a Proposta (3 notas)

A crise que motivou SDD, a definição da metodologia, e o espectro de rigor.

- [[01 - O problema do vibe coding em produção]] — Veracode 45%, Salesforce Ben 2026, tech debt acelerado
- [[02 - O que é Spec-Driven Development]] — definição, pipeline 4 fases, inversão fundamental
- [[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source]] — espectro de adoção, escolha do nível certo

### Bloco 2 — O Pipeline SDD (4 notas)

As fases canônicas, fase por fase, com anti-patterns e métricas.

- [[04 - Fase Specify — definindo outcomes e constraints]] — markdown estruturado, 5 elementos canônicos, machine-readable specs
- [[05 - Fase Design e Plan — arquitetura e decomposição]] — ADRs, contratos, decomposição em DAG de tasks
- [[06 - Fase Implement — execução disciplinada]] — uma task por vez, test-first, drift detection durante implement
- [[07 - Fase Validate — spec como contrato executável]] — 5 gates de CI, drift detection, NFRs como assertions

### Bloco 3 — Ferramentas e Ecossistema (3 notas)

Panorama dos players, integração com agentes, conexão com context engineering.

- [[08 - Ferramentas SDD — Kiro, Spec Kit, OpenSpec, Tessl]] — comparativo, quando usar cada um
- [[09 - SDD com agentes — coordinator, implementor, validator]] — multi-agent CIV, VeriMAP, isolamento de contexto
- [[10 - Integração com context engineering — specs como contexto persistente]] — specs nas camadas, JIT guiado, multi-agent SDD

### Bloco 4 — Prática e Futuro (2 notas)

Adoção concreta semana-a-semana e debate honesto sobre limites.

- [[11 - Guia de implementação SDD — do zero ao projeto]] — roadmap de 12 semanas, métricas, sinais de sucesso/falha
- [[12 - Debates — spec-as-source vs pragmatismo]] — críticas legítimas, quando NÃO usar, posição honesta

## Rotas alternativas

### Rota crise (estamos sofrendo de tech debt agora)
*"Time já adotou IA e está acumulando dívida — preciso reagir"*

[[01 - O problema do vibe coding em produção]] → [[02 - O que é Spec-Driven Development]] → [[11 - Guia de implementação SDD — do zero ao projeto]] → [[12 - Debates — spec-as-source vs pragmatismo]]

### Rota arquiteto (entender o método antes de adotar)
*"Quero avaliar SDD com cuidado antes de empurrar para o time"*

[[02 - O que é Spec-Driven Development]] → [[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source]] → [[04 - Fase Specify — definindo outcomes e constraints]] → [[07 - Fase Validate — spec como contrato executável]] → [[12 - Debates — spec-as-source vs pragmatismo]]

### Rota multi-agent (orquestração avançada)
*"Quero SDD operando com agentes coordenados em paralelo"*

[[02 - O que é Spec-Driven Development]] → [[05 - Fase Design e Plan — arquitetura e decomposição]] → [[09 - SDD com agentes — coordinator, implementor, validator]] → [[10 - Integração com context engineering — specs como contexto persistente]]

### Rota ferramenta (já decidi adotar — qual stack?)
*"Sei que quero SDD — qual ferramenta?"*

[[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source]] → [[08 - Ferramentas SDD — Kiro, Spec Kit, OpenSpec, Tessl]] → [[11 - Guia de implementação SDD — do zero ao projeto]]

### Rota cético (vendas demais — onde tá o problema?)
*"Tudo isso parece bullshit corporativo — me convença ou me explique os limites"*

[[12 - Debates — spec-as-source vs pragmatismo]] → [[01 - O problema do vibe coding em produção]] → [[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source]] → [[02 - O que é Spec-Driven Development]]

## Leituras recomendadas

| Fonte | Tipo | Cobertura |
|-------|------|-----------|
| *GitHub Blog — Spec-driven development with AI* | Post oficial | Notas 02, 04, 08, 11 |
| *GitHub Spec Kit (github/spec-kit)* | Repo | Notas 04-08, 11 |
| *Augment Code — What Is Spec-Driven Development?* | Guia | Trilha inteira |
| *Martin Fowler — Understanding SDD: Kiro, Spec Kit, Tessl* | Análise | Notas 03, 08 |
| *DeepLearning.AI / JetBrains — SDD with Coding Agents (Andrew Ng)* | Curso | Notas 02-07 |
| *Microsoft for Developers — Diving Into SDD With Spec Kit* | Tutorial | Notas 04-07 |
| *Veracode — 2025 GenAI Code Security Report* | Relatório | Nota 01 |
| *VeriMAP (EACL 2026)* | Paper peer-reviewed | Nota 09 |
| *AWS — From spec to production: drug discovery with Kiro* | Caso | Nota 08 |
| *Pixelmojo — AI Coding Technical Debt Crisis* | Análise crítica | Notas 01, 12 |

## Veja também

- [[Agentes de Codificação]] — onde SDD aterra na prática (Cursor, Claude Code, Kiro)
- [[Context Engineering]] — specs como camada de contexto persistente; CIV é arquitetura de contexto distribuída
- [[Economia de Tokens]] — SDD reduz custo via menos retrabalho e cache hit alto
- [[Segurança e Guardrails]] — SDD + [[Dicionário de IA#Guardrail|guardrails]] determinísticos = defesa em profundidade
