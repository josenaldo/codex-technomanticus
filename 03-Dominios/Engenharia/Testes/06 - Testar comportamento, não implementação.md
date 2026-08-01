---
title: "Testar comportamento, não implementação"
created: 2026-06-18
updated: 2026-08-01
type: concept
fase: adepto
status: evergreen
publish: true
tags:
  - engenharia
  - testes
  - mocks
  - design
  - entrevista
---

# Testar comportamento, não implementação

> [!abstract] Resumo em uma linha
> Um bom teste verifica o resultado observável do código, não os passos internos que o produziram — por isso ele sobrevive à refatoração. A regra de ouro: se uma refatoração que preserva comportamento quebra um teste, o teste está errado, não o código.
> Há duas formas de escrever a asserção — **state-based** (pergunta se o estado/retorno ficou certo) e **interaction-based** (pergunta se os colaboradores certos foram chamados) — e a primeira tolera refatoração, a segunda fica refém dela.
> Na prática, isso empurra você para preferir **fake sobre mock**: uma implementação real e simplificada (como um `InMemoryUserRepository` com `HashMap`) dá verificação de estado de graça, sem o acoplamento às chamadas que um mock cobra.

Imagine que você precisa avaliar um cozinheiro. Há dois jeitos. O primeiro: você prova o prato. Está no ponto? Tempero certo? Apresentação boa? O segundo: você fica atrás dele com uma prancheta anotando cada movimento de faca — "cortou a cebola em 0,8 cm, depois pegou a frigideira com a mão esquerda, depois...".

O primeiro avaliador testa **comportamento**. O segundo testa **implementação**.

Agora pense: o que acontece quando o cozinheiro descobre uma forma melhor de cortar a cebola? Para o primeiro avaliador, nada — o prato continua delicioso. Para o segundo, o mundo desaba: "ERRADO! Você cortou diferente!". E o prato? Ah, o prato ele nem provou.

Essa é a nota inteira em uma metáfora. O teste que prova o prato é robusto. O teste que cronometra a faca é frágil. E a maior parte dos testes ruins que você vai encontrar na vida estão segurando uma prancheta.

## A regra de ouro

> [!important] A regra
> Se você refatora o código mantendo o comportamento e um teste quebra, **o teste está errado** — não o código.

Refatoração, por definição, muda a estrutura interna sem mudar o comportamento observável. Renomear uma variável. Extrair um método. Trocar um `for` por um `stream`. Reordenar duas chamadas que não dependem uma da outra. Nada disso altera o que o sistema *faz*.

Então o que um teste de comportamento deveria fazer durante uma refatoração? **Nada.** Continuar verde. Silencioso. Confirmando que você não quebrou nada.

Quando o teste fica vermelho numa refatoração pura, ele acabou de te dar um **falso positivo**: gritou "regressão!" sem que houvesse regressão. Khorikov chama essa propriedade de **resistência à refatoração** (*resistance to refactoring*) e a coloca como um dos quatro pilares de um bom teste. Um teste que não resiste à refatoração polui seu sinal: você para de confiar no vermelho, porque metade das vezes é só o teste sendo chato.

```mermaid
flowchart TD
    A["Você refatora<br/>(comportamento preservado)"] --> B{"O teste<br/>fica vermelho?"}
    B -->|"Não — continua verde"| C["Teste de comportamento<br/>Confiavel"]
    B -->|"Sim — quebrou"| D["Teste de implementacao<br/>Fragil — falso positivo"]
    D --> E["Voce perde confianca no vermelho"]
    E --> F["Voce passa a ignorar testes<br/>ou deletar quando incomodam"]

    style C fill:#1b4332,color:#fff
    style D fill:#660708,color:#fff
    style F fill:#660708,color:#fff
```

Leitura do diagrama: o ramo da esquerda é o objetivo. O da direita é a espiral — um teste frágil não só te incomoda, ele corrói a sua confiança no suite inteiro. E um suite em que ninguém confia é pior que nenhum suite, porque custa manutenção sem dar segurança.

O que é, então, o "comportamento observável"? São três coisas que o mundo de fora consegue enxergar:

- **Retorno** — o valor que o método devolve.
- **Estado** — como o objeto (ou o sistema) ficou depois.
- **Efeito visível** — uma interação com uma dependência externa que *só* é observável por essa interação (o e-mail foi enviado de verdade, a linha foi gravada no banco).

Tudo o que estiver entre a chamada e essas três coisas é **implementação**: métodos privados, ordem de operações internas, estruturas de dados intermediárias, qual colaborador foi chamado primeiro. Nada disso é assunto do seu teste.

### O critério prático: para que serve essa API?

A definição acima ("retorno, estado, efeito visível") é precisa, mas ainda deixa uma dúvida no fim do dia: diante de um método específico, como saber se ele é comportamento ou detalhe? Khorikov propõe um critério operacional: **uma API é comportamento observável se existe um cliente — outra classe, outro serviço, o usuário final — que a usa para atingir um objetivo de negócio.** Se a única razão para o método existir é permitir que o teste espie o meio do caminho, ele é implementação, não importa quão útil pareça verificá-lo.

O sintoma mais concreto disso é um cheiro de código específico: **você precisou tornar um método `private` em `public` (ou anotá-lo `@VisibleForTesting`) só para o teste conseguir chamá-lo.** Isso é o teste forçando uma fresta na encapsulação — e o próprio ato de forçar já denuncia o problema: se nenhum cliente de produção jamais chamaria esse método diretamente, ele não tem negócio sendo parte da API pública, nem parte do vocabulário do teste.

> [!tip] O que fazer quando a lógica privada é importante demais para ignorar
> Khorikov é direto sobre a saída: se um método privado contém lógica complexa demais para ser coberta indiretamente através da API pública da classe, isso não é motivo para expor o método — é o sinal de que essa lógica merece **sua própria classe**, com sua própria API pública. A classe nova vira testável pelo comportamento; o método volta a ser privado (ou desaparece).

Repare que esse critério é o mesmo que já apareceu nos "quatro pilares": abrir uma fresta em um método privado para testá-lo reduz a resistência à refatoração quase a zero — qualquer mudança na implementação interna passa a arriscar quebrar esse teste, mesmo que o comportamento público continue idêntico.

## State-based × interaction-based testing

Há duas formas de escrever a asserção de um teste, e a escolha entre elas é o coração da fragilidade.

**State-based** (verificação de estado): você exercita o código e depois pergunta *"o objeto ficou como eu esperava?"*. Olha o retorno, olha o estado final.

**Interaction-based** (verificação de comportamento/interação): você pergunta *"o código chamou os colaboradores certos, com os argumentos certos?"*. Olha as chamadas — `verify(emailService).send(...)`.

Fowler, em **"Mocks Aren't Stubs"**, formaliza essa divisão: *state verification* investiga o estado do sistema e dos colaboradores depois do exercício; *behavior verification* checa se o sistema fez as chamadas corretas aos colaboradores. Stubs trabalham com verificação de estado; só mocks *insistem* em verificação de interação.

```mermaid
flowchart LR
    SUT["Sistema sob teste"]

    subgraph SB["State-based"]
        direction TB
        S1["Exercita o SUT"] --> S2["Pergunta:<br/>o estado/retorno<br/>esta correto?"]
    end

    subgraph IB["Interaction-based"]
        direction TB
        I1["Exercita o SUT"] --> I2["Pergunta:<br/>chamou colaborador.X()<br/>com estes argumentos?"]
    end

    SUT --> SB
    SUT --> IB

    S2 --> R1["Acoplado ao RESULTADO<br/>Sobrevive a refatoracao"]
    I2 --> R2["Acoplado a COMO<br/>Quebra se a ordem/forma muda"]

    style R1 fill:#1b4332,color:#fff
    style R2 fill:#7f5539,color:#fff
```

Leitura do diagrama: os dois começam igual — exercitam o SUT. A diferença está na pergunta final. State-based pergunta sobre o *resultado* e por isso tolera mudanças internas. Interaction-based pergunta sobre o *processo* e por isso fica refém dele. Não é que interaction-based seja sempre errado — é que ele cobra um preço (acoplamento) que nem sempre vale a pena.

> [!tip] A heurística
> **Prefira state-based.** Use interaction-based só quando o efeito é *exclusivamente* observável pela interação — não há estado nem retorno para inspecionar.

### Os quatro pilares de Khorikov

Resistência à refatoração não é a única vara de medir um teste — é uma de quatro, segundo o framework que Khorikov propõe em *Unit Testing Principles, Practices, and Patterns*. Vale nomear as outras três, porque a escolha state-based × interaction-based mexe em todas:

| Pilar | Pergunta | Efeito de interaction-based (mock em excesso) |
|---|---|---|
| **Proteção contra regressão** | O teste pega bug de verdade? | Cai — verificar "chamou X" não prova que X fez o que devia; um fake, que executa lógica real, pega mais bug |
| **Resistência à refatoração** | O teste sobrevive a mudar o "como"? | Cai diretamente — é o sintoma central desta nota |
| **Feedback rápido** | O teste roda em milissegundos? | Neutro a favorável — mocks costumam ser rápidos (é o under-mocking, não o over-mocking, que mata esse pilar) |
| **Manutenibilidade** | O teste é fácil de ler e escrever? | Cai — setup de mock cresce a cada colaborador; fakes são escritos uma vez |

Khorikov argumenta que os quatro pilares têm uma tensão estrutural: você pode maximizar qualquer três às custas do quarto, mas nunca os quatro ao mesmo tempo com a mesma técnica. O ponto prático desta nota é que **state-based testing com fakes** é o ponto do espaço de trade-offs que sacrifica menos dos quatro simultaneamente — não é grátis, mas é a escolha com o melhor retorno médio na maioria dos casos.

O exemplo canônico é o envio de e-mail. Quando seu serviço chama `emailService.send(user, msg)`, o que sobra para inspecionar do lado de cá? Nada. Não há valor de retorno significativo, não há estado interno que prove "o e-mail saiu". O *único* jeito de afirmar "o usuário foi notificado" é verificar que a chamada aconteceu. Aí interaction-based é a ferramenta certa, e o mock (ou spy) de `[[05 - Test doubles - dummy, stub, spy, mock, fake]]` é justificado.

Mas note a regra: você está verificando a interação porque o **comportamento** ("notificar o usuário") só se manifesta como interação. Você não está verificando a interação por preguiça de checar o estado. A diferença é sutil e separa o uso legítimo do mock do abuso.

## Over-mocking: testando os mocks

Over-mocking é quando você mocka tanta coisa que o teste deixa de falar sobre o código e passa a falar sobre os mocks. Os sintomas estão catalogados em `## Armadilhas comuns`, mais adiante.

A consequência de todos esses sintomas é a mesma frase: **você acaba testando os mocks**. O teste passa porque os mocks devolvem o que você mandou devolver — uma tautologia. Khorikov é direto sobre isso: o excesso de mocking esconde defeitos e acopla o teste à implementação cedo demais.

```mermaid
flowchart TD
    A["Mockar tudo<br/>(colaboradores, value objects, ...)"] --> B["Setup cheio de<br/>when().thenReturn()"]
    B --> C["Teste codifica a ORDEM<br/>e a FORMA das chamadas"]
    C --> D{"Refatoracao interna<br/>muda alguma chamada"}
    D --> E["Teste quebra<br/>sem regressao real"]
    E --> F["Falso positivo"]
    F --> G["'Vou so ajustar o mock'<br/>(toda refatoracao)"]
    G --> H["Custo de manutencao alto<br/>+ confianca baixa"]

    style F fill:#660708,color:#fff
    style H fill:#660708,color:#fff
```

Leitura do diagrama: cada seta é um degrau na ladeira. Mockar demais leva a setup pesado, que codifica o "como", que quebra na refatoração, que vira falso positivo, que vira retrabalho a cada mudança. O destino é um suite caro e em quem ninguém confia — exatamente o oposto do que um teste deveria entregar. (Os testes que quebram por causa de timing, e não de acoplamento, são outro animal: ver `[[11 - Testes flaky]]`.)

## Under-mocking: o outro extremo

O erro oposto também existe e é igualmente perigoso, só que mais silencioso. **Under-mocking** é quando um teste vendido como "unitário" bate em banco, rede ou disco de verdade — o detalhe está também em `## Armadilhas comuns`.

A questão não é "mockar é ruim". É *o que* você isola. Dependências fora do processo — banco, fila, API HTTP — precisam de cuidado. Em teste unitário você as substitui; quando quer exercitá-las de verdade, escreve um teste de outro nível, com intenção explícita: `[[07 - Testes de integração]]`. O pecado do under-mocking é a mistura — chamar de unitário algo que carrega o peso e a fragilidade da integração, sem os benefícios de nenhum dos dois.

Repare na simetria com o over-mocking:

| | Over-mocking | Under-mocking |
|---|---|---|
| Sintoma | Mocka tudo, até POJO | Não mocka nada, bate no banco |
| Acoplamento | Ao *como* (chamadas internas) | À *infra* (estado externo) |
| Falha típica | Falso positivo na refatoração | Flaky, lento, frágil por ambiente |
| Sinal | "Estou testando os mocks" | "Por que o teste unit demora 4s?" |

O ponto de equilíbrio entre os dois é o assunto da próxima seção. O mecanismo para chegar lá é sempre o mesmo: extrair uma interface na fronteira da dependência externa, e substituir a implementação real por um fake nos testes rápidos:

```java
// Antes: teste "unit" acoplado direto ao Postgres (under-mocking)
class OrderServiceTest {
    PostgresOrderRepository repo = new PostgresOrderRepository(realDataSource);
    OrderService service = new OrderService(repo);

    @Test
    void marksOrderAsPaid() {
        repo.save(new Order(1L, "PENDING"));   // grava no banco de verdade
        service.markAsPaid(1L);                 // conexão de rede, I/O em disco
        assertThat(repo.findById(1L).status()).isEqualTo("PAID"); // lento, flaky
    }
}

// Depois: interface na fronteira + fake em memória (nível certo de isolamento)
interface OrderRepository {
    void save(Order order);
    Order findById(Long id);
}

class InMemoryOrderRepository implements OrderRepository {
    private final Map<Long, Order> store = new HashMap<>();
    public void save(Order order) { store.put(order.id(), order); }
    public Order findById(Long id) { return store.get(id); }
}

class OrderServiceTest {
    OrderRepository repo = new InMemoryOrderRepository();  // troca de implementação, não de contrato
    OrderService service = new OrderService(repo);

    @Test
    void marksOrderAsPaid() {
        repo.save(new Order(1L, "PENDING"));
        service.markAsPaid(1L);
        assertThat(repo.findById(1L).status()).isEqualTo("PAID"); // milissegundos, determinístico
    }
}
```

`PostgresOrderRepository` continua existindo — ela só passa a ser exercitada por um teste de integração de outro nível (`[[07 - Testes de integração]]`), com intenção explícita, e não escondida atrás de um teste que se autodenomina "unit". A interface `OrderRepository` é o que torna a troca possível: sem ela, não há onde plugar o fake — é o mesmo ponto que a seção "Como isso conecta a design" faz mais adiante.

## Armadilhas comuns

> [!warning] Sinais de over-mocking
> - **Mockar value objects / POJOs.** `mock(Money.class)`? Para quê? Um objeto de valor não tem dependência, não tem efeito colateral — é só dado. Mockar dado é cerimônia pura. Use o objeto real.
> - **Cadeias longas de `when().thenReturn()`.** Quando o `setup` do teste tem dez linhas de stubbing antes de uma linha de ação, o teste virou uma transcrição da implementação. Você codificou *como* o SUT chama os colaboradores, passo a passo.
> - **`verifyNoMoreInteractions()` rígido.** Essa asserção diz "o SUT só pode chamar exatamente isto e nada mais". É a prancheta cronometrando a faca. Adicione uma chamada inofensiva (um log, uma métrica) e o teste quebra sem que nada de relevante tenha mudado.
> - **`@Spy` no próprio SUT.** Mockar parcialmente o objeto que você está testando significa que você está testando uma quimera — parte real, parte fingida. Você não testa mais o código; testa uma versão dele que não existe em produção.

> [!danger] O perigo do under-mocking
> Um teste "unit" que abre conexão com Postgres não é unitário — é de integração disfarçado. Ele é lento (segundos, não milissegundos), depende de infra (o banco precisa estar de pé), e é uma fonte clássica de flakiness (concorrência, dados sujos de outro teste, timeout de rede).

> [!warning] Mockar por preguiça, não por necessidade
> A seção sobre state-based × interaction-based já deu a régua: você só tem licença para verificar interação quando o efeito é *exclusivamente* observável pela chamada (§ [[#State-based × interaction-based testing]]). A armadilha é usar `verify(colaborador).metodo(...)` como atalho — porque é mais rápido de escrever do que montar o estado esperado — em vez de reservar a interação para os casos em que não há alternativa. Isso é o mesmo pecado do over-mocking, só que motivado por preguiça em vez de hábito: você acopla o teste ao *como* quando podia ter acoplado ao *o quê*.

## Fakes são subestimados (fake > mock)

Aqui está a tese central da nota, e é uma que muita gente demora anos para internalizar: **na maioria dos casos, um fake é melhor que um mock.**

Um **fake** é uma implementação real, mas simplificada, da dependência. O exemplo clássico: em vez de mockar um `UserRepository`, você escreve um `InMemoryUserRepository` que implementa a mesma interface usando um `HashMap`. Ele *funciona* — salva, busca, deleta — só que na memória, sem banco.

Por que isso é superior?

- **Não acopla a chamadas específicas.** O fake não sabe nem se importa com *quantas vezes* ou *em que ordem* você o chamou. Você guarda um usuário, depois busca — e o fake devolve o que foi guardado, porque ele *de fato* guarda. Isso é state-based testing nativo.
- **É reutilizável.** Um mock é configurado teste a teste (`when().thenReturn()` por toda parte). Um fake é escrito uma vez e usado por dezenas de testes. O setup encolhe drasticamente.
- **É mais legível.** `repo.save(user)` seguido de `assertThat(repo.findById(id)).isPresent()` lê como código de produção. Compare com três linhas de stubbing que ninguém entende em seis meses.
- **Pega bugs de verdade.** Como o fake tem lógica real (chaves do HashMap, sobrescrita em save duplicado), ele às vezes revela um comportamento que um mock — que devolve sempre o mesmo valor canned — esconderia.

> [!note] Quando o fake não serve
> Fake exige que você consiga escrever uma implementação plausível. Para o e-mail enviado, não dá — você não vai escrever um servidor SMTP de mentira só para o teste. Aí o mock/spy é certo, porque o efeito *é* a interação. A regra prática: **fake para dependências que guardam ou transformam dados (repositórios, caches); mock/spy para dependências cujo valor é o efeito colateral observável só pela chamada.**

A seção seguinte formaliza o caso concreto que motivou essa tese. Antes disso, vale fechar a heurística num diagrama de decisão — a pergunta que você deveria fazer toda vez que for escrever um test double:

```mermaid
flowchart TD
    A["Preciso isolar uma dependencia<br/>no teste"] --> B{"O efeito e observavel<br/>de outro jeito alem da chamada?<br/>(retorno, estado, leitura posterior)"}
    B -->|"Sim — da pra ler o estado depois"| C{"Consigo escrever uma<br/>implementacao real e simples?<br/>(HashMap, lista, arquivo temp)"}
    B -->|"Nao — o efeito SO existe<br/>como a chamada em si"| D["mock/spy<br/>(interaction-based e a unica opcao)"]
    C -->|"Sim"| E["fake<br/>(state-based, reutilizavel, robusto)"]
    C -->|"Nao — dependencia complexa<br/>demais pra fingir"| F["stub minimo<br/>(so o necessario pro cenario)"]

    style E fill:#1b4332,color:#fff
    style D fill:#7f5539,color:#fff
    style F fill:#7f5539,color:#fff
```

Leitura do diagrama: a primeira pergunta é a que a seção anterior já fez — o efeito é observável além da própria chamada? Se não, mock é a única ferramenta honesta. Se sim, a segunda pergunta decide entre fake (quando dá pra escrever uma implementação real barata) e stub (quando não dá, mas você só precisa de um retorno fixo pontual). O caminho verde — fake — é o que esta nota defende como *default*, não como regra absoluta.

## Casos práticos

> [!example] Da prancheta ao prato (caso real)
> Migrei de `@Mock UserRepository` com `when().thenReturn()` por todo lado para uma implementação `InMemoryUserRepository extends UserRepository` com `HashMap`. Ficou muito mais legível e os testes pararam de quebrar em refatorações que só mudavam a ordem de chamadas.

Esse caso amarra as duas teses da nota num nó só. **Fake > mock**: a implementação em `HashMap` deu quase todo o benefício do mock sem o custo. E **comportamento, não interação**: os testes pararam de quebrar em refatorações que só mexiam na *ordem das chamadas* — porque o fake nunca testou ordem de chamada para começar. Ele testava o estado. Mudou a ordem, o estado final continuou o mesmo, o teste continuou verde. Exatamente o que a regra de ouro pede.

```java
// ANTES — interaction-based, frágil
@Mock UserRepository repo;
// ... setup espalhado
when(repo.findById(1L)).thenReturn(Optional.of(alice));
when(repo.findByEmail("a@x.com")).thenReturn(Optional.of(alice));
// e o teste, lá no fim, ainda verificava a ordem das chamadas
verify(repo).findById(1L);
verify(repo).save(any());

// DEPOIS — state-based, robusto
class InMemoryUserRepository implements UserRepository {
    private final Map<Long, User> store = new HashMap<>();
    public Optional<User> findById(Long id) { return Optional.ofNullable(store.get(id)); }
    public Optional<User> findByEmail(String e) {
        return store.values().stream().filter(u -> u.email().equals(e)).findFirst();
    }
    public User save(User u) { store.put(u.id(), u); return u; }
}

// no teste:
var repo = new InMemoryUserRepository();
repo.save(alice);
var service = new UserService(repo);

service.deactivate(alice.id());

// asserção sobre ESTADO, não sobre chamadas:
assertThat(repo.findById(alice.id()).orElseThrow().isActive()).isFalse();
```

O teste "depois" não menciona nenhuma chamada interna. Ele afirma uma verdade sobre o mundo: *depois de desativar a Alice, a Alice está inativa*. Refatore `deactivate` como quiser — mude a ordem, extraia métodos, troque o algoritmo — enquanto a Alice acabar inativa, o teste fica verde.

> [!note] Gap consciente
> Esta seção registra só **um** caso real (a migração `@Mock` → `InMemoryUserRepository`). Não há um segundo cenário documentado nesta nota para ilustrar, por exemplo, a troca de um mock de efeito colateral (e-mail, fila) por um fake — esse caso, se e quando existir, deveria ser adicionado aqui como um segundo `[!example]`, não inventado para preencher a seção.

## Como isso conecta a design

Há uma descoberta que assusta na primeira vez: a dificuldade de testar comportamento quase sempre aponta para um problema de *design*, não de *teste*.

Quando você é *forçado* a mockar dez colaboradores para testar uma classe, a classe provavelmente faz coisas demais — viola Responsabilidade Única. Quando você precisa de `@Spy` no SUT, é porque a classe mistura lógica que você quer testar com lógica que você quer fingir — sinal de que essas duas lógicas deveriam estar em classes separadas. Quando o fake é impossível de escrever porque a "dependência" é uma classe concreta cheia de detalhes, falta uma **interface** — uma fronteira limpa entre o que seu código quer e como isso é cumprido.

O mecanismo por trás disso é simples de nomear: um fake só é possível de escrever quando o *contrato* que o SUT depende é pequeno e explícito. Uma classe concreta com vinte métodos públicos, campos privados acoplados e um construtor que abre conexão de rede não tem contrato nenhum — tem uma implementação inteira grudada nela. Comparar os dois lados:

```java
// Difícil de fakear — SUT depende da classe concreta inteira
class OrderService {
    private final PostgresOrderRepository repo; // classe concreta, cheia de detalhes de JDBC
    OrderService(PostgresOrderRepository repo) { this.repo = repo; }
    // para testar isso sem Postgres, você precisaria mockar (ou fingir) TODA a superfície
    // pública de PostgresOrderRepository — incluindo métodos que o OrderService nem usa.
}

// Fácil de fakear — SUT depende só do que precisa
interface OrderRepository {           // contrato pequeno, explícito (ISP)
    void save(Order order);
    Order findById(Long id);
}
class OrderService {
    private final OrderRepository repo; // qualquer implementação serve (DIP)
    OrderService(OrderRepository repo) { this.repo = repo; }
    // um InMemoryOrderRepository de 6 linhas já satisfaz o contrato inteiro
}
```

A diferença não é estilística — é o que separa "consigo escrever um fake em 5 minutos" de "preciso de um framework de mock pesado com reflection". Inversão de Dependência (o SUT depende da abstração `OrderRepository`, não da classe concreta) e Segregação de Interface (o contrato só expõe `save`/`findById`, não os vinte métodos de `PostgresOrderRepository`) não são regras de estilo arquitetural abstratas aqui — são a pré-condição técnica para o fake existir.

Testar comportamento *empurra* o código na direção certa: interfaces pequenas, contratos claros, dependências injetadas. É a mesma força que os princípios `[[03-Dominios/Engenharia/Design de Software/SOLID/index|SOLID]]` aplicam de outro ângulo — Inversão de Dependência te dá a interface que vira o ponto natural do fake; Segregação de Interface te dá interfaces pequenas que são triviais de fakear.

```mermaid
flowchart TD
    A["Tento testar<br/>o comportamento"] --> B{"E facil?"}
    B -->|"Sim"| C["Design ja esta bom<br/>(fronteiras claras)"]
    B -->|"Nao — preciso mockar tudo"| D["Sinal de design ruim"]
    D --> E["Classe faz demais<br/>(viola SRP)"]
    D --> F["Falta interface<br/>(viola DIP)"]
    E --> G["Refatore o CODIGO,<br/>nao force o teste"]
    F --> G
    G --> A

    style C fill:#1b4332,color:#fff
    style D fill:#7f5539,color:#fff
    style G fill:#1d3557,color:#fff
```

Leitura do diagrama: o teste difícil não é um problema a contornar com mais mocks — é um *diagnóstico* gratuito do seu design. O loop de volta para "tento testar" é o ponto: você refatora o código, tenta testar de novo, e agora é fácil. Código testável e código bem desenhado são, na prática, a mesma coisa vista por ângulos diferentes. (A aplicação concreta disso em Java aparece em `[[Testes em Java]]`, e a anatomia de uma asserção sobre comportamento está em `[[03 - Anatomia de um bom teste]]` e `[[04 - Testes unitários]]`.)

Note a ordem causal: você não escreve testes state-based *para então* ter um design melhor — o design bom é o que *permite* o teste state-based. A causalidade corre do design para o teste, não o contrário. Forçar um fake sobre um design ruim (mockando internamente pra simular a interface que falta) é maquiagem; a correção de verdade é extrair a interface primeiro.

## Em entrevista

> [!quote] Em inglês
> Test observable behavior, not implementation details — the golden rule is that a behavior-preserving refactor should never break a test. I default to state-based verification: I exercise the system and assert on the return value or the resulting state. I only reach for interaction-based verification (mocks) when the effect is *only* observable through the interaction, like sending an email or publishing a message. My biggest practical lever is preferring fakes over mocks — an in-memory repository backed by a HashMap gives me state-based testing for free, reads like production code, and doesn't shatter when I reorder internal calls. Over-mocking — mocking value objects, long `when().thenReturn()` chains, strict `verifyNoMoreInteractions()`, spying on the SUT — is a smell: you end up testing your mocks instead of your code. And when a class is painful to test without mocking everything, that's a design signal, not a testing problem — usually a missing interface or a class doing too much.

### Vocabulário

| PT-BR | EN |
|---|---|
| comportamento observável | observable behavior |
| detalhes de implementação | implementation details |
| resistência à refatoração | resistance to refactoring |
| falso positivo (teste quebra sem regressão) | false positive |
| verificação de estado | state verification / state-based testing |
| verificação de interação | interaction / behavior verification |
| excesso de mocking | over-mocking |
| testar os mocks | testing the mocks |
| dublê de teste | test double |
| implementação falsa em memória | in-memory fake |
| acoplado à implementação | coupled to the implementation |
| sinal de design ruim | design smell |
| proteção contra regressão | protection against regression |
| feedback rápido | fast feedback |
| manutenibilidade | maintainability |
| contrato / fronteira | contract / seam |

## O que vem a seguir

A regra "comportamento, não implementação" foi apresentada aqui com exemplos em Java/JVM (Mockito, `HashMap`, JUnit-style asserts), mas ela é uma lente, não uma tecnologia — vale em qualquer stack que tenha testes e mocks. Dois lugares onde essa mesma lente aparece com uma cara bem diferente:

- No front-end, a Testing Library formaliza a mesma ideia com um lema próprio ("the more your tests resemble the way your software is used, the more confidence they can give you") e a aplica a queries de DOM em vez de asserções de estado de objeto — vale a pena ver como o princípio se traduz para consultar por texto/role em vez de por `data-testid` ou classe CSS: `[[03-Dominios/Tecnologia/Testes JS/07 - Testing Library - filosofia e queries]]`.
- Quando o "comportamento observável" é grande demais ou complexo demais para caber numa asserção manual — uma resposta JSON inteira, uma árvore de renderização, um relatório — a técnica de approval/golden master testing captura o output inteiro como snapshot e compara contra uma versão aprovada, levando a mesma filosofia (testar o resultado, não o caminho) a um extremo prático: `[[03-Dominios/Engenharia/Arqueologia e Restauração de Software/11 - Approval e Golden Master testing]]`.

## Veja também

- `[[03 - Anatomia de um bom teste]]` — a estrutura da asserção que verifica comportamento
- `[[04 - Testes unitários]]` — o nível onde essa filosofia mais pega
- `[[05 - Test doubles - dummy, stub, spy, mock, fake]]` — o catálogo de dublês; fake vs mock detalhado
- `[[07 - Testes de integração]]` — onde dependências reais entram com intenção explícita
- `[[11 - Testes flaky]]` — a outra fonte de testes que você não pode confiar
- `[[16 - Estratégia de testes em entrevista]]` — como articular tudo isso sob pressão
- `[[03-Dominios/Engenharia/Design de Software/SOLID/index|SOLID]]` — por que código testável é código bem desenhado
- `[[Testes em Java]]` — Mockito, fakes e a aplicação concreta na linguagem
- `[[03-Dominios/Engenharia/Testes/index|Testes]]` — o índice do galho

> [!tip] Vídeo — To mock or not to mock?
> Georgios Kalaitzis, [**"To mock or not to mock? Choosing a mocking strategy for your unit tests"**](https://www.youtube.com/watch?v=QQUwZQvuFCQ) — talk que percorre o mesmo território desta nota do lado prático: o que é um test double, quando usar mock vs. quando preferir um fake, e como a escolha errada acopla o teste à implementação. Bom complemento em inglês para quem já entende a teoria (Fowler/Khorikov) e quer ver a decisão sendo tomada caso a caso.

## Fontes

- Martin Fowler, [**Mocks Aren't Stubs**](https://martinfowler.com/articles/mocksArentStubs.html) (2007) — a distinção canônica entre *state verification* e *behavior verification*, e entre o estilo "classicista" e o "mockista".
- Kent C. Dodds, [**Testing Implementation Details**](https://kentcdodds.com/blog/testing-implementation-details) — por que testar detalhes de implementação quebra na refatoração e dá falsos positivos; foque no que o "usuário" do código observa.
- Vladimir Khorikov, [**Unit Testing Principles, Practices, and Patterns**](https://www.manning.com/books/unit-testing) (Manning, 2020) — os quatro pilares, com destaque para *resistance to refactoring*; o excesso de mocking esconde defeitos e acopla o teste à implementação.
- Vladimir Khorikov, [**Unit testing private methods is not only about encapsulation**](https://khorikov.org/posts/2020-03-26-private-methods-encapsulation/) — o critério prático de "comportamento observável" (cliente com um objetivo) e o sintoma de precisar tornar um método `private` em `public` só para testá-lo; quando a lógica privada é complexa demais, a saída é extrair uma classe nova, não expor o método.
