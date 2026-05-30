---
title: "Cognitive debt: The hidden risk in AI-driven software development"
aliases: ["Cognitive debt: The hidden risk in AI-driven software development"]
source: https://newsletter.getdx.com/p/cognitive-debt-the-hidden-risk-in
author: Margaret-Anne Storey
site: Engineering Enablement
published: 2026-04-22
read: 2026-05-25
type: glosa
progress: backlog
status: lido
tags: [cognitive-debt, technical-debt, ai-development, shared-understanding, developer-productivity]
lang: en
publish: false
---

# Cognitive debt: The hidden risk in AI-driven software development — Margaret-Anne Storey

## TL;DR

IA generativa e agêntica deslocam o maior risco do desenvolvimento de software da dívida técnica (que vive no código) para a *dívida cognitiva* (que vive na mente das pessoas): a erosão do entendimento compartilhado sobre o que o programa faz, por que as decisões foram tomadas e como mudá-lo. Storey argumenta que velocidade sem entendimento é insustentável e propõe práticas para preservar a "teoria" do sistema distribuída entre as pessoas, docs, testes e agentes.

## Pontos-chave

- Dívida técnica vive no código; dívida cognitiva vive na mente dos desenvolvedores — é a erosão do entendimento compartilhado ao longo do tempo. Diferente da carga cognitiva (momentânea), a dívida cognitiva é uma propriedade de nível de projeto.
- Apoiada em Peter Naur, "um programa é uma teoria" distribuída na mente de muitos devs: o que o programa faz, como as intenções foram implementadas e como mudá-lo. Código limpo gerado por IA não impede que os humanos "percam o fio da meada".
- Adicionar mais agentes pode aumentar overhead de coordenação, decisões invisíveis e carga cognitiva (eco do *Mythical Man-Month*, de Brooks); a pressa de ir rápido a todo custo tensiona os limites de memória e capacidade humana.
- Sinais de alerta: hesitação em mudar por medo de quebrar algo, dependência crescente de "conhecimento tribal" de uma ou duas pessoas, sistema virando caixa-preta, onboarding lento, fadiga e estresse.
- Mitigação concreta: exigir que ao menos um humano entenda cada mudança gerada por IA antes do merge, documentar o *porquê* (não só o *quê*) e criar checkpoints regulares de reconstrução de entendimento (code reviews, retrospectivas, knowledge-sharing).
- Práticas como pair programming, refactoring e TDD — e o "make the hard change easy" de Kent Beck — ajudam a reconstruir o entendimento compartilhado; specs e documentos só servem se forem artefatos vivos com os quais o time engaja ativamente.
- IA baixa o custo de produzir estrutura, fazendo-a evoluir mais rápido do que o entendimento consegue estabilizar; conforme a IA reduz o atrito técnico, o entendimento compartilhado pode se tornar o gargalo da performance.

## Citações

> "Even if AI agents produce code that could be easy to understand, the humans involved may have simply lost the plot and may not understand what the program is supposed to do, how their intentions were implemented, or how to possibly change it."

> "Where cognitive load is what developers experience in the moment, cognitive debt is a project-level property, capturing how a team loses understanding over time."

> "Peter Naur reminded us some decades ago that a program is more than its source code. Rather a program is a theory that lives in the minds of the developer(s) capturing what the program does, how developer intentions are implemented, and how the program can be changed over time."

> "First, they may need to recognize that velocity without understanding is not sustainable."

> "As AI reduces technical friction, shared understanding may become the bottleneck on performance."

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
