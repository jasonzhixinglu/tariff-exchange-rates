# -*- coding: utf-8 -*-
"""Nested-CES model of Section 3.1 (eqs. 17-20) of
"Understanding Multilateral Tariffs and Exchange Rates".

Country 0 is A (currency numeraire).  nu_j = log e_{Aj}, so nu_0 = 0 and
log e_{ij} = nu_j - nu_i.  tau[i, j] is the ad valorem tariff levied by i on
imports from j.

Three layers:
  * `trade_balances`      exact nonlinear model, numpy (real or complex input)
  * `solve`               balanced-trade equilibrium, Newton on nu_1..nu_{N-1}
  * `linearize`           J = dTB/dnu, G = dTB/dtau at any baseline, by complex
                          step (exact to machine precision)
  * `symbolic_model`      the same equations in sympy, for the symbolic
                          linearization and the verification of (48)-(52), (57)
"""
from dataclasses import dataclass, field, replace

import numpy as np
import sympy as sp


# --------------------------------------------------------------- primitives
@dataclass
class Primitives:
    N: int = 3
    L: np.ndarray = None        # labour endowments
    AT: np.ndarray = None       # tradable productivity (w_i = A_Ti)
    AN: np.ndarray = None       # non-tradable productivity (does not enter TB)
    aT: np.ndarray = None       # tradable share alpha_T, by country
    aD: np.ndarray = None       # home weight alpha_D, by country
    eta: np.ndarray = None      # home-import elasticity, by country
    rho: np.ndarray = None      # cross-origin elasticity, by country
    beta: np.ndarray = None     # origin weights, rows sum to 1, zero diagonal
    tau: np.ndarray = None      # tariffs, zero diagonal

    def __post_init__(self):
        N = self.N
        vec = lambda v, d: np.full(N, d, float) if v is None else np.broadcast_to(np.asarray(v, float), (N,)).copy()
        self.L = vec(self.L, 1.0)
        self.AT = vec(self.AT, 1.0)
        self.AN = vec(self.AN, 1.0)
        self.aT = vec(self.aT, 0.6)
        self.aD = vec(self.aD, 0.7)
        self.eta = vec(self.eta, 1.5)
        self.rho = vec(self.rho, 3.0)
        if self.beta is None:
            self.beta = (np.ones((N, N)) - np.eye(N)) / (N - 1)
        self.beta = np.asarray(self.beta, float).copy()
        if self.tau is None:
            self.tau = np.zeros((N, N))
        self.tau = np.asarray(self.tau, float).copy()

    def with_(self, **kw):
        new = replace(self, **{k: v for k, v in kw.items()})
        return new


def symmetric(N=3, aD=0.7, aT=0.6, eta=1.5, rho=3.0, **kw):
    return Primitives(N=N, aD=aD, aT=aT, eta=eta, rho=rho, **kw)


def rhoD(aD, aT, eta):
    return aD * eta + (1 - aD) * (1 - aT)


def MN(N, aD, eta, rho):
    return (N * aD * (eta - 1) + (N - 2) * rho + 1) / (N - 1)


# ------------------------------------------------------------ exact model
def _ces_index(w, p, s):
    """[sum w p^(1-s)]^(1/(1-s)) along the last axis; Cobb-Douglas at s = 1."""
    if abs(s - 1.0) < 1e-12:
        return np.exp(np.sum(w * np.log(p), axis=-1))
    return np.sum(w * p ** (1 - s), axis=-1) ** (1 / (1 - s))


def pieces(nu_full, P, tau=None):
    """All model objects at log exchange rates nu_full (length N, nu_0 = 0)."""
    N = P.N
    tau = P.tau if tau is None else tau
    nu_full = np.asarray(nu_full)
    loge = nu_full[None, :] - nu_full[:, None]           # log e_ij
    p = (1 + tau) * np.exp(loge)                          # p_ij
    dtype = np.result_type(p, nu_full, tau)
    s = np.zeros((N, N), dtype=dtype)
    PM = np.zeros(N, dtype=dtype)
    PT = np.zeros(N, dtype=dtype)
    for i in range(N):
        js = [j for j in range(N) if j != i]
        PM[i] = _ces_index(P.beta[i, js], p[i, js], P.rho[i])
        # p_ii = 1
        e = P.eta[i]
        if abs(e - 1.0) < 1e-12:
            PT[i] = PM[i] ** (1 - P.aD[i])
        else:
            PT[i] = (P.aD[i] + (1 - P.aD[i]) * PM[i] ** (1 - e)) ** (1 / (1 - e))
        s[i, i] = P.aT[i] * P.aD[i] * (1 / PT[i]) ** (1 - e)
        for j in js:
            s[i, j] = (P.aT[i] * (1 - P.aD[i]) * (PM[i] / PT[i]) ** (1 - e)
                       * P.beta[i, j] * (p[i, j] / PM[i]) ** (1 - P.rho[i]))
    theta = tau / (1 + tau)
    I = P.AT * P.L / (1 - np.sum(theta * s * (1 - np.eye(N)), axis=1))   # eq. (19)
    It = np.exp(nu_full) * I                                            # common currency
    f = s * It[:, None] / (1 + tau)                                     # border flows
    f = f * (1 - np.eye(N))
    TB = f.sum(axis=0) - f.sum(axis=1)                                  # eq. (20)
    return dict(p=p, PM=PM, PT=PT, s=s, I=I, It=It, f=f, TB=TB)


def trade_balances(nu_full, P, tau=None):
    return pieces(nu_full, P, tau)["TB"]


def full(nu):
    return np.concatenate([[0.0], np.asarray(nu, float)])


def solve(P, tau=None, nu0=None, tol=1e-15, maxit=100):
    """Balanced-trade equilibrium: TB_i = 0 for i != A.  Newton with a
    complex-step Jacobian and backtracking.  Returns nu (length N-1)."""
    N = P.N
    tau = P.tau if tau is None else tau
    nu = np.zeros(N - 1) if nu0 is None else np.array(nu0, float)
    scale = float(np.sum(P.AT * P.L))
    F = lambda x: trade_balances(full(x), P, tau)[1:] / scale
    r = F(nu)
    for it in range(maxit):
        Jm = np.empty((N - 1, N - 1))
        h = 1e-30
        for l in range(N - 1):
            x = nu.astype(complex)
            x[l] += 1j * h
            Jm[:, l] = np.imag(trade_balances(np.concatenate([[0.0], x]), P, tau)[1:]) / h / scale
        step = np.linalg.solve(Jm, -r)
        t = 1.0
        while True:
            cand = nu + t * step
            rc = F(cand)
            if np.linalg.norm(rc) < np.linalg.norm(r) or t < 1e-6:
                break
            t /= 2
        nu, r = cand, rc
        if np.linalg.norm(r) < tol:
            break
    if np.linalg.norm(r) > 1e-11:
        raise RuntimeError("solver did not converge: |TB| = %g" % np.linalg.norm(r))
    return nu


def linearize(P, nu, tau=None, logtariff=False):
    """J (N-1 x N-1) and the full Jtilde (N x N) w.r.t. nu, and G_full
    (N x N x N): dTB_i/dtau_{jk}.  Complex step, so derivatives are exact to
    rounding.  If logtariff, derivatives are w.r.t. log(1+tau_jk)."""
    N = P.N
    tau = P.tau if tau is None else tau
    nuf = full(nu)
    h = 1e-30
    Jt = np.empty((N, N))
    for l in range(N):
        x = nuf.astype(complex)
        x[l] += 1j * h
        Jt[:, l] = np.imag(trade_balances(x, P, tau)) / h
    Gf = np.zeros((N, N, N))
    for j in range(N):
        for k in range(N):
            if j == k:
                continue
            t = tau.astype(complex)
            t[j, k] += 1j * h
            Gf[:, j, k] = np.imag(trade_balances(nuf.astype(complex), P, t)) / h
            if logtariff:
                Gf[:, j, k] *= (1 + tau[j, k])
    return Jt[1:, 1:], Jt, Gf


def response(P, nu, direction, tau=None, logtariff=False):
    """d nu / ds for tariff direction `direction` (N x N array of dtau_jk)."""
    J, _, Gf = linearize(P, nu, tau, logtariff)
    F = np.einsum("ijk,jk->i", Gf, direction)[1:]
    return np.linalg.solve(-J, F), J, F


def neer_weights(P, nu, tau=None, i=0):
    """Baseline bilateral trade weights of eq. (21) for country i."""
    f = pieces(full(nu), P, tau)["f"]
    tot = np.array([f[i, j] + f[j, i] for j in range(P.N)])
    tot[i] = 0.0
    return tot / tot.sum()


def mml_holds(J, tol=1e-12):
    """MML (8): off-diagonal J >= 0 and (-J)^{-1} >= 0 elementwise."""
    off = J - np.diag(np.diag(J))
    if np.any(off < -tol):
        return False, "offdiag"
    try:
        inv = np.linalg.inv(-J)
    except np.linalg.LinAlgError:
        return False, "singular"
    if np.any(inv < -tol * np.max(np.abs(inv))):
        return False, "inverse"
    return True, "ok"


# --------------------------------------------------------- symbolic model
def symbolic_model(N):
    """Sympy version of eqs. (17)-(20) with fully general, country-specific
    primitives.  Returns (TB list, symbols dict)."""
    idx = range(N)
    nu = sp.symbols("nu0:%d" % N)
    tau = {(i, j): sp.Symbol("tau_%d%d" % (i, j)) for i in idx for j in idx if i != j}
    beta = {(i, j): sp.Symbol("beta_%d%d" % (i, j), positive=True) for i in idx for j in idx if i != j}
    L = sp.symbols("L0:%d" % N, positive=True)
    AT = sp.symbols("AT0:%d" % N, positive=True)
    aT = sp.symbols("aT0:%d" % N, positive=True)
    aD = sp.symbols("aD0:%d" % N, positive=True)
    eta = sp.symbols("eta0:%d" % N, positive=True)
    rho = sp.symbols("rho0:%d" % N, positive=True)
    p = {(i, j): (1 + tau[i, j]) * sp.exp(nu[j] - nu[i]) for (i, j) in tau}
    s, Iv = {}, {}
    for i in idx:
        js = [j for j in idx if j != i]
        PM = sp.Add(*[beta[i, j] * p[i, j] ** (1 - rho[i]) for j in js]) ** (1 / (1 - rho[i]))
        PT = (aD[i] + (1 - aD[i]) * PM ** (1 - eta[i])) ** (1 / (1 - eta[i]))
        for j in js:
            s[i, j] = (aT[i] * (1 - aD[i]) * (PM / PT) ** (1 - eta[i]) * beta[i, j]
                       * (p[i, j] / PM) ** (1 - rho[i]))
        Iv[i] = AT[i] * L[i] / (1 - sp.Add(*[tau[i, j] / (1 + tau[i, j]) * s[i, j] for j in js]))
    f = {(i, j): s[i, j] * sp.exp(nu[i]) * Iv[i] / (1 + tau[i, j]) for (i, j) in tau}
    TB = [sp.Add(*[f[k, i] for k in idx if k != i]) - sp.Add(*[f[i, j] for j in idx if j != i])
          for i in idx]
    syms = dict(nu=nu, tau=tau, beta=beta, L=L, AT=AT, aT=aT, aD=aD, eta=eta, rho=rho)
    return TB, syms


def symbolic_linearization(N, tariffs=None, at=None):
    """Full Jacobian Jtilde_il = dTB_i/dnu_l and G_i,(jk) = dTB_i/dtau_jk as
    sympy matrices.  `tariffs` restricts the (j, k) pairs differentiated;
    `at` is a substitution dict applied (by xreplace) right after each
    derivative, which keeps the expressions small."""
    TB, S = symbolic_model(N)
    ev = (lambda e: e) if at is None else (lambda e: sp.simplify(e.xreplace(at(S)) if callable(at) else e.xreplace(at)))
    Jt = sp.Matrix(N, N, lambda i, l: ev(sp.diff(TB[i], S["nu"][l])))
    keys = list(S["tau"]) if tariffs is None else tariffs
    G = {jk: sp.Matrix([ev(sp.diff(TB[i], S["tau"][jk])) for i in range(N)]) for jk in keys}
    return Jt, G, S


def symmetric_subs(S, N, aD, aT, eta, rho):
    """Substitution dict for the symmetric free-trade baseline (nu = 0,
    tau = 0, L = A_T = 1, beta = 1/(N-1)), with symbolic common parameters."""
    d = {}
    for i in range(N):
        d.update({S["nu"][i]: 0, S["L"][i]: 1, S["AT"][i]: 1, S["aT"][i]: aT,
                  S["aD"][i]: aD, S["eta"][i]: eta, S["rho"][i]: rho})
    for k in S["tau"]:
        d[S["tau"][k]] = 0
        d[S["beta"][k]] = sp.Rational(1, N - 1)
    return d
