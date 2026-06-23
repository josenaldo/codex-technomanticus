---
title: "Galho Redes e Protocolos — design e plano (Fundamentos, Camada A)"
created: 2026-06-18
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - redes
---

# Galho Redes e Protocolos — design e plano

## Contexto
Sexto galho da Camada A do meta-plano de Fundamentos (`2026-06-15-fundamentos-meta-planejamento-design.md`),
depois de **Estruturas de Dados**, **Algoritmos**, **OO**, **SOLID** e **Banco de Dados** (todos COMPLETOS,
2026-06-17). Refatora o monólito `03-Dominios/Ciência/Redes e Protocolos.md` (653 ln, evergreen) no
padrão tronco/galhos + 3 fases. Interview-critical (★). Roster aprovado pelo usuário em 2026-06-18.

A semente é o monólito inteiro: modelo de camadas, TCP/UDP, DNS, TLS, HTTP (métodos/status/caching/CORS),
evolução HTTP, REST/GraphQL/gRPC, WebSocket/SSE, load balancing, CDN, latência/throughput, connection
pooling, rate limiting, retries/backoff, circuit breaker, timeouts, armadilhas, e 5 experiências reais do
usuário (preservar, [[feedback-no-fabrication]]).

## Decisões de escopo (aprovadas, não reabrir)

1. **Conteúdo "sabor system design" FICA como fundamento de rede.** Load balancing, CDN, rate limiting,
   retries/backoff, circuit breaker, connection pooling e os números de latência são fundamentos de rede —
   não são podados. As notas 12/13/14 forward-linkam `[[System Design]]` para a escala/composição de sistema.
2. **REST/GraphQL/gRPC e WebSocket/SSE = nível de PROTOCOLO aqui.** Transporte, serialização, streaming,
   multiplexing, quando escolher. O **design de API** (modelagem de recurso, versionamento, paginação,
   contrato de erro, HATEOAS, Richardson Maturity) é de `[[API Design]]` — linka, não duplica.
3. **TLS = o PROTOCOLO aqui** (handshake, certificados/CA, cipher suites, mTLS, pinning, HSTS, forward
   secrecy, TLS 1.3 / 0-RTT). As **primitivas criptográficas** (Diffie-Hellman, hashing, simétrico ×
   assimétrico, PKI a fundo) ficam pro futuro galho **Segurança Conceitual** (Camada D) — mencionar em
   PROSA, sem wikilink quebrado.
4. **Teto de prosa 2400 (permissão, não alvo); código e wire-diagrams ASCII não contam.** Alvo honesto
   ~300–520 ln. CORS é nota standalone (09), SEM nota dedicada de IP (pincelado na 01), TLS em Adepto.

## Fronteiras (rígido — linka, não duplica)
- **API Design** (`[[API Design]]`) — modelagem de recurso, versionamento, paginação, contrato de erro,
  HATEOAS, Richardson Maturity Model. A nota 10 trata REST/GraphQL/gRPC **como protocolo** e linka.
- **System Design** (`[[System Design]]`) — escala e composição de sistema. As notas 12 (números),
  13 (LB/CDN) e 14 (resiliência) são fundamento de rede e **forward-linkam** pra lá.
- **Mensageria / Kafka** (`[[Mensageria]]`, `[[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka]]`) — comunicação
  assíncrona. A nota 10 menciona mensageria como alternativa a chamadas síncronas e linka.
- **Segurança Conceitual** (futuro galho, Camada D) — primitivas cripto. A nota 05 (TLS) menciona DH/PKI
  em PROSA, sem wikilink (evita link quebrado).
- **Java** (`[[Spring Boot]]`) — OkHttp/connection pool, Resilience4j (circuit breaker/retry/rate limit),
  HikariCP. Callout linkando, não corpo. (Resilience4j já é tratado no galho Java/Microservices.)
- **Infraestrutura** (`[[03-Dominios/Tecnologia/Infraestrutura/Linux|Linux]]`, K8s networking, `[[Nginx]]`) — operar
  o stack. Linka.

## Preservação (rígido) — experiências REAIS, relocadas do monólito ([[feedback-no-fabrication]])
- **Arquitetura de comunicação do MedEspecialista** — REST p/ API pública (mobile+web), Kafka p/ async
  entre serviços (agendamento → notificação → faturamento), gRPC considerado p/ chamadas síncronas internas
  ao migrar pra microserviços → **nota 10**.
- **Debugging de latência** — endpoint ~1.5s; `EXPLAIN` do banco dava 20ms; a app fazia 3 chamadas HTTP
  síncronas sequenciais a um serviço externo (DNS não-cacheado + TLS handshake + response); fix: paralelizar
  com `CompletableFuture` + cachear respostas com TTL curto no Redis + cachear DNS localmente → caiu pra
  200ms → **nota 15** (caso-âncora de debugging; referenciado da 12 e 14).
- **CORS** — perdeu horas debugando "POST funciona no Postman mas não no browser" até entender que CORS é
  mecanismo do browser (a request nem chega ao servidor se o preflight falha); usa `Access-Control-Max-Age:
  86400` pra cachear preflight 24h → **nota 09**.
- **Caching** — endpoint de listagem de especialidades médicas (muda ~1x/mês); adicionou `Cache-Control:
  public, max-age=3600` + ETag; o CDN passou a servir direto e o endpoint sumiu dos logs do backend; zero
  código de cache aplicacional → **nota 08**.
- **WebSocket vs SSE** — dashboard de monitoramento de agendamentos; começou com WebSocket por "preciso de
  tempo real"; percebeu que o fluxo era unidirecional (servidor → dashboard); migrou pra SSE — mais simples,
  reconexão automática, funciona com o load balancer existente sem config extra → **nota 11**.

## Roster de notas (15; pode crescer/encolher por split)

### Iniciado
1. **O que é uma rede / modelo de camadas** *(âncora)* — protocolos, OSI × TCP-IP (5 camadas),
   encapsulamento, IP/portas/NAT pincelado, as duas faces em entrevista (system design + debugging).
   Forward-link às vizinhas.
2. **TCP** — 3-way handshake, garantias (entrega/ordem/fluxo), sliding window, slow start /
   congestion control, TIME_WAIT e esgotamento de portas efêmeras.
3. **UDP** — sem garantias, casos de uso (DNS, streaming, jogos, VoIP), TCP × UDP,
   confiabilidade-sobre-UDP → QUIC.
4. **DNS** — hierarquia de resolução, tipos de registro, TTL/cache, GeoDNS/anycast/round robin,
   DNS e latência, service discovery.

### Adepto
5. **TLS e HTTPS** — handshake, certificados/CA, cipher suites, mTLS, pinning, HSTS, forward secrecy,
   TLS 1.3 / 0-RTT. Primitivas cripto (DH/PKI) só em PROSA (galho futuro Segurança).
6. **HTTP: métodos, status e headers** — idempotência/safe, anatomia req/resp, 401 × 403, famílias de
   status, headers essenciais. Linka `[[API Design]]` para o design.
7. **A evolução do HTTP: 1.1 → 2 → 3** — texto × binário, multiplexing, head-of-line blocking,
   HPACK/QPACK, server push, QUIC sobre UDP.
8. **Caching HTTP** — `Cache-Control`, ETag/condicional (If-None-Match → 304), `Vary`, camadas de cache,
   stale-while-revalidate. *(exp real: especialidades médicas)*
9. **CORS e a same-origin policy** — same-origin, preflight (OPTIONS), headers, `Access-Control-Max-Age`,
   "CORS não é segurança do servidor". *(exp real: Postman × browser)*
10. **REST, GraphQL e gRPC** — comparação **de protocolo** (transporte, serialização, streaming) +
    quando escolher. Linka `[[API Design]]` (design) e `[[Mensageria]]` (async). *(exp real: MedEspecialista)*
11. **WebSocket e SSE** — bidirecional × unidirecional, handshake/upgrade, quando escolher, LB e proxies,
    reconexão. *(exp real: dashboard WS → SSE)*

### Magus
12. **Latência, throughput e os números** — latência × throughput × bandwidth, a tabela de números, RTT,
    por que caching/CDN/local importam. **Forward-linka [[System Design]]**. *(ref do caso da nota 15)*
13. **Load balancing e CDN** — L4 × L7, algoritmos, health checks, sticky sessions; CDN como cache de
    borda, invalidação (cache busting/purge/TTL). **Forward-linka [[System Design]]**.
14. **Resiliência de rede** — connection pooling, rate limiting (token bucket / sliding / fixed window),
    retry/backoff/jitter, circuit breaker, timeouts. **Forward-linka [[System Design]]** + callout
    Java/Resilience4j (`[[Spring Boot]]`). *(ref do caso da nota 15)*
15. **Capstone: redes em entrevista** — debugging de latência rastreando as camadas (caso-âncora real),
    system design de comunicação, "How to explain in English", vocabulário PT→EN, armadilhas consolidadas,
    recursos. *(exp real: 1.5s → 200ms)*

## Padrão por nota (idêntico aos galhos anteriores)
- PT-BR, registro Feynman (analogias, perguntas retóricas, callouts, frases curtas, resumo em 1 linha);
  profundo à medida do tema; teto 2400 (permissão; código/wire-diagrams não contam).
- **3–5 diagramas Mermaid** por nota onde ajudam, cada um com lead-in antes + "leitura do diagrama" depois.
  Bons para rede: `sequenceDiagram` (handshakes TCP/TLS, preflight CORS, SSE/WS), `flowchart` (resolução
  DNS, camadas, cache, decisão LB), tabelas markdown para comparações. **Sem `xychart-beta`** (não renderiza
  no Obsidian — usar tabela/flowchart). Símbolos/parênteses LITERAIS na prosa; entidades HTML (`&#40;` etc.)
  SÓ dentro de rótulos Mermaid e sempre entre aspas.
- **Seção final "Em entrevista"** — 4–7 frases EN + sub-seção "Vocabulário" PT→EN.
- Callout final `> [!info] Lastro` de honestidade citando fontes VERIFICADAS na web (WebSearch); não inventar.
- Atomicidade: linka vizinhas em vez de duplicar. `NN - Título.md` flat.
- `publish: false` nas notas; `publish: true` só no `index.md`. Frontmatter `fase:`, `type: concept`,
  `status: evergreen`, tags.
- **NUNCA fabricar** experiências/dados do usuário; preservar e relocar as 5 experiências reais (mapa acima).

## Tronco e MOC
- Pasta `03-Dominios/Ciência/Redes e Protocolos/` com `index.md` (MOC, `type: moc`, `status: growing`,
  `publish: true`, agrupado por fase, rotas alternativas, dataview, "Veja também").
- Alias do `index.md`: **"Redes e Protocolos"** + **"Redes"** + **"Redes de Computadores"** + **"Networking"**
  para resolver os ~15 links de entrada (API Design, System Design, Kafka/Mensageria, Banco de Dados,
  Arquitetura, Java, Infra, Senda Entrevistas, Full Stack Open, índice, README).
- A entrada Redes e Protocolos entra no MOC do domínio em DOIS arquivos: `Fundamentos/index.md` e
  `Fundamentos.md` (trocar a linha `[[Redes e Protocolos]]` por link ao `…/Redes e Protocolos/index`).

## Convenções de execução
- Subagent-driven, um subagente por nota, escrita em UMA chamada Write, com o house-style completo no prompt.
- Disparar por fase (Iniciado, depois Adepto, depois Magus), revisando armadilhas e commitando entre fases.
- Commits direto na main, SEM push, SEM Co-Authored-By ([[feedback-commits]]).

## Sequência de construção
1. Scaffold `Redes e Protocolos/index.md` + aliases. Commit.
2. Escrever as notas Iniciado (01–04), Adepto (05–11), Magus (12–15), uma por subagente. Relocar as
   experiências reais conforme o mapa de preservação. Commit por fase.
3. Registrar a entrada no MOC do domínio (`Fundamentos/index.md` + `Fundamentos.md`).
4. Remover o monólito `Redes e Protocolos.md` (`git rm`); checar armadilhas (entidades HTML na prosa,
   `xychart-beta`, `[[` partido por quebra de linha); verificar alvos externos; fechar MOCs; atualizar
   memória `project-fundamentos-meta-plan` (marcar Redes COMPLETO). Depois de Redes, só falta **Testes**
   pra fechar a Camada A.
