---
title: "Cloud — FinOps (a economia da cloud)"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - finops
  - custo
  - economia
aliases:
  - "FinOps — a economia da cloud"
  - "Galho 19 - FinOps"
---

# FinOps — a economia da cloud

> [!abstract] TL;DR
> Galho 19 da trilha Cloud, terceira nota do **Bloco 4 (Operar, sustentar, governar)**. Território exclusivo da Cloud — nenhuma outra trilha do vault cobre o que este galho cobre — e ouro pra entrevista sênior: por que a conta de nuvem explode sem ninguém decidir explicitamente que ela deveria, e como uma disciplina chamada FinOps existe só pra trazer de volta a responsabilidade financeira que o modelo pay-as-you-go apaga. O galho sobe do **problema** (o CapEx que virou OpEx sem controle) para os **modelos de precificação** (on-demand, reserved, savings plans, spot — a mesma vCPU, quatro preços), depois **visibilidade e alocação** (Cost Explorer, budgets, tags, CUR, showback/chargeback — você não otimiza o que não vê), depois **otimização** (right-sizing, tiering, transferência de dados, serverless), depois a **cultura FinOps** (o ciclo inform/optimize/operate, unit economics, os papéis), e fecha com um **capstone** que aplica tudo à arquitetura de referência do Galho 15 — a fatura peça por peça, e como cortá-la sem quebrar nada. 6 notas, 2 fases (Iniciado→Adepto, capstone Magus), lente dupla AWS ↔ DigitalOcean o galho inteiro, porque é justamente aqui que o pricing previsível da DO vira argumento de peso.

## Sobre este galho

FinOps não é uma ferramenta nem um dashboard — é a disciplina que junta engenharia, finanças e negócio em torno de uma pergunta simples e incômoda: *quanto isso custa, e vale a pena?* O modelo pay-as-you-go da cloud prometeu eliminar o CapEx (comprar servidor, esperar meses, torcer pra capacidade certa) e trocou por OpEx elástico — mas elástico pra cima é fácil de esquecer que também é elástico pra baixo, e sem alguém olhando, a fatura só cresce. Este galho ensina a mecânica de controlar essa fatura com a mesma profundidade que os galhos de compute e rede ensinaram a controlar a infraestrutura.

O fio condutor sobe do sintoma ao sistema. Primeiro o *porquê* — por que a conta explodiu, os culpados de sempre (recursos órfãos, superprovisionamento, egress) e os escondidos, FinOps como ponte entre CapEx e OpEx. Depois o *cardápio de preços* — os quatro modelos de compra de compute na AWS (on-demand, reserved instances, savings plans, spot) e a matemática de break-even entre eles. Depois a *visibilidade* — sem ver o gasto por serviço/time/produto (tags, Cost Explorer, budgets, CUR, showback vs. chargeback), nenhuma otimização é possível. Depois a *otimização* propriamente dita — os degraus que vão de eliminar desperdício óbvio a right-sizing, compra mais inteligente, resolver o custo escondido de transferência de dados, e arquitetura consciente de custo. Depois a *cultura* — o ciclo Inform→Optimize→Operate, o modelo de maturidade Crawl/Walk/Run, unit economics, e os papéis de quem faz o quê. E por fim o *capstone* — pegar a arquitetura de referência montada no Galho 15 e aplicar FinOps de ponta a ponta: a fatura ilustrativa peça por peça, a árvore de otimização, e o aviso de que otimizar demais também quebra coisa.

**Audiência primária:** quem sabe que a fatura da AWS assusta mas nunca formalizou por quê, nem separou "problema de arquitetura" de "problema de disciplina financeira". **Audiência secundária:** quem já usa tags e budgets no dia a dia mas nunca ligou os pontos entre pricing model, unit economics e o ciclo FinOps formal — o tipo de lacuna que aparece exatamente numa entrevista sênior sobre trade-offs de arquitetura.

> [!info] Fronteira
> **Modelos de precificação de compute genéricos** (o que é reserved capacity, o que é spot) já apareceram de raspão nos galhos de Compute (5-6); aqui eles são o centro, não a nota de rodapé. **Observabilidade técnica** (métricas, logs, alarms) é o Galho 17 — este galho usa os mesmos dados de billing, mas com a lente de custo, não de saúde do sistema. **Resiliência e continuidade** (Multi-AZ, DR) é o Galho 20 — e a tensão entre "gastar menos" e "sobreviver a uma falha" é deliberada: o capstone deste galho termina exatamente na porta desse próximo. Este galho não ensina a arquitetar — ensina a precificar e a governar o que já foi arquitetado.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/19 - FinOps — a economia da cloud/01 - Por que a conta explodiu|01 — Por que a conta explodiu]] — o problema do custo cloud (recursos órfãos, superprovisionamento, egress escondido), FinOps como disciplina que junta engenharia/finanças/negócio, CapEx→OpEx como mudança de modelo mental, e onde o pricing previsível da DigitalOcean já ganha de largada.

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/19 - FinOps — a economia da cloud/02 - Modelos de precificação|02 — Modelos de precificação]] — a mesma vCPU, quatro preços: on-demand (flexibilidade), Reserved Instances (comprar o futuro previsível), Savings Plans (comprar o compromisso, não o tipo), Spot (comprar a capacidade que sobrou); o mix ótimo, a matemática de break-even, e o ponto de virada do serverless.
3. [[03-Dominios/Tecnologia/Cloud/19 - FinOps — a economia da cloud/03 - Visibilidade e alocação de custo|03 — Visibilidade e alocação de custo]] — você não otimiza o que não vê: Cost Explorer, Budgets (a primeira linha de defesa contra o susto na fatura), cost allocation tags, Cost and Usage Report (o dado bruto), showback vs. chargeback vs. custo unitário, e Cost Anomaly Detection.
4. [[03-Dominios/Tecnologia/Cloud/19 - FinOps — a economia da cloud/04 - Otimização de custo|04 — Otimização de custo]] — os cinco degraus: eliminar desperdício, right-sizing, comprar melhor (RI/Savings/Spot), resolver o custo escondido de transferência de dados, e arquitetura consciente de custo (serverless/managed); onde a AWS tem mais alavancas e onde a DO desperdiça menos por design.
5. [[03-Dominios/Tecnologia/Cloud/19 - FinOps — a economia da cloud/05 - FinOps na prática e cultura|05 — FinOps na prática e cultura]] — o ciclo Inform→Optimize→Operate, o modelo de maturidade Crawl/Walk/Run, unit economics (a métrica que liga custo a valor), custo como requisito não-funcional, governança (do guardrail manual ao automático), e os papéis de quem faz o quê.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/19 - FinOps — a economia da cloud/06 - Otimizar o custo da arquitetura de referência (capstone)|06 — Otimizar o custo da arquitetura de referência (capstone)]] — aplica FinOps de ponta a ponta à arquitetura de referência do Galho 15: a fatura ilustrativa peça por peça, a árvore de otimização (uma alavanca por peça), o aviso de que otimizar demais quebra coisa, e a decisão serverless-vs-sempre-ligado revisitada como decisão de custo; ponte para o Galho 20 (o mesmo orçamento, puxado agora pela resiliência). Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — o problema, o cardápio de preços, a visibilidade, a otimização, a cultura, e a aplicação prática no fim.

### Já pago a fatura, quero entender e cortar rápido

02 (o mix de preços que realmente move a agulha) → 04 (os degraus de otimização, na ordem de esforço/retorno) → 06 (o exemplo trabalhado, peça por peça).

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework/index|Well-Architected Framework]] — Galho 3, o pilar de Otimização de Custo que este galho aprofunda até o fim
- [[03-Dominios/Tecnologia/Cloud/15 - Arquiteturas serverless e event-driven/index|Arquiteturas serverless e event-driven]] — Galho 15, a arquitetura de referência que o capstone deste galho precifica e otimiza
