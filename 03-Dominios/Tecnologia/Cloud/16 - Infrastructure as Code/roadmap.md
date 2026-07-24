---
title: "Roadmap — Infrastructure as Code"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Infrastructure as Code (galho 16)

Roadmap-folha do galho `Cloud/16 - Infrastructure as Code`. Bloco 4 (operar, sustentar, governar) — **galho que abre o bloco**. Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - Por que Infrastructure as Code
- **Estado:** ✅ feita · fase: Iniciado · 197 linhas
- **Escopo:** o problema do ClickOps a partir do capstone serverless do Bloco 3 (reconstruir de clique é insustentável), os quatro pecados (drift silencioso, snowflake servers, sem code review, conhecimento tribal), o que IaC entrega (reprodutibilidade, versionamento real, code review, plan antes de aplicar, documentação viva, ambientes idênticos), declarativo vs. imperativo com idempotência, exemplo concreto (fila/Droplet) mostrando a forma sintática `resource "<tipo>" "<nome>"`, panorama das ferramentas (Terraform/OpenTofu/CloudFormation/CDK/Pulumi/doctl) em tabela, fronteira com Operação (GitOps/CI fica lá); Terraform ↔ DO (sem fila gerenciada nativa — SQS não tem par 1:1, licença BSL/OpenTofu verificado 2026-07-24).

#### 02 - Terraform a fundo
- **Estado:** ✅ feita · fase: Adepto · 437 linhas · nota mais longa do galho
- **Escopo:** HCL e os seis tipos de bloco (`terraform`, `provider`, `resource`, `data`, `variable`, `output`) + `locals`, anatomia do `resource "<tipo>" "<nome_local>"`, o ciclo `init`→`plan`→`apply`→`destroy` com exemplo de diff real (`+`/`~`/`-`), providers AWS e DigitalOcean lado a lado (`aws_instance`↔`digitalocean_droplet`, `aws_security_group`↔`digitalocean_firewall`), multi-provider no mesmo config, tabela de tradução Azure/GCP, grafo de dependências (implícita vs. `depends_on`), `lifecycle` (`create_before_destroy`, `prevent_destroy`, `ignore_changes`), `count` vs. `for_each` (diferença na hora de remover item do meio), funções embutidas, OpenTofu (fork pós-BUSL, verificado 2026-07-24), variables/outputs com expressão ternária e splat.

#### 03 - State, backends e colaboração
- **Estado:** ✅ feita · fase: Adepto · 276 linhas
- **Escopo:** por que o Terraform precisa do state (mapear código → ID real na nuvem), os dois riscos (segredos em texto puro, dessincronização), regra "nunca commitar .tfstate", local state (funciona sozinho, quebra em equipe), remote state como fonte única de verdade, state locking (sequência Dev A/Dev B com lock DynamoDB), lente dupla backend S3+DynamoDB/`use_lockfile` (verificado 2026-07-24: DynamoDB deprecated) ↔ Spaces S3-compatível (sem garantia documentada de lock) ↔ Terraform Cloud gerenciado em tabela comparativa, `terraform_remote_state` para consumir state de outro projeto, drift (detecção via `plan`/refresh), `terraform import` (só popula state, não escreve o `.tf`; import blocks como via recomendada), `terraform state mv`, workspaces (por que não servem para isolar dev/stage/prod — citação direta da doc HashiCorp), armadilhas comuns.

#### 04 - IaC nativo — CloudFormation e CDK
- **Estado:** ✅ feita · fase: Adepto · 246 linhas
- **Escopo:** templates YAML/JSON e stacks como entidade real na conta AWS, intrinsic functions (`!Ref`, `!GetAtt`, `!Sub`, `!Join`), change sets como o "terraform plan" da AWS (create/describe/execute-change-set), rollback automático por padrão (vs. Terraform que não reverte sozinho) e drift detection sob demanda, nested stacks (análogo a módulos) e StackSets (multi-conta/região, sem equivalente nativo no Terraform), SAM como transform que expande `AWS::Serverless::Function`, CDK (infraestrutura em linguagem de programação real — TS/Python/Java/C#/Go — compilando para CloudFormation via `cdk synth`, constructs de alto nível, Pulumi como par multi-cloud), tabela comparativa de quando vale cada um, tabela de tradução Azure/GCP; honestidade sobre a DO não ter equivalente nativo (só provider Terraform).

#### 05 - Módulos, ambientes e boas práticas
- **Estado:** ✅ feita · fase: Adepto · 326 linhas
- **Escopo:** módulos como unidade de reuso (inputs/outputs, analogia com função), fontes de módulo (local/Registry público/Git/registry privado) com pin de versão, múltiplos ambientes — workspaces (por que a doc oficial desaconselha para dev/stage/prod), diretórios separados + módulos compartilhados (o "padrão de fato"), Terragrunt (camada de conveniência para boilerplate residual) — em tabela comparativa; segredos nunca no `.tf` (três camadas: nunca literal, `.tfvars` fora do Git, cofre em runtime via Secrets Manager/Vault) com exemplo errado/certo; CI com `plan` no PR e `apply` no merge em pipelines separados, credenciais OIDC de curta duração; testing de raspão (`terraform validate`, tflint, Checkov); boas práticas (least privilege, tagging, naming, remote state por ambiente, recursos órfãos); lente dupla estrutura multi-ambiente AWS/DO; exemplo completo de módulo + pipeline GitHub Actions.

#### 06 - Escolher e operar IaC (capstone)
- **Estado:** ✅ feita · fase: Magus · 332 linhas · **FECHA o galho, ABRE o Bloco 4**
- **Escopo:** árvore de decisão de três perguntas (só AWS ou multi-cloud? lógica real ou declaração estática? aceita gerenciar state?) entre Terraform/CloudFormation-SAM/CDK/Pulumi, tabela comparativa completa (modelo, state, linguagem, lock-in, curva, multi-cloud, ecossistema), tabela de tradução Azure/GCP, três estágios de maturidade operacional (laptop solo → CI+módulos → plataforma interna self-service), custo de trocar de ferramenta depois (`terraform import` é trabalho manual recurso a recurso; caminho inverso ainda menos rodado), aplicação da árvore na arquitetura serverless de referência do Bloco 3 decomposta em 4 módulos (api/orquestração/mensageria/dados) com exemplo de root module e um módulo (`mensageria`) aberto por dentro mostrando interface pequena e estável, os cinco anti-padrões mais caros (state local commitado, apply sem plan revisado, mono-state gigante, secrets no código, drift ignorado) com checagem via `.gitignore`/`git grep`, e por que IaC é fundação — não conveniência — para observabilidade/segurança/resiliência do resto do Bloco 4. Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Galho recebido já escrito (6 notas, 1814 linhas totais) — este roadmap foi gerado a partir da leitura integral das notas existentes, sem reescrita de conteúdo.
- Fronteiras explícitas no galho: GitOps/pipelines/platform engineering → Operação (nota 01, nota 05, nota 06); observabilidade/segurança/resiliência → próximos galhos do Bloco 4 (nota 06, seção final "Por que isto é fundação").
- Contraste de tamanho: nota 02 (mecânica pura de Terraform, 437 linhas) é a mais longa do galho — consistente com o padrão observado em outros galhos da trilha (notas de mecânica fecham mais alto que notas de síntese). Nota 01 (abertura/panorama, 197 linhas) é a mais curta, abaixo do piso de Iniciado, mas cobre o escopo completo (4 pecados, declarativo/imperativo, panorama de ferramentas) sem padding aparente.
- Achados factuais capturados com callout `[!info]` e data de verificação (2026-07-24): licença BSL do Terraform + fork OpenTofu (nota 01, nota 02); DynamoDB locking deprecated em favor de `use_lockfile` no backend S3 (nota 03); rollback automático como comportamento default do CloudFormation (nota 04); import blocks como via recomendada sobre `terraform import` (nota 03).
- Honestidade de paridade DO mantida em todas as notas: sem fila gerenciada nativa (nota 01), sem equivalente a CloudFormation/StackSets (nota 04, nota 06), Spaces sem garantia documentada de locking nativo equivalente ao DynamoDB (nota 03) — a árvore de decisão do capstone (nota 06) colapsa para Terraform sempre que a DO está no jogo.
- Capstone (06, 332 linhas) fecha com aplicação prática da arquitetura de referência do Bloco 3 decomposta em módulos Terraform — ponte explícita de volta ao galho 15 e adiante para o próximo galho (Observabilidade).
