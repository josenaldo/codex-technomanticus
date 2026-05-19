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
