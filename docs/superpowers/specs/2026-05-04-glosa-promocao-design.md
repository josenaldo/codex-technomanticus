---
title: "Spec — Pipeline de promoção de glosas e reorganização da documentação"
date: 2026-05-04
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Pipeline de promoção de glosas e reorganização da documentação

## 1. Contexto e motivação

O Codex Technomanticus organiza o conhecimento em quatro zonas operacionais (`01-Pergaminhos`, `02-Glosas`, `03-Dominios`, `04-Sendas`). O pipeline declarado é **pergaminho → glosa → nota de domínio**, mas a transição **glosa → domínio** nunca foi formalizada: como uma glosa "vira" parte do corpus, qual o vínculo entre ela e a nota resultante, qual o ciclo de vida de uma glosa após a promoção, e como o repositório de glosas se mantém legível quando crescer pra centenas/milhares de fichamentos.

Hoje, em 2026-05-04, o vault tem **uma única glosa** — momento ideal pra desenhar o pipeline limpo, com estrutura de pastas, frontmatter e skills antes que o uso real introduza débito.

A spec tem dois movimentos complementares:

1. **Pipeline de promoção de glosas**: define como uma glosa alimenta uma nota de domínio (modelo de relação, vínculos, frontmatter, ciclo de vida) e introduz quatro skills (`/promover-glosa`, `/sintetizar-glosas`, `/arquivar-glosas`, `/acordar-glosas`).
2. **Reorganização da documentação**: o guia atual (`00-Meta/guia/`) ganha uma subpasta `pipeline/` com cinco arquivos — visão geral + um por etapa do pipeline — substituindo o arquivo `sendas-e-dominios.md` criado na sessão anterior.

## 2. Objetivo

Entregar:

1. **Modelo conceitual** documentado: glosa permanece como artefato de leitura; notas de domínio nascem novas, citando glosas como fontes.
2. **Frontmatter ajustado** em `Template - Glosa.md` (campos `created`, `updated`, `promovida_em`).
3. **Frontmatter ajustado** em `Template - Nota.md` (seção `## Fontes` opcional).
4. **Estrutura física** de `02-Glosas/` com subpastas `Promovidas/<ano>/` e `Arquivadas/<ano>/`.
5. **Quatro skills** automatizando promoção, síntese, arquivamento e desarquivamento de glosas.
6. **Documentação reorganizada** em `00-Meta/guia/pipeline/` (5 arquivos), com substituição de `sendas-e-dominios.md`.
7. **Migração** da única glosa existente pra incorporar os novos campos.

## 3. Escopo

### Em escopo

- Atualização do `Template - Glosa.md` com `created`, `updated`, `promovida_em: []`.
- Atualização do `Template - Nota.md` com seção `## Fontes` opcional (comentada).
- Criação das pastas `02-Glosas/Promovidas/` e `02-Glosas/Arquivadas/` com `.gitkeep`.
- Migração frontmatter da única glosa existente (`02-Glosas/2026-design-md-spec-coding-agents.md`).
- Quatro skills em `.claude/skills/`: `promover-glosa`, `sintetizar-glosas`, `arquivar-glosas`, `acordar-glosas`.
- Reorganização do guia: criar `00-Meta/guia/pipeline/` com `index.md`, `Pergaminhos.md`, `Glosas.md`, `Domínios.md`, `Sendas.md`.
- Deletar `00-Meta/guia/sendas-e-dominios.md` (conteúdo migrado).

### Fora de escopo (trabalho subsequente)

- **Skill `/glosas-órfãs`**: varredura adicional listando glosas em raiz com decisão pendente há mais de N dias. Útil quando o vault tiver volume.
- **Dashboard cross-glosa no apocrypha**: visão consolidada de glosas, taxas de promoção, arquivamento. Mora no apocrypha — vide `docs/apocrypha-pendencias.md`.
- **Backfill em glosas antigas**: não há glosas antigas além da que será migrada na spec.
- **Geração automática de síntese textual**: a skill `/sintetizar-glosas` prepara o esqueleto da nota com `## Fontes` populada, mas **não** escreve a síntese em si. Síntese é voz própria; automatizar produz texto vazio.
- **Suporte a glosas de PDF/vídeo/podcast**: a skill `/glosa` atual só suporta artigos web. Extensão pra outros tipos é trabalho separado, fora desta spec.

## 4. Modelo conceitual

### 4.1 Glosa vs nota de domínio: naturezas distintas

| | Glosa | Nota de domínio |
|---|---|---|
| **Natureza** | Snapshot de leitura | Conhecimento sintetizado |
| **Voz** | Situada (TL;DR de uma fonte específica, citações, comentário pessoal) | Idiomática do vault (atemporal, integrativa) |
| **Datada** | Sim (campo `read`) | Vagamente (`created`/`updated`, mas o conteúdo é atemporal) |
| **Fontes** | Uma única — o material original | Múltiplas (incluindo glosas, observação, experiência) |
| **Pasta** | `02-Glosas/` | `03-Dominios/<X>/` |

A regra: **glosa não vira nota; ela alimenta nota.** Quando o tema merece consolidação no corpus, o usuário cria uma nota nova em `03-Dominios/`, com voz própria, citando a(s) glosa(s) como fontes.

### 4.2 Vínculo bidirecional

- **Da glosa pra nota:** campo `promovida_em: ["[[03-Dominios/X/Nota]]", ...]` (lista — uma glosa pode alimentar múltiplas notas).
- **Da nota pra glosa:** seção `## Fontes` no corpo da nota, com wikilinks pras glosas alimentadoras.

Razão pra duplicação: ambos os lados precisam ser navegáveis no Obsidian. A glosa "sabe" pra onde foi promovida; a nota "sabe" suas fontes. Atualização de ambos é responsabilidade das skills (não do usuário manualmente).

### 4.3 Ciclo de vida da glosa

```text
Criação (skill /glosa)
  ↓
[02-Glosas/<slug>.md]  progresso: andamento  promovida_em: []
  ↓
Leitura → o usuário marca progresso: feito (manualmente ou skill)
  ↓
Decisão:
  ├── Promover (skill /promover-glosa ou /sintetizar-glosas)
  │     ↓
  │     [02-Glosas/Promovidas/<ano>/<slug>.md]  promovida_em: [[Nota X]]
  │
  ├── Manter raiz (revisitará depois — fica até /arquivar-glosas pegar)
  │
  └── Abandonar (progresso: abandonado, fica raiz até arquivar)

Inatividade > 30 dias na raiz → /arquivar-glosas
  ↓
[02-Glosas/Arquivadas/<ano>/<slug>.md]
  ↓
Desarquivar (skill /acordar-glosas) → volta pra raiz como progresso: andamento
```

### 4.4 Princípio: nota nasce em estado preliminar

Quando uma glosa é promovida, a nota gerada nasce com:
- `status: seedling` (a nota é nova, não amadurecida).
- `progresso: andamento` (você acabou de começar — vai expandir, conectar, refinar).

Não nasce como `feito` mesmo que o conhecimento da glosa cubra o tema. A promoção é um **ponto de partida** pra nota, não um produto pronto.

## 5. Modelo de dados

### 5.1 `Template - Glosa.md` atualizado

Frontmatter alvo:

```yaml
---
title: "<% tp.file.title %>"
aliases: []
source: 
author: 
site: 
published: 
read: <% tp.date.now("YYYY-MM-DD") %>
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
type: glosa
status: lido
progresso: andamento
promovida_em: []
tags:
  - 
lang: 
publish: false
---
```

Mudanças vs. atual:
- **Adiciona** `created` (idêntico a `read` na criação, mas pode divergir se a glosa for criada após a leitura).
- **Adiciona** `updated` (atualizado a cada edição via skill ou manualmente).
- **Adiciona** `promovida_em: []` (lista de wikilinks — vazia inicialmente).

Nada é removido. O campo `read` permanece (data específica da leitura, semântica diferente de `created`).

### 5.2 `Template - Nota.md` atualizado

Adicionar seção opcional `## Fontes` entre `## Armadilhas comuns` e `## Aprofundamento`. Ordem final das seções:

```
## O que é
## Como funciona
## Quando usar
## Armadilhas comuns
## Fontes              ← NOVA
## Aprofundamento
## Veja também
```

Justificativa da ordem: `## Fontes` (de onde veio o conhecimento desta nota — fato histórico) precede `## Aprofundamento` (convites pra ler mais — futuro). Estrutura da seção:

```markdown
## Fontes

<!--
Glosas e outras fontes que alimentaram esta nota. Wikilinks pras glosas
em `02-Glosas/Promovidas/<ano>/` (ou raiz, se ainda não promovidas).
Skills /promover-glosa e /sintetizar-glosas populam essa seção
automaticamente.

- [[02-Glosas/Promovidas/2026/2026-exemplo-slug|Título da glosa]]
-->
```

A seção é opcional: notas sem fontes externas (escritas a partir de experiência ou observação direta) não precisam dela. Comentário HTML serve como guia pro usuário/skill.

### 5.3 Migração da glosa existente

A glosa `02-Glosas/2026-design-md-spec-coding-agents.md` precisa ganhar:
- `created: 2026-04-27` (mesma data de `read` — ela foi criada após leitura).
- `updated: 2026-05-04` (data de hoje, da migração).
- `promovida_em: []`.

Sem outras alterações no conteúdo.

## 6. Estrutura física

### 6.1 Layout de `02-Glosas/`

```text
02-Glosas/
├── <ano>-<slug>.md                ← raiz: ativas, recém-criadas, decisão pendente
├── Promovidas/
│   ├── .gitkeep
│   └── <ano>/
│       └── <ano-orig>-<slug>.md   ← arquivado por /promover-glosa ou /sintetizar-glosas
└── Arquivadas/
    ├── .gitkeep
    └── <ano>/
        └── <ano-orig>-<slug>.md   ← arquivado por /arquivar-glosas
```

### 6.2 Convenções de naming

- **Nome do arquivo é imutável.** Skill `/glosa` cria `<ano>-<slug>.md` (formato atual: o ano é da criação). Esse nome permanece em todas as movimentações de pasta.
- **`<ano>` na estrutura de subpasta é o ano da DECISÃO** (promoção ou arquivamento), não o ano da glosa em si. Razão: organiza por época da decisão, útil pra "que glosas eu promovi/arquivei em 2027?".

Exemplo:
- Glosa criada em 2026-04-27: `02-Glosas/2026-design-md-spec-coding-agents.md`.
- Promovida em 2027-03-15: `02-Glosas/Promovidas/2027/2026-design-md-spec-coding-agents.md`.

### 6.3 Wikilinks após movimento

Obsidian resolve wikilinks por nome do arquivo. Mover de `02-Glosas/<slug>.md` pra `02-Glosas/Promovidas/<ano>/<slug>.md` não quebra wikilinks existentes, **desde que o nome do arquivo seja único no vault**. Como `<ano>-<slug>` da skill `/glosa` é único por construção, isso é seguro.

**Risco de colisão:** se duas glosas (improvavelmente) tivessem o mesmo `<slug>`, Obsidian fica ambíguo. **Mitigação:** as skills validam antes de mover — se já existe arquivo com o mesmo nome no destino, abortam com erro claro.

### 6.4 `.gitkeep` em pastas vazias

`Promovidas/` e `Arquivadas/` nascem vazias. Pra que o git versione os diretórios, cada uma recebe um `.gitkeep` vazio.

## 7. Critério temporal pra arquivamento

A skill `/arquivar-glosas` precisa medir "inatividade" da glosa. Usa:

```python
idade_inativa = hoje - max(updated, mtime)
arquivar se idade_inativa > 30 dias
```

- **`updated`** (campo do frontmatter): atualizado pelas skills a cada interação significativa (promoção, anotação, alteração explícita).
- **`mtime`** (filesystem): atualizado por qualquer edição via Obsidian.
- **`max` dos dois**: qualquer atividade conta. Robusto contra `mtime` resetado por operações de filesystem (rebase, cópia entre máquinas) e contra falta de atualização do `updated` manual.
- **Glosas sem `updated`** (glosas antigas, criadas antes desta spec): cai no `mtime` puro.

**Critério aplica a TUDO na raiz** — independente de `progresso`. Glosa em `andamento` há 30 dias sem mexer significa abandono tácito; arquiva.

## 8. Skills

### 8.1 `/promover-glosa`

**Propósito:** transformar UMA glosa em ponto de partida de uma nota de domínio.

**Sintaxe:**
- `/promover-glosa <slug>` — slug da glosa específica.
- `/promover-glosa` (sem argumento) — modo interativo: lista glosas em raiz com `progresso: feito` ou `andamento`, usuário escolhe.

**Fluxo:**
1. Lê a glosa: extrai `title`, `tags`, `TL;DR`.
2. **Sugere domínio destino** com base nas tags da glosa (heurística: cada tag mapeia opcionalmente pra um domínio; tag mais específica vence). Apresenta sugestão; usuário confirma ou escolhe outro domínio interativamente.
3. **Sugere nome da nota.** Default: derivar do `title` da glosa simplificado pro conceito principal. Pede confirmação; usuário pode digitar outro.
4. **Verifica se a nota já existe** em `03-Dominios/<X>/<Nome>.md`. Se sim: pergunta se quer (a) anexar a glosa às fontes da nota existente, (b) escolher outro nome, (c) cancelar.
5. **Cria a nota** usando `Template - Nota.md` (caminho absoluto resolvido), com:
   - Frontmatter: `progresso: andamento`, `status: seedling`, tags = (tags-da-glosa ∪ tags-do-domínio), `created`/`updated` = hoje.
   - `## O que é` pré-populada com a TL;DR da glosa entre comentários: `<!-- ponto de partida da glosa: ... -->`.
   - `## Fontes` populada com `[[02-Glosas/Promovidas/<ano>/<slug>|título-da-glosa]]`.
   - Outras seções (`## Como funciona`, `## Quando usar`, etc.) ficam vazias com seus comentários originais.
6. **Move a glosa** de `02-Glosas/<slug>.md` pra `02-Glosas/Promovidas/<ano-atual>/<slug>.md`.
7. **Atualiza frontmatter da glosa**: `promovida_em: ["[[03-Dominios/<X>/<Nome>]]"]`. Atualiza `updated` pra hoje.
8. **Atualiza `progresso`** da glosa pra `feito` (se ainda estiver `andamento`).
9. Reporta: caminhos dos dois arquivos modificados/criados.

**Idempotência:**
- Glosa já em `Promovidas/`: append em `promovida_em` (lista cresce), cria nova nota normalmente, não re-move.
- Glosa não existe: erro claro.
- Domínio não existe: pergunta se quer criar (mas isso é fora do fluxo principal — recomenda criar via outra skill futura).

### 8.2 `/sintetizar-glosas`

**Propósito:** consolidar VÁRIAS glosas em UMA nota de domínio.

**Sintaxe:**
- `/sintetizar-glosas tag:<X>` — todas as glosas com tag `<X>`.
- `/sintetizar-glosas <assunto>` — busca textual em títulos/TL;DRs.
- `/sintetizar-glosas` (sem argumento) — modo interativo: usuário escolhe filtro.

**Fluxo:**
1. Filtra glosas (raiz + Promovidas — ambas podem alimentar) que casam com o critério.
2. Lista as candidatas (slug + título + tags + status). Usuário **seleciona**: default todas marcadas; pode tirar.
3. Lê o conteúdo de cada selecionada (TL;DR + pontos-chave).
4. **Sugere domínio + nome da nota** baseado nas tags comuns (interseção das tags das glosas).
5. **Cria nota** em `03-Dominios/<X>/<Nome>.md`:
   - Frontmatter idêntico a `/promover-glosa` (progresso, status, tags consolidadas).
   - Conteúdo: skeleton com seções padrão `## O que é`, `## Como funciona`, etc., **vazias com comentários** (não tenta gerar a síntese textual — voz própria do usuário).
   - `## Fontes` populada com wikilinks pras N glosas selecionadas.
6. **Move cada glosa selecionada que ainda esteja na raiz** pra `Promovidas/<ano-atual>/`.
7. **Atualiza `promovida_em` em cada uma** com o novo wikilink. Atualiza `updated` pra hoje.
8. Reporta: lista de arquivos movidos + novo arquivo criado.

**Idempotência:**
- Glosas já em `Promovidas/`: append em `promovida_em`, não re-move. Glosas em raiz: move normalmente.
- Mistura de raiz + promovidas no input é OK.

### 8.3 `/arquivar-glosas`

**Propósito:** mover pra arquivo glosas inativas há mais de 30 dias na raiz.

**Sintaxe:**
- `/arquivar-glosas` — varredura.

**Fluxo:**
1. Varre `02-Glosas/` raiz (não desce em `Promovidas/` ou `Arquivadas/`).
2. Pra cada arquivo, calcula `idade_inativa = hoje - max(updated, mtime)`.
3. Lista candidatas (>30d) com: nome, idade, tags, `progresso`.
4. **Pede confirmação interativa**: "arquivar todas? deselecionar? cancelar?". Usuário pode tirar itens da seleção.
5. Move as confirmadas pra `02-Glosas/Arquivadas/<ano-atual>/<slug>.md`.
6. Reporta: lista de arquivos movidos.

**Idempotência:**
- Sem candidatas: reporta "nada a arquivar" e sai.
- `Arquivadas/` já contém arquivo com mesmo nome: aborta com erro (deve ser raríssimo).

### 8.4 `/acordar-glosas`

**Propósito:** reativar glosas previamente arquivadas.

**Sintaxe:**
- `/acordar-glosas <slug>` — uma glosa específica.
- `/acordar-glosas tag:<X>` — todas as glosas arquivadas com tag `<X>`.
- `/acordar-glosas <assunto>` — busca textual.
- `/acordar-glosas` (sem argumento) — modo interativo.

**Fluxo:**
1. Filtra `02-Glosas/Arquivadas/**` por critério.
2. Lista candidatas com: nome, ano de arquivamento, tags, último `updated`.
3. **Pede confirmação interativa** (mesma UX da `/arquivar-glosas`).
4. Move as confirmadas: `Arquivadas/<ano>/<slug>.md` → `02-Glosas/<slug>.md` (raiz).
5. **Reseta `progresso`** pra `andamento`. Atualiza `updated` pra hoje.
6. Reporta: lista de arquivos movidos.

**Idempotência:**
- Glosa que não está arquivada: warning + skip.
- Conflito de nome na raiz (arquivo já existe): aborta com erro.

### 8.5 Convenções comuns às skills

- **Confirmação interativa**: skills que afetam múltiplos arquivos (`/sintetizar-glosas`, `/arquivar-glosas`, `/acordar-glosas`) sempre pedem confirmação antes de mover/criar. `/promover-glosa` afeta uma única glosa — pede confirmação só pro nome da nota e domínio destino.
- **Atualização de `updated`**: toda operação que altera frontmatter atualiza `updated`.
- **Não tocam no apocrypha**: todas as skills atuam apenas em `codex-technomanticus`.
- **Erros**: skills reportam erro humano-legível (não stack trace) e param. Não tentam "consertar" estados ambíguos automaticamente.

## 9. Reorganização da documentação

### 9.1 Nova estrutura

```
00-Meta/guia/
├── (existentes, sem mudar)
│   ├── Como usar este vault.md
│   ├── Convenções de escrita.md
│   ├── Decisões do vault.md
│   ├── Manutenção do vault.md
│   ├── Publicação.md
│   ├── Wikilinks e MOCs.md
│   ├── workflow.md
│   └── Dicionario de Magia Tecnomante.md
└── pipeline/                      ← NOVO
    ├── index.md                   ← visão geral do pipeline
    ├── Pergaminhos.md             ← etapa 1: captura
    ├── Glosas.md                  ← etapa 2: fichamento + promoção
    ├── Domínios.md                ← corpus
    └── Sendas.md                  ← mapas
```

### 9.2 Conteúdo de cada arquivo

**`pipeline/index.md`** — visão geral:

- Frase-resumo: "Pipeline de transformação do conhecimento no Codex".
- Diagrama em texto (`pergaminho → glosa → domínio` + sendas como mapa transversal).
- Princípios gerais: domínios = estantes, sendas = fluxograma, glosa = snapshot de leitura.
- Links pros 4 arquivos da subpasta.
- Links pra docs adjacentes (`workflow.md`, `Como usar este vault.md`).

**`pipeline/Pergaminhos.md`** — etapa 1:

- O que vai aqui: links soltos, ideias cruas, capturas de chat com LLMs, anotações imediatas.
- Estrutura da pasta `01-Pergaminhos/` (em particular, `entradas.md` como inbox).
- Como passa pra próxima etapa: skill `/glosa <url>` lê o pergaminho ou URL e produz uma glosa.

**`pipeline/Glosas.md`** — etapa 2 (esta spec, na maior parte):

- O que é uma glosa, voz situada, estrutura (template).
- Frontmatter completo com explicação de cada campo (`read`, `created`, `updated`, `progresso`, `promovida_em`).
- Estados de uma glosa (`andamento`, `feito`, `abandonado`, promovida, arquivada, acordada).
- Estrutura de pastas (`raiz`, `Promovidas/`, `Arquivadas/`).
- Promoção: explica `/promover-glosa` e `/sintetizar-glosas` em alto nível (sintaxe + fluxo resumido).
- Manutenção: `/arquivar-glosas` e `/acordar-glosas`, critério dos 30 dias.

**`pipeline/Domínios.md`** — etapa 3:

- O que é um domínio (estante).
- Modelo de organização (linguagens próprias, libs grandes, disciplinas cross-tech).
- Estrutura de uma nota de domínio (template, `## Fontes`, callout `[!convite]`).
- Convite `[!convite]` — convenção e exemplos.
- Maturidade da nota (`status: seedling/budding/evergreen`) e progresso de estudo (`progresso`).
- Como uma glosa promovida aparece aqui via `## Fontes`.

**`pipeline/Sendas.md`** — mapas:

- O que é uma senda (fluxograma sobre os domínios).
- O que ela contém / não contém.
- Formas `minimal` vs `structured`.
- Frontmatter (`type: trail`, `domain`, `maturity`, etc.).
- Bloco dataview de progresso.

### 9.3 Migração de `sendas-e-dominios.md`

O arquivo `00-Meta/guia/sendas-e-dominios.md` (criado em 2026-05-03 na sessão da spec de progresso-sendas) é redundante com a nova estrutura. Conteúdo redistribuído:

- "As quatro zonas e o pipeline" → `pipeline/index.md`.
- "Domínios = estantes; Sendas = fluxograma" → `pipeline/index.md` (princípio geral) + `pipeline/Domínios.md` + `pipeline/Sendas.md`.
- "Organização dos domínios (modelo de estantes)" → `pipeline/Domínios.md`.
- "Campo `progresso` no frontmatter" → `pipeline/Domínios.md` (e mencionado em `pipeline/Glosas.md`).
- "Callout `[!convite]`" → `pipeline/Domínios.md`.

Após a redistribuição, **deletar** `00-Meta/guia/sendas-e-dominios.md`. Não deixar redirect — não é necessário pra um vault de leitor único.

## 10. Repos afetados

| Repo | O que muda |
|---|---|
| `codex-technomanticus` | Templates (Glosa, Nota), estrutura `02-Glosas/`, 4 skills em `.claude/skills/`, reorganização do guia, migração da glosa existente |
| `codex-technomanticus-site` | **Não toca**. As skills são consumidas via Obsidian + Claude Code; o site só renderiza markdown |
| `codex-technomanticus-apocrypha` | **Não toca**. Pendências catalogadas em `docs/apocrypha-pendencias.md` |

## 11. Plano de execução (ordem sugerida)

1. Atualizar `Template - Glosa.md` (campos novos no frontmatter).
2. Atualizar `Template - Nota.md` (seção `## Fontes` opcional).
3. Migrar a glosa existente (`2026-design-md-spec-coding-agents.md`) com os novos campos.
4. Criar `02-Glosas/Promovidas/.gitkeep` e `02-Glosas/Arquivadas/.gitkeep`.
5. Criar a subpasta `00-Meta/guia/pipeline/` e os 5 arquivos (`index.md`, `Pergaminhos.md`, `Glosas.md`, `Domínios.md`, `Sendas.md`).
6. Deletar `00-Meta/guia/sendas-e-dominios.md`.
7. Criar skill `/promover-glosa` em `.claude/skills/promover-glosa/SKILL.md`.
8. Criar skill `/sintetizar-glosas` em `.claude/skills/sintetizar-glosas/SKILL.md`.
9. Criar skill `/arquivar-glosas` em `.claude/skills/arquivar-glosas/SKILL.md`.
10. Criar skill `/acordar-glosas` em `.claude/skills/acordar-glosas/SKILL.md`.
11. Validação manual: criar 1-2 glosas de teste, rodar cada skill, confirmar movimentos.

## 12. Riscos e validações

| Risco | Mitigação |
|---|---|
| Skills movem arquivos errados (bugs) | Confirmação interativa antes de mover; testes manuais com glosas-teste descartáveis |
| Wikilinks quebram após movimento | Obsidian resolve por nome do arquivo; verificar pós-movimento que `[[<slug>]]` ainda resolve |
| Conflito de nomes na pasta destino | Skills checam antes de mover; abortam com erro claro |
| `mtime` resetado por sync (Dropbox, iCloud) | Fallback `updated` no frontmatter; `max(updated, mtime)` cobre |
| Skill cria nota em domínio errado | Sugestão por tags + confirmação humana antes de criar |
| Glosa promovida 2x cria notas duplicadas | Skill detecta nota existente; pergunta antes de criar |
| Síntese automática vira bullshit | Skill explicitamente NÃO gera síntese textual; só prepara skeleton |

## 13. Trabalhos subsequentes sugeridos

1. **Skill `/glosas-órfãs`**: lista glosas em raiz com decisão pendente há mais de N dias (tipo 7d). Útil quando o vault tiver volume.
2. **Dashboard de glosas no apocrypha**: visão consolidada — taxa de promoção, glosas mais antigas em fila, top tags.
3. **Suporte a fontes não-web** (PDF, vídeo, podcast) na skill `/glosa` original.
4. **Indexação automática de tags por domínio**: skill que lê tags atuais do vault e sugere mapeamento tag → domínio (pra alimentar `/promover-glosa`).
5. **Visualização de grafo glosa↔nota**: aproveitar grafo do Obsidian, mas com filtro/cor por tipo (glosa vs nota).

## 14. Aceitação

A spec é considerada implementada quando:

- [ ] `Template - Glosa.md` tem `created`, `updated`, `promovida_em: []`.
- [ ] `Template - Nota.md` tem seção `## Fontes` opcional comentada.
- [ ] Glosa existente migrada com os novos campos.
- [ ] `02-Glosas/Promovidas/` e `02-Glosas/Arquivadas/` criadas com `.gitkeep`.
- [ ] As 4 skills criadas em `.claude/skills/<nome>/SKILL.md` com SKILL frontmatter completo (`name`, `description`).
- [ ] Subpasta `00-Meta/guia/pipeline/` criada com 5 arquivos preenchidos.
- [ ] `00-Meta/guia/sendas-e-dominios.md` deletado.
- [ ] Validação manual: criar uma glosa de teste, rodar `/promover-glosa`, verificar que (a) glosa moveu pra `Promovidas/<ano>/`, (b) nota nasceu em `03-Dominios/X/Y.md` com `## Fontes` correto, (c) `promovida_em` da glosa atualizado.
- [ ] Validação manual: rodar `/arquivar-glosas` numa glosa de teste com `updated` antiga, verificar movimento pra `Arquivadas/`.
- [ ] Validação manual: rodar `/acordar-glosas` na glosa arquivada, verificar volta pra raiz e reset de `progresso`.
- [ ] Validação manual: rodar `/sintetizar-glosas` com 2+ glosas, verificar que nota é criada com todas as fontes e cada glosa foi movida.
