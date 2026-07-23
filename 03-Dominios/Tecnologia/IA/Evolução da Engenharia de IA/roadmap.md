---
title: "Roadmap — Evolução da Engenharia de IA"
created: 2026-07-20
updated: 2026-07-22
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Evolução da Engenharia de IA

Roadmap do galho-folha `03-Dominios/Tecnologia/IA/Evolução da Engenharia de IA`. Mapeia as 9 notas do galho, uma entrada por nota.

> [!info] Origem
> Galho escrito de uma vez em **2026-07-20**, a partir de pesquisa web na mesma data (threads de @IntuitMachine, @steipete e @rohit4verse sobre graph engineering + cobertura secundária). Em **2026-07-21** o usuário forneceu os textos primários integrais de dois ensaios de Carlos E. Perez e um curso de Codez (@0xCodez): fez-se uma **passada de fidelidade** nas notas 05/06/07 com o ensaio integral, criou-se a **nota 09** (segundo ensaio, "o compilador que faltava"), e a parte prática (curso do Codez) virou nota **separada** em `Claude Code/Workflows/12` — decisão do usuário: o galho histórico conta a história, a prática mora nos galhos específicos. Não passou por `/diagnosticar-galho` — os estados abaixo refletem escrita + fidelidade, não auditoria `/verificar-nota`.

> [!note] Galho aberto por design
> Este galho documenta um capítulo **em curso**. Quando surgir a próxima **camada nomeada**, ela entra como **nota 10** (a 09 já foi usada por uma segunda lente sobre loop engineering, não por uma camada nova) — e as perguntas de triagem da nota 08 + a pergunta irmã da 09 ("existe compilador, e é independente?") são o filtro para decidir se ela merece a nota. O roadmap não fecha em 100%; ele fica em espera.

> [!note] Numeração ≠ ordem de leitura
> A nota **09** foi escrita depois da 08 mas **lê antes** dela (ordem: 01→…→07→09→08). É uma segunda lente sobre o loop, não o fecho. A numeração é cronológica de escrita; o `index.md` explicita a ordem de leitura.

**Legenda:** ✅ completo · 📋 escrito, enriquecimento pendente · 🔶 parcial · ⬜ não escrito · ➖ não se aplica

## Notas

| # | Nota | Fase | Tam. | Estado | Pendência |
|---|---|---|---|---|---|
| 01 | A escada de abstração — qual é a unidade de design | Iniciado | 47 KB | 📋 | sem mídia externa; conferir que o mapa do galho cita a 09 |
| 02 | Prompt engineering — o que morreu e o que sobrou | Iniciado | 29 KB | 📋 | menor nota do galho; candidata a enriquecimento (casos práticos) |
| 03 | Flow engineering — o precursor que ninguém cita | Adepto | 48 KB | 📋 | — |
| 04 | Context e harness — o ambiente vira o produto | Adepto | 32 KB | 📋 | verificar não-duplicação com o galho Context Engineering |
| 05 | Loop engineering — o motor de 4 tempos e as 4 traições | Adepto | 35 KB | 📋 | fidelidade feita (PDCA, HVAC, "teatro"); 2 imagens ✅ no repo |
| 06 | Graph engineering — a confiabilidade mora nas arestas | Magus | 41 KB | 📋 | fidelidade feita (MLOps, análogos, arrependimento de Perez); imagem ✅; conteúdo volátil — revisitar quando o discurso decantar |
| 07 | Grounded vs ungrounded — tocar a realidade | Magus | 35 KB | 📋 | fidelidade feita (loops-só-relatórios, previsão de falha); imagem ✅ |
| 08 | Hype, ceticismo e mercado — lendo o próximo ciclo | Magus | 34 KB | 📋 | dados de mercado com validade curta — revalidar ~jan/2027 |
| 09 | Loop engineering e o compilador que faltava | Magus | 55 KB | 📋 | nota grande (no porte da 01/03); sem mídia; candidata a passe de simplificação |

**Progresso:** 0 ✅ / 9 · 9 📋 · 0 🔶

## Artefatos do galho

| Artefato | Estado |
|---|---|
| `index.md` (MOC) | ✅ atualizado 2026-07-22 (inclui a 09) |
| `roadmap.md` | ✅ este arquivo |
| 4 imagens (slides de Perez) | ✅ no repo, distribuídas 05/06/07 (commit b339ba6) |
| Entrada no roadmap raiz de IA | ✅ galho #22 |
| Entrada no `index.md` do domínio IA | ⬜ pendente |

## Notas-satélite fora deste galho

- `Claude Code/Workflows/12 - Orquestração em grafo — fan-out, arestas e verificadores` — a **prática** do graph engineering (curso do Codez). Linkada por este galho como o "como"; ela linka de volta como o "por quê". APIs verificadas contra doc oficial; `parallel()` marcado como "conforme a fonte".

## Próximas ações, em ordem

1. Registrar o galho no `index.md` do domínio `IA/` (roadmap raiz já feito).
2. Rodar `/verificar-nota` nas 9 notas para auditoria estrutural (não foi rodada na escrita).
3. Nota 02 é a mais curta — primeira candidata a `/enriquecer-nota`; nota 09 é a maior — candidata a passe de simplificação.
4. Enriquecimento de mídia (vídeos/podcasts) via `/adicionar-midia` — nenhuma nota tem callout de mídia; o vídeo "What Makes Agency Actually Work?" (citado na 09) é ponto de partida.

## Riscos conhecidos

> [!warning] Validade do conteúdo
> As notas 06, 07 e 08 dependem de discurso de **julho de 2026**, dias de idade na escrita. O claim "92% da qualidade a 63% do preço" (nota 06) está marcado como não verificado no corpo. Dados de mercado da nota 08 são de agregadores de vaga, não fonte oficial — ressalva no texto.

> [!warning] Fontes primárias — status atualizado
> Os textos integrais dos **dois ensaios de Perez** e do **curso de Codez** foram fornecidos pelo usuário em 2026-07-21 e usados como fonte primária (fidelidade nas 05/06/07, nota 09, nota-satélite Workflows/12). O **thread de @steipete** e o de @rohit4verse seguem só via cobertura secundária (x.com retorna 402 a fetch; mirrors fora do ar). Citações atribuídas a Steinberger/svpino/Catacora vêm de terceiros — confirmar no original se precisar de precisão literal.
