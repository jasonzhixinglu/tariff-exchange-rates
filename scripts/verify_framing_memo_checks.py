"""
Resolve the computable open items of the framing memo (revision_framing_memo.md).

1. rho* for the real rate q vs the nominal rate e (memo section 3.4 / open item):
   they DIFFER — rho*(q) > rho*(e), because the tariff mechanically raises A's
   tariff-inclusive CPI, absorbing part of the nominal depreciation.

2. Threshold under non-zero steady-state NFA, TB_i = -b_i (memo section 3.2 /
   open item): the memo's claim that imbalances "shift the level but not the
   comparative static" is WRONG — the threshold location moves substantially
   with the baseline imbalance (structure survives via the general-baseline
   quadratic of scripts/derive_general_threshold.py).

Run:  python scripts/verify_framing_memo_checks.py
"""

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, fsolve

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from tariff_exchange_rates.nested import (  # noqa: E402
    make_params_nested, solve_3country_nested,
)
from verify_referee_claims import (  # noqa: E402
    isolated, nested_trade_balances, zero_tau,
)

AD, AT, ETA = 0.80, 0.40, 1.5


def d_dtau(rho, key, L=(1, 1, 1), h=1e-6):
    """d <key> / d tau at tau = 0 for an isolated tariff (package model)."""
    p = make_params_nested(alpha_T=AT, alpha_D=AD, eta=ETA, rho=rho, labor=L)
    T0, T1 = np.zeros((3, 3)), np.zeros((3, 3))
    T1[0, 1] = h
    e0 = solve_3country_nested(p, T0)
    e1 = solve_3country_nested(p, T1, init=[e0["log_e_AB"], e0["log_e_AC"]])
    return (e1[key] - e0[key]) / h


def check_real_rate_threshold():
    print("1. Nominal vs CPI-real reversal threshold "
          f"(aD={AD}, aT={AT}, eta={ETA}, equal sizes)")
    rs_e = brentq(lambda r: d_dtau(r, "log_e_AC"), 2, 8, xtol=1e-6)
    rs_q = brentq(lambda r: d_dtau(r, "log_q_AC"), 2, 8, xtol=1e-6)
    print(f"   rho*(e) = {rs_e:.4f}    rho*(q) = {rs_q:.4f}")
    assert abs(rs_e - 3.96) < 1e-3
    assert rs_q > rs_e + 0.5
    print("   [OK] rho*(q) > rho*(e): the tariff raises A's tariff-inclusive")
    print("        CPI, so real depreciation against C needs more diversion.\n")


def check_nfa_thresholds():
    print("2. Threshold under permanent imbalances TB_i = -b_i "
          "(b in units of A's baseline income)")

    def eq_nfa(tau, rho, b):
        f = lambda x: (nested_trade_balances(x, tau, AD, AT, ETA, rho, [1, 1, 1])[1:]
                       + np.array([b[1], b[2]]))
        return fsolve(f, [0.0, 0.0], xtol=1e-13)

    def thr(b, lo=2.0, hi=9.0, h=1e-6):
        def slope(rho):
            x0 = eq_nfa(zero_tau(), rho, b)
            x1 = eq_nfa(isolated(h), rho, b)
            return (x1[1] - x0[1]) / h
        return brentq(slope, lo, hi, xtol=1e-6)

    cases = [
        ("balanced",                    [0.00,  0.00,  0.00], 3.96),
        ("A deficit 3% vs B",           [0.03, -0.03,  0.00], 5.10),
        ("A deficit 3% vs C",           [0.03,  0.00, -0.03], 4.64),
        ("A deficit 6% vs B+C",         [0.06, -0.03, -0.03], 7.07),
        ("A surplus 3% vs B",           [-0.03, 0.03,  0.00], 3.42),
    ]
    for label, b, ref in cases:
        rs = thr(b)
        print(f"   {label:22s} rho* = {rs:5.2f}   (recorded: {ref})")
        assert abs(rs - ref) < 0.02
    print("   [OK] the threshold LOCATION moves substantially with the baseline")
    print("        imbalance; only the structure (reversal iff rho > threshold)")
    print("        is invariant. Memo section 3.2's neutrality sentence must be")
    print("        replaced by the general-baseline argument.")


if __name__ == "__main__":
    np.seterr(all="ignore")
    check_real_rate_threshold()
    check_nfa_thresholds()
    print("\nAll memo checks reproduced.")
