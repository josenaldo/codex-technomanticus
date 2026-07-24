---
title: "Roadmap — DNS, CDN e borda"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — DNS, CDN e borda (galho 10)

Roadmap-folha do galho `Cloud/10 - DNS, CDN e borda`. Bloco 2 (Os primitivos) — **galho que fecha o bloco**. Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - DNS na nuvem
- **Estado:** ✅ feita · fase: Iniciado · 263 linhas
- **Escopo:** DNS como serviço gerenciado — resolução recursivo vs autoritativo (root→TLD→autoritativo), zonas hospedadas + delegação por NS/glue, tipos de registro (A/AAAA/CNAME/MX/TXT/NS/ALIAS), CNAME não coexiste no apex + diferença crítica CNAME vs ALIAS/ANAME, TTL e propagação (baixar TTL antes de migração); Route 53 (hosted zones pública/privada, alias records) ↔ DO DNS (gratuito com nameservers da DO).

#### 02 - Roteamento DNS avançado
- **Estado:** ✅ feita · fase: Adepto · 329 linhas
- **Escopo:** o DNS como primeiro balanceador global — 8 políticas do Route 53 (simple, weighted 0-255 p/ canary, latency-based, geolocation + default `*`, geoproximity + bias, failover ativo-passivo, multivalue, IP-based), health checks (HTTP/HTTPS/TCP, limiar de 18% dos verificadores, RequestInterval 30s/10s), papel do TTL na velocidade do failover (30-60s), DR ativo-passivo; DO só round-robin nativo — roteamento avançado vive nos Load Balancers (Global LB GA recente), lacuna nomeada com honestidade.

#### 03 - CDN e cache de borda
- **Estado:** ✅ feita · fase: Adepto · 283 linhas
- **Escopo:** CDN como encarnação gerenciada do cache distribuído — CloudFront (distribution/origin/edge location), cache miss vs hit, cache behaviors por path pattern (ordem específico→genérico), TTL min/max/default (interação com Cache-Control), cache key (query string ignorada por padrão; menos na key = maior hit ratio), invalidação (1000 caminhos grátis/mês, wildcard/tag = 1 caminho, propagação em minutos) vs versionamento de nome, OAC (substitui OAI legado) travando o S3, edge compute de raspão; CDN embutida no DO Spaces (sem behaviors por path, sem OAC).

#### 04 - TLS e certificados na borda
- **Estado:** ✅ feita · fase: Adepto · 363 linhas
- **Escopo:** HTTPS gerenciado — handshake/terminação de raspão (fronteira p/ cripto), SNI (múltiplos certs num IP), terminação na borda vs pass-through vs re-encryption, terminar perto do usuário reduz latência do handshake, ACM (público gratuito, validação DNS por CNAME vs email, renovação automática, restrição us-east-1 p/ CloudFront), integração ACM↔CloudFront↔ALB; ACM ↔ DO (Let's Encrypt gerenciado nos LB/App Platform/Spaces, ou custom certificate).

#### 05 - A borda como camada
- **Estado:** ✅ feita · fase: Adepto · 306 linhas
- **Escopo:** a nota-mapa — DNS+CDN+TLS costurados numa pilha de defesa, o request atravessando o perímetro (diagrama central: DNS→TLS→Shield→WAF→cache→origin protegido), WAF camada 7 (web ACL, managed rule groups, rate-based, modo Count antes de Block, scope CLOUDFRONT em us-east-1), Shield camada 3/4 (Standard grátis automático vs Advanced US$3k/mês), origin protection como princípio (managed prefix list `origin-facing` + header secreto, defesa em profundidade); DO cobre 3/4 (DDoS Protection + Cloud Firewall grátis) mas SEM WAF nativo — camada 7 empurrada p/ Cloudflare/terceiros (honestidade categórica).

#### 06 - Arquitetura ponta a ponta (capstone do Bloco 2)
- **Estado:** ✅ feita · fase: Magus · 376 linhas · **FECHA o galho e o Bloco 2 inteiro**
- **Escopo:** costura os galhos 5-10 numa arquitetura de referência three-tier (borda → ALB público 2 AZ → EC2/ASG subnet privada app → RDS Multi-AZ subnet privada dados + ElastiCache + S3/OAC + NAT), request percorrendo a pilha até banco/cache/S3 e voltando (eleva o mapa da nota 05), tabela de decisão do Bloco 2 (requisito→primitivo→galho), custo como fio transversal (fatura ilustrativa dos custos espalhados nos galhos 5-10, marcada [!info]), ponte pro Bloco 3 (servers→serverless); versão DO simplificada (Droplets + LB + Managed DB + Spaces + Valkey + DNS, VPC plana sem NAT). Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Escrito em 2 ondas de 3 agentes (01-03, depois 04-06); orquestrador commitou serialmente (`c57d128`, `3b648bb`). 0 wikilinks quebrados no gate.
- **Contraste mecânica-vs-critério reconfirmado:** as notas Adepto de síntese/critério (02: 329, 03: 283, 05: 306) toparam abaixo do piso nominal (~400) SEM padding — densidade real cobrindo todo o escopo. A nota de mecânica (04: 363, TLS, 14 blocos de código) fechou mais alto. Nota-mapa (05) é síntese-de-camada: menos código, mais prosa conectiva. Piso é alvo, não gate; densidade ganha.
- Capstone (06) fechou 376 — abaixo da banda 400-460 dos capstones anteriores (galho 9: 430, galho 8: 428), mas denso e conectivo (3 Mermaid incl. a arquitetura de referência completa + versão DO, tabela de decisão do bloco, fatura de custo). Aceito como síntese, não inflado.
- Orquestrador corrigiu na nota 05 duas referências ambíguas "nota 07" → "Galho 7" dentro do diagrama Mermaid (o galho 10 não tem nota 07; a referência era ao Galho 7 VPC, corretamente linkado no corpo).
- **Path de Segurança inexistente:** o brief passou `Fundamentos/Segurança Conceitual/index` como possível alvo de wikilink (notas 04/05) — esse path NÃO existe neste vault (não há domínio `Fundamentos`; o mais próximo é `Engenharia/Segurança`). Agentes corretamente NÃO linkaram e mencionaram em prosa. Candidato a enriquecimento futuro: linkar `Engenharia/Segurança` se fizer sentido.
- Honestidade de paridade DO capturada: DO DNS só round-robin (sem weighted/latency/geo/failover nativo — vive nos Load Balancers/Global LB, nota 02); CDN embutida no Spaces sem behaviors por path nem OAC (nota 03); Let's Encrypt gerenciado ou custom cert (nota 04); DDoS Protection grátis camada 3/4 mas SEM WAF nativo — camada 7 via Cloudflare/terceiros (nota 05).
- Fatos datados marcados com [!info]: gratuidade do DO DNS (pricing deu 404 no fetch, mantido como fato conhecido sinalizado); CloudFront TTL/invalidação (1000 caminhos grátis/mês); us-east-1 obrigatório p/ cert CloudFront; Shield Advanced US$3k/mês (compromisso 1 ano); managed prefix list `com.amazonaws.global.cloudfront.origin-facing`; DO "does not support application layer (layer 7) protection" (citação exata); Global LB da DO (GA recente, mecânica interna não documentada).
- Fronteiras: conceito de CDN/LB/cache → System Design; cripto/TLS/PKI + SQLi/XSS → Segurança (prosa, path não existe no vault); DNS como protocolo → redes (prosa).
