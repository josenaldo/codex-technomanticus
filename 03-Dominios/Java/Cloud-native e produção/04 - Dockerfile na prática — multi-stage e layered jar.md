---
title: "Dockerfile na prática — multi-stage e layered jar"
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
  - docker
aliases:
  - "Dockerfile multi-stage"
---

# Dockerfile na prática — multi-stage e layered jar

> [!abstract] TL;DR
> Um Dockerfile de Spring Boot bem feito tem **dois estágios**: um **builder** que extrai o fat jar em camadas com `java -Djarmode=tools -jar app.jar extract --layers`, e um **runtime** que só copia cada camada com um `COPY` separado. Um `COPY` por camada faz o Docker reaproveitar cache — código muda toda hora, dependências quase nunca, então elas viram camadas distintas. A imagem base é uma **JRE** (não JDK), você roda como **usuário não-root** com `USER`, e o `ENTRYPOINT` vai em **exec-form** (`["java", ...]`) pra que o processo receba `SIGTERM` direito e desligue com graça. Esses são os ajustes que separam um container de demo de um container de produção.

## O que é

Um **multi-stage build** é um Dockerfile com mais de um bloco `FROM`. Cada `FROM` abre um **estágio** independente; o último estágio é o que vira a imagem final, e os anteriores são descartados — eles existem só pra produzir artefatos que o estágio final copia com `COPY --from=...`.

Aplicado a uma aplicação Java, a ideia é: o estágio **builder** pega o fat jar (o uber jar com tudo dentro), e o **explode** numa estrutura em camadas. O estágio **runtime** então copia essas camadas, uma por uma, e nunca toca no fat jar original. O resultado é uma imagem onde cada parte que muda em ritmos diferentes vira uma camada de Docker diferente.

A peça que torna isso possível no Spring Boot é o **`jarmode=tools`**: o próprio jar sabe se auto-extrair. O comando `java -Djarmode=tools -jar application.jar extract --layers` produz quatro pastas:

- `dependencies/` — as libs de terceiros (Spring, Jackson, driver de banco…). Mudam raramente.
- `spring-boot-loader/` — o loader que monta o classpath. Praticamente nunca muda.
- `snapshot-dependencies/` — dependências `-SNAPSHOT`, se houver. Mudam com mais frequência que as releases.
- `application/` — **o seu código** e os recursos. Muda a cada commit.

> [!info] "Layered jar" é literalmente isso
> O nome "layered jar" descreve a metadata que o Spring empacota dentro do fat jar dizendo *como* fatiar o conteúdo em camadas. O `jarmode=tools` lê essa metadata e materializa as pastas. Você não configura layout manualmente — vem pronto desde o Spring Boot 2.3.

## Por que importa

Pensa numa camada de Docker como uma caixa lacrada com um hash. Quando você faz `docker pull` ou um registry recebe um `push`, só viajam as camadas cujo hash mudou. Se você jogar **o jar inteiro num único `COPY`**, qualquer alteração de uma linha no seu código muda o hash daquela camada gigante — e toda ela (incluindo dezenas de megabytes de dependências que não mudaram) tem que ser reconstruída, repushada e repuxada.

Separando em camadas por **frequência de mudança**, o cenário comum (mexi no código, dependências intactas) só invalida a camada `application/`, que costuma ser a menor. Build mais rápido, push mais rápido, deploy mais rápido, menos banda. É a mesma lógica do cache de dependências do Maven, só que no nível da imagem.

Os outros três ajustes — JRE em vez de JDK, non-root, exec-form — não são sobre cache; são sobre **a imagem ser apropriada pra produção**:

- **JRE**: você não compila dentro do container de runtime, então o JDK (compilador, ferramentas) é peso morto e superfície de ataque extra.
- **Non-root**: se alguém escapar do processo, não quer que ele seja root dentro do container.
- **Exec-form**: define se o seu processo Java recebe ou não o `SIGTERM` que o orquestrador manda na hora de desligar — e isso decide se o [[03-Dominios/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|graceful shutdown]] funciona ou não.

## Como funciona

### Estágio builder e estágio runtime

O builder existe só pra trabalhar e ser jogado fora. Ele recebe o fat jar (via `COPY` do contexto de build ou `ARG`), roda a extração, e morre. Nada do builder vai pra imagem final exceto o que o runtime pedir explicitamente com `COPY --from=builder`.

```dockerfile
FROM bellsoft/liberica-openjre-debian:25-cds AS builder
WORKDIR /builder
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} application.jar
RUN java -Djarmode=tools -jar application.jar extract --layers --destination extracted
```

Depois do `RUN`, dentro de `/builder/extracted` existem as quatro pastas. O estágio de runtime começa do zero (outro `FROM`), e a única ponte entre eles é o `--from=builder`. Por isso o fat jar original **não entra** na imagem final: ele ficou no builder, que foi descartado.

> [!tip] Por que não extrair na mesma imagem?
> Sem multi-stage, o fat jar e as camadas extraídas conviveriam na mesma imagem — você pagaria o conteúdo duas vezes (jar inteiro + cópias extraídas). O estágio separado garante que só a forma extraída sobrevive.

### COPY por camada e o cache

Aqui está o coração da técnica. No runtime, **cada camada ganha o seu próprio `COPY`**, na ordem do que muda menos pro que muda mais:

```dockerfile
COPY --from=builder /builder/extracted/dependencies/ ./
COPY --from=builder /builder/extracted/spring-boot-loader/ ./
COPY --from=builder /builder/extracted/snapshot-dependencies/ ./
COPY --from=builder /builder/extracted/application/ ./
```

Cada `COPY` é uma instrução de Dockerfile, e **cada instrução vira uma camada**. A ordem importa por causa de como o cache de build funciona: o Docker reusa o cache de uma instrução enquanto tudo antes dela estiver idêntico. Colocando `dependencies/` primeiro e `application/` por último, um deploy típico (só o código mudou) reaproveita o cache das três primeiras camadas e só refaz a última.

Se você invertesse a ordem — `application/` primeiro — qualquer mudança de código invalidaria o cache de tudo que vem depois, jogando o benefício fora. **Mais estável em cima, mais volátil embaixo** é a regra.

### Base JRE, non-root e exec-form

Três decisões fecham o runtime pra produção:

**Base JRE.** Use uma imagem que tenha só a JRE, como `bellsoft/liberica-openjre-debian` ou `eclipse-temurin:<versão>-jre`. Sem compilador, sem ferramentas de build — menor e com menos CVEs pra escanear (assunto da [[03-Dominios/Java/Cloud-native e produção/05 - Imagem enxuta e segura — distroless e scanning|imagem enxuta e segura]]).

**Non-root.** Imagens rodam como root por padrão. Crie (ou reuse) um usuário sem privilégio e troque com `USER` antes do `ENTRYPOINT`:

```dockerfile
RUN useradd --system --no-create-home appuser
USER appuser
```

**Exec-form no ENTRYPOINT.** Existem duas formas de escrever `ENTRYPOINT`:

- **Exec-form** (array JSON): `ENTRYPOINT ["java", "-jar", "application.jar"]`. O Docker executa o `java` diretamente como **PID 1**, sem shell no meio.
- **Shell-form** (string): `ENTRYPOINT java -jar application.jar`. O Docker embrulha isso em `/bin/sh -c "..."`, então **o shell é o PID 1** e o `java` é filho dele.

A diferença é decisiva no shutdown. Quando o orquestrador quer parar o container, ele manda `SIGTERM` pro **PID 1**. Na exec-form, o PID 1 é a sua JVM — ela recebe o sinal e dispara o graceful shutdown. Na shell-form, o PID 1 é o `sh`, que **não repassa** sinais aos filhos; a JVM nunca vê o `SIGTERM`, fica viva até o `SIGKILL` brutal chegar (tipicamente uns 30s depois), e qualquer requisição em voo é cortada no meio. Detalhe aprofundado em [[03-Dominios/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|graceful shutdown e deploy sem downtime]].

> [!note] E o container-awareness?
> O Dockerfile só empacota; quem decide quanto de heap a JVM usa em runtime é o ergonomics lendo os limites do cgroup. Isso é o assunto de [[03-Dominios/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]] — o Dockerfile não precisa cravar `-Xmx`, basta passar limites de memória no `docker run`/Kubernetes que a JVM moderna respeita.

## Na prática

Dockerfile completo e válido pra um `order-service` empacotado com Maven:

```dockerfile
# ---- Estágio builder: extrai o fat jar em camadas ----
FROM bellsoft/liberica-openjre-debian:25-cds AS builder
WORKDIR /builder

# Aponta pro jar gerado em target/ (use build/libs/*.jar se for Gradle)
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} application.jar

# jarmode=tools explode o jar nas pastas dependencies/, spring-boot-loader/,
# snapshot-dependencies/ e application/
RUN java -Djarmode=tools -jar application.jar extract --layers --destination extracted

# ---- Estágio runtime: imagem final, só com as camadas ----
FROM bellsoft/liberica-openjre-debian:25-cds
WORKDIR /application

# Usuário não-root: nada roda como root na imagem final
RUN useradd --system --no-create-home --uid 1001 appuser

# Um COPY por camada — do que muda menos (dependencies) pro que muda mais
# (application). Maximiza reaproveitamento de cache entre builds.
COPY --from=builder /builder/extracted/dependencies/ ./
COPY --from=builder /builder/extracted/spring-boot-loader/ ./
COPY --from=builder /builder/extracted/snapshot-dependencies/ ./
COPY --from=builder /builder/extracted/application/ ./

# Garante que os arquivos pertençam ao usuário sem privilégio
RUN chown -R appuser:appuser /application
USER appuser

EXPOSE 8080

# Exec-form: a JVM é PID 1 e recebe SIGTERM direto -> graceful shutdown funciona.
# Note: este é o jar extraído (application.jar com referências às camadas),
# NÃO o fat jar original — que ficou no builder e foi descartado.
ENTRYPOINT ["java", "-jar", "application.jar"]
```

Build e run:

```bash
docker build -t order-service:1.0 .
docker run --rm -p 8080:8080 --memory=512m order-service:1.0
```

O `--memory=512m` é lido pelo cgroup e a JVM dimensiona o heap a partir dele — sem `-Xmx` fixo no Dockerfile.

## Armadilhas

### (1) Deixar o container rodando como root

Sem nenhuma instrução `USER`, o processo roda como root dentro do container. Se houver uma falha que permita execução de código, o atacante já começa como root naquele namespace — e, dependendo da configuração do host, isso pode virar ponto de partida pra escapar do container. Sempre crie um usuário sem privilégio e troque com `USER` antes do `ENTRYPOINT`. Custa duas linhas e fecha uma porta inteira.

### (2) ENTRYPOINT em shell-form não propaga SIGTERM

Escrever `ENTRYPOINT java -jar application.jar` (sem os colchetes) parece inofensivo, mas embrulha o comando num `/bin/sh -c`. O shell vira PID 1, recebe o `SIGTERM` do orquestrador e **não o repassa** pra JVM. Resultado: a aplicação ignora o pedido educado de desligar, segue atendendo até o `SIGKILL` chegar (em geral 30s depois), e toda requisição em andamento morre no meio — exatamente o oposto do [[03-Dominios/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|graceful shutdown]]. Use sempre exec-form: `ENTRYPOINT ["java", "-jar", "application.jar"]`.

### (3) Copiar o fat jar inteiro num único COPY

`COPY target/order-service.jar app.jar` seguido de `ENTRYPOINT ["java","-jar","app.jar"]` funciona — e joga fora todo o benefício de camadas. O jar inteiro vira **uma** camada monolítica; mudar uma linha de código invalida o hash dela inteira, forçando rebuild e repush de dezenas de MB de dependências que não mudaram. Em CI com muitos deploys, isso é desperdício constante de tempo e banda. Extraia em camadas com `jarmode=tools` e copie uma por uma.

### (4) Usar imagem JDK no runtime

`FROM eclipse-temurin:25-jdk` no estágio de runtime carrega compilador e ferramentas de build que você não usa pra *executar* — só pra *compilar*. Isso incha a imagem e aumenta a superfície de CVEs a escanear. No runtime use a variante `-jre` (ou distroless). O JDK, se precisar, fica só no builder.

## Em entrevista

### Frase pronta (inglês)

> For a production Spring Boot image I use a multi-stage Dockerfile. The builder stage extracts the fat jar into layers with `java -Djarmode=tools -jar app.jar extract --layers`, and the runtime stage copies each layer with a separate `COPY`, ordered from least to most volatile — dependencies first, application code last — so Docker reuses the cache when only my code changes. The runtime image is based on a JRE rather than a JDK, runs as a non-root user, and declares the `ENTRYPOINT` in exec form so the JVM becomes PID 1 and receives `SIGTERM` directly, which is what makes graceful shutdown actually work. Shell-form would put a shell as PID 1 and swallow the signal.

### Vocabulário

| Português | Inglês | Observação |
|---|---|---|
| build multi-estágio | multi-stage build | Vários `FROM`; só o último vira imagem |
| estágio builder | builder stage | Extrai as camadas e é descartado |
| imagem base | base image | JRE no runtime, não JDK |
| usuário não-root | non-root user | `USER` antes do `ENTRYPOINT` |
| forma exec | exec form | `ENTRYPOINT ["java", ...]`; JVM é PID 1 |
| forma shell | shell form | `ENTRYPOINT java ...`; engole o `SIGTERM` |
| sinal de término | SIGTERM | Sinal de parada graciosa enviado ao PID 1 |
| jar em camadas | layered jar | Metadata que diz como fatiar o fat jar |

## Veja também

- [[03-Dominios/Java/Cloud-native e produção/02 - A JVM dentro de um container|A JVM dentro de um container]]
- [[03-Dominios/Java/Cloud-native e produção/05 - Imagem enxuta e segura — distroless e scanning|Imagem enxuta e segura]]
- [[03-Dominios/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|Graceful shutdown e deploy sem downtime]]
- [[03-Dominios/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Spring Boot Reference — Packaging / Container Images / Dockerfiles: https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html
- Spring Boot Reference — Efficient Container Images (layered jars): https://docs.spring.io/spring-boot/reference/packaging/efficient.html
- Docker Docs — Multi-stage builds: https://docs.docker.com/build/building/multi-stage/
- Docker Docs — Dockerfile reference (`ENTRYPOINT`, exec vs shell form): https://docs.docker.com/reference/dockerfile/#entrypoint
