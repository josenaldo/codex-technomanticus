# Galho 1 — Linguagem e sintaxe moderna (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 1 da trilha Java Senior — 15 notas atômicas de linguagem em 3 fases + MOC do galho + Dicionário de Java + reescrita do MOC central + poda parcial do tronco `Java Fundamentals`.

**Architecture:** Padrão tronco/galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Java/Linguagem e sintaxe moderna/`, notas atômicas `publish: true` em PT-BR, numeração global 01-15. Cada nota refatora/expande material do tronco `Core/Java Fundamentals.md` (matéria-prima, não cópia 1:1); features version-specific verificadas via doc oficial/JEP. Ao fim, o tronco é podado (só a camada de linguagem) e a fabricação higienizada.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4 (publicação). Verificação de fonte via WebFetch (dev.java, docs.oracle.com, openjdk.org/jeps).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases`/`created`/`updated` por nota):

```yaml
---
title: "<título sem prefixo numérico>"
created: 2026-06-02
updated: 2026-06-02
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - linguagem
  - <fase>
  - <1-3 tags de conceito>
aliases:
  - <aliases>
---
```

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas (conceito central + regra prática + por que importa). Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista. (Pode fundir com "O que é" em notas Iniciado curtas.)
4. `## Como funciona` — H3s; mínimo 3 subseções em notas Adepto/Magus.
5. `## Na prática` — exemplos compiláveis, framing neutro ("padrão observado no JDK/Spring", hipotético explícito `// hipotético:`). NUNCA "no meu projeto".
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada armadilha: `### (N) Título` + descrição + exemplo curto de código demonstrando o problema + fix em 1 linha.
7. `## Em entrevista` — frase pronta em inglês com **3+ sentenças** (trade-off + decisão + caveat) + sub-bloco "Vocabulário" com **6+ termos PT→EN** traduzidos.
8. `## Veja também` — wikilinks SEM backticks. Sempre inclui: notas relacionadas do galho + `[[03-Dominios/Java/Linguagem e sintaxe moderna/index|MOC do galho]]` + `[[03-Dominios/Java/index|Trilha Java]]` + `[[Java Fundamentals]]` (tronco) + verbetes do Dicionário relevantes.
9. `## Referências` — docs oficiais + JEPs.

**Tamanho:** 200-500 linhas (notas Magus densas até 700).

**Restrições absolutas** (qualquer violação reprova a nota):
- Sem fabricação de experiência pessoal. Exemplos: `Order`, `Customer`, `alice@example.com`, ou `// hipotético: ...`. NUNCA `josenaldo`/caminhos pessoais.
- Sem invenção de API/feature/versão. Feature version-specific → WebFetch da fonte oficial no Step de pesquisa.
- Comparações justas ("quando X vence" E "quando Y vence").
- Versões hedged (ex: "record patterns: Java 21+; primitive patterns são preview no 23+ — verifique sua versão").
- Code fences: ` ```java ` pra código, ` ```text ` pra output/bytecode/erro. Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (nunca `git add -A`); 1 commit por nota.

**Material de origem:** `03-Dominios/Java/Core/Java Fundamentals.md` (ler a seção indicada em cada task como matéria-prima; expandir, não copiar). Spec de referência: `docs/superpowers/specs/2026-06-02-java-galho-01-linguagem-design.md` §5.

---

## Task 0: Pré-flight — pasta, versões e leitura do tronco

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/` (pasta)
- Read: `03-Dominios/Java/Core/Java Fundamentals.md`

- [ ] **Step 1: Criar a pasta do galho**

```bash
mkdir -p "03-Dominios/Java/Linguagem e sintaxe moderna"
```

- [ ] **Step 2: Ler o tronco e confirmar headings reais**

Ler `03-Dominios/Java/Core/Java Fundamentals.md` inteiro. Anotar os números de linha REAIS das seções a podar (podem ter divergido do spec): "Sintaxe básica e tipos", "Estruturas de controle", "Strings", "Arrays", "OOP em Java", "Records", "Sealed Classes", "Pattern Matching", "Annotations", "Generics", "Exceções", "Features modernas por versão", e a seção "Na prática (da minha experiência)".

- [ ] **Step 3: Fixar versões assumidas do galho**

Baseline: **Java 21 LTS** e **Java 25 LTS** (2025). Mencionar Java 17 LTS quando relevante. Confirmar via WebFetch em `https://dev.java/evolution/` a lista de LTS e o status (GA vs preview) das features recentes (primitive patterns, structured concurrency). Registrar numa nota de rascunho mental — será usado nas notas 14 e 15.

- [ ] **Step 4: Sem commit** (task de preparação; nada a versionar ainda).

---

## Fase INICIADO (notas 01-05)

### Task 1: Nota 01 — O modelo da linguagem Java

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/01 - O modelo da linguagem Java.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://dev.java/evolution/` e `https://docs.oracle.com/en/java/javase/21/` pra confirmar: ciclo de releases (6 meses), cadência LTS (a cada 2 anos: 8, 11, 17, 21, 25), distinção JDK/JRE/JVM.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, linguagem, iniciado, jvm, fundamentos]`, aliases `["Modelo Java", "WORA"]`.

Conteúdo (matéria-prima: tronco "## O que é" + intro de "JVM" no nível mental):
- TL;DR: Java = OO, tipada estática/forte, compilada pra bytecode, GC, WORA via JVM.
- `## O que é` — história curta (1995, Gosling/Sun→Oracle), onde domina hoje (enterprise, microservices, big data, Android legado).
- `## Como funciona` — H3s: "Compilação pra bytecode" (.java → javac → .class → JVM), "Write Once Run Anywhere" (papel da JVM), "JDK vs JRE vs JVM", "Tipagem estática e forte".
- `## Por que importa` — pra senior: distinguir versão da linguagem vs versão da JVM; LTS na prática.
- `### Releases e LTS` — modelo 6-em-6-meses + LTS (8/11/17/21/25); o que "LTS" significa pra empresas.
- `## Armadilhas` — ≥2: (1) confundir versão da linguagem com versão da JVM; (2) achar que "compilado" = nativo (é bytecode + JIT).
- `## Em entrevista` — frase 3+ sentenças sobre WORA/bytecode/JIT trade-off; vocabulário 6+ termos.
- `## Veja também` — 02, 03, 15, MOC galho, MOC central, tronco, `[[03-Dominios/Java/Core/Helsinki MOOC - Guia de Revisão|Helsinki MOOC]]`, verbetes `bytecode`/`WORA`/`LTS`.
- `## Referências` — dev.java, docs Oracle.

Tamanho: 200-320 linhas (nota de abertura, pode ser mais conceitual).

- [ ] **Step 3: Verificar a nota**

```bash
head -20 "03-Dominios/Java/Linguagem e sintaxe moderna/01 - O modelo da linguagem Java.md"
grep -cE "^## (O que é|Como funciona|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Java/Linguagem e sintaxe moderna/01 - O modelo da linguagem Java.md"
```
Expected: frontmatter com `fase: iniciado`; grep retorna ≥6.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/01 - O modelo da linguagem Java.md"
git commit -m "feat(java): galho 1 nota 01 — o modelo da linguagem Java"
```

---

### Task 2: Nota 02 — Tipos, variáveis e operadores

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/02 - Tipos, variáveis e operadores.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch doc oficial de primitivos (`https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html`) e `var` (JEP 286 / `https://dev.java/learn/`). Confirmar regras de autoboxing e cache de `Integer` (-128..127).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, linguagem, iniciado, tipos, operadores]`, aliases `["Tipos primitivos", "var"]`.

Conteúdo (matéria-prima: tronco "## Sintaxe básica e tipos"):
- `## O que é` — primitivos vs objetos.
- `## Como funciona` — H3s: "Primitivos e wrappers" (8 primitivos, autoboxing/unboxing + custo), "Casting e promoção numérica", "`var` e inferência local" (quando usar/não usar), "Igualdade: `==` vs `equals`" (referência vs valor), "Contrato equals/hashCode (introdução)" — apontar deep dive pra nota 07.
- `## Na prática` — exemplos de autoboxing em loop (custo), `var` legível vs ofuscante.
- `## Armadilhas` — ≥2: (1) `==` em wrappers/Strings (cache do Integer); (2) autoboxing em loop quente; (3) `var` escondendo o tipo.
- `## Em entrevista` + `## Veja também` (01, 07, MOC, tronco, verbetes `autoboxing`/`inferência de tipo (var)`) + `## Referências`.

Tamanho: 250-380 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "^fase: iniciado" "03-Dominios/Java/Linguagem e sintaxe moderna/02 - Tipos, variáveis e operadores.md"
grep -cE "^### \(" "03-Dominios/Java/Linguagem e sintaxe moderna/02 - Tipos, variáveis e operadores.md"
```
Expected: `fase: iniciado` presente; ≥2 armadilhas numeradas.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/02 - Tipos, variáveis e operadores.md"
git commit -m "feat(java): galho 1 nota 02 — tipos, variáveis e operadores"
```

---

### Task 3: Nota 03 — Estruturas de controle e fluxo

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/03 - Estruturas de controle e fluxo.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch JEP 361 (Switch Expressions) `https://openjdk.org/jeps/361`. Confirmar sintaxe `->`, `yield`, exaustividade.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, linguagem, iniciado, controle-de-fluxo, switch]`, aliases `["switch expression", "Estruturas de controle"]`.

Conteúdo (matéria-prima: tronco "## Estruturas de controle"):
- `## Como funciona` — H3s: "Condicionais (`if`/ternário)", "`switch` statement vs `switch` expression" (arrow form, `yield`, multi-label, exaustividade básica — gancho pro 14), "Loops (`for`, enhanced for, `while`/`do-while`)", "`break`, `continue`, labels".
- `## Na prática` — refatorar switch clássico (fall-through) pra switch expression.
- `## Armadilhas` — ≥2: (1) fall-through esquecendo `break` no switch clássico; (2) `switch` em `null` (NPE vs case `null` no moderno).
- `## Em entrevista` + `## Veja também` (02, 04, 14, MOC, tronco, verbetes `switch expression`/`yield`) + `## Referências`.

Tamanho: 220-350 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "switch expression|->|yield" "03-Dominios/Java/Linguagem e sintaxe moderna/03 - Estruturas de controle e fluxo.md" | head
```
Expected: cobre switch expression.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/03 - Estruturas de controle e fluxo.md"
git commit -m "feat(java): galho 1 nota 03 — estruturas de controle e fluxo"
```

---

### Task 4: Nota 04 — Strings e text blocks

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/04 - Strings e text blocks.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch JEP 378 (Text Blocks) `https://openjdk.org/jeps/378`. Confirmar incidental whitespace, `stripIndent`, métodos `lines`/`strip`/`repeat`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, linguagem, iniciado, strings, text-blocks]`, aliases `["String", "text blocks"]`.

Conteúdo (matéria-prima: tronco "## Strings"):
- `## Como funciona` — H3s: "Imutabilidade e String pool" (`intern`), "`StringBuilder` vs concatenação", "Formatação (`String.format`/`formatted`)", "Text blocks (Java 15+)" (incidental whitespace, interpolação ausente — sem template strings GA).
- `## Na prática` — JSON/SQL multi-linha com text block.
- `## Armadilhas` — ≥2: (1) `+` em loop (use StringBuilder); (2) comparar Strings com `==`; (3) indentação incidental em text block.
- `## Em entrevista` + `## Veja também` (02, 03, MOC, tronco, verbetes `String pool`/`text block`) + `## Referências`.

Tamanho: 250-380 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "text block|String pool|StringBuilder" "03-Dominios/Java/Linguagem e sintaxe moderna/04 - Strings e text blocks.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/04 - Strings e text blocks.md"
git commit -m "feat(java): galho 1 nota 04 — strings e text blocks"
```

---

### Task 5: Nota 05 — Arrays e varargs

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/05 - Arrays e varargs.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch doc de `Arrays` (`https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Arrays.html`) e heap pollution com varargs+generics (`@SafeVarargs`).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, linguagem, iniciado, arrays, varargs]`, aliases `["Array", "varargs"]`.

Conteúdo (matéria-prima: tronco "## Arrays"):
- `## Como funciona` — H3s: "Declaração e inicialização", "Arrays multidimensionais", "Utilitários (`Arrays`, `System.arraycopy`)", "Varargs" (desugaring pra array, ambiguidade de overload), "Arrays vs `List`".
- `## Armadilhas` — ≥2: (1) varargs + generics = heap pollution (`@SafeVarargs`); (2) `Arrays.asList` retorna lista de tamanho fixo; (3) `array.length` vs `list.size()`.
- `## Em entrevista` + `## Veja também` (02, 12, MOC, tronco, verbete `varargs`) + `## Referências`.

Tamanho: 200-320 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "varargs|heap pollution|SafeVarargs" "03-Dominios/Java/Linguagem e sintaxe moderna/05 - Arrays e varargs.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/05 - Arrays e varargs.md"
git commit -m "feat(java): galho 1 nota 05 — arrays e varargs"
```

---

## Fase ADEPTO (notas 06-11)

### Task 6: Nota 06 — Classes, objetos e encapsulamento

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/06 - Classes, objetos e encapsulamento.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch tutorial de classes/objetos da Oracle. Confirmar regras de modificadores de acesso (default/package-private incluído).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, linguagem, adepto, oop, encapsulamento]`, aliases `["Classes", "Encapsulamento"]`.

Conteúdo (matéria-prima: tronco "### Classes e objetos" + "### Modificadores de acesso"):
- `## Como funciona` — H3s: "Construtores e `this`", "Membros estáticos vs instância", "Modificadores de acesso (`public`/`protected`/default/`private`)", "Encapsulamento e getters/setters", "Objetos imutáveis (campos `final`, defensive copy)".
- `## Na prática` — value object imutável (gancho pro 13 records).
- `## Armadilhas` — ≥3: (1) vazar referência mutável via getter; (2) static abusivo (estado global); (3) inicialização em construtor vs field; cada uma com exemplo + fix.
- `## Em entrevista` + `## Veja também` (07, 08, 13, MOC, tronco, verbete `immutability`) + `## Referências`.

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "^fase: adepto" "03-Dominios/Java/Linguagem e sintaxe moderna/06 - Classes, objetos e encapsulamento.md"
grep -cE "^### \([0-9]" "03-Dominios/Java/Linguagem e sintaxe moderna/06 - Classes, objetos e encapsulamento.md"
```
Expected: `fase: adepto`; ≥3 armadilhas.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/06 - Classes, objetos e encapsulamento.md"
git commit -m "feat(java): galho 1 nota 06 — classes, objetos e encapsulamento"
```

---

### Task 7: Nota 07 — Herança e polimorfismo

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/07 - Herança e polimorfismo.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch contrato `equals`/`hashCode` (`Object` docs) e regras de overriding (covariância de retorno, `@Override`).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, linguagem, adepto, oop, polimorfismo]`, aliases `["Herança", "Polimorfismo", "Overriding"]`.

Conteúdo (matéria-prima: tronco "### Herança" + "### Overriding vs Overloading"):
- `## Como funciona` — H3s: "`extends` e `super`", "Overriding vs overloading (regras e dispatch)", "Polimorfismo dinâmico", "`final` (classe/método/var)", "Covariância de retorno", "Métodos de `Object`: `equals`/`hashCode`/`toString`" (contrato COMPLETO aqui — dono do conceito).
- `## Na prática` — implementar `equals`/`hashCode` corretos (e por que records resolvem isso — gancho 13).
- `## Armadilhas` — ≥3: (1) quebrar contrato equals/hashCode (set/map quebram); (2) confundir overloading (compile-time) com overriding (runtime); (3) chamar método overridable no construtor; com exemplo + fix.
- `## Em entrevista` + `## Veja também` (06, 08, 09, 13, MOC, tronco, verbetes `overriding`/`overloading`/`polimorfismo`) + `## Referências`.

Tamanho: 320-460 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "overriding|overloading|equals|hashCode" "03-Dominios/Java/Linguagem e sintaxe moderna/07 - Herança e polimorfismo.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/07 - Herança e polimorfismo.md"
git commit -m "feat(java): galho 1 nota 07 — herança e polimorfismo"
```

---

### Task 8: Nota 08 — Interfaces e classes abstratas

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/08 - Interfaces e classes abstratas.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch sobre default/static/private methods em interfaces (JEP 8/9 era) e resolução de conflito (diamante).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, linguagem, adepto, oop, interfaces]`, aliases `["Interface", "Classe abstrata"]`.

Conteúdo (matéria-prima: tronco "### Classes abstratas vs Interfaces"):
- `## Como funciona` — H3s: "Interfaces (default/static/private methods)", "Classes abstratas", "Interface vs abstract class — decisão", "Herança múltipla de tipo e o problema do diamante".
- `## Na prática` — quando default method é útil (evolução de API sem quebrar implementadores); comparação justa interface vs abstract.
- `## Armadilhas` — ≥3: (1) conflito de default methods (resolução obrigatória); (2) querer estado em interface (não tem — só `static final`); (3) abusar de default como "trait". Exemplo + fix.
- `## Em entrevista` + `## Veja também` (07, 09, 11, MOC, tronco, verbete `default method`) + `## Referências`.

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "default method|abstract|diamante|diamond" "03-Dominios/Java/Linguagem e sintaxe moderna/08 - Interfaces e classes abstratas.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/08 - Interfaces e classes abstratas.md"
git commit -m "feat(java): galho 1 nota 08 — interfaces e classes abstratas"
```

---

### Task 9: Nota 09 — Enums

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/09 - Enums.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch doc de `EnumMap`/`EnumSet` e o padrão enum-singleton (Effective Java item 3).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, linguagem, adepto, oop, enums]`, aliases `["Enum"]`.

Conteúdo (matéria-prima: tronco "### Enums"):
- `## Como funciona` — H3s: "Enum com estado e comportamento (construtor, campos)", "Método abstrato por constante", "`EnumMap` e `EnumSet`", "Enum como singleton", "Enum vs sealed (quando cada um)" — gancho 14.
- `## Armadilhas` — ≥3: (1) persistir `ordinal()` (quebra ao reordenar — persistir `name()`); (2) `switch` não-exaustivo em enum (sem default novo case some); (3) enum com estado mutável. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (07, 14, MOC, tronco, verbete `enum`) + `## Referências`.

Tamanho: 260-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "EnumMap|EnumSet|ordinal|sealed" "03-Dominios/Java/Linguagem e sintaxe moderna/09 - Enums.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/09 - Enums.md"
git commit -m "feat(java): galho 1 nota 09 — enums"
```

---

### Task 10: Nota 10 — Exceções e tratamento de erros

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch try-with-resources / `AutoCloseable` / suppressed exceptions (docs Oracle).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, linguagem, adepto, exceptions, erros]`, aliases `["Exceções", "try-with-resources"]`.

Conteúdo (matéria-prima: tronco "## Exceções"):
- `## Como funciona` — H3s: "Hierarquia (`Throwable`/`Error`/`Exception`/`RuntimeException`)", "Checked vs unchecked (o debate + posição pragmática sem dogma)", "`try`/`catch`/`finally`", "try-with-resources (`AutoCloseable`, suppressed)", "Custom exceptions (boas práticas)".
- `## Na prática` — exceções em lambdas/streams (wrapping); tratamento em API REST (gancho Galho 9).
- `## Armadilhas` — ≥3: (1) swallow (catch vazio); (2) catch `Exception`/`Throwable` genérico; (3) `return`/`throw` em `finally`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (08, MOC, tronco, verbetes `checked exception`/`unchecked exception`/`try-with-resources`) + `## Referências`.

Tamanho: 320-460 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "checked|unchecked|try-with-resources|AutoCloseable" "03-Dominios/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros.md"
git commit -m "feat(java): galho 1 nota 10 — exceções e tratamento de erros"
```

---

### Task 11: Nota 11 — Annotations

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch sobre meta-annotations (`@Retention`, `@Target`, `@Documented`, `@Inherited`) e annotation processing (visão geral).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, linguagem, adepto, annotations, metaprogramacao]`, aliases `["Annotations", "Anotações"]`.

Conteúdo (matéria-prima: tronco "## Annotations"):
- `## Como funciona` — H3s: "Built-in (`@Override`, `@Deprecated`, `@FunctionalInterface`, `@SuppressWarnings`)", "Meta-annotations e retention policies (SOURCE/CLASS/RUNTIME)", "Annotations customizadas", "Annotation processing (visão geral)", "Papel no Spring/Jakarta" (gancho galhos 7/8).
- `## Armadilhas` — ≥3: (1) retention errada (SOURCE quando precisa RUNTIME via reflection); (2) esquecer `@Override` (typo vira overload silencioso); (3) annotation sem `@Target` aplicada em lugar errado. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (07, 08, MOC, tronco) + `## Referências`.

Tamanho: 260-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "Retention|Target|RUNTIME|FunctionalInterface" "03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/11 - Annotations.md"
git commit -m "feat(java): galho 1 nota 11 — annotations"
```

---

## Fase MAGUS (notas 12-15)

### Task 12: Nota 12 — Generics em profundidade

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/12 - Generics em profundidade.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch sobre type erasure e PECS (Oracle Generics tutorial / Effective Java itens 26-33).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, linguagem, magus, generics, type-system]`, aliases `["Generics", "Genéricos", "PECS"]`.

Conteúdo (matéria-prima: tronco "## Generics"):
- `## Como funciona` — H3s: "Type parameters e métodos genéricos", "Bounded types (`extends`/`super`)", "Wildcards e **PECS** (Producer-Extends, Consumer-Super)", "**Type erasure** e consequências (no reified types, `instanceof` limitado, arrays de genéricos)", "Type tokens (`Class<T>`)".
- `## Na prática` — assinatura de API genérica bem-desenhada (ex: `copy(List<? super T> dst, List<? extends T> src)`).
- `## Armadilhas` — ≥3: (1) heap pollution (varargs+generics); (2) tentar `new T[]` / `instanceof List<String>`; (3) wildcard capture. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (05, 02, MOC, tronco, verbetes `generics`/`PECS`/`type erasure`/`wildcard`) + `## Referências`.

Tamanho: 350-520 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "PECS|type erasure|wildcard|reified" "03-Dominios/Java/Linguagem e sintaxe moderna/12 - Generics em profundidade.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/12 - Generics em profundidade.md"
git commit -m "feat(java): galho 1 nota 12 — generics em profundidade"
```

---

### Task 13: Nota 13 — Records e record patterns

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/13 - Records e record patterns.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch JEP 395 (Records) `https://openjdk.org/jeps/395` e JEP 440 (Record Patterns) `https://openjdk.org/jeps/440`. Confirmar GA do record pattern (Java 21).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, linguagem, magus, records, imutabilidade]`, aliases `["Record", "Records", "record patterns"]`.

Conteúdo (matéria-prima: tronco "## Records (Java 16+)"):
- `## Como funciona` — H3s: "Declaração e componentes (accessors, `equals`/`hashCode`/`toString` gerados)", "**Compact constructor** e validação", "Métodos adicionais e estáticos", "Records + interfaces", "**Record patterns** (Java 21, desestruturação)", "Imutabilidade rasa vs profunda".
- `## Na prática` — DTO/value object/tuple; records em Spring (request/response, `@ConfigurationProperties`).
- `## Armadilhas` — ≥3: (1) record com componente mutável (imutabilidade só rasa); (2) esperar encapsulamento (accessor expõe tudo); (3) record para entidade JPA (precisa no-arg ctor). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (06, 07, 14, MOC, tronco, verbetes `record`/`compact constructor`/`record pattern`) + `## Referências` (JEPs).

Tamanho: 350-520 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "compact constructor|record pattern|imutabilidade" "03-Dominios/Java/Linguagem e sintaxe moderna/13 - Records e record patterns.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/13 - Records e record patterns.md"
git commit -m "feat(java): galho 1 nota 13 — records e record patterns"
```

---

### Task 14: Nota 14 — Sealed classes e pattern matching

> **Contingência:** se esta nota passar de ~700 linhas, dividir em `14 - Sealed classes` + `15 - Pattern matching` e renumerar a evolução pra `16` (galho vira 16 notas). Atualizar MOC e numeração das tasks 15+ se isso ocorrer.

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/14 - Sealed classes e pattern matching.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch JEP 409 (Sealed Classes) `https://openjdk.org/jeps/409`, JEP 441 (Pattern Matching for switch) `https://openjdk.org/jeps/441`, e o status de **primitive patterns** (JEP 455, preview no 23+) em `https://dev.java/evolution/`. Confirmar exaustividade (sealed + switch dispensa `default`).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, linguagem, magus, sealed, pattern-matching]`, aliases `["Sealed classes", "Pattern matching", "switch patterns"]`.

Conteúdo (matéria-prima: tronco "## Sealed Classes (Java 17+)" + "## Pattern Matching"):
- `## Como funciona` — H3s: "Sealed classes/interfaces (`sealed`/`permits`/`non-sealed`)", "`instanceof` pattern (Java 16)", "**Switch patterns** (Java 21)", "Record patterns em switch (desestruturação aninhada)", "Guards (`when`)", "**Exaustividade** (sealed + switch sem `default`)" — DONO do conceito exaustividade, "Primitive patterns (preview 23+)".
- `## Na prática` — modelar domínio fechado (ex: `sealed interface Shape permits Circle, Square`) + switch exaustivo; comparação com visitor pattern.
- `## Armadilhas` — ≥3: (1) switch não-exaustivo sem default (compila em enum/sealed mas quebra ao adicionar tipo se tiver default); (2) ordem/dominance de labels (case mais específico antes); (3) tratar primitive patterns como GA. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (03, 09, 13, MOC, tronco, verbetes `sealed class`/`pattern matching`/`exhaustiveness`/`guard (pattern)`) + `## Referências` (JEPs 409/441/455).

Tamanho: 400-650 linhas (nota mais densa do galho).

- [ ] **Step 3: Verificar**

```bash
grep -E "sealed|permits|switch pattern|exaustiv|guard|when" "03-Dominios/Java/Linguagem e sintaxe moderna/14 - Sealed classes e pattern matching.md" | head
wc -l "03-Dominios/Java/Linguagem e sintaxe moderna/14 - Sealed classes e pattern matching.md"
```
Expected: cobre sealed+patterns+exaustividade; se `wc -l` > 700, aplicar contingência de divisão.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/14 - Sealed classes e pattern matching.md"
git commit -m "feat(java): galho 1 nota 14 — sealed classes e pattern matching"
```

---

### Task 15: Nota 15 — A evolução do Java (8 → 25)

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/15 - A evolução do Java (8 a 25).md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://dev.java/evolution/` pra a timeline definitiva. Confirmar: features-chave por versão, quais são LTS (8/11/17/21/25), o que é preview vs GA, `--enable-preview`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, linguagem, magus, versoes, lts]`, aliases `["Evolução do Java", "Features por versão", "Java timeline"]`.

Conteúdo (matéria-prima: tronco "## Features modernas por versão" + "## Armadilhas comuns" como cheatsheet):
- `## O que é` — por que acompanhar a evolução importa pra senior.
- `## Como funciona` — H3s: "Modelo de releases (6 meses) e LTS", "Preview features e `--enable-preview`", "Timeline das features que importam" (tabela: 8 lambdas/streams/Optional, 9 módulos/`var` no 10, 11 LTS/`String` methods, 14 switch expr, 15 text blocks, 16 records, 17 LTS sealed, 21 LTS patterns+virtual threads, 25 LTS), "Estratégia de migração entre versões".
- `## Na prática` — checklist de migração 8→17→21.
- `## Armadilhas` — ≥2: (1) usar preview em produção sem `--enable-preview` consciente; (2) confundir feature release com LTS no planejamento.
- `### Cheatsheet` — tabela-resumo das features do galho por versão.
- `## Em entrevista` + `## Veja também` (01, 03, 13, 14, MOC, tronco, verbetes `LTS`/`preview feature`) + `## Referências`.

Tamanho: 300-450 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "LTS|preview|enable-preview|virtual threads" "03-Dominios/Java/Linguagem e sintaxe moderna/15 - A evolução do Java (8 a 25).md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/15 - A evolução do Java (8 a 25).md"
git commit -m "feat(java): galho 1 nota 15 — a evolução do Java (8 a 25)"
```

---

## Task 16: MOC do galho

**Files:**
- Create: `03-Dominios/Java/Linguagem e sintaxe moderna/index.md`

- [ ] **Step 1: Escrever o MOC**

Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "Linguagem e sintaxe moderna"`, tags `[java, linguagem, moc]`, aliases `["Linguagem Java", "Galho 1 - Linguagem"]`, `created`/`updated: 2026-06-02`.

Conteúdo:
- `> [!abstract] TL;DR` — Galho 1 da trilha Java Senior; camada de linguagem do Java moderno, da sintaxe a records/sealed/pattern matching; base de todos os galhos.
- `## Sobre este galho` — escopo + audiência primária (senior em prep de entrevista, com "Em entrevista" em cada nota) + secundária (decisões de design/code review).
- `## Iniciado` — wikilinks 01-05.
- `## Adepto` — wikilinks 06-11.
- `## Magus` — wikilinks 12-15.
- `## Rotas alternativas` — 5 rotas (Completa 01→15; Entrevista 01→07→10→12→13→14; Features modernas 03→04→13→14→15; Pré-OCP 02→05→07→08→10→12; Fundamentos OOP 06→07→08→09).
- `## Todas as notas` — bloco Dataview:

````markdown
```dataview
TABLE fase, status, updated
FROM "03-Dominios/Java/Linguagem e sintaxe moderna"
WHERE type = "concept"
SORT file.name ASC
```
````

- `## Veja também` — `[[03-Dominios/Java/index|Java (MOC central)]]`, `[[Java Fundamentals]]` (tronco), `[[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]`, `[[03-Dominios/Java/Core/Helsinki MOOC - Guia de Revisão|Helsinki MOOC]]`.

- [ ] **Step 2: Verificar**

```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Java/Linguagem e sintaxe moderna/index.md"
grep -c "\[\[" "03-Dominios/Java/Linguagem e sintaxe moderna/index.md"
```
Expected: 4 headings de seção; ≥15 wikilinks (uma por nota).

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Java/Linguagem e sintaxe moderna/index.md"
git commit -m "feat(java): galho 1 MOC — linguagem e sintaxe moderna"
```

---

## Task 17: Dicionário de Java (criação + semeadura)

**Files:**
- Create: `03-Dominios/Java/Dicionário de Java.md`

- [ ] **Step 1: Inspecionar um glossário existente como template**

Ler `03-Dominios/Terminal/Dicionário do Terminal.md` (primeiras ~40 linhas) pra herdar frontmatter `type: glossary`, estrutura de seções alfabéticas e formato de verbete + `Veja também:`.

- [ ] **Step 2: Escrever o Dicionário semeado**

Frontmatter: `type: glossary`, `publish: true`, `title: "Dicionário de Java"`, tags `[java, glossary, moc]`, aliases `["Glossário de Java"]`, `created`/`updated: 2026-06-02`.

Seções alfabéticas (A, B, C…) com ~30-35 verbetes da camada de linguagem (1-3 linhas cada + `Veja também:` pra nota canônica):
`autoboxing` (→02), `bytecode` (→01), `checked exception` (→10), `compact constructor` (→13), `default method` (→08), `enhanced for` (→03), `enum` (→09), `exhaustiveness` (→14), `generics` (→12), `guard (pattern)` (→14), `immutability` (→06), `inferência de tipo (var)` (→02), `LTS` (→01/15), `overloading` (→07), `overriding` (→07), `pattern matching` (→14), `PECS` (→12), `polimorfismo` (→07), `preview feature` (→15), `record` (→13), `record pattern` (→13/14), `sealed class` (→14), `String pool` (→04), `switch expression` (→03), `text block` (→04), `try-with-resources` (→10), `type erasure` (→12), `unchecked exception` (→10), `varargs` (→05), `wildcard` (→12), `WORA` (→01), `yield` (→03).

Ordenação alfabética case-insensitive, sem acento.

- [ ] **Step 3: Verificar**

```bash
grep -E "type: glossary" "03-Dominios/Java/Dicionário de Java.md"
grep -c "Veja também" "03-Dominios/Java/Dicionário de Java.md"
```
Expected: `type: glossary`; ≥30 ocorrências de "Veja também".

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/Dicionário de Java.md"
git commit -m "feat(java): cria Dicionário de Java semeado com verbetes de linguagem"
```

---

## Task 18: Reescrever o MOC central `Java/index.md`

**Files:**
- Modify: `03-Dominios/Java/index.md`
- Modify: `03-Dominios/Java/Java.md` (nota de deprecação)

- [ ] **Step 1: Reescrever `Java/index.md` no estilo Node**

Manter frontmatter `type: moc`, `publish: true`; atualizar `updated: 2026-06-02`, `status: growing`, tags `[moc, java]`.

Conteúdo:
- `> [!abstract] TL;DR` — Trilha Java Senior em 18 galhos (linguagem → JVM → concorrência → desktop → Jakarta EE → Spring → reativa → segurança → testes → mensageria → build → microservices → cloud-native → OCP).
- `## Galhos da trilha` — lista dos 18 galhos. Galho 1 com wikilink ativo `[[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]` + descrição; galhos 2-18 como texto "(planejado)" com descrição curta (NÃO criar wikilinks pra pastas inexistentes — quebraria o Quartz; ver [[feedback_quartz_index]]).
- `## Referência` — `[[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]`, `[[Java Fundamentals]]` (tronco), `[[03-Dominios/Java/Core/Helsinki MOOC - Guia de Revisão|Helsinki MOOC]]`, `[[03-Dominios/Java/Core/Certificação Java OCP|Certificação OCP]]`.
- `## Veja também` — `[[03-Dominios/JavaScript/index|JavaScript]]`.

- [ ] **Step 2: Adicionar nota de deprecação em `Java/Java.md`**

No topo do corpo (após frontmatter), inserir callout:

```markdown
> [!warning] Nota legada
> Este MOC foi substituído por [[03-Dominios/Java/index|Java (índice central)]], reorganizado na trilha Java Senior de 18 galhos. Mantido por compatibilidade de wikilinks; não atualizar.
```

NÃO apagar o arquivo (histórico + wikilinks existentes).

- [ ] **Step 3: Verificar**

```bash
grep -cE "Galho|galho|planejado" "03-Dominios/Java/index.md"
grep -E "Linguagem e sintaxe moderna/index" "03-Dominios/Java/index.md"
grep -E "Nota legada" "03-Dominios/Java/Java.md"
```
Expected: lista dos galhos presente; wikilink ativo do Galho 1; callout de deprecação no Java.md.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Java/index.md" "03-Dominios/Java/Java.md"
git commit -m "feat(java): reescreve MOC central (trilha de 18 galhos) e deprecia Java.md"
```

---

## Task 19: Poda parcial do tronco `Java Fundamentals.md`

**Files:**
- Modify: `03-Dominios/Java/Core/Java Fundamentals.md`

- [ ] **Step 1: Reler o tronco e confirmar headings (usar notas do Task 0)**

Confirmar os ranges reais das seções a podar vs preservar.

- [ ] **Step 2: Podar as seções migradas (substituir por callout)**

Para CADA uma das seções migradas — "Sintaxe básica e tipos", "Estruturas de controle", "Strings", "Arrays", "OOP em Java" (com subseções), "Records", "Sealed Classes", "Pattern Matching", "Annotations", "Generics", "Exceções", "Features modernas por versão" — substituir o corpo por callout (manter o heading H2):

```markdown
> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna]]. Veja [[03-Dominios/Java/Linguagem e sintaxe moderna/<nota canônica do tópico>|<título>]].
```

(Apontar a nota canônica certa por tópico: tipos→02, controle→03, strings→04, arrays→05, OOP→06/07/08, records→13, sealed/pattern→14, annotations→11, generics→12, exceções→10, features→15.)

- [ ] **Step 3: Marcar as seções preservadas (vão pra outros galhos)**

No topo das seções "JVM", "Collections Framework", "Lambdas e Interfaces Funcionais", "Streams API", "Date/Time API", "I/O", "Optional", "Concorrência (visão geral)", inserir:

```markdown
> [!info] Migra em galho futuro
> Este tópico será expandido em galho próprio (JVM → Galho 3; Collections/Streams/Optional/Date-Time/IO → Galho 2; Concorrência → Galho 4). Por ora permanece aqui.
```

- [ ] **Step 4: Higienizar a fabricação**

Localizar `## Na prática (da minha experiência)` (≈ linha 1614) e reescrever como padrão neutro (ex: "## Na prática" com "padrão observado no ecossistema") OU remover a atribuição pessoal. **Regra inegociável** (ver [[feedback_no_fabrication]]). Varrer o resto do tronco por outras 1ªs pessoas ("eu", "meu", "na minha") e neutralizar.

- [ ] **Step 5: Atualizar frontmatter e "Veja também"**

`updated: 2026-06-02`. Em "Veja também", adicionar `[[03-Dominios/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (galho)]]`.

- [ ] **Step 6: Verificar**

```bash
grep -c "Migrado para galho próprio" "03-Dominios/Java/Core/Java Fundamentals.md"
grep -iE "da minha experiência|na minha experiência" "03-Dominios/Java/Core/Java Fundamentals.md"
```
Expected: ≥10 callouts de migração; ZERO ocorrências de "minha experiência".

- [ ] **Step 7: Commit**

```bash
git add "03-Dominios/Java/Core/Java Fundamentals.md"
git commit -m "refactor(java): poda parcial de Java Fundamentals (camada de linguagem → galho 1) + higieniza fabricação"
```

---

## Task 20: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: Conferir as 15 notas + MOC presentes**

```bash
ls "03-Dominios/Java/Linguagem e sintaxe moderna/" | sort
```
Expected: 01..15 + index.md (16 arquivos .md).

- [ ] **Step 2: Conferir frontmatter `fase` em todas**

```bash
grep -rL "^fase:" "03-Dominios/Java/Linguagem e sintaxe moderna/"*" - "*.md 2>/dev/null | grep -v index.md
for f in "03-Dominios/Java/Linguagem e sintaxe moderna/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```
Expected: toda nota 01-15 tem `fase:`; distribuição 5 iniciado / 6 adepto / 4 magus.

- [ ] **Step 3: Conferir seções obrigatórias em todas as notas**

```bash
for f in "03-Dominios/Java/Linguagem e sintaxe moderna/"[0-9]*.md; do
  echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"
done
```
Expected: cada nota retorna 3 (tem "Em entrevista", "Armadilhas", "Veja também").

- [ ] **Step 4: Rodar a skill de wikilinks**

Invocar a skill `verificar-wikilinks` na pasta `03-Dominios/Java/Linguagem e sintaxe moderna/` + `03-Dominios/Java/index.md`. Corrigir quebrados (especialmente folder-links que exigem index.md — regra Quartz).

- [ ] **Step 5: Build Quartz (se disponível no repo do site)**

Confirmar publicação sem erro conforme o pipeline do projeto (deploy cross-repo). Se o build não rodar localmente neste repo, registrar como verificação manual pendente.

- [ ] **Step 6: Sem commit** (task de verificação; correções de wikilink, se houver, commitam à parte).

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** as 15 notas (Tasks 1-15) cobrem o §3.1 do spec; MOC (16) cobre §3.2; Dicionário (17) cobre §3.3; MOC central (18) cobre §3.4; poda (19) cobre §3.5/§6; verificação (20) cobre §7. Todas as seções do spec mapeadas.

**Placeholder scan:** sem TBD/TODO. Conteúdo por nota especificado com seções concretas, fontes WebFetch nomeadas, armadilhas mínimas e tamanho-alvo.

**Type/naming consistency:** numeração 01-15 consistente entre tasks, MOC, Dicionário e poda. Rotas alternativas no MOC (Task 16) referenciam as mesmas notas. Contingência de divisão da nota 14 documentada com efeito na renumeração.
