"""Rebuild every paper number, table, figure and the PDF, in order.

    python code/run_all.py            # everything (FX data must be cached)
    python code/run_all.py --fetch    # also (re)download the 2025 FX data

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
    if "--fetch" in sys.argv:
        run([py, os.path.join("data", "fetch_fx_2025.py")], CODE)
    run([py, "-m", "pytest", "-q", "tests"], CODE)
    run([py, os.path.join("checks", "appendix_c.py")], CODE)
    run([py, os.path.join("checks", "appendix_c.py"), "--kappa-grid"], CODE)
    run([py, os.path.join("checks", "asymmetry_checks.py")], CODE)
    run([py, os.path.join("checks", "us_china_row.py")], CODE)
    run([py, os.path.join("tables", "make_tables.py")], CODE)
    figs = os.path.join(CODE, "figures")
    for f in sorted(os.listdir(figs)):
        if f.startswith("fig") and f.endswith(".py"):
            run([py, f], figs)
    run(["latexmk", "-pdf", "-interaction=nonstopmode", "main.tex"], os.path.join(ROOT, "paper"))


if __name__ == "__main__":
    main()
