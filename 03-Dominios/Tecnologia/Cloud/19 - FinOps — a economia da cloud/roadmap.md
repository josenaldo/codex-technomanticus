---
title: "Roadmap — FinOps (a economia da cloud)"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — FinOps — a economia da cloud (galho 19)

Roadmap-folha do galho `Cloud/19 - FinOps — a economia da cloud`. Bloco 4 (Operar, sustentar, governar) — território exclusivo da Cloud, ouro pra entrevista sênior. Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 6 |
| ⬜ pendente | 0 |
| ✅ feita | 6 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |
| M1 (mídia) | pendente — enriquecimento futuro |

---

## Notas

#### 01 - Por que a conta explodiu
- **Estado:** ✅ feita · fase: Iniciado · 134 linhas
- **Escopo:** a fatura que não devia existir, os culpados de sempre (recursos órfãos, superprovisionamento) e os escondidos (egress, NAT Gateway, IP elástico não associado), FinOps como disciplina que traz responsabilidade financeira pra nuvem, CapEx→OpEx como mudança de modelo mental, a lente dupla invertida (onde a DigitalOcean ganha por pricing previsível), o mapa do galho, armadilhas.

#### 02 - Modelos de precificação
- **Estado:** ✅ feita · fase: Adepto · 212 linhas
- **Escopo:** o problema (a mesma vCPU, quatro preços), os quatro modelos de compra de compute na AWS (On-Demand/flexibilidade, Reserved Instances/futuro previsível, Savings Plans/compromisso não-tipo, Spot/capacidade sobrando), o mix ótimo e a matemática de break-even, caso prático de uma equipe fictícia montando o mix, outras dimensões de custo além de compute, o ponto de virada do serverless, lente DigitalOcean (simplicidade vs. otimização), tabela de tradução Azure/GCP.

#### 03 - Visibilidade e alocação de custo
- **Estado:** ✅ feita · fase: Adepto · 281 linhas · com código (boto3/Athena)
- **Escopo:** a fatura chegou e ninguém sabe explicar, AWS Cost Explorer (painel visual), AWS Budgets (primeira linha de defesa), cost allocation tags (quem gastou o quê), Cost and Usage Report/CUR (o dado bruto), showback vs. chargeback vs. custo unitário, Cost Anomaly Detection (o vigia estatístico), exemplo de consulta ao CUR via Athena, lente DigitalOcean (simples porque precisa ser menos), tabela de tradução Azure/GCP, código instrumentando visibilidade na AWS.

#### 04 - Otimização de custo
- **Estado:** ✅ feita · fase: Adepto · 237 linhas · com código (right-sizing, VPC endpoint, scheduler)
- **Escopo:** você já sabe quanto gasta, e agora — os cinco degraus (1. eliminar desperdício, 2. right-sizing, 3. comprar melhor, 4. data transfer como custo escondido, com exemplo de Gateway VPC Endpoint pra S3, 5. serverless/managed/arquitetura consciente de custo), lente dupla (AWS tem mais alavancas, DO desperdiça menos por design), armadilhas, script de exemplo de scheduler de shutdown por tag.

#### 05 - FinOps na prática e cultura
- **Estado:** ✅ feita · fase: Adepto · 252 linhas
- **Escopo:** o dia em que a conta virou problema de todo mundo, o ciclo FinOps Inform→Optimize→Operate, modelo de maturidade Crawl/Walk/Run, unit economics (a métrica que liga custo a valor), custo como requisito não-funcional, caso prático de um time aplicando o ciclo pela primeira vez, governança (da intenção ao guardrail automático, com exemplo de budget action), tradução de nomes entre provedores, os papéis (quem faz o quê), armadilhas comuns.

#### 06 - Otimizar o custo da arquitetura de referência (capstone)
- **Estado:** ✅ feita · fase: Magus · 180 linhas · **FECHA o galho**
- **Escopo:** o diagrama está pronto, a fatura não veio junto — a fatura ilustrativa da arquitetura de referência (Galho 15) peça por peça, a árvore de otimização (uma alavanca por peça), o trade-off de otimizar demais e quebrar coisa, a decisão serverless-vs-sempre-ligado revisitada como decisão de custo, anti-padrões de custo na arquitetura, lente dupla (a mesma arquitetura, dois modelos de fatura); ponte explícita pro Galho 20 (Multi-region pode dobrar a fatura — FinOps e resiliência puxam o mesmo orçamento em direções opostas). Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Galho de 6 notas, Bloco 4, marcado na spec como "território exclusivo da Cloud; ouro pra sênior" — sem paralelo direto em Engenharia/Operação, ao contrário da maioria dos galhos anteriores da trilha.
- Lente dupla AWS↔DigitalOcean presente nas 6 notas, não só nas de mecânica — inclusive no capstone, que compara os dois modelos de fatura para a mesma arquitetura.
- Fronteiras assumidas neste roadmap: pilar de custo do Well-Architected (Galho 3) é a semente que este galho aprofunda até o fim; observabilidade técnica (Galho 17) e resiliência/DR (Galho 20) ficam fora — a ponte para o Galho 20 é explícita no fecho do capstone (mesmo orçamento, tensão custo vs. sobrevivência a falha).
- 0 wikilinks quebrados verificados: `index.md` e `roadmap.md` linkam apenas para arquivos confirmados via `ls` (Cloud/index, Galho 3/index, Galho 15/index, e as 6 notas do próprio galho).
