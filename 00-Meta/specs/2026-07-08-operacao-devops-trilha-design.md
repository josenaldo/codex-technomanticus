---
title: "Design Spec — Trilha Operação (DevOps/SRE)"
created: 2026-07-08
type: meta
publish: false
tags:
  - meta
  - spec
  - operacao
  - devops
  - sre
---

# Design Spec — Trilha Operação (DevOps/SRE)

> Item 9 da Onda C do [[00-Meta/Roadmap]] — "Operação (DevOps/SRE): CI/CD, containers em produção, observabilidade, deploy strategies, incident response". Par do [[System Design/index|System Design]]: um ensina a **desenhar** o sistema, o outro a **operá-lo**.

## Ponto de vista (a decisão-mestra, travada com o usuário 2026-07-08)

Esta trilha é escrita para **quem já conhece as peças** — as outras trilhas (System Design, Java/Node backend, Redes, Bancos) e as ferramentas (Docker, Kubernetes, CI/CD, observabilidade, Nginx, todas já cobertas como monólitos na estante Infraestrutura). O leitor **não quer aprender o que é um container ou a sintaxe de um Dockerfile** — quer saber **como aplicar tudo junto em produção e onde aprofundar**.

Consequências desse POV:
- **Estilo aplicação/decisão/integração**, não tutorial de ferramenta. Como os walkthroughs do System Design: assume o vocabulário, foca na condução real.
- **Fases Adepto→Magus predominam.** Pouco ou nenhum Iniciado — o leitor já passou disso.
- Cada nota responde "quando/por quê/qual trade-off em produção", não "o que é / como instalar".

## Contexto: o que já existe

A estante `03-Dominios/Tecnologia/Infraestrutura/` guarda **monólitos de ferramenta** ricos, mas em padrão referência (não fase/capítulo). Diagnóstico:

| Monólito | Linhas | Já cobre (relevante) |
|----------|--------|----------------------|
| Kubernetes | 1609 | probes, resources, config, RBAC, deployment strategies, troubleshooting |
| Observabilidade | 1404 | 3 pilares, Prometheus, RED/USE, SLI/SLO/SLA/error budget, tracing, debugging incidentes |
| CI-CD | 1303 | pipeline design, deployment strategies, GitOps, IaC, secrets |
| Docker | 1298 | imagens/layers, otimização, segurança, registry |
| Nginx | 1285 | reverse proxy, LB, TLS, caching, rate limiting |

**Muito do conteúdo sênior já está escrito — mas espalhado dentro dos tool-monoliths e duplicado** (deployment strategies aparece em K8s.md E CI-CD.md; observabilidade em K8s.md E Observabilidade.md; secrets em ambos). A trilha Operação vira a **casa conceitual canônica** dessa camada de prática; os monólitos ficam como **referência de ferramenta** que a trilha cross-linka.

O que genuinamente falta escrever (a cola SRE, hoje inexistente ou tangencial): **incident response / on-call / postmortems** como tema de primeira classe, **SLO engineering** consolidado, **deploy strategies** num lugar só, **migrations de banco em produção**, **IaC conceitual**.

## Estrutura de pastas

Trilha nova em `03-Dominios/Tecnologia/Operação/` (galho-pai, folder-galho no padrão Quartz), **fora** da estante Infraestrutura (que permanece como referência de ferramenta). Padrão idêntico ao System Design:

```
Tecnologia/Operação/
├── index.md            (MOC do galho-pai + porta de entrada)
├── roadmap.md          (roadmap recursivo, galho-pai)
├── 1 - O ofício de operar/     (Iniciado→Adepto)
├── 2 - Entrega e release/       (Adepto)
├── 3 - Rodar em produção/       (Adepto→Magus)
└── 4 - Observar e responder/    (Magus)
+ capstone no galho-pai (Magus)
```

> Nome da pasta com acento (`Operação`) segue a convenção do vault (ex.: `Comunicação entre Sistemas`). Confirmar no scaffolding que a folder-rule do Quartz resolve `[[Operação]]`.

## Roster de notas

### Sub-galho 1 — O ofício de operar (Iniciado→Adepto, ~4 notas)

> Enquadra o POV: o que muda quando o código vira um serviço rodando que alguém precisa manter vivo às 3h da manhã.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | O que é operar um sistema | O gap dev→prod; DevOps e SRE como respostas culturais/organizacionais; "you build it, you run it"; dev vs ops concerns. | enquadra a trilha |
| 02 | O contrato de uma app operável (12-Factor) | Os fatores que importam pra operar: config no ambiente, logs como stream, processos stateless/disposable, dev/prod parity. | linka [[Node.js]]/[[Spring Boot]] (config), System Design (stateless) |
| 03 | O ciclo de vida de um deploy | Visão macro do commit ao tráfego: build→artefato→deploy→release→observação; os próximos galhos são o deep dive de cada etapa. | mapa dos SG2/3/4 |
| 04 | Confiabilidade como feature | Disponibilidade, o custo dos "noves", SLA vs SLO (intro), por que 100% é a meta errada. | prepara o SG4 (SLO) |

### Sub-galho 2 — Entrega e release (Adepto, ~6 notas)

> Levar código a produção **com segurança e velocidade**. Foco em decisão de design, não sintaxe de pipeline.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | Pipeline de CI/CD como decisão de design | Estágios, gates, fast-feedback, o trade-off velocidade×segurança; o que automatizar e o que barrar. | reforço de [[CI-CD]] (ferramenta) sob ótica de design; linka [[Testes JS]]/testes |
| 02 | Deployment strategies | rolling / blue-green / canary / shadow; trade-offs (custo, risco, rollback speed); quando cada. | **casa canônica** — K8s.md/CI-CD.md apontam pra cá |
| 03 | Progressive delivery & rollback | Feature flags como kill switch, canary automatizado health-gated, rollback automático, decoupling deploy≠release. | linka 02 |
| 04 | Migrations de banco em produção | expand/contract, mudança de schema zero-downtime, backfill, o problema do deploy que quebra o schema antigo. | reforço de [[03-Dominios/Ciência/Banco de Dados/index\|Banco de Dados]] sob ótica de release |
| 05 | GitOps & Infrastructure as Code | Declarativo vs imperativo, drift, o repo como fonte da verdade; Terraform/Ansible **conceitual** (onde encaixam), não tutorial. | reforço de [[CI-CD]]; **Cloud fica fora** |
| 06 | Secrets & configuração em produção | Secret management, rotação, nunca commitar segredo, injeção em runtime; Vault/sealed-secrets conceitual. | linka [[Segurança e Guardrails]] se aplicável |

### Sub-galho 3 — Rodar em produção (Adepto→Magus, ~6 notas)

> O sistema está no ar. Como mantê-lo no ar, escalando e sem derrubar ninguém. **Fronteira dupla:** ferramenta (Docker/K8s/Nginx = referência) e app-JVM (Java G17).

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | Containers em produção | O que muda vs dev: imutabilidade, imagem mínima/segura, o container como unidade de deploy, o que NÃO colocar num container. | reforço de [[Docker]]; fronteira Java G17 (Jib/distroless é lá) |
| 02 | O contrato de produção do Kubernetes | Probes (liveness/readiness/startup), requests/limits, HPA, PDB, graceful shutdown — a **ótica operacional** (não "o que é um Pod"). | reforço de [[Kubernetes]]; **fronteira Java G17** (mesmo contrato, ótica JVM lá) |
| 03 | Zero-downtime & alta disponibilidade | Rolling sem derrubar, connection draining, readiness gating, réplicas + anti-affinity, o deploy que perde requests. | linka 02 e SG2-02 |
| 04 | Escala & capacidade | Autoscaling (HPA/VPA/cluster), capacity planning, o custo de escalar, load shedding, back-of-envelope de capacidade. | reforço de System Design (estimativas) sob ótica de operação |
| 05 | Rede & borda em produção | Ingress/reverse proxy, TLS termination, rate limiting na borda, health checks do LB. | reforço de [[Nginx]]; fronteira System Design (CDN/LB conceitual) |
| 06 | Resiliência operacional | Timeouts, retries com backoff, circuit breaker, bulkhead — **sob a ótica de quem opera** (config, tuning, o que observar). | **reforço** de [[05 - Circuit Breaker e resiliência]] (System Design) — ótica de operação, não de design |

### Sub-galho 4 — Observar e responder (Magus, ~6 notas)

> O coração da trilha e a parte mais fraca hoje no vault. Reliability engineering: enxergar o sistema e reagir quando ele quebra.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | Observabilidade como prática | Não "o que é log/métrica" — como **instrumentar pra responder perguntas não-antecipadas**; os 3 pilares aplicados, cardinalidade, structured logging, correlação. | reforço de [[Observabilidade]] (ferramenta) sob ótica de prática |
| 02 | SLI, SLO e error budgets | A **engenharia**: escolher SLI, definir SLO, o error budget como orçamento de risco e contrato dev↔ops, gastar/congelar. | casa canônica; Observabilidade.md aponta pra cá |
| 03 | Alerting que não gera fadiga | Alertar em **sintoma não causa**, RED/USE, page vs ticket, alert fatigue, runbooks acionáveis. | linka 01 e 02 |
| 04 | Incident response & on-call | O processo ao vivo de um incidente: papéis (IC), comunicação, **mitigar antes de achar root cause**, severidades, on-call saudável. | **novo — cola SRE central** |
| 05 | Postmortems & cultura blameless | Aprender com a falha: timeline, contributing factors, action items, blameless — por que culpar pessoa piora a confiabilidade. | linka 04 |
| 06 | Debugging de produção & chaos engineering | Investigar sob pressão com observabilidade; o arquétipo "troubleshoot" da entrevista; chaos como investir em confiança antes do incidente. | **reforço** do arquétipo troubleshoot de [[01 - O que é System Design e o que a entrevista avalia]] |

### Capstone (Magus, galho-pai)

**"Anatomia de um incidente de produção"** — um walkthrough integral que costura tudo: um serviço saudável, um deploy, um sintoma, o alerta, a resposta ao incidente, a mitigação, o postmortem, e o action item que vira melhoria de pipeline/observabilidade. Aplica os 4 sub-galhos num arco único. Decidir ao fechar o SG4 se puxa experiência real do usuário (só se ele fornecer — **nunca fabricar**, ver [[feedback_no_fabrication]]).

**Total planejado:** ~22 notas (4+6+6+6) + 1 capstone = **~23 notas**.

## Fronteiras anti-duplicação

| Tópico | Papel aqui | Mora em | Regra |
|--------|-----------|---------|-------|
| Docker/K8s/Nginx/CI-CD (sintaxe, "o que é") | — | Infraestrutura (monólitos) | referência: linkar, não reescrever |
| JVM-em-container, Jib/distroless, Spring AOT, contrato K8s da app | — | Java Galho 17 (Cloud-native) | app-side; Operação é agnóstico — reforço + cross-link |
| Cloud (AWS/GCP, managed services) | — | cobertura futura (fora de escopo) | Digital Ocean fica na estante; não entrar |
| Circuit breaker, retry, bulkhead (design) | ótica de operação | [[3 - Padrões recorrentes/index\|System Design SG3]] | reforço: como operar/tunar, não como desenhar |
| Deployment strategies, SLO, secrets (hoje duplicados nos monólitos) | casa canônica | esta trilha | monólitos ganham callout apontando pra cá |
| Estimativas de capacidade | ótica de operação | System Design SG1-03 | reforço |
| Testes/qualidade no pipeline | gate do pipeline | [[Testes JS]], Engenharia/Testes | linkar |

## Padrão de escrita (cravado)

Nota = **capítulo de livro** ([[feedback_padrao_capitulo_livro]]): TL;DR `[!abstract]`, abertura problema-first (uma cena de produção concreta), divulgação progressiva, exemplo trabalhado. Densidade-alvo **~440-540 linhas / alto word-count** ([[feedback_notas_profundas_diagramas]]). `fase:` no frontmatter. ≥1 Mermaid (paleta azul `#4A90D9` / âmbar `#F5A623` / vermelho `#D0021B`). Callouts `[!question]-` e `[!warning]`. Seção "Em entrevista" (operação cai em entrevista sênior) + "How to explain in English" com tabela PT↔EN. "O que vem a seguir". `## Fontes` com URL e dado datado. **Barra de densidade explícita no prompt de cada subagente** (mirar 5-7k palavras / 15-25 buscas / exemplo concreto) — lição do System Design SG3.

## Fontes canônicas da trilha

- **Livros:** *Site Reliability Engineering* (Google, "o livro SRE") + *The SRE Workbook*; *The DevOps Handbook* (Kim et al.); *Release It!* (Nygard); *Accelerate* (Forsgren/Humble/Kim — as 4 métricas DORA); *Designing Data-Intensive Applications* (Kleppmann).
- **Online:** Google SRE Book (sre.google/books); AWS Builders' Library; docs Kubernetes/Prometheus/Grafana; Charity Majors / honeycomb (observability); posts de postmortem público (ex.: Gitlab, Cloudflare).

## Plano de execução (ritmo B, igual System Design)

1. Criar `Operação/index.md` + `roadmap.md` (galho-pai).
2. Semear sub-galho a sub-galho, ordem 1→2→3→4. Cada subpasta: `index.md` + `roadmap.md` + notas via subagente-por-nota (**≤3/onda**, Sonnet, cada um lê o EXEMPLAR do System Design + este spec + o monólito de referência relevante, WebSearch inline, barra de densidade explícita).
3. Ao fechar cada sub-galho: roadmap-folha + roadmap-pai + commit (paths explícitos, sem Co-Authored-By, push manual).
4. Fechamento: capstone; adicionar callouts nos monólitos duplicados (K8s/CI-CD/Observabilidade) apontando pra casa canônica; atualizar [[00-Meta/Roadmap]] item 9 ⬜→🟢; atualizar memória.

## Pontos em aberto (decidir durante a execução)

- **IaC (SG2-05):** manter conceitual (recomendado) ou virar galho próprio com Terraform? Decisão: conceitual agora; Terraform vira broto/galho futuro se necessário.
- **On-call/incident (SG4-04/05):** confirmado dentro do escopo (é a cola SRE que falta).
- **EXEMPLAR:** usar a nota 01 do System Design (`1 - Framework de entrevista/01`) como referência de estrutura até a 1ª nota desta trilha virar o exemplar próprio.
- **Renumeração/contagem** por sub-galho pode ajustar no seeding.
