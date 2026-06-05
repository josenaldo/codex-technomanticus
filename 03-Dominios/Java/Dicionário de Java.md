---
title: "Dicionário de Java"
created: 2026-06-02
updated: 2026-06-03
type: glossary
status: growing
publish: true
tags:
  - java
  - glossary
  - moc
aliases:
  - Glossário de Java
---

# Dicionário de Java

> Glossário do domínio Java: termos de linguagem, plataforma e ecossistema. Semeado com o Galho 1 — Linguagem e sintaxe moderna; cresce a cada galho incorporado.

<!--
Como usar este glossário:

- Cada verbete é um `###` dentro de uma `##` temática (seção alfabética).
- Verbetes em ordem alfabética dentro de cada seção; ordenação case-insensitive, sem considerar acento.
- Linkar de outra nota: wikilink para este arquivo com âncora `#` + nome do termo.
- Customizar o texto exibido: adicionar o pipe `|` após a âncora, seguido do texto.
- A skill /verbete adiciona termos automaticamente em ordem alfabética.
- Cada verbete tem (i) 1-3 frases de definição em PT-BR e (ii) "Veja também:" com wikilinks para a(s) nota(s) que aprofundam.
-->

## A

### ABA problem
Anomalia em algoritmos lock-free onde um valor lido como A é alterado para B e de volta para A antes do CAS ser executado, fazendo o CAS ter sucesso incorretamente. A thread acredita que nada mudou, mas o estado intermediário pode ter corrompido invariantes. Solucionado com estampilhas de versão (ex: `AtomicStampedReference`).

Veja também: [[06 - Atômicos e operações lock-free]].

### Action API
`Action`/`AbstractAction` encapsulam um comportamento e seu estado (`enabled`, texto, ícone, accelerator key) em um único objeto reutilizável. O mesmo objeto pode ser plugado em botão, item de menu e toolbar, mantendo todos sincronizados automaticamente.

Veja também: [[03-Dominios/Java/Swing/11 - Action API, key bindings e performance|Action API]].

### adapter (event adapter)
Classe abstrata (ex.: `MouseAdapter`) que implementa um listener com métodos vazios, permitindo sobrescrever apenas os eventos de interesse, sem ter que implementar todos os métodos da interface.

Veja também: [[03-Dominios/Java/Swing/04 - O modelo de eventos|Modelo de eventos]].

### Atomic (variável atômica)
Variável que suporta operações de leitura, escrita e atualização compostas sem necessidade de `synchronized`, usando instruções CAS do hardware. O pacote `java.util.concurrent.atomic` oferece `AtomicInteger`, `AtomicLong`, `AtomicReference` e variantes. Garante atomicidade sem bloquear threads.

Veja também: [[06 - Atômicos e operações lock-free]].

### Autoboxing
Conversão automática entre tipos primitivos (ex: `int`) e seus wrappers (`Integer`) feita pelo compilador Java. O processo inverso — de wrapper para primitivo — chama-se *unboxing*. Pode causar `NullPointerException` e overhead de alocação se usado em laços intensivos.

Veja também: [[02 - Tipos, variáveis e operadores]].

### AWT (Abstract Window Toolkit)
Toolkit de GUI original do Java, com componentes heavyweight que têm peers nativos do sistema operacional. O Swing é construído sobre o AWT e o estende com componentes lightweight de renderização puramente Java.

Veja também: [[03-Dominios/Java/Swing/01 - O modelo do Swing|Modelo do Swing]].

## B

### Barrier (CyclicBarrier)
Ponto de sincronização onde um número fixo de threads deve se encontrar antes que qualquer uma prossiga. Ao contrário do `CountDownLatch`, o `CyclicBarrier` pode ser reutilizado após cada ciclo. Útil em algoritmos paralelos com fases distintas.

Veja também: [[09 - Sincronizadores]].

### BlockingQueue
Interface de fila thread-safe que bloqueia o produtor quando a fila está cheia e o consumidor quando está vazia, sem necessidade de `wait/notify` manuais. Implementações incluem `ArrayBlockingQueue`, `LinkedBlockingQueue` e `SynchronousQueue`. Pedra angular do padrão produtor-consumidor.

Veja também: [[07 - Concurrent collections]].

### Bytecode
Representação intermediária compilada pelo `javac` a partir do código-fonte `.java`, gravada em arquivos `.class`. Não é código de máquina nativo: é executado (ou JIT-compilado) pela JVM, o que viabiliza o princípio WORA.

Veja também: [[01 - O modelo da linguagem Java]].

## C

### Carrier thread
Thread da plataforma (OS thread) que executa uma virtual thread no modelo de virtual threads do Java. Uma virtual thread é montada sobre um carrier thread durante sua execução e desmontada ao bloquear, liberando o carrier para executar outra virtual thread.

Veja também: [[12 - Virtual Threads e Project Loom]].

### CAS (compare-and-swap)
Instrução atômica de hardware que compara o valor atual de uma posição de memória com um valor esperado e, somente se forem iguais, substitui pelo novo valor — tudo em uma única operação indivisível. Base de todos os algoritmos lock-free em Java. Exposto pela API `Unsafe` e pelas classes `Atomic*`.

Veja também: [[06 - Atômicos e operações lock-free]].

### cell editor
Componente temporário que entra em ação quando o usuário edita uma célula de `JTable`. Implementa `TableCellEditor` (ex.: `DefaultCellEditor` com `JComboBox`); confirma o valor editado via `stopCellEditing` e o devolve ao model.

Veja também: [[03-Dominios/Java/Swing/08 - Renderers e editors|Renderers e editors]].

### cell renderer
Objeto responsável por desenhar o conteúdo de cada célula ou item de `JTable`/`JList`, implementando `TableCellRenderer` ou `ListCellRenderer`. Reutilizado para pintar todas as células (rubber-stamp), por isso deve ser stateless.

Veja também: [[03-Dominios/Java/Swing/08 - Renderers e editors|Renderers e editors]].

### Checked exception
Exceção que o compilador obriga o desenvolvedor a declarar (`throws`) ou capturar (`try/catch`). Estende `Exception` (excluindo `RuntimeException`). Exemplos: `IOException`, `SQLException`. Usada quando o chamador pode se recuperar do erro.

Veja também: [[10 - Exceções e tratamento de erros]].

### Compact constructor
Construtor especial de records que omite a lista de parâmetros (não repete a assinatura) e executa antes da atribuição automática dos campos. Ideal para validação e normalização de dados sem boilerplate.

Veja também: [[13 - Records e record patterns]].

### CompletableFuture
Implementação de `Future` e `CompletionStage` introduzida no Java 8 que permite compor operações assíncronas em pipelines fluentes (`thenApply`, `thenCompose`, `thenCombine`). Suporta execução em thread pools customizados, tratamento de erros e combinação de múltiplos estágios sem bloqueio.

Veja também: [[10 - CompletableFuture e composição assíncrona]].

### componente lightweight / heavyweight
Componente lightweight (Swing) é pintado inteiramente em Java, sem peer nativo do SO; componente heavyweight (AWT) possui peer nativo. Lightweight possibilita aparência consistente cross-platform e suporte a pluggable look-and-feel.

Veja também: [[03-Dominios/Java/Swing/01 - O modelo do Swing|Modelo do Swing]].

### ConcurrentHashMap
Implementação de `Map` altamente concorrente que usa segmentação interna (striping) e CAS para permitir leituras sem bloqueio e escritas com granularidade fina. Substituiu `Hashtable` e `Collections.synchronizedMap` em cenários de alta concorrência. Não permite chaves ou valores `null`.

Veja também: [[07 - Concurrent collections]].

### Condição de corrida (race condition)
Defeito que ocorre quando o resultado de um programa depende da ordem de intercalação não-determinística de operações de múltiplas threads. Geralmente causada por acesso a estado compartilhado sem sincronização adequada. Difícil de reproduzir e depurar por ser sensível ao escalonamento do SO.

Veja também: [[04 - As armadilhas - race, deadlock e companhia]].

### content pane
Container interno de um top-level container (`JFrame`, `JDialog`) onde se adicionam os componentes visíveis da aplicação. `frame.add(...)` delega a ele. Usa `BorderLayout` por padrão.

Veja também: [[03-Dominios/Java/Swing/01 - O modelo do Swing|Modelo do Swing]].

### Contention
Situação em que múltiplas threads disputam o mesmo lock ou recurso simultaneamente, forçando algumas a esperar. Alta contention degrada performance e pode eliminar os ganhos do paralelismo. Mitigada por locks de granularidade fina, estruturas lock-free ou particionamento de estado.

Veja também: [[04 - As armadilhas - race, deadlock e companhia]].

## D

### Deadlock
Estado em que duas ou mais threads se bloqueiam mutuamente, cada uma esperando um lock que a outra segura — criando uma espera circular sem saída. Nenhuma das threads progride indefinidamente. Prevenido por ordenação consistente de locks, uso de `tryLock` com timeout ou eliminação de lock aninhado.

Veja também: [[04 - As armadilhas - race, deadlock e companhia]].

### Default method
Método com implementação definido em uma interface (palavra-chave `default`), introduzido no Java 8. Permite adicionar comportamento a interfaces sem quebrar classes que as implementam, viabilizando evolução retrocompatível de APIs.

Veja também: [[08 - Interfaces e classes abstratas]].

### delegation event model
Modelo de eventos do AWT/Swing: a fonte (componente) notifica os listeners registrados quando um evento ocorre, despachando um objeto de evento. Separa a produção do evento do seu tratamento, favorecendo extensibilidade.

Veja também: [[03-Dominios/Java/Swing/04 - O modelo de eventos|Modelo de eventos]].

### Document (modelo de texto)
Model dos componentes de texto (`JTextField`, `JTextArea`): representa o conteúdo como sequência de caracteres com atributos, não como `String`. Edições disparam `DocumentEvent` e podem ser interceptadas via `DocumentListener` ou `DocumentFilter`.

Veja também: [[03-Dominios/Java/Swing/07 - MVC em Swing e os models|MVC em Swing]].

### double buffering
Técnica em que o desenho é feito num buffer fora da tela e copiado de uma vez para o display, eliminando flicker. Ativo por padrão em todos os componentes Swing, gerenciado automaticamente pelo `RepaintManager`.

Veja também: [[03-Dominios/Java/Swing/10 - Custom painting e componentes customizados|Custom painting]].

## E

### EDT (Event Dispatch Thread)
Thread única onde o Swing processa todos os eventos e repinta a tela. A single-thread rule exige que todo acesso a componentes ocorra na EDT; operações longas nela travam a interface. Use `SwingUtilities.invokeLater` para delegar à EDT a partir de outras threads.

Veja também: [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|EDT]].

### effectively final
Variável local (ou parâmetro) que nunca é reatribuída após a inicialização, mesmo sem o modificador `final` explícito. Lambdas e classes anônimas só podem capturar variáveis `final` ou *effectively final*; reatribuir a variável depois da captura é erro de compilação. Garante que o valor capturado seja estável e evita closures sobre estado mutável.

Veja também: [[03-Dominios/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais]], [[03-Dominios/Java/Collections e Streams/13 - Composição funcional e funções de alta ordem|Composição funcional]].

### Enhanced for
Laço `for-each` — forma simplificada do `for` que itera diretamente sobre arrays ou qualquer objeto `Iterable`, sem índice explícito. Sintaxe: `for (Tipo var : coleção) { }`. Introduzido no Java 5.

Veja também: [[03 - Estruturas de controle e fluxo]].

### Enum
Tipo especial de classe cujas instâncias são um conjunto fechado e nomeado de constantes. Em Java, enums são objetos de pleno direito: podem ter campos, construtores, métodos e implementar interfaces. Garantem type-safety e eliminam "magic numbers".

Veja também: [[09 - Enums]].

### Exaustividade
Propriedade de um `switch` (expressão ou statement) que garante que todos os casos possíveis são cobertos. O compilador Java exige exaustividade em switch expressions e em switches sobre sealed classes e enums. Violação gera erro em tempo de compilação.

Veja também: [[14 - Sealed classes e pattern matching]].

### Executor / ExecutorService
Abstração do `java.util.concurrent` que desacopla a submissão de tarefas (`Runnable` ou `Callable`) de sua execução. `ExecutorService` estende `Executor` adicionando ciclo de vida (`shutdown`, `awaitTermination`) e suporte a `Future`. Preferido ao gerenciamento manual de threads.

Veja também: [[08 - Executors e thread pools]].

## F

### FlatLaf
Look and Feel moderno (flat, com suporte a dark mode) desenvolvido pela FormDev, disponível como biblioteca open-source third-party — não faz parte do JDK. Mantém aplicações Swing com aparência atual em diferentes sistemas operacionais.

Veja também: [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel]].

### Fork/join
Framework introduzido no Java 7 (`ForkJoinPool`, `RecursiveTask`, `RecursiveAction`) que divide um problema em subproblemas menores (fork), resolve-os em paralelo e combina os resultados (join). Usa work-stealing para maximizar a utilização dos núcleos. Base dos parallel streams e do `CompletableFuture`.

Veja também: [[15 - Parallel streams e fork-join]].

### Function / Predicate / Consumer / Supplier
As quatro interfaces funcionais centrais de `java.util.function`. `Function<T,R>` transforma um T em R (`apply`); `Predicate<T>` testa uma condição booleana sobre T (`test`); `Consumer<T>` executa uma ação sobre T sem retorno (`accept`); `Supplier<T>` fornece um T sem receber argumento (`get`). Cada uma traz métodos `default` de composição — `andThen`/`compose` (`Function`), `and`/`or`/`negate` (`Predicate`), `andThen` (`Consumer`) — base da composição funcional e das operações de Stream.

Veja também: [[03-Dominios/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais]], [[03-Dominios/Java/Collections e Streams/13 - Composição funcional e funções de alta ordem|Composição funcional]].

### Future
Interface que representa o resultado de uma operação assíncrona ainda em execução. Permite verificar se concluiu (`isDone`), cancelar (`cancel`) ou obter o resultado bloqueando (`get`). Limitada por não suportar composição; `CompletableFuture` supera essas limitações.

Veja também: [[08 - Executors e thread pools]].

## G

### Generics
Mecanismo de parametrização de tipos que permite escrever classes, interfaces e métodos que operam sobre um tipo definido pelo chamador, com checagem em tempo de compilação. Elimina casts explícitos e detecta erros de tipo cedo. Ex: `List<String>`.

Veja também: [[12 - Generics em profundidade]].

### GridBagLayout
Layout manager mais flexível do Swing: posiciona componentes numa grade configurável via `GridBagConstraints` (gridx, gridy, weightx, weighty, fill, anchor). Poderoso para layouts complexos, mas verboso em comparação com alternativas como `MigLayout`.

Veja também: [[03-Dominios/Java/Swing/03 - Layout managers|Layout managers]].

### Guard
Condição booleana adicional (`when`) que refina um case de pattern matching. Permite combinar a verificação de tipo/estrutura com uma expressão lógica no mesmo braço do switch. Ex: `case Integer i when i > 0 -> ...`.

Veja também: [[14 - Sealed classes e pattern matching]].

## H

### Happens-before
Relação de ordenação definida pelo Java Memory Model (JMM) que garante que ações de uma thread sejam visíveis e ordenadas corretamente para outra thread. Não é ordem temporal: duas ações podem ocorrer em qualquer tempo, mas se A happens-before B, o efeito de A é garantidamente visível quando B ocorre. Estabelecida por `synchronized`, `volatile`, start/join de threads, entre outros.

Veja também: [[11 - Java Memory Model em profundidade]].

## I

### Imutabilidade
Propriedade de um objeto cujo estado não pode ser alterado após a criação. Em Java, alcançada declarando campos `final`, não expondo mutadores e retornando cópias defensivas. Facilita raciocínio sobre o código e é segura para uso concorrente.

Veja também: [[06 - Classes, objetos e encapsulamento]].

### Inferência de tipo
Capacidade do compilador de deduzir o tipo de uma variável local a partir da expressão à direita, sem que o programador o declare explicitamente. Em Java (a partir do Java 10): `var nome = "Alice";`. Só se aplica a variáveis locais com inicializador.

Veja também: [[02 - Tipos, variáveis e operadores]].

### InputMap / ActionMap (key bindings)
Mecanismo de atalhos de teclado do Swing: `InputMap` mapeia `KeyStroke` para uma chave string, e `ActionMap` mapeia a chave para uma `Action`. Supera `KeyListener` por suportar escopos de foco (`WHEN_IN_FOCUSED_WINDOW`) independentemente de qual componente está focado.

Veja também: [[03-Dominios/Java/Swing/11 - Action API, key bindings e performance|Action API]].

### invokeLater / invokeAndWait
`SwingUtilities.invokeLater` agenda um `Runnable` para execução na EDT de forma assíncrona; `SwingUtilities.invokeAndWait` faz o mesmo de forma síncrona, bloqueando até a conclusão. `invokeAndWait` não pode ser chamado a partir da própria EDT.

Veja também: [[03-Dominios/Java/Swing/05 - A Event Dispatch Thread|EDT]].

## J

### JComponent
Classe-base da maioria dos componentes Swing (`J*`), que estende `Container` do AWT. Adiciona suporte a pluggable look-and-feel, double buffering, borders, tooltips, key bindings e painting otimizado.

Veja também: [[03-Dominios/Java/Swing/01 - O modelo do Swing|Modelo do Swing]].

## L

### Latch (CountDownLatch)
Sincronizador de uso único que permite que uma ou mais threads aguardem até que um contador chegue a zero. O contador é decrementado por `countDown()` e a espera é feita com `await()`. Ideal para aguardar a conclusão de um conjunto de tarefas ou o início de um evento comum. Não pode ser reutilizado.

Veja também: [[09 - Sincronizadores]].

### layout manager
Objeto que posiciona e dimensiona automaticamente os componentes de um container, respondendo a resize, look-and-feel e DPI. Exemplos: `BorderLayout`, `FlowLayout`, `BoxLayout`, `GridBagLayout`. Evita coordenadas absolutas e torna o layout adaptável.

Veja também: [[03-Dominios/Java/Swing/03 - Layout managers|Layout managers]].

### listener (event listener)
Objeto registrado em um componente (fonte) para ser notificado quando eventos específicos ocorrem, via callback (ex.: `ActionListener.actionPerformed`). Os callbacks são invocados na EDT.

Veja também: [[03-Dominios/Java/Swing/04 - O modelo de eventos|Modelo de eventos]].

### Livelock
Situação em que duas ou mais threads continuam executando (não bloqueadas) mas não progridem, pois cada uma reage à ação da outra em loop infinito — como duas pessoas que se desviam na mesma direção no corredor. Diferente do deadlock, as threads estão ativas mas inutilmente.

Veja também: [[04 - As armadilhas - race, deadlock e companhia]].

### Lock-free
Propriedade de um algoritmo ou estrutura de dados que garante progresso global mesmo se threads individuais forem preemptadas indefinidamente — ao menos uma thread sempre avança. Implementado com CAS e loops de retry sem `synchronized`. Reduz contention e risco de deadlock ao custo de maior complexidade.

Veja também: [[06 - Atômicos e operações lock-free]].

### look and feel (L&F)
Conjunto plugável que define a aparência visual e o comportamento interativo de todos os componentes Swing. Trocável em runtime via `UIManager.setLookAndFeel`; inclui opções como Metal, Nimbus, System L&F e bibliotecas third-party como FlatLaf.

Veja também: [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel]].

### LTS
Long-Term Support — versão do Java que recebe atualizações de segurança e correções por um período estendido (vários anos). Recomendada para produção. As principais versões LTS modernas são Java 8, 11, 17, 21 e 25.

Veja também: [[01 - O modelo da linguagem Java]], [[15 - A evolução do Java (8 a 25)]].

## M

### Monitor (intrinsic lock)
Mecanismo de sincronização intrínseco de todo objeto Java que combina exclusão mútua e comunicação via `wait/notify/notifyAll`. Cada objeto tem um lock implícito adquirido com `synchronized`. Ao entrar em um bloco `synchronized`, a thread adquire o monitor; ao sair, libera-o automaticamente.

Veja também: [[03 - Exclusão mútua com synchronized]].

### Mutual exclusion (exclusão mútua)
Propriedade que garante que apenas uma thread por vez execute uma seção crítica de código que acessa estado compartilhado. Implementada em Java por `synchronized`, `ReentrantLock` ou semáforos com 1 permissão. Previne condições de corrida ao serializar o acesso.

Veja também: [[03 - Exclusão mútua com synchronized]].

## N

### Nimbus
Look and Feel vetorial bundled no JDK desde o Java 7, alternativa ao Metal padrão. Renderiza os componentes com formas suaves e escala melhor em diferentes resoluções de tela. Configurável via `UIManager.put` para ajustes de cores e fontes.

Veja também: [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel]].

## O

### Overloading
Definição de múltiplos métodos com o mesmo nome mas assinaturas diferentes (quantidade ou tipos de parâmetros) em uma mesma classe. A resolução acontece em tempo de compilação com base nos tipos dos argumentos. Não deve ser confundido com overriding.

Veja também: [[07 - Herança e polimorfismo]].

### Overriding
Redefinição de um método herdado em uma subclasse, mantendo a mesma assinatura. Anotado com `@Override` para verificação do compilador. É o mecanismo base do polimorfismo dinâmico em Java — a JVM escolhe a implementação em tempo de execução pelo tipo real do objeto.

Veja também: [[07 - Herança e polimorfismo]].

## P

### paintComponent / custom painting
Método a sobrescrever (em vez de `paint`) para desenhar conteúdo customizado em um componente Swing. Deve chamar `super.paintComponent(g)` antes de desenhar e fazer cast de `Graphics` para `Graphics2D` para acessar a API completa de renderização Java2D.

Veja também: [[03-Dominios/Java/Swing/10 - Custom painting e componentes customizados|Custom painting]].

### Pattern matching
Mecanismo que combina teste de tipo, extração de componentes e (opcionalmente) uma guarda em uma única expressão coesa. A partir do Java 16 (`instanceof`) e Java 21 (switch patterns), elimina casts manuais e torna o código mais legível e seguro.

Veja também: [[14 - Sealed classes e pattern matching]].

### PECS
Producer Extends, Consumer Super — regra mnemônica para uso de wildcards em Generics. Use `? extends T` quando a coleção é fonte de dados (apenas leitura); use `? super T` quando a coleção é destino (apenas escrita). Define qual operação é type-safe em cada contexto.

Veja também: [[12 - Generics em profundidade]].

### Pinning
Fenômeno em que uma virtual thread fica "presa" ao seu carrier thread durante um bloco `synchronized` ou chamada nativa, impedindo que o carrier execute outras virtual threads enquanto aguarda. Reduz a escalabilidade de virtual threads; mitigado substituindo `synchronized` por `ReentrantLock` ou eliminando bloqueios em seções críticas.

Veja também: [[12 - Virtual Threads e Project Loom]].

### pluggable look-and-feel
Arquitetura do Swing em que a renderização de cada componente é delegada a um UI delegate (`ComponentUI`), separando o modelo/lógica da apresentação visual. Permite trocar toda a aparência da aplicação via `UIManager.setLookAndFeel` sem alterar o código da aplicação.

Veja também: [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel]].

### Polimorfismo
Capacidade de um mesmo método ou referência se comportar de maneiras diferentes conforme o tipo real do objeto em tempo de execução. Em Java, é realizado principalmente por overriding + herança/interface. Permite escrever código genérico que opera sobre famílias de tipos.

Veja também: [[07 - Herança e polimorfismo]].

### Preview feature
Funcionalidade completa de linguagem ou JVM incluída em uma versão do Java para coleta de feedback, mas não finalizada. Precisa ser habilitada explicitamente com `--enable-preview` em compilação e execução. Pode mudar ou ser removida antes de tornar-se permanente.

Veja também: [[15 - A evolução do Java (8 a 25)]].

## R

### Record
Classe de dados imutável declarada com `record NomeClasse(Tipo campo, ...)`. O compilador gera automaticamente construtor canônico, acessores, `equals`, `hashCode` e `toString`. Ideal para portadores de dados sem lógica de negócio.

Veja também: [[13 - Records e record patterns]].

### Record pattern
Extensão de pattern matching que desconstói um record diretamente no `instanceof` ou `switch`, ligando seus componentes a variáveis locais. Permite navegação estrutural em hierarquias de dados sem getters explícitos.

Veja também: [[13 - Records e record patterns]], [[14 - Sealed classes e pattern matching]].

## S

### Safe publication (publicação segura)
Conjunto de técnicas que garantem que um objeto construído por uma thread seja corretamente visível por outras threads sem objetos parcialmente inicializados. Alcançada via campos `final`, `volatile`, referências em coleções thread-safe ou blocos `synchronized`. Sem safe publication, outra thread pode ver o objeto em estado incompleto.

Veja também: [[11 - Java Memory Model em profundidade]].

### Scoped value
Mecanismo final (permanente) do Java 25 para compartilhar dados imutáveis com threads descendentes sem passar parâmetros explicitamente, como alternativa segura e eficiente ao `ThreadLocal`. O valor é acessível apenas dentro de um escopo delimitado e não pode ser alterado após a ligação.

Veja também: [[14 - Scoped values]].

### Sealed class
Classe (ou interface) que restringe explicitamente quais subclasses (ou subinterfaces) podem estendê-la, usando a palavra-chave `sealed` e a cláusula `permits`. Permite ao compilador verificar exaustividade em switches e torna hierarquias fechadas e explicitamente documentadas.

Veja também: [[14 - Sealed classes e pattern matching]].

### Semaphore (semáforo)
Sincronizador que controla o acesso a um recurso com um número limitado de permissões. Threads adquirem permissões com `acquire()` e as devolvem com `release()`; quando todas as permissões estão em uso, novos `acquire()` bloqueiam. Útil para limitar concorrência em pools de recursos ou seções com capacidade máxima.

Veja também: [[09 - Sincronizadores]].

### separable model (MVC do Swing)
Variação do MVC adotada pelo Swing: o model (dados) é separado do componente, enquanto view e controller são fundidos no UI delegate. O desenvolvedor customiza o model (ex.: `TableModel`); raramente precisa alterar view ou controller.

Veja também: [[03-Dominios/Java/Swing/07 - MVC em Swing e os models|MVC em Swing]].

### Starvation
Situação em que uma thread nunca obtém acesso a um recurso porque outras threads de maior prioridade ou mais agressivas o monopolizam indefinidamente. A thread não está bloqueada em deadlock — continua elegível para execução — mas jamais é escalonada. Mitigada com políticas de lock fair (ex: `new ReentrantLock(true)`).

Veja também: [[04 - As armadilhas - race, deadlock e companhia]].

### String pool
Área de memória (no heap, a partir do Java 7) onde a JVM armazena strings literais de forma deduplicada. Dois literais idênticos referenciam o mesmo objeto, economizando memória. Strings criadas com `new String(...)` não entram no pool automaticamente; `intern()` força a entrada.

Veja também: [[04 - Strings e text blocks]].

### Structured concurrency
API de concorrência estruturada em preview no Java 25 (exige `--enable-preview`), que trata um conjunto de tarefas concorrentes como uma unidade coesa com ciclo de vida delimitado por um `StructuredTaskScope`. Garante que subtarefas são concluídas (ou canceladas) antes que o escopo seja fechado, simplificando o tratamento de erros e cancelamento.

Veja também: [[13 - Structured concurrency]].

### SwingWorker
Classe utilitária para executar trabalho demorado em uma background thread (`doInBackground`) e devolver resultados e progresso à EDT (`process`/`done`), sem congelar a interface. Cada instância é de uso único — não pode ser reiniciada.

Veja também: [[03-Dominios/Java/Swing/06 - SwingWorker e tarefas em background|SwingWorker]].

### Switch expression
Forma moderna do `switch` (Java 14+) que é uma expressão — produz um valor — e usa a sintaxe de seta (`case X -> valor`). Elimina fall-through acidental, exige exaustividade e pode ser atribuído diretamente a uma variável.

Veja também: [[03 - Estruturas de controle e fluxo]].

### Synchronized
Modificador Java que garante exclusão mútua e visibilidade de memória. Pode ser aplicado a métodos (bloqueia no objeto `this` ou na classe) ou a blocos (`synchronized(lock) { }`) que bloqueiam em um objeto arbitrário. A thread adquire o monitor ao entrar e o libera ao sair, mesmo em caso de exceção.

Veja também: [[03 - Exclusão mútua com synchronized]].

## T

### TableModel / ListModel
Interfaces de model para `JTable` (`TableModel`) e `JList` (`ListModel`): guardam os dados que o componente apenas exibe. `AbstractTableModel` e `AbstractListModel` facilitam implementações customizadas, exigindo apenas os métodos essenciais.

Veja também: [[03-Dominios/Java/Swing/07 - MVC em Swing e os models|MVC em Swing]].

### Text block
Literal de string multilinha delimitado por `"""` (Java 15+). Preserva a indentação relativa, suporta interpolação futura e elimina concatenações e escapes desnecessários em strings longas como SQL, JSON ou HTML embutido.

Veja também: [[04 - Strings e text blocks]].

### Thread pool
Conjunto de threads pré-criadas e reutilizáveis que executam tarefas submetidas a uma fila, evitando o custo de criar e destruir threads para cada tarefa. Em Java, provido por `ExecutorService` com implementações como `ThreadPoolExecutor`, `FixedThreadPool` e `ForkJoinPool`. Fundamental para escalabilidade de aplicações concorrentes.

Veja também: [[08 - Executors e thread pools]].

### Try-with-resources
Construção `try (Recurso r = ...)` que garante o fechamento automático de qualquer objeto `AutoCloseable` ao fim do bloco, mesmo em caso de exceção. Elimina o padrão `finally { r.close(); }` e torna o gerenciamento de recursos mais seguro e legível.

Veja também: [[10 - Exceções e tratamento de erros]].

### Type erasure
Processo pelo qual o compilador Java remove as informações de tipo genérico em tempo de compilação, substituindo parâmetros de tipo por `Object` (ou pelo bound superior). Em tempo de execução, `List<String>` e `List<Integer>` são indistinguíveis, o que limita certas reflexões e casts.

Veja também: [[12 - Generics em profundidade]].

## U

### UIManager
Classe que gerencia o look and feel ativo e os defaults de UI de todos os componentes Swing. Métodos principais: `setLookAndFeel`, `getSystemLookAndFeelClassName`, `getLookAndFeelDefaults`. Permite sobrescrever cores, fontes e bordas via `UIManager.put(chave, valor)`.

Veja também: [[03-Dominios/Java/Swing/09 - Look and Feel e temas|Look and Feel]].

### Unchecked exception
Exceção que não precisa ser declarada nem capturada obrigatoriamente. Estende `RuntimeException` ou `Error`. Exemplos: `NullPointerException`, `IllegalArgumentException`. Geralmente indica bugs ou estados inesperados que o chamador não tem como recuperar programaticamente.

Veja também: [[10 - Exceções e tratamento de erros]].

## V

### Varargs
Mecanismo que permite declarar um método com número variável de argumentos do mesmo tipo (`Tipo... nomes`). O compilador converte os argumentos em um array. Deve ser o último parâmetro da assinatura e gera um aviso se usado junto com generics por ambiguidade de heap pollution.

Veja também: [[05 - Arrays e varargs]].

### Virtual thread
Thread leve gerenciada pela JVM (não mapeada 1:1 com OS threads), GA no Java 21 (JEP 444). Permite criar milhões de threads com baixo overhead de memória, tornando o modelo thread-per-request viável em servidores de alta concorrência. Criadas via `Thread.ofVirtual()` ou `Executors.newVirtualThreadPerTaskExecutor()`.

Veja também: [[12 - Virtual Threads e Project Loom]].

### Volatile
Modificador de campo que garante visibilidade imediata de escritas a todas as threads e proíbe reordenação de instruções ao redor da variável. Garante visibilidade e ordering, mas NÃO garante atomicidade composta: `volatile int i; i++` ainda é uma race condition pois envolve leitura-modificação-escrita não-atômica.

Veja também: [[11 - Java Memory Model em profundidade]].

## W

### Wildcard
Argumento de tipo genérico desconhecido, representado por `?`. Pode ser não-limitado (`?`), com limite superior (`? extends T`) ou com limite inferior (`? super T`). Aumenta a flexibilidade das APIs genéricas ao custo de restringir as operações permitidas sobre a coleção.

Veja também: [[12 - Generics em profundidade]].

### WORA
Write Once, Run Anywhere — princípio central do Java: o bytecode compilado roda em qualquer plataforma que possua uma JVM compatível, sem recompilação. Viabilizado pela camada de abstração da JVM entre o código e o hardware/SO.

Veja também: [[01 - O modelo da linguagem Java]].

### Work-stealing
Estratégia de escalonamento do `ForkJoinPool` onde threads ociosas "roubam" tarefas da fila de outras threads sobrecarregadas. Reduz ociosidade e melhora o balanceamento dinâmico de carga em workloads irregulares. Cada worker mantém uma deque (fila dupla) de tarefas; o roubo ocorre pela extremidade oposta.

Veja também: [[15 - Parallel streams e fork-join]].

## Y

### Yield
Palavra-chave usada dentro de um bloco de switch expression (`case X -> { ... yield valor; }`) para retornar o valor produzido pelo bloco. Necessário quando o braço do switch contém mais de uma instrução; na sintaxe de seta simples, o valor é retornado diretamente sem `yield`.

Veja também: [[03 - Estruturas de controle e fluxo]].
