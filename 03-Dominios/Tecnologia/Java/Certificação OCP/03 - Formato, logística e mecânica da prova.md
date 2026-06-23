---
title: "Formato, logística e mecânica da prova"
created: 2026-06-13
updated: 2026-06-13
type: concept
status: seedling
publish: true
fase: sobre-a-prova
tags:
  - java
  - certificacao-ocp
  - sobre-a-prova
aliases:
  - "Formato da prova OCP"
  - "Online proctored"
---

# Formato, logística e mecânica da prova

> [!abstract] TL;DR
> A OCP é uma prova de ~50 questões de múltipla escolha (umas pedem 1 resposta, outras pedem "Select two/three"), nota de corte ~68%, em inglês, por USD 245. A **duração** varia entre as fontes secundárias (90 a 120 min) — confirme na página oficial do *seu* exame. As pegadinhas moram em três lugares: multi-answer **sem crédito parcial** (acerte todas, sem extras), enunciados "Select two" fáceis de esquecer, e código Java real onde você decide *o que imprime / se compila / qual exceção lança*. O agendamento hoje aparece como **online proctored via oracle.com/education** (não mais Pearson VUE) — fonte secundária, verifique.

## Formato

| Item | Detalhe |
| --- | --- |
| **Nome oficial** | Java SE 21 Developer Professional (ou Java SE 25 Developer Professional) |
| **Código** | 1Z0-830 (Java 21) / 1Z0-831 (Java 25) |
| **Número de questões** | ~50 |
| **Nota de corte** | ~68% (muda a cada release) |
| **Formato** | Múltipla escolha — single answer + multi-answer ("Select two/three") |
| **Idioma** | Inglês (oficial) |
| **Preço** | USD 245 ("may vary by region") |
| **Duração** | 90–120 min (fontes divergem — confirmar) |

> [!warning] A duração não é confiável de cabeça
> As fontes secundárias **divergem entre 90 e 120 minutos** para o 1Z0-830 / 1Z0-831. O tronco antigo deste codex cravava 90 min — **não confie nele**. Antes de agendar, confirme a duração na **página oficial do seu exame específico** (links na seção **Referências**, abaixo). Esse número define todo o seu pacing na prova, então vale a checagem de dois minutos.

## Características traiçoeiras

A prova não é difícil só pelo conteúdo — ela é desenhada para punir leitura apressada. Os pontos que mais derrubam candidatos:

- **Multi-answer sem crédito parcial** — em questões de múltiplas respostas, você precisa marcar **todas** as corretas e **nenhuma** a mais. Acertar 2 de 3 vale **zero**, igual a errar tudo. Não há meio-termo.
- **"Select two" / "Select three" é fácil de esquecer** — o enunciado avisa quantas respostas marcar, mas no calor da prova é comum marcar só uma e seguir em frente. Leia o comando final de cada questão antes de responder.
- **Código Java real** — boa parte das questões mostra um trecho de código e pergunta *o que ele imprime*, *se compila*, ou *qual exceção lança*. Você precisa "rodar o compilador na cabeça" — incluindo erros de compilação, que muitas vezes são a resposta certa.
- **Marcador de revisão — use!** — dá para marcar uma questão e voltar depois. Use sem dó: na primeira passada, resolva o que é rápido e marque o que trava. Não queime tempo no início.
- **Proibido ajuda externa** — sem calculadora, sem scratch paper digital, sem consulta. O que você sabe na hora é o que vale.

> [!tip] Estratégia de mecânica
> Faça uma primeira passada respondendo só o que você tem certeza, marcando o resto para revisão. Numa segunda passada, ataque os marcados com o tempo restante. Isso evita que uma questão-armadilha no começo coma 10 minutos que faltariam no fim.

## Onde e como fazer

A prova pode ser feita de duas formas, com trade-offs claros:

**Online proctored (em casa):**
- Vantagem: sem deslocamento, faz do seu próprio ambiente, horários mais flexíveis.
- Custo: exige **webcam, microfone e ambiente limpo** — ninguém por perto, mesa livre, sem segundo monitor. Um *proctor* observa via webcam e conversa sobre o ambiente no início.
- Risco: **comportamento suspeito invalida a prova** — não pode falar sozinho, olhar para os lados repetidamente, levantar, ou ter alguém entrando no cômodo.

**Centro físico (presencial):**
- Vantagem: ambiente controlado, sem o estresse de ser vigiado por webcam; máquina e conexão são do centro.
- Custo: deslocamento, e a disponibilidade de horários/datas depende da sua cidade.

A escolha é prática: se você tem um cômodo calmo, webcam decente e disciplina para ficar imóvel, online proctored economiza tempo. Se seu ambiente é imprevisível (família, barulho, internet instável), o centro físico tira esse risco do seu caminho.

> [!info] Mudança de plataforma de agendamento — verificar
> **Fonte secundária — a verificar:** múltiplas fontes indicam que o **1Z0-830 não é mais administrado pela Pearson VUE**. O agendamento teria migrado para **oracle.com/education**, em modalidade **online proctored**. As páginas oficiais da Oracle estavam bloqueadas por JavaScript no momento desta nota, então **confirme o canal de agendamento atual** antes de comprar o voucher.

## Veja também

- [[03-Dominios/Tecnologia/Java/Certificação OCP/02 - Qual prova mirar — Java 21 (1Z0-830) vs Java 25 (1Z0-831)|Qual prova mirar]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/17 - O dia da prova e depois|O dia da prova e depois]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/16 - Estratégia de estudo e recursos|Estratégia de estudo]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- https://education.oracle.com/java-se-21-developer-professional/pexam_1Z0-830
- https://education.oracle.com/java-se-25-developer-professional/pexam_1Z0-831
