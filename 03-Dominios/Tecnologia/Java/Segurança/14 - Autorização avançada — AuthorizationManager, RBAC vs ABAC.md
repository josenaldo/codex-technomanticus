---
title: "Autorização avançada — AuthorizationManager, RBAC vs ABAC"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - seguranca
  - magus
  - autorizacao
  - rbac
aliases:
  - "Autorização avançada"
  - "AuthorizationManager"
  - "RBAC vs ABAC"
---

# Autorização avançada — AuthorizationManager, RBAC vs ABAC

> [!abstract] TL;DR
> Quando `hasRole("ADMIN")` deixa de bastar — porque a decisão depende de *quem é o dono do recurso*, de *qual tenant*, de *qual atributo* — entra o `AuthorizationManager`. Ele é o ponto de extensão único do Spring Security 6.x para autorização: você escreve a lógica que quiser (acesso pelo dono, pelo tenant, por atributo) e pluga via `.access(authorizationManager)`. Em termos de modelo: **RBAC** (papéis → permissões) cobre a esmagadora maioria dos casos; **ABAC** decide por *atributos* (do usuário, do recurso, do contexto), geralmente via SpEL; **ReBAC** decide por *relacionamentos* (estilo Google Zanzibar — OpenFGA/SpiceDB) e brilha em compartilhamento estilo Drive. Escolha o modelo mais simples que o domínio aceita, e suba de degrau só quando a explosão de papéis doer.

## O que é

Autorização avançada é tudo o que vai *além* de "este endpoint exige o papel X". É a camada que decide acesso com base em dados que só existem em tempo de execução: o objeto sendo acessado, o usuário autenticado, o instante, o tenant. No Spring Security 6.x essa camada tem um único contrato central, o `AuthorizationManager<T>`, que substituiu o antigo par `AccessDecisionManager` + `AccessDecisionVoter`.

O `AuthorizationManager<T>` é genérico no *contexto* da decisão. Para autorização de requisições HTTP, esse contexto é o `RequestAuthorizationContext` (carrega o `HttpServletRequest` e as variáveis de path), de modo que você trabalha com `AuthorizationManager<RequestAuthorizationContext>`. A mesma interface, com outro `T`, serve para method security e domínios custom.

Os três modelos clássicos de controle de acesso — **RBAC**, **ABAC** e **ReBAC** — não são features do Spring; são *padrões de modelagem*. O `AuthorizationManager` é o mecanismo neutro que permite implementar qualquer um deles.

## Por que importa

O erro de carreira mais comum em segurança de aplicações é forçar RBAC onde o domínio pedia ABAC. O sintoma é a "explosão de papéis": começa com `ADMIN` e `USER`, e seis meses depois há `ADMIN_REGION_NORTE`, `ADMIN_REGION_SUL`, `EDITOR_PRODUTO_X`, `EDITOR_PRODUTO_Y`. Cada novo atributo do negócio vira uma combinação cartesiana de papéis, e a tabela de roles deixa de caber na cabeça de qualquer pessoa.

Entender quando subir de RBAC para ABAC (ou ReBAC) é o que diferencia o sênior. Numa entrevista internacional, "I'd model that with RBAC, but if access depends on resource ownership I'd switch to attribute-based decisions through a custom `AuthorizationManager`" é exatamente o tipo de resposta que mostra maturidade de design, não decoreba de anotação.

E importa pela testabilidade: lógica de autorização espremida dentro de SpEL gigante em `@PreAuthorize` é ilegível e difícil de cobrir com teste. Extrair para um `AuthorizationManager` devolve a decisão para uma classe Java comum — injetável, mockável, unit-testável.

## Como funciona

### AuthorizationManager + .access(): lógica de autorização custom

O contrato central, em Spring Security 6.x, é:

```java
public interface AuthorizationManager<T> {
    AuthorizationResult authorize(Supplier<Authentication> authentication, T object);

    default void verify(Supplier<Authentication> authentication, T object) {
        // chama authorize() e lança AccessDeniedException se negativo
    }
}
```

Pontos que valem ouro:

- A autenticação chega como `Supplier<Authentication>` — *preguiçoso de propósito*. Se a sua regra não precisar do usuário (ex.: liberar por IP), o `Authentication` nunca é resolvido, economizando trabalho.
- O `object` é o contexto tipado. Para HTTP, `RequestAuthorizationContext`, de onde você tira `context.getRequest()` e `context.getVariables()` (as variáveis de path, tipo `{id}`).
- O retorno é um `AuthorizationResult` (cuja implementação clássica é `AuthorizationDecision`): **positivo** concede, **negativo** nega, **null** *abstém* (passa a decisão adiante).

A documentação oficial é explícita: *"you can also implement a custom `AuthorizationManager` and you can put just about any access-control logic you want in it"*. Você pluga esse manager na cadeia de requisições com `.access(...)`:

```java
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/orders/{id}").access(orderAuthManager)
    .anyRequest().authenticated()
);
```

`hasRole(...)`, `hasAuthority(...)` e amigos são, por baixo, apenas `AuthorizationManager`s prontos. `.access(...)` é a porta para os seus.

### RBAC (roles → permissões): simples, cobre a maioria

**Role-Based Access Control**: o usuário recebe *papéis*, papéis carregam *permissões*, e a decisão é "o usuário tem o papel/permissão exigido?". É o `hasRole("ADMIN")` / `hasAuthority("order:read")` do dia a dia.

Vantagem: simples de entender, auditar e administrar. A maioria das aplicações de linha de negócio é, no fundo, RBAC. O bom design aqui é separar *papéis* (cargo: `ADMIN`, `MANAGER`) de *permissões* (verbo+recurso: `order:read`, `order:cancel`) e mapear papéis → permissões, autorizando endpoints pela permissão. Isso evita que cada endpoint conheça nomes de papéis.

RBAC quebra quando a decisão depende de *qual instância* do recurso — aí não é mais "pode ler pedidos?", é "pode ler *este* pedido?". Esse "este" é atributo, e atributo é território de ABAC.

### ABAC (atributos via SpEL): decisão por atributo do usuário/recurso/contexto

**Attribute-Based Access Control**: a decisão é uma função de *atributos* — do **usuário** (departamento, tenant), do **recurso** (dono, status, classificação) e do **contexto** (horário, IP). A pergunta deixa de ser "que papel ele tem?" e vira "os atributos batem?".

No Spring, o caminho leve para ABAC é SpEL com referência ao recurso — `#resource.ownerId == authentication.principal.id`. O caminho robusto, quando a regra cresce, é mover esses mesmos atributos para dentro de um `AuthorizationManager` Java, onde dá para testar e logar.

A regra de ouro: SpEL é ótimo para *expressar* a condição; ele é péssimo para *abrigar* lógica de negócio. Condição de uma linha, fica no SpEL; árvore de `if`, sai para o manager.

### ReBAC (Zanzibar — OpenFGA/SpiceDB): 'Alice compartilhou X com Bob' (menção)

**Relationship-Based Access Control**: a decisão deriva de um *grafo de relacionamentos*, não de papéis nem de atributos isolados. O caso canônico é compartilhamento estilo Google Drive: *"Alice compartilhou o documento X com Bob"* — Bob pode ler X não por ser admin, nem por um atributo dele, mas pela aresta `Bob —viewer→ X` que Alice criou.

O paper de referência é o **Google Zanzibar** (2019), e os motores open-source que o implementam são **OpenFGA** e **SpiceDB**. A ideia é externalizar a autorização para um serviço que mantém o grafo de tuplas de relacionamento e responde "Bob pode `view` X?" em milissegundos.

Para o nosso contexto (entrevista Java sênior) ReBAC é **menção culta**: você não precisa implementá-lo, mas saber que ele existe, que vem do Zanzibar e que resolve compartilhamento-em-grafo onde RBAC/ABAC ficariam intratáveis já é um diferencial. No Spring, integra-se via — adivinhe — um `AuthorizationManager` que consulta o motor externo.

### RoleHierarchy: ADMIN herda USER

Por padrão, papéis no Spring são *planos*: quem tem `ROLE_ADMIN` **não** tem `ROLE_USER` automaticamente. Para que `ADMIN` herde `USER`, declara-se uma hierarquia com `RoleHierarchyImpl`:

```java
@Bean
static RoleHierarchy roleHierarchy() {
    return RoleHierarchyImpl.withDefaultRolePrefix()
        .role("ADMIN").implies("STAFF")
        .role("STAFF").implies("USER")
        .build();
}
```

Isso estabelece `ROLE_ADMIN ⇒ ROLE_STAFF ⇒ ROLE_USER`: um usuário com `ROLE_ADMIN` é avaliado *como se* também tivesse `STAFF` e `USER`. A hierarquia vale tanto para filtro (`authorizeHttpRequests`) quanto para method security — neste último, conecta-se ao `MethodSecurityExpressionHandler` via `setRoleHierarchy(...)`.

## Na prática

Um `AuthorizationManager` custom que autoriza pelo *dono do recurso* — o dono do pedido só vê o próprio pedido — mais a hierarquia de papéis para que `ADMIN` passe por cima da checagem de posse.

```java
// 1) AuthorizationManager custom: dono do recurso (modelo ABAC, atributo ownerId)
@Component
public class OrderAuthorizationManager
        implements AuthorizationManager<RequestAuthorizationContext> {

    private final OrderRepository orders;

    public OrderAuthorizationManager(OrderRepository orders) {
        this.orders = orders;
    }

    @Override
    public AuthorizationResult authorize(
            Supplier<Authentication> authentication,
            RequestAuthorizationContext context) {

        // variável de path {id} de /api/orders/{id}
        String orderId = context.getVariables().get("id");

        Authentication auth = authentication.get();
        if (!(auth.getPrincipal() instanceof AppUser principal)) {
            return new AuthorizationDecision(false);
        }

        boolean isOwner = orders.findById(orderId)
            .map(order -> order.getOwnerId().equals(principal.getId()))
            .orElse(false);

        // equivale ao SpEL: #resource.ownerId == authentication.principal.id
        return new AuthorizationDecision(isOwner);
    }
}
```

```java
// 2) SecurityFilterChain: pluga o manager via .access(...) e a hierarquia de papéis
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(
            HttpSecurity http,
            OrderAuthorizationManager orderAuthManager) throws Exception {

        http.authorizeHttpRequests(auth -> auth
            // ADMIN entra direto (hierarquia abaixo cobre); demais, só o dono
            .requestMatchers("/api/orders/{id}").access(orderAuthManager)
            .anyRequest().authenticated()
        );
        return http.build();
    }

    @Bean
    static RoleHierarchy roleHierarchy() {
        // ROLE_ADMIN herda ROLE_USER: admin é avaliado como se tivesse USER
        return RoleHierarchyImpl.withDefaultRolePrefix()
            .role("ADMIN").implies("USER")
            .build();
    }
}
```

Repare: a regra "dono vê o próprio" virou uma classe Java testável, não um SpEL de três linhas. E a hierarquia mora num único `@Bean`, em vez de espalhar `hasAnyRole("ADMIN","USER")` por todo lado.

## Armadilhas

### (1) Lógica de negócio demais no SpEL

Empurrar regra de negócio para dentro de `@PreAuthorize` ou `.access(new WebExpressionAuthorizationManager("..."))` produz strings ilegíveis e impossíveis de testar isoladamente — o SpEL não tem stack trace decente, não tem breakpoint, e quebra em runtime, não na compilação.

**Exemplo (ruim):**
```java
@PreAuthorize("hasRole('MANAGER') and (#order.status == 'OPEN' or " +
              "(#order.region == authentication.principal.region and " +
              "#order.total < authentication.principal.approvalLimit))")
public void approve(Order order) { ... }
```

**Fix:** extraia para um `AuthorizationManager` (ou um bean de serviço chamado pelo SpEL, `@PreAuthorize("@orderRules.canApprove(#order)")`). A decisão volta a ser Java comum — testável, depurável, logável.

### (2) RBAC onde o domínio pedia ABAC

Insistir em papéis para expressar atributos gera a *explosão combinatória de roles*. Cada nova dimensão do negócio (região, produto, tenant) multiplica a quantidade de papéis.

**Exemplo (sintoma):**
```text
ROLE_ADMIN_REGION_X
ROLE_ADMIN_REGION_Y
ROLE_ADMIN_REGION_Z
ROLE_EDITOR_PRODUTO_A
ROLE_EDITOR_PRODUTO_B
...   // some 200 papéis depois
```

**Fix:** reconheça que "região" e "produto" são *atributos*, não papéis. Mantenha papéis grossos (`ADMIN`, `EDITOR`) e decida o resto por atributo num `AuthorizationManager` que compara `principal.getRegion()` com `resource.getRegion()`. Um papel `EDITOR` + um atributo de região derrota duzentos papéis.

### (3) Role hierarchy implícita esquecida

Desenvolvedores assumem que `ADMIN` "obviamente" inclui `USER`. **Não inclui.** Sem um bean `RoleHierarchy`, papéis são planos, e um endpoint protegido por `hasRole("USER")` *barra* um usuário que só tem `ROLE_ADMIN`.

**Exemplo (bug silencioso):**
```java
// endpoint exige USER; admin tem só ROLE_ADMIN → 403 inesperado
.requestMatchers("/profile").hasRole("USER")
```

**Fix:** declare a hierarquia explicitamente com `RoleHierarchyImpl...role("ADMIN").implies("USER").build()` e exponha-a como `@Bean`. Aí `ADMIN` passa a ser avaliado como se também tivesse `USER`. (Cuidado extra com method security: a hierarquia precisa ser ligada ao `MethodSecurityExpressionHandler` via `setRoleHierarchy`.)

## Em entrevista

### Frase pronta (inglês)

> RBAC handles the vast majority of authorization needs — you map users to roles, roles to permissions, and you're done. The moment access depends on the specific resource instance — say, the owner of an order can only see their own order — that's an attribute, and I switch to attribute-based decisions. In Spring Security 6 I implement that with a custom `AuthorizationManager<RequestAuthorizationContext>` plugged in via `.access(...)`, which keeps the logic in a testable Java class instead of a sprawling SpEL string. For relationship-heavy domains like document sharing, I'd reach for ReBAC — the Google Zanzibar model, with engines like OpenFGA or SpiceDB — and I never forget to declare a `RoleHierarchy` so that `ADMIN` actually inherits `USER`, since roles are flat by default.

### Vocabulário

| Termo (EN) | Tradução / sentido |
| --- | --- |
| role-based access control (RBAC) | controle de acesso por papéis |
| attribute-based access control (ABAC) | controle de acesso por atributos |
| relationship-based access control (ReBAC) | controle de acesso por relacionamentos |
| resource ownership | posse do recurso (quem é o dono) |
| role hierarchy | hierarquia de papéis (`ADMIN` herda `USER`) |
| role explosion | explosão de papéis (anti-padrão de RBAC) |
| to abstain (a decision) | abster-se (retornar `null`, passar adiante) |
| to grant / to deny access | conceder / negar acesso |

## Veja também

- [[03-Dominios/Tecnologia/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Autorização baseada em URL]]
- [[03-Dominios/Tecnologia/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL|Method security]]
- [[03-Dominios/Tecnologia/Java/Segurança/16 - OWASP Top 10 no contexto Java|OWASP Top 10 no contexto Java]]
- [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- Spring Security Reference — Authorization Architecture: https://docs.spring.io/spring-security/reference/servlet/authorization/architecture.html
