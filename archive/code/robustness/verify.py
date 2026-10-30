# -*- coding: utf-8 -*-
"""Setup verification (task 2).

V1  symbolic linearization at the symmetric free-trade baseline reproduces
    (25), (48)-(52) for N = 2..5 and (57) for N = 3
V2  exact N = 3 responses converge to (57) as tau -> 0
V3  exact N = 2 solver at eta = 1 matches (41)
V4  sympy and complex-step linearizations agree at a random asymmetric
    baseline with tariffs (validates both tools away from symmetry)
Writes results/verify.json.  Exits non-zero on any discrepancy.
"""
import json
import os
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(__file__))
import model as M

OUT = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(OUT, exist_ok=True)
res = {}
ok_all = True


def check(name, cond, detail=""):
    global ok_all
    ok_all &= bool(cond)
    print("%-6s %-60s %s" % ("PASS" if cond else "FAIL", name, detail))
    res[name] = dict(ok=bool(cond), detail=str(detail))


# ------------------------------------------------------------------- V1
aD, aT, eta, rho = sp.symbols("alpha_D alpha_T eta rho", positive=True)
m = aT * (1 - aD)
rD = aD * eta + (1 - aD) * (1 - aT)
for N in (2, 3, 4, 5):
    Jt0, G, S = M.symbolic_linearization(
        N, tariffs=[(0, j) for j in range(1, N)],
        at=lambda S_: M.symmetric_subs(S_, N, aD, aT, eta, rho))
    MNs = (N * aD * (eta - 1) + (N - 2) * rho + 1) / (N - 1)
    off_ok = all(sp.simplify(Jt0[i, l] - m * MNs / (N - 1)) == 0
                 for i in range(N) for l in range(N) if i != l)
    dia_ok = all(sp.simplify(Jt0[i, i] + m * MNs) == 0 for i in range(N))
    check("(48) full Jacobian, N=%d" % N, off_ok and dia_ok)
    # tariff disturbance (49): t_j = dtau_{A j}
    t = sp.symbols("t1:%d" % N)
    tbar = sum(t) / (N - 1)
    GA = sp.Matrix(N, N - 1, lambda i, j: G[(0, j + 1)][i])
    F = GA * sp.Matrix(t)
    if N == 2:
        # (25): dTB_A = m M_2 dnu_B + m rho_D dtau
        ok25 = (sp.simplify(F[0] - m * rD * t[0]) == 0 and
                sp.simplify(Jt0[0, 1] - m * (1 + 2 * aD * (eta - 1))) == 0)
        check("(25) two-country linearization", ok25)
        continue
    ok49 = all(sp.simplify(F[i] - m / (N - 1) * (-rD * tbar - rho * (t[i - 1] - tbar))) == 0
               for i in range(1, N))
    check("(49) disturbance at unchanged rates, N=%d" % N, ok49)
    Gp = GA[1:, :]                                      # partners' rows
    one = sp.ones(N - 1, 1)
    gS = sp.simplify((Gp * one)[0])
    v = sp.zeros(N - 1, 1); v[0], v[1] = 1, -1
    gD = sp.simplify((Gp * v)[0])
    check("(50) g_S, g_D, N=%d" % N,
          sp.simplify(gS + m * rD / (N - 1)) == 0 and sp.simplify(gD + m * rho / (N - 1)) == 0
          and all(sp.simplify((Gp * one)[i] - gS) == 0 for i in range(N - 1)))
    J = Jt0[1:, 1:]
    c = m * MNs / (N - 1)
    ok51 = sp.simplify(-J - c * (N * sp.eye(N - 1) - one * one.T)) == sp.zeros(N - 1)
    check("(51) -J = c(NI - 11'), N=%d" % N, ok51)
    jS = sp.simplify((-J * one)[0]); jD = sp.simplify((-J * v)[0])
    check("(52) j_S, j_D, N=%d" % N,
          sp.simplify(jS - c) == 0 and sp.simplify(jD - N * c) == 0)
    if N == 3:
        dnu = (-J).LUsolve(GA[1:, :] * sp.Matrix([1, 0]))
        M3 = (3 * aD * (eta - 1) + rho + 1) / 2
        ok57 = (sp.simplify(dnu[0] + (rho + 3 * rD) / (6 * M3)) == 0 and
                sp.simplify(dnu[1] - (rho - 3 * rD) / (6 * M3)) == 0 and
                sp.simplify(dnu[1] - dnu[0] - rho / (3 * M3)) == 0)
        check("(57) N=3 slopes e_AB, e_AC, e_BC", ok57)

# ------------------------------------------------------------------- V2
cal = dict(aD=0.7, aT=0.6, eta=1.5)
rD_ = M.rhoD(cal["aD"], cal["aT"], cal["eta"])
rows = []
for r in (1.5, 3.51, 5.0, 8.0):
    P = M.symmetric(3, rho=r, **cal)
    M3 = M.MN(3, cal["aD"], cal["eta"], r)
    sB, sC = -(r + 3 * rD_) / (6 * M3), (r - 3 * rD_) / (6 * M3)
    errs = []
    for tau in (1e-1, 1e-2, 1e-3, 1e-4):
        T = np.zeros((3, 3)); T[0, 1] = tau
        nu = M.solve(P, T)
        errs.append((tau, nu[0] / tau - sB, nu[1] / tau - sC))
    rows.append(dict(rho=r, errs=errs))
    # error must shrink linearly in tau
    e = np.array([[abs(a), abs(b)] for _, a, b in errs])
    ratio = e[-2] / np.maximum(e[-1], 1e-300)
    conv = np.all(e[-1] < 1e-3) and np.all((ratio > 8) | (e[-1] < 1e-9))
    check("(57) exact N=3 converges, rho=%.2f" % r, conv,
          "err at tau=1e-4: (%.2e, %.2e)" % tuple(e[-1]))
res["V2_table"] = rows

# ------------------------------------------------------------------- V3
P2 = M.Primitives(N=2, L=[2.0, 1.0], AT=[1.3, 0.8], aD=0.7, aT=0.6, eta=1.0, rho=3.0)
m2 = 0.6 * 0.3
worst = 0.0
for tau in (0.05, 0.25, 0.5, 1.0, 2.0, 5.0):
    T = np.zeros((2, 2)); T[0, 1] = tau
    nu = M.solve(P2, T)
    closed = np.log(1.3 * 2.0 / (0.8 * 1.0) / (1 + (1 - m2) * tau))
    worst = max(worst, abs(nu[0] - closed))
check("(41) N=2 Cobb-Douglas exact solution", worst < 1e-12, "max |error| = %.1e" % worst)

# ------------------------------------------------------------------- V4
rng = np.random.default_rng(0)
N = 3
beta = np.zeros((N, N))
for i in range(N):
    js = [j for j in range(N) if j != i]
    b = rng.uniform(0.2, 0.8)
    beta[i, js] = [b, 1 - b]
tau = np.zeros((N, N)); tau[0, 1], tau[0, 2], tau[1, 0] = 0.3, 0.1, 0.2
P = M.Primitives(N=3, L=rng.uniform(1, 5, 3), AT=rng.uniform(0.5, 2, 3),
                 aT=rng.uniform(0.4, 0.7, 3), aD=rng.uniform(0.5, 0.9, 3),
                 eta=rng.uniform(1, 3, 3), rho=rng.uniform(1.5, 6, 3), beta=beta, tau=tau)
nu = M.solve(P)
J_cs, Jt_cs, G_cs = M.linearize(P, nu)
_, S = M.symbolic_model(N)
sub = {}
for i in range(N):
    sub.update({S["nu"][i]: M.full(nu)[i], S["L"][i]: P.L[i], S["AT"][i]: P.AT[i],
                S["aT"][i]: P.aT[i], S["aD"][i]: P.aD[i], S["eta"][i]: P.eta[i],
                S["rho"][i]: P.rho[i]})
for (i, j) in S["tau"]:
    sub[S["tau"][i, j]] = P.tau[i, j]
    sub[S["beta"][i, j]] = P.beta[i, j]
sub = {k: sp.Float(v, 30) for k, v in sub.items()}
Jt_s, G_s, _ = M.symbolic_linearization(N, at=lambda S_: sub)
Jt_num = np.array(Jt_s.evalf(), float)
G_num = np.array([[[float(G_s[(j, k)][i].evalf()) if j != k else 0.0
                    for k in range(N)] for j in range(N)] for i in range(N)])
d = max(np.max(np.abs(Jt_num - Jt_cs)), np.max(np.abs(G_num - G_cs)))
check("sympy vs complex-step at asymmetric baseline with tariffs", d < 1e-10, "max diff %.1e" % d)
# row identity of (10): sum_l Jtilde_il = TB_i = 0 at a balanced baseline
check("(10) homogeneity rows sum to zero", np.max(np.abs(Jt_cs.sum(1))) < 1e-10,
      "%.1e" % np.max(np.abs(Jt_cs.sum(1))))
check("(10) Walras columns sum to zero", np.max(np.abs(Jt_cs.sum(0))) < 1e-10,
      "%.1e" % np.max(np.abs(Jt_cs.sum(0))))

json.dump(res, open(os.path.join(OUT, "verify.json"), "w"), indent=1, default=float)
print("\nALL CHECKS PASSED" if ok_all else "\nDISCREPANCY FOUND")
sys.exit(0 if ok_all else 1)
