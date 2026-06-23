# Galho 5 — Swing (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 5 da trilha Java Senior — 12 notas atômicas de Swing (GUI desktop) em 3 fases + MOC do galho + expansão do Dicionário de Java + ativação do MOC central. **Galho novo, construído por pesquisa: sem tronco a podar.**

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Tecnologia/Java/Swing/`, notas atômicas `publish: true` em PT-BR, numeração global 01-12 (4 Iniciado / 5 Adepto / 3 Magus). Diferença-chave dos Galhos 1/4: **não há monolito de origem**. Cada nota **nasce de doc oficial verificada via WebFetch** (The Java Tutorials — *Creating a GUI with Swing*, `dev.java`, Javadoc `javax.swing`). O galho é dono do "como o Swing usa threads" (EDT/SwingWorker) e **linka** pro Galho 4 (Concorrência) pros primitivos, sem re-explicar. JavaFX (Galho 6) é só gancho na capstone. Branch dedicada `java-galho-05-swing` (NÃO em `main`) — **já criada e com o spec commitado**.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4 (publicação). Verificação de fonte via WebFetch (docs.oracle.com/javase/tutorial/uiswing, dev.java, Javadoc Java 21/25).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-03`):

```yaml
---
title: "<título sem prefixo numérico>"
created: 2026-06-03
updated: 2026-06-03
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - swing
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
5. `## Na prática` — exemplos compiláveis, framing neutro ("padrão observado no JDK / em IDEs Swing", "caso típico em ferramenta interna", hipotético explícito `// hipotético:`). NUNCA "no meu projeto". Ao demonstrar violação da EDT (tocar componente fora da EDT), declarar que o sintoma é **não-determinístico/intermitente**.
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada armadilha: `### (N) Título` + descrição + exemplo curto de código demonstrando o problema + fix em 1 linha.
7. `## Em entrevista` — frase pronta em inglês com **3+ sentenças** (trade-off + decisão + caveat) + sub-bloco "Vocabulário" com **6+ termos PT→EN** traduzidos.
8. `## Veja também` — wikilinks SEM backticks. Sempre inclui: notas relacionadas do galho + `[[03-Dominios/Tecnologia/Java/Swing/index|MOC do galho]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando o conceito conectar) `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência]]` / `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem]]` + verbetes do Dicionário relevantes.
9. `## Referências` — docs oficiais (The Java Tutorials, dev.java, Javadoc) + (quando pertinente) JEPs e projetos open-source identificados (FlatLaf, OpenJDK).

**Tamanho:** 200-500 linhas (notas Magus densas até 700).

**Restrições absolutas** (qualquer violação reprova a nota):
- **Galho de pesquisa: WebFetch obrigatório no Step 1 de cada nota.** Nada de API "de memória" — toda afirmação fundada em doc oficial conferida no Javadoc/Tutorial. Toda nota tem "Referências".
- Sem fabricação de experiência pessoal. Exemplos: `Order`, `Customer`, `OrderTableModel`, ou `// hipotético: ...`. NUNCA `josenaldo`/caminhos pessoais/casos vividos.
- **Sem estatística inventada** (especialmente na capstone 12): nenhum "X% das empresas usam Swing". Status só com fonte oficial + data.
- Comparações justas ("quando X vence" E "quando Y vence") — lightweight vs heavyweight, `invokeLater` vs `SwingWorker`, `KeyListener` vs `InputMap`, Swing vs JavaFX/web.
- Status do Swing hedged e datado: "Swing/AWT são tecnologias core do Java SE, suportadas enquanto o JDK for (Oracle Java Client Roadmap, 2018/2020); na prática recebem poucas features novas — verifique a release atual" em vez de "Swing está morto".
- **Não linkar notas do Galho 6 (JavaFX, inexistente).** Quando citar JavaFX, usar texto "(planejado)" sem wikilink. Linkar Galhos 1/4 (existentes) quando o conceito conectar.
- Code fences: ` ```java ` pra código, ` ```text ` pra output/stack trace. Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (nunca `git add -A`); 1 commit por nota.

**Material de origem:** NÃO há tronco. Fontes-base (conferir o trail específico por nota): The Java Tutorials — *Creating a GUI with Swing* (`https://docs.oracle.com/javase/tutorial/uiswing/`), `dev.java`, Javadoc `javax.swing` (Java 21). Spec de referência: `docs/superpowers/specs/2026-06-03-java-galho-05-swing-design.md` §5. Template de qualidade: notas dos Galhos 1 e 4 em `03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/` e `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/`.

**Modelo por nota:** sonnet por padrão; **opus** nas notas 05 (EDT), 06 (SwingWorker), 07 (MVC/models) e 12 (capstone estado atual) — as mais densas/sensíveis.

**Cuidado com o tutorial JDK 8:** o trail oficial tem banner "written for JDK 8". A API Swing é estável, mas **conferir cada API no Javadoc atual (Java 21/25)** e em `dev.java` quando houver versão mais nova; não assumir que tudo do tutorial JDK 8 é o estado da arte.

---

## Task 0: Pré-flight — branch, pasta e verificação de status (substitui leitura de tronco)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/` (pasta)

- [ ] **Step 1: Confirmar a branch dedicada**

```bash
git branch --show-current
```
Expected: `java-galho-05-swing` (já criada na fase de brainstorming, com o spec commitado). Se por algum motivo estiver em `main`, rodar `git checkout java-galho-05-swing`.

- [ ] **Step 2: Criar a pasta do galho**

```bash
mkdir -p "03-Dominios/Tecnologia/Java/Swing"
```

- [ ] **Step 3: Verificar status de manutenção/adoção do Swing (pré-flight, no lugar da leitura de tronco)**

WebFetch `https://blogs.oracle.com/java/post/java-client-roadmap-updates` (e, se acessível, o PDF `https://www.oracle.com/docs/tech/java/javaclientroadmapupdate2018mar.pdf`). Confirmar e anotar para a nota 12:
- Swing e AWT = "core Java SE technologies", suportadas enquanto o JDK for suportado (NÃO deprecadas/removidas).
- "Modo de manutenção" é jargão da comunidade, não termo oficial da Oracle — a capstone separa os dois.
- JavaFX desacoplado do JDK no Java 11 (OpenJFX standalone).

> Já confirmado na fase de brainstorming (registrado no §1/§6 do spec). Re-confirmar aqui para a execução da nota 12; nenhum número de adoção é inventado.

- [ ] **Step 4: Fixar versões assumidas do galho**

Baseline: **Java 21 LTS** / **Java 25 LTS**. A API Swing é estável desde o JDK 8; o que muda é a versão do JDK e o ecossistema (Nimbus bundled, FlatLaf third-party). Registrar que exemplos assumem Java 21+ e que `SwingWorker`/`javax.swing.Timer` existem desde Java 6/SE 6.

- [ ] **Step 5: Sem commit** (task de preparação; nada a versionar ainda).

---

## Fase INICIADO (notas 01-04)

### Task 1: Nota 01 — O modelo do Swing

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/01 - O modelo do Swing.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/uiswing/start/about.html` (About the JFC and Swing) e `https://docs.oracle.com/javase/tutorial/uiswing/components/toplevel.html` (Using Top-Level Containers). Confirmar a relação Swing/AWT (lightweight vs heavyweight), a hierarquia de componentes e o content pane.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, swing, iniciado, componentes, fundamentos]`, aliases `["Swing", "Modelo do Swing"]`.

Conteúdo:
- TL;DR: Swing = toolkit de GUI desktop em Java, desenhado sobre o AWT; componentes lightweight (pintados em Java) + arquitetura pluggable look-and-feel.
- `## O que é` — o que é Swing (parte do JFC); lightweight (Swing, `J*`) vs heavyweight (AWT, peers do SO); por que Swing nasceu.
- `## Por que importa` — pra senior: base de IDEs e ferramentas internas; entrevista cobra o modelo (por que single-thread, por que `J`-prefix).
- `## Como funciona` — H3s: "Hierarquia `Component`→`Container`→`JComponent`", "Top-level containers (`JFrame`/`JDialog`/`JWindow`) e o content pane", "Ciclo de uma janela (`pack`/`setVisible`/`setDefaultCloseOperation`)", "Pluggable look-and-feel (intro; deep na 09)".
- `## Na prática` — "Hello World" Swing mínimo construído na EDT (`SwingUtilities.invokeLater`), com `JFrame`+`JPanel`+`JLabel`.
- `## Armadilhas` — ≥2: (1) misturar componentes AWT e Swing (problemas de z-order/repaint) → preferir Swing puro; (2) construir/mostrar a UI fora da EDT (teaser da 05) → `invokeLater`. Exemplo + fix.
- `## Em entrevista` — frase 3+ sentenças sobre lightweight vs heavyweight e pluggable L&F; vocabulário 6+ termos.
- `## Veja também` — 02, 03, 04, 05, 12, MOC galho, MOC central, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem]]` (OOP), verbetes `AWT (Abstract Window Toolkit)`/`componente lightweight / heavyweight`/`content pane`/`JComponent`.
- `## Referências` — The Java Tutorials (About the JFC and Swing), dev.java, Javadoc `javax.swing`.

Tamanho: 220-340 linhas (abertura, conceitual).

- [ ] **Step 3: Verificar**

```bash
head -20 "03-Dominios/Tecnologia/Java/Swing/01 - O modelo do Swing.md"
grep -cE "^## (O que é|Como funciona|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Tecnologia/Java/Swing/01 - O modelo do Swing.md"
```
Expected: frontmatter com `fase: iniciado`; grep ≥6.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/01 - O modelo do Swing.md"
git commit -m "feat(java): galho 5 nota 01 — o modelo do Swing"
```

---

### Task 2: Nota 02 — Componentes e containers

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/02 - Componentes e containers.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/uiswing/components/componentlist.html` (A Visual Guide to Swing Components) e `https://docs.oracle.com/javase/tutorial/uiswing/components/index.html` (Using Swing Components). Confirmar a lista de componentes e containers e seus papéis.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, swing, iniciado, componentes]`, aliases `["Componentes Swing", "JButton", "JTable"]`.

Conteúdo:
- `## O que é` — o catálogo de widgets do Swing; componentes (controles) vs containers (agrupam).
- `## Como funciona` — H3s: "Controles básicos (`JButton`, `JLabel`, `JTextField`, `JTextArea`, `JPasswordField`)", "Seleção (`JCheckBox`/`JRadioButton`+`ButtonGroup`, `JComboBox`, `JList`)", "Componentes orientados a dados (`JTable`/`JTree` — intro; models vêm na 07)", "Containers intermediários (`JPanel`, `JScrollPane`, `JTabbedPane`, `JSplitPane`)", "Menus, toolbars e diálogos (`JMenuBar`/`JMenu`/`JMenuItem`, `JToolBar`, `JDialog`/`JOptionPane`)".
- `## Na prática` — montar um formulário simples (labels + campos + botão) num `JPanel`; um `JOptionPane.showMessageDialog`.
- `## Armadilhas` — ≥2: (1) `JList`/`JTextArea` sem `JScrollPane` (conteúdo cortado, sem scroll) → embrulhar em `JScrollPane`; (2) `JList`/`JTable` populados com dados crus em vez de model adequado (aponta pra 07); (3) `JOptionPane`/diálogo chamado fora da EDT (aponta pra 05). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 03, 07, MOC, central, verbetes `JComponent`) + `## Referências`.

Tamanho: 260-400 linhas (panorâmica de vocabulário).

- [ ] **Step 3: Verificar**

```bash
grep -E "JButton|JLabel|JTable|JScrollPane|JOptionPane|JPanel" "03-Dominios/Tecnologia/Java/Swing/02 - Componentes e containers.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/02 - Componentes e containers.md"
git commit -m "feat(java): galho 5 nota 02 — componentes e containers"
```

---

### Task 3: Nota 03 — Layout managers

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/03 - Layout managers.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/uiswing/layout/visual.html` (A Visual Guide to Layout Managers) e `https://docs.oracle.com/javase/tutorial/uiswing/layout/using.html` (Laying Out Components Within a Container). Confirmar o comportamento de cada layout e o uso de `GridBagConstraints`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, swing, iniciado, layout]`, aliases `["Layout managers", "BorderLayout", "GridBagLayout"]`.

Conteúdo:
- `## O que é` — layout manager = objeto que posiciona/dimensiona componentes de um container automaticamente (responsivo a resize/L&F/DPI).
- `## Como funciona` — H3s: "`BorderLayout` / `FlowLayout` / `GridLayout` (os básicos)", "`BoxLayout` e `CardLayout`", "`GridBagLayout` (o power tool, com `GridBagConstraints`)", "`GroupLayout` (gerado por GUI builders)", "Aninhar painéis para layouts complexos", "Sizing (`preferred`/`minimum`/`maximum`)".
- `## Na prática` — tela mestre-detalhe combinando `BorderLayout` + `JPanel` aninhado; um `GridBagLayout` com 2-3 constraints comentadas.
- `## Armadilhas` — ≥2: (1) **null layout / posicionamento absoluto** (`setBounds`) → quebra em resize/DPI/L&F diferente; usar layout manager; (2) `GridBagLayout` onde `BoxLayout`/`BorderLayout` resolveriam (complexidade desnecessária); (3) ignorar `getPreferredSize` em componente customizado (vira 0×0). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 02, 10, MOC, central, verbetes `layout manager`/`GridBagLayout`) + `## Referências`.

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "BorderLayout|FlowLayout|GridBagLayout|BoxLayout|preferredSize|null layout" "03-Dominios/Tecnologia/Java/Swing/03 - Layout managers.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/03 - Layout managers.md"
git commit -m "feat(java): galho 5 nota 03 — layout managers"
```

---

### Task 4: Nota 04 — O modelo de eventos

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/04 - O modelo de eventos.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/uiswing/events/index.html` (Writing Event Listeners) e `https://docs.oracle.com/javase/tutorial/uiswing/events/intro.html` (Introduction to Event Listeners). Confirmar o delegation event model e os tipos de listener/adapter.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: iniciado`, tags `[java, swing, iniciado, eventos, listeners]`, aliases `["Modelo de eventos", "ActionListener", "Listener"]`.

Conteúdo:
- `## O que é` — modelo event-driven (delegation event model): a fonte (componente) notifica listeners registrados quando algo acontece.
- `## Como funciona` — H3s: "Source, event e listener (o triângulo)", "Listeners comuns (`ActionListener`, `MouseListener`, `KeyListener`, `FocusListener`, `WindowListener`)", "Event objects (`ActionEvent`, `MouseEvent`)", "Lambda vs classe anônima vs adapter (`MouseAdapter`)", "Registrar/remover listeners". **Linka pro Galho 1** (interfaces funcionais / lambdas) onde o conceito conecta.
- `## Na prática` — botão com `ActionListener` via lambda; `MouseAdapter` só pra `mouseClicked`.
- `## Armadilhas` — ≥2: (1) trabalho pesado/IO dentro do listener (roda na EDT → congela a UI; aponta pra 05/06) → `SwingWorker`; (2) implementar a interface `MouseListener` inteira só pra um método (5 métodos vazios) → usar `MouseAdapter`; (3) `KeyListener` para atalho de teclado (depende de foco — aponta pra 11) → `InputMap`/`ActionMap`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 05, 11, MOC, central, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem]]`, verbetes `delegation event model`/`listener (event listener)`/`adapter (event adapter)`) + `## Referências`.

Tamanho: 260-400 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "ActionListener|MouseAdapter|delegation|KeyListener|ActionEvent" "03-Dominios/Tecnologia/Java/Swing/04 - O modelo de eventos.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/04 - O modelo de eventos.md"
git commit -m "feat(java): galho 5 nota 04 — o modelo de eventos"
```

---

## Fase ADEPTO (notas 05-09)

### Task 5: Nota 05 — A Event Dispatch Thread (EDT)  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/05 - A Event Dispatch Thread.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch `https://docs.oracle.com/javase/tutorial/uiswing/concurrency/index.html` (Concurrency in Swing), `https://docs.oracle.com/javase/tutorial/uiswing/concurrency/dispatch.html` (The Event Dispatch Thread) e Javadoc de `SwingUtilities` (`invokeLater`/`invokeAndWait`). Confirmar a single-thread rule e a diferença `invokeLater` vs `invokeAndWait`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, swing, adepto, edt, threading]`, aliases `["EDT", "Event Dispatch Thread", "invokeLater"]`.

Conteúdo (DONO do "como o Swing usa threads"):
- `## O que é` — a EDT: única thread onde event handling e painting acontecem; a single-thread rule do Swing.
- `## Por que importa` — quase todo bug de UI "congelada" ou intermitente vem de violar a EDT; entrevista cobra isso.
- `## Como funciona` — H3s: "A single-thread rule (por que a GUI é single-threaded)", "O que roda na EDT (dispatch de eventos + painting)", "A regra de ouro (não bloquear a EDT; não tocar componentes fora da EDT)", "`SwingUtilities.invokeLater` vs `invokeAndWait`", "`isEventDispatchThread`". **Linka Galho 4 (02 Threads)** pros primitivos de thread, sem re-explicar concorrência.
- `## Na prática` — atualizar um `JLabel` a partir de uma thread de background corretamente via `invokeLater`; iniciar a UI na EDT.
- `## Armadilhas` — ≥3: (1) atualizar componente de uma thread de background (corrupção/erro intermitente — **declarar não-determinístico**) → `invokeLater`; (2) `invokeAndWait` chamado a partir da própria EDT (lança exceção/deadlock) → checar `isEventDispatchThread`; (3) operação longa/IO direto num listener (congela a UI) → mover pra background (aponta pra 06). Exemplo + fix.
- `## Em entrevista` — frase 3+ sentenças sobre a single-thread rule e o trade-off (simplicidade vs responsabilidade do dev); vocabulário 6+ termos.
- `## Veja também` (04, 06, 11, MOC, central, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência]]` + `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/02 - Threads e seu ciclo de vida|Threads]]`, verbetes `EDT (Event Dispatch Thread)`/`invokeLater / invokeAndWait`) + `## Referências`.

Tamanho: 320-480 linhas (densa; usar opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "EDT|invokeLater|invokeAndWait|isEventDispatchThread|single-thread" "03-Dominios/Tecnologia/Java/Swing/05 - A Event Dispatch Thread.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/05 - A Event Dispatch Thread.md"
git commit -m "feat(java): galho 5 nota 05 — a Event Dispatch Thread (EDT)"
```

---

### Task 6: Nota 06 — SwingWorker e tarefas em background  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/06 - SwingWorker e tarefas em background.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch `https://docs.oracle.com/javase/tutorial/uiswing/concurrency/worker.html` (Worker Threads and SwingWorker), `https://docs.oracle.com/javase/tutorial/uiswing/concurrency/interim.html` (Tasks that Have Interim Results) e Javadoc `javax.swing.SwingWorker` (Java 21). Confirmar `doInBackground`/`publish`/`process`/`done` e qual roda na EDT vs no worker.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, swing, adepto, swingworker, threading]`, aliases `["SwingWorker", "Tarefas em background"]`.

Conteúdo:
- `## O que é` — `SwingWorker<T,V>`: ponte entre uma thread de background e a EDT, pra não congelar a UI.
- `## Como funciona` — H3s: "O ciclo (`doInBackground` no worker; `done`/`process` na EDT)", "Resultados intermediários (`publish`/`process`) e progresso (`setProgress`/`PropertyChangeListener`)", "Cancelamento (`cancel`/`isCancelled`)", "Obter o resultado (`get`)", "`javax.swing.Timer` (callbacks periódicos na EDT) vs `java.util.Timer`". **Linka Galho 4 (08 Executors)** sem re-explicar pools.
- `## Na prática` — carregar dados de uma fonte lenta (hipotética) com `SwingWorker`, publicando progresso numa `JProgressBar`.
- `## Armadilhas` — ≥3: (1) chamar `get()` na EDT antes de `done` (bloqueia a EDT — congela) → ler em `done()`; (2) tocar componentes dentro de `doInBackground` (fora da EDT) → usar `publish`/`process`; (3) exceção engolida silenciosamente (só aparece ao chamar `get` em `done`) → sempre tratar em `done`. Exemplo + fix.
- `## Em entrevista` — frase 3+ sentenças sobre o handoff worker→EDT; vocabulário 6+ termos.
- `## Veja também` (05, 11, MOC, central, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência]]` + `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/08 - Executors e thread pools|Executors]]`, verbete `SwingWorker`) + `## Referências`.

Tamanho: 300-460 linhas (densa; usar opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "SwingWorker|doInBackground|publish|process|done|javax.swing.Timer" "03-Dominios/Tecnologia/Java/Swing/06 - SwingWorker e tarefas em background.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/06 - SwingWorker e tarefas em background.md"
git commit -m "feat(java): galho 5 nota 06 — SwingWorker e tarefas em background"
```

---

### Task 7: Nota 07 — MVC em Swing e os models  ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/07 - MVC em Swing e os models.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus)**

WebFetch `https://docs.oracle.com/javase/tutorial/uiswing/components/table.html` (How to Use Tables), `https://docs.oracle.com/javase/tutorial/uiswing/components/list.html` (How to Use Lists) e Javadoc `TableModel`/`AbstractTableModel`. Confirmar o padrão separable model e como a view reage a eventos do model.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, swing, adepto, mvc, model]`, aliases `["MVC em Swing", "TableModel", "Separable model"]`.

Conteúdo:
- `## O que é` — o "MVC" pragmático do Swing: a **separable model architecture** (model separado da view/controller, que o L&F fornece).
- `## Como funciona` — H3s: "Separable model (por que separar dados de apresentação)", "`TableModel`/`AbstractTableModel`/`DefaultTableModel`", "`ListModel`/`AbstractListModel`/`DefaultListModel` e `ComboBoxModel`", "`Document` (modelo de texto) e `TreeModel`", "Model listeners (`TableModelListener`) e como a view atualiza", "Selection models".
- `## Na prática` — um `AbstractTableModel` tipado (`OrderTableModel`) que expõe uma `List<Order>`; disparar `fireTableRowsInserted` ao adicionar.
- `## Armadilhas` — ≥3: (1) mutar os dados do model sem disparar o evento (`fireTable...`) → view dessincroniza; (2) `DefaultTableModel` com `Vector`/`Object[][]` cru onde um `AbstractTableModel` tipado é mais seguro; (3) lógica de negócio/formatação no model em vez de no renderer (aponta pra 08). Exemplo + fix.
- `## Em entrevista` — frase 3+ sentenças sobre separable model vs MVC clássico; vocabulário 6+ termos.
- `## Veja também` (02, 08, MOC, central, verbetes `separable model (MVC do Swing)`/`TableModel / ListModel`/`Document (modelo de texto)`) + `## Referências`.

Tamanho: 320-480 linhas (densa; usar opus).

- [ ] **Step 3: Verificar**

```bash
grep -E "TableModel|AbstractTableModel|ListModel|separable|fireTable" "03-Dominios/Tecnologia/Java/Swing/07 - MVC em Swing e os models.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/07 - MVC em Swing e os models.md"
git commit -m "feat(java): galho 5 nota 07 — MVC em Swing e os models"
```

---

### Task 8: Nota 08 — Renderers e editors

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/08 - Renderers e editors.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/uiswing/components/table.html` (seções "Using Custom Renderers" e "Using Other Editors") e Javadoc `TableCellRenderer`/`ListCellRenderer`/`TableCellEditor`. Confirmar o rubber-stamp pattern (o renderer é reusado pra pintar cada célula).

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, swing, adepto, renderer, table]`, aliases `["Cell renderer", "TableCellRenderer", "Cell editor"]`.

Conteúdo:
- `## O que é` — renderer = como uma célula/item é desenhado; editor = como é editado. Pareiam com os models da 07.
- `## Como funciona` — H3s: "`TableCellRenderer`/`ListCellRenderer` e o **rubber-stamp pattern**", "`DefaultTableCellRenderer` (estender vs implementar)", "Cell editors (`TableCellEditor`, `DefaultCellEditor`)", "Renderer vs editor (display vs edição)".
- `## Na prática` — renderer que colore uma célula de status (`Order.status`) conforme o valor; editor com `JComboBox` numa coluna.
- `## Armadilhas` — ≥3: (1) criar `new JLabel()` por célula dentro do renderer (mata performance com muitas linhas) → reusar o componente (rubber-stamp); (2) estado mutável/listener acumulado no renderer (é chamado milhares de vezes); (3) editor que não chama `stopCellEditing` (valor perdido). Exemplo + fix.
- `## Em entrevista` + `## Veja também` (02, 07, MOC, central, verbetes `cell renderer`/`cell editor`) + `## Referências`.

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "TableCellRenderer|ListCellRenderer|rubber-stamp|DefaultTableCellRenderer|stopCellEditing" "03-Dominios/Tecnologia/Java/Swing/08 - Renderers e editors.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/08 - Renderers e editors.md"
git commit -m "feat(java): galho 5 nota 08 — renderers e editors"
```

---

### Task 9: Nota 09 — Look & Feel e temas

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/09 - Look and Feel e temas.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/uiswing/lookandfeel/index.html` (Modifying the Look and Feel) + `https://docs.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html`, Javadoc `UIManager`, e `https://www.formdev.com/flatlaf/` (FlatLaf — **identificar explicitamente como third-party, open-source, não-Oracle**). Confirmar os L&F bundled (Metal/Nimbus/system/Motif) e como trocar L&F.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: adepto`, tags `[java, swing, adepto, look-and-feel, ui]`, aliases `["Look and Feel", "Nimbus", "FlatLaf"]`.

Conteúdo:
- `## O que é` — pluggable look-and-feel: a aparência é desacoplada do componente; um L&F define como tudo é pintado.
- `## Como funciona` — H3s: "L&F bundled no JDK (Metal, **Nimbus**, system, Motif)", "`UIManager` (defaults, `setLookAndFeel`, `getSystemLookAndFeelClassName`)", "Trocar L&F em runtime (`SwingUtilities.updateComponentTreeUI`)", "Ecossistema moderno: **FlatLaf** (third-party, open-source — flat/dark, de-facto na comunidade; 1 snippet de setup + ressalva de dependência externa)", "Borders (`BorderFactory`) e fontes".
- `## Na prática` — setar o system L&F no boot (com try/catch); 1 exemplo de FlatLaf (`FlatLightLaf.setup()`) **rotulado como dependência third-party** (Maven coordinate citada como exemplo, não endosso).
- `## Armadilhas` — ≥3: (1) setar L&F **depois** de criar componentes sem `updateComponentTreeUI` (UI mista); (2) assumir que o system L&F é o mesmo em todo SO (cores/tamanhos mudam) → testar; (3) cores hard-coded quebrando no dark mode → usar chaves do `UIManager`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (01, 10, MOC, central, verbetes `look and feel (L&F)`/`pluggable look-and-feel`/`UIManager`/`Nimbus`/`FlatLaf`) + `## Referências`.

Tamanho: 280-420 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "UIManager|Nimbus|FlatLaf|setLookAndFeel|updateComponentTreeUI" "03-Dominios/Tecnologia/Java/Swing/09 - Look and Feel e temas.md" | head
grep -iE "third-party|não-Oracle|dependência" "03-Dominios/Tecnologia/Java/Swing/09 - Look and Feel e temas.md" | head
```
Expected: cobre L&F bundled + UIManager; FlatLaf rotulado como third-party.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/09 - Look and Feel e temas.md"
git commit -m "feat(java): galho 5 nota 09 — Look and Feel e temas"
```

---

## Fase MAGUS (notas 10-12)

### Task 10: Nota 10 — Custom painting e componentes customizados

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/10 - Custom painting e componentes customizados.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/uiswing/painting/index.html` (Performing Custom Painting), `https://docs.oracle.com/javase/tutorial/uiswing/painting/closer.html` (A Closer Look at the Paint Mechanism) e Javadoc `JComponent#paintComponent`. Confirmar a paint chain e o double buffering default.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, swing, magus, painting, custom-component]`, aliases `["Custom painting", "paintComponent", "Componente customizado"]`.

Conteúdo:
- `## O que é` — quando os componentes prontos não bastam: desenhar e compor componentes próprios.
- `## Como funciona` — H3s: "A paint chain (`paint`→`paintComponent`/`paintBorder`/`paintChildren`)", "`paintComponent(Graphics)` e `Graphics2D` (shapes, `RenderingHints` p/ antialiasing)", "Double buffering (default no Swing)", "`repaint(Rectangle)` vs `revalidate` (repintar vs relayout)", "Criar componente reutilizável (estender `JComponent`/`JPanel`, `getPreferredSize`)".
- `## Na prática` — um `JComponent` que desenha um gráfico/badge simples, sobrescrevendo `paintComponent` e `getPreferredSize`.
- `## Armadilhas` — ≥3: (1) sobrescrever `paint` em vez de `paintComponent` (quebra borders/children/double buffering) → `paintComponent`; (2) não chamar `super.paintComponent(g)` (artefatos de pintura) → chamar primeiro; (3) desenhar fora da EDT ou guardar o `Graphics` para usar depois (inválido) → pintar só dentro de `paintComponent`. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (03, 08, 09, 11, MOC, central, verbetes `paintComponent / custom painting`/`double buffering`) + `## Referências`.

Tamanho: 300-460 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "paintComponent|Graphics2D|double buffering|repaint|revalidate|super.paintComponent" "03-Dominios/Tecnologia/Java/Swing/10 - Custom painting e componentes customizados.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/10 - Custom painting e componentes customizados.md"
git commit -m "feat(java): galho 5 nota 10 — custom painting e componentes customizados"
```

---

### Task 11: Nota 11 — Action API, key bindings e performance

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/11 - Action API, key bindings e performance.md`

- [ ] **Step 1: Pesquisar fonte**

WebFetch `https://docs.oracle.com/javase/tutorial/uiswing/misc/action.html` (How to Use Actions) e `https://docs.oracle.com/javase/tutorial/uiswing/misc/keybinding.html` (How to Use Key Bindings). Confirmar como `Action` compartilha estado entre botão/menu/toolbar e por que `InputMap`/`ActionMap` vence `KeyListener`.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, swing, magus, action, key-bindings, performance]`, aliases `["Action API", "Key bindings", "InputMap"]`.

Conteúdo:
- `## O que é` — técnicas de senior: centralizar comportamento (Action API), atalhos robustos (key bindings) e manter a UI responsiva.
- `## Como funciona` — H3s: "Action API (`Action`/`AbstractAction` — encapsula comportamento + `enabled` + texto/ícone; compartilhado entre botão, item de menu e toolbar)", "Key bindings (`InputMap`/`ActionMap`) e por que vencem `KeyListener` (independente de foco/registro)", "Performance e responsividade (manter a EDT livre; models grandes lazy/virtuais; `repaint` de região)". Liga de volta à EDT (05) e ao SwingWorker (06).
- `## Na prática` — um `AbstractAction` "Salvar" reusado num botão e num item de menu (um só `setEnabled` desabilita ambos); bind de `Ctrl+S` via `InputMap`/`ActionMap`.
- `## Armadilhas` — ≥3: (1) duplicar a lógica do botão e do item de menu (drift) → uma `Action` compartilhada; (2) `KeyListener` para atalho de aplicação (só funciona com foco no componente) → `InputMap`/`ActionMap` no `WHEN_IN_FOCUSED_WINDOW`; (3) carregar 1M de linhas eager num `DefaultTableModel` (UI trava) → model lazy/virtual + paginação. Exemplo + fix.
- `## Em entrevista` + `## Veja também` (04, 05, 06, 07, 10, MOC, central, verbetes `Action API`/`InputMap / ActionMap (key bindings)`) + `## Referências`.

Tamanho: 300-440 linhas.

- [ ] **Step 3: Verificar**

```bash
grep -E "AbstractAction|InputMap|ActionMap|KeyListener|WHEN_IN_FOCUSED_WINDOW|setEnabled" "03-Dominios/Tecnologia/Java/Swing/11 - Action API, key bindings e performance.md" | head
```

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/11 - Action API, key bindings e performance.md"
git commit -m "feat(java): galho 5 nota 11 — Action API, key bindings e performance"
```

---

### Task 12: Nota 12 — Swing hoje: estado atual  ⟦opus⟧ (capstone)

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/12 - Swing hoje - estado atual.md`

- [ ] **Step 1: Pesquisar fonte (usar modelo opus) — VERIFICAÇÃO OBRIGATÓRIA**

WebFetch `https://blogs.oracle.com/java/post/java-client-roadmap-updates` (e o PDF `https://www.oracle.com/docs/tech/java/javaclientroadmapupdate2018mar.pdf` se acessível; senão usar a versão 2020 `https://www.oracle.com/technetwork/java/javase/javaclientroadmapupdatev2020may-6548840.pdf`). Confirmar a frase exata sobre Swing/AWT serem core Java SE e o suporte enquanto o JDK for. WebFetch `https://dev.java/` para qualquer atualização recente. **Cross-check com o Galho 4 nota 12 (Virtual Threads)**: a EDT permanece single-thread; virtual threads ajudam o trabalho de background, não substituem a EDT.

- [ ] **Step 2: Escrever a nota**

Frontmatter: `fase: magus`, tags `[java, swing, magus, estado-atual, arquitetura]`, aliases `["Swing hoje", "Estado atual do Swing"]`.

Conteúdo (capstone — decisão de arquitetura HONESTA, nem obituário nem panfleto):
- TL;DR: Swing é uma tecnologia **core e suportada** do Java SE (não deprecada), na prática com **poucas features novas**; ainda a escolha certa pra um nicho específico (ferramentas internas, IDEs, apps offline/legados), errada pra app moderno rico/web/mobile.
- `## O que é` — o estado real da API hoje.
- `## Como funciona` — H3s:
  - "O status oficial vs o consenso da comunidade" — **declaração oficial Oracle** (Swing/AWT = core Java SE, suporte enquanto o JDK for; fonte + data — Java Client Roadmap 2018/2020) **separada** do **consenso de-facto** (poucas features novas, "modo de manutenção" é jargão da comunidade, não termo oficial). **Sem estatística inventada.**
  - "Onde Swing ainda faz sentido" — ferramentas internas/admin, **IDEs (IntelliJ IDEA, NetBeans, Eclipse usam Swing/SWT)**, apps desktop offline/legados, ambientes embedded; sem dependência externa pesada.
  - "Onde Swing NÃO faz sentido" — app moderno com UI rica/animada, web, mobile, equipe sem experiência desktop.
  - "Swing × virtual threads" — a EDT continua single-thread; virtual threads (Galho 4) ajudam o background work (substituem pools em `SwingWorker`-like), **não** mudam o modelo da EDT. **Verificado.**
  - "O ecossistema vivo" — FlatLaf e ferramentas community mantêm Swing utilizável e moderno (third-party).
  - "E o JavaFX?" — gancho curto: a outra opção desktop do Java; comparação detalhada fica no **Galho 6 (JavaFX, planejado)** — **texto, sem wikilink**.
- `## Na prática` — uma árvore de decisão "devo usar Swing neste projeto?" (interno/offline/legado → talvez; moderno/web/mobile → não).
- `## Armadilhas` (de raciocínio) — ≥3: (1) tratar Swing como "morto" (é suportado e core) → declarar o status correto; (2) escolher Swing por inércia para um app moderno greenfield → avaliar web/JavaFX; (3) assumir que virtual threads "consertam" a natureza single-thread da EDT → não mudam o modelo da EDT. Cada uma com o raciocínio correto.
- `## Em entrevista` — frase 3+ sentenças enquadrando Swing como decisão de arquitetura honesta (quando sim/quando não + caveat de status); vocabulário 6+ termos.
- `### Cheatsheet do galho` — tabela "qual nota pra qual problema" (modelo→07, threading→05/06, aparência→09/10, atalhos→11).
- `## Veja também` (01, 05, 07, 09, MOC, central, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência]]`, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem]]`; Galho 6 JavaFX como **texto "(planejado)"**, sem wikilink) + `## Referências` (Oracle Java Client Roadmap 2018/2020 com data, dev.java, cross-ref Galho 4 nota 12).

Tamanho: 300-480 linhas (nota de fechamento; usar opus).

- [ ] **Step 3: Verificar**

```bash
grep -iE "core Java SE|roadmap|manutenção|virtual thread|JavaFX|planejado" "03-Dominios/Tecnologia/Java/Swing/12 - Swing hoje - estado atual.md" | head
grep -iE "[0-9]+%|porcento|por cento" "03-Dominios/Tecnologia/Java/Swing/12 - Swing hoje - estado atual.md"
```
Expected: cobre status oficial + comunidade + virtual threads + gancho JavaFX (planejado, sem wikilink); **segundo grep retorna VAZIO** (zero estatística inventada).

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/12 - Swing hoje - estado atual.md"
git commit -m "feat(java): galho 5 nota 12 — Swing hoje: estado atual (capstone)"
```

---

## Task 13: MOC do galho

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Swing/index.md`

- [ ] **Step 1: Escrever o MOC**

Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "Swing"`, tags `[java, swing, moc]`, aliases `["Swing", "Galho 5 - Swing"]`, `created`/`updated: 2026-06-03`.

Conteúdo (modelar pelo `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index.md`):
- `> [!abstract] TL;DR` — Galho 5 da trilha Java Senior; GUI desktop com Swing: componentes/containers, layouts, eventos, EDT/SwingWorker, MVC/models, L&F, custom painting e o estado atual da API.
- `## Sobre este galho` — escopo + audiência primária (senior em prep de entrevista) + secundária (decisão de arquitetura/manutenção de apps Swing) + nota de que é o **primeiro galho construído por pesquisa** (sem tronco).
- `## Iniciado` — wikilinks 01-04 (uma linha descritiva cada).
- `## Adepto` — wikilinks 05-09.
- `## Magus` — wikilinks 10-12.
- `## Rotas alternativas` — 5 rotas:
  - **Completa** — 01 → 12.
  - **Entrevista internacional** — 01 → 04 → 05 → 06 → 07 → 12.
  - **Threading do Swing** — 05 → 06 → 11.
  - **Construir uma tela do zero** — 01 → 02 → 03 → 04 → 07.
  - **Aparência e customização** — 03 → 09 → 08 → 10.
- `## Todas as notas` — bloco Dataview:

````markdown
```dataview
TABLE fase, status, updated
FROM "03-Dominios/Tecnologia/Java/Swing"
WHERE type = "concept"
SORT file.name ASC
```
````

- `## Veja também` — `[[03-Dominios/Tecnologia/Java/index|Java (MOC central)]]`, `[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (Galho 1)]]`, `[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo (Galho 4)]]`, `[[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]`. Galho 6 (JavaFX) como texto "(planejado)", SEM wikilink.

- [ ] **Step 2: Verificar**

```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Tecnologia/Java/Swing/index.md"
grep -c "\[\[" "03-Dominios/Tecnologia/Java/Swing/index.md"
grep -i "JavaFX" "03-Dominios/Tecnologia/Java/Swing/index.md"
```
Expected: 4 headings de seção; ≥12 wikilinks; "JavaFX" aparece como texto "(planejado)" SEM `[[`.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Swing/index.md"
git commit -m "feat(java): galho 5 MOC — Swing"
```

---

## Task 14: Expandir o Dicionário de Java (NÃO recriar)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`

- [ ] **Step 1: Reler o Dicionário existente**

Ler `03-Dominios/Tecnologia/Java/Dicionário de Java.md` inteiro. Mapear as seções alfabéticas existentes e os verbetes já presentes (Galhos 1 e 4). **NÃO recriar o arquivo; NÃO reordenar verbetes existentes.** Confirmar o formato de verbete (`### Termo` + definição 1-3 linhas + `Veja também: [[nota]].`).

- [ ] **Step 2: Extrair as âncoras de Dicionário usadas nas notas 01-12**

```bash
grep -rhoE "Dicionário de Java#[^]|]+" "03-Dominios/Tecnologia/Java/Swing/"
```
Anotar cada âncora referenciada pelas notas. **Cada verbete inserido deve ter heading que bate EXATAMENTE (case/acento) com a âncora usada** (regra do Galho 4). Se uma nota referencia `#cell renderer`, o heading é `### cell renderer`.

- [ ] **Step 3: Inserir os verbetes de Swing em ordem alfabética**

Inserir os ~24 verbetes abaixo na seção alfabética correta (criar seções novas se não existirem; ordenação case-insensitive, sem acento). Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` pra nota canônica do galho.

| Verbete | Seção | Nota canônica |
|---|---|---|
| Action API | A | →11 |
| adapter (event adapter) | A | →04 |
| AWT (Abstract Window Toolkit) | A | →01 |
| cell editor | C | →08 |
| cell renderer | C | →08 |
| componente lightweight / heavyweight | C | →01 |
| content pane | C | →01 |
| delegation event model | D | →04 |
| Document (modelo de texto) | D | →07 |
| double buffering | D | →10 |
| EDT (Event Dispatch Thread) | E | →05 |
| FlatLaf | F | →09 |
| GridBagLayout | G | →03 |
| InputMap / ActionMap (key bindings) | I | →11 |
| invokeLater / invokeAndWait | I | →05 |
| JComponent | J | →01 |
| layout manager | L | →03 |
| listener (event listener) | L | →04 |
| look and feel (L&F) | L | →09 |
| Nimbus | N | →09 |
| paintComponent / custom painting | P | →10 |
| pluggable look-and-feel | P | →09 |
| separable model (MVC do Swing) | S | →07 |
| SwingWorker | S | →06 |
| TableModel / ListModel | T | →07 |
| UIManager | U | →09 |

Atualizar frontmatter `updated: 2026-06-03`.

- [ ] **Step 4: Verificar**

```bash
grep -E "^### (EDT|SwingWorker|FlatLaf|paintComponent|separable model|Action API)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: verbetes de Swing presentes; contagem total de `###` subiu ~24 vs o baseline (Galhos 1+4). Verbetes anteriores intactos.

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
git commit -m "feat(java): expande Dicionário de Java com verbetes de Swing (galho 5)"
```

---

## Task 15: Ativar o Galho 5 no MOC central `Java/index.md`

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/index.md`

- [ ] **Step 1: Trocar a linha do Galho 5 por wikilink ativo**

Substituir a linha 32 (atualmente `5. Swing *(planejado)* — componentes, layout managers, EDT, MVC, estado atual de adoção`) por:

```markdown
5. [[03-Dominios/Tecnologia/Java/Swing/index|Swing]] — componentes e containers, layout managers, modelo de eventos, EDT/SwingWorker, MVC/models, Look & Feel, custom painting, estado atual da API
```

Atualizar `updated: 2026-06-03`. **Não mexer no resto do MOC** (galhos 2/3 e 6-18 permanecem como texto "(planejado)").

- [ ] **Step 2: Verificar**

```bash
grep -E "Swing/index" "03-Dominios/Tecnologia/Java/index.md"
grep -E "updated: 2026-06-03" "03-Dominios/Tecnologia/Java/index.md"
```
Expected: wikilink ativo do Galho 5; `updated` atualizado.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Java/index.md"
git commit -m "feat(java): ativa Galho 5 (Swing) no MOC central"
```

---

## Task 16: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: Conferir as 12 notas + MOC presentes**

```bash
ls "03-Dominios/Tecnologia/Java/Swing/" | sort
```
Expected: 01..12 + index.md (13 arquivos .md).

- [ ] **Step 2: Conferir frontmatter `fase` e distribuição**

```bash
for f in "03-Dominios/Tecnologia/Java/Swing/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```
Expected: toda nota 01-12 tem `fase:`; distribuição 4 iniciado / 5 adepto / 3 magus.

- [ ] **Step 3: Conferir seções obrigatórias em todas as notas**

```bash
for f in "03-Dominios/Tecnologia/Java/Swing/"[0-9]*.md; do
  echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"
done
```
Expected: cada nota retorna 3.

- [ ] **Step 4: Conferir ausência de fabricação e de wikilinks pro Galho 6**

```bash
grep -riE "minha experiência|no meu projeto|josenaldo" "03-Dominios/Tecnologia/Java/Swing/"
grep -rE "\[\[[^]]*JavaFX" "03-Dominios/Tecnologia/Java/Swing/"
```
Expected: ambos VAZIOS (zero fabricação; JavaFX nunca como wikilink — só texto "(planejado)").

- [ ] **Step 5: Rodar a skill de wikilinks**

Invocar a skill `verificar-wikilinks` na pasta `03-Dominios/Tecnologia/Java/Swing/` + `03-Dominios/Tecnologia/Java/index.md` + `03-Dominios/Tecnologia/Java/Dicionário de Java.md`. Corrigir quebrados (folder-links exigem index.md — regra Quartz). **Lembrar:** o checker dá falso-positivo em self-anchors `[[#Heading]]` — as notas evitam âncoras same-file; ignorar esse falso-positivo. **Conferir que as âncoras de `Dicionário de Java#...` usadas nas notas resolvem 1:1 com os headings dos verbetes inseridos (Task 14 Step 2).** Se houver correções, commitar à parte.

- [ ] **Step 6: Build Quartz (se disponível)**

Confirmar publicação sem erro conforme o pipeline do projeto (deploy cross-repo é manual do usuário — NÃO fazer push/deploy). Se o build não rodar localmente, registrar como verificação manual pendente.

- [ ] **Step 7: Resumo de fechamento (sem commit)**

Reportar ao usuário: notas criadas, distribuição de fases, verbetes adicionados, estado da verificação de wikilinks (e qualquer falso-positivo ignorado). Branch `java-galho-05-swing` pronta para review/merge manual (sem push).

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** as 12 notas (Tasks 1-12) cobrem o §3.1 do spec; MOC (Task 13) cobre §3.2; Dicionário expandido (Task 14) cobre §3.3; MOC central (Task 15) cobre §3.4; §3.5 (sem poda) é honrado pela ausência de task de poda; pré-flight de status (Task 0 Step 3) cobre §6; verificação final (Task 16) cobre §7. Fronteiras (§3.1 "decisões de fronteira") respeitadas: EDT/SwingWorker (05/06) donas do threading do Swing e linkam Galho 4; JavaFX só gancho na 12 (texto "planejado", sem wikilink); Galho 1 linkado nas notas 01/04; `JTable` distribuído entre 02/07/08/11.

**Placeholder scan:** sem TBD/TODO. Cada nota tem Step 1 com URLs de fonte oficial nomeadas, frontmatter concreto, outline de seções, armadilhas mínimas (≥2 Iniciado / ≥3 Adepto-Magus) e tamanho-alvo. Capstone (12) com verificação obrigatória + grep anti-estatística.

**Type/naming consistency:** numeração 01-12 consistente entre tasks, MOC (rotas/seções), Dicionário (notas canônicas) e verificação. Distribuição 4/5/3 consistente no header, nas fases das tasks e na Task 16 Step 2. Notas opus (05/06/07/12) marcadas ⟦opus⟧ com o modelo indicado no Step 1. Nomes de arquivo sem `:` (usado `-` em "09 - Look and Feel e temas" e "12 - Swing hoje - estado atual") pra evitar problema de filesystem. Âncoras do Dicionário conferidas 1:1 (Task 14 Step 2 + Task 16 Step 5).
