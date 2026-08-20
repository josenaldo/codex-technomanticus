---
title: "CSRF — por que ligado por default e quando desligar"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - seguranca
  - adepto
  - csrf
aliases:
  - "CSRF"
  - "Cross-Site Request Forgery"
---

# CSRF — por que ligado por default e quando desligar

> [!abstract] TL;DR
> **CSRF** (Cross-Site Request Forgery) é um ataque onde um site malicioso faz o **seu** browser disparar uma request autenticada contra outra aplicação — abusando do fato de que o browser anexa o cookie de sessão **automaticamente**. O Spring Security liga a proteção **por default**: cada request mutating (POST/PUT/DELETE/PATCH) precisa carregar um token sincronizado que o atacante não consegue forjar. A regra prática: **web app com sessão em cookie → mantenha** o CSRF ligado; **API stateless com JWT no header `Authorization` → desligue**, porque o browser nunca envia esse header sozinho. CSRF é um problema de credencial-anexada-automaticamente, e cookie é a credencial automática por excelência.

## O que é

CSRF é um ataque que explora a **confiança que a aplicação deposita no browser do usuário**. O mecanismo central é simples e perverso: quando você está logado em `https://meubanco.example`, o browser guarda um cookie de sessão e o **reanexa em toda request** que sai para aquele domínio — não importa quem disparou a request.

O atacante hospeda uma página em `https://app.example.com` (um site qualquer que você visita). Essa página contém um form (ou um `<img>`, ou um `fetch`) que aponta para `https://meubanco.example/transfer`. Quando o seu browser carrega a página maliciosa e dispara a request, ele **anexa o cookie de sessão do banco automaticamente**. Do ponto de vista do servidor do banco, a request parece legítima: vem com a sessão válida do usuário autenticado.

O atacante não precisa **ler** nada nem roubar o cookie. Ele só precisa fazer o seu browser **agir** usando uma credencial que o próprio browser carrega sozinho. É forjar (forgery) uma request entre sites (cross-site).

## Por que importa

Porque a credencial mais comum em web apps tradicionais — o **cookie de sessão** — é exatamente a credencial que o browser envia automaticamente. Isso significa que **qualquer aplicação com login baseado em sessão-em-cookie é CSRF-vulnerável por construção**, a menos que você adicione uma defesa explícita.

O impacto é direto: transferências de dinheiro, troca de senha, deleção de conta, alteração de email — qualquer operação state-changing que dependa apenas do cookie pode ser disparada por um terceiro. O usuário nem percebe; basta visitar a página errada enquanto está logado.

Por isso o Spring Security **liga a proteção por default**. A decisão arquitetural deles é "seguro por padrão": você não esquece de ligar o CSRF — você precisa **conscientemente desligar** quando o modelo de autenticação torna o ataque impossível (como numa API stateless com token no header).

## Como funciona

### O ataque: request autenticada forjada via cookie

O coração do CSRF é a **automaticidade do cookie**. Imagine um endpoint de transferência:

```
POST https://meubanco.example/transfer
Cookie: JSESSIONID=abc123...   ← anexado pelo browser, sempre
to=atacante&amount=10000
```

Numa página maliciosa em `https://app.example.com`, o atacante coloca:

```html
<form action="https://meubanco.example/transfer" method="post" id="evil">
  <input type="hidden" name="to" value="atacante" />
  <input type="hidden" name="amount" value="10000" />
</form>
<script>document.getElementById('evil').submit();</script>
```

Você visita essa página enquanto está logado no banco em outra aba. O form submete sozinho, o browser anexa o `JSESSIONID`, e o banco processa a transferência como se **você** tivesse pedido. O atacante nunca viu seu cookie — só o usou indiretamente.

### CSRF on por default: token sincronizado em cada request mutating

A defesa do Spring é o **synchronizer token pattern**. O servidor gera um token secreto, imprevisível, e exige que ele venha em **toda request state-changing**. O atacante, hospedado em outro domínio, **não tem como ler** esse token (a same-origin policy o impede), então não consegue forjar uma request válida.

A regra de quais métodos exigem o token segue HTTP: métodos **mutating** (POST, PUT, DELETE, PATCH) precisam do token; métodos **read-only / safe** (GET, HEAD, OPTIONS, TRACE) são **isentos**, porque (em teoria) não alteram estado. Por isso você nunca coloca operação destrutiva atrás de um GET.

A configuração default já faz tudo isso:

```java
http.csrf(Customizer.withDefaults());
```

Por baixo, o `CsrfFilter` valida o token; o `CsrfTokenRequestAttributeHandler` (ou seu primo com proteção BREACH, `XorCsrfTokenRequestAttributeHandler`, que é o default) resolve o token do header ou do parâmetro e o disponibiliza como atributo da request.

### Web app com sessão cookie: mantenha CSRF

Se a sua autenticação é **sessão guardada em cookie** (`JSESSIONID` + `HttpSessionCsrfTokenRepository`, o repositório default), o ataque CSRF é **plausível** — o cookie viaja automaticamente. Portanto: **mantenha o CSRF ligado.** É a configuração que você ganha de graça com `Customizer.withDefaults()`. Desligar aqui é abrir um buraco direto.

### API stateless com JWT no header: desligue (o browser não envia Authorization automaticamente)

Numa API **stateless** que autentica via **JWT no header `Authorization: Bearer ...`**, o cenário muda por completo. O browser **não anexa o header `Authorization` automaticamente** — diferente do cookie, ele só vai na request se o seu próprio JavaScript o colocar lá, deliberadamente, request a request.

Isso destrói a premissa do CSRF: o atacante em outro domínio não consegue fazer o seu browser enviar o JWT, porque o browser não tem nada a anexar sozinho. Não há credencial automática a abusar. Logo, **a proteção CSRF é desnecessária** e só atrapalha:

```java
http.csrf(csrf -> csrf.disable());
```

(Lembre: isso vale para JWT **no header**. Se você guardar o JWT num **cookie**, voltou ao mundo do cookie automático e o CSRF importa de novo. Para a mecânica do token em si, veja a nota 08.)

### SPA + cookie session: CookieCsrfTokenRepository + X-XSRF-TOKEN

O caso híbrido: uma **SPA** (Angular, React) que autentica via **sessão em cookie** mas faz chamadas AJAX em vez de submeter forms HTML. Aqui você precisa de CSRF, mas o token não pode ficar só no HTML — o JavaScript precisa **lê-lo e reenviá-lo**.

A solução é o `CookieCsrfTokenRepository.withHttpOnlyFalse()`: o token vai num cookie chamado **`XSRF-TOKEN`** com `HttpOnly=false`, para que o JS consiga lê-lo. O cliente então copia o valor para o header **`X-XSRF-TOKEN`** em cada request mutating. O Spring valida o casamento.

```java
http.csrf(csrf -> csrf
    .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()));
```

Frameworks como o Angular já fazem o ciclo "lê `XSRF-TOKEN` → reenvia em `X-XSRF-TOKEN`" automaticamente, porque essas são justamente as convenções default.

## Na prática

Form server-rendered (Thymeleaf/JSP) com o token escondido no hidden field:

```html
<form action="/transfer" method="post">
  <input type="text" name="amount" />
  <input type="hidden"
         name="${_csrf.parameterName}"
         value="${_csrf.token}" />
  <button type="submit">Transferir</button>
</form>
```

Os dois cenários de config que você mais vai escrever:

```java
// API stateless com JWT no header Authorization → desliga CSRF
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http.csrf(csrf -> csrf.disable())
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .oauth2ResourceServer(oauth -> oauth.jwt(Customizer.withDefaults()));
    return http.build();
}

// SPA com sessão em cookie → mantém CSRF, mas via cookie legível pelo JS
@Bean
SecurityFilterChain web(HttpSecurity http) throws Exception {
    http.csrf(csrf -> csrf
            .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()))
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .formLogin(Customizer.withDefaults());
    return http.build();
}
```

## Armadilhas

### (1) Desabilitar CSRF num web app com sessão cookie

**Descrição.** A armadilha mais perigosa: copiar `http.csrf(csrf -> csrf.disable())` de um tutorial de API stateless para uma aplicação que autentica via **sessão em cookie**. O app fica imediatamente vulnerável a CSRF — qualquer página maliciosa pode disparar operações autenticadas.

**Exemplo.** Um `Order` service com login por form e `JSESSIONID`, mas com CSRF desligado "porque o tutorial mandou". Uma página em `https://app.example.com` submete um POST de cancelamento de pedido; o browser anexa o cookie de sessão do `Customer` logado; o pedido é cancelado sem o consentimento dele.

**Fix.** Em qualquer fluxo com sessão-em-cookie, **mantenha o default** (`Customizer.withDefaults()`). Só desligue CSRF quando a autenticação não usa credencial anexada automaticamente pelo browser.

### (2) Manter CSRF numa API stateless com JWT

**Descrição.** O inverso: deixar o CSRF ligado numa API stateless que autentica via `Authorization: Bearer`. Como o browser nunca envia esse header sozinho, não há ataque CSRF possível — mas o `CsrfFilter` passa a **exigir um token CSRF** que clients não-browser (curl, Postman, apps mobile, outro microsserviço) não têm como fornecer. As requests mutating quebram com `403`.

**Exemplo.** Um app mobile chama `POST /api/orders` com um JWT válido no header. A API responde `403 Forbidden` — não por causa do JWT, mas porque falta o token CSRF que o Spring ainda está exigindo. O time perde horas debugando "auth quebrada" que é, na verdade, CSRF ligado onde não devia.

**Fix.** Em API stateless com token no header, `http.csrf(csrf -> csrf.disable())`. O modelo de credencial torna o CSRF inaplicável; mantê-lo só gera falsos `403`.

### (3) SPA que não lê o cookie XSRF-TOKEN e reenvia no header X-XSRF-TOKEN

**Descrição.** Você configura `CookieCsrfTokenRepository.withHttpOnlyFalse()` no backend, mas o frontend SPA **não fecha o ciclo**: não lê o cookie `XSRF-TOKEN` nem o reenvia no header `X-XSRF-TOKEN`. Resultado: toda chamada mutating leva `403`, e parece que "o CSRF está bugado".

**Exemplo.** Uma SPA React faz `fetch('/api/orders', { method: 'POST', credentials: 'include', body })`. O cookie de sessão vai junto (por causa do `credentials: 'include'`), mas o header `X-XSRF-TOKEN` não — o dev esqueceu de lê-lo do cookie. O backend rejeita com `403` por token CSRF ausente.

**Fix.** Garanta que o cliente leia o cookie `XSRF-TOKEN` e copie o valor para o header `X-XSRF-TOKEN` em cada request mutating. No Angular, o `HttpClientXsrfModule` faz isso automaticamente; no React/fetch, você precisa implementar (ler `document.cookie` ou usar um interceptor que copie o valor para o header).

## Em entrevista

### Frase pronta (inglês)

> CSRF is an attack that abuses the browser's habit of automatically attaching the session cookie to every request for a given origin, letting a malicious page forge an authenticated state-changing request on the user's behalf. Spring Security enables CSRF protection by default using a synchronizer token that the attacker can't read across origins, and it only guards unsafe methods like POST, PUT, DELETE, and PATCH — safe methods like GET are exempt. The key design decision is matching the protection to the credential model: a session-cookie web app must keep CSRF on, but a stateless API authenticated with a JWT in the Authorization header can safely disable it, because the browser never sends that header automatically — only your own JavaScript does.

### Vocabulário

| Termo (EN) | Tradução / sentido |
| --- | --- |
| Cross-Site Request Forgery (CSRF) | falsificação de request entre sites |
| synchronizer token pattern | padrão de token sincronizado (defesa default) |
| state-changing / unsafe method | método que altera estado (POST/PUT/DELETE/PATCH) |
| safe method | método read-only e isento (GET/HEAD/OPTIONS) |
| session cookie | cookie de sessão (credencial anexada automaticamente) |
| stateless API | API sem estado de sessão no servidor |
| same-origin policy | política de mesma origem (impede o atacante de ler o token) |
| BREACH protection | proteção contra BREACH (token "xorado" por request) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|OAuth2 Resource Server]]
- [[03-Dominios/Tecnologia/Java/Segurança/11 - CORS — a borda, o preflight e a config de segurança|CORS]]
- [[03-Dominios/Tecnologia/Java/Segurança/06 - A arquitetura do filter chain em profundidade|A arquitetura do filter chain]]
- [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- Spring Security Reference — CSRF: https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html
