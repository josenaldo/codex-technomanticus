---
title: "Reprodutibilidade e reproducible builds"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: magus
tags:
  - java
  - build
  - magus
  - supply-chain
aliases:
  - "reproducible builds"
  - "build determinístico"
---

# Reprodutibilidade e reproducible builds

> [!abstract] TL;DR
> Um build é **reprodutível** quando a mesma entrada (código-fonte + dependências fixadas + toolchain) produz **bit-a-bit o mesmo artefato**, independentemente de quem, quando ou onde o construiu. Por padrão isso **não** acontece: jars e zips gravam timestamps nas entries, ordenam arquivos de forma não-determinística e embutem datas no `MANIFEST.MF`. Em Maven, a chave é a propriedade `project.build.outputTimestamp`, que normaliza esses timestamps e estabiliza a ordem. A partir do **Maven 4.0.0-beta-5**, o modo Reproducible Builds passa a ser **default** (MNG-8258), sem precisar tocar no `pom.xml`. A validação é feita com o `maven-artifact-plugin`: `artifact:check-buildplan` (varre plugins com problemas conhecidos) e `artifact:compare` (rebuild e diff bit-a-bit contra uma referência). Pré-requisito: versões **fixadas**, sem `LATEST`, version ranges ou SNAPSHOT.

## O que é

**Reprodutibilidade de build** (reproducible builds) é a propriedade de um processo de construção em que, dadas as mesmas entradas controladas, a saída é **idêntica byte a byte** toda vez. As entradas controladas são:

- o **código-fonte** (um commit específico, congelado);
- as **dependências** resolvidas para versões exatas e imutáveis;
- a **toolchain** (versão do JDK, do Maven, dos plugins de build).

Se dois desenvolvedores em máquinas diferentes, ou um servidor de CI em dois momentos distintos, partirem dessas mesmas entradas, o `.jar` resultante deve ter exatamente o mesmo hash (SHA-256). Não é "o mesmo programa" no sentido funcional — é o **mesmo arquivo**, com os mesmos bytes na mesma ordem.

O termo é frequentemente confundido com "build estável" ou "build que sempre passa". Não é isso. Reprodutibilidade é uma afirmação **verificável** sobre bytes, não sobre comportamento. Ela existe justamente para ser checada por terceiros que não confiam cegamente no produtor do artefato.

## Por que importa

Reprodutibilidade não é purismo de engenharia — ela sustenta três garantias práticas:

1. **Verificabilidade.** Qualquer pessoa pode reconstruir o artefato a partir da fonte pública e comparar o hash com o binário publicado. Se baterem, há prova de que o binário corresponde àquele código-fonte, e não a uma versão adulterada injetada no meio do caminho.

2. **Cache confiável.** Sistemas de build incremental e caches distribuídos (de CI a builds remotos) só podem reaproveitar artefatos com segurança se a mesma entrada garantidamente produz a mesma saída. Sem determinismo, o cache vira uma fonte de bugs sutis ("funciona na minha máquina").

3. **Auditoria de supply chain.** Ataques de cadeia de suprimentos frequentemente inserem código malicioso **entre** a fonte e o binário distribuído (no servidor de build comprometido, por exemplo). Builds reprodutíveis fecham essa janela: se o binário publicado não bate com a reconstrução independente, há um sinal de alarme objetivo. É a base técnica de iniciativas de proveniência e atestação de artefatos. Ver [[03-Dominios/Java/Build e tooling/18 - Supply chain e SBOM|Supply chain e SBOM]].

## Como funciona

### (1) Por que builds não são determinísticos por padrão

O formato `JAR` é um `ZIP`, e o `ZIP` foi projetado para arquivar arquivos do sistema — não para ser determinístico. Várias fontes de não-determinismo entram silenciosamente:

- **Timestamps nas entries.** Cada arquivo dentro do zip carrega uma data de modificação. Por padrão, é o instante em que o build rodou. Dois builds em momentos diferentes geram bytes diferentes, mesmo com fonte idêntica.
- **Ordem das entries.** A ordem em que os arquivos são adicionados ao archive pode depender da ordem em que o sistema de arquivos lista diretórios, que **não é garantida** entre máquinas ou execuções.
- **Paths absolutos e ambiente.** Caminhos completos da máquina de build, nomes de usuário ou variáveis de ambiente podem vazar para dentro de arquivos gerados.
- **Metadados no `MANIFEST.MF`.** Cabeçalhos como `Build-Jdk`, `Built-By` ou uma data de build embutida mudam de build para build.

O resultado: dois builds "iguais" produzem jars com hashes diferentes, e a verificabilidade evapora.

### (2) `project.build.outputTimestamp` e o default no Maven 4

A propriedade-chave em Maven é `project.build.outputTimestamp`. Ela define um **único timestamp fixo** que todos os plugins de empacotamento (jar, war, etc.) passam a usar para as entries dos archives, em vez do relógio do momento. Aceita dois formatos:

- **ISO 8601**, por exemplo `2026-06-11T00:00:00Z`;
- **epoch em segundos** (um inteiro), útil para amarrar ao timestamp do commit.

Definir essa propriedade:

- normaliza todos os timestamps das entries para o mesmo valor;
- ordena as entries de forma estável e reprodutível;
- neutraliza metadados variáveis no manifest.

A partir do **Maven 4.0.0-beta-5**, o modo Reproducible Builds passa a estar **ativo por default** (ver MNG-8258), **sem** necessidade de alterar o `pom.xml`. Definir a propriedade no `pom.xml` só serve para **sobrescrever** o valor herdado quando você quer um timestamp específico. No Maven 3, ao contrário, era preciso declarar a propriedade explicitamente para obter o comportamento.

Em releases, o `maven-release-plugin` (3.0.0-M1+) **atualiza automaticamente** o valor de `project.build.outputTimestamp` durante a release, no mesmo commit que sobe o número da versão. Assim, cada release fica amarrada a um timestamp determinístico, e não ao relógio de quem rodou o `release:prepare`.

### (3) Validação com o `maven-artifact-plugin`

Configurar a propriedade não é garantia — algum plugin antigo ou alguma fonte de não-determinismo pode escapar. Por isso a reprodutibilidade precisa ser **validada**, não assumida. O `maven-artifact-plugin` oferece os goals:

- **`artifact:check-buildplan`** — varre o build plan do projeto e identifica plugins com problemas **conhecidos** de reprodutibilidade (compara contra uma lista mantida pelo plugin). É uma checagem estática barata, ótima de rodar no CI.
- **`artifact:compare`** — faz o build do `package` e **compara bit-a-bit** contra um build de referência previamente publicado. É a prova empírica: ou os bytes batem, ou não batem. Para diagnosticar exatamente *onde* divergiram, ferramentas como o `diffoscope` ajudam a inspecionar as diferenças.

`check-buildplan` previne problemas conhecidos; `compare` prova reprodutibilidade de fato.

## Na prática

Declarar o timestamp fixo no `pom.xml` (necessário no Maven 3; sobrescrita opcional no Maven 4):

```xml
<project>
  <!-- ... -->
  <properties>
    <project.build.outputTimestamp>2026-06-11T00:00:00Z</project.build.outputTimestamp>
  </properties>
  <!-- ... -->
</project>
```

Validar plugins com problemas conhecidos de reprodutibilidade:

```bash
mvn artifact:check-buildplan
```

Provar a reprodutibilidade bit-a-bit, reconstruindo e comparando contra uma referência publicada:

```bash
# build inicial, instala localmente
mvn clean install

# reconstrói e compara byte a byte contra a referência
mvn clean verify artifact:compare
```

Fixar versões de dependências para que a entrada seja imutável (sem ranges abertos, sem `LATEST`):

```xml
<dependencies>
  <dependency>
    <groupId>com.exemplo</groupId>
    <artifactId>biblioteca-pagamentos</artifactId>
    <version>2.4.1</version>
  </dependency>
</dependencies>
```

## Armadilhas

### (1) Timestamps e ordem não-determinística silenciosa

O modo de falha mais traiçoeiro: você nunca configurou `project.build.outputTimestamp` (em Maven 3) e o build "funciona". Tudo passa, os testes verdes, o artefato é gerado. Mas cada build produz um hash diferente porque as entries do jar carregam o relógio do momento e a ordem do sistema de arquivos. Ninguém percebe — até alguém tentar **verificar** o binário e descobrir que é impossível. A não-reprodutibilidade é silenciosa por construção; só aparece quando você a procura. Em Maven 4 o default mitiga isso, mas projetos legados e plugins desatualizados continuam vulneráveis.

### (2) `RANGE`, `LATEST` ou `SNAPSHOT` de versão quebra a reprodutibilidade

Reprodutibilidade exige **entrada imutável**. Qualquer dependência declarada com version range (`[1.0,2.0)`), com `LATEST`/`RELEASE`, ou com sufixo `-SNAPSHOT` resolve para artefatos potencialmente **diferentes** em momentos diferentes. O build de hoje puxa a `2.3.4`; o de amanhã, a `2.3.5` recém-publicada — e o hash muda sem que uma única linha de código sua tenha mudado. Fixar versões exatas é **pré-requisito**, não opcional. Ver [[03-Dominios/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão|Resolução e pin de versões]].

### (3) Assumir que é reprodutível sem rodar `compare`

Configurar `outputTimestamp` e fixar versões aumenta muito as chances de reprodutibilidade, mas **não prova nada**. Um plugin de geração de código que embute um path absoluto, um recurso que serializa um `HashMap` em ordem aleatória, ou uma dependência que não respeita o timestamp — qualquer um quebra o determinismo de formas que `check-buildplan` (que só conhece problemas *catalogados*) pode não pegar. A única prova é o `artifact:compare`: reconstruir e bater byte a byte. "Configurei, logo é reprodutível" é uma afirmação não verificada — e reprodutibilidade é, por definição, sobre verificação.

## Em entrevista

### Frase pronta (inglês)

A reproducible build means that the same inputs — source code, pinned dependencies, and toolchain — always produce a byte-for-byte identical artifact. By default JVM builds are not reproducible, because JAR entries embed build timestamps, file ordering is non-deterministic, and the manifest carries build-time metadata. In Maven, the key is the `project.build.outputTimestamp` property, which normalizes those timestamps and stabilizes ordering; starting with Maven 4 this mode is enabled by default. I always pin exact dependency versions as a prerequisite and validate with the `maven-artifact-plugin` — `check-buildplan` to catch known problematic plugins, and `compare` to prove byte-for-byte reproducibility against a reference build. This matters most for supply chain auditing: anyone can independently rebuild from source and confirm the published binary wasn't tampered with.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| build reprodutível | reproducible build |
| build determinístico | deterministic build |
| bit-a-bit / byte a byte | byte-for-byte / bit-for-bit |
| fixar versão (de dependência) | pin (dependency) version |
| version range aberto | open version range |
| cadeia de suprimentos | supply chain |
| toolchain | toolchain |
| verificabilidade | verifiability |

## Veja também

- [[03-Dominios/Java/Build e tooling/10 - Resolução de dependências e conflitos de versão|Resolução e pin de versões]]
- [[03-Dominios/Java/Build e tooling/18 - Supply chain e SBOM|Supply chain e SBOM]]
- [[03-Dominios/Java/Build e tooling/04 - Maven — plugins, profiles e o wrapper|Maven — profiles e reprodutibilidade]]
- [[03-Dominios/Java/Build e tooling/index|Build, tooling e ecossistema (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Apache Maven — Guide to Configuring for Reproducible Builds: https://maven.apache.org/guides/mini/guide-reproducible-builds.html
- Apache Maven Artifact Plugin (goals `check-buildplan` e `compare`): https://maven.apache.org/plugins/maven-artifact-plugin/
- MNG-8258 — Reproducible Builds mode active by default (Maven 4.0.0-beta-5): https://issues.apache.org/jira/browse/MNG-8258
- Reproducible Builds (projeto): https://reproducible-builds.org/
- diffoscope — in-depth comparison of build outputs: https://diffoscope.org/
