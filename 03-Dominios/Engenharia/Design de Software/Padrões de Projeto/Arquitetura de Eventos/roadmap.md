---
title: "Roadmap — Arquitetura de Eventos"
created: 2026-07-30
type: meta
publish: false
tags:
  - meta
  - roadmap
  - design-de-software
  - padroes-de-projeto
  - arquitetura-de-eventos
  - eda
---

# Roadmap — Arquitetura de Eventos (galho-folha, construção)

Roadmap da família `03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Arquitetura de Eventos`. Galho-**folha em modo construção**: uma entrada por nota **a escrever**. Pai: [[Padrões de Projeto/roadmap|Padrões de Projeto]]. Fontes canônicas: **Martin Fowler** (*What do you mean by "Event-Driven"?* — a taxonomia dos 4 estilos; *Domain Event*; *Event Sourcing*; *CQRS*), **Hohpe & Woolf** (Process Manager), **Chris Richardson** (Saga, Outbox — microservices.io) e **Eric Evans** (Domain Events no DDD).

## Escopo desta família

Os padrões que aparecem quando um sistema decide **comunicar por fatos ocorridos** em vez de comandos diretos: o que é um evento, o que ele carrega, quem reage, como coordenar um processo que atravessa serviços, e o que muda quando o evento deixa de ser notificação e vira a **fonte da verdade**.

## A lente desta família: o evento como decisão de acoplamento

**Esta é a família com maior sobreposição do galho, e a lente existe para resolver isso.** Levantamento feito em 2026-07-30: *Event Sourcing*, *CQRS*, *Saga*, *Outbox*, *Idempotência* e *Pub-Sub* **já têm casa profunda** em outros galhos do vault (ver a seção de fronteiras). Repetir aquelas notas seria desperdício.

O que aquelas casas **não** cobrem é o eixo que organiza esta família:

> **O que o evento carrega, e a quem isso amarra.** Todo padrão daqui é uma posição num espectro de acoplamento — do evento magro que só avisa que algo aconteceu, ao evento gordo que carrega o estado, ao log de eventos que *é* o estado.

A divisão de trabalho entre os três galhos fica assim, e deve ser reafirmada em cada nota:

| Galho | Pergunta que responde |
| --- | --- |
| **System Design** | quanto aguenta? (throughput, storage, snapshots, projeções em escala) |
| **Comunicação entre Sistemas** | como chega? (broker, entrega, ordenação, CDC, dual-write) |
| **Esta família** | **o que acopla?** (o que o evento carrega, quem depende de quem, o que quebra ao evoluir) |

**Eixo dorsal: Event Notification × Event-Carried State Transfer** — o evento magro contra o gordo. É o debate estruturante da família, no mesmo papel que *Active Record × Data Mapper* teve na família 2.

## Fronteiras (cravadas 2026-07-30)

Notas **autocontidas** aqui (princípio do catálogo), com cross-link explícito "aprofunde lá". Nenhuma nota desta família deve tentar substituir as abaixo:

| Tema | Casa profunda | O que fica lá |
| --- | --- | --- |
| Event Sourcing | [[03-Dominios/Engenharia/Arquitetura/System Design/3 - Padrões recorrentes/03 - Event Sourcing sob a ótica de system design\|System Design 3-03]] | escala, snapshots, storage, replay em volume |
| CQRS | [[03-Dominios/Engenharia/Arquitetura/System Design/3 - Padrões recorrentes/02 - CQRS sob a ótica de system design\|System Design 3-02]] | separação de cargas, réplicas de leitura, números |
| Pub-Sub em escala | [[03-Dominios/Engenharia/Arquitetura/System Design/3 - Padrões recorrentes/01 - Pub-Sub e event-driven em escala\|System Design 3-01]] | fan-out, partições, backpressure |
| Outbox e Saga (infra) | [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/04 - Outbox e Saga\|Comunicação 4-04]] | dual-write, Polling Publisher, CDC/log tailing, isolamento |
| Garantias de entrega | [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/03 - Garantias de entrega e ordenação\|Comunicação 4-03]] | at-least-once, ordenação, particionamento |
| Idempotência (mensageria) | [[Padrões de Projeto/Integração Empresarial (EIP)/12 - Idempotent Receiver\|EIP-12]] | dedup por id no nível do canal |
| Projeções / views materializadas | [[Padrões de Projeto/Acesso a Dados/15 - Polyglot persistence e materialized views\|Acesso a Dados/15]] | persistência da leitura derivada |
| Agregado (fronteira de consistência) | [[Padrões de Projeto/Acesso a Dados/14 - Modelagem por agregado e single-table design\|Acesso a Dados/14]] | modelagem do agregado |

## Anatomia de cada nota

Padrão-capítulo, como nas famílias 1-4:

1. **Cenário** — o problema concreto que faz o padrão aparecer
2. **A ideia** — o padrão, com Mermaid (sequência ou fluxo de eventos)
3. **O que ele acopla** ← *a seção-lente desta família* — o que o evento carrega, quem passa a depender de quem, e o que quebra quando o produtor evolui
4. **Armadilhas (reforçada)** — quando NÃO usar, ≥3
5. **O padrão em inglês** + tabela PT↔EN
6. **O que vem a seguir** + **Fontes**

Registro Feynman. Escrever direto, sem gate de aprovação por nota. Onde houver casa profunda, **abrir com o recorte** ("aqui: o acoplamento; escala e infra em X") para o leitor saber onde está.

**Esquema `fase:`** por centralidade: Iniciado = o que é um evento e o estilo mais simples; Adepto = o que ele carrega e como coordenar; Magus = os estilos que reorganizam o sistema inteiro.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Notas de conteúdo | 10 |
| Iniciado | 3 |
| Adepto | 4 |
| Magus | 3 |
| ✅ escritas | 3 (bloco Iniciado) |
| ⬜ pendentes | 7 |
| % concluído | 30% |
| Scaffolding | roadmap.md criado (2026-07-30); index.md ao fechar |

---

## Notas — Iniciado (o que é um evento, e o estilo mais magro)

#### 01 - Panorama da arquitetura de eventos   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: iniciado · 171 linhas
- **Escopo:** o que qualifica um **evento** (fato ocorrido, no passado, imutável, sem destinatário nomeado) × **comando** (pedido dirigido a alguém) × **documento**; por que "event-driven" virou guarda-chuva de coisas diferentes e o custo disso. **Os quatro estilos de Fowler** (*What do you mean by "Event-Driven"?*, 2017) — Event Notification · Event-Carried State Transfer · Event Sourcing · CQRS — como o mapa da família (Mermaid); eles correspondem exatamente às notas 03, 04, 09 e 10, o que dá à família um fio condutor com fonte. Mencionar *Event Collaboration* (termo anterior de Fowler no eaaDev) como sinônimo aproximado do estilo em que os componentes colaboram só por eventos, sem confundi-lo com a taxonomia dos quatro. A **lente do acoplamento** e a divisão de trabalho com System Design e Comunicação. Inversão de controle: com eventos, o produtor não sabe quem reage — o ganho e a perda (fluxo deixa de ser legível num lugar só).

#### 02 - Domain Events   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: iniciado · 158 linhas
- **Escopo:** o evento **nascendo dentro do domínio** (Evans/DDD): `PedidoConfirmado` como parte do modelo, não como detalhe de mensageria. A distinção decisiva entre **evento de domínio** (interno, no vocabulário do domínio, pode ser síncrono e in-process) e **evento de integração** (publicado para fora, contrato público, versionado) — e por que publicar o evento de domínio cru é o erro que amarra o modelo interno aos consumidores. Como o evento é levantado (coletado no agregado, despachado no commit). **Armadilhas:** evento de domínio virando contrato público; evento no passado × nome imperativo; efeito colateral escondido no handler.

#### 03 - Event Notification   [substantivo]
- **Estado:** ✅ escrita (2026-07-30) · fase: iniciado · 156 linhas
- **Escopo:** o evento **magro**: só o fato e um identificador. Quem se interessa **volta e pergunta**. É o menor acoplamento possível — o produtor não conhece consumidores nem o que eles precisam. O custo é a **chamada de volta** (chatty, e o produtor vira dependência de disponibilidade) e o risco de ler estado **posterior** ao evento. **Armadilhas:** teia de notificações sem fluxo legível; ler o estado atual e obter um mundo diferente do que gerou o evento; usar notificação onde o consumidor sempre vai precisar dos dados (é ECST disfarçado, com round-trip extra). Fecha o bloco Iniciado.

## Notas — Adepto (o que o evento carrega, e como coordenar)

#### 04 - Event-Carried State Transfer   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Escopo:** o evento **gordo**: carrega o estado necessário para o consumidor agir sem voltar. Ganha **autonomia** (o consumidor sobrevive à queda do produtor) e paga em **réplica de dados** — o consumidor passa a manter uma cópia local, eventualmente inconsistente, e a versão do payload vira contrato. **O eixo dorsal da família:** tabela Notification × ECST (acoplamento, autonomia, tamanho, evolução, consistência). **Armadilhas:** payload gordo demais e versionamento; assumir ordem de chegada ao aplicar estado; cópia local sem política de reconciliação.

#### 05 - Outbox   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Escopo:** o **dual-write problem** — gravar no banco e publicar no broker não é atômico, e qualquer ordem tem um caso de falha (evento sem dado, ou dado sem evento). O Outbox resolve gravando o evento **na mesma transação**, numa tabela, e publicando depois. **Recorte:** aqui o padrão como decisão de design (por que a atomicidade importa, o que ela garante e o que não garante); **a infra (Polling Publisher, CDC/log tailing) fica em Comunicação 4-04** — cross-link explícito. **Armadilhas:** achar que Outbox dá exactly-once (dá at-least-once ⇒ exige a nota 06); tabela de outbox sem expurgo; publicar o evento de domínio cru (liga com a 02).

#### 06 - Idempotent Consumer (Inbox)   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Escopo:** o outro lado do at-least-once — a mensagem **vai** chegar duplicada, e o consumidor precisa que processar duas vezes tenha o efeito de uma. Estratégias: **inbox** (registrar o id processado na mesma transação do efeito), operação naturalmente idempotente, upsert por chave de negócio. **Recorte:** o dedup no nível do canal está em [[Padrões de Projeto/Integração Empresarial (EIP)/12 - Idempotent Receiver|EIP-12]]; aqui o foco é a **idempotência do efeito de negócio** (cobrar duas vezes é diferente de gravar duas vezes). **Armadilhas:** dedup em memória; janela de dedup curta demais; idempotência que não cobre o efeito externo (e-mail já enviado).

#### 07 - Saga   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Escopo:** a transação de negócio que atravessa serviços, onde **não existe** transação distribuída viável — sequência de passos locais, cada um com sua **compensação**. **Coreografia** (cada serviço reage a eventos; acoplamento distribuído, fluxo ilegível) × **orquestração** (um coordenador comanda; fluxo explícito, coordenador central). **Recorte:** aqui a escolha como decisão de acoplamento; o exemplo trabalhado e o isolamento estão em Comunicação 4-04. **Armadilhas:** compensação que não compensa (efeito irreversível); saga sem timeout; coreografia crescendo até ninguém saber o fluxo. Fecha o bloco Adepto.

## Notas — Magus (os estilos que reorganizam o sistema)

#### 08 - Process Manager   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** o coordenador **explícito e stateful** de um processo de várias etapas (Hohpe & Woolf): mantém o estado da instância do processo, decide o próximo passo, trata timeout. A relação com a **saga orquestrada** (o Process Manager é o orquestrador) e com o [[Padrões de Projeto/Aplicação Corporativa/04 - Application Controller|Application Controller]] da família 4 — o mesmo raciocínio de máquina de estados, agora distribuído e durável (Step Functions, Temporal, Durable Functions). **Armadilhas:** process manager acumulando regra de negócio dos serviços; estado do processo sem durabilidade; confundir com roteador stateless.

#### 09 - Event Sourcing   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** o evento deixa de notificar e vira a **fonte da verdade**: o estado é derivado do log, não armazenado. Ganha auditoria completa, *time travel* e a possibilidade de reinterpretar o passado; paga em complexidade de leitura (projeções), evolução de esquema de eventos e **irreversibilidade** (o log é imutável — inclusive o erro). **Recorte:** aqui o que ele acopla e quando não vale; **escala, snapshots e storage em System Design 3-03**. **Armadilhas:** aplicar ao sistema inteiro em vez do agregado que precisa; esquema de evento sem estratégia de versão/upcasting; confundir com log de auditoria; LGPD/direito ao esquecimento contra log imutável.

#### 10 - CQRS   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** separar o **modelo de escrita** do **modelo de leitura** — e a lição de Young/Fowler de que ele é uma ferramenta **cirúrgica**, não default. A ligação natural com Event Sourcing (as projeções são o lado de leitura) e por que os dois são frequentemente confundidos como um só. **Recorte:** aqui o acoplamento e o critério de aplicação; escala e réplicas em System Design 3-02. **Armadilhas:** CQRS no sistema inteiro; consistência eventual não comunicada à UI (o usuário salva e não vê); dois modelos mantidos à mão sem projeção automática. **FECHA A FAMÍLIA** com mapa-de-escolha dos 10 padrões e a síntese do espectro de acoplamento (magro → gordo → log).

---

## Próximos passos

1. ✅ Bloco **Iniciado** (01-03) escrito — 2026-07-30. **Correção de fonte durante a escrita:** a taxonomia dos 4 estilos de Fowler é Event Notification · ECST · Event Sourcing · **CQRS** — *Event Collaboration* é termo anterior do eaaDev e NÃO integra os quatro (o roster inicial errava nisso). Os 4 estilos mapeiam exatamente nas notas 03, 04, 09 e 10.
2. ⬜ Escrever o bloco **Adepto** (04-07) — parar e perguntar.
3. ⬜ Escrever o bloco **Magus** (08-10) — a 10 fecha a família.
4. ⬜ `index.md` da família, no molde das famílias 1-4.
5. ⬜ Atualizar roadmap-pai + `index.md` do galho-pai + [[00-Meta/Roadmap]] central. Abrir a **família 6 (Nuvem e Resiliência)** — atenção: *Circuit Breaker* e *API Gateway/BFF* também já têm casa em System Design 3-05 e 3-06, mesmo levantamento de fronteira será necessário.
6. ⬜ Reavaliar a pendência transversal: graduar as notas 22-23 da GoF a **capstone** do galho-pai.

## Disciplina

- Escrita sequencial via `/escrever-nota`, uma nota por vez. **Sem fan-out massivo** (regra pessoal do usuário).
- Validar Mermaid: `node .agents/skills/verificar-nota/scripts/validar-mermaid.mjs "<nota>"`. Paleta azul `#4A90D9` / âmbar `#F5A623` / vermelho `#D0021B`.
- Frontmatter: `fase:` lowercase, `type: concept`, `publish: false`.
- **Wikilinks:** verificar filename+pasta reais antes de linkar. A família 6 ainda não existe → citar em prosa.
- **Git:** stage de paths **explícitos e estreitos** — nunca `git add` da pasta `Design de Software` inteira. Sem `Co-Authored-By`.
