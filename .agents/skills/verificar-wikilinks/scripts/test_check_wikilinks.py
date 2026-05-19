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


if __name__ == "__main__":
    unittest.main()
