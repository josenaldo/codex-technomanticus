---
title: "Cloud — O que é a nuvem, de verdade"
created: 2026-07-20
updated: 2026-07-23
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
aliases:
  - "O que é a nuvem, de verdade"
  - "Galho 1 - O que é a nuvem, de verdade"
---

# O que é a nuvem, de verdade

> [!abstract] TL;DR
> Galho 1 da trilha Cloud, Bloco 1 (Modelo mental e fundamentos): funda o modelo mental do domínio inteiro. Nuvem como infraestrutura virada API, capex vs opex, o espectro IaaS→SaaS, público/privado/híbrido/multi-cloud, o panorama dos provedores, e a virada mental de pensar em serviços em vez de servidores. 6 notas, 3 fases.

## Sobre este galho

Este é o alicerce de toda a trilha Cloud — sem ele, os outros 23 galhos ficam sem chão. Ele não ensina nenhum serviço específico ainda; ensina o vocabulário e o modelo mental que tornam qualquer serviço de nuvem legível: o que muda de verdade quando infraestrutura vira chamada de API, por que "opex em vez de capex" é o motor real da velocidade que a nuvem entrega, os cinco formatos de "quanto da pilha você opera" (IaaS/PaaS/CaaS/FaaS/SaaS), onde essa infraestrutura pode fisicamente estar, quem são os provedores e por que cada um tem uma filosofia de produto diferente, e — fechando o galho — a virada de mentalidade que separa quem "usa a nuvem como datacenter alugado" de quem projeta pensando em serviços gerenciados, falha como condição de operação e custo/segurança desde a primeira linha.

**Audiência primária:** quem conhece infraestrutura tradicional (servidor próprio, datacenter, VPS) e quer o modelo mental certo antes de tocar em qualquer console. **Audiência secundária:** quem já usa nuvem no dia a dia mas nunca formalizou o vocabulário — cada nota aplica a lente dupla AWS↔DigitalOcean que atravessa a trilha inteira.

A mecânica concreta de como um provedor é montado por dentro (conta, regions, plano de controle/dados) é o [[03-Dominios/Tecnologia/Cloud/02 - Anatomia de um provedor/index|Galho 2]]; a bússola de critério arquitetural é o [[03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework/index|Galho 3]] — este galho fica só no modelo mental de partida.

## Iniciado

1. [[01 - O que é computação em nuvem|01 — O que é computação em nuvem]] — as cinco características do NIST (SP 800-145), self-service, elasticidade, medição por uso.
2. [[02 - Capex, opex e a economia da elasticidade|02 — Capex, opex e a economia da elasticidade]] — por que "quem aprova" muda mais que "quanto custa a hora de máquina".
3. [[03 - Modelos de serviço — IaaS, PaaS, CaaS, FaaS e SaaS|03 — Modelos de serviço (IaaS, PaaS, CaaS, FaaS e SaaS)]] — o espectro de controle vs conveniência.

## Adepto

4. [[04 - Modelos de implantação — público, privado, híbrido e multi-cloud|04 — Modelos de implantação (público, privado, híbrido e multi-cloud)]] — "onde roda" é um eixo independente de "quanto você gerencia".
5. [[05 - O panorama dos provedores|05 — O panorama dos provedores]] — hyperscalers, segunda camada, e a filosofia de produto por trás do catálogo de cada um.

## Magus

6. [[06 - A virada mental — pensar em serviços, não em servidores|06 — A virada mental: pensar em serviços, não em servidores]] — cattle not pets, falha como condição de operação, custo e segurança desde o desenho. Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear recomendado para quem está começando do zero em nuvem.

### Já uso nuvem, quero só formalizar o vocabulário

01 (skim) → 03 (o espectro IaaS-SaaS raramente é articulado com clareza) → 06 (a virada mental é o que costuma faltar em quem "usa a nuvem só como VPS mais cara").

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Cloud/01 - O que é a nuvem, de verdade" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/02 - Anatomia de um provedor/index|Anatomia de um provedor]] — Galho 2
- [[03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework/index|Well-Architected Framework]] — Galho 3
- [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Identidade e acesso (IAM)]] — Galho 4
