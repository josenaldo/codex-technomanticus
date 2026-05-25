# Regras de proveniência — enriquecer-nota

Todo candidato que entra na nota por uma lente que exige fonte precisa de proveniência registrável.
Isso é o que impede a skill de adicionar "parágrafos óbvios" sem lastro.

## Quais lentes exigem fonte

| Lente              | Exige fonte? |
| ------------------ | ------------ |
| Profundidade       | **Sim** — todo candidato precisa de fonte verificável |
| Novidade c/ fonte  | **Sim** — sem fonte, o candidato é descartado na origem (nem chega ao crítico) |
| Lacunas            | Preferível; se for conhecimento estrutural consolidado, `geral` é aceito |
| Conexões           | N/A — são wikilinks internos; a "fonte" é a própria nota/dicionário |
| Higiene baseline   | N/A |

## O que conta como fonte verificável

- URL de artigo, doc oficial ou paper (com título).
- Nota do próprio vault (path ou wikilink).
- `geral` ("conhecimento geral") **só** é aceito para a lente Lacunas (cobertura estrutural).
  Nunca para Profundidade ou Novidade.

## Como registrar

- Fontes externas (URL/paper) entram na seção `## Referências` da nota, no formato já usado no vault:
  `- **Fonte** — [*Título*](url) (ano). Nota curta.`
- Se a nota não tem `## Referências`, criar a seção antes de `## Veja também` (ou ao final, se não houver).
- A fonte **nunca** vai no corpo do parágrafo — só na seção Referências (mantém a nota limpa).
- Durante o pipeline, cada candidato carrega sua fonte no campo `fonte` do schema.
- Fontes do tipo `nota` viram entradas em `## Veja também`, não em `## Referências`.
