---
title: "Flags, ergonomics e a JVM em containers"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - jvm
  - adepto
  - tuning
  - containers
aliases:
  - "Flags da JVM"
  - "JVM em containers"
  - "Ergonomics"
  - "MaxRAMPercentage"
---

# Flags, ergonomics e a JVM em containers

> [!abstract] TL;DR
> As flags `-X` e `-XX` são o painel de controle da JVM: definem heap, stack, Metaspace, coletor e centenas de outros parâmetros. **Ergonomics** é o mecanismo pelo qual a JVM deriva defaults inteligentes a partir do hardware detectado — ou, em container, a partir dos cgroups lidos via `UseContainerSupport` (habilitado por padrão no Linux). O erro clássico em K8s é fixar `-Xmx` colado no limite de memória do pod, sem folga para Metaspace, threads nativas e overhead da JVM: o processo ultrapassa o limite do cgroup e o kernel mata o pod com exit code 137 (OOMKill), que **não é** um `OutOfMemoryError` da JVM. `PrintFlagsFinal` revela o valor efetivo de toda flag após ergonomics e overrides — é a fonte da verdade antes de escalar qualquer investigação.

## O que é

Flags de JVM são os parâmetros de linha de comando que controlam o comportamento da JVM antes da aplicação sequer começar a rodar. Existem três categorias principais:

- **Flags padrão** (`-D`, `-verbose`, etc.) — portáveis entre implementações de JVM.
- **Flags `-X`** (Extra options) — específicas do HotSpot, estáveis o suficiente para uso em produção, mas sem garantia de portabilidade entre todos os JDKs. Exemplos: `-Xmx`, `-Xms`, `-Xss`.
- **Flags `-XX`** (Advanced options) — opções avançadas voltadas para tuning e diagnóstico. São divididas em dois subtipos pela sintaxe:
  - **Boolean**: `-XX:+NomeFlag` (habilita) / `-XX:-NomeFlag` (desabilita).
  - **Valor**: `-XX:NomeFlag=valor` (numérico, string ou tamanho com sufixo `k`/`m`/`g`).

**Ergonomics** é o processo pelo qual a JVM seleciona defaults derivados do ambiente de execução — número de CPUs, RAM disponível, tipo de máquina — reduzindo a quantidade de tuning manual necessária. A Oracle define ergonomics como *"o processo pelo qual a JVM e as heurísticas de GC melhoram a performance da aplicação"* (GC Tuning Guide, Java 21).

## Por que importa

Em produção, 90% do trabalho de tuning de JVM resume-se a três questões:

1. **Quanto heap o pod pode usar?** — o valor errado causa OOMKill (kernel) ou desperdício de RAM paga.
2. **Qual é o default que a JVM aplicou?** — ergonomics pode ter escolhido algo diferente do esperado.
3. **Qual flag está realmente ativa?** — layers de imagem Docker, variáveis de ambiente e scripts de startup se sobrepõem de formas não óbvias.

Errar qualquer uma dessas questões tem efeitos diretos e mensuráveis: pods reiniciando com exit code 137, SLA de latência estourado por GC pause inesperado, ou bills de cloud inflados por RAM subutilizada. Flags e ergonomics não são detalhe de configuração — são a camada de operação da JVM.

## Como funciona

### Anatomia de flag (-Xmx4g vs -XX:MaxHeapSize=4g; boolean vs valor)

`-Xmx` e `-XX:MaxHeapSize` são **aliases** — ambos definem o mesmo parâmetro interno. A forma `-X` é a sintaxe legada estável; a forma `-XX:` é a canônica interna. Quando `PrintFlagsFinal` é usado, o nome mostrado é sempre o nome interno (`MaxHeapSize`).

```bash
# Equivalentes — definem o mesmo parâmetro:
java -Xmx4g -jar app.jar
java -XX:MaxHeapSize=4g -jar app.jar

# Boolean: + habilita, - desabilita
java -XX:+UseG1GC          # habilita G1
java -XX:-UseContainerSupport  # desabilita container support

# Valor numérico com sufixo de unidade
java -XX:MaxRAMPercentage=75.0   # double
java -XX:G1HeapRegionSize=8m     # tamanho com sufixo
```

A distinção importa ao ler logs e ao pesquisar documentação: um blog pode citar `-Xmx` enquanto o `jcmd VM.flags` mostra `MaxHeapSize`.

### Dimensionamento de memória

As flags de memória mais usadas em produção:

| Flag | Alias `-X` | O que controla | Observação |
|------|-----------|---------------|------------|
| `-XX:InitialHeapSize` | `-Xms` | Heap inicial | Se igual a `-Xmx`, JVM não cresce o heap |
| `-XX:MaxHeapSize` | `-Xmx` | Heap máximo | Não inclui Metaspace, stacks, off-heap |
| `-XX:ThreadStackSize` | `-Xss` | Stack por thread | Default: 1024 KB (Linux/x64), 2048 KB (Aarch64) |
| `-XX:MetaspaceSize` | — | High-water mark do Metaspace | **Não é alocação inicial** — é o limiar que dispara GC de Metaspace |
| `-XX:MaxMetaspaceSize` | — | Teto absoluto do Metaspace | Sem limite por default (cresce até OS limit) |

> [!warning] MetaspaceSize ≠ alocação inicial
> `-XX:MetaspaceSize=256m` **não** pré-aloca 256 MB de Metaspace. Ele define o limiar a partir do qual a JVM começa a fazer GC de classes. A alocação real de Metaspace cresce conforme classes são carregadas, independente desse valor.

### Ergonomics

Na ausência de flags explícitas, a JVM deriva defaults do hardware:

- **Coletor de GC**: G1 em máquinas *server-class* (≥ 2 processadores **e** ≥ 1792 MB de RAM); Serial nos demais. (fonte: Oracle GC Tuning Guide, Java 21)
- **Heap inicial**: 1/64 da memória física disponível. (fonte: Oracle GC Tuning Guide, Java 21)
- **Heap máximo**: 1/4 da memória física disponível. (fonte: Oracle GC Tuning Guide, Java 21)
- **Threads de GC**: derivado do número de CPUs disponíveis.
- **Compilador JIT**: tiered (C1 + C2) por padrão.

Em uma máquina de 16 GB, ergonomics daria heap inicial de ~256 MB e heap máximo de ~4 GB sem nenhuma flag explícita.

### Container awareness (cgroups e UseContainerSupport)

Antes do Java 10 (JDK-8146115; backportado pro 8u191), a JVM enxergava a memória da máquina host inteira, não o limite do cgroup do container — resultado: ergonomics superdimensionava o heap, o processo estourava o limite do pod e o kernel matava o container.

A solução foi `UseContainerSupport`:

> *"The VM now provides automatic container detection support, which allows the VM to determine the amount of memory and number of processors that are available to a Java process running in docker containers. It uses this information to allocate system resources. The default for this flag is `true`, and container support is enabled by default."* (Java 21 man page)

Com `UseContainerSupport=true` (default no Linux), a JVM lê os cgroups e usa a memória e CPUs **do container** como referência para ergonomics, não as do host.

Sobre `MaxRAMPercentage` e `InitialRAMPercentage`: estas flags permitem definir o heap máximo e inicial como percentual da RAM disponível (conforme detectada — host ou container). A ergonomics default de 1/4 de RAM para heap máximo corresponde a ~25%; `MaxRAMPercentage` permite ajustar esse percentual explicitamente sem fixar um valor absoluto em bytes.

> [!note] Hedge sobre defaults dos *RAMPercentage
> Os valores numéricos default de `MaxRAMPercentage` e `InitialRAMPercentage` **não foram encontrados explicitamente** na man page do Java 21 nem no GC Tuning Guide durante a pesquisa desta nota. A Oracle confirma o comportamento ergonômico de 1/4 de RAM para heap máximo e 1/64 para heap inicial, mas não expõe esses defaults como valores de `*RAMPercentage` na documentação acessada. Use `java -XX:+PrintFlagsFinal -version | grep -i RAMPercentage` no seu JDK para ver os defaults reais do ambiente.

### Descobrindo a verdade (PrintFlagsFinal, PrintCommandLineFlags, jcmd)

A única forma confiável de saber o que a JVM está usando — depois de ergonomics, overrides e layers de imagem — é perguntar à JVM:

```bash
# Imprime TODOS os flags com seus valores efetivos (após ergonomics + overrides)
# Útil para verificar qualquer flag antes de colocar em produção
java -XX:+PrintFlagsFinal -version 2>&1 | grep -i maxheapsize

# Imprime apenas os flags que apareceram na linha de comando
# (ergonomicamente selecionados ou explícitos) — mais conciso
java -XX:+PrintCommandLineFlags -version

# Em processo já em execução (sem reiniciar)
jcmd <pid> VM.flags
```

A Oracle documenta `-XX:+PrintCommandLineFlags` como: *"Enables printing of ergonomically selected JVM flags that appeared on the command line. It can be useful to know the ergonomic values set by the JVM, such as the heap space size and the selected garbage collector."* (Java 21 man page)

## Na prática

Cenário hipotético: pod K8s com `resources.limits.memory: 2Gi`.

### Opção A — -Xmx fixo (frágil)

```bash
# // hipotético: pod com limits.memory: 2Gi
java -Xmx1536m -jar app.jar
```

Funciona, mas exige recalcular o valor toda vez que o limite do pod mudar. Se alguém ajusta o pod para `3Gi` e esquece de ajustar `-Xmx`, a JVM continua usando 1536 MB enquanto 1,5 GB fica ocioso.

### Opção B — MaxRAMPercentage (escala com o pod)

```bash
# // hipotético: pod com limits.memory: 2Gi
# Heap máximo = 75% de 2 GiB = ~1536 MB
# Restante (~512 MB) cobre Metaspace, stacks nativas, off-heap, overhead da JVM
java -XX:MaxRAMPercentage=75.0 -XX:InitialRAMPercentage=50.0 -jar app.jar
```

Com `UseContainerSupport` ativo (default), a JVM lê o limite do cgroup (`2Gi`) e calcula o heap máximo como 75% desse valor. Se o pod for redimensionado para `4Gi`, o heap escala automaticamente para ~3 GB sem alterar a flag.

### Verificando o heap efetivo

```bash
# // hipotético: verificando o que a JVM calculou com MaxRAMPercentage=75.0 num container de 2Gi
java -XX:MaxRAMPercentage=75.0 -XX:+PrintFlagsFinal -version 2>&1 | grep -i maxheapsize
```

```text
   size_t MaxHeapSize = 1610612736   {product} {ergonomic}
```

`1610612736` bytes = 1536 MB = 75% de 2048 MB. O sufixo `{ergonomic}` confirma que o valor foi calculado — não foi um `-Xmx` explícito.

## Armadilhas

### (1) -Xmx = limite do pod → OOMKill silencioso

**O problema:** definir `-Xmx` igual ao `limits.memory` do pod é o erro mais comum em containerização de Java. O heap da JVM não é a única coisa que consome memória no processo: Metaspace (classes carregadas), stacks nativas de threads, buffers off-heap (NIO, Netty), overhead interno da JVM e bibliotecas nativas também consomem. Quando a soma ultrapassa o limite do cgroup, o kernel OOM killer mata o processo com **exit code 137**.

```bash
# // hipotético: pod com limits.memory: 2Gi
# ERRADO — não sobra memória para nada além do heap
java -Xmx2g -jar app.jar
# Resultado: o processo ultrapassa 2 GiB assim que Metaspace + stacks crescem
# O kernel mata o pod: exit code 137
# O pod reinicia sem nenhum OutOfMemoryError da JVM nos logs — diagnóstico confuso
```

**O que distingue OOMKill de OOM da JVM:** `OutOfMemoryError` na JVM tem stack trace nos logs da aplicação; OOMKill do kernel **não gera nenhum log na JVM** — só aparece como reinicialização do pod com exit code 137 ou no `kubectl describe pod` como `OOMKilled: true`.

**Fix:** deixe pelo menos 25–30% de folga entre `-Xmx` e o limite do pod. Com `MaxRAMPercentage=75.0`, os 25% restantes cobrem Metaspace e overhead.

---

### (2) Confiar no default de RAM em container dedicado

**O problema:** com `UseContainerSupport` ativo e sem flag de heap explícita, a ergonomics usa ~25% da memória do container como heap máximo (conforme o padrão de 1/4 de RAM documentado pela Oracle). Em um pod dedicado com `limits.memory: 4Gi`, isso resulta em ~1 GB de heap — enquanto 3 GB ficam ociosos. A aplicação pode sofrer GC frequente por heap subdimensionado mesmo tendo RAM paga disponível.

```bash
# // hipotético: pod dedicado com limits.memory: 4Gi, sem flag de heap
java -jar app.jar
# Ergonomics → heap máximo ≈ 1 GiB (≈25% de 4 GiB)
# 3 GiB ficam sem uso; GC pode ser frequente desnecessariamente
```

**Fix:** em pods dedicados, defina `MaxRAMPercentage` explicitamente:

```bash
java -XX:MaxRAMPercentage=75.0 -jar app.jar
# Heap máximo ≈ 3 GiB; 1 GiB de folga para Metaspace e overhead
```

---

### (3) Copiar flag de outra versão de JDK → JVM não sobe

**O problema:** flags são adicionadas, modificadas e **removidas** entre versões de JDK. Uma flag desconhecida não é ignorada com warning — ela causa erro fatal de inicialização:

```bash
# Exemplo: flag removida ou inexistente na versão alvo
$ java -XX:+CMSClassUnloadingEnabled -jar app.jar
Unrecognized VM option 'CMSClassUnloadingEnabled'
Error: Could not create the Java Virtual Machine.
Error: A fatal exception has occurred. Program will exit.
```

O deploy falha antes da aplicação sequer tentar subir. Pior: a flag problemática pode estar enterrada num `JAVA_OPTS` herdado de Dockerfile de outra equipe ou de uma versão anterior.

**Fix:** ao migrar de versão de JDK, valide todas as flags contra a versão de destino:

```bash
# Lista todas as flags que o JDK atual reconhece
java -XX:+PrintFlagsFinal -version 2>&1 | grep NomeDaFlag

# Se não aparecer nada, a flag não existe neste JDK — remova ou substitua
```

Trate cada flag de JVM copiada da internet ou de config legada como suspeita até confirmar que existe — e faz o que o blog dizia — na versão específica em uso.

## Em entrevista

### Frase pronta (inglês)

> "JVM flags fall into two main categories: the `-X` extra options, which are HotSpot-specific but stable enough for production, and the `-XX` advanced options, which are used for tuning and diagnostics. Boolean `-XX` flags use plus or minus to toggle them, while value flags use an equals sign. Ergonomics is the JVM's mechanism for picking sensible defaults from the environment — G1 on server-class machines, an initial heap of one sixty-fourth and a maximum heap of one quarter of physical memory, and so on."

> "In containerized environments, the critical flag is `UseContainerSupport`, which is on by default on Linux. With it enabled, the JVM reads the cgroup limits instead of the host's total memory, so ergonomics sizes the heap against the pod's memory limit rather than the node's. The classic mistake is setting `-Xmx` equal to the pod's memory limit and leaving no room for Metaspace, thread stacks, and native overhead — the kernel OOM killer then terminates the process with exit code 137, which shows up as a pod restart with no OutOfMemoryError in the Java logs."

> "Before tuning anything, I always run `java -XX:+PrintFlagsFinal -version` to see the effective value of every flag after ergonomics and any overrides. It removes guesswork about what the JVM is actually using, especially when flags come from multiple sources — Dockerfile, environment variables, and startup scripts can all override each other in non-obvious ways."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| ergonomia da JVM | JVM ergonomics |
| flag booleana | boolean flag |
| limite de memória do pod | pod memory limit |
| suporte a container | container support |
| grupo de controle | cgroup (control group) |
| morte por falta de memória (kernel) | OOMKill / OOM killer |
| percentual de RAM máximo | max RAM percentage |
| valor efetivo da flag | effective flag value |

## Veja também

- [[02 - Áreas de memória de runtime]]
- [[06 - Os coletores do HotSpot]]
- [[10 - GC logs — unified logging e leitura]]
- [[11 - Tuning de GC — metodologia e prática]]
- [[12 - Diagnóstico — heap dumps, thread dumps e jcmd]]
- [[03-Dominios/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#ergonomics (JVM)|ergonomics (Dicionário)]]

## Referências

- [Java 21 man page — Extra and Advanced Runtime Options](https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html#advanced-runtime-options-for-java) — confirma: `UseContainerSupport` default `true` no Linux; `-XX:+PrintCommandLineFlags` imprime flags ergonômicas; sintaxe `-X`/`-XX`; `-Xss` defaults por plataforma
- [GC Tuning Guide, Ergonomics — Java 21](https://docs.oracle.com/en/java/javase/21/gctuning/ergonomics.html) — confirma: heap inicial = 1/64 da RAM física; heap máximo = 1/4 da RAM física; G1 em server-class machines (≥ 2 CPUs, ≥ 1792 MB); definição de ergonomics
- [VM Options Explorer — OpenJDK 21 (chriswhocodes.com)](https://chriswhocodes.com/hotspot_options_openjdk21.html) — referência de flags por versão; `InitialRAMPercentage` default reportado como 1.5625
