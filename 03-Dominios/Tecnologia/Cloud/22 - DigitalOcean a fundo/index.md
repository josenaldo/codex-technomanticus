---
title: "Cloud — DigitalOcean a fundo"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - digitalocean
  - do
aliases:
  - "DigitalOcean a fundo"
  - "Galho 22 - DigitalOcean a fundo"
---

# DigitalOcean a fundo

> [!abstract] TL;DR
> Galho 22 da trilha Cloud, e o segundo galho do **Bloco 5 (Provedores e maestria)** — depois de mapear a AWS a fundo no galho 21, este galho vira a lente para o polo oposto do espectro. O DigitalOcean é a antítese filosófica da AWS: em vez de ~240 serviços, um catálogo curado de algumas dezenas; em vez do paradoxo da escolha, uma opinião já tomada por você. O galho sobe da tese ao veredito: primeiro o **porquê** dessa curadoria deliberada (filosofia de produto, DX como diferencial), depois o **o quê** (o catálogo enxuto, serviço por serviço, contra o equivalente AWS), depois a **lente onde o DO ganha** (pricing previsível e legível), depois a **espinha operacional** (App Platform, o PaaS git-push-to-deploy que carrega a proposta), e fecha com o **framework de decisão sênior**: os sinais objetivos de que o DO basta, e os gatilhos de quando o projeto cresce pra AWS. 6 notas, 3 fases, lente dupla DO ↔ AWS o galho inteiro.

## Sobre este galho

Pra uma faixa enorme de projetos — SaaS pequeno/médio, side-projects, times sem plataforma dedicada — a simplicidade e o pricing previsível do DigitalOcean não são limitação: são vantagem. O valor sênior não está em saber operar o DO (isso qualquer tutorial ensina); está em saber **exatamente quando** ele basta e **exatamente quando** o projeto precisa somar ou migrar pra AWS. Este galho constrói esse julgamento com a mesma honestidade adversarial do galho 21: nem vende o DO como bala de prata, nem o trata como brinquedo de side-project.

O fio condutor sobe da filosofia ao veredito. Primeiro o *porquê* — a origem do DO (managed hosting cansado de tickets repetitivos, não academia de sistemas distribuídos), a curadoria como estratégia de produto deliberada (o paradoxo da escolha invertido), e DX como diferencial competitivo central, não acessório. Depois o *o quê* — o catálogo enxuto mapeado categoria por categoria contra o equivalente AWS, com honestidade explícita sobre o que não existe. Depois a *lente onde o DO ganha de fato* — pricing fixo, legível, sem as mil dimensões de cobrança da AWS, e onde previsibilidade vale mais que otimização fina de custo. Depois a *espinha operacional* — o App Platform como o coração da proposta DO, git-push-to-deploy, o spec YAML, e quando ele basta como PaaS. E por fim o *veredito* — o framework de decisão sênior com sinais objetivos, os gatilhos de migração, e o capstone que desenha um SaaS real no DO do zero.

**Audiência primária:** quem já operou (ou vai operar) AWS a fundo e precisa do contraponto — saber quando recomendar ou escolher o DO em vez de reflexivamente ir de AWS. **Audiência secundária:** quem já usa DO no dia a dia mas nunca formalizou *por que* ele funciona pro seu caso, nem os sinais objetivos que indicariam a hora de migrar.

> [!info] Fronteira
> A **AWS a fundo** (o polo de amplitude que este galho contrasta o tempo todo) é o Galho 21 desta trilha; o **Well-Architected Framework** (os princípios de arquitetura que atravessam qualquer provedor) é o Galho 3; **compute, storage, redes e IAM** genéricos (os conceitos que o DO também implementa, só que curados) são os Blocos 1 e 2 inteiros. Este galho trata o DO como produto e como decisão — sua filosofia, seu catálogo, seu pricing, sua espinha operacional e o cálculo de quando ele deixa de bastar — e linka essas fronteiras em vez de reexplicá-las.

## Adepto

1. [[03-Dominios/Tecnologia/Cloud/22 - DigitalOcean a fundo/02 - O catálogo enxuto do DO|02 — O catálogo enxuto do DO]] — o catálogo completo do DO mapeado por categoria (compute, storage, banco, rede, deploy, IA) e contra o equivalente AWS, com honestidade explícita sobre o que não existe (streaming de eventos nível Kinesis, bancos analíticos, multi-conta enterprise).
2. [[03-Dominios/Tecnologia/Cloud/22 - DigitalOcean a fundo/04 - App Platform como espinha|04 — App Platform como espinha]] — o App Platform como o coração da proposta DO: PaaS git-connected, o app spec em YAML, `doctl`, escalonamento e health checks automáticos, e quando ele basta sem precisar descer a container ou VM.

## Magus

3. [[03-Dominios/Tecnologia/Cloud/22 - DigitalOcean a fundo/01 - A filosofia da simplicidade|01 — A filosofia da simplicidade]] — por que o DO escolheu deliberadamente ser enxuto: origem em managed hosting, curadoria opinada como estratégia de produto, o paradoxo da escolha invertido, e DX como diferencial competitivo real.
4. [[03-Dominios/Tecnologia/Cloud/22 - DigitalOcean a fundo/03 - Pricing previsível como diferencial|03 — Pricing previsível como diferencial]] — preço fixo e legível do DO vs a conta imprevisível e multidimensional da AWS: onde previsibilidade vale mais que otimização fina de custo, e onde a AWS ainda ganha.
5. [[03-Dominios/Tecnologia/Cloud/22 - DigitalOcean a fundo/05 - Quando o DO basta e quando cresce pra AWS|05 — Quando o DO basta e quando cresce pra AWS]] — o framework de decisão sênior: os sinais de que o DO é suficiente e os gatilhos objetivos (não vibe) de migração pra AWS, com casos práticos.
6. [[03-Dominios/Tecnologia/Cloud/22 - DigitalOcean a fundo/06 - Capstone — pensar como arquiteto DO|06 — Capstone — pensar como arquiteto DO]] — síntese do galho: desenhar um SaaS B2B real no DO com o kit curado, um segundo caso onde um gatilho de migração acende no meio do caminho, e o checklist de quando essa é a escolha certa. Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — a filosofia, o catálogo, o pricing, a espinha operacional, a decisão, e a síntese aplicada no fim.

### Já uso DO, quero o framework de decisão

01 (a tese — por que a curadoria não é limitação) → 05 (os gatilhos objetivos de quando migrar) → 06 (o checklist aplicado a um caso real, incluindo o caso onde o gatilho acende).

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/21 - AWS a fundo/index|AWS a fundo]] — Galho 21, o polo de amplitude que este galho contrasta nota a nota
- [[03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework/index|Well-Architected Framework]] — Galho 3, os princípios de arquitetura que atravessam qualquer provedor escolhido
