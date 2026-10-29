"""Extensions of Appendix D (model/extensions.py): Ricardo-Viner tradables and
a permanent transfer-financed imbalance.

  * gamma = 1, T = 0 reproduce nested_ces (allocations, nu, local responses);
  * the IFT response equals central finite differences of the solver
    (tau step 1e-4, tolerance 1e-6) for gamma in {0.5, 2/3} and with transfers;
  * equilibrium identities: TB_i + T_i = 0, non-tradable clearing, labor
    adding up, income accounting, Walras."""
import numpy as np
import pytest

from model import extensions as ex
from model import nested_ces as nc

from test_linearization import random_direction, random_prims

H = 1e-4
TOL = 1e-6


def random_tariffs(N, seed, scale=0.3):
    rng = np.random.default_rng(seed + 500)
    t = rng.uniform(0, scale, (N, N))
    np.fill_diagonal(t, 0.0)
    return t


def random_transfer(N, seed, size=0.05):
    rng = np.random.default_rng(seed + 900)
    T = rng.normal(0, size, N)
    return T - T.mean()


def unilateral(N):
    d = np.zeros((N, N)); d[0, 1] = 1.0
    return d


PRIMS = [("sym", 3, 0), ("sym", 4, 0)] + [("asym", N, s) for N in (3, 4, 5) for s in (31, 32)]


def prims(kind, N, seed):
    return nc.symmetric(N, rho=3.3) if kind == "sym" else random_prims(N, seed)


@pytest.mark.parametrize("kind,N,seed", PRIMS)
def test_reproduces_nested_ces(kind, N, seed):
    P = prims(kind, N, seed)
    for tau in (np.zeros((N, N)), random_tariffs(N, seed)):
        nu_nc = nc.solve(P, tau)
        nu_ex, LT = ex.solve(P, tau)
        assert np.max(np.abs(nu_nc - nu_ex)) < 1e-12
        a0 = nc.allocation(nc.full(nu_nc), P, tau)
        a1 = ex.allocation(nc.full(nu_ex), LT, P, tau)
        for k in ("p", "PM", "PT", "s", "I", "It", "f", "TB", "P", "logV"):
            assert np.max(np.abs(a0[k] - a1[k])) < 1e-12, k
        # allocation at arbitrary off-equilibrium nu and LT is also identical
        rng = np.random.default_rng(seed)
        nuf = nc.full(rng.normal(0, 0.2, N - 1))
        a0 = nc.allocation(nuf, P, tau)
        a1 = ex.allocation(nuf, P.L * rng.uniform(0.2, 0.8, N), P, tau)
        for k in ("s", "I", "TB", "P", "logV"):
            assert np.max(np.abs(a0[k] - a1[k])) < 1e-12, k
        for d in (unilateral(N), random_direction(N, seed)):
            r0, J0 = nc.local_response(P, tau, nu_nc, d)
            r1 = ex.local_response(P, tau, nu_ex, LT, d)
            assert np.max(np.abs(r0 - r1["dnu"])) < 1e-12
            assert np.max(np.abs(J0 - r1["J"])) < 1e-12


CASES = ([("gamma", g, N, s) for g in (0.5, 2 / 3) for N in (3, 4, 5) for s in (41, 42)]
         + [("transfer", 1.0, N, s) for N in (3, 4, 5) for s in (43, 44)]
         + [("both", 0.5, N, s) for N in (3, 4) for s in (45,)])


@pytest.mark.parametrize("kind,gamma,N,seed", CASES)
def test_ift_equals_finite_differences(kind, gamma, N, seed):
    P = random_prims(N, seed)
    rng = np.random.default_rng(seed)
    g = gamma * rng.uniform(0.9, 1.0, N) if kind != "transfer" else 1.0
    T = random_transfer(N, seed) if kind != "gamma" else None
    tau0 = random_tariffs(N, seed, 0.2)
    nu0, LT0 = ex.solve(P, tau0, g, T)
    for d in (unilateral(N), random_direction(N, seed)):
        lr = ex.local_response(P, tau0, nu0, LT0, d, g, T, logtariff=False)
        up = ex.solve(P, tau0 + H * d, g, T, nu0=nu0, LT0=LT0)
        dn = ex.solve(P, tau0 - H * d, g, T, nu0=nu0, LT0=LT0)
        assert np.max(np.abs(lr["dnu"] - (up[0] - dn[0]) / (2 * H))) < TOL
        assert np.max(np.abs(lr["dLT"] - (up[1] - dn[1]) / (2 * H))) < TOL
        # total derivative of welfare and real rates
        fun = lambda a, nf: np.concatenate([a["logV"], nf + np.log(a["P"]) - np.log(a["P"][0])])

        def val(sol, tau):
            nf = nc.full(sol[0])
            return fun(ex.allocation(nf, sol[1], P, tau, g, T), nf).real
        td = ex.total_derivative(fun, P, tau0, nu0, LT0, d, g, T, logtariff=False)
        fd = (val(up, tau0 + H * d) - val(dn, tau0 - H * d)) / (2 * H)
        assert np.max(np.abs(td - fd)) < TOL


@pytest.mark.parametrize("kind,gamma,N,seed", CASES)
def test_equilibrium_identities(kind, gamma, N, seed):
    P = random_prims(N, seed)
    g = np.full(N, gamma)
    T = random_transfer(N, seed) if kind != "gamma" else np.zeros(N)
    tau = random_tariffs(N, seed)
    nu, LT = ex.solve(P, tau, g, T)
    a = ex.allocation(nc.full(nu), LT, P, tau, g, T)
    assert np.max(np.abs(a["TB"] + T)) < 1e-12           # including A (Walras)
    assert abs(a["TB"].sum()) < 1e-12
    assert np.max(np.abs(a["NT"])) < 1e-12
    assert np.all(LT > 0) and np.all(a["LN"] > 0)
    assert np.allclose(a["LT"] + a["LN"], P.L, atol=1e-14)
    # income = tradable output + non-tradable output + tariff revenue
    YN = P.AN * a["LN"]
    assert np.allclose(a["I"], a["YT"] + a["PN"] * YN + a["R"], atol=1e-12)
    # wage = value marginal product; rents = (1-gamma) Y_T
    assert np.allclose(a["w"] * LT, g * a["YT"], atol=1e-13)
    assert np.allclose(a["GDP"] - a["w"] * P.L, (1 - g) * a["YT"], atol=1e-13)
    # expenditure = income + transfer in own currency; shares sum to aT
    assert np.allclose(a["E"], a["I"] + T * np.exp(-nc.full(nu)), atol=1e-13)
    assert np.allclose(a["s"].sum(axis=1), P.aT, atol=1e-13)


def test_symmetric_free_trade_gamma():
    """At the symmetric point, nu = 0 for any gamma; L_T solves
    w L_N = (1 - aT)(Y_T + w L_N), i.e. L_T = gamma aT L / (gamma aT + 1 - aT)."""
    P = nc.symmetric(3, rho=4.0)
    for g in (0.5, 0.75, 1.0):
        nu, LT = ex.solve(P, gamma=g)
        assert np.max(np.abs(nu)) < 1e-13
        assert np.allclose(LT, g * 0.4 / (g * 0.4 + 0.6), atol=1e-13)


def test_transfer_helper_and_sign():
    P = nc.symmetric(3, rho=4.0)
    T = ex.transfer(P, 0, 1, 0.03)
    assert np.allclose(T, [0.03, -0.03, 0.0])
    nu, LT = ex.solve(P, T=T)
    a = ex.allocation(nc.full(nu), LT, P, np.zeros((3, 3)), T=T)
    assert a["TB"][0] < 0 and a["TB"][1] > 0          # A runs the deficit
    assert nu[0] < 0                                   # payer B depreciates: e_AB falls (orthodox transfer effect)
