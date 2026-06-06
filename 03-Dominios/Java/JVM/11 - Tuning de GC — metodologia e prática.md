---
title: "Tuning de GC — metodologia e prática"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - jvm
  - magus
  - gc
  - tuning
aliases:
  - "Tuning de GC"
  - "GC tuning"
  - "MaxGCPauseMillis"
---

# Tuning de GC — metodologia e prática

> [!abstract] TL;DR
> Tuning de GC não é uma coleção de flags — é **mover o ponto de operação no triângulo latência × throughput × footprint**, onde melhorar dois eixos quase sempre piora o terceiro. O método é o de qualquer engenharia orientada a medição: **baseline com GC log → meta explícita e mensurável → UMA mudança por vez → medir sob carga real → repetir**. A maioria dos "tunings" encontrados em produção é cargo cult — flags coladas de blog sem baseline, misturando coletores e versões. E às vezes a resposta certa não é tunar: é **trocar de coletor** ou **consertar o código** que aloca demais.

## O que é

Tuning de GC é o processo de ajustar o comportamento do coletor para que o perfil de execução da JVM atenda a um requisito **medido** — de latência, de throughput ou de consumo de memória. A palavra-chave é *medido*: sem um número de partida e um número de chegada, não existe tuning; existe superstição com sintaxe de flag.

O espaço de decisão é um triângulo com três eixos que puxam em direções opostas:

- **Latência** — quanto tempo as pausas STW roubam de cada request. Medida em percentis (p99, p999) e pior caso, nunca em média. É o eixo que aparece no SLA de serviços online.
- **Throughput** — fração do tempo total que a aplicação passa fazendo trabalho útil, em vez de coletar lixo. A documentação da Oracle formaliza isso no Parallel via `-XX:GCTimeRatio=<N>`: a meta é gastar no máximo `1/(1+N)` do tempo em GC (default 99 → 1% em GC). É o eixo que importa em batch e ETL.
- **Footprint** — quanta memória o processo realmente consome. Coletores low-pause precisam de *headroom* (folga de heap) para operar concorrentemente; heap maior também significa conta de cloud maior e menos pods por nó.

A regra prática do triângulo: **escolha dois**. Pausas curtas com throughput alto exigem heap e CPU de sobra (footprint paga). Footprint mínimo com throughput alto aceita pausas longas (latência paga). Pausas curtas com footprint apertado fazem o coletor correr atrás da alocação — e o throughput paga, às vezes com *allocation stalls*.

Tuning, portanto, é responder três perguntas em ordem: (1) em qual ponto do triângulo o sistema está **hoje** (baseline)? (2) em qual ponto o SLA **exige** que ele esteja (meta)? (3) qual é a **menor mudança** que move o ponto na direção certa — e quanto ela custa nos outros eixos?

## Por que importa

É um dos divisores mais nítidos entre senior e cargo cult.

**O anti-pattern dominante em produção é a flag colada de blog.** Um `JAVA_OPTS` herdado com oito flags de origens diferentes — metade da era Java 8, uma de coletor removido, duas contraditórias entre si — e ninguém no time sabe dizer qual problema cada uma resolvia, nem se resolvia. Sem baseline, é impossível saber se aquela config ajuda, atrapalha ou é ruído. E como remover flag "que sempre esteve aí" assusta, o lixo se acumula por anos, atravessando upgrades de JDK até o dia em que uma flag morta derruba a JVM no deploy.

**A metodologia vale mais que decorar flags.** O catálogo de flags muda a cada release; heurísticas internas dos coletores mudam mais ainda (o IHOP do G1, por exemplo, é adaptativo por default — um valor manual que fazia sentido no Java 8 hoje compete com a heurística). O que não muda é o método: medir, declarar meta, mudar uma coisa, medir de novo. Quem domina o método consegue tunar um coletor que ainda não existe; quem decorou flags fica refém do ano em que o blog foi escrito.

**Em entrevista, a pergunta "como você faria tuning de GC?" não está pedindo flags** — está testando se o candidato responde com processo ("primeiro eu capturo um GC log sob carga real e defino a meta...") ou com receita ("eu setaria MaxGCPauseMillis=50 e..."). A segunda resposta, sem a primeira, reprova.

## Como funciona

### O triângulo (latência/throughput/footprint) e o que seu SLA realmente pede

Antes de tocar em qualquer flag, traduza o requisito de negócio para um eixo do triângulo:

| Perfil do sistema | Eixo dominante | O que o SLA realmente pede |
|---|---|---|
| API síncrona com SLA de p99 | **Latência** | pausa de GC máxima que cabe no orçamento do p99 |
| Batch/ETL noturno | **Throughput** | % máximo do tempo total gasto em GC (trabalho/hora) |
| Sidecar, função serverless, pod denso | **Footprint** | RSS máximo do processo; pausas e throughput negociáveis |

O Parallel GC explicita essa hierarquia na própria documentação: ele atende as metas **nesta ordem** — primeiro a meta de pausa (`-XX:MaxGCPauseMillis`, que no Parallel é um *hint* sem valor default), depois a de throughput (`-XX:GCTimeRatio`), e só com as duas satisfeitas considera reduzir footprint. Essa ordem é um bom modelo mental para qualquer coletor: **declare qual eixo é inegociável e deixe os outros dois flutuarem**.

O erro comum é pedir os três: "quero p99 baixo, throughput máximo e o menor heap possível". Isso não é meta, é desejo. A meta de verdade tem a forma: *"pausa de GC p99 < 150ms, aceitando até 5% de throughput a menos e até 20% de heap a mais"*.

### Metodologia disciplinada

O loop completo, na ordem — pular etapa invalida o resultado:

**1. Baseline com GC log.** Capture `-Xlog:gc*` sob **carga representativa** (produção ou réplica fiel — a leitura do log está em [[10 - GC logs — unified logging e leitura]]). Extraia: distribuição de pausas (p50/p99/pior caso), frequência de coletas, ocorrência de Full GC / evacuation failure, % do tempo em GC, heap após coletas (live-set aproximado). Guarde o arquivo — ele é o "antes" de toda comparação futura.

**2. Meta explícita e mensurável.** Um número, com unidade e percentil: "pausa p99 < 150ms", "tempo em GC < 2% do total", "RSS < 1,5 GB". Se a baseline já cumpre a meta, **não há tuning a fazer** — encerrar aqui é o resultado mais comum e mais subestimado do processo.

**3. UMA mudança.** Uma flag, ou uma troca de coletor, ou um fix de código — nunca duas coisas na mesma rodada. Com duas mudanças simultâneas, o efeito observado não é atribuível a nenhuma delas, e o conhecimento gerado é zero.

**4. Medir sob carga real.** Mesmo workload, mesma duração, mesmo hardware da baseline. Compare as mesmas métricas do passo 1 — e olhe os **três eixos**, não só o que você queria melhorar: a pausa caiu, mas o throughput foi junto? O heap cresceu?

**5. Repetir — ou parar.** Meta atingida → documente a flag, o porquê, o log de antes e o de depois (o futuro time agradece quando for auditar o `JAVA_OPTS`). Meta não atingida após 2–3 rodadas honestas → o problema provavelmente não se resolve com tuning fino: é troca de coletor, mais recurso, ou código (seções adiante).

### Tuning de G1

A recomendação geral da Oracle é deselegante de tão simples: **use o G1 com defaults, ajustando no máximo a meta de pausa e o tamanho do heap** (`-Xmx`/`-Xms`). E, ao migrar de outro coletor, **comece removendo todas as flags de GC antigas**, não acumulando por cima. Os diais, quando o log justificar:

**`-XX:MaxGCPauseMillis` — o dial principal, e seu custo.** Define a meta de pausa (default 200ms). O G1 a cumpre principalmente **redimensionando a young generation**: meta menor → young menor → pausas mais curtas, porém mais frequentes. O custo é real e documentado: o controle de pausa "incorre em overhead tanto nas threads da aplicação quanto na eficiência de reclamação de espaço". Meta agressiva demais (10–50ms num heap de vários GB) faz o throughput despencar em troca de pausas que o G1 talvez nem consiga entregar — abaixo de certo ponto, a resposta certa é ZGC, não um número menor aqui. No sentido inverso, se o que falta é throughput, a doc manda **relaxar** a meta de pausa ou dar mais heap.

**`-XX:G1HeapRegionSize` — quando humongous incomoda.** Objetos ≥ metade de uma região viram *humongous* (caros, ver [[06 - Os coletores do HotSpot]]). Se `gc+heap=info` mostra muitas regiões humongous comparadas às regiões old, a doc oferece duas saídas: reduzir essas alocações no código (melhor) ou **aumentar o tamanho da região** com esta flag, para que os mesmos objetos deixem de ser humongous. Efeito colateral documentado: regiões maiores tendem a ter menos referências cruzadas, encolhendo as remembered sets (menos memória auxiliar) — mas também reduzem a granularidade com que o G1 trabalha.

**`-XX:InitiatingHeapOccupancyPercent` (IHOP) — marcação cedo ou tarde demais.** O IHOP define a ocupação do heap que dispara o ciclo de marcação concorrente. **Por default ele é adaptativo**: o G1 calcula o limiar sozinho a partir do comportamento observado. Os dois modos de falha:

- *Marcação tarde demais*: a marcação não termina antes do heap encher → evacuation failure → Full GC. Fixes documentados: aumentar o buffer da heurística via `-XX:G1ReservePercent`, ou desligar a adaptação (`-XX:-G1UseAdaptiveIHOP`) e fixar `-XX:InitiatingHeapOccupancyPercent` num valor menor — marcação começa mais cedo.
- *Marcação cedo demais* (IHOP manual baixo demais): ciclos concorrentes constantes queimando CPU para reclamar quase nada — throughput pago à toa.

Importante: setar `InitiatingHeapOccupancyPercent` **sem** desligar o modo adaptativo tem efeito limitado — em JDKs modernos o valor manual serve de ponto de partida da heurística, não de limiar fixo.

O que **não** fazer no G1 é explícito na doc: evitar `-Xmn`, `-XX:NewRatio` e afins, porque fixar a young "sobrescreve e na prática desabilita o controle de tempo de pausa" — a young dimensionável é o mecanismo central do coletor.

### Tuning de ZGC

A filosofia do ZGC é oposta à do G1 em quantidade de diais: ele "foi projetado para ser adaptativo e exigir configuração manual mínima" — redimensiona gerações, escala threads de GC e ajusta tenuring sozinho. Sobram pouquíssimas decisões, todas de **dimensionamento**:

**Heap (`-Xmx`) — a opção de tuning mais importante, segundo a própria doc.** Como o ZGC coleta concorrentemente, o heap precisa acomodar o live-set **mais headroom** suficiente para servir alocações *enquanto o GC roda*. Heap justo demais → o coletor não acompanha a taxa de alocação → **allocation stalls**: threads da aplicação param esperando memória, e a latência que o ZGC prometeu eliminar volta por outra porta. Regra da doc: "quanto mais memória você der ao ZGC, melhor" — equilibrado contra o desperdício.

**`-XX:SoftMaxHeapSize` — limite suave, não teto.** Define o tamanho que o ZGC vai *se esforçar* para não ultrapassar — mas ele **pode** crescer além, até o `-Xmx`, se isso for necessário para evitar stall da aplicação. Exemplo da doc: `-Xmx5g -XX:SoftMaxHeapSize=4g` → heurísticas miram 4 GB, com 1 GB de válvula de escape temporária. É a flag ideal para manter footprint baixo (pods densos, billing por RAM) sem abrir mão da margem de segurança nos picos.

**CPU para as fases concorrentes.** O trabalho que no Parallel acontecia dentro da pausa, no ZGC acontece em threads concorrentes competindo pelos mesmos cores da aplicação. Dimensionar CPU é parte do tuning: numa máquina saturada, o ZGC degrada — sem cores para marcar e realocar, vêm os stalls. Detalhes operacionais relacionados: por default o ZGC **devolve memória não usada ao SO** (uncommit, delay default de 300s via `-XX:ZUncommitDelay`); se latência extrema é o objetivo, a doc recomenda o oposto — `-Xms` = `-Xmx`, `-XX:+AlwaysPreTouch` e desligar uncommit (`-XX:-ZUncommit`) para eliminar o custo de commit/uncommit em runtime.

### Quando TROCAR de coletor em vez de tunar

Tuning move o ponto de operação **dentro do envelope** de um coletor; se a meta está fora do envelope, nenhuma flag alcança. Sinais de que o perfil não fecha e a resposta é trocar (catálogo e critérios em [[06 - Os coletores do HotSpot]]):

- **Meta de pausa abaixo do que o G1 entrega.** SLA pedindo pausas de poucos ms ou menos num heap grande: apertar `MaxGCPauseMillis` só destrói o throughput. O envelope certo é ZGC (ou Shenandoah, conforme o build).
- **Batch onde a pausa não importa e o G1 está "pagando por nada".** O overhead de controle de pausa do G1 é desperdício se ninguém espera resposta — Parallel entrega mais trabalho por hora.
- **Heap minúsculo em container de 1 vCPU.** As estruturas auxiliares do G1 pesam proporcionalmente; Serial tem o menor custo fixo.
- **CPU sem folga para coletor concorrente.** ZGC em máquina saturada vive de allocation stall; ou se aumenta CPU, ou se aceita um coletor com pausas (G1) que concentra o trabalho.

Troca de coletor é uma "mudança" no sentido do passo 3 da metodologia: uma por rodada, com baseline antes e medição depois — nos três eixos.

### Quando o problema NÃO é GC

Os dois cenários em que tunar o coletor é tratar sintoma:

**Alocação excessiva → consertar o código.** Se o GC log mostra coletas young a cada poucos segundos com taxa de alocação altíssima, o coletor está fazendo o trabalho dele — quem está errado é a aplicação. Causas típicas: objetos temporários em loop quente, conversões/boxing desnecessários, buffers realocados a cada request, logging que constrói strings gigantes mesmo com o nível desligado. Nenhuma flag reduz alocação; um profiler de alocação (JFR, [[13 - JFR e JMC — observabilidade de produção]]) aponta os sites de alocação dominantes, e o fix é no código. É frequentemente o tuning de maior retorno — e o único que melhora os três eixos ao mesmo tempo.

**Memory leak → heap dump, não heap maior.** Se o heap ocupado **após** Full GC cresce monotonicamente ao longo de horas/dias, não há o que tunar: objetos vivos (alcançáveis) não são responsabilidade do coletor. Aumentar `-Xmx` só agenda o OOM para mais tarde — e de brinde alonga as pausas até lá. O caminho é diagnóstico: heap dump e análise de dominators ([[12 - Diagnóstico — heap dumps, thread dumps e jcmd]]).

O teste rápido para distinguir: olhe o heap depois das coletas completas no log. **Estável** → o live-set é esse mesmo; problema (se houver) é alocação ou dimensionamento. **Crescendo sem teto** → leak; tuning não se aplica.

### Resumo dos diais (referência rápida)

| Flag | Coletor | O que faz | Quando o log justifica |
|---|---|---|---|
| `-Xmx` / `-Xms` | todos | tamanho do heap — o fator nº 1 de performance de GC segundo a Oracle | sempre o primeiro dial; iguais entre si para previsibilidade |
| `-XX:MaxGCPauseMillis` | G1 (default 200ms); Parallel (hint, sem default) | meta de pausa; G1 cumpre encolhendo a young | pausas estourando SLA **ou** relaxar quando falta throughput |
| `-XX:GCTimeRatio` | Parallel (default 99 → 1% em GC); G1 (default 12 → ~8%) | meta de throughput: máx `1/(1+N)` do tempo em GC | batch onde % de tempo em GC é a métrica que importa |
| `-XX:G1HeapRegionSize` | G1 | tamanho das regiões; objetos ≥ metade viram humongous | `gc+heap=info` mostrando muitas regiões humongous |
| `-XX:InitiatingHeapOccupancyPercent` (+ `-XX:-G1UseAdaptiveIHOP`) | G1 | ocupação que dispara a marcação concorrente (adaptativo por default) | evacuation failure / Full GC por marcação tardia |
| `-XX:SoftMaxHeapSize` | ZGC | limite *suave* — heurísticas miram nele, mas podem estourar até `-Xmx` para evitar stall | footprint apertado com necessidade de margem nos picos |

A tabela é referência, não receita: **nenhuma linha dela se aplica sem o log que a justifique**.

## Na prática

### Cenário completo — mixed pauses estourando o p99

```text
// hipotético: serviço de pedidos (OrderService), Java 21, G1 default,
// -Xmx8g, ~1.200 req/s em pico. SLA: p99 da API < 300ms.
// Sintoma: p99 estourando para 600-900ms em janelas de ~1 minuto, algumas vezes por hora.
```

**Passo 1 — baseline.** GC log (`-Xlog:gc*:file=gc.log:time,uptime,level,tags`) coletado por 24h sob carga real. Leitura:

```text
// hipotético: trechos relevantes da baseline
[…] GC(811) Pause Young (Normal) (G1 Evacuation Pause) 4811M->4302M(8192M) 38.112ms
[…] GC(847) Pause Young (Mixed) (G1 Evacuation Pause) 6913M->4870M(8192M) 412.339ms
[…] GC(848) Pause Young (Mixed) (G1 Evacuation Pause) 6101M->4955M(8192M) 388.516ms
[…] GC(902) To-space exhausted          ← 2 ocorrências em 24h
```

Diagnóstico da baseline: pausas young normais saudáveis (p99 ~45ms), mas **mixed collections de 350–450ms** em rajadas — coincidem com as janelas de p99 estourado. As duas ocorrências de `To-space exhausted` indicam que a **marcação concorrente está começando tarde**: quando o ciclo termina, a old já está cheia demais, e o G1 precisa de mixed pauses grandes e urgentes para recuperar espaço.

**Passo 2 — meta.** Pausa de GC p99 < **150ms**, aceitando até 3% de throughput a menos e zero `To-space exhausted` em 24h.

**Passo 3 — UMA mudança.** Das opções na mesa (relaxar/apertar `MaxGCPauseMillis`, mexer no IHOP, aumentar heap), a hipótese formada pela baseline aponta para marcação tardia. Mudança escolhida, conforme a doc do G1 para esse sintoma: desligar o IHOP adaptativo e antecipar a marcação.

```bash
# hipotético: a única mudança da rodada 1
java -Xmx8g \
  -XX:-G1UseAdaptiveIHOP -XX:InitiatingHeapOccupancyPercent=35 \
  -Xlog:gc*:file=gc.log:time,uptime,level,tags:filecount=5,filesize=20m \
  -jar order-service.jar
```

**Passo 4 — medir.** Mesmas 24h de perfil de carga:

```text
// hipotético: depois da mudança
- Marcação concorrente: 2,1x mais frequente (esperado — começa mais cedo)
- Mixed pauses: máx 142ms, p99 118ms (antes: 350-450ms)
- To-space exhausted: 0 ocorrências
- Throughput: -1,8% (dentro do orçamento de 3%)
- p99 da API: 240ms — dentro do SLA de 300ms
```

**Passo 5 — decisão.** Meta atingida na primeira rodada. Para: a flag é documentada no repositório com o porquê, o log de antes e o de depois ficam arquivados como evidência, e **nenhuma outra flag é adicionada** — a tentação de "já que estamos aqui, otimizar mais" é o começo do cargo cult. Custo aceito e registrado: ciclos de marcação mais frequentes (CPU) e -1,8% de throughput, em troca do p99.

### Anti-exemplo — o JAVA_OPTS de cargo cult

O bloco abaixo é o tipo de config que se encontra em Dockerfile herdado — oito flags coladas de blogs de épocas diferentes, sem baseline, sem meta, sem autor:

```bash
# hipotético: JAVA_OPTS herdado — NÃO copiar; desmonte linha a linha abaixo
java \
  -XX:+UseG1GC \
  -XX:+UseConcMarkSweepGC \
  -XX:CMSInitiatingOccupancyFraction=70 \
  -Xmn2g \
  -XX:NewRatio=3 \
  -XX:MaxGCPauseMillis=10 \
  -XX:GCTimeRatio=99 \
  -XX:+AggressiveOpts \
  -jar customer-api.jar
```

O desmonte, flag a flag:

| Flag | Veredito |
|---|---|
| `-XX:+UseG1GC` | Inócua — G1 já é default desde o Java 9. Só documenta intenção... que as próximas sete contradizem. |
| `-XX:+UseConcMarkSweepGC` | **Fatal.** CMS foi removido no Java 14; em qualquer JDK moderno, a JVM **não sobe** (`Unrecognized VM option`). Também contradiz a flag anterior — dois coletores selecionados. |
| `-XX:CMSInitiatingOccupancyFraction=70` | **Fatal.** Flag satélite de um coletor que não existe mais. Mesmo na era CMS, sem `UseCMSInitiatingOccupancyOnly` ela era só um chute inicial. |
| `-Xmn2g` | **Sabotagem do G1.** A doc manda explicitamente evitar: fixar a young "praticamente desabilita o controle de tempo de pausa". A meta de pausa da linha de baixo vira decorativa. |
| `-XX:NewRatio=3` | Mesmo pecado da anterior — e **conflita com ela** (duas formas de fixar a young com valores potencialmente incompatíveis). |
| `-XX:MaxGCPauseMillis=10` | Meta irreal para um heap de serviço comum no G1. O coletor encolhe a young ao mínimo tentando cumprir, minors disparam, throughput despenca — e 10ms não chega. Se 10ms é requisito real, a resposta é ZGC, não este número. |
| `-XX:GCTimeRatio=99` | Default **do Parallel** (1% em GC) colado num contexto G1, onde o default é 12 (~8%). Junto com a meta de pausa de 10ms, declara duas metas mutuamente impossíveis — pausas mínimas E tempo de GC mínimo. |
| `-XX:+AggressiveOpts` | Flag morta — deprecada no JDK 11, obsoleta no 12 (emite warning), expirada no 13 (derruba a JVM com `Unrecognized VM option`); em qualquer JDK atual derruba a JVM. Nunca teve semântica estável: era um pacote de opções experimentais que mudava por release. |

Resultado líquido do bloco: **a JVM nem inicia** num JDK ≥ 14. E se as flags fatais fossem removidas, o resto ainda seria um G1 sabotado perseguindo metas contraditórias. O fix não é ajustar — é **zerar**: voltar para `-Xmx` + GC log, capturar baseline e só readicionar o que um log justificar.

## Armadilhas

### (1) Tunar sem baseline e sem meta

**O problema:** mudar flags "para ver se melhora" sem um GC log de antes nem um número-alvo. Qualquer resultado é ininterpretável: se o p99 caiu, foi a flag ou a carga que mudou? Se nada mudou, a flag é inócua ou o problema está em outro lugar? Sem baseline, até uma melhora real é indistinguível de ruído — e a flag fica lá para sempre, protegida pelo medo de remover.

```bash
# hipotético: "tuning" sem evidência — o resultado não ensina nada
java -XX:MaxGCPauseMillis=100 -Xmx6g -jar customer-api.jar
# Melhorou? Comparado com o quê? Medido onde?
```

**Fix:** GC log **antes** de qualquer mudança ([[10 - GC logs — unified logging e leitura]]) e meta numérica declarada (percentil + unidade). Se a baseline já cumpre a meta, o tuning acabou antes de começar.

---

### (2) MaxGCPauseMillis agressivo demais

**O problema:** tratar a meta de pausa do G1 como botão de "deixar rápido" e cravar 20–50ms num heap de vários GB. O G1 só tem uma alavanca principal para cumprir: **encolher a young**. Young minúscula → minors constantes → o overhead fixo de cada pausa se paga centenas de vezes por minuto → throughput despenca. A doc é explícita: o controle de pausa custa overhead nas threads da aplicação e na eficiência de reclamação — e meta irreal maximiza esse custo sem entregar a pausa pedida.

```bash
# hipotético: meta irreal — throughput cai, e os 20ms não acontecem
java -XX:MaxGCPauseMillis=20 -Xmx8g -jar order-service.jar
```

**Fix:** se o log mostra o G1 falhando a meta consistentemente, **relaxe a meta** (ou aumente o heap), conforme a recomendação da Oracle para throughput. Se a pausa exigida pelo SLA está genuinamente abaixo do envelope do G1, a resposta é trocar para ZGC — não torturar o dial.

---

### (3) "Resolver" leak com -Xmx maior

**O problema:** OOM ou heap crescendo → reflexo de dobrar o `-Xmx`. Se a causa é leak (objetos alcançáveis acumulando), heap maior só **adia o OOM** — agora ele acontece de madrugada do dia seguinte em vez de à tarde — e, de brinde, as coletas completas que varrem esse heap inflado ficam proporcionalmente mais longas. O sistema ganha um modo de falha pior: mais raro, mais lento e mais difícil de reproduzir.

```bash
# hipotético: o leak agradece o prazo estendido
java -Xmx16g -jar order-service.jar   # antes: -Xmx8g, OOM a cada ~20h
# resultado: OOM a cada ~40h, com Full GCs de pausa dobrada no caminho
```

**Fix:** o teste do live-set — heap ocupado após coletas completas crescendo sem teto = leak. Aí o caminho é heap dump e análise de dominators ([[12 - Diagnóstico — heap dumps, thread dumps e jcmd]]), nunca flag. `-Xmx` maior é legítimo apenas quando o live-set é **estável** e genuinamente maior que o heap atual comporta.

---

### (4) Tunar várias flags de uma vez

**O problema:** rodada de tuning que muda quatro flags juntas "para ganhar tempo". O resultado — bom ou ruim — não é atribuível a nenhuma delas: se melhorou, qual segurar? Se piorou, qual reverter? E interações entre flags são reais (uma young fixada anula a meta de pausa, um IHOP manual compete com a heurística adaptativa). O conhecimento gerado pela rodada é zero, e o `JAVA_OPTS` ganhou quatro inquilinos permanentes.

```bash
# hipotético: 4 mudanças, 0 conclusões possíveis
java -XX:MaxGCPauseMillis=100 -XX:G1HeapRegionSize=16m \
     -XX:InitiatingHeapOccupancyPercent=40 -XX:ConcGCThreads=4 \
     -jar order-service.jar
```

**Fix:** uma mudança por rodada, sempre — mesmo que cada rodada custe um ciclo de medição. É mais lento por rodada e muito mais rápido até a causa: cada medição produz uma conclusão definitiva sobre uma variável. Disciplina de experimento, não de pressa.

## Em entrevista

### Frase pronta (inglês)

> "I treat GC tuning as a measurement-driven loop, not a bag of flags. First I capture a GC log under realistic load and establish a baseline — pause percentiles, collection frequency, any Full GCs — and I state an explicit, measurable goal, like 'GC pause p99 under 150 milliseconds'. Then I change exactly one thing per iteration and re-measure under the same load, watching all three axes — latency, throughput, and footprint — because improving one almost always taxes another."

> "The flags themselves are secondary to the method, but the dials I reach for are well documented: on G1, MaxGCPauseMillis is the main one — and the trade-off is explicit, since G1 meets a tighter pause goal mostly by shrinking the young generation, which means more frequent collections and lower throughput; if marking starts too late and I see evacuation failures, I look at the adaptive IHOP. On ZGC there's much less to tune — it's mostly about heap sizing with enough headroom for the concurrent cycles, plus SoftMaxHeapSize when I want to keep the footprint down without losing the safety margin."

> "The caveat I always add: a lot of what looks like a GC problem isn't one. If allocation rate is the issue, the fix is in the code, not in the collector; if the live-set grows without bound, that's a leak and the answer is a heap dump, not a bigger Xmx. And sometimes the honest conclusion of the baseline is that the pause goal is simply outside the collector's envelope — then I switch collectors instead of torturing flags."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| linha de base | baseline |
| meta de tempo de pausa | pause-time goal |
| meta de throughput | throughput goal |
| folga de heap | heap headroom |
| limite suave de heap | soft maximum heap size |
| conjunto vivo (objetos alcançáveis) | live-set |
| falha de evacuação | evacuation failure |
| limiar de ocupação para marcação | initiating heap occupancy (IHOP) |
| parada por falta de alocação | allocation stall |
| pegada de memória | (memory) footprint |
| tuning por imitação sem evidência | cargo cult tuning |
| uma mudança por rodada | one change per iteration |

## Veja também

- [[03 - Garbage Collection — o conceito]]
- [[06 - Os coletores do HotSpot]]
- [[09 - Flags, ergonomics e a JVM em containers]]
- [[10 - GC logs — unified logging e leitura]]
- [[12 - Diagnóstico — heap dumps, thread dumps e jcmd]]
- [[14 - Performance da JVM — síntese]]
- [[03-Dominios/Java/JVM/index|JVM por dentro (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#G1 GC|G1 GC (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#ZGC (generational)|ZGC (Dicionário)]]

## Referências

- [Factors Affecting Garbage Collection Performance — Oracle GC Tuning Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/gctuning/factors-affecting-garbage-collection-performance.html) — heap total como fator dominante; `-Xms`/`-Xmx`; proporção da young generation
- [Garbage-First Garbage Collector Tuning — Oracle GC Tuning Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/gctuning/garbage-first-garbage-collector-tuning.html) — `MaxGCPauseMillis` e seu custo; `G1HeapRegionSize` para humongous; IHOP adaptativo, `G1UseAdaptiveIHOP`, `G1ReservePercent`; `GCTimeRatio` no G1 (default 12, fórmula `1/(1+N)`); aviso contra `-Xmn`/`NewRatio` no G1; recomendação de começar com defaults
- [The Z Garbage Collector — Oracle GC Tuning Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/gctuning/z-garbage-collector.html) — heap sizing como tuning principal; semântica do `SoftMaxHeapSize` (limite suave, não teto); uncommit (`ZUncommitDelay`, `-XX:-ZUncommit`); `AlwaysPreTouch` para latência extrema; design adaptativo do ZGC
- [The Parallel Collector — Oracle GC Tuning Guide (Java 21)](https://docs.oracle.com/en/java/javase/21/gctuning/parallel-collector1.html) — `GCTimeRatio` no Parallel (default 99 → 1% em GC); `MaxGCPauseMillis` como hint sem default; ordem de prioridade das metas (pausa → throughput → footprint)
