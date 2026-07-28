---
title: "Cenário legal e normativo"
created: 2026-07-27
updated: 2026-07-27
type: concept
status: seedling
fase: Magus
tags:
  - acessibilidade
  - a11y
  - legal
  - conformidade
publish: true
---

# Cenário legal e normativo

> [!abstract] TL;DR
> Acessibilidade não é só boa prática — em jurisdições-chave, é **lei com consequência financeira**. O padrão técnico (WCAG) é o mesmo do mundo todo; o que muda é a **lei** que o torna obrigatório e para quem. Nos EUA: a **ADA** (via litígio, sobretudo para empresas privadas) e a nova regra do **ADA Título II** para governos (WCAG 2.1 AA, com prazos em 2027–2028); a **Seção 508** para o governo federal. Na Europa: a norma técnica **EN 301 549** e, sobretudo, o **European Accessibility Act (EAA)**, cujo prazo para novos produtos/serviços passou em **28/06/2025** e que atinge o setor privado (e-commerce, bancos, e-books) com multas que chegam a €100 mil ou 4% do faturamento. A régua operativa quase sempre é **WCAG 2.1 AA** (as leis demoram a incorporar a 2.2).

> [!info] Isto é orientação técnica, não aconselhamento jurídico
> Esta nota mapeia o cenário para você **conversar com o jurídico e priorizar tecnicamente** — não substitui advogado. Leis de acessibilidade variam por país, estado e setor, mudam com frequência, e têm exceções (porte da empresa, tipo de serviço). Para decisões de conformidade reais, consulte a assessoria legal da organização.

As notas anteriores deram o *como* e o *por que ético/de produto*. Esta dá o **por que jurídico** — o que transforma acessibilidade de "deveríamos" em "somos obrigados, sob pena de multa e processo". Para uma pessoa sênior, conhecer esse mapa é o que permite dar peso de negócio ao trabalho técnico numa reunião com produto ou jurídico.

## A distinção que organiza tudo: padrão vs. lei

O ponto que desembaraça o assunto inteiro (já antecipado na nota 04): **WCAG é o padrão técnico; a lei é o que obriga a segui-lo.** WCAG, sozinho, não tem força legal — é uma recomendação do W3C. O que dá dente a ela são as **legislações nacionais** que a *referenciam* como a definição de "acessível". A lei diz "seja acessível"; ela aponta para WCAG (geralmente **2.1 AA**) para dizer o que isso significa; e estabelece *quem* precisa cumprir, *até quando* e *qual a punição*.

Por isso o padrão é global e a obrigação é local: o mesmo WCAG 2.1 AA é referenciado pela lei americana, europeia e de dezenas de países — mas *quem é obrigado* e *o que acontece se não cumprir* depende da jurisdição.

## Estados Unidos: três regimes

- **ADA (Americans with Disabilities Act, 1990).** A lei antidiscriminação central. Ela **não menciona a web** no texto (é de 1990), mas os tribunais americanos passaram a interpretar sites e apps como "lugares de acomodação pública" sob o **Título III** (empresas privadas). O resultado é um cenário movido a **litígio**: milhares de ações por ano contra empresas com sites inacessíveis, tipicamente cobrando conformidade com WCAG como remédio. Não há um "padrão oficial" na ADA para a web — o que há é jurisprudência que converge em WCAG 2.1 AA.
- **ADA Título II (governos estaduais e locais).** Aqui a ambiguidade acabou: em **abril de 2024**, o Departamento de Justiça (DOJ) publicou uma **regra final** exigindo explicitamente **WCAG 2.1 AA** de sites e apps de governos estaduais e municipais. Os prazos foram **estendidos em um ano** por uma regra interina — entidades grandes (população ≥ 50 mil) passam a ter até **26 de abril de 2027**, e as menores até **26 de abril de 2028**.
- **Seção 508 (Rehabilitation Act).** Exige acessibilidade de tecnologia da informação de **agências federais** dos EUA e de quem fornece a elas. A versão "refresh" (2017) alinhou o 508 ao WCAG (nível AA). Se você vende software para o governo federal americano, o 508 é o portão.

## Europa: a EN 301 549 e o European Accessibility Act

- **EN 301 549.** É a **norma técnica** europeia de acessibilidade de TIC — o equivalente europeu que **incorpora o WCAG** (na versão harmonizada vigente, **2.1 AA**) e o estende para além da web (hardware, documentos, software). Quando uma lei europeia exige acessibilidade, ela costuma apontar para a EN 301 549, que por sua vez aponta para WCAG.
- **Web Accessibility Directive (2016).** Obrigou **sites e apps do setor público** dos países-membros a cumprir a EN 301 549. Foi o primeiro grande passo, restrito ao setor público.
- **European Accessibility Act (EAA).** O divisor de águas, porque **alcança o setor privado**. O prazo central — para **novos produtos e serviços** colocados no mercado da UE — passou em **28 de junho de 2025**. Seu escopo é largo: e-commerce, serviços bancários e de pagamento, e-books, mídia audiovisual, bilhética de transporte, computadores, smartphones, caixas eletrônicos e terminais de autoatendimento. Serviços já existentes têm transição até **28/06/2030**; contratos firmados antes de 28/06/2025 e serviços de emergência, até **28/06/2027**. As **multas** variam por país-membro, podendo chegar a patamares como **€100 mil ou 4% do faturamento anual** — o suficiente para tirar acessibilidade da pauta "quando sobrar tempo".

> [!info] Datas e versões envelhecem — reconfira antes de agir (estado em julho de 2026)
> Este é o capítulo mais perecível do domínio. Em julho de 2026: o prazo de **28/06/2025** da EAA já passou (fase de fiscalização); os prazos do **ADA Título II** foram **adiados em um ano** (2027 para grandes entidades, 2028 para menores) por regra interina do DOJ — confira se não houve nova mudança. E um detalhe técnico que surpreende: apesar de a **WCAG 2.2** existir desde 2023 (nota 04), a maioria das leis ainda referencia a **2.1 AA**, porque as normas harmonizadas demoram a incorporar novas versões. Construa para **2.2** (é superconjunto da 2.1), mas saiba que o *texto legal* que citam provavelmente diz "2.1". Se você lê isto depois de 2026, trate cada data acima como suspeita e reconfira na fonte.

## O Brasil e o panorama global

O leitor brasileiro tem seu próprio arcabouço, e o padrão global reaparece adaptado:

- **LBI — Lei Brasileira de Inclusão (Lei 13.146/2015)** torna a acessibilidade digital obrigatória, com destaque para sites de empresas e do poder público.
- **e-MAG** (Modelo de Acessibilidade em Governo Eletrônico) é o padrão para sites do governo federal brasileiro — inspirado no WCAG, adaptado ao contexto nacional.
- Dezenas de outros países (Canadá com a ACA, Reino Unido com o Equality Act, Austrália, etc.) têm leis próprias — quase todas **convergindo no WCAG AA** como régua técnica. É por isso que dominar WCAG (SG1) é o investimento que atravessa toda jurisdição: a lei muda de país para país; o padrão que ela referencia, quase não.

## O argumento de negócio, agora com dente

Volte ao caso de negócio da nota 01. Lá, "risco legal" era uma das três frentes. Agora ele tem números: um processo sob a ADA, uma multa de EAA na casa dos seis dígitos, um prazo de conformidade governamental vencendo. Numa conversa sênior, isto muda o enquadramento — acessibilidade deixa de competir com features por "ser o certo a fazer" e passa a ser **gestão de risco** com cifras. E o argumento decisivo: remediar sob litígio, com prazo judicial e sob os holofotes, custa **muito** mais do que construir certo desde o começo (o shift-left da nota 17). A lei é, no fim, o incentivo externo que alinha o bolso da empresa ao que o usuário sempre precisou.

**Cenário legal em uma frase:** WCAG é o padrão técnico global; leis como a ADA (EUA) e a EAA (Europa, prazo desde jun/2025, atingindo o setor privado com multas pesadas) é que o tornam obrigatório — a régua costuma ser 2.1 AA, e as datas mudam, então reconfira sempre.

## O que vem a seguir

Se a lei exige conformidade, a organização precisa saber **declará-la** — para clientes, para licitações, para o próprio jurídico. Existe um documento padrão para isso, e saber lê-lo e produzi-lo é a contraparte formal de tudo o que você auditou no SG3.

- [[03-Dominios/Tecnologia/Acessibilidade/Sustentar e Conformidade/19 - VPAT, ACR e comunicar conformidade|19 — VPAT, ACR e comunicar conformidade]] — o documento que declara conformidade.
- [[03-Dominios/Tecnologia/Acessibilidade/Fundamentos e Modelo Mental/04 - WCAG 2.2 pelo ofício|04 — WCAG 2.2 pelo ofício]] — a régua técnica que todas essas leis referenciam.
- [[03-Dominios/Tecnologia/Acessibilidade/Sustentar e Conformidade/20 - A11y em entrevista|20 — A11y em entrevista]] — como usar esse repertório numa conversa sênior.

## Fontes

- **U.S. Department of Justice** — [*Fact Sheet: New Rule on the Accessibility of Web Content and Mobile Apps (ADA Title II)*](https://www.ada.gov/resources/2024-03-08-web-rule/) — a regra de 2024 e o padrão WCAG 2.1 AA para governos.
- **European Commission** — [*European Accessibility Act*](https://ec.europa.eu/social/main.jsp?catId=1202) — escopo, prazos e obrigações da EAA.
- **ETSI** — [*EN 301 549*](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/) — a norma técnica europeia que incorpora o WCAG.
- **U.S. Access Board** — [*Section 508 Standards*](https://www.access-board.gov/ict/) — os requisitos para tecnologia do governo federal americano.
- **Governo Federal do Brasil** — [*e-MAG — Modelo de Acessibilidade em Governo Eletrônico*](https://emag.governoeletronico.gov.br/) — o padrão brasileiro de acessibilidade digital.
