---
title: "Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder"
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
  - password
aliases:
  - "Password encoding"
  - "BCrypt"
  - "DelegatingPasswordEncoder"
---

# Password encoding — BCrypt, Argon2 e o DelegatingPasswordEncoder

> [!abstract] TL;DR
> Senha **nunca** vai em plain text no banco. O `PasswordEncoder` faz o hash de mão única (one-way): você `encode` na hora de cadastrar e `matches` na hora de logar, mas nunca consegue "decodar" de volta. O **BCrypt** é o default razoável — propositalmente lento (slow-by-design) pra atrapalhar quem tenta força bruta. E o **`DelegatingPasswordEncoder`** carimba um prefixo `{id}` no hash (tipo `{bcrypt}$2a$10$...`) pra você poder trocar de algoritmo no futuro sem quebrar os logins de quem já tem senha cadastrada.

## O que é

`PasswordEncoder` é a interface do Spring Security responsável por transformar uma senha em texto puro num hash que pode ser guardado com segurança. Ela tem dois métodos que importam:

- `encode(rawPassword)` — recebe a senha digitada e devolve o hash que vai pro banco.
- `matches(rawPassword, encodedPassword)` — recebe a senha digitada no login e o hash guardado, e diz se batem.

Repare no que **não** existe: um método `decode`. Hash é via de mão única. O sistema nunca recupera a senha original — só compara. Por isso "esqueci minha senha" sempre te manda criar uma nova, nunca te mostra a antiga.

O Spring Security oferece várias implementações dessa interface (BCrypt, Argon2, Pbkdf2, SCrypt) e uma especial — o `DelegatingPasswordEncoder` — que orquestra as outras.

## Por que importa

Bancos de dados vazam. É só questão de quando. Quando o dump da tabela `users` cair na mão de um atacante, a única coisa entre ele e as senhas dos seus usuários é o quão bem você fez o hash.

Se você guardou plain text, acabou: ele tem tudo. Se guardou um hash rápido tipo MD5 ou SHA-256, ele roda bilhões de tentativas por segundo numa GPU e quebra a maioria das senhas comuns em minutos. Se guardou um hash adaptativo e lento como BCrypt ou Argon2, cada tentativa custa caro o suficiente pra força bruta deixar de valer a pena.

Como muita gente reusa senha entre serviços, um vazamento mal protegido não compromete só o seu sistema — compromete o e-mail, o banco e tudo mais daquele usuário. Hash forte é responsabilidade básica.

## Como funciona

### PasswordEncoder: encode e matches (nunca decode — hash é one-way)

O contrato é simples e a ausência de `decode` é proposital:

```java
PasswordEncoder encoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();

String hash = encoder.encode("s3nh4-do-usuario");
// guarda 'hash' no banco

boolean ok = encoder.matches("s3nh4-do-usuario", hash); // true
boolean nope = encoder.matches("chute-errado", hash);    // false
```

Um detalhe importante: bons encoders embutem um **salt** aleatório dentro do próprio hash. Por isso a mesma senha gera hashes diferentes a cada `encode` — e mesmo assim o `matches` funciona, porque o salt fica guardado no resultado. Isso derruba ataques de rainbow table.

### BCrypt (default), Argon2, Pbkdf2: o que muda e o work factor

Todos são funções adaptativas de mão única, mas com características diferentes:

| Encoder | Classe | Característica | Quando escolher |
| --- | --- | --- | --- |
| BCrypt | `BCryptPasswordEncoder` | Lento por design, work factor (strength) ajustável; default 10 | Default razoável pra apps novos |
| Argon2 | `Argon2PasswordEncoder` | Memory-hard; venceu a Password Hashing Competition (exige BouncyCastle) | Quando quer o estado da arte |
| Pbkdf2 | `Pbkdf2PasswordEncoder` | Function de derivação de chave; FIPS-friendly | Requisito de certificação FIPS |
| SCrypt | `SCryptPasswordEncoder` | Memory-hard, resiste a hardware dedicado | Defesa contra ASIC/GPU |
| NoOp | `NoOpPasswordEncoder` | Sem hash nenhum (plain text) — **deprecated** | Só legado/teste |

O **work factor** (no BCrypt, chamado de *strength*) é o número de iterações: quanto maior, mais lento o hash. O default do BCrypt é 10. A própria doc do Spring sugere ajustar a strength de forma que verificar uma senha leve em torno de 1 segundo no seu hardware — lento o bastante pra atrapalhar o atacante, rápido o bastante pra não travar seus logins. Como é adaptativo, você aumenta a strength conforme o hardware fica mais rápido com o tempo.

```java
// strength 16 em vez do default 10 (cada incremento ~dobra o custo)
BCryptPasswordEncoder forte = new BCryptPasswordEncoder(16);
```

### DelegatingPasswordEncoder: o prefixo {bcrypt}$... e a migração gradual

Aqui mora a sacada de engenharia. Em vez de amarrar seu sistema a um único algoritmo pra sempre, o `DelegatingPasswordEncoder` guarda no início de cada hash um **prefixo entre chaves** indicando qual encoder gerou aquele hash:

```text
{bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG
{argon2}$argon2id$v=19$m=16384,t=2,p=1$...
{noop}senhaEmTextoPuro
```

Na hora do `matches`, ele lê o `{id}`, descobre qual encoder usar e delega a verificação pra ele. Na hora do `encode`, ele usa o algoritmo "atual" (por padrão, bcrypt) e carimba o prefixo correspondente.

O ganho: você pode ter no banco senhas em formatos diferentes ao mesmo tempo. Logins antigos com `{bcrypt}` continuam funcionando enquanto novos cadastros já saem em `{argon2}`, sem downtime e sem forçar todo mundo a redefinir senha de uma vez. Pra trazer um legado de plain text pra dentro desse esquema, basta prefixar os hashes existentes com `{noop}` e ir migrando.

### Por que slow-by-design protege contra brute force

Parece contraintuitivo querer que algo seja lento. A lógica: um login legítimo acontece uma vez e tolera tranquilamente 200ms ou 500ms a mais. Já um atacante precisa testar **milhões ou bilhões** de combinações. Se cada tentativa custa uma fração de segundo de CPU/memória, o custo total da força bruta explode e fica inviável.

Hashes rápidos como MD5/SHA-256 foram feitos pra serem velozes — ótimo pra checksum, péssimo pra senha, porque uma GPU calcula bilhões por segundo. BCrypt e Argon2 invertem isso de propósito: são caros pra calcular e, no caso do Argon2/SCrypt, também caros em memória, o que neutraliza hardware paralelo barato.

## Na prática

Declare o encoder como um `@Bean` e o Spring Security o injeta onde precisar (no fluxo de autenticação e onde você cadastra usuários):

```java
@Configuration
public class SecurityConfig {

    @Bean
    public PasswordEncoder passwordEncoder() {
        // Opção recomendada: delega e suporta migração futura via prefixo {id}
        return PasswordEncoderFactories.createDelegatingPasswordEncoder();

        // Alternativa direta, sem prefixo:
        // return new BCryptPasswordEncoder();
    }
}
```

Usando no cadastro e no login:

```java
@Service
public class CustomerService {

    private final PasswordEncoder encoder;
    private final CustomerRepository repository;

    public CustomerService(PasswordEncoder encoder, CustomerRepository repository) {
        this.encoder = encoder;
        this.repository = repository;
    }

    public void register(String username, String rawPassword) {
        String hash = encoder.encode(rawPassword); // {bcrypt}$2a$10$...
        repository.save(new Customer(username, hash));
    }

    public boolean checkLogin(Customer customer, String rawPassword) {
        return encoder.matches(rawPassword, customer.getPasswordHash());
    }
}
```

O que fica guardado no banco com o `DelegatingPasswordEncoder`:

```text
{bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG
```

## Armadilhas

### (1) Plain text ou hash rápido (MD5/SHA) — slow-by-design existe por um motivo

Guardar senha em texto puro é o pior caso, mas usar um hash rápido (MD5, SHA-1, SHA-256 cru) é quase tão ruim: esses algoritmos foram projetados pra velocidade, então uma GPU quebra senhas comuns em minutos.

```java
// ERRADO — SHA-256 cru não é slow-by-design
String hash = DigestUtils.sha256Hex(rawPassword);
```

**Fix:** use um encoder adaptativo do Spring Security. BCrypt resolve a grande maioria dos casos; Argon2 se quiser o estado da arte.

```java
// CERTO
PasswordEncoder encoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();
String hash = encoder.encode(rawPassword);
```

### (2) NoOpPasswordEncoder em produção (deprecated, sem hash nenhum)

`NoOpPasswordEncoder` não faz hash — ele guarda a senha em texto puro, identificada pelo prefixo `{noop}`. Está **deprecated** justamente pra desencorajar uso. Aparece em tutoriais antigos e dá a falsa sensação de "ter um encoder configurado".

```java
// ERRADO em produção — guarda {noop}senhaEmTextoPuro
@Bean
public PasswordEncoder passwordEncoder() {
    return NoOpPasswordEncoder.getInstance();
}
```

**Fix:** troque pelo `DelegatingPasswordEncoder`. Se você tem um legado de plain text, prefixe os valores antigos com `{noop}` só durante a transição e migre cada usuário pro BCrypt no próximo login bem-sucedido.

### (3) Work factor baixo demais (inseguro) ou alto demais (latência de login)

A strength do BCrypt é um trade-off. Baixa demais (tipo 4) deixa o hash rápido e enfraquece a proteção contra força bruta. Alta demais (tipo 18 num servidor modesto) faz cada login custar muito tempo de CPU — e, sob carga, um pico de logins pode até virar vetor de negação de serviço.

```java
// Extremos problemáticos
new BCryptPasswordEncoder(4);   // fraco demais
new BCryptPasswordEncoder(18);  // pode pesar em hardware modesto
```

**Fix:** comece pelo default (10) e calibre medindo o tempo real de verificação no seu próprio hardware, mirando algo na casa de ~1 segundo conforme a recomendação da doc. Reavalie esse número de tempos em tempos, já que hardware fica mais rápido.

## Em entrevista

### Frase pronta (inglês)

> Passwords must never be stored in plain text. In Spring Security, a `PasswordEncoder` performs a one-way hash: you `encode` the password on signup and `matches` it on login, but you can never decode it back. BCrypt is the sensible default because it is slow by design — that deliberate cost is what makes brute-force attacks impractical, while a legitimate login barely notices. For long-lived systems I prefer the `DelegatingPasswordEncoder`, which prefixes each hash with an `{id}` like `{bcrypt}` so I can migrate to a stronger algorithm such as Argon2 later without breaking existing logins.

### Vocabulário

| Termo (EN) | Tradução / sentido |
| --- | --- |
| one-way hash | hash de mão única (sem volta/decode) |
| password encoding | codificação/hash de senha |
| work factor / strength | custo computacional ajustável do hash |
| slow-by-design | propositalmente lento (defesa contra brute force) |
| salt | valor aleatório embutido no hash, anti rainbow table |
| brute-force attack | ataque de força bruta |
| credential stuffing | reuso de credenciais vazadas em outros serviços |
| password migration | migração gradual entre algoritmos de hash |

## Veja também

- [[03-Dominios/Tecnologia/Java/Segurança/03 - Autenticação — UserDetailsService, AuthenticationManager, Form e Basic|Autenticação]]
- [[03-Dominios/Tecnologia/Java/Segurança/16 - OWASP Top 10 no contexto Java|OWASP Top 10 no contexto Java]]
- [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]] (verbetes PasswordEncoder / BCryptPasswordEncoder / DelegatingPasswordEncoder)

## Referências

- Spring Security Reference — Password Storage: https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html
