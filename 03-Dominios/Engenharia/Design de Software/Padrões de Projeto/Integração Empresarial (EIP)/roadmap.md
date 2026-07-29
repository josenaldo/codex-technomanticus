---
title: "Roadmap — Integração Empresarial (EIP)"
created: 2026-07-29
type: meta
publish: false
tags:
  - meta
  - roadmap
  - design-de-software
  - integracao-empresarial
  - eip
  - mensageria
---

# Roadmap — Integração Empresarial / EIP (galho-folha, construção)

Roadmap da família `03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Integração Empresarial (EIP)`. Galho-**folha em modo construção**: uma entrada por nota **a escrever**. Pai: [[Padrões de Projeto/roadmap|Padrões de Projeto]]. Fonte canônica: **Hohpe & Woolf, *Enterprise Integration Patterns* (2004)**; docs do **Apache Camel** e **Spring Integration**.

## Escopo desta família

Os padrões de **integração por mensagens** — o vocabulário nomeado de Hohpe & Woolf para conectar sistemas heterogêneos de forma assíncrona e desacoplada. Cobre os **blocos base** (Message, Message Channel, Pipes and Filters), o **roteamento** (routers, filter, splitter/aggregator, resequencer), a **transformação** (translator, normalizer, canonical model), e os **endpoints/confiabilidade** de produção (consumers, competing consumers, idempotent receiver, guaranteed delivery, dead letter, message bus × broker). Curado dos 65 padrões do livro para o subset de **maior valor legado** (ESBs, MOM, Camel/MuleSoft).

**Fronteira com [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] (decidida 2026-07-29):** este catálogo trata os **padrões nomeados como vocabulário de design** (lente Camel/Spring Integration — as ferramentas que *são* implementações dos EIPs). O galho **Comunicação** trata a **infra e a decisão** (qual broker, síncrono × assíncrono, JMS/IBM MQ/ESB, garantias de entrega, Kafka/RabbitMQ). Pontos de contato (Guaranteed Delivery, Dead Letter Channel, Idempotent Receiver) ficam **autocontidos** aqui + cross-link "aprofunde na infra → Comunicação". **Outbox e Saga NÃO entram nesta família** — são padrões de arquitetura de eventos (família 5 Eventos) e já têm nota de infra em Comunicação/4-04.

## Anatomia de cada nota

Padrão-capítulo, como nas famílias GoF e Acesso a Dados, **com a lente adaptada**: em EIP o contraste interessante é **como cada ferramenta de integração encarna o padrão** —

- **Apache Camel** — DSL de rotas (`from().choice().when()...`); o EIP explícito por excelência
- **Spring Integration** — os mesmos padrões como componentes Spring (channels, routers, transformers)
- **MuleSoft / ESBs** — o EIP no habitat enterprise clássico
- **Brokers/streams modernos** (Kafka, RabbitMQ, SQS) — como realizam (ou não) cada padrão

Estrutura: cenário → ideia (Mermaid) → **como as ferramentas de integração o encarnam** → **quando NÃO usar / usos equivocados (Armadilhas reforçada)** → inglês + PT↔EN → O que vem a seguir → Fontes. Cada entrada **autocontida** (catálogo de consulta); redundância com Comunicação é aceitável, cross-link como "aprofunde".

**Esquema `fase:`:** por centralidade/tema (Iniciado = blocos base; Adepto = roteamento/transformação; Magus = endpoints/confiabilidade/escala).

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Notas de conteúdo | 14 |
| Iniciado | 4 |
| Adepto | 5 |
| Magus | 5 |
| ✅ escritas | 14 |
| ⬜ pendentes | 0 |
| % concluído | 100% ✅ |
| Scaffolding | roadmap.md + index.md criados (2026-07-29) |

---

## Notas — Iniciado (os blocos base: o que é uma mensagem e por onde ela anda)

#### 01 - Panorama da integração   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: iniciado · 203 linhas
- **Escopo:** o problema (integrar sistemas heterogêneos); os **4 estilos de integração** (File Transfer, Shared Database, RPC, Messaging) e por que messaging vence pro desacoplamento; os **6 grupos** de padrões de Hohpe (Channels, Construction, Routing, Transformation, Endpoints, System Management); a lente Camel/Spring Integration; "smart endpoints, dumb pipes"; como usar o catálogo. Mermaid do mapa.
- **Resultado:** 4 estilos (tabela, messaging vence por desacoplamento tempo/espaço/tech); 6 grupos como estações do pipeline (Mermaid); lente ferramenta-É-o-padrão (Camel/Spring Integration); smart endpoints/dumb pipes como fio condutor (ESB); 3 armadilhas (RPC/shared-DB, reinventar sem nomear, inteligência no barramento). Abre a família.

#### 02 - Message   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: iniciado · 183 linhas
- **Escopo:** o **envelope** — header (metadados: id, tipo, correlação, reply-to) + payload (o dado). Os três tipos: **Command Message** (faça isto), **Document Message** (aqui está o dado), **Event Message** (isto aconteceu). Return Address, Correlation Identifier, Message Expiration como headers. **Armadilha:** payload gordo demais; acoplar o consumidor à estrutura interna.
- **Resultado:** envelope header+payload (Mermaid; header roteável sem abrir corpo); tabela das 3 intenções e seu acoplamento (command>document>event); Command→Event como passo de desacoplamento; tabela cross-tool (JMS/AMQP/Kafka/Camel); 3 armadilhas (payload gordo→Claim Check, acoplar à estrutura interna→contrato versionado, esquecer correlationId).

#### 03 - Message Channel   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: iniciado · 180 linhas
- **Escopo:** o **canal** por onde a mensagem trafega. **Point-to-Point** (uma mensagem, um consumidor — fila) × **Publish-Subscribe** (uma mensagem, N consumidores — tópico). Datatype Channel (um canal por tipo), Invalid Message Channel, Dead Letter Channel (intro, aprofundada na 13). **Armadilha:** misturar tipos num canal; confundir fila com tópico.
- **Resultado:** o canal desacopla; PP(fila,1)×PS(tópico,N) com Mermaid; regra trabalho→fila/fato→tópico (casa com command/event da 02); variantes Datatype/Invalid/Dead Letter; tabela cross-tool (Kafka unifica as 2 geometrias via consumer group); 3 armadilhas (misturar tipos, comando por pub-sub=N execuções, evento por fila=interessado perdido).

#### 04 - Pipes and Filters   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: iniciado · 172 linhas
- **Escopo:** o **pipeline** — decompor o processamento em filtros independentes conectados por pipes (canais). A metáfora-mãe do EIP: cada filtro faz uma coisa, componível, testável isolado. Base para todos os roteadores. Ecoa Unix pipes. **Armadilha:** filtro com estado/efeito colateral; pipeline longo demais e opaco.
- **Resultado:** filtros burros conectados por pipes (Mermaid pipeline decrypt→validate→dedup→translate); metáfora-mãe (todo EIP é um filtro; Camel/Spring Integration são motores pipes-and-filters); distinção vs Chain of Responsibility (fluxo de dados distribuído × responsabilidade in-process); 3 armadilhas (estado/efeito escondido, pipeline longo/opaco→tracing, acoplar por suposição não contrato). **Fecha o bloco Iniciado.**

## Notas — Adepto (roteamento e transformação: o coração do EIP)

#### 05 - Content-Based Router + Message Filter   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: adepto · 166 linhas
- **Escopo:** **Content-Based Router** (rotear pelo conteúdo/tipo da mensagem para o destino certo) + **Message Filter** (descartar mensagens que não interessam). O router escolhe UM destino; o filter é o router de 1 saída (passa ou descarta). Camel `choice().when()`. **Armadilha:** lógica de negócio inchando o router; router que vira God component (mover pra Routing Slip / Process Manager).
- **Resultado:** 1 entrada→1 de N saídas (Mermaid); filter = router de 1 saída (passa/descarta); distinção Message Filter × Selective Consumer × filter() de stream; RabbitMQ roteia por routing key não payload; 3 armadilhas (God Router/ESB-gargalo, regras espalhadas, destinos hard-coded→config). **Abre o bloco Adepto.**

#### 06 - Splitter + Aggregator   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: adepto · 173 linhas
- **Escopo:** o par **fan-out/fan-in** canônico. **Splitter** (quebra uma mensagem composta em várias — os itens de um pedido) e **Aggregator** (junta várias mensagens correlacionadas numa só — o padrão **stateful** que espera as partes, com estratégia de completude e timeout). **Armadilha central:** o Aggregator é stateful e precisa de completeness condition + timeout; sem isso, vaza memória ou trava esperando parte que nunca vem.
- **Resultado:** ciclo quebra-processa-junta (Mermaid); Splitter stateless × Aggregator stateful (as 4 decisões: correlação/completude/estratégia/timeout); Composed Message Processor; 3 estratégias de completude (contagem+sinal+timeout); onde o estado vive (MessageStore/janela Kafka); 3 armadilhas (sem completude+timeout=OOM/trava, splitter sem correlação, assumir ordem).

#### 07 - Recipient List + Scatter-Gather + Resequencer   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: adepto · 173 linhas
- **Escopo:** **Recipient List** (enviar a uma lista dinâmica de destinos — como o router, mas N destinos), **Scatter-Gather** (recipient list + aggregator: pergunta a vários, junta as respostas — ex. cotação de fornecedores), **Resequencer** (reordenar mensagens fora de ordem por sequence number). **Armadilha:** scatter-gather sem timeout; resequencer com buffer ilimitado.
- **Resultado:** Recipient List = lista dinâmica computada (× pub-sub: aqui o roteador conhece/decide); Scatter-Gather = RL+Aggregator (Mermaid licitação); distinção vs Splitter (partes do todo × mesma pergunta a vários); Resequencer stateful por sequence number; 3 armadilhas (SG sem timeout=refém do mais lento, resequencer buffer ilimitado=mensagem faltante trava, RL hard-coded).

#### 08 - Message Translator + Normalizer   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: adepto · 176 linhas
- **Escopo:** **Message Translator** (o [[07 - Adapter|Adapter]] da mensageria — traduz o formato entre sistemas que não se entendem) e **Normalizer** (traduz múltiplos formatos de entrada para um canônico). Níveis de tradução (transport, data representation, data types, data structure). Envelope Wrapper, Content Enricher, Content Filter, Claim Check como variantes. **Armadilha:** tradução espalhada; enricher que chama serviço síncrono e acopla.
- **Resultado:** o Adapter da mensageria; 4 níveis de tradução (Mermaid transporte→representação→tipos→estrutura); Normalizer = router+translator por formato→canônico; variantes (Content Enricher/Filter, Claim Check p/ payload gordo, Envelope Wrapper); DataWeave como DSL dedicada; 3 armadilhas (tradução espalhada→N×N, Content Enricher síncrono=RPC disfarçado, God Transformer).

#### 09 - Canonical Data Model   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: adepto · 177 linhas
- **Escopo:** o **modelo comum** que evita o N×N de tradutores (cada sistema traduz só de/para o canônico — N tradutores, não N²). O contraponto: centralizar demais o modelo canônico vira **acoplamento e gargalo** (a lição do ESB; encosta na Comunicação/4-05). **Armadilha central:** canonical model que vira um god-schema versionado por comitê; acoplamento por baixo do desacoplamento aparente.
- **Resultado:** N×N→N (Mermaid malha×estrela); lado sombrio = god-schema/comitê (faca de 2 gumes; canônico mínimo+por-contexto = smart-endpoints no modelo de dados); lente DDD (Published Language + ACL evita canônico global); Schema Registry como canônico de tópicos; 3 armadilhas (god-schema, acoplamento escondido, canônico prematuro). **Fecha o bloco Adepto.**

## Notas — Magus (endpoints, confiabilidade e escala: produção enterprise)

#### 10 - Consumers: Polling × Event-Driven   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: magus · 169 linhas · arquivo `10 - Consumers - Polling × Event-Driven.md`
- **Escopo:** os dois modos de um endpoint receber. **Polling Consumer** (o consumidor puxa, controla o ritmo — bom pra throttling) × **Event-Driven Consumer** (o broker empurra, menor latência). Message Dispatcher, Selective Consumer, Durable Subscriber, Idempotent Receiver (ponte pra 12). **Armadilha:** polling agressivo que martela o broker; push sem backpressure que afoga o consumidor.
- **Resultado:** pull×push (Mermaid); polling=throttling natural/latência; event-driven=baixa latência/sem backpressure; Kafka é polling por baixo (poll() embrulhado em @KafkaListener); Selective/Durable Subscriber; 3 armadilhas (polling agressivo→long polling, push sem backpressure→prefetch, subscriber não-durável). **Abre o bloco Magus.**

#### 11 - Competing Consumers   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: magus · 168 linhas
- **Escopo:** escalar o consumo — **N consumidores** na mesma fila, o broker distribui, cada mensagem vai pra UM (concorrência horizontal). O oposto do pub-sub. Consumo paralelo × ordenação (o trade-off: competing consumers quebra ordem). Message Grouping/partition key como saída. **Armadilha central:** perder ordenação ao paralelizar; assumir exactly-once quando é at-least-once.
- **Resultado:** competir pela próxima msg (Mermaid); trade-off ordem×paralelismo é a lição; particionar por chave (Kafka consumer group = competing consumers no nível de partição); tabela cross-tool (Message Groups/prefetch/partition key/SQS FIFO); 3 armadilhas (perder ordem→particionar, assumir exactly-once, poison/partição quente).

#### 12 - Idempotent Receiver   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: magus · 171 linhas
- **Escopo:** a entrega **at-least-once** (o padrão realista) garante que a mensagem chega, mas pode chegar **duplicada** — então o receptor precisa ser **idempotente** (processar 2× = processar 1×). Estratégias: dedup por message id (inbox), operações naturalmente idempotentes, upsert. Ecoa Comunicação/4-04 (Outbox/inbox). **Armadilha central:** assumir exactly-once do broker; idempotência só na aplicação sem dedup persistente.
- **Resultado:** msg que chega 2× (Mermaid inbox por id); 3 estratégias (dedup/naturalmente idempotente/upsert); exactly-once É MITO na fronteira (EOS Kafka só interno; at-least-once+idempotência=efetivamente-once); 3 armadilhas (crer no exactly-once do broker, dedup só em memória, chave/janela fraca).

#### 13 - Guaranteed Delivery + Dead Letter Channel   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: magus · 174 linhas
- **Escopo:** **Guaranteed Delivery** (a mensagem sobrevive a falha do broker/consumidor — persistência em disco, ack) e **Dead Letter Channel** (para onde vai a mensagem que não pôde ser entregue/processada após N tentativas — o "necrotério" que evita perder ou travar). Retry × DLQ; poison message. Aprofunda na infra: cross-link Comunicação/4-03. **Armadilha central:** DLQ sem monitoramento (mensagens morrem em silêncio); retry infinito de poison message.
- **Resultado:** as 2 falhas opostas (perder × travar); Guaranteed Delivery = persistir-antes-do-ack (WAL, custo throughput); DLQ = retry(transitório)×dead-letter(permanente), Mermaid c/ caminho vermelho; DLC × Invalid Message Channel; tabela cross-tool (persistent/DLX/redrive; Kafka durável nativo); 3 armadilhas (DLQ sem monitoramento, retry infinito de poison, durabilidade errada por fluxo). Corrigido link journaling (está em SO, não BD).

#### 14 - Message Bus × Message Broker   [substantivo]
- **Estado:** ✅ escrita (2026-07-29) · fase: magus · 199 linhas
- **Escopo:** a **topologia** da integração. **Message Broker** (hub-and-spoke: um mediador central roteia — desacopla, mas é ponto central) × **Message Bus** (um backbone comum com endpoints inteligentes). A ascensão e queda do **ESB** (a lição "smart endpoints, dumb pipes"); brokers leves (RabbitMQ) × logs distribuídos (Kafka). **FECHA A FAMÍLIA** com mapa-de-escolha. **Armadilha central:** broker centralizado que vira o ESB-gargalo de novo; lógica de negócio no barramento.
- **Resultado:** broker(hub-and-spoke)×bus(backbone), eixo = quanta inteligência no meio (Mermaid); ascensão/queda do ESB como lição-síntese (toda armadilha "God X" = inteligência no cano); Kafka puxa pro lado bus (log burro/consumidores espertos); tabela cross-tool; 3 armadilhas (broker→ESB, lógica no cano, topologia errada pra carga); **mapa-de-escolha dos 14 padrões** (mirror GoF-23). **FECHA A FAMÍLIA.**

---

## Próximos passos

1. ✅ Escrever 01 → 14. Concluído 2026-07-29 (Iniciado 01-04, Adepto 05-09, Magus 10-14).
2. ✅ `index.md` da família criado (MOC por fase + rotas).
3. ✅ Roadmap-pai (família 3 ✅) + index do galho-pai + [[00-Meta/Roadmap]] central atualizados. **Próxima: família 4 (Aplicação Corporativa / PoEAA não-dados).**
