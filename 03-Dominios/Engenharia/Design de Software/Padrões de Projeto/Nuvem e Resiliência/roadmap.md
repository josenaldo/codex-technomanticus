---
title: "Roadmap — Nuvem e Resiliência"
created: 2026-07-31
type: meta
publish: false
tags:
  - meta
  - roadmap
  - design-de-software
  - padroes-de-projeto
  - resiliencia
  - cloud
---

# Roadmap — Nuvem e Resiliência (galho-folha, construção)

Roadmap da família `03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Nuvem e Resiliência`. Galho-**folha em modo construção**. Pai: [[Padrões de Projeto/roadmap|Padrões de Projeto]]. **Sexta e última família.** Fontes canônicas: **Azure Cloud Design Patterns**, **Nygard** (*Release It!*), **Michael Fowler / Netflix** (Hystrix e a linhagem de tolerância a falhas), **Chris Richardson**.

## O levantamento de fronteira (2026-07-31) — leia antes de tudo

**Esta é a família mais coberta do vault, e a decisão de escrevê-la mesmo assim foi deliberada.** O levantamento encontrou:

| Padrão | Casas existentes |
| --- | --- |
| Timeout · Retry · Circuit Breaker · Bulkhead · Fallback · Load shedding | [[03-Dominios/Engenharia/Arquitetura/System Design/3 - Padrões recorrentes/05 - Circuit Breaker e resiliência\|System Design 3-05]] (33 KB) **+** [[03-Dominios/Engenharia/Operação/3 - Rodar em produção/06 - Resiliência operacional\|Operação 3-06]] (46 KB) |
| Strangler Fig | [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/18 - Strangler Fig\|Arqueologia 18]] (25 KB) |
| Anti-Corruption Layer | [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/19 - Branch by Abstraction e Anti-Corruption Layer\|Arqueologia 19]] (26 KB) |
| Rate Limiting | [[03-Dominios/Engenharia/Arquitetura/System Design/3 - Padrões recorrentes/04 - Rate Limiting\|System Design 3-04]] + [[03-Dominios/Engenharia/Comunicação entre Sistemas/3 - Confiabilidade do contrato/04 - Rate limiting como contrato\|Comunicação 3-04]] + [[03-Dominios/Tecnologia/Cloud/14 - API Gateway e edge de aplicação/03 - Throttling, quotas e caching\|Cloud 14-03]] |
| Cache-Aside | [[03-Dominios/Engenharia/Arquitetura/System Design/2 - Building blocks/02 - Caching\|System Design 2-02]] (47 KB) |
| API Gateway / BFF | [[03-Dominios/Engenharia/Arquitetura/System Design/3 - Padrões recorrentes/06 - API Gateway e BFF\|System Design 3-06]] + [[Padrões de Projeto/Aplicação Corporativa/06 - Remote Facade\|família 4, nota 06]] |
| Leader Election | [[03-Dominios/Engenharia/Arquitetura/System Design/2 - Building blocks/06 - CAP, consistência e consenso\|System Design 2-06]] |
| Health Endpoint · HA · DR | [[03-Dominios/Tecnologia/Cloud/20 - Resiliência e continuidade/index\|Cloud 20]] + Operação |

**Sem casa nenhuma:** apenas Ambassador, Sidecar, Valet Key e Gatekeeper.

**Decisão do usuário (2026-07-31):** construir a família **completa** mesmo assim, pelo princípio de **autocontenção do catálogo** — quem procura "Circuit Breaker" no catálogo de padrões deve encontrar uma entrada, não um ponteiro. Redundância de assunto é reforço (convenção do vault); o que não se admite é disputar o mesmo papel. Daí a lente abaixo.

## A lente desta família: o que o padrão sacrifica

As duas lentes óbvias **já estão ocupadas** — Operação 3-06 abre com "o mapa: onde cada padrão corta a corrente" e tem seção sobre resiliência no código × no mesh; System Design trata escala e entrevista. Repetir qualquer uma produziria a terceira versão pior do mesmo texto.

O eixo livre, e coerente com a espinha do galho (peso no *quando NÃO usar*):

> **Todo padrão de resiliência é uma escolha sobre o que sacrificar para não cair inteiro — e sobre quem paga a conta.** Retry sacrifica latência e amplifica carga; circuit breaker sacrifica requisições que talvez funcionassem; bulkhead sacrifica utilização de recursos; cache-aside sacrifica frescor; rate limiting sacrifica clientes legítimos na cauda; load shedding sacrifica requisições explicitamente.

Nenhum é gratuito, e o erro clássico é adotar vários sem somar os sacrifícios — o que produz sistemas que falham de formas novas e piores sob o próprio mecanismo de defesa.

| Galho | Pergunta que responde |
| --- | --- |
| **System Design** | *quanto aguenta?* — escala, números, a resposta de entrevista |
| **Operação** | *como tunar e operar?* — thresholds, orçamento de retry, mesh, teste |
| **Cloud** | *qual serviço faz isso?* — HA, multi-region, DR, gateway gerenciado |
| **Arqueologia** | *como migrar com isso?* — Strangler Fig e ACL como método |
| **Esta família** | ***o que se sacrifica, e quem paga?*** — o trade-off explícito, padrão a padrão |

## Anatomia de cada nota

1. **Cenário** — a falha concreta que o padrão evita
2. **A ideia** — o padrão, com Mermaid
3. **O que se sacrifica** ← *a seção-lente desta família* — o custo, e sobre quem ele recai
4. **Armadilhas (reforçada)** — quando NÃO usar, ≥3
5. **O padrão em inglês** + tabela PT↔EN
6. **O que vem a seguir** + **Fontes**

**Obrigatório nesta família:** toda nota abre com callout `[!info] O recorte desta nota`, apontando as casas profundas. Sem isso, a nota compete em vez de complementar.

**Esquema `fase:`** por centralidade: Iniciado = os quatro fundamentos que todo serviço precisa; Adepto = conter e degradar; Magus = topologia, fronteira e migração.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Notas de conteúdo | 14 |
| Iniciado | 5 |
| Adepto | 5 |
| Magus | 4 |
| ✅ escritas | 5 (bloco Iniciado) |
| ⬜ pendentes | 9 |
| % concluído | 36% |
| Scaffolding | roadmap.md criado (2026-07-31); index.md ao fechar |

---

## Notas — Iniciado (falhar bem: os fundamentos)

#### 01 - Panorama da resiliência   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: iniciado · 177 linhas
- **Escopo:** a **falha parcial** como o modo de falha que o monólito não tinha (no monólito, ou está no ar ou não está; distribuído, está *meio* no ar). A **falha em cascata** e o efeito dominó. O mapa dos padrões por onde eles cortam a corrente (Mermaid). A **lente do sacrifício** e a divisão de trabalho com System Design, Operação, Cloud e Arqueologia. Por que a soma dos padrões precisa ser avaliada junto.

#### 02 - Timeout   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: iniciado · 151 linhas
- **Escopo:** a defesa mais básica e a mais esquecida — **default infinito** é a configuração que derruba sistemas. Esperar para sempre transforma uma dependência lenta em esgotamento de threads/conexões e propaga a falha para cima. Timeout de conexão × de leitura × orçamento total da requisição (o *deadline* que atravessa a cadeia). **Sacrifício:** requisições que teriam sucesso se esperassem mais. **Armadilhas:** timeout maior que o do chamador (inútil); timeout uniforme sem base em percentil real; não propagar deadline.

#### 03 - Retry   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: iniciado · 150 linhas
- **Escopo:** repetir o que falhou — e por que a versão ingênua **piora** o incidente. *Backoff* exponencial, **jitter** (sem ele, os clientes sincronizam e martelam em ondas), **orçamento de retry** (teto de % de tráfego), e a distinção crítica entre erro **transitório** (vale repetir) e **permanente** (repetir é dano). Retry exige idempotência — ponte com [[Padrões de Projeto/Arquitetura de Eventos/06 - Idempotent Consumer (Inbox)|família 5, nota 06]]. **Sacrifício:** latência do caso ruim e **amplificação de carga** exatamente quando o alvo está fraco. **Armadilhas:** retry em cascata (multiplicação por camada); retry de não-idempotente; retry sem teto.

#### 04 - Circuit Breaker   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: iniciado · 139 linhas
- **Escopo:** parar de bater numa porta que não abre. Os **três estados** (fechado / aberto / meio-aberto) e o que cada transição custa. Falhar **rápido** preserva os recursos do chamador e dá espaço ao alvo para se recuperar. **Sacrifício central:** enquanto aberto, ele rejeita requisições que **talvez funcionassem** — é uma aposta estatística, e os dois erros (abrir cedo demais, tarde demais) têm custos opostos. **Armadilhas:** breaker por processo em frota grande (cada instância aprende sozinha); sem fallback definido, só troca timeout por erro; abrir por erro de negócio (4xx) em vez de falha de infraestrutura.

#### 05 - Bulkhead   [substantivo]
- **Estado:** ✅ escrita (2026-07-31) · fase: iniciado · 145 linhas
- **Escopo:** compartimentar como no casco de um navio — isolar recursos (pools de conexão, threads, instâncias) por dependência ou por cliente, para que o afogamento de um não afunde o todo. O caso clássico: uma dependência lenta consome **todo** o pool compartilhado e derruba funcionalidades que nada tinham a ver. **Sacrifício:** utilização — recursos reservados e ociosos em um compartimento não socorrem outro sob pressão. **Armadilhas:** compartimentos pequenos demais (falha sob pico normal); bulkhead sem observabilidade por compartimento; isolar thread mas compartilhar o recurso real (o banco).

## Notas — Adepto (conter e degradar)

#### 06 - Fallback e degradação graciosa   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Escopo:** o que responder quando a defesa disparou. Níveis: valor em cache, valor padrão, funcionalidade reduzida, mensagem honesta. **A armadilha-mãe:** o plano B **nunca exercitado** — que falha justamente no dia em que é acionado, transformando um incidente em dois. **Sacrifício:** correção — você serve algo *pior* de propósito, e alguém precisa decidir que isso é aceitável (decisão de produto, não técnica). **Armadilhas:** fallback silencioso que esconde a falha das métricas; fallback que chama outra dependência (nova cascata); dado velho servido como se fosse fresco.

#### 07 - Rate Limiting e Load Shedding   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Escopo:** os dois modos de dizer não. **Rate limiting** rejeita por **cota** (contrato: você tem N/min) — algoritmos em uma passada (token bucket × leaky bucket × janela deslizante) e o essencial: comunicar limites por header e responder 429 com `Retry-After`. **Load shedding** rejeita por **pressão** (o sistema está no limite agora), priorizando o que importa. **Sacrifício:** clientes legítimos na cauda, e a assimetria de quem é sacrificado primeiro. **Armadilhas:** limitar por IP atrás de NAT/proxy; rejeitar sem indicar quando voltar; shedding que derruba justamente a requisição de health check ou de pagamento.

#### 08 - Cache-Aside   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Escopo:** a aplicação consulta o cache, e em caso de falta busca na origem e popula. Como padrão de **resiliência** (não só de desempenho): o cache absorve a indisponibilidade da origem — e cria dependência nova. **Sacrifício:** frescor, e um segundo sistema que pode falhar. **Armadilhas:** *cache stampede* (a expiração simultânea derruba a origem — mitigar com jitter de TTL e *single-flight*); invalidação errada servindo dado velho indefinidamente; cache no caminho crítico sem *fail-open*.

#### 09 - Health Endpoint Monitoring   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Escopo:** o serviço expõe um endpoint que declara sua saúde, e a plataforma age sobre a resposta (tirar do balanceador, reiniciar). A distinção que decide tudo: **liveness** (estou vivo? falha ⇒ reiniciar) × **readiness** (posso receber tráfego agora? falha ⇒ tirar do balanceador) × **startup**. **Sacrifício:** um check profundo dá diagnóstico melhor e **propaga falha** — se o liveness verifica o banco, uma queda do banco reinicia toda a frota. **Armadilhas:** liveness checando dependências (a cascata acima); health que só responde 200 sem verificar nada; readiness sem período de aquecimento.

#### 10 - Leader Election   [substantivo]
- **Estado:** ⬜ pendente · fase: adepto
- **Escopo:** quando exatamente **uma** instância deve executar algo (job agendado, compactação, reconciliação), elege-se um líder por *lease* com renovação. **Sacrifício:** disponibilidade da função durante a reeleição, e complexidade de coordenação. **Armadilhas:** **split-brain** (dois líderes por partição de rede ou pausa de GC — o líder precisa saber que perdeu a liderança); lease sem renovação (líder morto segura o cargo); implementar do zero em vez de usar o mecanismo existente (lease do K8s, etcd, Zookeeper).

## Notas — Magus (topologia, fronteira e migração)

#### 11 - Ambassador + Sidecar   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** tirar a resiliência do código da aplicação e colocá-la num **processo acompanhante**. **Sidecar** = capacidade auxiliar no mesmo host/pod (proxy, log, métricas); **Ambassador** = o sidecar especializado em intermediar chamadas **de saída** (retry, timeout, circuit breaker, mTLS) — o modelo do service mesh. Valor central para poliglota e para **legado que não pode ser recompilado**. **Sacrifício:** um salto de rede, mais recursos por pod, e a resiliência sai do alcance do desenvolvedor (debugar fica mais difícil). **Armadilhas:** retry no mesh **e** na aplicação (multiplicação); mesh adotado pelo que ele promete e não pelo que se usa; sidecar que morre antes da app no encerramento.

#### 12 - Gatekeeper + Valet Key   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** os dois padrões de **borda de segurança** do catálogo Azure. **Gatekeeper** = uma instância intermediária valida e sanitiza antes de alcançar o serviço, que roda com privilégio menor. **Valet Key** = em vez de proxyar dados pesados, entregue ao cliente um **token de acesso limitado e temporário** para falar direto com o armazenamento (URL pré-assinada do S3) — descarrega a aplicação do caminho dos bytes. **Sacrifício:** Gatekeeper = latência e mais um salto; Valet Key = controle fino sobre o acesso, que passa a valer pelo escopo do token. **Armadilhas:** valet key com escopo largo ou validade longa; gatekeeper que vira God proxy; assumir que o token não vaza.

#### 13 - Anti-Corruption Layer + Strangler Fig   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** o par de **convivência com o legado**. **ACL** = camada de tradução na fronteira, para que o modelo do sistema antigo não contamine o novo. **Strangler Fig** = substituir por incremento, interceptando chamadas e desviando funcionalidade por funcionalidade, até o antigo morrer. **Recorte forte:** ambos têm nota dedicada na Arqueologia — aqui a entrada de catálogo (o que é, o que sacrifica); **o método de migração fica lá**. **Sacrifício:** ACL = código de tradução que não entrega valor de negócio e precisa ser mantido; Strangler = período longo com **dois sistemas vivos**, e o roteador de desvio como componente crítico. **Armadilhas:** estrangulamento que nunca termina (os dois sistemas viram permanentes); ACL que vaza o modelo antigo; desligar o antigo sem verificar quem ainda o chama.

#### 14 - Escolher o padrão de resiliência (capstone)   [substantivo]
- **Estado:** ⬜ pendente · fase: magus
- **Escopo:** **FECHA A FAMÍLIA E O GALHO-PAI.** Mapa de escolha por **sintoma** (a dependência está lenta / caiu / está sobrecarregada / o cliente abusa / preciso migrar). A **soma dos sacrifícios**: como os padrões interagem e a ordem em que se compõem (timeout dentro de retry dentro de breaker dentro de bulkhead), e por que empilhá-los sem somar produz falhas novas. A tabela final **padrão → o que sacrifica → quem paga**. E o fechamento do galho-pai: as seis famílias, as seis lentes, e o que o catálogo inteiro ensina.

---

## Próximos passos

1. ✅ Bloco **Iniciado** (01-05) escrito — 2026-07-31. Callout de recorte presente em todas. A lente do sacrifício rendeu conteúdo próprio em cada nota: timeout=requisições que esperariam mais · retry=carga sobre quem já está fraco (único padrão em que o custo recai sobre a DEPENDÊNCIA) · breaker=aposta estatística com dois erros de custo oposto · bulkhead=utilização.
2. ⬜ Escrever o bloco **Adepto** (06-10) — parar e perguntar.
3. ⬜ Escrever o bloco **Magus** (11-14) — a 14 fecha a família **e o galho-pai**.
4. ⬜ `index.md` da família, no molde das famílias 1-5.
5. ⬜ Atualizar roadmap-pai + `index.md` do galho-pai + [[00-Meta/Roadmap]] central — **galho-pai COMPLETO, 6/6 famílias**.
6. ⬜ Decidir a pendência transversal: **capstone do galho-pai** — avaliar se a nota 14 desta família já cumpre o papel, ou se as notas 22-23 da GoF ainda devem ser graduadas.

## Disciplina

- Escrita sequencial via `/escrever-nota`, uma nota por vez. **Sem fan-out massivo**.
- **Callout de recorte obrigatório** em toda nota — esta família complementa, não compete.
- Validar Mermaid: `node .agents/skills/verificar-nota/scripts/validar-mermaid.mjs "<nota>"`. Paleta azul `#4A90D9` / âmbar `#F5A623` / vermelho `#D0021B`.
- Frontmatter: `fase:` lowercase, `type: concept`, `publish: false`.
- **Wikilinks:** verificar filename+pasta reais antes de linkar.
- **Git:** stage de paths **explícitos e estreitos**. Sem `Co-Authored-By`.
