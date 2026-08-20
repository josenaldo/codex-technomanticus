---
title: "Quando NÃO fazer microservices"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: magus
tags:
  - java
  - microservices
  - magus
  - arquitetura
aliases:
  - "Quando não fazer microservices"
  - "Monólito modular"
  - "MonolithFirst"
---

# Quando NÃO fazer microservices

> [!abstract] TL;DR
> Microservices não é o estado natural de um sistema, é uma resposta a uma dor específica. Esta nota é a **contraparte** da tese honesta da nota 01: lá vimos *quando* a distribuição compensa; aqui vemos *quando ela custa caro demais* — e a resposta padrão na ausência dessa dor.
> - O distribuído cobra um **prêmio** (Fowler, *Microservice Premium*): rede não-confiável, consistência eventual, observabilidade distribuída, overhead operacional e complexidade cognitiva. Esse prêmio só se paga quando o monólito ficou grande/complexo demais para ser gerenciado.
> - O **default sensato é o monólito modular**: limites claros internos, deploy único, refatoração barata. Sam Newman o chama de subestimado e diz que microservices **não deve ser a escolha padrão**.
> - O caminho saudável é **modular → extração**: comece monólito (Fowler, *MonolithFirst*), descubra os limites na prática, e só extraia serviços com a **figueira estranguladora** (*strangler fig*) quando a dor justificar.
> - Decompõe-se por **capacidade de negócio / contexto delimitado** (DDD), nunca por camada técnica — decompor por camada gera o pior dos mundos, o **monólito distribuído**.
> - Sem dogma nos dois sentidos: nem "microservices pra tudo", nem "monólito pra sempre". A pergunta é *quando X e quando Y*.

## O que é

"Quando NÃO fazer microservices" é o exercício de **julgamento arquitetural** que fecha o arco aberto na nota 01. Lá a tese foi honesta: microservices resolvem problemas reais de escala organizacional e independência de deploy, mas trazem um custo. Aqui invertemos a lente e perguntamos: **na ausência desses problemas, qual é a arquitetura correta?**

A resposta da literatura madura é direta: **o monólito modular é o ponto de partida e o estado padrão**. Microservices é uma arquitetura que você *adota quando a precisa*, não a fundação sobre a qual você constrói por inércia ou por hype.

Três ideias-âncora sustentam o capítulo:

- **MonolithFirst** (Fowler, 2015) — comece como monólito, decomponha depois, porque os limites entre serviços são difíceis de acertar cedo. ([fonte](https://martinfowler.com/bliki/MonolithFirst.html))
- **Microservice Premium** (Fowler) — só compensa para sistemas complexos demais para serem gerenciados como monólito. ([fonte](https://martinfowler.com/bliki/MicroservicePremium.html))
- **Monólito modular subestimado** (Sam Newman) — microservices não é o default; o monólito modular bem feito entrega muito do que se busca, sem o prêmio do distribuído. ([fonte](https://www.infoq.com/news/2020/05/monolith-decomposition-newman/))

> [!info] Onde isto se encaixa na trilha
> A nota 01 deu a tese ("o que são e quando valem"). As notas intermediárias do galho deram o *como* (comunicação, dados, resiliência, observabilidade). Esta nota é o **capstone de julgamento**: ela pesa o custo acumulado de tudo que veio antes e devolve a pergunta ao leitor — *você realmente precisa disso?*

## Por que importa

Porque a decisão errada é cara nos dois sentidos, mas **assimetricamente**.

Escolher microservices cedo demais é o erro mais comum e mais doloroso. Você paga o prêmio antes de colher qualquer benefício: monta pipeline de deploy independente, observabilidade distribuída e tratamento de falha de rede para um sistema que ainda nem sabe se vai existir daqui a seis meses. Pior: você **congela limites de domínio** que ainda não entende, e mover funcionalidade entre serviços é ordens de magnitude mais caro do que mover entre módulos de um monólito.

> [!tip] A intuição de Fowler, em uma frase
> É mais fácil ter um sistema mal projetado *mas bem-sucedido* do que um sistema bem projetado *que fracassou*. Microservices prematuro otimiza a arquitetura à custa da velocidade de aprender — e velocidade de aprender é o que mantém o produto vivo antes do *product-market fit*.

A simetria do julgamento importa: **também não há virtude em manter um monólito que já doeu de verdade**. Se o time não cabe mais num deploy único, se domínios independentes brigam por um pipeline compartilhado, se a escala de um subsistema é radicalmente diferente do resto — aí o prêmio se paga. O ponto não é ser anti-microservices; é **não pagar antes da hora** e **extrair com critério**.

## Como funciona

### Os custos reais do distribuído (o prêmio)

O que Fowler chama de *Microservice Premium* é o conjunto de complexidades que deixam de ser opcionais no instante em que você cruza um limite de processo pela rede. Você as paga **mesmo que não use nenhum benefício de microservices**.

- **Rede não-confiável.** Uma chamada de método dentro do monólito não falha por timeout, não tem latência variável, não cai pela metade. Uma chamada entre serviços tem tudo isso. Cada fronteira de rede é um ponto de falha novo que você precisa tratar com retry, timeout, circuit breaker, fallback. (Veja [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|Consistência distribuída]].)
- **Consistência eventual.** No monólito, uma transação ACID abrange várias operações. Distribuído, você troca isso por saga, *outbox*, idempotência e janelas em que o sistema está temporariamente inconsistente. Isso não é detalhe de implementação: é uma mudança de modelo mental que contamina regras de negócio, UX e suporte.
- **Observabilidade distribuída.** Um stack trace local vira um *trace* distribuído que precisa correlacionar logs, métricas e spans de N serviços. Diagnosticar "por que o pedido falhou" deixa de ser ler um log e passa a ser reconstruir uma jornada que cruzou cinco processos.
- **Overhead operacional.** Deploy automatizado, *service discovery*, *config* centralizada, gestão de versões de contrato, infraestrutura de mensageria. Fowler é explícito: a maioria dos times não tem folga para arcar com isso de graça.
- **Complexidade cognitiva.** Talvez o custo mais silencioso. Entender o sistema deixa de ser ler um repositório e passa a ser segurar na cabeça um grafo de serviços, contratos e modos de falha. Cada engenheiro novo paga um pedágio maior.

> [!example] Feynman: o jantar em casa vs. o jantar em rede
> Cozinhar para a família num apartamento é o monólito: você fala "passa o sal" e o sal chega. Agora imagine cozinhar com cada ingrediente numa casa diferente da rua, e a única forma de pedir sal é mandar um bilhete pelo correio — que às vezes se perde, às vezes chega duas vezes, às vezes demora. O jantar *pode* ficar melhor se você é um restaurante com mil clientes e cozinhas especializadas. Mas se é só a família, você acabou de transformar "passa o sal" num projeto logístico. **Esse é o prêmio.**

### O monólito modular como default

A alternativa que a indústria redescobriu não é o "monólito espaguete" dos anos 2000 — é o **monólito modular**: um único processo de deploy, mas com **limites internos explícitos e respeitados** entre módulos.

Sam Newman é direto ao colocá-lo como subestimado e ao afirmar que microservices **não deveria ser a escolha padrão**, sendo particularmente inadequado para startups que ainda não têm experiência operacional de produção (parafraseado de seu argumento na [InfoQ](https://www.infoq.com/news/2020/05/monolith-decomposition-newman/)). O monólito modular entrega boa parte do que se busca em microservices — fronteiras de domínio claras, autonomia de equipe, evolução independente de cada módulo — **sem** pagar o prêmio do distribuído.

A chave é disciplina de fronteira:

- Cada módulo expõe uma **interface pública** estreita; o resto é privado.
- Módulos **não atravessam** o banco um do outro; conversam por API interna (chamada de método, não rede).
- A dependência entre módulos é **explícita e acíclica** — o que torna a futura extração barata, porque o limite já existe.

Quando os limites internos são bem desenhados, o monólito modular é a **plataforma de descoberta** ideal: você refatora fronteiras quase de graça enquanto ainda está aprendendo o domínio. É exatamente isso que o microservices prematuro destrói.

### O caminho modular → extração (strangler fig)

A evolução saudável não é um "big bang" de reescrita. É **incremental** e guiada por dor concreta.

1. **Comece monólito modular** (MonolithFirst). Descubra os contextos delimitados na prática, não no papel.
2. **Espere a dor.** Extração se justifica quando um módulo tem necessidade *real* divergente do resto: escala muito diferente, cadência de deploy conflitante, time que precisa de autonomia total, requisito de isolamento de falha.
3. **Extraia com a figueira estranguladora** (*strangler fig*, Newman/Fowler): coloque uma fachada que intercepta as chamadas ao módulo, redirecione gradualmente para o novo serviço, e remova o código antigo só quando o novo provou que funciona. Técnicas de apoio: *branching by abstraction*, *feature toggles* e *parallel run* (rodar os dois lados e comparar antes de cortar).
4. **Extraia um por vez.** Cada extração é validada em produção antes da próxima. Nunca decomponha tudo de uma vez.

> [!warning] O sinal de que algo deu errado
> Newman aponta um sintoma claro de fracasso: se você precisa de um "gerente de coordenação de release" em tempo integral para soltar suas mudanças, você não construiu microservices — construiu um **monólito distribuído**, que junta o overhead do distribuído com o acoplamento do monólito. É o pior dos dois mundos.

## Na prática

### Árvore de decisão: "devo extrair um serviço?"

```text
Pergunta de entrada: este módulo deve virar um serviço separado AGORA?

1. O produto já tem product-market fit / escala real?
   ├─ NÃO → PARE. Monólito modular. Você ainda está descobrindo o domínio.
   └─ SIM → continue.

2. Existe uma DOR concreta e atual neste módulo?
   ├─ NÃO → PARE. Não extraia por estética. Mantenha modular.
   └─ SIM → qual dor? continue.

3. A dor é uma destas?
   ├─ Escala radicalmente diferente do resto do sistema ............ candidato
   ├─ Cadência de deploy conflita com o resto (bloqueia releases) .. candidato
   ├─ Time precisa de autonomia total (Conway) .................... candidato
   ├─ Isolamento de falha crítico (não pode derrubar o resto) ..... candidato
   └─ "porque microservices é moderno" .......... PARE. Isto é envy.

4. O contexto delimitado deste módulo está CLARO e estável?
   ├─ NÃO → PARE. Estabilize a fronteira no monólito primeiro.
   │        Extrair com fronteira errada = mover funcionalidade
   │        entre serviços depois = caríssimo.
   └─ SIM → continue.

5. O time topa pagar o PRÊMIO (rede, consistência eventual,
   observabilidade distribuída, ops) para ESTE módulo?
   ├─ NÃO → PARE. Sem capacidade operacional, o serviço vira passivo.
   └─ SIM → EXTRAIA com strangler fig, um serviço por vez,
            validando em produção antes do próximo.
```

A regra de ouro condensada: **extraia quando a dor justifica o prêmio, e só quando a fronteira já está clara.** Na dúvida, fique no monólito modular — é o estado de menor arrependimento.

### Exemplo neutro: um monólito modular bem desenhado

Considere uma aplicação de comércio com dois domínios distintos: **pedidos** e **pagamentos**. Em vez de dois serviços de rede, dois módulos no mesmo processo:

```text
loja-app/                  (UM processo, UM deploy)
├── orders/                ← módulo "pedidos" (business capability)
│   ├── api/               ← interface PÚBLICA do módulo (estreita)
│   ├── domain/            ← regras internas (privadas)
│   └── data/              ← persistência própria (não compartilhada)
├── payments/              ← módulo "pagamentos" (business capability)
│   ├── api/               ← interface PÚBLICA
│   ├── domain/
│   └── data/
└── platform/              ← infra compartilhada (config, auth, logging)

Regras de fronteira:
  • orders chama payments SÓ pela interface payments/api (método, não rede)
  • orders NÃO lê a tabela de payments; payments NÃO lê a de orders
  • dependência é acíclica: orders → payments, nunca o contrário em loop
  • uma transação ACID ainda abrange os dois (sem consistência eventual)
```

Repare no ganho: as fronteiras de **pagamentos** e **pedidos** já estão desenhadas como capacidades de negócio. Se um dia *pagamentos* precisar escalar sozinho ou ter deploy independente, a extração via strangler fig é mecânica — o limite já existe. Você colheu a clareza de domínio do microservices **sem** ter pago o prêmio enquanto não precisava.

> [!tip] Conway's Law trabalhando a seu favor
> A Lei de Conway diz que a arquitetura do sistema tende a espelhar a estrutura de comunicação da organização. Use isso como bússola: extraia um serviço quando há um **time** que naturalmente "possui" aquela capacidade e ganha com autonomia. Extrair fronteiras que não correspondem a fronteiras de equipe gera serviços que ninguém é dono — e atrito de coordenação permanente.

## Armadilhas

### (1) Microservices prematuro, antes de product-market fit ou escala

O erro arquetípico. O time adota microservices na fundação porque "vamos escalar muito" ou porque está na moda — o que Fowler chama de *Microservice Envy*. Resultado: paga o prêmio inteiro (ops, rede, consistência eventual, observabilidade) para um produto que ainda está descobrindo se tem demanda. E congela limites de domínio que ainda não entende, tornando cada pivô de produto uma cirurgia distribuída. **Correção:** monólito modular até a dor real aparecer. Velocidade de aprender > pureza arquitetural enquanto não há *product-market fit*.

### (2) Decompor por camada técnica em vez de por domínio

Criar "serviço de controllers", "serviço de business logic", "serviço de data access" — ou seja, fatiar pela arquitetura em camadas. Isso produz serviços que **precisam ser deployados juntos** para qualquer mudança de feature, porque toda funcionalidade atravessa todas as camadas. É a receita exata do **monólito distribuído**: você tem o overhead da rede e o acoplamento do monólito, sem nenhum benefício. **Correção:** decomponha por **capacidade de negócio / contexto delimitado** (DDD). Cada serviço deve ser uma fatia vertical do domínio (ex.: *pedidos*, *pagamentos*), não uma camada horizontal.

### (3) Extrair sem contexto delimitado claro

Quebrar o monólito antes de entender onde estão de fato as fronteiras de domínio. Como mover funcionalidade entre serviços é muito mais caro do que entre módulos, uma fronteira errada custa caro para corrigir — às vezes é mais barato fundir os serviços de volta. **Correção:** estabilize a fronteira **dentro** do monólito modular primeiro; use *modelagem DDD* (que problemas você resolve? quem são os donos?) para identificar os limites antes de pagar pela rede. Extraia só fronteiras que já provaram ser estáveis.

> [!danger] A armadilha-mãe
> As três armadilhas têm uma raiz comum: **tratar microservices como default em vez de como resposta a uma dor.** Toda vez que a justificativa for "é a arquitetura certa" e não "esta dor concreta exige isto", desconfie.

## Em entrevista

### Frase pronta (inglês)

> Microservices aren't a default — they're a response to a specific organizational or scaling pain, and they charge a real premium: unreliable networks, eventual consistency, distributed observability and operational overhead. So my default for a new system is a **modular monolith** with clear internal boundaries, which buys most of the domain clarity without paying that premium. I only extract a service when there's concrete pain — a module that needs to scale or deploy independently, or a team that needs full autonomy — and even then I use the **strangler fig** pattern to peel it off one service at a time. The cardinal sin I watch for is decomposing by technical layer instead of by **business capability**, because that just produces a distributed monolith: all the network overhead with all the monolith coupling.

### Vocabulário

| Português | Inglês | Sentido em entrevista |
| --- | --- | --- |
| monólito modular | modular monolith | deploy único com fronteiras internas claras; o default sensato |
| prêmio dos microsserviços | microservice premium | custo fixo do distribuído que se paga mesmo sem usar os benefícios |
| contexto delimitado | bounded context | fronteira de domínio (DDD) por onde se decompõe corretamente |
| monólito distribuído | distributed monolith | anti-padrão: serviços que só deployam juntos; pior dos dois mundos |
| figueira estranguladora | strangler fig | padrão de extração incremental que substitui o legado aos poucos |
| capacidade de negócio | business capability | unidade vertical de domínio; eixo correto de decomposição |
| primeiro o monólito | monolith first | comece monólito, decomponha depois (Fowler) |
| envy / hype de microservices | microservice envy | adotar por moda, não por necessidade — sinal de alerta |

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/01 - O que são microservices e a tese honesta|O que são microservices e a tese honesta]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/02 - Monorepo vs multi-repo|Monorepo vs multi-repo]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|Consistência distribuída]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

> [!note] Próximos galhos
> Os galhos 17 e 18 da trilha Java (planejado) seguem a partir daqui; esta nota fecha o arco de julgamento do Galho 16.

## Referências

- Martin Fowler — *MonolithFirst* (2015): https://martinfowler.com/bliki/MonolithFirst.html
- Martin Fowler — *Microservice Premium*: https://martinfowler.com/bliki/MicroservicePremium.html
- Sam Newman, via InfoQ — *Monolith Decomposition Patterns* (2020): https://www.infoq.com/news/2020/05/monolith-decomposition-newman/
