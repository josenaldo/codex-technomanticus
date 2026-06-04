#!/usr/bin/env python3
"""
health-audit.py — Auditoria de saúde do vault Codex Technomanticus.

Roda LOCALMENTE contra o working tree (não depende de GitHub/nuvem).
Gera um relatório em 00-Meta/health-audits/<YYYY-MM-DD>.md e imprime um resumo.

Checks:
  1. Estrutura canônica  — pastas-zona do vault existem
  2. Skill drift         — skills em .agents/skills/ batem com o catálogo (AGENTS.md ou skills.md)
  3. Wikilinks quebrados — [[alvo]] que não resolve pra nenhuma nota/alias
  4. Notas órfãs         — notas sem nenhum link de entrada (ignora index/MOC/templates)
  5. Frontmatter ausente — .md de conteúdo sem bloco --- ---
  6. Glosas estagnadas   — arquivos na raiz de 02-Glosas/ parados há > 30 dias

Uso:  python3 00-Meta/scripts/health-audit.py [caminho-do-vault]
"""

import os
import re
import sys
import time
from datetime import datetime, date

# ── Localização do vault ────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT = sys.argv[1] if len(sys.argv) > 1 else os.path.normpath(os.path.join(SCRIPT_DIR, "..", ".."))

REQUIRED_DIRS = ["00-Meta", "01-Pergaminhos", "02-Glosas", "03-Dominios", "04-Sendas"]
EXCLUDE_DIRS = {".git", ".obsidian", ".claude", ".agents", "docs", "memory",
                "node_modules", "health-audits"}
# Docs de configuração/manifesto — não são notas do vault.
CONFIG_DOCS = {"agents.md", "claude.md", "gemini.md", "readme.md"}
STALE_DAYS = 30

WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
ALIAS_INLINE_RE = re.compile(r"^\s*aliases:\s*\[(.*)\]", re.IGNORECASE)
FENCED_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def is_template(rel):
    return "/templates/" in ("/" + rel.replace(os.sep, "/"))


def clean_text(text):
    """Remove blocos de código e spans inline pra não contar wikilinks de exemplo."""
    return INLINE_CODE_RE.sub("", FENCED_RE.sub("", text))


def is_placeholder(target):
    """Placeholders do Templater (<% %>) ou marcadores genéricos (<...>)."""
    return any(c in target for c in "<%>")


def iter_md_files():
    """Caminha pelo vault, pulando diretórios técnicos."""
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for f in files:
            if f.endswith(".md"):
                yield os.path.join(root, f)


def parse_frontmatter(text):
    """Retorna (tem_frontmatter, dict_simples). Parser leve, sem dependências."""
    if not text.startswith("---"):
        return False, {}
    end = text.find("\n---", 3)
    if end == -1:
        return False, {}
    fm, meta, key = text[3:end], {}, None
    for line in fm.splitlines():
        m = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1).lower()
            meta[key] = m.group(2).strip()
        elif key and re.match(r"^\s*-\s+", line):
            meta.setdefault(key + "__list", []).append(re.sub(r"^\s*-\s+", "", line).strip())
    return True, meta


def collect_aliases(meta):
    out = []
    if "aliases__list" in meta:
        out += meta["aliases__list"]
    raw = meta.get("aliases", "")
    if raw.startswith("["):
        out += [x.strip().strip('"\'') for x in raw[1:-1].split(",") if x.strip()]
    elif raw and not raw.startswith("["):
        out.append(raw.strip('"\''))
    return [a for a in (s.strip('"\'') for s in out) if a]


def norm(s):
    return s.strip().lower()


def main():
    notes = {}            # rel_path -> {basename, aliases, fm, text, mtime}
    basenames = {}        # lower basename -> count
    relpaths = set()      # lower rel path sem .md
    alias_set = set()     # lower aliases

    for path in iter_md_files():
        rel = os.path.relpath(path, VAULT)
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        base = os.path.splitext(os.path.basename(path))[0]
        has_fm, meta = parse_frontmatter(text)
        aliases = collect_aliases(meta)
        notes[rel] = {
            "base": base, "aliases": aliases, "has_fm": has_fm,
            "text": text, "clean": clean_text(text),
            "mtime": os.path.getmtime(path), "meta": meta,
        }
        basenames[norm(base)] = basenames.get(norm(base), 0) + 1
        relpaths.add(norm(os.path.splitext(rel)[0]))
        for a in aliases:
            alias_set.add(norm(a))

    findings = {}

    # ── 1. Estrutura canônica ──────────────────────────────────────────
    missing_dirs = [d for d in REQUIRED_DIRS if not os.path.isdir(os.path.join(VAULT, d))]
    findings["estrutura"] = missing_dirs

    # ── 2. Skill drift ─────────────────────────────────────────────────
    # Fonte do catálogo auto-detectada: AGENTS.md ou 00-Meta/guia/skills.md.
    skill_drift = {"sem_doc": [], "sem_skill": []}
    skills_dir = os.path.join(VAULT, ".agents", "skills")
    doc_path = next((os.path.join(VAULT, p) for p in
                     ("AGENTS.md", os.path.join("00-Meta", "guia", "skills.md"))
                     if os.path.isfile(os.path.join(VAULT, p))), None)
    if os.path.isdir(skills_dir) and doc_path:
        skill_dirs = {d for d in os.listdir(skills_dir)
                      if os.path.isdir(os.path.join(skills_dir, d))}
        doc_txt = open(doc_path, encoding="utf-8", errors="replace").read()
        # documentada = nome da pasta aparece no catálogo (com ou sem `/`).
        skill_drift["sem_doc"] = sorted(s for s in skill_dirs if s not in doc_txt)
        # comandos `/x` citados sem pasta de skill correspondente.
        # Exige crase imediatamente antes da barra (`/cmd`) pra não capturar
        # segmentos de path como `00-Meta/guia/skills.md` → guia/skills.
        cited = set(re.findall(r"`/([a-z][a-z0-9-]+)", doc_txt))
        skill_drift["sem_skill"] = sorted(cited - skill_dirs)
    findings["skill_drift"] = skill_drift

    # ── 3. Wikilinks quebrados ─────────────────────────────────────────
    ATTACH_EXT = (".pdf", ".html", ".png", ".jpg", ".jpeg", ".gif",
                  ".svg", ".canvas", ".xlsx", ".csv", ".mp3", ".mp4", ".webp")
    dangling = {}      # alvo-nota -> nº de ocorrências (deduplicado)
    attach_misses = 0  # links pra anexos/fontes externas (normal: vivem em ~/documents)
    for rel, n in notes.items():
        if is_template(rel):  # templates contêm placeholders por design
            continue
        for m in WIKILINK_RE.finditer(n["clean"]):
            target = m.group(1).split("|")[0].split("#")[0].split("^")[0].strip()
            if not target or is_placeholder(target):
                continue
            if target.lower().endswith(".md"):
                target = target[:-3]
            cand = norm(target)
            cand_base = norm(os.path.basename(target))
            if (cand in relpaths or cand_base in basenames or
                    cand in alias_set or cand_base in alias_set):
                continue
            if target.lower().endswith(ATTACH_EXT):
                attach_misses += 1
                continue
            dangling[target] = dangling.get(target, 0) + 1
    findings["dangling"] = sorted(dangling.items(), key=lambda x: (-x[1], x[0].lower()))
    findings["attach_misses"] = attach_misses

    # ── 4. Notas órfãs ─────────────────────────────────────────────────
    linked = set()
    for n in notes.values():
        for m in WIKILINK_RE.finditer(n["clean"]):
            t = m.group(1).split("|")[0].split("#")[0].split("^")[0].strip()
            if is_placeholder(t):
                continue
            if t.lower().endswith(".md"):
                t = t[:-3]
            linked.add(norm(os.path.basename(t)))
            linked.add(norm(t))
    orphans = []
    for rel, n in notes.items():
        b = norm(n["base"])
        fmtype = n["meta"].get("type", "").lower()
        if (b in ("index", "moc") or "moc" in fmtype or is_template(rel)
                or os.path.basename(rel).lower() in CONFIG_DOCS):
            continue
        if b not in linked and norm(os.path.splitext(rel)[0]) not in linked \
                and not any(norm(a) in linked for a in n["aliases"]):
            orphans.append(rel)
    findings["orphans"] = sorted(orphans)

    # ── 5. Frontmatter ausente ─────────────────────────────────────────
    no_fm = sorted(rel for rel, n in notes.items()
                   if not n["has_fm"] and not is_template(rel)
                   and os.path.basename(rel).lower() not in CONFIG_DOCS)
    findings["no_fm"] = no_fm

    # ── 6. Glosas estagnadas ───────────────────────────────────────────
    stale = []
    glosas_root = os.path.join(VAULT, "02-Glosas")
    now = time.time()
    if os.path.isdir(glosas_root):
        for f in os.listdir(glosas_root):
            p = os.path.join(glosas_root, f)
            if os.path.isfile(p) and f.endswith(".md") and f != "index.md":
                age = (now - os.path.getmtime(p)) / 86400
                if age > STALE_DAYS:
                    stale.append((f, int(age)))
    findings["stale_glosas"] = sorted(stale, key=lambda x: -x[1])

    write_report(findings, len(notes))


def write_report(f, total_notes):
    today = date.today().isoformat()
    out_dir = os.path.join(VAULT, "00-Meta", "health-audits")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{today}.md")

    n_issues = (len(f["estrutura"]) + len(f["skill_drift"]["sem_doc"]) +
                len(f["skill_drift"]["sem_skill"]) + len(f["dangling"]) +
                len(f["orphans"]) + len(f["no_fm"]) + len(f["stale_glosas"]))
    status = "✅ saudável" if n_issues == 0 else f"⚠️ {n_issues} achado(s)"

    L = []
    L.append("---")
    L.append(f'title: "Health Audit — {today}"')
    L.append("type: report")
    L.append("publish: false")
    L.append(f"created: {today}")
    L.append("tags:\n  - meta\n  - health-audit")
    L.append("---")
    L.append(f"# Health Audit — {today}\n")
    L.append(f"> [!abstract] TL;DR\n> {status} — {total_notes} notas auditadas.\n")

    L.append("## 1. Estrutura canônica")
    L.append("✅ Todas as pastas obrigatórias existem." if not f["estrutura"]
             else "Pastas **faltando**:\n" + "\n".join(f"- `{d}/`" for d in f["estrutura"]))
    L.append("")

    L.append("## 2. Skill drift (catálogo ↔ .agents/skills/)")
    sd = f["skill_drift"]
    if not sd["sem_doc"] and not sd["sem_skill"]:
        L.append("✅ Catálogo e as skills estão sincronizados.")
    else:
        if sd["sem_doc"]:
            L.append("Skills **sem menção no catálogo**:\n" + "\n".join(f"- `/{s}`" for s in sd["sem_doc"]))
        if sd["sem_skill"]:
            L.append("Comandos citados no catálogo **sem pasta de skill**:\n" + "\n".join(f"- `/{s}`" for s in sd["sem_skill"]))
    L.append("")

    L.append("## 3. Links pendentes (notas ainda não criadas)")
    L.append("> Dangling links são normais no Obsidian (stubs e forward-refs). "
             "Revise a lista buscando **typos** — um alvo que era pra resolver. "
             "Alvos repetidos em muitas notas tendem a ser conceitos a criar.")
    if f["attach_misses"]:
        L.append(f"\n_({f['attach_misses']} link(s) apontam pra anexos/fontes externas "
                 "— `.pdf`/`.html` etc. que vivem em `~/documents`; ignorados aqui.)_")
    if not f["dangling"]:
        L.append("\n✅ Nenhum link de nota pendente.")
    else:
        L.append(f"\n{len(f['dangling'])} alvo(s) distinto(s) sem nota correspondente "
                 "(× = nº de notas que referenciam):")
        for t, c in f["dangling"]:
            L.append(f"- `[[{t}]]` ×{c}")
    L.append("")

    L.append("## 4. Notas órfãs (sem link de entrada)")
    if not f["orphans"]:
        L.append("✅ Nenhuma órfã (ignorando index/MOC/templates).")
    else:
        L.append(f"{len(f['orphans'])} nota(s) sem links de entrada:")
        for rel in f["orphans"][:100]:
            L.append(f"- `{rel}`")
        if len(f["orphans"]) > 100:
            L.append(f"- … e mais {len(f['orphans']) - 100}.")
    L.append("")

    L.append("## 5. Frontmatter ausente")
    if not f["no_fm"]:
        L.append("✅ Todas as notas de conteúdo têm frontmatter.")
    else:
        L.append(f"{len(f['no_fm'])} nota(s) sem bloco `--- ---`:")
        for rel in f["no_fm"][:100]:
            L.append(f"- `{rel}`")
    L.append("")

    L.append("## 6. Glosas estagnadas (> 30 dias na raiz)")
    if not f["stale_glosas"]:
        L.append("✅ Nenhuma glosa parada — ou rode `/arquivar-glosas`.")
    else:
        L.append("Candidatas a `/arquivar-glosas`:")
        for name, age in f["stale_glosas"]:
            L.append(f"- `{name}` — parada há {age} dias")
    L.append("")

    report = "\n".join(L)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(report)

    print(f"[health-audit] {status} — relatório em {os.path.relpath(out_path, VAULT)}")
    print(f"[health-audit] {total_notes} notas | "
          f"links pendentes: {len(f['dangling'])} | órfãs: {len(f['orphans'])} | "
          f"sem frontmatter: {len(f['no_fm'])} | glosas paradas: {len(f['stale_glosas'])}")


if __name__ == "__main__":
    main()
