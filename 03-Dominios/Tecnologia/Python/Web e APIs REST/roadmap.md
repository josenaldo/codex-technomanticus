---
title: "Roadmap — Python Web e APIs REST"
created: 2026-07-11
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Web e APIs REST (galho 10)

Roadmap-folha do galho `Python/Web e APIs REST`. Fase **Adepto** — Django vs. FastAPI vs. Flask, routing, serialização, validação (Pydantic). Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Persistência de dados/index.md` e `Python/Persistência de dados/roadmap.md` (galho anterior, mesmo padrão).

Roster **não pré-cravado no spec** (só a descrição de alto nível "Django vs FastAPI vs Flask, routing, serialização, validação (Pydantic)") — desenhado nesta sessão seguindo o mesmo playbook dos Galhos 5, 7, 8 e 9. Segundo galho do bloco **"Backend e arquitetura"** (9-13) — consome a camada de persistência do Galho 9 e o protocolo ASGI cru do Galho 8 (nota 05), sem repetir nenhum dos dois.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 9 |
| ⬜ pendente | 0 |
| ✅ feita | 9 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - Django vs FastAPI vs Flask — panorama e filosofias
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** panorama comparativo dos três frameworks — `Flask` (WSGI, minimalista, microframework, você escolhe as peças), `Django` (WSGI/ASGI híbrido, "baterias inclusas", opinativo, MTV), `FastAPI` (ASGI nativo, tipagem como contrato via Pydantic, o mais recente). Critérios de escolha (tamanho do time, prazo, necessidade de admin/ORM pronto, performance de I/O). WSGI vs ASGI referenciado ao Galho 8 nota 05 sem reexplicar o protocolo. Abre o galho como mapa mental.
- **Resultado:** 305 linhas / 4520 palavras. Abre com uma squad decidindo framework sem critério real; compara os três com o mesmo endpoint `GET /produtos/{id}` implementado lado a lado; fecha com árvore de decisão Mermaid e tabela comparativa de 10 critérios. ASGI cru e Django ORM só referenciados via wikilink (Galho 8 nota 05, Galho 9 nota 04), sem reexplicar.

#### 02 - Roteamento — decorators, urls.py e path operations
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** como cada framework mapeia URL → código — Flask (`@app.route`, `Blueprint`), Django (`urls.py`, `path()`/`re_path()`, `include()`, class-based views vs function-based), FastAPI (`@app.get`/`@router.get`, `APIRouter`, path parameters tipados). Comparativo lado a lado do mesmo endpoint nos três.
- **Resultado:** 488 linhas / 4917 palavras. Abre com o bug de `APPEND_SLASH` do Django redirecionando `POST /tarefas` sem barra final (risco de o cliente descartar o corpo no redirect), comparado ao `strict_slashes` do Flask e `redirect_slashes` do FastAPI; desenvolve roteamento nos três (Blueprint/`include()`/`APIRouter`, FBV vs CBV, path params tipados como contrato — tipagem resolve forma, não existência); CRUD de "tarefas" roteado lado a lado, 1 diagrama Mermaid da árvore de roteamento, 3 armadilhas em callout.

#### 03 - Validação e serialização com Pydantic
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** `BaseModel` do Pydantic v2, validação automática de request body no FastAPI, `Field`/validators customizados, `response_model` (serialização de saída, o que ele esconde/filtra), união de tipos e `Optional`, erros de validação viram HTTP 422 automaticamente. Contraste breve com dataclasses puras (por que Pydantic ganhou popularidade sobre elas para fronteira de API).
- **Resultado:** 503 linhas / 5833 palavras. Abre com hash de senha vazando numa resposta porque `Usuario` era usado como modelo de entrada e de saída, sem `response_model` filtrando; desenvolve `BaseModel`/`Field`/`@field_validator`, o padrão `UserCreate`/`UserRead` como peneira declarativa (diagrama Mermaid do fluxo requisição→validação→lógica→filtro→resposta), `Optional`/uniões/modelos aninhados, formato exato do erro 422 (`detail`/`loc`/`msg`/`type`), contraste com dataclasses puras. Referencia Galho 5 (Tipagem moderna) sem repetir.

#### 04 - Injeção de dependência no FastAPI — Depends
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** `Depends()` como mecanismo central do FastAPI — dependências como funções/geradores, sub-dependências encadeadas, escopo por request, `yield` em dependências para cleanup (paralelo a context manager), casos de uso reais (sessão de banco do Galho 9, paginação, filtros compartilhados). O que torna o FastAPI testável (`app.dependency_overrides`).
- **Resultado:** 537 linhas / 5667 palavras. Abre com `Session` do SQLAlchemy vazando por early-return num handler que abria conexão manualmente; desenvolve `Depends()` como árvore de sub-dependências, escopo/cache por requisição, `yield` como context manager gerenciado pelo framework (sequenceDiagram setup/handler/teardown). Fecha com `app.dependency_overrides` para testabilidade.

#### 05 - Django REST Framework — serializers, viewsets e routers
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** DRF como a camada REST sobre o Django puro — `Serializer`/`ModelSerializer` (contraste direto com Pydantic da nota 03), `APIView` vs `ViewSet`/`ModelViewSet`, `Router` gerando URLs automaticamente, `permission_classes`/`authentication_classes` mencionados brevemente (aprofundado no Galho 11). Quando DRF vale a complexidade extra sobre FastAPI puro.
- **Resultado:** 500 linhas / 5289 palavras. Abre com `fields = "__all__"` vazando `notas_internas`, espelhando o incidente da nota 03; percorre `Serializer`→`ModelSerializer`→`SerializerMethodField`, `APIView` manual (~35 linhas) vs `ModelViewSet` (4 linhas), `Router` gerando rotas (diagrama Mermaid do pipeline). Fecha com tabela de decisão DRF vs FastAPI.

#### 06 - Tratamento de erros e respostas HTTP padronizadas
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** `HTTPException` do FastAPI, exception handlers customizados (`@app.exception_handler`), DRF exception handling (`exception_handler` custom, `APIException`), Flask `errorhandler`, formato de erro consistente (motivação para RFC 7807/Problem Details, sem exigir a lib pronta), status codes semânticos (400 vs 422 vs 409).
- **Resultado:** 687 linhas / 6735 palavras (linhas acima do alvo pelo volume de código nos 3 frameworks, palavras dentro do alvo). Abre com um frontend quebrando contra 3 formatos de erro diferentes, incluindo traceback vazado em produção (falha de segurança, não só cosmética); desenvolve exception handler em cada framework, RFC 7807 como padrão conceitual, worked example de 409 (email duplicado) nos três. Fecha com o contrato de erro proposto pra capstone (nota 09).

#### 07 - Middleware e o ciclo de vida da requisição
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** middleware nos três frameworks — Django (`MIDDLEWARE` list, `get_response`/`process_request`/`process_response`), Flask (`before_request`/`after_request`), FastAPI (`@app.middleware("http")`, `BaseHTTPMiddleware`). Ordem de execução, casos de uso (logging, CORS, tempo de request), referência ao `scope`/`receive`/`send` do ASGI cru (Galho 8 nota 05) sem repetir.
- **Resultado:** 523 linhas / 6269 palavras. Abre com middleware de auditoria posicionado depois do middleware de autenticação (tentativas rejeitadas nunca logadas); desenvolve a "cebola" do Django, hooks não-aninhados do Flask, `BaseHTTPMiddleware`/`call_next` do FastAPI sobre ASGI (2 diagramas Mermaid). Armadilha da ordem invertida de `add_middleware`.

#### 08 - Documentação automática com OpenAPI
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** geração automática de spec OpenAPI no FastAPI (Swagger UI/ReDoc de graça, a partir dos type hints e Pydantic models da nota 03), `drf-spectacular` no Django (anotação manual necessária), Flask sem suporte nativo (menção a `flasgger`/`apispec`). Por que "documentação de graça" é um dos argumentos centrais a favor do FastAPI em entrevista.
- **Resultado:** 445 linhas / 6623 palavras. Abre com um frontend perdendo um dia reverse-engineering um endpoint Flask sem docs, seguido de um bug de billing causado por Swagger doc manual desatualizada; desenvolve geração automática (FastAPI) vs anotação manual (`drf-spectacular`) vs ausência (Flask + libs de terceiro). Warning sobre expor `/docs` publicamente em produção.

#### 09 - Capstone — uma API REST completa de ponta a ponta
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** recapitula o galho construindo uma API REST completa (ex: sistema de tarefas/to-do multiusuário) com FastAPI + Pydantic + a camada de persistência do Galho 9 — roteamento (nota 02), validação/serialização (nota 03), injeção de dependência para sessão de banco (nota 04), tratamento de erros padronizado (nota 06), middleware de logging (nota 07), docs automática (nota 08). Cenário prático integrador, não introduz conceito novo raso. Aponta para o Galho 11 (Segurança) como próximo passo natural (a API ainda não tem autenticação).
- **Resultado:** 640 linhas / 5526 palavras. API de Tarefas multiusuário (Usuario→Tarefa) em 5 etapas incrementais, cada uma amarrando uma nota do galho: roteamento via `APIRouter` (02), `TarefaCreate`/`TarefaRead` com `usuario_id` nunca vazando pro input (03, espelhando o incidente da própria nota 03), `Depends(get_db)` consumindo `Engine`/`sessionmaker` do Galho 9 (04), contrato de erro `type`/`title`/`status`/`detail` proposto na nota 06 com 404-não-403 deliberado por segurança, middleware de correlation-ID/tempo de resposta (07). 3 diagramas Mermaid (ER, sequenceDiagram completo, flowchart das 5 camadas + OpenAPI de graça). Fecha o galho apontando `usuario_id` como query param — placeholder deliberado que o Galho 11 (Segurança) substitui — e para os Galhos 12/13.

> [!success] Galho 10 completo — 9/9 notas (2026-07-11)
> Panorama Django/FastAPI/Flask (01) → roteamento comparado (02) → Pydantic (03) → `Depends` (04) → DRF (05) → erros padronizados (06) → middleware (07) → OpenAPI automático (08) → capstone integradora de uma API de Tarefas multiusuário amarrando as 8 notas anteriores sobre a camada de persistência do Galho 9 (09). Próximo da trilha: Galho 11 — Segurança.

## Decisões e fronteiras registradas

- Protocolo ASGI cru (`scope`/`receive`/`send`) → Galho 8 nota 05; aqui só referenciado (notas 01 e 07).
- Camada de persistência (SQLAlchemy/Django ORM, migrations, N+1, transações, pooling) → Galho 9; aqui os endpoints consomem, sem repetir.
- Autenticação/autorização de API (JWT, OAuth2, API keys, `permission_classes` do DRF em profundidade) → Galho 11 (Segurança); aqui só mencionado en passant onde aparece organicamente (nota 05).
- Testes de API (`TestClient`, fixtures de rota, `pytest-django`) → Galho 12 (Testes).
- Repository/Unit of Work formal → Galho 13 (Arquitetura e Design Patterns).
- FastAPI recebe peso maior no roster (notas 03/04/08 dedicadas) por ser a recomendação de mercado atual (pesquisa do spec: Codar.me/Academify, Dunossauro/FastAPI do Zero); Django/DRF cobre o caminho opinativo "baterias inclusas"; Flask serve de baseline minimalista nas notas 01-02 e no comparativo.
