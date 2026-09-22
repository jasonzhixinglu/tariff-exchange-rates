# -*- coding: utf-8 -*-
"""Extra to tasks C/D: with primitives (not shares) held fixed, how does the
sign of d nu_C / d tau_AB change as rho rises?  Appendix B.3 (eq. 63) holds
baseline shares fixed, so the numerator is quadratic in rho with c_2 > 0.
With primitives fixed, an asymmetric free-trade baseline has relative prices
away from one, so the shares themselves move with rho.

500 draws from the task D box (common alpha_D, eta), with rho scanned on a
grid in [1, 200].  Counts the number of sign changes of d nu_C, keeping only
grid points where MML holds.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import model as M
from task_d import unpack

HERE = os.path.dirname(__file__)
RHOS = np.concatenate([np.linspace(1.05, 10, 18), np.geomspace(11, 200, 12)])

if __name__ == "__main__":
    rng = np.random.default_rng(7)
    counts = {}
    examples = []
    n_ok = 0
    for k in range(500):
        z = rng.random(9)
        signs = []
        ok = True
        for r in RHOS:
            z2 = z.copy(); z2[8] = (r - 1) / 9.0       # rho enters unpack as 1 + 9 z[8]
            P = unpack(z2, "common")
            try:
                nu = M.solve(P)
                J, _, Gf = M.linearize(P, nu)
            except Exception:
                ok = False; break
            if not M.mml_holds(J)[0]:
                ok = False; break
            signs.append(np.sign(np.linalg.solve(-J, Gf[1:, 0, 1])[1]))
        if not ok:
            continue
        n_ok += 1
        s = np.array(signs)
        changes = int(np.sum(s[1:] != s[:-1]))
        final = int(s[-1])
        key = "%d changes, sign at rho=200: %+d" % (changes, final)
        counts[key] = counts.get(key, 0) + 1
        if changes >= 2 and len(examples) < 5:
            P = unpack(z, "common")
            examples.append(dict(L=P.L.round(3).tolist(), beta_AB=float(P.beta[0, 1]),
                                 beta_BA=float(P.beta[1, 0]), beta_CA=float(P.beta[2, 0]),
                                 aD=float(P.aD[0]), eta=float(P.eta[0]),
                                 positive_rho=[float(r) for r, g in zip(RHOS, s) if g > 0]))
    out = dict(draws=500, all_grid_points_mml=n_ok, counts=counts, examples=examples,
               rho_grid=RHOS.tolist())
    print(json.dumps(out, indent=1))
    json.dump(out, open(os.path.join(HERE, "results", "task_d_rho_scan.json"), "w"), indent=1)
