---
title: "Por que existe um framework de arquitetura"
type: concept
fase: Iniciado
created: 2026-07-20
updated: 2026-07-20
status: seedling
publish: true
tags:
  - cloud
  - aws
  - digitalocean
  - well-architected
  - arquitetura
---
# Por que existe um framework de arquitetura

> [!abstract] TL;DR
> O AWS Well-Architected Framework não nasceu como uma lista de conformidade para auditor marcar "sim/não" — nasceu como um conjunto de **perguntas** que arquitetos da AWS já faziam informalmente, comparando o que dava errado (Root Cause Analysis) com o que uma arquitetura deveria ter garantido desde o início. Formalizado em 2015 a partir de práticas internas que já rodavam desde 2012, ele hoje tem seis pilares — excelência operacional, segurança, confiabilidade, eficiência de performance, otimização de custo e sustentabilidade — cada um com seus próprios princípios de design e sua própria lista de perguntas. Uma review "bem-arquitetada" de verdade é uma conversa sem culpa, de horas, não uma auditoria de dias. E aqui já vale plantar a semente que fecha este galho: os seis pilares **puxam a arquitetura em direções que se contradizem entre si** — não existe uma resposta que maximize todos ao mesmo tempo, só um trade-off explícito e defensável.

## A pergunta que ninguém sabe responder direito

Um time termina de subir uma nova versão do sistema de pagamentos: microsserviços em containers, banco gerenciado, fila entre os componentes, autoscaling configurado, HTTPS em todo lugar, backups automáticos. Funciona. Os testes passam. A demo para o time de produto foi um sucesso. Alguém do lado de negócio, satisfeito, pergunta uma coisa aparentemente simples: "então, está tudo certo? Isso está bem arquitetado?"

E aí a sala fica quieta.

Ninguém sabe responder com confiança, porque "está tudo certo" não é uma pergunta técnica — é um julgamento de valor que depende de critério, e ninguém no time definiu, por escrito, qual é esse critério antes de começar a construir. "Funciona" e "está bem arquitetado" não são a mesma coisa. Um sistema pode passar em todos os testes de integração e ainda assim ter um único ponto de falha que derruba tudo numa manhã de sexta-feira; pode estar seguro contra os ataques óbvios e mesmo assim conceder permissões amplas demais a um serviço que só precisava ler um bucket; pode escalar bonito sob carga simulada e ainda assim custar três vezes o necessário porque ninguém revisou o tamanho das instâncias desde o protótipo.

O mesmo silêncio acontece, com uma tensão diferente, numa entrevista técnica sênior. O entrevistador desenha um sistema no quadro e pergunta: "o que você mudaria nessa arquitetura?" Um candidato júnior aponta um ou dois problemas óbvios — "eu adicionaria um cache aqui", "isso parece um single point of failure". Um candidato sênior faz outra coisa: organiza a crítica em eixos — "do ponto de vista de confiabilidade, isso é um problema; do ponto de vista de custo, essa escolha é razoável; do ponto de vista de segurança, eu questionaria essa permissão" — e, principalmente, é honesto sobre o fato de que melhorar um eixo frequentemente piora outro. Essa organização em eixos não é um talento inato do candidato sênior. É um framework que ele aprendeu a usar, tantas vezes, que virou reflexo.

Esse framework existe, tem nome, e é o assunto desta nota e do galho inteiro que ela abre: o **AWS Well-Architected Framework**. E a primeira coisa a entender sobre ele é de onde veio — porque a origem explica por que ele é feito de perguntas, e não de uma lista de caixinhas para marcar.

## De onde veio: uma prática interna que virou framework público

O Well-Architected Framework não foi desenhado numa sala de reunião de marketing para lançar um produto. Ele nasceu de uma prática interna da AWS que já existia informalmente desde 2012, dentro do próprio trabalho dos Solutions Architects da empresa — as pessoas que, todos os dias, ajudavam clientes (e a própria AWS) a revisar arquiteturas em produção.

A lógica por trás dessa prática é simples e um pouco desconfortável: toda vez que um sistema falha de um jeito significativo — um incidente sério, uma reclamação de cliente, uma vulnerabilidade explorada — alguém escreve uma **Root Cause Analysis** (RCA, análise de causa raiz), documentando o que deu errado e por quê. A AWS, ao longo de anos revisando milhares de arquiteturas de clientes e sistemas próprios, percebeu um padrão: as mesmas categorias de pergunta apareciam, de novo e de novo, nas RCAs de incidentes completamente diferentes. "Vocês tinham um plano de recuperação testado?" "Quem tinha acesso a esse recurso, e por quê?" "Isso escalava automaticamente, ou alguém precisava intervir manualmente?" Essas perguntas recorrentes, quando reunidas, viraram literalmente o esqueleto do framework: não é uma lista de "boas práticas" abstratas importadas de um livro-texto — é uma coleção destilada de "isso já causou um incidente antes, então perguntamos sempre".

O framework foi ao público em novembro de 2015, na conferência re:Invent, quando o CTO da Amazon, Werner Vogels, anunciou o whitepaper "AWS Well-Architected Framework". Naquele primeiro lançamento público, existiam quatro pilares — segurança, confiabilidade, eficiência de performance e otimização de custo. Em 2016, a AWS formalizou o processo de review conduzido por Solutions Architects para clientes Enterprise Support e, no mesmo ano, adicionou um quinto pilar, excelência operacional — reconhecendo que arquitetura não é só o desenho estático do sistema, mas também a disciplina de operá-lo e evoluí-lo com segurança ao longo do tempo. O sexto e mais recente pilar, sustentabilidade, chegou em 2021, ampliando o critério de "bem-arquitetado" para incluir o impacto ambiental de rodar aquele sistema — região escolhida, eficiência de recursos, desperdício de capacidade.

> [!info] Caducidade
> A publicação atual do AWS Well-Architected Framework tem data de revisão de 6 de novembro de 2024, segundo a documentação oficial. O framework é revisado com regularidade — a AWS já passou por oito versões desde 2012. Confira a data de revisão mais recente na documentação antes de citar qualquer detalhe como definitivo.

Esse histórico importa porque explica uma decisão de design que, de outra forma, pareceria arbitrária: por que o framework é feito de **perguntas** — "como você opera o workload com segurança?", "como você recupera de falha?" — e não de uma lista de "faça X, não faça Y"? Porque uma pergunta força quem está revisando a pensar no contexto específico daquele sistema, enquanto uma regra fixa tenta empurrar todo sistema para a mesma resposta, mesmo quando o contexto não pede aquela resposta. A AWS documenta isso explicitamente: o framework é "premised on a set of design principles that influences architectural approach, and questions that verify that people don't neglect areas that often featured in Root Cause Analysis". Tradução prática: os princípios de design dizem a direção geral; as perguntas garantem que ninguém esqueça de olhar para uma área que, historicamente, é onde as coisas quebram.

## Um corpo de perguntas, não um checklist de conformidade

Aqui está a distinção que separa quem usa o framework bem de quem o usa mal, e ela é sutil o suficiente para escapar de quem só ouviu falar dele de longe: **o Well-Architected Framework não é um checklist de conformidade**. Não existe uma pontuação de aprovação, não existe um "selo" que uma arquitetura ganha ao passar em todas as perguntas, e — isso é dito explicitamente na documentação oficial — o processo de revisão **não é um mecanismo de auditoria**.

A diferença entre checklist e corpo de perguntas não é semântica, é estrutural. Um checklist tem itens binários: "criptografia em trânsito habilitada? sim/não." Uma pergunta do Well-Architected Framework é aberta e força uma resposta contextualizada: "**como você opera o workload com segurança?**" (essa é, literalmente, a primeira pergunta do pilar de Segurança, "SEC 1", no texto oficial). Não existe resposta única certa para essa pergunta — a resposta certa para um serviço interno de baixo risco, mantido por dois engenheiros, é diferente da resposta certa para um sistema de pagamentos regulado, com dezenas de pessoas tocando o código. O checklist trataria os dois sistemas igual; a pergunta obriga quem responde a justificar a escolha para o contexto daquele sistema específico.

Isso tem uma consequência direta sobre o que significa "bem-arquitetado": **a expressão é sempre relativa ao contexto e ao momento**, nunca um estado absoluto que um sistema atinge de uma vez por todas. Um sistema que estava bem-arquitetado há dois anos pode não estar mais — porque a carga cresceu dez vezes, porque um novo requisito regulatório apareceu, porque a equipe que o mantém mudou de três pessoas seniores para uma pessoa júnior sozinha, ou simplesmente porque a AWS lançou um serviço gerenciado novo que torna obsoleta a solução caseira que o time construiu em 2019. Um sistema "bem-arquitetado" em 2020 pode estar "mal-arquitetado" hoje sem que uma única linha de código nele tenha mudado — porque o contexto ao redor dele mudou, e a barra do que conta como bom se moveu junto.

```mermaid
flowchart TB
    subgraph Origem["De onde veio"]
        RCA["RCAs de incidentes reais<br/>(2012 em diante)"] --> Padroes["Padrões recorrentes<br/>de causa raiz"]
        Padroes --> Framework["Well-Architected Framework<br/>público (2015)"]
    end
    subgraph Estrutura["Como é feito"]
        Framework --> Principios["Princípios de design<br/>(direção geral, por pilar)"]
        Framework --> Perguntas["Perguntas abertas<br/>(ex.: SEC 1 — 'como você opera<br/>o workload com segurança?')"]
    end
    subgraph Uso["Como é usado"]
        Principios --> Review["Review — conversa,<br/>não auditoria"]
        Perguntas --> Review
        Review --> Contexto["Resposta certa depende<br/>do contexto e do momento —<br/>nunca é absoluta"]
    end
```

## Os seis pilares — nomeados aqui, desenvolvidos nas próximas notas

O framework organiza suas perguntas e princípios de design em seis categorias, chamadas de **pilares**. Esta nota só os nomeia — cada um ganha sua própria nota no restante deste galho, onde a mecânica de cada pilar é desenvolvida em profundidade:

1. **Excelência operacional** — operar e evoluir sistemas com segurança, aprendendo com falha sem cultura de culpa.
2. **Segurança** — proteger dados, sistemas e ativos, aproveitando as capacidades específicas da nuvem para isso.
3. **Confiabilidade** — garantir que um sistema cumpre sua função de forma consistente, e se recupera de falha sem intervenção manual heroica.
4. **Eficiência de performance** — usar os recursos computacionais de forma eficiente diante de uma carga e de uma tecnologia que mudam com o tempo.
5. **Otimização de custo** — evitar gasto desnecessário e entender de onde vem cada centavo da fatura.
6. **Sustentabilidade** — minimizar o impacto ambiental de rodar aquele sistema, o pilar mais recente do framework.

Cada pilar tem sua própria lista de perguntas — geralmente numeradas, como "SEC 1", "REL 2", "COST 3" — e seus próprios princípios de design, que são recomendações de direção (por exemplo, "implemente uma base de identidade forte" é um dos princípios de design do pilar de Segurança). Nenhum desses seis pilares será desenvolvido em profundidade aqui — essa é, literalmente, a razão de existir das próximas seis notas deste galho.

> [!info] Fronteira
> Excelência operacional, na prática de SRE — SLOs, postmortems, incident response — já tem casa própria no vault: [[03-Dominios/Engenharia/Operação/index|Operação (DevOps/SRE)]]. O pilar de excelência operacional, aqui, é o *critério de arquitetura* que justifica investir nessas práticas — não uma reexplicação delas.

## Como uma review acontece de verdade

Vale desfazer, com algum detalhe, a imagem que a palavra "review" costuma evocar em quem vem de processos de auditoria formal — sala fechada, checklist impresso, um avaliador de fora marcando itens em silêncio. Não é assim que uma Well-Architected Review funciona, e a documentação oficial é explícita sobre isso: deve ser "**lightweight** (hours not days)" e conduzida com "**blame-free approach that encourages diving deep**" — leve, de horas e não de dias, sem cultura de culpa, e que encoraja mergulhar fundo nos detalhes em vez de ficar na superfície.

Na prática, o formato recomendado é quase o oposto de uma auditoria: uma série de **conversas informais** sobre a arquitetura, onde a maior parte das respostas às perguntas do framework emerge naturalmente da discussão — seguida, se necessário, de uma ou duas reuniões focadas para esclarecer pontos de ambiguidade ou risco percebido. O material recomendado para essas reuniões também é revelador do tom pretendido: uma sala com quadro branco, impressões dos diagramas de arquitetura, e uma lista de ações para perguntas que precisam de pesquisa fora da reunião ("ativamos criptografia ou não? vamos confirmar e responder depois"). É trabalho de engenharia colaborativo, não interrogatório.

Um detalhe conceitual que vale carregar para qualquer decisão de arquitetura, não só para reviews formais, é a distinção entre **decisões de mão única e decisões de mão dupla** ("one-way doors" e "two-way doors", no vocabulário da própria AWS). Decisões de mão dupla são reversíveis — você pode tentar, errar, e voltar atrás sem grande custo; para essas, um processo leve é suficiente. Decisões de mão única são difíceis ou impossíveis de reverter — trocar o banco de dados principal de um sistema em produção, comprometer-se publicamente com uma API que terceiros vão consumir, escolher uma região onde dados regulados vão residir — e essas exigem mais inspeção *antes* de serem tomadas, porque o custo de errar não é "ajustar depois", é "reconstruir do zero". Uma boa review acontece cedo o suficiente na fase de design para pegar decisões de mão única antes que elas se tornem irreversíveis na prática, e de novo antes do go-live — e depois, de forma contínua, à medida que o sistema evolui em produção.

E aqui há outro ponto que a documentação oficial recomenda explicitamente, e que contraria a intuição de quem imagina o Well-Architected Framework como um evento único: o ideal não é uma "reunião de review" formal e pontual, marcada uma vez no calendário — é que os próprios membros do time usem o framework **continuamente**, revisando a arquitetura à medida que ela evolui, em vez de esperar por um evento formal. Uma review de verdade não termina com um relatório arquivado; termina com uma lista de ações priorizadas, e a expectativa de que a próxima review vai medir se essas ações realmente melhoraram alguma coisa.

Times que ainda não passaram por uma review costumam resistir com objeções previsíveis — "estamos ocupados demais com o lançamento", "não temos tempo para agir nos resultados", "não queremos expor os segredos da nossa implementação". A resposta institucional da AWS a cada uma delas é consistente: exatamente por estar perto de um lançamento é que vale a pena descobrir riscos antes, não depois; mesmo sem tempo para resolver tudo, ter um playbook para os riscos identificados já vale a review; e as perguntas do framework, por desenho, nunca pedem informação técnica ou comercial proprietária — só pedem que o time responda, para si mesmo, se cobriu as bases que historicamente causam incidentes.

## O teaser que fecha esta nota: os pilares não convivem em paz

Aqui vale nomear, sem ainda desenvolver, a tensão mais importante que existe dentro do framework — e que a nota 07 deste galho vai desenrolar por completo. Os seis pilares não são seis dimensões independentes que uma boa arquitetura simplesmente maximiza todas ao mesmo tempo. Eles **empurram em direções que se contradizem**, com frequência.

Confiabilidade, levada ao extremo, custa dinheiro: réplicas redundantes em múltiplas zonas de disponibilidade, testes de recuperação de desastre regulares, capacidade extra reservada para absorver picos sem degradar — tudo isso é exatamente o tipo de gasto que o pilar de otimização de custo pede para questionar. Segurança, levada ao extremo, custa velocidade: cada camada extra de aprovação, cada controle adicional de acesso, cada etapa de validação antes de um deploy é fricção a mais entre "o código está pronto" e "o código está em produção" — o tipo de fricção que o pilar de excelência operacional, com sua ênfase em mudanças pequenas e frequentes, tenta minimizar. Eficiência de performance, levada ao extremo, pode entrar em tensão direta com sustentabilidade — a instância mais rápida nem sempre é a mais eficiente em consumo de energia por unidade de trabalho útil entregue.

Nenhuma dessas tensões tem uma resposta universal certa. Um sistema de pagamentos regulado vai, com razão, priorizar segurança e confiabilidade mesmo pagando o preço em custo e velocidade. Um protótipo em fase de validação de produto vai, com igual razão, priorizar velocidade de entrega mesmo aceitando risco maior em confiabilidade. A pergunta que separa uma decisão de arquitetura sênior de uma decisão ingênua nunca é "qual pilar eu maximizo" — é "qual trade-off eu estou fazendo, explicitamente, e consigo justificar por que essa é a prioridade certa para este sistema, agora". Fazer esse trade-off de forma explícita e documentada — em vez de fingir, para si mesmo ou para o time, que dá para maximizar os seis pilares ao mesmo tempo — é exatamente a habilidade que a nota 07 vai ensinar a exercitar.

## Well-Architected além da AWS

O Well-Architected Framework, como produto com esse nome específico, é uma criação da AWS — não existe um "framework Well-Architected" genérico e vendor-neutro que todo provedor de nuvem implemente da mesma forma. Dito isso, a ideia central — organizar critério de arquitetura em pilares nomeados, cada um com seus próprios princípios — não ficou restrita à AWS. A Microsoft mantém o próprio **Azure Well-Architected Framework**, com cinco pilares (confiabilidade, segurança, otimização de custo, excelência operacional e eficiência de performance — sem um pilar de sustentabilidade dedicado, embora o tema apareça transversalmente). O Google Cloud mantém o próprio **Google Cloud Well-Architected Framework**, também com seis pilares — excelência operacional, segurança/privacidade/compliance, confiabilidade, otimização de custo, otimização de performance e sustentabilidade. Vale reconhecer o vocabulário se ele aparecer numa conversa sobre Azure ou GCP — mas o corpo desta trilha usa a versão AWS como referência canônica, porque é o vocabulário-padrão que aparece com mais frequência em entrevista técnica sênior e em discussões cross-cloud.

Na DigitalOcean, não existe um framework nomeado equivalente — e isso é informação, não lacuna: DigitalOcean se posiciona como uma nuvem mais simples, com um catálogo de produtos menor e menos superfície de decisão arquitetural para cobrir com um framework formal de pilares. Isso não significa que os critérios do Well-Architected Framework não se apliquem a um sistema rodando em DigitalOcean — significa apenas que não existe um documento oficial da própria DigitalOcean organizando esses critérios em pilares nomeados. As perguntas continuam valendo; só o "selo" institucional que as organiza é específico da AWS.

## Casos práticos

**A pergunta que a review revela antes do incidente revelar.** Um time está prestes a lançar uma funcionalidade nova, sob pressão de prazo. Alguém sugere uma review rápida antes do go-live — duas horas, não dois dias. Durante a conversa, ao passar pela pergunta "como você recupera de falha nesse componente?" (uma das perguntas centrais do pilar de Confiabilidade), o time percebe que ninguém testou, de fato, o procedimento de recuperação documentado — ele foi escrito, mas nunca exercitado. A review não impede o lançamento; ela transforma um risco invisível em um item de ação explícito, com prazo, antes que ele vire um incidente às três da manhã.

**A tensão entre pilares aparecendo numa decisão concreta.** Um time discute se deve adicionar uma camada extra de aprovação manual antes de qualquer deploy em produção, motivado por um requisito de segurança levantado numa auditoria externa. Um membro do time, aplicando o vocabulário do framework, nomeia a tensão em vez de só discordar: "isso melhora segurança, mas empurra contra excelência operacional — vai reduzir a frequência de deploys pequenos, que é exatamente o que reduz risco de mudança grande". A decisão final — manter a aprovação manual só para mudanças em componentes que tocam dados sensíveis, liberando o resto do pipeline — nasce de nomear o trade-off, não de fingir que ele não existe.

**A review usada como ferramenta de aprendizado de equipe, não de fiscalização.** Um engenheiro sênior, ao revisar a arquitetura de um time júnior pela primeira vez usando as perguntas do framework, descobre — e essa é uma experiência documentada como comum — que o próprio time que construiu o sistema nunca havia parado para responder, de forma explícita, várias das perguntas básicas sobre ele. A review não vira uma lista de erros do time júnior; vira o primeiro momento em que aquele time entende, de fato, o que construiu.

## Armadilhas comuns

> [!warning] Tratar o framework como checklist de conformidade
> Se uma review termina em "22 de 30 perguntas com 'sim'", alguém perdeu o ponto. As perguntas do framework existem para provocar julgamento contextualizado, não para gerar uma pontuação. Um sistema pode responder "não" honestamente a uma pergunta e ainda assim ser uma escolha correta para o contexto dele — desde que essa escolha seja consciente e documentada, não um "esquecemos disso".

> [!warning] Fazer a review uma vez e arquivar o resultado
> "Bem-arquitetado" não é um estado permanente — é relativo ao contexto e ao momento. Uma arquitetura revisada há dois anos, sem revisão desde então, provavelmente já desalinhou de alguma coisa: carga mudou, requisitos mudaram, serviços gerenciados novos apareceram. O framework foi desenhado para uso contínuo pelo próprio time que constrói, não para um evento único conduzido por um auditor externo.

> [!warning] Achar que existe uma resposta que maximiza todos os pilares
> Confiabilidade custa dinheiro. Segurança custa velocidade. Performance pode custar sustentabilidade. Qualquer decisão de arquitetura que pretenda "otimizar tudo ao mesmo tempo" está, na prática, escondendo um trade-off em vez de decidir sobre ele. A habilidade sênior não é evitar o trade-off — é nomeá-lo, documentá-lo, e revisitá-lo quando o contexto mudar. A nota 07 deste galho é inteiramente sobre como fazer isso bem.

## O que vem a seguir

Esta nota respondeu *por que* esse framework existe e *o que* ele é, no nível mais alto: um corpo de perguntas nascido de incidentes reais, organizado em seis pilares, usado como conversa contínua em vez de auditoria pontual. Mas nomear os seis pilares não é o mesmo que entendê-los — cada um tem seus próprios princípios de design, suas próprias perguntas numeradas, e sua própria forma de aparecer numa arquitetura real. A próxima nota entra no primeiro deles: **Excelência operacional** — o pilar sobre operar e evoluir sistemas com segurança, e a razão pela qual "infraestrutura como código" e "mudança pequena e reversível" não são só bordões de DevOps, são critério de arquitetura.

## Fontes

- [AWS Well-Architected Framework — Welcome (documentação oficial)](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) — definição do framework, publication date 6 de novembro de 2024, papel do AWS Well-Architected Tool; acessado em 2026-07-20.
- [AWS Well-Architected Framework — The review process (documentação oficial)](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-review-process.html) — como uma review acontece de verdade: leve, sem culpa, conversa não auditoria, decisões de mão única vs. mão dupla, objeções comuns de times; acessado em 2026-07-20.
- [AWS Well-Architected Framework — The pillars of the framework (documentação oficial)](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html) — nomes oficiais dos seis pilares; acessado em 2026-07-20.
- [AWS Well-Architected Framework — Security pillar, Security foundations (documentação oficial)](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-security.html) — texto verbatim da pergunta "SEC 1: How do you securely operate your workload?"; acessado em 2026-07-20.
- [AWS Well-Architected Framework — Security pillar whitepaper, Security foundations (documentação oficial)](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/security.html) — princípios de design do pilar de Segurança; acessado em 2026-07-20.
- [AWS — Well-Architected homepage](https://aws.amazon.com/architecture/well-architected/) — visão geral dos seis pilares e do AWS Well-Architected Tool; acessado em 2026-07-20.
- [AWS Architecture Blog — Announcing updates to the AWS Well-Architected Framework guidance](https://aws.amazon.com/blogs/architecture/announcing-updates-to-the-aws-well-architected-framework-guidance/) — linha do tempo oficial: origem em 2012, whitepaper em 2015, pilar de Excelência Operacional em 2016, pilar de Sustentabilidade em 2021; acessado em 2026-07-20.
- [History of AWS Well-Architected (Bram Verhagen, dev.to)](https://dev.to/bramverhagen/history-of-aws-well-architected-3k2k) — detalhamento da origem em 2012 com Philip "Fitz" Fitzsimons e o anúncio do whitepaper por Werner Vogels no re:Invent 2015; fonte secundária, não oficial da AWS, usada para complementar a linha do tempo confirmada na fonte anterior; acessado em 2026-07-20.
- [Microsoft — Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/) — pilares do framework equivalente da Microsoft, usado só como vocabulário de tradução; acessado em 2026-07-20.
- [Google Cloud — Well-Architected Framework](https://cloud.google.com/architecture/framework) — seis pilares do framework equivalente do Google Cloud, usado só como vocabulário de tradução; acessado em 2026-07-20.
