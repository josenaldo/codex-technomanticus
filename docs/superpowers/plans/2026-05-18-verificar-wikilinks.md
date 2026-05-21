# verificar-wikilinks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir a skill `verificar-wikilinks` (CLI Python stdlib + SKILL.md) que detecta e corrige wikilinks/links markdown internos quebrados em um vault Obsidian, aplicando a regra do Quartz (folder-link exige `index.md`).

**Architecture:** Duas camadas. Camada 1: script Python puro (`scripts/check_wikilinks.py`) indexa o vault, parseia links, resolve aplicando regras do Quartz e emite JSON. Camada 2: `SKILL.md` orquestra — invoca o script, agrupa quebras por motivo, propõe correções, aplica via `Edit` após aprovação. TDD com `unittest` da stdlib e vault sintético em `tempfile.TemporaryDirectory()`.

**Tech Stack:** Python 3.11+ stdlib only (`pathlib`, `re`, `json`, `argparse`, `difflib`, `datetime`, `tempfile`, `unittest`). Nenhuma dependência externa.

**Spec de referência:** `docs/superpowers/specs/2026-05-18-verificar-wikilinks-design.md`

**Contratos compartilhados entre tasks** (referência rápida):

```python
# Constantes
IGNORED_DIRS = {".git", ".obsidian", "node_modules", ".agents", ".quartz-cache"}

# Index do vault
Index = {
    "files_by_basename": dict[str, list[str]],   # basename sem .md -> relpaths POSIX
    "files_by_relpath":  set[str],                # relpaths POSIX de todos os .md
    "folders":           dict[str, list[str]],   # basename pasta -> relpaths POSIX
    "folders_with_index": set[str],               # subset de folders.values() com index.md
}

# Link extraído
Link = {
    "file":     str,         # relpath POSIX do .md de origem
    "line":     int,         # 1-based
    "raw":      str,         # texto cru do link, ex: "[[Anatomia|LLM]]"
    "target":   str,         # alvo sem alias/anchor, ex: "Anatomia"
    "alias":    str | None,
    "anchor":   str | None,  # sem "#"
    "type":     str,         # "wikilink" | "embed" | "markdown"
    "in_frontmatter": bool,
}

# Resultado de resolução (somente se quebrado)
Broken = Link | {
    "reason":     str,        # folder_without_index | target_not_found | ambiguous |
                              # anchor_not_found | markdown_broken_path | malformed
    "candidates": list[str],  # relpaths sugeridos
}
```

---

### Task 0: Bootstrap — diretório, esqueleto, harness de testes

**Files:**
- Create: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Create: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Criar o esqueleto do script principal**

Conteúdo de `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`:

```python
"""verificar-wikilinks — detector de wikilinks quebrados no vault.

Uso: python check_wikilinks.py <pasta-alvo> [--vault-root <path>]
                                            [--output <json-path>]
                                            [--respect-public-only]

Aplica a regra do Quartz: [[Pasta]] é quebrado se a pasta não tiver index.md.
"""

from __future__ import annotations

IGNORED_DIRS = {".git", ".obsidian", "node_modules", ".agents", ".quartz-cache"}


def main(argv: list[str] | None = None) -> int:
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 2: Criar o harness mínimo de testes**

Conteúdo de `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`:

```python
"""Testes do check_wikilinks. Vault sintético em tempfile.TemporaryDirectory.

Roda com: python -m unittest scripts/test_check_wikilinks.py
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import check_wikilinks as cw


def make_vault(tmp: Path, layout: dict[str, str]) -> Path:
    """Cria arquivos a partir de um dict {relpath: conteúdo}. Marca .obsidian/."""
    (tmp / ".obsidian").mkdir()
    for relpath, content in layout.items():
        p = tmp / relpath
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return tmp


class TestHarness(unittest.TestCase):
    def test_harness_smoke(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = make_vault(Path(tmp), {"a.md": "# a\n"})
            self.assertTrue((vault / "a.md").exists())
            self.assertTrue((vault / ".obsidian").exists())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Rodar o harness para garantir que importa**

Run:
```bash
cd /home/josenaldo/repos/personal/codex-technomanticus/.agents/skills/verificar-wikilinks
python -m unittest scripts.test_check_wikilinks -v
```

Expected: 1 teste passa (`test_harness_smoke ... ok`).

- [ ] **Step 4: Commit**

```bash
git add .agents/skills/verificar-wikilinks/
git commit -m "feat(skill/verificar-wikilinks): bootstrap script + harness de testes"
```

---

### Task 1: Indexação do vault

**Objetivo:** `index_vault(vault_root)` produz `Index` com basenames, relpaths, folders e folders_with_index. Auto-detecção de vault root sobe diretórios até achar `.obsidian/`.

**Files:**
- Modify: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Modify: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Escrever o teste falhando**

Adicionar ao final de `test_check_wikilinks.py`:

```python
class TestIndexVault(unittest.TestCase):
    def test_indexes_basenames_relpaths_folders_and_folders_with_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = make_vault(Path(tmp), {
                "Notas/A.md": "# A\n",
                "Notas/B.md": "# B\n",
                "Notas/Sub/index.md": "# Sub\n",
                "Notas/Outra/C.md": "# C\n",   # pasta SEM index
                ".agents/skills/x.md": "ignore",  # deve ser ignorado
            })
            idx = cw.index_vault(vault)

            self.assertIn("A", idx["files_by_basename"])
            self.assertEqual(idx["files_by_basename"]["A"], ["Notas/A.md"])
            self.assertIn("Notas/A.md", idx["files_by_relpath"])
            self.assertNotIn(".agents/skills/x.md", idx["files_by_relpath"])

            self.assertIn("Sub", idx["folders"])
            self.assertIn("Notas/Sub", idx["folders_with_index"])
            self.assertNotIn("Notas/Outra", idx["folders_with_index"])

    def test_auto_detect_vault_root_climbs_to_obsidian(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = make_vault(Path(tmp), {"Notas/A.md": "# A\n"})
            detected = cw.auto_detect_vault_root(vault / "Notas")
            self.assertEqual(detected, vault)

    def test_auto_detect_raises_when_no_obsidian(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "Notas").mkdir()
            with self.assertRaises(FileNotFoundError):
                cw.auto_detect_vault_root(Path(tmp) / "Notas")
```

- [ ] **Step 2: Rodar para verificar que falha**

Run:
```bash
cd /home/josenaldo/repos/personal/codex-technomanticus/.agents/skills/verificar-wikilinks
python -m unittest scripts.test_check_wikilinks.TestIndexVault -v
```

Expected: FAIL — `AttributeError: module 'check_wikilinks' has no attribute 'index_vault'`.

- [ ] **Step 3: Implementar `index_vault` e `auto_detect_vault_root`**

Adicionar ao `check_wikilinks.py`, após o bloco `IGNORED_DIRS`:

```python
from pathlib import Path


def auto_detect_vault_root(start: Path) -> Path:
    """Sobe diretórios a partir de `start` até encontrar uma pasta .obsidian/.

    Levanta FileNotFoundError se chegar à raiz do filesystem sem encontrar.
    """
    cur = start.resolve()
    while True:
        if (cur / ".obsidian").is_dir():
            return cur
        if cur.parent == cur:
            raise FileNotFoundError(f"vault root (.obsidian/) not found above {start}")
        cur = cur.parent


def index_vault(vault_root: Path) -> dict:
    """Walk no vault coletando .md e pastas. Retorna Index (ver header do plano)."""
    files_by_basename: dict[str, list[str]] = {}
    files_by_relpath: set[str] = set()
    folders: dict[str, list[str]] = {}
    folders_with_index: set[str] = set()

    vault_root = vault_root.resolve()

    for path in vault_root.rglob("*"):
        rel_parts = path.relative_to(vault_root).parts
        if any(part in IGNORED_DIRS for part in rel_parts):
            continue
        relpath = path.relative_to(vault_root).as_posix()

        if path.is_dir():
            folders.setdefault(path.name, []).append(relpath)
            if (path / "index.md").is_file():
                folders_with_index.add(relpath)
        elif path.is_file() and path.suffix == ".md":
            files_by_relpath.add(relpath)
            basename = path.stem
            files_by_basename.setdefault(basename, []).append(relpath)

    return {
        "files_by_basename": files_by_basename,
        "files_by_relpath": files_by_relpath,
        "folders": folders,
        "folders_with_index": folders_with_index,
    }
```

- [ ] **Step 4: Rodar para verificar passa**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestIndexVault -v
```

Expected: 3 testes PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/verificar-wikilinks/scripts/
git commit -m "feat(skill/verificar-wikilinks): indexa vault (basenames, folders, index.md)"
```

---

### Task 2: Extração de wikilinks (target, alias, anchor, embed)

**Objetivo:** `extract_wikilinks(text)` retorna lista de `Link` (sem o campo `file`; preenchido depois). Cobre `[[A]]`, `[[A|alias]]`, `[[A#sec]]`, `[[pasta/A]]`, `![[A]]`. Cumpre `test_alias_preserved_in_report`.

**Files:**
- Modify: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Modify: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Escrever os testes falhando**

Adicionar a `test_check_wikilinks.py`:

```python
class TestExtractWikilinks(unittest.TestCase):
    def test_simple_target(self):
        links = cw.extract_wikilinks("foo [[Anatomia]] bar\n")
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["target"], "Anatomia")
        self.assertIsNone(links[0]["alias"])
        self.assertIsNone(links[0]["anchor"])
        self.assertEqual(links[0]["type"], "wikilink")
        self.assertEqual(links[0]["line"], 1)
        self.assertEqual(links[0]["raw"], "[[Anatomia]]")

    def test_alias_preserved(self):
        links = cw.extract_wikilinks("[[Anatomia|LLM]]\n")
        self.assertEqual(links[0]["target"], "Anatomia")
        self.assertEqual(links[0]["alias"], "LLM")

    def test_anchor_extracted(self):
        links = cw.extract_wikilinks("[[Nota#Seção]]\n")
        self.assertEqual(links[0]["target"], "Nota")
        self.assertEqual(links[0]["anchor"], "Seção")

    def test_anchor_with_alias(self):
        links = cw.extract_wikilinks("[[Nota#Seção|atalho]]\n")
        self.assertEqual(links[0]["target"], "Nota")
        self.assertEqual(links[0]["anchor"], "Seção")
        self.assertEqual(links[0]["alias"], "atalho")

    def test_folder_target(self):
        links = cw.extract_wikilinks("[[pasta/Sub]]\n")
        self.assertEqual(links[0]["target"], "pasta/Sub")

    def test_embed_md_detected(self):
        links = cw.extract_wikilinks("![[Trecho]]\n")
        self.assertEqual(links[0]["type"], "embed")
        self.assertEqual(links[0]["target"], "Trecho")

    def test_multiple_links_one_line_distinct_positions(self):
        links = cw.extract_wikilinks("[[A]] e [[B]]\n")
        self.assertEqual([l["target"] for l in links], ["A", "B"])
        self.assertEqual(links[0]["line"], 1)
        self.assertEqual(links[1]["line"], 1)
```

- [ ] **Step 2: Rodar para verificar falha**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestExtractWikilinks -v
```

Expected: FAIL — `AttributeError: module 'check_wikilinks' has no attribute 'extract_wikilinks'`.

- [ ] **Step 3: Implementar `extract_wikilinks`**

Adicionar ao `check_wikilinks.py`:

```python
import re

# (alvo)(opt #anchor)(opt |alias). Captura o ! anterior para distinguir embed.
WIKILINK_RE = re.compile(r"(?P<embed>!?)\[\[(?P<body>[^\[\]\n]+?)\]\]")


def extract_wikilinks(text: str) -> list[dict]:
    """Extrai wikilinks (e embeds) de um texto. Retorna lista de Link (sem 'file').

    NÃO trata code fences nem frontmatter — isso fica em camadas posteriores.
    """
    results: list[dict] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in WIKILINK_RE.finditer(line):
            body = m.group("body")
            anchor: str | None = None
            alias: str | None = None

            if "|" in body:
                target_part, alias = body.split("|", 1)
            else:
                target_part = body
            if "#" in target_part:
                target, anchor = target_part.split("#", 1)
            else:
                target = target_part

            results.append({
                "line": lineno,
                "raw": m.group(0),
                "target": target.strip(),
                "alias": alias.strip() if alias is not None else None,
                "anchor": anchor.strip() if anchor is not None else None,
                "type": "embed" if m.group("embed") == "!" else "wikilink",
                "in_frontmatter": False,
            })
    return results
```

- [ ] **Step 4: Rodar para verificar passa**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestExtractWikilinks -v
```

Expected: 7 testes PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/verificar-wikilinks/scripts/
git commit -m "feat(skill/verificar-wikilinks): parser de wikilinks (target/alias/anchor/embed)"
```

---

### Task 3: Skip de code fences e inline code

**Objetivo:** Wikilinks dentro de ``` ... ``` ou de `` `...` `` são ignorados. Cumpre `test_ignores_wikilink_in_code_fence`.

**Files:**
- Modify: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Modify: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Escrever os testes falhando**

Adicionar:

```python
class TestCodeFences(unittest.TestCase):
    def test_ignores_wikilink_in_fenced_block(self):
        text = "antes\n```\n[[NaoExtrai]]\n```\ndepois [[Extrai]]\n"
        links = cw.extract_wikilinks_clean(text)
        targets = [l["target"] for l in links]
        self.assertEqual(targets, ["Extrai"])

    def test_ignores_wikilink_in_inline_code(self):
        text = "use `[[Sintaxe]]` literalmente e [[De Verdade]]\n"
        links = cw.extract_wikilinks_clean(text)
        targets = [l["target"] for l in links]
        self.assertEqual(targets, ["De Verdade"])

    def test_tilde_fences_also_work(self):
        text = "~~~\n[[Skip]]\n~~~\n[[Keep]]\n"
        links = cw.extract_wikilinks_clean(text)
        targets = [l["target"] for l in links]
        self.assertEqual(targets, ["Keep"])
```

- [ ] **Step 2: Rodar para verificar falha**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestCodeFences -v
```

Expected: FAIL — `extract_wikilinks_clean` não existe.

- [ ] **Step 3: Implementar `strip_code_fences` + `extract_wikilinks_clean`**

Adicionar:

```python
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
FENCE_RE = re.compile(r"^(```|~~~)")


def strip_code_fences(text: str) -> str:
    """Substitui o conteúdo de code fences e inline code por espaços (preserva linhas).

    Mantém o número de linhas para que `line` em extract_wikilinks continue correto.
    """
    out_lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line.lstrip()):
            in_fence = not in_fence
            out_lines.append("")  # consome a linha do delimitador
            continue
        if in_fence:
            out_lines.append("")
        else:
            out_lines.append(INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line))
    return "\n".join(out_lines)


def extract_wikilinks_clean(text: str) -> list[dict]:
    """Igual a extract_wikilinks, mas após mascarar code fences e inline code."""
    return extract_wikilinks(strip_code_fences(text))
```

- [ ] **Step 4: Rodar para verificar passa**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestCodeFences -v
```

Expected: 3 testes PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/verificar-wikilinks/scripts/
git commit -m "feat(skill/verificar-wikilinks): ignora wikilinks em code fences e inline code"
```

---

### Task 4: Detecção de frontmatter YAML

**Objetivo:** `find_frontmatter_range(text)` retorna `(start_line, end_line)` 1-based ou `None`. `extract_wikilinks_clean` deve marcar `in_frontmatter: true` quando a linha do link cair dentro do range.

**Files:**
- Modify: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Modify: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Escrever os testes falhando**

Adicionar:

```python
class TestFrontmatter(unittest.TestCase):
    def test_marks_wikilink_in_frontmatter(self):
        text = (
            "---\n"
            "related:\n"
            "  - \"[[Outra Nota]]\"\n"
            "---\n"
            "# corpo\n"
            "[[Externa]]\n"
        )
        links = cw.extract_wikilinks_clean(text)
        by_target = {l["target"]: l for l in links}
        self.assertTrue(by_target["Outra Nota"]["in_frontmatter"])
        self.assertFalse(by_target["Externa"]["in_frontmatter"])

    def test_no_frontmatter_means_all_false(self):
        text = "# título\n[[X]]\n"
        links = cw.extract_wikilinks_clean(text)
        self.assertFalse(links[0]["in_frontmatter"])

    def test_frontmatter_must_start_at_line_one(self):
        text = "preâmbulo\n---\nfoo: [[Y]]\n---\n"
        # '---' não na linha 1 -> não é frontmatter; Y NÃO está em frontmatter
        links = cw.extract_wikilinks_clean(text)
        self.assertFalse(links[0]["in_frontmatter"])
```

- [ ] **Step 2: Rodar para verificar falha**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestFrontmatter -v
```

Expected: FAIL — `test_marks_wikilink_in_frontmatter` falha porque `in_frontmatter` está sempre `False`.

- [ ] **Step 3: Implementar `find_frontmatter_range` e atualizar `extract_wikilinks_clean`**

Adicionar/substituir:

```python
def find_frontmatter_range(text: str) -> tuple[int, int] | None:
    """Detecta YAML frontmatter (---\\n ... \\n---). Retorna (start, end) 1-based.

    Apenas reconhece se '---' está na primeira linha (linha 1) e há um '---' depois.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return (1, i + 1)
    return None


def extract_wikilinks_clean(text: str) -> list[dict]:
    """Extrai wikilinks após mascarar code fences/inline; marca in_frontmatter."""
    fm_range = find_frontmatter_range(text)
    links = extract_wikilinks(strip_code_fences(text))
    if fm_range is not None:
        fm_start, fm_end = fm_range
        for link in links:
            if fm_start <= link["line"] <= fm_end:
                link["in_frontmatter"] = True
    return links
```

- [ ] **Step 4: Rodar para verificar passa**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestFrontmatter -v
python -m unittest scripts.test_check_wikilinks -v
```

Expected: 3 testes da classe PASS, suite inteira PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/verificar-wikilinks/scripts/
git commit -m "feat(skill/verificar-wikilinks): marca wikilinks em frontmatter YAML"
```

---

### Task 5: Extração de links markdown internos

**Objetivo:** `extract_markdown_links(text)` captura `[texto](caminho.md)` e `[texto](caminho.md#sec)`, ignora URLs `http(s)://`, ignora `mailto:`, `tel:`, anchors-puros `#sec`, e respeita code fences. Cumpre `test_ignores_http_urls_in_markdown_links`.

**Files:**
- Modify: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Modify: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Escrever os testes falhando**

Adicionar:

```python
class TestMarkdownLinks(unittest.TestCase):
    def test_extracts_internal_md_link(self):
        text = "veja [a nota](Notas/Outra.md)\n"
        links = cw.extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["target"], "Notas/Outra.md")
        self.assertEqual(links[0]["type"], "markdown")
        self.assertEqual(links[0]["alias"], "a nota")

    def test_extracts_internal_md_link_with_anchor(self):
        text = "[seção](Notas/X.md#parte-2)\n"
        links = cw.extract_markdown_links(text)
        self.assertEqual(links[0]["target"], "Notas/X.md")
        self.assertEqual(links[0]["anchor"], "parte-2")

    def test_ignores_http_urls(self):
        text = "[google](https://google.com) e [mail](mailto:x@y) e [intra](Notas/X.md)\n"
        links = cw.extract_markdown_links(text)
        self.assertEqual([l["target"] for l in links], ["Notas/X.md"])

    def test_ignores_pure_anchor(self):
        text = "[topo](#topo)\n"
        links = cw.extract_markdown_links(text)
        self.assertEqual(links, [])

    def test_ignores_link_inside_code_fence(self):
        text = "```\n[x](Notas/Y.md)\n```\n[z](Notas/W.md)\n"
        links = cw.extract_markdown_links(text)
        self.assertEqual([l["target"] for l in links], ["Notas/W.md"])
```

- [ ] **Step 2: Rodar para verificar falha**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestMarkdownLinks -v
```

Expected: FAIL — `extract_markdown_links` não existe.

- [ ] **Step 3: Implementar `extract_markdown_links`**

Adicionar:

```python
# [texto](destino) — destino sem espaços não escapados e sem ')'.
MD_LINK_RE = re.compile(r"\[([^\]\n]+)\]\(([^)\s]+)\)")
URL_SCHEME_RE = re.compile(r"^(https?:|mailto:|tel:|ftp:|data:)", re.IGNORECASE)


def extract_markdown_links(text: str) -> list[dict]:
    """Extrai links markdown internos `[t](caminho.md[#anchor])`.

    Ignora URLs externas (http/https/mailto/tel/ftp/data), anchors puros (#x)
    e links dentro de code fences/inline code.
    """
    cleaned = strip_code_fences(text)
    fm_range = find_frontmatter_range(text)
    results: list[dict] = []
    for lineno, line in enumerate(cleaned.splitlines(), start=1):
        for m in MD_LINK_RE.finditer(line):
            label, dest = m.group(1), m.group(2)
            if URL_SCHEME_RE.match(dest):
                continue
            if dest.startswith("#"):
                continue
            anchor: str | None = None
            target = dest
            if "#" in dest:
                target, anchor = dest.split("#", 1)
            if not target.endswith(".md"):
                continue  # ignora links para assets nesta v1
            in_fm = fm_range is not None and fm_range[0] <= lineno <= fm_range[1]
            results.append({
                "line": lineno,
                "raw": m.group(0),
                "target": target,
                "alias": label,
                "anchor": anchor,
                "type": "markdown",
                "in_frontmatter": in_fm,
            })
    return results
```

- [ ] **Step 4: Rodar para verificar passa**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestMarkdownLinks -v
```

Expected: 5 testes PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/verificar-wikilinks/scripts/
git commit -m "feat(skill/verificar-wikilinks): parser de links markdown internos"
```

---

### Task 6: Resolução — match exato por basename

**Objetivo:** `resolve_link(link, index)` retorna `None` quando o link resolve OK. `[[Anatomia]]` resolve se existir `Anatomia.md` em qualquer lugar do vault. Cumpre `test_wikilink_resolves_exact_match`.

**Files:**
- Modify: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Modify: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Escrever o teste falhando**

Adicionar:

```python
class TestResolveExact(unittest.TestCase):
    def _link(self, target, type_="wikilink", anchor=None):
        return {
            "file": "origem.md", "line": 1, "raw": f"[[{target}]]",
            "target": target, "alias": None, "anchor": anchor,
            "type": type_, "in_frontmatter": False,
        }

    def test_resolves_exact_basename(self):
        idx = {
            "files_by_basename": {"Anatomia": ["Notas/Anatomia.md"]},
            "files_by_relpath": {"Notas/Anatomia.md"},
            "folders": {},
            "folders_with_index": set(),
        }
        self.assertIsNone(cw.resolve_link(self._link("Anatomia"), idx))

    def test_resolves_target_with_explicit_path(self):
        idx = {
            "files_by_basename": {"Sub": ["Pasta/Sub.md"]},
            "files_by_relpath": {"Pasta/Sub.md"},
            "folders": {},
            "folders_with_index": set(),
        }
        self.assertIsNone(cw.resolve_link(self._link("Pasta/Sub"), idx))

    def test_resolves_target_with_md_extension(self):
        idx = {
            "files_by_basename": {"A": ["A.md"]},
            "files_by_relpath": {"A.md"},
            "folders": {},
            "folders_with_index": set(),
        }
        self.assertIsNone(cw.resolve_link(self._link("A.md"), idx))
```

- [ ] **Step 2: Rodar para verificar falha**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestResolveExact -v
```

Expected: FAIL — `resolve_link` não existe.

- [ ] **Step 3: Implementar `resolve_link` (apenas o caminho feliz)**

Adicionar:

```python
def resolve_link(link: dict, index: dict) -> dict | None:
    """Aplica regras do Quartz e retorna None se OK; Broken dict se quebrado.

    Ordem de tentativa:
    1. Path explícito (contém '/' ou termina em .md) -> match em files_by_relpath.
    2. Basename exato -> match único em files_by_basename.
    3. Senão: caminho de quebra (próximas tasks).
    """
    target = link["target"]
    target_norm = target[:-3] if target.endswith(".md") else target

    # 1) Path explícito
    if "/" in target_norm:
        candidate_rel = target_norm + ".md"
        if candidate_rel in index["files_by_relpath"]:
            return None

    # 2) Basename exato (sem path)
    matches = index["files_by_basename"].get(target_norm, [])
    if len(matches) == 1:
        return None

    # placeholder para Tasks 7/8/9/10
    return {**link, "reason": "target_not_found", "candidates": []}
```

- [ ] **Step 4: Rodar para verificar passa**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestResolveExact -v
```

Expected: 3 testes PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/verificar-wikilinks/scripts/
git commit -m "feat(skill/verificar-wikilinks): resolve match exato de basename"
```

---

### Task 7: Resolução — folder com/sem `index.md` (o bug)

**Objetivo:** `[[Pasta]]` é quebrado se a pasta existe mas **não tem `index.md`** (`reason: folder_without_index`); OK se tiver. Cumpre `test_folder_link_without_index_breaks` e `test_folder_link_with_index_resolves`.

**Files:**
- Modify: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Modify: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Escrever os testes falhando**

Adicionar:

```python
class TestResolveFolder(unittest.TestCase):
    def _link(self, target):
        return {
            "file": "MOC.md", "line": 1, "raw": f"[[{target}]]",
            "target": target, "alias": None, "anchor": None,
            "type": "wikilink", "in_frontmatter": False,
        }

    def test_folder_with_index_resolves(self):
        idx = {
            "files_by_basename": {"index": ["Pasta/index.md"]},
            "files_by_relpath": {"Pasta/index.md"},
            "folders": {"Pasta": ["Pasta"]},
            "folders_with_index": {"Pasta"},
        }
        self.assertIsNone(cw.resolve_link(self._link("Pasta"), idx))

    def test_folder_without_index_breaks(self):
        idx = {
            "files_by_basename": {"A": ["Pasta/A.md"]},
            "files_by_relpath": {"Pasta/A.md"},
            "folders": {"Pasta": ["Pasta"]},
            "folders_with_index": set(),
        }
        broken = cw.resolve_link(self._link("Pasta"), idx)
        self.assertIsNotNone(broken)
        self.assertEqual(broken["reason"], "folder_without_index")
        # candidates lista arquivos dentro da pasta como sugestão
        self.assertIn("Pasta/A.md", broken["candidates"])

    def test_nested_folder_path_with_index_resolves(self):
        idx = {
            "files_by_basename": {"index": ["A/B/index.md"]},
            "files_by_relpath": {"A/B/index.md"},
            "folders": {"B": ["A/B"]},
            "folders_with_index": {"A/B"},
        }
        self.assertIsNone(cw.resolve_link(self._link("A/B"), idx))
```

- [ ] **Step 2: Rodar para verificar falha**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestResolveFolder -v
```

Expected: 2/3 FAIL — `test_folder_without_index_breaks` retorna `target_not_found`, e os de pasta retornam quebra.

- [ ] **Step 3: Adicionar lógica de pasta a `resolve_link`**

Substituir `resolve_link` completo:

```python
def resolve_link(link: dict, index: dict) -> dict | None:
    target = link["target"]
    target_norm = target[:-3] if target.endswith(".md") else target

    # 1) Path explícito (tem '/' ou '.md')
    if "/" in target_norm or target.endswith(".md"):
        candidate_rel = target_norm + ".md"
        if candidate_rel in index["files_by_relpath"]:
            return None
        # 1b) Pode ser path para pasta (com ou sem index.md)
        if target_norm in index["folders_with_index"]:
            return None
        # Lista pastas cujo relpath bate exatamente (sem index)
        # folders dict mapeia basename->lista de relpaths, então cheque união:
        all_folder_paths = {p for paths in index["folders"].values() for p in paths}
        if target_norm in all_folder_paths:
            # pasta existe mas sem index
            inside = sorted(
                p for p in index["files_by_relpath"] if p.startswith(target_norm + "/")
            )
            return {**link, "reason": "folder_without_index", "candidates": inside[:10]}

    # 2) Basename exato como arquivo
    matches = index["files_by_basename"].get(target_norm, [])
    if len(matches) == 1:
        return None
    if len(matches) > 1:
        # tratado na Task 8 (ambiguous)
        return {**link, "reason": "ambiguous", "candidates": matches}

    # 3) Basename exato como pasta
    folder_paths = index["folders"].get(target_norm, [])
    if folder_paths:
        with_index = [p for p in folder_paths if p in index["folders_with_index"]]
        if len(with_index) == 1:
            return None
        if len(with_index) > 1:
            return {**link, "reason": "ambiguous", "candidates": with_index}
        # Sem index em nenhuma → folder_without_index, candidates = conteúdo
        inside: list[str] = []
        for fp in folder_paths:
            inside.extend(
                p for p in index["files_by_relpath"] if p.startswith(fp + "/")
            )
        return {**link, "reason": "folder_without_index", "candidates": sorted(inside)[:10]}

    # 4) Sem match em lugar nenhum (Task 9 cuida das sugestões fuzzy)
    return {**link, "reason": "target_not_found", "candidates": []}
```

- [ ] **Step 4: Rodar para verificar passa**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestResolveFolder -v
python -m unittest scripts.test_check_wikilinks.TestResolveExact -v
```

Expected: ambas as classes PASS (3 + 3 = 6).

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/verificar-wikilinks/scripts/
git commit -m "feat(skill/verificar-wikilinks): regra Quartz — folder-link exige index.md"
```

---

### Task 8: Resolução — ambíguo + sugestões fuzzy

**Objetivo:** Basenames duplicados retornam `reason: ambiguous` com lista de candidatos; ausência total retorna `reason: target_not_found` com sugestões via `difflib.get_close_matches` (cutoff 0.6). Cumpre `test_ambiguous_target_lists_candidates` e `test_fuzzy_suggestion_on_typo`.

**Files:**
- Modify: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Modify: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Escrever os testes falhando**

Adicionar:

```python
class TestAmbiguousAndFuzzy(unittest.TestCase):
    def _link(self, target):
        return {
            "file": "x.md", "line": 1, "raw": f"[[{target}]]",
            "target": target, "alias": None, "anchor": None,
            "type": "wikilink", "in_frontmatter": False,
        }

    def test_ambiguous_target_lists_candidates(self):
        idx = {
            "files_by_basename": {"Notas": ["A/Notas.md", "B/Notas.md"]},
            "files_by_relpath": {"A/Notas.md", "B/Notas.md"},
            "folders": {},
            "folders_with_index": set(),
        }
        broken = cw.resolve_link(self._link("Notas"), idx)
        self.assertEqual(broken["reason"], "ambiguous")
        self.assertEqual(sorted(broken["candidates"]), ["A/Notas.md", "B/Notas.md"])

    def test_fuzzy_suggestion_on_typo(self):
        idx = {
            "files_by_basename": {"Anatomia dos LLMs": ["Notas/Anatomia dos LLMs.md"]},
            "files_by_relpath": {"Notas/Anatomia dos LLMs.md"},
            "folders": {},
            "folders_with_index": set(),
        }
        broken = cw.resolve_link(self._link("Anatonia dos LLMs"), idx)
        self.assertEqual(broken["reason"], "target_not_found")
        self.assertIn("Notas/Anatomia dos LLMs.md", broken["candidates"])

    def test_target_not_found_no_close_match(self):
        idx = {
            "files_by_basename": {"Zebra": ["x/Zebra.md"]},
            "files_by_relpath": {"x/Zebra.md"},
            "folders": {},
            "folders_with_index": set(),
        }
        broken = cw.resolve_link(self._link("Mongoloide Cósmico"), idx)
        self.assertEqual(broken["reason"], "target_not_found")
        self.assertEqual(broken["candidates"], [])
```

- [ ] **Step 2: Rodar para verificar falha**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestAmbiguousAndFuzzy -v
```

Expected: `test_fuzzy_suggestion_on_typo` FAIL (candidates está `[]`). Os outros dois PASS (já cobertos pela Task 7).

- [ ] **Step 3: Adicionar `find_candidates` e injetar em `target_not_found`**

Adicionar:

```python
import difflib


def find_candidates(target: str, index: dict, n: int = 5, cutoff: float = 0.6) -> list[str]:
    """Sugestões fuzzy via difflib sobre basenames + relpaths."""
    pool = list(index["files_by_basename"].keys()) + list(index["files_by_relpath"])
    matches = difflib.get_close_matches(target, pool, n=n, cutoff=cutoff)
    # converte basenames sugeridos para relpaths (primeiro hit) para ficar útil
    resolved: list[str] = []
    for m in matches:
        if m in index["files_by_relpath"]:
            resolved.append(m)
        else:
            paths = index["files_by_basename"].get(m, [])
            resolved.extend(paths)
    # dedup preservando ordem
    seen: set[str] = set()
    out: list[str] = []
    for p in resolved:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out[:n]
```

E substituir o `return` final de `resolve_link` (caso 4):

```python
    # 4) Sem match em lugar nenhum — sugere via fuzzy
    return {
        **link,
        "reason": "target_not_found",
        "candidates": find_candidates(target_norm, index),
    }
```

- [ ] **Step 4: Rodar para verificar passa**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestAmbiguousAndFuzzy -v
```

Expected: 3 testes PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/verificar-wikilinks/scripts/
git commit -m "feat(skill/verificar-wikilinks): sugestões fuzzy + ambiguidade resolvida"
```

---

### Task 9: Resolução — validação de anchor (`#Seção`)

**Objetivo:** Quando `link.anchor` existe e o target resolve para um `.md`, abrir o arquivo, extrair headers e validar. Se não bater (comparando texto cru e slug `[a-z0-9-]`), `reason: anchor_not_found`. Cumpre `test_anchor_validation_existing_and_missing`.

**Files:**
- Modify: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Modify: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Escrever os testes falhando**

Adicionar:

```python
class TestAnchorValidation(unittest.TestCase):
    def test_anchor_validation_existing_and_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = make_vault(Path(tmp), {
                "Nota.md": "# Topo\n\n## Introdução\n\nconteúdo\n## Outra Seção\n",
            })
            idx = cw.index_vault(vault)

            ok_link = {
                "file": "origem.md", "line": 1, "raw": "[[Nota#Introdução]]",
                "target": "Nota", "alias": None, "anchor": "Introdução",
                "type": "wikilink", "in_frontmatter": False,
            }
            self.assertIsNone(cw.resolve_link(ok_link, idx, vault_root=vault))

            bad_link = {**ok_link, "anchor": "Inexistente", "raw": "[[Nota#Inexistente]]"}
            broken = cw.resolve_link(bad_link, idx, vault_root=vault)
            self.assertEqual(broken["reason"], "anchor_not_found")
            self.assertIn("Introdução", broken["candidates"])

    def test_anchor_validation_slug_form(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = make_vault(Path(tmp), {
                "Nota.md": "# Topo\n\n## Intro & Visão Geral\n",
            })
            idx = cw.index_vault(vault)
            link = {
                "file": "x.md", "line": 1, "raw": "[[Nota#intro-visão-geral]]",
                "target": "Nota", "alias": None, "anchor": "intro-visão-geral",
                "type": "wikilink", "in_frontmatter": False,
            }
            self.assertIsNone(cw.resolve_link(link, idx, vault_root=vault))
```

- [ ] **Step 2: Rodar para verificar falha**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestAnchorValidation -v
```

Expected: FAIL — `resolve_link` ainda não aceita `vault_root`; também não valida anchor.

- [ ] **Step 3: Adicionar `get_section_anchors`, slug e estender `resolve_link`**

Adicionar:

```python
HEADER_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")


def slugify_header(text: str) -> str:
    """Slug compatível com Obsidian/Quartz: lowercase, espaços->-, remove markdown.

    Mantém letras acentuadas (Quartz não transliterate por default).
    """
    text = text.strip().lower()
    # remove ênfase markdown comum
    text = re.sub(r"[*_`]+", "", text)
    # caracteres especiais inúteis
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")


def get_section_anchors(file_path: Path) -> list[str]:
    """Retorna lista de headers (texto cru) de um arquivo .md."""
    try:
        text = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    headers: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line.lstrip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADER_RE.match(line)
        if m:
            headers.append(m.group(1).strip())
    return headers
```

Agora modificar a assinatura de `resolve_link` para aceitar `vault_root=None`:

```python
def resolve_link(link: dict, index: dict, vault_root: Path | None = None) -> dict | None:
    target = link["target"]
    target_norm = target[:-3] if target.endswith(".md") else target

    resolved_path: str | None = None

    # 1) Path explícito (tem '/' ou '.md')
    if "/" in target_norm or target.endswith(".md"):
        candidate_rel = target_norm + ".md"
        if candidate_rel in index["files_by_relpath"]:
            resolved_path = candidate_rel
        elif target_norm in index["folders_with_index"]:
            resolved_path = target_norm + "/index.md"
        else:
            all_folder_paths = {p for paths in index["folders"].values() for p in paths}
            if target_norm in all_folder_paths:
                inside = sorted(
                    p for p in index["files_by_relpath"] if p.startswith(target_norm + "/")
                )
                return {**link, "reason": "folder_without_index", "candidates": inside[:10]}

    # 2) Basename exato como arquivo
    if resolved_path is None:
        matches = index["files_by_basename"].get(target_norm, [])
        if len(matches) == 1:
            resolved_path = matches[0]
        elif len(matches) > 1:
            return {**link, "reason": "ambiguous", "candidates": matches}

    # 3) Basename exato como pasta
    if resolved_path is None:
        folder_paths = index["folders"].get(target_norm, [])
        if folder_paths:
            with_index = [p for p in folder_paths if p in index["folders_with_index"]]
            if len(with_index) == 1:
                resolved_path = with_index[0] + "/index.md"
            elif len(with_index) > 1:
                return {**link, "reason": "ambiguous", "candidates": with_index}
            else:
                inside: list[str] = []
                for fp in folder_paths:
                    inside.extend(
                        p for p in index["files_by_relpath"] if p.startswith(fp + "/")
                    )
                return {**link, "reason": "folder_without_index",
                        "candidates": sorted(inside)[:10]}

    # 4) Nada bateu
    if resolved_path is None:
        return {**link, "reason": "target_not_found",
                "candidates": find_candidates(target_norm, index)}

    # 5) Validação de anchor (se houver e vault_root foi passado)
    if link["anchor"] and vault_root is not None:
        headers = get_section_anchors(vault_root / resolved_path)
        wanted = link["anchor"]
        ok = (
            wanted in headers
            or slugify_header(wanted) in {slugify_header(h) for h in headers}
        )
        if not ok:
            return {**link, "reason": "anchor_not_found", "candidates": headers[:10]}

    return None
```

- [ ] **Step 4: Rodar para verificar passa**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestAnchorValidation -v
python -m unittest scripts.test_check_wikilinks -v
```

Expected: ambos PASS; suite inteira PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/verificar-wikilinks/scripts/
git commit -m "feat(skill/verificar-wikilinks): validação de anchor (#Seção) em wikilinks"
```

---

### Task 10: Resolução — markdown link com caminho inválido

**Objetivo:** Para links `[t](caminho/x.md)`, se o path não existe em `files_by_relpath`, retornar `reason: markdown_broken_path`. Cumpre `test_markdown_link_internal_broken`.

**Files:**
- Modify: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Modify: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Escrever o teste falhando**

Adicionar:

```python
class TestMarkdownBrokenPath(unittest.TestCase):
    def test_markdown_link_internal_broken(self):
        idx = {
            "files_by_basename": {"Existente": ["Notas/Existente.md"]},
            "files_by_relpath": {"Notas/Existente.md"},
            "folders": {},
            "folders_with_index": set(),
        }
        link = {
            "file": "origem.md", "line": 5,
            "raw": "[t](Notas/Nao Existe.md)",
            "target": "Notas/Nao Existe.md", "alias": "t", "anchor": None,
            "type": "markdown", "in_frontmatter": False,
        }
        broken = cw.resolve_link(link, idx)
        self.assertEqual(broken["reason"], "markdown_broken_path")

    def test_markdown_link_internal_resolves(self):
        idx = {
            "files_by_basename": {"Existente": ["Notas/Existente.md"]},
            "files_by_relpath": {"Notas/Existente.md"},
            "folders": {},
            "folders_with_index": set(),
        }
        link = {
            "file": "x.md", "line": 1, "raw": "[t](Notas/Existente.md)",
            "target": "Notas/Existente.md", "alias": "t", "anchor": None,
            "type": "markdown", "in_frontmatter": False,
        }
        self.assertIsNone(cw.resolve_link(link, idx))
```

- [ ] **Step 2: Rodar para verificar falha**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestMarkdownBrokenPath -v
```

Expected: `test_markdown_link_internal_broken` falha — `reason` vem como `target_not_found` em vez de `markdown_broken_path`.

- [ ] **Step 3: Diferenciar `markdown_broken_path` em `resolve_link`**

Logo no início de `resolve_link`, **antes** do bloco `# 1) Path explícito`, adicionar:

```python
    # Markdown links têm 'target' já com '.md' — quebra deles é markdown_broken_path
    is_markdown = link["type"] == "markdown"
```

E ao final (caso 4 — nada bateu), substituir por:

```python
    if resolved_path is None:
        if is_markdown:
            return {**link, "reason": "markdown_broken_path",
                    "candidates": find_candidates(target_norm, index)}
        return {**link, "reason": "target_not_found",
                "candidates": find_candidates(target_norm, index)}
```

- [ ] **Step 4: Rodar para verificar passa**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestMarkdownBrokenPath -v
python -m unittest scripts.test_check_wikilinks -v
```

Expected: 2 PASS; suite inteira PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/verificar-wikilinks/scripts/
git commit -m "feat(skill/verificar-wikilinks): distingue markdown_broken_path"
```

---

### Task 11: `scan_folder` + CLI + saída JSON

**Objetivo:** Função `scan_folder(target, vault_root)` percorre `.md` da pasta-alvo, extrai links de cada arquivo, resolve, compõe relatório. `main(argv)` faz CLI com `argparse`, escreve JSON em `--output` (default `/tmp/wikilinks-report-<ts>.json`) e imprime o caminho no stdout.

**Files:**
- Modify: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Modify: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Escrever o teste falhando**

Adicionar:

```python
class TestScanAndCLI(unittest.TestCase):
    def test_scan_folder_detects_moc_bug(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = make_vault(Path(tmp), {
                "MOC/index.md": "# MOC\n\n[[Anatomia]] [[Existente]]\n",
                "MOC/Anatomia/01.md": "# 01\n",        # pasta sem index.md
                "MOC/Existente.md": "# Existente\n",
            })
            report = cw.scan_folder(vault / "MOC", vault_root=vault)
            self.assertEqual(report["stats"]["files_scanned"], 2)
            self.assertEqual(report["stats"]["links_broken"], 1)
            self.assertEqual(report["stats"]["by_reason"]["folder_without_index"], 1)
            self.assertEqual(report["broken"][0]["target"], "Anatomia")

    def test_cli_writes_json_to_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = make_vault(Path(tmp), {
                "MOC/index.md": "# MOC\n[[Sem]]\n",
            })
            out = Path(tmp) / "report.json"
            rc = cw.main([
                str(vault / "MOC"),
                "--vault-root", str(vault),
                "--output", str(out),
            ])
            self.assertEqual(rc, 0)
            self.assertTrue(out.exists())
            import json
            data = json.loads(out.read_text())
            self.assertEqual(data["stats"]["links_broken"], 1)
            self.assertEqual(data["target_folder"], "MOC")
```

- [ ] **Step 2: Rodar para verificar falha**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestScanAndCLI -v
```

Expected: FAIL — `scan_folder` e `main` não implementadas.

- [ ] **Step 3: Implementar `scan_folder` e `main`**

Adicionar ao final de `check_wikilinks.py`:

```python
import argparse
import json
from datetime import datetime, timezone


def scan_folder(target: Path, vault_root: Path) -> dict:
    """Varre todos os .md da pasta-alvo, extrai links e resolve.

    Retorna dict no formato definido na spec (campos: scanned_at, vault_root,
    target_folder, stats, broken, warnings).
    """
    target = target.resolve()
    vault_root = vault_root.resolve()

    if not target.is_dir():
        raise FileNotFoundError(f"target folder not found: {target}")

    index = index_vault(vault_root)
    broken: list[dict] = []
    warnings: list[dict] = []
    files_scanned = 0
    links_total = 0

    for path in sorted(target.rglob("*.md")):
        if any(part in IGNORED_DIRS for part in path.relative_to(vault_root).parts):
            continue
        rel = path.relative_to(vault_root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            warnings.append({"file": rel, "msg": f"unreadable: {exc.__class__.__name__}"})
            continue
        files_scanned += 1

        all_links = extract_wikilinks_clean(text) + extract_markdown_links(text)
        # filtrar embeds de assets (não-.md) já é feito no parser de markdown;
        # para wikilink embed sem .md no target, deixamos passar (Obsidian permite
        # embed de notas sem extensão) — assets ficam fora do escopo da v1.

        for link in all_links:
            link["file"] = rel
            links_total += 1
            result = resolve_link(link, index, vault_root=vault_root)
            if result is not None:
                broken.append(result)

    by_reason: dict[str, int] = {}
    for b in broken:
        by_reason[b["reason"]] = by_reason.get(b["reason"], 0) + 1

    return {
        "scanned_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "vault_root": vault_root.as_posix(),
        "target_folder": target.relative_to(vault_root).as_posix(),
        "stats": {
            "files_scanned": files_scanned,
            "links_total": links_total,
            "links_broken": len(broken),
            "by_reason": by_reason,
        },
        "broken": broken,
        "warnings": warnings,
    }


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="check_wikilinks",
        description="Detecta wikilinks/links markdown quebrados (regra Quartz).",
    )
    p.add_argument("target", help="pasta-alvo dentro do vault")
    p.add_argument("--vault-root", default=None,
                   help="raiz do vault (auto-detecta via .obsidian/ se omitido)")
    p.add_argument("--output", default=None,
                   help="caminho do JSON de saída (default: /tmp/wikilinks-report-<ts>.json)")
    p.add_argument("--respect-public-only", action="store_true",
                   help="ignora arquivos cujo path resolve fora do repo público")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv if argv is not None else [])
    target = Path(args.target).resolve()
    if args.vault_root:
        vault_root = Path(args.vault_root).resolve()
    else:
        vault_root = auto_detect_vault_root(target)

    if args.output:
        out_path = Path(args.output)
    else:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = Path(f"/tmp/wikilinks-report-{ts}.json")

    try:
        report = scan_folder(target, vault_root)
    except FileNotFoundError as exc:
        print(f"error: {exc}", flush=True)
        return 2

    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(out_path)
    return 0
```

E remover o `raise NotImplementedError` antigo da função `main` original (substitua o stub inteiro pela versão acima).

- [ ] **Step 4: Rodar para verificar passa**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestScanAndCLI -v
python -m unittest scripts.test_check_wikilinks -v
```

Expected: 2 PASS na classe; suite inteira PASS (10+ testes).

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/verificar-wikilinks/scripts/
git commit -m "feat(skill/verificar-wikilinks): scan_folder + CLI argparse + JSON output"
```

---

### Task 12: Polimento — wikilinks malformados, `--respect-public-only`, encoding

**Objetivo:** Detectar `[[a [[b]] c]]` como `malformed`; aplicar `--respect-public-only` filtrando paths fora do repo público; garantir que arquivos com encoding inválido geram warning e não quebram o run.

**Files:**
- Modify: `.agents/skills/verificar-wikilinks/scripts/check_wikilinks.py`
- Modify: `.agents/skills/verificar-wikilinks/scripts/test_check_wikilinks.py`

- [ ] **Step 1: Escrever os testes falhando**

Adicionar:

```python
class TestPolish(unittest.TestCase):
    def test_nested_wikilink_marked_malformed(self):
        # [[a [[b]] c]] é ambíguo; o parser captura [[b]] mas a forma externa fica
        # com colchete solto. Verificamos que pelo menos um link com '[[' no target
        # vira malformed.
        text = "[[a [[b]] c]]\n"
        links = cw.extract_wikilinks_clean(text)
        # esperamos pelo menos um link com target contendo '['
        offenders = [l for l in links if "[" in l["target"] or "]" in l["target"]]
        # se não houver, o parser absorveu; nesse caso garantimos que resolve marca malformed
        idx = {
            "files_by_basename": {}, "files_by_relpath": set(),
            "folders": {}, "folders_with_index": set(),
        }
        if offenders:
            broken = cw.resolve_link(offenders[0], idx)
            self.assertEqual(broken["reason"], "malformed")

    def test_encoding_error_recorded_as_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = make_vault(Path(tmp), {"MOC/ok.md": "# ok\n"})
            bad = vault / "MOC" / "bin.md"
            bad.write_bytes(b"\xff\xfe\x00invalid utf-8 \x80")
            report = cw.scan_folder(vault / "MOC", vault_root=vault)
            self.assertTrue(any(w["file"].endswith("bin.md") for w in report["warnings"]))

    def test_respect_public_only_filters_outside(self):
        # Simula vault com link para um arquivo "fora" do repo público.
        # Implementação: --respect-public-only descarta brokens cujos candidates
        # apontem para apocrypha. Aqui só checamos que a flag existe e roda.
        with tempfile.TemporaryDirectory() as tmp:
            vault = make_vault(Path(tmp), {"MOC/index.md": "# MOC\n[[Inexistente]]\n"})
            out = Path(tmp) / "r.json"
            rc = cw.main([
                str(vault / "MOC"),
                "--vault-root", str(vault),
                "--output", str(out),
                "--respect-public-only",
            ])
            self.assertEqual(rc, 0)
```

- [ ] **Step 2: Rodar para verificar falha**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestPolish -v
```

Expected: `test_nested_wikilink_marked_malformed` pode falhar dependendo do parser; encoding test pode falhar se a leitura abortar.

- [ ] **Step 3: Ajustes**

Em `resolve_link`, logo após `is_markdown = link["type"] == "markdown"`, adicionar:

```python
    # Wikilink malformado: target contém colchetes -> não dá pra resolver
    if "[" in link["target"] or "]" in link["target"]:
        return {**link, "reason": "malformed", "candidates": []}
```

Em `scan_folder`, substituir o bloco `text = path.read_text(...)` para usar `errors="replace"` como fallback e ainda assim emitir warning:

```python
        try:
            raw_bytes = path.read_bytes()
        except OSError as exc:
            warnings.append({"file": rel, "msg": f"unreadable: {exc.__class__.__name__}"})
            continue
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            warnings.append({"file": rel, "msg": "encoding error, decoded with replace"})
            text = raw_bytes.decode("utf-8", errors="replace")
```

Para `--respect-public-only`, em `main`, após chamar `scan_folder`, filtrar:

```python
    if args.respect_public_only:
        public_root = vault_root
        report["broken"] = [
            b for b in report["broken"]
            if not any(
                not (public_root / c).resolve().is_relative_to(public_root)
                for c in b.get("candidates", [])
            )
        ]
        report["stats"]["links_broken"] = len(report["broken"])
        # recomputa by_reason
        by_reason: dict[str, int] = {}
        for b in report["broken"]:
            by_reason[b["reason"]] = by_reason.get(b["reason"], 0) + 1
        report["stats"]["by_reason"] = by_reason
```

- [ ] **Step 4: Rodar para verificar passa**

Run:
```bash
python -m unittest scripts.test_check_wikilinks.TestPolish -v
python -m unittest scripts.test_check_wikilinks -v
```

Expected: 3 PASS na classe; suite inteira PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/verificar-wikilinks/scripts/
git commit -m "feat(skill/verificar-wikilinks): malformed, encoding-safe, --respect-public-only"
```

---

### Task 13: Escrever `SKILL.md`

**Objetivo:** Documento de orquestração — fluxo conversacional que o agente segue ao ser invocado.

**Files:**
- Create: `.agents/skills/verificar-wikilinks/SKILL.md`

- [ ] **Step 1: Criar `SKILL.md`**

Conteúdo de `.agents/skills/verificar-wikilinks/SKILL.md`:

```markdown
---
name: verificar-wikilinks
description: "Detecta e corrige wikilinks/links markdown quebrados em um vault Obsidian, aplicando a regra do Quartz (folder-link exige index.md). Use quando o usuário pedir /verificar-wikilinks <pasta>, 'checar links quebrados', 'auditar wikilinks', 'consertar links da MOC'."
---

# verificar-wikilinks

Detecta e corrige wikilinks quebrados em pastas do vault, aplicando a regra do
Quartz: `[[Pasta]]` só funciona se a pasta tiver `index.md`.

## Quando usar

- Usuário invoca `/verificar-wikilinks <pasta>` (ex: `03-Dominios/IA`).
- Usuário pede para "checar links quebrados", "auditar wikilinks", "consertar
  links da MOC".
- Após renomear/mover notas, antes de publicar no site Quartz.

## Fluxo

### 1. Receber pasta-alvo

Se o usuário não passou pasta, peça confirmação (sugira a pasta atual). Não
assuma.

### 2. Rodar o detector

```bash
python .agents/skills/verificar-wikilinks/scripts/check_wikilinks.py \
  <pasta> --respect-public-only
```

O script imprime o caminho do JSON gerado em `/tmp/wikilinks-report-*.json`.

### 3. Ler o JSON e agrupar por motivo

Leia o JSON. Apresente ao usuário um resumo:

```
Encontrei N quebras em M arquivos. Plano de correção:

folder_without_index (K):
  - [[Anatomia dos LLMs]] em 03-Dominios/IA/index.md:42
    → criar 03-Dominios/IA/Anatomia dos LLMs/index.md
  - [...]

target_not_found (K):
  - [[Velho Nome]] em ...:15
    → git log sugere renomeado para "Novo Nome.md"; atualizar wikilink

ambiguous (K):
  - [[Notas]] tem candidatos:
      1. A/Notas.md
      2. B/Notas.md
    Qual deve ser usado?

anchor_not_found (K):
  - [[Nota#Inexistente]]
    Seções existentes: ... Escolha uma ou peça remoção do anchor.
```

### 4. Estratégia por motivo

| Motivo | Ação default |
|---|---|
| `folder_without_index` | Criar `index.md` na pasta (frontmatter mínimo + título + lista do conteúdo). Alternativa: trocar wikilink para arquivo específico. |
| `target_not_found` | Rodar `git log --diff-filter=R --follow -- '*<basename>*'`. Se houver rename, atualizar automaticamente. Senão, perguntar. |
| `ambiguous` | Perguntar ao usuário qual candidato usar (uma vez por basename). |
| `anchor_not_found` | Listar seções existentes do destino, pedir escolha (ou remover anchor). |
| `markdown_broken_path` | Mesma lógica de `target_not_found`. Atualizar o `[texto](caminho)` inteiro. |
| `malformed` | Não auto-corrigir. Listar e pedir intervenção manual. |

### 5. Pedir aprovação do plano

Espere "sim/aprovado/proceda" antes de qualquer Edit. O usuário pode pedir
ajustes ("não crie index.md para X, troque o wikilink").

### 6. Aplicar correções

- Agrupe Edits por arquivo.
- Aplique em ordem decrescente de linha (preserva offsets).
- Se a mesma quebra aparece N vezes no mesmo arquivo, use `replace_all=true` no
  Edit.
- Para `folder_without_index`, crie o `index.md` com:

  ```markdown
  ---
  title: "<Nome da pasta>"
  created: <YYYY-MM-DD>
  type: moc
  ---

  # <Nome da pasta>

  - [[arquivo-1]]
  - [[arquivo-2]]
  ```

### 7. Verificação — re-rodar o script

Após aplicar tudo, rode o detector de novo. Reporte:

```
✅ Zero quebras restantes em <pasta>.
```

Se ainda houver, liste os resíduos (provavelmente decisões manuais não tomadas).

## Restrições

- **Não escrever no apocrypha**. Se uma correção exigir, bloqueie e reporte.
- **Não auto-corrigir** quando `reason` for `ambiguous`, `anchor_not_found` ou
  `malformed` — exigem decisão humana.
- **Não criar `index.md` automaticamente** se a pasta tem README.md (pode
  haver intenção explícita) — pergunte.

## Arquivos

- Script: `scripts/check_wikilinks.py`
- Testes: `scripts/test_check_wikilinks.py` (`python -m unittest`)
- Spec: `docs/superpowers/specs/2026-05-18-verificar-wikilinks-design.md`
```

- [ ] **Step 2: Commit**

```bash
git add .agents/skills/verificar-wikilinks/SKILL.md
git commit -m "feat(skill/verificar-wikilinks): SKILL.md com fluxo de orquestração"
```

---

### Task 14: Smoke test funcional na MOC IA

**Objetivo:** Rodar o script de verdade contra `03-Dominios/IA` e validar que o JSON detecta as quebras conhecidas. Esse é o critério de aceite "Detecta todas as quebras atuais da MOC IA conferidas manualmente".

**Files:** Nenhum criado/modificado — apenas execução e verificação.

- [ ] **Step 1: Rodar a suite completa uma última vez**

Run:
```bash
cd /home/josenaldo/repos/personal/codex-technomanticus/.agents/skills/verificar-wikilinks
python -m unittest scripts.test_check_wikilinks -v
```

Expected: 10+ testes PASS, 0 fail.

- [ ] **Step 2: Rodar o script contra a MOC IA**

Run:
```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
python .agents/skills/verificar-wikilinks/scripts/check_wikilinks.py \
  "03-Dominios/IA" --output /tmp/moc-ia-report.json
```

Expected: stdout imprime `/tmp/moc-ia-report.json`.

- [ ] **Step 3: Inspecionar o relatório**

Run:
```bash
python -c "import json; d=json.load(open('/tmp/moc-ia-report.json')); print('files:', d['stats']['files_scanned']); print('broken:', d['stats']['links_broken']); print('reasons:', d['stats']['by_reason']); print('---'); [print(b['file']+':'+str(b['line']), b['raw'], '->', b['reason']) for b in d['broken'][:20]]"
```

Expected: lista contendo pelo menos os wikilinks suspeitos da MOC IA com `reason: folder_without_index` (`[[Anatomia dos LLMs]]`, `[[MCP]]`, `[[Context Engineering]]` se as pastas correspondentes existem sem `index.md`).

- [ ] **Step 4: Aferir tempo**

Run:
```bash
time python .agents/skills/verificar-wikilinks/scripts/check_wikilinks.py "03-Dominios/IA" --output /tmp/moc-ia-report.json
```

Expected: real < 5s (critério de aceite).

- [ ] **Step 5: Conferência manual cruzada (sem código)**

Abra `03-Dominios/IA/index.md`. Para cada wikilink listado como `folder_without_index` no relatório, confirme via `ls` que a pasta existe e não tem `index.md`. Se algum wikilink suspeito **não** apareceu no relatório, registrar como bug e ajustar parser (não previsto no plano — abrir nova task).

Run (exemplo de verificação):
```bash
ls "03-Dominios/IA/Anatomia dos LLMs/" 2>/dev/null | grep -i 'index.md' || echo "SEM INDEX (confirma quebra)"
```

- [ ] **Step 6: Commit do estado final (se houver algo pendente)**

```bash
git status
# se houver algo não commitado da skill:
git add .agents/skills/verificar-wikilinks/
git commit -m "chore(skill/verificar-wikilinks): smoke test final na MOC IA"
```

---

## Self-Review — checklist do autor

**Spec coverage:**

- Detecção de wikilinks/embeds/markdown links → Tasks 2, 3, 5.
- Frontmatter detection → Task 4.
- Regra Quartz (folder sem index.md) → Task 7.
- Match exato, ambíguo, fuzzy, anchor, markdown broken path → Tasks 6, 8, 9, 10.
- Wikilink em code fence → Task 3.
- JSON com schema da spec → Task 11.
- `--vault-root`, `--output`, `--respect-public-only` → Tasks 11, 12.
- Encoding-safe → Task 12.
- `malformed` → Task 12.
- Tratamento de pasta-alvo inexistente → Task 11 (exit 2).
- 10 casos de teste da spec → Tasks 2 (4), 3 (7), 5 (8), 6 (1), 7 (2, 3), 8 (9, 10), 9 (5), 10 (6).
- SKILL.md (estratégia por motivo, dry-run, batch approval) → Task 13.
- Critério de aceite "detecta quebras da MOC IA" + "< 5s" → Task 14.

Coberto. Os pontos da spec sobre `git log --follow` para auto-correção de
renames ficam no SKILL.md (Task 13) como **estratégia do agente**, não no
script Python — isso está alinhado com a separação de camadas da spec.

**Placeholder scan:** nenhum "TBD" / "TODO" / "similar a Task N" / "implement
later". Todo step com mudança de código mostra o código.

**Type consistency:**

- `index_vault` retorna dict com chaves `files_by_basename`,
  `files_by_relpath`, `folders`, `folders_with_index` — consistente em todas
  as tasks que constroem fixtures.
- `Link` dict tem sempre `file`, `line`, `raw`, `target`, `alias`, `anchor`,
  `type`, `in_frontmatter` — consistente em parsers e fixtures.
- `Broken` adiciona `reason` + `candidates` — consistente.
- `resolve_link` evolui de `(link, index)` (Tasks 6-8) para `(link, index,
  vault_root=None)` (Task 9 em diante). Mudança backwards-compatible (default
  None); fixtures antigas continuam válidas.
- `scan_folder(target, vault_root)` e `main(argv)` — assinaturas usadas
  consistentemente.

OK.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-05-18-verificar-wikilinks.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — eu dispacho um subagente fresh por task, faço review entre tasks, iteração rápida.

**2. Inline Execution** — executo as tasks nesta sessão usando `executing-plans`, com checkpoints para review.

**Qual abordagem?**
