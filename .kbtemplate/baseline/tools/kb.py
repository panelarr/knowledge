#!/usr/bin/env python3
"""Knowledge base CLI. Stdlib only, Python 3.9+.

    python3 tools/kb.py check                 # health check (run before every commit)
    python3 tools/kb.py new adr "Use SQLite"  # next free ID, filled template, index row
    python3 tools/kb.py init                  # turn the template into your KB
    python3 tools/kb.py ops digest            # issues and PRs across registered repos
    python3 tools/kb.py --help                # everything else
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kblib.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
