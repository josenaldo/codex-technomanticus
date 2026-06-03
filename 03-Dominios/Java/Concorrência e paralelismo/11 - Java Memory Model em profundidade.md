---
title: "Java Memory Model em profundidade"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - concorrencia
  - magus
  - jmm
  - volatile
aliases:
  - Java Memory Model
  - JMM
  - happens-before
  - volatile
---

# Java Memory Model em profundidade

> [!abstract] TL;DR
> O **Java Memory Model (JMM)** define o que uma thread pode *legalmente observar* quando lê uma variável escrita por outra thread. Existe porque compiladores, o JIT e as CPUs **reordenam** instruções e mantêm valores em **caches/store buffers** locais — em código single-thread isso é invisível, mas em multi-thread quebra programas aparentemente corretos. A relação fundamental é **happens-before**: se A *happens-before* B, então os efeitos de A são visíveis para B. As arestas de happens-before são poucas e precisas — *program order*, unlock/lock do mesmo monitor, write/read da mesma variável `volatile`, `Thread.start()`, `Thread.join()`, e transitividade. **`volatile`** dá visibilidade e ordenação (proíbe reordenar leituras/escritas ao redor dela), mas **não dá atomicidade composta** — `i++` continua sendo um read-modify-write sujeito a corrida. **Campos `final`** têm uma garantia extra: se o objeto for **publicado com segurança** (sem vazar `this` durante a construção), toda thread vê os `final` corretamente inicializados, mesmo sem sincronização — é o que torna `String` e `Integer` imutáveis na prática. **Double-checked locking** só é correto com o campo `volatile`. Bugs de visibilidade têm output **não-determinístico**: podem passar em milhões de execuções e falhar em produção sob outro hardware ou JIT.

## O que é

O **Java Memory Model** é a parte da especificação da linguagem (JLS §17.4) que responde a uma única pergunta difícil: *quando uma thread escreve uma variável, quais valores outra thread tem permissão de ler?* A resposta intuitiva — "o último valor escrito" — está **errada** num sistema multiprocessado sem sincronização explícita.

Há duas razões físicas e duas razões de software pelas quais a intuição falha:

- **CPUs reordenam.** Processadores modernos executam instruções fora de ordem e usam *store buffers*: uma escrita em memória fica num buffer local do core antes de se tornar visível para os outros cores. Dois cores podem observar escritas em ordens diferentes.
- **Caches não são coerentes "de graça" para o programador.** Embora o hardware tenha protocolos de coerência de cache, o JMM não garante propagação imediata sem um ponto de sincronização — o custo de forçar isso (barreiras de memória) é pago apenas onde você pede.
- **O compilador `javac` e o JIT reordenam e otimizam.** Operações sem dependência aparente podem ser trocadas de ordem, e leituras repetidas de um campo podem ser **içadas** (*hoisted*) para fora de um loop, virando uma leitura única em registrador.
- **A regra de ouro do otimizador é "as if serial".** Qualquer reordenação é permitida desde que o resultado de uma thread *isolada* seja o mesmo. Essa garantia vale **por thread**, não entre threads — daí o perigo.

O exemplo mínimo: sem sincronização, este código pode imprimir `0`.

```java
// hipotético: dois campos de instância compartilhados, SEM volatile/sync
int x = 0;
boolean flag = false;

// Thread 1
x = 1;          // (a)
flag = true;    // (b)

// Thread 2
if (flag) {                 // (c)
    System.out.println(x);  // (d) — pode imprimir 0!
}
```

Por quê? A CPU pode tornar `(b)` visível antes de `(a)`; o JIT pode reordenar `(a)` e `(b)` (não há dependência de dados entre elas); e mesmo que a ordem seja preservada, a Thread 2 pode ler `flag` de um valor recente mas `x` de um cache obsoleto. Não há nenhuma aresta de *happens-before* entre `(a)` e `(d)`, então o JMM **autoriza** a leitura de `x == 0`.

O JMM existe para dar ao programador um contrato preciso: um conjunto pequeno de construções (`synchronized`, `volatile`, `final`, `start`/`join`, atômicos) que estabelecem *happens-before* e, portanto, visibilidade garantida. Tudo o que está fora dessas arestas é, por especificação, indefinido entre threads.

## Por que importa

Em uma entrevista sênior de Java, JMM é o tópico que separa "sei usar `synchronized`" de "entendo *por que* preciso dele". É também a fonte dos bugs de concorrência mais caros, porque eles são **silenciosos e não-determinísticos**:

- **O custo do erro é assimétrico.** Um bug de visibilidade pode não se manifestar em desenvolvimento, em CI, nem em milhões de requisições — e então falhar sob um JIT diferente, um processador com modelo de memória mais fraco (ARM é mais fraco que x86), ou sob carga que muda o *timing*. Você não consegue *testar* a ausência de uma corrida; só consegue *raciocinar* sobre ela com o modelo.
- **É a base de tudo o mais.** `volatile`, locks, `AtomicInteger`, `ConcurrentHashMap`, `CompletableFuture` — todos entregam suas garantias *em termos de happens-before*. Sem o modelo, as garantias de cada um seriam afirmações soltas; com ele, formam um sistema componível.
- **Decisões de design dependem dele.** Saber que `final` dá publicação segura justifica preferir imutabilidade. Saber que `volatile` não dá atomicidade composta justifica escolher `AtomicLong` ou um lock. Saber que DCL exige `volatile` evita um singleton sutilmente quebrado.

A consequência prática a internalizar: **acesso concorrente a estado mutável compartilhado sem uma aresta de happens-before é um bug**, mesmo quando "funciona". O fato de funcionar é coincidência de hardware e JIT, não correção.

## Como funciona

### Reordering (compilador, CPU, store buffers)

Há três níveis independentes de reordenação, e o JMM os trata uniformemente: qualquer um deles pode acontecer, e o modelo só proíbe os reordenamentos que cruzariam uma aresta de *happens-before*.

1. **Compilador (`javac` + JIT).** O JIT é o reordenador mais agressivo. Além de trocar a ordem de instruções independentes, ele faz *hoisting*: se um campo não-`volatile` é lido num loop e o compilador não vê escrita a ele, pode lê-lo **uma vez** e cachear em registrador — transformando `while (!stop)` num loop potencialmente infinito.
2. **CPU (execução out-of-order).** O processador despacha instruções conforme operandos ficam prontos, não na ordem do programa.
3. **Store buffers / hierarquia de memória.** Uma escrita vai primeiro para um *store buffer* local do core. Outro core só a vê quando ela é drenada para a cache compartilhada/memória. É por isso que duas threads podem discordar sobre a ordem de duas escritas.

A garantia que o programa single-thread tem é a regra **"as-if-serial"**: o resultado observável de *uma thread isolada* é como se tudo executasse em program order. Mas essa garantia **não se estende** entre threads. Sincronização (qualquer construção que crie *happens-before*) insere as **barreiras de memória** (*memory fences*) necessárias para conter essas reordenações nos pontos certos.

### Visibility (sem garantia entre threads sem sincronização)

**Visibilidade** é a pergunta "depois que a Thread 1 escreve `x`, a Thread 2 enxerga o novo valor?". Sem uma aresta de *happens-before* entre a escrita e a leitura, **não há garantia nenhuma** — a Thread 2 pode ver o valor antigo indefinidamente.

```java
// hipotético: flag SEM volatile
boolean stop = false;   // não-volatile

// Thread worker
while (!stop) {
    // trabalho
}
// outra thread faz: stop = true;
// PROBLEMA: o worker pode nunca enxergar a mudança — loop infinito
```

O JIT está autorizado a içar a leitura de `stop` para fora do loop (não há escrita visível a `stop` dentro dele), virando efetivamente `if (!stop) while(true) {}`. Isso é uma otimização **legal** sob o JMM, porque nada estabelece happens-before entre a escrita de `stop` em outra thread e a leitura no loop.

### Atomicidade (long/double podem ser não-atômicos sem volatile)

**Atomicidade** é a garantia de que uma operação acontece "de uma vez", sem estados intermediários observáveis. Duas nuances do JMM:

- **`long` e `double` não-`volatile` podem ter escritas/leituras não-atômicas.** O JLS (§17.7) permite que uma escrita de 64 bits a um campo não-`volatile` seja realizada como **duas** escritas de 32 bits. Em teoria, outra thread poderia ler uma palavra "rasgada" (*word tearing*) — os 32 bits altos de um valor e os 32 baixos de outro. Marcar o campo como `volatile` **garante** atomicidade da leitura/escrita de 64 bits. (Na prática, JVMs de 64 bits costumam fazer essas operações atômicas mesmo sem `volatile`, mas isso **não é garantido pela especificação** — não conte com isso.)
- **Atomicidade simples ≠ atomicidade composta.** Mesmo que ler e escrever um campo seja atômico, uma sequência *read-modify-write* (como `i++`) **não** é. Ela é três operações: ler, somar, escrever. Duas threads podem ler o mesmo valor, somar, e escrever — perdendo um incremento. `volatile` não conserta isso (ver Armadilha 2).

### Happens-before (a relação fundamental)

**Happens-before** (escrita *hb*) é uma relação de ordem parcial entre ações. Sua definição operacional: se `hb(A, B)`, então (1) os efeitos de memória de A são **visíveis** para B, e (2) A é considerado ordenado **antes** de B na ordem de sincronização. **Importante:** happens-before *não* significa "executa antes no tempo de relógio" — significa "se A e B forem ordenados, B vê o que A fez". Sem uma aresta hb, o JMM permite que B não veja A.

As arestas de happens-before definidas pelo JLS §17.4.5 (mais as relações *synchronizes-with* de §17.4.4 que as induzem):

1. **Program order** — se `x` e `y` são ações da *mesma* thread e `x` vem antes de `y` em program order, então `hb(x, y)`. (É o que dá a ilusão sequencial dentro de uma thread.)
2. **Monitor lock** — um *unlock* do monitor `m` *synchronizes-with* todo *lock* subsequente do mesmo `m`; logo, o unlock happens-before o lock seguinte. Tudo o que uma thread fez antes de soltar o lock é visível para a próxima que o adquirir.
3. **Volatile** — uma escrita a uma variável `volatile` `v` *synchronizes-with* toda leitura subsequente de `v` por qualquer thread; logo, a escrita happens-before a leitura.
4. **Thread start** — a ação que chama `Thread.start()` happens-before a primeira ação na thread iniciada. (Tudo que a thread-mãe preparou antes do `start()` é visível para a thread-filha.)
5. **Thread termination / join** — todas as ações de uma thread `T1` happens-before qualquer outra thread retornar com sucesso de `T1.join()` (ou detectar via `T1.isAlive() == false`). É o espelho do `start`.
6. **Default write** — a escrita do valor-padrão (`0`, `false`, `null`) de cada variável happens-before a primeira ação de qualquer thread. (Por isso você nunca "lê lixo" não inicializado em Java — no pior caso lê o zero/null padrão.)
7. **Interruption** — `T1` interromper `T2` happens-before `T2` (ou outra) detectar a interrupção via `isInterrupted()` ou `InterruptedException`.
8. **Final fields** — o congelamento (*freeze*) dos campos `final` no fim do construtor tem garantia especial de visibilidade para threads que veem o objeto **após** a construção (detalhado abaixo).
9. **Transitividade** — se `hb(x, y)` e `hb(y, z)`, então `hb(x, z)`. É o que permite **encadear**: a escrita de `x` antes de `flag=true` (volatile) torna-se visível para quem lê `flag==true` *e* depois lê `x` — por program order de um lado, aresta volatile no meio, program order do outro.

A transitividade é o motor que torna o modelo útil: uma única aresta `volatile` (ou um único lock) "carrega junto" todas as escritas anteriores em program order.

### `volatile`

`volatile` é o mecanismo mais leve do JMM e o **dono** desta nota. Ele dá duas garantias e nega uma terceira:

- **Visibilidade** — uma escrita `volatile` é imediatamente visível para leituras subsequentes de qualquer thread. Sem hoisting: cada leitura vai à memória.
- **Ordenação** — proíbe reordenamentos *através* do acesso `volatile`. Uma escrita `volatile` funciona como uma barreira: tudo o que veio antes dela em program order não pode ser movido para depois, e é publicado junto. Uma leitura `volatile` impede que leituras posteriores sejam movidas para antes. (Desde o JSR-133/Java 5, `volatile` tem essa semântica de *ordering*, não só visibilidade.)
- **NÃO dá atomicidade composta** — `volatile` torna cada leitura e cada escrita atômica individualmente (e atômica para `long`/`double`), mas *não* torna `i++` atômico, porque isso é read-modify-write.

O uso canônico é uma **flag de parada**:

```java
// hipotético: flag de parada correta com volatile
public class Worker implements Runnable {
    private volatile boolean stop = false;   // volatile é essencial

    public void pedirParada() {
        stop = true;   // visível imediatamente para a thread que roda run()
    }

    @Override
    public void run() {
        while (!stop) {   // sempre relê da memória; sem hoisting
            // trabalho
        }
    }
}
```

A regra mental: **use `volatile` quando uma thread escreve e outras leem, e a escrita não depende do valor anterior** (flags, referências publicadas, status). Quando a escrita *depende* do valor lido (contadores, acumuladores), `volatile` é insuficiente — use atômicos ou um lock.

### Final field semantics (publicação segura de imutáveis)

Campos `final` têm uma garantia que *nenhum outro campo* tem, descrita no JLS §17.5. No fim do construtor de um objeto ocorre uma ação de **freeze** dos seus campos `final`. A garantia formal:

> Uma thread que só consegue ver uma referência a um objeto **depois** que esse objeto foi completamente construído tem garantia de ver os valores **corretamente inicializados** dos campos `final` desse objeto — **mesmo sem sincronização**, e mesmo que a referência tenha sido passada por uma corrida de dados.

O exemplo da própria JLS §17.5 deixa o contraste explícito:

```java
// hipotético: baseado no exemplo da JLS §17.5
class Exemplo {
    final int x;   // final
    int y;         // NÃO-final
    static Exemplo f;

    Exemplo() {
        x = 3;
        y = 4;
    }

    static void writer() {
        f = new Exemplo();   // publica DEPOIS do construtor terminar
    }

    static void reader() {
        if (f != null) {
            int i = f.x;   // garantido ler 3   (campo final)
            int j = f.y;   // pode ler 0        (campo não-final, sem sync)
        }
    }
}
```

Como `writer()` escreve `f` *após* o construtor terminar, `f.x` (final) é garantidamente `3`. Já `f.y` não é `final`, então — sem nenhuma aresta de happens-before entre a escrita `y = 4` e a leitura — o `reader` pode ler `0`.

Essa garantia é exatamente o que permite que `String`, `Integer`, `BigDecimal` e outros imutáveis sejam **thread-safe sem sincronização**: seus campos internos são `final`, então qualquer thread que veja a referência vê o conteúdo correto. A condição é a publicação correta: **não vazar `this` antes do construtor terminar** (ver Armadilha 3).

### Double-checked locking correto (com `volatile`)

*Double-checked locking* (DCL) é o padrão de inicialização preguiçosa de um singleton que tenta evitar o custo do lock no caminho comum (objeto já criado). Ele **só é correto com o campo `volatile`** — antes do JSR-133 (Java 5), o idioma era considerado quebrado *por especificação*.

```java
// hipotético: DCL correto — note o volatile
public class Servico {
    private static volatile Servico instancia;   // volatile é CRÍTICO

    public static Servico getInstance() {
        Servico local = instancia;          // 1ª leitura (otimização: 1 leitura volatile)
        if (local == null) {                // primeira checagem (sem lock)
            synchronized (Servico.class) {
                local = instancia;
                if (local == null) {        // segunda checagem (com lock)
                    local = new Servico();
                    instancia = local;      // publicação via escrita volatile
                }
            }
        }
        return local;
    }
}
```

Por que `volatile` é indispensável: `instancia = new Servico()` não é uma operação única. Conceitualmente é (1) alocar memória, (2) rodar o construtor, (3) atribuir a referência ao campo. **Sem `volatile`**, o JMM permite reordenar (3) antes de (2) — outra thread veria `instancia != null` na primeira checagem (sem lock) e usaria um objeto **parcialmente construído**. A escrita `volatile` em `instancia` impede esse reordenamento e estabelece happens-before com a leitura volatile da primeira checagem.

A **alternativa moderna** é frequentemente preferível, pois não depende de DCL e é mais simples de auditar — usa a garantia de inicialização preguiçosa e thread-safe do *classloader* (idioma *initialization-on-demand holder*):

```java
// hipotético: idioma Holder — thread-safe sem volatile nem synchronized explícito
public class Servico {
    private Servico() {}

    private static class Holder {
        static final Servico INSTANCIA = new Servico();
    }

    public static Servico getInstance() {
        return Holder.INSTANCIA;   // classe Holder só é carregada/inicializada no 1º acesso
    }
}
```

A JVM garante que a inicialização de uma classe acontece sob um lock e é visível para todas as threads — sem precisar de `volatile` nem DCL.

### Safe vs unsafe publication

**Publicação** é tornar uma referência a um objeto visível para outras threads. **Publicação segura** (*safe publication*) garante que a thread que recebe a referência também vê o **estado do objeto** corretamente construído. Publicação **insegura** publica a referência sem uma aresta de happens-before que cubra os campos — a thread receptora pode ver a referência mas um objeto parcial.

Idiomas de **publicação segura** (cada um estabelece happens-before entre a construção e a leitura):

- Inicializar a referência num campo **`static`** durante a inicialização da classe (garantida pela JVM).
- Guardar a referência num campo **`volatile`** (ou `AtomicReference`).
- Guardar a referência num campo **`final`** de um objeto corretamente construído.
- Guardar a referência num campo protegido por **lock** (`synchronized`).
- Inserir a referência numa **concurrent collection** thread-safe (ex.: `ConcurrentHashMap`, `BlockingQueue`) — a coleção provê a sincronização interna.

Um objeto **efetivamente imutável** (estado nunca muda após a construção) é thread-safe contanto que seja publicado com *qualquer* mecanismo acima. Um objeto **mutável** precisa de publicação segura *e* de sincronização contínua em cada acesso posterior.

## Na prática

**Flag de parada com `volatile`** — uma thread sinaliza, outra observa. Escrita não depende do valor anterior, então `volatile` basta:

```java
// hipotético: sinalização de encerramento entre threads
public class Coletor implements Runnable {
    private volatile boolean encerrar = false;

    public void encerrar() {
        encerrar = true;   // publicação visível
    }

    @Override
    public void run() {
        while (!encerrar) {
            processarLote();
        }
        liberarRecursos();
    }

    private void processarLote() { /* ... */ }
    private void liberarRecursos() { /* ... */ }
}
```

**DCL correto de singleton** — caminho comum sem lock, primeira criação sob lock, campo `volatile`:

```java
// hipotético: cache de configuração inicializado preguiçosamente
public class Config {
    private static volatile Config instancia;
    private final Map<String, String> valores;   // final: publicação segura interna

    private Config() {
        this.valores = carregar();   // construção completa antes de publicar
    }

    public static Config getInstance() {
        Config local = instancia;
        if (local == null) {
            synchronized (Config.class) {
                local = instancia;
                if (local == null) {
                    instancia = local = new Config();
                }
            }
        }
        return local;
    }

    private Map<String, String> carregar() { /* ... */ return Map.of(); }
}
```

**Imutável publicado com segurança via `final`** — uma vez construído, é livre de corridas; pode ser passado entre threads sem sincronização:

```java
// hipotético: ponto imutável — campos final dão publicação segura
public final class Ponto {
    private final int x;
    private final int y;

    public Ponto(int x, int y) {
        this.x = x;
        this.y = y;
        // nenhum vazamento de 'this' aqui: construtor termina, freeze dos finais ocorre
    }

    public int getX() { return x; }
    public int getY() { return y; }
}

// Qualquer thread que receba a referência (mesmo via campo não-volatile)
// vê x e y corretos — garantia de final fields da JLS §17.5.
```

> [!warning] Bugs de visibilidade são não-determinísticos
> O output de um programa com corrida de visibilidade **não é reproduzível de forma confiável**. Um loop sem `volatile` pode terminar em uma execução e travar na seguinte; um objeto mal-publicado pode ser lido corretamente milhões de vezes e então, sob outro JIT/CPU/carga, ser lido parcial. **Ausência de falha em teste não prova ausência de corrida.** A correção só pode ser estabelecida por raciocínio com happens-before, não por execução repetida.

## Armadilhas

### (1) Double-checked locking sem `volatile`

**O problema:** o idioma DCL escrito com o campo de instância **não-`volatile`** está quebrado por especificação. `instancia = new Servico()` é, em baixo nível, "alocar + construir + atribuir referência". Sem `volatile`, o JMM permite que a atribuição da referência seja reordenada para *antes* do término do construtor. Outra thread executando a primeira checagem (fora do lock) pode ver `instancia != null` e retornar um objeto **parcialmente construído** — campos ainda em valor-padrão.

```java
// hipotético: DCL QUEBRADO — falta volatile
public class Servico {
    private static Servico instancia;   // ❌ deveria ser volatile

    public static Servico getInstance() {
        if (instancia == null) {                 // 1ª checagem (sem lock)
            synchronized (Servico.class) {
                if (instancia == null) {
                    instancia = new Servico();   // ❌ referência pode ficar visível
                }                                //    antes do construtor terminar
            }
        }
        return instancia;   // outra thread pode receber objeto meio-construído
    }
}
```

**Fix:** marque o campo como `volatile` (a escrita volatile impede o reordenamento e estabelece happens-before com a leitura volatile da primeira checagem) — ou, melhor, troque pelo idioma *Holder* que dispensa DCL:

```java
// hipotético: fix mínimo — volatile no campo
private static volatile Servico instancia;
// ...restante do DCL como na seção "Como funciona"
```

```java
// hipotético: fix preferível — idioma Holder, sem volatile nem DCL
public class Servico {
    private Servico() {}
    private static class Holder {
        static final Servico INSTANCIA = new Servico();
    }
    public static Servico getInstance() {
        return Holder.INSTANCIA;   // inicialização de classe é thread-safe pela JVM
    }
}
```

---

### (2) Achar que `volatile` torna `i++` atômico

**O problema:** `volatile` garante que cada *leitura* e cada *escrita* da variável é atômica e visível — mas `i++` (e `i += n`, `i = i * 2`, etc.) é um **read-modify-write**: três operações distintas (ler, somar, escrever). Entre a leitura e a escrita, outra thread pode ler o mesmo valor, e ambas escrevem o mesmo resultado — um incremento é **perdido**. O output é não-determinístico: a contagem final fica *menor* que o esperado, de forma imprevisível.

```java
// hipotético: contador QUEBRADO — volatile não dá atomicidade composta
public class Contador {
    private volatile int n = 0;     // ❌ volatile não conserta i++

    public void incrementar() {
        n++;   // read-modify-write: leitura e escrita separadas → corrida
    }
}
// Com N threads chamando incrementar() M vezes, n final < N*M (não-determinístico)
```

**Fix:** use um tipo atômico (lock-free, CAS) ou sincronize a operação composta inteira:

```java
// hipotético: fix com atômico (preferível para um único contador)
public class Contador {
    private final AtomicInteger n = new AtomicInteger();

    public void incrementar() {
        n.incrementAndGet();   // atômico: read-modify-write num único passo (CAS)
    }
    public int valor() { return n.get(); }
}
```

```java
// hipotético: fix com synchronized (quando há invariante sobre vários campos)
public class Contador {
    private int n = 0;

    public synchronized void incrementar() {
        n++;   // a seção crítica torna o read-modify-write atômico
    }
    public synchronized int valor() { return n; }
}
```

> Use `volatile` quando a escrita *não* depende do valor lido (flag, referência publicada). Use atômico/lock quando ela *depende* (contador, acumulador).

---

### (3) Vazar `this` no construtor (escape) / ler campo não-final sem sincronização

**O problema (escape de `this`):** a garantia de `final` fields exige que o objeto seja **completamente construído** antes de ser visível para outra thread. Se o construtor publica `this` antes de terminar — registrando um listener, iniciando uma thread, ou guardando `this` num campo estático/coleção compartilhada — outra thread pode acessar o objeto enquanto seus campos `final` ainda estão em valor-padrão. A garantia da JLS §17.5 é **anulada**.

```java
// hipotético: ESCAPE de this no construtor — quebra a garantia de final
public class Servico {
    private final int config;

    public Servico(Registrador reg) {
        reg.registrar(this);   // ❌ 'this' escapa ANTES do construtor terminar
        this.config = carregar();   // outra thread pode ler config==0 aqui
    }

    private int carregar() { /* ... */ return 42; }
}
```

**O problema (leitura de campo não-final sem sync):** mesmo com publicação correta, apenas campos `final` têm a garantia especial. Ler um campo **não-`final`** de um objeto publicado por uma corrida pode devolver o valor-padrão (como `f.y` no exemplo da JLS).

**Fix (escape):** nunca publique `this` no construtor. Construa o objeto totalmente e registre-o depois, num método de fábrica:

```java
// hipotético: fix — fábrica registra DEPOIS da construção completa
public class Servico {
    private final int config;

    private Servico() {
        this.config = carregar();   // construção completa primeiro
    }

    public static Servico criar(Registrador reg) {
        Servico s = new Servico();   // construtor termina (freeze dos finais)
        reg.registrar(s);            // publicação segura, objeto já completo
        return s;
    }

    private int carregar() { /* ... */ return 42; }
}
```

**Fix (campo não-final):** se o estado precisa ser lido por outras threads, ou torne-o `final` (imutável), ou publique-o e leia-o sob a mesma aresta de happens-before — campo `volatile`, `synchronized`, ou `AtomicReference`:

```java
// hipotético: fix — campo final dá publicação segura; sem sync no leitor
public final class Servico {
    private final int config;   // final: leitor vê valor correto sem sync

    public Servico() { this.config = carregar(); }
    public int getConfig() { return config; }
    private int carregar() { /* ... */ return 42; }
}
```

## Em entrevista

### Frase pronta (inglês)

> "The Java Memory Model defines what a thread is *allowed to observe* when it reads a variable written by another thread. It exists because the JIT, the CPU, and store buffers all reorder operations and keep values in local caches — single-threaded code never notices, but across threads it breaks code that looks correct. The model's core is the *happens-before* relation: if A happens-before B, then A's memory effects are guaranteed visible to B. The edges that create happens-before are deliberately few — program order within a thread, unlock/lock on the same monitor, write/read on the same `volatile`, `Thread.start`, `Thread.join`, and transitivity."
>
> "`volatile` is the lightest tool: it gives visibility and ordering — every read goes to memory, and writes can't be reordered across it — but it does *not* give compound atomicity, so `i++` is still a racy read-modify-write and needs an `AtomicInteger` or a lock instead. `final` fields get a stronger guarantee: if an object is *safely published* — meaning `this` never escapes during construction — any thread that sees the reference sees the correctly initialized `final` fields without synchronization, which is exactly why `String` and `Integer` are thread-safe."
>
> "A classic pitfall is double-checked locking: it's only correct when the field is `volatile`, otherwise another thread can see the reference assigned before the constructor finishes and use a partially constructed object. And crucially, visibility bugs are non-deterministic — they can pass millions of runs and fail under a different CPU or JIT, so you can't test your way to correctness; you have to reason with happens-before."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| modelo de memória | memory model |
| acontece-antes / relação happens-before | happens-before relation |
| visibilidade | visibility |
| reordenação (de instruções) | (instruction) reordering |
| barreira de memória | memory barrier / memory fence |
| buffer de escrita | store buffer |
| publicação segura | safe publication |
| objeto parcialmente construído | partially constructed object |
| vazamento de `this` (no construtor) | `this` escape (during construction) |
| leitura-modificação-escrita | read-modify-write |
| campo final / congelamento (freeze) | final field / freeze action |
| trava dupla checada | double-checked locking |
| ordem de programa | program order |
| coerência de cache | cache coherence |

## Veja também

- [[03 - Exclusão mútua com synchronized]]
- [[04 - As armadilhas - race, deadlock e companhia]]
- [[05 - Locks explícitos]]
- [[06 - Atômicos e operações lock-free]]
- [[12 - Virtual Threads e Project Loom]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|MOC do galho]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[Java Concurrency]]
- [[Java Fundamentals]]
- [[03-Dominios/Java/Dicionário de Java#Happens-before|happens-before]]
- [[03-Dominios/Java/Dicionário de Java#Volatile|volatile]]
- [[03-Dominios/Java/Dicionário de Java#Safe publication (publicação segura)|safe publication]]

## Referências

- [JLS §17.4 — Memory Model (Java SE 21)](https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html#jls-17.4) — define happens-before, *synchronizes-with* e a ordem de sincronização.
- [JLS §17.5 — `final` Field Semantics (Java SE 21)](https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html#jls-17.5) — freeze e garantia de publicação segura de imutáveis.
- [JLS §17.7 — Non-atomic Treatment of `double` and `long`](https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html#jls-17.7) — atomicidade de 64 bits e `volatile`.
- [JSR-133 (Java Memory Model and Thread Specification)](https://jcp.org/en/jsr/detail?id=133) — a revisão do JMM (Java 5) que corrigiu `volatile` e DCL.
- *Java Concurrency in Practice* — Brian Goetz et al., cap. 16 (The Java Memory Model) e cap. 3 (Sharing Objects: publicação segura).
