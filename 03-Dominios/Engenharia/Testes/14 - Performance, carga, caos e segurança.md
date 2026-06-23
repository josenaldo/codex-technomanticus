---
title: "Performance, carga, caos e segurança"
created: 2026-06-18
updated: 2026-06-18
type: concept
fase: magus
status: evergreen
publish: false
tags:
  - engenharia
  - testes
  - performance
  - seguranca
  - entrevista
---

# Performance, carga, caos e segurança

> [!abstract] Resumo em uma linha
> Testes funcionais perguntam "está correto?"; estes perguntam "aguenta?", "quão rápido?", "sobrevive à falha?" e "é seguro?" — e cada pergunta tem sua própria ferramenta e seu próprio momento de maturidade.

Toda a [[02 - A pirâmide de testes e suas variações|pirâmide de testes]] que vimos até aqui responde a uma única pergunta: **o código faz a coisa certa?** Unit, integração, e2e — todos checam *correção*. Mas um sistema pode estar 100% correto e ainda assim cair na Black Friday, vazar dados ou levar 8 segundos pra carregar.

Existe uma família inteira de testes que **não olha pra correção**. Olha pra *qualidade não-funcional*: velocidade, capacidade, resiliência, segurança. São testes que medem **limites** e **comportamento sob estresse**, não saídas esperadas.

A analogia que cola: pense no **crash test de carro**. Ninguém bate um carro contra a parede pra descobrir se o motor liga — isso é teste funcional. Bate-se de propósito pra descobrir *o que acontece quando o pior acontece*: o chassi amassa do jeito certo? O airbag dispara? A coluna de direção recua em vez de empalar o motorista? Você quebra a coisa de propósito, num ambiente controlado, **pra aprender antes que aconteça de verdade**.

## A diferença-chave

| Pergunta | Tipo de teste | O que mede |
|---|---|---|
| Está correto? | Funcional (unit/integração/e2e) | Saída == esperado |
| Quão rápido é este trecho? | **Microbenchmark** | Latência de uma função |
| Aguenta a carga esperada? | **Load test** | Latência e throughput sob N usuários |
| Onde quebra, e como? | **Stress test** | Ponto de ruptura e tipo de degradação |
| Sobrevive a falhas reais? | **Chaos engineering** | Resiliência sob injeção de falha |
| É seguro? | **Security testing** | Vulnerabilidades no código e nas deps |

> [!tip] A regra mental
> Se o teste tem um `assert resultado == esperado`, é funcional. Se o teste tem um *gráfico* (latência ao longo do tempo, requisições por segundo, p99), é não-funcional. Funcional dá verde ou vermelho; não-funcional dá uma **curva** que você interpreta.

## Microbenchmark — medir um trecho com precisão cirúrgica

Você quer saber: esta função de parsing leva 12ns ou 120ns? Esta troca de `ArrayList` por `LinkedList` ajudou? Microbenchmark mede **um trecho minúsculo de código**, isolado, com precisão de nanossegundos.

E aqui mora um campo minado. Medir tempo na JVM ingenuamente — `long t = System.nanoTime(); foo(); System.nanoTime() - t;` — produz **números que mentem**. Por quê?

> [!danger] As três armadilhas clássicas do microbenchmark na JVM
> - **JIT warmup.** O código roda interpretado no começo; só depois de ~10.000 invocações o JIT compila pra código de máquina otimizado. Se você mede *antes* do steady state, mistura modos de execução numa média sem sentido — mede o interpretador, não o código real de produção.
> - **Dead-code elimination (DCE).** Se o resultado do cálculo nunca é usado, o compilador é livre pra *apagar o cálculo inteiro*. Você mede uma função que o JIT deletou — e cronometra um loop vazio. É a armadilha mais perigosa, porque o número parece ótimo (e é zero útil).
> - **Constant folding.** Se a entrada é constante, o JIT pré-computa o resultado em tempo de compilação. Você mede uma leitura de constante, não a computação.

A resposta para isso é o **JMH** (Java Microbenchmark Harness), parte do projeto OpenJDK. Ele resolve cada armadilha:

- Roda iterações de **warmup** descartadas antes de medir, garantindo que o JIT já compilou tudo.
- Oferece o **`Blackhole`**: você passa o resultado para `blackhole.consume(x)`, e o JIT *não pode* eliminar o cálculo, porque o resultado "escapa". Mata o DCE.
- Roda múltiplos **forks** (JVMs separadas) pra evitar que o perfil de compilação de um benchmark contamine o outro, e reporta com desvio.

```java
@Benchmark
@Warmup(iterations = 5)
@Measurement(iterations = 10)
@Fork(3)
public void medeParse(Blackhole bh) {
    bh.consume(parser.parse(ENTRADA)); // consume() impede o JIT de apagar o parse
}
```

> [!warning] Não confie em `System.nanoTime()` ingênuo
> Microbenchmark feito à mão na JVM é quase sempre errado — e o pior é que ele *parece* funcionar. Detalhes na nota [[Testes em Java]]. Em outras linguagens o nome muda (Google Benchmark em C++, `criterion` em Rust/Python, `BenchmarkDotNet` em .NET), mas as três armadilhas são universais: warmup, eliminação de código morto, e medir o que não importa.

## Fuzzing — jogar lixo na entrada até algo quebrar

Antes de medir velocidade ou carga, vale uma técnica que mora na fronteira entre teste e segurança: o **fuzzing**. A ideia é quase boba de tão direta — em vez de escrever entradas cuidadosas, você **bombardeia a função com entradas malformadas, aleatórias, gigantes, vazias, com caracteres estranhos**, milhões delas, e vê o que faz o programa *crashar*, travar, vazar memória ou se comportar errado. Não há `assert resultado == esperado`; o oráculo é mais cru: **o programa não devia morrer com nenhuma entrada, por mais idiota que ela seja**.

A versão ingênua — gerar bytes aleatórios e torcer — é fraca. A entrada aleatória quase sempre é rejeitada logo no primeiro `if` de validação e nunca alcança o código profundo onde mora o bug. A evolução que mudou o jogo é o **coverage-guided fuzzing** (fuzzing guiado por cobertura): o programa é **instrumentado** pra reportar quais caminhos cada entrada exercita, e o fuzzer trata isso como um **algoritmo genético**. A "seleção natural" é a cobertura — quando uma entrada mutada alcança um trecho de código *novo*, o fuzzer a guarda no corpus e a usa como base pra novas mutações. Aos poucos, ele "aprende" a forma da entrada e penetra fundo no código, sem nunca ter visto a gramática do formato.

Lead-in: o diagrama abaixo mostra esse laço de retroalimentação que separa o fuzzing moderno do aleatório burro.

```mermaid
flowchart TD
    A["Corpus de entradas<br/>(sementes iniciais)"] --> B["Escolhe uma entrada<br/>e aplica mutação<br/>(bit flip, splice, ...)"]
    B --> C["Roda o programa<br/>instrumentado"]
    C --> D{"Crash, hang<br/>ou erro de sanitizer?"}
    D -->|"sim"| E["Salva como bug<br/>(entrada que reproduz)"]
    D -->|"não"| F{"Alcançou cobertura<br/>de código nova?"}
    F -->|"sim"| G["Adiciona ao corpus<br/>(semente promissora)"]
    F -->|"não"| H["Descarta a entrada"]
    G --> B
    H --> B
```

Leitura do diagrama: o coração é o losango F — *alcançou cobertura nova?*. Entradas que abrem caminhos inéditos viram sementes (G) e se reproduzem; as que não rendem nada são descartadas (H). É o que torna o fuzzing **direcionado** em vez de cego: ele não busca o bug, busca *código ainda não explorado*, e o bug aparece como subproduto. Quando casa com um **sanitizer** (AddressSanitizer detecta acesso fora dos limites, leak de memória), o losango D dispara em corrupções que nem chegariam a crashar sozinhas.

As ferramentas canônicas: **AFL / AFL++** (instrumentação em tempo de compilação, processo externo) e **libFuzzer** (in-process, integrado ao LLVM e aos sanitizers). O ponto de entrada do libFuzzer é minúsculo — você só escreve a função que recebe os bytes e os joga no código sob teste:

```cpp
// libFuzzer: o harness é só isto. O fuzzer cuida das mutações e da cobertura.
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    minha_funcao_de_parse(data, size); // crash/leak aqui vira um bug reportado
    return 0;
}
```

Por cima dessas engines, o **OSS-Fuzz** do Google roda fuzzing *contínuo* em centenas de projetos open-source críticos — e já encontrou **dezenas de milhares** de bugs e vulnerabilidades em coisas como OpenSSL, SQLite e curl. Fuzzing não é um teste que roda uma vez; é uma infraestrutura que roda pra sempre.

> [!tip] Fuzzing é primo do property-based testing — e do crash test de carro
> Repare o parentesco com o [[13 - Além do básico - property-based, snapshot, contract, smoke|property-based testing]]: ambos *geram* entradas em vez de você escrevê-las à mão. A diferença é o oráculo. No property-based, você afirma uma **propriedade** ("ordenar e reverter == reverter e ordenar") e a entrada gerada respeita uma gramática. No fuzzing, a propriedade implícita é mais humilde — "**não crashe**" — e a entrada é caótica de propósito, pra estressar o parser. Por isso o fuzzing pende pro lado da **segurança**: as entradas malformadas que ele encontra são exatamente os payloads que um atacante usaria pra causar um buffer overflow ou um DoS. É o crash test do carro aplicado à camada de entrada: bater de propósito, com lixo, pra descobrir onde o chassi do parser amassa.

## Load testing — simular a carga esperada

Microbenchmark olha uma função. **Load testing** olha o sistema inteiro de fora, simulando **usuários concorrentes** batendo na API como bateriam em produção num dia normal.

A pergunta é: com 500 usuários simultâneos (a carga que esperamos no pico), **a latência continua aceitável?** O throughput segura? Aqui você não olha média — olha **percentis**, exatamente como discutimos em [[03-Dominios/Ciência/Redes e Protocolos/12 - Latência, throughput e os números|latência e throughput]]. A média esconde o sofrimento; o **p95 e o p99** revelam a experiência da cauda — aqueles 1% de requisições que travam e geram tickets.

Ferramentas: **k6** (scripts em JavaScript, ótimo pra CI), **Gatling** (Scala/DSL), **JMeter** (GUI clássico, Java). O script descreve um perfil de carga: rampa de subida, platô no nível esperado, descida.

```javascript
// k6: rampa até 500 VUs, segura 5min, com SLO no p95
export const options = {
  stages: [
    { duration: '2m', target: 500 },  // sobe
    { duration: '5m', target: 500 },  // platô na carga esperada
    { duration: '2m', target: 0 },    // desce
  ],
  thresholds: { http_req_duration: ['p(95)<400'] }, // SLO: p95 abaixo de 400ms
};
```

> [!note] Load test valida um SLO, não acha o limite
> O objetivo do load test é confirmar que, **na carga que você espera**, o sistema cumpre seus acordos de nível de serviço. Ele não te diz onde o sistema quebra — pra isso é o próximo.

### O load test valida um orçamento, não um número redondo

O júnior pensa em load test como "aguenta 1000 RPS?". O sênior reformula: load test **não é sobre throughput, é sobre o contrato de latência**. A pergunta certa não é "aguenta X requisições por segundo?", e sim "**o p99 fica abaixo de Y ms enquanto serve X RPS?**". Throughput sozinho é vaidade — um sistema que serve 5.000 RPS com p99 de 9 segundos está, na prática, fora do ar.

É aqui que o load test encosta na disciplina de SRE. Um **SLO** (Service Level Objective) é o alvo interno: "99% das requisições abaixo de 300ms, medido sobre 30 dias". Dele nasce o **orçamento de erro** (error budget): se a meta é 99,9% de disponibilidade, o orçamento é 0,1% — algo como ~43 minutos de degradação por mês que você *pode gastar* sem violar o acordo. Acima do SLO está o **SLA** (Service Level Agreement), a promessa contratual ao cliente, com multa se quebrar — sempre mais frouxo que o SLO interno, pra dar margem.

E por que **percentis**, nunca média? Porque média esconde a cauda. Como vimos em [[03-Dominios/Ciência/Redes e Protocolos/12 - Latência, throughput e os números|os números de latência]], um serviço com média de 100ms pode ter 5% das requisições em 2 segundos — e esses 5% são justamente os usuários que abrem ticket. O p99 mostra o pior caso plausível; a média mostra um caso que talvez não exista. Por isso o `threshold` do k6 lá em cima é `p(95)<400`, não `avg<400`: o teste de carga **codifica o SLO como uma asserção** e o pipeline falha se a cauda estourar o orçamento.

> [!tip] O load test é o guardião do orçamento de latência
> Toda vez que você sobe uma versão nova, o load test responde: "essa mudança gastou orçamento de erro?". Se o p99 subiu de 280ms pra 350ms num SLO de 300ms, você acabou de estourar o budget num teste — antes de estourar em produção e queimar a confiança do cliente.

## Stress testing — empurrar até quebrar

Aqui muda a intenção. Load test pergunta "aguenta o esperado?". **Stress test pergunta "qual é o esperado *máximo*? Onde quebra? E como quebra?"**. Você empurra carga *além* do normal, subindo até o sistema ceder, pra achar o **ponto de ruptura** e — crucialmente — observar o **tipo de degradação**.

Lead-in: o diagrama abaixo mostra a carga subindo continuamente e os três regimes que o sistema atravessa até o colapso.

```mermaid
flowchart LR
    A["Carga baixa<br/>latência estável"] -->|sobe carga| B["Carga esperada<br/>p95 dentro do SLO"]
    B -->|continua subindo| C["Joelho da curva<br/>latência dispara,<br/>throughput estagna"]
    C -->|ultrapassa o limite| D{"Ponto de<br/>ruptura"}
    D -->|"degradação<br/>graciosa"| E["Rejeita excesso,<br/>core sobrevive<br/>(HTTP 503, fila, backpressure)"]
    D -->|"degradação<br/>catastrófica"| F["Cascata de falhas,<br/>timeouts, OOM,<br/>tudo cai junto"]
```

Leitura do diagrama: enquanto a carga é baixa ou esperada (A → B), a latência fica plana. No **joelho da curva** (C), cada usuário a mais faz a latência disparar e o throughput parar de crescer — o sistema está saturado. Passado o **ponto de ruptura** (D), há dois destinos possíveis. A bifurcação E × F é o que o stress test existe pra revelar:

- **Degradação graciosa** (E): o sistema *sabe* que está sobrecarregado e rejeita o excesso de forma controlada — retorna 503, aplica backpressure, enfileira. O núcleo continua de pé. Esse é o comportamento que você *quer*.
- **Degradação catastrófica** (F): uma falha derruba a próxima numa **cascata** — um pool de conexões esgota, timeouts em cadeia, `OutOfMemoryError`, e o sistema inteiro cai. Esse é o comportamento que você quer *descobrir num teste*, não numa madrugada de produção.

### Degradação graciosa é uma propriedade testável

O insight que separa o stress test maduro do amador: o **ponto de ruptura** (a curva D) importa muito menos que o **modo de ruptura**. Saber que o sistema cede em 8.000 RPS é um número; saber *como* ele cede é uma propriedade de design — e essa propriedade pode (e deve) ser asserida.

A **degradação graciosa** é precisamente isso: a capacidade de, ao saturar, **rejeitar trabalho de forma controlada em vez de derreter**. Na prática significa devolver `503 Service Unavailable` com um header `Retry-After` (dizendo ao cliente "volte em 5s") em vez de aceitar a requisição, segurá-la numa fila infinita e estourar o pool de threads. Significa **load shedding** — descartar deliberadamente o excesso pra proteger o núcleo — em vez de tratar todo mundo igual e cair com todo mundo junto.

Aqui o stress test encosta diretamente nos padrões de [[03-Dominios/Ciência/Redes e Protocolos/14 - Resiliência de rede|Resiliência de rede]]. O **circuit breaker** que abre quando um dependente engasga, o **bulkhead** que isola pools pra que a saturação de um não afunde os outros, o **load shedding** que sacrifica requisições não-essenciais — todos esses mecanismos só *existem* pra produzir degradação graciosa sob estresse. E o stress test é o juiz: ele não pergunta apenas "quebrou?", pergunta "**ao quebrar, devolveu 503 limpo ou entrou em colapso em cascata?**". Você pode literalmente escrever a asserção: "acima do ponto de ruptura, a taxa de 503 deve subir mas o p99 das requisições *aceitas* deve permanecer abaixo do SLO". Isso transforma resiliência de uma promessa de arquitetura num resultado mensurável.

Duas variações de stress test que aparecem de passagem:

> [!example] Spike e soak
> - **Spike test**: em vez de subir a carga em rampa, você *dispara* um pico gigante e instantâneo (de 50 pra 5.000 usuários em segundos) e vê se o sistema sobrevive e se *recupera*. Simula o tweet viral, o post que bombou.
> - **Soak test** (endurance): mantém uma carga moderada por *horas*. Existe pra caçar problemas que só aparecem com tempo — **vazamento de memória**, conexões que não fecham, logs enchendo o disco. Um sistema pode passar no load test de 10 minutos e morrer no soak de 8 horas.

## Chaos engineering — quebrar de propósito, em produção

Os testes acima rodam num ambiente controlado, contra carga sintética. **Chaos engineering** vira a mesa: injeta falhas reais — mata uma instância, adiciona latência de rede, descarta pacotes — **no sistema rodando**, às vezes em produção, pra validar que ele realmente aguenta o que você *jura* que ele aguenta.

A Netflix, que cunhou a prática, define como "a disciplina de experimentar num sistema distribuído pra construir confiança na sua capacidade de suportar condições turbulentas em produção". A ferramenta seminal é o **Chaos Monkey** (2012), parte da *Simian Army*: ele **mata instâncias aleatoriamente** durante o horário comercial.

> [!quote] Por que matar máquinas no horário comercial?
> A lógica é brilhante e contraintuitiva: a falha *vai* acontecer um dia. A pergunta é só *quando* você descobre que seu sistema não a tolera. Melhor descobrir às 14h de uma terça, com toda a equipe acordada e cafeinada, do que às 3h de um domingo. Chaos engineering força a falha para o horário comercial.

O método é experimental, não aleatório. Você forma uma **hipótese sobre o estado estável** (steady state) — para a Netflix, "streams por segundo" (SPS). Mede esse estado por throughput, taxa de erro e percentis de latência. Injeta a falha. Vê se a métrica de steady state se desvia. Se não desviou, ganhou confiança. Se desviou, achou uma fraqueza pra corrigir.

Lead-in: o ciclo do chaos é um loop de aprendizado, não um teste de aprovar/reprovar.

```mermaid
flowchart TD
    A["Define o estado estável<br/>(ex: streams/seg, p99, erro%)"] --> B["Forma hipótese:<br/>'o sistema mantém o estado<br/>estável mesmo se X falhar'"]
    B --> C["Injeta a falha<br/>(mata instância, +latência,<br/>perda de pacote)"]
    C --> D{"O estado estável<br/>se manteve?"}
    D -->|"sim"| E["Confiança ganha<br/>a resiliência existe"]
    D -->|"não"| F["Fraqueza descoberta<br/>corrige o sistema"]
    F --> B
    E --> G["Aumenta o raio de impacto<br/>(blast radius), repete"]
    G --> C
```

Leitura do diagrama: o coração é o losango D — *o estado estável se manteve?*. Se sim, você aumenta o **raio de impacto** (blast radius) e testa algo mais agressivo. Se não, você corrige e volta a hipotetizar. Nunca é "passou/falhou": é um ciclo que **expande a confiança** enquanto controla o dano potencial.

Repare a conexão direta com o que vimos em redes. Chaos engineering é o teste *prático* dos padrões de [[03-Dominios/Ciência/Redes e Protocolos/14 - Resiliência de rede|Resiliência de rede]] — circuit breaker, retry com backoff, timeout, bulkhead. De que adianta ter um circuit breaker no código se ninguém nunca verificou que ele *abre* quando o dependente cai? O chaos injeta a falha pra provar que a resiliência configurada funciona de verdade.

> [!warning] Chaos é pra quem tem maturidade — e infra distribuída
> Não comece por aqui. Matar instâncias em produção só faz sentido quando você já tem: observabilidade decente (pra detectar o desvio), redundância (pra sobreviver à falha injetada), e um sistema *distribuído* onde a falha de um nó deveria ser absorvida. Em um monólito sem réplica, chaos engineering só causa downtime. Times maduros têm ferramentas modernas (Gremlin, Litmus, AWS Fault Injection Service) com controle fino de blast radius e botão de pânico.

### O método importa mais que a ferramenta

A confusão fatal é tratar chaos engineering como "quebrar coisas pra ver o que acontece". Isso é vandalismo, não engenharia. A disciplina é **rigorosamente científica** — os *Principles of Chaos Engineering* a definem como um experimento controlado com quatro passos: (1) defina o estado estável por métricas de negócio; (2) **hipotetize** que esse estado se mantém tanto no grupo de controle quanto no experimental; (3) injete eventos do mundo real (crash de servidor, partição de rede, falha de disco); (4) tente *refutar* a hipótese comparando o estado estável entre controle e experimento. Sem hipótese antes do experimento, você não tem chaos engineering — tem um incidente autoinfligido.

Dois conceitos operacionais governam a maturidade:

- **Game day.** É o chaos engineering feito como *evento planejado*: uma janela agendada, uma hipótese escrita, um blast radius decidido de antemão, **critério de aborto** definido ("se o p99 dobrar, paramos") e a equipe inteira de prontidão observando. O game day é o oposto do Chaos Monkey rodando solto — é o ensaio deliberado de um cenário de falha, com toda a sala assistindo, pra exercitar tanto o sistema *quanto* a resposta humana (runbooks, alertas, on-call).
- **Blast radius (raio de explosão).** A regra de ouro: **comece pequeno e expanda só com confiança**. Um shard, uma célula, uma zona, ou 1% do tráfego primeiro. Só depois de várias execuções verdes você amplia o raio. Isso é o que separa o experimento responsável da roleta russa: você controla *quanto dano* o experimento pode causar antes de saber se o sistema aguenta. O loop do diagrama acima já mostra isso — só se aumenta o blast radius (G) depois que a hipótese se confirma (E).

Repare que estado estável, hipótese e blast radius reaproveitam exatamente o vocabulário do método científico: observação → hipótese → experimento controlado → comparação. A diferença é que o laboratório é o seu sistema de produção, e o controle de variáveis é o blast radius.

## Security testing — caçar vulnerabilidades, não bugs

A última pergunta não-funcional: **é seguro?** Aqui não se mede tempo nem carga — se procura **vulnerabilidades** que um atacante exploraria. Há três famílias complementares, e a confusão entre elas é clássica em entrevista.

| Sigla | O que é | Quando age | Acha |
|---|---|---|---|
| **SAST** | Static Application Security Testing | No código, sem rodar | Falhas no código que *você* escreveu (injeção, lógica, overflow) |
| **DAST** | Dynamic Application Security Testing | Na app *rodando* | Falhas visíveis de fora, atacando como um hacker |
| **SCA** | Software Composition Analysis / dependency scanning | Nas dependências | Vulnerabilidades nas libs que você *importou* |

- **SAST** analisa o código-fonte linha por linha, *antes* de compilar ou rodar, contra um banco de padrões perigosos (frequentemente alinhado ao **OWASP Top 10** e ao CWE). É o mais "shift-left" de todos — roda no IDE e no commit.
- **DAST** ataca a aplicação *em execução*, de fora pra dentro, como faria um invasor: injeta payloads, testa endpoints, sonda respostas. Roda assim que a app sobe em staging.
- **SCA / dependency scanning** monta o **bill of materials** (lista de pacotes) e cruza cada um com bases de CVEs conhecidos. É aqui que vivem **Dependabot**, **Snyk** e o **OWASP Dependency-Check**. Lembre que a maioria das brechas modernas vem de uma lib transitiva desatualizada, não do seu código — daí o peso do SCA.

O fio condutor é o **shift-left**: empurrar a segurança pra *cedo* no ciclo, dentro do CI, pra pegar o problema antes de chegar à produção (onde corrigir custa muito mais). Veremos a mecânica no pipeline em [[15 - Testes em CI-CD]].

Lead-in: o diagrama posiciona cada análise no momento certo do pipeline.

```mermaid
flowchart LR
    A["Dev escreve código"] --> B["SAST<br/>analisa o código<br/>(IDE / commit)"]
    A --> C["SCA<br/>varre dependências<br/>(no build)"]
    B --> D["Build e deploy<br/>em staging"]
    C --> D
    D --> E["DAST<br/>ataca a app rodando<br/>(staging)"]
    E --> F{"Vulnerabilidade<br/>crítica?"}
    F -->|"sim"| G["Falha o pipeline<br/>bloqueia o merge/deploy"]
    F -->|"não"| H["Promove pra produção"]
```

Leitura do diagrama: SAST e SCA agem **cedo e sem rodar a app** (análise estática do código e das deps), em paralelo, no commit/build. DAST age **depois**, porque precisa da app *de pé* pra atacá-la. O losango F é o portão: vulnerabilidade crítica **quebra o build**, exatamente como um teste vermelho. Segurança vira parte do gate de qualidade, não um checklist manual no fim do trimestre.

### Scanner automático × teste de invasão humano

SAST, DAST e SCA são todos **scanners automáticos**: rápidos, repetíveis, rodando a cada commit, lançando uma rede ampla sobre vulnerabilidades *conhecidas* — padrões catalogados no OWASP Top 10, CVEs publicados, configurações erradas comuns. São excelentes naquilo em que máquinas brilham: cobertura e consistência. Mas têm um teto fundamental — **não pensam**.

O **teste de invasão** (penetration test, ou pentest) preenche essa lacuna. É **humano, periódico e criativo**: um especialista (red team) ataca o sistema como um adversário real ataparia. A diferença não é só "manual em vez de automático" — é qualitativa. O pentester **encadeia** falhas de baixa severidade que cada scanner reporta isoladamente como ruído, transformando três achados "médios" numa cadeia de exploração crítica. Ele descobre **falhas de lógica de negócio** — "e se eu pular a etapa de pagamento e chamar direto o endpoint de confirmação?" — que nenhum scanner detecta, porque não há padrão de código errado: o código está *correto*, a *lógica* é que está furada. Pentest é caro e lento (tipicamente trimestral ou anual), exatamente porque depende de criatividade humana, que não escala como CPU.

> [!tip] Shift-left E shift-right — segurança nas duas pontas
> O **shift-left** empurra a segurança pra *cedo*: SAST no IDE, SCA no build, DAST em staging — tudo no CI, pegando o problema antes do deploy, quando corrigir é barato. Mas segurança madura também faz **shift-right**: vigilância *em produção*, depois do deploy. Pentests periódicos contra o ambiente real, monitoramento de runtime, bug bounty, detecção de anomalias. A razão é simples — nem toda ameaça é visível no código ou em staging; algumas só emergem com tráfego real, dados reais e atacantes reais. O scanner automático é o radar que varre o tempo todo; o pentest é o detetive que entra de vez em quando e pensa como o ladrão. Você precisa dos dois, em pontos diferentes do ciclo.

## Onde cada um entra — uma questão de maturidade

Você não faz tudo isso de uma vez. A ordem natural de adoção segue a maturidade do time e do sistema:

> [!summary] A escada de maturidade
> 1. **Comece pelo básico que dá retorno imediato**: load test do *caminho crítico* (o checkout, o login), com o p99 amarrado a um SLO, e **dependency scanning (SCA)** no CI. Baixo custo, alto valor — pega a maioria dos sustos.
> 2. **Adicione microbenchmark** quando tiver um hotspot específico pra otimizar com dados, não com achismo; e **fuzzing** se você mantém parsers ou processa entrada não-confiável.
> 3. **Adicione SAST e stress test** conforme a base de código e o tráfego crescem — e use o stress test pra asserir *degradação graciosa*, não só o ponto de ruptura.
> 4. **Evolua pra DAST e pentest periódico** quando a superfície de ataque justificar; e pra **chaos engineering** só quando tiver infra *distribuída* e observabilidade madura — antes disso, custo alto e retorno baixo.

A armadilha do júnior em entrevista é dizer "a gente faz chaos engineering" num sistema que é um monólito num servidor. O sênior sabe que **cada teste não-funcional tem um pré-requisito de maturidade** — e que aplicar o avançado cedo demais é desperdício, não sofisticação. Conecta com a [[16 - Estratégia de testes em entrevista|estratégia de testes]]: escolher o teste certo pro contexto certo. Os tipos mais exóticos de teste funcional (property-based, contract) ficam em [[13 - Além do básico - property-based, snapshot, contract, smoke]].

## Em entrevista

Non-functional tests answer different questions than functional ones: not "is it correct?" but "is it fast, does it scale, does it survive failure, is it secure?". I always distinguish **load testing** — and I frame it not as "can it handle X RPS?" but as "does the p99 stay under Y ms *while* serving X RPS?", because throughput without a latency budget is vanity; the load test really validates an SLO and guards the error budget. **Stress testing** pushes past that limit to find the breaking point and, more importantly, whether degradation is graceful — shedding load with a clean 503 and Retry-After — or catastrophic, cascading into OOM and timeouts. I treat graceful degradation as a *testable property*, not an architectural hope. **Fuzzing** is something I bring up for parsers and anything touching untrusted input: coverage-guided fuzzers like libFuzzer and AFL++ mutate inputs toward new code paths, and OSS-Fuzz runs that continuously — it's the security-leaning cousin of property-based testing, where the implicit property is just "don't crash". For microbenchmarks I reach for JMH precisely because hand-rolled timers fall into JIT warmup, dead-code elimination, and constant-folding traps. **Chaos engineering** I'd only recommend for mature teams with distributed infra and good observability — and I'm careful to describe it as a scientific method (steady state, hypothesis, controlled blast radius, abort criteria, game days), not "breaking things for fun". On security I'd combine SAST, SCA, and DAST shifted left into CI with periodic human penetration testing shifted right into production, since automated scanners catch known patterns at scale but only a creative human chains low-severity findings and spots business-logic flaws. The honest senior answer is that most teams should start with load-testing the critical path and dependency scanning, and only graduate to chaos once the infrastructure justifies it.

### Vocabulário
- teste de carga → load testing
- teste de estresse → stress testing
- engenharia do caos → chaos engineering
- ponto de ruptura → breaking point
- degradação graciosa → graceful degradation
- teste de invasão / fuzzing → penetration testing / fuzzing
- guiado por cobertura → coverage-guided (fuzzing)
- orçamento de erro → error budget
- raio de explosão → blast radius
- descarte de carga → load shedding
- análise estática → static analysis (SAST)
- análise dinâmica → dynamic analysis (DAST)
- varredura de dependências → dependency scanning (SCA)
- vazamento de memória → memory leak

> [!info] Lastro
> - [Netflix's Principles of Chaos Engineering — InfoQ](https://www.infoq.com/news/2015/09/netflix-chaos-engineering/) e [Chaos engineering — Wikipedia](https://en.wikipedia.org/wiki/Chaos_engineering) (definição da Netflix, steady state, Chaos Monkey / Simian Army, 2012)
> - [Microbenchmarking in Java with JMH: Common Flaws — Daniel Mitterdorfer](https://daniel.mitterdorfer.name/posts/2014-05-20-benchmarking-flaws/) e [Avoiding Benchmarking Pitfalls on the JVM — Oracle](https://www.oracle.com/technical-resources/articles/java/architect-benchmarking.html) (JIT warmup, dead-code elimination, Blackhole, forks)
> - [Load testing Grafana k6: Peak, spike, and soak tests — Grafana Labs](https://grafana.com/blog/2023/02/14/load-testing-grafana-k6-peak-spike-and-soak-tests/) (load × stress × spike × soak)
> - [Understanding SAST, DAST, and SCA — Ajay Monga](https://medium.com/@ajay.monga73/understanding-sast-dast-and-sca-essential-layers-of-application-security-e4a06d3e7f75) e [Differences between AppSec testing types — OpsMx](https://www.opsmx.com/blog/differences-between-sast-dast-sca-comparing-appsec-strategies/) (SAST × DAST × SCA, shift-left, OWASP)
> - [Focus on Fuzzing: Coverage-Guided Fuzzing — SAFECode](https://safecode.org/blog/focus-on-fuzzing-a-closer-look-at-coverage-guided-fuzzing/) e [libFuzzer and AFL++ — Google ClusterFuzz](https://google.github.io/clusterfuzz/setting-up-fuzzing/libfuzzer-and-afl/) (algoritmo genético guiado por cobertura, AFL/libFuzzer, OSS-Fuzz, sanitizers)
> - [Defining SLOs — Google SRE Book](https://sre.google/sre-book/service-level-objectives/) e [Error Budgets — Nobl9](https://www.nobl9.com/resources/a-complete-guide-to-error-budgets-setting-up-slos-slis-and-slas-to-maintain-reliability) (SLI/SLO/SLA, orçamento de erro, percentis p50/p95/p99, média mente)
> - [DAST vs Penetration Testing — Snyk](https://snyk.io/articles/dast-vs-penetration-testing/) e [Penetration Testing vs Vulnerability Scanning — StackHawk](https://www.stackhawk.com/blog/penetration-testing-vs-vulnerability-scanning-differences-use-cases/) (scanner automático × pentest humano, encadeamento de falhas, lógica de negócio, shift-left/shift-right)

## Veja também
- [[02 - A pirâmide de testes e suas variações]] — o universo funcional do qual estes testes são o complemento
- [[13 - Além do básico - property-based, snapshot, contract, smoke]] — tipos exóticos de teste *funcional*
- [[15 - Testes em CI-CD]] — onde SAST, SCA, DAST e load tests entram no pipeline
- [[16 - Estratégia de testes em entrevista]] — escolher o teste certo pro contexto certo
- [[03-Dominios/Ciência/Redes e Protocolos/14 - Resiliência de rede|Resiliência de rede]] — os padrões que o chaos engineering valida na prática
- [[03-Dominios/Ciência/Redes e Protocolos/12 - Latência, throughput e os números|Latência, throughput e os números]] — os percentis que o load test mede
- [[Testes em Java]] — JMH e microbenchmark no ecossistema Java
- [[03-Dominios/Engenharia/Testes/index|Testes]]
