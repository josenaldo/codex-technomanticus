---
title: "Roadmap — Python Programação Reativa e Assíncrona"
created: 2026-07-11
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Programação Reativa e Assíncrona (galho 8)

Roadmap-folha do galho `Python/Programação Reativa e Assíncrona`. Fase **Magus** — asyncio deep-dive, aiohttp, ASGI, back-pressure, padrões de produção. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Concorrência e paralelismo/index.md` e `Python/Concorrência e paralelismo/roadmap.md` (galho anterior, mesmo padrão).

Roster **não pré-cravado no spec** (só a descrição de alto nível "asyncio deep-dive, aiohttp, async frameworks, back-pressure") — desenhado nesta sessão seguindo o mesmo playbook dos Galhos 5 e 7. Decisão de fronteira: **os fundamentals de asyncio (event loop básico, coroutines, `Task`, `gather`, `TaskGroup`, cancelamento) não são reexplicados aqui** — já fechados nas notas 06-07 do Galho 7; este galho referencia via wikilink e foca em rede, ecossistema e produção. **FastAPI/Django/Flask em profundidade ficam pro Galho 10** (Web e APIs REST) — aqui o protocolo ASGI é explicado conceitualmente, não os frameworks específicos.

> [!success] Galho 8 completo — 8/8 notas (2026-07-11)
> A capstone fechou o galho amarrando `aiohttp.ClientSession` reutilizada (nota 03) + `asyncio.Semaphore` limitando concorrência (nota 06) + retry com backoff e circuit breaker + supervisão de tasks e graceful shutdown com progresso parcial (nota 07) num web scraper assíncrono de produção real, rodável de ponta a ponta. Próximo da trilha: Galho 9 — Persistência de dados.

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

#### 01 - Event loop por dentro — selectors, callbacks e a relação Future/Task
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** o que `asyncio.run()` de fato instancia (`SelectorEventLoop` no Linux, baseado em `selectors`/`epoll`), como I/O não-bloqueante é registrado e despachado via callbacks, a relação real entre `Future` (promessa de um valor) e `Task` (`Future` + coroutine agendada — `Task` é subclasse de `Future`), `loop.call_soon`/`call_later`/`call_at`. Assume Galho 7 notas 06-07 como pré-requisito (não repete o que é uma coroutine/Task).
- **Resultado:** 428 linhas / 6660 palavras. Abre com o bug de tratar `loop.call_soon()` como um `await` disfarçado (agenda mas não sincroniza); cobre `SelectorEventLoop`/`ProactorEventLoop` e a escolha automática `epoll`/`kqueue`/`select` via `selectors.DefaultSelector`, o ciclo completo do loop (`add_reader`→despacho→callback→retomada de `Future`), a relação de herança real `Task(Future)` e o mecanismo de `Task.__step` avançando a coroutine como um gerador, `call_soon`/`call_later`/`call_at` com `loop.time()` monotônico, `asyncio.sleep()` reimplementado sobre `call_later` para amarrar as peças, nota sobre eager task factory (3.12+) e modo debug (`PYTHONASYNCIODEBUG`) como ferramenta de diagnóstico prático.

#### 02 - Streams assíncronos — StreamReader, StreamWriter e protocolos de rede
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** `asyncio.open_connection`/`start_server`, `StreamReader`/`StreamWriter`, ler/escrever bytes de forma assíncrona, implementar um protocolo de rede simples (ex: cliente/servidor de echo ou um mini protocolo de linha), `readuntil`/`readline`/`drain()` (back-pressure em nível de socket).
- **Resultado:** 409 linhas / 5113 palavras. Servidor+cliente de chat TCP linha-a-linha completos e funcionais com `asyncio.open_connection`/`start_server`; foco em `writer.drain()` como mecanismo de back-pressure (incluindo o `pause_writing`/`resume_writing` por baixo), `readline`/`readexactly`/`readuntil` para delimitação de mensagens, e armadilhas de produção (write sem drain, EOF não tratado, código bloqueante no handler).

#### 03 - aiohttp cliente — ClientSession, connection pooling e requisições concorrentes
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** `aiohttp.ClientSession` (por que reutilizar a sessão importa — connection pooling), requisições concorrentes com `asyncio.gather`/`TaskGroup` (retomando o Galho 7 sem reexplicar), timeouts (`ClientTimeout`), tratamento de erros de rede, streaming de resposta grande.
- **Resultado:** 435 linhas / 5915 palavras. Abre com o bug de recriar `ClientSession` a cada requisição (perde connection pooling, paga handshake TCP+TLS repetido) e o warning `Unclosed client session`; cobre concorrência real via `gather`/`TaskGroup` sobre sessão compartilhada (aplicando, não reexplicando, o Galho 7 nota 07), `ClientTimeout` (`total` vs. `connect`/`sock_read` granular), hierarquia de `aiohttp.ClientError` vs. `TimeoutError` nativo (armadilha do `except` que não captura timeout), e `response.content.iter_chunked()` para streaming sem carregar tudo em memória.

#### 04 - aiohttp servidor — web.Application, routing e middlewares
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** `web.Application`, rotas (`add_get`/`add_post`/decorators), handlers assíncronos, middlewares (logging, auth básica, tratamento de exceção centralizado), `web.run_app`, contraste com frameworks WSGI síncronos (Flask/Django clássico) em termos de modelo de concorrência.
- **Resultado:** 431 linhas / 5005 palavras. Abre com o bug de chamar um SDK legado síncrono (bloqueante) dentro de um handler `async def`, travando o event loop inteiro e paralisando TODAS as conexões concorrentes, não só a requisição atual; cobre `RouteTableDef`/`app.router.add_get`/`add_post`, handlers com `web.Response`/`web.json_response`, middlewares `@web.middleware` encadeados (logging, tratamento de exceção centralizado distinguindo `web.HTTPException` de erro genérico, auth via header com `request[...]` propagando contexto), `web.run_app()` (event loop, socket, sinais `SIGINT`/`SIGTERM`, graceful shutdown embutido), e o contraste de modelo de concorrência com WSGI síncrono (1 worker bloqueado = isolado vs. 1 processo aiohttp bloqueado = todas as conexões param), com o fix via `asyncio.to_thread()`.

#### 05 - ASGI e o ecossistema de frameworks assíncronos
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** o protocolo ASGI (spec, `scope`/`receive`/`send`), por que ele existe (WSGI é síncrono por design, não dá pra fazer WebSocket/long-polling nativamente), quem implementa ASGI (Uvicorn/Hypercorn como servidores, Starlette/FastAPI como frameworks), panorama do ecossistema sem se aprofundar em nenhum framework específico (fronteira explícita: FastAPI em detalhe é Galho 10).
- **Resultado:** 333 linhas / 5255 palavras. Abre com o bug de tentar WebSocket dentro de uma view Flask/WSGI (função síncrona que só devolve uma resposta, sem como manter a conexão trocando eventos ao longo do tempo); implementa uma aplicação ASGI crua (`async def app(scope, receive, send)`, sem framework nenhum, rodável via `uvicorn`) cobrindo `http` e `lifespan`; detalha os três tipos de `scope` (`http`/`websocket`/`lifespan`) com tabela de eventos, o contraste estrutural WSGI vs. ASGI (thread bloqueada por requisição vs. event loop único cooperativo), o mapa servidores (Uvicorn/Hypercorn/Daphne) vs. frameworks (Starlette como camada mínima, FastAPI = Starlette+Pydantic), e a nuance real de que `aiohttp` (nota 04) não é ASGI — tem sua própria API de servidor, não intercambiável com o ecossistema Uvicorn/Starlette/FastAPI.

#### 06 - Back-pressure — Semaphore, Queue com maxsize e buffering
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** o problema de back-pressure (produtor mais rápido que consumidor, memória crescendo sem controle), `asyncio.Semaphore` para limitar concorrência (ex: N requisições HTTP simultâneas), `asyncio.Queue(maxsize=N)` como buffer limitado (retomando `asyncio.Queue` do Galho 7 nota 07 sem repetir a API básica), padrão de rate limiting simples.
- **Resultado:** 431 linhas / 6318 palavras. Abre com o bug de disparar 10.000 requisições via `asyncio.gather()` sem limite nenhum (estoura file descriptors locais e aciona rate-limit/bloqueio do fornecedor remoto); cobre back-pressure em termos gerais (as 3 respostas possíveis a um produtor mais rápido — acumular sem limite, descartar, ou propagar a lentidão de volta), `asyncio.Semaphore(N)` como limitador de concorrência aplicado ao fix do bug de abertura (conectando com a nota 03/aiohttp cliente) + `BoundedSemaphore` como variante que detecta `release()` em excesso, `asyncio.Queue(maxsize=N)` como buffer com capacidade máxima (incluindo `task_done()`/`join()` e o padrão worker pool com múltiplos consumidores na mesma fila), tabela de decisão Semaphore vs Queue, e um `LimitadorDeTaxa` simplificado (token bucket) combinando Semaphore + intervalo mínimo para rate limiting real. Referencia `writer.drain()` (nota 02) como o mesmo princípio em nível de socket, sem repetir o mecanismo.

#### 07 - Padrões de produção com asyncio — supervisão de tasks, graceful shutdown, circuit breaker
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** supervisão de tasks de longa duração (task que morre silenciosamente por exceção não tratada — `asyncio.ensure_future`/callbacks de erro), graceful shutdown (capturar `SIGTERM`/`SIGINT`, cancelar tasks em andamento e aguardar limpeza), circuit breaker assíncrono (padrão simples de estado aberto/fechado/half-open para proteger chamadas externas instáveis).
- **Resultado:** 488 linhas / 5578 palavras. Abre com o bug clássico de produção — uma `asyncio.create_task()` "fire-and-forget" cujo consumidor de fila de e-mails morre silenciosamente na primeira exceção não tratada, sem log nenhum, só um warning tardio de `Task exception was never retrieved` no `__del__`; cobre supervisão via `add_done_callback()` (detectar e logar) e um loop supervisor que recria a task com teto de tentativas consecutivas (recuperar automaticamente), graceful shutdown via `loop.add_signal_handler()` + `asyncio.Event` (handler síncrono só sinaliza, corrotina faz a sequência ordenada parar-de-aceitar→cancelar-com-timeout→limpar-recursos), e um circuit breaker assíncrono mínimo e funcional (fechado/aberto/meio-aberto, com `asyncio.Lock` protegendo as transições de estado) protegendo uma chamada externa instável. Dois diagramas Mermaid (stateDiagram do supervisor recriando a task, stateDiagram do circuit breaker) mais um sequenceDiagram do graceful shutdown.

#### 08 - Capstone — web scraper assíncrono de produção
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** recapitula o galho num scraper real: `aiohttp.ClientSession` (nota 03) + `Semaphore` para limitar concorrência (nota 06) + tratamento de erro e retry + graceful shutdown ao receber `SIGINT` (nota 07) + streams se aplicável. Cenário prático integrador, não introduz conceito novo raso.
- **Resultado:** 551 linhas / 6139 palavras. Constrói um `ScraperAssincrono` completo e rodável em quatro etapas: `ClientSession` reutilizada + `asyncio.Semaphore(N)` limitando concorrência real (aplicando notas 03/06 sem repetir a API básica); retry com backoff exponencial combinado a um `CircuitBreaker` de três estados (fechado/aberto/meio-aberto, `asyncio.Lock` protegendo transições) que falha rápido quando o alvo falha em série; supervisão de cada task via `add_done_callback()` (uma exceção não prevista é logada, não derruba as outras); graceful shutdown via `loop.add_signal_handler()` + `asyncio.Event`, com a nuance de exigir `await asyncio.sleep(0)` entre disparos para o signal handler ter chance de rodar antes que todas as tasks já tenham sido criadas, `asyncio.wait(..., timeout=...)` para drenar com teto de tempo, e persistência de URLs pendentes num JSON de progresso parcial para retomada. Um diagrama Mermaid (flowchart) do fluxo completo. Fecha o galho com recap das 8 notas e aponta pro Galho 9 (Persistência) e de volta pro Galho 7 (Concorrência e paralelismo) como par que fecha o bloco de concorrência/execução.

## Decisões e fronteiras registradas

- Fundamentals de asyncio (event loop básico, coroutines, `Task`, `gather`, `TaskGroup`, cancelamento) → Galho 7 notas 06-07, não repetidos aqui.
- FastAPI/Django/Flask em profundidade (routing de aplicação, serialização, validação Pydantic aplicada) → Galho 10 (Web e APIs REST); aqui ASGI é só o protocolo conceitual.
- `multiprocessing`/`concurrent.futures`/threading → Galho 7, não repetidos aqui.
