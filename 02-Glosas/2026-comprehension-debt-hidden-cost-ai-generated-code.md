---
title: "Comprehension Debt - the hidden cost of AI generated code."
aliases: ["Comprehension Debt - the hidden cost of AI generated code."]
source: https://addyosmani.com/blog/comprehension-debt/
author: Addy Osmani
site: AddyOsmani.com
published: 2026-03-14
read: 2026-05-08
created: 2026-05-08
updated: 2026-05-08
type: glosa
status: lido
progresso: andamento
promovida_em: []
tags: [comprehension-debt, ai-generated-code, code-review, software-engineering]
lang: en
publish: false
---

# Comprehension Debt - the hidden cost of AI generated code. — Addy Osmani

## TL;DR

Addy Osmani define dívida de compreensão como a distância crescente entre o volume de código existente e o quanto dele alguém realmente entende. O texto argumenta que IA torna código barato de gerar, mas não torna entendimento barato de pular; quando revisão, testes e specs são tratados como substitutos da compreensão humana, o sistema acumula risco invisível.

## Pontos-chave

- Dívida de compreensão é apresentada como um custo oculto da dependência excessiva de IA e automação: o código parece limpo, os testes passam, mas a teoria humana do sistema se perde.
- O problema central é uma assimetria de velocidade: IA gera código mais rápido do que humanos conseguem avaliar, transformando revisão de qualidade em gargalo de throughput.
- Código gerado por IA tende a vir sintaticamente correto, bem formatado e superficialmente plausível, justamente os sinais que historicamente aumentavam confiança em revisão.
- Testes, linters e análise estática ajudam, mas têm teto: não cobrem comportamentos que ninguém pensou em especificar nem respondem se mudanças massivas de teste preservam intenção.
- Specs detalhadas também não resolvem sozinhas, porque a tradução de uma especificação para código envolve muitas decisões implícitas sobre edge cases, dados, erros, performance e interação.
- A habilidade escassa passa a ser a de manter contexto profundo do sistema: saber quais comportamentos são críticos, por que decisões antigas foram tomadas e quando um refactor altera algo que usuários dependem.
- Métricas tradicionais como velocity, DORA, contagem de PRs e cobertura não capturam déficit de compreensão, criando incentivos para otimizar produção visível enquanto o entendimento real se deteriora.

## Citações

> "Comprehension debt is the growing gap between how much code exists in your system and how much of it any human being genuinely understands."

> "Surface correctness is not systemic correctness."

> "Tests are necessary. They are not sufficient."

> "The comprehension work is the job."

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
