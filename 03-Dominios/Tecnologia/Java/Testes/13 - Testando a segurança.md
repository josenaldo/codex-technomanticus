---
title: "Testando a segurança"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - testes
  - magus
  - spring-test
aliases:
  - "testando segurança"
  - "@WithMockUser"
---

# Testando a segurança

> [!abstract] TL;DR
> O `spring-security-test` injeta uma identidade simulada nos seus testes: `@WithMockUser` define roles e username no `SecurityContext`, `with(jwt())` simula o fluxo de Resource Server (token já validado), e `with(csrf())` injeta o token CSRF esperado. Você dispara requests pelo MockMvc com essa identidade no contexto e assere o resultado: **401** quando ninguém está autenticado, **403** quando alguém autenticado não tem autorização. Method security (`@PreAuthorize`) só dispara nos testes se o slice habilitar a anotação.

## O que é

Testar a segurança é exercitar o que o [[03-Dominios/Tecnologia/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|Galho 12]] construiu: o filter chain decide quem entra (autenticação) e o que pode fazer (autorização). O problema é que, num teste, não há browser, não há login form, não há token real assinado por um provedor. Você precisa de um jeito de dizer "finja que este request veio de um ADMIN autenticado" sem subir o fluxo inteiro de login.

É exatamente isso que a biblioteca `spring-security-test` faz. Ela oferece dois mecanismos complementares:

- **Anotações** (`@WithMockUser`, `@WithUserDetails`) que populam o `SecurityContext` **antes** do método de teste rodar, declarativamente.
- **Request post-processors** (`jwt()`, `csrf()`, `user()`) que se acoplam ao `MockMvcRequest` via `.with(...)`, modificando o request **na hora do disparo**.

Os dois caminhos terminam no mesmo lugar: um `Authentication` populado no contexto, exatamente como se o filter chain real tivesse autenticado o usuário. O que o teste de fato verifica é a camada de **autorização** — se as regras de `authorizeHttpRequests` e os `@PreAuthorize` respondem corretamente a uma identidade conhecida.

```xml
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-test</artifactId>
    <scope>test</scope>
</dependency>
```

## Por que importa

Segurança é a feature em que um falso negativo no teste vira um CVE em produção. Você pode ter o `SecurityFilterChain` mais bem desenhado do mundo, mas se nenhum teste prova que `/admin` realmente bloqueia um `USER`, você está confiando em fé. E configuração de segurança quebra silenciosamente: um `requestMatchers` na ordem errada, um `permitAll()` esquecido num path novo, um `@PreAuthorize` com SpEL inválido que só falha em runtime.

Testar a segurança também é o ponto onde slices de teste e config de segurança colidem. Um `@WebMvcTest` carrega a config de segurança por padrão (diferente de não carregar services), então um teste de controller que ignorava 401 de repente começa a falhar — e isso é um sintoma, não um bug. Esta nota é a face do [[03-Dominios/Tecnologia/Java/Testes/index|galho de Testes]] que paga a dívida deixada pelo capstone do Galho 12: a stack que testa aquela segurança vive aqui.

## Como funciona

### @WithMockUser / @WithUserDetails: identidade simulada

`@WithMockUser` é a forma mais barata de ter um usuário autenticado num teste. Ela roda **antes** do método (via `TestExecutionListener`) e injeta um `Authentication` no `SecurityContext` com username, password e authorities fabricados:

```java
@WithMockUser(username = "alice", roles = "ADMIN")
```

Detalhe que pega: `roles = "ADMIN"` vira a authority `ROLE_ADMIN` (o prefixo é adicionado), enquanto `authorities = "ORDER_READ"` entra **literal**, sem prefixo. Essa distinção entre role e authority é do [[03-Dominios/Tecnologia/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Galho 12]] — aqui só observamos a consequência: usar a chave errada faz o teste passar/falhar pelo motivo errado.

`@WithUserDetails`, por outro lado, **não fabrica** o usuário: ela busca por username no seu `UserDetailsService` real, carregando o usuário como ele existe na aplicação (com as authorities reais, password encoder real, etc.). Use `@WithMockUser` quando a identidade é descartável e `@WithUserDetails` quando você quer testar contra um usuário de verdade do seu domínio.

Ambas funcionam tanto em method security (sem MockMvc) quanto em testes MockMvc — o `SecurityContext` é o canal comum.

### with(jwt()) / with(csrf()): os post-processors do MockMvc

Quando a identidade depende do request (ou você quer simular um fluxo OAuth2 sem assinar token de verdade), os post-processors são o caminho. Eles vêm de:

```java
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;
```

e se aplicam ao request com `.with(...)`:

- `with(jwt())` — simula um Resource Server: injeta um `JwtAuthenticationToken` no contexto **sem validar assinatura nem chamar o decoder**. Você customiza claims e authorities: `with(jwt().jwt(j -> j.claim("sub", "alice")).authorities(new SimpleGrantedAuthority("SCOPE_orders:read")))`. Isso testa a autorização da [[03-Dominios/Tecnologia/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|API como Resource Server]] sem precisar de um provedor de identidade.
- `with(csrf())` — injeta o token CSRF que o filtro espera num request mutante (POST/PUT/DELETE). Sem ele, um endpoint com CSRF ligado retorna 403 mesmo com usuário autenticado.
- `with(user("bob").roles("USER"))` — equivalente imperativo de `@WithMockUser`, útil quando o usuário varia dentro do mesmo método de teste.

Post-processors compõem: `.with(jwt()).with(csrf())` aplica os dois. A regra mental é "anotação para o caso fixo do método, post-processor para o caso que varia por request".

### Testar 401 vs 403 (não-autenticado vs não-autorizado)

A distinção é o coração do teste de autorização e os dois códigos significam coisas diferentes:

- **401 Unauthorized** — *ninguém está autenticado*. Não há identidade no contexto. Você reproduz isso disparando o request **sem** `@WithMockUser` e **sem** post-processor de auth. O filter chain rejeita antes de chegar ao handler.
- **403 Forbidden** — *há um usuário autenticado, mas ele não tem a autoridade necessária*. Você reproduz autenticando com a role **errada**: `@WithMockUser(roles = "USER")` batendo num endpoint que exige `ADMIN`.

```java
mockMvc.perform(get("/admin")).andExpect(status().isUnauthorized());        // 401: sem auth

mockMvc.perform(get("/admin").with(user("u").roles("USER")))               // 403: autenticado, sem role
       .andExpect(status().isForbidden());
```

Confundir os dois é o erro clássico (ver Armadilhas). Um teste que espera 403 mas recebe 401 está, na verdade, dizendo "eu esqueci de autenticar".

### Testar method security (@PreAuthorize)

Há dois jeitos de exercitar [[03-Dominios/Tecnologia/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL|method security]]:

1. **Via MockMvc** — bate no endpoint que chama o método protegido. Funciona se o slice carregar a config de method security.
2. **Direto no bean** — sem MockMvc nenhum, injeta o service e chama o método com `@WithMockUser` ativo. Aqui o `@PreAuthorize` é avaliado pelo `MethodSecurityInterceptor` no proxy do bean:

```java
@Test
@WithMockUser(authorities = "ORDER_DELETE")
void deletaOrderComAuthority() {
    orderService.delete(42L); // passa
}

@Test
@WithMockUser(roles = "USER")
void deleteSemAuthorityLancaAccessDenied() {
    assertThatThrownBy(() -> orderService.delete(42L))
        .isInstanceOf(AccessDeniedException.class);
}
```

O ponto crítico: `@PreAuthorize` só dispara se a anotação `@EnableMethodSecurity` estiver presente no contexto de teste. Num slice mínimo que não importa essa config, o método executa **sem** checar nada — o teste "passa" sem testar segurança alguma. Daí a Armadilha (3).

## Na prática

Um `@WebMvcTest` de um `OrderController`: o caminho feliz autenticado, o caso sem auth (401), o POST com CSRF e um disparo via `jwt()` com authority específica.

```java
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(OrderController.class)
class OrderControllerSecurityTest {

    @Autowired MockMvc mockMvc;
    @MockitoBean OrderService orderService;

    @Test
    @WithMockUser(roles = "ADMIN")
    void adminListaOrders() throws Exception {
        mockMvc.perform(get("/orders"))
               .andExpect(status().isOk());
    }

    @Test
    void semAuthRetorna401() throws Exception {
        mockMvc.perform(get("/orders"))
               .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(roles = "USER")
    void userSemRoleAdminRetorna403() throws Exception {
        mockMvc.perform(delete("/orders/1").with(csrf()))
               .andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void postCriaOrderComCsrf() throws Exception {
        mockMvc.perform(post("/orders")
                   .with(csrf())
                   .contentType(MediaType.APPLICATION_JSON)
                   .content("{\"item\":\"book\"}"))
               .andExpect(status().isCreated());
    }

    @Test
    void resourceServerComJwtEAuthority() throws Exception {
        mockMvc.perform(get("/orders")
                   .with(jwt().authorities(
                       new SimpleGrantedAuthority("SCOPE_orders:read"))))
               .andExpect(status().isOk());
    }
}
```

Note o que **não** está aqui: nenhuma re-explicação de como o filter chain autentica, do que é uma role versus authority, ou de como `@PreAuthorize` avalia SpEL. Tudo isso é [[03-Dominios/Tecnologia/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|Galho 12]]. O teste só prova que a config existente responde como esperado a uma identidade conhecida.

## Armadilhas

### (1) Testar endpoint protegido sem auth e estranhar o 401

Você escreve um teste de controller, dispara `get("/orders")` e leva um 401 inesperado — o teste vermelho parece um bug do controller. Não é: o `@WebMvcTest` **carrega a config de segurança por padrão**, então sem identidade no contexto o request é barrado antes do handler.

```java
@Test
void listaOrders() throws Exception {
    mockMvc.perform(get("/orders"))
           .andExpect(status().isOk()); // FALHA: recebe 401, não 200
}
```

**Fix:** decida o que o teste quer provar. Se é o caso autenticado, adicione `@WithMockUser(roles = "ADMIN")` ou `.with(jwt())`. Se é o caso anônimo, mude a expectativa para `status().isUnauthorized()`. O 401 aqui é o sistema funcionando, não falhando.

### (2) Esquecer with(csrf()) num POST com CSRF ligado

[[03-Dominios/Tecnologia/Java/Segurança/10 - CSRF — por que ligado por default e quando desligar|CSRF vem ligado por default]] para métodos mutantes. Um teste de POST autenticado mas sem o post-processor de CSRF recebe **403** — e o desenvolvedor culpa a autorização, quando na verdade faltou o token.

```java
@Test
@WithMockUser(roles = "ADMIN")
void criaOrder() throws Exception {
    mockMvc.perform(post("/orders").content("{}"))
           .andExpect(status().isCreated()); // FALHA: 403 por falta de CSRF
}
```

**Fix:** adicione `.with(csrf())` em todo POST/PUT/DELETE enquanto o CSRF estiver ligado. O 403 sem isso é indistinguível, à primeira vista, de uma falha de autorização — por isso é tão traiçoeiro.

### (3) @WithMockUser num slice sem method security habilitado

Você protege `OrderService.delete` com `@PreAuthorize("hasAuthority('ORDER_DELETE')")`, escreve um teste com `@WithMockUser(roles = "USER")` esperando `AccessDeniedException`... e o método executa normalmente. Motivo: o contexto de teste não importou `@EnableMethodSecurity`, então o proxy que avalia `@PreAuthorize` nunca foi criado. A anotação vira decoração inerte.

```java
@Test
@WithMockUser(roles = "USER")
void deleteDeveriaSerNegado() {
    orderService.delete(1L); // NÃO lança nada — @PreAuthorize não dispara
}
```

**Fix:** garanta que a config de method security entra no contexto de teste — importe explicitamente a `@Configuration` anotada com `@EnableMethodSecurity` (ex.: `@Import(MethodSecurityConfig.class)`) ou use um teste de contexto completo. Sem isso, o teste dá um falso verde silencioso, que é o pior tipo de teste de segurança.

## Em entrevista

### Frase pronta (inglês)

> I test Spring Security with the `spring-security-test` library. For a known identity I use `@WithMockUser` or `@WithUserDetails` to populate the `SecurityContext` before the test runs, and for request-scoped scenarios I use the MockMvc post-processors — `with(jwt())` to simulate a resource-server flow without signing a real token, and `with(csrf())` so mutating requests carry the expected CSRF token. The core assertions are the authorization outcomes: 401 when the request is unauthenticated, and 403 when an authenticated principal lacks the required authority. For method security I either drive the endpoint through MockMvc or call the protected bean directly, but only after making sure `@EnableMethodSecurity` is actually in the test context — otherwise `@PreAuthorize` silently never fires and the test passes for the wrong reason.

### Vocabulário

| Termo | Significado |
| --- | --- |
| `spring-security-test` | Dependência que fornece anotações e post-processors de teste |
| `@WithMockUser` | Injeta um usuário fabricado no `SecurityContext` antes do teste |
| `@WithUserDetails` | Carrega um usuário real do `UserDetailsService` para o teste |
| Request post-processor | Mutator aplicado ao request via `.with(...)` no MockMvc |
| `with(jwt())` | Simula autenticação de Resource Server sem validar assinatura |
| `with(csrf())` | Injeta o token CSRF esperado em requests mutantes |
| 401 vs 403 | Não-autenticado (sem identidade) vs não-autorizado (sem permissão) |
| Method security | Autorização no nível do método via `@PreAuthorize`/`@PostAuthorize` |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc|@WebMvcTest]]
- [[03-Dominios/Tecnologia/Java/Testes/12 - Testes de integração ponta a ponta|Testes de integração ponta a ponta]]
- [[03-Dominios/Tecnologia/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Autorização baseada em URL]]
- [[03-Dominios/Tecnologia/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL|Method security]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- Spring Security Reference — Testing: https://docs.spring.io/spring-security/reference/servlet/test/index.html
- Spring Security Reference — Testing MockMvc: https://docs.spring.io/spring-security/reference/servlet/test/mockmvc/index.html
