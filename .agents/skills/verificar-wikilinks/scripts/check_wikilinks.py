"""verificar-wikilinks — detector de wikilinks quebrados no vault."""
from __future__ import annotations

IGNORED_DIRS = {".git", ".obsidian", "node_modules", ".agents", ".quartz-cache"}


def main(argv: list[str] | None = None) -> int:
    raise NotImplementedError


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
