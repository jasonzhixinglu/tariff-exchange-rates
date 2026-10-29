"""Extensions of the exact nested-CES model (Appendix D).

One generalized allocation covers both extensions; with gamma = 1 and T = 0
it reproduces nested_ces exactly.

(1) Ricardo-Viner tradables.  Y_Ti = A_Ti L_Ti^gamma_i (gamma_i <= 1),
    Y_Ni = A_Ni L_Ni, L_Ti + L_Ni = L_i (labor mobile across sectors within a
    country).  The producer price of each tradable is one in its own currency,
    so
        w_i = gamma_i A_Ti L_Ti^(gamma_i - 1),   P_Ni = w_i / A_Ni,
    and the specific-factor rents (1 - gamma_i) Y_Ti are rebated lump-sum.
    GDP_i = Y_Ti + P_Ni Y_Ni = Y_Ti + w_i L_Ni.

(2) Permanent transfer.  Country i receives T_i, fixed in units of A's
    currency (sum_i T_i = 0); in own currency it is T_i / e_Ai = T_i e^{-nu_i}.

Expenditure and income (own currency), tariff revenue rebated with REALIZED
shares s_ij (theta_ij = tau_ij / (1 + tau_ij), thbar_i = sum_{j!=i} theta_ij s_ij):
    E_i = I_i + T_i e^{-nu_i},     I_i = GDP_i + thbar_i E_i,
    =>  E_i = (GDP_i + T_i e^{-nu_i}) / (1 - thbar_i).
Flows at border prices in A's currency: f_ij = s_ij e^{nu_i} E_i / (1 + tau_ij);
TB_i = sum_k f_ki - sum_j f_ij.

Equilibrium (unknowns nu_j for j != A and L_Ti for all i):
    non-tradable clearing   P_Ni Y_Ni = (1 - alpha_Ti) E_i      (all i),
    external balance        TB_i + T_i = 0                      (i != A;
                            A's holds by Walras since sum TB = sum T = 0).
Welfare: log V_i = log E_i - alpha_Ti log P_Ti - (1 - alpha_Ti) log P_Ni
(E_i = I_i when T = 0, so this is nested_ces' logV).

L_T is parameterized internally as L_T = L / (1 + exp(-z)).  All functions
accept complex input so derivatives can be taken by complex step.
"""
import numpy as np

from . import nested_ces as nc
from .nested_ces import _jac_cs, full  # noqa: F401


def _vec(v, N, default):
    if v is None:
        return np.full(N, default, dtype=float)
    return np.broadcast_to(np.asarray(v), (N,)).copy()


def _sig(z):
    return 1.0 / (1.0 + np.exp(-z))


def allocation(nu_full, LT, P, tau, gamma=1.0, T=None):
    """All equilibrium objects at log exchange rates nu_full (length N) and
    tradable employment LT (length N).  Returns the nested_ces keys plus
    E (expenditure), GDP, w, PN, LT, LN, YT, R (tariff revenue), NT (non-tradable
    excess supply P_N Y_N - (1-aT) E) and ext (TB + T)."""
    N = P.N
    nu_full = np.asarray(nu_full)
    tau = np.asarray(tau)
    LT = np.asarray(LT)
    g = _vec(gamma, N, 1.0)
    T = np.zeros(N) if T is None else np.asarray(T)
    base = nc.allocation(nu_full, P, tau)        # price block depends on prices only
    s, PT = base["s"], base["PT"]
    offdiag = 1.0 - np.eye(N)
    thbar = np.sum(tau / (1.0 + tau) * s * offdiag, axis=1)
    LN = P.L - LT
    w = g * P.AT * LT ** (g - 1.0)
    YT = P.AT * LT ** g
    PN = w / P.AN
    GDP = YT + w * LN
    Tloc = T * np.exp(-nu_full)
    E = (GDP + Tloc) / (1.0 - thbar)
    I = E - Tloc
    Et = np.exp(nu_full) * E
    f = s * Et[:, None] / (1.0 + tau) * offdiag
    TB = f.sum(axis=0) - f.sum(axis=1)
    Pagg = PT ** P.aT * PN ** (1.0 - P.aT)
    logV = np.log(E) - P.aT * np.log(PT) - (1.0 - P.aT) * np.log(PN)
    NT = w * LN - (1.0 - P.aT) * E
    return dict(p=base["p"], PM=base["PM"], PT=PT, s=s, I=I, It=np.exp(nu_full) * I,
                E=E, Et=Et, f=f, TB=TB, P=Pagg, logV=logV, GDP=GDP, w=w, PN=PN,
                LT=LT, LN=LN, YT=YT, R=thbar * E, NT=NT, ext=TB + T)


def _unpack(x, P):
    N = P.N
    x = np.asarray(x)
    return full(x[:N - 1]), P.L * _sig(x[N - 1:])


def residuals(x, P, tau, gamma=1.0, T=None, scale=1.0):
    """Stacked residuals [TB_i + T_i (i != A); NT_i (all i)] at
    x = (nu_1..nu_{N-1}, z_0..z_{N-1})."""
    nu_full, LT = _unpack(x, P)
    a = allocation(nu_full, LT, P, tau, gamma, T)
    return np.concatenate([a["ext"][1:], a["NT"]]) / scale


def _z_of(LT, L):
    LT = np.asarray(LT, float)
    return np.log(LT / (L - LT))


def _initial_z(P, nu, tau, T):
    """L_T implied by non-tradable clearing at gamma = 1 (closed form)."""
    a = allocation(full(nu), P.L / 2, P, tau, 1.0, T)
    LN = (1.0 - P.aT) * a["E"].real / P.AT
    LT = np.clip(P.L - LN, 1e-6 * P.L, (1 - 1e-6) * P.L)
    return _z_of(LT, P.L)


def solve(P, tau=None, gamma=1.0, T=None, nu0=None, LT0=None, tol=1e-14, maxit=200):
    """Equilibrium: TB_i + T_i = 0 (i != A) and non-tradable clearing (all i).
    Newton with complex-step Jacobian and backtracking.  Returns (nu, LT)."""
    N = P.N
    tau = np.zeros((N, N)) if tau is None else np.asarray(tau, dtype=float)
    T = np.zeros(N) if T is None else np.asarray(T, dtype=float)
    nu = np.zeros(N - 1) if nu0 is None else np.array(nu0, dtype=float)
    z = _initial_z(P, nu, tau, T) if LT0 is None else _z_of(LT0, P.L)
    x = np.concatenate([nu, z])
    scale = float(np.sum(P.AT * P.L))

    def resid(y):
        return residuals(y, P, tau, gamma, T, scale)

    r = resid(x)
    for _ in range(maxit):
        if np.linalg.norm(r) < tol:
            break
        Jm = _jac_cs(resid, x)
        step = np.linalg.solve(Jm, -r)
        t = 1.0
        while True:
            cand = x + t * step
            rc = resid(cand)
            if np.all(np.isfinite(rc)) and (np.linalg.norm(rc) < np.linalg.norm(r) or t < 1e-8):
                break
            t /= 2.0
        x, r = cand, rc
    if not np.linalg.norm(r) < 1e-11:
        raise RuntimeError("solver did not converge: |resid| = %g" % np.linalg.norm(r))
    nu_full, LT = _unpack(x, P)
    return nu_full[1:], LT


def solve_path(P, tau_final, gamma=1.0, T=None, steps=8, nu0=None, LT0=None):
    """Continuation in tau from 0 (or from the supplied baseline) to tau_final."""
    nu, LT = solve(P, None, gamma, T, nu0=nu0, LT0=LT0)
    for s in np.linspace(0, 1, steps + 1)[1:]:
        nu, LT = solve(P, s * np.asarray(tau_final, float), gamma, T, nu0=nu, LT0=LT)
    return nu, LT


def local_response(P, tau, nu, LT, direction, gamma=1.0, T=None, logtariff=True):
    """First-order response along a tariff direction at any baseline, by the
    implicit function theorem on the stacked system with complex-step
    derivatives.  With logtariff, direction entries are d log(1 + tau_jk).

    Returns dict(dnu, dLT, dx, J, Jfull, G):
      J      reduced Jacobian d(TB_i + T_i)/d nu_l (i, l != A) with L_T
             re-optimized (Schur complement), comparable to nested_ces' J;
      Jfull  Jacobian of the stacked residuals in x = (nu, z);
      G      derivative of the stacked residuals along the tariff direction."""
    N = P.N
    tau = np.asarray(tau, dtype=float)
    x = np.concatenate([np.asarray(nu, float), _z_of(LT, P.L)])
    Jf = _jac_cs(lambda y: residuals(y, P, tau, gamma, T), x)
    d = np.asarray(direction, dtype=float) * ((1.0 + tau) if logtariff else 1.0)
    h = 1e-30
    G = np.imag(residuals(x.astype(complex), P, tau + 1j * h * d, gamma, T)) / h
    dx = np.linalg.solve(-Jf, G)
    n = N - 1
    Jnn, JnL, JLn, JLL = Jf[:n, :n], Jf[:n, n:], Jf[n:, :n], Jf[n:, n:]
    J = Jnn - JnL @ np.linalg.solve(JLL, JLn)
    sg = _sig(x[n:])
    dLT = P.L * sg * (1 - sg) * dx[n:]
    return dict(dnu=dx[:n], dLT=dLT, dx=dx, J=J, Jfull=Jf, G=G)


def total_derivative(fun, P, tau, nu, LT, direction, gamma=1.0, T=None, logtariff=True):
    """First-order change of fun(allocation_dict, nu_full) along a tariff
    direction, including the equilibrium response of (nu, L_T)."""
    tau = np.asarray(tau, dtype=float)
    lr = local_response(P, tau, nu, LT, direction, gamma, T, logtariff)
    x = np.concatenate([np.asarray(nu, float), _z_of(LT, P.L)])
    d = np.asarray(direction, dtype=float) * ((1.0 + tau) if logtariff else 1.0)
    h = 1e-30

    def F(xc, tc):
        nf, lt = _unpack(xc, P)
        return fun(allocation(nf, lt, P, tc, gamma, T), nf)

    dfx = _jac_cs(lambda y: F(y, tau), x)
    dft = np.imag(F(x.astype(complex), tau + 1j * h * d)) / h
    return dfx @ lr["dx"] + dft


def transfer(P, recipient, payer, share, gamma=1.0):
    """T vector: `recipient` receives share x its income at the no-transfer
    free-trade equilibrium (in A's currency), paid by `payer`."""
    nu, LT = solve(P, None, gamma)
    a = allocation(full(nu), LT, P, np.zeros((P.N, P.N)), gamma)
    T = np.zeros(P.N)
    T[recipient] = share * a["It"].real[recipient]
    T[payer] = -T[recipient]
    return T
