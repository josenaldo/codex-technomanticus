# Galho 6 — JavaFX (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 6 da trilha Java Senior — 14 notas atômicas (scene graph, layouts, controls, eventos, FXML, properties/binding, TableView, CSS, threading da UI, MVVM, custom controls, empacotamento, estado do projeto) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **poda INTEGRAL do tronco** `Frontend/JavaFX.md` + **quitação da dívida reversa** ("JavaFX planejado" → wikilinks).

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Tecnologia/Java/JavaFX/`, notas `publish: true` em PT-BR, numeração global 01-14 (5/5/4). **Galho de refator com poda INTEGRAL** (como `Java Concurrency` no Galho 4): o tronco `Frontend/JavaFX.md` (161 linhas) é raso, desatualizado ("toolkit oficial da Oracle, substituindo o Swing") e **contaminado de fabricação** (`patient-view.fxml`/`PatientController`/`TableView<Patient>`, `SimpleStringProperty("Josenaldo")`, `## Na prática (da minha experiência)` em 1ª pessoa) — é **contraexemplo, não matéria-prima**; as notas nascem das fontes oficiais (openjfx.io, Javadoc OpenJFX, CSS Reference Guide, Gluon). Fronteiras: teoria de UI single-thread → Galho 5 (linkar EDT/SwingWorker); concorrência → Galho 4; JPMS → Galho 3 (nota 08); Spring DI → "Galho 8 (planejado)" texto; GraalVM native → "Galho 17 (planejado)" texto. Comparações Swing×JavaFX **sempre linkam a nota do Galho 5**. **Direto na `main`** ([[feedback_galhos_direto_main]]); push manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação via WebFetch (openjfx.io, Javadoc OpenJFX, gluonhq.com, man pages Oracle; openjdk.org dá 403 → fallback).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-06`):

```yaml
---
title: "<título sem prefixo numérico>"
created: 2026-06-06
updated: 2026-06-06
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - javafx
  - <fase>
  - <1-3 tags de conceito: scene-graph, layout, controls, eventos, fxml, binding, tableview, css, threading, mvvm, canvas, jpackage, openjfx>
aliases:
  - <aliases>
---
```

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas. Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista. (Pode fundir com "O que é" em Iniciado curtas.)
4. `## Como funciona` — H3s; mínimo 3 em Adepto/Magus.
5. `## Na prática` — código compilável (Java moderno, FXML bem-formado, CSS válido de JavaFX); framing neutro; **NUNCA** 1ª pessoa, `Patient`/`getSpecialty`, `Josenaldo`. Domínios neutros: `Order`, `Customer`, `Product`.
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada uma: `### (N) Título` + descrição + exemplo curto + fix em 1 linha.
7. `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + "Vocabulário" **6+ termos** em tabela `| Termo PT | Termo EN |`.
8. `## Veja também` — wikilinks SEM backticks, SEM âncoras same-file `[[#...]]`. Sempre: notas do galho + `[[03-Dominios/Tecnologia/Java/JavaFX/index|JavaFX (MOC do galho)]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando conectar) Galhos 3/4/5 + verbetes do Dicionário.
9. `## Referências` — docs oficiais consultadas (openjfx.io, Javadoc, Gluon, man pages).

**Tamanho:** 200-500 linhas (Magus densas até 700).

**Restrições absolutas:**
- **Tronco é contraexemplo** — NÃO copiar nada de `Frontend/JavaFX.md`. Toda alegação version-specific verificada via WebFetch. Toda nota tem Referências.
- Sem fabricação ([[feedback_no_fabrication]]); zero estatística de adoção inventada (regra do Galho 5).
- **Não re-explicar o que é de outro galho:** teoria de UI thread/EDT/SwingWorker → Galho 5 (notas 05/06); virtual threads → Galho 4 (nota 12); JPMS → Galho 3 (nota 08); lambdas → Galho 2 (nota 04). Spring/CDI → "Galho 8 (planejado)" e GraalVM native → "Galho 17 (planejado)", texto puro SEM wikilink.
- Comparações justas (quando Swing vence E quando JavaFX vence).
- Code fences: ` ```java `, ` ```xml ` (FXML), ` ```css `, ` ```bash `, ` ```text `. Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (bot de backup roda em timer); 1 commit por nota; direto na `main`; **sem push, sem deploy**.

**Modelo por nota:** sonnet por padrão; **opus** nas **07** (Properties/binding), **10** (Application Thread/Task), **13** (Empacotamento) e **14** (capstone).

**Fontes oficiais (base):**
- OpenJFX: `https://openjfx.io/` e docs `https://openjfx.io/openjfx-docs/` (getting started, run with maven/gradle)
- Javadoc OpenJFX 21: `https://openjfx.io/javadoc/21/` (módulos javafx.base/graphics/controls/fxml)
- Introdução ao FXML: `https://openjfx.io/javadoc/21/javafx.fxml/javafx/fxml/doc-files/introduction_to_fxml.html`
- CSS Reference Guide: `https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/doc-files/cssref.html`
- Scene Builder: `https://gluonhq.com/products/scene-builder/`
- jpackage man page: `https://docs.oracle.com/en/java/javase/21/docs/specs/man/jpackage.html` · jlink: `https://docs.oracle.com/en/java/javase/21/docs/specs/man/jlink.html`
- JEP 392 (jpackage, Java 16): openjdk.org dá 403 → confirmar via man page/release notes Oracle.

---

## Task 0: Pré-flight — pasta e confirmação do terreno

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/` (pasta)

- [ ] **Step 1: Confirmar `main`**

```bash
git branch --show-current
```
Expected: `main`. NÃO criar branch.

- [ ] **Step 2: Criar a pasta do galho**

```bash
mkdir -p "03-Dominios/Tecnologia/Java/JavaFX"
```

- [ ] **Step 3: Reconfirmar o tronco e a fabricação (contraexemplo)**

```bash
grep -nE "Patient|Josenaldo|minha experiência" "03-Dominios/Tecnologia/Java/Frontend/JavaFX.md"
```
Expected: ocorrências presentes (morrem na poda integral, Task 18). NÃO copiar nada deste arquivo.

- [ ] **Step 4: Confirmar títulos exatos das notas vizinhas linkadas**

```bash
ls "03-Dominios/Tecnologia/Java/Swing/" | grep -E "^(03|04|05|06|08|10|12) "
ls "03-Dominios/Tecnologia/Java/JVM/" | grep -E "^08 "
ls "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/" | grep -E "^12 "
ls "03-Dominios/Tecnologia/Java/Collections e Streams/" | grep -E "^04 "
```
Expected: confirmar filenames exatos (o plano assume `03 - Layout managers`, `04 - O modelo de eventos`, `05 - A Event Dispatch Thread`, `06 - SwingWorker e tarefas em background`, `08 - Renderers e editors`, `10 - Custom painting e componentes customizados`, `12 - Swing hoje - estado atual`, `08 - JPMS — o sistema de módulos`, `12 - Virtual Threads e Project Loom`, `04 - Lambdas e interfaces funcionais`). Anotar divergências.

- [ ] **Step 5: Localizar a dívida reversa ("JavaFX planejado")**

```bash
grep -rni "javafx" "03-Dominios/Tecnologia/Java/Swing/" "03-Dominios/Tecnologia/Java/JVM/" "03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/" "03-Dominios/Tecnologia/Java/Collections e Streams/" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/" | grep -i "planejado"
grep -rn "\[\[JavaFX\]\]" "03-Dominios/Tecnologia/Java/" --include="*.md" | grep -v "Frontend/JavaFX.md"
```
Anotar: (a) ganchos "planejado" a converter (Task 19); (b) quem linka `[[JavaFX]]` (tronco) — esses continuam válidos após a poda (arquivo persiste).

- [ ] **Step 6: Fixar fatos a verificar (WebFetch nota a nota)**

Linha do tempo (JavaFX 2 em 2011; bundled JDK 8; desacoplado Java 11); release atual do JavaFX e cadence; coordenadas Maven (`org.openjfx:javafx-controls`); nomes dos módulos JPMS (`javafx.base`/`javafx.graphics`/`javafx.controls`/`javafx.fxml`); jpackage = JEP 392/Java 16; Scene Builder mantido pela Gluon; Gluon LTS. Nada de memória.

- [ ] **Step 7: Sem commit** (preparação).

---

## Fase INICIADO (notas 01-05)

### Task 1: Nota 01 — JavaFX — o que é e como chega ao projeto

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/01 - JavaFX — o que é e como chega ao projeto.md`

- [ ] **Step 1: Pesquisar fonte — VERIFICAÇÃO DE LINHA DO TEMPO**

WebFetch `https://openjfx.io/` e `https://openjfx.io/openjfx-docs/` (getting started — seções "JavaFX and IntelliJ/Maven/Gradle"). CONFIRMAR: JavaFX não vem no JDK (desacoplado no Java 11), coordenadas Maven `org.openjfx:javafx-*`, release atual, plugin maven/gradle. História (JavaFX 2 em 2011, bundled no JDK 8): confirmar em openjfx.io/dev.java/Wikipedia como apoio — hedge no que não confirmar em fonte primária.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, javafx, iniciado, openjfx]`, aliases `["JavaFX", "OpenJFX", "Primeira aplicação JavaFX"]`.

Conteúdo:
- TL;DR: JavaFX é o toolkit desktop moderno do ecossistema Java — scene graph, FXML, binding e CSS; **não vem no JDK** (desacoplado no 11; projeto OpenJFX); chega via Maven/Gradle; Swing continua existindo (não foi "substituído").
- `## O que é` — toolkit de UI desktop; linha do tempo honesta (JavaFX 2 → bundled JDK 8 → desacoplado Java 11 → OpenJFX com stewardship Gluon/comunidade); **mata o framing "substituto oficial do Swing"** (Swing segue core Java SE — linka [[12 - Swing hoje - estado atual]] do Galho 5).
- `## Por que importa` — setup é a primeira pegadinha (não está no JDK!); entrevista cobra o estado atual, não o de 2014.
- `## Como funciona` — H3s: "De onde vem (OpenJFX, releases acoplados à cadence do JDK)", "Como chega ao projeto (Maven/Gradle `org.openjfx:javafx-controls` + plugin; ou SDK standalone)", "O lifecycle de `Application` (`init` → `start(Stage)` → `stop`; o launcher)", "Stage e Scene (janela e conteúdo — teaser do scene graph, nota 02)".
- `## Na prática` — `HelloFX` completo (Application + Stage + Scene + Label) em ```java; trecho de `pom.xml` com dependência e plugin em ```xml; rodar com `mvn javafx:run` em ```bash; mencionar o erro "JavaFX runtime components are missing" como teaser da nota 13 (sem resolver aqui).
- `## Armadilhas` — ≥2: (1) achar que JavaFX vem no JDK (compila? não acha as classes) → dependência Maven/Gradle; (2) rodar `java HelloFX` direto e tomar "runtime components are missing" → usar o plugin (`mvn javafx:run`) ou module-path (nota 13); (3) tutorial de 2014 (JDK 8 bundled, `jfxrt.jar`) → docs atuais do openjfx.io.
- `## Em entrevista` + `## Veja também` ([[02 - Scene graph — stage, scene e nodes]], [[13 - Empacotamento — módulos, jlink e jpackage]], [[14 - JavaFX hoje — estado do projeto e Swing vs JavaFX]], [[03-Dominios/Tecnologia/Java/Swing/12 - Swing hoje - estado atual|Swing hoje]], MOC galho, MOC central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#OpenJFX|OpenJFX (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#Stage / Scene|Stage / Scene (Dicionário)]]) + `## Referências`.

Tamanho: 220-340 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -cE "^## (O que é|Por que importa|Como funciona|Na prática|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Tecnologia/Java/JavaFX/01 - JavaFX — o que é e como chega ao projeto.md"
grep -E "org.openjfx|Java 11|OpenJFX|Application|Stage" "03-Dominios/Tecnologia/Java/JavaFX/01 - JavaFX — o que é e como chega ao projeto.md" | head
```
Expected: ≥7 seções; linha do tempo + setup cobertos.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/01 - JavaFX — o que é e como chega ao projeto.md"
git commit -m "feat(java): galho 6 nota 01 — JavaFX, o que é e como chega ao projeto"
```

---

### Task 2: Nota 02 — Scene graph — stage, scene e nodes

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/02 - Scene graph — stage, scene e nodes.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch Javadoc `https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/Node.html` (e/ou `Scene`/`Stage`). Confirmar: hierarquia `Node`/`Parent`/`Group`/`Region`, sistema de coordenadas (local vs parent vs scene), transformações, retained mode.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, javafx, iniciado, scene-graph]`, aliases `["Scene graph", "Stage Scene Node"]`.

Conteúdo:
- `## O que é` — o scene graph: árvore de `Node`s que descreve a UI; **retained mode** (você descreve, o framework renderiza e re-renderiza).
- `## Por que importa` — é o modelo mental central do JavaFX; o contraste com o paint do Swing é pergunta clássica de quem migra.
- `## Como funciona` — H3s: "Stage → Scene → root (a espinha)", "Node, Parent, Group e Region (a taxonomia)", "Coordenadas e transformações (translate/scale/rotate; local vs parent vs scene)", "Retained vs immediate mode — o contraste com `paintComponent` do Swing" (→ linka [[10 - Custom painting e componentes customizados]] do Galho 5, sem re-explicar painting). Diagrama ```text da árvore.
- `## Na prática` — montar uma cena pequena por código (VBox com Label+Button), inspecionar `getChildren()`, aplicar uma transformação; `node.lookup()` por seletor (teaser CSS nota 09).
- `## Armadilhas` — ≥2: (1) adicionar o mesmo Node em dois parents (`IllegalArgumentException: duplicate children`) → um node, um pai; (2) esperar que mutar a UI redesenhe "na hora errada" da thread (teaser da regra da nota 10); (3) abusar de `Group` quando `Region`/pane com layout resolve (Group não faz layout).
- `## Em entrevista` + `## Veja também` (01, 03, 09, 10, 12, [[03-Dominios/Tecnologia/Java/Swing/10 - Custom painting e componentes customizados|Custom painting (Swing)]], MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#scene graph|scene graph (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#retained mode / immediate mode|retained mode (Dicionário)]]) + `## Referências`.

Tamanho: 240-380 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "Node|Parent|Group|Region|retained|coordenada|transform" "03-Dominios/Tecnologia/Java/JavaFX/02 - Scene graph — stage, scene e nodes.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/02 - Scene graph — stage, scene e nodes.md"
git commit -m "feat(java): galho 6 nota 02 — scene graph (stage, scene e nodes)"
```

---

### Task 3: Nota 03 — Layout panes

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/03 - Layout panes.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch Javadoc `https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/layout/package-summary.html`. Confirmar os panes (`VBox`/`HBox`/`BorderPane`/`GridPane`/`StackPane`/`FlowPane`/`AnchorPane`/`TilePane`) e os static constraints (`setHgrow`/`setVgrow`/`setMargin`).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, javafx, iniciado, layout]`, aliases `["Layout panes", "VBox HBox", "GridPane"]`.

Conteúdo:
- `## O que é` — panes = containers com política de layout embutida (o análogo dos layout managers do Swing, mas cada pane É seu layout).
- `## Como funciona` — H3s: "Os lineares (`VBox`/`HBox` + spacing/padding/alignment)", "`BorderPane` (top/bottom/left/right/center) e `StackPane`", "`GridPane` (linhas/colunas, span, constraints)", "`FlowPane`/`TilePane`/`AnchorPane` (quando usar)", "Growth e constraints estáticos (`HBox.setHgrow(node, Priority.ALWAYS)`, `setMargin`)", "Contraste com o Swing (1 container + 1 manager plugável vs pane = layout)" → linka [[03 - Layout managers]] (Galho 5).
- `## Na prática` — formulário com `GridPane` (labels + fields), janela app-like com `BorderPane` (toolbar/center/status), redimensionamento com `Hgrow`.
- `## Armadilhas` — ≥2: (1) `AnchorPane` pra tudo (layout absoluto disfarçado, quebra em resize) → pane com política; (2) esquecer `Hgrow`/`Vgrow` e culpar o pane ("não estica") → constraint explícito; (3) aninhar panes demais sem necessidade (custo de layout pass + ilegibilidade) → escolher o pane certo.
- `## Em entrevista` + `## Veja também` (02, 04, 06, 09, [[03-Dominios/Tecnologia/Java/Swing/03 - Layout managers|Layout managers (Swing)]], MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#layout pane|layout pane (Dicionário)]]) + `## Referências`.

Tamanho: 240-380 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "VBox|HBox|BorderPane|GridPane|StackPane|AnchorPane|Hgrow|Priority" "03-Dominios/Tecnologia/Java/JavaFX/03 - Layout panes.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/03 - Layout panes.md"
git commit -m "feat(java): galho 6 nota 03 — layout panes"
```

---

### Task 4: Nota 04 — Controls essenciais

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/04 - Controls essenciais.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch Javadoc `https://openjfx.io/javadoc/21/javafx.controls/javafx/scene/control/package-summary.html`. Confirmar os controls citados e a relação `ListView`/`TableView` ↔ `ObservableList`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, javafx, iniciado, controls]`, aliases `["Controls JavaFX", "TextField Button", "ComboBox"]`.

Conteúdo:
- `## O que é` — a biblioteca de controls (`javafx.scene.control`): widgets prontos sobre o scene graph.
- `## Como funciona` — H3s: "Texto e ação (`Label`/`Button`/`TextField`/`TextArea`/`PasswordField` + promptText/tooltip)", "Escolha (`CheckBox`/`RadioButton`+`ToggleGroup`/`ComboBox`/`ChoiceBox`)", "Listas e tabelas — visão geral (`ListView`/`TableView` sobre `ObservableList` — profundidade na nota 08)", "Janela e diálogo (`Alert`/`Dialog`/`FileChooser` — visão geral)", "Estado (`disable`/`visible`/`managed`)".
- `## Na prática` — form de cadastro de `Customer` (TextField + ComboBox + CheckBox + Button com `setOnAction`); um `Alert` de confirmação.
- `## Armadilhas` — ≥2: (1) `visible=false` mas o espaço continua (managed!) → `setManaged(false)` junto; (2) `RadioButton` sem `ToggleGroup` (todos marcáveis) → agrupar; (3) ler `TextField.getText()` e esquecer validação/conversão (não há InputVerifier automático) → validar no handler/binding (nota 07).
- `## Em entrevista` + `## Veja também` (03, 05, 06, 07, 08, MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#ObservableList|ObservableList (Dicionário)]]) + `## Referências`.

Tamanho: 220-360 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "Button|TextField|ComboBox|CheckBox|ToggleGroup|ListView|TableView|Alert" "03-Dominios/Tecnologia/Java/JavaFX/04 - Controls essenciais.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/04 - Controls essenciais.md"
git commit -m "feat(java): galho 6 nota 04 — controls essenciais"
```

---

### Task 5: Nota 05 — Eventos — capturing, bubbling e handlers

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/05 - Eventos — capturing, bubbling e handlers.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch Javadoc `https://openjfx.io/javadoc/21/javafx.base/javafx/event/Event.html` e/ou tutorial de event handling do OpenJFX se acessível. Confirmar: event dispatch chain (capturing → target → bubbling), `addEventFilter` (capturing) vs `addEventHandler` (bubbling), `consume()`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, javafx, iniciado, eventos]`, aliases `["Eventos JavaFX", "EventFilter EventHandler", "Bubbling"]`.

Conteúdo:
- `## O que é` — modelo de eventos por dispatch chain na árvore do scene graph (desce capturando, sobe borbulhando) — diferente do Swing (listener direto no componente) → linka [[04 - O modelo de eventos]] (Galho 5).
- `## Como funciona` — H3s: "A dispatch chain (capturing → target → bubbling)", "`EventFilter` (capturing) vs `EventHandler` (bubbling)", "`consume()` (parar a propagação)", "Convenience methods (`setOnAction`/`setOnMouseClicked`/`setOnKeyPressed`)", "Tipos de evento (`ActionEvent`, `MouseEvent`, `KeyEvent` — hierarquia de `EventType`)". Diagrama ```text da chain.
- `## Na prática` — handler de ação em Button (lambda — linka Galho 2 nota 04 sem re-explicar); filter no parent interceptando antes do filho; `consume()` bloqueando um atalho.
- `## Armadilhas` — ≥2: (1) esperar que handler no pai rode antes do filho (bubbling sobe — use filter pra interceptar antes) → `addEventFilter`; (2) esquecer `consume()` e o evento "vaza" pra outro handler; (3) lógica pesada no handler (trava a UI thread — teaser nota 10).
- `## Em entrevista` + `## Veja também` (02, 04, 10, [[03-Dominios/Tecnologia/Java/Swing/04 - O modelo de eventos|O modelo de eventos (Swing)]], [[03-Dominios/Tecnologia/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas]], MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#event dispatch chain (capturing / bubbling)|event dispatch chain (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#EventFilter / EventHandler|EventFilter / EventHandler (Dicionário)]]) + `## Referências`.

Tamanho: 220-360 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "capturing|bubbling|EventFilter|EventHandler|consume|dispatch chain|setOnAction" "03-Dominios/Tecnologia/Java/JavaFX/05 - Eventos — capturing, bubbling e handlers.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/05 - Eventos — capturing, bubbling e handlers.md"
git commit -m "feat(java): galho 6 nota 05 — eventos (capturing, bubbling e handlers)"
```

---

## Fase ADEPTO (notas 06-10)

### Task 6: Nota 06 — FXML e Scene Builder

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/06 - FXML e Scene Builder.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://openjfx.io/javadoc/21/javafx.fxml/javafx/fxml/doc-files/introduction_to_fxml.html` (Introduction to FXML) e `https://gluonhq.com/products/scene-builder/` (confirmar que Scene Builder é mantido/distribuído pela Gluon). Confirmar: `fx:controller`, `fx:id`, `@FXML`, `initialize()`, `FXMLLoader.load`/`getController`, `ResourceBundle`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, javafx, adepto, fxml]`, aliases `["FXML", "Scene Builder", "FXMLLoader"]`.

Conteúdo:
- `## O que é` — FXML: a view em XML declarativo, separada do controller Java; Scene Builder: o editor visual (Gluon).
- `## Por que importa` — separação view/lógica; é o formato que designers/ferramentas falam; entrevista cobra o ciclo FXMLLoader → controller.
- `## Como funciona` — H3s: "Anatomia de um FXML (imports, root, `fx:id`, atributos)", "O controller (`fx:controller`, `@FXML` em campos e métodos, `initialize()` e a ordem de injeção)", "`FXMLLoader` (load, `getController`, `setControllerFactory` — gancho da nota 11)", "Resources e i18n (`%key` + `ResourceBundle`)", "Scene Builder (papel, ida-e-volta com o FXML)", "FXML vs código puro (trade-offs honestos: tooling/separação vs type-safety/refactoring)".
- `## Na prática` — par completo `order-view.fxml` (```xml: VBox + TextField fx:id + Button onAction) + `OrderController` (```java: @FXML + initialize + handler); carregar com FXMLLoader no `start`.
- `## Armadilhas` — ≥3: (1) campo `@FXML` null no construtor (injeção vem DEPOIS) → usar `initialize()`; (2) `fx:id` ≠ nome do campo (silenciosamente null) → bater os nomes; (3) caminho de resource errado no `getResource` (NPE no load) → path absoluto do classpath `/com/example/order-view.fxml`; (4) lógica de negócio no controller FXML (vira god class) → ViewModel (nota 11).
- `## Em entrevista` + `## Veja também` (01, 04, 07, 11, MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#FXML|FXML (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#fx:id / @FXML|fx:id (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#FXMLLoader|FXMLLoader (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#Scene Builder|Scene Builder (Dicionário)]]) + `## Referências`.

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "fx:controller|fx:id|@FXML|initialize|FXMLLoader|ResourceBundle|Scene Builder" "03-Dominios/Tecnologia/Java/JavaFX/06 - FXML e Scene Builder.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/06 - FXML e Scene Builder.md"
git commit -m "feat(java): galho 6 nota 06 — FXML e Scene Builder"
```

---

### Task 7: Nota 07 — Properties e binding  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/07 - Properties e binding.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch Javadoc `https://openjfx.io/javadoc/21/javafx.base/javafx/beans/property/package-summary.html` e `https://openjfx.io/javadoc/21/javafx.base/javafx/beans/binding/Bindings.html`. Confirmar: hierarquia `ObservableValue`/`Property`, implementações `Simple*Property`, `bind`/`bindBidirectional`/`unbind`, invalidation vs change listener (lazy evaluation), fábricas de `Bindings`, weak listeners.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, javafx, adepto, binding]`, aliases `["Properties JavaFX", "Binding", "SimpleStringProperty"]`.

Conteúdo:
- `## O que é` — o sistema reativo do JavaFX: valores observáveis (`ObservableValue`), mutáveis e bindáveis (`Property`); a UI inteira é construída sobre eles (todo control expõe `xxxProperty()`).
- `## Por que importa` — é O diferencial do JavaFX sobre o Swing (que não tem nada nativo equivalente); base do MVVM (nota 11) e do Task (nota 10); entrevista adora "invalidation vs change".
- `## Como funciona` — H3s: "A hierarquia (`ObservableValue` → `ReadOnlyProperty` → `Property`; especializações String/Integer/Double/Boolean/Object)", "O padrão de property em modelos (`private final StringProperty name = new SimpleStringProperty(); name() / nameProperty() / setName()`)", "Binding unidirecional (`bind` — o alvo fica read-only) e bidirecional (`bindBidirectional`)", "Invalidation vs change listener (lazy evaluation — invalidation não recalcula; change força o valor)", "Computed bindings (`Bindings.createStringBinding`, `concat`, `when().then().otherwise()`)", "Weak listeners e leaks (quem segura quem; `WeakChangeListener`)", "Quando binding clareia vs quando vira teia indebugável (regra prática)".
- `## Na prática` — model `Order` com properties; `label.textProperty().bind(order.totalProperty().asString("R$ %.2f"))`; bidirectional em TextField; um computed binding (total = qty × price); demonstrar `bind` + `set` manual = `RuntimeException: A bound value cannot be set`.
- `## Armadilhas` — ≥3: (1) `set` num property bound (exception) → quem binda não seta; (2) listener anônimo segurando o objeto inteiro (leak) → weak listener ou unbind no dispose; (3) cadeia de bindings com dependência circular (bidirectional A↔B↔A — loop/comportamento errático) → desenhar o grafo antes; (4) usar change listener onde invalidation basta (custo de avaliação eager em cadeias longas).
- `## Em entrevista` + `## Veja também` (04, 06, 08, 10, 11, MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#Property (JavaFX)|Property (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#binding (JavaFX)|binding (Dicionário)]]) + `## Referências`.

Tamanho: 320-500 linhas (densa; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "ObservableValue|SimpleStringProperty|bindBidirectional|invalidation|change listener|Bindings|Weak" "03-Dominios/Tecnologia/Java/JavaFX/07 - Properties e binding.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/07 - Properties e binding.md"
git commit -m "feat(java): galho 6 nota 07 — properties e binding"
```

---

### Task 8: Nota 08 — TableView, cell factories e dados observáveis

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/08 - TableView, cell factories e dados observáveis.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch Javadoc `https://openjfx.io/javadoc/21/javafx.controls/javafx/scene/control/TableView.html` (a doc da classe é extensa e exemplificada) + `https://openjfx.io/javadoc/21/javafx.base/javafx/collections/transformation/FilteredList.html`. Confirmar: `cellValueFactory` vs `cellFactory`, `updateItem` (regras: super, empty), `SortedList.comparatorProperty().bind(table.comparatorProperty())`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, javafx, adepto, tableview]`, aliases `["TableView", "Cell factory", "FilteredList SortedList"]`.

Conteúdo:
- `## O que é` — o workhorse de dados do JavaFX: `TableView<S>` sobre `ObservableList<S>`, colunas tipadas `TableColumn<S,T>`.
- `## Por que importa` — toda app de negócio tem grid; o par cellValueFactory/cellFactory é o conceito que separa quem entende do que copia código; análogo direto dos renderers do Swing → linka [[08 - Renderers e editors]] (Galho 5).
- `## Como funciona` — H3s: "`ObservableList` e `FXCollections` (a lista que avisa)", "`cellValueFactory` (DADOS: de S pra ObservableValue<T> — com properties do model, nota 07)", "`cellFactory` (RENDER: a célula custom; as regras de `updateItem` — chamar super, tratar empty)", "Seleção (`selectionModel`, single/multiple)", "Edição (células editáveis, `onEditCommit`)", "Sorting e filtering (`SortedList`/`FilteredList` + `comparatorProperty().bind` — o pipeline list→filtered→sorted→table)".
- `## Na prática` — tabela de `Order` completa: model com properties (nota 07), colunas com `cellValueFactory`, uma coluna com `cellFactory` custom (status colorido), filtro por TextField com `FilteredList.predicateProperty().bind(...)`.
- `## Armadilhas` — ≥3: (1) `updateItem` sem tratar `empty` (células fantasma ao rolar — célula é REUSADA) → `if (empty) { setText(null); setGraphic(null); }`; (2) `SortedList` sem `comparatorProperty().bind` (clicar no header não ordena) → bind; (3) trocar a `List` inteira em vez de mutar a `ObservableList` (tabela não atualiza) → `setAll`; (4) lógica pesada em `updateItem` (roda no scroll!) → pré-computar.
- `## Em entrevista` + `## Veja também` (04, 07, 09, [[03-Dominios/Tecnologia/Java/Swing/08 - Renderers e editors|Renderers e editors (Swing)]], MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#cell factory / cell value factory|cell factory (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#ObservableList|ObservableList (Dicionário)]]) + `## Referências`.

Tamanho: 300-460 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "cellValueFactory|cellFactory|updateItem|ObservableList|FilteredList|SortedList|comparatorProperty" "03-Dominios/Tecnologia/Java/JavaFX/08 - TableView, cell factories e dados observáveis.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/08 - TableView, cell factories e dados observáveis.md"
git commit -m "feat(java): galho 6 nota 08 — TableView, cell factories e dados observáveis"
```

---

### Task 9: Nota 09 — CSS em JavaFX

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/09 - CSS em JavaFX.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/doc-files/cssref.html` (CSS Reference Guide — a fonte canônica). Confirmar: seletores suportados, propriedades `-fx-*` citadas, precedência (inline > parent stylesheet > scene stylesheet > user agent), Modena como user-agent stylesheet default, pseudo-classes.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, javafx, adepto, css]`, aliases `["CSS JavaFX", "-fx-", "Modena"]`.

Conteúdo:
- `## O que é` — estilização via CSS próprio do JavaFX: sintaxe familiar, **vocabulário próprio** (`-fx-*`) — NÃO é CSS web (subset/dialeto; sem float/grid/media queries; layout é dos panes, não do CSS).
- `## Por que importa` — temas e identidade visual sem recompilar; o que o Swing nunca teve nativo (L&F é outra coisa → contraste honesto); entrevista pergunta a precedência.
- `## Como funciona` — H3s: "Seletores (`.style-class`, `#id`, descendentes, pseudo-classes `:hover`/`:focused`/`:disabled`)", "Propriedades `-fx-*` (background, border, font, padding — as famílias; sempre conferir no Reference Guide)", "Onde pendurar (inline `setStyle`, `getStyleClass`, stylesheets de Scene/Parent)", "Precedência (inline > stylesheet do Parent > da Scene > user-agent/Modena)", "Custom pseudo-classes (`PseudoClass.getPseudoClass` + `pseudoClassStateChanged`)", "Temas (trocar stylesheet em runtime; claro/escuro)".
- `## Na prática` — `app.css` (```css) com style class pra botão primário + pseudo-class `:hover`; aplicar na Scene; tema escuro alternável por código; custom pseudo-class `.overdue` em linha de tabela (conecta nota 08).
- `## Armadilhas` — ≥3: (1) copiar CSS web (`background-color` sem `-fx-`, grid/flex — ignorados silenciosamente) → Reference Guide; (2) inline `setStyle` espalhado (vence tudo e não tematiza) → style classes; (3) seletor de estrutura interna de control (`.text-field > .text`) que quebra entre versões → API pública de style class quando existir.
- `## Em entrevista` + `## Veja também` (02, 03, 08, 12, [[03-Dominios/Tecnologia/Java/Swing/09 - Look and Feel e temas|Look and Feel (Swing)]], MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#CSS do JavaFX (-fx-)|CSS do JavaFX (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#Modena|Modena (Dicionário)]]) + `## Referências`.

Tamanho: 260-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "\-fx\-|Modena|pseudo|stylesheet|precedência|getStyleClass" "03-Dominios/Tecnologia/Java/JavaFX/09 - CSS em JavaFX.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/09 - CSS em JavaFX.md"
git commit -m "feat(java): galho 6 nota 09 — CSS em JavaFX"
```

---

### Task 10: Nota 10 — A JavaFX Application Thread — Task, Service e Platform.runLater  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/10 - A JavaFX Application Thread — Task, Service e Platform.runLater.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch Javadoc `https://openjfx.io/javadoc/21/javafx.graphics/javafx/concurrent/Task.html` e `https://openjfx.io/javadoc/21/javafx.graphics/javafx/concurrent/Service.html` (atenção: o pacote é `javafx.concurrent` — conferir o módulo real no Javadoc). Confirmar: regra da JavaFX Application Thread, `Platform.runLater`, properties de `Task` (progress/message/value/state), `updateProgress`/`updateMessage`, `Service.restart`, `ScheduledService`, cancelamento.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, javafx, adepto, threading]`, aliases `["JavaFX Application Thread", "Task Service", "Platform.runLater"]`.

Conteúdo:
- `## O que é` — a single-thread rule do JavaFX: scene graph só pode ser tocado pela **JavaFX Application Thread** — mesma regra do EDT do Swing → linka [[05 - A Event Dispatch Thread]] (Galho 5) pra teoria (POR QUE toolkits são single-threaded), **sem re-explicar**.
- `## Por que importa` — violar = `IllegalStateException: Not on FX application thread` (quando dá sorte) ou corrupção silenciosa; bloquear = app congelada; é A pergunta de entrevista desktop.
- `## Como funciona` — H3s: "A regra e a thread (quem é a FX Application Thread; `Platform.isFxApplicationThread`)", "`Platform.runLater` (de volta pra UI thread; quando NÃO usar — rajadas → coalescing)", "`Task<V>` (o worker com properties **bindáveis**: progress/message/value/state — a vantagem estrutural sobre o SwingWorker → linka [[06 - SwingWorker e tarefas em background]] do Galho 5)", "`Service<V>` (Task reusável: `restart`/`reset`; executor configurável)", "`ScheduledService` (períodico com backoff)", "Cancelamento cooperativo (`isCancelled` no corpo; `updateProgress` lança se cancelado?  — conferir Javadoc)", "Virtual threads e JavaFX (o que muda e o que não muda — a regra da UI thread CONTINUA; linka [[12 - Virtual Threads e Project Loom]] do Galho 4, sem re-explicar Loom)".
- `## Na prática` — `Task<List<Order>>` carregando dados: `progressProperty().bind` numa ProgressBar, `setOnSucceeded` populando a `ObservableList` (conecta nota 08); um `Service` de refresh com `restart()`; contraexemplo do erro (tocar Label dentro do `call()`) com a exception real em ```text.
- `## Armadilhas` — ≥3: (1) tocar a UI dentro de `call()` (exception/corrupção) → properties do Task + `updateMessage`/`updateProgress`, ou `runLater`; (2) bloquear a FX thread com I/O no handler (app congela; nem spinner roda) → Task; (3) `Platform.runLater` em loop apertado (enfileira milhares de runnables — UI engasga) → coalescing/throttle; (4) esquecer `setOnFailed` (exceção do Task morre silenciosa) → handler de falha sempre.
- `## Em entrevista` + `## Veja também` (05, 07, 08, [[03-Dominios/Tecnologia/Java/Swing/05 - A Event Dispatch Thread|EDT (Swing)]], [[03-Dominios/Tecnologia/Java/Swing/06 - SwingWorker e tarefas em background|SwingWorker (Swing)]], [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads]], MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#JavaFX Application Thread|JavaFX Application Thread (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#Platform.runLater|Platform.runLater (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#Task / Service (JavaFX)|Task / Service (Dicionário)]]) + `## Referências`.

Tamanho: 320-500 linhas (densa; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "Application Thread|Platform.runLater|Task|Service|updateProgress|setOnSucceeded|setOnFailed|isCancelled" "03-Dominios/Tecnologia/Java/JavaFX/10 - A JavaFX Application Thread — Task, Service e Platform.runLater.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/10 - A JavaFX Application Thread — Task, Service e Platform.runLater.md"
git commit -m "feat(java): galho 6 nota 10 — a JavaFX Application Thread (Task, Service e Platform.runLater)"
```

---

## Fase MAGUS (notas 11-14)

### Task 11: Nota 11 — Arquitetura — MVC, MVVM e injeção de dependência

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md`

- [ ] **Step 1: Pesquisar fonte**

Reler as notas 06 (FXML/controller) e 07 (properties/binding) — esta nota compõe as duas. WebFetch Javadoc `FXMLLoader` (`setControllerFactory`) pra confirmar o gancho de DI. Padrões MVVM: basear no mecanismo (properties+binding), sem citar frameworks específicos como fato (mvvmFX etc. só como menção de existência, sem detalhar).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, javafx, magus, mvvm, arquitetura]`, aliases `["MVVM JavaFX", "Arquitetura JavaFX", "controllerFactory"]`.

Conteúdo:
- `## O que é` — como organizar uma app JavaFX além do controller: MVC (o que o FXML te dá), MVVM (o que properties/binding habilitam), e DI nos controllers.
- `## Por que importa` — controller FXML vira god class rápido; MVVM é o caso arquitetural FORTE do JavaFX (o motivo de escolhê-lo sobre Swing em app nova); testabilidade sem toolkit é argumento de senior.
- `## Como funciona` — H3s: "MVC à la FXML (FXML=view, controller=glue, model=domínio; onde ele rateia)", "MVVM com properties (ViewModel expõe properties + commands; View binda; **zero referência View→lógica e zero ViewModel→View**)", "O ViewModel testável (JUnit puro, sem toolkit, sem thread de UI — properties são `javafx.base`)", "DI nos controllers (`FXMLLoader.setControllerFactory(factory)` — o gancho; Spring/CDI entram aí, tema do Galho 8 (planejado), texto sem wikilink)", "Quando MVC basta vs quando MVVM compensa (tamanho/tempo de vida/time)".
- `## Na prática` — refatorar o par da nota 06: `OrderViewModel` (properties + método `save()`) + controller fino que só binda; teste JUnit do ViewModel sem JavaFX rodando (só `javafx.base` no classpath); `setControllerFactory` com factory manual (sem framework).
- `## Armadilhas` — ≥3: (1) lógica de negócio no controller FXML (intestável, acoplada à view) → ViewModel; (2) ViewModel referenciando Nodes (inverteu a seta — vira controller disfarçado) → ViewModel só expõe properties; (3) binding bidirecional View↔ViewModel pra tudo (perde o fluxo de dados explícito em forms complexos) → unidirecional + commands onde importa; (4) testar ViewModel com Thread de UI/Robot sem precisar (properties não exigem toolkit) → JUnit puro.
- `## Em entrevista` + `## Veja também` (06, 07, 10, 14, MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#MVVM|MVVM (Dicionário)]]) + `## Referências`.

Tamanho: 280-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "MVVM|ViewModel|controllerFactory|testáve|binda" "03-Dominios/Tecnologia/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md" | head
grep -E "\[\[[^]]*Spring" "03-Dominios/Tecnologia/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md"
```
Expected: MVVM coberto; segundo grep VAZIO (Spring só texto "planejado").

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/11 - Arquitetura — MVC, MVVM e injeção de dependência.md"
git commit -m "feat(java): galho 6 nota 11 — arquitetura (MVC, MVVM e injeção de dependência)"
```

---

### Task 12: Nota 12 — Custom controls, Canvas e charts

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/12 - Custom controls, Canvas e charts.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch Javadoc `https://openjfx.io/javadoc/21/javafx.graphics/javafx/scene/canvas/Canvas.html` + `https://openjfx.io/javadoc/21/javafx.controls/javafx/scene/control/Control.html` (contrato control/skin) + `https://openjfx.io/javadoc/21/javafx.controls/javafx/scene/chart/package-summary.html` (charts). Confirmar: `GraphicsContext`, contrato `Control`+`Skin`, charts disponíveis (`LineChart`/`BarChart`/`PieChart`/`AreaChart`...).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, javafx, magus, canvas, custom-controls]`, aliases `["Custom controls JavaFX", "Canvas", "Charts JavaFX"]`.

Conteúdo:
- `## O que é` — os 3 caminhos pra UI que não existe pronta: **compor** (Region + filhos), **estender** (Control + Skin), **desenhar** (Canvas).
- `## Por que importa` — saber escolher o caminho (e não cair direto no Canvas) é maturidade; o contraste com custom painting do Swing → linka [[10 - Custom painting e componentes customizados]] (Galho 5).
- `## Como funciona` — H3s: "Compor (Region/HBox com filhos + properties próprias — o caminho de 90% dos casos)", "Estender (`Control` + `Skin` — o contrato que separa estado de visual; quando vale o custo)", "Desenhar (`Canvas`/`GraphicsContext` — immediate mode DENTRO do retained; redesenho é seu; quando faz sentido: plot denso, jogo, visualização)", "Charts nativos (`LineChart`/`BarChart`/`PieChart` sobre `XYChart.Series` — visão geral; estilização via CSS, nota 09)", "Contraste com Swing (paintComponent vs scene graph + Canvas)".
- `## Na prática` — control composto (badge de status: Region + Label + properties + CSS); um Canvas com waveform/sparkline simples redesenhado sob demanda; um `LineChart` de pedidos/dia com `XYChart.Series`.
- `## Armadilhas` — ≥3: (1) Canvas pra tudo (perde CSS, eventos por node, acessibilidade — tudo manual) → compor primeiro; (2) esquecer que Canvas NÃO redesenha sozinho (resize → branco) → redesenhar em listener de width/height; (3) Skin acessando estado interno do Control por cast (acopla — quebra o contrato) → API de properties; (4) muitos milhares de nodes no scene graph quando 1 Canvas resolvia (custo de layout/pick) → medir e escolher.
- `## Em entrevista` + `## Veja também` (02, 09, [[03-Dominios/Tecnologia/Java/Swing/10 - Custom painting e componentes customizados|Custom painting (Swing)]], MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#Canvas (JavaFX)|Canvas (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#skin (Control)|skin (Dicionário)]]) + `## Referências`.

Tamanho: 280-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "Canvas|GraphicsContext|Skin|Control|LineChart|XYChart|Region" "03-Dominios/Tecnologia/Java/JavaFX/12 - Custom controls, Canvas e charts.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/12 - Custom controls, Canvas e charts.md"
git commit -m "feat(java): galho 6 nota 12 — custom controls, Canvas e charts"
```

---

### Task 13: Nota 13 — Empacotamento — módulos, jlink e jpackage  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage.md`

- [ ] **Step 1: Pesquisar fonte — VERIFICAÇÃO OBRIGATÓRIA**

WebFetch `https://openjfx.io/openjfx-docs/` (seções de runtime images / modular vs non-modular) + man pages `https://docs.oracle.com/en/java/javase/21/docs/specs/man/jpackage.html` e `https://docs.oracle.com/en/java/javase/21/docs/specs/man/jlink.html`. CONFIRMAR: nomes dos módulos JavaFX (`javafx.base`/`javafx.graphics`/`javafx.controls`/`javafx.fxml`/`javafx.media`/`javafx.web`), a mensagem real do erro de runtime components, sintaxe `--module-path`/`--add-modules`, jpackage = **JEP 392, Java 16** (confirmar via man page/release notes — openjdk.org 403), formatos de saída do jpackage (deb/rpm/msi/exe/dmg/pkg).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, javafx, magus, jpackage, jpms]`, aliases `["Empacotamento JavaFX", "jpackage", "jlink", "module-path"]`.

Conteúdo:
- `## O que é` — o caminho do código ao executável distribuível: JavaFX é um conjunto de **módulos JPMS** fora do JDK → o app precisa resolvê-los em dev e EMBARCÁ-LOS na distribuição (jlink/jpackage).
- `## Por que importa` — é onde a maioria trava ("roda na IDE, não roda fora"); o erro de runtime components é rito de passagem; distribuir app desktop sem pedir "instale o Java" é requisito real.
- `## Como funciona` — H3s: "JavaFX como módulos (`javafx.controls` puxa graphics/base; `javafx.fxml`; o que cada um traz)" → linka [[08 - JPMS — o sistema de módulos]] (**Galho 3**) pra mecânica de JPMS, sem re-explicar; "Module-path vs classpath (por que `java -jar` cru falha: **a mensagem real do erro** e as 2 saídas — `--module-path`+`--add-modules` ou launcher não-modular)", "App modular vs não-modular (com/sem module-info — trade-offs práticos)", "`jlink` (runtime enxuto com SEUS módulos + os do JavaFX; requer mundo modular)", "`jpackage` (JEP 392, Java 16 — instalador/app-image nativo por plataforma; funciona com app não-modular também; `--type`, ícone, versão)", "Native image (GraalVM/Gluon Substrate — menção de existência, 'Galho 17 (planejado)', sem wikilink)".
- `## Na prática` — o erro completo em ```text (`Error: JavaFX runtime components are missing, and are required to run this application`) + fix com `--module-path $JAVAFX_HOME/lib --add-modules javafx.controls,javafx.fxml`; um `jlink` de app modular (comando + output de tamanho ilustrativo); um `jpackage --type deb` (ou genérico) com as flags principais.
- `## Armadilhas` — ≥3: (1) `java -jar app.jar` com JavaFX no classpath (o launcher detecta e aborta — a mensagem famosa) → module-path ou classe launcher separada (main que não estende Application); (2) esquecer `--add-modules javafx.fxml` (FXML quebra em runtime com ClassNotFound) → listar todos os módulos usados; (3) jlink com app não-modular (não resolve automatic modules) → modularizar ou pular pro jpackage com runtime completo; (4) distribuir exigindo JRE instalado em 2026 (não existe mais JRE standalone confiável) → jpackage embarca o runtime.
- `## Em entrevista` + `## Veja também` (01, 11, 14, [[03-Dominios/Tecnologia/Java/JVM/08 - JPMS — o sistema de módulos|JPMS (Galho 3)]], MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#jlink|jlink (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#jpackage|jpackage (Dicionário)]]) + `## Referências`.

Tamanho: 300-460 linhas (version-sensitive; opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "javafx.controls|javafx.fxml|module-path|add-modules|jlink|jpackage|JEP 392|runtime components" "03-Dominios/Tecnologia/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/13 - Empacotamento — módulos, jlink e jpackage.md"
git commit -m "feat(java): galho 6 nota 13 — empacotamento (módulos, jlink e jpackage)"
```

---

### Task 14: Nota 14 — JavaFX hoje — estado do projeto e Swing vs JavaFX  ⟦opus⟧ (capstone)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/14 - JavaFX hoje — estado do projeto e Swing vs JavaFX.md`

- [ ] **Step 1: Pesquisar fonte — VERIFICAÇÃO OBRIGATÓRIA (governança/releases)**

Reler [[12 - Swing hoje - estado atual]] (Galho 5) — esta capstone é o par dela e NÃO pode contradizê-la (Swing = core Java SE suportado; "modo de manutenção" é jargão de comunidade, não termo oficial). WebFetch `https://openjfx.io/` (release atual, cadence) + `https://gluonhq.com/products/javafx/` (papel da Gluon, LTS comercial) + Scene Builder (`https://gluonhq.com/products/scene-builder/`). CONFIRMAR: versão atual do JavaFX, cadence (acoplada ao JDK — 2 releases/ano), o que é a Gluon (builds, LTS, Scene Builder), OpenJFX como projeto aberto (github.com/openjdk/jfx). **ZERO estatística de adoção inventada** — falar de sinais verificáveis (releases ativos, repositório, vendors), não de market share.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, javafx, magus, sintese, openjfx]`, aliases `["JavaFX hoje", "Swing vs JavaFX", "Estado do JavaFX"]`.

Conteúdo (capstone — liga o galho e fecha o par desktop):
- TL;DR: JavaFX está vivo e ativo (OpenJFX, releases semestrais, stewardship Gluon + comunidade), mas fora do JDK; a escolha Swing vs JavaFX é sobre contexto (legado/ecossistema vs reativo/CSS/moderno) — e às vezes a resposta é "nenhum dos dois".
- `## O que é` — o estado do projeto + o framework de decisão.
- `## Por que importa` — "desktop Java em 2026?" é pergunta real de entrevista; responder com a tabela mental de 2014 ("JavaFX substituiu o Swing") ou de 2010 ("JavaFX morreu") reprova igual.
- `## Como funciona` — H3s:
  - "Governança e releases (Oracle → OpenJFX; github.com/openjdk/jfx; cadence acoplada ao JDK; papel da Gluon: builds, LTS comercial, Scene Builder)" — fatos verificados, com hedge no que não confirmar.
  - "Sinais de vitalidade honestos (releases, features recentes confirmáveis no openjfx.io; SEM números de adoção)".
  - "Swing vs JavaFX — a decision matrix" (tabela: ecossistema/3rd-party, look nativo, CSS/temas, binding/reatividade, threading, empacotamento, contratação/legado, tooling) — **comparação justa**: quando Swing vence (legado grande, ecossistema de componentes, time que o domina) e quando JavaFX vence (app nova, MVVM/binding, theming, mídia). Cada linha conecta às notas dos dois galhos (linkar [[12 - Swing hoje - estado atual]]).
  - "Quando nenhum dos dois (web app, Electron/Tauri, mobile — menção honesta; Gluon Mobile existe — menção sem aprofundar)".
  - "O que o senior responde (frame de decisão, não torcida)".
- `## Na prática` — 2-3 cenários hipotéticos explícitos decidindo: manutenção de ERP Swing de 15 anos (fica Swing — e por quê); ferramenta interna nova de dados (JavaFX + MVVM); produto SaaS (web, desktop nem entra).
- `## Armadilhas` (de raciocínio) — ≥3: (1) "JavaFX morreu quando saiu do JDK" (desacoplar ≠ morrer — cadence própria é sinal de vida) → checar releases; (2) "Swing está deprecado" (não está — capstone do Galho 5) → não migrar por medo infundado; (3) reescrever app Swing estável em JavaFX "pra modernizar" sem requisito (custo/risco sem payoff) → migração pede motivo concreto; (4) citar estatística de adoção de blog (ninguém tem esse dado) → sinais verificáveis.
- `## Em entrevista` + `### Cheatsheet do galho` — tabela "qual nota pra qual problema" (setup→01, árvore→02, layout→03, widgets→04, eventos→05, view declarativa→06, reatividade→07, grid de dados→08, tema→09, não travar a UI→10, arquitetura→11, UI custom→12, distribuir→13) com wikilinks.
- `## Veja também` — (01, 07, 10, 11, 13, [[03-Dominios/Tecnologia/Java/Swing/12 - Swing hoje - estado atual|Swing hoje (Galho 5)]], [[03-Dominios/Tecnologia/Java/Swing/index|Swing (MOC do Galho 5)]], MOC, central, [[03-Dominios/Tecnologia/Java/Dicionário de Java#OpenJFX|OpenJFX (Dicionário)]], [[03-Dominios/Tecnologia/Java/Dicionário de Java#Gluon|Gluon (Dicionário)]]) + `## Referências`.

Tamanho: 320-500 linhas (fechamento; opus).

- [ ] **Step 3: Verificar**

```bash
grep -iE "decision|matrix|Gluon|OpenJFX|cadence|cheatsheet" "03-Dominios/Tecnologia/Java/JavaFX/14 - JavaFX hoje — estado do projeto e Swing vs JavaFX.md" | head
grep -riE "minha experiência|no meu projeto|josenaldo|Patient|% dos desenvolvedores|market share" "03-Dominios/Tecnologia/Java/JavaFX/14 - JavaFX hoje — estado do projeto e Swing vs JavaFX.md"
```
Expected: cobre decisão + cheatsheet; **segundo grep VAZIO** (zero fabricação/estatística).

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/14 - JavaFX hoje — estado do projeto e Swing vs JavaFX.md"
git commit -m "feat(java): galho 6 nota 14 — JavaFX hoje (capstone)"
```

---

## Task 15: MOC do galho

**Files:**
- Create: `03-Dominios/Tecnologia/Java/JavaFX/index.md`

- [ ] **Step 1: Escrever o MOC**

Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "JavaFX"`, tags `[java, javafx, moc]`, aliases `["Galho 6 - JavaFX", "OpenJFX (galho)"]`, `created`/`updated: 2026-06-06`. (Alias "OpenJFX (galho)" — evitar colidir com verbete; conferir.)

Conteúdo (modelar pelo `03-Dominios/Tecnologia/Java/JVM/index.md`):
- TL;DR — Galho 6; scene graph, FXML, properties/binding, CSS, Task/Service, MVVM, empacotamento, estado do projeto; 14 notas em 3 fases.
- `## Sobre este galho` — escopo + audiência + **refator com poda integral** do tronco `Frontend/JavaFX.md` + par desktop com [[03-Dominios/Tecnologia/Java/Swing/index|Swing (Galho 5)]] + fronteiras (teoria de UI thread → Galho 5; JPMS → Galho 3; concorrência → Galho 4).
- `## Iniciado` (01-05) / `## Adepto` (06-10) / `## Magus` (11-14) — wikilinks + 1 linha cada.
- `## Rotas alternativas` — 5:
  - **Completa** — 01 → 14.
  - **Entrevista internacional** — 01 → 02 → 07 → 10 → 14.
  - **Vindo do Swing** — 01 → 02 → 05 → 10 → 14.
  - **App de dados** — 04 → 06 → 07 → 08 → 09.
  - **Do código ao instalador** — 06 → 11 → 13.
- `## Todas as notas` — Dataview (`FROM "03-Dominios/Tecnologia/Java/JavaFX"`, `WHERE type = "concept"`).
- `## Veja também` — MOC central, Galhos 1/3/4/5 (index), Dicionário, `[[JavaFX]]` (tronco em transição).

- [ ] **Step 2: Verificar**

```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Tecnologia/Java/JavaFX/index.md"
grep -c "\[\[" "03-Dominios/Tecnologia/Java/JavaFX/index.md"
```
Expected: 4 headings; ≥14 wikilinks.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/JavaFX/index.md"
git commit -m "feat(java): galho 6 MOC — JavaFX"
```

---

## Task 16: Expandir o Dicionário de Java (NÃO recriar)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`

- [ ] **Step 1: Extrair as âncoras realmente usadas**

```bash
grep -rhoE "Dicionário de Java#[^]|]+" "03-Dominios/Tecnologia/Java/JavaFX/" | sort -u
```
Lista esperada (~22-26; ajustar ao grep): `binding (JavaFX)`, `Canvas (JavaFX)`, `cell factory / cell value factory`, `CSS do JavaFX (-fx-)`, `event dispatch chain (capturing / bubbling)`, `EventFilter / EventHandler`, `FXML`, `fx:id / @FXML`, `FXMLLoader`, `Gluon`, `JavaFX Application Thread`, `jlink`, `jpackage`, `layout pane`, `Modena`, `MVVM`, `node (scene graph)` (se usada), `ObservableList`, `OpenJFX`, `Platform.runLater`, `Property (JavaFX)`, `retained mode / immediate mode`, `Scene Builder`, `scene graph`, `skin (Control)`, `Stage / Scene`, `Task / Service (JavaFX)`.

- [ ] **Step 2: Ler o Dicionário inteiro e conferir duplicatas**

Formato `### Termo` + 1-3 linhas + `Veja também:`. **NÃO recriar/reordenar.** Conferir colisões com verbetes dos Galhos 1-5 (ex.: termos de EDT/Swing são do Galho 5; `jlink` pode NÃO existir ainda — o Galho 3 nota 13 menciona jlink mas o verbete não foi criado lá; conferir).

- [ ] **Step 3: Inserir em ordem alfabética** (case-insensitive, sem acento; criar seções se preciso). Cada verbete: heading EXATO da âncora + definição fiel às notas + `Veja também:` pra nota canônica (binding/Property→07; Canvas/skin→12; cell factory/ObservableList→08; CSS/Modena→09; eventos→05; FXML/fx:id/FXMLLoader/Scene Builder→06; Gluon/OpenJFX→14; Application Thread/Platform.runLater/Task-Service→10; jlink/jpackage→13; layout pane→03; MVVM→11; retained mode/scene graph/Stage-Scene→02). Atualizar `updated: 2026-06-06`.

- [ ] **Step 4: Verificar**

```bash
grep -E "^### (scene graph|FXML|Property \(JavaFX\)|jpackage|MVVM|Gluon)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: novos presentes; contagem subiu ~22-26 vs baseline (141).

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 6 (JavaFX)"
```

---

## Task 17: Ativar o Galho 6 no MOC central

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/index.md`

- [ ] **Step 1: Trocar a linha do item 6** (localizar por conteúdo: `6. JavaFX *(planejado)* — scene graph, FXML, properties/binding, CSS, estado atual do projeto`) por:

```markdown
6. [[03-Dominios/Tecnologia/Java/JavaFX/index|JavaFX]] — scene graph, FXML/Scene Builder, properties e binding, CSS, Task/Service e threading, MVVM, jlink/jpackage, estado do projeto (OpenJFX/Gluon)
```

Atualizar `updated: 2026-06-06`. Não mexer no resto.

- [ ] **Step 2: Verificar**

```bash
grep -E "JavaFX/index" "03-Dominios/Tecnologia/Java/index.md"
grep -c "planejado" "03-Dominios/Tecnologia/Java/index.md"
```
Expected: wikilink ativo; "planejado" caiu exatamente 1 vs baseline.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/index.md"
git commit -m "feat(java): ativa Galho 6 (JavaFX) no MOC central"
```

---

## Task 18: Poda INTEGRAL do tronco `Frontend/JavaFX.md`

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Frontend/JavaFX.md`

- [ ] **Step 1: Reler o tronco** (161 linhas; fabricação confirmada no pré-flight). A poda substitui **todo o corpo** após o H1.

- [ ] **Step 2: Substituir o corpo pelo callout** — o arquivo final fica (frontmatter preservado com `updated: 2026-06-06`; `publish: false` mantido):

```markdown
# JavaFX

Framework para aplicações desktop em Java — scene graph, FXML, properties/binding e CSS. Desacoplado do JDK desde o Java 11; vive como projeto OpenJFX.

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/JavaFX/index|JavaFX]]. Veja [[01 - JavaFX — o que é e como chega ao projeto]], [[02 - Scene graph — stage, scene e nodes]], [[07 - Properties e binding]], [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]], [[14 - JavaFX hoje — estado do projeto e Swing vs JavaFX]].
```

(Implementação sugerida: python3 substituindo de `## O que é` ao fim do arquivo, como na poda do Galho 3.)

- [ ] **Step 3: Verificar**

```bash
grep -nE "Patient|Josenaldo|minha experiência|is my choice" "03-Dominios/Tecnologia/Java/Frontend/JavaFX.md"
grep -c "Migrado para galho próprio" "03-Dominios/Tecnologia/Java/Frontend/JavaFX.md"
grep -E "publish: false" "03-Dominios/Tecnologia/Java/Frontend/JavaFX.md"
wc -l "03-Dominios/Tecnologia/Java/Frontend/JavaFX.md"
```
Expected: primeiro grep **VAZIO** (fabricação zerada); callout presente; `publish: false` mantido; arquivo ~25 linhas.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Frontend/JavaFX.md"
git commit -m "refactor(java): poda integral do tronco Frontend/JavaFX.md (galho 6) — zera fabricação"
```

---

## Task 19: Quitar a dívida reversa ("JavaFX planejado" → wikilinks)

**Files:**
- Modify: arquivos localizados na Task 0 Step 5

- [ ] **Step 1: Relocalizar (por conteúdo)**

```bash
grep -rni "javafx" "03-Dominios/Tecnologia/Java/Swing/" "03-Dominios/Tecnologia/Java/JVM/" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/" "03-Dominios/Tecnologia/Java/Collections e Streams/" "03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/" | grep -iE "planejado|galho 6"
```

- [ ] **Step 2: Converter cada ponteiro** pro wikilink mais específico, ajustando o texto pra não dizer mais "planejado":
- Menção a comparação/estado ("Swing vs JavaFX", capstone do Swing) → `[[03-Dominios/Tecnologia/Java/JavaFX/14 - JavaFX hoje — estado do projeto e Swing vs JavaFX|JavaFX hoje]]`
- Menção genérica ao galho (MOCs) → `[[03-Dominios/Tecnologia/Java/JavaFX/index|JavaFX (Galho 6)]]`
- Menção a um tema específico (binding, FXML, threading) → a nota correspondente (07/06/10)
**Não inventar links onde o contexto não pede.**

- [ ] **Step 3: Verificar**

```bash
grep -rni "javafx" "03-Dominios/Tecnologia/Java/Swing/" "03-Dominios/Tecnologia/Java/JVM/" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/" | grep -i "planejado"
```
Expected: VAZIO.

- [ ] **Step 4: Commit**

```bash
git add <cada arquivo editado, nominal>
git commit -m "refactor(java): quita dívida reversa — ponteiros 'JavaFX planejado' viram wikilinks"
```

---

## Task 20: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: 14 notas + MOC**

```bash
ls "03-Dominios/Tecnologia/Java/JavaFX/" | sort
```
Expected: 01..14 + index.md (15 arquivos).

- [ ] **Step 2: Fases (5/5/4)**

```bash
for f in "03-Dominios/Tecnologia/Java/JavaFX/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```

- [ ] **Step 3: Seções obrigatórias (3 por nota)**

```bash
for f in "03-Dominios/Tecnologia/Java/JavaFX/"[0-9]*.md; do echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"; done
```

- [ ] **Step 4: Anti-fabricação + wikilinks proibidos**

```bash
grep -riE "minha experiência|no meu projeto|josenaldo|Patient|getSpecialty|market share|% dos desenvolvedores" "03-Dominios/Tecnologia/Java/JavaFX/"
grep -rE "\[\[[^]]*(Spring|Jakarta|GraalVM|Gluon Mobile|Galho 1[5-8]|Galho [78])" "03-Dominios/Tecnologia/Java/JavaFX/"
grep -rn '\[\[#' "03-Dominios/Tecnologia/Java/JavaFX/"
```
Expected: todos VAZIOS.

- [ ] **Step 5: Frase pronta (1 por nota)**

```bash
for f in "03-Dominios/Tecnologia/Java/JavaFX/"[0-9]*.md; do echo "$f: $(grep -c '### Frase pronta (inglês)' "$f")"; done
```

- [ ] **Step 6: Skill `verificar-wikilinks`**

Rodar na pasta `03-Dominios/Tecnologia/Java/JavaFX/` + conferir (via report da pasta `03-Dominios/Java` filtrado) os arquivos tocados fora: `index.md` central, Dicionário, `Frontend/JavaFX.md`, arquivos da dívida reversa. Âncoras `Dicionário de Java#...` resolvem 1:1. Corrigir e commitar à parte se houver.

- [ ] **Step 7: Quartz** — build local não roda no pipeline deste repo (deploy cross-repo manual); registrar como verificação manual pendente.

- [ ] **Step 8: Resumo de fechamento (sem commit)** — reportar: 14 notas (5/5/4), verbetes, poda integral (fabricação zerada — mostrar o grep vazio), dívida reversa, wikilinks. Commits locais na `main`; **push manual do usuário**. Atualizar memória [[project_trilha_java]] com status e fatos cravados.

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** Tasks 1-14 ↔ §3.1 (14 notas, escopos idênticos); Task 15 ↔ §3.2 (MOC, 5 rotas iguais); Task 16 ↔ §3.3 (verbetes, âncoras 1:1); Task 17 ↔ §3.4; Task 18 ↔ §3.5 (poda integral, texto do callout idêntico ao spec); Task 19 ↔ §3.6; reciprocidade §3.7 honrada nos wikilinks de ida das notas 02/03/05/08/10/12 (Galho 5), 10 (Galho 4), 13 (Galho 3); Task 0 ↔ §6; Task 20 ↔ §7. Fronteiras: Spring/GraalVM só texto "(planejado)" (greps na Task 20 e na Task 11 garantem).

**Placeholder scan:** sem TBD/TODO; cada nota tem fontes nomeadas, frontmatter concreto, H3s, armadilhas mínimas com conteúdo real, tamanho-alvo. Notas version-sensitive (01 linha do tempo, 13 jpackage/módulos, 14 governança) com verificação obrigatória e instrução de hedge.

**Type/naming consistency:** numeração 01-14 idêntica entre tasks, MOC, Dicionário, poda e cheatsheet da capstone; distribuição 5/5/4 consistente; opus 07/10/13/14 marcadas ⟦opus⟧; filenames sem `:` nem `/` (em dash nos compostos); títulos vizinhos (Swing 03/04/05/06/08/10/12, JVM 08, Concorrência 12, Collections 04) assumidos e **reconfirmados na Task 0 Step 4**; âncoras do Dicionário extraídas por grep antes de inserir (Task 16) e validadas na Task 20.
