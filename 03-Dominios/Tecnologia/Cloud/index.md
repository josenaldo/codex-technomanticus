---
title: "Cloud"
type: moc
publish: true
created: 2026-07-20
updated: 2026-07-24
status: seedling
tags:
  - moc
  - cloud
  - aws
  - digitalocean
aliases:
  - Cloud
  - Computação em Nuvem
---
# Cloud

> [!abstract] TL;DR
> Trilha Cloud organizada em **24 galhos + capstone**, com espinha conceitual-neutra: cada nota ensina o conceito e aplica a **lente dupla AWS↔DigitalOcean** — o serviço "canônico" da AWS ao lado do equivalente pragmático da DigitalOcean, que o autor usa há ~2 anos. Azure e Google Cloud entram só como camada de tradução (mapeamento de nomes), não como trilhas próprias. O **Well-Architected Framework** (os 6 pilares) é a bússola conceitual que atravessa o domínio inteiro.

Cloud aqui é a **plataforma e seus serviços gerenciados** — compute, rede, armazenamento, bancos, serverless, mensageria — e o modelo mental pra raciocinar sobre eles (responsabilidade compartilhada, elasticidade, plano de controle vs plano de dados). Não é a disciplina de operar em produção (isso é [[03-Dominios/Engenharia/Operação/index|Operação]]) nem a arte de desenhar sistemas (isso é [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura]]) — é a base sobre a qual as duas se apoiam. Ver [[03-Dominios/Tecnologia/Cloud/roadmap|roadmap]] pro estado de cada galho.

## Galhos da trilha

### Bloco 1 — Modelo mental e fundamentos

1. ✅ [[03-Dominios/Tecnologia/Cloud/01 - O que é a nuvem, de verdade/index|O que é a nuvem, de verdade]]
2. ✅ [[03-Dominios/Tecnologia/Cloud/02 - Anatomia de um provedor/index|Anatomia de um provedor]]
3. ✅ [[03-Dominios/Tecnologia/Cloud/03 - Well-Architected Framework/index|Well-Architected Framework]]
4. ✅ [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Identidade e acesso (IAM)]]

### Bloco 2 — Os primitivos

5. ✅ [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/index|Compute I — máquinas virtuais]]
6. ✅ [[03-Dominios/Tecnologia/Cloud/06 - Compute II — elasticidade e balanceamento/index|Compute II — elasticidade e balanceamento]]
7. ✅ [[03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)/index|Rede na nuvem (VPC)]]
8. ✅ [[03-Dominios/Tecnologia/Cloud/08 - Armazenamento (object, block e file)/index|Armazenamento — object, block e file]]
9. ✅ [[03-Dominios/Tecnologia/Cloud/09 - Bancos gerenciados/index|Bancos gerenciados]]
10. ✅ [[03-Dominios/Tecnologia/Cloud/10 - DNS, CDN e borda/index|DNS, CDN e borda]]

### Bloco 3 — Serverless e arquiteturas modernas

11. ✅ [[03-Dominios/Tecnologia/Cloud/11 - Serverless e FaaS — Lambda a fundo/index|Serverless e FaaS — Lambda a fundo]]
12. ✅ [[03-Dominios/Tecnologia/Cloud/12 - Containers gerenciados/index|Containers gerenciados]]
13. ✅ [[03-Dominios/Tecnologia/Cloud/13 - Mensageria e eventos gerenciados/index|Mensageria e eventos gerenciados]]
14. ⬜ API Gateway e edge de aplicação
15. ⬜ Arquiteturas serverless e event-driven

### Bloco 4 — Operar, sustentar, governar

16. ⬜ Infrastructure as Code
17. ⬜ Observabilidade na cloud
18. ⬜ Segurança na cloud a fundo
19. ⬜ FinOps — a economia da cloud
20. ⬜ Resiliência e continuidade

### Bloco 5 — Provedores e maestria

21. ⬜ AWS a fundo — consolidação
22. ⬜ DigitalOcean a fundo — consolidação
23. ⬜ Panorama multi-cloud e portabilidade
24. ⬜ Certificação — AWS Solutions Architect Associate

### Capstone

- ⬜ Arquitetar um SaaS na cloud do zero — costura os 24 galhos numa arquitetura completa

## Como ler

A ordem numérica (1→24, blocos 1→5) é a recomendada: modelo mental primeiro, depois os primitivos, depois serverless, depois governança, e só no final a consolidação por provedor. Mas quem já usa DigitalOcean no dia a dia pode ler o **galho 22 (DigitalOcean a fundo)** cedo, como âncora — ele mapeia o que você já conhece na prática pro vocabulário formal que os galhos 1-20 constroem. Ainda assim, a ordem numérica cobre o terreno com menos buracos.

## Artefatos do domínio

- [[03-Dominios/Tecnologia/Cloud/Dicionário|Dicionário]] — glossário provider-neutro dos termos do domínio.
- [[03-Dominios/Tecnologia/Cloud/Biblioteca|Biblioteca]] — recursos externos (AWS, DigitalOcean, Azure, GCP).
- [[03-Dominios/Tecnologia/Cloud/roadmap|Roadmap]] — estado de construção dos 24 galhos.

## Veja também

- [[03-Dominios/Engenharia/Operação/index|Operação (DevOps/SRE)]] — Cloud é a plataforma e seus serviços; Operação é a disciplina de operá-los em produção (CI/CD, observabilidade operacional, incident response).
- [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura / System Design]] — Cloud fornece os primitivos; Arquitetura decide como compô-los num sistema.
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — mensageria e APIs atravessam a fronteira entre os dois domínios.
- [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]] — IAM (galho 4) é a aplicação, na nuvem, dos conceitos gerais desse domínio.
- [[04-Sendas/Senda Cloud|Senda Cloud]] — ordem de leitura curatorial e recursos externos usados como pesquisa prévia.
