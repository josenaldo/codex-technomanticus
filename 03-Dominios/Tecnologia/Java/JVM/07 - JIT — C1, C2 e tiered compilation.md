---
title: "JIT — C1, C2 e tiered compilation"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - jvm
  - adepto
  - jit
aliases:
  - "JIT"
  - "Tiered compilation"
  - "C1 C2"
  - "Escape analysis"
---

# JIT — C1, C2 e tiered compilation

> [!abstract] TL;DR
> O JIT (just-in-time compiler) compila bytecode para código nativo **em runtime**, guiado por **profiling do comportamento real** do programa — informação que nenhum compilador ahead-of-time tem. O HotSpot combina três motores: o **interpretador** (executa imediatamente, coleta perfil), o **C1** (compila rápido, otimiza pouco, instrumenta profiling) e o **C2** (compila devagar, otimiza agressivamente) — e a **tiered compilation**, default desde sempre nos JDKs modernos, orquestra a promoção entre eles. Duas consequências práticas definem o tema: **warmup** (a aplicação só atinge velocidade de cruzeiro depois que o caminho quente passou pelo C2 — por isso benchmark ingênuo mente) e **deoptimization** (o C2 **especula** com base no perfil; quando a especulação falha, o código nativo é descartado e a execução volta pro interpretador — é a rede de segurança que torna a especulação viável).

## O que é

Java é compilado duas vezes. O `javac` faz a primeira: fonte → bytecode, sem nenhuma otimização relevante ([[04 - Bytecode por dentro — anatomia e javap]]). A segunda compilação — bytecode → código de máquina nativo — acontece **dentro da JVM, enquanto o programa roda**. Esse é o trabalho do JIT.

Três estratégias de execução existem nesse espectro:

- **Interpretação pura**: a JVM lê bytecode instrução por instrução e executa. Começa instantaneamente, não gasta nada compilando — mas cada instrução paga o custo do loop de interpretação. Ordens de magnitude mais lento que nativo.
- **Compilação ahead-of-time (AOT)**: tudo vira nativo antes de rodar (caminho do GraalVM Native Image). Startup instantâneo, mas o compilador decide às cegas — sem saber quais branches são tomados, quais tipos aparecem de verdade, quais métodos são quentes.
- **Compilação just-in-time**: a JVM **observa o programa rodando** e compila para nativo apenas o que vale a pena, usando o perfil observado para otimizar. Paga warmup, mas o código final pode ser **melhor** que o de um AOT — porque otimiza para o comportamento que de fato aconteceu, inclusive especulando sobre o que "sempre acontece".

O HotSpot carrega **dois compiladores JIT**, herança da época em que existiam duas VMs distintas:

- **C1 (client compiler)**: compila **rápido** e produz código **razoável**. Faz as otimizações baratas (inlining básico, eliminação de código trivialmente morto) e — papel central no design atual — emite código **instrumentado**, que coleta dados de profiling sobre si mesmo enquanto roda.
- **C2 (server compiler)**: compila **devagar** e produz código **excelente**. É onde moram as otimizações pesadas: inlining profundo, escape analysis, loop unrolling, especulação baseada em perfil.

Por que dois? Porque os requisitos são contraditórios: no startup você quer sair do interpretador o quanto antes (latência de compilação importa); no estado estacionário você quer o melhor código possível (qualidade importa, latência de compilação não). Um compilador só teria que escolher um lado. Dois compiladores + um interpretador permitem ter os dois — e é exatamente isso que a tiered compilation entrega.

Os nomes "client" e "server" são fósseis úteis: vêm da era em que se escolhia a VM na linha de comando (`-client` para desktop, startup rápido; `-server` para servidores, pico de performance). Desde a introdução da tiered compilation (Java 7) e sua consolidação como default, a distinção sumiu — toda JVM HotSpot moderna usa **os dois compiladores em cooperação**, e a documentação da Oracle descreve a tiered compilation justamente como "trazer a velocidade de startup da client VM para a server VM".

## Por que importa

**"Por que a aplicação ficou rápida depois de 10 minutos?"** — porque os caminhos quentes terminaram de subir a escada interpretador → C1 → C2. Antes disso, parte do código roda interpretado ou em código C1, ambos mais lentos que o produto final do C2. Esse período é o **warmup**, e ele explica fenômenos que parecem misteriosos para quem não conhece o JIT: os primeiros requests de um deploy são os mais lentos; a latência cai em degraus nos primeiros minutos; dois pods idênticos têm p99 diferente porque um acabou de subir.

**Benchmark ingênuo mente — sempre.** Medir um trecho de código com `System.nanoTime()` num loop mistura tempo de interpretador, tempo de compilação JIT rodando em background e código C1/C2 na mesma média — e, pior, o C2 pode **eliminar o código inteiro** se perceber que o resultado não é usado (dead code elimination), produzindo o famoso benchmark que "prova" que uma operação custa 0ns. Quem apresenta números de microbenchmark caseiro numa discussão técnica está, na prática, medindo o próprio erro de metodologia. A resposta é JMH — detalhes na seção Na prática, abaixo.

**Deoptimization é pergunta clássica de entrevista senior.** "O que acontece quando o JIT compila um método com uma suposição que depois se revela falsa?" separa quem decorou "JIT compila código quente" de quem entende o modelo: o C2 **especula** (esse `if` nunca foi tomado, esse call site só viu um tipo), gera código otimizado para a especulação com um *guard* de verificação, e quando o guard falha o código é invalidado (*made not entrant*), a execução **volta pro interpretador** e o método é eventualmente recompilado com o perfil corrigido. Sem deoptimization não haveria especulação; sem especulação, o JIT perderia suas otimizações mais lucrativas.

## Como funciona

### Tiered compilation — o fluxo

A documentação da Oracle confirma: **tiered compilation é o modo default** (a flag `-XX:-TieredCompilation` existe justamente para *desligar* o que vem ligado). O fluxo, do método recém-carregado ao código de pico:

1. **Interpretador**: todo método começa interpretado. O interpretador executa e, de quebra, **conta**: invocações do método e iterações de loops (*back edges*). Esses contadores são o gatilho de tudo.
2. **Promoção para C1**: quando os contadores de invocação/loop cruzam um limiar, o método é enfileirado para compilação. O C1 gera rapidamente uma versão nativa **com instrumentação de profiling** — o método agora roda muito mais rápido que interpretado *e continua coletando perfil sobre si mesmo* (quais branches são tomados, quais tipos aparecem em cada call site).
3. **Promoção para C2**: o método continua quente e o perfil amadurece. O C2 então recompila usando todo o histórico coletado — e é aqui que entram inlining agressivo, escape analysis e especulação. O resultado substitui a versão C1.
4. **Métodos mornos param no meio**: um método chamado algumas centenas de vezes pode viver para sempre na versão C1 — o C2 só é acionado se a frequência justificar o custo da compilação cara. A maioria absoluta dos métodos de uma aplicação nem sai do interpretador; a regra 80/20 é severa aqui.

Detalhe que cai em entrevista: a compilação acontece em **threads de compilação em background** — a aplicação não para para compilar; ela continua rodando a versão atual (interpretada ou C1) até a nova ficar pronta. E loops longos não precisam esperar o método ser chamado de novo: a JVM consegue trocar a execução para código compilado **no meio do loop** (*on-stack replacement*, o `%` no output do `PrintCompilation`).

O ganho do desenho, nas palavras da Oracle: o código C1 é "substancialmente mais rápido que o interpretador" durante a fase de profiling, então o programa **já roda rápido enquanto o perfil é coletado** — e como profilar ficou barato, dá para profilar por mais tempo, o que rende perfil melhor e, portanto, **código C2 melhor**. Tiered compilation melhora o startup *e* o pico.

A tabela mental dos três motores:

| Motor | Começa a executar | Velocidade do código | Custo de compilar | Papel no fluxo |
|-------|-------------------|----------------------|--------------------|----------------|
| **Interpretador** | Imediatamente | Lenta (ordens de magnitude vs nativo) | Zero | Executa tudo no início; coleta contadores de invocação/loop; destino do fallback de deoptimization |
| **C1 (client)** | Rápido de produzir | Boa | Baixo | Tira o método quente do interpretador cedo; emite código **instrumentado** que continua coletando perfil |
| **C2 (server)** | Lento de produzir | Excelente (pico) | Alto | Recompila o que continua quente, usando o perfil maduro para otimizações agressivas e especulativas |

Duas leituras úteis da tabela: o interpretador nunca é "desperdício" — ele é o estágio de coleta de dados e a rede de segurança; e o C1 não é um "C2 piorado" — é a peça que torna o profiling barato o suficiente para o C2 receber matéria-prima de qualidade.

### As otimizações do C2

**Inlining — a otimização-mãe.** Copiar o corpo do método chamado para dentro do chamador. O ganho direto (eliminar o overhead da chamada) é o menor dos benefícios: o ganho real é que o inlining **funde os contextos** — depois de inlinar, o C2 enxerga chamador e chamado como um bloco único e pode aplicar todas as outras otimizações através da fronteira que antes era opaca. Constant folding atravessa o que era uma chamada; escape analysis enxerga o objeto criado num método e consumido no outro; dead code elimination remove ramos que só são mortos quando os dois contextos se juntam. Por isso a literatura chama inlining de *the mother of all optimizations*: ele não otimiza — ele **habilita**. O profiling alimenta decisões de inlining inclusive para chamadas virtuais: se um call site só viu um tipo concreto (*monomorphic call site*), o C2 inlina a implementação direto, com um guard de tipo como seguro.

O inlining tem limites de orçamento: métodos grandes demais (em bytecode) não são inlinados, e cadeias profundas estouram o budget de cada compilação. A implicação prática inverte uma intuição comum: **métodos pequenos e focados não são só estética — são mais amigáveis ao JIT**. O mega-método de 400 linhas é opaco para inlining; a mesma lógica decomposta em métodos pequenos e quentes vira um bloco único otimizado no código final, sem custo de chamada. Em Java moderno, "extrair método" raramente custa performance — frequentemente ganha.

**Escape analysis — o objeto que não escapa pode nem existir.** O C2 analisa o escopo de uso de cada `new`: se o objeto **não escapa** do método (nunca é retornado, guardado num campo, passado para fora), a alocação no heap pode ser eliminada por completo via **scalar replacement** — os campos do objeto viram variáveis locais/registradores, e o objeto, como entidade, deixa de existir. A documentação da Oracle (Java 21) confirma escape analysis habilitada por default e é precisa num detalhe que derruba candidato: o HotSpot **não** faz alocação na pilha (*stack allocation*) — ele faz scalar replacement, que é mais radical: não move a alocação, **elimina** a alocação. É esse mecanismo que torna barato o custo aparente de abstrações temporárias — iteradores de loop, objetos de janela, wrappers de boxing que nascem e morrem dentro de um método quente podem custar zero alocação no código final. O custo de alocação e boxing que essa análise elimina é exatamente o tema de [[03-Dominios/Tecnologia/Java/Collections e Streams/09 - Streams primitivos|Streams primitivos]] — com a ressalva de que escape analysis é **best effort**: ela falha em métodos grandes demais ou fluxos complexos, então não substitui escolher a estrutura certa.

**Lock elision.** Subproduto direto da escape analysis, documentado pela Oracle: se um objeto não escapa da thread, **nenhuma outra thread pode vê-lo** — logo, `synchronized` sobre ele é teatro, e o C2 remove o lock do código gerado. O exemplo clássico da própria documentação: `StringBuffer` ou `Vector` usados como variáveis locais têm seus locks eliminados. Consequência importante: "synchronized é lento" sem qualificar o cenário é afirmação datada — em código sem contenção real, o lock pode literalmente não existir no nativo. O modelo completo de locks e contenção é assunto de [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]].

**Dead code elimination.** Código cujo resultado comprovadamente não afeta nada observável é removido. Ótimo para produção (computação inútil some), fatal para microbenchmark caseiro: o loop que calcula e descarta um valor é exatamente o padrão que o DCE devora — sobra um loop vazio, que também é removido, e o "benchmark" mede o custo de nada.

**Loop unrolling.** O C2 replica o corpo de loops quentes várias vezes por iteração, reduzindo o overhead de incremento/teste/salto e abrindo espaço para vetorização e melhor uso do pipeline da CPU. Combinado com o profiling de back edges, é parte do motivo de loops numéricos quentes em Java rodarem em velocidade comparável a código nativo escrito à mão.

### Deoptimization — a rede de segurança

O C2 é um compilador **especulativo**: ele aposta que o futuro repetirá o perfil observado. "Esse branch nunca foi tomado em 100 mil execuções → compilo só o caminho quente e deixo um guard no frio." "Esse call site só viu `ArrayList` → inlino `ArrayList.get` direto, com um teste de classe como seguro."

Gatilhos típicos de falha da aposta:

- **Branch "impossível" acontece**: o caminho que nunca tinha sido tomado em centenas de milhares de execuções finalmente executa — entrada nova, feature flag virada, caso de borda raro.
- **Tipo novo num call site monomórfico**: o site que só via `ArrayList` recebe um `LinkedList`; o guard de classe falha.
- **Carga de classe quebra hipótese de hierarquia**: o C2 tinha provado que um método virtual só tinha uma implementação carregada e o inlinou sem guard caro; uma subclasse nova carregada em runtime invalida a prova — e a JVM deoptimiza o código dependente dela.

Quando isso acontece, o guard (ou o mecanismo de invalidação por carga de classe) dispara a **deoptimization**:

1. O código nativo especulativo é **invalidado** (marcado *made not entrant*: chamadas novas não entram mais nele; as em andamento terminam ou são transferidas).
2. A execução do método **volta para o interpretador**, reconstruindo o estado (variáveis locais, pilha de operandos) a partir dos metadados que o C2 gravou para esse fim.
3. O perfil é atualizado com o fato novo, os contadores trabalham de novo, e o método é **recompilado** — agora sem a especulação que falhou (ou com uma versão mais conservadora dela).

Por que especular compensa, se pode dar errado? Aritmética de frequências: a especulação acelera **todas** as execuções do caminho comum; a deoptimization custa caro **uma vez** por falha. Se a hipótese vale 99,99% do tempo, o saldo é enorme. O caso ruim é a hipótese instável — especula, deoptimiza, recompila, o perfil muda, especula de novo — e aí o sintoma em produção é performance serrilhada em código que "não mudou". Deoptimization também é rotina não-excepcional: acontece em massa quando classes novas são carregadas (lazy loading de um framework no primeiro request de um endpoint, por exemplo).

### Warmup — por que os primeiros N requests são lentos

Juntando as peças: depois do startup, todo caminho de código novo começa interpretado, sobe para C1 quando esquenta e só chega ao C2 com perfil maduro. Durante essa subida, a aplicação funciona — mas mais lenta que seu estado final. Efeitos práticos:

- **Deploy e p99**: logo após um deploy, a latência sobe — não porque "o servidor está frio" em sentido vago, mas porque os caminhos quentes regrediram para interpretador/C1. Rolling deploys agressivos mantêm uma fração da frota permanentemente em warmup.
- **Serverless e instâncias efêmeras**: uma função que vive 30 segundos pode **nunca** sair do C1 — paga o custo do modelo JIT (compilação em runtime) sem colher o benefício (código de pico). É por isso que o ecossistema de cold-start gravita para AOT (GraalVM Native Image) ou para mecanismos de checkpoint/restauração e cache de código que "engarrafam" o warmup de uma execução para as seguintes (linha do projeto Leyden no OpenJDK).
- **Load test honesto** descarta os primeiros minutos: medir warmup junto com estado estacionário produz números que não representam nenhum dos dois.

Mitigações usuais, em ordem crescente de esforço:

- **Aceitar e dimensionar**: readiness probe que só libera tráfego depois de um período de aquecimento; rollout gradual para diluir a frota fria.
- **Aquecer ativamente**: disparar tráfego sintético contra os endpoints quentes antes de entrar no balanceador — aquece exatamente os caminhos que importam (aquecer "qualquer coisa" não compila os métodos certos).
- **Mudar de modelo**: para cold-start dominante (serverless), AOT via GraalVM Native Image troca o pico do C2 por startup instantâneo — um trade-off de arquitetura, não uma flag.

### Code cache — onde o nativo mora

Todo código que o JIT gera vive numa região de memória **nativa** (fora do heap Java) chamada **code cache**. Pontos verificados na documentação da Oracle (Java 21):

- Tamanho máximo controlado por `-XX:ReservedCodeCacheSize` — **default de 240 MB** com tiered compilation (48 MB se tiered for desligada), com limite de 2 GB.
- Desde o Java 9, o code cache é **segmentado** (*segmented code cache*): segmentos separados por tipo de código (código profiled do C1, código non-profiled do C2, código interno da JVM), o que reduz fragmentação e melhora o tempo de varredura.
- **Se o code cache enche, a compilação para.** A JVM emite o aviso (`CodeCache is full. Compiler has been disabled.`) e segue executando — mas métodos novos que esquentarem ficam presos no interpretador/nível atual para sempre. A aplicação não quebra; ela **degrada silenciosamente**, e o sintoma (lentidão progressiva e teimosa) raramente aponta para a causa. Aplicações grandes, uso pesado de geração dinâmica de classes (proxies, lambdas em massa) e deoptimization frequente são os consumidores típicos.

## Na prática

### Vendo o JIT trabalhar: `-XX:+PrintCompilation`

A flag (documentada na man page do `java` 21) imprime uma linha por método compilado:

```text
$ java -XX:+PrintCompilation -jar app.jar
# saída ilustrativa, abreviada — colunas:
# [tempo desde o início, ms] [id da compilação] [flags] [nível] [método (tamanho em bytecode)]

    142    1       3       java.lang.String::hashCode (49 bytes)
    145    2       3       java.lang.String::equals (65 bytes)
    151    3     n 0       java.lang.System::arraycopy (native)   (static)
    310   87 %     3       com.example.OrderService::processAll @ 12 (89 bytes)
   1796   95       3       com.example.Order::total (38 bytes)
   1843  412       4       com.example.Order::total (38 bytes)
   1844   95       3       com.example.Order::total (38 bytes)   made not entrant
   9120  412       4       com.example.Order::total (38 bytes)   made not entrant
```

Como ler:

- **Coluna de nível**: o tier de compilação. Os níveis baixos são do C1 (com instrumentação de profiling); o nível mais alto é o **C2**. A história de `Order::total` acima é a escada inteira: compilado pelo C1, depois recompilado pelo C2 — e a versão C1 marcada `made not entrant` (substituída).
- **`%`**: *on-stack replacement* — a compilação foi disparada por um loop quente, e o código trocado no meio da execução (o `@ 12` é o índice do bytecode do back edge).
- **`n`**: wrapper para método nativo; **`s`** indicaria método `synchronized`; **`!`** método com handler de exceção.
- **`made not entrant` num código nível-C2** (última linha) é a assinatura de uma **deoptimization**: uma especulação falhou e o código de pico foi invalidado. Algumas ocorrências são vida normal; uma metralhadora delas no mesmo método é sintoma de especulação instável.

Para investigar decisões de inlining, existe `-XX:+PrintInlining` (exige `-XX:+UnlockDiagnosticVMOptions`).

### Flags de diagnóstico do JIT (man page Java 21)

```bash
# Ver cada método sendo compilado (uma linha por compilação)
java -XX:+PrintCompilation -jar app.jar

# Ver as decisões de inlining (diagnóstica — exige unlock)
java -XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining -jar app.jar

# Aumentar o code cache (default 240 MB com tiered; limite 2 GB)
java -XX:ReservedCodeCacheSize=512m -jar app-grande.jar

# Desligar tiered compilation (vem HABILITADA por default)
# — só interpretador + C2; raramente justificável fora de diagnóstico
java -XX:-TieredCompilation -jar app.jar

# Modos de teste/diagnóstico — NUNCA em produção:
java -Xint  -jar app.jar    # tudo interpretado; JIT desligado
java -Xcomp -jar app.jar    # compila tudo no 1º uso; "testing mode" segundo a man page
```

Regra de leitura para qualquer flag de JIT achada num `JAVA_OPTS` herdado: as de observação (`PrintCompilation`, `PrintInlining`) são inofensivas além do ruído de log; as que mudam o comportamento (`-Xint`, `-Xcomp`, `-XX:-TieredCompilation`) precisam de justificativa escrita — e quase nunca têm.

### Por que medir com JMH

Tudo que esta nota descreveu — warmup, DCE, inlining dependente de perfil — conspira contra medição manual. O caso clássico do benchmark que mente:

```java
// hipotético: o microbenchmark caseiro que "prova" custo zero
long start = System.nanoTime();
for (int i = 0; i < 1_000_000; i++) {
    Order order = new Order(100, "BRL");
    order.total();                        // resultado descartado
}
long elapsed = System.nanoTime() - start;
// O C2 vê que nada do loop é observável → dead code elimination
// remove o corpo, depois o loop. "Resultado": ~0ns por iteração.
// Mediu-se o custo de coisa nenhuma.
```

O **JMH** (Java Microbenchmark Harness, projeto do próprio OpenJDK — "a Java harness for building, running, and analysing nano/micro/milli/macro benchmarks", na definição do README) existe porque escrever benchmark correto na JVM é um problema de especialista. Ele resolve sistematicamente o que o loop caseiro ignora: roda **iterações de warmup** descartadas antes de medir, fazendo a medição capturar código C2 estabilizado; isola execuções em JVMs separadas (*forks*) para neutralizar profile pollution; e derrota o DCE exigindo que todo valor computado seja **consumido** — retornando-o do método de benchmark ou entregando-o a um `Blackhole`, o objeto do JMH cujo único papel é consumir valores de um jeito que o JIT não consegue provar inútil:

```java
// hipotético: o mesmo benchmark, do jeito certo
@Benchmark
public long total() {
    Order order = new Order(100, "BRL");
    return order.total();                 // valor retornado → JMH consome → sem DCE
}

@Benchmark
public void totalComBlackhole(Blackhole bh) {
    Order order = new Order(100, "BRL");
    bh.consume(order.total());            // alternativa explícita p/ múltiplos valores
}
```

Regra de bolso para discussão técnica: número de performance de trecho de código Java sem JMH (ou metodologia equivalente) não é evidência — é anedota.

Duas observações de quem opera isso:

- **JIT quase nunca é o que você tuna — é o que você entende.** Diferente do GC ([[06 - Os coletores do HotSpot]]), onde escolher coletor e flags é decisão real, o JIT default raramente pede intervenção. O valor do conhecimento está em **diagnóstico**: explicar o warmup pós-deploy, reconhecer deoptimization serrilhando a latência, identificar code cache cheio, e não cair em benchmark mentiroso.
- **O JIT é o motivo de "performance de Java" ser uma pergunta sem resposta curta.** O mesmo código-fonte tem performances diferentes conforme o perfil, a fase de warmup e as especulações ativas. Qualquer afirmação séria de custo precisa dizer **em que estado da JVM** foi medida.

## Armadilhas

### (1) Microbenchmark caseiro sem JMH — o DCE engole o código

**O problema:** o loop com `System.nanoTime()` parece inofensivo, mas comete os três pecados capitais ao mesmo tempo: mede warmup junto com pico, mede uma única JVM com um único perfil, e — o pior — computa valores que descarta. O C2 aplica dead code elimination, o corpo do loop evapora e o resultado é um número minúsculo que não mede nada. Esses números depois viram base de decisão ("provei que X é mais rápido que Y") e a decisão herda o erro.

**Fix:** JMH, sempre. Estruture o benchmark para que todo valor computado seja retornado ou consumido via `Blackhole`, use os defaults de warmup/forks do harness e desconfie de qualquer resultado bom demais (nanossegundos suspeitos de zero = DCE venceu de novo). O README do JMH recomenda inclusive rodar via JAR standalone, não pela IDE — ambiente não controlado contamina a medição.

---

### (2) Medir durante o warmup — números do interpretador travestidos de veredito

**O problema:** rodar o load test (ou o benchmark) imediatamente após o startup e tratar os primeiros segundos como representativos. Os números capturados misturam interpretador, código C1 e threads de compilação competindo por CPU — um regime transitório que não voltará a existir. Conclusões típicas do erro: "a JVM é lenta", "a rota X é 5x mais lenta que a Y" (X só estava mais fria), comparações AOT vs JIT onde o JIT nunca chegou ao estado que o diferencia.

**Fix:** separe warmup de medição **explicitamente**. Em JMH isso é automático (`@Warmup` antes de `@Measurement`); em load test, descarte os primeiros minutos e confirme a estabilização observando a latência parar de cair (ou `-XX:+PrintCompilation` silenciar nos caminhos quentes). Se o seu caso real É o warmup — serverless, jobs curtos — então meça o warmup de propósito, com essa moldura, e considere as soluções da categoria (AOT, checkpoint/cache de código).

---

### (3) Concluir que `synchronized` "é lento" sem considerar o JIT

**O problema:** benchmark de método `synchronized` sem contenção, em objeto que não escapa, "provando" que o lock custa caro — ou o inverso, concluindo que custa zero e extrapolando para produção. Os dois erram pelo mesmo motivo: o resultado depende do que o C2 fez, não do que o código-fonte diz. Com escape analysis, o lock de um objeto confinado é **elidido** — o código medido pode não conter lock nenhum. Já no sistema real, o mesmo `synchronized` sobre um objeto compartilhado e disputado tem custo dominado por **contenção** — fenômeno que o microbenchmark de thread única é estruturalmente incapaz de exibir.

**Fix:** meça o cenário real: o objeto realmente escapa? Há contenção de verdade, com quantas threads? JMH tem suporte a benchmarks multi-thread (`@Threads`, grupos) exatamente para isso. E na decisão de design, o custo de `synchronized` raramente é o argumento decisivo — o modelo de concorrência correto vem antes ([[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]).

---

### (4) `-Xint` ou `-Xcomp` em produção — quebrar o equilíbrio tiered

**O problema:** as duas flags desligam o desenho que esta nota inteira descreve. `-Xint` roda **tudo interpretado** — a man page é explícita: os benefícios do JIT simplesmente não existem nesse modo; a aplicação fica ordens de magnitude mais lenta, para sempre. `-Xcomp` força compilação no primeiro uso de cada método — e a man page a classifica como **modo de teste** que "não deve ser usado em ambientes de produção": compilar tudo de cara significa compilar **sem perfil**, ou seja, sem a matéria-prima das melhores otimizações do C2, além de inflar brutalmente o startup. Essas flags aparecem em produção por herança de algum debugging antigo enterrado num `JAVA_OPTS`.

**Fix:** em produção, o equilíbrio tiered default é a resposta correta na esmagadora maioria dos casos — `-Xint`/`-Xcomp` são ferramentas de diagnóstico (isolar suspeita de bug de compilador, exercitar o JIT em teste). Audite os `JAVA_OPTS` herdados; se houver flag de JIT sem justificativa documentada e medida, remova.

---

### (5) Ignorar o code cache até ele encher

**O problema:** aplicação grande, muitos proxies/lambdas gerados dinamicamente, e em algum momento o log diz `CodeCache is full. Compiler has been disabled.` — quase sempre ninguém vê, porque a aplicação **não quebra**: ela só para de compilar. Código novo que esquentar depois disso fica preso no interpretador/C1 indefinidamente. O sintoma observável é lentidão que se instala e não regride, dias depois da causa.

**Fix:** monitore a ocupação do code cache como métrica de produção (exposta via JMX/agentes de APM) e trate o aviso de code cache cheio como alerta, não ruído. Se a aplicação legitimamente precisa de mais espaço, aumente `-XX:ReservedCodeCacheSize` acima dos 240 MB default (limite de 2 GB). Se o consumo cresce sem teto, o problema é outro — geração dinâmica de classes descontrolada ou deoptimization em loop — e aumentar o cache só adia o sintoma.

## Em entrevista

### Frase pronta (inglês)

> "HotSpot uses tiered compilation by default: every method starts in the interpreter, which collects invocation and loop counters; hot methods get quickly compiled by C1, which produces decent code instrumented to keep profiling itself; and once the profile matures, C2 recompiles them with aggressive, profile-guided optimizations — deep inlining, escape analysis, loop unrolling. That's why a JVM application needs warmup before it reaches peak performance, and why naive microbenchmarks lie: they measure a mix of interpreter, C1, and compilation overhead, or worse, dead-code-eliminated nothing."

> "C2 is a speculative compiler — it bets that the future will look like the observed profile, for example inlining through a call site that has only ever seen one concrete type, guarded by a cheap check. When a speculation fails, the JIT deoptimizes: the compiled code is invalidated, execution falls back to the interpreter, and the method gets recompiled with the corrected profile. Deoptimization is the safety net that makes speculation profitable — the speculative fast path wins on every common execution, and the deopt cost is paid once per broken assumption."

> "Two practical consequences I always keep in mind: escape analysis means an object that doesn't escape a method can be scalar-replaced — never allocated at all — and its lock elided, so claims like 'allocation is expensive' or 'synchronized is slow' need to be qualified by what the JIT actually did; and any performance number measured without JMH or an equivalent harness — proper warmup, forked JVMs, Blackhole against dead code elimination — is an anecdote, not evidence."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| compilação just-in-time | just-in-time (JIT) compilation |
| compilação em camadas | tiered compilation |
| compilação ahead-of-time | ahead-of-time (AOT) compilation |
| interpretador | interpreter |
| perfil de execução / profiling | execution profile / profiling |
| aquecimento (da JVM) | (JVM) warmup |
| desotimização | deoptimization |
| análise de escape | escape analysis |
| substituição escalar | scalar replacement |
| elisão de lock | lock elision |
| eliminação de código morto | dead code elimination |
| desenrolamento de loop | loop unrolling |
| ponto de chamada monomórfico | monomorphic call site |
| substituição na pilha | on-stack replacement (OSR) |
| cache de código | code cache |
| caminho quente | hot path |
| código invalidado | made not entrant |
| compilador especulativo | speculative compiler |
| guard (verificação de especulação) | guard / uncommon trap check |
| contador de invocação | invocation counter |

## Veja também

- [[01 - A JVM — o que é e o pipeline de execução]]
- [[04 - Bytecode por dentro — anatomia e javap]]
- [[06 - Os coletores do HotSpot]]
- [[14 - Performance da JVM — síntese]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/09 - Streams primitivos|Streams primitivos]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]
- [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#tiered compilation|tiered compilation (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#escape analysis|escape analysis (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#deoptimization|deoptimization (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#inlining (JIT)|inlining (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#code cache|code cache (Dicionário)]]

## Referências

- [Java HotSpot Virtual Machine Performance Enhancements — Oracle JVM Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/vm/java-hotspot-virtual-machine-performance-enhancements.html) — tiered compilation default; papel do client compiler instrumentado; escape analysis (scalar replacement + eliminação de locks; sem stack allocation); compressed oops; segmented code cache
- [The java Command — man page (Java 21)](https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html) — `-XX:+PrintCompilation`, `-XX:+PrintInlining`, `-Xint`, `-Xcomp` ("should not be used in production environments"), `-XX:-TieredCompilation` (default: habilitada), `-XX:ReservedCodeCacheSize` (default 240 MB; 48 MB sem tiered; limite 2 GB)
- [JMH — Java Microbenchmark Harness (OpenJDK)](https://github.com/openjdk/jmh) — definição e propósito do harness; recomendação de rodar via projeto standalone, não pela IDE
