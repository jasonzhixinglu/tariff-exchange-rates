# -*- coding: utf-8 -*-
"""Check (a): trade-weighted NEER at a plausible calibration.

N = 3, free trade, first order.  alpha_D = 0.8, alpha_T = 0.4, eta = 1.5 for
all countries.  beta_AB = 0.2 (beta_AC = 0.8); beta_AB alone cannot push
w_AC above about 0.73 (w_AC = 0.731 at beta_AB = 0.02), so L_B is chosen so
that A's baseline trade weight on C hits the target at the reference point
rho_ref = 3 rho_D.  Everything else is symmetric.  Primitives are then held
fixed while rho varies, and the free-trade baseline is re-solved at each rho.
Reported: first rho with d nu_C = 0 and first rho with d nu_A^E = 0 on
(1, 20], MML at every grid point, and an exact check at tau = 0.01.
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(__file__))
import model as M

HERE = os.path.dirname(__file__)
CAL = dict(aD=0.8, aT=0.4, eta=1.5)
RHO_REF = 3 * M.rhoD(**CAL)
BETA_AB = 0.2
DIRECTION = np.zeros((3, 3)); DIRECTION[0, 1] = 1.0


def prim(LB, rho):
    P = M.symmetric(3, rho=rho, **CAL)
    b = P.beta.copy(); b[0, 1], b[0, 2] = BETA_AB, 1 - BETA_AB
    L = P.L.copy(); L[1] = LB
    return P.with_(beta=b, L=L)


def at(LB, rho):
    P = prim(LB, rho)
    nu = M.solve(P)
    J, _, Gf = M.linearize(P, nu)
    dnu = np.linalg.solve(-J, Gf[1:, 0, 1])
    w = M.neer_weights(P, nu)
    return dict(dnuB=dnu[0], dnuC=dnu[1], neer=w[1] * dnu[0] + w[2] * dnu[1],
                wAC=w[2], mml=M.mml_holds(J)[0], P=P, nu=nu)


def first_root(LB, key, grid):
    vals = [at(LB, r)[key] for r in grid]
    for a, b, fa, fb in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if fa < 0 <= fb:
            return brentq(lambda r: at(LB, r)[key], a, b, xtol=1e-8)
    return None


if __name__ == "__main__":
    grid = np.linspace(1.01, 20, 120)
    out = dict(calibration=CAL, beta_AB=BETA_AB, rho_ref=RHO_REF, cases=[])
    for target in (0.75, 0.85, 0.90):
        LB = brentq(lambda l: at(l, RHO_REF)["wAC"] - target, 0.01, 1.0, xtol=1e-10)
        mml_all = all(at(LB, r)["mml"] for r in grid)
        rC = first_root(LB, "dnuC", grid)
        rE = first_root(LB, "neer", grid)
        case = dict(target_wAC=target, L_B=LB, mml_on_grid=mml_all, rho_reversal=rC, rho_neer=rE,
                    wAC_at_reversal=at(LB, rC)["wAC"] if rC else None,
                    wAC_at_neer=at(LB, rE)["wAC"] if rE else None,
                    wAC_at_rho20=at(LB, 20.0)["wAC"])
        out["cases"].append(case)
        print("w_AC=%.2f  L_B=%.4f  MML all rho<=20: %s  reversal at rho=%s  NEER flips at rho=%s  (w_AC there %s)"
              % (target, LB, mml_all, "%.3f" % rC if rC else "none",
                 "%.3f" % rE if rE else "none for rho<=20",
                 "%.3f" % case["wAC_at_neer"] if rE else "-"))
    # exact check, w_AC = 0.85 case, at a rho between the two roots and one above both
    c = out["cases"][1]
    checks = []
    rhos = [0.5 * (c["rho_reversal"] + (c["rho_neer"] or 20.0))]
    if c["rho_neer"]:
        rhos.append(c["rho_neer"] + 2.0)
    for r in rhos:
        a = at(c["L_B"], r)
        T = np.zeros((3, 3)); T[0, 1] = 0.01
        nu1 = M.solve(a["P"], T, nu0=a["nu"])
        d = (nu1 - a["nu"]) / 0.01
        w = M.neer_weights(a["P"], a["nu"])
        checks.append(dict(rho=r, linear_dnuC=a["dnuC"], exact_dnuC=d[1], linear_neer=a["neer"],
                           exact_neer=w[1] * d[0] + w[2] * d[1]))
        print("  exact check rho=%.3f: d nu_C linear %+.5f exact %+.5f | NEER linear %+.5f exact %+.5f"
              % (r, a["dnuC"], d[1], a["neer"], w[1] * d[0] + w[2] * d[1]))
    out["exact_checks"] = checks
    json.dump(out, open(os.path.join(HERE, "results", "check_neer_calibration.json"), "w"), indent=1)
