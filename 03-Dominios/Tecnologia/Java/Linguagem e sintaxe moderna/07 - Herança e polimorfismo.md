---
title: "Herança e polimorfismo"
created: 2026-06-02
updated: 2026-06-02
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - linguagem
  - adepto
  - oop
  - polimorfismo
aliases:
  - Herança
  - Polimorfismo
  - Overriding
---

# Herança e polimorfismo

> [!abstract] TL;DR
> **Herança** (`extends`) permite que uma subclasse reutilize e especialize o comportamento de uma superclasse. **Polimorfismo dinâmico** (virtual method invocation) garante que a JVM chame a implementação correta em runtime com base no tipo real do objeto, não no tipo da referência. **Overriding** (sobrescrita) é resolvido em runtime — mesma assinatura, subclasse redefine o método; **overloading** (sobrecarga) é resolvido em compile-time — mesmo nome, parâmetros diferentes. O **contrato `equals`/`hashCode`** da classe `Object` é a pedra angular da corretude em coleções: objetos iguais segundo `equals` devem produzir o mesmo `hashCode`; sobrescrever um sem o outro quebra `HashMap`, `HashSet` e qualquer estrutura baseada em hash.

## O que é

**Herança** é o mecanismo pelo qual uma classe (subclasse) adquire o estado e o comportamento de outra (superclasse). Em Java, herança tem dois papéis distintos:

- **Reuso de implementação** — a subclasse herda métodos e campos da superclasse, evitando duplicação de código.
- **Subtipagem** — um objeto da subclasse pode ser tratado como instância da superclasse. Isso é a base do polimorfismo.

**Polimorfismo** (do grego: "muitas formas") é a capacidade de um mesmo código operar sobre objetos de tipos diferentes. Em Java OOP, o polimorfismo mais relevante é o **polimorfismo dinâmico** (ou de subtipo): dado que `Cachorro extends Animal`, uma referência do tipo `Animal` pode apontar para um objeto `Cachorro`, e a chamada `animal.fazerSom()` executará o método de `Cachorro` — não o de `Animal` — em tempo de execução.

```java
Animal animal = new Cachorro();  // referência Animal, objeto Cachorro
animal.fazerSom();               // chama Cachorro.fazerSom() — polimorfismo em ação
```

Isso permite escrever código que lida com uma abstração (`Animal`) e continua correto quando novos subtipos são introduzidos (`Gato`, `Pato`) — sem alterar o código existente.

## Como funciona

### `extends` e `super`

A palavra-chave `extends` estabelece a relação de herança. Uma classe pode estender apenas uma superclasse (herança simples). Todos os membros não-`private` da superclasse ficam disponíveis na subclasse.

```java
public class Veiculo {
    protected String marca;
    protected int anoFabricacao;

    public Veiculo(String marca, int anoFabricacao) {
        this.marca = marca;
        this.anoFabricacao = anoFabricacao;
    }

    public String getDescricao() {
        return marca + " (" + anoFabricacao + ")";
    }
}

public class Carro extends Veiculo {
    private int numeroPortas;

    public Carro(String marca, int anoFabricacao, int numeroPortas) {
        super(marca, anoFabricacao);   // (1) deve ser a primeira instrução
        this.numeroPortas = numeroPortas;
    }

    @Override
    public String getDescricao() {
        return super.getDescricao() + " — " + numeroPortas + " portas";  // (2)
    }
}
```

Dois usos de `super`:

1. **`super(...)`** — chama o construtor da superclasse. Deve ser a primeira instrução do construtor da subclasse. Se a subclasse não chamar `super(...)` explicitamente, o compilador insere `super()` (sem argumentos) automaticamente — o que causa erro de compilação se a superclasse não tiver construtor sem argumentos.
2. **`super.metodo()`** — invoca a implementação do método na superclasse, útil para estender (e não substituir completamente) o comportamento.

**Regras fundamentais de herança:**

- Java suporta herança simples: uma classe pode ter apenas uma superclasse direta.
- Todos os membros `public` e `protected` (e package-private, se no mesmo pacote) são herdados.
- Campos `private` não são herdados (mas existem no objeto — acessíveis via getters/setters).
- Construtores não são herdados — a subclasse deve definir seus próprios construtores e chamar `super(...)`.

---

### Overriding vs overloading

Estes dois conceitos são frequentemente confundidos — mas operam em momentos completamente distintos.

**Overriding (sobrescrita)** — a subclasse redefine um método herdado da superclasse. A resolução acontece em **runtime** (dynamic dispatch): a JVM olha o tipo real do objeto para decidir qual implementação chamar.

Regras para overriding válido:
- Mesma assinatura (nome + parâmetros) que o método da superclasse.
- Tipo de retorno igual ou **covariante** (subtipo do retorno original — válido a partir do Java 5).
- Visibilidade **igual ou mais permissiva** (não pode reduzir: `public` → `protected` é proibido).
- Não pode lançar checked exceptions mais amplas que o método original.
- Métodos `static` não são sobrescritos — são *ocultados* (method hiding).
- A anotação `@Override` não é obrigatória, mas é obrigatória por convenção: ela faz o compilador verificar que existe de fato um método para sobrescrever, evitando bugs silenciosos.

**Overloading (sobrecarga)** — múltiplos métodos com o mesmo nome mas assinaturas diferentes (número ou tipo de parâmetros) na mesma classe (ou herdados). A resolução acontece em **compile-time** com base no tipo estático da referência, não no tipo real do objeto.

```java
// ---- Overloading: compile-time, mesmo nome, parâmetros diferentes ----
public class Formatador {
    public String formatar(int valor) {
        return String.valueOf(valor);
    }

    public String formatar(double valor) {          // sobrecarregado
        return String.format("%.2f", valor);
    }

    public String formatar(int valor, String prefixo) { // sobrecarregado
        return prefixo + valor;
    }
}

// ---- Overriding: runtime, mesma assinatura, subclasse redefine ----
public class Forma {
    public double area() { return 0.0; }
}

public class Circulo extends Forma {
    private final double raio;

    public Circulo(double raio) { this.raio = raio; }

    @Override
    public double area() {                          // override — resolved at runtime
        return Math.PI * raio * raio;
    }
}
```

| Aspecto | Overriding | Overloading |
|---|---|---|
| Onde ocorre | Superclasse × subclasse | Mesma classe (ou herança) |
| Assinatura | **Mesma** | **Diferente** (parâmetros) |
| Retorno | Igual ou covariante | Qualquer |
| Resolução | **Runtime** (dynamic dispatch) | **Compile-time** (tipo estático) |
| `@Override` | Recomendado | Não se aplica |
| Métodos `static` | Não (method hiding) | Sim |

---

### Polimorfismo dinâmico

O polimorfismo dinâmico (também chamado de *virtual method invocation*) é a consequência direta do overriding: quando um método é invocado por uma referência de superclasse, a JVM despacha para a implementação do tipo **real** do objeto, determinada em runtime.

```java
public abstract class Notificacao {
    public abstract void enviar(String mensagem);

    public void enviarComLog(String mensagem) {
        System.out.println("[LOG] Enviando: " + mensagem);
        enviar(mensagem);          // chama a implementação da subclasse concreta
    }
}

public class EmailNotificacao extends Notificacao {
    private final String destinatario;

    public EmailNotificacao(String destinatario) {
        this.destinatario = destinatario;
    }

    @Override
    public void enviar(String mensagem) {
        System.out.println("Email para " + destinatario + ": " + mensagem);
    }
}

public class SmsNotificacao extends Notificacao {
    private final String telefone;

    public SmsNotificacao(String telefone) {
        this.telefone = telefone;
    }

    @Override
    public void enviar(String mensagem) {
        System.out.println("SMS para " + telefone + ": " + mensagem);
    }
}

// Código cliente — não sabe qual implementação vai usar
List<Notificacao> canais = List.of(
    new EmailNotificacao("usuario@exemplo.com"),
    new SmsNotificacao("+5511999999999")
);

for (Notificacao n : canais) {
    n.enviarComLog("Seu pedido foi confirmado.");
    // Cada chamada despacha para a implementação correta em runtime
}
```

A JVM implementa isso via *vtable* (virtual method table): cada classe tem uma tabela de ponteiros para os métodos sobrescritos. Em runtime, a chamada consulta a vtable do tipo real — custo praticamente zero de overhead (uma indireção de ponteiro).

---

### `final` (classe/método/variável)

A palavra-chave `final` tem três usos distintos com semânticas próprias:

| Contexto | Efeito |
|---|---|
| `final class` | Classe não pode ser estendida. Exemplos: `String`, `Integer`. |
| `final method` | Método não pode ser sobrescrito por subclasses. |
| `final` variável/campo | Referência não pode ser reatribuída após inicialização. |

```java
public final class Imutavel {        // ninguém pode estender
    private final int valor;         // campo: não reatribuível

    public Imutavel(int valor) {
        this.valor = valor;
    }

    public final int getValor() {    // método: não sobrescrevível (redundante em final class)
        return valor;
    }
}
```

`final` em campo garante que a referência não muda — não que o objeto referenciado seja imutável. Um `final List<String>` não pode ser reatribuído, mas a lista em si pode ser modificada com `add()` e `remove()`.

---

### Métodos de `Object`: `equals`, `hashCode`, `toString`

Toda classe Java herda da classe `Object`. Os três métodos mais importantes para sobrescrever são `equals`, `hashCode` e `toString`.

#### O contrato de `equals`

Conforme documentado na API Java 21 (Oracle), o método `equals` implementa uma **relação de equivalência** sobre referências não-nulas, com as seguintes propriedades obrigatórias:

1. **Reflexivo**: para qualquer referência não-nula `x`, `x.equals(x)` deve retornar `true`.
2. **Simétrico**: para quaisquer referências não-nulas `x` e `y`, `x.equals(y)` deve retornar `true` se e somente se `y.equals(x)` retornar `true`.
3. **Transitivo**: para quaisquer referências não-nulas `x`, `y` e `z`, se `x.equals(y)` e `y.equals(z)` retornam `true`, então `x.equals(z)` também deve retornar `true`.
4. **Consistente**: múltiplas invocações de `x.equals(y)` devem retornar consistentemente `true` ou consistentemente `false`, desde que nenhuma informação usada nas comparações seja modificada.
5. **Nulo**: para qualquer referência não-nula `x`, `x.equals(null)` deve retornar `false`.

A implementação default de `Object.equals` compara por **identidade de referência** (`==`). Se você quer igualdade por valor (como em value objects), deve sobrescrever.

#### O contrato de `hashCode`

Conforme a API Java 21 (Oracle), o contrato de `hashCode` estabelece:

1. **Consistência**: invocado múltiplas vezes sobre o mesmo objeto durante a mesma execução da aplicação, `hashCode` deve retornar consistentemente o mesmo inteiro, desde que nenhuma informação usada nas comparações de `equals` seja modificada.
2. **Objetos iguais → mesmo hash**: se `x.equals(y)`, então `x.hashCode() == y.hashCode()`. **Esta é a regra mais crítica.**
3. **Objetos desiguais → hash diferente não obrigatório**: não é requerido que objetos desiguais produzam hashes distintos. Contudo, produzir hashes distintos para objetos desiguais **melhora o desempenho** de hash tables (menos colisões).

#### Por que sobrescrever os dois juntos

A relação entre `equals` e `hashCode` é assimétrica: `equals` implica `hashCode` igual, mas `hashCode` igual **não implica** `equals`. Isso cria uma armadilha clássica: se você sobrescreve `equals` sem sobrescrever `hashCode`, dois objetos que `equals` considera iguais poderão ter hashes diferentes. O resultado é que `HashMap`, `HashSet` e qualquer estrutura baseada em hash buscará o objeto em um bucket errado — e o objeto "desaparece" da coleção, mesmo estando logicamente presente.

A nota da API Java 21 é explícita: *"It is generally necessary to override the hashCode method whenever the equals method is overridden, so as to maintain the general contract for the hashCode method, which states that equal objects must have equal hash codes."*

A implementação default de `Object.hashCode` é baseada na identidade do objeto (geralmente derivada do endereço de memória). Após sobrescrever `equals` para igualdade por valor, o `hashCode` herdado passará a ser inconsistente com `equals`.

## Na prática

Implementando `equals` e `hashCode` corretamente para um value object:

```java
import java.util.Objects;

/**
 * Value object que representa um produto em um catálogo.
 * Dois produtos são iguais se têm o mesmo código SKU.
 */
public final class Produto {

    private final String sku;
    private final String nome;
    private final double preco;

    public Produto(String sku, String nome, double preco) {
        this.sku   = Objects.requireNonNull(sku,   "sku é obrigatório");
        this.nome  = Objects.requireNonNull(nome,  "nome é obrigatório");
        this.preco = preco;
    }

    public String getSku()   { return sku; }
    public String getNome()  { return nome; }
    public double getPreco() { return preco; }

    /**
     * Igualdade baseada em SKU — o identificador de negócio único.
     * Segue o contrato completo: reflexivo, simétrico, transitivo,
     * consistente, e x.equals(null) == false.
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;                          // reflexividade (e otimização)
        if (!(o instanceof Produto outro)) return false;     // null-safe + type check
        return Objects.equals(sku, outro.sku);               // igualdade por valor
    }

    /**
     * hashCode consistente com equals: dois produtos com mesmo SKU
     * produzem o mesmo hash — garantindo corretude em HashSet/HashMap.
     */
    @Override
    public int hashCode() {
        return Objects.hash(sku);   // delega para Objects.hash — seguro para null
    }

    @Override
    public String toString() {
        return "Produto[sku=" + sku + ", nome=" + nome + ", preco=" + preco + "]";
    }
}
```

```java
// Demonstração de corretude em coleção hash-based
Set<Produto> catalogo = new HashSet<>();
Produto p1 = new Produto("SKU-001", "Teclado", 150.0);
Produto p2 = new Produto("SKU-001", "Teclado Mecânico", 180.0); // mesmo SKU

catalogo.add(p1);
System.out.println(catalogo.contains(p2)); // true — equals + hashCode corretos
System.out.println(p1.equals(p2));         // true
System.out.println(p1.hashCode() == p2.hashCode()); // true
```

**`Objects.equals` e `Objects.hash`** (pacote `java.util`) são os helpers modernos:

- `Objects.equals(a, b)` — null-safe: retorna `true` se ambos são `null`, `false` se apenas um é `null`, e delega para `a.equals(b)` caso contrário.
- `Objects.hash(campo1, campo2, ...)` — combina múltiplos campos em um único hash, com tratamento correto de `null`. Substitui o idioma manual `31 * result + campo.hashCode()`.

> **Gancho:** `record` (Java 16+) gera `equals`, `hashCode` e `toString` automaticamente com base em todos os campos do componente — eliminando esse boilerplate por completo. Veja [[13 - Records e record patterns]].

## Armadilhas

### (1) Sobrescrever `equals` sem sobrescrever `hashCode`

**O problema:** o contrato exige que objetos iguais segundo `equals` produzam o mesmo `hashCode`. Se você sobrescreve `equals` mas não `hashCode`, o `hashCode` herdado de `Object` é baseado na identidade do objeto — não no valor. Dois objetos logicamente iguais terão hashes diferentes e serão armazenados em buckets diferentes em qualquer estrutura baseada em hash. O objeto "some" da coleção.

```java
public class Ponto {
    private final int x;
    private final int y;

    public Ponto(int x, int y) { this.x = x; this.y = y; }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Ponto p)) return false;
        return x == p.x && y == p.y;
    }

    // PROBLEMA: hashCode não foi sobrescrito.
    // Object.hashCode() retorna hash baseado em identidade (endereço de memória).
}

Set<Ponto> pontos = new HashSet<>();
Ponto a = new Ponto(1, 2);
Ponto b = new Ponto(1, 2);  // "igual" a 'a' segundo equals

pontos.add(a);
System.out.println(pontos.contains(b)); // FALSE — b vai para bucket errado!
System.out.println(a.equals(b));        // true — contradição!
```

**Fix:** sempre sobrescreva `hashCode` junto com `equals`.

```java
@Override
public int hashCode() {
    return Objects.hash(x, y);   // garante: equals true → hashCode igual
}
```

---

### (2) Confundir overloading (compile-time) com overriding (runtime)

**O problema:** overloading é resolvido em compile-time pelo **tipo estático** da referência, não pelo tipo real do objeto. Se você espera polimorfismo mas o método está sobrecarregado (não sobrescrito), o despacho vai para a versão errada.

```java
public class Processador {
    public void processar(Object obj) {
        System.out.println("processar(Object)");
    }

    public void processar(String s) {
        System.out.println("processar(String)");
    }
}

Processador p = new Processador();
Object valor = "texto";   // tipo estático: Object; tipo real: String

p.processar(valor);       // imprime "processar(Object)" — não "processar(String)"!
// Overloading usa o tipo ESTÁTICO (Object), não o tipo real (String)
```

O compilador vê `processar(Object)` porque o tipo estático de `valor` é `Object`. Para polimorfismo real, use overriding (subclasse com `@Override`), não overloading.

**Fix:** se precisar de comportamento diferente por tipo real, use `instanceof` / pattern matching, ou modele com overriding em uma hierarquia de classes.

```java
// Alternativa: overriding real na hierarquia
public abstract class Item {
    public abstract void processar();
}

public class ItemTexto extends Item {
    @Override
    public void processar() { System.out.println("processar texto"); }
}
```

---

### (3) Chamar método sobrescrevível no construtor da superclasse

**O problema:** quando o construtor da superclasse chama um método de instância que a subclasse sobrescreve, o método da subclasse é executado *antes* do construtor da subclasse rodar. Campos declarados na subclasse ainda têm seus valores default (`null`, `0`, `false`) nesse momento — o objeto está parcialmente inicializado.

```java
public class Validador {
    public Validador() {
        inicializar();   // PERIGO: chama método sobrescrevível
    }

    protected void inicializar() {
        System.out.println("Validador.inicializar");
    }
}

public class ValidadorDeEmail extends Validador {
    private final String dominio;  // campo da subclasse

    public ValidadorDeEmail(String dominio) {
        super();                   // chama Validador() → chama inicializar() sobrescrito
        this.dominio = dominio;    // inicializado DEPOIS do super()
    }

    @Override
    protected void inicializar() {
        // dominio ainda é null aqui — construtor da subclasse não rodou
        System.out.println("Domínio: " + dominio.toUpperCase()); // NullPointerException!
    }
}

new ValidadorDeEmail("empresa.com");  // lança NullPointerException
```

**Fix:** evite chamar métodos de instância sobrescritíveis no construtor. Prefira métodos `private` ou `final` (que não podem ser sobrescritos) para lógica de inicialização:

```java
public class Validador {
    public Validador() {
        inicializarInterno();   // private: não pode ser sobrescrito — seguro
    }

    private void inicializarInterno() { }  // sem polimorfismo, sem risco
}
```

Se precisar de lógica de inicialização polimórfica, use o padrão de fábrica: construa o objeto primeiro (via `new`), depois chame o método de inicialização no objeto já construído.

## Em entrevista

### Frase pronta (inglês)

> "When you override `equals` to define value equality, you must also override `hashCode` to maintain the contract that equal objects produce the same hash code — otherwise your objects will silently disappear from `HashSet` and `HashMap` because they end up in different buckets." "The trade-off in implementing `equals` is deciding which fields define identity: for a domain entity you might use only the business key, while for a value object you typically compare all fields — that decision belongs to the domain model, not to the infrastructure." "A subtle caveat is that overriding and overloading look similar but resolve at completely different times: overriding is resolved at runtime based on the actual type of the object, while overloading is resolved at compile-time based on the static type of the reference — so adding an overloaded method never gives you polymorphic dispatch."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| herança | inheritance |
| superclasse / classe pai | superclass / parent class |
| subclasse / classe filha | subclass / child class |
| sobrescrita | overriding |
| sobrecarga | overloading |
| polimorfismo dinâmico | dynamic polymorphism / virtual method invocation |
| despacho dinâmico | dynamic dispatch |
| covariância de retorno | covariant return type |
| contrato equals/hashCode | equals/hashCode contract |
| classe selada | sealed class |
| vinculação em tempo de execução | runtime binding / late binding |
| vinculação em tempo de compilação | compile-time binding / early binding |

## Veja também

- [[06 - Classes, objetos e encapsulamento]]
- [[08 - Interfaces e classes abstratas]]
- [[09 - Enums]]
- [[13 - Records e record patterns]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [Object.equals — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html#equals(java.lang.Object))
- [Object.hashCode — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html#hashCode())
- [Object.toString — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html#toString())
- [Inheritance — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/IandI/subclasses.html)
- [Overriding and Hiding Methods — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/IandI/override.html)
