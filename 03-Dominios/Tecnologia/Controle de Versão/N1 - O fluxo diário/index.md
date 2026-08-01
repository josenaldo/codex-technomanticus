---
title: "N1 — O fluxo diário"
type: moc
publish: true
created: 2026-07-31
updated: 2026-07-31
status: seedling
tags:
  - moc
  - controle-de-versao
  - git
aliases:
  - O fluxo diário
  - Git nível 1
---

# N1 — O fluxo diário

> [!abstract] TL;DR
> O [[03-Dominios/Tecnologia/Controle de Versão/N0 - Sobrevivência/index|N0]] garantiu que você não perde trabalho. Este nível é sobre **usar o Git num projeto de verdade, todo dia, sem que ele atrapalhe**: parar de versionar lixo, ler o histórico com proveito, abrir linhas paralelas para testar ideias arriscadas, resolver o momento em que duas edições se cruzam, e sincronizar com outras pessoas sem sobrescrever ninguém.

Aqui o Git deixa de ser uma apólice de seguro e vira ferramenta de trabalho. É também onde ele começa a devolver mais do que custa: a partir do momento em que você confia em ramificar, experimentar deixa de ser arriscado.

O público continua sendo amplo — os exemplos ainda são de documentos e projetos acadêmicos —, mas a partir daqui o vocabulário começa a se aproximar do que você vai encontrar em equipes de software.

---

## As 6 notas

| # | Nota | O que você sai sabendo |
|---|------|------------------------|
| 06 | [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/06 - Ignorar arquivos - o gitignore e suas regras\|Ignorar arquivos — o `.gitignore` e suas regras]] | manter o `status` limpo; por que ignorar não apaga do histórico |
| 07 | [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/07 - Ler o histórico - log e diff\|Ler o histórico — `log` e `diff`]] | achar quando algo mudou; ler um diff sem medo |
| 08 | [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/08 - Branches na prática\|Branches na prática]] | linhas paralelas de trabalho; experimentar sem risco; juntar de volta |
| 09 | [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/09 - Conflito - por que acontece e como resolver\|Conflito — por que acontece e como resolver]] | ler os marcadores, resolver com calma, e a saída de emergência |
| 10 | [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/10 - Guardar trabalho pela metade - stash e worktrees\|Guardar trabalho pela metade — stash e worktrees]] | interromper sem perder o meio do caminho |
| 11 | [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/11 - Sincronizar com o time\|Sincronizar com o time]] | `fetch` × `pull`, push recusado, múltiplos remotos |

> **Estado (2026-07-31):** **escrita completa — 6/6 notas.** Falta enriquecimento de mídia (M1). Ver o [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/roadmap|roadmap do nível]].

---

## Veja também

- [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] — o domínio e os 7 níveis
- [[03-Dominios/Tecnologia/Controle de Versão/N0 - Sobrevivência/index|N0 — Sobrevivência]] — o nível anterior; este pressupõe aquele
- [[03-Dominios/Tecnologia/Controle de Versão/Biblioteca de Controle de Versão|Biblioteca]] — simuladores interativos e material em português
