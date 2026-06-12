---
title: "A JVM dentro de um container"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - cloud-native
  - iniciado
  - container
aliases:
  - "JVM container-aware"
  - "Container-awareness"
---

# A JVM dentro de um container

> [!abstract] TL;DR
> Por padrão (desde o **Java 10**), a JVM é **container-aware**: a flag `-XX:+UseContainerSupport` faz ela ler os limites de RAM e CPU do **cgroup** em vez de enxergar a máquina inteira. Em vez de fixar o heap com `-Xmx`, prefira `-XX:MaxRAMPercentage` (default **25.0**) — assim o heap é **relativo** ao limite do container e acompanha o redeploy. `-Xmx` fixo **tem precedência** sobre os percentuais e por isso é frágil: se o limite do container encolher, o heap não encolhe junto e você toma **OOM-kill**.

## O que é

**Container-awareness** é a capacidade da JVM de descobrir, em tempo de execução, **quanta memória e quanta CPU ela realmente pode usar** quando roda dentro de um container (Docker, Kubernetes, etc.) — e não quanto a máquina física oferece.

A analogia: imagine alguém que sempre dimensionou seus móveis pelo tamanho da casa inteira, sem saber que mora num quarto alugado dentro dela. Mais cedo ou mais tarde compra um sofá que não cabe pela porta. A JVM antiga era esse inquilino: lia `/proc/meminfo` e via toda a RAM do host. A JVM **container-aware** finalmente lê o tamanho do quarto onde mora — o limite do cgroup — e mobília de acordo.

O mecanismo concreto é o **cgroup** (control group), o recurso do kernel Linux que o runtime de container usa para impor limites. A JVM lê esse pseudo-filesystem do cgroup e ajusta seus defaults a partir dele.

## Por que importa

Antes da container-awareness, uma JVM num container com limite de 512 MB ainda achava que tinha, digamos, 16 GB (a RAM do host). Ela calculava heap, número de threads de GC e pools internos com base nesse número errado. Resultado: a JVM tentava crescer além do limite, o kernel via o processo ultrapassar o teto do cgroup e o **matava** (OOM-kill) — sem stack trace Java, sem aviso elegante, só um pod reiniciando em loop.

Em ambiente cloud-native isso é o caso comum, não a exceção: todo pod do Kubernetes roda com `resources.limits`. Dimensionar a JVM corretamente dentro desse envelope é o que separa um serviço estável de um `CrashLoopBackOff` misterioso.

## Como funciona

### UseContainerSupport e o cgroup

`-XX:+UseContainerSupport` está **ligada por padrão desde o Java 10**. Com ela, a JVM lê do cgroup:

- o **limite de memória** do container (em vez da RAM do host);
- o **limite de CPU** (quotas/shares), que vira o número de processadores "visíveis".

O kernel garante, via cgroup, que nenhum processo ultrapasse esses limites. A JVM apenas **lê** esses tetos e usa como base para seus cálculos. Se você quiser desligar (raríssimo), `-XX:-UseContainerSupport` volta ao comportamento antigo de enxergar o host.

> [!info] cgroup v1 vs v2
> Existem duas gerações da API de cgroup. O suporte da JVM a **cgroup v2** chegou no **JDK 17** (e foi backportado para **11.0.16+** e **8u372+**). Hosts modernos tendem a ser **cgroup-v2-only**. JDKs anteriores a esses só entendem cgroup v1 — num host v2-only eles **não detectam o container** e voltam a enxergar a memória do host.

### MaxRAMPercentage vs -Xmx fixo

Em vez de cravar o heap com um valor absoluto (`-Xmx512m`), a abordagem container-aware é dimensionar o heap como **percentual do limite do container**:

- `-XX:MaxRAMPercentage` — teto do heap como % da RAM disponível. **Default: 25.0** (ou seja, 25% do limite).
- `-XX:InitialRAMPercentage` — heap inicial como %. Default baixo (1.5625%).
- `-XX:MinRAMPercentage` — apesar do nome, controla o percentual quando a memória total é **pequena**. Default: 50.0.

A vantagem: se o limite do container mudar no redeploy (de 512 MB para 1 GB, por exemplo), o heap **acompanha automaticamente**, porque é relativo.

> [!warning] Precedência
> `-Xmx` (e `-Xms`) **têm precedência** sobre os percentuais. Se você passar `-Xmx` fixo, os `*RAMPercentage` são **ignorados**. É por isso que misturar os dois sem querer é uma fonte clássica de confusão: o percentual "não funciona" porque há um `-Xmx` esquecido em algum lugar.

O **detalhe do default 25%**: é conservador. Num container de 1 GB, o heap padrão fica em ~256 MB — sobra muito para metaspace, threads, buffers nativos e o próprio overhead da JVM. Em produção é comum subir esse percentual (ex.: 50–75%), medindo antes.

> [!note] Fronteira com o Galho 3
> O que acontece **dentro** do heap — como o GC organiza e recicla a memória, gerações, coletores — é assunto do [[03-Dominios/Java/JVM/03 - Garbage Collection — o conceito|Garbage Collection (Galho 3)]]. Aqui o foco é só **quanto** heap a JVM se concede a partir do limite do container, não **como** ela o gerencia por dentro.

### ActiveProcessorCount e a CPU

Memória não é o único limite que a JVM lê do cgroup. O **número de CPUs** detectado influencia o tamanho do pool de threads do GC, do common pool do `ForkJoinPool`, e de várias heurísticas internas.

`-XX:ActiveProcessorCount=N` permite **cravar manualmente** quantos cores a JVM deve assumir, ignorando a heurística de detecção. Útil quando as quotas de CPU do container são fracionárias (ex.: `cpu: "1500m"` no Kubernetes) e a detecção automática arredonda de um jeito que não te agrada.

## Na prática

Flags típicas de uma JVM container-aware (domínio neutro, um serviço HTTP qualquer):

```bash
java \
  -XX:MaxRAMPercentage=75.0 \
  -XX:InitialRAMPercentage=50.0 \
  -XX:ActiveProcessorCount=2 \
  -jar app.jar
```

E o lado do Kubernetes, definindo o "quarto" que a JVM vai ler via cgroup:

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "2"
```

Aqui a JVM lê o `limits.memory` de **1Gi** e, com `MaxRAMPercentage=75.0`, se concede ~768 MB de heap. Se amanhã o limite virar `2Gi`, o heap reescala sozinho — nenhuma flag precisa mudar. Esse é o ganho de usar percentual em vez de `-Xmx` fixo.

## Armadilhas

### (1) `-Xmx` fixo num container com limite menor → OOM-kill

Você definiu `-Xmx1g` na imagem. Meses depois, alguém aperta o `limits.memory` do pod para `512Mi` para economizar. A JVM **ignora** o cgroup para o heap (porque `-Xmx` tem precedência) e tenta crescer até 1 GB. O kernel vê o processo passar de 512 Mi e dá **OOM-kill** — sem exceção Java, sem stack trace, só o pod reiniciando. Pior: o `-Xmx` fixo **não acompanha o redeploy**. A correção é trocar o valor fixo por `-XX:MaxRAMPercentage`, que é relativo ao limite e reescala automaticamente.

### (2) JDK antigo em host cgroup-v2-only → usa a memória do host

Você roda uma imagem com um JDK anterior ao **11.0.16 / 17 / 8u372** num cluster moderno, que é **cgroup-v2-only**. Esse JDK só entende cgroup v1; em host v2 ele **não detecta o container** e volta a enxergar toda a RAM do host. Com `MaxRAMPercentage=25%` calculado sobre, digamos, 64 GB do nó, a JVM se concede 16 GB de heap dentro de um pod de 1 GB — e morre na primeira alocação séria. A correção é **subir o JDK** para uma versão com suporte a cgroup v2.

## Em entrevista

### Frase pronta (inglês)

> Since Java 10, the JVM is container-aware by default through `-XX:+UseContainerSupport`, so it reads memory and CPU limits from the cgroup instead of the host. Rather than pinning a fixed `-Xmx`, I prefer `-XX:MaxRAMPercentage`, which sizes the heap relative to the container limit and automatically rescales on redeploy. A fixed `-Xmx` is fragile because it takes precedence over the percentage flags and doesn't follow a shrinking limit, which leads straight to an OOM-kill with no Java stack trace.

### Vocabulário

| Português | Inglês |
| --- | --- |
| consciência de container | container-awareness |
| grupo de controle | cgroup (control group) |
| limite de memória | memory limit |
| percentual de RAM | RAM percentage |
| heap | heap |
| morte por falta de memória | OOM-kill |
| precedência | precedence |
| reescalar no redeploy | rescale on redeploy |

## Veja também

- [[03-Dominios/Java/Cloud-native e produção/01 - Production-ready e cloud-native — a tese honesta|Production-ready e cloud-native]]
- [[03-Dominios/Java/Cloud-native e produção/11 - Config e recursos no Kubernetes|Config e recursos no Kubernetes]]
- [[03-Dominios/Java/JVM/03 - Garbage Collection — o conceito|Garbage Collection (Galho 3)]]
- [[03-Dominios/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

A observabilidade dessa JVM em produção (métricas de heap, GC, OOM) é tema do **Galho 18 — Observabilidade (planejado)**.

## Referências

- Red Hat Developers — *Java 17: What's new in OpenJDK's container awareness* (2022). https://developers.redhat.com/articles/2022/04/19/java-17-whats-new-openjdks-container-awareness
