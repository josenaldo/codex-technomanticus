---
title: "Roadmap — Configuração"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Configuração

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Tecnologia/IA/Claude Code/Configuração`
**Nível:** galho-folha
**Diagnóstico:** 2026-07-02
**Última execução:** —

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** SEM fase (sequência 01→08)
**Piso de linhas:** não aplicável

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 8 |
| ➖ não precisa | 0 |
| ✅ feita | 0 |
| % concluído | 0% |

> Diagnóstico concluído em 2026-07-02. Todas as 8 notas entram no loop de enriquecimento.
> Custo: 6 `[substantivo]` · 2 `[mecânico]` (05, 08).

---

## Notas

#### 01 - Hierarquia de configuração   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 363 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E4 (sem `## Casos práticos`), E5 (sem `## O que vem a seguir` — só "Veja também", lista sem narrativa), E8 (armadilhas em prosa/negrito, não `[!warning]` individuais), L1 (wikilinks só dentro da própria pasta Configuração), M1 (sem callout `[!tip]` com vídeo/podcast)
- **Score:** 8/12
- **Plano de execução:**
  - Criar seção `## Casos práticos` com ≥2 cenários concretos de produção (resolve E4)
  - Criar seção `## O que vem a seguir` com ponte narrativa para as próximas notas do galho, complementando "Veja também" (resolve E5)
  - Reescrever `## Armadilhas` como ≥3 callouts `[!warning]` individuais, um por armadilha (resolve E8)
  - Adicionar ≥1 wikilink apontando para nota fora da pasta Configuração (resolve L1)
  - Rodar /adicionar-midia para embutir callout `[!tip]` com vídeo/podcast relevante sobre hierarquia de configuração (resolve M1)
- **Resultado:** —

#### 02 - CLAUDE.md anatomia   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 390 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E5 (sem "## O que vem a seguir"; só "## Veja também" sem ponte narrativa)
- **Score:** 8/11 (P1 N/A — nota conceitual, sem exemplo de código real)
- **Plano de execução:**
  - Adicionar seção `## Casos práticos` com ≥2 cenários de produção concretos, ex. um CLAUDE.md genérico que gerou decisão errada por falta de contexto de domínio, e um CLAUDE.md desatualizado que instruiu comando/lib obsoleta (resolve E4)
  - Adicionar seção `## O que vem a seguir` com ponte narrativa para "03 - CLAUDE.md receitas" (templates por stack), substituindo/complementando "## Veja também" (resolve E5, item de núcleo)
  - Adicionar seção `## Armadilhas comuns` com ≥3 callouts `[!warning]` individuais, ex. CLAUDE.md viciado em detalhe de implementação, CLAUDE.md nunca revisado após mudança de stack, seção de Restrições sem o "por quê" (resolve E8)
  - Rodar `/adicionar-midia` para buscar vídeo/podcast relevante sobre CLAUDE.md/onboarding de agentes e embutir callout `[!tip]` (resolve M1)
- **Resultado:** —

#### 03 - CLAUDE.md receitas   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 424 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E1 (TL;DR com só 1 linha densa, falta ≥3), E5 (não há "O que vem a seguir" — há "Veja também", só lista de links) — outros gaps: E3 (sem diagrama Mermaid), E4 (sem seção "Casos práticos" dedicada — exemplos preenchidos existem, mas não sob esse título), E8 (sem "Armadilhas comuns" com `[!warning]`), P1 (exemplos de código só mostram caminho feliz, nenhum caso-problema), L1 (wikilinks em "Veja também" apontam só para notas da própria pasta Configuração)
- **Score:** 5/12
- **Plano de execução:**
  - Expandir o callout `> [!abstract] TL;DR` para ≥3 linhas densas (resolve E1, item de núcleo)
  - Adicionar ≥1 diagrama Mermaid com semântica visual — ex: fluxo de decisão "qual receita escolher" ou árvore stack→template (resolve E3)
  - Criar seção `## Casos práticos` com ≥2 cenários de produção concretos, reaproveitando/expandindo os exemplos preenchidos (PayHub, Analytica) (resolve E4)
  - Reescrever "## Veja também" como `## O que vem a seguir`, com ponte narrativa em vez de lista pura de links (resolve E5, item de núcleo)
  - Criar seção `## Armadilhas comuns` com ≥3 callouts `[!warning]` individuais (ex: copiar receita sem adaptar, placeholder esquecido, restrições genéricas demais) (resolve E8)
  - Adicionar exemplo de código/config mostrando um caso-problema real (ex: CLAUDE.md mal preenchido levando o agente a decisão errada) (resolve P1)
  - Adicionar ≥1 wikilink apontando para nota fora da pasta Configuração (resolve L1)
- **Resultado:** —

#### 04 - settings.json   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 429 linhas reais · fase: ausente · status: growing
- **Núcleo/gaps:** E5 (sem `## O que vem a seguir` — há "Veja também", lista pura sem ponte narrativa) — outros gaps: E4 (sem seção `## Casos práticos` dedicada; existem configs por stack e um exemplo anotado, mas não como cenários de produção), E8 (seção "Armadilhas" em prosa/negrito, não `[!warning]` individuais), P1 (exemplos de código só mostram caminho feliz — nenhum caso-problema, ex. allow vazio travando sessão ou deny amplo demais), M1 (sem callout `[!tip]` com vídeo/podcast)
- **Score:** 8/12
- **Plano de execução:**
  - Criar seção `## Casos práticos` com ≥2 cenários de produção concretos, reaproveitando/expandindo os exemplos por stack e o exemplo fullstack anotado (resolve E4)
  - Reescrever "## Veja também" como `## O que vem a seguir`, com ponte narrativa para "05 - Permissions" e "07 - Pasta .claude" (resolve E5, item de núcleo)
  - Reescrever `## Armadilhas` como `## Armadilhas comuns` com ≥3 callouts `[!warning]` individuais, um por armadilha já listada (resolve E8)
  - Adicionar exemplo de código mostrando caso-problema real, ex: allow list vazio travando a sessão, ou `"deny": ["Bash(*)"]` bloqueando tudo (resolve P1)
  - Rodar `/adicionar-midia` para buscar vídeo/podcast relevante sobre configuração/permissions do Claude Code e embutir callout `[!tip]` (resolve M1)
- **Resultado:** —

#### 05 - Permissions   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 397 linhas reais · fase: ausente (SEM fase) · status: growing
- **Núcleo/gaps:** E5 (sem "## O que vem a seguir" — só "## Veja também" listado)
- **Score:** 7/11
- **Plano de execução:**
  - Criar seção `## Casos práticos` com ≥2 cenários de produção concretos, reaproveitando os exemplos de tier Node/Python/Java como cenários narrados — resolve E4
  - Adicionar seção `## O que vem a seguir` com ponte narrativa para as notas 04/01/08, complementando o atual "## Veja também" — resolve E5
  - Reescrever "## Armadilhas" como `## Armadilhas comuns`, convertendo os 5 itens em negrito em callouts `[!warning]` individuais (mínimo 3) — resolve E8
  - Adicionar ≥1 wikilink apontando para nota fora da pasta Configuração (ex.: nota de segurança/Bash tools no domínio IA) — resolve L1
  - Adicionar callout `[!tip]` com link para vídeo/podcast sobre permissions no Claude Code — resolve M1
- **Resultado:** —

#### 06 - Slash commands customizados   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 366 linhas reais · fase: ausente (SEM fase) · status: growing
- **Núcleo/gaps:** E1 (TL;DR com só 1 linha densa, falta ≥3), E5 (sem "## O que vem a seguir" — só "## Veja também", lista sem ponte narrativa), L2 (seção chamada "## Referências", não "## Fontes") — outros gaps: E4 (sem seção "Casos práticos" dedicada — há "Biblioteca de commands úteis", mas não cenários de produção narrados), E8 (seção "## Armadilhas" em negrito/prosa, não callouts `[!warning]` individuais), M1 (sem callout `[!tip]` com vídeo/podcast)
- **Score:** 6/11 (P1 N/A — exemplos são arquivos de command/template, não código com caso-problema a resolver)
- **Plano de execução:**
  - Expandir o callout `> [!abstract] TL;DR` para ≥3 linhas densas (resolve E1, item de núcleo)
  - Reescrever "## Veja também" como `## O que vem a seguir`, com ponte narrativa para "07 - Pasta .claude" e "08 - Armadilhas de configuração" (resolve E5, item de núcleo)
  - Renomear "## Referências" para `## Fontes`, mantendo os links externos existentes (resolve L2, item de núcleo)
  - Criar seção `## Casos práticos` com ≥2 cenários de produção concretos, reaproveitando/expandindo exemplos da "Biblioteca de commands úteis" (ex.: time que padronizou `/pr-check` após bug recorrente passar por review) (resolve E4)
  - Reescrever "## Armadilhas" como `## Armadilhas comuns`, convertendo os 5 itens em negrito em callouts `[!warning]` individuais (mínimo 3) (resolve E8)
  - Rodar `/adicionar-midia` para buscar vídeo/podcast relevante sobre slash commands customizados e embutir callout `[!tip]` (resolve M1)
- **Resultado:** —

#### 07 - Pasta .claude   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 371 linhas reais · fase: ausente (SEM fase) · status: growing
- **Núcleo/gaps:** E5 (sem `## O que vem a seguir` — só "## Veja também", lista pura sem ponte narrativa), L2 (seção chamada "## Referências", não "## Fontes") — outros gaps: E4 (sem seção `## Casos práticos` dedicada), E8 (seção "## Armadilhas" em negrito/prosa, não callouts `[!warning]` individuais), L1 (todos os wikilinks apontam só para notas da própria pasta Configuração), M1 (sem callout `[!tip]` com vídeo/podcast), P1 (exemplos de código — settings.json, settings.local.json, script de setup — só mostram caminho feliz, nenhum caso-problema)
- **Score:** 5/12
- **Plano de execução:**
  - Reescrever "## Veja também" como `## O que vem a seguir`, com ponte narrativa para "08 - Armadilhas de configuração" (resolve E5, item de núcleo)
  - Renomear "## Referências" para `## Fontes`, mantendo os links externos existentes (resolve L2, item de núcleo)
  - Criar seção `## Casos práticos` com ≥2 cenários de produção concretos, ex. secret vazado por estar em `settings.json` versionado, e time que divergiu do padrão por falta de `commands/` compartilhado (resolve E4)
  - Reescrever "## Armadilhas" como `## Armadilhas comuns`, convertendo os 4 itens em negrito em callouts `[!warning]` individuais (resolve E8)
  - Adicionar ≥1 wikilink apontando para nota fora da pasta Configuração (resolve L1)
  - Rodar `/adicionar-midia` para buscar vídeo/podcast relevante sobre a estrutura da pasta .claude e embutir callout `[!tip]` (resolve M1)
  - Adicionar exemplo mostrando um caso-problema real, ex: `settings.local.json` staged antes do `.gitignore` vazando credencial dev, ou `settings.json` com `deny` amplo demais bloqueando comando legítimo (resolve P1)
- **Resultado:** —


#### 08 - Armadilhas de configuração   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 370 linhas reais · fase: ausente (SEM fase) · status: growing
- **Núcleo/gaps:** E1 (TL;DR é 1 parágrafo denso mas fica numa única linha, falta ≥3 linhas densas), E5 (sem `## O que vem a seguir` — só "## Veja também", lista pura de wikilinks sem ponte narrativa), L2 (seção chamada "## Referências", não "## Fontes") — outros gaps: E4 (sem seção `## Casos práticos` dedicada — as 12 armadilhas já são cenários concretos, mas não estão sob esse título), E8 (12 armadilhas em `### Armadilha N` com **Sintoma/Causa/Fix**, não callouts `[!warning]` individuais), L1 (wikilinks em "Veja também" apontam só para notas da própria pasta Configuração), M1 (sem callout `[!tip]` com vídeo/podcast)
- **Score:** 6/12
- **Plano de execução:**
  - Expandir o callout `> [!abstract] TL;DR` de 1 parágrafo corrido para ≥3 linhas densas distintas (resolve E1, item de núcleo)
  - Criar seção `## Casos práticos` com ≥2 cenários de produção concretos, reaproveitando armadilhas já catalogadas (ex.: allow amplo demais permitindo `git push --force` acidental; secret commitado exigindo rotação) (resolve E4)
  - Reescrever "## Veja também" como `## O que vem a seguir`, com ponte narrativa pras próximas ações do leitor após diagnosticar a própria configuração (resolve E5, item de núcleo)
  - Converter os 12 blocos `### Armadilha N` em callouts `[!warning]` individuais (mantendo sintoma/causa/fix), agrupados sob `## Armadilhas comuns` por categoria (resolve E8)
  - Adicionar ≥1 wikilink apontando para nota fora da pasta Configuração (ex.: nota de segurança/secrets no domínio IA ou Tecnologia) (resolve L1)
  - Renomear "## Referências" para `## Fontes`, mantendo os links externos existentes (resolve L2, item de núcleo)
  - Rodar `/adicionar-midia` para buscar vídeo/podcast relevante sobre troubleshooting de configuração do Claude Code e embutir callout `[!tip]` (resolve M1)
- **Resultado:** —
