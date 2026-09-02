---
title: "Linux"
type: moc
publish: true
created: 2026-05-21
updated: 2026-08-16
status: growing
tags:
  - moc
  - linux
  - infraestrutura
aliases:
  - Linux (Infraestrutura)
---

# Linux

> [!abstract] TL;DR
> O quarto e último galho do domínio, e o que fica **por baixo** dos outros três: Docker, Kubernetes e Nginx rodam todos sobre isto. A lente é *o sistema como o processo o vê* — não como o kernel funciona por dentro, que é [[03-Dominios/Ciência/Sistemas Operacionais/index|Ciência/Sistemas Operacionais]], e não a ergonomia do shell, que é [[03-Dominios/Tecnologia/Terminal/index|Terminal]], mas **o que a máquina entrega a cada processo** e como isso é observado, operado e investigado.

A espinha do galho é o **contrato de execução** apresentado na nota 01: identidade, credenciais, descritores, diretório, ambiente, limites e recorte. Cada nota seguinte desenvolve um item desse contrato — e quase todo problema de "funciona aqui e não lá" acaba sendo uma linha dele diferente do que se imaginava.

---

## Iniciado — o sistema visível

| # | Nota | O quê |
|---|------|-------|
| 01 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/01 - O que o Linux entrega a um processo\|O que o Linux entrega a um processo]] | o contrato de execução, e onde lê-lo em `/proc/<pid>/` |
| 02 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/02 - A hierarquia do sistema de arquivos\|A hierarquia do sistema de arquivos]] | FHS, o merge do `/usr`, e `/proc` e `/sys` como janelas do kernel |
| 03 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/03 - Tudo é arquivo - descritores e redirecionamento\|Tudo é arquivo]] | descritores, `2>&1` e a ordem que importa, log de serviço e de container |
| 04 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/04 - Identidade - usuários, grupos e permissão\|Identidade: usuários, grupos e permissão]] | os três UIDs, os nove bits, e por que apagar depende do diretório |
| 05 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/05 - O processo como objeto administrável\|O processo como objeto administrável]] | a árvore, zumbi × estado `D`, sinais, e por que morre ao fechar o terminal |

## Adepto — o sistema operado

| # | Nota | O quê |
|---|------|-------|
| 06 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/06 - systemd - o modelo de unidades\|systemd: o modelo de unidades]] | declarar em vez de sequenciar · `start` × `enable` · `Requires=` × `After=` |
| 07 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/07 - Escrever um serviço que se comporta\|Escrever um serviço que se comporta]] | a unidade comentada · `Type=` · `Restart=` · o contrato de parada |
| 08 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/08 - Logs - journald e o que veio antes\|Logs: journald e o que veio antes]] | por que binário · consultar e reter · o journal volátil |
| 09 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/09 - Agendamento - cron e timers\|Agendamento: cron e timers]] | os três defeitos do cron, e por que o timer venceu |
| 10 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/10 - A máquina na rede\|A máquina na rede]] | endereço de escuta, rotas, resolução de nomes, as três camadas de firewall |
| 11 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/11 - Software instalado\|Software instalado]] | o gerenciador como banco de dados, e por que `curl \| sh` é decisão |

## Magus — o sistema investigado

| # | Nota | O quê |
|---|------|-------|
| 12 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/12 - Diagnóstico - os primeiros sessenta segundos\|Os primeiros sessenta segundos]] | o checklist de Gregg, o método USE, e o load average que não mede CPU |
| 13 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/13 - CPU, memória, disco e I-O, um de cada vez\|CPU, memória, disco e I/O]] | o número que engana × o número que decide, em cada eixo |
| 14 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/14 - Quando o processo some - OOM killer e limites\|Quando o processo some]] | OOM do sistema × de cgroup · código 137 · rlimits |
| 15 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/15 - Ver o que o processo pede ao kernel\|Ver o que o processo pede ao kernel]] | `strace` com recorte, `lsof` sem custo, `dmesg` como testemunha |
| 16 | [[03-Dominios/Tecnologia/Infraestrutura/Linux/16 - Capstone - a máquina que ficou lenta às três da manhã\|Capstone]] | investigação completa, do primeiro `uptime` à decisão |

---

## Referência do galho

- [[03-Dominios/Tecnologia/Infraestrutura/Linux/Comandos para entender agentes|Comandos para entender agentes]] — referência de consulta com recorte próprio (inspecionar agentes e processos), mantida como material de apoio, não dissolvida nas notas acima.

---

## Fronteiras

Este galho **linka** e não reescreve:

- [[03-Dominios/Ciência/Sistemas Operacionais/index|Ciência/Sistemas Operacionais]] — o **mecanismo**: processos, escalonamento, memória virtual, sistemas de arquivos, namespaces e cgroups. Aqui é como isso se manifesta numa máquina que você opera.
- [[03-Dominios/Tecnologia/Terminal/index|Terminal]] — a **ergonomia do shell**: Zsh, prompt, completion, multiplexador, TUIs. Aqui é o sistema por baixo dele.
- [[03-Dominios/Engenharia/Operação/index|Engenharia/Operação]] — o **ofício**: SLO, alerta, incidente, postmortem. Aqui é o instrumento que aquela prática pressupõe.
- [[03-Dominios/Ciência/Redes e Protocolos/index|Ciência/Redes e Protocolos]] — o **protocolo**. Aqui é sempre *esta máquina*.
- [[03-Dominios/Tecnologia/Infraestrutura/Docker/index|Docker]] · [[03-Dominios/Tecnologia/Infraestrutura/Kubernetes/index|Kubernetes]] · [[03-Dominios/Tecnologia/Infraestrutura/Nginx/index|Nginx]] — os três galhos que rodam sobre isto, e que apontam para cá quando o assunto é o sistema por baixo.

## Veja também

- [[03-Dominios/Tecnologia/Infraestrutura/index|Infraestrutura]] — o domínio e o sanduíche de quatro camadas
- [[03-Dominios/Tecnologia/Infraestrutura/Linux|Linux (referência)]] — o guia de origem, hoje com o mapa de redirecionamento e as seções de entrevista
