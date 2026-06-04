---
title: "I/O moderno com java.nio.file"
created: 2026-06-04
updated: 2026-06-04
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - collections
  - adepto
  - io
  - nio
aliases:
  - "java.nio.file"
  - "Files"
  - "Path"
  - "I/O moderno"
---

# I/O moderno com java.nio.file

> [!abstract] TL;DR
> `java.nio.file` (NIO.2, Java 7) é a API moderna de I/O de arquivos em Java. Seu núcleo são duas classes: `Path` (representa um caminho no sistema de arquivos) e `Files` (executa as operações). Para arquivos pequenos, `readString` e `writeString` são diretos e sem cerimônia. Para arquivos grandes, `Files.lines` retorna um `Stream<String>` lazy que **precisa ser fechado** — use sempre `try-with-resources`. O mesmo vale para `Files.walk` e `Files.list`. A API legada `java.io.File` ainda existe, mas deve ser evitada em código novo.

## O que é

`java.nio.file` é a API de I/O de arquivos introduzida no Java 7 como parte do pacote NIO.2 (*New I/O 2*). Antes dela, a única opção era `java.io.File`, uma classe datada com interface inconsistente, sem suporte a exceções verificáveis e com semântica de retorno booleano que tornava o diagnóstico de erros difícil.

NIO.2 resolveu esses problemas com dois tipos centrais:

- **`Path`** — representa um caminho no sistema de arquivos (arquivo ou diretório), seja ele absoluto ou relativo. É apenas uma referência sintática: não exige que o arquivo exista.
- **`Files`** — classe utilitária com métodos estáticos que realizam operações reais no sistema de arquivos (leitura, escrita, cópia, traversal de diretórios).

```java
Path p = Path.of("dados", "entrada.csv");  // portable, sem hard-code de separador
```

A API legada `java.io.File` pode ser convertida para `Path` via `file.toPath()`, permitindo migração gradual sem reescrita total.

## Por que importa

Em entrevistas e no código de produção, três razões justificam o domínio desta API:

1. **Ubiquidade:** leitura e escrita de arquivos aparecem em testes de integração, processamento de logs, importação de dados CSV, geração de relatórios e pipelines de build. Não conhecer a API moderna é um sinal imediato de senioridade comprometida.

2. **Armadilha de vazar recursos:** `Files.lines`, `Files.walk` e `Files.list` retornam `Stream` que mantém um *file handle* aberto. Não fechá-lo é um bug silencioso que explode em produção sob carga. A distinção entre "stream que fecha sozinho" e "stream que precisa de try-with-resources" é justamente o que os entrevistadores testam.

3. **Memória:** ler um arquivo de 2 GB com `readAllLines` resulta em `OutOfMemoryError`. A alternativa correta — `Files.lines` com streaming — exige entender o contrato de fechamento. Esse é o tipo de trade-off que separa quem usa a API de quem a *entende*.

## Como funciona

### `Path` e `Files` (a dupla central)

`Path` é imutável e representa apenas a sintaxe do caminho. Não acessa o disco até que uma operação seja feita via `Files`.

```java
// Construção portável — nunca concatenar strings com "/"
Path base   = Path.of("/var/app/data");
Path config = base.resolve("config.json");  // /var/app/data/config.json
Path parent = config.getParent();           // /var/app/data
String name = config.getFileName().toString(); // "config.json"

// Conversão do legado
File legacyFile = new File("antigo.txt");
Path modernPath = legacyFile.toPath();
```

`Path.of("a", "b", "c")` constrói `a/b/c` (ou `a\b\c` no Windows) sem hard-code de separador — ponto importante que os entrevistadores valorizam.

### Ler (`readString` / `readAllLines` / `lines`) e escrever (`writeString` / `write`)

**Leitura completa em memória** — adequado para arquivos pequenos:

```java
// Lê o arquivo inteiro como String (UTF-8 por padrão)
String conteudo = Files.readString(Path.of("config.json"));

// Lê como List<String>, uma entrada por linha
List<String> linhas = Files.readAllLines(Path.of("config.json"));
```

**Leitura via streaming** — obrigatório para arquivos grandes:

```java
// Files.lines retorna Stream<String> lazy — DEVE ser fechado
try (Stream<String> stream = Files.lines(Path.of("eventos.log"))) {
    long erros = stream
        .filter(linha -> linha.contains("ERROR"))
        .count();
    System.out.println("Erros encontrados: " + erros);
}  // stream.close() chamado aqui — file handle liberado
```

**Escrita:**

```java
// Escreve String inteira (cria ou sobrescreve)
Files.writeString(Path.of("saida.txt"), "linha 1\nlinha 2\n");

// Escreve com opções (append)
Files.writeString(Path.of("log.txt"), "nova entrada\n", StandardOpenOption.APPEND);

// Escreve coleção de linhas
List<String> linhas = List.of("alfa", "beta", "gama");
Files.write(Path.of("lista.txt"), linhas);
```

**Tabela-resumo dos métodos de leitura:**

| Método            | Retorna         | Lazy? | AutoCloseable? | Risco    |
|-------------------|-----------------|-------|----------------|----------|
| `readString()`    | `String`        | não   | não            | nenhum   |
| `readAllLines()`  | `List<String>`  | não   | não            | OOM      |
| `lines()`         | `Stream<String>`| sim   | **sim**        | vaza FD  |

### Operações de diretório (`exists` / `createDirectories` / `list` / `walk`)

```java
Path dir = Path.of("relatorios", "2026", "junho");

// Verifica existência (não lança exceção se o caminho não existir)
if (!Files.exists(dir)) {
    // Cria dir e todos os pais necessários; idempotente se já existir
    Files.createDirectories(dir);
}

// Lista o conteúdo de um diretório (1 nível) — stream lazy, fechar obrigatório
try (Stream<Path> entradas = Files.list(dir)) {
    entradas
        .filter(Files::isRegularFile)
        .map(Path::getFileName)
        .forEach(System.out::println);
}

// Traversal recursivo da árvore — stream lazy, fechar obrigatório
try (Stream<Path> arvore = Files.walk(Path.of("src"))) {
    arvore
        .filter(p -> p.toString().endsWith(".java"))
        .forEach(System.out::println);
}
```

`Files.walk` com profundidade máxima:

```java
try (Stream<Path> raso = Files.walk(Path.of("src"), 2)) {
    // visita no máximo 2 níveis abaixo de "src"
}
```

### `try-with-resources` e `AutoCloseable` (linkar Galho 1, nota 10)

`Files.lines`, `Files.list` e `Files.walk` retornam streams que implementam `AutoCloseable`. Isso significa que devem ser usados dentro de um bloco `try-with-resources` — a mesma construção que garante o fechamento de `BufferedReader`, `Connection` e outros recursos.

Para o funcionamento detalhado do `try-with-resources` (exceções suprimidas, ordem de fechamento, multi-recurso), veja [[03-Dominios/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros|Exceções e tratamento de erros]].

A regra prática: **se `Files` devolve um `Stream`, ele precisa de `try-with-resources`**.

### Streaming de arquivos grandes (`Files.lines` retorna `Stream<String>` — fechar!)

O modelo mental correto é: `Files.lines` não lê o arquivo inteiro de uma vez. Ele abre um *file handle* e entrega as linhas sob demanda conforme o `Stream` é consumido. O handle permanece aberto até que:

- o `Stream` seja fechado explicitamente (`stream.close()`), ou
- o bloco `try-with-resources` termine.

Se o `Stream` for atribuído a um campo, passado para outro método ou simplesmente "esquecido" fora de um `try`, o handle vaza. Em aplicações de longa duração, o sistema operacional eventualmente recusa novas aberturas de arquivo com `Too many open files`.

```java
// ERRADO — sem try-with-resources, file handle vaza
Stream<String> stream = Files.lines(Path.of("grande.csv")); // risco real
stream.filter(l -> l.startsWith("WARN")).forEach(System.out::println);
// stream nunca fechado se uma exceção ocorrer antes do fim

// CORRETO
try (Stream<String> stream = Files.lines(Path.of("grande.csv"))) {
    stream.filter(l -> l.startsWith("WARN")).forEach(System.out::println);
}
```

O mesmo raciocínio se aplica a `Files.walk` e `Files.list`.

## Na prática

### Ler arquivo inteiro com `readString`

Cenário: carregar um JSON de configuração pequeno em memória para parsear.

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.io.IOException;

public class ConfigLoader {

    public static String carregarConfig(String caminho) throws IOException {
        Path path = Path.of(caminho);

        if (!Files.exists(path)) {
            throw new IllegalArgumentException("Arquivo não encontrado: " + caminho);
        }

        return Files.readString(path);  // UTF-8 por padrão; sem try-with-resources necessário
    }
}
```

`readString` não precisa de `try-with-resources` porque não retorna um recurso aberto — ele abre, lê, fecha e devolve a `String` pronta.

### Processar CSV grande linha-a-linha com `Files.lines`

Cenário: um arquivo de log com milhões de linhas; contar e coletar apenas as linhas de erro sem carregar tudo em memória.

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class LogAnalyser {

    public static List<String> coletarErros(Path arquivo) throws IOException {
        // try-with-resources garante fechamento mesmo se uma exceção ocorrer
        try (Stream<String> linhas = Files.lines(arquivo)) {
            return linhas
                .filter(l -> l.contains("ERROR") || l.contains("FATAL"))
                .collect(Collectors.toList());
        }
    }

    public static void main(String[] args) throws IOException {
        Path log = Path.of("var", "log", "app", "production.log");

        List<String> erros = coletarErros(log);
        System.out.printf("Total de erros: %d%n", erros.size());
        erros.stream().limit(10).forEach(System.out::println);
    }
}
```

Pontos de design a destacar em entrevista:

- `try-with-resources` envolve o stream, não o bloco inteiro — recursos fecham no momento certo.
- `Collectors.toList()` materializa o resultado; a partir daí o stream pode fechar sem problema.
- `Path.of("var", "log", "app", "production.log")` — portable, sem separador hard-coded.

## Armadilhas

### 1. Não fechar o `Stream` de `Files.lines` / `Files.walk` (vaza file handle)

`Files.lines`, `Files.walk` e `Files.list` retornam streams que mantêm um file descriptor aberto. Omitir o `try-with-resources` vaza o handle — especialmente grave se houver exceção no meio do processamento.

```java
// ERRADO
Files.walk(Path.of("src"))
    .filter(p -> p.toString().endsWith(".java"))
    .forEach(System.out::println);
// stream nunca fechado — file descriptor vaza

// CORRETO
try (Stream<Path> arquivos = Files.walk(Path.of("src"))) {
    arquivos
        .filter(p -> p.toString().endsWith(".java"))
        .forEach(System.out::println);
}
```

**Regra:** toda vez que `Files` devolver um `Stream`, envolva em `try-with-resources`.

### 2. Usar `readAllLines` / `readString` em arquivo gigante (OOM)

`readAllLines` carrega todas as linhas em uma `List<String>` e `readString` carrega o arquivo inteiro como uma `String` — ambos em memória de uma só vez. Para arquivos de muitos megabytes (ou gigabytes), o resultado é `OutOfMemoryError`.

```java
// ERRADO para arquivo de 2 GB
List<String> todas = Files.readAllLines(Path.of("dump.sql")); // OOM

// CORRETO — streaming, uma linha por vez
try (Stream<String> linhas = Files.lines(Path.of("dump.sql"))) {
    linhas.filter(l -> l.startsWith("INSERT")).forEach(this::processar);
}
```

**Regra:** `readString` e `readAllLines` são para arquivos que cabem confortavelmente na heap. Para qualquer coisa maior que alguns MB, use `Files.lines`.

### 3. Path com separador hard-coded (`"a/b"`) em vez de `Path.of("a", "b")`

Concatenar separadores de caminho na string torna o código não-portável entre sistemas operacionais.

```java
// FRÁGIL — quebra no Windows (usa '\')
Path p = Path.of("dados/entrada/arquivo.csv");

// CORRETO — Path.of resolve o separador da plataforma
Path p = Path.of("dados", "entrada", "arquivo.csv");

// Ou usando resolve (para componentes dinâmicos)
Path base   = Path.of("dados");
Path target = base.resolve("entrada").resolve("arquivo.csv");
```

Embora na prática a maioria das JVMs modernas aceite `/` no Windows, a convenção `Path.of(componentes…)` comunica intenção clara e é a forma que os entrevistadores esperam ver.

## Em entrevista

### Frase pronta (inglês)

"NIO.2, introduced in Java 7, replaced the legacy `java.io.File` with a cleaner `Path` and `Files` API. For small files, `Files.readString` and `Files.writeString` handle everything in one call. For large files, `Files.lines` returns a lazy `Stream<String>` that reads line by line without loading the whole file into memory. The critical contract is that this stream holds an open file descriptor, so it must always be closed — which is exactly why you wrap it in a try-with-resources block. The same rule applies to `Files.walk` and `Files.list`. Forgetting to close those streams is one of the classic resource-leak bugs in Java applications."

### Vocabulário (inglês técnico)

| Termo | Definição |
|---|---|
| **NIO.2** | *New I/O 2*, the file system API introduced in Java 7 via `java.nio.file` |
| **`Path`** | Immutable object representing a file system path; syntactic, no disk access |
| **`Files`** | Utility class with static methods for actual file system operations |
| **lazy stream** | A `Stream` that reads data on demand, rather than loading everything upfront |
| **file descriptor / file handle** | OS-level resource kept open by lazy streams; must be closed to avoid leaks |
| **try-with-resources** | Java construct that automatically closes `AutoCloseable` resources on block exit |
| **`AutoCloseable`** | Interface that marks a resource as closeable; enables try-with-resources |
| **`readAllLines` vs `lines`** | Eager (all in memory) vs lazy (stream, closeable) — key trade-off question |

## Veja também

- [[05 - Introdução à Stream API]]
- [[07 - Operações de Stream — intermediárias e terminais]]
- [[03-Dominios/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros|Exceções]]
- [[03-Dominios/Java/Dicionário de Java#java.nio.file (Path / Files)|java.nio.file]]
- [[03-Dominios/Java/Dicionário de Java#try-with-resources|try-with-resources]]

## Referências

- Oracle. *Java NIO.2 File I/O Tutorial*. Disponível em: https://docs.oracle.com/javase/tutorial/essential/io/fileio.html
- Oracle. *java.nio.file.Files (Java SE 21 API)*. Disponível em: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/file/Files.html
- Oracle. *java.nio.file.Path (Java SE 21 API)*. Disponível em: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/file/Path.html
