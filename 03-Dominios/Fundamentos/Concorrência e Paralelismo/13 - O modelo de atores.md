---
title: "O modelo de atores"
created: 2026-06-18
updated: 2026-06-18
type: concept
fase: magus
status: evergreen
publish: false
tags:
  - fundamentos
  - concorrencia
  - modelos
  - atores
  - entrevista
---

# O modelo de atores

> [!abstract] Resumo em uma linha
> Em vez de proteger memória compartilhada com cadeados, o modelo de atores elimina o compartilhamento: cada ator é um pequeno ser isolado, com estado privado e uma caixa de entrada, que processa um recado por vez e fala com os outros só por mensagens assíncronas.

Você já viu duas formas de domar a concorrência. Em [[03 - Estado compartilhado e race conditions]], a memória é compartilhada e você paga o pedágio dos cadeados. Em [[12 - Troca de mensagens e CSP]], processos anônimos se encontram em canais e trocam dados num aperto de mão. O modelo de atores é o terceiro grande paradigma — e o mais radical na sua aposta: *e se ninguém pudesse tocar no estado de ninguém?*

Pense num escritório enorme. Cada funcionário tem sua própria mesa, suas próprias gavetas, seus próprios papéis. Ninguém invade a mesa do outro pra mexer numa planilha. Se você precisa que alguém faça algo, você deixa um bilhete na caixa de entrada dele. Ele lê os bilhetes um por um, na ordem que chegaram, e responde — talvez mudando seus próprios papéis, talvez deixando bilhetes pra outras pessoas, talvez contratando um estagiário novo. Esse funcionário é um ator.

A pergunta que move este modelo é simples: se a race condition nasce de dois fios de execução pisando no mesmo dado, e se cada dado vive dentro de um único dono que processa um pedido por vez, *de onde viria a corrida?*

## O modelo: Hewitt, 1973

O modelo de atores foi proposto em 1973 por Carl Hewitt, junto com Peter Bishop e Richard Steiger, como uma arquitetura modular universal para construir sistemas inteligentes. A ideia era ter uma unidade de computação que fosse, ao mesmo tempo, a unidade de concorrência, a unidade de estado e a unidade de comunicação. Essa unidade é o **ator**.

Um ator tem três coisas e faz três coisas. As três coisas que ele *tem*:

- **Estado privado.** Memória que é só dele. Ninguém de fora lê, ninguém de fora escreve. Não existe ponteiro pro miolo de um ator.
- **Um endereço.** Uma identidade pela qual outros atores conseguem mandar mensagens pra ele. O endereço é público; o estado, não.
- **Um mailbox (caixa de mensagens).** Uma fila onde as mensagens que chegam ficam esperando, na ordem em que chegaram.

E as três coisas que ele *pode fazer* ao processar uma mensagem — e só ao processar uma mensagem:

1. **Mudar seu próprio estado** (mexer nas suas gavetas).
2. **Enviar mensagens** a outros atores que ele conhece (deixar bilhetes).
3. **Criar novos atores** (contratar estagiários).

Nada além disso. Toda a riqueza de um sistema de atores emerge dessas três ações encadeadas, milhões de vezes por segundo. As mensagens são **imutáveis** e a comunicação é **100% assíncrona**: você manda o recado e segue a vida — *fire-and-forget*, sem esperar resposta na linha.

Vamos olhar o ciclo de vida de uma única mensagem dentro de um ator.

```mermaid
flowchart TD
    M[Mensagem chega] --> MB[(Mailbox / fila)]
    MB --> P{Ator livre?}
    P -->|não, processando outra| W[Espera na fila]
    W --> MB
    P -->|sim| R[Pega a próxima mensagem]
    R --> H[Processa: roda o comportamento do ator]
    H --> A1[Muda estado privado]
    H --> A2[Envia mensagens a outros atores]
    H --> A3[Cria novos atores]
    A1 --> D[Pronto p/ próxima mensagem]
    A2 --> D
    A3 --> D
    D --> MB
```

Leitura do diagrama: a mensagem entra pela fila do mailbox. Se o ator já está ocupado processando outra mensagem, a nova espera — não há atendimento em paralelo dentro do ator. Quando ele fica livre, pega a próxima, roda seu comportamento (que pode disparar qualquer combinação das três ações) e só então volta pra fila pra pegar a seguinte. O laço nunca processa duas mensagens ao mesmo tempo.

> [!note] O comportamento pode mudar
> Na formulação de Hewitt, ao processar uma mensagem o ator também especifica qual será seu comportamento para a *próxima* mensagem. Ou seja, um ator pode "trocar de chapéu" entre mensagens — uma máquina de estados onde cada transição é disparada por um recado. É um detalhe sutil mas poderoso: o ator de amanhã não precisa ser igual ao de hoje.

## Por que isso mata a race condition

Aqui está o coração do modelo. Em [[01 - Concorrência e paralelismo - o que é e por que é difícil]] vimos que a dificuldade da concorrência mora no **estado mutável compartilhado**. Tire o compartilhamento e o problema some — não se mitiga, *some*.

O truque tem duas camadas. **Entre atores**, há concorrência plena: mil atores podem estar processando suas mensagens ao mesmo tempo, em mil núcleos. **Dentro de um ator**, há serialização absoluta: um ator processa exatamente uma mensagem de cada vez, do começo ao fim, sem interrupção.

Repare no que isso significa pro estado privado. O único código que toca o estado de um ator é o próprio ator, e ele só roda um pedaço por vez. Não existe "dois acessos simultâneos ao mesmo dado", porque nunca há dois acessos simultâneos — *período*. A região crítica é o ator inteiro, e a exclusão mútua é grátis, dada pela arquitetura.

Lembra do confinamento que vimos em [[03 - Estado compartilhado e race conditions]]? Confinar um dado a uma única thread o torna seguro sem cadeado. O modelo de atores pega essa ideia e a eleva a princípio organizador do sistema todo: *todo* estado é confinado, *sempre*, a um único ator. Você não confina por disciplina; confina por construção.

```mermaid
sequenceDiagram
    participant Cliente
    participant Conta as Ator Conta (saldo privado)
    participant Log as Ator Log
    Cliente->>Conta: {sacar, 50}
    Note over Conta: processa sozinho;<br/>saldo 100 -> 50
    Conta-->>Log: {sacado, 50}
    Cliente->>Conta: {sacar, 30}
    Note over Conta: processa sozinho;<br/>saldo 50 -> 20
    Conta-->>Log: {sacado, 30}
    Note over Cliente,Log: setas tracejadas = assíncrono;<br/>ninguém espera resposta
```

Leitura do diagrama: dois saques chegam ao ator Conta. Mesmo que o Cliente dispare os dois quase juntos, eles entram na fila e são processados em série — `100 → 50 → 20`, sem perder atualização. O saldo é privado: não há outra thread capaz de ler `100` e escrever `70` "por cima". As setas tracejadas marcam o envio assíncrono: o Cliente não bloqueia esperando, e o ator Log recebe os avisos quando der.

Compare isso com o mesmo cenário em memória compartilhada com `saldo -= 50` sem cadeado: duas threads leem `100`, ambas calculam e gravam, uma sobrescreve a outra, e some dinheiro. O ator não tem como cair nessa, porque a sequência inteira "ler, calcular, gravar" roda atomicamente do ponto de vista de fora.

## Ator × CSP: dois sabores de mensagem

É fácil confundir atores com CSP — ambos pregam "comunique trocando mensagens, não compartilhando memória". Mas a diferença na *forma* da comunicação muda tudo, e entrevistadores adoram cobrar isso.

```mermaid
flowchart LR
    subgraph Atores
        direction TB
        A1[Ator A] -->|msg p/ endereço de B| MBb[(Mailbox de B)]
        MBb --> B1[Ator B]
    end
    subgraph CSP
        direction TB
        A2[Processo A] <-->|rendezvous no canal| CH{{Canal anônimo}}
        CH <-->|rendezvous| B2[Processo B]
    end
```

Leitura do diagrama: à esquerda, o modelo de atores — A conhece o *endereço* de B e deposita a mensagem no mailbox de B; B não precisa estar pronto, o recado espera na fila, e A segue sem bloquear. À direita, CSP — A e B se encontram num *canal anônimo*; o canal não pertence a ninguém, e (no caso síncrono clássico) os dois precisam estar prontos ao mesmo tempo pro rendezvous acontecer.

As diferenças que importam:

- **Endereçamento.** No modelo de atores, você fala com um ator *específico*, identificado pelo endereço. Em CSP, você fala com um *canal*, e quem está do outro lado é anônimo — qualquer processo pode estar lá.
- **Acoplamento temporal.** Atores são assíncronos com buffer (o mailbox): o emissor não espera. CSP clássico é um rendezvous síncrono: emissor e receptor sincronizam no ponto da troca. (Canais com buffer suavizam isso, mas a alma de CSP é o encontro.)
- **Onde o estado vive.** No modelo de atores, o estado mora *dentro* do ator. Em CSP, o estado vive no processo também, mas a abstração de primeira classe é o *canal*, não o processo.

Uma régua mental: **atores são como mandar uma carta** (endereço, caixa de correio, assíncrono); **CSP é como um telefonema** (linha aberta, os dois presentes, síncrono). Vale revisitar [[12 - Troca de mensagens e CSP]] pra ver o outro lado dessa moeda em detalhe.

## Showcase: Erlang, Elixir e a BEAM

Se CSP tem Go como vitrine, o modelo de atores tem **Erlang** — e sua máquina virtual, a **BEAM**. Erlang nasceu na Ericsson nos anos 80 pra programar centrais telefônicas: sistemas que não podem cair, que rodam por anos, que atualizam sem desligar. O modelo de atores não foi um enfeite acadêmico ali; foi a resposta a um problema de engenharia brutal.

### Processos leves

Na BEAM, o ator se chama **processo** — mas esqueça o processo do sistema operacional. Um processo da BEAM é absurdamente barato: começa com cerca de 1 a 2,5 KB de memória, e a máquina virtual roda **milhões** deles num único nó. Eles são totalmente isolados: cada processo tem seu **próprio heap** e seu **próprio coletor de lixo**.

Esse detalhe do GC por processo é genial. Em runtimes com heap compartilhado, o coletor de lixo às vezes precisa pausar o mundo inteiro. Na BEAM, quando um processo coleta seu lixinho, só ele pausa — os outros milhões seguem. Sem pausas globais. É o isolamento do modelo de atores pagando dividendos até na latência.

O escalonador é preemptivo e justo: a BEAM conta "reduções" (passos de execução) e troca de processo periodicamente, então um processo guloso não trava os vizinhos. Há um escalonador por núcleo de CPU, e o paralelismo entre processos sai de graça.

```mermaid
flowchart TB
    subgraph BEAM["BEAM (uma VM, milhões de processos)"]
        direction LR
        P1[proc. heap próprio<br/>GC próprio]
        P2[proc. heap próprio<br/>GC próprio]
        P3[proc. heap próprio<br/>GC próprio]
        Pn[... milhões ...]
    end
    P1 -.send/receive.-> P2
    P2 -.send/receive.-> P3
    P3 -.send/receive.-> Pn
```

Leitura do diagrama: dentro de uma única instância da BEAM convivem milhões de processos, cada um com heap e GC próprios — caixas estanques. A única ponte entre eles são as setas tracejadas de `send`/`receive`: mensagens assíncronas. Não há memória atravessando as paredes. O isolamento é físico no nível do runtime.

O envio é literal: `Pid ! Mensagem` em Erlang manda um recado pro processo de identificador `Pid`; o `receive` do lado de lá casa padrões nas mensagens da fila. É o modelo de Hewitt quase ao pé da letra.

### "Let it crash" e árvores de supervisão

Aqui mora a contribuição mais contraintuitiva — e mais bonita — da cultura Erlang. A filosofia chama-se **"let it crash"** ("deixe quebrar").

Em quase toda linguagem você aprende a programar *defensivamente*: checar cada entrada, tratar cada erro, blindar cada função contra o inesperado. Erlang vira a mesa. A ideia é: *não* tente prever e tratar todo erro possível dentro do processo. Se algo deu errado de um jeito que você não esperava, deixe o processo **morrer** — e tenha um **supervisor** que o reinicia num estado limpo, conhecido e correto.

```mermaid
flowchart TD
    Sup[Supervisor] -->|monitora| W1[Worker 1]
    Sup -->|monitora| W2[Worker 2]
    Sup -->|monitora| W3[Worker 3]
    W2 -.crash!.-> X((X))
    X -->|notifica supervisor| Sup
    Sup -->|reinicia em estado limpo| W2new[Worker 2 - novo]
```

Leitura do diagrama: o supervisor monitora os workers. O Worker 2 estoura — talvez um dado corrompido, um caso impossível. Em vez de propagar o caos, ele simplesmente morre. O supervisor é notificado, descarta o cadáver e parte um worker novinho, do zero, sem o estado bichado que causou o problema. O sistema se cura sozinho.

> [!tip] Por que "deixar quebrar" funciona
> A intuição parece suicida — "deixar quebrar" soa como desistir. Mas pense: a maioria dos bugs em produção vem de estado corrompido ou de combinações que você nunca imaginou. Tentar tratar o que você não previu é, por definição, impossível. Reiniciar do zero, ao contrário, leva o processo de volta a um estado *conhecido e correto*. Some isso ao isolamento (um processo que morre não derruba os vizinhos) e você tem resiliência por construção, não por heroísmo no código. O segredo não é a ausência de falhas — é o **confinamento** delas.

Os supervisores se organizam em **árvores de supervisão**: supervisores que supervisionam workers e outros supervisores. Quando uma falha não pode ser resolvida no nível baixo, ela *escala* — o supervisor pai reinicia um ramo inteiro, ou repassa o problema pra cima. É uma hierarquia de responsabilidade pela cura, espelhando a hierarquia do sistema.

> [!warning] "Let it crash" não é "deixe tudo quebrar"
> A frase é frequentemente mal entendida. Não significa abandonar validação de entrada do usuário ou ignorar erros esperados — esses você trata normalmente. Significa não escrever código defensivo paranoico contra falhas *inesperadas* e *irrecuperáveis*. Você ainda valida o que é validável; o que você *não* faz é tentar costurar um estado já corrompido de volta à vida.

### OTP, GenServer e a telecom

Toda essa disciplina não fica solta — vem empacotada no **OTP** (Open Telecom Platform), o conjunto de bibliotecas e princípios de design do Erlang. O termo "Erlang" é praticamente intercambiável com "Erlang/OTP". A abstração central é o **GenServer** (*generic server*): um esqueleto de ator com estado que você preenche com *callbacks* — como tratar uma chamada síncrona, um *cast* assíncrono, uma mudança de estado. O GenServer cuida do mailbox, do laço de recepção e da integração com supervisores; você só escreve a lógica.

E o **hot code reload**: a BEAM consegue **trocar o código de um sistema em produção sem desligá-lo**. Você sobe uma nova versão de um módulo (incrementando o `@vsn` e definindo um *callback* `code_change` que migra o estado), e os processos passam a rodar o código novo na próxima mensagem. Pra uma central telefônica que não pode cair, isso não é luxo — é requisito.

O resultado dessa pilha toda virou lenda. Em 1998 a Ericsson lançou o switch **AXD301**, com mais de um milhão de linhas de Erlang, e relatou disponibilidade de **nove noves** — 99,9999999% de uptime. São cerca de 30 milissegundos de indisponibilidade por ano. Esse número é o cartão de visitas do modelo de atores levado a sério.

**Elixir** é a linguagem moderna que roda na mesma BEAM, com sintaxe mais amigável e ferramental atual, herdando OTP, supervisão, "let it crash" e hot reload de graça. E na JVM, o **Akka** é o port mais famoso do modelo de atores — atores como objetos pequenos e *stateful* que só conversam por mensagens assíncronas, sem expor métodos tradicionais.

## Distribuição transparente

Há uma consequência elegante de comunicar só por mensagens endereçadas, e não por memória: o modelo *não se importa onde o ator mora*.

Se A fala com B mandando uma mensagem pro endereço de B, faz diferença se B está no mesmo processo, na mesma máquina ou num data center do outro lado do oceano? Pra A, não. O endereço abstrai a localização. Isso se chama **transparência de localização** (*location transparency*), e é a razão de o modelo de atores se estender naturalmente pra sistemas distribuídos.

No Akka, por exemplo, a forma como os atores interagem é a mesma quer estejam no mesmo host, quer em hosts, núcleos ou nuvens diferentes — quase não há API de rede, só configuração. Você escreve a aplicação como se tudo fosse local; o *deployment* remoto de subárvores de atores vai num arquivo de config. A memória compartilhada nunca te deixaria fazer isso: ponteiro não atravessa a rede. Mensagem, sim.

É aqui que o modelo de atores e os [[03-Dominios/Fundamentos/Redes e Protocolos/index|Redes]] se encontram. Um ator remoto é, no fundo, um endereço pra onde mensagens viajam por TCP em vez de irem pra uma fila local. Mas — e este é o porém honesto — atravessar a rede traz de volta as durezas dos sistemas distribuídos: mensagens podem se perder, chegar fora de ordem, duplicar. A transparência é da *interface*, não da *física*. Você programa igual; só que precisa de protocolos que tolerem perda e reordenação (temas que [[12 - Troca de mensagens e CSP]] tangencia e que voltam em [[17 - Padrões de concorrência]]).

## Prós e contras

Nenhum modelo é grátis. O de atores tem trocas claras.

**A favor:**

- **Sem cadeados, sem race condition por construção.** O estado é confinado; a exclusão mútua é estrutural.
- **Tolerância a falhas.** Isolamento + "let it crash" + supervisão dão resiliência que seria penosa de montar à mão.
- **Escala horizontal.** A transparência de localização leva o mesmo código de um núcleo pra um cluster.
- **Modelo mental claro.** "Pequenos seres que trocam recados" é mais fácil de raciocinar do que um emaranhado de threads e cadeados.

**Contra:**

- **Mailbox sem limite.** Se um ator recebe mensagens mais rápido do que processa, a fila cresce e cresce — até estourar a memória. Isso é um problema de *backpressure*, e a resposta costuma vir do mundo reativo e do [[14 - Loop de eventos e assincronia]]: limitar a fila, descartar, ou empurrar a pressão de volta pro emissor.
- **Debugging de fluxo assíncrono é duro.** Sem pilha de chamadas linear, rastrear "quem mandou o quê pra quem, e em que ordem" exige tracing e correlação. O fire-and-forget que dá liberdade também esconde o fio da meada.
- **Overhead de mensagens.** Copiar e enfileirar mensagens custa mais do que uma chamada de função direta. Pra trabalho fino e fortemente acoplado, atores podem ser pesados demais.
- **Entrega não é garantida de graça.** As mensagens podem se perder ou reordenar — sobretudo no caso distribuído. Garantir entrega exige *protocolo* (acks, timeouts, idempotência), que você precisa construir por cima.

A régua: o modelo de atores brilha onde há **muitas entidades concorrentes, fracamente acopladas, que precisam sobreviver a falhas e escalar** — conexões de usuários, dispositivos IoT, sessões, agentes. Brilha menos em computação numérica fina e fortemente acoplada, onde o overhead de mensagem domina e um modelo de memória compartilhada com paralelismo de dados se sai melhor. Como sempre em [[18 - Concorrência em entrevista]], a resposta certa é "depende da forma da carga".

## Em entrevista

Use estas frases em inglês quando o tema aparecer:

- "The actor model makes each actor own its private state; nothing outside can touch it, so there's no shared mutable state to race over."
- "Actors run concurrently with each other but process their own mailbox one message at a time — concurrency between actors, serialization within each one."
- "Unlike CSP channels, which are anonymous and synchronous, actors have an address and an asynchronous mailbox — you send to a specific actor, fire-and-forget."
- "Erlang's 'let it crash' philosophy means you don't program defensively for every failure; you let the process die and a supervisor restarts it in a clean state."
- "Because actors only talk via messages, the model gives you location transparency — the same code runs whether the actor is local or on another machine."
- "The main trade-offs are unbounded mailboxes needing backpressure, hard async debugging, and the fact that message delivery and ordering aren't guaranteed without a protocol on top."

### Vocabulário

- modelo de atores → actor model
- ator → actor
- estado privado → private state
- caixa de mensagens → mailbox
- "deixe quebrar" → let it crash
- árvore de supervisão → supervision tree
- supervisor → supervisor
- processo leve → lightweight process
- transparência de localização → location transparency
- contrapressão → backpressure
- recarga de código a quente → hot code reload

> [!info] Lastro
> - [Actor model — Wikipedia](https://en.wikipedia.org/wiki/Actor_model) (Hewitt, Bishop e Steiger, 1973; estado privado, mailbox, processar mensagens em série, criar atores, comunicação assíncrona)
> - [Erlang (programming language) — Wikipedia](https://en.wikipedia.org/wiki/Erlang_(programming_language)) (Erlang/OTP, hot code swapping, AXD301 com nove noves de uptime, 1998)
> - [#71: Erlang: let it crash! — Tomasz Nurkiewicz](https://nurkiewicz.com/2022/04/erlang.html) (filosofia "let it crash", supervisão, processos leves e isolados na BEAM)
> - [Location Transparency — Akka core](https://doc.akka.io/docs/akka/current/general/remoting.html) (transparência de localização; mesma interação local ou remota, dirigida por configuração)

## Veja também

- [[12 - Troca de mensagens e CSP]] — o modelo irmão: canais anônimos e rendezvous síncrono
- [[03 - Estado compartilhado e race conditions]] — o problema que os atores eliminam por confinamento
- [[14 - Loop de eventos e assincronia]] — assincronia e backpressure, o calcanhar do mailbox
- [[17 - Padrões de concorrência]] — onde atores viram receitas práticas
- [[18 - Concorrência em entrevista]] — como escolher entre os modelos sob pressão
- [[03-Dominios/Fundamentos/Concorrência e Paralelismo/index|Concorrência e Paralelismo]] — o índice do galho
