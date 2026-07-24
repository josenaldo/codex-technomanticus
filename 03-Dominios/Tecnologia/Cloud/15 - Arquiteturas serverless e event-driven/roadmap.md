---
title: "Roadmap — Arquiteturas serverless e event-driven"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Arquiteturas serverless e event-driven (galho 15)

Roadmap-folha do galho `Cloud/15 - Arquiteturas serverless e event-driven`. Bloco 3 (Serverless e arquiteturas modernas) — **capstone do bloco**. Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - O paradigma event-driven completo
- **Estado:** ✅ feita · fase: Iniciado · 185 linhas
- **Escopo:** o problema que motivou os galhos 11-14, o que é de fato um evento, os três papéis (produtor/evento/consumidor), os building blocks recapitulados e encaixados (galho 14 API Gateway na borda, galho 11 Lambda como consumidor/produtor, galho 13 mensageria como canal, galho 12 container para carga pesada) com diagrama Mermaid de um pedido de e-commerce, a regra síncrono-na-borda/assíncrono-no-miolo, por que vale a complexidade, o que ninguém conta antes (debugging distribuído, consistência eventual), AWS catálogo completo ↔ DigitalOcean montado na mão.

#### 02 - Orquestração vs coreografia
- **Estado:** ✅ feita · fase: Adepto · 248 linhas
- **Escopo:** quem decide "e agora, o quê?" depois de um evento, orquestração (um maestro, uma partitura — Step Functions centraliza o fluxo) vs coreografia (ninguém manda, todos reagem — EventBridge/SNS desacopla), o padrão saga que aparece nos dois lados, lado a lado (tabela de trade-offs: acoplamento, visibilidade, debugging, escalabilidade de manutenção), a mesma decisão escrita dos dois jeitos em código.

#### 03 - Step Functions a fundo
- **Estado:** ✅ feita · fase: Adepto · 312 linhas
- **Escopo:** código de orquestração como código que ninguém quer escrever duas vezes, a state machine em Amazon States Language, dois motores para dois tipos de carga (Standard vs Express workflows), as peças menos óbvias da ASL, chamar 200+ APIs da AWS sem escrever cliente HTTP (integrações otimizadas de serviço), saga modelando compensação para transações distribuídas, fan-out sobre uma lista (estado Map), criar e disparar via CLI, honestidade sobre uma lacuna real (limite/lock-in).

#### 04 - Pipeline de dados serverless
- **Estado:** ✅ feita · fase: Adepto · 227 linhas
- **Escopo:** dado chega, alguém precisa processar; o padrão landing→trigger→transform→load; como o dado entra no pipeline (S3 event notification, Kinesis Data Streams); da função solitária ao fan-out orquestrado (Step Functions Map sobre chunks); duas filosofias de processamento (streaming vs batch); pipeline de vendas diário na AWS como exemplo trabalhado; Kinesis Firehose na prática (buffer, S3, transformação inline); armadilhas comuns de ETL serverless.

#### 05 - Padrões e anti-padrões serverless
- **Estado:** ✅ feita · fase: Adepto · 275 linhas
- **Escopo:** você já construiu o sistema errado antes de perceber; os padrões maduros (função de propósito único, fan-out/fan-in, coreografia por eventos, orquestração com Step Functions, idempotência sempre, DLQ em tudo); os anti-padrões (Lambda monolítica, Lambda chamando Lambda de forma síncrona — o calcanhar de Aquiles, estado em memória entre invocações, distributed monolith disfarçado de microsserviços); onde event-driven serverless fica caro, o preço mais alto do event-driven (debugging distribuído); os padrões na prática, AWS e DigitalOcean.

#### 06 - Arquitetura serverless de referência (capstone do Bloco 3)
- **Estado:** ✅ feita · fase: Magus · 195 linhas · **FECHA o galho e o Bloco 3**
- **Escopo:** peças ótimas, sistema nenhum — o problema de abertura; um pedido de e-commerce do clique ao e-mail de confirmação (borda síncrona API Gateway → Lambda cria pedido → EventBridge/SNS fan-out → cobrança/estoque/e-mail → container Fargate para reprocessamento pesado); por que a orquestração some no meio do caminho em certos trechos; a escolha que muda preço e comportamento (Lambda vs Fargate por duração); a tabela de decisão do Bloco 3 inteiro; quando essa arquitetura é a certa e quando é over-engineering; a mesma arquitetura em dois graus de maturidade; paridade AWS ↔ DigitalOcean detalhada (borda+compute boa, orquestração sem paridade — sem Step Functions da DO, mensageria parcial via Managed Kafka, sem EventBridge equivalente, estado bom em relacional sem paridade DynamoDB, storage real via Spaces, analytics sem paridade ponta a ponta); preview do Bloco 4 (IaC, observabilidade, defesa em profundidade, FinOps, resiliência a falha parcial).

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Galho de síntese: nenhuma nota introduz serviço gerenciado novo — todas encaixam Lambda (galho 11), containers (galho 12), mensageria (galho 13) e API Gateway (galho 14) numa arquitetura. Fidelidade de escopo verificada nota a nota via cabeçalhos `##`.
- Contagem de linhas roda mais baixa que o galho 11 (185-312 vs 243-415) porque 4 das 6 notas (02-05) carregam blocos de código/JSON de state machine e diagramas Mermaid que o `wc -l` das notas anteriores também tinha, mas aqui a densidade de prosa por bloco é mais alta — a aceitar como consistente com o padrão "piso é alvo, não gate" já registrado no galho 11.
- Capstone (06, 195 linhas) fecha mais enxuto que o capstone do galho 11 (06, 381 linhas) — cobre 8 galhos anteriores (8-15) numa síntese com diagrama único + tabela de decisão + tabela de paridade AWS/DO, sem reexplicar mecânica já coberta pelos galhos-fonte. Aceito como síntese de ponte, não capstone monolítico.
- Fronteiras confirmadas por leitura das notas: IaC, observabilidade, defesa em profundidade e FinOps aparecem explicitamente adiadas para o Bloco 4 na nota 06 ("O que vem a seguir"); coreografia/coordenação distribuída em abstrato aponta para Comunicação entre Sistemas.
- Wikilinks do índice conferidos via `ls` contra os diretórios reais: Cloud/index, galhos 11/13/14 (`index.md` confirmado em cada), e `Engenharia/Comunicação entre Sistemas/index.md`. Nenhum alvo inexistente linkado.
