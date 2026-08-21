---
title: "Cloud — API Gateway e edge de aplicação"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - api-gateway
  - edge
aliases:
  - "API Gateway e edge de aplicação"
  - "Galho 14 - API Gateway e edge de aplicação"
---

# API Gateway e edge de aplicação

> [!abstract] TL;DR
> Galho 14 da trilha Cloud, Bloco 3. Se o [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/index|galho 11]] construiu a função que processa uma requisição, este galho constrói a **borda de aplicação** que decide se essa requisição chega até ela — o API Gateway como porta de entrada gerenciada das APIs. O galho sobe da pergunta ao capítulo prático: primeiro o **porquê** (o front door de APIs, o problema de N serviços expostos sem fachada, a diferença com Load Balancer e CDN), depois a **anatomia** (REST vs HTTP vs WebSocket API, resources/methods/stages, os tipos de integration), depois duas notas de **política de borda** — throttling/quotas/caching e autorização (IAM, Cognito, Lambda authorizers, JWT) —, fecha com a honestidade sobre a **DigitalOcean** (que não tem API Gateway equivalente) e um **capstone** que compõe tudo numa arquitetura serverless completa. 6 notas, 3 fases, lente dupla AWS API Gateway ↔ DigitalOcean App Platform/Functions.

## Sobre este galho

Um API Gateway é a fachada única de um conjunto de APIs: um proxy reverso gerenciado que entende semântica de rota HTTP — método, path, header, corpo — e centraliza roteamento, autenticação, throttling, transformação de payload e caching antes que a requisição toque o backend. Ele resolve um problema muito concreto: sem ele, cada cliente precisa saber o endereço de N serviços, e cada serviço reimplementa a mesma lógica de auth, rate limit e CORS. Este galho ensina essa peça a fundo — e separa com honestidade o que ela oferece do que a DigitalOcean, sem um produto equivalente, pede pra compor com outras peças.

O fio condutor sobe do conceito à composição. Primeiro o *porquê* — o front door de APIs, a diferença de camada entre API Gateway, Load Balancer e CDN, e o casamento nativo com Lambda como trigger HTTP síncrono. Depois a *anatomia* em uma nota central: os três produtos do Amazon API Gateway (REST, HTTP, WebSocket) com anatomias e preços diferentes debaixo do mesmo nome, e a estrutura comum de resources, methods, integrations e stages. Depois duas notas de *política de borda*: throttling/quotas/caching (token bucket, usage plans, API keys, response cache) e autorização (AWS_IAM, Cognito authorizer, Lambda authorizer, JWT authorizer nativo, mTLS, resource policies) — cada uma linkando pra fronteira certa (Comunicação entre Sistemas, Auth e Identidade) em vez de reexplicar teoria de protocolo. Depois a *honestidade DigitalOcean* — o que App Platform (ingress) e Functions (HTTP trigger) cobrem, o que falta, e os dois caminhos reais pra preencher a lacuna (Cloudflare, ou Kong/APISIX próprio). E fecha com o *capstone*: uma arquitetura de checkout serverless completa, cliente → DNS/CDN → API Gateway (JWT authorizer + throttle) → Lambda → mensageria, nomeando a pilha de cinco decisões que fecham qualquer borda de API em produção.

**Audiência primária:** quem sabe que existe um "API Gateway" na AWS mas nunca decidiu, com intenção, entre REST API e HTTP API, nem entende por que throttling e autenticação vivem na borda em vez de dentro do código. **Audiência secundária:** quem já usa API Gateway com Lambda mas nunca formalizou a diferença entre os quatro mecanismos de autorização, ou nunca precisou desenhar a mesma arquitetura sem a peça pronta — como acontece na DigitalOcean.

> [!info] Fronteira
> O **conceito** de rate limiting (token bucket, sliding window) e caching como estratégia (cache-aside, invalidação) vive em [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]]; o **protocolo** de autenticação e autorização (OAuth 2.1, OIDC, anatomia de um JWT) vive em [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]] — mencionado aqui apenas na página deste galho. A **borda de rede** (DNS, CDN, TLS, WAF) é o Galho 10 desta trilha; a **função serverless** que o Gateway aciona é o Galho 11; a **mensageria** que recebe o evento publicado depois da resposta é tratada num galho posterior desta trilha. Este galho trata a borda de *aplicação* — a fachada que entende rota e cliente — e linka essas fronteiras em vez de reexplicá-las.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/14 - API Gateway e edge de aplicação/01 - Por que um API Gateway|01 — Por que um API Gateway]] — o front door de APIs: o problema de N serviços sem fachada única, o conceito de proxy reverso com semântica de API, a diferença de camada com Load Balancer e CDN, o casamento com serverless (API Gateway como trigger HTTP do Lambda); AWS Amazon API Gateway ↔ DO sem equivalente dedicado (App Platform ingress + Functions HTTP trigger).

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/14 - API Gateway e edge de aplicação/02 - Tipos e anatomia do API Gateway|02 — Tipos e anatomia do API Gateway]] — três produtos, uma marca: REST API (rico: cache, usage plans, WAF, VTL) vs HTTP API (enxuto: JWT nativo, deploy automático, mais barato) vs WebSocket API (conexão persistente, $connect/$disconnect/$default); a anatomia comum de resources, methods, integrations (Lambda proxy/non-proxy, HTTP, AWS service, VPC Link) e stages; DO só tem routing por path, sem os três sabores.
3. [[03-Dominios/Tecnologia/Cloud/14 - API Gateway e edge de aplicação/03 - Throttling, quotas e caching|03 — Throttling, quotas e caching]] — o token bucket na porta (rate/burst, `429`), usage plans + API keys como mecanismo de monetização de API, response caching por estágio (TTL, cache key, invalidação); as três camadas de defesa em profundidade antes do Lambda; ponte→Comunicação entre Sistemas; DO sem equivalente gerenciado.
4. [[03-Dominios/Tecnologia/Cloud/14 - API Gateway e edge de aplicação/04 - Autorização na borda de API|04 — Autorização na borda de API]] — os quatro mecanismos de "quem entra": AWS_IAM (SigV4, serviço-a-serviço), Cognito user pools authorizer (JWT gerenciado, zero código), Lambda authorizer (TOKEN/REQUEST, válvula de escape com lógica própria), JWT authorizer nativo (HTTP API, qualquer provedor OIDC); mTLS e resource policies como filtros de rede antes do authorizer; ponte→Auth e Identidade; DO sem authorizer gerenciado, validação vira código na app.
5. [[03-Dominios/Tecnologia/Cloud/14 - API Gateway e edge de aplicação/05 - A borda de API na DigitalOcean e alternativas|05 — A borda de API na DigitalOcean e alternativas]] — a honestidade de frente: DO não tem API Gateway; App Platform ingress resolve só roteamento por path, Functions expõe HTTP direto sem gateway na frente; os dois caminhos reais pra preencher a lacuna (Cloudflare na frente, ou Kong/APISIX próprio em Droplet/DOKS); e, de brinde, quando o próprio API Gateway da AWS não é a resposta certa (ALB→Lambda direto, CloudFront + Lambda@Edge).

## Magus

6. [[03-Dominios/Tecnologia/Cloud/14 - API Gateway e edge de aplicação/06 - Compondo a borda de API (capstone)|06 — Compondo a borda de API]] — uma arquitetura de checkout serverless completa (cliente → DNS/CDN → API Gateway com JWT authorizer + throttle → Lambda → banco → EventBridge) amarrando as cinco notas anteriores; a pilha de cinco decisões que fecham qualquer borda de API (REST vs HTTP, qual authorizer, throttle, cache, custom domain); os padrões BFF e API composition; os três anti-padrões mais comuns em produção; a mesma arquitetura montada na DigitalOcean por composição, sem API Gateway nativo. Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — o porquê, a anatomia, as duas políticas de borda, a honestidade DigitalOcean, e a composição final.

### Já uso API Gateway com Lambda, quero fechar as lacunas

02 (a diferença REST vs HTTP API que a maioria escolhe no piloto automático) → 04 (os quatro mecanismos de autorização e quando cada um vale) → 06 (a pilha de decisões e os anti-padrões que separam uma borda bem desenhada de uma que só trocou "servidor" por "função").

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/index|Serverless e FaaS — Lambda a fundo]] — Galho 11, o Lambda que este galho aciona via trigger HTTP síncrono
- [[03-Dominios/Tecnologia/Cloud/10 - DNS, CDN e borda/index|DNS, CDN e borda]] — Galho 10, a borda de rede que fica um passo antes da borda de aplicação
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — o conceito de rate limiting e caching que a política de borda deste galho encarna
