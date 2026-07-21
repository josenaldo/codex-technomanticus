---
title: "Roadmap — Evolução da Engenharia de IA"
created: 2026-07-20
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Evolução da Engenharia de IA

Roadmap do galho-folha `03-Dominios/Tecnologia/IA/Evolução da Engenharia de IA`. Mapeia as 8 notas do galho, uma entrada por nota.

> [!info] Origem
> Galho escrito de uma vez em **2026-07-20**, a partir de pesquisa web na mesma data (threads de @IntuitMachine, @steipete e @rohit4verse sobre graph engineering + cobertura secundária). Não passou por `/diagnosticar-galho` — os estados abaixo refletem a escrita inicial, não uma auditoria de qualidade nota a nota.

> [!warning] Pendência de mídia — bloqueia 3 notas
> As notas 05, 06 e 07 embutem 4 imagens que **ainda não estão no repositório**. Os embeds renderizam quebrados até os arquivos serem salvos nesta pasta:
> - `evolucao-eng-loop-motor-4-tempos.png` (nota 05)
> - `evolucao-eng-onde-um-loop-quebra.png` (nota 05)
> - `evolucao-eng-graph-engineering.png` (nota 06)
> - `evolucao-eng-grounded-vs-ungrounded.png` (nota 07)
>
> Fonte: thread de Carlos E. Perez (@IntuitMachine), julho de 2026.

> [!note] Galho aberto por design
> Este galho documenta um capítulo **em curso**. Quando surgir a próxima camada nomeada, ela entra como **nota 09** — e as perguntas de triagem da nota 08 são o filtro para decidir se ela merece a nota. O roadmap não fecha em 100%; ele fica em espera.

**Legenda:** ✅ completo · 📋 escrito, enriquecimento pendente · 🔶 parcial · ⬜ não escrito · ➖ não se aplica

## Notas

| # | Nota | Fase | Tam. | Estado | Pendência |
|---|---|---|---|---|---|
| 01 | A escada de abstração — qual é a unidade de design | Iniciado | 47 KB | 📋 | mídia (nenhum diagrama externo); revisar se o mapa do galho bate com as 8 notas finais |
| 02 | Prompt engineering — o que morreu e o que sobrou | Iniciado | 29 KB | 📋 | menor nota do galho; candidata a enriquecimento (casos práticos) |
| 03 | Flow engineering — o precursor que ninguém cita | Adepto | 48 KB | 📋 | mídia |
| 04 | Context e harness — o ambiente vira o produto | Adepto | 32 KB | 📋 | mídia; verificar não-duplicação com o galho Context Engineering |
| 05 | Loop engineering — o motor de 4 tempos e as 4 traições | Adepto | 33 KB | 🔶 | **2 imagens faltando** |
| 06 | Graph engineering — a confiabilidade mora nas arestas | Magus | 36 KB | 🔶 | **1 imagem faltando**; conteúdo mais volátil do galho — revisitar quando o discurso decantar |
| 07 | Grounded vs ungrounded — tocar a realidade | Magus | 31 KB | 🔶 | **1 imagem faltando** |
| 08 | Hype, ceticismo e mercado — lendo o próximo ciclo | Magus | 34 KB | 📋 | dados de mercado com validade curta — revalidar em ~6 meses |

**Progresso:** 0 ✅ / 8 · 5 📋 · 3 🔶

## Artefatos do galho

| Artefato | Estado |
|---|---|
| `index.md` (MOC) | ✅ criado 2026-07-20 |
| `roadmap.md` | ✅ este arquivo |
| Entrada no roadmap raiz de IA | ⬜ pendente |
| Entrada no `index.md` do domínio IA | ⬜ pendente |

## Próximas ações, em ordem

1. **Salvar as 4 imagens** na pasta do galho com os nomes exatos listados acima — desbloqueia 05, 06 e 07.
2. Registrar o galho no `roadmap.md` raiz de `IA/` e no `index.md` do domínio.
3. Rodar `/verificar-nota` nas 8 notas para auditoria estrutural (não foi rodada na escrita).
4. Nota 02 é a mais curta — primeira candidata a `/enriquecer-nota`.
5. Enriquecimento de mídia (vídeos/podcasts) via `/adicionar-midia` — nenhuma nota tem callout de mídia.

## Riscos conhecidos

> [!warning] Validade do conteúdo
> As notas 06, 07 e 08 dependem de discurso de **julho de 2026**, com dias de idade na data da escrita. Claims de blog (o "92% da qualidade a 63% do preço" na nota 06) estão marcados como não verificados no corpo da nota, mas devem ser revisitados. Os dados de mercado da nota 08 são de agregadores de vaga, não fonte oficial — a ressalva está no texto.

> [!warning] Fontes primárias inacessíveis
> Os três threads originais do X não puderam ser lidos direto (x.com retorna 402 a fetch automatizado; mirrors fora do ar). O conteúdo foi reconstruído a partir de cobertura secundária + das 4 imagens fornecidas pelo usuário. Se alguma citação atribuída precisar de precisão literal, confirmar no thread original.
