---
title: "Landing page de validação e sinais de demanda"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - indie-hacker
  - empreendedorismo
  - validacao
  - landing-page
  - demanda
aliases:
  - Landing page de validação
  - Sinais de demanda
  - Waitlist validation
---

# Landing page de validação e sinais de demanda

> [!abstract] TL;DR
> Após entrevistas Mom Test, o próximo passo de validação é testar messaging com uma landing page simples: problema → solução → CTA. Não é um site bonito — é um experimento. A métrica que importa é conversão (visitante → email ou pre-order), não tráfego. Uma taxa de conversão de 5-10% em emails de waitlist indica interesse real. Pre-orders com pagamento são o sinal mais forte possível antes de construir. Em 2026, ferramentas como Carrd, Framer, ou HTML estático permitem lançar uma landing page em horas, não semanas.

## O que é

Uma landing page de validação não é o site do produto — é um experimento de mercado disfarçado de página web. O objetivo é testar se a messaging (problema + solução + proposta de valor) ressoa com o público-alvo o suficiente para gerar ação: deixar email, fazer pre-order, ou agendar uma conversa.

A landing page é o elo entre validação qualitativa (entrevistas) e validação quantitativa (números). Entrevistas dizem "essas pessoas têm essa dor"; a landing page diz "essa mensagem, nesse canal, atrai X% de conversão".

## Por que importa

Há um gap perigoso entre "20 entrevistados confirmaram a dor" e "pessoas na internet clicam no meu CTA". Entrevistas são contextuais — a pessoa está na sua frente, com atenção. Landing page testa a realidade: **quando a pessoa está scrollando distraída, a sua messaging para ela?**

Sem essa validação, o risco é construir algo que resolve um problema real mas que ninguém encontra ou entende pela comunicação.

## Como funciona

### Estrutura mínima da landing page

A página inteira cabe em uma tela (acima do fold). Sem scroll infinito. Sem seção de blog. Sem FAQ com 30 perguntas.

| Seção | Conteúdo | Exemplo |
|-------|----------|---------|
| **Headline** | O problema em 1 frase | "Está estudando sozinho e esquecendo tudo?" |
| **Subheadline** | A solução em 1 frase | "O EstudeMe organiza, agenda e revisa pra você." |
| **3 bullet points** | Os 3 diferenciais | ✅ Repetição espaçada inteligente / ✅ Integração com Obsidian / ✅ Open source |
| **CTA** | Ação clara | Botão: "Quero acesso antecipado" → formulário de email |
| **Prova social (opcional)** | Qualquer forma de credibilidade | "Open source no GitHub" / "Built by a dev, for devs" |

### Métricas que importam

| Métrica | O que mede | Meta |
|---------|-----------|------|
| **Taxa de conversão** (visitante → email) | Interesse real | 5-10% = bom; >10% = excelente |
| **Volume de emails** | Tamanho da audiência | 100 em 30 dias = sinal verde |
| **Fonte do tráfego** | Qual canal funciona | Qual subreddit/comunidade gera mais conversão |
| **Taxa de abertura do email de confirmação** | Qualidade do lead | >60% = lead quente |

O que **não** importa: bounces, tempo na página, pageviews totais. São métricas de vaidade neste estágio.

### Hierarquia de sinais de demanda

Ordenados do mais fraco ao mais forte:

| # | Sinal | Força | O que prova |
|---|-------|-------|-------------|
| 1 | Pageview | ⚪ Fraca | A pessoa clicou (pode ter sido acidente) |
| 2 | Email na waitlist | 🟡 Média | Interesse real, mas sem compromisso financeiro |
| 3 | Compartilhou com alguém | 🟡 Média | Valor percebido ("isso resolveria meu problema") |
| 4 | Perguntou quando lança | 🟢 Forte | Urgência real |
| 5 | Pre-order com pagamento ($1-10) | 🟢🟢 Muito forte | Willingness-to-pay comprovada |
| 6 | Ofereceu dinheiro espontaneamente | 🟢🟢🟢 Sinal máximo | Dor tão grande que paga antes de ver |

### Ferramentas (custo zero em 2026)

| Ferramenta | Para quê | Custo |
|-----------|---------|-------|
| **Carrd** | Landing page simples | Free tier (1 site) |
| **Framer** | Landing page mais elaborada | Free tier |
| **HTML estático + GitHub Pages** | Controle total, zero custo | Grátis |
| **Mailchimp / Buttondown** | Coleta de emails | Free tier |
| **Stripe / LemonSqueezy** | Pre-orders com pagamento | Só paga quando recebe |
| **PostHog / Plausible** | Analytics sem cookies | Free tier |

### Onde divulgar

O tráfego para a landing page não vem de SEO (não há tempo). Vem de:

1. **Comunidades onde a persona vive** — Reddit (r/learnprogramming, r/ObsidianMD, r/SaaS), Discord
2. **Posts úteis com link no perfil** — não spam; contribua primeiro
3. **Lista dos entrevistados do Mom Test** — "Lembra da conversa? A landing page está no ar"
4. **Twitter/X do projeto** — se já existe
5. **Show HN** (Hacker News) — para devtools, funciona muito bem

Regra: **não compre ads neste estágio**. Se a messaging é boa, tráfego orgânico de 2-3 comunidades basta para testar conversão.

## Na prática

O fluxo completo de validação via landing page:

1. Construa a página (1-2 horas com Carrd ou HTML)
2. Compartilhe em 3 comunidades relevantes com post genuíno (não spam)
3. Acompanhe por 30 dias
4. Analise:
   - **100+ emails em 30 dias** → sinal verde, prossiga para MVP
   - **20-100 emails** → messaging ou canal pode precisar de ajuste
   - **<20 emails** → volte ao Mom Test, revise o problema

## Armadilhas

- **Gastar semanas na landing page.** É um experimento, não uma obra de arte. Se leva mais de 1 dia, está over-engineering.

- **Otimizar para tráfego em vez de conversão.** 10.000 visitas com 0.1% de conversão = 10 emails. 200 visitas com 10% de conversão = 20 emails. O segundo cenário é melhor.

- **Não ter CTA claro.** "Saiba mais" não é CTA. "Quero acesso antecipado" é CTA. "Pague $5 para reservar" é CTA melhor ainda.

- **Ignorar a fonte do tráfego.** Se 80% dos emails vieram do r/ObsidianMD e 0% do LinkedIn, isso é informação valiosa sobre canal de distribuição.

- **Usar métricas de vaidade como validação.** "Tive 5.000 pageviews!" não significa nada sem conversão. A pergunta é: quantos desses 5.000 agiram?

## Veja também

- [[04 - The Mom Test — entrevistas que não mentem]] — validação qualitativa que precede
- [[05 - Nicho vs mercado amplo]] — para quem a landing page fala
- [[07 - O que é realmente um MVP]] — o que construir depois de validar
- [[16 - Lançamento — de soft launch ao Product Hunt]] — quando a landing page vira produto

## Referências

- **Fitzpatrick, Rob** — *The Mom Test*. Compromisso (email, pre-order) como sinal de validação.
- **Kahl, Arvid** — *Zero to Sold*. Estágio "Preparation": landing page como teste de mercado.
- **Lavingia, Sahil** — *The Minimalist Entrepreneur*. "Start, then learn" — lance a página antes de perfeiçoar.
- **Indie Hackers** — Discussões sobre taxas de conversão de waitlist e resultados de Show HN posts.
