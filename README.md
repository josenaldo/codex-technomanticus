---
title: Codex Technomanticus
type: moc
publish: true
---
# Codex Technomanticus

## Grimório Tecnomântico do Arquimago Multiplanar

### Engenharia de software é magia aplicada à realidade digital

**Magia, para mim, é isto: a arte de converter intenção em alteração da realidade por meio de fórmulas precisas, símbolos verificáveis e rituais de entrega.**

Quando me deparei com essa definição, percebi que ela descrevia com precisão o que fazemos em engenharia de software. Partimos de uma ideia abstrata, traduzimos essa intenção em linguagens e símbolos, aplicamos artefatos, rituais e práticas, e então produzimos efeitos concretos no mundo real.

Essa definição me lembra de uma frase de um certo escritor de ficção científica:

> "Qualquer tecnologia suficientemente avançada é indistinguível da magia"
>
> - Arthur C. Clarke

A frase de Arthur C. Clarke reforça essa intuição: quanto mais sofisticada a tecnologia, mais ela parece misteriosa para quem observa de fora, ao ponto em que ela se torna indistinguível de magia. E, no contexto atual, com os avanços da IA, essa impressão se intensificou. Sistemas que aprendem, raciocinam e criam tornaram comum algo que há poucas décadas parecia ficção. Fazer sofetware hoje é quase mágico.

É nesse ponto que a metáfora se fecha: desenvolvimento de software, especialmente na era da IA, é uma forma de tecnomancia. Engenheiros são os magos modernos, alterando a realidade com método, linguagem e disciplina.

### Evergreen Notes

Se a prática é tecnomântica, o registro também precisa ser vivo. Para isso eu uso o que, descobri recentemente, é chamado *Evergreen notes*: notas atemporais, escritas para serem revisitadas, refinadas e reutilizadas.

A ideia é começar com notas simples, que capturam insights, referências e práticas. Com o tempo, essas notas são revisitadas, expandidas, corrigidas e organizadas. Elas são "cultivadas", de forma a se manterem sempre verdejantes, frescas, ou seja "sempre verdes" (em tradução livre).

Elas se tornam um repositório de conhecimento vivo, que reflete a evolução do entendimento e da prática. Não são rascunhos descartáveis: são conhecimento cultivado.

### Commonplace Book

O cultivo pode levar a vários formatos, mas o que eu uso, e também aprendi recentemente, é o *commonplace book*: um caderno de pensamentos, referências, sínteses e aprendizados organizados para consulta futura.

Na prática, ele funciona como um repositório pessoal de longo prazo: um lugar para registrar ideias, conectar conceitos e voltar às notas com contexto suficiente para evoluí-las.

### Grimório

Como leitor de fantasia e ficção científica, o termo que melhor traduz o uso prático desse conhecimento para mim é **grimório**: o livro de feitiços onde o mago registra as fórmulas que realmente funcionam, os rituais que produzem efeitos concretos e as combinações de símbolos que alteram a realidade de forma previsível. Este caderno digital cumpre exatamente esse papel: um grimório de engenharia, onde cada nota nasce de pesquisa, estudo, prática, revisão, erro, acerto e lapidação contínua.

Este não é um repositório-vitrine. Não é portfólio nem currículo. É meu grimório de engenharia full-stack: um compêndio pessoal dos temas que estudo, pratico e refino ao longo dos anos.

Também é um grimório comunitário, pois compartilho com colegas, amigos e a comunidade em geral. Acredito que conhecimento é mais poderoso quando circula, e este vault é uma forma de contribuir para o ecossistema de aprendizado em engenharia de software.

E é por isso que o nome deste projeto é **Codex Technomanticus**. "Codex" porque este vault é um compêndio vivo; "tecnomântico" porque o foco é transformar conhecimento técnico em prática que altera a realidade; e "Arquimago Multiplanar" como uma forma simbólica de dizer o que faço em engenharia full-stack: transitar entre múltiplos planos do sistema (fundamentos, backend, frontend, dados, infraestrutura, IA e arquitetura), conectando tudo de ponta a ponta com coerência.

A todos que chegarem aqui, sejam bem-vindos ao meu **Codex Technomanticus — Grimório Tecnomântico do Arquimago Multiplanar**. Que ele seja útil para sua jornada de aprendizado e prática, e que o conhecimento aqui registrado se transforme em magia aplicada no mundo real.

---

## As 5 zonas do grimório

O conteúdo flui em cinco zonas numeradas, do bruto ao curatorial:

- **`00-Meta/`** — meta-linguagem do codex: `guia/` (8 arquivos cobrindo estrutura, fluxo, convenções, manutenção, publicação, decisões e dicionário), `templates/` Templater, `mestres/` (referências de devs)
- **`01-Pergaminhos/`** — links brutos coletados (`entradas.md`), wishlist (`avaliar.md`), recursos incipientes (Brag Document, listas de cursos)
- **`02-Glosas/`** — fichamentos de artigos lidos (uma ficha por leitura, formato `<ano>-<slug>.md`)
- **`03-Domínios/`** — conhecimento integrado e evergreen, organizado por área (Java, IA, Arquitetura, Entrevistas, etc.)
- **`04-Sendas/`** — caminhos curatoriais que sequenciam Domínios pra atender objetivos (Senda Entrevistas, Senda Frontend, etc.)

Detalhes em [[Como usar este vault]] e [[workflow]].

## Captura e destilação — skill `/glosa`

Pra reduzir o atrito do "li algo, quero guardar":

- Cole o link em `01-Pergaminhos/entradas.md` quando aparecer
- Quando ler, invoque `/glosa <url>` — a skill faz o WebFetch, gera fichamento estruturado em `02-Glosas/`, e remove o link de Pergaminhos automaticamente
- Você só preenche **Meu comentário** (sua reação genuína) e **Ver também** (wikilinks pra Domínios)

Limitação atual: só artigos web (HTML). PDFs, YouTube, podcasts, redes sociais avisam e abortam.

---

## Ritual de navegação

Cada Domínio em `03-Domínios/` tem um portal de entrada (MOC com mesmo nome da pasta). Se estiver chegando agora, comece por esses portais.

> Veja também [[Como usar este vault]] e [[Senda Entrevistas]].

---

## Domínio dos Fundamentos

- [[Fundamentos]]
- [[Algoritmos]] · [[Estruturas de Dados]] · [[Banco de dados]] · [[Orientação a Objetos]] · [[Testes]] · [[Redes e Protocolos]]

## Domínio da Arquitetura

- [[Arquitetura]]
- [[Arquitetura de Software]] · [[System Design]] · [[Design Patterns]] · [[API Design]]
- **Mensageria:** [[Mensageria]] · [[Event Streaming]] · [[03-Dominios/Java/Backend/Kafka/Kafka]] · [[RabbitMQ]] · [[BullMQ]]
- [[Event Storming]] · [[Gateway de Pagamento]]

## Domínio de Java

- [[Java]]
- **Core:** [[Java Fundamentals]] · [[Java Concurrency]] · [[Certificação Java OCP]] · [[Helsinki MOOC - Guia de Revisão]]
- **Backend:** [[Spring Boot]] · [[Spring Data JPA]] · [[Spring Security]] · [[03-Dominios/Java/Backend/Kafka/Kafka]] · [[Testes em Java]] · [[gRPC e Go]]
- **Frontend:** [[JavaFX]]

## Domínio de JavaScript

- [[03-Dominios/JavaScript/index]]
- **Core:** [[JavaScript Fundamentals]] · [[TypeScript]] · [[Testes em JavaScript]]
- **Backend:** [[Node.js]]
- **Frontend:** [[React]] · [[React Red Flag Manual]] · [[HTML e CSS]] · [[Bootstrap]] · [[Material UI]] · [[03-Dominios/React/Mantine]]
- **Revisão:** [[Full Stack Open - Guia de Revisão]]

## Domínio de Python

- [[Python]]
- **Backend:** [[Python Backend]]
- **Setup:** [[Instalando Anaconda no Ubuntu]]

## Domínio de Go

- [[Go]]
- **Backend:** [[Go Backend]] · [[gRPC e Go]]

## Domínio de Inteligência Artificial

- [[03-Dominios/IA/index|IA]] — portal do domínio com 10 trilhas + overview + ferramentas
- **[[03-Dominios/IA/index|Formação Engenheiro de IA]]** — programa estruturado: 10 trilhas + 4 sendas transversais (Praticante, Arquiteto, Líder Técnico, Open Source)
- **Trilhas atomizadas:**
    - [[Anatomia dos LLMs]] (17 notas) — fundamentos: tokens, atenção, modelos, APIs, treino, evaluation
    - [[Anatomia de Agents]] (9 notas) — fundamentos genéricos: ciclo, tools, memory, planning, multi-agent
    - [[Agentes de Codificação]] (18 notas) — Cursor, Claude Code, Copilot, Aider, MCP
    - [[Economia de Tokens]] (20 notas) — prompt caching, pruning, sub-agents, ROI
    - [[Context Engineering]] (16 notas) — pipelines, camadas, JIT, prompting, skills
    - [[Spec-Driven Development]] (12 notas) — Specify→Plan→Tasks→Implement, Kiro, Spec Kit
    - [[Segurança e Guardrails]] (12 notas) — SAST, sandbox, slopsquat, EU AI Act
    - [[Memória de Agentes]] (23 notas) — Letta, Mem0, Zep, Generative Agents, A-MEM
    - [[RAG e Vector Databases]] (13 notas) — embeddings, chunking, retrieval, reranking, evaluation
    - [[MCP]] (10 notas) — Model Context Protocol, servers, segurança, ecossistema
- **Overview:** [[03-Dominios/IA/index|Inteligência Artificial]] — portal panorâmico do campo
- **Ferramentas:** [[03-Dominios/IA/Ferramentas de IA/index|Ferramentas de IA]] — [[Claude]] · [[GitHub Copilot]] · [[Codex]] · [[Gemini]] · [[Comparativo de LLMs]]

## Domínio de Infraestrutura

- [[Infraestrutura]]
- **Containers:** [[Docker]] · [[Comandos Docker e WSL]] · [[Docker credential helpers]] · [[Kubernetes]] · [[WSL, Docker e Kubernetes]]
- **Servidores e cloud:** [[Nginx]] · [[Digital Ocean]]
- **Linux/Terminal:** [[Linux]] · [[Terminal]] · [[Configurando Ambiente Linux no WSL]]
- **CI/CD e operação:** [[CI-CD]] · [[Observabilidade]] · [[GitHub CLI]]

## Domínio de Inglês

- Notas de estudo de inglês para entrevistas internacionais (em `03-Domínios/Inglês/`)

## Domínio de Entrevistas

- **Senda guia:** [[Senda Entrevistas]]
- **Notas de prep:** [[Behavioral Questions]] · [[STAR Method]] · [[Coding Challenges Strategy]] · [[System Design Practice]] · [[Communicating Trade-offs]]

## Domínio de RPA

- [[RPA]] — Robotic Process Automation
- [[Building Your First Automation Bot]] · [[Identifying Use Cases for Creating Bots]]

## Domínio de Ferramentas

- [[Ferramentas]]
- [[Versionamento]] · [[Atalhos do IntelliJ]] · [[Prompts]]

## Sendas (caminhos curatoriais)

- [[Sendas]] — MOC de todas as sendas
- **Stacks:** [[Senda Java]] · [[Senda JS-TS]] · [[Senda Python]] · [[Senda Go]]
- **Camadas:** [[Senda Backend]] · [[Senda Frontend]] · [[Senda Fullstack Java-Spring + TS-React-Nextjs 15]] · [[Senda Cloud]] · [[Senda Devops]]
- **Domínio:** [[Senda IA]] · [[Senda Entrevistas]]

## Mestres

- [[Mestres Jedi]] — desenvolvedores e referências (em `00-Meta/mestres/`)

## Recursos e curadoria

- [[Brag Document]] · [[Cursos completos]] · [[Courses]] · [[Curso Fullcycle 3.0]] (em `01-Pergaminhos/recursos/`)

## Guia do vault

A pasta `00-Meta/guia/` reúne toda a meta-documentação do Codex:

- [[Como usar este vault]] — mapa estático: zonas, navegação, templates
- [[workflow]] — pipeline cognitivo e skill `/glosa`
- [[Convenções de escrita]] — filename, frontmatter, status, tags, atomicidade
- [[Wikilinks e MOCs]] — boas práticas de linking e índices
- [[Manutenção do vault]] — rotinas de processamento e revisão
- [[Publicação]] — pipeline Quartz e isolamento público/apocrypha
- [[Decisões do vault]] — registro de decisões de design (ADRs leves)
- [[Dicionario de Magia Tecnomante]] — vocabulário do grimório
