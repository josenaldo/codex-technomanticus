---
title: "Performance — JMH e microbenchmarks"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - testes
  - magus
  - jmh
aliases:
  - "JMH"
  - "microbenchmark"
  - "Java Microbenchmark Harness"
---

# Performance — JMH e microbenchmarks

> [!abstract] TL;DR
> Medir performance num `@Test` com `System.nanoTime()` mente: a JVM aquece, o JIT compila *durante* a medição, e código sem efeito colateral é simplesmente eliminado. O **JMH** (Java Microbenchmark Harness) é o harness oficial do OpenJDK que lida com warmup, *fork* de JVM e *dead-code elimination* por você. É assim que se mede microbenchmark a sério — não com um cronômetro num teste de unidade.

## O que é

**JMH** é o **Java Microbenchmark Harness**, mantido pelo próprio projeto OpenJDK. Ele existe porque medir a velocidade de um trecho de código Java é surpreendentemente difícil: a JVM é uma plataforma adaptativa, e quase toda tentativa ingênua de cronometrar uma operação acaba medindo o harness, o aquecimento ou o nada — em vez do código de interesse.

Um *microbenchmark* mede um pedaço pequeno e isolado de código — a diferença entre concatenar com `+` e com `StringBuilder`, o custo de um `HashMap` vs. `TreeMap`, o overhead de um `Stream` vs. um `for`. JMH dá a infraestrutura para que essas medidas sejam **reprodutíveis e confiáveis**, em vez de números que mudam de execução para execução.

O escopo aqui é **microbenchmark de código**: medir uma operação isolada num ambiente controlado. Profiling de produção e observabilidade — onde você mede a aplicação rodando sob carga real — são outro tema ([[03-Dominios/Tecnologia/Java/Cloud-native e produção/18 - Profiling e diagnóstico sob carga — produção|profiling de produção, Galho 17]]), e não usam JMH.

## Por que importa

Decisões de performance baseadas em "achismo" custam caro. Otimizar o trecho errado, ou trocar uma estrutura de dados por outra "porque parece mais rápida", desperdiça tempo e às vezes *piora* o desempenho. Um microbenchmark honesto transforma a discussão de opinião em medida.

Mas a única coisa pior que não medir é **medir errado**. Um benchmark ingênuo que diz "`StringBuilder` é 1000x mais rápido" porque o JIT eliminou o loop de concatenação produz uma conclusão falsa com aparência de rigor. JMH importa justamente porque desarma essas armadilhas: ele força o aquecimento, isola a JVM e impede que o compilador apague o que você queria medir.

## Como funciona

### Por que medir performance num @Test mente (warmup, JIT, dead-code elimination, constant folding)

Cronometrar com `System.nanoTime()` dentro de um `@Test` falha por quatro razões, todas vindas da natureza adaptativa da JVM (o mecanismo está no Galho 3):

- **Warmup**: nas primeiras execuções o método roda **interpretado** ou só parcialmente compilado. Medir antes do aquecimento mede a JVM fria, não o código otimizado que rodará em produção.
- **JIT compilando durante a medição**: o compilador C2 entra em ação no meio do seu loop de medida. Você cronometra uma mistura de código interpretado e compilado — um número sem significado.
- **Dead-code elimination**: se o resultado do cálculo não é usado, o JIT prova que o cálculo não tem efeito observável e **o apaga**. Você cronometra um loop vazio.
- **Constant folding**: se as entradas são constantes conhecidas em tempo de compilação, o JIT pré-computa o resultado. Você cronometra uma atribuição de constante, não o algoritmo.

O JIT que torna tudo isso traiçoeiro é exatamente o assunto do Galho 3 — aqui interessa só a consequência: um `@Test` não tem como controlar nenhum desses fatores.

### JMH: @Benchmark / @Warmup / @Measurement / @Fork / @State

JMH resolve cada problema com uma anotação. O método a medir é marcado com **`@Benchmark`**, e o harness o executa em fases controladas:

- **`@BenchmarkMode(Mode.AverageTime)`** — escolhe o que medir. `AverageTime` reporta tempo médio por operação; há também `Throughput` (operações por unidade de tempo), `SampleTime` e `SingleShotTime`.
- **`@Warmup(iterations = N, time = ...)`** — roda N iterações *descartadas* antes de medir, deixando o JIT aquecer e compilar. Só depois do warmup as medidas começam.
- **`@Measurement(iterations = N, time = ...)`** — as iterações que realmente contam para o resultado.
- **`@Fork(value = N)`** — roda o benchmark em uma JVM *separada* (ou N JVMs). Isolar o processo evita que o estado de uma medida contamine a próxima (perfis de compilação, alocação prévia) e reduz a variância entre execuções.
- **`@State(Scope.Thread)`** — encapsula o estado mutável do benchmark num objeto gerenciado pelo JMH. O escopo `Thread` dá uma instância por thread; há também `Benchmark` (compartilhado) e `Group`.

### @Param: variar o tamanho do input

A anotação **`@Param`** declara valores que o JMH vai injetar num campo do estado, rodando o benchmark uma vez para cada valor. É como você varia o tamanho do input sem duplicar o método:

```java
@Param({"10", "100", "1000"})
private int size;
```

O JMH executa o benchmark três vezes — `size=10`, `size=100`, `size=1000` — e reporta cada um separadamente. Isso revela como o custo *escala* com a entrada, em vez de dar um único número opaco.

### Blackhole: consumir o resultado pra o JIT não eliminar

Para impedir a *dead-code elimination*, o resultado do cálculo precisa ser **consumido** de um jeito que o JIT não consiga otimizar. Há duas formas:

1. **Retornar o valor** do método `@Benchmark` — o JMH trata o retorno como consumido.
2. **`Blackhole`** — um parâmetro injetado pelo JMH cujo método `consume(...)` engole qualquer valor sem que o compilador prove que ele é inútil. Indispensável quando o benchmark produz *vários* resultados num loop (você não pode retornar todos).

```java
@Benchmark
public void medirComBlackhole(Blackhole bh) {
    bh.consume(calcular());
}
```

Sem o `Blackhole` (ou o retorno), o JIT apagaria `calcular()` e você cronometraria um loop vazio.

## Na prática

Um benchmark comparando concatenação com `+` versus `StringBuilder`, variando o número de junções:

```java
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@Warmup(iterations = 5, time = 1)
@Measurement(iterations = 5, time = 1)
@Fork(value = 2)
@State(Scope.Thread)
public class StringConcatBenchmark {

    @Param({"10", "100", "1000"})
    private int repeticoes;

    @Benchmark
    public String concatComPlus() {
        String resultado = "";
        for (int i = 0; i < repeticoes; i++) {
            resultado += i;   // cria uma nova String a cada volta
        }
        return resultado;     // retornado => consumido, sem dead-code elimination
    }

    @Benchmark
    public void concatComStringBuilder(Blackhole bh) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < repeticoes; i++) {
            sb.append(i);
        }
        bh.consume(sb.toString());  // Blackhole consome o resultado
    }
}
```

O `@Warmup` garante que o JIT (Galho 3: [[03-Dominios/Tecnologia/Java/JVM/07 - JIT — C1, C2 e tiered compilation|JIT — C1, C2 e tiered compilation]]) já tenha compilado os dois métodos antes da medição; o `@Fork(2)` roda tudo em duas JVMs separadas para checar a estabilidade do número; o `@Param` mostra como a vantagem do `StringBuilder` cresce com o tamanho da entrada. Sem essas anotações, o mesmo código num `@Test` daria um resultado quase aleatório — é o JIT que torna o microbenchmark traiçoeiro.

## Armadilhas

### (1) Medir com System.nanoTime() dentro de um @Test

Cronometrar manualmente num teste de unidade dá um número que parece preciso (nanossegundos!) mas não tem significado: o JIT compila no meio da medição e o warmup falseia o começo.

```java
@Test
void quaoRapidoEh() {
    long inicio = System.nanoTime();
    for (int i = 0; i < 1_000_000; i++) {
        calcular();   // medido frio, depois compilando, depois quente — tudo misturado
    }
    long fim = System.nanoTime();
    System.out.println((fim - inicio) + " ns");  // número sem valor
}
```

**Fix**: tire a medição do `@Test`. Use JMH com `@Warmup` e `@Measurement`, que separam o aquecimento da medida e isolam a JVM com `@Fork`.

### (2) Sem warmup

Mesmo dentro do JMH, configurar `@Warmup(iterations = 0)` (ou cronometrar à mão sem aquecer) mede a JVM **fria e interpretada**, não o código que o JIT compilou. O resultado superestima o custo real em produção, às vezes por ordens de magnitude.

```java
@Warmup(iterations = 0)            // erro: sem aquecimento
@Measurement(iterations = 5)
@Benchmark
public int semWarmup() { ... }     // mede código interpretado
```

**Fix**: dê iterações de warmup suficientes (`@Warmup(iterations = 5)` é um ponto de partida razoável) para o C2 compilar o método antes da fase de medição.

### (3) Resultado não consumido

Se o método `@Benchmark` calcula algo e **não** retorna nem entrega o valor ao `Blackhole`, o JIT prova que o cálculo não tem efeito observável e o elimina. Você cronometra um loop vazio e conclui, falsamente, que a operação é "instantânea".

```java
@Benchmark
public void resultadoIgnorado() {
    calcular();   // retorno descartado => dead-code elimination => loop apagado
}
```

**Fix**: **retorne** o valor do método, ou injete um `Blackhole` e chame `bh.consume(resultado)`. Assim o compilador é obrigado a manter o cálculo vivo.

## Em entrevista

### Frase pronta (inglês)

> Timing code with `System.nanoTime()` inside a unit test is misleading on the JVM: the method runs interpreted until the JIT warms up, the C2 compiler kicks in *during* the measurement, and any result you don't consume gets removed by dead-code elimination. That's why I reach for JMH, the OpenJDK microbenchmark harness — it controls warmup, forks a separate JVM, and uses `Blackhole` to keep the compiler from optimizing away the very code I'm measuring. I treat JMH as code-level microbenchmarking, kept separate from production profiling, which answers a different question under real load.

### Vocabulário

| Termo (EN) | Tradução / sentido |
| --- | --- |
| microbenchmark | medida isolada de um trecho pequeno de código |
| warmup | iterações descartadas para o JIT compilar antes de medir |
| dead-code elimination | o JIT apaga cálculos sem efeito observável |
| constant folding | o JIT pré-computa resultados de entradas constantes |
| fork (JVM) | rodar o benchmark numa JVM separada para isolar e reduzir variância |
| harness | a infraestrutura que orquestra a medição (o próprio JMH) |
| throughput | operações por unidade de tempo (modo de benchmark) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/17 - Mutation testing — PIT e cobertura honesta|Mutation testing — PIT]]
- [[03-Dominios/Tecnologia/Java/JVM/07 - JIT — C1, C2 e tiered compilation|JIT — C1, C2 e tiered compilation]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]] (verbete JMH (microbenchmark))

## Referências

- OpenJDK JMH (Java Microbenchmark Harness): https://github.com/openjdk/jmh
