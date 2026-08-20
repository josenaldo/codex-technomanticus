---
title: "Strings e text blocks"
created: 2026-06-02
updated: 2026-06-02
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - linguagem
  - iniciado
  - strings
  - text-blocks
aliases:
  - String
  - text blocks
---

# Strings e text blocks

> [!abstract] TL;DR
> `String` em Java é um **objeto imutável** — toda operação retorna uma nova instância. O **String pool** interna literais automaticamente, permitindo reúso de memória, mas `==` entre Strings continua perigoso. Para concatenação em loops, use **`StringBuilder`** (mutável). **`String.format`** e o método **`.formatted()`** oferecem interpolação por posição. **Text blocks** (`"""`, Java 15+) permitem Strings multi-linha com indentação controlada automaticamente — sem interpolação nativa. Os métodos modernos `strip`, `repeat`, `lines` e `isBlank` (Java 11+) cobrem necessidades cotidianas com suporte a Unicode pleno.

## O que é

`String` é uma classe do pacote `java.lang` que representa uma **sequência imutável de caracteres Unicode**. Diferente dos tipos primitivos, é um objeto no heap — mas recebe tratamento especial da JVM.

A imutabilidade significa que **nenhum método altera o objeto original**: `toUpperCase()`, `replace()`, `trim()` — todos retornam uma nova instância. O objeto original pode ser compartilhado com segurança entre threads sem sincronização.

Essa característica viabiliza o **String pool** (interning), permite usar Strings como chaves seguras em `HashMap`, e garante que constantes de `switch` sejam invariantes em compile-time.

## Como funciona

### Imutabilidade e String pool

Quando o compilador encontra um **literal** (`"hello"`), a JVM verifica o **String pool** (área especial no heap, gerenciada pela JVM) — se o mesmo valor já existe, retorna a referência existente; caso contrário, cria e adiciona ao pool.

```java
String a = "hello";
String b = "hello";
System.out.println(a == b);       // true — mesma referência do pool

String c = new String("hello");
System.out.println(a == c);       // false — c foi criada fora do pool
System.out.println(a.equals(c));  // true  — mesmo conteúdo

String d = c.intern();            // força inserção/busca no pool
System.out.println(a == d);       // true  — d agora aponta para o objeto do pool
```

O método `intern()` força a pesquisa no pool: se o valor já existir, retorna a referência do pool; se não, insere e retorna. Na prática, `intern()` raramente é necessário em código de aplicação — é mais relevante em ferramentas, parsers ou código que processa grandes volumes de Strings repetidas.

**Imutabilidade e concorrência:** nenhum método muda o estado interno, então múltiplas threads lêem o mesmo objeto sem race condition — sem `synchronized`, `volatile` ou cópias defensivas.

---

### Concatenação: `+` vs `StringBuilder`

O operador `+` é **açúcar sintático**: fora de loops, o compilador (Java 9+) usa `StringConcatFactory` via `invokedynamic` e otimiza bem. O problema aparece em **loops**: a cada iteração, uma nova instância intermediária pode ser criada, acumulando pressão no GC.

```java
// Problemático em loop: cria String nova a cada iteração
String resultado = "";
for (String item : lista) {
    resultado += item + ", ";   // N novas Strings alocadas
}

// Correto: StringBuilder é mutável, um objeto para todo o loop
StringBuilder sb = new StringBuilder();
for (String item : lista) {
    sb.append(item).append(", ");
}
String resultado = sb.toString();  // uma única String no final
```

`StringBuilder` é **não thread-safe**. Para acumulação concorrente, use `StringBuffer` ou `Collectors.joining()`.

---

### Formatação (`String.format`, `formatted`, `String.join`)

**`String.format`** — método estático, sintaxe `printf`-style:

```java
String msg = String.format("Paciente %s, idade %d, peso %.1f kg", nome, idade, peso);
// → "Paciente Ana, idade 35, peso 68.5 kg"
```

**`.formatted()`** — método de instância disponível desde **Java 15**, funciona como `String.format` mas chamado diretamente na String de template (mais legível com text blocks):

```java
String relatorio = """
        Paciente: %s
        Idade:    %d
        CID:      %s
        """.formatted(nome, idade, cid);
```

**`String.join`** — concatena com separador, mais legível que `format` para listas:

```java
String csv = String.join(", ", "Ana", "Bruno", "Carlos");
// → "Ana, Bruno, Carlos"

List<String> nomes = List.of("Ana", "Bruno", "Carlos");
String linha = String.join(" | ", nomes);
// → "Ana | Bruno | Carlos"
```

Para coleções, `Collectors.joining(separador, prefixo, sufixo)` é a alternativa funcional.

---

### Text blocks (Java 15+)

Text blocks permitem Strings **multi-linha** sem escapes de quebra de linha. São delimitados por `"""` — o delimitador de abertura deve ser seguido obrigatoriamente de uma quebra de linha (não pode haver conteúdo na mesma linha).

```java
String json = """
        {
            "nome": "Ana",
            "idade": 35
        }
        """;
```

**Indentação incidental vs. essencial:** o compilador determina a margem esquerda comum a todas as linhas (incluindo a linha do delimitador de fechamento) e a remove. Isso é chamado de *incidental whitespace* — espaços que existem apenas por causa da indentação do código-fonte. O que sobra é a *essential whitespace*, a indentação relativa real do conteúdo.

```java
void exemplo() {
    String html = """
            <html>
                <body>
                    <p>Olá</p>
                </body>
            </html>
            """;
    // Margem: 12 espaços (todos os delimitadores concordam).
    // Resultado: "<html>\n    <body>\n        <p>Olá</p>\n    </body>\n</html>\n"
}
```

A posição do delimitador de fechamento `"""` controla a margem:
- Na mesma indentação do conteúdo → remove os espaços comuns normalmente.
- Na coluna 0 (sem recuo) → preserva toda a indentação do conteúdo.
- Na última linha de conteúdo → exclui o `\n` final.

**Sequências de escape especiais em text blocks:**

| Sequência | Efeito |
|-----------|--------|
| `\` + fim de linha | Suprime a quebra de linha (linha de continuação) |
| `\s` | Espaço explícito — impede que espaços à direita sejam removidos |

```java
// \ no final da linha: suprime o \n (útil para linhas longas legíveis)
String paragrafo = """
        Lorem ipsum dolor sit amet, consectetur adipiscing \
        elit, sed do eiusmod tempor incididunt.\
        """;
// Resultado: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt."

// \s como "cerca de espaço": preserva espaços à direita
String colunas = """
        red  \s
        green\s
        blue \s
        """;
// Resultado: cada linha tem exatamente 6 caracteres (espaços preservados)
```

**Normalização de quebras de linha:** `\r`, `\r\n` e `\n` são normalizados para `\n` pelo compilador, garantindo consistência cross-platform.

**Ausência de interpolação:** text blocks são **literais puros** — sem `${}` ou `\{}`. Para inserir valores, use `.formatted()` após o bloco:

```java
String query = """
        SELECT *
        FROM usuarios
        WHERE id = %d
        """.formatted(userId);
```

> String Templates (prévia em Java 21/22 com `STR."..."`) foram removidos das prévias e **não estão disponíveis como feature GA** em nenhuma versão LTS atual. Não utilize em código de produção.

---

### Métodos modernos (`strip`, `repeat`, `lines`, `isBlank`)

Introduzidos no **Java 11**, esses métodos têm suporte correto a **Unicode** (diferente dos métodos mais antigos):

| Método | Desde | Descrição |
|--------|-------|-----------|
| `strip()` / `stripLeading()` / `stripTrailing()` | Java 11 | Remove espaços Unicode no início/fim (substitui `trim()`) |
| `isBlank()` | Java 11 | `true` se vazio ou contém apenas espaços Unicode |
| `lines()` | Java 11 | `Stream<String>` das linhas (`\n`, `\r\n`, `\r`) |
| `repeat(n)` | Java 11 | Repete a String `n` vezes |
| `stripIndent()` | Java 15 | Aplica o algoritmo de text block a qualquer String em runtime |
| `translateEscapes()` | Java 15 | Processa sequências de escape (`\n`, `\t`, etc.) em uma String |

```java
"  Olá mundo  ".strip();          // "Olá mundo"
"  ".isBlank();                   // true
"".isBlank();                     // true
"ab".repeat(3);                   // "ababab"

"linha1\nlinha2\nlinha3"
    .lines()
    .filter(l -> !l.isBlank())
    .toList();                    // ["linha1", "linha2", "linha3"]
```

**`trim()` vs `strip()`:** `trim()` remove apenas caracteres ≤ U+0020 (ASCII). `strip()` usa `Character.isWhitespace()` — reconhece todos os espaços Unicode (non-breaking space, ideographic space, etc.). Prefira `strip()` em código novo.

## Na prática

**Cenário:** construir uma query SQL e um payload JSON. Compare o texto com text block vs. concatenação tradicional.

```java
// Concatenação tradicional — difícil de ler, propenso a erros de aspas
String sqlAntigo = "SELECT u.id, u.nome, u.email\n" +
                   "FROM usuarios u\n" +
                   "JOIN pedidos p ON p.usuario_id = u.id\n" +
                   "WHERE u.ativo = true\n" +
                   "  AND p.status = 'PENDENTE'\n" +
                   "ORDER BY p.criado_em DESC\n" +
                   "LIMIT " + limite;

// Com text block — estrutura visual fiel ao SQL real
String sql = """
        SELECT u.id, u.nome, u.email
        FROM usuarios u
        JOIN pedidos p ON p.usuario_id = u.id
        WHERE u.ativo = true
          AND p.status = 'PENDENTE'
        ORDER BY p.criado_em DESC
        LIMIT %d
        """.formatted(limite);
```

```java
// JSON via concatenação — aspas duplas precisam de escape em todo lugar
String jsonAntigo = "{\n" +
                    "  \"evento\": \"" + tipo + "\",\n" +
                    "  \"usuarioId\": " + userId + ",\n" +
                    "  \"timestamp\": \"" + agora + "\"\n" +
                    "}";

// JSON com text block — aspas simples e duplas livres (exceto três seguidas)
String jsonEvento = """
        {
            "evento": "%s",
            "usuarioId": %d,
            "timestamp": "%s"
        }
        """.formatted(tipo, userId, agora);
```

O text block elimina `\n` explícitos e escapes de aspas duplas, deixando o conteúdo visualmente idêntico ao resultado em runtime.

## Armadilhas

### (1) `+` em loop quente — alocação desnecessária

**O problema:** usar `+=` para acumular uma String em um loop cria uma nova instância a cada iteração. Em loops com muitos elementos, isso gera pressão significativa no GC.

```java
// Problemático: N alocações intermediárias
String lista = "";
for (String nome : nomes) {
    lista += nome + "\n";   // cria nova String a cada iteração
}
```

**Fix:** use `StringBuilder` para acumulação, convertendo para `String` apenas ao final. Para casos com Streams, `Collectors.joining()` é idiomático e equivalente.

```java
StringBuilder sb = new StringBuilder();
for (String nome : nomes) {
    sb.append(nome).append('\n');
}
String lista = sb.toString();

// Com Stream:
String lista = nomes.stream().collect(Collectors.joining("\n", "", "\n"));
```

---

### (2) Comparar Strings com `==` em vez de `.equals()`

**O problema:** `==` compara **referências** (se as duas variáveis apontam para o mesmo objeto), não o **conteúdo**. Por conta do String pool, literais iguais podem ser o mesmo objeto e `==` retorna `true` — o que cria uma falsa sensação de segurança. Com Strings vindas de APIs, banco de dados, parâmetros ou `new String(...)`, o comportamento falha silenciosamente.

```java
String a = "status";
String b = "status";
System.out.println(a == b);       // true — literais internados no pool (coincidência!)

String c = new String("status");
System.out.println(a == c);       // false — c é objeto diferente (mesmo valor)
System.out.println(a.equals(c));  // true  — correto: compara conteúdo

// Cenário real: parâmetro de request ou resultado de query
String statusDb = resultSet.getString("status");
if (statusDb == "ativo") {        // ERRADO: quase sempre false fora do pool
    ...
}
if ("ativo".equals(statusDb)) {   // CORRETO: compara conteúdo; null-safe (não lança NPE)
    ...
}
```

**Fix:** sempre use `.equals()` para comparar conteúdo. Coloque a constante à esquerda — `"ativo".equals(statusDb)` — para evitar `NullPointerException`. Use `Objects.equals(a, b)` quando ambas podem ser `null`.

---

### (3) Indentação incidental inesperada em text block

**O problema:** o algoritmo de remoção de indentação incidental leva em conta **todos os caracteres de espaço** — inclusive a posição do delimitador de fechamento `"""`. Se o fechamento estiver mais à esquerda do que o conteúdo, a indentação do conteúdo é preservada (pode ser inesperado). Se o fechamento estiver na coluna 0, **nenhuma indentação é removida**.

```java
// Problema: fechamento mais à esquerda que o conteúdo
String problema = """
            {
                "chave": "valor"
            }
    """;  // fechamento com 4 espaços → remove apenas 4 espaços de cada linha
          // resultado: "        {\n            \"chave\": \"valor\"\n        }\n"
          // (8 espaços à frente de "{" — provavelmente não era o esperado)

// Correto: fechar no mesmo nível do conteúdo
String correto = """
        {
            "chave": "valor"
        }
        """;  // 8 espaços → remove 8 → resultado sem indentação extra
```

**Fix:** mantenha o delimitador de fechamento na mesma indentação do conteúdo. Use `-Xlint:text-blocks` para detectar inconsistências de tabs vs. espaços.

## Em entrevista

### Frase pronta (inglês)

> "String immutability in Java is a deliberate design choice with several cascading benefits: it enables the JVM to maintain the String pool, where identical literals share a single object, reducing memory overhead; it makes Strings inherently thread-safe without synchronization, since no thread can mutate a String another thread is reading; and it allows Strings to be safely used as HashMap keys, since their hash code is stable. The trade-off is that any modification — concatenation, replacement, case conversion — produces a new object, so naive string building in a loop with `+=` allocates one object per iteration, which adds GC pressure at scale; the fix is to use `StringBuilder` for mutable accumulation and call `toString()` once at the end. For the `==` vs `.equals()` pitfall: the String pool can make `==` appear to work for literals, but strings coming from APIs, databases, or `new String(...)` live outside the pool, so `==` will return false even for equal content — always use `.equals()` or `Objects.equals()` for value comparison."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| imutabilidade | immutability |
| pool de strings / interning | String pool / string interning |
| internação forçada | explicit interning (`intern()`) |
| construtor de strings mutável | mutable string builder (`StringBuilder`) |
| bloco de texto / texto multi-linha | text block |
| espaço em branco incidental | incidental whitespace |
| espaço em branco essencial | essential whitespace |
| supressão de quebra de linha | line continuation (`\` at end of line) |
| formatação por posição | positional formatting (`String.format`, `.formatted()`) |
| identidade de referência vs. igualdade de valor | reference identity (`==`) vs. value equality (`.equals()`) |

## Veja também

- [[02 - Tipos, variáveis e operadores]]
- [[03 - Estruturas de controle e fluxo]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [JEP 378: Text Blocks — openjdk.org](https://openjdk.org/jeps/378)
- [Java Text Blocks — Developer's Guide (Oracle, Java 21)](https://docs.oracle.com/en/java/javase/21/text-blocks/index.html)
- [String (java.lang) — Java SE 21 API Docs](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/String.html)
- [StringBuilder (java.lang) — Java SE 21 API Docs](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/StringBuilder.html)
- [Strings — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/data/strings.html)
- [Formatting Numeric Print Output — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/data/numberformat.html)
