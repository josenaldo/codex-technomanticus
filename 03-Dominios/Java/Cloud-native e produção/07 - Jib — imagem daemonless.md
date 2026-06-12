---
title: "Jib — imagem daemonless"
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
  - "Jib"
---

# Jib — imagem daemonless

> [!abstract] TL;DR
> **Jib** (`com.google.cloud.tools:jib`, do Google, v3.5.x) builda imagem OCI/Docker **sem Docker daemon e sem Dockerfile**, direto de um plugin Maven ou Gradle. Faz **layering automático** (separa dependências de classes — só a camada que mudou é reconstruída) e gera builds **reprodutíveis** (mesmo conteúdo → exatamente a mesma imagem). Empurra a imagem direto pro registry. Contraste com [[03-Dominios/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile|Buildpacks]]: lá o lifecycle CNB precisa do daemon; aqui o plugin resolve tudo sozinho, daemonless.

## O que é

**Jib** é uma ferramenta do Google (`GoogleContainerTools/jib`) que constrói imagens de container OCI/Docker para aplicações Java **sem você escrever um Dockerfile** e **sem precisar de um Docker daemon rodando**. Ela vive como plugin do seu build: `jib-maven-plugin` ou `jib-gradle-plugin` (também existe a Jib CLI e a Jib Core como biblioteca). A versão atual da família é a **3.5.x**.

A ideia central: o build já sabe quais são suas dependências e quais são suas classes. Por que então delegar isso a um `Dockerfile` que copia um JAR gordo numa camada única? Jib pega esse conhecimento e monta a imagem camada por camada, ele mesmo, falando direto com o registry pelo protocolo da Registry API.

Pense no Dockerfile clássico como uma receita que você dita a um cozinheiro (o daemon) na cozinha (o Docker). Jib dispensa cozinheiro e cozinha: ele monta o prato e o entrega na mesa (o registry) sem intermediário.

## Por que importa

- **Sem daemon, sem Dockerfile.** Em CI/CD, isso elimina a necessidade de Docker-in-Docker ou de um socket de daemon privilegiado no agente de build. Menos superfície de configuração, menos atrito de permissão.
- **Builds rápidos por layering inteligente.** Como dependências e classes ficam em camadas separadas, mudar uma linha do seu código reconstrói só a camada de classes — as dependências (que mudam raramente) vêm do cache. Rebuilds ficam muito mais rápidos.
- **Reprodutibilidade.** Mesmo conteúdo gera exatamente a mesma imagem (mesmo digest), o que evita redeploys desnecessários e torna o pipeline determinístico.
- **Integração nativa ao build.** Está no `pom.xml`/`build.gradle`, não num arquivo paralelo. Quem mexe no build mexe na imagem, no mesmo lugar.

## Como funciona

### Daemonless e sem Dockerfile

Jib não usa o Docker daemon para o caminho padrão (`jib:build`). Ele constrói a imagem em memória/disco e fala o protocolo do registry diretamente, fazendo **push** da imagem para lá. Não há `docker build`, não há `Dockerfile`, não há daemon. A imagem de base, as dependências e suas classes são montadas pelo próprio plugin.

Quando você *quer* o daemon (por exemplo, para carregar a imagem localmente e testar com `docker run`), existe o goal `jib:dockerBuild`, que aí sim usa o daemon. Mas isso é a exceção, não a regra.

### Layering automático + reproducible

Jib particiona a aplicação em camadas distintas, separando **dependências** de **classes** (e tipicamente também recursos/`resources` e snapshots). A consequência prática:

- Você muda só seu código → a camada de classes é reconstruída, a de dependências vem do cache → push rápido.
- Você adiciona uma dependência → a camada de deps muda, mas a base permanece.

Além disso, o build é **reproducible**: rodar de novo com o mesmo conteúdo produz a mesma imagem. Jib normaliza timestamps e ordenação para que o digest seja estável. Isso é o oposto do Dockerfile ingênuo, onde um `COPY` com timestamp atual gera uma imagem diferente a cada build, mesmo sem mudança de conteúdo.

### Buildpacks vs Jib

Os dois resolvem o mesmo problema — gerar imagem sem Dockerfile — por caminhos diferentes:

| Eixo | Buildpacks (nota 06) | Jib |
| --- | --- | --- |
| Quem monta | lifecycle CNB (Paketo, etc.) | plugin Maven/Gradle do Google |
| Precisa de daemon? | Sim (o lifecycle roda em container) | **Não** (`jib:build` é daemonless) |
| Acoplamento | detecta a stack genericamente | focado em Java, conhece o build |
| Camadas | gerenciadas pelo buildpack | layering automático deps/classes |

Buildpacks são mais agnósticos de linguagem e trazem opinião de runtime pronta; Jib é mais cirúrgico para Java e dispensa o daemon. Para o panorama completo das opções de empacotamento, veja [[03-Dominios/Java/Cloud-native e produção/03 - Empacotando o app numa imagem — o panorama|Empacotando o app numa imagem (panorama)]].

## Na prática

Plugin Maven no `pom.xml`, apontando para a imagem de destino no registry:

```xml
<build>
  <plugins>
    <plugin>
      <groupId>com.google.cloud.tools</groupId>
      <artifactId>jib-maven-plugin</artifactId>
      <version>3.5.3</version>
      <configuration>
        <to>
          <image>registry.example.com/equipe/servico-pedidos:latest</image>
        </to>
      </configuration>
    </plugin>
  </plugins>
</build>
```

Construir e empurrar direto pro registry, sem daemon:

```bash
# Build daemonless: monta a imagem e faz push pro registry
mvn compile jib:build

# Variante que usa o Docker daemon local (para testar com docker run)
mvn compile jib:dockerBuild
```

`jib:build` é o caminho padrão (daemonless, push direto). `jib:dockerBuild` existe para quando você quer a imagem carregada no daemon local.

## Armadilhas

### (1) Assumir que Jib precisa de Docker

A confusão mais comum: achar que, por gerar imagem, Jib exige um Docker daemon. **Não exige.** O goal padrão `jib:build` é daemonless — ele fala direto com o registry. Você só toca no daemon se escolher `jib:dockerBuild` de propósito. Em pipelines de CI, isso é justamente a vantagem: você não precisa subir Docker-in-Docker nem montar o socket privilegiado.

### (2) Customização mais limitada que um Dockerfile

Jib é opinativo e otimizado para o caso Java. Se sua imagem exige passos arbitrários de build (instalar pacotes do SO, rodar scripts de provisionamento, comandos `RUN` complexos), você bate no teto: Jib não executa um shell arbitrário durante o build como um `Dockerfile` faria. Dá para ajustar base image, entrypoint, portas, labels, usuário e arquivos extras, mas não é um substituto de propósito geral para Dockerfiles cheios de `RUN`. Avalie o trade-off antes de adotar.

### (3) Credenciais de registry mal configuradas

Como o push é direto pro registry, Jib precisa autenticar. Falha de credencial é a causa nº 1 de build quebrado. Jib resolve credenciais a partir de credential helpers (Docker config / helper do provedor de nuvem), do `settings.xml` do Maven ou de configuração explícita do plugin. Se o helper não está instalado ou o token expirou, o push falha com erro de autorização. Garanta que o ambiente de CI tenha o credential helper certo (ou as credenciais injetadas) antes de rodar `jib:build`.

## Em entrevista

### Frase pronta (inglês)

> Jib is a Google build plugin that produces OCI images for Java apps **without a Docker daemon and without a Dockerfile** — the default `jib:build` goal pushes straight to the image registry. It does **automatic layering**, separating dependencies from application classes, so only the changed layer is rebuilt and rebuilds stay fast. The builds are also **reproducible**: the same content yields the same image, which avoids needless redeploys. Compared to Buildpacks, which need a daemon to run the CNB lifecycle, Jib is daemonless and tightly integrated into the Maven or Gradle build.

### Vocabulário

| Português | Inglês |
| --- | --- |
| sem daemon | daemonless |
| camadas automáticas | automatic layering |
| reprodutível | reproducible |
| registro de imagem | image registry |
| empurrar (subir imagem) | push |
| plugin de build | build plugin |
| imagem de base | base image |
| sem Dockerfile | Dockerfile-less |

## Veja também

- [[03-Dominios/Java/Cloud-native e produção/03 - Empacotando o app numa imagem — o panorama|Empacotando o app numa imagem (panorama)]]
- [[03-Dominios/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile|Buildpacks]]
- [[03-Dominios/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- [GoogleContainerTools/jib — repositório oficial](https://github.com/GoogleContainerTools/jib) — "Jib builds optimized Docker and OCI images for your Java applications without a Docker daemon"; layering automático (deps vs classes), reproducible builds, plugins Maven/Gradle, Jib CLI e Jib Core. Família v3.5.x (jib-gradle-plugin 3.5.3, fev/2026).
