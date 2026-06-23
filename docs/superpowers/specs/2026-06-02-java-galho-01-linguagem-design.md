---
title: "Spec — Galho 1 da trilha Java Senior (Linguagem e sintaxe moderna)"
date: 2026-06-02
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 1 da trilha Java Senior (Linguagem e sintaxe moderna)

## 1. Contexto e motivação

Este é o **primeiro galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda.

O galho refatora a **espinha de linguagem** do tronco `03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md` (1660 linhas, `publish: false`, `status: evergreen`). O tronco é abrangente mas saturado: cobre desde sintaxe básica até features Java 25, misturando JVM, Collections, Streams e Concorrência — temas que pertencem a outros galhos (3, 2, 2, 4 respectivamente).

Este galho extrai e faz **florescer** apenas a camada de linguagem: tipos, controle de fluxo, OOP, e o conjunto de features modernas que definem o Java atual (records, sealed classes, pattern matching, switch expressions). É a fundação didática de toda a trilha.

**Atenção à fabricação:** o tronco tem uma seção `## Na prática (da minha experiência)` (linha ~1614). Nenhuma nota nova pode herdar atribuição de experiência pessoal — exemplos são neutros ou hipotéticos explícitos (ver §4.3). A poda do tronco (§6) higieniza essa seção.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **15 notas atômicas + 1 MOC do galho + criação e semeadura do Dicionário de Java**, em `03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/` e `03-Dominios/Tecnologia/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (5 Iniciado + 6 Adepto + 4 Magus).

A trilha precisa ser:

- **Pedagógica** — o leitor sai da nota 01 entendendo o modelo da linguagem; das notas Adepto, dominando OOP idiomático; das notas Magus, fluente em records/sealed/pattern matching ao nível de explicar trade-offs em entrevista.
- **Honesta** — code samples compiláveis, comparações justas, versões hedged.
- **Atômica** — cada nota cobre um tópico bem-delimitado; cross-references ricos via wikilinks e Dicionário.
- **Senior-oriented** — a barra é "decidir, justificar, reconhecer patterns e armadilhas em code review", não "implementar from scratch".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/`)

Pasta nova, flat. 15 notas + 1 MOC. Numeração global por galho (não reinicia por fase).

#### Iniciado (5 notas — modelo mental + sintaxe pra começar)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | O modelo da linguagem Java | OO, tipagem estática/forte, compilação pra bytecode, WORA/JVM, edições (SE), ciclo de releases e LTS (6 meses, LTS a cada 2 anos), JDK vs JRE. Ponto de entrada da trilha. |
| 02 | Tipos, variáveis e operadores | Primitivos, wrappers e autoboxing, casting/promoção numérica, `var` (inferência local), escopo, igualdade (`==` vs `equals`), contrato `equals`/`hashCode` (introdução). |
| 03 | Estruturas de controle e fluxo | `if`, `switch` statement vs **switch expression** (`->`, `yield`), loops (`for`, enhanced for, `while`), `break`/`continue`/labels. |
| 04 | Strings e text blocks | Imutabilidade, String pool/`intern`, `StringBuilder`, `String.format`/`formatted`, **text blocks** (Java 15+), métodos modernos (`strip`, `repeat`, `lines`). |
| 05 | Arrays e varargs | Declaração, multidimensional, `Arrays`/`System.arraycopy`, varargs e armadilhas, arrays vs `List`. |

#### Adepto (6 notas — OOP idiomático + mecanismos da linguagem)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 06 | Classes, objetos e encapsulamento | Construtores, `this`, membros estáticos vs instância, modificadores de acesso, encapsulamento, imutabilidade de objetos. |
| 07 | Herança e polimorfismo | `extends`, `super`, **overriding vs overloading**, polimorfismo dinâmico, `final`, covariância de retorno, `Object` (`equals`/`hashCode`/`toString`). |
| 08 | Interfaces e classes abstratas | Interfaces (default/static/private methods), classes abstratas, quando cada uma, herança múltipla de tipo, diamante. |
| 09 | Enums | Enums com estado e comportamento, construtores, métodos abstratos por constante, `EnumMap`/`EnumSet`, enums vs sealed (gancho pro Magus). |
| 10 | Exceções e tratamento de erros | Hierarquia (`Throwable`), **checked vs unchecked** (o debate), `try`/`catch`/`finally`, **try-with-resources**, custom exceptions, anti-patterns (swallow, catch genérico), exceções em lambdas. |
| 11 | Annotations | Built-in (`@Override`, `@Deprecated`, `@FunctionalInterface`, `@SuppressWarnings`), meta-annotations (`@Retention`, `@Target`), annotations customizadas, processamento (visão geral), papel no Spring/Jakarta (gancho). |

#### Magus (4 notas — features modernas e maestria)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 12 | Generics em profundidade | Type parameters, bounded types, **wildcards e PECS** (Producer-Extends, Consumer-Super), **type erasure** e suas consequências, generics + arrays, métodos genéricos, armadilhas. |
| 13 | Records e record patterns | Declaração, **compact constructor** e validação, métodos adicionais, records + interfaces, **record patterns** (Java 21), records imutáveis, quando usar (DTO/value objects), records em Spring. |
| 14 | Sealed classes e pattern matching | Sealed classes/interfaces (`permits`), **pattern matching** (`instanceof` Java 16, **switch patterns** Java 21, **record patterns**, **guards** `when`), exaustividade (sealed + switch sem `default`), primitive patterns (Java 23+ preview). Dono do conceito "exaustividade". |
| 15 | A evolução do Java (8 → 25) | Mapa das features por versão e LTS, o que importa pra senior, distinção LTS vs feature releases, **preview features** e como ativá-las, migração entre versões. Nota panorâmica/cheatsheet de fechamento. |

**Decisões de fronteira (escopo NÃO coberto aqui):**
- **JVM** (memory, GC, JIT, classloader, módulos) → Galho 3. A nota 01 menciona JVM/bytecode no nível "modelo mental", sem deep dive.
- **Collections, Streams, lambdas, `Optional`, Date/Time, I/O** → Galho 2. Lambdas aparecem só como sintaxe necessária pra interfaces funcionais em annotations/generics, linkando pro Galho 2.
- **Concorrência / Virtual Threads** → Galho 4. A nota 01 e a 15 citam Virtual Threads como marco, sem aprofundar.

### 3.2. MOC do galho

`03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "Linguagem e sintaxe moderna"`, tags `java/linguagem/moc`, aliases `["Linguagem Java", "Galho 1"]`)
- TL;DR callout (galho cobre a camada de linguagem do Java moderno, da sintaxe a records/sealed/pattern matching)
- "Sobre este galho" + audiência primária/secundária
- Conteúdo agrupado em 3 H3 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 15 notas
- **Rotas alternativas (4-5):**
  - **Completa** — 01 → 15 em ordem
  - **Entrevista internacional** — 01 → 07 → 10 → 12 → 13 → 14 (foco em explicar OOP/features modernas em inglês)
  - **Features modernas (Java recente)** — 03 → 04 → 13 → 14 → 15 (records/sealed/patterns/switch)
  - **Revisão pré-OCP** — 02 → 05 → 07 → 08 → 10 → 12 (tópicos cobrados na prova; gancho pro Galho 18)
  - **Fundamentos OOP** — 06 → 07 → 08 → 09 (quem precisa firmar orientação a objetos)
- "Veja também": tronco `[[Java Fundamentals]]`, MOC central, Galho 2 (Collections/Streams), Galho 3 (JVM), Galho 4 (Concorrência), Dicionário de Java, Helsinki MOOC (referência iniciante)
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (criação + semeadura)

`03-Dominios/Tecnologia/Java/Dicionário de Java.md` — **criado neste galho**, `type: glossary`, no padrão dos outros domínios (estrutura com seções alfabéticas, frontmatter `type: glossary`, `publish: true`). Semeado com os verbetes da camada de linguagem (~30-35), em ordem alfabética case-insensitive (sem acento na ordenação). Exemplos de verbetes:

`autoboxing`, `bytecode`, `checked exception`, `compact constructor`, `default method`, `enhanced for`, `enum`, `exhaustiveness`, `generics`, `guard (pattern)`, `immutability`, `inferência de tipo (var)`, `LTS`, `overloading`, `overriding`, `pattern matching`, `PECS`, `polimorfismo`, `preview feature`, `record`, `record pattern`, `sealed class`, `String pool`, `switch expression`, `text block`, `try-with-resources`, `type erasure`, `unchecked exception`, `varargs`, `wildcard`, `WORA`, `yield`.

Cada verbete: definição curta (1-3 linhas) + `Veja também:` apontando pra nota canônica do galho. Verbetes serão expandidos por galhos futuros.

### 3.4. MOC central reescrito

`03-Dominios/Tecnologia/Java/index.md` reescrito no estilo `Node/index.md`: TL;DR da trilha de 18 galhos, lista de galhos (Galho 1 linkado e ativo; demais como "planejado"), "Veja também" (JavaScript, TypeScript, Dicionário de Java). O `Java/Java.md` duplicado recebe nota de deprecação apontando pro `index.md` (não apagar — histórico). Os MOCs `Core/index.md`, `Backend/index.md`, `Frontend/index.md` permanecem por enquanto (serão absorvidos quando os galhos correspondentes migrarem); o `index.md` central passa a ser a entrada canônica.

> **Caveat Quartz:** `index.md` é obrigatório e NÃO pode ser removido (ver [[feedback_quartz_index]]). A pasta `Linguagem e sintaxe moderna/` precisa de seu próprio `index.md` como MOC (folder-link exige index.md — regra do Quartz).

### 3.5. Poda do tronco

`03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md` — poda **parcial** (só a camada de linguagem). Ver §6.

## 4. Convenções por nota

Herda §7 do roadmap. Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-02
updated: 2026-06-02
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - linguagem
  - <fase>
  - <tags específicas: oop, records, sealed, pattern-matching, generics, exceptions, enums, annotations, strings>
aliases:
  - <aliases>
---
```

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2)
- `## O que é` / `## Por que importa` / `## Como funciona` — H3s conforme o tópico (mínimo 3 subseções em "Como funciona" pra notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis, framing neutro ("padrão observado no JDK/Spring", "caso típico em..."); NUNCA "no meu projeto"
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com descrição + exemplo curto de código demonstrando o problema + fix em 1 linha
- `## Em entrevista` — frase pronta em inglês com **3+ sentenças** (trade-off + decisão + caveat) + vocabulário **6+ termos PT→EN** com tradução de cada
- `## Veja também` — wikilinks SEM backticks; sempre inclui notas relacionadas do galho + `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|MOC do galho]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + verbetes do Dicionário relevantes
- `## Referências` — docs oficiais (dev.java, docs.oracle.com), JEPs relevantes, talks identificadas

### 4.3. Restrições absolutas

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `alice@example.com`) ou hipotéticos explícitos (`// hipotético: ...`). NUNCA `josenaldo` nem caminhos pessoais.
2. **Sem invenção** de APIs/features/versões. Cada feature version-specific verificável via doc oficial ou JEP (WebFetch obrigatório no Step 1 de cada nota Magus e de qualquer feature recente).
3. **Code samples compiláveis** — Java válido; preferir snippets testáveis em jshell/JBang.
4. **Comparações justas** — ao comparar (record vs class, sealed vs enum, checked vs unchecked, interface vs abstract class), incluir "quando X vence" E "quando Y vence". Sem dogma.
5. **Versões hedged** — "Java 21+ (record patterns); primitive patterns são preview no 23+, verifique sua versão" em vez de afirmar disponibilidade GA precipitada.
6. **Wikilinks sem backticks** em "Veja também"; tronco + MOC do galho + MOC central obrigatórios.
7. **Code fences corretos:** ` ```java ` pra código, ` ```text ` pra output/bytecode/erros de compilação. Sempre fechadas.
8. **`fase:` no frontmatter + na tag** — obrigatório.
9. **Higiene de commits** — sem `Co-Authored-By: Claude`, sem `--no-verify`, `git add <path>` nominal, 1 commit por nota.
10. **Tom pedagógico graduado** — Iniciado assume pouco; Magus assume domínio dos anteriores.

## 5. Conteúdo por nota (síntese)

Esboço do recorte de cada nota. O conteúdo do tronco `Java Fundamentals` é matéria-prima (refatorar/expandir, não copiar 1:1); features recentes exigem verificação via doc oficial/JEP.

- **01 — Modelo da linguagem.** Por que Java domina enterprise. Tipagem, OO, bytecode→JVM, WORA. JDK/JRE/JVM. Releases 6-em-6-meses + LTS. Onde Java é usado hoje (backend, big data, Android legado). Armadilhas: confundir versão da linguagem com versão da JVM. Tronco: seção "O que é" + parte de "JVM" (nível mental) + "Features modernas por versão" (intro).
- **02 — Tipos e operadores.** Primitivos vs wrappers, autoboxing e seu custo, promoção/casting, `var` e quando NÃO usar, `==` vs `equals`, contrato equals/hashCode (intro, deep no 07). Armadilhas: `==` em wrappers/Strings, autoboxing em loop, `var` ofuscando tipo. Tronco: "Sintaxe básica e tipos".
- **03 — Controle de fluxo.** `if`, switch statement vs expression (arrow, `yield`, exaustividade básica), loops, labels. Armadilhas: fall-through no switch clássico, `switch` em null. Tronco: "Estruturas de controle".
- **04 — Strings e text blocks.** Imutabilidade e pool, StringBuilder vs concatenação, `formatted`, text blocks e incidental whitespace, métodos modernos. Armadilhas: `+` em loop, comparar com `==`. Tronco: "Strings".
- **05 — Arrays e varargs.** Arrays fixos, multidimensional, utilitários, varargs (alocação, ambiguidade), arrays vs `List`. Armadilhas: varargs + generics (heap pollution), `Arrays.asList` fixo. Tronco: "Arrays".
- **06 — Classes e encapsulamento.** Construtores/`this`, static vs instância, modificadores, encapsulamento, objetos imutáveis. Armadilhas: vazar referência mutável, static abusivo. Tronco: "OOP — Classes e objetos / Modificadores de acesso".
- **07 — Herança e polimorfismo.** extends/super, overriding vs overloading (regras), polimorfismo, `final`, `Object` methods (equals/hashCode/toString — contrato completo aqui). Armadilhas: quebrar contrato equals/hashCode, overloading confundido com overriding. Tronco: "Herança / Overriding vs Overloading".
- **08 — Interfaces e abstratas.** Interface (default/static/private), abstract class, decisão, diamante e resolução. Armadilhas: default method conflitante, abstract com estado vs interface. Tronco: "Classes abstratas vs Interfaces".
- **09 — Enums.** Enum com estado/comportamento, método abstrato por constante, EnumMap/EnumSet, singleton via enum, enum vs sealed. Armadilhas: `ordinal()` persistido, switch não-exaustivo em enum. Tronco: "Enums".
- **10 — Exceções.** Throwable, checked vs unchecked (debate + posição pragmática), try/catch/finally, try-with-resources (`AutoCloseable`, suppressed), custom exceptions, anti-patterns, exceções em lambdas/streams, exceções em APIs REST (gancho pro Galho 9). Armadilhas: swallow, catch `Exception`, throw em finally. Tronco: "Exceções".
- **11 — Annotations.** Built-in, meta-annotations, retention policies, custom annotation + processamento (visão geral), papel no Spring/Jakarta (gancho). Armadilhas: retention errada (RUNTIME vs SOURCE), esquecer `@Override`. Tronco: "Annotations".
- **12 — Generics.** Type params, bounded, wildcards + **PECS**, **type erasure** e consequências (no reified types, `instanceof` limitado, arrays de genéricos), métodos genéricos. Armadilhas: heap pollution, capturar wildcard, `Class<T>` token. Tronco: "Generics".
- **13 — Records.** Declaração, compact constructor + validação, accessors, record + interface, **record patterns**, imutabilidade rasa vs profunda, quando usar (DTO/value object/tuple), records em Spring. Armadilhas: record com campo mutável, esperar imutabilidade profunda. Tronco: "Records (Java 16+)".
- **14 — Sealed + pattern matching.** Sealed classes/interfaces + `permits`, instanceof pattern, switch patterns, record patterns, guards (`when`), **exaustividade** (sealed + switch dispensa default), primitive patterns (preview 23+). Armadilhas: switch não-exaustivo sem default, dominance de labels. Tronco: "Sealed Classes / Pattern Matching".
- **15 — Evolução do Java (8→25).** Timeline das features que importam (8 funcional/streams, 9 módulos, 10 var, 11 LTS, 14 switch expr, 16 records, 17 sealed LTS, 21 patterns+virtual threads LTS, 25 LTS), LTS vs feature release, preview features (`--enable-preview`), estratégia de migração de versão. Cheatsheet final. Tronco: "Features modernas por versão" + "Armadilhas comuns" (cheatsheet).

## 6. Poda do tronco (`Java Fundamentals.md`)

Poda **parcial** — só a camada de linguagem migra; JVM/Collections/Streams/Concorrência **ficam** (migram nos galhos 3/2/4). Procedimento:

1. **Ler o tronco** pra confirmar headings reais (linhas indicadas no §1 podem ter mudado).
2. **Substituir** por callout, as seções migradas: "Sintaxe básica e tipos", "Estruturas de controle", "Strings", "Arrays", "OOP em Java" (todas as subseções), "Records", "Sealed Classes", "Pattern Matching", "Annotations", "Generics", "Exceções", "Features modernas por versão".

```markdown
> [!nota] Migrado para galho próprio
> A camada de linguagem (tipos, OOP, records, sealed, pattern matching, generics, exceções) foi expandida no galho [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja em particular [[13 - Records e record patterns]] e [[14 - Sealed classes e pattern matching]].
```

3. **MANTER** intactas: "JVM" (vai pro Galho 3), "Collections Framework", "Lambdas e Interfaces Funcionais", "Streams API", "Date/Time API", "I/O", "Optional" (vão pro Galho 2), "Concorrência (visão geral)" (vai pro Galho 4). Adicionar callout `[!info]` no topo dessas indicando que migrarão em galhos futuros.
4. **Higienizar** a seção `## Na prática (da minha experiência)`: reescrever como padrão neutro ou remover atribuição pessoal (regra inegociável de fabricação).
5. **Atualizar** "Veja também" do tronco + `updated: 2026-06-02`.
6. **Não apagar** histórico — commit reversível.

Decisão sobre o destino final do tronco (MOC enxuto? deprecação?) só após galhos 1-4 fecharem.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 15 notas em `03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 5/6/4.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview.
3. Dicionário de Java criado (`type: glossary`) e semeado com ~30 verbetes da camada de linguagem.
4. MOC central `Java/index.md` reescrito; `Java.md` com nota de deprecação.
5. Tronco `Java Fundamentals` podado (camada de linguagem) + fabricação higienizada; seções de outros galhos preservadas com callout `[!info]`.
6. Cada nota: TL;DR; 3-5 code samples (notas conceituais); "Em entrevista" com frase 3+ sentenças EN + 6+ termos PT→EN; "Armadilhas" com exemplo+fix; wikilinks (galho + tronco + MOC + Dicionário).
7. Zero fabricação de experiência pessoal.
8. Features version-specific (records, sealed, patterns, switch expr, text blocks, primitive patterns) verificadas via doc oficial/JEP.
9. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal.
10. Quartz publica sem erros; folder-link da nova pasta resolve (index.md presente).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Nota 14 (sealed + pattern matching) inflar (>700 linhas) | Se passar de 700, dividir em "14 - Sealed classes" + "15 - Pattern matching" e renumerar evolução pra 16 (vira 16 notas). Decidir na execução. |
| Sobreposição record/sealed/enum entre notas 09, 13, 14 | Dono claro: enum→09, record→13, sealed+exaustividade→14. Outras linkam, não re-explicam. |
| Lambdas/streams "vazarem" pro galho 1 (estão no tronco junto) | Galho 1 só usa lambda como sintaxe necessária (interface funcional em 08/11); deep dive fica explicitamente no Galho 2, com wikilink. |
| Poda parcial deixar `Java Fundamentals` confuso (meio podado) | Callout `[!info]` no topo das seções preservadas explicando que migrarão; tronco aceito "em transição" até galhos 2-4. |
| Features preview (primitive patterns 23+) apresentadas como GA | Versões hedged + verificação JEP obrigatória; declarar "preview" explicitamente. |
| Migração flat quebrar wikilinks pra `Core/Java Fundamentals` | Manter o tronco onde está (em `Core/`) nesta rodada — só a pasta do galho é nova/flat; auditar com skill `verificar-wikilinks` no fim. |

## 9. Próximos passos

1. **Aprovação deste spec** + roadmap
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-02-java-galho-01-linguagem-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` (1 task por nota + tasks de Dicionário, MOC central, poda)
4. **Verificação** de wikilinks + build Quartz
5. **Revisão do roadmap** com aprendizados antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- Tronco a podar: `03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md`
- Specs de referência: `2026-05-07-node-runtime-event-loop-design.md`, `2026-05-22-terminal-cli-utils-design.md` (formato 3-fases)
- Memórias: [[project_tronco_galhos_pattern]], [[project_trilhas_fases_aprendizado]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]]
