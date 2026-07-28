---
title: "Padrões WAI-ARIA APG II"
created: 2026-07-27
updated: 2026-07-27
type: concept
status: seedling
fase: Adepto
tags:
  - acessibilidade
  - a11y
  - aria
  - apg
publish: true
---

# Padrões WAI-ARIA APG II

> [!abstract] TL;DR
> Estes são os widgets que separam quem lê o APG de quem improvisa: **combobox** (input + lista de sugestões), **menu/menubar** (menu de aplicação, não de navegação), **listbox** (seleção de uma lista), **tree** (hierarquia expansível) e **grid** (navegação bidimensional por células). O que os torna difíceis é o **teclado**: setas em duas direções, `Home`/`End`, digitação para pular itens (*typeahead*), `Enter`/`Espaço` com significados distintos. A moral prática, que a próxima nota desenvolve: para estes cinco, **quase ninguém deveria escrever do zero** — o custo de acertar o contrato inteiro é alto demais, e existem bibliotecas testadas que o entregam. Conhecer o padrão é o que te deixa *avaliar* e *depurar* essas bibliotecas, não reinventá-las.

A nota anterior cobriu os padrões de complexidade gerenciável. Agora os pesos-pesados. Se disclosure era um botão com um atributo, um **grid** acessível é uma máquina de estados de teclado com navegação em duas dimensões. É aqui que a frase "no ARIA is better than bad ARIA" morde mais forte: um combobox meio-implementado é ativamente pior que um `<select>` feio, porque promete uma interação rica e entrega uma armadilha.

## Combobox: o campeão de implementações quebradas

O **combobox** é onipresente — todo campo de busca com autocomplete, todo seletor com filtro é um. E é provavelmente o widget mais mal-implementado da web, porque parece simples (um input com uma listinha embaixo) e é traiçoeiro (o foco fica no input enquanto a "seleção" percorre a lista).

O contrato da APG, resumido:

```html
<label for="busca">Cidade</label>
<input
  id="busca" role="combobox"
  aria-expanded="false" aria-controls="lista"
  aria-activedescendant=""  autocomplete="off"
>
<ul id="lista" role="listbox" hidden>
  <li role="option" id="opt-1">São Paulo</li>
  <li role="option" id="opt-2">Salvador</li>
</ul>
```

O segredo está em como o foco funciona — e é um conceito novo:

- **O foco de teclado *nunca sai do input*.** O usuário digita normalmente. As setas ↓/↑ **não movem o foco** para a lista; em vez disso, mudam qual opção está "ativa".
- **`aria-activedescendant`** aponta para o `id` da opção ativa. É esse atributo — não o foco de verdade — que diz ao leitor de tela "a opção São Paulo está destacada agora". Chama-se *padrão de foco gerenciado por descendente ativo*, alternativa ao roving tabindex para casos em que o foco físico precisa ficar num lugar só.
- **Estado:** `aria-expanded` abre/fecha a lista; `aria-selected` na opção escolhida.
- **Teclado:** ↓/↑ percorrem opções, `Enter` seleciona, `Esc` fecha a lista, digitar filtra.

> [!question]- `aria-activedescendant` ou roving tabindex — quando cada um?
> São as duas estratégias de foco para widgets compostos, e a escolha depende de *onde o foco físico precisa estar*. Use **roving tabindex** (nota 06) quando o foco realmente se move entre os elementos do grupo — abas, toolbar, radiogroup: cada item, ao ficar ativo, recebe `.focus()` de fato. Use **`aria-activedescendant`** quando o foco precisa ficar **parado num elemento** (tipicamente um input onde o usuário digita) enquanto uma "seleção virtual" percorre outra lista — combobox, alguns listboxes. No primeiro, o foco viaja; no segundo, o foco fica e um ponteiro virtual viaja. Escolher errado quebra a digitação ou a navegação.

## Menu e menubar: o menu que não é de navegação

Cuidado com uma confusão de nomes que causa muito ARIA errado: o padrão **`menu`/`menubar`** da APG **não** é o menu de navegação do seu site (aquela barra com "Home, Sobre, Contato"). Aquilo é uma lista de links — use `<nav>` com `<ul>`/`<a>`, e pare por aí. O role `menu` é para **menus de aplicação**: o menu de um editor ("Arquivo, Editar, Ver"), um menu de contexto (botão direito), um dropdown de *ações* dentro de um app.

> [!warning] `role="menu"` no menu de navegação do site
> **O que acontece:** você põe `role="menu"` e `role="menuitem"` na navegação principal. Agora o leitor de tela entra em "modo aplicação", espera navegação por setas, e o comportamento de links normais fica estranho — Tab não percorre os itens como o usuário espera de uma navegação.
> **Por quê:** `menu`/`menuitem` sinalizam um menu de *comandos de aplicação* com semântica e teclado próprios (setas, não Tab). Uma navegação de site é uma lista de links, semanticamente diferente.
> **Como evitar:** navegação = `<nav><ul><li><a>`. Reserve `role="menu"` para menus de ação de aplicação de verdade, onde o teclado por setas faz sentido.

Quando é de fato um menu de aplicação, o contrato inclui: role `menu`/`menubar` no container, `menuitem` (ou `menuitemcheckbox`/`menuitemradio`) nos itens, navegação por **setas** (não Tab), `Esc` para fechar, `Enter`/`Espaço` para ativar, e retorno de foco ao botão que abriu o menu.

## Listbox, tree e grid: navegação estruturada

Os três restantes compartilham a ideia de **navegar uma estrutura por teclado**, cada um numa forma:

- **Listbox** (`role="listbox"` + `option`) — uma lista de onde se seleciona um ou mais itens, como um `<select>` estilizado. Foco na listbox, setas movem a seleção, `Home`/`End` para as pontas, digitação faz *typeahead*. Antes de usá-lo, a pergunta de sempre: um `<select>` nativo não resolve? Quase sempre resolve, e é infinitamente mais barato.
- **Tree** (`role="tree"` + `treeitem` + `group`) — uma hierarquia expansível, como o explorador de arquivos de uma IDE. Setas ↓/↑ navegam itens visíveis; **seta → expande** um nó (ou entra no filho); **seta ← recolhe** (ou volta ao pai); `aria-expanded` marca nós abertos; `aria-level` indica profundidade. É navegação em árvore, com o teclado espelhando a estrutura.
- **Grid** (`role="grid"` + `row` + `gridcell`) — o mais complexo: navegação **bidimensional** por células, como uma planilha ou um data table interativo. Setas movem em quatro direções célula a célula, `Home`/`End` vão às pontas da linha, `Ctrl+Home`/`Ctrl+End` ao canto da grade. Note: `role="grid"` é para tabelas **interativas** (navegáveis por seta, com células editáveis ou selecionáveis); para uma tabela de *dados* comum, use `<table>` nativo — ele já é acessível e não precisa de nada disso.

O padrão de teclado que atravessa os três — setas para navegar, `Home`/`End` para extremos, typeahead para pular — é o mesmo que o usuário já conhece de componentes nativos do sistema operacional. Seguir a APG é, no fundo, **respeitar as expectativas de teclado que o usuário traz de fora** do seu app.

## A conclusão honesta: não escreva do zero

Chegando ao fim do catálogo, é hora da moral prática, que vai contra o instinto do engenheiro. Você acabou de ver que um combobox tem `aria-activedescendant` + gestão de estado da lista + cinco teclas; que um grid tem navegação 2D completa. Implementar *um* desses corretamente, testar em NVDA + JAWS + VoiceOver, cobrir os edge cases de teclado — é dias de trabalho, e o WebAIM mostra que a maioria erra.

Por isso a recomendação da comunidade e deste domínio: **para os widgets complexos, use uma biblioteca de componentes acessíveis** (Radix, React Aria, e afins) que já implementa esses contratos, os testa e os mantém. O valor de ter lido esta nota não é para você reescrever o combobox — é para você **avaliar** se a lib que escolheu implementa o contrato certo, **depurar** quando o leitor de tela faz algo estranho, e **saber o que está quebrado** quando o teste manual falha. Você aprende o padrão para julgar a ferramenta, não para substituí-la.

**APG II em uma frase:** combobox, menu, listbox, tree e grid são widgets de teclado intrincado que quase ninguém deveria escrever à mão — conheça o contrato para avaliar e depurar as bibliotecas que o implementam, e sempre pergunte antes se um `<select>`/`<table>` nativo já resolve.

> [!tip] Vídeo — depurar widgets ARIA quebrados
> [**Debugging broken accessibility**](https://www.youtube.com/watch?v=In2sH3h_fJg) (Sarah Higley, Inclusive Design 24, ~50 min) — a autoridade da comunidade em comboboxes mostra, na prática, como widgets ARIA complexos quebram e como diagnosticá-los. É exatamente a habilidade que esta nota defende: você aprende o padrão não para reescrevê-lo, mas para *avaliar e depurar* o que a biblioteca (ou o colega) entregou.

## Casos práticos

**Caso 1 — o combobox que deixava o foco vazar.** Um campo de busca com autocomplete foi implementado só com JavaScript de posicionamento: ao apertar ↓, o código dava `.focus()` na primeira sugestão da lista. Funcionava visualmente — a opção ficava destacada — mas o cursor de texto sumia do input, e o usuário de leitor de tela ouvia o app "pular" para fora do campo que estava digitando. A correção foi trocar o roving tabindex por `aria-activedescendant`: o foco real nunca sai do `<input>`, e é o atributo — não o `.focus()` — que aponta a opção ativa. O comportamento visual não mudou nem um pixel; o que mudou foi inteiramente invisível pra quem enxerga a tela, e decisivo pra quem não enxerga.

**Caso 2 — o grid que não precisava existir.** Um dashboard interno pediu uma "tabela editável" e o time montou um `role="grid"` completo — navegação por setas, `gridcell`, `aria-selected` por célula — porque "table normal não tem navegação por teclado". Só que os dados eram só para leitura: nenhuma célula era editável ou selecionável, era um relatório. Um `<table>` nativo com `<th scope="col">` já entrega leitura por leitor de tela, ordenação por coluna via cabeçalho e nenhuma linha de JavaScript de teclado. O `role="grid"` foi trocado por `<table>` puro e o código de navegação 2D — a parte mais cara de manter — foi deletado inteiro. `role="grid"` existe para quando a interação é de fato bidimensional (planilha, células editáveis); para dado que só se lê, é over-engineering acessível.

## Armadilhas comuns

> [!warning] `role="menu"` na navegação do site
> **O que acontece:** a navegação principal (`Home`, `Sobre`, `Contato`) ganha `role="menu"`/`role="menuitem"`. O leitor de tela entra em modo de menu de aplicação, passa a esperar navegação por setas, e `Tab` para de se comportar como o usuário espera de uma lista de links.
> **Por quê:** `menu`/`menuitem` sinalizam comandos de *aplicação*, com teclado próprio (setas, `Esc`, retorno de foco). Uma navegação de site é semanticamente uma lista de links, não um menu de app.
> **Como evitar:** navegação = `<nav><ul><li><a>`, sem roles extras. Reserve `role="menu"` para menus de ação reais (editor, menu de contexto, dropdown de comandos).

> [!warning] Combobox sem `aria-activedescendant`
> **O que acontece:** o widget parece funcionar — a opção destacada muda de cor ao apertar ↓ — mas o leitor de tela nunca anuncia qual opção está ativa, porque o foco real nunca saiu do input e nada além do CSS mudou.
> **Por quê:** sem `aria-activedescendant` apontando pro `id` da opção ativa, não existe nenhum sinal programático de "seleção virtual" — só a aparência visual, que tecnologia assistiva não lê.
> **Como evitar:** sempre que o foco físico ficar no input (padrão combobox), atualize `aria-activedescendant` a cada mudança de opção ativa, e sincronize com `aria-selected` na opção correspondente.

> [!warning] Escrever grid do zero em vez de `<table>`
> **O que acontece:** o time implementa `role="grid"` completo — navegação 2D, `Home`/`End`, `Ctrl+Home`/`Ctrl+End` — para exibir dados que são só leitura.
> **Por quê:** `role="grid"` existe para tabelas *interativas* (células editáveis/selecionáveis por teclado). Para dado estático, é complexidade paga à toa: mais JavaScript pra manter, mais superfície pra quebrar, zero ganho de acessibilidade sobre um `<table>` nativo.
> **Como evitar:** pergunte antes: alguma célula é editável ou selecionável individualmente? Se não, `<table>` com `<th scope>` resolve — já é acessível por padrão.

> [!warning] Escolher roving tabindex quando devia ser `aria-activedescendant` (ou vice-versa)
> **O que acontece:** um combobox implementado com roving tabindex faz o foco pular fisicamente pra dentro da lista de sugestões — e o cursor de texto do input desaparece a cada seta. Ou o inverso: uma toolbar de botões implementada com `aria-activedescendant` deixa os botões "inalcançáveis" por foco real, quebrando clique e outras interações que dependem de foco físico.
> **Por quê:** as duas estratégias resolvem o mesmo problema (mover "o item ativo" num grupo) de formas opostas — uma move o foco de verdade, a outra mantém o foco parado e move um ponteiro virtual — e servem contextos diferentes.
> **Como evitar:** pergunte onde o foco físico *precisa* ficar. Se o usuário está digitando em algum lugar (input), use `aria-activedescendant`. Se os itens do grupo são eles mesmos focáveis/clicáveis (abas, toolbar, radiogroup), use roving tabindex.

## Como explicar em inglês

In an interview, this is the kind of nuance that signals you've actually built these widgets, not just read the spec. The line I'd use: *"The hardest part of an accessible combobox isn't the visual dropdown — it's that keyboard focus never leaves the input. You track the active option with `aria-activedescendant` instead of moving real DOM focus, which is the opposite strategy from something like a tab list, where you'd use roving tabindex because focus really does need to move between elements."* That one sentence shows you know both patterns exist, and — more importantly — that you know *when* to reach for each one, which is the actual skill being tested.

| PT | EN |
|---|---|
| combobox | combobox |
| descendente ativo | active descendant |
| tabindex circulante / foco gerenciado por rotação | roving tabindex |
| caixa de seleção (lista) | listbox |
| árvore (hierarquia expansível) | tree (view) |
| grade (navegação bidimensional) | grid |
| foco de teclado | keyboard focus |
| tecla de atalho para pular itens digitando | typeahead |

## O que vem a seguir

A conclusão desta nota — "use uma biblioteca" — merece o cuidado de saber *quais* e *como*, porque "biblioteca de componentes" não é sinônimo de "acessível". Algumas resolvem a11y de verdade; outras são só estilo. A próxima nota separa uma coisa da outra no ecossistema React.

- [[03-Dominios/Tecnologia/Acessibilidade/Construir Acessível/10 - A11y em React e component libraries|10 — A11y em React e component libraries]] — Radix, React Aria, Headless UI: o que resolvem e o que não.
- [[03-Dominios/Tecnologia/Acessibilidade/Auditar e Testar/14 - Testes de a11y no código|14 — Testes de a11y no código]] — como provar que o widget (seu ou da lib) cumpre o contrato.
- [[03-Dominios/Tecnologia/Acessibilidade/Construir Acessível/08 - Padrões WAI-ARIA APG I|08 — APG I]] — os padrões mais simples que esta nota pressupõe.

## Fontes

- **W3C WAI** — [*APG — Combobox Pattern*](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/) — o contrato completo do widget mais mal-implementado, incluindo `aria-activedescendant`.
- **W3C WAI** — [*APG — Menu and Menubar*](https://www.w3.org/WAI/ARIA/apg/patterns/menubar/), [*Grid*](https://www.w3.org/WAI/ARIA/apg/patterns/grid/), [*Tree View*](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/) — os contratos de teclado dos widgets estruturados.
- **W3C WAI** — [*Managing Focus Within Components (activedescendant vs roving tabindex)*](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/) — as duas estratégias de foco comparadas.
- **Sarah Higley** — [*"Playing" with automated accessibility testing / Comboboxes*](https://sarahmhigley.com/writing/select-your-poison/) — análise das armadilhas reais de implementar comboboxes.
