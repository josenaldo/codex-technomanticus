---
title: "Dicionário de Java"
created: 2026-06-02
updated: 2026-06-02
type: glossary
status: growing
publish: true
tags:
  - java
  - glossary
  - moc
aliases:
  - Glossário de Java
---

# Dicionário de Java

> Glossário do domínio Java: termos de linguagem, plataforma e ecossistema. Semeado com o Galho 1 — Linguagem e sintaxe moderna; cresce a cada galho incorporado.

<!--
Como usar este glossário:

- Cada verbete é um `###` dentro de uma `##` temática (seção alfabética).
- Verbetes em ordem alfabética dentro de cada seção; ordenação case-insensitive, sem considerar acento.
- Linkar de outra nota: wikilink para este arquivo com âncora `#` + nome do termo.
- Customizar o texto exibido: adicionar o pipe `|` após a âncora, seguido do texto.
- A skill /verbete adiciona termos automaticamente em ordem alfabética.
- Cada verbete tem (i) 1-3 frases de definição em PT-BR e (ii) "Veja também:" com wikilinks para a(s) nota(s) que aprofundam.
-->

## A

### Autoboxing
Conversão automática entre tipos primitivos (ex: `int`) e seus wrappers (`Integer`) feita pelo compilador Java. O processo inverso — de wrapper para primitivo — chama-se *unboxing*. Pode causar `NullPointerException` e overhead de alocação se usado em laços intensivos.

Veja também: [[02 - Tipos, variáveis e operadores]].

## B

### Bytecode
Representação intermediária compilada pelo `javac` a partir do código-fonte `.java`, gravada em arquivos `.class`. Não é código de máquina nativo: é executado (ou JIT-compilado) pela JVM, o que viabiliza o princípio WORA.

Veja também: [[01 - O modelo da linguagem Java]].

## C

### Checked exception
Exceção que o compilador obriga o desenvolvedor a declarar (`throws`) ou capturar (`try/catch`). Estende `Exception` (excluindo `RuntimeException`). Exemplos: `IOException`, `SQLException`. Usada quando o chamador pode se recuperar do erro.

Veja também: [[10 - Exceções e tratamento de erros]].

### Compact constructor
Construtor especial de records que omite a lista de parâmetros (não repete a assinatura) e executa antes da atribuição automática dos campos. Ideal para validação e normalização de dados sem boilerplate.

Veja também: [[13 - Records e record patterns]].

## D

### Default method
Método com implementação definido em uma interface (palavra-chave `default`), introduzido no Java 8. Permite adicionar comportamento a interfaces sem quebrar classes que as implementam, viabilizando evolução retrocompatível de APIs.

Veja também: [[08 - Interfaces e classes abstratas]].

## E

### Enhanced for
Laço `for-each` — forma simplificada do `for` que itera diretamente sobre arrays ou qualquer objeto `Iterable`, sem índice explícito. Sintaxe: `for (Tipo var : coleção) { }`. Introduzido no Java 5.

Veja também: [[03 - Estruturas de controle e fluxo]].

### Enum
Tipo especial de classe cujas instâncias são um conjunto fechado e nomeado de constantes. Em Java, enums são objetos de pleno direito: podem ter campos, construtores, métodos e implementar interfaces. Garantem type-safety e eliminam "magic numbers".

Veja também: [[09 - Enums]].

### Exaustividade
Propriedade de um `switch` (expressão ou statement) que garante que todos os casos possíveis são cobertos. O compilador Java exige exaustividade em switch expressions e em switches sobre sealed classes e enums. Violação gera erro em tempo de compilação.

Veja também: [[14 - Sealed classes e pattern matching]].

## G

### Generics
Mecanismo de parametrização de tipos que permite escrever classes, interfaces e métodos que operam sobre um tipo definido pelo chamador, com checagem em tempo de compilação. Elimina casts explícitos e detecta erros de tipo cedo. Ex: `List<String>`.

Veja também: [[12 - Generics em profundidade]].

### Guard
Condição booleana adicional (`when`) que refina um case de pattern matching. Permite combinar a verificação de tipo/estrutura com uma expressão lógica no mesmo braço do switch. Ex: `case Integer i when i > 0 -> ...`.

Veja também: [[14 - Sealed classes e pattern matching]].

## I

### Imutabilidade
Propriedade de um objeto cujo estado não pode ser alterado após a criação. Em Java, alcançada declarando campos `final`, não expondo mutadores e retornando cópias defensivas. Facilita raciocínio sobre o código e é segura para uso concorrente.

Veja também: [[06 - Classes, objetos e encapsulamento]].

### Inferência de tipo
Capacidade do compilador de deduzir o tipo de uma variável local a partir da expressão à direita, sem que o programador o declare explicitamente. Em Java (a partir do Java 10): `var nome = "Alice";`. Só se aplica a variáveis locais com inicializador.

Veja também: [[02 - Tipos, variáveis e operadores]].

## L

### LTS
Long-Term Support — versão do Java que recebe atualizações de segurança e correções por um período estendido (vários anos). Recomendada para produção. As principais versões LTS modernas são Java 8, 11, 17, 21 e 25.

Veja também: [[01 - O modelo da linguagem Java]], [[15 - A evolução do Java (8 a 25)]].

## O

### Overloading
Definição de múltiplos métodos com o mesmo nome mas assinaturas diferentes (quantidade ou tipos de parâmetros) em uma mesma classe. A resolução acontece em tempo de compilação com base nos tipos dos argumentos. Não deve ser confundido com overriding.

Veja também: [[07 - Herança e polimorfismo]].

### Overriding
Redefinição de um método herdado em uma subclasse, mantendo a mesma assinatura. Anotado com `@Override` para verificação do compilador. É o mecanismo base do polimorfismo dinâmico em Java — a JVM escolhe a implementação em tempo de execução pelo tipo real do objeto.

Veja também: [[07 - Herança e polimorfismo]].

## P

### Pattern matching
Mecanismo que combina teste de tipo, extração de componentes e (opcionalmente) uma guarda em uma única expressão coesa. A partir do Java 16 (`instanceof`) e Java 21 (switch patterns), elimina casts manuais e torna o código mais legível e seguro.

Veja também: [[14 - Sealed classes e pattern matching]].

### PECS
Producer Extends, Consumer Super — regra mnemônica para uso de wildcards em Generics. Use `? extends T` quando a coleção é fonte de dados (apenas leitura); use `? super T` quando a coleção é destino (apenas escrita). Define qual operação é type-safe em cada contexto.

Veja também: [[12 - Generics em profundidade]].

### Polimorfismo
Capacidade de um mesmo método ou referência se comportar de maneiras diferentes conforme o tipo real do objeto em tempo de execução. Em Java, é realizado principalmente por overriding + herança/interface. Permite escrever código genérico que opera sobre famílias de tipos.

Veja também: [[07 - Herança e polimorfismo]].

### Preview feature
Funcionalidade completa de linguagem ou JVM incluída em uma versão do Java para coleta de feedback, mas não finalizada. Precisa ser habilitada explicitamente com `--enable-preview` em compilação e execução. Pode mudar ou ser removida antes de tornar-se permanente.

Veja também: [[15 - A evolução do Java (8 a 25)]].

## R

### Record
Classe de dados imutável declarada com `record NomeClasse(Tipo campo, ...)`. O compilador gera automaticamente construtor canônico, acessores, `equals`, `hashCode` e `toString`. Ideal para portadores de dados sem lógica de negócio.

Veja também: [[13 - Records e record patterns]].

### Record pattern
Extensão de pattern matching que desconstói um record diretamente no `instanceof` ou `switch`, ligando seus componentes a variáveis locais. Permite navegação estrutural em hierarquias de dados sem getters explícitos.

Veja também: [[13 - Records e record patterns]], [[14 - Sealed classes e pattern matching]].

## S

### Sealed class
Classe (ou interface) que restringe explicitamente quais subclasses (ou subinterfaces) podem estendê-la, usando a palavra-chave `sealed` e a cláusula `permits`. Permite ao compilador verificar exaustividade em switches e torna hierarquias fechadas e explicitamente documentadas.

Veja também: [[14 - Sealed classes e pattern matching]].

### String pool
Área de memória (no heap, a partir do Java 7) onde a JVM armazena strings literais de forma deduplicada. Dois literais idênticos referenciam o mesmo objeto, economizando memória. Strings criadas com `new String(...)` não entram no pool automaticamente; `intern()` força a entrada.

Veja também: [[04 - Strings e text blocks]].

### Switch expression
Forma moderna do `switch` (Java 14+) que é uma expressão — produz um valor — e usa a sintaxe de seta (`case X -> valor`). Elimina fall-through acidental, exige exaustividade e pode ser atribuído diretamente a uma variável.

Veja também: [[03 - Estruturas de controle e fluxo]].

## T

### Text block
Literal de string multilinha delimitado por `"""` (Java 15+). Preserva a indentação relativa, suporta interpolação futura e elimina concatenações e escapes desnecessários em strings longas como SQL, JSON ou HTML embutido.

Veja também: [[04 - Strings e text blocks]].

### Try-with-resources
Construção `try (Recurso r = ...)` que garante o fechamento automático de qualquer objeto `AutoCloseable` ao fim do bloco, mesmo em caso de exceção. Elimina o padrão `finally { r.close(); }` e torna o gerenciamento de recursos mais seguro e legível.

Veja também: [[10 - Exceções e tratamento de erros]].

### Type erasure
Processo pelo qual o compilador Java remove as informações de tipo genérico em tempo de compilação, substituindo parâmetros de tipo por `Object` (ou pelo bound superior). Em tempo de execução, `List<String>` e `List<Integer>` são indistinguíveis, o que limita certas reflexões e casts.

Veja também: [[12 - Generics em profundidade]].

## U

### Unchecked exception
Exceção que não precisa ser declarada nem capturada obrigatoriamente. Estende `RuntimeException` ou `Error`. Exemplos: `NullPointerException`, `IllegalArgumentException`. Geralmente indica bugs ou estados inesperados que o chamador não tem como recuperar programaticamente.

Veja também: [[10 - Exceções e tratamento de erros]].

## V

### Varargs
Mecanismo que permite declarar um método com número variável de argumentos do mesmo tipo (`Tipo... nomes`). O compilador converte os argumentos em um array. Deve ser o último parâmetro da assinatura e gera um aviso se usado junto com generics por ambiguidade de heap pollution.

Veja também: [[05 - Arrays e varargs]].

## W

### Wildcard
Argumento de tipo genérico desconhecido, representado por `?`. Pode ser não-limitado (`?`), com limite superior (`? extends T`) ou com limite inferior (`? super T`). Aumenta a flexibilidade das APIs genéricas ao custo de restringir as operações permitidas sobre a coleção.

Veja também: [[12 - Generics em profundidade]].

### WORA
Write Once, Run Anywhere — princípio central do Java: o bytecode compilado roda em qualquer plataforma que possua uma JVM compatível, sem recompilação. Viabilizado pela camada de abstração da JVM entre o código e o hardware/SO.

Veja também: [[01 - O modelo da linguagem Java]].

## Y

### Yield
Palavra-chave usada dentro de um bloco de switch expression (`case X -> { ... yield valor; }`) para retornar o valor produzido pelo bloco. Necessário quando o braço do switch contém mais de uma instrução; na sintaxe de seta simples, o valor é retornado diretamente sem `yield`.

Veja também: [[03 - Estruturas de controle e fluxo]].
