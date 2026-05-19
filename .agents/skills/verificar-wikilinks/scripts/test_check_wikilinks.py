"""Testes de verificar-wikilinks. Rodar com: python -m unittest scripts.test_check_wikilinks -v"""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path


def make_vault(files: dict[str, str]) -> Path:
    """Cria um vault temporário com os arquivos descritos (relpath -> conteúdo).
    Sempre cria .obsidian/ para auto-detect funcionar.
    """
    tmp = Path(tempfile.mkdtemp(prefix="vault-"))
    (tmp / ".obsidian").mkdir()
    for rel, content in files.items():
        p = tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return tmp


class TestHarness(unittest.TestCase):
    def test_harness_smoke(self):
        vault = make_vault({"A.md": "# A", "sub/B.md": "# B"})
        self.assertTrue((vault / ".obsidian").is_dir())
        self.assertTrue((vault / "A.md").is_file())
        self.assertTrue((vault / "sub" / "B.md").is_file())


if __name__ == "__main__":
    unittest.main()
