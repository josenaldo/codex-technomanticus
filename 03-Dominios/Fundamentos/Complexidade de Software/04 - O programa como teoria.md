---
title: "O programa como teoria"
created: 2026-05-26
updated: 2026-06-16
type: concept
progress: backlog
status: evergreen
fase: iniciado
tags:
  - fundamentos
  - engenharia-de-software
  - complexidade-de-software
  - iniciado
aliases:
  - O programa como teoria
  - Teoria do programa
  - Theory building
  - Programming as Theory Building
  - Programação como construção de teoria
publish: false
---

# O programa como teoria

A tese de Peter Naur de que programar não é produzir texto (código), e sim **construir uma teoria** — um conhecimento em grande parte tácito que vive na mente de quem desenvolve, não no artefato.

> [!abstract] TL;DR
> Em *Programming as Theory Building* (1985), Peter Naur argumenta que o produto real da programação não é o código, mas a **teoria** que os desenvolvedores formam: como o programa corresponde ao mundo, por que está estruturado assim, e como evoluí-lo de forma coerente. Código e documentação são externalizações *parciais* dessa teoria. Quando a equipe que a detém se dispersa, o programa "morre" — ainda compila, mas ninguém consegue modificá-lo com segurança. É a base teórica do [[Débito cognitivo|débito cognitivo]].

## O que é

Naur parte da distinção de **Gilbert Ryle** (*The Concept of Mind*, 1949) entre *knowing-that* (saber proposicional — fatos) e *knowing-how* (saber-fazer — uma capacidade). Ter uma "teoria" de algo, no sentido de Ryle, não é possuir um texto: é ter a **capacidade** de explicar, justificar e responder a situações novas.

A tese central: **programar é construir uma teoria, não produzir texto.** O código-fonte e a documentação são, no máximo, registros parciais dessa teoria. A teoria de verdade — *knowing-how* — mora na cabeça dos programadores.

## A teoria do programador — três componentes

A teoria que um desenvolvedor tem de um programa lhe permite:

1. **Mapear o programa ao mundo** — explicar como cada parte do código corresponde aos assuntos do domínio real que ele resolve.
2. **Justificar a estrutura (o "porquê")** — dizer por que o programa está organizado *assim* e não de outro jeito; quais decisões foram tomadas, contra quais alternativas, e sob quais restrições.
3. **Evoluir com coerência** — responder a novas demandas estendendo o programa de modo consistente com seu design, sem violá-lo.

Quem tem a teoria responde a essas três coisas; quem só tem o texto, não.

## Por que a teoria não cabe na documentação

A teoria é majoritariamente **tácita** (no sentido de Michael Polanyi: "sabemos mais do que conseguimos dizer"). Documentação e código conseguem registrar *parte* do "o quê", mas o "porquê" e a capacidade de julgar mudanças coerentes resistem à externalização completa. Por isso, por melhor que seja a documentação, ela nunca transmite a teoria por inteiro — ela ajuda quem já está reconstruindo a teoria, mas não a substitui.

## A morte e o renascimento do programa

O corolário mais citado de Naur: **um programa morre quando a equipe que detém sua teoria se dispersa.** O que resta é texto — ainda executa, mas modificações feitas por quem não tem a teoria tendem a ser remendos que não se encaixam no design, degradando o sistema. Reviver o programa não é ler a documentação: é **reconstruir a teoria**, trabalho lento, caro e que só pessoas podem fazer.

## Por que importa hoje

Naur já desafiava a "visão de produção" da programação — a ideia de que programar é fabricar texto e que, portanto, programadores são intercambiáveis e métodos podem mecanizar a produção. Se o programa é uma teoria, o ativo é a **mente** que a sustenta.

Quarenta anos depois, o conceito ressurge por causa da IA generativa: ela barateia a produção do *texto* sem necessariamente construir a *teoria* na cabeça de ninguém. Gera-se o artefato pulando o trabalho de *theory building* — e o programa nasce já na condição de "morto" no sentido de Naur. Esse é o mecanismo por trás do [[Débito cognitivo]].

## Referências

- **Peter Naur** — *Programming as Theory Building* (1985). *Microprocessing and Microprogramming*, vol. 15, pp. 253–261. Reimpresso em *Computing: A Human Activity* (ACM Press, 1992).
- **Gilbert Ryle** — *The Concept of Mind* (1949) — a distinção *knowing-that* × *knowing-how* que Naur retoma.
- **Michael Polanyi** — *The Tacit Dimension* (1966) — conhecimento tácito ("sabemos mais do que conseguimos dizer").

## Veja também

- [[01 - A complexidade como problema central]] — abre o galho Complexidade de Software, onde esta nota é a fase Iniciado
- [[11 - Dívida cognitiva]] — a erosão dessa teoria em nível de projeto, sob a lente geral
- [[15 - Pensamento sistêmico]] — o software como sistema sociotécnico de pessoas + código + processo
- [[Débito cognitivo]] — a erosão, em nível de projeto, dessa teoria sob a lente da IA (Storey, 2026)
- [[03 - O comprehension gate|Comprehension gate]] — a prática que defende a teoria mudança a mudança
- [[02-Glosas/2026-cognitive-debt-hidden-risk-ai-driven-software-development|Cognitive debt — Margaret-Anne Storey (DX)]] — a glosa que conecta Naur ao contexto de IA
