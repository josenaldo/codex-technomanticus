---
title: "Roadmap — Python Arquitetura e Design Patterns"
created: 2026-07-12
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Arquitetura e Design Patterns (galho 13)

Roadmap-folha do galho `Python/Arquitetura e Design Patterns`. Fase **Magus** — por que GoF clássico é menos necessário em Python; Repository/UoW, DI, hexagonal/clean architecture (Percival & Gregory). Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Testes/index.md` e `Python/Testes/roadmap.md` (galho anterior, mesmo padrão).

Roster **não pré-cravado no spec** (só a descrição de alto nível) — desenhado nesta sessão seguindo o mesmo playbook dos Galhos 5, 7, 8, 9, 10, 11 e 12. Quinto e último galho do bloco **"Backend e arquitetura"** (9-13) — fecha esse bloco antes da trilha entrar em plataforma distribuída/produção (14-18).

**Fronteira cravada:** GoF clássico (Engenharia/Design de Software), SOLID (mesma pasta), arquitetura hexagonal como estilo teórico (Engenharia/Arquitetura) — todos referenciados, nenhum reensinado. Este galho aplica **Architecture Patterns with Python** (Percival & Gregory) ao código real dos Galhos 9-12: `Session` do Galho 9 já era informalmente uma Unit of Work; a capstone do Galho 12 já apontou isso — este galho formaliza.

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

#### 01 - Por que GoF clássico é menos necessário em Python
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Escopo:** por que boa parte do catálogo GoF (Strategy, Command, Observer, Iterator, alguns casos de Factory) fica menos necessária quando a linguagem já tem first-class functions (uma função É um Strategy), duck typing (não precisa de interface explícita pra polimorfismo), decorators (substituem boa parte de Decorator/Proxy formal), e generators/protocolo iterator (Iterator já é built-in, coberto no Galho 4). Não desenvolve cada pattern do zero — referencia [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Clássicos (GoF)/index|Design Patterns (GoF)]] pra quem quiser a versão clássica, e mostra o CONTRASTE: a mesma solução em Java com classe+interface vs. em Python com função/closure.
- **Resultado:** 482 linhas / 4928 palavras. Abre com `DiscountStrategyFactory` java-like (interface+3 classes+factory) vs dict de lambdas de 7 linhas em Python; desenvolve Strategy/Command/Iterator/Decorator(GoF vs sintático, com desambiguação explícita)/Factory lado a lado, fecha com Adapter/Singleton ainda relevantes e tabela de decisão.

#### 02 - Domain modeling — separando a lógica de negócio do framework
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Escopo:** o problema de lógica de negócio espalhada dentro de handlers FastAPI/models SQLAlchemy (acoplamento ao framework), Value Objects vs Entities (distinção conceitual, referenciando OO do Galho 3 sem repetir dunder methods), o domínio como Python puro — classes/dataclasses que não sabem nada sobre HTTP nem sobre banco, testáveis sem subir nenhum dos dois (referenciando a nota 01 do Galho 12 sobre testes unitários).
- **Resultado:** 495 linhas / 5504 palavras. Abre com regra "sem subtarefa pendente" só no handler, ignorada por um job de background gravando direto no ORM; extrai `Tarefa` de domínio puro com exceção própria; Entity (`Tarefa`, `__eq__` por id) vs Value Object (`PeriodoDeTempo` frozen dataclass); diagrama antes/depois de lógica duplicada.

#### 03 - Repository pattern — abstraindo a persistência
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Escopo:** o Repository como abstração entre o domínio e a persistência (uma interface `abc.ABC` com `add`/`get`, uma implementação `SqlAlchemyRepository` por trás — referenciando a mecânica de `Session` do Galho 9 nota 02 sem repetir), por que isso desacopla o domínio do SQLAlchemy (testável com um `FakeRepository` em memória, referenciando mocking do Galho 12 nota 04 como contraste — Repository é uma alternativa arquitetural a mockar o ORM em todo teste).
- **Resultado:** 436 linhas / 4747 palavras. Abre com suíte de Service Layer frágil por mockar `Session.query().filter().join()...` encadeado; `AbstractRepository`/`SqlAlchemyTarefaRepository`/`FakeRepository` com código real, contraste tabelado com mocking do ORM, 3 armadilhas (ORM vazando pela interface, `find(**filtros)` genérico demais, drift Fake/real), ressalva honesta de custo/benefício citando Percival & Gregory.

#### 04 - Unit of Work — formalizando o padrão que já existia
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 438 linhas / 5170 palavras. Abre com mover tarefa entre usuários + criar notificação via 2 commits separados, conexão cai no meio, estado inconsistente; `AbstractUnitOfWork`/`SqlAlchemyUnitOfWork` (1 Session, commit único) com sequenceDiagram; `FakeUnitOfWork`; ressalva honesta sobre atomicidade só dentro de 1 transação (outbox/saga fora do escopo).
- **Escopo:** nomeia e generaliza o que a `Session` do SQLAlchemy já fazia informalmente (Galho 9 nota 02) — um `AbstractUnitOfWork` com `__enter__`/`__exit__`/`commit`/`rollback`, agrupando um ou mais Repositories numa única transação atômica, e por que isso separa "o que muda" (domínio) de "quando persiste" (UoW) — referenciando transações do Galho 9 nota 06 sem repetir isolation levels.

#### 05 - Injeção de dependência como princípio — sem framework pesado
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 402 linhas / 4724 palavras. Abre com dev de Spring perguntando "onde está o container de DI"; distingue princípio de mecanismo, composition root decidindo `SqlAlchemyUnitOfWork` vs `FakeUnitOfWork`, `dependency-injector` como exceção não-norma, `Protocol` vs `ABC` pro contrato de dependência.
- **Escopo:** DI como PRINCÍPIO (inverter quem decide a implementação concreta, não quem escreve `import`) vs. `Depends()` do FastAPI como MECANISMO (já ensinado no Galho 10 nota 04, só referenciado aqui). Contraste com frameworks DI pesados de outras linguagens (Spring `@Autowired`, referenciando a trilha Java se fizer sentido) — Python geralmente resolve isso com composição simples no bootstrap da aplicação (`main.py` decide qual Repository/UoW concreto injetar), sem container de DI dedicado.

#### 06 - Service Layer — orquestrando casos de uso
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 527 linhas / 6998 palavras. Abre com worker de fila reusando lógica de criação de tarefa só copiando o handler gordo inteiro; extrai `CriarTarefaComando`/`ConcluirTarefaComando` (dataclasses de intenção, tabela das 3 responsabilidades vs Pydantic vs domínio), handler final de 3 linhas, contraste `FakeUnitOfWork` (regra de negócio) vs `TestClient` (integração).
- **Escopo:** a camada entre o handler HTTP (Galho 10) e o domínio (nota 02) — uma função de caso de uso (`criar_tarefa(cmd, uow)`) que orquestra Repository+UoW+domínio, deixando o handler magro (só parse de request/response). Contraste explícito com o handler "gordo" que apareceu nas capstones dos Galhos 10-12 (lógica de negócio misturada com FastAPI/SQLAlchemy) — este é o refactor que a capstone do Galho 12 já previu.

#### 07 - Arquitetura hexagonal e Ports and Adapters em Python
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Resultado:** 447 linhas / 5051 palavras. Abre com requisito "notificar por Slack também" mostrando duplicação sem fronteira; introduz `AbstractNotificador` como novo Port de saída (distinto do `AbstractNotificacaoRepository` da nota 04), `EmailAdapter`/`ConsoleAdapter`/`SlackAdapter`; diagrama hexagonal central da API de Tarefas inteira + sequenceDiagram; tabela cruzando cada conceito hexagonal com onde já foi construído (notas 02-06).
- **Escopo:** aplica o estilo hexagonal (referenciando [[03-Dominios/Engenharia/Arquitetura/index|Engenharia/Arquitetura]] como teoria, sem repetir) ao código Python concreto — Ports (interfaces abstratas: `AbstractRepository`, `AbstractUnitOfWork`) e Adapters (implementações concretas: `SqlAlchemyRepository`, FastAPI como adapter de entrada, um adapter de e-mail/notificação como exemplo de porta de saída). Diagrama da API de Tarefas reorganizada em camadas.

#### 08 - Capstone — refatorando a API de Tarefas pra arquitetura hexagonal
- **Estado:** ✅ feita (2026-07-12) · fase: Magus
- **Escopo:** recapitula o galho pegando a API de Tarefas testada na capstone do Galho 12 e refatorando pra arquitetura hexagonal — extrai o domínio (nota 02), introduz Repository (03) e Unit of Work (04) formais, move lógica de negócio pra Service Layer (06), reorganiza em Ports and Adapters (07), com os testes do Galho 12 confirmando que o comportamento não mudou (só a forma). Cenário prático integrador. Fecha o bloco "Backend e arquitetura" (9-13) e aponta para o Galho 14 (Mensageria) como próximo passo — Domain Events, que aparecem naturalmente numa arquitetura hexagonal madura, são o gancho pra mensageria assíncrona.
- **Resultado:** 752 linhas / 7031 palavras. 7 passos amarrando as 7 notas anteriores: extração do domínio, Repository, UoW, composition root, Service Layer, Ports/Adapters formais. Passo 7 é o clímax: os 42 testes da capstone do Galho 12 (incluindo Broken Access Control/SSTI/rate limiting) rodam SEM MODIFICAÇÃO contra o código refatorado — prova viva de teste-de-comportamento sobrevivendo a refactor interno. 5 diagramas Mermaid. Fecha o galho E o bloco "Backend e arquitetura" (9-13) inteiro.

> [!success] Galho 13 completo — 8/8 notas (2026-07-12) — fecha o bloco "Backend e arquitetura" (9-13)
> GoF menos necessário em Python (01) → domain modeling puro (02) → Repository (03) → Unit of Work (04) → DI como princípio (05) → Service Layer (06) → arquitetura hexagonal/Ports and Adapters (07) → capstone refatorando a API de Tarefas inteira, com a suíte de testes do Galho 12 sobrevivendo intacta ao refactor (08). Fonte primária: Percival & Gregory, Architecture Patterns with Python. Próximo da trilha: Galho 14 — Mensageria (abre o bloco "Plataforma distribuída e produção").

## Decisões e fronteiras registradas

- Padrões GoF clássicos (Strategy, Observer, Factory, Adapter, etc.) → [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Clássicos (GoF)/index|Design Patterns (GoF)]]; aqui só o contraste de por que menos necessários em Python.
- SOLID → [[03-Dominios/Engenharia/Design de Software/SOLID/index|SOLID]]; referenciado, não repetido.
- Arquitetura hexagonal/Ports and Adapters como estilo arquitetural teórico → [[03-Dominios/Engenharia/Arquitetura/index|Engenharia/Arquitetura]]; aqui é a aplicação Python concreta.
- Mecânica de `Session`/`Engine`/transações → Galho 9; aqui formaliza o padrão (Repository/UoW) sem repetir a mecânica.
- `Depends()` do FastAPI → Galho 10 nota 04; aqui DI é discutida como princípio, não como sintaxe.
- Mocking/testes unitários → Galho 12; aqui Repository é apresentado como alternativa arquitetural a mockar o ORM em todo teste, sem repetir a mecânica de `unittest.mock`.
- CQRS e Domain Events em profundidade → fora do escopo deste galho (mencionados de leve na capstone como gancho pro Galho 14, não desenvolvidos).
