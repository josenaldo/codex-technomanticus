---
title: "Exceções e tratamento de erros"
created: 2026-06-02
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - linguagem
  - adepto
  - exceptions
  - erros
aliases:
  - Exceções
  - try-with-resources
---

# Exceções e tratamento de erros

> [!abstract] TL;DR
> **Exceções** são o mecanismo de Java para sinalizar erros fora do fluxo normal de execução. A hierarquia começa em `Throwable`, que se divide em `Error` (erros da JVM — não capturar) e `Exception` (erros de aplicação). `Exception` se subdivide em **checked** (o compilador obriga a tratar) e **unchecked** (subclasses de `RuntimeException` — sem obrigação). O debate checked vs unchecked não tem resposta dogmática: frameworks modernos preferem unchecked, mas checked ainda faz sentido quando o caller tem como se recuperar. **`try-with-resources`** (Java 7+) fecha recursos `AutoCloseable` automaticamente, em ordem reversa, e resolve a armadilha de exceções suprimidas que o `finally` manual introduzia. **Custom exceptions** devem herdar de `RuntimeException`, preservar a causa original e carregar contexto de negócio. Anti-patterns fatais: catch vazio (swallow), catch de `Exception`/`Throwable` indiscriminado, e `return`/`throw` dentro de `finally`.

## O que é

Uma **exceção** é um evento que interrompe o fluxo normal de execução de um programa — um sinal de que algo deu errado em um ponto que a lógica principal não esperava tratar diretamente. Em vez de usar códigos de retorno especiais (como `-1` ou `null`), Java modela erros como objetos que "voam" pela pilha de chamadas até serem capturados pelo bloco `catch` adequado, ou terminam o programa se não forem tratados.

Isso separa o código de caminho feliz (happy path) do código de tratamento de erro: o método que detecta o problema lança a exceção, e o código que sabe como reagir a captura — potencialmente vários níveis acima na call stack.

```java
// Sem exceções (estilo C)
int result = parseInt(input);
if (result == -1) { /* como distinguir erro de valor válido? */ }

// Com exceções (Java)
try {
    int result = Integer.parseInt(input);  // lança NumberFormatException se inválido
    process(result);
} catch (NumberFormatException e) {
    log.warn("Entrada inválida: {}", input);
}
```

## Como funciona

### Hierarquia (`Throwable` → `Error` / `Exception` → `RuntimeException`)

Toda exceção em Java é um objeto que estende `Throwable`. A hierarquia tem dois ramos principais:

```text
Throwable
  ├── Error
  │     ├── OutOfMemoryError
  │     ├── StackOverflowError
  │     ├── VirtualMachineError
  │     └── AssertionError
  │
  └── Exception
        ├── IOException
        ├── SQLException
        ├── InterruptedException
        ├── ClassNotFoundException
        │     ... (outras checked)
        │
        └── RuntimeException         ← unchecked
              ├── NullPointerException
              ├── IllegalArgumentException
              ├── IllegalStateException
              ├── IndexOutOfBoundsException
              ├── ClassCastException
              ├── ArithmeticException
              └── UnsupportedOperationException
```

**`Error`** representa falhas graves da JVM ou do ambiente de execução — situações em que o sistema está tão comprometido que tentar se recuperar é perigoso ou impossível. `OutOfMemoryError` significa que o heap acabou; `StackOverflowError` significa que a pilha de chamadas estourou (geralmente recursão infinita). A regra prática é **não capturar `Error`**: o programa está em estado inconsistente e a única ação sensata é deixar a JVM encerrar, liberar o processo, e deixar o orquestrador (Kubernetes, systemd) reiniciá-lo.

**`Exception`** representa condições que o código de aplicação pode razoavelmente tratar. É dividida em duas categorias:

- **Checked exceptions** — subclasses diretas de `Exception` que *não* são `RuntimeException`. O compilador exige que todo método que pode lançá-las declare `throws X` ou as capture com `try/catch`. Exemplos: `IOException`, `SQLException`, `InterruptedException`.
- **Unchecked exceptions** — subclasses de `RuntimeException`. O compilador não exige declaração nem captura. Exemplos: `NullPointerException`, `IllegalArgumentException`. Geralmente indicam bugs de programação (contrato violado) ou erros que o caller não tem como antecipar.

---

### Checked vs unchecked — o debate

O debate é real e tem argumentos sérios dos dois lados. A posição mais útil é **pragmática**, não dogmática.

**Argumentos a favor de checked exceptions:**

- O compilador força o caller a pensar sobre o que fazer quando uma operação falha.
- Documentam explicitamente no contrato do método quais falhas são possíveis.
- Fazem sentido quando a falha é esperada, o caller tem como se recuperar, e ignorar seria um bug silencioso. Exemplo: uma interface de leitura de arquivo onde `IOException` é um caso de uso legítimo que o caller precisa tratar.

**Argumentos contra checked exceptions (e pela tendência unchecked):**

- **Poluição de assinatura**: `throws IOException, SQLException, ParseException` sobe pela call stack inteira, expondo detalhes de implementação para camadas que nada podem fazer com eles.
- **Vazamento de abstração**: uma interface de repositório de alto nível que declara `throws SQLException` está amarrada à tecnologia de persistência que usa.
- **Incompatibilidade com lambdas e streams**: interfaces funcionais (`Consumer<T>`, `Function<T,R>`) não declaram checked exceptions — qualquer lambda com uma operação checked obriga a wrapping manual.
- **Supressão silenciosa**: quando o custo de tratar é alto, programadores frequentemente escrevem `catch (Exception e) {}` vazio para silenciar o compilador — o pior dos mundos.

**Tendência moderna:** a maioria das bibliotecas contemporâneas (Spring, Hibernate/JPA, Project Reactor, gRPC Java) adota unchecked como default. O próprio Java reconhece o problema — `java.io.UncheckedIOException` foi adicionado justamente para wrapear `IOException` em contextos funcionais.

**Quando usar cada um:**

| Situação | Recomendação |
|---|---|
| O caller *pode* se recuperar e *deve* ser forçado a pensar nisso | Checked pode fazer sentido |
| Falha indica bug de programação (argumento nulo, estado inválido) | Unchecked — `IllegalArgumentException`, `IllegalStateException` |
| Biblioteca / framework com API pública de alto nível | Unchecked — não force seus detalhes de implementação no caller |
| Código com lambdas e streams | Unchecked — checked não atravessa interfaces funcionais |
| Default quando a dúvida existir | Unchecked |

---

### `try` / `catch` / `finally`

A estrutura básica de tratamento:

```java
try {
    // código que pode lançar exceção
    String conteudo = Files.readString(Path.of("dados.txt"));
    processar(conteudo);

} catch (IOException e) {
    // captura IOException e suas subclasses
    log.error("Falha ao ler arquivo", e);
    throw new ProcessingException("Arquivo indisponível", e);

} catch (ProcessingException e) {
    // captura exceção mais específica — ordem importa: do mais específico ao mais geral
    log.warn("Erro de processamento", e);

} finally {
    // executa SEMPRE: com ou sem exceção, com ou sem return
    contadorTentativas.increment();
}
```

**Regras importantes:**

- A ordem dos blocos `catch` importa: o mais específico deve vir antes do mais geral. Um `catch (Exception e)` antes de um `catch (IOException e)` faz o segundo tornar-se código morto — o compilador emite erro.
- `finally` **sempre executa** — mesmo se houver `return` no bloco `try` ou `catch`. É o mecanismo histórico de garantia de limpeza.
- Se tanto `catch` quanto `finally` lançarem exceções, a exceção do `finally` substitui a original — a do `catch` é perdida. Esse comportamento silencioso é uma das razões para preferir `try-with-resources`.

**Multi-catch** (Java 7+): quando dois ou mais tipos de exceção devem ter o mesmo tratamento, use `|` para evitar duplicação:

```java
try {
    executar();
} catch (IOException | SQLException e) {
    // variável 'e' é implicitamente final
    log.error("Falha de I/O ou BD", e);
    throw new ServiceException("Operação falhou", e);
}
```

A variável do multi-catch é implicitamente `final` — não pode ser reatribuída dentro do bloco.

---

### try-with-resources

Introduzido no Java 7, `try-with-resources` fecha automaticamente qualquer recurso que implemente `java.lang.AutoCloseable`. É a maneira correta de lidar com recursos como conexões, streams e arquivos.

```java
// Antes (Java 6) — verboso e propenso a bugs
BufferedReader reader = null;
try {
    reader = new BufferedReader(new FileReader("dados.csv"));
    processar(reader.readLine());
} catch (IOException e) {
    log.error("Erro de leitura", e);
} finally {
    if (reader != null) {
        try {
            reader.close();  // close() pode lançar também
        } catch (IOException ex) {
            log.error("Erro ao fechar", ex);
        }
    }
}

// Com try-with-resources (Java 7+) — correto e conciso
try (var reader = new BufferedReader(new FileReader("dados.csv"))) {
    processar(reader.readLine());
} catch (IOException e) {
    log.error("Erro de leitura", e);
}
// reader.close() é chamado automaticamente ao sair do bloco
```

**Múltiplos recursos** — separados por `;` na declaração:

```java
try (var zipFile   = new ZipFile(zipFileName);
     var writer    = Files.newBufferedWriter(outputPath, StandardCharsets.UTF_8)) {
    // usa zipFile e writer
}
// writer.close() é chamado PRIMEIRO, depois zipFile.close()
// (ordem reversa à de declaração)
```

**Ordem de fechamento:** recursos são fechados na **ordem inversa** à de sua declaração — o último declarado é o primeiro fechado. Isso espelha a ordem natural de dependência: se `writer` depende de `zipFile`, faz sentido fechar `writer` antes.

**Exceções suprimidas:** se o bloco `try` lança uma exceção e, durante o fechamento automático, o método `close()` de um recurso também lança, a exceção do `close()` é **suprimida** (não substitui a original). A exceção primária é propagada normalmente; as suprimidas ficam acessíveis via `Throwable.getSuppressed()`. Isso é superior ao `finally` manual, onde a exceção do `close()` substituiria a original silenciosamente.

```java
try {
    throw new RuntimeException("erro original");
} catch (RuntimeException e) {
    Throwable[] suprimidas = e.getSuppressed();  // exceções do close()
    for (Throwable s : suprimidas) {
        log.warn("Exceção suprimida: {}", s.getMessage());
    }
    throw e;
}
```

**Blocos `catch` e `finally` com `try-with-resources`** executam *depois* que os recursos já foram fechados — garantia importante para quem usa o recurso no bloco `catch`.

---

### Custom exceptions — boas práticas

Criar exceções de domínio torna o código mais expressivo e facilita o tratamento em camadas superiores (ex.: mapear para HTTP status em uma API REST).

```java
// Exceção de domínio — unchecked, com contexto rico
public class PacienteNaoEncontradoException extends RuntimeException {

    private final Long pacienteId;

    public PacienteNaoEncontradoException(Long id) {
        super("Paciente não encontrado: id=" + id);
        this.pacienteId = id;
    }

    // Construtor com cause — para wrapping
    public PacienteNaoEncontradoException(Long id, Throwable cause) {
        super("Paciente não encontrado: id=" + id, cause);
        this.pacienteId = id;
    }

    public Long getPacienteId() {
        return pacienteId;
    }
}
```

**Preservar a cause — exception chaining:**

```java
try {
    return repositorio.buscarPaciente(id);
} catch (DataAccessException e) {
    // Wrapping: preserva a causa original na chain
    throw new PacienteNaoEncontradoException(id, e);
}
```

**Regras para custom exceptions:**

- **Herdar de `RuntimeException`** para unchecked (default moderno).
- **Mensagens úteis** com dados concretos: `"id=42"` em vez de `"not found"`.
- **Preservar a causa** — nunca `throw new MinhaException("msg")` descartando a original; passe-a como `cause`.
- **Não criar exceção para controle de fluxo** — exceções têm custo (capturar stack trace); se você as usa como `if/else`, está abusando do mecanismo.
- **Localizar no domínio** — `com.empresa.dominio.exception`, não em `util.exceptions` genérico.
- **Não criar uma hierarquia extensa** — exceções de domínio geralmente não precisam de subhierarquias elaboradas. Prefira uma ou duas exceções com campos de contexto a uma árvore de subclasses.

## Na prática

### Exceções em lambdas e streams

O ponto de atrito mais frequente em Java moderno: **checked exceptions não atravessam interfaces funcionais**. `Consumer<T>`, `Function<T,R>` e similares não declaram `throws`, então qualquer operação checked dentro de uma lambda não compila.

```java
// NÃO COMPILA — IOException é checked, Consumer não declara throws
List<Path> arquivos = /* ... */;
arquivos.forEach(p -> Files.readString(p));  // erro de compilação
```

**Workaround 1 — wrapear em unchecked na hora:**

```java
arquivos.forEach(p -> {
    try {
        processar(Files.readString(p));
    } catch (IOException e) {
        throw new UncheckedIOException(e);  // wrapper padrão do Java para IOException
    }
});
```

**Workaround 2 — helper utilitário genérico:**

```java
@FunctionalInterface
public interface ThrowingFunction<T, R> {
    R apply(T t) throws Exception;
}

public static <T, R> Function<T, R> unchecked(ThrowingFunction<T, R> fn) {
    return t -> {
        try {
            return fn.apply(t);
        } catch (RuntimeException e) {
            throw e;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    };
}

// Uso limpo no stream
List<String> conteudos = arquivos.stream()
    .map(unchecked(Files::readString))
    .toList();
```

**Sneaky throw** (técnica avançada, use com critério): por causa do type erasure, é possível lançar uma checked exception sem declará-la. Bibliotecas como Lombok (`@SneakyThrows`) e algumas instruções de bytecode permitem isso. O efeito é que o caller nunca vê a exceção no contrato do método. Use apenas quando o custo do wrapping é proibitivo e você tem controle total do contexto; em APIs públicas é uma armadilha.

---

### Tratamento em API REST

Em aplicações Spring Boot, o padrão é mapear exceções de domínio para HTTP status codes em um único lugar, mantendo os controllers limpos:

```java
// Controller — lança exceção de domínio, sem se preocupar com HTTP
@GetMapping("/pacientes/{id}")
public PacienteResponse buscar(@PathVariable Long id) {
    return servico.buscar(id);  // lança PacienteNaoEncontradoException se não existir
}

// Handler global — mapeia exceção → HTTP response
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(PacienteNaoEncontradoException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ProblemDetail handleNaoEncontrado(PacienteNaoEncontradoException ex) {
        ProblemDetail detail = ProblemDetail.forStatus(HttpStatus.NOT_FOUND);
        detail.setTitle("Paciente não encontrado");
        detail.setDetail(ex.getMessage());
        return detail;
    }

    @ExceptionHandler(IllegalArgumentException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ProblemDetail handleArgumentoInvalido(IllegalArgumentException ex) {
        ProblemDetail detail = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        detail.setDetail(ex.getMessage());
        return detail;
    }
}
```

O `@RestControllerAdvice` é o gancho central para tratamento de exceções em APIs REST — tema aprofundado em [[03-Dominios/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções com @ControllerAdvice]]. O formato `ProblemDetail` ([[03-Dominios/Java/Web e APIs REST/10 - Problem Details — RFC 9457|RFC 9457]]) é o padrão moderno de resposta de erro em Spring Boot 3+.

## Armadilhas

### (1) Swallowing exception — catch vazio engole o erro

**O problema:** capturar uma exceção e não fazer nada (ou logar sem relançar) faz o erro desaparecer silenciosamente. O programa continua em estado inconsistente sem nenhuma evidência do que aconteceu.

```java
// RUIM — o erro some
try {
    enviarEmail(usuario);
} catch (Exception e) {
    // nada aqui — o email falhou, ninguém sabe
}
```

```java
// FIX — trate ou propague, nunca engula
try {
    enviarEmail(usuario);
} catch (EmailException e) {
    log.error("Falha ao enviar email para usuário id={}", usuario.getId(), e);
    // Decida: relançar? Usar fallback? Marcar para retry?
    notificacaoFallback.registrarFalha(usuario, e);
}
```

A regra é simples: se você captura uma exceção, **faça algo com ela** — logue com contexto suficiente, relance (como ela é ou wrapada), ou execute um tratamento de fallback deliberado. Catch vazio é quase sempre um bug esperando para ser descoberto em produção.

---

### (2) Catch genérico `Exception` ou `Throwable` — captura demais

**O problema:** capturar `Exception` pega tudo — inclusive `RuntimeException`s que indicam bugs de programação (`NullPointerException`, `ClassCastException`), mascarando erros que deveriam ser corrigidos no código. Capturar `Throwable` é ainda pior: inclui `Error` (como `OutOfMemoryError`), que a JVM lança quando está em estado irrecuperável.

```java
// RUIM — captura NullPointerException, ClassCastException, bugs de programação
try {
    resultado = processarPedido(pedido);
} catch (Exception e) {
    log.error("Algo deu errado", e);
    return Optional.empty();
}

// AINDA PIOR — captura OutOfMemoryError, StackOverflowError
try {
    resultado = processarPedido(pedido);
} catch (Throwable t) {
    log.error("Algo deu errado", t);
}
```

```java
// FIX — seja específico; capture apenas o que você sabe tratar
try {
    resultado = processarPedido(pedido);
} catch (PedidoInvalidoException e) {
    log.warn("Pedido inválido id={}: {}", pedido.getId(), e.getMessage());
    return Optional.empty();
} catch (ServicoExternoException e) {
    log.error("Falha no serviço externo ao processar pedido id={}", pedido.getId(), e);
    throw e;  // propaga para retry em camada superior
}
// NPE e bugs: não capturar — devem chegar ao log de erro e ser corrigidos
```

Catch genérico em fronteiras de sistema (entry points de thread, handlers HTTP globais) pode ser aceitável — mas mesmo lá prefira `catch (RuntimeException e)` a `catch (Throwable t)`.

---

### (3) `return` ou `throw` dentro de `finally` — descarta a exceção original

**O problema:** qualquer `return` ou `throw` dentro de um bloco `finally` substitui o valor de retorno ou a exceção que estava sendo propagada. A exceção original é silenciosamente descartada — sem stack trace, sem log, sem rastro.

```java
// RUIM — o finally com return descarta qualquer exceção do try
public String lerDados() {
    try {
        return Files.readString(Path.of("dados.txt"));  // pode lançar IOException
    } finally {
        return "fallback";  // SEMPRE retorna "fallback" — IOException some!
    }
}
```

```java
// RUIM — o throw do finally substitui a exceção original
public void processar() {
    try {
        executarLogica();  // lança IllegalStateException
    } finally {
        fecharConexao();   // lança IOException — substitui IllegalStateException!
    }
}
```

```java
// FIX — finally deve conter apenas limpeza que não lança, ou tratar a exceção internamente
public void processar() {
    try {
        executarLogica();
    } finally {
        try {
            fecharConexao();
        } catch (IOException ex) {
            log.warn("Falha ao fechar conexão", ex);  // loga sem propagar
        }
    }
}

// MELHOR — use try-with-resources; o problema de exceções suprimidas é tratado automaticamente
try (var conexao = abrirConexao()) {
    executarLogica(conexao);
}  // close() chamado automaticamente; exceção suprimida acessível via getSuppressed()
```

**Regra prática:** `finally` deve conter apenas código de limpeza — fechar recursos, liberar locks, atualizar contadores. Nunca `return`, nunca `throw` que pode vazar. Quando precisar lidar com exceções de limpeza, capture-as dentro do próprio `finally` e logue sem relançar.

## Em entrevista

### Frase pronta (inglês)

> "The checked versus unchecked debate comes down to whether the caller can realistically recover from the failure: if you're writing a low-level I/O utility where the caller genuinely needs to decide how to handle a missing file, a checked exception makes the contract explicit and forces the decision." "In practice, most modern frameworks — Spring, JPA, Reactor — default to unchecked exceptions because checked exceptions pollute method signatures, leak implementation details through abstraction layers, and simply don't compose with lambdas and streams." "The important caveat with unchecked is discipline: you lose the compiler safety net, so you need good documentation, consistent naming conventions for your domain exceptions, and a centralized handler — like a `@RestControllerAdvice` in Spring — to translate domain exceptions into proper HTTP responses without letting raw stack traces reach the client."

> "Try-with-resources is the canonical way to handle any `AutoCloseable` resource in Java 7 and later: resources are closed in reverse declaration order, and if both the try block and the close method throw, the close exception is suppressed rather than replacing the original — you can retrieve it via `getSuppressed()`. The old finally pattern had the opposite and more dangerous behavior: a throw in finally would silently discard the original exception."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| exceção verificada | checked exception |
| exceção não verificada | unchecked exception |
| pilha de chamadas | call stack / stack trace |
| capturar e relançar | catch and rethrow |
| exceção suprimida | suppressed exception |
| encadeamento de exceções | exception chaining |
| recurso autocloseable | AutoCloseable resource |
| engolir exceção | swallow an exception |
| propagação de exceção | exception propagation |
| bloco de limpeza | finally block / cleanup block |

## Veja também

- [[08 - Interfaces e classes abstratas]]
- [[06 - Classes, objetos e encapsulamento]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [Exceptions — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/exceptions/)
- [The try-with-resources Statement — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html)
- [AutoCloseable — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/AutoCloseable.html)
- [Throwable.getSuppressed — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Throwable.html#getSuppressed())
