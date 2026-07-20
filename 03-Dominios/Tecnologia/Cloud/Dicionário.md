---
title: "Dicionário — Cloud"
created: 2026-07-20
updated: 2026-07-20
type: glossary
status: seedling
aliases: []
tags:
  - glossary
  - cloud
lang: pt
publish: true
---

# Dicionário — Cloud

> Glossário do domínio Cloud: vocabulário conceitual-neutro, com o equivalente AWS/DigitalOcean apontado quando fizer sentido. Cada verbete é referenciado por uma ou mais notas das trilhas do domínio.

<!--
Como usar este glossário:

- Verbetes em ordem alfabética, um `###` cada.
- Linkar de outra nota: [[Dicionário#Nome do termo]]
- Customizar texto exibido: [[Dicionário#Nome do termo|texto]]
- A skill /verbete adiciona termos automaticamente em ordem alfabética.
- Cada verbete tem 2-4 linhas de definição em PT-BR, provider-neutra, com o equivalente AWS/DO citado quando ajudar a fixar o conceito.
-->

### Availability zone

Data center (ou grupo de data centers) fisicamente isolado dentro de uma region, com energia, refrigeração e rede independentes dos demais — a unidade que a nuvem usa pra sobreviver a uma falha localizada sem sair da region. Na AWS, cada region tem 3+ AZs (`us-east-1a`, `us-east-1b`...); a DigitalOcean não expõe AZs como conceito de primeira classe — seus datacenters (`nyc1`, `nyc3`) já fazem esse papel de forma mais simples, sem multi-AZ dentro do mesmo datacenter.

### Blast radius

O "raio de explosão" de uma falha ou de um acesso comprometido: quanto do sistema é afetado quando algo dá errado. Desenhar pra reduzir blast radius significa isolar recursos (contas separadas, VPCs separadas, IAM com escopo mínimo) pra que uma falha ou vazamento em uma parte não derrube ou exponha o resto.

### Egress

Tráfego de dados **saindo** da rede do provedor pra fora (internet ou outra region/provedor). É o lado que normalmente tem custo — ingress (entrada) costuma ser gratuito. AWS cobra egress por GB com faixas regressivas; a DigitalOcean inclui uma cota generosa de egress no preço do droplet antes de cobrar o excedente, o que simplifica bastante a conta.

### Elasticidade

Capacidade de um recurso crescer ou encolher automaticamente conforme a demanda, sem intervenção manual — o oposto de provisionar pra pico e deixar capacidade ociosa. Auto Scaling Groups na AWS e Autoscale Pools na DigitalOcean são a mesma ideia com nomes diferentes.

### FaaS

Function as a Service — unidade de deploy é uma função, não um servidor nem um container; o provedor cuida de provisionamento, scaling e cobra por invocação/tempo de execução. AWS Lambda é a referência do mercado; a DigitalOcean tem Functions (baseado em Apache OpenWhisk), com proposta mais simples e menos integrada ao resto da plataforma.

### IaaS

Infrastructure as a Service — o provedor entrega a infraestrutura crua (máquina virtual, rede, storage) e você administra o sistema operacional pra cima. É a camada mais baixa das três (IaaS/PaaS/SaaS); EC2 (AWS) e Droplets (DigitalOcean) são IaaS clássico.

### Lock-in

Grau de dificuldade (técnica, contratual ou de custo) pra migrar uma carga de trabalho pra fora de um provedor. Serviços gerenciados proprietários (ex.: DynamoDB, Lambda com integrações nativas) aumentam lock-in em troca de produtividade; a DigitalOcean, por apostar mais em ferramentas open-source padrão (Kubernetes vanilla, Postgres gerenciado), tende a gerar menos lock-in — trade-off explorado a fundo no galho 23 (Panorama multi-cloud).

### PaaS

Platform as a Service — o provedor cuida também do runtime/sistema operacional; você entrega código ou imagem e ele cuida do resto. AWS Elastic Beanstalk e App Runner, ou a App Platform da DigitalOcean, são exemplos — mais abstração que IaaS, menos que SaaS.

### Plano de controle

*Control plane*: a camada que **gerencia** os recursos — API que recebe "crie uma VM", "delete um bucket", decide onde e como. É o que você toca quando usa o console, a CLI ou o Terraform. Separado (e normalmente mais lento/menos crítico pra latência) do plano de dados.

### Plano de dados

*Data plane*: a camada que **executa** o trabalho real — os pacotes de rede sendo roteados, os bytes sendo lidos de um disco, a requisição HTTP sendo respondida. É o que precisa ser rápido e resiliente segundo a segundo; uma falha no plano de controle não deveria (num bom design) derrubar o plano de dados já em execução.

### Region

Área geográfica ampla onde um provedor opera um cluster de datacenters (uma ou mais availability zones). Escolher a region certa é decisão de latência, custo, residência de dados e conformidade legal. AWS tem ~30+ regions no mundo; a DigitalOcean tem um conjunto bem mais enxuto (~15 datacenters), o que simplifica a escolha mas reduz a granularidade geográfica.

### Responsabilidade compartilhada

*Shared responsibility model*: o modelo que divide segurança entre provedor ("segurança **da** nuvem" — hardware, datacenter, rede física, hipervisor) e cliente ("segurança **na** nuvem" — configuração, dados, IAM, patch do SO em IaaS). Quanto mais gerenciado o serviço (IaaS → PaaS → SaaS), mais responsabilidade migra pro provedor. É a bússola de segurança do domínio, aprofundada no galho 18.

### Right-sizing

Prática de ajustar o tamanho (CPU, memória, tipo de instância) de um recurso pra sua carga real de trabalho, evitando tanto over-provisioning (custo desperdiçado) quanto under-provisioning (risco de saturação). Pilar central de FinOps (galho 19) — ferramentas como AWS Compute Optimizer automatizam a recomendação; na DigitalOcean, o exercício costuma ser manual, olhando métricas de CPU/memória do droplet ao longo do tempo.

### SaaS

Software as a Service — a aplicação inteira é entregue pronta pro uso final; nada de infraestrutura, runtime ou até código pra gerenciar. É o topo da pirâmide IaaS/PaaS/SaaS — o próprio objetivo do capstone da trilha é construir *um* SaaS usando as camadas de baixo.
