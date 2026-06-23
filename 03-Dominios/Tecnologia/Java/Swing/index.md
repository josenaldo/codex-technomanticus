---
title: "Swing"
type: moc
status: growing
publish: true
created: 2026-06-03
updated: 2026-06-03
tags:
  - java
  - swing
  - moc
aliases:
  - Swing
  - Galho 5 - Swing
---
# Swing

> [!abstract] TL;DR
> **Galho 5 da trilha Java Senior.** GUI desktop com Swing, do modelo de componentes ao estado atual da API: componentes e containers, layout managers, modelo de eventos, a **Event Dispatch Thread (EDT)** e `SwingWorker`, **MVC/separable model** (`TableModel`/`ListModel`), renderers e editors, Look and Feel, custom painting, Action API/key bindings e uma capstone honesta sobre **quando (não) usar Swing hoje**. 12 notas atômicas em 3 fases (Iniciado/Adepto/Magus), cada uma com seção "Em entrevista" em inglês.

## Sobre este galho

Swing é a primeira das duas interfaces desktop da trilha (a outra é o Galho 6, JavaFX). O galho é dono do **modelo de GUI desktop Swing** e do **threading do Swing** (a regra single-thread da EDT, `SwingWorker`) — para os primitivos de concorrência subjacentes, linka para o [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Galho 4 (Concorrência)]] em vez de re-explicar.

É também o **primeiro galho construído por pesquisa**, não por refator de um monolito: não havia um tronco `Swing.md` para podar. Cada nota nasce de documentação oficial (The Java Tutorials — *Creating a GUI with Swing*, `dev.java`, Javadoc `javax.swing`) verificada na escrita.

**Audiência primária:** dev senior em preparação para entrevista internacional — precisa explicar o modelo (por que single-thread, lightweight vs heavyweight), reconhecer armadilhas em code review e decidir arquitetura com honestidade. **Audiência secundária:** quem mantém ou avalia uma aplicação Swing em produção (ferramentas internas, IDEs, apps legados).

## Iniciado

Vocabulário e modelo mental — o suficiente para montar uma tela funcional.

- [[03-Dominios/Tecnologia/Java/Swing/01 - O modelo do Swing|01 — O modelo do Swing]] — o que é Swing, lightweight vs heavyweight (AWT), hierarquia `Component`→`JComponent`, top-level containers e content pane, pluggable look-and-feel.
- [[03-Dominios/Tecnologia/Java/Swing/02 - Componentes e containers|02 — Componentes e containers]] — o catálogo de widgets: botões, labels, campos de texto, seleção, `JTable`/`JTree`, containers intermediários, menus, toolbars e diálogos.
- [[03-Dominios/Tecnologia/Java/Swing/03 - Layout managers|03 — Layout managers]] — `BorderLayout`, `FlowLayout`, `GridLayout`, `BoxLayout`, `CardLayout`, `GridBagLayout`, aninhamento e sizing; o anti-pattern do null layout.
- [[03-Dominios/Tecnologia/Java/Swing/04 - O modelo de eventos|04 — O modelo de eventos]] — o delegation event model: listeners, event objects, lambdas vs classes anônimas vs adapters.

## Adepto

Domínio operacional — usar Swing com confiança.

- [[03-Dominios/Tecnologia/Java/Swing/05 - A Event Dispatch Thread|05 — A Event Dispatch Thread (EDT)]] — a single-thread rule, `invokeLater`/`invokeAndWait`, a regra de ouro; o coração do threading do Swing.
- [[03-Dominios/Tecnologia/Java/Swing/06 - SwingWorker e tarefas em background|06 — SwingWorker e tarefas em background]] — `doInBackground`/`publish`/`process`/`done`, progresso, cancelamento; o handoff worker→EDT sem congelar a UI.
- [[03-Dominios/Tecnologia/Java/Swing/07 - MVC em Swing e os models|07 — MVC em Swing e os models]] — a separable model architecture: `TableModel`/`AbstractTableModel`, `ListModel`, `Document`, model listeners e eventos `fireTable…`.
- [[03-Dominios/Tecnologia/Java/Swing/08 - Renderers e editors|08 — Renderers e editors]] — cell renderers e editors, o rubber-stamp pattern, customizar a aparência de células em `JTable`/`JList`.
- [[03-Dominios/Tecnologia/Java/Swing/09 - Look and Feel e temas|09 — Look and Feel e temas]] — pluggable L&F, `UIManager`, Metal/Nimbus/system, FlatLaf (third-party), customização leve.

## Magus

Maestria e decisão de arquitetura.

- [[03-Dominios/Tecnologia/Java/Swing/10 - Custom painting e componentes customizados|10 — Custom painting e componentes customizados]] — `paintComponent`/`Graphics2D`, a paint chain, double buffering, `repaint` vs `revalidate`, criar componentes próprios.
- [[03-Dominios/Tecnologia/Java/Swing/11 - Action API, key bindings e performance|11 — Action API, key bindings e performance]] — `Action`/`AbstractAction` compartilhado, `InputMap`/`ActionMap` (por que vence `KeyListener`), responsividade e models grandes.
- [[03-Dominios/Tecnologia/Java/Swing/12 - Swing hoje - estado atual|12 — Swing hoje: estado atual]] — *(capstone)* status oficial vs consenso da comunidade, onde Swing faz sentido vs não, Swing × virtual threads, e o gancho para o JavaFX. Decisão de arquitetura honesta.

## Rotas alternativas

- **Completa** — 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12 (o galho inteiro, em ordem).
- **Entrevista internacional** — 01 → 04 → 05 → 06 → 07 → 12 (o modelo, eventos, EDT, SwingWorker, models e o estado atual — o que mais cai).
- **Threading do Swing** — 05 → 06 → 11 (EDT, SwingWorker e responsividade; liga ao [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Galho 4]]).
- **Construir uma tela do zero** — 01 → 02 → 03 → 04 → 07 (montar uma UI funcional alimentada por dados).
- **Aparência e customização** — 03 → 09 → 08 → 10 (layouts, Look and Feel, renderers e pintura customizada).

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Tecnologia/Java/Swing"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Java (MOC central)]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|Linguagem e sintaxe moderna (Galho 1)]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo (Galho 4)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]
- [[03-Dominios/Tecnologia/Java/JavaFX/index|JavaFX (Galho 6)]] — a outra interface desktop do Java.
