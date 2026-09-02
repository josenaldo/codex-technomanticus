---
title: "API Design"
created: 2026-04-01
updated: 2026-07-09
type: concept
progress: done
status: evergreen
tags:
  - arquitetura
  - entrevista
publish: false
---

# API Design

> [!info] Conteúdo migrado para a trilha
> O conteúdo de desenho de API foi reescrito e aprofundado na trilha [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] (4 sub-galhos, 22 notas + capstone). Os links abaixo apontam pra casa de cada tema. O que não migrou (file upload) e a seção "Na prática" do autor continuam aqui.

A arte de projetar interfaces de comunicação entre sistemas que sejam **intuitivas para o consumidor**, **consistentes**, **seguras** e **evoluíveis sem quebrar clientes existentes**. Enquanto [[Redes e Protocolos]] cobre o "como" da comunicação (HTTP, TCP, TLS) e [[System Design]] cobre o "quanto" (escala, cache, rate limiting em alto nível), a trilha [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] foca no **contrato**: o que sua API promete, como ela responde, e como ela evolui.

## Onde encontrar cada tema agora

| Tema | Nota canônica |
|------|----------------|
| Modelagem de recursos, verbos HTTP, nested vs flat | [[2 - Comunicação síncrona/01 - REST — modelagem de recursos e maturidade\|REST — modelagem de recursos e maturidade]] |
| Richardson Maturity Model, HATEOAS/HAL | [[2 - Comunicação síncrona/01 - REST — modelagem de recursos e maturidade\|REST — modelagem de recursos e maturidade]] |
| Status codes, RFC 9457 Problem Details, content negotiation | [[2 - Comunicação síncrona/02 - REST — o contrato de resposta\|REST — o contrato de resposta]] |
| Paginação (offset/cursor), filtros, autenticação (API key/JWT/OAuth) | [[2 - Comunicação síncrona/03 - Paginação, filtros e autenticação em REST\|Paginação, filtros e autenticação em REST]] |
| GraphQL (schema, resolvers, N+1/DataLoader) | [[2 - Comunicação síncrona/04 - GraphQL — schema, resolvers e quando vale\|GraphQL — schema, resolvers e quando vale]] |
| gRPC (Protobuf, HTTP/2, streaming) | [[2 - Comunicação síncrona/05 - gRPC — Protobuf, HTTP2 e streaming\|gRPC — Protobuf, HTTP2 e streaming]] |
| REST vs GraphQL vs gRPC, OpenAPI, contract testing | [[2 - Comunicação síncrona/06 - REST vs GraphQL vs gRPC — decisão\|REST vs GraphQL vs gRPC — decisão]] |
| Idempotência (Idempotency-Key) | [[3 - Confiabilidade do contrato/01 - Idempotência\|Idempotência]] |
| Versionamento e evolução de contrato | [[3 - Confiabilidade do contrato/02 - Versionamento e evolução de contrato\|Versionamento e evolução de contrato]] |
| Caching HTTP, ETag, optimistic locking | [[3 - Confiabilidade do contrato/03 - Caching HTTP e requisições condicionais\|Caching HTTP e requisições condicionais]] |
| Rate limiting como contrato (headers, 429) | [[3 - Confiabilidade do contrato/04 - Rate limiting como contrato\|Rate limiting como contrato]] |
| Webhooks, 202+polling, bulk operations | [[3 - Confiabilidade do contrato/05 - Webhooks e operações assíncronas\|Webhooks e operações assíncronas]] |
| RPC legado (SOAP/CORBA/DCOM/XML-RPC) e onde sobrevive | [[1 - Panorama e decisão/02 - RPC clássico e por que caiu\|RPC clássico e por que caiu]] |
| Panorama comparativo e framework de decisão | [[1 - Panorama e decisão/05 - O que está emergindo e framework de decisão\|O que está emergindo e framework de decisão]] |
| Um walkthrough completo, todas as decisões juntas | [[Desenhando a comunicação de um sistema do zero]] (capstone) |

---

## File upload

> [!info] Único tema deste monólito que não migrou pra trilha (fora do roster da spec).

### Multipart form data (simples)

```http
POST /documents
Content-Type: multipart/form-data; boundary=...

--boundary
Content-Disposition: form-data; name="metadata"
Content-Type: application/json

{ "title": "Exame médico" }
--boundary
Content-Disposition: form-data; name="file"; filename="exame.pdf"
Content-Type: application/pdf

<binary content>
--boundary--
```

**Limites:** OK para arquivos pequenos (< 10MB). Tem overhead de base64 se enviado como JSON.

### Presigned URLs (arquivos grandes)

Cliente sobe direto pro storage (S3), sem passar pela sua API.

```
Passo 1: Cliente pede URL de upload
  POST /documents/upload-url
  { "filename": "video.mp4", "content_type": "video/mp4", "size": 500000000 }

  Response:
  {
    "upload_url": "https://bucket.s3.amazonaws.com/...?X-Amz-Signature=...",
    "document_id": "doc-123",
    "expires_at": "..."
  }

Passo 2: Cliente faz PUT direto no S3
  PUT <upload_url>
  (corpo = arquivo binário)

Passo 3: Cliente confirma
  POST /documents/doc-123/confirm
```

**Prós:** sua API não carrega o arquivo na memória, escala sem limite, mais rápido.

**Contras:** mais complexo, cliente precisa entender o fluxo.

### Chunked/resumable upload

Para uploads enormes com recuperação de falha: cliente envia em pedaços, servidor junta. S3 Multipart Upload, Google Resumable Upload, tus.io protocol.

---

## Na prática (da minha experiência)

> **MedEspecialista — API REST com RFC 9457 e Problem Details:** Implementei um `@RestControllerAdvice` global que traduz exceções de domínio em respostas Problem Details padronizadas. Todo erro tem `type`, `title`, `status`, `detail`, `trace_id` e, quando aplicável, um array `errors` com `field`, `code`, `message`. O frontend React mostra mensagens ao usuário usando o `code` (para i18n) e loga o `trace_id` — quando um usuário reporta um problema, eu busco pelo trace_id nos logs do backend e encontro o request exato. Reduziu drasticamente o tempo de debugging.
>
> **Idempotency para pagamentos:** No endpoint de criação de pagamento, exijo header `Idempotency-Key` (UUID). Armazeno a chave + hash do request + response em uma tabela com TTL de 24h. Se o mesmo key vem de novo com mesmo request, retorno a response cacheada. Se vem com request diferente, retorno 422 "key reused". Isso salvou mais de uma vez: mobile com rede ruim retentando o pagamento que tinha ido pelo primeiro tentativa.
>
> **Versionamento por URL path:** Uso `/api/v1/...` desde o dia 1. Quando precisei fazer breaking change em um endpoint, lancei `/api/v2/patients` em paralelo, mantive v1 funcionando, e só desliguei v1 depois de 6 meses e de confirmar por logs que nenhum cliente usava mais. Sem drama.
>
> **Paginação cursor-based no feed:** A listagem de consultas agendadas do médico usa cursor-based pagination (encoded com created_at + id). Inicialmente tinha offset, mas com médicos que têm milhares de consultas históricas, offset com página 500 ficava lento. Cursor resolve em O(log n) via índice composto `(doctor_id, created_at DESC, id DESC)`.
>
> **OpenAPI como contrato:** SpringDoc gera o OpenAPI a partir das annotations. O frontend (React + TypeScript) consome esse OpenAPI via `openapi-typescript` para gerar tipos e clients automaticamente. Quando o backend muda um campo, o TypeScript quebra no frontend — erro de compilação, não em runtime. Esse ciclo salvou vários bugs antes de chegar em produção.
>
> **A lição principal:** tratar a API como um produto, não como uma consequência do código. Quem vai consumir ela? Como fica a experiência dele? O que acontece quando ela falhar? Essas perguntas importam mais que detalhes de implementação.

---

## Veja também

- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — a trilha completa (4 sub-galhos + capstone)
- [[Redes e Protocolos]] — HTTP, TCP, TLS, WebSocket, gRPC em profundidade
- [[System Design]] — rate limiting, caching, escala, patterns
- [[Arquitetura de Software]] — DDD, bounded contexts, como APIs expõem domínios
- [[Spring Boot]] — implementação prática de APIs REST na stack Java
- [[Node.js]] — implementação em Node/Express/NestJS
- [[Python Backend]] — Django REST Framework, FastAPI
- [[03-Dominios/Tecnologia/Go/index|Go]] — trilha Go: net/http e frameworks (galho 10), gRPC e protobuf (galho 12)
