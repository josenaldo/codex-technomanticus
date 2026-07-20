---
title: "Plano de Execução — Trilha Cloud"
type: spec
created: 2026-07-20
updated: 2026-07-20
status: growing
publish: false
tags:
  - meta
  - spec
  - roadmap
  - cloud
aliases:
  - Plano Trilha Cloud
---

# Plano de Execução — Trilha Cloud

> **Design de origem:** [[2026-07-20-trilha-cloud-design|Design — Trilha Cloud]]. Este plano detalha a construção. A trilha corre em granularidade de **galho** (um por vez, direto na `main`); cada galho é detalhado em notas quando chega a vez dele.

**Objetivo:** Construir o domínio Cloud em `03-Dominios/Tecnologia/Cloud/` — 24 galhos + capstone, notas atômicas em 3 fases, padrão capítulo, espinha conceitual-neutra com lente dupla AWS↔DigitalOcean.

**Arquitetura:** Galhos flat numerados (`01 - ...` a `24 - ...`) sob `Tecnologia/Cloud/`. Cada nota é escrita seguindo `/escrever-nota`, auditada por `/verificar-nota`, commitada. Cada galho tem `index.md` (MOC por fase) e `roadmap.md`. A raiz tem `index.md` (MOC do domínio), `roadmap.md`, `Dicionário.md`, `Biblioteca.md`.

**Execução — subagentes com fan-out controlado:** o orquestrador (esta sessão) fica leve e coordena; a escrita das notas é delegada a **subagentes, ≤3 por rodada** (disciplina da skill `enriquecer-galho`: governança de tokens via ccusage, parada para revisão a cada rodada). Subagentes herdam Sonnet — não forçar Opus para geração de conteúdo. Fan-out massivo via `Workflow` **só com opt-in explícito do usuário**.

**Tech Stack (do vault):** Obsidian Flavored Markdown · skills `/escrever-nota` · `/verificar-nota` · `/enriquecer-nota` · `/diagnosticar-galho` · Mermaid · Dataview.

## Restrições globais (valem para TODA nota)

- **Padrão capítulo:** TL;DR (`[!abstract]`) → abertura-problema (cenário, não "X é...") → mecanismo com ≥1 diagrama Mermaid → casos práticos → armadilhas comuns (`[!warning]`) → "O que vem a seguir" (bridge para a PRÓXIMA nota) → Fontes (com URLs).
- **Registro Feynman:** analogias, perguntas retóricas, resumo em 1 linha; parágrafos curtos; sem padding.
- **Lente dupla AWS↔DO:** o conceito vem primeiro, provider-neutro; depois a encarnação concreta nos dois — *"em AWS é S3, em DO é Spaces"*. AWS = vocabulário-padrão de entrevista; DO = "como eu já faço isso hoje". Nunca abrir uma nota pelo nome do serviço.
- **Tabela de tradução de 4 colunas** (`Conceito · AWS · Azure · GCP · DO`) obrigatória nos galhos de primitivos (blocos 2 e 3); opcional nos demais. Azure/GCP entram **só como tradução** — nunca com passo-a-passo hands-on.
- **Âncora Well-Architected:** todo galho dos blocos 2–5 fecha amarrando explicitamente a ≥1 dos 6 pilares (excelência operacional, segurança, confiabilidade, eficiência de performance, otimização de custo, sustentabilidade).
- **Fronteiras — linkar, não reexplicar:** SRE/deploy/incident → [[03-Dominios/Engenharia/Operação/index|Operação]]; conceitos abstratos de LB/fila/CDN/sharding → [[03-Dominios/Engenharia/Arquitetura/index|System Design]] e [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação]]; OAuth/OIDC → [[03-Dominios/Engenharia/Auth e Identidade/index|Auth]]; K8s a fundo → Infraestrutura/Operação. Usar callout `[!info]` de ponte.
- **Fases:** `fase: Iniciado|Adepto|Magus` no frontmatter. Piso subordinado ao padrão capítulo (Iniciado ~300+ / Adepto ~400+ / Magus ~500+).
- **Caducidade — crítica neste domínio:** preço, nome de serviço, limites e código de exame envelhecem rápido. Toda afirmação datada leva `[!info]` de caducidade com a data de verificação. **Verificar nomes de serviço e códigos de exame no momento da escrita** — não assumir a partir de memória.
- **Frontmatter:** `title`, `type: concept`, `fase`, `tags` (incl. `cloud`, `aws`, `digitalocean`), `publish: true`, `created`/`updated`.
- **Títulos sem `/`** (lição da trilha Go: barra no título vira subpasta no filesystem). Usar `e` ou `vs` no lugar.
- **Subagentes recebem os títulos das notas vizinhas** (lição da Go: agentes alucinam wikilinks de vizinhos que não existem). Nunca deixar o subagente inventar o alvo do bridge.
- **Commits:** um commit por nota (ou por par coeso), **path explícito**, sem assinatura Claude. Push manual.

---

## Fase 0 — Andaime do domínio (antes do galho 1)

### Task 0: Criar a pasta Cloud e os artefatos de domínio

**Files:**
- Create: `03-Dominios/Tecnologia/Cloud/index.md` (MOC do domínio)
- Create: `03-Dominios/Tecnologia/Cloud/roadmap.md` (roadmap-pai)
- Create: `03-Dominios/Tecnologia/Cloud/Dicionário.md` (`type: glossary`)
- Create: `03-Dominios/Tecnologia/Cloud/Biblioteca.md` (`type: reference`)
- Modify: `04-Sendas/Senda Cloud.md`

- [ ] **Passo 1:** Criar `index.md` como MOC do domínio: TL;DR, tabela dos 24 galhos + capstone agrupados nos 5 blocos (com estado ⬜/🟡/✅), seção "Como ler" (ordem dos blocos, e o atalho pra quem já usa DO), Veja também. **Nunca remover este arquivo depois** (regra Quartz).
- [ ] **Passo 2:** Criar `roadmap.md` (galho-pai) via template `00-Meta/templates/Template - Roadmap.md` (modo pai), listando os 24 galhos como sub-galhos ⬜ não diagnosticados.
- [ ] **Passo 3:** Criar `Dicionário.md` semeado com os termos que a trilha vai usar desde o galho 1: region, availability zone, edge location, plano de controle, plano de dados, responsabilidade compartilhada, elasticidade, IaaS/PaaS/FaaS/SaaS, egress, blast radius, right-sizing, lock-in. Ordem alfabética.
- [ ] **Passo 4:** Criar `Biblioteca.md` absorvendo o conteúdo de `04-Sendas/Senda Cloud.md` (AWS Architecture Center, Architecture Blog, Well-Architected, Whitepapers, Training) + acrescentar: DigitalOcean Community Tutorials/Docs, Azure Architecture Center, Google Cloud Architecture Framework.
- [ ] **Passo 5:** Reescrever `04-Sendas/Senda Cloud.md` como **Senda de verdade** (ordem de leitura curatorial apontando pros galhos da trilha), já que a lista crua de links migrou pra `Biblioteca.md`. Manter o arquivo (não deletar).
- [ ] **Passo 6:** Commit: `git add` dos 5 paths explícitos → `docs(cloud): andaime do domínio — MOC, roadmap, dicionário, biblioteca`.

---

## Galho 1 — O que é a nuvem, de verdade (DETALHADO)

**Pasta:** `03-Dominios/Tecnologia/Cloud/01 - O que é a nuvem, de verdade/`
**Meta:** 6 notas em 3 fases. Fundar o modelo mental para quem nunca estudou cloud de forma sistemática.

**Fronteiras (o que NÃO vai aqui):**
- Regions/AZs, console/CLI/SDK, responsabilidade compartilhada → **galho 2** (aqui só o conceito de "o provedor tem estrutura global", sem mecânica).
- Os 6 pilares do Well-Architected → **galho 3** (aqui no máximo um teaser de uma linha).
- IAM, VPC, EC2, S3, Lambda → blocos 2 e 3. **Nenhum serviço é ensinado aqui** — só nomeado como exemplo do modelo.
- FinOps/pricing a fundo → **galho 19** (aqui só a lógica capex→opex, não a prática de otimizar).

**Roster de notas:**

| # | Nota | Fase | Escopo |
|---|------|------|--------|
| 01 | O que é computação em nuvem | Iniciado | o problema antes da nuvem (comprar servidor, provisionar pra pico, meses de lead time); as 5 características do NIST (self-service sob demanda, acesso amplo, pooling, elasticidade rápida, serviço medido); o que a nuvem **não** é ("computador de outra pessoa" é caricatura) |
| 02 | Capex, opex e a economia da elasticidade | Iniciado | comprar ativo vs alugar capacidade; provisionar-pra-pico vs escalar-sob-demanda; elasticidade ≠ escalabilidade; economias de escala do provedor; TCO e o custo escondido do datacenter próprio; primeira noção de que **custo vira restrição de design** |
| 03 | Modelos de serviço — IaaS, PaaS, CaaS, FaaS e SaaS | Iniciado | o espectro controle↔conveniência; quem gerencia o quê em cada camada (tabela); analogia trabalhada; onde Droplet, App Platform, Lambda e Gmail caem no espectro; como escolher a camada |
| 04 | Modelos de implantação — público, privado, híbrido e multi-cloud | Adepto | nuvem pública/privada/híbrida/multi; por que empresa regulada faz híbrido; multi-cloud como decisão cara (teaser do galho 23); soberania de dados e residência |
| 05 | O panorama dos provedores | Adepto | AWS/Azure/GCP/DO — participação, filosofia e público de cada um; **primeira tabela de tradução de 4 colunas** (compute, storage, serverless); por que esta trilha escolhe AWS+DO como coluna prática |
| 06 | A virada mental — pensar em serviços, não em servidores | Magus | cattle vs pets; "managed-first" como default e quando desobedecer; projetar para a falha (tudo falha o tempo todo); o servidor como detalhe de implementação; custo e segurança como restrições de design desde o dia 1; o que muda no seu jeito de arquitetar |

**MOC do galho:** `03-Dominios/Tecnologia/Cloud/01 - O que é a nuvem, de verdade/index.md` agrupando por fase.
**Roadmap do galho:** `.../01 - O que é a nuvem, de verdade/roadmap.md`.

### Ciclo por nota (repetir para 01→06)

- [ ] **Passo A — Escrever:** `/escrever-nota "03-Dominios/Tecnologia/Cloud/01 - O que é a nuvem, de verdade/0N - <título>"` com o escopo da linha da tabela. Padrão capítulo + restrições globais. Passar ao subagente: escopo da nota, títulos das notas **vizinhas** (anterior e próxima, para o bridge), e as fronteiras acima.
- [ ] **Passo B — Gate:** `/verificar-nota` na nota recém-criada.
- [ ] **Passo C — Ajustar:** se o gate apontar lacuna (falta Mermaid, abertura sem cenário, TL;DR raso, refs sem URL, falta a lente dupla), corrigir inline.
- [ ] **Passo D — Commit:** `git add "<path da nota>"` → `feat(cloud): galho 1 nota 0N — <título>` (path explícito, sem assinatura).

### Fecho do galho 1

- [ ] **Passo E:** Criar `index.md` do galho (MOC por fase) e `roadmap.md` do galho (6/6 ✅).
- [ ] **Passo F:** Atualizar `roadmap.md`-pai do domínio (galho 1 ✅) e o MOC `Cloud/index.md`.
- [ ] **Passo G:** Acrescentar ao `Dicionário.md` os termos novos que o galho introduziu.
- [ ] **Passo H:** Commit de fecho: `docs(cloud): fecha galho 1 — O que é a nuvem, de verdade (6/6) + roadmaps`.

---

## Galhos 2–24 + Capstone (a detalhar na vez de cada um)

Cada galho, quando chegar sua vez, ganha uma seção como a do galho 1 (roster de notas por fase + fronteiras + ciclo). Roster macro dos temas em [[2026-07-20-trilha-cloud-design|Design]]. Sequência:

**Bloco 1 — Modelo mental e fundamentos**
- [ ] **Galho 2:** Anatomia de um provedor
- [ ] **Galho 3:** Well-Architected Framework ← a bússola; os galhos seguintes amarram nos pilares
- [ ] **Galho 4:** Identidade e acesso (IAM) ← ponte com Auth e Identidade

**Bloco 2 — Os primitivos**
- [ ] **Galho 5:** Compute I — máquinas virtuais
- [ ] **Galho 6:** Compute II — elasticidade e balanceamento ← ponte com System Design (LB)
- [ ] **Galho 7:** Rede na nuvem (VPC) ← o galho mais importante do bloco
- [ ] **Galho 8:** Armazenamento — object, block e file
- [ ] **Galho 9:** Bancos gerenciados ← ponte com System Design (SQL/NoSQL) e Dados
- [ ] **Galho 10:** DNS, CDN e borda ← ponte com System Design (CDN)

**Bloco 3 — Serverless e arquiteturas modernas**
- [ ] **Galho 11:** Serverless e FaaS — Lambda a fundo
- [ ] **Galho 12:** Containers gerenciados ← ponte com Operação (K8s)
- [ ] **Galho 13:** Mensageria e eventos gerenciados ← ponte com Comunicação entre Sistemas
- [ ] **Galho 14:** API Gateway e edge de aplicação ← ponte com Comunicação (rate limiting) e Auth
- [ ] **Galho 15:** Arquiteturas serverless e event-driven

**Bloco 4 — Operar, sustentar, governar**
- [ ] **Galho 16:** Infrastructure as Code ← ponte com Operação (GitOps/IaC)
- [ ] **Galho 17:** Observabilidade na cloud ← ponte com Operação (observabilidade)
- [ ] **Galho 18:** Segurança na cloud a fundo ← ponte com Segurança e Auth
- [ ] **Galho 19:** FinOps — a economia da cloud ← território exclusivo da Cloud
- [ ] **Galho 20:** Resiliência e continuidade ← ponte com Operação e System Design

**Bloco 5 — Provedores e maestria**
- [ ] **Galho 21:** AWS a fundo — consolidação
- [ ] **Galho 22:** DigitalOcean a fundo — consolidação
- [ ] **Galho 23:** Panorama multi-cloud e portabilidade ← Azure/GCP, tabela de tradução completa, lock-in
- [ ] **Galho 24:** Certificação — AWS Solutions Architect Associate ← **confirmar o código do exame vigente na hora de escrever**
- [ ] **Capstone:** Arquitetar um SaaS na cloud do zero

## Fecho da trilha

- [ ] Mover Cloud para 🟢/✅ no [[00-Meta/Roadmap|Roadmap mestre]]: acrescentar linha na seção Tecnologia, riscar o item em "Tier 1 — construção nova" e em "Coberturas ausentes a considerar".
- [ ] Criar memória `project_trilha_cloud.md` + linha no `MEMORY.md`.
- [ ] Rodar `/verificar-wikilinks "03-Dominios/Tecnologia/Cloud"` (regra Quartz: folder-link exige `index.md`).
- [ ] Registrar a pendência de **enriquecimento de mídia (M1)** no roadmap do domínio, junto com Arqueologia/Web Performance/Testes JS/Go.
