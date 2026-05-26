---
title: "Nginx"
created: 2026-04-01
updated: 2026-04-11
type: concept
status: evergreen
tags:
  - infraestrutura
  - devops
  - entrevista
publish: false
---

# Nginx

Deep dive em **Nginx** — web server, reverse proxy, load balancer, TLS termination, cache HTTP. Para Linux, ver [[Linux]]. Para Kubernetes Ingress, ver [[Kubernetes]]. Para performance web, ver [[Redes e Protocolos]].

## O que é

**Nginx** (pronuncia-se "engine-x") é um **web server de alto desempenho** criado em 2004 por **Igor Sysoev** para resolver o **C10K problem** — servir 10.000 conexões simultâneas em uma única máquina. Baseado em **event-driven architecture** (single-threaded, non-blocking I/O), usa muito menos memória que Apache e escala muito melhor.

**Usos principais:**

1. **Reverse proxy** — front para aplicações (Node, Java, Python, Go)
2. **Load balancer** — distribui tráfego entre múltiplas instâncias
3. **Static file serving** — HTML, CSS, JS, imagens
4. **TLS termination** — decripta HTTPS, fala HTTP com backend
5. **HTTP cache** — cache de respostas para reduzir carga no backend
6. **API gateway** — rate limiting, auth, routing por path/host
7. **Ingress controller** em Kubernetes (nginx-ingress)

**Nginx vs Apache:**

| | Nginx | Apache |
| --- | --- | --- |
| Modelo | Event-driven | Process/thread per connection |
| Memória por conexão | Baixíssima | Alta |
| Performance estática | Altíssima | Alta |
| Módulos dinâmicos | Limitado | Rico |
| `.htaccess` | Não | Sim |
| Configuração | Centralizada | Distribuída |
| Adoção (2026) | Dominante | Legacy em apps novas |

Em 2026, Nginx é o **reverse proxy mais usado do mundo** — 33%+ dos sites ativos.

Em entrevistas, o que diferencia um senior em Nginx:

1. **Entender o modelo event-driven** — workers, conexões, async
2. **Reverse proxy com upstream** — `proxy_pass`, headers, buffering
3. **Load balancing algorithms** — round-robin, least_conn, ip_hash
4. **TLS hardening** — protocols, ciphers, HSTS, OCSP stapling
5. **Rate limiting** — zones, burst, shared memory
6. **Caching HTTP** — `proxy_cache`, invalidation, headers
7. **Logging estruturado** — JSON logs, access + error
8. **Troubleshooting** — 502 Bad Gateway, 504 Gateway Timeout, upstream errors
9. **Security** — headers, request body limits, timeouts

---

## Arquitetura

Nginx tem um **master process** (root) que lê config e gerencia **worker processes** (non-root):

```
┌────────────────────┐
│   master process   │  (root)
│   - lê config       │
│   - gerencia workers│
└────────┬────────────┘
         │
         ├─────────┬─────────┬─────────┐
         │         │         │         │
         ↓         ↓         ↓         ↓
     worker 1  worker 2  worker 3  worker 4
     (nobody)  (nobody)  (nobody)  (nobody)
         │
         │  cada worker: event loop
         │  ┌──────────────────────┐
         │  │  epoll/kqueue        │
         │  │  (async I/O)         │
         │  └──────────────────────┘
         │  milhares de conexões
```

**Event-driven model:**

- Cada worker é **single-threaded** com event loop (similar a Node.js)
- Usa **epoll** (Linux), **kqueue** (BSD), **eventport** (Solaris) — notificações assíncronas do kernel
- Uma conexão = ~2.5KB de memória
- Um worker pode servir **milhares** de conexões simultâneas

**Por que é rápido:**

- Sem overhead de thread/process por conexão
- Context switches mínimos
- Copy reduzido (sendfile, zero-copy)
- Non-blocking I/O em tudo

**Workers = número de CPU cores** (típico). Configure com:

```nginx
worker_processes auto;  # auto-detect número de cores
```

---

## Estrutura da configuração

Config principal em `/etc/nginx/nginx.conf`. Organizada em **blocos** (contextos) hierárquicos:

```nginx
# Main context
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    # HTTP-level config
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    sendfile on;
    tcp_nopush on;
    keepalive_timeout 65;
    gzip on;

    # Include de outros arquivos
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;

    server {
        # Server (virtual host)
        listen 80;
        server_name example.com;

        location / {
            # Location (path)
            root /var/www/html;
            index index.html;
        }
    }
}
```

**Contextos (blocos):**

- **main** — config global, top level
- **events** — conexões
- **http** — config de HTTP (o mais usado)
  - **server** — virtual host
    - **location** — rota/path
  - **upstream** — backend pool
- **mail** — proxy SMTP/POP3/IMAP (raro)
- **stream** — proxy TCP/UDP (não HTTP)

### Comandos essenciais

```bash
# Validar config
sudo nginx -t
sudo nginx -T                  # dump config completa

# Reload sem downtime
sudo nginx -s reload           # SIGHUP
sudo systemctl reload nginx

# Restart
sudo systemctl restart nginx

# Status
sudo systemctl status nginx

# Logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u nginx -f
```

**Regra:** **sempre** `nginx -t` antes de reload. Config inválida e reload = servidor morto.

---

## Server e location blocks

### Server block — virtual host

```nginx
server {
    listen 80;
    listen [::]:80;                        # IPv6
    server_name example.com www.example.com;

    root /var/www/example;
    index index.html;

    access_log /var/log/nginx/example.access.log;
    error_log /var/log/nginx/example.error.log;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**`server_name` matching:**

```nginx
server_name example.com;                  # exato
server_name *.example.com;                 # wildcard
server_name example.*;                     # wildcard
server_name ~^www\d+\.example\.com$;       # regex (começa com ~)
server_name _;                             # catch-all
```

**Default server:**

```nginx
server {
    listen 80 default_server;
    return 444;                            # drop connection
}
```

Requests que não casam com nenhum `server_name` caem no default.

### Location blocks

```nginx
server {
    location / {                           # match prefix
        ...
    }

    location /api/ {                       # match prefix "/api/"
        ...
    }

    location = /health {                   # match exato
        return 200 "OK";
    }

    location ~ \.php$ {                    # regex (case sensitive)
        ...
    }

    location ~* \.(jpg|png|gif)$ {         # regex case-insensitive
        expires 30d;
    }

    location ^~ /static/ {                 # prefix match, não verifica regex
        alias /var/www/static/;
    }
}
```

**Ordem de matching:**

1. **`= path`** — match exato (mais rápido)
2. **`^~ path`** — prefix match sem verificar regex
3. **`~ pattern` / `~* pattern`** — regex (na ordem de aparição)
4. **`path`** — prefix match (usa o mais longo)

---

## Reverse proxy

O uso mais comum — Nginx recebe requests externos e os encaminha para backends.

### Setup básico

```nginx
upstream backend {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Headers importantes

```nginx
# Passar informação real do cliente
proxy_set_header Host $host;                    # hostname original
proxy_set_header X-Real-IP $remote_addr;        # IP do cliente
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;    # http ou https
proxy_set_header X-Forwarded-Host $host;
proxy_set_header X-Forwarded-Port $server_port;
```

**Por que:** o backend precisa saber quem é o cliente real, não o proxy. Sem `X-Forwarded-*`, o backend vê tudo vindo de `127.0.0.1`.

**No backend, configure** para confiar no proxy:

- **Spring Boot:** `server.forward-headers-strategy=native`
- **Express:** `app.set('trust proxy', 'loopback')`
- **Django:** `USE_X_FORWARDED_HOST = True`

### Timeouts

```nginx
proxy_connect_timeout 5s;        # conectar ao upstream
proxy_send_timeout 60s;           # enviar request
proxy_read_timeout 60s;           # esperar response
```

**Erros comuns:**

- **502 Bad Gateway** — upstream não respondeu ou respondeu inválido
- **504 Gateway Timeout** — timeout estourado
- **503 Service Unavailable** — todos upstreams down

### WebSocket

Nginx precisa de config especial para upgrade HTTP → WebSocket:

```nginx
location /ws/ {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 3600s;                   # WS pode ficar idle
}
```

### gRPC

```nginx
location / {
    grpc_pass grpc://backend;
    grpc_set_header Host $host;
}
```

### Buffers

Nginx lê response do upstream para buffer antes de enviar ao cliente:

```nginx
proxy_buffering on;                            # default
proxy_buffer_size 4k;
proxy_buffers 8 4k;
proxy_busy_buffers_size 8k;
```

**Desligar buffering** (streaming, SSE):

```nginx
proxy_buffering off;
```

---

## Load balancing

```nginx
upstream backend {
    # Algoritmo (default: round-robin)
    least_conn;                     # menos conexões ativas

    server backend1.example.com:3000 weight=3;
    server backend2.example.com:3000 weight=1;
    server backend3.example.com:3000 backup;      # só se todos falham
    server backend4.example.com:3000 down;         # removido

    # Health check passivo
    server backend5.example.com:3000 max_fails=3 fail_timeout=30s;

    # Keepalive
    keepalive 32;
}

server {
    location / {
        proxy_pass http://backend;

        # Necessário para keepalive funcionar
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

### Algoritmos

| Algoritmo | Comportamento | Uso |
| --- | --- | --- |
| **round-robin** (default) | Distribui sequencialmente | Servidores iguais |
| **least_conn** | Para com menos conexões ativas | Cargas desiguais |
| **ip_hash** | Mesmo IP → mesmo servidor | Sessions sticky |
| **hash $variable** | Hash customizado | Caching consistente |
| **random** | Aleatório (com two_choices) | Grandes pools |

**Sticky sessions via cookie** (módulo comercial ou nginx-sticky-module):

```nginx
upstream backend {
    server backend1;
    server backend2;
    sticky cookie srv_id expires=1h;
}
```

### Health checks

**Passivo (OSS):**

```nginx
server backend1 max_fails=3 fail_timeout=30s;
```

Se 3 falhas em 30s, marcado como down por 30s.

**Ativo** (Nginx Plus ou módulos de terceiros):

```nginx
location / {
    proxy_pass http://backend;
    health_check interval=5s fails=3 passes=2 uri=/health;
}
```

---

## TLS / HTTPS

### Config básica

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Protocols — só TLS 1.2 e 1.3
    ssl_protocols TLSv1.2 TLSv1.3;

    # Ciphers fortes
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Session
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
    resolver 8.8.8.8 1.1.1.1 valid=300s;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # ... resto da config
}

# HTTP → HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### Let's Encrypt com certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renew (via systemd timer ou cron)
sudo certbot renew --dry-run
```

Certbot atualiza a config do Nginx automaticamente.

### HTTP/2 e HTTP/3

```nginx
# HTTP/2 (default em 2026)
listen 443 ssl http2;

# HTTP/3 (experimental)
listen 443 ssl http2;
listen 443 quic reuseport;
add_header Alt-Svc 'h3=":443"; ma=86400';
```

### mTLS (mutual TLS)

Cliente também apresenta certificado — usado em comunicação entre microserviços, APIs B2B:

```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/ssl/server.crt;
    ssl_certificate_key /etc/ssl/server.key;
    ssl_client_certificate /etc/ssl/ca.crt;
    ssl_verify_client on;                     # exige cliente com cert válido

    location / {
        proxy_pass http://backend;
        proxy_set_header X-Client-DN $ssl_client_s_dn;
    }
}
```

---

## Caching

Nginx pode cachear responses do upstream para reduzir carga.

```nginx
http {
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m
                     max_size=1g inactive=60m use_temp_path=off;

    server {
        location /api/ {
            proxy_pass http://backend;
            proxy_cache my_cache;
            proxy_cache_valid 200 302 10m;     # cache 2xx por 10 min
            proxy_cache_valid 404 1m;
            proxy_cache_key "$scheme$request_method$host$request_uri";
            proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
            proxy_cache_background_update on;
            proxy_cache_lock on;
            add_header X-Cache-Status $upstream_cache_status;
        }
    }
}
```

**`X-Cache-Status`** valores:

- `MISS` — não estava no cache
- `HIT` — retornado do cache
- `EXPIRED` — estava expirado
- `STALE` — retornado stale (upstream down)
- `UPDATING` — servindo stale enquanto atualiza
- `BYPASS` — pulou o cache

### Cache key customizado

```nginx
# Ignora query string de tracking
proxy_cache_key "$scheme$host$request_uri$cookie_user";
```

### Respeitar headers do backend

```nginx
proxy_cache_valid 200 1h;
proxy_ignore_headers Cache-Control Expires;    # força TTL definido no Nginx
# OU respeita backend
# (sem ignore, usa Cache-Control do backend)
```

### Static file serving — eficiência máxima

```nginx
location /static/ {
    alias /var/www/static/;
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;

    # Compressão
    gzip_static on;                    # serve .gz pré-comprimido

    # Zero-copy
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
}
```

**`sendfile`** — kernel copia direto do disco para o socket (sem passar pelo userspace). Maximiza throughput.

---

## Compressão

```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;                             # 1-9, tradeoff CPU/size
gzip_min_length 1000;
gzip_types
    text/plain
    text/css
    text/xml
    text/javascript
    application/javascript
    application/json
    application/xml
    application/xml+rss
    image/svg+xml;
```

**Brotli** (mais eficiente que gzip) via módulo `ngx_brotli`:

```nginx
brotli on;
brotli_comp_level 6;
brotli_types text/plain text/css application/json application/javascript;
```

**Regra:** para assets estáticos, pré-comprima no build e sirva com `gzip_static` / `brotli_static` — evita recompressão a cada request.

---

## Rate limiting

Protege backend contra abuse e DDoS.

```nginx
http {
    # Zone — 10MB = ~160k IPs
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            # 10 req/s sustentado, burst de 20 sem delay
            proxy_pass http://backend;
        }

        location /login {
            limit_req zone=login burst=3;
            # 5 req/min, burst de 3 com delay
            proxy_pass http://backend;
        }
    }
}
```

**Parâmetros:**

- **`burst`** — fila de requests extras aceitos
- **`nodelay`** — processa burst imediatamente (senão fica em fila com delay)
- **`delay`** — número de requests antes de começar delay

### Connection limiting

```nginx
limit_conn_zone $binary_remote_addr zone=addr:10m;

server {
    limit_conn addr 10;     # máximo 10 conexões simultâneas por IP
}
```

### Rate limiting por API key

```nginx
map $http_apikey $api_limit_key {
    default $binary_remote_addr;
    "premium-key-123" "";     # sem limite
}

limit_req_zone $api_limit_key zone=api:10m rate=10r/s;
```

---

## Logging

### Access log customizado

```nginx
log_format json escape=json '{'
    '"time_local":"$time_iso8601",'
    '"remote_addr":"$remote_addr",'
    '"remote_user":"$remote_user",'
    '"request":"$request",'
    '"status": $status,'
    '"body_bytes_sent":$body_bytes_sent,'
    '"request_time":$request_time,'
    '"upstream_response_time":"$upstream_response_time",'
    '"upstream_addr":"$upstream_addr",'
    '"http_referer":"$http_referer",'
    '"http_user_agent":"$http_user_agent",'
    '"http_x_forwarded_for":"$http_x_forwarded_for",'
    '"request_id":"$request_id"'
'}';

access_log /var/log/nginx/access.log json;
```

**Logs estruturados em JSON** facilitam ingestão em Elasticsearch, Loki, Datadog.

### Variáveis importantes

- `$request_time` — tempo total desde primeiro byte do request
- `$upstream_response_time` — tempo do upstream (sem Nginx overhead)
- `$upstream_addr` — qual upstream respondeu
- `$upstream_status` — status do upstream
- `$request_id` — ID único (gerado por Nginx)

### Log rotation

```bash
# /etc/logrotate.d/nginx (já vem por default)
/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 nginx adm
    sharedscripts
    postrotate
        if [ -f /var/run/nginx.pid ]; then
            kill -USR1 `cat /var/run/nginx.pid`
        fi
    endscript
}
```

**Nginx-specific:** use `USR1` signal para reabrir logs sem restart.

---

## Variables e redirecionamentos

### Variáveis built-in

| Variable | O que é |
| --- | --- |
| `$host` | Host header |
| `$server_name` | server_name do bloco |
| `$remote_addr` | IP do cliente |
| `$request_uri` | URI completa (com query string) |
| `$uri` | URI normalizada (sem query string) |
| `$query_string` | query string |
| `$args` | alias para $query_string |
| `$arg_foo` | query param "foo" |
| `$http_foo` | request header "Foo" |
| `$sent_http_foo` | response header "Foo" |
| `$cookie_foo` | cookie "foo" |
| `$scheme` | http ou https |
| `$request_method` | GET, POST, ... |
| `$request_id` | ID único gerado |

### Redirects

```nginx
# Temporário (302)
return 302 https://$host$request_uri;

# Permanente (301)
return 301 https://new-domain.com$request_uri;

# Rewrite
rewrite ^/old/(.*)$ /new/$1 permanent;
rewrite ^/api/v1/(.*)$ /v1/$1 break;

# Por path
location /old-path {
    return 301 /new-path;
}
```

**`return` vs `rewrite`:**

- **`return`** é mais simples e rápido. Prefira.
- **`rewrite`** é para quando você precisa manipular a URL internamente.

### Try_files

Pattern para SPAs:

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

Tenta o arquivo, depois o diretório, depois retorna `/index.html` (deixa o client-side router lidar).

---

## Security headers

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

# HSTS — só HTTPS
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

# CSP
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;" always;
```

**`always`** — adiciona header mesmo em responses de erro.

### Limitar request body

```nginx
client_max_body_size 10m;        # default 1m
```

### Timeouts

```nginx
client_body_timeout 10s;
client_header_timeout 10s;
keepalive_timeout 65;
send_timeout 10s;
```

### Esconder versão

```nginx
server_tokens off;               # remove "Server: nginx/1.27.0"
```

### Block user agents maliciosos

```nginx
if ($http_user_agent ~* (bot|crawler|spider)) {
    return 403;
}
```

**Cuidado com `if`:** tem pegadinhas no Nginx. Prefira `map` quando possível.

---

## Nginx em containers

### Docker image oficial

```dockerfile
FROM nginx:1.27-alpine

# Config customizada
COPY nginx.conf /etc/nginx/nginx.conf
COPY site.conf /etc/nginx/conf.d/default.conf

# Static files
COPY build/ /usr/share/nginx/html/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Importante:** `daemon off;` — container precisa ter processo foreground, senão morre imediatamente.

### Multi-stage build para SPA

```dockerfile
# Stage 1: build React
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Nginx sirva
FROM nginx:1.27-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Kubernetes Ingress Controller

`nginx-ingress` é um dos controllers mais usados em K8s. Configuração via annotations:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
    name: myapp
    annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /
        nginx.ingress.kubernetes.io/ssl-redirect: "true"
        nginx.ingress.kubernetes.io/proxy-body-size: "10m"
        nginx.ingress.kubernetes.io/rate-limit-rps: "100"
spec:
    ingressClassName: nginx
    tls:
        - hosts: [app.example.com]
          secretName: app-tls
    rules:
        - host: app.example.com
          http:
              paths:
                  - path: /
                    pathType: Prefix
                    backend:
                        service:
                            name: myapp
                            port:
                                number: 80
```

Ver [[Kubernetes]] (seção Ingress) para detalhes.

---

## Troubleshooting

### Validar config

```bash
sudo nginx -t
sudo nginx -T                    # dump completa (verificar o que está realmente carregado)
```

### Logs

```bash
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u nginx -f
```

### Erros comuns

#### 502 Bad Gateway

- Upstream down
- Upstream respondeu inválido
- Firewall bloqueando conexão do Nginx ao upstream

```bash
# Testar conectividade manualmente
curl -v http://backend-ip:port/
```

#### 504 Gateway Timeout

- Upstream lento demais
- Timeout muito baixo

```nginx
proxy_read_timeout 120s;
```

#### 413 Request Entity Too Large

- Request body maior que `client_max_body_size`

```nginx
client_max_body_size 50m;
```

#### 499 Client Closed Request

- Cliente desistiu antes do upstream responder
- Normal em alguns casos, mas se frequente → upstream lento

#### 500 com "worker_connections are not enough"

- Limite de conexões por worker atingido

```nginx
events {
    worker_connections 4096;     # default 512 ou 1024
}
```

```bash
ulimit -n    # verifique também file descriptors do sistema
```

### Debug request processing

```nginx
error_log /var/log/nginx/error.log debug;    # verboso
```

### stub_status

```nginx
location /nginx_status {
    stub_status;
    allow 127.0.0.1;
    deny all;
}
```

```
Active connections: 291
server accepts handled requests
 16630948 16630948 31070465
Reading: 6 Writing: 179 Waiting: 106
```

**Para métricas Prometheus:** nginx-prometheus-exporter.

---

## Patterns de produção

### 1. Always `nginx -t` before reload

```bash
sudo nginx -t && sudo systemctl reload nginx
```

### 2. Graceful reload

`nginx -s reload` não derruba conexões — SIGHUP mantém workers antigos até finalizarem.

### 3. Config em múltiplos arquivos

```
/etc/nginx/
├── nginx.conf          # main
├── conf.d/
│   └── default.conf    # http-level includes
└── sites-enabled/
    ├── example.com
    └── api.example.com
```

### 4. Gerenciamento via Git + CI

Config em repo, CI valida (`nginx -t`), deploy via Ansible/Puppet/Terraform.

### 5. Logs em JSON

Facilita ingestão em Elasticsearch, Datadog, Loki.

### 6. `request_id` propagado

```nginx
proxy_set_header X-Request-ID $request_id;
```

Backend loga com esse ID, facilita trace distribuído.

### 7. Monitoring

- **stub_status** para métricas básicas
- **nginx-prometheus-exporter** para Prometheus
- **Datadog agent** com Nginx integration
- Alertas em 5xx rate, latência, upstream errors

### 8. Zero-downtime config changes

- Sempre valide antes (`nginx -t`)
- `nginx -s reload` (SIGHUP) não interrompe conexões ativas
- Para upgrade do binário: `nginx -s USR2` (novo master + workers)

---

## Armadilhas comuns

- **Esquecer `proxy_set_header Host`** — backend recebe `Host: backend-ip`
- **Não passar `X-Forwarded-*`** — backend vê localhost
- **`proxy_read_timeout` muito baixo** — 504 em requests lentas
- **`client_max_body_size` default (1m)** — upload fail silencioso com 413
- **`return` vs `rewrite` confundidos** — rewrite infinito
- **`if` dentro de `location`** — comportamento inesperado, prefira `map`
- **Reload sem `nginx -t`** — config quebrada derruba servidor
- **Não usar `gzip_static`** — recomprimindo a cada request
- **Logs sem rotate** — disco cheio
- **`worker_connections` muito baixo** — 503 sob carga
- **SSL com ciphers fracos ou protocolos antigos** — falha em SSL Labs
- **Não redirecionar HTTP → HTTPS** — tráfego inseguro
- **`server_tokens on`** — vaza versão, ajuda atacantes
- **Regex greedy em location** — lento
- **`try_files` errado em SPA** — 404 em refresh
- **Buffering ligado em streams** — SSE, downloads grandes travam
- **Cache sem purge** — conteúdo velho servido
- **ip_hash com CDN na frente** — todos os requests vêm do IP da CDN
- **Não usar keepalive em upstream** — TCP handshake em cada request
- **Healthcheck agressivo demais** — sobrecarga no backend
- **Timeouts default** — 60s, pode ser lento demais
- **Error log em `debug`** em produção — disco cheio rápido
- **`access_log off`** em tudo — perde visibilidade
- **Location block sem `/` final** — matches inesperados
- **Reescrever URL sem entender matching order** — loops

---

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
- [Nginx Cookbook](https://www.nginx.com/resources/library/complete-nginx-cookbook/) — patterns práticos
- [Nginx Admin Guide](https://docs.nginx.com/nginx/admin-guide/)

### Livros

- **Nginx Cookbook** — Derek DeJonghe (O'Reilly, gratuito via Nginx)
- **Nginx HTTP Server** — Clément Nedelcu

### Ferramentas

- [nginx.conf generator (DigitalOcean)](https://www.digitalocean.com/community/tools/nginx)
- [Nginx Playground](https://nginx-playground.wizardzines.com/) — Julia Evans
- [SSL Labs Test](https://www.ssllabs.com/ssltest/) — testa TLS config
- [nginx-prometheus-exporter](https://github.com/nginxinc/nginx-prometheus-exporter)
- [GoAccess](https://goaccess.io/) — analyze access logs em tempo real

### Alternativas modernas

- **Caddy** — config mais simples, HTTPS automático, mas menos flexível
- **Traefik** — cloud-native, K8s ingress popular, service discovery nativo
- **Envoy** — service mesh (Istio, Linkerd), observability top-tier
- **HAProxy** — load balancer clássico, mais focado em TCP/L4

---

## Veja também

- [[Linux]] — fundação
- [[Docker]] — Nginx em containers
- [[Kubernetes]] — nginx-ingress controller
- [[Redes e Protocolos]] — HTTP, TLS, HTTP/2
- [[API Design]] — rate limiting, caching
- [[System Design]] — load balancing em arquitetura
- [[CI-CD]] — deploy de config Nginx
- [[Observabilidade]] — Nginx metrics e logs
