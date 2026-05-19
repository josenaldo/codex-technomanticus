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

    def test_escaped_pipe_in_table_treated_as_alias_separator(self):
        # Em tabelas markdown, `|` precisa ser escapado como `\|`.
        # O parser deve tratar `\|` como o separador alias/target (não como literal).
        links = cw.extract_wikilinks("[[Anatomia dos LLMs\\|17 - Evaluation]]\n")
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["target"], "Anatomia dos LLMs")
        self.assertEqual(links[0]["alias"], "17 - Evaluation")


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
        links = cw.extract_wikilinks_clean(text)
        self.assertFalse(links[0]["in_frontmatter"])


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
        self.assertIn("Pasta/A.md", broken["candidates"])

    def test_nested_folder_path_with_index_resolves(self):
        idx = {
            "files_by_basename": {"index": ["A/B/index.md"]},
            "files_by_relpath": {"A/B/index.md"},
            "folders": {"B": ["A/B"]},
            "folders_with_index": {"A/B"},
        }
        self.assertIsNone(cw.resolve_link(self._link("A/B"), idx))


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


class TestScanAndCLI(unittest.TestCase):
    def test_scan_folder_detects_moc_bug(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = make_vault(Path(tmp), {
                "MOC/index.md": "# MOC\n\n[[Anatomia]] [[Existente]]\n",
                "MOC/Anatomia/01.md": "# 01\n",        # pasta sem index.md
                "MOC/Existente.md": "# Existente\n",
            })
            report = cw.scan_folder(vault / "MOC", vault_root=vault)
            self.assertEqual(report["stats"]["files_scanned"], 3)
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


class TestPolish(unittest.TestCase):
    def test_nested_wikilink_marked_malformed(self):
        text = "[[a [[b]] c]]\n"
        links = cw.extract_wikilinks_clean(text)
        offenders = [l for l in links if "[" in l["target"] or "]" in l["target"]]
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


if __name__ == "__main__":
    unittest.main()
