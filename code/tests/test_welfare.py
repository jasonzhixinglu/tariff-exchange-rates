"""Lemma 4.1: at free trade, the first-order change in A's money-metric
utility equals -m_A sum_j b_Aj d nu_j, for any tariff vector.

Utility is Cobb-Douglas over tradables and non-tradables with CES tradable
and import price indices and income including rebated tariff revenue
(nested_ces.allocation()['logV'], the log of indirect utility up to a
constant).  The derivative is taken by central finite differences of the
nonlinear solver."""
import numpy as np
import pytest

from model import linear as lin
from model import nested_ces as nc

from test_linearization import random_prims

H = 1e-4


def fd_welfare(P, nu0, d):
    def logV(tau):
        nu = nc.solve(P, tau, nu0=nu0)
        return nc.allocation(nc.full(nu), P, tau)["logV"].real[0]
    return (logV(H * d) - logV(-H * d)) / (2 * H)


def shocks(N):
    out = {}
    d = np.zeros((N, N)); d[0, 1] = 1.0; out["unilateral"] = d
    d = np.zeros((N, N)); d[0, 1] = d[1, 0] = 1.0; out["retaliation"] = d
    d = np.zeros((N, N)); d[0, 1:] = 1.0; d[1:, 0] = 1.0; out["war"] = d
    d = np.zeros((N, N)); d[1, 2] = 1.0; out["foreign only"] = d
    rng = np.random.default_rng(N)
    d = rng.uniform(0, 1, (N, N)); np.fill_diagonal(d, 0.0); out["random"] = d
    return out


CASES = [("sym", 3, 0), ("sym", 5, 0), ("asym", 3, 21), ("asym", 3, 22), ("asym", 4, 23), ("asym", 5, 24)]


@pytest.mark.parametrize("kind,N,seed", CASES)
def test_lemma_41(kind, N, seed):
    P = nc.symmetric(N, rho=5.0) if kind == "sym" else random_prims(N, seed)
    nu0 = nc.solve(P)
    base = nc.baseline_shares(P, nu0)
    mA = base["aT"][0] * (1 - base["h"][0])
    bA = lin.import_weights(base)
    for name, d in shocks(N).items():
        dnu = lin.response(base, d)
        lemma = -mA * bA @ dnu
        fd = fd_welfare(P, nu0, d)
        assert abs(fd - lemma) < 1e-6, (name, fd, lemma)
        assert abs(lin.welfare_change(base, d) - lemma) < 1e-13
