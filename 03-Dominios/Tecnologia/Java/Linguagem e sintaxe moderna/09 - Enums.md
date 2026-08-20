---
title: "Enums"
created: 2026-06-02
updated: 2026-06-02
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - linguagem
  - adepto
  - oop
  - enums
aliases:
  - Enum
---

# Enums

> [!abstract] TL;DR
> Um `enum` é um conjunto fixo de instâncias nomeadas — type-safe e mais expressivo do que constantes `int` ou `String`. Cada constante pode carregar estado (campos `final`) e comportamento (métodos), inclusive implementações distintas por constante (*constant-specific method bodies*). `EnumMap` e `EnumSet` são estruturas altamente eficientes por usarem array e bitvector internamente, respectivamente. Um `enum` de elemento único é o jeito idiomático de implementar singleton em Java (thread-safe e serialization-safe por construção). Para hierarquias fechadas mais complexas, o comparativo com `sealed classes` (Java 17+) define onde cada solução encaixa melhor.

## O que é

Um `enum` (tipo enumerado) é um tipo especial que define um **conjunto fechado de constantes nomeadas**, cada uma sendo uma instância única da própria classe enum. O compilador garante que nenhum outro valor desse tipo possa existir em runtime.

Antes dos enums (pré-Java 5), o padrão comum era usar constantes inteiras:

```java
// Padrão pré-Java 5 — type-unsafe, sem type checking
public static final int STATUS_PENDENTE   = 0;
public static final int STATUS_CONFIRMADO = 1;
public static final int STATUS_CANCELADO  = 2;

// Problema: nada impede o compilador de aceitar valores inválidos
processar(999); // compila sem erro — um int qualquer
```

Com enum, o compilador rejeita qualquer valor que não seja uma das constantes declaradas:

```java
public enum OrderStatus { PENDING, CONFIRMED, CANCELLED }

processar(OrderStatus.PENDING);  // correto
processar(999);                  // erro de compilação — type-safe
```

Além de type-safety, enums em Java são classes de primeira categoria: podem ter **campos**, **construtores**, **métodos de instância e estáticos**, e cada constante pode até **sobrescrever métodos** com comportamento próprio.

## Como funciona

### Enum básico e métodos implícitos

A declaração mais simples lista apenas os nomes das constantes:

```java
public enum DiaDaSemana {
    SEGUNDA, TERCA, QUARTA, QUINTA, SEXTA, SABADO, DOMINGO
}
```

O compilador adiciona automaticamente os seguintes métodos:

| Método | Descrição |
|---|---|
| `values()` | Retorna array com todas as constantes na ordem de declaração |
| `valueOf(String name)` | Retorna a constante com o nome exato (case-sensitive); lança `IllegalArgumentException` se não encontrar |
| `name()` | Retorna o nome da constante exatamente como declarado no código |
| `ordinal()` | Retorna o índice inteiro (base 0) na ordem de declaração |
| `toString()` | Por padrão retorna o mesmo que `name()` — pode ser sobrescrito |

```java
// values() — itera todas as constantes em ordem de declaração
for (DiaDaSemana dia : DiaDaSemana.values()) {
    System.out.println(dia.name() + " → ordinal " + dia.ordinal());
}
// SEGUNDA → ordinal 0
// TERCA   → ordinal 1
// ...

// valueOf() — converte String para constante
DiaDaSemana d = DiaDaSemana.valueOf("SEXTA"); // DiaDaSemana.SEXTA

// ordinal() — índice de posição (uso raramente recomendado — veja Armadilhas)
System.out.println(DiaDaSemana.DOMINGO.ordinal()); // 6
```

Todo enum implicitamente estende `java.lang.Enum` e implementa `Comparable` e `Serializable`. Por isso, enums não podem estender outra classe — mas podem implementar interfaces.

---

### Enum com estado e comportamento

Enums podem ter campos, construtores e métodos. Os campos devem ser `final` para manter a semântica de constante imutável. O construtor é sempre `private` (ou package-private) — o compilador não permite construção externa.

```java
public enum OrderStatus {

    PENDING("Pendente"),
    CONFIRMED("Confirmado"),
    SHIPPED("Enviado"),
    DELIVERED("Entregue"),
    CANCELLED("Cancelado");

    private final String label;

    // Construtor privado — chamado pelo compilador ao criar cada constante
    OrderStatus(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }

    /** Retorna true se o pedido está em estado terminal (sem transição possível). */
    public boolean isFinal() {
        return this == DELIVERED || this == CANCELLED;
    }
}
```

```java
// Uso
OrderStatus status = OrderStatus.PENDING;
System.out.println(status.getLabel());  // "Pendente"
System.out.println(status.isFinal());   // false

OrderStatus.DELIVERED.isFinal();        // true
```

A lista de constantes deve vir **antes** de qualquer campo ou método, e deve terminar com `;` quando houver membros adicionais.

---

### Método abstrato por constante

Cada constante pode fornecer sua própria implementação de um método declarado abstrato no enum — o que a spec chama de *constant-specific method bodies* (corpo de método específico da constante). É uma forma de polimorfismo embutida no próprio enum.

```java
public enum Operacao {

    SOMA("+") {
        @Override
        public double aplicar(double x, double y) { return x + y; }
    },

    SUBTRACAO("-") {
        @Override
        public double aplicar(double x, double y) { return x - y; }
    },

    MULTIPLICACAO("*") {
        @Override
        public double aplicar(double x, double y) { return x * y; }
    },

    DIVISAO("/") {
        @Override
        public double aplicar(double x, double y) {
            if (y == 0) throw new ArithmeticException("Divisão por zero");
            return x / y;
        }
    };

    private final String simbolo;

    Operacao(String simbolo) { this.simbolo = simbolo; }

    public String getSimbolo() { return simbolo; }

    /** Método abstrato — cada constante é obrigada a implementar. */
    public abstract double aplicar(double x, double y);
}
```

```java
double resultado = Operacao.SOMA.aplicar(10, 3);       // 13.0
double resultado2 = Operacao.MULTIPLICACAO.aplicar(4, 5); // 20.0

// Iterar todas as operações
for (Operacao op : Operacao.values()) {
    System.out.printf("10 %s 3 = %.1f%n", op.getSimbolo(), op.aplicar(10, 3));
}
```

Esse padrão elimina o `switch` espalhado pelo código e centraliza o comportamento na própria constante. Cada nova constante é **forçada** a implementar o método — o compilador não aceita omissão.

---

### `EnumMap` e `EnumSet`

`EnumMap` e `EnumSet` são implementações especializadas para chaves/elementos do tipo enum, introduzidas no Java 5. A vantagem de desempenho vem da representação interna.

**`EnumMap<K extends Enum<K>, V>`**

Internamente representado como um **array** indexado pelo `ordinal()` de cada constante. Não usa hash, não tem colisões. Todas as operações básicas são O(1) e tipicamente mais rápidas do que `HashMap`. Mantém as chaves na ordem de declaração do enum.

```java
import java.util.EnumMap;

EnumMap<OrderStatus, String> mensagens = new EnumMap<>(OrderStatus.class);
mensagens.put(OrderStatus.PENDING,   "Aguardando confirmação");
mensagens.put(OrderStatus.CONFIRMED, "Pedido confirmado");
mensagens.put(OrderStatus.DELIVERED, "Entregue com sucesso");

// Chaves sempre em ordem de declaração do enum
mensagens.forEach((status, msg) ->
    System.out.println(status.getLabel() + ": " + msg)
);

// Acesso direto — sem hashing, sem colisão
String msg = mensagens.get(OrderStatus.PENDING); // O(1) puro
```

Null como chave não é permitido; null como valor é permitido. Não é thread-safe — sincronize externamente se necessário.

**`EnumSet<E extends Enum<E>>`**

Representado internamente como **bitvector** (vetor de bits). Para enums com até 64 constantes, usa um único `long`; para enums maiores, usa `long[]`. Operações de adição, remoção e consulta são manipulações de bit — extremamente eficientes. Operações em massa (`containsAll`, `retainAll`) entre dois `EnumSet` também rodam em tempo constante.

```java
import java.util.EnumSet;

// Métodos de fábrica — não tem construtor público
EnumSet<DiaDaSemana> uteis     = EnumSet.range(DiaDaSemana.SEGUNDA, DiaDaSemana.SEXTA);
EnumSet<DiaDaSemana> fimDeSem  = EnumSet.of(DiaDaSemana.SABADO, DiaDaSemana.DOMINGO);
EnumSet<DiaDaSemana> todos     = EnumSet.allOf(DiaDaSemana.class);
EnumSet<DiaDaSemana> vazio     = EnumSet.noneOf(DiaDaSemana.class);
EnumSet<DiaDaSemana> naoUteis  = EnumSet.complementOf(uteis);

System.out.println(uteis.contains(DiaDaSemana.TERCA)); // true
System.out.println(uteis.containsAll(fimDeSem));        // false
```

Null não é permitido como elemento. Iteração ocorre na ordem de declaração do enum.

| | `EnumMap` | `HashMap` |
|---|---|---|
| Chave | Apenas enum | Qualquer tipo |
| Estrutura interna | Array por ordinal | Hash table |
| Custo de lookup | O(1) sem hash | O(1) amortizado |
| Ordem das chaves | Declaração do enum | Não garantida |
| Null como chave | Não | Sim |

| | `EnumSet` | `HashSet` |
|---|---|---|
| Elemento | Apenas enum | Qualquer tipo |
| Estrutura interna | Bitvector (long/long[]) | Hash table |
| Custo de operação | O(1) bit op | O(1) amortizado |
| Ordem de iteração | Declaração do enum | Não garantida |
| Null elemento | Não | Sim |

---

### Enum como singleton

*Effective Java* (Joshua Bloch), Item 3, recomenda enum de elemento único como a melhor forma de implementar o padrão singleton em Java. As razões:

1. **Thread-safety garantida pela JVM** — a inicialização de constantes de enum é feita pelo class loader, que garante atomicidade sem necessidade de `synchronized` ou `volatile`.
2. **Proteção contra serialização** — a desserialização de objetos normais pode criar instâncias extras; para enum, a JVM garante que apenas a instância canônica exista.
3. **Proteção contra reflection** — `Constructor.newInstance()` lança `IllegalArgumentException` para enums, impedindo quebra via reflection.

```java
public enum Configuracao {
    INSTANCE;

    private final String ambiente;
    private final int maxConexoes;

    // Construtor (privado por padrão em enum)
    Configuracao() {
        this.ambiente    = System.getenv().getOrDefault("APP_ENV", "development");
        this.maxConexoes = 20;
    }

    public String getAmbiente()    { return ambiente; }
    public int    getMaxConexoes() { return maxConexoes; }
}
```

```java
// Acesso ao singleton — sempre a mesma instância
Configuracao cfg = Configuracao.INSTANCE;
System.out.println(cfg.getAmbiente());      // "development"
System.out.println(cfg.getMaxConexoes());   // 20

// Garantia de unicidade
System.out.println(Configuracao.INSTANCE == Configuracao.INSTANCE); // sempre true
```

Comparado ao singleton via double-checked locking, o enum é mais simples, seguro e idiomático em Java.

---

### Enum vs sealed classes

`sealed classes` (Java 17+) e enums resolvem problemas relacionados — hierarquias fechadas de tipos — mas em níveis distintos de granularidade.

| Critério | `enum` | `sealed class` |
|---|---|---|
| Instâncias | Fixas e únicas (constantes) | Múltiplas por subtype |
| Estado por instância | Compartilhado entre constantes do mesmo campo | Cada instância tem seu próprio estado |
| Subtipo | Não (cada constante é da mesma classe) | Sim (subclasses distintas) |
| Composição | Não pode estender outra classe | Subclasses podem ser classes completas |
| Pattern matching | `switch` sobre `enum` | `switch` com `instanceof` patterns |
| Caso de uso principal | Conjunto de valores fixos com comportamento | Modelagem de ADT (tipos algébricos) |

Escolha **enum** quando o domínio é um conjunto fixo de valores que compartilham a mesma estrutura (mesmo conjunto de campos). Escolha **sealed class** quando os variantes têm estruturas diferentes (ex: `Sucesso` com `valor`, `Erro` com `mensagem` e `codigo`).

```java
// Enum: todos os status têm o mesmo campo label
public enum ResultadoStatus { SUCESSO, ERRO_VALIDACAO, ERRO_SISTEMA }

// Sealed: variantes com estruturas diferentes
public sealed interface Resultado<T> permits Sucesso, Falha {}
public record Sucesso<T>(T valor)                  implements Resultado<T> {}
public record Falha<T>(String mensagem, int codigo) implements Resultado<T> {}
```

Gancho para: [[14 - Sealed classes e pattern matching]].

## Na prática

Modelando um fluxo de status de pedido com transições de estado encapsuladas no próprio enum:

```java
import java.util.EnumSet;
import java.util.Set;

public enum StatusPedido {

    RASCUNHO("Rascunho") {
        @Override
        public Set<StatusPedido> proximosPermitidos() {
            return EnumSet.of(PENDENTE, CANCELADO);
        }
    },

    PENDENTE("Pendente") {
        @Override
        public Set<StatusPedido> proximosPermitidos() {
            return EnumSet.of(CONFIRMADO, CANCELADO);
        }
    },

    CONFIRMADO("Confirmado") {
        @Override
        public Set<StatusPedido> proximosPermitidos() {
            return EnumSet.of(ENVIADO, CANCELADO);
        }
    },

    ENVIADO("Enviado") {
        @Override
        public Set<StatusPedido> proximosPermitidos() {
            return EnumSet.of(ENTREGUE);
        }
    },

    ENTREGUE("Entregue") {
        @Override
        public Set<StatusPedido> proximosPermitidos() {
            return EnumSet.noneOf(StatusPedido.class);
        }
    },

    CANCELADO("Cancelado") {
        @Override
        public Set<StatusPedido> proximosPermitidos() {
            return EnumSet.noneOf(StatusPedido.class);
        }
    };

    private final String label;

    StatusPedido(String label) { this.label = label; }

    public String getLabel() { return label; }

    public abstract Set<StatusPedido> proximosPermitidos();

    /** Verifica e executa a transição, lançando exceção se inválida. */
    public StatusPedido transicionarPara(StatusPedido proximo) {
        if (!proximosPermitidos().contains(proximo)) {
            throw new IllegalStateException(
                "Transição inválida: " + this.label + " → " + proximo.label
            );
        }
        return proximo;
    }

    public boolean isFinal() { return proximosPermitidos().isEmpty(); }
}
```

```java
// Uso
StatusPedido status = StatusPedido.PENDENTE;
status = status.transicionarPara(StatusPedido.CONFIRMADO); // OK
status = status.transicionarPara(StatusPedido.ENVIADO);    // OK

try {
    status.transicionarPara(StatusPedido.RASCUNHO); // lança IllegalStateException
} catch (IllegalStateException e) {
    System.out.println(e.getMessage()); // "Transição inválida: Enviado → Rascunho"
}

System.out.println(StatusPedido.ENTREGUE.isFinal()); // true
```

Esse padrão centraliza as regras de transição no próprio tipo, eliminando condicionais espalhadas e garantindo que o compilador force a implementação de `proximosPermitidos` em cada constante nova.

## Armadilhas

### (1) Persistir ou serializar `ordinal()` em vez de `name()`

**O problema:** `ordinal()` retorna a posição de declaração da constante (0, 1, 2...). Ao persistir esse número em banco de dados, arquivo, ou mensagem — e depois inserir, remover ou reordenar constantes — todos os valores armazenados ficam desalinhados silenciosamente.

```java
// PROBLEMA: salvar ordinal no banco
public enum Prioridade { BAIXA, MEDIA, ALTA }

// Salvo no banco: BAIXA=0, MEDIA=1, ALTA=2

// Desenvolvedor insere URGENTE antes de ALTA:
public enum Prioridade { BAIXA, MEDIA, URGENTE, ALTA }

// Agora: BAIXA=0, MEDIA=1, URGENTE=2, ALTA=3
// Registros antigos com valor "2" agora apontam para URGENTE, não ALTA!
// Nenhum erro em runtime — corrupção silenciosa de dados.
```

**Fix:** persistir sempre `name()` (ou um campo estável dedicado), nunca `ordinal()`.

```java
public enum Prioridade {
    BAIXA("LOW"),
    MEDIA("MEDIUM"),
    URGENTE("URGENT"),
    ALTA("HIGH");

    private final String codigo; // campo estável para persistência

    Prioridade(String codigo) { this.codigo = codigo; }
    public String getCodigo() { return codigo; }

    public static Prioridade fromCodigo(String codigo) {
        for (Prioridade p : values()) {
            if (p.codigo.equals(codigo)) return p;
        }
        throw new IllegalArgumentException("Código desconhecido: " + codigo);
    }
}
```

Use `ordinal()` apenas quando a posição relativa tiver semântica intrínseca e estável (ex: comparação de ordem), mas nunca como identificador persistido.

---

### (2) `switch` sobre enum sem cobrir todos os casos

**O problema:** ao usar `switch` sobre enum com `case` somente para algumas constantes, novas constantes adicionadas ao enum passam pelo `switch` sem tratamento — muitas vezes caindo em `default` silencioso ou, se não houver `default`, simplesmente sem execução.

```java
public enum Nivel { INICIANTE, ADEPTO, MAGUS }

// PROBLEMA: switch sem default + nova constante não coberta
public String descricaoNivel(Nivel nivel) {
    return switch (nivel) {
        case INICIANTE -> "Aprendiz";
        case ADEPTO    -> "Praticante";
        // MAGUS foi esquecido — não há erro de compilação com switch tradicional
        // Com switch expression sem default, o compilador alerta — mas só no Java moderno
    };
}
```

Com o `switch` expression (Java 14+), o compilador **exige** cobertura total para enums — o que é uma vantagem. Já o `switch` statement clássico não exige cobertura e falha silenciosamente.

**Fix:** use `switch` expression moderno (sem `default` quando quiser que o compilador force cobertura de todos os casos), ou adicione um `default` que lance exceção para detectar constantes não tratadas:

```java
// Opção 1: switch expression — compilador exige cobertura total
public String descricaoNivel(Nivel nivel) {
    return switch (nivel) {
        case INICIANTE -> "Aprendiz";
        case ADEPTO    -> "Praticante";
        case MAGUS     -> "Mestre";
        // Sem default: compilador garante que todos os cases estão cobertos
    };
}

// Opção 2: switch statement com default seguro
public String descricaoNivel(Nivel nivel) {
    switch (nivel) {
        case INICIANTE: return "Aprendiz";
        case ADEPTO:    return "Praticante";
        case MAGUS:     return "Mestre";
        default:
            throw new IllegalArgumentException("Nível não tratado: " + nivel);
    }
}
```

---

### (3) Enum com estado mutável

**O problema:** campos mutáveis em enum quebram a garantia semântica de constante. Como cada constante é um singleton (uma única instância por JVM), mutações afetam globalmente todas as partes do sistema que usam aquela constante.

```java
public enum Configuracao {
    PRODUCAO, DESENVOLVIMENTO;

    private String urlBanco; // PROBLEMA: campo mutável

    public void setUrlBanco(String url) { this.urlBanco = url; } // PERIGO
    public String getUrlBanco()         { return urlBanco; }
}

// Em algum ponto do código:
Configuracao.PRODUCAO.setUrlBanco("jdbc:postgresql://prod-server/db");

// Em outro thread ou módulo:
Configuracao.PRODUCAO.getUrlBanco(); // estado global compartilhado — imprevisível
```

**Consequências:** comportamento dependente de ordem de execução, problemas em ambientes multi-thread sem sincronização, e dificuldade extrema de rastrear quem alterou o estado.

**Fix:** campos de enum devem ser `final` e inicializados no construtor. Se precisar de configuração dinâmica, use um `Map` externo ou injeção de dependência — não o enum.

```java
public enum Configuracao {
    PRODUCAO("jdbc:postgresql://prod-server/db"),
    DESENVOLVIMENTO("jdbc:h2:mem:testdb");

    private final String urlBanco; // imutável — correto

    Configuracao(String urlBanco) { this.urlBanco = urlBanco; }
    public String getUrlBanco()   { return urlBanco; }
}
```

## Em entrevista

### Frase pronta (inglês)

> "Enums in Java are not just named constants — they are full-fledged classes where each constant is a singleton instance, which means they can carry immutable state and behavior, making them ideal for modeling domain concepts like status codes or operation types." "When you need to associate data with each constant, the trade-off is between keeping state in the enum itself (simple, centralized) versus an external map — but once you add mutable state, you break the implicit singleton guarantee and introduce hidden global state shared across the entire JVM." "For collections of enum keys or values, `EnumMap` and `EnumSet` are the right choice over `HashMap` and `HashSet` — `EnumMap` uses an array indexed by ordinal so there is no hashing at all, and `EnumSet` uses a bit vector that fits 64 constants in a single `long` — both are O(1) and significantly faster; the caveat is that null keys or elements are not allowed."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| tipo enumerado | enum type |
| constante de enum | enum constant |
| corpo de método específico da constante | constant-specific method body |
| método abstrato por constante | per-constant abstract method |
| singleton via enum | enum singleton |
| segurança de tipo | type safety |
| vetor de bits / bitvector | bit vector |
| mapa com array interno | array-backed map |
| constante de tempo de compilação | compile-time constant |
| ordinal | ordinal |
| serialização segura | serialization-safe |

## Veja também

- [[07 - Herança e polimorfismo]]
- [[14 - Sealed classes e pattern matching]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [Enum Types — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/javaOO/enum.html)
- [java.lang.Enum — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Enum.html)
- [EnumMap — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/EnumMap.html)
- [EnumSet — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/EnumSet.html)
- [Effective Java, 3rd ed. — Item 3: Enforce the singleton property with a private constructor or an enum type (Joshua Bloch)](https://www.oreilly.com/library/view/effective-java/9780134686097/)
- [Effective Java, 3rd ed. — Item 34: Use enums instead of int constants (Joshua Bloch)](https://www.oreilly.com/library/view/effective-java/9780134686097/)
