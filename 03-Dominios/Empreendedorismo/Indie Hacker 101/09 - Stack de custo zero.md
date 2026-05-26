---
title: "Stack de custo zero"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - indie-hacker
  - empreendedorismo
  - produto
  - infraestrutura
  - stack
aliases:
  - Zero cost stack
  - Stack gratuita
  - Infraestrutura bootstrap
---

# Stack de custo zero

> [!abstract] TL;DR
> Em 2026, é possível lançar e operar um SaaS completo sem gastar $1 em infraestrutura até ter receita. Free tiers generosos de Vercel, Supabase, Stripe, PostHog, GitHub Actions e Resend cobrem hosting, banco de dados, pagamentos, analytics, CI/CD e email transacional. O custo real de começar um projeto bootstrapped é tempo, não dinheiro. Essa nota mapeia a stack de custo zero, quando cada free tier atinge limite, e em que ordem começar a pagar.

## O que é

A "stack de custo zero" é o conjunto de ferramentas e serviços com free tier suficiente para lançar, operar e até escalar um SaaS indie até os primeiros ~1.000 usuários sem custo de infraestrutura. Não é gambiar — é usar deliberadamente os free tiers generosos que empresas de infraestrutura oferecem para atrair devs.

O princípio: **não gaste dinheiro em infra até ter receita que justifique**. Cada dólar gasto antes de ter clientes pagantes é dólar saindo da reserva pessoal.

## Por que importa

"Preciso de investimento para começar" é o mito mais destrutivo do empreendedorismo em software. Em 2026, a barreira financeira de entrada é efetivamente zero para a maioria dos SaaS. A barreira real é tempo, disciplina e habilidade — não dinheiro.

Isso muda o cálculo de risco fundamentalmente (ver [[03 - Risco calculado do solo founder]]): se o custo financeiro é próximo de zero, o pior cenário é "perdi tempo e ganhei habilidades". Isso é um risco aceitável para qualquer dev empregado.

## Como funciona

### A stack completa (custo $0)

| Categoria | Ferramenta | Free tier | Limite |
|-----------|-----------|-----------|--------|
| **Hosting frontend** | Vercel | Ilimitado para projetos pessoais | Bandwidth: 100GB/mês |
| **Hosting alternativo** | GitHub Pages | Ilimitado para estáticos | Sem server-side rendering |
| **Banco de dados** | Supabase | PostgreSQL, 500MB, 2 projetos | Pausa após 1 semana inativo |
| **Banco alternativo** | Neon | PostgreSQL serverless, 0.5GB | 100h compute/mês |
| **Auth** | Supabase Auth | 50.000 MAUs | Generoso para início |
| **Pagamentos** | Stripe | Sem taxa mensal | 2.9% + $0.30 por transação (só paga quando recebe) |
| **Pagamentos alternativo** | LemonSqueezy | Sem taxa mensal | 5% + $0.50 por transação (cobre tax compliance global) |
| **Analytics** | PostHog | 1M eventos/mês | Generoso para início |
| **Analytics alternativo** | Plausible (self-hosted) | Grátis se self-hosted | Requer setup |
| **Monitoramento de erros** | Sentry | 5.000 eventos/mês | Suficiente para MVP |
| **Email transacional** | Resend | 3.000 emails/mês | Suficiente para MVP |
| **Email alternativo** | Mailgun | 1.000 emails/mês (trial) | Limitado |
| **CI/CD** | GitHub Actions | 2.000 min/mês (free) | Ilimitado para open source |
| **DNS/domínio** | Cloudflare (DNS) | Grátis | Domínio: ~$10/ano (único custo real) |
| **CDN** | Cloudflare | Generous free tier | Mais que suficiente |
| **File storage** | Supabase Storage | 1GB | Limite apertado para mídia |

### Custo real para lançar

| Item | Custo |
|------|-------|
| Domínio (.com) | ~$10/ano |
| Tudo mais | $0 |
| **Total ano 1** | **~$10** |

### Quando começar a pagar (e por quê)

A migração de free para paid deve seguir a receita, não a antecipá-la:

| Gatilho | Ação | Custo mensal |
|---------|------|-------------|
| **Primeiro MRR >$100** | Upgrade Supabase Pro ($25/mês) | $25 |
| **MRR >$300** | Upgrade Vercel Pro ($20/mês) | $20 |
| **MRR >$500** | Upgrade PostHog ($0 → usage-based) | ~$0-50 |
| **MRR >$1K** | Upgrade Sentry ($26/mês), Resend ($20/mês) | ~$46 |
| **MRR >$2K** | Considerar infra dedicada (Railway, Fly.io) | ~$50-100 |

**Regra de ouro:** infraestrutura não deve consumir mais que 10-15% do MRR. Se consome mais, ou o pricing está errado ou a stack está over-engineered.

### O que NÃO precisa no MVP

| Ferramenta/serviço | Por que não agora |
|-------------------|------------------|
| CDN premium (Fastly, CloudFront) | Cloudflare free é suficiente |
| APM (Datadog, New Relic) | PostHog + Sentry cobrem monitoramento básico |
| CRM (HubSpot, Salesforce) | Planilha + email funciona até 100 clientes |
| Marketing automation (Mailchimp Pro) | Resend + 1 sequência manual funciona |
| Design tools pagos (Figma Pro) | Figma free tier basta para 1 pessoa |

## Na prática

Stack recomendada para um SaaS indie em 2026 (custo $0 até ter receita):

```
Frontend:   Next.js / Vite → deploy no Vercel
Backend:    Supabase (PostgreSQL + Auth + Realtime + Storage)
Pagamento:  Stripe (paga só quando recebe)
Analytics:  PostHog (1M eventos/mês grátis)
Erros:      Sentry (5K eventos/mês grátis)
Email:      Resend (3K emails/mês grátis)
CI/CD:      GitHub Actions (grátis para open source)
DNS:        Cloudflare (grátis)
```

Para projetos open source (como o EstudeMe), o GitHub Actions é efetivamente ilimitado — o free tier para repos públicos não tem cap de minutos.

## Armadilhas

- **Over-engineering a stack antes de ter usuários.** Kubernetes, microservices, event sourcing — nada disso é necessário para 0-1.000 usuários. Monolito no Supabase resolve.

- **Pagar por ferramenta premium "por garantia".** Cada ferramenta paga adiciona custo fixo que corrói runway. O free tier existe para este estágio — use.

- **Ignorar os limites do free tier.** Supabase pausa projetos inativos no free tier. PostHog tem cap de eventos. Conheça os limites antes de depender deles em produção.

- **Trocar de stack por hype.** A stack que funciona é melhor que a stack que está na moda. Não mude de Supabase para PlanetScale para Turso porque leu um thread no Twitter. Mude quando tiver um problema real que a stack atual não resolve.

- **Esquecer o custo de domínio.** É o único custo real (~$10/ano). Registre cedo — domínios bons desaparecem.

## Veja também

- [[07 - O que é realmente um MVP]] — o que construir com essa stack
- [[03 - Risco calculado do solo founder]] — por que custo zero muda o cálculo de risco
- [[12 - Unit economics — CAC, LTV, MRR, churn]] — quando começar a gastar
- [[01 - Bootstrapping vs venture capital]] — por que não precisa de capital

## Referências

- **Documentação oficial** — Vercel, Supabase, Stripe, PostHog, Sentry, Resend, GitHub Actions, Cloudflare. Free tier terms atualizados em 2026.
- **Kahl, Arvid** — *Zero to Sold*. Bootstrapping econômico como princípio, não como limitação.
- **Comunidades** — Indie Hackers, r/SaaS. Discussões recorrentes sobre stack de custo zero e quando migrar para paid.
