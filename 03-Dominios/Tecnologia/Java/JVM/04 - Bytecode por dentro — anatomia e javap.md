---
title: "Bytecode por dentro — anatomia e javap"
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
  - bytecode
aliases:
  - "Bytecode"
  - "javap"
  - "Instruções da JVM"
---

# Bytecode por dentro — anatomia e javap

> [!abstract] TL;DR
> Bytecode é o instruction set portátil da JVM: o compilador `javac` traduz código-fonte Java para bytecode, que fica empacotado em arquivos `.class`. Esse arquivo é um contêiner binário estruturado — com magic number `CAFEBABE`, versão, constant pool, métodos e atributos — entendido por qualquer implementação da JVM, em qualquer plataforma. A ferramenta `javap -c -v` é a lupa que desmonta esse binário e torna visível o que o compilador gerou. Lembrete crítico: performance se mede no JIT, não no bytecode — o que você vê no `javap` raramente é o que a JVM de fato executa em produção.

## O que é

**Bytecode** é o conjunto de instruções de baixo nível definido pela especificação da JVM. Diferente do código de máquina nativo (x86, ARM), bytecode não é executado diretamente pelo hardware — é interpretado ou compilado pelo runtime da JVM. Essa separação é o que garante a portabilidade "write once, run anywhere".

O produto da compilação de cada arquivo `.java` é um arquivo `.class`. Esse arquivo é um binário estruturado que o carregador de classes da JVM lê para criar a representação interna da classe em memória.

### Anatomia do `.class`

A estrutura de um arquivo `.class` é definida pela [JVM Specification (§4)](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html):

```text
ClassFile {
    u4   magic;                  // 0xCAFEBABE — identifica um .class válido
    u2   minor_version;          // versão menor (normalmente 0; 65535 = preview)
    u2   major_version;          // 65 = Java 21, 52 = Java 8, 51 = Java 7
    u2   constant_pool_count;
    cp_info  constant_pool[...]; // tabela de constantes simbólicas
    u2   access_flags;           // public, final, interface, abstract...
    u2   this_class;             // índice na constant pool → nome desta classe
    u2   super_class;            // índice → superclasse
    u2   interfaces_count;
    u2   interfaces[...];
    u2   fields_count;
    field_info  fields[...];     // campos declarados
    u2   methods_count;
    method_info methods[...];    // métodos + bytecode de cada um
    u2   attributes_count;
    attribute_info attributes[...]; // SourceFile, InnerClasses, Record...
}
```

**Campos-chave:**

- **magic (`0xCAFEBABE`)** — os primeiros 4 bytes de todo `.class` válido. A JVM rejeita o arquivo imediatamente se esse valor estiver errado.
- **major_version** — indica com qual versão do compilador a classe foi gerada. A JVM lança `UnsupportedClassVersionError` se esse número for maior do que a versão que ela suporta. Java 21 = 65, Java 17 = 61, Java 11 = 55, Java 8 = 52.
- **constant pool** — tabela central de constantes simbólicas (strings, nomes de classe, descritores de método, referências de campo). Quase toda instrução de bytecode referencia a constant pool por índice, não por valor direto.
- **methods** — cada entrada `method_info` aponta para um atributo `Code` que contém o bytecode compilado daquele método, mais tabelas de linha (para stack traces) e variáveis locais.

## Por que importa

### Desmistifica a linguagem

O bytecode revela o que o compilador realmente gera para construções de alto nível:

- Um `record` gera um construtor canônico, métodos acessores (`name()`, `age()`), `equals`, `hashCode` e `toString` — tudo visível via `javap`.
- Uma lambda não vira uma classe anônima compilada: desde Java 8 o compilador emite uma instrução `invokedynamic` que delega a criação da instância funcional para a `LambdaMetafactory` em runtime.
- Concatenação de strings com `+` (a partir do Java 9) não gera mais `StringBuilder` explícito — usa `invokedynamic` com `StringConcatFactory`.

### Ferramenta de debugging de último nível

Quando o comportamento de um trecho de código é surpreendente e nenhuma leitura do fonte esclarece, `javap` pode revelar se o compilador gerou algo inesperado: boxing implícito, cast sintético, bridge methods de genéricos apagados (*type erasure*).

### Relevância em entrevistas

Perguntas sobre bytecode aparecem em entrevistas sênior como sonda de profundidade: "como lambda é implementado?", "o que `invokedynamic` faz?", "por que você pode ter `UnsupportedClassVersionError`?". Não é necessário memorizar opcodes — é necessário entender o modelo.

## Como funciona

### Anatomia do `.class` (constant pool, métodos, atributos)

A **constant pool** é o coração simbólico do arquivo. Ela contém entradas tipadas (tags 1 a 20), entre elas:

| Tag | Tipo | Uso |
|-----|------|-----|
| `CONSTANT_Utf8` (1) | String UTF-8 | Nomes de classe, método, campo, descritores |
| `CONSTANT_Class` (7) | Índice para Utf8 | Referência a uma classe ou interface |
| `CONSTANT_Methodref` (10) | Classe + NameAndType | Chamada de método de classe |
| `CONSTANT_Fieldref` (9) | Classe + NameAndType | Acesso a campo |
| `CONSTANT_String` (8) | Índice para Utf8 | Literal de String |
| `CONSTANT_InvokeDynamic` (18) | Bootstrap + NameAndType | Chamada dinâmica (lambdas, concat) |
| `CONSTANT_MethodHandle` (15) | Referência a método/campo | Usado por lambdas e `MethodHandles` |

As instruções de bytecode são pequenas: um opcode de 1 byte seguido de operandos (geralmente índices na constant pool). Uma chamada como `System.out.println("ok")` no bytecode vira `invokevirtual #N`, onde `#N` é um índice na constant pool que eventualmente resolve para `java/io/PrintStream.println:(Ljava/lang/String;)V`.

### Máquina de pilha (stack-based vs register-based; frame = locals + operand stack)

A JVM é uma **máquina de pilha** (*stack-based machine*), em contraste com máquinas de registradores como x86 e ARM. Não há instruções como "some o registrador R1 com R2" — em vez disso, os operandos são empilhados e as operações os consomem e produzem valores no topo da pilha.

Cada chamada de método cria um **frame** na pilha de execução da thread. O frame contém:

- **Local variable array** — array de slots (cada slot = 1 ou 2 palavras) que armazena parâmetros e variáveis locais. Em métodos de instância, `locals[0]` é sempre `this`.
- **Operand stack** — pilha de operandos usada durante a execução das instruções.
- **Referência para o pool de constantes da classe** — para resolução simbólica em runtime.

O número máximo de slots de locais e de profundidade de pilha é calculado pelo compilador e registrado no atributo `Code` de cada método (`max_locals`, `max_stack`).

### Famílias de instrução (load/store, aritméticas, invoke*, new/getfield)

As instruções da JVM se organizam em famílias pelo prefixo de tipo (`i` = int, `l` = long, `f` = float, `d` = double, `a` = referência):

| Família | Exemplos | O que faz |
|---------|----------|-----------|
| **load** | `iload_1`, `aload_0`, `lload_2` | Empurra variável local para a operand stack |
| **store** | `istore_1`, `astore_2` | Desempilha e armazena em variável local |
| **aritmética** | `iadd`, `isub`, `imul`, `idiv`, `irem` | Opera os dois topos da pilha (int) |
| **conversão** | `i2l`, `i2d`, `l2i` | Converte entre tipos primitivos |
| **comparação/desvio** | `if_icmpeq`, `ifeq`, `goto` | Comparação + salto condicional |
| **invocação** | `invokevirtual`, `invokestatic`, `invokespecial`, `invokeinterface`, `invokedynamic` | Diferentes formas de chamar métodos |
| **objeto/campo** | `new`, `getfield`, `putfield`, `getstatic`, `putstatic` | Criação e acesso a objetos e campos |
| **retorno** | `ireturn`, `areturn`, `lreturn`, `return` | Retorna valor (ou void) do método |
| **pilha** | `dup`, `pop`, `swap` | Manipulação direta da operand stack |

### `invokedynamic` (call site dinâmico; lambdas e String concat moderna)

`invokedynamic` (Java 7+) é a instrução mais versátil do conjunto. Diferente das outras variantes de invocação, ela não resolve o método-alvo em tempo de compilação. Em vez disso, associa ao call site um **bootstrap method** que será chamado uma única vez, na primeira execução, para retornar um `CallSite` — um objeto que encapsula o `MethodHandle` do método de destino.

**Lambdas:** o compilador gera `invokedynamic` cujo bootstrap method é `LambdaMetafactory.metafactory`. Esse design foi escolhido desde o Java 8 em vez de compilar cada lambda para uma classe anônima (alternativa que foi rejeitada), o que permite à JVM escolher e otimizar a estratégia de implementação em runtime via `MethodHandles`. Isso é transparente para o código Java — a implementação completa está em [[03-Dominios/Tecnologia/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais]].

**String concat:** a partir do Java 9, `"Hello " + name` gera `invokedynamic` com bootstrap em `StringConcatFactory`. A JVM escolhe a estratégia de concatenação mais eficiente para a plataforma — não mais `StringBuilder` emitido rigidamente pelo compilador.

### Inspecionando com `javap -c -v`

```bash
# Compilar e inspecionar
javac Order.java
javap -c Order          # bytecode de cada método
javap -v Order          # bytecode + constant pool + metadados completos
javap -c -p Order       # inclui membros privados
javap -s Order          # apenas assinaturas internas (descritores JVM)
```

Flags principais:

| Flag | O que mostra |
|------|-------------|
| `-c` | Bytecode disassemblado de cada método |
| `-v` / `-verbose` | Bytecode + constant pool + `max_stack`, `max_locals`, `flags` |
| `-p` / `-private` | Inclui membros privados e sintéticos |
| `-s` | Descritores internos (ex: `(II)I` para `int sum(int, int)`) |
| `-l` | Tabela de linhas e de variáveis locais |
| `-constants` | Exibe valores de campos `static final` |

## Na prática

### `javap -c` de um método simples

Dada a classe:

```java
public class Order {
    public int sum(int a, int b) {
        return a + b;
    }
}
```

`javap -c Order` produz:

```text
public int sum(int, int);
  Code:
     0: iload_1       // empurra local[1] (parâmetro 'a') na operand stack
     1: iload_2       // empurra local[2] (parâmetro 'b') na operand stack
     2: iadd          // desempilha dois ints, empurra a soma
     3: ireturn       // desempilha o int do topo e retorna ao chamador
```

Observações:
- `local[0]` é `this` (método de instância) — por isso `a` começa em `local[1]`.
- Em um método `static`, `a` seria `local[0]`.
- A instrução `iadd` opera sobre inteiros; para `long` seria `ladd`, para `double`, `dadd`.

### Trecho de `javap -v` mostrando a constant pool

```text
Constant pool:
   #1 = Methodref  #4.#13   // java/lang/Object."<init>":()V
   #2 = Class      #14      // Order
   #3 = Class      #15      // java/lang/Object
   #4 = Utf8       Order
   ...
   #13 = NameAndType #9:#10 // "<init>":()V

public int sum(int, int);
  descriptor: (II)I
  flags: (0x0001) ACC_PUBLIC
  Code:
    stack=2, locals=3, args_size=3
       0: iload_1
       1: iload_2
       2: iadd
       3: ireturn
    LineNumberTable:
      line 3: 0
```

`descriptor: (II)I` é a notação interna da JVM para um método que recebe dois `int` e retorna `int`. `stack=2` diz que a operand stack precisará de no máximo 2 slots; `locals=3` = `this` + `a` + `b`.

### O que um `record` gera

```java
public record Point(int x, int y) {}
```

`javap -p Point` mostra o que o compilador gerou:

```text
public final class Point extends java.lang.Record {
  private final int x;
  private final int y;
  public Point(int, int);          // construtor canônico
  public int x();                  // accessor x
  public int y();                  // accessor y
  public final java.lang.String toString();
  public final int hashCode();
  public final boolean equals(java.lang.Object);
}
```

Nenhum campo `name` ou lógica extra — o compilador gerou tudo a partir da declaração do record. A semântica completa de records está em [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/13 - Records e record patterns|Records]].

## Armadilhas

### (1) "Otimizar" lendo bytecode — o JIT reescreve tudo

**O problema:** ao ver bytecode verboso no `javap`, é tentador concluir que o código é "lento" e tentar reescrever o fonte para reduzir instruções. Esse raciocínio ignora o JIT: o compilador just-in-time do HotSpot (C2 especialmente) inlina métodos, elimina alocações (*escape analysis*), reordena instruções e produz código nativo que pode ser radicalmente diferente do bytecode. Um loop simples com bytecode "feio" pode ser vetorizado pelo JIT e rodar mais rápido do que código "limpo" sem inlining.

```java
// O bytecode desta soma pode parecer mais longo que o esperado
// (boxing, checagens de null), mas o JIT elimina tudo em hot paths
int total = items.stream().mapToInt(Item::value).sum();
```

**Fix:** meça com [JMH](https://github.com/openjdk/jmh) (ver nota [[07 - JIT — C1, C2 e tiered compilation]]). Bytecode é o ponto de partida do JIT, não o destino final.

---

### (2) Confundir `major version` com versão da linguagem

**O problema:** o campo `major_version` do `.class` indica com qual versão da plataforma o arquivo foi compilado. É fácil compilar acidentalmente com o JDK instalado e depois tentar rodar em um servidor com JRE mais antigo, obtendo:

```text
Exception in thread "main" java.lang.UnsupportedClassVersionError:
    Order has been compiled by a more recent version of the Java Runtime
    (class file version 65.0), this version of the Java Runtime only
    recognizes class file versions up to 55.0
```

`65.0` = Java 21; `55.0` = Java 11. A JVM que executa não suporta a versão compilada.

**Fix:** use `--release N` no `javac` (ou no `pom.xml`/`build.gradle`) para garantir que o bytecode gerado seja compatível com o alvo de deploy:

```bash
javac --release 11 Order.java   # gera major_version=55 mesmo no JDK 21
```

Em projetos Maven:

```xml
<properties>
    <maven.compiler.release>11</maven.compiler.release>
</properties>
```

---

### (3) Assumir que 1 linha de código = 1 instrução (o caso da concatenação)

**O problema:** uma linha aparentemente trivial pode gerar bytecode inesperadamente diferente do que a leitura do fonte sugere. O exemplo mais comum é a concatenação de strings:

```java
String msg = "Order " + id + " total: " + total;
```

No Java 8, isso gerava 4+ instruções para construir um `StringBuilder` explícito. No Java 9+, gera uma única instrução `invokedynamic` para `StringConcatFactory`:

```text
invokedynamic #4, 0  // InvokeDynamic #0:makeConcatWithConstants:(II)Ljava/lang/String;
```

Quem assume que o comportamento em runtime é o que "parece óbvio" no bytecode pode se surpreender ao diagnosticar um problema de performance ou comportamento em versões diferentes do JDK.

**Fix:** sempre valide com `javap -v` na versão-alvo de deploy, especialmente ao migrar entre versões do JDK onde estratégias de geração de código (como concatenação de strings) mudaram.

## Em entrevista

### Frase pronta (inglês)

> "The Java compiler doesn't produce native machine code — it produces bytecode, a platform-independent instruction set for the JVM. Each `.class` file is a structured binary container with a magic number `CAFEBABE`, a major version that identifies the Java release, a constant pool that holds all symbolic references, and a set of methods each carrying their own bytecode in a `Code` attribute."

> "The JVM is a stack-based machine: instead of named registers, each method execution gets a frame with a local variable array and an operand stack. Instructions like `iload`, `iadd`, and `ireturn` push, operate on, and pop values from that stack. The `javap -c -v` tool disassembles the bytecode so you can see exactly what the compiler generated — useful for understanding features like how records generate their accessors or how `invokedynamic` backs lambda expressions."

> "One important caveat: bytecode is the input to the JIT compiler, not the final story. The HotSpot JIT — especially the C2 compiler — can inline, devirtualize, and optimize bytecode heavily. So if you want to understand actual runtime performance, you benchmark with JMH and look at JIT output, not at `javap` output."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| bytecode | bytecode |
| contêiner de classe | class file |
| pool de constantes | constant pool |
| pilha de operandos | operand stack |
| array de variáveis locais | local variable array |
| quadro de execução | execution frame |
| instrução de invocação | invoke instruction |
| call site dinâmico | dynamic call site |
| fábrica de lambda | lambda metafactory |
| número de versão maior | major version number |
| erro de versão incompatível | `UnsupportedClassVersionError` |
| compilação just-in-time | JIT compilation |

## Veja também

- [[01 - A JVM — o que é e o pipeline de execução]]
- [[05 - Classloading e o delegation model]]
- [[07 - JIT — C1, C2 e tiered compilation]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/13 - Records e record patterns|Records]]
- [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#bytecode|bytecode (Dicionário)]]

## Referências

- [javap man page — Oracle Java SE 21](https://docs.oracle.com/en/java/javase/21/docs/specs/man/javap.html) — flags `-c`, `-v`, `-p`, `-s`, `-l`, `-constants` e exemplos de saída.
- [The Java Virtual Machine Specification, Java SE 21 Edition — Chapter 4: The `class` File Format](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html) — estrutura do `ClassFile`, constant pool tags, major versions, descritores de campo e método.
- [The Java Virtual Machine Specification, Java SE 21 Edition — Chapter 6: The Java Virtual Machine Instruction Set](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-6.html) — referência completa de todos os opcodes e suas semânticas.
- [JEP 309: Dynamic Class-File Constants](https://openjdk.org/jeps/309) — introdução de `CONSTANT_Dynamic` (Java 11).
- [JEP 280: Indify String Concatenation](https://openjdk.org/jeps/280) — migração de `+` string para `invokedynamic` (Java 9).
