---
title: "Helsinki MOOC — Guia de Revisão Java"
created: 2026-04-10
updated: 2026-04-10
type: how-to
status: evergreen
tags:
  - java
  - iniciante
  - revisao
publish: false
---

# Helsinki MOOC — Guia de Revisão Java

Resumo em português do curso **[Java Programming](https://java-programming.mooc.fi)** da Universidade de Helsinki (Agile Education Research Group / MOOC.fi) — um dos melhores cursos gratuitos de Java do mundo. Esta nota serve como **guia de consulta rápida e revisão** para quem está começando em Java ou para quem não mexe com a linguagem há tempos e precisa relembrar os fundamentos.

Para tópicos avançados, ver [[Java Fundamentals]], [[Java Concurrency]] e [[Testes em Java]].

## Sobre o curso

O curso é dividido em duas partes:

- **Java Programming I** (Partes 1-7) — fundamentos: variáveis, loops, métodos, listas, arrays, strings, introdução à orientação a objetos
- **Java Programming II** (Partes 8-14) — tópicos avançados: HashMap, herança, interfaces, streams, exceções, arquivos, genéricos, JavaFX

Cada parte equivale a **1 semana de estudo** (10+ horas). O curso é gratuito, em inglês, e a nota é dada por exercícios práticos no TMC (Test My Code) plugin da IDE NetBeans/IntelliJ.

**Objetivo deste guia:** não reproduzir o curso inteiro (ele já existe), mas oferecer um **mapa consultável** com os tópicos principais, exemplos resumidos em código, e pontos de atenção para quem precisa revisar.

---

## Como usar este guia

- **Iniciante absoluto** — leia sequencialmente, faça as partes 1-7, depois 8-14
- **Desenvolvedor vindo de outra linguagem** — pule para Parte 4 (OOP) e acelere
- **Dev Java precisando revisar** — use como índice, consulte a seção que precisar
- **Preparação para entrevistas juniors** — revise todas as partes de 1-11

Cada parte tem: **o que você aprende** → **exemplos de código** → **erros comuns** → **extensões além do curso**.

---

# Java Programming I

## Parte 1 — Primeiros passos em programação

**Objetivo:** aprender a escrever, compilar e executar um programa Java básico. Entender saída, entrada, variáveis, cálculos e condicionais.

### 1.1 Como funciona um programa Java

Java é uma linguagem compilada. O ciclo é:

```
código fonte (.java)
    ↓  javac
bytecode (.class)
    ↓  java (JVM)
execução
```

Todo programa Java tem uma **classe** com um método `main` — o ponto de entrada.

```java
public class Main {
    public static void main(String[] args) {
        // código aqui
    }
}
```

### 1.2 Imprimindo na tela

`System.out.println` imprime e quebra linha. `System.out.print` imprime sem quebrar.

```java
System.out.println("Olá, mundo!");
System.out.print("Sem ");
System.out.println("quebra");

// Múltiplas linhas
System.out.println("Linha 1");
System.out.println("Linha 2");
```

**Dica moderna:** em Java 21+ com instance main (preview), você pode simplificar:

```java
void main() {
    println("Olá, mundo!");  // Java 21+ preview
}
```

### 1.3 Lendo entrada do usuário

Use a classe `Scanner`:

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Qual é o seu nome? ");
        String nome = scanner.nextLine();

        System.out.println("Olá, " + nome + "!");
    }
}
```

**Métodos do Scanner:**

- `nextLine()` — lê uma linha inteira (String)
- `nextInt()` — lê um inteiro
- `nextDouble()` — lê um double

**Cuidado:** `nextInt()` deixa o `\n` no buffer. Se for ler linha depois, chame `nextLine()` primeiro para consumir.

### 1.4 Variáveis

Uma variável é um nome com um tipo e um valor. Em Java, você **declara o tipo**.

```java
int idade = 30;           // inteiro
double preco = 19.99;     // decimal
String nome = "Maria";    // texto
boolean ativo = true;     // verdadeiro/falso
char letra = 'A';         // caractere único
```

**Tipos primitivos mais usados:**

| Tipo      | O que guarda     | Exemplo                                        |
| --------- | ---------------- | ---------------------------------------------- |
| `int`     | Inteiros         | `42`, `-7`, `0`                                |
| `double`  | Decimais         | `3.14`, `-0.5`                                 |
| `boolean` | Verdadeiro/falso | `true`, `false`                                |
| `char`    | 1 caractere      | `'A'`, `'%'`                                   |
| `String`  | Texto            | `"Maria"` (na verdade é classe, não primitivo) |

**Nomes de variáveis:** `camelCase`, começando com letra minúscula, descritivos. `idadeDoPaciente`, não `x` ou `ip`.

### 1.5 Calculando com números

Operadores matemáticos: `+`, `-`, `*`, `/`, `%` (resto).

```java
int a = 10;
int b = 3;

System.out.println(a + b);  // 13
System.out.println(a - b);  // 7
System.out.println(a * b);  // 30
System.out.println(a / b);  // 3 (!) — divisão inteira
System.out.println(a % b);  // 1

double x = 10.0;
double y = 3.0;
System.out.println(x / y);  // 3.3333333...
```

**Armadilha clássica:** `10 / 3` em `int` é `3`, não `3.33`. Para obter decimal, pelo menos um operando precisa ser `double`.

```java
double resultado = (double) 10 / 3;  // 3.333...
```

**Conversão de String para número:**

```java
String entrada = scanner.nextLine();
int numero = Integer.parseInt(entrada);
double decimal = Double.parseDouble(entrada);
```

### 1.6 Declarações condicionais

`if` executa código se uma condição é verdadeira. `else` executa o oposto.

```java
int idade = 20;

if (idade >= 18) {
    System.out.println("Maior de idade");
} else if (idade >= 13) {
    System.out.println("Adolescente");
} else {
    System.out.println("Criança");
}
```

**Operadores de comparação:** `==`, `!=`, `<`, `>`, `<=`, `>=`

**Operadores lógicos:** `&&` (E), `||` (OU), `!` (NÃO)

```java
if (idade >= 18 && temCarteira) {
    System.out.println("Pode dirigir");
}
```

**Atenção com Strings:** nunca use `==` para comparar Strings. Use `.equals()`:

```java
String nome = scanner.nextLine();

if (nome == "Maria") { ... }        // ERRADO (compara referência)
if (nome.equals("Maria")) { ... }    // CERTO (compara conteúdo)
```

### Erros comuns na Parte 1

- **Esquecer `;`** no fim da linha
- **Usar `=` em condicional** — `if (x = 5)` é atribuição, não comparação. Use `==`
- **Comparar String com `==`** — use `.equals()`
- **Divisão inteira quando queria decimal** — cast pelo menos um operando para `double`
- **Scanner + nextInt() + nextLine()** — o `\n` fica no buffer

---

## Parte 2 — Repetição e métodos

**Objetivo:** aprender a repetir código (loops) e dividir o programa em métodos.

### 2.1 Problemas recorrentes

Programas reais repetem muito. Em vez de copiar-colar código, usamos **loops** (repetição) e **métodos** (reutilização).

### 2.2 While loop

Repete enquanto a condição for verdadeira.

```java
int i = 0;
while (i < 5) {
    System.out.println("i = " + i);
    i++;  // equivalente a i = i + 1
}
// Imprime 0, 1, 2, 3, 4
```

**Uso típico:** ler entrada até o usuário digitar algo específico.

```java
Scanner scanner = new Scanner(System.in);
while (true) {
    System.out.print("Digite algo (ou 'sair'): ");
    String entrada = scanner.nextLine();

    if (entrada.equals("sair")) {
        break;  // sai do loop
    }

    System.out.println("Você digitou: " + entrada);
}
```

### 2.3 For loop

Loop mais compacto quando você sabe quantas iterações precisa.

```java
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}
// Imprime 0 a 9
```

Estrutura: `for (inicialização; condição; incremento)`.

**For-each** (para listas/arrays — detalhes na Parte 3):

```java
int[] numeros = {1, 2, 3, 4, 5};
for (int n : numeros) {
    System.out.println(n);
}
```

### 2.4 Mais sobre loops

**Loops aninhados** (loop dentro de loop):

```java
for (int i = 1; i <= 3; i++) {
    for (int j = 1; j <= 3; j++) {
        System.out.print(i * j + " ");
    }
    System.out.println();
}
// 1 2 3
// 2 4 6
// 3 6 9
```

**`break`** — sai do loop imediatamente. **`continue`** — pula para a próxima iteração.

```java
for (int i = 0; i < 10; i++) {
    if (i == 5) break;          // para quando chega em 5
    if (i % 2 == 0) continue;   // pula números pares
    System.out.println(i);
}
// Imprime: 1, 3
```

### 2.5 Métodos

Método é um bloco de código reutilizável com nome.

```java
public class Main {
    public static void main(String[] args) {
        cumprimentar("Maria");
        cumprimentar("João");

        int soma = somar(5, 3);
        System.out.println("Soma: " + soma);
    }

    public static void cumprimentar(String nome) {
        System.out.println("Olá, " + nome + "!");
    }

    public static int somar(int a, int b) {
        return a + b;
    }
}
```

**Anatomia de um método:**

```java
public static int somar(int a, int b) {
//  ↑      ↑     ↑     ↑       ↑
//  │      │     │     │       └── parâmetros (entrada)
//  │      │     │     └────────── nome do método
//  │      │     └──────────────── tipo de retorno
//  │      └────────────────────── pertence à classe (estático)
//  └───────────────────────────── visibilidade
    return a + b;  // valor retornado
}
```

**Se um método não retorna valor, o tipo é `void`:**

```java
public static void cumprimentar(String nome) {
    System.out.println("Olá, " + nome);
    // sem return
}
```

### Erros comuns na Parte 2

- **Loop infinito** — esquecer de atualizar a variável de controle (`while (i < 5) { ... }` sem `i++`)
- **Off-by-one** — usar `<=` quando queria `<`, ou vice-versa
- **Chamar método estático de instância** — confusão com `static`
- **Esquecer `return`** em método que deveria retornar
- **Método com tipo `void` tentando retornar algo**

### Dica extra

Divida seu código em métodos pequenos. Um método bom faz **uma coisa só** e tem um nome que descreve exatamente o que faz. Se você está usando `e` na descrição ("ler dados E calcular média"), provavelmente deveriam ser dois métodos.

---

## Parte 3 — Listas, arrays e strings

**Objetivo:** trabalhar com coleções de dados — listas dinâmicas, arrays fixos, e manipulação de strings.

### 3.1 Descobrindo erros

**Tipos de erro:**

- **Sintático** — código não compila (`;` faltando). Compilador avisa.
- **Runtime** — programa quebra durante execução (`NullPointerException`). Erro na hora.
- **Lógico** — programa roda, mas produz resultado errado. O pior tipo.

**Debugging:**

- **Print statements** — adicione `System.out.println` para ver variáveis
- **Debugger da IDE** — breakpoints, inspecionar variáveis passo a passo
- **Ler a mensagem do erro inteira** — stack trace mostra exatamente onde quebrou
- **Reduzir o problema** — criar exemplo mínimo que reproduz o bug

### 3.2 Listas (ArrayList)

Lista dinâmica — cresce conforme você adiciona elementos.

```java
import java.util.ArrayList;

ArrayList<String> nomes = new ArrayList<>();
nomes.add("Maria");
nomes.add("João");
nomes.add("Ana");

System.out.println(nomes.size());      // 3
System.out.println(nomes.get(0));      // "Maria"
nomes.remove("João");
System.out.println(nomes.contains("Ana"));  // true

// Iterar
for (String nome : nomes) {
    System.out.println(nome);
}
```

**Métodos comuns de `ArrayList`:**

| Método                             | O que faz                  |
| ---------------------------------- | -------------------------- |
| `add(elem)`                        | Adiciona no final          |
| `get(índice)`                      | Retorna elemento no índice |
| `set(índice, elem)`                | Substitui elemento         |
| `remove(elem)` ou `remove(índice)` | Remove                     |
| `size()`                           | Tamanho da lista           |
| `contains(elem)`                   | Verifica se contém         |
| `indexOf(elem)`                    | Índice do elemento         |
| `isEmpty()`                        | Lista vazia?               |
| `clear()`                          | Remove tudo                |

**`<String>` é o tipo parametrizado** — diz que a lista só aceita Strings. Mais sobre isso na Parte 12.

### 3.3 Arrays

Array é uma coleção de **tamanho fixo**. Mais primitivo que lista.

```java
int[] numeros = new int[5];     // array de 5 inteiros, todos 0
numeros[0] = 10;
numeros[1] = 20;

System.out.println(numeros[0]);       // 10
System.out.println(numeros.length);    // 5 — é propriedade, não método

// Inicialização com valores
int[] primos = {2, 3, 5, 7, 11};

// Iterar
for (int i = 0; i < primos.length; i++) {
    System.out.println(primos[i]);
}

// Ou for-each
for (int p : primos) {
    System.out.println(p);
}
```

**Arrays multidimensionais:**

```java
int[][] matriz = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};
System.out.println(matriz[1][2]);  // 6
```

### 3.4 Strings

Strings em Java são **imutáveis** — qualquer operação retorna uma nova String, sem modificar a original.

```java
String texto = "Olá, Mundo";

texto.length();               // 10
texto.charAt(0);              // 'O'
texto.substring(0, 3);        // "Olá"
texto.substring(5);           // "Mundo"
texto.toUpperCase();          // "OLÁ, MUNDO"
texto.toLowerCase();          // "olá, mundo"
texto.contains("Mundo");      // true
texto.startsWith("Olá");      // true
texto.endsWith("do");         // true
texto.indexOf("M");           // 5
texto.replace("Mundo", "Maria"); // "Olá, Maria"
texto.trim();                 // remove espaços nas pontas

// Split — divide em array
String csv = "a,b,c,d";
String[] partes = csv.split(",");  // ["a", "b", "c", "d"]

// Concatenação
String nome = "Maria";
int idade = 30;
String msg = nome + " tem " + idade + " anos";
// Ou formatado (Java 15+)
String msg2 = "%s tem %d anos".formatted(nome, idade);
```

**Comparação de Strings:**

```java
String a = "hello";
String b = "hello";
String c = new String("hello");

a == b;         // true (ambas do pool interno)
a == c;         // false (c é novo objeto)
a.equals(c);    // true (mesmo conteúdo)

// Ignorar caixa
"Hello".equalsIgnoreCase("hello");  // true
```

**Regra de ouro:** sempre use `.equals()` para comparar strings. Nunca `==`.

### Erros comuns na Parte 3

- **IndexOutOfBoundsException** — acessar índice que não existe (`lista.get(10)` quando a lista tem 5 elementos)
- **NullPointerException** — tentar operar em algo `null`
- **Modificar lista durante iteração** — causa `ConcurrentModificationException`. Use iterator ou copie antes.
- **Usar `==` em Strings** — funciona às vezes (por causa do pool interno) e quebra outras. Sempre `.equals()`.
- **Esquecer que `String` é imutável** — `texto.toUpperCase();` sozinho não faz nada. Precisa `texto = texto.toUpperCase();`

---

## Parte 4 — Introdução à Programação Orientada a Objetos

**Objetivo:** entender classes, objetos, métodos de instância, construtores. O começo da POO.

### 4.1 O que é POO

Programação Orientada a Objetos organiza o código em **objetos** — unidades que têm dados (atributos) e comportamento (métodos).

**Analogia:** uma classe é como uma receita de bolo. Um objeto é o bolo pronto. Você pode fazer vários bolos com a mesma receita.

### 4.2 Classes e objetos

```java
public class Pessoa {
    // Atributos (dados)
    private String nome;
    private int idade;

    // Construtor — cria um objeto
    public Pessoa(String nome, int idade) {
        this.nome = nome;
        this.idade = idade;
    }

    // Métodos (comportamento)
    public String getNome() {
        return nome;
    }

    public int getIdade() {
        return idade;
    }

    public void fazerAniversario() {
        this.idade++;
    }

    public String toString() {
        return nome + ", " + idade + " anos";
    }
}
```

Uso:

```java
public class Main {
    public static void main(String[] args) {
        Pessoa maria = new Pessoa("Maria", 30);
        Pessoa joao = new Pessoa("João", 25);

        System.out.println(maria);  // chama toString automaticamente → "Maria, 30 anos"
        maria.fazerAniversario();
        System.out.println(maria);  // "Maria, 31 anos"
    }
}
```

### 4.3 Conceitos importantes

**`this`** — referência ao objeto atual. Usado para distinguir campo do parâmetro.

```java
public Pessoa(String nome, int idade) {
    this.nome = nome;    // this.nome é o campo; nome é o parâmetro
    this.idade = idade;
}
```

**`new`** — cria um novo objeto chamando o construtor.

```java
Pessoa p = new Pessoa("Maria", 30);
```

**`private` vs `public`:**

- **`private`** — só a própria classe acessa (encapsulamento)
- **`public`** — qualquer classe acessa

Regra prática: **atributos privados, métodos públicos quando necessário**. Isso protege o estado interno do objeto.

**Getters e Setters:**

```java
private String nome;

public String getNome() {           // getter
    return nome;
}

public void setNome(String nome) {  // setter
    this.nome = nome;
}
```

Getters permitem ler; setters permitem modificar de forma controlada (podem validar).

### 4.4 Objetos em listas

Você pode ter listas de qualquer tipo, inclusive dos seus próprios objetos:

```java
ArrayList<Pessoa> pessoas = new ArrayList<>();
pessoas.add(new Pessoa("Maria", 30));
pessoas.add(new Pessoa("João", 25));

for (Pessoa p : pessoas) {
    System.out.println(p.getNome());
}
```

### 4.5 Lendo de arquivos

Usa `Scanner` com um arquivo, ou `Files.readAllLines` (mais moderno):

```java
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

List<String> linhas = Files.readAllLines(Paths.get("dados.txt"));
for (String linha : linhas) {
    System.out.println(linha);
}
```

### Erros comuns na Parte 4

- **Esquecer `this`** quando parâmetro e campo têm o mesmo nome
- **Não inicializar no construtor** — campos ficam com default (`null`, `0`, `false`)
- **Esquecer `new`** ao criar objeto — `Pessoa p = Pessoa(...)` não compila
- **Tornar tudo `public`** — quebra encapsulamento
- **Não sobrescrever `toString()`** — imprime lixo como `Pessoa@7a81197d`

---

## Parte 5 — Mais sobre Orientação a Objetos

**Objetivo:** overloading, variáveis primitivas vs referências, como objetos são armazenados.

### 5.1 Aprendendo POO

**Comportamento no objeto.** Evite colocar lógica em classes externas que manipulam o objeto. Se o comportamento pertence ao objeto, coloque no próprio objeto.

```java
// RUIM — lógica fora do objeto
Pessoa p = new Pessoa("Maria", 30);
p.setIdade(p.getIdade() + 1);  // envelhecer manualmente

// BOM — lógica dentro do objeto
p.fazerAniversario();
```

### 5.2 Overloading (sobrecarga)

Múltiplos métodos/construtores com o mesmo nome, diferenciados pelos parâmetros.

```java
public class Calculadora {
    public int somar(int a, int b) {
        return a + b;
    }

    public double somar(double a, double b) {
        return a + b;
    }

    public int somar(int a, int b, int c) {
        return a + b + c;
    }
}
```

**Overloading de construtor** — muito comum:

```java
public class Pessoa {
    private String nome;
    private int idade;

    public Pessoa(String nome, int idade) {
        this.nome = nome;
        this.idade = idade;
    }

    // Construtor sobrecarregado — assume idade 0
    public Pessoa(String nome) {
        this(nome, 0);  // chama o outro construtor
    }
}
```

`this(args)` no começo do construtor chama outro construtor da mesma classe — evita duplicação.

### 5.3 Variáveis primitivas vs referências

**Primitivas** (`int`, `double`, `boolean`, `char`) — guardam o **valor** diretamente.

**Referências** (objetos, Strings, Arrays) — guardam um **endereço** que aponta para o objeto.

```java
int a = 10;
int b = a;  // copia o valor
b = 20;
System.out.println(a);  // 10 — a não mudou

Pessoa p1 = new Pessoa("Maria");
Pessoa p2 = p1;  // copia a referência, ambos apontam para o MESMO objeto
p2.setNome("João");
System.out.println(p1.getNome());  // "João" — p1 também vê a mudança!
```

### 5.4 Objetos e referências

Implicações práticas:

**1. Passar objeto para método:** a função recebe a mesma referência, pode modificar o objeto original.

```java
public static void envelhecer(Pessoa p) {
    p.fazerAniversario();  // modifica o objeto passado
}

Pessoa maria = new Pessoa("Maria", 30);
envelhecer(maria);
System.out.println(maria.getIdade());  // 31
```

**2. Igualdade:** `==` compara referências (mesmo objeto na memória), `.equals()` compara conteúdo (se sobrescrito).

```java
Pessoa p1 = new Pessoa("Maria", 30);
Pessoa p2 = new Pessoa("Maria", 30);

p1 == p2;         // false (objetos diferentes na memória)
p1.equals(p2);    // depende da implementação de equals na classe Pessoa
```

**3. `null`:** uma referência pode apontar para "nada". Chamar método em `null` causa `NullPointerException`.

```java
Pessoa p = null;
p.getNome();  // NullPointerException
```

### Erros comuns na Parte 5

- **Confundir cópia de valor com cópia de referência** — modificar "uma cópia" de objeto modifica o original
- **Esquecer de sobrescrever `equals()`** — herda do Object, compara referências
- **NullPointerException** — não verificar se objeto é `null` antes de usar
- **Construtores com código duplicado** — use `this(...)` para chamar outro construtor

---

## Parte 6 — Programas mais complexos

**Objetivo:** separar interface do usuário da lógica, testar código, construir programas maiores.

### 6.1 Objetos em listas, listas como parte de objetos

Você pode ter listas **dentro** de objetos. Exemplo: uma Turma tem uma lista de Alunos.

```java
public class Turma {
    private String nome;
    private ArrayList<Aluno> alunos;

    public Turma(String nome) {
        this.nome = nome;
        this.alunos = new ArrayList<>();
    }

    public void adicionarAluno(Aluno a) {
        this.alunos.add(a);
    }

    public int quantidadeDeAlunos() {
        return alunos.size();
    }

    public double mediaDasIdades() {
        if (alunos.isEmpty()) return 0;

        int soma = 0;
        for (Aluno a : alunos) {
            soma += a.getIdade();
        }
        return (double) soma / alunos.size();
    }
}
```

### 6.2 Separando interface do usuário da lógica

Programas que misturam entrada do usuário com lógica de negócio ficam **acoplados** e difíceis de testar. Separe!

**Anti-pattern:**

```java
// Tudo no main — ruim
Scanner scanner = new Scanner(System.in);
while (true) {
    System.out.print("Comando: ");
    String cmd = scanner.nextLine();

    if (cmd.equals("adicionar")) {
        // lógica misturada com UI
    } else if (cmd.equals("listar")) {
        // ...
    }
}
```

**Melhor — separar em classes:**

```java
public class AgendaApp {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Agenda agenda = new Agenda();           // lógica
        AgendaUI ui = new AgendaUI(agenda, scanner);  // interface
        ui.iniciar();
    }
}

public class Agenda {
    private ArrayList<String> contatos;

    public void adicionarContato(String nome) { ... }
    public ArrayList<String> listarContatos() { return contatos; }
    // ... pura lógica, sem input/output
}

public class AgendaUI {
    private Agenda agenda;
    private Scanner scanner;

    public void iniciar() {
        // loop de menu, chama métodos da Agenda
    }
}
```

**Vantagens:**

- Agenda pode ser testada sem UI
- UI pode ser trocada (terminal, GUI, web) sem mudar a lógica
- Código mais fácil de entender

### 6.3 Introdução a testes

Teste automatizado verifica que seu código funciona como esperado. **JUnit** é a biblioteca padrão.

```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CalculadoraTest {

    @Test
    public void somarDoisNumerosPositivos() {
        Calculadora calc = new Calculadora();
        int resultado = calc.somar(2, 3);
        assertEquals(5, resultado);
    }

    @Test
    public void somarComZero() {
        Calculadora calc = new Calculadora();
        assertEquals(10, calc.somar(10, 0));
    }
}
```

**Estrutura de um teste:**

1. **Arrange** — preparar o cenário (criar objetos)
2. **Act** — executar o método que está sendo testado
3. **Assert** — verificar o resultado esperado

**Assertions comuns:**

- `assertEquals(esperado, atual)` — devem ser iguais
- `assertTrue(condição)` — deve ser verdadeiro
- `assertFalse(condição)` — deve ser falso
- `assertNull(objeto)` — deve ser null
- `assertNotNull(objeto)` — não deve ser null

→ Para deep dive em testes, ver [[Testes em Java]].

### 6.4 Programas complexos

Quando o programa cresce, divida em múltiplas classes, cada uma com responsabilidade clara:

```
Modelo (lógica de negócio):
  - Pessoa, Turma, Agenda...

Serviços (operações):
  - AgendaService, UsuarioService...

UI (interação):
  - TerminalUI, GraphicalUI...

Persistência (dados):
  - ArquivoLeitor, BancoDados...
```

**Princípio:** cada classe tem **uma responsabilidade** (Single Responsibility Principle — parte do SOLID).

### Erros comuns na Parte 6

- **Classe "Deus"** — uma classe que faz tudo (1000+ linhas). Divida!
- **UI misturada com lógica** — dificulta testes e reuso
- **Testes que dependem uns dos outros** — cada teste deve ser independente
- **Mocks onde não precisa** — tente testar a coisa real primeiro

---

## Parte 7 — Paradigmas e algoritmos

**Objetivo:** conhecer paradigmas de programação, algoritmos básicos (ordenação, busca), e concluir o Java Programming I.

### 7.1 Paradigmas de programação

Um paradigma é uma forma de pensar sobre programação. Java suporta vários:

**Imperativo / Procedural** — sequência de comandos. C, Python procedural.

```java
int soma = 0;
for (int i = 0; i < numeros.length; i++) {
    soma += numeros[i];
}
```

**Orientado a Objetos** — objetos com estado e comportamento. Java, C++, C#.

```java
Calculadora calc = new Calculadora();
int soma = calc.somar(numeros);
```

**Funcional** — funções como valores, imutabilidade, sem side effects. Haskell, Scala, JavaScript moderno.

```java
// Java também suporta, desde Java 8
int soma = Arrays.stream(numeros).sum();
```

**Declarativo** — você diz *o que* quer, não *como* fazer. SQL, HTML.

```sql
SELECT SUM(preco) FROM produtos;
```

Java é **principalmente OO**, mas desde Java 8 incorporou features funcionais (lambdas, streams) — ver Parte 10.

### 7.2 Algoritmos

Um algoritmo é uma sequência de passos para resolver um problema. Os clássicos:

**Busca linear** (O(n)) — percorre a lista do início ao fim:

```java
public static int buscar(int[] arr, int alvo) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == alvo) {
            return i;
        }
    }
    return -1;  // não encontrado
}
```

**Busca binária** (O(log n)) — só funciona em array **ordenado**:

```java
public static int buscarBinaria(int[] arr, int alvo) {
    int inicio = 0;
    int fim = arr.length - 1;

    while (inicio <= fim) {
        int meio = (inicio + fim) / 2;
        if (arr[meio] == alvo) return meio;
        if (arr[meio] < alvo) inicio = meio + 1;
        else fim = meio - 1;
    }
    return -1;
}
```

**Ordenação — Bubble Sort** (O(n²), lento mas simples):

```java
public static void bubbleSort(int[] arr) {
    for (int i = 0; i < arr.length - 1; i++) {
        for (int j = 0; j < arr.length - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                // trocar
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}
```

**Na prática:** use `Arrays.sort(arr)` ou `Collections.sort(lista)` — são muito mais rápidos (O(n log n)).

```java
int[] arr = {5, 2, 8, 1, 9};
Arrays.sort(arr);  // {1, 2, 5, 8, 9}
```

### 7.3 Notação Big-O

Forma de comparar a **eficiência** de algoritmos.

| Notação      | Exemplo                  | Crescimento  |
| ------------ | ------------------------ | ------------ |
| `O(1)`       | Acessar array por índice | Constante    |
| `O(log n)`   | Busca binária            | Logarítmico  |
| `O(n)`       | Busca linear             | Linear       |
| `O(n log n)` | Merge sort, quick sort   | Linear × log |
| `O(n²)`      | Bubble sort              | Quadrático   |
| `O(2^n)`     | Fibonacci recursivo      | Exponencial  |

Para deep dive, ver [[Algoritmos]] e [[Estruturas de Dados]].

### Erros comuns na Parte 7

- **Busca binária em array não ordenado** — resultado incorreto
- **Inventar algoritmo de ordenação** — use `Arrays.sort`, é mais rápido
- **Não pensar em complexidade** — loops aninhados em listas grandes matam a performance

---

# Java Programming II

## Parte 8 — HashMap

**Objetivo:** dominar `HashMap`, entender igualdade de objetos (`equals`/`hashCode`), agrupar dados.

### 8.1 Recapitulação

A Parte 8 começa revisando POO, listas, e introduz a próxima estrutura de dados: HashMap.

### 8.2 HashMap

HashMap é um dicionário — associa **chaves** a **valores**. Acesso é **O(1)** (muito rápido).

```java
import java.util.HashMap;

HashMap<String, Integer> idades = new HashMap<>();
idades.put("Maria", 30);
idades.put("João", 25);
idades.put("Ana", 28);

System.out.println(idades.get("Maria"));         // 30
System.out.println(idades.containsKey("João"));  // true
System.out.println(idades.size());                // 3

idades.remove("João");

// Iterar
for (String nome : idades.keySet()) {
    System.out.println(nome + ": " + idades.get(nome));
}

// Ou pegar entradas
for (Map.Entry<String, Integer> entry : idades.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}
```

**Métodos principais:**

| Método                         | O que faz                               |
| ------------------------------ | --------------------------------------- |
| `put(chave, valor)`            | Adiciona/atualiza                       |
| `get(chave)`                   | Retorna valor (ou `null` se não existe) |
| `containsKey(chave)`           | Verifica se chave existe                |
| `remove(chave)`                | Remove entrada                          |
| `size()`                       | Número de entradas                      |
| `keySet()`                     | Conjunto de chaves                      |
| `values()`                     | Coleção de valores                      |
| `entrySet()`                   | Conjunto de entradas (chave+valor)      |
| `getOrDefault(chave, default)` | Retorna valor ou default se não existe  |

### 8.3 Igualdade de objetos

Para usar **seus próprios objetos como chave** de HashMap, você precisa implementar `equals` e `hashCode`.

```java
public class Pessoa {
    private String nome;
    private String cpf;

    // ... construtor, getters

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Pessoa)) return false;
        Pessoa outra = (Pessoa) obj;
        return this.cpf.equals(outra.cpf);  // duas pessoas são iguais se têm o mesmo CPF
    }

    @Override
    public int hashCode() {
        return cpf.hashCode();
    }
}
```

**Contrato equals/hashCode:**

1. Se `a.equals(b)` é `true`, então `a.hashCode() == b.hashCode()` deve ser `true`
2. Se `a.hashCode() == b.hashCode()`, **não** significa que `a.equals(b)` — pode ser colisão
3. Se não cumprir o contrato, `HashMap` e `HashSet` não funcionam corretamente

**Em Java moderno:** use `Objects.equals()` e `Objects.hash()`:

```java
import java.util.Objects;

@Override
public boolean equals(Object obj) {
    if (this == obj) return true;
    if (!(obj instanceof Pessoa)) return false;
    Pessoa outra = (Pessoa) obj;
    return Objects.equals(this.cpf, outra.cpf);
}

@Override
public int hashCode() {
    return Objects.hash(cpf);
}
```

**Melhor ainda — Records (Java 16+)** geram equals/hashCode automaticamente:

```java
public record Pessoa(String nome, String cpf) {}
// equals, hashCode, toString automáticos!
```

### 8.4 Agrupando dados com HashMap

Caso comum: contar ocorrências ou agrupar.

**Contar palavras em um texto:**

```java
String[] palavras = texto.split(" ");
HashMap<String, Integer> contagem = new HashMap<>();

for (String p : palavras) {
    contagem.put(p, contagem.getOrDefault(p, 0) + 1);
}
```

**Agrupar pessoas por idade:**

```java
HashMap<Integer, ArrayList<Pessoa>> porIdade = new HashMap<>();

for (Pessoa p : pessoas) {
    porIdade.computeIfAbsent(p.getIdade(), k -> new ArrayList<>()).add(p);
}
```

### 8.5 Busca rápida com HashMap

HashMap é ideal para busca rápida. Em vez de percorrer lista (O(n)), busca direto pela chave (O(1)).

```java
// RUIM — busca linear
for (Pessoa p : pessoas) {
    if (p.getCpf().equals("123.456.789-00")) {
        return p;
    }
}

// MELHOR — HashMap indexado por CPF
HashMap<String, Pessoa> porCpf = new HashMap<>();
for (Pessoa p : pessoas) {
    porCpf.put(p.getCpf(), p);
}
Pessoa p = porCpf.get("123.456.789-00");  // O(1)
```

### Erros comuns na Parte 8

- **Usar objeto como chave sem sobrescrever equals/hashCode** — não encontra nada
- **`get()` retornando `null`** — chave não existe, precisa verificar
- **Modificar objeto após colocar como chave** — quebra o hash, HashMap perde a entrada
- **Iterar e modificar** — `ConcurrentModificationException`

---

## Parte 9 — Herança e Interfaces

**Objetivo:** os dois mecanismos fundamentais de extensibilidade em POO.

### 9.1 Herança

Uma classe pode **estender** outra, herdando seus atributos e métodos.

```java
public class Animal {
    protected String nome;

    public Animal(String nome) {
        this.nome = nome;
    }

    public void comer() {
        System.out.println(nome + " está comendo");
    }
}

public class Cachorro extends Animal {
    public Cachorro(String nome) {
        super(nome);  // chama construtor do pai
    }

    public void latir() {
        System.out.println(nome + " disse: Au au!");
    }
}

// Uso
Cachorro rex = new Cachorro("Rex");
rex.comer();   // herdado de Animal
rex.latir();   // específico de Cachorro
```

**`super`** — referência à classe pai. `super(...)` chama construtor; `super.metodo()` chama método do pai.

**`protected`** — visível para a classe e suas filhas (mais aberto que `private`, mais fechado que `public`).

**Sobrescrita (override)** — filha redefine método do pai:

```java
public class Gato extends Animal {
    public Gato(String nome) {
        super(nome);
    }

    @Override
    public void comer() {
        System.out.println(nome + " está comendo (de um jeito elegante)");
    }
}
```

`@Override` é opcional mas recomendado — o compilador avisa se você errou a assinatura.

### 9.2 Interfaces

Interface define um **contrato** — métodos que as classes implementadoras devem ter, sem dizer como.

```java
public interface Comparavel {
    int compararCom(Object outro);
}

public class Produto implements Comparavel {
    private double preco;

    @Override
    public int compararCom(Object outro) {
        Produto p = (Produto) outro;
        return Double.compare(this.preco, p.preco);
    }
}
```

**Interface vs classe abstrata:**

- **Interface** — só contrato (métodos sem corpo, por default). Uma classe pode implementar **várias**.
- **Classe abstrata** — pode ter estado e métodos implementados. Uma classe só pode estender **uma**.

**Desde Java 8, interfaces podem ter `default` methods:**

```java
public interface Saudavel {
    String getNome();

    default void cumprimentar() {
        System.out.println("Olá, " + getNome());
    }
}
```

### 9.3 Polimorfismo

Um objeto pode ser tratado como tipo do pai, mas comporta-se como filho.

```java
Animal a = new Cachorro("Rex");
a.comer();  // chama o comer() de Cachorro (dynamic dispatch)
// a.latir();  // ERRO — Animal não tem latir()
```

**Uso prático — lista polimorfa:**

```java
ArrayList<Animal> zoo = new ArrayList<>();
zoo.add(new Cachorro("Rex"));
zoo.add(new Gato("Mimi"));
zoo.add(new Passaro("Piu"));

for (Animal a : zoo) {
    a.comer();  // cada um come do seu jeito
}
```

**`instanceof`** — verifica o tipo real:

```java
for (Animal a : zoo) {
    if (a instanceof Cachorro) {
        Cachorro c = (Cachorro) a;
        c.latir();
    }
}

// Java 16+ — pattern matching
if (a instanceof Cachorro c) {
    c.latir();
}
```

### Erros comuns na Parte 9

- **Esquecer `super()` no construtor** — só é automático se o pai tem construtor sem argumentos
- **Não usar `@Override`** — errar a assinatura e criar método novo em vez de sobrescrever
- **Herdar por conveniência** — herança implica relação "é um". Composição é frequentemente melhor (`Cachorro tem um Nome` em vez de `Cachorro é um Animal`)
- **Classes abstratas enormes** — herança profunda vira problema. Prefira interfaces.

---

## Parte 10 — Streams, Comparable, Lambdas

**Objetivo:** programação funcional em Java — streams, lambdas, expressões regulares.

### 10.1 Streams

Stream é uma **pipeline de processamento** de coleções, no estilo funcional. Introduzido no Java 8.

```java
import java.util.stream.Collectors;

List<Pessoa> pessoas = ...;

// Filtrar adultos, pegar nomes, juntar em lista
List<String> nomesAdultos = pessoas.stream()
    .filter(p -> p.getIdade() >= 18)
    .map(Pessoa::getNome)
    .collect(Collectors.toList());
```

**Operações comuns:**

- **`filter(predicado)`** — mantém elementos que atendem a condição
- **`map(função)`** — transforma cada elemento
- **`sorted()`** — ordena
- **`limit(n)`** — primeiros n
- **`skip(n)`** — pula n
- **`distinct()`** — remove duplicatas
- **`count()`** — conta (terminal)
- **`collect(...)`** — coleta em List/Set/Map (terminal)
- **`forEach(ação)`** — executa para cada (terminal)
- **`reduce(...)`** — reduz a um único valor (terminal)

**Intermediárias** vs **terminais:**

- Intermediárias retornam Stream, são "lazy"
- Terminais consomem o stream e produzem resultado

**Exemplo completo:**

```java
double mediaIdade = pessoas.stream()
    .filter(p -> p.getIdade() >= 18)
    .mapToInt(Pessoa::getIdade)
    .average()
    .orElse(0.0);

// Agrupar por cidade
Map<String, List<Pessoa>> porCidade = pessoas.stream()
    .collect(Collectors.groupingBy(Pessoa::getCidade));
```

### 10.2 Lambdas

Lambda é uma função anônima. Sintaxe compacta para passar comportamento.

```java
// Antes
pessoas.sort(new Comparator<Pessoa>() {
    @Override
    public int compare(Pessoa a, Pessoa b) {
        return a.getNome().compareTo(b.getNome());
    }
});

// Com lambda
pessoas.sort((a, b) -> a.getNome().compareTo(b.getNome()));

// Com method reference
pessoas.sort(Comparator.comparing(Pessoa::getNome));
```

**Sintaxe:**

- `() -> corpo` — sem parâmetros
- `x -> corpo` — um parâmetro
- `(x, y) -> corpo` — múltiplos parâmetros
- `(x) -> { várias linhas; return resultado; }` — corpo em bloco

**Method references** (`::`) são atalhos para lambdas que só chamam um método existente:

- `String::toUpperCase` — `s -> s.toUpperCase()`
- `Pessoa::getNome` — `p -> p.getNome()`
- `System.out::println` — `x -> System.out.println(x)`
- `ArrayList::new` — `() -> new ArrayList<>()`

### 10.3 Comparable

Interface para dar ordem natural a seus objetos.

```java
public class Produto implements Comparable<Produto> {
    private String nome;
    private double preco;

    @Override
    public int compareTo(Produto outro) {
        return Double.compare(this.preco, outro.preco);
    }
}

// Agora você pode ordenar
List<Produto> produtos = ...;
Collections.sort(produtos);  // usa compareTo
```

**Regra do compareTo:**

- Retorna **negativo** se `this < outro`
- Retorna **zero** se `this == outro`
- Retorna **positivo** se `this > outro`

**Comparator** — alternativa externa, útil quando você quer múltiplas ordens:

```java
Comparator<Produto> porNome = Comparator.comparing(Produto::getNome);
Comparator<Produto> porPreco = Comparator.comparing(Produto::getPreco);
Comparator<Produto> porPrecoDesc = porPreco.reversed();
Comparator<Produto> composto = porPreco.thenComparing(porNome);

produtos.sort(porPreco);
```

### 10.4 Outras técnicas

**Expressões regulares:**

```java
String texto = "meu telefone é 11 98765-4321";
if (texto.matches(".*\\d{2} \\d{5}-\\d{4}.*")) {
    System.out.println("Contém telefone");
}

String apenasNumeros = texto.replaceAll("[^0-9]", "");  // só dígitos
```

**Enums com comportamento:**

```java
public enum Status {
    ATIVO("Ativo"),
    INATIVO("Inativo"),
    BLOQUEADO("Bloqueado");

    private final String rotulo;

    Status(String rotulo) {
        this.rotulo = rotulo;
    }

    public String getRotulo() {
        return rotulo;
    }
}
```

**Iterator** — forma manual de percorrer coleção (usado por for-each por baixo):

```java
Iterator<String> it = lista.iterator();
while (it.hasNext()) {
    String item = it.next();
    if (item.startsWith("x")) {
        it.remove();  // forma segura de remover durante iteração
    }
}
```

### Erros comuns na Parte 10

- **Stream consumido 2x** — um stream só pode ter operação terminal uma vez
- **Parallel stream sem pensar** — nem sempre é mais rápido
- **Collector errado** — `toMap` lança exceção em chaves duplicadas
- **Lambda com variável mutável** — só pode capturar "effectively final"
- **Regex complexa sem testar** — teste em [regex101.com](https://regex101.com)

---

## Parte 11 — Diagramas, pacotes, exceções, arquivos

**Objetivo:** organizar código em pacotes, lidar com erros, ler/escrever arquivos.

### 11.1 Diagramas de classe (UML)

Notação visual para representar classes e relacionamentos.

```
┌───────────────┐       ┌───────────────┐
│    Pessoa     │       │    Curso      │
├───────────────┤       ├───────────────┤
│ - nome        │       │ - nome        │
│ - idade       │       │ - creditos    │
├───────────────┤       ├───────────────┤
│ + getNome()   │       │ + getNome()   │
│ + getIdade()  │       │ + getCreditos │
└───────┬───────┘       └───────────────┘
        │                       ▲
        │                       │
        │                       │
┌───────▼───────┐       ┌──────┴───────┐
│    Aluno      │─────▶│   Matricula   │
├───────────────┤  N  N├───────────────┤
│ - matricula   │       │ - data        │
└───────────────┘       │ - nota        │
                        └───────────────┘
```

**Simbologia básica:**

- `-` — private
- `+` — public
- `#` — protected
- **Herança** — seta com triângulo vazio, aponta da filha para pai
- **Composição** — diamante preto (parte de)
- **Agregação** — diamante vazio (usa)
- **Associação** — seta simples (conhece)

Para detalhes, ver [[Arquitetura de Software]] (seção C4 Model).

### 11.2 Pacotes

Pacote agrupa classes relacionadas. Evita conflito de nomes.

```java
package com.medespecialista.modelo;  // primeira linha do arquivo

import java.util.ArrayList;
import com.medespecialista.servico.PessoaService;

public class Pessoa { ... }
```

**Convenção:** `com.empresa.projeto.subpacote` (inverso de domínio).

**Estrutura de arquivos:**

```
src/
  com/
    medespecialista/
      modelo/
        Pessoa.java
        Paciente.java
      servico/
        PessoaService.java
```

### 11.3 Exceções

Exceção é um erro que interrompe execução normal. Você pode **tratar** ou **propagar**.

```java
try {
    int resultado = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Erro: divisão por zero");
}
```

**Estrutura:**

```java
try {
    // código que pode dar erro
} catch (TipoDeExcecao1 e) {
    // tratamento
} catch (TipoDeExcecao2 e) {
    // tratamento
} finally {
    // sempre executa, com erro ou sem
}
```

**Checked vs Unchecked:**

- **Checked** — compilador obriga a tratar (`IOException`). Tipicamente erros recuperáveis.
- **Unchecked** (`RuntimeException`) — não precisa tratar, mas pode. Tipicamente bugs.

**Lançando uma exceção:**

```java
public void sacar(double valor) {
    if (valor <= 0) {
        throw new IllegalArgumentException("Valor deve ser positivo");
    }
    if (valor > saldo) {
        throw new IllegalStateException("Saldo insuficiente");
    }
    saldo -= valor;
}
```

**Criando exceções customizadas:**

```java
public class SaldoInsuficienteException extends RuntimeException {
    public SaldoInsuficienteException(String msg) {
        super(msg);
    }
}
```

### 11.4 Processando arquivos

**Ler arquivo (moderno):**

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

try {
    List<String> linhas = Files.readAllLines(Path.of("dados.txt"));
    for (String linha : linhas) {
        System.out.println(linha);
    }
} catch (IOException e) {
    System.out.println("Erro ao ler: " + e.getMessage());
}
```

**Ler arquivo grande (streaming):**

```java
try (var stream = Files.lines(Path.of("grande.txt"))) {
    stream.filter(linha -> linha.contains("ERROR"))
          .forEach(System.out::println);
}
// try-with-resources fecha o arquivo automaticamente
```

**Escrever arquivo:**

```java
try {
    Files.writeString(Path.of("saida.txt"), "Olá mundo");
    Files.write(Path.of("linhas.txt"), listaDeStrings);
} catch (IOException e) {
    e.printStackTrace();
}
```

**Try-with-resources** — fecha recursos automaticamente:

```java
try (Scanner scanner = new Scanner(new File("dados.txt"))) {
    while (scanner.hasNextLine()) {
        System.out.println(scanner.nextLine());
    }
} catch (FileNotFoundException e) {
    System.out.println("Arquivo não encontrado");
}
// scanner.close() automático
```

### Erros comuns na Parte 11

- **Engolir exceções com `catch (Exception e) {}`** — erros ficam escondidos
- **Não fechar recursos** — use try-with-resources sempre
- **`throws Exception` generalizado** — declare tipos específicos
- **Arquivo em caminho errado** — use caminho absoluto para testar
- **Encoding de arquivo** — especifique charset se não for UTF-8

→ Para deep dive em exceções, ver [[Java Fundamentals]] (seção Exceções).

---

## Parte 12 — Tipos genéricos e estruturas de dados

**Objetivo:** entender `<T>` (genéricos), implementar `ArrayList` e `HashMap` do zero, trabalhar com aleatoriedade e dados multidimensionais.

### 12.1 Parâmetros de tipo (Generics)

`ArrayList<String>` significa "ArrayList de Strings". O `<String>` é um **parâmetro de tipo**. Generics garantem segurança de tipo em compile-time.

```java
ArrayList<String> nomes = new ArrayList<>();
nomes.add("Maria");
// nomes.add(42);  // ERRO — compile-time

String primeiro = nomes.get(0);  // sem cast!
```

**Antes de generics (Java 1.4):**

```java
ArrayList nomes = new ArrayList();
nomes.add("Maria");
nomes.add(42);  // sem type safety
String primeiro = (String) nomes.get(0);  // cast explícito
```

**Criando classe genérica:**

```java
public class Par<K, V> {
    private K chave;
    private V valor;

    public Par(K chave, V valor) {
        this.chave = chave;
        this.valor = valor;
    }

    public K getChave() { return chave; }
    public V getValor() { return valor; }
}

// Uso
Par<String, Integer> idade = new Par<>("Maria", 30);
Par<Integer, String> nome = new Par<>(1, "Um");
```

**Diamond operator `<>`** — infere o tipo em Java 7+:

```java
// Antes
ArrayList<String> lista = new ArrayList<String>();

// Moderno
ArrayList<String> lista = new ArrayList<>();
```

**`var` (Java 10+)** elimina a verbosidade:

```java
var lista = new ArrayList<String>();  // var infere ArrayList<String>
```

### 12.2 Como ArrayList e HashMap funcionam

**ArrayList por dentro:**

```java
public class MeuArrayList<T> {
    private Object[] valores;
    private int tamanho;

    public MeuArrayList() {
        this.valores = new Object[10];
        this.tamanho = 0;
    }

    public void add(T valor) {
        if (tamanho == valores.length) {
            // cresce o array (dobra o tamanho)
            Object[] novo = new Object[valores.length * 2];
            System.arraycopy(valores, 0, novo, 0, valores.length);
            valores = novo;
        }
        valores[tamanho++] = valor;
    }

    @SuppressWarnings("unchecked")
    public T get(int indice) {
        return (T) valores[indice];
    }

    public int size() {
        return tamanho;
    }
}
```

**HashMap por dentro (simplificado):**

```java
public class MeuHashMap<K, V> {
    private ArrayList<Par<K, V>>[] buckets;

    @SuppressWarnings("unchecked")
    public MeuHashMap() {
        this.buckets = new ArrayList[16];
        for (int i = 0; i < 16; i++) {
            buckets[i] = new ArrayList<>();
        }
    }

    private int indiceDoBucket(K chave) {
        return Math.abs(chave.hashCode()) % buckets.length;
    }

    public void put(K chave, V valor) {
        int idx = indiceDoBucket(chave);
        for (Par<K, V> par : buckets[idx]) {
            if (par.getChave().equals(chave)) {
                par.setValor(valor);  // atualiza
                return;
            }
        }
        buckets[idx].add(new Par<>(chave, valor));
    }

    public V get(K chave) {
        int idx = indiceDoBucket(chave);
        for (Par<K, V> par : buckets[idx]) {
            if (par.getChave().equals(chave)) {
                return par.getValor();
            }
        }
        return null;
    }
}
```

**Por isso `equals` e `hashCode` são essenciais** — HashMap usa ambos para localizar entradas.

### 12.3 Aleatoriedade

```java
import java.util.Random;

Random random = new Random();

int numero = random.nextInt(100);       // 0 a 99
int dado = random.nextInt(6) + 1;        // 1 a 6
double decimal = random.nextDouble();    // 0.0 a 1.0
boolean moeda = random.nextBoolean();    // true ou false

// Seed fixa — reprodutível (útil para testes)
Random determinista = new Random(42);
```

**Em Java moderno:**

```java
int n = ThreadLocalRandom.current().nextInt(1, 101);  // 1 a 100 (inclusivo, exclusivo)
```

### 12.4 Dados multidimensionais

Array de arrays — útil para tabelas, matrizes, grades.

```java
int[][] tabuleiro = new int[8][8];  // 8x8

// Inicializar
for (int i = 0; i < 8; i++) {
    for (int j = 0; j < 8; j++) {
        tabuleiro[i][j] = 0;
    }
}

// Literal
int[][] matriz = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

matriz[1][2] = 60;  // linha 1, coluna 2 → 6 vira 60

// Arrays "jagged" — linhas de tamanhos diferentes
int[][] irregular = new int[3][];
irregular[0] = new int[]{1, 2};
irregular[1] = new int[]{3, 4, 5};
irregular[2] = new int[]{6};
```

### Erros comuns na Parte 12

- **Raw types** — `ArrayList` sem `<T>` compila mas perde type safety
- **Array de genéricos** — `new T[10]` não funciona (use `Object[]` com cast)
- **Confundir `length` (array) com `size()` (lista)** — `array.length`, `lista.size()`
- **Aleatoriedade com range errado** — `nextInt(6)` é 0 a 5, não 1 a 6

---

## Parte 13 — Interfaces gráficas com JavaFX

**Objetivo:** criar aplicações com interface gráfica usando JavaFX.

> **Nota:** JavaFX é menos usado em aplicações empresariais modernas (que tendem a ser web-based), mas é ótimo para aprender conceitos de GUI. Para apps desktop profissionais modernas, considere alternativas como Electron (JS) ou Compose for Desktop (Kotlin).

### 13.1 Interfaces gráficas

GUI básica em JavaFX:

```java
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

public class HelloWorld extends Application {

    @Override
    public void start(Stage stage) {
        Label label = new Label("Olá, JavaFX!");
        StackPane root = new StackPane(label);
        Scene scene = new Scene(root, 300, 200);

        stage.setTitle("Minha App");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

**Conceitos:**

- **`Application`** — classe base da aplicação
- **`Stage`** — a janela
- **`Scene`** — o conteúdo da janela (uma cena por vez)
- **Nodes** — qualquer componente (Label, Button, TextField, Panel, ...)

### 13.2 Componentes e layout

**Componentes comuns:**

- `Label` — texto não editável
- `Button` — botão clicável
- `TextField` — entrada de texto
- `TextArea` — texto multi-linha
- `CheckBox` — caixa de seleção
- `RadioButton` — opções exclusivas
- `ComboBox` — dropdown
- `ListView` — lista rolável

**Layouts:**

- `VBox` — empilha vertical
- `HBox` — empilha horizontal
- `StackPane` — sobreposto
- `BorderPane` — top/bottom/left/right/center
- `GridPane` — grade de linhas e colunas
- `FlowPane` — flui como texto

```java
VBox root = new VBox(10);  // espaçamento de 10
root.getChildren().addAll(
    new Label("Nome:"),
    new TextField(),
    new Button("OK")
);
```

### 13.3 Tratamento de eventos

Ação em resposta a clique, tecla, etc.

```java
Button botao = new Button("Clique aqui");
botao.setOnAction(event -> {
    System.out.println("Clicado!");
});

// Input de teclado
TextField campo = new TextField();
campo.setOnAction(event -> {
    System.out.println("Enter pressionado. Texto: " + campo.getText());
});
```

### 13.4 Parâmetros de lançamento

Passar argumentos ao iniciar:

```java
public static void main(String[] args) {
    launch(args);
}

@Override
public void init() {
    Parameters params = getParameters();
    List<String> raw = params.getRaw();
    // acessa argumentos da linha de comando
}
```

### 13.5 Múltiplas telas

Trocar cenas na mesma janela:

```java
Scene tela1 = criarTela1();
Scene tela2 = criarTela2();

Button btnIrParaTela2 = new Button("Ir para tela 2");
btnIrParaTela2.setOnAction(e -> stage.setScene(tela2));
```

### Erros comuns na Parte 13

- **Esquecer `launch(args)`** no main
- **Modificar UI fora da thread JavaFX** — use `Platform.runLater()`
- **Layout confuso** — use `SceneBuilder` ou FXML para GUIs complexas
- **Memory leaks com eventos** — removar listeners quando não precisar mais

---

## Parte 14 — Visualização, multimídia e projeto final

**Objetivo:** gráficos, áudio, projeto Asteroids, Maven e bibliotecas externas.

### 14.1 Visualização de dados

JavaFX tem componentes de gráfico built-in:

**LineChart:**

```java
import javafx.scene.chart.*;

NumberAxis xAxis = new NumberAxis();
NumberAxis yAxis = new NumberAxis();
LineChart<Number, Number> chart = new LineChart<>(xAxis, yAxis);

XYChart.Series<Number, Number> serie = new XYChart.Series<>();
serie.setName("Vendas 2026");
serie.getData().add(new XYChart.Data<>(1, 100));
serie.getData().add(new XYChart.Data<>(2, 150));
serie.getData().add(new XYChart.Data<>(3, 120));

chart.getData().add(serie);
```

**BarChart, PieChart, ScatterChart** — outros tipos disponíveis.

### 14.2 Multimídia em programas

**Gráficos (Canvas):**

```java
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

Canvas canvas = new Canvas(400, 300);
GraphicsContext gc = canvas.getGraphicsContext2D();

gc.setFill(Color.BLUE);
gc.fillRect(50, 50, 100, 100);

gc.setStroke(Color.RED);
gc.strokeOval(200, 50, 80, 80);

gc.fillText("Texto", 100, 200);
```

**Imagens:**

```java
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;

Image imagem = new Image("file:logo.png");
ImageView view = new ImageView(imagem);
```

**Áudio:**

```java
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;

Media som = new Media(new File("som.mp3").toURI().toString());
MediaPlayer player = new MediaPlayer(som);
player.play();
```

### 14.3 Projeto Asteroids

O curso guia você a construir o clássico jogo Asteroids. Conceitos aplicados:

- **Game loop** — loop infinito que atualiza e redesenha
- **Animação** — `AnimationTimer` do JavaFX
- **Colisão** — detectar quando objetos se tocam
- **Input** — ler teclas do jogador
- **Estado do jogo** — posição, velocidade, pontuação

Esqueleto:

```java
public class AsteroidsGame extends Application {
    private List<Ship> ships;
    private List<Asteroid> asteroids;

    @Override
    public void start(Stage stage) {
        Canvas canvas = new Canvas(800, 600);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        new AnimationTimer() {
            @Override
            public void handle(long now) {
                update();
                render(gc);
            }
        }.start();

        // ... setup de cena
    }

    private void update() { /* atualiza posições */ }
    private void render(GraphicsContext gc) { /* desenha */ }
}
```

### 14.4 Maven e bibliotecas externas

**Maven** é a ferramenta padrão para gerenciar dependências em Java. Define projeto em `pom.xml`:

```xml
<?xml version="1.0"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.exemplo</groupId>
    <artifactId>meu-app</artifactId>
    <version>1.0.0</version>

    <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
    </properties>

    <dependencies>
        <!-- Biblioteca externa -->
        <dependency>
            <groupId>com.google.code.gson</groupId>
            <artifactId>gson</artifactId>
            <version>2.10.1</version>
        </dependency>

        <!-- JUnit para testes -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

**Comandos Maven:**

```bash
mvn compile          # compilar
mvn test             # rodar testes
mvn package          # gerar JAR
mvn clean            # limpar target/
mvn install          # instalar no repositório local
```

**Adicionando dependência:**

1. Achar no [Maven Central](https://search.maven.org/) ou [mvnrepository.com](https://mvnrepository.com)
2. Copiar o bloco `<dependency>` para o `pom.xml`
3. Rodar `mvn install` ou deixar IDE resolver automaticamente

**Alternativa:** Gradle (`build.gradle`) é popular em projetos mais novos, com sintaxe mais concisa.

### Erros comuns na Parte 14

- **Game loop sem sleep** — CPU 100%
- **Animação fora da thread JavaFX** — crash
- **Dependency hell** — versões incompatíveis de libs
- **Não especificar versão no `pom.xml`** — build pode quebrar

---

# Próximos passos depois do MOOC

Completado o Helsinki MOOC, você tem fundamentos sólidos. Próximos passos:

### 1. Aprofundar a linguagem

- [[Java Fundamentals]] — JVM, Collections avançadas, Streams profundos, features modernas
- [[Java Concurrency]] — Memory Model, CompletableFuture, Virtual Threads
- [[Certificação Java OCP]] — estruturar estudo com objetivo de certificação

### 2. Orientação a objetos profunda

- [[Orientação a Objetos]] — princípios, encapsulamento, polimorfismo
- [[Design Patterns]] — padrões clássicos (Factory, Observer, Strategy, etc.)
- [[Arquitetura de Software]] — SOLID, DDD, Clean Architecture

### 3. Frameworks modernos

- [[Spring Boot]] — framework dominante para backend Java
- **Spring Framework** — core, AOP, DI, profiles, beans
- **Spring Data JPA** — persistência
- **Spring Security** — autenticação/autorização

### 4. Testes avançados

- [[Testes em Java]] — JUnit 5, Mockito, AssertJ, Testcontainers
- TDD (Test-Driven Development)
- Mutation testing

### 5. Banco de dados e persistência

- [[Banco de dados]] — SQL, modelagem, índices, transações
- JPA, Hibernate
- JDBC puro (quando você precisa de controle)

### 6. Arquitetura distribuída

- [[System Design]] — escalabilidade, caching, message queues
- [[API Design]] — REST, GraphQL, gRPC
- [[Mensageria]] — Kafka, RabbitMQ
- [[03-Dominios/Java/Backend/Kafka/Kafka]] — event streaming

### 7. Devops e produção

- **Docker** — containers
- **Kubernetes** — orquestração
- CI/CD com GitHub Actions
- Monitoramento (Prometheus, Grafana)

### 8. Prática

- **Projetos próprios** — construa algo que você usaria
- **Open source** — contribua em projetos Java no GitHub
- **LeetCode/HackerRank** — algoritmos para entrevistas
- **System design challenges** — arquitetura para entrevistas senior

---

## Dicas gerais para aprendizagem

### Como estudar Java de forma efetiva

1. **Digite o código, não copie.** O músculo cognitivo forma errando e digitando.
2. **Quebre coisas.** Mude o código dos exemplos. Veja o que acontece quando você tira o `static`, o `final`, o `return`. Bugs ensinam.
3. **Leia stacktraces inteiras.** A mensagem de erro geralmente diz exatamente onde está o problema.
4. **Use o debugger.** Breakpoints e step-through são mil vezes melhores que `System.out.println`.
5. **Faça projetinhos.** Construa uma calculadora, agenda de contatos, jogo da velha. Projetos consolidam conceitos.
6. **Não pule fundamentos.** Resistir a aprender OOP direito vai te morder na idade senior.
7. **Comunidade.** Stack Overflow, Reddit r/learnjava, Discord servers. Pergunte quando travar.
8. **Descanse.** Cérebro consolida durante o sono. 4h focadas valem mais que 12h cansadas.

### Ferramentas essenciais

- **IntelliJ IDEA Community** (gratuito) — melhor IDE para Java
- **VS Code + Java Extension Pack** — alternativa leve
- **SDKMAN** — gerenciar versões de Java (`sdk install java 21.0.2-tem`)
- **Maven ou Gradle** — build tool
- **Git** — controle de versão (aprenda cedo)
- **JShell** — REPL do Java, teste snippets rapidamente

### Mitos e verdades

- ❌ "Java é lento" — Java é muito rápido, comparável a C++ para a maioria dos casos
- ❌ "Java é verboso" — Java moderno (17+) é muito mais conciso
- ❌ "Java é para dinossauros" — Java é uma das linguagens mais usadas no mercado enterprise
- ✅ "Java é complexo" — tem muitos detalhes, mas isso traz poder e flexibilidade
- ✅ "Java tem ótimo mercado" — especialmente em grandes empresas

---

## Recursos complementares ao MOOC

### Livros para iniciantes

- **Head First Java** — Kathy Sierra, Bert Bates (aprendizado visual, divertido)
- **Java: The Complete Reference** — Herbert Schildt (referência completa)
- **Modern Java in Action** — Raoul-Gabriel Urma (features funcionais)

### Livros intermediário/avançado

- **Effective Java** — Joshua Bloch (78 items essenciais)
- **Java Concurrency in Practice** — Brian Goetz (concorrência)
- **Clean Code** — Robert Martin (qualidade de código, exemplos em Java)

### Cursos complementares

- [Helsinki MOOC (este curso)](https://java-programming.mooc.fi) — fundamentos
- [Nélio Alves — Java COMPLETO (Udemy, pt-BR)](https://www.udemy.com/course/java-curso-completo) — em português
- [Maratona Java Virado no Jiraya (YouTube, pt-BR)](https://www.youtube.com/playlist?list=PL62G310vn6nFIsOCC0H-C2infYgwm8SWW) — gratuito
- [Baeldung](https://www.baeldung.com/start-here) — tutoriais de Spring e Java

### Prática

- [Hyperskill (JetBrains)](https://hyperskill.org) — exercícios interativos
- [Exercism Java track](https://exercism.org/tracks/java) — exercícios com mentoria
- [Codingbat Java](https://codingbat.com/java) — problemas pequenos e objetivos
- [HackerRank Java](https://www.hackerrank.com/domains/java) — desafios

---

## Veja também

- [[Java Fundamentals]] — próximo passo depois do MOOC
- [[Java Concurrency]] — concorrência avançada
- [[Testes em Java]] — testes profundos com JUnit 5, Mockito
- [[Certificação Java OCP]] — certificação Java SE 21
- [[Spring Boot]] — framework web dominante
- [[Orientação a Objetos]] — aprofundar OOP
- [[Design Patterns]] — padrões clássicos
- [[Banco de dados]] — persistência
- [[Senda Java]] — plano de aprendizado completo
- [[What should you do to stand out as a Java-Spring Boot Developer]]
