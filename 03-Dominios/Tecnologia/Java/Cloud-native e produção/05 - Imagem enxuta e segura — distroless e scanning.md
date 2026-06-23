---
title: "Imagem enxuta e segura — distroless e scanning"
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
  - seguranca
aliases:
  - "Distroless"
  - "Image scanning"
---

# Imagem enxuta e segura — distroless e scanning

> [!abstract] TL;DR
> Uma imagem de container Java baseada num Linux completo (Debian, Ubuntu) carrega centenas de pacotes que o seu app **nunca usa** — shell, `apt`, `curl`, libs de sistema — e cada um desses pacotes é uma porta a mais para um CVE. A resposta é a imagem **distroless**: `gcr.io/distroless/java21-debian13` contém **só o runtime Java e o seu app**, sem shell e sem gerenciador de pacotes. Isso encolhe a **superfície de ataque** e deixa o resultado do **scanning** muito mais limpo.
> Como não há shell, o `ENTRYPOINT` **tem** que ser exec-form (`["java", "-jar", "app.jar"]`): sem `/bin/sh` para interpretar a shell-form, o container nem sobe. Distroless ainda oferece variantes **`:nonroot`** (rodar sem ser root) e **`:debug`** (busybox embutido, só para investigar incidente).
> Mas imagem enxuta **não** dispensa **image scanning**: ferramentas como Trivy ou Grype varrem as camadas atrás de CVEs conhecidos no runtime e nas dependências. Distroless reduz o ruído; o scanner ainda é quem confirma que não sobrou vulnerabilidade. (O inventário formal de dependências — **SBOM** — é assunto do [[03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM|Galho 15]].)

## O que é

**Distroless** é uma família de imagens base mantida pelo Google (projeto `GoogleContainerTools/distroless`) que segue um princípio radical: a imagem contém **apenas o seu aplicativo e suas dependências de runtime** — nada da "distro" Linux que normalmente vem junto. Nas palavras do próprio README: *"Distroless images contain only your application and its runtime dependencies. They do not contain package managers, shells or any other programs you would expect to find in a standard Linux distribution."*

Para Java, o projeto publica imagens já com a JVM dentro:

- `gcr.io/distroless/java17-debian13`
- `gcr.io/distroless/java21-debian13`
- `gcr.io/distroless/java25-debian13`
- `gcr.io/distroless/java-base-debian13` (sem JDK/JRE, para você trazer o seu)

**Image scanning** é o outro lado da moeda: passar um scanner de vulnerabilidades (Trivy, Grype) sobre a imagem para listar os **CVEs** conhecidos nas suas camadas — no runtime, nas libs de sistema que sobraram e nas dependências do app. Distroless e scanning andam juntos: o primeiro reduz o que existe para ser atacado; o segundo verifica o que ainda restou.

## Por que importa

Toda linha de código que entra na imagem é código que **pode** ter uma vulnerabilidade — inclusive código que você nunca chama. Uma imagem `eclipse-temurin:21` (baseada em Ubuntu) traz bash, coreutils, glibc, openssl, gerenciador de pacotes: dezenas de componentes que existem só porque "vêm na distro". Cada um deles aparece no relatório do scanner, cada um pode ganhar um CVE amanhã, e nenhum deles é necessário para `java -jar app.jar` rodar.

Isso é o conceito de **superfície de ataque** (attack surface): quanto mais coisa há na imagem, mais pontos um atacante pode explorar — e, na prática mais imediata, mais ruído de CVE você precisa triar a cada build. Remover o shell, por exemplo, derruba uma classe inteira de ataques: um invasor que consegue injetar um comando não acha `/bin/sh` para executá-lo; quem escapa para dentro do container não tem `curl` para baixar a próxima ferramenta nem `apt` para instalar.

> [!tip] Analogia da bagagem de mão
> Pense numa imagem Linux completa como uma mala despachada cheia de "por via das dúvidas": guarda-chuva, kit de costura, três carregadores. Você atravessa a alfândega (o scanner) e cada item precisa ser justificado — e qualquer um deles pode estar com a validade vencida (um CVE).
> A distroless é a bagagem de mão minimalista: só passaporte e celular (o runtime e o app). A alfândega passa rápido, porque há quase nada para inspecionar. E não tem o canivete esquecido no fundo (o shell) para o segurança confiscar.

A consequência prática é dupla: imagens **menores** (pull mais rápido, menos custo de registry) e relatórios de scanning **mais curtos e acionáveis** — quando aparece um CVE, é provável que seja algo que realmente importa, não um pacote de sistema que você nem usa.

## Como funciona

### Distroless: o que é e por que encolhe a superfície

A imagem distroless é montada **sem** o sistema de pacotes de uma distro. Não há `apt`/`apk`, não há `/bin/bash` nem `/bin/sh`, não há `ls`, `cat`, `ps`. Há o filesystem mínimo (algumas libs de sistema, certificados de CA, fuso horário) mais — nas variantes Java — a JVM. O seu `app.jar` é a única coisa "sua" lá dentro.

O ganho de segurança vem de três frentes ao mesmo tempo:

1. **Menos pacotes = menos CVEs possíveis.** Cada pacote ausente é um vetor de vulnerabilidade que simplesmente não existe na sua imagem.
2. **Sem shell = sem pivô.** Boa parte das técnicas de pós-exploração (command injection que vira RCE, scripts que baixam payloads) depende de um shell. Distroless não oferece um.
3. **Sem gerenciador de pacotes = imutabilidade.** Ninguém instala nada em runtime; a imagem é o que você buildou, ponto.

### Non-root: não rodar como root

Por padrão, um processo em container roda como **root** (uid 0). Se algo escapa do isolamento do container, esse root pode virar acesso privilegiado no host. A boa prática é rodar como **usuário não-root** (non-root). Distroless facilita: cada imagem tem uma variante **`:nonroot`** (e `:debug-nonroot`) que já vem com um usuário sem privilégios pré-configurado.

Você ativa isso escolhendo a tag certa e/ou declarando o usuário no Dockerfile:

```dockerfile
FROM gcr.io/distroless/java21-debian13:nonroot
USER nonroot
```

O princípio é o **menor privilégio**: o processo recebe só o que precisa para servir requisições — e servir requisições não exige ser root.

### Image scanning: varrer CVEs nas camadas

Um scanner de imagem (Trivy, Grype) abre cada **camada** da imagem, identifica os pacotes e versões presentes (sistema operacional + dependências da aplicação) e cruza com bases públicas de vulnerabilidades. O resultado é uma lista de **CVEs** com severidade (low/medium/high/critical), o pacote afetado e, quando existe, a versão que corrige.

> [!info] Conceitual, não cravado em versão
> Trivy e Grype são as ferramentas open-source mais citadas para esse papel, mas a mecânica vale para qualquer scanner. Não fixo versões aqui porque a interface de linha de comando e o catálogo de CVEs mudam com frequência — o que importa é o **conceito**: build → scan → falha o pipeline se aparecer CVE acima do limite que você tolera.

O scanning costuma virar um **gate de CI**: o build falha se a imagem tiver vulnerabilidade `HIGH`/`CRITICAL` com correção disponível. É aí que distroless e scanning se reforçam — a base enxuta entrega menos achados, e o gate garante que mesmo os poucos que aparecem sejam tratados antes do deploy.

## Na prática

Um Dockerfile multi-stage que termina numa base distroless non-root. O estágio de build usa uma imagem completa (com shell, para extrair o jar); o estágio final é distroless:

```dockerfile
# --- estágio de build (imagem completa, tem shell) ---
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /build
COPY . .
RUN ./mvnw -q clean package -DskipTests \
 && java -Djarmode=tools -jar target/catalog-service.jar extract --layers --destination extracted

# --- estágio final (distroless, sem shell, non-root) ---
FROM gcr.io/distroless/java21-debian13:nonroot
WORKDIR /app
COPY --from=builder /build/extracted/dependencies/ ./
COPY --from=builder /build/extracted/spring-boot-loader/ ./
COPY --from=builder /build/extracted/snapshot-dependencies/ ./
COPY --from=builder /build/extracted/application/ ./

USER nonroot
# exec-form OBRIGATÓRIO: distroless não tem shell para interpretar shell-form
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
```

Repare em dois pontos: o `ENTRYPOINT` está em **exec-form** (lista JSON) — em shell-form (`ENTRYPOINT java -jar ...`) o runtime tentaria prefixar com `/bin/sh`, que **não existe** na distroless, e o container não sobe. E a base é `:nonroot`, com o `USER nonroot` reforçando o uid sem privilégios.

Escaneando a imagem resultante (conceitual — a sintaxe exata depende da ferramenta e da versão):

```bash
# 1) builda a imagem
docker build -t catalog-service:latest .

# 2) escaneia atrás de CVEs nas camadas (exemplo conceitual)
trivy image catalog-service:latest
# ou
grype catalog-service:latest

# 3) num pipeline, falha o build se houver CVE alto/crítico com fix:
trivy image --severity HIGH,CRITICAL --exit-code 1 catalog-service:latest
```

O `--exit-code 1` é o que transforma o scan num gate: vulnerabilidade acima do limite → o passo de CI retorna erro → o deploy não acontece.

## Armadilhas

### (1) Debugar uma distroless "normal" — não há shell

Bateu o incidente em produção, você faz `docker exec -it <container> sh`… e recebe um erro: não existe `sh`, nem `bash`, nem `ls`. A imagem distroless padrão **não tem shell de propósito**. Para investigar, use a variante **`:debug`** (ou `:debug-nonroot`), que embute um **busybox** com um shell mínimo — pensada exatamente para entrar no container e olhar de perto. A regra: rode `:nonroot` em produção, troque para `:debug` só quando precisar investigar (e volte depois). Tratar a ausência de shell como bug, e não como feature, é o erro de quem está chegando agora na distroless.

### (2) Base sem pin / usar `:latest`

`FROM gcr.io/distroless/java21-debian13` (sem tag explícita) ou `:latest` faz o build pegar "o que estiver lá hoje". Isso quebra a **reprodutibilidade** (o mesmo Dockerfile gera imagens diferentes em dias diferentes) e esconde regressões de segurança: você não sabe qual base entrou. Fixe a tag (`:nonroot`) e, em cenários mais rígidos, **pin por digest** (`@sha256:...`) para garantir que a base é byte-a-byte a que você auditou. Imagem imutável só é imutável se a base também for fixada.

### (3) Achar que distroless dispensa o scanning

A tentação é pensar: "minha base é mínima, logo é segura, não preciso escanear". Falso. Distroless **reduz** a superfície, não a zera — a JVM, as libs de sistema que restam e, principalmente, as **suas dependências de aplicação** (todo o `BOOT-INF/lib`) continuam podendo ter CVEs. Um Log4Shell da vida mora nas **suas** dependências, não na distro. Distroless e scanning são camadas **complementares**: a base enxuta diminui o ruído, o scanner confirma que não sobrou nada crítico. Pular o scan porque a base é distroless é confundir "menos provável" com "impossível".

## Em entrevista

### Frase pronta (inglês)

> For production Java images I default to a distroless base like `gcr.io/distroless/java21-debian13`: it ships only the JVM and my application, with no shell and no package manager, which shrinks the attack surface and gives me much cleaner vulnerability scans. Because there's no shell, the `ENTRYPOINT` must be in exec form, and I run the `:nonroot` variant so the process never runs as root. Distroless reduces the noise but it doesn't replace image scanning — I still run Trivy or Grype in CI and fail the build on high or critical CVEs, since my own application dependencies can be vulnerable regardless of how minimal the base is. When I need to troubleshoot a running container, I swap in the `:debug` variant, which bundles a busybox shell for that purpose only.

### Vocabulário

| PT-BR | Inglês |
| --- | --- |
| imagem sem distro / distroless | distroless image |
| superfície de ataque | attack surface |
| escaneamento de imagem | image scanning |
| vulnerabilidade conhecida | CVE / known vulnerability |
| usuário não-root | non-root user |
| imagem mínima | minimal image |
| menor privilégio | least privilege |
| gate de CI (build falha) | CI gate / failing the build |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/04 - Dockerfile na prática — multi-stage e layered jar|Dockerfile na prática]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile|Buildpacks]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM|Supply chain e SBOM (Galho 15)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

> [!note] Fronteira com o Galho 15
> O **SBOM** (Software Bill of Materials) — o inventário formal e assinado de tudo que entra na imagem, base da rastreabilidade de supply chain — é assunto do [[03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM|Galho 15]]. Aqui, no Galho 17, o foco é a **imagem de produção** em si: base enxuta, non-root e o scanning que roda sobre ela. Scanner e SBOM se complementam — um lista as vulnerabilidades, o outro lista os componentes —, mas vivem em galhos diferentes.

## Referências

- GoogleContainerTools/distroless — README e catálogo de imagens (Java 17/21/25, variantes `nonroot` e `debug`, ausência de shell e package manager, ENTRYPOINT exec-form): <https://github.com/GoogleContainerTools/distroless>
- Trivy — scanner de vulnerabilidades de container (Aqua Security): <https://github.com/aquasecurity/trivy>
- Grype — scanner de vulnerabilidades (Anchore): <https://github.com/anchore/grype>
