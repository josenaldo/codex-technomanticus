---
title: "Sealed classes e pattern matching"
created: 2026-06-02
updated: 2026-06-02
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - linguagem
  - magus
  - sealed
  - pattern-matching
aliases:
  - Sealed classes
  - Pattern matching
  - switch patterns
---

# Sealed classes e pattern matching

> [!abstract] TL;DR
> **Sealed classes/interfaces** (Java 17, GA) restringem quem pode estender ou implementar uma hierarquia: `sealed interface Shape permits Circle, Square, Rectangle` declara explicitamente o conjunto fechado de subtipos, e cada subtipo deve ser `final`, `sealed` ou `non-sealed`. **Pattern matching** testa o tipo e extrai dados em um único passo — em `instanceof` (Java 16, GA com binding variable e flow scoping), em `switch` (Java 21, GA com type patterns, guards `when` e `case null` explícito) e com **record patterns** (Java 21, GA) que desestruturam records, inclusive de forma aninhada. Juntos habilitam **exaustividade**: ao usar `switch` sobre um tipo selado cobrindo todos os subtipos, o compilador verifica a cobertura e **dispensa o `default`** — adicionar um novo subtipo passa a gerar erro de compilação onde faltar tratamento. **Primitive patterns** (JEP 455) são **preview** (Java 23), **não GA**.

## O que é

Sealed classes e pattern matching são features distintas que, combinadas, habilitam **modelagem de domínio fechado** com verificação de cobertura pelo compilador.

**Sealed** restringe a hierarquia: uma classe ou interface `sealed` declara, via cláusula `permits`, exatamente quais tipos podem estendê-la ou implementá-la. Diferente de `final` (que proíbe qualquer extensão) e de uma classe aberta (que permite extensão por qualquer um), `sealed` define um conjunto **fechado e conhecido** de subtipos. Isso dá ao compilador — e ao leitor humano — a garantia de que a hierarquia é exaustiva: `Shape` é um de `{Circle, Square, Rectangle}`, e nada mais.

**Pattern matching** testa um tipo e, no mesmo passo, extrai o valor já convertido para uma **binding variable**. Em vez de `instanceof` seguido de cast manual, `if (obj instanceof String s)` testa e vincula `s` de uma vez. Record patterns vão além e desestruturam o conteúdo: `case Point(int x, int y)` testa o tipo `Point` e extrai seus componentes `x` e `y`.

A sinergia aparece na **exaustividade**. Quando o `switch` opera sobre um tipo selado e cobre todos os subtipos permitidos, o compilador prova que a cobertura é total e dispensa o `default`. Esse é o coração da *data-oriented programming* no Java: modelar dados como hierarquias seladas de records e processá-los com switch exaustivo — um equivalente a Algebraic Data Types (ADTs) e *exhaustive matching* de linguagens funcionais.

> [!info] Conceito-dono: exaustividade (exhaustiveness)
> Esta nota é a dona do conceito de **exaustividade**. Exaustividade é a propriedade de um `switch` cobrir **todos** os casos possíveis do seu seletor, verificada em tempo de compilação. Ela só é possível quando o conjunto de casos é **finito e conhecido** pelo compilador — o que sealed types e enums garantem. As notas [[09 - Enums]] e [[13 - Records e record patterns]] referenciam este conceito; a definição canônica e suas armadilhas vivem aqui.

## Como funciona

### Sealed classes e interfaces

A declaração usa o modificador `sealed` seguido da cláusula `permits`, que lista os subtipos autorizados:

```java
public sealed interface Shape
    permits Circle, Square, Rectangle {}

public sealed class Vehicle
    permits Car, Truck, Motorcycle {}
```

Cada subtipo permitido deve declarar **exatamente um** dos três modificadores:

- **`final`** — não pode ser estendido adiante. Fecha o ramo.
- **`sealed`** — continua restrito, com sua própria cláusula `permits`. Propaga o controle.
- **`non-sealed`** — reabre o ramo: qualquer um pode estendê-lo. Escape hatch para extensibilidade controlada.

```java
public sealed interface Shape permits Circle, Square, Rectangle {}

public final class Circle implements Shape {}        // ramo fechado
public sealed class Rectangle implements Shape        // continua restrito
    permits Square, Oblong {}
public non-sealed class Square implements Shape {}    // reaberto
```

Records satisfazem o contrato naturalmente, pois são implicitamente `final`:

```java
public sealed interface Shape permits Circle, Square, Rectangle {}

// Records são final por definição — combinação canônica com sealed
public record Circle(double radius) implements Shape {}
public record Square(double side) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}
```

Restrições de acesso impostas pelo compilador:

- Cada subtipo permitido deve ser **diretamente acessível** ao tipo selado em tempo de compilação.
- Cada subtipo deve **estender/implementar diretamente** o tipo selado.
- Os subtipos devem estar no **mesmo módulo** (em módulo nomeado) ou no **mesmo pacote** (no módulo sem nome). Não é possível selar uma hierarquia cujos subtipos vivam em módulos diferentes.

A cláusula `permits` pode ser **omitida** se todos os subtipos estiverem declarados no mesmo arquivo-fonte — o compilador infere o conjunto:

```java
// Arquivo Shape.java — permits inferido
public sealed interface Shape {}
record Circle(double radius) implements Shape {}
record Square(double side) implements Shape {}
```

---

### instanceof pattern (Java 16)

O **type pattern** em `instanceof` testa o tipo e, se compatível, vincula o objeto já convertido a uma **binding variable** (também chamada *pattern variable*). Elimina o cast manual:

```java
// Antes — teste, depois cast manual
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}

// Com pattern — teste + binding em um passo
if (obj instanceof String s) {
    System.out.println(s.length());   // s já é String
}
```

A binding variable obedece a **flow scoping**: ela está em escopo apenas onde o compilador consegue provar que o `instanceof` foi verdadeiro. Isso permite combinar com `&&` e tratar a negação:

```java
// Binding válido dentro da condição combinada com &&
if (obj instanceof String s && !s.isBlank()) {
    process(s);                       // s em escopo aqui
}

// Flow scoping com early return — s em escopo no fluxo "verdadeiro" após o if
public int length(Object obj) {
    if (!(obj instanceof String s)) {
        return 0;                     // s NÃO está em escopo aqui
    }
    return s.length();                // s EM escopo — o else implícito garante String
}
```

O escopo não é o bloco `{}` léxico, mas o conjunto de pontos do programa onde o teste comprovadamente passou. Por isso `if (!(obj instanceof String s)) return;` deixa `s` disponível **depois** do `if`.

---

### Switch patterns (Java 21)

O `switch` deixa de aceitar apenas constantes e passa a aceitar **type patterns** como labels. O seletor pode ser qualquer tipo de referência (ou `int`):

```java
String describe(Object obj) {
    return switch (obj) {
        case Integer i  -> "int: " + i;          // type pattern + binding
        case Long l     -> "long: " + l;
        case String s   -> "string de tamanho " + s.length();
        case int[] arr  -> "array de " + arr.length;
        case null       -> "nulo";               // case null explícito
        default         -> "outra coisa";
    };
}
```

Diferenças importantes em relação ao `switch` clássico:

- **`case null` explícito** — historicamente um `switch` lançava `NullPointerException` ao receber `null`. Com patterns, é possível tratar `null` como um label próprio. Sem `case null`, o comportamento de NPE em `null` é preservado (a menos que exista `case null, default`).
- Não se pode combinar `null` com outro pattern no mesmo label, exceto `default`: `case null, String s` é erro; `case null, default` é válido.

---

### Record patterns em switch (Java 21)

**Record patterns** desestruturam um record diretamente no label, vinculando seus componentes:

```java
record Point(int x, int y) {}
record Line(Point start, Point end) {}

String describe(Object obj) {
    return switch (obj) {
        // Desestrutura Point — extrai x e y de uma vez
        case Point(int x, int y) -> "ponto em (" + x + "," + y + ")";

        // Aninhamento — patterns dentro de patterns
        case Line(Point(var x1, var y1), Point p2) ->
            "linha de (" + x1 + "," + y1 + ") até " + p2;

        case null -> "nulo";
        default   -> "desconhecido";
    };
}
```

O aninhamento é recursivo: cada componente pode, por sua vez, ser um record pattern. `var` infere o tipo do componente. A desestruturação é o que torna o `switch` sobre uma hierarquia selada de records tão expressivo — testa o tipo e extrai os dados na mesma cláusula.

---

### Guards (`when`)

Um **guard** adiciona uma condição booleana a um pattern via cláusula `when`. O case só casa se o pattern bater **e** o guard for verdadeiro:

```java
String classify(Object obj) {
    return switch (obj) {
        case Integer i when i > 0  -> "positivo: " + i;
        case Integer i when i < 0  -> "negativo: " + i;
        case Integer i             -> "zero";          // i == 0
        case String s when s.isBlank() -> "string em branco";
        case String s              -> "string: " + s;
        default                    -> "outro";
    };
}
```

Guards combinam com record patterns para expressar regras de domínio diretamente no label:

```java
double area(Shape shape) {
    return switch (shape) {
        case Circle(double r) when r > 0 -> Math.PI * r * r;
        case Circle c                    -> 0;   // raio inválido
        case Rectangle(double w, double h) when w == h -> w * w;  // quadrado
        case Rectangle(double w, double h)             -> w * h;
        case Square(double s)            -> s * s;
    };
}
```

Atenção: um case **guardado** (`when`) não conta para a exaustividade, pois o compilador não consegue provar que o guard sempre será verdadeiro. É preciso ter, ao final, um case **sem guard** que cubra o tipo (como `case Circle c` acima cobrindo o `Circle` cujo `r <= 0`).

---

### Exaustividade

A **exaustividade** (*exhaustiveness*) é a propriedade central que sealed + pattern matching habilita. Quando o `switch` é uma **expressão** (produz valor) e o seletor é de um tipo selado, o compilador exige que **todos** os subtipos permitidos sejam cobertos. Se a cobertura é total, o `default` torna-se **desnecessário**:

```java
sealed interface Shape permits Circle, Square, Rectangle {}
record Circle(double radius) implements Shape {}
record Square(double side) implements Shape {}
record Rectangle(double width, double height) implements Shape {}

double area(Shape shape) {
    return switch (shape) {
        case Circle c    -> Math.PI * c.radius() * c.radius();
        case Square s    -> s.side() * s.side();
        case Rectangle r -> r.width() * r.height();
        // Sem default! O compilador prova que a cobertura é exaustiva.
    };
}
```

Como isso funciona e por que importa:

- O compilador conhece o conjunto fechado `{Circle, Square, Rectangle}` graças ao `sealed ... permits`. Ele verifica que cada um aparece em algum case (com pattern não guardado).
- Se faltar um subtipo, **erro de compilação**: `the switch expression does not cover all possible input values`.
- Se um novo subtipo `Triangle` for adicionado ao `permits`, **todos** os switches exaustivos sobre `Shape` passam a falhar na compilação até serem atualizados. Esse é o ganho central: o compilador vira uma checklist de "onde preciso tratar o novo caso".

**`case null` e exaustividade.** Por padrão um switch exaustivo sobre tipo de referência não precisa de `case null` — ele lança NPE em `null` como o switch clássico. Se o domínio admite `null` como valor legítimo, adicione `case null` explícito (sozinho ou via `case null, default`). Em domínio fechado bem modelado, geralmente prefere-se rejeitar `null` na fronteira e manter o switch sem ele.

**Por que evitar `default` em domínio fechado.** Adicionar um `default` a um switch sobre sealed type **desliga** a verificação de exaustividade: o compilador passa a aceitar qualquer cobertura, porque o `default` "fecha" todos os casos restantes. O preço é silencioso e perigoso — ao adicionar um novo subtipo, o `default` o engole sem aviso, e um bug de "esqueci de tratar o novo caso" só aparece em runtime. Em domínio fechado, **omitir o `default` é a feature, não a omissão**. Esse é o mesmo princípio do switch exaustivo sobre enums — veja [[09 - Enums]].

---

### Primitive patterns (preview, Java 23+)

> [!warning] Preview — NÃO é GA
> **Primitive Types in Patterns, instanceof, and switch** (JEP 455) é uma feature **preview** introduzida no **Java 23** — **não é GA** (general availability). Continuou como segundo preview (JEP 488) em versões posteriores. Para compilar e rodar é necessário `--enable-preview`, e a API/sintaxe pode mudar antes de estabilizar. Não assuma disponibilidade em produção sem confirmar a versão do JDK.

A proposta estende patterns, `instanceof` e `switch` para aceitarem **tipos primitivos**. Hoje, `switch` aceita apenas `byte`, `short`, `char` e `int` como seletor; a feature ampliaria para `boolean`, `float`, `double` e `long`, e permitiria primitive type patterns como `case int i`:

```java
// PREVIEW (JEP 455, Java 23) — exige --enable-preview
Object o = 42;
String s = switch (o) {
    case int i    -> "int: " + i;
    case long l   -> "long: " + l;
    case double d -> "double: " + d;
    default       -> "outro";
};

// instanceof com primitivo (preview) — testa conversão segura sem perda
if (x instanceof byte b) {
    // x cabe em byte sem lossy conversion
}
```

O valor da feature está em tornar `instanceof`/`switch` uniformes para todos os tipos e em proteger contra *lossy conversions*. Mas, repetindo: **preview**, sujeito a mudança.

## Na prática

O caso canônico é **modelar um domínio fechado** como interface selada de records e processá-lo com `switch` exaustivo. Calculando a área de formas geométricas:

```java
public sealed interface Shape
    permits Circle, Square, Rectangle {}

public record Circle(double radius) implements Shape {}
public record Square(double side) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}

public final class Geometry {
    public static double area(Shape shape) {
        return switch (shape) {
            case Circle(double r)            -> Math.PI * r * r;
            case Square(double s)            -> s * s;
            case Rectangle(double w, double h) -> w * h;
            // exaustivo: sem default, compilador garante cobertura
        };
    }

    public static double perimeter(Shape shape) {
        return switch (shape) {
            case Circle(double r)            -> 2 * Math.PI * r;
            case Square(double s)            -> 4 * s;
            case Rectangle(double w, double h) -> 2 * (w + h);
        };
    }
}
```

Adicionar `Triangle` ao domínio é uma operação guiada pelo compilador: inclui-se `Triangle` no `permits`, cria-se o record, e **`area` e `perimeter` passam a não compilar** até tratarem o novo caso. O conjunto de pontos a atualizar é exato e mecânico.

### Comparação com o Visitor pattern

Antes do pattern matching, a forma idiomática de adicionar operações a uma hierarquia fechada sem espalhar `instanceof` era o **Visitor pattern**:

```java
// Visitor clássico — a hierarquia "aceita" visitantes
interface Shape {
    <R> R accept(Visitor<R> v);
}
interface Visitor<R> {
    R visitCircle(Circle c);
    R visitSquare(Square s);
    R visitRectangle(Rectangle r);
}

final class Circle implements Shape {
    final double radius;
    Circle(double radius) { this.radius = radius; }
    public <R> R accept(Visitor<R> v) { return v.visitCircle(this); }
}
// ... Square, Rectangle análogos, cada um com accept()

// Operação = uma implementação de Visitor
class AreaVisitor implements Visitor<Double> {
    public Double visitCircle(Circle c)       { return Math.PI * c.radius * c.radius; }
    public Double visitSquare(Square s)       { return s.side * s.side; }
    public Double visitRectangle(Rectangle r) { return r.width * r.height; }
}
```

Os dois resolvem o mesmo problema (adicionar operações a uma hierarquia de tipos), com trade-offs diferentes:

- **Pattern matching vence quando** o conjunto de tipos é estável e novas **operações** são frequentes. Cada operação é um método com um `switch` local — não exige tocar nas classes da hierarquia. Menos boilerplate (sem `accept`/`visit`), mais legível, e a exaustividade dá a mesma garantia de cobertura que o Visitor obtém via métodos abstratos.
- **Visitor ainda tem espaço quando** a hierarquia **não pode ser selada** (subtipos em módulos diferentes, ou hierarquia genuinamente aberta a extensão por terceiros), ou quando se quer forçar, via tipo, que toda nova operação trate todos os casos sem depender de uma versão de compilador com pattern matching. O Visitor também desacopla a operação da hierarquia de forma mais explícita em APIs públicas.

Em código moderno (Java 21+) sobre domínio fechado próprio, o switch exaustivo sobre sealed types costuma ser a escolha mais direta; o Visitor permanece relevante em hierarquias abertas ou APIs que não controlam todos os subtipos.

## Armadilhas

### (1) Usar `default` em switch sobre sealed type

**O problema:** adicionar um `default` a um switch exaustivo sobre um tipo selado **desliga a verificação de exaustividade**. O compilador para de exigir cobertura de todos os subtipos, porque o `default` cobre "todo o resto". Ao adicionar um novo subtipo, nenhum erro de compilação aparece — o novo caso é silenciosamente engolido pelo `default`, e o bug só se manifesta em runtime.

```java
sealed interface Shape permits Circle, Square, Rectangle {}
// ... e depois alguém adiciona:  permits Circle, Square, Rectangle, Triangle

double area(Shape shape) {
    return switch (shape) {
        case Circle c    -> Math.PI * c.radius() * c.radius();
        case Square s    -> s.side() * s.side();
        case Rectangle r -> r.width() * r.height();
        default          -> 0.0;   // ❌ engole Triangle silenciosamente — área 0, sem aviso
    };
}
```

**Fix:** em domínio fechado, **não use `default`**. Liste todos os subtipos. Assim, ao adicionar `Triangle`, o switch deixa de compilar e o compilador aponta exatamente onde tratar:

```java
double area(Shape shape) {
    return switch (shape) {
        case Circle c    -> Math.PI * c.radius() * c.radius();
        case Square s    -> s.side() * s.side();
        case Rectangle r -> r.width() * r.height();
        // sem default — adicionar Triangle ao permits quebra a compilação aqui
    };
}
// Erro: the switch expression does not cover all possible input values
```

---

### (2) Dominance de labels — case genérico antes do específico

**O problema:** se um label mais **genérico** aparece antes de um mais **específico**, o específico se torna inalcançável (*unreachable*). O compilador detecta a **dominance** e gera erro. Vale para subtipos e para guards.

```java
String describe(Object obj) {
    return switch (obj) {
        case CharSequence cs -> "char sequence";
        case String s        -> "string";   // ❌ erro: dominado por CharSequence
        default              -> "outro";
    };
}
// Erro de compilação: this case label is dominated by a preceding case label
```

O mesmo ocorre com um pattern não guardado antes de um guardado do mesmo tipo: `case Integer i` (sem guard) domina qualquer `case Integer i when ...` posterior, tornando-o inalcançável.

**Fix:** ordene do mais **específico** para o mais **genérico**; coloque casos guardados (`when`) **antes** do caso não guardado do mesmo tipo:

```java
String describe(Object obj) {
    return switch (obj) {
        case String s        -> "string";        // específico primeiro
        case CharSequence cs -> "char sequence"; // genérico depois
        default              -> "outro";
    };
}

String classify(Object obj) {
    return switch (obj) {
        case Integer i when i > 0 -> "positivo"; // guarded primeiro
        case Integer i            -> "<= 0";     // unguarded depois (pega o resto)
        default                   -> "outro";
    };
}
```

---

### (3) Tratar primitive patterns / string templates como GA quando são preview

**O problema:** assumir que features **preview** estão disponíveis em produção. **Primitive patterns** (JEP 455, Java 23) são preview. **String templates** (`STR."..."`) também foram preview e acabaram **removidas** em versões posteriores para redesenho — um lembrete de que preview pode mudar ou desaparecer. Escrever código que depende delas sem `--enable-preview`, ou assumir estabilidade de API, quebra build e portabilidade.

```java
// ❌ Tentar usar primitive pattern sem habilitar preview
Object o = 42;
String s = switch (o) {
    case int i -> "int: " + i;   // erro: preview feature não habilitada
    default    -> "?";
};
// error: patterns on primitive types are a preview feature and are disabled by default
```

**Fix:** confirme a versão do JDK e o status da feature antes de usar. Para preview, compile/rode com `--enable-preview` (ciente do risco), e prefira a forma GA equivalente em código de produção:

```java
// ✅ Forma GA — reference patterns (estável desde Java 21)
Object o = 42;
String s = switch (o) {
    case Integer i -> "int: " + i;   // Integer (reference) — GA, sem preview
    default        -> "?";
};

// Para preview deliberado:
//   javac --release 23 --enable-preview Foo.java
//   java  --enable-preview Foo
```

Regra prática: em entrevista e em código de produção, marque claramente o que é GA (sealed Java 17, switch patterns / record patterns Java 21) versus preview (primitive patterns), e nunca apresente preview como disponível por padrão.

## Em entrevista

### Frase pronta (inglês)

> "Sealed interfaces let me close a type hierarchy explicitly — `sealed interface Shape permits Circle, Square, Rectangle` — so the compiler knows the exact, finite set of subtypes; combined with a switch expression, this gives me exhaustiveness checking, which means I can drop the `default` branch entirely. The deliberate decision here is to model a fixed domain as a sealed hierarchy of records and process it with an exhaustive switch, because that turns the compiler into a safety net: if someone adds a new subtype, every switch that doesn't handle it fails to compile, instead of silently falling through at runtime. The caveat is that I never add a `default` branch to an exhaustive switch over a sealed type — a `default` switches the exhaustiveness check off, so a newly added subtype would be silently swallowed and the bug would only surface in production."

> "I treat preview features carefully: pattern matching for switch and record patterns are general-availability since Java 21, but primitive types in patterns — JEP 455 — are still a preview feature in Java 23, so they require `--enable-preview` and the syntax can still change; I don't ship code that depends on preview features."

> "This style is essentially data-oriented programming in Java: instead of polymorphism through inheritance, I separate immutable data — sealed hierarchies of records — from the behavior that operates on it via exhaustive pattern matching, which often reads cleaner than the classic visitor pattern when the set of types is stable and I keep adding new operations."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| classe/interface selada | sealed class / sealed interface |
| hierarquia fechada | closed hierarchy |
| subtipo permitido | permitted subtype / subclass |
| casamento de padrões | pattern matching |
| variável de vínculo | binding variable / pattern variable |
| escopo de fluxo | flow scoping |
| guarda (cláusula when) | guard / guarded pattern |
| exaustividade | exhaustiveness |
| desestruturação | deconstruction / destructuring |
| dominância de labels | case label dominance |
| feature preview | preview feature |
| programação orientada a dados | data-oriented programming |

## Veja também

- [[03 - Estruturas de controle e fluxo]]
- [[09 - Enums]]
- [[13 - Records e record patterns]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [JEP 409: Sealed Classes](https://openjdk.org/jeps/409) — sealed classes/interfaces; GA no Java 17
- [JEP 441: Pattern Matching for switch](https://openjdk.org/jeps/441) — switch patterns, guards e exaustividade; GA no Java 21
- [JEP 455: Primitive Types in Patterns, instanceof, and switch (Preview)](https://openjdk.org/jeps/455) — **preview** no Java 23, não GA
- [Sealed Classes and Interfaces — Oracle Java 21 Language Guide](https://docs.oracle.com/en/java/javase/21/language/sealed-classes-and-interfaces.html)
- [Pattern Matching for switch — Oracle Java 21 Language Guide](https://docs.oracle.com/en/java/javase/21/language/pattern-matching-switch.html)
