---
title: "Dicionário de Fundamentos"
created: 2026-06-07
updated: 2026-06-07
type: glossary
status: seedling
aliases:
  - Glossário de Fundamentos
tags:
  - glossary
  - fundamentos
lang: pt
publish: true
---

# Dicionário de Fundamentos

> Termos de ciência da computação e engenharia de software que sobrevivem à troca de linguagem, framework ou paradigma — o vocabulário comum das outras estantes.

<!--
Como usar este glossário:

- Cada verbete é um `###` dentro de uma `##` temática.
- Linkar de outra nota: [[Dicionário de Fundamentos#Nome do termo]]
- Customizar texto exibido: [[Dicionário de Fundamentos#Nome do termo|texto]]
- A skill /verbete adiciona termos automaticamente em ordem alfabética.
- Ajuste `lang:` no frontmatter (`pt` ou `en`) — define o idioma das definições.
-->

## Abstração e design

### Abstração que vaza (leaky abstraction)
Abstração que falha em esconder completamente a complexidade subjacente que pretendia simplificar, forçando quem a usa a entender detalhes da camada de baixo. Termo de Joel Spolsky (*The Law of Leaky Abstractions*, 2002): "toda abstração não-trivial, em algum grau, vaza" — abstrações poupam tempo de trabalho, mas não de aprendizado.

*Veja também: [[Abstrações que vazam]]*

## Performance e observabilidade

### p99
Percentil 99 de uma métrica — tipicamente latência: o valor abaixo do qual ficam 99% das requisições, ou seja, apenas 1% é mais lento que isso. Usado em SLOs e monitoramento porque médias escondem a cauda da distribuição: p50 (mediana) descreve o caso típico, enquanto p95/p99/p999 revelam a experiência dos piores casos — justamente onde pausas de GC, lock contention e cold starts aparecem.
