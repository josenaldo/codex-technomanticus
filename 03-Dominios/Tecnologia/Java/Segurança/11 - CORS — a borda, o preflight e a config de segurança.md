---
title: "CORS — a borda, o preflight e a config de segurança"
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
  - cors
aliases:
  - "CORS"
  - "Cross-Origin Resource Sharing"
---

# CORS — a borda, o preflight e a config de segurança

> [!abstract] TL;DR
> **CORS (Cross-Origin Resource Sharing)** é um mecanismo do **browser** que libera (ou bloqueia) requests que saem de uma origem para outra. Ele **não é segurança do servidor**: quem ignora CORS — `curl`, Postman, um script — passa direto. A autenticação continua sendo obrigatória de qualquer jeito. No Spring Security, você configura origens **explícitas** (nunca `*` junto com credentials), registra um `CorsConfigurationSource` e pluga ele no filter chain com `http.cors(Customizer.withDefaults())`, de modo que o `CorsFilter` rode **cedo**, antes da autenticação.

## O que é

CORS é uma especificação do browser que controla quando um JavaScript rodando na origem `A` pode ler a resposta de um request feito para a origem `B`. "Origem" é a tripla **esquema + host + porta** (`https://app.example.com:443`). Se qualquer um dos três difere, o request é **cross-origin**.

Por padrão, o browser aplica a **same-origin policy**: o JS pode disparar o request, mas não consegue **ler** a resposta de outra origem, a menos que o servidor responda com os cabeçalhos `Access-Control-Allow-*` certos. CORS é justamente o protocolo desses cabeçalhos — uma negociação entre o que o servidor permite e o que o browser deixa o script enxergar.

O detalhe que confunde todo mundo: **CORS é uma permissão de leitura imposta pelo browser**, não uma muralha no servidor. O servidor sempre recebe e processa o request; o browser é quem decide se entrega a resposta de volta ao JS.

## Por que importa

Toda SPA moderna esbarra em CORS. O front roda em `https://app.example.com`, a API em `https://api.example.com` — origens diferentes, logo cross-origin. Sem configuração, o browser bloqueia a leitura da resposta e você vê o clássico erro no console:

```
Access to fetch at 'https://api.example.com/users' from origin
'https://app.example.com' has been blocked by CORS policy.
```

Importa também porque é um ponto onde se erra para os **dois lados**:

- **Frouxo demais**: liberar `*` com credentials, ou refletir qualquer origem, abre brecha de CSRF-like e vazamento de dados autenticados.
- **Apertado demais**: esquecer de liberar o método `PUT`, ou um header custom, e o **preflight** falha — o request real nem sai.

E há a armadilha conceitual mais perigosa: tratar CORS como se fosse **autorização**. Não é. Quem entende isso configura CORS para a ergonomia do browser e protege o servidor com autenticação de verdade.

## Como funciona

### CORS é do browser, não do servidor (curl bypassa — não é segurança server-side)

O servidor não "bloqueia" nada por CORS. Ele responde normalmente; o **browser** é quem inspeciona os cabeçalhos `Access-Control-Allow-Origin` e decide se o JS pode ler a resposta. Ferramentas que não são browsers — `curl`, Postman, um cliente HTTP em Python, um cron — **ignoram CORS por completo**.

```bash
# Funciona perfeitamente, sem nenhum header CORS — curl não liga pra origem
curl https://api.example.com/users
```

A consequência prática: se o seu único controle de acesso fosse CORS, qualquer atacante com `curl` leria tudo. Por isso **CORS nunca substitui autenticação/autorização**. Pense nele como uma conveniência do navegador, não como um portão. O portão é o filter chain de segurança (ver [[03-Dominios/Tecnologia/Java/Segurança/06 - A arquitetura do filter chain em profundidade|A arquitetura do filter chain]]).

### CorsConfigurationSource: origens, métodos, headers, credentials

No Spring Security, a forma canônica de configurar CORS é expor um bean `CorsConfigurationSource` (na prática, um `UrlBasedCorsConfigurationSource`, que mapeia padrões de path para uma `CorsConfiguration`). Os principais setters da `CorsConfiguration`:

| Método | O que controla |
| --- | --- |
| `setAllowedOrigins` | Lista de origens exatas liberadas (`https://app.example.com`) |
| `setAllowedOriginPatterns` | Origens por padrão (`https://*.example.com`); permite curinga com credentials |
| `setAllowedMethods` | Verbos HTTP liberados (`GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`) |
| `setAllowedHeaders` | Headers de request liberados (`Authorization`, `Content-Type`, custom) |
| `setAllowCredentials` | Se cookies/`Authorization` cross-origin são permitidos (`true`/`false`) |
| `setMaxAge` | Quantos segundos o browser pode cachear o resultado do preflight |

Cada um vira um cabeçalho de resposta: `setAllowedOrigins` → `Access-Control-Allow-Origin`, `setAllowedMethods` → `Access-Control-Allow-Methods`, e assim por diante. O `UrlBasedCorsConfigurationSource.registerCorsConfiguration("/**", config)` aplica a config a todos os paths.

### O preflight OPTIONS: quando o browser pergunta antes

Para requests "simples" (um `GET` ou um `POST` com `Content-Type` básico, sem headers custom), o browser manda o request direto e só checa os cabeçalhos na resposta. Mas para requests **"complexos"** — método `PUT`/`DELETE`, `Content-Type: application/json`, ou qualquer header custom como `Authorization` ou `X-Trace-Id` — o browser primeiro dispara um **preflight**: um request `OPTIONS` perguntando "posso?".

```
OPTIONS /users HTTP/1.1
Origin: https://app.example.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: Authorization, Content-Type
```

O servidor responde com os `Access-Control-Allow-*` correspondentes. Só **se** o preflight aprovar é que o browser envia o request real. Um detalhe crítico de segurança: **o preflight não carrega cookies/`JSESSIONID`** — por isso ele precisa ser tratado **antes** da autenticação no filter chain (ver o último H3). O `setMaxAge` existe justamente para o browser não repetir o preflight a cada chamada.

### allowedOrigins('*') + allowCredentials(true): por que o browser rejeita

A especificação CORS **proíbe** combinar o curinga `*` em `Access-Control-Allow-Origin` com `Access-Control-Allow-Credentials: true`. Liberar "qualquer origem" **e** mandar credenciais ao mesmo tempo seria um vazamento universal de dados autenticados — qualquer site poderia ler respostas logadas do seu usuário.

Quando você configura `setAllowedOrigins(List.of("*"))` junto com `setAllowCredentials(true)`, o browser **rejeita** a resposta com erro, mesmo o servidor tendo respondido. A saída:

- **Origens explícitas**: `setAllowedOrigins(List.of("https://app.example.com"))` — o jeito mais seguro.
- **`setAllowedOriginPatterns`**: introduzido justamente para esse caso. Aceita curinga (`https://*.example.com`) e, em runtime, **reflete a origem concreta** que bateu no padrão de volta no header — nunca o literal `*` — então funciona com credentials.

### CORS no filter chain (Spring Security) vs config MVC (Galho 9)

Há dois lugares para configurar CORS no Spring, e eles operam em **camadas diferentes**. O Galho 9 (Web/MVC) tratou CORS como **configuração MVC** — `@CrossOrigin` em controllers e `WebMvcConfigurer#addCorsMappings` —, que roda no nível do `DispatcherServlet`, **depois** que o request já atravessou os filtros de segurança. Para o detalhe dessa camada (filtros vs interceptors no MVC), veja [[03-Dominios/Tecnologia/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]].

Aqui, na borda de segurança, o CORS precisa rodar **antes** da autenticação — porque o preflight `OPTIONS` chega **sem cookies** e seria barrado por uma cadeia de auth que não o reconhece. Por isso o Spring Security tem o seu próprio `CorsFilter`, posicionado bem no início do filter chain. Você o ativa com:

```java
http.cors(Customizer.withDefaults());
```

Isso instrui o Security a pegar o bean `CorsConfigurationSource` do contexto e instalar o `CorsFilter` antes dos filtros de autenticação. Resultado: o preflight é respondido cedo e o request real autenticado segue normalmente. **Regra prática**: numa app com Spring Security, configure CORS pelo `http.cors(...)` + bean, não pelo `WebMvcConfigurer` — senão o preflight pode ser barrado pela camada de segurança antes de chegar ao MVC.

## Na prática

Um bean `CorsConfigurationSource` com origens explícitas e credentials, plugado no filter chain:

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.List;

@Configuration
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // pega o bean CorsConfigurationSource e instala o CorsFilter cedo,
            // antes da autenticacao
            .cors(Customizer.withDefaults())
            .authorizeHttpRequests(auth -> auth
                .anyRequest().authenticated()
            )
            .httpBasic(Customizer.withDefaults());
        return http.build();
    }

    @Bean
    CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        // origens EXPLICITAS — nunca "*" junto com credentials
        config.setAllowedOrigins(List.of("https://app.example.com"));
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L); // cacheia o preflight por 1h

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }
}
```

Com isso, o preflight `OPTIONS` é respondido pelo `CorsFilter` no início da cadeia, e o request real autenticado (com `Authorization`) segue para os filtros de auth.

## Armadilhas

### (1) `allowedOrigins("*")` + `allowCredentials(true)`

A combinação proibida pela spec. O browser **rejeita** a resposta, mesmo o servidor respondendo 200, e você vê um erro de CORS no console que parece "do nada".

```java
// QUEBRA no browser: curinga + credentials e' invalido
config.setAllowedOrigins(List.of("*"));
config.setAllowCredentials(true);
```

**Fix**: use origens explícitas, ou `setAllowedOriginPatterns` (que reflete a origem concreta em vez do literal `*`):

```java
config.setAllowedOriginPatterns(List.of("https://*.example.com"));
config.setAllowCredentials(true); // agora OK
```

### (2) Assumir que CORS protege o servidor

Tratar CORS como controle de acesso. CORS só é respeitado pelo **browser**; `curl`, Postman e qualquer script HTTP **ignoram** os cabeçalhos e leem a resposta normalmente.

```bash
# Le a resposta sem nenhum header CORS — CORS nao protege nada aqui
curl -H "Authorization: Bearer <token>" https://api.example.com/users
```

**Fix**: trate CORS como ergonomia do browser e proteja o endpoint com **autenticação e autorização de verdade** no filter chain. CORS nunca substitui auth.

### (3) Preflight OPTIONS bloqueado

Um request "complexo" (header custom, `PUT`, JSON) dispara um preflight `OPTIONS` que **falha antes** do request real sair — geralmente porque o método ou o header custom não foi liberado, ou porque o `OPTIONS` foi barrado pela autenticação (lembre: o preflight chega **sem cookies**).

```java
// Front manda header custom X-Trace-Id, mas ele nao esta liberado
// -> preflight falha, request real nem acontece
config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
// faltou "X-Trace-Id"
```

**Fix**: inclua todos os métodos e headers que o front usa (`config.setAllowedHeaders(List.of("Authorization", "Content-Type", "X-Trace-Id"))`) e garanta o CORS no filter chain via `http.cors(...)`, para o `CorsFilter` responder o `OPTIONS` antes da autenticação.

## Em entrevista

### Frase pronta (inglês)

> CORS is a **browser** mechanism, not server-side security — `curl` and Postman ignore it entirely, so authentication is always mandatory regardless of CORS. For complex requests, the browser sends a **preflight** `OPTIONS` to ask which methods and headers are allowed before the real request goes out. In Spring Security I expose a `CorsConfigurationSource` bean with **explicit origins** — never `*` together with `allowCredentials(true)`, which the browser rejects — and wire it with `http.cors(Customizer.withDefaults())` so the `CorsFilter` runs early, before authentication, since the preflight arrives without cookies.

### Vocabulário

| Termo (EN) | Tradução / nota |
| --- | --- |
| Cross-Origin Resource Sharing (CORS) | compartilhamento de recursos entre origens |
| same-origin policy | política de mesma origem (padrão do browser) |
| preflight request | request preliminar (`OPTIONS`) para requests complexos |
| `Access-Control-Allow-Origin` | header de resposta que libera a origem |
| allowed origins / origin patterns | origens liberadas / padrões de origem |
| credentials (cookies, auth header) | credenciais enviadas cross-origin |

## Veja também

- [[03-Dominios/Tecnologia/Java/Segurança/10 - CSRF — por que ligado por default e quando desligar|CSRF]]
- [[03-Dominios/Tecnologia/Java/Segurança/06 - A arquitetura do filter chain em profundidade|A arquitetura do filter chain]] (o `CorsFilter` na cadeia)
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]] (onde o Galho 9 tratou filtros/CORS na camada MVC)
- [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]] (verbete CORS)

## Referências

- Spring Security Reference — CORS: https://docs.spring.io/spring-security/reference/servlet/integrations/cors.html
