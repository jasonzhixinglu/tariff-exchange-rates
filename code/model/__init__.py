"""Nested-CES N-country model of "Understanding Multilateral Tariffs and
Exchange Rates" (Lu and Milkov).

    nested_ces    exact nonlinear model and balanced-trade solver
    linear        linearized system of Appendix A from baseline shares
    closed_forms  symmetric-benchmark closed forms and the composite bystander
    asymmetry     fixed-baseline polynomials and primitive-fixed thresholds

Scripts put the `code/` directory on sys.path and `import model`.
"""
from . import asymmetry, closed_forms, linear, nested_ces  # noqa: F401
from . import extensions  # noqa: F401,E402
