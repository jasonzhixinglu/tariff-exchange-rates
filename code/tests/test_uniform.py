"""Proposition 4.2 (uniform tariffs): at any balanced free-trade baseline at
which MML holds, a uniform marginal tariff by A has disturbance
F_j = -f_Aj rho_D^A < 0 in every entry, appreciates A against every partner,
and raises A's welfare.  The individual welfare-gradient components need not
all be positive."""
import numpy as np
import pytest

from model import linear as lin
from model import nested_ces as nc

from test_linearization import random_prims

SEEDS = [(N, s) for N in (3, 4, 5) for s in range(40, 60)]


def flows_from_A(base):
    B = lin.unpack(base)
    s = B["aT"][0] * (1.0 - B["h"][0]) * B["b"][0]
    return (s * B["y"][0])[1:]


@pytest.mark.parametrize("N,seed", SEEDS)
def test_uniform_tariff_signs(N, seed):
    P = random_prims(N, seed)
    base = nc.baseline_shares(P, nc.solve(P))
    J = lin.reduced_jacobian(base)
    assert lin.mml(J)
    d = lin.uniform_tariff(base)
    F = lin.disturbance(base, d)
    dnu = lin.response(base, d)
    assert np.all(F < 0)
    assert np.all(dnu < 0)
    assert lin.welfare_change(base, d) > 0
    g = lin.welfare_gradient(base)
    assert abs(g.sum() - lin.welfare_change(base, d)) < 1e-13


@pytest.mark.parametrize("N,seed", SEEDS)
def test_uniform_disturbance_closed_form(N, seed):
    P = random_prims(N, seed)
    base = nc.baseline_shares(P, nc.solve(P))
    F = lin.disturbance(base, lin.uniform_tariff(base))
    closed = -flows_from_A(base) * lin.own_rhoD(base)
    assert np.max(np.abs(F - closed)) < 1e-12


@pytest.mark.parametrize("N,seed", [(3, 41), (4, 47), (5, 53)])
def test_uniform_disturbance_exact_model(N, seed):
    """The linear disturbance equals the complex-step derivative of the exact
    model's trade balances along the uniform direction."""
    P = random_prims(N, seed)
    nu = nc.solve(P)
    base = nc.baseline_shares(P, nu)
    d = lin.uniform_tariff(base)
    h = 1e-30
    G = np.imag(nc.trade_balances(nc.full(nu).astype(complex), P,
                                  np.zeros((N, N)) + 1j * h * d))[1:] / h
    assert np.max(np.abs(G - lin.disturbance(base, d))) < 1e-12


def test_component_can_be_negative():
    """Example (b) of Section 4.3 at rho = 5: g_B < 0 < g_B + g_C."""
    from model import asymmetry as asy
    P = asy.three_country_prims(L=(1.0, 0.22, 1.0), beta_AB=0.2, rho=3.96)
    base = lin.with_rho(asy.base_from_prims(P)[0], 5.0)
    g = lin.welfare_gradient(base)
    assert g[0] < 0 < g.sum()
    assert g[1] > 0
