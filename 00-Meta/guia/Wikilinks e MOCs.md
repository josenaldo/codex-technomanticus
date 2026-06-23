---
title: "Wikilinks e MOCs"
created: 2026-04-28
updated: 2026-04-28
type: how-to
status: seedling
tags:
  - guia
  - meta
publish: false
---

# Wikilinks e MOCs

Como conectar notas no Codex. O valor de um vault não está nas notas isoladas — está na rede que elas formam.

## Wikilinks

### Sintaxe

```markdown
[[Nome da Nota]]                  Link simples
[[Nome da Nota|texto exibido]]    Alias inline (display custom)
[[Nome da Nota#Heading]]          Link pra um heading específico
[[#Heading nesta nota]]            Link interno na mesma nota
```

### Quando usar wikilink vs link Markdown

- **`[[wikilink]]`** — sempre que linkar pra outra nota dentro do vault. Obsidian rastreia renomeações automaticamente.
- **`[texto](url)`** — só pra URLs externas (artigos, docs oficiais, repos no GitHub).

### Sem path absoluto

Prefira `[[Spring Boot]]` em vez de `[[03-Dominios/Tecnologia/Java/Spring Boot]]`. Obsidian resolve por filename, e wikilinks com path quebram quando você reorganiza pastas.

Exceção: quando há **dois arquivos com o mesmo nome** em pastas diferentes. Aí o path resolve a ambiguidade. Em geral, evite duplicar nomes — renomeie um dos dois.

### Linkar antes de existir

Você pode escrever `[[Conceito que ainda não escrevi]]` numa nota. Obsidian mostra o link em vermelho/cinza ("link não-resolvido"). Isso é útil:

- Cria placeholders pra notas futuras
- Mostra na sidebar de "Unresolved Links" o que está sendo demandado pelo vault
- Quando você finalmente cria a nota com aquele nome, todos os links retroativos passam a funcionar

### Aliases pra variações de nome

Use o campo `aliases` no frontmatter pra que outras formas do nome resolvam pro mesmo arquivo:

```yaml
aliases:
  - Spring Framework
  - Spring (Java)
```

Aí `[[Spring Framework]]` em qualquer nota vai pra `Spring Boot.md` (se essa é a nota canônica).

### Densidade de links

Uma nota saudável tem **3-7 wikilinks saindo**. Menos que isso e ela está isolada; mais que isso e provavelmente quebrou a regra de atomicidade ([[Convenções de escrita]]).

A seção "Veja também" no final é o lugar canônico pra wikilinks adicionais que não couberam no corpo.

## MOCs (Maps of Content)

### O que é um MOC

Um MOC é um índice curatorial de uma área. Não é tabela de conteúdo gerada automaticamente — é uma lista **selecionada e ordenada** das notas que importam, com seções que fazem sentido pra navegação.

### MOC de Domínio vs MOC de Senda

| Tipo            | Localização          | Função                                                              |
| --------------- | -------------------- | ------------------------------------------------------------------- |
| MOC de Domínio  | `03-Dominios/X/X.md` | Mapa estático da área: que conceitos existem, organizados por tema. |
| Senda           | `04-Sendas/Senda <Tema>.md` | Trilha sequencial pra atender objetivo (estudo, prep entrevista). Tem ordem. |

**A diferença essencial:** MOC de Domínio responde "o que existe sobre X?". Senda responde "em que ordem estudo X pra alcançar Y?".

### Quando criar um MOC

Crie quando uma pasta de Domínio tiver **5+ notas** e você sentir que precisa de orientação pra navegar entre elas. Antes disso, a própria estrutura de pasta basta.

### Anatomia de um MOC vivo

Um bom MOC tem:

1. **Introdução de 2-3 frases** descrevendo o que a área cobre
2. **Seções temáticas** (não alfabéticas) — agrupe por subtema, não por inicial
3. **Wikilinks pra notas existentes** — não invente entradas vazias
4. **Dataview opcional** no final, pra listar automaticamente notas que você esqueceu de adicionar:

````markdown
```dataview
LIST
FROM "03-Dominios/Tecnologia/Java"
WHERE type != "moc"
SORT file.name ASC
```
````

### MOC desatualizado mente

A maior armadilha de MOC é virar fóssil. Quando você cria uma nota nova em `03-Dominios/Tecnologia/Java/`, **o MOC `Java.md` precisa ser atualizado** ou ele estará escondendo conteúdo. Por isso o bloco Dataview no fim ajuda — ele lista o que está lá fisicamente, mesmo que o MOC manual não cite.

Rotina de revisão de MOCs em [[Manutenção do vault]].

## Veja também

- [[Convenções de escrita]] — atomicidade e filenames
- [[Como usar este vault]] — onde os MOCs ficam
