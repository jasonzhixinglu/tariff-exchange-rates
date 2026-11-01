"""Appendix D: robustness of the bystander threshold to (D.2) diminishing
returns in tradables (Ricardo-Viner) and (D.3) a permanent transfer-financed
trade imbalance, from the exact model in model/extensions.py.

US-like calibration (aD, aT, eta) = (0.8, 0.4, 1.5), N = 3, A = 0 levies the
tariff on B = 1, bystander C = 2; primitives symmetric unless stated (L = 1,
A_T = A_N = 1, beta = 1/2).  The baseline is re-solved from primitives at each
rho.  Roots are located by scanning rho on a log grid over [1.05, 60] and
refining every sign change with brentq.
Writes code/results/appendix_d.json.
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from model import closed_forms as cf  # noqa: E402
from model import extensions as ex  # noqa: E402
from model import linear as lin  # noqa: E402
from model import nested_ces as nc  # noqa: E402

CAL = cf.US_LIKE
N = 3
A, B, C = 0, 1, 2
RHO_LO, RHO_HI = 1.05, 60.0
DEFICIT = 0.03
TAU_BIG = 1.45


def d_unilateral():
    d = np.zeros((N, N)); d[A, B] = 1.0
    return d


def prims(rho, L=(1.0, 1.0, 1.0)):
    return nc.symmetric(N, rho=rho, L=np.array(L, float), **CAL)


def transfer_for(P, payer, gamma=1.0):
    """A receives DEFICIT x its no-transfer free-trade income (A's currency),
    paid by `payer`; None for balanced trade."""
    return None if payer is None else ex.transfer(P, A, payer, DEFICIT, gamma)


# ------------------------------------------------------------ marginal
def marginal(rho, gamma=1.0, L=(1.0, 1.0, 1.0), payer=None, extra=False):
    """d nu / d log(1+tau_AB) at the (re-solved) free-trade baseline."""
    P = prims(rho, L)
    T = transfer_for(P, payer, gamma)
    nu, LT = ex.solve(P, None, gamma, T)
    tau = np.zeros((N, N))
    lr = ex.local_response(P, tau, nu, LT, d_unilateral(), gamma, T)
    if not extra:
        return lr["dnu"][C - 1]
    dlogV = ex.total_derivative(lambda a, nf: a["logV"], P, tau, nu, LT,
                                d_unilateral(), gamma, T)
    dlogq = ex.total_derivative(lambda a, nf: nf + np.log(a["P"]) - np.log(a["P"][A]),
                                P, tau, nu, LT, d_unilateral(), gamma, T)
    return dict(dnu_B=lr["dnu"][B - 1], dnu_C=lr["dnu"][C - 1],
                neer_equal_weight=float(np.mean(lr["dnu"])),
                dlogV_A=dlogV[A], dlogq_AC=dlogq[C], mml=lin.mml(lr["J"]))


def marginal_real(rho, gamma=1.0, L=(1.0, 1.0, 1.0), payer=None):
    return marginal(rho, gamma, L, payer, extra=True)["dlogq_AC"]


# ------------------------------------------------------------ discrete
def discrete(rho, payer=None, real=False, tau=TAU_BIG):
    """log e_AC (or log q_AC) at tau_AB = tau minus its value at tau = 0,
    both at the same (transfer) baseline; continuation in tau."""
    P = prims(rho)
    T = transfer_for(P, payer)
    t = np.zeros((N, N)); t[A, B] = tau
    out = []
    nu, LT = ex.solve(P, None, 1.0, T)
    for tt, (nu1, LT1) in ((0.0, (nu, LT)), (tau, ex.solve_path(P, t, 1.0, T, nu0=nu, LT0=LT))):
        tauv = tt * d_unilateral()
        nf = nc.full(nu1)
        a = ex.allocation(nf, LT1, P, tauv, 1.0, T)
        out.append(nf[C] + (np.log(a["P"][C].real) - np.log(a["P"][A].real) if real else 0.0))
    return out[1] - out[0]


# ------------------------------------------------------------ roots
def roots_on_grid(f, n=60, lo=RHO_LO, hi=RHO_HI):
    grid = np.exp(np.linspace(np.log(lo), np.log(hi), n))
    vals = np.array([f(r) for r in grid])
    roots = []
    for a, b, fa, fb in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if np.sign(fa) != np.sign(fb):
            r = brentq(f, a, b, xtol=1e-11)
            roots.append(dict(rho=r, crossing="neg_to_pos" if fb > fa else "pos_to_neg"))
    return dict(roots=roots, n_roots=len(roots), sign_at_lo=float(np.sign(vals[0])),
                sign_at_hi=float(np.sign(vals[-1])))


def first_root(res):
    return res["roots"][0]["rho"] if res["roots"] else None


def marginal_threshold(gamma=1.0, L=(1.0, 1.0, 1.0), payer=None, n=60):
    res = roots_on_grid(lambda r: marginal(r, gamma, L, payer), n=n)
    for rt in res["roots"]:
        info = marginal(rt["rho"], gamma, L, payer, extra=True)
        rt.update(mml=info["mml"], dnu_B=info["dnu_B"], neer_equal_weight=info["neer_equal_weight"],
                  dlogV_A=info["dlogV_A"])
    return res


def mml_at(rho, payer=None, tau=0.0, gamma=1.0, L=(1.0, 1.0, 1.0)):
    """MML (def:mml) for the reduced Jacobian at the equilibrium with
    tau_AB = tau (re-solved from primitives, continuation in tau)."""
    P = prims(rho, L)
    T = transfer_for(P, payer, gamma)
    nu, LT = ex.solve(P, None, gamma, T)
    t = np.zeros((N, N))
    if tau:
        t[A, B] = tau
        nu, LT = ex.solve_path(P, t, gamma, T, nu0=nu, LT0=LT)
    J = ex.local_response(P, t, nu, LT, d_unilateral(), gamma, T)["J"]
    return lin.mml(J)


def add_mml(res, payer=None, tau=0.0):
    for rt in res["roots"]:
        rt["mml_baseline"] = mml_at(rt["rho"], payer)
        if tau:
            rt["mml_at_tau"] = mml_at(rt["rho"], payer, tau)
    return res


# ------------------------------------------------------------ D.2 analytics
def kappa_rv(gamma, aT):
    """Multiplier on A's income response to its own tariff at fixed nu
    (free trade, Cobb-Douglas upper tier, Ricardo-Viner tradables):
    d log E_A / d log(1+tau_AB) = kappa * s_AB, kappa = 1 at gamma = 1."""
    return 1.0 + (1 - aT) ** 2 * (1 - gamma) / (aT * (1 - aT + gamma * aT))


def rhoD_rv(gamma, aD, aT, eta):
    """Domestic diversion margin with Ricardo-Viner tradables."""
    return aD * eta + (1 - aD) * (1 - aT) * gamma / (1 - aT + gamma * aT)


def rv_diagnostics():
    """(i) closed-form income response and symmetric threshold vs the exact
    model; (ii) J at gamma < 1 equals the gamma = 1 J at equal nominal
    incomes (checked at an asymmetric L); (iii) size-only counterpart of the
    small-bystander case."""
    out = {}
    aD, aT, eta = CAL["aD"], CAL["aT"], CAL["eta"]
    for g in (0.9, 0.75, 2 / 3, 0.5):
        diag = baseline_diag(4.0, g)
        out["%.4g" % g] = dict(kappa=kappa_rv(g, aT),
                               dlogE_closed=kappa_rv(g, aT) * cf.m(aD, aT) / (N - 1),
                               dlogE_exact=diag["dlogE_A_fixed_nu"],
                               threshold_closed=N * rhoD_rv(g, aD, aT, eta))
    # J equivalence at L = (1, 1, 0.1), gamma = 0.5, rho = 4
    g, L = 0.5, (1.0, 1.0, 0.1)
    P = prims(4.0, L)
    nu, LT = ex.solve(P, None, g)
    a = ex.allocation(nc.full(nu), LT, P, np.zeros((N, N)), g)
    J_rv = ex.local_response(P, np.zeros((N, N)), nu, LT, d_unilateral(), g)["J"]
    Leq = a["GDP"].real / P.AT                     # gamma = 1 labor with equal GDP
    P1 = prims(4.0, tuple(Leq))
    nu1, LT1 = ex.solve(P1, None, 1.0)
    J_lin = ex.local_response(P1, np.zeros((N, N)), nu1, LT1, d_unilateral(), 1.0)["J"]
    out["J_equivalence_LC0.1_gamma0.5"] = dict(
        max_abs_diff=float(np.max(np.abs(J_rv - J_lin))), nu_diff=float(np.max(np.abs(nu - nu1))),
        income_ratio_C_to_A=float(a["GDP"].real[C] / a["GDP"].real[A]))
    # size-only counterpart: linear technology, bystander labor set so that
    # its income relative to A matches the gamma-economy (L_C^gamma scaling)
    size_only = {}
    for gg in (2 / 3, 0.5):
        P = prims(4.0, L, )
        nu, LT = ex.solve(P, None, gg)
        GDP = ex.allocation(nc.full(nu), LT, P, np.zeros((N, N)), gg)["GDP"].real
        LC = GDP[C] / GDP[A]
        size_only["%.4g" % gg] = dict(LC_equiv=LC, threshold_linear=first_root(
            marginal_threshold(1.0, L=(1.0, 1.0, LC), n=80)))
    out["small_bystander_size_only"] = size_only
    return out


# ------------------------------------------------------------ diagnostics
def baseline_diag(rho, gamma=1.0, payer=None, L=(1.0, 1.0, 1.0)):
    """Baseline shares that enter the linearization, plus the pieces of the
    first-order system (reduced J and the disturbance at fixed nu)."""
    P = prims(rho, L)
    T = transfer_for(P, payer, gamma)
    nu, LT = ex.solve(P, None, gamma, T)
    tau = np.zeros((N, N))
    a = ex.allocation(nc.full(nu), LT, P, tau, gamma, T)
    s = a["s"].real
    f = a["f"].real
    lr = ex.local_response(P, tau, nu, LT, d_unilateral(), gamma, T)
    n = N - 1
    # disturbance with L_T re-optimized at fixed nu (Schur complement)
    Jf, G = lr["Jfull"], lr["G"]
    Gred = G[:n] - Jf[:n, n:] @ np.linalg.solve(Jf[n:, n:], G[n:])
    # d log E_A at fixed nu (A's expenditure response to its own tariff)
    dz = -np.linalg.solve(Jf[n:, n:], G[n:])
    x = np.concatenate([nu, ex._z_of(LT, P.L)])

    def logE(xc, tc):
        nf, lt = ex._unpack(xc, P)
        return np.log(ex.allocation(nf, lt, P, tc, gamma, T)["E"])
    h = 1e-30
    xc = x.astype(complex); dE_z = ex._jac_cs(lambda y: logE(y, tau), x)[:, n:] @ dz
    dE_t = np.imag(logE(xc, tau + 1j * h * d_unilateral())) / h
    return dict(nu=nu.tolist(), LT=LT.tolist(), T=(None if T is None else T.tolist()),
                expenditure_A_currency=a["Et"].real.tolist(),
                import_share_of_expenditure=[float(1 - s[i, i] / P.aT[i]) * float(P.aT[i])
                                             for i in range(N)],
                home_share_in_tradables=[float(s[i, i] / P.aT[i]) for i in range(N)],
                A_import_origin_share_C=float(s[A, C] / (s[A, B] + s[A, C])),
                C_exports_to_A_over_C_exports=float(f[C, A] / (f[C, A] + f[C, B])),
                J_reduced=lr["J"].tolist(), G_reduced=Gred.tolist(),
                dlogE_A_fixed_nu=float((dE_z + dE_t)[A]))


def main():
    res = {"calibration": CAL, "rho_D": cf.rhoD(**CAL), "three_rho_D": 3 * cf.rhoD(**CAL)}

    # D.2 (a) symmetric point, Ricardo-Viner
    d2a = {}
    for g in (1.0, 0.9, 0.75, 2 / 3, 0.5):
        d2a["%.4g" % g] = marginal_threshold(g)
    res["D2a_symmetric"] = d2a
    res["D2a_diag_rho4"] = {"%.4g" % g: baseline_diag(4.0, g) for g in (1.0, 0.5)}

    # D.2 (b) small bystander L_C = 0.1
    d2b = {}
    for g in (1.0, 2 / 3, 0.5):
        d2b["%.4g" % g] = marginal_threshold(g, L=(1.0, 1.0, 0.1), n=80)
    res["D2b_small_bystander_LC_0.1"] = d2b
    res["D2_analytics"] = rv_diagnostics()

    # D.3 (a) deficit 3% of A's income, counterpart on B or C
    res["D3a_deficit_marginal"] = {"balanced": marginal_threshold(),
                                   "payer_B": marginal_threshold(payer=B),
                                   "payer_C": marginal_threshold(payer=C)}
    global DEFICIT
    sens = {}
    for share in (0.01, -0.01, -0.03):
        DEFICIT = share
        sens["%+.2f" % share] = {k: first_root(marginal_threshold(payer=p, n=30))
                                 for k, p in (("payer_B", B), ("payer_C", C))}
    DEFICIT = 0.03
    res["D3a_deficit_size_sensitivity"] = sens
    res["D3a_diag_rho4"] = {k: baseline_diag(4.0, payer=p)
                            for k, p in (("balanced", None), ("payer_B", B), ("payer_C", C))}

    # D.3 (b) discrete tau_AB = 1.45: real and nominal, balanced and deficit
    d3b = {}
    for k, p in (("balanced", None), ("payer_B", B), ("payer_C", C)):
        d3b[k] = dict(
            real_discrete=add_mml(roots_on_grid(lambda r: discrete(r, p, real=True), n=30),
                                  p, TAU_BIG),
            nominal_discrete=add_mml(roots_on_grid(lambda r: discrete(r, p, real=False), n=30),
                                     p, TAU_BIG),
            real_marginal=add_mml(roots_on_grid(lambda r: marginal_real(r, payer=p), n=40), p))
        d3b[k]["mml_baseline_on_grid"] = all(
            mml_at(r, p) for r in np.exp(np.linspace(np.log(RHO_LO), np.log(RHO_HI), 15)))
    d3b["rho_q_star_closed_form_balanced"] = cf.rho_q_star(N, **CAL)
    d3b["appendix_c_nominal_1.45_reference"] = 2.7004127363225012
    res["D3b_discrete_tau_1.45"] = d3b

    out = os.path.join(HERE, "..", "results", "appendix_d.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1, default=float)
    summary(res)


def _r(x):
    def tag(r):
        k = "mml" if "mml" in r else "mml_baseline" if "mml_baseline" in r else None
        s = "" if k is None else ",MML" if r[k] else ",noMML"
        if "mml_at_tau" in r:
            s += ",MML@tau" if r["mml_at_tau"] else ",noMML@tau"
        return s
    return ", ".join("%.4f(%s%s)" % (r["rho"], r["crossing"], tag(r))
                     for r in x["roots"]) or "none (sign %+d on [1.05,60])" % x["sign_at_lo"]


def summary(res):
    print("3 rho_D = %.4f" % res["three_rho_D"])
    print("D.2(a) symmetric, bystander threshold by gamma:")
    for g, v in res["D2a_symmetric"].items():
        rt = v["roots"][0] if v["roots"] else {}
        print("  gamma=%-6s rho* = %s  neer=%.4g dlogV_A=%.4g" % (
            g, _r(v), rt.get("neer_equal_weight", np.nan), rt.get("dlogV_A", np.nan)))
    print("D.2(b) L_C = 0.1:")
    for g, v in res["D2b_small_bystander_LC_0.1"].items():
        print("  gamma=%-6s rho* = %s" % (g, _r(v)))
    print("D.3(a) deficit 3%:")
    for k, v in res["D3a_deficit_marginal"].items():
        print("  %-9s rho* = %s" % (k, _r(v)))
    print("  sensitivity to T_A/I_A (negative = A surplus):",
          json.dumps(res["D3a_deficit_size_sensitivity"]))
    print("D.3(b) tau_AB = 1.45:")
    for k in ("balanced", "payer_B", "payer_C"):
        v = res["D3b_discrete_tau_1.45"][k]
        print("  %-9s real discrete %s | nominal discrete %s | real marginal %s" % (
            k, _r(v["real_discrete"]), _r(v["nominal_discrete"]), _r(v["real_marginal"])))
    print("  rho_q_star closed form (balanced, marginal real) = %.4f"
          % res["D3b_discrete_tau_1.45"]["rho_q_star_closed_form_balanced"])
    print("  MML at baseline on rho grid:", {k: res["D3b_discrete_tau_1.45"][k]["mml_baseline_on_grid"]
                                            for k in ("balanced", "payer_B", "payer_C")})
    print("D.2 analytics:", json.dumps(res["D2_analytics"], indent=1, default=float))


if __name__ == "__main__":
    main()
