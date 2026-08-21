---
title: "Cloud — Compute I: máquinas virtuais"
created: 2026-07-23
updated: 2026-07-23
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
aliases:
  - "Compute I — máquinas virtuais"
  - "Galho 5 - Compute I"
---

# Compute I — máquinas virtuais

> [!abstract] TL;DR
> Galho 5 da trilha Cloud, abertura do Bloco 2 (Os primitivos): a máquina virtual como o primeiro primitivo concreto que se aluga na nuvem. O que é uma instância (hipervisor, control plane vs a instância), como escolher tamanho e perfil (tipos e famílias), como uma instância vazia vira útil (imagens/AMIs, user data, cloud-init), o que sobrevive entre nascer e morrer (ciclo de vida, efêmero vs persistente), como se paga por ela (on-demand/reserved/spot), e por que uma VM única cuidada à mão não é como se opera compute de verdade — a ponte para elasticidade. 6 notas, 3 fases, lente dupla AWS (EC2) ↔ DigitalOcean (Droplet).

## Sobre este galho

Os Galhos 1-4 deram modelo mental, mecânica de provedor, bússola arquitetural e o perímetro de identidade. Este galho entrega o primeiro **primitivo** que você aluga e opera: a máquina virtual. É a base concreta sobre a qual containers, funções serverless e bancos gerenciados acabam rodando — entender a VM é entender o chão de todo o resto.

O fio condutor vai do concreto ao arquitetural: primeiro *o que a coisa é* (uma fatia de um servidor físico, entregue como recurso alugável), depois *como dimensioná-la e provisioná-la* (perfil de recurso, imagem, bootstrap no boot), depois *o que acontece com ela ao longo do tempo e do dinheiro* (ciclo de vida, o que persiste, o que se paga), e por fim *por que operá-la à mão não escala* — fechando na virada mental que abre o Galho 6 (Compute II): não se cuida de uma instância como bicho de estimação; sobem-se muitas instâncias iguais, descartáveis, atrás de um balanceador que as ajusta sozinho.

**Audiência primária:** quem já tem a mecânica de conta/geografia (Galho 2) e a lente de segurança/identidade (Galhos 3-4) e agora precisa provisionar e operar compute de fato. **Audiência secundária:** quem já sobe instâncias no dia a dia mas nunca formalizou a diferença entre `stop` e `terminate`, por que a fatura veio maior do que o esperado, ou por que "só reiniciar a instância" não é como arquiteturas sérias se recuperam de falha.

> [!info] Fronteiras
> A **disciplina de operar** compute em produção (deploy, SRE, incident response) vive em [[03-Dominios/Engenharia/Operação/index|Operação]]. Os **conceitos abstratos** de balanceamento, escala e estado externalizado vivem em [[03-Dominios/Engenharia/Arquitetura/index|System Design]]. Este galho mostra a *encarnação gerenciada* desses conceitos na nuvem e linka de volta — não os reensina.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/01 - Anatomia de uma máquina virtual na nuvem|01 — Anatomia de uma máquina virtual na nuvem]] — hipervisor, instância como recurso alugável, EC2 ↔ Droplet, por que a VM continua sendo o primitivo base.
2. [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/02 - Tipos e famílias de instância|02 — Tipos e famílias de instância]] — vCPU/RAM/rede, famílias (general/compute/memory/storage/GPU), a nomenclatura EC2 decodificada, right-sizing.

## Adepto

3. [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/03 - Imagens, AMIs e provisionamento no boot|03 — Imagens, AMIs e provisionamento no boot]] — AMI/Snapshot, user data e cloud-init, golden image vs bootstrap no boot.
4. [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/04 - Ciclo de vida de uma instância|04 — Ciclo de vida de uma instância]] — estados, stop vs hibernate vs terminate, armazenamento efêmero vs persistente, o que se paga em cada estado.
5. [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/05 - Modelos de preço (on-demand, reserved, spot)|05 — Modelos de preço: on-demand, reserved e spot]] — o eixo do compromisso, RI vs Savings Plan, spot e a interrupção de 2 min, a ponte FinOps.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/06 - Padrões de uso e o caminho para a elasticidade|06 — Padrões de uso e o caminho para a elasticidade]] — cattle vs pets, infraestrutura imutável, estado externalizado, design tolerante a spot, o teto da escala vertical. Capstone do galho e ponte para o Compute II.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear recomendado — cada nota resolve o problema que a anterior deixou em aberto (a instância vazia → como provisioná-la → o que sobrevive → o que custa → por que operá-la à mão não escala).

### Já subo instâncias, quero fechar as lacunas de fato

04 (a diferença entre `stop`/`hibernate`/`terminate` e o que persiste é a raiz de quase toda perda de dado e susto de fatura) → 05 (por que a mesma instância custa 3x mais ou menos) → 06 (por que "só reiniciar a instância" não é como se recupera de falha de verdade).

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Identidade e acesso (IAM)]] — Galho 4, o perímetro que protege este compute
- [[03-Dominios/Engenharia/Arquitetura/index|System Design]] — os conceitos abstratos de escala e balanceamento que o Compute II encarna
- [[03-Dominios/Engenharia/Operação/index|Operação (DevOps/SRE)]] — a disciplina de operar em produção o que este galho provisiona
