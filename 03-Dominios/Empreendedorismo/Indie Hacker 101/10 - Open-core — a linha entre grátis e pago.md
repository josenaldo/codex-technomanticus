---
title: "Open-core — a linha entre grátis e pago"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - indie-hacker
  - empreendedorismo
  - modelo-negocio
  - open-core
  - monetizacao
aliases:
  - Open core
  - Modelo open-core
  - Open source business model
---

# Open-core — a linha entre grátis e pago

> [!abstract] TL;DR
> Open-core é o modelo de negócio em que o produto core é open source (grátis, MIT/Apache) e a monetização vem de features proprietárias no topo: SaaS hospedado, features enterprise (SSO, audit logs), integrações premium, ou IA avançada. A linha entre grátis e pago define tudo: se o core é fraco, a comunidade não cresce; se tudo é grátis, não há receita. A regra prática é **buyer-based placement**: features que o dev individual ama ficam no core grátis; features que o CTO ou compliance officer exige ficam no tier pago. GitLab, Supabase e Sentry são os exemplos de referência em 2026.

## O que é

Open-core não é "open source com freemium". É um modelo de negócio com arquitetura específica:

1. **Core open source.** O produto funcional, usável, com licença permissiva (MIT, Apache 2.0). Qualquer pessoa pode baixar, usar, modificar e contribuir. Este é o motor de adoção e comunidade.

2. **Camada proprietária.** Features adicionais que atendem necessidades de equipes, empresas ou power users — coisas que indivíduos não precisam mas organizações exigem. Esta é a fonte de receita.

A tensão central do modelo é: **onde traçar a linha?** Core demais no grátis e não há incentivo para pagar. Core de menos no grátis e a comunidade open source não cresce (porque o produto é um "teaser" inútil).

## Por que importa

Para indie hackers construindo dev tools ou SaaS técnico, open-core oferece vantagens únicas:

- **Distribuição orgânica.** Open source atrai devs sem custo de marketing — eles descobrem, experimentam, contribuem e evangelizam.
- **Trust por transparência.** Código aberto é auditável. Para devtools, isso é diferencial competitivo real.
- **Community moat.** Uma comunidade ativa é mais difícil de replicar que uma feature.
- **Portfolio como marketing.** O repo aberto é demonstração técnica permanente.

Mas open-core só funciona se a monetização estiver clara desde o design. Projetos open source sem modelo de receita viram hobbies caros do mantenedor.

## Como funciona

### O framework buyer-based placement

Desenvolvido por Open Core Ventures, este framework resolve a tensão "o que é grátis vs pago":

| Quem decide a compra? | O que valoriza? | Onde colocar? |
|----------------------|-----------------|--------------|
| **Dev individual** | Features que resolvem o problema dele | **Core (grátis)** |
| **Tech lead / gerente** | Colaboração, integrações, performance | **Pro (pago)** |
| **CTO / compliance** | SSO, SCIM, audit logs, SLA, SOC2 | **Enterprise (pago)** |

A lógica: o dev individual é o vetor de adoção. Ele descobre, testa, gosta e leva para dentro da organização. A organização então precisa de features que o dev individual não precisa — e paga por elas. **O core gratuito é o marketing; o tier pago é o produto.**

### Exemplos de referência em 2026

**GitLab:**
- Core: DevOps completo (SCM, CI/CD, project management) — open source
- Pago: security scanning avançado, compliance, audit logs, orchestration enterprise
- Lição: o core é poderoso o suficiente para competir com GitHub; o pago resolve dores corporativas

**Supabase:**
- Core: PostgreSQL + Auth + Realtime + Storage — open source
- Pago: limites maiores (compute, storage, MAUs), SSO, SOC2 compliance, support prioritário
- Modelo: subscription base + usage-based scaling
- Lição: free tier generoso atrai devs; scaling natural empurra para paid

**Sentry:**
- Core: error tracking engine — open source
- Pago: SaaS hospedado por tiers de uso (eventos, traces), analytics avançados, SSO
- Lição: o self-hosted é funcional; o SaaS é conveniente. Devs pagam pela conveniência.

### Tiers típicos de um SaaS open-core

| Tier | Target | Features típicas | Pricing |
|------|--------|------------------|---------|
| **Free / Community** | Dev individual | Core funcional, uso pessoal, 1 projeto | $0 |
| **Pro / Team** | Pequenas equipes | Limites maiores, colaboração, integrações, analytics | $10-30/mês/seat |
| **Enterprise** | Organizações | SSO, SCIM, audit logs, SLA, compliance, support dedicado | $50-200/mês/seat |

### A armadilha do "open source washing"

Se o core gratuito é um "teaser" — funcional o suficiente para demo mas inútil para uso real — a comunidade percebe e se recusa a adotar. O core precisa ser um produto real, usável, valioso por si só. Se não é, não é open-core — é freemium com código exposto.

Regra: **se um dev não consegue resolver o problema core usando apenas a versão gratuita, o modelo está errado.**

## Na prática

Para um indie hacker construindo uma ferramenta de estudo (como referência genérica):

| Camada | Licença | Exemplos de features |
|--------|---------|---------------------|
| **Core (CLI + lib)** | MIT | Parser, algoritmo de revisão, validação, export |
| **Plugin/extensão** | MIT | Integração com editor, visualização, dashboard básico |
| **SaaS/Web App** | Proprietário | Marketplace, IA avançada, sync cloud, analytics pro, API B2B |

A regra aplicada: o dev autodidata consegue usar CLI + plugin para estudar. Se quiser IA, sync, ou marketplace, paga o tier Pro ($10/mês).

## Armadilhas

- **Dar tudo no grátis e não ter o que cobrar.** Generosidade no core é bom; generosidade total é hobby, não negócio.

- **Crippleware: core tão limitado que ninguém usa.** Se precisa de 3 upgrades para fazer algo útil, a adoção orgânica morre.

- **Não comunicar claramente o que é grátis vs pago.** Pricing page confusa gera desconfiança. Transparência absoluta.

- **Medo de cobrar da comunidade.** Open source não significa que tudo é grátis. O código é grátis; o serviço pode ser pago. Redis, MongoDB, Elastic — todos monetizam serviço ao redor de código open source.

- **Licença errada no core.** MIT e Apache 2.0 são as mais seguras para adoção. AGPL e SSPL assustam empresas. Escolha com cuidado — mudar licença depois é controverso.

## Veja também

- [[11 - Pricing para SaaS bootstrapped]] — como precificar os tiers
- [[12 - Unit economics — CAC, LTV, MRR, churn]] — métricas do modelo
- [[01 - Bootstrapping vs venture capital]] — por que open-core é natural para bootstrap
- [[15 - Product-led growth para bootstrapped]] — free tier como motor de crescimento

## Referências

- **Open Core Ventures** — opencoreventures.com. Framework buyer-based placement e análise de modelos open-core.
- **Supabase Blog** — "Open Source Business Model". Análise detalhada do modelo de pricing da Supabase.
- **GitLab Handbook** — Publicly documented pricing and tier philosophy.
- **Sentry** — sentry.io. Exemplo de open-core com SaaS hospedado como revenue driver principal.
