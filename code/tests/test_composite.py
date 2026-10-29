"""Proposition 3.6: the symmetric N-country economy reduces exactly (to first
order) to a three-country economy with a composite bystander."""
import numpy as np
import pytest
from scipy.optimize import brentq

from model import closed_forms as cf
from model import linear as lin

PARAMS = [(0.8, 0.4, 1.5), (0.6, 0.7, 1.2), (0.9, 0.3, 3.0), (0.5, 0.5, 2.0)]
NS = range(4, 11)
RHOS = (1.1, 4.0, 9.0)


def shocks(N):
    """The four shocks in the N-country and the composite economy."""
    out = {}
    d = np.zeros((N, N)); d[0, 1] = 1.0
    c = np.zeros((3, 3)); c[0, 1] = 1.0
    out["A on B"] = (d, c)
    d = np.zeros((N, N)); d[0, 1] = d[1, 0] = 1.0
    c = np.zeros((3, 3)); c[0, 1] = c[1, 0] = 1.0
    out["A-B war"] = (d, c)
    d = np.zeros((N, N)); d[0, 2:] = 1.0
    c = np.zeros((3, 3)); c[0, 2] = 1.0
    out["A on all bystanders"] = (d, c)
    d = np.zeros((N, N)); d[2:, 1] = 1.0
    c = np.zeros((3, 3)); c[2, 1] = 1.0
    out["all bystanders on B"] = (d, c)
    return out


@pytest.mark.parametrize("N", NS)
@pytest.mark.parametrize("aD,aT,eta", PARAMS)
def test_exact_reduction(N, aD, aT, eta):
    for rho in RHOS:
        full_base = lin.symmetric_base(N, aD=aD, aT=aT, eta=eta, rho=rho)
        comp = cf.composite_base(N, aD, aT, eta, rho)
        assert np.max(np.abs(lin.balance_residual(comp))) < 1e-14
        for name, (d, c) in shocks(N).items():
            dn = lin.response(full_base, d)
            dc = lin.response(comp, c)
            assert np.max(np.abs(dn[1:] - dn[1])) < 1e-12, name   # bystanders move together
            assert abs(dn[0] - dc[0]) < 1e-12, (name, dn[0], dc[0])
            assert abs(dn[1] - dc[1]) < 1e-12, (name, dn[1], dc[1])
            # NEER: equal weights in N countries = trade weights in the composite
            w = lin.trade_weights(comp)
            assert abs(dn.mean() - w @ dc) < 1e-12


@pytest.mark.parametrize("N", NS)
def test_reduced_system(N):
    aD, aT, eta = 0.8, 0.4, 1.5
    for rho in RHOS:
        comp = cf.composite_base(N, aD, aT, eta, rho)
        # (3.10): -J of the composite economy
        A, c = cf.composite_system(N, aD, aT, eta, rho)
        assert np.max(np.abs(-lin.reduced_jacobian(comp) - A)) < 1e-13
        assert abs(np.linalg.det(A) - c ** 2 * N * (N - 2)) < 1e-13
        # (3.11) and the unilateral disturbances
        cc = np.zeros((3, 3)); cc[0, 1] = 1.0
        F = lin.disturbance(comp, cc)
        mm, rD = cf.m(aD, aT), cf.rhoD(aD, aT, eta)
        FB = -mm * (rD + (N - 2) * rho) / (N - 1) ** 2
        Fc = mm * (rho - rD) / (N - 1) ** 2
        assert abs(F[0] - FB) < 1e-13 and abs(F[1] - (N - 2) * Fc) < 1e-13
        dnu = lin.response(comp, cc)
        assert abs(dnu[1] - (FB + (N - 1) * Fc) / (c * N)) < 1e-12
        assert abs(dnu[0] - (2 * FB + (N - 2) * Fc) / (c * N)) < 1e-12


def ordinary_threshold(N, aD=0.8, aT=0.4, eta=1.5):
    cc = np.zeros((3, 3)); cc[0, 1] = 1.0
    f = lambda r: lin.response(cf.composite_base(N, aD, aT, eta, r, ordinary_eta=True), cc)[1]
    return brentq(f, 1.0001, 30.0, xtol=1e-12)


def test_ordinary_eta_thresholds():
    vals = {N: ordinary_threshold(N) for N in (3, 4, 5, 8)}
    assert abs(vals[3] - 3.96) < 1e-9
    # The draft (Table 1) states 3.82, 3.77, 3.71.  N = 5 is 3.7648, i.e. 3.76
    # at two decimals; the draft's 3.77 is off by one in the last digit.
    assert [round(vals[N], 4) for N in (4, 5, 8)] == [3.8177, 3.7648, 3.7092]
    assert max(abs(vals[N] - v) for N, v in zip((4, 5, 8), (3.82, 3.77, 3.71))) < 0.006
    assert vals[4] > vals[5] > vals[8]


def test_eta_C_column():
    assert [round(cf.eta_C(N, 0.8, 1.5, 4.0), 2) for N in (3, 4, 5, 8)] == [1.50, 2.46, 2.89, 3.39]
