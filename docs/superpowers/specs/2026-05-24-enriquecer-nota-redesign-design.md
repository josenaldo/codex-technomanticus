# Spec: Redesign da skill `enriquecer-nota` (v2)

**Data:** 2026-05-24
**Status:** aprovado
**Supersede parcialmente:** [`2026-05-08-enriquecer-nota-design.md`](2026-05-08-enriquecer-nota-design.md)

---

## Motivação

A v1 da `enriquecer-nota` otimiza para **completude mecânica**: frontmatter, typos,
presença de TL;DR/intro, varredura de linkagem e uma busca web genérica. Na prática,
ela *decora* a nota — adiciona parágrafos óbvios que não acrescentam muito — porque
não tem nenhum modelo de **ganho de informação**:

- nunca pergunta "o que esta nota deixou de cobrir que um leitor sênior esperaria?";
- não tem filtro de **novidade** que rejeite o que o leitor-alvo já sabe;
- a pesquisa web é desfocada, gerando resumos genéricos;
- quem gera o conteúdo é quem julga se ele presta (sem revisor independente).

A v2 muda o eixo de "decorar a nota" para **"achar e fechar lacunas reais, com fonte
verificável, filtrado por novidade contra o nível-alvo da nota"**, sob controle
granular do usuário.

### Inspiração externa

Padrões emprestados do plugin [`wiki-builder`](https://github.com/dair-ai/dair-academy-plugins/tree/main/plugins/wiki-builder)
da DAIR Academy:

1. **Gate de proveniência** — "não converta afirmações soltas em fatos sem fonte".
2. **Prompts por operação** em vez de fluxo monolítico (`compile-concept-page`,
   `query-and-file`, `lint-wiki`).
3. **Passo de `lint`** — verificação de qualidade *depois* de gerar.

O `query-and-file` (enriquecimento dirigido por uma pergunta em aberto) vira o *motor
interno* das lentes de Profundidade e Lacunas. O `llm-council` (deliberação multi-modelo
do Karpathy) inspira o passo de crítica, mas sem depender de API externa paga — usamos
um subagente do próprio Claude Code.

---

## Decisões de design (travadas com o usuário)

| Decisão | Escolha |
|---|---|
| Dimensões de valor | Todas as 4 (Profundidade, Lacunas, Novidade-c/-fonte, Conexões), **selecionáveis** |
| Controle | Dois níveis: escolher lentes no início **+** cherry-pick item a item no fim |
| Régua de novidade | Subagente **crítico**, **calibrado pela `fase`** da nota |
| Escopo de edição | Aditivo **+** pode aprofundar/reescrever trecho raso, sempre como **diff** aprovado item a item; nunca remove em silêncio |
| Arquitetura | Pipeline de lentes + subagente crítico (Abordagem A) |

---

## Invocação

Inalterada em relação à v1:

```
/enriquecer-nota [path] [instrução complementar]
```

- **Sem `path`:** pergunta qual nota enriquecer.
- **Com `path`:** usa o arquivo indicado.
- **Instrução complementar:** texto livre tratado como contexto (foco temático, URLs a
  incorporar, ênfase em seção). Pode também pré-selecionar lentes (ex: "só profundidade
  e conexões").

---

## As 4 lentes

Cada lente é um analisador focado, com um *motor* próprio. O usuário escolhe quais rodar.

| Lente | O que faz | Motor | Precisa de web? |
|---|---|---|---|
| **Profundidade** | Vai além do óbvio: trade-offs, edge cases, gotchas, o detalhe que separa júnior de sênior | Gera as *perguntas em aberto* que um leitor da fase-alvo (ou acima) faria; pesquisa e responde com fonte | Sim |
| **Lacunas** | Sub-tópicos que a nota deveria cobrir e não cobre | Monta o outline de cobertura esperada do tema no nível da nota; faz diff com o conteúdo atual; propõe o que falta | Às vezes |
| **Novidade c/ fonte** | Fatos líquidos-novos que o leitor-alvo provavelmente não sabe | Pesquisa dirigida; **exige proveniência**; bane conhecimento genérico sem fonte | Sim |
| **Conexões** | Wikilinks pro dicionário do domínio + notas/trilhas relacionadas | Varredura de linkagem da v1 (`### <Termo>` no glossário) + grep no vault por notas relacionadas | Não |

### Higiene baseline (sempre roda)

Independente das lentes, sempre roda um passe barato de higiene, apresentado num grupo
próprio e discreto no plano:

- **Frontmatter:** `status: seedling → growing`, `updated: → hoje`, `progresso: andamento`
  se ausente e aplicável.
- **Typos / erros gramaticais óbvios.**
- **Estrutura:** TL;DR e parágrafo de introdução presentes?

A higiene **não** passa pelo crítico (são correções objetivas, não candidatos de conteúdo).

---

## Fluxo (7 fases)

### Fase 1 — Identificar alvo
1. Valida `path` (ou pergunta).
2. Lê a nota inteira.
3. Infere o **domínio** pelo path (`03-Dominios/<X>/`).
4. Localiza o **dicionário do domínio** (`type: glossary`). Se vários, pergunta. Se
   nenhum, a lente Conexões e a criação de verbetes ficam desativadas.
5. **Lê `fase:`** do frontmatter (Iniciado/Adepto/Magus). Fallback: infere pelo conteúdo;
   default **sênior (régua Magus)**, dado o contexto do usuário — é a régua mais estrita,
   então corta o máximo de óbvio.

### Fase 2 — Escolher lentes
Apresenta menu **multi-select** das 4 lentes. Avisa que a higiene baseline sempre roda.
Se a instrução complementar já indicou lentes, pré-seleciona e confirma.

### Fase 3 — Análise por lente
Para cada lente selecionada, roda o motor correspondente e produz um pool de
**candidatos**. Cada candidato carrega:

```
{ lente, conteúdo_rascunho, local_alvo, fonte (URL/nota/"conhecimento geral"), tipo (adição|reescrita) }
```

Lentes que precisam de fora fazem **WebSearch dirigido** (não genérico) e registram a
proveniência. Reescritas (aprofundar trecho raso) carregam `tipo: reescrita` e o texto
original a ser substituído.

### Fase 4 — Crítica (subagente)
Despacha **um** subagente revisor (Agent tool, `general-purpose` com o prompt de
`references/critico.md`) recebendo: o pool de candidatos + a nota + a `fase`/nível.

O crítico:
- pontua cada candidato por **novidade** e **profundidade** contra o nível-alvo;
- **descarta** os óbvios (que um leitor naquele nível já saberia) e os sem fonte
  verificável quando a lente exige fonte (Profundidade, Novidade);
- devolve os sobreviventes com **justificativa de 1 linha + confiança**, e a lista do
  que cortou (com motivo).

Uma única chamada de subagente cobre o pool inteiro (controle de custo).

### Fase 5 — Plano
Apresenta os **sobreviventes agrupados por lente**; reescritas mostradas como **diff
antes→depois**; higiene em grupo próprio. Mostra também (recolhido) o que o crítico
**descartou**, para o usuário poder resgatar.

```
PLANO — <título da nota>   (fase-alvo: <Adepto>)

HIGIENE
[ ] status: seedling → growing
[ ] updated: → 2026-05-24

PROFUNDIDADE
[ ] +§Trade-offs: <rascunho>   — fonte: <url>   (crítico: "edge case não-óbvio", alta)
[~] reescrever §X (raso): "<antes>" → "<depois>"   — fonte: <url>

LACUNAS
[ ] +§<sub-tópico ausente>: <rascunho>   — fonte: <url>

NOVIDADE
[ ] +<fato>   — fonte: <url>   (crítico: "provavelmente desconhecido no nível", média)

CONEXÕES
[ ] [[Dicionário de IA#Termo|texto]] — §Y
[ ] DICIONÁRIO: criar verbete <termo> + wikilink

DESCARTADOS PELO CRÍTICO (3) ▸ (recolhido; expanda para resgatar)

[c] confirmar marcados   [x] cancelar   [e] editar item   alternar item N
```

### Fase 6 — Execução
Ordem determinística (relê o arquivo antes de cada edição):
1. Frontmatter (higiene)
2. Estrutura (TL;DR/intro)
3. Adições de conteúdo
4. **Reescritas (diffs)** — substituição exata do trecho original aprovado
5. Wikilinks inline
6. Verbetes (lógica `/verbete`: alfabético, idioma do glossário, bump do dicionário) + wikilink
7. Referências (proveniência das fontes usadas)
8. Veja também

### Fase 7 — Relatório
O que entrou por lente, verbetes criados, fontes adicionadas, e **o que o crítico cortou**
(transparência do gate).

```
CONCLUÍDO — <título>   (fase-alvo: Adepto)
✓ Higiene: status, updated
✓ Profundidade: 2 adições + 1 trecho aprofundado (2 fontes)
✓ Lacunas: 1 sub-tópico
✓ Novidade: 1 fato (1 fonte)
✓ Conexões: 3 wikilinks, 1 verbete criado (vibe coding)
– Crítico cortou 3 candidatos (óbvios para o nível)
```

---

## Arquitetura de arquivos

```
.claude/skills/enriquecer-nota/
├── SKILL.md                      # reescrito com as 7 fases
└── references/
    ├── lentes.md                 # definição detalhada de cada lente + seu motor
    ├── critico.md                # prompt do subagente: entrada, rubrica por fase, formato de saída
    └── proveniencia.md           # regras de fonte (o que exige fonte, formato na seção Referências)
```

- **Crítico** despachado via Agent tool, `subagent_type: general-purpose`, com o prompt
  de `references/critico.md`.
- A **rubrica de fase** vive em `critico.md`: o que conta como "óbvio" em Iniciado vs
  Adepto vs Magus.

---

## Calibragem por fase

| Fase | Régua do crítico (corta se...) |
|---|---|
| **Iniciado** (júnior) | ...for trivial até para quem está começando no tema |
| **Adepto** (pleno) | ...um pleno da área já saberia; exige nuance/trade-off |
| **Magus** (sênior) | ...um sênior já domina; exige edge case, gotcha, detalhe de produção |
| *sem `fase:`* | infere; default **sênior** |

---

## O que se mantém vs muda (vs v1)

**Mantém:** invocação, confirmação-antes-de-executar, segurança aditiva-por-padrão,
integração `/verbete`, formato de wikilink `[[Dict#Termo|texto]]`, "Veja também",
bump de frontmatter, não cria notas novas.

**Muda:**
- Adiciona **seleção de lentes** (Fase 2).
- Troca a busca genérica por **pesquisa focada-por-lente com proveniência**.
- Adiciona o **subagente crítico** (Fase 4).
- Permite **aprofundar-com-diff** (antes: só aditivo).
- Plano **agrupado por lente** + mostra descartados.
- Lê e usa **`fase:`** como calibragem.

---

## Fora de escopo

- Não reorganiza a nota inteira (mover/fundir seções livremente) — reescrita é cirúrgica,
  trecho a trecho, sempre com diff.
- Não apaga conteúdo sem mostrar.
- Não cria notas novas (só edita a nota-alvo e o dicionário).
- Não progride `status` para `mature` (decisão do usuário).
- Crítico é uma chamada de subagente por execução — sem loop de deliberação multi-rodada
  (YAGNI; pode virar evolução futura se a qualidade do gate não bastar).

---

## Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Custo/latência do subagente crítico | Uma única chamada cobre o pool inteiro; higiene não passa pelo crítico |
| Notas sem `fase:` (maioria fora das trilhas) | Fallback de inferência com default sênior |
| Crítico cortar algo que o usuário queria | Lista de descartados visível no plano, com resgate |
| Reescrita corromper a nota | Diff antes→depois aprovado item a item; substituição exata; relê arquivo antes de editar |
