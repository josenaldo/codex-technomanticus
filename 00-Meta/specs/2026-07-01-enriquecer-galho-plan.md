# Suíte enriquecer-galho — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) ou superpowers:executing-plans para implementar tarefa a tarefa. Steps usam checkbox (`- [ ]`).

**Goal:** Criar uma suíte de skills que coordena o enriquecimento de qualquer galho do vault, nota a nota, com memória em disco (`roadmap.md` por pasta) e governança de tokens via `ccusage`.

**Architecture:** Coordenador `enriquecer-galho` (Opus) que ou chama `diagnosticar-galho` (gera o roadmap) ou roda o loop de execução em ondas de ≤3 subagentes invocando `enriquecer-nota --auto`. Estado por nota no `roadmap.md` da pasta é a fonte de verdade contra double-work.

**Tech Stack:** Markdown (Obsidian Flavored), skills do Claude Code (`.agents/skills/` → symlink `.claude/skills/`), `ccusage` CLI, skill-creator para autoria.

**Design de referência:** `00-Meta/specs/2026-07-01-enriquecer-galho-design.md` — leia antes de começar.

## Global Constraints

- Skills vivem em `.agents/skills/<nome>/SKILL.md` (symlink `.claude/skills`). **Nunca** editar via `.claude/skills` (é symlink; cópia única).
- Concorrência: **≤3 subagentes simultâneos** em qualquer fase (diagnóstico ou execução).
- `enriquecer-nota --auto` no fluxo de galho **não dispara subagente crítico** (senão 3×crítico = 6 agentes).
- Parada dura a cada **15 notas** enriquecidas por sessão.
- Governança: `ccusage blocks --active --offline --json` ao fim de cada nota; pausa se tempo <~30min OU uso/projeção >~50% do teto do bloco.
- Coordenador em Opus; execução em Sonnet (substantivo) / Haiku effort low (mecânico) via `CLAUDE_CODE_SUBAGENT_MODEL` — não forçar Opus em subagente.
- `roadmap.md`: `type: meta`, `publish: false`. Excluído de inventário de notas.
- Commits/push são **manuais do usuário** — o plano não auto-commita a menos que o usuário peça.
- Não fabricar dados do usuário; não referenciar apocrypha; redundância entre notas é reforço (não deduplicar).

---

### Task 1: Modo `--auto` na `enriquecer-nota`

**Files:**
- Modify: `.agents/skills/enriquecer-nota/SKILL.md`

**Interfaces:**
- Produces: invocação `/enriquecer-nota <path> --auto "<instrução/plano>"` que aplica o plano dado **sem** menu de lentes (Fase 2), **sem** gate de confirmação (Fase 5/convenção), e **sem** despachar o subagente crítico (Fase 4). Consumida pela Task 3.

- [ ] **Step 1: Ler a skill atual inteira** para mapear as fases interativas (Fase 2 menu, Fase 4 crítico, Fase 5 plano+confirmação, "Confirmação antes de executar" nas convenções rígidas).

- [ ] **Step 2: Adicionar seção "## Modo `--auto` (não-interativo)"** logo após a seção de Invocação, com este contrato exato:
  - Ativado por `--auto` no comando.
  - **Com instrução/plano explícito** (uso pelo galho): pula Fase 2 (menu), Fase 4 (crítico) e Fase 5 (confirmação). Aplica exatamente as mudanças descritas na instrução, seguindo o Registro Feynman e os formatos de seção da Fase 3. Grava direto.
  - **Sem instrução** (uso avulso do usuário): roda as lentes de higiene + as lentes inferidas do diagnóstico da Fase 0, **sem** confirmação, mas **ainda sem** disparar o crítico quando invocada dentro de outro subagente (evita fan-out aninhado). Aplica os sobreviventes.
  - Registra no relatório final (Fase 7) que rodou em modo `--auto`.

- [ ] **Step 3: Ajustar as "Convenções rígidas"** — trocar "Confirmação antes de executar — nenhuma edição sem plano aprovado" por: "Confirmação antes de executar — EXCETO em modo `--auto`, onde o plano vem pré-aprovado (via diagnóstico/galho) ou é gerado e aplicado sem gate."

- [ ] **Step 4: Ajustar a Fase 4 (Crítica)** — adicionar nota: "Pulada em modo `--auto`. No fluxo de `enriquecer-galho`, o plano do `roadmap.md` já é a lista vetada; não há crítico."

- [ ] **Step 5: Verificação (dry-run inline, sem subagente):** escolher UMA nota já diagnosticada com fix mecânico (ex: `Structured Outputs/02 - JSON Schema como contrato.md`, gap E2). Simular mentalmente/descrever o fluxo `--auto` com a instrução "adicionar parágrafo de abertura-problema antes de '## JSON Schema 101'". Confirmar que o contrato da skill leva a: sem menu, sem crítico, aplica e grava. Documentar o resultado do dry-run em 2 linhas.

- [ ] **Step 6:** Reportar ao usuário o diff da SKILL.md para revisão (não commitar).

---

### Task 2: Skill `diagnosticar-galho`

**Files:**
- Create: `.agents/skills/diagnosticar-galho/SKILL.md`

**Interfaces:**
- Consumes: régua da `verificar-nota` (checklist ESTRUTURA/PROFUNDIDADE/TAMANHO/LINKS/MÍDIA).
- Produces: `<galho>/roadmap.md` com uma entrada executável por nota (formato do design), estado inicial `⬜`/`➖`, classificação `[mecânico]/[substantivo]`, e plano de execução concreto. Consumido pela Task 3.

- [ ] **Step 1: Criar via skill-creator** (`/skill-creator`) ou escrever SKILL.md com frontmatter `name: diagnosticar-galho` + description gatilho ("diagnosticar galho", "criar roadmap de enriquecimento do galho", chamada por `enriquecer-galho`).

- [ ] **Step 2: Documentar Fase 0 — Inventário.** Comando de listagem que exclui `index.md` e `roadmap.md`, identifica brotos (`Xa/Xb`), e detecta o esquema de `fase:` do galho (grep do primeiro `fase:` em cada nota; classificar: usa fases Iniciado/Adepto/Magus com piso, OU organiza por sequência/Blocos sem fase). Registrar o esquema no cabeçalho do roadmap.

- [ ] **Step 3: Documentar Fase 1 — Semeadura.** Criar `<galho>/roadmap.md` com frontmatter `type: meta, publish: false`, cabeçalho (nome, régua, esquema de fase, data), tabela-resumo, e um placeholder `<!-- nota: <arquivo> -->` por nota (append via heredoc, robusto contra reescrita do Obsidian).

- [ ] **Step 4: Documentar Fase 2 — Análise nota a nota.** Prompt-template do subagente (ANEXAR o template literal na skill): recebe path + régua; lê conteúdo REAL (ignora linhas em branco de rodapé); audita 12 itens do checklist; classifica custo `[mecânico]`/`[substantivo]`; escreve plano de execução acionável; define estado `⬜` (precisa) ou `➖` (não precisa); substitui o placeholder exato via Edit. **≤3 concorrentes.** Modelo: Sonnet.

- [ ] **Step 5: Documentar Fase 3 — Fecho.** Verificar 0 placeholders restantes; preencher tabela-resumo (contagem por estado); **parar** (diagnóstico é revisado antes de executar).

- [ ] **Step 6: Documentar o formato EXATO da entrada por nota** (copiar do design, seção "Entrada por nota") como bloco de referência dentro da skill.

- [ ] **Step 7: Convenções rígidas** — ≤3 concorrentes; não editar as notas (read-only); não fabricar dados; um subagente por nota; grava só no roadmap.

- [ ] **Step 8: Verificação (dry-run real, escopo mínimo):** rodar a Fase 0+1 (inventário + semeadura) num galho pequeno NÃO-IA para não colidir com o roadmap IA existente — se não houver, usar uma pasta de teste temporária no scratchpad. Confirmar que o `roadmap.md` é criado com N placeholders corretos. Reportar.

---

### Task 3: Skill `enriquecer-galho` (coordenador)

**Files:**
- Create: `.agents/skills/enriquecer-galho/SKILL.md`

**Interfaces:**
- Consumes: `diagnosticar-galho` (Task 2), `enriquecer-nota --auto` (Task 1), `ccusage`.
- Produces: entrada `/enriquecer-galho <path>`; muta `<galho>/roadmap.md` (estados `🔄`→`✅`).

- [ ] **Step 1: Criar SKILL.md** com frontmatter `name: enriquecer-galho`, description gatilho ("enriquecer galho", "enriquecer o galho X", "rodar enriquecimento do galho"), e nota de que roda em Opus (opusplan) — coordenação.

- [ ] **Step 2: Documentar o roteamento de entrada.** Recebe `<path>`. Se `<path>/roadmap.md` **não existe** → invoca `diagnosticar-galho <path>` e **PARA** (avisa que o diagnóstico está pronto para revisão). Se **existe** → segue para o loop.

- [ ] **Step 3: Documentar o loop de execução:**
  1. Ler `roadmap.md`, coletar notas `⬜` (ignorar `✅`/`➖`/`🔄`).
  2. Se zero `⬜` → galho concluído; reportar e encerrar.
  3. **Governança pré-onda:** rodar `ccusage blocks --active --offline --json`; se pausa (regras abaixo) → avisar fluxo e parar.
  4. Formar onda de ≤3 notas `⬜`; marcar cada uma `🔄` no roadmap antes de despachar.
  5. Para cada nota da onda, despachar subagente: `[mecânico]`→haiku/low, `[substantivo]`→Sonnet; o subagente invoca `enriquecer-nota --auto <path> "<plano do roadmap>"`.
  6. Conforme **cada** subagente conclui: gravar `✅ (data)` + resumo no roadmap **imediatamente**; incrementar contador de sessão; rodar **governança pós-nota** (ccusage).
  7. Se contador == 15 → **parada dura** (Step 5). Senão, voltar a 1.

- [ ] **Step 4: Documentar a governança de tokens (bloco literal na skill):**
  - Comando: `ccusage blocks --active --offline --json`.
  - Parse: tempo restante do bloco, tokens usados, teto do bloco, projeção.
  - **Pausa se:** restante < ~30 min **OU** uso > ~50% do teto **OU** projeção > ~50% do teto.
  - Ação de pausa: escrever no chat o snapshot (usado/projeção/restante) + "pausando enriquecimento (baixa prioridade); retomo no próximo bloco". Encerrar sem erro.

- [ ] **Step 5: Documentar a parada das 15:** ao atingir 15, parar tudo, avisar "15 notas nesta sessão — revise `git diff` e rode `/clear`; ao retomar, `enriquecer-galho <path>` continua da primeira `⬜`."

- [ ] **Step 6: Convenções rígidas** — ≤3 concorrentes; nunca marcar galho "feito" com `⬜`/`🔄` restantes; gravar estado por nota ANTES de seguir; não commitar (push manual); coordenador não faz enriquecimento (só orquestra).

- [ ] **Step 7: Verificação estrutural:** reler a SKILL.md e confirmar que os 3 gatilhos de pausa, o teto de 3, a parada de 15 e o roteamento diagnóstico-ou-execução estão todos explícitos e sem contradição. Reportar.

---

### Task 4: Migrar `guia/roadmap - ia.md` → `roadmap.md` por pasta

**Files:**
- Create: `03-Dominios/Tecnologia/IA/<cada galho>/roadmap.md` (19 arquivos)
- Modify/Remove: `00-Meta/guia/roadmap - ia.md` (vira índice-ponteiro ou é removido)

**Interfaces:**
- Consumes: formato do design; dados já existentes no arquivo central.

- [ ] **Step 1:** Para cada galho no arquivo central, extrair a seção `## N. <Galho>` e suas entradas `#### `.

- [ ] **Step 2:** Para cada nota, adicionar o campo `- **Enriquecimento:**` derivado: "Precisa mudança: NÃO" → `➖ não precisa`; "SIM" → `⬜ pendente`.

- [ ] **Step 3:** Adicionar a classificação `[mecânico]/[substantivo]` no título de cada nota, inferida das "Mudanças propostas" (só reformatação/URL/abertura/Mermaid/armadilhas = mecânico; expandir piso/pesquisar/reescrever = substantivo). Renomear "Mudanças propostas" → "Plano de execução".

- [ ] **Step 4:** Gravar `<galho>/roadmap.md` com frontmatter `type: meta, publish: false` + cabeçalho + tabela-resumo.

- [ ] **Step 5:** Substituir `guia/roadmap - ia.md` por um índice curto que aponta para os 19 `roadmap.md` (ou remover, se o usuário preferir). Confirmar com o usuário antes de remover.

- [ ] **Step 6: Verificação:** `find 03-Dominios/Tecnologia/IA -name roadmap.md | wc -l` == 19; conferir 1 galho manualmente (contagem de `####` bate com o número de notas). Reportar.

> Nota de custo: esta task é majoritariamente mecânica (mover texto + derivar campos). Fazer inline, sem fan-out. A classificação mecânico/substantivo pode ser feita por regra simples sobre o texto das propostas.

---

### Task 5: Piloto — rodar `enriquecer-galho` nos 3 galhos

**Files:**
- Modify: notas + `roadmap.md` de Ferramentas de IA, Structured Outputs, Evaluation.

- [ ] **Step 1:** `enriquecer-galho "03-Dominios/Tecnologia/IA/Structured Outputs"` (mecânico) — deve entrar direto no loop (roadmap já existe pós-Task 4). Rodar 1 onda (≤3), conferir que estados viram `✅` e os diffs fazem sentido.

- [ ] **Step 2:** Após a 1ª onda, verificar a governança: confirmar que `ccusage` foi consultado e o snapshot apareceu. Reportar o fluxo.

- [ ] **Step 3:** Continuar Structured Outputs + Evaluation + Ferramentas de IA até 15 notas OU pausa por governança, o que vier primeiro. Validar a **parada das 15** e a **retomada** (relê roadmap, pega próxima `⬜`).

- [ ] **Step 4:** Revisar `git diff` do piloto com o usuário; ajustar as skills se algo saiu do esperado (ex: `--auto` disparou crítico, contagem errada, subagente pesado demais).

---

## Self-Review (cobertura do spec)

- **Arquitetura (2 skills + `--auto`)** → Tasks 1, 2, 3. ✓
- **roadmap.md por pasta, publish:false** → Tasks 2 (criação), 4 (migração), Global Constraints. ✓
- **Máquina de estados / anti-double-work / anti-galho-falso** → Task 3 Steps 3, 6. ✓
- **Diagnóstico produz plano executável + classe de custo** → Task 2 Steps 4, 6. ✓
- **Execução em ondas ≤3, save por nota, tiers de modelo** → Task 3 Step 3. ✓
- **Governança ccusage (50%, 30min)** → Task 3 Step 4. ✓
- **Parada das 15 + resumível** → Task 3 Step 5. ✓
- **Migração IA** → Task 4. ✓
- **Piloto nos 3 galhos** → Task 5. ✓

Placeholders: nenhum "TBD". Tipos/nomes consistentes (`--auto`, estados `⬜/🔄/✅/➖`, `ccusage blocks --active --offline --json`) idênticos entre tasks. Sem gaps de spec.
