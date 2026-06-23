---
title: "Method security — @PreAuthorize, @PostAuthorize e SpEL"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - seguranca
  - adepto
  - method-security
  - autorizacao
aliases:
  - "method security"
  - "@PreAuthorize"
---

# Method security — @PreAuthorize, @PostAuthorize e SpEL

> [!abstract] TL;DR
> Autorização no nível do método (`@PreAuthorize` / `@PostAuthorize`) é **mais granular** que a baseada em URL: a decisão pode olhar parâmetros e valor de retorno, coisa impossível na camada de requisição. Habilita-se com `@EnableMethodSecurity` (que já substituiu o antigo `@EnableGlobalMethodSecurity` e vem com `prePostEnabled` ligado por default). O mecanismo por baixo é o **proxy AOP do Spring** (Galho 8) — exatamente o mesmo que move o `@Transactional`. Por isso só funciona em método `public` chamado **de fora** do bean: em método `private`/`final` ou em self-invocation a anotação é ignorada silenciosamente.

## O que é

Method security é o conjunto de anotações do Spring Security que aplica regras de autorização **no método**, não na rota HTTP. Em vez de dizer "quem pode `POST /admin`", você diz "quem pode chamar `UserService.deleteUser(...)`".

As quatro anotações centrais:

- `@PreAuthorize` — avalia uma expressão **antes** de executar o método; se falhar, o método nem roda.
- `@PostAuthorize` — avalia **depois**, com acesso ao `returnObject` (o valor retornado).
- `@PreFilter` — filtra a **coleção de entrada** antes da execução.
- `@PostFilter` — filtra a **coleção de retorno** depois da execução.

Tudo escrito em **SpEL** (Spring Expression Language), o que permite expressões ricas como `hasRole('ADMIN') or #order.ownerId == authentication.principal.id`.

## Por que importa

A autorização baseada em URL (ver [[03-Dominios/Tecnologia/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Autorização baseada em URL]]) é **grossa**: ela só conhece o caminho e o método HTTP. Ela não sabe *qual* recurso está sendo acessado nem *quem* é o dono dele.

Method security resolve dois problemas que a URL não alcança:

1. **Autorização contextual** — "só o dono do pedido pode vê-lo" exige cruzar o usuário logado com o dado. Isso só dá pra fazer olhando o parâmetro (`#order`) ou o retorno (`returnObject`).
2. **Defesa em profundidade** — a regra fica colada na camada de serviço, então mesmo que um novo controller esqueça de proteger uma rota, o serviço continua negando. A proteção viaja com o método, não com a rota.

A documentação oficial recomenda method security justamente quando "os parâmetros do método e os valores de retorno contribuem para a decisão de autorização".

## Como funciona

### @EnableMethodSecurity (o que substituiu @EnableGlobalMethodSecurity)

A anotação atual é `@EnableMethodSecurity`. A doc oficial é explícita: ela **supersede** o antigo `@EnableGlobalMethodSecurity` (e o `<sec:global-method-security/>` do XML). Se você ver `@EnableGlobalMethodSecurity` num projeto, é código legado de versões anteriores ao Security 6.x.

```java
@Configuration
@EnableMethodSecurity
public class MethodSecurityConfig {
    // prePostEnabled já é true por default — nada a configurar
}
```

Por padrão (`prePostEnabled = true`), ela liga `@PreAuthorize`, `@PostAuthorize`, `@PreFilter` e `@PostFilter`. Internamente, o Spring registra interceptadores AOP — por exemplo:

```java
@Bean
static Advisor preAuthorizeMethodInterceptor() {
    return AuthorizationManagerBeforeMethodInterceptor.preAuthorize();
}
```

Esse `Advisor` é o elo direto com o Galho 8: a autorização é um **advice** aplicado por **proxy**.

### @PreAuthorize / @PostAuthorize: antes vs depois da execução

A diferença é puramente temporal, e ela tem consequências práticas.

- **`@PreAuthorize`** roda **antes**. A expressão tem acesso aos parâmetros (`#param`) e ao `authentication`, mas **não** ao retorno (ele ainda não existe). Use quando a decisão depende só de quem chama e do que foi passado.

- **`@PostAuthorize`** roda **depois**. Ganha acesso ao `returnObject` — o valor que o método produziu. Use quando você só consegue decidir *olhando o resultado*: por exemplo, carregar um pedido e só então verificar se o dono bate.

```java
@PostAuthorize("returnObject.ownerId == authentication.principal.id")
public Order readOrder(Long id) {
    // só retorna se o pedido pertencer ao usuário logado
}
```

A pegadinha: `@PostAuthorize` **executa o método inteiro** antes de negar. Se o método é caro (uma query pesada, uma chamada externa), você paga o custo mesmo para um acesso que será recusado. Mais sobre isso na seção Armadilhas, abaixo.

### @PreFilter / @PostFilter: filtrando coleções

Enquanto `@PreAuthorize`/`@PostAuthorize` decidem **sim ou não** para a chamada inteira, os filtros **podam coleções** elemento a elemento. Dentro da expressão, `filterObject` representa **cada item** da coleção.

- **`@PreFilter`** filtra a coleção que **entra** no método (parâmetros: arrays, collections, maps, streams).
- **`@PostFilter`** filtra a coleção que o método **retorna**.

```java
@PostFilter("filterObject.ownerId == authentication.principal.id")
public List<Order> listOrders() {
    // retorna todos; o filtro remove os que não são do usuário
}
```

O resultado: o chamador só vê os elementos que passaram na expressão. Os demais somem da lista silenciosamente — sem exceção.

### SpEL: hasRole, #param, authentication.principal, @bean

As expressões aceitam um vocabulário rico. Os mais usados:

| Expressão | O que faz |
|-----------|-----------|
| `hasRole('ADMIN')` | true se o usuário tem a role `ADMIN` (o prefixo `ROLE_` é adicionado automaticamente) |
| `hasAuthority('orders:read')` | true se tem a authority exata (sem prefixo) |
| `hasAnyRole('ADMIN','MANAGER')` | true se tem qualquer uma das roles |
| `#order` / `#id` | referencia um parâmetro do método pelo nome |
| `authentication` | o objeto `Authentication` completo |
| `principal` | atalho para `authentication.getPrincipal()` |
| `returnObject` | o valor retornado (só em `@PostAuthorize`) |
| `filterObject` | cada elemento (em `@PreFilter`/`@PostFilter`) |
| `@beanName.metodo(...)` | delega a decisão a um bean Spring — `@authz.check(authentication, #id)` |

> [!tip] `hasRole` vs `hasAuthority`
> `hasRole('ADMIN')` testa contra a authority `ROLE_ADMIN` (prefixo implícito). `hasAuthority('ROLE_ADMIN')` faz o mesmo, mas explícito. Para permissões sem prefixo (granulares, tipo `orders:read`), use `hasAuthority`. A distinção roles vs authorities está em [[03-Dominios/Tecnologia/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Autorização baseada em URL]].

A delegação `@bean` é a porta de entrada para autorização avançada (RBAC/ABAC com `AuthorizationManager`) — ver [[03-Dominios/Tecnologia/Java/Segurança/14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC|Autorização avançada]].

### URL-based (grossa) vs method-level (granular)

A doc oficial coloca as duas lado a lado:

| Aspecto | URL-based (request-level) | Method-level |
|---------|---------------------------|--------------|
| Granularidade | grossa (coarse-grained) | fina (fine-grained) |
| Onde se configura | classe de config (`HttpSecurity`) | na anotação, local ao método |
| Estilo | DSL | anotações + SpEL |
| Acesso a dados | só caminho + método HTTP | parâmetros **e** retorno |

As duas **coexistem**: a URL faz a triagem grossa (bloqueia rotas inteiras), e o método faz a decisão fina (cruza o usuário com o recurso). Não é "ou uma ou outra" — é defesa em camadas.

> [!important] A fronteira com o Galho 8 — o proxy AOP
> `@PreAuthorize` **não é mágica do compilador**: é um **proxy AOP** envolvendo o bean, **exatamente o mesmo mecanismo do `@Transactional`**. Quando outro bean chama `userService.deleteUser(...)`, a chamada passa pelo proxy, que roda o interceptador de autorização *antes* de delegar ao método real.
>
> A consequência direta dos **limites do proxy**:
> - método `private` ou `final` → o proxy não consegue interceptar → a anotação é **ignorada**;
> - **self-invocation** (um método do bean chama outro método anotado do *mesmo* bean via `this`) → a chamada **não passa pelo proxy** → a anotação é **ignorada**.
>
> Isso não é um detalhe de method security; é o comportamento universal dos proxies do Spring. A explicação completa está em [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]] e [[03-Dominios/Tecnologia/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]]. Se você já entende por que `@Transactional` falha em self-invocation, você já entende por que `@PreAuthorize` falha — é o mesmo proxy.

## Na prática

Configuração mínima e um serviço neutro com as três técnicas:

```java
@Configuration
@EnableMethodSecurity
public class MethodSecurityConfig {
    // prePostEnabled = true por default; nada mais a fazer
}
```

```java
@Service
public class UserService {

    // 1. Pré-autorização por role: só ADMIN pode deletar usuário
    @PreAuthorize("hasRole('ADMIN')")
    public void deleteUser(Long userId) {
        // ...
    }
}
```

```java
@Service
public class OrderService {

    // 2. Pré-autorização contextual: ADMIN OU o próprio dono do pedido.
    //    #order referencia o parâmetro; authentication.principal.id é o usuário logado.
    @PreAuthorize("hasRole('ADMIN') or #order.ownerId == authentication.principal.id")
    public void updateOrder(Order order) {
        // ...
    }

    // 3. Pós-filtro: retorna a lista completa, mas o chamador
    //    só enxerga os pedidos que são dele.
    @PostFilter("filterObject.ownerId == authentication.principal.id")
    public List<Order> listOrders() {
        return orderRepository.findAll();
    }
}
```

Note como a regra de negócio "só o dono vê seu pedido" vive colada ao serviço, escrita uma vez, e protege qualquer controller que chame esses métodos.

## Armadilhas

### (1) Esquecer `@EnableMethodSecurity` — falha silenciosa

Sem `@EnableMethodSecurity` em alguma `@Configuration`, **nenhuma** das anotações é processada. O pior: não há erro, não há log, não há exceção. As anotações `@PreAuthorize` ficam ali, parecendo proteção, mas o método executa para qualquer um. É uma falha de segurança que passa despercebida em testes felizes.

```java
// ❌ Configuração sem @EnableMethodSecurity
@Configuration
public class SecurityConfig {
    // @PreAuthorize em qualquer lugar do app: IGNORADO em silêncio
}
```

**Fix:** garanta a anotação numa classe de config e escreva um teste com um usuário **sem** a role esperada, afirmando que recebe `AccessDeniedException` (403). Um teste de negação é a única prova de que a proteção está ligada.

```java
@Configuration
@EnableMethodSecurity   // ✅
public class SecurityConfig { }
```

### (2) `@PreAuthorize` em método `private`/`final` ou self-invocation

Como method security roda sobre o **proxy AOP** (Galho 8), a anotação só é interceptada quando a chamada **atravessa o proxy**. Método `private` ou `final` não pode ser proxiado; e self-invocation (`this.metodo()`) chama o objeto real diretamente, pulando o proxy.

```java
@Service
public class OrderService {

    public void process(Order order) {
        archive(order);   // ❌ chamada interna via this → não passa pelo proxy
    }

    @PreAuthorize("hasRole('ADMIN')")   // IGNORADO quando chamado por process()
    public void archive(Order order) { /* ... */ }
}
```

**Fix:** torne o método `public` e invoque-o **de outro bean** (a chamada externa passa pelo proxy). Não re-explico o porquê aqui — o mecanismo de proxy e self-invocation está em [[03-Dominios/Tecnologia/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]].

### (3) `@PostAuthorize` carregando dado caro antes de negar

`@PostAuthorize` checa **depois** que o método rodou. Se o método faz trabalho pesado (query custosa, chamada a serviço externo) e a checagem nega, você pagou todo o custo para então devolver 403. Em métodos caros, isso é desperdício — e potencialmente um vetor de DoS.

```java
@PostAuthorize("returnObject.ownerId == authentication.principal.id")
public Order loadFullOrderWithItems(Long id) {
    // ❌ carrega pedido + itens + histórico... e só DEPOIS verifica o dono
}
```

**Fix:** quando der para decidir **antes** com os parâmetros, prefira `@PreAuthorize` — ele barra a chamada sem executar nada. Use `@PostAuthorize` apenas quando a decisão *realmente* depende do retorno e o custo de carregá-lo é aceitável.

```java
@PreAuthorize("@orderAuthz.isOwner(#id, authentication)")  // ✅ nega antes de carregar
public Order loadFullOrderWithItems(Long id) { /* ... */ }
```

## Em entrevista

### Frase pronta (inglês)

> Method security in Spring is annotation-based authorization at the service layer: `@PreAuthorize` runs before the method and `@PostAuthorize` runs after, with access to the return value, while `@PreFilter` and `@PostFilter` prune collections element by element. You enable it with `@EnableMethodSecurity`, which replaced the older `@EnableGlobalMethodSecurity` and ships with the pre/post annotations on by default. The crucial thing to understand is that it runs on Spring's AOP proxy — the exact same mechanism as `@Transactional` — so it only fires for public methods invoked from outside the bean. A `@PreAuthorize` on a private method, or one reached through self-invocation, is silently ignored, which is the number-one source of "why isn't my authorization working" bugs.

### Vocabulário

| Termo (EN) | PT-BR / sentido |
|------------|-----------------|
| method-level authorization | autorização no nível do método |
| fine-grained / coarse-grained | granularidade fina / grossa |
| AOP proxy | proxy de AOP (envolve o bean) |
| self-invocation | chamada interna (`this.metodo()`) |
| return value (`returnObject`) | valor de retorno acessível no pós |
| to prune a collection | podar/filtrar uma coleção |
| silently ignored | ignorado em silêncio (sem erro) |
| SpEL expression | expressão SpEL |

## Veja também

- [[03-Dominios/Tecnologia/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Autorização baseada em URL]]
- [[03-Dominios/Tecnologia/Java/Segurança/14 - Autorização avançada — AuthorizationManager, RBAC vs ABAC|Autorização avançada]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]]
- [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- [Spring Security Reference — Method Security](https://docs.spring.io/spring-security/reference/servlet/authorization/method-security.html) (consultado em 2026-06-10; baseline Security 6.x / Boot 3.x)
