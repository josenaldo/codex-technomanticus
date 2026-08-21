---
title: "Cloud — Segurança na cloud a fundo"
created: 2026-07-24
updated: 2026-07-24
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - seguranca
  - kms
  - compliance
aliases:
  - "Segurança na cloud a fundo"
  - "Galho 18 - Segurança na cloud a fundo"
---

# Segurança na cloud a fundo

> [!abstract] TL;DR
> Galho 18 da trilha Cloud, Bloco 4. As dezessete notas anteriores já mencionaram IAM, security groups, criptografia em repouso — mas sempre de raspão, como pré-requisito de outra coisa. Este galho para e olha só para segurança: primeiro a **responsabilidade compartilhada na prática** (onde a linha realmente cai, e por que quase todo vazamento noticiado é 100% culpa do lado do cliente), depois **criptografia gerenciada** (KMS, envelope encryption, o cofre que nunca entrega a chave em texto puro), depois **segredos** (Secrets Manager vs Parameter Store, rotação automática), depois **rede e perímetro** (defesa em profundidade, PrivateLink, acesso administrativo sem porta aberta), depois **governança em escala** (SCP, CloudTrail, Config, GuardDuty — o teto organizacional e o rastro de auditoria), e fecha com um **threat model completo** sobre a arquitetura de referência do galho 15. 6 notas, 3 fases, lente dupla AWS ↔ DigitalOcean.

## Sobre este galho

Segurança na nuvem não é um serviço que se liga com um clique — é uma disciplina que atravessa cada camada já vista na trilha, agora examinada com a pergunta certa: *o que pode dar errado aqui, e o que impede isso de acontecer?* Este galho não reintroduz IAM, VPC ou security groups do zero — ele assume que o leitor já os viu (galhos 4 e 7) e foca no que ainda falta: onde exatamente termina a responsabilidade do provedor e começa a sua, como proteger dado em repouso sem virar você mesmo o alvo, onde um segredo de aplicação pode (e não pode) morar, como transformar "configurei certo hoje" em "sei que continua certo daqui a seis meses", e como montar, peça por peça, o modelo de ameaças de um sistema real.

O fio condutor sobe de uma conta só para muitas contas e muito tempo. Primeiro o *modelo mental* — a responsabilidade compartilhada com números reais (quase todo incidente é configuração, não hack sofisticado). Depois a *mecânica de proteção de dados* em duas notas: criptografia gerenciada via KMS (envelope encryption, chaves AWS-managed vs customer-managed) e segredos de aplicação via Secrets Manager/Parameter Store (rotação automática vs cifra sem rotação). Depois o *perímetro*: defesa em profundidade da borda até a aplicação, conectividade privada (PrivateLink) e acesso administrativo sem porta aberta (Session Manager). Depois a *governança em escala*: Service Control Policies como teto organizacional, CloudTrail como log imutável, Config como compliance-como-código, GuardDuty como detecção por ML. E por fim o *capstone*: um threat model completo sobre a arquitetura serverless de referência, com least privilege como fio condutor único.

**Audiência primária:** quem já configurou IAM, security group e um bucket privado seguindo tutorial, mas nunca formalizou *por que* essas escolhas seguram um ataque real, nem sabe onde fica a fronteira entre "o provedor garante" e "eu garanto". **Audiência secundária:** quem já opera em produção mas nunca institucionalizou auditoria (CloudTrail/Config) além do básico, ou nunca fez um threat model explícito de uma arquitetura própria.

> [!info] Fronteira
> **IAM básico** (usuários, roles, políticas) é o [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Galho 4]]; **VPC e segurança de rede fundamental** (subnets, security groups, NACLs) é o [[03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)/index|Galho 7]]; **borda e CDN** (WAF, Shield, DNS) é o [[03-Dominios/Tecnologia/Cloud/10 - DNS, CDN e borda/index|Galho 10]]; **conceitos gerais de autenticação/autorização** (OAuth, OIDC, RBAC) vivem em [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]]; **FinOps** (custo dos controles de segurança) é o Galho 19. Este galho trata o que fica *além* desses fundamentos — criptografia gerenciada, segredos, defesa em profundidade aplicada, governança em escala e threat modeling — e linka essas fronteiras em vez de reexplicá-las.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/18 - Segurança na cloud a fundo/01 - Responsabilidade compartilhada na prática|01 — Responsabilidade compartilhada na prática]] — security *of* the cloud vs security *in* the cloud com números reais, a linha se movendo por tipo de serviço (IaaS exige mais, serverless menos, mas nunca zero), por que a maioria dos vazamentos noticiados é configuração errada do lado do cliente.

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/18 - Segurança na cloud a fundo/02 - Criptografia gerenciada (KMS)|02 — Criptografia gerenciada (KMS)]] — por que o KMS não criptografa seus dados diretamente, envelope encryption (chave de dados descartável + chave-mestra), tipos de chave (AWS managed vs customer managed vs BYOK), key policies, integração nativa com S3/EBS/RDS; DO cifra em repouso por padrão mas sem KMS gerenciado.
3. [[03-Dominios/Tecnologia/Cloud/18 - Segurança na cloud a fundo/03 - Segredos — Secrets Manager e Parameter Store|03 — Segredos — Secrets Manager e Parameter Store]] — onde um segredo NÃO pode morar (código, env var em texto puro, state do Terraform), Secrets Manager com rotação automática embutida, SSM Parameter Store como irmão mais barato sem rotação, injeção em Lambda/ECS; DO cifra env vars sem rotação gerenciada.
4. [[03-Dominios/Tecnologia/Cloud/18 - Segurança na cloud a fundo/04 - Segurança de rede e perímetro|04 — Segurança de rede e perímetro]] — defesa em profundidade camada por camada (borda → VPC → subnet → instância → aplicação), conectividade privada via VPC endpoints/PrivateLink, acesso administrativo sem porta aberta (SSM Session Manager), zero-trust de raspão; DO cobre o essencial mas sem PrivateLink nem Session Manager.
5. [[03-Dominios/Tecnologia/Cloud/18 - Segurança na cloud a fundo/05 - Governança, auditoria e compliance|05 — Governança, auditoria e compliance]] — Service Control Policies como teto organizacional, CloudTrail como log imutável de toda chamada de API, AWS Config como compliance-como-código, GuardDuty como detecção por ML, e um modelo de ameaças cloud-nativo (credencial vazada, bucket público, escalação de privilégio, SSRF contra metadata); DO com catálogo bem mais enxuto aqui.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/18 - Segurança na cloud a fundo/06 - Threat model de uma arquitetura cloud (capstone)|06 — Threat model de uma arquitetura cloud (capstone)]] — pega a arquitetura serverless de referência do galho 15 e sobrepõe cada camada deste galho (IAM em cada seta, KMS no estado, Secrets Manager nas credenciais, WAF na borda, CloudTrail auditando tudo), threat model peça por peça, STRIDE de raspão, least privilege como fio condutor único, anti-padrões a evitar. Capstone do galho.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — do modelo mental à proteção de dados, ao perímetro, à governança em escala, e ao threat model completo no fim.

### Já opero em produção, quero fechar as lacunas de auditoria

01 (relembrar onde cai a linha da sua responsabilidade) → 05 (CloudTrail, Config, GuardDuty — o que falta institucionalizar) → 06 (o exercício de threat model que amarra tudo).

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Identidade e acesso (IAM)]] — Galho 4, o IAM básico que este galho aprofunda em least privilege e SCP
- [[03-Dominios/Tecnologia/Cloud/10 - DNS, CDN e borda/index|DNS, CDN e borda]] — Galho 10, o WAF e Shield que a defesa em profundidade deste galho retoma na borda
- [[03-Dominios/Engenharia/Auth e Identidade/index|Auth e Identidade]] — o conceito geral de autenticação/autorização que o IAM da nuvem implementa
