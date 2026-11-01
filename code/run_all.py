"""Rebuild every paper number, table, figure and the PDF, in order.

    python code/run_all.py

The FX script downloads only raw files missing from data/raw/fx2025 and
rebuilds the processed files from the cache, so the run is offline once the
cache exists.
Steps: unit tests -> numerical checks (code/results/*.json) -> tables
(paper/tables) -> figures (paper/figures) -> latexmk (paper/main.pdf).
"""
import os
import subprocess
import sys

CODE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CODE)


def run(args, cwd):
    print("\n$", " ".join(args), "  (in %s)" % os.path.relpath(cwd, ROOT))
    subprocess.run(args, cwd=cwd, check=True)


def main():
    py = sys.executable
    run([py, "-m", "pytest", "-q", "tests"], CODE)
    run([py, os.path.join("checks", "appendix_c.py")], CODE)
    run([py, os.path.join("checks", "appendix_c.py"), "--kappa-grid"], CODE)
    run([py, os.path.join("checks", "asymmetry_checks.py")], CODE)
    run([py, os.path.join("checks", "us_china_row.py")], CODE)
    run([py, os.path.join("checks", "appendix_d.py")], CODE)
    run([py, os.path.join("data", "fetch_fx_2025.py")], CODE)
    run([py, os.path.join("checks", "episode2025.py")], CODE)
    run([py, os.path.join("tables", "make_tables.py")], CODE)
    figs = os.path.join(CODE, "figures")
    for f in sorted(os.listdir(figs)):
        if f.startswith("fig") and f.endswith(".py"):
            run([py, f], figs)
    run(["latexmk", "-pdf", "-interaction=nonstopmode", "main.tex"], os.path.join(ROOT, "paper"))
    # The online supplement resolves references from main.aux, so it builds second.
    run(["latexmk", "-pdf", "-interaction=nonstopmode", "online_appendix.tex"], os.path.join(ROOT, "paper"))


if __name__ == "__main__":
    main()
