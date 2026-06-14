---
title: "Domínio 9 — I/O"
created: 2026-06-13
updated: 2026-06-13
type: concept
status: seedling
publish: true
fase: dominios
tags:
  - java
  - certificacao-ocp
  - dominios
aliases:
  - "Domínio 9 OCP"
  - "I/O na OCP"
---

# Domínio 9 — I/O

> [!abstract] TL;DR
> Cobertura **parcial**. A trilha cobre bem o **NIO.2** (`java.nio.file` — Path, Files, Files.lines, Files.walk) no Galho 2. Mas a prova também cobra o **java.io clássico** (streams de bytes e de chars) e a **serialização**, que ficam **de fora** da trilha. Esta nota mapeia o que dá pra revisar nas notas existentes e marca, com honestidade, o que exige estudo à parte.

> [!info] Títulos oficiais
> - **1Z0-830 (Java 21):** *Using Java I/O API*
> - **1Z0-831 (Java 25):** *Performing Input and Output Operations Using the Java I/O API*

## O que a Oracle cobra

- **java.io** — hierarquia de fluxos: `InputStream`/`OutputStream` para **bytes**; `Reader`/`Writer` para **caracteres**.
- **BufferedReader / BufferedWriter** — envolver (*wrap*) outros fluxos para ganhar performance via buffer.
- **FileInputStream / FileOutputStream / FileReader / FileWriter** — acesso a arquivos em nível de byte ou de char.
- **try-with-resources** — fechamento automático de recursos (`AutoCloseable`).
- **java.nio.file** — `Path`, `Paths`, `Files`, `Files.lines`, `Files.walk`.
- **Serialização** — `Serializable`, `transient`, `serialVersionUID`, `ObjectInputStream` / `ObjectOutputStream`.
- **Console I/O** — a classe `Console`.

## Mapa de revisão

- [[03-Dominios/Java/Collections e Streams/12 - I-O moderno com java.nio.file|I/O moderno com java.nio.file (G2)]] — Path/Files/Files.lines/walk.

## Pegadinhas deste domínio

1. **Byte stream vs char stream** — `InputStream`/`OutputStream` movem **bytes**; `Reader`/`Writer` movem **caracteres** (com codificação). Saber qual usar é a pegadinha base:
   ```java
   // texto → char stream
   try (var r = new BufferedReader(new FileReader("arq.txt"))) { ... }
   // binário → byte stream
   try (var in = new FileInputStream("foto.png")) { ... }
   ```
2. **`transient` exclui o campo da serialização** — no *deserialize* ele volta com o valor **default** do tipo (0, `false`, `null`):
   ```java
   transient String senha; // após readObject: senha == null
   ```
3. **`serialVersionUID` incompatível → `InvalidClassException`** — se o UID gravado não bate com o da classe atual, a desserialização explode.
4. **try-with-resources fecha na ordem reversa** — recursos declarados são fechados do último para o primeiro:
   ```java
   try (var a = abre(); var b = abre()) { ... } // fecha b, depois a
   ```

Linke o [[03-Dominios/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|catálogo de pegadinhas]] para a coleção completa.

## Lacuna da trilha

> [!warning] Seam de honestidade
> A trilha cobre `java.nio.file` (Galho 2), mas **não cobre** três coisas que a prova cobra: java.io clássico, serialização e Console. O conteúdo mínimo autocontido de cada uma está abaixo — para a prova, estude à parte.

### 1. java.io clássico

Duas hierarquias paralelas, escolhidas pela natureza do dado:

- **Bytes:** `InputStream` / `OutputStream` (e filhos como `FileInputStream`, `FileOutputStream`). Use para dados binários (imagens, áudio, bytes brutos).
- **Caracteres:** `Reader` / `Writer` (e filhos como `FileReader`, `FileWriter`). Use para **texto** — eles aplicam a codificação de caracteres.

**Por que envolver com Buffer?** `FileReader`/`FileWriter` sem buffer fazem uma chamada de I/O por caractere — caro. `BufferedReader`/`BufferedWriter` acumulam em um buffer de memória e tocam o disco em blocos. É o padrão *decorator*: você **envolve** um fluxo dentro do outro.

```java
// leitura linha a linha — o readLine() só existe no BufferedReader
try (var r = new BufferedReader(new FileReader("dados.txt"))) {
    String linha;
    while ((linha = r.readLine()) != null) {  // null = fim do arquivo
        System.out.println(linha);
    }
}
```

`readLine()` retorna a linha **sem** o terminador de linha, e `null` quando o fluxo acaba — essa é a condição de parada clássica do laço.

### 2. Serialização

Transformar um objeto em bytes (gravar/transmitir) e reconstruí-lo depois.

- **`Serializable`** — é uma **marker interface** (sem métodos). Implementá-la apenas *sinaliza* que a classe pode ser serializada.
- **`transient`** — marca um campo a ser **pulado** na serialização (ver pegadinha 2).
- **`serialVersionUID`** — um `long` que **controla a compatibilidade de versão** da classe entre a gravação e a leitura. Se não declarar, o compilador gera um implícito frágil; declarar explicitamente é boa prática.
- **API:** `ObjectOutputStream.writeObject(obj)` grava; `ObjectInputStream.readObject()` reconstrói (retorna `Object`, exige cast).

```java
try (var out = new ObjectOutputStream(new FileOutputStream("o.ser"))) {
    out.writeObject(pessoa);
}
try (var in = new ObjectInputStream(new FileInputStream("o.ser"))) {
    Pessoa p = (Pessoa) in.readObject();
}
```

> [!note] Cai pouco
> Serialização costuma render apenas **1–2 questões**. Não invista tempo demais aqui — saiba os marcadores (`transient`, `serialVersionUID`) e a dupla `writeObject`/`readObject`.

### 3. Console

`System.console()` dá acesso ao terminal interativo:

- Pode **retornar `null`** quando não há um terminal real (ex.: rodando dentro de uma IDE ou com I/O redirecionado). **Sempre cheque por null** antes de usar.
- `readLine()` lê uma linha digitada; `readPassword()` lê **sem ecoar** os caracteres na tela (retorna `char[]`, não `String`).

```java
Console c = System.console();
if (c != null) {
    String user = c.readLine("Usuário: ");
    char[] pwd  = c.readPassword("Senha: ");
}
```

> [!tip] Estude à parte
> Para fechar essas lacunas, use o capítulo de I/O do **Sybex (OCP Java SE 21)** e a **documentação oficial** do pacote `java.io`.

## Em entrevista

Um framing curto, sem reivindicar credencial:

> "In Java I/O I distinguish **byte streams** (`InputStream`/`OutputStream`) from **character streams** (`Reader`/`Writer`) — text goes through character streams so encoding is handled correctly. For serialization, I mark fields I don't want persisted as `transient`."

**Vocabulário PT | EN**
- fluxo de bytes → *byte stream*
- transitório → *transient*
- serialização → *serialization*

## Veja também

- [[03-Dominios/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho]]
- [[03-Dominios/Java/Certificação OCP/14 - Domínio 10 — Localização|Domínio 10 — Localização]]
- [[03-Dominios/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- Java I/O docs: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/io/package-summary.html
- Enthuware 21: https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus
