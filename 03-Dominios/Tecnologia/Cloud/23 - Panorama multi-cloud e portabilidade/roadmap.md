---
title: "Roadmap — Panorama multi-cloud e portabilidade"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Panorama multi-cloud e portabilidade (galho 23)

Roadmap-folha do galho `Cloud/23 - Panorama multi-cloud e portabilidade`. Bloco 5 (Provedores e maestria). Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - Por que (e por que não) multi-cloud
- **Estado:** ✅ feita · fase: Magus · 134 linhas
- **Escopo:** desmonta o mito "não colocar os ovos numa cesta só" (analogia mal aplicada com diversificação financeira), o espectro single-cloud → ativo-ativo com gradiente de custo, as razões legítimas (regulação/soberania de dados, requisito contratual de cliente/governo, best-of-breed pontual como BigQuery, M&A que herdou duas nuvens, DR cross-provider) vs as ruins ("ovos na cesta" sem medir, poder de barganha fantasioso, resiliência que vira fragilidade, portabilidade "por via das dúvidas"), o custo real decomposto (2x IAM/rede/billing/skills, abstração de menor denominador comum, egress inter-cloud), tabela motivo→legítimo?→custo, e um caso trabalhado (fintech que quase migra pro Azure "por precaução").

#### 02 - Azure em uma nota
- **Estado:** ✅ feita · fase: Adepto · 139 linhas
- **Escopo:** a Azure como produto de identidade e integração enterprise que também vende compute — Microsoft Entra ID (ex-Azure AD, identidade de *usuário*, não de recurso) vs Azure RBAC (identidade de recurso, o parente do IAM), Azure Arc (gerenciar híbrido/multi-cloud como se fosse Azure) e Azure Stack (hardware Azure on-prem), tabela de tradução núcleo Azure↔AWS↔DO (compute, storage, banco, rede, identidade, IaC), hierarquia Management Group→Subscription→Resource Group, três casos práticos (empresa já Microsoft, fintech greenfield sem AD, agência de governo/FedRAMP), onde a Azure é notavelmente forte (identidade/Zero Trust, .NET/Office 365, governo/reguladas), e onde a analogia AWS→Azure quebra.

#### 03 - GCP em uma nota
- **Estado:** ✅ feita · fase: Adepto · 176 linhas
- **Escopo:** o GCP como engenharia interna do Google exportada (MapReduce, Bigtable, Borg→Kubernetes) — três traços de filosofia (data-first, network-first, opinião forte/catálogo menor), núcleo traduzido por categoria (Compute Engine, **Cloud Run** com scale-to-zero real destacado, **GKE**, Cloud Functions; Cloud Storage/Persistent Disk; Cloud SQL, **Cloud Spanner** com TrueTime, **BigQuery** como diferencial), a VPC global do GCP vs VPC regional da AWS (diagrama comparativo), onde o GCP brilha (BigQuery/analytics, GKE/Cloud Run, rede global, Vertex AI/ML) e onde o catálogo é mais raso, tabela de tradução GCP↔AWS completa.

#### 04 - A tabela de tradução dos quatro
- **Estado:** ✅ feita · fase: Adepto · 201 linhas · nota de referência
- **Escopo:** a tabela mestra de equivalência AWS/Azure/GCP/DO por categoria — compute (VM, auto scaling, spot), containers/Kubernetes (EKS/AKS/GKE/DOKS, registries), serverless/FaaS, PaaS de aplicação, storage (object/block/file), bancos relacionais e NoSQL, cache, rede (VPC/LB/DNS/CDN), fila/mensageria (maior lacuna da DO), API Gateway/WAF, IaC (Terraform como denominador comum), identidade, observabilidade; cada linha linka de volta pra nota da trilha que explica o conceito; travessão explícito onde o provedor genuinamente não tem produto equivalente.

#### 05 - Lock-in e portabilidade — Kubernetes como camada
- **Estado:** ✅ feita · fase: Magus · 180 linhas · nota central
- **Escopo:** lock-in como espectro (IaaS puro → serviços gerenciados abertos → proprietários com API de facto → 100% proprietários) com correlação inversa lock-in↔esforço operacional, tabela serviço→grau de lock-in→esforço de migração (EC2 horas, DynamoDB/BigQuery meses), Kubernetes como maior ilha de portabilidade real (manifests portam, mas LoadBalancer/PersistentVolume não — diagrama), outras camadas neutras (Terraform/OpenTofu, padrões abertos S3/Postgres/OpenTelemetry, especificação OCI de containers), três casos trabalhados (startup abraça lock-in, fintech regulada minimiza, empresa data-heavy já capturada pelo BigQuery), GitOps/multi-cluster como teste prático de portabilidade, framework de decisão (fluxograma probabilidade de troca × ganho de produtividade), lock-in não-técnico (contratual/committed use, skills, gravitação de dados), armadilha do "imposto de portabilidade pago pra um evento que nunca vem".

#### 06 - Capstone — a decisão de provedor
- **Estado:** ✅ feita · fase: Magus · 103 linhas · **FECHA o galho**
- **Escopo:** recapitula as 5 notas anteriores em quatro movimentos (mito do multi-cloud → Azure → GCP → tabela/lock-in), framework de decisão de provedor em fluxograma (ecossistema dominante → compliance setorial → perfil data-heavy → escala/amplitude → budget/previsibilidade), peso de cada ramo (AWS amplitude, Azure legado corporativo, GCP dados, DO simplicidade), quatro cenários trabalhados (startup SaaS enxuta, enterprise casa Microsoft, produto data-heavy, empresa que precisa de amplitude) com recomendação e porquê, a regra de ouro (uma nuvem principal + multi-cloud só com motivo mensurável + lock-in seletivo). Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Galho escrito com AWS (galho 21) e DigitalOcean (galho 22) já a fundo no domínio — Azure e GCP tratados só em nível de filosofia/mapa mental (nem hands-on), por design deliberado (registrado explicitamente na nota 03 e no capstone).
- Achado factual capturado com honestidade: Microsoft Entra ID (ex-Azure AD, rebranding 2023) é identidade de *usuário/gente*, distinto de Azure RBAC (identidade de *recurso*) — a fonte mais comum de confusão pra quem já conhece IAM da AWS; capturado com [!info] verificado em learn.microsoft.com. Modo "indirectly connected" do Azure Arc foi aposentado em setembro de 2025.
- Honestidade de precificação: preço exato do BigQuery por TB (nota 03) não pôde ser confirmado diretamente na página oficial (conteúdo truncado na busca) — marcado explicitamente com [!info] em vez de cravar o número, mesma disciplina já usada no galho de Serverless (galho 11) pra pricing que renderiza via JS.
- Nota 05 registra explicitamente que os graus de lock-in e esforços de migração na tabela central são avaliação qualitativa de arquitetura, não benchmark publicado — heurística de conversa de design, não métrica auditável.
- Fronteiras: Kubernetes gerenciado (produto) → galho 12 (Containers gerenciados); Terraform/IaC a fundo → galho 16; FinOps/committed use discounts a fundo → galho 19; contrato de produção do Kubernetes (operação) → domínio Engenharia/Operação (linkado direto na nota 05). Todas prosa, não reexplicadas aqui.
- Notas de fase: galho sem nota Iniciado — a fase de entrada já pressupõe AWS e/ou DigitalOcean a fundo (galhos 21/22), então a nota 01 (Magus) abre direto com uma decisão de arquitetura, não com fundamentos.
