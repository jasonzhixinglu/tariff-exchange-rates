"""
Tariff matrix construction for the 3-country model.

A tariff matrix is a 3×3 numpy array where entry [i, j] is the ad valorem
rate imposed by country i on goods imported from country j. Diagonal entries
are always zero (no self-tariff).

Countries are indexed 0 = A, 1 = B, 2 = C throughout.
"""

import numpy as np


def make_tariff_matrix(
    tau_AB=0.0, tau_BA=0.0,
    tau_AC=0.0, tau_CA=0.0,
    tau_BC=0.0, tau_CB=0.0,
):
    """
    Build a 3×3 tariff matrix from bilateral rates.

    Parameters
    ----------
    tau_AB : A's tariff on B's goods
    tau_BA : B's tariff on A's goods
    tau_AC : A's tariff on C's goods
    tau_CA : C's tariff on A's goods
    tau_BC : B's tariff on C's goods
    tau_CB : C's tariff on B's goods

    Returns
    -------
    np.ndarray, shape (3, 3)
    """
    return np.array([
        [0.0,    tau_AB, tau_AC],
        [tau_BA, 0.0,    tau_BC],
        [tau_CA, tau_CB, 0.0   ],
    ])


def free_trade():
    """All tariffs zero."""
    return make_tariff_matrix()


def uniform_tariff(tau):
    """Country A imposes tau symmetrically on both B and C."""
    return make_tariff_matrix(tau_AB=tau, tau_AC=tau)


def isolated_tariff(tau):
    """Country A imposes tau on B only; all other rates zero."""
    return make_tariff_matrix(tau_AB=tau)


def trade_war(tau):
    """Countries A and B impose tau on each other; C faces no new tariffs."""
    return make_tariff_matrix(tau_AB=tau, tau_BA=tau)
