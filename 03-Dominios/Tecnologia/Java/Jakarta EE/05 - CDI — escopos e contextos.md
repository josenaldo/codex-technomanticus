---
title: "CDI — escopos e contextos"
created: 2026-06-07
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - jakarta-ee
  - adepto
  - cdi
aliases:
  - "Escopos CDI"
  - "Client proxy"
  - "@ApplicationScoped"
---

# CDI — escopos e contextos

> [!abstract] TL;DR
> O **escopo** define _quando_ o container cria e descarta um bean — uma instância por aplicação, por requisição, por sessão. Os **escopos normais** (`@ApplicationScoped`, `@RequestScoped`, `@SessionScoped`, `@ConversationScoped`) são entregues via **client proxy**: você nunca segura a instância real, e sim um intermediário que resolve o contexto ativo a cada chamada de método. Esse detalhe explica meia dúzia de comportamentos "mágicos" — por que classe `final` quebra o deployment, por que a instância só nasce na primeira chamada (lazy), e por que injetar um bean request-scoped dentro de um application-scoped simplesmente funciona.

## O que é

Na nota anterior ([[04 - CDI — beans e injeção]]) vimos o **DI** da sigla CDI. Esta nota é sobre o **C**: _Contexts_.

Um **contexto** é a estrutura que o container mantém para gerenciar o ciclo de vida das instâncias de um escopo. A spec CDI 4.1 (§6.3) define o contexto de um escopo normal como **um mapeamento de cada tipo de bean daquele escopo para uma instância** — e esse mapeamento é o que vive e morre junto com a requisição, a sessão ou a aplicação. Cada escopo tem o seu contexto:

- O **contexto de aplicação** vive enquanto a aplicação estiver no ar.
- O **contexto de requisição** nasce quando uma requisição chega e morre quando ela termina.
- O **contexto de sessão** acompanha a sessão HTTP do usuário.
- O **contexto de conversação** delimita uma "conversa" (várias requisições agrupadas, ex.: um wizard de checkout).

Pense no contexto como uma **prateleira temporária**: o container guarda ali a instância do bean enquanto o escopo estiver ativo, e quando o escopo acaba, varre a prateleira inteira — chamando `@PreDestroy` em cada instância antes de descartar.

Quando uma classe não declara escopo nenhum, o default é `@Dependent` (spec §2.4.4) — e veremos adiante por que isso surpreende muita gente.

## Por que importa

**Escopo errado é a categoria de bug mais sorrateira do CDI.** Dois sintomas clássicos, em direções opostas:

- **Estado vazando:** um bean `@ApplicationScoped` com um campo mutável que deveria ser por usuário — de repente o carrinho do cliente A aparece pro cliente B. Uma instância só, compartilhada por todas as threads e usuários.
- **Estado sumindo:** um bean `@Dependent` (o default!) que você achava que era singleton — cada ponto de injeção recebe uma instância nova, e aquele cache que você populou num lugar está vazio no outro.

Além disso, entender o **client proxy** desmistifica comportamentos que parecem mágica em qualquer container de DI — os frameworks construídos sobre essas ideias (veja [[03-Dominios/Tecnologia/Java/Spring Core e Boot/07 - Ciclo de vida e escopos de beans|escopos no Spring]]) reaproveitam o mesmo raciocínio. E em entrevista de nível sênior, a pergunta favorita é exatamente: **"como pode um bean request-scoped ser injetado num application-scoped sem vazar entre requisições?"** A resposta — _porque a referência injetada é um proxy, não a instância_ — separa quem usou o framework de quem entendeu o framework.

## Como funciona

### Os escopos normais: quando usar cada um

A spec define quatro escopos normais embutidos (pacote `jakarta.enterprise.context`):

| Escopo | Tempo de vida | Quando usar |
|---|---|---|
| `@ApplicationScoped` | Uma instância por aplicação | Serviços sem estado por usuário, caches compartilhados, configuração |
| `@RequestScoped` | Uma instância por requisição | Estado da requisição corrente (dados do request, contexto de auditoria) |
| `@SessionScoped` | Uma instância por sessão HTTP | Estado por usuário entre requisições (carrinho, preferências) |
| `@ConversationScoped` | Uma instância por conversação (delimitada pelo app) | Fluxos multi-página (wizard, checkout em etapas) |

Os dois últimos pertencem ao **CDI Full** (perfis web/platform); `@RequestScoped` e `@ApplicationScoped` existem também no **CDI Lite** (o subconjunto pensado para build-time, usado por runtimes como Quarkus).

Visualizando os tempos de vida:

```text
aplicação    |=============================================|  @ApplicationScoped
sessão (u1)  |   |=====================================|    |  @SessionScoped
conversação  |   |        |==========|                 |    |  @ConversationScoped (begin..end)
requisições  |   |req|  |req|  |req|  |req|            |    |  @RequestScoped
             |   '---'  '---'  '---'  '---'            |    |
@Dependent: nasce e morre junto com QUEM o injetou (sem linha própria)
```

O `@ConversationScoped` merece um parêntese: por padrão a conversação é **transiente** (dura uma requisição). O container fornece um bean embutido `Conversation` (request-scoped, nome `jakarta.enterprise.context.conversation`) com `begin()` e `end()` para promovê-la a **long-running** — aí ela atravessa múltiplas requisições até `end()` ou timeout.

### `@Dependent`: o pseudo-escopo

Nem todo escopo é normal. A spec (§6.3) divide os escopos em dois grupos:

- **Escopos normais** — declarados com a meta-anotação `@NormalScope`, que sinaliza ao container: _este escopo exige client proxy_.
- **Pseudo-escopos** — declarados com `@jakarta.inject.Scope`, sem proxy. O único embutido é o `@Dependent`.

`@Dependent` significa: **a instância pertence a quem a injetou**. A spec (§6.4) é taxativa:

- Nenhuma instância injetada é compartilhada entre dois pontos de injeção.
- A instância fica amarrada ao ciclo de vida do objeto que a recebeu — criada junto, destruída junto.
- Cada `get()` no contexto `@Dependent` retorna uma **instância nova**.

A analogia: um bean de escopo normal é um **serviço público** — todo mundo que liga pro mesmo número fala com a "mesma" entidade. Um bean `@Dependent` é um **acessório descartável** — cada cliente recebe o seu, e ele vai pro lixo junto com o dono.

Como não há proxy, a referência injetada de um `@Dependent` **é a instância real**. Isso tem um efeito colateral útil: classes `final` podem ser `@Dependent` sem problema — a restrição de proxy não se aplica.

### Client proxy: o mecanismo por trás dos escopos normais

Aqui está o coração da nota. Quando você injeta um bean de escopo normal, **a referência que você recebe não é a instância do bean** — é um **client proxy**: um objeto gerado pelo container que implementa/estende os tipos do bean e **delega cada chamada de método à instância corrente** do contexto ativo (spec §5.4).

A sequência, a cada chamada de método (spec §5.4.1):

```text
seu código ──> [client proxy] ──1──> "qual é o contexto ativo deste escopo AGORA?"
                              ──2──> obtém (ou cria) a instância corrente nesse contexto
                              ──3──> delega a chamada à instância real
```

Por que essa indireção? A spec lista as razões — e a primeira é a que cai em entrevista:

1. **Garantia de instância corrente.** Se um bean `@RequestScoped` é injetado num `@ApplicationScoped`, o campo é preenchido **uma vez** (na criação do bean application-scoped), mas precisa apontar pra instância da **requisição atual** a cada uso. Só uma referência indireta resolve isso: o proxy é fixo, mas o alvo muda a cada requisição.
2. **Dependências circulares.** O proxy permite quebrar ciclos na construção do grafo de beans.
3. **Lazy instantiation.** Como o proxy só resolve a instância na primeira chamada de método, o bean real pode nem existir ainda quando foi "injetado" — a criação é adiada até o primeiro uso de verdade.

Esse mecanismo impõe restrições. A spec (§3.10, _Unproxyable bean types_) lista os tipos que o container **não consegue proxiar**:

- classes **sem construtor não-privado sem parâmetros**;
- classes declaradas **`final`**;
- classes com **métodos `final` não-estáticos** de visibilidade `public`, `protected` ou default;
- classes e interfaces **`sealed`**;
- tipos primitivos;
- tipos array.

Se um ponto de injeção que exige proxy resolve para um bean com tipo improxiável, o container **detecta automaticamente e trata como problema de deployment** — a aplicação nem sobe. A API define `jakarta.enterprise.inject.UnproxyableResolutionException` exatamente para esse caso.

> [!question] Por que `final` quebra?
> Porque o proxy de uma classe concreta é gerado **por subclasse**: o container cria em runtime (ou build-time) uma classe `CartService$Proxy extends CartService` que sobrescreve os métodos para delegar. `final` proíbe herança/sobrescrita — logo, não há como gerar o proxy. Beans expostos por **interface** escapam de parte das restrições, porque proxiar interface não exige herança da implementação.

### Ciclo de vida: `@PostConstruct` e `@PreDestroy`

O container constrói a instância em três tempos: **construtor → injeção de dependências → `@PostConstruct`**. Na destruição (quando o contexto do escopo acaba), roda o **`@PreDestroy`** antes do descarte.

A consequência prática: **o construtor não é o lugar de inicialização pesada**. Dois motivos:

1. No construtor, **as dependências injetadas por campo ainda não chegaram** — usar um campo `@Inject` ali dá `NullPointerException`.
2. O container (e o proxy) podem instanciar a classe em momentos que você não controla — a subclasse de proxy, por exemplo, também invoca o construtor da superclasse. Lógica pesada no construtor roda em horas inesperadas.

A regra de ouro: **construtor só atribui; `@PostConstruct` inicializa**. E graças à lazy instantiation via proxy, o `@PostConstruct` de um bean de escopo normal só roda na **primeira chamada real de método** — não no deploy, não na injeção.

O container ainda emite eventos de ciclo de contexto que você pode observar: `@Initialized(RequestScoped.class)`, `@BeforeDestroyed(...)` e `@Destroyed(...)` — úteis para ganchos de início/fim de requisição sem servlet listener. (Eventos são o tema de [[06 - CDI — qualifiers, producers e eventos]].)

### Escopo ativo e `ContextNotActiveException`

Um contexto não existe o tempo todo — ele está **ativo** ou não. O contexto de requisição, por exemplo, está ativo durante o processamento de uma requisição (e a spec Lite acrescenta: durante notificação de observer assíncrono e durante callbacks `@PostConstruct`).

Quando o proxy tenta resolver a instância e **não há contexto ativo** para o escopo, a spec (§6.5.1) manda lançar **`jakarta.enterprise.context.ContextNotActiveException`**. O caso clássico: acessar um bean `@RequestScoped` de uma thread que você mesmo criou — a requisição "pertence" à thread do servidor; a sua thread nova não tem contexto de requisição nenhum.

Repare no detalhe sutil: a exceção estoura **na chamada do método**, não na injeção. A injeção sempre "funciona" (é só o proxy); o erro aparece depois, no primeiro uso fora de contexto — o que torna o stack trace menos óbvio de rastrear.

### Passivação: por que `Serializable` em session e conversation

Sessões HTTP podem ser **passivadas**: a spec (§17.5) define passivação como "a transferência temporária do estado de um objeto ocioso da memória para armazenamento secundário" (disco, outro nó do cluster). Quando o servidor passiva uma sessão, os beans `@SessionScoped` e `@ConversationScoped` pendurados nela vão junto — serializados.

Por isso a spec declara session e conversation como **passivating scopes** (`@NormalScope(passivating = true)`) e exige que os beans desses escopos sejam **passivation capable**: para um managed bean, isso significa que **a classe do bean é `Serializable`** (e seus interceptors/decorators também). O container **valida no deployment**: bean com escopo passivante que não é passivation capable = problema de deployment, a aplicação não sobe.

Nenhum outro escopo embutido é passivante — `@ApplicationScoped` e `@RequestScoped` não exigem `Serializable`.

## Na prática

O cenário canônico: um carrinho por sessão de usuário, consumido por um serviço único da aplicação.

```java
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import jakarta.enterprise.context.SessionScoped;

@SessionScoped
public class CartService implements Serializable { // Serializable: escopo passivante

    private List<String> items;

    public CartService() {
        // só atribuições triviais aqui — o proxy também passa por este construtor
        System.out.println("construtor: pode rodar mais de uma vez (proxy + instância real)");
    }

    @PostConstruct
    void init() {
        // roda UMA vez por instância real, na PRIMEIRA chamada de método via proxy
        this.items = new ArrayList<>();
        System.out.println("@PostConstruct: a sessão " + hashCode() + " ganhou um carrinho");
    }

    @PreDestroy
    void cleanup() {
        // roda quando a sessão HTTP expira/invalida
        System.out.println("@PreDestroy: sessão acabou, descartando " + items.size() + " itens");
    }

    public void add(String sku) {
        items.add(sku);
    }

    public List<String> items() {
        return List.copyOf(items);
    }
}
```

Agora o consumidor — repare na assimetria de escopos que "não deveria funcionar":

```java
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

@ApplicationScoped
public class CheckoutService {

    @Inject
    CartService cart; // NÃO é a instância: é um client proxy

    public void checkout(String sku) {
        // a CADA chamada, o proxy resolve o CartService da SESSÃO CORRENTE.
        // Usuário A e usuário B passam por este MESMO CheckoutService,
        // mas cada um enxerga o SEU carrinho.
        cart.add(sku);
    }
}
```

`CheckoutService` é um só para a aplicação inteira; `cart` foi injetado uma única vez. Mesmo assim, cada usuário vê o próprio carrinho — porque `cart` é um proxy que pergunta "qual é a sessão desta requisição?" a cada chamada. Sem proxy, o primeiro usuário a tocar o `CheckoutService` "congelaria" o carrinho dele para todos os demais.

A lazy instantiation aparece nos logs: o `@PostConstruct` do `CartService` **não** roda quando o `CheckoutService` é criado, nem quando a sessão começa — só quando `cart.add(...)` é chamado pela primeira vez naquela sessão.

E o contraexemplo — classe `final` com escopo normal:

```java
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public final class OrderCodeGenerator { // final + escopo normal = improxiável

    public String next() {
        return "ORD-" + System.nanoTime();
    }
}
```

A spec classifica isso como **problema de deployment**: o container detecta o tipo improxiável na validação e a aplicação falha ao subir. No Weld (implementação de referência), o erro reportado envolve uma `UnproxyableResolutionException` indicando que o tipo do bean de escopo normal não pode ser proxiado — a mensagem exata varia por versão, mas a categoria é esta:

```text
DEPLOY: falha na validação do deployment
  jakarta.enterprise.inject.UnproxyableResolutionException:
  bean de escopo normal com tipo improxiável (classe final) — ver spec CDI §3.10
```

Os fixes possíveis: remover o `final` da classe, expor o bean por uma **interface**, ou — se uma instância por consumidor for aceitável — rebaixar para `@Dependent`, que dispensa proxy.

## Armadilhas

### (1) `@Dependent` achando que é singleton

O escopo **default** é `@Dependent`, não `@ApplicationScoped`. Quem esquece a anotação ganha uma instância nova **por ponto de injeção** — e o estado "some" misteriosamente.

```java
// SEM anotação de escopo => @Dependent
public class SkuCache {
    private final Map<String, String> cache = new HashMap<>();
    public void put(String k, String v) { cache.put(k, v); }
    public String get(String k) { return cache.get(k); }
}
```

O `ServiceA` popula o cache; o `ServiceB` lê e está sempre vazio — porque cada um recebeu **o seu** `SkuCache`. Não é bug de concorrência, não é limpeza prematura: são duas instâncias.

**Fix:** anote explicitamente o escopo pretendido — `@ApplicationScoped` para um cache compartilhado. Regra prática: **nunca confie no default**; declare o escopo de todo bean com estado.

### (2) Inicialização pesada no construtor

```java
@ApplicationScoped
public class CatalogService {
    private final List<Product> catalog;

    public CatalogService() {
        this.catalog = loadFromDatabase(); // ERRADO: roda em momentos fora do seu controle
    }
}
```

Três problemas: dependências `@Inject` por campo ainda são `null` no construtor; o container/proxy pode invocar o construtor mais vezes ou em momentos que você não prevê (a subclasse de proxy também o atravessa); e a falha numa carga pesada no construtor vira erro de instanciação difícil de diagnosticar.

**Fix:** construtor só atribui; mova a carga para um método `@PostConstruct` — que roda exatamente uma vez por instância real, após a injeção completa.

### (3) `@SessionScoped` sem `Serializable`

```java
@SessionScoped
public class UserPreferences { /* sem implements Serializable */ }
```

Session e conversation são **escopos passivantes**: a spec exige beans **passivation capable**, e para managed beans isso significa classe `Serializable`. O container valida no deployment e trata a violação como problema de deployment — a aplicação não sobe (e se subisse, a passivação da sessão num cluster estouraria na serialização).

**Fix:** `implements Serializable` — e atenção aos **campos**: dependências injetadas em beans passivantes também precisam ser passivation capable (beans de escopo normal sempre são, porque o que se serializa é o proxy; o perigo são campos `@Dependent` ou objetos crus não-serializáveis). Campo que não deve ser serializado: marque `transient` e reconstrua no `@PostConstruct`... mas lembre que `@PostConstruct` não roda de novo na ativação.

### (4) Acessar bean request-scoped de uma thread própria

```java
@ApplicationScoped
public class ReportService {

    @Inject
    RequestAudit audit; // @RequestScoped

    public void generateAsync() {
        new Thread(() -> {
            audit.log("gerando relatório"); // ContextNotActiveException!
        }).start();
    }
}
```

O contexto de requisição está associado à thread que processa a requisição. A thread nova não tem contexto ativo — o proxy tenta resolver a instância corrente, não encontra contexto, e lança `ContextNotActiveException`. **Propagação de contexto não é automática** entre threads.

**Fix:** capture os dados necessários **antes** de despachar para outra thread (passe valores, não beans com escopo), ou use os mecanismos de propagação de contexto do seu runtime (ex.: Jakarta Concurrency / MicroProfile Context Propagation). Sobre threads, executors e os perigos de criar `Thread` na mão, o assunto já foi tratado em [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência (Galho 4)]] — aqui basta a regra: **escopo CDI não atravessa thread sozinho**.

## Em entrevista

### Frase pronta (inglês)

> "In CDI, a scope defines when the container creates and destroys a bean, and each scope is backed by a context. Normal scopes like application, request and session are delivered through a client proxy: the injected reference is never the actual instance, but a proxy that resolves the current contextual instance on every method call. That's why injecting a request-scoped bean into an application-scoped one works safely — the proxy re-resolves the right instance per request — and it's also why normal-scoped beans can't be final and are instantiated lazily on first use. Session and conversation scopes are passivating, so their beans must be serializable, and accessing a scoped bean from a thread without an active context throws ContextNotActiveException."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| escopo | scope |
| contexto ativo | active context |
| escopo normal | normal scope |
| pseudo-escopo | pseudo-scope |
| proxy de cliente | client proxy |
| instância corrente | current instance |
| tipo improxiável | unproxyable bean type |
| instanciação preguiçosa | lazy instantiation |
| passivação / capaz de passivação | passivation / passivation capable |
| escopo passivante | passivating scope |

## Veja também

- [[04 - CDI — beans e injeção]] — a base: managed beans, `@Inject`, typesafe resolution
- [[06 - CDI — qualifiers, producers e eventos]] — inclusive os eventos `@Initialized`/`@Destroyed` de contexto
- [[13 - CDI avançado — interceptors, decorators e extensões]] — interceptors também dependem de proxy
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência (Galho 4)]] — threads, executors e por que contexto não se propaga sozinho
- [[03-Dominios/Tecnologia/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#escopo (CDI)|escopo (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#client proxy (CDI)|client proxy (Dicionário)]]

## Referências

- [Jakarta CDI 4.1 — página da especificação](https://jakarta.ee/specifications/cdi/4.1/) — acesso em 2026-06-07
- [Jakarta CDI 4.1 — documento da spec (scopes & contexts: §2.4, §3.10, §5.4, §6.3–6.6, §17.5–17.6)](https://jakarta.ee/specifications/cdi/4.1/jakarta-cdi-spec-4.1) — acesso em 2026-06-07
- [Jakarta CDI 4.1 — apidocs, pacote `jakarta.enterprise.context`](https://jakarta.ee/specifications/cdi/4.1/apidocs/jakarta/enterprise/context/package-summary.html) — acesso em 2026-06-07
- [Jakarta CDI 4.1 — apidocs, `UnproxyableResolutionException`](https://jakarta.ee/specifications/cdi/4.1/apidocs/jakarta/enterprise/inject/UnproxyableResolutionException.html) — acesso em 2026-06-07
