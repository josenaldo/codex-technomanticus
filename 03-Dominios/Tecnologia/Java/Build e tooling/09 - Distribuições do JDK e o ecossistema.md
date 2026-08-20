---
title: "Distribuições do JDK e o ecossistema"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - build
  - iniciado
  - jdk
  - sdkman
aliases:
  - "JDK distributions"
  - "Temurin"
  - "Corretto"
---

# Distribuições do JDK e o ecossistema

> [!abstract] TL;DR
> **OpenJDK** é o projeto open-source de referência do Java — o código-fonte. Uma **distribuição** é um binário compilado a partir desse código, com selo de certificação, política de suporte e licença próprios. O bytecode que sai de qualquer distribuição certificada é o mesmo. Desde 2021 o **Oracle JDK** voltou a ser **grátis para produção** sob a **NFTC** (No-Fee Terms and Conditions), desfazendo o pânico de licenciamento de 2019. Alternativas como **Eclipse Temurin**, **Amazon Corretto**, **Azul Zulu**, **BellSoft Liberica** e **Microsoft Build of OpenJDK** são **GPLv2 + Classpath Exception**. As **LTS** são **17, 21 (set/2023) e 25 (16/09/2025)**, com nova cadência de **uma LTS a cada 2 anos** (próxima: **Java 29, set/2027**). Versões non-LTS (24, 26) têm suporte de **só 6 meses**. **SDKMAN** instala e troca versões de JDK localmente.

## O que é

"Baixar o Java" parece trivial até você abrir a página de downloads e descobrir que existem dez fornecedores diferentes, cada um com um nome de licença distinto, e que o mesmo número de versão (digamos, Java 21) aparece em todos eles. A confusão é compreensível, e o vocabulário ajuda a desfazê-la.

**OpenJDK** é o projeto de referência: um repositório open-source, mantido sob o guarda-chuva da Oracle e da comunidade, onde o Java é de fato desenvolvido. É lá que as JEPs (JDK Enhancement Proposals) viram código. Mas o OpenJDK é *código-fonte* — ele não te entrega um instalador pronto com suporte de longo prazo, builds para todas as plataformas e um SLA.

Uma **distribuição** (ou *build*) do JDK é um binário que um fornecedor compila a partir do código do OpenJDK, certifica contra o TCK (Technology Compatibility Kit, a suíte oficial de conformidade) e empacota com sua própria política de patches de segurança, suporte e licença. Como todas partem do mesmo código de referência e passam pelo mesmo TCK, **o bytecode e o comportamento são equivalentes** — a diferença está no entorno: quem te dá patches, por quanto tempo, e sob quais termos legais.

Uma analogia que costuma destravar a confusão: o OpenJDK está para o Java como o **kernel Linux** está para as distribuições Linux. Ninguém roda "o kernel" puro em produção — roda Ubuntu, Debian, Fedora, cada um empacotando o mesmo kernel com suas próprias políticas de release e suporte. Com o Java é igual: você não roda "o OpenJDK", roda Temurin, Corretto, Oracle JDK — todos o mesmo núcleo, embalados de formas diferentes.

## Por que importa

A escolha da distribuição quase nunca muda como seu código roda — muda quem responde quando algo quebra em produção e quanto isso custa. Em entrevista e no trabalho real, três perguntas recorrem:

1. **"Java é pago?"** — Não, e quem responde "sim" está preso ao trauma de 2019 (ver adiante). Você pode rodar Java em produção, comercialmente, sem pagar nada, escolhendo praticamente qualquer distribuição — inclusive a própria da Oracle a partir da v17.
2. **"Qual distribuição usar?"** — Depende de ecossistema e suporte, não de performance. Quem está na AWS tende a Corretto; quem quer neutralidade de fornecedor e governança comunitária vai de Temurin; quem precisa de SLA pago com 24/7 contrata Azul ou Oracle.
3. **"Posso ficar em qualquer versão?"** — Não impunemente. Rodar uma **non-LTS em produção** significa que em 6 meses não há mais patches de segurança — uma armadilha clássica.

Errar isso custa caro: ou você paga licença sem precisar, ou roda produção numa versão sem patches, ou descobre tarde demais que sua distribuição "grátis" virou cobrável depois de uma janela de updates.

Há também uma dimensão de *compliance* que pega empresas grandes de surpresa: auditorias de licenciamento. Quem deixou o Oracle JDK instalado em servidores sob a licença OTN (sem assinatura) durante a era do pânico pode receber cobrança retroativa. A defesa moderna é simples e barata: padronizar numa distribuição **GPLv2+CE** (Temurin, Corretto, etc.), onde não há sequer a possibilidade dessa cobrança, ou usar o Oracle JDK ciente da janela NFTC. A escolha da distribuição, portanto, não é só técnica — é também jurídica e financeira.

## Como funciona

### OpenJDK (o projeto) vs distribuição (o binário)

Pense no OpenJDK como a *receita* e nas distribuições como *padarias*. Todas seguem a mesma receita certificada (TCK), então o pão tem o mesmo sabor. O que muda é o serviço: por quanto tempo a padaria mantém aquele pão fresco (janela de suporte), se cobra entrega (suporte pago) e sob qual contrato você o consome (licença).

Concretamente: um `.jar` compilado com Temurin 21 roda idêntico sob Corretto 21 ou Oracle JDK 21. Não há "lock-in" de bytecode. Trocar de distribuição é, na prática, trocar o binário do JDK e revalidar seu pipeline — não reescrever código.

Vale separar dois selos de qualidade que as distribuições sérias exibem:

- **TCK / JCK** — a suíte de conformidade oficial. Passar nela é o que autoriza um binário a se chamar "Java SE". Garante *compatibilidade*: que o build implementa a especificação corretamente.
- **AQAvit** — uma suíte de qualidade complementar (mantida no âmbito do Adoptium) que vai além da conformidade, exercitando robustez, performance e segurança. Temurin, por exemplo, é "AQAvit verified" além de TCK-certified.

A lição para entrevista: "todas as distribuições certificadas são intercambiáveis a nível de bytecode" é verdade, mas o que você está realmente comprando (ou escolhendo de graça) é a *cadeia de suprimento* — quem compila, com que rigor de teste, e por quanto tempo te entrega patches. Por isso a pergunta certa nunca é "qual é mais rápida?", e sim "quem dá suporte, por quanto tempo, e sob qual licença?".

### A história da licença: 2019 → 2021 (o trauma e a correção)

O mito "tem que pagar pra usar Java" nasce de um evento real e mal-comunicado:

- **Antes de 2019**: o Oracle JDK era grátis para a maioria dos usos sob a antiga BCL.
- **2019 (Java 11)**: a Oracle mudou o **Oracle JDK** para a licença **OTN** (Oracle Technology Network). O uso comercial/produção passou a **exigir assinatura paga**. O uso gratuito ficou restrito a desenvolvimento, testes e uso pessoal. *Isto valia apenas para o binário Oracle JDK* — o OpenJDK e distribuições como Temurin/Corretto continuaram grátis. Mas o recado chegou distorcido, e instalou-se o pânico de que "Java agora é pago".
- **2021 (Java 17)**: a Oracle introduziu a **NFTC (No-Fee Terms and Conditions)**. Sob a NFTC, o **Oracle JDK voltou a ser grátis inclusive para produção e redistribuição comercial**, sem taxa. A NFTC é a licença do Oracle JDK a partir da v17 — e segue como licença para v21 e posteriores.

O detalhe fino que vira pegadinha de entrevista: a NFTC dá updates gratuitos por uma janela. Para uma LTS, os updates do Oracle JDK ficam sob NFTC **até cerca de um ano após a LTS seguinte**; depois disso, os updates daquela versão migram para a OTN paga. Ou seja, você não paga para *usar* a versão, mas para continuar recebendo *patches* dela depois que a janela gratuita fecha. Por isso muita gente prefere uma distribuição GPLv2+CE, onde a janela de patches segue a política do fornecedor sem virar cobrança.

### O calendário: LTS, non-LTS e a nova cadência de 2 anos

O Java sai em **release de funcionalidade a cada 6 meses** (março e setembro). A maioria dessas versões é **non-LTS**: recebe atualizações por apenas **6 meses**, até a próxima sair. Periodicamente uma versão é marcada **LTS (Long-Term Support)**, com anos de patches.

A cadência de LTS **mudou de 3 anos para 2 anos**. A sequência LTS recente:

- **Java 17** — LTS (set/2021)
- **Java 21** — LTS (set/2023)
- **Java 25** — LTS (16/09/2025)
- **Java 29** — próxima LTS planejada (set/2027)

E as non-LTS recentes, com suporte de apenas 6 meses: **Java 24 (18/03/2025)** e **Java 26 (17/03/2026)**.

A regra prática: **produção fica em LTS**; non-LTS serve para experimentar features novas em dev/CI, sabendo que o relógio de suporte é curto.

Por que a Oracle encurtou a cadência de 3 para 2 anos? A justificativa pública é reduzir a distância que uma equipe precisa saltar entre LTS consecutivas. Pulando de LTS em LTS a cada 3 anos, você acumulava 6 releases de funcionalidade entre uma migração e outra — um salto grande, com muito *deprecation* e mudança de comportamento de uma vez só. A cada 2 anos, são 4 releases entre LTS: migrações mais frequentes, porém menores e menos arriscadas. A contrapartida é que mais releases passam a carregar o selo LTS ao longo do tempo, e os times precisam planejar upgrades num ritmo um pouco mais apertado.

Um ponto que confunde iniciantes: o número da versão **não** indica "estabilidade" — a Java 26 é mais nova que a Java 25, mas é a 25 (LTS) que você quer em produção. "Mais recente" e "mais apoiada por mais tempo" são eixos diferentes. As features de uma non-LTS não somem: elas se acumulam e chegam consolidadas na próxima LTS. Quem rodou a 24 e a 26 em dev colhe na 25 (e depois na 29) o que experimentou.

### As distribuições, uma a uma

Todas as alternativas abaixo partem do mesmo OpenJDK e são certificadas — a diferença é posicionamento e suporte, não comportamento.

- **Oracle JDK** — a build da própria Oracle. Sob **NFTC** a partir da v17, é grátis para produção comercial dentro da janela de updates; depois dessa janela, os patches daquela versão migram para a OTN paga. É a escolha natural de quem já tem contrato Oracle ou quer suporte comercial direto da fonte.
- **Eclipse Temurin** — produzida pelo Adoptium Working Group (sob a Eclipse Foundation). É a opção *neutra de fornecedor* por excelência: governança comunitária, sem amarra a uma nuvem ou empresa, **GPLv2+CE**. Costuma ser o "default seguro" quando não há um motivo específico para escolher outra.
- **Amazon Corretto** — a build da AWS, **GPLv2+CE**, com patches mantidos pela Amazon e alinhamento natural a Lambda, EC2 e ECS. Faz sentido para quem já vive no ecossistema AWS e quer a mesma build da nuvem na máquina local.
- **Azul Zulu** — build da Azul, **GPLv2+CE** na versão Community, com opções comerciais pagas (suporte estendido, builds otimizadas) à parte. Forte presença em ambientes que exigem SLA e suporte de longo prazo contratado.
- **BellSoft Liberica** — build da BellSoft, **GPLv2+CE**, conhecida por imagens "full" (que incluem JavaFX) e por foco em ARM e dispositivos embarcados; suporte comercial à parte.
- **Microsoft Build of OpenJDK** — build da Microsoft, **GPLv2+CE**, alinhada a Azure e ao uso interno da empresa, com ênfase em versões LTS.
- **GraalVM (Oracle)** — não é só um JDK: traz um compilador JIT avançado e capacidade de **AOT / native image**. Sob **GFTC** a partir do JDK 21, é grátis para produção comercial. O native image (compilar para um executável nativo) é assunto do **[[03-Dominios/Tecnologia/Java/Cloud-native e produção/08 - GraalVM Native Image — conceito e trade-offs|Galho 17 (GraalVM Native Image)]]** — aqui basta saber que GraalVM existe e tem licença própria.

### Onde isso vive: source vs binário

Reforçando o vocabulário com um mapa mental: o **OpenJDK** vive como repositório de código no projeto upstream. Cada fornecedor mantém uma *pipeline de build* que pega esse código (eventualmente com patches próprios de backport de segurança), compila para Windows/Linux/macOS em várias arquiteturas (x64, ARM), roda TCK/AQAvit e publica os artefatos. Quando você faz `sdk install java 21.0.4-tem`, está baixando o artefato final dessa pipeline — não compilando nada. A versão `21.0.4` segue o esquema semântico do Java (`FEATURE.INTERIM.UPDATE`), onde o `.4` é o nível de patch de segurança: subir de `21.0.3` para `21.0.4` é aplicar correções sem mudar funcionalidade.

### Patches e fim de vida (EOL)

Manter um JDK em produção é, na prática, acompanhar dois eventos:

- **Updates trimestrais (CPU)** — a cada trimestre saem versões de patch (o `.UPDATE` sobe) com correções de segurança. Para uma LTS, essas atualizações chegam pelo fornecedor da sua distribuição. Aplicá-las é rotina de manutenção, não um upgrade arriscado: o código de aplicação não muda.
- **EOL (End of Life)** — o ponto em que uma versão para de receber patches. Para non-LTS isso acontece em ~6 meses; para LTS, anos depois. Bater no EOL com produção rodando é o cenário a evitar: a partir dali, vulnerabilidades novas não são corrigidas naquela versão.

O detalhe que distingue distribuições aqui é *por quanto tempo* cada fornecedor estende os patches de uma LTS — a janela varia entre eles e, no caso do Oracle JDK, é onde a transição NFTC → OTN paga entra em cena. Para planejar, vale consultar o roadmap de suporte da distribuição escolhida em vez de assumir um prazo único para todas.

## Na prática

```text
Distribuição × Licença × Posicionamento

Distribuição                  | Licença              | Posicionamento
------------------------------|----------------------|--------------------------------------------------
Oracle JDK                    | NFTC (v17+/v21+)     | Build de referência da Oracle; grátis p/ produção
                              |                      | na janela NFTC; suporte pago via OTN depois
Eclipse Temurin (Adoptium)    | GPLv2 + Classpath    | Build comunitária, neutra de fornecedor; o
                              | Exception            | "default seguro" para quem não quer lock-in
Amazon Corretto               | GPLv2 + Classpath    | Build da AWS; alinhada a Lambda/EC2; suporte
                              | Exception            | da Amazon sem custo extra na nuvem
Azul Zulu                     | GPLv2 + Classpath    | Build da Azul; opção comercial robusta com SLA
                              | Exception            | pago (Zulu Prime / suporte estendido) à parte
BellSoft Liberica             | GPLv2 + Classpath    | Build da BellSoft; forte em embarcado e em
                              | Exception            | imagens "full" (com JavaFX); suporte pago à parte
Microsoft Build of OpenJDK    | GPLv2 + Classpath    | Build da Microsoft; alinhada a Azure e ao uso
                              | Exception            | interno; foco em LTS
GraalVM (Oracle)              | GFTC (JDK 21+)       | Build da Oracle com JIT/AOT avançados; grátis
                              |                      | p/ produção sob GFTC; AOT/native image é Galho 17
```

Gerir versões locais com **SDKMAN** (instala JDKs, e também Maven/Gradle):

```bash
# listar JDKs disponíveis (mostra fornecedores e sufixos: -tem, -amzn, -zulu...)
sdk list java

# instalar uma build específica (sufixo -tem = Temurin)
sdk install java 21.0.4-tem

# usar uma versão só na sessão atual do shell
sdk use java 21.0.4-tem

# definir o default global da máquina
sdk default java 21.0.4-tem

# trocar para experimentar uma non-LTS em dev (NÃO em produção)
sdk install java 24.0.1-tem
sdk use java 24.0.1-tem

# o mesmo mecanismo gere build tools
sdk install maven
sdk install gradle

# conferir qual JDK/distribuição está ativo no shell
sdk current java
java -version
```

Os sufixos (`-tem`, `-amzn`, `-zulu`, `-librca`, `-oracle`, `-graal`) indicam a distribuição — você escolhe fornecedor e versão na mesma linha de comando, sem caçar instaladores em sites.

Em CI, o padrão equivalente é a action `setup-java` (no GitHub Actions), que recebe `distribution:` (`temurin`, `corretto`, `zulu`, `liberica`, `oracle`, `microsoft`) e `java-version:`. A ideia é a mesma do SDKMAN: pinar fornecedor e versão de forma explícita e reproduzível, em vez de depender de "o que estava instalado na máquina". E há ainda o mecanismo nativo do próprio build tool — **toolchains** (Galho 13) — que deixa o Maven/Gradle baixar e selecionar o JDK certo por projeto, independente do JDK que roda o build em si.

## Armadilhas

### (1) Achar que precisa pagar a Oracle para usar Java em produção

Resíduo do trauma de 2019. Hoje há **duas** saídas gratuitas para produção comercial: usar o **Oracle JDK sob NFTC** (v17+), ou usar qualquer distribuição **GPLv2+CE** (Temurin, Corretto, Zulu, Liberica, Microsoft). Você só paga se *quiser* suporte comercial com SLA, ou se ficar no Oracle JDK *após* a janela de updates gratuitos da NFTC fechar e quiser continuar recebendo patches daquela versão via OTN. "Java é pago" é falso como afirmação geral.

### (2) Usar non-LTS (24, 26) em produção sem entender o suporte de só 6 meses

Versões non-LTS recebem patches de segurança por **apenas 6 meses**, até a próxima release de funcionalidade. Subir a Java 24 ou 26 em produção e esquecer ali significa rodar, em meio ano, uma versão **sem nenhum patch** — risco de segurança direto. Non-LTS é para *experimentar* features novas em dev/CI; produção fica nas **LTS (17, 21, 25)**, que têm anos de suporte. Confundir o número mais alto com "o melhor para produção" é o erro clássico.

### (3) Misturar distribuições entre build e runtime sem perceber

É comum compilar o projeto com uma distribuição (digamos, Temurin local) e empacotar a imagem de produção sobre outra (digamos, a base oficial `eclipse-temurin` ou um `corretto` no Docker). Em si, isso não quebra nada — o bytecode é o mesmo. O perigo é *não saber* qual distribuição roda em produção: quando um CVE da JVM aparece, você precisa saber de quem cobrar o patch e em qual base atualizar. A higiene é fixar a distribuição explicitamente em todo lugar (SDKMAN local, `setup-java` no CI, tag de imagem no Docker) e tratar "qual JDK roda em prod" como informação versionada, não como acidente do ambiente.

## Em entrevista

### Frase pronta (inglês)

> OpenJDK is the open-source reference project — the source code — while a *distribution* is a binary that a vendor compiles from it, certifies against the TCK, and ships with its own support and license terms; the bytecode is the same across all of them. Since 2021, Oracle's own JDK is free for production again under the NFTC, which corrected the licensing scare from the Java 11 era — and alternatives like Eclipse Temurin, Amazon Corretto and Azul Zulu are GPLv2 with the Classpath Exception. For production I stick to LTS releases — currently 17, 21 and 25, with the cadence now every two years and Java 29 due in 2027 — because non-LTS versions like 24 and 26 only get six months of updates, and I manage all of this locally with SDKMAN.

### Mini-roteiro de decisão (para responder "qual você usaria?")

1. Está numa nuvem específica? Use a build daquele fornecedor (Corretto na AWS, Microsoft no Azure) — patches alinhados, suporte sem custo extra.
2. Quer neutralidade e governança comunitária? **Temurin**.
3. Precisa de SLA comercial com suporte 24/7? **Azul** ou **Oracle JDK** com assinatura.
4. Em qualquer caso: **produção em LTS** (17/21/25), non-LTS só em dev/CI, e fixe a distribuição explicitamente em todo o pipeline.

O entrevistador raramente quer um nome de fornecedor "certo" — quer ver que você entende os *eixos de decisão* (suporte, licença, ecossistema, janela de patches) e que não confunde "Java pago" com a realidade pós-NFTC.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| projeto open-source de referência; o código-fonte onde o Java é desenvolvido | OpenJDK |
| binário do JDK compilado por um fornecedor e certificado contra o TCK | Distribution / build |
| suíte oficial de conformidade que um build precisa passar para se chamar Java SE | TCK (Technology Compatibility Kit) |
| release com patches por vários anos (17, 21, 25); a próxima é a 29 em 2027 | LTS (Long-Term Support) |
| licença da Oracle que torna o Oracle JDK grátis para produção a partir da v17 | NFTC (No-Fee Terms and Conditions) |
| licença open-source do Temurin, Corretto, Zulu, Liberica e builds da Microsoft | GPLv2 + Classpath Exception |
| licença do GraalVM, grátis para produção a partir do JDK 21 | GFTC (GraalVM Free Terms and Conditions) |
| a mudança do intervalo de 3 anos para 2 anos entre releases LTS | Two-year LTS cadence |
| suíte adicional de qualidade/robustez (Adoptium) além da conformidade TCK | AQAvit |
| o ciclo trimestral de patches de segurança que sobe o nível de update | CPU (Critical Patch Update) |
| o ponto em que um release para de receber patches de segurança | EOL (End of Life) |
| a licença paga por trás do pânico de 2019 e dos updates pós-janela NFTC | OTN (Oracle Technology Network) License |
| não atrelado a uma única nuvem ou empresa (o argumento de venda do Temurin) | Vendor-neutral |
| o release da cadência de 6 meses, com apenas 6 meses de updates (ex.: 24, 26) | Non-LTS / feature release |
| o passo do GitHub Actions que fixa distribuição e versão no CI | `setup-java` |

### Frase pronta alternativa (curta)

> "Java itself is free — the licensing question is about which *distribution* and what *support window*. I default to a GPLv2+CE build like Temurin, pin it explicitly across local, CI and Docker, and keep production on an LTS."

## Veja também

- [[03-Dominios/Tecnologia/Java/JVM/01 - A JVM — o que é e o pipeline de execução|A JVM (Galho 3)]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/13 - Toolchains — buildar com um JDK, mirar outro|Toolchains]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/08 - Maven vs Gradle — trade-offs honestos|Maven vs Gradle]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Oracle — Java SE Support Roadmap (cadência de releases e LTS, datas): https://www.oracle.com/java/technologies/java-se-support-roadmap.html
- Oracle — Moving the JDK to a Two Year LTS Cadence: https://blogs.oracle.com/java/moving-the-jdk-to-a-two-year-lts-cadence
- Oracle — Oracle JDK License General FAQs (NFTC e histórico OTN): https://www.oracle.com/java/technologies/javase/jdk-faqs.html
- Oracle — No-Fee Terms and Conditions (NFTC) License Agreement: https://www.oracle.com/downloads/licenses/no-fee-license.html
- Oracle — Introducing the GraalVM Free License (GFTC): https://blogs.oracle.com/graal/graalvm-free-license
- Eclipse Adoptium — Temurin (GPLv2 + Classpath Exception): https://adoptium.net/ — FAQ: https://adoptium.net/docs/faq/
- SDKMAN!: https://sdkman.io/
- Java version history (datas de release 17/21/24/25/26): https://en.wikipedia.org/wiki/Java_version_history
