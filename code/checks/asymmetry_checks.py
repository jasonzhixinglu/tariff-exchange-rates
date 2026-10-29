"""Section 4 computations, N = 3, US-like parameters unless stated.

  * examples (a)-(c) of Proposition 4.3: normalized Q_{A|B}(rho) and roots;
  * the two-root network example;
  * Table 2: sign of q2 on the size x import-weight grid at rho-bar = 3 rho_D;
  * Table 3: bystander reversal and trade-weighted NEER thresholds (primitives
    held fixed, baseline re-solved at each rho);
  * the reconciliation of the import-weighted aggregate terms-of-trade
    threshold (example b, 3.34) with the trade-weighted NEER threshold (3.98);
  * the leading coefficient of the bilateral bystander numerator.
Writes code/results/asymmetry.json.
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from model import asymmetry as asy  # noqa: E402
from model import closed_forms as cf  # noqa: E402
from model import linear as lin  # noqa: E402

D = asy.unilateral_direction(3)
RHO_BAR = 3 * cf.rhoD(**cf.US_LIKE)            # 3.96
SB_GRID = [0.1, 0.2, 0.4, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0]
BAB_GRID = [0.10, 0.20, 0.35, 0.50, 0.65, 0.80, 0.90]


def import_Q(base):
    return asy.poly_coeffs(base, lin.import_weights(base), D)


def example_a():
    base = lin.symmetric_base(3, rho=RHO_BAR, **cf.US_LIKE)
    q = import_Q(base)
    q[0] = 0.0 if abs(q[0]) < 1e-12 * np.abs(q).max() else q[0]
    return base, q


def example_b(L_B=0.22):
    P = asy.three_country_prims(L=(1, L_B, 1), beta_AB=0.2, rho=RHO_BAR, **cf.US_LIKE)
    base, _ = asy.base_from_prims(P)
    return base, import_Q(base)


EXC_H = np.array([0.201, 0.854, 0.360])
EXC_B = np.array([[0, .525, .475], [.766, 0, .234], [.407, .593, 0]])
EXC_Y = np.array([1.0, 5.118, 0.866])


def example_c(rebalance=True):
    y = lin.balanced_incomes(EXC_H, EXC_B, 0.862) if rebalance else EXC_Y
    base = dict(y=y, h=EXC_H, b=EXC_B, aT=0.862, eta=3.007, rho=RHO_BAR)
    return base, import_Q(base)


def two_root_example():
    P = asy.three_country_prims(L=(1, 2, 1), beta_AB=0.2, beta_BA=0.9, beta_CA=0.1,
                                rho=RHO_BAR, **cf.US_LIKE)
    base, _ = asy.base_from_prims(P)
    return base, import_Q(base)


def q2_grid():
    rows = []
    for sb in SB_GRID:
        row = []
        for bab in BAB_GRID:
            P = asy.three_country_prims(L=(1, sb, 1), beta_AB=bab, rho=RHO_BAR, **cf.US_LIKE)
            base, _ = asy.base_from_prims(P)
            q = import_Q(base)
            qh = asy.normalized(q)
            sym = abs(sb - 1) < 1e-12 and abs(bab - 0.5) < 1e-12
            sign = 0 if sym else int(np.sign(qh[0]))
            roots = asy.positive_roots(q) if sign != 0 else asy.positive_roots(q[1:])
            row.append(dict(S_B=sb, beta_AB=bab, sign_q2=sign, qhat=qh.tolist(),
                            roots=roots.tolist(), mml=lin.mml(lin.reduced_jacobian(base)),
                            two_root=bool(qh[0] < 0 and qh[1] > 0 and qh[1] ** 2 - 4 * qh[0] * qh[2] > 0)))
        rows.append(row)
    return rows


# ------------------------------------------------- Table 3 and reconciliation
def _prims(L_B, rho):
    return asy.three_country_prims(L=(1, L_B, 1), beta_AB=0.2, rho=rho, **cf.US_LIKE)


_cache = {}


def at(L_B, rho):
    key = (L_B, rho)
    if key not in _cache:
        _cache[key] = asy.responses_at(_prims(L_B, rho))
    return _cache[key]


GRID = np.linspace(1.01, 20.0, 96)


def first_root(fun):
    roots, _ = asy.scan_roots(fun, GRID)
    return roots[0] if roots else None


def table3_row(target):
    L_B = brentq(lambda l: at(l, RHO_BAR)["w"][1] - target, 0.01, 1.0, xtol=1e-12)
    out = dict(w_AC=target, L_B=L_B)
    out["rho_dnuC"] = first_root(lambda r: at(L_B, r)["dnu"][1])
    out["rho_neer"] = first_root(lambda r: at(L_B, r)["w"] @ at(L_B, r)["dnu"])
    out["rho_tot_primfixed"] = first_root(lambda r: at(L_B, r)["b"] @ at(L_B, r)["dnu"])
    base = at(L_B, RHO_BAR)["base"]
    out["rho_tot_fixedbase"] = asy.positive_roots(import_Q(base))[-1]
    out["rho_neer_fixedbase"] = asy.positive_roots(asy.poly_coeffs(base, lin.trade_weights(base), D))[-1]
    out["rho_dnuC_fixedbase"] = asy.positive_roots(asy.poly_coeffs(base, np.array([0.0, 1.0]), D))[-1]
    out["import_weights"] = at(L_B, RHO_BAR)["b"].tolist()
    out["trade_weights"] = at(L_B, RHO_BAR)["w"].tolist()
    out["mml_on_grid"] = all(at(L_B, r)["mml"] for r in GRID)
    return out


def leading_coefficient_check(n=20, seed=0):
    """Bilateral bystander numerator: q2 / [b_AB b_AC b_CA b_CB (1-h_A)(1-h_C) y_A y_C]."""
    rng = np.random.default_rng(seed)
    ratios = []
    for _ in range(n):
        P = asy.three_country_prims(L=np.exp(rng.normal(0, .6, 3)), beta_AB=rng.uniform(.1, .9),
                                    beta_BA=rng.uniform(.1, .9), beta_CA=rng.uniform(.1, .9),
                                    rho=3.0, aD=0.8, aT=0.4, eta=1.5)
        base, _ = asy.base_from_prims(P)
        q = asy.poly_coeffs(base, np.array([0.0, 1.0]), D)
        b, h, y = base["b"], base["h"], base["y"]
        prod = b[0, 1] * b[0, 2] * b[2, 0] * b[2, 1] * (1 - h[0]) * (1 - h[2]) * y[0] * y[2]
        ratios.append(q[0] / prod)
    return ratios


def main():
    res = {}
    _, qa = example_a(); res["example_a"] = dict(qhat=asy.normalized(qa).tolist())
    for lb in (0.22, None):
        if lb is None:
            continue
    _, qb = example_b(); res["example_b"] = dict(qhat=asy.normalized(qb).tolist(),
                                                  roots=asy.positive_roots(qb).tolist())
    for reb in (False, True):
        base, qc = example_c(reb)
        res["example_c_" + ("rebalanced" if reb else "as_stated")] = dict(
            y=list(base["y"]), qhat=asy.normalized(qc).tolist(), roots=asy.positive_roots(qc).tolist(),
            tb_residual=lin.balance_residual(base).tolist())
    _, q2r = two_root_example()
    res["two_root_example"] = dict(qhat=asy.normalized(q2r).tolist(), roots=asy.positive_roots(q2r).tolist())
    res["q2_grid"] = q2_grid()
    res["table3"] = [table3_row(t) for t in (0.75, 0.85, 0.90)]
    ratios = leading_coefficient_check()
    res["leading_coeff_ratio"] = dict(min=min(ratios), max=max(ratios))
    print(json.dumps({k: v for k, v in res.items() if k != "q2_grid"}, indent=1))
    with open(os.path.join(HERE, "..", "results", "asymmetry.json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
