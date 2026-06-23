---
title: "Spec — Galho 5 da trilha Java Senior (Swing)"
date: 2026-06-03
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 5 da trilha Java Senior (Swing)

## 1. Contexto e motivação

Este é o **quinto galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda. Os Galhos 1 (Linguagem, 15 notas) e 4 (Concorrência, 16 notas) já fecharam e mergearam em `main` — seus artefatos são o **template de padrão e qualidade** deste galho.

**Diferença estrutural decisiva: este é o primeiro galho construído POR PESQUISA, não por refator de monolito.** O roadmap (§5, Galho 5) confirma: **"Tronco a podar: nenhum (galho novo)."** Não existe `Swing.md` para refatorar. As notas **nascem de docs oficiais** (`docs.oracle.com` / `dev.java` / The Java Tutorials — *Creating a GUI with Swing*) verificadas via WebFetch. Consequências:

- **Sem seção de poda** (§6 do spec do Galho 4 não tem equivalente aqui).
- **Sem pré-flight de leitura de tronco.** No lugar dele: pré-flight = **confirmar o estado atual de manutenção/adoção do Swing via fonte oficial**, sem inventar números (ver §6).
- A matéria-prima é a documentação oficial, não um texto pré-existente do autor — atenção redobrada à fabricação (todo exemplo é neutro ou hipotético explícito).

Swing é a primeira das duas interfaces desktop da trilha (Galho 6 = JavaFX). Posicionado **após Concorrência** (Galho 4) por causa da **Event Dispatch Thread (EDT)**: o modelo de threading do Swing só faz sentido depois que o leitor domina threads, executors e a noção de single-thread confinement.

**Atenção ao estado atual (capstone, nota 12):** "modo de manutenção" é **jargão da comunidade, não termo oficial da Oracle**. O pré-flight (§6) confirmou via [Java Client Roadmap Update (Oracle, 2018)](https://www.oracle.com/docs/tech/java/javaclientroadmapupdate2018mar.pdf) e [Java Client Roadmap Updates (blogs.oracle.com)](https://blogs.oracle.com/java/post/java-client-roadmap-updates) que **Swing e AWT são "core Java SE technologies"**, suportados enquanto o JDK for suportado — não deprecados, não removidos. A capstone deve separar honestamente *o que a Oracle declara* (suporte como tecnologia core) de *o consenso de-facto da comunidade* (poucas features novas, papel de nicho hoje), sem inventar estatísticas e sem virar nem obituário nem panfleto.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **12 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central**, em `03-Dominios/Tecnologia/Java/Swing/` e `03-Dominios/Tecnologia/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (4 Iniciado + 5 Adepto + 3 Magus). **Sem poda** (galho novo).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** o modelo de componentes do Swing (lightweight vs heavyweight/AWT), o contrato da EDT (single-thread rule) e a arquitetura MVC/separable-model.
- **Escolher e justificar** o layout manager certo, o model certo (`TableModel`/`ListModel`/`Document`) e a estratégia de threading (`invokeLater` vs `SwingWorker`) para um cenário dado.
- **Reconhecer e diagnosticar** em code review as armadilhas clássicas (tocar componente fora da EDT, bloquear a EDT, null layout, `KeyListener` onde `InputMap`/`ActionMap` é correto).
- **Decidir e defender honestamente** quando Swing ainda faz sentido (ferramentas internas, IDEs, apps offline/legados) e quando não (app moderno rico/web/mobile), com o status real da API na ponta da língua.

A barra é "decidir, justificar, reconhecer patterns e armadilhas em code review" — não "implementar um toolkit de UI from scratch".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Tecnologia/Java/Swing/`)

Pasta **nova**, flat. 12 notas + 1 MOC. Numeração global por galho (não reinicia por fase). Pasta precisa de `index.md` (Quartz folder-link).

#### Iniciado (4 notas — vocabulário + modelo mental)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | O modelo do Swing | O que é Swing; **lightweight (Swing) vs heavyweight (AWT)** e a relação com o AWT; hierarquia `Component`→`Container`→`JComponent`; top-level containers (`JFrame`/`JDialog`/`JWindow`) e o **content pane**; arquitetura pluggable look-and-feel (intro, deep na 09); estrutura de um primeiro app. Porta de entrada do galho. |
| 02 | Componentes e containers | Catálogo de widgets: `JButton`/`JLabel`/`JTextField`/`JTextArea`/`JPasswordField`, `JCheckBox`/`JRadioButton`+`ButtonGroup`, `JComboBox`/`JList`, `JTable`/`JTree` (intro — models vêm na 07), containers intermediários (`JPanel`/`JScrollPane`/`JTabbedPane`/`JSplitPane`), menus (`JMenuBar`/`JMenu`/`JMenuItem`), `JToolBar`, diálogos (`JDialog`/`JOptionPane`). Panorâmica de vocabulário. |
| 03 | Layout managers | `BorderLayout`, `FlowLayout`, `GridLayout`, `BoxLayout`, `CardLayout`, `GroupLayout`, `GridBagLayout` (o power tool, com `GridBagConstraints`); aninhamento de painéis; `preferred`/`minimum`/`maximum` size; **null layout (posicionamento absoluto) como anti-pattern**. |
| 04 | O modelo de eventos | Modelo event-driven (delegation event model); listeners (`ActionListener`, `MouseListener`, `KeyListener`, `FocusListener`, `WindowListener`); event objects (`ActionEvent`, `MouseEvent`); lambdas vs classes anônimas vs adapters (`MouseAdapter`); o observer pattern por trás. **Linka pro Galho 1** (interfaces funcionais / lambdas). |

#### Adepto (5 notas — domínio operacional; 3 densas → opus)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 05 | A Event Dispatch Thread (EDT) *(opus)* | A **single-thread rule**; por que a GUI é single-threaded; o que roda na EDT (event handling + painting); a regra de ouro (não bloquear a EDT; não tocar componentes fora da EDT); `SwingUtilities.invokeLater`/`invokeAndWait`; `SwingUtilities.isEventDispatchThread`. **Dono do "como o Swing usa threads"; linka pro Galho 4** (02 Threads) pros primitivos, sem re-explicar concorrência. |
| 06 | SwingWorker e tarefas em background *(opus)* | `SwingWorker<T,V>`: `doInBackground`/`publish`/`process`/`done`, progress (`setProgress`/`PropertyChangeListener`), cancelamento, `get()`; o handoff worker→EDT; `javax.swing.Timer` (vs `java.util.Timer`). **Linka pro Galho 4** (08 Executors) sem re-explicar pools. |
| 07 | MVC em Swing e os models *(opus)* | A arquitetura **separable model** (o "MVC" pragmático do Swing); `TableModel`/`AbstractTableModel`/`DefaultTableModel`, `ListModel`/`AbstractListModel`/`DefaultListModel`, `ComboBoxModel`, `Document` (texto), `TreeModel`; **model listeners** (`TableModelListener`) e como a view reage; selection models. Por que separar dados de apresentação. |
| 08 | Renderers e editors | Cell renderers (`TableCellRenderer`/`ListCellRenderer`/`DefaultTableCellRenderer`), cell editors (`TableCellEditor`), o **rubber-stamp pattern** (um componente reusado pra pintar N células), rendering customizado em `JTable`/`JList`/`JComboBox`. Par natural com a 07. |
| 09 | Look & Feel e temas | L&F plugável; Metal/Nimbus/system/Motif (bundled no JDK); `UIManager` (defaults, trocar L&F em runtime, `updateComponentTreeUI`); **FlatLaf** como o L&F moderno de-facto da comunidade (open-source, **third-party — não-Oracle**, com 1 snippet de setup e ressalva explícita de dependência externa); intro a borders (`BorderFactory`) e fontes. |

#### Magus (3 notas — maestria + decisão de arquitetura; capstone → opus)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 10 | Custom painting e componentes customizados | `paintComponent(Graphics)` e `Graphics2D` (shapes, antialiasing via `RenderingHints`); a paint chain (`paint`→`paintComponent`/`paintBorder`/`paintChildren`); **double buffering** (default no Swing); `repaint(Rectangle)` vs `revalidate`; estender `JComponent`/`JPanel` pra criar componentes reutilizáveis; `getPreferredSize`. |
| 11 | Action API, key bindings e performance | **Action API** (`javax.swing.Action`/`AbstractAction` — encapsula comportamento + estado `enabled` + texto/ícone, compartilhado entre botão/menu/toolbar); **key bindings** (`InputMap`/`ActionMap` e por que vencem `KeyListener`); responsividade (manter a EDT livre, lazy/virtual models pra `JTable`/`JList` grandes, `repaint` de região). Liga de volta à EDT (05) e ao SwingWorker (06). |
| 12 | Swing hoje — estado atual *(capstone, opus)* | Status de suporte/manutenção: **frase honesta separando declaração oficial Oracle (Swing/AWT = core Java SE, suportado enquanto o JDK for) de consenso de-facto da comunidade (poucas features novas, papel de nicho)** — com fonte + data, **sem estatísticas inventadas**; onde Swing ainda faz sentido (ferramentas internas, IDEs — IntelliJ/NetBeans/Eclipse usam Swing, apps offline/desktop legados, embedded) vs onde não (app moderno rico/web/mobile); **Swing × virtual threads** com honestidade (EDT continua single-thread; virtual threads não mudam o modelo da EDT — verificar); **gancho pro Galho 6 (JavaFX)** SEM comparar a fundo (texto "planejado", sem wikilink quebrado); munição de entrevista enquadrada como decisão de arquitetura honesta. **WebFetch obrigatório** (Oracle roadmap + dev.java). |

**Decisões de fronteira (escopo NÃO coberto aqui ou de outro dono):**
- **Threading base (threads, executors, virtual threads)** → Galho 4 é dono. As notas 05 (EDT) e 06 (SwingWorker) são donas do *threading do Swing* (single-thread rule, `invokeLater`, `SwingWorker`) e **linkam** pra `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência]]` e notas específicas (02 Threads, 08 Executors) — **não re-explicam** concorrência base.
- **`Swing × virtual threads`** → a honestidade é: a EDT permanece single-thread; virtual threads ajudam o *trabalho de background* (como `SwingWorker` ou executors), não substituem a EDT. Citar com status verificado, sem hype.
- **JavaFX** → Galho 6 (próximo). É **dono** da comparação Swing vs JavaFX. O Galho 5 deixa só um **gancho** na capstone (12); **NÃO** comparar a fundo, **NÃO** linkar notas inexistentes do Galho 6 — usar texto "planejado" no MOC.
- **OOP / interfaces / lambdas** → Galho 1. A nota 04 (eventos) e a 10 (componentes customizados) linkam pro Galho 1 quando o conceito conectar, sem re-ensinar OOP.
- **`JTable` (o tópico mais pesado)** se distribui: catálogo na 02, model na 07, renderers/editors na 08, performance na 11 — nenhuma nota sozinha vira monstro.

### 3.2. MOC do galho

`03-Dominios/Tecnologia/Java/Swing/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "Swing"`, tags `java`/`swing`/`moc`, aliases `["Swing", "Galho 5 - Swing"]`)
- TL;DR callout (galho cobre GUI desktop Swing: componentes, layouts, eventos, EDT/SwingWorker, MVC/models, L&F, custom painting e o estado atual da API)
- "Sobre este galho" + audiência primária/secundária + nota de que é o primeiro galho construído por pesquisa (sem tronco)
- Conteúdo agrupado em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 12 notas (uma linha descritiva cada, no padrão dos MOCs dos Galhos 1 e 4)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 12 em ordem
  - **Entrevista internacional** — 01 → 04 → 05 → 06 → 07 → 12 (modelo, eventos, EDT, SwingWorker, MVC, estado atual — o que mais cai)
  - **Threading do Swing** — 05 → 06 → 11 (EDT, SwingWorker, performance/responsividade) — liga ao Galho 4
  - **Construir uma tela do zero** — 01 → 02 → 03 → 04 → 07 (montar uma UI funcional com dados)
  - **Aparência e customização** — 03 → 09 → 08 → 10 (layouts, L&F, renderers, custom painting)
- "Veja também": MOC central `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]`, Galho 1 (Linguagem), Galho 4 (Concorrência), Galho 6 (JavaFX, **planejado** — texto sem wikilink), Dicionário de Java
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Tecnologia/Java/Dicionário de Java.md` já existe (criado no Galho 1, expandido no Galho 4, `type: glossary`, seções alfabéticas). Este galho **expande** o arquivo existente inserindo os verbetes de Swing **em ordem alfabética case-insensitive (sem acento)** nas seções apropriadas, criando seções novas quando necessário. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Atualizar `updated: 2026-06-03` no frontmatter.

Verbetes a inserir (~20-24):

`Action API`, `adapter (event adapter)`, `AWT (Abstract Window Toolkit)`, `cell renderer`, `cell editor`, `componente lightweight / heavyweight`, `content pane`, `delegation event model`, `Document (modelo de texto)`, `double buffering`, `EDT (Event Dispatch Thread)`, `FlatLaf`, `GridBagLayout`, `InputMap / ActionMap (key bindings)`, `invokeLater / invokeAndWait`, `JComponent`, `layout manager`, `listener (event listener)`, `look and feel (L&F)`, `Nimbus`, `paintComponent / custom painting`, `pluggable look-and-feel`, `separable model (MVC do Swing)`, `SwingWorker`, `TableModel / ListModel`, `UIManager`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho. **Conferir 1:1** que os headings dos verbetes batem EXATAMENTE com as âncoras usadas nas notas (extrair as âncoras de Dicionário das notas e conferir, como no Galho 4).

### 3.4. MOC central (ativação do Galho 5)

`03-Dominios/Tecnologia/Java/index.md` já existe e lista os 18 galhos. Task **mínima**: trocar a linha 32 (atualmente `5. Swing *(planejado)* — componentes, layout managers, EDT, MVC, estado atual de adoção`) por um wikilink ativo no padrão das linhas 25/28:

```markdown
5. [[03-Dominios/Tecnologia/Java/Swing/index|Swing]] — componentes e containers, layout managers, modelo de eventos, EDT/SwingWorker, MVC/models, Look & Feel, custom painting, estado atual da API
```

Atualizar `updated: 2026-06-03`. Não mexer no resto do MOC central.

### 3.5. Sem poda

**Galho novo, sem tronco.** Não há `Swing.md` a podar. (O `Frontend/JavaFX.md`, 161 linhas, é tronco do **Galho 6**, não deste.) Nenhuma task de poda; nenhuma higienização de monolito.

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos Galhos 1 e 4. Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-03
updated: 2026-06-03
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - swing
  - <fase>
  - <tags específicas: componentes, layout, eventos, edt, swingworker, mvc, model, renderer, look-and-feel, painting>
aliases:
  - <aliases opcionais>
---
```

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2)
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis; framing neutro ("padrão observado no JDK/em IDEs Swing", "caso típico em ferramenta interna"); NUNCA "no meu projeto"
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com descrição + exemplo curto de código demonstrando o problema + fix em 1 linha
- `## Em entrevista` — frase pronta em inglês com **3+ sentenças** (trade-off + decisão + caveat) + vocabulário **6+ termos PT→EN**
- `## Veja também` — wikilinks **SEM backticks**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Tecnologia/Java/Swing/index|MOC do galho]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando o conceito conectar) `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência]]` / Galho 1 + verbetes do Dicionário. **Evitar âncoras same-file `[[#Heading]]`** (falso-positivo no checker).
- `## Referências` — docs oficiais (dev.java, docs.oracle.com/The Java Tutorials), JEPs quando relevantes, projetos open-source identificados (FlatLaf, OpenJDK). **Toda nota é fundada em fonte oficial verificada via WebFetch** (galho de pesquisa).

### 4.3. Restrições absolutas

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `OrderTableModel`) ou hipotéticos explícitos (`// hipotético: ...`). NUNCA `josenaldo` nem casos vividos. **Atenção redobrada na capstone (12): nenhuma estatística inventada** ("X% das empresas usam Swing") nem status fabricado — só o que a fonte oficial declara, com data.
2. **Sem invenção** de APIs/componentes/comportamentos. Como é galho de pesquisa, **WebFetch é obrigatório no Step 1 de cada nota** pra fundar o conteúdo em doc oficial; nada de API "de memória" sem conferir.
3. **Code samples compiláveis** — Swing válido; preferir snippets executáveis (classe `main` com `SwingUtilities.invokeLater`). Ao mostrar um bug de threading (tocar componente fora da EDT), deixar explícito que o sintoma é não-determinístico.
4. **Comparações justas** — ao comparar (lightweight vs heavyweight, `invokeLater` vs `SwingWorker`, `KeyListener` vs `InputMap`, Swing vs JavaFX/web), incluir "quando X" E "quando Y". Sem dogma. A capstone é o ápice dessa exigência (nem obituário nem panfleto).
5. **Status hedged + datado** — "Swing/AWT são tecnologias core do Java SE, suportadas enquanto o JDK for (Oracle Java Client Roadmap, 2018/2020); na prática recebem poucas features novas — verifique a release atual" em vez de "Swing está morto/em manutenção" cru.
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar notas do Galho 6 (JavaFX, inexistente)** — usar texto "planejado".
7. **Code fences corretos:** ` ```java ` pra código, ` ```text ` pra output/stack trace. Sempre fechadas.
8. **`fase:` no frontmatter + na tag** — obrigatório.
9. **Higiene de commits** — sem `Co-Authored-By: Claude`, sem `--no-verify`, `git add <path>` nominal, 1 commit por nota.
10. **Tom pedagógico graduado** — Iniciado assume pouco; Magus assume domínio dos anteriores e dos Galhos 1 e 4 (EDT pressupõe a noção de thread).

## 5. Conteúdo por nota (síntese)

Esboço do recorte. **Toda nota funda-se em doc oficial verificada via WebFetch** (não há tronco a copiar). Fontes-base: The Java Tutorials — *Creating a GUI with Swing* (`docs.oracle.com/javase/tutorial/uiswing/`), `dev.java`, Javadoc de `javax.swing`.

- **01 — O modelo do Swing.** O que é Swing (toolkit de GUI sobre o AWT); lightweight (Swing, desenhado em Java) vs heavyweight (AWT, peers do SO); hierarquia `Component`→`Container`→`JComponent`; top-level containers (`JFrame`/`JDialog`/`JWindow`) e o content pane; `pack`/`setVisible`/`setDefaultCloseOperation`; intro à arquitetura pluggable L&F. Armadilhas: misturar componentes AWT e Swing; esquecer `setVisible(true)`; construir a UI fora da EDT (teaser da 05). Fontes: Tutorial "About the JFC and Swing", "A Visual Guide to Swing Components".
- **02 — Componentes e containers.** Catálogo: botões/labels/campos de texto, seleção (`JCheckBox`/`JRadioButton`+`ButtonGroup`, `JComboBox`, `JList`), tabelas/árvores (intro), containers (`JPanel`/`JScrollPane`/`JTabbedPane`/`JSplitPane`), menus, `JToolBar`, diálogos (`JOptionPane`). Armadilhas: adicionar muitos componentes sem `JScrollPane`; `JList`/`JTable` sem model adequado (aponta pra 07); `JOptionPane` chamado fora da EDT. Fontes: "Using Swing Components".
- **03 — Layout managers.** Cada layout, quando usar, `GridBagConstraints`, aninhamento de painéis, sizing. Armadilhas: **null layout** (quebra em resize/DPI); abusar de `GridBagLayout` onde `BoxLayout` resolve; ignorar `preferredSize`. Fontes: "Laying Out Components Within a Container".
- **04 — O modelo de eventos.** Delegation event model, listeners e event objects, lambda vs anônima vs adapter, registro/remoção de listeners. **Linka pro Galho 1** (interfaces funcionais). Armadilhas: trabalho pesado no listener (bloqueia EDT — aponta pra 05/06); segurar referência e vazar listener; `KeyListener` pra atalho global (aponta pra 11). Fontes: "Writing Event Listeners".
- **05 — A Event Dispatch Thread (EDT) (opus).** Single-thread rule, o que roda na EDT, a regra de ouro, `invokeLater`/`invokeAndWait`, `isEventDispatchThread`. **Dono do threading do Swing.** Linka Galho 4 (02). Armadilhas: atualizar componente de uma thread de background (corrupção/erro intermitente) → fix `invokeLater`; `invokeAndWait` na própria EDT (deadlock); construir a UI na `main` em vez da EDT. Fontes: "Concurrency in Swing"; Javadoc `SwingUtilities`.
- **06 — SwingWorker e tarefas em background (opus).** `SwingWorker<T,V>` e seu ciclo, `publish`/`process`/`done`, progress, cancelamento, `get()`, `javax.swing.Timer`. Linka Galho 4 (08). Armadilhas: ler `get()` na EDT antes de `done` (bloqueia); atualizar UI dentro de `doInBackground` (fora da EDT); ignorar exceção engolida em `done`. Fontes: "Worker Threads and SwingWorker"; Javadoc `SwingWorker`.
- **07 — MVC em Swing e os models (opus).** Separable model, `TableModel`/`AbstractTableModel`/`DefaultTableModel`, `ListModel`, `ComboBoxModel`, `Document`, `TreeModel`, model listeners, selection models. Armadilhas: mutar dados do model sem disparar `fireTableDataChanged` (view dessincroniza); usar `DefaultTableModel` com `Vector` cru onde um `AbstractTableModel` tipado é melhor; lógica de negócio no renderer (aponta pra 08). Fontes: "How to Use Tables", "How to Use Lists"; Javadoc `TableModel`.
- **08 — Renderers e editors.** `TableCellRenderer`/`ListCellRenderer`/`DefaultTableCellRenderer`, `TableCellEditor`, rubber-stamp pattern, customização. Armadilhas: criar um `new JLabel` por célula (vaza performance — reusar o componente); estado mutável no renderer; editor sem `stopCellEditing`. Fontes: "Using Custom Renderers"; Javadoc `TableCellRenderer`.
- **09 — Look & Feel e temas.** Pluggable L&F, `UIManager`, Metal/Nimbus/system/Motif, trocar L&F + `updateComponentTreeUI`, **FlatLaf** (third-party, open-source, com setup e ressalva), `BorderFactory`, fontes. Armadilhas: setar L&F depois de criar componentes (sem `updateComponentTreeUI`); assumir que system L&F existe em todo SO; hard-coded colors quebrando no dark mode. Fontes: "Modifying the Look and Feel"; Javadoc `UIManager`; repo/docs FlatLaf (identificado como third-party).
- **10 — Custom painting e componentes customizados.** `paintComponent`/`Graphics2D`, paint chain, `RenderingHints` (antialias), double buffering, `repaint`/`revalidate`, estender `JComponent`/`JPanel`, `getPreferredSize`. Armadilhas: sobrescrever `paint` em vez de `paintComponent`; não chamar `super.paintComponent` (artefatos); desenhar fora da EDT/segurar `Graphics`. Fontes: "Performing Custom Painting"; Javadoc `JComponent#paintComponent`.
- **11 — Action API, key bindings e performance.** `Action`/`AbstractAction` (estado compartilhado entre botão/menu/toolbar), `InputMap`/`ActionMap` (por que vence `KeyListener`), responsividade (EDT livre, models grandes lazy/virtuais, `repaint` de região). Liga 05/06. Armadilhas: duplicar lógica em listener de botão e de menu (use `Action`); `KeyListener` pra atalho (perde com foco) → `InputMap`/`ActionMap`; carregar 1M linhas num `DefaultTableModel` eager. Fontes: "How to Use Actions", "How to Use Key Bindings".
- **12 — Swing hoje — estado atual (capstone, opus).** Status oficial (core Java SE, suporte enquanto o JDK for — Oracle roadmap 2018/2020, com data) vs consenso de-facto (poucas features novas, nicho); onde ainda faz sentido (ferramentas internas, IDEs Swing — IntelliJ/NetBeans/Eclipse, apps offline/legados) vs onde não (moderno rico/web/mobile); **Swing × virtual threads** (EDT segue single-thread; VTs ajudam background, não a EDT — verificar); ecossistema vivo (FlatLaf); gancho pro Galho 6 (JavaFX, planejado); enquadramento de entrevista. Cheatsheet de fechamento (qual nota pra qual problema). **WebFetch obrigatório.** Armadilhas (de raciocínio): tratar Swing como "morto" (é suportado); escolher Swing por inércia pra app moderno; assumir que virtual threads "consertam" a EDT. Fontes: Oracle Java Client Roadmap (2018, 2020); dev.java; Javadoc/JEPs de virtual threads (cross-check com Galho 4 nota 12).

## 6. Pré-flight (substitui a poda): verificação de estado

Como não há tronco, o pré-flight do galho é **confirmar fatos via fonte oficial antes de escrever**, especialmente para a capstone (12). Executado nesta fase de brainstorming e a ser re-confirmado na execução da nota 12:

1. **Status de suporte do Swing/AWT** — confirmado: "core Java SE technologies", suportadas enquanto o JDK for ([Oracle Java Client Roadmap 2018](https://www.oracle.com/docs/tech/java/javaclientroadmapupdate2018mar.pdf); [blogs.oracle.com](https://blogs.oracle.com/java/post/java-client-roadmap-updates)). "Modo de manutenção" é jargão da comunidade, não termo oficial — a capstone separa os dois.
2. **JavaFX desacoplado do JDK no Java 11** (OpenJFX standalone) — confirmado na mesma fonte; relevante pro gancho do Galho 6.
3. **Versão do The Java Tutorials** — o trail oficial *Creating a GUI with Swing* tem banner "written for JDK 8"; a API Swing é estável desde então, mas as notas devem **conferir cada API no Javadoc atual (Java 21/25)** e em `dev.java` quando houver versão mais nova, não assumir que tudo do tutorial JDK 8 é o estado da arte.
4. **Swing × virtual threads** — re-confirmar na nota 12 (cross-check com Galho 4 nota 12) que a EDT permanece single-thread e que virtual threads não alteram o modelo da EDT.

Nenhum número de adoção é inventado. Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 12 notas em `03-Dominios/Tecnologia/Java/Swing/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 4/5/3.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~20-24 verbetes de Swing em ordem alfabética; verbetes dos Galhos 1 e 4 intactos; `updated` atualizado; headings dos verbetes conferidos 1:1 com as âncoras usadas nas notas.
4. MOC central `Java/index.md` com Galho 5 ativado (linha 32 vira wikilink); resto intacto.
5. **Sem poda** (galho novo) — nenhum tronco modificado.
6. Cada nota: TL;DR; 3-5 code samples (notas conceituais); "Em entrevista" com frase 3+ sentenças EN + 6+ termos PT→EN; "Armadilhas" com exemplo+fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + Galhos 1/4 quando conectar + Dicionário); "Referências" com docs oficiais verificadas.
7. Zero fabricação de experiência pessoal; **zero estatística inventada na capstone**; status do Swing hedged, datado e com fonte.
8. APIs e comportamentos fundados em doc oficial (WebFetch no Step 1 de cada nota); nenhuma API "de memória".
9. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal.
10. `verificar-wikilinks` roda limpo na pasta do galho (cuidado: falso-positivo em self-anchors `[[#Heading]]` — preferir não usar âncoras same-file); Quartz publica sem erros.

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Galho de pesquisa: inventar API/comportamento "de memória" | WebFetch obrigatório no Step 1 de cada nota; toda nota tem "Referências" com fonte oficial; nada afirmado sem conferir no Javadoc/Tutorial. |
| Capstone (12) virar obituário ou panfleto, ou inventar estatística | Frase honesta separa declaração oficial Oracle (com data/fonte) de consenso de-facto; nenhum número de adoção; trade-off "quando sim / quando não" obrigatório; WebFetch. |
| Sobreposição de threading com Galho 4 (EDT/SwingWorker re-explicarem concorrência) | Notas 05/06 são donas só do *threading do Swing*; linkam Galho 4 (02 Threads, 08 Executors) pros primitivos; não re-explicam threads/pools. |
| Comparar Swing vs JavaFX a fundo (que é do Galho 6) | Só gancho na capstone; Galho 6 é dono; texto "planejado" no MOC, sem wikilink quebrado. |
| Tutorial oficial é "written for JDK 8" e pode estar desatualizado | Conferir cada API no Javadoc atual (21/25) e dev.java; declarar version-specificity quando houver; não assumir que o tutorial JDK 8 é o estado da arte. |
| `JTable` (tópico pesado) inflar uma nota | Distribuído: catálogo (02), model (07), renderers/editors (08), performance (11); nenhuma nota sozinha o cobre. |
| Endossar dependência third-party (FlatLaf) como se fosse oficial | FlatLaf rotulado explicitamente como community/open-source/não-Oracle, com ressalva; L&F bundled (Metal/Nimbus/system) é o baseline. |
| Code samples de Swing não-determinísticos (threading) | Declarar que sintomas de violação da EDT são intermitentes; exemplos *demonstram* o bug sem prometer reprodução garantida. |
| Magus crescer demais | Distribuição 4/5/3 fixada (Magus leve por design — 1 nota avançada dividida + capstone); se inflar, dividir nota, não galho. |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-03-java-galho-05-swing-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` em branch dedicada `java-galho-05-swing` (1 subagente por nota; sonnet, opus pras notas 05/06/07 e 12; review **por fase** + fix loop)
4. **Verificação** de wikilinks + build Quartz
5. **Revisão do roadmap** com aprendizados antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- `2026-06-02-java-galho-01-linguagem-design.md` / `...-execution.md` — Galho 1 (template de qualidade/plano)
- `2026-06-03-java-galho-04-concorrencia-design.md` / `...-execution.md` — Galho 4 (template mais recente; donos de threading que o Galho 5 linka)
- Artefatos a atualizar: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`, `03-Dominios/Tecnologia/Java/index.md`
- Fontes-base do galho: The Java Tutorials — *Creating a GUI with Swing* (`docs.oracle.com/javase/tutorial/uiswing/`), `dev.java`, Javadoc `javax.swing`, Oracle Java Client Roadmap (2018/2020)
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]]
