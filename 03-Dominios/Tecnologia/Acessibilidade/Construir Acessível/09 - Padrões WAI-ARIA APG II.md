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
