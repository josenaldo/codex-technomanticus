---
title: "Monitores e disco — btop, htop, dust"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - terminal
  - cli-utils
  - magus
  - btop
  - htop
  - dust
  - monitoring
aliases:
  - btop
  - htop
  - dust
  - Monitores
---

> [!abstract] TL;DR
> Três ferramentas pra observabilidade local: **btop** (TUI moderna com gráficos e mouse), **htop** (clássico leve, ubíquo em servidores), **dust** (du moderno em árvore por tamanho). htop pra ssh em servidor minimalista; btop pra workstation rica; dust pra responder "quem comeu meu disco?". Todos lêem `/proc` (Linux) ou equivalente; nenhum precisa root pra uso comum.

## O que é / Como funciona

### btop — monitor moderno

TUI rica em C++: CPU/RAM/disk/network com gráficos visuais, lista de processos, sensors. Mouse-aware — clique pra ordenar coluna, scroll com roda. Themes customizáveis em `~/.config/btop/themes/`. Config persistente em `~/.config/btop/btop.conf` (gerada no primeiro run).

Modo TTY (`--tty_on`) reduz uso de chars Unicode pra rodar bem em ssh com bandwidth limitado.

### htop — clássico leve

TUI simples desenvolvida desde 2004, ubíqua em quase todo Linux server. F-keys principais:

| Tecla | Ação |
|---|---|
| F2 | Setup (config) |
| F3 | Search por nome |
| F4 | Filter por padrão |
| F5 | Tree view (parent → children) |
| F6 | Sort by column |
| F9 | Kill (escolhe signal) |
| F10 | Quit |

Footprint mínimo (~5MB RAM). Suporta árvore de processos, filtros por user (`htop -u <user>`), por PID (`htop -p <pids>`).

### dust — du moderno

Visualização em árvore por tamanho com barras horizontais coloridas. Default mostra top N maiores (~30 entries). Flags principais:

- `-d <num>` — profundidade máxima
- `-n <num>` — número de entries
- `-r` — reverte ordem
- `-X <nome>` — pula pastas/arquivos com este nome
- `-e <regex>` — incluir só arquivos que casam regex
- `-v <regex>` — excluir arquivos que casam regex
- `-z <size>` — minimum size (ex: `-z 10M`)
- `-c` — sem cores (monochrome)
- `-p` — paths completos

**Não respeita `.gitignore` por padrão** (sem flag pra isso) — em projetos com `node_modules/`/`target/`/`vendor/`, esses dirs dominam o output.

### Comparação btop vs htop

| Aspecto | btop | htop |
|---|---|---|
| Visual | Rico (gráficos, mouse) | Simples (barras, listas) |
| Resource overhead | Maior (~20-50MB RAM) | Mínimo (~5MB) |
| Customização | Themes, layout flexível | Config básica |
| ssh em servidor minimalista | `--tty_on` funciona | Default OK |
| Workstation moderna | Default ótimo | Funciona, sub-utiliza terminal |

### Quando cada um vence

- **htop em ssh:** server slow, bandwidth limitado, "matar processo rápido"
- **btop em workstation:** monitorar build local, ver IO/network em gráfico, mouse-friendly
- **dust em disco cheio:** identificar pasta culpada rapidamente

## Na prática

### Setup

```bash
# btop config gerada no primeiro run
btop                                  # cria ~/.config/btop/btop.conf

# htop config interativa (F10 após mudanças salva)
htop                                  # cria ~/.config/htop/htoprc com setup

# dust não tem config persistente — flags por invocação
dust --version
```

### Receitas comuns

```bash
# Top 30 maiores pastas, profundidade 3
dust -d 3 -n 30 ~

# Excluir pastas custosas (dust não respeita .gitignore)
dust -d 2 -X node_modules -X .git -X target ~

# Só arquivos maiores que 100MB
dust -z 100M ~/Downloads

# Só arquivos PNG (regex include)
dust -e '\.png$' ~/Pictures

# htop com refresh 1s, só processos do user atual
htop -d 1 -u $USER

# btop em modo TTY (ssh resource-baixo)
btop --tty_on

# Buscar processo no htop: F3, digitar nome, Enter
# Matar no htop: F9, escolher signal (default SIGTERM 15, alternativa 9=SIGKILL)
```

### Aliases sugeridos

```bash
alias top=btop                        # se workstation tem btop instalado
alias du-disk='dust -d 3 -n 30'
alias htops='htop -d 1 -u $USER'      # htop refresh rápido, scoped por user
```

### Persistência de config (dotfiles)

- **btop**: `~/.config/btop/btop.conf` pode ir nos dotfiles, mas tem paths absolutos OS-específicos — usar template (chezmoi) ou regenerar por máquina
- **htop**: `~/.config/htop/htoprc` é portável; gere em uma máquina, replique
- **dust**: sem config; flags por uso

### Versão hedged

btop 1.3+; htop 3.x+; dust 1.2+. Verifique versões localmente com `<tool> --version`.

## Armadilhas

### (1) btop em ssh com bandwidth baixo

**Causa:** btop default usa muitos chars Unicode pra gráficos; em conexão lenta, refresh lag.

**Sintoma:** btop fica congelado por segundos a cada update.

**Como detectar:** ssh com `-vvv` mostra latência alta; comparar `btop` vs `htop` na mesma conexão.

**Solução:** rodar com `btop --tty_on` (modo TTY-friendly, menos chars Unicode). Ou usar htop em servidor remoto — htop é nativamente leve.

### (2) htop kill em árvore pode matar processo errado

**Causa:** F5 tree view mostra hierarquia; F9 (kill) na pasta-pai não mata children pelo PID parent — mas matar parent pode deixar children órfãos (adotados por init/systemd).

**Sintoma:** processo mau-comportado continua rodando após "kill no parent".

**Como detectar:** após kill, `ps aux` mostra child ainda ativo.

**Solução:** entender o problema: pra matar grupo de processos, usar PGID (`kill -- -$PGID`) ou `pkill -P <ppid>` (kill children do parent). htop em si só mata por PID individual.

### (3) dust não respeita `.gitignore`

**Causa:** dust não tem flag pra respeitar gitignore por default.

**Sintoma:** output infla com `node_modules/`, `target/`, `vendor/`, `.git/` — pasta inocente parece grande.

**Como detectar:** rodar `dust -d 2 .` em projeto com `node_modules`; ver se aparece.

**Solução:** usar `-X` repetido pra pular pastas comuns: `dust -X node_modules -X .git -X target -X vendor -X build`. Considerar criar alias `alias dustp='dust -X node_modules -X .git -X target -X vendor'` pra projetos.

### (4) btop config persistido em dotfiles com paths absolutos

**Causa:** btop salva paths de logs, themes customizados em `btop.conf` — paths absolutos da máquina origem (`/home/alice/.config/btop/themes/...`).

**Sintoma:** ao copiar config pra outra máquina, btop falha em achar log/theme paths.

**Como detectar:** abrir `btop.conf` e procurar paths que começam com `/`.

**Solução:** versionar só keys portáveis (theme padrão, cores, layout); regenerar config em cada máquina. Ou usar chezmoi templates pra substituir paths por `{{ .chezmoi.homeDir }}`.

### (5) Contagem de RAM Linux ≠ "memória disponível" intuitiva

**Causa:** Linux conta cache + buffers como "usado" pra fins de `free`, mas o campo `available` (kernel ≥ 3.14) é o que realmente importa pra aplicações.

**Sintoma:** htop mostra 90% RAM "usada"; mas sistema responde bem (cache, não app).

**Como detectar:** comparar `free -h` (used) vs (available); a diferença é cache reclamável.

**Solução:** confiar em `available`, não `used`. btop tem visualização separada de cache vs realmente-usado. Em htop, modo "free memory" (configurável em F2) mostra parecido com `free -h`.

### (6) Confundir RSS / VSZ no kill decision

**Causa:** RSS (resident set size — RAM real) vs VSZ (virtual — endereço alocado, pode não usar) — kill por VSZ alto pode matar processo inocente.

**Sintoma:** processo com VSZ enorme parece "comilão" mas RSS é pequeno (lazy allocation, mmap).

**Como detectar:** htop mostra ambos (coluna `RES` ou `M_RESIDENT` = RSS; coluna `VIRT` ou `M_SIZE` = VSZ).

**Solução:** priorizar RSS pra decisões de kill por memória. VSZ é só ceiling de endereço; muitos processos modernos têm VSZ grande sem custo real.

## Em inglês

- **Monitor de processos** — *process monitor*. "btop e htop são process monitors com TUI rica."
- **Uso de memória** — *memory usage*. "RSS reflete o memory usage real; VSZ é o virtual alocado."
- **Resident set size** — *resident set size (RSS)*. "RSS é a memória física que o processo está ocupando."
- **Memória virtual** — *virtual memory*. "Virtual memory inclui mmap e regiões não-paginadas."
- **Uso de disco** — *disk usage*. "dust mostra disk usage em árvore visual."
- **Visão em árvore** — *tree view*. "htop F5 abre tree view de processos parent → children."
- **Taxa de refresh** — *refresh rate*. "`htop -d 1` define refresh rate de 1 segundo."
- **Sinal de kill** — *kill signal*. "F9 no htop escolhe o kill signal (SIGTERM, SIGKILL, etc.)."
- **Memória disponível** — *available memory*. "Linux 3.14+ expõe available memory separado de used."
- **Cache** — *cache*. "Linux usa RAM livre como cache; libera quando aplicação precisa."

## Veja também

- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[03-Dominios/Tecnologia/Terminal/TUIs/index|TUIs (galho 4)]] — Lazydocker pra inspeção específica de containers (vs btop pra host)
- [[Dicionário do Terminal#btop|btop]]
- [[Dicionário do Terminal#htop|htop]]
- [[Dicionário do Terminal#dust|dust]]

## Referências

- btop: https://github.com/aristocratos/btop
- htop: https://htop.dev/
- dust: https://github.com/bootandy/dust
