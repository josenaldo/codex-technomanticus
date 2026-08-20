---
title: "Native vs JVM — a decisão honesta"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: magus
tags:
  - java
  - cloud-native
  - magus
  - native-image
aliases:
  - "Native vs JVM"
  - "Quando usar native image"
---

# Native vs JVM — a decisão honesta

> [!abstract] TL;DR
> Native image **não é um upgrade da JVM** — é uma **plataforma de execução diferente**, com outro conjunto de trade-offs. Native vence quando o **startup domina o seu SLA**: serverless/FaaS, scale-to-zero, CLIs, alta densidade de instâncias. A JVM tradicional vence quando **throughput de pico**, **build/CI rápido** ou **dinamismo** (agentes, instrumentação, reflection sem metadata) importam mais. A pergunta honesta não é "native é melhor?", é "**o que domina o meu SLA e o meu custo?**". Sem dogma: existe um "quando X" *e* um "quando Y", e ambos são respostas legítimas.

## O que é

Esta nota é o **capstone de julgamento** do galho. Ela não re-explica *o que é* native image (isso é a [[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|nota 08]]) nem *como* o Spring AOT prepara a aplicação (a [[03-Dominios/Tecnologia/Java/Cloud-native e produção/09 - Native Image com Spring — Spring AOT na prática|nota 09]]). Ela responde uma pergunta diferente, e mais difícil: **dada uma aplicação concreta, native image ou JVM?**

A resposta honesta tem duas metades. Native compila *ahead-of-time* sob a *closed-world assumption*: a [GraalVM](https://www.graalvm.org/latest/reference-manual/native-image/) faz análise estática a partir do `main`, e "código que não pode ser alcançado quando a imagem nativa é criada será removido e não fará parte do executável". Isso dá os ganhos (startup em milissegundos, footprint reduzido, "peak performance immediately, with no warmup") e impõe os custos (build lento, mundo fechado, metadata de *reachability* para reflection/proxies/JNI). A JVM faz o oposto: carrega o mundo dinamicamente e otimiza em runtime com o JIT.

> [!info] Trade-off, não tier
> A leitura ingênua é tratar native como "JVM turbinada" ou JVM como "native legado". Errado nas duas direções. São **eixos diferentes do mesmo espaço de decisão**: um troca runtime por build-time, outro troca build-time por runtime. Não há vencedor universal — há vencedor *por workload*.

## Por que importa

Porque a escolha errada custa caro nos dois sentidos, e o erro raramente aparece no `hello world`.

Escolher native sem ser *startup-bound* significa pagar build de minutos, CI mais complexo (notas [[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|08]]/09) e o risco de bibliotecas sem *reachability metadata* — para ganhar um startup que ninguém no seu SLA estava esperando. Escolher JVM para uma função serverless que escala a zero significa pagar *cold start* de segundos a cada invocação, estourar a latência percebida e desperdiçar o modelo de cobrança por execução.

A decisão é **arquitetural e de plataforma**, tomada cedo, e cara de reverter. Por isso ela merece um framework explícito em vez de hype — em qualquer das direções.

## Como funciona

O framework tem três perguntas. Responda-as *para a sua aplicação*, não para "Java em geral".

### Quando native image vale

Native vence quando o **tempo de inicialização é parte do SLA ou do custo**. Casos canônicos:

- **Serverless / FaaS**: cada *cold start* entra na latência do usuário. Startup em milissegundos vs segundos muda a viabilidade do produto.
- **Scale-to-zero**: a instância sobe sob demanda. Se subir é lento, a elasticidade vira gargalo.
- **CLIs e ferramentas de linha de comando**: o processo nasce, faz uma coisa e morre. Não há *runtime* longo para o JIT amortizar o warmup — o startup *é* o tempo total.
- **Alta densidade**: muitas instâncias pequenas num nó. Footprint menor por processo significa mais processos por host — densidade vira dinheiro.

O fio condutor: nesses cenários **o startup e o footprint dominam**, e o throughput de pico em regime estacionário ou nunca chega a importar (processo curto) ou não é o gargalo.

> [!example] O teste de uma pergunta
> "Se eu cortar 2 segundos do startup, alguém do outro lado nota?" Se a resposta é *sim e isso muda o SLA ou a conta* — native está na mesa. Se a resposta é *não, o processo roda horas e o que importa é a vazão* — provavelmente não.

### Quando a JVM tradicional vence

A JVM vence quando o que importa acontece **depois** do warmup, ou quando o **build/dinamismo** pesam mais que o startup:

- **Throughput de pico via JIT**: em serviços longevos, o JIT perfila o código *real* em produção e recompila os *hot paths* com C2 — tiered compilation, *profile-guided optimization* em runtime, *speculative optimizations* que a análise estática não pode fazer. Para esse regime, ver [[03-Dominios/Tecnologia/Java/JVM/07 - JIT — C1, C2 e tiered compilation|JIT (Galho 3)]] e [[03-Dominios/Tecnologia/Java/JVM/14 - Performance da JVM — síntese|Performance da JVM — síntese]]. Native entrega pico imediato, mas o **teto** de pico do JIT em workloads longos é difícil de bater sem PGO bem feito.
- **Build rápido e CI simples**: `./mvnw package` em segundos vs minutos de compilação AOT. Loop de feedback do dev e custo de pipeline (notas [[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|08]]/09).
- **Dinamismo, agentes e instrumentação**: APM/Java agents via `-javaagent`, reflection sem metadata pré-declarado, *bytecode instrumentation*, *hot reload* de dev. O mundo fechado da native fecha a porta para boa parte disso.
- **Bibliotecas sem reachability metadata**: se uma dependência usa reflection/proxies e não publica os *hints*, native quebra em runtime de formas sutis. Na JVM, simplesmente funciona.

> [!note] Feynman
> Pense no JIT como um chef que prova o prato enquanto cozinha e ajusta o tempero ao gosto real dos clientes daquela noite — leva uns minutos para acertar, mas o prato fica ótimo. A native é um prato congelado de fábrica: pronto na hora, sempre igual, mas o tempero foi decidido antes de saber quem ia comer. Para um restaurante que serve a noite inteira, o chef ganha. Para uma máquina de venda automática que entrega *agora*, o congelado ganha.

### O custo de build/CI e o trade-off de plataforma

O custo escondido da native não está no runtime — está **antes** dele. A compilação AOT é cara (build em minutos), o pipeline precisa de toolchain GraalVM, e cada dependência precisa de *reachability metadata* válido (detalhado nas notas [[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|08]] e 09). Esse custo é recorrente: todo build, todo CI, toda atualização de dependência.

Por isso a decisão é de **plataforma, não de versão**. Você não "atualiza" de JVM para native como atualiza de Java 21 para 25. Você escolhe um **modelo de execução** com outra economia: paga no build para ganhar no startup, ou paga no startup para ganhar no build e no dinamismo. Tratar isso como "ligar uma flag" é a raiz da maioria das migrações frustradas.

## Na prática

Árvore de decisão neutra (domínios genéricos — vale para qualquer serviço, não há projeto real implícito aqui):

```text
DECISÃO: native image vs JVM tradicional
│
├─ EIXO 1 — Startup domina o SLA/custo?
│   ├─ Função serverless, scale-to-zero, CLI curta ........ PESA p/ NATIVE
│   └─ Serviço longevo (roda horas/dias, cold start raro) . PESA p/ JVM
│
├─ EIXO 2 — Throughput de pico é o gargalo?
│   ├─ Hot path longo, vazão importa mais que latência
│   │   de subida → JIT (C2 + PGO em runtime) .............. PESA p/ JVM
│   └─ Processo curto / pico nunca é o gargalo ............. NEUTRO p/ native
│
├─ EIXO 3 — Precisa de dinamismo?
│   ├─ Java agents, instrumentação, reflection sem
│   │   metadata, hot reload ............................... PESA p/ JVM
│   └─ Mundo fechado é aceitável (deps com hints OK) ....... NEUTRO p/ native
│
└─ EIXO 4 — Build/CI rápido é prioridade?
    ├─ Loop de dev curto, pipeline simples, atualizações
    │   frequentes de deps ................................. PESA p/ JVM
    └─ Build lento aceitável (deploy raro, ganho no
        runtime compensa) .................................. NEUTRO p/ native

LEITURA: conte os pesos PARA A SUA app.
  • Vários eixos apontando NATIVE + startup-bound real → native image.
  • Throughput/dinamismo/build dominando → JVM tradicional.
  • Empate → fique na JVM (default seguro): menor custo de migração,
    reversível, sem dívida de reachability metadata.
```

| Perfil de workload          | Startup-bound? | Pico via JIT? | Dinamismo? | Build/CI    | Tende a       |
| --------------------------- | -------------- | ------------- | ---------- | ----------- | ------------- |
| Função serverless / FaaS    | sim, crítico   | irrelevante   | baixo      | tolera lento| **native**    |
| CLI / ferramenta curta      | sim, é o total | irrelevante   | baixo      | tolera lento| **native**    |
| Serviço longevo de vazão    | não            | sim, é o teto | médio      | quer rápido | **JVM**       |
| Serviço com APM/agentes     | varia          | varia         | alto       | quer rápido | **JVM**       |
| Alta densidade de réplicas  | sim (footprint)| varia         | baixo      | tolera lento| **native***  |

> [!tip] Regra do default
> Na dúvida, **comece na JVM**. É o caminho reversível e de menor custo de migração. Mova para native quando tiver uma *razão de startup* concreta — não por hype, e não "porque é o futuro". `*` Alta densidade só fecha para native se o footprint reduzido realmente vira mais réplicas por nó *no seu cluster*; meça antes de assumir.

## Armadilhas

### (1) Migrar pra native por hype, sem startup-bound real

O erro mais comum: adotar native porque "é cloud-native moderno", sem que startup ou footprint estejam no SLA. O resultado é pagar todo o custo (build lento, CI complexo, dívida de *reachability metadata*) por um ganho que o seu workload não consome. Se o serviço roda por horas e o gargalo é vazão, o startup mais rápido é irrelevante — e você trocou a parte fácil pela difícil. **Native sem razão de startup é custo sem benefício.**

### (2) Subestimar o custo de build/CI e do reachability metadata

A demo compila num clique; a aplicação real tem dezenas de dependências transitivas, e cada uma precisa de *hints* válidos para reflection/proxies/JNI ou quebra em runtime de forma sutil. Some o build AOT de minutos a cada commit, a toolchain GraalVM no pipeline, e a manutenção dos *hints* a cada bump de dependência. Esse custo é **recorrente e cresce com a aplicação** (notas [[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|08]]/09). Quem orça só o runtime e esquece o build/CI descobre o trade-off tarde demais.

### (3) Assumir paridade de throughput de pico

Native entrega pico *imediato* (sem warmup), o que é ótimo para processos curtos — mas isso **não** é o mesmo que ter o *teto* de pico mais alto. Em serviço longevo, o JIT C2 perfila o tráfego real, recompila *hot paths* e aplica otimizações especulativas que a análise estática AOT não pode fazer ([[03-Dominios/Tecnologia/Java/JVM/07 - JIT — C1, C2 e tiered compilation|JIT]], [[03-Dominios/Tecnologia/Java/JVM/14 - Performance da JVM — síntese|Performance da JVM]]). Assumir "native = mais rápido sempre" confunde *startup* com *steady-state throughput*. São métricas diferentes; native ganha a primeira, a JVM frequentemente ganha a segunda em workloads de vazão. (Sem número aqui de propósito — a magnitude depende do workload; meça o seu, não cite benchmark de blog.)

## Em entrevista

### Frase pronta (inglês)

> Native image isn't a JVM upgrade — it's a different execution platform with a different cost model. It wins when startup dominates the SLA: serverless, scale-to-zero, CLIs, high density — where milliseconds-to-ready and a smaller footprint translate directly into latency or cost. The JVM tends to win when peak throughput matters, because the JIT profiles real production traffic and optimizes hot paths in ways ahead-of-time analysis can't, and also when you need fast builds, runtime dynamism like agents and instrumentation, or libraries that lack reachability metadata. So my default is to start on the JVM — it's the reversible, lower-cost path — and move to native only when there's a concrete startup-bound reason, not because it's fashionable.

### Vocabulário

| Português            | Inglês          |
| -------------------- | --------------- |
| imagem nativa        | native image    |
| escala a zero        | scale-to-zero   |
| sem servidor         | serverless      |
| vazão de pico        | peak throughput |
| densidade            | density         |
| custo de plataforma  | platform cost   |
| partida a frio       | cold start      |
| mundo fechado        | closed world    |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|GraalVM Native Image (conceito)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/09 - Native Image com Spring — Spring AOT na prática|Native Image com Spring]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/22 - Capstone — do jar ao cluster|Capstone — do jar ao cluster]]
- [[03-Dominios/Tecnologia/Java/JVM/07 - JIT — C1, C2 e tiered compilation|JIT (Galho 3)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Spring Boot Reference — [Introducing GraalVM Native Images](https://docs.spring.io/spring-boot/reference/packaging/native-image/introducing-graalvm-native-images.html) (closed-world assumption, *reachability metadata*, beans fixos em build time, sem lazy class loading)
- GraalVM — [Native Image Reference Manual](https://www.graalvm.org/latest/reference-manual/native-image/) ("start in milliseconds", "peak performance immediately, with no warmup", "fraction of the resources", análise estática a partir do `main`, metadata para JNI/Reflection/Dynamic Proxy)
