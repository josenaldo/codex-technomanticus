---
title: "Classes, objetos e encapsulamento"
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
  - encapsulamento
aliases:
  - Classes
  - Encapsulamento
---

# Classes, objetos e encapsulamento

> [!abstract] TL;DR
> Uma **classe** é o molde; um **objeto** é a instância criada a partir dele. O construtor inicializa o estado — sobrecarregue-o com **constructor overloading** e delegue via `this()`. **Membros estáticos** pertencem à classe (compartilhados); membros de instância pertencem ao objeto. **Modificadores de acesso** (`public` / `protected` / package-private / `private`) controlam visibilidade com granularidade de classe, pacote, subclasse e mundo. **Encapsulamento** esconde o estado interno atrás de uma interface pública controlada. **Imutabilidade** elimina uma classe inteira de bugs: campos `final`, sem setters, defensive copy de mutáveis — e `record` (Java 16+) entrega tudo isso com zero boilerplate.

## O que é

Em Java, uma **classe** é um molde que define dois aspectos de uma entidade:

- **Estado** — os dados que o objeto carrega, representados pelos seus *campos* (`fields`)
- **Comportamento** — o que o objeto sabe fazer, representado pelos seus *métodos*

Um **objeto** é uma *instância* concreta criada a partir desse molde. Cada objeto tem seu próprio espaço de memória para os campos de instância, mas compartilha a definição dos métodos com todos os outros objetos da mesma classe.

```java
// O molde (classe)
public class Termostato {
    private int temperatura;       // estado
    public void ajustar(int t) {   // comportamento
        this.temperatura = t;
    }
}

// A instância (objeto)
Termostato sala = new Termostato();   // objeto criado no heap
Termostato cozinha = new Termostato(); // outro objeto, outro espaço de estado
```

`sala` e `cozinha` são objetos independentes — cada um tem sua própria `temperatura`. O operador `new` aloca memória no heap e chama o construtor para inicializar o estado.

## Como funciona

### Construtores e `this`

O construtor é chamado exatamente uma vez por objeto, no momento em que ele é criado via `new`. Sua responsabilidade é deixar o objeto em um estado válido e consistente.

**Overloading de construtor** — uma mesma classe pode ter múltiplos construtores com assinaturas diferentes (número ou tipos de parâmetros distintos):

```java
public class Produto {
    private final String codigo;
    private final String nome;
    private final double preco;
    private final String categoria;

    // Construtor completo
    public Produto(String codigo, String nome, double preco, String categoria) {
        this.codigo    = codigo;
        this.nome      = nome;
        this.preco     = preco;
        this.categoria = categoria;
    }

    // Construtor auxiliar — delega ao principal via this()
    public Produto(String codigo, String nome, double preco) {
        this(codigo, nome, preco, "GERAL");   // this() deve ser a primeira instrução
    }
}
```

A chamada `this(...)` invoca outro construtor da *mesma* classe e deve ser a **primeira instrução** do corpo do construtor que a usa. Isso evita duplicação de lógica de inicialização.

**Construtor default:** se nenhum construtor é declarado, o compilador gera automaticamente um construtor sem argumentos que chama `super()`. Assim que você declara *qualquer* construtor, o default deixa de existir — se precisar dele, declare-o explicitamente.

**Ordem de inicialização** em uma instância (garantida pela JVM):

```text
1. Valores default dos campos (0, null, false) — antes de qualquer código
2. Inicializadores de campo na ordem de declaração (int x = 10;)
3. Blocos de inicialização de instância ({ ... }) na ordem de aparição
4. Corpo do construtor
```

O compilador Java copia os blocos de inicialização de instância *em cada construtor*, na posição antes do corpo do construtor. Isso permite compartilhar lógica comum entre construtores sem criar um método separado.

```java
public class Contador {
    private final long criadoEm;
    private int valor = 0;          // passo 2: campo inicializado

    {                               // passo 3: bloco de init — roda em todo construtor
        criadoEm = System.currentTimeMillis();
    }

    public Contador() { }           // passo 4: construtor
    public Contador(int inicial) { this.valor = inicial; }
}
```

---

### Membros estáticos vs instância

A palavra-chave `static` transforma um membro em **membro de classe** — ele pertence à classe, não a nenhuma instância específica. Todos os objetos compartilham o mesmo campo estático; métodos estáticos não recebem referência `this`.

| Aspecto | Membro de instância | Membro estático |
|---------|--------------------|--------------------|
| Pertence a | Cada objeto individualmente | A classe inteira |
| Acesso | Via referência de objeto | Via nome da classe (preferido) |
| Pode acessar `this` | Sim | Não |
| Pode acessar campos de instância | Sim | Não diretamente |
| Inicializado | No construtor / declaração | No carregamento da classe |

```java
public class Conexao {
    private static int totalConexoes = 0;   // campo estático
    private final String host;              // campo de instância

    public Conexao(String host) {
        this.host = host;
        totalConexoes++;                    // acessa campo estático — OK
    }

    public static int getTotalConexoes() {  // método estático
        return totalConexoes;
        // return this.host;  ← ERRO: static não tem 'this'
    }

    public String getHost() {              // método de instância
        return this.host;
    }
}
```

**Bloco de inicialização estático** — executado *uma única vez*, quando a classe é carregada pela JVM. Útil para inicializar campos estáticos que requerem lógica complexa:

```java
public class ConfiguracaoSistema {
    private static final Map<String, String> DEFAULTS;

    static {
        DEFAULTS = new HashMap<>();
        DEFAULTS.put("timeout", "30");
        DEFAULTS.put("retries", "3");
    }
}
```

**Quando usar `static`:** dados ou comportamentos que fazem sentido para a *classe como um todo*, não para nenhuma instância em particular — contadores globais, constantes, factory methods, utilitários puros (sem estado).

**Cuidado:** campos estáticos mutáveis são estado global — difíceis de testar (interferem entre testes), problemáticos em concorrência, e aumentam o acoplamento.

---

### Modificadores de acesso

Java oferece quatro níveis de acesso, confirmados pela documentação oficial (Oracle Java Tutorials — Controlling Access to Members of a Class):

| Modificador | Mesma classe | Mesmo pacote | Subclasse (outro pacote) | Qualquer lugar |
|-------------|:---:|:---:|:---:|:---:|
| `public`    | Sim | Sim | Sim | Sim |
| `protected` | Sim | Sim | Sim | Não |
| (sem modificador — *package-private*) | Sim | Sim | Não | Não |
| `private`   | Sim | Não | Não | Não |

O nível sem modificador explícito é chamado de **package-private** (ou *default access*). Não existe a palavra-chave `package` para isso — a ausência de modificador é o sinal.

**Regra prática da Oracle:** use o modificador mais restritivo que faça sentido para o membro. `private` é o padrão para campos; `public` deve ser a exceção, não a regra.

```java
public class ContaBancaria {
    private double saldo;                 // campo: sempre private
    private String titular;

    public ContaBancaria(String titular) { // construtor: public para ser instanciável
        this.titular = titular;
        this.saldo   = 0.0;
    }

    public double getSaldo() {            // getter: public — interface controlada
        return saldo;
    }

    protected void auditarOperacao(String descricao) { // protected: disponível a subclasses
        // lógica de auditoria
    }

    private void validarSaldo(double valor) { // privado: detalhe de implementação
        if (valor < 0) throw new IllegalArgumentException("Valor negativo: " + valor);
    }

    public void depositar(double valor) {
        validarSaldo(valor);
        this.saldo += valor;
    }
}
```

---

### Encapsulamento

Encapsulamento significa esconder os detalhes de implementação e expor apenas o que é necessário. Em Java, isso se traduz em:

1. **Campos `private`** — nenhum código externo acessa o estado diretamente
2. **Getters e setters controlados** — o acesso passa por um método que pode validar, logar, ou converter
3. **Tell, don't ask** — em vez de o chamador pedir o estado e decidir, ele *instrui* o objeto a fazer algo

```java
// Violação de encapsulamento — campo público
public class Pedido {
    public int quantidade;   // qualquer um altera diretamente: pedido.quantidade = -5;
}

// Com encapsulamento
public class Pedido {
    private int quantidade;

    public void setQuantidade(int qtd) {
        if (qtd <= 0) throw new IllegalArgumentException("Quantidade inválida: " + qtd);
        this.quantidade = qtd;
    }

    public int getQuantidade() {
        return quantidade;
    }
}
```

**Tell, don't ask na prática:**

```java
// Ruim — o chamador pergunta o estado e decide
if (pedido.getQuantidade() > estoque.getQuantidade()) {
    // trata insuficiência
}

// Melhor — o objeto decide
estoque.reservar(pedido);   // lança exceção se insuficiente
```

Encapsulamento permite alterar a representação interna sem quebrar clientes externos — desde que a interface pública se mantenha.

---

### Objetos imutáveis

Um objeto imutável é aquele cujo estado nunca muda após a construção. As vantagens são significativas: thread-safe por definição, livre de bugs de mutação acidental, safe para compartilhamento e caching.

Receita para imutabilidade com classe regular:

1. Todos os campos `final`
2. Nenhum setter
3. **Defensive copy** de qualquer objeto mutável recebido no construtor
4. **Defensive copy** de qualquer objeto mutável retornado por getter

```java
public final class Intervalo {
    private final LocalDate inicio;
    private final LocalDate fim;

    public Intervalo(LocalDate inicio, LocalDate fim) {
        if (inicio == null || fim == null) {
            throw new NullPointerException("Datas não podem ser null");
        }
        if (fim.isBefore(inicio)) {
            throw new IllegalArgumentException("fim anterior a inicio");
        }
        // LocalDate já é imutável: defensive copy não necessária aqui
        this.inicio = inicio;
        this.fim    = fim;
    }

    public LocalDate getInicio() { return inicio; }
    public LocalDate getFim()    { return fim; }

    public boolean contem(LocalDate data) {
        return !data.isBefore(inicio) && !data.isAfter(fim);
    }
}
```

`LocalDate` já é imutável, então não precisa de defensive copy. Para tipos mutáveis (ex.: `Date`, arrays, coleções mutáveis), a cópia defensiva é obrigatória — veja a seção Armadilhas.

> A evolução natural desta abordagem é o `record` (Java 16+), que gera campos `final`, accessors e construtores automaticamente. Gancho para [[13 - Records e record patterns]].

## Na prática

Value object imutável com defensive copy de campo mutável:

```java
import java.util.Arrays;
import java.util.Objects;

/**
 * Value object imutável representando uma chave criptográfica.
 * Demonstra defensive copy para garantir imutabilidade real
 * mesmo com campos cujo tipo é mutável (byte[]).
 */
public final class ChaveCriptografica {

    private final String algoritmo;
    private final byte[] bytes;          // byte[] é mutável — exige defensive copy

    public ChaveCriptografica(String algoritmo, byte[] bytes) {
        Objects.requireNonNull(algoritmo, "algoritmo é obrigatório");
        Objects.requireNonNull(bytes, "bytes é obrigatório");
        if (bytes.length == 0) {
            throw new IllegalArgumentException("bytes não pode ser vazio");
        }
        this.algoritmo = algoritmo;
        this.bytes     = Arrays.copyOf(bytes, bytes.length);  // cópia defensiva na entrada
    }

    public String getAlgoritmo() {
        return algoritmo;
    }

    public byte[] getBytes() {
        return Arrays.copyOf(bytes, bytes.length);  // cópia defensiva na saída
    }

    public int tamanhoEmBits() {
        return bytes.length * 8;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof ChaveCriptografica other)) return false;
        return algoritmo.equals(other.algoritmo)
            && Arrays.equals(bytes, other.bytes);
    }

    @Override
    public int hashCode() {
        int result = algoritmo.hashCode();
        result = 31 * result + Arrays.hashCode(bytes);
        return result;
    }

    @Override
    public String toString() {
        return "ChaveCriptografica[algoritmo=" + algoritmo
             + ", tamanho=" + tamanhoEmBits() + " bits]";
    }
}
```

Por que duas cópias defensivas? Se o construtor não copiar o array recebido, quem criou o objeto pode alterar o array original e corromper o estado interno. Se o getter não copiar o array retornado, quem recebe o getter pode alterar o array e corromper o objeto. Ambas as cópias são necessárias para garantir imutabilidade real.

## Armadilhas

### (1) Vazar referência mutável via getter (quebra imutabilidade)

**O problema:** retornar diretamente um campo mutável expõe o estado interno do objeto. O chamador pode alterá-lo sem passar pelo construtor ou por qualquer validação.

```java
public final class Registro {
    private final Date criado;      // java.util.Date é mutável

    public Registro() {
        this.criado = new Date();
    }

    // PROBLEMA: retorna referência ao campo interno
    public Date getCriado() {
        return criado;
    }
}

// O chamador "quebra" a imutabilidade:
Registro r = new Registro();
r.getCriado().setTime(0L);   // altera o campo interno criado!
```

**Fix:** retorne uma cópia defensiva.

```java
public Date getCriado() {
    return new Date(criado.getTime());   // cópia — chamador não afeta o campo interno
}
```

**Alternativa moderna:** use `java.time.Instant` (imutável) em vez de `java.util.Date` — elimina a necessidade de defensive copy.

---

### (2) Estado estático mutável — dificulta teste e causa bugs em concorrência

**O problema:** campos `static` não-`final` são estado global. Qualquer parte do código pode lê-los e alterá-los, inclusive em paralelo. Testes passam ou falham dependendo da ordem de execução.

```java
public class GeradorDeId {
    public static int proximoId = 1;    // PROBLEMA: campo estático mutável público

    public static int gerar() {
        return proximoId++;             // não thread-safe, não testável isoladamente
    }
}

// Teste A deixa proximoId = 5; Teste B vê 5 em vez de 1 — testes acoplados!
```

**Fix:** use injeção de dependência para gerenciar o ciclo de vida, ou se precisar de um contador global, torne-o thread-safe e encapsulado.

```java
public class GeradorDeId {
    private static final AtomicInteger contador = new AtomicInteger(0);

    private GeradorDeId() {}   // sem instanciação

    public static int gerar() {
        return contador.incrementAndGet();
    }
}
```

---

### (3) Chamar método sobrescrevível no construtor

**O problema:** quando um construtor de superclasse chama um método que a subclasse sobrescreve (`@Override`), o método da subclasse é executado *antes* do construtor da subclasse ter rodado. O objeto está parcialmente inicializado — campos da subclasse ainda têm valor default (`null`, `0`, `false`).

```java
public class Base {
    public Base() {
        inicializar();     // chama método sobrescrevível — PERIGO
    }

    protected void inicializar() {
        System.out.println("Base.inicializar");
    }
}

public class Derivada extends Base {
    private final String nome;

    public Derivada(String nome) {
        super();              // chama Base() → chama inicializar() sobrescrito
        this.nome = nome;     // ainda não executou quando inicializar() rodou
    }

    @Override
    protected void inicializar() {
        System.out.println("nome = " + nome);  // nome é null aqui!
    }
}

new Derivada("teste");
// Imprime: "nome = null"  ← campo lido antes de ser inicializado
```

**Fix:** evite chamar métodos de instância sobrescritíveis no construtor. Prefira `private` ou `final` para métodos chamados no construtor, ou use o padrão de inicialização em dois passos (factory method após construção).

```java
public class Base {
    public Base() { }

    private void inicializarInterno() { }  // private: não pode ser sobrescrito
}
```

## Em entrevista

### Frase pronta (inglês)

> "Encapsulation is about hiding internal state behind a controlled interface — keeping fields `private` and exposing only what callers need to know, so the implementation can change without breaking clients." "Immutability takes that one step further: if an object's state never changes after construction, you get thread safety for free and eliminate an entire category of aliasing bugs — but you have to be careful with mutable types like arrays or `Date`, which require defensive copies both in the constructor and in getters." "The trade-off with defensive copies is allocation cost, which is why modern Java favors truly immutable types like `LocalDate` and `Instant`, and `record`s that generate all the right scaffolding automatically."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| classe / molde | class / blueprint |
| objeto / instância | object / instance |
| campo de instância | instance field / instance variable |
| campo estático / variável de classe | static field / class variable |
| sobrecarga de construtor | constructor overloading |
| encapsulamento | encapsulation |
| cópia defensiva | defensive copy |
| imutabilidade | immutability |
| acesso package-private | package-private / default access |
| membro de classe | class member (static member) |
| diga, não pergunte | tell, don't ask |
| bloco de inicialização estático | static initializer block |

## Veja também

- [[07 - Herança e polimorfismo]]
- [[08 - Interfaces e classes abstratas]]
- [[13 - Records e record patterns]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [Classes and Objects — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/javaOO/index.html)
- [Controlling Access to Members of a Class — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/javaOO/accesscontrol.html)
- [Providing Constructors for Your Classes — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/javaOO/constructors.html)
- [Understanding Class Members — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/javaOO/classvars.html)
- [Initializing Fields — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/javaOO/initial.html)
