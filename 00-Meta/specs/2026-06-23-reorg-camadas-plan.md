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

### ✅ Batch 3 — Dissolver o cluster JS (FEITO 2026-06-23, tag `pre-batch3`, commit 62d2a13 + apocrypha 300846f)
- **Dedup invertido**: as versões RICAS estavam em `JavaScript/Frontend/` (não em React/); viraram canônicas em `React/Mantine.md` e `React/MUI.md` (substituíram os stubs de 44 ln); alias `Material UI` no MUI.md p/ inbound resolver
- `React.md` (1647 ln) + `React Red Flag Manual.md` (3547 ln) → `React/`
- `JavaScript/Core/` achatado (Fundamentals + Testes em JS → raiz de JavaScript); `Core/` removido
- `Node.js.md` (97 inbound, conteúdo próprio) → `Node/` como nota-tronco (NÃO descartado); `Backend/` removido
- `Frontend/` dissolvido: Networking + Debugging → **novo domínio `Plataforma Web`** (adiantado do Batch 4); Validação (Zod/Yup/Joi) → `JavaScript/Validação/`
- Resta `JavaScript/Frontend/` só com `HTML e CSS.md` + `Bootstrap.md` (Batch 4 finaliza); `JavaScript/Backend/`, `JavaScript/Core/`, domínio `Frontend/` deixaram de existir
- **Gotcha confirmado:** `for f in $(grep -rl ...)` quebra em nomes com espaço — usar Python/`-print0` pro rewrite

### ✅ Batch 4 — Splits de conteúdo + domínios novos (FEITO 2026-06-23, tag `pre-batch4`, commit b741a81)
- Criados `Tecnologia/HTML`, `Tecnologia/CSS`, `Tecnologia/Tooling e Build`, `Engenharia/Dados`, `Engenharia/Operação` (index.md MOC). `Plataforma Web` já no Batch 3
- `HTML e CSS.md` (1553 ln) splitado: HTML semântico (49-313) → `HTML/HTML semântico.md`; CSS (314→fim) → `CSS/CSS.md`; `Bootstrap.md` → CSS. `JavaScript/Frontend/` dissolvido de vez. `[[HTML e CSS]]` (12 refs) repontado → HTML + CSS
- **DESVIO aprovado (não fragmentar trilhas maduras):** `Banco de Dados` fica INTEIRO em Ciência; `Engenharia/Dados` é domínio de conteúdo novo que linka a teoria. Idem `Infraestrutura` (não rachada); `Engenharia/Operação` é novo, semente migra de Observabilidade.md+CI-CD.md no Batch 5
- HTML/CSS/Tooling e Build/Dados/Operação são MOCs-semente (trilha real = Batch 5)
- fix straggler: Dataview FROM antigo em `React/TypeScript com React/index`

### ✍️ Batch 5+ — Conteúdo (trilhas) — alvo: prep entrevistas, eixo frontend-web + system design
- Padrão: 3 fases (Iniciado/Adepto/Magus), notas ~440-540 ln estilo capítulo, diagramas Mermaid
- **Eixo frontend-web:** TypeScript (trilha do zero), CSS (expandir semente), HTML (expandir semente), JavaScript (consolidar em trilha), Plataforma Web (fetch/Web APIs/storage/workers), Tooling e Build (bundlers/transpilação/package managers), aprofundar React
- **Eixo system design:** Comunicação entre Sistemas (virar trilha), Dados (modelagem dimensional/warehouse/pipelines), Operação (SRE/SLO/deploy/observabilidade — migrar semente de Infra)
- Migrar conteúdo conceitual de `Infraestrutura/Observabilidade.md` + `CI-CD.md` → `Operação` ao escrever a trilha
- Outros pendentes (fora do eixo prioritário): Go, Python, Arquitetura (decidir trilha vs MOC), Entrevistas, Inglês, RPA, Ferramentas; Java falta só galho 18 (Cert. OCP)

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
