---
title: "O business case da performance"
created: 2026-07-06
updated: 2026-07-06
type: concept
status: seedling
fase: Magus
tags:
  - web-performance
  - produção
  - business-case
  - priorização
publish: true
---

# O business case da performance

> [!abstract] TL;DR
> Performance compete por tempo de engenharia com features, e perde toda discussão travada em jargão técnico ("nosso LCP está em 3,2 s"). Para ganhar prioridade, você traduz **milissegundos em dinheiro**: liga a métrica ao número de negócio (conversão, receita, bounce, retenção) que o Galho 1 já provou existir. As táticas: usar o seu **próprio RUM** para estimar o impacto (não só estudos de terceiros), rodar **experimentos** (A/B de performance) para provar causalidade, apresentar em **linguagem de stakeholder** (receita, não LCP), e priorizar por **impacto × esforço**. O business case é o que transforma performance de "nice to have" técnico em investimento com ROI.

## O problema: performance perde a briga por prioridade

Você sabe medir, otimizar, prevenir regressão e diagnosticar. Mas na reunião de priorização, "melhorar o LCP do checkout" fica atrás de "nova feature X" — de novo. Por quê? Porque você apresentou um **número técnico** ("o LCP está em 3,2 s") para pessoas que decidem em **números de negócio** (receita, conversão, custo). Elas não sabem o que fazer com "3,2 segundos"; sabem exatamente o que fazer com "estamos perdendo R$ X por mês".

O melhor trabalho técnico do mundo não é feito se ninguém aprovar o tempo para fazê-lo. O business case é a ponte entre a métrica que *você* enxerga e a decisão que o *negócio* toma — e construí-lo é uma habilidade de engenharia sênior tão importante quanto otimizar o INP.

## Traduzir milissegundos em dinheiro

O Galho 1 ([[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/01 - Por que performance importa|G1 nota 01]]) provou que a relação existe: 0,1 s de velocidade → +8% de conversão no varejo (Deloitte); a curva de bounce que acelera com a espera. Aqui você usa esses fatos como **argumento de investimento**, em três níveis de força crescente:

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
graph LR
    A["Estudos de terceiros<br/>(Deloitte, Google)"] -->|fraco: 'outras empresas'| B["Seu RUM correlacionado<br/>(seu p75 × sua conversão)"]
    B -->|forte: 'nossos dados'| C["Experimento A/B<br/>(prova causal)"]
    C -->|mais forte: 'nós provamos'| D[💰 caso de investimento]
    style B fill:#4A90D9,color:#fff
    style C fill:#4A90D9,color:#fff
    style D fill:#F5A623,color:#000
```

1. **Estudos de terceiros** (Deloitte, Google, casos de Amazon/Pinterest): úteis para introduzir a ideia, mas fracos porque são "outras empresas, outro contexto". Servem de gancho, não de prova.
2. **Seu próprio RUM correlacionado:** cruze o seu RUM (nota 03) com os seus dados de conversão. "Usuários no quartil mais rápido de LCP convertem 2× mais que os do quartil mais lento" é infinitamente mais persuasivo que qualquer estudo externo — são *os seus* usuários e *o seu* dinheiro. (Cuidado: correlação não é causa — usuários rápidos podem ter aparelhos melhores e mais renda.)
3. **Experimento (A/B de performance):** a prova de ouro. Sirva uma versão mais lenta (ou mais rápida) para uma fração dos usuários e meça a diferença de conversão. Isola a causalidade que a correlação não garante. É o que empresas grandes fazem para cravar o ROI de performance.

## Falar a língua de quem decide

O mesmo fato, dois enquadramentos:

| ❌ Linguagem técnica | ✅ Linguagem de negócio |
|----------------------|-------------------------|
| "O LCP do checkout está em 3,4 s" | "A página de pagamento demora a carregar, e usuários abandonam antes de comprar" |
| "Reduzimos o TBT em 200 ms" | "A página responde mais rápido ao toque; menos gente desiste no meio" |
| "Estamos com CLS de 0,3" | "Elementos pulam na tela e o usuário clica no botão errado, gerando erros e devoluções" |
| "Precisamos de um budget no CI" | "Queremos impedir que a próxima feature deixe o site lento e derrube vendas" |

A regra: sempre termine a frase em **impacto no usuário ou no dinheiro**, nunca na métrica. A métrica é o *meio*; o resultado de negócio é o *fim* que interessa a quem aprova.

> [!question]- E se eu não tiver dados de conversão para correlacionar (ex: um site que não vende nada)?
> O business case não é só receita direta — é **qualquer resultado que a organização valoriza**. Para um site de conteúdo: tempo na página, páginas por sessão, retorno de visitantes, receita de anúncios (que cai com bounce). Para um SaaS: ativação, retenção, tickets de suporte por lentidão. Para o setor público/interno: produtividade, custo de suporte, acessibilidade. E há sempre o **SEO** (G1 nota 01): performance ruim derruba ranking, que derruba tráfego — um custo de aquisição mensurável. O truque é descobrir qual é a **métrica-norte do negócio** e ligar performance a ela; sempre há uma.

> [!warning] Prometer um número de ROI que você não pode sustentar
> **O que acontece:** para vender o projeto, você promete "vamos aumentar a conversão em 8% melhorando o LCP" (extrapolando o estudo da Deloitte). Entrega a melhoria de LCP, a conversão sobe 1%, e a sua credibilidade — e a da causa "performance" — afunda. **Por quê:** os percentuais de estudos externos são de outros contextos; a sua elasticidade real é diferente e desconhecida até você medir. Prometer o número dos outros é apostar credibilidade em dado emprestado. **Como evitar:** apresente estudos como **direção** ("mais rápido tende a converter mais"), não como garantia. Para prometer número, meça o **seu** (correlação do RUM, e idealmente um A/B). Sub-prometa e supere; a confiança conquistada é o que financia o *próximo* investimento em performance.

**O business case em uma frase:** performance ganha prioridade quando você traduz a métrica técnica no número de negócio que ela move — usando seu próprio RUM (e, no ideal, um A/B) em vez de estudos emprestados, falando a língua de quem decide (receita, não LCP), e priorizando por impacto × esforço.

## Como explicar em inglês

> "Performance competes with features for engineering time, and it loses every argument framed in jargon like 'our LCP is 3.2 seconds.' To win priority, I translate milliseconds into money — tying the metric to the business number it moves: conversion, revenue, retention. I lean on my **own RUM** correlated with conversion data, not just third-party studies, and ideally an **A/B test** to prove causation. And I speak the stakeholder's language: not 'we cut TBT by 200ms' but 'the page responds faster to taps, so fewer people abandon checkout.' One caution: I present external studies as direction, never as a promised ROI number — I only promise numbers I've measured on our own users."

| PT | EN |
|----|----|
| Argumento de negócio | Business case |
| Retorno sobre investimento | Return on investment (ROI) |
| Correlação vs. causa | Correlation vs. causation |
| Métrica-norte | North-star metric |
| Impacto × esforço | Impact vs. effort |
| Parte interessada | Stakeholder |

## O que vem a seguir

Com o business case, você consegue aprovação para *um* projeto de performance. Mas aprovação pontual não sustenta performance ao longo do tempo — no próximo trimestre a pressão volta e o site apodrece de novo. O capstone do domínio é sobre transformar isso em algo permanente: uma **cultura** em que performance é responsabilidade de todos, o tempo todo.

- [[03-Dominios/Tecnologia/Web Performance/Performance em Produção/08 - Cultura de performance|08 — Cultura de performance]] — ownership, prevenir o apodrecimento; o capstone do domínio inteiro.

## Fontes

- **web.dev (Google)** — [*The business impact of Core Web Vitals*](https://web.dev/case-studies/) — estudos de caso ligando CWV a métricas de negócio.
- **web.dev (Google)** — [*Value of speed / conversion*](https://web.dev/articles/value-of-speed) — como quantificar o impacto de performance em receita.
- **WPO Stats** — [wpostats.com](https://wpostats.com/) — coletânea de casos reais de performance × negócio, útil como munição (e como direção, não promessa).
