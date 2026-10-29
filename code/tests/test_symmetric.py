"""At the symmetric benchmark the linear solver reproduces Theorem 3.2,
Propositions 3.3, 3.5 and 3.7 and Corollary 3.4, for N = 2, ..., 8."""
import numpy as np
import pytest
from scipy.optimize import brentq

from model import closed_forms as cf
from model import linear as lin

PARAMS = [cf.US_LIKE, cf.FIG2, dict(aD=0.6, aT=0.7, eta=1.2), dict(aD=0.9, aT=0.3, eta=3.0)]
RHOS = [1.1, 2.5, 4.0, 9.0]
NS = range(3, 9)


def e(N, i, j):
    d = np.zeros((N, N)); d[i, j] = 1.0
    return d


def test_two_country():
    for p in PARAMS:
        base = lin.symmetric_base(2, rho=2.0, **p)
        r = lin.response(base, e(2, 0, 1))[0]
        assert abs(r + cf.rhoD(**p) / cf.M2(p["aD"], p["eta"])) < 1e-13
        assert abs(cf.MN(2, p["aD"], p["eta"], 7.0) - cf.M2(p["aD"], p["eta"])) < 1e-14


@pytest.mark.parametrize("N", NS)
@pytest.mark.parametrize("p", PARAMS)
def test_lemma_A1_and_eigenvalues(N, p):
    for rho in RHOS:
        base = lin.symmetric_base(N, rho=rho, **p)
        mm, M = cf.m(p["aD"], p["aT"]), cf.MN(N, p["aD"], p["eta"], rho)
        Jt = lin.full_jacobian(base)
        expect = np.full((N, N), mm * M / (N - 1)); np.fill_diagonal(expect, -mm * M)
        assert np.max(np.abs(Jt - expect)) < 1e-13
        # tariff disturbance: dTB_i = m/(N-1) [-rho_D tbar - rho (t_i - tbar)]
        rng = np.random.default_rng(N)
        t = rng.normal(size=N - 1)
        d = np.zeros((N, N)); d[0, 1:] = t
        F = lin.disturbance(base, d)
        tbar = t.mean()
        expectF = mm / (N - 1) * (-cf.rhoD(**p) * tbar - rho * (t - tbar))
        assert np.max(np.abs(F - expectF)) < 1e-13
        # Theorem 3.2: d nu = lam_A tbar 1 + lam_R (t - tbar)
        dnu = lin.response(base, d)
        expect_nu = (cf.lamA(N, rho=rho, **p) * tbar
                     + cf.lamR(N, rho=rho, **p) * (t - tbar))
        assert np.max(np.abs(dnu - expect_nu)) < 1e-12
        assert lin.mml(lin.reduced_jacobian(base))


@pytest.mark.parametrize("N", NS)
@pytest.mark.parametrize("p", PARAMS)
def test_unilateral(N, p):
    for rho in RHOS:
        base = lin.symmetric_base(N, rho=rho, **p)
        dnu = lin.response(base, e(N, 0, 1))
        neer, dB, dC = cf.unilateral(N, rho=rho, **p)
        assert abs(dnu[0] - dB) < 1e-12 and np.max(np.abs(dnu[1:] - dC)) < 1e-12
        assert abs(dnu.mean() - neer) < 1e-12 and neer < 0 and dB < 0
        F = lin.disturbance(base, e(N, 0, 1))
        assert abs(F[1] - cf.bystander_disturbance(N, rho=rho, **p)) < 1e-13
    # bystander threshold N rho_D, from the linear solver
    f = lambda r: lin.response(lin.symmetric_base(N, rho=r, **p), e(N, 0, 1))[1]
    thr = brentq(f, 0.5, 200.0, xtol=1e-13)
    assert abs(thr - N * cf.rhoD(**p)) < 1e-9


@pytest.mark.parametrize("N", NS)
def test_k_partners(N):
    p = cf.US_LIKE
    for k in range(1, N - 1):
        d = np.zeros((N, N)); d[0, 1:k + 1] = 1.0
        for rho in RHOS:
            dnu = lin.response(lin.symmetric_base(N, rho=rho, **p), d)
            dB, dC, neer = cf.k_partners(N, k, rho=rho, **p)
            assert np.max(np.abs(dnu[:k] - dB)) < 1e-12
            assert np.max(np.abs(dnu[k:] - dC)) < 1e-12
            assert abs(dnu.mean() - neer) < 1e-12
        f = lambda r: lin.response(lin.symmetric_base(N, rho=r, **p), d)[k]
        assert abs(brentq(f, 0.5, 200.0, xtol=1e-13) - N * cf.rhoD(**p)) < 1e-9
    # relative treatment: depreciation against j iff t_j / tbar < 1 - N rho_D / rho
    rng = np.random.default_rng(3)
    for _ in range(20):
        t = rng.uniform(0, 1, N - 1); rho = rng.uniform(1.1, 15)
        d = np.zeros((N, N)); d[0, 1:] = t
        dnu = lin.response(lin.symmetric_base(N, rho=rho, **p), d)
        pred = t / t.mean() < 1 - N * cf.rhoD(**p) / rho
        assert np.all((dnu > 0) == pred)


@pytest.mark.parametrize("N", NS)
@pytest.mark.parametrize("p", PARAMS)
def test_retaliation_and_war(N, p):
    d = e(N, 0, 1) + e(N, 1, 0)
    war = np.zeros((N, N)); war[0, 1:] = 1.0; war[1:, 0] = 1.0
    for rho in RHOS:
        base = lin.symmetric_base(N, rho=rho, **p)
        dnu = lin.response(base, d)
        dB, dC, neer = cf.retaliation(N, rho=rho, **p)
        assert abs(dnu[0]) < 1e-12
        assert np.max(np.abs(dnu[1:] - dC)) < 1e-12
        assert abs(dnu.mean() - neer) < 1e-12
        dw = lin.response(base, war)
        assert np.max(np.abs(dw - cf.multilateral_war(N, rho=rho, **p))) < 1e-12
    f = lambda r: lin.response(lin.symmetric_base(N, rho=r, **p), d)[1]
    assert abs(brentq(f, 0.3, 200.0, xtol=1e-13) - cf.rhoD(**p)) < 1e-9


@pytest.mark.parametrize("N", NS)
def test_real_rates(N):
    p = cf.US_LIKE  # m = 0.08 < 1/N for N <= 8
    for rho in RHOS:
        base = lin.symmetric_base(N, rho=rho, **p)
        dq = lin.real_response(base, e(N, 0, 1))
        qB, qC, qE = cf.real_unilateral(N, rho=rho, **p)
        assert abs(dq[0] - qB) < 1e-12 and np.max(np.abs(dq[1:] - qC)) < 1e-12
        assert abs(dq.mean() - qE) < 1e-12 and qE < 0
    f = lambda r: lin.real_response(lin.symmetric_base(N, rho=r, **p), e(N, 0, 1))[1]
    thr = brentq(f, 0.5, 400.0, xtol=1e-13)
    assert abs(thr - cf.rho_q_star(N, **p)) < 1e-9
    assert thr > N * cf.rhoD(**p)


def test_us_like_values():
    p = cf.US_LIKE
    assert abs(cf.rhoD(**p) - 1.32) < 1e-12
    assert abs(3 * cf.rhoD(**p) - 3.96) < 1e-12
    assert round(cf.rho_q_star(3, **p), 2) == 4.93


@pytest.mark.parametrize("N", NS)
def test_single_elasticity(N):
    # Corollary 3.4: rho = eta = sigma never reverses when alpha_D >= 1/N
    for aD in (1.0 / N, 0.5, 0.8):
        if aD < 1.0 / N:
            continue
        for aT in (0.2, 0.4, 0.9):
            for s in np.linspace(0.6, 30, 60):
                assert cf.unilateral(N, aD, aT, s, s)[2] < 0
    aT, s = 0.4, 2.7
    assert abs(cf.unilateral(N, 1.0 / N, aT, s, s)[2] + (1 - aT) / (N * s)) < 1e-13
