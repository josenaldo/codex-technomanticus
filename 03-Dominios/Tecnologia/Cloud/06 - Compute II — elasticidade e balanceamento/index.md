---
title: "Cloud — Compute II: elasticidade e balanceamento"
created: 2026-07-23
updated: 2026-07-23
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
aliases:
  - "Compute II — elasticidade e balanceamento"
  - "Galho 6 - Compute II"
---

# Compute II — elasticidade e balanceamento

> [!abstract] TL;DR
> Galho 6 da trilha Cloud, Bloco 2 (Os primitivos): de uma instância única para uma frota que se auto-cura e se auto-ajusta ao tráfego. Por que uma instância não basta (escala horizontal vs vertical), o balanceador de carga como porta de entrada (ALB L7 vs NLB L4, DO LB), health checks que tiram a instância doente do rodízio, Auto Scaling Groups que substituem e multiplicam instâncias sozinhos, as políticas que decidem quando escalar, e a arquitetura elástica de ponta a ponta multi-AZ que costura tudo. 6 notas, 3 fases, lente dupla AWS ↔ DigitalOcean.

## Sobre este galho

O Galho 5 entregou a máquina virtual como primitivo e terminou num impasse: uma instância única, por maior que seja, tem teto e é ponto único de falha. Este galho resolve esse impasse com a virada central da computação em nuvem — não se cuida de uma instância como bicho de estimação; sobem-se muitas instâncias iguais e descartáveis atrás de um balanceador, e deixa-se a plataforma ajustar o número sozinha conforme o tráfego.

O fio condutor monta a arquitetura peça por peça: primeiro *por que* precisamos de mais de uma (o teto da escala vertical), depois a *porta de entrada* que distribui tráfego (o load balancer), depois como o sistema *sabe que uma instância morreu* (health checks), depois o componente que *multiplica e cura* a frota (Auto Scaling Group), depois *como ele decide* quando mudar o número (políticas de escala), e por fim a *arquitetura de referência completa* — DNS → LB multi-AZ → ASG multi-AZ → instâncias stateless → estado externalizado — que aguenta um pico de Black Friday sem intervenção humana e sobrevive à queda de uma zona inteira.

**Audiência primária:** quem já sabe provisionar uma VM (Galho 5) e agora precisa fazê-la escalar e resistir a falha. **Audiência secundária:** quem já usa auto scaling mas nunca formalizou por que o serviço escala tarde demais, por que fica oscilando (flapping), ou por que uma instância travada continua recebendo tráfego.

> [!info] Fronteira
> O **conceito abstrato** de balanceamento de carga (o que é, algoritmos, camada 4 vs camada 7 como teoria) vive em [[03-Dominios/Engenharia/Arquitetura/index|System Design]] e [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]]. Este galho mostra a **encarnação gerenciada** desses conceitos na nuvem (ELB da AWS, DO Load Balancer) e linka de volta — não os reensina. A **disciplina de operar** essa frota em produção (deploy, SLO, incident response) vive em [[03-Dominios/Engenharia/Operação/index|Operação]].

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/06 - Compute II — elasticidade e balanceamento/01 - Por que uma instância não basta|01 — Por que uma instância não basta]] — escala horizontal vs vertical, o teto e o ponto único de falha, o balanceador como porta de entrada, o pré-requisito de statelessness.

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/06 - Compute II — elasticidade e balanceamento/02 - Balanceamento de carga na nuvem|02 — Balanceamento de carga na nuvem]] — ALB (L7) vs NLB (L4), DO Load Balancer, target groups, listeners, algoritmos, sticky sessions, terminação TLS.
3. [[03-Dominios/Tecnologia/Cloud/06 - Compute II — elasticidade e balanceamento/03 - Health checks|03 — Health checks]] — interval/timeout/thresholds, health check do LB vs do ASG, connection draining, liveness vs readiness.
4. [[03-Dominios/Tecnologia/Cloud/06 - Compute II — elasticidade e balanceamento/04 - Auto Scaling Groups|04 — Auto Scaling Groups]] — desired/min/max, self-healing, launch template, distribuição multi-AZ, instance refresh.
5. [[03-Dominios/Tecnologia/Cloud/06 - Compute II — elasticidade e balanceamento/05 - Políticas de escala|05 — Políticas de escala]] — target tracking, step, scheduled, escolha de métrica, cooldown/warmup e flapping.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/06 - Compute II — elasticidade e balanceamento/06 - Arquitetura elástica de ponta a ponta|06 — Arquitetura elástica de ponta a ponta]] — DNS → LB → ASG → instâncias stateless → estado externalizado, alta disponibilidade multi-AZ, custo vs resiliência. Capstone do galho e ponte para a rede (VPC).

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — cada nota adiciona uma peça da arquitetura elástica, e a nota 06 monta o todo.

### Já uso auto scaling, quero fechar as lacunas de fato

03 (por que uma instância travada ainda recebe tráfego, e como os thresholds decidem quando ela sai) → 05 (por que o serviço escala tarde ou fica em flapping) → 06 (por que uma frota num datacenter só não é alta disponibilidade de verdade).

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Cloud/06 - Compute II — elasticidade e balanceamento" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/index|Compute I — máquinas virtuais]] — Galho 5, a instância única que este galho aprende a multiplicar
- [[03-Dominios/Tecnologia/Cloud/02 - Anatomia de um provedor/index|Anatomia de um provedor]] — Galho 2, de onde vêm as regions e availability zones que a alta disponibilidade deste galho usa
- [[03-Dominios/Engenharia/Arquitetura/index|System Design]] — os conceitos abstratos de balanceamento, escala e alta disponibilidade que este galho encarna
- [[03-Dominios/Engenharia/Operação/index|Operação (DevOps/SRE)]] — a disciplina de operar em produção a frota elástica que este galho monta
