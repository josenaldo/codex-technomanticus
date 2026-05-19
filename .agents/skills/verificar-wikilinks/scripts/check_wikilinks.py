"""verificar-wikilinks — detector de wikilinks quebrados no vault.

Uso: python check_wikilinks.py <pasta-alvo> [--vault-root <path>]
                                            [--output <json-path>]
                                            [--respect-public-only]

Aplica a regra do Quartz: [[Pasta]] é quebrado se a pasta não tiver index.md.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

IGNORED_DIRS = {".git", ".obsidian", "node_modules", ".agents", ".quartz-cache"}

WIKILINK_RE = re.compile(r"(?P<embed>!?)\[\[(?P<body>[^\[\]\n]+?)\]\]")
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
            out_lines.append("")
            continue
        if in_fence:
            out_lines.append("")
        else:
            out_lines.append(INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line))
    return "\n".join(out_lines)


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
                continue
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

            unescaped_body = body.replace("\\|", "|")
            if "|" in unescaped_body:
                target_part, alias = unescaped_body.split("|", 1)
            else:
                target_part = unescaped_body
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


HEADER_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")


def slugify_header(text: str) -> str:
    """Slug compatível com Obsidian/Quartz: lowercase, espaços->-, remove markdown.

    Mantém letras acentuadas (Quartz não transliterate por default).
    """
    text = text.strip().lower()
    text = re.sub(r"[*_`]+", "", text)
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


def find_candidates(target: str, index: dict, n: int = 5, cutoff: float = 0.6) -> list[str]:
    """Sugestões fuzzy via difflib sobre basenames + relpaths."""
    pool = list(index["files_by_basename"].keys()) + list(index["files_by_relpath"])
    matches = difflib.get_close_matches(target, pool, n=n, cutoff=cutoff)
    resolved: list[str] = []
    for m in matches:
        if m in index["files_by_relpath"]:
            resolved.append(m)
        else:
            paths = index["files_by_basename"].get(m, [])
            resolved.extend(paths)
    seen: set[str] = set()
    out: list[str] = []
    for p in resolved:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out[:n]


def resolve_link(link: dict, index: dict, vault_root: Path | None = None) -> dict | None:
    target = link["target"]
    target_norm = target[:-3] if target.endswith(".md") else target
    is_markdown = link["type"] == "markdown"

    if "[" in target or "]" in target:
        return {**link, "reason": "malformed", "candidates": []}

    resolved_path: str | None = None

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

    if resolved_path is None:
        matches = index["files_by_basename"].get(target_norm, [])
        if len(matches) == 1:
            resolved_path = matches[0]
        elif len(matches) > 1:
            return {**link, "reason": "ambiguous", "candidates": matches}

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

    if resolved_path is None:
        if is_markdown:
            return {**link, "reason": "markdown_broken_path",
                    "candidates": find_candidates(target_norm, index)}
        return {**link, "reason": "target_not_found",
                "candidates": find_candidates(target_norm, index)}

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
            raw_bytes = path.read_bytes()
        except OSError as exc:
            warnings.append({"file": rel, "msg": f"unreadable: {exc.__class__.__name__}"})
            continue
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            warnings.append({"file": rel, "msg": "encoding error, decoded with replace"})
            text = raw_bytes.decode("utf-8", errors="replace")
        files_scanned += 1

        all_links = extract_wikilinks_clean(text) + extract_markdown_links(text)

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
        by_reason: dict[str, int] = {}
        for b in report["broken"]:
            by_reason[b["reason"]] = by_reason.get(b["reason"], 0) + 1
        report["stats"]["by_reason"] = by_reason

    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
