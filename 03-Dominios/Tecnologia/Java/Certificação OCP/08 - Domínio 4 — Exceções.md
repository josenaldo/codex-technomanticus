---
title: "Domínio 4 — Exceções"
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
  - "Domínio 4 OCP"
  - "Exceções na OCP"
---

# Domínio 4 — Exceções

> [!abstract] TL;DR
> Este domínio cobra a mecânica de tratamento de erros do Java: a hierarquia de `Throwable`, a distinção entre *checked* e *unchecked*, o fluxo exato de `try`/`catch`/`finally`, o `try-with-resources` (com seus *suppressed exceptions* e ordem reversa de fechamento) e as regras de `throws` na sobrescrita. A prova adora pegadinhas de **ordem de execução** — `return` no `finally`, ordem de `close()`, multi-catch que não compila. Domine o fluxo e o controle, não decore casos isolados.

> [!info] Títulos oficiais
> - **1Z0-830 (Java 21):** *Handling Exceptions*
> - **1Z0-831 (Java 25):** *Implementing Exception Handling in Java Applications*

## O que a Oracle cobra

- **Hierarquia** — `Throwable` é a raiz; abaixo dela, `Error` (falhas do ambiente, não se tratam) e `Exception`. Dentro de `Exception`, há `RuntimeException` e suas filhas (*unchecked*) e o restante (*checked*).
- **Checked vs unchecked** — *checked* obrigam tratamento ou propagação via `throws` (verificado em compilação); *unchecked* (`RuntimeException` e `Error`) não obrigam nada. Saber classificar uma exceção dada é cobrança recorrente.
- **try/catch/finally** — ordem de execução, multi-catch com `|`, *exception chaining* (`new RuntimeException("msg", causa)` e `getCause()`).
- **try-with-resources** — `AutoCloseable`/`Closeable`, *suppressed exceptions*, ordem de `close()`.
- **throws** — propagação de exceções pela pilha e regras de *overriding* (sobrescrita não pode ampliar o contrato de checked).
- **Custom exceptions** — criar subclasses de `Exception` ou `RuntimeException` com construtores que repassam mensagem e causa.
- **Assertions** — `assert cond : msg;`, habilitação via `-ea`. Raro, mas pode aparecer.

## Mapa de revisão

- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros|Exceções e tratamento de erros (G1)]] — toda a mecânica.

## Pegadinhas deste domínio

**(1) `return` no `try` e `return` no `finally` — o do `finally` vence.** O `finally` sempre executa, e se ele tem seu próprio `return`, descarta o valor que o `try` ia retornar:

```java
public int foo() {
    try {
        return 1;
    } finally {
        return 2; // retorna 2 — o return do try é descartado
    }
}
```

**(2) `try-with-resources` fecha na ORDEM REVERSA da declaração.** O último recurso aberto é o primeiro a ser fechado:

```java
try (var a = abrir("A"); var b = abrir("B")) {
    // ...
} // fecha B primeiro, depois A
```

**(3) Multi-catch não pode listar exceções relacionadas por herança.** Se uma já é subclasse da outra, há redundância e o código NÃO compila:

```java
try {
    // ...
} catch (IOException | FileNotFoundException e) { // ERRO de compilação:
    // FileNotFoundException já é subclasse de IOException
}
```

**(4) Sobrescrita não pode ADICIONAR checked exception.** O método que sobrescreve pode declarar as mesmas checked, uma subclasse delas, menos exceções ou nenhuma — mas nunca uma checked nova/mais ampla:

```java
class Pai {
    void m() throws IOException {}
}
class Filho extends Pai {
    @Override
    void m() throws FileNotFoundException {} // OK: subclasse de IOException
    // void m() throws Exception {}          // NÃO compila: amplia o contrato
}
```

**(5) Suppressed exceptions — a do `close()` fica suprimida se o corpo já lançou.** Se o bloco `try` lança e o `close()` também lança, a do corpo "vence" (é propagada) e a do `close()` vira *suppressed*, recuperável via `getSuppressed()`:

```java
try (var r = recursoQueFalhaAoFechar()) {
    throw new RuntimeException("erro no corpo"); // esta propaga
} // exceção do close() fica suprimida — e.getSuppressed()[0]
```

> [!tip] Para o catálogo completo
> Mais armadilhas de fluxo e compilação estão reunidas em [[03-Dominios/Tecnologia/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|catálogo de pegadinhas]].

## Em entrevista

Você não reivindica a credencial, mas o vocabulário aparece naturalmente ao falar de robustez:

> "I lean on try-with-resources so every `AutoCloseable` is closed in reverse order, and I check `getSuppressed()` when a failure during `close()` could mask the real error from the body."

Ou, sobre controle de fluxo:

> "A `return` in `finally` silently overrides the one in `try`, so I keep `finally` free of control-flow statements."

**Vocabulário PT | EN:**

- exceção verificada → *checked exception*
- exceção não verificada → *unchecked exception*
- exceção suprimida → *suppressed exception*
- encadeamento de exceções → *exception chaining*
- propagação → *propagation*
- sobrescrita → *overriding*

## Veja também

- [[03-Dominios/Tecnologia/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/09 - Domínio 5 — Arrays e coleções|Domínio 5 — Arrays e coleções]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus
