---
title: "GraalVM Native Image — conceito e trade-offs"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - cloud-native
  - adepto
  - native-image
  - graalvm
aliases:
  - "GraalVM Native Image"
  - "Native Image"
  - "AOT closed-world"
---

# GraalVM Native Image — conceito e trade-offs

> [!abstract] TL;DR
> **Native Image** compila seu app Java **ahead-of-time (AOT)** para um executável nativo, sob a hipótese de **mundo fechado** (*closed-world*): só entra no binário o código alcançável a partir do `main`, descoberto por análise estática **em tempo de build**. Você ganha **startup em milissegundos** e **footprint** baixo — mas **perde o JIT em runtime** (sem otimização especulativa de pico), o build fica lento, e todo dinamismo (reflection, proxies, recursos, serialização) precisa de **reachability metadata** explícito, senão **quebra em runtime, não no build**. O que é AOT e JIT *como mecanismo* da JVM é o Galho 3 — aqui o foco é o conceito de Native Image e o trade-off honesto. Versões cravadas: **GraalVM 25** (16/set/2025) e o aviso de que a Oracle **desfocou GraalVM como produto Java SE** a partir do JDK 24.

## O que é

**Native Image** é a ferramenta da GraalVM que pega o bytecode do seu app e o compila **ahead-of-time** num **executável nativo** autocontido — um binário do sistema operacional, sem precisar de uma JVM por baixo para rodar.

A diferença de fundo em relação ao modo tradicional: a JVM normal carrega bytecode, interpreta e vai compilando os trechos quentes com o **JIT** enquanto o app roda. O Native Image inverte isso — toda a compilação acontece **antes**, no momento do build, e o que sai é código de máquina pronto.

O preço dessa antecipação é a regra que governa tudo aqui: a **hipótese de mundo fechado** (*closed-world assumption*). Nas palavras da própria doc:

> *"all the bytecode in your application that can be called at runtime must be known (observed and analyzed) at build time."*

Ou seja: o que não for **visto e analisado** no build, não existe no binário. Não há como carregar uma classe nova depois.

> [!info] GraalVM 25 e licenças
> A versão atual é a **GraalVM 25**, lançada em **16 de setembro de 2025** (a linha 25 já teve patches: 25.0.1 em 21/out/2025 e 25.0.2 em 20/jan/2026). Existem duas distribuições com licenças distintas:
> - **Oracle GraalVM** — sob a **GFTC** (*GraalVM Free Terms and Conditions*), que **permite uso gratuito inclusive comercial e em produção**.
> - **GraalVM Community Edition** — open source, sob **GPLv2 com Classpath Exception (CPE)** (a mesma licença do OpenJDK).
>
> Fontes: [Reference Manual — Native Image](https://www.graalvm.org/latest/reference-manual/native-image/), [Release Notes JDK 25](https://www.graalvm.org/release-notes/JDK_25/), [GraalVM FAQ](https://www.graalvm.org/faq/) (acesso em 12/jun/2026).

## Por que importa

A pergunta honesta é: *por que eu trocaria o JIT por isso?* A resposta vem do perfil de carga que domina cloud-native.

A JVM tradicional foi desenhada para processos **longevos**: ela paga um custo de warmup (interpretar, perfilar, recompilar com o JIT) que se amortiza ao longo de horas de execução. Esse modelo brilha num servidor que sobe uma vez e roda por dias.

Mas há cargas em que esse warmup é exatamente o inimigo:

- **Serverless / scale-to-zero** — a função sobe do zero a cada (ou quase cada) requisição. Pagar warmup toda vez é inviável; o **cold start** é a métrica que dói.
- **Alta densidade** — muitas instâncias pequenas num cluster. Cada MB de heap e cada segundo de boot multiplicam pelo número de réplicas.
- **CLIs** — uma ferramenta de linha de comando roda, faz o trabalho e morre em segundos. Warmup é puro desperdício.

Para esses casos, **startup em milissegundos** e **footprint enxuto** valem mais que throughput de pico. É aí que Native Image entra. A doc resume o ganho assim:

> *"Starts in milliseconds"* e *"Delivers peak performance immediately, with no warmup"*.

(Atenção ao "peak performance immediately": é *desempenho imediato sem warmup* — não significa que o pico do nativo iguala o pico que o JIT atinge depois de aquecido. Sobre isso, ver os trade-offs adiante.)

## Como funciona

### AOT closed-world + análise de alcançabilidade

O coração do Native Image é uma **análise estática** que roda **em tempo de build** (não executa seu app):

> *"performs an analysis to see which classes, methods, and fields within your application are reachable and must be included in the native executable. The analysis is static: it does not run your application."*

Partindo dos pontos de entrada (o `main` e afins), a ferramenta faz um *grafo de alcançabilidade*: que método chama qual, que classe é tocada por qual campo. Tudo que for **alcançável** entra no binário; tudo que **não for** é descartado (*dead code elimination* em escala da aplicação inteira, incluindo bibliotecas e até partes do JDK).

> [!tip] A metáfora do museu fechado
> Pense no build como montar uma exposição num museu que vai ser **lacrado** antes de abrir. Você precisa decidir *na montagem* cada quadro que entra. Depois que as portas fecham (runtime), não dá pra trazer obra nova: se um visitante pedir um quadro que ficou de fora, não existe — e o pedido falha ali, na sala, não na montagem.

Essa é a força e a fraqueza do modelo: a força é o binário pequeno e o boot instantâneo; a fraqueza é que **qualquer caminho de código que a análise não enxergar simplesmente não existe** no executável.

### Reachability metadata + Tracing Agent

O problema: a análise estática **não consegue prever** caminhos dinâmicos. Reflection, proxies dinâmicos, carregamento de recursos por nome, serialização, JNI — tudo isso decide *em runtime*, por strings ou configuração, o que vai ser usado. A análise não tem como adivinhar.

A solução é o **reachability metadata** (antes referido informalmente como "reflection config" e espalhado em vários JSONs; hoje a doc trata como um conceito unificado). É um arquivo que **declara explicitamente** ao Native Image quais elementos dinâmicos precisam sobreviver à poda:

- arquivo: **`reachability-metadata.json`**
- local: **`META-INF/native-image/<groupId>/<artifactId>/`** no classpath
- cobre: **`reflection`**, **`jni`**, **`resources`** (incluindo *resource bundles*), **serialização**, **proxies** (por lista ordenada de interfaces), lambdas e descritores da **FFM API**.

Escrever esse JSON à mão é doloroso. Por isso existe o **Tracing Agent**: você roda o app **na JVM normal**, com o agente anexado, exercitando os caminhos dinâmicos (idealmente cobertos por testes), e ele **grava o metadata observado**:

```bash
java -agentlib:native-image-agent=config-output-dir=META-INF/native-image ...
```

A pegadinha embutida: o agente só registra o que foi **efetivamente executado** durante a coleta. Um caminho de reflection que seus testes não exercitaram **não entra no metadata** — e vai faltar no binário.

### Os trade-offs: sem JIT, build lento, dinamismo restrito

Aqui está a parte honesta. Native Image não é "JVM, só que mais rápido". É outro ponto no espaço de trade-offs:

- **Sem JIT em runtime.** O binário nativo é AOT puro: não há **otimização especulativa de pico** ao longo da execução. O JIT da JVM (C2, profile-guided, especulação com deopt) costuma atingir, depois de aquecido, um **throughput de pico** que o AOT estático tipicamente **não alcança**. Você troca *pico sustentado* por *desempenho imediato*. O que é JIT (C1/C2, tiered) e por que ele bate o AOT em pico é mecanismo de JVM → ver Galho 3.
- **Build lento e pesado.** A análise de mundo fechado é cara: builds de Native Image levam **minutos** e consomem bastante CPU/memória — bem mais que um `package` comum. Isso pesa no CI.
- **Dinamismo restrito.** Tudo que a análise estática não enxerga (reflection, proxies, recursos, serialização) exige metadata. Bibliotecas que abusam de dinamismo sem fornecer metadata viram fonte de bug.
- **Mundo fechado por definição.** Não há carregamento dinâmico de classes "de fora" em runtime. O conjunto de código é fixo no build.

> [!warning] A fronteira do Galho 3 (não re-explicar aqui)
> **AOT** e **JIT** como *mecanismos* de execução da JVM — o que são, como o JIT compila trechos quentes, C1/C2, tiered compilation — pertencem ao **Galho 3 (JVM)**. Esta nota usa esses conceitos, não os ensina. Quando precisar do "por que o JIT ganha em pico" ou "o que é compilação AOT", siga os links da seção "Veja também" abaixo.

## Na prática

Compilação direta com a ferramenta `native-image` (domínio neutro):

```bash
# 1) Compila as classes normalmente (javac/maven/gradle) — omitido

# 2) Coleta reachability metadata rodando na JVM com o Tracing Agent
java -agentlib:native-image-agent=config-output-dir=src/main/resources/META-INF/native-image \
     -cp target/app.jar com.exemplo.App

# 3) Gera o executável nativo a partir do jar
native-image -jar target/app.jar app

# 4) Roda o binário — sem JVM por baixo, sobe em milissegundos
./app
```

Exemplo de `reachability-metadata.json` (declarando uma classe acessada por reflection e um recurso lido por nome):

```json
{
  "reflection": [
    {
      "type": "com.exemplo.dominio.Pedido",
      "allDeclaredFields": true,
      "allDeclaredMethods": true,
      "allDeclaredConstructors": true
    }
  ],
  "resources": {
    "includes": [
      { "glob": "config/mensagens.properties" }
    ]
  }
}
```

A leitura do que está acontecendo: você está dizendo à análise "mesmo que você não veja ninguém chamando `Pedido` por nome, **mantenha** seus campos/métodos/construtores no binário, porque alguém vai instanciá-la por reflection". Sem essa declaração, a classe é podada e a chamada reflexiva estoura **em runtime**.

## Armadilhas

### (1) Esquecer hints de reflection → a falha aparece em RUNTIME, não no build

Esta é a mais traiçoeira. Se um caminho de reflection/proxy/recurso **não está no metadata**, o build **passa de boa** — a análise simplesmente não sabia que aquilo era necessário e podou. O erro só aparece quando o código dinâmico é executado de verdade: `ClassNotFoundException`, `NoSuchMethodException`, recurso `null`. Ou seja, o build verde te dá uma falsa sensação de segurança, e a quebra vaza para produção. A defesa é coletar metadata com o Tracing Agent **sob boa cobertura de testes** — porque o agente só registra o que foi executado.

### (2) Esperar throughput de pico igual ao da JVM aquecida

Native Image te dá desempenho **imediato** (sem warmup). Mas "imediato" não é "máximo". A JVM com JIT, depois de aquecida, costuma entregar **throughput de pico superior** graças à otimização especulativa. Se sua carga é um serviço longevo, *throughput-bound*, que roda horas sob alta vazão, trocar a JVM por nativo pode **piorar** seu desempenho em regime. Native Image brilha em **startup e footprint**, não necessariamente em pico sustentado. (Por que o JIT ganha em pico → Galho 3.)

### (3) Achar que toda aplicação deve virar nativa

Não deve. Native Image resolve um problema específico (cold start, footprint, densidade) e cobra um preço real (build lento, dinamismo restrito, pico mais baixo). Um monólito *throughput-bound* longevo, cheio de bibliotecas reflexivas sem metadata, é o pior caso: você paga todo o custo e colhe pouco do benefício. A decisão **nativo vs JVM** é uma escolha de engenharia caso a caso → nota 21.

## Em entrevista

### Frase pronta (inglês)

> GraalVM Native Image compiles a Java application **ahead-of-time** into a self-contained native executable, under a **closed-world assumption**: only code reachable from `main`, determined by static analysis **at build time**, ends up in the binary. The win is **millisecond startup** and a small **footprint**, which is ideal for serverless, scale-to-zero, and CLI workloads. The honest cost is that there's **no JIT at runtime**, so you lose the speculative peak-performance optimization a warmed-up JVM gives you, the build is slow, and every dynamic feature — reflection, proxies, resources, serialization — must be declared through **reachability metadata**, otherwise it fails **at runtime, not at build time**. So it's a trade-off, not a free upgrade: I'd reach for it when startup and density dominate, and stay on the JVM when sustained peak throughput is the priority.

### Vocabulário

| Português | Inglês |
| --- | --- |
| imagem nativa | native image |
| compilação AOT | ahead-of-time (AOT) compilation |
| mundo fechado | closed-world (assumption) |
| metadados de alcançabilidade | reachability metadata |
| reflexão | reflection |
| tempo de warmup | warmup time |
| desempenho de pico | peak performance / throughput |
| agente de rastreamento | tracing agent |

## Veja também

- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/09 - Native Image com Spring — Spring AOT na prática|Native Image com Spring]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/21 - Native vs JVM — a decisão honesta|Native vs JVM (a decisão honesta)]]
- [[03-Dominios/Tecnologia/Java/JVM/07 - JIT — C1, C2 e tiered compilation|JIT (Galho 3)]]
- [[03-Dominios/Tecnologia/Java/JVM/01 - A JVM — o que é e o pipeline de execução|A JVM (Galho 3)]]
- [[03-Dominios/Tecnologia/Java/JVM/14 - Performance da JVM — síntese|Performance da JVM — síntese (Galho 3)]]
- [[03-Dominios/Tecnologia/Java/Cloud-native e produção/index|Cloud-native e produção (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- GraalVM — [Native Image Reference Manual](https://www.graalvm.org/latest/reference-manual/native-image/) (closed-world, análise estática, "starts in milliseconds / peak performance immediately"; acesso em 12/jun/2026).
- GraalVM — [Reachability Metadata](https://www.graalvm.org/latest/reference-manual/native-image/metadata/) (`reachability-metadata.json` em `META-INF/native-image/`; cobre reflection/jni/resources/serialization/proxies; Tracing Agent `-agentlib:native-image-agent`; acesso em 12/jun/2026).
- GraalVM — [Release Notes JDK 25](https://www.graalvm.org/release-notes/JDK_25/) (GraalVM 25 em 16/set/2025; 25.0.1 em 21/out/2025; 25.0.2 em 20/jan/2026; Oracle GraalVM 25 sobre Oracle JDK 25, CE 25 sobre OpenJDK 25; acesso em 12/jun/2026).
- GraalVM — [FAQ](https://www.graalvm.org/faq/) (licenças: Oracle GraalVM sob GFTC com uso comercial/produção gratuito; Community Edition sob GPLv2 + Classpath Exception; acesso em 12/jun/2026).
- Oracle — [Detaching GraalVM from the Java Ecosystem Train](https://blogs.oracle.com/java/detaching-graalvm-from-the-java-ecosystem-train) e cobertura associada (GraalVM for JDK 24 foi o **último** release licenciado/suportado como parte dos produtos Oracle Java SE; Oracle **desfocou GraalVM como produto Java**, mas **Native Image segue mantido** via GFTC e Community Edition; acesso em 12/jun/2026).
