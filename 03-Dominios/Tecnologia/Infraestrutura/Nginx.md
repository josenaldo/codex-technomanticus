---
title: "Nginx"
created: 2026-04-01
updated: 2026-08-08
type: reference
progress: done
status: evergreen
tags:
  - infraestrutura
  - devops
  - entrevista
publish: false
---

# Nginx

> [!info] Tronco podado — o capítulo virou galho
> Esta nota era um monólito de referência técnica de ~1285 linhas. Em 2026-08-08 ela foi **podada**: o conteúdo conceitual virou o galho [[03-Dominios/Tecnologia/Infraestrutura/Nginx/index|Nginx]], com 16 notas em 3 fases sob a lente *o ciclo de vida de uma request*. O que permanece aqui é o material que **não pertence ao galho**: o relato de experiência do autor e o material de articulação em inglês, ambos preservados na íntegra.

## Onde cada assunto foi parar

| Assunto que estava aqui | Onde está agora |
|---|---|
| O que é Nginx, arquitetura, master/worker | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/01 - O problema que o Nginx resolve\|01 — O problema que o Nginx resolve]] |
| Estrutura da configuração, contextos | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/02 - A estrutura da configuração\|02 — A estrutura da configuração]] |
| Server block, virtual host | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/03 - Como o Nginx escolhe o server block\|03 — Como o Nginx escolhe o server block]] |
| Location blocks e ordem de match | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/04 - location e a tabela de precedência\|04 — location e a tabela de precedência]] |
| — (assunto novo, não existia aqui) | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/05 - O ciclo de vida de uma request\|05 — O ciclo de vida de uma request]] |
| Static file serving, `try_files` | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/06 - Servir arquivos estáticos\|06 — Servir arquivos estáticos]] |
| Reverse proxy, headers, timeouts, buffers, WebSocket, gRPC | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/07 - Proxy reverso\|07 — Proxy reverso]] |
| Load balancing, algoritmos, health checks | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/08 - upstream e balanceamento\|08 — upstream e balanceamento]] · teoria em [[03-Dominios/Ciência/Redes e Protocolos/13 - Load balancing e CDN\|Redes: Load balancing e CDN]] |
| TLS/HTTPS, Let's Encrypt, HTTP/2 e HTTP/3, mTLS | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/09 - TLS no Nginx\|09 — TLS no Nginx]] · teoria em [[03-Dominios/Ciência/Redes e Protocolos/05 - TLS e HTTPS\|Redes: TLS e HTTPS]] |
| Caching, cache key, respeitar headers do backend | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/10 - Cache no Nginx\|10 — Cache no Nginx]] · semântica em [[03-Dominios/Ciência/Redes e Protocolos/08 - Caching HTTP\|Redes: Caching HTTP]] |
| Compressão, rate limiting, connection limiting, limitar body | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/11 - Limitar e comprimir\|11 — Limitar e comprimir]] |
| Variáveis, redirects, `try_files`, logging, log em JSON | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/12 - Variáveis, map, rewrite e logging\|12 — Variáveis, map, rewrite e logging]] |
| Troubleshooting, `nginx -t`, `stub_status`, erros comuns, patterns de produção | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/13 - Tuning e diagnóstico\|13 — Tuning e diagnóstico]] |
| Nginx em containers, Docker image, Kubernetes Ingress Controller | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/14 - Nginx em container e como Ingress Controller\|14 — Nginx em container e como Ingress Controller]] |
| Alternativas modernas | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/15 - O ecossistema além do Nginx\|15 — O ecossistema além do Nginx]] |
| Security headers, config de produção completa | [[03-Dominios/Tecnologia/Infraestrutura/Nginx/16 - Capstone - a borda de uma aplicação\|16 — Capstone: a borda de uma aplicação]] |
| Armadilhas comuns | distribuídas na seção `## Armadilhas comuns` de cada nota do galho |

> [!warning] O que mudou desde que este monólito foi escrito
> Este tronco data de abril de 2026 e alguns trechos dele **envelheceram**. Três casos que o galho corrige, com a versão cravada: o par `proxy_http_version 1.1;` + `proxy_set_header Connection "";` deixou de ser necessário para keepalive de upstream na **1.29.7** (o keepalive passou a vir ligado por padrão, e o padrão do `proxy_http_version` virou `1.1`); o parâmetro `http2` dentro de `listen` está **depreciado** desde a **1.25.1** em favor da diretiva `http2` própria; e o `ingress-nginx` foi **aposentado** pelo Kubernetes SIG Network, sem correção de segurança desde março de 2026. O material preservado abaixo **não foi alterado** — é relato datado, e vale como tal.

## Na prática (da minha experiência)

> **Nginx é meu reverse proxy default** há anos. No MedEspecialista, Nginx está na frente de todos os serviços — terminando TLS, fazendo rate limiting, passando request_id para tracing, logando em JSON.
>
> **Config básica que uso em todo projeto:**
>
> ```nginx
> server_tokens off;
> client_max_body_size 10m;
> keepalive_timeout 65;
>
> # TLS forte
> ssl_protocols TLSv1.2 TLSv1.3;
> ssl_prefer_server_ciphers off;
>
> # Headers
> add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
> add_header X-Frame-Options SAMEORIGIN always;
> add_header X-Content-Type-Options nosniff always;
> add_header Referrer-Policy strict-origin-when-cross-origin always;
>
> # Compressão
> gzip on;
> gzip_comp_level 6;
> gzip_types text/css application/javascript application/json;
>
> # Proxy
> proxy_http_version 1.1;
> proxy_set_header Host $host;
> proxy_set_header X-Real-IP $remote_addr;
> proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
> proxy_set_header X-Forwarded-Proto $scheme;
> proxy_set_header X-Request-ID $request_id;
> proxy_connect_timeout 5s;
> proxy_read_timeout 60s;
> proxy_send_timeout 60s;
> ```
>
> **Incidente memorável — 504 intermitente:**
>
> API começou a dar 504 esporadicamente. Logs do Nginx mostravam upstream timeout, mas backend estava saudável. Investigação: `proxy_read_timeout 60s` era o limit, e uma query lenta de relatório levava 70s em alguns casos. Fix temporário: aumentar timeout para 180s na location `/reports/`. Fix real: otimizar a query no backend.
>
> **Outro — rate limit quebrando requests legítimos:**
>
> Usuários reclamavam de 429 Too Many Requests. Diagnóstico: `limit_req_zone $binary_remote_addr rate=10r/s` era muito baixo para apps mobile fazendo prefetch. Fix: aumentar para 30r/s com `burst=60 nodelay`, e rate limit separado por endpoint (mais restritivo só em `/login`, `/signup`).
>
> **WebSocket por Nginx — config que funciona:**
>
> ```nginx
> map $http_upgrade $connection_upgrade {
>     default upgrade;
>     '' close;
> }
>
> location /ws/ {
>     proxy_pass http://ws-backend;
>     proxy_http_version 1.1;
>     proxy_set_header Upgrade $http_upgrade;
>     proxy_set_header Connection $connection_upgrade;
>     proxy_read_timeout 3600s;
>     proxy_send_timeout 3600s;
> }
> ```
>
> **A lição principal:** Nginx é simples em casos simples, mas tem muitas armadilhas. Read the docs (são ótimas), teste com `nginx -t` religiosamente, use healthchecks e rate limiting, e logue estruturado desde o dia 1.

---

## How to explain in English

> "Nginx is my default reverse proxy for pretty much any production system. It handles TLS termination, load balancing, static files, rate limiting, caching, and security headers — all with minimal resource overhead thanks to its event-driven architecture.
>
> My baseline configuration starts with strong TLS (TLS 1.2 and 1.3 only, modern cipher suites), HSTS, security headers, gzip compression, and proper forwarded headers so the backend sees the real client IP and protocol. For reverse proxy, I always set `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`, `Host`, and `X-Request-ID` — the last one lets me propagate a request ID for distributed tracing.
>
> For load balancing, round-robin is the default but I often use `least_conn` when backend pods have variable workloads. Health checks are passive in open-source Nginx with `max_fails` and `fail_timeout`. For active health checks and fancier load balancing, you need Nginx Plus or a different tool.
>
> I always configure rate limiting with `limit_req_zone` — different zones for login, API, and general traffic. The `burst` parameter with `nodelay` handles traffic spikes gracefully. For API authentication, I use `map` to exempt premium keys from limits.
>
> Logging goes structured — JSON format with `$request_time`, `$upstream_response_time`, and `$request_id` — makes ingesting into Elasticsearch or Loki trivial. I never run `server_tokens on` in production, never reload without `nginx -t`, and I monitor stub_status or Prometheus exporter for basic health metrics.
>
> For WebSocket, you need `proxy_http_version 1.1` and the Upgrade/Connection headers, plus long timeouts since connections stay idle. For gRPC, use `grpc_pass` instead of `proxy_pass`.
>
> Common pitfalls I watch for: forgetting `client_max_body_size` so uploads fail silently with 413, `proxy_read_timeout` too low causing 504, missing security headers, running as root, and using `if` inside location blocks where it has unexpected behavior."

### Frases úteis em entrevista

- "Nginx's event-driven architecture solved the C10K problem — thousands of connections per worker with minimal memory."
- "I always pass forwarded headers so the backend sees the real client."
- "TLS 1.2 and 1.3 only, strong ciphers, HSTS, OCSP stapling — my baseline."
- "`nginx -t` before every reload, always."
- "Rate limiting with `limit_req_zone` is the first defense against abuse."
- "Structured JSON logging makes centralized logging trivial."
- "`gzip_static` serves pre-compressed files — zero CPU cost."
- "WebSocket needs HTTP 1.1 and Upgrade headers."
- "Passive health checks with `max_fails` and `fail_timeout` in OSS Nginx."
- "`proxy_http_version 1.1` + empty Connection header for upstream keepalive."

### Key vocabulary

- servidor web → web server
- proxy reverso → reverse proxy
- balanceamento de carga → load balancing
- upstream → upstream
- terminação TLS → TLS termination
- cabeçalho → header
- limitação de taxa → rate limiting
- cache de proxy → proxy cache
- host virtual → virtual host
- reescrita → rewrite
- redirecionamento → redirect
- worker → worker process
- reinicialização graciosa → graceful reload
- erro do gateway → gateway error (502, 504)
- manter vivo → keepalive

---

## Recursos

### Documentação

- [Nginx Docs](https://nginx.org/en/docs/)
- [Nginx Admin Guide](https://docs.nginx.com/nginx/admin-guide/)

### Livros

- **Nginx Cookbook** — Derek DeJonghe (O'Reilly)
- **Nginx HTTP Server** — Clément Nedelcu

### Ferramentas

- [nginx.conf generator (DigitalOcean)](https://www.digitalocean.com/community/tools/nginx)
- [Nginx Playground](https://nginx-playground.wizardzines.com/) — Julia Evans
- [SSL Labs Test](https://www.ssllabs.com/ssltest/) — testa TLS config
- [nginx-prometheus-exporter](https://github.com/nginxinc/nginx-prometheus-exporter)
- [GoAccess](https://goaccess.io/) — analyze access logs em tempo real

### Alternativas modernas

Caddy, Traefik, Envoy, HAProxy — e os forks `freenginx` e Angie — estão tratados com fonte e data em [[03-Dominios/Tecnologia/Infraestrutura/Nginx/15 - O ecossistema além do Nginx|15 — O ecossistema além do Nginx]].

---

## Veja também

- [[03-Dominios/Tecnologia/Infraestrutura/Nginx/index|Nginx (galho)]] — as 16 notas que saíram daqui
- [[03-Dominios/Tecnologia/Infraestrutura/index|Infraestrutura]] — o domínio
- [[Linux]] — fundação
- [[Docker]] — Nginx em containers
- [[Kubernetes]] — o Ingress cujo controlador é um Nginx
- [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]] — HTTP, TLS, cache e balanceamento como teoria
- [[03-Dominios/Engenharia/Arquitetura/System Design/index|System Design]] — load balancing em arquitetura
- [[CI-CD]] — deploy de config Nginx
- [[Observabilidade]] — Nginx metrics e logs
