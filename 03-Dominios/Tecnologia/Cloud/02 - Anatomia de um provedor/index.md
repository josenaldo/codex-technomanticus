---
title: "Cloud — Anatomia de um provedor"
created: 2026-07-20
updated: 2026-07-23
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
aliases:
  - "Anatomia de um provedor"
  - "Galho 2 - Anatomia de um provedor"
---

# Anatomia de um provedor

> [!abstract] TL;DR
> Galho 2 da trilha Cloud, Bloco 1: como um provedor é montado por dentro — mecânica concreta, não mais só modelo mental. Conta como unidade fundamental, geografia (regions/AZs/edge), plano de controle vs plano de dados, as quatro portas de acesso (console/CLI/SDK/API), responsabilidade compartilhada, e os limites/cotas/SLA que todo contrato de provedor impõe. 6 notas, 3 fases.

## Sobre este galho

O [[03-Dominios/Tecnologia/Cloud/01 - O que é a nuvem, de verdade/index|Galho 1]] deu o modelo mental; este galho abre a caixa e mostra as peças que qualquer provedor — AWS, DigitalOcean, ou outro — compartilha por baixo dos nomes diferentes. A conta como unidade de isolamento e blast radius, a geografia que decide latência/preço/disponibilidade legal do dado, a distinção entre o sistema que orquestra (plano de controle, frágil e otimizado para consistência) e o sistema que serve tráfego (plano de dados, otimizado para ficar de pé), os quatro clientes que falam com a mesma API HTTP, a linha que separa o que o provedor garante do que você garante, e os tetos — cota, rate limit, SLA — que toda arquitetura precisa respeitar.

**Audiência primária:** quem já entende o modelo mental do Galho 1 e precisa da mecânica concreta antes de tocar em qualquer serviço específico (compute, rede, storage vêm nos galhos seguintes). **Audiência secundária:** quem já opera nuvem no dia a dia mas nunca formalizou por que o console às vezes cai e a aplicação continua no ar, ou por que um script de automação pode derrubar o plano de controle sem afetar tráfego de produção.

Os primitivos que rodam dentro dessa anatomia (compute, rede, storage) começam no Bloco 2; a bússola de critério arquitetural é o [[03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework/index|Galho 3]]; e a identidade — que atravessa toda essa anatomia como perímetro — é o [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Galho 4]].

## Iniciado

1. [[01 - A conta e a organização|01 — A conta e a organização]] — a conta como unidade de isolamento e cobrança, root user, blast radius, Organizations/Teams.
2. [[02 - Geografia da nuvem — regions, zonas e edge|02 — Geografia da nuvem (regions, zonas e edge)]] — region, availability zone e edge location como três níveis de granularidade.
4. [[04 - As quatro portas — console, CLI, SDK e API|04 — As quatro portas (console, CLI, SDK e API)]] — quatro clientes da mesma API HTTP assinada.

## Adepto

3. [[03 - Plano de controle e plano de dados|03 — Plano de controle e plano de dados]] — dois sistemas com propriedades opostas rodando lado a lado.
5. [[05 - O modelo de responsabilidade compartilhada|05 — O modelo de responsabilidade compartilhada]] — segurança "da" nuvem vs segurança "na" nuvem.

## Magus

6. [[06 - Limites, cotas e o contrato do provedor|06 — Limites, cotas e o contrato do provedor]] — cotas ajustáveis, rate limit, SLA que garante crédito e não continuidade. Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear recomendado para quem está construindo a mecânica do zero.

### Já opero nuvem, quero fechar lacunas

03 (plano de controle vs dados raramente é articulado) → 05 (responsabilidade compartilhada é o divisor entre "o provedor falhou" e "eu configurei errado") → 06 (cotas e SLA batem direto na operação real).

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/01 - O que é a nuvem, de verdade/index|O que é a nuvem, de verdade]] — Galho 1
- [[03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework/index|Well-Architected Framework]] — Galho 3
- [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Identidade e acesso (IAM)]] — Galho 4
