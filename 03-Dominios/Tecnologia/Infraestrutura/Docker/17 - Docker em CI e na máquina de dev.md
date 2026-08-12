---
title: "Docker em CI e na máquina de dev"
created: 2026-08-02
updated: 2026-08-02
type: concept
fase: Magus
status: seedling
publish: true
tags:
  - infraestrutura
  - docker
  - ci-cd
  - testes
---

# Docker em CI e na máquina de dev

> [!abstract] TL;DR
> Um Dockerfile que constrói em 20 segundos na sua máquina pode levar minutos no pipeline — não porque o pipeline seja mais lento, mas porque o executor de CI nasce e morre a cada execução, e com ele morre o cache de camadas que a nota 05 mostrou ser o motor da velocidade local. A resposta é tornar o cache exportável para fora da máquina descartável, e escolher com cuidado como o job de CI fala com um daemon Docker sem repetir o erro que a nota 13 já condenou — montar o socket do host é entregar a máquina para quem quer que controle esse job. Do outro lado do mesmo problema, Testcontainers usa exatamente essa mesma imagem imutável para eliminar o mock de infraestrutura em testes de integração, e um ambiente de desenvolvimento em container aplica bind mount e recarga automática sem nunca virar forma de distribuir software. A imagem como artefato atravessa os três: o que constrói, o que testa e o que roda em dev é, ou deveria ser, a mesma peça imutável vista de três ângulos.

Um time que acabou de adotar CI para um monorepo Node percebe algo estranho: o build local do serviço de checkout leva 20 segundos porque `npm ci` está em cache — a camada não mudou desde ontem. No pipeline, o mesmo Dockerfile, o mesmo `package-lock.json` intocado, leva 4 minutos. Alguém sugere "deve ser a máquina do CI, que é mais fraca". Não é. É que a máquina do CI não existe mais depois que o job termina. Ela é provisionada, roda o job, e é descartada — sem disco persistente, sem `/var/lib/docker` acumulado de builds anteriores. Toda vez que `RUN npm ci` executa num executor novo, ele executa contra um cache vazio, porque não há cache: há só a promessa de uma máquina limpa a cada vez.

A primeira hipótese do time costuma ser sobre hardware — "o executor de CI tem menos CPU, menos I/O" — e vale a pena descartá-la rápido, porque geralmente não é isso: executores de CI hospedados modernos têm recursos comparáveis a um laptop de desenvolvimento razoável, às vezes superiores. A segunda hipótese, mais próxima da verdade mas ainda incompleta, é "o download de dependências está mais lento na rede do provedor" — o que às vezes é parcialmente verdade, mas não explica por que o mesmo download, na mesma rede, é rápido na segunda execução de um pipeline bem configurado e lento de novo na terceira, se a terceira caiu num executor físico diferente do da segunda.

A explicação completa só aparece quando alguém compara a saída de `docker build` local com a saída do mesmo comando em CI: localmente, a maioria das linhas do log aparece marcada como `CACHED`; em CI, sem configuração adicional, nenhuma linha aparece assim — cada instrução é executada de verdade, do zero, porque o daemon que roda o build nunca viu aquele Dockerfile antes. É essa diferença, visível literalmente no log de build, que separa "máquina mais lenta" (falso) de "máquina sem memória do que já construiu antes" (verdadeiro).

Esse é o ponto de partida desta nota: o Dockerfile não muda entre a máquina do desenvolvedor e o pipeline, mas o ambiente ao redor dele muda radicalmente — e são exatamente as garantias que a nota 05 deu como certas (cache local persistente, contexto de build estável) que precisam ser reconstruídas artificialmente em CI. A segunda metade da nota olha para o mesmo artefato — a imagem — de um ângulo diferente: não como algo que se constrói, mas como algo que se consome, em testes de integração via Testcontainers e em ambientes de desenvolvimento inteiros rodando dentro de um container.

## O problema estrutural do cache em CI

Na sua máquina, o cache de build vive no daemon local: cada layer construída fica em `/var/lib/docker`, e o próximo `docker build` reaproveita as que não mudaram, na cascata que a nota 05 descreveu — mude o `package.json` e tudo depois dele reconstrói; mude só o código-fonte e as layers de instalação de dependências sobrevivem. Esse mecanismo depende de uma coisa que parece óbvia até que falte: a mesma máquina construindo a mesma imagem duas vezes seguidas.

Um executor de CI hospedado (GitHub Actions, GitLab CI, CircleCI, e a maioria dos serviços equivalentes) não oferece essa continuidade por padrão. Cada execução de job normalmente sobe uma VM ou container novo, roda os passos, e desmonta tudo — incluindo qualquer camada de imagem que tenha sido construída durante o job. Do ponto de vista do daemon Docker rodando naquele executor, é sempre a primeira vez que ele vê aquele Dockerfile. Cache miss em toda instrução `RUN`, sempre.

O efeito é sistemático, não aleatório: builds de CI tendem a ser dominados pelo tempo das instruções que baixam e instalam dependências — `npm ci`, `pip install`, `mvn dependency:resolve`, `apt-get install` — porque são exatamente essas instruções que, localmente, o cache elimina na maioria das execuções. Multiplique isso por dezenas de pipelines rodando em paralelo, cada um pagando o preço total do download, e o custo agregado de "cache que não existe" vira uma linha visível na fatura de minutos de CI.

### Cache exportável: registry e cache do provedor

A saída não é fingir que o executor tem disco persistente — é tirar o cache de dentro do executor e colocá-lo em algum lugar que sobrevive entre execuções. A nota 10 já apontou para cá ao descrever o `--cache-from` e o `--cache-to` do BuildKit: o mecanismo que torna o cache **exportável**, não apenas local.

Duas famílias de destino são comuns:

**Cache no próprio registry de imagens.** O BuildKit pode empacotar o cache de camadas como um artefato paralelo à imagem final e publicá-lo num registry — o mesmo registry (Docker Hub, GHCR, ECR, ...) que a nota 12 descreveu para as imagens. Antes de construir, o job puxa esse cache; depois de construir, publica a versão atualizada.

```bash
docker buildx build \
  --cache-from type=registry,ref=ghcr.io/minhaorg/minhaapp:buildcache \
  --cache-to type=registry,ref=ghcr.io/minhaorg/minhaapp:buildcache,mode=max \
  -t ghcr.io/minhaorg/minhaapp:$COMMIT_SHA \
  --push .
```

`mode=max` diz ao BuildKit para exportar camadas intermediárias também, não só as da imagem final — sem isso, layers de estágios de build descartados em multi-stage não ficam disponíveis para cache futuro.

**Cache gerenciado pelo próprio provedor de CI.** Serviços como GitHub Actions oferecem um backend de cache dedicado (`type=gha`), separado do registry de imagens, com seu próprio ciclo de vida e cota de armazenamento por repositório.

```yaml
# exemplo ilustrativo — o mecanismo importa mais que o provedor específico
- uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

Este exemplo usa GitHub Actions porque é o mais documentado publicamente, mas o mecanismo — cache exportado como artefato endereçável fora do executor, reimportado no início do próximo build — existe em praticamente todo provedor de CI moderno, com nomes e limites de cota diferentes.

Entre as duas famílias, a escolha raramente é binária. Cache em registry tem a vantagem de ser portável entre provedores — se o time migrar de um serviço de CI para outro, o cache continua no mesmo lugar, porque vive no registry de imagens, não dentro do provedor de CI — e de ser inspecionável com as mesmas ferramentas usadas para imagens normais. Cache gerenciado pelo provedor costuma ser mais simples de configurar (sem precisar de credenciais de push para um registry só para o cache) e, por viver dentro da infraestrutura do próprio provedor, tende a ter latência menor entre o executor e o cache. A troca é previsível: portabilidade e uniformidade contra simplicidade e velocidade — e nada impede um pipeline de usar registry para o cache que precisa sobreviver a uma eventual troca de provedor, e o cache do provedor para o resto.

> [!warning] Cache de cada branch competindo pelo mesmo destino
> Configurar `--cache-to` apontando sempre para a mesma referência, sem segmentar por branch, faz com que o cache de uma feature branch de vida curta sobrescreva o cache da branch principal — e o próximo build de `main` herda camadas de um Dockerfile que já foi descartado junto com a branch. Segmentar a referência de cache por branch (ou usar a branch principal como cache-base e a branch da feature como cache adicional, um padrão que o BuildKit suporta com múltiplas fontes de `--cache-from`) evita essa contaminação cruzada.

### O que muda quando o cache é remoto

Cache local é gratuito em latência: ler uma layer do disco do daemon é quase instantâneo. Cache remoto troca essa gratuidade por uma dependência de rede — cada camada reaproveitada precisa ser baixada do registry ou do backend de cache antes de ser usada, e cada camada nova precisa ser enviada de volta ao final do build. Para um monorepo com imagens de poucas centenas de megabytes, isso ainda é ordens de grandeza mais rápido que reconstruir do zero, mas o gargalo deixa de ser CPU/disco e passa a ser banda e latência de rede entre o executor e o serviço de cache. Um executor de CI numa região distante do registry paga esse preço em cada camada.

Há também um custo de armazenamento que cache local nunca teve: cache exportado ocupa espaço no registry (contabilizado às vezes junto com as imagens de produção) ou numa cota separada do provedor, e cotas estouradas silenciosamente voltam o pipeline ao comportamento de cache frio — o build fica lento de novo, sem erro explícito, só devagar.

| | Cache local (daemon do desenvolvedor) | Cache exportável (registry ou backend do provedor) |
| --- | --- | --- |
| Persistência | Sobrevive enquanto a máquina não limpar o daemon | Sobrevive independente do executor, até ser expirado ou sobrescrito |
| Gargalo | CPU e disco locais | Rede — upload no fim do build, download no início |
| Custo de armazenamento | Absorvido no disco do desenvolvedor | Cota de registry ou do backend de cache do provedor |
| Concorrência | Um desenvolvedor, um daemon, sem disputa | Múltiplos builds paralelos podem sobrescrever o cache um do outro |
| Configuração necessária | Nenhuma — é o comportamento default do BuildKit | Explícita, via `--cache-from`/`--cache-to` ou equivalente |

### Confirmando que o cache exportável está de fato sendo usado

Depois de configurar `--cache-from`/`--cache-to`, o jeito confiável de saber se a configuração está surtindo efeito é ler a saída do próprio build, não assumir que "configurei, então deve estar funcionando". O BuildKit anota cada etapa do build com o tempo gasto e, quando uma etapa é satisfeita a partir do cache importado, marca isso explicitamente na saída — de forma equivalente ao `CACHED` que aparece em builds locais, mas agora alimentado por uma camada que veio de fora da máquina atual, não de uma execução anterior na mesma máquina.

```text
#8 [stage-1 3/6] RUN ./mvnw dependency:go-offline
#8 CACHED

#9 [stage-1 4/6] COPY src/ src/
#9 DONE 0.4s
```

Uma etapa marcada `CACHED` que deveria mudar (porque o `pom.xml` mudou nesse commit, por exemplo) é sinal de um problema diferente — cache reaproveitado indevidamente, geralmente porque a chave de cache não está considerando algo que deveria invalidar aquela camada. Uma etapa que deveria estar `CACHED` mas aparece com tempo de execução real, mesmo depois de duas execuções seguidas sem mudança no Dockerfile, é sinal de que o cache exportável não está sendo lido — o candidato mais comum é exatamente o erro descrito numa das armadilhas desta nota, `--cache-to` configurado sem o `--cache-from` correspondente.

### Executores hospedados contra executores próprios

Vale separar dois cenários que costumam ser confundidos sob o mesmo rótulo de "CI". Um **executor hospedado** (o modelo default de serviços como GitHub Actions ou GitLab.com) é provisionado do zero a cada job e destruído ao final — é exatamente o cenário descrito até aqui, sem cache local possível. Um **executor próprio** (self-hosted runner, mantido pelo time em uma máquina ou VM de longa duração) não tem essa característica: se o mesmo executor físico roda o job de hoje e o de ontem, o `/var/lib/docker` dele pode, de fato, acumular cache local entre execuções, exatamente como acontece na máquina de um desenvolvedor.

Isso não elimina a necessidade de cache exportável — um time normalmente tem mais de um executor próprio, e um job pode cair em qualquer um deles, então depender só do cache local de uma máquina específica é frágil — mas explica por que às vezes um pipeline com executor próprio parece não sofrer do problema descrito nesta nota: ele está, sem querer, se beneficiando de um cache que só existe porque a "máquina descartável" não foi, de fato, descartada. Tratar isso como garantia, em vez de acidente, é assumir um risco que se materializa no dia em que o time escala o número de executores ou troca de provedor.

### Um exemplo trabalhado: antes e depois do cache exportável

Considere um serviço Java com Maven, empacotado num Dockerfile multi-stage nos moldes da nota 09 — estágio de build com `eclipse-temurin:21-jdk-alpine`, estágio de runtime com a JRE. Sem cache exportável, um pipeline de CI típico para esse serviço gasta a maior parte do tempo de build baixando o repositório Maven inteiro a cada execução — `./mvnw dependency:go-offline` sozinho pode consumir a maior parte do tempo total do job, porque o `~/.m2` do executor está sempre vazio.

A correção não muda uma linha do Dockerfile. Muda o comando de build, que passa a declarar de onde ler e para onde escrever o cache:

```bash
docker buildx build \
  --cache-from type=registry,ref=ghcr.io/minhaorg/servico:buildcache \
  --cache-to type=registry,ref=ghcr.io/minhaorg/servico:buildcache,mode=max \
  --target runtime \
  -t ghcr.io/minhaorg/servico:$COMMIT_SHA \
  --push .
```

Na primeira execução após essa mudança, o comportamento é idêntico ao de antes — não existe cache remoto ainda para importar, então o build paga o custo total e, ao final, publica o cache pela primeira vez. Da segunda execução em diante, desde que o `pom.xml` não tenha mudado, o passo `dependency:go-offline` reaproveita a camada publicada no registry: o job baixa essa camada (rede, mas rápido, porque é uma camada, não centenas de artefatos Maven individuais) em vez de resolver o repositório inteiro de novo. O ganho não aparece no primeiro build depois da mudança — aparece a partir do segundo, e é aí que times costumam concluir erroneamente que "não funcionou", quando na verdade só ainda não tinha nada para importar.

Esse mesmo raciocínio explica por que builds de CI de PRs concorrentes, todos publicando cache para a mesma referência, podem se atropelar: o cache que o build B lê pode já ter sido sobrescrito pelo build A, que terminou primeiro. Não é incorreção — cache é, por definição, uma otimização best-effort — mas é uma fonte comum de "por que esse build específico não usou cache" quando dois pipelines rodam em paralelo sobre o mesmo branch de referência de cache.

### O peso do cache muda conforme o ecossistema de dependências

Nem toda linguagem sofre igualmente com a ausência de cache em CI. Ecossistemas com resolução de dependências centralizada e lockfile determinístico — Go com seu `go.sum`, por exemplo — tendem a ter downloads relativamente rápidos e paralelizáveis mesmo a frio, porque o próprio `go mod download` já é eficiente e os módulos costumam ser pequenos. Ecossistemas com árvores de dependência profundas e muitos pacotes pequenos — o `node_modules` de um projeto Node médio, com centenas ou milhares de entradas — sofrem desproporcionalmente mais com cache frio, porque o custo não é só banda, é a quantidade de requisições individuais ao registry de pacotes. Repositórios Maven ou Gradle ficam no meio: menos arquivos que npm, mas artefatos individualmente maiores.

Essa diferença explica por que a mesma política de cache exportável rende ganhos bem diferentes conforme o serviço: um monorepo poliglota que aplica cache remoto uniformemente costuma ver o maior ganho absoluto nos serviços Node, e o menor nos serviços Go — não porque a configuração esteja errada em algum deles, mas porque o problema que o cache resolve tinha pesos diferentes para começar.

> [!tip] Vídeo — `--cache-from`, que é a resposta direta ao problema desta seção
> [**docker: fast CI rebuilds with `--cache-from`**](https://www.youtube.com/watch?v=77j6JFBTmTc) (anthonywritescode, ~6 min, EN) demonstra a técnica que resolve o problema estrutural descrito acima: como o runner de CI nasce sem cache local, a saída é **buscar uma imagem já construída e apresentá-la como origem de cache**. Ele mostra o comportamento acontecendo — inclusive o caso que mais importa e que quase nenhum material menciona, o **acerto parcial**: o cache é aproveitado até a instrução em que algo mudou, e só dali para baixo o build recomeça. É a mesma cascata da nota 05, agora atravessando máquinas diferentes em vez de execuções na mesma máquina. **O que ele não cobre:** Docker-in-Docker contra socket montado, estratégia de tags em CI, o cache exportável do BuildKit (`--cache-to`, tratado na nota 10), e o custo de armazenar cache, que esta nota discute no fim.

## Docker-in-Docker contra socket montado

Para construir uma imagem, o job de CI precisa falar com algum daemon Docker. Existem, essencialmente, duas formas de dar isso a um job que roda ele mesmo dentro de um container (o caso comum quando o executor de CI já usa containers para isolar jobs):

**Montar o socket do host dentro do job** (`-v /var/run/docker.sock:/var/run/docker.sock`). O job passa a falar diretamente com o daemon que também gerencia todos os outros containers da máquina do executor — inclusive, potencialmente, containers de outros jobs, se o executor for compartilhado.

**Docker-in-Docker (DinD)** — subir um daemon Docker próprio, isolado, dentro (ou ao lado, como sidecar) do container do job, tipicamente com a imagem oficial `docker:dind`. O job fala com esse daemon dedicado, que não enxerga nem é enxergado pelo daemon do host.

A diferença não é cosmética. A nota 13 já nomeou o problema com precisão: **montar o socket do daemon dentro de um container é entregar a máquina** — quem controla o daemon controla todos os containers que ele gerencia, pode ler volumes de outros containers, escalar privilégio até root no host, e inspecionar ou adulterar qualquer coisa que passe por ali. Um job de CI com o socket montado não está "rodando isolado" — está rodando com controle administrativo sobre o executor inteiro.

Isso é especialmente grave em dois cenários que aparecem com frequência em CI real:

- **Repositório público com CI que roda em pull requests de forasteiros.** Um PR malicioso pode incluir um passo de build ou teste que, tendo acesso ao socket, escapa do sandbox do job e ataca a infraestrutura de CI — não só o repositório, mas potencialmente outros repositórios que compartilham o mesmo executor.
- **Monorepo com contribuição externa ou múltiplos times.** Mesmo sem má intenção, um job com socket montado pode acidentalmente remover ou corromper containers de outro job rodando na mesma máquina, porque do ponto de vista do daemon todos são só containers — não há isolamento por job.

Docker-in-Docker resolve isso trocando o daemon compartilhado por um daemon descartável e isolado por job — mas paga um preço em complexidade (o container DinD normalmente precisa rodar `--privileged`, o que também é uma concessão de segurança, embora mais contida que expor o daemon do host) e em tempo de inicialização (subir um daemon novo a cada job tem custo).

> [!warning] "Privileged" em DinD não é gratuito
> `docker:dind` tradicionalmente exige `--privileged` para funcionar, o que dá ao container acesso amplo a recursos do kernel do host. É mais contido que montar o socket do host diretamente, mas ainda é uma concessão de segurança real — não trate DinD como "a alternativa segura" sem qualificação.

Uma forma de organizar essa escolha é comparar as três vias pelo que cada uma expõe:

| Estratégia | O que o job controla | Custo típico |
| --- | --- | --- |
| Socket do host montado | O daemon inteiro do executor — todos os containers, de todos os jobs que ele gerencia | Nenhum custo de inicialização, mas superfície de ataque máxima |
| Docker-in-Docker | Um daemon próprio, isolado, descartado ao final do job | Exige `--privileged` (ou equivalente) e tempo de subir um daemon novo a cada execução |
| Construtor sem daemon | Nada além do próprio processo de build — não há daemon compartilhado para expor | Ecossistema e maturidade variam conforme a ferramenta, ver nota 16 |

### Construtores sem daemon como terceira via

A nota 16 mapeou alternativas ao par cliente-servidor tradicional do Docker — construtores que não dependem de um daemon persistente rodando em segundo plano. Em CI, essa característica é particularmente atraente: um construtor sem daemon elimina de saída a pergunta "como esse job fala com o daemon", porque não há daemon compartilhado para expor. O job constrói a imagem como um processo isolado, sem socket para montar e sem daemon sidecar para subir, o que reduz a superfície de ataque descrita acima a praticamente zero nesse ponto específico do pipeline.

Essa não é uma substituição universal — construtores sem daemon têm seu próprio conjunto de limitações e maturidade de ecossistema, que a nota 16 já cobriu —, mas em CI, onde o daemon compartilhado é justamente a fonte do risco, a ausência de daemon é uma vantagem estrutural, não incidental.

Muitos provedores de CI hospedados que oferecem builds de imagem como funcionalidade de primeira classe (em vez de "rode Docker você mesmo dentro do job") já adotaram essa via por padrão internamente — o job declara "quero construir esta imagem a partir deste Dockerfile" e o provedor decide como isolar essa construção, sem expor ao usuário a escolha entre socket montado e DinD. Do ponto de vista de quem escreve o pipeline, isso é a mesma vantagem de segurança discutida acima, só que terceirizada: a decisão de "como construir sem entregar a máquina" já foi tomada pelo provedor, e vale a pena verificar qual foi essa escolha antes de assumir que ela é segura por padrão.

### Segredos de build em CI: o mesmo mount, um risco diferente

CI raramente constrói imagens sem precisar de algum segredo durante o build — um token para baixar um pacote privado, uma credencial para autenticar num registry interno antes de puxar uma base image. A nota 10 já descreveu o secret mount do BuildKit como a forma de passar esse segredo sem ele acabar gravado numa camada da imagem final; em CI, o mesmo mecanismo ganha um risco adicional específico do ambiente: o segredo em si normalmente vem de um cofre do provedor (variáveis de ambiente marcadas como secret, integração com um gerenciador externo), e o passo de build precisa recebê-lo sem que ele vaze para o log do job — algo que o BuildKit não garante sozinho, porque um `RUN` mal escrito dentro do Dockerfile pode `echo` o conteúdo do secret mount por engano.

```dockerfile
# syntax=docker/dockerfile:1.7
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) npm config set //registry.npmjs.org/:_authToken=$NPM_TOKEN && \
    npm ci
```

```bash
docker build --secret id=npm_token,env=NPM_TOKEN -t myapp .
```

A disciplina de CI aqui é dupla: usar o secret mount (nunca `ARG`/`ENV` para credenciais, pelo motivo já coberto na nota 10) e garantir que o provedor de CI mascare o valor do segredo automaticamente em qualquer log gerado — a maioria dos provedores modernos faz isso para variáveis marcadas como secret, mas só para o valor literal, não para transformações dele (um segredo em base64, por exemplo, pode escapar da máscara se impresso nesse formato).

## Tags de imagem em CI

Uma decisão pequena com efeito grande: com que tag o job de CI publica a imagem que acabou de construir. A tentação óbvia é reusar uma tag móvel — `latest`, `main`, `staging` — porque simplifica o passo seguinte do pipeline ("sempre puxe `staging`"). O problema é que uma tag móvel é, por definição, mutável: `staging` aponta para o que quer que tenha sido o último push, e não há registro confiável de qual código gerou a imagem que está rodando agora, a menos que alguém tenha anotado isso à parte.

A prática recomendada é tagar cada imagem com o identificador do commit que a gerou — o SHA do Git, tipicamente:

```yaml
tags: |
  ghcr.io/${{ github.repository }}:${{ github.sha }}
```

Isso dá rastreabilidade determinística: dado um problema em produção, "qual imagem está rodando" e "qual código gerou essa imagem" são a mesma pergunta, respondida pela tag. Tags móveis continuam úteis como *ponteiros* de conveniência (`latest` apontando para o build mais recente da branch principal, por exemplo), mas nunca como a referência que um ambiente de produção usa para decidir o que rodar.

Essa disciplina se conecta diretamente com o que a nota 12 estabeleceu sobre digests: tag por commit dá rastreabilidade em nível humano (qual código), digest dá garantia em nível criptográfico (bit a bit, essa imagem não mudou). Um pipeline maduro publica com tag de commit e, no passo de deploy, referencia por digest — as duas camadas de imutabilidade compostas, não uma substituindo a outra.

Um corolário direto dessa disciplina é **construir uma vez, promover várias** — em vez de reconstruir a imagem para cada ambiente (dev, staging, produção), o pipeline constrói uma única vez, tagueia com o commit, e os ambientes seguintes referenciam essa mesma imagem por digest, sem passar de novo por `docker build`. Isso elimina uma classe inteira de bug ("funcionava em staging, quebrou em produção" causado por uma dependência de sistema que mudou de versão entre os dois builds) porque não há dois builds — há um artefato só, movido entre ambientes. A mecânica de *como* essa promoção acontece — aprovações, gates, estratégia de deploy — é disciplina de Operação, não deste galho; aqui importa só que ela depende da imagem ser referenciável de forma estável, o que uma tag de commit e um digest garantem e uma tag `latest` não.

### Build matrix multi-arquitetura

Quando o pipeline precisa publicar para mais de uma arquitetura (`linux/amd64` e `linux/arm64`, tipicamente, para suportar tanto executores tradicionais quanto instâncias baseadas em ARM), o Buildx introduzido na nota 10 constrói cada arquitetura separadamente e as agrupa sob um único manifesto multi-arquitetura na tag final. Cada arquitetura tem seu próprio conjunto de camadas e, portanto, sua própria linha de cache — um cache exportado para `amd64` não acelera o build de `arm64`, e times que esquecem disso costumam ver metade do build (a arquitetura "nova" na matriz) permanecer lenta mesmo depois de configurar `--cache-from`/`--cache-to`, porque o cache existente nunca cobriu aquela arquitetura.

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --cache-from type=registry,ref=ghcr.io/minhaorg/servico:buildcache \
  --cache-to type=registry,ref=ghcr.io/minhaorg/servico:buildcache,mode=max \
  -t ghcr.io/minhaorg/servico:$COMMIT_SHA \
  --push .
```

```mermaid
flowchart LR
    A[Código no repositório] --> B["Build com cache remoto<br/>(registry ou backend do provedor)"]
    B --> C["Imagem publicada<br/>tag = commit SHA<br/>+ digest"]
    C --> D["Teste de integração<br/>consumindo a mesma imagem<br/>(Testcontainers)"]
    D --> E["Promoção /<br/>deploy por digest"]
```

## Docker como dependência de teste

Até aqui, a nota tratou a imagem como o que se **produz** em CI. A segunda metade olha para a mesma imagem como o que se **consome** — em testes de integração e em ambientes de desenvolvimento inteiros.

### O mesmo problema de acesso, agora no passo de teste

Antes de chegar em Testcontainers propriamente, vale nomear algo que passa despercebido: rodar testes de integração baseados em Testcontainers dentro de um pipeline de CI exige exatamente a mesma decisão discutida na primeira metade desta nota — como o processo de teste, rodando dentro do container do job, fala com um daemon Docker para subir o Postgres ou o Kafka do teste. Não é um problema novo; é o mesmo problema de acesso ao daemon, revisitado no passo de teste em vez de no passo de build.

A maioria dos executores hospedados modernos já resolve isso na configuração padrão da máquina — o executor vem com um daemon Docker disponível e acessível ao job sem que o time precise montar socket nem subir DinD manualmente, porque o próprio provedor gerencia esse acesso de forma controlada, fora do container do job. Times que rodam executores próprios ou containers de job mais restritos precisam replicar deliberadamente uma das três estratégias comparadas mais acima — e a escolha carrega o mesmo trade-off de segurança, não um mais brando só porque agora é "teste" e não "build".

| Passo do pipeline | Precisa de acesso a Docker? | Nível de exposição típico |
| --- | --- | --- |
| Build da imagem | Sim — para executar `docker build` | Depende da estratégia escolhida (socket, DinD, daemonless) |
| Testes unitários | Não | Nenhum |
| Testes de integração com Testcontainers | Sim — para subir as dependências reais | Mesmo espectro de risco do build |
| Scan de vulnerabilidade (Trivy e afins) | Geralmente sim — para inspecionar a imagem construída | Normalmente leitura, sem subir containers novos |
| Deploy | Depende do alvo — normalmente não fala com o daemon local | Fora do escopo desta nota, ver fronteira com Operação |

### Testcontainers: subir a dependência real

Um teste de integração clássico para um repositório que fala com PostgreSQL tem duas opções ruins: rodar contra um banco compartilhado (que outro teste pode ter deixado sujo, ou que simplesmente não existe no executor de CI) ou simular o banco com um mock ou um banco em memória com semântica diferente (H2 fingindo ser Postgres, por exemplo, mascarando diferenças reais de SQL, tipos e comportamento transacional).

Testcontainers propõe uma terceira via: usar o Docker que já está disponível — na máquina do desenvolvedor ou no executor de CI — para subir a dependência **real** dentro do próprio processo de teste, e derrubá-la quando o teste termina. Não é um Postgres simulado; é a imagem oficial `postgres`, rodando como container efêmero, exatamente a mesma peça imutável que roda em produção.

```java
@Testcontainers
class PedidoRepositoryIT {

    @Container
    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:16-alpine");

    @Test
    void salvaEBuscaPedido() {
        // conexão real contra o container que acabou de subir
    }
}
```

O que isso resolve é o problema de fidelidade: o teste roda contra o comportamento real do banco (locks, tipos, funções específicas do SQL dialect), não contra uma aproximação. Uma migration que usa uma feature específica do Postgres 16 falha no teste exatamente como falharia em produção, em vez de passar silenciosamente contra um mock complacente.

O que isso custa é tempo de inicialização — subir um container de banco leva segundos, não milissegundos, o que multiplicado por uma suíte grande vira minutos adicionais de execução — e a exigência estrutural de que o executor de teste tenha acesso a um runtime de container. Um executor de CI que não tem Docker disponível, ou que bloqueia acesso ao daemon por política, simplesmente não consegue rodar esses testes, e é preciso decidir explicitamente como o socket (ou um daemon dedicado) chega até o processo de teste — a mesma decisão de Docker-in-Docker contra socket montado discutida acima, agora em contexto de teste em vez de build.

Testcontainers não sobe o container e assume cegamente que ele já está pronto — cada módulo define uma **estratégia de espera** (*wait strategy*) apropriada ao serviço, tipicamente escutando uma porta específica ficar aceita ou uma mensagem de log característica aparecer, antes de liberar o teste para conectar. Isso evita a classe de teste "flaky" mais comum em suítes com dependências externas: o teste que falha uma vez a cada dez porque tentou conectar no banco um segundo antes dele terminar de inicializar.

```java
@Container
static GenericContainer<?> kafka = new GenericContainer<>("confluentinc/cp-kafka:7.6.0")
    .withExposedPorts(9092)
    .waitingFor(Wait.forLogMessage(".*started \\(kafka.server.KafkaServer\\).*", 1));
```

Para suítes grandes onde subir o mesmo container (um Postgres, por exemplo) a cada classe de teste seria caro demais, Testcontainers oferece um modo de **reutilização** — o container fica de pé entre execuções de teste locais em vez de subir e derrubar a cada vez, trocando isolamento perfeito por velocidade de feedback durante desenvolvimento ativo. Esse modo é pensado para a máquina do desenvolvedor, não para CI: em CI, onde cada execução já começa de um executor limpo, a reutilização entre execuções não tem onde persistir, e o padrão continua sendo subir e derrubar por execução.

Testes de integração que envolvem mais de um serviço — a aplicação falando com um banco e, ao mesmo tempo, publicando eventos num broker de mensagens — sobem múltiplos containers Testcontainers no mesmo teste, cada um numa network Docker isolada criada para aquela execução, exatamente o mecanismo de rede em bridge custom que o galho já cobriu para orquestração multi-container em geral. A diferença é que aqui a network é efêmera e privada ao teste: nasce quando o primeiro container sobe, morre quando o último é reaperado, sem interferir com nenhuma outra suíte rodando em paralelo no mesmo executor.

### Ciclo de vida gerenciado pelo teste, e o processo que limpa órfãos

Uma característica central de Testcontainers é que o ciclo de vida do container é amarrado ao ciclo de vida do teste — o framework sobe o container antes da suíte (ou de cada teste, dependendo do escopo configurado) e derruba ao final. Mas testes travam, processos de teste são mortos abruptamente (timeout de CI, `Ctrl+C` de um desenvolvedor impaciente, OOM killer), e nesses casos o `afterAll` que derrubaria o container nunca executa.

Para evitar containers órfãos acumulando no daemon, Testcontainers sobe, junto com os containers de teste, um processo auxiliar — chamado Ryuk na implementação de referência — que monitora a sessão de teste através de uma conexão mantida aberta e remove qualquer container, rede ou volume marcado com os labels daquela sessão assim que detecta que o processo de teste desapareceu, mesmo em terminação anormal. É o mesmo problema, em miniatura, que motivou os healthchecks e as políticas de restart cobertas alhures no domínio: um sistema que sobrevive à falha do seu operador, em vez de confiar que o operador sempre vai limpar depois de si.

> [!warning] Ryuk exige privilégio para funcionar, e às vezes precisa ser desligado
> O processo de limpeza precisa falar com o mesmo daemon que gerencia os containers de teste, o que em ambientes de CI com políticas restritas de acesso a containers privilegiados pode falhar na inicialização. Ambientes assim costumam expor uma variável de ambiente para desativar esse componente — desligá-lo sem outro mecanismo de limpeza no lugar reintroduz o acúmulo de containers órfãos que ele existe para prevenir.

### Amortizando o custo de inicialização

O custo de subir um container por classe de teste — segundos multiplicados por dezenas de classes — é real, mas raramente precisa ser pago tantas vezes quanto parece. Um padrão comum é compartilhar uma única instância do container de dependência entre todas as classes de teste de uma mesma suíte, subindo-a uma vez no início da execução e derrubando-a só ao final, em vez de repetir o ciclo completo a cada classe. O ganho é aritmético: se subir um Postgres custa três segundos e a suíte tem cinquenta classes, pagar esse custo uma vez em vez de cinquenta vezes é a diferença entre alguns segundos e alguns minutos de tempo total de pipeline.

O trade-off é o mesmo de sempre que se compartilha estado entre testes: isolamento perfeito por teste (cada um com seu próprio banco limpo) dá lugar a isolamento por dado (cada teste limpa ou usa um schema/tabela próprio dentro do mesmo container compartilhado), o que exige disciplina extra na escrita dos testes para não deixar um teste contaminar o próximo através de dados residuais no mesmo container.

Testcontainers tem bindings para múltiplas linguagens, incluindo Java e o ecossistema JavaScript/TypeScript — para o aprofundamento específico de cada stack, ver [[03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes|Testcontainers — infra real em testes]] e o galho [[03-Dominios/Tecnologia/Testes JS/index|Testes JS]].

### Ambiente de desenvolvimento em container

O outro consumo comum da imagem, fora de teste e fora de produção, é o ambiente de desenvolvimento inteiro rodando em container: código-fonte montado via bind mount dentro do container (a mesma técnica descrita na nota de dados persistentes do galho, aplicada aqui a código em vez de dados), um processo de recarga automática observando mudanças no filesystem montado e reiniciando ou recompilando a aplicação, e o desenvolvedor editando arquivos no host com seu editor normal enquanto a execução acontece dentro do container.

O ganho é reprodutibilidade de ambiente — a versão de runtime, as bibliotecas de sistema, as variáveis de ambiente são as mesmas para todo mundo do time, sem depender de "instale isso na sua máquina" — e isolamento do host, que fica livre de instalar toolchains específicas de cada projeto.

Na prática, esse arranjo raramente é um único container isolado — é o `compose.yaml` de desenvolvimento que a nota 11 do galho descreveu, com o serviço da aplicação apontando para um estágio de build específico e o código montado por cima:

```yaml
services:
    app:
        build:
            context: .
            target: dev
        volumes:
            - .:/app
            - /app/node_modules
        command: npm run dev
        ports:
            - "3000:3000"
```

A segunda entrada em `volumes` merece atenção — um volume anônimo apontando para `/app/node_modules` dentro do container evita que o bind mount do código-fonte (`.:/app`) sobrescreva o `node_modules` instalado dentro da imagem com o que quer que exista (ou não exista) no host. É um detalhe pequeno que, ausente, produz o erro clássico de "funciona no container, mas só depois que eu apago node_modules do host e reconstruo" — o bind mount, por ser montado por cima, esconde o que a imagem já tinha lá dentro.

Um efeito colateral prático do bind mount é que ferramentas de debug — anexar um debugger remoto, inspecionar variáveis, colocar um breakpoint — funcionam sem fricção extra, porque o código dentro do container é literalmente o mesmo arquivo que o editor no host está mostrando; qualquer mudança salva no host aparece instantaneamente dentro do container, e o processo de reload cuida de recarregar o runtime. É essa propriedade — feedback imediato, ambiente idêntico ao de todo o time — que faz o padrão valer a complexidade extra de manter um `compose.yaml` de desenvolvimento separado do Dockerfile de produção.

A fronteira que precisa ficar honesta: esse arranjo — bind mount do código-fonte, live reload, imagem que muda a cada salvamento de arquivo — é excelente durante o desenvolvimento e **não é** uma forma de entregar software. A imagem que um desenvolvedor usa em dev, com o código montado por fora e o processo de reload observando o filesystem, não é a imagem imutável que a nota 09 descreveu como o alvo de multi-stage builds, nem a que se publica com tag de commit e se referencia por digest em produção. São dois artefatos com propósitos diferentes, mesmo quando compartilham o mesmo `Dockerfile` como ponto de partida — geralmente através de um estágio (`target`) dedicado ao dev, algo que o Compose já suporta nativamente ao selecionar qual estágio de um build multi-stage usar.

> [!warning] Configurar só `--cache-to` ou só `--cache-from`
> Os dois flags são independentes: `--cache-to` sem `--cache-from` publica o cache mas nunca o lê de volta (o build fica sempre frio na leitura, mesmo já tendo um cache disponível); `--cache-from` sem `--cache-to` lê um cache que nunca é atualizado, ficando cada vez mais desatualizado em relação ao Dockerfile atual. Os dois precisam estar presentes, apontando para a mesma referência, para o ciclo completo funcionar.

> [!warning] Imagem de dev publicada como se fosse imagem de produção
> Publicar ou promover para produção a mesma imagem usada em desenvolvimento — com bind mount configurado, ferramentas de debug instaladas, hot reload ativo — reintroduz exatamente os problemas que multi-stage e distroless existem para evitar: superfície de ataque maior, tamanho maior, comportamento que muda conforme o filesystem montado por fora. O estágio de dev e o estágio de produção precisam divergir explicitamente no Dockerfile.

## Cache como custo, não só como velocidade

Minutos de execução em CI hospedado normalmente são cobrados — por minuto de máquina, por concorrência de jobs paralelos, ou por um teto mensal que estoura e passa a ser cobrado à parte. Um build que cai de quatro minutos para quarenta segundos não é só "mais rápido para o desenvolvedor que está esperando o PR ficar verde" — é uma fatura menor no fim do mês, multiplicada pelo número de vezes que o pipeline roda por dia. Times que tratam a lentidão de CI como incômodo de produtividade, sem olhar para o custo em minutos faturados, costumam subestimar o retorno de configurar cache exportável corretamente.

A forma prática de acompanhar isso não é confiar na percepção de "parece mais rápido" — é medir. A maioria dos provedores de CI expõe, no próprio painel do job, o tempo gasto em cada etapa, e comparar esse tempo antes e depois de configurar `--cache-from`/`--cache-to` é o mesmo tipo de verificação já descrito para confirmar que o cache está sendo lido, agora aplicado ao longo de várias execuções em vez de uma só. Uma queda abrupta e sustentada no tempo médio da etapa de build, a partir do dia em que o cache exportável entrou em produção, é a confirmação de que o investimento se pagou; uma melhora só na primeira execução e volta ao patamar anterior nas seguintes é sinal de que algo na configuração — geralmente a referência do cache sendo sobrescrita por builds concorrentes, como descrito mais acima — está impedindo o efeito de se sustentar.

## Armadilhas comuns

> [!warning] Confiar em `--no-cache` para "resolver" build lento em CI
> Alguns times, frustrados com cache miss constante, adicionam `--no-cache` a todo build de CI — o que só formaliza o que já estava acontecendo e remove qualquer chance de que o cache exportável (`--cache-from`/`--cache-to`) funcione quando configurado depois. O problema não é o cache estar "sujo"; é ele não existir fora da máquina descartável.

> [!warning] Socket do host montado "só para esse job interno"
> A justificativa de que um job específico é "confiável" (roda só código do próprio time, nunca de fora) não muda o fato de que qualquer processo dentro desse job herda controle total sobre o daemon do host enquanto o socket estiver montado — incluindo qualquer dependência transitiva de build ou teste que rode código de terceiros sem que ninguém tenha auditado.

> [!warning] Tag `latest` como fonte de cache
> Usar `--cache-from image:latest` parece razoável até que `latest` seja reatribuído por outro build concorrente no meio da execução — o cache que o build está lendo pode já não corresponder ao que ele acabou de publicar segundos antes, produzindo resultados inconsistentes entre execuções aparentemente idênticas.

> [!warning] Ryuk (ou equivalente) desligado sem substituto
> Desativar o processo de limpeza de containers órfãos porque o ambiente de CI não permite containers privilegiados, sem configurar nenhuma outra rotina de limpeza (um passo de `docker system prune` agendado, por exemplo), transforma vazamento ocasional de containers em acúmulo silencioso até o disco do executor encher.

> [!warning] Ambiente de dev em container promovido direto a produção
> Copiar o `compose.yaml` de desenvolvimento — com bind mount do código e volumes de cache local — para o ambiente de produção, em vez de construir a imagem imutável do estágio correto, recria em produção a mesma fragilidade que motivou multi-stage builds: comportamento que depende do que está montado por fora, não só do que está dentro da imagem.

## Como explicar em inglês

> "The Dockerfile doesn't change between my laptop and CI, but the environment around it does — CI runners are disposable, so local layer cache simply doesn't exist there unless I explicitly export it to a registry or to the CI provider's own cache backend. That's the single biggest reason a 20-second local build takes minutes in a pipeline. For giving a CI job access to Docker, I avoid mounting the host's socket into a job container — that hands the job full control over the daemon, and therefore over every other container the runner manages, which is a real risk on public repos or with external contributions. Docker-in-Docker or a daemonless builder are the safer alternatives. I always tag CI-built images with the commit SHA, never a floating tag like `latest`, so 'what's running' and 'what code produced it' are the same question. On the testing side, Testcontainers spins up the real dependency — Postgres, Kafka, whatever the service actually talks to — inside the test process itself, instead of mocking it, and a resource-reaper sidecar cleans up orphaned containers if the test process dies mid-run. And a containerized dev environment with bind-mounted source and live reload is great for local development, but it is never the artifact you ship — that's a different, immutable image built without the bind mount."

| Português | Inglês |
| --- | --- |
| executor de CI (descartável) | CI runner (ephemeral) |
| cache exportável | exportable cache |
| socket do daemon montado | mounted daemon socket |
| Docker-in-Docker | Docker-in-Docker (DinD) |
| construtor sem daemon | daemonless builder |
| identificador do commit | commit SHA |
| tag móvel | floating tag |
| dependência real de teste | real test dependency |
| processo órfão / container órfão | orphaned container |
| processo de limpeza (Ryuk) | resource reaper |
| ambiente de dev em container | containerized dev environment |
| recarga automática | live reload / hot reload |

## A mesma imagem, três contextos

Vale fechar amarrando os três contextos cobertos nesta nota à lente que atravessa o galho inteiro desde a nota 01 — a imagem como artefato imutável e composto de camadas. Em nenhum dos três contextos a imagem deixa de ser essa coisa; o que muda é o que cada contexto exige dela.

| Contexto | O que a imagem precisa oferecer | O que quebra se a lente for ignorada |
| --- | --- | --- |
| Build em CI | Camadas cacheáveis, mesmo sem memória local do executor | Build lento sem explicação aparente, tratado como "máquina fraca" |
| Teste com Testcontainers | Ser exatamente a mesma peça que roda em produção, não uma aproximação | Teste passa contra um mock e falha contra o banco real, ou vice-versa |
| Desenvolvimento em container | Aceitar código montado por fora sem fingir que isso é a imagem final | Imagem de dev promovida a produção, reintroduzindo os riscos que multi-stage evita |

Em CI, a imutabilidade da imagem é o que permite cachear com confiança — uma camada que não mudou pode ser reaproveitada porque, por definição, produzir a mesma entrada duas vezes produz a mesma camada. Em teste, é o que dá a Testcontainers sua razão de existir — testar contra uma cópia exata do que vai para produção, não contra uma reimplementação com semântica própria. Em desenvolvimento, é a linha que separa o container de dev (que aceita ser modificado por fora, via bind mount, porque existe para servir ao desenvolvedor) do container de produção (que nunca deveria).

### Vocabulário adicional

- pipeline de CI → CI pipeline
- job / execução → job / run
- fatura de minutos de build → build minutes billing
- cache hit / cache miss → cache hit / cache miss
- imagem promovida entre ambientes → promoted image across environments
- segredo de build → build secret

## O que vem a seguir

Esta nota fechou o ciclo de vida da imagem visto de fora: como ela é construída sob a pressão de um ambiente descartável, como é publicada com uma tag que conta a verdade sobre sua origem, e como é consumida — em teste, via Testcontainers, e em desenvolvimento, via bind mount e live reload — sem nunca confundir esses dois últimos com a forma de entregar software. A nota 18, capstone do galho, junta todas as dezessete anteriores num único exercício: empacotar uma aplicação do zero até uma imagem que se defenderia numa revisão de produção — multi-stage, non-root, digest, cache exportável, tudo o que até aqui foi tratado peça por peça, agora como um artefato só.

> [!note] Fronteira com Operação
> O pipeline como disciplina de entrega — estratégias de deploy (blue-green, canary, rolling), promoção de imagem entre ambientes, GitOps — pertence a [[03-Dominios/Engenharia/Operação/2 - Entrega e release/01 - Pipeline de CI-CD como decisão de design|Pipeline de CI-CD como decisão de design]]. Esta nota tratou do mecanismo do Docker dentro desse pipeline — como a imagem é construída, cacheada e tagueada —, não da disciplina de quando e como promovê-la entre ambientes.

## Fontes

- [Docker Build Cache — Docker Docs](https://docs.docker.com/build/cache/)
- [Cache storage backends — Docker Docs](https://docs.docker.com/build/cache/backends/)
- [Docker Build in GitHub Actions — Docker Docs](https://docs.docker.com/build/ci/github-actions/)
- [docker/build-push-action — GitHub](https://github.com/docker/build-push-action)
- [Docker-in-Docker — Jérôme Petazzoni, "Using Docker-in-Docker for your CI or testing environment"](https://www.docker.com/blog/docker-can-now-run-within-docker/)
- [Testcontainers — Documentação oficial](https://testcontainers.com/getting-started/)
- [Testcontainers for Java — Documentação](https://java.testcontainers.org/)
- [Custom configuration and Ryuk — Testcontainers for Java](https://java.testcontainers.org/features/configuration/)
- [Ryuk the Resource Reaper — Worldline Tech Blog](https://blog.worldline.tech/2023/01/04/ryuk.html)
- [Dev Containers specification](https://containers.dev/)
- [BuildKit — GitHub](https://github.com/moby/buildkit)

## Veja também

- [[03-Dominios/Tecnologia/Infraestrutura/Docker/05 - Build e cache — por que seu build está lento|05 — Build e cache]]
- [[03-Dominios/Tecnologia/Infraestrutura/Docker/10 - BuildKit por dentro|10 — BuildKit por dentro]]
- [[03-Dominios/Tecnologia/Infraestrutura/Docker/12 - Registry|12 — Registry]]
- [[03-Dominios/Tecnologia/Infraestrutura/Docker/13 - Segurança da imagem e do runtime|13 — Segurança da imagem e do runtime]]
- [[03-Dominios/Tecnologia/Infraestrutura/Docker/16 - O ecossistema além do Docker|16 — O ecossistema além do Docker]]
- [[03-Dominios/Tecnologia/Infraestrutura/Docker/index|Docker]]
