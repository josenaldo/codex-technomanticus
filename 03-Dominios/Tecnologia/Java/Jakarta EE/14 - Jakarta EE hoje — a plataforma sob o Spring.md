---
title: "Jakarta EE hoje — a plataforma sob o Spring"
created: 2026-06-07
updated: 2026-06-07
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - jakarta-ee
  - magus
  - sintese
  - especificacao
aliases:
  - "Jakarta EE hoje"
  - "Jakarta EE vs Spring"
  - "Estado do Jakarta EE"
---

# Jakarta EE hoje — a plataforma sob o Spring

> [!abstract] TL;DR
> Jakarta EE está **vivo e em movimento**: a versão 11 saiu em **26/jun/2025**, a 12 está em desenvolvimento, e tudo isso roda numa cadência aberta sob a Eclipse Foundation. Mais importante: a plataforma é a **fundação invisível** do ecossistema enterprise Java. O framework dominante não substitui as specs — ele as **implementa, consome e abstrai**, enquanto a nova geração de runtimes cloud-native (via Core Profile) as usa direto. Saber a especificação é entender o que **todo framework esconde** por baixo da API bonita. Esta é a nota que fecha o galho: o mapa que conecta as 13 specs que você estudou ao mundo real onde elas são usadas (quase sempre) sem aparecer.

## O que é

Esta capstone tem duas funções. A primeira é descritiva: **qual é o estado real da plataforma Jakarta EE hoje** — versões, governança, perfis, runtimes que a consomem. A segunda é estratégica: **um framework de decisão** para a pergunta que aparece em entrevista e em reunião de arquitetura — "Jakarta EE ou um framework? Plataforma pura ou ecossistema?".

Os doze blocos anteriores deste galho dissecaram especificações isoladas: o modelo spec/implementação, a migração `javax`→`jakarta`, Servlet, CDI (em três notas), JAX-RS, Bean Validation, JPA e o ciclo de vida da entidade, JTA, EJB e CDI avançado. Cada uma respondeu "o que esta spec define". Esta nota responde a pergunta que junta tudo: **onde essas specs vivem, quem as governa, e por que dominar o contrato te dá vantagem mesmo quando você nunca usa um app server "puro"**.

O frame central: Jakarta EE é um **conjunto de contratos** (especificações + TCK), não um produto. O que você baixa e roda é sempre uma **implementação** — um app server (WildFly, Open Liberty, GlassFish, Payara) ou um runtime moderno (Quarkus, Helidon). E o framework mais popular do mercado é, na prática, mais uma camada que **se apoia nesses mesmos contratos** do que um rival que os tornou obsoletos.

## Por que importa

Há um meme de blog antigo: "Jakarta EE morreu, ninguém usa Java EE, todo mundo migrou pro framework". É uma **meia-verdade datada**. A parte verdadeira: a era do app server monolítico pesado como escolha-padrão acabou. A parte falsa: as **especificações não morreram** — elas se espalharam. Hoje você consome JPA, CDI, Bean Validation e JAX-RS o tempo todo, muitas vezes sem perceber, porque o framework que você usa as implementa ou as embute.

Para uma entrevista internacional sênior, a diferença entre repetir o meme e responder **com datas e specs concretas** ("a 11 é de junho de 2025, a 12 está em desenvolvimento, o Core Profile é a ponte cloud-native, e o framework X implementa CDI/Servlet/JPA por baixo") é exatamente a diferença entre júnior e sênior. O entrevistador não quer saber se você sabe o nome do framework; quer saber se você entende **a camada de contratos por baixo dele** — porque é essa camada que sobrevive a trocas de framework, define portabilidade e explica por que `@Transactional` ou `@Valid` funcionam.

E há um motivo arquitetural maior: a **tabela spec→framework** desta nota é o mapa mental do bloco enterprise da trilha. Os galhos 8, 9 e 10 (planejados) cobrirão o framework dominante em profundidade; quando chegarem, você já saberá **qual contrato Jakarta está por baixo de cada feature** — e isso transforma a forma como você aprende o framework: não como mágica, mas como conveniência sobre padrões que você já domina.

## Como funciona

### Governança e cadência (Eclipse Foundation, Working Group, EFSP, TCK)

Jakarta EE é governado pelo **Jakarta EE Working Group**, hospedado na **Eclipse Foundation**, sob um modelo de governança vendor-neutral. A página oficial é explícita: "The vendor neutral governance model at the Eclipse Foundation ensures every Jakarta EE Working Group member has an equal voice." Nenhum fornecedor único controla o rumo da plataforma — é um consórcio.

O processo formal de criação de specs é o **Jakarta EE Specification Process (JESP)**, que adota o **Eclipse Foundation Specification Process v1.3 (EFSP)**. O JESP define ciclos de revisão com ballots (votações) de prazos definidos — Creation, Plan, Progress, Release e Service Release Reviews. Cada especificação passa por esse funil antes de virar oficial. Para a Plataforma 11, por exemplo, o Release Review ballot encerrou em **2025-06-17**.

Cada spec só pode ser declarada "compatível" por uma implementação que passe no **TCK (Technology Compatibility Kit)** — a bateria de testes de conformidade. É o TCK que dá sentido ao modelo de contratos: "compatível com Jakarta EE 11" não é marketing, é **um teste objetivo que a implementação passou**. (O contrato spec/impl/TCK é o tema da nota 01 deste galho.)

A cadência real, verificável nas releases oficiais:

| Versão | Data | Status |
| --- | --- | --- |
| Jakarta EE 8 | 10/set/2019 | primeira release pós-doação Oracle→Eclipse |
| Jakarta EE 9 | 08/dez/2020 | o "big bang" `javax`→`jakarta` |
| Jakarta EE 9.1 | 25/mai/2021 | suporte a Java SE 11 |
| Jakarta EE 10 | 22/set/2022 | introdução do Core Profile |
| **Jakarta EE 11** | **26/jun/2025** | **release atual** — verificado |
| Jakarta EE 12 | em desenvolvimento | WIP — verificado |

A 11 traz, segundo a spec oficial da Plataforma: suporte a **Java Records**, suporte a **Virtual Threads** ciente do runtime da JDK, e **Jakarta Data 1.0**. O requisito mínimo é **Java SE 17 ou superior**. A 12 está em desenvolvimento aberto, com propostas e milestones rastreáveis publicamente. Ou seja: uma plataforma que lançou versão **em 2025** e tem a próxima **em andamento** não é uma plataforma morta — é uma plataforma em manutenção evolutiva contínua.

### Os 3 perfis e o papel estratégico do Core Profile

Jakarta EE não é monolítico: ele se divide em três **perfis**, do menor pro maior:

- **Core Profile** — o conjunto mínimo, pensado para runtimes pequenos e cloud-native. A spec oficial descreve-o como "a profile of the Jakarta EE platform specifically targeted at smaller runtimes". Na versão 11, suas dependências centrais incluem **Jakarta Annotations 3.0**, **Jakarta Interceptors 2.2**, **Jakarta Contexts and Dependency Injection 4.1** e **Jakarta RESTful Web Services 4.0**. É o tijolo de injeção de dependência mais REST, sem o peso do app server completo. (O termo "CDI Lite" aparece no ecossistema como o subconjunto de CDI voltado a build-time/runtimes enxutos; a inclusão exata por versão deve ser conferida no documento da spec — verifique a release atual antes de citar a granularidade.)
- **Web Profile** — o perfil intermediário, com a stack web tradicional (Servlet, JPA, CDI, JAX-RS, validação etc.) sem o conjunto completo de specs enterprise legadas.
- **Platform** (Full Platform) — tudo: o Web Profile mais as specs enterprise históricas (mensageria, batch, conectores etc.).

O **Core Profile** é a peça estratégica desta nota. Foi introduzido na versão 10 (2022) justamente para servir de **ponte para a nova geração de runtimes cloud-native** — frameworks que querem CDI e REST com footprint mínimo, startup rápido e compatibilidade com containers. Três runtimes que consomem specs Jakarta nessa pegada (citados, sem explicar):

- **Quarkus** — "a Java framework designed... for building cloud-native applications", construído para Kubernetes; consome MicroProfile e specs Jakarta.
- **Open Liberty** — "a lightweight open framework for building fast and efficient cloud-native Java microservices", com suporte às últimas versões de MicroProfile e Jakarta EE (a 26.0.0.5 trouxe suporte oficial a Jakarta EE 11).
- **Helidon** — "a cloud-native, open-source Java framework for writing microservices that run on a fast web core powered by Java virtual threads"; provê APIs como JAX-RS, CDI e JSON-P/B.

A leitura: o Core Profile é a prova de que as specs **não ficaram presas ao app server pesado** — elas viraram a base de runtimes modernos e leves.

### MicroProfile

MicroProfile é um **complemento cloud-native** ao Jakarta EE, também sob a Eclipse Foundation, mas com **governança própria** (working group e charter separados). Sua missão, nas próprias palavras: "An open forum to optimize Enterprise Java for a microservices architecture." Ele padroniza áreas que o Jakarta EE não cobre nativamente — config, health checks, métricas, tolerância a falhas, telemetria — pensadas para microsserviços. A relação é de **sobreposição cooperativa**, não de rivalidade: o MicroProfile 7.1 inclui o **Core Profile do Jakarta EE como spec componente**, construindo cloud-native em cima da fundação Jakarta. Menção honesta: se você for fundo em runtimes como Quarkus, Helidon ou Open Liberty, vai esbarrar em MicroProfile do lado de fora das specs Jakarta puras.

### A tese do galho: o que o Spring esconde

Aqui está o coração da capstone. As specs que você estudou nos 13 blocos anteriores **não desapareceram** quando o mercado adotou o framework dominante. Elas estão lá embaixo. O framework oferece uma API própria, mais ergonômica, que em muitos casos **é uma camada sobre a spec** (ou sobre a mesma ideia, com sintaxe própria). A tabela mapeia o contrato Jakarta à feature equivalente do lado do framework:

| Spec Jakarta | O que o Spring oferece por cima |
| --- | --- |
| CDI | Injeção de dependência / `@Autowired` |
| Servlet | O chão sobre o qual o Spring MVC roda |
| JAX-RS | Alternativa aos controllers REST |
| Bean Validation | `@Valid` |
| JPA | Base do Spring Data JPA |
| JTA | `@Transactional` |

> [!warning] Fronteira deste galho
> A coluna da direita é **só o nome da feature** — o "endereço" onde você encontra a contraparte. Como o framework dominante funciona por dentro (proxies, container, autoconfiguração, etc.) é assunto dos **Galhos 8, 9 e 10 (planejados)**, não desta nota. Aqui o objetivo é único: mostrar que **cada conveniência do framework tem um contrato Jakarta correspondente** que você já domina. Quando o galho do framework chegar, esta tabela vira a ponte: você não estará aprendendo mágica nova, estará aprendendo a embalagem de specs conhecidas.

A consequência prática dessa tese: trocar de framework ou adotar um runtime novo **não joga fora seu conhecimento** — porque o conhecimento de baixo nível (a spec) é o que persiste. Bean Validation é Bean Validation seja a anotação chamada de onde for; JPA é JPA por baixo de qualquer abstração de repositório. **Aprender a spec é aprender o invariante.**

### Plataforma pura vs framework (comparação justa)

Não há vencedor universal. Há contexto. Uma comparação honesta, sem dogma:

**Quando Jakarta EE "puro" (sem framework por cima) faz sentido:**
- **Padronização e portabilidade**: você quer código que rode em qualquer implementação certificada, sem lock-in de fornecedor.
- **App server existente**: já há WildFly/Open Liberty/Payara em produção, time treinado, operação madura.
- **Contratos estáveis de longo prazo**: specs evoluem devagar e com retrocompatibilidade levada a sério — bom para sistemas de vida longa.

**Quando um framework faz mais sentido:**
- **Ecossistema e integrações**: bibliotecas, starters, comunidade enorme, "tudo já tem um jeito pronto".
- **Produtividade percebida**: convenções e autoconfiguração reduzem boilerplate inicial.
- **Contratação**: o mercado de devs é maior, onboarding mais rápido, mais material disponível.

Note que **nenhuma dessas colunas é sobre "qualidade técnica intrínseca"** — são sobre **trade-offs de contexto**: lock-in vs ecossistema, estabilidade vs velocidade, portabilidade vs conveniência. O sênior não escolhe por bandeira; escolhe pela coluna que casa com o requisito.

### O que o senior responde

Frame de decisão, não torcida. Quando perguntam "plataforma ou framework?", a resposta sênior é uma **pergunta de volta**:

1. **Já existe um app server e um time treinado nele?** Se sim, modernizar dentro da plataforma costuma ser mais barato que reescrever.
2. **O requisito é portabilidade/padronização ou velocidade de entrega + ecossistema?** Isso aponta a coluna.
3. **É cloud-native enxuto com startup e footprint críticos?** Aí Core Profile + runtime moderno entra forte.
4. **Independente da escolha: o time entende as specs por baixo?** Porque é isso que te salva quando o framework "esconde demais" e algo quebra na camada de baixo.

A torcida ("framework é sempre melhor" ou "spec pura é mais correta") é resposta de júnior. O frame de requisitos é resposta de sênior.

## Na prática

Três cenários **hipotéticos** (explicitamente ilustrativos — não experiência relatada) que mostram o frame aplicado:

**Cenário hipotético A — sistema WildFly/Jakarta existente.** Uma empresa tem um ERP em WildFly, rodando há anos, com EJB, JPA e JTA. A pressão é "migrar pro framework moderno". A resposta sênior não é reescrever por moda: é **ficar e modernizar dentro da plataforma** — atualizar para Jakarta EE 11, adotar CDI no lugar de EJB onde fizer sentido, aproveitar virtual threads. A portabilidade e a base treinada são ativos, não dívida. Reescrita só se houver requisito que a plataforma não atende.

**Cenário hipotético B — serviço novo num time que já usa o framework.** Time padronizado no framework dominante, todo o tooling de CI/CD em volta dele. Um serviço novo nasce ali: **usar o framework é a escolha certa** — consistência operacional vale muito. Mas o diferencial: o dev que **conhece JPA, CDI e Bean Validation por baixo** entende o que a abstração de repositório está fazendo, depura problemas de transação na raiz e não trata `@Transactional` como caixa-preta. Saber a spec **te faz melhor no framework**, não fora dele.

**Cenário hipotético C — produto cloud-native enxuto.** Startup construindo microsserviços com requisito duro de startup rápido e baixo consumo de memória (custo de container). Aqui o caminho natural é um **runtime moderno sobre o Core Profile** (Quarkus/Helidon/Open Liberty na pegada leve), possivelmente com MicroProfile para config/health/métricas. CDI + REST do Core Profile dão a base; o footprint mínimo é o requisito que decide.

Em nenhum dos três a resposta é dogmática. Em todos, **conhecer as specs Jakarta é o que sustenta a decisão** — seja para ficar, para usar bem o framework, ou para escolher o runtime certo.

## Armadilhas

### (1) "Jakarta EE morreu"
A armadilha mais comum, herdada de blogs antigos. A era do app server pesado como padrão único acabou — mas a **plataforma não morreu**: a versão 11 é de **junho de 2025**, a 12 está em desenvolvimento, e as specs fundam o ecossistema inteiro (inclusive o framework dominante e os runtimes cloud-native). **Fix:** antes de repetir o meme, **cheque as releases oficiais** (jakarta.ee/release). Datas verificáveis matam o meme.

### (2) "O framework substituiu as specs"
Tratar o framework como se tivesse tornado Jakarta EE obsoleto. Na verdade ele **implementa, consome e abstrai** as specs — CDI, Servlet, JPA e Bean Validation estão lá embaixo. Quem só sabe a API do framework está vendo a embalagem; quem sabe a spec vê o conteúdo. **Fix:** use a **tabela da tese** (spec→feature) como mapa. Para cada conveniência do framework, identifique o contrato Jakarta correspondente — e você terá vantagem na próxima dúvida de baixo nível.

### (3) Decidir plataforma por ideologia
Escolher "specs puras porque são mais corretas" ou "framework porque é mais prático" como **identidade**, antes de olhar o requisito. Isso produz arquitetura ruim em ambas as direções: lock-in desnecessário ou reescrita por moda. **Fix:** deixe o **contexto decidir** — app server existente, requisito de portabilidade vs ecossistema, restrição cloud-native. O frame de decisão (seção "O que o senior responde") vem antes da preferência.

### (4) Citar estatística de adoção de blog
Afirmar "X% do mercado usa Y" ou "a maioria migrou" com base em post não-fontado. Números de adoção circulam sem metodologia e envelhecem rápido — repeti-los é frágil em entrevista. **Fix:** fale em **sinais verificáveis** — releases datadas, specs ativas, runtimes certificados que passaram no TCK. Esses são fatos checáveis; market share de blog não é.

## Em entrevista

### Frase pronta (inglês)

> Jakarta EE is alive and evolving: version 11 shipped in June 2025, version 12 is in active development, and the whole platform runs on an open, vendor-neutral cadence under the Eclipse Foundation. More importantly, it's the invisible foundation of the enterprise Java ecosystem — the dominant framework doesn't replace specifications like CDI, Servlet, JPA, or Bean Validation; it implements and consumes them, while the modern cloud-native runtimes build on the Core Profile directly. So when I evaluate "platform versus framework", I don't pick a side ideologically — I look at the context: an existing app server and a trained team point toward modernizing within the platform, while a need for ecosystem and delivery speed points toward a framework, and a lean cloud-native target points toward a Core Profile runtime. Either way, knowing the underlying specs is what makes me effective, because that knowledge survives any framework choice.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| especificação | specification / spec |
| implementação compatível | compatible implementation |
| conjunto de testes de conformidade | Technology Compatibility Kit (TCK) |
| cadência de releases | release cadence |
| portabilidade | portability |
| dependência de fornecedor | vendor lock-in |
| neutro quanto a fornecedor | vendor-neutral |
| nativo de nuvem | cloud-native |
| perfil mínimo | Core Profile |

### Cheatsheet do galho

Qual nota abrir para qual problema:

| Problema / tema | Nota |
| --- | --- |
| Spec vs implementação (o modelo) | [[01 - O modelo Jakarta EE — especificações e implementações]] |
| Migração `javax`→`jakarta` | [[02 - De Java EE a Jakarta EE]] |
| HTTP base (a camada de baixo) | [[03 - Servlet API — o alicerce HTTP]] |
| Injeção de dependência (DI) | [[04 - CDI — beans e injeção]] |
| Escopos e contextos | [[05 - CDI — escopos e contextos]] |
| Qualifiers, producers e eventos | [[06 - CDI — qualifiers, producers e eventos]] |
| REST declarativo | [[07 - JAX-RS — REST declarativo]] |
| Validação | [[08 - Bean Validation]] |
| Contrato de ORM | [[09 - JPA — a especificação de persistência]] |
| Estados da entidade | [[10 - EntityManager e o ciclo de vida da entidade]] |
| Transações | [[11 - JTA — transações na plataforma]] |
| Legado que moldou a plataforma | [[12 - EJB — o legado que moldou a plataforma]] |
| AOP / extensões (interceptors, decorators) | [[13 - CDI avançado — interceptors, decorators e extensões]] |

## Veja também

- [[01 - O modelo Jakarta EE — especificações e implementações]]
- [[02 - De Java EE a Jakarta EE]]
- [[04 - CDI — beans e injeção]]
- [[13 - CDI avançado — interceptors, decorators e extensões]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Jakarta EE|Jakarta EE (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Core Profile|Core Profile (Dicionário)]]

## Referências

Acesso em 2026-06-07.

- Jakarta EE — Releases: https://jakarta.ee/release/
- Jakarta EE 11 Platform Specification: https://jakarta.ee/specifications/platform/11/
- Jakarta EE Core Profile 11 Specification: https://jakarta.ee/specifications/coreprofile/11/
- Jakarta EE — About / Governança: https://jakarta.ee/about/
- Jakarta EE Specification Process (JESP / EFSP): https://jakarta.ee/about/jesp/
- MicroProfile: https://microprofile.io/
- Quarkus — About: https://quarkus.io/about/
- Open Liberty — About: https://openliberty.io/about/
- Helidon: https://helidon.io/
