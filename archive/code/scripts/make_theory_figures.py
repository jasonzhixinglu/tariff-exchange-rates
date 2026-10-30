# -*- coding: utf-8 -*-
"""Generate the two theoretical figures for notes/model_derivations.tex.

Every line, slope, shift and point is computed from the model equations, so
the figures are quantitatively consistent with the text:

  Fig 1  generic bilateral adjustment in (dnu, dTB_A) space
         dTB_A = TB_Anu dnu + TB_Atau dtau; drawn with the nested-CES
         values TB_Anu = m M_2, TB_Atau = m rho_D, but labelled generically

  Fig 2  average protection / relative treatment decomposition at N = 3
         (dtau, 0) = (dtau/2, dtau/2) + (dtau/2, -dtau/2)
         dnu   = lambda_A (dtau/2) 1 + lambda_R (dtau/2, -dtau/2)
         F/j_S = lambda_A (dtau/2) 1 + 3 lambda_R (dtau/2, -dtau/2)
         with the two components orthogonal in (dnu_B, dnu_C) space.
         (Written to fig3_decomposition.pdf, the name the .tex includes.)

Run:  python scripts/make_theory_figures.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "cm",
    "axes.linewidth": 0.8,
    "font.size": 9,
    "pdf.fonttype": 42,
})

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "notes", "figures")

# ---------------------------------------------------------------- parameters
aD, aT, eta = 0.70, 0.60, 1.50
m = aT * (1.0 - aD)
rhoD = aD * eta + (1.0 - aD) * (1.0 - aT)             # domestic diversion margin
M2 = 1.0 + 2.0 * aD * (eta - 1.0)
RHO_MID, RHO_HIGH = 2.2, 5.0                          # rhoD < 2.2 < 3 rhoD < 5


def M3(rho):
    return (3.0 * aD * (eta - 1.0) + rho + 1.0) / 2.0


def lam_A(rho):
    return -rhoD / M3(rho)


def lam_R(rho):
    return -rho / (3.0 * M3(rho))


INK = "0.10"
MID = "0.45"
GREY = "0.62"
DASH = (0, (4.5, 2.5))
DOT = (0, (1, 2))


def _frame(ax, xlim, ylim, xlabel, ylabel, equal=False):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    ax.axhline(0.0, color=INK, lw=0.7, zorder=1)
    ax.axvline(0.0, color=INK, lw=0.7, zorder=1)
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(xlim[1], 0.012 * (ylim[1] - ylim[0]), xlabel,
            ha="right", va="bottom", fontsize=9)
    ax.text(0.012 * (xlim[1] - xlim[0]), ylim[1], ylabel,
            ha="left", va="top", fontsize=9)


def _line_point(slope, intercept, xlim, ylim, frac, pad=0.06):
    """A point on y = slope x + intercept that sits inside the window.
    frac = 0 is the left-most admissible x, frac = 1 the right-most."""
    xs = [xlim[0] + pad * (xlim[1] - xlim[0]),
          xlim[1] - pad * (xlim[1] - xlim[0])]
    lo, hi = ylim[0] + pad * (ylim[1] - ylim[0]), ylim[1] - pad * (ylim[1] - ylim[0])
    if abs(slope) > 1e-12:
        xa, xb = (lo - intercept) / slope, (hi - intercept) / slope
        xs = [max(xs[0], min(xa, xb)), min(xs[1], max(xa, xb))]
    x = xs[0] + frac * (xs[1] - xs[0])
    return x, slope * x + intercept


# ------------------------------------------------------------------- Figure 1
def figure1(dtau=0.20):
    shift = m * rhoD * dtau                 # TB_Atau * dtau
    slope = m * M2                          # TB_Anu
    nu_star = -rhoD / M2 * dtau             # post-tariff equilibrium

    xlim, ylim = (-0.30, 0.27), (-0.105, 0.125)
    fig, ax = plt.subplots(figsize=(4.7, 3.3))
    x = np.linspace(xlim[0], xlim[1], 200)
    ax.plot(x, slope * x, color=GREY, lw=1.3, ls=DASH, zorder=3)
    ax.plot(x, slope * x + shift, color=INK, lw=1.5, zorder=3)
    _frame(ax, xlim, ylim, r"$d\nu=d\log e_{AB}$", r"$d\mathrm{TB}_A$")

    # (i) tariff shifts the schedule up at unchanged exchange rates
    ax.annotate("", xy=(0, shift), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2,
                                shrinkA=0, shrinkB=0))
    ax.plot([0], [0], "o", ms=4.4, mfc="white", mec=INK, mew=1.2, zorder=6)
    ax.plot([0], [shift], "s", ms=4.0, mfc="white", mec=INK, mew=1.2, zorder=6)
    ax.plot([nu_star], [0], "o", ms=4.8, color=INK, zorder=6)

    # (ii) the exchange rate moves back along the new schedule
    ax.annotate("", xy=(nu_star, 0.0), xytext=(0, shift),
                arrowprops=dict(arrowstyle="-|>", color=MID, lw=1.1,
                                shrinkA=5, shrinkB=5,
                                connectionstyle="arc3,rad=-0.3"))

    ax.text(0.014, shift, r"$\mathrm{TB}_{A\tau}\,d\tau$", va="center",
            ha="left", fontsize=9)
    ax.text(0.014, shift - 0.020, "tariff at unchanged\nexchange rates",
            va="top", ha="left", fontsize=7.4, color=MID)
    ax.text(nu_star, -0.012,
            r"$d\nu^{\ast}=-\dfrac{\mathrm{TB}_{A\tau}}{\mathrm{TB}_{A\nu}}\,d\tau$",
            va="top", ha="center", fontsize=9)

    px, py = _line_point(slope, shift, xlim, ylim, 1.0)
    ax.text(px, py + 0.007, "after the tariff", ha="right", va="bottom",
            fontsize=7.8, color=INK)
    px, py = _line_point(slope, 0.0, xlim, ylim, 1.0)
    ax.text(px, py - 0.016, r"before ($d\tau=0$)", ha="right", va="top",
            fontsize=7.8, color=GREY)
    px, py = _line_point(slope, 0.0, xlim, ylim, 0.0)
    ax.text(px + 0.010, py - 0.010,
            "slope $\\mathrm{TB}_{A\\nu}>0$\n(Marshall–Lerner)",
            ha="left", va="top", fontsize=7.8, color=INK)

    fig.tight_layout(pad=0.4)
    fig.savefig(os.path.join(OUT, "fig1_two_country.pdf"))
    plt.close(fig)
    return dict(shift=shift, slope=slope, nu_star=nu_star)


# ------------------------------------------------------------------- Figure 2
def _panel2(ax, rho, tau, title):
    lA, lR = lam_A(rho), lam_R(rho)
    step = lA * tau / 2.0                     # average-protection step
    rel = lR * tau / 2.0                      # relative-treatment step
    Sx, Sy = step, step
    Fx, Fy = step + rel, step - rel           # equilibrium d nu
    Dx, Dy = step + 3.0 * rel, step - 3.0 * rel   # F / j_S (N = 3)

    xlim, ylim = (-1.00, 0.16), (-0.56, 0.66)
    _frame(ax, xlim, ylim, r"$d\nu_B$", r"$d\nu_C$", equal=True)

    # the constant (NEER) direction
    d = np.linspace(-0.56, 0.13, 40)
    ax.plot(d, d, color=GREY, lw=0.8, ls=DOT, zorder=2)
    ax.text(-0.560, -0.572, r"common direction $\mathbf{1}$",
            fontsize=7.2, color=MID, ha="left", va="top", rotation=45,
            rotation_mode="anchor")

    # the zero-sum direction through the average-protection point, drawn
    # only where the legs do not already trace it
    amax = min(abs(rel) + 0.11, Sy - ylim[0] - 0.03, xlim[1] - Sx - 0.02)
    if abs(Sx + amax) < 0.10:                 # keep the label off the axis
        amax = -Sx - 0.02
    a = np.linspace(0.0, amax, 20)
    ax.plot(Sx + a, Sy - a, color=GREY, lw=0.8, ls=DOT, zorder=2)
    ax.text(Sx + amax, Sy - amax + 0.012, "zero-sum",
            fontsize=7.2, color=MID, ha="right", va="bottom", rotation=-45,
            rotation_mode="anchor")

    # disturbance at unchanged exchange rates (dashed), then the solid legs
    ax.plot([Sx, Dx], [Sy, Dy], color=INK, lw=1.3, ls=DASH, zorder=3)
    ax.annotate("", xy=(Sx, Sy), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6,
                                shrinkA=0, shrinkB=0), zorder=5)
    ax.annotate("", xy=(Fx, Fy), xytext=(Sx, Sy),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6,
                                shrinkA=0, shrinkB=0), zorder=5)

    ax.plot([0], [0], "o", ms=4.2, mfc="white", mec=INK, mew=1.2, zorder=7)
    ax.plot([Sx], [Sy], "o", ms=4.2, color=INK, zorder=7)
    ax.plot([Fx], [Fy], "o", ms=5.2, color=INK, zorder=7)
    ax.plot([Dx], [Dy], "s", ms=4.6, mfc="white", mec=INK, mew=1.2, zorder=7)

    ax.text(Sx / 2 + 0.012, Sy / 2 - 0.012,  # along the common arrow, at its midpoint
            r"$\lambda_A\,\bar t\,\mathbf{1}$", ha="center", va="top",
            fontsize=9.5, rotation=45, rotation_mode="anchor")
    ax.text((Sx + Fx) / 2 - 0.032, (Sy + Fy) / 2 - 0.032,
            r"$\lambda_R\,\tilde t$", ha="right", va="top", fontsize=9.5)
    ax.text((Fx + Dx) / 2 + 0.030, (Fy + Dy) / 2 + 0.030,
            r"$3\lambda_R\,\tilde t$", ha="left", va="bottom", fontsize=9.5)
    ax.text(Sx + 0.028, Sy - 0.028,
            r"$d\nu_A^E=\lambda_A\bar t$", ha="left", va="top", fontsize=8)
    ax.text(Fx + 0.030, Fy + 0.030, r"$d\boldsymbol{\nu}$", ha="left",
            va="bottom", fontsize=10)
    ax.text(Dx - 0.022, Dy + 0.022, r"$\boldsymbol{F}/j_S$", ha="right",
            va="bottom", fontsize=9.5)

    # heights above the axis: the bystander response and its disturbance
    for y, lab in ((Fy, r"$d\nu_C$"), (Dy, r"$F_C>0$")):
        x0 = Fx if y == Fy else Dx
        ax.plot([x0, 0], [y, y], color=GREY, lw=0.6, ls=DOT, zorder=2)
        ax.text(0.014, y + (0.014 if y > 0 else -0.014), lab,
                ha="left", va="bottom" if y > 0 else "top",
                fontsize=8, color=MID)

    ax.set_title(title, fontsize=8.8, pad=8)
    return dict(S=(Sx, Sy), F=(Fx, Fy), D=(Dx, Dy), lam_A=lA, lam_R=lR)


def figure2(tau=1.0):
    fig, axes = plt.subplots(1, 2, figsize=(6.7, 4.05), layout="constrained")
    out = {}
    out["mid"] = _panel2(
        axes[0], RHO_MID, tau,
        r"(a) $\rho_D<\rho<3\rho_D$:  $d\nu_C<0$ although $F_C>0$")
    out["high"] = _panel2(axes[1], RHO_HIGH, tau,
                          r"(b) $\rho>3\rho_D$:  $d\nu_C>0$")
    fig.suptitle(r"$\mathbf{t}=(d\tau,0)=(d\tau/2,\ d\tau/2)+(d\tau/2,\ -d\tau/2)$",
                 y=0.035, fontsize=8, color=MID)
    fig.savefig(os.path.join(OUT, "fig3_decomposition.pdf"))
    plt.close(fig)
    return out


# ------------------------------------------------------------------- checks
def selfcheck(r1, r2):
    """Every plotted point must equal the closed form in the text."""
    dtau = 0.20
    assert abs(r1["nu_star"] - (-rhoD / M2 * dtau)) < 1e-12
    assert rhoD < RHO_MID < 3 * rhoD < RHO_HIGH
    for key, rho in (("mid", RHO_MID), ("high", RHO_HIGH)):
        m3 = M3(rho)
        nuB = -(rho + 3 * rhoD) / (6 * m3)
        nuC = (rho - 3 * rhoD) / (6 * m3)
        # the decomposition lands on the closed-form equilibrium
        assert abs(r2[key]["F"][0] - nuB) < 1e-12
        assert abs(r2[key]["F"][1] - nuC) < 1e-12
        # the average-protection component carries the whole NEER response
        assert abs(r2[key]["S"][0] - (-rhoD / (2 * m3))) < 1e-12
        # the two components are orthogonal in (nu_B, nu_C) space
        Sv = np.array(r2[key]["S"])
        Rv = np.array(r2[key]["F"]) - Sv
        assert abs(float(Sv @ Rv)) < 1e-14
        # F / j_S from (3c-JF): F = -(m/4)(rho + rho_D, rho_D - rho), j_S = m M_3 / 2
        FjS = -np.array([rho + rhoD, rhoD - rho]) / (2 * m3)
        assert np.allclose(r2[key]["D"], FjS, atol=1e-12)
        assert abs(r2[key]["D"][1] - (rho - rhoD) / (2 * m3)) < 1e-12
    for key in ("mid", "high"):
        r = r2[key]
        print("fig2 %-4s K = (%+.4f, %+.4f)  dnu = (%+.4f, %+.4f)  F/j_S = (%+.4f, %+.4f)"
              % ((key,) + r["S"] + r["F"] + r["D"]))
    print("rho_D = %.4f,  3 rho_D = %.4f,  M_2 = %.4f" % (rhoD, 3 * rhoD, M2))
    print("all figure self-checks passed")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    r1, r2 = figure1(), figure2()
    selfcheck(r1, r2)
    print("written to", OUT)
