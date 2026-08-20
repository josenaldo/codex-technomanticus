---
title: "Latência, throughput e os números"
created: 2026-06-18
updated: 2026-06-18
type: concept
fase: Magus
status: evergreen
publish: false
tags:
  - ciencia-da-computacao
  - redes
  - performance
  - entrevista
---

# Latência, throughput e os números

> [!abstract] Resumo em uma linha
> Latência é o tempo de UMA operação, throughput é o volume por segundo, bandwidth é o teto do canal — e a hierarquia memória → disco → rede tem ordens de grandeza que justificam quase toda decisão de system design.

Todo senior carrega uma planilha mental. Não os números exatos — esses mudam com o hardware. As **ordens de grandeza**. Quando alguém propõe "vamos buscar isso do banco a cada request", o senior já ouve o custo: um salto de microssegundos (cache local) para milissegundos (rede). Mil vezes mais caro. A intuição não vem de decorar; vem de internalizar a pirâmide.

Esta nota é sobre essa pirâmide. E sobre os três termos que iniciantes confundem o tempo todo: latência, throughput e bandwidth.

## Os três termos que ninguém deveria confundir

Imagine um cano d'água ligando duas casas.

- A **largura do cano** é a **bandwidth**: a capacidade máxima de água que o cano comporta. É uma propriedade física do canal. Um cano grosso pode levar muita água; um fino, pouca.
- O **tempo que uma gota leva** para atravessar o cano de uma ponta à outra é a **latência**: quanto demora UMA operação a completar.
- A **água que de fato sai** pela outra ponta por segundo é o **throughput**: o volume real entregue, dado tudo que atrapalha no caminho.

> [!warning] Bandwidth ≠ throughput
> Bandwidth é o teto teórico. Throughput é o que você realmente obtém — sempre menor, porque cabeçalhos de protocolo, retransmissões, controle de congestão e contenção comem parte da capacidade. Um link de 1 Gbps (bandwidth) raramente entrega 1 Gbps de dados úteis (throughput).

E o ponto que confunde mais gente: **você pode ter bandwidth altíssima E latência altíssima ao mesmo tempo.** Um link de satélite geoestacionário pode transferir gigabytes por segundo (cano larguíssimo), mas cada pacote viaja ~36.000 km até o satélite e mais ~36.000 km de volta — RTT na casa dos 500 ms a 600 ms. Bandwidth de sobra; latência terrível.

A analogia clássica: um caminhão lotado de HDs cruzando o país tem **throughput** absurdo (petabytes em um dia) e **latência** péssima (você espera um dia inteiro pela primeira resposta). "Never underestimate the bandwidth of a station wagon full of tapes."

> [!tip] A pergunta diagnóstica
> Quando alguém diz "a rede está lenta", pergunte: lento para *uma* request (latência) ou lento para *muitas* requests (throughput)? São problemas diferentes, com soluções diferentes. Latência alta você ataca aproximando ou paralelizando; throughput baixo você ataca alargando o cano ou removendo gargalos.

## RTT e suas quatro componentes

A latência de uma operação de rede — o **RTT** (Round-Trip Time), o ida-e-volta — não é um número monolítico. Ela se decompõe em quatro partes, e só uma delas o dinheiro não compra.

1. **Propagação** — o tempo do sinal viajar pela distância física. Limitado pela velocidade da luz. Na fibra, a luz anda a ~66% da velocidade no vácuo (índice de refração ~1.5), ou seja ~200.000 km/s. Isso dá um piso de aproximadamente **1 ms a cada 100–200 km** de cabo. Esse é um limite **físico**.
2. **Transmissão** — o tempo de empurrar os bits para o fio. Depende do tamanho do pacote dividido pela bandwidth. Cano mais largo → menos tempo de transmissão.
3. **Fila** (queuing) — o pacote esperando em buffers de roteadores congestionados. Variável e imprevisível; é a principal fonte de jitter.
4. **Processamento** — roteadores inspecionando cabeçalhos, decidindo rotas, fazendo NAT/firewall.

> [!important] O piso que dinheiro nenhum compra
> Propagação é regida pela velocidade da luz — uma constante do universo. Nova York ↔ Londres tem ~5.500 km de fibra; mesmo na linha reta teórica, a luz na fibra leva ~28 ms só de ida. Na prática o RTT fica perto de **70–80 ms** com os desvios reais do cabeamento. Nenhum upgrade de servidor, nenhuma otimização de código resolve isso. A única saída é **encurtar a distância física** — e é exatamente por isso que CDNs existem. Ver [[13 - Load balancing e CDN]].

Isso explica por que latência intercontinental tem um piso. Você pode comprar o melhor hardware do mundo; a luz continua levando o tempo que leva para cruzar o oceano.

## A tabela que todo programador deveria conhecer

Esta é a tabela canônica, popularizada por **Jeff Dean** (Google) a partir de números compilados também por **Peter Norvig**. Os valores absolutos envelhecem com o hardware — SSDs ficaram muito mais rápidos desde a versão original de ~2012 — então trate-os como **ordens de grandeza**, não como verdade gravada em pedra.

| Operação | Latência aproximada | Em escala humana (×1 bilhão) |
| --- | --- | --- |
| Referência em cache L1 | ~1 ns | 1 segundo |
| Branch mispredict | ~3 ns | 3 segundos |
| Referência em cache L2 | ~4–7 ns | ~5 segundos |
| Mutex lock/unlock | ~25 ns | 25 segundos |
| Acesso à RAM (main memory) | ~100 ns | ~1,5 minuto |
| Leitura sequencial 1 MB da RAM | ~3–10 μs | ~1–3 horas |
| SSD random read | ~16–100 μs | ~5 horas a 1 dia |
| Round-trip no mesmo datacenter | ~0,5 ms | ~6 dias |
| Leitura 1 MB do SSD | ~50–1.000 μs | dias |
| Seek de HDD (disco mecânico) | ~10 ms | ~4 meses |
| Round-trip mesma região (AZ↔AZ) | ~1 ms | ~11 dias |
| Round-trip inter-região (continental) | ~30–100 ms | ~1–3 anos |
| Round-trip intercontinental | ~100–300 ms | ~3–10 anos |

A coluna da direita multiplica tudo por 1 bilhão para trazer os números para a escala humana. Ela revela o que importa: se um acesso à cache L1 fosse 1 segundo, um seek de HDD seria **4 meses** e uma viagem intercontinental seriam **anos**.

> [!note] Não decore. Internalize os saltos.
> O valor não está em saber que RAM é 100 ns. Está em sentir os degraus:
> - **Cache → RAM**: ~100× mais lento.
> - **RAM → SSD**: ~100–1000× mais lento.
> - **SSD/disco local → rede no datacenter**: outro salto grande.
> - **Datacenter → outra região**: ~100× mais lento que rede local.
>
> Cada degrau é uma ordem de grandeza ou mais. É essa sequência que sua intuição precisa cantar de cor.

O diagrama abaixo desenha a pirâmide. Note como cada degrau abaixo é dramaticamente mais caro que o de cima.

```mermaid
flowchart TD
    L1["Cache L1<br/>~1 ns"] --> RAM["RAM<br/>~100 ns<br/>(100&times; mais lento)"]
    RAM --> SSD["SSD random read<br/>~16-100 &mu;s<br/>(100-1000&times;)"]
    SSD --> DC["Rede no datacenter<br/>~0,5 ms<br/>(salto p/ a rede)"]
    DC --> HDD["Seek de HDD<br/>~10 ms"]
    DC --> REG["Inter-regiao<br/>~30-100 ms<br/>(100&times; a rede local)"]
    REG --> INTER["Intercontinental<br/>~100-300 ms<br/>(limite fisico: luz)"]

    style L1 fill:#1b5e20,color:#fff
    style RAM fill:#2e7d32,color:#fff
    style SSD fill:#f9a825,color:#000
    style DC fill:#ef6c00,color:#fff
    style HDD fill:#c62828,color:#fff
    style REG fill:#b71c1c,color:#fff
    style INTER fill:#6a1b1c,color:#fff
```

Leitura do diagrama: descendo a pirâmide, a cor esquenta e o custo dispara. O verde (memória) é o reino dos nanossegundos; o amarelo (SSD) salta para microssegundos; o laranja/vermelho (rede e disco mecânico) entra nos milissegundos. Cada transição de cor é pelo menos uma ordem de grandeza. O fundo da pirâmide — intercontinental — é onde a física, não a engenharia, manda.

## Por que esses números justificam quase tudo

Internalizada a pirâmide, metade do system design vira consequência óbvia.

- **Por que caching importa**: cache evita o salto caro. Servir da RAM (~100 ns) em vez de ir ao banco remoto (~1 ms+) é mil vezes mais rápido. É o motivo de [[08 - Caching HTTP]] e de caches de aplicação existirem. Cada hit de cache é um salto da pirâmide que você não pagou.
- **Por que banco local > banco remoto**: colocar o banco na mesma região da aplicação (~1 ms) em vez de cruzar o continente (~30–100 ms) corta a latência de cada query em 30–100×. Co-localização não é detalhe; é arquitetura.
- **Por que CDN existe**: não dá para vencer a velocidade da luz, então CDNs **aproximam fisicamente** o conteúdo do usuário. Em vez de 200 ms até o servidor de origem do outro lado do mundo, 10 ms até o edge mais próximo. Ver [[13 - Load balancing e CDN]] e [[04 - DNS]] (que escolhe o edge).
- **Por que minimizar round-trips é a regra de ouro**: se cada round-trip custa dezenas de milissegundos, fazer dez em série custa centenas de milissegundos. A regra de ouro do system design de performance é: **reduza o número de round-trips serializados.** É também por isso que protocolos como o do [[02 - TCP]] sofrem com o handshake e o slow start — cada um custa RTTs antes de qualquer dado útil trafegar.

> [!tip] O reflexo do senior
> Antes de otimizar um algoritmo de O(n²) para O(n log n), pergunte: esse código está fazendo uma chamada de rede dentro do loop? Porque uma chamada de rede dentro do loop derrota qualquer melhoria de complexidade. O salto para a rede domina tudo.

## Tail latency: a média mente

Aqui está o conceito que separa o pleno do senior. Você mede a latência de um serviço e vê "média de 20 ms". Parece ótimo. Mas a média **esconde a cauda**.

O que mata a experiência do usuário não é a média; é o **p99** — o percentil 99, o valor que 99% das requests ficam abaixo. Se seu p99 é 800 ms, significa que **1 em cada 100 requests** demora quase um segundo. Para um usuário fazendo dezenas de ações, ele vai bater nessa cauda toda hora.

> [!quote] The Tail at Scale (Dean & Barroso, 2013)
> Em um serviço onde cada request precisa consultar 100 backends em paralelo, se cada backend tem só **1% de chance** de estar lento (p99 = 10 ms), a chance de **pelo menos um** estar lento é 1 − (0,99)¹⁰⁰ ≈ **63%**. A latência percebida pelo usuário, que espera por todos, tende ao p99 de um deles — não à média.

Isso é o **fan-out amplificando a cauda**. Quanto mais subsistemas uma request toca, mais provável que ela esbarre na cauda lenta de pelo menos um. Em escala, o p99 individual vira o caso comum do todo.

```mermaid
flowchart TD
    REQ["1 request do usuario<br/>espera por TODOS"] --> B1["Backend 1<br/>p50: 5 ms"]
    REQ --> B2["Backend 2<br/>p50: 5 ms"]
    REQ --> B3["Backend 3<br/>p50: 5 ms"]
    REQ --> DOTS["..."]
    REQ --> B100["Backend 100<br/>AZAR: p99 = 800 ms"]

    B1 --> JOIN["Resposta final<br/>= o mais LENTO<br/>= 800 ms"]
    B2 --> JOIN
    B3 --> JOIN
    DOTS --> JOIN
    B100 --> JOIN

    style B100 fill:#c62828,color:#fff
    style JOIN fill:#b71c1c,color:#fff
    style REQ fill:#1565c0,color:#fff
```

Leitura do diagrama: a request abre em 100 chamadas paralelas. Quase todas voltam rápido (5 ms), mas basta UMA cair na cauda lenta (vermelho, 800 ms) para a resposta final — que precisa de todos — ficar travada nesse pior caso. Com 100 backends, a probabilidade de ao menos um estar na cauda é alta. Por isso o p99 de um backend vira a experiência típica do agregado.

> [!important] Implicação prática
> Otimize a cauda, não só a média. Técnicas como **hedged requests** (mandar a mesma request a dois backends e usar a primeira resposta) atacam exatamente isso — no paper original, hedging cortou um p99 de 1.800 ms para 74 ms inflando o trabalho total em só ~2%. Monitore p95/p99/p999, nunca apenas a média. E veja [[14 - Resiliência de rede]] para timeouts e retries que limitam a cauda.

## A regra dos round-trips

Cada round-trip **serial** soma um RTT inteiro. Faça três chamadas em sequência, onde a segunda depende da primeira e a terceira da segunda, e você paga 3×RTT antes de a primeira linha de resposta sair. Faça as três em **paralelo** (quando não há dependência) e você paga só 1×RTT — o tempo da mais lenta.

```mermaid
sequenceDiagram
    participant C as Cliente
    participant A as Servico A
    participant B as Servico B
    participant D as Servico C

    Note over C,D: SERIAL — cada chamada espera a anterior (3 x RTT)
    C->>A: chamada 1
    A-->>C: resposta 1
    C->>B: chamada 2
    B-->>C: resposta 2
    C->>D: chamada 3
    D-->>C: resposta 3
    Note over C,D: total ~= 3 x RTT

    Note over C,D: PARALELO — todas de uma vez (1 x RTT)
    par
        C->>A: chamada 1
        A-->>C: resposta 1
    and
        C->>B: chamada 2
        B-->>C: resposta 2
    and
        C->>D: chamada 3
        D-->>C: resposta 3
    end
    Note over C,D: total ~= 1 x RTT (a mais lenta)
```

Leitura do diagrama: no bloco serial, cada chamada só parte depois que a anterior volta — os RTTs empilham. No bloco paralelo (`par`), as três disparam juntas e o cliente espera apenas a mais lenta. Mesmo trabalho, mesma rede; o que muda é o **agendamento**. Se houver dependência real entre as chamadas, você é obrigado a serializar; se não houver, serializar é desperdício puro.

A consequência: **paralelize o que for independente; faça batch do que for repetitivo.** Em vez de N queries de um item cada (N round-trips), uma query de N itens (1 round-trip). Em vez de chamadas encadeadas, um fan-out paralelo.

> [!example] O caso clássico (ver capstone)
> Um endpoint que demorava 1,5 s porque fazia três chamadas HTTP **sequenciais** caiu para ~200 ms ao paralelizá-las — a soma virou o máximo. É o exemplo de debugging que vive em [[15 - Redes em entrevista]]; aqui só registramos o princípio, lá está a história completa.

## Lei de Little: o que amarra os três

Latência, throughput e concorrência não são três grandezas soltas. Uma lei simples e universal as costura: a **Lei de Little**. Ela diz que o número de requests "em voo" dentro do sistema (a **concorrência**) é igual ao throughput multiplicado pela latência média:

> concorrência = throughput × latência
> L = λ × W

Pense numa fila de banco. Se chegam 2 clientes por minuto (throughput, λ) e cada um leva 5 minutos sendo atendido (latência, W), em regime estável há sempre ~10 clientes dentro da agência (concorrência, L). Não é mágica: é contagem. O que entra menos o que sai se acumula, e em equilíbrio o estoque é o produto dos dois.

A lei vale para qualquer sistema estável — filas de banco, aeroportos, threads de um servidor, conexões de um pool. É por isso que ela é uma das ferramentas mais afiadas do senior: você sabe **dois** dos três números e ela te entrega o terceiro de graça.

Um exemplo concreto de dimensionamento. Seu serviço precisa sustentar **1000 RPS** e cada request leva **200 ms** (0,2 s) em média:

| Grandeza | Símbolo | Valor |
| --- | --- | --- |
| Throughput | λ | 1000 req/s |
| Latência média | W | 0,2 s |
| **Requests em voo** | **L = λ × W** | **200** |

Ou seja: para sustentar esse tráfego, **200 requests** estão sendo processadas a qualquer instante. Se seu modelo é uma thread (ou conexão) por request, você precisa de ~200 threads/conexões vivas ao mesmo tempo. Daí o tamanho mínimo do seu pool — não é chute, é a Lei de Little.

```mermaid
flowchart LR
    IN["Chegam<br/>1000 req/s<br/>(throughput &lambda;)"] --> SYS

    subgraph SYS["Sistema em regime"]
        FLIGHT["200 requests EM VOO<br/>(concorrencia L = &lambda; x W)<br/>cada uma leva 0,2 s (latencia W)"]
    end

    SYS --> OUT["Saem<br/>1000 req/s"]

    style IN fill:#1565c0,color:#fff
    style FLIGHT fill:#2e7d32,color:#fff
    style OUT fill:#1565c0,color:#fff
```

Leitura do diagrama: o que entra (1000 req/s) tem que sair (1000 req/s) em regime estável — senão a fila explode. O que fica "preso" no meio, em voo, é a concorrência: throughput vezes latência, aqui 200 requests. Aumente a latência sem mexer no resto e a caixa do meio incha; o sistema precisa de mais capacidade simultânea só para manter o mesmo throughput.

> [!important] A consequência cruel: latência alta força uma escolha
> Reescreva a lei como **throughput = concorrência ÷ latência**. Sua concorrência é teto fixo — o pool tem N conexões, o servidor tem N threads. Se a latência **dobra** (a dependência ficou lenta, o GC pausou, o banco engasgou) e a concorrência não pode subir, o throughput **cai pela metade**. Você não tem terceira opção: ou aceita menos throughput, ou aumenta a concorrência (mais conexões, mais threads). E aumentar concorrência tem custo e limite — pools esgotam, threads competem por CPU. É exatamente por isso que **timeouts e tamanho de pool** em [[14 - Resiliência de rede]] são decisões acopladas: um pool pequeno com latência alta vira gargalo silencioso, e requests novas ficam esperando conexão livre em vez de serem atendidas.

## Bandwidth-delay product: o que cabe no cano

Se a Lei de Little conta requests em voo, o **bandwidth-delay product (BDP)** conta **bytes** em voo. É quanto dado cabe "dentro do cano" entre você e o outro lado a qualquer instante:

> BDP = bandwidth × RTT

É a mesma ideia da Lei de Little aplicada a bits: o cano tem um comprimento (o RTT) e uma largura (a bandwidth), e o volume que ele comporta cheio é o produto dos dois. Voltando à analogia da mangueira: uma mangueira grossa e comprida segura muito mais água parada lá dentro que uma fina e curta — mesmo que as duas, em regime, deixem passar o mesmo tanto por segundo.

Por que isso importa de verdade? Por causa do **TCP**. O TCP só pode ter um certo volume de dados não confirmados em trânsito antes de parar e esperar os ACKs — esse é o tamanho da **janela** (ver window scaling em [[02 - TCP]]). Se a janela for **menor** que o BDP, o emissor enche o que a janela permite, trava, e fica ocioso esperando confirmação enquanto o cano ainda tinha espaço de sobra. **Você desperdiça banda por causa da latência.**

Exemplo concreto. Um link de **1 Gbps** com RTT de **100 ms** (0,1 s):

| Grandeza | Valor |
| --- | --- |
| Bandwidth | 1 Gbps = 1.000.000.000 bits/s |
| RTT | 0,1 s |
| **BDP** | **10⁸ bits ÷ 8 = 12,5 MB** |

Para encher esse canal, o TCP precisa de uma janela de **12,5 MB** em voo. Mas o cabeçalho TCP original limita a janela a **65.535 bytes (~64 KB)** — quase 200× menor que o necessário. Sem a extensão de **window scaling** (RFC 1323/7323), esse link de 1 Gbps entregaria uma fração ridícula da sua capacidade.

> [!note] Rede longa e gorda (long fat network, LFN)
> Uma rede com BDP grande — alta banda **e** alto RTT — é uma **long fat network**. "Gorda" (fat) pela banda larga, "longa" (long) pelo RTT alto. Pela RFC 1072, é LFN quando o BDP passa de ~10⁵ bits (~64 KB), exatamente o ponto em que o window scaling deixa de ser opcional. Transferência intercontinental de alto volume (replicação de banco entre continentes, backup cross-region) é o caso clássico: a física do RTT exige janelas grandes, e sem elas a banda fica subutilizada. É a latência sabotando o throughput por baixo dos panos.

## Bufferbloat: quando mais buffer piora tudo

Intuição ingênua: "buffer maior é melhor, perco menos pacotes". Errado, e de um jeito que derruba entrevistado. Buffers grandes demais em roteadores, modems e placas causam **bufferbloat** — latência inchada sob carga.

A mecânica: quando o gargalo do caminho é um link lento (seu upload doméstico, por exemplo), os pacotes chegam mais rápido do que saem. Com um buffer pequeno, o excesso é **descartado** cedo — e o TCP, vendo a perda, **desacelera** (é assim que ele descobre congestionamento). Com um buffer **gigante**, nada é descartado: os pacotes se **empilham na fila**. O TCP não recebe sinal de congestionamento, continua mandando, e a fila cresce até segundos de espera. Resultado: enquanto um download satura o link, seu ping para tudo dispara — videochamada engasga, jogo trava, SSH fica intragável.

```mermaid
flowchart TD
    SRC["Trafego chega rapido<br/>(download saturando)"] --> BUF

    subgraph BUF["Buffer GIGANTE no roteador/modem"]
        Q["Fila enchendo...<br/>pacote 1, 2, 3 ... 5000<br/>(segundos de espera acumulados)"]
    end

    BUF --> LINK["Link lento (gargalo)<br/>sai devagar"]

    Q -. "nada descartado<br/>=> TCP nao ve perda<br/>=> nao desacelera" .-> Q
    LINK --> RTT["RTT de TODO o trafego<br/>incha: ping de 20 ms vira 1-2 s"]

    style BUF fill:#c62828,color:#fff
    style Q fill:#b71c1c,color:#fff
    style RTT fill:#6a1b1c,color:#fff
    style LINK fill:#ef6c00,color:#fff
```

Leitura do diagrama: o tráfego chega mais rápido do que o link lento consegue escoar. Num mundo são, o excesso seria descartado e o TCP frearia. Aqui o buffer gigante (vermelho) absorve tudo e a fila só cresce — sem descarte, o TCP nunca recebe o sinal de "pare". A conta é paga por **todo** o tráfego que atravessa essa fila: o RTT de coisas que nem têm a ver com o download (ping, VoIP) incha junto.

> [!warning] Mais buffer não é mais robustez — é mais latência
> O instinto de "aumentar o buffer para não perder pacote" é uma armadilha. Descarte de pacotes não é só perda: é o **mecanismo de sinalização** que o TCP usa para descobrir que precisa frear. Buffers excessivos sequestram esse sinal e trocam perda (recuperável, barata) por latência crônica (que arruína toda aplicação interativa). A mitigação correta é **AQM** (Active Queue Management): algoritmos como **CoDel** (Controlled Delay, 2012) e **FQ-CoDel/CAKE** descartam ou marcam pacotes cedo, mantendo a fila curta de propósito. A regra mental: a solução para fila cheia não é fila maior — é fila gerenciada.

## O piso geográfico: a luz não negocia

A componente de **propagação** do RTT (vista lá em cima) tem um piso que nenhuma engenharia atravessa. A luz no vácuo anda a ~300.000 km/s, mas na fibra ela vai a ~**200.000 km/s** — cerca de **2/3 de c**, porque o índice de refração do vidro (~1,46–1,5) freia o sinal. Esse número é a régua para estimar latência intercontinental de cabeça.

Faça a conta para **São Paulo ↔ Virgínia (Norte)**, um par real (a maior região AWS, us-east-1, fica na Virgínia). A distância de fibra é da ordem de **7.500 km** só de ida:

| Etapa | Conta | Resultado |
| --- | --- | --- |
| Distância (ida) | — | ~7.500 km |
| Velocidade na fibra | ~200.000 km/s | — |
| Propagação (ida) | 7.500 ÷ 200.000 | ~37,5 ms |
| **Piso de RTT (ida e volta)** | ×2 | **~75 ms** |

E isso é o **piso teórico**, em linha reta, **antes** de somar processamento de roteadores, filas, retransmissões e os desvios reais do cabeamento (que nunca é reto). Na prática o RTT real fica acima disso — fácil 110–130 ms. Mas o piso de ~75 ms é **físico**: nenhum servidor mais rápido, nenhuma otimização de código, nenhum dinheiro o derruba abaixo do que a luz permite.

> [!important] Por que esse piso justifica edge e CDN
> Se um usuário em São Paulo busca conteúdo de um servidor na Virgínia, **cada round-trip** já nasce com ~75 ms de piso só de propagação. Encadeie um handshake TCP + TLS + a request HTTP e são vários RTTs empilhados — centenas de milissegundos antes do primeiro byte útil. A única saída é **encurtar a distância física**: pôr o conteúdo num edge em São Paulo derruba a propagação para ~poucos ms. Não é luxo de performance; é a física obrigando arquitetura. Esse é o argumento de fundação de [[13 - Load balancing e CDN]] — você não vence a velocidade da luz, você foge dela aproximando-se do usuário.

## Percentis na prática: por que a média mente (de novo)

Já vimos que a média esconde a cauda. Na prática, o senior não relata "latência média"; relata uma **distribuição** de percentis:

- **p50** (mediana): metade das requests é mais rápida que isso. É o "caso típico" — e por isso é o que a média *finge* representar, mas não representa quando a distribuição é torta (e latência de rede sempre é torta, com cauda longa à direita).
- **p95 / p99**: o que 95% / 99% das requests ficam abaixo. É onde mora a dor real. Um p99 de 800 ms diz que 1 em 100 requests passa de 800 ms.
- **p99.9** (três noves): 1 em 1000. Parece paranoia, até você lembrar que um usuário ativo faz centenas de requests por sessão — e cada uma é uma chance de cair na cauda.

> [!tip] Por que a média é inútil para SLO
> A média é puxada para baixo pela maioria rápida e mascara o pequeno grupo que sofre. Duas distribuições com a **mesma média** podem ter p99 dez vezes diferentes. Você define SLO em percentil ("p99 < 300 ms"), nunca em média, justamente porque é a cauda que gera ticket de suporte e usuário irritado.

E aqui o gancho com o **fan-out** já visto: o p99 de uma dependência não fica contido nela. Sob fan-out, **o p99 da dependência vira o p50 — o caso típico — do seu serviço**. A matemática é a mesma de "The Tail at Scale": se sua request espera por muitos backends, basta um cair na cauda para a resposta inteira herdar essa lentidão, e com backends suficientes isso acontece na *maioria* das requests. Ou seja: a cauda de quem você chama promove-se a mediana de quem chama. Otimizar só a média da sua dependência não adianta — é a cauda dela que define a sua experiência.

## Em entrevista

In interviews, define the three terms crisply: latency is the time for one operation, throughput is volume per second, and bandwidth is the channel's ceiling — you can have high bandwidth and high latency at the same time (satellite links). I always mention that cross-continent latency has a physical floor set by the speed of light in fiber, roughly 1 ms per 100–200 km, which no amount of money buys away — that is why CDNs move content physically closer. I lean on the "latency numbers every programmer should know" hierarchy as orders of magnitude, not memorized constants: the jumps from cache to RAM to SSD to network are what drive caching, co-located databases, and minimizing round-trips. For senior signal, I bring up tail latency — the average lies, p99 is what users feel, and fan-out amplifies the tail, so a request touching 100 backends tends toward one backend's p99; under fan-out, a dependency's p99 effectively becomes your service's p50. I tie the three concepts together with Little's Law: concurrency equals throughput times latency (L = λ × W), so 1000 RPS at 200 ms means 200 requests in flight — that's what sizes your thread or connection pool, and if latency rises with a fixed pool, throughput must drop. I mention the bandwidth-delay product (bandwidth × RTT) to explain long fat networks: on a high-bandwidth, high-RTT link the TCP window must be large enough to fill the pipe, or latency silently caps throughput — which is why TCP window scaling exists. I also flag bufferbloat as a counterintuitive trap: oversized buffers don't add robustness, they inflate latency under load because they hide the packet loss TCP relies on to slow down, and AQM like CoDel is the fix. Finally I state the round-trip rule, and I always anchor the physical floor: light in fiber travels at roughly 200,000 km/s (about two-thirds of c), so São Paulo to Virginia carries a ~75 ms one-way propagation floor before any processing — no money buys that away, which is the whole reason edge and CDN exist. A concrete story (a 1.5 s endpoint cut to 200 ms by parallelizing three sequential HTTP calls) lands this well.

### Vocabulário

- latência → latency
- vazão / volume por segundo → throughput
- largura de banda / capacidade do canal → bandwidth
- ida-e-volta → round-trip (RTT)
- tempo de propagação → propagation delay
- atraso de fila → queuing delay
- velocidade da luz na fibra → speed of light in fiber
- lei de Little → Little's Law
- requests em voo / concorrência → in-flight requests / concurrency
- produto banda-atraso → bandwidth-delay product (BDP)
- rede longa e gorda → long fat network (LFN)
- janela TCP / escalonamento de janela → TCP window / window scaling
- inchaço de buffer → bufferbloat
- gerenciamento ativo de fila → active queue management (AQM)
- cauda de latência → tail latency
- percentil 99 → 99th percentile (p99)
- percentil de cauda → tail percentile
- amplificação por fan-out → fan-out amplification
- chamadas em série → serial / sequential calls
- chamadas em paralelo → parallel calls
- agrupar em lote → to batch
- requisições redundantes → hedged requests
- ordem de grandeza → order of magnitude
- gargalo → bottleneck

> [!info] Lastro
> - [Latency Numbers Every Programmer Should Know — gist jboner/2841832](https://gist.github.com/jboner/2841832) (números canônicos, atribuídos a Jeff Dean / Peter Norvig)
> - [Colin Scott — Latency Numbers (interactive, por ano)](https://colin-scott.github.io/personal_website/research/interactive_latency.html) (mostra como os números envelhecem com o hardware)
> - Dean, J. & Barroso, L. A. — ["The Tail at Scale", CACM 56(2), 2013, pp. 74–80](https://www.semanticscholar.org/paper/The-tail-at-scale-Dean-Barroso/0831a5baf38c9b3d43c755319a602b15fc01c52d) (p99, fan-out, hedged requests)
> - Grigorik, I. — [High Performance Browser Networking, cap. "Primer on Latency and Bandwidth"](https://hpbn.co/primer-on-latency-and-bandwidth/) (componentes do RTT, velocidade da luz na fibra ~66% de c)
> - [Little's Law — Modal GPU Glossary](https://modal.com/gpu-glossary/perf/littles-law) e [Using Little's Law to scale applications — Dan Slimmon](https://blog.danslimmon.com/2022/06/07/using-littles-law-to-scale-applications/) (L = λW; concorrência = throughput × latência; dimensionamento de pool)
> - [Bandwidth-delay product — Wikipedia](https://en.wikipedia.org/wiki/Bandwidth-delay_product) e [TCP window scale option — Wikipedia](https://en.wikipedia.org/wiki/TCP_window_scale_option) (BDP = banda × RTT; LFN > ~64 KB exige window scaling; RFC 1072/7323)
> - [Bufferbloat FAQs — Bufferbloat.net](https://www.bufferbloat.net/projects/bloat/wiki/Bufferbloat_FAQs/) e [Fighting Bufferbloat with FQ_CoDel — OPNsense](https://docs.opnsense.org/manual/how-tos/shaper_bufferbloat.html) (buffers inflam latência sob carga; CoDel/FQ-CoDel/CAKE como AQM)
> - [Calculating Optical Fiber Latency — M2 Optics](https://www.m2optics.com/blog/bid/70587/calculating-optical-fiber-latency) (luz na fibra ~200.000 km/s; índice de refração ~1,46–1,5)

## Veja também

- [[02 - TCP]] — handshake e slow start custam RTTs antes do primeiro byte útil
- [[08 - Caching HTTP]] — caching como forma de pular o salto caro da pirâmide
- [[13 - Load balancing e CDN]] — aproximar fisicamente para vencer a propagação
- [[04 - DNS]] — escolhe o edge mais próximo; também adiciona RTTs
- [[14 - Resiliência de rede]] — timeouts e retries que domam a cauda
- [[15 - Redes em entrevista]] — capstone com o caso do endpoint de 1,5 s → 200 ms
- [[System Design]] — onde esses números viram decisões de arquitetura
- [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]]
