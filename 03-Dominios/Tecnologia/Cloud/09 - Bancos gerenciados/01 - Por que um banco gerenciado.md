---
title: "Por que um banco gerenciado"
type: concept
fase: Iniciado
created: 2026-07-23
updated: 2026-07-25
status: seedling
publish: true
tags:
  - cloud
  - aws
  - digitalocean
  - bancos
  - database
  - rds
---
# Por que um banco gerenciado

> [!abstract] TL;DR
> O galho 8 terminou mostrando que, por baixo de quase todo serviço gerenciado, existe um dos três primitivos de armazenamento — e que um banco de dados gerenciado roda o engine sobre um volume de **block storage**, exatamente como qualquer instância comum. Esta nota sobe uma camada: em vez de olhar para o disco por baixo, olha para o **serviço inteiro** que embrulha esse disco — o **banco de dados gerenciado (managed database)**. A ideia central é simples de enunciar e cara de ignorar: rodar PostgreSQL ou MySQL numa instância que você mesmo administra funciona perfeitamente bem até a primeira 3 da manhã em que o disco enche, o processo trava, ou uma falha de segurança exige patch urgente — e aí a pergunta vira "quem está de plantão para isso?". Um banco gerenciado é o provedor de nuvem assumindo o trabalho operacional não-diferenciado — provisionamento, patching de sistema operacional e do engine, backup automático, failover, monitoramento, replicação — e devolvendo a você um endpoint de conexão. Você continua dono do que só você pode decidir: o schema, as queries, os índices, o tuning da aplicação. Isso não é gratuito: managed custa mais por hora que a mesma instância crua, e você abre mão de acesso root ao sistema operacional. Este galho — depois deste mapa — mergulha em bancos relacionais gerenciados (RDS e o Managed Database da DigitalOcean), NoSQL gerenciado (DynamoDB) e cache gerenciado, sempre com a mesma pergunta de fundo: o que o provedor tira das suas costas, e o que continua seu.

## O problema: o banco que caiu às 3 da manhã

Imagine a seguinte história, comum o bastante para soar familiar a qualquer time que já rodou produção por conta própria: uma startup sobe um PostgreSQL numa instância EC2 (ou um Droplet da DigitalOcean) porque "é só instalar o `postgresql-server`, configurar e pronto" — e de fato é. O banco sobe, a aplicação conecta, tudo funciona nos primeiros meses. Ninguém questiona a decisão, porque não há nada de errado com ela — até o dia em que várias coisas pequenas, invisíveis até então, deixam de ser invisíveis ao mesmo tempo.

Uma madrugada de sexta para sábado, o disco daquela instância enche — os logs de transação (WAL, no caso do PostgreSQL) cresceram sem que ninguém tivesse configurado rotação, porque configurar rotação de WAL nunca esteve na lista de tarefas de ninguém. O processo do banco trava aceitando escrita. A aplicação inteira, que depende desse banco, começa a devolver erro 500 para todo mundo. Um alarme dispara — se é que existe um alarme configurado, o que nem sempre é verdade nessa fase de uma startup. Quem recebe esse alarme, às 3 da manhã, precisa responder a uma sequência de perguntas que ninguém tinha pensado antes:

- Como faço o disco crescer sem derrubar o banco de vez?
- Existe um backup recente? Quando foi a última vez que alguém *testou* restaurar esse backup, não só criá-lo?
- Existe uma réplica pronta para assumir enquanto o disco principal é consertado, ou o site simplesmente fica fora do ar até alguém acordar e agir manualmente?
- O patch de segurança que saiu semana passada para essa versão do PostgreSQL — alguém aplicou? Alguém sequer estava rastreando que ele existia?

Nenhuma dessas perguntas é sobre o **produto** que a startup constrói. Nenhuma delas aparece no roadmap de features, nenhuma delas empolga ninguém no time. É exatamente esse o ponto: administrar um banco de dados de produção — patch, backup testado, failover, monitoramento de disco, replicação — é trabalho real, contínuo, especializado, e **não é o trabalho que a empresa foi fundada para fazer**. AWS descreve esse tipo de tarefa, em outros contextos de nuvem, como "undifferentiated heavy lifting" — o peso operacional que toda empresa de tecnologia precisa carregar, mas que não diferencia uma empresa da concorrente. Ganhar a briga de "quem administra melhor o PostgreSQL" nunca foi a vantagem competitiva de nenhuma startup: a vantagem competitiva está no produto que roda em cima do banco.

## O mecanismo: o que "gerenciado" tira das suas costas — e o que continua seu

Um **banco de dados gerenciado** é um serviço em que o provedor de nuvem assume a operação do banco — o dia a dia de mantê-lo de pé, seguro e íntegro — e entrega, em troca, um **endpoint de conexão**: um host e uma porta aos quais a aplicação se conecta como se fosse qualquer outro banco, sem que ninguém precise fazer SSH na máquina por trás dele. A AWS documenta essa divisão com uma tabela de responsabilidades que compara três modelos — banco on-premises, banco numa instância EC2 crua, e RDS — e a diferença entre os dois últimos é exatamente o ponto desta nota: mesmo já estando na nuvem, rodar o banco "na mão" dentro de uma instância deixa scaling, alta disponibilidade, backup, patching do engine e do sistema operacional inteiramente por sua conta; o RDS move todas essas linhas para a coluna "AWS".

Vale nomear com precisão o que muda de mãos:

- **Provisionamento**: criar o disco, alocar CPU/memória certos para a carga, configurar rede — o provedor faz com um comando ou um clique, em vez de você instalar um sistema operacional do zero.
- **Patching**: atualizações de segurança do sistema operacional e do próprio engine (PostgreSQL, MySQL etc.) passam a ser aplicadas pelo provedor, geralmente numa janela de manutenção configurável — não mais uma tarefa manual que alguém precisa lembrar de fazer.
- **Backups automáticos**: snapshots diários e, no caso da AWS, backup contínuo de transaction log que viabiliza restauração para um ponto específico no tempo (point-in-time recovery) — sem que ninguém precise escrever e testar um script de `pg_dump` em cron.
- **Failover**: se o provedor oferece um modo de alta disponibilidade (Multi-AZ na AWS, uma réplica standby na DigitalOcean), a promoção de uma réplica a primária, quando a instância principal falha, acontece de forma automatizada — em minutos, sem intervenção manual às 3 da manhã.
- **Monitoramento**: métricas de CPU, memória, conexões, IOPS chegam prontas num painel (CloudWatch na AWS, o painel de métricas da DigitalOcean), sem que alguém precise instalar e manter um agente de monitoramento à parte.
- **Replicação**: réplicas de leitura, criadas com um comando, sem que o operador precise configurar manualmente `pg_basebackup`, slots de replicação e streaming replication à mão.

O que **não** muda de mãos — porque nenhum provedor consegue fazer isso por você, dado que depende do seu domínio de negócio — é justamente o que fica dentro do banco: o **schema** (quais tabelas, quais colunas, quais tipos), as **queries** que a aplicação executa, os **índices** que aceleram (ou não) essas queries, e o **connection pooling** feito no lado da aplicação. A própria AWS é explícita sobre esse limite: o RDS é responsável por hospedar a infraestrutura e o software do banco, mas "você é responsável pelo tuning de query" — e tuning de query "depende muito do design do banco, do tamanho dos dados, da distribuição dos dados, da carga da aplicação e dos padrões de query", processos que a AWS chama de "altamente individualizados" e que continuam seus.

> [!tip] Assista: RDS Overview: Understanding Amazon Relational Database Service (RDS)
> **Canal:** AWS For Everyone | **Duração:** ~6min | **Idioma:** EN
>
> Um resumo rápido e direto do que o provedor assume ao ligar o RDS — útil como segunda voz confirmando a lista de responsabilidades que esta seção acabou de nomear, sem se alongar em nenhuma delas.
> Trecho de destaque [01:54]: *"it has inbuilt failover capabilities it has automated backups (...) it provides multi-az support (...) another really cool functionality (...) called read replicas"*
>
> 🎬 [Assistir no YouTube](https://www.youtube.com/watch?v=qelK_DMqJsc)

```mermaid
flowchart LR
    subgraph SelfHosted["Self-hosted (EC2 / Droplet)"]
        direction TB
        SH1["Você: provisiona o disco"]
        SH2["Você: instala e faz patch do SO"]
        SH3["Você: instala e faz patch do engine"]
        SH4["Você: escreve e testa backup"]
        SH5["Você: configura failover manual"]
        SH6["Você: monta monitoramento"]
        SH7["Você: schema, queries, índices"]
    end
    subgraph Managed["Banco gerenciado (RDS / Managed DB)"]
        direction TB
        M1["Provedor: provisiona o disco"]
        M2["Provedor: patch do SO"]
        M3["Provedor: patch do engine"]
        M4["Provedor: backup automático + PITR"]
        M5["Provedor: failover automatizado"]
        M6["Provedor: monitoramento pronto"]
        M7["Você: schema, queries, índices"]
    end
```

A tabela do AWS User Guide compara diretamente os três modelos de operação — vale reproduzi-la porque ela é a fonte mais direta desta divisão:

| Responsabilidade | On-premises | EC2 (self-hosted) | RDS (gerenciado) |
|---|---|---|---|
| Otimização da aplicação | Cliente | Cliente | Cliente |
| Escala | Cliente | Cliente | AWS |
| Alta disponibilidade | Cliente | Cliente | AWS |
| Backup do banco | Cliente | Cliente | AWS |
| Patch do software do banco | Cliente | Cliente | AWS |
| Instalação do software do banco | Cliente | Cliente | AWS |
| Patch do sistema operacional | Cliente | Cliente | AWS |
| Instalação do sistema operacional | Cliente | Cliente | AWS |
| Manutenção do servidor físico | Cliente | AWS | AWS |
| Ciclo de vida do hardware | Cliente | AWS | AWS |

> [!info] Fronteira — modelo de responsabilidade compartilhada
> Esta tabela é uma aplicação, ao domínio de banco de dados, do modelo de responsabilidade compartilhada já visto no galho 2 desta trilha: [[03-Dominios/Tecnologia/Cloud/02 - Anatomia de um provedor/index|Anatomia de um provedor]]. O eixo "segurança **da** nuvem" (infraestrutura, hardware, patch de SO) versus "segurança **na** nuvem" (dados, controle de acesso, classificação de ativos) continua valendo aqui — só que, com um banco gerenciado, a linha divisória sobe: o provedor absorve o patch do engine e do SO, mas a AWS é explícita que "os clientes continuam responsáveis por gerenciar seus dados... e usar as ferramentas de IAM para aplicar as permissões apropriadas". O galho 2 não é reexplicado aqui — só retomado no ponto específico de banco de dados.

## Casos práticos: criando um banco gerenciado, na lente dupla

**Na AWS, criar uma instância RDS mínima** é um único comando — repare que não existe um passo de "instalar o PostgreSQL" ou "aplicar patch de segurança" em lugar nenhum deste fluxo, porque esses passos deixaram de existir do lado do usuário:

```bash
$ aws rds create-db-instance \
    --db-instance-identifier loja-web-prod \
    --db-instance-class db.t4g.micro \
    --engine postgres \
    --engine-version 16.4 \
    --master-username admin_loja \
    --master-user-password "SenhaTemporariaForte#2026" \
    --allocated-storage 20 \
    --backup-retention-period 7 \
    --no-publicly-accessible
```

```bash
$ aws rds describe-db-instances \
    --db-instance-identifier loja-web-prod \
    --query 'DBInstances[0].[DBInstanceStatus,Endpoint.Address,Endpoint.Port]' \
    --output table
```

A aplicação conecta usando o endpoint devolvido — um host que a AWS gerencia por trás, não um IP fixo de uma instância que você criou à mão:

```bash
$ psql "host=loja-web-prod.abcdefghijk.us-east-1.rds.amazonaws.com \
    port=5432 dbname=loja user=admin_loja sslmode=require"
```

**Na DigitalOcean, o equivalente conceitual é o Managed Database**, criado via `doctl` — o mesmo padrão de "descreva o que você quer, receba um endpoint pronto":

```bash
$ doctl databases create loja-web-prod \
    --engine pg \
    --version 16 \
    --region nyc1 \
    --size db-s-1vcpu-1gb \
    --num-nodes 1
```

```bash
$ doctl databases connection <database-id> --format Host,Port,User,Database
```

```bash
$ psql "postgresql://doadmin:SENHA@loja-web-prod-do-user-123456-0.b.db.ondigitalocean.com:25060/defaultdb?sslmode=require"
```

Em ambos os casos, o que a aplicação recebe é um único elemento: uma **string de conexão** apontando para um endpoint gerenciado. Tudo que aconteceu antes dela existir — provisionar o disco, instalar o engine na versão pedida, configurar backup, colocar o banco atrás de uma rede privada — foi trabalho do provedor, não seu.

```mermaid
flowchart TB
    Dev["Time de desenvolvimento"] -->|"1 comando:<br/>create-db-instance / databases create"| Provider["Provedor de nuvem"]
    Provider -->|"Provisiona disco,<br/>instala engine,<br/>configura rede"| Infra["Infraestrutura pronta<br/>(invisível ao dev)"]
    Provider -->|"Devolve"| Endpoint["Endpoint de conexão<br/>host:porta"]
    Endpoint --> App["Aplicação conecta<br/>como qualquer banco"]
    Provider -.->|"Contínuo, automático"| Ops["Patch · Backup ·<br/>Failover · Monitoramento"]
```

## O que este galho cobre — a camada de dados gerenciada

Este galho olha para três camadas diferentes de banco gerenciado, cada uma resolvendo um formato de dado diferente — o mesmo tipo de eixo "quem acessa, com que semântica" que organizou o galho 8 de armazenamento:

```mermaid
flowchart LR
    Galho9["Galho 9: Bancos gerenciados"]
    Galho9 --> Relacional["Relacional gerenciado<br/>(notas 02-04)<br/>RDS / Managed DB Postgres-MySQL"]
    Galho9 --> NoSQL["NoSQL gerenciado<br/>(nota 05)<br/>DynamoDB"]
    Galho9 --> Cache["Cache gerenciado<br/>(nota 06)<br/>ElastiCache / Managed Redis-Valkey"]
```

> [!info] Fronteira — modelagem de dados e escolha SQL vs NoSQL
> Este galho trata bancos gerenciados como **serviço de infraestrutura** — o que o provedor opera por você. A teoria de modelagem de dados, normalização e o desenho de schema pertencem ao domínio [[03-Dominios/Engenharia/Dados/index|Dados]]. E a decisão arquitetural de "SQL ou NoSQL para este problema" — um trade-off de consistência, escala e forma de acesso — é uma decisão de System Design; o capstone 06 deste galho retoma esse ponto na hora de comparar RDS com DynamoDB, sem reabrir a teoria completa.

## O catálogo: o que cada provedor oferece como banco gerenciado

| Engine / tipo | AWS | DigitalOcean |
|---|---|---|
| Relacional (SQL) | RDS: PostgreSQL, MySQL, MariaDB, Oracle, SQL Server, IBM Db2; Aurora (compatível MySQL/PostgreSQL) | Managed Database: PostgreSQL, MySQL |
| NoSQL documento | DynamoDB (chave-valor/documento), DocumentDB | MongoDB |
| Cache em memória | ElastiCache (Redis, Valkey, Memcached) | Managed Database: Valkey (compatível Redis) |
| Streaming / fila | MSK (Kafka gerenciado) | Managed Database: Kafka |
| Busca | OpenSearch Service | Managed Database: OpenSearch |

> [!info] Caducidade
> Este catálogo reflete a documentação consultada em 2026-07-23. A DigitalOcean expandiu seu catálogo de Managed Databases nos últimos anos (Kafka, MongoDB e OpenSearch são adições relativamente recentes); vale checar a lista de produtos da DigitalOcean antes de assumir esta tabela como definitiva ao planejar uma arquitetura real.

| Conceito | AWS | Azure | GCP |
|---|---|---|---|
| Relacional gerenciado | Amazon RDS | Azure SQL Database / Azure Database for PostgreSQL-MySQL | Cloud SQL |
| Relacional gerenciado nativo de nuvem | Aurora | — | AlloyDB |
| NoSQL gerenciado | DynamoDB | Cosmos DB | Firestore / Bigtable |
| Cache gerenciado | ElastiCache | Azure Cache for Redis | Memorystore |

## O trade-off honesto: managed custa mais, e você perde acesso root

Nada disso vem de graça, e fingir o contrário seria desonesto. Dois custos reais valem ser nomeados antes de qualquer entusiasmo:

**Custo por hora mais alto.** Uma instância RDS `db.t4g.micro` custa mais por hora que uma instância EC2 `t4g.micro` crua de tamanho equivalente — o provedor está cobrando, junto com a capacidade computacional, o trabalho operacional descrito nesta nota. Para uma carga pequena e previsível, essa diferença pode ser irrelevante frente ao custo de uma pessoa de plantão; para uma frota grande, rodando há anos, o acumulado pode justificar reconsiderar o modelo — é uma conta que vale refazer periodicamente, não assumir de um lado ou de outro para sempre.

**Perda de acesso root ao sistema operacional e a parte da configuração do engine.** Rodar seu próprio PostgreSQL numa EC2 dá acesso de superusuário ao sistema operacional, à instalação de qualquer extensão exótica do PostgreSQL, e a parâmetros de baixo nível que o RDS pode não expor (ou expor só parcialmente, via grupo de parâmetros). Cenários legítimos para continuar self-hosted incluem: uma extensão de banco pouco comum que o provedor não suporta, controle regulatório que exige acesso físico ou de SO auditável, uma migração lift-and-shift de um sistema legado com dependências de configuração muito específicas, ou escala tão grande que a engenharia própria de operação de banco já supera, em ganho, o custo do time necessário para mantê-la.

## Armadilhas comuns

> [!warning] Achar que "managed" significa "não preciso pensar em mais nada"
> O erro mais caro é tratar "banco gerenciado" como sinônimo de "banco que cuida de si mesmo". O provedor tira de você o patch, o backup, o failover — mas a query lenta que faz um full table scan em uma tabela de dez milhões de linhas continua lenta, com ou sem RDS. Um índice faltando continua faltando. Nenhum provedor de nuvem lê o padrão de acesso da sua aplicação e cria o índice certo sozinho.

> [!warning] Subestimar o custo de managed na hora de orçar
> É comum comparar o preço por hora de uma instância RDS só com o preço por hora de uma instância EC2 do mesmo tamanho, e concluir que managed é "caro". Essa comparação ignora o que está sendo comprado: o tempo de engenharia que deixaria de ser gasto em patch, backup e resposta a incidente. A comparação honesta é "custo total de propriedade", não só a etiqueta de preço por hora.

> [!warning] Lock-in em features proprietárias do provedor
> Bancos como o Amazon Aurora oferecem ganhos reais de performance e disponibilidade — mas fazem isso com uma camada de armazenamento distribuído proprietária da AWS, incompatível com qualquer outro provedor. Migrar de Aurora para PostgreSQL genérico (ou para outro provedor) exige um dump/restore completo, não uma troca de configuração. Adotar uma feature proprietária de banco gerenciado é uma decisão arquitetural, não um detalhe de implementação — vale saber, no momento de adotar, que essa porta de saída ficou mais estreita.

## Um cenário concreto: do Postgres na EC2 para o RDS

Volte à startup do início desta nota, mas agora depois da madrugada ruim. O time se senta, decide migrar o PostgreSQL da EC2 para o RDS, e vale acompanhar passo a passo o que muda — porque a migração em si não é mágica: é um `pg_dump`/`pg_restore` (ou, para minimizar downtime, uma réplica lógica criada com AWS Database Migration Service) de um banco Postgres para outro banco Postgres. O RDS não lê o schema antigo e o conserta; ele só passa a hospedar exatamente o mesmo schema, as mesmas tabelas, os mesmos índices — bons ou ruins — que já existiam.

O que desaparece da lista de tarefas do time, já na primeira semana:

- **O cron do `pg_dump`.** Antes, alguém tinha escrito e mantinha um script como este, torcendo para que o disco de destino nunca enchesse:

  ```bash
  # crontab de alguém, às 2h da manhã, self-hosted
  0 2 * * * pg_dump -Fc loja > /backups/loja-$(date +\%F).dump
  0 3 * * * find /backups -mtime +7 -delete
  ```

  Depois da migração, esse cron simplesmente some. O RDS já faz snapshot diário mais backup contínuo de transaction log, viabilizando restauração para qualquer minuto dentro do período de retenção — sem que ninguém precise lembrar de rodar ou testar o script.
- **A pergunta "o disco vai encher hoje?"** — o RDS pode ser configurado com storage autoscaling, crescendo sozinho até um teto definido, em vez de alguém monitorar `df -h` manualmente.
- **Configurar replicação de standby na mão.** Ativar Multi-AZ é uma opção no console ou uma flag no `create-db-instance`, não uma sessão de `pg_basebackup` e `recovery.conf` decorado de cor.
- **Aplicar o patch de segurança da versão do engine.** A AWS aplica na janela de manutenção configurada; o time só decide *quando*, não *como*.

O que **continua** exatamente do mesmo tamanho, porque nenhum provedor pode fazer isso por você:

- O schema continua sendo o schema que o time desenhou — migrations (Flyway, Alembic, o que for) continuam rodando do lado da aplicação, na mesma ordem de sempre.
- Os índices que faltavam antes da migração continuam faltando depois dela; o RDS não olha para uma query lenta e cria um índice sozinho.
- O connection pooling (PgBouncer, ou o pool nativo do driver) continua sendo configuração da aplicação — o RDS não sabe quantas conexões simultâneas o seu framework abre por padrão.
- Revisar `EXPLAIN ANALYZE` de uma query que ficou lenta continua sendo trabalho humano, de gente que entende o schema.

O diálogo muda de forma reveladora. **Antes**, a pergunta de plantão às 3h era operacional: "o disco encheu, como eu drenagem o WAL sem perder dado?". **Depois**, se alguém é acordado, a pergunta tende a ser de aplicação: "essa query específica ficou lenta depois do deploy de ontem — o que mudou no código?". A migração não elimina incidentes; ela muda a *categoria* dos incidentes que sobram, empurrando os operacionais (disco, patch, failover) para o provedor e deixando os de domínio (schema, query, índice) exatamente onde só o time pode resolvê-los.

## O custo real: por que "mais caro por hora" pode sair mais barato

A comparação mais comum — e mais enganosa — é abrir o preço por hora de uma instância RDS ao lado do preço por hora de uma EC2 crua do mesmo tamanho, e concluir que managed "custa 30-50% a mais". Essa conta captura só uma linha do TCO (custo total de propriedade) e ignora todas as outras.

> [!info] Tabela ilustrativa — não são preços reais da AWS
> Os valores abaixo são unidades relativas (não dólares), só para mostrar a forma da conta. Preços reais variam por região, engine e tamanho de instância — consulte a calculadora oficial do provedor antes de orçar de verdade.

| Item de custo | Self-hosted (EC2) | Managed (RDS) |
|---|---|---|
| Instância/compute (por hora) | 10 | 14 |
| Storage | 3 | 4 |
| Backup (armazenamento + script) | 1 (+ tempo de eng.) | 2 (incluso) |
| Horas de engenharia/mês (setup, patch, monitoramento, on-call) | ~15-20h | ~1-2h |
| Risco de incidente (downtime/perda de dado por erro operacional) | Alto, cauda longa | Baixo |
| **Total percebido** | "10" (só compute) | "14" (só compute) |
| **Total real** | 10 + 3 + 1 + custo de 15-20h de eng. | 14 + 4 + 2 + custo de 1-2h de eng. |

A linha que a comparação ingênua esconde é "horas de engenharia por mês". Uma pessoa sênior de infraestrutura custa, tipicamente, dezenas a centenas de dólares por hora quando se conta salário carregado, benefícios e o custo de oportunidade de não estar trabalhando no produto. Quinze a vinte horas por mês gerenciando um banco — patch, backup testado, monitoramento de disco, resposta a incidente — somam rápido a um valor que faz a diferença de preço por hora entre EC2 e RDS parecer irrelevante. E isso antes de contar o risco de cauda longa: uma restauração de backup que falha, um failover manual que dá errado às 3 da manhã, um patch de segurança que ninguém aplicou — eventos raros, mas caros quando acontecem, e que o managed também absorve.

A regra prática, então, não é "managed é sempre melhor" — é mais estreita que isso: **managed vence quando o tempo da equipe vale mais que a diferença de preço por hora**, o que é o caso da esmagadora maioria dos times pequenos e médios, porque a alternativa é gastar o tempo escasso de gente sênior em trabalho que não diferencia o produto. Self-hosted volta a fazer sentido no eixo de custo apenas quando a escala é grande o bastante para que manter uma equipe dedicada de operação de banco custe *menos*, por unidade de carga, que o prêmio cumulativo do managed — ou quando um requisito específico (extensão exótica, controle regulatório de acesso físico) já tira a opção managed da mesa, como visto na seção anterior sobre trade-offs.

## O que vem a seguir

Este mapa nomeou o "porquê" — o que "gerenciado" tira das suas costas, o que continua seu, e onde o self-hosted ainda faz sentido. A próxima nota deste galho mergulha a fundo no banco relacional gerenciado mais usado da AWS: o RDS propriamente dito — como Multi-AZ funciona por dentro, o que são réplicas de leitura, como parameter groups controlam o comportamento do engine, e onde o Aurora se encaixa nessa história.

## Fontes

- [AWS RDS — What is Amazon Relational Database Service?](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html) — tabela de comparação de responsabilidades on-premises/EC2/RDS, responsabilidade de tuning de query do cliente, lista de engines suportados (Db2, MariaDB, SQL Server, MySQL, Oracle, PostgreSQL); acessado em 2026-07-23.
- [DigitalOcean — Managed Databases](https://docs.digitalocean.com/products/databases/) — descrição do serviço, engines oferecidos (PostgreSQL, MySQL, Kafka, MongoDB, Valkey, OpenSearch), backup diário com PITR, failover automatizado; acessado em 2026-07-23.
- [AWS — Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) — divisão "segurança da nuvem" (AWS) vs "segurança na nuvem" (cliente), aplicação a serviços gerenciados; acessado em 2026-07-23.
