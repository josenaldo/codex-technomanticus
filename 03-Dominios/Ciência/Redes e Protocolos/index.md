---
title: "Redes e Protocolos"
created: 2026-06-18
updated: 2026-06-18
type: moc
status: growing
publish: true
tags:
  - ciencia-da-computacao
  - redes
  - protocolos
  - http
  - entrevista
  - moc
aliases:
  - Redes e Protocolos
  - Redes
  - Redes de Computadores
  - Networking
  - Galho - Redes e Protocolos
---

# Redes e Protocolos

> [!abstract] TL;DR
> Galho de Ciência da Computação sobre como sistemas conversam — do **modelo de camadas** e **TCP/UDP/DNS/TLS** até **HTTP** (métodos, status, caching, CORS, HTTP/2-3), os **protocolos de aplicação** (REST/GraphQL/gRPC, WebSocket/SSE) e a **engenharia de comunicação em escala** (latência, load balancing, CDN, resiliência). Para um senior, a rede é onde nascem os gargalos invisíveis: saber rastrear as camadas é o que separa "está lento" de "está lento *porque*". Interview-critical.

## Sobre este galho

Networking aparece em entrevista de duas formas: **system design** ("como você projetaria isso?" exige latência, DNS, load balancing, CDN, protocolos) e **debugging** ("por que está lento?" exige rastrear camadas: DNS? TLS? slow start? N+1 de chamadas?). Este galho cobre as duas faces, do bit ao byte de aplicação.

**Fronteiras (linka, não duplica):**
- **Design de API** (modelagem de recurso, versionamento, paginação, HATEOAS, Richardson) → [[API Design]]. Aqui REST/GraphQL/gRPC são tratados **como protocolo** (transporte, serialização, streaming).
- **Escala e composição de sistema** → [[System Design]]. Load balancing, CDN, números de latência e resiliência são fundamento de rede aqui e **forward-linkam** pra lá.
- **Comunicação assíncrona** → [[Mensageria]] / [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka|Kafka]]. A nota de REST/gRPC menciona mensageria como alternativa síncrona × assíncrona e linka.
- **Primitivas criptográficas** (Diffie-Hellman, hashing, PKI a fundo) → galho futuro de Segurança Conceitual. A nota de TLS trata o **protocolo**; a cripto interna fica mencionada em prosa.
- **Java/produção** (OkHttp, Resilience4j, HikariCP) → [[Spring Boot]]. **Operar o stack** (Nginx, Linux, K8s) → [[03-Dominios/Tecnologia/Infraestrutura/Linux|Linux]] / [[Nginx]].

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista" com frases prontas em inglês e vocabulário técnico PT→EN.

## Iniciado — as camadas e o transporte

1. [[01 - O que é uma rede e o modelo de camadas]] — protocolos, OSI × TCP/IP, encapsulamento, IP/portas/NAT, as duas faces em entrevista.
2. [[02 - TCP]] — 3-way handshake, garantias, sliding window, slow start, TIME_WAIT.
3. [[03 - UDP]] — sem garantias, casos de uso, TCP × UDP, confiabilidade-sobre-UDP e QUIC.
4. [[04 - DNS]] — hierarquia de resolução, tipos de registro, TTL/cache, GeoDNS/anycast.

## Adepto — TLS, HTTP e os protocolos de aplicação

5. [[05 - TLS e HTTPS]] — handshake, certificados/CA, cipher suites, mTLS, HSTS, forward secrecy, TLS 1.3.
6. [[06 - HTTP - métodos, status e headers]] — idempotência/safe, anatomia req/resp, 401 × 403, status, headers.
7. [[07 - A evolução do HTTP]] — 1.1 → 2 → 3: binário, multiplexing, HOL blocking, HPACK/QPACK, QUIC.
8. [[08 - Caching HTTP]] — Cache-Control, ETag/condicional, Vary, camadas, stale-while-revalidate.
9. [[09 - CORS e a same-origin policy]] — preflight, headers, Max-Age, "não é segurança do servidor".
10. [[10 - REST, GraphQL e gRPC]] — comparação de protocolo + quando escolher; linka API Design.
11. [[11 - WebSocket e SSE]] — bidirecional × unidirecional, quando escolher, LB e reconexão.

## Magus — latência, escala e resiliência

12. [[12 - Latência, throughput e os números]] — latência × throughput × bandwidth, a tabela de números, RTT.
13. [[13 - Load balancing e CDN]] — L4 × L7, algoritmos, health checks, sticky sessions; CDN e invalidação.
14. [[14 - Resiliência de rede]] — connection pooling, rate limiting, retry/backoff/jitter, circuit breaker, timeouts.
15. [[15 - Redes em entrevista]] — debugging rastreando camadas, system design de comunicação, inglês, vocabulário.

## Rotas alternativas

### Entrevista internacional
01 → 02 → 05 → 06 → 12 → 14 → 15. As camadas, TCP, TLS, HTTP, os números, resiliência e o capstone.

### Debugging de latência
01 → 02 → 04 → 05 → 12 → 15. Camadas, handshake TCP, DNS, TLS e os números — e o caso real no capstone.

### Protocolos de aplicação
06 → 07 → 10 → 11. HTTP a fundo, sua evolução, e os protocolos de API e tempo-real.

### System design de comunicação
12 → 13 → 14 → 15. Os números, distribuição de carga/CDN, resiliência e o fechamento.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Ciência/Redes e Protocolos"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Ciência/index|Fundamentos (MOC do domínio)]]
- [[API Design]] — design de API (recurso, versionamento, paginação, contrato de erro)
- [[System Design]] — escala e composição: LB, CDN, resiliência na escala de sistema
- [[Mensageria]] — comunicação assíncrona entre serviços
- [[Spring Boot]] — OkHttp, Resilience4j, HikariCP no ecossistema Java
- [[Dicionário de Ciência da Computação]]
