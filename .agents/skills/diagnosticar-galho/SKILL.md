---
name: diagnosticar-galho
description: >
  Audita um galho de notas nota a nota e gera `<galho>/roadmap.md` com uma entrada executável
  por nota (estado, score, plano de execução, classificação de custo). É a cristalização do
  processo de diagnóstico feito manualmente no domínio IA e funciona como pré-condição da
  `enriquecer-galho`. Use quando o usuário pedir "diagnosticar galho", "criar roadmap de
  enriquecimento do galho", ou quando a skill `enriquecer-galho` detectar que `roadmap.md`
  ainda não existe na pasta do galho.
---

# Skill: diagnosticar-galho

Audita um galho inteiro — uma nota por vez, com ≤3 subagentes concorrentes — e produz
`<galho>/roadmap.md` com uma entrada executável por nota. Não edita nenhuma nota do galho;
é **estritamente read-only nas notas**. Quando termina, para e aguarda revisão humana.

## Invocação

```
/diagnosticar-galho <path-do-galho>
```

- **`<path-do-galho>`:** caminho absoluto (ou relativo à raiz do vault) para a pasta do galho.
  Ex: `03-Dominios/Tecnologia/IA/Anatomia dos LLMs`.
- Se `<galho>/roadmap.md` já existir, aborta com aviso: "roadmap.md já existe — use
  `enriquecer-galho` para executar ou delete-o para rediagnosticar."

---

## Fase 0 — Inventário

**Objetivo:** conhecer o galho antes de criar qualquer arquivo.

1. Liste todos os `.md` da pasta do galho (não recursivo — só o nível imediato), excluindo
   `index.md` e `roadmap.md`.
2. Identifique **brotos**: arquivos cujo nome termina em letra minúscula após o número
   (padrão `Xa`, `Xb` — ex: `04a.md`, `04b.md`). Brotos são isentos do piso de linhas
   (T1/T2/T3 não se aplica).
3. Detecte o **esquema de `fase:`** do galho:
   - Para cada nota, grepe o campo `fase:` no frontmatter.
   - Se ≥50% das notas usam `Iniciado`, `Adepto` ou `Magus` → esquema **COM fase**
     (piso de linhas é obrigatório: Iniciado ≥300, Adepto ≥400, Magus ≥500).
   - Se ≥50% das notas não têm `fase:` → esquema **SEM fase** (organizado por sequência
     ou Blocos; ausência de `fase:` NÃO é gap).
   - Se ambíguo (ex: galho em transição), registre como "misto" e documente no cabeçalho.
4. Registre: total de notas, lista de brotos identificados, esquema detectado.

---

## Fase 1 — Semeadura

**Objetivo:** criar `<galho>/roadmap.md` com estrutura inicial e um placeholder por nota.

Crie o arquivo via append (`cat >> ... <<'EOF'`) para robustez contra reescrita:

```
---
title: "Roadmap — <nome-do-galho>"
created: <YYYY-MM-DD>
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — <nome-do-galho>

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `<path-relativo>`
**Diagnóstico:** <YYYY-MM-DD>
**Última execução:** —

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** <COM fase (Iniciado/Adepto/Magus) | SEM fase (sequência/Blocos) | misto>
**Piso de linhas:** <aplicável: Iniciado ≥300 / Adepto ≥400 / Magus ≥500 | não aplicável>

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | <N> |
| ⬜ pendente | — |
| ➖ não precisa | — |
| ✅ feita | — |
| % concluído | — |

> Tabela preenchida ao final do diagnóstico (Fase 3).

---

## Notas

```

Em seguida, para cada nota na lista do inventário (em ordem de nome de arquivo), anexe
um placeholder:

```
<!-- nota: <nome-do-arquivo.md> -->
```

Feche o arquivo. O `roadmap.md` agora tem tantos placeholders quantas notas há no galho.

---

## Fase 2 — Análise nota a nota

**Objetivo:** substituir cada placeholder pela entrada executável da nota.

Dispare **subagentes em lotes de ≤3 concorrentes**. Cada subagente recebe o prompt abaixo
(LITERAL — copie integralmente, substituindo apenas os valores entre `<>`).

### Prompt-template do subagente (LITERAL)

```
Você é um auditor de notas do vault Codex Technomanticus. Sua tarefa é analisar UMA nota
e gravar a entrada dela no roadmap do galho.

## Dados da tarefa

- **Nota a analisar:** `<path-absoluto-da-nota>`
- **Roadmap:** `<path-absoluto-do-roadmap.md>`
- **Placeholder a substituir:** `<!-- nota: <nome-do-arquivo.md> -->`
- **Esquema de fase do galho:** <COM fase | SEM fase | misto>
- **É broto?** <SIM (isento do piso T1/T2/T3) | NÃO>

## Régua de análise (12 itens com isenções)

### ESTRUTURA
- E1: TL;DR callout `> [!abstract]` com ≥3 linhas densas
- E2: Abertura com problema/cenário real (não começa com "X é um…")
- E3: ≥1 diagrama Mermaid com semântica visual (não decorativo)
- E4: Seção `## Casos práticos` com ≥2 cenários de produção concretos
- E5: Seção `## O que vem a seguir` — ponte narrativa, não só lista de links
- E6: Seção de inglês presente (nome exato ou variação equivalente)
- E7: Tabela de termos técnicos PT ↔ EN
- E8: Seção `## Armadilhas comuns` com ≥3 callouts `[!warning]` individuais

### PROFUNDIDADE
- P1: Exemplo de código mostra ≥1 caso-problema (não só caminho feliz) — N/A para nota conceitual pura
- P2: Nota explica *por quê* funciona, não apenas *o quê*

### LINKS
- L1: ≥1 `[[wikilink]]` apontando para nota fora da pasta atual
- L2: Seção `## Fontes` com ≥1 link externo verificável (URL clicável, não citação em prosa)

### MÍDIA
- M1: ≥1 callout `[!tip]` com link para vídeo/podcast relevante

### Isenções aplicáveis
- Brotos (filename `Xa`/`Xb`): isentos de T1/T2/T3 (piso de linhas)
- Esquema SEM fase: ausência de `fase:` NÃO é gap; não cobrar T1/T2/T3 como item automático
- `fase: Iniciado` ou `fase: Adepto`: P3 (teoria subjacente) não se aplica
- Notas `type: meta` ou `type: glossary`: isentas de E6 e E7
- Notas sem seção de código: P1 marcado como N/A

## Como executar

1. **Leia a nota inteira** (`<path-absoluto-da-nota>`).
2. **Conte as linhas REAIS**: use `wc -l` e subtraia linhas em branco de rodapé (linhas em
   branco contíguas ao final do arquivo inflam a contagem e não representam conteúdo).
   Reporte o número real.
3. **Extraia do frontmatter**: `fase:`, `status:`, `type:`.
4. **Audite cada um dos 12 itens** da régua, aplicando isenções.
5. **Calcule o score**: N/12 (considerando isenções — itens isentos não contam para o teto).
6. **Classifique o custo** da correção:
   - `[mecânico]`: correções baratas sem pesquisa web — incluem: expandir TL;DR existente,
     adicionar URLs já inferíveis do contexto, converter abertura para problema/cenário,
     converter ASCII/lista de armadilhas para `[!warning]`, adicionar seção "O que vem a
     seguir" com wikilink para a próxima nota da sequência.
   - `[substantivo]`: requer pesquisa, expansão real de conteúdo ou reescrita de seção —
     incluem: expandir nota abaixo do piso adicionando conteúdo técnico novo, pesquisar
     fato novo ou URL externa verificável, criar seção de casos práticos com cenários de
     produção, reescrever seção com mecanismo ausente.
   - Se a nota tem gaps mecânicos E substantivos, classifique pela ação dominante (maior
     esforço define a classe do bloco).
7. **Decida o estado inicial**:
   - `➖ não precisa`: score ≥9/12 E nenhum item de núcleo faltando (núcleo = E1, E2, E5,
     L2, P2 presentes) — nunca entra no loop de execução.
   - `⬜ pendente`: qualquer item de núcleo ausente OU score <9/12 — entra no loop.
8. **Escreva o plano de execução**: ações concretas, enumeradas, suficientes para aplicar
   sem re-planejar. Cada ação deve citar o item da checklist que resolve (ex: "→ ativa E8").
   Se estado = `➖`, escreva "— nenhuma".
9. **Substitua o placeholder exato** `<!-- nota: <nome-do-arquivo.md> -->` no roadmap pela
   entrada formatada (via Edit, substituição exata do placeholder como old_string).
   **Não edite nenhum outro trecho do roadmap.**

## Formato da entrada (EXATO — não altere a estrutura)

#### <NN> - <Título da nota>   [mecânico | substantivo]
- **Enriquecimento:** ⬜ pendente | ➖ não precisa
- **Estado:** <N linhas reais> linhas · fase: <valor|ausente> · status: <valor>
- **Núcleo/gaps:** <lista dos itens da checklist que falham; "—" se nenhum>
- **Score:** <N>/12
- **Plano de execução:**
  - <ação 1 — cita item que resolve>
  - <ação 2 — cita item que resolve>
- **Resultado:** —

### Regras do formato
- `NN` = número do arquivo sem extensão (ex: `01`, `04a`).
- A linha `#### …` termina com `[mecânico]` ou `[substantivo]` (sem barra — só um dos dois).
- `Enriquecimento` recebe apenas `⬜ pendente` ou `➖ não precisa` (os outros estados são
  preenchidos pelo loop de execução do `enriquecer-galho`).
- `Resultado` fica sempre `—` ao sair do diagnóstico.
- Não acrescente campos extras; não omita campos existentes.

## Restrição crítica

**Não edite o conteúdo das notas.** Você só pode escrever no `roadmap.md`, substituindo
o placeholder designado. Qualquer edição em nota de conteúdo é proibida.
```

### Controle de concorrência

- Dispare no máximo **3 subagentes por lote**.
- Aguarde o lote completar antes de disparar o próximo.
- Modelo dos subagentes: **Sonnet** (herda via `CLAUDE_CODE_SUBAGENT_MODEL`; não forçar Opus).
- Ordem de processamento: mesma ordem do inventário (por nome de arquivo).

---

## Fase 3 — Fecho

**Objetivo:** verificar integridade e preencher a tabela-resumo. Não inicia execução.

1. **Valide** que não há `<!-- nota: … -->` restante no `roadmap.md` (todos substituídos).
   Se houver placeholder remanescente, re-dispare o subagente daquela nota.
2. **Preencha a tabela-resumo** no cabeçalho do roadmap:
   - Total de notas diagnosticadas.
   - Contagem de `⬜ pendente`, `➖ não precisa`, `✅ feita` (zero neste ponto).
   - % concluído = `✅ / total × 100` (zero neste ponto — roadmap acabou de ser criado).
3. **Informe o usuário:**
   ```
   Diagnóstico concluído — <N> notas auditadas em <galho>.
   roadmap.md criado em: <path-roadmap>
   ⬜ pendente: <N>   ➖ não precisa: <N>
   Revise o roadmap antes de executar. Use `/enriquecer-galho <path>` para iniciar.
   ```
4. **PARE.** O diagnóstico é revisado pelo usuário antes de qualquer execução.
   Não chame `enriquecer-nota`, não edite nenhuma nota do galho.

---

## Formato EXATO da entrada por nota

Referência canônica para o que cada subagente deve produzir (ver também a seção
"Entrada por nota" do design `00-Meta/specs/2026-07-01-enriquecer-galho-design.md`):

```
#### NN - Título da nota   [mecânico | substantivo]
- **Enriquecimento:** ⬜ pendente | ➖ não precisa
- **Estado:** <N> linhas reais · fase: <X|ausente> · status: <valor>
- **Núcleo/gaps:** <itens do checklist que falham — ex: E2, E5, L2 · "—" se nenhum>
- **Score:** N/12
- **Plano de execução:**
  - <ação 1 concreta — cita o item que resolve>
  - <ação 2 concreta — cita o item que resolve>
- **Resultado:** —
```

### Máquina de estados (fonte de verdade)

| Estado | Significado | Quem define |
|--------|-------------|-------------|
| `⬜ pendente` | Diagnosticada; aguarda execução | Subagente de diagnóstico |
| `➖ não precisa` | Sem gap relevante; nunca entra no loop | Subagente de diagnóstico |
| `🔄 em andamento` | Subagente de execução despachado | Loop do `enriquecer-galho` |
| `✅ feita (YYYY-MM-DD)` | Execução concluída e gravada | Loop do `enriquecer-galho` |

**O loop de execução toca apenas `⬜`.** `🔄` protege contra re-despacho concorrente.
Um galho só é considerado "enriquecido" quando há zero `⬜` e zero `🔄`.

---

## Classificação de custo — referência rápida

| Custo | Definição | Exemplos de ação |
|-------|-----------|-----------------|
| `[mecânico]` | Correção barata, sem pesquisa web | Expandir TL;DR · converter abertura para problema/cenário · transformar lista de armadilhas em `[!warning]` · converter ASCII para Mermaid · adicionar seção "O que vem a seguir" com wikilink para próxima nota · adicionar URLs inferíveis do contexto |
| `[substantivo]` | Requer pesquisa, expansão real ou reescrita | Expandir conteúdo para atingir piso de linhas · pesquisar e verificar URL externa · criar casos práticos com cenários de produção · reescrever seção ausente de mecanismo causal · pesquisar vídeo/podcast relevante para M1 |

A classe do bloco é determinada pela **ação dominante** (maior esforço):
uma nota com duas ações mecânicas e uma substantiva é classificada `[substantivo]`.

No loop de execução (`enriquecer-galho`):
- `[mecânico]` → subagente Haiku, effort low.
- `[substantivo]` → subagente Sonnet.

---

## Convenções rígidas

1. **Teto de 3 concorrentes** — nunca mais de 3 subagentes de análise rodando ao mesmo tempo.
2. **Read-only nas notas** — esta skill não edita nenhum arquivo de conteúdo do galho;
   escreve exclusivamente no `roadmap.md`.
3. **Não fabricar dados do usuário** — plano de execução deve derivar do conteúdo real lido;
   nunca inventar exemplos, projetos ou experiências que não estejam na nota.
4. **Um subagente por nota** — nunca paralelizar mais de uma nota por subagente.
5. **Grava só no roadmap** — o único arquivo que esta skill cria ou modifica é `<galho>/roadmap.md`.
6. **Redundância entre notas é reforço** — não propor deduplicação de conteúdo repetido
   entre notas; linkar em vez de podar.
7. **Parar após o diagnóstico** — a Fase 3 termina com `STOP`; não invoca nenhuma skill de execução.
8. **Append via heredoc** — na Fase 1, use `cat >> ... <<'EOF'` para criar o roadmap; não
   abra o arquivo via Write/Edit em chunk único (risco de conflito se o Obsidian tiver o
   arquivo aberto).
