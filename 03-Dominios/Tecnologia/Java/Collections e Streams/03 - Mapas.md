---
title: "Mapas"
created: 2026-06-04
updated: 2026-06-04
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - collections
  - iniciado
  - map
aliases:
  - HashMap
  - TreeMap
  - Mapas
---

# Mapas

> [!abstract] TL;DR
> `Map<K,V>` associa chaves únicas a valores. `HashMap` é a implementação padrão: O(1) amortizado para `get`/`put`, sem garantia de ordem, distribuição por hash com treeification automática de buckets em O(log n) a partir de Java 8. `LinkedHashMap` preserva a ordem de inserção (ou de acesso, para cache LRU). `TreeMap` mantém as chaves em ordem natural ou por `Comparator` com O(log n) garantido, expondo a API `NavigableMap` (`floorKey`, `ceilingKey`, `headMap`). A API moderna de `Map` (`merge`, `computeIfAbsent`, `getOrDefault`) elimina código boilerplate de null-check e padrões condicionais. Chave imutável com `hashCode`/`equals` corretos é um requisito inegociável.

## O que é

`Map<K,V>` é uma estrutura de dados que associa **chaves únicas** a **valores**. Diferente das coleções da hierarquia `Collection`, um mapa não armazena elementos individuais — armazena pares (entrada). Cada chave pode aparecer no mapa no máximo uma vez; o valor associado pode repetir.

A interface `Map` não estende `Iterable` nem `Collection`. Ela expõe três *views* mutáveis do seu conteúdo:

- `keySet()` — `Set<K>` das chaves.
- `values()` — `Collection<V>` dos valores (pode ter duplicatas).
- `entrySet()` — `Set<Map.Entry<K,V>>` dos pares, o ponto de entrada preferido para iteração.

As implementações mais usadas no JDK — `HashMap`, `LinkedHashMap` e `TreeMap` — fazem parte do **Java Collections Framework** e estão no pacote `java.util`.

## Por que importa

Mapas são a estrutura de busca por chave mais usada na prática: tabelas de frequência, índices invertidos, caches, configurações chave-valor, agrupamentos de dados. Conhecer qual implementação escolher e como usar a API moderna evita código verboso, corrige classes inteiras de bugs e é tema recorrente em entrevistas técnicas de nível pleno/sênior.

A partir do Java 8, a API ganhou métodos de alto nível que eliminam padrões verbosos de null-check e if-then-put: `getOrDefault`, `putIfAbsent`, `merge`, `compute`, `computeIfAbsent` e `forEach`. Saber usá-los corretamente distingue código idiomático de código defensivo com muitas condicionais.

## Como funciona

### `HashMap` por dentro

`HashMap<K,V>` armazena as entradas em um array de **buckets**. Ao inserir uma chave, a JVM chama `key.hashCode()`, aplica uma função de espalhamento interna e determina qual bucket receberá a entrada.

**Contrato `hashCode`/`equals`:** o Javadoc do Java 21 estabelece que se `a.equals(b)` é `true`, então `a.hashCode()` deve ser igual a `b.hashCode()`. A violação desse contrato é silenciosa e catastrófica: o mapa não consegue localizar entradas já inseridas, pois a busca usa `hashCode` para encontrar o bucket e `equals` para comparar dentro dele.

```java
// Contrato correto: mesma chave lógica → mesmo hashCode
record OrderId(String value) {}   // record implementa hashCode/equals automaticamente

Map<OrderId, Order> orders = new HashMap<>();
orders.put(new OrderId("ORD-1"), order);
// new OrderId("ORD-1").hashCode() == new OrderId("ORD-1").hashCode() → busca funciona
orders.get(new OrderId("ORD-1")); // retorna order ✓
```

**Parâmetros de performance:**
- *Capacidade inicial:* 16 buckets (padrão).
- *Fator de carga:* 0.75 (padrão). Quando `size > capacity × 0.75`, o mapa é redimensionado para aproximadamente o dobro. O redimensionamento reconstrói todos os buckets.
- *Complexidade:* O(1) amortizado para `get`/`put`, assumindo boa distribuição de hash.

**Treeification de bucket (Java 8+):** quando muitas chaves caem no mesmo bucket, a lista ligada interna é convertida para uma **árvore rubro-negra** quando a lista atinge `TREEIFY_THRESHOLD = 8` entradas **e** a capacidade total do mapa é ≥ 64. Isso muda a busca no bucket de O(n) para O(log n), protegendo contra ataques de colisão de hash e chaves com `hashCode` de má qualidade.

**Ordem:** indefinida e não garantida entre execuções. Não use `HashMap` quando a ordem importa.

---

### `LinkedHashMap` — ordem de inserção ou acesso

`LinkedHashMap<K,V>` estende `HashMap` com uma lista duplamente ligada que conecta as entradas na ordem em que foram inseridas (comportamento padrão). A performance é praticamente idêntica à do `HashMap`: O(1) amortizado para `get`/`put`/`remove`. A iteração percorre a lista ligada em O(n) proporcional ao *tamanho*, não à capacidade — vantagem sobre `HashMap` em mapas com alta capacidade e poucos elementos.

```java
Map<String, Integer> steps = new LinkedHashMap<>();
steps.put("parsing", 1);
steps.put("validation", 2);
steps.put("persistence", 3);

// Iteração preserva a ordem de inserção: parsing, validation, persistence
steps.forEach((step, order) -> System.out.println(order + ". " + step));
```

**Modo access-order (base de cache LRU):** o construtor `LinkedHashMap(int capacity, float loadFactor, boolean accessOrder)` com `accessOrder = true` reordena as entradas para que a menos recentemente acessada fique na frente. Sobrescrever `removeEldestEntry` implementa a política de eviction:

```java
int MAX = 100;
Map<String, Product> cache = new LinkedHashMap<>(16, 0.75f, true) {
    @Override
    protected boolean removeEldestEntry(Map.Entry<String, Product> eldest) {
        return size() > MAX; // remove o item menos recentemente usado quando passa do limite
    }
};
```

> [!note] Em access-order, até uma simples chamada `get()` é uma modificação estrutural que altera a ordem interna. O Javadoc alerta: iteração durante acesso concorrente lança `ConcurrentModificationException`.

---

### `TreeMap` / `NavigableMap` — mapa ordenado

`TreeMap<K,V>` implementa `NavigableMap<K,V>` usando uma **árvore rubro-negra**. Todas as operações principais (`get`, `put`, `remove`, `containsKey`) são O(log n) garantido — sem caso médio/pior.

As chaves são mantidas em **ordem natural** (se implementam `Comparable`) ou pela ordem de um `Comparator` fornecido no construtor. Chaves `null` não são permitidas.

Além das operações de `Map`, `NavigableMap` expõe navegação por intervalos:

| Método | Semântica |
|---|---|
| `floorKey(k)` | maior chave ≤ k (ou `null`) |
| `ceilingKey(k)` | menor chave ≥ k (ou `null`) |
| `lowerKey(k)` | maior chave < k estritamente |
| `higherKey(k)` | menor chave > k estritamente |
| `firstKey()` / `lastKey()` | extremos do mapa |
| `headMap(k)` | view das chaves < k |
| `tailMap(k)` | view das chaves ≥ k |
| `subMap(from, to)` | view do intervalo [from, to) |

```java
TreeMap<Integer, String> schedule = new TreeMap<>();
schedule.put(8, "standup");
schedule.put(14, "review");
schedule.put(17, "retrospectiva");

// Qual é o próximo evento a partir das 10h?
Integer next = schedule.ceilingKey(10); // 14

// Qual foi o último evento até as 15h?
Integer last = schedule.floorKey(15);   // 14

// Eventos entre 12h e 18h
NavigableMap<Integer, String> afternoon = schedule.subMap(12, true, 18, true);
// {14=review, 17=retrospectiva}
```

---

### A API rica de `Map`

Os métodos default da interface `Map` (Java 8+) cobrem os padrões mais comuns sem if-then-null:

| Método | Comportamento |
|---|---|
| `getOrDefault(k, def)` | retorna valor ou `def` se ausente |
| `putIfAbsent(k, v)` | insere só se chave ausente; retorna valor atual |
| `merge(k, v, fn)` | insere `v` se ausente; caso contrário, aplica `fn(valorAtual, v)` |
| `compute(k, fn)` | recomputa sempre; `fn(k, null)` se ausente; remove se `fn` retorna `null` |
| `computeIfAbsent(k, fn)` | computa e insere apenas se chave ausente ou mapeada para `null` |
| `computeIfPresent(k, fn)` | recomputa só se chave presente e valor não-null; remove se `fn` retorna `null` |
| `forEach(action)` | itera todos os pares como `BiConsumer<K,V>` |

## Na prática

### Contagem de frequência com `merge`

```java
String[] words = {"order", "product", "order", "category", "product", "order"};

Map<String, Integer> frequency = new HashMap<>();
for (String word : words) {
    frequency.merge(word, 1, Integer::sum);
}
// {order=3, product=2, category=1}
```

`merge` elimina o padrão verboso `getOrDefault` + `put`. Se a chave não existe, insere `1`; caso contrário, soma `1` ao valor atual.

---

### Agrupamento com `computeIfAbsent`

```java
record Order(String category, String id) {}

List<Order> orders = List.of(
    new Order("electronics", "ORD-1"),
    new Order("books", "ORD-2"),
    new Order("electronics", "ORD-3")
);

Map<String, List<Order>> byCategory = new HashMap<>();
for (Order o : orders) {
    byCategory.computeIfAbsent(o.category(), k -> new ArrayList<>()).add(o);
}
// {electronics=[ORD-1, ORD-3], books=[ORD-2]}
```

`computeIfAbsent` cria a lista apenas na primeira vez que a categoria aparece e a retorna diretamente, evitando a verificação manual `if (map.containsKey(k))`.

---

### `TreeMap` para ranges

```java
TreeMap<Integer, String> priceRanges = new TreeMap<>();
priceRanges.put(0,    "free");
priceRanges.put(50,   "budget");
priceRanges.put(200,  "standard");
priceRanges.put(1000, "premium");

// Qual faixa se aplica a um produto de R$ 350?
String tier = priceRanges.floorEntry(350).getValue(); // "standard"
```

`floorEntry` encontra o maior preço-âncora que não excede o valor dado — padrão típico de classificação por faixa.

## Armadilhas

### (1) `hashCode`/`equals` inconsistente ou chave mutada após inserção

**O problema:** se a classe usada como chave não implementa `hashCode` e `equals` corretamente, ou se o objeto-chave é mutado depois de inserido, o mapa não consegue localizar a entrada. A chave "some": `put` registra a entrada em um bucket, mas após a mutação `get` calcula um hash diferente, vai a outro bucket e não acha nada.

```java
// RUIM — classe mutável sem hashCode/equals customizado
class ProductKey {
    String code;
    ProductKey(String code) { this.code = code; }
    // sem @Override de equals/hashCode: usa identidade de referência
}

Map<ProductKey, String> catalog = new HashMap<>();
ProductKey key = new ProductKey("P-001");
catalog.put(key, "Notebook");

key.code = "P-999"; // mutação da chave após inserção

catalog.get(key); // null — a entrada foi para o bucket de "P-001"
```

```java
// FIX — use chave imutável com hashCode/equals corretos
record ProductKey(String code) {}

Map<ProductKey, String> catalog = new HashMap<>();
catalog.put(new ProductKey("P-001"), "Notebook");
catalog.get(new ProductKey("P-001")); // "Notebook" ✓
```

> [!tip] `record` gera `hashCode` e `equals` baseados em todos os componentes automaticamente e é imutável por definição. Prefira `record` ou tipos imutáveis como chaves de mapas.

---

### (2) `HashMap` em acesso concorrente — use `ConcurrentHashMap`

**O problema:** `HashMap` não é thread-safe. Acessos concorrentes sem sincronização produzem resultados incorretos silenciosos, `ConcurrentModificationException` durante iteração e, historicamente (antes do Java 8), podiam causar loop infinito por corrupção da estrutura interna de encadeamento de buckets.

```java
// RUIM — HashMap compartilhado entre threads sem sincronização
Map<String, Integer> shared = new HashMap<>();

// Thread A e Thread B executando simultaneamente:
shared.put("counter", shared.getOrDefault("counter", 0) + 1);
// Resultado imprevisível: race condition, dados corrompidos
```

```java
// FIX — use ConcurrentHashMap para acesso concorrente
// Ver [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections|Concurrent collections]]
Map<String, Integer> safe = new ConcurrentHashMap<>();
safe.merge("counter", 1, Integer::sum); // operação atômica
```

---

### (3) `get` retornando `null` — ausência vs. valor nulo

**O problema:** `HashMap` permite `null` como valor. `map.get(key)` retorna `null` tanto quando a chave não existe quanto quando ela existe com valor `null`. Código que trata esses casos como equivalentes produz lógica incorreta.

```java
// RUIM — null ambíguo: ausente ou valor nulo?
Map<String, String> config = new HashMap<>();
config.put("timeout", null); // valor explicitamente nulo

String timeout = config.get("timeout"); // null
// É null porque a chave não existe, ou porque o valor é null?
if (timeout == null) {
    timeout = "30s"; // sobrescreve um null intencional — bug silencioso
}
```

```java
// FIX 1 — getOrDefault não distingue null de ausente; use containsKey quando importar
if (!config.containsKey("timeout")) {
    config.put("timeout", "30s");
}

// FIX 2 — putIfAbsent: insere só se a chave não existe (ou o valor é null)
config.putIfAbsent("timeout", "30s");

// FIX 3 — prefira não armazenar null como valor; use Optional ou um sentinel
Map<String, Optional<String>> strict = new HashMap<>();
strict.put("timeout", Optional.empty()); // intenção explícita
```

## Em entrevista

### Frase pronta (inglês)

> "`HashMap` gives you O(1) amortized performance for `get` and `put` by distributing keys across buckets using their `hashCode`, with collision chaining resolved by linked lists — or, since Java 8, by a red-black tree when a bucket exceeds eight entries (`TREEIFY_THRESHOLD`), which brings worst-case lookup in that bucket down from O(n) to O(log n)."
>
> "The `hashCode`/`equals` contract is non-negotiable for any class used as a map key: if two objects are equal by `equals`, they must return the same `hashCode`; breaking this contract causes entries to silently disappear from the map. Using an immutable `record` as a key is the idiomatic fix — the compiler generates the correct contract automatically."
>
> "The modern `Map` API — `merge`, `computeIfAbsent`, `getOrDefault` — eliminates most null-check boilerplate. `merge(key, 1, Integer::sum)` is the canonical one-liner for frequency counting; `computeIfAbsent(key, k -> new ArrayList<>()).add(item)` is the canonical pattern for grouping. If ordering matters, `TreeMap` gives you `NavigableMap` with `floorKey` and `ceilingKey` for range queries at O(log n) guaranteed."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| tabela de dispersão | hash table |
| função de hash | hash function |
| colisão de hash | hash collision |
| balde / compartimento | bucket |
| arborificação de bucket | bucket treeification |
| fator de carga | load factor |
| rehashing / redimensionamento | rehashing / resize |
| chave imutável | immutable key |
| mapa navegável | navigable map |
| ordem de inserção | insertion order |
| ordem de acesso | access order |

## Veja também

- [[01 - O Collections Framework]]
- [[02 - Listas, conjuntos e filas]]
- [[06 - Comparable e Comparator]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/13 - Records e record patterns|Records]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/07 - Concurrent collections|Concurrent collections]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#hashCode / equals (contrato)|hashCode / equals]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#treeification|treeification]]

## Referências

- [Map — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Map.html)
- [HashMap — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html)
- [LinkedHashMap — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/LinkedHashMap.html)
- [TreeMap — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/TreeMap.html)
- [Maps — dev.java (Oracle)](https://dev.java/learn/api/collections-framework/maps/)
