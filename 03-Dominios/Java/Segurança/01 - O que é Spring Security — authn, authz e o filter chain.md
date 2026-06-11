---
title: "O que é Spring Security — authn, authz e o filter chain"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - seguranca
  - iniciado
  - spring-security
  - filter-chain
aliases:
  - "Spring Security"
  - "o que é Spring Security"
  - "filter chain"
---

# O que é Spring Security — authn, authz e o filter chain

> [!abstract] TL;DR
> Spring Security protege a aplicação através de um **filter chain** — uma cadeia de filtros Servlet que intercepta cada request **antes** que ele chegue ao `DispatcherServlet`. Ele separa dois conceitos que nunca devem se misturar: **autenticação** (authn — quem você é) e **autorização** (authz — o que você pode fazer). A configuração moderna na versão **6.x** é um bean `SecurityFilterChain` escrito com **lambda DSL** e anotado com `@EnableWebSecurity` — o velho `WebSecurityConfigurerAdapter` foi **removido na 6.0** e não existe mais.

## O que é

Spring Security é o framework de segurança do ecossistema Spring. Ele resolve dois problemas distintos, e a primeira coisa a entender é que eles são **distintos**:

- **Autenticação (authentication, authn)** — responde "*quem é você?*". É o processo de provar identidade: usuário e senha, token, certificado. O resultado é um `Authentication` populado no contexto.
- **Autorização (authorization, authz)** — responde "*o que você tem permissão de fazer?*". Dado que já sabemos quem você é, decide se você pode acessar este endpoint, este método, este recurso.

Você sempre autentica **primeiro** e autoriza **depois** — não dá pra decidir o que alguém pode fazer sem antes saber quem é. Spring Security materializa essa ordem na própria cadeia de filtros: o filtro que autentica roda antes do filtro que autoriza.

## Por que importa

Toda aplicação séria exposta na web precisa decidir quem entra e o que cada um faz. Spring Security é a resposta padrão para isso no mundo Spring, e por ser tão onipresente, **entrevista cobra**. As perguntas clássicas são:

- "O que é o filter chain do Spring Security?"
- "Como uma request flui até o controller passando pela segurança?"
- "Qual a diferença entre autenticação e autorização?"

Quem responde "Spring Security é a tela de login" perdeu a questão. A tela de login é **um filtro** dentro de uma cadeia inteira. Entender a cadeia — e onde ela se encaixa em relação ao `DispatcherServlet` — é o que separa a resposta de iniciado da resposta de quem realmente conhece o framework.

## Como funciona

### Autenticação vs autorização: dois conceitos, não misturar

Pense num prédio comercial:

- **Autenticação** é o crachá na recepção: você prova que é o João da empresa X. A recepção não decide pra onde você vai — só confirma que você é o João.
- **Autorização** é o leitor de crachá em cada porta: o crachá do João abre o 3º andar mas não o data center. Agora que já sabemos que você é o João, decidimos a cada porta o que ele pode abrir.

São camadas diferentes, com momentos diferentes e perguntas diferentes. Misturar as duas — por exemplo, tratar "está logado?" como se fosse "pode fazer isso?" — é um dos erros mais comuns (ver Armadilhas).

### O filter chain: request → FilterChainProxy → SecurityFilterChain → DispatcherServlet

Spring Security é construído sobre **Servlet Filters**. Um `Filter` genérico intercepta requests antes do servlet — esse mecanismo é da camada web (ver [[03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]]). Spring Security usa esse ponto de entrada para inserir sua própria cadeia.

O caminho de uma request é:

1. O container cria a `FilterChain` padrão e passa o request adiante.
2. Um `DelegatingFilterProxy` (registrado no container) faz a ponte do mundo Servlet para o mundo Spring, delegando para um bean gerenciado pelo container de Spring.
3. Esse bean é o `FilterChainProxy` — o filtro central de Spring Security. Ele é o ponto único de entrada de toda a segurança e o melhor lugar para começar a depurar.
4. O `FilterChainProxy` escolhe, via `RequestMatcher`, **qual** `SecurityFilterChain` aplicar a este request (pode haver várias cadeias configuradas — só a primeira que casa é usada).
5. A `SecurityFilterChain` escolhida define a lista ordenada de filtros de segurança a executar (autenticação, autorização, proteções contra exploits como CSRF).
6. Se o request sobreviver à cadeia (autenticado e autorizado), ele finalmente chega ao `DispatcherServlet` e segue o fluxo normal de MVC — ver [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]].

Os filtros dentro da cadeia têm ordem definida — por exemplo, `BasicAuthenticationFilter` (autenticação via HTTP Basic) e `UsernamePasswordAuthenticationFilter` (form login) rodam **antes** do `AuthorizationFilter` (autorização). A ordem não é acidental: autenticação precede autorização.

### Config 6.x: o bean SecurityFilterChain + lambda DSL (WebSecurityConfigurerAdapter foi removido na 6.0)

Na versão **6.x** (baseline: Spring Boot 3.x, namespace `jakarta.*`, Java 17), a configuração é um **bean** que retorna uma `SecurityFilterChain`, construído com a **lambda DSL** do `HttpSecurity`:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .anyRequest().authenticated()
            )
            .httpBasic(Customizer.withDefaults());
        return http.build();
    }
}
```

O ponto crucial: até a versão 5.x você estendia uma classe abstrata, `WebSecurityConfigurerAdapter`, e sobrescrevia métodos. Essa classe foi **removida na 6.0**. Não existe mais. A forma correta hoje é declarar o bean `SecurityFilterChain` como acima. Código antigo (ou tutorial antigo) que manda estender `WebSecurityConfigurerAdapter` está desatualizado e **não compila** na 6.x.

> [!info] E as versões mais novas?
> A 6.x é o baseline para entrevistas atuais. Já existem Spring Security 7.x / Spring Boot 4.x como linhas mais recentes, mas o padrão `SecurityFilterChain` + lambda DSL é o mesmo — o que mudou foi o adapter sumir, e isso já aconteceu na 6.0.

### A dupla fronteira: o chain na frente do DispatcherServlet (Galho 9), method security sobre AOP (Galho 8)

Spring Security age em **duas fronteiras** complementares:

1. **Na borda HTTP** — o filter chain senta na frente do `DispatcherServlet` e protege por URL/request. É a primeira linha. O `DispatcherServlet` e o pipeline MVC são assunto do Galho 9 — aqui só ancoramos que o chain vem **antes** dele: ver [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]].
2. **No nível de método** — *method security* (anotações como `@PreAuthorize`) protege beans diretamente, e funciona porque é implementada sobre **AOP/proxies** — o mesmo mecanismo de proxy de bean do Galho 8. Aqui só ancoramos a ideia; o detalhe de method security é tema de nota própria mais adiante neste galho.

A lição de iniciado: segurança no Spring não é um lugar só. Tem a cadeia na frente da web e tem a proteção dentro dos beans. As duas se complementam.

## Na prática

Um `SecurityFilterChain` mínimo que exige autenticação em qualquer request, com HTTP Basic:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/public/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .httpBasic(Customizer.withDefaults())
            .formLogin(Customizer.withDefaults());
        return http.build();
    }
}
```

Repare na separação: `authorizeHttpRequests` é **autorização** (quem pode o quê — `permitAll`, `hasRole`, `authenticated`), enquanto `httpBasic` e `formLogin` configuram **autenticação** (como você prova quem é). Mesma config, dois conceitos lado a lado, sem se confundirem.

O fluxo de uma request a um endpoint protegido (digamos `GET /admin/orders`, atendido por um `OrderController`):

```text
   Cliente (GET /admin/orders)
        │
        ▼
   FilterChain do container
        │
        ▼
   DelegatingFilterProxy   ── ponte Servlet → Spring
        │
        ▼
   FilterChainProxy        ── filtro central de segurança
        │
        │  escolhe via RequestMatcher
        ▼
   SecurityFilterChain     ── filtros ordenados:
        │                     1. autenticação (Basic / form login)
        │                     2. autorização (AuthorizationFilter)
        │
        │  request autenticado + autorizado?
        ▼
   DispatcherServlet       ── (Galho 9) pipeline MVC
        │
        ▼
   OrderController.list()  ── chega o request limpo
```

Se a autenticação falha, ou a autorização nega, o request **nunca chega** ao `OrderController` — a cadeia corta antes.

## Armadilhas

### (1) Misturar autenticação e autorização

São perguntas diferentes: authn é "*quem é você?*", authz é "*o que você pode?*". Tratar "está logado" como se fosse "pode fazer" leva a brechas — um usuário autenticado **não** é automaticamente autorizado para tudo.

Exemplo: deixar `anyRequest().authenticated()` e achar que `/admin/**` está protegido contra usuários comuns. Não está — qualquer usuário logado passa. Falta a regra de **autorização** por papel.

Fix: separe sempre as duas camadas — autentique com `httpBasic`/`formLogin` e autorize com `requestMatchers(...).hasRole(...)` distinto de `.authenticated()`.

### (2) Usar WebSecurityConfigurerAdapter

`WebSecurityConfigurerAdapter` foi **removido na 6.0**. Tutoriais e respostas de fórum antigos mandam estender essa classe e sobrescrever `configure(HttpSecurity)` — isso nem compila na 6.x.

Exemplo: `public class SecurityConfig extends WebSecurityConfigurerAdapter { ... }` → erro de compilação (classe inexistente).

Fix: declare um bean `SecurityFilterChain` recebendo `HttpSecurity` e retornando `http.build()`, numa `@Configuration` com `@EnableWebSecurity`.

### (3) Achar que "Spring Security = formulário de login"

O form login é **um filtro** dentro da cadeia, não o framework inteiro. Reduzir Spring Security à tela de login esconde a autorização, as proteções contra exploits (CSRF, headers) e a própria mecânica do filter chain.

Exemplo: configurar só `formLogin` e assumir que a app está "segura", sem nenhuma regra de autorização nem entender que cada request passa pela cadeia toda.

Fix: pense em **filter chain**, não em "login" — a cadeia inteira (autenticação + autorização + proteções) é o que protege a aplicação.

## Em entrevista

### Frase pronta (inglês)

> Spring Security works as a **filter chain** that sits in front of the `DispatcherServlet`: every request goes through a `FilterChainProxy`, which picks a matching `SecurityFilterChain` and runs its ordered security filters before the request ever reaches a controller. The key trade-off it enforces is keeping **authentication** ("who are you?") and **authorization** ("what are you allowed to do?") as two separate stages — you always authenticate first, then authorize. The modern decision in **6.x** is to define a `SecurityFilterChain` bean using the lambda DSL with `@EnableWebSecurity`; the important caveat is that `WebSecurityConfigurerAdapter` was **removed in 6.0**, so any code extending it simply won't compile anymore.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| autenticação | authentication (authn) |
| autorização | authorization (authz) |
| cadeia de filtros | filter chain |
| filtro de segurança | security filter |
| usuário autenticado | authenticated user |
| papel / função | role |
| ponto de entrada de autenticação | authentication entry point |
| acesso negado | access denied |

## Veja também

- [[03-Dominios/Java/Segurança/02 - SecurityContext, Authentication e Principal — o usuário atual|SecurityContext, Authentication e Principal]]
- [[03-Dominios/Java/Segurança/06 - A arquitetura do filter chain em profundidade|A arquitetura do filter chain em profundidade]]
- [[03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]]
- [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]
- [[03-Dominios/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]]

## Referências

- [Spring Security Reference — Servlet Architecture](https://docs.spring.io/spring-security/reference/servlet/architecture.html)
- [Spring Security Reference — Getting Started](https://docs.spring.io/spring-security/reference/servlet/getting-started.html)
- [Spring Security 6.5 Reference — Getting Started](https://docs.spring.io/spring-security/reference/6.5/servlet/getting-started.html)
