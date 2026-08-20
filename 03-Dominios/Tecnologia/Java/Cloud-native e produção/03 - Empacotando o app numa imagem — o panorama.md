---
title: "Empacotando o app numa imagem — o panorama"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - cloud-native
  - iniciado
  - container
aliases:
  - "Imagem de container"
  - "Layered jar"
---

# Empacotando o app numa imagem — o panorama

> [!abstract] TL;DR
> Em produção cloud-native, o artefato que importa não é mais o `jar` — é a **imagem de container** (OCI). O `jar` é só o conteúdo; a imagem é a mala despachada que o orquestrador (Kubernetes, ECS) sabe rodar. O Spring Boot transforma o `jar` num **layered jar**: ele carrega um índice (`layers.idx`) que descreve **4 camadas** — `dependencies`, `spring-boot-loader`, `snapshot-dependencies` e `application` — ordenadas da que **menos muda** para a que **mais muda**. Extrair essas camadas com `java -Djarmode=tools -jar app.jar extract --layers` e copiá-las separadas na imagem faz o Docker **reaproveitar cache de layers**: você rebuilda só a camada de aplicação, não as centenas de MB de dependências. Há **3 vias** de construir a imagem: Dockerfile à mão ([[03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar|nota 04]]), Buildpacks ([[03-Dominios/Tecnologia/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile|nota 06]]) e Jib ([[03-Dominios/Tecnologia/Java/Cloud-native e produção/07 - Jib — imagem daemonless|nota 07]]). **Não confunda** com o empacotamento do *JAR* (fat/thin/repackage) — isso é o [[03-Dominios/Tecnologia/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage|Galho 15]]. Aqui o assunto é a **imagem de container**.

## O que é

Empacotar o app numa imagem é embrulhar o `jar` já construído — junto com um runtime Java e o sistema de arquivos mínimo — num artefato **OCI** (Open Container Initiative), o formato padrão que Docker, containerd e os orquestradores entendem.

Pense em duas etapas distintas:

1. **Build do JAR** — o Maven/Gradle produz um `app.jar` executável. *Como* esse jar é montado (fat, thin, repackage) é território do [[03-Dominios/Tecnologia/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage|Galho 15]]. Esta nota **não re-explica** isso.
2. **Build da IMAGEM** — pegamos esse `app.jar` e o transformamos numa **imagem de container** pronta pra subir num registry e rodar num cluster. É **isto** que esta nota cobre.

O pulo do gato do Spring Boot é o **layered jar**: em vez de tratar o jar como um bloco monolítico, ele o organiza em camadas declaradas num arquivo de índice chamado `layers.idx`, embutido no próprio jar. Cada camada agrupa partes que mudam no **mesmo ritmo**.

## Por que importa

Imagem de container é a moeda de troca da produção moderna. Você não faz `scp` de um `jar` para um servidor; você empurra uma **imagem** para um **registry** (Docker Hub, ECR, GHCR) e o orquestrador a baixa.

O problema: uma imagem Java carrega facilmente centenas de MB de dependências (Spring, drivers, bibliotecas). Se a imagem for uma camada única, **qualquer** mudança no código — uma linha — invalida o cache inteiro: o build copia tudo de novo, o push sobe tudo de novo, o pull no cluster baixa tudo de novo.

O **layered jar** resolve isso separando o que muda devagar do que muda toda hora. As dependências (que mudam só quando você troca uma versão) ficam numa camada estável; o seu código (que muda a cada commit) fica isolado na última. O Docker, que faz cache **por camada**, reaproveita as camadas estáveis e reconstrói só a de cima. Resultado: builds e deploys muito mais rápidos, e menos tráfego de rede.

> [!tip] Analogia das malas despachadas
> Imagine empacotar uma viagem. A **mala de equipamento pesado** (barraca, fogareiro) raramente muda entre viagens — você reaproveita a mesma toda vez. A **mala de roupas** muda a cada estação. E a **mochila de mão** (documentos, celular) muda **toda viagem**. Se você jogar tudo numa única mala gigante, qualquer trocinha exige refazer a mala inteira. Separando por **ritmo de mudança**, você só remonta a mochila de mão. As camadas do jar são exatamente isso: deps = mala pesada (quase imutável), `application` = mochila de mão (sempre muda).

## Como funciona

### O layered jar e o `jarmode=tools`

O Spring Boot embute no `jar` um índice `layers.idx` que lista as camadas **na ordem em que devem entrar na imagem** (da mais estável para a mais volátil). As 4 camadas padrão são:

| Camada | Conteúdo | Muda... |
| --- | --- | --- |
| `dependencies` | Dependências de versão lançada (released) | raramente |
| `spring-boot-loader` | Classes do loader do Boot (`org/springframework/boot/loader`) | quase nunca |
| `snapshot-dependencies` | Dependências `-SNAPSHOT` (em desenvolvimento) | às vezes |
| `application` | Suas classes e recursos (`BOOT-INF/classes`, manifest) | sempre |

Para fatiar o jar nessas camadas no disco, o Boot 3.x oferece o **jarmode** `tools`:

```bash
java -Djarmode=tools -jar app.jar extract --layers --destination extracted
```

Isso usa a lib `spring-boot-jarmode-tools` (adicionada automaticamente) e cria um diretório por camada dentro de `extracted/`.

> [!warning] Boot 2.x usava outro nome
> No Spring Boot 2.x o comando era `java -Djarmode=layertools -jar app.jar extract`. No **Boot 3.x** o jarmode foi renomeado para `tools` e o comando passou a ser `-Djarmode=tools ... extract --layers`. Use sempre `tools` em projetos atuais.

### O cache de layers

A mágica acontece quando cada camada extraída vira uma **layer de imagem separada**. Num Dockerfile multi-stage, você copia uma por vez:

```dockerfile
COPY --from=builder /builder/extracted/dependencies/ ./
COPY --from=builder /builder/extracted/spring-boot-loader/ ./
COPY --from=builder /builder/extracted/snapshot-dependencies/ ./
COPY --from=builder /builder/extracted/application/ ./
```

Como o Docker faz cache **por instrução/camada**, e as camadas estão ordenadas da menos volátil (em cima) para a mais volátil (embaixo), um rebuild que só mudou o código invalida apenas a última `COPY` (`application/`). As três de cima vêm do cache — não são reconstruídas, nem reempurradas para o registry, nem rebaixadas no cluster.

A regra de ouro: **ordem importa**. Camada estável primeiro, volátil por último. Inverter a ordem destrói o ganho de cache.

### As 3 vias em resumo

Extrair camadas e escrever `COPY` à mão é só **uma** das formas. Há três, cada uma com seu trade-off:

| Via | Como funciona | Nota |
| --- | --- | --- |
| **Dockerfile à mão** | Você escreve o `Dockerfile` multi-stage, extrai com `jarmode=tools` e copia camada a camada. Controle total. | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar|nota 04]] |
| **Buildpacks** | `mvn spring-boot:build-image` gera a imagem **sem Dockerfile**; o buildpack já aplica as camadas e escolhe um base image seguro. | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile|nota 06]] |
| **Jib** | Plugin Maven/Gradle que constrói a imagem **sem daemon Docker** e já organiza camadas otimizadas. | [[03-Dominios/Tecnologia/Java/Cloud-native e produção/07 - Jib — imagem daemonless|nota 07]] |

As três respeitam o mesmo princípio de **separação por ritmo de mudança**; mudam o quanto de controle e quanto de cerimônia você assume.

## Na prática

Extraindo as camadas de um `order-service` para inspecionar o resultado:

```bash
# Boot 3.x — fatia o jar nas 4 camadas
java -Djarmode=tools -jar order-service.jar extract --layers --destination extracted

# inspeciona o que saiu
ls extracted/
```

O índice `layers.idx` dentro do jar descreve a estrutura assim (esquemático):

```text
- "dependencies":
  - BOOT-INF/lib/spring-context-6.x.jar
  - BOOT-INF/lib/postgresql-42.x.jar
- "spring-boot-loader":
  - org/springframework/boot/loader/launch/JarLauncher.class
- "snapshot-dependencies":
  - BOOT-INF/lib/order-shared-1.0-SNAPSHOT.jar
- "application":
  - META-INF/MANIFEST.MF
  - BOOT-INF/classes/com/acme/order/OrderApplication.class
```

E o diretório `extracted/` resultante tem uma pasta por camada:

```text
extracted/
├── dependencies/
├── spring-boot-loader/
├── snapshot-dependencies/
└── application/
```

A partir daqui, qualquer das 3 vias monta a imagem reaproveitando essa separação. A nota 04 mostra o Dockerfile multi-stage completo que consome exatamente esse `extracted/`.

## Armadilhas

### (1) Jar gordo numa camada só — perde o cache de layers

A armadilha mais comum: tratar a imagem como um bloco monolítico — um `COPY app.jar` único, ou um `ADD` de tudo numa camada só. Funciona, mas **joga fora** todo o ganho do layered jar. Qualquer mudança de código invalida a camada inteira (deps incluídas), e cada deploy reempurra/rebaixa centenas de MB que não mudaram. O ponto inteiro de extrair as camadas é colocar `dependencies` em cima (estável) e `application` embaixo (volátil). Se elas estão juntas, não há o que cachear.

### (2) Confundir o empacotamento do JAR (G15) com a imagem

`fat jar`, `thin jar` e `repackage` descrevem como o **JAR** é montado — assunto do [[03-Dominios/Tecnologia/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage|Galho 15]]. **Imagem de container**, **layered jar** e **cache de layers** descrevem como a **IMAGEM** é montada — assunto desta nota. São etapas diferentes: primeiro você produz o jar (G15), depois embrulha esse jar numa imagem (aqui). Misturar os dois numa resposta de entrevista (ou num pipeline) denuncia que você não separou as camadas mentais do problema. O layered jar **pressupõe** um jar já empacotado; ele só o re-organiza para a imagem.

## Em entrevista

### Frase pronta (inglês)

> In a cloud-native setup, the deployable artifact isn't the jar anymore — it's an OCI container image, and a naive single-layer image kills build and deploy performance. Spring Boot solves this with a layered jar: a `layers.idx` index splits the archive into four layers — dependencies, spring-boot-loader, snapshot-dependencies and application — ordered from least to most frequently changed. I extract them with `java -Djarmode=tools -jar app.jar extract --layers` and copy each into its own image layer, so Docker's layer caching only rebuilds and re-pushes the application layer on a typical code change. Depending on the team, I'll do this with a hand-written multi-stage Dockerfile, with Cloud Native Buildpacks for a Dockerfile-free build, or with Jib when there's no Docker daemon available.

### Vocabulário

| PT-BR | Inglês |
| --- | --- |
| imagem de container | container image |
| camada | layer |
| cache de camadas | layer caching |
| jar em camadas | layered jar |
| imagem OCI | OCI image |
| registro | registry |
| build multi-estágio | multi-stage build |
| ritmo de mudança | change frequency / churn |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar|Dockerfile na prática]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile|Buildpacks]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/07 - Jib — imagem daemonless|Jib]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/15 - Empacotamento — fat jar, thin jar e repackage|Empacotamento (Galho 15)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

> [!note] Adiante no galho
> Depois de saber empacotar a imagem, o próximo passo natural é como o app **se comporta em produção** (configuração externalizada, observabilidade, graceful shutdown) — o miolo deste mesmo galho, das notas 10 em diante.

## Referências

- Spring Boot Reference — *Efficient Container Images / Layering Docker Images*: <https://docs.spring.io/spring-boot/reference/packaging/container-images/efficient-images.html>
- Spring Boot Reference — *Dockerfiles*: <https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html>
