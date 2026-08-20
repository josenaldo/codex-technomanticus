---
title: "Estruturas de controle e fluxo"
created: 2026-06-02
updated: 2026-06-02
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - linguagem
  - iniciado
  - controle-de-fluxo
  - switch
aliases:
  - switch expression
  - Estruturas de controle
---

# Estruturas de controle e fluxo

> [!abstract] TL;DR
> Java oferece condicionais (`if`/`else`, operador ternário), **switch** nas formas _statement_ e _expression_ (Java 14+), e quatro variantes de loops (`for`, enhanced for/for-each, `while`, `do-while`). O **switch expression** — introduzido pelo JEP 361 — elimina fall-through acidental com a sintaxe de seta `->`, suporta multi-label (`case A, B, C`) e exige exaustividade, tornando-se a forma preferida quando o switch retorna um valor. Os keywords `break`, `continue` e labels controlam saída antecipada de loops e blocos aninhados.

## O que é

Fluxo de controle imperativo é o mecanismo pelo qual um programa decide **qual código executar** e **quantas vezes executá-lo**, baseado em condições avaliadas em tempo de execução.

Em Java, as estruturas de controle de fluxo dividem-se em três famílias:

- **Condicionais** — bifurcam a execução com base em expressões booleanas: `if`/`else if`/`else` e o operador ternário `? :`.
- **Seleção por valor** — `switch` (nas formas _statement_ e _expression_) roteia a execução de acordo com o valor de uma expressão.
- **Repetição** — loops que executam um bloco enquanto uma condição for verdadeira ou por um número determinado de iterações: `for`, enhanced for, `while`, `do-while`.

Além das estruturas de repetição, existem os **controladores de fluxo dentro de loops**: `break`, `continue` e labels, que permitem interromper ou pular iterações em laços simples ou aninhados.

Embora a Streams API cubra muitos cenários de iteração de forma mais declarativa, entender essas estruturas imperativas é fundamental — elas são o substrato de toda lógica de controle em Java e aparecem diretamente em código de baixo nível, em benchmarks, em implementações de algoritmos e em perguntas de entrevista.

## Como funciona

### Condicionais (`if`/`else`, ternário)

A forma canônica é `if`/`else if`/`else`. Cada condição é uma expressão que avalia para `boolean` (Java não aceita inteiros como condições, ao contrário de C/C++).

```java
int idade = 20;

if (idade >= 18) {
    System.out.println("adulto");
} else if (idade >= 13) {
    System.out.println("adolescente");
} else {
    System.out.println("criança");
}
```

O **operador ternário** `condição ? valorSeVerdadeiro : valorSeFalso` é uma expressão — retorna um valor e pode ser usado onde qualquer expressão é válida. É adequado para atribuições simples; condicionais com lógica complexa tornam-se ilegíveis com ternário aninhado.

```java
// Adequado: lógica simples e intenção clara
String rotulo = idade >= 18 ? "maior" : "menor";

// Evitar: ternário aninhado (difícil de ler)
String faixa = idade >= 65 ? "idoso" : idade >= 18 ? "adulto" : "jovem";
```

---

### `switch` statement vs `switch` expression

Java possui **duas formas** de `switch`, com semânticas distintas.

#### Switch statement (forma clássica)

A forma tradicional usa `case X:` com dois-pontos. O fluxo **cai** (fall-through) de um `case` para o próximo a menos que haja um `break` explícito. Isso é uma fonte histórica de bugs.

```java
// Switch statement clássico com fall-through intencional
int dia = 3;
String tipo;
switch (dia) {
    case 1:
    case 7:
        tipo = "fim de semana";
        break;
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
        tipo = "dia útil";
        break;
    default:
        tipo = "inválido";
}
```

Problemático: esquecer o `break` faz a execução escorregar para o próximo `case` silenciosamente. Ver a armadilha **(1) Fall-through esquecendo `break`** abaixo.

#### Switch expression (Java 14+, JEP 361)

Introduzida definitivamente no Java 14 pelo JEP 361. A forma `case L ->` (seta) tem três propriedades-chave confirmadas na especificação:

1. **Sem fall-through** — cada arm é independente; ao encontrar a label correspondente, somente o código à direita da seta executa.
2. **Multi-label** — múltiplas labels podem ser agrupadas com vírgula em um único `case`: `case A, B, C ->`.
3. **Exaustividade obrigatória** — o compilador exige que todos os valores possíveis estejam cobertos (com `default` para tipos abertos; para `enum` cobrindo todas as constantes, o compilador insere `default` implicitamente).

```java
// Switch expression com seta — sem fall-through, sem break
String resultado = switch (dia) {
    case 1, 7    -> "fim de semana";
    case 2, 3, 4, 5, 6 -> "dia útil";
    default      -> throw new IllegalArgumentException("Dia inválido: " + dia);
};
```

Quando o arm precisa de **múltiplas instruções**, usa-se um bloco `{}` com `yield` para produzir o valor:

```java
int numLetras = switch (diaSemana) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY                -> 7;
    case THURSDAY, SATURDAY     -> 8;
    case WEDNESDAY              -> {
        System.out.println("Quarta-feira");
        yield 9;  // yield produz o valor do bloco
    }
};
```

`yield` é exclusivo do switch expression (não pode ser usado em switch statement). `break` é exclusivo do switch statement. O uso de `yield` com a forma de dois-pontos no switch expression (forma colon, também válida) é mais verboso e deve ser preterido em favor da forma de seta.

**Gancho de profundidade:** quando o tipo avaliado no switch é uma sealed class ou interface, a exaustividade passa a ser verificada estaticamente pelo compilador — não é mais necessário um `default`. Isso é explorado em [[14 - Sealed classes e pattern matching]].

---

### Loops (`for`, enhanced for/for-each, `while`, `do-while`)

#### `for` clássico

Ideal quando o índice é necessário ou quando o número de iterações é conhecido previamente.

```java
// Forma geral: inicialização; condição; atualização
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

// Todas as partes são opcionais (mas os ponto-e-vírgulas são obrigatórios)
int i = 0;
for (; i < 10; ) {   // equivale a um while
    System.out.println(i++);
}
```

#### Enhanced for (for-each)

Itera sobre qualquer `Iterable` ou array sem expor o índice. Mais legível quando o índice não é necessário.

```java
List<String> nomes = List.of("Ana", "Bruno", "Carlos");
for (String nome : nomes) {
    System.out.println(nome);
}

int[] numeros = {1, 2, 3, 4, 5};
for (int n : numeros) {
    System.out.println(n);
}
```

Restrição importante: **não é possível modificar a coleção subjacente durante a iteração** com for-each — isso lança `ConcurrentModificationException`. Ver a armadilha **(3) Modificar coleção dentro de for-each** abaixo.

#### `while`

Verifica a condição antes de cada iteração. Se a condição for falsa na primeira avaliação, o corpo nunca executa.

```java
int contador = 0;
while (contador < 5) {
    System.out.println(contador);
    contador++;
}
```

#### `do-while`

Executa o corpo **ao menos uma vez** antes de verificar a condição. Útil para menus, validação de input e retry loops onde ao menos uma tentativa é garantida.

```java
String entrada;
do {
    entrada = scanner.nextLine();
} while (entrada.isBlank());
// Garante que a entrada não seja em branco antes de prosseguir
```

---

### `break`, `continue` e labels

**`break`** encerra o loop (ou switch statement) mais interno imediatamente.

**`continue`** pula para a próxima iteração do loop mais interno, ignorando o restante do corpo atual.

```java
for (int i = 0; i < 10; i++) {
    if (i == 5) break;       // interrompe quando i == 5
    if (i % 2 == 0) continue; // pula números pares
    System.out.println(i);    // imprime 1, 3
}
```

**Labels** permitem que `break` e `continue` referenciem um loop externo específico em estruturas aninhadas. Um label é um identificador seguido de `:` antes da declaração do loop.

```java
externo:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (i == 1 && j == 1) break externo;  // sai do loop externo
        System.out.println(i + "," + j);
    }
}
// Saída: 0,0 / 0,1 / 0,2 / 1,0
```

Labels são válidos, mas o uso excessivo é um sinal de que o código pode ser refatorado em métodos menores com `return` explícito.

## Na prática

**Refatorando switch statement com fall-through para switch expression:**

Considere o switch statement clássico abaixo — o padrão de multi-label era feito empilhando `case` vazios, com `break` em cada grupo:

```java
// ANTES — switch statement clássico (Java pré-14)
String descricao;
switch (status) {
    case "PENDING":
    case "QUEUED":
        descricao = "Aguardando processamento";
        break;
    case "RUNNING":
        descricao = "Em execução";
        break;
    case "DONE":
        descricao = "Concluído";
        break;
    default:
        descricao = "Status desconhecido";
}
```

Com switch expression (Java 14+), o mesmo código torna-se mais conciso, sem o risco de esquecer um `break`, e retorna o valor diretamente:

```java
// DEPOIS — switch expression (Java 14+)
String descricao = switch (status) {
    case "PENDING", "QUEUED" -> "Aguardando processamento";
    case "RUNNING"           -> "Em execução";
    case "DONE"              -> "Concluído";
    default                  -> "Status desconhecido";
};
```

Pontos a observar na refatoração:
- Multi-label com vírgula substitui o empilhamento de `case` vazios.
- A ausência de `break` não é um esquecimento — a seta `->` não tem fall-through por design.
- O valor é atribuído diretamente; não é necessária a variável declarada antes do bloco.
- O compilador exige `default` porque `String` não é um tipo fechado.

## Armadilhas

### (1) Fall-through esquecendo `break` no switch clássico

**O problema:** no switch statement, a ausência de `break` faz a execução "escorregar" para o próximo `case`, mesmo que a label não corresponda ao valor avaliado. Esse comportamento é silencioso — nenhum aviso em tempo de compilação.

```java
int cod = 2;
switch (cod) {
    case 1:
        System.out.println("um");
        // ESQUECEU O break!
    case 2:
        System.out.println("dois");
        // ESQUECEU O break!
    case 3:
        System.out.println("três");
        break;
}
// Saída: "dois" e "três" — executou também o case 3
```

**Fix:** adicionar `break` em cada `case` — ou, preferencialmente, migrar para switch expression com `->`, onde fall-through é impossível por design.

```java
String saida = switch (cod) {
    case 1 -> "um";
    case 2 -> "dois";
    case 3 -> "três";
    default -> "outro";
};
```

---

### (2) `switch` em valor `null` — NPE no clássico; `case null` no moderno

**O problema:** no switch statement e no switch expression pré-Java 21, passar `null` como valor avaliado lança `NullPointerException` imediatamente — antes de qualquer `case` ser verificado. Isso não é intuitivo para quem espera que o `default` cubra o caso nulo.

```java
String valor = null;

// NPE aqui — não chega nem a avaliar os cases
switch (valor) {
    case "A":
        System.out.println("A");
        break;
    default:
        System.out.println("outro");
}
```

**Fix clássico (defensivo):** verificar `null` antes do switch.

```java
if (valor == null) {
    // tratar null separadamente
} else {
    switch (valor) { ... }
}
```

**Fix moderno (Java 21+, pattern matching):** switch expression suporta `case null` explicitamente, eliminando a necessidade de checar fora do switch.

```java
String resultado = switch (valor) {
    case null    -> "nulo";
    case "A"     -> "valor A";
    default      -> "outro";
};
```

---

### (3) Modificar coleção dentro de for-each (`ConcurrentModificationException`)

**O problema:** o enhanced for usa internamente um `Iterator`. Modificar a coleção subjacente (adicionar ou remover elementos) durante a iteração invalida o iterator, e a JVM lança `ConcurrentModificationException` na próxima chamada a `next()`.

```java
List<String> nomes = new ArrayList<>(List.of("Ana", "Bruno", "Carlos"));

for (String nome : nomes) {
    if (nome.startsWith("B")) {
        nomes.remove(nome);  // ConcurrentModificationException!
    }
}
```

**Fix opção 1 — `Iterator` explícito com `remove()`:** o `Iterator` tem método `remove()` que remove o elemento atual de forma segura.

```java
Iterator<String> it = nomes.iterator();
while (it.hasNext()) {
    if (it.next().startsWith("B")) {
        it.remove();  // remoção segura via iterator
    }
}
```

**Fix opção 2 — `removeIf()` (Java 8+):** mais conciso para remoções baseadas em predicado.

```java
nomes.removeIf(nome -> nome.startsWith("B"));
```

**Fix opção 3 — iterar sobre cópia:** criar uma cópia da coleção para iterar enquanto modifica a original.

```java
for (String nome : new ArrayList<>(nomes)) {
    if (nome.startsWith("B")) nomes.remove(nome);
}
```

## Em entrevista

### Frase pronta (inglês)

> "The key trade-off between switch statement and switch expression is expressiveness versus legacy compatibility. Switch expressions — introduced as a standard feature in Java 14 via JEP 361 — return a value directly, making them ideal for assignments and removing the need for `break` statements entirely; the arrow form `->` guarantees no fall-through by design, which eliminates one of the most common sources of subtle bugs in switch statements. The caveat is exhaustiveness: switch expressions must cover all possible values at compile time, so you'll always need a `default` clause unless you're switching on a sealed type where the compiler can verify completeness statically — which is where pattern matching and sealed classes, introduced in later versions, provide the strongest guarantees."

Use essa resposta para perguntas como *"What is the difference between switch statement and switch expression in Java?"*, *"What improvements did Java 14 bring to switch?"* ou *"How does the compiler enforce exhaustiveness in switch expressions?"*.

### Vocabulário

| Termo PT                                  | Termo EN                                              |
|-------------------------------------------|-------------------------------------------------------|
| estrutura de controle                     | control flow structure                                |
| condicional                               | conditional statement                                 |
| operador ternário                         | ternary operator / conditional expression             |
| seleção por valor                         | value-based selection / switch                        |
| queda de caso (switch)                    | fall-through                                          |
| expressão switch                          | switch expression                                     |
| declaração switch                         | switch statement                                      |
| exaustividade                             | exhaustiveness                                        |
| multi-label de case                       | multi-label case / comma-separated case labels        |
| palavra-chave yield                       | `yield` keyword                                       |
| loop aprimorado / for-each                | enhanced for loop / for-each loop                     |
| modificação concorrente (iteração)        | concurrent modification (`ConcurrentModificationException`) |

## Veja também

- [[02 - Tipos, variáveis e operadores]]
- [[04 - Strings e text blocks]]
- [[14 - Sealed classes e pattern matching]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [JEP 361: Switch Expressions (Standard) — openjdk.org](https://openjdk.org/jeps/361)
- [Switch Expressions — Oracle Java SE 14 Language Updates](https://docs.oracle.com/en/java/javase/14/language/switch-expressions.html)
- [The switch Statement — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/switch.html)
- [Branching Statements — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/branch.html)
- [JDK 21 Documentation — Oracle](https://docs.oracle.com/en/java/javase/21/)
