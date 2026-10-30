# -*- coding: utf-8 -*-
"""Task D: NEER and ordering check at asymmetric free-trade baselines, N = 3.

Unilateral tariff by A on B (first order).  For each draw:
  * solve the free-trade equilibrium (baseline re-solved, shares never set)
  * J, F by complex step; keep the draw only if MML (8) holds:
        J_il >= 0 (l != i)  and  (-J)^{-1} >= 0 elementwise
  * (i)  NEER   dnu_A^E = w_AB dnu_B + w_AC dnu_C,  weights of eq. (21)
  * (ii) order  dnu_B - dnu_C
Margins are reported raw (log change per unit tariff) and scale-free,
divided by max(|dnu_B| + |dnu_C|, 0.1); the floor stops the search from
rewarding points where both responses vanish.

Search box: L_i log-uniform on [1, 10]; beta_ij in [0.1, 0.9] (A_T = 1);
alpha_D in [0.5, 0.9]; eta in [1, 4]; rho in [1, 10]; alpha_T = 0.6.
Variant "common": alpha_D, eta, rho common to all countries.
Variant "country": alpha_D, eta, rho drawn separately for each country.
Random draws, then differential evolution on each margin.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import differential_evolution

sys.path.insert(0, os.path.dirname(__file__))
import model as M

HERE = os.path.dirname(__file__)
DIRECTION = np.zeros((3, 3)); DIRECTION[0, 1] = 1.0


def unpack(z, variant):
    """z in the unit cube -> primitives."""
    z = np.asarray(z, float)
    L = 10 ** z[0:3]
    beta = np.zeros((3, 3))
    for i, b in enumerate(0.1 + 0.8 * z[3:6]):
        js = [j for j in range(3) if j != i]
        beta[i, js] = [b, 1 - b]
    if variant == "common":
        aD, eta, rho = 0.5 + 0.4 * z[6], 1 + 3 * z[7], 1 + 9 * z[8]
    else:
        aD, eta, rho = 0.5 + 0.4 * z[6:9], 1 + 3 * z[9:12], 1 + 9 * z[12:15]
    return M.Primitives(N=3, L=L, AT=1.0, aT=0.6, aD=aD, eta=eta, rho=rho, beta=beta)


DIM = {"common": 9, "country": 15}


def evaluate(P):
    nu = M.solve(P)
    J, Jt, Gf = M.linearize(P, nu)
    F = Gf[1:, 0, 1]
    dnu = np.linalg.solve(-J, F)
    ok, why = M.mml_holds(J)
    w = M.neer_weights(P, nu)
    neer = w[1] * dnu[0] + w[2] * dnu[1]
    order = dnu[0] - dnu[1]
    scale = max(abs(dnu[0]) + abs(dnu[1]), 0.1)   # floor avoids rewarding tiny responses
    gs = bool(np.all(Jt - np.diag(np.diag(Jt)) >= -1e-12))     # gross substitutability
    return dict(mml=ok, why=why, gs=gs, neer=neer, order=order, neer_n=neer / scale,
                order_n=order / scale, dnuB=dnu[0], dnuC=dnu[1], w=w[1:], F=F, nu0=nu)


def describe(P):
    return dict(L=P.L.round(4).tolist(), beta_AB=round(P.beta[0, 1], 4), beta_BA=round(P.beta[1, 0], 4),
                beta_CA=round(P.beta[2, 0], 4), aD=np.round(P.aD, 4).tolist(),
                eta=np.round(P.eta, 4).tolist(), rho=np.round(P.rho, 4).tolist())


def exact_check(P, tau=0.01):
    """Finite-tariff confirmation of the first-order signs."""
    nu0 = M.solve(P)
    T = np.zeros((3, 3)); T[0, 1] = tau
    nu1 = M.solve(P, T, nu0=nu0)
    w = M.neer_weights(P, nu0)
    d = nu1 - nu0
    return dict(neer=float(w[1] * d[0] + w[2] * d[1]), order=float(d[0] - d[1]))


if __name__ == "__main__":
    rng = np.random.default_rng(20260922)
    out = {}
    # "draws" runs the random draws only (no targeted search); a variant name
    # restricts the run to that variant
    draws_only = "draws" in sys.argv[1:]
    variants = [v for v in ("common", "country") if v in sys.argv[1:]] or ["common", "country"]
    for variant in variants:
        t0 = time.time()
        n_draw = 20000
        rec = []
        n_fail = 0
        for k in range(n_draw):
            z = rng.random(DIM[variant])
            P = unpack(z, variant)
            try:
                r = evaluate(P)
            except Exception:
                n_fail += 1
                continue
            rec.append((z, r))
        kept = [(z, r) for z, r in rec if r["mml"]]
        print("%s: %d draws, %d solver failures, %d satisfy MML (%.0fs)"
              % (variant, n_draw, n_fail, len(kept), time.time() - t0))
        why = {}
        for z, r in rec:
            why[r["why"]] = why.get(r["why"], 0) + 1
        neer = np.array([r["neer"] for _, r in kept])
        order = np.array([r["order"] for _, r in kept])
        neer_n = np.array([r["neer_n"] for _, r in kept])
        order_n = np.array([r["order_n"] for _, r in kept])
        gs_share = np.mean([r["gs"] for _, r in kept])
        summ = dict(draws=n_draw, solver_failures=n_fail, mml_kept=len(kept), mml_reasons=why,
                    gs_share_among_kept=float(gs_share),
                    neer_positive=int(np.sum(neer > 0)), order_positive=int(np.sum(order > 0)),
                    neer_max=float(neer.max()), neer_n_max=float(neer_n.max()),
                    order_max=float(order.max()), order_n_max=float(order_n.max()),
                    neer_quantiles=np.quantile(neer_n, [0, .5, .99, 1]).tolist(),
                    order_quantiles=np.quantile(order_n, [0, .5, .99, 1]).tolist())
        # draws that violate MML: do they break the claims?
        bad = [(z, r) for z, r in rec if not r["mml"]]
        summ["non_mml_neer_positive"] = int(sum(r["neer"] > 0 for _, r in bad))
        summ["non_mml_order_positive"] = int(sum(r["order"] > 0 for _, r in bad))
        # what the counterexamples have in common
        rho_A = lambda z: float(np.atleast_1d(unpack(z, variant).rho)[0])
        eta_A = lambda z: float(np.atleast_1d(unpack(z, variant).eta)[0])
        cx = {}
        for key in ("neer", "order"):
            pos = [(z, r) for z, r in kept if r[key] > 0]
            if not pos:
                continue
            cx[key] = dict(
                n=len(pos),
                rho_A_min=min(rho_A(z) for z, _ in pos), rho_A_median=float(np.median([rho_A(z) for z, _ in pos])),
                eta_A_median=float(np.median([eta_A(z) for z, _ in pos])),
                share_dnuC_positive=float(np.mean([r["dnuC"] > 0 for _, r in pos])),
                w_AC_median=float(np.median([r["w"][1] for _, r in pos])),
                w_AC_min=float(min(r["w"][1] for _, r in pos)),
                share_FC_negative=float(np.mean([r["F"][1] < 0 for _, r in pos])),
                share_FB_negative=float(np.mean([r["F"][0] < 0 for _, r in pos])),
                equal_weight_avg_positive=float(np.mean([(r["dnuB"] + r["dnuC"]) > 0 for _, r in pos])))
        # among all kept draws: how often does the bystander rate reverse?
        cx["all_share_dnuC_positive"] = float(np.mean([r["dnuC"] > 0 for _, r in kept]))
        cx["all_share_dnuB_positive"] = float(np.mean([r["dnuB"] > 0 for _, r in kept]))
        summ["counterexample_profile"] = cx
        print("  profile", json.dumps(cx))
        for key in ("neer_n", "order_n"):
            zb, rb = max(kept, key=lambda zr: zr[1][key])
            summ["closest_random_" + key] = dict(value=rb[key], raw=rb[key.split("_")[0]],
                                                 params=describe(unpack(zb, variant)))
        print("  NEER>0: %d   order>0: %d   max NEER/scale %.4f   max order/scale %.4f"
              % (summ["neer_positive"], summ["order_positive"], summ["neer_n_max"], summ["order_n_max"]))

        # ------------------------------------------ targeted search
        for key in (() if draws_only else ("neer", "order", "neer_n", "order_n")):
            def obj(z):
                try:
                    r = evaluate(unpack(z, variant))
                except Exception:
                    return 10.0
                if not r["mml"]:
                    return 5.0
                return -r[key]
            seed = sorted(kept, key=lambda zr: -zr[1][key])[:40]
            init = np.array([z for z, _ in seed] + [rng.random(DIM[variant]) for _ in range(20)])
            t1 = time.time()
            de = differential_evolution(obj, [(0, 1)] * DIM[variant], init=init, maxiter=150,
                                        tol=1e-10, seed=1, polish=True, updating="deferred")
            P = unpack(de.x, variant)
            r = evaluate(P)
            ex = exact_check(P)
            summ["optimum_" + key] = dict(value=float(-de.fun), raw=float(r[key.split("_")[0]]),
                                          dnuB=float(r["dnuB"]), dnuC=float(r["dnuC"]),
                                          weights=r["w"].tolist(), mml=bool(r["mml"]),
                                          exact_tau_0_01=ex, params=describe(P),
                                          scale_free=float(r[key.split("_")[0] + "_n"]),
                                          on_boundary=[int(i) for i in np.where((de.x < 1e-3) | (de.x > 1 - 1e-3))[0]])
            print("  DE max %s = %.5f (raw %.5f), exact check %s, %.0fs"
                  % (key, -de.fun, r[key.split("_")[0]], ex, time.time() - t1))
            print("     params", describe(P))
        out[variant] = summ
        json.dump(out, open(os.path.join(HERE, "results", "task_d%s.json" % ("_draws" if draws_only else "")), "w"),
                  indent=1, default=float)

        # store the kept draws compactly for the figure
        np.savez(os.path.join(HERE, "results", "task_d_%s.npz" % variant),
                 neer_n=neer_n, order_n=order_n, neer_raw=neer, order_raw=order,
                 bAB=np.array([unpack(z, variant).beta[0, 1] for z, _ in kept]),
                 rho=np.array([np.atleast_1d(unpack(z, variant).rho)[0] for z, _ in kept]))
    print("done")
