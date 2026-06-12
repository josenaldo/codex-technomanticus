---
title: "A JVM — o que é e o pipeline de execução"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - jvm
  - iniciado
  - runtime
aliases:
  - "JVM"
  - "Java Virtual Machine"
  - "Pipeline de execução Java"
---

# A JVM — o que é e o pipeline de execução

> [!abstract] TL;DR
> A JVM (*Java Virtual Machine*) é o runtime que executa bytecode — ela interpreta as instruções primeiro e, conforme detecta código executado com frequência (*hot spots*), compila esse trecho para código nativo via JIT. É o mecanismo que torna Java portátil: o mesmo `.class` roda em qualquer sistema que tenha uma JVM. Entender o pipeline (não tratar a JVM como caixa preta) é o que diferencia dev sênior de pleno em entrevistas e em debugging de produção.

## O que é

A JVM é uma máquina virtual de pilha (*stack-based virtual machine*) que carrega, verifica e executa bytecode Java. Ela isola o programa do sistema operacional subjacente — código compilado uma vez roda em qualquer plataforma que tenha uma JVM compatível (*write once, run anywhere*).

### JVM, JRE e JDK — a distinção

| Componente | O que inclui | Para quem |
|------------|-------------|-----------|
| **JVM** | Motor de execução (interpretador + JIT + GC + classloader) | Base de tudo |
| **JRE** | JVM + bibliotecas padrão (rt.jar até o Java 8; módulos desde o 9) | Apenas rodar aplicações |
| **JDK** | JRE + ferramentas de desenvolvimento (`javac`, `javap`, `jshell`, `jmap`, `jstack`…) | Desenvolver e depurar |

> O JRE como distribuição separada foi descontinuado a partir do Java 11 (OpenJDK / Oracle). Hoje distribui-se apenas o JDK completo — mas a distinção conceitual permanece e aparece em entrevistas.

### Implementações de referência

- **HotSpot** — implementação de referência, mantida pela Oracle como parte do **OpenJDK** (open source). É o que você usa por padrão ao instalar qualquer distribuição OpenJDK (Temurin, Amazon Corretto, Microsoft Build of OpenJDK etc.).
- **Eclipse OpenJ9** — implementação alternativa mantida pela Eclipse Foundation, focada em menor footprint de memória e startup rápido. Presente no IBM Semeru.
- **GraalVM** — distribui o HotSpot + compilador GraalVM (que pode substituir C2) e suporta *native image* (compilação AOT), removendo a JVM do runtime. Compilação AOT e *native image* são tema do [[03-Dominios/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|Galho 17 (GraalVM Native Image)]] — aqui apenas registramos que a opção existe.

## Por que importa

Tratar a JVM como caixa preta é suficiente para escrever código. Não é suficiente para:

- **Entrevistas de sênior** — perguntas sobre pipeline de execução, por que Java não é "lento", como o GC impacta latência, ou o que é um *classloader* aparecem regularmente em ciclos de entrevista para posições internacionais.
- **Debugging de produção** — entender onde o código "vive" (heap, stack, metaspace) e como o JIT decide o que compilar é pré-requisito para interpretar traces de `jstack`, `jmap`, ou ferramentas de APM como Datadog e Dynatrace.
- **Tuning de performance** — escolher o GC certo, ajustar flags de JIT, entender tiered compilation afeta diretamente SLAs em sistemas de alta carga.

## Como funciona

### De `.java` a `.class` — `javac` e o bytecode

O compilador `javac` transforma código-fonte (`.java`) em **bytecode** (`.class`). Bytecode não é código de máquina nativo — é um conjunto de instruções para a JVM, independente de arquitetura. Isso é o que garante portabilidade: o mesmo `.class` roda no Linux x86-64, no macOS ARM e no Windows sem recompilação.

```text
Fonte (.java)
     │
     ▼  javac
Bytecode (.class)  ← instrução-set da JVM, não da CPU
     │
     ▼  JVM
  Execução
```

O bytecode pode ser inspecionado com `javap -c` (tema da [[04 - Bytecode por dentro — anatomia e javap]]).

### Pipeline completo

```text
Código-fonte (.java)
        │
        ▼  javac
  Bytecode (.class)
        │
        ▼  ClassLoader
  Carga + Verificação
  (bytecode verifier)
        │
        ▼
  Interpretador
  (execução linha a linha)
        │
        ├──── código frio → permanece interpretado
        │
        └──── código quente (hot spot detectado)
                    │
                    ▼  JIT Compiler (C1 → C2)
             Código nativo (otimizado)
                    │
                    ▼
              CPU executa
```

Ao mesmo tempo, o **GC** gerencia o ciclo de vida dos objetos no heap — é um serviço contínuo do runtime, não uma etapa do pipeline de startup.

### Carga e verificação — classloader + bytecode verifier (visão geral)

Antes de executar qualquer bytecode, a JVM precisa carregar a classe e verificar que o bytecode é válido e seguro. Esse processo usa uma hierarquia com três classloaders encadeados no HotSpot:

```text
Bootstrap ClassLoader    ← carrega java.lang.*, java.util.*, módulos core
        ↓
Platform ClassLoader     ← carrega APIs do Java SE (módulos de plataforma)
        ↓
System/Application ClassLoader  ← carrega classes da aplicação (classpath / module path)
```

A regra é *parent delegation*: cada classloader pergunta ao pai antes de tentar carregar por conta própria. Isso evita que código de aplicação substitua classes de sistema. O **bytecode verifier** valida estrutura do arquivo `.class`, consistência de tipos, e controle de acesso antes de qualquer execução.

Detalhe de classloading e delegation model: ver [[05 - Classloading e o delegation model]].

### Interpretação e JIT (visão geral)

A JVM HotSpot começa **interpretando** o bytecode — traduz e executa instrução por instrução. Paralelamente, monitora quais métodos e loops são executados com frequência. Quando um trecho atinge o limiar de "quente" (*hot*), o **compilador JIT** entra em ação e compila esse trecho para código nativo da CPU, que passa a ser executado diretamente.

O HotSpot tem dois compiladores JIT:

- **C1** (*client compiler*) — compilação rápida com otimizações leves; reduz latência de startup.
- **C2** (*server compiler*) — compilação mais agressiva e lenta; gera código mais otimizado para código que roda muito.

A estratégia padrão é **tiered compilation** (desde Java 7, padrão no Java 8+): o código passa por C1 primeiro e, se continuar quente, é recompilado por C2. Resultado: startup razoável *e* throughput alto em regime.

Detalhe de JIT, C1/C2 e tiered compilation: ver [[07 - JIT — C1, C2 e tiered compilation]].

### GC como serviço do runtime (visão geral)

O **Garbage Collector** gerencia o ciclo de vida dos objetos no heap — aloca e libera memória de forma automática. Ele não é uma etapa sequencial do pipeline: roda concorrentemente (ou em pausas curtas, dependendo do GC) ao longo de toda a vida da aplicação.

O HotSpot oferece múltiplos coletores (`G1` é o padrão desde Java 9, `ZGC` e `Shenandoah` visam pausas sub-milissegundo). A escolha impacta diretamente latência e throughput.

Conceito e motivação do GC: ver [[03 - Garbage Collection — o conceito]]. Áreas de memória (heap, stack, metaspace): ver [[02 - Áreas de memória de runtime]].

## Na prática

### Compilar e rodar um arquivo Java

```bash
# Compilar
javac Order.java

# Executar
java Order
```

```text
Order created: #1001 for customer Alice — total: R$450.00
```

Arquivo `Order.java`:

```java
public class Order {
    private final int id;
    private final String customer;
    private final double total;

    public Order(int id, String customer, double total) {
        this.id = id;
        this.customer = customer;
        this.total = total;
    }

    @Override
    public String toString() {
        return "Order created: #" + id + " for customer " + customer
               + " — total: R$" + String.format("%.2f", total);
    }

    public static void main(String[] args) {
        Order order = new Order(1001, "Alice", 450.00);
        System.out.println(order);
    }
}
```

### O que `java -version` revela

```bash
java -version
```

```text
openjdk version "21.0.3" 2024-04-16
OpenJDK Runtime Environment Temurin-21.0.3+9 (build 21.0.3+9)
OpenJDK 64-Bit Server VM Temurin-21.0.3+9 (build 21.0.3+9, mixed mode, sharing)
```

- **openjdk version "21.0.3"** — versão de lançamento + patch.
- **OpenJDK Runtime Environment Temurin** — distribuição (Adoptium Temurin neste caso).
- **mixed mode** — JVM rodando em tiered compilation: interpreta *e* compila via JIT (C1 + C2).
- **sharing** — Class Data Sharing (CDS) ativo: metadados de classes do bootstrap são pré-carregados de um arquivo compartilhado, acelerando startup.

### Primeiro contato com `javap -c`

```bash
javap -c Order.class
```

```text
public java.lang.String toString();
  Code:
     0: new           #7   // class java/lang/StringBuilder
     3: dup
     4: invokespecial #13  // Method java/lang/StringBuilder."<init>":()V
     7: ldc           #14  // String "Order created: #"
     9: invokevirtual #16  // Method java/lang/StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;
    ...
```

Cada linha é uma instrução de bytecode. `new`, `dup`, `invokespecial`, `ldc`, `invokevirtual` são opcodes da JVM — não instruções de CPU. O JIT decide quais desses trechos merecem compilação nativa. Para entender o bytecode em detalhe, ver [[04 - Bytecode por dentro — anatomia e javap]].

## Armadilhas

### (1) "Java é interpretado, logo é lento"

**O problema:** é uma meia-verdade que persiste desde os anos 90. Na época, Java era de fato quase puramente interpretado. Hoje, o HotSpot com tiered compilation compila código quente para instruções nativas da CPU com otimizações agressivas — inlining, escape analysis, eliminação de alocações etc. Benchmarks modernos (JMH) mostram que código Java quente pode ser comparável ou superar C++ não otimizado.

```bash
# Confirmar que JIT está ativo (mixed mode)
java -version 2>&1 | grep "mixed mode"
```

```text
OpenJDK 64-Bit Server VM ... (build 21.0.3+9, mixed mode, sharing)
```

**Fix:** a afirmação correta é "Java tem overhead de warmup". Após o JIT aquecer (~alguns milhares de invocações), o código compilado roda nativo. Para contextos de startup crítico (serverless, CLI), considerar GraalVM native image ([[03-Dominios/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|Galho 17]]). Para mais detalhes do JIT: ver [[07 - JIT — C1, C2 e tiered compilation]].

---

### (2) Assumir que toda JVM se comporta igual

**O problema:** vendors e versões divergem em defaults de GC, limites de heap, flags de JIT, e comportamento de classloading. Um tuning que funciona no HotSpot da Temurin 21 pode não produzir o mesmo resultado no OpenJ9 da IBM Semeru ou em versões mais antigas.

```bash
# Ver TODOS os flags efetivos da JVM atual
java -XX:+PrintFlagsFinal -version 2>&1 | grep -E "UseG1GC|TieredCompilation|MaxHeapSize"
```

```text
     bool TieredCompilation                       = true    {pd product} {default}
     bool UseG1GC                                 = true    {product} {ergonomic}
 size_t MaxHeapSize                               = 4294967296 {product} {ergonomic}
```

**Fix:** nunca assumir defaults — sempre conferir com `-XX:+PrintFlagsFinal`. Ao migrar entre vendors ou versões, revisar os flags críticos de GC e JIT explicitamente.

## Em entrevista

### Frase pronta (inglês)

> "The JVM is the runtime engine that loads, verifies, and executes Java bytecode. It's what makes Java platform-independent — you compile once to bytecode and run anywhere a JVM exists. HotSpot, the reference implementation, starts by interpreting bytecode and uses tiered compilation to detect hot spots and compile them to native machine code via C1 and C2 JIT compilers, which means the trade-off is startup overhead in exchange for very high throughput at steady state. The GC runs as a continuous runtime service managing heap memory, so the choice of collector — G1, ZGC, Shenandoah — directly impacts latency guarantees. The caveat for senior-level decisions is that JVM behavior differs across vendors and versions: defaults for GC, JIT thresholds, and heap sizing vary, so you should always validate effective flags with `-XX:+PrintFlagsFinal` rather than assuming cross-vendor consistency."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| máquina virtual Java | Java Virtual Machine (JVM) |
| bytecode | bytecode |
| compilação JIT | JIT compilation / just-in-time compilation |
| código quente / ponto quente | hot spot / hot code |
| compilação em camadas | tiered compilation |
| carregador de classes | classloader |
| coletor de lixo / coleta de lixo | garbage collector / garbage collection |
| interpretador | interpreter |
| compilação AOT (antes do tempo) | ahead-of-time compilation (AOT) |
| imagem nativa | native image |
| aquecimento da JVM | JVM warmup |
| modo misto | mixed mode |

## Veja também

- [[02 - Áreas de memória de runtime]]
- [[03 - Garbage Collection — o conceito]]
- [[04 - Bytecode por dentro — anatomia e javap]]
- [[05 - Classloading e o delegation model]]
- [[07 - JIT — C1, C2 e tiered compilation]]
- [[03-Dominios/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#bytecode|bytecode (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#JIT (C1 / C2)|JIT (Dicionário)]]

## Referências

- [Getting Started with Java — dev.java](https://dev.java/learn/getting-started/)
- [Java Virtual Machine Technology Overview — Oracle Docs (Java 21)](https://docs.oracle.com/en/java/javase/21/vm/java-virtual-machine-technology-overview.html)
- [ClassLoader — Java 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ClassLoader.html)
- [Compiler Control — Oracle Docs (Java 21)](https://docs.oracle.com/en/java/javase/21/vm/compiler-control1.html)
