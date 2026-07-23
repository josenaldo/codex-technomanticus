---
title: "Roadmap — Rede na nuvem (VPC)"
created: 2026-07-23
updated: 2026-07-23
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Rede na nuvem (VPC) (galho 7)

Roadmap-folha do galho `Cloud/07 - Rede na nuvem (VPC)`. Bloco 2 (Os primitivos) — o galho mais denso da trilha. Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 6 |
| ⬜ pendente | 0 |
| ✅ feita | 6 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |
| M1 (mídia) | pendente — enriquecimento futuro |

---

## Notas

#### 01 - A VPC e o endereçamento
- **Estado:** ✅ feita · fase: Iniciado · 299 linhas
- **Escopo:** VPC como rede isolada, notação CIDR com exemplos trabalhados, RFC 1918, VPC default vs custom, escopo regional, DO VPC (não atravessa datacenters).

#### 02 - Subnets e roteamento
- **Estado:** ✅ feita · fase: Adepto · 396 linhas
- **Escopo:** subnet presa a 1 AZ, pública vs privada (é rota pra IGW, não flag), route tables, local route, longest-prefix match, 5 IPs reservados; DO VPC é rede plana (sem subnet/route table editável).

#### 03 - Gateways - internet e NAT
- **Estado:** ✅ feita · fase: Adepto · 404 linhas
- **Escopo:** internet gateway, NAT gateway (saída sem entrada), armadilha de custo do NAT com números, VPC endpoints como alternativa, NAT instance + source/dest check; DO NAT Gateway GA nov/2025.

#### 04 - Security groups e NACLs
- **Estado:** ✅ feita · fase: Adepto · 402 linhas
- **Escopo:** SG stateful/allow-only nível instância vs NACL stateless/allow+deny nível subnet, ephemeral ports, referência SG→SG, ordem de avaliação NACL→SG, DO Cloud Firewalls (sem NACL de subnet).

#### 05 - Conectividade privada
- **Estado:** ✅ feita · fase: Adepto · 397 linhas
- **Escopo:** VPC peering (não-transitivo, CIDR não-sobreposto), gateway vs interface endpoint (PrivateLink), transit gateway, VPN/Direct Connect de passagem; DO peering GA + Partner Network Connect (Megaport), sem endpoints.

#### 06 - Desenhando uma rede segura de ponta a ponta
- **Estado:** ✅ feita · fase: Magus · 431 linhas · **FECHA o galho**
- **Escopo:** arquitetura three-tier em VPC multi-AZ (web/app/db), cadeia de security groups, defesa em profundidade, caminho do atacante barrado por camada, síntese das 6 notas → ponte para o Galho 8 (Armazenamento). Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Escrito em 2 ondas de 3 agentes (01-03, depois 04-06); orquestrador commitou serialmente (`0f1d9b5`, `be0e82a`). 0 wikilinks quebrados no gate.
- Galho mais denso da trilha ("o mais temido"): fronteira com System Design (arquitetura segura) e Segurança; a distinção SG vs NACL e a armadilha de custo do NAT são os pontos que mais aparecem em entrevista.
- Nota 03 reaberta 1x p/ atingir piso Adepto SEM padding (332→404): montagem ponta a ponta, VPC endpoints, custo do NAT trabalhado, NAT instance.
- Honestidade de paridade DO reforçada: VPC plana sem subnet/route table, Cloud Firewall (sem NACL), peering GA mas sem cross-account, NAT Gateway recém-GA. Correção factual pega em runtime: DO tem Partner Network Connect (Megaport), não "sem equivalente".
- Capstone (06) fechou 431 — dentro da banda de capstone Magus (430-500).
