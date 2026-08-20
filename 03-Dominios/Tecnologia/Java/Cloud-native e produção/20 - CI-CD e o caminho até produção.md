---
title: "CI/CD e o caminho até produção"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: Magus
tags:
  - java
  - cloud-native
  - magus
  - ci-cd
  - deploy
aliases:
  - "CI/CD"
  - "Pipeline de deploy"
  - "GitOps"
---

# CI/CD e o caminho até produção

> [!abstract] TL;DR
> **CI/CD** é a esteira que leva o jar testado até o cluster, com portões de qualidade no caminho. O **pipeline** percorre quatro estágios — **build → test → imagem → deploy** — e cada estágio só passa adiante o que o anterior aprovou. No CI, o **quality gate** (cobertura, lint, vulnerabilidades — fronteira do Galho 15) barra código ruim antes de gerar artefato. No deploy, a **supply chain** exige que a imagem seja **assinada** e acompanhada de um **SBOM** (inventário do que tem dentro — também Galho 15). O passo de imagem reusa **Buildpacks ou Jib** das notas 06/07. E o estado do cluster pode ser dirigido por **GitOps**: o repositório declara o que deveria estar rodando e um agente reconcilia a realidade com essa declaração. A regra de ouro: você promove para produção **exatamente o mesmo artefato** que foi testado — nunca um rebuild.

## O que é

**CI (continuous integration / integração contínua)** é a prática de integrar mudanças de código com frequência, validando cada uma com build e testes automatizados. **CD** tem dois sentidos que convivem: **continuous delivery (entrega contínua)** — todo commit que passa fica *pronto* para ir a produção com um clique — e **continuous deployment (implantação contínua)** — esse clique também é automático, e o que passa *vai* a produção sem intervenção humana.

Na prática, isso se materializa num **pipeline**: uma sequência de estágios automatizados disparada por um evento (geralmente um push ou um pull request). Pense numa esteira de fábrica. O código entra numa ponta como fonte; sai na outra como um contêiner rodando no cluster. Entre as pontas há estações de inspeção — os **quality gates** — que param a esteira se algo não está conforme.

Os quatro estágios canônicos:

| Estágio | O que faz | Saída |
| --- | --- | --- |
| **build** | compila e empacota o jar | artefato (jar) |
| **test** | unit, integração, quality gate | verde/vermelho |
| **imagem** | embrulha o jar numa imagem OCI | imagem assinada + SBOM |
| **deploy** | publica a imagem no cluster | app rodando |

> [!info] Fronteira com o Galho 15
> O *conteúdo* de cada gate (quais regras, que cobertura, como assinar, o que é um SBOM) é assunto de [[03-Dominios/Tecnologia/Java/Build e tooling/16 - Quality gates no build|Quality gates no build]] e [[03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM|Supply chain e SBOM]]. Aqui a gente olha o *fluxo* — onde cada peça encaixa na esteira até produção.

## Por que importa

Sem pipeline, "ir a produção" é um ritual manual: alguém builda na própria máquina, copia um jar, sobe num servidor, reza. Três problemas nascem daí, e o CI/CD ataca cada um.

**Reprodutibilidade.** Build na máquina do dev carrega o ambiente do dev — versão de JDK, variável de ambiente esquecida, dependência em cache local. O CI builda num ambiente limpo e versionado, então o resultado é o mesmo independente de quem disparou.

**Feedback rápido.** Quanto mais cedo um defeito é pego, mais barato é consertá-lo. O gate no CI reprova um PR em minutos, antes de o código sequer virar artefato — em vez de o bug aparecer em produção, onde custa um incidente.

**Rastreabilidade e confiança.** Numa esteira automatizada, todo deploy tem proveniência: este commit, este pipeline, esta imagem, este SBOM, esta assinatura. Quando algo quebra às três da manhã, você sabe exatamente o que subiu e consegue reverter para o artefato anterior — que ainda existe, intacto, porque foi *promovido* e não *rebuiltado*.

## Como funciona

### O pipeline: build → test → imagem → deploy

O pipeline é dirigido por eventos. Um push abre um PR; o PR dispara os estágios; cada estágio é uma barreira: só passa adiante quem o anterior aprovou.

- **build** — o CI clona o repo num runner limpo, resolve dependências (via Maven/Gradle) e compila. Saída: o jar.
- **test** — roda testes unitários e de integração. Aqui mora o **quality gate**: cobertura mínima, ausência de *code smells* críticos, dependências sem vulnerabilidades conhecidas. Reprovou um critério, o pipeline para — e o PR não funde. *(O que cada gate verifica é o Galho 15; aqui ele é só a estação de inspeção da esteira.)*
- **imagem** — com o jar aprovado, o CI gera uma imagem OCI. Esse passo **reusa Buildpacks ou Jib** — não há Dockerfile novo a manter. Veja [[03-Dominios/Tecnologia/Java/Cloud-native e produção/06 - Buildpacks — imagem sem Dockerfile|Buildpacks]] e [[03-Dominios/Tecnologia/Java/Cloud-native e produção/07 - Jib — imagem daemonless|Jib]]. A imagem é empurrada para um registry.
- **deploy** — a imagem do registry é aplicada ao cluster, com uma estratégia de rollout (próxima H3).

A regra que costura tudo: o artefato que sai do `build` é o **mesmo** que percorre `test`, `imagem` e `deploy`. Você **promove** esse artefato entre ambientes (dev → staging → prod), nunca recompila por ambiente. Recompilar quebra a garantia — você passaria a produção um binário que ninguém testou.

### Supply chain no deploy: SBOM e assinatura

O estágio de imagem não termina ao empurrar bytes para o registry. Numa esteira madura, ele anexa duas coisas à imagem:

- um **SBOM (software bill of materials / cadeia de suprimentos)** — o inventário de tudo que está dentro da imagem: bibliotecas, versões, licenças. Quando a próxima CVE de uma lib transitiva aparecer, o SBOM responde "estou afetado?" sem arqueologia.
- uma **assinatura** — uma prova criptográfica de que *este* pipeline gerou *esta* imagem. No deploy, o cluster pode recusar imagem não assinada, fechando a porta para artefato adulterado ou de origem desconhecida.

> [!warning] Não re-explico aqui
> *Como* gerar o SBOM, *como* assinar, qual ferramenta — tudo isso é [[03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM|Supply chain e SBOM (Galho 15)]]. O ponto desta nota é *onde* na esteira essas peças entram: o SBOM e a assinatura nascem no estágio de **imagem** e são *verificados* no estágio de **deploy**. A supply chain não é um adendo opcional no fim — é a alça que conecta o que foi testado ao que entra no cluster.

### GitOps e estratégias de deploy

**GitOps** é um modelo de deploy onde o **repositório Git é a fonte da verdade do estado desejado** do cluster. Em vez de o pipeline empurrar comandos para o cluster (modelo *push*), você commita a configuração do estado desejado — "quero a imagem `order-service:1.4.2` rodando, com três réplicas" — e um **agente** dentro do cluster observa esse repo e **reconcilia** continuamente: se a realidade diverge do declarado, ele corrige.

A ideia central é o **loop de reconciliação**: declaro o destino, o agente cuida de chegar lá e de manter. Deploy vira um `git commit`; rollback vira um `git revert`. *(Conceitual de propósito — qual ferramenta implementa o agente é detalhe de operação, fora do escopo desta nota.)*

Independente de push ou GitOps, *como* a nova versão substitui a antiga é a **estratégia de deploy** — e isso já foi visto em [[03-Dominios/Tecnologia/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|Graceful shutdown e deploy sem downtime]]:

- **rolling** — troca as réplicas aos poucos; simples, mas convive com duas versões durante a transição.
- **blue-green** — sobe o ambiente novo inteiro ao lado do velho e vira o tráfego de uma vez; rollback é virar de volta.
- **canary** — manda uma fração do tráfego para a versão nova, observa as métricas, e só então amplia.

O recap importa porque o pipeline *escolhe* a estratégia, mas é o **graceful shutdown** (nota 12) que garante que nenhuma requisição em voo seja cortada quando uma réplica antiga sai.

## Na prática

Um pipeline conceitual para um `order-service`, em pseudo-YAML (estrutura ilustrativa, não a sintaxe exata de nenhuma ferramenta):

```yaml
# pipeline conceitual — order-service
pipeline:
  trigger: push        # ou pull_request

  stages:
    - build:
        run: ./mvnw -B package -DskipTests
        outputs: [target/order-service.jar]

    - test:
        run: ./mvnw -B verify          # unit + integração
        quality-gate:                  # fronteira Galho 15
          coverage-min: 80%
          vulnerabilities: none-critical
        on-fail: stop                  # PR não funde

    - image:
        # reusa Buildpacks (nota 06) — sem Dockerfile novo
        run: ./mvnw spring-boot:build-image
        produce:
          - sbom                       # inventário (Galho 15)
          - signature                  # assinatura (Galho 15)
        push-to: registry/order-service:${commit}

    - deploy:
        verify:
          - signature-valid            # cluster recusa imagem não assinada
        promote: registry/order-service:${commit}   # MESMO artefato do test
        strategy: rolling              # ou blue-green / canary (nota 12)
```

O fluxo, do commit ao cluster:

```text
push (commit abc123)
   │
   ▼
[ build ] ── jar ──────────────────────────►  (artefato único)
   │                                                 │
   ▼                                                 │
[ test ] ── quality gate ──► reprovou? ── PARA       │  promove
   │ passou                                          │  o MESMO
   ▼                                                 ▼  artefato
[ image ] ── imagem OCI + SBOM + assinatura ──►  registry
   │
   ▼
[ deploy ] ── verifica assinatura ──► aplica no cluster
                                          │
                                          ▼
                                 estratégia: rolling / blue-green / canary
                                 (graceful shutdown drena requisições — nota 12)
```

Repare no detalhe que costura tudo: o `${commit}` que nomeia a imagem é o mesmo do `build`. Não há recompilação entre `test` e `deploy` — a imagem promovida é bit-a-bit a que passou no gate.

## Armadilhas

### (1) Buildar a imagem fora do CI

Gerar a imagem na máquina de alguém — ou num passo manual fora da esteira — destrói a reprodutibilidade. O ambiente local carrega estado que o runner limpo não tem: outra versão de JDK, cache de dependência diferente, uma variável de ambiente. O resultado é uma imagem que "funciona na minha máquina" e ninguém consegue reproduzir. A imagem precisa nascer *dentro* do pipeline, num ambiente versionado e descartável.

### (2) Deploy sem SBOM nem assinatura

Subir uma imagem sem inventário e sem prova de origem é navegar às cegas. Sem **SBOM**, a próxima CVE de uma dependência transitiva vira uma caçada manual por todos os serviços. Sem **assinatura**, o cluster não tem como distinguir a imagem do seu pipeline de uma imagem adulterada com o mesmo nome. Os dois nascem no estágio de imagem e são verificados no deploy — não são luxo, são a alça da supply chain. *(Mecânica em [[03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM|Supply chain e SBOM]].)*

### (3) Promover um artefato diferente do que foi testado

A armadilha mais sutil e mais perigosa: recompilar o código por ambiente, em vez de promover o artefato único. Se `staging` builda um jar e `prod` builda outro a partir do mesmo commit, eles *deveriam* ser idênticos — mas qualquer diferença de timestamp, de versão de plugin, de cache, quebra a igualdade. Você acaba mandando para produção um binário que **nenhum teste viu**. A garantia do pipeline só vale se o que se promove é, byte a byte, o que passou no gate. Builde uma vez, promova o mesmo artefato adiante.

## Em entrevista

### Frase pronta (inglês)

> A CI/CD pipeline is the conveyor belt that carries a tested jar all the way to the cluster, with quality gates along the way. The stages are build, test, image, and deploy — and the golden rule is that I promote the exact same artifact that passed the tests, never a rebuild, because rebuilding per environment quietly ships a binary nobody tested. The image stage reuses Buildpacks or Jib, so there's no Dockerfile to maintain, and it produces a signed image with an SBOM attached, so the deploy stage can refuse unsigned images and answer "am I affected?" the next time a transitive CVE lands. On top of that I lean toward GitOps, where a Git repo declares the desired state and an in-cluster agent continuously reconciles reality against it — deploy becomes a commit and rollback becomes a revert. The rollout strategy itself — rolling, blue-green, or canary — is what keeps healthy instances serving traffic throughout, and graceful shutdown is what guarantees no in-flight request gets cut when an old replica drains.

### Vocabulário

| Português | Inglês |
| --- | --- |
| integração contínua | continuous integration |
| entrega contínua | continuous delivery |
| esteira | pipeline |
| portão de qualidade | quality gate |
| cadeia de suprimentos | supply chain |
| promoção de artefato | artifact promotion |
| estado desejado | desired state |
| loop de reconciliação | reconciliation loop |
| inventário de software | software bill of materials (SBOM) |
| reverter | roll back |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/12 - Graceful shutdown e deploy sem downtime|Graceful shutdown e deploy sem downtime]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/22 - Capstone — do jar ao cluster|Capstone — do jar ao cluster]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM|Supply chain e SBOM (Galho 15)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- [Spring Boot Reference — Container Images](https://docs.spring.io/spring-boot/reference/packaging/container-images/index.html) — Buildpacks (`spring-boot:build-image` / `bootBuildImage`) e Jib como formas de produzir a imagem OCI no estágio de imagem do pipeline.
- [Spring Boot Reference — Packaging](https://docs.spring.io/spring-boot/reference/) — framing de developing → packaging → testing → deploying.
- Quality gates e SBOM/assinatura: ver Galho 15 — [[03-Dominios/Tecnologia/Java/Build e tooling/16 - Quality gates no build|Quality gates no build]] e [[03-Dominios/Tecnologia/Java/Build e tooling/18 - Supply chain e SBOM|Supply chain e SBOM]].
