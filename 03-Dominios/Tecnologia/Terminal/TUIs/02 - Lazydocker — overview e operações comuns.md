---
title: "Lazydocker — overview e operações comuns"
created: 2026-05-21
updated: 2026-05-21
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - tuis
  - lazydocker
  - iniciado
  - docker
aliases:
  - Lazydocker overview
---

# Lazydocker — overview e operações comuns

> [!abstract] TL;DR
> Lazydocker é uma TUI Docker em Go por Jesse Duffield (mesmo autor de Lazygit). Painéis: Project (top-left), Services/Containers, Images, Volumes, Networks (left); Logs/Config/Stats (right). `s` stop, `r` restart, `E` exec shell, `m` logs full screen, `p` pause. Vence pra dev local com docker-compose — dashboard ao vivo de CPU/mem por container. Substitui `docker ps`/`docker logs -f` pra workflow interativo.

## O que é / Como funciona

### Quem é Lazydocker

**Lazydocker** é uma TUI para Docker criada por Jesse Duffield (o mesmo autor do Lazygit). Escrita em Go, distribui como single binary sem dependências extras.

- **Linguagem:** Go — single binary, sem runtime externo
- **Estilo:** painéis com keybindings contextuais (não modal; cada painel tem seus próprios atalhos, visíveis via `?`)
- **Foco:** dev local — monitorar e operar containers, visualizar logs em tempo real, exec shell pra debug
- **Não substitui:** `docker` CLI pra scripts e CI/CD; portainer pra gestão multi-host ou equipes não-dev

### Layout dos painéis

Lazydocker divide a tela em duas grandes regiões: esquerda (lista de recursos) e direita (conteúdo contextual). O painel Project fica no topo da coluna esquerda, exibindo o estado do docker-compose se detectado no cwd. Abaixo, os painéis de lista são acessados pelas teclas `1`–`6`.

```text
┌─Project──────────────────────────────────────┐
│ docker-compose status (se detectado)          │
├─Services/Containers────┬─Logs / Config / Stats┤
│ ▶ api                  │                      │
│ ▶ db                   │  <output do painel   │
│ ▶ cache                │   e tab ativos>      │
├─Images─────────────────┤                      │
│ alpine:3.19            │                      │
│ postgres:16            │                      │
├─Volumes────────────────┤                      │
│ vol-data               │                      │
├─Networks───────────────┤                      │
│ bridge                 │                      │
│ myproj_net             │                      │
└────────────────────────┴──────────────────────┘
```

Navegação entre painéis: teclas `1`–`6` (Project=`1`, Services=`2`, Containers=`3`, Images=`4`, Volumes=`5`, Networks=`6`). Dentro de cada painel, `]`/`[` trocam as abas (Logs, Config, Stats, Top). `enter` foca o painel principal direito.

Quando um `docker-compose.yml` (ou `compose.yaml`) está presente no cwd, Lazydocker auto-detecta e exibe os containers agrupados como **services** no painel Services. Sem compose, todos os containers do daemon aparecem no painel Containers.

### Operações por painel — cheatsheet

| Painel | Tecla | Ação |
|---|---|---|
| Services | `u` | Up service |
| Services | `S` | Start service |
| Services | `s` | Stop service |
| Services | `p` | Pause service |
| Services | `r` | Restart service |
| Services | `d` | Remove containers do service |
| Services | `U` | Up project inteiro |
| Services | `D` | Down project inteiro |
| Services | `E` | Exec shell no container do service |
| Services | `a` | Attach ao container |
| Services | `m` | View logs |
| Services | `b` | View bulk commands |
| Containers | `s` | Stop container |
| Containers | `p` | Pause container |
| Containers | `r` | Restart container |
| Containers | `d` | Remove container (com confirm) |
| Containers | `E` | Exec shell (`/bin/sh`) |
| Containers | `a` | Attach ao container |
| Containers | `m` | View logs |
| Containers | `w` | Abrir no browser (primeira porta HTTP) |
| Images | `d` | Remove image |
| Images | `c` | Run predefined custom command |
| Volumes | `d` | Remove volume |
| Networks | `d` | Remove network |
| Global | `1`–`6` | Focar painel (Project, Services, Containers, Images, Volumes, Networks) |
| Global | `]` / `[` | Próxima / anterior aba no painel ativo |
| Global | `+` / `_` | Próximo / anterior screen mode (normal/half/fullscreen) |
| Global | `?` | Help contextual |
| Global | `q` | Quit |

> [!note] Sobre `e` vs `E`
> No painel **Project**, `e` abre o config do Lazydocker para edição; `o` abre o config já existente. No painel **Services** e **Containers**, a tecla de exec shell é `E` (maiúsculo). Não confundir.

### Dashboard ao vivo

A aba **Stats** de qualquer container exibe CPU, memória e network I/O em tempo real (refresh ~1s). Útil para:

- Detectar memory leak progressivo num serviço
- Identificar container com CPU runaway em idle
- Comparar consumo de recursos entre services do compose

A aba **Top** mostra os processos rodando dentro do container (equivale a `docker top <container>`).

### Quando Lazydocker ganha

- **Dev local com docker-compose stack:** dashboard consolidado sem precisar de múltiplos terminais com `docker logs -f`
- **Tail multi-container logs simultaneamente:** navega entre services com `j`/`k` e vê logs ao vivo no painel direito
- **Debug de crash loop:** restart count visível na lista; logs do crash acessíveis em dois keypresses
- **One-off shell pra inspect:** `E` no container/service abre shell imediatamente, sem digitar o hash do container
- **Visualizar CPU/mem de cada service:** aba Stats sem precisar de `docker stats` separado

### Quando `docker` CLI ainda ganha

- Scripts CI/CD e automações — Lazydocker é interativo, não compositável
- `docker build` com args complexos e multi-stage
- `docker network create` / `docker volume create` com flags específicas
- Contextos sem TTY (SSH sem `-t`, cron, pipelines)

### Quando portainer/portainer-like ainda ganha

- **Multi-host / cluster:** Lazydocker gerencia apenas o daemon local
- **Equipes não-dev:** UI gráfica com mouse, sem curva de terminal
- **Gestão de Swarm ou Kubernetes:** Lazydocker não suporta orquestração distribuída

---

## Na prática

### Instalação rápida

```bash
# Homebrew (macOS e Linux)
brew install jesseduffield/lazydocker/lazydocker

# Script de instalação binário (Linux/macOS)
curl https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash

# Go install (requer Go ≥1.19)
go install github.com/jesseduffield/lazydocker@latest

# Arch Linux AUR
yay -S lazydocker

# Docker (sem instalar na máquina)
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock lazyteam/lazydocker
```

(Referência: Lazydocker 0.24+; keybindings podem variar em versões mais antigas.)

### Primeira execução

```bash
cd ~/repos/myproj
lazydocker
```

Auto-detecta `docker-compose.yml` (ou `compose.yaml`) no cwd. Sem arquivo compose, exibe todos os containers do daemon no painel Containers. Para sair: `q`.

### Workflow comum (dev local)

1. `lazydocker` no diretório do projeto com compose
2. `j`/`k` navega entre services no painel Services
3. `enter` em um service → aba Logs (live tail) no painel direito
4. `]`/`[` troca entre abas Logs / Config / Stats / Top
5. `E` abre shell no container pra inspecionar filesystem, env vars ou testar queries
6. Em outra pane do Zellij/tmux, editar código; `r` no Lazydocker pra restartar o service
7. Aba Stats pra confirmar que memória voltou ao normal após fix

---

## Armadilhas

**1. `d` em Containers remove o container — confunde com stop**

- **Causa:** `d` é "Remove" (equivale a `docker rm`), não stop. Pra parar sem remover, use `s`.
- **Sintoma:** container some da lista; ao subir novamente, começa do zero (sem estado efêmero do container).
- **Como detectar:** `docker ps -a` não exibe mais o container; Lazydocker mostra lista menor.
- **Solução:** usar `s` (stop) pra pausar sem destruir; ler o prompt de confirmação antes de pressionar `enter` em operações com `d`.

**2. `r` (restart) vs `R` (restart options) — não há `R` que remove com volumes**

- **Causa:** em **Services**, a tecla `R` abre "View restart options" (não remove volumes). Porém, `D` (maiúsculo) faz `docker compose down` — que por padrão não remove volumes nomeados, mas remove containers e networks.
- **Sintoma:** ao usar `D`, containers sobem do zero na próxima vez; volumes nomeados sobrevivem (mas volumes anônimos não).
- **Como detectar:** `docker volume ls` mostra volumes nomeados ainda presentes após `D`.
- **Solução:** entender que `docker compose down` não remove volumes nomeados por padrão; pra remover volumes também, é necessário a flag `--volumes` via CLI, não via Lazydocker.

**3. Lazydocker fora do diretório do compose — sem agrupamento por service**

- **Causa:** a auto-detecção do `docker-compose.yml` usa o cwd ao abrir o Lazydocker.
- **Sintoma:** painel Services vazio ou ausente; containers aparecem soltos no painel Containers sem agrupamento.
- **Como detectar:** painel Project não exibe service tree; todos containers visíveis como containers individuais.
- **Solução:** `cd <dir-com-compose>` antes de iniciar `lazydocker`; ou configurar o path explicitamente no config YAML (nota 05).

**4. Logs muito longos travam a navegação**

- **Causa:** container chatty (muitos logs por segundo) sobrecarrega a renderização da aba Logs.
- **Sintoma:** scroll travado, UI não responsiva, delay nos keypresses.
- **Como detectar:** UX visivelmente lenta ao selecionar container com alto volume de logs.
- **Solução:** usar `m` pra entrar em fullscreen da log view com melhor performance; configurar `logs.tail` no config para limitar quantidade de linhas carregadas (nota 05).

**5. Exec (`E`) em Alpine sem `/bin/bash`**

- **Causa:** `E` executa `/bin/sh` por padrão; Alpine Linux não inclui bash — apenas busybox sh.
- **Sintoma:** se customizado pra `/bin/bash`, recebe "not found"; com `/bin/sh` funciona, mas sem features do bash.
- **Como detectar:** testar `E` numa imagem Alpine; observar qual shell é aberto.
- **Solução:** Alpine tem `/bin/sh` funcional via busybox; pra bash completo, instalar `bash` na imagem ou usar `customCommands` no config pra executar comandos específicos (nota 05).

**6. `e` no painel Project edita o config do Lazydocker, não arquivos do projeto**

- **Causa:** no painel Project (tecla `1`), `e` abre o `config.yml` do Lazydocker no editor configurado — não arquivos do docker-compose.
- **Sintoma:** surpresa ao ver o config YAML do Lazydocker abrir no editor.
- **Como detectar:** observer qual arquivo o editor abre.
- **Solução:** usar `o` pra abrir (visualizar) o config; saber que `e` é exclusivamente pra editar o config do Lazydocker.

---

## Em inglês

- **container** — *container*. "instância isolada de uma imagem Docker rodando como processo no host."
- **image** — *image*. "snapshot imutável do filesystem e configuração usado pra criar containers."
- **volume** — *volume*. "armazenamento persistente gerenciado pelo Docker; sobrevive à remoção do container."
- **network** — *network*. "rede virtual Docker que conecta containers entre si e com o host."
- **log** — *log*. "saída de stdout/stderr de um container; acessada via `docker logs` ou aba Logs no Lazydocker."
- **exec** — *exec*. "executar processo dentro de container já rodando; `docker exec -it <id> /bin/sh`."
- **dashboard** — *dashboard*. "visão consolidada de múltiplos recursos em tempo real; o painel principal do Lazydocker."
- **health check** — *health check*. "teste periódico configurado na imagem ou compose pra verificar se o container está saudável."
- **restart** — *restart*. "reiniciar container sem removê-lo; preserva estado efêmero do container (mas não persiste entre `docker rm`)."
- **docker-compose** — *docker compose*. "orquestrador multi-container; define services, volumes e networks em `compose.yaml`; `docker compose up/down`."

---

## Veja também

- [[01 - Lazygit — overview e operações essenciais]] — TUI irmã pra git
- [[05 - Lazydocker — config, customização e workflow]] — `~/.config/lazydocker/config.yml`
- [[07 - Lazydocker — debugging avançado e docker-compose]] — Magus
- [[03-Dominios/Tecnologia/Terminal/TUIs/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Lazydocker|lazydocker]], [[Dicionário do Terminal#Docker-compose|docker-compose]], [[Dicionário do Terminal#Exec (Lazydocker)|exec]]

---

## Referências

- Lazydocker — repositório oficial: https://github.com/jesseduffield/lazydocker
- Keybindings oficiais: https://github.com/jesseduffield/lazydocker/blob/master/docs/keybindings/Keybindings_en.md
