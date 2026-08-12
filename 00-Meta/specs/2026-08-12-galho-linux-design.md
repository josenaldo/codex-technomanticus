---
title: "Design — Galho 4: Linux"
created: 2026-08-12
type: meta
publish: false
tags:
  - meta
  - spec
  - design
  - linux
  - infraestrutura
---

# Design — Galho 4: Linux

Spec de roster do último galho do domínio `Tecnologia/Infraestrutura`, previsto na [[00-Meta/specs/2026-08-02-dominio-infraestrutura-design|spec de design do domínio]] e adiado de propósito para depois de Docker, Kubernetes e Nginx — porque é o galho que mais se sobrepõe a vizinhos, e escrevê-lo por último permite que as fronteiras dos outros três já estejam cravadas.

**Lente do galho:** *o sistema como o processo o vê.*

---

## Levantamento de fronteira — feito ANTES do roster

Este é o método que o domínio adotou desde Padrões de Projeto e que, nos galhos 3 (Nginx) e 2 (Kubernetes), evitou notas redundantes e definiu a lente. Aqui ele é mais crítico que nos outros três, porque o Linux faz fronteira com **quatro** vizinhos ao mesmo tempo.

### Vizinho 1 — `Ciência/Sistemas Operacionais` (14 notas)

O galho mais perigoso, porque cobre o mesmo vocabulário por outro eixo. O que **já existe lá**: o que é um SO · system calls e a fronteira kernel-usuário · processos · threads · escalonamento de CPU · memória lógica→física · memória virtual e paginação · substituição de páginas e thrashing · IPC · I/O · sistemas de arquivos · journaling · **virtualização e containers** · SO em entrevista.

**A divisão:** lá é *como o mecanismo funciona*, aqui é *como ele se manifesta numa máquina que você precisa operar*. A nota de escalonamento explica algoritmos; a nota daqui explica por que o `load average` está em 14 e o que fazer. A nota de memória virtual explica paginação; a nota daqui explica por que o processo morreu sem log e como confirmar que foi o OOM killer.

> [!warning] Regra dura deste galho
> Nenhuma nota daqui reabre mecanismo de kernel. Onde a explicação exigir, **linka e segue**. Foi exatamente a regra aplicada na nota 15 do Docker, e é o que impede este galho de virar uma segunda versão pior de `Ciência/SO`.

### Vizinho 2 — `Tecnologia/Terminal` (7 galhos, 78 notas)

O que **já existe lá**: Shell com 10 notas centradas em **Zsh como ambiente** (Zsh × Bash, history, Oh-My-Zsh, Powerlevel10k, keybindings, ZLE, completion, globbing e parameter expansion, plugins) · CLI Utils (fzf, ripgrep, bat, eza, delta) · Dotfiles · Editor (Neovim) · Multiplexer (tmux/Zellij) · TUIs (Lazygit, Lazydocker) · Workflow.

**A divisão:** lá é a **ergonomia do shell** — como *você* trabalha; aqui é o **sistema por baixo dele**. `Ctrl-R` e completion são de lá. Descritor de arquivo, redirecionamento, o que `2>&1` significa para o kernel, e por que um processo em background morre ao fechar o terminal são daqui.

> [!question]- E scripting em Bash, fica onde?
> **Fora dos dois, por ora.** O galho Shell do Terminal é deliberadamente Zsh-como-ambiente-interativo e não trata script como artefato; este galho trata o sistema, não a linguagem. Escrever Bash bem — `set -euo pipefail`, quoting, arrays, armadilhas de expansão — é assunto de tamanho próprio e mereceria um galho em Terminal, não um apêndice aqui. **Registrado como lacuna consciente**, não absorvido.

### Vizinho 3 — `Engenharia/Operação`

O que já existe lá: observabilidade, SLO, alerting, resposta a incidente, postmortem, debugging e chaos.

**A divisão:** lá é o **ofício de operar** — o que é um SLO, como se conduz um incidente, o que entra num postmortem. Aqui é **a máquina**: quais comandos revelam o quê, nesta máquina, agora. A nota de diagnóstico daqui é o instrumento que a nota de incidente de lá pressupõe.

### Vizinho 4 — os galhos 1-3 deste mesmo domínio

Docker, Kubernetes e Nginx já foram escritos e já apontam para cá em três pontos. O Docker 15 cede o *como* do kernel a `Ciência/SO 13`; o Kubernetes 17 trata do kubelet e do nó; o Nginx 13 trata de `worker_rlimit_nofile` e do teto de descritores. **Este galho é quem explica descritor de arquivo, cgroup e namespace do ponto de vista de quem administra a máquina** — o degrau que falta entre a teoria de `Ciência/SO` e a ferramenta dos galhos 1-3.

### O que sobra de fato para este galho

Depois de subtrair os quatro vizinhos, o território é: **a hierarquia e o modelo de arquivos · identidade e permissão · o processo como objeto administrável · o sistema de init e serviços · a máquina na rede · software instalado · e diagnóstico.** É coerente, é de tamanho razoável, e não existe em nenhum outro lugar do vault.

---

## Material-semente

| Fonte | Tamanho | Destino |
|---|---|---|
| `Infraestrutura/Linux.md` | 1118 linhas | Semente principal. Cobre FHS, shell, processos e jobs, permissões, users/groups, rede, systemd, pacotes, debugging. Vira tronco podado, como Docker.md, Kubernetes.md e Nginx.md |
| `Infraestrutura/Linux/Comandos para entender agentes.md` | 572 linhas | Nota existente, `type: reference`. **Não é conteúdo de trilha** — é uma referência de comandos com recorte próprio. Mantém-se como referência do galho, com callout de ponte |
| `Infraestrutura/Configurando Ambiente Linux no WSL.md` | 7,9 K | Material de ambiente local; permanece como referência solta, conforme decidido no Roadmap |

---

## Roster proposto — 16 notas em 3 fases

### Iniciado — o sistema visível (5)

| # | Nota | Lente |
|---|------|-------|
| 01 | O que o Linux entrega a um processo | o contrato: PID, credenciais, descritores, cwd, ambiente. A nota que estabelece a lente do galho |
| 02 | A hierarquia do sistema de arquivos | FHS como convenção, não regra · `/proc` e `/sys` como sistemas de arquivos **sintéticos** — a porta pela qual tudo o mais neste galho é observado |
| 03 | Tudo é arquivo — descritores e redirecionamento | fd 0/1/2 · o que `2>&1` faz de verdade · pipe como fd · por que a ordem do redirecionamento importa · `lsof` como leitura da tabela |
| 04 | Identidade: usuários, grupos e permissão | rwx, octal, `chmod`/`chown` · umask · setuid/setgid/sticky · ACL quando o modelo básico não basta · `sudo` como política, não como prefixo |
| 05 | O processo como objeto administrável | árvore de processos e PPID · estados (incluindo zumbi e `D`) · sinais como interface · `nohup`, `&`, e por que o processo morre ao fechar o terminal |

### Adepto — o sistema operado (6)

| # | Nota | Lente |
|---|------|-------|
| 06 | systemd: o modelo de unidades | por que substituiu o init · unit, target, dependência · o ciclo `start`/`enable` e a diferença entre os dois |
| 07 | Escrever um serviço que se comporta | arquivo `.service` comentado · `Restart=`, `User=`, limites · o contrato de sinal e o timeout de parada — mesma discussão do PID 1 do Docker 08, agora do lado do host |
| 08 | Logs: journald e o que veio antes | journal binário × texto em `/var/log` · `journalctl` com recorte por unidade, tempo e prioridade · persistência e rotação |
| 09 | Agendamento: cron e timers | cron e sua sintaxe · timers do systemd · por que timer venceu em máquina moderna · o erro clássico do `PATH` no cron |
| 10 | A máquina na rede | interfaces e endereços (`ip`) · rotas · o que está escutando (`ss`) · resolução de nomes e a bagunça do `/etc/resolv.conf` · firewall como conceito |
| 11 | Software instalado | gerenciador de pacotes como banco de dados · apt/dnf/pacman/apk lado a lado · repositório e assinatura · Snap/Flatpak/AppImage e o que eles resolvem · por que "instalar do site" é decisão, não atalho |

### Magus — o sistema investigado (4 + capstone)

| # | Nota | Lente |
|---|------|-------|
| 12 | Diagnóstico: os primeiros sessenta segundos | o checklist de Brendan Gregg, comando a comando · o que **load average** de fato mede em Linux (inclui `D`, não só CPU) · o método antes das ferramentas |
| 13 | CPU, memória, disco e I/O, um de cada vez | quatro eixos, quatro conjuntos de sinais · o que é `%wa` · por que memória "livre" quase nunca é o número que importa |
| 14 | Quando o processo some: OOM killer e limites | `oom_score` e como a decisão é tomada · onde isso aparece no log · `ulimit` e `RLIMIT_*` · a ponte com o Kubernetes 17, que trata do mesmo mecanismo do lado do orquestrador |
| 15 | Ver o que o processo pede ao kernel | `strace` e o que ele custa · `lsof` de novo, agora como investigação · `dmesg` e o boot · quando a resposta está no kernel e não na aplicação |
| 16 | Capstone — a máquina que ficou lenta às três da manhã | investigação completa, do primeiro `uptime` à causa raiz, atravessando os quatro eixos e terminando numa decisão |

---

## Ordem de construção

Sequencial, em blocos, **com pergunta ao usuário a cada bloco** — a convenção do domínio:

1. **Bloco 1** (01-03) — a lente e o modelo de arquivos. É o bloco que define se o galho tem identidade própria ou vira apêndice de `Ciência/SO`.
2. **Bloco 2** (04-05) — identidade e processo.
3. **Bloco 3** (06-07) — systemd.
4. **Bloco 4** (08-09) — logs e agendamento.
5. **Bloco 5** (10-11) — rede e pacotes.
6. **Bloco 6** (12-13) — diagnóstico.
7. **Bloco 7** (14-16) — limites, kernel e capstone.
8. **Fechamento** — poda do `Linux.md`, callouts de volta, `index.md`, `roadmap.md`.

## Critérios de pronto

Os mesmos do domínio: padrão capítulo · `fase:` no frontmatter · abertura por problema · Mermaid onde o assunto é estrutural · `## Armadilhas comuns` com `[!warning]` · inglês com tabela PT↔EN · ponte `## O que vem a seguir` · `## Fontes` com URL clicável · zero wikilinks quebrados. **M1 em passada posterior**, com `yt-dlp` central — e com a expectativa, baseada nos três galhos anteriores, de yield alto: Linux tem material de conferência e canais de autoridade em abundância.

## Riscos

**O risco número um é redundância com `Ciência/SO`**, e a mitigação é a regra dura declarada acima. **O risco número dois é o galho inchar**: FHS, permissões, rede e pacotes são assuntos que aceitam expansão infinita, e o corte é a lente — se a informação não muda o que você faz diante de uma máquina, ela é de outro galho.

## Lacunas conscientes registradas

- **Scripting em Bash** — não entra aqui nem no Terminal atual; merece galho próprio em `Tecnologia/Terminal`.
- **SSH** — o monólito o cobre; a decisão é tratá-lo como **ferramenta de acesso** e deixá-lo na nota 10 (rede) em nível de uso, sem virar nota própria. Chaves, agente e configuração de servidor pertencem a segurança operacional, não a este galho.
- **SELinux/AppArmor** — fora. É superfície grande e de baixo retorno para o perfil-alvo; fica registrado como possível broto.
