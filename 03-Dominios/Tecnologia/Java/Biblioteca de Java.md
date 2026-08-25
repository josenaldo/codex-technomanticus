---
title: "Biblioteca de Java"
created: 2026-05-11
updated: 2026-08-25
type: reference
status: budding
aliases: []
tags:
  - java
  - referências
lang: pt
publish: true
---

# Biblioteca de Java

> Portais, blogs e recursos de referência para o ecossistema Java — organizados entre equivalente direto do Real Python e complementos especializados.

## Equivalente direto

- **[Baeldung](https://www.baeldung.com)** — portal — Mesma fórmula do Real Python: artigos profundos, focados em problemas reais, organizados por temas (Spring Boot, JPA/Hibernate, Java Core, Concurrency, REST, Security). Qualidade técnica boa, mas SEO-otimizado e às vezes raso em tópicos complexos.

## Complementos essenciais

- **[Vlad Mihalcea](https://vladmihalcea.com/blog/)** — blog pessoal — Referência absoluta em JPA/Hibernate, performance de banco e transações. Profundidade muito maior que Baeldung em persistência. Obrigatório para stack Spring + Postgres.
- **[Thorben Janssen](https://thorben-janssen.com/)** — blog pessoal — Também forte em Hibernate, viés mais didático.
- **[InfoQ (track Java/JVM)](https://www.infoq.com)** — portal de arquitetura — Não é portal Java, mas cobre tendências e debates (Project Loom, Valhalla, GraalVM, microservices) que Baeldung não toca. Mais "Pragmatic Engineer" que "Real Python".
- **[Java, SQL and jOOQ](https://blog.jooq.org/)** (Lukas Eder) — blog corporativo/pessoal — Posts excelentes sobre Java, SQL e como os dois conversam mal. Lukas Eder é o criador do jOOQ.
- **[SivaLabs](https://www.sivalabs.in/)** — blog pessoal — Tutoriais práticos de Spring Boot, Testcontainers, microservices. Estilo "caso real" em vez de blog institucional.

> [!info] Nota crítica
> Para arquitetura de verdade, Vlad Mihalcea + InfoQ + livros clássicos (Effective Java, Java Concurrency in Practice) ainda batem qualquer portal.


## Videoaulas e playlists

> Playlists gratuitas do YouTube, verificadas uma a uma em 2026-08-25 (título, número de aulas e data da aula mais recente vêm dos metadados do próprio YouTube, não de memória). Prioridade para **português**, **cobertura ampla** e **projeto prático**; o inglês entra onde o material em PT-BR envelheceu ou nunca existiu. O ano entre parênteses é o intervalo real de publicação — importa muito num ecossistema onde Spring Boot já vai na versão 4.

### Java core

- **[Maratona Java Virado no Jiraya](https://www.youtube.com/playlist?list=PL62G310vn6nFIsOCC0H-C2infYgwm8SWW)** — DevDojo (William Suane) — 286 aulas (2021) — **PT** — A referência de cobertura em português: sintaxe, orientação a objetos, coleções, genéricos, exceções, tudo do zero e sem pular etapa. Nada mais completo em PT-BR e de graça. Ponto fraco: é de 2021, então não cobre records maduros, virtual threads nem os recursos de Java 21+.
- **[Curso de JAVA + SPRING](https://www.youtube.com/playlist?list=PLNCSWIsR6ADI_wMAx9F-Iu8Hs9HHxj4sb)** — [[Fernanda Kipper]] — 18 aulas (2024) — **PT** — O material mais **atual** em português juntando fundamentos, orientação a objetos, threads e Spring, sempre construindo algo. Curta e densa: serve como atualização por cima da Maratona, não como substituta dela.
- **[Fundamentos do Java para Iniciantes](https://www.youtube.com/playlist?list=PLiFLtuN04BS2GSi8Q-haYkRy8KEv6Grvf)** — [[Giuliana Bezerra]] — 15 aulas (2022-2023) — **PT** — Começa por WORA, JVM, JDK e JRE, que é o corte conceitual certo para quem vem de outra linguagem.
- **[Java Avançado](https://www.youtube.com/playlist?list=PLiFLtuN04BS2bWB9UcIrun35kV080KoKU)** — [[Giuliana Bezerra]] — 6 aulas (2024) — **PT** — Anotações, Streams e outros tópicos que a maioria dos cursos introdutórios trata de raspão.
- **[Curso Estrutura de Dados e Algoritmos com Java](https://www.youtube.com/playlist?list=PLGxZ4Rq3BOBrgumpzz-l8kFMw2DLERdxi)** — [[Loiane Groner]] — 55 aulas (2016-2023) — **PT** — Ainda recebe aulas novas. Vale pelo par estrutura de dados + implementação em Java, não pela sintaxe moderna.
- **[Curso de Java Básico](https://www.youtube.com/playlist?list=PLGxZ4Rq3BOBq0KXHsp5J3PxyFaBIXVs3r)** (98 aulas, 2013-2016) e **[Módulo 2: Intermediário](https://www.youtube.com/playlist?list=PLGxZ4Rq3BOBoqYyFWOV_YbfBW80YGAGEI)** (50 aulas, 2016-2019) — [[Loiane Groner]] — **PT** — Didática excelente e cobertura enorme, mas **datadas**: Java 8 era novidade quando foram gravadas. Use como reforço de fundamento, nunca como fonte de "como se escreve Java hoje".

### Spring e Spring Boot

- **[Spring Boot Essentials 2](https://www.youtube.com/playlist?list=PL62G310vn6nFBIxp6ZwGnm8xMcGE3VA5H)** — DevDojo — 52 aulas (2020) — **PT** — O curso gratuito de Spring Boot mais completo em português: sai do Initializr e vai até empacotamento com Jib. Envelheceu em versões (Boot 2.x), mas os conceitos — auto-configuração, camadas, tratamento de erro, documentação — continuam valendo.
- **[Spring REST](https://www.youtube.com/playlist?list=PLZTjHbp2Y783orm-9p3L5oRzFxVKrmAVd)** — AlgaWorks — 28 aulas (2020-2023) — **PT** — Foco em desenhar API REST de verdade com Spring, não em CRUD de vitrine.
- **[SPRING FRAMEWORK](https://www.youtube.com/playlist?list=PLZTjHbp2Y783-vNLT6v9jmRR4MPZZfhJA)** — AlgaWorks — 32 aulas (2016-2019) — **PT** — Boa para o **núcleo**: contêiner, injeção de dependência, `@Autowired`, ciclo de vida de bean. Justamente a parte que quase não muda entre versões.
- **[Tutoriais Spring](https://www.youtube.com/playlist?list=PLiFLtuN04BS1pObTFjm5g2TwgBIBfEyze)** — [[Giuliana Bezerra]] — 8 aulas (2023-2024) — **PT** — Tópicos avulsos e atuais: GraphQL com Spring Boot, Spring State Machine. Complemento, não trilha.
- **[Aulões Spring Boot](https://www.youtube.com/playlist?list=PLiFLtuN04BS2yfbo3HYLNq_O1zDq9RRQi)** — [[Giuliana Bezerra]] — 4 aulas (2022-2023) — **PT** — Aulas longas e temáticas, incluindo injeção de dependência "do Java ao Spring", que é a melhor porta de entrada conceitual para quem já sabe Java.
- **[Tutoriais Spring Batch](https://www.youtube.com/playlist?list=PLiFLtuN04BS07Yw7rnoz1ytWCLu8yteVv)** — [[Giuliana Bezerra]] — 12 aulas (2022-2024) — **PT** — Único material sério em português sobre processamento em lote com Spring. Assunto que aparece em legado corporativo o tempo inteiro e quase nunca é ensinado.
- **[Spring 6 and Spring Boot Tutorial for Beginners](https://www.youtube.com/playlist?list=PLsyeobzWxl7qbKoSgR5ub6jolI8-ocxCF)** — Telusko — 41 aulas (2024) — **EN** — Cobre Spring 6 / Boot 3 do zero até OAuth com Google e GitHub. É a trilha completa mais recente entre as gratuitas.

### Projeto prático fim a fim

- **[CRUD Angular + Spring](https://www.youtube.com/playlist?list=PLGxZ4Rq3BOBpwaVgAPxTxhdX_TfSVlTcY)** — [[Loiane Groner]] — 64 aulas (2021-2023) — **PT** — A melhor opção em português de **construir uma aplicação inteira acompanhando**: back-end Spring e front-end Angular, do primeiro commit ao deploy, com refatorações reais no caminho.
- **[Da Arquitetura ao Deploy](https://www.youtube.com/playlist?list=PLiFLtuN04BS1c-JvhKFxYyeD-GVtnwUcx)** — [[Giuliana Bezerra]] — 7 aulas (2023) — **PT** — Pega um sistema de pagamentos e desce da decisão arquitetural até Docker e nuvem. Mostra o raciocínio que antecede o código, que é o que falta na maioria dos cursos.
- **[Spring AI + Angular](https://www.youtube.com/playlist?list=PLGxZ4Rq3BOBrv9_kAgnWdWgMCxpQsTk6h)** — [[Loiane Groner]] — 11 aulas (2025) — **PT** — Material mais recente da lista em português: API REST de chat com memória usando Spring AI.
- **[Book Social Network](https://www.youtube.com/playlist?list=PL41m5U3u3wwk0xrfl0FK--idljxVR2Dnx)** — Bouali Ali — 4 aulas longas (2024) — **EN** — Aplicação completa com Spring Boot, Angular, Docker, Keycloak e notificação em tempo real por WebSocket. Cada vídeo tem várias horas; é praticamente um curso por aula.

### JPA, Hibernate e persistência

- **[JPA LiveClass](https://www.youtube.com/playlist?list=PLZTjHbp2Y7812axMiHkbXTYt9IDCSYgQz)** — AlgaWorks — 20 aulas (2019) — **PT** — Do mapeamento básico até JPQL e Criteria API em lote. É o material mais completo em português sobre JPA, ainda que de 2019.
- **[High-Performance Java Persistence](https://www.youtube.com/playlist?list=PLwZWXcnAr8uecV7Oi3arDBRmQarKg7d65)** — Vlad Mihalcea — 30 vídeos (2017-2026) — **EN** — ⭐ **A referência viva de Hibernate.** Continua recebendo vídeos novos (o mais recente é de abril de 2026) e cada um resolve um problema concreto de desempenho: como registrar SQL, buscar hierarquia, evitar N+1. Complemento obrigatório ao blog dele, já listado acima.
- **[JPA/Hibernate Fundamentals 2023](https://www.youtube.com/playlist?list=PLEocw3gLFc8UYNv0uRG399GSggi8icTL6)** — Laurentiu Spilca — 16 aulas (2023-2024) — **EN** — Trilha estruturada do zero, do mapeamento de entidade até Spring Data. Spilca é autor do *Spring Start Here*, e a didática dele é de livro, não de tutorial.
- **[Spring Data JPA | Hibernate](https://www.youtube.com/playlist?list=PL41m5U3u3wwkS8BU0fIeRQwY3hK4VlFlX)** — Bouali Ali — 8 aulas (2022-2024) — **EN** — Curso completo de Spring Data JPA num punhado de vídeos longos.

### Microsserviços e sistemas distribuídos

- **[Microsserviços](https://www.youtube.com/playlist?list=PLZTjHbp2Y7809w3PLM0UE_LgQq6vk49q0)** — AlgaWorks — 29 vídeos (2022-2025) — **PT** — ⭐ O material em português **mais atual** sobre o assunto, ainda recebendo vídeos. Cobre desde Circuit Breaker com Resilience4j até discussões de quando não fatiar.
- **[Microsserviços](https://www.youtube.com/playlist?list=PLiFLtuN04BS2pgvdO2W7s6HEGhNojtk0F)** e **[Microservices Patterns](https://www.youtube.com/playlist?list=PLiFLtuN04BS2D3okN9Tyv91LPdoCdzzSZ)** — [[Giuliana Bezerra]] — 6 e 4 vídeos (2023-2025) — **PT** — Foco em padrão, não em ferramenta: Strangler Fig, decomposição, estratégias de migração.
- **[MICROSERVICES COM JAVA SPRING](https://www.youtube.com/playlist?list=PL8iIphQOyG-Dp037UnFG0x8aduelvZZWE)** — [[Michelli Brito]] — 5 vídeos (2021-2025) — **PT** — Inclui observabilidade com Actuator, que é a parte que quase todo curso de microsserviços esquece.
- **[Spring Boot Microservices](https://www.youtube.com/playlist?list=PL62G310vn6nH_iMQoPMhIlK_ey1npyUUl)** — DevDojo — 11 aulas (2019) — **PT** — Datada (Eureka e Zuul da era Spring Cloud antiga), mas ainda útil para entender de onde vieram os padrões. Leia junto com o galho de [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos]], que registra o que morreu desde então.
- **[RabbitMQ Direto Ao Ponto](https://www.youtube.com/playlist?list=PL62G310vn6nF-iJF7v3DWhk5Mngup-sub)** — DevDojo — 5 aulas (2022-2023) — **PT** — Curto e prático, bom par para o galho de [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria]].

### Segurança

- **[Spring Security Fundamentals 2022](https://www.youtube.com/playlist?list=PLEocw3gLFc8X_a8hGWGaBnSkPFJmbb8QP)** — Laurentiu Spilca — 23 aulas (2022-2023) — **EN** — ⭐ Melhor material gratuito sobre Spring Security em qualquer idioma. Constrói o entendimento do filter chain por dentro, em vez de decorar configuração. Não há equivalente em português com essa profundidade.

### Testes

- **[Testes Unitários](https://www.youtube.com/playlist?list=PLZTjHbp2Y781l0lo9KITB8DtBeOljmFbK)** — AlgaWorks — 9 vídeos (2023) — **PT** — Introdução decente em português ao assunto.
- **[Testing Spring Apps for Developers](https://www.youtube.com/playlist?list=PLEocw3gLFc8VpWbb8F8GxQeGEe1VS95ok)** — Laurentiu Spilca — 6 aulas (2026) — **EN** — ⭐ Publicada em 2026, é o material mais recente da lista inteira. Trata de testar aplicação Spring de verdade, com os slices e o contexto de teste.

### Programação reativa

- **[Spring WebFlux Essentials](https://www.youtube.com/playlist?list=PL62G310vn6nH5Tgcp5q2a1xCb6CsZJAi7)** — DevDojo — 34 aulas (2020) — **PT** — Único curso completo de WebFlux em português. Tem a irmã **[Project Reactor Essentials](https://www.youtube.com/playlist?list=PL62G310vn6nG3sBMCIEoZBK3r3E_4aKW5)**, que ensina o Reactor por baixo — comece por ela.
- **[Reactive Spring](https://www.youtube.com/playlist?list=PLEocw3gLFc8W-w8QZbM8f955StBEiQjJk)** — Laurentiu Spilca — **EN** — Complemento conceitual.

### Estar em dia

- **[Inside Java Newscast](https://www.youtube.com/playlist?list=PLX8CzqL3ArzX8ZzPNjBgji7rznFFiOr58)** — canal oficial Java (Oracle) — 114 episódios (2021-2026) — **EN** — ⭐ A forma mais eficiente de acompanhar o que entra em cada JDK. Nikolai Parlog explica JEP por JEP, com o contexto de por que a decisão foi tomada.
- **[Spring Boot 4](https://www.youtube.com/playlist?list=PLZV0a2jwt22v874ngZcWw3umP2yfsV9sK)** — Dan Vega — 18 vídeos (2025-2026) — **EN** — ⭐ Cobre Spring Framework 7 e Boot 4 conforme saem. É onde o material das trilhas em português ainda não chegou.
- **[Spring Tips](https://www.youtube.com/playlist?list=PLgGXSWYM2FpPw8rV0tZoMiJYSCiLhPnOc)** — Spring Developer (Josh Long) — 161 episódios (2016-2024) — **EN** — Série oficial da equipe do Spring. Cada episódio pega um recurso e mostra funcionando; é a fonte primária depois da documentação.
- **[Sip of Java](https://www.youtube.com/playlist?list=PLX8CzqL3ArzWkPoqzLemlQ-Nm5wXzRmfE)** — canal oficial Java — **EN** — Pílulas de um a dois minutos sobre recursos pontuais da linguagem.

> [!warning] Cuidado com o que parece gratuito
> Dois cursos que aparecem em busca como se fossem abertos **não são**: o *Spring Boot Direto Das Trincheiras* do DevDojo (169 aulas, o material mais atual do canal) e o *Modern Spring From Scratch* do Java Brains são **exclusivos para membros pagantes** do canal — a playlist é pública, os vídeos não. O mesmo vale para as playlists marcadas com 🔒 no canal da [[Fernanda Kipper]]. Verificado em 2026-08-25.

> [!info] Como escolher
> Se a meta é **cobertura**, a Maratona Java do DevDojo continua imbatível em português — aceite que ela para em 2021. Se a meta é **estar atual**, a combinação que funciona é curso em PT-BR para a base e canal em inglês para a fronteira: Vlad Mihalcea para persistência, Spilca para segurança e testes, Dan Vega e Inside Java Newscast para versões novas. Se a meta é **construir alguma coisa**, o CRUD Angular + Spring da [[Loiane Groner]] é a trilha mais longa e completa, e o Book Social Network do Bouali Ali é a mais densa.
