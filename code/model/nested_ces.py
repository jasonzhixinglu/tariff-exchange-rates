"""Exact (nonlinear) N-country nested-CES model of Section 3.2.

Conventions (as in the paper):
  * country 0 is A, whose currency is the numeraire;
  * nu_j = log e_{Aj}; a rise is a depreciation of A against j; nu_0 = 0;
  * tau[i, j] is the ad valorem tariff levied by i on imports from j;
  * consumer price of j's good in i (i's currency): p_ij = (1 + tau_ij) e_ij,
    with each tradable's producer price normalized to one in its own currency;
  * preferences: Cobb-Douglas outer layer (tradable share alpha_T),
    home-vs-import CES (home weight alpha_D, elasticity eta),
    cross-origin CES (origin weights beta_ij, elasticity rho);
  * income with rebated tariff revenue, using REALIZED shares s_ij:
        I_i = w_i L_i / (1 - sum_j s_ij tau_ij / (1 + tau_ij));
  * trade balances at border (tariff-exclusive) prices:
        TB_i = sum_k f_ki - sum_j f_ij,   f_ij = s_ij Itilde_i / (1 + tau_ij),
    with Itilde_i = e_{Ai} I_i the income in A's currency.

All primitives may differ by country.  Every function accepts complex input
so that derivatives can be taken by complex step.
"""
from dataclasses import dataclass, replace

import numpy as np


@dataclass
class Primitives:
    N: int = 3
    L: np.ndarray = None      # labor endowments
    AT: np.ndarray = None     # tradable productivity; w_i = A_Ti
    AN: np.ndarray = None     # non-tradable productivity; P_Ni = A_Ti / A_Ni
    aT: np.ndarray = None     # tradable expenditure share alpha_T
    aD: np.ndarray = None     # home weight alpha_D
    eta: np.ndarray = None    # home-import elasticity
    rho: np.ndarray = None    # cross-origin elasticity
    beta: np.ndarray = None   # origin weights; zero diagonal, rows sum to one

    def __post_init__(self):
        N = self.N

        def vec(v, default):
            if v is None:
                return np.full(N, default, dtype=float)
            return np.broadcast_to(np.asarray(v, dtype=float), (N,)).copy()

        self.L = vec(self.L, 1.0)
        self.AT = vec(self.AT, 1.0)
        self.AN = vec(self.AN, 1.0)
        self.aT = vec(self.aT, 0.4)
        self.aD = vec(self.aD, 0.8)
        self.eta = vec(self.eta, 1.5)
        self.rho = vec(self.rho, 4.0)
        if self.beta is None:
            self.beta = (np.ones((N, N)) - np.eye(N)) / (N - 1)
        self.beta = np.asarray(self.beta, dtype=float).copy()
        np.fill_diagonal(self.beta, 0.0)
        if not np.allclose(self.beta.sum(axis=1), 1.0):
            raise ValueError("beta rows must sum to one over j != i")

    def with_(self, **kw):
        return replace(self, **kw)


def symmetric(N=3, aD=0.8, aT=0.4, eta=1.5, rho=4.0, **kw):
    """Symmetric benchmark primitives (US-like defaults)."""
    return Primitives(N=N, aD=aD, aT=aT, eta=eta, rho=rho, **kw)


def _ces_index(w, p, s):
    """[sum w p^(1-s)]^(1/(1-s)); the Cobb-Douglas limit at s = 1."""
    if abs(s - 1.0) < 1e-12:
        return np.exp(np.sum(w * np.log(p)))
    return np.sum(w * p ** (1.0 - s)) ** (1.0 / (1.0 - s))


def full(nu):
    """Prepend nu_A = 0."""
    nu = np.asarray(nu)
    return np.concatenate([np.zeros(1, dtype=nu.dtype), nu])


def allocation(nu_full, P, tau):
    """All equilibrium objects at log exchange rates nu_full (length N)."""
    N = P.N
    nu_full = np.asarray(nu_full)
    tau = np.asarray(tau)
    loge = nu_full[None, :] - nu_full[:, None]          # log e_ij
    p = (1.0 + tau) * np.exp(loge)                       # p_ij, p_ii = 1
    dtype = np.result_type(p, nu_full, tau, float)
    s = np.zeros((N, N), dtype=dtype)
    PM = np.zeros(N, dtype=dtype)
    PT = np.zeros(N, dtype=dtype)
    for i in range(N):
        js = [j for j in range(N) if j != i]
        PM[i] = _ces_index(P.beta[i, js], p[i, js], P.rho[i])
        e = P.eta[i]
        if abs(e - 1.0) < 1e-12:
            PT[i] = PM[i] ** (1.0 - P.aD[i])
            s[i, i] = P.aT[i] * P.aD[i]
            mshare = P.aT[i] * (1.0 - P.aD[i])
        else:
            PT[i] = (P.aD[i] + (1.0 - P.aD[i]) * PM[i] ** (1.0 - e)) ** (1.0 / (1.0 - e))
            s[i, i] = P.aT[i] * P.aD[i] * PT[i] ** (e - 1.0)
            mshare = P.aT[i] * (1.0 - P.aD[i]) * (PM[i] / PT[i]) ** (1.0 - e)
        for j in js:
            s[i, j] = mshare * P.beta[i, j] * (p[i, j] / PM[i]) ** (1.0 - P.rho[i])
    offdiag = 1.0 - np.eye(N)
    theta = tau / (1.0 + tau)
    w = P.AT
    I = w * P.L / (1.0 - np.sum(theta * s * offdiag, axis=1))
    It = np.exp(nu_full) * I
    f = s * It[:, None] / (1.0 + tau) * offdiag
    TB = f.sum(axis=0) - f.sum(axis=1)
    PN = P.AT / P.AN
    Pagg = PT ** P.aT * PN ** (1.0 - P.aT)
    # indirect utility up to a country-specific constant: I / P (own currency)
    logV = np.log(I) - P.aT * np.log(PT) - (1.0 - P.aT) * np.log(PN)
    return dict(p=p, PM=PM, PT=PT, s=s, I=I, It=It, f=f, TB=TB, P=Pagg, logV=logV)


def trade_balances(nu_full, P, tau):
    return allocation(nu_full, P, tau)["TB"]


def _jac_cs(fun, x, h=1e-30):
    """Complex-step Jacobian of a real vector function."""
    x = np.asarray(x, dtype=float)
    cols = []
    for l in range(len(x)):
        xc = x.astype(complex)
        xc[l] += 1j * h
        cols.append(np.imag(fun(xc)) / h)
    return np.column_stack(cols)


def solve(P, tau=None, nu0=None, tol=1e-14, maxit=200):
    """Balanced-trade equilibrium: TB_i = 0 for i != A (Walras' law drops A).

    Newton's method with a complex-step Jacobian and backtracking.
    Returns nu = (nu_j)_{j != A}.
    """
    N = P.N
    tau = np.zeros((N, N)) if tau is None else np.asarray(tau, dtype=float)
    nu = np.zeros(N - 1) if nu0 is None else np.array(nu0, dtype=float)
    scale = float(np.sum(P.AT * P.L))

    def resid(x):
        return trade_balances(full(x), P, tau)[1:] / scale

    r = resid(nu)
    for _ in range(maxit):
        if np.linalg.norm(r) < tol:
            break
        Jm = _jac_cs(resid, nu)
        step = np.linalg.solve(Jm, -r)
        t = 1.0
        while True:
            cand = nu + t * step
            rc = resid(cand)
            if np.all(np.isfinite(rc)) and (np.linalg.norm(rc) < np.linalg.norm(r) or t < 1e-8):
                break
            t /= 2.0
        nu, r = cand, rc
    if not np.linalg.norm(r) < 1e-11:
        raise RuntimeError("solver did not converge: |TB| = %g" % np.linalg.norm(r))
    return nu


def local_response(P, tau, nu, direction, logtariff=True):
    """First-order d nu along a tariff direction at ANY baseline (tau, nu),
    by the implicit function theorem with complex-step derivatives.
    With logtariff, direction entries are d log(1 + tau_jk)."""
    N = P.N
    tau = np.asarray(tau, dtype=float)
    Jm = _jac_cs(lambda x: trade_balances(full(x), P, tau)[1:], nu)
    d = np.asarray(direction, dtype=float) * ((1.0 + tau) if logtariff else 1.0)
    h = 1e-30
    G = np.imag(trade_balances(full(np.asarray(nu, float)).astype(complex), P,
                               tau + 1j * h * d))[1:] / h
    return np.linalg.solve(-Jm, G), Jm


def baseline_shares(P, nu, tau=None):
    """Baseline objects used by the linearization (Appendix A):
    common-currency incomes y_i, home shares h_i, import-origin shares b_ij."""
    N = P.N
    tau = np.zeros((N, N)) if tau is None else tau
    a = allocation(full(nu), P, tau)
    s = a["s"].real
    h = np.diag(s) / P.aT
    imp = s * (1.0 - np.eye(N))
    b = imp / imp.sum(axis=1, keepdims=True)
    return dict(y=a["It"].real, h=h, b=b, aT=P.aT.copy(), eta=P.eta.copy(),
                rho=P.rho.copy())


def neer_weights(P, nu, tau=None, i=0):
    """Baseline bilateral trade weights w_ij = (f_ij + f_ji) / sum_k (f_ik + f_ki)."""
    N = P.N
    tau = np.zeros((N, N)) if tau is None else tau
    f = allocation(full(nu), P, tau)["f"].real
    tot = f[i, :] + f[:, i]
    tot[i] = 0.0
    return tot / tot.sum()


def import_weights(P, nu, tau=None, i=0):
    """Origin shares b_ij in i's import bundle (tariff-inclusive expenditure)."""
    N = P.N
    tau = np.zeros((N, N)) if tau is None else tau
    s = allocation(full(nu), P, tau)["s"].real[i].copy()
    s[i] = 0.0
    return s / s.sum()
