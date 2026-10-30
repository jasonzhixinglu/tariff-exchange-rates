"""Where does a US-China-ROW configuration sit in the q2 sign grid (Table 2)?
For archive/build-reports/BUILD_REPORT.md only; not a claim in the paper.

Data (2024, data/raw/trade2024/trade_2024.json): US-reported imports by origin
(Census), China-reported imports by origin (GACC), ROW imports from the US and
China as the residual of US/China exports, PPP GDP (IMF WEO Oct 2026).
A = US, B = China, C = ROW.  Origin weights beta_ij are calibrated so that the
balanced free-trade baseline reproduces the observed import-origin shares b_ij
at rho-bar = 3 rho_D; sizes L_i from PPP GDP.  We report (i) the grid
coordinates (S_B/S_C, b_AB) and the sign of q2 there, and (ii) q2, q0 and the
roots for the full calibrated network, for common US-like (alpha_D, alpha_T,
eta) and for a variant with the US home share set to its measured goods-
absorption value.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, ".."))

from model import asymmetry as asy  # noqa: E402
from model import closed_forms as cf  # noqa: E402
from model import linear as lin  # noqa: E402
from model import nested_ces as nc  # noqa: E402

D = asy.unilateral_direction(3)
RHO_BAR = 3 * cf.rhoD(**cf.US_LIKE)


def load():
    raw = json.load(open(os.path.join(ROOT, "data", "raw", "trade2024", "trade_2024.json")))
    return raw


def calibrate(L, b_target, aD, rho=RHO_BAR, iters=200):
    beta = b_target.copy()
    for _ in range(iters):
        P = nc.Primitives(N=3, L=L, aD=aD, aT=0.4, eta=1.5, rho=rho, beta=beta)
        nu = nc.solve(P)
        base = nc.baseline_shares(P, nu)
        err = np.nanmax(np.abs(base["b"] - b_target))
        if err < 1e-12:
            break
        beta = beta * np.where(base["b"] > 0, b_target / np.where(base["b"] > 0, base["b"], 1), 0)
        beta = beta / beta.sum(axis=1, keepdims=True)
    return P, base


def main():
    raw = load()
    g = lambda a, k: raw[a][k]["value"]
    vals = dict(us_imp_tot=g("us_census", "imports_total"), us_imp_cn=g("us_census", "imports_from_china"),
                us_exp_tot=g("us_census", "exports_total"), us_exp_cn=g("us_census", "exports_to_china"),
                cn_exp_tot=g("china_gacc", "exports_total"), cn_imp_tot=g("china_gacc", "imports_total"),
                cn_exp_us=g("china_gacc", "exports_to_us"), cn_imp_us=g("china_gacc", "imports_from_us"))
    ppp = dict(us=g("gdp_imf_weo", "ppp_usa"), china=g("gdp_imf_weo", "ppp_chn"),
               world=g("gdp_imf_weo", "ppp_world"))
    b = np.zeros((3, 3))
    b[0, 1] = vals["us_imp_cn"] / vals["us_imp_tot"]; b[0, 2] = 1 - b[0, 1]
    b[1, 0] = vals["cn_imp_us"] / vals["cn_imp_tot"]; b[1, 2] = 1 - b[1, 0]
    row_from_us = vals["us_exp_tot"] - vals["us_exp_cn"]
    row_from_cn = vals["cn_exp_tot"] - vals["cn_exp_us"]
    b[2, 0] = row_from_us / (row_from_us + row_from_cn); b[2, 1] = 1 - b[2, 0]
    L = np.array([ppp["us"], ppp["china"], ppp["world"] - ppp["us"] - ppp["china"]]) / ppp["us"]
    out = dict(inputs=vals, ppp=ppp, b_target=b.tolist(), L=L.tolist(),
               grid_coordinates=dict(S_B_over_S_C=L[1] / L[2], b_AB=b[0, 1]))
    # grid-cell analogue: S_A = S_C = 1, beta_AB chosen so the baseline b_AB matches
    from scipy.optimize import brentq
    sb = L[1] / L[2]

    def bab_gap(x):
        P = asy.three_country_prims(L=(1, sb, 1), beta_AB=x, rho=RHO_BAR, **cf.US_LIKE)
        return asy.base_from_prims(P)[0]["b"][0, 1] - b[0, 1]
    beta_AB = brentq(bab_gap, 0.01, 0.99)
    P = asy.three_country_prims(L=(1, sb, 1), beta_AB=beta_AB, rho=RHO_BAR, **cf.US_LIKE)
    base, _ = asy.base_from_prims(P)
    q = asy.poly_coeffs(base, lin.import_weights(base), D)
    out["grid_analogue"] = dict(beta_AB=beta_AB, qhat=asy.normalized(q).tolist(),
                                roots=asy.positive_roots(q).tolist())
    res = {}
    for label, aD in (("common_aD_0.8", np.full(3, 0.8)),
                      ("us_home_share_0.673", np.array([0.673, 0.8, 0.8]))):
        P, base = calibrate(L, b, aD)
        q = asy.poly_coeffs(base, lin.import_weights(base), D)
        qC = asy.poly_coeffs(base, np.array([0.0, 1.0]), D)
        res[label] = dict(beta=P.beta.tolist(), h=base["h"].tolist(), y=base["y"].tolist(),
                          qhat=asy.normalized(q).tolist(), roots=asy.positive_roots(q).tolist(),
                          bystander_roots=asy.positive_roots(qC).tolist(),
                          mml=lin.mml(lin.reduced_jacobian(base)))
    out["calibrated_network"] = res
    print(json.dumps(out, indent=1, default=str))
    json.dump(out, open(os.path.join(HERE, "..", "results", "us_china_row.json"), "w"), indent=1,
              default=str)


if __name__ == "__main__":
    main()
