---
title: "Por que performance importa"
created: 2026-07-05
updated: 2026-07-05
type: concept
status: seedling
fase: iniciado
tags:
  - web-performance
  - core-web-vitals
  - medição
publish: true
---

# Por que performance importa

> [!abstract] TL;DR
> Performance web não é um capricho de engenharia — é uma alavanca de **receita, retenção e visibilidade**. Cada 100 ms de espera a mais derruba conversão; cada segundo extra de carregamento sangra usuários pela porta dos fundos. O Google transformou isso em sinal de ranking (Core Web Vitals), então lentidão custa duas vezes: no usuário que desiste e no tráfego orgânico que nunca chega. A aposta deste domínio inteiro cabe em uma frase: **você não otimiza o que não mede** — e é por isso que começamos por medição, não por otimização.

## O usuário que você nunca vê ir embora

Imagine uma loja física onde, a cada segundo que o cliente espera no caixa, 10% das pessoas na fila simplesmente evaporam. Você nunca as vê saindo — elas não reclamam, não pedem o livro de reclamações, não voltam. Só somem. Na web, é exatamente isso que acontece, e o mais cruel é que **é invisível no seu dia a dia**: você desenvolve num MacBook potente, numa rede de fibra, com o cache quente. A página voa. Para o usuário num Android intermediário, numa rede 4G instável, com o cache frio, a mesma página se arrasta — e ele fecha a aba antes do seu conteúdo aparecer.

Esse é o problema central da performance web: **a experiência que você mede na sua máquina não é a experiência que o usuário vive**. E a experiência do usuário, por mais silenciosa que seja o abandono, aparece brutalmente nos números do negócio.

> [!question]- Se o usuário desiste em silêncio, como eu sei que estou perdendo alguém?
> Você não sabe — a menos que instrumente. É por isso que "performance" e "medição" são inseparáveis. O abandono por lentidão não gera erro, não gera log, não gera ticket de suporte. Ele só aparece se você coletar métricas de carregamento e de interação dos usuários reais e cruzar com taxa de conversão. Sem instrumentação, o dinheiro escorre por um ralo que você não consegue ver. Essa é a razão de a nota 06 deste galho existir.

## O que a lentidão custa em dinheiro

Não são achismos. Há duas décadas a indústria mede a relação entre velocidade e receita, e o padrão se repete em todo lugar.

O estudo mais citado é o **"Milliseconds Make Millions"**, conduzido pela Deloitte Digital e comissionado pelo Google (2020). Eles instrumentaram sites móveis de marcas de varejo, viagem, luxo e geração de leads na Europa e nos EUA durante quatro semanas, e mediram o efeito de melhorar a velocidade em apenas **0,1 segundo** (100 ms):

| Setor | Efeito de +0,1s de velocidade |
|-------|-------------------------------|
| Varejo | Conversão **+8,4%**, ticket médio **+9,2%** |
| Viagem | Conversão **+10,1%** |
| Luxo | Progressão pro carrinho **+40,1%** (páginas de produto) |
| Geração de leads | Progressão no funil de formulário **+21,6%** |

Leia de novo: **0,1 segundo**. Não é reescrever a arquitetura — é o custo de uma fonte mal carregada, de uma imagem sem otimizar, de um script de terceiros bloqueando a renderização.

O outro lado da moeda — quanto a lentidão **afasta** — vem do próprio Google, que cruzou tempo de carregamento com probabilidade de abandono (bounce) em milhões de páginas móveis:

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
graph LR
    A["1s → 3s"] -->|"+32% de bounce"| B["3s → 5s"]
    B -->|"+90% de bounce"| C["5s → 6s"]
    C -->|"+106% de bounce"| D["6s → 10s"]
    D -->|"+123% de bounce"| E[Abandono]
    style A fill:#4A90D9,color:#fff
    style C fill:#F5A623,color:#000
    style D fill:#D0021B,color:#fff
    style E fill:#D0021B,color:#fff
```

Quando o carregamento passa de 1 para 3 segundos, a probabilidade de o usuário abandonar sobe **32%**. De 1 para 5 segundos, **90%**. De 1 para 10 segundos, **123%**. A curva não é linear — ela acelera. A Deloitte encontrou o limiar cognitivo: **passados 1.000 ms (1 segundo), o usuário perde o foco na tarefa** que estava fazendo.

Os casos individuais das grandes empresas contam a mesma história, e viraram folclore da engenharia justamente por serem consistentes:

- A **Amazon** calculou, ainda em 2006, que cada 100 ms de latência custava **1% em vendas** (Greg Linden).
- A **BBC** descobriu que perdia **10% dos usuários** para cada segundo adicional de carregamento.
- O **Pinterest** reduziu o tempo de espera percebido em 40% e viu **+15% de tráfego orgânico** e de cadastros.

> [!info] Números envelhecem — o padrão, não
> Percentuais específicos (o "1% da Amazon", o "10% da BBC") são de estudos de anos diferentes, com metodologias diferentes, e devem ser citados como **ilustração da direção**, não como lei física. O que se mantém estável há 20 anos é a **forma da relação**: mais lento → menos conversão → menos receita, com a curva de abandono acelerando conforme a espera cresce. Sempre prefira medir o **seu** site a extrapolar o número de outra empresa.

## O segundo custo: o Google te vê lento

Até aqui falamos do usuário que já chegou na sua página. Mas há um custo anterior: **o usuário que nunca chega porque você caiu no ranking**.

Desde 2021, o Google incorporou a performance ao seu conjunto de sinais de ranqueamento, sob o guarda-chuva do **Page Experience**. O coração desse sinal são os **Core Web Vitals** — três métricas que capturam carregamento, responsividade e estabilidade visual (você vai conhecê-las em detalhe na próxima nota). A partir de **12 de março de 2024**, o trio passou a ser **LCP** (Largest Contentful Paint), **INP** (Interaction to Next Paint) e **CLS** (Cumulative Layout Shift) — o INP substituiu a antiga métrica FID nessa data.

Isso muda a natureza do problema. Performance deixou de ser só "experiência do usuário" e virou **aquisição**: um site lento aparece menos nas buscas, recebe menos visitantes orgânicos, e paga mais caro por cada clique que compra. O ralo agora tem dois furos — a conversão que você perde *e* o tráfego que nunca ganha.

> [!warning] Não superestime o peso no ranking
> O próprio Google descreve os Core Web Vitals como um sinal **leve** — conteúdo relevante e autoridade continuam pesando muito mais. A performance é um **desempate** e um **piso de qualidade**, não uma bala de prata de SEO. Otimizar CWV num site com conteúdo fraco não salva o ranking; ignorar CWV num site bom joga fora um desempate de graça. Trate-o como higiene, não como estratégia isolada.

## A aposta do domínio: medir antes de otimizar

Se lentidão custa tão caro, a reação instintiva é sair otimizando: minificar isso, lazy-load aquilo, trocar de CDN. Esse é o erro clássico. Otimizar às cegas é gastar esforço no que talvez nem seja o gargalo — e não ter como provar que melhorou.

O princípio que organiza este domínio inteiro é:

> **Você não otimiza o que não mede.**

Antes de tocar em qualquer técnica de carregamento ou de runtime, você precisa responder três perguntas com **números**, não com intuição:

1. **Qual métrica está ruim?** LCP? INP? CLS? Cada uma aponta para uma família de causas diferente.
2. **Para quem está ruim?** A média esconde tudo. O seu p75 no celular pode ser péssimo enquanto a mediana no desktop parece ótima.
3. **Quanto isso custa?** Ligar a métrica técnica ao número de negócio (conversão, bounce, receita) é o que transforma "a página está lenta" em "estamos perdendo X% de conversão por causa do LCP no mobile".

Responder a essas três perguntas é *literalmente* o conteúdo dos Galhos 1. Só depois de medir — e de saber ler o que a medição diz — é que faz sentido carregar mais rápido (Galho 2), manter a página responsiva (Galho 3) e sustentar isso em produção (Galho 4).

**Por que performance importa em uma frase:** porque a lentidão cobra em receita, retenção e ranking ao mesmo tempo — e o único jeito de estancar essa sangria é medir onde ela acontece, para quem, e quanto custa.

## Como explicar em inglês

Em entrevista, o enquadramento que impressiona é o que **liga a métrica técnica ao resultado de negócio** — não o que recita números de cor.

> "Web performance isn't just an engineering nicety — it's a revenue lever. Studies like Deloitte's *Milliseconds Make Millions* show that even a 0.1-second speed improvement can lift retail conversions by around 8%. And since 2021, Google folds performance into its ranking signals through Core Web Vitals, so a slow site loses twice: users bounce, and organic traffic never arrives. That's why my first move is never to optimize blindly — it's to measure. You can't optimize what you don't measure."

| PT | EN |
|----|----|
| Taxa de rejeição / abandono | Bounce rate |
| Taxa de conversão | Conversion rate |
| Ticket médio | Average order value (AOV) |
| Sinal de ranqueamento | Ranking signal |
| Tráfego orgânico | Organic traffic |
| Gargalo | Bottleneck |
| Você não otimiza o que não mede | You can't optimize what you don't measure |

## O que vem a seguir

Agora que a aposta está clara — performance custa dinheiro e visibilidade, e o remédio começa por medir —, o próximo passo é conhecer **exatamente o que medir**. O Google destilou a experiência do usuário em três métricas, e é impossível conversar sobre performance moderna sem dominá-las.

- [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/02 - Os três Core Web Vitals|02 — Os três Core Web Vitals]] — LCP, INP e CLS: o que cada um mede, os limiares de "bom", e por que esses três (a nota-âncora do galho).
- [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/03 - Lab vs Field|03 — Lab vs Field]] — por que a média mente e por que "para quem está ruim" depende de medir usuários reais.

## Fontes

- **Deloitte Digital (comissionado pelo Google)** — [*Milliseconds Make Millions*](https://www.deloitte.com/ie/en/services/consulting/research/milliseconds-make-millions.html) ([relatório PDF no Think with Google](https://www.thinkwithgoogle.com/_qs/documents/9757/Milliseconds_Make_Millions_report_hQYAbZJ.pdf)) — estudo de referência sobre o efeito de 0,1s de velocidade na conversão, por setor.
- **Google Search Central** — [*Introducing INP to Core Web Vitals*](https://developers.google.com/search/blog/2023/05/introducing-inp) — anúncio oficial da substituição de FID por INP (efetiva 12/03/2024).
- **Addy Osmani** — [*The History of Core Web Vitals*](https://addyosmani.com/blog/core-web-vitals/) — linha do tempo das métricas e do papel delas no Page Experience, por um dos engenheiros do Chrome.
- **Think with Google** — benchmarks de probabilidade de bounce por tempo de carregamento móvel (curva 1s→3s→5s→10s) — dados agregados de milhões de páginas.
