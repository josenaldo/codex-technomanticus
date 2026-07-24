---
title: "Cloud — Certificação AWS Solutions Architect Associate"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - aws
  - certificacao
aliases:
  - "Certificação AWS Solutions Architect Associate"
  - "Galho 24 - Certificação SAA-C03"
---

# Certificação AWS Solutions Architect Associate

> [!abstract] TL;DR
> Galho 24 da trilha Cloud, e o último galho do **Bloco 5 (Provedores e maestria)**. O AWS Solutions Architect Associate (SAA-C03) é a certificação que transforma a trilha Cloud em credencial reconhecida — e, mais do que o papel, o blueprint do exame é um ótimo checklist do que um arquiteto AWS precisa saber. O galho abre com **o exame em si** (formato, custo, passing score, valor real), mapeia **os quatro domínios do blueprint** (Secure, Resilient, High-Performing, Cost-Optimized) e seus pesos, faz o **mapa reverso** de cada galho da trilha ao domínio que ele já preparou, expõe os **serviços que o exame ama e as pegadinhas** recorrentes, monta uma **estratégia de prova**, e fecha com um **capstone**: um plano de estudo concreto de semanas que usa a trilha como base e fecha as lacunas do exame. 6 notas, 3 fases.

## Sobre este galho

O SAA-C03 não é conhecimento novo — é o mesmo conhecimento que a trilha Cloud já construiu, mas organizado por um blueprint oficial e cobrado sob pressão de tempo e distratoras desenhadas pra confundir. Este galho não reensina os serviços; ele traduz a trilha para a linguagem do exame, mostra onde a trilha já cobre o blueprint e onde não cobre, e ensina a mecânica de fazer a prova em si — porque saber a matéria e passar no exame são habilidades relacionadas, mas não idênticas.

O fio condutor vai do exame à estratégia. Primeiro o *quê e o porquê* — o que é o SAA-C03, formato, custo, passing score, validade, e por que vale (ou não) a pena. Depois o *blueprint* em duas notas: os quatro domínios oficiais com seus pesos, e o mapa reverso — cada galho da trilha Cloud contra cada domínio do exame, expondo lacunas com honestidade. Depois o *conteúdo que mais pesa na prova* — os serviços superrepresentados e os padrões de pegadinha (Multi-AZ vs Read Replica, Security Group vs NACL, "gerenciado" vence "você operando") que separam quem estudou de quem decorou. Depois a *tática de sentar na cadeira* — gestão de tempo, eliminação de distratoras, flag-and-review, o manejo psicológico da prova. E fecha com o *capstone*: um plano de estudo de semanas, ancorado na trilha, que fecha as lacunas do mapa reverso.

**Audiência primária:** quem terminou (ou está terminando) a trilha Cloud e quer transformar esse conhecimento em uma certificação reconhecida pelo mercado, sem refazer do zero um curso de exame. **Audiência secundária:** quem já estuda para o SAA-C03 por outra fonte e quer um mapa honesto de onde a trilha já cobre o blueprint e onde precisa reforçar.

> [!info] Fronteira
> O **conteúdo técnico de cada serviço** (EC2, RDS, S3, VPC, IAM, Lambda, etc.) vive nos galhos correspondentes da trilha Cloud, especialmente [[03-Dominios/Tecnologia/Cloud/21 - AWS a fundo/index|AWS a fundo]] (galho 21) e [[03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework/index|Well-Architected Framework]] (galho 3), cujos pilares mapeiam quase 1:1 aos quatro domínios do exame. Este galho não reexplica esse conteúdo — ele mapeia, prioriza e ensina a fazer a prova sobre ele.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/24 - Certificação AWS Solutions Architect Associate/01 - O exame e seu valor|01 — O exame e seu valor — o que é o SAA-C03 e por que fazer]] — formato do exame (65 questões, 130 min, passing score, custo, validade de 3 anos), o equivalente nas outras nuvens, onde o SAA se encaixa na escada de certificações AWS, e o valor real da certificação pra carreira — a economia da sinalização.

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/24 - Certificação AWS Solutions Architect Associate/02 - Os quatro domínios do blueprint|02 — Os quatro domínios do blueprint — o que o exame cobra e com que peso]] — os 4 domínios oficiais do SAA-C03 (Design Secure ~30%, Resilient ~26%, High-Performing ~24%, Cost-Optimized ~20%) e sua sobreposição quase perfeita com os pilares do Well-Architected.
3. [[03-Dominios/Tecnologia/Cloud/24 - Certificação AWS Solutions Architect Associate/03 - Mapa da trilha ao blueprint|03 — Mapa da trilha ao blueprint — o que você já sabe]] — mapa reverso galho → domínio → cobertura: onde a trilha Cloud já preparou cada domínio do exame, as lacunas em detalhe, e como usar o mapa pra montar a revisão sem reestudar o que já foi coberto.
4. [[03-Dominios/Tecnologia/Cloud/24 - Certificação AWS Solutions Architect Associate/04 - Serviços que o exame ama e as pegadinhas|04 — Serviços que o exame ama — e as pegadinhas recorrentes]] — o dicionário secreto da prova: os serviços superrepresentados, o vocabulário de frequência de acesso, e os padrões de pegadinha recorrentes (Multi-AZ vs Read Replica, SG vs NACL, ALB vs NLB vs GWLB, EBS vs EFS vs S3) que separam a resposta certa das distratoras.
5. [[03-Dominios/Tecnologia/Cloud/24 - Certificação AWS Solutions Architect Associate/05 - Estratégia de prova|05 — Estratégia de prova — como sentar e passar]] — o relógio como adversário previsível, a técnica das duas descartáveis e as duas na dúvida, onde o requisito-chave se esconde no enunciado, simulados como termômetro (não decoreba), e o manejo psicológico do pânico na hora da prova.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/24 - Certificação AWS Solutions Architect Associate/06 - Capstone — plano de estudo para o SAA-C03|06 — Capstone — um plano de estudo para o SAA-C03]] — síntese do galho: um cronograma de 4 a 6 semanas ancorado na trilha, semana a semana por domínio, simulados e revisão de erros, critério objetivo de "estou pronto", e o fechamento do galho 24 (e do que vem depois, no domínio inteiro). Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — o exame, o blueprint, o mapa reverso, as pegadinhas, a estratégia, e o plano de estudo no fim.

### Já terminei a trilha, só quero o plano de prova

03 (o mapa que mostra o que já sei e onde estão as lacunas) → 04 (as pegadinhas que a trilha por si só não ensina) → 06 (o cronograma que fecha o resto).

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Cloud/24 - Certificação AWS Solutions Architect Associate" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework/index|Well-Architected Framework]] — Galho 3, os pilares que os quatro domínios do exame quase replicam
- [[03-Dominios/Tecnologia/Cloud/21 - AWS a fundo/index|AWS a fundo]] — Galho 21, o conteúdo técnico que este galho organiza para o exame
