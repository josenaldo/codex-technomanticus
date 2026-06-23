---
title: "Fase Specify — definindo outcomes e constraints"
created: 2026-05-02
updated: 2026-05-02
type: concept
progress: backlog
status: seedling
publish: true
tags:
  - sdd
  - ia
  - metodologia
  - specify
aliases:
  - Specify phase
  - Fase Specify
  - Outcomes e constraints
---

# Fase Specify — definindo outcomes e constraints

> [!abstract] TL;DR
> Specify é a primeira fase do pipeline SDD: descrever **o que** vai ser construído e **por quê**, sem cair em **como**. Foco em outcomes (o resultado que valida sucesso) e constraints (o que não pode ser violado). Em 2026, o padrão de facto é **markdown estruturado**, legível por humano e por LLM, versionado no repositório. GitHub Spec Kit, Kiro e OpenSpec convergiram em um formato semelhante: user journeys + acceptance criteria + non-functional requirements.

## A regra fundamental

**Specify responde "o quê" e "por quê". Nunca "como".**

| Nível | Pergunta | Onde mora |
|---|---|---|
| Specify | **O quê?** Por quê? | `specs/` |
| Plan | Como (arquitetura)? | `plan/` |
| Tasks | Decomposto em quais passos? | `tasks/` |
| Implement | Em código? | `src/` |

Misturar "como" no specify é o erro mais comum. Quando aparece *"vamos usar Postgres com índice em X"*, isso é Plan, não Specify.

## Anatomia de uma boa spec

```markdown
# Feature: Refund de pagamentos

## Outcome
Cliente que solicita refund deve receber confirmação em até 24h
e crédito processado em até 5 dias úteis.

## User journeys

### J1 — Refund total dentro de 7 dias
1. Cliente abre app, vai em "Histórico de pagamentos"
2. Seleciona pagamento dos últimos 7 dias
3. Clica em "Solicitar reembolso"
4. Confirma motivo
5. Recebe confirmação de recebimento (email + push)
6. Em até 5 dias úteis, vê crédito no método original

### J2 — Refund parcial após 7 dias
... (similar com diferenças)

## Acceptance criteria

- [ ] Cliente vê apenas pagamentos elegíveis para refund
- [ ] Refund total possível para pagamentos ≤ 7 dias
- [ ] Refund parcial requer aprovação manual
- [ ] Email de confirmação inclui ID de transação e prazo
- [ ] Estado do refund visível no histórico

## Non-functional requirements

- Latência p95 da requisição: < 500ms
- 0 perda de evento (idempotência obrigatória)
- Auditável: todo refund registrado em log imutável por 7 anos (compliance)

## Out of scope (explicit)

- Refund em método diferente do original (será spec separada)
- Refund de mais de 90 dias (não suportado nesta feature)

## Open questions

- Como tratar refund quando método original foi cancelado pelo banco?
- (...)
```

## Os 5 elementos canônicos

| Elemento | Função | Erro comum |
|---|---|---|
| **Outcome** | Definir sucesso em uma frase | Confundir com feature (saída ≠ resultado) |
| **User journeys** | Como o usuário interage | Pular para componentes técnicos |
| **Acceptance criteria** | Lista validável | Critério vago ("deve ser rápido") |
| **Non-functional requirements** | Performance, segurança, compliance | Esquecer (vira surpresa em prod) |
| **Out of scope** | Limites explícitos | Não declarar — agente preenche tudo |
| **Open questions** | O que ainda não decidiu | Não documentar (volta como bug) |

## Linguagem natural estruturada

A spec deve ser:

- **Legível por humano** — é o contrato que o time entende
- **Legível por [[Dicionário de IA#LLM (Large Language Model)|LLM]]** — agente vai consumi-la como contexto
- **Não-ambígua o suficiente** — frases declarativas, números concretos, listas pontuais
- **Não-código** — não é UML, não é JSON, não é regex (em geral)

> [!tip] Teste do "explica para outro engenheiro"
> Se você lesse essa spec sem ter participado da discussão, conseguiria implementar **uma** versão do que se espera? Se houvesse ≥2 implementações plausíveis e contraditórias, a spec ainda está vaga.

## Machine-readable specs (opcional, alta-rigor)

Em [[03 - Níveis de rigor — spec-first, spec-anchored, spec-as-source|spec-as-source]], a spec é parcialmente estruturada para máquina:

```yaml
# specs/auth/refund.spec.yml
feature: refund_payment
outcome: |
  Cliente que solicita refund deve receber confirmação em <24h
  e crédito processado em <5 dias úteis.

acceptance:
  - id: AC1
    given: payment_age <= 7d
    when: customer.requests_refund(amount=full)
    then: refund.created and notification.sent

  - id: AC2
    given: payment_age > 7d
    when: customer.requests_refund(amount=partial)
    then: approval_required and pending.created

nfr:
  latency_p95_ms: 500
  idempotency: required
  audit_retention_years: 7
```

Vantagem: pode virar input para gerador de testes ou contracts. Custo: linguagem específica, learning curve.

## Padrões de qualidade

### SMART para acceptance criteria

- **Specific** — "exibir X dado Y"
- **Measurable** — "p95 < 500ms"
- **Achievable** — não pede impossível
- **Relevant** — conectado ao outcome
- **Time-bound** — "<24h", "em 5 dias úteis"

### "BDD-style" para journeys

```
Given <pré-condição>
When <ação>
Then <consequência observável>
```

Mesmo sem framework BDD, a estrutura mental ajuda.

## Como LLMs ajudam (e atrapalham) na fase Specify

**Ajudam:**

- Geração de primeiro draft a partir de bullet points
- Detecção de ambiguidade ("isso pode ter 3 interpretações")
- Cobertura de edge cases (perguntar "e se?")
- Conversão de tickets soltos em spec coerente

**Atrapalham:**

- Inventam acceptance criteria razoáveis mas não-validados pelo PM
- Misturam "como" (saltam para Plan)
- Adicionam funcionalidade não pedida
- Aderem a templates verbosos

> [!warning] Spec gerada por IA precisa de revisão humana mais cuidadosa do que código
> Se a spec está errada, todo o resto cai em cascata. Tempo gasto em revisar spec é o **melhor investimento** do projeto.

## Anti-patterns

- **Spec verbose com 10 páginas** — vira leitura obrigatória que ninguém faz
- **Spec sem acceptance criteria** — dá interpretação aberta ao agente
- **Spec sem out-of-scope** — agente decide sozinho o que cortar
- **Spec sem open questions** — finge certeza onde não há
- **Spec stale 3 sprints depois** — virou static, perdeu rigor
- **Spec sem versionamento** — em Confluence, em vez de git

## Métricas

| Métrica | Alvo |
|---|---|
| **% de PRs gerados que aderem a 100% dos AC** | >85% |
| **Tamanho médio da spec** | 1-3 páginas (≤2K tokens) |
| **Tempo entre primeira spec e aprovação** | <2 dias |
| **Frequência de "specify" durante implementação** | Baixa (sinaliza rework) |

## Veja também

- [[02 - O que é Spec-Driven Development]]
- [[05 - Fase Design e Plan — arquitetura e decomposição]]
- [[Context Engineering|11 - Skills e instructions como contexto]]
- [[Agentes de Codificação|03 - O comprehension gate]]

## Referências

- **GitHub Spec Kit** — *spec-driven.md* (2026).
- **Augment Code** — *What Is Spec-Driven Development?* (2026).
- **Microsoft for Developers** — *Diving Into Spec-Driven Development With GitHub Spec Kit* (2026).
- **Zencoder Docs** — *A Practical Guide to Spec-Driven Development* (2026).
