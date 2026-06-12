---
title: "Buildpacks — imagem sem Dockerfile"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - cloud-native
  - adepto
  - container
aliases:
  - "Cloud Native Buildpacks"
  - "Paketo"
  - "bootBuildImage"
---

# Buildpacks — imagem sem Dockerfile

> [!abstract] TL;DR
> **Cloud Native Buildpacks (CNB)** é uma spec da CNCF (incubating) que transforma seu código-fonte em uma **imagem OCI sem você escrever um Dockerfile**. O conhecimento de como construir a imagem (camadas, JVM, segurança, non-root) fica centralizado no **builder**, não espalhado por dezenas de Dockerfiles. **Paketo** é a implementação de buildpacks para Java/Spring. O Spring Boot embute isso desde a versão 2.3: `./mvnw spring-boot:build-image` (ou `bootBuildImage` no Gradle) chama o builder default `paketobuildpacks/builder-noble-java-tiny` e cospe a imagem — **mas precisa de um Docker daemon rodando**. Fixe a versão da JVM com `BP_JVM_VERSION`.

## O que é

Pensa num Dockerfile de aplicação Java. Você escreve `FROM eclipse-temurin:21`, copia o JAR, define o `ENTRYPOINT`, talvez crie um usuário non-root, talvez separe as camadas pra cache. Agora multiplica isso por 50 serviços. Cada time copia, cola, esquece de atualizar a base, deixa rodando como root. O Dockerfile vira dívida espalhada.

**Cloud Native Buildpacks** invertem o problema. Em vez de cada dev descrever *como* empacotar, um time central mantém um **builder** que já sabe empacotar qualquer app Java do jeito certo. O dev só aponta o builder pro código-fonte e recebe uma **imagem OCI** pronta — **sem Dockerfile**.

CNB é um projeto **CNCF incubating** (iniciado por Pivotal e Heroku em 2018). A spec define três peças:

- **Buildpack** — uma unidade que *detecta* se o app casa com seu critério (ex.: "tem um `pom.xml`? então é Maven") e fornece as dependências de build e runtime.
- **Builder** — combina um conjunto de buildpacks com imagens-base (build image + run image), formando o ambiente completo que transforma fonte em imagem.
- **Lifecycle** — o motor que orquestra as fases (detect, analyze, restore, build, export, rebase…). É quem realmente roda o pipeline.

**Paketo** é a implementação de buildpacks para Java (e Spring) sobre essa spec. É o que o Spring Boot usa por baixo.

## Por que importa

Numa entrevista de plataforma/produção, buildpacks são a resposta para "como vocês padronizam a containerização de dezenas de serviços?". Os ganhos concretos:

- **Conhecimento centralizado** — segurança, compliance e boas práticas (non-root, JVM enxuta, camadas otimizadas) vivem no builder. Atualizar a base de 50 serviços vira um `rebase`, não 50 PRs de Dockerfile.
- **Zero Dockerfile pra manter** — menos superfície de erro humano. O dev não precisa saber escrever um Dockerfile bom.
- **Já vem no Spring Boot** — desde a 2.3, `build-image`/`bootBuildImage` são plugins de primeira classe. Sem ferramenta extra pra instalar no pipeline (além do Docker daemon).
- **Imagens non-root por padrão** — o Paketo já constrói e roda como usuário non-root, seguindo a spec da plataforma CNB. Você não precisa lembrar de criar o usuário.

A alternativa de mesma família é o [[03-Dominios/Java/Cloud-native e produção/07 - Jib — imagem daemonless|Jib]] (sem daemon). O panorama das três abordagens — Dockerfile, buildpacks, Jib — está em [[03-Dominios/Java/Cloud-native e produção/03 - Empacotando o app numa imagem — o panorama|Empacotando o app numa imagem (panorama)]].

## Como funciona

### CNB: builder, buildpack e lifecycle

O fluxo conceitual de um build com buildpacks:

1. **Detect** — cada buildpack do builder olha o código-fonte e responde "isso é comigo?". O buildpack de Maven detecta o `pom.xml`, o de JVM se declara necessário, e assim por diante.
2. **Build** — os buildpacks selecionados rodam em ordem, cada um contribuindo *camadas* (a JVM numa camada, as dependências noutra, o app noutra). Camadas separadas = cache melhor: trocar uma linha de código não reconstrói a camada da JVM.
3. **Export** — o lifecycle junta tudo numa **imagem OCI** final, com a run image como base, o usuário non-root configurado e o process type de entrada definido.

Ninguém escreveu um `FROM` ou um `COPY`. O builder carregava esse conhecimento; o lifecycle executou.

> [!info] Builder, buildpack, lifecycle — quem é quem
> Analogia: o **buildpack** é um especialista (um sabe instalar JVM, outro sabe rodar Maven). O **builder** é a equipe completa desses especialistas mais o "escritório" (imagens-base). O **lifecycle** é o gerente que chama cada especialista na hora certa e entrega o produto final embalado (a imagem OCI).

### Paketo + bootBuildImage no Spring Boot

O Spring Boot embrulha tudo isso num goal/task:

- Maven: `spring-boot:build-image`
- Gradle: `bootBuildImage`

Disponível **desde o Spring Boot 2.3**. Por baixo, o plugin chama o **builder default**:

```
paketobuildpacks/builder-noble-java-tiny:latest
```

(`noble` = Ubuntu 24.04 Noble Numbat; `tiny` = base mínima sem shell, menor superfície). O Paketo detecta Maven/Gradle, compila o app, instala a JVM e produz a imagem **non-root** — tudo sem você tocar num Dockerfile.

### BP_JVM_VERSION e o Docker daemon

Dois pontos operacionais que caem em entrevista:

- **Precisa de Docker daemon.** O goal inspeciona a configuração local do Docker CLI pra descobrir o contexto e conecta nesse daemon pra construir e gravar a imagem. Sem daemon (ou socket equivalente), o build falha. É a diferença prática para o Jib, que é **daemonless**.
- **`BP_JVM_VERSION` fixa a JVM.** Variável de build do Paketo que define a versão major do JDK/JRE. Sem ela, você herda o default do builder — que muda quando o builder atualiza. Em produção, **fixe**.

## Na prática

Build pela linha de comando (Maven), num serviço genérico de pedidos:

```bash
# constrói a imagem OCI direto do código, sem Dockerfile
./mvnw spring-boot:build-image \
  -Dspring-boot.build-image.imageName=registry.exemplo.com/pedidos-service:1.4.0
```

(Requer um Docker daemon acessível na máquina/agent de CI.)

Configuração equivalente no Gradle (Kotlin DSL), fixando a JVM e o nome da imagem:

```kotlin
tasks.named<org.springframework.boot.gradle.tasks.bundling.BootBuildImage>("bootBuildImage") {
    imageName.set("registry.exemplo.com/pedidos-service:${project.version}")
    // pin do builder: nunca dependa só do default "latest"
    builder.set("paketobuildpacks/builder-noble-java-tiny:0.0.x")
    environment.set(
        mapOf(
            "BP_JVM_VERSION" to "21", // fixa a JVM major
        ),
    )
}
```

Para gerar **native image** via buildpack (GraalVM), o caminho é a variável `BP_NATIVE_IMAGE` — detalhado em [[03-Dominios/Java/Cloud-native e produção/09 - Native Image com Spring — Spring AOT na prática|Native Image com Spring]].

## Armadilhas

### (1) Esquecer que precisa do Docker daemon

A pegadinha mais comum. `build-image`/`bootBuildImage` **não** funcionam num agent de CI sem Docker daemon (ou socket equivalente). Pipelines em runners "puros", ambientes restritos ou clusters sem Docker-in-Docker quebram aqui. Se você precisa empacotar **sem daemon**, a resposta é [[03-Dominios/Java/Cloud-native e produção/07 - Jib — imagem daemonless|Jib]], não buildpacks. Saber dizer isso numa entrevista mostra que você entendeu o trade-off, não só o comando.

### (2) Builder desatualizado / sem pin

Confiar no `paketobuildpacks/builder-noble-java-tiny:latest` parece conveniente, mas `latest` é uma bomba-relógio: a base e os buildpacks mudam sem você pedir, e dois builds da mesma tag podem gerar imagens diferentes — adeus reprodutibilidade. **Fixe uma versão do builder** e atualize de propósito, num PR revisado. Builder esquecido por meses também acumula CVEs na base; tratar atualização como tarefa explícita é parte do valor centralizado dos buildpacks.

### (3) Não fixar BP_JVM_VERSION

Sem `BP_JVM_VERSION`, a versão da JVM vem do default do builder. Quando o builder atualizar, sua imagem pode pular de Java 21 pra 23 sem aviso — e quebrar em runtime por uma incompatibilidade sutil. Sempre **declare a major version** que você homologou. É barato e elimina uma classe inteira de surpresas em produção.

## Em entrevista

### Frase pronta (inglês)

> We package our Spring Boot services with Cloud Native Buildpacks instead of hand-written Dockerfiles. The `bootBuildImage` task uses the default Paketo builder, so all the containerization knowledge — non-root users, layering, the right JVM — lives in one place rather than being copy-pasted across every service. The main caveat is that it needs a Docker daemon to run, so on daemonless CI we reach for Jib instead. We always pin the builder version and set `BP_JVM_VERSION` to keep builds reproducible.

### Vocabulário

| Português | Inglês |
| --- | --- |
| pacote de build | buildpack |
| construtor | builder |
| ciclo de vida | lifecycle |
| imagem OCI | OCI image |
| sem Dockerfile | Dockerfile-less |
| daemon do Docker | Docker daemon |
| usuário não-root | non-root user |
| reprodutibilidade de build | build reproducibility |

## Veja também

- [[03-Dominios/Java/Cloud-native e produção/03 - Empacotando o app numa imagem — o panorama|Empacotando o app numa imagem (panorama)]]
- [[03-Dominios/Java/Cloud-native e produção/07 - Jib — imagem daemonless|Jib]]
- [[03-Dominios/Java/Cloud-native e produção/09 - Native Image com Spring — Spring AOT na prática|Native Image com Spring]]
- [[03-Dominios/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Cloud Native Buildpacks — Documentation (CNCF incubating). https://buildpacks.io/docs/
- Paketo Buildpacks — Java How-To. https://paketo.io/docs/howto/java/
- Spring Boot Maven Plugin — `build-image`. https://docs.spring.io/spring-boot/maven-plugin/build-image.html
