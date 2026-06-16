---
title: "Abstrações que vazam"
created: 2026-06-07
updated: 2026-06-16
type: concept
status: seedling
progress: backlog
fase: adepto
tags:
  - fundamentos
  - engenharia-de-software
  - abstracao
  - complexidade-de-software
  - adepto
aliases:
  - Abstrações que vazam
  - Leaky abstraction
  - Abstração vazada
  - Lei das Abstrações Vazadas
  - Law of Leaky Abstractions
publish: false
---

# Abstrações que vazam

Uma abstração **vaza** quando os detalhes internos que ela deveria esconder escapam pela interface — e quem a usa é forçado a entender a camada de baixo pra resolver o problema.

> [!abstract] TL;DR
> Joel Spolsky cunhou a **Lei das Abstrações Vazadas** em 2002: *"All non-trivial abstractions, to some degree, are leaky"* — toda abstração não-trivial vaza em algum grau. A consequência prática é dura: abstrações poupam tempo de **trabalho**, mas não de **aprendizado**. Elas te deixam produtivo no caso comum, mas quando vazam (GC pausando, ORM gerando N+1, GIL serializando threads, slice de Go mutando o array do vizinho), só resolve quem entende o nível de baixo. Não é argumento contra abstrações — é argumento contra a ilusão de que elas dispensam os fundamentos.

## O que é

O termo foi cunhado e popularizado por **Joel Spolsky** no ensaio *The Law of Leaky Abstractions* (Joel on Software, 11/11/2002), com o enunciado:

> [!quote] Lei das Abstrações Vazadas
> *"All non-trivial abstractions, to some degree, are leaky."*
> — Joel Spolsky, 2002

A definição operacional: uma abstração vazada **falha em esconder completamente a complexidade subjacente** que pretendia simplificar. O contrato era "use esta interface simples e ignore o que há embaixo"; o vazamento é o momento em que o que há embaixo afeta o comportamento observável — e ignorá-lo deixa de ser opção.

O fenômeno já tinha sido descrito antes (Gregor Kiczales, *Towards a New Model of Abstraction*, ~1992, sobre abstrações imperfeitas e *open implementation*), mas o nome e a "lei" são de Spolsky.

> [!note] Tensão definicional
> Há duas leituras em disputa. Pra Spolsky, vazar é **propriedade universal** de toda abstração não-trivial — não é defeito, é física. Pra críticos como Haufe (ver [[#Críticas e refinamentos]]), abstração que vaza é só **abstração mal especificada**. A Wikipedia adota a leitura de "design flaw". As duas leituras convivem na literatura; esta nota apresenta ambas.

## A consequência: poupa trabalho, não aprendizado

O ponto central do ensaio não é a lei em si, é o corolário:

> *"The abstractions save us time working, but they don't save us time learning."*

E a única forma de lidar com vazamentos com competência é *"learn about how the abstractions work and what they are abstracting"*. Ou seja: a abstração acelera o caso comum, mas **não te isenta de entender a camada que ela esconde** — porque quando ela vazar (e vai vazar), o debugging acontece no nível de baixo. Paradoxalmente, ferramentas que prometem que você "não precisa saber X" criam o pior cenário: você acaba precisando saber X *e* a ferramenta.

### O exemplo canônico: TCP sobre IP

TCP promete entrega confiável e ordenada — construída sobre IP, que não promete nada (*"TCP is obliged to somehow send data reliably using only an unreliable tool"*). Em condições normais, a mágica funciona. Mas se um cabo é rompido ou a rede congestiona, a não-confiabilidade do IP **atravessa** a abstração: mensagens não chegam, tudo fica lento, conexões caem. TCP não consegue esconder a rede pra sempre — *"sometimes, the network leaks through the abstraction"*. Veja [[Redes e Protocolos]].

## Exemplos por ecossistema

> [!info] Lastro das afirmações
> Os exemplos de **GC (Java/Python)** e **GIL (CPython)** passaram por verificação adversarial contra fontes primárias (docs Oracle, glossário e PEPs do CPython) na pesquisa que alimentou esta nota. Os demais são semântica documentada de cada linguagem (docs oficiais citadas), mas não passaram pelo mesmo crivo — distinção registrada por honestidade epistêmica.

### Java

- **Garbage Collector** — promete "esqueça gerenciamento de memória". Mas *memory leaks continuam existindo* (caches sem limite, listeners não removidos, `ThreadLocal` esquecido — em linguagem com GC, "leak" vira *objeto alcançável-mas-desnecessário*, não ponteiro perdido): a Oracle mantém capítulo oficial de *Troubleshoot Memory Leaks* na doc do Java SE. E as pausas de GC afetam latência a ponto de ZGC e Shenandoah existirem precisamente pra mitigar stop-the-world. Quando o p99 explode, você desce pra [[03 - Garbage Collection — o conceito|o conceito de GC]], [[06 - Os coletores do HotSpot|os coletores]] e [[11 - Tuning de GC — metodologia e prática|tuning]].
- **ORM (Hibernate/JPA)** — promete "trabalhe com objetos, esqueça SQL". Até o problema de **N+1 queries**, a `LazyInitializationException` (proxy lazy acessado fora de sessão) ou a query lenta que exige ler o SQL gerado e o plano de execução. O vazamento dobra a conta: você precisa entender SQL *e* o ORM. O próprio Spolsky já citava ORMs no ensaio original como SQL vazando por strings de query.
- **JIT** — promete "performance transparente". Mas warmup (o código começa interpretado), *deoptimizations* e limites de inlining fazem a performance variar de formas que só se explicam descendo pra [[07 - JIT — C1, C2 e tiered compilation|C1/C2 e tiered compilation]].

### TypeScript

- **Type erasure** — o sistema de tipos promete segurança, mas **não existe em runtime**: os tipos são apagados na compilação. Um `as User` num JSON vindo da rede não valida nada — o objeto errado atravessa o "tipo" e explode longe dali. O vazamento força a entender que TS é uma camada estática sobre JavaScript dinâmico (daí validadores de runtime como Zod existirem).
- **`async/await` sobre o event loop** — a sintaxe promete "código assíncrono que parece síncrono". Mas um loop CPU-bound dentro de uma função `async` ainda **bloqueia o event loop inteiro** — `await` não cria thread, só agenda continuação. Quem não entende o event loop não explica por que o servidor "travou" com código aparentemente assíncrono.
- **Tipagem estrutural** — duas interfaces sem relação nominal são intercambiáveis se as formas coincidem; o "tipo errado" passa silenciosamente onde uma linguagem nominal acusaria.

### Go

- **Slices e o array subjacente** — slice promete "array dinâmico simples", mas é uma *view* `(ptr, len, cap)` sobre um array compartilhado. Dois slices podem **aliasar o mesmo array**: um `append` dentro da capacidade muta dados que outro slice enxerga; um `append` que estoura a capacidade realoca e *des*-compartilha silenciosamente. O comportamento só faz sentido entendendo a mecânica interna (documentada no Go Blog, *Go Slices: usage and internals*).
- **Interface com typed nil** — uma interface guardando um ponteiro nil (`(*T)(nil)`) **não compara igual a `nil`**: a interface só é nil se tipo *e* valor forem nil. O clássico `return err` que nunca é nil vaza a representação interna de interfaces (par tipo/valor), documentado no FAQ oficial de Go.
- **Goroutines e o scheduler** — prometem "concorrência barata, esqueça threads". Mas chamadas de sistema bloqueantes, CGO e loops sem pontos de preempção interagem com o scheduler M:N de formas que exigem entender Ps, Ms e Gs quando a latência degrada.

### Python

- **GIL** — a API de `threading` promete paralelismo, mas o *Global Interpreter Lock* permite **uma thread executando bytecode por vez**: programas CPU-bound multi-thread são efetivamente single-threaded (no benchmark da Real Python: ~6,2s com 1 thread, ~6,9s com 2 — *mais lento*, pelo overhead do lock). A causa é um detalhe de implementação do CPython: o *reference counting* precisava de proteção contra races, e um lock global foi mais barato que locks por objeto. Vazamento de manual: um detalhe interno do interpretador dita a arquitetura do seu código (multiprocessing vs threading). **Caveat temporal**: desde o 3.13 existe build *free-threaded* opt-in (PEP 703), oficial no 3.14 (PEP 779) — mas o build padrão em 2026 ainda tem GIL.
- **GC + ciclos de referência** — o reference counting libera a maioria dos objetos, mas ciclos exigem o coletor geracional — e pausas em heaps grandes motivaram o GC **incremental** do 3.14. O "esqueça memória" vaza igual ao Java.
- **Interning de inteiros pequenos** — CPython mantém cache dos ints de -5 a 256; `a is b` dá `True` pra `256` e `False` pra `257`. O operador `is` vaza o modelo de objetos do interpretador — por isso a regra "compare valores com o operador de igualdade (`a == b`), use `is` só pra `None`".

## Conceitos vizinhos

- **Information hiding (Parnas, 1972)** — o contraponto prescritivo direto. Em *On the Criteria To Be Used in Decomposing Systems into Modules* (CACM 15(12), 1972; precursor no paper IFIP de 1971), David Parnas define que cada módulo deve **esconder uma decisão de design propensa a mudar** — não meramente "esconder dados". Abstração que vaza é precisamente uma *falha de information hiding*: a decisão volátil escapou e o cliente passou a depender dela.
- **Encapsulamento** — o mecanismo de linguagem (visibilidade, interfaces) que tenta implementar information hiding. Vazamento acontece *apesar* do encapsulamento: o compilador esconde o campo, mas não esconde o comportamento (latência, ordem, falha). Veja [[Orientação a Objetos]].
- **Lei de Hyrum** — o extremo lógico do vazamento: *"With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody."* Com usuários suficientes, **toda a implementação vira interface implícita** — alguém depende até dos seus bugs. A própria página canônica (hyrumslaw.com) cita Spolsky como mecanismo: a lei de Hyrum é o que acontece quando os vazamentos ganham dependentes em escala (Google a registra em *Software Engineering at Google*, cap. 1).

A cadeia conceitual: Parnas prescreve o que esconder → Spolsky observa que o esconderijo sempre vaza um pouco → Hyrum observa que, em escala, tudo que vazou vira contrato.

## Críticas e refinamentos

- **Haufe (2019) — "leaky abstractions are just bad abstractions"**: Michael L. Haufe rejeita a lei argumentando que os exemplos de Spolsky são um *straw man* — atribuem às abstrações garantias que elas nunca prometeram (TCP não promete entrega *incondicional*; promete confiabilidade *enquanto a conexão existir*). Abstração que cumpre sua especificação não "vaza"; a que vaza estava mal especificada. Pra Haufe, perpetuar a lei *"is actively harmful to the industry"* porque normaliza especificações ruins.
- **Principles Wiki — de lei descritiva a princípio prescritivo**: a lei de Spolsky *descreve* um efeito; como princípio de engenharia, ela vira três estratégias quando um vazamento dói: **(1)** redesenhar a abstração pra vazar menos; **(2)** trocá-la por uma abstração melhor; **(3)** *remover* a abstração quando os vazamentos custam mais do que ela economiza — com alerta explícito contra empilhar frameworks uns sobre os outros (cada camada empilhada soma os vazamentos de todas as de baixo).
- **Jeff Atwood — *All Abstractions Are Failed Abstractions*** (Coding Horror, 2009): estende a tese com exemplos de LINQ-to-SQL, no espírito de Spolsky.

## Como projetar abstrações que vazam menos

- **Especifique o contrato de verdade** (resposta à crítica de Haufe): diga o que a abstração *não* promete — limites, modos de falha, custos. Vazamento surpreende menos quando está documentado como comportamento.
- **Esconda decisões, não apenas dados** (Parnas): pergunte "que decisão volátil este módulo protege?" — se a resposta vazar pela API (nomes, tipos, ordem de chamadas), a troca futura da decisão quebra os clientes.
- **Ofereça *escape hatches* deliberados**: uma porta explícita pro nível de baixo (o `unwrap()` da conexão crua, o `nativeQuery` do ORM) é melhor que forçar o usuário a contornar a abstração por fora quando ela não basta.
- **Não empilhe frameworks**: cada camada soma os vazamentos das de baixo; profundidade de pilha é custo, não arquitetura.
- **Minimize a superfície observável** (defesa contra Hyrum): quanto menos comportamento observável, menos coisas pra alguém depender — randomize o que não é prometido (ordem de iteração, formatos internos), ou alguém vai cravar dependência nele.
- **Saiba quando *não* abstrair**: se os usuários precisam descer o tempo todo, a abstração virou pedágio — removê-la é uma das três estratégias legítimas.

## Armadilhas comuns

- **Acreditar que a ferramenta dispensa o fundamento** — o ORM não dispensa SQL, o GC não dispensa modelo de memória, o `async` não dispensa o event loop. É exatamente o erro que a lei denuncia.
- **Culpar a abstração por promessa que ela não fez** — antes de declarar vazamento, leia a especificação: às vezes o "vazamento" é contrato documentado que ninguém leu (o ponto de Haufe).
- **Resolver vazamento com mais uma camada** — embrulhar uma abstração vazada em outra abstração soma vazamentos em vez de eliminá-los.
- **Depender do que vazou** — usar comportamento interno observável (interning de ints, ordem de iteração, SQL gerado) como se fosse contrato; é assim que se vira estatística da lei de Hyrum.

## Referências

- **Joel Spolsky** — [The Law of Leaky Abstractions](https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/) (Joel on Software, 11/11/2002) — o ensaio fundador.
- **Hyrum Wright / Titus Winters** — [Hyrum's Law](https://www.hyrumslaw.com/) — página canônica; também em *Software Engineering at Google* (O'Reilly, 2020, cap. 1).
- **David Parnas** — [On the Criteria To Be Used in Decomposing Systems into Modules](https://dl.acm.org/doi/10.1145/361598.361623) (CACM 15(12), 1972) — information hiding.
- **Michael L. Haufe** — [Leaky Abstractions Are Just Bad Abstractions](https://thenewobjective.com/requirements-engineering/leaky-abstractions-are-just-bad-abstractions/) (2019) — a crítica direta.
- **Principles Wiki** — [Law of Leaky Abstractions](http://www.principles-wiki.net/principles:law_of_leaky_abstractions) — leitura prescritiva e as três estratégias.
- **Jeff Atwood** — [All Abstractions Are Failed Abstractions](https://blog.codinghorror.com/all-abstractions-are-failed-abstractions/) (Coding Horror, 2009).
- **Oracle** — [Troubleshoot Memory Leaks](https://docs.oracle.com/en/java/javase/25/troubleshoot/troubleshooting-memory-leaks.html) (Java SE 25) — leaks apesar do GC.
- **Real Python** — [What Is the Python GIL?](https://realpython.com/python-gil/) + [PEP 703](https://peps.python.org/pep-0703/) e [free-threading HOWTO](https://docs.python.org/3/howto/free-threading-python.html) — o GIL e sua remoção opt-in.
- **Go Blog** — [Go Slices: usage and internals](https://go.dev/blog/slices-intro) — a mecânica `(ptr, len, cap)`.
- **Total TypeScript** — [TypeScript Types Don't Exist at Runtime](https://www.totaltypescript.com/typescript-types-dont-exist-at-runtime) — type erasure.
- **Gregor Kiczales** — *Towards a New Model of Abstraction in Software Engineering* (~1992) — precursor acadêmico (*open implementation*).

## Veja também

- [[05 - Abstração - a ferramenta central]] — a abstração e o information hiding que esta lei mostra vazando
- [[07 - Módulos profundos e rasos]] — como dimensionar abstrações (interface simples, muita funcionalidade)
- [[Redes e Protocolos]] — TCP/IP, o exemplo canônico da lei
- [[Orientação a Objetos]] — encapsulamento, o mecanismo que o vazamento atravessa
- [[03 - Garbage Collection — o conceito]] — a abstração de memória da JVM por dentro
- [[07 - JIT — C1, C2 e tiered compilation]] — por que a performance "transparente" varia
- [[O programa como teoria]] — outro fundamento sobre o que o código esconde: o entendimento mora nas pessoas
- [[Dicionário de Fundamentos#Abstração que vaza (leaky abstraction)|Verbete no Dicionário de Fundamentos]]
