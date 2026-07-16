---
title: Precificação — retainer, hourly e project-based
created: 2026-07-08
updated: 2026-07-08
type: concept
status: seedling
publish: true
tags:
  - fractional
  - empreendedorismo
  - carreira
aliases:
  - Precificação fractional
  - Quanto cobrar fractional
progress: done
---

> [!abstract] TL;DR
> Retainers de fractional CTO variam de $3.000 a $15.000/mês para engajamentos de 10-20h/semana, e hourly rates ficam entre $150 e $500/hora (média $200-350). Retainer costuma embutir um desconto de 10-20% sobre o equivalente por hora, porque o cliente ganha disponibilidade garantida e você ganha receita previsível. Pra calcular seu próprio preço: defina a renda anual-alvo, divida por horas faturáveis realistas (1.000-1.200/ano, não 2.000), ajuste pra cima 25-35% pra cobrir impostos e benefícios que um CLT teria embutidos, e aplique um prêmio de 20-30% se seu nicho for especializado (IA/ML, saúde, fintech, segurança).

## O problema de precificar sem referência

Um engenheiro sênior sai do primeiro processo de venda fractional e o cliente pergunta "quanto você cobra?". Sem número de referência, ele improvisa um valor baseado no que ganhava de salário mensal dividido por 4 — e ancora um preço baixo demais, que vai persegui-lo nas próximas negociações (o próximo cliente, ou até o mesmo cliente numa renovação, tende a usar esse número como ponto de partida). O erro raiz não é falta de confiança — é falta de um método pra calcular o número antes da conversa acontecer.

## Como funciona o mecanismo dos três modelos de preço

> [!question]- Por que existem três formatos de cobrança em vez de um só?
> Porque cada formato transfere o risco de um jeito diferente entre você e o cliente. Hourly transfere o risco de "quanto tempo vai levar" pro cliente (ele paga pelo que for usado, sem teto claro). Retainer transfere o risco pro fractional (você promete disponibilidade fixa por um valor fixo, independente de quanto trabalho realmente aparece naquele mês). Project-based fixa o preço pro escopo inteiro, então o risco de estimar mal o esforço é seu.

| Modelo | Como funciona | Quem assume o risco | Quando faz sentido |
|--------|----------------|----------------------|----------------------|
| **Hourly** | $150-500/hora, faturado pelo tempo efetivamente trabalhado | Cliente (paga o que usar) | Engajamentos esporádicos, escopo imprevisível, fase de teste antes de fechar retainer |
| **Retainer mensal** | Valor fixo por um número de horas/dias garantido por semana | Fractional (compromete disponibilidade fixa) | Engajamentos recorrentes advisory ou hands-on — o formato padrão do modelo fractional |
| **Project-based** | Valor fechado pra um entregável com prazo definido | Fractional (estimou o esforço errado, absorve a diferença) | Devido diligence, migração pontual, auditoria — trabalho com início e fim claros |

### Faixas de mercado (referência internacional, 2026)

- **Hourly:** $150-500/hora; a maioria dos fractional CTOs experientes cobra $200-350/hora. Localização importa — cidades como San Francisco/NY cobram $275-350, mercados secundários $200-275.
- **Retainer mensal:** $3.000-15.000/mês para 10-20h/semana. Uma referência comum: 10h/semana ≈ $5.000-10.000/mês; 20h/semana (quase embedded) ≈ $10.000-15.000/mês.
- **Retainer costuma dar desconto de 10-20%** sobre o hourly equivalente — o cliente paga menos por hora em troca de garantir a disponibilidade, e o fractional aceita porque ganha previsibilidade de caixa.

> [!info] Câmbio e mercado brasileiro
> Essas faixas são de mercado internacional (principalmente EUA), o público mais comum de quem atua fractional a partir do Brasil. Um fractional brasileiro competitivo costuma precificar abaixo do topo americano, mas isso não deveria significar precificar como freelancer júnior — ver a armadilha de "desconto geográfico" abaixo. A parte de como estruturar o recebimento em dólar e a tributação correspondente fica em [[11 - Faturando em dólar — nota fiscal e isenções]] e [[12 - Organização financeira e câmbio]].

## Como calcular seu próprio número

> [!question]- Por onde começo, sem já ter clientes de referência?
> Trabalhe de trás pra frente a partir da renda que você precisa, não do que "parece razoável cobrar":
>
> 1. **Defina a renda anual-alvo** — o que você precisaria faturar (não lucrar; faturar) pra sustentar seu padrão de vida e reinvestir no negócio.
> 2. **Divida por horas faturáveis realistas** — 1.000 a 1.200 horas por ano, não 2.000. Um ano fractional tem tempo não-faturável: prospecção, administração, férias, período entre clientes.
> 3. **Ajuste pra cima 25-35%** pra cobrir o que um CLT teria embutido (impostos, benefícios, reserva) e que agora é custo seu — ver [[10 - Abrindo e mantendo o CNPJ certo]] pra entender a carga tributária PJ que entra nessa conta.
> 4. **Aplique um prêmio de 20-30%** se seu nicho for especializado (IA/ML, saúde/HIPAA, fintech/PCI, segurança) — especialistas nessas áreas cobram consistentemente acima da média, porque o risco de errar é maior pro cliente.

O resultado é seu valor-hora de referência. A partir dele, um retainer de N horas/semana é `valor-hora × horas/semana × 4,3 semanas × (1 - desconto de 10-20%)`.

**Em uma frase:** calcule de trás pra frente a partir da renda-alvo e das horas realmente faturáveis, não do que parece "razoável" cobrar sem referência.

## Casos práticos

### Cenário 1: primeiro retainer, sem histórico de preço

Um engenheiro que ganhava R$25.000/mês como Head of Engineering CLT decide virar fractional. Ele calcula: quer manter uma renda equivalente a R$35.000/mês (compensando a perda de benefícios e a irregularidade), o que dá R$420.000/ano. Com 1.100 horas faturáveis/ano, o valor-hora de referência fica em ~R$380 (~$70-75, considerando câmbio) — mas ele opera em dólar com clientes internacionais, então recalcula usando faixas de mercado americano ($200-350/hora), aplicando um desconto consciente (não um desconto involuntário por insegurança) até ganhar mais cases. Ele fecha o primeiro contrato em $180/hora, deixando claro (pra si mesmo) que é uma tarifa de entrada, não o teto.

### Cenário 2: renegociando de hourly pra retainer

Um fractional vinha cobrando $200/hora de um cliente, faturando em média 35 horas/mês — cerca de $7.000/mês, variável. Depois de 4 meses de relação estável, ele propõe migrar pra retainer: 40h/mês garantidas por $7.200/mês (um desconto de ~10% sobre o equivalente hourly). O cliente ganha previsibilidade de orçamento; ele ganha previsibilidade de receita e libera tempo mental que gastava calculando quantas horas cobrar a cada mês.

## Armadilhas comuns

> [!warning] Ancorar preço baixo na primeira negociação
> **O que acontece:** sob pressão de fechar o primeiro cliente, o profissional aceita um valor abaixo do calculado, achando que "depois eu subo".
> **Por quê:** o primeiro preço vira referência — tanto pro próprio cliente em renovações quanto psicologicamente pro profissional, que passa a ancorar negociações futuras nesse número.
> **Como evitar:** calcular o número antes da conversa (ver método acima) e tratá-lo como piso, não como ponto de partida pra negociação pra baixo.

> [!warning] "Desconto geográfico" automático por estar no Brasil
> **O que acontece:** o profissional assume que, por morar no Brasil, deveria cobrar significativamente menos que o mercado americano, independente da qualidade da entrega.
> **Por quê:** o cliente internacional está pagando pelo resultado técnico, não pelo custo de vida do fractional — um fractional brasileiro competente entrega o mesmo valor que um americano equivalente. Descontar demais deixa dinheiro na mesa sem necessidade.
> **Como evitar:** precificar pelo valor entregue e pela faixa de mercado do cliente, com um desconto moderado e consciente (não automático) enquanto o portfolio ainda está em construção — ver [[08 - Se diferenciando como fractional brasileiro]] pra como transformar isso em vantagem competitiva em vez de justificativa pra cobrar pouco.

> [!warning] Não reajustar o retainer com o tempo
> **O que acontece:** o mesmo retainer segue igual por anos, mesmo com o custo de vida, a experiência acumulada e a demanda pelo profissional crescendo.
> **Por quê:** clientes raramente oferecem reajuste espontâneo — cabe ao fractional revisitar o valor periodicamente, especialmente em renovação de contrato.
> **Como evitar:** definir de antemão uma cadência de revisão (ex: anual, ou a cada renovação de 6 meses) e comunicar isso já no contrato inicial (ver [[13 - Anatomia de um contrato internacional de serviço]]).

## Como explicar em inglês

Fractional CTO retainers typically run $3,000 to $15,000 a month for 10-20 hours a week, and hourly rates fall between $150 and $500, averaging $200-350. A retainer usually bakes in a 10-20% discount versus the hourly equivalent — the client gets guaranteed availability, and I get predictable income.

| PT | EN |
|----|----|
| Precificação | Pricing |
| Retainer mensal | Monthly retainer |
| Tarifa por hora | Hourly rate |
| Baseado em projeto | Project-based |
| Prêmio de especialização | Specialization premium |
| Horas faturáveis | Billable hours |

## Veja também

- [[03-Dominios/Carreira/Empreendedorismo/Indie Hacker 101/11 - Pricing para SaaS bootstrapped|Pricing para SaaS bootstrapped]] — a mesma lógica de precificar por valor entregue, aplicada a produto em vez de serviço

## O que vem a seguir

Preço definido, mas ninguém contrata só pelo número — o cliente precisa de evidência de que você entrega o que promete. A próxima nota cobre como construir essa evidência antes mesmo do primeiro cliente fractional.

- [[06 - Prova social e portfolio fractional]] — como construir credibilidade verificável
- [[09 - Do discovery call ao contrato assinado]] — onde esse preço entra na conversa de venda

## Fontes

- **FractionalCTOExperts** — [Fractional CTO Cost & Rates 2026: Complete Pricing Guide](https://fractionalctoexperts.com/blog/fractional-cto-rates) — faixas de hourly e retainer por região e carga horária
- **Connectd** — [How to Set Your Fractional Executive Rate: A Pricing Guide](https://www.connectd.com/us/article/fractional-executive-rates-us) — método de cálculo de trás pra frente (renda-alvo → horas faturáveis → ajustes)
- **TLVTech** — [Understanding Fractional CTO Rates](https://www.tlvtech.io/post/understanding-fractional-cto-rates-a-guide-for-entrepreneurs-and-business-leaders) — prêmio de especialização por nicho técnico
