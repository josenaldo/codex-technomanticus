---
title: "Roadmap — DigitalOcean a fundo"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — DigitalOcean a fundo (galho 22)

Roadmap-folha do galho `Cloud/22 - DigitalOcean a fundo`. Bloco 5 (Provedores e maestria) — segundo galho do bloco, par do galho 21 (AWS a fundo). Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - A filosofia da simplicidade
- **Estado:** ✅ feita · fase: Magus · 222 linhas · 2 Mermaid
- **Escopo:** o problema das 240 peças de Lego da AWS (S3 sozinho com storage classes/lifecycle/versionamento/3 camadas de ACL) vs. a resposta única do DO (Spaces); origem — fundação em 24/06/2011 por Ben e Moisey Uretsky + Jeff Carr, Alec Hartman, Mitch Wainer, saídos da ServerStack (managed hosting desde 2003), TechStars Boulder 2012, pricing de lançamento $5/mês, meta de Droplet em <1min; curadoria como decisão de produto (não limitação técnica), o paradoxo da escolha invertido (Barry Schwartz); DX como diferencial competitivo — documentação como produto, Community com 8.000+ tutoriais, UI sem treinamento (Droplet em "55 segundos"); comparação `aws-cli` vs `doctl` em código (grafo de dependências prévias vs. defaults sensatos); tabela de decisões pré-tomadas pela DO (rede, motores de banco, deploy, pricing); tabela-resumo "duas filosofias de produto"; honestidade nos dois sentidos (onde a curadoria se paga vs. onde cobra a conta — sem Organizations/SCPs, sem Kinesis, sem Redshift, sem FedRAMP/HIPAA em todos os serviços); tradução Azure/GCP; três perfis de time (dev solo, scale-up regulada, SaaS pequeno-médio); nuance final — curadoria evolui (DOKS, GPU Droplets, Managed Weaviate) mas mantém o filtro editorial.

#### 02 - O catálogo enxuto do DO
- **Estado:** ✅ feita · fase: Adepto · 238 linhas · 2 Mermaid
- **Escopo:** o catálogo do DO mapeado categoria por categoria (Compute — Droplets/App Platform/Functions/GPU Droplets; Storage — Spaces/Volumes; Bancos — Managed Databases com PostgreSQL/MySQL/Redis-Valkey/MongoDB/Kafka; Rede — VPC/Load Balancers/DNS/Firewalls; Kubernetes — DOKS; IA — GenAI Platform/Gradient/Managed Weaviate) com tabela grande serviço-a-serviço contra o equivalente AWS mais próximo; seção explícita "o que não existe" (streaming nível Kinesis, bancos analíticos tipo Redshift, multi-conta enterprise com SCPs, profundidade de compliance FedRAMP/HIPAA por serviço, Cognito/Step Functions/Athena-Glue equivalentes); tradução pra quem já pensa em Azure/GCP; como ler a tabela na prática (quando "sem equivalente" é lacuna real vs. quando é "resolvido de outro jeito").

#### 03 - Pricing previsível como diferencial
- **Estado:** ✅ feita · fase: Magus · 222 linhas · 4 Mermaid
- **Escopo:** o problema da fatura AWS imprevisível (compute + storage + transferência + IP ocioso em linhas separadas) vs. o modelo DO (preço de tabela fixo por recurso, banda incluída, fatura de uma linha); o terror do egress AWS (múltiplas dimensões de cobrança de saída de dados) vs. banda inclusa no preço do Droplet/Spaces; o custo real de "otimizar" a fatura AWS (FinOps não é grátis — tempo de engenheiro sênior); honestidade sobre onde a AWS ainda ganha (reserved instances/savings plans bem geridos em escala batem o preço fixo do DO); o que a previsibilidade compra além de dinheiro (previsibilidade de orçamento, menos superfície de erro de configuração de custo); exemplo trabalhado — mesma arquitetura, duas faturas lado a lado; tradução Azure/GCP; fluxo prático de decisão; tabela de cenários comparados.

#### 04 - App Platform como espinha
- **Estado:** ✅ feita · fase: Adepto · 289 linhas · 2 Mermaid · mecânica (10 blocos de código: Dockerfile, YAML do app spec, bash `doctl`)
- **Escopo:** o problema que o App Platform resolve (deploy gerenciado sem escolher entre Lambda/Fargate/Beanstalk/App Runner/EC2+ASG); o que é de fato — PaaS git-connected estilo Heroku; o app spec como YAML declarativo da aplicação inteira (services, workers, jobs, static sites, databases anexados); `doctl apps` operando o mesmo spec via CLI; escalonamento, health checks, deploy automático e domínio gerenciado; o modelo mental "Heroku-like"; tamanhos de instância e custo; quando o App Platform basta (vs. quando descer pra Droplet/Kubernetes); tradução Azure (App Service)/GCP (App Engine/Cloud Run) só como nomenclatura; caso prático — saindo do Fargate pro App Platform; as armadilhas (cold start em planos básicos, limites de customização de infraestrutura, vendor lock-in do spec).

#### 05 - Quando o DO basta e quando cresce pra AWS
- **Estado:** ✅ feita · fase: Magus · 165 linhas · 2 Mermaid
- **Escopo:** o problema da pergunta errada ("o DO é bom o bastante?" em vez de "eu preciso do que ele não tem?"); o perfil onde o DO basta e sobra; os gatilhos objetivos de migração — não vibe, sinal concreto (compliance setorial específica, multi-conta com blast radius, serviço de nicho sem equivalente, escala que ultrapassa o teto de algum primitivo DO); tabela de sinais; casos práticos aplicando o framework; nuance de meio-termo (nem tudo é tudo-ou-nada — dá pra somar AWS pontualmente sem migrar tudo); tradução Azure/GCP no mesmo mapa de decisão.

#### 06 - Capstone — pensar como arquiteto DO
- **Estado:** ✅ feita · fase: Magus · 358 linhas · 4 Mermaid · mecânica (12 blocos de código: YAML, HCL Terraform, bash) · **FECHA o galho**
- **Escopo:** recapitulação do arco em cinco notas, uma tese; caso trabalhado — desenhar um SaaS B2B pequeno-médio do zero no DO (Droplet/App Platform + Managed Postgres + Spaces); checklist mental do arquiteto DO; segundo caso — um gatilho de migração acendendo no meio do caminho (o produto cresce e um sinal da nota 05 dispara); checklist mental em detalhe; honestidade reafirmada sobre onde o DO não serve; o que a experiência prolongada em produção ensina que a teoria não; fechamento do arco — duas lentes (amplitude AWS / curadoria DO), uma decisão de engenharia. Capstone do galho.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Como no galho 21, a estrutura de fase é **não monotônica** com a ordem numérica dos arquivos: notas 01, 03, 05 e 06 são Magus; notas 02 e 04 são Adepto. A leitura recomendada continua sendo a ordem numérica 01→06 (ver "Rotas alternativas: Completa" no index) — a seção Adepto/Magus do MOC agrupa por fase de aprendizado, não repete a ordem narrativa.
- Este galho fecha o par de consolidação por provedor do Bloco 5, aberto pelo galho 21 (AWS a fundo). A nota 06 do galho 21 já linkava pra frente pro caminho `22 - DigitalOcean a fundo/05 - Quando o DO basta e quando cresce pra AWS` antes deste `index.md` existir; com este fecho, o galho 22 passa a ter `index.md` publicável — uma futura sessão pode revisar o "Veja também" do galho 21 pra trocar a menção em prosa por wikilink direto ao índice, mas essa edição fica fora do escopo deste fecho (não se toca em notas de conteúdo do galho 21 aqui).
- Fronteiras honestas capturadas nas 6 notas: sem equivalente DO pra Kinesis/streaming de eventos gerenciado, Redshift/bancos analíticos, AWS Organizations/SCPs, Cognito, Step Functions, Athena/Glue, profundidade de compliance setorial (nota 02); onde a AWS ainda ganha em pricing — reserved instances/savings plans bem geridos em escala (nota 03); armadilhas do App Platform — cold start em planos básicos, limite de customização de infra, lock-in do app spec (nota 04).
- Achados factuais verificados na data de escrita (2026-07-24): fundação da DigitalOcean em 24/06/2011, passagem pelo TechStars Boulder 2012, pricing de lançamento $5/mês (Wikipedia + imprensa); "55 segundos" e "8.000+ tutoriais" são números de marketing da própria DigitalOcean, não medição independente — marcados com [!info] na nota 01.
