"""The analytic linearization (Appendix A) equals central finite differences
of the nonlinear solver at tau = +-1e-4, to 1e-6."""
import numpy as np
import pytest

from model import linear as lin
from model import nested_ces as nc

H = 1e-4
TOL = 1e-6


def random_prims(N, seed):
    rng = np.random.default_rng(seed)
    beta = rng.dirichlet(np.ones(N - 1) * 2.0, size=N)
    B = np.zeros((N, N))
    for i in range(N):
        B[i, [j for j in range(N) if j != i]] = beta[i]
    return nc.Primitives(
        N=N, L=np.exp(rng.normal(0, 0.7, N)), AT=np.exp(rng.normal(0, 0.2, N)),
        aT=rng.uniform(0.3, 0.7, N), aD=rng.uniform(0.5, 0.9, N),
        eta=rng.uniform(1.0, 3.0, N), rho=rng.uniform(1.2, 6.0, N), beta=B)


def fd_response(P, nu0, direction):
    up = nc.solve(P, H * direction, nu0=nu0)
    dn = nc.solve(P, -H * direction, nu0=nu0)
    return (up - dn) / (2 * H)


def random_direction(N, seed):
    rng = np.random.default_rng(seed + 1000)
    d = rng.normal(size=(N, N))
    np.fill_diagonal(d, 0.0)
    return d


CASES = [("sym", N, 0) for N in (2, 3, 4, 5)] + [("asym", N, s) for N in (3, 4, 5) for s in (1, 2, 3)]


@pytest.mark.parametrize("kind,N,seed", CASES)
def test_linear_equals_finite_differences(kind, N, seed):
    P = nc.symmetric(N, rho=3.3) if kind == "sym" else random_prims(N, seed)
    nu0 = nc.solve(P)
    base = nc.baseline_shares(P, nu0)
    assert np.max(np.abs(lin.balance_residual(base))) < 1e-12
    directions = [random_direction(N, seed)]
    d = np.zeros((N, N)); d[0, 1] = 1.0
    directions.append(d)
    if N >= 3:
        d = np.zeros((N, N)); d[0, 1] = d[1, 0] = 1.0
        directions.append(d)
    for direction in directions:
        lin_r = lin.response(base, direction)
        fd_r = fd_response(P, nu0, direction)
        assert np.max(np.abs(lin_r - fd_r)) < TOL, (lin_r, fd_r)


@pytest.mark.parametrize("N,seed", [(3, 4), (4, 5), (5, 6)])
def test_jacobian_matches_complex_step(N, seed):
    P = random_prims(N, seed)
    nu0 = nc.solve(P)
    base = nc.baseline_shares(P, nu0)
    Jt = lin.full_jacobian(base)
    nu_full = nc.full(nu0)
    cs = nc._jac_cs(lambda x: nc.trade_balances(x, P, np.zeros((N, N))), nu_full)
    assert np.max(np.abs(Jt - cs)) < 1e-12
    # homogeneity (rows) and Walras (columns)
    assert np.max(np.abs(Jt.sum(axis=1))) < 1e-12
    assert np.max(np.abs(Jt.sum(axis=0))) < 1e-12


@pytest.mark.parametrize("N,seed", [(3, 7), (4, 8)])
def test_disturbance_matches_complex_step(N, seed):
    P = random_prims(N, seed)
    nu0 = nc.solve(P)
    base = nc.baseline_shares(P, nu0)
    nu_full = nc.full(nu0)
    for j in range(N):
        for k in range(N):
            if j == k:
                continue
            d = np.zeros((N, N)); d[j, k] = 1.0
            t = (1j * 1e-30) * d
            cs = np.imag(nc.trade_balances(nu_full.astype(complex), P, t)) / 1e-30
            assert np.max(np.abs(lin.dTB(base, np.zeros(N), d) - cs)) < 1e-12


def test_real_rate_matches_finite_differences():
    P = random_prims(3, 11)
    nu0 = nc.solve(P)
    base = nc.baseline_shares(P, nu0)
    d = np.zeros((3, 3)); d[0, 1] = 1.0
    def logq(tau):
        nu = nc.solve(P, tau, nu0=nu0)
        a = nc.allocation(nc.full(nu), P, tau)
        return nc.full(nu)[1:] + np.log(a["P"][1:]) - np.log(a["P"][0])
    fd = (logq(H * d) - logq(-H * d)) / (2 * H)
    assert np.max(np.abs(lin.real_response(base, d) - fd)) < TOL
