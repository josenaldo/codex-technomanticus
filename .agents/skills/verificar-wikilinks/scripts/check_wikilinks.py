"""verificar-wikilinks — detector de wikilinks quebrados no vault.

Uso: python check_wikilinks.py <pasta-alvo> [--vault-root <path>]
                                            [--output <json-path>]
                                            [--respect-public-only]

Aplica a regra do Quartz: [[Pasta]] é quebrado se a pasta não tiver index.md.
"""

from __future__ import annotations

import re
from pathlib import Path

IGNORED_DIRS = {".git", ".obsidian", "node_modules", ".agents", ".quartz-cache"}

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


def main(argv: list[str] | None = None) -> int:
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
