---
title: "Roadmap — Auth e Identidade"
created: 2026-07-10
type: meta
publish: false
tags:
  - meta
  - roadmap
  - auth-identidade
---

# Roadmap — Auth e Identidade (galho-pai)

Roadmap do galho `03-Dominios/Engenharia/Auth e Identidade`. Galho-**pai**: mapeia o estado dos sub-galhos. Cada sub-galho tem seu próprio `roadmap.md` (folha). Spec de origem: [[00-Meta/specs/2026-07-10-auth-identidade-trilha-design]].

## Estado dos sub-galhos

| # | Sub-galho | Fase | Notas planejadas | Estado |
|---|-----------|------|------------------|--------|
| 1 | Fundamentos de identidade | Iniciado | 5 | ✅ 5/5 (2026-07-10) |
| 2 | OAuth 2.1 e OpenID Connect | Adepto | 6 | ✅ 6/6 (2026-07-11) |
| 3 | Autorização e multi-tenancy | Adepto→Magus | 4 | ✅ 4/4 (2026-07-11) |
| 4 | Auth nos stacks | Magus | 6 | ✅ 6/6 (2026-07-11) |
| 5 | Keycloak | Magus | 3 | ⬜ pendente |
| ★ | Capstone — Desenhando a identidade de um SaaS B2B | Magus | 1 | ⬜ pendente |

**Total planejado:** 24 notas de conteúdo + 1 capstone (25) + scaffolding (index/roadmap por sub-galho).

## Ordem de execução (ritmo B)

Sub-galho a sub-galho, ponta a ponta: 1 → 2 → 3 → 4 → 5 → capstone. Commit por sub-galho (paths explícitos, sem Co-Authored-By, push manual). Ao fechar cada sub-galho, atualizar o roadmap-folha dele e esta tabela.

## Rollup para o domínio (ao concluir)

- Callouts em [[12 - Autenticação|Segurança 12]] e [[13 - Autorização e controle de acesso|Segurança 13]] apontando pra cá (casa canônica do deep-dive).
- Callout leve em Comunicação SG2-03 (auth de API) apontando pra cá.
- Atualizar [[00-Meta/Roadmap]]: seção Engenharia (nova linha) + coberturas ausentes (Auth & Identidade 🚫 → 🟢).
- Sinalizar nos roadmaps das trilhas Python e Go (quando existir) que auth-nos-stacks mora aqui.

## Pendências transversais

- Baseline de versões cravadas (revisar na manutenção): OAuth 2.1 draft-15 · Keycloak 26.x (26.6 estável / 26.7) · Spring Security 6.4+ (passkeys/OTT) · better-auth (ecossistema volátil — caducidade explícita).
- SG3-02 (OpenFGA/Zanzibar): se crescer demais na escrita, vira broto `fase: Magus`.
