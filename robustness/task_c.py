# -*- coding: utf-8 -*-
"""Task C: first-order asymmetry sensitivities of the bystander threshold,
N = 3, at the symmetric free-trade baseline with rho = 3 rho_D.

S(rho; x) = d nu_C / d tau_AB at the free-trade equilibrium of primitives x
(the baseline is re-solved for every x; shares are never perturbed directly).
rho*(x) solves S = 0, so  d rho*/dx = -S_x / S_rho,  S_rho = 1/(6 M_3).

Analytic route (sympy).  With S = e_C'(-J)^{-1} F,
    dS = e_C'(-J)^{-1} [ dF + dJ (-J)^{-1} F ],
    dJ = J_x + sum_l J_{nu_l} dnu0_l/dx,   dF likewise,
    dnu0/dx = -J^{-1} TB_x          (the baseline moves with x).
Only second derivatives of TB are needed.  Checked against central finite
differences of rho*(x) computed with the exact solver.

Perturbations:
  beta_AB   A's weight on B, with beta_AC = 1 - beta_AB
  L_C       bystander labour endowment (size)
  L_B       target labour endowment (size)
  alpha_D^A home weight in A only
"""
import json
import os
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
import model as M
import style

HERE = os.path.dirname(__file__)
CAL = dict(aD=0.7, aT=0.6, eta=1.5)
NAMES = ["beta_AB", "L_C", "L_B", "alpha_D^A"]


# ----------------------------------------------------------- numeric route
def primitives(rho, x=None, h=0.0, cal=CAL):
    P = M.symmetric(3, rho=rho, **cal)
    if x == "beta_AB":
        b = P.beta.copy(); b[0, 1] += h; b[0, 2] -= h; P = P.with_(beta=b)
    elif x == "L_C":
        L = P.L.copy(); L[2] += h; P = P.with_(L=L)
    elif x == "L_B":
        L = P.L.copy(); L[1] += h; P = P.with_(L=L)
    elif x == "alpha_D^A":
        a = P.aD.copy(); a[0] += h; P = P.with_(aD=a)
    return P


def S(rho, x=None, h=0.0, cal=CAL):
    P = primitives(rho, x, h, cal)
    nu0 = M.solve(P)
    D = np.zeros((3, 3)); D[0, 1] = 1.0
    dnu, J, F = M.response(P, nu0, D)
    return dnu[1]


def rho_star(x=None, h=0.0, cal=CAL):
    """Root of S near 3 rho_D; the bracket widens until it straddles the root.
    nan if no root on (1, 100)."""
    r0 = 3 * M.rhoD(**cal)
    f = lambda r: S(r, x, h, cal)
    lo, hi = 0.8 * r0, 1.25 * r0
    while f(lo) > 0 and lo > 1.01:
        lo = max(1.01, lo * 0.8)
    while f(hi) < 0:
        hi *= 1.25
        if hi > 100:
            return float("nan")
    if f(lo) > 0:
        return float("nan")
    return brentq(f, lo, hi, xtol=1e-13)


def fd_derivative(x, cal=CAL):
    out = {}
    for h in (1e-2, 1e-3):
        out[h] = (rho_star(x, h, cal) - rho_star(x, -h, cal)) / (2 * h)
    # Richardson (central differences are O(h^2))
    rich = out[1e-3] + (out[1e-3] - out[1e-2]) / 99.0
    return out[1e-2], out[1e-3], rich


# ---------------------------------------------------------- symbolic route
def symbolic_sensitivities():
    aD, aT, eta, rho = sp.symbols("alpha_D alpha_T eta rho", positive=True)
    TB, Sy = M.symbolic_model(3)
    # tie beta_AC to beta_AB before differentiating
    TB = [e.xreplace({Sy["beta"][0, 2]: 1 - Sy["beta"][0, 1]}) for e in TB]
    xs = {"beta_AB": Sy["beta"][0, 1], "L_C": Sy["L"][2], "L_B": Sy["L"][1],
          "alpha_D^A": Sy["aD"][0]}
    base = M.symmetric_subs(Sy, 3, aD, aT, eta, rho)
    base.pop(Sy["beta"][0, 2])
    ev = lambda e: sp.simplify(e.xreplace(base))
    nu = [Sy["nu"][1], Sy["nu"][2]]
    tAB = Sy["tau"][0, 1]
    T = [TB[1], TB[2]]
    J = sp.Matrix(2, 2, lambda i, l: ev(sp.diff(T[i], nu[l])))
    F = sp.Matrix([ev(sp.diff(T[i], tAB)) for i in range(2)])
    Jinv = (-J).inv()
    dnu = sp.simplify(Jinv * F)
    eC = sp.Matrix([[0, 1]])
    res = {}
    for name, x in xs.items():
        TBx = sp.Matrix([ev(sp.diff(T[i], x)) for i in range(2)])
        dnu0 = sp.simplify(-J.inv() * TBx)                    # baseline shift
        dJ = sp.Matrix(2, 2, lambda i, l: ev(sp.diff(T[i], nu[l], x))
                       + sum(ev(sp.diff(T[i], nu[l], nu[k])) * dnu0[k] for k in range(2)))
        dF = sp.Matrix([ev(sp.diff(T[i], tAB, x))
                        + sum(ev(sp.diff(T[i], tAB, nu[k])) * dnu0[k] for k in range(2))
                        for i in range(2)])
        dS = (eC * Jinv * (dF + dJ * dnu))[0]
        M3 = (3 * aD * (eta - 1) + rho + 1) / 2
        rD = aD * eta + (1 - aD) * (1 - aT)
        drho = sp.factor(sp.simplify((-dS * 6 * M3).subs(rho, 3 * rD)))
        res[name] = drho
        print(name, ":", drho)
    return (aD, aT, eta), res




def draw_figure(out, sym, aD, aT, eta, rD):
    # figure: rho*(x)/3rho_D over a finite range of each primitive (baseline cal)
    fig, axes = plt.subplots(1, 4, figsize=(8.6, 2.5), sharey=True)
    ranges = {"beta_AB": (-0.3, 0.3), "L_C": (-0.6, 2.0), "L_B": (-0.6, 2.0), "alpha_D^A": (-0.2, 0.2)}
    base_val = {"beta_AB": 0.5, "L_C": 1.0, "L_B": 1.0, "alpha_D^A": 0.7}
    labels = {"beta_AB": r"$\beta_{AB}$", "L_C": r"$L_C$", "L_B": r"$L_B$", "alpha_D^A": r"$\alpha_D^A$"}
    curves = {}
    for ax, name in zip(axes, NAMES):
        hs = np.linspace(*ranges[name], 17)
        ys = np.array([rho_star(name, h) for h in hs]) / (3 * rD)
        a = float(sym[name].subs({aD: CAL["aD"], aT: CAL["aT"], eta: CAL["eta"]}))
        ax.plot(base_val[name] + hs, ys, color=style.SERIES[0], lw=1.7)
        ax.plot(base_val[name] + hs, 1 + a * hs / (3 * rD), color=style.SERIES[1], lw=0.9,
                ls=(0, (3, 2)))
        ax.axhline(1, color=style.MUTED, lw=0.6)
        ax.axvline(base_val[name], color=style.MUTED, lw=0.6)
        ax.set_xlabel(labels[name])
        style.finish(ax)
        curves[name] = dict(x=(base_val[name] + hs).tolist(), ratio=ys.tolist())
    axes[0].set_ylabel(r"$\rho^\ast/3\rho_D$")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "figures", "task_c_sensitivities.png"), dpi=200)
    out["curves"] = curves
    json.dump(out, open(os.path.join(HERE, "results", "task_c.json"), "w"), indent=1)
    print("figure written")


if __name__ == "__main__" and sys.argv[1:] == ["fig"]:
    # redraw the figure from saved closed forms, without redoing sympy
    out = json.load(open(os.path.join(HERE, "results", "task_c.json")))
    aD, aT, eta = sp.symbols("alpha_D alpha_T eta", positive=True)
    sym = {k: sp.sympify(v, locals=dict(alpha_D=aD, alpha_T=aT, eta=eta)) for k, v in out["symbolic"].items()}
    rD = M.rhoD(**CAL)
    draw_figure(out, sym, aD, aT, eta, rD)
elif __name__ == "__main__":
    (aD, aT, eta), sym = symbolic_sensitivities()
    rD = M.rhoD(**CAL)
    print("rho*(sym) = %.10f, 3 rho_D = %.10f" % (rho_star(), 3 * rD))
    out = {"rho_star_symmetric": rho_star(), "three_rhoD": 3 * rD, "rows": []}
    cals = {"baseline": CAL, "US-like": dict(aD=0.8, aT=0.4, eta=1.5),
            "low home bias, high eta": dict(aD=0.5, aT=0.6, eta=3.0)}
    for cname, cal in cals.items():
        for name in NAMES:
            a = float(sym[name].subs({aD: cal["aD"], aT: cal["aT"], eta: cal["eta"]}))
            f2, f3, fr = fd_derivative(name, cal)
            r0 = 3 * M.rhoD(**cal)
            out["rows"].append(dict(cal=cname, x=name, analytic=a, fd_1e2=f2, fd_1e3=f3,
                                    fd_richardson=fr, elasticity=a * (0.5 if name == "beta_AB" else
                                                                      (cal["aD"] if name == "alpha_D^A" else 1.0)) / r0))
            print("%-24s %-10s analytic %+.6f  fd %+.6f  rich %+.6f  (d rho*/dx)/(3rho_D) %+.4f"
                  % (cname, name, a, f3, fr, a / r0))
    out["symbolic"] = {k: str(v) for k, v in sym.items()}
    json.dump(out, open(os.path.join(HERE, "results", "task_c.json"), "w"), indent=1)
    draw_figure(out, sym, aD, aT, eta, rD)
