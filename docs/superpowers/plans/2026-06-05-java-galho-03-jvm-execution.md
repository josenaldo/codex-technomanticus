# Galho 3 — JVM por dentro (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 3 da trilha Java Senior — 14 notas atômicas (memória de runtime, GC, JIT, classloading, bytecode, JPMS, diagnóstico/JFR, performance) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **poda da seção JVM do tronco** `Java Fundamentals` + **quitação da dívida reversa** ("Galho 3 planejado" → wikilinks).

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Tecnologia/Java/JVM/`, notas atômicas `publish: true` em PT-BR, numeração global 01-14 (5 Iniciado / 5 Adepto / 4 Magus). **Galho de refator de tronco:** a seção `## JVM (Java Virtual Machine)` de `Core/Java Fundamentals.md` está marcada `[!info] Migra em galho futuro (Galho 3)` e é matéria-prima **desatualizada** (tabela de GC com CMS, ZGC "Java 15" sem generational) — as notas **expandem e modernizam via WebFetch** (não copiam). Galho dono do *runtime* da JVM; **linka** Galho 4 (JMM, Virtual Threads), Galho 2 (lambdas/invokedynamic, boxing) e Galho 1 sem re-explicar. A seção `## Concorrência (visão geral)` do tronco é dívida do Galho 4 — **não é tocada**. **Trabalho direto na `main`** (sem branch — [[feedback_galhos_direto_main]]); push é manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação de fonte via WebFetch (docs.oracle.com — JVM Guide/GC Tuning Guide/troubleshooting/man pages, dev.java, Javadoc; JEPs no openjdk.org dão 403 → fallback Oracle/dev.java).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-05`):

```yaml
---
title: "<título sem prefixo numérico>"
created: 2026-06-05
updated: 2026-06-05
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - jvm
  - <fase>
  - <1-3 tags de conceito: gc, jit, bytecode, classloading, jpms, tuning, diagnostico, jfr, memoria>
aliases:
  - <aliases>
---
```

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas (conceito central + regra prática + por que importa). Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista/produção. (Pode fundir com "O que é" em notas Iniciado curtas.)
4. `## Como funciona` — H3s; mínimo 3 subseções em notas Adepto/Magus.
5. `## Na prática` — código Java e/ou comandos de CLI (`java -XX:...`, `jcmd`, `javap`, `jstat`) com flags reais conferidas; outputs ilustrativos em ` ```text `. Framing neutro ("padrão observado em serviços enterprise", "caso típico de JVM containerizada", hipotético explícito `// hipotético:`). **NUNCA** "no meu projeto"; **NUNCA** `Patient`/`getSpecialty`. Domínios neutros: `Order`, `Customer`, `Product`.
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada armadilha: `### (N) Título` + descrição + exemplo curto (código/comando/log) demonstrando o problema + fix em 1 linha.
7. `## Em entrevista` — subheading `### Frase pronta (inglês)` com frase de **3+ sentenças** (trade-off + decisão + caveat) + sub-bloco "Vocabulário" com **6+ termos PT→EN** traduzidos.
8. `## Veja também` — wikilinks SEM backticks. Sempre inclui: notas relacionadas do galho + `[[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro (MOC do galho)]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando o conceito conectar) Galho 1 / Galho 2 / Galho 4 + verbetes do Dicionário relevantes. **Sem âncoras same-file `[[#Heading]]`.**
9. `## Referências` — docs oficiais (Oracle JVM Guide, GC Tuning Guide, man pages, dev.java, Javadoc) + JEPs quando pertinentes (linkar openjdk.org como referência é ok; **verificar conteúdo** via fallback).

**Tamanho:** 200-500 linhas (notas Magus densas até 700).

**Restrições absolutas** (qualquer violação reprova a nota):
- **Tronco é matéria-prima desatualizada, não cópia.** A tabela de GC do tronco cita CMS sem nota de remoção e ZGC "Java 15" sem generational — reconstruir com fonte. **Toda afirmação version-specific (JEP/flag/default) é verificada via WebFetch antes de afirmar** — nada de "de memória". Toda nota tem "Referências".
- Sem fabricação de experiência pessoal. Exemplos: `Order`, `Customer`, `Product`, ou `// hipotético: ...`. NUNCA `josenaldo`/caminhos pessoais/casos vividos/`Patient`.
- **Não re-explicar o que é de outro galho.** JMM/happens-before/volatile → Galho 4 nota 11 (linkar). Virtual Threads/Loom → Galho 4 nota 12 (linkar). Lambdas → Galho 2 nota 04 (linkar). Boxing/streams primitivos → Galho 2 nota 09 (linkar). Generics/records → Galho 1 (linkar). GraalVM native image / profiling de aplicação → Galho 17, texto "(planejado)" **sem wikilink**.
- Comparações justas ("quando X vence" E "quando Y vence") — G1 vs ZGC vs Parallel, JIT vs AOT, jcmd vs ferramentas legadas, JFR vs APM.
- Code fences: ` ```java ` pra código, ` ```bash ` pra comandos, ` ```text ` pra output/log. Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (nunca `git add -A` — bot de backup do vault roda em timer); 1 commit por nota; **direto na `main`**; **sem push**; **sem deploy**.

**Material de origem:** tronco `03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md` (seção `## JVM (Java Virtual Machine)`). Spec de referência: `docs/superpowers/specs/2026-06-05-java-galho-03-jvm-design.md` §5. Template de qualidade: notas dos Galhos 1/2/4/5 em `03-Dominios/Tecnologia/Java/`.

**Modelo por nota:** sonnet por padrão; **opus** nas notas **06** (Coletores), **07** (JIT), **11** (Tuning) e **14** (capstone) — as mais densas/version-sensitive.

**Fontes oficiais (base por área):**
- GC Tuning Guide (Java 21): `https://docs.oracle.com/en/java/javase/21/gctuning/`
- JVM Guide (Java 21): `https://docs.oracle.com/en/java/javase/21/vm/`
- Troubleshooting Guide (Java 21): `https://docs.oracle.com/en/java/javase/21/troubleshoot/`
- Man pages (`java`, `javap`, `jcmd`, `jstat`, `jmap`, `jstack`, `jlink`): `https://docs.oracle.com/en/java/javase/21/docs/specs/man/`
- JFR: `https://docs.oracle.com/en/java/javase/21/jfapi/` + Javadoc `jdk.jfr`
- dev.java: `https://dev.java/learn/`
- Javadoc Java 21: `https://docs.oracle.com/en/java/javase/21/docs/api/`
- JEPs (158, 248, 261, 318, 328, 349, 363, 377, 379, 404, 439, 483, 490): `https://openjdk.org/jeps/<n>` — **costuma dar 403 no WebFetch**; usar como referência citada e verificar conteúdo via Oracle docs/dev.java/release notes (`https://www.oracle.com/java/technologies/javase/<ver>-relnote-issues.html` ou `https://jdk.java.net/<ver>/release-notes`).

---

## Task 0: Pré-flight — pasta e confirmação do terreno (tronco já lido na brainstorming)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/` (pasta)

- [ ] **Step 1: Confirmar que está na `main`**

```bash
git branch --show-current
```
Expected: `main`. (Galho 3 é executado direto na main — [[feedback_galhos_direto_main]]. NÃO criar branch.)

- [ ] **Step 2: Criar a pasta do galho**

```bash
mkdir -p "03-Dominios/Tecnologia/Java/JVM"
```

- [ ] **Step 3: Reconfirmar a seção do tronco a podar (matéria-prima)**

```bash
grep -n "^## JVM (Java Virtual Machine)" "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md"
grep -n "Migra em galho futuro (Galho 3" "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md"
grep -nE "^## |^### " "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md" | head -20
```
Expected: a seção existe, marcada `[!info] Migra em galho futuro (Galho 3 ...)`, com subseções `### Pipeline de compilação e execução`, `### Bytecode — uma olhada`, `### Memory areas`, `### Garbage Collection`, `### Como escolher GC`, `### JIT Compiler`, `### Classloader`, `### Project Loom e Virtual Threads`. (Já confirmado na brainstorming; reconfirmar pois linhas podem ter mudado.) **NÃO** tocar `## Concorrência (visão geral)` (dívida Galho 4).

- [ ] **Step 4: Confirmar os títulos exatos das notas vizinhas que serão linkadas**

```bash
ls "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/" | grep -E "^(11|12) "
ls "03-Dominios/Tecnologia/Java/Collections e Streams/" | grep -E "^(04|09) "
```
Expected: confirmar filenames exatos de Galho 4 notas 11 (Java Memory Model) e 12 (Virtual Threads) e Galho 2 notas 04 (Lambdas) e 09 (Streams primitivos). **Anotar os títulos exatos** — os wikilinks das notas deste galho usam esses nomes (o plano abaixo assume `11 - Java Memory Model em profundidade` e ajusta se divergir).

- [ ] **Step 5: Localizar a dívida reversa ("Galho 3 planejado" nos galhos fechados)**

```bash
grep -rn "Galho 3" "03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/" "03-Dominios/Tecnologia/Java/Collections e Streams/" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/" "03-Dominios/Tecnologia/Java/Swing/" "03-Dominios/Tecnologia/Java/index.md" | grep -vi "galho 3 (jvm" | cat
grep -rni "JVM.*planejado\|planejado.*JVM" "03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/" "03-Dominios/Tecnologia/Java/Collections e Streams/" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/" "03-Dominios/Tecnologia/Java/Swing/"
```
Anotar **todas** as ocorrências de ponteiro textual "Galho 3 (JVM) planejado" — alvos da Task 19. (A linha 27 do MOC central é da Task 17, não desta lista.)

- [ ] **Step 6: Fixar versões assumidas**

Baseline: **Java 21 LTS** (Javadoc/guides) com fatos de releases posteriores verificados individualmente. Lista de verificação version-specific (WebFetch na execução, nota a nota): G1 default (JEP 248, Java 9), unified logging (JEP 158, Java 9), JPMS (JEP 261, Java 9), Epsilon (JEP 318, Java 11), JFR OSS (JEP 328, Java 11), CMS removido (JEP 363, Java 14), JFR streaming (JEP 349, Java 14), ZGC production (JEP 377, Java 15), Shenandoah (JEP 379, Java 15), **ZGC generational (JEP 439, Java 21)**, ZGC non-gen deprecado/removido (JEP 490 — confirmar versão), Shenandoah generational (JEP 404 — confirmar status/versão), Project Leyden/AOT (JEP 483, Java 24 + JEPs subsequentes — confirmar status, hedge se preview).

- [ ] **Step 7: Sem commit** (task de preparação).

---

## Fase INICIADO (notas 01-05)

### Task 1: Nota 01 — A JVM — o que é e o pipeline de execução

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/01 - A JVM — o que é e o pipeline de execução.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://dev.java/learn/getting-started/` (seção "what is the JVM") e/ou `https://docs.oracle.com/en/java/javase/21/vm/java-virtual-machine-technology-overview.html` (JVM Guide overview). Confirmar: papel do `javac`, bytecode independente de plataforma, interpretação + JIT no HotSpot, distinção JVM/JRE/JDK.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, jvm, iniciado, runtime]`, aliases `["JVM", "Java Virtual Machine", "Pipeline de execução Java"]`.

Conteúdo:
- TL;DR: a JVM é o runtime que executa bytecode — interpreta primeiro, compila o código quente via JIT; é o que torna Java portátil ("write once, run anywhere") e o que diferencia senior de junior é entendê-la, não usá-la como caixa preta.
- `## O que é` — JVM (executa bytecode) vs JRE (JVM + bibliotecas) vs JDK (JRE + ferramentas de dev); HotSpot como implementação de referência (OpenJDK); menção a outras (Eclipse OpenJ9, GraalVM — texto, sem aprofundar; native image é "Galho 17, planejado", sem wikilink).
- `## Por que importa` — entrevistas de senior cobram o pipeline; debugging de produção exige saber onde o código "vive" (interpretado? compilado? em que área de memória?).
- `## Como funciona` — H3s: "De `.java` a `.class` (`javac` e o bytecode)", "Carga e verificação (classloader + bytecode verifier — visão geral, detalhe na nota 05)", "Interpretação e JIT (visão geral — detalhe na nota 07)", "GC como serviço do runtime (visão geral — detalhe nas notas 03/06)". Diagrama em ` ```text ` do pipeline (modernizar o do tronco).
- `## Na prática` — compilar e rodar um `Order.java` (`javac` → `java`); mostrar `java -version` e o que revela (vendor, versão, modo); `javap -c` teaser de 3 linhas (ponte pra nota 04).
- `## Armadilhas` — ≥2: (1) "Java é interpretado, logo lento" (meia-verdade — JIT compila código quente pra nativo) → entender tiered compilation (nota 07); (2) assumir que toda JVM se comporta igual (vendors/versões divergem em defaults de GC, flags) → conferir com `java -XX:+PrintFlagsFinal`. Exemplo + fix.
- `## Em entrevista` (`### Frase pronta (inglês)`) + `## Veja também` (02, 03, 04, 05, 07, MOC galho, MOC central, verbetes `bytecode`/`JIT (C1 / C2)`) + `## Referências`.

Tamanho: 220-340 linhas (abertura).

- [ ] **Step 3: Verificar**

```bash
grep -cE "^## (O que é|Por que importa|Como funciona|Na prática|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Tecnologia/Java/JVM/01 - A JVM — o que é e o pipeline de execução.md"
grep -E "javac|bytecode|HotSpot|JIT|JRE|JDK" "03-Dominios/Tecnologia/Java/JVM/01 - A JVM — o que é e o pipeline de execução.md" | head
```
Expected: ≥7 seções; cobre pipeline + distinções.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/01 - A JVM — o que é e o pipeline de execução.md"
git commit -m "feat(java): galho 3 nota 01 — a JVM e o pipeline de execução"
```

---

### Task 2: Nota 02 — Áreas de memória de runtime

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/02 - Áreas de memória de runtime.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/en/java/javase/21/gctuning/generations.html` (Generations) + JVM Guide. Confirmar: Eden/Survivor/Old, Metaspace (substituiu PermGen no Java 8), humongous objects no G1, variantes de `OutOfMemoryError` (heap space, Metaspace, native) via Troubleshooting Guide (`https://docs.oracle.com/en/java/javase/21/troubleshoot/troubleshooting-memory-leaks.html` ou página de OOM).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, jvm, iniciado, memoria, heap]`, aliases `["Heap e Metaspace", "Memória da JVM", "Áreas de memória"]`.

Conteúdo:
- `## O que é` — o mapa de memória do processo JVM: heap (objetos, compartilhada), Metaspace (metadata de classes, nativa), stacks (por thread), PC register, native method stack, code cache (JIT).
- `## Por que importa` — cada `OutOfMemoryError` tem endereço: saber a área errada acelera o diagnóstico; entrevista cobra heap vs stack e Metaspace vs PermGen.
- `## Como funciona` — H3s: "Heap: Young (Eden + S0/S1) e Old/Tenured (+ humongous no G1)", "Metaspace (Java 8+; por que PermGen morreu)", "Stack por thread (frames, variáveis locais, operandos; `-Xss`)", "PC register e native method stack", "Code cache (onde o JIT guarda código nativo)". Diagrama ` ```text ` modernizado do tronco. **Fronteira:** alocação/layout é daqui; *visibilidade* de escritas entre threads é [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade|Java Memory Model]] (Galho 4) — citar e linkar, sem re-explicar happens-before.
- `## Na prática` — mapa de erros: `OutOfMemoryError: Java heap space` / `: Metaspace` / `: unable to create native thread` vs `StackOverflowError`; flags de dimensionamento (`-Xms`/`-Xmx`/`-Xss`/`-XX:MaxMetaspaceSize`) com exemplo de linha de comando.
- `## Armadilhas` — ≥2: (1) achar que `-Xmx` limita a memória total do processo (Metaspace, stacks, code cache, buffers nativos ficam fora) → dimensionar o pod/host pelo RSS, não pelo `-Xmx`; (2) `OutOfMemoryError: Metaspace` por leak de classloader em redeploy (ponte pra nota 05) → heap dump e analisar classloaders; (3) recursão profunda → `StackOverflowError` (e quando ajustar `-Xss` vs reescrever iterativo). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 03, 05, 09, 12, MOC, central, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade|Java Memory Model]]`, verbetes `heap`/`Metaspace`/`stack frame`) + `## Referências`.

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "Eden|Survivor|Metaspace|PermGen|StackOverflowError|OutOfMemoryError|code cache" "03-Dominios/Tecnologia/Java/JVM/02 - Áreas de memória de runtime.md" | head
grep -c "Java Memory Model" "03-Dominios/Tecnologia/Java/JVM/02 - Áreas de memória de runtime.md"
```
Expected: cobre as áreas + mapa de erros; link pro JMM presente (≥1).

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/02 - Áreas de memória de runtime.md"
git commit -m "feat(java): galho 3 nota 02 — áreas de memória de runtime"
```

---

### Task 3: Nota 03 — Garbage Collection — o conceito

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/03 - Garbage Collection — o conceito.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/en/java/javase/21/gctuning/garbage-collector-implementation.html` (GC implementation) + `https://docs.oracle.com/en/java/javase/21/gctuning/introduction-garbage-collection-tuning.html`. Confirmar: reachability/GC roots, generational hypothesis, minor/major/mixed, stop-the-world. Para references API: Javadoc `java.lang.ref` (Java 21).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, jvm, iniciado, gc]`, aliases `["Garbage Collection", "GC", "Coleta de lixo"]`.

Conteúdo:
- `## O que é` — GC = liberar automaticamente memória de objetos **inalcançáveis** a partir dos GC roots (stacks, statics, JNI refs); não é "deletar o que você não usa mais", é "coletar o que ninguém alcança".
- `## Por que importa` — GC é o trade-off central do runtime (pausa vs throughput vs memória); senior precisa do vocabulário (minor/major, STW, promoção) pra ler logs e conversar tuning.
- `## Como funciona` — H3s: "Reachability e GC roots", "A weak generational hypothesis (a maioria dos objetos morre jovem)", "Minor, major e mixed collections (promoção, tenuring)", "Stop-the-world e safepoints", "Soft/weak/phantom references (visão geral — quando aparecem em cache/cleanup)". **Sem catálogo de coletores** (nota 06).
- `## Na prática` — demonstrar promoção conceitualmente (objeto que sobrevive N minors vai pra Old); `System.gc()` é *pedido*, não ordem (e por que desabilitam com `-XX:+DisableExplicitGC`); teaser de 5 linhas de um GC log (ponte pra nota 10).
- `## Armadilhas` — ≥2: (1) chamar `System.gc()` em produção (Full GC STW na cara do usuário) → deixar o coletor decidir; (2) cache estático sem bound segura referências → "leak na frente do GC" (o GC não coleta o que você ainda alcança) → bound/expiração ou referência fraca; (3) confundir GC com gestão de recursos nativos (files/sockets não são coletados no close) → try-with-resources (linka Galho 1, [[10 - Exceções e tratamento de erros]]). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (02, 06, 10, 11, MOC, central, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros|Exceções e tratamento de erros]]`, verbetes `GC roots / reachability`/`stop-the-world`/`weak generational hypothesis`/`safepoint`) + `## Referências`.

Tamanho: 260-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "reachab|GC roots|generational|minor|major|stop-the-world|safepoint|System.gc" "03-Dominios/Tecnologia/Java/JVM/03 - Garbage Collection — o conceito.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/03 - Garbage Collection — o conceito.md"
git commit -m "feat(java): galho 3 nota 03 — garbage collection, o conceito"
```

---

### Task 4: Nota 04 — Bytecode por dentro — anatomia e javap

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/04 - Bytecode por dentro — anatomia e javap.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/en/java/javase/21/docs/specs/man/javap.html` (man page do javap). Confirmar flags (`-c`, `-v`, `-p`) e o formato de saída. Para a estrutura do `.class` e instruções: JVM Spec capítulo 4/6 como referência citada (`https://docs.oracle.com/javase/specs/jvms/se21/html/`) — verificar o que for afirmado.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, jvm, iniciado, bytecode]`, aliases `["Bytecode", "javap", "Instruções da JVM"]`.

Conteúdo:
- `## O que é` — bytecode = o instruction set portátil da JVM; o `.class` é um contêiner binário (magic number `CAFEBABE`, constant pool, métodos, atributos).
- `## Por que importa` — ler bytecode desmistifica a linguagem (o que o compilador gera de verdade pra um record, um lambda, um switch) e é ferramenta de debugging de último nível; entrevista usa pra sondar profundidade.
- `## Como funciona` — H3s: "Anatomia do `.class` (constant pool, métodos, atributos)", "Máquina de pilha (stack-based vs register-based; frame = locals + operand stack)", "Famílias de instrução (`iload`/`istore`/`iadd`, `invokevirtual`/`invokestatic`/`invokespecial`/`invokeinterface`/`invokedynamic`, `new`/`getfield`)", "`invokedynamic` (call site dinâmico; é como lambdas são implementadas — linka [[04 - Lambdas e interfaces funcionais]] do Galho 2, sem re-explicar)", "Inspecionando com `javap -c -v`".
- `## Na prática` — `javap -c` de um método `sum(int, int)` de `Order` com output ` ```text ` comentado linha a linha; `javap -v` mostrando constant pool (trecho); o que um record gera (`javap` enxuto — linka Galho 1 [[13 - Records e record patterns]]).
- `## Armadilhas` — ≥2: (1) "otimizar" lendo bytecode (o JIT reescreve tudo — bytecode ≠ o que executa) → medir com JMH (nota 07); (2) confundir versão de bytecode (`major version`) com versão da linguagem → `javac --release N` e o erro `UnsupportedClassVersionError`; (3) assumir 1 linha de código = 1 instrução (um `a + b` de String vira invokedynamic/StringConcatFactory). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 05, 07, MOC, central, `[[03-Dominios/Tecnologia/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais]]`, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/13 - Records e record patterns|Records]]`, verbetes `bytecode`) + `## Referências`.

Tamanho: 260-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "javap|constant pool|CAFEBABE|invokedynamic|invokevirtual|stack-based|operand" "03-Dominios/Tecnologia/Java/JVM/04 - Bytecode por dentro — anatomia e javap.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/04 - Bytecode por dentro — anatomia e javap.md"
git commit -m "feat(java): galho 3 nota 04 — bytecode por dentro (anatomia e javap)"
```

---

### Task 5: Nota 05 — Classloading e o delegation model

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/05 - Classloading e o delegation model.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch Javadoc `java.lang.ClassLoader` (Java 21) — descreve a hierarquia (bootstrap/platform/application desde Java 9) e o delegation model. Complementar com `https://docs.oracle.com/en/java/javase/21/vm/class-data-sharing.html` se citar CDS de passagem (dono: nota 14).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, jvm, iniciado, classloading]`, aliases `["Classloader", "Parent delegation", "Carregamento de classes"]`.

Conteúdo:
- `## O que é` — classloading = trazer `.class` pra dentro da JVM **sob demanda**, em três fases: loading → linking (verification, preparation, resolution) → initialization (static init).
- `## Por que importa` — app servers, plugins e frameworks vivem de classloaders; metade dos erros "estranhos" de deploy (`NoClassDefFoundError`, `ClassCastException` impossível) é classloading.
- `## Como funciona` — H3s: "As três fases (loading/linking/initialization — o que acontece em cada)", "A hierarquia (Bootstrap → Platform → Application; o que cada um carrega desde Java 9)", "Parent delegation (pedido sobe antes de carregar; por que protege `java.lang.String`)", "Custom classloaders (isolamento de WARs, plugins, hot reload)", "Identidade de classe = classe + classloader".
- `## Na prática` — `Class.forName` vs `ClassLoader.loadClass`; inspecionar `Order.class.getClassLoader()` e a cadeia de parents (snippet + output ` ```text `); cenário hipotético de plugin com classloader próprio.
- `## Armadilhas` — ≥2: (1) a mesma classe carregada por 2 classloaders **não** é a mesma classe → `ClassCastException` "impossível" em app server/plugin → garantir que a classe compartilhada vem do parent; (2) leak de classloader em redeploy (static/ThreadLocal segura referência → Metaspace OOM — linka nota 02) → limpar referências no undeploy; (3) `ClassNotFoundException` (pedido explícito falhou) vs `NoClassDefFoundError` (estava no compile, sumiu no runtime, ou static init quebrou antes). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 02, 04, 08, MOC, central, verbetes `classloader (parent delegation)`) + `## Referências`.

Tamanho: 260-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "Bootstrap|Platform|Application|delegation|loading|linking|initialization|NoClassDefFoundError|ClassNotFoundException" "03-Dominios/Tecnologia/Java/JVM/05 - Classloading e o delegation model.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/05 - Classloading e o delegation model.md"
git commit -m "feat(java): galho 3 nota 05 — classloading e o delegation model"
```

---

## Fase ADEPTO (notas 06-10)

### Task 6: Nota 06 — Os coletores do HotSpot  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/06 - Os coletores do HotSpot.md`

- [ ] **Step 1: Pesquisar fonte — VERIFICAÇÃO OBRIGATÓRIA (campo minado de versões)**

WebFetch `https://docs.oracle.com/en/java/javase/21/gctuning/available-collectors.html` + páginas de G1 (`garbage-first-g1-garbage-collector1.html`) e ZGC (`z-garbage-collector.html`) do GC Tuning Guide. **Confirmar cada fato de versão** (openjdk.org dá 403 — fallback via Oracle docs/release notes): G1 default (JEP 248, Java 9); ZGC production (JEP 377, Java 15); **ZGC generational (JEP 439, Java 21)** e o destino do modo non-generational (JEP 490 — deprecação/remoção, confirmar versão exata); Shenandoah production (JEP 379, Java 15) e generational (JEP 404 — confirmar status: experimental? em que versão?); Epsilon (JEP 318, Java 11); CMS **removido** (JEP 363, Java 14). **Não afirmar sem fonte; hedge no que for experimental.**

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, jvm, adepto, gc]`, aliases `["Coletores de GC", "G1", "ZGC", "Shenandoah"]`.

Conteúdo:
- `## O que é` — o catálogo de coletores do HotSpot e o trade-off de cada um (pausa × throughput × footprint × heap size).
- `## Por que importa` — a escolha de coletor é decisão de arquitetura observável (p99, custo de CPU/RAM); a tabela mental desatualizada (CMS! ZGC sem generational!) reprova em entrevista.
- `## Como funciona` — H3s: "Serial e Parallel (os geracionais clássicos; throughput-first)", "G1 — o default (regions, pause time target, mixed collections, humongous)", "ZGC — low-latency (concurrent, pausas sub-ms; **generational desde Java 21/JEP 439**; non-gen deprecado/removido — versão conforme verificado)", "Shenandoah (concurrent, perfil similar ao ZGC; status generational conforme verificado)", "Epsilon (no-op; testes/benchmark)", "CMS — nota histórica (removido no Java 14/JEP 363; ainda assombra blogs)". Tabela comparativa final (colunas: coletor / desde / pausas / throughput / heap / uso ideal) **reconstruída com os fatos verificados** — não copiar a do tronco.
- `## Na prática` — flags de seleção (`-XX:+UseG1GC`, `-XX:+UseZGC`, `-XX:+UseParallelGC`, `-XX:+UseSerialGC`, `-XX:+UseEpsilonGC`); escolha de primeira ordem comentada: default → G1; p99 crítico/heap grande → ZGC; batch throughput → Parallel; heap < ~512MB/sidecar → Serial.
- `## Armadilhas` — ≥3: (1) copiar escolha/flags de blog antigo (CMS, `-XX:+UseConcMarkSweepGC` nem existe mais — JVM não sobe) → conferir release notes da sua versão; (2) ligar ZGC em heap minúsculo esperando milagre (low-pause cobra em CPU/footprint; G1 pode ser melhor) → medir com a carga real; (3) ignorar que "pausa < 1ms" não é "GC grátis" (trabalho concorrente compete com a aplicação por CPU) → dimensionar cores. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (03, 09, 10, 11, 14, MOC, central, verbetes `G1 GC`/`ZGC (generational)`/`Shenandoah`/`Epsilon GC`) + `## Referências` (GC Tuning Guide + JEPs citados).

Tamanho: 340-520 linhas (densa; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "G1|ZGC|Shenandoah|Epsilon|Serial|Parallel|JEP (248|318|363|377|379|404|439|490)" "03-Dominios/Tecnologia/Java/JVM/06 - Os coletores do HotSpot.md" | head -20
grep -i "CMS" "03-Dominios/Tecnologia/Java/JVM/06 - Os coletores do HotSpot.md" | head -3
```
Expected: cobre todos os coletores com JEPs/versões citados; CMS só como nota histórica de remoção.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/06 - Os coletores do HotSpot.md"
git commit -m "feat(java): galho 3 nota 06 — os coletores do HotSpot"
```

---

### Task 7: Nota 07 — JIT — C1, C2 e tiered compilation  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/07 - JIT — C1, C2 e tiered compilation.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch `https://docs.oracle.com/en/java/javase/21/vm/java-hotspot-virtual-machine-performance-enhancements.html` (JVM Guide — performance/compiler) e/ou dev.java sobre JIT. Confirmar: tiered compilation default, papéis de C1/C2, otimizações (inlining, escape analysis), deoptimization, code cache. JMH: `https://github.com/openjdk/jmh` (README) como referência da ferramenta.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, jvm, adepto, jit]`, aliases `["JIT", "Tiered compilation", "C1 C2", "Escape analysis"]`.

Conteúdo:
- `## O que é` — JIT = compilar bytecode pra código nativo **em runtime**, guiado por profiling real; o HotSpot combina interpretador + C1 (rápido, leve) + C2 (lento, agressivo).
- `## Por que importa` — explica warmup, por que benchmark ingênuo mente, e por que "código quente" muda de performance sozinho; entrevista de senior adora deoptimization.
- `## Como funciona` — H3s: "Tiered compilation (interpretador → C1 com profiling → C2; níveis e promoção por contadores)", "O que o C2 faz (inlining — a otimização-mãe; escape analysis e alocação que desaparece; lock elision; dead code elimination; loop unrolling)", "Deoptimization (especulação que falhou → volta pro interpretador; por que ainda assim compensa)", "Warmup (por que os primeiros N requests são lentos)", "Code cache (onde o nativo mora; o que acontece se enche)". Escape analysis/boxing → linka [[03-Dominios/Tecnologia/Java/Collections e Streams/09 - Streams primitivos|Streams primitivos]] (Galho 2). Lock elision menciona `synchronized` → linka Galho 4 índice, sem re-explicar locks.
- `## Na prática` — flags de observação (`-XX:+PrintCompilation` com output ` ```text ` comentado); por que medir com JMH (dead code elimination engole benchmark ingênuo — exemplo do erro e do fix com Blackhole, marcado `// hipotético:` se ilustrativo); menção honesta: não decorar níveis numéricos, entender o fluxo.
- `## Armadilhas` — ≥3: (1) microbenchmark sem JMH (JIT elimina o código "não usado" e o loop mede nada) → JMH com Blackhole; (2) medir performance durante warmup (números do interpretador/C1) → aquecer antes de medir; (3) concluir que `synchronized` "é lento" sem considerar lock elision/biased history (o JIT remove lock não-contendido) → medir o caso real; (4) `-Xint`/`-Xcomp` em produção ("forçar" o modo quebra o equilíbrio tiered). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 04, 06, 14, MOC, central, `[[03-Dominios/Tecnologia/Java/Collections e Streams/09 - Streams primitivos|Streams primitivos]]`, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]`, verbetes `tiered compilation`/`inlining (JIT)`/`escape analysis`/`deoptimization`/`code cache`) + `## Referências`.

Tamanho: 320-500 linhas (densa; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "C1|C2|tiered|inlining|escape analysis|deoptimiz|warmup|JMH|code cache|PrintCompilation" "03-Dominios/Tecnologia/Java/JVM/07 - JIT — C1, C2 e tiered compilation.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/07 - JIT — C1, C2 e tiered compilation.md"
git commit -m "feat(java): galho 3 nota 07 — JIT (C1, C2 e tiered compilation)"
```

---

### Task 8: Nota 08 — JPMS — o sistema de módulos

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/08 - JPMS — o sistema de módulos.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://dev.java/learn/modules/intro/` (série Modules do dev.java). Confirmar: sintaxe de `module-info.java` (`requires`/`requires transitive`/`exports`/`exports ... to`/`opens`/`uses`/`provides ... with`), unnamed/automatic modules, `--add-opens`/`--add-exports`. JEP 261 (Java 9) como referência citada; a história do `--illegal-access` (permit → deny, JEP 403 strong encapsulation Java 17) — confirmar via dev.java/release notes.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, jvm, adepto, jpms, modulos]`, aliases `["JPMS", "module-info", "Sistema de módulos", "Java Platform Module System"]`.

Conteúdo:
- `## O que é` — JPMS (Java 9, JEP 261): módulos com dependências (`requires`) e API pública (`exports`) explícitas, checadas em compile e runtime; o fim do classpath como saco sem fundo (mas ele convive — unnamed module).
- `## Por que importa` — o próprio JDK é modular (afeta todo mundo via strong encapsulation: o `--add-opens` que seu framework pede); módulos aparecem em migração de app legado e em entrevista "Java 9+".
- `## Como funciona` — H3s: "`module-info.java` (requires/exports e variantes `transitive`/`exports ... to`)", "`opens` e reflection (por que Hibernate/Jackson precisam)", "Services (`uses`/`provides ... with` — ServiceLoader de primeira classe)", "Convivendo com o classpath (unnamed module, automatic modules, `Automatic-Module-Name`)", "Strong encapsulation (da era `--illegal-access` ao deny por default; `--add-opens`/`--add-exports` como válvulas)", "`jlink` (runtime enxuto sob medida — menção como payoff)".
- `## Na prática` — um `module-info.java` mínimo de app `com.example.orders` (requires/exports/opens pra framework hipotético); o erro clássico `InaccessibleObjectException` e o fix com `opens`/`--add-opens` (output ` ```text `).
- `## Armadilhas` — ≥3: (1) esquecer `opens` pro pacote que o framework reflete (quebra em runtime com `InaccessibleObjectException`) → `opens com.example.orders.model;`; (2) depender de automatic module sem `Automatic-Module-Name` no manifest (nome derivado do filename — instável) → pedir/esperar o atributo, ou ficar no classpath; (3) split packages (mesmo pacote em 2 módulos — erro de resolução) → reempacotar; (4) achar que classpath morreu (a maioria das apps Spring roda no classpath até hoje — módulos são opt-in). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 05, 14, MOC, central, verbetes `JPMS (module-info)`) + `## Referências` (dev.java, JEP 261).

Tamanho: 300-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "module-info|requires|exports|opens|transitive|automatic|jlink|add-opens|InaccessibleObjectException" "03-Dominios/Tecnologia/Java/JVM/08 - JPMS — o sistema de módulos.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/08 - JPMS — o sistema de módulos.md"
git commit -m "feat(java): galho 3 nota 08 — JPMS, o sistema de módulos"
```

---

### Task 9: Nota 09 — Flags, ergonomics e a JVM em containers

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/09 - Flags, ergonomics e a JVM em containers.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html` (man page do `java` — seções de -X/-XX e ergonomics) + GC Tuning Guide capítulo ergonomics (`https://docs.oracle.com/en/java/javase/21/gctuning/ergonomics.html`). **Confirmar container awareness**: `-XX:+UseContainerSupport` (default on em Linux), `MaxRAMPercentage`/`InitialRAMPercentage` e o default de heap (~25% da RAM disponível) — via man page/Oracle docs.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, jvm, adepto, tuning, containers]`, aliases `["Flags da JVM", "JVM em containers", "Ergonomics", "MaxRAMPercentage"]`.

Conteúdo:
- `## O que é` — o painel de controle da JVM: flags `-X` (estáveis básicas) e `-XX` (avançadas; boolean `+/-` vs valor `=`); ergonomics = os defaults que a JVM escolhe sozinha olhando o hardware (ou o container).
- `## Por que importa` — 90% da operação cotidiana da JVM em produção é isto: dimensionar heap num pod, entender por que o default fez X, descobrir a flag efetiva. Errar aqui = OOMKilled.
- `## Como funciona` — H3s: "Anatomia de flag (`-Xmx4g` vs `-XX:MaxHeapSize=4g`; `-XX:+Flag` vs `-XX:Flag=valor`)", "Dimensionamento de memória (`-Xms`/`-Xmx`, `-Xss`, `MetaspaceSize`/`MaxMetaspaceSize`)", "Ergonomics (como a JVM escolhe coletor/heap/threads pelo hardware)", "Container awareness (cgroups; `UseContainerSupport`; `MaxRAMPercentage`/`InitialRAMPercentage`; o default de ~25% e por que ele é conservador)", "Descobrindo a verdade (`-XX:+PrintFlagsFinal`, `java -XX:+PrintCommandLineFlags -version`)".
- `## Na prática` — pod hipotético com `limits.memory: 2Gi`: comparar `-Xmx1536m` fixo vs `-XX:MaxRAMPercentage=75` (e por que percentual escala com o limite); ver o heap efetivo com `jcmd <pid> VM.flags` / `PrintFlagsFinal | grep MaxHeapSize` (output ` ```text `).
- `## Armadilhas` — ≥3: (1) `-Xmx` = limite do pod (sem folga pra Metaspace/stacks/nativo) → OOMKilled pelo kernel (exit 137), **não** OOM da JVM → deixar 25-30% de folga; (2) confiar no default de 25% em container dedicado (subutiliza 3/4 da RAM paga) → `MaxRAMPercentage` explícito; (3) copiar flag de outra versão (flag removida → JVM nem sobe; `Unrecognized VM option`) → validar com `PrintFlagsFinal` na versão alvo. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (02, 06, 10, 11, 12, MOC, central, verbetes `ergonomics (JVM)`) + `## Referências` (man page java, GC Tuning ergonomics).

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "Xmx|Xms|MaxRAMPercentage|UseContainerSupport|PrintFlagsFinal|ergonomics|cgroup|OOMKilled" "03-Dominios/Tecnologia/Java/JVM/09 - Flags, ergonomics e a JVM em containers.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/09 - Flags, ergonomics e a JVM em containers.md"
git commit -m "feat(java): galho 3 nota 09 — flags, ergonomics e a JVM em containers"
```

---

### Task 10: Nota 10 — GC logs — unified logging e leitura

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/10 - GC logs — unified logging e leitura.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch man page do `java` (seção `-Xlog` — `https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html`) pra sintaxe de unified logging (JEP 158, Java 9 — confirmar via doc). Confirmar a forma `-Xlog:gc*:file=gc.log:time,uptime,level,tags` e o formato de saída do G1.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, jvm, adepto, gc, diagnostico]`, aliases `["GC logs", "Unified logging", "-Xlog"]`.

Conteúdo:
- `## O que é` — unified logging (Java 9, JEP 158): um sistema único de log da JVM (`-Xlog:seletor:output:decoradores`); GC log = a caixa-preta do coletor, custo ~zero, valor imenso.
- `## Por que importa` — sem GC log não há diagnóstico de pausa nem tuning honesto (nota 11 depende desta); ler um log de G1 é hard skill de senior.
- `## Como funciona` — H3s: "A sintaxe do `-Xlog` (seletores `gc*`, níveis, decoradores, outputs, rotação)", "Anatomia de um log do G1 (Pause Young, Mixed, fases concorrentes, to-space exhausted)", "Anatomia de um log do ZGC (fases concorrentes, pausas sub-ms)", "O que olhar primeiro (frequência de pausas, duração p99 — não média, taxa de promoção, humongous allocations, **Full GC = red flag no G1/ZGC**)", "Da era antiga pra cá (`-XX:+PrintGCDetails`/`-Xloggc` removidos/migrados no Java 9+)".
- `## Na prática` — linha recomendada de produção (`-Xlog:gc*:file=gc.log:time,uptime,level,tags:filecount=5,filesize=20m`); trecho de log G1 real-formato em ` ```text ` anotado linha a linha (pause young, heap antes→depois, tempo); trecho com to-space exhausted e o que significa.
- `## Armadilhas` — ≥3: (1) rodar produção **sem** GC log ("overhead" é mito — o custo é ~zero e sem ele o incidente vira adivinhação) → ligar sempre, com rotação; (2) olhar pausa média e ignorar cauda/Full GC (a média esconde o p99.9 que derruba o SLA) → percentis + procurar Full GC; (3) usar `-XX:+PrintGCDetails` (pré-9) em JVM moderna (Unrecognized option ou alias deprecation) → migrar pra `-Xlog`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (03, 06, 09, 11, 12, 13, MOC, central, verbetes `unified logging (-Xlog)`) + `## Referências`.

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "Xlog|unified|Pause Young|Mixed|to-space|Full GC|decorador|filecount" "03-Dominios/Tecnologia/Java/JVM/10 - GC logs — unified logging e leitura.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/10 - GC logs — unified logging e leitura.md"
git commit -m "feat(java): galho 3 nota 10 — GC logs (unified logging e leitura)"
```

---

## Fase MAGUS (notas 11-14)

### Task 11: Nota 11 — Tuning de GC — metodologia e prática  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/11 - Tuning de GC — metodologia e prática.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch GC Tuning Guide: `https://docs.oracle.com/en/java/javase/21/gctuning/factors-affecting-garbage-collection-performance.html` + capítulo de tuning do G1 (`garbage-first-garbage-collector-tuning.html`) + ZGC. Confirmar flags citadas: `MaxGCPauseMillis`, `G1HeapRegionSize`, `InitiatingHeapOccupancyPercent`, `SoftMaxHeapSize` (ZGC), `GCTimeRatio` (Parallel). **Nenhuma flag sem fonte.**

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, jvm, magus, gc, tuning]`, aliases `["Tuning de GC", "GC tuning", "MaxGCPauseMillis"]`.

Conteúdo:
- `## O que é` — tuning de GC = mover o ponto no triângulo **latência × throughput × footprint** (escolha 2) com base em medição — não colecionar flags.
- `## Por que importa` — separa senior de cargo cult: a maioria dos "tunings" em produção é flag copiada sem baseline; saber a metodologia vale mais que decorar flags.
- `## Como funciona` — H3s: "O triângulo (latência/throughput/footprint) e o que o seu SLA realmente pede", "Metodologia disciplinada (1. baseline com GC log; 2. meta explícita e mensurável; 3. UMA mudança por vez; 4. medir sob carga real; 5. repetir)", "Tuning de G1 (`-XX:MaxGCPauseMillis` — o dial principal e seu custo; região via `G1HeapRegionSize` quando humongous; `InitiatingHeapOccupancyPercent` pra marking cedo demais/tarde demais)", "Tuning de ZGC (dimensionar heap; `SoftMaxHeapSize`; CPU pra fases concorrentes)", "Quando TROCAR de coletor em vez de tunar (sinais de que o perfil não fecha)", "Quando o problema NÃO é GC (alocação excessiva — resolver no código; leak — resolver com heap dump, nota 12)".
- `## Na prática` — cenário hipotético completo (`// hipotético:`): serviço com p99 estourando; baseline do GC log mostra pausas mixed longas; meta declarada; uma mudança; resultado medido. Anti-exemplo de cargo cult (lista de 8 flags coladas de blog) e por que é ruído.
- `## Armadilhas` — ≥3: (1) tunar sem baseline/meta (não dá pra saber se melhorou) → GC log antes, meta numérica; (2) `MaxGCPauseMillis` agressivo demais (G1 encolhe young → minors frequentes → throughput despenca) → relaxar a meta ou trocar pra ZGC; (3) "resolver" leak com `-Xmx` maior (só adia o OOM e alonga as pausas) → heap dump e achar o leak (nota 12); (4) tunar várias flags de uma vez (impossível atribuir efeito) → uma por rodada. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (03, 06, 09, 10, 12, 14, MOC, central, verbetes `G1 GC`/`ZGC (generational)`) + `## Referências` (GC Tuning Guide).

Tamanho: 320-500 linhas (densa; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "triângulo|latência|throughput|footprint|baseline|MaxGCPauseMillis|InitiatingHeapOccupancy|SoftMaxHeapSize|cargo cult" "03-Dominios/Tecnologia/Java/JVM/11 - Tuning de GC — metodologia e prática.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/11 - Tuning de GC — metodologia e prática.md"
git commit -m "feat(java): galho 3 nota 11 — tuning de GC (metodologia e prática)"
```

---

### Task 12: Nota 12 — Diagnóstico — heap dumps, thread dumps e jcmd

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/12 - Diagnóstico — heap dumps, thread dumps e jcmd.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch man page do `jcmd` (`https://docs.oracle.com/en/java/javase/21/docs/specs/man/jcmd.html`) — confirmar subcomandos (`GC.heap_dump`, `Thread.print`, `VM.flags`, `GC.heap_info`, `VM.native_memory`). Troubleshooting Guide pra heap dump/OOM (`https://docs.oracle.com/en/java/javase/21/troubleshoot/`). Eclipse MAT: `https://eclipse.dev/mat/` (existência/papel — dominator tree, leak suspects).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, jvm, magus, diagnostico]`, aliases `["Heap dump", "Thread dump", "jcmd", "Eclipse MAT"]`.

Conteúdo:
- `## O que é` — o kit forense da JVM: `jcmd` (canivete canônico moderno), heap dump (foto da memória), thread dump (foto das threads), NMT (memória nativa).
- `## Por que importa` — quando o OOM/deadlock acontece, ou você tem a evidência ou tem adivinhação; capturar e ler dumps é o hard skill que resolve incidente.
- `## Como funciona` — H3s: "`jcmd` — o canivete (`GC.heap_dump`, `Thread.print`, `VM.flags`, `GC.heap_info`, `VM.native_memory`, `help`)", "As ferramentas legadas vivas (`jstat -gcutil` pra séries, `jmap`/`jstack` — quando ainda aparecem)", "Heap dump (capturar: `jcmd`/`-XX:+HeapDumpOnOutOfMemoryError` + `HeapDumpPath`; analisar no Eclipse MAT: histogram, dominator tree, leak suspects; anatomia de um leak típico — cache sem bound, listener não removido, ThreadLocal em pool)", "Thread dump (estados de thread, lock owners, deadlock detection; ler em série — 3+ dumps espaçados)", "NMT (`-XX:NativeMemoryTracking=summary` + `jcmd VM.native_memory` — quando o RSS cresce e o heap não)".
- `## Na prática` — sequência de incidente hipotético (`// hipotético:`): OOM no pod → tinha `HeapDumpOnOutOfMemoryError`? → copiar dump pra fora → MAT → dominator tree aponta `Map` gigante num cache estático → fix. Comandos completos + outputs ` ```text ` ilustrativos.
- `## Armadilhas` — ≥3: (1) heap dump em produção sem saber o custo (pausa STW + arquivo do tamanho do heap + disco) → janela controlada, disco conferido; (2) analisar o dump na máquina de produção (MAT come RAM/CPU) → copiar pra estação/ambiente de análise; (3) esquecer `-XX:+HeapDumpOnOutOfMemoryError` (o OOM acontece de madrugada e a evidência morre com o pod) → flag sempre ligada + `HeapDumpPath` em volume persistente; (4) concluir de UM thread dump ("está travado!" — pode ser snapshot infeliz) → série de 3+ com intervalo. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (02, 09, 10, 11, 13, MOC, central, verbetes `heap dump`/`jcmd`/`NMT (Native Memory Tracking)`) + `## Referências` (man jcmd, Troubleshooting Guide, MAT).

Tamanho: 300-460 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "jcmd|heap_dump|Thread.print|HeapDumpOnOutOfMemoryError|MAT|dominator|jstat|NativeMemoryTracking" "03-Dominios/Tecnologia/Java/JVM/12 - Diagnóstico — heap dumps, thread dumps e jcmd.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/12 - Diagnóstico — heap dumps, thread dumps e jcmd.md"
git commit -m "feat(java): galho 3 nota 12 — diagnóstico (heap dumps, thread dumps e jcmd)"
```

---

### Task 13: Nota 13 — JFR e JMC — observabilidade de produção

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/13 - JFR e JMC — observabilidade de produção.md`

- [ ] **Step 1: Pesquisar fonte — VERIFICAÇÃO OBRIGATÓRIA**

WebFetch `https://docs.oracle.com/en/java/javase/21/jfapi/` (JFR API guide) + Javadoc `jdk.jfr` (Java 21). **Confirmar**: JFR OSS desde Java 11 (JEP 328) e Event Streaming (JEP 349, Java 14) — openjdk.org 403 → confirmar via Oracle docs/dev.java; o claim de overhead (~1%) — usar o número que a doc oficial usar, com hedge se não houver; JMC é projeto separado (download próprio — `https://www.oracle.com/java/technologies/jdk-mission-control.html` ou adoptium/azul).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, jvm, magus, jfr, diagnostico]`, aliases `["JFR", "Java Flight Recorder", "JMC", "Mission Control"]`.

Conteúdo:
- `## O que é` — JFR = gravador de eventos embutido na JVM (alocação, GC, locks, I/O, métodos), overhead baixo o suficiente pra ficar **sempre ligado em produção**; JMC = a ferramenta de análise (projeto separado).
- `## Por que importa` — é a caixa-preta de avião da JVM: quando o incidente acontece, a gravação **já existia**; OSS desde Java 11 (JEP 328 — sem licença extra), subutilizado por desconhecimento.
- `## Como funciona` — H3s: "Arquitetura de events (categorias; buffers em memória; o modelo de baixo overhead)", "Ligando (flags `-XX:StartFlightRecording=...` e `jcmd JFR.start/JFR.dump/JFR.stop`; profiles `default` vs `profile`)", "Analisando no JMC (automated analysis, method profiling, alocação, latências de lock/I/O)", "JFR Event Streaming (JEP 349, Java 14 — consumir events em tempo real)", "Custom events (estender `jdk.jfr.Event` — instrumentação de domínio)", "Posicionamento (JFR vs profiler de attach vs APM — complementares: JFR é o sempre-ligado de JVM, APM é distribuído/negócio)".
- `## Na prática` — ligar gravação contínua com ring buffer (`-XX:StartFlightRecording=disk=true,maxage=12h,maxsize=512m,dumponexit=true`) — flags conferidas na doc; dump sob demanda com `jcmd <pid> JFR.dump filename=incident.jfr`; um custom event `OrderProcessedEvent` (código completo, ~10 linhas).
- `## Armadilhas` — ≥3: (1) confundir JFR (coleta, no JDK) com JMC (análise, projeto/download separado) → instalar JMC à parte; (2) gravação sem `maxage`/`maxsize` (cresce até encher o disco) → ring buffer sempre; (3) tratar JFR como substituto de APM/tracing distribuído (JFR enxerga UMA JVM) → usar os dois; (4) ligar profile `profile` (mais pesado) achando que é o default de produção → `default` pra always-on. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (10, 12, 14, MOC, central, verbetes `JFR (Java Flight Recorder)`/`JMC (JDK Mission Control)`) + `## Referências` (JFR API guide, Javadoc jdk.jfr, JEPs 328/349).

Tamanho: 280-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "JFR|JMC|StartFlightRecording|JFR.dump|maxage|maxsize|Event Streaming|jdk.jfr|JEP (328|349)" "03-Dominios/Tecnologia/Java/JVM/13 - JFR e JMC — observabilidade de produção.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/13 - JFR e JMC — observabilidade de produção.md"
git commit -m "feat(java): galho 3 nota 13 — JFR e JMC (observabilidade de produção)"
```

---

### Task 14: Nota 14 — Performance da JVM — síntese  ⟦opus⟧ (capstone)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/14 - Performance da JVM — síntese.md`

- [ ] **Step 1: Pesquisar fonte — VERIFICAÇÃO OBRIGATÓRIA (Leyden/CDS)**

Reler as notas 01-13 do galho (síntese). **WebFetch para CDS/AppCDS e Project Leyden**: `https://docs.oracle.com/en/java/javase/21/vm/class-data-sharing.html` (CDS) + confirmar o estado do AOT de Leyden — JEP 483 (Ahead-of-Time Class Loading & Linking, Java 24) e JEPs subsequentes (514/515 em Java 25 — method profiles/command-line ergonomics): **confirmar número, nome e status de cada um citado** via fallback (Oracle release notes, dev.java, `https://openjdk.org/projects/leyden/` se acessível). **Hedge explícito** no que não for final. Sem inventar benchmark.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, jvm, magus, sintese, performance]`, aliases `["Performance da JVM", "Decision tree de GC", "Troubleshooting JVM"]`.

Conteúdo (capstone — decisão de arquitetura, liga o galho):
- TL;DR: performance de JVM não é flag mágica — é escolher o coletor pro perfil, medir antes de mexer, e saber em que fase (startup/warmup/peak) o problema mora. A nota consolida os critérios do galho.
- `## O que é` — síntese: como raciocinar sobre performance da JVM de ponta a ponta.
- `## Como funciona` — H3s:
  - "Decision tree de coletor" — consolidando 06/10/11: SLA de latência? heap? CPU disponível? batch vs serving? → G1/ZGC/Parallel/Serial, com o porquê de cada ramo.
  - "Startup vs warmup vs peak" — o eixo temporal: startup (classloading, CDS/AppCDS ajudam), warmup (JIT — nota 07; impacto em serverless/autoscaling), peak (GC/alocação dominam). CDS/AppCDS explicado curto (archives de classes pré-processadas); **Project Leyden/AOT** com status verificado e hedge (JEP 483 Java 24+; evolução conforme confirmado no Step 1). GraalVM native image: menção como alternativa radical de startup — "Galho 17 (planejado)", sem wikilink.
  - "Checklist de troubleshooting" — OOM (qual área? → nota 02/12), latência alta (GC? → 10/11; lock? → Galho 4; warmup? → 07), CPU alto (GC concorrente? JIT? aplicação? → 06/07/13).
  - "Virtual Threads e a JVM" — impacto citado (stacks no heap como continuations, carrier threads, escala de I/O-bound) → **linka** [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads]] (título conforme Task 0 Step 4), **não re-explica Loom**.
- `## Na prática` — 2-3 cenários hipotéticos explícitos escolhendo postura: API latency-sensitive (ZGC + JFR always-on + warmup plan), batch noturno (Parallel + throughput), serverless/scale-to-zero (startup: CDS/AOT conforme status verificado).
- `## Armadilhas` (de raciocínio) — ≥3: (1) otimizar sem medir (toda decisão do galho começa com baseline — log/JFR); (2) escolher coletor por hype e não por SLA medido; (3) tratar a JVM como caixa preta até o incidente (observabilidade — log de GC + JFR — se liga ANTES); (4) ignorar startup/warmup em workload elástico (o p99 do primeiro minuto também é p99). Cada uma com o raciocínio correto.
- `## Em entrevista` — frase 3+ sentenças enquadrando performance de JVM como decisão de engenharia orientada a medição; vocabulário 6+ termos.
- `### Cheatsheet do galho` — tabela "qual nota pra qual problema" (pipeline→01, memória/OOM→02, GC conceito→03, bytecode→04, classloading→05, escolher coletor→06, warmup/JIT→07, módulos→08, containers/flags→09, ler logs→10, tunar→11, dumps/forense→12, always-on→13).
- `## Veja também` (01, 06, 07, 09, 10, 11, 12, 13, MOC, central, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads]]`) + `## Referências` (CDS docs, JEPs Leyden verificados).

Tamanho: 320-500 linhas (fechamento; opus).

- [ ] **Step 3: Verificar**

```bash
grep -iE "decision|startup|warmup|peak|CDS|Leyden|checklist|cheatsheet" "03-Dominios/Tecnologia/Java/JVM/14 - Performance da JVM — síntese.md" | head
grep -riE "minha experiência|no meu projeto|josenaldo|Patient" "03-Dominios/Tecnologia/Java/JVM/14 - Performance da JVM — síntese.md"
```
Expected: cobre decision tree + eixo temporal + checklist + cheatsheet; **segundo grep VAZIO** (zero fabricação).

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/14 - Performance da JVM — síntese.md"
git commit -m "feat(java): galho 3 nota 14 — performance da JVM (capstone)"
```

---

## Task 15: MOC do galho

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JVM/index.md`

- [ ] **Step 1: Escrever o MOC**

Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "JVM por dentro"`, tags `[java, jvm, moc]`, aliases `["JVM", "Galho 3 - JVM por dentro"]`, `created`/`updated: 2026-06-05`.

Conteúdo (modelar pelo `03-Dominios/Tecnologia/Java/Collections e Streams/index.md`):
- `> [!abstract] TL;DR` — Galho 3 da trilha Java Senior; memória de runtime, Garbage Collection (conceito → coletores → logs → tuning), JIT, classloading, bytecode, JPMS, diagnóstico (jcmd/heap dumps/JFR) e performance.
- `## Sobre este galho` — escopo + audiência primária (senior em prep de entrevista + operação de JVM em produção) + secundária + nota de que é galho de **refator do tronco** `Java Fundamentals` (poda da seção JVM — a última grande seção do tronco). Registrar a fronteira: memory model de *runtime* é daqui; *Java Memory Model* (happens-before) é do Galho 4.
- `## Iniciado` — wikilinks 01-05 (uma linha descritiva cada).
- `## Adepto` — wikilinks 06-10.
- `## Magus` — wikilinks 11-14.
- `## Rotas alternativas` — 5 rotas:
  - **Completa** — 01 → 14.
  - **Entrevista internacional** — 01 → 02 → 03 → 06 → 07 → 14.
  - **Sobrevivência em produção** — 09 → 10 → 12 → 13 → 11.
  - **Por dentro do runtime** — 04 → 05 → 07 → 08.
  - **Tuning de memória e GC** — 02 → 03 → 06 → 10 → 11.
- `## Todas as notas` — bloco Dataview:

````markdown
```dataview
TABLE fase, status, updated
FROM "03-Dominios/Tecnologia/Java/JVM"
WHERE type = "concept"
SORT file.name ASC
```
````

- `## Veja também` — `[[03-Dominios/Tecnologia/Java/index|Java (MOC central)]]`, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (Galho 1)]]`, `[[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections, Streams e Programação Funcional (Galho 2)]]`, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo (Galho 4)]]`, `[[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]`, `[[Java Fundamentals]]` (tronco em transição).

- [ ] **Step 2: Verificar**

```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Tecnologia/Java/JVM/index.md"
grep -c "\[\[" "03-Dominios/Tecnologia/Java/JVM/index.md"
```
Expected: 4 headings de seção; ≥14 wikilinks.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JVM/index.md"
git commit -m "feat(java): galho 3 MOC — JVM por dentro"
```

---

## Task 16: Expandir o Dicionário de Java (NÃO recriar)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`

- [ ] **Step 1: Reler o Dicionário existente**

Ler `03-Dominios/Tecnologia/Java/Dicionário de Java.md` inteiro. Mapear as seções alfabéticas e os verbetes já presentes (Galhos 1/2/4/5). **NÃO recriar; NÃO reordenar.** Confirmar o formato (`### Termo` + 1-3 linhas + `Veja também: [[nota]].`). **Conferir duplicatas** — termos de threads/locks são do Galho 4; `boxing / unboxing` é do Galho 2; não reinserir.

- [ ] **Step 2: Extrair as âncoras de Dicionário usadas nas notas 01-14**

```bash
grep -rhoE "Dicionário de Java#[^]|]+" "03-Dominios/Tecnologia/Java/JVM/"
```
Anotar cada âncora. **Cada verbete inserido deve ter heading que bate EXATAMENTE (case/acento) com a âncora usada nas notas** (regra dos galhos anteriores).

- [ ] **Step 3: Inserir os verbetes em ordem alfabética**

Inserir os verbetes abaixo na seção alfabética correta (case-insensitive, sem acento; criar seção se não existir). Cada um: definição 1-3 linhas em PT-BR + `Veja também:` pra nota canônica. **Conferir antes de inserir que o termo não existe** (ajustar a lista às âncoras reais do Step 2).

| Verbete | Seção | Nota canônica |
|---|---|---|
| bytecode | B | →04 |
| classloader (parent delegation) | C | →05 |
| code cache | C | →07 |
| deoptimization | D | →07 |
| Eden / Survivor spaces | E | →02 |
| Epsilon GC | E | →06 |
| ergonomics (JVM) | E | →09 |
| escape analysis | E | →07 |
| G1 GC | G | →06 |
| GC roots / reachability | G | →03 |
| heap | H | →02 |
| heap dump | H | →12 |
| inlining (JIT) | I | →07 |
| jcmd | J | →12 |
| JFR (Java Flight Recorder) | J | →13 |
| JIT (C1 / C2) | J | →07 |
| JMC (JDK Mission Control) | J | →13 |
| JPMS (module-info) | J | →08 |
| Metaspace | M | →02 |
| NMT (Native Memory Tracking) | N | →12 |
| safepoint | S | →03 |
| Shenandoah | S | →06 |
| stack frame | S | →02 |
| stop-the-world | S | →03 |
| tiered compilation | T | →07 |
| unified logging (-Xlog) | U | →10 |
| weak generational hypothesis | W | →03 |
| ZGC (generational) | Z | →06 |

Atualizar frontmatter `updated: 2026-06-05`.

- [ ] **Step 4: Verificar**

```bash
grep -E "^### (bytecode|G1 GC|JIT|Metaspace|safepoint|tiered compilation|ZGC)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: verbetes do Galho 3 presentes; contagem total subiu ~26-28 vs baseline; verbetes anteriores intactos.

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 3 (JVM)"
```

---

## Task 17: Ativar o Galho 3 no MOC central `Java/index.md`

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/index.md`

- [ ] **Step 1: Trocar a linha do Galho 3 por wikilink ativo**

Localizar por conteúdo (linha 27 hoje: `3. JVM por dentro *(planejado)* — memory model, GC (G1/ZGC), JIT, classloading, bytecode, módulos (JPMS), tuning`) e substituir por:

```markdown
3. [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro]] — memória de runtime, GC (G1/ZGC/Shenandoah), JIT e tiered compilation, classloading, bytecode, módulos (JPMS), diagnóstico (JFR/jcmd) e tuning
```

Atualizar `updated: 2026-06-05`. **Não mexer no resto** (galhos 6-18 seguem texto "(planejado)").

- [ ] **Step 2: Verificar**

```bash
grep -E "JVM/index" "03-Dominios/Tecnologia/Java/index.md"
grep -E "updated: 2026-06-05" "03-Dominios/Tecnologia/Java/index.md"
grep -c "planejado" "03-Dominios/Tecnologia/Java/index.md"
```
Expected: wikilink ativo do Galho 3; `updated` atualizado; "planejado" caiu exatamente 1 vs baseline.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/index.md"
git commit -m "feat(java): ativa Galho 3 (JVM por dentro) no MOC central"
```

---

## Task 18: Poda da seção JVM do tronco

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md`

- [ ] **Step 1: Reler a seção a podar (confirmar limites)**

Reler `Core/Java Fundamentals.md` na seção `## JVM (Java Virtual Machine)` (marcada `[!info] Migra em galho futuro (Galho 3 ...)`). Confirmar onde começa e termina (até o `---` antes de `## Sintaxe básica e tipos`). A poda absorve **todas** as subseções, incluindo `### Project Loom e Virtual Threads` (já era só ponteiro pro Galho 4 — morre sem substituição). **NÃO** tocar `## Concorrência (visão geral)` (dívida Galho 4) nem a cauda (já higienizada pelo Galho 2).

- [ ] **Step 2: Substituir a seção pelo callout de poda**

Substituir o **corpo inteiro** da seção (do callout `[!info]` até antes do `---` final da seção) por um callout no padrão §9 do roadmap (mantém o heading `## `):

```markdown
## JVM (Java Virtual Machine)

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro]]. Veja [[01 - A JVM — o que é e o pipeline de execução]], [[02 - Áreas de memória de runtime]], [[03 - Garbage Collection — o conceito]], [[06 - Os coletores do HotSpot]], [[07 - JIT — C1, C2 e tiered compilation]].
```

(Os wikilinks usam o título de arquivo sem path — Obsidian resolve pelo nome; os callouts dos Galhos 1/2 no mesmo tronco já usam esse formato. Conferir na Task 20 que resolvem.)

- [ ] **Step 3: Conferir intro e "Veja também" do tronco**

A intro do tronco (linha ~16 e o bloco "Em entrevistas, o que diferencia um senior") menciona JVM — pode ficar (texto-resumo, não corpo migrado). No `## Veja também` do tronco, adicionar:

```markdown
- [[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro (galho)]]
```

- [ ] **Step 4: Atualizar `updated` do tronco**

Atualizar o frontmatter `updated:` de `Core/Java Fundamentals.md` para `2026-06-05`.

- [ ] **Step 5: Verificar**

```bash
grep -A3 "^## JVM (Java Virtual Machine)" "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md" | head -5
grep -c "Migrado para galho próprio" "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md"
grep -nE "^### (Memory areas|Garbage Collection|JIT Compiler|Classloader)" "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md"
grep -nE "^## Concorrência" "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md"
```
Expected: seção JVM agora é callout "Migrado" (contador subiu 1 vs baseline); subseções da JVM **sumiram** (grep 3 vazio); `## Concorrência` ainda presente (intacta).

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md"
git commit -m "refactor(java): poda a seção JVM do tronco Java Fundamentals (galho 3)"
```

---

## Task 19: Quitar a dívida reversa ("Galho 3 planejado" → wikilinks)

**Files:**
- Modify: arquivos localizados na Task 0 Step 5 (galhos 1/2/4/5 com ponteiro textual "Galho 3 (JVM) planejado")

- [ ] **Step 1: Relocalizar as ocorrências (por conteúdo, não por linha)**

```bash
grep -rn "Galho 3" "03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/" "03-Dominios/Tecnologia/Java/Collections e Streams/" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/" "03-Dominios/Tecnologia/Java/Swing/"
```
Listar as ocorrências de texto "Galho 3 (JVM)... planejado" (a lista da Task 0 Step 5 pode ter mudado).

- [ ] **Step 2: Converter cada ponteiro textual em wikilink**

Para cada ocorrência, trocar o texto "Galho 3 (JVM), planejado" (e variações) pelo wikilink pra **nota mais específica** do Galho 3 conforme o contexto:
- Menção a custo de memória/heap/alocação/boxing → `[[03-Dominios/Tecnologia/Java/JVM/02 - Áreas de memória de runtime|Áreas de memória de runtime]]`
- Menção a GC genérico → `[[03-Dominios/Tecnologia/Java/JVM/03 - Garbage Collection — o conceito|Garbage Collection]]`
- Menção a JIT/warmup/otimização → `[[03-Dominios/Tecnologia/Java/JVM/07 - JIT — C1, C2 e tiered compilation|JIT]]`
- Menção genérica ao galho (MOCs "Veja também") → `[[03-Dominios/Tecnologia/Java/JVM/index|JVM por dentro (Galho 3)]]`

Ajustar o texto ao redor pra não dizer mais "planejado". **Não inventar links onde o contexto não pede** — só converter os ponteiros existentes.

- [ ] **Step 3: Verificar**

```bash
grep -rn "Galho 3" "03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/" "03-Dominios/Tecnologia/Java/Collections e Streams/" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/" "03-Dominios/Tecnologia/Java/Swing/" | grep -i "planejado"
```
Expected: VAZIO (nenhum "Galho 3 ... planejado" remanescente nos galhos fechados).

- [ ] **Step 4: Commit**

```bash
git add <cada arquivo editado, nominal>
git commit -m "refactor(java): quita dívida reversa — ponteiros 'Galho 3 planejado' viram wikilinks"
```

---

## Task 20: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: Conferir as 14 notas + MOC presentes**

```bash
ls "03-Dominios/Tecnologia/Java/JVM/" | sort
```
Expected: 01..14 + index.md (15 arquivos .md).

- [ ] **Step 2: Conferir frontmatter `fase` e distribuição**

```bash
for f in "03-Dominios/Tecnologia/Java/JVM/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```
Expected: toda nota 01-14 tem `fase:`; distribuição 5 iniciado / 5 adepto / 4 magus.

- [ ] **Step 3: Conferir seções obrigatórias em todas as notas**

```bash
for f in "03-Dominios/Tecnologia/Java/JVM/"[0-9]*.md; do
  echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"
done
```
Expected: cada nota retorna 3.

- [ ] **Step 4: Conferir ausência de fabricação e de wikilinks pra galhos inexistentes**

```bash
grep -riE "minha experiência|no meu projeto|josenaldo|Patient|getSpecialty" "03-Dominios/Tecnologia/Java/JVM/"
grep -rE "\[\[[^]]*(JavaFX|Jakarta|GraalVM|Galho 1[5-8])" "03-Dominios/Tecnologia/Java/JVM/"
```
Expected: ambos VAZIOS (zero fabricação; galhos futuros só como texto "(planejado)").

- [ ] **Step 5: Conferir a "Frase pronta (inglês)" em todas as notas**

```bash
for f in "03-Dominios/Tecnologia/Java/JVM/"[0-9]*.md; do
  echo "$f: $(grep -c '### Frase pronta (inglês)' "$f")"
done
```
Expected: cada nota retorna 1.

- [ ] **Step 6: Rodar a skill de wikilinks**

Invocar a skill `verificar-wikilinks` na pasta `03-Dominios/Tecnologia/Java/JVM/` + `03-Dominios/Tecnologia/Java/index.md` + `03-Dominios/Tecnologia/Java/Dicionário de Java.md` + `03-Dominios/Tecnologia/Java/Core/Java Fundamentals.md` + os arquivos editados na Task 19. Corrigir quebrados (folder-links exigem index.md — regra Quartz). **Lembrar:** falso-positivo em self-anchors `[[#Heading]]` — as notas evitam âncoras same-file; ignorar esse falso-positivo. **Conferir que as âncoras `Dicionário de Java#...` usadas nas notas resolvem 1:1 com os headings dos verbetes inseridos (Task 16 Step 2).** Conferir também que os wikilinks curtos do tronco podado (`[[01 - A JVM — o que é e o pipeline de execução]]` etc.) resolvem. Se houver correções, commitar à parte.

- [ ] **Step 7: Build Quartz (se disponível)**

Confirmar publicação sem erro conforme o pipeline do projeto (deploy cross-repo é manual do usuário — NÃO fazer push/deploy). Se o build não rodar localmente, registrar como verificação manual pendente.

- [ ] **Step 8: Resumo de fechamento (sem commit)**

Reportar ao usuário: 14 notas criadas, distribuição de fases, verbetes adicionados, poda da seção JVM executada (última grande seção do tronco — só resta a dívida do Galho 4), dívida reversa quitada, estado da verificação de wikilinks (e falso-positivos ignorados). Lembrar a decisão diferida (§3.6 do spec): o tronco vira nota-resumo enxuta quando a dívida do Galho 4 for quitada. Trabalho está na `main` (commits locais) — **push é manual do usuário** (não foi feito).

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** as 14 notas (Tasks 1-14) cobrem o §3.1 do spec; MOC (Task 15) → §3.2; Dicionário expandido (Task 16) → §3.3; MOC central (Task 17) → §3.4; poda da seção JVM (Task 18) → §3.5; decisão do destino do tronco (§3.6) registrada como diferida e ecoada no fechamento (Task 20 Step 8); dívida reversa + reciprocidade de links (§3.7) → Task 19 e wikilinks de ida nas notas 02/03 (JMM), 04 (Lambdas), 07 (Streams primitivos), 14 (Virtual Threads); pré-flight (§6) → Task 0; critérios de aceitação (§7) → Task 20. Fronteiras respeitadas: JMM/Loom linkam Galho 4 sem re-explicar; lambdas/boxing linkam Galho 2; GraalVM/profiling como texto "Galho 17 (planejado)" sem wikilink.

**Placeholder scan:** sem TBD/TODO. Cada nota tem Step 1 com URLs de fonte oficial nomeadas, frontmatter concreto, outline de seções (H3s), armadilhas mínimas (≥2 Iniciado / ≥3 Adepto-Magus) e tamanho-alvo. Notas version-sensitive (06 coletores, 13 JFR, 14 Leyden) com verificação obrigatória explícita e instrução de hedge. Capstone (14) com grep anti-fabricação.

**Type/naming consistency:** numeração 01-14 consistente entre tasks, MOC (rotas/seções), Dicionário (notas canônicas), poda (callout) e verificação. Distribuição 5/5/4 consistente no header, nas fases das tasks e na Task 20 Step 2. Notas opus (06/07/11/14) marcadas ⟦opus⟧. Nomes de arquivo sem `:` nem `/` (usado `—` nos títulos compostos). Pasta `JVM` consistente em todos os paths. Títulos das notas vizinhas (Galho 4: 11/12; Galho 2: 04/09) assumidos pelo padrão dos specs e **reconfirmados na Task 0 Step 4** — qualquer divergência ajusta os wikilinks nas notas. Âncoras do Dicionário conferidas 1:1 (Task 16 Step 2 + Task 20 Step 6). Dívida reversa (Task 19) edita por conteúdo, não por linha.
