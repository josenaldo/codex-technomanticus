---
title: "Annotations"
created: 2026-06-02
updated: 2026-06-07
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - linguagem
  - adepto
  - annotations
  - metaprogramacao
aliases:
  - Annotations
  - Anotações
---

# Annotations

> [!abstract] TL;DR
> **Annotations** são metadados sobre código — marcadores que o compilador, ferramentas de build ou o runtime lêem para tomar decisões sem alterar o fluxo lógico do programa. Java traz um conjunto de **annotations built-in** (`@Override`, `@Deprecated`, `@FunctionalInterface`, `@SuppressWarnings`, `@SafeVarargs`) e permite criar annotations customizadas com `@interface`. O comportamento de cada annotation em relação ao ciclo de vida é definido pelas **meta-annotations**: `@Retention` controla se a annotation sobrevive até o runtime (RUNTIME), fica apenas no bytecode (CLASS) ou é descartada após a compilação (SOURCE); `@Target` restringe onde ela pode ser aplicada; `@Documented`, `@Inherited` e `@Repeatable` complementam. A **retention policy** é a escolha mais crítica: annotations com SOURCE (Lombok) são invisíveis em runtime; com RUNTIME são legíveis via reflection — base de Spring (`@Component`, `@Autowired`) e Jakarta EE (`@Entity`, `@Column`).

## O que é

Uma **annotation** é metadado aplicado a um elemento do código-fonte — classe, método, campo, parâmetro, variável local, ou até o próprio pacote. Diferente de um comentário, uma annotation é estruturada, tipada e pode ser processada automaticamente por ferramentas.

```java
// Comentário: informação apenas para humanos, invisível para ferramentas
// Annotation: metadado estruturado, processável por compilador e frameworks
@Override
public String toString() {
    return "Exemplo";
}
```

As três categorias de uso, segundo a especificação Oracle:

1. **Informação para o compilador** — detectar erros e suprimir warnings (`@Override`, `@SuppressWarnings`).
2. **Processamento em compile-time ou build-time** — gerar código, XML ou outras saídas a partir do código-fonte (Lombok, MapStruct, gRPC codegen).
3. **Processamento em runtime** — examinar metadados de classes e membros via reflection (Spring, Jakarta EE, JUnit).

O programa principal nunca "sente" a annotation diretamente — quem a processa é sempre uma ferramenta externa (compilador, annotation processor, framework via reflection).

## Como funciona

### Annotations built-in

Java define algumas annotations na própria linguagem (`java.lang`), com comportamento implementado no compilador:

**`@Override`** — declara que o método sobrescreve um método da superclasse ou de uma interface. Se a assinatura não bater com nenhum método herdado, o compilador emite um erro de compilação, protegendo contra typos silenciosos.

```java
public class Retangulo extends Forma {
    @Override
    public double calcularArea() {   // compilador verifica que Forma tem este método
        return largura * altura;
    }
}
```

**`@Deprecated`** — sinaliza que um elemento está obsoleto e não deveria ser usado em código novo. O compilador emite um warning quando o elemento marcado é referenciado. Por convenção, deve ser acompanhado de uma tag Javadoc `@deprecated` (com `d` minúsculo) explicando o motivo e a alternativa.

```java
/**
 * @deprecated Use {@link #calcular(double, double)} com dois parâmetros.
 */
@Deprecated
public double calcular(double valor) {
    return calcular(valor, 0.0);
}
```

**`@FunctionalInterface`** — garante que a interface tem exatamente um método abstrato (contrato de interface funcional exigido por lambdas e method references). Se a interface violar esse contrato, o compilador emite erro.

```java
@FunctionalInterface
public interface Transformador<T, R> {
    R transformar(T entrada);
    // Adicionar outro método abstrato aqui causaria erro de compilação
}
```

**`@SuppressWarnings`** — instrui o compilador a suprimir categorias específicas de warnings. Categorias comuns: `"unchecked"` (operações com generics não verificadas), `"deprecation"` (uso de elementos `@Deprecated`), `"rawtypes"` (uso de tipos raw).

```java
@SuppressWarnings("unchecked")
public <T> List<T> converterLista(List<?> lista) {
    return (List<T>) lista;  // cast unchecked — warning suprimido intencionalmente
}
```

**`@SafeVarargs`** — aplicada a métodos ou construtores com parâmetros varargs de tipo genérico, declara que o corpo do método não realiza operações potencialmente inseguras no array de varargs. Suprime o warning `"unchecked"` relacionado.

```java
@SafeVarargs
public static <T> List<T> combinar(List<T>... listas) {
    List<T> resultado = new ArrayList<>();
    for (List<T> lista : listas) {
        resultado.addAll(lista);
    }
    return resultado;
}
```

---

### Meta-annotations

Meta-annotations são annotations aplicadas a outras annotations — descrevem o comportamento e as restrições da annotation que decoram. Estão em `java.lang.annotation`.

**`@Retention`** — define até quando a annotation é preservada. Recebe um valor de `RetentionPolicy`:

```java
@Retention(RetentionPolicy.RUNTIME)
public @interface MinhaAnnotation { }
```

**`@Target`** — restringe em que elementos do código a annotation pode ser aplicada. Recebe um ou mais valores de `ElementType`:

```java
@Target({ElementType.FIELD, ElementType.METHOD})
public @interface Validar { }
```

Valores comuns de `ElementType`: `TYPE` (classe/interface/enum), `FIELD`, `METHOD`, `PARAMETER`, `CONSTRUCTOR`, `LOCAL_VARIABLE`, `ANNOTATION_TYPE`, `PACKAGE`.

**`@Documented`** — indica que a annotation deve aparecer na documentação Javadoc dos elementos que a usam. Sem `@Documented`, ferramentas Javadoc ignoram a annotation.

```java
@Documented
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface PublicApi { }
```

**`@Inherited`** — se a annotation estiver aplicada a uma classe, subclasses herdam automaticamente essa annotation. Só funciona para annotations em classes (não em métodos, campos ou interfaces).

```java
@Inherited
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Auditavel { }

@Auditavel
public class BaseServico { }

// SubServico herda @Auditavel automaticamente
public class SubServico extends BaseServico { }
```

**`@Repeatable`** — permite que a mesma annotation seja aplicada múltiplas vezes no mesmo elemento. Exige uma annotation "container" que agrupa as repetições em array.

```java
@Repeatable(Agendamentos.class)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Agendamento {
    String cron();
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Agendamentos {
    Agendamento[] value();
}

// Uso com repetição
@Agendamento(cron = "0 0 8 * * MON-FRI")
@Agendamento(cron = "0 0 18 * * MON-FRI")
public void sincronizar() { }
```

---

### Retention policies em detalhe

A escolha da retention policy é a decisão mais importante ao criar uma annotation customizada — ela determina em que momento do ciclo de vida a annotation está disponível.

```text
Código-fonte (.java)
       │
       ▼
  javac (compilação)
       │
       ├── SOURCE: annotation descartada aqui
       │
       ▼
  Bytecode (.class)
       │
       ├── CLASS: annotation presente no .class, mas...
       │
       ▼
  JVM (classloading em runtime)
       │
       ├── CLASS: annotation NÃO carregada na JVM (não visível via reflection)
       ├── RUNTIME: annotation CARREGADA na JVM (visível via reflection)
       │
       ▼
  Execução
```

**SOURCE** — a annotation é descartada pelo compilador após a fase de processamento. Não aparece no bytecode. Usada exclusivamente por ferramentas que operam sobre o código-fonte. Exemplo clássico: **Lombok** (`@Getter`, `@Setter`, `@Builder`) — o annotation processor do Lombok gera código-fonte durante a compilação e a annotation em si não precisa existir em runtime. `@Override` e `@SuppressWarnings` também têm retention SOURCE.

**CLASS** — a annotation é gravada no bytecode pelo compilador, mas a JVM não a carrega ao executar o programa. Não é acessível via reflection. É a **política default** quando `@Retention` é omitida. Usada principalmente por ferramentas de análise de bytecode (profilers, instrumentação de bytecode como AspectJ em certos modos, ferramentas de análise estática).

**RUNTIME** — a annotation é gravada no bytecode e a JVM a mantém em memória durante a execução. É a única política que permite acesso via reflection (`Class.getAnnotations()`, `Method.getAnnotation()`, etc.). Frameworks como Spring e Jakarta EE dependem exclusivamente de RUNTIME para ler annotations em runtime.

```java
// Resumo prático: quando usar cada política
// SOURCE   → ferramenta só precisa do código-fonte  (Lombok, @Override, @SuppressWarnings)
// CLASS    → ferramenta só precisa do bytecode, não do runtime  (raramente escolhido intencionalmente)
// RUNTIME  → framework/biblioteca vai ler via reflection em runtime  (Spring, Jakarta, JUnit)
```

---

### Annotations customizadas

Annotations são declaradas com a sintaxe `@interface`, que é uma forma especial de interface:

```java
import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
public @interface NaoVazio {
    String mensagem() default "O campo não pode ser vazio";
    String[] grupos() default {};
}
```

**Regras de declaração:**

- Elementos são declarados como métodos sem parâmetros (sintaxe `tipo nomeElemento()`).
- O tipo de retorno deve ser: primitivo, `String`, `Class`, enum, annotation, ou array de qualquer um desses.
- Elementos podem ter `default` — elementos sem default são obrigatórios na utilização.
- Não pode haver herança entre annotations (annotations não podem estender outras annotations).

**Single-value annotation** — quando a annotation tem apenas um elemento chamado `value`, o nome pode ser omitido na utilização:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Timeout {
    long value();   // único elemento chamado "value"
}

// Uso: @Timeout(500) em vez de @Timeout(value = 500)
@Timeout(500)
public void operacaoLenta() { }
```

**Annotation sem elementos (marker annotation)** — serve apenas como marcador, sem dados:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Imutavel { }

@Imutavel
public final class Ponto {
    private final double x, y;
    // ...
}
```

---

### Annotation processing (visão geral)

Há duas formas principais de processar annotations, em momentos distintos do ciclo de vida:

**Annotation Processing Tool (APT) — compile-time:** o compilador invoca annotation processors registrados via `META-INF/services/javax.annotation.processing.Processor`. O processor recebe os elementos anotados e pode inspecionar a AST (Abstract Syntax Tree), gerar novos arquivos `.java` ou `.class`, ou emitir erros e warnings de compilação. Exige apenas `RetentionPolicy.SOURCE` ou `CLASS`. Exemplos: Lombok, MapStruct, Dagger, gRPC codegen.

**Reflection — runtime:** depois que a JVM carrega as classes, qualquer código pode usar a API de reflection (`java.lang.reflect`) para ler annotations com `RetentionPolicy.RUNTIME`. É o mecanismo usado por frameworks em produção. Exemplo: Spring lê `@Autowired`, `@Component`, `@Transactional` em runtime para construir o application context e aplicar proxies.

A distinção fundamental: APT é mais eficiente (custo zero em runtime, erros detectados em compilação), mas só pode inspecionar estrutura estática; reflection é dinâmica e flexível, mas tem custo em runtime e só funciona com RUNTIME retention.

---

### Papel no Spring / Jakarta EE

Spring e Jakarta EE são construídos sobre annotations com `RetentionPolicy.RUNTIME` + reflection. Alguns exemplos centrais:

```java
// Spring — stereotype annotations (component scanning)
@Component          // registra o bean no ApplicationContext
@Service            // @Component especializado: lógica de negócio
@Repository         // @Component especializado: acesso a dados
@Controller         // @Component especializado: MVC controller
@RestController     // @Controller + @ResponseBody

// Spring — injeção de dependências
@Autowired          // injeta bean por tipo
@Qualifier("nome")  // desambiguação quando há múltiplos beans do mesmo tipo
@Value("${prop}")   // injeta propriedades de configuração

// Jakarta EE — persistência (JPA)
@Entity             // mapeia classe para tabela no banco
@Table(name = "pacientes")
@Column(name = "nome_completo", nullable = false)
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
```

Todas essas annotations têm `@Retention(RUNTIME)` — o container scanneia o classpath em startup, lê as annotations via reflection, e constrói o grafo de dependências e os proxies. Este é o ponto de conexão com o galho [[03-Dominios/Java/Jakarta EE/index|Jakarta EE]] (CDI, JPA e Bean Validation são specs construídas sobre annotations RUNTIME) e com o Galho 8 (Spring, planejado).

## Na prática

O cenário a seguir é hipotético — um validador simples de campos de formulário usando annotation customizada com `@Retention(RUNTIME)` lida via reflection:

```java
import java.lang.annotation.*;
import java.lang.reflect.Field;

// 1. Declarar a annotation customizada
@Retention(RetentionPolicy.RUNTIME)      // precisa ser RUNTIME para ler via reflection
@Target(ElementType.FIELD)              // aplicável apenas a campos
@Documented
public @interface Obrigatorio {
    String mensagem() default "Campo obrigatório não pode ser nulo ou vazio";
}

// 2. Usar a annotation em uma classe de domínio
public class FormularioCadastro {

    @Obrigatorio
    private String nome;

    @Obrigatorio(mensagem = "E-mail é obrigatório para envio de confirmação")
    private String email;

    private String telefone;   // opcional — sem @Obrigatorio

    // construtor, getters...
    public FormularioCadastro(String nome, String email, String telefone) {
        this.nome = nome;
        this.email = email;
        this.telefone = telefone;
    }
}

// 3. Ler a annotation via reflection e validar
public class Validador {

    public static List<String> validar(Object objeto) throws IllegalAccessException {
        List<String> erros = new ArrayList<>();
        Class<?> classe = objeto.getClass();

        for (Field campo : classe.getDeclaredFields()) {
            if (campo.isAnnotationPresent(Obrigatorio.class)) {
                campo.setAccessible(true);
                Object valor = campo.get(objeto);

                boolean vazio = valor == null
                    || (valor instanceof String s && s.isBlank());

                if (vazio) {
                    Obrigatorio annotation = campo.getAnnotation(Obrigatorio.class);
                    erros.add(campo.getName() + ": " + annotation.mensagem());
                }
            }
        }
        return erros;
    }
}

// 4. Uso
FormularioCadastro form = new FormularioCadastro(null, "joao@email.com", null);
List<String> erros = Validador.validar(form);
// erros → ["nome: Campo obrigatório não pode ser nulo ou vazio"]
```

**Pontos chave do exemplo:**

- `@Retention(RUNTIME)` é obrigatório — sem ele, `campo.isAnnotationPresent(Obrigatorio.class)` retorna sempre `false`.
- `campo.setAccessible(true)` é necessário para acessar campos `private` via reflection.
- `campo.getAnnotation(Obrigatorio.class)` retorna a instância da annotation com os valores declarados, incluindo o `default`.

Na prática, frameworks como Bean Validation (Jakarta) fazem exatamente isso em escala — `@NotNull`, `@NotBlank`, `@Size` são annotations com RUNTIME retention lidas por um validador via reflection.

## Armadilhas

### (1) Retention errada — annotation invisível em runtime

**O problema:** declarar uma annotation customizada sem `@Retention`, ou com `RetentionPolicy.SOURCE` / `CLASS`, quando a intenção é lê-la via reflection em runtime. Sem `RUNTIME`, `isAnnotationPresent()` e `getAnnotation()` retornam `false`/`null` mesmo que a annotation esteja presente no código-fonte — sem nenhum erro de compilação.

```java
// RUIM — sem @Retention, o default é CLASS
// annotation presente no .class mas NÃO carregada pela JVM
public @interface Auditavel { }

// No código de auditoria:
if (metodo.isAnnotationPresent(Auditavel.class)) {
    // NUNCA entra aqui — annotation não está disponível em runtime!
    registrarAuditoria(metodo);
}
```

```java
// FIX — adicionar @Retention(RUNTIME) explicitamente
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Auditavel { }

// Agora isAnnotationPresent() funciona corretamente
if (metodo.isAnnotationPresent(Auditavel.class)) {
    registrarAuditoria(metodo);  // executa como esperado
}
```

**Regra prática:** toda annotation que precisa ser lida em runtime — por framework, por código de validação, por proxies — deve ter `@Retention(RetentionPolicy.RUNTIME)`. Se esquecer, a falha é silenciosa: o código compila, o teste de smoke passa, mas o comportamento esperado nunca acontece.

---

### (2) Esquecer `@Override` — typo na assinatura vira overload silencioso

**O problema:** ao sobrescrever um método sem usar `@Override`, um typo no nome ou uma diferença de assinatura faz o compilador criar um **novo método** (overload) em vez de sobrescrever o existente. O método da superclasse continua sendo chamado pelo polimorfismo — o novo método é um "fantasma" nunca invocado pelo dispatch normal.

```java
public class CacheServico extends BaseServico {

    // Intenção: sobrescrever invalidarCache() do BaseServico
    // Problema: typo — "invalidarCashe" com 's' ao invés de 'c'
    // Sem @Override, compila sem erro!
    public void invalidarCashe() {   // overload acidental, não override
        super.invalidarCache();
        log.info("Cache invalidado");
    }
}

// Em runtime:
CacheServico servico = new CacheServico();
servico.invalidarCache();   // chama BaseServico.invalidarCache() — o novo método NUNCA é chamado
```

```java
// FIX — @Override expõe o typo em tempo de compilação
public class CacheServico extends BaseServico {

    @Override
    public void invalidarCashe() {   // ERRO DE COMPILAÇÃO: não existe método com esse nome na superclasse
        // compilador aponta o problema imediatamente
    }

    @Override
    public void invalidarCache() {   // correto — compilador confirma que o override é válido
        super.invalidarCache();
        log.info("Cache invalidado");
    }
}
```

**Regra prática:** use `@Override` em todo método que pretende sobrescrever — sem exceção. É custo zero e elimina uma categoria inteira de bugs sutis que só aparecem em runtime.

---

### (3) `@Target` ausente ou errado — annotation aplicável em lugar não-intencionado

**O problema:** sem `@Target`, uma annotation pode ser aplicada a qualquer elemento do código (classe, método, campo, parâmetro, etc.). Se a lógica de processamento da annotation assume que só será encontrada em campos, mas alguém a aplica em um método, o comportamento é inesperado — sem nenhum erro de compilação avisando que o uso está errado.

```java
// RUIM — sem @Target, aplicável em qualquer lugar
@Retention(RetentionPolicy.RUNTIME)
public @interface SensitiveDados { }

// O código de mascaramento espera encontrar @SensitiveDados em FIELDS
// Mas alguém aplica no método inteiro por engano — sem erro de compilação
@SensitiveDados         // aplicado ao método — intenção era nos campos
public class RelatorioDTO {
    private String cpf;
    private String senha;
}
```

```java
// FIX — declarar @Target explicitamente para restringir o uso intencionado
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)      // só pode ser aplicada em campos
public @interface SensitiveDados { }

// Agora aplicar @SensitiveDados em um método gera ERRO DE COMPILAÇÃO
// "Annotation type not applicable to this kind of declaration"

public class RelatorioDTO {
    @SensitiveDados
    private String cpf;     // correto — campo

    @SensitiveDados
    private String senha;   // correto — campo

    @SensitiveDados         // ERRO DE COMPILAÇÃO — não é um campo
    public String getCpf() { return cpf; }
}
```

**Regra prática:** sempre declare `@Target` explicitamente. Define contrato de uso, habilita detecção de erro em compilação, e documenta a intenção da annotation.

## Em entrevista

### Frase pronta (inglês)

> "The most critical decision when creating a custom annotation is choosing the right retention policy: SOURCE means the annotation is discarded after compilation and is only useful for compile-time tools like Lombok; CLASS means it ends up in the bytecode but is not loaded by the JVM, so it is invisible to reflection; RUNTIME is the only policy that allows frameworks like Spring to read the annotation via reflection when building the application context or applying proxies."

> "When a framework like Spring reads `@Component` or `@Autowired`, it uses `Class.getDeclaredFields()` and `Method.getAnnotation()` at startup — this only works because those annotations carry `@Retention(RetentionPolicy.RUNTIME)`; if you create a custom annotation and forget to set RUNTIME retention, `isAnnotationPresent()` silently returns false and the feature never activates, with no compile-time error to warn you."

> "The practical caveat with annotation-based frameworks is that the contract is implicit: a missing annotation or the wrong retention policy produces a silent failure — the code compiles, the tests may pass, but the expected behavior simply does not happen at runtime; this is why explicit `@Target` declarations and always using `@Override` on every override are defensive practices that pay off across large codebases."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| anotação / annotation | annotation |
| meta-anotação | meta-annotation |
| política de retenção | retention policy |
| processamento de annotations | annotation processing |
| ferramenta de processamento | annotation processor / APT |
| reflexão / introspecção | reflection |
| sobrescrita acidental de overload | accidental overload (instead of override) |
| annotation de marcador | marker annotation |
| elemento da annotation | annotation element |
| annotation container | container annotation |
| interface funcional | functional interface |

## Veja também

- [[07 - Herança e polimorfismo]]
- [[08 - Interfaces e classes abstratas]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [Annotations — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/annotations/)
- [Predefined Annotation Types — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/annotations/predefined.html)
- [Declaring an Annotation Type — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/annotations/declaring.html)
- [RetentionPolicy — Java SE 8 API (Oracle)](https://docs.oracle.com/javase/8/docs/api/java/lang/annotation/RetentionPolicy.html)
- [java.lang.annotation — Java SE 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/annotation/package-summary.html)
