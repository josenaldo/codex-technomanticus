# Migração `progresso` → `progress` — Plano de Execução

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrar a propriedade de frontmatter `progresso` (PT, valores variados) para `progress` (EN, 5 estados padronizados) em dois repositórios coordenadamente, sem quebrar dashboards do apocrypha.

**Architecture:** Migração ordenada em 7 fases: branch + templates → skills (público) → notas existentes via sed direcionado (público + apocrypha) → notas consumíveis sem o campo (inserção via Python) → dashboards (apocrypha) → prosa → verificação. Cada fase tem dry-run + amostra antes de aplicar em massa. Sem backward-compat: cutover completo.

**Tech Stack:** `bash`, `sed`, `grep`, `git`, `python3` (para parsing de YAML frontmatter quando preciso inserir o campo). Sem dependências exóticas.

**Repositórios envolvidos:**
- Público: `/home/josenaldo/repos/personal/codex-technomanticus` (branch `feat/migrate-progress-property` já criada)
- Apocrypha: `/home/josenaldo/repos/personal/codex-technomanticus-apocrypha` (branch a criar)

**Spec:** `docs/superpowers/specs/2026-05-28-progress-property-migration-design.md`

---

## Mapping de referência (citar nas tasks)

**Valores antigos → novos:**

```
pendente   → backlog
andamento  → in_progress
em-curso   → in_progress
feito      → done
completo   → done
pausado    → paused
abandonado → abandoned
```

**Tipos consumíveis (recebem `progress`):**

```
glosa, concept, lesson, workbook, lesson-workbook,
community-session, community-workbook,
mock-interview, mock-interview-script, mock-interview-coaching-log
```

**Tipos não consumíveis (não recebem; se tiverem `progresso:` herdado, remover):**

```
moc, glossary, reference, how-to, til, dashboard,
trail, senda, trail-index, roadmap, todo-list
```

---

## Task 1: Branch no apocrypha

**Files:**
- Modify: nenhum (apenas git)

- [ ] **Step 1.1: Verificar working tree do apocrypha**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus-apocrypha && git status --short && git branch --show-current
```

Expected: lista de arquivos modificados (pode ter vault backups pendentes); branch atual provavelmente `main`.

- [ ] **Step 1.2: Stash mudanças não relacionadas se houver**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus-apocrypha && git stash push -u -m "pre-progress-migration $(date +%Y%m%d-%H%M%S)" 2>&1 | tail -3
```

Expected: ou "Saved working directory..." ou "No local changes to save".

- [ ] **Step 1.3: Criar branch**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus-apocrypha && git checkout -b feat/migrate-progress-property && git branch --show-current
```

Expected: `feat/migrate-progress-property`.

---

## Task 2: Templates do público

**Files:**
- Modify: `00-Meta/templates/Template - Glosa.md`
- Modify: `00-Meta/templates/Template - Nota.md`
- Modify: `00-Meta/templates/Template - Interview Note.md` (adicionar campo)

- [ ] **Step 2.1: Atualizar Template - Glosa.md**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
sed -i 's/^progresso: andamento$/progress: in_progress/' "00-Meta/templates/Template - Glosa.md"
grep -E "^(progresso|progress):" "00-Meta/templates/Template - Glosa.md"
```

Expected output: `progress: in_progress`

- [ ] **Step 2.2: Atualizar Template - Nota.md**

```bash
sed -i 's/^progresso: pendente$/progress: backlog/' "00-Meta/templates/Template - Nota.md"
grep -E "^(progresso|progress):" "00-Meta/templates/Template - Nota.md"
```

Expected output: `progress: backlog`

- [ ] **Step 2.3: Adicionar progress em Template - Interview Note.md**

Insere `progress: backlog` na linha imediatamente após `status: seedling`:

```bash
sed -i '/^status: seedling$/a\progress: backlog' "00-Meta/templates/Template - Interview Note.md"
sed -n '1,12p' "00-Meta/templates/Template - Interview Note.md"
```

Expected: frontmatter contém `status: seedling` seguido de `progress: backlog`.

- [ ] **Step 2.4: Commit**

```bash
git add "00-Meta/templates/Template - Glosa.md" "00-Meta/templates/Template - Nota.md" "00-Meta/templates/Template - Interview Note.md"
git commit -m "feat(templates): migrar progresso → progress nos templates consumíveis

Glosa: andamento → in_progress
Nota: pendente → backlog
Interview Note: adiciona progress: backlog (type=concept, faltava o campo)"
```

Expected: `3 files changed`.

---

## Task 3: Skills do público

**Files:**
- Modify: `.claude/skills/arquivar-glosas/SKILL.md`
- Modify: `.claude/skills/acordar-glosas/SKILL.md`
- Modify: `.claude/skills/promover-glosa/SKILL.md`
- Modify: `.claude/skills/sintetizar-glosas/SKILL.md`
- Modify: `.claude/skills/enriquecer-nota/references/lentes.md`

`.agents/skills/` é symlink para `.claude/skills/` — alterar em um lugar só.

- [ ] **Step 3.1: arquivar-glosas — substituir referências**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
sed -i \
  -e 's/`progresso`/`progress`/g' \
  -e 's/progresso: andamento/progress: in_progress/g' \
  -e 's/progresso: feito/progress: done/g' \
  -e 's/progresso: abandonado/progress: abandoned/g' \
  -e 's/progresso: pausado/progress: paused/g' \
  -e 's/progresso: pendente/progress: backlog/g' \
  .claude/skills/arquivar-glosas/SKILL.md
grep -n "progresso\|progress" .claude/skills/arquivar-glosas/SKILL.md
```

Expected: nenhuma linha com `progresso` (palavra exata); todas as ocorrências usam `progress` + valores novos.

- [ ] **Step 3.2: acordar-glosas — substituir + ajustar reset**

```bash
sed -i \
  -e 's/`progresso`/`progress`/g' \
  -e 's/progresso: andamento/progress: in_progress/g' \
  .claude/skills/acordar-glosas/SKILL.md
grep -n "progresso\|progress" .claude/skills/acordar-glosas/SKILL.md
```

Expected: nenhuma ocorrência de `progresso`; descrição da reativação usa `progress: in_progress`.

- [ ] **Step 3.3: promover-glosa — substituir filtros e transições**

```bash
sed -i \
  -e 's/`progresso`/`progress`/g' \
  -e 's/progresso: andamento/progress: in_progress/g' \
  -e 's/progresso: feito/progress: done/g' \
  -e 's/`andamento` ou `feito`/`in_progress` ou `done`/g' \
  -e 's/`andamento`\|`feito`/`in_progress`\|`done`/g' \
  -e 's/é `andamento`, mudar pra `feito`/é `in_progress`, mudar pra `done`/g' \
  .claude/skills/promover-glosa/SKILL.md
grep -n "progresso\|andamento\|feito" .claude/skills/promover-glosa/SKILL.md
```

Expected: nenhuma menção a `progresso`, `andamento` ou `feito`.

- [ ] **Step 3.4: sintetizar-glosas — substituir exemplo**

```bash
sed -i \
  -e 's/progresso: andamento/progress: in_progress/g' \
  -e 's/`progresso`/`progress`/g' \
  .claude/skills/sintetizar-glosas/SKILL.md
grep -n "progresso\|progress" .claude/skills/sintetizar-glosas/SKILL.md
```

Expected: nenhuma menção a `progresso`.

- [ ] **Step 3.5: enriquecer-nota/lentes.md — substituir**

```bash
sed -i \
  -e 's/progresso: andamento/progress: in_progress/g' \
  -e 's/`progresso`/`progress`/g' \
  .claude/skills/enriquecer-nota/references/lentes.md
grep -n "progresso\|progress" .claude/skills/enriquecer-nota/references/lentes.md
```

Expected: nenhuma menção a `progresso`.

- [ ] **Step 3.6: Validação cruzada de todas as skills**

```bash
grep -rn "progresso" .claude/skills/
```

Expected: nenhum output (exit code 1).

- [ ] **Step 3.7: Commit**

```bash
git add .claude/skills/
git commit -m "feat(skills): migrar progresso → progress nas 5 skills de glosa/nota

- arquivar-glosas, acordar-glosas, promover-glosa: filtros e transições remapeados
- sintetizar-glosas, enriquecer-nota: exemplos atualizados
- Valores em PT (andamento, feito, pendente) substituídos pelos equivalentes EN"
```

Expected: commit com 5 arquivos.

---

## Task 4: Templates do apocrypha

**Files:**
- Modify: `00-Meta/templates/Template - Nota.md`
- Modify: `00-Meta/templates/Template - Glosa.md`
- Modify: `00-Meta/templates/Lucy/Lucy - Processed.md` (se tiver `progresso:`)
- Modify: `00-Meta/templates/Lucy/Lucy - Workbook.md` (se tiver `progresso:`)
- Inspect: `00-Meta/templates/Lucy/Lucy - Ebook MOC.md` (não tocar se for `type: moc`)

- [ ] **Step 4.1: Inspecionar templates Lucy primeiro**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus-apocrypha
for f in "00-Meta/templates/Lucy/Lucy - Processed.md" "00-Meta/templates/Lucy/Lucy - Workbook.md" "00-Meta/templates/Lucy/Lucy - Ebook MOC.md"; do
  echo "=== $f ==="
  sed -n '1,15p' "$f"
done
```

Expected: três frontmatters mostrados. Confirmar para cada arquivo:
- `Lucy - Processed.md`: deve ser `type: lesson` (consumível, migrar)
- `Lucy - Workbook.md`: deve ser `type: workbook` (consumível, migrar)
- `Lucy - Ebook MOC.md`: deve ser `type: moc` (não consumível, remover `progresso:` se existir)

- [ ] **Step 4.2: Template - Nota.md (apocrypha)**

```bash
sed -i 's/^progresso: pendente$/progress: backlog/' "00-Meta/templates/Template - Nota.md"
grep -E "^(progresso|progress):" "00-Meta/templates/Template - Nota.md"
```

Expected: `progress: backlog`.

- [ ] **Step 4.3: Template - Glosa.md (apocrypha)**

```bash
sed -i 's/^progresso: andamento$/progress: in_progress/' "00-Meta/templates/Template - Glosa.md"
grep -E "^(progresso|progress):" "00-Meta/templates/Template - Glosa.md"
```

Expected: `progress: in_progress`.

- [ ] **Step 4.4: Lucy - Processed.md e Lucy - Workbook.md (se consumíveis)**

Para cada template Lucy consumível detectado no Step 4.1:

```bash
for f in "00-Meta/templates/Lucy/Lucy - Processed.md" "00-Meta/templates/Lucy/Lucy - Workbook.md"; do
  sed -i \
    -e 's/^progresso: pendente$/progress: backlog/' \
    -e 's/^progresso: andamento$/progress: in_progress/' \
    -e 's/^progresso: feito$/progress: done/' \
    "$f"
  echo "=== $f ==="
  grep -E "^(progresso|progress):" "$f"
done
```

Expected: cada um mostra a linha `progress: <valor>`.

- [ ] **Step 4.5: Lucy - Ebook MOC.md — remover progresso herdado se existir**

```bash
sed -i '/^progresso:/d' "00-Meta/templates/Lucy/Lucy - Ebook MOC.md"
grep -E "^(progresso|progress):" "00-Meta/templates/Lucy/Lucy - Ebook MOC.md" && echo "AINDA TEM" || echo "OK: limpo"
```

Expected: `OK: limpo`.

- [ ] **Step 4.6: Validação dos templates do apocrypha**

```bash
grep -rn "^progresso:" 00-Meta/templates/
```

Expected: nenhum output.

- [ ] **Step 4.7: Commit**

```bash
git add "00-Meta/templates/"
git commit -m "feat(templates): migrar progresso → progress nos templates do apocrypha

- Template - Nota, Template - Glosa: valores remapeados (PT → EN)
- Lucy - Processed, Lucy - Workbook: valores remapeados (consumíveis)
- Lucy - Ebook MOC: campo removido (tipo moc, não consumível)"
```

Expected: commit com até 5 arquivos.

---

## Task 5: Script de migração de frontmatter em notas existentes

Esta task **prepara** o script reutilizável. Aplicação real fica nas Tasks 6 e 7.

**Files:**
- Create: `/tmp/migrate-progress.sh` (script utilitário; não vai pro git)

- [ ] **Step 5.1: Criar script de substituição de valor em mesma linha**

```bash
cat > /tmp/migrate-progress.sh <<'EOF'
#!/usr/bin/env bash
# Migra `progresso:` → `progress:` com remapeamento de valores em uma única linha.
# Uso: migrate-progress.sh <arquivo.md> [--dry-run]
# Sem --dry-run: modifica o arquivo in-place.
# Com --dry-run: imprime o diff esperado, sem modificar.
set -euo pipefail

FILE="$1"
DRY="${2:-}"

if [[ ! -f "$FILE" ]]; then
  echo "ERRO: arquivo não existe: $FILE" >&2
  exit 1
fi

# Sequência de substituições (em ordem: valor primeiro, depois chave).
# Importante: substituir valor ANTES de renomear a chave, porque a regex
# casa "progresso: <valor-antigo>" — depois renomeamos a chave.
SED_ARGS=(
  -e 's|^progresso: pendente$|progress: backlog|'
  -e 's|^progresso: andamento$|progress: in_progress|'
  -e 's|^progresso: em-curso$|progress: in_progress|'
  -e 's|^progresso: feito$|progress: done|'
  -e 's|^progresso: completo$|progress: done|'
  -e 's|^progresso: pausado$|progress: paused|'
  -e 's|^progresso: abandonado$|progress: abandoned|'
  # Fallback: se sobrou algum `progresso:` com valor desconhecido,
  # apenas renomeia a chave (preserva valor) — será apontado pelo checker.
  -e 's|^progresso:|progress:|'
)

if [[ "$DRY" == "--dry-run" ]]; then
  diff <(cat "$FILE") <(sed "${SED_ARGS[@]}" "$FILE") || true
else
  sed -i "${SED_ARGS[@]}" "$FILE"
fi
EOF
chmod +x /tmp/migrate-progress.sh
/tmp/migrate-progress.sh
```

Expected: erro `arquivo não existe` (sem args) — confirma que script existe e é executável.

- [ ] **Step 5.2: Smoke test com arquivo descartável**

```bash
TMPDIR=$(mktemp -d)
cat > "$TMPDIR/test.md" <<'EOF'
---
title: Teste
progresso: andamento
type: glosa
---
conteúdo
EOF

/tmp/migrate-progress.sh "$TMPDIR/test.md" --dry-run
echo "---"
/tmp/migrate-progress.sh "$TMPDIR/test.md"
cat "$TMPDIR/test.md"
rm -rf "$TMPDIR"
```

Expected: dry-run mostra `< progresso: andamento` e `> progress: in_progress`; aplicação real produz frontmatter com `progress: in_progress`.

---

## Task 6: Migrar frontmatter no público

**Files:**
- Modify: 91 notas com `progresso:` em `codex-technomanticus`

- [ ] **Step 6.1: Catalogar notas alvo + valores atuais**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
grep -rl "^progresso:" --include="*.md" . > /tmp/public-progresso-files.txt
wc -l /tmp/public-progresso-files.txt
grep -rh "^progresso:" --include="*.md" . | sort | uniq -c | sort -rn
```

Expected: 91 arquivos; distribuição `andamento` (77), `pendente` (32), `feito` (4), etc. — números podem mudar se há linhas de comentário em templates.

- [ ] **Step 6.2: Dry-run em 5 amostras aleatórias**

```bash
shuf -n 5 /tmp/public-progresso-files.txt | while read f; do
  echo "=== $f ==="
  /tmp/migrate-progress.sh "$f" --dry-run
done
```

Expected: 5 diffs mostrando `< progresso: <valor>` → `> progress: <novo-valor>`. Inspecionar manualmente. **CHECKPOINT** — se algo parecer errado, parar e ajustar o script.

- [ ] **Step 6.3: Aplicar em todos os arquivos públicos**

```bash
while read f; do /tmp/migrate-progress.sh "$f"; done < /tmp/public-progresso-files.txt
echo "Aplicado em $(wc -l < /tmp/public-progresso-files.txt) arquivos."
```

Expected: contador igual ao da Step 6.1.

- [ ] **Step 6.4: Verificar resultado**

```bash
grep -rh "^progresso:" --include="*.md" . | wc -l
grep -rh "^progress:" --include="*.md" . | sort | uniq -c | sort -rn
```

Expected: primeiro `0`; segundo lista distribuição em estados novos. Valores devem estar todos em `{backlog, in_progress, paused, done, abandoned}`.

- [ ] **Step 6.5: Identificar e remover `progresso:` herdado em não consumíveis**

Casos onde a regex pode ter convertido para `progress:` mas a nota é não consumível (ex.: moc, glossary). Detectar:

```bash
# Lista arquivos onde progress: existe mas type: é não consumível
python3 <<'PY'
import re, pathlib
NON_CONSUMABLE = {"moc", "glossary", "reference", "how-to", "til", "dashboard",
                  "trail", "senda", "trail-index", "roadmap", "todo-list"}
root = pathlib.Path(".")
hits = []
for p in root.rglob("*.md"):
    if "/.git/" in str(p) or "/node_modules/" in str(p):
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        continue
    if not text.startswith("---"):
        continue
    end = text.find("\n---", 4)
    if end == -1:
        continue
    fm = text[4:end]
    m_type = re.search(r"^type:\s*(\S+)", fm, re.M)
    m_prog = re.search(r"^progress:\s*(\S+)", fm, re.M)
    if m_type and m_prog and m_type.group(1) in NON_CONSUMABLE:
        hits.append((str(p), m_type.group(1), m_prog.group(1)))
for h in hits:
    print(h)
print(f"TOTAL: {len(hits)}")
PY
```

Expected: lista (talvez vazia) de arquivos não consumíveis que herdaram `progress:`. **CHECKPOINT** — se houver, decidir caso a caso se remove ou se o `type:` está errado.

- [ ] **Step 6.6: Remover `progress:` dos não consumíveis identificados**

Para cada arquivo apontado em 6.5 (substituir `<path>` pelo caminho real, ou rodar em loop):

```bash
# Exemplo — repetir por arquivo identificado:
# sed -i '/^progress:/d' "<path>"

# Ou em batch a partir da lista (se a Step 6.5 escreveu nomes em /tmp):
python3 <<'PY' > /tmp/non-consumable-with-progress.txt
import re, pathlib
NON_CONSUMABLE = {"moc", "glossary", "reference", "how-to", "til", "dashboard",
                  "trail", "senda", "trail-index", "roadmap", "todo-list"}
for p in pathlib.Path(".").rglob("*.md"):
    if "/.git/" in str(p): continue
    try: text = p.read_text(encoding="utf-8")
    except: continue
    if not text.startswith("---"): continue
    end = text.find("\n---", 4)
    if end == -1: continue
    fm = text[4:end]
    m_type = re.search(r"^type:\s*(\S+)", fm, re.M)
    m_prog = re.search(r"^progress:", fm, re.M)
    if m_type and m_prog and m_type.group(1) in NON_CONSUMABLE:
        print(p)
PY

while read f; do sed -i '/^progress:/d' "$f"; done < /tmp/non-consumable-with-progress.txt
wc -l /tmp/non-consumable-with-progress.txt
```

Expected: contagem de arquivos limpos. Se 0, esse step é no-op.

- [ ] **Step 6.7: Identificar notas consumíveis SEM `progress:` e adicionar `progress: backlog`**

```bash
python3 <<'PY' > /tmp/consumable-without-progress.txt
import re, pathlib
CONSUMABLE = {"glosa", "concept", "lesson", "workbook", "lesson-workbook",
              "community-session", "community-workbook",
              "mock-interview", "mock-interview-script",
              "mock-interview-coaching-log"}
for p in pathlib.Path(".").rglob("*.md"):
    s = str(p)
    if any(x in s for x in ("/.git/", "/node_modules/", "/00-Meta/templates/",
                            "/docs/superpowers/", "/.claude/", "/.agents/",
                            "/devlog/", "/memory/")):
        continue
    try: text = p.read_text(encoding="utf-8")
    except: continue
    if not text.startswith("---"): continue
    end = text.find("\n---", 4)
    if end == -1: continue
    fm = text[4:end]
    m_type = re.search(r"^type:\s*(\S+)", fm, re.M)
    m_prog = re.search(r"^progress:", fm, re.M)
    if m_type and (m_type.group(1) in CONSUMABLE) and not m_prog:
        print(p)
PY

wc -l /tmp/consumable-without-progress.txt
head -5 /tmp/consumable-without-progress.txt
```

Expected: lista (pode ser zero ou várias). **CHECKPOINT** — confirmar contagem razoável.

- [ ] **Step 6.8: Inserir `progress: backlog` nas notas consumíveis sem o campo**

Inserir imediatamente após a linha `type:`:

```bash
python3 <<'PY'
import re, pathlib
files = [l.strip() for l in open("/tmp/consumable-without-progress.txt") if l.strip()]
for f in files:
    p = pathlib.Path(f)
    text = p.read_text(encoding="utf-8")
    # Insere progress: backlog logo após a linha `type: ...`
    new = re.sub(
        r"^(type:\s*\S+)$",
        r"\1\nprogress: backlog",
        text,
        count=1,
        flags=re.M,
    )
    if new != text:
        p.write_text(new, encoding="utf-8")
print(f"OK: {len(files)} arquivos atualizados.")
PY
```

Expected: `OK: N arquivos atualizados.` onde N = contagem do step 6.7.

- [ ] **Step 6.9: Verificação cruzada do público**

```bash
echo "Arquivos com progresso: residual:"
grep -rl "^progresso:" --include="*.md" . | wc -l
echo "Distribuição final de progress::"
grep -rh "^progress:" --include="*.md" . | sort | uniq -c | sort -rn
echo "Valores fora do conjunto esperado:"
grep -rh "^progress:" --include="*.md" . \
  | grep -vE "^progress: (backlog|in_progress|paused|done|abandoned)$" \
  || echo "(nenhum)"
```

Expected: residual `0`; distribuição com valores apenas em `{backlog, in_progress, paused, done, abandoned}`; mensagem `(nenhum)` para valores inesperados.

- [ ] **Step 6.10: Commit do público — frontmatter de notas**

```bash
git add -u
git status --short | head -20
git commit -m "feat(notes): migrar progresso → progress em todas as notas consumíveis

- 91 notas com progresso: substituídas por progress: + valores remapeados
- Notas consumíveis sem o campo: progress: backlog adicionado
- Notas não consumíveis com progress: herdado: campo removido (limpa inconsistência)

Mapeamento de valores: pendente→backlog, andamento/em-curso→in_progress,
feito/completo→done, pausado→paused, abandonado→abandoned."
```

Expected: commit com dezenas/centenas de arquivos modificados.

---

## Task 7: Migrar frontmatter no apocrypha

**Files:**
- Modify: 21 notas com `progresso:` + ~52 notas consumíveis sem o campo (Lucy + GCA)

- [ ] **Step 7.1: Catalogar notas alvo no apocrypha**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus-apocrypha
# Excluir o symlink Codex (aponta pro público, já migrado)
find . -name "*.md" -not -path "./.git/*" -not -path "./Codex/*" -not -path "./node_modules/*" > /tmp/apocrypha-all.txt
grep -l "^progresso:" -- $(cat /tmp/apocrypha-all.txt) 2>/dev/null > /tmp/apocrypha-progresso-files.txt
wc -l /tmp/apocrypha-progresso-files.txt
grep -h "^progresso:" -- $(cat /tmp/apocrypha-progresso-files.txt) | sort | uniq -c | sort -rn
```

Expected: 21 arquivos; distribuição `pendente` (20), `andamento` (1).

- [ ] **Step 7.2: Dry-run em até 5 amostras do apocrypha**

```bash
shuf -n 5 /tmp/apocrypha-progresso-files.txt | while read f; do
  echo "=== $f ==="
  /tmp/migrate-progress.sh "$f" --dry-run
done
```

Expected: 5 diffs mostrando substituição correta. **CHECKPOINT** — inspecionar manualmente.

- [ ] **Step 7.3: Aplicar em todos os arquivos do apocrypha**

```bash
while read f; do /tmp/migrate-progress.sh "$f"; done < /tmp/apocrypha-progresso-files.txt
echo "Aplicado em $(wc -l < /tmp/apocrypha-progresso-files.txt) arquivos."
```

Expected: contador igual ao da Step 7.1.

- [ ] **Step 7.4: Identificar e remover `progresso:` herdado em não consumíveis (apocrypha)**

```bash
python3 <<'PY' > /tmp/apocrypha-non-consumable-with-progress.txt
import re, pathlib
NON_CONSUMABLE = {"moc", "glossary", "reference", "how-to", "til", "dashboard",
                  "trail", "senda", "trail-index", "roadmap", "todo-list"}
root = pathlib.Path(".")
for p in root.rglob("*.md"):
    s = str(p)
    if "/.git/" in s or "/Codex/" in s or "/node_modules/" in s: continue
    try: text = p.read_text(encoding="utf-8")
    except: continue
    if not text.startswith("---"): continue
    end = text.find("\n---", 4)
    if end == -1: continue
    fm = text[4:end]
    m_type = re.search(r"^type:\s*(\S+)", fm, re.M)
    m_prog = re.search(r"^progress:", fm, re.M)
    if m_type and (m_type.group(1) in NON_CONSUMABLE) and m_prog:
        print(p)
PY
wc -l /tmp/apocrypha-non-consumable-with-progress.txt
while read f; do sed -i '/^progress:/d' "$f"; done < /tmp/apocrypha-non-consumable-with-progress.txt
```

Expected: contagem possivelmente zero (apocrypha hoje só tem `pendente` em consumíveis).

- [ ] **Step 7.5: Identificar e popular notas consumíveis sem `progress:` (Lucy + GCA + outras)**

```bash
python3 <<'PY' > /tmp/apocrypha-consumable-without-progress.txt
import re, pathlib
CONSUMABLE = {"glosa", "concept", "lesson", "workbook", "lesson-workbook",
              "community-session", "community-workbook",
              "mock-interview", "mock-interview-script",
              "mock-interview-coaching-log"}
root = pathlib.Path(".")
for p in root.rglob("*.md"):
    s = str(p)
    if any(x in s for x in ("/.git/", "/Codex/", "/node_modules/",
                            "/00-Meta/templates/", "/docs/", "/.claude/",
                            "/.agents/", "/memory/")):
        continue
    try: text = p.read_text(encoding="utf-8")
    except: continue
    if not text.startswith("---"): continue
    end = text.find("\n---", 4)
    if end == -1: continue
    fm = text[4:end]
    m_type = re.search(r"^type:\s*(\S+)", fm, re.M)
    m_prog = re.search(r"^progress:", fm, re.M)
    if m_type and (m_type.group(1) in CONSUMABLE) and not m_prog:
        print(p)
PY
wc -l /tmp/apocrypha-consumable-without-progress.txt
head -10 /tmp/apocrypha-consumable-without-progress.txt
```

Expected: lista com ~52 arquivos (GCA + Lucy sem o campo). **CHECKPOINT** — confirmar.

- [ ] **Step 7.6: Inserir `progress: backlog` nas notas consumíveis sem o campo (apocrypha)**

```bash
python3 <<'PY'
import re, pathlib
files = [l.strip() for l in open("/tmp/apocrypha-consumable-without-progress.txt") if l.strip()]
for f in files:
    p = pathlib.Path(f)
    text = p.read_text(encoding="utf-8")
    new = re.sub(
        r"^(type:\s*\S+)$",
        r"\1\nprogress: backlog",
        text,
        count=1,
        flags=re.M,
    )
    if new != text:
        p.write_text(new, encoding="utf-8")
print(f"OK: {len(files)} arquivos atualizados.")
PY
```

Expected: `OK: N arquivos atualizados.` onde N = contagem do step 7.5.

- [ ] **Step 7.7: Verificação cruzada do apocrypha**

```bash
echo "Arquivos com progresso: residual:"
find . -name "*.md" -not -path "./.git/*" -not -path "./Codex/*" -exec grep -l "^progresso:" {} \; | wc -l
echo "Distribuição final de progress::"
find . -name "*.md" -not -path "./.git/*" -not -path "./Codex/*" -exec grep -h "^progress:" {} \; | sort | uniq -c | sort -rn
echo "Valores fora do conjunto esperado:"
find . -name "*.md" -not -path "./.git/*" -not -path "./Codex/*" -exec grep -h "^progress:" {} \; \
  | grep -vE "^progress: (backlog|in_progress|paused|done|abandoned)$" \
  || echo "(nenhum)"
```

Expected: residual `0`; distribuição válida; `(nenhum)` para valores inesperados.

- [ ] **Step 7.8: Commit do apocrypha — frontmatter de notas**

```bash
git add -u
git status --short | head -20
git commit -m "feat(notes): migrar progresso → progress em notas consumíveis do apocrypha

- 21 notas com progresso: substituídas por progress: + valores remapeados
- ~52 notas consumíveis sem o campo (Lucy + GCA): progress: backlog adicionado
- Inclui lesson, workbook, community-session, community-workbook,
  mock-interview, mock-interview-script, mock-interview-coaching-log"
```

Expected: commit com várias dezenas de arquivos.

---

## Task 8: Dashboards do apocrypha

**Files:**
- Modify: `00-Meta/dashboards/Dashboard - Progresso agregado.md`
- Modify: `00-Meta/dashboards/Dashboard - O que estudar hoje.md`
- Modify: `00-Meta/dashboards/Dashboard - Cross-glosa.md`

- [ ] **Step 8.1: Dashboard - Cross-glosa.md (mais simples — só display)**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus-apocrypha
sed -i 's/g\.progresso /g.progress /g; s/g\.progresso?/g.progress?/g; s/g\.progresso\b/g.progress/g' \
  "00-Meta/dashboards/Dashboard - Cross-glosa.md"
grep -n "progresso\|progress" "00-Meta/dashboards/Dashboard - Cross-glosa.md"
```

Expected: nenhuma menção a `progresso` (palavra exata). Header "Progresso" do título manter como prosa? — verificar; ver step 8.4.

- [ ] **Step 8.2: Dashboard - O que estudar hoje.md**

Substituir referências em JS:

```bash
sed -i \
  -e 's/p\.progresso/p.progress/g' \
  -e 's/n\.progresso/n.progress/g' \
  -e 's/"andamento"/"in_progress"/g' \
  -e 's/"feito"/"done"/g' \
  -e 's/"pausado"/"paused"/g' \
  -e 's/"abandonado"/"abandoned"/g' \
  -e 's/"pendente"/"backlog"/g' \
  -e 's/`progresso: andamento`/`progress: in_progress`/g' \
  -e 's/`progresso`/`progress`/g' \
  "00-Meta/dashboards/Dashboard - O que estudar hoje.md"
grep -n "progresso\|andamento\|feito\|pausado\|abandonado\|pendente" \
  "00-Meta/dashboards/Dashboard - O que estudar hoje.md"
```

Expected: nenhuma linha de código com palavras antigas. Pode sobrar prosa do título/descrição com "andamento" — verificar.

- [ ] **Step 8.3: Dashboard - Progresso agregado.md**

```bash
sed -i \
  -e 's/r\.progresso/r.progress/g' \
  -e 's/p\.progresso/p.progress/g' \
  -e 's/"andamento"/"in_progress"/g' \
  -e 's/"feito"/"done"/g' \
  -e 's/"pausado"/"paused"/g' \
  -e 's/"abandonado"/"abandoned"/g' \
  -e 's/"pendente"/"backlog"/g' \
  -e 's/feito: 0, andamento: 0, pausado: 0, abandonado: 0, pendente: 0/done: 0, in_progress: 0, paused: 0, abandoned: 0, backlog: 0/g' \
  -e 's/c\.feito/c.done/g; s/c\.andamento/c.in_progress/g; s/c\.pausado/c.paused/g; s/c\.abandonado/c.abandoned/g; s/c\.pendente/c.backlog/g' \
  "00-Meta/dashboards/Dashboard - Progresso agregado.md"
grep -n "progresso\|andamento\|feito\|pausado\|abandonado\|pendente" \
  "00-Meta/dashboards/Dashboard - Progresso agregado.md"
```

Expected: nenhuma linha de código com identificadores antigos. Pode sobrar título/prosa em PT.

- [ ] **Step 8.4: Revisão visual dos 3 dashboards**

```bash
for f in "00-Meta/dashboards/Dashboard - Cross-glosa.md" \
         "00-Meta/dashboards/Dashboard - O que estudar hoje.md" \
         "00-Meta/dashboards/Dashboard - Progresso agregado.md"; do
  echo "=== $f ==="
  cat "$f"
done
```

Expected: leitura manual. Verificar:
- Nenhum `g.progresso`, `p.progresso`, `r.progresso` restante
- Nenhuma comparação com valores em PT (`"andamento"`, etc.)
- Rótulos exibidos em PT (`Feitas`, `Em andamento`, etc.) podem ser mantidos — são labels visuais, não dependem da chave

- [ ] **Step 8.5: Commit dos dashboards**

```bash
git add "00-Meta/dashboards/"
git commit -m "feat(dashboards): migrar queries de progresso → progress

- Dashboard - Progresso agregado: queries Dataview/DataviewJS e objeto de grupo
- Dashboard - O que estudar hoje: filtros .where() e checagens de valor
- Dashboard - Cross-glosa: referência de display

Rótulos visuais em PT (\"Em andamento\", \"Feitas\") preservados;
apenas chaves e valores comparáveis foram traduzidos para EN."
```

Expected: commit com 3 arquivos.

---

## Task 9: Prosa em guia/skills.md (apocrypha)

**Files:**
- Modify: `00-Meta/guia/skills.md`

- [ ] **Step 9.1: Atualizar as 2 referências literais ao campo**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus-apocrypha
sed -i \
  -e 's/`progresso`/`progress`/g' \
  -e 's/`progresso: andamento`/`progress: in_progress`/g' \
  "00-Meta/guia/skills.md"
grep -n "progresso\|progress" "00-Meta/guia/skills.md"
```

Expected: apenas `progress` aparece (uma menção como descrição independente de filtro e uma como reset ao acordar).

- [ ] **Step 9.2: Commit**

```bash
git add "00-Meta/guia/skills.md"
git commit -m "docs(guia): atualizar referências literais ao campo progresso → progress

Atualiza descrições de skills no guia do vault para refletir a nova
nomenclatura. Referências em prosa onde \"progresso\" é palavra comum
(CLAUDE.md, AGENTS.md, \"Como usar este vault.md\") foram preservadas."
```

Expected: commit com 1 arquivo.

---

## Task 10: Verificação final e relatório

**Files:** nenhum — apenas comandos de validação.

- [ ] **Step 10.1: Verificação cruzada nos dois repos**

```bash
echo "=== PÚBLICO ==="
cd /home/josenaldo/repos/personal/codex-technomanticus
echo "  Residual de progresso: em frontmatter:"
grep -rh "^progresso:" --include="*.md" . | wc -l
echo "  Residual de progresso: em skills/templates:"
grep -rn "progresso" .claude/skills/ "00-Meta/templates/" 2>/dev/null | wc -l
echo "  Distribuição de progress::"
grep -rh "^progress:" --include="*.md" . | sort | uniq -c | sort -rn
echo

echo "=== APOCRYPHA ==="
cd /home/josenaldo/repos/personal/codex-technomanticus-apocrypha
echo "  Residual de progresso: em frontmatter:"
find . -name "*.md" -not -path "./.git/*" -not -path "./Codex/*" -exec grep -l "^progresso:" {} \; | wc -l
echo "  Residual de progresso em dashboards/templates/skills:"
grep -rn "progresso" "00-Meta/templates/" "00-Meta/dashboards/" "00-Meta/guia/skills.md" 2>/dev/null | wc -l
echo "  Distribuição de progress::"
find . -name "*.md" -not -path "./.git/*" -not -path "./Codex/*" -exec grep -h "^progress:" {} \; | sort | uniq -c | sort -rn
```

Expected:
- Públicos: residual frontmatter `0`, residual skills/templates `0`, distribuição usa apenas estados novos
- Apocrypha: residual frontmatter `0`, residual dashboards/templates `0`, distribuição usa apenas estados novos

- [ ] **Step 10.2: Diff resumo dos dois repos**

```bash
echo "=== PÚBLICO ==="
cd /home/josenaldo/repos/personal/codex-technomanticus
git log --oneline main..HEAD
git diff --stat main..HEAD | tail -5
echo

echo "=== APOCRYPHA ==="
cd /home/josenaldo/repos/personal/codex-technomanticus-apocrypha
git log --oneline main..HEAD
git diff --stat main..HEAD | tail -5
```

Expected: ~5 commits em cada repo; estatística de mudanças coerente com inventário.

- [ ] **Step 10.3: Checklist de revisão visual (manual pelo usuário)**

Pedir ao usuário pra:
1. Abrir Obsidian no apocrypha
2. Abrir os 3 dashboards e confirmar que populam corretamente:
   - `Dashboard - Progresso agregado` (totais globais + por domínio + por senda)
   - `Dashboard - O que estudar hoje` (em andamento + convites)
   - `Dashboard - Cross-glosa` (métricas + fila + tags)
3. Abrir 2-3 notas migradas aleatórias e confirmar que o frontmatter está bem formado

**Se algo quebrar:** capturar screenshot/mensagem; voltar ao step relevante; ajustar; recommitar.

---

## Self-Review

**Spec coverage check:**

- §"Decisões de design > Escopo": Task 6/7 implementam via lista `CONSUMABLE`/`NON_CONSUMABLE` em Python (mesmo enum que o spec) ✓
- §"Decisões de design > Estados": Mapeamento literal nas Tasks 5/6/7 ✓
- §"Decisões de design > Comportamento por situação": as 4 situações cobertas em Steps 6.3/6.5/6.7 (público) e 7.3/7.4/7.5 (apocrypha) ✓
- §"Decisões de design > Sem backward-compat": script `migrate-progress.sh` substitui de uma vez, sem alias ✓
- §"Inventário > Público": Tasks 2 (templates) + 3 (skills) + 6 (frontmatter) cobrem tudo ✓
- §"Inventário > Apocrypha": Tasks 4 (templates) + 7 (frontmatter) + 8 (dashboards) + 9 (prosa) cobrem tudo ✓
- §"Mudanças semânticas nas skills": Task 3 atualiza textualmente; comportamento mudo das skills emerge das substituições ✓
- §"Mudanças nos dashboards": Task 8 cobre os 3 dashboards ✓
- §"Plano de execução": Tasks 1-9 + verificação 10 — ordem alinhada ao spec ✓
- §"Critérios de verificação": Step 10.1 cobre todos os greps; 10.3 cobre validação visual ✓
- §"Não-objetivos": filtros em scripts Python excluem `/memory/`, `/devlog/`, `/.git/`, `/Codex/` (no apocrypha), `/.claude/`, templates ✓

**Placeholder scan:** Nenhum "TBD"/"TODO"/"fill in"/"appropriate". Todos os comandos têm conteúdo concreto. ✓

**Type/identifier consistency:** Constantes `CONSUMABLE`/`NON_CONSUMABLE` em Python repetidas literalmente nos Steps 6.5/6.7/7.4/7.5 (intencional: cada step é auto-contido — o engenheiro pode ler fora de ordem). ✓

**Identificadores nos sed dos dashboards:** `g.progresso`, `p.progresso`, `r.progresso`, `n.progresso`, `c.feito`, `c.andamento`, `c.pausado`, `c.abandonado`, `c.pendente` — cobrem todas as variáveis vistas nos 3 dashboards durante a exploração. ✓

---

## Execução

**Plan complete and saved to `docs/superpowers/plans/2026-05-28-progress-property-migration-execution.md`. Two execution options:**

1. **Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks, fast iteration. Cada task acima vira um job isolado; o agente principal revisa o resultado antes de seguir.

2. **Inline Execution** — execute tasks nesta sessão usando `executing-plans`, batch execution with checkpoints. Mantém todo o contexto desta conversa (útil porque já temos a topologia do vault na cabeça).

**Which approach?**
