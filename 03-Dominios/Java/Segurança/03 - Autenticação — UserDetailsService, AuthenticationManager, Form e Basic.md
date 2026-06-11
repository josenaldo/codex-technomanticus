---
title: "Autenticação — UserDetailsService, AuthenticationManager, Form e Basic"
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
  - autenticacao
aliases:
  - "Autenticação no Spring Security"
  - "UserDetailsService"
---

# Autenticação — UserDetailsService, AuthenticationManager, Form e Basic

> [!abstract] TL;DR
> **Autenticação** é o ato de provar _quem é_ o usuário (em oposição à autorização, que decide _o que ele pode fazer_). No Spring Security, o `UserDetailsService` carrega o usuário a partir do banco (ou de onde quer que ele viva); o `AuthenticationManager` — quase sempre o `ProviderManager` — delega para um `AuthenticationProvider` (o `DaoAuthenticationProvider`), que confere a senha enviada contra a senha armazenada usando o `PasswordEncoder`. A entrada de credenciais pode chegar por **HTTP Basic** (header `Authorization: Basic`, simples, stateless, sempre sobre HTTPS) ou por **Form login** (formulário HTML, sessão, cookie). No fim, um `Authentication` autenticado vai parar no `SecurityContextHolder`.

## O que é

Autenticação responde à pergunta **"você é quem diz ser?"**. O usuário apresenta uma identidade (um username) e uma prova (uma senha, um token), e o Spring Security verifica se a prova bate com o que ele conhece sobre aquela identidade.

O coração desse processo, no caso de username/senha, é o trio:

- `UserDetailsService` — sabe **carregar** o usuário (busca no banco e devolve um `UserDetails`).
- `AuthenticationManager` / `AuthenticationProvider` — sabe **orquestrar** a verificação.
- `PasswordEncoder` — sabe **comparar** a senha enviada com a armazenada (ver [[03-Dominios/Java/Segurança/04 - Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder|Password encoding]]).

Antes de mergulhar no fluxo, vale ter um mapa de **qual mecanismo de autenticação usar e quando**:

| Mecanismo | Como funciona | Quando usar |
| --- | --- | --- |
| **HTTP Basic** | Username/senha em Base64 no header `Authorization`, a cada request | APIs internas simples, scripts, ferramentas de linha de comando — **sempre sobre HTTPS** |
| **Form login** | Formulário HTML, sessão server-side, cookie de sessão | Aplicações web tradicionais com navegador e UI própria de login |
| **JWT** (token assinado, stateless) | Cliente envia um token autocontido no header `Authorization: Bearer` | APIs REST stateless, SPAs, mobile — ver [[03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação\|JWT]] (nota 08/09 do galho) |
| **OAuth2 / OIDC** | Delegação a um provedor de identidade (Google, Keycloak, etc.) | Login social, SSO corporativo, federação de identidade — nota 12 do galho (planejado) |

> [!info] Sobre Base64
> Base64 **não é criptografia** — é só uma codificação reversível por qualquer um. `dXNlcjpzZW5oYQ==` decodifica trivialmente para `user:senha`. Por isso HTTP Basic exige HTTPS: sem TLS, a credencial trafega em texto claro disfarçado.

## Por que importa

Em entrevista sênior e na prática, três coisas se cobram aqui:

1. **Saber onde a senha é verificada.** Muita gente acha que o `UserDetailsService` "loga o usuário". Não loga: ele só **carrega** os dados. Quem compara a senha é o `AuthenticationProvider` com o `PasswordEncoder`. Confundir isso leva a bugs de segurança (por exemplo, comparar senha em texto puro dentro do `loadUserByUsername`).
2. **Saber separar stateless de stateful.** HTTP Basic e JWT são stateless (sem sessão); Form login é stateful (com sessão). A escolha muda tudo: CSRF, escalabilidade horizontal, logout, expiração.
3. **Não vazar informação no erro.** Distinguir "usuário não existe" de "senha errada" entrega informação valiosa a um atacante (enumeração de usuários). O comportamento correto é uma mensagem genérica.

## Como funciona

### UserDetailsService: carregando o usuário do banco

`UserDetailsService` é uma interface de **um método só**:

```java
public interface UserDetailsService {
    UserDetails loadUserByUsername(String username) throws UsernameNotFoundException;
}
```

O contrato é direto: recebe um username, devolve um `UserDetails` (que carrega username, senha _codificada_, authorities e flags de conta — habilitada, bloqueada, expirada) ou lança `UsernameNotFoundException` se não achar.

O ponto-chave de configuração: **se você expõe um `UserDetailsService` como `@Bean`, o Spring Security o detecta automaticamente** e o usa para montar o `DaoAuthenticationProvider`. Não é preciso registrar nada manualmente — basta o bean existir (e não haver um `AuthenticationManagerBuilder` ou um `AuthenticationProvider` já populado que sobreponha esse comportamento).

Para _construir_ um `UserDetails`, o Spring oferece o builder `User.builder()`:

```java
UserDetails user = User.builder()
        .username("alice")
        .password(encodedPassword)        // já codificada pelo PasswordEncoder
        .authorities("ROLE_ADMIN")
        .build();
```

### AuthenticationManager → AuthenticationProvider → UserDetailsService + PasswordEncoder

O `AuthenticationManager` é a interface central da autenticação:

```java
public interface AuthenticationManager {
    Authentication authenticate(Authentication authentication)
            throws AuthenticationException;
}
```

Ela recebe um `Authentication` **não autenticado** (com username e senha cruas) e devolve um `Authentication` **autenticado** (com o principal resolvido e as authorities preenchidas) — ou lança uma `AuthenticationException`.

A implementação mais comum é o `ProviderManager`, que mantém uma **lista de `AuthenticationProvider`** e tenta cada um até que algum saiba lidar com aquele tipo de autenticação. Para username/senha, o provider que entra em cena é o `DaoAuthenticationProvider`, que faz exatamente dois passos:

```text
AuthenticationManager (ProviderManager)
        │
        ▼
DaoAuthenticationProvider
        │  1. userDetailsService.loadUserByUsername(username)
        │  2. passwordEncoder.matches(senhaEnviada, userDetails.getPassword())
        ▼
Authentication autenticado  →  SecurityContextHolder
```

Repare na divisão de responsabilidades: o `UserDetailsService` **carrega**, o `PasswordEncoder` **compara**, o `AuthenticationProvider` **orquestra**, o `AuthenticationManager` **coordena os providers**, e o resultado final é guardado no `SecurityContextHolder` (ver [[03-Dominios/Java/Segurança/02 - SecurityContext, Authentication e Principal — o usuário atual|SecurityContext, Authentication e Principal]]).

### Form login (sessão) vs HTTP Basic (header, sempre HTTPS)

As duas formas de _entregar credenciais_ ao mesmo motor de verificação:

**Form login** — stateful, para navegadores:

- O usuário não autenticado é redirecionado para uma página de login (`/login` por padrão).
- Ele submete um formulário HTML (`POST` com `username` e `password`).
- Em caso de sucesso, o servidor cria uma **sessão HTTP** e devolve um cookie (`JSESSIONID`). Os requests seguintes carregam só o cookie — as credenciais não voltam a trafegar.
- Como há sessão e cookie, **CSRF importa** (ver nota futura do galho sobre CSRF, planejado).

**HTTP Basic** — stateless, para clientes programáticos:

- Cliente pede um recurso protegido sem credencial.
- O `BasicAuthenticationEntryPoint` responde `401` com `WWW-Authenticate: Basic realm="Realm"`.
- O cliente repete o request com `Authorization: Basic <base64(username:senha)>`.
- O `BasicAuthenticationFilter` extrai as credenciais, monta um `UsernamePasswordAuthenticationToken` e passa ao `AuthenticationManager`.
- **A credencial vai em todo request** — por isso, sem HTTPS, ela está exposta a cada chamada.

> [!warning] Comportamento padrão mudou
> No Spring Boot 3.x / Security 6.x, HTTP Basic e Form login deixam de ser habilitados "de graça" assim que você fornece uma configuração `SecurityFilterChain` própria. Se quiser qualquer um dos dois, **configure-o explicitamente** no `HttpSecurity`.

### Autenticação programática (authManager.authenticate(...))

Às vezes você precisa autenticar fora do fluxo automático dos filtros — por exemplo, num endpoint custom de login que devolve um token, ou para "logar" o usuário logo após o cadastro. Nesse caso você injeta o `AuthenticationManager` e o chama na mão:

```java
@Service
public class LoginService {

    private final AuthenticationManager authenticationManager;

    public LoginService(AuthenticationManager authenticationManager) {
        this.authenticationManager = authenticationManager;
    }

    public Authentication login(String username, String rawPassword) {
        Authentication request =
                new UsernamePasswordAuthenticationToken(username, rawPassword);
        // pode lançar BadCredentialsException, DisabledException, etc.
        Authentication result = authenticationManager.authenticate(request);
        SecurityContextHolder.getContext().setAuthentication(result);
        return result;
    }
}
```

Você passa um token **não autenticado** (com a senha crua), o manager dispara todo o fluxo (provider → `UserDetailsService` → `PasswordEncoder`) e devolve um token **autenticado** — ou lança uma `AuthenticationException`. Note que **você nunca compara senha à mão**: deixa o motor fazer.

## Na prática

Uma implementação típica de `UserDetailsService` mapeia as suas **entidades de domínio neutras** (`User`, `Role`) para o `UserDetails` que o Spring entende:

```java
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.core.userdetails.User;

@Service
public class UserDetailsServiceImpl implements UserDetailsService {

    private final UserRepository userRepository;

    public UserDetailsServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String username)
            throws UsernameNotFoundException {

        User user = userRepository.findByUsername(username)
                .orElseThrow(() ->
                        new UsernameNotFoundException("Invalid credentials"));

        String[] authorities = user.getRoles().stream()
                .map(role -> "ROLE_" + role.getName())   // ex.: ROLE_ADMIN
                .toArray(String[]::new);

        return User.builder()
                .username(user.getUsername())
                .password(user.getPassword())   // hash já armazenado no banco
                .authorities(authorities)
                .disabled(!user.isEnabled())
                .build();
    }
}
```

Repare:

- As entidades de persistência (`User`, `Role`) são suas; o `UserDetails` é o que o Spring consome. O `UserDetailsServiceImpl` é a **ponte** entre os dois mundos.
- A senha devolvida é o **hash armazenado**, nunca a senha em texto. Quem compara é o `PasswordEncoder` lá no provider.
- A `UsernameNotFoundException` carrega uma mensagem **genérica** de propósito (ver Armadilha 1).

E a configuração do `HttpSecurity` ligando os dois mecanismos de entrega de credencial:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/login", "/public/**").permitAll()
                .anyRequest().authenticated()
            )
            // HTTP Basic — para clientes programáticos (sempre sobre HTTPS)
            .httpBasic(Customizer.withDefaults())
            // Form login — para o navegador, com página de login custom
            .formLogin(form -> form
                .loginPage("/login")
                .defaultSuccessUrl("/home", true)
                .permitAll()
            );
        return http.build();
    }

    @Bean
    PasswordEncoder passwordEncoder() {
        return PasswordEncoderFactories.createDelegatingPasswordEncoder();
    }
}
```

Com o `UserDetailsServiceImpl` exposto como `@Bean` (`@Service` já basta) e um `PasswordEncoder` no contexto, o Spring monta o `DaoAuthenticationProvider` sozinho. Você não instancia o provider manualmente.

## Armadilhas

### (1) Erro de autenticação que vaza informação

Distinguir "usuário não encontrado" de "senha incorreta" entrega ao atacante um **oráculo de enumeração de usuários**: ele descobre quais usernames existem só pela mensagem de erro.

```java
// RUIM — mensagens distintas vazam a existência da conta
User user = userRepository.findByUsername(username)
        .orElseThrow(() -> new UsernameNotFoundException("Username does not exist"));
// ... mais adiante: "Wrong password for user " + username
```

**Fix:** use uma mensagem **genérica e idêntica** para os dois casos ("Invalid credentials"). O próprio Spring, por padrão, converte `UsernameNotFoundException` em `BadCredentialsException` para uniformizar o erro — não trabalhe contra esse comportamento expondo mensagens específicas na sua UI ou logs voltados ao usuário.

### (2) HTTP Basic sem HTTPS

Com `httpBasic(...)` habilitado mas o app servindo HTTP puro, a credencial (Base64, ou seja, **reversível**) trafega legível em **cada request** — qualquer um na rede a captura.

```java
// PERIGOSO se o app aceita HTTP simples
http.httpBasic(Customizer.withDefaults());
```

**Fix:** force HTTPS no nível da infraestrutura (proxy/load balancer) e, no app, exija canal seguro:

```java
http.requiresChannel(channel -> channel.anyRequest().requiresSecure());
```

Assim o Spring redireciona requests HTTP para HTTPS antes de qualquer credencial trafegar.

### (3) Não tratar (ou tratar errado) a UsernameNotFoundException

Retornar `null` do `loadUserByUsername` em vez de lançar a exceção produz `NullPointerException` lá dentro do provider, com stack trace confuso e comportamento indefinido.

```java
// RUIM — devolve null silenciosamente
@Override
public UserDetails loadUserByUsername(String username) {
    User user = userRepository.findByUsername(username).orElse(null);
    return mapToUserDetails(user); // NPE quando user == null
}
```

**Fix:** o contrato manda **lançar `UsernameNotFoundException`** quando o usuário não existe (com mensagem genérica, conforme Armadilha 1). É o sinal que o provider espera para falhar a autenticação de forma controlada.

## Em entrevista

### Frase pronta (inglês)

> In Spring Security, authentication for username/password flows through three collaborators. The `UserDetailsService` only **loads** the user — typically mapping my own `User` and `Role` entities into a `UserDetails` — while the actual password check happens in the `DaoAuthenticationProvider`, which uses a `PasswordEncoder` to compare the submitted password against the stored hash. The `AuthenticationManager`, usually a `ProviderManager`, coordinates the providers and, on success, the authenticated `Authentication` is stored in the `SecurityContextHolder`. Credentials can arrive via HTTP Basic — stateless, sent in the `Authorization` header on every request, and therefore strictly over HTTPS — or via form login, which is session-based and relies on a cookie. A common mistake I always flag is leaking whether a username exists: the error message must stay generic to avoid user enumeration.

### Vocabulário

| Termo (EN) | Tradução / nota |
| --- | --- |
| credentials | credenciais (username + senha/token) |
| to load the user | carregar o usuário (não "logar") |
| password hash | hash da senha (nunca em texto claro) |
| stateless | sem estado (sem sessão server-side) |
| user enumeration | enumeração de usuários (vazamento via mensagens distintas) |
| challenge (`WWW-Authenticate`) | desafio enviado pelo servidor no `401` |
| in-memory authentication | autenticação em memória (para testes/protótipos) |
| to delegate to a provider | delegar a um provider de autenticação |

## Veja também

- [[03-Dominios/Java/Segurança/02 - SecurityContext, Authentication e Principal — o usuário atual|SecurityContext, Authentication e Principal]]
- [[03-Dominios/Java/Segurança/04 - Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder|Password encoding]]
- [[03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação|JWT]]
- [[03-Dominios/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]] (verbetes UserDetailsService / AuthenticationManager / AuthenticationProvider)

## Referências

- [Authentication (servlet) — Spring Security Reference](https://docs.spring.io/spring-security/reference/servlet/authentication/index.html)
- [UserDetailsService — Spring Security Reference](https://docs.spring.io/spring-security/reference/servlet/authentication/passwords/user-details-service.html)
- [Basic Authentication — Spring Security Reference](https://docs.spring.io/spring-security/reference/servlet/authentication/passwords/basic.html)
