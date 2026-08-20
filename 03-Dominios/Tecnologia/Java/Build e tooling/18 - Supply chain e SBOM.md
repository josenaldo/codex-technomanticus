---
title: "Supply chain e SBOM"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: Magus
tags:
  - java
  - build
  - magus
  - supply-chain
  - sbom
aliases:
  - "SBOM"
  - "CycloneDX"
  - "supply chain"
---

# Supply chain e SBOM

> [!abstract] TL;DR
> Quando o **Log4Shell** (CVE-2021-44228, dez/2021) estourou, a pergunta que travou times do mundo inteiro foi banal e devastadora: _"a gente usa Log4j onde?"_. Quem tinha um **inventário** das próprias dependências respondeu em horas; quem não tinha varreu repositórios por dias. Esse inventário é o **SBOM** (_Software Bill of Materials_): a lista completa de componentes, versões e licenças que o seu artefato embarca. O padrão dominante é o **CycloneDX** (standard Ecma International, foco em segurança/supply chain; plugins `cyclonedx-maven-plugin` e `cyclonedx-gradle-plugin` geram JSON/XML), com **SPDX** como alternativa mais voltada a licença/compliance. Mas SBOM é só o "**o quê**" — você ainda cruza esse inventário com bases de CVE via **SCA** (ex.: **OWASP Dependency-Check**) e prova **como** o artefato foi buildado via **SLSA** (proveniência/attestation, níveis L1-L3). Atenção: **CVE scan sozinho não basta** (não pega typosquatting, dependency confusion nem backdoor recém-plantado sem CVE), e SBOM (inventário) **não é** reprodutibilidade (determinismo do build).

## O que é

**Supply chain de software** é todo o caminho que um pedaço de código percorre até virar o artefato que você executa em produção: do código-fonte de uma lib transitiva qualquer, passando pelo repositório onde ela foi publicada, pelo build que a baixou e empacotou, até o JAR/imagem que sobe no servidor. Cada elo desse caminho é uma **superfície de ataque** — e a lição de 2021 foi que a maioria dos times não tinha visibilidade nenhuma sobre os elos intermediários.

O **SBOM** (_Software Bill of Materials_) é o documento que torna essa cadeia visível. Por analogia direta com a indústria: assim como um fabricante de carro mantém uma _bill of materials_ listando cada peça e fornecedor, o SBOM lista cada **componente de software** que compõe o seu produto — bibliotecas diretas e transitivas, suas **versões exatas**, **licenças** e, idealmente, identificadores que permitem cruzá-las com bases de vulnerabilidade. Não é um relatório de segurança; é um **inventário**. O valor dele aparece no dia em que uma CVE nova é divulgada e você precisa responder, em minutos, _"isso me afeta?"_.

No ecossistema Java o SBOM costuma ser gerado pelo próprio build (Maven/Gradle), porque é o build que conhece o grafo de dependências resolvido — o mesmo grafo que você estuda em [[03-Dominios/Tecnologia/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão|resolução de dependências]].

### A anatomia do problema (por que Log4Shell foi um divisor de águas)

Vale destrinchar por que a CVE-2021-44228 entrou para a história como o evento que popularizou SBOM. Log4j 2 é uma biblioteca de logging tão ubíqua no mundo Java que praticamente todo serviço a embarcava — quase sempre como **dependência transitiva**, puxada por algum framework, sem que ninguém a tivesse declarado conscientemente. Quando a falha de execução remota de código foi divulgada, o trabalho urgente de cada time não era "como mitigar" (a correção saiu rápido), era a pergunta logística anterior: **"em quais dos nossos N serviços, e em qual versão, o Log4j vulnerável está embarcado?"**.

Sem inventário, isso vira uma varredura manual: clonar cada repositório, rodar `mvn dependency:tree`, ler o grafo à mão, repetir para dezenas de serviços. Com um SBOM por artefato, arquivado em release, a mesma pergunta vira uma _query_: filtrar todos os BOMs onde `org.apache.logging.log4j:log4j-core` aparece, e ler a versão. A diferença entre dias e minutos de resposta a um incidente crítico é exatamente o que transformou SBOM de boa prática teórica em requisito operacional.

Repare ainda num detalhe que o `dependency:tree` manual esconde: o **artefato empacotado** pode conter mais do que o grafo de dependências declarado sugere. Um _fat jar_ embute classes de terceiros _shaded_ (renomeadas e reempacotadas dentro do seu JAR), e bibliotecas podem trazer recursos nativos. Um SBOM gerado a partir do build resolve isso porque parte do que o build realmente empacotou, não apenas do que você escreveu no POM — é a diferença entre "o que eu declarei" e "o que de fato embarca no binário". Em entrevista, mencionar esse cuidado com _shading_ é o tipo de detalhe que sinaliza experiência real de operação.

## Por que importa

Em entrevista sênior pós-Log4Shell, supply chain deixou de ser tema de nicho e virou pergunta de _design_ e de _operação_. O que separa quem entende do assunto:

- **Tempo de resposta a incidente**: a métrica que importa não é "temos zero CVEs" (impossível), é "quanto tempo levo para saber se a CVE de hoje me atinge". SBOM transforma isso de uma caça manual em uma _query_.
- **Compliance e contratos**: ordens como o _Executive Order 14028_ nos EUA passaram a exigir SBOM de fornecedores de software para o governo. Cliente enterprise hoje pede SBOM no onboarding. Isso significa que, em muitas organizações, gerar SBOM deixou de ser uma escolha de engenharia e virou um **requisito de venda** — sem ele, o contrato não fecha. Para o sênior, traduzir esse requisito em pipeline (não em planilha manual) é parte do trabalho.
- **Profundidade da cadeia**: o risco quase nunca está na dependência que você declarou — está três níveis abaixo, numa transitiva que você nunca leu. Só um inventário automatizado enxerga isso.
- **Camadas de defesa**: o sênior sabe articular que SBOM, SCA e proveniência (SLSA) resolvem **problemas diferentes** e se complementam. Tratar os três como sinônimo é sinal de quem nunca operou um incidente.

Há também um enquadramento que pega bem em conversa de _staff/principal_: supply chain security é, no fundo, um problema de **observabilidade aplicado às dependências**. Do mesmo jeito que você não rodaria produção sem logs e métricas porque "está funcionando", você não deveria distribuir um artefato sem saber o que tem dentro dele. O SBOM é o equivalente, no plano de build, ao que tracing e logs são no plano de runtime: o instrumento que transforma "acho que sei o que está rodando" em "sei exatamente o que está rodando, e posso provar".

## Como funciona

### SBOM e CycloneDX vs SPDX

Existem dois formatos de SBOM consolidados, e a distinção entre eles é a primeira coisa que diferencia uma resposta rasa de uma resposta sênior.

**CycloneDX** é o padrão mantido pela OWASP e standardizado pela **Ecma International**. A linhagem importa para a entrevista: a versão **1.6** foi a primeira ratificada como standard Ecma (**ECMA-424**), e a especificação seguiu evoluindo — a versão **1.7** foi publicada em outubro de 2025, com a edição Ecma-424 correspondente. O foco do CycloneDX é **segurança e supply chain**: ele modela com precisão componentes, dependências, vulnerabilidades, serviços e até ativos criptográficos. Suporta os formatos **JSON, XML e Protocol Buffers**. No mundo Java, é gerado pelos plugins `cyclonedx-maven-plugin` e `cyclonedx-gradle-plugin`, que leem o grafo de dependências resolvido pelo build.

O fato de ser um **standard Ecma** não é detalhe burocrático: significa que o formato tem um processo de governança e versionamento estável, e que ferramentas de fornecedores diferentes podem gerar e consumir o mesmo SBOM com a garantia de interoperar. Para um SBOM, interoperabilidade é tudo — não adianta o seu build gerar um inventário que a plataforma de monitoramento do cliente não sabe ler. Por isso você fixa explicitamente o `schemaVersion` no plugin (ex.: `1.6`): assim o documento gerado tem um contrato de schema conhecido, e quem consome sabe exatamente como interpretá-lo.

**SPDX** (_Software Package Data Exchange_), mantido pela Linux Foundation e padronizado como ISO/IEC 5962, nasceu com foco em **licença e compliance** — mapear quem pode usar o quê, sob quais termos. Ele também descreve componentes, mas seu DNA é o jurídico/licenciamento, enquanto o do CycloneDX é o de segurança operacional.

Os dois não são rivais excludentes; um time pode emitir ambos a partir do mesmo build, e a maioria das ferramentas converte de um para o outro. O ponto que importa em entrevista é entender que **formato de SBOM é uma escolha de propósito**, não de gosto: a área jurídica que precisa auditar licenças de tudo que embarca tem um problema diferente da equipe de segurança que precisa reagir a uma CVE — e cada formato foi otimizado para um desses problemas. Saber recitar "existe CycloneDX e SPDX" é trivial; saber **por que** os dois coexistem é o que demonstra profundidade.

> [!tip] Regra de bolso
> Pergunta "qual a licença de tudo que embarco?" → SPDX brilha. Pergunta "quais componentes têm CVE aberta?" → CycloneDX foi desenhado para isso. Na prática, ferramentas modernas exportam ambos, mas saber **por que cada um existe** é o que pega na entrevista.

### SCA e dependency-check

SBOM responde "o quê eu embarco". A pergunta seguinte é "**alguma dessas coisas é vulnerável?**", e isso é trabalho de **SCA** (_Software Composition Analysis_).

**OWASP Dependency-Check** é uma ferramenta SCA _flagship_ da OWASP que detecta vulnerabilidades publicamente divulgadas nas dependências de um projeto. O mecanismo: para cada dependência, ela tenta determinar um identificador **CPE** (_Common Platform Enumeration_) e, quando encontra, lista as **CVEs** associadas. A base principal é o **NVD** (_National Vulnerability Database_) do NIST, da qual ela se atualiza automaticamente via _data feeds_; também cruza fontes adicionais como OSS Index, RetireJS, NPM Audit e Bundler Audit. Ela roda como CLI, como plugin de build (Maven/Gradle/Ant) ou em CI/CD, e tipicamente **falha o build** acima de um limiar de severidade configurado.

A diferença mental entre SBOM e SCA: o SBOM é um **substantivo** (um documento, um inventário que você guarda e versiona); o SCA é um **verbo** (a ação de cruzar esse inventário contra bases de CVE, repetida a cada novo dia, porque a base muda mesmo que o seu código não mude).

Há uma sutileza de pipeline que cai em entrevista: o SCA deve rodar em **dois momentos diferentes**. No _pull request_, ele é um **gate** — barra a entrada de uma dependência com CVE conhecida antes do merge. Mas isso não basta, porque uma dependência aprovada hoje pode ter uma CVE divulgada amanhã, sem que uma linha do seu código mude. Por isso o SCA também roda **agendado** (tipicamente noturno) contra o que já está em produção, re-cruzando o inventário existente com a base de CVE atualizada. Quem só roda no PR tem a falsa sensação de cobertura; o risco mora justamente nas dependências antigas que ninguém toca.

### SLSA e proveniência

SBOM e SCA olham para **o que** entrou no artefato. **SLSA** (_Supply-chain Levels for Software Artifacts_, pronuncia-se "salsa") olha para **como o artefato foi produzido** — a integridade do próprio build.

SLSA é um framework de _checklist_ de controles para prevenir adulteração e garantir integridade da cadeia, organizado em **níveis de assurance crescente** (do nível 1 ao 3, com tiers superiores endereçando ameaças mais sofisticadas). O conceito central é a **proveniência** (_provenance_): um registro verificável e assinado — uma **attestation** — de _quem_ buildou o artefato, _a partir de qual fonte_, _em qual plataforma de build_ e _com quais parâmetros_. A documentação oficial é explícita: "o primeiro on-ramp para SLSA é gerar proveniência".

Note a mudança de perspectiva que SLSA introduz. SBOM e SCA são instrumentos voltados a **você, o produtor**, entendendo o que produz. SLSA acrescenta uma dimensão voltada ao **consumidor** do artefato: alguém que recebe o seu JAR ou a sua imagem e quer verificar, sem confiar cegamente em você, que aquilo foi mesmo buildado pelo pipeline que você diz. Essa inversão — provar para terceiros, de forma criptograficamente verificável, em vez de pedir que confiem — é o que distingue um framework de integridade de cadeia de um mero relatório interno. É também por isso que as assinaturas e attestations não podem ser geradas pela mesma mão que escreve o código: nos níveis altos, a plataforma de build precisa ser a fonte da verdade.

Por que isso é uma camada distinta: um atacante que comprometa o seu **pipeline de build** pode injetar código malicioso _depois_ de o SBOM e o SCA terem aprovado o código-fonte — foi o vetor do incidente SolarWinds. A proveniência SLSA permite que o **consumidor** do artefato verifique que ele saiu de um build confiável e não foi adulterado no caminho.

A progressão de níveis dá a intuição do esforço crescente: nos níveis iniciais, basta o pipeline **gerar e disponibilizar a proveniência** do build de forma automatizada; nos níveis mais altos, exige-se que essa proveniência seja gerada por uma **plataforma de build isolada e endurecida**, de modo que nem mesmo quem submete o código consiga forjar a attestation. A ideia operacional é simples: subir de nível significa mover a confiança de "o desenvolvedor afirma" para "a plataforma prova, e nem o desenvolvedor consegue mentir".

O caso `xz/liblzma` (CVE-2024-3094, descoberto em 2024) é o exemplo didático perfeito de por que essa camada existe. Um mantenedor malicioso, ao longo de meses, ganhou confiança no projeto e plantou um backdoor **não no código-fonte do repositório**, mas nos artefatos de _release_ — o tarball distribuído continha um payload que não estava visível no Git. Um SBOM teria listado a versão; um scanner de CVE não teria nada para apontar (a CVE só existiu após a descoberta). O que cobre esse vetor é justamente a proveniência: a capacidade de verificar que o artefato distribuído corresponde, bit a bit, ao que o build produziu a partir da fonte auditável — e que não houve um passo manual e opaco no meio.

As três peças se encaixam assim — o **SBOM** diz _o que_ tem dentro, o **SCA** diz _o que está vulnerável_, e o **SLSA** diz _que o que está dentro é realmente o que foi buildado a partir da fonte confiável_.

### Onde o SBOM é consumido

Gerar o SBOM é metade do ciclo; o valor só se materializa quando ele é **ingerido por algo que monitora**. O fluxo maduro tem três destinos para o `bom.json` gerado no build:

- **Arquivamento versionado**: o SBOM vira um artefato de release, armazenado junto ao JAR/imagem e carimbado com a mesma versão. É a "memória" que você consulta quando uma CVE futura aparece.
- **Plataforma de monitoramento contínuo**: ferramentas de _SBOM management_ (como o OWASP Dependency-Track, projeto irmão do Dependency-Check) ingerem o SBOM e re-avaliam os componentes contra novas CVEs ao longo do tempo, gerando alerta quando uma vulnerabilidade nova atinge um componente que você já tinha em produção. É aqui que o ciclo se fecha.
- **Verificação na admissão**: em ambientes mais maduros, o orquestrador (ex.: um _admission controller_ em Kubernetes) pode recusar imagens sem SBOM válido ou sem proveniência SLSA assinada, fechando a porta no momento do deploy.

A diferença entre "ter SBOM" e "ter um programa de supply chain" está justamente no segundo destino: o **loop contínuo** de ingestão e re-avaliação. Sem ele, o SBOM é só um arquivo morto. Vale frisar o ponto temporal que une os três destinos: uma vulnerabilidade não nasce com o seu código — ela é **descoberta** dias, meses ou anos depois de você ter buildado. Um programa de supply chain é, no fundo, a infraestrutura que garante que essa descoberta futura encontre o seu inventário passado e dispare um alerta, em vez de te pegar de surpresa quando a notícia chegar pelo Twitter.

> [!warning] CVE scanning sozinho NÃO basta
> Cruzar dependências contra bases de CVE é necessário, mas tem um ponto cego estrutural: **só pega o que já tem CVE atribuída**. Não pega:
> - **Typosquatting** — pacote `reqeusts` (com o erro de digitação) imitando `requests`; é um pacote _novo_ e malicioso, sem CVE.
> - **Dependency confusion** — atacante publica em um repositório público um pacote com o **mesmo nome** de um pacote interno seu, e o resolver baixa o do atacante por ter versão "maior".
> - **Backdoor recém-plantado** — comprometimento de uma lib legítima (vide o caso `xz/liblzma` de 2024): entre o plantio e a divulgação, **não há CVE para o scanner cruzar**.
> É por isso que o SBOM (saber exatamente o que você tem) e a proveniência (saber de onde veio) cobrem o que o scan de CVE não alcança.

## Na prática

Gerar um SBOM CycloneDX agregado de um projeto Maven multi-módulo, configurando o plugin no POM:

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.cyclonedx</groupId>
      <artifactId>cyclonedx-maven-plugin</artifactId>
      <version>2.9.1</version>
      <executions>
        <execution>
          <id>gerar-sbom</id>
          <phase>package</phase>
          <goals>
            <!-- agrega todos os módulos num único BOM -->
            <goal>makeAggregateBom</goal>
          </goals>
        </execution>
      </executions>
      <configuration>
        <!-- versão da especificação CycloneDX -->
        <schemaVersion>1.6</schemaVersion>
        <outputFormat>json</outputFormat>
        <outputName>bom</outputName>
      </configuration>
    </plugin>
  </plugins>
</build>
```

Com o plugin configurado, o build passa a emitir `target/bom.json` na fase `package`. Você também pode invocar o goal diretamente, sem ligá-lo ao lifecycle:

```bash
# gera o SBOM agregado sem precisar declarar a execution no POM
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom

# roda o SCA: cruza as dependências contra o NVD e falha o build
# acima do limiar de severidade (escala CVSS 0-10)
mvn org.owasp:dependency-check-maven:check -Dformat=ALL -DfailBuildOnCVSS=7

# em CI, o SBOM gerado vira artefato versionado e arquivado:
cp target/bom.json artefatos-release/sbom-$(date +%F).json
```

No Gradle, o equivalente é aplicar o plugin `org.cyclonedx.bom` e rodar a task `cyclonedxBom`; o SCA usa o plugin `org.owasp.dependencycheck` com a task `dependencyCheckAnalyze`. A ideia operacional é a mesma: **o SBOM é um output de release** (arquivado junto com o artefato, com o mesmo número de versão), e o **SCA é um gate de pipeline** (roda toda noite, não só no release, porque CVEs novas aparecem para código que não mudou).

O conteúdo gerado é um documento estruturado. Um trecho de um SBOM CycloneDX em JSON tem a forma abaixo — cada componente carrega coordenadas, versão e um **PURL** (_package URL_), o identificador canônico que ferramentas de consumo usam para cruzar contra bases de vulnerabilidade:

```bash
# inspecionar quais componentes o SBOM lista (requer jq instalado)
jq '.components[] | {nome: .name, versao: .version, purl: .purl}' target/bom.json

# exemplo de saída para uma dependência:
# {
#   "nome": "log4j-core",
#   "versao": "2.17.1",
#   "purl": "pkg:maven/org.apache.logging.log4j/log4j-core@2.17.1"
# }
```

É exatamente essa estrutura que torna o SBOM consultável em escala: filtrar por `purl` em todos os BOMs arquivados responde, em segundos, qual serviço embarca qual versão de qualquer componente.

Uma decisão prática que sempre aparece é **qual limiar usa para falhar o build**. O `-DfailBuildOnCVSS` recebe um valor na escala CVSS (de 0 a 10); usar `7` significa quebrar o pipeline diante de qualquer vulnerabilidade de severidade alta ou crítica. O cuidado de engenharia aqui é o **balanço entre rigor e ruído**: um limiar baixo demais transforma o gate em uma fábrica de falsos positivos que o time aprende a ignorar (e ignorar um gate é pior do que não ter gate); um limiar alto demais deixa passar risco real. Some-se a isso o problema dos **falsos positivos legítimos** — uma CVE que existe na lib mas não no caminho de código que você usa. A resposta madura não é desligar o scanner: é manter um arquivo de **supressões versionado e justificado** (cada supressão com link para a análise que provou que não se aplica), de modo que a decisão de ignorar uma CVE seja auditável e revisada, não silenciosa.

> [!tip] Onde isso encaixa no pipeline
> Pense em três pontos de inserção distintos no ciclo de build/release:
>
> 1. **No PR** — o SCA roda como gate, barrando dependência com CVE conhecida antes do merge.
> 2. **No release** — o `cyclonedx-maven-plugin` gera o SBOM na fase `package`, e ele é arquivado junto ao artefato com a mesma versão.
> 3. **Agendado** — o SCA (ou a plataforma de monitoramento que ingeriu o SBOM) re-avalia o que já está em produção contra a base de CVE atualizada, todo dia.
>
> Cada ponto cobre uma janela de tempo diferente. Quem só tem o ponto 1 está cego para a CVE que aparece depois do merge.

## Armadilhas

### (1) SBOM gerado e nunca consumido — teatro de compliance

O anti-padrão mais comum. O time pluga o `cyclonedx-maven-plugin`, marca "geramos SBOM" no checklist de auditoria, e o `bom.json` vai para uma pasta que ninguém abre. Um SBOM que não é **consumido** — ingerido em uma ferramenta que monitora os componentes contra CVEs novas ao longo do tempo — não responde à pergunta que justifica existir ("a CVE de hoje me afeta?"). Gerar é trivial; o valor está no **loop de consumo contínuo**. SBOM arquivado e esquecido é segurança de fachada.

### (2) Achar que o CVE scan cobre typosquatting e dependency confusion

Confiar que "rodamos Dependency-Check no CI, estamos cobertos" ignora o ponto cego estrutural do SCA: ele só enxerga vulnerabilidades **com CVE atribuída**. Ataques de supply chain modernos — typosquatting, dependency confusion, backdoor plantado em pacote legítimo antes da divulgação — operam exatamente na **janela sem CVE**. O scan é uma camada necessária, não suficiente. Defesa real combina SCA com controle de origem (repositórios privados/proxy, _allowlist_ de namespaces, verificação de assinatura/proveniência via SLSA).

### (3) Confundir SBOM (inventário) com reprodutibilidade (determinismo)

São eixos ortogonais e complementares, e misturá-los denuncia entendimento raso. O **SBOM** responde **"o quê"** o artefato contém — é um inventário descritivo. A **reprodutibilidade** (tema da nota de [[03-Dominios/Tecnologia/Java/Build e tooling/17 - Reprodutibilidade e reproducible builds|reprodutibilidade]]) responde **"como"** o artefato foi produzido em termos de **determinismo**: rodar o mesmo build duas vezes gera bytes idênticos. Um SBOM pode listar perfeitamente seus componentes mesmo que o build não seja reprodutível; e um build pode ser bit-a-bit reprodutível sem que ninguém tenha gerado um SBOM. Juntos eles se reforçam — um build reprodutível torna a proveniência verificável, e o SBOM torna o conteúdo auditável — mas resolvem problemas diferentes.

### (4) Tratar o gate de CVE como ruído e suprimir tudo

Decorrência das anteriores, mas vale isolar: o caminho mais comum para um programa de supply chain morrer não é técnico, é cultural. O scanner começa apontando uma vulnerabilidade real, o time não tem tempo de tratar, suprime "temporariamente", e a supressão temporária vira permanente. Multiplicado por dezenas de findings, o arquivo de supressões cresce sem justificativa e o gate passa a sempre verde — segurança de aparência. A disciplina que separa um programa vivo de um morto é tornar **cada supressão um item auditável**, com prazo de revisão e justificativa rastreável, em vez de um botão de silenciar.

## Em entrevista

### Frase pronta (inglês)

> After Log4Shell, supply chain security stopped being optional. The first thing I push for is an **SBOM** — a CycloneDX inventory generated by the build itself, so we know exactly which components and versions we ship. But an SBOM is only the "what": we feed it into an **SCA** tool like OWASP Dependency-Check to cross-reference dependencies against CVE databases, and we treat **SLSA provenance** as a separate layer that proves *how* the artifact was built. I'm always explicit that CVE scanning alone doesn't catch typosquatting or dependency confusion, because those have no CVE yet — and that an SBOM is an inventory, not the same thing as a reproducible build.

### Pergunta-armadilha esperada

Uma pergunta de acompanhamento comum é _"se você já roda um scanner de CVE no CI, por que precisa de SBOM?"_. A resposta sênior separa os dois eixos: o scanner responde **hoje** se você tem uma vulnerabilidade **conhecida hoje**; o SBOM é o **registro histórico** que permite responder, no futuro, sobre uma CVE que **ainda não existe** no momento do build. Quando a próxima Log4Shell aparecer, você não vai re-buildar artefatos antigos para descobrir o que eles contêm — vai consultar os SBOMs que arquivou. Scanner é tempo presente; SBOM é a memória que você vai precisar no tempo futuro.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| Inventário de componentes (SBOM) | Software Bill of Materials (SBOM) |
| Cadeia de suprimentos de software | Software supply chain |
| Análise de composição de software | Software Composition Analysis (SCA) |
| Proveniência / atestação | Provenance / attestation |
| Vulnerabilidade divulgada (CVE) | Disclosed vulnerability (CVE) |
| Confusão de dependências | Dependency confusion |
| Digitação enganosa (typosquatting) | Typosquatting |
| Integridade da cadeia de build | Build chain integrity |

## Veja também

- [[03-Dominios/Tecnologia/Java/Build e tooling/17 - Reprodutibilidade e reproducible builds|Reprodutibilidade]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/19 - Publicação de artefatos|Publicação de artefatos]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão|Resolução de dependências]]
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- [CycloneDX — Specification Overview](https://cyclonedx.org/specification/overview/) — formato SBOM da OWASP, standard Ecma International (ECMA-424); versão 1.6 ratificada como standard, 1.7 publicada em out/2025; formatos JSON, XML e Protocol Buffers.
- [SLSA — Supply-chain Levels for Software Artifacts](https://slsa.dev/) — framework de integridade de build em níveis (L1-L3); proveniência como primeiro on-ramp.
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/) — ferramenta SCA flagship da OWASP; cruza dependências contra o NVD/NIST via CPE → CVE.
- [SPDX — Software Package Data Exchange](https://spdx.dev/) — formato alternativo de SBOM (Linux Foundation, ISO/IEC 5962), foco em licença/compliance.
