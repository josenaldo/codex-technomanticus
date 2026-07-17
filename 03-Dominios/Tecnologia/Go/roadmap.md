---
title: "Roadmap — Go"
created: 2026-07-16
updated: 2026-07-16
type: meta
publish: false
tags:
  - meta
  - roadmap
  - go
---
# Roadmap — Go

Roadmap-**raiz** da trilha `03-Dominios/Tecnologia/Go`. Mapeia o estado dos **21 galhos** (sub-galhos) + as notas soltas do domínio. Cada galho terá o próprio `roadmap.md` (Modo A) mapeando suas notas quando for construído.

**Design:** [[00-Meta/specs/2026-07-16-trilha-go-design|Design — Trilha Go]] · **Plano:** [[00-Meta/specs/2026-07-16-trilha-go-plano|Plano de Execução]]

**Nível:** raiz de domínio (contém galhos)

**Legenda de estado:** ✅ completo (0 ⬜) · 📋 diagnosticado, escrita pendente · 🔶 parcial · ⬜ não iniciado · ⚪ especial/fora do fluxo · `%` = (✅ + ➖) / total.

## Notas diretas (logo abaixo desta pasta)

| Nota | Tipo | Estado |
|------|------|--------|
| `index.md` | MOC da trilha | ➖ não precisa |
| `roadmap.md` | este roadmap | ➖ não precisa |
| `Go.md` | stub legado | ⚪ a excluir (conteúdo migra para os galhos) |
| `Go Backend.md` | stub legado (rico) | ⚪ a excluir — fonte de migração p/ galhos 9/11/14/16/18 |

## Galhos

| # | Galho | Notas | Estado | roadmap |
|--:|-------|------:|--------|---------|
| 1 | Fundamentos e sintaxe | 8 | ✅ escrito (2026-07-16) | ✓ [[01 - Fundamentos e sintaxe/roadmap\|roadmap]] |
| 2 | Tipos, structs e métodos | ~8 | ⬜ não iniciado | a criar |
| 3 | Interfaces e composição | ~8 | ⬜ não iniciado | a criar |
| 4 | Erros como valor | ~8 | ⬜ não iniciado | a criar |
| 5 | Coleções e dados | ~8 | ⬜ não iniciado | a criar |
| 6 | Generics | ~7 | ⬜ não iniciado | a criar |
| 7 | Goroutines e o scheduler | ~8 | ⬜ não iniciado | a criar |
| 8 | Channels e select | ~8 | ⬜ não iniciado | a criar |
| 9 | Sincronização e context | ~8 | ⬜ não iniciado | a criar |
| 10 | net/http e web frameworks | ~8 | ⬜ não iniciado | a criar |
| 11 | Persistência | ~8 | ⬜ não iniciado | a criar |
| 12 | gRPC e protobuf | ~7 | ⬜ não iniciado | a criar |
| 13 | Mensageria | ~7 | ⬜ não iniciado | a criar |
| 14 | Microservices e arquitetura | ~8 | ⬜ não iniciado | a criar |
| 15 | Testes | ~8 | ⬜ não iniciado | a criar |
| 16 | Observabilidade | ~8 | ⬜ não iniciado | a criar |
| 17 | Runtime interno | ~8 | ⬜ não iniciado | a criar |
| 18 | Cloud-native e produção | ~8 | ⬜ não iniciado | a criar |
| 19 | Segurança | ~8 | ⬜ não iniciado | a criar |
| 20 | Go idiomático | ~7 | ⬜ não iniciado | a criar |
| 21 | Preparação para entrevista de Go | ~7 | ⬜ não iniciado | a criar |
| — | Capstone | 1 | ⬜ não iniciado | — |

## Tabela-resumo (agregado)

| Métrica | Valor |
|---------|-------|
| Galhos | 21 + capstone |
| ✅ escritos | 1 (galho 1) |
| 🔶 em construção | 0 |
| ⬜ não iniciados | 20 + capstone |
| Notas escritas | 8 |
| Notas estimadas | ~160 |

---

## Próximos passos

1. ~~**Galho 1 — Fundamentos e sintaxe:** escrever as 8 notas~~ ✅ **feito (2026-07-16)** — 8/8 no padrão capítulo, `index.md` + `roadmap.md` do galho criados.
2. **Galho 2 — Tipos, structs e métodos:** próximo. Seguir galho a galho na ordem dos blocos (fundamentos → concorrência → serviços → produção → entrevista).
3. Nos galhos 9/11/14/16/18: migrar o conteúdo correspondente do `Go Backend.md`.
4. Ao fim: excluir `Go.md` e `Go Backend.md`; mover Go para ✅ no [[00-Meta/Roadmap|Roadmap mestre]]; criar memória.
