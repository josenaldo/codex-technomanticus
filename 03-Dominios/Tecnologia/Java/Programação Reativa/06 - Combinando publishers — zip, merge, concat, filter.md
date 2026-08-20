---
title: "Combinando publishers — zip, merge, concat, filter"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - reativa
  - adepto
  - operadores
aliases:
  - "combinando publishers"
  - "zip merge concat"
---

# Combinando publishers — zip, merge, concat, filter

> [!abstract] TL;DR
> Para juntar fontes reativas, três operadores resolvem a maioria dos casos: **`zip`** combina elemento-a-elemento, esperando que *todos* os lados emitam antes de produzir cada par; **`merge`** intercala os itens conforme chegam (assina tudo ao mesmo tempo, sem garantir ordem entre fontes); **`concat`** concatena de forma ordenada — assina a próxima fonte só depois que a anterior completa. Do outro lado, operadores de filtro (**`filter`**, **`take`**, **`skip`**, **`distinct`**) reduzem o fluxo: descartam itens por predicado, pegam ou pulam os primeiros N, ou ignoram duplicatas.

## O que é

Programação reativa raramente lida com uma fonte só. Você consulta um `Customer` por um lado e seus `Order`s por outro, ou agrega vários streams de eventos num só. **Combinar publishers** é o ato de pegar dois ou mais `Mono`/`Flux` e produzir um único publisher de saída.

Reactor oferece um leque de operadores de combinação, mas três cobrem a maior parte do trabalho diário, e diferem em *como* tratam tempo e ordem:

- **`zip`** — combina elemento-a-elemento. Segundo a documentação, ele emite "each time all sides have emitted": espera o N-ésimo item de *cada* fonte antes de produzir o N-ésimo resultado combinado.
- **`merge`** — emite "in emission order (combined items emitted as they come)": assina todas as fontes ansiosamente e repassa os itens na ordem em que de fato chegam.
- **`concat`** — emite "in sequential order": assina uma fonte por vez, drena ela por completo, e só então passa pra próxima.

Em paralelo, há os operadores de **filtro**, que não juntam fontes — eles *afinam* um único fluxo, removendo elementos.

## Por que importa

A escolha entre `zip`, `merge` e `concat` é uma das perguntas clássicas de entrevista reativa, e por bom motivo: trocar um pelo outro muda silenciosamente a semântica do seu sistema.

- **Ordem é um contrato.** Usar `merge` onde a ordem importava produz bugs intermitentes — funciona no teste local (fontes rápidas) e quebra em produção (uma fonte lenta intercala diferente). `concat` garante ordem; `merge` não.
- **Latência.** `concat` é sequencial: o tempo total é a *soma* das fontes. `merge` e `zip` assinam em paralelo, então o custo tende ao *máximo*, não à soma. Para duas chamadas HTTP independentes, isso é a diferença entre 200 ms e 100 ms.
- **Perda de dados.** `zip` para quando a *fonte mais curta* completa — itens a mais nas outras fontes são descartados. Combinar fluxos de tamanhos diferentes com `zip` por engano perde dados sem avisar.
- **Filtro no lugar errado.** Filtrar em memória o que deveria ser cláusula `WHERE` no banco traz linhas demais pela rede e desperdiça CPU.

## Como funciona

### `zip`: combina elemento-a-elemento (espera os dois)

`zip` é o operador de **correlação posicional**. Ele alinha as fontes por índice: o 1º item de A com o 1º de B, o 2º com o 2º, e assim por diante. Para emitir o par de índice N, ele precisa que *todas* as fontes já tenham emitido o item N — daí "espera os dois".

Com `Mono`, o caso é especialmente comum: `Mono.zip(a, b)` dispara `a` e `b` em paralelo e te entrega um `Tuple2` quando ambos resolvem. É o jeito idiomático de fazer duas buscas independentes e juntar os resultados.

Com `Flux`, `zip` produz um fluxo de tuplas (ou aplica um combinador). O ponto de atenção: ele cadencia pelo mais lento e termina junto com o mais curto.

### `merge` vs `concat`: intercalado (conforme chegam) vs ordenado (um após o outro)

Esses dois resolvem o mesmo problema — "junte os itens de A e B num só fluxo" — com semânticas opostas de tempo:

- **`merge`** assina A *e* B imediatamente e repassa cada item no instante em que ele chega. A saída é **intercalada** pela velocidade real das fontes, sem garantia de que todos os itens de A venham antes dos de B. Bom quando você quer o resultado o mais cedo possível e a origem de cada item não importa.
- **`concat`** assina A, repassa todos os itens de A, espera A **completar**, e só então assina B. A saída é **ordenada**: A inteiro, depois B inteiro. É o que você quer quando a ordem entre fontes é um contrato.

Resumindo: `merge` otimiza latência ao custo da ordem; `concat` garante ordem ao custo de serializar o tempo.

### Filtrando: `filter` / `take` / `skip` / `distinct`

Operadores de filtro afinam um único fluxo, descartando elementos:

- **`filter`** — remove elementos "based on an arbitrary criteria": mantém só os que satisfazem o predicado.
- **`take`** — limita "by taking N elements at the beginning of the sequence": pega os primeiros N e completa.
- **`skip`** — descarta "by skipping elements at the beginning of the sequence": pula os primeiros N e emite o resto.
- **`distinct`** — deduplica "by ignoring duplicates in the whole sequence (logical set)": ignora valores já vistos no fluxo inteiro.

Eles compõem livremente com os operadores de combinação: é comum `merge`-ar fontes e depois `distinct()` pra remover repetições, ou `concat` e `take(10)` pros primeiros dez.

### Quando a ordem importa (concat) vs quando não (merge)

A regra prática para escolher entre os dois é uma pergunta só: **a ordem entre as fontes é parte do contrato?**

- Se *sim* — paginação que precisa sair na sequência das páginas, log que deve preservar ordem cronológica das fontes, montagem de um documento por seções — use **`concat`**. Você troca paralelismo por garantia de ordem.
- Se *não* — agregar notificações de vários canais, juntar resultados de réplicas onde só o conjunto importa — use **`merge`**. Você ganha latência menor e aceita intercalação arbitrária.

E quando você precisa de **pares correlacionados** (não de uma união), nenhum dos dois serve: é caso de `zip`.

## Na prática

Combinando dois resultados independentes com `Mono.zip` (espera ambos):

```java
import reactor.core.publisher.Mono;
import reactor.util.function.Tuple2;

Mono<Customer> customerMono = customerRepository.findById(customerId);
Mono<Order> orderMono = orderRepository.findLatestByCustomer(customerId);

// zip dispara as duas buscas em paralelo e espera AS DUAS resolverem.
Mono<Tuple2<Customer, Order>> combinado = Mono.zip(customerMono, orderMono);

Mono<String> resumo = Mono.zip(customerMono, orderMono)
        .map(tuple -> {
            Customer c = tuple.getT1();
            Order o = tuple.getT2();
            return c.name() + " — último pedido: " + o.id();
        });
```

`merge` (conforme chegam) vs `concat` (ordenado):

```java
import reactor.core.publisher.Flux;

Flux<Order> pendentes = orderService.streamPendentes();
Flux<Order> arquivados = orderService.streamArquivados();

// merge: intercala — itens saem na ordem em que cada fonte os entrega.
Flux<Order> intercalado = Flux.merge(pendentes, arquivados);

// concat: ordenado — todos os pendentes, depois todos os arquivados.
Flux<Order> ordenado = Flux.concat(pendentes, arquivados);
```

Filtrando o fluxo combinado:

```java
import reactor.core.publisher.Flux;
import java.math.BigDecimal;

Flux<Order> relevantes = Flux.merge(pendentes, arquivados)
        .filter(o -> o.total().compareTo(BigDecimal.valueOf(100)) > 0) // só pedidos acima de 100
        .distinct()                     // remove duplicatas (mesmo Order nas duas fontes)
        .take(20);                      // os primeiros 20 e completa
```

Marble simplificado — `merge` vs `concat` para as mesmas duas fontes:

```text
fonte A:   a1......a2..........a3---|
fonte B:   ....b1......b2--|

merge(A,B):  a1..b1..a2..b2..a3---|     (intercalado, conforme chegam)

concat(A,B): a1......a2..........a3--b1......b2--|
                                   ^ B só começa quando A completa
```

## Armadilhas

### (1) Usar `merge` quando a ordem importava

Você junta duas fontes com `merge` e o teste passa — porque localmente ambas são rápidas e saem "quase" na ordem que você esperava. Em produção, uma fonte fica lenta e os itens intercalam diferente, quebrando uma invariante de ordem.

```java
// BUG: precisa que as páginas saiam em ordem, mas merge não garante isso.
Flux<Page> paginas = Flux.merge(buscarPagina(1), buscarPagina(2), buscarPagina(3));
// page 2 pode sair antes da page 1 se a fonte 1 demorar mais.
```

Fix: quando a ordem entre fontes é contrato, use `concat` — ele assina a próxima fonte só depois que a anterior completa, garantindo A inteiro, depois B inteiro.

```java
Flux<Page> paginas = Flux.concat(buscarPagina(1), buscarPagina(2), buscarPagina(3));
```

### (2) `zip` com fluxos de tamanhos diferentes (para no menor — perde elementos)

`zip` alinha por posição e completa quando a fonte *mais curta* completa. Se as fontes têm tamanhos diferentes, os itens extras da fonte mais longa são silenciosamente descartados — sem erro, sem aviso.

```java
import reactor.core.publisher.Flux;

Flux<String> nomes  = Flux.just("Ana", "Bia", "Caio");   // 3 itens
Flux<Order> orders  = Flux.just(o1, o2, o3, o4, o5);      // 5 itens

// zip emite apenas 3 pares — o4 e o5 são DESCARTADOS.
Flux<String> pares = Flux.zip(nomes, orders, (n, o) -> n + ": " + o.id());
```

Fix: garanta que os fluxos tenham a mesma cardinalidade antes de `zip`, ou repense o desenho — talvez você quisesse `flatMap` (correlacionar por chave) e não correlação posicional por índice.

### (3) `filter` pesado que deveria ser query no banco

Você puxa o catálogo inteiro do banco e filtra em memória com `.filter(...)`. Funciona com poucos registros, mas traz linhas demais pela rede e gasta CPU à toa — o filtro deveria ser uma cláusula `WHERE` empurrada pro banco.

```java
import reactor.core.publisher.Flux;
import java.math.BigDecimal;

// BUG: carrega TODOS os products e descarta a maioria em memória.
Flux<Product> caros = productRepository.findAll()
        .filter(p -> p.price().compareTo(BigDecimal.valueOf(1000)) > 0);
```

Fix: empurre o predicado pra origem — um método de repositório com a condição na query (`findByPriceGreaterThan(1000)`). Reserve `filter` reativo pra critérios que o banco não consegue expressar ou pra fontes que não são bancos.

```java
Flux<Product> caros = productRepository.findByPriceGreaterThan(1000);
```

## Em entrevista

### Frase pronta (inglês)

> When you need to combine reactive sources in Project Reactor, the three core operators differ in how they handle time and ordering. `zip` correlates element-by-element and only emits once all sides have emitted, so it waits for every source — it's ideal for firing two independent lookups in parallel and joining their results, but be aware it completes when the shortest source completes and drops the extra elements. `merge` subscribes to all sources eagerly and emits items as they arrive, interleaving them with no ordering guarantee between sources, which minimizes latency. `concat`, by contrast, subscribes to one source at a time and fully drains it before moving on, preserving order at the cost of serializing the work. On the filtering side, `filter`, `take`, `skip`, and `distinct` trim a single stream — and a heavy `filter` in memory is often a sign the predicate should have been pushed down to the database as a `WHERE` clause.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| combinar publishers | combine publishers |
| elemento-a-elemento | element-by-element |
| intercalar / intercalado | interleave / interleaved |
| ordem sequencial | sequential order |
| esperar todos os lados emitirem | wait for all sides to emit |
| empurrar o filtro pro banco | push the filter down to the database |
| correlação posicional | positional correlation |
| descartar elementos | drop elements |

## Veja também

- [[03-Dominios/Tecnologia/Java/Programação Reativa/05 - map e flatMap — transformando o fluxo|map e flatMap]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/07 - Error handling reativo — onErrorResume, onErrorReturn, retry|Error handling reativo]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Project Reactor Reference — Which operator do I need? (combining e filtering): https://projectreactor.io/docs/core/release/reference/apdx-operatorChoice.html
- Project Reactor Reference — Transforming an Existing Sequence (`filter`, `distinct`, `take`, `skip`): https://projectreactor.io/docs/core/release/reference/coreFeatures.html
- Project Reactor — `Flux` Javadoc (`zip`, `merge`, `concat`): https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html
- Project Reactor — `Mono.zip` Javadoc: https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html
