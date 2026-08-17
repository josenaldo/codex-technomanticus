---
title: "Linux"
created: 2026-04-01
updated: 2026-08-16
type: concept
progress: done
status: evergreen
tags:
  - infraestrutura
  - entrevista
publish: false
---

# Linux

> [!info] Tronco podado — o conteúdo virou galho atômico
> Esta nota era um monólito de 1118 linhas sobre Linux. Em **2026-08-16** o assunto virou o galho [[03-Dominios/Tecnologia/Infraestrutura/Linux/index|Infraestrutura/Linux]], com 16 notas em 3 fases e a lente *o sistema como o processo o vê* — o quarto e último galho do domínio, depois de Docker, Kubernetes e Nginx.
>
> Nada foi perdido: cada seção foi absorvida e desenvolvida. O mapa está abaixo, e as seções de relato pessoal e de inglês seguem preservadas aqui, ao fim da nota.

## Para onde foi cada seção

| O que havia aqui | Onde está agora |
|---|---|
| O que é, e por que Linux importa | [[03-Dominios/Tecnologia/Infraestrutura/Linux/01 - O que o Linux entrega a um processo\|01 — O contrato de execução]] |
| Filesystem hierarchy | [[03-Dominios/Tecnologia/Infraestrutura/Linux/02 - A hierarquia do sistema de arquivos\|02 — A hierarquia]], que acrescenta `/proc` e `/sys` como sistemas de arquivos sintéticos |
| Shell básico, variáveis, redirecionamento | [[03-Dominios/Tecnologia/Infraestrutura/Linux/03 - Tudo é arquivo - descritores e redirecionamento\|03 — Descritores e redirecionamento]] · a ergonomia do shell fica em [[03-Dominios/Tecnologia/Terminal/index\|Terminal]] |
| Permissões, users e groups | [[03-Dominios/Tecnologia/Infraestrutura/Linux/04 - Identidade - usuários, grupos e permissão\|04 — Identidade e permissão]] |
| Processos e jobs, sinais, foreground/background | [[03-Dominios/Tecnologia/Infraestrutura/Linux/05 - O processo como objeto administrável\|05 — O processo como objeto administrável]] |
| Systemd: serviços e criação de unidade | [[03-Dominios/Tecnologia/Infraestrutura/Linux/06 - systemd - o modelo de unidades\|06 — O modelo de unidades]] · [[03-Dominios/Tecnologia/Infraestrutura/Linux/07 - Escrever um serviço que se comporta\|07 — Escrever um serviço]] |
| journalctl | [[03-Dominios/Tecnologia/Infraestrutura/Linux/08 - Logs - journald e o que veio antes\|08 — journald]] |
| Timers e cron | [[03-Dominios/Tecnologia/Infraestrutura/Linux/09 - Agendamento - cron e timers\|09 — Agendamento]] |
| Networking, SSH, firewall, network namespaces | [[03-Dominios/Tecnologia/Infraestrutura/Linux/10 - A máquina na rede\|10 — A máquina na rede]] · o protocolo em [[03-Dominios/Ciência/Redes e Protocolos/index\|Ciência/Redes]] |
| Package management (APT, DNF, Pacman, APK, Snap/Flatpak) | [[03-Dominios/Tecnologia/Infraestrutura/Linux/11 - Software instalado\|11 — Software instalado]] |
| Monitoring e o checklist "o servidor está lento" | [[03-Dominios/Tecnologia/Infraestrutura/Linux/12 - Diagnóstico - os primeiros sessenta segundos\|12 — Os primeiros sessenta segundos]] · [[03-Dominios/Tecnologia/Infraestrutura/Linux/13 - CPU, memória, disco e I-O, um de cada vez\|13 — Os quatro eixos]] |
| strace, lsof, dmesg, perf | [[03-Dominios/Tecnologia/Infraestrutura/Linux/15 - Ver o que o processo pede ao kernel\|15 — O que o processo pede ao kernel]] |
| Checklist de 60 segundos de Brendan Gregg | desenvolvido na [[03-Dominios/Tecnologia/Infraestrutura/Linux/12 - Diagnóstico - os primeiros sessenta segundos\|nota 12]], com o método USE |

> [!note] O que **não** migrou, e por quê
> As duas seções abaixo são **material de entrevista** — relato pessoal e articulação em inglês. O galho novo não incorpora experiência pessoal do autor, então elas ficam preservadas aqui. Mesmo tratamento dado a `Docker.md`, `Kubernetes.md` e `Nginx.md`.

## Na prática (da minha experiência)

> **Linux é meu ambiente principal de trabalho há 15+ anos.** WSL2 hoje, Ubuntu em servidores, Alpine em containers. Entender Linux profundamente distingue um senior de alguém que só "usa bash".
>
> **Patterns que uso todo dia:**
>
> **1. `set -euo pipefail` em todo script.** Sem isso, bugs silenciosos são garantidos.
>
> **2. `ripgrep` e `fd` em vez de `grep -r` e `find`.** 10x mais rápido, melhor UX.
>
> **3. `htop` / `btop` em vez de `top`.** Visual superior.
>
> **4. `journalctl` em vez de `tail /var/log/...`.** Systemd centralizou logs — use.
>
> **5. SSH config (`~/.ssh/config`).** Aliases para todos os servidores, key automaticamente, ProxyJump para bastion.
>
> **6. `tmux` em servidores remotos.** Sessão sobrevive a desconexão.
>
> **7. `dotfiles` versionados.** `.bashrc`, `.tmux.conf`, `.vimrc`, `.gitconfig` tudo no git. Máquina nova? `./install.sh`.
>
> **8. `fzf`** — fuzzy finder. Ctrl+R para histórico de comandos, `fzf` para arquivos. Produtividade enorme.
>
> **Incidente memorável — disk cheio:**
>
> Servidor de produção parou de responder. `df -h` mostrou `/var/log` a 100%. Causa: log de nginx não estava sendo rotacionado porque `logrotate` estava quebrado. Remediação imediata: `truncate -s 0 /var/log/nginx/access.log` (não delete o arquivo — nginx ainda tem FD aberto). Fix definitivo: consertar logrotate.
>
> **Outro — processo zumbi consumindo memory:**
>
> App Java tinha leak, consumia 2GB a cada 6 horas. `ps aux --sort=-%mem` identificou. OOM killer matava, systemd reiniciava. Fix imediato: MemoryMax no unit file + alarme. Fix real: debug do leak no código (heap dump via jmap, análise em VisualVM).
>
> **Outro — SSH travava após key-based auth:**
>
> Login via chave levava 30 segundos. Causa: `UseDNS yes` em `/etc/ssh/sshd_config` — SSH tentava reverse DNS do cliente que não existia. Fix: `UseDNS no`. Login instantâneo.
>
> **A lição principal:** Linux é enorme, mas 20 comandos resolvem 80% dos problemas. Dominar `grep`, `awk`, `find`, `ssh`, `systemctl`, `journalctl`, `ps`, `top`, `netstat`/`ss`, `lsof`, `tcpdump`, `curl`, e scripting bash básico é o que faz você produtivo. Para o resto, Google + man pages existem.

---

## How to explain in English

> "Linux has been my primary development and production environment for over 15 years. Understanding Linux deeply — not just using commands from memory — is what separates a senior from someone who just 'knows bash'.
>
> For day-to-day work, my essentials are the GNU coreutils plus modern replacements. I use `ripgrep` instead of `grep -r` because it's orders of magnitude faster, `fd` instead of `find`, `htop` or `btop` instead of `top`. For text processing, grep, sed, awk, and jq are always there — the combination can solve almost any data transformation in a pipeline.
>
> I script in bash with `set -euo pipefail` as the first line — fail fast, no silent errors. For scheduled tasks, I prefer systemd timers over cron because systemd centralizes logging via journalctl and handles dependencies properly.
>
> For server debugging, I follow Brendan Gregg's 60-second checklist: `uptime` for load, `vmstat` and `mpstat` for CPU and memory, `iostat` for disk I/O, `sar` for network, and `top` or `htop` for processes. If something's wrong, one of those usually shows where. For deeper investigation, `strace` for syscalls, `lsof` for open files and ports, `tcpdump` for packets, and `journalctl` for systemd logs.
>
> For SSH, I use key-based authentication with Ed25519 keys, disable password auth on servers, and keep a detailed `~/.ssh/config` with aliases and ProxyJump for bastion hosts. For remote sessions, `tmux` keeps my work persistent across disconnects.
>
> Understanding Linux primitives — namespaces, cgroups, systemd units, filesystems — makes containers and Kubernetes far less magical. When I see a Dockerfile or a Kubernetes Pod, I understand what's actually happening at the kernel level: PID and network namespaces, cgroup limits, overlay filesystems, and capabilities. That foundation pays off when things break."

### Frases úteis em entrevista

- "`set -euo pipefail` as the first line of any bash script."
- "ripgrep and fd replace grep and find for everything."
- "systemd for services, journalctl for logs, systemctl for control."
- "Brendan Gregg's 60-second performance checklist catches most issues."
- "strace for syscalls, lsof for open files, tcpdump for packets."
- "SSH keys Ed25519, disable password auth, ssh config with ProxyJump."
- "Containers are namespaces plus cgroups plus overlayfs — nothing magical."
- "Prefer `tmux` over `nohup` for long-running sessions."
- "`chmod 777` is an answer, never the answer."
- "pkill and pgrep by pattern beat `ps aux | grep`."

### Key vocabulary

- núcleo → kernel
- camada do usuário → userspace
- distribuição → distribution / distro
- interpretador de comandos → shell
- encadeamento → pipe
- redirecionamento → redirection
- processo → process
- thread → thread
- sinal → signal
- proprietário → owner
- permissão → permission
- propriedade → ownership
- privilégio → privilege
- primeiro plano → foreground
- segundo plano → background
- montagem → mount
- ponto de montagem → mount point
- sistema de arquivos → filesystem
- ligação → link (symbolic / hard)
- espaço de nomes → namespace
- grupo de controle → cgroup
- variável de ambiente → environment variable
- substituição de comando → command substitution
- heredoc → heredoc
- fluxo → stream (stdin, stdout, stderr)

---

## Recursos

### Documentação

- [Linux man pages](https://man7.org/linux/man-pages/) — `man <cmd>` ou `man -k keyword`
- [tldr](https://tldr.sh/) — versões resumidas do man (essencial)
- [GNU Coreutils](https://www.gnu.org/software/coreutils/)
- [systemd docs](https://systemd.io/)
- [Arch Wiki](https://wiki.archlinux.org/) — melhor documentação Linux da internet, funciona para qualquer distro

### Livros

- **The Linux Command Line** — William Shotts (gratuito, linuxcommand.org)
- **Linux Bible** — Christopher Negus
- **How Linux Works** — Brian Ward
- **Systems Performance** — Brendan Gregg (profundo, referência de performance)
- **BPF Performance Tools** — Brendan Gregg (avançado)

### Blogs

- [Julia Evans](https://jvns.ca/) — Linux explained with comics
- [Brendan Gregg](https://www.brendangregg.com/) — performance deep dives
- [LWN.net](https://lwn.net/) — kernel news

### Cursos

- [Linux Foundation courses](https://training.linuxfoundation.org/)
- [Linux Journey](https://linuxjourney.com/) — interativo, gratuito

### Ferramentas modernas (vale instalar)

- [ripgrep (rg)](https://github.com/BurntSushi/ripgrep) — grep melhor
- [fd](https://github.com/sharkdp/fd) — find melhor
- [bat](https://github.com/sharkdp/bat) — cat com highlighting
- [exa / eza](https://github.com/eza-community/eza) — ls melhor
- [htop](https://htop.dev/), [btop](https://github.com/aristocratos/btop)
- [fzf](https://github.com/junegunn/fzf) — fuzzy finder
- [jq](https://jqlang.github.io/jq/), [yq](https://github.com/mikefarah/yq)
- [tmux](https://github.com/tmux/tmux)
- [zoxide](https://github.com/ajeetdsouza/zoxide) — cd mais esperto
- [direnv](https://direnv.net/) — env vars por diretório
- [ncdu](https://dev.yorhel.nl/ncdu) — du interativo
- [iotop](https://en.wikipedia.org/wiki/Iotop), [iftop](https://pdw.ex-parrot.com/iftop/), [nethogs](https://github.com/raboof/nethogs)
- [dust](https://github.com/bootandy/dust) — du moderno
- [procs](https://github.com/dalance/procs) — ps moderno
- [starship](https://starship.rs/) — prompt bonito e rápido
- [delta](https://github.com/dandavison/delta) — git diff melhor

---

## Veja também

- [[Docker]] — containers (cgroups + namespaces)
- [[Kubernetes]] — orquestração
- [[Nginx]] — reverse proxy
- [[Terminal]] — shell customization
- [[Configurando Ambiente Linux no WSL]] — WSL setup
- [[Redes e Protocolos]] — networking básico
- [[03-Dominios/Ciência/Banco de Dados/index|Banco de Dados]] — administração de DBs
- [[CI-CD]] — build e deploy em Linux
- [[System Design]] — Linux em arquitetura
