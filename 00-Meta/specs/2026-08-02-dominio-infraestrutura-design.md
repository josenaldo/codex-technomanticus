---
title: "Design — Domínio Infraestrutura (Docker, Kubernetes, Nginx, Linux)"
created: 2026-08-02
updated: 2026-08-02
type: spec
publish: false
tags:
  - meta
  - spec
  - design
  - infraestrutura
---

# Design — Domínio Infraestrutura

Spec de design do domínio `03-Dominios/Tecnologia/Infraestrutura`, aberto como **Tier 2** do [[00-Meta/Roadmap|Roadmap central]] em 2026-08-02. É o último bloco de construção nova com escopo já fechado: o escopo da estante foi decidido em 2026-07-31, na mesma sessão que tirou Git daqui e o promoveu a domínio próprio.

## O achado que define o domínio

O levantamento de fronteira foi feito **antes** do roster — o método que funcionou em Padrões de Projeto e que evitou notas redundantes lá. O achado é que **o resto do vault já opera essas ferramentas sem nunca as ensinar**, e diz isso explicitamente:

- `Engenharia/Operação/3 - Rodar em produção/01 - Containers em produção` abre com *"Este documento assume que você já sabe escrever um Dockerfile e rodar `docker build` — ver [[Docker]] pra isso"*, apontando para o monólito.
- `Engenharia/Operação/3 - Rodar em produção/02 - O contrato de produção do Kubernetes` diz *"Esta nota assume que você já sabe o que é um Pod, um Deployment, um Service"*.
- `Engenharia/Operação/3 - Rodar em produção/05 - Rede e borda em produção` usa Nginx como Ingress sem ensinar uma linha de configuração de Nginx.
- `Ciência/Sistemas Operacionais/13 - Virtualização e containers` já cobre namespaces, cgroups, OCI e runc — o mecanismo no kernel.

Ou seja: existe o mecanismo (Ciência), existe o ofício (Engenharia), existe a plataforma gerenciada (Cloud) — e **falta a ferramenta no meio**, que os três pressupõem.

## Lente do domínio

**A ferramenta por dentro, para quem já vai operá-la.**

Não é "como usar Docker" — tutorial de comando envelhece e o vault não é manual. É *o que a ferramenta realmente faz quando você dá esse comando*, que é exatamente o que Operação pressupõe e nunca explica, e o que separa quem repete receita de quem debuga às três da manhã.

### O sanduíche de quatro camadas

| Camada | Casa | Pergunta que responde |
|---|---|---|
| Mecanismo | `Ciência/Sistemas Operacionais/13` | como o isolamento funciona no kernel |
| **A ferramenta** | **`Tecnologia/Infraestrutura`** | **como a ferramenta funciona por dentro** |
| O ofício | `Engenharia/Operação/3` | o que muda quando é produção |
| A plataforma | `Tecnologia/Cloud/12` | quando alguém gerencia por você |

Essa tabela é o contrato de fronteira do domínio e deve ser reproduzida no `index.md`.

## Decisões estruturais

**Quatro galhos, construídos em sequência.** Docker → Kubernetes → Nginx → Linux. Cada galho fecha sozinho antes do próximo abrir, com pergunta ao usuário a cada bloco — o modelo de Padrões de Projeto. A ordem coloca o pré-requisito conceitual antes (Docker antes de Kubernetes) e a base absoluta por último: Linux é o galho que mais se sobrepõe a Terminal e a Ciência/SO, então se beneficia de ser escrito depois que os outros três cravaram suas fronteiras.

**Três fases em todos os quatro** (Iniciado/Adepto/Magus), escala Cloud/Go — notas de 440-540 linhas, `fase:` no frontmatter, padrão capítulo de livro. **Não** é o modelo de Controle de Versão (níveis, notas curtas, público geral): aqui Operação já ocupou a camada rasa, e nota curta nessa faixa vira resumo pior do que o original.

**Numeração por galho**, `01..N` dentro de cada pasta — modelo Java/Cloud, não a numeração contínua de Controle de Versão. Os galhos são ferramentas independentes; não há ordem de leitura única atravessando os quatro.

**Uma lente por galho**, cravada antes do roster:

| Galho | Lente | O fio condutor |
|---|---|---|
| Docker | **A imagem como artefato** | tudo é consequência de uma decisão de design: a imagem é imutável e em camadas |
| Kubernetes | **O loop de reconciliação** | K8s não executa comandos, converge estado — `kubectl apply` escreve no etcd e vai embora |
| Nginx | **O ciclo de vida de uma request** | a ordem de avaliação não é a ordem do arquivo; seguir a request explica 90% dos bugs |
| Linux | **O sistema como o processo o vê** | processos, descritores, permissões e systemd — a base para debug de produção e legado |

## Contrato de fronteira

A fronteira com Operação é renegociada **nota a nota, não em bloco**. Onde Operação já disse melhor, o galho linka em vez de repetir; onde Operação pressupõe, o galho preenche e Operação ganha um callout de volta apontando para cá — o mesmo movimento feito em Arqueologia quando Controle de Versão fechou.

| Fronteira | Fica lá | Fica aqui |
|---|---|---|
| `Ciência/SO 13` | namespaces, cgroups, runc, OCI, escape de container | como Docker usa isso, e o que o daemon faz por cima |
| `Operação 3-01` | imagem de produção, imutabilidade, digest, não-root **como disciplina** | como a imagem é construída, o cache, as camadas |
| `Operação 3-02` | o contrato de runtime (probes, requests/limits, shutdown) | o modelo de objetos e o loop que os reconcilia |
| `Operação 3-05` | Ingress, Gateway API, mesh, NetworkPolicy **em produção** | a configuração do Nginx em si; rede do Docker |
| `Operação 2-05` | GitOps e IaC | — (nada aqui) |
| `Cloud 12` | ECS, Fargate, App Platform, K8s gerenciado | o Kubernetes que você mesmo opera |
| `Terminal` | ergonomia do shell, dotfiles, Lazydocker, TUIs | o sistema por baixo do shell |
| `Java/Go/Python cloud-native` | o Dockerfile **daquela** linguagem, JVM em container | o Dockerfile como mecanismo, agnóstico de stack |
| `Testes JS`, `Java/Testes 11` | Testcontainers como prática de teste | Docker em CI como mecanismo |

## Destino do material existente

**Os quatro monólitos viram tronco podado**, no padrão `Ferramentas/Versionamento.md`: tabela de redirecionamento para as notas do galho, e **preservação literal** das seções `Na prática (da minha experiência)` e `How to explain in English`. Isso é regra, não detalhe — esse material é relato pessoal do autor e material de entrevista; o galho **não** incorpora relato pessoal, e nada nele pode ser inventado.

| Arquivo | Linhas | Destino |
|---|---|---|
| `Docker.md` | 1298 | tronco podado → galho `Docker/` |
| `Kubernetes.md` | 1612 | tronco podado → galho `Kubernetes/` |
| `Nginx.md` | 1285 | tronco podado → galho `Nginx/` |
| `Linux.md` | 1118 | tronco podado → galho `Linux/` (que hoje tem 1 nota só) |
| `CI-CD.md` | 1309 | **fica podado** apontando para `Engenharia/Operação` (decisão de 2026-07-08, mantida) |
| `Observabilidade.md` | 1407 | **fica podado** apontando para `Engenharia/Operação` (idem) |
| `Digital Ocean.md` | 53 | aponta para `Cloud` galho 22 |
| `Infraestrutura.md` | 46 | absorvido pelo `index.md`; o `index` é o MOC do domínio |
| `Comandos Docker e WSL.md`, `Configurando Ambiente Linux no WSL.md`, `WSL, Docker e Kubernetes.md`, `Docker credential helpers.md` | — | **seguem como referência solta** — material de ambiente local, não viram galho |
| `Terminal.md` (a cópia que vive nesta estante) | 129 | aponta para `Tecnologia/Terminal` |

**Artefatos de domínio** (convenção do vault): criar `Dicionário de Infraestrutura.md` (`type: glossary`) e `Biblioteca de Infraestrutura.md` (`type: reference`, links verificados por HTTP). Nenhum dos dois existe hoje. Vão ao fim, quando os quatro galhos estiverem escritos e o vocabulário estabilizado.

## Galho 1 — Docker (roster detalhado)

**Lente: a imagem como artefato.** Tudo em Docker é consequência de uma única decisão de design — a imagem é imutável e composta de camadas. Cache de build, tamanho final, superfície de ataque, a ordem do `COPY`, por que o container morre quando o PID 1 morre: tudo cai fora dessa premissa. O galho é escrito para que o leitor consiga *prever* o comportamento em vez de consultar.

**18 notas.** Semente: `Docker.md` (1298 linhas, rico em código, `publish: false`).

### Iniciado — o modelo e o uso diário

| # | Nota | Recorte |
|---|---|---|
| 01 | O problema que o container resolve (e o que ele não é) | VM × container; o que Docker adiciona ao que o kernel já fazia; ponte explícita para `Ciência/SO 13` |
| 02 | A anatomia de uma imagem | camadas, união de sistemas de arquivos, camada de escrita do container, tag × digest |
| 03 | O ciclo de vida de um container | criar/rodar/parar/remover; PID 1; sinais; stdout/stderr como contrato de log |
| 04 | O Dockerfile como receita de camadas | instruções, o que cria camada e o que não cria, ordem como decisão |
| 05 | Build e cache — por que seu build está lento | invalidação de cache, a ordem do `COPY`, `.dockerignore`, contexto de build |
| 06 | Dados que sobrevivem ao container | volumes, bind mounts, tmpfs; por que o container é efêmero por design |
| 07 | Rede no Docker | bridge, host, none; DNS interno; publicar porta × expor porta |

### Adepto — construir bem

| # | Nota | Recorte |
|---|---|---|
| 08 | ENTRYPOINT, CMD e o container que não morre direito | exec × shell form; propagação de sinal; processo zumbi e `--init` |
| 09 | Multi-stage e imagens mínimas | alpine × distroless × scratch; trade-off de debug; fronteira declarada com `Operação 3-01` |
| 10 | BuildKit por dentro | cache mount, secret mount, ssh mount; grafo de build; multi-arch com buildx |
| 11 | Compose como ambiente de desenvolvimento | e **por que não é orquestrador de produção** — a ponte narrativa para o galho de Kubernetes |
| 12 | Registry | push/pull, tags imutáveis, digest, registry privado, retenção e custo |
| 13 | Segurança da imagem e do runtime | non-root, capabilities, read-only, scanning, o que uma CVE na base significa |
| 14 | Debugar um container | logs, exec, inspect, events; e o que fazer quando não há shell (distroless) |

### Magus — o que sustenta

| # | Nota | Recorte |
|---|---|---|
| 15 | Docker por dentro | daemon, containerd, runc, OCI; o que roda quando você dá `docker run`; fronteira com `Ciência/SO 13` |
| 16 | O ecossistema além do Docker | Podman, nerdctl, Buildah, rootless; onde Docker deixou de ser sinônimo de container |
| 17 | Docker em CI e na máquina de dev | docker-in-docker × socket montado, cache entre builds, ponte para Testcontainers |
| 18 | Capstone — empacotar uma app do zero | da app sem Dockerfile até a imagem que você defenderia numa revisão de produção |

## Galhos 2 a 4 (esboço)

Detalhamento vem quando cada um for aberto — o roster definitivo depende da fronteira que o galho anterior tiver cravado.

**Kubernetes — o loop de reconciliação** (~22-25 notas). Iniciado: o problema que orquestração resolve · o loop de reconciliação · Pod · Deployment/ReplicaSet · Service · namespaces e labels · `kubectl` como cliente de API. Adepto: Ingress e Gateway API · ConfigMap/Secret · volumes e StatefulSet · Job/CronJob · DaemonSet · scheduling (afinidade, taints) · RBAC · Helm e Kustomize. Magus: control plane por dentro (etcd, api-server, scheduler, controller-manager) · CRDs e operators · autoscaling (HPA/VPA/Cluster) · rede do cluster (CNI) · capstone. Fronteira permanente: o *contrato de runtime* fica em `Operação 3-02`; o *mecanismo* fica aqui.

**Nginx — o ciclo de vida de uma request** (~10-12 notas). Iniciado: o que Nginx é e o modelo de processos (master/worker, event loop) · a estrutura da configuração (contextos e herança) · `server` e a escolha do virtual host · `location` e a tabela de precedência de match. Adepto: proxy reverso e o que a barra final do `proxy_pass` faz · upstream e balanceamento · TLS · cache · compressão e rate limiting · logging e variáveis. Magus: tuning e o que medir · Nginx em container e como Ingress (ponte para `Operação 3-05`) · capstone.

**Linux — o sistema como o processo o vê** (~15-18 notas). Iniciado: hierarquia do sistema de arquivos · processos e sinais · permissões, usuários e grupos · descritores de arquivo e redirecionamento. Adepto: systemd e unidades · rede (interfaces, rotas, portas, DNS) · pacotes · logs e journald · agendamento (cron/timers). Magus: diagnosticar CPU, memória, disco e I/O · o que aconteceu no boot · OOM killer e por que o processo sumiu · cgroups e namespaces vistos de cima (fronteira com `Ciência/SO 13`) · capstone de investigação. Fronteira permanente com Terminal: lá é a *ergonomia do shell*, aqui é o *sistema por baixo dele*.

## Critérios de pronto

Por nota: padrão capítulo de livro · `fase:` no frontmatter · abertura por problema/cenário · diagramas Mermaid onde o assunto é estrutural · `## Armadilhas comuns` com `[!warning]` · seção de inglês com tabela PT↔EN · ponte `## O que vem a seguir` · `## Fontes` com URLs clicáveis · M1 (vídeo verificado por `yt-dlp`) na passada de enriquecimento.

Por galho: `index.md` (MOC agrupado por fase) · `roadmap.md` (convenção da árvore de roadmaps) · monólito-semente podado · callouts de volta inseridos nas notas de Operação/Cloud/SO que passam a ter contraparte aqui · zero wikilinks quebrados.

Por domínio: `index.md` reformado com o sanduíche de quatro camadas · Dicionário · Biblioteca · Roadmap central atualizado.

## Riscos conhecidos

**Redundância com Operação.** É o risco principal, e a mitigação é a tabela de fronteira acima somada à régua de que redundância entre notas é reforço, não defeito — o que se evita é *reexplicar pior*, não *tocar no mesmo assunto*.

**Caducidade.** Kubernetes e o ecossistema de containers envelhecem rápido (Gateway API sucedendo Ingress, Docker deixando de ser sinônimo de container, ambient mesh). Notas de ferramenta levam `[!info]` de caducidade com a versão-baseline cravada, como foi feito em Java 16/17.

**Escala.** Quatro galhos somam ~65-73 notas — comparável a um domínio inteiro. Construção sequencial com pergunta a cada bloco é o que impede isso de virar fan-out sem revisão.
