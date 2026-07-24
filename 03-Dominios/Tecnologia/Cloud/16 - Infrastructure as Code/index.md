---
title: "Cloud — Infrastructure as Code"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - iac
  - terraform
aliases:
  - "Infrastructure as Code"
  - "Galho 16 - Infrastructure as Code"
---

# Infrastructure as Code

> [!abstract] TL;DR
> Galho 16 da trilha Cloud, e o que **abre o Bloco 4 (operar, sustentar, governar)**. Os três blocos anteriores ensinaram compute, dados, rede, storage, serverless — sempre assumindo, em silêncio, que *alguém* provisiona isso de algum jeito. Este galho torna esse "de algum jeito" explícito: infraestrutura deixa de ser cliques no console (ClickOps) e vira código versionado, revisável e reproduzível. O galho sobe do *porquê* ao *como escolher*: primeiro o problema do ClickOps e o modelo declarativo vs. imperativo, depois **Terraform a fundo** (HCL, providers, o ciclo `init`/`plan`/`apply`, o grafo de dependências), depois o **state** — o mapa que separa Terraform de um script qualquer, e por que ele precisa de backend remoto com locking em qualquer time real —, depois o caminho **nativo da AWS** (CloudFormation, change sets, SAM, CDK) como contraponto ao multi-cloud, depois **módulos, ambientes e boas práticas** que separam um repositório de IaC amador de um profissional, e fecha com o capstone: a árvore de decisão entre Terraform, CloudFormation/CDK e Pulumi, aplicada de volta à arquitetura serverless que fechou o Bloco 3, mais os anti-padrões que mais custam caro em produção. 6 notas, 3 fases, lente dupla Terraform multi-cloud (AWS ↔ DigitalOcean) — com honestidade sobre onde a DO simplesmente não tem equivalente nativo.

## Sobre este galho

IaC é a virada de "lembrar quais botões cliquei" para "ler o que está escrito no arquivo". Não é só conveniência: é reprodutibilidade (o mesmo arquivo gera a mesma infraestrutura em qualquer conta ou região), versionamento real (`git log` vira histórico da infraestrutura), code review antes de qualquer mudança tocar produção, e um `plan` que mostra exatamente o que vai mudar antes de mudar — o equivalente de um `git diff` para infraestrutura. Este galho não vende Terraform como única resposta; ensina a mecânica do modelo declarativo a fundo, o contraponto nativo de cada nuvem, e a disciplina de engenharia (módulos, ambientes, CI, segredos fora do código) que separa um repositório de IaC que sobrevive ao crescimento de um que vira, ele mesmo, um novo ClickOps.

O fio condutor sobe do problema à decisão de arquitetura. Primeiro o *porquê* — os quatro pecados do ClickOps (drift, snowflake servers, ausência de review, conhecimento tribal), a distinção declarativo vs. imperativo, idempotência, e o panorama das ferramentas. Depois a *mecânica* Terraform em duas notas: a linguagem (HCL, os seis tipos de bloco, o ciclo `init`→`plan`→`apply`→`destroy`, providers, o grafo de dependências, `count`/`for_each`), e o **state** — por que ele existe, por que é perigoso (segredos em texto puro, dessincronização), backend remoto com locking (S3+DynamoDB/`use_lockfile` na AWS, Spaces na DO, Terraform Cloud), `terraform_remote_state`, drift, `import`, `state mv`, e por que workspaces não servem para separar dev/stage/prod. Depois o *contraponto nativo* — CloudFormation (templates, stacks, change sets, rollback automático, drift detection, nested stacks, StackSets), SAM, e CDK (infraestrutura em linguagem de programação de verdade, compilando para CloudFormation por baixo). Depois *organização e disciplina* — módulos como unidade de reuso, a estratégia de ambientes que de fato vence na indústria (diretórios + módulos, não workspaces), segredos nunca no código, CI com `plan` no PR e `apply` no merge, e as ferramentas de qualidade (`validate`, tflint, Checkov). E por fim a *decisão* — a árvore de três perguntas (multi-cloud? lógica real ou declaração estática? aceita gerenciar state?), os três estágios de maturidade operacional, e os cinco anti-padrões mais caros.

**Audiência primária:** quem já clicou o suficiente no console para sentir a dor — recriar um ambiente, explicar por que um recurso está diferente do esperado — mas nunca escreveu um `.tf` de verdade nem entende por que "o state" é um problema à parte. **Audiência secundária:** quem já usa Terraform no trabalho mas nunca formalizou por que backend remoto com locking é obrigatório em time, por que workspaces não servem para separar produção de staging, ou quando CloudFormation/CDK realmente vence Terraform.

> [!info] Fronteira
> **GitOps, pipelines de deploy e "quem aperta o botão de produção"** são disciplina de entrega contínua, tratada no domínio [[03-Dominios/Engenharia/Operação/index|Operação]] — este galho ensina o modelo declarativo e como rodar `plan`/`apply`, não como orquestrar isso dentro de um pipeline. **Observabilidade** (instrumentar o que o IaC provisionou) é o próximo galho desta trilha; **segurança** e **resiliência** também vêm depois no Bloco 4, e todas as três assumem como pré-condição a infraestrutura declarada que este galho entrega. Este galho trata só de *provisionar* — a ferramenta, o modelo, o state, a organização do código — e linka essas fronteiras em vez de reexplicá-las.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/16 - Infrastructure as Code/01 - Por que Infrastructure as Code|01 — Por que Infrastructure as Code]] — o problema do ClickOps (drift, snowflake servers, sem code review, conhecimento tribal), o que IaC entrega (reprodutibilidade, versionamento, plan antes de aplicar), declarativo vs. imperativo, idempotência, e o panorama das ferramentas (Terraform, OpenTofu, CloudFormation, CDK, Pulumi); Terraform ↔ DO (sem fila gerenciada nativa, mesma forma sintática com um Droplet).

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/16 - Infrastructure as Code/02 - Terraform a fundo|02 — Terraform a fundo]] — HCL e os seis (mais `locals`) tipos de bloco, o ciclo `init`→`plan`→`apply`→`destroy`, providers (o mesmo vocabulário, nuvens diferentes: `aws_instance` ↔ `digitalocean_droplet`), o grafo de dependências (implícita vs. `depends_on`), `lifecycle`, `count` vs. `for_each`, OpenTofu como fork open-source; variables/outputs amarrando tudo.
3. [[03-Dominios/Tecnologia/Cloud/16 - Infrastructure as Code/03 - State, backends e colaboração|03 — State, backends e colaboração]] — o que é o state e por que o Terraform precisa dele, os dois riscos (segredos em texto puro, dessincronização da realidade), state local vs. remoto, locking (por que dois `apply` simultâneos corrompem tudo), backend S3+DynamoDB/`use_lockfile` (AWS) ↔ Spaces S3-compatível (DO) ↔ Terraform Cloud gerenciado, `terraform_remote_state`, drift, `terraform import`, `terraform state mv`, e por que workspaces não servem para isolar dev/stage/prod.
4. [[03-Dominios/Tecnologia/Cloud/16 - Infrastructure as Code/04 - IaC nativo — CloudFormation e CDK|04 — IaC nativo — CloudFormation e CDK]] — templates, stacks e o motor de orquestração do CloudFormation, change sets (o "terraform plan" da AWS), rollback automático e drift detection, nested stacks e StackSets, SAM (açúcar para serverless), CDK (infraestrutura em linguagem de programação real, compilando para CloudFormation), quando cada um vale contra Terraform/Pulumi; honestidade sobre a DO não ter equivalente nativo.
5. [[03-Dominios/Tecnologia/Cloud/16 - Infrastructure as Code/05 - Módulos, ambientes e boas práticas|05 — Módulos, ambientes e boas práticas]] — módulos como unidade de reuso (inputs/outputs, fontes local/Registry/Git), a estratégia de ambientes que vence na prática (diretórios + módulos, não workspaces, com Terragrunt como camada opcional), segredos nunca no código (cofre em runtime), CI com `plan` no PR e `apply` no merge, `validate`/tflint/Checkov como portão de qualidade, e boas práticas de tagging/naming/least privilege.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/16 - Infrastructure as Code/06 - Escolher e operar IaC (capstone)|06 — Escolher e operar IaC]] — a árvore de decisão de três perguntas (multi-cloud? lógica real ou declaração estática? aceita gerenciar state?) entre Terraform, CloudFormation/CDK e Pulumi, aplicada de volta à arquitetura serverless de referência do Bloco 3 (esqueleto de módulos), os três estágios de maturidade operacional, o custo de trocar de ferramenta depois, os cinco anti-padrões mais caros (state local commitado, apply sem plan, mono-state gigante, secrets no código, drift ignorado), e por que IaC é fundação — não conveniência — para observabilidade, segurança e resiliência. Capstone do galho, abre o Bloco 4.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — o problema, a mecânica Terraform, o state, o contraponto nativo, a organização de código, e a decisão de ferramenta e operação no fim.

### Já uso Terraform, quero fechar as lacunas

03 (state/backend/locking, o que mais gera incidente em time) → 05 (a estratégia de ambientes que de fato vence — diretórios, não workspaces — e CI com plan/apply separados) → 06 (a árvore de decisão contra CloudFormation/CDK/Pulumi, e os anti-padrões).

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Cloud/16 - Infrastructure as Code" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/15 - Arquiteturas serverless e event-driven/index|Arquiteturas serverless e event-driven]] — Galho 15, a arquitetura de referência que o capstone deste galho decompõe em módulos
- [[03-Dominios/Engenharia/Operação/index|Operação]] — GitOps, pipelines de CI/CD e platform engineering, a camada de processo em torno do que este galho provisiona
