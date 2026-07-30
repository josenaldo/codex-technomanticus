---
title: "Roadmap — Aplicação Corporativa"
created: 2026-07-30
type: meta
publish: false
tags:
  - meta
  - roadmap
  - design-de-software
  - padroes-de-projeto
  - aplicacao-corporativa
  - poeaa
---

# Roadmap — Aplicação Corporativa / PoEAA não-dados (galho-folha, construção)

Roadmap da família `03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Aplicação Corporativa`. Galho-**folha em modo construção**: uma entrada por nota **a escrever**. Pai: [[Padrões de Projeto/roadmap|Padrões de Projeto]]. Fonte canônica: **Martin Fowler, *Patterns of Enterprise Application Architecture* (2002)** — a metade **não-dados** do catálogo (a metade de dados é a [[Padrões de Projeto/Acesso a Dados/roadmap|família 2]]).

## Escopo desta família

Os padrões de **estruturação de uma aplicação corporativa** fora da camada de persistência: como a **apresentação web** despacha requisições e monta telas, como a **distribuição** atravessa a fronteira de processo, como a **concorrência offline** protege dados entre requisições sem segurar transação, e os **padrões-base** que aparecem embutidos em todo framework.

## A lente desta família: arqueológica

**Esta é a família mais datada das seis, e isso é a matéria-prima, não um defeito.** O PoEAA foi escrito em 2002 contra J2EE/JSP/WebForms. Boa parte do roster descreve decisões que quase nenhum framework de 2026 ainda oferece como escolha: Spring MVC, Rails e ASP.NET Core já cravaram Front Controller + Template View, e a discussão de session state migrou para JWT × sessão distribuída. Descrever *Two-Step View* como se fosse uma opção viva produziria nota morta.

Por isso a lente **não é cross-framework** (como foi cross-ORM na família 2 e cross-ferramenta na família 3). É **arqueológica**, no eixo **era × hoje**:

> Você abriu um sistema de 2006 e encontrou **isto**. Era a decisão certa naquele contexto — por quê? Onde esse padrão **ressuscitou**, sob que nome? E como se convive com ele, ou se migra?

Casa com a espinha do vault ([[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index|Arqueologia e Restauração de Software]]) e com o ofício de consultor de legado.

**Estrutura interna por camada, sem lente técnica única.** O material é heterogêneo — *Front Controller* e *Money* não se comparam pelo mesmo eixo. Forçar uma lente única produziria contraste artificial. Cada bloco fala o idioma do seu problema.

## A seção "A ressurreição" (decisão de design desta família)

Praticamente todo padrão do roster tem um retorno moderno, e a maioria voltou **por causa** da nuvem — serverless, autoescala e edge desfizeram as premissas de 2002. Isso é sistemático o bastante para virar **seção obrigatória da anatomia**, entre "como a era encarnava" e "Armadilhas":

> **A ressurreição** — onde o padrão reapareceu, sob que nome, e o que mudou no contexto que o tornou viável de novo.

**Regra de honestidade:** cada seção marca explicitamente o que é **correspondência reconhecida** (a comunidade já nomeia a relação) e o que é **leitura deste catálogo** (defensável, mas não canônica). Nunca apresentar interpretação como consenso.

Mapa preliminar (a confirmar nota a nota):

| Padrão | Ressurreição | Status |
|--------|--------------|--------|
| Page Controller | file-based routing (Next `app/`, SvelteKit, Nuxt, Remix, Astro); 1 função serverless por rota | reconhecida |
| Front Controller | mudou de camada: API Gateway, ingress, middleware de edge | reconhecida |
| Remote Facade | **BFF** (Backend for Frontend); aggregation pattern de API Gateway | reconhecida |
| Client Session State | **JWT** — a nuvem inverteu a recomendação de 2002 (sem sticky sessions) | reconhecida |
| Database Session State | session store em Redis/DynamoDB — o default atual | reconhecida |
| Service Stub | service virtualization: MSW, WireMock, LocalStack, Testcontainers | reconhecida |
| Optimistic Offline Lock | condition expressions (DynamoDB), `If-Match`/ETag, `@Version` do JPA | reconhecida |
| Separated Interface | a base de Ports & Adapters / Hexagonal | reconhecida |
| Plugin · Registry | plugins de Vite/esbuild, providers do Terraform; DI containers, service discovery | reconhecida |
| Transform View | **React é Transform View** (função dados→árvore); JSP/ERB eram Template View | leitura |
| Two-Step View | o payload dos **React Server Components** como primeiro estágio | leitura |
| Application Controller | Step Functions, Durable Functions, XState — a máquina de estados virou serviço | leitura |
| Server Session State | Durable Objects / Durable Entities / atores — estado com identidade, agora viável | leitura |
| DTO | mensagem protobuf do gRPC; GraphQL resolve a chatty interface que o motivou | leitura |
| Value Object · Money | records do Java, branded types do TS, newtype do Rust (Valhalla ainda não entregou) | leitura |
| Special Case | `Optional` / `Result` e pattern matching | leitura |
| Coarse-Grained Lock | **sem ressurreição honesta** — sobrevive diluído no agregado do DDD | — |

## Fronteira com a família 2 (Acesso a Dados) — cravada 2026-07-30

Três padrões-base do PoEAA já têm **casa canônica** na família 2 e **não ganham nota nova aqui**:

| Padrão | Casa canônica |
|--------|---------------|
| **Service Layer** | [[Padrões de Projeto/Acesso a Dados/04 - Table Module\|Acesso a Dados/04]] (seção dedicada) |
| **Gateway** | [[Padrões de Projeto/Acesso a Dados/07 - Gateways\|Acesso a Dados/07]] |
| **Mapper** | [[Padrões de Projeto/Acesso a Dados/08 - Data Mapper\|Acesso a Dados/08]] |

Aparecem **em prosa + cross-link** ("a nota canônica é aquela"). Esta é a única redundância que o galho **não** aceita: duas notas disputando o mesmo padrão não é reforço, é contradição. Redundância de *assunto* segue bem-vinda (convenção do vault).

## Anatomia de cada nota

Padrão-capítulo, como nas famílias 1-3, **com a seção nova**:

1. **Cenário no legado** — o que você encontra abrindo o sistema
2. **A ideia** — o padrão em si, com Mermaid
3. **Como a era encarnava** — J2EE/JSP/WebForms/Struts, o contexto que fazia sentido
4. **A ressurreição** ← *nova* — onde voltou, sob que nome, marcando reconhecida × leitura
5. **Armadilhas (reforçada)** — quando NÃO usar, ≥3
6. **O padrão em inglês** + tabela PT↔EN
7. **O que vem a seguir** + **Fontes**

Registro Feynman. Escrever direto, sem gate de aprovação por nota.

**Esquema `fase:`** — alinhado 1:1 com o bloco de camada. Base fica em Magus não por dificuldade conceitual, mas por **frequência de reconhecimento**: identificar que um `AbstractEntity` é Layer Supertype ou que um `Optional` é Special Case é olho treinado, não conteúdo difícil — coerente com a convenção do galho de que `fase:` mede centralidade, não gate de aprendizado.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Notas de conteúdo | 14 |
| Iniciado (Apresentação) | 5 |
| Adepto (Distribuição, estado e concorrência) | 5 |
| Magus (Base) | 4 |
| ✅ escritas | 10 (Iniciado + Adepto) |
| ⬜ pendentes | 4 (bloco Magus) |
| % concluído | 71% |
| Scaffolding | roadmap.md criado (2026-07-30); index.md ao fechar |

---

## Notas — Iniciado (Apresentação: como a requisição vira tela)

#### 01 - Panorama da aplicação corporativa   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: iniciado · 200 linhas
- **Escopo:** o que o PoEAA chama de "aplicação corporativa" (dados persistentes, muitas telas, integração, regras ilógicas de negócio); as **camadas** (apresentação · domínio · fonte de dados) e por que a divisão em 3 é a decisão-mãe; onde esta família fica (não-dados) e onde fica a família 2; o **contexto de 2002** (J2EE, EJB, JSP, Struts, WebForms) que gerou o catálogo; **como ler um legado pelas camadas** — o método arqueológico da família. Mermaid do mapa das 4 camadas do roster. Apresenta a seção "A ressurreição" como fio condutor.

#### 02 - MVC — o padrão mais mal-entendido   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: iniciado · 170 linhas
- **Escopo:** o MVC **original** (Smalltalk-80, Reenskaug 1979: observer, view sincronizada por notificação) × o **MVC web** (request/response, sem observer, "model" virando ora entidade ora camada inteira) × a diáspora **MV\*** (MVP, MVVM, MVI). Por que o mesmo nome cobre coisas diferentes e o custo disso numa conversa de arquitetura. **Armadilhas:** "model" como sinônimo de tabela; controller gordo com regra de negócio; achar que usar um framework MVC dá separação de responsabilidades de graça.

#### 03 - Page Controller × Front Controller   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: iniciado · 169 linhas
- **Escopo:** os dois modos de despachar. **Page Controller** (um controlador por página/ação — o modelo de scripts CGI/ASP/JSP) × **Front Controller** (um ponto único que recebe tudo e delega — o modelo Struts/Spring MVC). Trade-off: duplicação × centralização; onde entra o filtro/interceptor. **Ressurreição forte:** o file-based routing trouxe Page Controller de volta com outro nome, e Front Controller virou infraestrutura (API Gateway, ingress, edge middleware). **Armadilhas:** front controller que vira God dispatcher; page controller com lógica duplicada em N arquivos.

#### 04 - Application Controller   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: iniciado · 157 linhas
- **Escopo:** quem decide **o próximo passo** — a camada que centraliza o fluxo de telas e a lógica de "de onde vim, pra onde vou" (wizards, checkout, workflows de aprovação), separada do controlador que trata a requisição. Por que aparece quando o fluxo é rico e some quando é CRUD. **Ressurreição (leitura):** Step Functions, Durable Functions, XState — a máquina de estados saiu do objeto e virou serviço. **Armadilhas:** aplicar em CRUD (indireção pura); fluxo codificado em `if` espalhado pelos controllers.

#### 05 - Template View × Transform View × Two-Step View   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: iniciado · 166 linhas
- **Escopo:** as três estratégias de renderizar. **Template View** (HTML com buracos — JSP, ERB, Thymeleaf), **Transform View** (função que recebe dados e produz a saída — XSLT no livro), **Two-Step View** (renderiza para uma representação lógica independente de tela, depois para a saída final — o padrão do look-and-feel global). **Ressurreição:** React é Transform View (leitura, mas central para a família); o payload dos RSC como primeiro estágio de um Two-Step View (leitura marcada). **Armadilhas:** lógica de negócio no template; Two-Step View aplicado sem a necessidade que o justifica (uma única aparência). **Fecha o bloco Iniciado.**

## Notas — Adepto (Distribuição, estado e concorrência offline)

#### 06 - Remote Facade   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: adepto · 157 linhas
- **Escopo:** a interface **grossa** sobre objetos finos, para não pagar round-trip de rede por getter — a Primeira Lei da Distribuição de Objetos de Fowler ("não distribua seus objetos"). O contexto EJB/CORBA/RMI que a tornou necessária. **Ressurreição forte:** **BFF** (Backend for Frontend) e o aggregation pattern de API Gateway são Remote Facade sem renomear o conceito. **Armadilhas:** facade que vira God service; aplicar in-process (indireção sem ganho); confundir com Facade do GoF (motivação diferente: rede × complexidade). **Abre o bloco Adepto.**

#### 07 - DTO — e por que virou pejorativo   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: adepto · 164 linhas
- **Escopo:** o **Data Transfer Object** — objeto burro que carrega dados através de uma fronteira de processo, criado para amortizar chamadas remotas. Por que ele é hoje o padrão mais aplicado sem motivo (DTO entre camadas do mesmo processo) e o mais atacado em revisão de arquitetura. O que é assembly/mapping e onde ele dói. **Ressurreição (leitura):** a mensagem protobuf do gRPC é um DTO gerado; o GraphQL resolve a chatty interface que motivou o DTO. **Armadilhas:** DTO sem fronteira de rede; anemia por DTO (o modelo vira DTO); explosão de mapeadores.

#### 08 - Session State — Client × Server × Database   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: adepto · 154 linhas
- **Escopo:** onde guardar o estado de uma conversa entre requisições, dado que HTTP não tem memória. **Client** (cookie, hidden field, URL — Fowler lista as ressalvas: tamanho, segurança), **Server** (HttpSession em memória — exige afinidade ou replicação), **Database** (tabela de sessão — durável, mais lento). **A ressurreição mais interessante da família:** a nuvem **inverteu a recomendação** — serverless e autoescala mataram sticky sessions, JWT resolveu a objeção de segurança de 2002 por assinatura, e o session store em Redis/DynamoDB virou default. Server Session State volta pela porta dos fundos com Durable Objects/atores (leitura). **Armadilhas:** JWT gordo/sem revogação; sessão em memória atrás de load balancer; confundir sessão com cache.

#### 09 - Optimistic × Pessimistic Offline Lock   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: adepto · 175 linhas
- **Escopo:** proteger dados numa **transação de negócio que atravessa várias requisições** — onde não se pode segurar transação de banco aberta. **Optimistic** (detecta conflito no commit, por versão/timestamp — assume que colisão é rara) × **Pessimistic** (evita conflito reservando o registro — assume que colisão é cara). Como escolher pelo custo do retrabalho. **Ressurreição forte:** optimistic virou o mecanismo padrão da nuvem (condition expressions, `If-Match`/ETag, `@Version`), porque lock distribuído é caro; pessimistic exige Redis/Zookeeper e vive só onde o conflito é intolerável. **Armadilhas:** lock pessimista sem timeout (usuário fecha o browser e trava o registro); otimista sem UX de conflito (o usuário perde o trabalho digitado); confundir com lock de banco.

#### 10 - Coarse-Grained Lock   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: adepto · 146 linhas
- **Escopo:** travar um **grupo** de objetos com um único lock — porque travar item a item vaza inconsistência entre as partes de um todo (o pedido e suas linhas). Implementações: versão compartilhada, root lock. **Honestidade:** é o padrão do roster **sem ressurreição limpa** — sobrevive diluído no conceito de **agregado** do DDD (o agregado é a unidade de consistência, o que é a mesma ideia com outro nome e outra justificativa). A seção "A ressurreição" desta nota diz isso explicitamente em vez de inventar correspondência. **Armadilhas:** granularidade grossa demais (contenção); confundir a fronteira do lock com a fronteira da tela. **Fecha o bloco Adepto.**

## Notas — Magus (Base: os padrões que você já usa sem saber o nome)

#### 11 - Layer Supertype + Separated Interface   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** **Layer Supertype** (a classe-base de uma camada que carrega o comportamento comum — `AbstractEntity`, `BaseController`) e **Separated Interface** (declarar a interface num pacote/módulo diferente da implementação, para inverter a direção da dependência). **Ressurreição forte:** Separated Interface é a mecânica de **Ports & Adapters / Hexagonal** — o padrão está no auge com outro nome, e reconhecê-lo desmistifica a arquitetura hexagonal. **Armadilhas:** Layer Supertype virando lixeira de utilitários e herança profunda; Separated Interface com uma implementação só (indireção sem inversão real). **Abre o bloco Magus.**

#### 12 - Registry + Plugin + Service Stub   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** os três padrões de **resolver quem é a implementação**. **Registry** (objeto global bem-conhecido onde se acha serviços — e sua má fama como Service Locator × injeção de dependência), **Plugin** (escolher a implementação em configuração, não em compilação), **Service Stub** (substituir um serviço externo por um dublê para testar). **Ressurreição forte nos três:** DI containers e service discovery (Consul/Eureka); arquitetura de plugins onipresente (Vite/esbuild, providers do Terraform); service virtualization como indústria (MSW, WireMock, LocalStack, Testcontainers). **Armadilhas:** Registry como singleton global que esconde dependências e quebra teste; plugin sem contrato versionado; stub que diverge do serviço real em silêncio.

#### 13 - Value Object + Money   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** **Value Object** (identidade pelo valor, não por referência — imutável, comparável por conteúdo) e **Money** como o caso canônico: por que representar dinheiro em `double` é bug garantido, arredondamento, alocação de resto na divisão, moeda como parte do valor. **Ressurreição (leitura):** records do Java, branded types do TS, newtype do Rust; o Valhalla ainda **não** entregou value classes, então esse pedaço é futuro, não presente — marcar. **Armadilhas:** Value Object mutável; `equals`/`hashCode` inconsistentes; centavos em ponto flutuante; misturar moedas sem tipo.

#### 14 - Special Case + Null Object   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** **Special Case** (uma subclasse que representa um caso especial — `UnknownCustomer`, `NullOrder`) e **Null Object** como o seu caso mais famoso: substituir a checagem de `null` espalhada por um objeto que responde com comportamento neutro. **Ressurreição forte:** `Optional`/`Maybe`, tipos `Result`, e pattern matching (que dá a alternativa estrutural ao polimorfismo do Special Case). **Armadilhas:** Null Object que esconde erro real (o caso "não encontrado" que deveria explodir); proliferação de casos especiais em vez de rever o modelo. **FECHA A FAMÍLIA** com um mapa-de-escolha dos 14 padrões e uma síntese da lente arqueológica (o que a nuvem ressuscitou e por quê).

---

## Próximos passos

1. ✅ Bloco **Iniciado** (01-05) escrito — 2026-07-30.
2. ✅ Bloco **Adepto** (06-10) escrito — 2026-07-30. Nota 10 registra explicitamente a **ausência** de ressurreição do Coarse-Grained Lock (absorvido pelo agregado do DDD), em vez de inventar correspondência.
3. ⬜ Escrever o bloco **Magus** (11-14) — a 14 fecha a família.
4. ⬜ `index.md` da família (MOC por fase + rotas), no molde das famílias 1-3.
5. ⬜ Atualizar roadmap-pai (família 4 ✅) + `index.md` do galho-pai + [[00-Meta/Roadmap]] central. Abrir a **família 5 (Arquitetura de Eventos)**.
6. ⬜ Reavaliar a pendência transversal do galho-pai: graduar as notas 22-23 da GoF a **capstone** que generaliza pras famílias.

## Disciplina

- Escrita sequencial via `/escrever-nota`, uma nota por vez. **Sem fan-out massivo** (regra pessoal do usuário).
- Validar Mermaid: `node .agents/skills/verificar-nota/scripts/validar-mermaid.mjs "<nota>"`. Paleta azul `#4A90D9` / âmbar `#F5A623` / vermelho `#D0021B`.
- Frontmatter: `fase:` lowercase, `type: concept`, `publish: false`.
- **Wikilinks:** verificar filename+pasta reais do alvo antes de linkar. Famílias 5-6 ainda não existem → citar em prosa, nunca folder-link quebrado.
- **Git:** stage de paths **explícitos e estreitos** (só esta família + roadmaps/index tocados) — nunca `git add` da pasta `Design de Software` inteira (varre trabalho paralelo do usuário). Sem `Co-Authored-By`.
