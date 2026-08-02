---
title: "Plano de execução — Galho 1: Docker"
created: 2026-08-02
updated: 2026-08-02
type: spec
publish: false
tags:
  - meta
  - spec
  - plano
  - infraestrutura
  - docker
---

# Plano de execução — Galho 1: Docker

> **Para quem executa:** cada bloco abaixo é uma unidade de trabalho fechada, com gate próprio. Escrita de nota usa a skill `/escrever-nota`; o gate é `/verificar-nota`. Passos usam checkbox (`- [ ]`) para rastreio. Fonte do desenho: [[00-Meta/specs/2026-08-02-dominio-infraestrutura-design|design do domínio]].

**Objetivo:** escrever as 18 notas do galho `Tecnologia/Infraestrutura/Docker`, em 3 fases, sob a lente *a imagem como artefato*, e podar o monólito `Docker.md` ao final.

**Arquitetura:** galho-folha com `index.md` (MOC por fase) + `roadmap.md` (árvore de roadmaps) + 18 notas numeradas `01..18`. A semente é `Docker.md` (1298 linhas, `publish: false`), rica em código e já organizada por assunto. As notas **não** herdam a estrutura do monólito: o monólito é referência técnica, o galho é narrativa.

**Ferramental:** `/escrever-nota` (criação) · `/verificar-nota` (gate) · `/verificar-wikilinks` (integridade) · `yt-dlp` (M1, passada posterior) · Mermaid para diagramas.

## Restrições globais

Valem para toda nota deste galho, copiadas da spec:

- **Lente:** a imagem como artefato — tudo em Docker é consequência de a imagem ser imutável e em camadas. Toda nota deve poder ser lida como corolário disso.
- **Escala:** padrão capítulo de livro, 440-540 linhas, escala Cloud/Go. Não é o registro curto de Controle de Versão.
- **Fase:** `fase:` no frontmatter — `Iniciado` (01-07), `Adepto` (08-14), `Magus` (15-18).
- **Numeração:** por galho, `01..18`, dentro de `Infraestrutura/Docker/`.
- **Núcleo obrigatório por nota:** TL;DR `[!abstract]` · abertura por problema/cenário (nunca "X é...") · corpo-mecanismo · `## Armadilhas comuns` com ≥3 `[!warning]` · seção de inglês com tabela PT↔EN · `## O que vem a seguir` (ponte para a próxima nota da sequência, não para "notas relacionadas") · `## Fontes` com URLs clicáveis.
- **Diagramas:** Mermaid onde o assunto é estrutural. `quadrantChart` é proibido (risco de render, decisão de 2026-07-31).
- **Caducidade:** toda nota que crava versão ou comportamento de ferramenta leva `[!info]` de caducidade com a baseline declarada.
- **Nada inventado:** proibido fabricar experiência, cliente ou caso do autor. O relato pessoal do monólito fica no tronco podado, não migra para as notas.
- **Sem quebra manual de linha:** parágrafo é uma linha só, por mais longa.
- **Fronteira:** onde `Operação`, `Cloud 12` ou `Ciência/SO 13` já cobrem, linkar em vez de reexplicar. A tabela de fronteira está na spec e é normativa.

---

## Bloco 0 — Esqueleto do galho

**Arquivos:**
- Criar: `03-Dominios/Tecnologia/Infraestrutura/Docker/index.md`
- Criar: `03-Dominios/Tecnologia/Infraestrutura/Docker/roadmap.md`

**Interfaces:**
- Produz: a pasta e os dois artefatos de rastreio que todos os blocos seguintes atualizam. O `roadmap.md` segue `00-Meta/templates/Template - Roadmap.md` em modo galho-folha, com uma linha por nota (estado, pendências).

- [ ] **Passo 1:** criar `Docker/index.md` como MOC agrupado por fase, com as 18 notas listadas (links ainda quebrados — serão resolvidos conforme as notas nascem), TL;DR declarando a lente, e callout de fronteira reproduzindo o sanduíche de quatro camadas da spec.
- [ ] **Passo 2:** criar `Docker/roadmap.md` em modo galho-folha, 18 linhas, todas `📋 desenhada, não escrita`.
- [ ] **Passo 3:** commit — `feat(infra): abre galho Docker — index e roadmap`.

---

## Bloco 1 — Iniciado, o modelo (notas 01-04)

**Arquivos:** criar `Docker/01..04`. Modificar `Docker/index.md`, `Docker/roadmap.md`.

**Interfaces:**
- Consome: nada. É a entrada do galho.
- Produz: o vocabulário que o galho inteiro usa — *camada*, *imagem*, *container*, *tag*, *digest*, *camada de escrita*, *PID 1*. As notas seguintes assumem esses termos definidos e **não** os reintroduzem.

- [ ] **Passo 1: nota 01 — O problema que o container resolve (e o que ele não é).** Abre pelo cenário do "funciona na minha máquina" e pela pergunta que o leitor sênior tem: o que o Docker adiciona ao que o kernel já fazia? Contrasta VM × container em custo e isolamento. Ponte explícita e declarada para [[03-Dominios/Ciência/Sistemas Operacionais/13 - Virtualização e containers|Ciência/SO 13]] — o mecanismo de namespaces e cgroups **fica lá**; aqui entra só o que Docker constrói por cima. Fecha dizendo o que Docker **não** é: não é VM, não é sistema de deploy, não é orquestrador.
- [ ] **Passo 2: nota 02 — A anatomia de uma imagem.** O coração da lente. Camadas, união de sistemas de arquivos, a camada de escrita do container (copy-on-write), por que dois containers da mesma imagem não se enxergam. Tag × digest, e por que `latest` é uma mentira conveniente. Diagrama Mermaid da pilha de camadas.
- [ ] **Passo 3: nota 03 — O ciclo de vida de um container.** Criar/rodar/parar/remover como estados, não como comandos. PID 1 e o que muda para um processo que é o init do próprio namespace. Propagação de sinal e por que `docker stop` demora dez segundos. `stdout`/`stderr` como o contrato de log (ponte para Observabilidade em Operação).
- [ ] **Passo 4: nota 04 — O Dockerfile como receita de camadas.** Cada instrução lida como "isto cria uma camada, aquilo não". Ordem como decisão de design, não de estilo. Prepara a 05 sem entregá-la.
- [ ] **Passo 5: gate.** Rodar `/verificar-nota` nas quatro. Corrigir o que o checklist apontar antes de seguir.
- [ ] **Passo 6:** atualizar `index.md` e `roadmap.md` (4 notas → `🔶 escrita`), commitar — `feat(infra): Docker 01-04 — o modelo da imagem`.
- [ ] **Passo 7: parada de revisão.** Apresentar as 4 notas ao usuário e perguntar se a lente está pegando antes de escrever mais.

---

## Bloco 2 — Iniciado, o uso diário (notas 05-07)

**Arquivos:** criar `Docker/05..07`. Modificar `index.md`, `roadmap.md`.

**Interfaces:**
- Consome: *camada* e *cache de camada* (nota 02, 04); *ciclo de vida* (nota 03).
- Produz: o modelo de armazenamento e de rede que as notas 09, 11 e 13 assumem.

- [ ] **Passo 1: nota 05 — Build e cache: por que seu build está lento.** Invalidação de cache camada a camada; a ordem do `COPY` como a otimização que mais rende; `.dockerignore` e o custo do contexto de build enviado ao daemon. Exemplo trabalhado com um build lento virando rápido, com o diff de Dockerfile lado a lado.
- [ ] **Passo 2: nota 06 — Dados que sobrevivem ao container.** Volumes × bind mounts × tmpfs; onde cada um vive na máquina; por que o container é efêmero por design e o que isso implica para banco em container. Armadilha central: bind mount mascarando permissão em Linux.
- [ ] **Passo 3: nota 07 — Rede no Docker.** Drivers bridge/host/none; o DNS interno que resolve nome de serviço; publicar porta × `EXPOSE` (que não publica nada). Prepara o Compose sem entregá-lo.
- [ ] **Passo 4: gate.** `/verificar-nota` nas três.
- [ ] **Passo 5:** atualizar rastreio e commitar — `feat(infra): Docker 05-07 — cache, volumes e rede`.

---

## Bloco 3 — Adepto, construir bem (notas 08-11)

**Arquivos:** criar `Docker/08..11`. Modificar `index.md`, `roadmap.md`.

**Interfaces:**
- Consome: *PID 1* e *sinal* (nota 03); *camada* e *cache* (02, 04, 05); *rede* e *volume* (06, 07).
- Produz: a nota 11 é a **ponte narrativa para o galho de Kubernetes** — ela precisa terminar com a limitação que motiva orquestração, porque o galho 2 vai abrir citando exatamente esse ponto.

- [ ] **Passo 1: nota 08 — ENTRYPOINT, CMD e o container que não morre direito.** Exec form × shell form e por que a segunda engole o SIGTERM; processo zumbi e `--init`; a combinação ENTRYPOINT+CMD como template de comando. É a nota que fecha o assunto aberto na 03.
- [ ] **Passo 2: nota 09 — Multi-stage e imagens mínimas.** Alpine × distroless × scratch com trade-off honesto (musl × glibc, ausência de shell contra debug). **Fronteira declarada em callout:** a *disciplina* de imagem de produção (imutabilidade, digest, não-root como política) fica em [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/01 - Containers em produção|Operação 3-01]]; aqui é a *construção*.
- [ ] **Passo 3: nota 10 — BuildKit por dentro.** O grafo de build que substituiu a execução linear; cache mount, secret mount e ssh mount (e por que `--build-arg` para segredo vaza na imagem); multi-arch com buildx. `[!info]` de caducidade com a baseline cravada.
- [ ] **Passo 4: nota 11 — Compose como ambiente de desenvolvimento.** O que Compose resolve bem (subir a dependência local em um comando) e por que **não** é orquestrador de produção — sem reconciliação, sem escala real, sem tolerância a falha de nó. Termina apontando a lacuna que o galho de Kubernetes preenche.
- [ ] **Passo 5: gate.** `/verificar-nota` nas quatro.
- [ ] **Passo 6:** atualizar rastreio e commitar — `feat(infra): Docker 08-11 — construir bem e o limite do Compose`.
- [ ] **Passo 7: parada de revisão.** Perguntar ao usuário se a fronteira com Operação está no lugar certo — este é o bloco onde ela mais aperta.

---

## Bloco 4 — Adepto, operar a imagem (notas 12-14)

**Arquivos:** criar `Docker/12..14`. Modificar `index.md`, `roadmap.md`.

**Interfaces:**
- Consome: *digest* e *tag* (nota 02); *imagem mínima* (09).
- Produz: o vocabulário de registry e de diagnóstico que a 17 e o capstone reutilizam.

- [ ] **Passo 1: nota 12 — Registry.** Push/pull como transferência de camadas (e por que só as camadas novas sobem); tag imutável × digest; registry privado, autenticação, retenção e custo de armazenamento. Menciona `Docker credential helpers.md` como referência solta da estante.
- [ ] **Passo 2: nota 13 — Segurança da imagem e do runtime.** Non-root, capabilities, read-only, seccomp de raspão; o que uma CVE na imagem base significa na prática e por que scanning é higiene contínua, não gate único. Fronteira com `Engenharia/Segurança` declarada.
- [ ] **Passo 3: nota 14 — Debugar um container.** `logs`, `exec`, `inspect`, `events`, `stats`; e a parte que raramente se ensina: o que fazer quando **não há shell** porque a imagem é distroless — container efêmero de debug, `nsenter`, copiar binário. Fecha o arco aberto na 09 (imagem mínima cobra preço no debug).
- [ ] **Passo 4: gate.** `/verificar-nota` nas três.
- [ ] **Passo 5:** atualizar rastreio e commitar — `feat(infra): Docker 12-14 — registry, segurança e debug`.

---

## Bloco 5 — Magus (notas 15-17)

**Arquivos:** criar `Docker/15..17`. Modificar `index.md`, `roadmap.md`.

**Interfaces:**
- Consome: todo o vocabulário anterior. É a camada que reexplica o que já foi usado, agora pelo mecanismo.
- Produz: o fechamento conceitual que o capstone assume.

- [ ] **Passo 1: nota 15 — Docker por dentro.** O que roda quando você digita `docker run`: cliente → daemon → containerd → runc → o processo. OCI como o padrão que desacoplou tudo isso. **Fronteira dura:** namespaces e cgroups ficam em Ciência/SO 13 — aqui é a cadeia de componentes do Docker, não o mecanismo do kernel.
- [ ] **Passo 2: nota 16 — O ecossistema além do Docker.** Podman (e o modelo daemonless/rootless), nerdctl, Buildah; por que Docker deixou de ser sinônimo de container e o que isso muda na prática de quem escreve Dockerfile. `[!info]` de caducidade.
- [ ] **Passo 3: nota 17 — Docker em CI e na máquina de dev.** Docker-in-Docker × socket montado e o risco de segurança do segundo; cache de camada entre builds de CI; ponte para Testcontainers em [[03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes|Java/Testes 11]] e para `Tecnologia/Testes JS`.
- [ ] **Passo 4: gate.** `/verificar-nota` nas três.
- [ ] **Passo 5:** atualizar rastreio e commitar — `feat(infra): Docker 15-17 — o mecanismo e o ecossistema`.

---

## Bloco 6 — Capstone (nota 18)

**Arquivos:** criar `Docker/18 - Capstone - empacotar uma app do zero.md`.

**Interfaces:**
- Consome: as 17 anteriores.
- Produz: nada — é a folha do galho.

- [ ] **Passo 1: nota 18 — Capstone: empacotar uma app do zero.** Caso trabalhado, não resumo (padrão da nota 17 de Complexidade de Software). Parte de uma app sem Dockerfile e chega à imagem que se defenderia numa revisão de produção, decidindo em voz alta a cada passo: base, ordem de camadas, multi-stage, usuário, healthcheck, tag. Cada decisão referencia a nota que a fundamenta. Fecha com o que **não** cabe aqui e mora em Operação.
- [ ] **Passo 2: gate.** `/verificar-nota`.
- [ ] **Passo 3:** commitar — `feat(infra): Docker 18 — capstone`.

---

## Bloco 7 — Fechamento do galho

**Arquivos:**
- Modificar: `Infraestrutura/Docker.md` (poda), `Infraestrutura/index.md`, `Docker/index.md`, `Docker/roadmap.md`, `Infraestrutura/roadmap.md` (criar se não existir)
- Modificar: notas de fronteira que ganham callout de volta

- [ ] **Passo 1: podar `Docker.md`.** Vira tronco: TL;DR curto, tabela de redirecionamento assunto → nota do galho, e **preservação literal** das seções `Na prática (da minha experiência)` e `How to explain in English`. Modelo: `Ferramentas/Versionamento.md`.
- [ ] **Passo 2: callouts de volta.** Inserir em `Operação 3-01` (aponta para 02/04/05/09), `Ciência/SO 13` (aponta para 15) e `Cloud 12-01` (aponta para 01/02) um callout dizendo onde mora a contraparte. Mesmo movimento feito em Arqueologia quando Controle de Versão fechou.
- [ ] **Passo 3:** reformar `Infraestrutura/index.md` — absorver `Infraestrutura.md`, publicar o sanduíche de quatro camadas, listar o galho Docker.
- [ ] **Passo 4:** criar `Infraestrutura/roadmap.md` (raiz de domínio) com os quatro galhos e seus estados.
- [ ] **Passo 5:** rodar `/verificar-wikilinks` na pasta `Infraestrutura/` — gate de zero links quebrados. Atenção à regra do Quartz: link para pasta exige `index.md`.
- [ ] **Passo 6:** atualizar o Roadmap central (item Infraestrutura no Tier 2 e na tabela de Tecnologia).
- [ ] **Passo 7:** commitar — `feat(infra): fecha galho Docker — poda o monólito e reforma a estante`.
- [ ] **Passo 8:** perguntar ao usuário se abre o galho 2 (Kubernetes) ou para aqui.

---

## O que fica fora deste plano

- **M1 (mídia).** Passada posterior, depois da escrita — modelo de todos os galhos do vault. Busca e verificação de ID **centrais via `yt-dlp`**, nunca delegadas a subagente: ID de YouTube é o dado que subagente mais alucina.
- **Dicionário e Biblioteca de Infraestrutura.** Artefatos de domínio, criados quando os quatro galhos estiverem escritos e o vocabulário estabilizado.
- **Galhos 2-4.** Cada um ganha seu próprio plano, com roster detalhado no momento da abertura.

## Governança de custo

Escrita de nota é tarefa de execução, não de arquitetura: roda em Sonnet. Se houver fan-out, **teto de 3 subagentes por bloco** — nunca um agente por nota dos 18. O orquestrador não escreve nota diretamente quando estiver delegando; e quando escrever, escreve inline sem subagente. Workflow (fan-out massivo) só com opt-in explícito do usuário.
