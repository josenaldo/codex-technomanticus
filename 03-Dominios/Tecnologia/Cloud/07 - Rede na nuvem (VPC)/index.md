---
title: "Cloud — Rede na nuvem (VPC)"
created: 2026-07-23
updated: 2026-07-23
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
aliases:
  - "Rede na nuvem (VPC)"
  - "Galho 7 - Rede na nuvem (VPC)"
---

# Rede na nuvem (VPC)

> [!abstract] TL;DR
> Galho 7 da trilha Cloud, Bloco 2 (Os primitivos) — "o mais importante e mais temido". A rede virtual privada onde todo o compute dos galhos 5-6 realmente vive, aberta camada por camada: a VPC e o endereçamento (CIDR, RFC 1918), subnets pública vs privada e roteamento, os gateways que deixam o tráfego entrar (IGW) e sair sem exposição (NAT), as duas camadas de firewall (security groups stateful vs NACLs stateless), a conectividade privada entre VPCs e serviços (peering, endpoints, transit gateway), e o desenho de uma rede three-tier segura de ponta a ponta. 6 notas, 3 fases, lente dupla AWS ↔ DigitalOcean.

## Sobre este galho

Os galhos 5 e 6 subiram instâncias e uma frota elástica atrás de um balanceador — mas trataram a rede em que tudo isso vive como mágica: as instâncias simplesmente se enxergavam, o LB simplesmente as alcançava. Este galho abre essa caixa-preta, e não por acaso é o mais temido da trilha: a maioria dos incidentes de "não conecta" e boa parte das brechas de segurança nascem de uma rede mal desenhada, não de um bug de aplicação.

O fio condutor constrói a rede de dentro para fora: primeiro o *espaço de endereços* (a VPC e seu CIDR), depois como *subdividi-lo e rotear* (subnets e route tables — onde mora a distinção pública/privada que quase todo mundo entende errado), depois como o tráfego *entra e sai* (internet gateway e NAT gateway, com a armadilha de custo do NAT), depois como *filtrar* quem fala com quem (security groups e NACLs, as duas camadas de firewall), depois como *conectar de forma privada* VPCs e serviços sem passar pela internet (peering, endpoints, transit gateway), e por fim o *desenho completo* de uma rede three-tier segura por design — que é onde a frota elástica do galho 6 de fato passa a morar.

**Audiência primária:** quem já sobe instâncias (galhos 5-6) mas trata a VPC como configuração que "só funciona" e precisa desenhá-la com intenção. **Audiência secundária:** quem já opera VPCs mas nunca formalizou por que uma subnet é "pública", por que o NAT gateway aparece tão caro na fatura, ou a diferença exata entre security group e NACL que toda entrevista cobra.

> [!info] Fronteira
> Os conceitos abstratos de **arquitetura segura e defesa em profundidade** vivem em [[03-Dominios/Engenharia/Arquitetura/index|System Design]]; a **disciplina de operar** a rede em produção vive em [[03-Dominios/Engenharia/Operação/index|Operação]]. Este galho mostra a encarnação concreta na nuvem (VPC da AWS, VPC da DigitalOcean) e linka de volta — não reensina teoria de redes.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)/01 - A VPC e o endereçamento|01 — A VPC e o endereçamento]] — rede virtual isolada, CIDR e RFC 1918, VPC default vs custom, escopo regional, DO VPC.

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)/02 - Subnets e roteamento|02 — Subnets e roteamento]] — subnet presa a uma AZ, pública vs privada (é rota, não flag), route tables, local route, o desenho de camadas.
3. [[03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)/03 - Gateways - internet e NAT|03 — Gateways: internet e NAT]] — internet gateway, NAT gateway (saída sem entrada), a armadilha de custo do NAT, VPC endpoints como alternativa, NAT instance.
4. [[03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)/04 - Security groups e NACLs|04 — Security groups e NACLs]] — firewall stateful (SG) vs stateless (NACL), ephemeral ports, referência SG→SG, ordem de avaliação, DO Cloud Firewalls.
5. [[03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)/05 - Conectividade privada|05 — Conectividade privada]] — VPC peering (não-transitivo), gateway vs interface endpoints (PrivateLink), transit gateway, DO peering.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)/06 - Desenhando uma rede segura de ponta a ponta|06 — Desenhando uma rede segura de ponta a ponta]] — arquitetura three-tier em VPC multi-AZ, cadeia de security groups, defesa em profundidade, o caminho do atacante barrado camada a camada. Capstone do galho e ponte para o armazenamento.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — cada nota adiciona uma camada da rede, e a nota 06 monta a VPC segura completa.

### Já uso VPC, quero fechar as lacunas de fato

02 (por que "pública" é uma rota, não uma flag) → 03 (por que o NAT gateway custa o que custa, e como evitá-lo com endpoints) → 04 (a diferença exata SG vs NACL e a pegadinha das ephemeral ports).

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/06 - Compute II — elasticidade e balanceamento/index|Compute II — elasticidade e balanceamento]] — Galho 6, a frota elástica que passa a viver dentro desta VPC
- [[03-Dominios/Tecnologia/Cloud/02 - Anatomia de um provedor/index|Anatomia de um provedor]] — Galho 2, de onde vêm as regions e AZs que a VPC atravessa
- [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Identidade e acesso (IAM)]] — Galho 4, a outra metade do perímetro: identidade filtra quem faz a chamada, a rede filtra de onde
- [[03-Dominios/Engenharia/Arquitetura/index|System Design]] — os conceitos abstratos de arquitetura segura que esta VPC encarna
