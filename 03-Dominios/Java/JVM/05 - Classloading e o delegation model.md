---
title: "Classloading e o delegation model"
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
  - classloading
aliases:
  - "Classloader"
  - "Parent delegation"
  - "Carregamento de classes"
---

# Classloading e o delegation model

> [!abstract] TL;DR
> Classes entram na JVM sob demanda em três fases: **loading → linking → initialization**. Antes de tentar carregar uma classe, cada classloader delega o pedido ao seu parent — o que garante que `java.lang.String` sempre vem do bootstrap loader e não pode ser substituída por código da aplicação. A identidade de uma classe é o par **nome binário + classloader que a definiu**: a mesma classe carregada duas vezes por loaders diferentes produz dois tipos incompatíveis para a JVM.

## O que é

Classloading é o processo pelo qual a JVM encontra, lê e prepara a representação binária de uma classe ou interface — tudo isso **sob demanda**, no momento em que o tipo é referenciado pela primeira vez, não no startup da aplicação.

O processo se divide em três fases principais:

**1. Loading** — o classloader localiza o bytecode (`.class`) pelo nome binário da classe, lê os bytes e constrói o objeto `Class<?>` correspondente na Method Area (Metaspace). A distinção entre *defining loader* (quem efetivamente chamou `defineClass`) e *initiating loader* (quem iniciou a busca, podendo ter delegado) é formal na spec e relevante para entender conflitos.

**2. Linking** — integra a classe ao estado de runtime da JVM. Composta por três sub-fases:

- **Verification** — verifica que o bytecode é estruturalmente válido conforme as restrições da JVM Spec §4.9. Lança `VerifyError` se houver violação. Pode carregar classes adicionais (para checar tipos), mas não as verifica nem prepara.
- **Preparation** — aloca os campos estáticos e os inicializa com os **valores-padrão** (`null`, `0`, `false`) — sem executar nenhum código Java. Os inicializadores explícitos (`static int X = 42`) ficam para a fase de initialization.
- **Resolution** — converte referências simbólicas da constant pool (nomes de classes, campos e métodos como strings) em referências diretas e concretas. É **lazy**: ocorre no momento em que cada instrução que a exige é executada (`new`, `invokestatic`, `getfield`, etc.).

**3. Initialization** — executa o método `<clinit>` da classe (bloco `static { ... }` e inicializadores de campos estáticos, na ordem declarada). Ocorre antes do primeiro uso efetivo da classe — instanciação (`new`), acesso a campo estático (`getstatic`/`putstatic`) ou chamada de método estático (`invokestatic`). Uma classe é completamente verificada e preparada antes de ser inicializada.

## Por que importa

App servers (Tomcat, WildFly), sistemas de plugins, frameworks de injeção de dependência (Spring, CDI) e ferramentas de hot reload (JRebel, Quarkus dev mode) dependem inteiramente do mecanismo de classloading para isolar aplicações, carregar versões diferentes de uma mesma biblioteca e substituir classes em runtime.

Consequência prática: uma fatia significativa dos erros "estranhos" de deploy tem origem em classloading:

- `ClassNotFoundException` — pedido explícito ao classloader falhou; a classe não foi encontrada na hierarquia.
- `NoClassDefFoundError` — a classe estava presente na compilação, mas sumiu no runtime (jar faltando no classpath), **ou** o `<clinit>` lançou uma exceção na primeira tentativa de inicialização e a classe ficou em estado inválido.
- `ClassCastException` "impossível" — a mesma classe foi carregada por dois classloaders diferentes e os tipos resultantes são incompatíveis para o sistema de tipos da JVM.
- `LinkageError` / `VerifyError` — bytecode inválido ou conflito de versão de uma dependência compartilhada.

Entender classloading é o mapa para diagnosticar esses erros sem adivinhar.

## Como funciona

### As três fases (o que acontece em cada)

```text
┌─────────────────────────────────────────────────────────┐
│                     CLASSLOADING                        │
│                                                         │
│  1. Loading        → lê bytes → cria Class<?> object   │
│                                                         │
│  2. Linking                                             │
│     2a. Verification  → valida bytecode estruturalmente │
│     2b. Preparation   → aloca statics, defaults         │
│     2c. Resolution    → resolve symrefs (lazy)          │
│                                                         │
│  3. Initialization → executa <clinit>                   │
└─────────────────────────────────────────────────────────┘
```

Verification e preparation podem ocorrer imediatamente após o loading ou de forma adiantada pelo JIT — a spec permite liberdade ao implementador, desde que os invariantes sejam mantidos. Resolution é sempre lazy por design, o que é crucial para o startup rápido da JVM.

### A hierarquia (Bootstrap → Platform → Application/System)

Desde Java 9, com a introdução do JPMS, a JVM tem três classloaders embutidos com papéis bem definidos:

```text
Bootstrap ClassLoader
  │  carrega: java.base e outros módulos core do JDK
  │  representado como: null em ClassLoader.getParent()
  │  não tem parent
  │
  └── Platform ClassLoader  (nome: "platform")
        │  carrega: módulos da plataforma Java SE não cobertos pelo bootstrap
        │  (ex: java.sql, java.xml, java.logging)
        │  parent: Bootstrap
        │
        └── System/Application ClassLoader  (nome: "app")
              carrega: classpath da aplicação (java.class.path),
                       module path, ferramentas JDK
              parent: Platform
              retornado por: ClassLoader.getSystemClassLoader()
```

Antes do Java 9 existia o Extension ClassLoader no lugar do Platform ClassLoader. A mudança reflete a modularização do JDK: o Platform ClassLoader pode, em casos específicos de upgrade de módulos, delegar para o Application ClassLoader — o que é atípico mas está previsto na API.

### Parent delegation (pedido sobe antes de carregar)

O `loadClass` do `ClassLoader` segue este algoritmo por padrão:

```text
loadClass("com.example.Order"):
  1. findLoadedClass("com.example.Order") — já foi carregada antes?
     → se sim, retorna a Class<?> cacheada

  2. parent.loadClass("com.example.Order")  ← delega para o parent
     → se parent == null, usa o bootstrap loader
     → se o parent encontrar, retorna a Class<?> do parent

  3. this.findClass("com.example.Order")  ← só tenta carregar localmente
     → se encontrar, chama defineClass e retorna
     → se não encontrar, lança ClassNotFoundException
```

Por que isso protege `java.lang.String`? Quando qualquer classloader tenta carregar `java.lang.String`, o pedido sobe até o Bootstrap loader, que a encontra imediatamente no módulo `java.base` e a retorna. O classloader da aplicação nunca chega à etapa 3 para `java.lang.*` — logo, um jar malicioso com uma `String` substituta simplesmente não chega a ser carregado pelo mecanismo padrão.

Subclasses de `ClassLoader` são encorajadas a sobrescrever `findClass` (não `loadClass`) para preservar o contrato de delegação. Quebrar o contrato — busca local antes de delegar — é a técnica usada por classloaders de contexto (*context classloaders*) em app servers para inverter a delegação, o que exige cuidado redobrado.

### Custom classloaders (isolamento de apps, plugins, hot reload)

Custom classloaders são a base de:

- **Isolamento em app servers**: cada aplicação web tem seu próprio `WebappClassLoader`. Duas apps podem usar versões diferentes do `commons-lang` sem conflito, porque cada versão está num classloader distinto.
- **Sistemas de plugins**: cada plugin recebe um classloader próprio. O host define quais pacotes são compartilhados (carregados pelo parent comum) e quais são privados de cada plugin.
- **Hot reload em dev**: o classloader da versão antiga é descartado e um novo carrega os `.class` recompilados. Funciona porque a identidade da classe inclui o classloader — a nova versão é um tipo diferente para a JVM.

### Identidade de classe = classe + classloader

Este é o ponto mais contraintuitivo do modelo. A JVM identifica uma classe pelo par `(nome binário, classloader que a definiu)`. A mesma classe `com.example.Order` carregada por dois classloaders distintos produz **dois objetos `Class<?>` distintos** — e os objetos dessas classes são de tipos incompatíveis entre si.

```text
ClassLoader A  →  define  com.example.Order  →  Class<?> #1
ClassLoader B  →  define  com.example.Order  →  Class<?> #2

Class<?> #1 != Class<?> #2

Objeto de #1  instanceof  Class<?> #2  →  FALSE
Cast de objeto de #1 para tipo de #2  →  ClassCastException
```

Essa propriedade é fundamental para o isolamento. É também a causa raiz dos `ClassCastException` "impossíveis" — onde o stack trace mostra `ClassCastException: com.example.Order cannot be cast to com.example.Order`.

## Na prática

### `Class.forName` vs `ClassLoader.loadClass`

```java
// Class.forName — carrega E INICIALIZA por padrão
Class<?> clazz = Class.forName("com.example.OrderProcessor");
// <clinit> de OrderProcessor já foi executado aqui

// Class.forName com initialize=false — carrega, mas NÃO inicializa
Class<?> clazz = Class.forName("com.example.OrderProcessor",
                                false,
                                Thread.currentThread().getContextClassLoader());
// <clinit> ainda não executou

// ClassLoader.loadClass — carrega, faz linking opcional, NÃO inicializa
ClassLoader cl = Order.class.getClassLoader();
Class<?> clazz = cl.loadClass("com.example.OrderProcessor");
// <clinit> ainda não executou
```

A diferença importa para frameworks de DI e ORMs que carregam classes registradas por nome: se o `<clinit>` tem efeitos colaterais (registrar um driver JDBC, por exemplo), `Class.forName` é a escolha correta — e é exatamente como `DriverManager` funciona.

### Inspecionando a cadeia de classloaders

```java
// Inspecionando a cadeia de classloaders de uma classe de negócio
Class<?> cls = Order.class;

ClassLoader loader = cls.getClassLoader();
while (loader != null) {
    System.out.println(loader.getName() + " → " + loader);
    loader = loader.getParent();
}
System.out.println("null (bootstrap)");
```

Saída típica em aplicação standalone:

```text
app → jdk.internal.loader.ClassLoaders$AppClassLoader@<addr>
platform → jdk.internal.loader.ClassLoaders$PlatformClassLoader@<addr>
null (bootstrap)
```

Para uma classe do JDK como `java.util.ArrayList`:

```text
null (bootstrap)
```

`getClassLoader()` retorna `null` para classes carregadas pelo bootstrap loader.

### Sistema de plugins com classloader por plugin (hipotético)

```java
// hipotético: framework de plugins onde cada plugin tem isolamento de classpath
public class PluginLoader {

    public Plugin load(Path pluginJar, String mainClass) throws Exception {
        // Cria um classloader filho que lê o jar do plugin
        // mas delega ao parent (app classloader) para as classes da API compartilhada
        URLClassLoader pluginCl = new URLClassLoader(
            new URL[]{ pluginJar.toUri().toURL() },
            PluginLoader.class.getClassLoader()  // ← parent = app classloader
        );

        // loadClass NÃO inicializa — Class.forName com initialize=true para executar o <clinit>
        Class<?> pluginClass = Class.forName(mainClass, true, pluginCl);
        return (Plugin) pluginClass.getDeclaredConstructor().newInstance();
    }

    public void unload(URLClassLoader pluginCl) throws IOException {
        pluginCl.close(); // ← libera referências; permite GC do classloader
    }
}
```

A interface `Plugin` deve ser carregada pelo parent classloader (app ou acima), não pelo classloader do plugin — caso contrário, o cast `(Plugin)` lança `ClassCastException` por identidade incompatível.

## Armadilhas

### (1) Mesma classe, dois classloaders → ClassCastException "impossível"

**O problema:** num sistema com plugins ou múltiplos módulos, a classe `com.example.Order` pode ser carregada tanto pelo classloader do plugin quanto pelo classloader do host — se ambos tiverem o jar no seu classpath. Um objeto criado no contexto do plugin não pode ser convertido para o tipo `Order` do host, mesmo que o bytecode seja idêntico.

```java
// Cenário: plugin carrega sua própria cópia de Order
Object orderFromPlugin = pluginCl.loadClass("com.example.Order")
                                 .getDeclaredConstructor()
                                 .newInstance();

// LANÇA ClassCastException mesmo que o bytecode seja idêntico:
Order order = (Order) orderFromPlugin;
// ClassCastException: com.example.Order cannot be cast to com.example.Order

// instanceof também falha:
boolean same = orderFromPlugin instanceof Order; // false
```

**Fix:** classes compartilhadas entre host e plugin devem vir exclusivamente do classloader parent comum. O classloader do plugin **não** deve ter o jar dessas classes no seu próprio classpath — elas chegam por delegação. A regra prática: a API de contrato (interfaces, DTOs compartilhados) fica no parent; a implementação fica em cada classloader filho.

---

### (2) Leak de classloader em redeploy → Metaspace OOM

**O problema:** em redeploys de apps em servidores, o classloader antigo deve ser elegível para GC. Se algum objeto ainda tem referência ao classloader antigo — via campo `static`, `ThreadLocal`, caches de framework — o classloader **não é coletado**, e as classes que ele definiu permanecem no Metaspace. Redeployar repetidamente sem reiniciar o servidor leva a `OutOfMemoryError: Metaspace`.

As áreas de memória da JVM, incluindo o Metaspace onde as classes vivem, estão detalhadas em [[02 - Áreas de memória de runtime]].

```java
// Fonte clássica de leak: ThreadLocal estático não limpo no undeploy
public class RequestContext {
    // static → sempre alcançável a partir dos GC roots
    // contém referências a objetos cujas classes foram carregadas pelo WebappClassLoader
    private static final ThreadLocal<RequestData> CONTEXT = new ThreadLocal<>();
}
```

**Fix:** no listener de undeploy (ex: `ServletContextListener.contextDestroyed`), limpe explicitamente todos os `ThreadLocal`s, cancele timers e threads de background e remova listeners de eventos que registraram callbacks com referência ao classloader da aplicação. Ferramentas como `jmap` e analisadores de heap (Eclipse MAT) ajudam a identificar o caminho de referência que impede o GC.

---

### (3) ClassNotFoundException vs NoClassDefFoundError — não são a mesma coisa

**O problema:** ambos indicam "classe não encontrada", mas têm origens e tratamentos completamente diferentes:

| Exceção | Tipo | Quando ocorre |
|---------|------|---------------|
| `ClassNotFoundException` | `Exception` (checked) | Pedido explícito ao classloader (`Class.forName`, `loadClass`) falhou — a classe não está no classpath |
| `NoClassDefFoundError` | `Error` (unchecked) | A classe estava presente na compilação mas sumiu no runtime (jar ausente), **ou** o `<clinit>` lançou uma exceção na primeira tentativa de inicialização e a JVM marcou a classe como inválida |

```java
// ClassNotFoundException — checked, pedido explícito falhou
try {
    Class<?> cls = Class.forName("com.example.MissingService"); // jar não está no classpath
} catch (ClassNotFoundException e) {
    // esperado — trate com fallback ou log adequado
}

// NoClassDefFoundError — Error, ocorre em uso indireto
// Se o <clinit> de OrderProcessor lançou RuntimeException na primeira chamada,
// toda tentativa subsequente de usar OrderProcessor lança NoClassDefFoundError,
// mesmo que o .class esteja no classpath.
OrderProcessor op = new OrderProcessor(); // ← pode lançar NoClassDefFoundError
```

**Fix:** para `ClassNotFoundException`, verifique o classpath/module path e adicione o jar faltante. Para `NoClassDefFoundError` causado por falha no `<clinit>`, inspecione a causa raiz — a JVM registra a exceção original; procure por `ExceptionInInitializerError` nos logs para encontrar o `<clinit>` que falhou.

## Em entrevista

### Frase pronta (inglês)

> "Class loading in the JVM is an on-demand process split into three phases: loading finds and creates the binary representation of the class; linking verifies the bytecode, allocates static fields with default values, and lazily resolves symbolic references; initialization runs the static initializer `<clinit>`. The key thing is that none of this happens until the class is actually needed."

> "The parent delegation model means that before a classloader tries to load a class itself, it delegates to its parent. The built-in hierarchy is bootstrap — which loads the core JDK modules like `java.base` — then platform, then the application classloader. This prevents application code from shadowing `java.lang.String` or any other core class, because the bootstrap loader always gets the first shot."

> "Class identity in the JVM is the pair of binary name plus defining classloader. The same fully qualified class name loaded by two different classloaders produces two distinct, incompatible types. This is the root cause of the 'impossible' `ClassCastException` you see in plugin systems or application servers — and it's also what makes classloader-based isolation work in the first place."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| carregamento de classes | class loading |
| modelo de delegação ao parent | parent delegation model |
| classloader de bootstrap | bootstrap class loader |
| classloader da plataforma | platform class loader |
| classloader da aplicação / sistema | application / system class loader |
| verificação (bytecode) | verification |
| preparação (campos estáticos) | preparation |
| resolução (referências simbólicas) | resolution |
| inicialização (bloco estático) | initialization / `<clinit>` |
| classloader definidor | defining class loader |
| classloader iniciador | initiating class loader |
| identidade de classe | class identity |

## Veja também

- [[01 - A JVM — o que é e o pipeline de execução]]
- [[02 - Áreas de memória de runtime]]
- [[04 - Bytecode por dentro — anatomia e javap]]
- [[08 - JPMS — o sistema de módulos]]
- [[03-Dominios/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#classloader (parent delegation)|classloader (Dicionário)]]

## Referências

- [java.lang.ClassLoader — Javadoc Java 21](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ClassLoader.html)
- [JVM Specification SE 21, Chapter 5 — Loading, Linking, and Initializing](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-5.html)
