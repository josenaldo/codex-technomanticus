---
title: "Plano — Reorganização em 4 camadas"
type: spec
created: 2026-06-23
updated: 2026-06-23
status: in_progress
tags:
  - spec
  - reorg
  - camadas
---
# Plano — Reorganização do vault em 4 camadas

## Visão

`03-Dominios/` deixa de ser pastas flat e passa a ter **4 camadas físicas** como teto. A regra de colocação de qualquer assunto novo:

> É o **porquê** funciona (ciência atemporal), o **como construir/operar bem** (engenharia neutra de stack), o **como fazer em X** (tecnologia concreta), ou **carreira** (não-técnico)?

Seam-chave (anti-duplicação): a **fundamentação** fica na camada de Engenharia/Ciência; cada **tecnologia** linka pra lá e cuida das particularidades. Ex.: princípios de RBAC em `Engenharia/Segurança`; *RBAC no Spring* no galho de Spring.

## Árvore-alvo

```
03-Dominios/
├── Ciência/            (o PORQUÊ — CS atemporal)
│   ├── Algoritmos · Estruturas de Dados · Teoria da Computação
│   ├── Matemática para Computação · Organização de Computadores
│   ├── Sistemas Operacionais · Concorrência e Paralelismo
│   ├── Compiladores e Linguagens · Redes e Protocolos
│   ├── Paradigmas · Banco de Dados (só teoria)
│   └── index.md (MOC)
├── Engenharia/         (o COMO construir/operar bem — neutro)
│   ├── Arquitetura ✓ · Design de Software ✓ (SOLID/OO/Patterns)
│   ├── Comunicação entre Sistemas ✓ (API Design/Mensageria)
│   ├── Testes ✓ · Segurança ✓ · Complexidade de Software ✓
│   ├── Dados (NOVO — de BD engenharia)
│   ├── Operação (NOVO — de Infra princípios)
│   └── index.md (MOC)
├── Tecnologia/         (o COMO fazer em X — concreto)
│   ├── JavaScript (linguagem) · TypeScript · Node ✓ · React ✓
│   ├── HTML (NOVO) · CSS (NOVO) · Plataforma Web (NOVO)
│   ├── Tooling e Build (NOVO — Vite/Webpack/Babel/Turbopack/pnpm)
│   ├── Java ✓ · Go ✓ · Python ✓ · IA ✓
│   ├── Infraestrutura (só tools, após split) · Ferramentas · Terminal · RPA
│   └── index.md (MOC)
└── Carreira/           (não-técnico)
    ├── Entrevistas · Inglês · Empreendedorismo
    └── index.md (MOC)
```

`✓` = já existe/feito. Demais domínios de Tecnologia novos nascem na fase de conteúdo.

## Status

- **Fase A (estrutura física) — FEITA.** 4 camadas criadas; 25 domínios distribuídos via git mv; ~9.4k refs full-path reescritas em 954 arquivos; 0 stragglers; apocrypha (dashboard camada-aware). Tag `pre-reorg`.
- **Fase B (conteúdo) — PARCIAL.** Feito: Design de Software (SOLID+OO+Patterns), Comunicação entre Sistemas (API+Mensageria), Arquitetura enxuta, TS-com-React→React, TypeScript.md→TypeScript. Tag `pre-phaseB`.

## Batches restantes (ORDEM: limpeza antes de conteúdo)

### ✅ Batch 1 — Reword Fundamentos → Ciência da Computação (FEITO 2026-06-23, tag `pre-batch1`, commits 9bc478e + 76405fc)
- `Dicionário de Fundamentos.md` → `Dicionário de Ciência da Computação.md` (aliases antigos preservados p/ links históricos dos specs)
- `index.md` virou a MOC da camada (agrupamento temático portado do `Fundamentos.md`; lista só os 11 galhos de Ciência; OO/SOLID/Testes/Segurança/Complexidade → Veja também da Engenharia); `camada: Ciência` + tags
- `Fundamentos.md` **deletado** (MOC duplicado, Dataview já quebrado); 4 inbound `[[Fundamentos]]` redirecionados
- Prosa "Galho de Fundamentos" reescrita respeitando o novo lar (Ciência vs Engenharia); aliases `|Fundamentos]]` → `|Ciência da Computação]]`
- **Batch 1b:** tag `fundamentos` → `ciencia-da-computacao` (195 notas) / `engenharia` (80 notas); Tecnologia mantém `fundamentos` (marcador de conteúdo); specs preservados

### ✅ Batch 2 — Resolver links quebrados (FEITO 2026-06-23, tag `pre-batch2`, commit 5dabeb1)
- Escopo real: **739 reportados → 0 quebras genuínas** (não os ~47 estimados). 319 links corrigidos em 128 arquivos.
- Casos: normalização full-path (cluster IA path-relativo), casing `Banco de dados`→`Banco de Dados/index`, `[[Testes]]` por contexto (Engenharia vs Java), `[[index]]`→pasta-própria, Anatomia LLMs 13→15 (renumerado), headings de vídeo com `|`→`—` (WSL/RPA), forward-refs HTML/CSS → fonte interina
- **GOTCHA:** o `check_wikilinks.py` reporta ~420 FALSOS POSITIVOS estruturais (âncoras same-file 384, imagens existentes 20, em-dash em `[nota](…)` 9, placeholders em comentário 7, crase em âncora 4). NÃO são quebras — validar contra heading/arquivo real antes de "consertar". Vale melhorar o script.

### 🧹 Batch 3 — Dissolver o resto do cluster JS (dedup + distribuir)
- **Dedup primeiro**: `Mantine.md` e MUI existem em `React/` E `JavaScript/Frontend/` (Material UI.md vs MUI.md) — decidir versão canônica, fundir
- `JavaScript/Frontend/React.md`, `React Red Flag Manual.md`, `Material UI.md` → React (após dedup)
- `JavaScript/Backend/Node.js.md` → Node (ou descartar se redundante com a trilha madura)
- `JavaScript/Core/` achatado: `JavaScript Fundamentals.md`, `Testes em JavaScript.md` sobem pra raiz de JavaScript
- `Frontend/Networking/` (Axios, Fetch) → Plataforma Web; `Frontend/Debugging.md` → Plataforma Web
- `Frontend/Validação/` (Zod/Yup/Joi) → JavaScript (ecossistema) ou TypeScript (decidir)
- Objetivo: `JavaScript/Frontend/`, `JavaScript/Backend/`, `JavaScript/Core/` e o domínio `Frontend/` deixam de existir

### 🔪 Batch 4 — Splits de conteúdo + domínios novos
- Criar `Tecnologia/HTML`, `Tecnologia/CSS`, `Tecnologia/Plataforma Web`, `Tecnologia/Tooling e Build`, `Engenharia/Dados`, `Engenharia/Operação` (com index.md MOC)
- Split `JavaScript/Frontend/HTML e CSS.md` → HTML + CSS; `Bootstrap.md` → CSS
- Split `Ciência/Banco de Dados`: teoria fica, engenharia (modelagem/indexação/tradeoffs) → `Dados`
- Racha `Infraestrutura`: princípios (SRE/deploy/observabilidade) → `Operação`; `Observabilidade.md` e `CI-CD.md` racham por dentro; tools ficam em Infraestrutura

### ✍️ Batch 5+ — Conteúdo (trilhas)
- Escrever trilhas (3 fases: Iniciado/Adepto/Magus) dos domínios novos: Plataforma Web, HTML, CSS, Tooling e Build, Comunicação entre Sistemas, Dados, Operação, e aprofundar JavaScript/TypeScript/React
- Dobrar os stubs sobreviventes em cada trilha conforme for escrita

## Método (cada batch que move arquivo)

1. `git tag pre-batchN` (âncora reversível)
2. `git mv` os arquivos/pastas
3. Prefix-rewrite determinístico: `s#03-Dominios/SRC([]/"|)#.])#03-Dominios/DST\1#g` — **terminador inclui `.` quando o move é de ARQUIVO** (`.md` na ref); pra pasta basta `[]/"|)#]`. Ordem: regras específicas antes das genéricas
4. Verificar **0 stragglers** (`grep -rhoF "03-Dominios/SRC"`)
5. Atualizar MOCs afetados (camada + domínios)
6. Commit atômico, sem assinatura
7. Se mexeu em path que o apocrypha referencia: passada no apocrypha (commit separado)

## Âncoras git

- `pre-reorg` — antes da Fase A
- `pre-phaseB` — antes da Fase B
- (criar `pre-batchN` por batch)
