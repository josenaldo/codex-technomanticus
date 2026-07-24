---
title: "Roadmap — AWS a fundo (consolidação)"
created: 2026-07-24
updated: 2026-07-24
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — AWS a fundo (galho 21)

Roadmap-folha do galho `Cloud/21 - AWS a fundo`. Bloco 5 (Provedores e maestria) — **galho que abre o bloco**. Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - A filosofia da amplitude
- **Estado:** ✅ feita · fase: Magus · 227 linhas
- **Escopo:** o "susto do console" (ansiedade de amplitude), primitivo componível vs. plataforma opinada (S3/SQS/Lambda burros entre si vs. App Platform já decidido), "tudo é uma API primeiro" (memorando de Bezos de 2002, folclore via Steve Yegge — marcado com honestidade de fonte), working backwards (PR/FAQ) e o two-pizza team como as três engrenagens que multiplicam o catálogo, mapa de camadas de abstração (infra crua → primitivos gerenciados → orquestração → soluções verticais), lente dupla AWS (200+ serviços, whitepaper oficial) vs DigitalOcean (~8 categorias core), caso prático de upload de foto de perfil composto em 5 primitivos, o preço da amplitude (paradoxo da escolha de Barry Schwartz, curva de aprendizado, 5 formas de fazer a mesma coisa), e o contraponto — amplitude também é vantagem em requisitos regulatórios pesados, com a fractalidade do próprio S3 (8→300+ microsserviços internos) como ilustração.

#### 02 - Sinal e ruído no catálogo
- **Estado:** ✅ feita · fase: Magus · 197 linhas
- **Escopo:** a analogia do vocabulário ativo vs. passivo (2-3 mil palavras cobrem o cotidiano de um idioma de 300 mil), o núcleo de ~25 serviços em 8 categorias (Compute, Storage, Rede, Dados, Integração, Operação) com tabela de referência linkando de volta aos galhos 4-19 da trilha, os quatro sinais de ruído (nome de marketing sobre primitivo conhecido, duplicação "com IA"/"mais mágica", descontinuado/modo manutenção, nicho de cliente enterprise) com árvore de decisão, framework de avaliação rápida de 4 perguntas (qual primitivo encapsula, qual o lock-in, existe alternativa mais simples, GA ou preview), caso prático fictício ("Amazon ProductGenius") aplicando o framework passo a passo, a lente DO como "o núcleo, pré-filtrado" com tabela de tradução AWS/Azure/GCP/DO, e o alerta de cargo-culting arquitetural (over-engineering por copiar palestra de re:Invent fora de escala).

#### 03 - Operar a AWS — console, CLI, SDK e IaC
- **Estado:** ✅ feita · fase: Adepto · 335 linhas
- **Escopo:** as quatro portas pra mesma API de controle (console/CLI/SDK/IaC) com diagrama; console pra explorar/aprender/depurar e o antipadrão ClickOps; CLI como ferramenta do dia a dia — `aws configure` clássico vs. perfis nomeados vs. o caminho recomendado com IAM Identity Center/SSO (PKCE desde CLI v2.22.0, `aws sso login`, `aws sts get-caller-identity`), comandos do dia a dia com `--query`/JMESPath; SDK (boto3) para quando o script vira lógica de aplicação; IaC declarativo — CloudFormation nativo vs. CDK (stacks/constructs) vs. Terraform, e quando cada um brilha; a escada de maturidade console→CLI→SDK→IaC; lente dupla DO (`doctl`, token de API pessoal sem SSO federado — lacuna honesta, App Spec YAML como artefato de app inteira) e tabela de tradução Azure/GCP.

#### 04 - Os big rocks que faltaram
- **Estado:** ✅ feita · fase: Adepto · 290 linhas
- **Escopo:** mapa de reconhecimento (não tutorial) dos serviços grandes o bastante pra merecer nome próprio mas fora do escopo dos primitivos 1-20: Cognito (user pools vs identity pools, identidade B2C de fora pra dentro vs. IAM de dentro pra dentro — sem equivalente na DO), Step Functions (Standard vs Express, integrações otimizadas, o padrão `.sync`/Run a Job), Athena e Glue (SQL serverless sobre S3 + Data Catalog — sem equivalente direto na DO), SageMaker vs Bedrock (treinar modelo vs. consumir LLM pronto — DO tem oferta parcial, GenAI/Gradient Platform), os menores (Lambda@Edge/CloudFront Functions, Systems Manager, Cost Explorer, WAF/Shield, EventBridge Pipes, Macie, QuickSight) com tabela-resumo de 14 linhas; framework de decisão "compor primitivo vs. alcançar o big rock" (recorrência, garantia vs conveniência, reuso, caminho de saída/lock-in); cenário composto de ponta a ponta (Cognito→API Gateway→Step Functions→Athena/Glue→Bedrock) com fragmento ASL e comandos CLI; tabela de tradução Azure/GCP.

#### 05 - O jeito AWS de arquitetar
- **Estado:** ✅ feita · fase: Magus · 315 linhas
- **Escopo:** a metáfora da correnteza — sete correntes idiomáticas que a AWS empurra: (1) eventos em vez de chamada síncrona (EventBridge/SNS/SQS, eventos nativos que os serviços já emitem), (2) serverless-first pra carga variável (a lógica econômica de multiplexação de capacidade ociosa), (3) IAM permeando cada interação serviço-a-serviço (sem "confiança implícita" on-prem), (4) multi-AZ como piso e multi-region como exceção cara, (5) múltiplas contas/AWS Organizations como fronteira de blast radius e billing (SCPs, landing zone), (6) tags como espinha dorsal de custo e governança (tabela de tags mínimas), (7) Well-Architected como bússola de "design for failure"; árvore de decisão consolidando as 7 correntes; dois exemplos trabalhados (processar upload de imagem, notificar cliente por múltiplos canais) contrastando "contra a corrente" vs "idiomático"; lente DO como filosofia oposta (menos peças, glue manual); três armadilhas nomeadas (over-engineering serverless em carga constante, multi-conta antes da hora, IAM granular como fricção sem IaC).

#### 06 - Capstone — pensar como arquiteto AWS
- **Estado:** ✅ feita · fase: Magus · 127 linhas · **FECHA o galho**
- **Escopo:** síntese das 5 notas anteriores num parágrafo cada (porquê → o que importa → como opero → o que eu não vi → como componho), checklist mental de 7 perguntas (primitivo certo, gerenciado ou cru, event-driven ou síncrono, IAM desde o desenho, multi-AZ piso/multi-region exceção, spot/serverless pra baratear, qual pilar do WAF está sendo otimizado) com os 6 pilares confirmados (Sustainability desde dez/2021); caso de entrevista de ponta a ponta — desenhar um encurtador de URL — rodando as 7 perguntas com trade-offs verbalizados (DynamoDB, Lambda+API Gateway+CloudFront, IAM por função, multi-AZ nativo, analytics assíncrono via EventBridge) e a variante de pipeline de imagens; fecha com "quando NÃO usar a AWS" — o mesmo problema resolvido num App Platform da DO — e o aviso de que o erro mais caro não é escolher o serviço errado dentro da AWS, é escolher a AWS quando o problema não pedia essa amplitude; ponte pro galho 22 (DigitalOcean a fundo) e recursos externos (Well-Architected Labs, talks de re:Invent).

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Este é o primeiro galho do Bloco 5 (Provedores e maestria) e tem estrutura de fase **não monotônica** com a ordem dos arquivos: notas 01, 02, 05 e 06 são Magus; notas 03 e 04 são Adepto. A leitura recomendada continua sendo a ordem numérica 01→06 (ver "Rotas alternativas: Completa" no index) — a seção Adepto/Magus do MOC agrupa por fase de aprendizado, não repete a ordem narrativa.
- Nota 06 (capstone) já linka pra frente, pro galho 22 (`22 - DigitalOcean a fundo/05 - Quando o DO basta e quando cresce pra AWS`) — esse arquivo de nota existe no diretório do galho 22, mas o galho 22 ainda não tem `index.md` (não fechado); por isso o índice deste galho 21 evita linkar `22 - DigitalOcean a fundo/index` (alvo inexistente) e só menciona o galho 22 em prosa no "Veja também".
- Fronteiras honestas capturadas nas 6 notas: Cognito, Step Functions, Athena/Glue não têm equivalente direto na DigitalOcean (nota 04); IAM Identity Center/SSO com credenciais federadas temporárias não tem equivalente na DO, que usa token de API pessoal (nota 03); AWS Organizations/SCPs não tem equivalente de granularidade comparável — DO tem só Teams (nota 05).
- Achados factuais verificados na data de escrita (2026-07-24): "mais de 200 serviços" é o número oficial do whitepaper AWS (o "~240" citado em blogs/talks é estimativa não-oficial); o memorando de Bezos de 2002 sobre API-first não é documento oficial publicado — vem do relato de Steve Yegge (2011), tratado como folclore de engenharia; os 6 pilares do Well-Architected Framework incluem Sustainability desde dezembro de 2021.
