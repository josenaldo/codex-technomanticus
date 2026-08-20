---
title: "Monorepo vs multi-repo"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - microservices
  - iniciado
  - arquitetura
aliases:
  - "Monorepo vs multi-repo"
  - "Topologia de repositórios"
---

# Monorepo vs multi-repo

> [!abstract] TL;DR
> **Monorepo vs multi-repo** é uma decisão sobre **topologia de repositórios** — como você distribui os serviços deployáveis entre repositórios Git. No **multi-repo**, cada serviço mora no seu próprio repo, com release e ownership independentes. No **monorepo**, vários serviços convivem num único repo, ganhando refatoração atômica e consistência ao custo de tooling pesado de CI. Cuidado para não confundir isso com **multi-módulo de build** (um único projeto Maven/Gradle com vários módulos), que é eixo do [[03-Dominios/Tecnologia/Java/Build e tooling/12 - Projetos multi-módulo|Galho 15]] — lá é a estrutura de **um build**; aqui é a organização de **repositórios deployáveis**.

## O que é

Quando você tem dez microservices, surge uma pergunta de logística que parece trivial e não é: **onde eles ficam guardados?** Em quantos repositórios Git você espalha esse código? Essa escolha de **topologia de repositórios** tem dois extremos.

- **Multi-repo** (também chamado *polyrepo*): um serviço, um repositório. O `order-service` tem o seu repo, o `payment-service` tem outro, e cada um vive sua vida — seu histórico, seu CI, seu ciclo de release.
- **Monorepo**: um único repositório guarda **vários** serviços (às vezes todos os da organização). Todo o código deployável compartilha um histórico Git e uma árvore de diretórios.

Repare que o eixo aqui é **quantos repositórios** e **o que cada um contém em termos de serviços que sobem para produção**. Não é sobre como o build interno de cada serviço é organizado — um único serviço pode perfeitamente ser um projeto multi-módulo Maven, e isso é ortogonal à topologia de repos.

> [!info] A confusão que vale evitar de cara
> "Multi-módulo" (Galho 15) e "multi-repo" (esta nota) soam parecidos e tratam de coisas diferentes. Multi-módulo é **estrutura de um build**: um projeto, vários módulos compilados juntos. Multi-repo é **estrutura de deploy/ownership**: vários serviços que sobem para produção de forma independente, cada um no seu repositório. Você pode ter um monorepo cheio de projetos single-module, ou um multi-repo onde cada repo é multi-módulo. São eixos perpendiculares.

## Por que importa

A topologia de repositórios não é um detalhe de organização de pastas — ela molda o **dia a dia** de quem desenvolve e opera os serviços.

- **Ela decide o que é fácil e o que é caro.** Em multi-repo, isolar um time num serviço é trivial, mas uma mudança que atravessa três serviços vira uma coreografia de PRs. Em monorepo, a mudança cross-serviço cabe num único commit, mas manter o CI rápido com milhares de arquivos exige ferramenta dedicada.
- **Ela define a fronteira de ownership.** "De quem é esse código?" tem resposta óbvia quando o repo é do time. Num monorepo, ownership precisa ser declarado por convenção (por exemplo, arquivos de *code owners* por diretório), não pela borda do repositório.
- **Ela afeta a descoberta de código.** Num monorepo, achar quem usa uma função compartilhada é uma busca de texto. Em multi-repo, esse mesmo grep não atravessa as fronteiras — você descobre dependências por documentação e por contratos publicados.
- **Ela muda o modelo de versionamento.** Multi-repo praticamente força versionamento explícito de bibliotecas compartilhadas (publica-se um pacote, consumidores fazem *bump*). Monorepo permite consumir o código compartilhado direto da árvore, sem pacote versionado, porque todo mundo está no mesmo commit.

Essa escolha tende a ser difícil de reverter depois que a organização cresce, então entender os trade-offs cedo importa.

## Como funciona

### Multi-repo (um serviço, um repo)

Cada serviço deployável é um repositório Git autossuficiente. O `order-service` tem o seu `main`, seu pipeline de CI, suas tags de release. O time dono daquele repo tem **autonomia**: escolhe libs, define a cadência de release, decide as regras de contribuição.

Segundo a [monorepo.tools](https://monorepo.tools/), essa autonomia é o principal benefício do modelo *polyrepo* — times fazem "escolhas independentes sobre bibliotecas, cadência de release e regras de contribuição".

O preço aparece no **código compartilhado**. Ainda pela monorepo.tools, compartilhar código entre repos exige "montar um repositório dedicado, CI, publicação de pacote e gestão de versão". E uma correção de bug numa biblioteca compartilhada vira uma sequência de merges em históricos desconectados — a página descreve isso como "ginástica de compatibilidade: releases beta, upgrades dos consumidores, releases estáveis, repete".

O outro custo é a **inconsistência**: cada repo "faz suas próprias escolhas sobre tooling, dependências, estrutura de código e documentação" (monorepo.tools). Sem disciplina ativa, dez repos viram dez dialetos.

### Monorepo (vários serviços, um repo)

Um único repositório abriga vários serviços. O ganho central é a **mudança atômica**: pela monorepo.tools, "uma breaking change numa biblioteca compartilhada e a correção em cada consumidor caem no mesmo PR". Conserta-se o bug uma vez e "todo consumidor recebe a correção — sem cópias para rastrear".

Como todos os consumidores estão no mesmo repo, "nenhum pacote versionado é necessário" para compartilhar código (monorepo.tools) — você importa direto da árvore. E a **consistência** vem de graça em parte: "regras organizacionais vivem num lugar só e se aplicam em todo lugar".

O custo escondido é o **tooling de build/CI**. Um monorepo grande sem ferramenta adequada faz o CI rodar tudo a cada commit, o que não escala. A monorepo.tools lista o que as ferramentas de monorepo de ponta entregam para resolver isso: cache local e remoto, execução distribuída de tarefas, **detecção de "affected"** (rodar só o que a mudança afeta), divisão de tarefas e *deflaking*. Sem isso, o monorepo vira gargalo.

> [!warning] Monorepo ≠ build acoplado
> Um monorepo **não** significa que tudo é compilado e deployado junto. Serviços num monorepo bem montado continuam tendo deploy independente — a topologia de repositório é uma coisa, a fronteira de deploy é outra. O que o monorepo dá é a *possibilidade* de mudança atômica e visibilidade total do código; cabe ao tooling preservar a independência de deploy.

### O eixo de decisão

Em uma frase: **multi-repo otimiza isolamento; monorepo otimiza mudança atômica e consistência.** A pergunta-chave é com qual dor você prefere conviver.

| Dimensão | Multi-repo | Monorepo |
|---|---|---|
| Isolamento / autonomia | Alto (borda do repo = borda do time) | Precisa ser imposto por convenção |
| Mudança cross-serviço | Cara (PRs sequenciados, *bumps*) | Atômica (um PR) |
| Descoberta de código | Limitada à fronteira do repo | Busca de texto em tudo |
| Versionamento de compartilhado | Explícito (publica pacote) | Implícito (consome da árvore) |
| Consistência de tooling | Por repo, tende a divergir | Centralizada |
| Custo de CI | Naturalmente particionado | Exige tooling de *affected*/cache |

Note que isolamento e mudança atômica são quase **opostos**: tornar a mudança cross-serviço barata (monorepo) significa derrubar as fronteiras que dão o isolamento (multi-repo). Não existe almoço grátis aqui — só trade-off honesto.

## Na prática

Um exemplo neutro das duas topologias para dois serviços, `order-service` e `payment-service`, mais uma biblioteca compartilhada `commons-money`.

**Multi-repo** — três repositórios independentes:

```text
order-service/            # repositório Git próprio
├── src/
├── pom.xml
└── .ci/pipeline.yml      # CI dedicado deste serviço

payment-service/          # outro repositório Git
├── src/
├── pom.xml
└── .ci/pipeline.yml

commons-money/            # biblioteca compartilhada, repo próprio
├── src/
├── pom.xml
└── .ci/pipeline.yml      # publica pacote versionado (ex.: 1.4.0)
                          # order/payment consomem via dependência versionada
```

**Monorepo** — um repositório, três projetos na árvore:

```text
platform/                 # um único repositório Git
├── services/
│   ├── order-service/
│   │   ├── src/
│   │   └── pom.xml
│   └── payment-service/
│       ├── src/
│       └── pom.xml
├── libs/
│   └── commons-money/    # consumido direto da árvore, sem pacote publicado
│       ├── src/
│       └── pom.xml
├── CODEOWNERS            # ownership declarado por diretório
└── .ci/pipeline.yml      # CI com detecção de "affected" para não rodar tudo
```

No multi-repo, uma mudança em `commons-money` exige novo release do pacote e *bump* em cada serviço. No monorepo, a mesma mudança e a adaptação de `order` e `payment` cabem num único PR — ao custo de um pipeline que precisa saber rodar só o que foi afetado.

## Armadilhas

### (1) Confundir multi-módulo (build) com multi-repo (deploy)

**Sintoma:** alguém diz "nosso projeto Maven tem cinco módulos, então temos um monorepo" — ou o contrário, "vamos quebrar em multi-repo" quando o que se quer de fato é só separar módulos de build.

**Por que erra:** são eixos diferentes. Multi-módulo é a estrutura interna de **um build** (um projeto, vários `pom.xml` filhos compilados juntos), tema do [[03-Dominios/Tecnologia/Java/Build e tooling/12 - Projetos multi-módulo|Galho 15]]. Multi-repo é a organização de **repositórios de serviços deployáveis**, com release e ownership independentes. Um único repo pode conter um projeto multi-módulo; um monorepo pode conter dezenas de projetos single-module.

**Fix:** antes de decidir, pergunte "isso é sobre como **um build** se organiza, ou sobre quantos **repositórios** os serviços deployáveis ocupam?". A primeira pergunta é Galho 15; a segunda é esta nota. Se a conversa for sobre `pom.xml` pai/filho, é build. Se for sobre quem faz deploy de quê e quando, é topologia de repo.

### (2) Adotar monorepo sem tooling e transformar o CI em gargalo

**Sintoma:** o monorepo cresce, e cada PR dispara o build e os testes de **todos** os serviços. O pipeline que levava 4 minutos passa a levar 40, e a fila de merge vira o gargalo do time.

**Por que erra:** monorepo só escala com ferramenta que entende o **grafo de dependências** e roda apenas o que foi afetado. A própria [monorepo.tools](https://monorepo.tools/) lista isso como capacidade essencial das ferramentas de ponta: cache local/remoto, execução distribuída de tarefas e **detecção de "affected"**. Sem isso, você paga o custo de monorepo (CI lento, gargalo) sem colher o benefício.

**Fix:** ou você entra no monorepo já com tooling de *affected*/cache configurado, ou não entra. Trate a ferramenta de build do monorepo como parte da decisão, não como algo a resolver depois. Se a organização não tem apetite para esse investimento de tooling, multi-repo particiona o CI de graça — cada repo só roda o seu.

## Em entrevista

### Frase pronta (inglês)

> Monorepo versus multi-repo is a decision about **repository topology**, not about how a single build is structured. In a **multi-repo** setup each deployable service lives in its own repository, which gives strong isolation and independent release and ownership — but cross-service changes become a choreography of sequenced pull requests and version bumps. A **monorepo** keeps many services in one repository, so a breaking change and its fixes across consumers can land in a single atomic change, and tooling and conventions stay consistent — but it only scales with build tooling that runs just the affected projects, otherwise CI becomes the bottleneck. I always separate this from multi-module builds, which are about structuring one project, not about how many repositories hold the deployable services.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| monorepo (um repositório guardando vários serviços deployáveis) | monorepo |
| multi-repo / polyrepo (um serviço por repositório) | multi-repo / polyrepo |
| repositório (unidade de versionamento Git; o eixo desta decisão) | repository |
| deploy independente (cada serviço sobe no seu próprio ritmo) | independent deployment |
| propriedade (quem é dono e responde pelo código) | ownership |
| mudança atômica (altera vários serviços num único commit/PR) | atomic change |
| detecção de afetados (rodar no CI só o que a mudança impacta) | affected detection |
| fronteira de repositório (borda do que um time vê e versiona) | repository boundary |

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/01 - O que são microservices e a tese honesta|O que são microservices]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/05 - Comunicação inter-serviços — síncrono vs assíncrono|Comunicação inter-serviços]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/12 - Projetos multi-módulo|Projetos multi-módulo (Galho 15)]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- [monorepo.tools — Monorepo Explained](https://monorepo.tools/) — trade-offs de monorepo vs polyrepo, capacidades de tooling (cache, execução distribuída, detecção de *affected*), mudança atômica, código compartilhado e consistência. Fonte das citações desta nota.
- Martin Fowler sobre monorepo/many-repos — **não confirmado**: as URLs tentadas (`martinfowler.com/bliki/MonorepoAntiPattern.html` e `martinfowler.com/articles/monorepos.html`) retornaram HTTP 404 na pesquisa, então nenhuma afirmação foi atribuída a essa fonte.
