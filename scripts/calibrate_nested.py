"""
Phase 3: import-share calibration of the nested (eta, rho) model.

For each configuration {A = USA, B = CHN, C in {EU, VNM, ROW}}:

  * Country-specific expenditure shares on partners from data
    (share_ij = goods imports_ij / nominal GDP_i, 2024, importer-reported;
    see data/calibration_inputs.json for sources and caveats).
  * alpha_T = 0.40 for all; home tradable share alpha_D_i and import-bundle
    origin weights b_ij implied by the two partner shares.
  * The demand system is INVERTED at the model's free-trade equilibrium:
    preference weights are iterated until the equilibrium realized shares
    match the data shares (with unequal sizes, equilibrium prices differ
    from 1, so weights != shares; see REVISION_PLAN 3.6).
  * Sizes L_i from PPP GDP as before.

Outputs data/calibration_nested.json: for each configuration and each rho
on the grid (eta = 1.5 baseline), Regime 1 / Regime 2 changes in log e and
log q for all three bilaterals, plus the configuration's reversal
thresholds (marginal and cumulative at each regime's tariff).

Run:  python scripts/calibrate_nested.py
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tariff_exchange_rates.nested import (  # noqa: E402
    compute_allocation_nested, make_params_nested, solve_3country_nested,
)

ALPHA_T = 0.40
ETA = 1.5

REGIMES = {
    "regime1": {"tau_AB": 0.20, "tau_BA": 0.00, "tau_AC": 0.00},
    "regime2": {"tau_AB": 1.45, "tau_BA": 1.25, "tau_AC": 0.10},
    # Regime 3: rates in force at the December 2025 window (post-Geneva truce
    # and the November 10, 2025 fentanyl cut): US on China 10% reciprocal +
    # 10% fentanyl = 20% incremental; China on US 10%; US on C from the 2025
    # framework deals: EU 15%, Vietnam 20%, ROW ~15% (approximate trade-
    # weighted mix of the 10% baseline / 15% floor / higher country rates).
    "regime3": {"tau_AB": 0.20, "tau_BA": 0.10,
                "tau_AC": {"EU": 0.15, "VNM": 0.20, "VNM_adj": 0.20,
                           "ROW": 0.15}},
    # Regime 2a: the April 2, 2025 ANNOUNCED reciprocal rates on C (paused
    # April 9), for the expectations-pricing variant: EU 20%, Vietnam 46%.
    # ROW announced average is ambiguous; variant reported for EU/VNM only.
    "regime2a": {"tau_AB": 1.45, "tau_BA": 1.25,
                 "tau_AC": {"EU": 0.20, "VNM": 0.46, "VNM_adj": 0.46,
                            "ROW": 0.10}},
}


def load_inputs():
    with open(ROOT / "data" / "calibration_inputs.json") as f:
        return json.load(f)


def data_shares(inp, trio, import_scale=None):
    """Target expenditure share matrix s[i][j] (share of total income of i
    spent on j's goods), i, j in trio order [A, B, C]. Home shares fill the
    tradable residual: s[i][i] = alpha_T - sum of partner shares.
    import_scale[(i_name, j_name)] optionally scales a bilateral flow
    (used for the Vietnam processing-trade adjustment)."""
    gdp = inp["gdp_nominal_2024"]
    M = inp["goods_imports_2024"]
    import_scale = import_scale or {}
    n = len(trio)
    s = np.zeros((n, n))
    for i, ci in enumerate(trio):
        for j, cj in enumerate(trio):
            if ci == cj:
                continue
            scale = import_scale.get((ci, cj), 1.0)
            s[i, j] = scale * M[ci][cj] / gdp[ci]
        s[i, i] = ALPHA_T - s[i].sum()
        if s[i, i] <= 0:
            raise ValueError(
                f"{ci}: partner import shares exceed alpha_T "
                f"({s[i].sum() - s[i, i]:.3f} > {ALPHA_T}) — see the "
                f"processing-trade caveat in calibration_inputs.json")
    return s


def invert_weights(target_shares, L, eta, rho, tol=1e-9, max_iter=200):
    """Find (alpha_D_i, beta_ij) such that the model's FREE-TRADE equilibrium
    realized shares equal target_shares. Multiplicative updating on the
    weight matrix; returns (alpha_D, beta, achieved shares, params)."""
    n = 3
    W = target_shares / ALPHA_T          # within-tradables weight matrix guess
    eq_init = None
    for _ in range(max_iter):
        alpha_D = np.diag(W).copy()
        beta = W * (1.0 - np.eye(n))
        beta = beta / beta.sum(axis=1, keepdims=True)
        p = make_params_nested(ALPHA_T, alpha_D, eta, rho, labor=L, beta=beta)
        eq = solve_3country_nested(p, np.zeros((3, 3)), init=eq_init)
        eq_init = [eq["log_e_AB"], eq["log_e_AC"]]
        realized = eq["allocation"]["shares"]          # shares of income
        gap = np.max(np.abs(realized - target_shares))
        if gap < tol:
            return alpha_D, beta, realized, p
        ratio = target_shares / np.maximum(realized, 1e-12)
        W = W * ratio ** 0.7                           # damped multiplicative step
        W = W / W.sum(axis=1, keepdims=True)           # rows sum to 1
    # The multiplicative iteration stalls near the equilibrium solver's own
    # precision; accept any gap that is economically negligible.
    if gap < 1e-6:
        return alpha_D, beta, realized, p
    raise RuntimeError(f"weight inversion did not converge (gap {gap:.2e})")


def tariff_matrix(reg, config=None):
    T = np.zeros((3, 3))
    T[0, 1] = reg["tau_AB"]
    T[1, 0] = reg["tau_BA"]
    tac = reg["tau_AC"]
    T[0, 2] = tac[config] if isinstance(tac, dict) else tac
    return T


def solve_changes(params, T, base_eq):
    """Percent changes in e and log-point changes in q vs free trade."""
    eq = solve_3country_nested(params, T,
                               init=[base_eq["log_e_AB"], base_eq["log_e_AC"]])
    out = {}
    for k in ("AB", "AC", "BC"):
        out[f"de_{k}"] = round(
            100 * (np.exp(eq[f"log_e_{k}"] - base_eq[f"log_e_{k}"]) - 1), 4)
        out[f"dq_{k}"] = round(
            100 * (np.exp(eq[f"log_q_{k}"] - base_eq[f"log_q_{k}"]) - 1), 4)
    out["residual"] = float(eq["residual_norm"])
    return out


def config_thresholds(target_shares, L, eta, regimes):
    """Reversal thresholds for this configuration: marginal (tau -> 0) and
    cumulative at each regime's tau_AB (isolated-tariff experiment), from
    re-inverted weights at each candidate rho."""
    def d_or_cum(rho, tau=None):
        aD, beta, _, p = invert_weights(target_shares, L, eta, rho)
        T0 = np.zeros((3, 3))
        eq0 = solve_3country_nested(p, T0)
        if tau is None:                                   # marginal
            h = 1e-5
            T1 = np.zeros((3, 3)); T1[0, 1] = h
            eq1 = solve_3country_nested(
                p, T1, init=[eq0["log_e_AB"], eq0["log_e_AC"]])
            return (eq1["log_e_AC"] - eq0["log_e_AC"]) / h
        T1 = np.zeros((3, 3)); T1[0, 1] = tau
        eq1 = solve_3country_nested(
            p, T1, init=[eq0["log_e_AB"], eq0["log_e_AC"]])
        return eq1["log_e_AC"] - eq0["log_e_AC"]

    out = {}
    for label, tau in [("marginal", None), ("cum_tau020", 0.20),
                       ("cum_tau145", 1.45)]:
        try:
            out[label] = round(brentq(lambda r: d_or_cum(r, tau), 1.05, 15.0,
                                      xtol=1e-4), 3)
        except ValueError:
            out[label] = None                             # no crossing in range
    return out


def run():
    inp = load_inputs()
    Lmap = inp["gdp_ppp_2024_L"]
    rho_grid = inp["elasticities"]["rho_grid"]

    configs = {
        "EU":  (["USA", "CHN", "EU"], None),
        "VNM": (["USA", "CHN", "VNM"], None),
        # Processing-trade adjustment: only ~half of Vietnam's gross imports
        # from China are final absorption (the rest is re-export content);
        # see calibration_inputs.json meta.principles.
        "VNM_adj": (["USA", "CHN", "VNM"], {("VNM", "CHN"): 0.5}),
        "ROW": (["USA", "CHN", "ROW"], None),
    }

    results = {}
    for name, (trio, scale) in configs.items():
        L = tuple(Lmap[c] for c in trio)
        s = data_shares(inp, trio, scale)
        print(f"\n=== {name}: trio {trio}, L = {np.round(L, 3)} ===")
        print("  target shares (of income):")
        for i, ci in enumerate(trio):
            print(f"    {ci:4s}: " + "  ".join(
                f"{trio[j]}={s[i, j]*100:5.2f}%" for j in range(3)))
        alpha_D_print = np.diag(s) / ALPHA_T
        print(f"  implied home tradable shares alpha_D: "
              + "  ".join(f"{trio[i]}={alpha_D_print[i]:.3f}" for i in range(3)))

        cfg = {"trio": trio, "L": list(L),
               "target_shares": s.round(6).tolist(),
               "alpha_D_data": alpha_D_print.round(4).tolist(),
               "eta": ETA, "rho_results": {}}

        for rho in rho_grid:
            aD, beta, realized, p = invert_weights(s, L, ETA, rho)
            base_eq = solve_3country_nested(p, np.zeros((3, 3)))
            entry = {"alpha_D_weights": np.round(aD, 5).tolist(),
                     "share_fit_gap": float(np.max(np.abs(realized - s)))}
            for rk, reg in REGIMES.items():
                entry[rk] = solve_changes(p, tariff_matrix(reg, name), base_eq)
            cfg["rho_results"][str(rho)] = entry
            r2 = entry["regime2"]
            print(f"  rho={rho:4.1f}: R2 de_AB={r2['de_AB']:+6.2f} "
                  f"de_AC={r2['de_AC']:+6.2f} dq_AC={r2['dq_AC']:+6.2f}")

        print("  thresholds ...", end=" ", flush=True)
        cfg["rho_star"] = config_thresholds(s, L, ETA, REGIMES)
        print(cfg["rho_star"])
        results[name] = cfg

    payload = {
        "meta": {
            "description": "Nested-model calibration on 2024 import shares "
                           "(demand system inverted at the free-trade "
                           "equilibrium); see calibration_inputs.json",
            "alpha_T": ALPHA_T, "eta": ETA, "regimes": REGIMES,
            "conventions": "de/dq: percent changes vs free trade; positive "
                           "= depreciation of first-named currency",
        },
        "configs": results,
    }
    out = ROOT / "data" / "calibration_nested.json"
    with open(out, "w") as f:
        json.dump(payload, f, indent=1)
    print(f"\nWritten to {out}")


if __name__ == "__main__":
    np.seterr(all="ignore")
    run()
