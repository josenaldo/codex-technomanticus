---
title: "Generics em profundidade"
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
  - generics
  - type-system
aliases:
  - Generics
  - Genéricos
  - PECS
---

# Generics em profundidade

> [!abstract] TL;DR
> **Generics** adicionam segurança de tipo em compile-time e permitem reuso paramétrico: uma única implementação funciona para múltiplos tipos sem casting manual. **Type parameters** (`<T>`, `<E>`, `<K, V>`) parametrizam classes, interfaces e métodos. **Bounded types** (`<T extends Number>`) restringem os tipos aceitos. **Wildcards** (`? extends` / `? super` / `?`) tornam APIs mais flexíveis, guiados pelo mnemônico **PECS** — *Producer Extends, Consumer Super*: use `? extends` quando a estrutura *produz* valores para você ler, e `? super` quando ela *consome* valores que você escreve. **Type erasure** remove toda informação genérica em runtime: `List<String>` e `List<Integer>` viram o mesmo `List` no bytecode, o que proíbe `new T[]`, `instanceof List<String>` e overload por tipo genérico, e introduz *bridge methods* invisíveis para preservar polimorfismo.

## O que é

**Generics** são o mecanismo do Java para escrever código que opera sobre tipos arbitrários sem abrir mão da verificação estática de tipos. Antes dos generics (Java 5), coleções operavam sobre `Object`:

```java
// Antes — sem generics: necessário cast manual, ClassCastException em runtime
List nomes = new ArrayList();
nomes.add("Ana");
nomes.add(42);               // compilador não reclama
String nome = (String) nomes.get(1); // ClassCastException em runtime
```

Com generics, o compilador detecta o problema antes de executar o programa:

```java
// Com generics: erro detectado em compile-time
List<String> nomes = new ArrayList<>();
nomes.add("Ana");
nomes.add(42);               // ERRO de compilação — não compila
String nome = nomes.get(0);  // sem cast — tipo garantido
```

Os dois papéis centrais dos generics são:

- **Segurança de tipo em compile-time** — o compilador rastreia o tipo parametrizado e rejeita operações inválidas antes que o código chegue à JVM.
- **Reuso paramétrico** — uma única implementação (`class Stack<T>`, `<T> T max(T a, T b)`) funciona corretamente para `String`, `Integer`, `Produto` ou qualquer tipo, sem duplicação de código.

O resultado é código mais legível (sem casts espalhados), mais seguro (erros de tipo detectados cedo) e mais expressivo (a assinatura comunica quais tipos são aceitos e retornados).

## Como funciona

### Type parameters e métodos genéricos

Um **type parameter** é um placeholder declarado entre `<>` que representa um tipo concreto a ser fornecido pelo chamador.

**Convenções de nomenclatura** (por Oracle):

| Letter | Significado |
|--------|-------------|
| `T` | Type (tipo genérico) |
| `E` | Element (elemento de coleção) |
| `K` | Key (chave de mapa) |
| `V` | Value (valor de mapa) |
| `N` | Number (número) |
| `R` | Return type (retorno de função) |

**Classe genérica:**

```java
// Caixa parametrizada — funciona para qualquer tipo T
public class Caixa<T> {
    private T conteudo;

    public void guardar(T item) {
        this.conteudo = item;
    }

    public T abrir() {
        return conteudo;
    }
}

// Uso: o compilador trava o tipo em Caixa<String>
Caixa<String> caixaDeTexto = new Caixa<>();
caixaDeTexto.guardar("mensagem secreta");
String texto = caixaDeTexto.abrir();   // sem cast

Caixa<Integer> caixaDeNumero = new Caixa<>();
caixaDeNumero.guardar(42);
Integer numero = caixaDeNumero.abrir();
```

**Interface genérica:**

```java
public interface Repositorio<T, ID> {
    T buscarPorId(ID id);
    List<T> listarTodos();
    void salvar(T entidade);
}

// Implementação concreta fixa os type parameters
public class PacienteRepositorio implements Repositorio<Paciente, Long> {
    @Override
    public Paciente buscarPorId(Long id) { /* ... */ return null; }
    // ...
}
```

**Método genérico:** o type parameter é declarado *antes* do tipo de retorno, dentro de `<>`.

```java
public class Utilitarios {

    // <T> declara o type parameter; T aparece no retorno e nos parâmetros
    public static <T> T primeiroNaoNulo(T a, T b) {
        return a != null ? a : b;
    }

    // Método de troca genérico — dois elementos de um array
    public static <T> void trocar(T[] array, int i, int j) {
        T temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

// Inferência de tipo — compilador deduz T=String
String resultado = Utilitarios.primeiroNaoNulo(null, "fallback");

// Forma explícita (raramente necessária)
String resultado2 = Utilitarios.<String>primeiroNaoNulo(null, "fallback");
```

**Raw types** — usar uma classe genérica sem type parameter. Tecnicamente válido por compatibilidade retroativa, mas perde toda a segurança de tipo e deve ser evitado em código novo:

```java
// Raw type — tipo apagado, sem verificação: EVITAR
List lista = new ArrayList();
lista.add("texto");
lista.add(42);          // compilador não reclama
String s = (String) lista.get(1); // ClassCastException em runtime
```

---

### Bounded types

**Upper bound** — `<T extends Tipo>` restringe `T` a `Tipo` ou qualquer subtipo de `Tipo`. O compilador permite chamar métodos de `Tipo` sobre `T`:

```java
// Aceita qualquer T que seja Number ou subclasse: Integer, Double, Long...
public static <T extends Number> double somar(List<T> lista) {
    double total = 0;
    for (T elemento : lista) {
        total += elemento.doubleValue(); // doubleValue() existe em Number — válido!
    }
    return total;
}

somar(List.of(1, 2, 3));       // T=Integer — ok
somar(List.of(1.5, 2.5));     // T=Double — ok
somar(List.of("texto"));      // ERRO de compilação — String não é Number
```

**Múltiplos bounds** — `<T extends A & B>` exige que `T` seja subtipo de A *e* implemente B. A classe concreta (se houver) deve vir primeiro; interfaces ficam depois, separadas por `&`:

```java
// T deve ser Comparable com si mesmo E ser Serializable
public static <T extends Comparable<T> & java.io.Serializable> T maximo(T a, T b) {
    return a.compareTo(b) >= 0 ? a : b;
}
```

Regra: **apenas uma classe** pode aparecer nos bounds (Java não tem herança múltipla); o restante são interfaces. `<T extends String & Comparable<T>>` é válido; `<T extends String & Number>` causa erro de compilação.

---

### Wildcards e PECS

Wildcard (`?`) é um tipo desconhecido. Ele aparece em declarações de variáveis e parâmetros — nunca na declaração de classes ou métodos genéricos. Há três formas:

| Wildcard | Sintaxe | Semântica |
|----------|---------|-----------|
| Upper bounded | `? extends T` | Tipo desconhecido que é `T` ou subtipo de `T` |
| Lower bounded | `? super T` | Tipo desconhecido que é `T` ou supertipo de `T` |
| Unbounded | `?` | Qualquer tipo; equivalente a `? extends Object` |

**PECS — Producer Extends, Consumer Super**

O mnemônico PECS (cunhado por Joshua Bloch no *Effective Java*) guia qual wildcard usar:

- **Producer Extends**: se a estrutura *produz* (fornece) elementos para você *ler*, use `? extends T`. Você pode ler `T`s dela, mas não pode escrever (o compilador não sabe o subtipo exato).
- **Consumer Super**: se a estrutura *consome* (recebe) elementos que você vai *escrever*, use `? super T`. Você pode escrever `T`s nela (inclusive subtipos), mas não pode ler com tipo preciso (retorna `Object`).

O exemplo canônico é `Collections.copy`:

```java
// Assinatura real de Collections.copy (simplificada):
public static <T> void copy(List<? super T> dst, List<? extends T> src) {
    for (T elemento : src) {  // src produz T — extends ✔
        dst.add(elemento);    // dst consome T  — super ✔
    }
}
```

- `src` é um *producer*: você lê `T` dele → `? extends T`
- `dst` é um *consumer*: você escreve `T` nele → `? super T`

```java
List<Integer>       inteiros = List.of(1, 2, 3);
List<Number>        numeros  = new ArrayList<>();
List<Object>        objetos  = new ArrayList<>();

Collections.copy(numeros, inteiros);   // T=Integer, dst=List<Number> (super Integer) ✔
Collections.copy(objetos, inteiros);   // T=Integer, dst=List<Object> (super Integer) ✔
// Collections.copy(inteiros, numeros); // ERRO — List<Integer> não é ? super Integer
```

**Por que `List<? extends T>` é somente leitura:**

```java
List<? extends Number> producer = new ArrayList<Integer>();
producer.add(3.14);      // ERRO — compilador não sabe se é List<Integer>, List<Double>...
producer.add(null);      // null é ok (único valor permitido)
Number n = producer.get(0); // ok — retorna Number (bound superior)
```

O compilador não sabe o subtipo exato (`Integer`? `Double`?), portanto proíbe qualquer `add` que não seja `null`.

**Quando usar unbounded `?`:** quando o código só precisa de métodos de `Object`, ou quando a operação é independente do tipo:

```java
public static void imprimirLista(List<?> lista) {
    for (Object item : lista) {
        System.out.println(item);    // apenas toString() — Object suficiente
    }
}
```

**Wildcards não são type parameters:** não aparecem na declaração de classe/método genérico — são usados apenas em tipos de variáveis, campos, parâmetros e retornos.

---

### Type erasure

**Type erasure** é a estratégia de implementação escolhida pelo Java ao introduzir generics no Java 5. O compilador usa informação genérica para verificação estática e inserção de casts implícitos, depois a *apaga* completamente do bytecode. Resultado: `List<String>` e `List<Integer>` produzem bytecode idêntico — ambos viram `List`.

**O que o compilador faz durante erasure:**

1. **Substitui type parameters pelo bound (ou `Object` se unbounded)**

```text
// Antes da erasure (código-fonte):
public class Caixa<T> {
    private T conteudo;
    public T abrir() { return conteudo; }
}

// Depois da erasure (bytecode):
public class Caixa {
    private Object conteudo;
    public Object abrir() { return conteudo; }
}
```

```text
// Com bound:
public <T extends Number> double somar(List<T> lista) { ... }

// Após erasure:
public double somar(List lista) { ... }   // T → Number
```

2. **Insere casts automáticos nos pontos de uso** — quando o compilador sabe o tipo concreto (pelo contexto), ele insere um cast no bytecode:

```java
List<String> nomes = new ArrayList<>();
nomes.add("Ana");
String s = nomes.get(0);  // compilador insere: (String) lista.get(0) no bytecode
```

3. **Gera bridge methods** para preservar polimorfismo em subclasses de tipos genéricos:

```java
public interface Comparavel<T> {
    int comparar(T outro);
}

public class Numero implements Comparavel<Numero> {
    private int valor;
    @Override
    public int comparar(Numero outro) { return Integer.compare(this.valor, outro.valor); }
}
```

Após erasure, `Comparavel` vira `Comparavel` com `int comparar(Object outro)`. Para que polimorfismo funcione, o compilador gera um *bridge method* invisível em `Numero`:

```java
// Bridge method gerado pelo compilador (invisível no código-fonte):
public int comparar(Object outro) {
    return comparar((Numero) outro);   // delega para o método real
}
```

**Consequências práticas do type erasure:**

| Operação | Resultado |
|----------|-----------|
| `new T()` | ERRO de compilação — tipo apagado em runtime |
| `new T[]` | ERRO de compilação — arrays guardam tipo em runtime |
| `instanceof List<String>` | ERRO de compilação — não reificável |
| `instanceof List<?>` | OK — wildcard unbounded é reificável |
| Overload `void f(List<String>)` e `void f(List<Integer>)` | ERRO — mesma assinatura após erasure |
| `catch (SomeException<T> e)` | ERRO — tipo genérico em catch |

```java
public class Fábrica<T> {
    // ERRO: new T() não compila — tipo apagado
    // public T criar() { return new T(); }

    // SOLUÇÃO: passar Class<T> como type token
    public T criar(Class<T> tipo) throws Exception {
        return tipo.getDeclaredConstructor().newInstance();
    }
}

// ERRO: instanceof com tipo parametrizado
Object obj = List.of("a", "b");
if (obj instanceof List<String> lista) { /* não compila */ }

// OK: instanceof com wildcard
if (obj instanceof List<?> lista) { System.out.println(lista.size()); }
```

**Por que erasure existe:** manter compatibilidade binária com código Java pré-generics. Bibliotecas compiladas sem generics continuam funcionando junto com código genérico moderno. O custo é a ausência de informação de tipo em runtime.

---

### Type tokens

Um **type token** é o padrão de passar `Class<T>` como parâmetro explícito para contornar a erasure quando é necessário conhecer o tipo em runtime.

```java
// Sem type token — não é possível criar T ou fazer cast seguro
public class Conversor<T> {
    // ❌ T não existe em runtime
}

// Com type token — Class<T> preserva o tipo
public class Conversor<T> {
    private final Class<T> tipo;

    public Conversor(Class<T> tipo) {
        this.tipo = tipo;
    }

    public T converter(Object objeto) {
        return tipo.cast(objeto);  // cast seguro via reflection
    }

    public boolean éCompatível(Object objeto) {
        return tipo.isInstance(objeto);  // instanceof seguro via reflection
    }
}

// Uso
Conversor<String> c = new Conversor<>(String.class);
String s = c.converter("texto");    // ok
boolean b = c.éCompatível(42);     // false
```

O padrão é amplamente usado em frameworks: `ObjectMapper.readValue(json, Paciente.class)`, `entityManager.find(Paciente.class, id)`, `context.getBean(ServicoEmail.class)`.

## Na prática

Ao desenhar uma API genérica, aplique PECS sistematicamente para maximizar flexibilidade sem sacrificar segurança:

```java
/**
 * Copia elementos de uma fonte para um destino.
 *
 * <p>O uso de wildcards com PECS garante que o chamador pode passar:
 * - Como src: qualquer List<Integer>, List<Double> ou List<Number> (para T=Number)
 * - Como dst: qualquer List<Number> ou List<Object> (para T=Number)
 *
 * @param <T> o tipo dos elementos copiados
 * @param dst destino — consumer, aceita T e supertipos
 * @param src fonte  — producer, fornece T e subtipos
 */
public static <T> void copiar(List<? super T> dst, List<? extends T> src) {
    for (T item : src) {
        dst.add(item);
    }
}

// ── Exemplo com hierarquia de tipos ─────────────────────────────────────────
//   Object
//     └── Number
//           ├── Integer
//           └── Double

List<Integer>  inteiros  = List.of(1, 2, 3);
List<Double>   doubles   = List.of(1.5, 2.5);
List<Number>   numeros   = new ArrayList<>();
List<Object>   objetos   = new ArrayList<>();

copiar(numeros, inteiros);  // T=Integer: dst=List<Number> (Number super Integer) ✔
copiar(numeros, doubles);   // T=Double:  dst=List<Number> (Number super Double)  ✔
copiar(objetos, inteiros);  // T=Integer: dst=List<Object> (Object super Integer) ✔
```

Outro padrão comum é um método utilitário que encontra o máximo de uma coleção — bounded type parameter garante que `compareTo` esteja disponível:

```java
/**
 * Retorna o elemento máximo de uma coleção não-vazia.
 * T extends Comparable<T> garante a existência de compareTo em compile-time.
 */
public static <T extends Comparable<T>> T maximo(Collection<? extends T> colecao) {
    if (colecao.isEmpty()) throw new NoSuchElementException("Coleção vazia");
    T max = null;
    for (T elemento : colecao) {
        if (max == null || elemento.compareTo(max) > 0) {
            max = elemento;
        }
    }
    return max;
}

String maior = maximo(List.of("banana", "abacate", "cereja"));  // "cereja"
Integer maiorNum = maximo(List.of(3, 1, 4, 1, 5, 9));          // 9
```

**Regras de design para APIs genéricas:**

- Prefira type parameters (`<T>`) na assinatura do método quando o tipo precisa ser consistente em vários pontos (entrada e saída relacionados).
- Use wildcards (`?`) em parâmetros quando a consistência de tipo não é exigida entre parâmetros — isso aumenta a flexibilidade do chamador.
- Evite wildcards em tipos de retorno: forçar o chamador a lidar com `List<? extends Foo>` é difícil de usar; retorne `List<Foo>` e deixe a genericidade para os parâmetros.

## Armadilhas

### (1) Heap pollution com varargs e generics

**O problema:** varargs (`T... args`) é açúcar sintático para um array. Mas arrays de tipo genérico têm uma tensão fundamental: arrays são *covariantes* e guardam tipo em runtime (via *reifiable types*), enquanto generics usam erasure. O compilador cria `T[]` internamente para o vararg, que após erasure vira `Object[]`. Isso abre uma janela para que referências do tipo errado entrem no array, causando `ClassCastException` em locais inesperados — longe do ponto original de inserção. Esse fenômeno é chamado *heap pollution*.

```java
// Método vulnerável — varargs genérico
public static void métodoInseguro(List<String>... listas) {
    Object[] array = listas;            // ok para o compilador — covariância de arrays
    array[0] = List.of(42);             // heap pollution: List<Integer> entra onde esperava List<String>
    String s = listas[0].get(0);        // ClassCastException em runtime — longe da causa!
}

// Compilador emite: "unchecked or unsafe operations" ao compilar o chamador
métodoInseguro(List.of("a"), List.of("b"));
```

**Fix:** se o método for seguro (não vaza a referência do array para fora e não escreve no array), anote com `@SafeVarargs` para suprimir o warning nos call sites — e documente a garantia:

```java
// @SafeVarargs: afirma que o método não vaza o array de varargs
// Condição: o array é somente lido, nunca escrito ou exposto
@SafeVarargs
public static <T> List<T> combinar(List<T>... listas) {
    List<T> resultado = new ArrayList<>();
    for (List<T> lista : listas) {
        resultado.addAll(lista);   // lê listas, não escreve no array
    }
    return resultado;
}

List<String> combinado = combinar(List.of("a"), List.of("b", "c"));
```

`@SafeVarargs` pode ser aplicado apenas a métodos `static`, `final` ou construtores (métodos que não podem ser sobrescritos). Não use `@SafeVarargs` se o método escreve no array de varargs ou vaza a referência — nesse caso, o warning é legítimo.

---

### (2) Tentar `new T[]` ou `instanceof List<String>` (erasure proíbe)

**O problema:** type erasure apaga o tipo genérico em runtime. A JVM não sabe se está lidando com `List<String>` ou `List<Integer>`. Duas consequências diretas:

```java
// CASO 1: new T[] — ERRO de compilação
public class Pilha<T> {
    // ❌ Não compila: generic array creation
    private T[] elementos = new T[10];

    // ✔ Workaround aceito: cast com raw type (gera unchecked warning — aceitável aqui)
    @SuppressWarnings("unchecked")
    private T[] elementos2 = (T[]) new Object[10];

    // ✔ Workaround mais limpo: usar List<T>
    private List<T> elementos3 = new ArrayList<>();
}

// CASO 2: instanceof com tipo parametrizado — ERRO de compilação
Object obj = List.of("a", "b");
if (obj instanceof List<String> lista) {  // ❌ não compila
    // ...
}

// ✔ Correto: wildcard unbounded é reificável
if (obj instanceof List<?> lista) {       // ok
    // para verificação do tipo concreto, use type token
}

// CASO 3: overload por tipo genérico — ERRO de compilação (mesma erasure)
// ❌ Não compila: ambos viram processar(List) após erasure
public void processar(List<String> nomes) { /* ... */ }
public void processar(List<Integer> ids)  { /* ... */ }  // duplicate method after erasure
```

**Fix geral:** ao precisar de tipo em runtime, passe `Class<T>` explicitamente (type token) ou use `instanceof List<?>` seguido de cast explícito documentado.

---

### (3) Wildcard capture — não se pode escrever em `List<? extends T>`

**O problema:** `List<? extends Número>` é somente leitura para adição. O compilador não sabe se a lista é concretamente `List<Integer>`, `List<Double>` ou `List<BigDecimal>` — não pode permitir que você adicione elementos do tipo errado.

```java
public static void dobrarElementos(List<? extends Number> lista) {
    for (int i = 0; i < lista.size(); i++) {
        Number n = lista.get(i);             // leitura ok — retorna Number
        lista.set(i, n.doubleValue() * 2);   // ❌ ERRO de compilação
        // set espera ? extends Number, mas n.doubleValue() * 2 é double (Double)
        // e compilador não sabe se a lista aceita Double
    }
}
```

Esse comportamento é chamado **wildcard capture**: o compilador "captura" o wildcard como um tipo desconhecido `CAP#1`, e não consegue confirmar que `Double` é compatível com `CAP#1`.

**Fix 1:** use type parameter em vez de wildcard quando precisa escrever *e* ler:

```java
public static <T extends Number> void processar(List<T> lista) {
    // T é concreto no contexto do método — pode ler e usar
    for (T elemento : lista) {
        System.out.println(elemento.doubleValue());
    }
    // ainda não pode adicionar elementos (T desconhecido fora do método)
    // mas pode set se tiver referência do mesmo tipo
}
```

**Fix 2:** se precisar apenas ler e operar sobre os valores (não modificar a lista), `? extends T` é a escolha certa — trata-se de uma API de produção:

```java
// Correto: somar não precisa modificar a lista
public static double somar(List<? extends Number> lista) {
    return lista.stream()
                .mapToDouble(Number::doubleValue)
                .sum();
}
```

**Regra prática:** se você precisa *escrever* na coleção, use `? super T` (consumer) ou um type parameter `<T>`. Se só precisa *ler*, use `? extends T` (producer) — mas aceite que a coleção será efetivamente somente leitura naquele contexto.

## Em entrevista

### Frase pronta (inglês)

> "Java generics provide compile-time type safety through parameterized types, but the implementation relies on type erasure — all generic type information is removed at bytecode level, so `List<String>` and `List<Integer>` are indistinguishable at runtime."
>
> "This trade-off means you get backward compatibility with pre-generics code at the cost of runtime limitations: you cannot create generic arrays with `new T[]`, use `instanceof` with parameterized types like `instanceof List<String>`, or overload methods that differ only in their generic type arguments, because after erasure they all have the same signature."
>
> "When designing generic APIs, PECS — Producer Extends, Consumer Super — is the key decision rule: if a parameter gives you data to read, declare it as `? extends T`; if it receives data you write, declare it as `? super T`; this mirrors exactly what `Collections.copy` does with its `src` and `dst` parameters, and applying it consistently makes APIs that work with the full type hierarchy rather than just one concrete type."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| tipo genérico / tipo parametrizado | generic type / parameterized type |
| parâmetro de tipo | type parameter |
| curinga | wildcard |
| apagamento de tipo | type erasure |
| poluição de heap | heap pollution |
| limite superior / inferior | upper bound / lower bound |
| tipo bruto | raw type |
| token de tipo | type token |
| método ponte | bridge method |
| tipo não reificável | non-reifiable type |
| captura de curinga | wildcard capture |
| produtor / consumidor (PECS) | producer / consumer (PECS) |

## Veja também

- [[05 - Arrays e varargs]]
- [[02 - Tipos, variáveis e operadores]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [Generics — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/generics/index.html)
- [Wildcards — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/generics/wildcards.html)
- [Guidelines for Wildcard Use — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/generics/wildcardGuidelines.html)
- [Type Erasure — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/generics/erasure.html)
- [Non-Reifiable Types and Heap Pollution — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/generics/nonReifiableVarargsType.html)
