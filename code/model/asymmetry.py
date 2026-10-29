"""Asymmetric baselines (Section 4): the fixed-baseline polynomial
Q(rho) = w' adj(-J(rho)) F(rho) and thresholds with primitives held fixed."""
import numpy as np
from scipy.optimize import brentq

from . import linear as lin
from . import nested_ces as nc


def unilateral_direction(N, target=1, imposer=0):
    d = np.zeros((N, N))
    d[imposer, target] = 1.0
    return d


def adj(Mx):
    return np.linalg.det(Mx) * np.linalg.inv(Mx)


def numerator(base, rho, weights, dtau):
    """w' adj(-J(rho)) F(rho) at a fixed baseline (shares held fixed)."""
    bb = lin.with_rho(base, rho)
    A = -lin.reduced_jacobian(bb)
    return float(np.asarray(weights) @ adj(A) @ lin.disturbance(bb, dtau))


def poly_coeffs(base, weights, dtau, rhos=(1.0, 2.0, 3.0), deg=2):
    """Coefficients (q_deg, ..., q_0) of the fixed-baseline numerator, which is
    a polynomial of degree N-1 in rho.  Extracted by exact interpolation at
    deg+1 points and verified at two further points."""
    rhos = np.asarray(rhos, dtype=float)
    if len(rhos) != deg + 1:
        rhos = np.arange(1.0, deg + 2.0)
    vals = np.array([numerator(base, r, weights, dtau) for r in rhos])
    q = np.linalg.solve(np.vander(rhos, deg + 1), vals)
    for r in (5.5, 11.0):
        v = numerator(base, r, weights, dtau)
        assert abs(np.polyval(q, r) - v) <= 1e-9 * max(1.0, abs(v)), "not a polynomial of this degree"
    return q


def normalized(q, tol=1e-12):
    """Q-hat: divide by |q2| if q2 != 0, else by |q1|."""
    q = np.asarray(q, dtype=float)
    scale = abs(q[0]) if abs(q[0]) > tol * np.abs(q).max() else abs(q[1])
    return q / scale


def positive_roots(q, tol=1e-12):
    q = np.asarray(q, dtype=float)
    if abs(q[0]) < tol * np.abs(q).max():
        q = q[1:]
    r = np.roots(q)
    return np.sort(r[(np.abs(r.imag) < 1e-10) & (r.real > 0)].real)


def three_country_prims(L=(1.0, 1.0, 1.0), beta_AB=0.5, beta_BA=0.5, beta_CA=0.5,
                        aD=0.8, aT=0.4, eta=1.5, rho=3.96):
    beta = np.array([[0.0, beta_AB, 1 - beta_AB],
                     [beta_BA, 0.0, 1 - beta_BA],
                     [beta_CA, 1 - beta_CA, 0.0]])
    return nc.Primitives(N=3, L=np.array(L, float), aD=aD, aT=aT, eta=eta, rho=rho,
                         beta=beta)


def base_from_prims(P, nu=None):
    nu = nc.solve(P) if nu is None else nu
    return nc.baseline_shares(P, nu), nu


def responses_at(P, nu=None, dtau=None):
    """Linear responses at the free-trade baseline of primitives P."""
    base, nu = base_from_prims(P, nu)
    dtau = unilateral_direction(P.N) if dtau is None else dtau
    dnu = lin.response(base, dtau)
    J = lin.reduced_jacobian(base)
    return dict(dnu=dnu, base=base, nu=nu, mml=lin.mml(J),
                b=lin.import_weights(base), w=lin.trade_weights(base))


def scan_roots(fun, grid):
    """All sign changes of fun on grid, refined by brentq."""
    vals = np.array([fun(r) for r in grid])
    roots = []
    for a, b, fa, fb in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if np.sign(fa) != np.sign(fb):
            roots.append(brentq(fun, a, b, xtol=1e-10))
    return roots, vals
