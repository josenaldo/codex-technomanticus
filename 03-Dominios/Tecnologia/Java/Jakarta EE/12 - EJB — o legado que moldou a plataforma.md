---
title: "EJB — o legado que moldou a plataforma"
created: 2026-06-07
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - jakarta-ee
  - magus
  - ejb
aliases:
  - "EJB"
  - "Enterprise JavaBeans"
  - "Session beans"
---

# EJB — o legado que moldou a plataforma

> [!abstract] TL;DR
> EJB foi o modelo de componente enterprise por uma década — transações, segurança e remoting declarativos quando nada mais oferecia isso de forma padronizada. O peso do EJB 2.x (home/remote interfaces, descritores XML, entity beans/CMP) gerou uma reação expressiva da comunidade em direção a frameworks mais leves, e pressionou a própria plataforma: o EJB 3.x simplificou radicalmente, antecipando conceitos que depois amadureceram no CDI. Hoje a spec está estável (4.0, usada no Jakarta EE 9/10/11; 4.1 em desenvolvimento para Jakarta EE 12), o CDI absorveu o papel central de injeção de dependência e escopos, e o EJB persiste onde foi cravado: legados corporativos. Conhecer EJB não é nostalgia — é o que diferencia um senior que entende a história da plataforma de um que só conhece o presente.

## O que é

Jakarta Enterprise Beans (EJB) define uma arquitetura para desenvolvimento e implantação de aplicações de negócio baseadas em componentes gerenciados pelo contêiner. O componente EJB é um objeto Java cujo ciclo de vida, transações, segurança e acesso remoto são controlados pelo servidor de aplicação — não pelo código da aplicação.

A spec nasce ainda como `javax.ejb` no tempo do J2EE, atravessa a transição para `jakarta.ejb` no Jakarta EE 9 (que quebrou compatibilidade binária de propósito para abrir o namespace), e chega à versão 4.0 como uma spec estável, enxuta e com escopo bem delimitado.

A visão histórica honesta: EJB não era "enterprise sobre-engenhado por acidente". Era a resposta disponível — e padronizada — para problemas reais de sistemas distribuídos numa era em que as alternativas de mercado eram proprietárias ou inexistentes. O custo veio depois, com o amadurecimento do ecossistema e a percepção de que boa parte do modelo era acidental, não essencial.

## Por que importa

**Legados corporativos existem.** Manutenção e migração de sistemas EJB são trabalho real de engenheiro senior em grandes organizações. Não conhecer a spec é chegar sem mapa num terreno que tem décadas de decisões sedimentadas.

**A história explica o presente.** CDI não surgiu do nada: os conceitos de DI gerenciada pelo contêiner, interceptors, escopos e integração transacional têm raízes diretas nas lições aprendidas (e nos erros cometidos) com EJB. Entender o "por que" do CDI exige entender o "contra o quê" ele foi construído.

**Entrevista: testa maturidade histórica.** A pergunta "EJB vs CDI — quando usar cada um?" não testa memorização de API. Testa se o candidato tem perspectiva sobre a plataforma — se entende que tecnologia é acumulada, não substituída do dia para a noite, e que stacks reais têm estratificação histórica.

## Como funciona

### Ascensão (J2EE): o que o EJB resolvia

No início dos anos 2000, construir uma aplicação enterprise distribuída exigia resolver à mão (ou com infra proprietária) uma lista pesada de preocupações transversais:

- **Gerenciamento de transações**: demarcação, commit/rollback, propagação entre chamadas de serviço.
- **Segurança**: autenticação, autorização por papel (`isCallerInRole`), propagação de identidade entre componentes.
- **Pooling de instâncias**: criar e destruir objetos a cada requisição num servidor de alta carga é caro; o contêiner gerenciava pools de beans stateless.
- **Acesso remoto padronizado**: chamada entre JVMs com semântica pass-by-value, registro JNDI, sem depender de solução proprietária.

O EJB entregava tudo isso de forma declarativa — você anotava (ou, na era 2.x, declarava em XML) e o contêiner fazia o resto. Para o contexto da época, isso era real e valioso.

### O peso do 2.x

O EJB 2.x acumulou complexidade que se tornava acidental conforme o ecossistema amadurecia:

**Home interfaces e remote/local interfaces**: cada bean exigia pelo menos três artefatos além da implementação — interface `EJBHome`, interface `EJBLocalHome`, interface de componente. O contêiner gerava stubs via ferramentas proprietárias. O código de bootstrap para obter uma referência a um bean envolvia JNDI lookup, narrow cast e tratamento de exceções checked obrigatórias.

**Descritores XML**: `ejb-jar.xml` e os descritores de deployment específicos do servidor precisavam espelhar cada detalhe do código. Qualquer divergência resultava em falha em runtime, não em compilação.

**Entity beans e CMP (Container-Managed Persistence)**: o EJB 2.x tentou resolver persistência dentro do contêiner, com mapeamento objeto-relacional declarado em XML e gerado pelo servidor. A abstração vazava, o comportamento variava entre fornecedores, e o modelo era fundamentalmente mais difícil de usar do que SQL direto para qualquer consulta não trivial.

Essa combinação gerou pressão da comunidade por alternativas mais simples. Surgiram frameworks mais leves — alguns ainda ativos, abordados no galho [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]] — que mostraram na prática que POJOs gerenciados por um contêiner leve podiam entregar o mesmo resultado com fração do cerimônial.

### A simplificação do 3.x

O EJB 3.0 (Java EE 5, 2006) foi uma virada radical, alinhada com as ideias que já circulavam na comunidade:

- **Annotations substituem XML**: `@Stateless`, `@Stateful`, `@Singleton`, `@TransactionAttribute`, `@RolesAllowed` — o descritor XML passou a ser opcional.
- **POJOs como beans**: não mais herança de interfaces geradas. O bean é uma classe Java comum; o contêiner descobre e gerencia via anotação.
- **Injeção de dependência básica**: `@EJB` e `@Resource` para injetar referências sem JNDI manual.
- **Home interfaces opcionais**: a interface de componente local/remota agora podia ser uma interface Java simples, sem contratos especiais.

Essa simplificação convergiu com a direção que virou CDI — tanto que CDI foi introduzido no Java EE 6 como a evolução natural do mesmo raciocínio, agora aplicado a qualquer bean gerenciado, não só aos componentes enterprise.

### Os tipos hoje

A Jakarta Enterprise Beans 4.0 define como componentes mandatórios:

**Session beans stateless (`@Stateless`)**: sem estado conversacional entre chamadas; o contêiner mantém um pool de instâncias. Caso de uso clássico: serviço de aplicação que processa uma requisição e retorna. A transação, por padrão, é `REQUIRED` — o contêiner abre e fecha por método.

**Session beans stateful (`@Stateful`)**: mantêm estado conversacional com um cliente específico durante uma sessão. O contêiner gerencia passivação/ativação para liberar memória. Caso de uso: carrinho de compras, wizard multi-passo. O bean é criado para um cliente e destruído quando ele chama o método anotado com `@Remove`.

**Session beans singleton (`@Singleton`)**: uma única instância por aplicação, gerenciada pelo contêiner com controle de concorrência declarativo (`@Lock`, `@ConcurrencyManagement`). Caso de uso: cache de configuração compartilhado, registro de estado global.

**Message-driven beans (MDB)**: componentes assíncronos ativados por mensagens (Jakarta Messaging e outros sistemas de mensageria via adaptadores). Não têm interface cliente — são consumidos pela infraestrutura. A mensageria e MDB são o foco do Galho 14 (planejado); aqui a menção é apenas para completar o quadro dos tipos definidos pela spec.

**Timer service (`@Schedule`)**: permite declarar tarefas agendadas diretamente no componente EJB, com expressões de calendário (similar ao cron). A anotação `@Schedule` é repetível desde o EJB 3.2.

```java
import jakarta.ejb.Schedule;
import jakarta.ejb.Stateless;

@Stateless
public class RelatorioAgendadoBean {

    @Schedule(hour = "2", minute = "0", second = "0", persistent = false)
    public void gerarRelatorioNocturno() {
        // executa todo dia às 02:00
        // transação REQUIRED gerenciada pelo contêiner
    }

    @Schedule(dayOfWeek = "Mon", hour = "8", persistent = false)
    public void gerarRelatorioSemanal() {
        // executa toda segunda-feira às 08:00
    }
}
```

**Entity beans**: marcados como opcionais desde o EJB 3.2 e continuam opcionais no 4.0. Na prática, JPA (Jakarta Persistence) substituiu completamente esse papel — as `@Entity` do JPA são uma história separada (Galhos 9 e 10).

### EJB × CDI

A relação entre EJB e CDI no Jakarta EE moderno é de integração, não de substituição completa. A spec 4.0 define explicitamente que um EJB empacotado em um CDI bean archive (e não anotado com `@Vetoed`) é considerado um bean gerenciado pelo CDI.

**O que o CDI absorveu** (e onde ele é hoje a escolha default):
- Injeção de dependência tipada (`@Inject`) sem JNDI.
- Escopos (`@RequestScoped`, `@SessionScoped`, `@ApplicationScoped`, `@ConversationScoped`).
- Interceptors e decorators de propósito geral.
- Eventos CDI (`@Observes`).
- Gerenciamento de ciclo de vida de beans arbitrários.

**O que ainda é exclusivo do EJB conforme a spec 4.0**:
- **Timer service declarativo** (`@Schedule`): o CDI não tem equivalente nativo na spec; frameworks e extensões preenchem essa lacuna fora da spec base.
- **Remoting padronizado**: o modelo de acesso remoto entre JVMs com semântica pass-by-value e lookup JNDI permanece no escopo do EJB — o CDI é local por design.
- **Controle de concorrência declarativo** em singletons (`@Lock(LockType.READ/WRITE)`): o CDI não oferece esse mecanismo na spec base.
- **Pooling de instâncias** para stateless beans: o contêiner gerencia o pool automaticamente; no CDI, `@ApplicationScoped` é uma instância única (sem pooling), e `@RequestScoped` cria uma instância por requisição sem pool.

**Status verificável**: Jakarta Enterprise Beans 4.0 é a spec estável atual (Jakarta EE 9/10/11). A versão 4.1 está listada como "under development" para Jakarta EE 12 na página oficial de especificações (`jakarta.ee/specifications/enterprise-beans/`).

## Na prática

O código abaixo mostra um padrão típico encontrado em legados: um `@Stateless` com timer agendado e acesso transacional, seguido do equivalente moderno em CDI puro.

**Estilo EJB (legado ativo):**

```java
import jakarta.ejb.Schedule;
import jakarta.ejb.Stateless;
import jakarta.ejb.TransactionAttribute;
import jakarta.ejb.TransactionAttributeType;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

@Stateless
public class PedidoServiceBean {

    @PersistenceContext
    private EntityManager em;

    // Transação REQUIRED por padrão no @Stateless
    public void processarPedido(Long pedidoId) {
        Pedido pedido = em.find(Pedido.class, pedidoId);
        pedido.setStatus("PROCESSADO");
        // commit automático ao final do método (CMT)
    }

    @TransactionAttribute(TransactionAttributeType.REQUIRES_NEW)
    public void auditarPedido(Long pedidoId) {
        // abre NOVA transação independente da chamadora
        em.persist(new AuditLog(pedidoId, "AUDITADO"));
    }

    @Schedule(hour = "1", minute = "30", second = "0", persistent = false)
    public void expirarPedidosAntigos() {
        em.createQuery("UPDATE Pedido p SET p.status = 'EXPIRADO' " +
                       "WHERE p.criadoEm < :limite")
          .setParameter("limite", LocalDate.now().minusDays(30))
          .executeUpdate();
    }
}
```

**Equivalente moderno em CDI:**

```java
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;
import jakarta.transaction.Transactional.TxType;

@ApplicationScoped
public class PedidoService {

    @Inject
    private EntityManager em;

    @Transactional                           // equivalente a REQUIRED
    public void processarPedido(Long pedidoId) {
        Pedido pedido = em.find(Pedido.class, pedidoId);
        pedido.setStatus("PROCESSADO");
    }

    @Transactional(TxType.REQUIRES_NEW)
    public void auditarPedido(Long pedidoId) {
        em.persist(new AuditLog(pedidoId, "AUDITADO"));
    }

    // CDI base não tem @Schedule — depende de extensão
    // (ex: Jakarta Batch, ou scheduler do servidor/framework do Spring)
}
```

**Comparação justa:**

| Aspecto | EJB (`@Stateless`) | CDI (`@ApplicationScoped` + `@Transactional`) |
|---|---|---|
| Transação CMT | Automática por método (`@TransactionAttribute`) | Requer `@Transactional` explícito (JTA interceptor) |
| Timer declarativo | `@Schedule` nativo na spec | Sem equivalente na spec CDI base |
| Pooling de instâncias | Sim (contêiner gerencia o pool) | Não — `@ApplicationScoped` é singleton |
| Acesso remoto | Suportado na spec | Fora do escopo do CDI |
| Acoplamento à spec | `jakarta.ejb.*` | `jakarta.enterprise.*` + `jakarta.transaction.*` |
| Portabilidade de código | Qualquer servidor Jakarta EE | Qualquer servidor Jakarta EE (CDI é obrigatório) |

O que se ganha migrando para CDI: código com menos dependência do contêiner EJB, mais fácil de testar em isolamento (sem servidor completo), e alinhado com o modelo que a plataforma prioriza. O que se perde: timer service nativo e pooling gerenciado automaticamente — lacunas que precisam ser preenchidas por outra spec ou ferramenta.

## Armadilhas

### (1) Tratar EJB como sinônimo de "Java enterprise moderno"

**Descrição:** Candidatos com histórico em stacks legados às vezes usam "EJB" e "Java enterprise" como sinônimos no currículo ou em entrevista, sinalizando que a referência parou em Java EE 5/6.

**Cenário:** Em entrevista para uma vaga com stack Jakarta EE 10 + Quarkus, o candidato descreve sua arquitetura como "uso session beans para tudo" sem mencionar CDI, `@Transactional`, ou o modelo atual.

**Fix:** Atualizar o vocabulário. O modelo central hoje é CDI. EJB é uma spec que coexiste para casos específicos (timer, remoting, legado). A frase correta é: "trabalhei com EJB em sistema legado e conheço a diferença para o modelo CDI atual."

### (2) Reescrever EJB estável sem business case

**Descrição:** O instinto de modernizar pode levar a propostas de reescrita de código EJB funcional sem avaliar custo, risco e payoff real.

**Cenário:** Um sistema de gestão financeira tem 800 session beans `@Stateless` funcionando em produção há 10 anos, cobrindo regras de negócio críticas. A proposta é "migrar tudo para CDI puro" como objetivo de sprint.

**Fix:** Migração tem custo (tempo de engenharia, risco de regressão, testes de integração) e benefício (manutenibilidade, alinhamento com a plataforma atual). O business case precisa justificar o trade-off. Refatoração incremental com escopo delimitado é mais defensável do que reescrita total.

### (3) Confundir entity beans (CMP) com JPA entities

**Descrição:** O nome "entity" aparece em dois contextos muito diferentes. Entity beans do EJB 2.x (com CMP) são uma tecnologia morta, tornada opcional desde o EJB 3.2. As `@Entity` do JPA são a persistência viva e central da plataforma — historia completamente separada.

**Cenário:** Em uma revisão de código, alguém comenta "entity beans foram depreciados, então não deveríamos usar `@Entity`." O raciocínio está errado: entity beans do EJB 2.x foram depreciados; JPA entities (`jakarta.persistence.@Entity`) são a spec de persistência oficial e ativa.

**Fix:** Diferenciar terminologia com precisão: "entity bean" (EJB 2.x, CMP, opcional/morto) vs. "JPA entity" (`@Entity`, Jakarta Persistence, ativa). São specs distintas com histórias distintas.

### (4) Descartar conhecimento de EJB ao entrevistar para vaga com legado

**Descrição:** O movimento de valorizar apenas tecnologias "modernas" pode levar a omitir ou subestimar experiência com EJB, justamente quando a vaga tem sistema legado expressivo.

**Cenário:** A vaga é em banco de médio porte com sistema core em Java EE 6 (EJB 3.1). O candidato omite experiência com EJB no currículo por achar que "vai contra" o perfil senior moderno. O entrevistador pergunta sobre session beans stateful e o candidato hesita.

**Fix:** Conhecimento de EJB em contexto de legado é diferencial concreto — não é bagagem a esconder. A postura correta é apresentar o conhecimento com contexto: "trabalhei com EJB 3.x, entendo o modelo de CMT, e sei quando migrar para CDI faz sentido vs. quando o legado deve ser mantido." Honestidade sobre o stack demonstra maturidade.

## Em entrevista

### Frase pronta (inglês)

"EJB was the standard enterprise component model for over a decade, solving real problems like declarative transaction management, security, and remote access before lighter alternatives existed. The complexity of EJB 2.x — home interfaces, XML descriptors, entity beans with CMP — drove the community toward simpler approaches and eventually shaped the simplification in EJB 3.x, which introduced annotations and POJOs. Today, CDI has taken over as the primary managed bean model, absorbing dependency injection, scopes, and interceptors; EJB 4.0 remains stable and relevant for timer service, remote access, and existing enterprise systems where the migration cost outweighs the benefit."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Bean sem estado | Stateless session bean |
| Bean com estado | Stateful session bean |
| Bean singleton | Singleton session bean |
| Bean dirigido a mensagem | Message-driven bean (MDB) |
| Gerenciamento de transação pelo contêiner | Container-Managed Transaction (CMT) |
| Gerenciamento de transação pelo bean | Bean-Managed Transaction (BMT) |
| Persistência gerenciada pelo contêiner | Container-Managed Persistence (CMP) |
| Interface home (legado) | Home interface |
| Serviço de timer declarativo | Declarative timer service |
| Atributo de transação | Transaction attribute |
| Pooling de instâncias | Instance pooling |
| Passivação / ativação | Passivation / activation |

## Veja também

- [[04 - CDI — beans e injeção]]
- [[11 - JTA — transações na plataforma]]
- [[13 - CDI avançado — interceptors, decorators e extensões]]
- [[14 - Jakarta EE hoje — a plataforma sob o Spring]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#EJB (Enterprise JavaBeans)|EJB (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#session bean|session bean (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#MDB (message-driven bean)|MDB (Dicionário)]]

## Referências

- Jakarta Enterprise Beans 4.0 Specification — página oficial: <https://jakarta.ee/specifications/enterprise-beans/4.0/>. Acesso: 2026-06-07.
- Jakarta Enterprise Beans 4.0 Core Spec (HTML): <https://jakarta.ee/specifications/enterprise-beans/4.0/jakarta-enterprise-beans-spec-core-4.0.html>. Acesso: 2026-06-07.
- Jakarta Enterprise Beans — todas as versões (inclui 4.1 "under development"): <https://jakarta.ee/specifications/enterprise-beans/>. Acesso: 2026-06-07.
