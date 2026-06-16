---
title: "Dicionário de Fundamentos"
created: 2026-06-07
updated: 2026-06-16
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

### Information hiding
Princípio de Parnas (*On the Criteria To Be Used in Decomposing Systems into Modules*, 1972): cada módulo deve esconder uma decisão de design propensa a mudar, localizando o impacto de mudanças futuras. Não é "esconder dados" nem decompor pelos passos do fluxograma — é guardar a decisão volátil atrás de uma interface estável.

*Veja também: [[05 - Abstração - a ferramenta central]]*

### Lei de Hyrum (Hyrum's Law)
Com um número suficiente de usuários de uma API, todo comportamento observável passa a ser dependido por alguém, independentemente do que o contrato promete. É o extremo lógico do vazamento de abstrações: em escala, toda a implementação vira interface implícita — alguém depende até dos bugs (Hyrum Wright / Titus Winters, *Software Engineering at Google*).

*Veja também: [[06 - Abstrações que vazam]]*

## Complexidade e dívidas

### Carga cognitiva
Esforço mental momentâneo e individual para entender e mudar um trecho de código com segurança. É distinta do débito cognitivo, que é uma propriedade coletiva e acumulada ao longo do tempo: a carga é o custo do "agora" de uma pessoa diante do código.

*Veja também: [[08 - Carga cognitiva e legibilidade]]*

### Complexidade acidental
Complexidade que vem das ferramentas, da linguagem e da representação escolhidas — não do problema em si. É onde o esforço de engenharia compensa, porque pode ser reduzida com melhores abstrações, linguagens e ferramentas.

*Veja também: [[02 - Complexidade essencial vs. acidental]]*

### Complexidade essencial
Complexidade inerente ao problema que o software resolve. Em larga medida é irredutível: nenhuma ferramenta ou linguagem melhor a elimina, porque ela é da natureza do domínio, não da implementação (Fred Brooks, *No Silver Bullet*).

*Veja também: [[02 - Complexidade essencial vs. acidental]]*

### Débito cognitivo
Erosão, ao longo do tempo, do entendimento compartilhado que uma equipe tem sobre o sistema. É uma propriedade de nível de projeto (coletiva e temporal), não o esforço individual de um leitor — distinção que o separa da carga cognitiva (Margaret-Anne Storey, *Triple Debt Model*).

*Veja também: [[11 - Dívida cognitiva]]*

### Débito de intenção
Ausência ou erosão do rationale externalizado — metas, restrições e o porquê das decisões — que explica por que o sistema é como é. Diferente das outras dívidas, vive nos artefatos (specs, ADRs, AGENTS.md) ou na falta deles, e só humanos a geram (Storey; Addy Osmani).

*Veja também: [[12 - Dívida de intenção]]*

### Débito técnico
Custo futuro acumulado por atalhos de implementação. Como um empréstimo, cobra "juros" na forma de manutenção mais cara a cada mudança, até ser pago por refatoração — metáfora cunhada por Ward Cunningham.

*Veja também: [[10 - Dívida técnica]]*

### Entropia de software
Tendência de um sistema a aumentar em desordem e complexidade conforme é modificado, a menos que se gaste energia ativa para contê-la. É o "software rot": sem manutenção deliberada, a estrutura decai e fica cada vez mais cara de mudar.

*Veja também: [[13 - Entropia de software e decaimento]]*

### Lei de Conway
Organizações que projetam sistemas produzem desenhos cuja estrutura espelha a estrutura de comunicação da própria organização (Melvin Conway, 1968).

*Veja também: [[16 - Lei de Conway]]*

## Performance e observabilidade

### p99
Percentil 99 de uma métrica — tipicamente latência: o valor abaixo do qual ficam 99% das requisições, ou seja, apenas 1% é mais lento que isso. Usado em SLOs e monitoramento porque médias escondem a cauda da distribuição: p50 (mediana) descreve o caso típico, enquanto p95/p99/p999 revelam a experiência dos piores casos — justamente onde pausas de GC, lock contention e cold starts aparecem.
