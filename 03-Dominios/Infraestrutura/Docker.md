---
title: "Docker"
created: 2026-04-01
updated: 2026-04-11
type: concept
status: evergreen
tags:
  - infraestrutura
  - devops
  - entrevista
publish: false
---

# Docker

Deep dive em **Docker** — containers, imagens, Dockerfile, Compose, volumes, networks, multi-stage builds, segurança, e patterns de produção. Para orquestração em escala, ver [[Kubernetes]]. Para Linux foundation, ver [[Linux]]. Para reverse proxy, ver [[Nginx]].

## O que é

Docker é uma **plataforma de containerização** que empacota aplicações e suas dependências em unidades isoladas e portáveis chamadas **containers**. Criado em 2013 por Solomon Hykes na dotCloud, revolucionou deploy e desenvolvimento — transformou "funciona na minha máquina" em "funciona em qualquer máquina".

**Container vs VM:**

```
┌─────────────────────┐        ┌─────────────────────┐
│    VM               │        │   Container         │
│  ┌────────────────┐ │        │  ┌───────────────┐  │
│  │   App          │ │        │  │    App        │  │
│  ├────────────────┤ │        │  ├───────────────┤  │
│  │  Bins/Libs     │ │        │  │  Bins/Libs    │  │
│  ├────────────────┤ │        │  └───────────────┘  │
│  │   Guest OS     │ │        │                     │
│  ├────────────────┤ │        │  Shared kernel      │
│  │   Hypervisor   │ │        │  (Linux)            │
│  ├────────────────┤ │        ├─────────────────────┤
│  │   Host OS      │ │        │   Host OS           │
│  ├────────────────┤ │        ├─────────────────────┤
│  │   Hardware     │ │        │   Hardware          │
│  └────────────────┘ │        └─────────────────────┘
└─────────────────────┘

~ GB de RAM por VM              ~ MB de RAM por container
Minutos para iniciar            Segundos para iniciar
```

**Containers vs VMs:**

- **Containers compartilham o kernel** do OS host → mais leves
- **Isolamento via namespaces e cgroups** (Linux kernel features)
- **Imagens em camadas (layers)** — deduplicação automática
- **Deploy imutável** — mesma imagem roda em dev, staging, prod

Em entrevistas, o que diferencia um senior em Docker:

1. **Entender a arquitetura** — daemon, client, registry, runtime (containerd, runc)
2. **Escrever Dockerfile otimizado** — layers, cache, multi-stage, imagens pequenas
3. **Volumes e networks** — persistência e comunicação entre containers
4. **Docker Compose** — orquestração local, dev environments
5. **Segurança** — non-root users, secrets, vulnerability scanning, supply chain
6. **Debugging** — logs, exec, inspect, stats, top
7. **Performance** — startup time, image size, build cache
8. **Production patterns** — healthchecks, restart policies, graceful shutdown
9. **Registry** — Docker Hub, ECR, GHCR, private registries
10. **Moderno** — BuildKit, Buildx, multi-arch builds, rootless Docker

---

## Arquitetura

```
┌─────────────────────────────────────────────────┐
│  Docker Client (docker CLI)                     │
│  docker build, docker run, docker pull, ...     │
└────────────────┬────────────────────────────────┘
                 │ REST API (socket)
                 ↓
┌─────────────────────────────────────────────────┐
│  Docker Daemon (dockerd)                        │
│  ┌────────────────┐  ┌────────────────────┐     │
│  │  Image Manager │  │  Container Manager │     │
│  └────────────────┘  └──────────┬─────────┘     │
│                                 │                │
│  ┌──────────────────────────────┴──────────┐    │
│  │  containerd  (container runtime)         │    │
│  └──────────────────┬──────────────────────┘    │
│                     │                            │
│  ┌──────────────────┴──────────────────────┐    │
│  │  runc  (OCI runtime — creates containers)│    │
│  └──────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
         ↕
┌─────────────────────┐
│  Registry           │ Docker Hub, ECR, GHCR, ...
│  (imagens)          │
└─────────────────────┘
```

**Componentes:**

- **Docker Client** (`docker`) — CLI que você usa. Fala com o daemon via socket (`/var/run/docker.sock`).
- **Docker Daemon** (`dockerd`) — processo que gerencia images, containers, networks, volumes.
- **containerd** — runtime de container de alto nível. Gerencia ciclo de vida.
- **runc** — runtime de baixo nível. Cria containers invocando syscalls do kernel (namespaces, cgroups).
- **Registry** — armazenamento de imagens (Docker Hub, AWS ECR, GitHub Container Registry).

**Rootless Docker (2020+):** versão que roda sem privilégios root, mais seguro para ambientes multi-tenant.

### Conceitos core

- **Image** — blueprint read-only. Conjunto de layers.
- **Container** — instância em execução de uma imagem. Pode ser iniciada, parada, removida.
- **Layer** — mudança (camada) em um filesystem. Imagens são compostas de layers.
- **Dockerfile** — receita declarativa para construir imagens.
- **Volume** — persistência de dados fora do container.
- **Network** — comunicação entre containers.
- **Registry** — repositório de imagens.
- **Tag** — versão de uma imagem (`nginx:1.27-alpine`).

---

## Imagens e layers

Cada instrução do Dockerfile cria uma **layer**. Layers são imutáveis e deduplicadas entre imagens.

```
Imagem nginx:alpine
├── Layer 1: Alpine Linux base (5 MB)
├── Layer 2: nginx install (4 MB)
├── Layer 3: config files (few KB)
└── Layer 4: entrypoint (few KB)
```

**Benefícios:**

- **Cache de build** — se uma layer não muda, é reutilizada
- **Push/pull eficiente** — apenas layers novas são transferidas
- **Storage eficiente** — duas imagens que compartilham base layer ocupam espaço uma vez

### Anatomia de uma tag

```
registry.example.com/namespace/image:tag@sha256:abc123...
│                   │         │     │   │
│                   │         │     │   └── digest (imutável, recomendado em produção)
│                   │         │     └────── tag (mutável — pode apontar para outra image)
│                   │         └──────────── nome da imagem
│                   └────────────────────── namespace (user/org)
└────────────────────────────────────────── registry (default: docker.io)
```

**Exemplos:**

```bash
nginx                           # docker.io/library/nginx:latest
nginx:1.27-alpine               # versão específica
ghcr.io/myorg/myapp:1.0.0       # GitHub Container Registry
public.ecr.aws/amazoncorretto/amazoncorretto:21  # AWS ECR Public
```

### Tags vs Digests

**Tag** — mutável. `nginx:1.27` pode ser reatribuído.

**Digest** — imutável (hash SHA256 da imagem). **Use em produção** para garantir reprodutibilidade:

```bash
docker pull nginx@sha256:abc123...
```

---

## Dockerfile

### Estrutura básica

```dockerfile
# Base image
FROM node:22-alpine

# Metadata
LABEL maintainer="dev@medespecialista.com"
LABEL version="1.0.0"

# Working directory
WORKDIR /app

# Install dependencies (cached se package.json não mudar)
COPY package*.json ./
RUN npm ci --only=production

# Copy application
COPY . .

# Expose port (documentação — não publica)
EXPOSE 3000

# Default user (não root!)
USER node

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1

# Command
CMD ["node", "server.js"]
```

### Instruções principais

| Instrução | O que faz |
| --- | --- |
| `FROM` | Base image (obrigatório, primeira instrução útil) |
| `LABEL` | Metadata (key=value) |
| `WORKDIR` | Define diretório de trabalho (cria se não existe) |
| `COPY` | Copia arquivos do host para a imagem |
| `ADD` | Como COPY, mas também suporta URLs e tar. **Prefira COPY.** |
| `RUN` | Executa comando durante o build (cria nova layer) |
| `ENV` | Define variável de ambiente |
| `ARG` | Variável só durante build (`--build-arg`) |
| `EXPOSE` | Documenta porta (não publica — use `-p` no run) |
| `VOLUME` | Marca ponto de montagem |
| `USER` | Usuário para instruções seguintes |
| `ENTRYPOINT` | Comando principal (difícil de sobrescrever) |
| `CMD` | Argumentos para ENTRYPOINT, ou comando default |
| `HEALTHCHECK` | Comando para verificar saúde do container |
| `STOPSIGNAL` | Signal enviado ao container stop |
| `SHELL` | Muda o shell default |
| `ONBUILD` | Instrução executada em builds filhos (raro) |

### ENTRYPOINT vs CMD

**CMD** — comando default, **fácil** de sobrescrever:

```dockerfile
CMD ["node", "server.js"]
```

```bash
docker run myimage                 # node server.js
docker run myimage echo hello      # echo hello  (sobrescreveu)
```

**ENTRYPOINT** — comando fixo, **difícil** de sobrescrever:

```dockerfile
ENTRYPOINT ["node"]
CMD ["server.js"]
```

```bash
docker run myimage                      # node server.js
docker run myimage other.js             # node other.js
docker run --entrypoint echo myimage hi # echo hi
```

**Pattern comum:** ENTRYPOINT = binário, CMD = args default.

### Exec vs Shell form

```dockerfile
# Shell form — roda em /bin/sh -c "..."
CMD node server.js
# Problemas: signals não chegam ao processo (SIGTERM ignorado), shell extra

# Exec form — roda direto, sem shell
CMD ["node", "server.js"]
# Recomendado: signals funcionam, sem shell interpretation
```

**Regra:** **sempre use exec form** (`[]`). Signals (SIGTERM em graceful shutdown) dependem disso.

### Build

```bash
docker build -t myapp:1.0 .
docker build -t myapp:1.0 -f Dockerfile.prod .
docker build --no-cache -t myapp:1.0 .
docker build --build-arg VERSION=1.0 -t myapp .
docker build --platform linux/amd64,linux/arm64 -t myapp .  # multi-arch
```

### BuildKit

Novo engine de build (default no Docker 23+). Muito mais rápido, paralelismo, secrets mounts, cache avançado.

```bash
# Ativar (se não for default)
DOCKER_BUILDKIT=1 docker build .

# Buildx — extensão para multi-arch
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t myapp --push .
```

**Features do BuildKit:**

```dockerfile
# syntax=docker/dockerfile:1.6

# Secret mount — não vai para a imagem
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci

# Cache mount — cache persistente entre builds
RUN --mount=type=cache,target=/root/.npm npm ci

# SSH mount — para clonar repos privados
RUN --mount=type=ssh git clone git@github.com:private/repo.git
```

```bash
docker build --secret id=npmrc,src=$HOME/.npmrc -t myapp .
```

---

## Otimizando Dockerfiles

### Layer caching

Docker usa cache baseado em **instruções + conteúdo**. Se uma layer muda, todas as seguintes são reconstruídas.

**Regra:** ordem de mudança, da menos frequente para mais frequente:

```dockerfile
# RUIM — qualquer mudança em código invalida node_modules
FROM node:22-alpine
WORKDIR /app
COPY . .
RUN npm ci

# BOM — código muda sem reinstalar deps
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
```

### Multi-stage builds

Constrói a aplicação em um estágio e copia **apenas artifacts** para um estágio menor:

```dockerfile
# Stage 1: build
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: runtime
FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
RUN npm ci --only=production && npm cache clean --force
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

**Benefícios:**

- Imagem final **muito menor** (sem build tools, dev dependencies, source)
- Menos surface area para vulnerabilidades
- Deploy mais rápido

**Exemplo Java (Spring Boot):**

```dockerfile
# Stage 1: build com Maven
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY pom.xml .
COPY .mvn/ .mvn/
COPY mvnw .
RUN ./mvnw dependency:go-offline
COPY src/ src/
RUN ./mvnw package -DskipTests

# Stage 2: runtime só com JRE
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
USER nobody
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Exemplo Go:**

```dockerfile
FROM golang:1.23-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /bin/app ./cmd/server

# Runtime minimo — só o binário!
FROM scratch
COPY --from=builder /bin/app /app
EXPOSE 8080
ENTRYPOINT ["/app"]
```

Imagem final Go: **~10 MB** (só o binário!).

### Imagens mínimas

Escolha o base image certo:

| Base | Tamanho | Quando usar |
| --- | --- | --- |
| `scratch` | 0 bytes | Go, Rust (binários estáticos) |
| `distroless` | ~20 MB | Java, Python, Node — mais seguro que alpine |
| `alpine` | ~5 MB | Leve, mas musl libc pode ter pegadinhas |
| `slim` | ~50-100 MB | Debian mínimo, libc glibc |
| `:latest` / full | 100-500+ MB | Desenvolvimento, não produção |

**Recomendação 2026:** `distroless` é o padrão ouro para produção — sem shell, sem package manager, surface area mínima. Google maintém.

```dockerfile
FROM gcr.io/distroless/java21-debian12
COPY app.jar /app.jar
CMD ["/app.jar"]
```

### .dockerignore

Exclui arquivos do build context — acelera build e evita secrets:

```
# .dockerignore
node_modules
.git
.env
.env.local
*.log
.DS_Store
coverage/
.vscode/
.idea/
Dockerfile*
.dockerignore
```

**Importante:** sem `.dockerignore`, todo o diretório é enviado ao daemon, o que pode ser lento e vazar secrets.

---

## Running containers

### docker run — opções essenciais

```bash
# Básico
docker run nginx

# Nome, porta, detached, remove ao parar
docker run --name web -p 8080:80 -d --rm nginx

# Variáveis de ambiente
docker run -e NODE_ENV=production -e DATABASE_URL=... myapp

# Env from file
docker run --env-file .env myapp

# Volumes
docker run -v /host/path:/container/path myapp
docker run -v my-volume:/data myapp         # named volume
docker run -v $(pwd):/app myapp             # bind mount current dir

# Networks
docker run --network my-network myapp

# Restart policy
docker run --restart=unless-stopped myapp

# Resource limits
docker run --memory 512m --cpus 2 myapp

# Interactive shell
docker run -it alpine sh

# Run as user
docker run -u 1000:1000 myapp

# Read-only filesystem
docker run --read-only myapp

# Healthcheck override
docker run --health-cmd="curl -f http://localhost/health" --health-interval=30s myapp
```

### Comandos essenciais

```bash
# Containers
docker ps                    # rodando
docker ps -a                 # todos (incluindo parados)
docker start <id>
docker stop <id>
docker restart <id>
docker rm <id>
docker rm -f <id>            # força (para + remove)
docker kill <id>             # SIGKILL

# Logs
docker logs <id>
docker logs -f <id>          # follow
docker logs --tail 100 <id>
docker logs --since 10m <id>

# Exec (rodar comando em container)
docker exec -it <id> sh
docker exec -it <id> bash
docker exec <id> ls /app

# Stats e inspection
docker stats                 # CPU, RAM, IO live
docker inspect <id>          # JSON com tudo
docker top <id>              # processos
docker port <id>             # portas mapeadas

# Images
docker images
docker pull <image>
docker push <image>
docker rmi <image>
docker tag source:tag target:tag
docker history <image>        # layers
docker inspect <image>

# Cleanup
docker system prune           # remove tudo que não está em uso
docker system prune -a        # inclui imagens sem containers
docker volume prune
docker network prune
docker builder prune          # cache do build
```

### Graceful shutdown

Docker envia SIGTERM, depois SIGKILL (default após 10s).

```bash
docker stop --time=30 <id>   # espera 30s antes do KILL
```

No seu app, capture SIGTERM:

```javascript
// Node
process.on('SIGTERM', async () => {
    console.log('graceful shutdown');
    await server.close();
    process.exit(0);
});
```

Java: `@PreDestroy` ou `SpringApplication` lifecycle. Ver [[Spring Boot]].

### Healthchecks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1
```

**Parâmetros:**

- `interval` — frequência (default 30s)
- `timeout` — máximo de tempo por check
- `start-period` — grace period no startup
- `retries` — fails consecutivos antes de marcar unhealthy

**Estados:** `starting`, `healthy`, `unhealthy`. Orquestradores (K8s, Docker Swarm) usam para decisões.

---

## Volumes e persistência

Containers são **efêmeros** — ao remover, filesystem se vai. Para persistir dados, use volumes ou bind mounts.

### Bind mount

Monta diretório do host no container.

```bash
docker run -v /data:/app/data myapp
docker run -v $(pwd)/src:/app/src myapp   # dev: live reload
docker run -v $(pwd):/app:ro myapp         # read-only
```

**Uso típico:**

- Desenvolvimento (live reload)
- Configs do host
- Dados que você quer acessar diretamente

### Named volumes

Gerenciados pelo Docker, armazenados em `/var/lib/docker/volumes/`.

```bash
docker volume create my-data
docker run -v my-data:/app/data myapp

# Listar
docker volume ls
docker volume inspect my-data
docker volume rm my-data
```

**Uso típico:**

- Dados de banco (Postgres, MySQL, MongoDB)
- Uploads de usuário
- Caches persistentes

**Bind mount vs Volume:**

| | Bind mount | Volume |
| --- | --- | --- |
| Performance | Depende do host | Otimizado pelo Docker |
| Portabilidade | ❌ path do host | ✅ nome abstrato |
| Backup | Manual | `docker volume` commands |
| Driver | Local apenas | Suporta plugins (NFS, Ceph, ...) |
| Uso recomendado | Dev, configs | Produção, dados persistentes |

### tmpfs

Em memória, perdido ao parar:

```bash
docker run --tmpfs /tmp myapp
```

**Uso:** dados sensíveis que não devem tocar o disco.

---

## Networks

Containers podem se comunicar via networks gerenciadas pelo Docker.

### Tipos de network

- **bridge** (default) — rede virtual privada. Containers na mesma bridge se comunicam por nome.
- **host** — container usa a network stack do host (sem isolamento).
- **none** — sem rede.
- **overlay** — multi-host (Docker Swarm, raro sem Swarm).
- **macvlan** — container tem MAC próprio, aparece como device físico na LAN.

### Bridge network — o default

```bash
# Criar custom bridge (recomendado vs default bridge)
docker network create my-network

# Rodar containers nela
docker run --network my-network --name db postgres
docker run --network my-network --name app myapp

# Agora 'app' pode conectar em 'db:5432' por nome
```

**Por que custom bridge é melhor que default bridge:**

- **DNS interno** — containers resolvem uns aos outros pelo nome
- **Isolamento** — containers em bridges diferentes não se veem
- **Melhor gerenciamento** — você controla quem está onde

### Port publishing

```bash
# -p host:container
docker run -p 8080:80 nginx            # host 8080 → container 80
docker run -p 127.0.0.1:8080:80 nginx  # só localhost
docker run -P nginx                    # publica todas as EXPOSE em portas random
```

---

## Docker Compose

Orquestração multi-container declarativa. Ideal para dev environments e projetos pequenos.

### compose.yaml (nome novo — antes: docker-compose.yml)

```yaml
# compose.yaml
services:
    app:
        build:
            context: .
            dockerfile: Dockerfile
        ports:
            - "3000:3000"
        environment:
            - NODE_ENV=production
            - DATABASE_URL=postgres://user:pass@db:5432/app
        depends_on:
            db:
                condition: service_healthy
        volumes:
            - ./logs:/app/logs
        restart: unless-stopped
        healthcheck:
            test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
            interval: 30s
            timeout: 10s
            retries: 3

    db:
        image: postgres:16-alpine
        environment:
            POSTGRES_USER: user
            POSTGRES_PASSWORD: pass
            POSTGRES_DB: app
        volumes:
            - pg-data:/var/lib/postgresql/data
        healthcheck:
            test: ["CMD-SHELL", "pg_isready -U user"]
            interval: 5s
            timeout: 5s
            retries: 5

    redis:
        image: redis:7-alpine
        volumes:
            - redis-data:/data
        command: redis-server --appendonly yes

    nginx:
        image: nginx:1.27-alpine
        ports:
            - "80:80"
            - "443:443"
        volumes:
            - ./nginx.conf:/etc/nginx/nginx.conf:ro
            - ./certs:/etc/nginx/certs:ro
        depends_on:
            - app

volumes:
    pg-data:
    redis-data:
```

### Comandos Compose

```bash
docker compose up                 # inicia todos
docker compose up -d              # detached
docker compose up --build         # rebuild images
docker compose down               # para e remove
docker compose down -v            # + remove volumes
docker compose ps                 # lista services
docker compose logs -f            # logs de todos
docker compose logs -f app        # logs de um
docker compose exec app sh        # shell em um service
docker compose restart app
docker compose build app
docker compose pull               # atualiza imagens
docker compose config             # valida e mostra config final
```

### Compose multi-file (dev vs prod)

```bash
# compose.yaml       — base
# compose.dev.yaml   — overrides para dev
# compose.prod.yaml  — overrides para prod

docker compose -f compose.yaml -f compose.dev.yaml up
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

**Dev overrides:**

```yaml
# compose.dev.yaml
services:
    app:
        build:
            target: dev  # target de multi-stage
        volumes:
            - .:/app     # live reload
        command: npm run dev
```

### Profiles

```yaml
services:
    tests:
        profiles: [test]
        image: myapp-tests
```

```bash
docker compose --profile test up  # ativa profile 'test'
```

---

## Docker em desenvolvimento

### Dev containers

Padrão da Microsoft/VS Code para ambientes reprodutíveis:

```json
// .devcontainer/devcontainer.json
{
    "name": "Node.js",
    "image": "mcr.microsoft.com/devcontainers/javascript-node:22",
    "features": {
        "ghcr.io/devcontainers/features/docker-in-docker:2": {}
    },
    "forwardPorts": [3000],
    "postCreateCommand": "npm install"
}
```

Dev inteiro roda em container — não poluí o host.

### Testcontainers — testes de integração

Usa Docker para spin up serviços reais em testes (PostgreSQL, Kafka, Redis, ...).

```typescript
import { PostgreSqlContainer } from '@testcontainers/postgresql';

let container;

beforeAll(async () => {
    container = await new PostgreSqlContainer('postgres:16').start();
});

afterAll(async () => {
    await container.stop();
});
```

Ver [[Testes em Java]] e [[Testes em JavaScript]] para deep dive.

---

## Segurança

### Regras de ouro

1. **Nunca rode como root** no container
2. **Use imagens oficiais ou verified**
3. **Use pin de versão** (evite `:latest`)
4. **Use digests em produção** (`image@sha256:...`)
5. **Mínimo privilégio** — `--read-only`, `--cap-drop=ALL`
6. **Scan vulnerabilities** regularmente
7. **Nunca embeda secrets no Dockerfile**
8. **Use `.dockerignore`** para não vazar arquivos locais

### Non-root user

```dockerfile
FROM node:22-alpine

# Cria user não-root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeapp -u 1001 -G nodejs

WORKDIR /app
COPY --chown=nodeapp:nodejs . .

USER nodeapp

CMD ["node", "server.js"]
```

Ou use o user built-in em imagens oficiais: `USER node` (Node image), `USER nobody` (JRE), etc.

### Secrets — nunca no Dockerfile

**RUIM:**

```dockerfile
ENV API_KEY=secret123    # Fica na imagem, visível a quem puxar!
```

**BOM — runtime:**

```bash
docker run -e API_KEY=$API_KEY myapp
docker run --env-file .env myapp
```

**BuildKit secrets (build time):**

```dockerfile
# syntax=docker/dockerfile:1.6
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
```

```bash
docker build --secret id=mysecret,src=./secret.txt .
```

**Em produção:** use **Docker secrets** (Swarm), **Kubernetes secrets**, **Vault**, **AWS Secrets Manager**.

### Capabilities

Containers rodam com capabilities do Linux. Drop as desnecessárias:

```bash
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx
```

### Read-only filesystem

```bash
docker run --read-only --tmpfs /tmp myapp
```

Container não pode escrever exceto em `/tmp` (tmpfs). Previne malware persistence.

### Security scanning

```bash
# Docker Scout (built-in, 2023+)
docker scout cves myapp:1.0

# Trivy — open source, muito popular
trivy image myapp:1.0

# Snyk
snyk container test myapp:1.0
```

**Em CI:** rode scan em cada PR, falhe em vulnerabilidades críticas.

### Supply chain

**Ameaças:**

- **Typosquatting** — `nginx` vs `nignx`
- **Image takeover** — maintainer malicioso publica versão comprometida
- **Base image vulnerabilities** — OS desatualizado

**Defesas:**

- **Usar imagens oficiais ou verified publishers**
- **Imagens assinadas** (Cosign, Notary)
- **SBOM** (Software Bill of Materials)
- **Registry privado** com scanning

---

## Registry

### Docker Hub

Default. Grátis para público, pago para privado + limits de pull.

```bash
docker login
docker push username/myapp:1.0
docker pull username/myapp:1.0
```

### Alternativas

- **GitHub Container Registry (GHCR)** — grátis, integra com GitHub Actions
- **AWS ECR** — pago, integra com AWS
- **Google Artifact Registry**
- **Azure Container Registry**
- **Harbor** — self-hosted, open source
- **Quay.io** — Red Hat

### GitHub Actions + GHCR

```yaml
name: Build and push

on:
    push:
        branches: [main]

jobs:
    build:
        runs-on: ubuntu-latest
        permissions:
            contents: read
            packages: write
        steps:
            - uses: actions/checkout@v4
            - uses: docker/login-action@v3
              with:
                  registry: ghcr.io
                  username: ${{ github.actor }}
                  password: ${{ secrets.GITHUB_TOKEN }}
            - uses: docker/setup-buildx-action@v3
            - uses: docker/build-push-action@v5
              with:
                  context: .
                  push: true
                  tags: |
                      ghcr.io/${{ github.repository }}:latest
                      ghcr.io/${{ github.repository }}:${{ github.sha }}
                  cache-from: type=gha
                  cache-to: type=gha,mode=max
```

---

## Troubleshooting

### Container não inicia

```bash
docker logs <id>
docker inspect <id>
docker run -it --entrypoint sh myimage  # shell na imagem para debug
```

### Container morre logo após iniciar

```bash
docker ps -a  # ver exit code
docker logs <id>
```

**Causas comuns:**

- Processo principal sai (comando errado, permissões, arquivo não existe)
- OOM (out of memory) killed
- Bug na aplicação
- Signal não tratado

### Out of memory

```bash
docker stats                  # live usage
docker inspect <id> | grep -i memory
```

**Fix:** `--memory` limits, reduzir uso, investigar leaks.

### Slow build

- Use `.dockerignore`
- Ordene layers por frequência de mudança
- Use cache mounts (BuildKit)
- Multi-stage build
- Pin de versão (evita checar updates)

### Disk cheio

```bash
docker system df              # ver uso
docker system prune -a --volumes  # cleanup agressivo
```

### Network issue entre containers

```bash
docker network ls
docker network inspect my-network
docker exec -it app ping db
```

---

## Patterns de produção

### 1. Immutable images

Não mude containers rodando. Rebuild + redeploy. Garante reprodutibilidade.

### 2. Sidecar pattern

Container auxiliar no mesmo pod/host:

```yaml
services:
    app:
        image: myapp
    log-shipper:
        image: fluent/fluent-bit
        volumes:
            - log-data:/var/log
```

### 3. Init container / depends_on

Espera dependências antes de iniciar:

```yaml
app:
    depends_on:
        db:
            condition: service_healthy
```

### 4. Configuration via env

12-factor app — config via env vars, não arquivos hardcoded.

### 5. Stateless containers

Containers não devem ter estado local. Dados em volumes, sessões em Redis, arquivos em S3.

### 6. Log to stdout/stderr

Não escreva logs em arquivo dentro do container. Escreva em stdout — Docker/K8s coletam.

```javascript
// BOM
console.log(JSON.stringify({ level: 'info', msg: 'user logged in' }));

// RUIM
fs.appendFile('/var/log/app.log', ...);
```

### 7. Single process per container

Evite supervisor/systemd dentro do container. Um container = um processo principal.

**Exceção:** init scripts que fazem setup mínimo antes de `exec` no processo principal.

---

## Armadilhas comuns

- **`COPY . .` sem `.dockerignore`** — lento, vaza secrets, invalida cache
- **`FROM :latest`** — reproducibilidade destruída
- **Root user** — security risk
- **Secrets em ENV/ARG** — visíveis em `docker inspect`
- **`ADD` em vez de `COPY`** — confuso com URLs e tar
- **Shell form em CMD/ENTRYPOINT** — signals não funcionam
- **Instalar build tools em runtime image** — imagem gigante
- **Ignorar `.dockerignore`** — node_modules no build context
- **Apt-get install sem `--no-install-recommends`** — pacotes desnecessários
- **Dois comandos em dois RUNs vs um RUN encadeado** — mais layers, maior cache
- **Instalar pacotes sem cleanup** — `apt clean` necessário
- **Volume anônimo por engano** — `VOLUME` no Dockerfile causa problemas inesperados
- **`depends_on` sem `condition: service_healthy`** — só espera start, não ready
- **Ports publicados em interface externa** — `0.0.0.0` vs `127.0.0.1`
- **Container rodando como PID 1 sem init handler** — zombie processes
- **`docker exec` em produção como debugging permanente** — não escalável
- **Volumes tornados persistentes mas não versionados** — dados órfãos
- **Multi-stage sem nomear stages** — difícil manter
- **Rebuild sempre em vez de usar cache** — lento
- **Host volumes com permissões erradas** — UID mismatch entre host e container
- **Usar `latest` como cache source** — cache miss garantido

---

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

- [[Kubernetes]] — orquestração em escala
- [[Linux]] — foundation dos containers
- [[Nginx]] — reverse proxy comum em containers
- [[CI-CD]] — build e deploy automatizados
- [[WSL, Docker e Kubernetes]] — setup em Windows
- [[Comandos Docker e WSL]] — quick reference
- [[Testes em Java]] — Testcontainers
- [[Testes em JavaScript]] — Testcontainers para JS
- [[System Design]] — containers em architecture
- [[Spring Boot]] — Dockerfile para Java
- [[Node.js]] — Dockerfile para Node
