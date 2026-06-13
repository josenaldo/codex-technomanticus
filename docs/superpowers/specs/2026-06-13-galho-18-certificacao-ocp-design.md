# Galho 18 — Certificação Java OCP — Design / Spec

- **Data:** 2026-06-13
- **Trilha:** Java Senior (último galho — fecha a trilha de 18 galhos)
- **Pasta destino:** `03-Dominios/Java/Certificação OCP/`
- **Branch:** `main` (autorização durável — galhos Java direto na main desde o Galho 6)

---

## 1. Tese do galho

Este é o **último galho** da trilha e é **atípico**: não é uma trilha conceitual nova, é um **guia da prova OCP** que mapeia para os galhos já existentes (principalmente 1-4 de linguagem, mais Collections/Streams, Concorrência, I/O, JVM/módulos). Decisão de roadmap (2026-06-02): *"OCP é o último galho — mapeia pros galhos 1-4, não re-explica linguagem."*

O valor **não** é re-ensinar `switch`/generics/streams — é o **ângulo de certificação**: o que a Oracle cobra, como as questões mentem, e onde o candidato senior tropeça por excesso de confiança. Toda a mecânica de linguagem vive nos galhos 1-4 — este galho **referencia, nunca duplica** (fronteira-assinatura).

---

## 2. Decisões cravadas no brainstorm (2026-06-13)

1. **Versão da prova:** **ambas como cidadãs de 1ª classe** — Java SE 21 (1Z0-830) e Java SE 25 (1Z0-831). Os 10 domínios oficiais são quase idênticos (só a redação muda); o mapeamento objetivo→galho serve as duas. Uma nota dedicada compara as versões.
2. **Espinha estrutural:** **híbrido por objetivo oficial** — a espinha é o syllabus da Oracle; cada nota de domínio mapeia para as notas exatas dos galhos.
3. **Agrupamento do MOC:** **grupos de certificação** (não as 3 fases canônicas): *Sobre a prova* → *Os domínios do exame* → *Pegadinhas, estratégia e dia da prova*. O campo `fase:` do frontmatter é **repurposado** para o slug do grupo (`sobre-a-prova` / `dominios` / `estrategia`), preservando o dataview do MOC.
4. **Amplitude:** **17 notas de conteúdo** — 4 *Sobre a prova* + 10 *domínio* (1:1 com o syllabus oficial) + 3 *Estratégia*.
5. **Tronco legado** `Core/Certificação Java OCP.md`: **colher e podar para hub** (padrão da trilha, como Java Fundamentals/Spring Boot). Migrar o conteúdo bom para as notas atômicas, depois podar o tronco a um stub-hub que redireciona ao galho 18. Mantém `publish: false`.
6. **Não-fabricação (voz de plano):** o tronco legado afirma em 1ª pessoa que o usuário **fez** a OCP (15 mocks, caderno de 30 páginas, *"I pursued the OCP certification"*). O usuário **ainda não fez — é um objetivo em preparação.** Reescrever tudo isso em **voz de plano** (futuro/presente: *"meu plano é…"*, *"estou me preparando para…"*), **nunca afirmando a prova já feita nem a credencial já obtida**. O conteúdo em inglês ("Em entrevista"/"How to explain") vira roteiro honesto de quem se prepara — demonstra o conhecimento, não reivindica o certificado.

---

## 3. Fatos cravados da pesquisa (usar; não inventar)

**Fontes oficiais (existência confirmada; páginas Oracle bloqueadas por JS, dados detalhados via Enthuware/busca — marcar como secundário onde aplicável):**

- 1Z0-830 (Java SE 21): `https://education.oracle.com/java-se-21-developer-professional/pexam_1Z0-830`
- 1Z0-831 (Java SE 25): `https://education.oracle.com/java-se-25-developer-professional/pexam_1Z0-831`
- Enthuware syllabus 21: `https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus`
- Enthuware syllabus 25: `https://enthuware.com/oca-ocp-java-certification-resources/297-ocp-java-25-exam-syllabus`

**Fatos:**
- **1Z0-831 (Java SE 25) lançado em 01/mai/2026.** Coexiste com o 1Z0-830 — a Oracle **não** anunciou aposentadoria do 830 nem data de retirement (afirmar só isso; não inferir coexistência permanente).
- Ambas as provas têm **10 seções oficiais de objetivos** (não 12 — o tronco legado inflou/desatualizou).
- Formato (fonte secundária; páginas Oracle não lidas diretamente): **50 questões, nota de corte ~68%**, múltipla escolha (single + multi-answer, "Select two/three", sem crédito parcial). Preço **USD 245** ("may vary by region").
- **Duração: dado contraditório (90 vs 120 min) — NÃO cravar um número único.** Registrar como "verificar na página oficial; fontes secundárias divergem (90–120 min)". Honestidade > falso preciso.
- **OCA morta desde Java 11** — prova OCP única (1Z0-815+816 → consolidados no 1Z0-819 em ago/2020 → 1Z0-829 → 1Z0-830 → 1Z0-831). Sem pré-requisito OCA. (Java 8 ainda exigia OCA 1Z0-808 antes do OCP 1Z0-809.)
- **Registro:** múltiplas fontes indicam que o 1Z0-830 **não é mais administrado pela Pearson VUE** — agendamento via `oracle.com/education`, online proctored. Marcar como **fonte secundária / verificar**.
- **Livro Sybex:** *OCP Oracle Certified Professional Java SE 21 Developer Study Guide: Exam 1Z0-830*, **Jeanne Boyarsky & Scott Selikoff** (Sybex/Wiley, 2024), ISBN-13 **9781394286614**. **Só existe para o 1Z0-830 (Java 21)** — ainda não há edição Java 25.
- **ZERO estatística de aprovação.** Nenhuma fonte oficial dá taxa de aprovação; não inventar.

**Títulos oficiais dos 10 domínios** (mostrar os dois no callout de cada nota de domínio):

| # | 1Z0-830 (Java 21) | 1Z0-831 (Java 25) |
|---|---|---|
| 1 | Handling Date, Time, Text, Numeric and Boolean Values | Handling Date, Time, Text, Numeric and Boolean Values |
| 2 | Controlling Program Flow | Implementing Program Flow Control Using Decision and Looping Constructs |
| 3 | Using Object-Oriented Concepts in Java | Applying Object-Oriented Principles in Java Programs |
| 4 | Handling Exceptions | Implementing Exception Handling in Java Applications |
| 5 | Working with Arrays and Collections | Using Arrays and Collections to Store and Retrieve Data |
| 6 | Working with Streams and Lambda expressions | Processing Data Using Streams and Lambda Expressions |
| 7 | Packaging and Deploying Java Code | Packaging and Deploying Java Code |
| 8 | Managing Concurrent Code Execution | Implementing Multithreading for Concurrent Code Execution |
| 9 | Using Java I/O API | Performing Input and Output Operations Using the Java I/O API |
| 10 | Implementing Localization | Developing Applications with Localization Support |

---

## 4. Mapa de notas (17 notas de conteúdo)

Pasta: `03-Dominios/Java/Certificação OCP/`. Tag do galho: **`certificacao-ocp`**.

### Grupo 1 — Sobre a prova (`fase: sobre-a-prova`)

- **01 - A certificação OCP — o que é, por que (e por que não) fazer** — valor (credencial internacional, forcing function), críticas honestas (corner cases ≠ arquitetura, custo), OCA morta, quando vale a pena.
- **02 - Qual prova mirar — Java 21 (1Z0-830) vs Java 25 (1Z0-831)** — tabela comparativa, ambas válidas, status de coexistência (sem retirement anunciado), livro Sybex só p/ 21, recomendação honesta por perfil do candidato.
- **03 - Formato, logística e mecânica da prova** — 50q, ~68%, duração (registrar divergência), multi-answer sem parcial, online proctored, registro via oracle.com, marcador de revisão, o que é proibido.
- **04 - O mapa objetivo → galho — revisar a trilha pra prova** — **NOTA-CORAÇÃO / hub de revisão.** Tabela grande cruzando os 10 domínios oficiais → notas exatas dos galhos. Sinaliza os 3 domínios com cobertura parcial. É o ponto de entrada do candidato que já fez a trilha.

### Grupo 2 — Os domínios do exame (`fase: dominios`) — 1:1 com o syllabus

Estrutura de cada nota de domínio (ver §5.2). Cobertura na trilha marcada:

- **05 - Domínio 1 — Datas, texto, números e booleanos** → G1·02, G1·04, G2·11. *Cheia.*
- **06 - Domínio 2 — Controle de fluxo** → G1·03, G1·14. *Cheia.*
- **07 - Domínio 3 — Orientação a objetos** → G1·06, 07, 08, 09, 11, 12, 13, 14. *Cheia.*
- **08 - Domínio 4 — Exceções** → G1·10. *Cheia.*
- **09 - Domínio 5 — Arrays e coleções** → G1·05, G2·01, 02, 03, 06, 14. *Cheia.*
- **10 - Domínio 6 — Streams e lambdas** → G2·04, 05, 07, 08, 09, 10, 13, 15. *Cheia.*
- **11 - Domínio 7 — Empacotamento, deployment e módulos** → G3·08 (JPMS), G6 (jlink/jpackage). ***Parcial*** — gap: `jar`/`META-INF`, `jShell`, implicit classes & instance `main` (Java 21+/25). A nota carrega esse gap de forma autocontida.
- **12 - Domínio 8 — Concorrência** → G4 (todo; destaque 02, 03, 06, 07, 08, 10, 11, 12, 15). *Cheia.*
- **13 - Domínio 9 — I/O** → G2·12 (`java.nio.file`). ***Parcial*** — gap: `java.io` (byte/char streams, Buffered*), serialização (`Serializable`/`transient`/`serialVersionUID`), `Console`. Autocontido.
- **14 - Domínio 10 — Localização** → G2·11 (`DateTimeFormatter`). ***Parcial*** — gap: `Locale`, `ResourceBundle`, `NumberFormat`. Autocontido.

### Grupo 3 — Pegadinhas, estratégia e dia da prova (`fase: estrategia`)

- **15 - O catálogo de pegadinhas clássicas** — colhido + expandido do tronco: Integer cache (-128..127), String pool vs `new String`/`intern`, `var` ambíguo, autoboxing+null→NPE, `final` com objeto mutável, override/overload com autoboxing (ordem: exact→widening→autoboxing→varargs), static hiding ≠ override, try/finally com `return`, try-with-resources (ordem reversa), `equals`/`hashCode`, view vs cópia, switch fall-through, stream one-shot, effectively final, init de arrays, enum constructor private, type erasure. Cada pegadinha linka ao domínio/galho onde a mecânica vive.
- **16 - Estratégia de estudo e recursos** — plano em **voz de plano** (não prova feita), livro Sybex, Enthuware/mocks, caderno de erros, JShell/`javap`, como usar mocks, regra "3 mocks >80% antes de marcar".
- **17 - O dia da prova e depois** — tips antes/durante, gestão de tempo (50q em 90–120min), mentalidade, após passar (CertView/Credly/LinkedIn) / após reprovar (14 dias, relatório de áreas fracas).

---

## 5. Estrutura das notas

### 5.1 Frontmatter (todas as notas de conteúdo)

```yaml
---
title: "<título sem o prefixo numérico>"
created: 2026-06-13
updated: 2026-06-13
type: concept
status: seedling
publish: true
fase: <sobre-a-prova | dominios | estrategia>
tags:
  - java
  - certificacao-ocp
  - <slug-do-grupo igual ao fase>
aliases:
  - "<alias curto 1>"
  - "<alias curto 2>"
---
```

### 5.2 Seções — notas de DOMÍNIO (grupo 2)

1. TL;DR (callout `> [!abstract]`).
2. `> [!info] Títulos oficiais` — os dois títulos (21 e 25) lado a lado.
3. `## O que a Oracle cobra` — os sub-objetivos oficiais do domínio (lista), em registro de prova.
4. `## Mapa de revisão` — tabela/lista com as **notas exatas dos galhos** (wikilinks — ver §7) que ensinam cada sub-tópico. É o coração do "revisar via trilha".
5. `## Pegadinhas deste domínio` — as armadilhas de prova específicas (linka ao [[15 - catálogo]] quando transversal).
6. `## Lacuna da trilha` *(só nos domínios parciais 7, 9, 10)* — o que o galho não cobre e o candidato precisa estudar à parte; conteúdo autocontido mínimo + fontes. **Seam de honestidade.**
7. `## Em entrevista` — leve; frase em inglês que demonstra o conhecimento do domínio (não reivindica credencial) + vocabulário PT/EN.
8. `## Veja também` — notas-irmãs do galho + galhos mapeados.
9. `## Referências` — página oficial do objetivo + docs.

### 5.3 Seções — notas de PROSA (grupos 1 e 3)

Estrutura mais discursiva (o template padrão O-que-é/Por-que/Como-funciona encaixa parcialmente). Mínimo: TL;DR → corpo em seções próprias → `## Veja também` → `## Referências`. A nota 04 (mapa) é majoritariamente tabela. A nota 15 (pegadinhas) é catálogo. Voz de plano nas notas 16/17 onde houver 1ª pessoa.

### 5.4 MOC (`index.md` do galho)

`type: moc`, `publish: true`, tags `java`/`certificacao-ocp`/`moc`, aliases incluindo "Galho 18 - Certificação OCP". TL;DR + "Sobre este galho" (a tese atípica + a fronteira-assinatura: linka galhos 1-4/G2/G3/G6, não re-explica) + os 3 grupos (Sobre a prova / Os domínios do exame / Pegadinhas, estratégia e dia da prova) + **Rotas alternativas** (Completa / Reta-final pré-prova / Só-pegadinhas / Por-domínio) + Veja também + bloco dataview (`WHERE type = "concept"`).

---

## 6. Trabalho fora das notas de conteúdo

1. **Poda do tronco legado** `03-Dominios/Java/Core/Certificação Java OCP.md`: após colher o conteúdo, reduzir a um **stub-hub** curto (mantém `publish: false`) que aponta para o galho 18 (`[[03-Dominios/Java/Certificação OCP/index|Certificação OCP (Galho 18)]]`). Não deletar (preserva ponto de entrada legado e wikilinks históricos).
2. **`index.md` central** (`03-Dominios/Java/index.md`):
   - Linha 54: trocar `18. Certificação Java OCP *(planejado)*` por wikilink ativo `[[03-Dominios/Java/Certificação OCP/index|Certificação Java OCP]] — …`.
   - Linha 61: atualizar o "(vira Galho 18)" para apontar ao galho ativo.
   - Atualizar `updated:`.
3. **Dicionário de Java** (`03-Dominios/Java/Dicionário de Java.md`, `type: glossary`, A-Z): adicionar verbetes **sem duplicar** (linkar aos existentes). Candidatos: OCP, OCA, 1Z0-830, 1Z0-831, exam objective, passing score, online proctored, voucher, Enthuware, CertView, Credly, Pearson VUE. **Antes de inserir, grep cada termo** no Dicionário; se já existir, linkar em vez de recriar. Inserção em ordem alfabética na seção da letra correta.
4. **verificar-wikilinks** na pasta do galho + index central, no fim. Validar **programaticamente** todos os wikilinks (lição recorrente dos galhos 12/16/17: subagentes alucinam títulos plausíveis-mas-errados).

---

## 7. Anti-alucinação de wikilinks — títulos EXATOS dos alvos

**Regra:** ao pedir wikilinks a subagentes, passar SEMPRE os títulos exatos abaixo. Validar com `verificar-wikilinks` + grep no fim. Formato do wikilink: `[[03-Dominios/Java/<Galho>/<arquivo sem .md>|<rótulo>]]`.

**Galho 1 — `Linguagem e sintaxe moderna/`:**
`01 - O modelo da linguagem Java` · `02 - Tipos, variáveis e operadores` · `03 - Estruturas de controle e fluxo` · `04 - Strings e text blocks` · `05 - Arrays e varargs` · `06 - Classes, objetos e encapsulamento` · `07 - Herança e polimorfismo` · `08 - Interfaces e classes abstratas` · `09 - Enums` · `10 - Exceções e tratamento de erros` · `11 - Annotations` · `12 - Generics em profundidade` · `13 - Records e record patterns` · `14 - Sealed classes e pattern matching` · `15 - A evolução do Java (8 a 25)`

**Galho 2 — `Collections e Streams/`:**
`01 - O Collections Framework` · `02 - Listas, conjuntos e filas` · `03 - Mapas` · `04 - Lambdas e interfaces funcionais` · `05 - Introdução à Stream API` · `06 - Comparable e Comparator` · `07 - Operações de Stream — intermediárias e terminais` · `08 - Collectors e agrupamento` · `09 - Streams primitivos` · `10 - Optional` · `11 - java.time — Date e Time API` · `12 - I-O moderno com java.nio.file` · `13 - Composição funcional e funções de alta ordem` · `14 - SequencedCollection e SequencedMap` · `15 - Collectors customizados e Gatherers` · `16 - Escolha de coleção e estilo funcional — síntese`

**Galho 3 — `JVM/`:**
`01 - A JVM — o que é e o pipeline de execução` · `02 - Áreas de memória de runtime` · `03 - Garbage Collection — o conceito` · `04 - Bytecode por dentro — anatomia e javap` · `05 - Classloading e o delegation model` · `06 - Os coletores do HotSpot` · `07 - JIT — C1, C2 e tiered compilation` · `08 - JPMS — o sistema de módulos` · `09 - Flags, ergonomics e a JVM em containers` · `10 - GC logs — unified logging e leitura` · `11 - Tuning de GC — metodologia e prática` · `12 - Diagnóstico — heap dumps, thread dumps e jcmd` · `13 - JFR e JMC — observabilidade de produção` · `14 - Performance da JVM — síntese`

**Galho 4 — `Concorrência e paralelismo/`:**
`01 - Concorrência e paralelismo - o modelo` · `02 - Threads e seu ciclo de vida` · `03 - Exclusão mútua com synchronized` · `04 - As armadilhas - race, deadlock e companhia` · `05 - Locks explícitos` · `06 - Atômicos e operações lock-free` · `07 - Concurrent collections` · `08 - Executors e thread pools` · `09 - Sincronizadores` · `10 - CompletableFuture e composição assíncrona` · `11 - Java Memory Model em profundidade` · `12 - Virtual Threads e Project Loom` · `13 - Structured concurrency` · `14 - Scoped values` · `15 - Parallel streams e fork-join` · `16 - Padrões e diagnóstico de concorrência`

**Galho 6 — `JavaFX/`:** para jlink/jpackage usar `13 - Empacotamento — módulos, jlink e jpackage`.

---

## 8. Regras de execução

- **Direto na main**, sem branch (autorização durável). Push manual pelo usuário — **não** fazer push/deploy sem pedido.
- **Subagent-driven:** subagentes **write-only** (criam/editam arquivos); o **controller commita nominalmente** (`git add <arquivos>` específicos — **nunca `git add -A`**; o bot do Obsidian Git roda no timer).
- **Sem Co-Authored-By Claude** nos commits.
- **Sem fabricação** de experiência/projeto/cliente. Voz de plano onde o tronco afirmava prova feita. Domínios de exemplo neutros.
- **publish: true** nas notas de conteúdo; tag de galho; MOC com rotas; expansão do Dicionário (linkar, não duplicar).
- **Pré-flight → brainstorm → spec → plano → execução com review por fase → commits granulares** (1 commit por fase coerente).
- **verificar-wikilinks** + grep programático no fim.

---

## 9. Sequência de execução (fases para o plano)

1. **Fase 0 — Scaffolding:** criar pasta + `index.md` (MOC) do galho com os 17 títulos como wikilinks (esqueleto).
2. **Fase 1 — Sobre a prova (01-04):** as 4 notas, com a 04 (mapa) usando os títulos exatos do §7.
3. **Fase 2 — Domínios cheios (05, 06, 07, 08, 09, 10, 12):** 7 notas de cobertura cheia.
4. **Fase 3 — Domínios parciais (11, 13, 14):** 3 notas com a seção "Lacuna da trilha".
5. **Fase 4 — Estratégia (15, 16, 17):** catálogo de pegadinhas + estudo + dia da prova; colher do tronco; voz de plano.
6. **Fase 5 — Integração:** podar tronco a stub-hub; atualizar index central; expandir Dicionário.
7. **Fase 6 — Validação:** `verificar-wikilinks` + grep; review final; commit de fechamento.

Cada fase: review antes de commitar. Commits granulares por fase.
