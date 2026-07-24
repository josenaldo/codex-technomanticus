---
title: "Cloud — DNS, CDN e borda"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - dns
  - cdn
  - borda
aliases:
  - "DNS, CDN e borda"
  - "Galho 10 - DNS, CDN e borda"
---

# DNS, CDN e borda

> [!abstract] TL;DR
> Galho 10 da trilha Cloud, e o que **fecha o Bloco 2 (Os primitivos)**. Os galhos 5-9 deram à aplicação onde computar, como escalar, onde viver isolada, onde guardar bytes e onde guardar estado. Falta a última pergunta: como um cliente do outro lado do planeta *encontra* e *alcança* tudo isso — rápido e protegido. Esse é o trabalho da **borda**. O galho sobe do nome ao request: primeiro o **DNS** (a agenda telefônica da internet, como serviço gerenciado), depois o **roteamento DNS avançado** (o DNS como o primeiro balanceador global — latência, geo, failover), depois a **CDN** (CloudFront aproximando o conteúdo do usuário e cacheando na borda), depois o **TLS na borda** (certificado gerenciado, terminação, ACM), depois **a borda como camada** de defesa (WAF, Shield, origin protection — a nota-mapa que costura DNS+CDN+TLS numa pilha só), e fecha com o **capstone do Bloco 2 inteiro**: uma arquitetura de referência ponta a ponta amarrando os seis galhos, e a ponte para o serverless. 6 notas, 3 fases, lente dupla AWS ↔ DigitalOcean.

## Sobre este galho

Os galhos 5-9 construíram os primitivos de infraestrutura como peças isoladas. Este galho responde à pergunta que faltava — *como o mundo chega até eles* — e, ao respondê-la, revela que DNS, CDN, TLS e defesa não são capítulos separados: são camadas empilhadas de um único perímetro chamado **borda**. É na borda que o nome é resolvido, que o TLS termina, que o cache responde sem acordar o origin, e que o tráfego hostil é filtrado antes de tocar a aplicação.

O fio condutor sobe do nome ao request. Primeiro o *DNS* em duas notas: a mecânica de resolução e os tipos de registro como serviço gerenciado (Route 53 ↔ DO DNS), depois o roteamento avançado que transforma o DNS no primeiro balanceador de carga global. Depois a *CDN* — CloudFront, edge locations, cache behaviors, invalidação, e a proteção do origin via OAC. Depois o *TLS na borda* — como o HTTPS é provisionado, terminado e renovado sem gestão manual de certificado, com ACM e Let's Encrypt gerenciado. Depois *a borda como camada* — a nota-síntese que junta tudo numa pilha de defesa (WAF na camada 7, Shield na camada 3/4, origin protection como princípio) e desenha o request atravessando o perímetro inteiro. E por fim o *capstone*: a arquitetura de referência do Bloco 2 completa, com o request percorrendo borda → compute → banco → cache → storage e voltando, a tabela de decisão do bloco inteiro, e a virada de mentalidade que abre o Bloco 3.

**Audiência primária:** quem sabe o que é DNS e HTTPS mas nunca provisionou uma zona, uma distribution ou um certificado gerenciado com intenção, nem sabe onde exatamente cada defesa da borda se encaixa. **Audiência secundária:** quem já usa CloudFront/Route 53 mas nunca formalizou por que TLS deve terminar na borda, por que invalidação é cara, ou por que o origin nunca fala direto com a internet.

> [!info] Fronteira
> O **conceito abstrato** de CDN, load balancing e cache distribuído vive em [[03-Dominios/Engenharia/Arquitetura/index|System Design]]; a **teoria de criptografia/TLS/PKI** e a anatomia de vulnerabilidades (SQLi, XSS) são território de Segurança; **DNS como protocolo de rede** a fundo é assunto de redes. Este galho trata a borda como a **encarnação gerenciada** desses conceitos na nuvem — Route 53, CloudFront, ACM, WAF, Shield — e a mecânica concreta de operá-los. Onde a teoria é dona, o galho linka em vez de reexplicar.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/10 - DNS, CDN e borda/01 - DNS na nuvem|01 — DNS na nuvem]] — a agenda telefônica da internet como serviço gerenciado: resolução recursiva vs autoritativa, zonas hospedadas, tipos de registro (A/AAAA/CNAME/ALIAS/MX/TXT/NS), a diferença crítica CNAME vs ALIAS no apex, TTL e propagação; Route 53 ↔ DO DNS.

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/10 - DNS, CDN e borda/02 - Roteamento DNS avançado|02 — Roteamento DNS avançado]] — o DNS como o primeiro balanceador de carga global: as políticas do Route 53 (simple, weighted, latency, geolocation, geoproximity, failover, multivalue, IP-based), health checks, o papel do TTL na velocidade do failover, DR ativo-passivo; a simplicidade deliberada do DO DNS (só round-robin).
3. [[03-Dominios/Tecnologia/Cloud/10 - DNS, CDN e borda/03 - CDN e cache de borda|03 — CDN e cache de borda]] — a CDN como encarnação gerenciada do cache distribuído: CloudFront, edge locations, cache behaviors por path, TTL (min/max/default), cache keys, invalidação (cara e lenta) vs versionamento, origin protection via OAC; CDN embutida no DO Spaces.
4. [[03-Dominios/Tecnologia/Cloud/10 - DNS, CDN e borda/04 - TLS e certificados na borda|04 — TLS e certificados na borda]] — HTTPS gerenciado sem o pesadelo da renovação manual: handshake e terminação de raspão, SNI, terminar TLS perto do usuário, ACM (validação por DNS, renovação automática, a restrição us-east-1 para CloudFront); ACM ↔ Let's Encrypt gerenciado da DO.
5. [[03-Dominios/Tecnologia/Cloud/10 - DNS, CDN e borda/05 - A borda como camada|05 — A borda como camada]] — a nota-mapa: DNS+CDN+TLS costurados numa pilha de defesa, o request atravessando o perímetro inteiro, WAF (camada 7), Shield (camada 3/4), origin protection como princípio (prefix list + header secreto); a lacuna honesta de WAF na DO.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/10 - DNS, CDN e borda/06 - Arquitetura ponta a ponta (capstone do Bloco 2)|06 — Arquitetura ponta a ponta (capstone do Bloco 2)]] — costura os seis galhos do Bloco 2 numa arquitetura de referência three-tier completa (borda → ALB → ASG → RDS Multi-AZ + cache + S3), o request percorrendo a pilha inteira, a tabela de decisão do bloco, a fatura ilustrativa dos custos espalhados, e a ponte para o Bloco 3 (servers → serverless). Capstone do galho e do Bloco 2.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — o nome, o roteamento, o cache, o transporte seguro, a camada de defesa, e a síntese ponta a ponta no fim.

### Já opero na borda, quero fechar as lacunas

02 (a diferença exata entre as políticas de roteamento que toda entrevista cobra) → 04 (por que TLS termina na borda e como o certificado se renova sozinho) → 05 (a pilha de defesa inteira e por que o origin nunca é público) → 06 (a arquitetura ponta a ponta que amarra o Bloco 2).

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Cloud/10 - DNS, CDN e borda" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/09 - Bancos gerenciados/index|Bancos gerenciados]] — Galho 9, o estado que a arquitetura de referência protege atrás da borda
- [[03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)/index|Rede na nuvem (VPC)]] — Galho 7, a subnet privada e o security group que travam o origin
- [[03-Dominios/Tecnologia/Cloud/06 - Compute II — elasticidade e balanceamento/index|Compute II — elasticidade e balanceamento]] — Galho 6, o load balancer regional que fica atrás da borda global
- [[03-Dominios/Engenharia/Arquitetura/index|System Design]] — o conceito abstrato de CDN, LB e cache que este galho encarna em serviços gerenciados
