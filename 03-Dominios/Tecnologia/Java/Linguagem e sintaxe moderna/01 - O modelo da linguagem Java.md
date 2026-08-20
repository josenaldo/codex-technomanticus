---
title: "O modelo da linguagem Java"
created: 2026-06-02
updated: 2026-06-02
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - linguagem
  - iniciado
  - jvm
  - fundamentos
aliases:
  - Modelo Java
  - WORA
---

# O modelo da linguagem Java

> [!abstract] TL;DR
> Java = orientada a objetos, estaticamente e fortemente tipada, compilada para bytecode, garbage-collected, e portátil via JVM (Write Once, Run Anywhere). O código-fonte `.java` vira bytecode `.class` independente de plataforma; a JVM de cada sistema operacional executa esse bytecode — via interpretação inicial e JIT em seguida.

## O que é

Java é uma linguagem **orientada a objetos**, **fortemente e estaticamente tipada**, **compilada para bytecode** e **garbage-collected**. Foi criada em 1995 por James Gosling e sua equipe na Sun Microsystems (adquirida pela Oracle em 2010), com o princípio central de **"Write Once, Run Anywhere"** (WORA): o mesmo bytecode roda em qualquer plataforma que tenha uma JVM compatível.

### Onde Java domina hoje

- **Enterprise/backend**: sistemas financeiros, ERP, servidores de aplicação (WildFly, WebLogic, WebSphere), stack Spring Boot
- **Microserviços**: Quarkus, Micronaut, Helidon — frameworks nativos à nuvem baseados em Java/JVM
- **Big data**: Hadoop MapReduce, Apache Spark, Apache Kafka — todos escritos em Java/Scala sobre a JVM
- **Android legado**: até o surgimento do Kotlin (2017) como linguagem oficial, Android era Java puro; o ecossistema ainda carrega décadas de código Java

## Por que importa

Para um desenvolvedor sênior, dois conceitos são frequentemente confundidos e importantes de distinguir:

### Versão da linguagem vs. versão da JVM/JDK

A **especificação da linguagem Java** (Java Language Specification — JLS) define a sintaxe e semântica do código-fonte. A **JVM** tem sua própria especificação separada (Java Virtual Machine Specification). Ambas evoluem juntas em releases do JDK, mas não são a mesma coisa:

- Um compilador `javac` do JDK 21 pode gerar bytecode alvo de versões anteriores (`--release 17`)
- Código compilado com JDK 11 pode rodar em uma JVM 21 (retrocompatibilidade)
- O inverso geralmente não funciona: bytecode de JDK 21 não roda em JVM 11

### O que LTS significa na prática

Desde Java 9 (setembro de 2017), o Java adotou um ciclo de releases de **6 meses** — uma versão nova a cada março e setembro. Isso resolveu o problema de grandes releases atrasadas (Java 7 demorou 5 anos, Java 8 demorou 3 anos), mas criou um novo desafio: empresas não conseguem migrar a cada 6 meses.

As versões **LTS (Long-Term Support)** respondem a esse desafio. Em vez de suporte de apenas 6 meses, recebem anos de atualizações de segurança e correções:

| Versão | Lançamento       | Tipo |
|--------|-----------------|------|
| Java 8  | Mar 2014        | LTS  |
| Java 11 | Set 2018        | LTS  |
| Java 17 | Set 2021        | LTS  |
| Java 21 | Set 2023        | LTS  |
| Java 25 | Set 2025        | LTS (planejado) |

A cadência LTS é aproximadamente a cada **2 anos** (a cada 4 feature releases). Empresas com sistemas em produção tendem a migrar apenas entre versões LTS, o que significa que Java 17 e Java 21 são as versões mais relevantes para o mercado enterprise atual.

## Como funciona

### Compilação para bytecode

O fluxo de desenvolvimento e execução de um programa Java passa por etapas distintas:

```
Código-fonte         Compilação           Bytecode           Execução
(.java)         ──────────────►         (.class)       ──────────────►  resultado
                   javac                                  JVM (interpreta
                                                          + JIT compila)
```

1. O desenvolvedor escreve código `.java` (texto legível por humanos)
2. `javac` (o compilador do JDK) transforma esse código em **bytecode** — um conjunto de instruções para uma máquina virtual stack-based, armazenado em arquivos `.class`
3. A JVM **carrega** as classes via classloader
4. O **bytecode verifier** valida que o bytecode é seguro (não viola tipagem, não corrompe a pilha de operandos)
5. A JVM **interpreta** o bytecode inicialmente, instrução por instrução
6. O **compilador JIT (Just-In-Time)** identifica os "hot paths" — trechos executados com frequência — e os compila para código nativo otimizado para a arquitetura da máquina atual (x86, ARM etc.)

Exemplo: este método Java simples:

```java
public int somar(int a, int b) {
    return a + b;
}
```

Compila para bytecode inspecionável com `javap -c`:

```text
public int somar(int, int);
  Code:
     0: iload_1      // empilha parâmetro a
     1: iload_2      // empilha parâmetro b
     2: iadd         // desempilha os dois, soma, empilha resultado
     3: ireturn      // retorna o topo da pilha
```

A JVM é **stack-based**: operações trabalham sobre uma pilha de operandos, não diretamente em registradores. Isso simplifica o bytecode e o torna independente da arquitetura da CPU.

### Write Once, Run Anywhere

O papel da JVM é ser uma **camada de portabilidade**: o mesmo arquivo `.class` roda em qualquer sistema operacional que tenha uma JVM compatível instalada. A JVM é que conhece os detalhes do sistema operacional e da CPU — o bytecode não.

```
Mesmo bytecode (.class)
        │
        ├──► JVM para Linux/x86     ──► código nativo Linux/x86
        │
        ├──► JVM para macOS/ARM     ──► código nativo macOS/ARM
        │
        └──► JVM para Windows/x86   ──► código nativo Windows/x86
```

O contrato é: desde que a JVM implemente a especificação corretamente, o comportamento do programa é idêntico em todas as plataformas. Na prática, há edge cases (formatos de path, comportamento de `File`, encoding padrão), mas o princípio se sustenta para a grande maioria dos programas.

### JDK vs JRE vs JVM

Três termos que aparecem juntos e causam confusão:

| Componente | O que contém | Quem usa |
|------------|--------------|---------|
| **JVM** (Java Virtual Machine) | Engine de execução: classloader, bytecode verifier, interpreter, JIT compiler, garbage collector | Parte de todos os outros |
| **JRE** (Java Runtime Environment) | JVM + bibliotecas de classe padrão (java.lang, java.util etc.) | Usuário final que só executa apps Java (praticamente extinto desde Java 9+) |
| **JDK** (Java Development Kit) | JRE + ferramentas de desenvolvimento: `javac`, `javap`, `jshell`, `jpackage`, `jlink`, profilers | Desenvolvedor |

> Desde Java 9, o JRE standalone foi descontinuado como distribuição separada. O desenvolvedor instala o JDK; o usuário final geralmente recebe um runtime empacotado junto com a aplicação via `jlink` ou `jpackage`.

### Tipagem estática e forte

**Estática** significa que o tipo de cada variável é declarado em tempo de compilação e verificado pelo `javac` antes de o programa rodar:

```java
String nome = "Alice";
nome = 42; // erro em compile-time: incompatible types: int cannot be converted to String
```

**Forte** significa que Java não realiza coerção implícita entre tipos incompatíveis. Não existe a promoção silenciosa de tipos que existe em linguagens como JavaScript ou PHP:

```java
// hipotético: em JavaScript, isso funcionaria silenciosamente
// Em Java, é erro de compilação:
int numero = "10" + 5; // erro: String não é int
```

A única coerção implícita permitida é **widening**: promoção de tipo menor para maior sem perda de informação (ex: `int` → `long`, `float` → `double`). Narrowing (o inverso) exige cast explícito:

```java
long grande = 1_000_000L;
int menor = (int) grande; // cast explícito — pode perder dados
```

A vantagem de tipagem estática e forte é que uma categoria inteira de bugs é detectada pelo compilador, antes de qualquer teste ou execução.

### Releases e LTS

O modelo de release adotado a partir de 2017 (Java 9) separou dois ritmos:

- **Feature releases**: a cada 6 meses (março e setembro). Suporte apenas até a próxima feature release. Úteis para explorar features novas, mas inadequadas para produção enterprise.
- **LTS releases**: a cada ~2 anos (a cada 4 feature releases). Recebem atualizações de segurança e correções críticas por anos — pelo menos 5 anos em distribuições Oracle, e mais em distribuidores como Adoptium (Eclipse Temurin), Amazon Corretto, Azul Zulu.

Na prática, o ecossistema enterprise gravita em torno das versões LTS. Java 17 e Java 21 são as mais adotadas no momento; Java 25 (setembro de 2025) é a próxima LTS planejada.

## Na prática

No ecossistema enterprise, padrão observado em projetos Spring Boot e Jakarta EE:

- A maioria das novas iniciativas usa Java 17 ou Java 21 como baseline mínima, por conta das melhorias de performance do GC, Records, sealed classes e — no caso do 21 — Virtual Threads
- O ciclo de upgrade tende a seguir versões LTS; pular uma LTS (ex: ficar em Java 11 e ir direto para Java 21) é comum em sistemas com maior inércia
- Ferramentas de build (Maven, Gradle) e frameworks (Spring Boot 3.x, Quarkus 3.x) sinalizaram Java 17 como versão mínima suportada, acelerando a migração

Do ponto de vista operacional, uma equipe que mantém aplicações em produção precisa entender a distinção entre o número de versão e o suporte disponível: rodar Java 20 (feature release) em produção significa ficar sem patches de segurança em 6 meses.

## Armadilhas

### (1) Confundir versão da linguagem com versão da JVM/JDK

Um equívoco frequente é tratar "Java 21" como se fosse uma entidade única, quando na realidade envolve ao menos três versões coordenadas: a especificação da linguagem (JLS), a especificação da JVM (JVMS) e o JDK como distribuição de ferramentas.

**O problema manifesta assim:** ao compilar com `--release 17` num JDK 21, o código usa a sintaxe e APIs disponíveis até Java 17, mas o compilador é o do JDK 21. A JVM que vai executar pode ser 17, 21, ou superior — e cada uma tem comportamentos de GC, JIT e desempenho diferentes.

```java
// Compilado com JDK 21, mas target release 17:
// javac --release 17 MeuServico.java
// Isso gera bytecode que roda em JVM 17+, mas sem features de runtime do 21
// (ex: Virtual Threads — que são runtime, não apenas sintaxe)
public class MeuServico {
    public void processar() {
        // Thread.ofVirtual() -- ERRO: API só existe na JVM 21+
        // mesmo compilando com JDK 21 e --release 17
    }
}
```

**Fix:** Distinguir sempre o que é feature de **linguagem** (sintaxe, checada pelo compilador) do que é feature de **runtime** (APIs, comportamento da JVM). Virtual Threads, por exemplo, são runtime — exigem JVM 21, independentemente do `--release` usado.

### (2) Achar que "compilado" significa código nativo (como C/C++)

Em C/C++, "compilar" produz um executável específico para a arquitetura e o OS: um `.exe` para Windows x86 não roda em Linux ARM. Quem vem dessas linguagens pode assumir que Java funciona da mesma forma.

**O problema:** o `javac` não produz código de máquina — produz **bytecode** para a JVM. O código nativo só é gerado **em tempo de execução**, pelo JIT, para os hot paths. Isso tem implicações práticas:

```text
C/C++:
  Fonte (.c)  ──►  gcc  ──►  executável nativo (Windows x86)
                             └─ roda direto na CPU, sem intermediário

Java:
  Fonte (.java)  ──►  javac  ──►  bytecode (.class)  ──►  JVM  ──►  execução
                                  └─ portátil             └─ JIT compila hot paths
                                                             para nativo em runtime
```

Um JAR não é um executável nativo. Ele requer uma JVM instalada para rodar. A vantagem é portabilidade; a desvantagem histórica era tempo de startup (a JVM precisa inicializar, carregar classes, e o JIT precisa "aquecer"). Esse gap está sendo endereçado por GraalVM Native Image (compilação AOT — Ahead-of-Time), mas esse é o comportamento padrão do OpenJDK.

**Fix:** Ao discutir performance, diferenciar: startup frio (JVM boot + JIT warm-up) vs. throughput em regime estável (onde JIT já otimizou os hot paths e Java frequentemente iguala ou supera C++ em benchmarks de servidor).

## Em entrevista

### Frase pronta (inglês)

> "Java compiles source code to platform-independent bytecode, which the JVM then executes — first via interpretation and then through JIT compilation of hot paths into native code for the host architecture. This is what makes WORA work: the same `.class` file runs on any JVM-compliant runtime, whether Linux, macOS, or Windows. The trade-off is that startup latency is higher than natively compiled languages because the JVM needs to initialize and the JIT needs time to warm up, though in long-running server workloads this cost is amortized and throughput becomes comparable."

Use essa resposta quando perguntarem *"How does Java execution work?"*, *"What is the JVM?"* ou *"Explain Write Once Run Anywhere."* Esteja pronto para aprofundar o JIT warm-up, GraalVM Native Image como alternativa AOT, ou a distinção entre JDK/JRE/JVM.

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| máquina virtual | virtual machine (JVM) |
| bytecode | bytecode (inalterado — termo técnico universal) |
| compilação antecipada | ahead-of-time compilation (AOT) |
| compilação em tempo de execução | just-in-time compilation (JIT) |
| coleta de lixo | garbage collection (GC) |
| tipagem estática | static typing |
| tipagem forte | strong typing |
| ampliação de tipo | widening (conversão implícita para tipo maior) |
| estreitamento de tipo | narrowing (conversão explícita para tipo menor — requer cast) |
| caminho quente | hot path (trecho de código compilado pelo JIT) |
| versão de suporte estendido | long-term support release (LTS) |
| kit de desenvolvimento | Java Development Kit (JDK) |

## Veja também

- [[02 - Tipos, variáveis e operadores]]
- [[03 - Estruturas de controle e fluxo]]
- [[15 - A evolução do Java (8 a 25)]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Fundamentals]]
- [[03-Dominios/Tecnologia/Java/Core/Helsinki MOOC - Guia de Revisão|Helsinki MOOC]]

## Referências

- [Java Platform Evolution — dev.java](https://dev.java/evolution/)
- [JDK 21 Documentation — Oracle](https://docs.oracle.com/en/java/javase/21/)
- [Java Version History — Wikipedia](https://en.wikipedia.org/wiki/Java_version_history)
