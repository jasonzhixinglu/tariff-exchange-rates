"""Linearized system of Appendix A, built from baseline shares.

A baseline is a dict with
  y   (N,)   incomes in a common currency,
  h   (N,)   home shares of tradable expenditure,
  b   (N,N)  origin shares in each import bundle (zero diagonal, rows sum to 1),
  aT  (N,)   tradable expenditure shares,
  eta (N,)   home-import elasticities (country-specific allowed),
  rho (N,)   cross-origin elasticities (country-specific allowed).
The baseline is a balanced free-trade equilibrium.  Country 0 is A.

The equations (Appendix A):
  dp_ij        = dnu_j - dnu_i + dtau_ij,              dp_ii = 0
  dlog P_Mi    = sum_j b_ij dp_ij
  dlog s_ij    = (1-rho_i)(dp_ij - dlog P_Mi) + (1-eta_i) h_i dlog P_Mi
  dlog Itil_i  = dnu_i + sum_j s_ij dtau_ij
  dTB_i        = sum_k f_ki (dlog s_ki + dlog Itil_k - dtau_ki)
               - sum_j f_ij (dlog s_ij + dlog Itil_i - dtau_ij),
with s_ij = aT_i (1-h_i) b_ij and f_ij = s_ij y_i.
"""
import numpy as np


def _arr(base, key, N):
    return np.broadcast_to(np.asarray(base[key], dtype=float), (N,)).copy()


def unpack(base):
    b = np.asarray(base["b"], dtype=float).copy()
    N = b.shape[0]
    np.fill_diagonal(b, 0.0)
    return dict(N=N, y=_arr(base, "y", N), h=_arr(base, "h", N), b=b,
                aT=_arr(base, "aT", N), eta=_arr(base, "eta", N),
                rho=_arr(base, "rho", N))


def symmetric_base(N, aD=0.8, aT=0.4, eta=1.5, rho=4.0):
    """Symmetric free-trade benchmark: y_i = 1, h_i = alpha_D, b_ij = 1/(N-1)."""
    b = (np.ones((N, N)) - np.eye(N)) / (N - 1)
    return dict(y=np.ones(N), h=np.full(N, aD), b=b, aT=np.full(N, aT),
                eta=np.full(N, eta), rho=np.full(N, rho))


def with_rho(base, rho):
    out = dict(base)
    out["rho"] = np.broadcast_to(np.asarray(rho, dtype=float),
                                 (np.asarray(base["b"]).shape[0],)).copy()
    return out


def price_changes(base, dnu, dtau):
    B = unpack(base)
    N = B["N"]
    dtau = np.zeros((N, N)) if dtau is None else np.asarray(dtau, dtype=float)
    dp = dnu[None, :] - dnu[:, None] + dtau
    np.fill_diagonal(dp, 0.0)
    dPM = (B["b"] * dp).sum(axis=1)
    return B, dtau, dp, dPM


def dTB(base, dnu, dtau=None):
    """First-order change in all N trade balances.

    dnu: (N,) changes in log currency values relative to A (dnu[0] = 0 for the
         usual normalization, but any N-vector is accepted);
    dtau: (N,N) tariff changes.
    """
    dnu = np.asarray(dnu, dtype=float)
    B, dtau, dp, dPM = price_changes(base, dnu, dtau)
    N = B["N"]
    off = 1.0 - np.eye(N)
    s = (B["aT"] * (1.0 - B["h"]))[:, None] * B["b"] * off
    dlogs = ((1.0 - B["rho"])[:, None] * (dp - dPM[:, None])
             + ((1.0 - B["eta"]) * B["h"] * dPM)[:, None])
    dlogI = dnu + (s * dtau).sum(axis=1)
    f = s * B["y"][:, None]
    df = f * (dlogs + dlogI[:, None] - dtau) * off
    return df.sum(axis=0) - df.sum(axis=1)


def full_jacobian(base):
    """Jtilde_il = dTB_i / dnu_l (N x N), currency values in a common unit."""
    N = unpack(base)["N"]
    return np.column_stack([dTB(base, np.eye(N)[l]) for l in range(N)])


def reduced_jacobian(base):
    """J: delete A's row and column (A is the numeraire; Walras drops TB_A)."""
    return full_jacobian(base)[1:, 1:]


def disturbance(base, dtau):
    """F: trade-balance disturbance at unchanged exchange rates, i != A."""
    N = unpack(base)["N"]
    return dTB(base, np.zeros(N), dtau)[1:]


def response(base, dtau):
    """d nu = (-J)^{-1} F, nu_j = log e_{Aj}, j != A."""
    return np.linalg.solve(-reduced_jacobian(base), disturbance(base, dtau))


def mml(J, tol=1e-12):
    """Multilateral Marshall-Lerner: J_il >= 0 off the diagonal and
    (-J)^{-1} >= 0 elementwise."""
    off = J - np.diag(np.diag(J))
    if np.any(off < -tol * max(1.0, np.abs(J).max())):
        return False
    try:
        inv = np.linalg.inv(-J)
    except np.linalg.LinAlgError:
        return False
    return bool(np.all(inv >= -tol * np.abs(inv).max()))


def real_response(base, dtau):
    """d log q_{Aj} for j != A, with q_ij = e_ij P_j / P_i and
    dlog P_i = aT_i (1 - h_i) dlog P_Mi (own-currency consumer price level)."""
    B = unpack(base)
    dnu = np.concatenate([[0.0], response(base, dtau)])
    _, _, _, dPM = price_changes(base, dnu, dtau)
    dP = B["aT"] * (1.0 - B["h"]) * dPM
    return dnu[1:] + dP[1:] - dP[0]


def welfare_change(base, dtau, i=0):
    """First-order change in log indirect utility of country i (money metric):
    dlog V_i = dlog I_i - aT_i dlog P_Ti, with dlog P_Ti = (1 - h_i) dlog P_Mi."""
    B = unpack(base)
    N = B["N"]
    dtau = np.zeros((N, N)) if dtau is None else np.asarray(dtau, dtype=float)
    dnu = np.concatenate([[0.0], response(base, dtau)])
    _, _, _, dPM = price_changes(base, dnu, dtau)
    s = (B["aT"] * (1.0 - B["h"]))[:, None] * B["b"]
    dlogI_own = (s * dtau).sum(axis=1)
    return dlogI_own[i] - B["aT"][i] * (1.0 - B["h"][i]) * dPM[i]


def import_weights(base, i=0):
    b = unpack(base)["b"][i].copy()
    return np.delete(b, i)


def trade_weights(base, i=0):
    B = unpack(base)
    s = (B["aT"] * (1.0 - B["h"]))[:, None] * B["b"]
    f = s * B["y"][:, None]
    tot = f[i, :] + f[:, i]
    tot = np.delete(tot, i)
    return tot / tot.sum()


def balance_residual(base):
    """Baseline trade balances (should be ~0 for a valid baseline)."""
    B = unpack(base)
    s = (B["aT"] * (1.0 - B["h"]))[:, None] * B["b"]
    f = s * B["y"][:, None]
    return f.sum(axis=0) - f.sum(axis=1)


def balanced_incomes(h, b, aT, y0=0):
    """Incomes that balance trade for given (h, b, aT), normalized y[y0] = 1:
    x = aT (1-h) y solves x' = x' b."""
    b = np.asarray(b, dtype=float)
    N = b.shape[0]
    aT = np.broadcast_to(np.asarray(aT, float), (N,))
    w, V = np.linalg.eig(b.T)
    x = np.real(V[:, np.argmin(np.abs(w - 1.0))])
    y = x / (aT * (1.0 - np.asarray(h, float)))
    return y / y[y0]
