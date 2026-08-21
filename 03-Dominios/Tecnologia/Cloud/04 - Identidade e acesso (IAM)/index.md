---
title: "Cloud — Identidade e acesso (IAM)"
created: 2026-07-20
updated: 2026-07-23
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
aliases:
  - "Identidade e acesso (IAM)"
  - "Galho 4 - Identidade e acesso (IAM)"
---

# Identidade e acesso (IAM)

> [!abstract] TL;DR
> Galho 4 da trilha Cloud, Bloco 1: identidade como perímetro — o primeiro serviço concreto da trilha. Por que autenticação e autorização substituem o firewall na nuvem, usuários e o problema da credencial de longa duração, como uma política é avaliada, roles e credenciais temporárias, least privilege na prática, e identidade entre contas e federação (humana e de CI/CD). 6 notas, 3 fases.

## Sobre este galho

Os Galhos 1-3 deram modelo mental, mecânica e bússola; este galho entrega o primeiro serviço de nuvem estudado a fundo, porque a maioria dos incidentes graves de nuvem nasce de uma permissão mal concedida, não de uma invasão sofisticada. O fio condutor: no datacenter o perímetro era físico e depois virou rede; na nuvem não existe "dentro" — toda ação é uma chamada de API que passa por autenticação e autorização. O galho percorre esse perímetro de identidade do básico (usuário, grupo, chave de acesso estática e por que ela é perigosa) ao avançado (papéis com credencial que expira sozinha, como uma política é de fato avaliada — default nega, negação explícita é definitiva —, o ciclo prático de apertar permissão com dados em vez de adivinhar, e as três variações de "provar quem você é para um limite de confiança que não é o seu": entre contas, para gente via federação corporativa, e para pipelines de CI/CD via identidade de carga de trabalho).

**Audiência primária:** quem já tem a mecânica de conta/geografia do Galho 2 e a lente de segurança do pilar Segurança (Galho 3) e agora precisa operar identidade de verdade. **Audiência secundária:** quem já usa IAM no dia a dia mas nunca formalizou por que `AccessDenied` aparece mesmo com "acesso total" concedido, ou por que uma chave de acesso estática é sempre o ponto fraco.

Este galho é a aplicação concreta, na nuvem, dos conceitos gerais do domínio [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]]. Os primitivos de compute/rede/storage que essa identidade vai proteger começam no Bloco 2.

## Iniciado

1. [[01 - Por que identidade é o primeiro serviço|01 — Por que identidade é o primeiro serviço]] — sem "dentro" na nuvem: toda ação passa por autenticação e autorização.
2. [[02 - Usuários, grupos e o problema da credencial de longa duração|02 — Usuários, grupos e o problema da credencial de longa duração]] — a chave de acesso estática e por que ela é o ponto fraco, não o usuário.

## Adepto

3. [[03 - Políticas — como uma permissão é avaliada|03 — Políticas: como uma permissão é avaliada]] — default nega, política de identidade + de recurso se somam, negação explícita é definitiva.
4. [[04 - Roles e credenciais temporárias|04 — Roles e credenciais temporárias]] — credencial que nasce com prazo de validade via trust policy e STS.

## Magus

5. [[05 - Least privilege na prática|05 — Least privilege na prática]] — apertar permissão com dados de uso real, não adivinhar de primeira.
6. [[06 - Identidade entre contas e federação|06 — Identidade entre contas e federação]] — assumir papel entre contas, SSO corporativo, identidade de carga de trabalho para CI/CD. Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear recomendado — cada nota resolve o problema estrutural que a anterior deixou em aberto.

### Já configuro IAM, quero fechar as lacunas de fato

02 (a credencial estática é a raiz de quase todo vazamento) → 03 (avaliação de política é o que ninguém formaliza) → 06 (federação e identidade de CI/CD fecham o arco da credencial que nunca deveria ter existido).

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/01 - O que é a nuvem, de verdade/index|O que é a nuvem, de verdade]] — Galho 1
- [[03-Dominios/Tecnologia/Cloud/02 - Anatomia de um provedor/index|Anatomia de um provedor]] — Galho 2
- [[03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework/index|Well-Architected Framework]] — Galho 3
- [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]] — domínio geral, do qual este galho é a aplicação na nuvem
