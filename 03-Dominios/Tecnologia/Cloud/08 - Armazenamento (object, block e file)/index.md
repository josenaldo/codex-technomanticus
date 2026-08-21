---
title: "Cloud — Armazenamento (object, block e file)"
created: 2026-07-23
updated: 2026-07-23
type: moc
status: growing
publish: true
tags:
  - cloud
  - moc
  - armazenamento
  - storage
aliases:
  - "Armazenamento (object, block e file)"
  - "Galho 8 - Armazenamento"
---

# Armazenamento (object, block e file)

> [!abstract] TL;DR
> Galho 8 da trilha Cloud, Bloco 2 (Os primitivos). "Guardar dados na nuvem" não é uma frase com um único significado: há três formatos fundamentais, cada um com um contrato de acesso diferente. **Object storage** (S3/Spaces) guarda objetos imutáveis sob uma chave num namespace plano, acessados por API HTTP, com escala infinita e durabilidade de 11 noves. **Block storage** (EBS/Volumes) é o disco bruto dedicado a uma instância — o "HD" da VM dos galhos 5-6. **File storage** (EFS) é o filesystem de rede NFS que muitas instâncias montam ao mesmo tempo. O galho abre o mapa dos três, mergulha no object storage (anatomia, classes de custo, proteção), depois no block storage (tipos, IOPS, snapshots), e fecha com o file storage e a grande decisão de qual usar em cada camada. 6 notas, 3 fases, lente dupla AWS ↔ DigitalOcean.

## Sobre este galho

Os galhos 5 e 6 subiram instâncias e uma frota elástica; o galho 7 desenhou a rede onde tudo isso vive. Mas nenhum deles perguntou onde os *dados* ficam — o disco de boot foi tratado como um detalhe da VM, e o banco de dados como um problema para depois. Este galho responde: quando você guarda dados na nuvem, guarda em qual dos três formatos, e por quê.

O fio condutor vai do mapa ao detalhe e volta à decisão. Primeiro o *mapa* dos três tipos e o eixo que os separa (quem acessa, com que semântica, a que custo). Depois o *object storage* aberto em três notas — a anatomia (buckets, chaves, durabilidade), a economia (classes de acesso e lifecycle, onde a fatura explode ou encolhe) e a proteção (versioning, replication, object lock — porque 11 noves não protegem de um `delete` acidental). Depois o *block storage* — os tipos de volume, IOPS provisionado, snapshots, e a ligação com o ciclo de vida da instância do galho 5. E por fim o *file storage* e a síntese: dado um requisito real, qual dos três primitivos é a escolha certa em cada camada de uma arquitetura.

**Audiência primária:** quem sobe recursos na nuvem mas ainda escolhe o armazenamento "por hábito" (tudo em S3, ou tudo no disco da VM) e precisa decidir com intenção. **Audiência secundária:** quem já usa os três mas nunca formalizou por que object storage não é um filesystem, por que o versioning pode explodir a conta, ou a diferença exata que toda entrevista cobra entre object, block e file.

> [!info] Fronteira
> A durabilidade e a replicação como **conceitos distribuídos** (quóruns, consistência vs disponibilidade) vivem em [[03-Dominios/Engenharia/Arquitetura/index|System Design]]; o armazenamento como **motor de um banco de dados gerenciado** é o galho 9 (Bancos gerenciados) e o domínio [[03-Dominios/Engenharia/Dados/index|Dados]]; **backup como disciplina de operação** é [[03-Dominios/Engenharia/Operação/index|Operação]]. Este galho trata o armazenamento como recurso de infraestrutura bruto — o primitivo sobre o qual essas camadas mais altas se apoiam.

## Iniciado

1. [[03-Dominios/Tecnologia/Cloud/08 - Armazenamento (object, block e file)/01 - Os três tipos de armazenamento|01 — Os três tipos de armazenamento]] — object vs block vs file, o eixo de decisão (quem acessa, semântica, custo), as três analogias, e por baixo de quase todo serviço gerenciado é um destes três.

## Adepto

2. [[03-Dominios/Tecnologia/Cloud/08 - Armazenamento (object, block e file)/02 - Object storage a fundo|02 — Object storage a fundo]] — anatomia bucket/chave/objeto, namespace plano, durabilidade de 11 noves, strong consistency, multipart, presigned URLs, Block Public Access; S3 ↔ Spaces.
3. [[03-Dominios/Tecnologia/Cloud/08 - Armazenamento (object, block e file)/03 - Classes de acesso e lifecycle|03 — Classes de acesso e lifecycle]] — Standard/IA/Intelligent-Tiering/Glacier, o trade-off custo-de-storage vs custo-de-retrieval, lifecycle policies, a fatura que explode; Spaces tem preço único.
4. [[03-Dominios/Tecnologia/Cloud/08 - Armazenamento (object, block e file)/04 - Versioning, durabilidade e proteção|04 — Versioning, durabilidade e proteção]] — 11 noves não salvam de erro humano: versioning, delete markers, replication (CRR/SRR), Object Lock (WORM), MFA delete; Spaces não versiona.
5. [[03-Dominios/Tecnologia/Cloud/08 - Armazenamento (object, block e file)/05 - Block storage — EBS e Volumes|05 — Block storage — EBS e Volumes]] — o disco da VM a fundo: tipos de volume (gp3/io2/st1/sc1), IOPS e throughput, snapshots incrementais (guardados em object storage), Elastic Volumes, ciclo de vida; EBS ↔ Volumes.

## Magus

6. [[03-Dominios/Tecnologia/Cloud/08 - Armazenamento (object, block e file)/06 - File storage e a escolha do armazenamento|06 — File storage e a escolha do armazenamento]] — EFS (NFS gerenciado multi-AZ, modos de performance/throughput, lifecycle), FSx de raspão, a ausência de file storage gerenciado na DO, e a árvore de decisão consolidada dos três tipos. Capstone do galho e ponte para os bancos gerenciados.

## Rotas alternativas

### Completa

01 → 02 → 03 → 04 → 05 → 06. Percurso linear — o mapa, depois object storage em profundidade, depois block storage, e a síntese decisória no fim.

### Já uso S3/Volumes, quero fechar as lacunas de fato

03 (por que a fatura do object storage cresce e como lifecycle a controla) → 04 (por que versioning e Object Lock existem, e a pegadinha de custo) → 06 (a árvore de decisão que separa object, block e file sem hesitar em entrevista).

## Veja também

- [[03-Dominios/Tecnologia/Cloud/index|Cloud]] (MOC do domínio)
- [[03-Dominios/Tecnologia/Cloud/07 - Rede na nuvem (VPC)/index|Rede na nuvem (VPC)]] — Galho 7, a rede onde as instâncias que consomem esse armazenamento vivem
- [[03-Dominios/Tecnologia/Cloud/05 - Compute I — máquinas virtuais/index|Compute I — máquinas virtuais]] — Galho 5, de onde vem o disco de boot que a nota 05 abre como block storage
- [[03-Dominios/Tecnologia/Cloud/04 - Identidade e acesso (IAM)/index|Identidade e acesso (IAM)]] — Galho 4, quem controla o acesso a buckets e volumes
- [[03-Dominios/Engenharia/Arquitetura/index|System Design]] — os conceitos distribuídos de durabilidade e replicação que este armazenamento encarna
