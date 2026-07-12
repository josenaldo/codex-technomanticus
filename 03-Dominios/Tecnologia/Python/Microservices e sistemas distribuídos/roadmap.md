---
title: "Roadmap — Python Microservices e sistemas distribuídos"
created: 2026-07-12
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Microservices e sistemas distribuídos (galho 15)

Roadmap-folha do galho `Python/Microservices e sistemas distribuídos`. Fase **Magus** — comunicação entre serviços em Python, cliente de API Gateway. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Mensageria/index.md` e `roadmap.md` (galho anterior, mesmo padrão).

Roster **não pré-cravado no spec** (descrição de alto nível "comunicação entre serviços em Python, cliente de API Gateway") — desenhado nesta sessão. Segundo galho do bloco **"Plataforma distribuída e produção"** (14-18).

**Fronteira cravada (ampla, verificada nesta sessão):** CAP/consistência/consenso, Circuit Breaker, API Gateway/BFF, Rate Limiting como padrão → [[03-Dominios/Engenharia/Arquitetura/System Design/index|System Design]] (sub-galhos 2 e 3 — Building blocks e Padrões recorrentes). Contratos REST/GraphQL/gRPC, idempotência, versionamento, caching HTTP, webhooks → [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] (sub-galhos 2 e 3). Java/Microservices (24 notas) é o exemplar de aplicação numa stack — este galho faz o equivalente Python, mas mantém a escala já estabelecida da trilha (8 notas), porque o spec original é mais estreito ("comunicação entre serviços em Python, cliente de API Gateway") do que o roster completo do Java.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 0 |
| ✅ feita | 8 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - Panorama — de monolito modular a microservices em Python
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 160 linhas / 3141 palavras (nota-mapa deliberadamente mais leve). Abre com time de notificações bloqueado por code freeze do time de produto (motivo organizacional real, não moda); mostra o que já está pronto (hexagonal do Galho 13, Outbox do Galho 14) via diagrama monólito-vs-microservices; "microservice premium" honesto; tabela "o que muda no código"; mapa de leitura.
- **Escopo:** a API de Tarefas construída ao longo da trilha (Galhos 9-14) já é um "monolito modular" bem organizado (arquitetura hexagonal do Galho 13, eventos assíncronos do Galho 14) — este galho não é sobre "quebrar tudo em microservices por moda", é sobre COMO, quando a decisão de extrair um serviço já foi tomada (referenciando [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/23 - Quando NÃO fazer microservices|a tese honesta do Java]] e/ou System Design sem repetir), o código Python se comunica com esse novo serviço. Mapa do galho.

#### 02 - Comunicação síncrona entre serviços — httpx
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 431 linhas / 6162 palavras. Abre com `httpx.get()` sem timeout travando todos os workers Gunicorn numa cascata; timeouts granulares (connect/read/write/pool), connection pooling via `Client()` reutilizável (paralelo ao Galho 9 nota 07), padrão `lifespan`/`app.state`/`Depends()` pro `AsyncClient` singleton (contraste com `Session` per-request do Galho 10).
- **Escopo:** `httpx` como cliente HTTP moderno (síncrono e assíncrono na mesma API, sucessor de `requests` pra uso em produção com asyncio), timeouts explícitos (por que NUNCA usar um cliente sem timeout configurado — request pendurada pra sempre), connection pooling/`Client()` reutilizável (custo de abrir conexão TCP+TLS a cada request, referenciando o Galho 9 nota 07 sobre esse mesmo custo no contexto de banco, sem repetir).

#### 03 - Resiliência na prática — tenacity e circuit breaker
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 398 linhas / 5078 palavras. Abre com `while True` retry ingênuo multiplicando carga sobre serviço já fora do ar; `tenacity` (`retry_if_exception` só timeout/5xx, nunca 4xx), `pybreaker` (3 estados referenciados de System Design), composição breaker-por-fora/retry-por-dentro com attempt count curto pra não estourar o breaker sozinho.
- **Escopo:** aplica o conceito de Circuit Breaker (já coberto em [[03-Dominios/Engenharia/Arquitetura/System Design/3 - Padrões recorrentes/05 - Circuit Breaker e resiliência|System Design]], referenciado sem repetir) com código Python real — `tenacity` (retry com backoff exponencial, `@retry(stop=..., wait=...)`) e `pybreaker`/`circuitbreaker` (estados fechado/aberto/half-open aplicados a uma chamada HTTP real via `httpx` da nota 02).

#### 04 - Cliente de API Gateway — autenticação serviço-a-serviço
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 503 linhas / 5779 palavras. Abre com serviço obtendo token novo a cada chamada, sobrecarregando o servidor de autorização (e sendo rate-limitado nele mesmo, ironicamente); `GatewayTokenClient` com cache/`Lock()`, `X-API-Key` como alternativa mais simples, `Retry-After` integrado a uma wait function customizada do `tenacity` da nota 03.
- **Escopo:** como um serviço Python consome uma API atrás de um Gateway (conceito de Gateway já coberto em System Design, referenciado sem repetir) — autenticação serviço-a-serviço (client credentials/API key, referenciando OAuth2 client credentials já coberto em [[03-Dominios/Engenharia/Auth e Identidade/2 - OAuth 2.1 e OpenID Connect/04 - Grants de máquina e fluxos especiais|Auth e Identidade]] sem repetir), awareness de rate limit (ler headers `Retry-After`/`X-RateLimit-*` e reagir, conectando com `tenacity` da nota 03).

#### 05 - Service discovery na prática
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 240 linhas / 4097 palavras (deliberadamente curta, código Python mínimo — maior parte é infra fora do escopo). Abre com júnior perguntando "onde está o código de service discovery" e a resposta honesta "não tem, é DNS do Kubernetes"; contraste breve com Consul/registry dedicado; explica por que client-side LB raramente é código em Python/Kubernetes.
- **Escopo:** como um cliente Python descobre o endereço de um serviço em vez de hardcoded — DNS interno/Kubernetes Service (`http://notificacoes-service.default.svc.cluster.local`, o jeito mais comum e mais simples hoje) vs. um client de service registry explícito (Consul, mencionado brevemente, sem desenvolver — referencia System Design/Java se cobrirem o conceito). Foco é honesto: na maioria dos deploys modernos (Kubernetes), "service discovery" já é DNS, não uma biblioteca especial.

#### 06 - Tracing distribuído com OpenTelemetry
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 363 linhas / 6431 palavras. Abre com "concluir tarefa" lento e uma hora de investigação sem correlação até achar o gargalo (chamada HTTP síncrona esquecida num consumer); instrumentação automática FastAPI+httpx como caminho prioritário, propagação W3C Trace Context, sequenceDiagram do trace correlacionando os 2 serviços.
- **Escopo:** OpenTelemetry Python SDK, instrumentação automática do FastAPI (`opentelemetry-instrumentation-fastapi`) e do `httpx` (`opentelemetry-instrumentation-httpx`), propagação de contexto de trace entre serviços (o trace ID viaja no header HTTP entre o serviço A e o serviço B, permitindo reconstruir a jornada completa de uma requisição). Não desenvolve o backend de coleta (Jaeger/Tempo) a fundo — é infra, mencionado brevemente.

#### 07 - Saga orquestrada em Python
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 420 linhas / 4594 palavras. Abre com `try/except: pass` engolindo falha de notificação, deixando tarefa órfã; `orquestrar_criar_tarefa_com_lembrete()` reusando Service Layer (Galho 13) + resiliência (nota 03), decisão explícita compensar-vs-degradar via `lembrete_obrigatorio`, compensação idempotente testada, contraste breve com Saga coreografada (já implícita no Galho 14).
- **Escopo:** o conceito de Saga já foi mencionado en passant no Galho 14 (Outbox e Saga — [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/04 - Outbox e Saga|Comunicação entre Sistemas]]) — esta nota desenvolve a implementação ORQUESTRADA (um coordenador central chama cada serviço em sequência, com passo de compensação se algo falhar no meio) com código Python real, usando o Service Layer (Galho 13 nota 06) como o orquestrador natural. Contraste breve com Saga coreografada (via eventos do Galho 14, sem orquestrador central).

#### 08 - Capstone — extraindo o serviço de Notificações
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Escopo:** recapitula o galho extraindo o `AbstractNotificador`/`SlackAdapter` (Galho 13 nota 07, consumido pelo worker do Galho 14) pra um SERVIÇO PYTHON SEPARADO com sua própria API HTTP — o serviço de Tarefas passa a chamar esse serviço de Notificações via `httpx` (nota 02) com retry/circuit breaker (nota 03), autenticado como client (nota 04), com tracing propagado (nota 06). Cenário prático integrador. Aponta para o Galho 16 (Build e tooling) como próximo passo — agora que existem DOIS serviços Python, packaging/tooling consistente entre eles importa mais.
- **Resultado:** 792 linhas / 7674 palavras. 9 peças amarrando as 7 notas anteriores: `notificacoes-service` FastAPI novo reusando `SlackAdapter` sem mudança, `httpx.AsyncClient` singleton, resiliência composta, `GatewayTokenClient` com cache, `pydantic-settings`, OpenTelemetry correlacionando os 2 processos, consumer do Galho 14 fisicamente realocado pro novo serviço, Saga orquestrada rodando contra o endpoint real. 5 diagramas Mermaid. Fecha o galho.

> [!success] Galho 15 completo — 8/8 notas (2026-07-12)
> Panorama honesto (01) → httpx com timeout/pooling (02) → resiliência tenacity/circuit breaker (03) → cliente de API Gateway/OAuth2 client credentials (04) → service discovery via DNS (05) → tracing distribuído com OpenTelemetry (06) → Saga orquestrada (07) → capstone extraindo o serviço de Notificações de verdade, com os dois serviços conversando síncrono (httpx+resiliência) e assíncrono (RabbitMQ do Galho 14) (08). CAP/Circuit Breaker/API Gateway como conceito nunca repetidos — sempre referenciados a System Design/Comunicação entre Sistemas. Próximo da trilha: Galho 16 — Build e tooling.

## Decisões e fronteiras registradas

- CAP/consistência/consenso, Circuit Breaker, API Gateway/BFF, Rate Limiting → [[03-Dominios/Engenharia/Arquitetura/System Design/index|System Design]]; aqui é só a aplicação Python.
- Contratos REST/GraphQL/gRPC, idempotência, versionamento, webhooks → [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]]; aqui é só o cliente consumindo.
- Mensageria/broker/Outbox/DLQ → Galho 14 desta trilha; reusado, não repetido.
- OAuth2 client credentials/grants de máquina → Auth e Identidade SG2; referenciado na nota 04.
- Observabilidade de produção (logging estruturado, métricas, dashboards) → Galho 17 futuro; aqui só tracing é tocado (nota 06).
- Kubernetes/deploy em si → Galho 18 futuro (Cloud-native e produção); aqui service discovery via DNS é só mencionado como fato, não ensinado como operar Kubernetes.
- Escala 8 notas (não 24 como Java) — spec original mais estreito, e boa parte do que Java desenvolve (Spring Cloud Config, Gateway reativo vs MVC, service mesh) já não se aplica sem framework equivalente em Python ou é infra pura.
