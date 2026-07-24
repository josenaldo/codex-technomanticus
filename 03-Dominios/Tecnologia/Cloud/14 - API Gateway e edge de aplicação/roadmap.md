---
title: "Roadmap — API Gateway e edge de aplicação"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — API Gateway e edge de aplicação (galho 14)

Roadmap-folha do galho `Cloud/14 - API Gateway e edge de aplicação`. Bloco 3 (Serverless e arquiteturas modernas). Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - Por que um API Gateway
- **Estado:** ✅ feita · fase: Iniciado · 222 linhas
- **Escopo:** o problema de N serviços expostos sem fachada única (cliente precisa saber endereço/auth/rate-limit de cada um), o conceito de proxy reverso gerenciado com semântica de API (roteamento, auth, throttling, transformação, caching, observabilidade), API Gateway vs Load Balancer vs borda de rede/CDN (camadas diferentes da requisição), o casamento com serverless (Gateway como trigger HTTP síncrono do Lambda), lente dupla Amazon API Gateway (REST/HTTP/WebSocket, tabela de tipos) ↔ DigitalOcean sem produto equivalente (App Platform `ingress.rules`, Functions HTTP triggers), 3 casos práticos (multi-serviço via YAML, App Platform ingress, trigger síncrono do Lambda), tabela de tradução Azure/GCP.

#### 02 - Tipos e anatomia do API Gateway
- **Estado:** ✅ feita · fase: Adepto · 318 linhas · nota central de mecânica (comandos AWS CLI)
- **Escopo:** os três produtos do Amazon API Gateway — REST API (rico: usage plans/API keys, cache gerenciado, WAF, mapping templates VTL, edge-optimized), HTTP API (enxuto: JWT authorizer nativo, deploy automático, ~70% mais barato), WebSocket API (conexão persistente, rotas $connect/$disconnect/$default/customizadas, connectionId); anatomia comum (resources, methods, integrations, stages, stage variables); 4 integration types (Lambda proxy, Lambda non-proxy + VTL, HTTP, AWS service integration, VPC Link); request/response (mapping templates, payload passthrough, CORS); deployment (canary release, custom domain + ACM); observabilidade (execution logs do REST API vs ausência no HTTP API); criação via CLI (apigatewayv2 vs apigateway completo); lente DO — routing, não gateway (sem VTL/stages versionados/usage plans/VPC Link).

#### 03 - Throttling, quotas e caching
- **Estado:** ✅ feita · fase: Adepto · 301 linhas
- **Escopo:** throttling via token bucket (rate/burst, `429`, 4 camadas de limite — AWS fixo/conta/API-estágio/método/cliente), limite de conta padrão 10.000 RPS/burst 5.000 (2.500/1.250 em regiões novas), throttling best-effort não garantido; usage plans + API keys como mecanismo de monetização de API (quota + throttle por cliente); response caching (REST API só, TTL default 300s/máx 3.600s, cache key, invalidação via `flush-stage-cache` ou header, métricas CacheHitCount/CacheMissCount); pilha de defesa em profundidade (cache → quota → throttle → backend); ponte→Comunicação entre Sistemas (conceito de caching/rate limiting); caso prático de catálogo com 2 tiers; DO sem equivalente — implementação própria (express-rate-limit) ou proxy de terceiro.

#### 04 - Autorização na borda de API
- **Estado:** ✅ feita · fase: Adepto · 348 linhas
- **Escopo:** os quatro mecanismos de "quem entra": AWS_IAM (SigV4, service-to-service, identity-based policy + `execute-api:Invoke`), Cognito user pools authorizer (JWT gerenciado zero-código, claims em `$context.authorizer.claims`), Lambda authorizer TOKEN vs REQUEST (política IAM allow/deny, cache TTL padrão 300s/máx 3.600s, `context` livre pro backend), JWT authorizer nativo (só HTTP API, qualquer provedor OIDC, Issuer/Audience declarativos, cache de JWKS por até 2h, armadilha aud-vence-client_id); mTLS (handshake, truststore S3) e resource policies (IP/VPC) como filtros de rede antes do authorizer; tabela de cenário→mecanismo; ponte→Auth e Identidade (OAuth/OIDC/JWT como protocolo); DO sem authorizer gerenciado — validação vira middleware na app ou na Function.

#### 05 - A borda de API na DigitalOcean e alternativas
- **Estado:** ✅ feita · fase: Adepto · 258 linhas
- **Escopo:** honestidade central do galho — DO não tem API Gateway; App Platform `ingress` resolve só roteamento por path (TLS automático, CORS por regra, sem throttling/usage plans/authorizer); Functions expõe HTTP direto com só limites de plataforma (600 inv/min, 120 concorrentes, payload 1MB), não política por cliente; dois caminhos honestos — Cloudflare na frente (rate limit, WAF, Access; duas contas, duas faturas) ou proxy próprio Kong/APISIX em Droplet/DOKS (controle total, perde "gerenciado"); segunda honestidade dentro da própria AWS — ALB→Lambda direto e CloudFront+Lambda@Edge como alternativas ao API Gateway em alto volume; caso prático evolutivo (MVP→parceiros→transformação de contrato) mostrando os caminhos se somando; tabela REST/HTTP/ALB.

#### 06 - Compondo a borda de API (capstone)
- **Estado:** ✅ feita · fase: Magus · 414 linhas · **FECHA o galho**
- **Escopo:** arquitetura de checkout serverless completa (cliente → Route53/CloudFront → API Gateway HTTP API + JWT authorizer + throttle → Lambda → RDS → EventBridge → 3 consumidores assíncronos), separando explicitamente a borda síncrona (este galho) da mensageria assíncrona (galho posterior); pilha de 5 decisões que fecham qualquer borda (REST vs HTTP API, qual authorizer, throttle sempre presente, cache só onde idempotente, custom domain); os dois caminhos de rejeição (401/429) e o custo zero de Lambda/RDS quando a borda barra; dois padrões de composição — BFF e API composition (com exemplo de orquestração `Promise.all`); três costuras nomeadas com galho 11 (Lambda)/galho 12 (Containers)/mensageria; a mesma arquitetura montada na DO por composição (Cloudflare + App Platform + Function, auth em código); tabela de decisão final + tabela de "o que cobra cada camada" (sem número somado); honestidade final — quando ALB→Lambda substitui o Gateway mesmo na AWS; 3 anti-padrões (Gateway como service mesh interno, lógica de negócio em VTL, throttling esquecido); verificação por comando (não memória). Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Roadmap gerado retroativamente a partir das 6 notas já escritas (não houve execução via `enriquecer-galho`/`diagnosticar-galho` nesta sessão — as notas já existiam completas no disco).
- Todas as 6 notas datadas `created`/`updated: 2026-07-24`, `status: seedling`, `fase` consistente com a progressão Iniciado(1)→Adepto(4)→Magus(1) do padrão de 3 fases.
- Fronteiras nomeadas de forma consistente nas 6 notas: conceito de rate limiting/caching → Comunicação entre Sistemas; protocolo OAuth/OIDC/JWT → Auth e Identidade; borda de rede (DNS/CDN/TLS) → Galho 10; função serverless acionada → Galho 11; mensageria assíncrona pós-resposta → galho posterior da trilha (mencionado em prosa nas notas 03 e 06, sem wikilink — galho não confirmado nesta sessão).
- Honestidade DigitalOcean é o fio condutor do galho, não só da nota 05: cada nota (01, 02, 03, 04) já registra a lacuna específica daquela camada antes da nota 05 consolidar tudo, e o capstone (06) monta a arquitetura equivalente por composição (Cloudflare + App Platform + Function) em vez de fingir paridade.
- Duas notas ([[03-Dominios/Tecnologia/Cloud/14 - API Gateway e edge de aplicação/01 - Por que um API Gateway|01]] e [[03-Dominios/Tecnologia/Cloud/14 - API Gateway e edge de aplicação/05 - A borda de API na DigitalOcean e alternativas|05]]) registram tentativas de WebFetch em páginas específicas de docs.digitalocean.com que retornaram 404 — marcadas com `[!info] Verificado` explicando o que ficou confirmado por fontes estáveis vs o que precisa reconferência.
- Contraste mecânica-vs-síntese: nota de mecânica pura (02: 318 linhas, comandos AWS CLI extensos) e capstone (06: 414 linhas, o mais longo do galho, com 2 arquiteturas completas + tabela de custo) ficam nas bandas mais altas; nota de abertura (01: 222 linhas) e a mais enxuta do galho (03: 301) cobrem o escopo sem padding aparente.
