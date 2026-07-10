---
title: "Design Spec — Trilha Python"
created: 2026-07-09
type: meta
publish: false
tags:
  - meta
  - spec
  - python
---

# Design Spec — Trilha Python

> Cobertura ausente adicionada ao [[00-Meta/Roadmap]] em 2026-07-09 (junto com Go). Escala e método iguais à trilha [[03-Dominios/Tecnologia/Java/index|Java]] (18→19 galhos): profundidade didática do básico (Iniciado) ao avançado (Magus), POV fullstack backend. **IA-com-Python fica fora do escopo** — vai virar parte de uma trilha futura cross-language (Java/Go/Python/JS) para IA, ainda não desenhada.

## Ponto de vista (travado com o usuário 2026-07-09)

Trilha **didática de ponta a ponta**, não uma trilha de "tradução rápida" como as notas de fronteira em [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] (que só citam Python en passant). Aqui o galho é a casa canônica da linguagem — mesmo nível de profundidade e mesmo padrão estrutural do Java: notas atômicas numeradas, 3 fases (Iniciado/Adepto/Magus), seção "Em entrevista", frontmatter com `fase:`.

Consequências:
- **Do zero ao avançado dentro de cada galho de linguagem** (galhos 1-6) — diferente das trilhas de System Design/Operação/Comunicação, que assumem sênior. Aqui o leitor pode estar pegando Python pela primeira vez.
- **POV fullstack backend** nos galhos de framework/persistência/arquitetura (9-15): Django, FastAPI, SQLAlchemy — não cobre data science/ML/notebooks.
- **Links de referência sempre que possível** — Real Python, material do Dunossauro (FastAPI do Zero), e os livros-fonte (ver "Fontes canônicas") citados nota a nota, não só na seção de Recursos.

## Pesquisa prévia — mercado e fontes (2026-07-09)

- **Fontes do usuário:** stub atual (`Python.md`/`Python Backend.md`/`Instalando Anaconda no Ubuntu.md`), `04-Sendas/Senda Python.md` (lista de cursos/vídeos — mesmo conteúdo do export Notion fornecido, nada adicional), Real Python (realpython.com), material do Dunossauro (FastAPI do Zero, exercícios), livro **Python Fluente** (Ramalho).
- **Pesquisa de mercado (WebSearch):** cursos BR mais recomendados hoje cobrem Django/DRF/FastAPI com foco em API/backend (Codar.me, Academify) e TDD/Clean Code/deploy (Python Pro — Renzo Nuccitelli) — confirma os galhos 10-13 e 17.
- **Lacuna encontrada e incorporada:** **Architecture Patterns with Python** (Percival & Gregory) aparece constantemente ao lado de *Effective Python* (Slatkin) e *High Performance Python* (Gorelick/Ozsvald) como leitura essencial de sênior — cobre Repository/Unit of Work, DDD, hexagonal/clean architecture, arquitetura orientada a eventos. Motivou o **galho 13 novo** (Arquitetura e Design Patterns em Python), ausente do rascunho inicial. O mesmo autor tem *Test-Driven Development with Python* — reforça o galho 12 (Testes).

## Contexto: o que já existe

`03-Dominios/Tecnologia/Python/` hoje é uma estante rasa: `Python.md` (24 ln, MOC redundante), `Python Backend.md` (297 ln — mistura Django/FastAPI/troubleshooting de produção sem estrutura de fase), `Instalando Anaconda no Ubuntu.md` (setup). Sem nenhum padrão de galho/fase — equivalente ao estado do Java antes da reforma (`Java Fundamentals.md`, `Java Concurrency.md` como troncos).

## Estrutura de pastas

Mesmo padrão do Java: **galhos flat** sob `Tecnologia/Python/`, sem pasta "Trilha" intermediária. Cada galho tem `index.md` (agrupa notas por fase Iniciado/Adepto/Magus + rotas alternativas de leitura + dataview) e `roadmap.md` (roadmap-folha, convenção atual do vault — ver [[project_roadmap_tree]]). Um `roadmap.md` de nível Python/ (galho-pai) mapeia o estado dos 19 galhos.

```
Tecnologia/Python/
├── index.md            (MOC — lista os 19 galhos, mesmo padrão do Java/index.md)
├── roadmap.md           (roadmap recursivo do domínio)
├── Core/
├── Collections e Comprehensions/
├── OO e Data Model/
├── Funcional e idiomas avançados/
├── Tipagem moderna/
├── CPython internals/
├── Concorrência e paralelismo/
├── Programação Reativa e Assíncrona/
├── Persistência de dados/
├── Web e APIs REST/
├── Segurança/
├── Testes/
├── Arquitetura e Design Patterns/
├── Mensageria/
├── Microservices e sistemas distribuídos/
├── Build e tooling/
├── Observabilidade e produção/
├── Cloud-native e produção/
└── Certificação (PCEP-PCAP)/
```

`Python Backend.md` vira tronco podado quando os galhos 9-11/17 absorverem o conteúdo (troubleshooting de produção → Observabilidade; Django/FastAPI → Web e APIs REST). `Instalando Anaconda no Ubuntu.md` permanece como referência de setup (fora do escopo didático).

## Roster de galhos (19, ~250-300 notas planejadas ao todo — escala Java)

### Núcleo da linguagem (Iniciado→Adepto)

| # | Galho | Fase predominante | Escopo |
|---|-------|-------------------|--------|
| 1 | Core | Iniciado | Sintaxe, tipos, controle de fluxo, funções, erros/exceções, módulos/imports |
| 2 | Collections e Comprehensions | Iniciado→Adepto | list/dict/set/tuple, comprehensions, itertools, desempacotamento |
| 3 | OO e Data Model | Adepto | Classes, dunder methods, properties, dataclasses, ABC/Protocol — coração do Python Fluente |
| 4 | Funcional e idiomas avançados | Adepto→Magus | Generators, iterators, decorators, closures, context managers, functools |
| 5 | Tipagem moderna | Adepto | Type hints, mypy/pyright, Pydantic, structural typing (Protocol) |
| 6 | CPython internals | Magus | GIL de verdade, memory management, GC, profiling — equivalente ao galho JVM do Java |

### Concorrência e execução (Adepto→Magus)

| 7 | Concorrência e paralelismo | Adepto→Magus | GIL, threading, multiprocessing, asyncio fundamentals |
| 8 | Programação Reativa e Assíncrona | Magus | asyncio deep-dive, aiohttp, async frameworks, back-pressure |

### Backend e arquitetura (Adepto→Magus, POV fullstack)

| 9 | Persistência de dados | Adepto→Magus | SQLAlchemy, Django ORM, migrations, N+1, transações |
| 10 | Web e APIs REST | Adepto | Django vs FastAPI vs Flask, routing, serialização, validação (Pydantic) |
| 11 | Segurança | Adepto→Magus | Auth (JWT/OAuth), OWASP, validação de input, secrets |
| 12 | Testes | Adepto | pytest, fixtures, mocking, coverage, TDD (Percival) |
| 13 | Arquitetura e Design Patterns | Magus | Por que GoF clássico é menos necessário em Python; Repository/UoW, DI, hexagonal/clean architecture (Percival & Gregory) |

### Plataforma distribuída e produção (Magus)

| 14 | Mensageria | Adepto→Magus | Celery, RQ, aio-pika, kafka-python/aiokafka |
| 15 | Microservices e sistemas distribuídos | Magus | Comunicação entre serviços em Python, cliente de API Gateway |
| 16 | Build e tooling | Iniciado→Adepto | Packaging moderno (uv, poetry), virtual envs, pyproject.toml, ruff/black |
| 17 | Observabilidade e produção | Magus | Logging, OpenTelemetry, WSGI/ASGI (gunicorn/uvicorn), deploy |
| 18 | Cloud-native e produção | Magus | Containers Python, serverless/Lambda Python |

### Certificação (Magus, opcional, planejada por último — mesmo padrão do Java)

| 19 | Certificação (PCEP/PCAP) | Magus | Guia de estudo mapeado aos galhos 1-6 |

## Fronteiras anti-duplicação

| Tópico | Papel aqui | Mora em | Regra |
|--------|-----------|---------|-------|
| SOLID, GoF genérico, arquitetura agnóstica de linguagem | reforço com exemplo Python | [[03-Dominios/Engenharia/Design de Software/index\|Design de Software]] | linkar; galho 13 é a reinterpretação **idiomática Python** (duck typing muda o cálculo de quais patterns fazem sentido) |
| Testes genérico (pirâmide, TDD conceitual) | reforço com pytest | [[03-Dominios/Engenharia/Testes/index\|Testes]] | linkar; galho 12 é ferramental pytest |
| REST/GraphQL/gRPC conceitual, idempotência, versionamento, mensageria conceitual | reforço com implementação Python | [[03-Dominios/Engenharia/Comunicação entre Sistemas/index\|Comunicação entre Sistemas]] | linkar sem reexplicar; galhos 10/14/15 mostram "como isso é em Python" |
| System Design (escala, CAP, patterns) | referência | [[03-Dominios/Engenharia/Arquitetura/System Design/index\|System Design]] | linkar |
| DevOps/observabilidade/deploy genérico | reforço com stack Python | [[03-Dominios/Engenharia/Operação/index\|Operação]] | linkar; galhos 17/18 são a ótica Python |
| Segurança genérica (OWASP Top 10, RBAC/ABAC) | reforço com libs Python | [[03-Dominios/Engenharia/Segurança/index\|Segurança]] | linkar; galho 11 é ferramental |
| IA com Python (LangChain, agentes, RAG) | **fora de escopo** | trilha futura cross-language IA (não existe ainda) | não entrar |

## Padrão de escrita (herdado do Java, adaptado)

Mesmo padrão-mestre de capítulo de livro das outras trilhas, mas replicando a convenção estrutural específica do Java: `index.md` do galho agrupa notas por cabeçalho de fase (`## Iniciado`, `## Adepto`, `## Magus`), oferece **rotas alternativas de leitura** (linear, entrevista internacional, projetando produção, etc. — como o galho Web e APIs REST do Java), e usa dataview pra listar todas as notas. Frontmatter com `fase:`. Seção **"Em entrevista"** obrigatória (mesmo em galhos de fundamentos, ao contrário das trilhas de arquitetura que só têm isso em fases avançadas). Densidade-alvo ~440-540 linhas / 5-7k palavras por nota, ≥1 Mermaid, callouts `[!question]-`/`[!warning]`, `## Fontes` datadas. **Links de referência inline** para Real Python, Dunossauro (FastAPI do Zero), e os livros-fonte sempre que a nota tocar o tema deles — não só na seção Recursos final.

## Fontes canônicas da trilha

- **Livros:** *Python Fluente* / *Fluent Python* 2ª ed. (Luciano Ramalho — fonte central para galhos 3-4); *Effective Python* (Brett Slatkin); *High Performance Python* (Gorelick & Ozsvald); *Architecture Patterns with Python* (Percival & Gregory — fonte central do galho 13); *Test-Driven Development with Python* (Percival — reforço do galho 12); *Fluent Python* já citado cobre também Data Model/descriptors/metaclasses.
- **Online/comunidade:** [Real Python](https://realpython.com/) (fonte primária de artigos por tema); [FastAPI do Zero — Dunossauro](https://fastapidozero.dunossauro.com/); documentação oficial (docs.python.org, PEPs — especialmente PEP 8, PEP 484/type hints, PEP 703/GIL opcional); [SQLAlchemy docs](https://docs.sqlalchemy.org/); [FastAPI docs](https://fastapi.tiangolo.com/); [Django docs](https://docs.djangoproject.com/); Talk Python Training / PyBites como referência complementar.
- **Palestras/vídeos:** palestras do Ramalho já mapeadas em `Senda Python.md` (descritores, geradores, metaprogramação, assíncrono) — usar como fonte quando o tema bater.

## Plano de execução (ritmo Java — um galho por vez, sem branch dedicada)

1. Criar `Tecnologia/Python/index.md` (MOC) + `roadmap.md` (galho-pai) — feito neste spec-turn.
2. Semear **um galho por vez**, ordem sugerida = ordem da tabela (núcleo da linguagem primeiro, produção por último, certificação ao final — mesmo padrão do Java, que também deixou a certificação pro fim). Cada galho: `index.md` + `roadmap.md` + notas via subagente-por-nota (≤3/onda, Sonnet, barra de densidade explícita, WebSearch inline citando Real Python/Dunossauro/livros-fonte).
3. Commit por galho fechado (paths explícitos, sem Co-Authored-By, push manual) — direto na main, sem branch (mesma convenção do Java a partir do Galho 6, ver [[feedback_galhos_direto_main]]).
4. **Esta é uma trilha de múltiplas sessões** (escala Java — semanas, não uma sessão). Cada sessão fecha 1 galho (ou 2 pequenos) e para; não tentar completar tudo de uma vez.
5. Ao fechar cada galho, atualizar roadmap-folha + roadmap-pai + memória.

## Pontos em aberto

- **EXEMPLAR:** usar `Java/Web e APIs REST/index.md` e suas notas 01-05 como referência estrutural até a trilha Python ter seu próprio exemplar consolidado (o Galho 1 — Core — vira o exemplar próprio assim que fechar).
- Destino final de `Python Backend.md`: tronco podado, redistribuído entre galhos 9/10/17 no fechamento de cada um.
- Certificação (galho 19): confirmar se PCEP/PCAP são as certs relevantes (equivalente PCEP≈nível básico, PCAP≈nível associate da Python Institute) antes de escrever — pesquisar no momento de abrir esse galho, não agora.
