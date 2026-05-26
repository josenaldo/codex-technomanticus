---
title: "Fator R — tributação para devs PJ"
created: 2026-05-06
updated: 2026-05-06
type: concept
status: seedling
publish: true
tags:
  - empreendedorismo
  - tributacao
  - simples-nacional
  - fator-r
  - pj
  - dev
aliases:
  - Fator R
  - Anexo III vs V
  - Simples Nacional para devs
---
# Fator R — tributação para devs PJ

> [!abstract] TL;DR
> Fator R é a razão **folha de pagamento ÷ receita bruta**, ambas dos últimos 12 meses. Se ≥ 28%, sua empresa de serviços paga DAS pelo **Anexo III** (alíquota efetiva começando em **6%**); se < 28%, cai no **Anexo V** (começando em **15,5%**). Para devs PJ solo, o jogo é dimensionar o pró-labore o suficiente para cruzar o gatilho dos 28% e capturar o Anexo III. Em 2026 a conta ficou mais favorável: a nova isenção de IRPF até R$ 5.000/mês (com redução gradual até R$ 7.350) reduziu o custo pessoal de subir o pró-labore. A reforma tributária (LC 214/2025) ainda preserva o regime em 2026, mas exige decisão até **setembro/2026** sobre Simples tradicional vs **Simples híbrido** a partir de 2027.

## O que é

O **Fator R** é o critério que o Simples Nacional usa para decidir, em empresas prestadoras de serviços com CNAE sujeito a essa regra (parte do Anexo V), se o tributo do mês será calculado pelo Anexo III (mais barato) ou pelo Anexo V (mais caro).

A fórmula:

$$
\text{Fator R} = \frac{\text{Folha de pagamento (12 meses)}}{\text{Receita bruta (12 meses)}}
$$

- **≥ 28%** → tributação pelo **Anexo III**
- **< 28%** → tributação pelo **Anexo V**

O cálculo é feito **mês a mês**, sempre olhando a janela móvel dos últimos 12 meses. Mudar pró-labore hoje não muda tudo amanhã — o efeito entra gradualmente.

> [!info] Onde a folha conta
> "Folha" inclui pró-labore, salários CLT, INSS patronal, FGTS, férias e 13º. Para o dev PJ solo, na prática a folha **é o pró-labore** (mais o INSS do sócio).

## Por que importa para devs

A diferença entre os dois anexos é brutal logo na primeira faixa:

| Anexo | Faixa 1 (até R$ 180k/ano) | Carga em 12 meses de R$ 240k |
|-------|---------------------------|-------------------------------|
| III   | 6,00%                     | 7,30% efetiva                 |
| V     | 15,50%                    | 16,13% efetiva                |

Para um dev faturando R$ 20k/mês (R$ 240k/ano), a diferença entre cair no III ou no V é de aproximadamente **R$ 21 mil por ano** apenas no DAS. Por isso o Fator R virou eixo central de planejamento tributário PJ no setor de tecnologia.

## Como funciona

### A janela móvel de 12 meses

O Fator R não enxerga o mês isolado — ele acumula. Significa que:

- Quem está abrindo empresa precisa de tempo até "construir" a folha que sustenta o Anexo III
- Mudanças de pró-labore se diluem ao longo de 12 meses
- Um mês sem retirada de pró-labore (férias, viagem) pode derrubar o fator e jogar o mês seguinte no Anexo V

### Anexo III — tabela 2026

| Faixa | Receita bruta anual | Alíquota nominal | Valor a deduzir |
|-------|---------------------|------------------|-----------------|
| 1ª    | até R$ 180.000      | 6,00%            | R$ 0            |
| 2ª    | R$ 180.000,01 a R$ 360.000 | 11,20%    | R$ 9.360        |
| 3ª    | R$ 360.000,01 a R$ 720.000 | 13,50%    | R$ 17.640       |
| 4ª    | R$ 720.000,01 a R$ 1,8mi   | 16,00%    | R$ 35.640       |
| 5ª    | R$ 1,8mi a R$ 3,6mi        | 21,00%    | R$ 125.640      |
| 6ª    | R$ 3,6mi a R$ 4,8mi        | 33,00%    | R$ 648.000      |

### Anexo V — tabela 2026

| Faixa | Receita bruta anual | Alíquota nominal | Valor a deduzir |
|-------|---------------------|------------------|-----------------|
| 1ª    | até R$ 180.000      | 15,50%           | R$ 0            |
| 2ª    | R$ 180.000,01 a R$ 360.000 | 18,00%    | R$ 4.500        |
| 3ª    | R$ 360.000,01 a R$ 720.000 | 19,50%    | R$ 9.900        |
| 4ª    | R$ 720.000,01 a R$ 1,8mi   | 20,50%    | R$ 17.100       |
| 5ª    | R$ 1,8mi a R$ 3,6mi        | 23,00%    | R$ 62.100       |
| 6ª    | R$ 3,6mi a R$ 4,8mi        | 30,50%    | R$ 540.000      |

### Alíquota efetiva

A alíquota da tabela é nominal — o que você efetivamente paga é menor (ou igual) graças à parcela a deduzir:

$$
\text{Alíquota efetiva} = \frac{\text{RBT12} \times \text{Alíquota nominal} - \text{Valor a deduzir}}{\text{RBT12}}
$$

Onde **RBT12** é a receita bruta acumulada nos últimos 12 meses.

Exemplo prático para R$ 240k/ano no Anexo III:

$$
\frac{240.000 \times 0{,}112 - 9.360}{240.000} = \frac{17.520}{240.000} \approx 7{,}30\%
$$

## Cenários comparados — com vs sem Fator R

Premissas: dev solo, ME no Simples, sem funcionários, exportação ou serviço nacional sem retenção relevante. Valores recalculados com fórmula oficial; INSS patronal já embutido no DAS em ambos os anexos. IRPF estimado considerando a tabela 2026 (isenção até R$ 5k, redução gradual até R$ 7.350).

### R$ 5.000/mês (R$ 60k/ano)

| Item | Com Fator R (Anexo III) | Sem Fator R (Anexo V) |
|------|--------------------------|------------------------|
| Pró-labore | R$ 1.500 | R$ 1.000 |
| DAS (alíq. efetiva) | R$ 300 (6,00%) | R$ 775 (15,50%) |
| INSS sócio (11%) | R$ 165 | R$ 110 |
| IRPF | R$ 0 | R$ 0 |
| Contador | R$ 300 | R$ 300 |
| **Total custos** | **R$ 765** | **R$ 1.185** |
| **Carga efetiva** | **~15,3%** | **~23,7%** |

**Diferença: ~R$ 420/mês a favor do Anexo III.**

### R$ 10.000/mês (R$ 120k/ano)

| Item | Com Fator R (Anexo III) | Sem Fator R (Anexo V) |
|------|--------------------------|------------------------|
| Pró-labore | R$ 3.000 | R$ 1.500 |
| DAS | R$ 600 (6,00%) | R$ 1.550 (15,50%) |
| INSS sócio | R$ 330 | R$ 165 |
| IRPF | R$ 0 (isento na nova regra) | R$ 0 |
| Contador | R$ 300 | R$ 300 |
| **Total custos** | **R$ 1.230** | **R$ 2.015** |
| **Carga efetiva** | **~12,3%** | **~20,2%** |

**Diferença: ~R$ 785/mês a favor do Anexo III.**

### R$ 15.000/mês (R$ 180k/ano)

No limite da 1ª faixa do Anexo III. Pró-labore precisa ≥ R$ 4.200/mês para garantir Fator R ≥ 28%.

| Item | Com Fator R (Anexo III) | Sem Fator R (Anexo V) |
|------|--------------------------|------------------------|
| Pró-labore | R$ 4.500 | R$ 2.000 |
| DAS | R$ 900 (6,00%) | R$ 2.325 (15,50%) |
| INSS sócio | R$ 495 | R$ 220 |
| IRPF | R$ 0 (isento até R$ 5k) | R$ 0 |
| Contador | R$ 350 | R$ 350 |
| **Total custos** | **R$ 1.745** | **R$ 2.895** |
| **Carga efetiva** | **~11,6%** | **~19,3%** |

**Diferença: ~R$ 1.150/mês a favor do Anexo III.**

### R$ 20.000/mês (R$ 240k/ano)

2ª faixa. Pró-labore precisa ≥ R$ 5.600/mês para Fator R ≥ 28%.

| Item | Com Fator R (Anexo III) | Sem Fator R (Anexo V) |
|------|--------------------------|------------------------|
| Pró-labore | R$ 6.000 | R$ 2.500 |
| DAS | R$ 1.460 (7,30%) | R$ 3.225 (16,13%) |
| INSS sócio | R$ 660 | R$ 275 |
| IRPF | R$ 0–80 (faixa de redução) | R$ 0 |
| Contador | R$ 400 | R$ 400 |
| **Total custos** | **~R$ 2.560** | **~R$ 3.900** |
| **Carga efetiva** | **~12,8%** | **~19,5%** |

**Diferença: ~R$ 1.340/mês a favor do Anexo III.**

> [!tip] O ponto ótimo
> Para devs PJ solo em 2026, a faixa de **R$ 10k–25k/mês** é onde o Fator R rende mais. Acima de R$ 30k/mês, a vantagem começa a estreitar porque o IRPF do pró-labore "come" parte do ganho — momento de avaliar **lucro presumido** com contador especializado.

## O que mudou em 2026

### IRPF — nova isenção até R$ 5.000

Em vigor desde 1º de janeiro de 2026:

- **Isenção total** para rendimento mensal até R$ 5.000 (anual: R$ 60.000)
- **Redução gradual** entre R$ 5.000,01 e R$ 7.350/mês (R$ 60k a R$ 88,2k/ano)
- **Desconto simplificado mensal** de R$ 607,20 (substitui deduções legais)
- Acima de R$ 7.350/mês: tabela progressiva normal

**Impacto no Fator R**: a estratégia tradicional era manter pró-labore baixo para evitar IRPF — agora o teto da "zona livre" subiu, permitindo pró-labore até R$ 5k sem custo de IRPF. Isso facilita capturar o Anexo III com mais folga.

### Reforma tributária — preparando o terreno para 2027

A LC 214/2025 implementou o IBS/CBS, mas em 2026 o Simples Nacional **mantém as alíquotas atuais** — o IBS e a CBS aparecem na DAS apenas de forma **informativa**. O impacto financeiro só começa em 2027.

A decisão estratégica vem em **setembro/2026**: a empresa do Simples deve optar entre:

| Regime | Como funciona | Quando faz sentido |
|--------|---------------|---------------------|
| **Simples tradicional** | DAS unificado, sem crédito de IBS/CBS para o cliente | Cliente é PF ou outra empresa do Simples — crédito não importa |
| **Simples híbrido** | IBS/CBS apurados fora do DAS, com débito-crédito | Clientes B2B do regime regular — eles tomam crédito integral |

Para devs que atendem **PJs do regime regular** ou exportam serviços (créditos não se aplicam diretamente), essa escolha pode ser decisiva para manter competitividade.

> [!warning] Tecnologia não está nas listas reduzidas
> A alíquota geral de IBS+CBS prevista é **~26,50%** sem reduções para serviços de TI. Para empresas do regime regular (não-Simples), isso significa peso muito maior — mais um motivo para o Simples seguir atrativo para dev PJ por mais tempo.

## CNAE importa

Nem todo CNAE de TI sofre Fator R do mesmo jeito:

| Atividade | CNAE típico | Comportamento |
|-----------|-------------|---------------|
| Desenvolvimento de software sob encomenda | 6201-5/01 | Sujeito a Fator R |
| Programação de software | 6201-5/02 | Sujeito a Fator R |
| Consultoria em TI | 6204-0/00 | Sujeito a Fator R |
| Suporte técnico | 6209-1/00 | Sujeito a Fator R |
| Licenciamento de software customizável | 6202-3/00 | Sujeito a Fator R |
| Licenciamento de software não-customizável | 6203-1/00 | Anexo III direto (sem Fator R) |

Vale a checagem caso a caso com contador, porque CNAE errado pode jogar a empresa para fora do Simples ou trancar no anexo errado.

## Para quem trabalha para o exterior

Cenário comum em dev PJ:

- Empresa brasileira (ME)
- Cliente no exterior, recebimento em USD/EUR
- Exportação de serviços

**Benefícios mantidos em 2026:**
- Imunidade de ISS sobre exportação (vários municípios)
- Sem retenções típicas de PJ nacional
- Receita de exportação **conta normalmente** para o cálculo do Fator R e da RBT12

A mecânica do Fator R não muda — o que muda é que a carga efetiva tende a ser ainda menor por conta da imunidade do ISS dentro do DAS.

## Armadilhas

- **Pró-labore muito baixo "para economizar IRPF".** Era estratégia comum até 2025; com a isenção até R$ 5k em 2026, perdeu muito sentido. Pró-labore baixo demais pode jogar a empresa no Anexo V e custar mais do que o IRPF "economizado".

- **Pular meses de pró-labore.** Cada mês sem retirada reduz a folha acumulada. Em janelas curtas isso pode derrubar o Fator R abaixo de 28% e mover o mês seguinte para o Anexo V.

- **Confundir Fator R com Anexo IV.** Algumas atividades (advocacia, engenharia) tributam direto pelo Anexo IV ou V, sem possibilidade de Fator R. Confirme o enquadramento do CNAE antes de planejar.

- **Esquecer da decisão de setembro/2026.** A janela para optar por Simples tradicional vs híbrido para 2027 é curta e exige análise do perfil de clientes (PF, Simples, regime regular) — adiar pode comprometer a competitividade B2B.

- **Tratar contador como commodity.** Em TI, escolha errada de CNAE, anexo, pró-labore ou regime tributário custa milhares por ano. Contador especializado em TI tipicamente paga o próprio custo várias vezes só por ajustar a estratégia.

- **MEI como atalho.** MEI não usa Fator R, mas o limite (R$ 81k/ano) e a vedação para várias atividades de TI tornam-no inviável para dev profissional na maioria dos casos.

## Veja também

- [[03-Dominios/Empreendedorismo/Indie Hacker 101/index|Indie Hacker 101]] — trilha sobre SaaS bootstrapped (contexto onde a estrutura PJ aparece)
- [[03-Dominios/Empreendedorismo/Indie Hacker 101/12 - Unit economics — CAC, LTV, MRR, churn|Unit economics]] — métricas que conversam com a carga tributária real
- [[03-Dominios/Empreendedorismo/Indie Hacker 101/11 - Pricing para SaaS bootstrapped|Pricing para SaaS bootstrapped]] — preço precisa cobrir tributo + custo total

## Referências

- **Receita Federal** — [Nova tabela do IRPF com isenção até R$ 5 mil (jan/2026)](https://www.gov.br/fazenda/pt-br/assuntos/noticias/2026/janeiro/receita-divulga-nova-tabela-do-irpf-com-as-mudancas-apos-isencao-para-quem-ganha-ate-r-5-mil)
- **Ministério da Fazenda / Secom** — [Tabela IR 2026 e regra de isenção](https://www.gov.br/secom/pt-br/acompanhe-a-secom/noticias/2026/01/nova-tabela-do-ir-veja-faixas-e-aliquotas-e-saiba-mais-sobre-medida-que-isenta-o-pagamento-para-quem-ganha-ate-r-5-mil)
- **Senado Federal** — [Implementação da reforma tributária em 2026](https://www12.senado.leg.br/noticias/materias/2026/01/02/ano-de-2026-marca-implementacao-da-reforma-tributaria)
- **Contabilizei** — [Anexo III Simples Nacional — tabela 2026](https://www.contabilizei.com.br/contabilidade-online/anexo-3-simples-nacional/) | [Anexo V Simples Nacional — tabela 2026](https://www.contabilizei.com.br/contabilidade-online/anexo-5-simples-nacional/) | [Simples Nacional na Reforma Tributária](https://www.contabilizei.com.br/contabilidade-online/reforma-tributaria-simples-nacional/)
- **Contabilidade.com** — [Fator R no Simples Nacional 2026](https://contabilidade.com/blog/fator-r-no-simples-nacional-2026-como-calcular-e-pagar-menos/) | [Anexo V 2026 — guia completo](https://contabilidade.com/blog/anexo-5-do-simples-nacional-2026-tabela-completa-de-atividades-aliquotas-e-impostos/)
- **Agilize** — [Tabela atualizada dos anexos do Simples 2026](https://artigos.agilize.com.br/tabela-anexos-simples-nacional-2026/) | [Reforma tributária e Simples Nacional](https://artigos.agilize.com.br/reforma-tributaria-simples-nacional-2026/)
- **e-Auditoria** — [Anexo III ou V: Fator R decide imposto](https://www.e-auditoria.com.br/blog/anexo-iii-ou-anexo-v-simples-nacional/)

> [!note] Origem desta nota
> Ponto de partida: conversa do usuário com o ChatGPT em 2026-05-06 sobre Fator R para devs PJ ME. Os cenários numéricos foram **recalculados** a partir da fórmula oficial do Simples Nacional (RBT12 × alíquota − dedução) ÷ RBT12 e cruzados com as tabelas vigentes em 2026 — alguns valores divergem daqueles da conversa original por conta de imprecisões nas alíquotas efetivas que o ChatGPT usou.
