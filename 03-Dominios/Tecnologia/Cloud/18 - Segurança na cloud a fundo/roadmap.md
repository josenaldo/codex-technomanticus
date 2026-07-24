---
title: "Roadmap — Segurança na cloud a fundo"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Segurança na cloud a fundo (galho 18)

Roadmap-folha do galho `Cloud/18 - Segurança na cloud a fundo`. Bloco 4. Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - Responsabilidade compartilhada na prática
- **Estado:** ✅ feita · fase: Iniciado · 185 linhas
- **Escopo:** security *of* the cloud vs security *in* the cloud, retomando o modelo do galho 2 agora com as mãos na massa; a linha se movendo conforme o tipo de serviço (IaaS exige mais do cliente, serverless menos, nunca zero); a ilusão "está na nuvem, logo é seguro" desmontada em números (bucket público, security group aberto, credencial vazada — quase sempre 100% culpa do cliente); mapa do restante do galho; nomenclatura entre provedores.

#### 02 - Criptografia gerenciada (KMS)
- **Estado:** ✅ feita · fase: Adepto · 291 linhas
- **Escopo:** por que o KMS não criptografa dados diretamente, envelope encryption (chave de dados descartável cifrada por chave-mestra), tipos de chave (AWS managed vs customer managed vs BYOK), o que rotaciona de fato, integração nativa com S3/EBS/RDS como o ponto forte, exemplo de ponta a ponta, key policies, quando vale subir pra customer managed, recursos avançados (multi-region keys, grants) de raspão; DO cifra em repouso por padrão em vários produtos mas sem KMS gerenciado com granularidade de política/BYOK — lacuna real; tabela de tradução Azure/GCP.

#### 03 - Segredos — Secrets Manager e Parameter Store
- **Estado:** ✅ feita · fase: Adepto · 295 linhas
- **Escopo:** onde um segredo NÃO pode morar (código, env var em texto puro, state do Terraform); Secrets Manager como cofre com rotação embutida (troca senha no RDS e no cofre no mesmo golpe, sem downtime), cifrado por KMS (fronteira→nota 02); SSM Parameter Store como irmão mais barato, `SecureString` cifrado mas sem rotação automática; injeção em Lambda e ECS; os comandos de uso; por que rotacionar afinal; AWS Secrets Manager vs DigitalOcean (App Platform cifra env vars, sem rotação gerenciada — paridade quebra de verdade aqui).

#### 04 - Segurança de rede e perímetro
- **Estado:** ✅ feita · fase: Adepto · 274 linhas
- **Escopo:** cada camada de segurança sozinha mente sobre estar segura; defesa em profundidade como regra que organiza tudo (borda/WAF-Shield → VPC → subnet/NACL → instância/security group → aplicação/IAM), retomando VPC (galho 7) e borda (galho 10) sob a lente de superfície de ataque; conectividade privada via VPC endpoints/PrivateLink como controle de segurança (não só de custo); matar o SSH exposto via SSM Session Manager (acesso administrativo sem porta aberta); zero-trust de raspão; fechando uma arquitetura de três camadas; armadilhas; DO cobre o essencial (Cloud Firewall, VPC) mas sem PrivateLink, Network Firewall gerenciado nem substituto do Session Manager.

#### 05 - Governança, auditoria e compliance
- **Estado:** ✅ feita · fase: Adepto · 318 linhas
- **Escopo:** o problema de muitas contas/muita gente/muito tempo (vs. as notas anteriores, que resolviam problemas de uma conta só); Service Control Policies como teto organizacional que nenhuma política individual fura; CloudTrail como log imutável — "quem fez o quê, quando"; AWS Config transformando "configuração correta" em regra que roda sozinha (compliance como código, não checklist); GuardDuty, Security Hub e Inspector de raspão (detecção por ML); a nuvem como facilitadora de compliance, não certificado automático; modelo de ameaças cloud-nativo (credencial vazada, bucket público, escalação de privilégio, SSRF contra metadata do servidor) com a defesa específica de cada uma; tabela de tradução Azure/GCP; casos práticos; armadilhas comuns; DO com catálogo bem mais enxuto (log de atividade básico, sem SCP, sem ML, sem agregador de postura).

#### 06 - Threat model de uma arquitetura cloud (capstone)
- **Estado:** ✅ feita · fase: Magus · 176 linhas · **FECHA o galho**
- **Escopo:** segurança como pergunta feita sobre cada seta do diagrama de arquitetura, não como serviço que se liga; pega a arquitetura serverless de referência do galho 15 sob a lupa e sobrepõe cada camada deste galho (IAM em cada seta, KMS no estado, Secrets Manager nas credenciais, WAF na borda, CloudTrail auditando tudo); threat model peça por peça; STRIDE de raspão; least privilege como fio condutor único (cada permissão concedida é superfície de ataque); anti-padrões que este capstone existe para evitar; ponte pro galho 19 (FinOps) — segurança e custo não são inimigos, mas exigem a mesma disciplina de olhar componente por componente. Capstone do galho.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Galho fechado com as 6 notas já escritas no repositório antes deste roadmap ser gerado; roadmap redigido em modo retroativo (audit-only), sem tocar nas notas de conteúdo.
- Fronteiras explícitas confirmadas nas próprias notas: IAM básico e VPC/security groups → galhos 4 e 7; borda/WAF/Shield → galho 10; conceito geral de auth → Engenharia/Auth e Identidade; FinOps (custo dos controles) → galho 19 (prosa, galho ainda não existe no momento deste roadmap).
- Densidade das notas na banda esperada para Adepto (274-318 linhas) e Iniciado (185); capstone mais enxuto (176 linhas) mas denso — síntese aplicada sobre arquitetura já existente (galho 15), não introdução de conceito novo.
- Paridade DigitalOcean capturada consistentemente: sem KMS gerenciado dedicado (nota 02), sem rotação gerenciada de segredos (nota 03), sem PrivateLink/Session Manager (nota 04), catálogo de governança bem mais enxuto — sem SCP, sem detecção por ML (nota 05).
