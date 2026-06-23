# Dashboards do apocrypha — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Habilitar cross-vault awareness no apocrypha via symlink relativo, e criar três dashboards Dataview (progresso agregado, "estudar hoje", cross-glosa) que cruzam dados do vault público a partir do apocrypha.

**Architecture:** Symlink relativo `Codex` → `../codex-technomanticus` (versionado pelo Git como mode 120000). Três notas de dashboard em `00-Meta/dashboards/` com queries Dataview/DataviewJS lendo `Codex/...`. Sem código de runtime, sem cópia de dados, sem alteração no público. Desktop-only (Android via GitSync não suporta).

**Tech Stack:** Markdown + YAML frontmatter, Obsidian (Dataview, Templater), Git (com `core.symlinks=true`).

**Spec:** `codex-technomanticus/docs/superpowers/specs/2026-05-05-dashboards-apocrypha-design.md`

---

## File Structure

### Repo `codex-technomanticus-apocrypha` (privado — único repo afetado)

| Arquivo | Ação | Responsabilidade |
|---|---|---|
| `Codex` | Create (symlink) | Symlink relativo → `../codex-technomanticus`. Habilita Dataview a indexar o público. |
| `00-Meta/README.md` | Create ou Modify | Nota operacional: precondição de layout, limitação mobile, comando de recriar symlink. |
| `00-Meta/dashboards/Dashboard - Progresso agregado.md` | Create | Dashboard 1: totais globais + por domínio + por senda. |
| `00-Meta/dashboards/Dashboard - O que estudar hoje.md` | Create | Dashboard 2: em andamento (sorted) + convites em sendas ativas. |
| `00-Meta/dashboards/Dashboard - Cross-glosa.md` | Create | Dashboard 3: métricas + fila + top tags + promoções recentes. |

### Repos NÃO afetados

- `codex-technomanticus` (público): zero alteração.
- `codex-technomanticus-site` (Quartz): zero alteração; deploy não passa pelo apocrypha.

### Notas pro implementador

- **Plano roda dentro do `codex-technomanticus-apocrypha`.** Os caminhos abaixo são todos relativos a esse repo. Antes de começar, `cd codex-technomanticus-apocrypha`.
- **Pré-condição de filesystem:** os dois repos clonados lado a lado (mesmo diretório pai). No desktop atual: `~/repos/personal/codex-technomanticus` e `~/repos/personal/codex-technomanticus-apocrypha`.
- **Sem testes automatizados.** Dashboards são markdown + queries Dataview. Validação é visual no Obsidian (renderiza? colunas batem? totais batem com sample manual?).
- **Sem TDD.** Não aplicável.
- **Commits frequentes.** Cada task termina com 1 commit. Mensagens em português; **NÃO usar `Co-Authored-By: Claude`**.
- **Caracteres especiais nos paths.** `03-Dominios`, etc. — preservar acentos (e o nome `Dashboard - O que estudar hoje.md` tem espaços + traço).
- **Desktop-only:** dashboards não funcionam no Android. Documentar no README.
- **Hoje é 2026-05-05.**
- **Vault público NÃO é tocado.** Restrição absoluta.

---

## Task 1: Verificar pré-requisitos no apocrypha

**Files:**
- (nenhum — etapa de inspeção)

- [ ] **Step 1: Confirmar layout dos repos lado a lado**

```bash
ls -d ~/repos/personal/codex-technomanticus ~/repos/personal/codex-technomanticus-apocrypha
```

Expected: ambos os diretórios listados, sem erro. Se algum faltar, abortar e reorganizar antes de continuar.

- [ ] **Step 2: Confirmar Dataview ativo no apocrypha**

```bash
cd ~/repos/personal/codex-technomanticus-apocrypha
ls .obsidian/plugins/dataview/main.js 2>/dev/null && echo "Dataview instalado" || echo "FALTA Dataview"
```

Expected: `Dataview instalado`.
Se faltar: abrir Obsidian no apocrypha → Settings → Community plugins → Browse → instalar "Dataview" → ativar. Repetir o check.

- [ ] **Step 3: Confirmar Templater ativo no apocrypha**

```bash
ls .obsidian/plugins/templater-obsidian/main.js 2>/dev/null && echo "Templater instalado" || echo "FALTA Templater"
```

Expected: `Templater instalado`.
Se faltar: instalar via Community plugins (mesmo fluxo). Templater não é estritamente necessário pros dashboards desta spec, mas o backlog de daily notes vai precisar — instala já.

- [ ] **Step 4: Confirmar `core.symlinks` no Git do apocrypha**

```bash
git -C ~/repos/personal/codex-technomanticus-apocrypha config --get core.symlinks
```

Expected: `true` (default no Linux). Se vier vazio ou `false`, rodar:

```bash
git -C ~/repos/personal/codex-technomanticus-apocrypha config core.symlinks true
```

Sem commit nesta task — só verificação.

---

## Task 2: Criar e versionar o symlink `Codex`

**Files:**
- Create: `Codex` (symlink relativo → `../codex-technomanticus`)

- [ ] **Step 1: Confirmar raiz do apocrypha**

```bash
cd ~/repos/personal/codex-technomanticus-apocrypha
ls -d 00-Meta 02-Glosas 03-Dominios 04-Sendas 2>&1
test ! -e Codex && echo "Codex ausente — ok pra criar" || echo "Codex já existe — investigar antes"
```

Expected: as 4 pastas existentes listadas + "Codex ausente — ok pra criar". Se `Codex` já existir, parar e investigar.

- [ ] **Step 2: Criar o symlink relativo**

```bash
cd ~/repos/personal/codex-technomanticus-apocrypha
ln -s ../codex-technomanticus Codex
```

- [ ] **Step 3: Validar que o symlink resolve**

```bash
ls -la Codex
ls Codex/03-Dominios | head -5
```

Expected:
- `ls -la Codex` mostra `Codex -> ../codex-technomanticus`.
- `ls Codex/03-Dominios` lista pastas de domínio do público (Arquitetura, JavaScript, IA, etc.).

Se `ls Codex/...` der "No such file", o symlink está dangling — verificar layout e posição relativa.

- [ ] **Step 4: Confirmar que o Git enxerga como symlink**

```bash
cd ~/repos/personal/codex-technomanticus-apocrypha
git status
git ls-files --stage Codex 2>/dev/null  # após add
```

`git status` deve mostrar `Codex` como untracked. Ainda sem `git ls-files` neste momento (não foi add'ed).

- [ ] **Step 5: Adicionar e commitar**

```bash
cd ~/repos/personal/codex-technomanticus-apocrypha
git add Codex
git ls-files --stage Codex
```

Expected do `git ls-files --stage`: linha começando com `120000 ...` (mode de symlink, NÃO `100644`). Se vier `100644`, o Git não reconheceu como symlink — abortar, configurar `core.symlinks=true`, remover o arquivo, recriar com `ln -s`.

```bash
git commit -m "chore: symlink relativo Codex → vault público"
```

---

## Task 3: Criar nota operacional `00-Meta/README.md`

**Files:**
- Create ou Modify: `00-Meta/README.md`

- [ ] **Step 1: Verificar se a pasta `00-Meta/` existe; criar se não**

```bash
cd ~/repos/personal/codex-technomanticus-apocrypha
mkdir -p 00-Meta
ls 00-Meta/
```

- [ ] **Step 2: Verificar se README.md já existe**

```bash
test -f 00-Meta/README.md && cat 00-Meta/README.md || echo "Não existe — criar do zero"
```

Se existir conteúdo: anexar a seção nova ao final, preservando o que já está lá. Se não existir: criar do zero com o conteúdo completo abaixo.

- [ ] **Step 3: Escrever (ou anexar) o conteúdo**

Conteúdo (criar do zero):

```markdown
---
title: README — Operação do apocrypha
type: meta
created: 2026-05-05
publish: false
---

# README — Operação do apocrypha

## Cross-vault awareness (symlink → vault público)

O apocrypha enxerga o vault público (`codex-technomanticus`) através do symlink relativo `Codex` → `../codex-technomanticus`. Isso habilita os dashboards em `00-Meta/dashboards/` a rodarem queries Dataview contra os arquivos do público sem cópia de dados.

### Pré-condição de layout

Os dois repos precisam ficar **lado a lado**, num diretório pai comum:

\`\`\`
<base>/
├── codex-technomanticus/           (público)
└── codex-technomanticus-apocrypha/ (privado)
\`\`\`

No desktop atual: `~/repos/personal/`. Em qualquer máquina nova, basta clonar os dois repos lado a lado pra que o symlink resolva automaticamente.

### Recriar o symlink (se quebrado)

\`\`\`bash
cd <base>/codex-technomanticus-apocrypha
rm -f Codex
ln -s ../codex-technomanticus Codex
\`\`\`

### Limitação mobile (Android + GitSync)

Symlinks **não funcionam** no Android com a stack atual:

- O storage acessível ao Obsidian (`/storage/emulated/0/`) é FUSE/sdcardfs e bloqueia `symlink()` em muitos ROMs.
- JGit (motor do GitSync) materializa o symlink como arquivo-texto contendo `../codex-technomanticus` — não é referência funcional.
- Mesmo se criado, Obsidian Mobile não atravessa o symlink de forma confiável.

**Resultado prático no celular/tablet:**
- A pasta `Codex/` aparece como arquivo (ou inválida).
- Os 3 dashboards renderizam **vazios**.
- Daily notes, drafts, glosas e demais conteúdos do apocrypha funcionam normalmente.

**Decisão:** dashboards consolidados são **desktop-only**. Mobile é pra captura/leitura local.
```

Comando:

```bash
cat > 00-Meta/README.md << 'EOF'
[colar o conteúdo acima — atenção: o exemplo de árvore usa \`\`\` escapado pra não fechar o heredoc; remover as barras invertidas ao colar]
EOF
```

⚠️ Atenção: o markdown acima usa `\`\`\`` escapado pra ilustrar dentro deste plano. Ao escrever no README de fato, usar `\`\`\`` literal (3 crases sem barras). Use `Edit` ou `Write` tool em vez de heredoc se preferir evitar essa armadilha.

- [ ] **Step 4: Verificar conteúdo escrito**

```bash
cat 00-Meta/README.md | head -20
```

Expected: frontmatter + título + início da seção "Cross-vault awareness".

- [ ] **Step 5: Commitar**

```bash
git add 00-Meta/README.md
git commit -m "docs: README operacional do apocrypha (cross-vault + limitação mobile)"
```

---

## Task 4: Criar `Dashboard - Progresso agregado.md`

**Files:**
- Create: `00-Meta/dashboards/Dashboard - Progresso agregado.md`

- [ ] **Step 1: Criar a pasta `dashboards/`**

```bash
cd ~/repos/personal/codex-technomanticus-apocrypha
mkdir -p 00-Meta/dashboards
ls 00-Meta/dashboards/
```

- [ ] **Step 2: Escrever o arquivo**

Caminho exato (atenção aos espaços no nome): `00-Meta/dashboards/Dashboard - Progresso agregado.md`.

Conteúdo completo:

````markdown
---
title: Dashboard - Progresso agregado
type: dashboard
created: 2026-05-05
publish: false
---

# Dashboard — Progresso agregado

Visão consolidada do estado de estudo cruzando dados do vault público (`Codex/`).

## Totais globais (notas de domínio)

```dataview
TABLE WITHOUT ID
  length(rows) AS "Total",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "feito")) AS "Feitas",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "andamento")) AS "Em andamento",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "pausado")) AS "Pausadas",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "abandonado")) AS "Abandonadas",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "pendente")) AS "Pendentes"
FROM "Codex/03-Dominios"
GROUP BY true
```

## Por domínio

```dataviewjs
const pages = dv.pages('"Codex/03-Dominios"');

const groups = {};
for (const p of pages) {
  const parts = p.file.folder.split("/");
  const idx = parts.indexOf("03-Dominios");
  if (idx === -1 || !parts[idx + 1]) continue;
  const dominio = parts[idx + 1];
  if (!groups[dominio]) groups[dominio] = { feito: 0, andamento: 0, pausado: 0, abandonado: 0, pendente: 0 };
  const prog = p.progresso ?? "pendente";
  if (groups[dominio][prog] !== undefined) groups[dominio][prog]++;
}

const rows = Object.entries(groups).map(([d, c]) => {
  const total = c.feito + c.andamento + c.pausado + c.abandonado + c.pendente;
  const pct = total > 0 ? ((c.feito / total) * 100).toFixed(0) : "0";
  return [d, c.feito, c.andamento, c.pausado, c.abandonado, c.pendente, `${pct}%`];
});

rows.sort((a, b) => parseInt(b[6]) - parseInt(a[6]));
dv.table(["Domínio", "Feitas", "Andamento", "Pausadas", "Abandonadas", "Pendentes", "% feito"], rows);
```

## Por senda

```dataviewjs
const sendas = dv.pages('"Codex/04-Sendas"');

const rows = [];
for (const senda of sendas) {
  const targets = senda.file.outlinks
    .filter(l => l.path && l.path.includes("03-Dominios/"))
    .map(l => dv.page(l.path))
    .filter(p => p);

  const total = targets.length;
  if (total === 0) continue;

  const feito = targets.filter(p => (p.progresso ?? "pendente") === "feito").length;
  const andamento = targets.filter(p => (p.progresso ?? "pendente") === "andamento").length;
  const pct = total > 0 ? ((feito / total) * 100).toFixed(0) : "0";

  rows.push([senda.file.link, total, `${pct}%`, andamento]);
}

rows.sort((a, b) => parseInt(b[2]) - parseInt(a[2]));
dv.table(["Senda", "Itens", "% feito", "Em andamento agora"], rows);
```
````

Use o tool `Write` (não `cat <<EOF`) — heredoc com markdown nested codeblocks é frágil.

- [ ] **Step 3: Validação visual no Obsidian**

Abrir o Obsidian no apocrypha. Navegar até `00-Meta/dashboards/Dashboard - Progresso agregado.md`. Confirmar:

- 3 blocos renderizam (não aparecem como código bruto).
- Bloco 1 mostra uma única linha com 6 colunas.
- Bloco 2 lista os domínios em colunas (Arquitetura, JavaScript, IA, etc.) com `% feito`.
- Bloco 3 lista as sendas existentes com totais.

Se aparecer "No results" em algum bloco: provavelmente o symlink não resolve OU não há notas com `progresso` definido (default `pendente` deveria ainda contar). Investigar.

- [ ] **Step 4: Smoke test cruzado**

Pegar 1 domínio (ex: `JavaScript`). Contar manualmente notas em `Codex/03-Dominios/Tecnologia/JavaScript/` (ou `~/repos/personal/codex-technomanticus/03-Dominios/Tecnologia/JavaScript/`):

```bash
find ~/repos/personal/codex-technomanticus/03-Dominios/JavaScript -name "*.md" | wc -l
```

Confirmar que a soma das colunas (Feitas+Andamento+Pausadas+Abandonadas+Pendentes) na linha JavaScript do dashboard bate com esse número (ou difere por arquivos `index.md`/`README.md` excluíveis — usar julgamento).

- [ ] **Step 5: Commitar**

```bash
git add "00-Meta/dashboards/Dashboard - Progresso agregado.md"
git commit -m "feat: Dashboard - Progresso agregado (totais + por domínio + por senda)"
```

---

## Task 5: Criar `Dashboard - O que estudar hoje.md`

**Files:**
- Create: `00-Meta/dashboards/Dashboard - O que estudar hoje.md`

- [ ] **Step 1: Escrever o arquivo**

Caminho: `00-Meta/dashboards/Dashboard - O que estudar hoje.md`.

Conteúdo completo:

````markdown
---
title: Dashboard - O que estudar hoje
type: dashboard
created: 2026-05-05
publish: false
---

# Dashboard — O que estudar hoje

Heurísticas pra responder "o que faço hoje?" sem inventar modelo de fila/prioridade. Os blocos surfacedam itens parados e convites em sendas onde já existe atividade.

## Em andamento (mais antigos no topo)

Itens com `progresso: andamento`, ordenados pelo update mais antigo. ⚠️ marca itens parados há mais de 14 dias.

```dataviewjs
const today = dv.date("today");
const STALL_DIAS = 14;

function daysSince(raw) {
  let dt = raw;
  if (typeof dt === "string") dt = dv.date(dt);
  if (!dt || dt.isValid !== true) return 0;
  const diff = today.diff(dt, "days");
  return Math.max(0, Math.floor(diff?.days ?? 0));
}

const pages = dv.pages('"Codex"')
  .where(p => p.progresso === "andamento")
  .filter(p => !p.file.path.includes("Promovidas") && !p.file.path.includes("Arquivadas"));

const sendas = dv.pages('"Codex/04-Sendas"');

const rows = [];
for (const p of pages) {
  const days = daysSince(p.updated ?? p.file.mtime);
  const flag = days > STALL_DIAS ? "⚠️ " : "";

  const sendasContendo = sendas
    .where(s => s.file.outlinks.some(l => l.path === p.file.path))
    .map(s => s.file.link.toString());

  rows.push([`${flag}${p.file.link}`, sendasContendo.join(", ") || "—", days]);
}

rows.sort((a, b) => b[2] - a[2]);
dv.table(["Item", "Senda(s)", "Dias desde update"], rows);
```

## Convites em sendas ativas

Callouts `[!convite]` em notas que pertencem a sendas onde já existe pelo menos uma nota com `progresso ∈ {andamento, feito}`.

```dataviewjs
const allNotes = dv.pages('"Codex/03-Dominios"');
const activeNotePaths = new Set();
for (const n of allNotes) {
  const prog = n.progresso ?? "pendente";
  if (prog === "andamento" || prog === "feito") activeNotePaths.add(n.file.path);
}

const sendas = dv.pages('"Codex/04-Sendas"');
const activeSendas = sendas.filter(s =>
  s.file.outlinks.some(l => l.path && activeNotePaths.has(l.path))
);

const rows = [];
for (const senda of activeSendas) {
  for (const link of senda.file.outlinks) {
    if (!link.path || !link.path.includes("03-Dominios/")) continue;
    const note = dv.page(link.path);
    if (!note) continue;

    const content = await dv.io.load(note.file.path);
    if (!content) continue;

    const matches = [...content.matchAll(/^>\s*\[!convite\]\s*([^\n]*)$/gm)];
    for (const m of matches) {
      const titulo = (m[1] || "").trim() || "(sem título)";
      rows.push([senda.file.link, note.file.link, titulo]);
    }
  }
}

rows.sort((a, b) => a[0].toString().localeCompare(b[0].toString()));
dv.table(["Senda", "Nota", "Convite"], rows);
```
````

Use o tool `Write`.

- [ ] **Step 2: Validação visual no Obsidian**

Abrir `Dashboard - O que estudar hoje.md`. Confirmar:

- Bloco 1 ("Em andamento") renderiza tabela com 3 colunas (Item, Senda(s), Dias desde update). Pode estar vazio se não houver itens com `progresso: andamento` agora — checar manualmente:

```bash
grep -l "progresso: andamento" ~/repos/personal/codex-technomanticus/03-Dominios -r 2>/dev/null | head
grep -l "progresso: andamento" ~/repos/personal/codex-technomanticus/02-Glosas -r 2>/dev/null | head
```

Se houver matches no grep mas a tabela estiver vazia: investigar (possível problema de path ou frontmatter parsing).

- Bloco 2 ("Convites em sendas ativas") renderiza tabela. Pode estar vazio se não houver callouts `[!convite]` em sendas ativas — confirmar manualmente:

```bash
grep -r "\[!convite\]" ~/repos/personal/codex-technomanticus/03-Dominios | head
```

- [ ] **Step 3: Smoke test do bloco 1**

Pegar uma nota com `progresso: andamento` (do grep do Step 2). Confirmar que ela aparece na tabela do bloco 1, com a contagem de dias plausível (`hoje - updated` ou `hoje - mtime`).

- [ ] **Step 4: Commitar**

```bash
git add "00-Meta/dashboards/Dashboard - O que estudar hoje.md"
git commit -m "feat: Dashboard - O que estudar hoje (em andamento + convites)"
```

---

## Task 6: Criar `Dashboard - Cross-glosa.md`

**Files:**
- Create: `00-Meta/dashboards/Dashboard - Cross-glosa.md`

- [ ] **Step 1: Escrever o arquivo**

Caminho: `00-Meta/dashboards/Dashboard - Cross-glosa.md`.

Conteúdo completo:

````markdown
---
title: Dashboard - Cross-glosa
type: dashboard
created: 2026-05-05
publish: false
---

# Dashboard — Cross-glosa

Visão consolidada do repositório de glosas: métricas, fila ativa, top tags, promoções recentes.

## Métricas

```dataviewjs
const ativas = dv.pages('"Codex/02-Glosas"')
  .filter(p => !p.file.path.includes("Promovidas") && !p.file.path.includes("Arquivadas"));
const promovidas = dv.pages('"Codex/02-Glosas/Promovidas"');
const arquivadas = dv.pages('"Codex/02-Glosas/Arquivadas"');

const N = ativas.length;
const M = promovidas.length;
const K = arquivadas.length;
const taxa = (M + K > 0) ? ((M / (M + K)) * 100).toFixed(1) + "%" : "—";

const ultPromocaoRaw = promovidas
  .map(p => p.updated ?? p.file.mtime)
  .filter(d => d)
  .sort((a, b) => b - a)[0];
const ultPromocao = ultPromocaoRaw
  ? dv.date(ultPromocaoRaw).toFormat("yyyy-MM-dd")
  : "—";

dv.paragraph(
  `**${N} ativas** · **${M} promovidas** · **${K} arquivadas** · ` +
  `Taxa de promoção: **${taxa}** · Última promoção: **${ultPromocao}**`
);
```

## Glosas ativas em fila (mais antigas no topo)

```dataviewjs
const today = dv.date("today");

function daysSince(raw) {
  let dt = raw;
  if (typeof dt === "string") dt = dv.date(dt);
  if (!dt || dt.isValid !== true) return 0;
  const diff = today.diff(dt, "days");
  return Math.max(0, Math.floor(diff?.days ?? 0));
}

const ativas = dv.pages('"Codex/02-Glosas"')
  .filter(p => !p.file.path.includes("Promovidas") && !p.file.path.includes("Arquivadas"));

const rows = ativas.map(g => {
  const days = daysSince(g.updated ?? g.file.mtime);
  return [g.file.link, days, g.progresso ?? "—", (g.tags ?? []).join(", ")];
});

rows.sort((a, b) => b[1] - a[1]);
dv.table(["Glosa", "Dias parada", "Progresso", "Tags"], rows);
```

## Top 10 tags

```dataviewjs
const fontes = dv.pages('"Codex/02-Glosas"')
  .filter(p => !p.file.path.includes("Arquivadas"));

const counts = {};
for (const g of fontes) {
  for (const t of (g.tags ?? [])) {
    counts[t] = (counts[t] ?? 0) + 1;
  }
}

const rows = Object.entries(counts)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 10)
  .map(([tag, n]) => [`#${tag}`, n]);

dv.table(["Tag", "Glosas"], rows);
```

## Promoções recentes (top 5)

```dataviewjs
const promovidas = dv.pages('"Codex/02-Glosas/Promovidas"');

const rows = promovidas.map(g => {
  const updatedRaw = g.updated ?? g.file.mtime;
  const updated = updatedRaw ? dv.date(updatedRaw) : null;
  const updatedStr = updated ? updated.toFormat("yyyy-MM-dd") : "—";

  const notasGeradas = (g.promovida_em ?? []).map(l => {
    if (typeof l === "string") return l;
    if (l && l.path) return `[[${l.path}|${l.path.split("/").pop().replace(".md", "")}]]`;
    return String(l);
  });

  return [g.file.link, updatedStr, notasGeradas.join(", ") || "—", updated];
});

rows.sort((a, b) => (b[3] ?? 0) - (a[3] ?? 0));
const top5 = rows.slice(0, 5).map(r => r.slice(0, 3));
dv.table(["Glosa", "Promovida em", "Nota gerada"], top5);
```
````

Use o tool `Write`.

- [ ] **Step 2: Validação visual no Obsidian**

Abrir `Dashboard - Cross-glosa.md`. Confirmar:

- **Bloco "Métricas":** linha em parágrafo mostrando N/M/K + taxa + última promoção. No estado atual do público: `N=0` glosas ativas (a única foi promovida na sessão anterior), `M ≥ 1`, `K=0`. Conferir contra:

```bash
ls ~/repos/personal/codex-technomanticus/02-Glosas/*.md 2>/dev/null | wc -l   # N (ativas em raiz)
find ~/repos/personal/codex-technomanticus/02-Glosas/Promovidas -name "*.md" 2>/dev/null | wc -l   # M
find ~/repos/personal/codex-technomanticus/02-Glosas/Arquivadas -name "*.md" 2>/dev/null | wc -l   # K
```

- **Bloco "Glosas ativas em fila":** vazio se `N=0`, com tabela caso contrário.
- **Bloco "Top 10 tags":** lista as tags presentes nas glosas (ativas + promovidas). Se não houver tags, fica vazio.
- **Bloco "Promoções recentes":** lista até 5 promovidas mais recentes, com a coluna "Nota gerada" mostrando wikilink se `promovida_em` foi populado.

- [ ] **Step 3: Smoke test da taxa**

Conferir manualmente: `taxa = M / (M + K) · 100`. No estado atual com `K=0`: `taxa = 100%` (todas as resolvidas viraram nota). Confirmar que o dashboard mostra esse valor.

- [ ] **Step 4: Commitar**

```bash
git add "00-Meta/dashboards/Dashboard - Cross-glosa.md"
git commit -m "feat: Dashboard - Cross-glosa (métricas + fila + tags + promoções)"
```

---

## Task 7: Validação final integrada

**Files:**
- (nenhum — etapa de validação)

- [ ] **Step 1: Validar `git log` final do apocrypha**

```bash
cd ~/repos/personal/codex-technomanticus-apocrypha
git log --oneline -10
```

Expected: 4 commits recentes nesta sequência (mais recente no topo):

1. `feat: Dashboard - Cross-glosa ...`
2. `feat: Dashboard - O que estudar hoje ...`
3. `feat: Dashboard - Progresso agregado ...`
4. `docs: README operacional do apocrypha ...`
5. `chore: symlink relativo Codex → vault público`

- [ ] **Step 2: Validar que os 3 dashboards abrem no Obsidian sem erro**

No Obsidian (apocrypha): abrir cada um dos 3 dashboards na ordem. Confirmar que:

- Nenhum bloco mostra erro vermelho de Dataview ("Evaluation Error" / "Could not parse").
- Tabelas renderizam (mesmo que vazias quando não há dados correspondentes).
- Sem console errors críticos no Developer Tools (Ctrl+Shift+I) — warnings ok.

- [ ] **Step 3: Validar que o vault público continua intocado**

```bash
cd ~/repos/personal/codex-technomanticus
git status
```

Expected: working tree do público idêntico ao estado pré-implementação (apenas as modificações já existentes antes desta sessão, se houver). **Não pode haver nada novo introduzido por esta task.**

- [ ] **Step 4: Validar que o site público não foi afetado**

Verificação rápida: a pipeline de deploy (`codex-technomanticus-site`) só lê de `codex-technomanticus`, não conhece o apocrypha. Como o público não mudou, o deploy continua igual. Sem ação necessária — apenas confirmar mentalmente.

- [ ] **Step 5: (Opcional) Push do apocrypha**

```bash
cd ~/repos/personal/codex-technomanticus-apocrypha
git push
```

Pular se preferir agrupar com outras mudanças da sessão.

- [ ] **Step 6: Atualizar `apocrypha-pendencias.md` no público**

Mover-se pro repo público e remover do `docs/apocrypha-pendencias.md` os itens agora resolvidos pela spec 2026-05-05:

- Cross-vault awareness (toda a seção do topo) → resolvida.
- "Tracking de progresso de estudo (spec 2026-05-03)" — os dois bullets ("Dashboard agregado de progresso" e "O que estudar hoje?") → resolvidos.
- "Dashboard cross-glosa (spec 2026-05-04)" → resolvido.

Substituir por uma nota de referência no topo do arquivo, no estilo:

```markdown
> **Resolvido pela spec `2026-05-05-dashboards-apocrypha-design.md`** (executada em <data>): cross-vault awareness, dashboard agregado de progresso, "o que estudar hoje?", dashboard cross-glosa. Próximas pendências abaixo.
```

E manter a seção "Daily notes do Obsidian" (não tocada por esta spec).

```bash
cd ~/repos/personal/codex-technomanticus
# editar docs/apocrypha-pendencias.md conforme acima
git add docs/apocrypha-pendencias.md
git commit -m "docs: marca pendências do apocrypha resolvidas pela spec dashboards"
```

---

## Self-review checklist (já validado pelo autor do plano)

- [x] **Cobertura da spec:** §4 (cross-vault) → Tasks 1-2; §5 (estrutura) → Tasks 3-6; §6 (Dashboard 1) → Task 4; §7 (Dashboard 2) → Task 5; §8 (Dashboard 3) → Task 6; §11 (sequência) → Tasks 1-7 nesta ordem.
- [x] **Sem placeholders.** Todas as queries Dataview/JS estão escritas inline; todos os comandos são exatos; nenhum "TBD".
- [x] **Type/identifier consistency.** Paths consistentes (`Codex/...` em todos os blocos), nomes de arquivos preservam espaços + traço, frontmatter idêntico nos 3 dashboards.
- [x] **Restrição "não tocar no público":** apenas a Task 7 Step 6 toca o público (atualização de pendências), e é opcional/contextual — fora da execução core no apocrypha.
- [x] **Restrição "não tocar no apocrypha agora":** o plano declara explicitamente que executa **na sessão dedicada do apocrypha**, não nesta sessão.
