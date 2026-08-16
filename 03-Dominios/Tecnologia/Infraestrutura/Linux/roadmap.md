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
| 10 | A máquina na rede | Adepto | 📋 desenhada | 5 |
| 11 | Software instalado | Adepto | 📋 desenhada | 5 |
| 12 | Diagnóstico: os primeiros sessenta segundos | Magus | 📋 desenhada | 6 |
| 13 | CPU, memória, disco e I/O, um de cada vez | Magus | 📋 desenhada | 6 |
| 14 | Quando o processo some: OOM killer e limites | Magus | 📋 desenhada | 7 |
| 15 | Ver o que o processo pede ao kernel | Magus | 📋 desenhada | 7 |
| 16 | Capstone — a máquina que ficou lenta às três da manhã | Magus | 📋 desenhada | 7 |

## Outros arquivos do galho

| Arquivo | Tipo | Estado |
|---|---|---|
| `index.md` | MOC | ⬜ reformar no fechamento (hoje descreve o galho antigo, de 1 nota) |
| `Comandos para entender agentes.md` | reference | ➖ **mantido como referência do galho**, com recorte próprio. Decisão de 2026-08-12: não dissolver nas notas novas — mesmo tratamento do `GitHub CLI.md` em Controle de Versão. Falta o callout de ponte |
| `Infraestrutura/Linux.md` (1118 linhas) | monólito-semente | ⬜ podar no fechamento, como Docker.md, Kubernetes.md e Nginx.md |

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

## Pendências

- **Blocos 5-7** (notas 10-16), com pergunta ao usuário a cada bloco.
- **Fechamento:** podar `Linux.md`, reformar `index.md`, callout de ponte na referência de comandos, callouts de volta em `Ciência/SO` e `Operação`.
- **M1 (mídia):** passada posterior, `yt-dlp` central. **Expectativa de yield alto** — Linux tem material de conferência e canais de autoridade em abundância, ao contrário do que ocorreu com configuração de Nginx.

## Lacunas conscientes (do design)

Scripting em Bash (merece galho próprio em Terminal) · SSH (fica como ferramenta de acesso na nota 10) · SELinux/AppArmor (possível broto).
