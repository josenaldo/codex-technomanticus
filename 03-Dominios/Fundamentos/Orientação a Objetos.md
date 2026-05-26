---
title: "Orientação a Objetos"
created: 2026-04-01
updated: 2026-04-09
type: concept
status: evergreen
tags:
  - fundamentos
  - entrevista
publish: false
---

# Orientação a Objetos

Paradigma que organiza software em objetos que encapsulam **estado** e **comportamento** e colaboram através de mensagens (chamadas de métodos). Em entrevistas de senior, o diferencial não é recitar os quatro pilares — é demonstrar **quando aplicar**, **quando não aplicar**, e reconhecer os anti-patterns mais comuns.

## O que é

Orientação a Objetos é um paradigma onde o software é modelado como uma coleção de objetos que representam conceitos do domínio. Cada objeto tem:

- **Estado** — dados internos (atributos)
- **Comportamento** — operações que atuam sobre o estado (métodos)
- **Identidade** — um objeto é distinto mesmo que outro tenha o mesmo estado

A promessa original da OOP (Alan Kay, Smalltalk) era construir sistemas por **mensagens entre objetos autônomos**. A interpretação mainstream (Java, C++) acabou focando em classes e herança — o que trouxe problemas que a comunidade vem corrigindo com DDD, composição e programação funcional pragmática.

> **Visão de Alan Kay:** "OOP to me means only messaging, local retention and protection and hiding of state-process, and extreme late-binding of all things." Ou seja: encapsulamento extremo e troca de mensagens. Herança é acidente histórico, não essência.

---

## Os 4 pilares

### 1. Encapsulamento

Esconder o estado interno e expor apenas uma interface pública bem definida. Quem usa o objeto **não sabe** (e não deveria depender) de como ele armazena ou processa internamente.

**Por que importa:** permite mudar a implementação interna sem quebrar clientes. É a única coisa que torna refatoração segura em larga escala.

```java
public class Conta {
    private BigDecimal saldo;

    public void sacar(BigDecimal valor) {
        if (valor.compareTo(saldo) > 0) {
            throw new SaldoInsuficienteException();
        }
        saldo = saldo.subtract(valor);
    }

    public BigDecimal getSaldo() {
        return saldo;
    }
}
```

**Anti-padrão clássico:** expor tudo via getters/setters públicos. Isso **não é encapsulamento** — é encapsulamento falso. Se qualquer um pode fazer `conta.setSaldo(novoValor)`, você não tem invariantes protegidas.

```typescript
class Conta {
  #saldo: number;  // campo privado de verdade em JS moderno

  constructor(saldoInicial: number) {
    this.#saldo = saldoInicial;
  }

  sacar(valor: number): void {
    if (valor > this.#saldo) throw new Error("Saldo insuficiente");
    this.#saldo -= valor;
  }

  get saldo(): number { return this.#saldo; }
}
```

### 2. Herança

Uma classe (subclasse) herda atributos e métodos de outra (superclasse), permitindo reutilização e especialização.

```java
public abstract class Animal {
    protected String nome;
    public abstract void emitirSom();
}

public class Cachorro extends Animal {
    @Override
    public void emitirSom() { System.out.println("Au au"); }
}
```

**Cuidado:** herança cria **acoplamento forte** — a subclasse depende de detalhes internos da superclasse. Mudanças na base podem quebrar filhos (problema do "fragile base class"). Herança deve modelar relações **is-a** reais, não reuso de código.

> **Regra prática:** antes de herdar, pergunte "o filho realmente é-um pai em qualquer contexto em que o pai é usado?". Se não, prefira composição.

### 3. Polimorfismo

Objetos de diferentes tipos respondem à mesma interface. O código cliente trata todos uniformemente; cada objeto responde de forma específica.

**Dois tipos:**

- **Polimorfismo de subtipo (runtime):** override. `Cachorro` e `Gato` implementam `Animal.emitirSom()` diferente.
- **Polimorfismo paramétrico (generics):** `List<T>` funciona para qualquer T.
- **Ad-hoc (overload):** mesmo nome de método, assinaturas diferentes. Em Java sim; em TS/JS, não.

```java
List<Animal> animais = List.of(new Cachorro(), new Gato(), new Vaca());
for (Animal a : animais) {
    a.emitirSom();  // polimorfismo de runtime
}
```

### 4. Abstração

Modelar um conceito pelo que ele **faz**, não como faz. Uma interface `PaymentGateway` define *o que* é pagar, sem dizer se é Stripe, PagSeguro ou PIX.

```java
public interface PaymentGateway {
    PaymentResult charge(Money amount, Customer customer);
    void refund(String transactionId);
}

public class StripeGateway implements PaymentGateway { /* ... */ }
public class PagSeguroGateway implements PaymentGateway { /* ... */ }
```

**Abstração ≠ interface:** abstração é o ato de escolher o nível certo de detalhe para o problema. Uma classe `Money` com operações `add`, `subtract`, `convert` é abstração — mesmo sem interface — porque esconde representação (BigDecimal, moeda, escala).

---

## SOLID

Cinco princípios que, aplicados juntos, levam a código flexível, testável e evolutivo. Não são regras religiosas — são heurísticas cujas exceções você deve conhecer.

### S — Single Responsibility Principle (SRP)

> "Uma classe deve ter **uma única razão para mudar**."

Não é "uma classe, uma função". É sobre **eixos de mudança**: se regras de persistência mudam por um motivo e regras de negócio por outro, separe-as em classes distintas.

```java
// Ruim: uma classe com 3 razões para mudar
class PedidoService {
    void criarPedido() { /* lógica de negócio */ }
    void salvarNoBanco() { /* persistência */ }
    void enviarEmail()  { /* notificação */ }
}

// Bom: 3 classes, 3 razões
class PedidoService {
    private PedidoRepository repo;
    private EmailService emails;
    void criarPedido(Pedido p) {
        // valida, orquestra
        repo.save(p);
        emails.notificarCriacao(p);
    }
}
```

### O — Open/Closed Principle

> "Módulos devem estar **abertos para extensão** e **fechados para modificação**."

Adicionar comportamento novo não deveria exigir mudar código existente. Alcança-se com polimorfismo: novos casos = novas classes implementando a mesma interface.

```java
// Violação: adicionar um novo tipo exige editar este switch
double calcularArea(Forma f) {
    switch (f.tipo) {
        case "circulo":   return Math.PI * f.raio * f.raio;
        case "quadrado":  return f.lado * f.lado;
        // novo tipo → editar aqui, e em todos os outros switches
    }
}

// OCP: cada forma sabe calcular a própria área
interface Forma {
    double area();
}
class Circulo implements Forma { public double area() { return Math.PI * raio * raio; } }
class Quadrado implements Forma { public double area() { return lado * lado; } }
// Novo tipo = nova classe, zero alteração no código existente
```

### L — Liskov Substitution Principle (LSP)

> "Subtipos devem ser substituíveis pelo tipo base **sem quebrar o comportamento esperado**."

Se o código funciona com `Bird`, deve funcionar com `Penguin` sem surpresas. Violar LSP significa que sua hierarquia está modelando algo errado.

**Exemplo canônico de violação:** `Rectangle` → `Square`. Parece natural, mas se o código espera `rect.setWidth(5); rect.setHeight(10); assert rect.area() == 50`, um `Square` que sincroniza width/height quebra.

**Sinal de violação:** métodos da subclasse que lançam `UnsupportedOperationException` ou checam o tipo concreto. Isso quer dizer que a subclasse não é realmente um subtipo.

### I — Interface Segregation Principle (ISP)

> "Nenhum cliente deve ser forçado a depender de métodos que não usa."

Prefira **várias interfaces pequenas** a uma grande.

```java
// Violação: quem só imprime é obrigado a implementar fax/scan
interface Multifuncional {
    void imprimir();
    void escanear();
    void enviarFax();
}

// ISP: separar em capacidades
interface Impressora { void imprimir(); }
interface Scanner    { void escanear(); }
interface Fax        { void enviarFax(); }

class ImpressoraSimples implements Impressora { /* ... */ }
class MFP implements Impressora, Scanner, Fax { /* ... */ }
```

### D — Dependency Inversion Principle (DIP)

> "Módulos de alto nível não devem depender de módulos de baixo nível. Ambos devem depender de **abstrações**."

Em vez de `PedidoService` importar `MySQLPedidoRepository`, ele importa `PedidoRepository` (interface). A implementação concreta é injetada de fora.

**Isto é a base de Dependency Injection** — e é o que torna Spring Boot tão poderoso. Seus beans dependem de interfaces; o container escolhe a implementação em tempo de boot ou teste.

```java
@Service
public class PedidoService {
    private final PedidoRepository repo; // interface!

    public PedidoService(PedidoRepository repo) { // Spring injeta
        this.repo = repo;
    }
}
```

---

## Composição sobre Herança

Regra prática mais importante em OOP moderna. Em vez de estender classes, **componha objetos** injetando dependências ou delegando comportamento.

### Por que herança é perigosa

1. **Acoplamento forte** — filho conhece detalhes da base, mudanças se propagam
2. **Hierarquia rígida** — você só tem **uma** cadeia de pais
3. **Fragile base class** — qualquer mudança na base pode quebrar filhos
4. **Reuso de código, não de conceito** — herdar só para reutilizar método é abuso
5. **Dificulta testes** — difícil mockar pedaço de uma hierarquia

### Composição: exemplos

```typescript
// Herança (frágil, rígida)
class EmailNotifier extends Notifier { /* ... */ }
class SmsNotifier   extends Notifier { /* ... */ }

// Composição (flexível)
interface MessageSender {
  send(to: string, content: string): Promise<void>;
}

class NotificationService {
  constructor(private sender: MessageSender) {}

  async notify(user: User, msg: string) {
    await this.sender.send(user.contact, msg);
  }
}

// Troca de comportamento: passar outra implementação
const service = new NotificationService(new EmailSender());
// ou new SmsSender(), new SlackSender(), new PushSender()...
```

### Quando herança **é** adequada

- **Hierarquia de domínio real e estável** — `Payment` → `CreditCardPayment`, `BankTransferPayment`
- **Template Method pattern** — classe abstrata define esqueleto, filhas preenchem lacunas
- **Frameworks** — estender `JpaRepository`, `HttpServlet`, `AbstractController`
- **Value objects imutáveis** — herança não causa problemas quando não há estado mutável

Mesmo nesses casos, mantenha hierarquias **rasas** (máximo 2-3 níveis).

---

## Tell, Don't Ask

Não pergunte o estado de um objeto para decidir o que fazer — **diga** ao objeto o que você quer. Esse princípio mantém a lógica junto dos dados e evita espalhar regras de negócio pelos clientes.

```java
// Ask: lógica fora do objeto, encapsulamento vazado
if (pedido.getStatus() == PENDENTE && pedido.getTotal().compareTo(LIMITE) < 0) {
    pedido.setStatus(APROVADO);
    pedido.setAprovadoEm(LocalDateTime.now());
}

// Tell: objeto sabe suas próprias regras
pedido.aprovar(); // a lógica de "pode aprovar?" está dentro do método
```

**Relação com DDD:** objetos ricos em comportamento (Rich Domain Model) implementam suas próprias regras; o oposto (Anemic Domain Model) trata entidades como DTOs e coloca toda lógica em services. A segunda abordagem é comum em projetos Java/Spring, mas perde os benefícios de OOP.

---

## Conceitos complementares

### Classes abstratas vs Interfaces

| Aspecto | Interface | Classe abstrata |
| --- | --- | --- |
| Herança múltipla | sim (implementa várias) | não (herda uma só) |
| Estado (campos) | só constantes | sim, campos mutáveis |
| Métodos concretos | sim (`default` em Java 8+) | sim |
| Construtores | não | sim |
| Uso típico | contrato / capacidade | compartilhar implementação parcial |

**Regra prática:** comece com interface. Só migre para classe abstrata se **for mesmo** compartilhar estado ou implementação não-trivial entre filhos.

### Coupling e Cohesion

- **Coupling (acoplamento)** — quanto um módulo depende de outro. Queremos **baixo**.
- **Cohesion (coesão)** — quão relacionadas são as responsabilidades dentro de um módulo. Queremos **alta**.

Bom design = **baixo acoplamento, alta coesão**. SRP otimiza coesão; DIP otimiza acoplamento.

### Law of Demeter (Lei de Demeter)

"Fale apenas com seus amigos imediatos." Evite cadeias de chamadas como `pedido.getCliente().getEndereco().getCep()`. Isso vaza estrutura interna e cria acoplamento transitivo.

```java
// Violação
pedido.getCliente().getEndereco().getCep();

// Correção
pedido.getCepDeEntrega(); // o pedido expõe o que o cliente precisa
```

### Value Objects vs Entities

- **Entity** — tem **identidade**. Dois `User` com o mesmo nome são diferentes se têm IDs diferentes. Mutável.
- **Value Object** — sem identidade. Dois `Money(10, BRL)` são iguais. **Imutável** por regra.

Modelar corretamente isso é o primeiro passo para DDD. Em Java 14+, `record` é a forma natural de value object.

```java
public record Money(BigDecimal amount, Currency currency) {
    public Money add(Money other) {
        if (!currency.equals(other.currency))
            throw new IllegalArgumentException("moedas diferentes");
        return new Money(amount.add(other.amount), currency);
    }
}
```

### Imutabilidade

Objetos imutáveis não mudam após construção. Vantagens: thread-safe, fácil raciocinar, sem side effects, hashable de forma estável.

```java
public final class Coordenada {
    private final double latitude;
    private final double longitude;

    public Coordenada(double lat, double lon) {
        this.latitude = lat;
        this.longitude = lon;
    }

    public Coordenada comLatitude(double nova) {
        return new Coordenada(nova, this.longitude); // retorna nova instância
    }
}
```

Linguagens modernas encorajam imutabilidade: `record` em Java, `readonly` em TS, `data class` em Kotlin, `case class` em Scala.

---

## DDD e Rich Domain Model

Domain-Driven Design (Eric Evans) traz OOP de volta às suas raízes: modelar o **domínio do negócio** com objetos ricos em comportamento.

### Conceitos chave

- **Entity** — objeto com identidade (User, Order)
- **Value Object** — objeto sem identidade, imutável (Money, Address)
- **Aggregate** — conjunto de entities/VOs tratadas como uma unidade, com uma **raiz** que garante invariantes (Order é raiz, OrderItem só existe dentro do Order)
- **Domain Service** — operação que não pertence naturalmente a uma entidade (ex.: transferência entre contas)
- **Repository** — abstração para persistência de aggregates
- **Domain Event** — algo significativo aconteceu no domínio (OrderPlaced, PaymentApproved)
- **Bounded Context** — delimitação de um modelo de domínio coeso. Um mesmo termo ("Produto") pode significar coisas diferentes em contextos diferentes

### Anemic vs Rich Domain Model

```java
// Anemic — entidade sem comportamento (anti-padrão OOP)
class Pedido {
    Long id;
    Status status;
    BigDecimal total;
    // só getters e setters
}

class PedidoService {
    void aprovar(Pedido p) {
        if (p.getStatus() != PENDENTE) throw new ...;
        if (p.getTotal().compareTo(LIMITE) > 0) throw new ...;
        p.setStatus(APROVADO);
    }
}

// Rich — comportamento na entidade
class Pedido {
    private Long id;
    private Status status;
    private BigDecimal total;

    public void aprovar() {
        if (status != PENDENTE)
            throw new PedidoNaoPodeSerAprovadoException();
        if (total.compareTo(LIMITE_APROVACAO) > 0)
            throw new ValorAcimaDoLimiteException();
        this.status = APROVADO;
    }
}

class PedidoService {
    void aprovar(Long id) {
        Pedido p = repo.findById(id).orElseThrow();
        p.aprovar();
        repo.save(p);
    }
}
```

---

## Anti-patterns comuns

- **God Class** — classe que faz tudo. Viola SRP. Quebre por responsabilidade.
- **Anemic Domain Model** — entidades só com getters/setters, lógica em services. Você está fazendo programação procedural disfarçada.
- **Feature Envy** — um método usa mais dados de outra classe do que da sua própria. Mova-o para lá.
- **Data Class / Data Clump** — agrupamentos de dados que aparecem juntos em muitos lugares. Extraia para um objeto.
- **Shotgun Surgery** — uma mudança simples exige tocar muitas classes. Coesão ruim.
- **Yo-yo Problem** — hierarquia profunda onde você precisa navegar pra cima e pra baixo pra entender o fluxo.
- **Refused Bequest** — subclasse herda métodos que não usa ou lança exceção. Violação de LSP ou hierarquia errada.
- **Circular Dependency** — A depende de B que depende de A. Extraia a dependência comum.
- **Primitive Obsession** — usar `String` e `int` em vez de tipos de domínio (`Cpf`, `Email`, `Money`).
- **Exposed Internals** — getters/setters públicos que permitem mutação descontrolada.
- **Leaky Abstraction** — interface que vaza detalhes da implementação (ex.: método `executeRawSQL()` em `Repository`).

---

## Armadilhas comuns em entrevistas

- **Recitar definições sem contexto:** "encapsulamento é esconder estado" não impressiona. Dê exemplo de **quando** viu isso ser violado e **por que** importou.
- **Dizer que usa SOLID sem aplicar:** entrevistadores testam. "Como você aplicou DIP recentemente?"
- **Defender herança a qualquer custo:** em 2026, a resposta esperada é "prefiro composição, exceto em X e Y".
- **Confundir interface com classe abstrata:** saiba a diferença e quando escolher cada uma.
- **Esquecer que OOP é ferramenta, não religião:** às vezes uma função pura é melhor que uma classe. Nem tudo precisa ser objeto.
- **Over-engineering:** criar interface com uma implementação "para o futuro". YAGNI. Crie quando a segunda implementação aparecer.

---

## Na prática (da minha experiência)

> No MedEspecialista, a arquitetura de notificações foi um caso canônico de DIP + OCP bem aplicado. A interface `NotificationSender` tem implementações para email, SMS e push. Adicionar WhatsApp foi criar uma classe nova — zero mudança no código consumidor. E em testes, injetar um `FakeSender` que só grava as mensagens em memória tornou a suíte rápida e determinística.
>
> O oposto que aprendi a evitar: no início da carreira, fazia `Service` gigantes com toda a lógica de negócio, enquanto entidades eram só getters/setters (Anemic Domain Model). Refatorar isso depois de anos é doloroso. Hoje, começo com Rich Domain Model: a regra "um pedido só pode ser aprovado se estiver pendente e dentro do limite" vive dentro de `Pedido.aprovar()`, não espalhada em services.
>
> Sobre herança: no Digidados, tive uma hierarquia de 4 níveis de `Report` que parecia elegante no papel e virou pesadelo de manutenção. Refatorei para composição — `ReportBuilder` que recebe `HeaderStrategy`, `BodyStrategy`, `FooterStrategy`. Mais verboso, infinitamente mais flexível.
>
> **Lição:** as regras de OOP são ferramentas para reduzir acoplamento e aumentar coesão. Se uma regra "correta" está piorando seu código, você aplicou errado ou escolheu a regra errada para o problema.

---

## How to explain in English

> "Object-Oriented Programming is the foundation of how I structure backend systems, but I try to be pragmatic about it. The four pillars — encapsulation, inheritance, polymorphism, abstraction — are a starting point, but what actually matters day-to-day is SOLID, composition over inheritance, and keeping domain logic inside the domain objects.
>
> In my Spring Boot work, dependency inversion is everywhere: services depend on repository interfaces, and Spring injects the concrete implementations. That's what makes the code testable — I can swap in fakes or mocks — and extensible, because adding a new behavior usually means adding a class rather than editing existing ones.
>
> I've learned to be skeptical of deep inheritance hierarchies. Early in my career, I built elegant class trees that turned into maintenance nightmares — any change to a base class rippled everywhere. Now I default to composition: inject a collaborator instead of inheriting from one. Inheritance I reserve for genuine is-a relationships and framework extension points.
>
> The other habit I've built is keeping the domain rich. Instead of anemic entities with only getters and setters and fat services doing all the work, I put the business rules where the data lives. An `Order` knows whether it can be approved, a `Money` knows how to add itself to another Money of the same currency. That alignment between data and behavior is what OOP is really about."

### Frases úteis para pivotar design

- "I'd extract that into its own class because it has a distinct reason to change."
- "I'd depend on an interface here so we can swap implementations in tests."
- "This violates Liskov — the subclass is refusing a behavior the base class promises."
- "That's primitive obsession — we should have a `Money` type instead of `BigDecimal` everywhere."
- "I prefer composition here; inheritance would couple us too tightly to the base class."
- "Let's put that invariant inside the entity so we can't accidentally bypass it."

### Key vocabulary

- encapsulamento → encapsulation
- herança → inheritance
- polimorfismo → polymorphism
- abstração → abstraction
- composição → composition
- classe base → base class / superclass
- subclasse → subclass / derived class
- sobrescrita → override
- sobrecarga → overload
- interface → interface
- classe abstrata → abstract class
- classe concreta → concrete class
- instância → instance
- inversão de dependência → dependency inversion
- injeção de dependência → dependency injection
- princípio da responsabilidade única → single responsibility principle
- princípio aberto-fechado → open/closed principle
- substituição de Liskov → Liskov substitution
- segregação de interfaces → interface segregation
- modelo de domínio anêmico → anemic domain model
- modelo de domínio rico → rich domain model
- acoplamento → coupling
- coesão → cohesion
- objeto de valor → value object
- entidade → entity
- agregado → aggregate
- contexto delimitado → bounded context

---

## Recursos

### Livros

- *Domain-Driven Design* — Eric Evans (o "blue book")
- *Implementing Domain-Driven Design* — Vaughn Vernon (o "red book")
- *Clean Code* — Robert C. Martin
- *Clean Architecture* — Robert C. Martin
- *Refactoring* — Martin Fowler
- *Object-Oriented Software Construction* — Bertrand Meyer (clássico, denso)
- *Effective Java* — Joshua Bloch (capítulos 4-6 tratam de OOP em Java)

### Artigos

- [Tell Don't Ask — Martin Fowler](https://martinfowler.com/bliki/TellDontAsk.html)
- [AnemicDomainModel — Martin Fowler](https://martinfowler.com/bliki/AnemicDomainModel.html)
- [Composition over Inheritance — Wikipedia](https://en.wikipedia.org/wiki/Composition_over_inheritance)
- [SOLID Principles — Uncle Bob](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html)

## Veja também

- [[Design Patterns]]
- [[Arquitetura de Software]]
- [[Java Fundamentals]]
- [[Estruturas de Dados]]
