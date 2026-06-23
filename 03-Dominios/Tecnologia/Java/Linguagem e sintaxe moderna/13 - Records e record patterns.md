---
title: "Records e record patterns"
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
  - records
  - imutabilidade
aliases:
  - Record
  - Records
  - record patterns
---

# Records e record patterns

> [!abstract] TL;DR
> **Records** (Java 16, GA) são classes portadoras de dados imutáveis e transparentes: declara-se `record Point(int x, int y) {}` e o compilador gera construtor canônico, accessors `x()` / `y()` (sem prefixo `get`), `equals`, `hashCode` e `toString`. O **compact constructor** (sem lista de parâmetros) permite validação e normalização, com atribuição implícita dos componentes no final. **Record patterns** (Java 21, GA) permitem desestruturar records diretamente em `instanceof` e `switch`, inclusive de forma aninhada. A imutabilidade é **rasa**: os campos são `final`, mas referências para objetos mutáveis continuam mutáveis. Use records para DTOs, value objects e tuplas; evite-os como entidades JPA.

## O que é

Um **record** é uma classe especial que o compilador trata como portadora de dados imutável e transparente. Ao declarar:

```java
public record Point(int x, int y) {}
```

o compilador gera automaticamente uma classe equivalente a:

```java
public final class Point extends java.lang.Record {
    private final int x;
    private final int y;

    // Construtor canônico — mesmo header da declaração
    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    // Accessors — nome idêntico ao componente, sem prefixo "get"
    public int x() { return x; }
    public int y() { return y; }

    // equals, hashCode, toString baseados em todos os componentes
    @Override public boolean equals(Object o) { ... }
    @Override public int hashCode() { ... }
    @Override public String toString() { return "Point[x=" + x + ", y=" + y + "]"; }
}
```

Quatro pontos centrais sobre o que o compilador gera:

1. **Campos privados e finais** — um para cada componente declarado no header.
2. **Construtor canônico** — assinatura exatamente igual à da declaração; nenhum parâmetro adicional.
3. **Accessors** — um método público por componente, com o mesmo nome (`x()`, não `getX()`). Frameworks que dependem da convenção JavaBean (`getX()`) precisarão de atenção especial.
4. **`equals` / `hashCode` / `toString`** — baseados em todos os componentes via deep structural equality.

Records são implicitamente `final` (não podem ser estendidos) e estendem implicitamente `java.lang.Record` (não podem estender qualquer outra classe). Podem, porém, implementar interfaces.

## Como funciona

### Declaração e componentes

A sintaxe mínima é o nome seguido da lista de componentes entre parênteses:

```java
// Record simples
public record Point(int x, int y) {}

// Record com componentes de tipos ricos
public record Money(BigDecimal amount, String currencyCode) {}

// Record genérico
public record Pair<A, B>(A first, B second) {}
```

Uso — o accessor tem o mesmo nome do componente, sem `get`:

```java
var p = new Point(3, 4);
int xCoord = p.x();    // p.getX() NÃO existe — é p.x()
int yCoord = p.y();

System.out.println(p); // "Point[x=3, y=4]" — toString gerado
```

Nenhuma instância de campo extra pode ser declarada. Campos `static` são permitidos:

```java
public record Money(BigDecimal amount, String currencyCode) {
    // Permitido: campo estático
    private static final String DEFAULT_CURRENCY = "BRL";

    // ERRO de compilação: campo de instância extra não é permitido
    // private String description;  // ❌
}
```

---

### Compact constructor e validação

O **compact constructor** omite a lista de parâmetros: o compilador disponibiliza as variáveis de componente para uso dentro do bloco, e a atribuição `this.campo = campo` é inserida implicitamente ao final. Isso é o local canônico para validação e normalização:

```java
public record Patient(Long id, String name, LocalDate birthDate, String email) {

    // Compact constructor — sem parâmetros explícitos
    public Patient {
        Objects.requireNonNull(id, "id is required");

        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("name is required");
        }

        if (birthDate != null && birthDate.isAfter(LocalDate.now())) {
            throw new IllegalArgumentException("birthDate cannot be in the future");
        }

        // Normalização: reatribuição permitida antes da atribuição implícita
        name  = name.strip();
        email = email != null ? email.toLowerCase() : null;

        // Aqui o compilador insere implicitamente:
        //   this.id        = id;
        //   this.name      = name;      // já normalizado
        //   this.birthDate = birthDate;
        //   this.email     = email;     // já normalizado
    }
}
```

Regras do compact constructor:

- Sem lista de parâmetros — os nomes dos componentes são variáveis já disponíveis.
- Pode reatribuir as variáveis de componente antes da atribuição implícita (normalização).
- Não pode acessar `this.campo` — os campos ainda não foram atribuídos nesse ponto.
- A atribuição implícita ocorre no final, **depois** de qualquer código do bloco.

---

### Métodos adicionais e estáticos

Records podem conter métodos de instância, métodos estáticos e static factories. O que não podem ter é campo de instância adicional além dos componentes declarados:

```java
public record Money(BigDecimal amount, String currencyCode) {

    // Validação no compact constructor
    public Money {
        Objects.requireNonNull(amount, "amount required");
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("amount cannot be negative");
        }
    }

    // Método de negócio — pode existir normalmente
    public Money add(Money other) {
        if (!this.currencyCode.equals(other.currencyCode)) {
            throw new IllegalArgumentException("currency mismatch");
        }
        return new Money(this.amount.add(other.amount), this.currencyCode);
    }

    public boolean isZero() {
        return amount.compareTo(BigDecimal.ZERO) == 0;
    }

    // Static factory — cria instância com intenção explícita
    public static Money zero(String currencyCode) {
        return new Money(BigDecimal.ZERO, currencyCode);
    }

    public static Money of(double amount, String currencyCode) {
        return new Money(BigDecimal.valueOf(amount), currencyCode);
    }
}
```

Também é possível sobrescrever os accessors gerados — a assinatura deve ser exatamente a mesma (nome e tipo de retorno):

```java
public record Temperature(double celsius) {

    // Sobrescreve o accessor gerado — mesma assinatura obrigatória
    @Override
    public double celsius() {
        return Math.round(celsius * 100.0) / 100.0; // arredonda
    }

    // Accessor adicional conveniente (não é gerado automaticamente)
    public double fahrenheit() {
        return celsius * 9.0 / 5.0 + 32;
    }
}
```

---

### Records + interfaces

Records podem implementar interfaces. Isso é especialmente útil para plugá-los em hierarquias existentes:

```java
public interface Identifiable {
    Long id();  // mesmo nome que o accessor de record
}

// Record já implementa id() pelo accessor automático — zero código extra
public record Patient(Long id, String name) implements Identifiable {}
```

Quando a interface declara um método com o mesmo nome e tipo de retorno de um componente, o accessor gerado satisfaz automaticamente o contrato da interface.

Records **não podem** estender classes (não é possível `record Foo(...) extends Bar`). A única superclasse implícita é `java.lang.Record`. A combinação natural com [[14 - Sealed classes e pattern matching]] é usar records como subtipos de interfaces seladas:

```java
// Interface selada define hierarquia fechada
public sealed interface Shape permits Circle, Rectangle, Triangle {}

// Subtipos como records — imutáveis e transparentes
public record Circle(double radius) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}
public record Triangle(double base, double height) implements Shape {}
```

---

### Record patterns (Java 21)

**Record patterns** (JEP 440, GA no Java 21) permitem desestruturar um record diretamente no padrão de um `instanceof` ou `switch`, vinculando as variáveis dos componentes no mesmo passo:

```java
record Point(int x, int y) {}
record Circle(Point center, double radius) {}

// Sem record patterns — verbose
if (obj instanceof Circle c) {
    Point center = c.center();
    double r = c.radius();
    System.out.println("Centro: " + center.x() + "," + center.y() + " raio: " + r);
}

// Com record patterns — desestruturação direta
if (obj instanceof Circle(Point(int x, int y), double r)) {
    System.out.println("Centro: " + x + "," + y + " raio: " + r);
}
```

O tipo pode ser inferido usando `var`:

```java
if (obj instanceof Circle(Point(var x, var y), var r)) {
    System.out.println(x + " " + y + " " + r);
}
```

**Aninhamento** funciona de forma recursiva — cada componente pode ser, ele mesmo, um pattern:

```java
record ColoredPoint(Point point, String color) {}
record Box(ColoredPoint topLeft, ColoredPoint bottomRight) {}

void printBox(Object obj) {
    if (obj instanceof Box(
            ColoredPoint(Point(var x1, var y1), var color1),
            ColoredPoint(Point(var x2, var y2), var color2))) {
        System.out.printf("(%d,%d)[%s] → (%d,%d)[%s]%n",
            x1, y1, color1, x2, y2, color2);
    }
}
```

**Em `switch` com guarda (`when`):**

```java
String describe(Object obj) {
    return switch (obj) {
        case Circle(Point(int x, int y), double r) when r > 10
            -> "Grande círculo em (" + x + "," + y + ")";
        case Circle(Point p, double r)
            -> "Círculo pequeno, raio " + r;
        case Rectangle(double w, double h) when w == h
            -> "Quadrado de lado " + w;
        case Rectangle(double w, double h)
            -> "Retângulo " + w + "×" + h;
        case null   -> "nulo";
        default     -> "desconhecido";
    };
}
```

Quando combinados com interfaces seladas, o compilador verifica a **exaustividade**: todos os subtipos cobertos no `switch` dispensam o `default`. Veja [[14 - Sealed classes e pattern matching]] para detalhes sobre exhaustiveness checking.

---

### Imutabilidade rasa vs profunda

A imutabilidade dos records é **rasa** (*shallow*): os campos são `final`, o que impede reatribuição de referência — mas não impede a mutação do objeto referenciado. Um `record Foo(List<String> items)` tem o campo `items` final, porém `foo.items().add("extra")` compila e executa sem erros.

```java
public record NameList(List<String> names) {}

// O campo 'names' é final — não pode ser reatribuído
// Mas a lista em si é mutável
var nl = new NameList(new ArrayList<>(List.of("Ana", "Bruno")));
nl.names().add("Carlos");    // ✅ compila e executa — names é mutável
System.out.println(nl);      // "NameList[names=[Ana, Bruno, Carlos]]"
```

Para imutabilidade real com coleções, aplique defensive copy no compact constructor:

```java
public record NameList(List<String> names) {

    // Defensive copy — protege contra mutação externa
    public NameList {
        names = List.copyOf(names);  // cria lista imutável
    }
}

var lista = new ArrayList<>(List.of("Ana", "Bruno"));
var nl = new NameList(lista);
lista.add("Carlos");          // mutação na lista original
System.out.println(nl);       // "NameList[names=[Ana, Bruno]]" — não afetado
```

O mesmo princípio se aplica a arrays: `int[]`, `byte[]` e qualquer array são mutáveis mesmo dentro de um record; deve-se usar `Arrays.copyOf` no compact constructor e retornar uma cópia defensiva no accessor sobrescrito, se for expor o array.

## Na prática

**DTOs e value objects** são os casos de uso primários de records. Eliminam o boilerplate de classes anêmicas com dezenas de linhas de getters, `equals` e `toString`:

```java
// DTO de request — validações com Bean Validation
public record CreatePatientRequest(
    @NotBlank String name,
    @Email @NotBlank String email,
    @Past @NotNull LocalDate birthDate
) {}

// DTO de response com static factory
public record PatientResponse(Long id, String name, String email, int age) {

    public static PatientResponse from(Patient patient) {
        return new PatientResponse(
            patient.getId(),
            patient.getName(),
            patient.getEmail(),
            Period.between(patient.getBirthDate(), LocalDate.now()).getYears()
        );
    }
}

// Controller — limpo, sem cerimônia
@PostMapping("/patients")
public PatientResponse create(@Valid @RequestBody CreatePatientRequest req) {
    Patient saved = service.create(req);
    return PatientResponse.from(saved);
}
```

**Em Spring Boot**, records funcionam bem como corpos de request/response com `@RequestBody` (Jackson serializa/deserializa sem configuração extra a partir do Jackson 2.12+). Para `@ConfigurationProperties`, o suporte a records foi adicionado no Spring Boot 2.6+:

```java
@ConfigurationProperties(prefix = "app.mail")
public record MailProperties(
    String host,
    int port,
    String username,
    boolean ssl
) {}
```

**JPA e `@Entity`**: records não funcionam diretamente como entidades JPA. O motivo é que a especificação JPA exige um construtor sem argumentos e a possibilidade de atribuir campos (setters ou acesso por reflection). Records não têm construtor sem-arg gerado pelo compilador, seus campos são `final` e a classe é `final` — incompatível com o modelo de proxy que frameworks como Hibernate utilizam. Use classes normais (ou `@Embeddable` para value objects em JPA) para entidades, e records apenas para DTOs e projections:

```java
// Projeção em Spring Data JPA — record funciona aqui
public record PatientSummary(Long id, String name) {}

// Uso com JPQL
@Query("SELECT new com.example.dto.PatientSummary(p.id, p.name) FROM Patient p WHERE p.active = true")
List<PatientSummary> findActiveSummaries();
```

## Armadilhas

### (1) Componente mutável — imutabilidade só na referência

**O problema:** um record com `List`, `Map`, `Date` ou array como componente parece imutável mas não é. O campo `final` bloqueia reatribuição da referência; a mutação do objeto em si ainda é possível.

```java
public record Config(List<String> allowedHosts) {}

var hosts = new ArrayList<>(List.of("api.example.com"));
var config = new Config(hosts);

// Problema 1: o chamador ainda tem a referência e pode mutar
hosts.add("evil.example.com");
System.out.println(config.allowedHosts()); // [api.example.com, evil.example.com] — vazou!

// Problema 2: quem obtém via accessor também pode mutar
config.allowedHosts().clear();             // ✅ compila — esvazia a lista dentro do record
```

**Fix:** defensive copy no compact constructor + retorno imutável no accessor:

```java
public record Config(List<String> allowedHosts) {

    public Config {
        allowedHosts = List.copyOf(allowedHosts); // copia e torna imutável
    }
}

var hosts = new ArrayList<>(List.of("api.example.com"));
var config = new Config(hosts);
hosts.add("evil.example.com");             // não afeta mais o record
config.allowedHosts().add("x");            // lança UnsupportedOperationException
```

---

### (2) Esperar encapsulamento — todos os componentes são expostos

**O problema:** records são classes **transparentes** por design. Cada componente declarado gera um accessor público. Não há como declarar um componente e deixá-lo privado ou acessível apenas via método customizado com lógica de controle de acesso.

```java
public record CreditCard(String number, String cvv, LocalDate expiry) {}

CreditCard card = new CreditCard("4111111111111111", "123", LocalDate.of(2027, 12, 1));

// Todos os componentes expostos publicamente — nenhuma proteção
String cvv = card.cvv();    // acessível sem restrição
System.out.println(card);   // "CreditCard[number=4111..., cvv=123, expiry=2027-12-01]" — CVV no log!
```

**Fix:** se o domínio exige controle de acesso ou ocultação de dados, use uma classe comum com `private` fields e accessors seletivos. Se mesmo assim quiser um record, sobrescreva `toString()` para omitir dados sensíveis:

```java
public record CreditCard(String number, String cvv, LocalDate expiry) {

    @Override
    public String toString() {
        // Nunca logar CVV — sobrescreve o toString gerado
        return "CreditCard[number=****" + number.substring(number.length() - 4)
             + ", expiry=" + expiry + "]";
    }
}
```

Mas tenha em mente: o accessor `cvv()` ainda é público. Para encapsulamento real, use uma classe.

---

### (3) Tentar usar record como entidade JPA

**O problema:** records são `final` e seus campos são `final`. JPA (via Hibernate/EclipseLink) exige:
- Construtor sem argumentos (`public` ou `protected`)
- Campos não-`final` (para atribuição pós-construção)
- Classe não-`final` (para geração de proxy/subclasse lazy loading)

Nenhuma dessas condições é satisfeita por um record:

```java
// ERRO em tempo de inicialização do contexto Spring/JPA
@Entity
@Table(name = "patients")
public record Patient(
    @Id Long id,
    String name,
    String email
) {}
// HibernateException: No default constructor for entity: Patient
// (e outros erros similares dependendo do provider)
```

**Fix:** use uma classe normal para `@Entity`. Use records apenas para DTOs e projections:

```java
// Entidade — classe normal
@Entity
@Table(name = "patients")
public class Patient {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String email;

    protected Patient() {}  // JPA precisa do no-arg constructor

    public Patient(String name, String email) {
        this.name = name;
        this.email = email;
    }

    // getters...
}

// DTO de resposta — record é perfeito aqui
public record PatientResponse(Long id, String name, String email) {
    public static PatientResponse from(Patient p) {
        return new PatientResponse(p.getId(), p.getName(), p.getEmail());
    }
}
```

## Em entrevista

### Frase pronta (inglês)

> "Records in Java 16 are transparent data carriers: the compiler generates the canonical constructor, field-named accessors without the 'get' prefix, and structural `equals`, `hashCode`, and `toString` — eliminating the boilerplate that used to justify Lombok for pure data classes."

> "The immutability guarantee is shallow, not deep: the record's fields are `final`, which prevents re-assignment of the references, but if a component holds a mutable object like a `List` or an array, the contents can still be modified; the fix is a defensive copy in the compact constructor using `List.copyOf` or `Arrays.copyOf`."

> "In practice I use records for DTOs and value objects — request/response bodies in REST APIs, configuration properties in Spring Boot, and projections in Spring Data queries — but I avoid them as JPA entities because the `final` class and `final` fields are incompatible with the proxy-based lazy loading that Hibernate relies on; for entities, plain classes remain the right choice."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| registro / record | record |
| componente de record | record component |
| construtor canônico | canonical constructor |
| construtor compacto | compact constructor |
| accessor (sem prefixo get) | accessor / component accessor |
| imutabilidade rasa | shallow immutability |
| cópia defensiva | defensive copy |
| desestruturação / record pattern | deconstruction / record pattern |
| classe portadora de dados | data carrier class |
| objeto de valor | value object |

## Veja também

- [[06 - Classes, objetos e encapsulamento]]
- [[07 - Herança e polimorfismo]]
- [[14 - Sealed classes e pattern matching]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [JEP 395: Records](https://openjdk.org/jeps/395) — especificação original; records GA no Java 16
- [JEP 440: Record Patterns](https://openjdk.org/jeps/440) — record patterns GA no Java 21
- [Record Classes — Oracle Java 21 Language Guide](https://docs.oracle.com/en/java/javase/21/language/records.html)
- [Record Patterns — Oracle Java 21 Language Guide](https://docs.oracle.com/en/java/javase/21/language/record-patterns.html)
