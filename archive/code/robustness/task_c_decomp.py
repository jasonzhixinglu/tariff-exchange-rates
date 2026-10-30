# -*- coding: utf-8 -*-
"""Task C, attribution.  By the sign rule (9),
    d nu_C = theta_CB F_B + theta_CC F_C,   theta = (-J)^{-1},
so at the threshold  R_F = R_theta, with
    R_F     = -F_C / F_B            relative disturbance (diversion to C vs loss of B)
    R_theta = theta_CB / theta_CC   relative adjustment (how much C's rate responds to B's
                                     disturbance, per unit of its own)
Let D(rho, x) = ln R_F - ln R_theta.  Then
    d rho*/dx = -(D_x) / D_rho = -(dlnR_F/dx) / D_rho + (dlnR_theta/dx) / D_rho,
splitting each sensitivity into a disturbance part and an adjustment part.
Derivatives by central differences; the baseline is re-solved at every point.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import model as M
from task_c import primitives, CAL, NAMES

HERE = os.path.dirname(__file__)


def ratios(rho, x=None, h=0.0, cal=CAL):
    P = primitives(rho, x, h, cal)
    nu0 = M.solve(P)
    J, _, Gf = M.linearize(P, nu0)
    F = Gf[1:, 0, 1]
    th = np.linalg.inv(-J)
    return np.log(-F[1] / F[0]), np.log(th[1, 0] / th[1, 1]), F, th


if __name__ == "__main__":
    out = {}
    cals = {"baseline": CAL, "US-like": dict(aD=0.8, aT=0.4, eta=1.5),
            "low home bias, high eta": dict(aD=0.5, aT=0.6, eta=3.0)}
    for cname, cal in cals.items():
        r0 = 3 * M.rhoD(**cal)
        e = 1e-4
        lf_p, lt_p, _, _ = ratios(r0 + e, cal=cal)
        lf_m, lt_m, _, _ = ratios(r0 - e, cal=cal)
        Drho = ((lf_p - lt_p) - (lf_m - lt_m)) / (2 * e)
        _, _, F0, th0 = ratios(r0, cal=cal)
        rows = {}
        for x in NAMES:
            h = 1e-4
            a = ratios(r0, x, h, cal)
            b = ratios(r0, x, -h, cal)
            dF = (a[0] - b[0]) / (2 * h)
            dT = (a[1] - b[1]) / (2 * h)
            rows[x] = dict(disturbance_part=-dF / Drho, adjustment_part=dT / Drho,
                           total=(-dF + dT) / Drho, dlnRF=dF, dlnRtheta=dT)
            print("%-24s %-10s total %+.4f = disturbance %+.4f + adjustment %+.4f"
                  % (cname, x, rows[x]["total"], rows[x]["disturbance_part"], rows[x]["adjustment_part"]))
        out[cname] = dict(D_rho=Drho, F=F0.tolist(), theta=th0.tolist(), rows=rows)
    json.dump(out, open(os.path.join(HERE, "results", "task_c_decomp.json"), "w"), indent=1)
