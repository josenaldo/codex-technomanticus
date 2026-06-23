---
title: "Linux"
created: 2026-04-01
updated: 2026-04-11
type: concept
progress: backlog
status: evergreen
tags:
  - infraestrutura
  - entrevista
publish: false
---

# Linux

Deep dive em **Linux** para developers — o sistema operacional que roda 90%+ dos servidores, containers, CI/CD e clouds. Fundamentos de shell, processos, filesystem, permissões, networking, systemd, debugging e troubleshooting. Para containers, ver [[Docker]]. Para orquestração, ver [[Kubernetes]]. Para terminal/shell customization, ver [[Terminal]].

## O que é

Linux é o **kernel open-source** criado por **Linus Torvalds em 1991**. Combinado com GNU userspace forma o **GNU/Linux**. Distribuições (distros) empacotam kernel + userspace + tooling:

**Famílias de distros:**

- **Debian** — Debian, Ubuntu, Linux Mint, Kali
- **Red Hat** — RHEL, Fedora, CentOS Stream, Rocky Linux, AlmaLinux, Amazon Linux 2023
- **Arch** — Arch, Manjaro, EndeavourOS
- **SUSE** — openSUSE, SLES
- **Gentoo** — Gentoo, Funtoo
- **Alpine** — Alpine (musl libc, popular em containers)

**Para desenvolvimento:**

- **Ubuntu** / **Debian** — default, mais documentação
- **Fedora** — features recentes, dev-friendly
- **Arch** — rolling release, controle total
- **Alpine** — minúsculo (~5MB), usado em containers

**Para produção:**

- **Ubuntu LTS** — 5 anos de suporte, muito comum
- **RHEL** / **Rocky** / **Alma** — enterprise, certificação
- **Amazon Linux 2023** — otimizado para AWS
- **Debian stable** — ultra estável

Em 2026, **WSL2** (Windows Subsystem for Linux) trouxe Linux nativo para Windows — muitos devs Windows hoje trabalham no WSL.

Em entrevistas, o que diferencia um senior em Linux:

1. **Filesystem hierarchy** — /etc, /var, /usr, /home, /proc, /sys
2. **Permissions** — user, group, other; rwx; sudo; POSIX ACLs
3. **Processos** — foreground/background, signals, PID, PPID, systemd
4. **Shell avançado** — pipes, redirection, substitution, loops, conditionals
5. **Networking** — ports, sockets, iptables/nftables, DNS, SSH
6. **Debugging** — top, htop, strace, lsof, tcpdump, journalctl
7. **Package management** — apt, dnf, pacman, apk
8. **Text processing** — grep, sed, awk, jq
9. **Systemd** — services, units, journalctl, targets
10. **Cgroups e namespaces** — base de containers

---

## Filesystem hierarchy

Linux segue o **FHS (Filesystem Hierarchy Standard)**:

```
/
├── bin      → /usr/bin         # binários essenciais (ls, cp, ...)
├── sbin     → /usr/sbin        # system binaries (iptables, ...)
├── lib      → /usr/lib         # bibliotecas
├── boot                         # bootloader, kernel
├── dev                          # device files (/dev/sda, /dev/null, ...)
├── etc                          # configurações do sistema
│   ├── passwd                  # users
│   ├── shadow                  # password hashes
│   ├── hosts                   # /etc/hosts
│   ├── resolv.conf             # DNS
│   ├── fstab                   # mounts no boot
│   ├── ssh/                    # SSH config
│   └── systemd/                # systemd units
├── home                         # /home/user
├── media                        # removable media
├── mnt                          # mount temporário
├── opt                          # software opcional (Oracle, VS Code, etc.)
├── proc                         # processos (virtual, gerado pelo kernel)
│   ├── cpuinfo
│   ├── meminfo
│   └── <pid>/                  # info de cada processo
├── root                         # home do root
├── run                          # runtime state (sockets, PIDs, locks)
├── srv                          # dados servidos (web, FTP)
├── sys                          # kernel interface (devices, config)
├── tmp                          # temporário (limpo no boot)
├── usr                          # user programs (read-only)
│   ├── bin                     # apps instalados
│   ├── lib
│   ├── local/                  # software instalado manualmente
│   └── share                   # docs, man pages
└── var                          # variable data
    ├── log/                    # logs (/var/log/syslog, /var/log/nginx)
    ├── lib/                    # state (databases, /var/lib/docker)
    ├── cache/
    └── spool/                  # filas (cron, mail)
```

**Regras práticas:**

- **Configuração do sistema** — `/etc`
- **Dados de usuário** — `/home/<user>`
- **Logs** — `/var/log`
- **Binários de apps** — `/usr/bin`, `/usr/local/bin`
- **Software manual** — `/opt` ou `/usr/local`
- **Temporário** — `/tmp` (volátil) ou `/var/tmp` (persistente)

---

## Shell básico

### Bash vs Zsh vs Fish

- **Bash** — default, POSIX-compliant, scripting padrão
- **Zsh** — extensível, plugins (Oh My Zsh), melhor autocomplete — **default em macOS**
- **Fish** — moderno, user-friendly, mas sintaxe diferente

Para scripts portáveis, use **bash** (ou POSIX `sh`). Para uso interativo, **zsh** ou **fish**.

> [!info] Galho dedicado
> Comandos de arquivos, pipes/redirections e text processing (grep, sed, awk, cut, sort, uniq, jq) viram referência detalhada em [[Comandos para entender agentes]] — por comando, com flags essenciais, exemplos reais e receitas combinadas.

### Variables e substitution

```bash
# Definir
NAME="Maria"
echo "Olá, $NAME"
echo "Olá, ${NAME}"            # forma explícita

# Export — passa para subshells
export PATH="/new/path:$PATH"

# Command substitution
DATE=$(date +%Y-%m-%d)
FILES=$(ls | wc -l)
echo "Hoje é $DATE, há $FILES arquivos"

# Arithmetic
result=$((5 + 3))
let x=x+1
((x++))

# Default values
${VAR:-default}     # se VAR não set, use "default"
${VAR:=default}     # e também atribui
${VAR:?error}       # erro se VAR não set
${VAR:+alternative} # se VAR set, use "alternative"
```

### Scripting bash

```bash
#!/usr/bin/env bash
set -euo pipefail           # fail fast

# Arguments
NAME=$1
AGE=${2:-30}                # default 30

# Condicionais
if [[ -f "$FILE" ]]; then
    echo "existe"
elif [[ -d "$FILE" ]]; then
    echo "é diretório"
else
    echo "não existe"
fi

# Comparações numéricas
if (( AGE > 18 )); then
    echo "adulto"
fi

# Strings
if [[ "$NAME" == "Maria" ]]; then ...
if [[ -z "$VAR" ]]; then ...      # vazio
if [[ -n "$VAR" ]]; then ...      # não vazio
if [[ "$NAME" =~ ^M ]]; then ...  # regex

# Loops
for file in *.log; do
    echo "$file"
done

for i in {1..10}; do
    echo $i
done

while read line; do
    echo "$line"
done < file.txt

# Funções
greet() {
    local name=$1
    echo "Olá, $name"
}
greet "Maria"

# Error handling
command || echo "falhou"
command && echo "sucesso"
command || exit 1
```

**Flags de `set`:**

- `set -e` — exit no primeiro erro
- `set -u` — erro em variável não definida
- `set -o pipefail` — erro se qualquer parte de pipe falhar
- `set -x` — print cada comando (debug)

**Regra:** sempre use `set -euo pipefail` em scripts de produção.

---

## Processos e jobs

### ps, top, htop

```bash
ps aux                          # todos os processos
ps -ef                          # mesmo, formato diferente
ps aux | grep nginx             # filtrar
pgrep nginx                     # só PIDs
pgrep -f "java -jar"            # por comando

top                              # interativo (q para sair)
htop                             # melhor UI (precisa instalar)

# Ordena por memória
ps aux --sort=-%mem | head

# Ordena por CPU
ps aux --sort=-%cpu | head
```

### Signals e kill

```bash
kill <pid>                     # SIGTERM (default)
kill -9 <pid>                  # SIGKILL (brutal, não pode capturar)
kill -15 <pid>                 # SIGTERM (explícito)
kill -HUP <pid>                # SIGHUP (reload config)
kill -SIGTERM <pid>

killall nginx                  # por nome
pkill -f "java -jar app.jar"   # por pattern
```

**Signals importantes:**

| Signal | Nome | Comportamento |
| --- | --- | --- |
| 1 | SIGHUP | Hangup (reload config) |
| 2 | SIGINT | Interrupt (Ctrl+C) |
| 9 | SIGKILL | Kill forçado (uncatchable) |
| 15 | SIGTERM | Terminate (graceful) |
| 17/19 | SIGSTOP | Stop (Ctrl+Z) |
| 18/20 | SIGCONT | Continue |

**Regra:** sempre prefira `SIGTERM` a `SIGKILL`. `SIGKILL` não permite cleanup.

### Foreground e background

```bash
command &                       # roda em background
command                         # foreground
Ctrl+Z                          # suspende foreground (SIGSTOP)
bg                              # continua em background
fg                              # traz para foreground
jobs                            # lista jobs
fg %1                           # traz job 1 para frente
kill %1                         # mata job 1

# Nohup — não morre quando sessão fecha
nohup command &
nohup command > out.log 2>&1 &

# Disown — desvincula do shell
command &
disown
```

**Para serviços reais**, use `systemd` (abaixo), não `nohup`.

### screen e tmux

Multiplexadores de terminal — permitem sessions persistentes:

```bash
# tmux (mais moderno)
tmux new -s mysession           # nova sessão
tmux attach -t mysession        # anexar
tmux ls                         # listar
# Dentro: Ctrl+b d para detach
```

---

## Permissões

### Modelo rwx

Cada arquivo tem:

- **Owner** (user)
- **Group**
- **Others** (todos os outros)

E cada um tem:

- **r** (read) — 4
- **w** (write) — 2
- **x** (execute) — 1

```bash
ls -l
-rw-r--r-- 1 alice developers 1234 Apr 11 10:00 file.txt
│└┬┘└┬┘└┬┘
│ │  │  └── others: r--
│ │  └───── group: r--
│ └──────── owner: rw-
└────────── tipo: - (arquivo), d (dir), l (link)
```

### chmod — alterar permissões

```bash
# Numérico (octal)
chmod 755 script.sh             # rwxr-xr-x
chmod 644 file.txt              # rw-r--r--
chmod 600 secret.key            # rw------- (só owner)
chmod 700 dir                   # rwx------ (só owner)

# Simbólico
chmod +x script.sh              # adiciona x para todos
chmod u+x script.sh             # adiciona x para owner
chmod g-w file                  # remove w do group
chmod o=r file                  # others = só r
chmod -R 755 dir                # recursivo
```

**Valores comuns:**

| Octal | Permissões | Uso |
| --- | --- | --- |
| 644 | rw-r--r-- | Arquivo normal |
| 600 | rw------- | Arquivo privado |
| 755 | rwxr-xr-x | Executável, dir |
| 700 | rwx------ | Dir privado |
| 777 | rwxrwxrwx | **Nunca** (raramente justificável) |

### chown — mudar owner/group

```bash
chown alice file.txt            # muda owner
chown alice:developers file.txt # owner e group
chown -R www-data:www-data /var/www
chgrp developers file.txt       # só group
```

### sudo

```bash
sudo command                    # roda como root
sudo -u alice command           # roda como alice
sudo -i                         # shell root interativo
sudo !!                         # re-run último comando com sudo
```

**`/etc/sudoers`** (editar com `visudo`):

```
alice ALL=(ALL) ALL             # alice pode rodar tudo
%developers ALL=(ALL) NOPASSWD: /usr/bin/docker  # grupo sem senha
```

### umask

Default permissions quando arquivo é criado:

```bash
umask                          # ver atual
umask 022                      # arquivos 644, dirs 755
umask 077                      # arquivos 600, dirs 700 (privado)
```

### Special permissions

- **SUID (4xxx)** — executa como owner (ex.: `/usr/bin/passwd`)
- **SGID (2xxx)** — executa como group, ou herda group em dirs
- **Sticky (1xxx)** — só owner pode deletar (ex.: `/tmp`)

```bash
chmod u+s file                  # SUID
chmod g+s dir                   # SGID
chmod +t dir                    # sticky
```

### ACLs (Access Control Lists)

Permissions mais granulares que user/group/other:

```bash
setfacl -m u:bob:rw file        # dá rw para bob
getfacl file                     # ver ACLs
setfacl -x u:bob file            # remove
setfacl -b file                  # remove todas ACLs
```

---

## Users e groups

```bash
# Info
whoami                          # user atual
id                              # UID, GID, grupos
id alice                        # de outro user
groups                          # grupos do user atual
who                             # users logados
w                               # mais detalhado

# Criar/remover
sudo useradd -m -s /bin/bash alice  # -m cria home, -s shell
sudo passwd alice                   # define senha
sudo userdel -r alice               # -r remove home
sudo usermod -aG docker alice       # adiciona ao grupo docker

# Grupos
sudo groupadd developers
sudo groupdel developers
```

**Arquivos importantes:**

- `/etc/passwd` — lista de users
- `/etc/shadow` — hashes de senha
- `/etc/group` — grupos

---

## Networking

### Comandos essenciais

```bash
# Info de interface
ip addr                          # IPs (substitui ifconfig)
ip a                             # atalho
ip link                          # links
ip route                         # tabela de rotas
ip route get 8.8.8.8             # rota para um IP

# Legacy
ifconfig
route -n

# Conectividade
ping google.com
ping -c 4 google.com             # 4 pacotes
traceroute google.com
mtr google.com                   # ping + traceroute contínuo

# DNS
dig google.com
dig @8.8.8.8 google.com          # servidor específico
dig google.com MX                # MX records
host google.com
nslookup google.com              # legacy
cat /etc/resolv.conf             # config DNS
cat /etc/hosts                   # overrides locais

# Portas abertas
ss -tuln                         # socket stats (substitui netstat)
ss -tulnp                        # + processo
netstat -tulnp                   # legacy

# Conexões ativas
ss -t                            # TCP
ss -u                            # UDP
ss -t state established          # conexões estabelecidas

# HTTP
curl -I https://example.com      # só headers
curl -v https://example.com      # verbose
curl -X POST -d '{"key":"val"}' -H "Content-Type: application/json" https://api.com
curl -o file.tar.gz https://example.com/file.tar.gz    # salva
curl --resolve example.com:443:1.2.3.4 https://example.com  # força IP

# Download
wget https://example.com/file
wget -c https://example.com/file  # continua
```

### SSH

```bash
# Conectar
ssh user@host
ssh -p 2222 user@host
ssh -i ~/.ssh/mykey.pem user@host

# Keys
ssh-keygen -t ed25519 -C "email@example.com"
ssh-copy-id user@host             # copia public key para ~/.ssh/authorized_keys

# Config — ~/.ssh/config
Host prod
    HostName 1.2.3.4
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/prod.pem

# Agora: ssh prod

# Tunnel (port forwarding)
ssh -L 8080:localhost:80 user@host      # local 8080 → remote 80
ssh -R 9000:localhost:3000 user@host    # reverse (expor local na remote)
ssh -D 1080 user@host                   # SOCKS proxy

# Copiar arquivos
scp file user@host:/path
scp user@host:/path/file .
scp -r dir user@host:/path

# Rsync (melhor)
rsync -av dir/ user@host:/path/       # sync incremental
rsync -av --delete dir/ user@host:/path/  # com delete
rsync -az --progress dir/ user@host:/path/  # com compressão
```

**Regras de segurança SSH:**

1. **Use key-based auth**, desabilite password auth
2. **Use Ed25519**, não RSA antigo
3. **Porta 22 OK** (se firewall correto) ou mude para outra
4. **`PermitRootLogin no`** em `/etc/ssh/sshd_config`
5. **Fail2ban** para bloquear bruteforce

### Firewall

**iptables** (legacy) ou **nftables** (moderno) ou **ufw** (simples):

```bash
# ufw (Ubuntu — simples)
sudo ufw enable
sudo ufw allow 22
sudo ufw allow 443/tcp
sudo ufw deny 3306
sudo ufw status

# iptables
sudo iptables -L
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# nftables (moderno)
sudo nft list ruleset
```

### Network namespaces

Base de containers. Permite criar stacks de rede isoladas:

```bash
sudo ip netns add mynet
sudo ip netns exec mynet ip addr
```

---

## Systemd

**systemd** é o init system padrão da maioria das distros modernas. Gerencia serviços, targets (equivalente a runlevels), logs, sockets, timers.

### Gerenciando serviços

```bash
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx     # SIGHUP (reload config sem restart)
sudo systemctl status nginx
sudo systemctl enable nginx     # start no boot
sudo systemctl disable nginx    # não start no boot
sudo systemctl is-active nginx
sudo systemctl is-enabled nginx
sudo systemctl list-units --type=service
sudo systemctl list-units --failed
```

### Criar um serviço

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/node /opt/myapp/server.js
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=myapp

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/myapp /var/lib/myapp

# Resource limits
MemoryMax=1G
CPUQuota=50%

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now myapp
```

### journalctl — logs do systemd

```bash
journalctl                           # todos os logs
journalctl -u nginx                  # de um serviço
journalctl -u nginx -f               # follow
journalctl -u nginx --since "1 hour ago"
journalctl -u nginx --since today
journalctl -u nginx --since "2026-04-10 10:00" --until "2026-04-10 11:00"
journalctl -u nginx -n 100           # últimas 100
journalctl -u nginx -p err           # só erros
journalctl -k                        # kernel
journalctl --disk-usage              # espaço ocupado
sudo journalctl --vacuum-time=2d     # limpar > 2 dias
sudo journalctl --vacuum-size=500M   # limitar a 500M
```

### Timers (alternativa a cron)

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily backup

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Backup script

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```

```bash
sudo systemctl enable --now backup.timer
sudo systemctl list-timers
```

---

## Package management

### APT (Debian/Ubuntu)

```bash
sudo apt update                      # atualiza índices
sudo apt upgrade                     # atualiza pacotes
sudo apt install nginx postgresql
sudo apt remove nginx                 # remove pacote
sudo apt purge nginx                  # remove + configs
sudo apt autoremove                   # remove deps órfãs
apt search nginx
apt show nginx
apt list --installed
sudo apt update && sudo apt upgrade   # atualização completa
```

### DNF (Fedora/RHEL)

```bash
sudo dnf install nginx
sudo dnf update
sudo dnf remove nginx
sudo dnf search nginx
sudo dnf info nginx
sudo dnf list installed
```

### Pacman (Arch)

```bash
sudo pacman -S nginx             # install
sudo pacman -Syu                 # sync + update
sudo pacman -R nginx             # remove
sudo pacman -Rs nginx            # + deps órfãs
pacman -Ss nginx                 # search
pacman -Si nginx                 # info
```

### APK (Alpine)

```bash
apk add nginx
apk update
apk upgrade
apk del nginx
apk search nginx
apk info nginx
```

### Universal — Snap, Flatpak, AppImage

- **Snap** (Canonical) — containers, auto-update
- **Flatpak** — desktop apps, sandboxed
- **AppImage** — single file, portátil

```bash
sudo snap install vscode --classic
flatpak install flathub org.mozilla.firefox
```

---

## Debugging e performance

### Monitoring

```bash
top                              # processos live
htop                             # melhor UI
btop                             # mais moderno
atop                             # histórico
vmstat 1                         # virtual memory stats
iostat -x 1                      # I/O stats (sysstat)
mpstat 1                         # CPU por core
sar                              # historical (sysstat)

# Memory
free -h                          # RAM
free -m                          # MB

# Disk
df -h                            # free space
du -sh /                         # uso de diretório
iotop                            # I/O top
ncdu /                           # UI para du

# Network
iftop                            # live network
nethogs                          # por processo
ss -tuln                         # ports
```

### strace — syscall tracing

```bash
strace ls                        # traça todas as syscalls
strace -p <pid>                  # processo existente
strace -e trace=open,read ls     # só open e read
strace -c ls                     # summary
strace -o trace.log ls           # salva em arquivo
```

**Uso:** debuggar "por que não abre esse arquivo?", ver syscalls reais, descobrir onde um programa está bloqueado.

### lsof — list open files

```bash
lsof -p <pid>                    # arquivos abertos por processo
lsof -i :80                      # quem usa porta 80
lsof -i TCP                      # conexões TCP
lsof -u alice                    # de um user
lsof /path/file                  # quem usa esse arquivo
lsof +D /var/log                 # recursivo
```

### tcpdump — packet capture

```bash
sudo tcpdump -i eth0
sudo tcpdump -i eth0 port 80
sudo tcpdump -i eth0 host 1.2.3.4
sudo tcpdump -i eth0 -w out.pcap         # salva para Wireshark
sudo tcpdump -i eth0 -A port 80          # ASCII (texto)
```

### dmesg — kernel messages

```bash
dmesg                            # todas
dmesg -T                         # timestamps humanos
dmesg | grep -i error
sudo dmesg -w                    # follow
```

### perf — performance counters

```bash
sudo perf top                         # hot functions live
sudo perf record -F 99 -a -g -- sleep 10    # profile
sudo perf report                      # ver resultado
```

### Debugging checklist — "O servidor está lento"

```bash
# 1. Load average
uptime                           # carga dos últimos 1, 5, 15 min
# > número de cores = overload

# 2. CPU
top                              # quem está usando CPU?
mpstat 1                         # por core

# 3. Memory
free -h                          # quanto livre?
# swap muito ativo = problema

# 4. Disk I/O
iostat -x 1                      # %util > 80% = bottleneck
iotop                            # quem está usando

# 5. Disk space
df -h                            # cheio?

# 6. Network
ss -tan | wc -l                  # quantas conexões?
iftop                            # banda

# 7. Processes
ps aux --sort=-%mem | head       # top mem
ps aux --sort=-%cpu | head       # top cpu

# 8. Logs
journalctl -p err --since "1 hour ago"
tail -f /var/log/syslog
```

### Brendan Gregg's checklist (60 seconds)

Lendária checklist para diagnosticar servidor lento em 60 segundos:

```bash
uptime
dmesg | tail
vmstat 1
mpstat -P ALL 1
pidstat 1
iostat -xz 1
free -m
sar -n DEV 1
sar -n TCP,ETCP 1
top
```

---

## Cgroups e namespaces

Base dos containers. Linux kernel features que permitem isolamento.

### Namespaces

Isolam recursos:

- **PID** — processos não se veem
- **NET** — network stacks separadas
- **MNT** — filesystem mounts
- **UTS** — hostname
- **IPC** — inter-process communication
- **USER** — UIDs/GIDs (privilégios)
- **CGROUP** — controle de cgroups
- **TIME** — relógio (raro)

```bash
sudo unshare -p -f --mount-proc /bin/bash  # novo PID namespace
ls /proc/<pid>/ns/                          # ver namespaces de um processo
```

### Cgroups (control groups)

Limita e contabiliza recursos:

- **CPU** — limit, shares
- **Memory** — limit, swap
- **IO** — disk throughput
- **Devices** — access
- **Network** — via tc
- **PIDs** — máximo de processos

```bash
# v2 (moderno) — /sys/fs/cgroup/
cat /sys/fs/cgroup/memory.max
cat /sys/fs/cgroup/cpu.max

# Criar cgroup (systemd)
systemd-run --scope -p MemoryMax=500M --user command
```

**Containers** (Docker, Podman) usam namespaces + cgroups por baixo dos panos.

---

## Armadilhas comuns

- **`rm -rf /`** — sem proteção, destrói sistema. Use `--preserve-root` (default em GNU rm moderno) e pense 3 vezes
- **`chmod 777`** — nunca. Sempre mínimo privilégio.
- **Cat de log gigante** — use `less` ou `tail`
- **`grep -r`** em `/` — lento e pode percorrer filesystems especiais. Use ripgrep ou limite.
- **Editar `/etc/sudoers` sem `visudo`** — syntax error pode bloquear sudo
- **Ignorar `set -euo pipefail`** em scripts — erros silenciosos
- **Usar `sh` quando precisa de bash** — `#!/bin/sh` em scripts bash pode quebrar em Alpine (dash)
- **`kill -9` antes de tentar `kill`** — processo não tem chance de cleanup
- **Esquecer `sudo systemctl daemon-reload`** após editar unit file
- **Logs escrevendo em `/var/log` sem rotate** — disk cheio
- **`umask` errado em script** — arquivos com permissão muito aberta
- **Não usar `quotes` em variáveis** — `rm $FILE` quebra se FILE tem espaço
- **`ls | grep` em vez de shell glob** — parse de ls é não-portável
- **`curl | sh`** — rode software confiável sem ler? Risco
- **SSH keys sem passphrase em laptops** — roubo = acesso total
- **`:` em ficheiros de path** — quebra `$PATH`
- **`.` em `$PATH`** — vulnerabilidade clássica
- **Esquecer `&` e `disown`** — fechar terminal mata processo
- **Editing file durante write** — corrupção
- **Pipes em scripts sem `pipefail`** — erros invisíveis
- **Confundir `echo $?`** com sucesso — verifica exit code do **último** comando
- **Crontab em vez de systemd timer** — systemd é mais robusto (logs, dependências)
- **`find -exec cmd {} \;`** quando `xargs -0` é mais eficiente

---

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
