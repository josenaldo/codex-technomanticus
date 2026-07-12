---
title: "Roadmap — Python"
created: 2026-07-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Python (galho-pai)

Roadmap do domínio `03-Dominios/Tecnologia/Python`. Escala e método iguais à trilha [[03-Dominios/Tecnologia/Java/index|Java]] (19 galhos, um por vez, múltiplas sessões). Spec de origem: [[00-Meta/specs/2026-07-09-python-trilha-design]].

## Estado dos galhos

| # | Galho | Fase | Estado |
|---|-------|------|--------|
| 1 | Core | Iniciado | ✅ 9/9 (2026-07-09) |
| 2 | Collections e Comprehensions | Iniciado→Adepto | ✅ 8/8 (2026-07-09) |
| 3 | OO e Data Model | Adepto | ✅ 9/9 (2026-07-09) |
| 4 | Funcional e idiomas avançados | Adepto→Magus | ✅ 9/9 (2026-07-10) |
| 5 | Tipagem moderna | Adepto | ✅ 8/8 (2026-07-10) |
| 6 | CPython internals | Magus | ✅ 9/9 (2026-07-10) |
| 7 | Concorrência e paralelismo | Adepto→Magus | ✅ 8/8 (2026-07-10) |
| 8 | Programação Reativa e Assíncrona | Magus | ✅ 8/8 (2026-07-11) |
| 9 | Persistência de dados | Adepto→Magus | ✅ 8/8 (2026-07-11) |
| 10 | Web e APIs REST | Adepto | ✅ 9/9 (2026-07-11) |
| 11 | Segurança | Adepto→Magus | ✅ 9/9 (2026-07-11) |
| 12 | Testes | Adepto | ✅ 9/9 (2026-07-11) |
| 13 | Arquitetura e Design Patterns | Magus | ✅ 8/8 (2026-07-12) |
| 14 | Mensageria | Adepto→Magus | ✅ 8/8 (2026-07-12) |
| 15 | Microservices e sistemas distribuídos | Magus | ✅ 8/8 (2026-07-12) |
| 16 | Build e tooling | Iniciado→Adepto | ✅ 8/8 (2026-07-12) |
| 17 | Observabilidade e produção | Magus | ✅ 8/8 (2026-07-12) |
| 18 | Cloud-native e produção | Magus | ✅ 8/8 (2026-07-12) |
| 19 | Certificação (PCEP/PCAP) | Magus | ✅ 8/8 (2026-07-12) |

**Total planejado:** ~250-300 notas ao todo (escala Java), distribuídas nos 19 galhos + scaffolding por galho.

**TRILHA COMPLETA em 2026-07-12** — 19/19 galhos ✅. Ver [[03-Dominios/Tecnologia/Python/index|index]] pro rollup final.

## Ordem de execução (ritmo Java — um galho por vez, direto na main)

Núcleo da linguagem primeiro (galhos 1-6), depois concorrência (7-8), backend/arquitetura (9-13), plataforma distribuída/produção (14-18), certificação por último (19) — mesma lógica do Java, que também fechou certificação ao final. **Um galho por sessão** (ou dois pequenos); nunca tentar completar a trilha inteira de uma vez. Cada galho: `index.md` (fases + rotas alternativas + dataview) + `roadmap.md` + notas via subagente-por-nota (≤3/onda, Sonnet, barra de densidade explícita, cita Real Python/Dunossauro/livros-fonte). Commit por galho fechado, sem branch dedicada (ver [[feedback_galhos_direto_main]]), push manual.

## Rollup para o domínio (ao longo do fechamento de cada galho)

- Podar `Python Backend.md` conforme os galhos 9/10/17 absorvem o conteúdo.
- Atualizar esta tabela e a memória do projeto a cada galho fechado.
- Ao fechar o galho 19 (último): marcar a trilha completa, revisar `index.md` do domínio.

## Pendências transversais

- EXEMPLAR: usar `Java/Web e APIs REST/index.md` e notas 01-05 como referência estrutural até o Galho 1 (Core) virar o exemplar próprio.
- Certificação (galho 19): pesquisar PCEP/PCAP no momento de abrir o galho, não antes.
