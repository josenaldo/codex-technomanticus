---
title: "Suíte enriquecer-galho — coordenação de enriquecimento por galho"
created: 2026-07-01
type: spec
status: draft
publish: false
tags:
  - meta
  - spec
  - skills
  - enriquecimento
---

# Suíte `enriquecer-galho` — design

## Problema

Enriquecer um domínio inteiro (ex: IA, 237 notas) é uma tarefa longa, que precisa
ser dividida em partes e rodar por **semanas**, aproveitando o **excedente** de tokens
sem roubar da janela do trabalho principal. As rodadas manuais anteriores falharam em três
pontos concretos:

1. **Double-work** — a mesma nota foi enriquecida mais de uma vez (perda de rastro de estado).
2. **Galho-falso** — galhos marcados como enriquecidos sem terem sido.
3. **Fan-out explosivo** — subagentes demais em paralelo queimaram a janela de 5h em <10 min.

## Objetivo

Um processo **repetível, resumível e genérico** (qualquer galho, qualquer domínio, qualquer
profundidade) que enriquece um galho nota a nota, com **governança de tokens rígida** e
**memória permanente em disco**, de modo que possa ser interrompido e retomado a qualquer
momento sem perder trabalho nem repetir trabalho.

## Não-objetivos

- Não é específico do domínio IA — serve a qualquer pasta de notas de domínio.
- Não substitui a `escrever-nota` (criação do zero) nem a `verificar-nota` (auditoria read-only).
- Não roda em foreground disputando tokens com o trabalho principal — é **baixa prioridade**.

---

## Arquitetura

Suíte de **duas skills novas** + **uma modificação** numa skill existente.

### `enriquecer-galho <path-do-galho>` — coordenador (roda em Opus / opusplan)

Ponto de entrada único. Recebe o caminho de uma pasta de galho.

- Se **não existe** `<path>/roadmap.md` → invoca `diagnosticar-galho` e **para** (o diagnóstico
  é revisado antes de qualquer execução).
- Se **existe** `<path>/roadmap.md` → entra no **loop de execução** (ver abaixo).

O coordenador é quem detém o estado da sessão (contador das 15, governança de tokens) e nunca
delega essas decisões a subagentes.

### `diagnosticar-galho <path-do-galho>` — micro-skill

Gera `<path>/roadmap.md` com **uma entrada executável por nota**. É o que foi feito
manualmente na auditoria do domínio IA, agora cristalizado e generalizado.

### `enriquecer-nota` — ganha modo `--auto` (não-interativo)

Modo novo na skill existente, reusável de dois jeitos:

- **No fluxo do galho:** recebe o **plano já aprovado no diagnóstico** (via argumento/instrução) e
  aplica direto — **sem menu de lentes, sem gate de confirmação, e SEM disparar o subagente
  crítico**. Isso é obrigatório para respeitar o teto de concorrência (ver Governança).
- **Avulso:** o usuário pode chamar `/enriquecer-nota <path> --auto "<instrução>"` para uma nota
  única, quando quiser, fora do fluxo de galho.

> Onde vivem as skills: `.agents/skills/` (symlink `→ .claude/skills`). Uma cópia só.

---

## `roadmap.md` — memória permanente por galho

Vive **dentro da pasta do galho** (`<galho>/roadmap.md`), frontmatter `type: meta`,
`publish: false`. Contém só os dados daquele galho — zero ambiguidade, localidade total.

### Estrutura

- **Cabeçalho:** nome do galho, régua de análise (padrão das skills), datas de diagnóstico/execução.
- **Tabela-resumo** do galho: total de notas, distribuição de estados, % concluído.
- **Uma entrada por nota**, no formato executável abaixo.

### Entrada por nota (formato executável)

```
#### NN - Título   [mecânico | substantivo]
- **Enriquecimento:** ⬜ pendente | 🔄 em andamento | ✅ feita (YYYY-MM-DD) | ➖ não precisa
- **Estado:** <N> linhas reais · fase: <X|ausente> · status: <frontmatter>
- **Núcleo/gaps:** <itens do checklist verificar-nota que falham>
- **Score:** N/12
- **Plano de execução:** (instruções concretas o suficiente para aplicar sem re-planejar)
  - <ação 1>
  - <ação 2>
- **Resultado:** <preenchido na execução: o que foi feito, novo score, ou "—">
```

### Máquina de estados (fonte de verdade contra double-work e galho-falso)

- `➖ não precisa` — derivado do diagnóstico (nenhum gap relevante); **nunca entra no loop**.
- `⬜ pendente` — diagnosticada, aguardando execução. **O loop só toca `⬜`.**
- `🔄 em andamento` — marcada ao despachar o subagente (protege contra re-despacho concorrente).
- `✅ feita (data)` — marcada ao concluir e gravar o resultado.

**Regra de conclusão do galho:** o galho só é considerado "enriquecido" quando há **zero `⬜` e
zero `🔄`**. Isso elimina os problemas 1 e 2 por construção.

---

## Fase de diagnóstico (`diagnosticar-galho`)

1. **Inventário:** lista notas da pasta (exclui `index.md`, `roadmap.md`; identifica brotos `Xa/Xb`
   e o campo `fase:` do galho — se usa Iniciado/Adepto/Magus ou organização por sequência/Blocos).
2. **Semeadura:** cria `roadmap.md` com um placeholder por nota (`<!-- nota: <arquivo> -->`).
3. **Análise nota a nota:** um subagente por nota, **≤3 concorrentes**. Cada um:
   - lê a nota inteira (conteúdo real, ignorando linhas em branco de rodapé que inflam `wc -l`);
   - audita contra o checklist da `verificar-nota` (ESTRUTURA/PROFUNDIDADE/TAMANHO/LINKS/MÍDIA)
     calibrado pela régua das skills (núcleo mínimo + opcionais caso-a-caso);
   - **classifica custo:** `[mecânico]` (correção barata sem web: TL;DR, URLs, abertura-problema,
     ASCII→Mermaid, armadilhas→`[!warning]`) ou `[substantivo]` (expandir p/ piso, pesquisar fato
     novo, reescrever seção);
   - **escreve o plano de execução** concreto + estado inicial (`⬜` ou `➖`);
   - grava seu bloco substituindo o placeholder exato (Edit).
4. **Para.** O diagnóstico é revisado pelo usuário antes de qualquer execução.

---

## Fase de execução (loop do `enriquecer-galho`)

1. Relê `<galho>/roadmap.md`, seleciona as notas `⬜`.
2. Dispara em **ondas de ≤3 subagentes**, cada um invocando `enriquecer-nota --auto` com o
   **plano da nota** vindo do roadmap:
   - `[mecânico]` → **haiku, effort low**.
   - `[substantivo]` → **Sonnet**.
3. Conforme **cada** subagente conclui (não espera a onda inteira), o coordenador:
   - grava `✅ (data)` + resumo do resultado no roadmap **imediatamente**;
   - incrementa o contador da sessão;
   - roda a **checagem de governança de tokens** (abaixo).
4. Próxima onda só começa se a governança permitir **e** o contador < 15.

---

## Governança de tokens (ccusage)

Mecanismo: `ccusage` (CLI, lê os JSONL locais do Claude Code — legível via Bash, diferente do
`/usage` que é só UI). Comando: `ccusage blocks --active --offline --json` (o `--offline` evita
chamada de rede a cada check).

Sinais lidos: tokens usados no bloco de 5h, teto estimado do bloco, tempo restante, e **projeção**
de total se o ritmo continuar. A medição cobre a **sessão inteira** (main loop + subagentes), então
reflete automaticamente o trabalho principal — é isso que garante "não roubar do main".

**Checagem ao fim de cada nota.** Pausa (avisa o fluxo e para) se qualquer:

1. Tempo restante do bloco **< ~30 min** (não começar nota que pode ser cortada no meio);
2. Uso atual do bloco **> ~50%** do teto (perfil conservador — cede ao main);
3. Projeção do bloco **> ~50%** do teto (burn alto).

Na pausa, o roadmap já tem tudo gravado — retomar no próximo bloco/sessão é trivial.

---

## Fronteira de sessão — parada dura das 15 (inegociável)

Contador de notas enriquecidas na sessão. Ao atingir **15**:

1. Para tudo.
2. Avisa: "15 notas — hora do `/clear`."
3. O usuário revisa os diffs (`git diff`) das 15 notas e reverte o que não gostou.
4. `/clear` limpa a sessão (evita o imposto de contexto gigante em cache-read).
5. Ao retomar (nova sessão), `enriquecer-galho <path>` relê o `roadmap.md` e continua da
   primeira `⬜`. Resumível por design.

---

## Modelos (opusplan)

- **Coordenador (`enriquecer-galho`, `diagnosticar-galho`):** Opus.
- **Subagentes de execução:** Sonnet (substantivo) / Haiku effort low (mecânico) —
  herdam via `CLAUDE_CODE_SUBAGENT_MODEL`, sem forçar Opus.

---

## Migração do diagnóstico IA existente

O `00-Meta/guia/roadmap - ia.md` (19 galhos num arquivo) precisa ser **fatiado**: a seção de
cada galho migra para o `roadmap.md` da respectiva pasta, adicionando (a) o campo de estado
(`✅/➖/⬜` derivado de "Precisa mudança: NÃO/SIM") e (b) a classificação `[mecânico]/[substantivo]`
(inferida das mudanças propostas). Aproveita todo o diagnóstico já feito; evita re-diagnosticar.
Após a migração, o arquivo central pode virar um índice/ponteiro ou ser removido.

---

## Como cada problema anterior é resolvido

| Problema | Mecanismo |
| -------- | --------- |
| Double-work (mesma nota 2×) | Máquina de estados: loop só toca `⬜`; `🔄` protege contra re-despacho |
| Galho-falso | Galho só "feito" com zero `⬜`/`🔄`; estado por nota no disco |
| Fan-out explosivo | Teto de ≤3 concorrentes · `--auto` sem crítico aninhado · governança ccusage por nota · parada das 15 |

## Sequência de implementação (para o plano)

1. Adicionar modo `--auto` à `enriquecer-nota` (explicit-plan, sem crítico/gate/menu).
2. Criar `diagnosticar-galho` (generaliza a auditoria feita; grava `roadmap.md` na pasta).
3. Criar `enriquecer-galho` (coordenador: diagnóstico-ou-execução, ondas ≤3, governança ccusage, parada 15).
4. Migrar `guia/roadmap - ia.md` → `roadmap.md` por pasta (fatiar + estado + classificação).
5. Teste piloto: rodar `enriquecer-galho` em **3 galhos já diagnosticados** — Ferramentas de IA (5, pesado em caducidade), Structured Outputs (8, mecânico), Evaluation (8, mecânico). Cobre os dois perfis de custo e valida a governança de tokens em volume real.
