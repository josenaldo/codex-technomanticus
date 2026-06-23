---
title: "Interfaces e classes abstratas"
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
  - interfaces
aliases:
  - Interface
  - Classe abstrata
---

# Interfaces e classes abstratas

> [!abstract] TL;DR
> **Interface** define um contrato/tipo: o que um objeto sabe fazer, sem ditar como. Desde o Java 8, pode ter `default methods` (implementação compartilhada) e `static methods`; desde o Java 9, também `private methods`. **Classe abstrata** é um esqueleto parcial: pode ter estado (campos de instância), construtor e métodos concretos — mas não pode ser instanciada diretamente. A regra de ouro: se a decisão envolve **estado compartilhado ou inicialização**, use classe abstrata; se envolve **tipo/contrato ou herança múltipla**, use interface. O **problema do diamante** (dois default methods conflitantes herdados da mesma assinatura) exige resolução explícita: a classe deve sobrescrever o método e pode delegar com `InterfaceX.super.metodo()`.

## O que é

**Interface** é um tipo de referência que define um contrato: um conjunto de métodos que qualquer implementador deve respeitar. Conceitualmente, uma interface responde à pergunta *"o que este objeto consegue fazer?"* — sem ditar como. A partir do Java 8, interfaces ganharam capacidade de carregar implementação via `default` e `static` methods; a partir do Java 9, também `private` methods internos. Mesmo assim, uma interface **não tem estado** — não possui campos de instância, apenas constantes `static final`.

**Classe abstrata** é uma classe parcialmente implementada que serve de esqueleto para subclasses. Ela responde à pergunta *"do que este objeto é feito?"* — pode ter campos de instância, construtor, métodos concretos e métodos abstratos que as subclasses são obrigadas a implementar. Não pode ser instanciada diretamente com `new`, mas define estrutura e comportamento compartilhado.

A distinção fundamental:

| | Interface | Classe abstrata |
|---|---|---|
| Estado (campos de instância) | Não | Sim |
| Construtor | Não | Sim |
| Herança múltipla | Sim (uma classe implementa N) | Não (extends único) |
| Métodos concretos | `default` / `static` / `private` | Sim (qualquer método) |
| Constantes | `static final` implícito | Qualquer modificador |

## Como funciona

### Interfaces

Uma interface declara membros que descrevem capacidades. O compilador trata certos modificadores como implícitos.

**Métodos abstratos** — implicitamente `public abstract`. Toda classe concreta que implementar a interface deve providenciar a implementação.

```java
public interface Exportavel {
    // public abstract é implícito
    byte[] exportar();
    String getFormato();
}
```

**Constantes `static final`** — todo campo de interface é implicitamente `public static final`. Não existem campos de instância.

```java
public interface Limites {
    int TAMANHO_MAXIMO = 1_000; // public static final implícito
}
```

**Default methods (Java 8)** — implementação padrão que as classes implementadoras herdam automaticamente, podendo sobrescrever se quiserem. O objetivo primário foi permitir que interfaces evoluíssem sem quebrar implementadores existentes.

```java
public interface Colecao<T> {
    void adicionar(T item);
    int tamanho();

    // default method — herdado automaticamente; sobrescrevível
    default boolean estaVazia() {
        return tamanho() == 0;
    }
}
```

**Static methods (Java 8)** — métodos de fábrica ou utilitários associados à interface, chamados diretamente pelo nome da interface. Não são herdados pelas implementações nem pelas subinterfaces.

```java
public interface Validador<T> {
    boolean validar(T valor);

    // factory method na própria interface
    static Validador<String> naoNulo() {
        return valor -> valor != null && !valor.isBlank();
    }
}

// Uso: Validador<String> v = Validador.naoNulo();
```

**Private methods (Java 9)** — métodos auxiliares internos à interface, usados para compartilhar lógica entre `default` methods sem expor essa lógica como API. Não são herdados por implementadores nem por subinterfaces.

```java
public interface Notificavel {
    void notificar(String mensagem);

    default void notificarComRetentativa(String mensagem, int tentativas) {
        for (int i = 0; i < tentativas; i++) {
            if (tentarNotificar(mensagem)) return;
        }
    }

    default void notificarOuLogar(String mensagem) {
        if (!tentarNotificar(mensagem)) {
            registrarFalha(mensagem);
        }
    }

    // private: lógica interna compartilhada entre os dois default methods acima
    private boolean tentarNotificar(String mensagem) {
        try {
            notificar(mensagem);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    // private static: não precisa de instância
    private static void registrarFalha(String mensagem) {
        System.err.println("Falha ao notificar: " + mensagem);
    }
}
```

**Functional interfaces** — interface com exatamente **um método abstrato** (SAM — Single Abstract Method). São a base das lambdas e method references do Java 8+. `default` e `static` methods não contam para o requisito SAM. A anotação `@FunctionalInterface` instrui o compilador a verificar isso.

```java
@FunctionalInterface
public interface Transformador<T, R> {
    R transformar(T entrada);      // único método abstrato

    default Transformador<T, T> identidade() {  // não conta para SAM
        return t -> (T) t;
    }
}

// Uso com lambda:
Transformador<String, Integer> comprimento = s -> s.length();
```

> **Gancho:** functional interfaces são o ponto de entrada para lambdas, streams e `java.util.function`. Veja o Galho 2 para aprofundar.

---

### Classes abstratas

Uma classe abstrata pode conter qualquer membro que uma classe concreta contém — mais métodos marcados com `abstract` que as subclasses devem implementar.

```java
public abstract class Relatorio {
    // estado compartilhado — campos de instância
    protected final String titulo;
    protected final LocalDate dataGeracao;

    // construtor — inicialização obrigatória do estado comum
    protected Relatorio(String titulo) {
        this.titulo = titulo;
        this.dataGeracao = LocalDate.now();
    }

    // método abstrato — subclasse define o conteúdo específico
    public abstract List<String> gerarLinhas();

    // método concreto — comportamento compartilhado por todas as subclasses
    public void imprimir() {
        System.out.println("=== " + titulo + " (" + dataGeracao + ") ===");
        gerarLinhas().forEach(System.out::println);
    }

    // método concreto utilitário
    protected String formatarValor(double valor) {
        return String.format("R$ %.2f", valor);
    }
}

public class RelatorioVendas extends Relatorio {
    private final List<Double> vendas;

    public RelatorioVendas(List<Double> vendas) {
        super("Relatório de Vendas");
        this.vendas = vendas;
    }

    @Override
    public List<String> gerarLinhas() {
        return vendas.stream()
            .map(v -> "  Venda: " + formatarValor(v))
            .toList();
    }
}
```

Regras fundamentais de classes abstratas:

- `abstract class` não pode ser instanciada diretamente (`new Relatorio()` é erro de compilação).
- Pode ter zero ou mais métodos `abstract` — uma classe com método abstrato **deve** ser declarada `abstract`.
- Uma subclasse que não implementar todos os métodos abstratos também deve ser declarada `abstract`.
- Construtores são chamados pela subclasse via `super(...)` — mesmo que a classe abstrata não seja instanciada diretamente, seu construtor inicializa o estado herdado.

---

### Interface vs classe abstrata — decisão

A decisão não é sobre preferência estilística — é sobre o que o modelo de domínio pede.

| Critério | Interface | Classe abstrata |
|---|---|---|
| Precisa de **estado** (campos de instância)? | Não | **Sim** |
| Precisa de **construtor** com lógica de inicialização? | Não | **Sim** |
| Uma classe pode já estender outra e ainda querer esse tipo? | **Sim** (implements múltiplos) | Não (extends único) |
| É um **contrato/capacidade** ("é capaz de X")? | **Sim** | Raramente |
| É uma **identidade/esqueleto** ("é um tipo de Y")? | Raramente | **Sim** |
| Precisa **evoluir a API** sem quebrar implementadores? | **Sim** (default method) | Sim (método concreto) |
| Quer compartilhar lógica concreta **com estado comum**? | Limitado (só via default) | **Sim** |

**Heurística prática:**

- Se a abstração só precisa definir *o que*, use interface.
- Se a abstração precisa definir *parte do como* **e** manter estado compartilhado, use classe abstrata.
- Se precisar dos dois (estado + herança múltipla de tipo), use classe abstrata + interface: a abstrata implementa a interface e fornece parte da implementação.

---

### Herança múltipla de tipo e o problema do diamante

Java permite herança múltipla de **tipo** (implementar N interfaces), mas não de **estado** (extends de uma só classe). Isso elimina a maioria dos problemas clássicos do diamante — mas `default` methods reintroduziram o problema a nível de implementação.

**Cenário:** duas interfaces definem um `default` method com a mesma assinatura. Uma classe implementa as duas.

```java
interface Voador {
    default String mover() {
        return "voando";
    }
}

interface Nadador {
    default String mover() {
        return "nadando";
    }
}

// ERRO DE COMPILAÇÃO: ambiguidade não resolvida
// class Pato implements Voador, Nadador { }
```

O compilador detecta o conflito e exige resolução explícita. As **três regras de resolução**, em ordem de prioridade (conforme Java Language Specification §9.4.1):

**Regra 1 — Classe vence interface:** um método concreto herdado de uma superclasse tem prioridade sobre qualquer `default` method de uma interface, mesmo que a interface seja mais específica.

```java
class Ave {
    public String mover() { return "andando"; }  // método concreto na classe
}

class Pato extends Ave implements Voador {
    // mover() de Ave vence — nenhum conflito, nenhum override necessário
}
```

**Regra 2 — Subinterface vence superinterface:** se duas interfaces estão em relação de herança, a mais específica (subinterface) vence.

```java
interface Animal {
    default String respirar() { return "respirando"; }
}

interface Mamifero extends Animal {
    @Override
    default String respirar() { return "pulmões"; }  // mais específico
}

class Cachorro implements Mamifero, Animal {
    // Mamifero.respirar() vence — é a subinterface de Animal
}
```

**Regra 3 — Conflito irresolvível → erro de compilação + override explícito obrigatório:** quando nenhuma das duas regras anteriores se aplica (interfaces independentes com mesma assinatura), o compilador emite erro. A classe deve sobrescrever explicitamente, podendo delegar a qualquer das interfaces com `Interface.super.metodo()`.

```java
class Pato implements Voador, Nadador {
    @Override
    public String mover() {
        // delegação explícita — escolhe qual implementação usar
        return Voador.super.mover() + " e " + Nadador.super.mover();
        // ou apenas: return "voando baixo"; — implementação própria
    }
}
```

A sintaxe `Interface.super.metodo()` só é válida quando `Interface` é uma **superinterface direta** da classe ou interface que contém o código — não funciona para interfaces transitivas.

> **Nota confirmada via JLS §9.4.1:** *"If an interface I inherits a default method whose signature is override-equivalent with another method inherited by I, then a compile-time error occurs."* — o compilador detecta ativamente o conflito e o reporta como erro, exigindo resolução explícita.

## Na prática

### Quando `default` method é a escolha certa

O caso de uso primário e historicamente motivador foi **evolução de API sem quebra de compatibilidade binária**: quando a interface `Collection` precisou ganhar o método `stream()` no Java 8, adicionar um método abstrato teria quebrado todos os implementadores existentes em toda a ecosfera Java. A solução foi `default Collection.stream()` — implementadores antigos herdaram a implementação automaticamente.

```java
// Antes do Java 8: adicionar método abstrato em interface pública = quebrar tudo
// Java 8: default method resolve o problema de evolução
interface Collection<E> {
    // ... métodos existentes ...

    default Stream<E> stream() {                // adicionado sem quebrar ninguém
        return StreamSupport.stream(spliterator(), false);
    }
}
```

Outros usos legítimos:

- **Métodos de conveniência** que se expressam completamente em termos de outros métodos da interface (como `isEmpty()` expressado via `size()`).
- **Comportamento opt-in** — implementadores que precisem de comportamento diferente sobrescrevem; os demais herdam o padrão sem precisar escrever nada.

### Comparação justa: interface vs classe abstrata

Nem interface nem classe abstrata é universalmente melhor. A escolha depende do que o modelo precisa.

**Interface ganha quando:**

- A abstração é transversal: `Comparable`, `Serializable`, `Closeable` — não faz sentido forçar uma hierarquia de herança para isso.
- Uma classe já estende outra e precisa desse contrato: `ArrayList extends AbstractList implements List, RandomAccess, Cloneable, Serializable`.
- O objetivo é **plugabilidade** e **testabilidade** — qualquer objeto que implemente a interface pode ser passado, facilitando mocks e implementações alternativas.
- A abstração vai evoluir gradualmente via `default` methods ao longo das versões da API.

**Classe abstrata ganha quando:**

- Há **estado compartilhado** que as subclasses precisam herdar e que requer inicialização no construtor.
- Parte da implementação não pode ser expressa sem estado (ex.: um template method que usa campos para controlar fluxo).
- O domínio modela uma **hierarquia de identidade** clara ("um `RelatorioVendas` é um `Relatorio`"), não apenas uma capacidade.
- Precisa controlar visibilidade de métodos internos (`protected`) sem expô-los na API pública.

**Padrão híbrido** — muito comum em bibliotecas maduras (ex.: coleções Java): interface define o contrato (`List`), classe abstrata fornece implementação parcial (`AbstractList`), classe concreta completa (`ArrayList`). Quem quiser implementar `List` do zero pode; quem quiser aproveitar o esqueleto estende `AbstractList`.

```java
// Contrato completo
public interface Repositorio<T, ID> {
    T buscar(ID id);
    void salvar(T entidade);
    void deletar(ID id);
    List<T> listarTodos();
}

// Esqueleto com lógica compartilhada (cache, log, validação)
public abstract class RepositorioBase<T, ID> implements Repositorio<T, ID> {
    private final Map<ID, T> cache = new HashMap<>();

    @Override
    public T buscar(ID id) {
        return cache.computeIfAbsent(id, this::buscarNoBanco);
    }

    // subclasse define como vai ao banco
    protected abstract T buscarNoBanco(ID id);

    @Override
    public void salvar(T entidade) {
        validar(entidade);
        salvarNoBanco(entidade);
    }

    protected abstract void salvarNoBanco(T entidade);

    protected void validar(T entidade) {
        Objects.requireNonNull(entidade, "entidade não pode ser nula");
    }
}

// Implementação concreta — só precisa completar o que é específico de banco
public class RepositorioProdutoJdbc extends RepositorioBase<Produto, Long> {
    @Override
    protected Produto buscarNoBanco(Long id) { /* JDBC */ return null; }

    @Override
    protected void salvarNoBanco(Produto p) { /* JDBC */ }

    @Override
    public void deletar(Long id) { /* JDBC */ }

    @Override
    public List<Produto> listarTodos() { /* JDBC */ return List.of(); }
}
```

## Armadilhas

### (1) Conflito de default methods exige resolução explícita — o compilador não escolhe

**O problema:** quando duas interfaces independentes declaram um `default` method com a mesma assinatura e uma classe implementa as duas, o compilador emite erro. Não há "mais específico" para escolher e o compilador não inventa uma prioridade.

```java
interface Logavel {
    default String identificar() {
        return "log:" + getClass().getSimpleName();
    }
}

interface Auditavel {
    default String identificar() {
        return "audit:" + getClass().getSimpleName();
    }
}

// ERRO DE COMPILAÇÃO:
// class Servico implements Logavel, Auditavel { }
// → "class Servico inherits unrelated defaults for identificar() from types Logavel and Auditavel"
```

**Fix:** sobrescrever o método na classe. Pode delegar a uma das interfaces com `Interface.super.metodo()` ou fornecer implementação própria.

```java
class Servico implements Logavel, Auditavel {
    @Override
    public String identificar() {
        // opção 1: delegar a uma interface específica
        return Logavel.super.identificar();

        // opção 2: combinar ambos
        // return Logavel.super.identificar() + "|" + Auditavel.super.identificar();

        // opção 3: implementação própria, ignorando ambos
        // return "servico:" + getClass().getSimpleName();
    }
}
```

---

### (2) Interface não tem campos de instância — só constantes `static final`

**O problema:** quem vem de outras linguagens pode tentar usar interface para compartilhar estado mutável entre implementadores. Isso não funciona: qualquer campo em interface é implicitamente `public static final` — uma constante compartilhada por todos, não um campo por instância.

```java
public interface Configuravel {
    // ARMADILHA: parece um campo de instância mutável, mas é static final
    int TIMEOUT = 30;    // na prática: public static final int TIMEOUT = 30

    // ISSO NÃO COMPILA — interface não tem campos de instância mutáveis:
    // String nome;       // erro: "Variable 'nome' might not have been initialized"
    // int contador = 0;  // compila, mas é static final — alteração impossível
}

class ClienteHttp implements Configuravel {
    // TIMEOUT é de Configuravel — não é "deste" objeto
    // Configuravel.TIMEOUT == ClienteHttp.TIMEOUT == 30 (a mesma constante)
}
```

**Fix:** se precisar de estado por instância, use classe abstrata (com campos `protected`) ou encapsule o estado na própria classe concreta.

```java
public abstract class ConectavelBase {
    // estado por instância — cada objeto tem o seu
    protected int timeout;
    protected String host;

    protected ConectavelBase(String host, int timeout) {
        this.host = host;
        this.timeout = timeout;
    }
}
```

---

### (3) Abusar de default methods como se fossem traits ou herança de implementação

**O problema:** `default` methods foram projetados para **evolução de API** e **métodos de conveniência**, não como substitutos de herança de implementação ou mixins/traits. Colocar lógica complexa, com dependência de estado externo ou efeitos colaterais relevantes, em `default` methods cria acoplamento oculto e dificulta o rastreamento de comportamento.

```java
// ABUSO: default method com lógica de negócio pesada que simula herança de estado
public interface Processavel {
    String getId();

    // default method que "simula" ter estado — depende de estado externo implícito
    default void processarComAuditoria() {
        AuditoriaGlobal.registrar(getId());  // dependência global oculta
        processar();
        AuditoriaGlobal.confirmar(getId()); // mais estado global oculto
    }

    void processar();
}
```

Agora toda classe que implementar `Processavel` herda a dependência de `AuditoriaGlobal` — sem saber. Mudar `processarComAuditoria()` impacta silenciosamente todas as implementações.

**Fix:** lógica de negócio complexa pertence a serviços ou classes abstratas, onde o estado é explícito e o ciclo de vida é controlado.

```java
// Correto: default method expressado em termos de outros métodos da PRÓPRIA interface
public interface Processavel {
    void processar();
    boolean estaAtivo();

    // ok: conveniência que só usa membros da interface
    default void processarSeAtivo() {
        if (estaAtivo()) processar();
    }
}

// Lógica com dependência externa fica em serviço separado
public class ProcessadorComAuditoria {
    private final Processavel alvo;
    private final AuditoriaService auditoria;

    public void executar() {
        auditoria.registrar(alvo);
        alvo.processar();
        auditoria.confirmar(alvo);
    }
}
```

## Em entrevista

### Frase pronta (inglês)

> "The core trade-off between interface and abstract class is about type versus state: an interface defines what a type can do and supports multiple inheritance of type, while an abstract class defines what a type partially is and can carry shared instance state — so if you need fields, a constructor, or shared mutable state, the abstract class wins." "The decision shifts when you're designing for evolution: default methods in Java 8 let you add new behavior to an existing interface without breaking its implementors, which is exactly how `Collection.stream()` was introduced — the compiler inserts the default implementation for anyone who hasn't overridden it." "A critical caveat is the diamond problem with default methods: when two independent interfaces declare the same default method signature and a class implements both, the compiler produces a compile-time error rather than silently picking one — the programmer must explicitly resolve the conflict, optionally delegating to a specific interface's implementation with the `Interface.super.method()` syntax."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| interface | interface |
| classe abstrata | abstract class |
| método padrão | default method |
| método estático de interface | interface static method |
| método privado de interface | interface private method |
| contrato | contract |
| método de fábrica funcional | functional interface |
| problema do diamante | diamond problem |
| herança múltipla de tipo | multiple inheritance of type |
| resolução de conflito | conflict resolution |
| subinterface | subinterface |
| delegação explícita | explicit delegation |

## Veja também

- [[06 - Classes, objetos e encapsulamento]]
- [[07 - Herança e polimorfismo]]
- [[09 - Enums]]
- [[11 - Annotations]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [Default Methods — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/IandI/defaultmethods.html)
- [Multiple Inheritance of Type — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/IandI/multipleinheritance.html)
- [Interfaces — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/IandI/createinterface.html)
- [Abstract Methods and Classes — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/IandI/abstract.html)
- [Java Language Specification §9.4.1 — Interface Method Declarations (Oracle)](https://docs.oracle.com/javase/specs/jls/se21/html/jls-9.html)
