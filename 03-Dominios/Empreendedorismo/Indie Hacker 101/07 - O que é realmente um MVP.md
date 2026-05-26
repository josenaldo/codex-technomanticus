---
title: "O que é realmente um MVP"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - indie-hacker
  - empreendedorismo
  - produto
  - mvp
  - scope
aliases:
  - MVP
  - Minimum Viable Product
  - Produto mínimo viável
---

# O que é realmente um MVP

> [!abstract] TL;DR
> MVP não é "versão incompleta do produto final" — é "menor experimento que valida a hipótese de que alguém paga para resolver este problema". A diferença é categórica: a versão incompleta pressupõe que o produto final é correto e só falta construir mais; o experimento pressupõe que você não sabe se está certo e precisa descobrir gastando o mínimo possível. Scope creep é o assassino #1 de projetos indie hacker — não concorrência, não falta de ideia, não falta de skills. A cura é definir o MVP como uma feature, não como um produto, e usar Shape Up para manter o escopo controlado.

## O que é

Eric Ries definiu MVP em *The Lean Startup* como "a versão de um novo produto que permite a um time coletar a quantidade máxima de aprendizado validado sobre clientes com o menor esforço". A palavra-chave não é "produto" — é **"aprendizado"**.

O MVP não é para impressionar. Não é para ter feature parity com concorrentes. Não é para mostrar no portfolio. É para responder uma pergunta específica: **"Alguém paga para resolver este problema, desta forma?"**

Se a resposta for sim, construa mais. Se for não, pivote. Se for "talvez", refine o experimento. Em qualquer caso, o MVP cumpriu seu papel em semanas, não meses.

## Por que importa

O ciclo mortal do indie hacker é:

```
Ideia → "Vou construir completo" → 6 meses de build → Lançamento → Ninguém usa → Desistência
```

O ciclo saudável é:

```
Ideia → Validação (Mom Test) → MVP (2-4 semanas) → Feedback real → Iterar ou pivotar
```

A diferença de tempo entre os dois ciclos é a diferença entre persistir e desistir. Quem constrói 6 meses sem feedback esgota motivação, energia e paciência antes de ter dados reais.

### Scope creep: o assassino #1

Scope creep não parece perigoso porque cada feature individual parece "pequena" e "necessária". Mas a soma de 30 features "pequenas e necessárias" é um produto que leva 1 ano para ficar pronto — e que resolve 30 problemas de forma medíocre em vez de 1 problema de forma excepcional.

O conceito de **one-feature product** é o antídoto: se você tivesse que escolher UMA feature para cobrar, qual seria? Essa é o MVP.

## Como funciona

### O framework "Um verbo, um substantivo"

O MVP pode ser descrito como: **"[Persona] consegue [verbo] [substantivo] usando o produto."**

Exemplos:
- "Dev autodidata consegue **revisar flashcards** usando o CLI" ← isso é um MVP
- "Dev autodidata consegue criar, organizar, revisar, compartilhar e exportar flashcards com IA, integração com Obsidian, analytics e marketplace" ← isso é um produto de 2 anos

### Critério de "done" para o MVP

O MVP está pronto quando:

1. **Uma pessoa real** (não você, não seu amigo) **consegue usar** para resolver o problema core
2. **Sem ajuda sua** (sem pair programming, sem Zoom explicando)
3. **E está disposta a pagar** (ou dar feedback detalhado como substituto temporário)

Se 3 de 5 testadores conseguem completar o fluxo core sem ajuda e dizem "sim, eu pagaria por isso" — o MVP validou a hipótese. Se 4 de 5 travam no onboarding, o aprendizado é: "o problema é real mas o UX precisa de trabalho". Em ambos os casos, o MVP cumpriu seu papel.

### MVP de validação vs MVP de produto

| Tipo | O que é | Quando usar |
|------|---------|-------------|
| **MVP de validação** | Landing page, Wizard of Oz, serviço manual | Antes de escrever código — testar demand |
| **MVP de produto** | Software real, mínimo, funcional | Após validar demand — testar solução |

Para indie hackers com skills de dev, a tentação é pular direto para MVP de produto. Resista se possível: [[06 - Landing page de validação e sinais de demanda|landing page]] e [[04 - The Mom Test — entrevistas que não mentem|entrevistas]] são MVPs de validação que custam horas, não semanas.

### Quanto tempo para um MVP?

Benchmark saudável para indie hacker solo:

| Complexidade | Timeline | Exemplo |
|-------------|----------|---------|
| CLI tool simples | 1-2 semanas | Parser de markdown + FSRS |
| Web app simples | 2-4 semanas | CRUD + auth + 1 feature core |
| Plugin/extensão | 2-3 semanas | Obsidian plugin com 1 view |

**Regra: se leva mais de 4 semanas, corte escopo.** Se depois de cortar ainda leva mais de 4 semanas, corte de novo. O MVP não precisa ser bonito, não precisa ter onboarding polido, não precisa ter dark mode.

## Na prática

Exemplos de MVPs que funcionaram como experimentos mínimos:

- **Dropbox**: antes de construir o produto, Drew Houston fez um vídeo de 3 minutos mostrando como funcionaria. O vídeo viralizou no Hacker News e gerou 75.000 signups overnight. O produto nem existia.
- **Buffer**: Joel Gascoigne criou uma landing page de 2 telas. Tela 1: proposta de valor. Tela 2: pricing (para testar willingness-to-pay). Tela 3: "na verdade, ainda não está pronto — deixe seu email". Os cliques no pricing validaram a hipótese.
- **Basecamp**: começou como ferramenta interna da 37signals para gerenciar projetos de clientes de web design. O "MVP" era a ferramenta que eles mesmos precisavam.

## Armadilhas

- **"Preciso de feature parity com [concorrente]."** Não precisa. O concorrente tem 5 anos e 50 devs. Seu diferencial não é ter mais features — é resolver um sub-problema melhor para um sub-grupo.

- **"Não posso lançar sem [auth/dark mode/i18n/mobile]."** Pode. O primeiro usuário real não se importa com dark mode. Se importa com resolver o problema. O resto vem depois.

- **"Vou lançar quando estiver pronto."** Nunca está pronto. O dia certo de lançar é quando dá vergonha do quão simples é — porque se não dá vergonha, demorou demais.

- **Confundir feedback de features com validação.** "Seria legal ter X" ≠ "eu pago por X". O Mom Test vale aqui também.

- **Gold-plating.** Polir a UI por semanas quando ninguém testou o fluxo core é otimizar o que não importa. Funcionalidade > estética no MVP.

## Veja também

- [[04 - The Mom Test — entrevistas que não mentem]] — validação antes do MVP
- [[06 - Landing page de validação e sinais de demanda]] — MVP de validação
- [[08 - Shape Up para solo founders]] — como manter escopo controlado
- [[09 - Stack de custo zero]] — infraestrutura para o MVP

## Referências

- **Ries, Eric** — *The Lean Startup*. Definição original de MVP e ciclo Build-Measure-Learn.
- **Kahl, Arvid** — *Zero to Sold*. Estágio "Survival": construir o mínimo para sobreviver.
- **Fried, Jason & DHH** — *Rework*. "Launch now" — lançar cedo como disciplina.
- **Basecamp** — *Shape Up*. Appetite e fixed time/variable scope como antídoto para scope creep.
