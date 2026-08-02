---
title: "Docker"
created: 2026-04-01
updated: 2026-08-02
type: reference
progress: done
status: evergreen
tags:
  - infraestrutura
  - devops
  - entrevista
publish: false
---

# Docker

> [!info] Tronco podado — o capítulo virou galho
> Esta nota era um monólito de referência técnica de ~1300 linhas. Em 2026-08-02 ela foi **podada**: o conteúdo conceitual virou o galho [[03-Dominios/Tecnologia/Infraestrutura/Docker/index|Docker]], com 18 notas em 3 fases sob a lente *a imagem como artefato*. O que permanece aqui é o material que **não pertence ao galho**: o relato de experiência do autor e o material de articulação em inglês, ambos preservados na íntegra.

## Onde cada assunto foi parar

| Assunto que estava aqui | Onde está agora |
|---|---|
| O que é container, container × VM | [[03-Dominios/Tecnologia/Infraestrutura/Docker/01 - O problema que o container resolve\|01 — O problema que o container resolve]] |
| Imagens, camadas, tags e digests | [[03-Dominios/Tecnologia/Infraestrutura/Docker/02 - A anatomia de uma imagem\|02 — A anatomia de uma imagem]] |
| Rodar containers, ciclo de vida | [[03-Dominios/Tecnologia/Infraestrutura/Docker/03 - O ciclo de vida de um container\|03 — O ciclo de vida de um container]] |
| Dockerfile, instruções principais | [[03-Dominios/Tecnologia/Infraestrutura/Docker/04 - O Dockerfile como receita de camadas\|04 — O Dockerfile como receita de camadas]] |
| Otimizar Dockerfile, layer caching | [[03-Dominios/Tecnologia/Infraestrutura/Docker/05 - Build e cache — por que seu build está lento\|05 — Build e cache]] |
| Volumes e persistência | [[03-Dominios/Tecnologia/Infraestrutura/Docker/06 - Dados que sobrevivem ao container\|06 — Dados que sobrevivem ao container]] |
| Networks | [[03-Dominios/Tecnologia/Infraestrutura/Docker/07 - Rede no Docker\|07 — Rede no Docker]] |
| ENTRYPOINT × CMD, exec × shell form | [[03-Dominios/Tecnologia/Infraestrutura/Docker/08 - ENTRYPOINT, CMD e o container que não morre direito\|08 — ENTRYPOINT, CMD e o container que não morre direito]] |
| Multi-stage builds, imagens mínimas | [[03-Dominios/Tecnologia/Infraestrutura/Docker/09 - Multi-stage e imagens mínimas\|09 — Multi-stage e imagens mínimas]] |
| BuildKit, buildx, mounts de cache e segredo | [[03-Dominios/Tecnologia/Infraestrutura/Docker/10 - BuildKit por dentro\|10 — BuildKit por dentro]] |
| Docker Compose | [[03-Dominios/Tecnologia/Infraestrutura/Docker/11 - Compose como ambiente de desenvolvimento\|11 — Compose como ambiente de desenvolvimento]] |
| Registry | [[03-Dominios/Tecnologia/Infraestrutura/Docker/12 - Registry\|12 — Registry]] |
| Segurança | [[03-Dominios/Tecnologia/Infraestrutura/Docker/13 - Segurança da imagem e do runtime\|13 — Segurança da imagem e do runtime]] |
| Troubleshooting | [[03-Dominios/Tecnologia/Infraestrutura/Docker/14 - Debugar um container\|14 — Debugar um container]] |
| Arquitetura, conceitos core | [[03-Dominios/Tecnologia/Infraestrutura/Docker/15 - Docker por dentro\|15 — Docker por dentro]] |
| Docker em desenvolvimento, Testcontainers | [[03-Dominios/Tecnologia/Infraestrutura/Docker/17 - Docker em CI e na máquina de dev\|17 — Docker em CI e na máquina de dev]] |
| Patterns de produção | [[03-Dominios/Tecnologia/Infraestrutura/Docker/18 - Capstone - empacotar uma app do zero\|18 — Capstone]] + [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/01 - Containers em produção\|Operação: containers em produção]] |
| Armadilhas comuns | distribuídas na seção `## Armadilhas comuns` de cada nota do galho |

## Na prática (da minha experiência)

> **Docker é minha primeira linha de defesa contra "funciona na minha máquina".** No MedEspecialista, toda a stack local (Postgres, Redis, Kafka, MinIO, Keycloak) roda via Docker Compose. Onboarding de um novo dev é `git clone && docker compose up`. 15 minutos e tudo está rodando.
>
> **Patterns que padronizei:**
>
> **1. Multi-stage sempre.** Runtime image nunca tem build tools. `node:22-alpine` para build, `distroless` ou `node:22-alpine` para runtime (dependendo de necessidades de debug).
>
> **2. Usuário não-root em todo Dockerfile.** Sem exceção. Imagens oficiais normalmente já têm um — use.
>
> **3. Layer ordering religioso.** `COPY package*.json` → `npm ci` → `COPY source`. Invalida cache só quando realmente precisa.
>
> **4. `.dockerignore` antes do primeiro build.** Inclui `node_modules`, `.git`, `.env*`, `coverage/`, `dist/`, IDE files.
>
> **5. BuildKit cache mounts** para node_modules e Maven repos. Build de CI caiu de 3 min para 40s.
>
> **6. Trivy scan no CI.** Toda PR roda scan. Falhas com critical/high severities bloqueiam merge.
>
> **7. Digests em produção.** `image@sha256:...`, não `image:tag`. Garantia absoluta de que a imagem não mudou silenciosamente.
>
> **8. Healthchecks em todos os services.** Compose usa `condition: service_healthy` em `depends_on`.
>
> **Incidente memorável — imagem gigante:**
>
> API Node demorava 30+ min para deploy. Imagem era de 1.2 GB. Diagnóstico: `COPY . .` incluía `node_modules` local (Linux vs Mac binaries), `.git`, logs, `coverage/`. Depois de `.dockerignore` + multi-stage + `npm ci --only=production`, imagem caiu para 85 MB. Deploy de 30min → 3min.
>
> **Outro incidente — container fica reiniciando:**
>
> Container Spring Boot reiniciava a cada 30s em produção. Logs mostravam `healthcheck failed`. Causa: `HEALTHCHECK` chamava `curl http://localhost:8080/actuator/health`, mas `curl` não estava instalado na imagem alpine. Fix: instalar curl, OU mudar para `wget`, OU usar probe via JVM direto.
>
> **Alpine pitfall com Node:**
>
> Alpine usa musl libc, não glibc. Alguns binários Node (sharp, bcrypt) precisam de builds específicas. Algumas bibliotecas falham silenciosamente. Solução: usar `node:22-slim` (Debian) em vez de alpine quando tiver dependências nativas. 20 MB a mais, dor de cabeça zero.
>
> **A lição principal:** Docker é enganosamente simples. Um Dockerfile que "funciona" pode ter problemas de segurança, performance, manutenibilidade. Investir em multi-stage, security scanning, layer optimization e non-root paga por si mesmo rápido.

---

## How to explain in English

> "Docker fundamentally changed how I deploy applications. Containers provide the reproducibility I need without the overhead of VMs — same image runs identically in dev, staging, and production. That said, writing a Dockerfile that works is easy. Writing one that's secure, small, and fast requires discipline.
>
> My defaults: multi-stage builds separating build tools from runtime, non-root users, pinned base images (never `:latest`), `.dockerignore` to avoid polluting the build context, layer ordering from least to most frequently changed. For runtime images I prefer distroless over alpine — no shell, no package manager, tiny attack surface. For Go, I use `scratch` and statically linked binaries.
>
> Docker Compose is my default for local development environments. A single `compose.yaml` describes the entire stack — application, database, cache, message broker — and a new developer is productive in under 15 minutes with `docker compose up`. I use healthchecks with `depends_on: condition: service_healthy` to avoid race conditions between services.
>
> For security, I scan every image with Trivy in CI and fail builds on critical vulnerabilities. I never embed secrets in images — always passed at runtime via environment variables or mounted from Docker secrets, Kubernetes secrets, or Vault. I drop all capabilities and add back only what's needed.
>
> In production, I use image digests instead of tags to guarantee reproducibility, set resource limits, configure graceful shutdown handlers that catch SIGTERM, and log to stdout so Docker and Kubernetes can collect centrally. One process per container, stateless by default, with all persistent data in volumes or external services.
>
> Common pitfalls I watch for: running as root, `COPY . .` without `.dockerignore`, shell form in CMD/ENTRYPOINT that breaks signal handling, installing build tools in runtime images, and using `:latest` anywhere. And always multi-stage — the single biggest win for image size and security."

### Frases úteis em entrevista

- "Multi-stage builds always — build tools never touch runtime images."
- "Non-root user in every Dockerfile, no exceptions."
- "Distroless images for production — no shell, no package manager, minimal attack surface."
- "Layer ordering from least to most frequently changed to maximize cache hits."
- "`.dockerignore` is the first thing I add to any project."
- "Image digests in production, not tags. Reproducibility is non-negotiable."
- "Secrets never in images — always at runtime via env vars or secret stores."
- "One process per container. Logs to stdout. Stateless by default."
- "BuildKit cache mounts cut my CI build times dramatically."
- "Trivy in CI blocks critical CVEs from merging."

### Key vocabulary

- contêiner → container
- imagem → image
- camada → layer
- registro → registry
- construção multi-estágio → multi-stage build
- montagem → mount
- volume persistente → persistent volume
- verificação de saúde → healthcheck
- desligamento gracioso → graceful shutdown
- cache de camada → layer cache
- cadeia de suprimentos → supply chain
- varredura de vulnerabilidade → vulnerability scanning
- assinatura → digest
- privilégio mínimo → least privilege
- sem raiz → rootless

---

## Recursos

### Documentação

- [Docker Docs](https://docs.docker.com/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Docker Compose spec](https://docs.docker.com/compose/compose-file/)
- [BuildKit docs](https://docs.docker.com/build/buildkit/)
- [OCI Spec](https://opencontainers.org/)

### Livros e cursos

- **Docker Deep Dive** — Nigel Poulton (atualizado regularmente)
- **Docker in Action** — Jeff Nickoloff, Stephen Kuenzli
- **Full Stack Open Part 12** — Containers (da Universidade de Helsinki, gratuito)

### Blogs e artigos

- [Julia Evans — Container articles](https://jvns.ca/categories/containers/)
- [Docker blog](https://www.docker.com/blog/)
- [Ivan Velichko — Container learning](https://iximiuz.com/en/)
- [Google Distroless](https://github.com/GoogleContainerTools/distroless)

### Ferramentas

- [Trivy](https://trivy.dev/) — vulnerability scanning
- [Dive](https://github.com/wagoodman/dive) — explorar layers de imagem
- [Hadolint](https://github.com/hadolint/hadolint) — Dockerfile linter
- [ctop](https://github.com/bcicen/ctop) — `top` para containers
- [lazydocker](https://github.com/jesseduffield/lazydocker) — TUI para Docker
- [Docker Scout](https://docs.docker.com/scout/) — image analysis built-in

### Base images recomendadas

- [Distroless](https://github.com/GoogleContainerTools/distroless) — Java, Python, Node, Go
- [Chainguard Images](https://www.chainguard.dev/chainguard-images) — minimal, continuously updated
- [Alpine](https://alpinelinux.org/) — leve mas cuidado com musl libc

---


## Veja também

- [[03-Dominios/Tecnologia/Infraestrutura/Docker/index|Docker (galho)]] — as 18 notas que sucedem este monólito
- [[03-Dominios/Tecnologia/Infraestrutura/index|Infraestrutura]] — o domínio
- [[03-Dominios/Engenharia/Operação/index|Engenharia/Operação]] — a disciplina de rodar isso em produção
- [[03-Dominios/Ciência/Sistemas Operacionais/13 - Virtualização e containers|Virtualização e containers]] — o mecanismo no kernel
