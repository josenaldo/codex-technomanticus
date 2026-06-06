---
title: "Spec — Galho 6 da trilha Java Senior (JavaFX)"
date: 2026-06-06
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 6 da trilha Java Senior (JavaFX)

## 1. Contexto e motivação

Este é o **sexto galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`). Pressupõe leitura do roadmap. Os Galhos 1 (Linguagem, 15 notas), 2 (Collections/Streams, 16), 3 (JVM, 14), 4 (Concorrência, 16) e 5 (Swing, 12) já fecharam e estão em `main` — seus artefatos são o **template de padrão e qualidade**. Fecha o par desktop iniciado pelo Galho 5.

**Galho de REFATOR DE TRONCO com poda INTEGRAL** (como o `Java Concurrency` no Galho 4): o tronco `Frontend/JavaFX.md` (161 linhas) é raso, desatualizado e **contaminado de fabricação** — o corpo inteiro vira callout. Consequências do pré-flight (§6):

- **Fabricação pesada no tronco** ([[feedback_no_fabrication]]): `patient-view.fxml`/`PatientController`/`TableView<Patient>` (sabor MedEspecialista), `new SimpleStringProperty("Josenaldo")`, seção `## Na prática (da minha experiência)` em 1ª pessoa ("Usei JavaFX em projetos...") e frase em inglês em 1ª pessoa ("JavaFX is my choice... I use Task<V>"). **A poda integral mata tudo.** As notas novas usam exemplos neutros.
- **Framing desatualizado no tronco**: "toolkit oficial da Oracle, substituindo o Swing" — errado hoje. JavaFX foi **desacoplado do JDK no Java 11**, vive como projeto OpenJFX (stewardship Gluon + comunidade), e o Swing segue core Java SE (capstone do Galho 5). A nota 01 mata esse framing logo na entrada.
- **Sem callout de migração prévio**: diferente do `Java Fundamentals`, o tronco não foi marcado "Migra em galho futuro" — a poda cria o callout direto.
- **Dívida reversa**: o Galho 5 deixou ganchos "JavaFX (planejado)" sem wikilink (regra do spec dele). Quitar aqui.

Galho 6 é o **dono de JavaFX** na trilha: scene graph, FXML, properties/binding, CSS, controls, threading da UI (Task/Service), arquitetura (MVVM), empacotamento e estado do projeto. Depende dos Galhos 1, 4 (threading) e 5 (comparação). **14 notas**.

## 2. Objetivo

Produzir, em sessão de execução dedicada **direto na `main`** ([[feedback_galhos_direto_main]]), **14 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central + poda integral do tronco + quitação da dívida reversa do Galho 5**, em `03-Dominios/Java/JavaFX/` e `03-Dominios/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (5 Iniciado + 5 Adepto + 4 Magus).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** o scene graph (retained mode), o modelo de properties/binding, o papel do FXML e a single-thread rule da JavaFX Application Thread.
- **Construir e justificar** uma tela de dados (TableView + ObservableList + bindings + CSS) com background work correto (Task/Service), sem bloquear a UI thread.
- **Decidir e defender** Swing vs JavaFX (vs web) para um cenário dado, com o estado atual de ambos os projetos na ponta da língua — sem estatística inventada.
- **Empacotar** uma app JavaFX moderna (module-path, jlink, jpackage) e explicar o erro clássico "JavaFX runtime components are missing".

A barra: "construir, decidir e defender em entrevista" — não "dominar cada control da API".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Java/JavaFX/`)

Pasta **nova**, flat. 14 notas + 1 MOC (`index.md`, Quartz folder-link). Numeração global. Tag de galho: `javafx`. (O tronco `Frontend/JavaFX.md` continua existindo como callout — sem conflito.)

#### Iniciado (5 notas — vocabulário + modelo mental)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | JavaFX — o que é e como chega ao projeto | História honesta: JavaFX 2 (2011) → bundled no JDK 8 → **desacoplado no Java 11**; OpenJFX; **não vem no JDK** — dependência Maven/Gradle ou SDK; primeira `Application` (lifecycle `init`/`start`/`stop`, `Stage`/`Scene`); launcher e o erro de classpath (teaser da 13). Mata o framing "substituto oficial do Swing". |
| 02 | Scene graph — stage, scene e nodes | A árvore de nós (retained mode — o framework redesenha, você descreve), `Node`/`Parent`/`Group`, coordenadas e transformações, efeitos; **diferença pro modelo de painting do Swing** (immediate mode em `paintComponent`) → linka [[10 - Custom painting e componentes customizados]] (Galho 5), sem re-explicar. |
| 03 | Layout panes | `VBox`/`HBox`/`BorderPane`/`GridPane`/`StackPane`/`FlowPane`/`AnchorPane`/`TilePane`; growth, constraints estáticos (`setHgrow`), padding/spacing/alignment; vs layout managers do Swing → linka [[03 - Layout managers]] (Galho 5). |
| 04 | Controls essenciais | `Button`/`Label`/`TextField`/`TextArea`/`CheckBox`/`RadioButton`/`ComboBox`/`ListView`/`TableView` (visão geral — profundidade na 08); `ObservableList` como backing (teaser da 08); prompt text, tooltip, disable. |
| 05 | Eventos — capturing, bubbling e handlers | Event dispatch chain (capturing → target → bubbling), `EventHandler` vs `EventFilter`, `consume()`, convenience methods (`setOnAction`); vs modelo de listeners do Swing → linka [[04 - O modelo de eventos]] (Galho 5). |

#### Adepto (5 notas — domínio operacional; 2 densas → opus)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 06 | FXML e Scene Builder | Layout declarativo em XML, `fx:id`/`fx:controller`/`@FXML`/`initialize()`, `FXMLLoader` (load, controller access), Scene Builder (Gluon — confirmar status); resources e i18n (`ResourceBundle`); quando FXML vs código puro (trade-offs honestos). |
| 07 | Properties e binding *(opus)* | `ObservableValue`/`Property`, implementações (`SimpleStringProperty` etc.), o padrão de property em POJOs JavaFX (método `xxxProperty()`), `bind`/`bindBidirectional`/`unbind`, invalidation vs change listeners (lazy evaluation!), `Bindings.*` e computed bindings (`createStringBinding`), weak listeners e leaks; quando binding clareia vs vira teia de dependências indebugável. O coração reativo do JavaFX. |
| 08 | TableView, cell factories e dados observáveis | `ObservableList`/`FXCollections`, `cellValueFactory` (dados) vs `cellFactory` (render), células customizadas (updateItem e suas regras), seleção (`selectionModel`), edição, `SortedList`/`FilteredList` (+ `comparatorProperty().bind`); análogo aos renderers/editors do Swing → linka [[08 - Renderers e editors]] (Galho 5). |
| 09 | CSS em JavaFX | Seletores (`.style-class`, `#id`, pseudo-classes `:hover`/`:focused`), propriedades `-fx-*`, stylesheets por Scene/Parent, ordem de precedência (inline > stylesheet de Parent > de Scene > user-agent), tema **Modena** (default), custom pseudo-classes; **CSS do JavaFX ≠ CSS web** (subset próprio, layout NÃO é CSS); temas claro/escuro. |
| 10 | A JavaFX Application Thread — Task, Service e Platform.runLater *(opus)* | Single-thread rule (igual EDT do Swing → linka [[05 - A Event Dispatch Thread]] e [[06 - SwingWorker e tarefas em background]] do Galho 5, sem re-explicar a teoria); `Platform.runLater` (e quando NÃO usar — coalescing manual); `Task<V>` (properties de progress/message/value **bindáveis** — a vantagem sobre SwingWorker), `Service<V>` (reusável, restart), `ScheduledService`; cancelamento cooperativo; virtual threads + JavaFX (citar impacto, linkar Galho 4 nota 12, sem re-explicar Loom). |

#### Magus (4 notas — maestria + decisão; 2 → opus)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 11 | Arquitetura — MVC, MVVM e injeção de dependência | Controller FXML como MVC "de view"; **MVVM com bindings** (o caso arquitetural forte do JavaFX: ViewModel com properties, View binda, zero referência reversa); `FXMLLoader.setControllerFactory` e DI (menção a Spring/CDI como texto "Galho 8 (planejado)", sem wikilink); testabilidade do ViewModel sem toolkit. |
| 12 | Custom controls, Canvas e charts | Os 3 caminhos: compor (`Region` + filhos), estender (`Control` + skin — o contrato), desenhar (`Canvas` — immediate mode dentro do retained, quando faz sentido); charts nativos (`LineChart`/`BarChart`/`PieChart` — visão geral); vs custom painting do Swing → linka [[10 - Custom painting e componentes customizados]] (Galho 5). |
| 13 | Empacotamento — módulos, jlink e jpackage *(opus)* | JavaFX como módulos JPMS (`javafx.controls`/`javafx.fxml`/`javafx.graphics`...) → linka [[08 - JPMS — o sistema de módulos]] (**Galho 3**); module-path vs classpath e o erro clássico "Error: JavaFX runtime components are missing"; `jlink` (runtime customizado com os módulos do JavaFX); **`jpackage` (JEP 392, Java 16 — confirmar)** pra instalador nativo (deb/rpm/msi/dmg); GraalVM native/Gluon Substrate como menção ("Galho 17 (planejado)", sem wikilink). |
| 14 | JavaFX hoje — estado do projeto e Swing vs JavaFX *(capstone, opus)* | Governança pós-Oracle: OpenJFX (projeto OpenJDK), papel da Gluon (releases, LTS comercial, Scene Builder), cadence acoplada ao JDK (release atual — **confirmar via WebFetch**); adoção honesta (**ZERO estatística inventada** — regra cravada no Galho 5); **decision matrix Swing vs JavaFX** (ecossistema/legado/estabilidade vs reativo/CSS/moderno) + quando nenhum dos dois (web/Electron — menção); o que o senior responde quando perguntam "desktop Java em 2026?". Linka [[12 - Swing hoje - estado atual]] (Galho 5). Liga o galho. |

**Decisões de fronteira (escopo NÃO coberto ou de outro dono):**

- **EDT, SwingWorker, teoria de UI single-thread** → **Galho 5 é dono** (notas 05/06). A nota 10 estabelece a regra do JavaFX e **linka** a teoria, sem re-explicar por que UI toolkits são single-threaded.
- **Concorrência (executors, virtual threads, cancelamento)** → **Galho 4 é dono**. Nota 10 cita e linka.
- **JPMS (module-info, module-path)** → **Galho 3 é dono** (nota 08). Nota 13 aplica ao JavaFX e linka, sem re-explicar delegation/requires.
- **Spring/CDI (injeção nos controllers)** → Galho 7/8 (futuros). Texto "(planejado)", **sem wikilink**. A integração Spring Boot+JavaFX que existia no tronco morre na poda (era o único conteúdo não-coberto; a nota 11 menciona `controllerFactory` como o gancho técnico, sem reconstruir o exemplo Spring).
- **GraalVM native image / Gluon Substrate** → Galho 17 (futuro). Texto "(planejado)", sem wikilink.
- **Lambdas/method references nos handlers** → Galho 2 (nota 04). Usar sem re-explicar; linkar quando didático.
- **Mobile (Gluon Mobile/Attach)** → fora do escopo da trilha; menção de existência na 14, sem nota.

### 3.2. MOC do galho

`03-Dominios/Java/JavaFX/index.md`:
- `type: moc`, `status: growing`, `title: "JavaFX"`, tags `java`/`javafx`/`moc`, aliases `["Galho 6 - JavaFX", "OpenJFX"]`
- TL;DR + "Sobre este galho" (refator com **poda integral** do tronco `Frontend/JavaFX.md`; par desktop com o Galho 5; fronteira: teoria de UI thread é do Galho 5, JPMS é do Galho 3)
- 3 H2 de fase (5/5/4) com linha descritiva por nota
- **Rotas alternativas (5):**
  - **Completa** — 01 → 14
  - **Entrevista internacional** — 01 → 02 → 07 → 10 → 14
  - **Vindo do Swing** — 01 → 02 → 05 → 10 → 14 (os contrastes, linkando o Galho 5)
  - **App de dados** — 04 → 06 → 07 → 08 → 09
  - **Do código ao instalador** — 06 → 11 → 13
- Dataview + "Veja também" (MOC central, Galhos 1/3/4/5, Dicionário, tronco `[[JavaFX]]` em transição)

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

Inserir ~22-26 verbetes em ordem alfabética (ajustar às âncoras reais na execução; conferir duplicatas — `EDT` etc. são do Galho 5):

`binding (JavaFX)`, `Canvas (JavaFX)`, `cell factory / cell value factory`, `CSS do JavaFX (-fx-)`, `event dispatch chain (capturing / bubbling)`, `EventFilter / EventHandler`, `FXML`, `fx:id / @FXML`, `FXMLLoader`, `Gluon`, `JavaFX Application Thread`, `jlink`, `jpackage`, `layout pane`, `Modena`, `MVVM`, `node (scene graph)`, `ObservableList`, `OpenJFX`, `Platform.runLater`, `Property (JavaFX)`, `retained mode / immediate mode`, `Scene Builder`, `scene graph`, `skin (Control)`, `Stage / Scene`, `Task / Service (JavaFX)`.

Headings 1:1 com as âncoras das notas (extrair e conferir, como nos galhos anteriores). Atualizar `updated:`.

### 3.4. MOC central (ativação do Galho 6)

Trocar a linha do item 6 (hoje: `6. JavaFX *(planejado)* — scene graph, FXML, properties/binding, CSS, estado atual do projeto`) por:

```markdown
6. [[03-Dominios/Java/JavaFX/index|JavaFX]] — scene graph, FXML/Scene Builder, properties e binding, CSS, Task/Service e threading, MVVM, jlink/jpackage, estado do projeto (OpenJFX/Gluon)
```

Atualizar `updated:`. Editar por conteúdo, não por número de linha.

### 3.5. Poda INTEGRAL do tronco

`Frontend/JavaFX.md` (161 linhas): o corpo inteiro (de `## O que é` ao fim) vira callout único, preservando frontmatter (atualizar `updated:`) + H1 + 1 linha de definição neutra:

```markdown
# JavaFX

Framework para aplicações desktop em Java — scene graph, FXML, properties/binding e CSS. Desacoplado do JDK desde o Java 11; vive como projeto OpenJFX.

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/JavaFX/index|JavaFX]]. Veja [[01 - JavaFX — o que é e como chega ao projeto]], [[02 - Scene graph — stage, scene e nodes]], [[07 - Properties e binding]], [[10 - A JavaFX Application Thread — Task, Service e Platform.runLater]], [[14 - JavaFX hoje — estado do projeto e Swing vs JavaFX]].
```

A poda **elimina a fabricação** (`Patient*`, `Josenaldo`, "da minha experiência", inglês em 1ª pessoa) e o framing desatualizado. `publish: false` permanece. Não deletar o arquivo (wikilinks externos: conferir com grep quem aponta pra `[[JavaFX]]` e validar que continuam resolvendo no callout).

### 3.6. Dívida reversa (ganchos "JavaFX (planejado)")

O Galho 5 deixou ganchos textuais "JavaFX... (planejado)" (regra do spec dele: sem wikilink pra galho inexistente). Grep na execução: `grep -rn "JavaFX" 03-Dominios/Java/Swing/ 03-Dominios/Java/JVM/ <MOCs>` filtrando "planejado"/"Galho 6". Converter cada um pra wikilink da nota mais específica (capstone 12 do Swing → [[14 - JavaFX hoje...]]; menções genéricas → MOC do galho). O MOC central é a §3.4 (separado).

### 3.7. Reciprocidade de links

Notas deste galho linkam os donos (ida): 02/03/05/08/12 → notas do Galho 5; 10 → Galho 5 (05/06) + Galho 4 (12 Virtual Threads); 13 → Galho 3 (08 JPMS). Os MOCs dos Galhos 3/5 ganham link de volta pro Galho 6 via dívida reversa (§3.6) onde houver gancho.

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos Galhos 1-5. Reforços:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
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
  - <específicas: scene-graph, fxml, binding, css, threading, tableview, mvvm, jpackage>
aliases:
  - <opcionais>
---
```

### 4.2. Estrutura H2 obrigatória

Idêntica aos galhos anteriores: TL;DR callout → `## O que é` → `## Por que importa` → `## Como funciona` (≥3 H3s em Adepto/Magus) → `## Na prática` (código compilável; framing neutro) → `## Armadilhas` (≥2 Iniciado / ≥3 Adepto-Magus, exemplo+fix) → `## Em entrevista` (`### Frase pronta (inglês)` 3+ sentenças + vocabulário 6+ termos, tabela `| Termo PT | Termo EN |`) → `## Veja também` (wikilinks SEM backticks, sem âncoras same-file; MOC galho + MOC central + Galhos 3/4/5 quando conectar + Dicionário) → `## Referências` (docs oficiais).

### 4.3. Restrições absolutas

1. **Sem fabricação** ([[feedback_no_fabrication]]). Exemplos neutros (`Order`/`Customer`/`Product`); **NUNCA** `Patient`/`Josenaldo` (ambos presentes no tronco atual — não copiar NADA do tronco). Hipotéticos explícitos.
2. **WebFetch obrigatório pra version-specific:** desacoplamento do JDK (Java 11), release atual do JavaFX e cadence, módulos JPMS do JavaFX (nomes), jpackage (JEP 392, Java 16), Scene Builder (Gluon, status atual), Gluon LTS, status de charts/Canvas. Fontes: `openjfx.io` (site oficial + docs), `gluonhq.com`, Javadoc OpenJFX (`openjfx.io/javadoc/`), JEPs via fallback (openjdk.org dá 403). Nada de memória.
3. **Tronco é contraexemplo, não matéria-prima**: raso, fabricado e desatualizado — as notas nascem das fontes oficiais.
4. **Code samples compiláveis** (Java moderno; FXML bem-formado; CSS válido de JavaFX). Fences `java`/`xml`/`css`/`bash`/`text`.
5. **Comparações justas** Swing×JavaFX (quando cada um vence) — capstone 14 é o ápice; sem estatística de adoção inventada (regra do Galho 5).
6. **Não linkar galhos inexistentes** (7/8/17) — texto "(planejado)".
7. **Higiene de commits** ([[feedback_commits]], [[feedback_galhos_direto_main]]): 1 commit/nota, add nominal (bot de backup roda em timer), subagents write-only + controlador commita, sem push, sem deploy.
8. **Tom graduado** por fase; Magus assume Galhos 1-5.

## 5. Conteúdo por nota (síntese)

Fontes-base: `openjfx.io` (Getting Started, docs), Javadoc OpenJFX (javafx.graphics/controls/fxml/base), CSS Reference Guide do JavaFX, Gluon (Scene Builder, LTS), JEP 392 (fallback). Por nota: ver tabela §3.1 (escopo nuclear) — armadilhas mínimas por nota definidas no plano de execução. Destaques de verificação:

- **01**: linha do tempo (JavaFX 2 em 2011, bundled JDK 8, desacoplado Java 11) — confirmar em openjfx.io/dev.java; coordenadas Maven (`org.openjfx:javafx-controls`).
- **07**: API de properties/bindings no Javadoc `javafx.base` (invalidation vs change, lazy evaluation, `Bindings`).
- **09**: CSS Reference Guide oficial (seletores, precedência, Modena como default).
- **10**: Javadoc `javafx.concurrent` (`Task`/`Service`/`ScheduledService`), `Platform.runLater`.
- **13**: nomes dos módulos JavaFX; mensagem real do erro de runtime components; `jpackage` (JEP 392, Java 16) e `jlink` — man pages Oracle.
- **14**: governança OpenJFX/Gluon, release atual e cadence — openjfx.io/gluonhq.com; ZERO números de adoção.

## 6. Pré-flight (executado nesta fase de brainstorming)

1. **Tronco lido** (`Frontend/JavaFX.md`, 161 linhas): raso, sem callout de migração, **fabricação confirmada** (`patient-view.fxml`/`PatientController`/`TableView<Patient>`, `SimpleStringProperty("Josenaldo")`, `## Na prática (da minha experiência)` 1ª pessoa, inglês 1ª pessoa) e framing desatualizado ("toolkit oficial da Oracle, substituindo o Swing").
2. **Galho 5 mapeado**: 12 notas; alvos de comparação 03 (layouts), 04 (eventos), 05 (EDT), 06 (SwingWorker), 08 (renderers), 10 (custom painting), 12 (Swing hoje). Ganchos "JavaFX (planejado)" = dívida reversa.
3. **Galho 3 nota 08 (JPMS)** existe — alvo do link da nota 13.
4. **Roadmap §5 Galho 6 confirmado**: escopo, dependências (1, 4, 5), tronco a podar.
5. **Verificações version-specific na execução**: ver §4.3.2.

Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

1. 14 notas em `03-Dominios/Java/JavaFX/`, frontmatter completo com `fase:`, `publish: true`, distribuição 5/5/4.
2. MOC do galho (3 fases + 5 rotas + dataview + `index.md` presente).
3. Dicionário **expandido** (~22-26 verbetes, ordem alfabética, âncoras 1:1, sem duplicar, anteriores intactos, `updated` atualizado).
4. MOC central com Galho 6 ativado; resto intacto.
5. **Poda integral executada**: `Frontend/JavaFX.md` reduzido a frontmatter + H1 + definição neutra + callout; fabricação e 1ª pessoa **zeradas** no arquivo; `publish: false` mantido; wikilinks externos pro tronco continuam resolvendo.
6. **Dívida reversa quitada**: ganchos "JavaFX (planejado)" nos galhos fechados viram wikilinks.
7. Cada nota: TL;DR; 3-5 code samples; "Em entrevista" completa; "Armadilhas" com exemplo+fix (≥2/≥3); wikilinks (galho + central + Galhos 3/4/5 quando conectar + Dicionário); Referências oficiais.
8. Zero fabricação; comparações Swing×JavaFX justas; zero estatística de adoção inventada; version-specific via WebFetch.
9. 1 commit/nota; sem Co-Authored-By; sem `--no-verify`; add nominal; direto na `main`; **sem push, sem deploy**.
10. `verificar-wikilinks` limpo na pasta do galho e em todos os arquivos tocados fora dela; sem âncoras same-file.

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Copiar exemplo do tronco (Patient/Josenaldo) | Tronco declarado contraexemplo (§4.3.3); notas nascem das fontes; greps anti-fabricação na verificação final. |
| Framing desatualizado ("substituto do Swing", "vem no JDK") | Nota 01 mata na entrada com linha do tempo verificada; capstone 14 consolida estado atual. |
| Estatística de adoção inventada na 14 | Regra cravada do Galho 5: zero números sem fonte; falar de governança/cadence/sinais, não de market share. |
| Re-explicar EDT/threading (Galho 5/4) ou JPMS (Galho 3) | Fronteiras §3.1; nota 10 linka teoria, nota 13 linka JPMS; reviews por fase checam. |
| Versões erradas (desacoplamento, jpackage, release atual) | WebFetch obrigatório (§4.3.2); hedge no que não confirmar. |
| CSS do JavaFX confundido com CSS web | Nota 09 explicita o subset e as diferenças; exemplos só com propriedades `-fx-*` reais (CSS Reference Guide). |
| Quebrar wikilinks de quem aponta pro tronco `[[JavaFX]]` | Poda preserva o arquivo e o H1; grep por `[[JavaFX]]` na verificação; o alias do MOC do galho ("OpenJFX") não colide. |
| Race com bot de backup | Padrão consolidado: subagents write-only; controlador commita nominal logo após cada arquivo. |
| Galho inflar (TableView/properties densos) | Tópicos divididos (04 visão geral / 08 profundidade; 07 isolada); [[feedback_notas_atomicas]] se passar. |

## 9. Próximos passos

1. **Aprovação deste spec** ✅ (mapa aprovado no brainstorming em 2026-06-06)
2. **Plano de execução** via `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-06-java-galho-06-javafx-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` direto na `main` (subagents write-only; sonnet, **opus nas 07/10/13/14**; review POR FASE + fix loop; controlador commita)
4. **Poda integral** do tronco + **dívida reversa** do Galho 5
5. **Verificação** (wikilinks, âncoras do Dicionário, greps anti-fabricação)
6. **Revisão do roadmap** antes do próximo galho

## 10. Documentos relacionados

- Roadmap: `2026-06-02-java-senior-roadmap-design.md`
- Specs/planos dos Galhos 1-5 (templates) — em especial Galho 5 (Swing, par desktop) e Galho 4 (poda integral de tronco)
- Tronco a podar: `03-Dominios/Java/Frontend/JavaFX.md` (poda integral)
- Artefatos a atualizar: `Dicionário de Java.md`, `03-Dominios/Java/index.md`, notas/MOCs com gancho "JavaFX (planejado)"
- Fontes-base: openjfx.io (+ Javadoc), CSS Reference Guide, gluonhq.com, JEP 392 (fallback), man pages jlink/jpackage
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]], [[feedback_galhos_direto_main]], [[feedback_notas_atomicas]]
