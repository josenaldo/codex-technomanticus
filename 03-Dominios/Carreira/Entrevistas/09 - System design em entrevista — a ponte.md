---
title: "System design em entrevista — a ponte"
created: 2026-07-31
updated: 2026-07-31
type: concept
status: seedling
fase: Adepto
tags:
  - carreira
  - entrevistas
  - system-design
publish: true
aliases:
  - System design em entrevista
  - A etapa de system design
---

# System design em entrevista — a ponte

> [!abstract] TL;DR
> Esta nota é **deliberadamente curta**. A entrevista de system design tem trilha inteira neste vault — framework de cinco notas, blocos de construção, padrões recorrentes, oito walkthroughs e um capstone sobre conduzir a conversa. Aqui fica só o que pertence a **este** galho: onde a etapa se encaixa no funil, o que ela mede num sênior (que não é conhecimento de componentes, e sim **julgamento sob ambiguidade**) e o comportamento que a reprova com mais frequência — projetar para uma escala que ninguém pediu. Para estudar a etapa, o caminho é a trilha.

> [!info] Onde estudar de verdade
> **[[03-Dominios/Engenharia/Arquitetura/System Design/index|System Design]]** — a trilha completa: [[03-Dominios/Engenharia/Arquitetura/System Design/1 - Framework de entrevista/index|framework de entrevista]] (clarificar requisitos, estimativas, API e modelo de dados, do macro ao deep dive), [[03-Dominios/Engenharia/Arquitetura/System Design/2 - Building blocks/index|building blocks]], [[03-Dominios/Engenharia/Arquitetura/System Design/3 - Padrões recorrentes/index|padrões recorrentes]], [[03-Dominios/Engenharia/Arquitetura/System Design/4 - Walkthroughs/index|walkthroughs]] e o capstone [[03-Dominios/Engenharia/Arquitetura/System Design/Conduzindo a entrevista completa|Conduzindo a entrevista completa]].

## Por que esta nota existe

Um galho sobre entrevista sênior que não mencionasse system design teria um buraco visível — é a etapa de maior peso em boa parte dos processos. Mas duplicar aqui o que já existe em vinte e sete notas seria pior: produziria uma versão rasa competindo com a completa, e quem consultasse o galho errado sairia pior informado.

Então a solução é esta: **situar a etapa no funil e apontar o caminho.**

## Onde a etapa se encaixa

No funil descrito em [[02 - A anatomia do funil internacional]], system design costuma ser a quarta etapa — depois do deep dive técnico, antes da cultural. Duas particularidades a distinguem das demais:

**É a etapa com maior variância de formato.** Pode ser um problema aberto de produto ("projete um encurtador de URL"), o desenho de algo próximo do que a empresa realmente opera, ou uma discussão sobre um sistema que **você** construiu — essa última cada vez mais comum em processos sênior, e frequentemente misturada ao deep dive.

**É a que mais depende de você conduzir.** Nas outras, o entrevistador guia. Aqui o enunciado costuma ser uma frase, e o silêncio seguinte é parte do teste: espera-se que você estruture a conversa, faça as perguntas e proponha a ordem. Quem espera ser guiado já perdeu metade do sinal.

## O que isto está medindo

Não é conhecimento de componentes. Saber o que é um cache distribuído, uma fila ou um índice é pré-requisito — todos os finalistas sabem. O que se mede:

| Sinal | Como aparece |
| --- | --- |
| **Julgamento sob ambiguidade** | você pergunta a escala **antes** de desenhar |
| **Priorização** | ataca o gargalo real, não o componente favorito |
| **Trade-off explícito** | diz o que cada escolha custa, sem ser cobrado |
| **Simplicidade** | propõe o **mínimo** que resolve, e sabe quando parar |
| **Comunicação** | conduz a conversa e checa alinhamento no caminho |

O último item é o que mais surpreende quem se prepara sozinho: a etapa é uma **conversa**, não uma apresentação. Desenhar em silêncio e apresentar o resultado no fim entrega menos sinal do que ir verificando ("faz sentido eu aprofundar a parte de escrita primeiro?").

> [!question]- Se eu não souber projetar o sistema que ele pediu?
> Isso é esperado, e não é o fim da avaliação — ninguém projeta um sistema desconhecido em quarenta e cinco minutos. O que se avalia é **como você atravessa o desconhecido**: enunciar premissas em voz alta, dividir em partes tratáveis, dizer o que você **não** sabe e como descobriria, e escolher por critério em vez de por familiaridade. Admitir "nunca operei nessa escala; minha premissa é X, e se ela estiver errada a decisão muda para Y" costuma pontuar melhor que fingir domínio — porque é exatamente o comportamento desejável num sistema real com requisito incerto.

## O erro que mais reprova

**Projetar para uma escala que ninguém pediu.** É o erro característico do candidato sênior — e é o mesmo caso da abertura da [[01 - O que uma entrevista sênior avalia|nota 01]] deste galho: chegar direto com particionamento, cache distribuído e mensageria, para um problema cuja escala nunca foi perguntada.

O que o entrevistador registra não é "sabe muito", é **"não pergunta antes de decidir"** — projeção direta de como a pessoa vai gastar dinheiro e complexidade no time dele. A correção é barata: começar perguntando volume, crescimento e requisitos de consistência, e só então dimensionar. Sistema simples que atende o que foi pedido, com um caminho de evolução declarado, avalia melhor que arquitetura elaborada para um problema imaginado.

## O que vem a seguir

A última nota do bloco fecha o ciclo dos formatos: todos eles — comportamental, técnico, system design — consomem o mesmo insumo, que é o seu repertório de experiências. Falta o método de construí-lo.

- [[10 - O banco de histórias]] — como montar e indexar o repertório; fecha o bloco Adepto.
- [[03-Dominios/Engenharia/Arquitetura/System Design/index|System Design]] — a trilha completa desta etapa.
- [[11 - Comunicar trade-offs sob pressão]] — a habilidade que esta etapa mais cobra.

## Veja também

- [[08 - A entrevista técnica - os três formatos]] — as outras etapas técnicas do funil.
- [[02 - A anatomia do funil internacional]] — onde esta etapa se encaixa.

## Fontes

- A trilha [[03-Dominios/Engenharia/Arquitetura/System Design/index|System Design]] deste vault — as fontes primárias estão lá, nota a nota.
- **Alex Xu** — *System Design Interview* — a referência de formato para a etapa.
