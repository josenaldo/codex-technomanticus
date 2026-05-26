---
title: "Unit economics — CAC, LTV, MRR, churn"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - indie-hacker
  - empreendedorismo
  - modelo-negocio
  - metricas
  - unit-economics
aliases:
  - Unit economics
  - SaaS metrics
  - CAC LTV MRR churn
---

# Unit economics — CAC, LTV, MRR, churn

> [!abstract] TL;DR
> Unit economics são as métricas que dizem se cada cliente gera lucro ou prejuízo. As quatro métricas essenciais para indie hacker são: **MRR** (quanto entra por mês), **churn** (quanto sai por mês), **LTV** (quanto cada cliente vale no total), e **CAC** (quanto custa adquirir cada cliente). A razão LTV:CAC ≥ 3:1 é o benchmark de saúde. Para bootstrapped, o objetivo adicional é **CAC payback < 3 meses** — o dinheiro investido em aquisição precisa voltar rápido.

## O que é

Unit economics ("economia unitária") é a análise de receita e custo por unidade — neste caso, por cliente. Em SaaS, responde: "cada novo cliente me deixa mais rico ou mais pobre?"

Para VC-backed startups, a resposta pode ser "mais pobre por agora, mais rico no futuro" — porque há capital para absorver prejuízos temporários. Para indie hackers bootstrapped, a resposta precisa ser "mais rico agora" — porque não há capital para absorver nada.

## Por que importa

Sem unit economics, o indie hacker opera no escuro:
- "Estou crescendo?" → Sim, mas churn come o crescimento
- "Estou lucrando?" → Talvez, mas CAC está comendo a margem
- "Posso investir em marketing?" → Depende de quanto cada cliente retorna

Com unit economics, cada decisão é informada: "Se meu LTV é $120 e meu CAC é $30, posso gastar até $30 para adquirir um cliente e ainda ter 4× de retorno."

## Como funciona

### As 4 métricas essenciais

#### 1. MRR (Monthly Recurring Revenue)

**O que é:** Soma de todas as assinaturas recorrentes ativas no mês.

**Fórmula:** MRR = Σ (preço mensal de cada assinatura ativa)

**Variações importantes:**
- **New MRR:** receita de novos clientes este mês
- **Expansion MRR:** receita adicional de upgrades (free → pro)
- **Contraction MRR:** receita perdida por downgrades (pro → free)
- **Churned MRR:** receita perdida por cancelamentos

**Net MRR = New + Expansion - Contraction - Churned**

**Benchmark para indie hacker:** Crescimento de 10-20% mês a mês é forte nos primeiros 12 meses.

#### 2. Churn Rate

**O que é:** Percentual de clientes (ou receita) perdidos por mês.

**Fórmulas:**
- Customer churn = (clientes cancelados / clientes totais 30 dias atrás) × 100
- Revenue churn = (MRR perdido / MRR total 30 dias atrás) × 100

**Benchmark:** < 5% mensal = saudável. > 10% mensal = problema sério.

**Por que churn é tão importante:** Churn é compounding negativo. 5% churn mensal = ~46% dos clientes perdidos em 1 ano. 10% mensal = ~72% perdidos. Com churn alto, você corre na esteira — adquire clientes e perde na mesma velocidade.

#### 3. LTV (Customer Lifetime Value)

**O que é:** Receita total esperada de um cliente durante toda a relação.

**Fórmula simplificada:** LTV = ARPU / churn rate mensal
- ARPU = Average Revenue Per User (receita média por usuário/mês)

**Exemplo:** Se ARPU = $10/mês e churn = 5%/mês → LTV = $10 / 0.05 = $200

**O que LTV diz:** Quanto você pode investir para adquirir um cliente e quanto precisa de retenção para que o investimento retorne.

#### 4. CAC (Customer Acquisition Cost)

**O que é:** Custo total para adquirir um novo cliente pagante.

**Fórmula:** CAC = (total gasto em aquisição no período) / (novos clientes pagantes no período)

**Para indie hackers:** O CAC ideal é ~$0 (orgânico via SEO, comunidade, word-of-mouth). Quando investe em ads ou ferramentas de marketing, CAC sobe. Monitorar para garantir que não corroa a margem.

### A razão LTV:CAC

| LTV:CAC | O que significa |
|---------|----------------|
| < 1:1 | Cada cliente custa mais do que vale — insustentável |
| 1:1 | Break-even — sem lucro após aquisição |
| 3:1 | **Benchmark saudável** — $3 de retorno para cada $1 investido |
| 5:1+ | Excelente — mas pode significar sub-investimento em growth |

### CAC Payback Period

**O que é:** Quantos meses leva para recuperar o custo de aquisição de um cliente.

**Fórmula:** CAC Payback = CAC / ARPU

**Exemplo:** CAC = $30, ARPU = $10/mês → Payback = 3 meses

**Benchmark para bootstrap:** < 6 meses. Ideal: < 3 meses. Se > 12 meses, o modelo precisa de ajuste (ou CAC alto demais, ou preço baixo demais).

### NRR (Net Revenue Retention)

**O que é:** Mede se os clientes existentes estão gastando mais ou menos ao longo do tempo, descontando churn.

**Fórmula:** NRR = (MRR início + expansion - contraction - churned) / MRR início × 100

**Benchmark:** > 100% = clientes existentes crescem mais do que churnam. É o "santo graal" — crescimento mesmo sem novos clientes.

### Dashboard mínimo

| Métrica | Frequência | Ferramenta |
|---------|-----------|-----------|
| MRR | Semanal | Stripe Dashboard |
| Churn | Mensal | Stripe + planilha |
| LTV | Mensal | Cálculo manual (ARPU/churn) |
| CAC | Mensal | Planilha (custos / novos clientes) |
| NRR | Mensal | Planilha |
| Active users | Semanal | PostHog |

## Na prática

Cenário de referência para SaaS indie a $10/mês:

| Cenário | Clientes | MRR | Churn | LTV | CAC | LTV:CAC |
|---------|----------|-----|-------|-----|-----|---------|
| **Dia 0** | 0 | $0 | — | — | — | — |
| **Mês 3** | 20 | $200 | 10% | $100 | $0 (orgânico) | ∞ |
| **Mês 6** | 100 | $1K | 5% | $200 | $5 | 40:1 |
| **Mês 12** | 400 | $4K | 4% | $250 | $10 | 25:1 |
| **Meta: Mês 18** | 2.000 | $20K | 3% | $333 | $20 | 17:1 |

Note: nos primeiros meses com CAC ~$0 (orgânico), a razão LTV:CAC é artificialmente alta. Quando começar a investir em aquisição, ela normaliza.

## Armadilhas

- **Medir MRR sem medir churn.** MRR crescendo com churn de 10% é ilusão: parece crescimento, mas é esteira. Net MRR é a métrica real.

- **CAC = $0 não significa que aquisição é grátis.** Seu tempo tem valor. Se gasta 20h/semana criando conteúdo, esse é um custo de aquisição — mesmo que não saia do bolso.

- **Calcular LTV com dados de 2 meses.** LTV precisa de pelo menos 6 meses de dados de churn para ser confiável. Antes disso, é estimativa.

- **Otimizar CAC antes de otimizar retenção.** Se o balde está furado (churn alto), encher mais rápido (mais aquisição) não resolve. Conserte o balde primeiro.

- **Ignorar revenue churn vs customer churn.** Se seus melhores clientes churnam e os piores ficam, o negócio piora mesmo com customer churn "aceitável".

## Veja também

- [[11 - Pricing para SaaS bootstrapped]] — pricing afeta diretamente todas as métricas
- [[10 - Open-core — a linha entre grátis e pago]] — modelo que define ARPU
- [[17 - Retenção e redução de churn]] — como melhorar churn
- [[02 - O conceito de enough — Company of One]] — quantos clientes = "enough"

## Referências

- **Baremetrics** — baremetrics.com. Dashboard de métricas SaaS com benchmarks públicos.
- **Stripe Atlas** — Blog sobre unit economics e SaaS metrics para founders.
- **ProfitWell (Patrick Campbell)** — Pesquisas sobre churn, pricing e unit economics em SaaS.
- **CloudZero** — Guias sobre LTV:CAC ratio e benchmarks.
- **Kahl, Arvid** — *Zero to Sold*. Métricas no estágio "Stability" do negócio bootstrapped.
