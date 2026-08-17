---
title: "Roadmap — Galho 4: Linux"
created: 2026-08-12
updated: 2026-08-12
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Galho 4: Linux

Roadmap do galho `Tecnologia/Infraestrutura/Linux` (galho-folha), o **último do domínio**. Fonte do roster: [[00-Meta/specs/2026-08-12-galho-linux-design|design de 2026-08-12]], que traz o levantamento de fronteira feito antes do roster.

**Lente:** *o sistema como o processo o vê.*

**Estado: escrita completa — 16/16 notas em 2026-08-16.** Falta só M1.

**Legenda:** ✅ escrita + M1 · 🔶 escrita, falta M1 · 📋 desenhada · ⬜ não iniciada.

## Notas

| # | Nota | Fase | Estado | Bloco |
|---|------|------|--------|-------|
| 01 | O que o Linux entrega a um processo | Iniciado | 🔶 escrita 2026-08-12 | 1 |
| 02 | A hierarquia do sistema de arquivos | Iniciado | 🔶 escrita 2026-08-12 | 1 |
| 03 | Tudo é arquivo — descritores e redirecionamento | Iniciado | 🔶 escrita 2026-08-12 | 1 |
| 04 | Identidade: usuários, grupos e permissão | Iniciado | 🔶 escrita 2026-08-12 | 2 |
| 05 | O processo como objeto administrável | Iniciado | 🔶 escrita 2026-08-12 | 2 |
| 06 | systemd: o modelo de unidades | Adepto | 🔶 escrita 2026-08-14 | 3 |
| 07 | Escrever um serviço que se comporta | Adepto | 🔶 escrita 2026-08-14 | 3 |
| 08 | Logs: journald e o que veio antes | Adepto | 🔶 escrita 2026-08-16 | 4 |
| 09 | Agendamento: cron e timers | Adepto | 🔶 escrita 2026-08-16 | 4 |
| 10 | A máquina na rede | Adepto | 🔶 escrita 2026-08-16 | 5 |
| 11 | Software instalado | Adepto | 🔶 escrita 2026-08-16 | 5 |
| 12 | Diagnóstico: os primeiros sessenta segundos | Magus | 🔶 escrita 2026-08-16 | 6 |
| 13 | CPU, memória, disco e I/O, um de cada vez | Magus | 🔶 escrita 2026-08-16 | 6 |
| 14 | Quando o processo some: OOM killer e limites | Magus | 🔶 escrita 2026-08-16 | 7 |
| 15 | Ver o que o processo pede ao kernel | Magus | 🔶 escrita 2026-08-16 | 7 |
| 16 | Capstone — a máquina que ficou lenta às três da manhã | Magus | 🔶 escrita 2026-08-16 | 7 |

## Outros arquivos do galho

| Arquivo | Tipo | Estado |
|---|---|---|
| `index.md` | MOC | ✅ reformado 2026-08-16 — MOC por fase, referência do galho e tabela de fronteiras |
| `Comandos para entender agentes.md` | reference | ✅ mantido como referência do galho, **com callout de ponte inserido 2026-08-16** |
| `Infraestrutura/Linux.md` | monólito-semente | ✅ **podado 2026-08-16: 1118 → 198 linhas**, com mapa de redirecionamento; seções de relato pessoal e de inglês preservadas |

## Bloco 1 — o que ficou decidido ao escrever

- **A lente se sustentou.** A nota 01 estabelece o **contrato de execução** (identidade, credenciais, descritores, lugar, ambiente, limites, recorte) e as notas seguintes são cada uma um item desse contrato. Isso resolve o risco número um do design — virar apêndice de `Ciência/SO` —, porque o eixo passou a ser *o que o processo recebeu*, não *como o kernel implementa*.
- **`/proc` virou a espinha instrumental do galho.** A nota 02 apresenta `/proc` e `/sys` como sistemas de arquivos **sintéticos**, e a partir daí toda investigação das notas seguintes tem onde ser verificada. O detalhe de `/proc/uptime` ter tamanho zero e conteúdo é o gancho didático que fecha a ideia.
- **Encadeamento por enigma, não por sumário.** A nota 02 termina no arquivo apagado que não libera espaço, e a 03 resolve com descritor. Vale repetir o padrão nos blocos seguintes.
- **Fronteira respeitada sem exceção:** as três notas linkam `Ciência/SO` (03 Processos, 10 I/O, 11 Sistemas de arquivos) e não reabrem mecanismo. Zero wikilinks quebrados.
- **Ponte para os galhos 1-3 já construída:** a nota 03 amarra o teto de descritores ao `worker_rlimit_nofile` do Nginx 13 e ao contrato de log de container do Docker.

## Bloco 2 — o que ficou decidido ao escrever

- **A nota 04 apoia-se num achado que quase nenhum material trata como central:** apagar um arquivo depende do `w` **do diretório**, não do arquivo. Ele explica os dois enigmas da abertura e justifica o sticky bit em `/tmp` — e é o tipo de fato que muda o que a pessoa faz diante de um "permissão negada".
- **`namei -l` entrou como ferramenta de diagnóstico de permissão**, no lugar do reflexo `chmod 777`. A armadilha correspondente diz isso explicitamente.
- **A nota 05 organiza-se por dois enigmas opostos com a mesma aparência** — zumbi e estado `D`, os dois "não morrem" —, e a distinção decide a conduta: no zumbi o alvo é o pai; no `D` o alvo é a camada de baixo, e sinal nenhum resolve.
- **`D` conta no load average** ficou registrado aqui como gancho explícito para a nota 12, que é onde o número é explicado.
- **A cadeia terminal → sessão → grupo** foi apresentada só até onde explica `SIGHUP`, `nohup` e `disown`, cedendo multiplexador a `Tecnologia/Terminal`. A conclusão da nota — *o que precisa sobreviver a você não pertence à sua sessão* — é a ponte narrativa para o systemd.
- **Pontes com os galhos 1-3:** a 05 amarra o problema de zumbi em container ao Docker 08 (PID 1) e ao `--init`; a 04 amarra o `USER` do Dockerfile ao fato de UID 0 no container ser UID 0 no kernel do host.

## Bloco 3 — o que ficou decidido ao escrever

- **A fronteira com `Engenharia/Operação` foi mantida sem esforço**, porque o corte se mostrou natural: aqui é o **modelo de unidades e o contrato do serviço com a máquina**; lá continua sendo a disciplina de operar. Nenhuma das duas notas fala de SLO, alerta ou incidente.
- **A nota 07 é a nota 01 preenchida.** Cada campo de `[Service]` — `User=`, `WorkingDirectory=`, `Environment=`, `LimitNOFILE=` — é um item do contrato de execução, agora declarado em vez de herdado por acidente. Isso amarra o bloco 3 ao bloco 1 e reforça a lente do galho.
- **Duas distinções carregam a nota 06:** `start` × `enable` (agir agora × agir no próximo boot) e `Requires=` × `After=` (dependência × ordem, independentes entre si). A segunda é a origem das corridas de inicialização que só aparecem no boot.
- **"Iniciado" não é "pronto"** ficou registrado como callout de aviso, com a observação de que é o **mesmo problema do `depends_on` do Compose** e tem a mesma solução — `Type=notify` ou aplicação que tolera indisponibilidade e tenta de novo.
- **O contrato de parada é o mesmo do container**, e isso foi dito explicitamente: `SIGTERM` → janela → `SIGKILL`. A nota 07 conclui, como o Docker 08, que aplicação que ignora `SIGTERM` é defeito da aplicação — aumentar o timeout é conviver com perda de dados.
- **`systemd-analyze security` entrou como ferramenta**, junto com as diretivas de endurecimento (`NoNewPrivileges`, `PrivateTmp`, `ProtectSystem`). É o comando mais subestimado do assunto e cabia aqui, não em Operação.

## Bloco 4 — o que ficou decidido ao escrever

- **A nota 08 abre pelo pior caso real e não pelo comando:** o journal volátil, que apaga o log do boot anterior justamente quando a máquina reinicia sozinha. A verificação (`journalctl --list-boots`) entrou como coisa a fazer em toda máquina herdada, antes de precisar.
- **A justificativa do formato binário ficou honesta nos dois sentidos:** o ganho real é guardar registro com **campos confiáveis** preenchidos pelo `journald` (que a aplicação não forja), e o preço real é precisar da ferramenta para ler — daí a convivência legítima com `rsyslog` em máquina crítica.
- **O gancho da nota 03 fechou nas duas direções:** aplicação que não aparece no journal ou escreve em arquivo próprio, ou está bufferizando porque do outro lado não há terminal.
- **A nota 09 organiza-se pelos três defeitos históricos do cron** (ambiente mínimo · saída que vira e-mail descartado · não sabe que a máquina esteve desligada) e mostra o timer resolvendo os três. O argumento mais forte não é sintaxe: é que **a execução vira um objeto do sistema**, com estado conhecido — daí não haver execução sobreposta e ser possível disparar o trabalho à mão com o contrato real.
- **Registrado com honestidade quando o cron ainda é a escolha certa:** máquina sem `systemd`, container enxuto, tarefa pessoal simples. E que, em container, a resposta melhor costuma ser nenhum dos dois, e sim o agendador da plataforma — ponte para o Kubernetes 11.
- **`systemd-analyze calendar` entrou como o recurso que o cron não tem:** testar a expressão sem esperar o horário.

## Bloco 5 — o que ficou decidido ao escrever

- **Fase Adepto fechada (06-11).** A máquina está configurada, supervisionada, com log consultável, tarefas agendadas, rede compreendida e software com procedência.
- **A nota 10 abre pelo achado que mais economiza tempo real:** "funciona local e ninguém alcança" quase nunca é firewall — é a aplicação escutando em `127.0.0.1`. `ss -tlnp` responde numa coluna, antes de qualquer regra. A escada de diagnóstico (loopback → interface → de fora) elimina uma camada por vez e evita a conversa errada com quem administra a rede.
- **A armadilha do `dig` foi tratada como estrutural, não como dica:** `dig` e `nslookup` ignoram `/etc/hosts` e `nsswitch.conf`; a aplicação não. `getent hosts` é o que reproduz o caminho dela, e a divergência entre os dois **é** o achado. É a origem da maior parte da falha intermitente de nome.
- **Fronteira com `Ciência/Redes` mantida sem esforço:** protocolo (TCP, DNS, TLS) é lá; aqui é sempre *esta máquina* — que endereços tem, por onde sai, o que escuta, como resolve. SSH entrou só como ferramenta de acesso, conforme o design previa.
- **A nota 11 troca a pergunta "como instalo" por "daqui a dois anos, alguém vai saber de onde isto veio?"** — e abre com o binário órfão em `/usr/local/bin` que nenhum `dpkg -S` reconhece. O gerenciador de pacotes é apresentado como **banco de dados**, com as consultas (`-S`, `-L`, `policy`) em primeiro plano, não os verbos de instalação.
- **Dois mal-entendidos corrigidos explicitamente:** `apt update` não atualiza software, e versão antiga em distribuição estável **não** significa sem correção, por causa do retroporte.
- **Ponte com Docker construída pelo argumento, não por link solto:** a imagem é a resposta de outra natureza ao mesmo problema de procedência, e é por isso que fixar versão da base em vez de `latest` é a mesma pergunta noutro lugar.

## Bloco 6 — o que ficou decidido ao escrever

- **A dívida da nota 05 foi paga com destaque:** em Linux o load average inclui estado `D`, e por isso não mede CPU. A nota 12 transforma isso num diagrama de decisão (load alto → o que `vmstat`/`mpstat` dizem → CPU, espera por I/O, ou I/O travado) em vez de deixar como curiosidade.
- **O checklist de Gregg entrou como espinha, e o método USE como o que o sustenta.** A pergunta que mais diferencia é a de **saturação**: utilização em 100% pode ser aproveitamento bom; o que dói é fila. Isso prepara a crítica ao `%util` na nota 13.
- **Registrado que tudo é `/proc` formatado**, com os arquivos equivalentes — porque `sysstat` frequentemente não está instalado em container ou máquina enxuta, e instalar durante incidente nem sempre é opção.
- **A nota 13 organiza-se por "o número que engana × o número que decide"**, um par por eixo. Os quatro: `%iowait` (é CPU ociosa, não disco lento) · `free` (o certo é `available`) · `%util` (perdeu sentido em NVMe; o par é `await` + `aqu-sz`) · banda (raramente é o limite; erro e retransmissão sim).
- **`%steal` ganhou tratamento próprio** e um caso trabalhado inteiro, porque é a coluna que quase ninguém olha e a única que aponta para **fora da máquina** — nenhuma otimização local resolve, e a conclusão é trocar de instância ou acionar o provedor.
- **Armadilha registrada contra `drop_caches`** como "liberar memória" em produção.

## Bloco 7 e fechamento — o que ficou decidido

- **A nota 14 dá o atalho de diagnóstico que fecha o caso mais rápido:** término sem erro no log da aplicação **é** informação, porque `SIGKILL` não é entregue ao processo — e **código de saída 137** (`128 + 9`) identifica morte forçada de imediato. Separa OOM **do sistema** de OOM **de cgroup**, que é a confusão que faz alguém olhar `free` no host e concluir que memória não era o problema.
- **A ponte com Kubernetes 17 é pelo mecanismo:** `oom_score_adj` é o mesmo dos dois lados — aqui a máquina, lá quem o configura por classe de QoS.
- **A nota 15 trata o custo do `strace` como parte do conteúdo**, não como nota de rodapé: `-c` antes de saída completa, recorte com `-e trace=`, `timeout`, e eBPF nomeado como o caminho para observação contínua. Também registra que **silêncio sob `strace` é informação** — o problema é interno ao processo, e a ferramenta certa passa a ser do ecossistema da linguagem.
- **O capstone é uma investigação com hipóteses descartadas**, não um resumo: três eliminações (OOM/hardware, disco/memória, enxurrada de requisições) antes do achado, e a causa num lugar diferente do sintoma — lentidão na aplicação, causa numa recarga de configuração dela, dano no banco. Fecha separando **contenção** de **correção**, com o aviso de que parar na primeira é o que faz o incidente voltar.
- **Fechamento completo em 2026-08-16:** `Linux.md` podado de 1118 para 198 linhas com mapa de redirecionamento (seções de entrevista preservadas, como nos três galhos anteriores) · `index.md` reformado como MOC por fase, com referência e fronteiras · callout de ponte na referência de comandos · **callouts de volta inseridos em `Ciência/SO` 02, 03, 07 e 11**, que passaram a ter contraparte operacional.

## M1 — mídia (rodada de 2026-08-16)

**9 de 16 notas com vídeo embutido e verificado.** Transcrições lidas antes de embutir, conforme a regra do domínio.

| Nota | Vídeo | ID | Canal | Idioma |
|---|---|---|---|---|
| 02 | Linux File System/Structure Explained | `HbgzrKJvDRw` | DorianDotSlash, 16 min | EN |
| 03 | What's behind a file descriptor? I/O redirection with `dup2` | `rW_NV6rf0rM` | Chris Kanich, 20 min | EN |
| 04 | Understanding File & Directory Permissions | `4e669hSjaX8` | Learn Linux TV, 36 min | EN |
| 05 | KILL Linux processes (also manage them) | `LfC6pv8VISk` | NetworkChuck, 22 min | EN |
| 06 | systemd on Linux 1: Intro and Unit Files | `N1vgvhiyq0E` | tutoriaLinux, 14 min | EN |
| 09 | Automate Your Tasks with systemd Timers | `n6BuUgkZ5T0` | Learn Linux TV, 33 min | EN |
| 11 | Linux Packaging Formats explained | `1lLZ-59xH3Y` | The Linux Experiment, 20 min | EN |
| 12 | Linux Performance Tools | `FJW8nGV4jxY` | **Brendan Gregg**, 54 min | EN |
| 15 | Entendendo e utilizando o strace no Linux | `G-HpLitxpXc` | **LINUXtips**, 10 min | **PT-BR** |

> [!success] Duas inserções que valem registro
> **Nota 12 é fonte primária:** quem apresenta é o autor do checklist e do método USE. O trecho mais valioso não são as ferramentas, e sim o **método do enunciado do problema** — perguntar o que "lento" significa e como se quantifica, antes de qualquer comando —, que corresponde exatamente à abertura da nota. O vídeo de 72 segundos do mesmo autor, que é literalmente o checklist, ficou **citado dentro do callout** em vez de embutido, por estar abaixo do piso de duração.
>
> **Nota 15 é PT-BR e corrige o vídeo:** o LINUXtips nomeia o `ptrace` como mecanismo, o que amarra ao callout de `ptrace_scope` da nota. Mas apresenta `-r` como "quanto tempo cada chamada levou" — `-r` são carimbos **relativos entre** chamadas; quem mede o tempo **dentro** de cada uma é `-T`. A precisão ficou registrada no próprio callout.

### Notas sem vídeo, e por quê

| Nota | Situação |
|---|---|
| 01 — O contrato de execução | Ainda sem rodada de busca própria; o recorte é conceitual e pode não ter equivalente direto |
| 07 — Escrever um serviço | Ainda sem rodada |
| 08 — journald | Ainda sem rodada |
| 10 — A máquina na rede | `vDWY3PuHMX8` (Akamai, 94 mil views) foi lido e **reprovado**: começa em `ip addr` e deriva para uso de `curl`, sem tratar rotas, endereço de escuta ou resolução de nomes — o núcleo da nota |
| 13 — Os quatro eixos | Melhores resultados com 121, 73, 449 e 35 visualizações. Sem candidato à altura |
| 14 — OOM killer | O material bom é longo demais (`ql1axx--8sI`, Linux Foundation, 96 min, acima do teto) ou tem audiência baixa demais |
| 16 — Capstone | Ainda sem rodada |

## Pendências

- **M1:** completar as 7 notas restantes. Passada posterior, `yt-dlp` central. **Expectativa de yield alto** — Linux tem material de conferência e canais de autoridade em abundância, ao contrário do que ocorreu com configuração de Nginx. E o ângulo **PT-BR** já se provou no domínio (nota 01 do Docker), então entra desde a primeira rodada.

## Lacunas conscientes (do design)

Scripting em Bash (merece galho próprio em Terminal) · SSH (fica como ferramenta de acesso na nota 10) · SELinux/AppArmor (possível broto).
