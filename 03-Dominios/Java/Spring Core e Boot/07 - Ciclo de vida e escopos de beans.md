---
title: "Ciclo de vida e escopos de beans"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - spring
  - adepto
  - beans
aliases:
  - "bean lifecycle"
  - "bean scopes"
---

# Ciclo de vida e escopos de beans

> [!abstract] TL;DR
> Todo bean Spring passa por fases ordenadas — instanciação, injeção de propriedades, callbacks *Aware*, `BeanPostProcessor`, inicialização (`@PostConstruct`) e, ao final, destruição (`@PreDestroy`). O **escopo** define quantas instâncias existem e por quanto tempo: `singleton` (padrão) cria uma única; `prototype` cria uma nova a cada solicitação; `request`/`session`/`application`/`websocket` limitam a instância à duração do contexto web correspondente. O ponto de tensão clássico é injetar um bean de vida curta (prototype, request) em um singleton — a solução passa por `ObjectProvider`, `@Lookup` ou scoped proxy com `proxyMode`.

## O que é

O **ciclo de vida** de um bean é a sequência de etapas que o container executa desde a criação até a destruição do objeto. O **escopo** complementa essa ideia definindo a política de reúso: quantas instâncias coexistem e qual é o gatilho para criar ou descartar cada uma.

Juntos, ciclo de vida e escopo determinam quando o código de inicialização roda, se o bean é compartilhado entre threads, se precisa ser thread-safe e como recursos são liberados.

## Por que importa

Um serviço que abre uma conexão no construtor e nunca a fecha vaza recursos silenciosamente. Um singleton que guarda estado mutável por requisição tem condição de corrida. Um prototype injetado ingenuamente em um singleton é sempre o mesmo objeto — exatamente o oposto do esperado.

Entender o ciclo de vida resolve o "onde coloco este código de inicialização?" (`@PostConstruct`, não no construtor). Entender escopos resolve o "por que meu bean de sessão tem dados de outro usuário?" (singleton injetando session-scoped sem proxy).

## Como funciona

### O ciclo de vida (instanciação → populate → *Aware → BeanPostProcessor → @PostConstruct/init → BPP → pronto → @PreDestroy/destroy)

O container executa estas etapas em ordem para cada bean gerenciado:

1. **Instanciação** — o construtor é chamado.
2. **Populate properties** — dependências e `@Value` são injetados via setter ou campo.
3. **Interfaces *Aware*** — o container chama `setBeanName()`, `setApplicationContext()` e outras interfaces `Aware` que o bean implementar, entregando infraestrutura interna.
4. **`BeanPostProcessor.postProcessBeforeInitialization()`** — ponto de extensão antes da inicialização (usado por AOP, `@Autowired`, etc.).
5. **Inicialização** — executa nesta ordem: `@PostConstruct`, `InitializingBean.afterPropertiesSet()`, `init-method` customizado.
6. **`BeanPostProcessor.postProcessAfterInitialization()`** — ponto de extensão após a inicialização; é aqui que proxies AOP são criados.
7. **Bean pronto** — disponível para uso pela aplicação.
8. **Destruição** — executa nesta ordem: `@PreDestroy`, `DisposableBean.destroy()`, `destroy-method` customizado.

> [!info] Callbacks recomendados
> Prefira `@PostConstruct` e `@PreDestroy` (JSR-250): são padrão Jakarta, não acoplam o código ao Spring e são suficientes para a grande maioria dos casos.

> [!warning] Inicialização e proxies AOP
> Os callbacks de inicialização rodam no bean **bruto**, antes do proxy AOP ser criado. Isso é intencional: garante que a inicialização opere no objeto real, não no proxy.

### Escopos (singleton default, prototype, request/session/application/websocket)

| Escopo | Instâncias | Duração | Contexto |
|---|---|---|---|
| `singleton` | Uma por container | Vida do container | Qualquer |
| `prototype` | Uma por solicitação | Até o cliente descartar | Qualquer |
| `request` | Uma por requisição HTTP | Duração da requisição | Web |
| `session` | Uma por sessão HTTP | Duração da sessão | Web |
| `application` | Uma por `ServletContext` | Vida da aplicação web | Web |
| `websocket` | Uma por sessão WebSocket | Duração da sessão WS | Web/STOMP |

**`singleton`** é o padrão. Significa "um por container Spring", não "um por JVM" (distinção em relação ao GoF Singleton).

**`prototype`** entrega uma nova instância a cada `getBean()` ou injeção. O container **não chama** callbacks de destruição em prototypes — a responsabilidade de limpeza é do código cliente.

Os escopos web (`request`, `session`, `application`, `websocket`) só funcionam em contextos que expõem o estado HTTP ao container (ex.: com `DispatcherServlet`, `RequestContextListener` ou `RequestContextFilter`). No Spring Boot, isso é configurado automaticamente.

Exemplo de declaração:

```java
@RequestScope
@Component
public class CarrinhoDaRequisicao {
    private final List<String> itens = new ArrayList<>();
    // Nova instância por request; descartada ao final
}

@SessionScope
@Component
public class PreferenciasDoUsuario {
    private String idioma = "pt-BR";
    // Uma instância por sessão HTTP
}
```

### Prototype em singleton: o problema e as saídas (ObjectProvider, @Lookup, scoped proxy)

Quando um bean `singleton` declara uma dependência `prototype`, o Spring a injeta **uma única vez** na criação do singleton. A partir daí, o singleton reutiliza sempre a mesma instância — o comportamento prototype se perde.

```java
@Component
public class Processador {         // singleton (padrão)

    @Autowired
    private Tarefa tarefa;         // prototype — mas injetado apenas uma vez!

    public void processar() {
        tarefa.executar();         // sempre a mesma instância: bug silencioso
    }
}
```

Há três saídas:

**Saída 1 — `ObjectProvider<T>`** (recomendada para prototypes)

```java
@Component
public class Processador {

    private final ObjectProvider<Tarefa> tarefaProvider;

    public Processador(ObjectProvider<Tarefa> tarefaProvider) {
        this.tarefaProvider = tarefaProvider;
    }

    public void processar() {
        Tarefa tarefa = tarefaProvider.getObject(); // nova instância a cada chamada
        tarefa.executar();
    }
}
```

**Saída 2 — `@Lookup`** (injeção de método)

```java
@Component
public abstract class Processador {

    public void processar() {
        Tarefa tarefa = criarTarefa();
        tarefa.executar();
    }

    @Lookup
    protected abstract Tarefa criarTarefa(); // Spring gera a implementação via CGLIB
}
```

**Saída 3 — scoped proxy** (para escopos web: request/session)

```java
@RequestScope(proxyMode = ScopedProxyMode.TARGET_CLASS)
@Component
public class ContextoDaRequisicao {
    // ...
}
```

O proxy é injetado no singleton; cada chamada ao proxy é roteada para a instância real do escopo corrente. Essa é a abordagem padrão para escopos web injetados em singletons.

## Na prática

Cenário: serviço que abre um recurso na inicialização e o libera ao encerrar, combinado com uso de `ObjectProvider` para um bean prototype.

```java
@Component
public class RelatorioService {

    private final ObjectProvider<RelatorioBuilder> builderProvider;
    private RelatorioConfig config;

    public RelatorioService(ObjectProvider<RelatorioBuilder> builderProvider) {
        this.builderProvider = builderProvider;
    }

    @PostConstruct
    public void init() {
        // Roda após injeção de dependências; container já está pronto
        this.config = RelatorioConfig.carregar();
        System.out.println("RelatorioService inicializado com config: " + config);
    }

    public String gerar(String tipo) {
        // Nova instância de RelatorioBuilder por chamada (escopo prototype)
        RelatorioBuilder builder = builderProvider.getObject();
        return builder.tipo(tipo).config(config).build();
    }

    @PreDestroy
    public void encerrar() {
        // Roda antes de o container descartar o bean
        if (config != null) {
            config.fechar();
        }
        System.out.println("RelatorioService encerrado");
    }
}
```

Pontos relevantes:
- `@PostConstruct` garante que `config` seja carregado **depois** que todas as dependências foram injetadas.
- `@PreDestroy` libera o recurso de forma ordenada quando o contexto fecha.
- `ObjectProvider.getObject()` entrega uma instância nova de `RelatorioBuilder` a cada chamada — correto para um bean prototype stateful.

## Armadilhas

### (1) Estado mutável em singleton sem thread-safety

Singletons são compartilhados entre threads. Campos mutáveis sem sincronização provocam condições de corrida sutis.

```java
@Service
public class ContadorService {          // singleton
    private int total = 0;             // PERIGOSO: threads concorrentes

    public void incrementar() {
        total++;                        // não é operação atômica
    }
}
```

**Fix**: use `AtomicInteger`, `volatile` com operações adequadas, ou redesenhe o serviço para ser stateless. Ver [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]].

### (2) Prototype injetado ingenuamente em singleton

Como descrito na seção anterior, a injeção direta de um prototype em um singleton congela a instância. O sintoma típico é: estado acumulado entre chamadas quando deveria ser zerado.

```java
@Autowired
private Tarefa tarefa; // prototype — mas o Spring injeta só na criação do singleton
```

**Fix**: use `ObjectProvider<Tarefa>`, `@Lookup` ou recupere pelo `ApplicationContext`.

### (3) Lógica pesada no construtor em vez de `@PostConstruct`

O construtor roda **antes** de o container injetar dependências. Qualquer lógica que dependa de campos injetados lança `NullPointerException` ou usa valores ainda nulos.

```java
@Service
public class RelatorioService {

    @Autowired
    private RelatorioDao dao;

    public RelatorioService() {
        List<?> dados = dao.listarTodos(); // ERRO: dao ainda é null aqui
    }
}
```

**Fix**: mova a lógica de inicialização para um método `@PostConstruct`. Para operações longas (carregamento de cache volumoso, conexões externas), considere `SmartInitializingSingleton` ou `@EventListener(ContextRefreshedEvent.class)` para não bloquear o lock de criação de singletons.

## Em entrevista

### Frase pronta (inglês)

"Every Spring bean goes through a well-defined lifecycle: instantiation, dependency injection, *Aware* callbacks, BeanPostProcessor hooks, then the init callback — `@PostConstruct` being the recommended one — and finally destruction via `@PreDestroy`. Scope controls how many instances exist: `singleton` gives one per container, `prototype` gives a new one per request, and the web scopes tie the instance to an HTTP request, session, or the ServletContext. The classic interview trap is the prototype-in-singleton problem: when a singleton holds a reference to a prototype bean, the prototype is injected only once and reused forever, defeating its purpose. The clean solutions are `ObjectProvider<T>`, which lets you pull a fresh instance on demand, `@Lookup` method injection, or a scoped proxy with `proxyMode = TARGET_CLASS` for web-scoped beans injected into singletons."

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| ciclo de vida do bean | bean lifecycle |
| escopo do bean | bean scope |
| singleton (por container) | singleton (per-container) |
| prototype | prototype |
| escopo de requisição | request scope |
| escopo de sessão | session scope |
| proxy com escopo | scoped proxy |
| callback de inicialização | initialization callback |
| callback de destruição | destruction callback |
| injeção de método | method injection |
| provedor de objeto | object provider |
| interface consciente | Aware interface |

## Veja também

- [[03-Dominios/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext — o container e seu ciclo]] — o container que orquestra todo o ciclo de vida descrito aqui
- [[03-Dominios/Java/Spring Core e Boot/13 - BeanPostProcessor e BeanFactoryPostProcessor|BeanPostProcessor e BeanFactoryPostProcessor]] — os pontos de extensão que interceptam as fases de inicialização
- [[03-Dominios/Java/Jakarta EE/05 - CDI — escopos e contextos|CDI — escopos e contextos]] — a spec Jakarta tem a mesma tensão de escopo e usa client proxies; mecanismo próprio do CDI, independente do Spring
- [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] — essencial para singletons com estado mutável
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#bean scope (Spring)|bean scope (Spring)]]

## Referências

- Spring Framework Reference — Bean Scopes: https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html
- Spring Framework Reference — Lifecycle Callbacks: https://docs.spring.io/spring-framework/reference/core/beans/factory-nature.html
