---
title: "Spec — Dashboards do apocrypha (cross-vault + 3 dashboards)"
date: 2026-05-05
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Dashboards do apocrypha (cross-vault + 3 dashboards)

## 1. Contexto e motivação

As specs `2026-05-03-progresso-sendas-design.md` e `2026-05-04-glosa-promocao-design.md` introduziram, no vault público (`codex-technomanticus`), a infraestrutura de tracking de estudo (campo `progresso`, queries dataview por senda) e o pipeline de promoção/arquivamento de glosas (campos `promovida_em`, `updated`, estrutura `02-Glosas/{Promovidas,Arquivadas}/<ano>/`). Ambas explicitamente puntearam pro apocrypha as visões consolidadas/agregadas — vide `docs/apocrypha-pendencias.md`.

Esta spec entrega essas visões: três dashboards no vault privado (`codex-technomanticus-apocrypha`), alimentados por queries dataview que cruzam dados do público. A precondição é uma forma do Obsidian do apocrypha enxergar os arquivos do público — resolvida via symlink relativo, sem mirror nem duplicação de dados.

A spec opera dois movimentos:

1. **Infraestrutura cross-vault**: symlink relativo `Codex` → `../codex-technomanticus`, comitado no apocrypha. Habilita Dataview a indexar o público a partir do apocrypha.
2. **Três dashboards** em `00-Meta/dashboards/`, cada um num arquivo: progresso agregado, "o que estudar hoje" (heurístico), cross-glosa.

## 2. Objetivo

Entregar:

1. **Symlink relativo** versionado dentro do apocrypha, apontando pro repo público.
2. **Pasta `00-Meta/dashboards/`** criada.
3. **Três notas de dashboard** com queries Dataview/DataviewJS funcionais:
   - `Dashboard - Progresso agregado.md`
   - `Dashboard - O que estudar hoje.md`
   - `Dashboard - Cross-glosa.md`
4. **Documentação curta** no apocrypha explicando layout esperado (precondição cross-device) e limitação mobile.

## 3. Escopo

### Em escopo

- Criação do symlink relativo `Codex` → `../codex-technomanticus`.
- Verificação de que Dataview e Templater estão instalados/ativados no apocrypha (instalar se faltarem).
- Criação dos três arquivos de dashboard com queries prontas.
- Nota curta de operação em `00-Meta/README.md` (ou similar) explicando precondição de layout dos repos lado a lado.

### Fora de escopo (trabalho subsequente)

- **Velocidade temporal de progresso** (notas que viraram `feito` nos últimos N dias). Exigiria campo novo no público (`concluido_em`) ou parse de git log. Quando aparecer dor real, vira sub-spec.
- **Dashboards funcionais no mobile**. Symlink não funciona via GitSync no Android (vide §4.3). Se "estudar hoje no commute" virar dor real, evolui-se pro approach Mirror (script que copia público → `Codex-mirror/` versionado, sincronizável). Não fazer agora.
- **"O que estudar hoje?" prescritivo** (com modelo de ordem global e prioridade). Esta spec entrega uma versão heurística que evita inventar fila/prioridade sem ter visto a dor. Modelo prescritivo vira sub-spec quando a heurística incomodar.
- **Skill `/sync-cross-vault`** que automatize criação/verificação do symlink. Pra um único comando, manual basta. Vira skill se virar dor.
- **Histogramas/gráficos** (glosas arquivadas por época, cadência de promoção mensal). Overkill pra valor incremental hoje.
- **Hub MOC dos dashboards** (`00-Meta/Dashboards.md` listando os três). Cada dashboard é navegável por nome ou wikilink direto; hub adiciona arquivo sem entregar valor proporcional.

## 4. Arquitetura cross-vault

### 4.1 Mecanismo

Symlink relativo, criado uma vez na máquina de desenvolvimento e versionado pelo Git como entrada de mode `120000`.

```text
codex-technomanticus-apocrypha/
├── 00-Meta/
├── 01-Pergaminhos/
├── 02-Glosas/
├── 03-Dominios/
├── 04-Sendas/
└── Codex          → ../codex-technomanticus    (symlink)
```

A estrutura do apocrypha **espelha** a do público na raiz (mesmas pastas `00-Meta/`, `01-Pergaminhos/`, etc.) — cada uma contendo o conteúdo privado do vault. O symlink `Codex` é a única adição estrutural; ele expõe o vault público sob um namespace separado, sem conflitar com os diretórios homônimos do apocrypha.

Comando de criação (a executar dentro do repo apocrypha, na sessão dedicada):

```bash
cd codex-technomanticus-apocrypha
ln -s ../codex-technomanticus Codex
git add Codex
git commit -m "chore: symlink relativo pro vault público"
```

Caminhos resultantes vistos pelo Obsidian do apocrypha:

- `Codex/03-Dominios/...`
- `Codex/02-Glosas/...`
- `Codex/04-Sendas/...`

### 4.2 Precondição de layout (cross-device)

O symlink usa caminho **relativo** (`../codex-technomanticus`). Pra resolver corretamente em qualquer máquina, os dois repos precisam estar lado a lado, num diretório comum:

```text
<base>/
├── codex-technomanticus/           (público)
└── codex-technomanticus-apocrypha/ (privado)
```

No desktop atual, `<base>` é `~/repos/personal/`. Em qualquer device futuro (laptop secundário, etc.), basta clonar os dois repos lado a lado pra que o symlink funcione automaticamente.

### 4.3 Limitação mobile (Android + GitSync)

Symlinks não funcionam de forma confiável no Android com a stack atual (GitSync + Obsidian Mobile). Razões:

- Storage acessível ao Obsidian (`/storage/emulated/0/`) é FUSE/sdcardfs por cima de ext4 — `symlink()` syscall falha em muitos ROMs/versões.
- JGit (motor do GitSync) tipicamente cai em fallback que materializa o symlink como **arquivo de texto contendo o path-alvo** (~30 bytes, conteúdo `../codex-technomanticus`).
- Mesmo se o symlink fosse criado, o indexador do Obsidian Mobile historicamente não atravessa symlinks cross-folder de forma consistente.

**Comportamento esperado no Android:**

- A pasta `Codex/` aparece como arquivo (não pasta) ou inválida.
- Os 3 dashboards renderizam **vazios** (Dataview não encontra arquivos no path).
- Daily notes, drafts, glosas e demais conteúdos do apocrypha **continuam funcionando normalmente** (não dependem do symlink).

**Decisão:** dashboards são **desktop-only**. Mobile é usado pra captura/leitura local. Documentar essa limitação na nota de operação do apocrypha.

### 4.4 Impacto no público e no deploy do site

- **Repo público:** zero impacto. Não sabe que o symlink existe; estrutura inalterada.
- **Pipeline `codex-technomanticus` → `codex-technomanticus-site` (Quartz):** zero impacto. O deploy lê só o público, nunca toca o apocrypha.
- **Risco de "vazamento":** zero. Editar arquivo público "via" symlink modifica o working tree do repo público (que tem `.git` próprio). `git status` do apocrypha permanece limpo; modificação aparece no `git status` do público, no lugar correto.

## 5. Estrutura de arquivos no apocrypha

```text
codex-technomanticus-apocrypha/
├── 00-Meta/
│   ├── README.md                          ← nota curta de operação (precondição + limitação mobile)
│   └── dashboards/
│       ├── Dashboard - Progresso agregado.md
│       ├── Dashboard - O que estudar hoje.md
│       └── Dashboard - Cross-glosa.md
├── 01-Pergaminhos/                        ← (existente, não tocado)
├── 02-Glosas/                             ← (existente, próprias do apocrypha — não confundir com Codex/02-Glosas/)
├── 03-Dominios/                           ← (existente, não tocado)
├── 04-Sendas/                             ← (existente, não tocado)
└── Codex                                  ← symlink (versionado)
```

**Atenção à coexistência:** o apocrypha tem `02-Glosas/`, `03-Dominios/`, etc. próprias na raiz (conteúdo privado do vault). As queries Dataview dos dashboards leem **especificamente** `Codex/02-Glosas/`, `Codex/03-Dominios/`, etc. — namespaceadas pelo prefixo do symlink. Não há mistura entre conteúdo público (via `Codex/`) e privado (na raiz do apocrypha).

Frontmatter padrão dos dashboards:

```yaml
---
title: <título>
type: dashboard
created: 2026-05-05
publish: false
---
```

Dashboards nunca são publicados (apocrypha não publica nada hoje, mas `publish: false` deixa explícito).

## 6. Dashboard 1 — Progresso agregado

Arquivo: `00-Meta/dashboards/Dashboard - Progresso agregado.md`.

### 6.1 Bloco — Totais globais (apenas notas de domínio)

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

### 6.2 Bloco — Por domínio

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

O domínio é inferido do path (primeira pasta sob `03-Dominios/`). Sub-domínios não aparecem como linha separada — ficam agregados sob o domínio raiz. Sub-domínios desejados como linha podem ser adicionados ajustando a lógica de extração; fora do MVP.

### 6.3 Bloco — Por senda

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

A consulta itera todas as notas em `04-Sendas/` independentemente de `tipo` no frontmatter — assume convenção de que tudo nessa pasta é senda (consistente com o público hoje).

## 7. Dashboard 2 — O que estudar hoje

Arquivo: `00-Meta/dashboards/Dashboard - O que estudar hoje.md`.

A heurística: sem inventar modelo de fila/prioridade global, mostra o que está aberto e onde existe atividade. Ordering surfaces stale items naturalmente.

### 7.1 Bloco A — Em andamento (mais antigos no topo)

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

`updated` é o campo canônico (introduzido pelas specs 05-03 e 05-04 e atualizado pelas skills de glosa). Fallback pra `file.mtime` quando ausente — comum em notas que ainda não foram tocadas pelo novo template.

A função `daysSince` é defensiva por dois motivos práticos: (1) `dv.date()` pode retornar `null` quando recebe entrada inesperada (DateTime já-construído, string vazia, valor de frontmatter malformado) e o `today.diff(null)` quebra com TypeError; (2) `file.mtime` pode ser hoje à tarde enquanto `today` é meia-noite UTC, gerando `Math.floor(-0.6) = -1` — clamp em ≥ 0 evita "dias negativos" no display.

### 7.2 Bloco B — Convites em sendas ativas

Convites são callouts `[!convite]` dentro de notas de domínio (vide spec 05-03 §6.4). Dataview não indexa callouts diretamente; precisa-se ler o conteúdo bruto via `dv.io.load`.

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

Trade-off de performance: `dv.io.load` por nota é I/O por arquivo. Em vault grande, esse bloco pode ficar lento. Mitigação: limitar via cache (Dataview re-executa só quando arquivo muda). Se virar gargalo real, alternativa é introduzir um campo `convites: N` no frontmatter da nota (atualizado por skill na inserção do callout) — fora do MVP.

## 8. Dashboard 3 — Cross-glosa

Arquivo: `00-Meta/dashboards/Dashboard - Cross-glosa.md`.

### 8.1 Bloco A — Métricas

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

Taxa de promoção considera apenas glosas **resolvidas** (promovidas ou arquivadas) como denominador — glosas ativas não entraram no veredito ainda. Última promoção é inferida do `updated` (que a skill `/promover-glosa` bumpa pra hoje na promoção, conforme spec 05-04 §7).

### 8.2 Bloco B — Glosas ativas em fila (mais antigas no topo)

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

Mesma função `daysSince` defensiva descrita em §7.1 — necessária por motivos idênticos.

### 8.3 Bloco C — Top 10 tags

Considera glosas ativas + promovidas (tira arquivadas pra não contaminar com lixo).

```dataviewjs
const fontes = [
  ...dv.pages('"Codex/02-Glosas"')
    .filter(p => !p.file.path.includes("Arquivadas")),
];

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

Tag rendering como `#tag` em texto (não link clicável que resolva pra busca por tag) — limitação do `dv.table` simples. Se desejar busca clicável, pode-se trocar `#${tag}` por uma ligação custom; fora do MVP.

### 8.4 Bloco D — Promoções recentes (top 5)

```dataviewjs
const promovidas = dv.pages('"Codex/02-Glosas/Promovidas"');

const rows = promovidas.map(g => {
  const updatedRaw = g.updated ?? g.file.mtime;
  const updated = updatedRaw ? dv.date(updatedRaw) : null;
  const updatedStr = updated ? updated.toFormat("yyyy-MM-dd") : "—";

  const notasGeradas = (g.promovida_em ?? []).map(l => {
    if (typeof l === "string") return l;
    if (l && l.path) return dv.fileLink(l.path);
    return String(l);
  });

  return [g.file.link, updatedStr, notasGeradas.join(", ") || "—", updated];
});

rows.sort((a, b) => (b[3] ?? 0) - (a[3] ?? 0));
const top5 = rows.slice(0, 5).map(r => r.slice(0, 3));
dv.table(["Glosa", "Promovida em", "Nota gerada"], top5);
```

`promovida_em` no frontmatter é lista de wikilinks (spec 05-04 §4.2). Renderização preserva o link.

## 9. Privacy e split público × apocrypha

Esta spec **respeita rigorosamente** a separação:

- **Vault público** (`codex-technomanticus`): não recebe nenhuma alteração. Continua sendo a fonte da verdade dos dados (`progresso`, `promovida_em`, `updated`, estrutura de pastas).
- **Vault apocrypha** (`codex-technomanticus-apocrypha`): recebe symlink + 3 dashboards + 1 nota de operação. Dashboards são **leitura analítica/pessoal sobre o estado do público**, sem cópia de conteúdo.
- **Fluxo de informação:** unidirecional. Apocrypha lê do público via symlink; público nunca lê do apocrypha. A regra de `feedback_public_apocrypha_separation.md` continua válida — público segue ignorando completamente o apocrypha.

Nenhum arquivo público referencia o apocrypha (nem por wikilink, nem por path, nem por menção). O symlink mora **dentro** do apocrypha; o público não tem ciência dele.

## 10. Repos afetados

| Repo | O quê |
|---|---|
| `codex-technomanticus` (público) | **Não tocar nesta spec.** Zero alteração. |
| `codex-technomanticus-site` (Quartz) | **Não tocar nesta spec.** Deploy não passa pelo apocrypha. |
| `codex-technomanticus-apocrypha` (privado) | Symlink `Codex`, pasta `00-Meta/dashboards/` com 3 arquivos, nota curta de operação em `00-Meta/README.md`. |

## 11. Sequência de implementação

A executar na **sessão dedicada do apocrypha** (não nesta sessão do público).

1. **Verificar dependências** no apocrypha:
   - Plugin Dataview instalado e ativado.
   - Plugin Templater instalado e ativado (já planejado pelo backlog de daily notes).
   - Instalar/ativar o que faltar.
2. **Criar symlink relativo:**
   ```bash
   cd codex-technomanticus-apocrypha/Apocrypha
   ln -s ../codex-technomanticus Codex
   ```
3. **Validar resolução:** abrir Obsidian no apocrypha; confirmar que `Codex/` aparece como pasta navegável e expõe `02-Glosas/`, `03-Dominios/`, `04-Sendas/`.
4. **Criar pasta** `00-Meta/dashboards/`.
5. **Criar os 3 arquivos de dashboard** com o frontmatter padrão e os blocos das §§6, 7, 8.
6. **Criar nota de operação** `00-Meta/README.md` com:
   - Precondição de layout (repos lado a lado).
   - Limitação mobile (Android/GitSync — dashboards não funcionam).
   - Comando de recriar o symlink se necessário.
7. **Comitar tudo** no apocrypha (symlink + dashboards + README).
8. **Validação manual:**
   - Abrir cada dashboard.
   - Confirmar que tabelas renderizam (mesmo que vazias quando não houver dado correspondente).
   - Confirmar que totais batem com inspeção manual de algumas notas.

## 12. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Symlink dangling se base dir mudar | Sempre clonar os dois repos lado a lado (documentado em §4.2). Se a base mudar, recriar o symlink. |
| Dataview lento no bloco de convites (`dv.io.load`) | Aceitar lentidão inicial; otimizar com campo `convites: N` no frontmatter se virar gargalo (sub-spec). |
| `updated` ausente em notas antigas | Fallback pra `file.mtime` em todas as queries (já implementado). Sub-ótimo mas funcional. |
| Promoção de spec 05-04 ainda não aplicada (campo `promovida_em` faltando) | Dashboard 3 mostra "—" pra notas geradas em glosas pré-migração. Cosmético. |
| Mobile abre dashboard e renderiza vazio sem aviso | README de operação documenta a limitação; usuário aprende rapidamente que dashboard é desktop-only. |

## 13. Trabalhos subsequentes

- **Suporte mobile via Mirror** — script que copia `codex-technomanticus/{02-Glosas,03-Dominios,04-Sendas}` pra `Codex-mirror/` versionado, sincronizável via GitSync. Quando "estudar hoje no commute" virar dor.
- **"O que estudar hoje?" prescritivo** — modelo de ordem global e prioridade (sub-spec). Quando a heurística atual incomodar.
- **Campo `concluido_em`** no público pra habilitar dashboard de velocidade temporal. Sub-spec leve no público.
- **Histogramas/gráficos** (cadência de promoção mensal, glosas arquivadas por época). Quando a leitura analítica frequente justificar o esforço de visualização.
- **Hub MOC** `00-Meta/Dashboards.md` — caso o número de dashboards cresça além de 3-4.
- **Skill `/sync-cross-vault`** automatizando criação/verificação do symlink. Caso acabe replicando o setup em mais de uma máquina.
- **CSS custom** pros dashboards (cores diferenciadas, status badges). Cosmético.
