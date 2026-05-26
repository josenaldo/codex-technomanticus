---
title: "Redes e Protocolos"
created: 2026-04-01
updated: 2026-04-09
type: concept
status: evergreen
tags:
  - fundamentos
  - entrevista
publish: false
---

# Redes e Protocolos

Fundamentos de comunicação entre sistemas — do modelo OSI ao HTTP/3, de DNS a gRPC. Para um senior fullstack, os protocolos de aplicação (HTTP, WebSocket, gRPC) são o dia a dia, mas entender as camadas inferiores (TCP/UDP, DNS, TLS) é o que permite **debugar**, **projetar** e **defender decisões** em system design.

## O que é

Uma rede de computadores é um conjunto de máquinas que se comunicam seguindo **protocolos** — regras padronizadas que definem formato de mensagem, endereçamento, controle de erros e fluxo. A internet é uma rede de redes, e o stack TCP/IP é o que faz tudo funcionar.

Em entrevistas, networking aparece de duas formas:

1. **System design** — "como você projetaria este sistema?" exige saber latência, throughput, DNS, load balancing, CDNs, caching, protocolos
2. **Debugging** — "por que está lento?" exige rastrear camadas: DNS? TLS handshake? TCP slow start? payload grande? N+1 de chamadas?

---

## Modelo de camadas

### OSI (7 camadas) vs TCP/IP (4 camadas)

Na prática e em entrevistas, o modelo TCP/IP com detalhe de 5 camadas é o mais útil:

| # | Camada | Protocolos | O que faz | O que importa pro dev |
| --- | --- | --- | --- | --- |
| 7/6/5 | Aplicação | HTTP, gRPC, WebSocket, DNS, SMTP, FTP | Interface com o usuário/aplicação | APIs, REST, GraphQL, headers |
| 4 | Transporte | TCP, UDP, QUIC | Entrega de dados entre processos | Portas, confiabilidade, flow control |
| 3 | Rede | IP, ICMP | Roteamento entre redes | Endereçamento IP, subnets, routing |
| 2 | Enlace | Ethernet, Wi-Fi, ARP | Entrega dentro de uma rede local | MAC address, frames, switches |
| 1 | Física | Cabos, sinais | Bits no meio físico | Raramente relevante para software |

> **Para entrevistas:** você precisa entender profundamente as camadas 4 (TCP/UDP) e 7 (HTTP). Camadas 1-3 são "bom saber" para system design (routing, BGP, subnets aparecem em escala grande).

---

## TCP (Transmission Control Protocol)

Protocolo de transporte **confiável**, **ordenado** e **com controle de fluxo**. Base do HTTP, bancos de dados, email, SSH.

### Three-way handshake

```
Cliente → SYN →         Servidor
Cliente ← SYN-ACK ←     Servidor
Cliente → ACK →          Servidor
```

Estabelece uma conexão antes de enviar dados. **Custo:** 1 RTT (round-trip time) extra antes do primeiro byte de dados. Em conexões novas cross-continent (~100ms RTT), isso é perceptível.

### Garantias

- **Entrega confiável** — retransmite pacotes perdidos (acknowledgments + timeouts)
- **Ordenação** — pacotes chegam na ordem correta (sequence numbers)
- **Controle de fluxo** — receptor informa quanto consegue processar (sliding window)
- **Controle de congestionamento** — TCP começa devagar (slow start) e acelera progressivamente; reduz a taxa ao detectar perda

### Slow start e implicações

Conexões TCP novas começam com **janela pequena** (~14KB) e dobram a cada RTT até atingir um limiar. Isso significa que **a primeira request** em uma conexão nova é naturalmente mais lenta. Soluções:

- **Keep-alive / connection pooling** — reutilizar conexões já "aquecidas"
- **HTTP/2 multiplexing** — uma só conexão para múltiplas requests
- **HTTP/3 QUIC** — elimina head-of-line blocking do TCP

### TCP connection termination (4-way)

```
FIN → ACK ← FIN → ACK ←
```

Conexão fica em estado `TIME_WAIT` por ~2 minutos (evita pacotes atrasados da conexão anterior). Em servidores de alta concorrência, pode esgotar portas efêmeras se não usar connection pooling.

---

## UDP (User Datagram Protocol)

**Sem garantias**: sem handshake, sem ordem, sem confirmação, sem controle de congestionamento. Cada datagrama é independente.

**Vantagens:** latência mínima (sem RTT de handshake), overhead baixo (header de 8 bytes vs 20+ do TCP).

**Usado em:**

- **DNS** — queries curtas, resposta rápida
- **Streaming de vídeo/áudio** — perder um frame é aceitável; atraso não é
- **Jogos online** — posição do jogador precisa ser fresh, não retransmitida
- **VoIP** — preferível perder uma sílaba a ter delay
- **QUIC/HTTP/3** — confiabilidade implementada **sobre** UDP, em nível de aplicação

### Quando escolher TCP vs UDP

| Critério | TCP | UDP |
| --- | --- | --- |
| Dados íntegros e ordenados obrigatórios | ✅ | ❌ |
| Tolerância a perda de pacotes | ❌ | ✅ |
| Latência mínima é prioridade | ❌ | ✅ |
| Precisa de multiplexing custom | ❌ | ✅ (QUIC) |

---

## DNS (Domain Name System)

O "catálogo telefônico" da internet. Traduz nomes legíveis (`api.example.com`) em endereços IP (`93.184.216.34`).

### Hierarquia de resolução

```
Browser cache → OS cache → Resolver (ISP) → Root NS → TLD NS (.com) → Authoritative NS (example.com)
```

Cada nível pode cachear. O **TTL** (Time To Live) do registro define por quanto tempo o cache é válido.

### Tipos de registro

| Registro | O que faz | Exemplo |
| --- | --- | --- |
| **A** | Nome → IPv4 | `api.example.com → 93.184.216.34` |
| **AAAA** | Nome → IPv6 | `api.example.com → 2606:2800:...` |
| **CNAME** | Alias (aponta para outro nome) | `www → example.com` |
| **MX** | Mail server | Email routing |
| **NS** | Name server autoritativo | Delegação de zona |
| **TXT** | Texto livre | SPF, DKIM, verificação de domínio |
| **SRV** | Serviço + porta | Service discovery |
| **CAA** | Certificate Authority Authorization | Segurança de certificados |

### DNS e latência

Uma query DNS não-cached pode levar **50-200ms** (múltiplos hops). Mitigações:

- **Prefetch DNS** — `<link rel="dns-prefetch" href="//api.example.com">`
- **TTL adequado** — muito curto = muitas resoluções; muito longo = lentidão pra mudar
- **DNS caching local** — resolvers como `dnsmasq`, `unbound`
- **Anycast DNS** — múltiplos servidores com o mesmo IP; a rede roteia para o mais próximo

### DNS em system design

- **Failover** — mudar DNS para apontar para backup (lento — respeita TTL)
- **Global load balancing** — DNS retorna IPs diferentes por região (GeoDNS)
- **Service discovery** — Consul, CoreDNS, AWS Route 53 com health checks
- **DNS Round Robin** — retorna múltiplos IPs; cliente escolhe um (balanceamento primitivo)

---

## TLS (Transport Layer Security)

Criptografia em trânsito. HTTP + TLS = HTTPS. Protege contra espionagem (eavesdropping), adulteração (tampering) e falsificação (impersonation).

### TLS handshake (simplificado)

```
Cliente → ClientHello (versão TLS, cipher suites)
Servidor → ServerHello + Certificado
Cliente verifica certificado (cadeia de confiança até CA raiz)
Troca de chaves (Diffie-Hellman ou RSA)
Ambos derivam chave simétrica → tráfego criptografado
```

**Custo:** 1-2 RTTs extras por conexão nova. **TLS 1.3** reduziu para 1 RTT (e suporta 0-RTT para reconexões).

### Conceitos chave

- **Certificado digital** — prova a identidade do servidor. Emitido por CA (Certificate Authority). Let's Encrypt automatizou isso.
- **Cipher suite** — combinação de algoritmos: troca de chaves + criptografia simétrica + hash. Ex.: `TLS_AES_256_GCM_SHA384`.
- **mTLS (mutual TLS)** — **ambos** os lados apresentam certificado. Usado em comunicação entre microserviços (service mesh, Istio).
- **Certificate pinning** — cliente só aceita certificados específicos (evita MitM mesmo com CA comprometida).
- **HSTS** — header que instrui o browser a sempre usar HTTPS. Previne downgrade para HTTP.

### TLS em entrevistas

Saber que "HTTPS criptografa tudo" não basta. Saiba explicar: quem emite o certificado, o que o cliente verifica, por que a troca de chaves usa Diffie-Hellman, o que significa forward secrecy (comprometer a chave de hoje não decifra tráfego de ontem).

---

## HTTP em profundidade

### Anatomia de uma request HTTP

```
GET /api/medicos?especialidade=cardio HTTP/1.1
Host: api.medespecialista.com
Authorization: Bearer eyJhbG...
Accept: application/json
Cache-Control: no-cache
```

### Anatomia de uma response

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Cache-Control: max-age=300
ETag: "abc123"
X-Request-Id: uuid-here

{"data": [...]}
```

### Métodos HTTP

| Método | Idempotente | Safe | Uso |
| --- | --- | --- | --- |
| GET | sim | sim | Ler recurso |
| POST | **não** | não | Criar recurso, ações |
| PUT | sim | não | Substituir recurso inteiro |
| PATCH | **não** (na prática) | não | Atualizar parcialmente |
| DELETE | sim | não | Remover recurso |
| HEAD | sim | sim | Metadados (como GET sem body) |
| OPTIONS | sim | sim | CORS preflight, capabilities |

**Idempotente** = chamar N vezes produz o mesmo resultado que chamar 1 vez. Crítico para retries.

### Status codes que todo dev precisa saber

| Range | Significado | Exemplos |
| --- | --- | --- |
| 2xx | Sucesso | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirecionamento | 301 Moved Permanently, 304 Not Modified |
| 4xx | Erro do cliente | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Entity, 429 Too Many Requests |
| 5xx | Erro do servidor | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout |

**Diferença 401 vs 403:** 401 = "não sei quem você é" (autenticação); 403 = "sei quem você é, mas não tem permissão" (autorização).

### HTTP/1.1 → HTTP/2 → HTTP/3

| Aspecto | HTTP/1.1 | HTTP/2 | HTTP/3 |
| --- | --- | --- | --- |
| Transporte | TCP | TCP | **QUIC (UDP)** |
| Formato | texto | **binário** | binário |
| Multiplexing | não (1 req/conexão ou pipelining limitado) | **sim** (streams) | sim |
| Compressão de headers | não | **HPACK** | QPACK |
| Head-of-line blocking | sim (TCP) | parcial (TCP ainda bloqueia) | **não** (streams independentes) |
| Server push | não | sim (pouco usado) | sim |
| Handshake | TCP + TLS = 2-3 RTTs | TCP + TLS = 2-3 RTTs | **1 RTT** (0-RTT em reconexão) |

**Na prática:** HTTP/2 é o padrão em 2026 para APIs. HTTP/3 está crescendo, especialmente em CDNs (Cloudflare, Google). Para o desenvolvedor backend, a diferença é transparente — o web server / load balancer cuida da negociação de protocolo.

### Caching HTTP

Mecanismo poderoso para reduzir latência e carga no backend. Controlado por headers:

- **`Cache-Control`** — `max-age=300` (5 min), `no-cache` (revalida sempre), `no-store` (nunca cacheia), `private` (só browser), `public` (CDN pode cachear)
- **`ETag`** — hash do conteúdo. Cliente manda `If-None-Match: "abc123"` → servidor retorna 304 se não mudou
- **`Last-Modified`** / **`If-Modified-Since`** — baseado em data
- **`Vary`** — indica quais headers do request afetam o cache. Ex.: `Vary: Accept-Encoding` diferencia respostas gzip vs brotli

**Layers de cache:**

```
Browser → CDN → Reverse proxy (Nginx) → Application cache (Redis) → Database
```

### CORS (Cross-Origin Resource Sharing)

Mecanismo do **browser** que restringe requests de um domínio para outro. O servidor controla via headers:

```
Access-Control-Allow-Origin: https://frontend.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 86400
```

**Preflight:** para requests "complexos" (não GET/POST simples), o browser envia OPTIONS antes. Otimize com `Access-Control-Max-Age` para cachear o preflight.

> **CORS não é segurança do servidor.** É proteção do browser contra scripts maliciosos. Qualquer `curl` ou backend bypassa completamente.

---

## REST, GraphQL e gRPC

### REST (Representational State Transfer)

Estilo arquitetural (não protocolo) baseado em recursos identificados por URLs, operados por métodos HTTP.

**Princípios:**

- **Stateless** — cada request contém toda informação necessária
- **Recursos** — URIs identificam entidades (`/api/medicos/42`)
- **Representações** — JSON, XML, etc.
- **HATEOAS** — respostas incluem links para ações possíveis (na teoria; raramente implementado em pureza)
- **Cacheable** — respostas podem ser cacheadas via headers HTTP

**Richardson Maturity Model:**

| Nível | O que usa |
| --- | --- |
| 0 | Um endpoint, POST pra tudo (RPC sobre HTTP) |
| 1 | Recursos com URIs distintas |
| 2 | Métodos HTTP corretos (GET, POST, PUT, DELETE) + status codes |
| 3 | HATEOAS (links de navegação na resposta) |

A maioria das APIs em produção está no nível 2, e tá ótimo.

### GraphQL

Linguagem de query para APIs. O cliente **declara exatamente** quais campos quer.

```graphql
query {
  medico(id: 42) {
    nome
    especialidade
    avaliacoes(limit: 5) {
      nota
      comentario
    }
  }
}
```

**Vantagens:**

- Elimina over-fetching (trazer dados desnecessários) e under-fetching (precisar de múltiplas requests)
- Um único endpoint
- Schema fortemente tipado, auto-documentado (introspecção)
- Ideal quando **clientes diferentes** precisam de **dados diferentes** (mobile vs web vs smartwatch)

**Desvantagens:**

- Caching mais complexo (não usa HTTP caching naturalmente — tudo é POST)
- N+1 no resolver se não usar DataLoader
- Query complexa pode ser cara — precisa de rate limiting por complexidade
- Observabilidade mais difícil (todas as requests vão pro mesmo endpoint)
- Overkill para CRUD simples ou APIs internas

### gRPC

Framework RPC usando Protocol Buffers (serialização binária) sobre HTTP/2.

```protobuf
service MedicoService {
  rpc GetMedico(MedicoRequest) returns (MedicoResponse);
  rpc ListMedicos(ListRequest) returns (stream MedicoResponse); // streaming
}
```

**Vantagens:**

- **Muito rápido** — protobuf é 3-10x menor que JSON, serialização/deserialização mais rápida
- **Contrato forte** — `.proto` files geram código em qualquer linguagem
- **Streaming** — unidirecional, bidirecional
- **HTTP/2 nativo** — multiplexing

**Desvantagens:**

- Não funciona nativamente em browsers (precisa de gRPC-Web proxy)
- Debugging mais difícil (binário, não legível)
- Tooling menos maduro que REST para APIs públicas

### Quando escolher

| Cenário | Escolha | Por quê |
| --- | --- | --- |
| API pública, CRUD | REST | Universal, cacheável, tooling maduro |
| Clientes com necessidades variadas | GraphQL | Flexibilidade de query, schema tipado |
| Microserviços internos, alta perf | gRPC | Velocidade, contrato forte, streaming |
| Comunicação assíncrona | Mensageria (Kafka, RabbitMQ) | Desacoplamento, resiliência |
| Push do servidor → cliente | SSE ou WebSocket | Tempo real |

---

## WebSocket e SSE

### WebSocket

Conexão **bidirecional persistente** sobre TCP. Handshake HTTP → Upgrade → comunicação full-duplex.

```
GET /chat HTTP/1.1
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==

HTTP/1.1 101 Switching Protocols
Upgrade: websocket
```

**Uso:** chat, collaborative editing, gaming, notificações bidirecionais, dashboards live.

**Considerações:**

- Mantém conexão TCP aberta por cliente — escala diferente de REST (stateful)
- Load balancing com "sticky sessions" ou usar pub/sub externo (Redis)
- Reconexão precisa ser implementada pelo cliente
- Não funciona bem com CDNs e proxies que não suportam WebSocket

### SSE (Server-Sent Events)

**Unidirecional**: servidor → cliente. Usa HTTP normal (GET com `text/event-stream`). Reconexão automática.

```
data: {"type": "update", "value": 42}
id: 123
retry: 5000

data: {"type": "heartbeat"}
```

**Vantagens sobre WebSocket:**

- Funciona com HTTP/2 (multiplexado com outras requests)
- Reconexão automática com `Last-Event-ID`
- Passa por CDNs e proxies sem configuração extra
- Mais simples de implementar e debugar

**Use SSE quando:** push unidirecional é suficiente (feeds, dashboards, progresso de tarefas, notificações).

**Use WebSocket quando:** comunicação bidirecional é necessária (chat, gaming, collaborative editing).

---

## Load Balancing

Distribui tráfego entre múltiplas instâncias de um serviço.

### Camadas

- **L4 (transporte):** roteia por IP/porta. Rápido, simples. Ex.: AWS NLB, HAProxy (modo TCP).
- **L7 (aplicação):** inspeciona HTTP (path, headers, cookies). Permite routing inteligente. Ex.: Nginx, AWS ALB, Envoy.

### Algoritmos

| Algoritmo | Comportamento | Quando usar |
| --- | --- | --- |
| Round Robin | distribui sequencialmente | servidores homogêneos |
| Least Connections | manda pro que tem menos conexões ativas | cargas desiguais |
| IP Hash | mesma origem → mesmo servidor | sessões sticky |
| Weighted | peso por capacidade do servidor | servidores heterogêneos |
| Random | aleatório | surpreendentemente eficaz em larga escala |

### Health checks

O load balancer verifica periodicamente se as instâncias estão saudáveis. Tipos:

- **TCP** — consegue conectar na porta?
- **HTTP** — `GET /health` retorna 200?
- **Deep** — verifica dependências (banco, cache)

Instância que falha health check é removida do pool.

### Session affinity (sticky sessions)

Requests do mesmo cliente sempre vão para a mesma instância. **Evite quando possível** — dificulta scaling e failover. Prefira sessão externalizada (Redis, JWT stateless).

---

## CDN (Content Delivery Network)

Rede de servidores distribuídos geograficamente que cacheia conteúdo próximo ao usuário. Reduz latência, aumenta throughput, absorve picos de tráfego.

**Exemplos:** Cloudflare, AWS CloudFront, Fastly, Akamai.

**O que cacheia:**

- Assets estáticos (JS, CSS, imagens, fontes) — sempre
- Respostas de API — quando os headers de cache permitem
- Conteúdo dinâmico na edge (edge computing) — Cloudflare Workers, Vercel Edge Functions

**Headers importantes:**

- `Cache-Control: public, max-age=31536000` — CDN pode cachear por 1 ano (assets com hash no nome)
- `Cache-Control: private` — só browser, não CDN
- `Vary: Accept-Encoding` — CDN mantém versões gzip e brotli

**Cache invalidation** é o problema mais difícil. Estratégias:

- **Cache busting** — nome do arquivo inclui hash (`app.a1b2c3.js`)
- **Purge** — API da CDN para invalidar path específico
- **TTL curto + stale-while-revalidate** — serve do cache enquanto revalida em background

---

## Conceitos para System Design

### Latência e throughput

- **Latência** — tempo entre enviar request e receber resposta (medida em ms)
- **Throughput** — volume de requests por segundo (RPS) ou dados por segundo (Mbps)
- **Bandwidth** — capacidade máxima do canal (não = throughput real)

**Números de latência que todo senior deve ter como referência:**

| Operação | Latência |
| --- | --- |
| L1 cache | ~1 ns |
| L2 cache | ~5 ns |
| RAM | ~100 ns |
| SSD random read | ~100 μs |
| HDD random read | ~10 ms |
| Rede local (data center) | ~0.5 ms |
| Rede entre regiões | ~30-100 ms |
| Rede intercontinental | ~100-300 ms |

> Esses números justificam por que caching importa, por que bancos locais são mais rápidos que remotos, e por que CDNs existem.

### Connection pooling

Criar conexão TCP + TLS é caro. Connection pool mantém conexões abertas e reutiliza. Essencial para: banco de dados (HikariCP, PgBouncer), HTTP clients (OkHttp pool), Redis.

**Dimensionamento:** pool pequeno demais = requests esperando conexão; grande demais = banco sobrecarregado. HikariCP recomenda `pool_size = cores * 2 + 1` como ponto de partida.

### Rate limiting

Limitar quantas requests um cliente pode fazer em um período. Protege contra abuse e garante fairness.

**Algoritmos:**

- **Token bucket** — tokens regeneram a uma taxa fixa; cada request consome um
- **Sliding window** — conta requests em janela deslizante
- **Fixed window** — conta por janela fixa (simples, mas permite burst na fronteira)

**Implementação:** Redis (`INCR` + `EXPIRE`), Nginx, API Gateway.

### Retries e backoff

Requests falham. **Retry** resolve falhas transientes, mas retry ingênuo pode derrubar o servidor em cascata.

- **Exponential backoff** — 1s → 2s → 4s → 8s → max
- **Jitter** — adiciona aleatoriedade ao backoff para evitar thundering herd (todos retrying no mesmo instante)
- **Circuit breaker** — após N falhas consecutivas, para de tentar por um tempo (Resilience4j, Hystrix)

### Timeout

Toda chamada de rede precisa de timeout. Sem timeout = thread/conexão presa para sempre se o servidor travar.

- **Connection timeout** — quanto tempo esperar para estabelecer conexão (rápido, ~1-5s)
- **Read/response timeout** — quanto tempo esperar pela resposta (depende do serviço, ~5-30s)
- **Request timeout** — tempo total ponta-a-ponta

---

## Armadilhas comuns

- **Ignorar latência de rede** — em system design, a rede é sempre gargalo. Minimize round-trips. Batch quando possível.
- **DNS mal configurado** — TTL muito baixo = muitas resoluções; muito alto = lento para failover.
- **Não entender CORS** — é proteção do browser, não do servidor. Qualquer `curl` bypassa.
- **Confundir REST com HTTP** — REST é estilo arquitetural. Nem toda API HTTP é REST.
- **WebSocket para tudo** — se só precisa push do servidor, SSE é mais simples.
- **Não usar connection pooling** — criar conexão por request é desperdício de CPU e latência.
- **Timeouts ausentes** — chamada de rede sem timeout trava threads e esgota pools.
- **Retry sem backoff** — amplifica falhas em cascata.
- **Ignorar TLS overhead** — em HTTP/1.1, cada request nova paga handshake. Use keep-alive ou HTTP/2.
- **Serializar muito dado** — JSON de 10MB na response. Use paginação, streaming ou compressão.
- **Não comprimir** — habilite gzip/brotli no servidor e CDN. JSON comprime muito bem (60-90% de redução).
- **Sticky sessions como default** — dificulta escalabilidade. Externalize sessão.
- **Cachear sem estratégia de invalidação** — "there are only two hard things in CS: cache invalidation and naming things."
- **HEAD-of-line blocking sem saber** — HTTP/1.1 com muitas requests paralelas ao mesmo domínio. HTTP/2 resolve.
- **Assumir rede confiável** — em sistema distribuído, a rede **vai** falhar. Design for failure.

---

## Na prática (da minha experiência)

> No MedEspecialista, a arquitetura de comunicação segue um padrão: **REST para API pública** (mobile e web consomem), **Kafka para comunicação assíncrona entre serviços** (agendamento → notificação → faturamento), e consideramos gRPC para chamadas síncronas internas quando migramos pra microserviços.
>
> **Um caso real de debugging de latência:** um endpoint estava levando ~1.5s para responder. O `EXPLAIN ANALYZE` do banco mostrava 20ms. O problema era que a aplicação fazia 3 chamadas HTTP síncronas sequenciais a um serviço externo durante a request: DNS (não cacheado) + TLS handshake + response. Solução: paralelizar com `CompletableFuture`, cachear respostas com TTL curto no Redis, e cachear DNS localmente. Caiu pra 200ms.
>
> **Sobre CORS:** já perdi horas debugando "por que meu POST funciona no Postman mas não no browser?" até entender que CORS é mecanismo do browser. A request nem chega ao servidor se o preflight falha. Configuro `Access-Control-Max-Age: 86400` para cachear preflight por 24h.
>
> **Sobre caching:** no endpoint de listagem de especialidades médicas (dados que mudam uma vez por mês), adicionei `Cache-Control: public, max-age=3600` + ETag. O CDN passou a servir diretamente, e o endpoint praticamente sumiu dos logs do backend. Zero linha de código de cache aplicacional.
>
> **Sobre WebSocket vs SSE:** no dashboard de monitoramento de agendamentos, comecei com WebSocket porque "preciso de tempo real". Depois percebi que o fluxo era unidirecional (servidor → dashboard). Migrei pra SSE — código mais simples, reconexão automática, funciona com o load balancer existente sem configuração extra.

---

## How to explain in English

> "Networking is something I deal with daily as a fullstack developer, even if most of the time the framework abstracts it away. When I'm designing APIs, I default to REST over HTTP — it's well-understood, cacheable, and has excellent tooling. For internal microservice communication where latency matters, I evaluate gRPC because Protocol Buffers are much more compact than JSON and HTTP/2 multiplexing reduces overhead significantly.
>
> One area where networking knowledge really pays off is debugging latency issues. When an endpoint is slow, I trace through the layers: is it DNS resolution? TLS handshake on a new connection? TCP slow start? The application itself? Or is it making sequential HTTP calls to external services when it could parallelize them? I had exactly that situation — a 1.5-second endpoint turned out to be three sequential external calls. Parallelizing them and adding a short-lived Redis cache brought it down to 200 milliseconds.
>
> For caching, I rely heavily on HTTP cache semantics — `Cache-Control`, `ETag`, `Vary`. For data that changes rarely, like a list of medical specialties, setting proper cache headers means the CDN serves the response directly without ever hitting my backend. That's the cheapest performance win you can get.
>
> On real-time communication: I used to default to WebSocket, but I've learned that Server-Sent Events are simpler and sufficient when the flow is server-to-client only. SSE works with HTTP/2, reconnects automatically, and doesn't require special load balancer configuration. I reserve WebSocket for truly bidirectional use cases like chat."

### Frases úteis em entrevista

- "The bottleneck is network latency, not compute — let's minimize round-trips."
- "I'd put a CDN in front of this to serve static assets and cacheable API responses from the edge."
- "We should use connection pooling here to avoid paying the TCP + TLS handshake on every request."
- "I'd add exponential backoff with jitter to these retries to avoid thundering herd."
- "This is a good candidate for SSE rather than WebSocket — the communication is server-to-client only."
- "REST for the public API, gRPC internally between services where we need the performance."
- "Let me check if the DNS TTL is reasonable — too low means unnecessary resolution overhead."
- "We need a circuit breaker on this external call so a downstream failure doesn't cascade."

### Key vocabulary

- camada de aplicação → application layer
- camada de transporte → transport layer
- handshake de três vias → three-way handshake (SYN-SYN/ACK-ACK)
- resolução de nomes → name resolution (DNS)
- latência → latency
- throughput → throughput
- largura de banda → bandwidth
- ida e volta → round-trip time (RTT)
- balanceamento de carga → load balancing
- proxy reverso → reverse proxy
- rede de distribuição de conteúdo → content delivery network (CDN)
- conexão persistente → persistent connection / keep-alive
- pool de conexões → connection pool
- certificado digital → digital certificate
- criptografia em trânsito → encryption in transit
- autenticação mútua → mutual TLS (mTLS)
- limitação de taxa → rate limiting
- disjuntor → circuit breaker
- backoff exponencial → exponential backoff
- jitter → jitter (aleatoriedade no retry)
- cabeçalho → header
- idempotente → idempotent
- estado da arte → state of the art
- comunicação bidirecional → bidirectional communication
- eventos enviados pelo servidor → server-sent events (SSE)
- cabeçalho de cache → cache header
- invalidação de cache → cache invalidation

---

## Recursos

### Livros

- *High Performance Browser Networking* — Ilya Grigorik ([hpbn.co](https://hpbn.co/), gratuito — o melhor sobre networking para devs web)
- *Computer Networking: A Top-Down Approach* — Kurose & Ross (textbook clássico)
- *Designing Data-Intensive Applications* — Martin Kleppmann (capítulos sobre rede e consistência)

### Online

- [HTTP/2 explained](https://http2-explained.haxx.se/) — guia visual de Daniel Stenberg (autor do curl)
- [HTTP/3 explained](https://http3-explained.haxx.se/) — continuação
- [How DNS Works](https://howdns.works/) — comic interativo
- [Latency Numbers Every Programmer Should Know](https://gist.github.com/jboner/2841832)
- [Mozilla MDN — HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) — referência canônica
- [gRPC docs](https://grpc.io/docs/) — documentação oficial

## Veja também

- [[API Design]]
- [[System Design]]
- [[03-Dominios/Java/Backend/Kafka/Kafka]]
- [[Arquitetura de Software]]
- [[Banco de dados]] — connection pooling, replicação
