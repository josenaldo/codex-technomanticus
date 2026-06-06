---
title: "Garbage Collection — o conceito"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - jvm
  - iniciado
  - gc
aliases:
  - "Garbage Collection"
  - "GC"
  - "Coleta de lixo"
---

# Garbage Collection — o conceito

> [!abstract] TL;DR
> O GC libera automaticamente a memória de objetos **inalcançáveis** a partir dos GC roots (stacks de threads, campos estáticos, referências JNI). A aposta central é a *weak generational hypothesis*: a maioria dos objetos morre jovem, por isso coletar só a geração jovem com frequência é muito mais eficiente do que coletar o heap inteiro. Toda coleta tem custo — pausa stop-the-world ou consumo de CPU concorrente — e dominar esse vocabulário (minor/major, STW, promoção) é pré-requisito para ler logs e discutir tuning.

## O que é

O Garbage Collector é o subsistema da JVM responsável por gerenciar automaticamente a memória dinâmica. Em vez de exigir que o programador libere explicitamente memória (como em C com `free()`), a JVM determina quais objetos ainda são necessários e recupera os demais.

O critério não é "o que o programador não usa mais" — é **reachability**: um objeto é coletável quando nenhum caminho de referências o alcança a partir dos **GC roots**. GC roots são as âncoras vivas do grafo de objetos:

| GC root | Exemplos |
|---------|----------|
| Variáveis locais e parâmetros em stacks de threads ativas | `Order order = new Order()` dentro de um método em execução |
| Campos estáticos de classes carregadas | `private static final Map<K,V> CACHE = ...` |
| Referências JNI | Objetos passados a/de código nativo via JNI |
| Objetos internos da JVM | Classes do bootstrap classloader, strings internadas |

Qualquer objeto alcançável a partir de um root — diretamente ou por cadeia de referências — está **vivo**. O restante é lixo e pode ser reclamado.

## Por que importa

O GC é o principal trade-off do runtime Java: você ganha produtividade (sem `malloc`/`free`, sem double-free, sem dangling pointers), mas paga com:

- **Pausas stop-the-world** — o GC pode suspender todas as threads da aplicação por milissegundos (ou segundos, em coletores antigos).
- **Overhead de throughput** — mesmo coletores concorrentes consomem CPU em background.
- **Pressão de memória** — o heap precisa ter folga para o GC operar eficientemente; heap apertado significa coletas mais frequentes.

Para um desenvolvedor sênior, o vocabulário de GC é obrigatório em três contextos:

1. **Leitura de logs**: identificar minor GC frequente vs. major GC raro-mas-longo vs. Full GC catastrófico.
2. **Diagnóstico de latência**: distinguir spike de latência causado por STW de problema na aplicação.
3. **Discussão de tuning**: escolher coletor, ajustar tamanho de gerações e safepoint behavior — a nota [[11 - Tuning de GC — metodologia e prática]] cobre isso.

## Como funciona

### Reachability e GC roots

O GC opera sobre o **grafo de objetos**: cada objeto é um nó, cada campo de referência é uma aresta direcionada. O algoritmo de marcação (*mark phase*) percorre esse grafo a partir dos GC roots e marca tudo que for alcançável. O que não foi marcado ao final da travessia é lixo.

```text
GC roots
  ├── Thread 1 stack → Order → Customer → Address   ← VIVOS
  ├── Thread 2 stack → (vazio)
  └── static Cache  → Entry  → Product              ← VIVOS

Objeto órfão: Invoice sem referência de nenhum root  ← LIXO
```

A fase de varrimento (*sweep*) ou compactação (*compact*) reclaim a memória dos objetos não marcados. Coletores modernos como G1 e ZGC adicionam fases de relocação para compactar o heap sem fragmentação.

### A weak generational hypothesis (a maioria dos objetos morre jovem)

A hipótese geracional é a observação empírica que fundamenta todos os coletores modernos da JVM:

> **A grande maioria dos objetos tem vida muito curta.** Iteradores, strings intermediárias, builders, objetos de request/response — quase tudo é alocado e descartado em milissegundos.

Consequência prática: em vez de coletar o heap inteiro toda vez (caro), o GC divide o heap em **gerações** e concentra o esforço onde há mais lixo para coletar — a **Young Generation**.

```text
Young Generation (Eden + S0 + S1)
  → coletas frequentes, rápidas (maioria dos objetos já morreu)

Old / Tenured Generation
  → coletas raras, mais longas (poucos objetos, mas todos sobreviveram várias rounds)
```

A nota [[02 - Áreas de memória de runtime]] detalha a estrutura física das regiões de heap (Eden, Survivor, Old, humongous objects no G1).

### Minor, major e mixed collections (promoção, tenuring threshold)

| Tipo | O que coleta | Frequência | Custo típico |
|------|-------------|------------|--------------|
| **Minor GC** | Young Generation (Eden + Survivors) | Alta | Baixo (milissegundos) |
| **Major GC** | Old Generation | Baixa | Alto (dezenas a centenas de ms) |
| **Mixed GC** | Young + subset da Old (G1/ZGC) | Média | Intermediário |
| **Full GC** | Heap inteiro + Metaspace | Rara (indica problema) | Muito alto (STW longo) |

**Ciclo de vida de um objeto na geração jovem:**

1. Objeto alocado em **Eden**.
2. Minor GC: se o objeto ainda estiver vivo, é copiado para o espaço **Survivor** ativo (S0 ou S1). Cada sobrevivência incrementa o **age** (contador de tenuring).
3. Quando o age atinge o **tenuring threshold** (padrão: 15 no HotSpot, ajustável via `-XX:MaxTenuringThreshold`), o objeto é **promovido** para a **Old Generation**.
4. Objetos grandes (*humongous* no G1) podem ser promovidos diretamente para a Old sem passar pelos Survivors.

A promoção é o mecanismo pelo qual objetos genuinamente de longa duração chegam à Old Generation. Promoção prematura — objetos indo para a Old antes do tempo por falta de espaço nos Survivors — é um sinal de que o heap Young está subdimensionado.

### Stop-the-world e safepoints (o que são, por que existem)

**Stop-the-world (STW)** é uma pausa em que a JVM suspende todas as threads da aplicação para que o GC possa operar em um heap estático e consistente. Durante uma pausa STW, nenhuma thread de aplicação avança — do ponto de vista do usuário final, a aplicação congela.

Por que STW existe? O GC precisa percorrer o grafo de objetos de forma consistente. Se threads da aplicação continuassem rodando durante a marcação, elas poderiam criar novas referências ou apagar referências existentes enquanto o GC está no meio da travessia — o que corromperia a análise de reachability.

**Safepoints** são pontos no bytecode onde a JVM garante que o estado de cada thread está bem definido e pode ser inspecionado pelo GC. Antes de iniciar uma fase STW, a JVM pede que todas as threads atinjam um safepoint (via *safepoint poll*) e então as suspende. O tempo entre a requisição e a chegada de todas as threads ao safepoint é o **time-to-safepoint (TTSP)** — um TTSP alto pode inflar as pausas percebidas pelo usuário mesmo que a fase de GC em si seja curta.

Coletores modernos (G1, ZGC, Shenandoah) minimizam o uso de STW ao executar as fases mais longas (marcação, relocação) de forma **concorrente** — em paralelo com as threads da aplicação — reservando STW apenas para fases curtas que exigem consistência absoluta.

### Soft, weak e phantom references (visão geral — caches e cleanup)

Além das referências fortes (*strong references*, o tipo padrão em Java), a JVM suporta três níveis de referência que permitem ao programador influenciar quando o GC pode coletar um objeto:

| Tipo | Quando o GC coleta | Caso de uso típico |
|------|-------------------|--------------------|
| `SoftReference<T>` | Quando há pressão de memória | Caches sensíveis à memória disponível |
| `WeakReference<T>` | No próximo GC após o objeto tornar-se fracamente alcançável | Canonicalizing maps (`WeakHashMap`), listeners sem risco de leak |
| `PhantomReference<T>` | Após finalização, antes da reclamação final | Cleanup pós-mortem de recursos nativos (via `Cleaner`) |

A **hierarquia de reachability** — forte > soft > fraca > phantom > inalcançável — determina em qual ciclo de GC o objeto será enfileirado na `ReferenceQueue` associada.

> [!note] Escopo desta nota
> O catálogo completo de coletores (G1, ZGC, Shenandoah, Serial, Parallel) — suas arquiteturas, algoritmos e trade-offs — está em [[06 - Os coletores do HotSpot]]. Esta nota foca nos conceitos que todos os coletores compartilham.

## Na prática

### Promoção conceitual

Um objeto que sobrevive ao tenuring threshold acumula coletas na Young Generation antes de ser promovido:

```text
Ciclo 1: Order alocada em Eden
Minor GC 1: Order ainda referenciada → copiada para S0, age=1
Minor GC 2: Order ainda referenciada → copiada para S1, age=2
...
Minor GC 15: age=15 → Order promovida para Old Generation
```

Se o código de negócio cria muitas instâncias de `Order` que duram apenas o tempo de um request HTTP, essas instâncias devem morrer em Eden — nunca chegar à Old. Quando você vê promoção excessiva nos logs, o heap Young está pequeno ou há leak de referência que impede a coleta.

### `System.gc()` é pedido, não ordem

```java
// NÃO faça isso em produção:
System.gc(); // "sugere" ao GC que rode uma Full GC — pode ou não acontecer

// Em produção, a flag abaixo impede chamadas explícitas de terem efeito:
// -XX:+DisableExplicitGC
```

Chamar `System.gc()` em produção é um anti-padrão clássico. Na maioria dos casos, o efeito é o oposto do desejado: força uma Full GC (STW de todo o heap), introduzindo uma pausa longa e desnecessária. O GC do HotSpot tem ergonomics automáticos bem calibrados — deixe-o decidir quando coletar.

### Como um GC log parece (teaser)

Os logs unificados da JVM (flag `-Xlog:gc*`) mostram eventos como este:

```text
[0.314s][info][gc,start] GC(0) Pause Young (Normal) (G1 Evacuation Pause)
[0.314s][info][gc,task ] GC(0) Using 4 workers of 4 for evacuation
[0.322s][info][gc,heap ] GC(0) Eden regions: 24->0(24)
[0.322s][info][gc,heap ] GC(0) Survivor regions: 0->3(3)
[0.322s][info][gc      ] GC(0) Pause Young (Normal) 38M->6M(256M) 8.253ms
```

Ler esse log — entender o que cada campo significa, distinguir Pause Young de Pause Full, medir time-to-safepoint — é o assunto da nota [[10 - GC logs — unified logging e leitura]].

## Armadilhas

### (1) Chamar `System.gc()` em produção

**O problema:** muitos times adicionam `System.gc()` em rotinas de "limpeza de memória" ou após processar grandes lotes, acreditando que isso libera memória de forma controlada. Na prática, a chamada pode disparar uma **Full GC stop-the-world** sobre o heap inteiro, causando uma pausa de segundos em produção.

```java
// Anti-padrão: tentativa de "forçar liberação de memória"
public void processLargeReport(List<ReportData> data) {
    // ... processamento ...
    data.clear();
    System.gc(); // ← Full GC desnecessária; pode pausar a aplicação por segundos
}
```

**Fix:** remova a chamada e confie no GC ergonomics. Se a aplicação sofre de pressão de memória genuína, a solução está no dimensionamento do heap (`-Xmx`) ou no diagnóstico de leak — não em forçar coletas. Em servidores, adicione `-XX:+DisableExplicitGC` para que chamadas de `System.gc()` vindas de bibliotecas de terceiros também sejam ignoradas.

---

### (2) Cache estático sem bound — "leak na frente do GC"

**O problema:** o GC só coleta o que é **inalcançável**. Um cache estático que cresce indefinidamente mantém todos os seus valores fortemente alcançáveis — o GC não pode coletar nenhum deles, mesmo que nunca mais sejam acessados. Isso é um memory leak clássico que o GC é estruturalmente incapaz de resolver.

```java
// Leak: o GC nunca coleta nenhuma entrada deste cache
public class ProductCache {
    // Referência estática → sempre alcançável a partir de GC roots
    private static final Map<String, Product> CACHE = new HashMap<>();

    public static void cache(String id, Product p) {
        CACHE.put(id, p);  // cresce sem limite; entradas nunca são removidas
    }
}
```

**Fix:** use um cache com bound (tamanho máximo) e política de expiração — Caffeine ou Guava Cache são escolhas comuns em Java. Para casos onde a memória deve ser a restrição, use `SoftReference` como valor do cache: o GC pode limpar entradas sob pressão de memória. Para chaves que não devem impedir coleta, use `WeakHashMap`.

```java
// Com Caffeine: bound + expiração
Cache<String, Product> cache = Caffeine.newBuilder()
    .maximumSize(1_000)
    .expireAfterWrite(10, TimeUnit.MINUTES)
    .build();
```

---

### (3) Confundir GC com gestão de recursos nativos

**O problema:** o GC gerencia memória de objetos Java no heap. Ele **não fecha** arquivos, conexões de banco, sockets ou qualquer recurso nativo. Confiar no finalizador ou no GC para fechar recursos é um anti-padrão: o GC pode nunca rodar (ou rodar muito tarde), e o recurso fica vazando.

```java
// Errado: arquivo pode ficar aberto indefinidamente
public void processOrders(String filePath) throws IOException {
    BufferedReader reader = new BufferedReader(new FileReader(filePath));
    // ... lê dados ...
    // reader nunca é fechado explicitamente — "o GC vai cuidar"
}
```

**Fix:** use `try-with-resources` para qualquer recurso que implemente `AutoCloseable`. O recurso é fechado imediatamente ao sair do bloco, independentemente de GC.

```java
// Correto: fechamento garantido pelo compilador
public void processOrders(String filePath) throws IOException {
    try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
        // ... lê dados ...
    } // reader.close() chamado automaticamente aqui
}
```

Para limpeza de recursos nativos em APIs de baixo nível, a alternativa moderna ao `finalize()` (deprecado desde Java 9, removido no Java 18) é `java.lang.ref.Cleaner` com `PhantomReference`. Veja [[03-Dominios/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros|Exceções e tratamento de erros]] para o uso correto de `try-with-resources`.

## Em entrevista

### Frase pronta (inglês)

> "Garbage collection in the JVM is based on reachability, not on explicit deallocation. An object is eligible for collection when no path of references from any GC root — thread stacks, static fields, JNI references — leads to it. The GC traverses the object graph from those roots, marks everything reachable, and reclaims the rest."

> "The key insight behind generational GC is the weak generational hypothesis: most objects die young. By separating the heap into Young and Old generations and collecting the Young generation frequently — minor GCs — the GC avoids the cost of scanning the entire heap on every cycle. Objects that survive enough minor GCs are promoted to the Old generation, which is collected far less often in major or mixed GCs."

> "Every GC involves a trade-off between pause time, throughput, and memory footprint. Stop-the-world pauses happen when the JVM needs to suspend all application threads to ensure a consistent view of the object graph. Modern collectors like G1 and ZGC minimize STW by doing most work concurrently, but they can't eliminate it entirely. Understanding this vocabulary — minor GC, major GC, STW, safepoint, promotion — is essential for reading GC logs and having meaningful conversations about tuning."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| coleta de lixo | garbage collection (GC) |
| alcançabilidade | reachability |
| raízes do GC | GC roots |
| hipótese geracional fraca | weak generational hypothesis |
| coleta menor / coleta maior | minor GC / major GC |
| coleta mista | mixed GC |
| promoção de objeto | object promotion |
| limiar de tenuring | tenuring threshold |
| pausa stop-the-world | stop-the-world pause (STW) |
| ponto seguro | safepoint |
| referência fraca | weak reference |
| referência suave | soft reference |
| referência fantasma | phantom reference |

## Veja também

- [[02 - Áreas de memória de runtime]]
- [[06 - Os coletores do HotSpot]]
- [[10 - GC logs — unified logging e leitura]]
- [[11 - Tuning de GC — metodologia e prática]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros|Exceções e tratamento de erros]]
- [[03-Dominios/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#GC roots / reachability|GC roots (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#stop-the-world|stop-the-world (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#weak generational hypothesis|weak generational hypothesis (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#safepoint|safepoint (Dicionário)]]

## Referências

- [Garbage Collector Implementation — Oracle GC Tuning Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/gctuning/garbage-collector-implementation.html)
- [Introduction to Garbage Collection Tuning — Oracle GC Tuning Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/gctuning/introduction-garbage-collection-tuning.html)
- [java.lang.ref package — Javadoc Java 21 (SoftReference, WeakReference, PhantomReference)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ref/package-summary.html)
