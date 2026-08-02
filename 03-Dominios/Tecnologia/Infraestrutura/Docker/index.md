---
title: "Docker"
created: 2026-08-02
updated: 2026-08-02
type: moc
status: growing
publish: true
tags:
  - moc
  - infraestrutura
  - docker
  - containers
aliases:
  - "Docker (galho)"
  - "Galho Docker"
---

# Docker

> [!abstract] TL;DR
> Primeiro galho do domínio [[03-Dominios/Tecnologia/Infraestrutura/index|Infraestrutura]], sob a lente **a imagem como artefato**: quase tudo que o Docker faz é consequência de uma única decisão de design — a imagem é imutável e composta de camadas. Cache de build, tamanho final, superfície de ataque, a ordem do `COPY`, o container que ignora `Ctrl+C`: nada disso é regra arbitrária, é corolário. O galho sobe do modelo (o que uma imagem é, o que um container é enquanto roda) para a construção deliberada (multi-stage, BuildKit, registry, segurança) e fecha no mecanismo (daemon, containerd, runc, OCI) e num capstone que empacota uma app do zero. 18 notas, 3 fases.

## Sobre este galho

Este galho existe porque o resto do vault já opera Docker sem nunca o ensinar. A nota [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/01 - Containers em produção|Containers em produção]] abre dizendo, com todas as letras, que assume que você já sabe escrever um Dockerfile. É esse pressuposto que mora aqui.

O recorte não é tutorial. Comando envelhece, e a documentação oficial faz isso melhor. O que este galho entrega é a capacidade de **prever** o comportamento em vez de consultá-lo: por que o build ficou lento depois de uma mudança de uma linha, por que o container demora dez segundos para morrer, por que a imagem tem 1,2 GB, por que o segredo que você passou em `--build-arg` está gravado na imagem para sempre. Todas essas perguntas têm a mesma raiz, e o galho a persegue do começo ao fim.

**Audiência primária:** quem já usa Docker todo dia por receita e trava quando o comportamento foge do esperado. **Audiência secundária:** quem vai responder, num loop de entrevista sênior, o que acontece entre `docker run` e o processo existir.

> [!info] Fronteira — o sanduíche de quatro camadas
> Este galho é a fatia do meio de quatro camadas que o vault cobre em casas diferentes:
>
> | Camada | Casa | Pergunta que responde |
> |---|---|---|
> | Mecanismo | [[03-Dominios/Ciência/Sistemas Operacionais/13 - Virtualização e containers\|Ciência/SO 13]] | como o isolamento funciona no kernel (namespaces, cgroups, runc, OCI) |
> | **A ferramenta** | **este galho** | **como o Docker funciona por dentro** |
> | O ofício | [[03-Dominios/Engenharia/Operação/index\|Engenharia/Operação]] | o que muda quando é produção |
> | A plataforma | [[03-Dominios/Tecnologia/Cloud/12 - Containers gerenciados/index\|Cloud, galho 12]] | quando alguém gerencia o container por você |
>
> Onde a camada vizinha já cobre melhor, este galho **linka em vez de repetir**. O Dockerfile de uma linguagem específica também fica fora: isso vive nos galhos cloud-native de [[03-Dominios/Tecnologia/Java/index\|Java]], [[03-Dominios/Tecnologia/Go/index\|Go]] e [[03-Dominios/Tecnologia/Python/index\|Python]].

## Iniciado — o modelo e o uso diário

1. [[03-Dominios/Tecnologia/Infraestrutura/Docker/01 - O problema que o container resolve|01 — O problema que o container resolve (e o que ele não é)]] — VM contra container em custo e isolamento, o que o Docker acrescenta ao que o kernel já fazia, e as três coisas que Docker não é.
2. [[03-Dominios/Tecnologia/Infraestrutura/Docker/02 - A anatomia de uma imagem|02 — A anatomia de uma imagem]] — camadas, união de sistemas de arquivos, a camada de escrita do container, tag contra digest.
3. [[03-Dominios/Tecnologia/Infraestrutura/Docker/03 - O ciclo de vida de um container|03 — O ciclo de vida de um container]] — os estados, o PID 1, a propagação de sinal e por que `docker stop` demora dez segundos.
4. [[03-Dominios/Tecnologia/Infraestrutura/Docker/04 - O Dockerfile como receita de camadas|04 — O Dockerfile como receita de camadas]] — o que cria camada e o que não cria, e a ordem das instruções como decisão de design.
5. [[03-Dominios/Tecnologia/Infraestrutura/Docker/05 - Build e cache — por que seu build está lento|05 — Build e cache: por que seu build está lento]] — invalidação em cascata, a ordem do `COPY`, `.dockerignore` e o custo do contexto de build.
6. [[03-Dominios/Tecnologia/Infraestrutura/Docker/06 - Dados que sobrevivem ao container|06 — Dados que sobrevivem ao container]] — volumes, bind mounts e tmpfs; por que o container é efêmero por design.
7. [[03-Dominios/Tecnologia/Infraestrutura/Docker/07 - Rede no Docker|07 — Rede no Docker]] — bridge, host e none; o DNS interno; publicar porta contra `EXPOSE`, que não publica nada.

## Adepto — construir bem e operar a imagem

8. [[03-Dominios/Tecnologia/Infraestrutura/Docker/08 - ENTRYPOINT, CMD e o container que não morre direito|08 — ENTRYPOINT, CMD e o container que não morre direito]] — forma exec contra forma shell, sinal engolido, processo zumbi e `--init`.
9. [[03-Dominios/Tecnologia/Infraestrutura/Docker/09 - Multi-stage e imagens mínimas|09 — Multi-stage e imagens mínimas]] — alpine, distroless e scratch com o trade-off honesto de cada um.
10. [[03-Dominios/Tecnologia/Infraestrutura/Docker/10 - BuildKit por dentro|10 — BuildKit por dentro]] — o grafo de build, cache mount, secret mount e o build multi-arquitetura.
11. [[03-Dominios/Tecnologia/Infraestrutura/Docker/11 - Compose como ambiente de desenvolvimento|11 — Compose como ambiente de desenvolvimento]] — o que ele resolve bem e por que não é orquestrador de produção.
12. [[03-Dominios/Tecnologia/Infraestrutura/Docker/12 - Registry|12 — Registry]] — push e pull como transferência de camadas, tag imutável contra digest, retenção e custo.
13. [[03-Dominios/Tecnologia/Infraestrutura/Docker/13 - Segurança da imagem e do runtime|13 — Segurança da imagem e do runtime]] — não-root, capabilities, sistema de arquivos somente leitura e o que uma CVE na base significa.
14. [[03-Dominios/Tecnologia/Infraestrutura/Docker/14 - Debugar um container|14 — Debugar um container]] — logs, exec, inspect e events; e o que fazer quando não há shell.

## Magus — o que sustenta

15. [[03-Dominios/Tecnologia/Infraestrutura/Docker/15 - Docker por dentro|15 — Docker por dentro]] — cliente, daemon, containerd, runc e o padrão OCI que desacoplou tudo isso.
16. [[03-Dominios/Tecnologia/Infraestrutura/Docker/16 - O ecossistema além do Docker|16 — O ecossistema além do Docker]] — Podman, nerdctl, Buildah e o modelo rootless.
17. [[03-Dominios/Tecnologia/Infraestrutura/Docker/17 - Docker em CI e na máquina de dev|17 — Docker em CI e na máquina de dev]] — docker-in-docker contra socket montado, cache entre builds e a ponte para Testcontainers.
18. [[03-Dominios/Tecnologia/Infraestrutura/Docker/18 - Capstone - empacotar uma app do zero|18 — Capstone: empacotar uma app do zero]] — da app sem Dockerfile até a imagem que você defenderia numa revisão de produção.

## Rotas alternativas

### Completa

01 → 18, na ordem. O galho é escrito como uma sequência: cada nota fecha um assunto que a anterior abriu de propósito.

### Já uso Docker, quero fechar as lacunas

02 (o que a imagem realmente é) → 05 (por que o build está lento) → 08 (o container que não morre direito) → 15 (o que roda quando você digita `docker run`).

### Vou ser entrevistado sobre containers

01 → 02 → 15 → 09 → 13. O arco que responde "o que é um container, por baixo?" e "como você constrói uma imagem que se defende em produção?".

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Infraestrutura/Docker" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Infraestrutura/index|Infraestrutura]] — MOC do domínio
- [[03-Dominios/Tecnologia/Infraestrutura/Docker.md|Docker (tronco)]] — a nota de referência técnica que originou este galho
- [[03-Dominios/Ciência/Sistemas Operacionais/13 - Virtualização e containers|Virtualização e containers]] — o mecanismo no kernel
- [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/01 - Containers em produção|Containers em produção]] — a mesma imagem, sob a disciplina de produção
- [[03-Dominios/Tecnologia/Terminal/TUIs/02 - Lazydocker — overview e operações comuns|Lazydocker]] — a interface de terminal para o que este galho ensina na mão
