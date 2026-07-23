---
title: "Roadmap — Armazenamento (object, block e file)"
created: 2026-07-23
updated: 2026-07-23
type: meta
publish: false
tags:
  - meta
  - roadmap
  - cloud
---

# Roadmap — Armazenamento (object, block e file) (galho 8)

Roadmap-folha do galho `Cloud/08 - Armazenamento (object, block e file)`. Bloco 2 (Os primitivos). Spec: [[00-Meta/specs/2026-07-20-trilha-cloud-design]].

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

#### 01 - Os três tipos de armazenamento
- **Estado:** ✅ feita · fase: Iniciado · 278 linhas
- **Escopo:** o mapa do galho — object vs block vs file, eixo de decisão (quem acessa/semântica/latência/custo), 3 analogias (guarda-volumes, HD USB, pasta de rede), cenário com os 3 convivendo, honestidade DO (sem file storage gerenciado), e "por baixo de quase todo serviço gerenciado é um destes três" (bancos→block, data lake→object, snapshots→object).

#### 02 - Object storage a fundo
- **Estado:** ✅ feita · fase: Adepto · 402 linhas
- **Escopo:** anatomia objeto/chave/metadados/version-id, namespace plano (pasta é ilusão de prefixo), bucket global-único preso a região, durabilidade 11 noves (≥3 AZs), strong read-after-write (dez/2020), API REST, presigned URLs, limites (5 GB single-PUT, 5 TB objeto), multipart, Block Public Access; S3 ↔ Spaces (API-compatível, CDN embutido).

#### 03 - Classes de acesso e lifecycle
- **Estado:** ✅ feita · fase: Adepto · 393 linhas
- **Escopo:** classes S3 (Standard/IA/One Zone-IA/Intelligent-Tiering/Glacier IR/Flexible/Deep Archive), trade-off custo-storage↓ vs custo/latência-retrieval↑ + mínimos, lifecycle policies (transição por idade, expirar versões, limpar multipart), breakeven ilustrativo; Spaces preço único (Standard+Cold), Azure/GCP têm tiers análogos.

#### 04 - Versioning, durabilidade e proteção
- **Estado:** ✅ feita · fase: Adepto · 396 linhas
- **Escopo:** 11 noves protegem hardware, não erro humano/ransomware; versioning + delete markers + restaurar, durabilidade vs disponibilidade, replication (CRR/SRR, exige versioning), Object Lock/WORM (Governance vs Compliance, esta IRREVERSÍVEL), MFA delete; Spaces não versiona, Azure/GCP têm.

#### 05 - Block storage — EBS e Volumes
- **Estado:** ✅ feita · fase: Adepto · 481 linhas
- **Escopo:** o disco da VM a fundo — volume raiz vs dados, tipos (gp3 default/gp2 burst/io1-io2 provisionado/st1-sc1 HDD), IOPS+throughput, snapshots incrementais (guardados em object storage, cobram delta), Elastic Volumes sem downtime, Multi-Attach (io2, exceção à regra 1-por-instância), DeleteOnTermination, encryption KMS; EBS ↔ Volumes (DO 1 tipo SSD).

#### 06 - File storage e a escolha do armazenamento
- **Estado:** ✅ feita · fase: Magus · 428 linhas · **FECHA o galho**
- **Escopo:** EFS (NFS gerenciado multi-AZ, modos General Purpose/Elastic-Bursting-Provisioned, storage classes + lifecycle, Access Points), FSx de raspão, Max I/O legado; ausência de file storage gerenciado na DO (NFS auto-operado) como critério de escolha; árvore de decisão consolidada dos 3 tipos + cenário end-to-end + tabela-síntese; ponte para galho 9 (Bancos gerenciados). Capstone.

---

## Pendências

- **M1 (mídia):** enriquecimento de vídeos/podcasts ainda não rodado neste galho — pendente para sessão futura.

## Notas de execução

- Escrito em 2 ondas de 3 agentes (01-03, depois 04-06); orquestrador commitou serialmente (`716b234`, `2482ed9`). 0 wikilinks quebrados no gate.
- Nota 01 (mapa/síntese, Iniciado) reaberta 1x (258→278) SEM padding: seção "por baixo de todo serviço gerenciado é um destes três" (EBS snapshots armazenados em object storage confirmado por fetch). Topou em 278 <300 — aceito como nota-mapa.
- Nota 05 (mecânica) fechou 481, bem acima do piso Adepto — código real (13 blocos) fecha fácil, confirmando o contraste mecânica-vs-critério das ondas anteriores.
- Capstone (06) fechou 428 — a 2 linhas da banda 430-500, densidade estrutural completa (síntese, sem padding); aceito.
- Correções/honestidade factual da escrita: pricing AWS S3 renderiza via JS (WebFetch não extrai $/GB) → nota 03 usa custo relativo/ordinal + [!info] calculadora; Spaces não tem versioning (nota 04) nem file storage gerenciado (notas 01/06); gp3 é default de console e desacopla IOPS do tamanho (nota 05); EFS Max I/O é modo legado (nota 06); Object Lock Compliance é irreversível (nota 04).
- Fronteiras respeitadas: durabilidade conceitual → System Design; bancos gerenciados → galho 9 (não existe, mencionado em prosa); KMS a fundo → galho 18; backup como disciplina → Operação.
