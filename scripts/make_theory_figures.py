# -*- coding: utf-8 -*-
"""Generate the three theoretical figures for notes/model_derivations.tex.

Every line, slope, shift and point is computed from the model equations, so
the figures are quantitatively consistent with the text:

  Fig 1  generic bilateral adjustment in (dnu, dTB_A) space
         dTB_A = TB_Anu dnu + TB_Atau dtau; drawn with the nested-CES
         values TB_Anu = m D_2, TB_Atau = m rho1*, but labelled generically

  Fig 2  three-country adjustment in (nu_B, nu_C) space
         TB_B = 0:  nu_C = 2 nu_B + (rho + rho1*) dtau / D_3
         TB_C = 0:  nu_C = nu_B/2 + (rho - rho1*) dtau / (2 D_3)

  Fig 3  average protection / relative treatment decomposition at N = 3
         (tau, 0) = (tau/2, tau/2) + (tau/2, -tau/2)
         nu = lambda_S (tau/2) 1 + lambda_D (tau/2, -tau/2)
         with the two components orthogonal in (nu_B, nu_C) space.

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
rho1 = 1.0 + aD * (eta - 1.0) - aT * (1.0 - aD)      # rho_1^*
D2 = 1.0 + 2.0 * aD * (eta - 1.0)
RHO_MID, RHO_HIGH = 2.2, 5.0                          # rho1* < 2.2 < 3rho1* < 5


def D3(rho):
    return 3.0 * aD * (eta - 1.0) + rho + 1.0


def lam_S(rho):
    return -2.0 * rho1 / D3(rho)


def lam_D(rho):
    return -2.0 * rho / (3.0 * D3(rho))


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
    shift = m * rho1 * dtau                 # TB_Atau * dtau
    slope = m * D2                          # TB_Anu
    nu_star = -rho1 / D2 * dtau             # post-tariff equilibrium

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
def _panel2(ax, rho, dtau, title, show_impact):
    d3 = D3(rho)
    sB = (rho + rho1) * dtau / d3            # intercept shift of TB_B = 0
    sC = (rho - rho1) * dtau / (2.0 * d3)    # intercept shift of TB_C = 0
    nuB = -(rho + 3.0 * rho1) / (3.0 * d3) * dtau
    nuC = (rho - 3.0 * rho1) / (3.0 * d3) * dtau

    xlim, ylim = (-0.64, 0.28), (-0.40, 0.52)
    x = np.linspace(xlim[0], xlim[1], 200)
    ax.plot(x, 2.0 * x, color=GREY, lw=1.0, ls=DASH, zorder=2)
    ax.plot(x, 0.5 * x, color=GREY, lw=1.0, ls=DASH, zorder=2)
    ax.plot(x, 2.0 * x + sB, color=INK, lw=1.5, zorder=3)
    ax.plot(x, 0.5 * x + sC, color=INK, lw=1.5, zorder=3)
    _frame(ax, xlim, ylim, r"$\nu_B$", r"$\nu_C$", equal=True)

    ax.plot([0], [0], "o", ms=4.4, mfc="white", mec=INK, mew=1.2, zorder=7)
    ax.plot([nuB], [nuC], "o", ms=5.0, color=INK, zorder=7)
    ax.text(0.024, -0.024, r"$E$", va="top", ha="left", fontsize=9)
    ax.text(nuB - 0.045, nuC - 0.030, r"$E'$", va="top", ha="right", fontsize=9)

    px, py = _line_point(2.0, sB, xlim, ylim, 1.0)
    ax.text(px - 0.014, py, r"$\mathrm{TB}_B=0$", ha="right", va="center",
            fontsize=8, color=INK)
    px, py = _line_point(0.5, sC, xlim, ylim, 0.82)
    ax.text(px, py + 0.022, r"$\mathrm{TB}_C=0$", ha="right", va="bottom",
            fontsize=8, color=INK)

    # impact effect: holding nu_B at zero, C's balance clears at nu_C = sC,
    # whose sign is the sign of rho - rho1*
    ax.plot([0], [sC], "s", ms=4.2, mfc="white", mec=INK, mew=1.2, zorder=7)
    ax.annotate("", xy=(0, sC), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1,
                                shrinkA=0, shrinkB=0))
    ax.text(0.048, sC, r"$F_C>0$", va="center", ha="left", fontsize=8.4)

    if show_impact:
        ax.annotate("", xy=(nuB, nuC), xytext=(0, sC),
                    arrowprops=dict(arrowstyle="-|>", color=MID, lw=1.1,
                                    shrinkA=6, shrinkB=7,
                                    connectionstyle="arc3,rad=0.28"))

    # read the bystander response off the vertical axis
    ax.plot([nuB, 0], [nuC, nuC], color=GREY, lw=0.6, ls=DOT, zorder=2)
    ax.text(-0.016, nuC + (0.016 if nuC > 0 else -0.016), r"$\nu_C$",
            ha="right", va="bottom" if nuC > 0 else "top", fontsize=8,
            color=MID)

    ax.set_title(title, fontsize=8.8, pad=8)
    return dict(sB=sB, sC=sC, nuB=nuB, nuC=nuC)


def figure2(dtau=1.0):
    fig, axes = plt.subplots(1, 2, figsize=(6.7, 4.0), layout="constrained")
    out = {}
    out["mid"] = _panel2(
        axes[0], RHO_MID, dtau,
        r"(a) $\rho_1^*<\rho<3\rho_1^*$:  $\nu_C<0$ although $F_C>0$",
        show_impact=True)
    out["high"] = _panel2(
        axes[1], RHO_HIGH, dtau,
        r"(b) $\rho>3\rho_1^*$:  bilateral reversal, $\nu_C>0$",
        show_impact=False)
    fig.suptitle(r"dashed: loci at $d\tau=0$;  solid: loci after the tariff",
                 y=0.035, fontsize=7.6, color=MID)
    fig.savefig(os.path.join(OUT, "fig2_three_country.pdf"))
    plt.close(fig)
    return out


# ------------------------------------------------------------------- Figure 3
def _panel3(ax, rho, tau, title):
    lS, lD = lam_S(rho), lam_D(rho)
    step = lS * tau / 2.0                     # average-protection step
    rel = lD * tau / 2.0                      # relative-treatment step
    Sx, Sy = step, step
    Fx, Fy = step + rel, step - rel

    xlim, ylim = (-0.64, 0.16), (-0.50, 0.30)
    _frame(ax, xlim, ylim, r"$\nu_B$", r"$\nu_C$", equal=True)

    # the constant (NEER) direction
    d = np.linspace(-0.48, 0.13, 40)
    ax.plot(d, d, color=GREY, lw=0.8, ls=DOT, zorder=2)
    ax.text(-0.455, -0.470, r"common direction $\mathbf{1}$",
            fontsize=7.2, color=MID, ha="left", va="top", rotation=45,
            rotation_mode="anchor")

    # the zero-sum direction through the average-protection point
    amax = min(abs(rel) + 0.11, Sy - ylim[0] - 0.03, xlim[1] - Sx - 0.02)
    amin = -(abs(rel) + 0.055)
    a = np.linspace(amin, amax, 40)
    ax.plot(Sx + a, Sy - a, color=GREY, lw=0.8, ls=DOT, zorder=2)
    ax.text(Sx + amax, Sy - amax + 0.012, "zero-sum",
            fontsize=7.2, color=MID, ha="right", va="bottom", rotation=-45,
            rotation_mode="anchor")

    ax.annotate("", xy=(Sx, Sy), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6,
                                shrinkA=0, shrinkB=0))
    ax.annotate("", xy=(Fx, Fy), xytext=(Sx, Sy),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6,
                                shrinkA=0, shrinkB=0))

    ax.plot([0], [0], "o", ms=4.2, mfc="white", mec=INK, mew=1.2, zorder=7)
    ax.plot([Sx], [Sy], "o", ms=4.2, color=INK, zorder=7)
    ax.plot([Fx], [Fy], "o", ms=5.2, color=INK, zorder=7)

    ax.text(Sx / 2 - 0.042, Sy / 2 + 0.042,
            r"$\lambda_S\,\bar t\,\mathbf{1}$", ha="right", va="bottom",
            fontsize=9.5)
    ax.text((Sx + Fx) / 2 - 0.032, (Sy + Fy) / 2 - 0.032,
            r"$\lambda_D\,\tilde t$", ha="right", va="top", fontsize=9.5)
    ax.text(Sx + 0.028, Sy - 0.028,
            r"$d\nu_A^E=\lambda_S\bar t$", ha="left", va="top", fontsize=8)
    ax.text(Fx - 0.022, Fy + 0.022, r"$\nu$", ha="right", va="bottom",
            fontsize=10)

    # the height of nu above the axis is the bystander response
    ax.plot([Fx, 0], [Fy, Fy], color=GREY, lw=0.6, ls=DOT, zorder=2)
    ax.text(-0.014, Fy + (0.014 if Fy > 0 else -0.014),
            r"$\nu_C$", ha="right", va="bottom" if Fy > 0 else "top",
            fontsize=8, color=MID)

    ax.set_title(title, fontsize=8.8, pad=8)
    return dict(S=(Sx, Sy), F=(Fx, Fy), lam_S=lS, lam_D=lD)


def figure3(tau=1.0):
    fig, axes = plt.subplots(1, 2, figsize=(6.7, 3.9), layout="constrained")
    out = {}
    out["mid"] = _panel3(axes[0], RHO_MID, tau,
                         r"(a) $\rho<3\rho_1^*$:  $\nu_C<0$")
    out["high"] = _panel3(axes[1], RHO_HIGH, tau,
                          r"(b) $\rho>3\rho_1^*$:  $\nu_C>0$")
    fig.suptitle(r"$t=(\tau,0)=(\tau/2,\ \tau/2)+(\tau/2,\ -\tau/2)$",
                 y=0.035, fontsize=8, color=MID)
    fig.savefig(os.path.join(OUT, "fig3_decomposition.pdf"))
    plt.close(fig)
    return out


# ------------------------------------------------------------------- checks
def selfcheck(r1, r2, r3):
    """Every plotted point must equal the closed form in the text."""
    dtau = 0.20
    assert abs(r1["nu_star"] - (-rho1 / D2 * dtau)) < 1e-12
    assert rho1 < RHO_MID < 3 * rho1 < RHO_HIGH
    for key, rho in (("mid", RHO_MID), ("high", RHO_HIGH)):
        d3 = D3(rho)
        nuB = -(rho + 3 * rho1) / (3 * d3)
        nuC = (rho - 3 * rho1) / (3 * d3)
        assert abs(r2[key]["nuB"] - nuB) < 1e-12
        assert abs(r2[key]["nuC"] - nuC) < 1e-12
        # the two loci intersect at the closed-form equilibrium
        assert abs(nuC - (2 * nuB + r2[key]["sB"])) < 1e-12
        assert abs(nuC - (0.5 * nuB + r2[key]["sC"])) < 1e-12
        # impact effect on C has the sign of rho - rho1*
        assert np.sign(r2[key]["sC"]) == np.sign(rho - rho1)
        # the decomposition lands on the same equilibrium
        assert abs(r3[key]["F"][0] - nuB) < 1e-12
        assert abs(r3[key]["F"][1] - nuC) < 1e-12
        # the average-protection component carries the whole NEER response
        assert abs(r3[key]["S"][0] - (-rho1 / d3)) < 1e-12
        # the two components are orthogonal in (nu_B, nu_C) space
        Sv = np.array(r3[key]["S"])
        Rv = np.array(r3[key]["F"]) - Sv
        assert abs(float(Sv @ Rv)) < 1e-14
    print("rho1* = %.4f,  3 rho1* = %.4f,  D_2 = %.4f" % (rho1, 3 * rho1, D2))
    print("fig2 (a) rho=%.1f: F_C shift = %+.4f, equilibrium nu_C = %+.4f"
          % (RHO_MID, r2["mid"]["sC"], r2["mid"]["nuC"]))
    print("fig2 (b) rho=%.1f: F_C shift = %+.4f, equilibrium nu_C = %+.4f"
          % (RHO_HIGH, r2["high"]["sC"], r2["high"]["nuC"]))
    print("all figure self-checks passed")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    r1, r2, r3 = figure1(), figure2(), figure3()
    selfcheck(r1, r2, r3)
    print("written to", OUT)
