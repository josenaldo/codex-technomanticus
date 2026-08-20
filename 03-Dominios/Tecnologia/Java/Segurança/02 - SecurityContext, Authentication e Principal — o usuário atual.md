---
title: "SecurityContext, Authentication e Principal — o usuário atual"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - seguranca
  - iniciado
  - spring-security
aliases:
  - "SecurityContext"
  - "Authentication vs Principal"
---

# SecurityContext, Authentication e Principal — o usuário atual

> [!abstract] TL;DR
> Depois que o Spring Security autentica alguém, ele precisa de um lugar para guardar "quem está logado agora". Esse lugar é o `SecurityContextHolder` — por padrão um `ThreadLocal`, ou seja, vinculado à thread que processa o request. Dentro dele mora um `SecurityContext`, que carrega um único objeto `Authentication`. O `Authentication` junta duas coisas: o **principal** (quem é o usuário) e os `GrantedAuthority` (o que ele pode fazer). No controller, você raramente cava o `SecurityContextHolder` na mão: a anotação `@AuthenticationPrincipal` injeta o principal direto no parâmetro do método.

## O que é

São três peças que respondem à pergunta "quem é o usuário atual e o que ele pode fazer?":

- **`SecurityContextHolder`** — o cofre estático onde o Spring Security guarda os dados de quem está autenticado. Por padrão usa uma estratégia de `ThreadLocal`, de modo que qualquer método rodando na mesma thread enxerga o mesmo "usuário atual" sem precisar passá-lo de parâmetro em parâmetro.
- **`SecurityContext`** — o que está dentro do holder. É basicamente um envelope que contém o `Authentication`.
- **`Authentication`** — o objeto que representa o usuário autenticado. Curiosamente, ele estende `java.security.Principal` (a interface padrão do Java para "uma identidade"), e expõe o **principal**, as **credentials** e as **authorities**.

Em uma frase: o holder guarda o contexto, o contexto guarda o `Authentication`, e o `Authentication` descreve a pessoa logada.

## Por que importa

Quase toda decisão de autorização depende de saber quem é o usuário atual. Quando você escreve `@PreAuthorize("hasRole('ADMIN')")` ou checa se o dono de um `Order` é quem está pedindo, por baixo dos panos o Spring lê o `Authentication` do `SecurityContextHolder`.

Entender esse trio evita dois tipos de erro comuns: (1) tentar buscar o usuário logado de um jeito frágil (sessão HTTP na mão, parâmetros passados manualmente) quando o Spring já oferece um ponto único; e (2) cair em bugs sutis de `ThreadLocal` — usuário vazando entre requests, principal de tipo inesperado, ou `getAuthentication()` retornando `null`.

## Como funciona

### SecurityContextHolder: o "usuário atual" (um ThreadLocal)

O `SecurityContextHolder` é uma classe com métodos estáticos. Por padrão, a estratégia de armazenamento é `MODE_THREADLOCAL`: cada thread tem sua própria cópia do `SecurityContext`. Isso é conveniente porque, durante o processamento de um request HTTP, tudo roda (em geral) na mesma thread — então qualquer camada (controller, service, repository) consegue perguntar "quem é o usuário?" sem receber isso como argumento.

```java
SecurityContext context = SecurityContextHolder.getContext();
Authentication authentication = context.getAuthentication();
String username = authentication.getName(); // herdado de Principal
```

O Spring Security cuida de **popular** o holder no começo do request (a partir da sessão, de um token JWT, etc.) e de **limpá-lo** no fim, via o filtro `SecurityContextHolderFilter`. Esse "limpar no fim" é crucial em ambientes com thread pool — falaremos disso nas Armadilhas.

> [!tip] Outras estratégias
> Além de `MODE_THREADLOCAL`, existem `MODE_INHERITABLETHREADLOCAL` (propaga o contexto para threads-filhas) e `MODE_GLOBAL` (uma instância para a aplicação inteira). Para fase iniciado, basta saber que o default é por-thread.

### Authentication: principal + credentials + authorities

A interface `Authentication` agrega o estado de uma autenticação. Os métodos que importam:

| Método | O que devolve |
| --- | --- |
| `getPrincipal()` | quem é o usuário (tipicamente `UserDetails`, `Jwt` ou `OidcUser`) |
| `getCredentials()` | a "prova" — normalmente a senha; costuma ser apagada após autenticar |
| `getAuthorities()` | uma `Collection<GrantedAuthority>` — o que o usuário pode fazer |
| `isAuthenticated()` | `true` se já foi autenticado, `false` se é só um pedido de autenticação |
| `getName()` | o nome do principal (herdado de `java.security.Principal`) |

O mesmo tipo `Authentication` tem dois papéis: **antes** de autenticar, ele carrega as credenciais cruas e `isAuthenticated()` é `false`; **depois**, o `AuthenticationManager` devolve um `Authentication` autenticado, com as credenciais limpas e as authorities preenchidas, que é o que vai parar no `SecurityContext`.

### Principal vs Authorities: quem é vs o que pode

É fácil confundir os dois, mas a distinção é limpa:

- O **principal** responde "**quem** é?". É a identidade — geralmente um objeto rico com username, e-mail, flags de conta, etc.
- As **authorities** respondem "**o que** pode?". Cada `GrantedAuthority` é uma permissão de alto nível: uma role (`ROLE_ADMIN`), uma permissão (`ORDER_READ`) ou um scope OAuth2 (`SCOPE_orders`).

O principal **carrega** suas authorities (um `UserDetails` tem `getAuthorities()`), mas conceitualmente são eixos diferentes. Autenticação é sobre o principal; autorização é sobre as authorities.

### Acessando no controller: @AuthenticationPrincipal

Ler o `SecurityContextHolder` na mão funciona, mas polui o código e dificulta testes. No Spring MVC, a anotação `@AuthenticationPrincipal` resolve isso: ela injeta diretamente o **principal** (o resultado de `getAuthentication().getPrincipal()`) no parâmetro do método do controller.

Você também pode injetar o `Authentication` inteiro só declarando um parâmetro desse tipo, ou pegar o contexto completo com `@CurrentSecurityContext`.

## Na prática

```java
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.bind.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CurrentUserController {

    // Forma 1: lendo o Authentication direto do holder (em qualquer camada)
    public String quemEstaLogado() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return "anônimo";
        }
        return auth.getName(); // ex.: "customer42"
    }

    // Forma 2: injetando o principal no controller (preferível)
    @GetMapping("/me")
    public String me(@AuthenticationPrincipal UserDetails user) {
        return "Usuário: " + user.getUsername()
                + " | Authorities: " + user.getAuthorities();
    }
}
```

A Forma 2 é mais limpa: o método declara exatamente o que precisa, fica fácil de testar (basta passar um `UserDetails` falso) e não depende de chamadas estáticas escondidas.

## Armadilhas

### (1) `getPrincipal()` sem checar o tipo → `ClassCastException`

O principal **não é sempre** um `UserDetails`. Dependendo do mecanismo de autenticação, ele pode ser um `Jwt` (autenticação por token), um `OidcUser` (login OIDC) ou até uma `String` simples.

```java
// Frágil: assume UserDetails cegamente
UserDetails user = (UserDetails) auth.getPrincipal(); // ClassCastException se for Jwt!
```

**Fix:** ou você sabe o mecanismo em uso e declara o tipo correto, ou checa antes de fazer o cast:

```java
Object principal = auth.getPrincipal();
if (principal instanceof UserDetails userDetails) {
    String username = userDetails.getUsername();
}
```

### (2) `SecurityContextHolder` vazando entre requests num thread pool

Como o default é `ThreadLocal`, e servidores reutilizam threads via pool, um `SecurityContext` deixado pendurado pode "vazar" para o próximo request que pegar a mesma thread — fazendo o request B enxergar o usuário do request A.

```java
// Perigoso: setou e nunca limpou
SecurityContextHolder.getContext().setAuthentication(novaAuth);
// ... a thread volta para o pool ainda "logada"
```

No fluxo HTTP normal o Spring limpa o holder ao fim do request. O problema aparece quando você manipula o contexto **manualmente** (jobs assíncronos, código em background).

**Fix:** sempre limpe o contexto no `finally` quando você o setou na mão:

```java
try {
    SecurityContextHolder.getContext().setAuthentication(novaAuth);
    // ... trabalho com o usuário X
} finally {
    SecurityContextHolder.clearContext();
}
```

### (3) Assumir que `getAuthentication()` é sempre não-nulo

Em endpoints públicos, ou antes de qualquer autenticação acontecer, `getAuthentication()` pode retornar `null`. Em muitas configs, requests não autenticados recebem um `AnonymousAuthenticationToken` (com authority `ROLE_ANONYMOUS`) em vez de `null` — mas você não pode contar com isso em todo lugar.

```java
// NPE se a request for pública e não houver auth
String nome = SecurityContextHolder.getContext().getAuthentication().getName();
```

**Fix:** trate o `null` e/ou o caso anônimo explicitamente:

```java
Authentication auth = SecurityContextHolder.getContext().getAuthentication();
boolean logado = auth != null
        && auth.isAuthenticated()
        && !(auth instanceof AnonymousAuthenticationToken);
```

## Em entrevista

### Frase pronta (inglês)

> In Spring Security, the currently authenticated user lives in the `SecurityContextHolder`, which by default is backed by a `ThreadLocal` tied to the request thread. It holds a `SecurityContext`, and that context holds a single `Authentication` object. The `Authentication` separates two concerns: the principal — who the user is, typically a `UserDetails`, `Jwt`, or `OidcUser` — and the granted authorities, which describe what the user is allowed to do. In a controller I usually avoid reading the holder directly and instead inject the principal with `@AuthenticationPrincipal`, which keeps the method explicit and easy to test.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| usuário atual / autenticado | current / authenticated user |
| contexto de segurança | security context |
| identidade (quem é) | principal |
| credenciais | credentials |
| permissões concedidas | granted authorities |
| variável por thread | thread-local |
| usuário anônimo | anonymous user |
| limpar o contexto | clear the context |

## Veja também

- [[03-Dominios/Tecnologia/Java/Segurança/01 - O que é Spring Security — authn, authz e o filter chain|O que é Spring Security]]
- [[03-Dominios/Tecnologia/Java/Segurança/03 - Autenticação — UserDetailsService, AuthenticationManager, Form e Basic|Autenticação]]
- [[03-Dominios/Tecnologia/Java/Segurança/17 - Uma request autenticada do token à autorização no método|Uma request autenticada de ponta a ponta]]
- [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- Spring Security Reference — Authentication Architecture: https://docs.spring.io/spring-security/reference/servlet/authentication/architecture.html
