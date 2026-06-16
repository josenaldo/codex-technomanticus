---
title: "Galho Complexidade de Software — plano de implementação"
created: 2026-06-16
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - complexidade-de-software
---

# Galho Complexidade de Software — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir o galho 12 de Fundamentos — "Complexidade de Software" — como uma sub-trilha de 16 notas atômicas em 3 fases, migrando duas notas existentes e cruzando com o cluster IA/Lado Sombrio.

**Architecture:** Pasta `03-Dominios/Fundamentos/Complexidade de Software/` com notas `NN - Título.md` (frontmatter `fase:`), um `index.md` (MOC) agrupado por fase, e callout no MOC do domínio. Conteúdo em registro didático Feynman; afirmações factuais com fonte verificada.

**Tech Stack:** Obsidian Flavored Markdown; Dataview; skills do vault (`verbete`, `verificar-wikilinks`, `enriquecer-nota`); git.

**Design de referência:** `00-Meta/specs/2026-06-16-galho-complexidade-de-software-design.md`.

**Convenções herdadas (não re-decidir):**
- Limite ~600 linhas/nota; dividir se estourar.
- `publish: false` nas notas do galho (convenção de Fundamentos: notas não publicam; só o `index.md`/MOC é `publish: true`). Verificado em 2026-06-16 contra todas as notas do domínio.
- Nunca deletar `index.md` (regra Quartz). Folder-link exige `index.md`.
- Não assinar commits (sem Co-Authored-By).
- Honestidade epistêmica: marcar o que não passou por verificação de fonte.
- Cada nota = um commit (commits frequentes).

---

## Verificação no lugar de TDD

Como o deliverable é conteúdo, cada tarefa de nota troca o ciclo "teste→implementação" por:
1. **Escrever** a nota (frontmatter + seções + prosa).
2. **Verificar:** frontmatter válido (`fase`, `type`, `tags`, `publish`); wikilinks citados resolvem; afirmações factuais têm fonte; cobre os pontos-chave listados.
3. **Commit.**

Afirmações com dado factual (datas, autores, números, citações) devem ser conferidas via web/glosa antes do commit — não escrever de memória.

---

## Task 1: Scaffold da pasta e MOC do galho

**Files:**
- Create: `03-Dominios/Fundamentos/Complexidade de Software/index.md`

- [ ] **Step 1: Criar o MOC com as 16 entradas como esqueleto**

Conteúdo de `index.md`:

```markdown
---
title: "Complexidade de Software"
created: 2026-06-16
updated: 2026-06-16
type: moc
status: seedling
publish: true
tags:
  - fundamentos
  - complexidade-de-software
  - moc
aliases:
  - Galho 12 - Complexidade de Software
  - A Complexidade do Software
---

# Complexidade de Software

> [!abstract] TL;DR
> Galho 12 de Fundamentos. O estudo daquilo que torna software difícil de construir e
> manter — complexidade essencial vs. acidental, os limites da abstração, carga cognitiva,
> as três dívidas (técnica, cognitiva, intenção) e o decaimento dos sistemas no tempo. A
> espinha: *o que ajuda a entender ou gerenciar a complexidade do software?*

## Sobre este galho

Cobre a complexidade como o problema central do software, de ponta a ponta: por que software
é difícil (Brooks, Tar Pit, Hickey, Naur), os mecanismos com que a gerenciamos e onde eles
falham (abstração, information hiding, módulos, carga cognitiva), as três dívidas do Triple
Debt Model (Storey) e a gestão da complexidade no tempo e no todo (entropia, manutenção,
pensamento sistêmico, Lei de Conway).

**Não cobre:** Design Patterns e estilos arquiteturais (ficam em [[03-Dominios/Arquitetura/index|Arquitetura]]);
as manifestações AI-specific dos débitos (ficam em [[03-Dominios/IA/O Lado Sombrio da IA/index|O Lado Sombrio da IA]],
sob a lente da IA — este galho trata sob a lente geral/atemporal, cross-linkado).

## Iniciado

1. [[01 - A complexidade como problema central]] — a dificuldade-raiz do software; Brooks, No Silver Bullet.
2. [[02 - Complexidade essencial vs. acidental]] — a distinção de Brooks; estado e Out of the Tar Pit.
3. [[03 - Simplicidade não é facilidade]] — Hickey, Simple Made Easy; complecting.
4. [[04 - O programa como teoria]] — Naur, theory-building; conhecimento tácito.

## Adepto

5. [[05 - Abstração - a ferramenta central]] — information hiding (Parnas); esconder decisões voláteis.
6. [[06 - Abstrações que vazam]] — Spolsky, Lei das Abstrações Vazadas; Lei de Hyrum.
7. [[07 - Módulos profundos e rasos]] — Ousterhout, A Philosophy of Software Design.
8. [[08 - Carga cognitiva e legibilidade]] — cognitive load; menor surpresa; obscuridade.
9. [[09 - As três dívidas do software]] — Triple Debt Model (Storey): técnica/cognitiva/intenção.
10. [[10 - Dívida técnica]] — Cunningham; juros; atalhos no código.
11. [[11 - Dívida cognitiva]] — erosão do entendimento compartilhado (perspectiva geral).
12. [[12 - Dívida de intenção]] — Storey/Osmani/Fowler; externalizar rationale.

## Magus

13. [[13 - Entropia de software e decaimento]] — bit rot, broken windows, big ball of mud.
14. [[14 - Manutenção e evolução]] — legado como gestão de complexidade no tempo.
15. [[15 - Pensamento sistêmico]] — feedback, emergência, parte vs. todo.
16. [[16 - Lei de Conway]] — complexidade organizacional ↔ arquitetural.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Fundamentos/Complexidade de Software"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Fundamentos/index|Fundamentos (MOC do domínio)]]
- [[03-Dominios/IA/O Lado Sombrio da IA/index|O Lado Sombrio da IA]] — os débitos sob a lente da IA
- [[Dicionário de Fundamentos]]
```

- [ ] **Step 2: Verificar** — `index.md` existe, dataview bem-formado, wikilinks de "Veja também" resolvem (os `NN - ...` ainda não existem; é esperado até as próximas tarefas).

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Fundamentos/Complexidade de Software/index.md"
git commit -m "feat(fundamentos): scaffold do galho Complexidade de Software (MOC)"
```

---

## Task 2: Migrar a nota do Naur → `04 - O programa como teoria`

**Files:**
- Move: `03-Dominios/Fundamentos/O programa como teoria.md` → `03-Dominios/Fundamentos/Complexidade de Software/04 - O programa como teoria.md`

- [ ] **Step 1: Mover com git (preserva histórico)**

```bash
git mv "03-Dominios/Fundamentos/O programa como teoria.md" \
       "03-Dominios/Fundamentos/Complexidade de Software/04 - O programa como teoria.md"
```

- [ ] **Step 2: Ajustar frontmatter** — adicionar `fase: iniciado`; adicionar tag `complexidade-de-software` e `iniciado`; **remover** o alias `Teoria do sistema` (vai pra nota 15); manter `title: "O programa como teoria"` e os demais aliases. Manter o corpo intacto.

- [ ] **Step 3: Verificar** — wikilinks que apontam pra esta nota por nome (`[[O programa como teoria]]`) continuam resolvendo; nenhum link interno quebrou.

- [ ] **Step 4: Commit**

```bash
git add -A "03-Dominios/Fundamentos/"
git commit -m "refactor(fundamentos): migra 'O programa como teoria' p/ galho Complexidade (nota 04)"
```

---

## Task 3: Migrar a nota do Spolsky → `06 - Abstrações que vazam`

**Files:**
- Move: `03-Dominios/Fundamentos/Abstrações que vazam.md` → `03-Dominios/Fundamentos/Complexidade de Software/06 - Abstrações que vazam.md`

- [ ] **Step 1: Mover com git**

```bash
git mv "03-Dominios/Fundamentos/Abstrações que vazam.md" \
       "03-Dominios/Fundamentos/Complexidade de Software/06 - Abstrações que vazam.md"
```

- [ ] **Step 2: Ajustar frontmatter** — adicionar `fase: adepto` e tags `complexidade-de-software`, `adepto`; manter título/aliases/corpo.

- [ ] **Step 3: Verificar** — `[[Abstrações que vazam]]` resolve; links no corpo (Redes e Protocolos, GC, JIT) intactos.

- [ ] **Step 4: Commit**

```bash
git add -A "03-Dominios/Fundamentos/"
git commit -m "refactor(fundamentos): migra 'Abstrações que vazam' p/ galho Complexidade (nota 06)"
```

---

## Task 4: Atualizar o MOC do domínio Fundamentos

**Files:**
- Modify: `03-Dominios/Fundamentos/index.md`
- Modify: `03-Dominios/Fundamentos/Fundamentos.md`

- [ ] **Step 1: Em `index.md`** — na seção "Conteúdo", remover as linhas de `[[O programa como teoria]]` e `[[Abstrações que vazam]]` da raiz; adicionar entrada do galho:

```markdown
- [[03-Dominios/Fundamentos/Complexidade de Software/index|Complexidade de Software]] — galho 12: o que torna software difícil e como gerenciá-lo (essencial vs. acidental, abstração, dívidas, sistemas)
```

- [ ] **Step 2: Em `Fundamentos.md`** — adicionar seção/linha para o galho sob um agrupamento adequado (ex.: nova seção "Engenharia e Complexidade") apontando para o `index` do galho.

- [ ] **Step 3: Verificar** — `verificar-wikilinks` na pasta `03-Dominios/Fundamentos/`; zero quebrados; o folder-link do galho resolve pro `index.md`.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Fundamentos/index.md" "03-Dominios/Fundamentos/Fundamentos.md"
git commit -m "docs(fundamentos): registra galho Complexidade no MOC do domínio"
```

---

## Template de nota (aplicar nas Tasks 5–18)

Frontmatter padrão (ajustar `title`, `fase`, `tags`):

```markdown
---
title: "<título sem o prefixo NN>"
created: 2026-06-16
updated: 2026-06-16
type: concept
progress: backlog
status: seedling
publish: false
fase: <iniciado|adepto|magus>
tags:
  - fundamentos
  - complexidade-de-software
  - <fase>
  - <2-3 tags do tema>
---

# <título>

<frase de abertura: 1-2 linhas definindo o conceito>

> [!abstract] TL;DR
> <síntese em 2-4 linhas>

## O que é
...
## <seções de desenvolvimento em registro didático>
...
## Armadilhas comuns   (quando couber)
## Em entrevista        (SÓ nas notas marcadas [entrevista] abaixo)
## Referências
## Veja também
```

Cada tarefa de nota segue: escrever → verificar (frontmatter/links/fontes/pontos-chave) → commit
`feat(fundamentos): nota NN - <título>`.

---

## Task 5: Nota `01 - A complexidade como problema central` (Iniciado)

**Files:** Create `03-Dominios/Fundamentos/Complexidade de Software/01 - A complexidade como problema central.md`

- [ ] **Step 1: Escrever.** Pontos-chave: complexidade como a dificuldade-raiz do software (não a única, mas a central); por que complexidade importa (custo de mudança cresce com ela); panorama do galho (mapa das 16 notas); definição operacional de complexidade (Ousterhout: "tudo que torna o sistema difícil de entender e modificar"). Fonte: Brooks, *No Silver Bullet*; Ousterhout, *A Philosophy of Software Design* (cap. 1-2). Tags: `complexidade`, `brooks`. Sem "Em entrevista".
- [ ] **Step 2: Verificar** — Brooks/Ousterhout citados corretamente (ano, obra); links pras notas 02–04 resolvem.
- [ ] **Step 3: Commit.**

## Task 6: Nota `02 - Complexidade essencial vs. acidental` (Iniciado)

**Files:** Create `.../02 - Complexidade essencial vs. acidental.md`

- [ ] **Step 1: Escrever.** Pontos-chave: distinção de Brooks (essencial = inerente ao problema; acidental = das ferramentas/representação); por que "no silver bullet" (ganhos sobraram só na acidental); *Out of the Tar Pit* (Moseley & Marks): complexidade vinda do **estado** e do controle; complexidade essencial é irredutível, acidental é onde dá pra atacar. Fonte: Brooks *No Silver Bullet* (1986); Moseley & Marks *Out of the Tar Pit* (2006). Tags: `complexidade-essencial`, `estado`. `[entrevista]` leve (trade-off útil de articular).
- [ ] **Step 2: Verificar** — datas/autores; distinção bem representada; link nota 03.
- [ ] **Step 3: Commit.**

## Task 7: Nota `03 - Simplicidade não é facilidade` (Iniciado)

**Files:** Create `.../03 - Simplicidade não é facilidade.md`

- [ ] **Step 1: Escrever.** Pontos-chave: Hickey, *Simple Made Easy* — simple (objetivo, "um só entrelaçamento") vs. easy (subjetivo, "ao alcance"); **complecting** (entrelaçar) como origem de complexidade; simplicidade como escolha de design, não conforto. Fonte: Rich Hickey, palestra *Simple Made Easy* (Strange Loop, 2011). Tags: `simplicidade`, `hickey`. Sem "Em entrevista".
- [ ] **Step 2: Verificar** — atribuição correta da palestra; conceito de complecting fiel.
- [ ] **Step 3: Commit.**

## Task 8: (migração já feita — nota 04 existe). Enriquecer `04 - O programa como teoria`

**Files:** Modify `.../04 - O programa como teoria.md`

- [ ] **Step 1:** Adicionar ao corpo (sem quebrar o existente) um link explícito pra nota `11 - Dívida cognitiva` e pra `15 - Pensamento sistêmico`; garantir `## Veja também` aponta dentro do galho. Atualizar `updated`.
- [ ] **Step 2: Verificar** links internos do galho resolvem.
- [ ] **Step 3: Commit** `docs(fundamentos): conecta nota 04 ao galho Complexidade`.

## Task 9: Nota `05 - Abstração - a ferramenta central` (Adepto)

**Files:** Create `.../05 - Abstração - a ferramenta central.md`

- [ ] **Step 1: Escrever.** Pontos-chave: abstração como a principal ferramenta de gestão de complexidade; information hiding (Parnas, 1972) — esconder **decisões de design propensas a mudar**, não só dados; abstração ≠ indireção; boas vs. más abstrações; prepara a nota 06 (limites) e 07 (módulos). Fonte: Parnas, *On the Criteria...* (CACM 1972); Ousterhout (deep modules). Tags: `abstracao`, `information-hiding`, `parnas`. Sem "Em entrevista".
- [ ] **Step 2: Verificar** — Parnas citado certo; link nota 06/07.
- [ ] **Step 3: Commit.**

## Task 10: (migração feita — nota 06 existe). Conectar `06 - Abstrações que vazam`

**Files:** Modify `.../06 - Abstrações que vazam.md`

- [ ] **Step 1:** Garantir `## Veja também` aponta pra `05 - Abstração` e `07 - Módulos profundos e rasos` dentro do galho; atualizar `updated`. Não reescrever o corpo (já é maduro).
- [ ] **Step 2: Verificar** links.
- [ ] **Step 3: Commit** `docs(fundamentos): conecta nota 06 ao galho Complexidade`.

## Task 11: Nota `07 - Módulos profundos e rasos` (Adepto)

**Files:** Create `.../07 - Módulos profundos e rasos.md`

- [ ] **Step 1: Escrever.** Pontos-chave: Ousterhout — deep module (interface simples, muita funcionalidade) vs. shallow (interface grande, pouca); profundidade como medida de bom encapsulamento; "classitis"; complexidade é incremental (cada pedacinho conta). Fonte: Ousterhout, *A Philosophy of Software Design*. Tags: `modularidade`, `ousterhout`, `encapsulamento`. Sem "Em entrevista".
- [ ] **Step 2: Verificar** — conceitos fiéis ao livro.
- [ ] **Step 3: Commit.**

## Task 12: Nota `08 - Carga cognitiva e legibilidade` (Adepto)

**Files:** Create `.../08 - Carga cognitiva e legibilidade.md`

- [ ] **Step 1: Escrever.** Pontos-chave: carga cognitiva como esforço mental momentâneo pra entender código (distinta de débito cognitivo — que é de projeto/tempo); princípio da menor surpresa; obscuridade (Ousterhout); ressalva honesta sobre métricas (complexidade ciclomática mede uma faceta, não "a" complexidade). Fonte: Ousterhout; literatura de cognitive load. Tags: `carga-cognitiva`, `legibilidade`. Cross-link: tabela de distinção em `IA/.../Débito cognitivo`. Sem "Em entrevista".
- [ ] **Step 2: Verificar** — distinção carga × débito clara; ressalva de métricas presente.
- [ ] **Step 3: Commit.**

## Task 13: Nota `09 - As três dívidas do software` (Adepto)

**Files:** Create `.../09 - As três dívidas do software.md`

- [ ] **Step 1: Escrever.** Pontos-chave: Triple Debt Model (Storey) — técnica (código) / cognitiva (pessoas) / intenção (artefatos); independentes e interagentes; tabela onde-vive/natureza; serve de hub pras notas 10–12. Fonte: glosa `2026-from-technical-debt-to-cognitive-and-intent-debt` (Storey arXiv); Fowler; Osmani. Tags: `triple-debt-model`, `dividas`, `storey`. `[entrevista]`.
- [ ] **Step 2: Verificar** — modelo atribuído à Storey; as 3 dívidas corretas; links 10–12.
- [ ] **Step 3: Commit.**

## Task 14: Nota `10 - Dívida técnica` (Adepto)

**Files:** Create `.../10 - Dívida técnica.md`

- [ ] **Step 1: Escrever.** Pontos-chave: metáfora original de Ward Cunningham; juros (custo de manutenção crescente); deliberada vs. inadvertida (quadrante de Fowler); paga-se refatorando; relação com complexidade acidental. Fonte: Cunningham; Fowler, *Technical Debt Quadrant*. Tags: `divida-tecnica`, `cunningham`, `refactoring`. `[entrevista]`.
- [ ] **Step 2: Verificar** — Cunningham como autor da metáfora; quadrante de Fowler correto.
- [ ] **Step 3: Commit.**

## Task 15: Nota `11 - Dívida cognitiva` (Adepto)

**Files:** Create `.../11 - Dívida cognitiva.md`

- [ ] **Step 1: Escrever.** Pontos-chave: erosão do entendimento *compartilhado* em nível de projeto/tempo (Storey); distinta de carga cognitiva (momentânea) e débito técnico (código); sinais de alerta; mitigação (reconstruir teoria: pairing, review, docs do porquê). Perspectiva **geral/atemporal** — cross-link explícito pra `IA/O Lado Sombrio da IA/Débito cognitivo` (a mesma ideia sob a lente da IA). Fonte: glosa Storey; nota IA existente. Tags: `divida-cognitiva`, `entendimento-compartilhado`. Sem "Em entrevista".
- [ ] **Step 2: Verificar** — distinção tripla clara; cross-link IA presente e recíproco (ver Task 19).
- [ ] **Step 3: Commit.**

## Task 16: Nota `12 - Dívida de intenção` (Adepto)

**Files:** Create `.../12 - Dívida de intenção.md`

- [ ] **Step 1: Escrever.** Pontos-chave: ausência/erosão de rationale, metas e restrições **externalizados** (Storey/Osmani); vive nos artefatos (specs, ADRs, AGENTS.md/CLAUDE.md, README de não-objetivos); só humanos geram intenção (agente infere, não recupera); testes de diagnóstico (5 minutos, não-objetivos, ADR, linguagem ubíqua); pagar = externalizar como artefato de primeira classe. Fonte: glosas Osmani/Fowler/Storey/Developers Digest. Tags: `divida-intencao`, `adr`, `rationale`. `[entrevista]`.
- [ ] **Step 2: Verificar** — 4 glosas citadas em Referências; conceito fiel.
- [ ] **Step 3: Commit.**

## Task 17: Nota `13 - Entropia de software e decaimento` (Magus)

**Files:** Create `.../13 - Entropia de software e decaimento.md`

- [ ] **Step 1: Escrever.** Pontos-chave: software apodrece sob mudança (software entropy / bit rot); *broken windows* (pequenas degradações convidam mais); big ball of mud (Foote & Yoder); leis de Lehman (evolução e complexidade crescente). Fonte: Foote & Yoder, *Big Ball of Mud* (1997); Lehman's Laws; Hunt & Thomas (broken windows). Tags: `entropia-software`, `big-ball-of-mud`, `lehman`. Sem "Em entrevista".
- [ ] **Step 2: Verificar** — atribuições corretas (Foote&Yoder, Lehman).
- [ ] **Step 3: Commit.**

## Task 18: Notas Magus restantes — `14`, `15`, `16`

**Files:** Create `.../14 - Manutenção e evolução.md`, `.../15 - Pensamento sistêmico.md`, `.../16 - Lei de Conway.md`

- [ ] **Step 1: Escrever `14 - Manutenção e evolução`.** Pontos-chave: manutenção como atividade dominante do ciclo de vida; legado = código sem teoria (liga à nota 04); *make the hard change easy, then make the easy change* (Beck); refatoração como reconstrução de entendimento. Fonte: Beck; Feathers, *Working Effectively with Legacy Code*. Tags: `manutencao`, `legado`. Commit.
- [ ] **Step 2: Escrever `15 - Pensamento sistêmico`.** Pontos-chave: sistema como todo > soma das partes; feedback loops; emergência; fronteiras de sistema; aplicar a software (efeitos de segunda ordem, ciclos de reforço de complexidade). **Adicionar alias `Teoria do sistema`** (migrado da nota 04). Fonte: Meadows, *Thinking in Systems*. Tags: `pensamento-sistemico`, `feedback`, `emergencia`. Commit.
- [ ] **Step 3: Escrever `16 - Lei de Conway`.** Pontos-chave: organizações desenham sistemas que copiam sua estrutura de comunicação (Conway, 1968); inverse Conway maneuver; complexidade organizacional vaza pra arquitetura. Fonte: Conway, *How Do Committees Invent?* (1968); Skelton & Pais, *Team Topologies*. Tags: `lei-de-conway`, `organizacao`. `[entrevista]` leve. Commit.
- [ ] **Step 4: Verificar** — cada uma: frontmatter, links, fontes; alias "Teoria do sistema" só na 15.

---

## Task 19: Cross-links recíprocos com IA/Lado Sombrio

**Files:**
- Modify: `03-Dominios/IA/O Lado Sombrio da IA/Débito cognitivo.md`
- Modify: `03-Dominios/IA/O Lado Sombrio da IA/index.md`

- [ ] **Step 1:** Em `Débito cognitivo.md`, na seção "Veja também", adicionar link pra `[[11 - Dívida cognitiva]]` com nota de que é o conceito-mãe sob a perspectiva geral; reforçar no corpo que esta nota trata a **aceleração por IA**. Atualizar `updated`.
- [ ] **Step 2:** No `index.md` do Lado Sombrio, na seção "Fundamento", adicionar link pro `index` do galho Complexidade (além do já existente p/ O programa como teoria).
- [ ] **Step 3: Verificar** — links recíprocos resolvem nos dois sentidos; sem quebrar wikilinks existentes da nota IA.
- [ ] **Step 4: Commit** `docs(ia): cross-link Débito cognitivo ↔ galho Complexidade de Software`.

## Task 20: Verbetes no Dicionário de Fundamentos

**Files:** Modify `03-Dominios/Fundamentos/Dicionário de Fundamentos.md` (via skill `/verbete`)

- [ ] **Step 1:** Adicionar verbetes (em ordem alfabética, na seção certa) para termos novos: complexidade essencial, complexidade acidental, débito técnico, débito cognitivo, débito de intenção, carga cognitiva, entropia de software, Lei de Conway, Lei de Hyrum, information hiding. (Abstração que vaza já existe.) Cada verbete: termo + definição curta + link pra nota do galho.
- [ ] **Step 2: Verificar** — ordem alfabética; sem duplicar verbetes existentes; links resolvem.
- [ ] **Step 3: Commit** `docs(fundamentos): verbetes de Complexidade no Dicionário`.

## Task 21: Verificação final do galho

- [ ] **Step 1:** Rodar `verificar-wikilinks` em `03-Dominios/Fundamentos/Complexidade de Software/` e em `03-Dominios/Fundamentos/` — corrigir quaisquer quebrados.
- [ ] **Step 2:** Conferir o dataview do `index.md` lista as 16 notas; todas com `fase` e `status`.
- [ ] **Step 3:** Atualizar `status` do `index.md` do galho de `seedling` → `growing`; `updated` na data de fechamento.
- [ ] **Step 4: Commit** `chore(fundamentos): fecha 1ª passada do galho Complexidade de Software`.

---

## Self-review (cobertura do spec)

- 16 notas → Tasks 5–18 (04 e 06 via migração 2–3 + conexão 8/10). ✓
- Migrações Naur/Spolsky + alias "Teoria do sistema" → Tasks 2, 3, 18. ✓
- Fronteira por perspectiva c/ IA (cross-link, nada movido) → Tasks 15, 19. ✓
- MOC do galho + tronco do domínio → Tasks 1, 4. ✓
- Glosas como fonte das dívidas → Tasks 13, 15, 16. ✓
- Dicionário + verificação Quartz/wikilinks → Tasks 20, 21. ✓
- Fora de escopo (Design Patterns, AI-specific, processos) respeitado nos prompts das notas. ✓
