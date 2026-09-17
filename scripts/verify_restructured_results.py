# -*- coding: utf-8 -*-
"""Symbolic verification of every closed form displayed in
notes/model_derivations.tex after the structural revision.

The linearized system is rebuilt from the primitives in
Section 5.1 (equations dp / dindex / dshome / dsfor / dincome / dtb) with
exact symbolic parameters, for N = 2, ..., 6, and each displayed equation is
checked against it.  Nothing is imported from the closed forms being tested.

Conventions (matching the notes): nu[i] = d log e_{Ai}, nu[0] = 0, A = 0.
Countries 1..N-1 are A's partners; B = 1; bystanders are 2..N-1.
"""
import sympy as sp

aD, aT, eta, rho, dtau = sp.symbols("alpha_D alpha_T eta rho dtau", positive=True)
m = aT * (1 - aD)
rho1 = 1 + aD * (eta - 1) - aT * (1 - aD)


def DN(N):
    return N * aD * (eta - 1) + (N - 2) * rho + 1


def build(N, dt):
    """Linearize at the symmetric balanced free-trade baseline.

    dt[i][j] = d tau_{ij}.  Returns (nu, dTB) where nu solves dTB_i = 0 for
    i != 0 and dTB is the vector of trade-balance changes as functions of nu.
    """
    b = sp.Rational(1, N - 1)
    nu = [sp.Integer(0)] + list(sp.symbols("nu1:%d" % N))

    dp = {}
    for i in range(N):
        for j in range(N):
            if i != j:
                dp[i, j] = nu[j] - nu[i] + dt[i][j]

    dPM = [sum(b * dp[i, j] for j in range(N) if j != i) for i in range(N)]
    dlog_s = {}
    for i in range(N):
        for j in range(N):
            if i != j:
                dlog_s[i, j] = ((1 - rho) * (dp[i, j] - dPM[i])
                                + (1 - eta) * aD * dPM[i])
    # d log Itilde_i = nu_i + sum_j s_ij dt_ij, s_ij = m b at the baseline
    dI = [nu[i] + sum(m * b * dt[i][j] for j in range(N) if j != i)
          for i in range(N)]

    f = m * b                                    # baseline flow value
    dTB = []
    for i in range(N):
        acc = 0
        for k in range(N):
            if k != i:
                acc += f * (dlog_s[k, i] + dI[k] - dt[k][i])
        for j in range(N):
            if j != i:
                acc -= f * (dlog_s[i, j] + dI[i] - dt[i][j])
        dTB.append(sp.expand(acc))
    return nu, dTB


def zeros(N):
    return [[sp.Integer(0)] * N for _ in range(N)]


def solve(N, dt):
    nu, dTB = build(N, dt)
    sol = sp.solve(dTB[1:], nu[1:], dict=True)[0]
    return [sp.simplify(sp.together(sol[x])) for x in nu[1:]]


def eq(a, b_):
    return sp.simplify(sp.together(sp.expand(a - b_))) == 0


CHECKS = []


def check(name, cond):
    CHECKS.append((name, bool(cond)))
    print("  [%s] %s" % ("ok" if cond else "FAIL", name))


# --------------------------------------------------------------- Section 3
def section3():
    print("Section 3: two-country benchmark")
    dt = zeros(2)
    dt[0][1] = dtau
    nu, dTB = build(2, dt)
    # eq:2c-collected  dTB_A = m D_2 nu_B + m rho1* dtau
    D2 = 2 * aD * (eta - 1) + 1
    check("eq:2c-collected", eq(dTB[0], m * D2 * nu[1] + m * rho1 * dtau))
    # eq:2c-slope
    check("eq:2c-slope", eq(solve(2, dt)[0], -rho1 / D2 * dtau))
    # Figure 1 geometry: slope and shift of the plotted schedule
    check("fig 1 slope/shift", eq(sp.diff(dTB[0], nu[1]), m * D2)
          and eq(dTB[0].subs(nu[1], 0), m * rho1 * dtau))


# --------------------------------------------------------------- Section 5.1
def section51():
    print("Section 5.1: Jacobian and D_N (Lemma F.1, eq:full-jacobian)")
    for N in range(2, 7):
        dt = zeros(N)
        nu, dTB = build(N, dt)
        off = sp.simplify(sp.diff(dTB[1], nu[2] if N > 2 else nu[1]))
        if N == 2:
            off = sp.simplify(sp.diff(dTB[1], nu[1]))
            check("N=2 Jtilde_BB = -m D_2", eq(off, -m * DN(2)))
            continue
        check("N=%d Jtilde off-diagonal = m D_N/(N-1)^2" % N,
              eq(off, m * DN(N) / (N - 1) ** 2))
        diag = sp.simplify(sp.diff(dTB[1], nu[1]))
        check("N=%d Jtilde diagonal = -m D_N/(N-1)" % N,
              eq(diag, -m * DN(N) / (N - 1)))


# --------------------------------------------------------------- Section 5.2
def section52():
    print("Section 5.2: g, j, lambda and the decomposition")
    for N in range(3, 7):
        # G from an arbitrary tariff vector imposed by A
        ts = sp.symbols("t1:%d" % N)
        dt = zeros(N)
        for j in range(1, N):
            dt[0][j] = ts[j - 1]
        nu, dTB = build(N, dt)
        Gmat = sp.Matrix(N - 1, N - 1,
                         lambda i, j: sp.diff(dTB[i + 1], ts[j]).subs(
                             {x: 0 for x in nu[1:]}))
        Jmat = sp.Matrix(N - 1, N - 1,
                         lambda i, j: sp.diff(dTB[i + 1], nu[j + 1]))
        one = sp.ones(N - 1, 1)
        gS = sp.simplify((Gmat * one)[0])
        gD = sp.simplify(Gmat[0, 0] - Gmat[0, 1])
        jS = sp.simplify(-(Jmat * one)[0])
        jD = sp.simplify(-(Jmat[0, 0] - Jmat[0, 1]))
        check("N=%d eq:g-eigen g_S" % N, eq(gS, -m * rho1 / (N - 1)))
        check("N=%d eq:g-eigen g_D" % N, eq(gD, -m * rho / (N - 1)))
        check("N=%d eq:j-eigen j_S" % N, eq(jS, m * DN(N) / (N - 1) ** 2))
        check("N=%d eq:j-eigen j_D" % N, eq(jD, N * m * DN(N) / (N - 1) ** 2))
        check("N=%d eq:eigen lambda_S" % N,
              eq(gS / jS, -(N - 1) * rho1 / DN(N)))
        check("N=%d eq:eigen lambda_D" % N,
              eq(gD / jD, -(N - 1) * rho / (N * DN(N))))
        # eq:gj-ratios: g_D/g_S independent of N, j_D/j_S = N
        check("N=%d eq:gj-ratios g_D/g_S = rho/rho1*" % N,
              eq(gD / gS, rho / rho1))
        check("N=%d eq:gj-ratios j_D/j_S = N" % N, eq(jD / jS, N))
        check("N=%d lambda_D/lambda_S = rho/(N rho1*)" % N,
              eq((gD / jD) / (gS / jS), rho / (N * rho1)))
        # eq:scale-disc for a generic tariff vector
        sol = sp.solve([sp.Eq(x, 0) for x in dTB[1:]], nu[1:], dict=True)[0]
        tbar = sum(ts) / (N - 1)
        lS, lD = gS / jS, gD / jD
        for j in range(1, N):
            check("N=%d eq:scale-disc nu_%d" % (N, j),
                  eq(sol[nu[j]], lS * tbar + lD * (ts[j - 1] - tbar)))
        # eq:neer-scale
        neer = sum(sol[nu[j]] for j in range(1, N)) / (N - 1)
        check("N=%d eq:neer-scale" % N, eq(neer, lS * tbar))
        # eq:cross-disc
        if N >= 3:
            check("N=%d eq:cross-disc" % N,
                  eq(sol[nu[2]] - sol[nu[1]], lD * (ts[1] - ts[0])))


# --------------------------------------------------------------- Section 5.3
def section53():
    print("Section 5.3: unilateral tariff (Theorem 5.2) and eq:F-general")
    for N in range(3, 7):
        dt = zeros(N)
        dt[0][1] = dtau
        nu, dTB = build(N, dt)
        sol = sp.solve([sp.Eq(x, 0) for x in dTB[1:]], nu[1:], dict=True)[0]
        nuB, nuC = sol[nu[1]], sol[nu[2]]
        check("N=%d eq:N-slopes (target)" % N,
              eq(nuB, -(N * rho1 + (N - 2) * rho) / (N * DN(N)) * dtau))
        check("N=%d eq:N-slopes-C (bystander)" % N,
              eq(nuC, (rho - N * rho1) / (N * DN(N)) * dtau))
        check("N=%d eq:N-slopes-C (e_BC)" % N,
              eq(nuC - nuB, (N - 1) * rho / (N * DN(N)) * dtau))
        neer = sum(sol[nu[j]] for j in range(1, N)) / (N - 1)
        check("N=%d eq:N-neer" % N, eq(neer, -rho1 / DN(N) * dtau))
        # eq:F-general: impact disturbances
        F = [sp.expand(x.subs({y: 0 for y in nu[1:]})) for x in dTB[1:]]
        check("N=%d eq:F-general F_B" % N,
              eq(F[0], -m * (rho1 + (N - 2) * rho) / (N - 1) ** 2 * dtau))
        check("N=%d eq:F-general F_C" % N,
              eq(F[1], m * (rho - rho1) / (N - 1) ** 2 * dtau))


# --------------------------------------------------------------- Section 5.4
def section54():
    print("Section 5.4: multiple targets (eq:k-targets, eq:N-broad)")
    for N in range(3, 7):
        for k in range(1, N):
            dt = zeros(N)
            for j in range(1, k + 1):
                dt[0][j] = dtau
            nu, dTB = build(N, dt)
            sol = sp.solve([sp.Eq(x, 0) for x in dTB[1:]], nu[1:], dict=True)[0]
            nuB = sol[nu[1]]
            check("N=%d k=%d eq:k-targets target" % (N, k),
                  eq(nuB, (-k * rho1 / DN(N)
                           - (N - 1 - k) * rho / (N * DN(N))) * dtau))
            if k <= N - 2:
                check("N=%d k=%d eq:k-targets bystander" % (N, k),
                      eq(sol[nu[N - 1]],
                         k * (rho - N * rho1) / (N * DN(N)) * dtau))
            neer = sum(sol[nu[j]] for j in range(1, N)) / (N - 1)
            check("N=%d k=%d eq:k-targets NEER" % (N, k),
                  eq(neer, -k * rho1 / DN(N) * dtau))
            if k == N - 1:
                check("N=%d eq:N-broad" % N,
                      eq(nuB, -(N - 1) * rho1 / DN(N) * dtau))


# --------------------------------------------------------------- Section 5.5
def section55():
    print("Section 5.5: three-country illustration and the Figure 2 loci")
    dt = zeros(3)
    dt[0][1] = dtau
    nu, dTB = build(3, dt)
    D3 = DN(3)
    # eq:3c-JF
    J = sp.Matrix(2, 2, lambda i, j: sp.diff(dTB[i + 1], nu[j + 1]))
    F = sp.Matrix(2, 1, lambda i, j: dTB[i + 1].subs(
        {nu[1]: 0, nu[2]: 0})) / dtau
    check("eq:3c-JF J", sp.simplify(J + sp.Rational(1, 4) * m * D3 * sp.Matrix(
        [[2, -1], [-1, 2]])) == sp.zeros(2, 2))
    check("eq:3c-JF F", sp.simplify(F - (-sp.Rational(1, 4) * m * sp.Matrix(
        [[rho + rho1], [rho1 - rho]]))) == sp.zeros(2, 1))
    sol = sp.solve([sp.Eq(x, 0) for x in dTB[1:]], nu[1:], dict=True)[0]
    check("eq:3c-slopes e_AB", eq(sol[nu[1]], -(rho + 3 * rho1) / (3 * D3) * dtau))
    check("eq:3c-slopes e_AC", eq(sol[nu[2]], (rho - 3 * rho1) / (3 * D3) * dtau))
    check("eq:3c-slopes e_BC",
          eq(sol[nu[2]] - sol[nu[1]], 2 * rho / (3 * D3) * dtau))
    # eq:3c-loci: solve each trade-balance condition for nu_C
    locB = sp.solve(sp.Eq(dTB[1], 0), nu[2])[0]
    locC = sp.solve(sp.Eq(dTB[2], 0), nu[2])[0]
    check("eq:3c-loci TB_B = 0",
          eq(locB, 2 * nu[1] + (rho + rho1) * dtau / D3))
    check("eq:3c-loci TB_C = 0",
          eq(locC, nu[1] / 2 + (rho - rho1) * dtau / (2 * D3)))
    # Figure 3: the two components add up to the equilibrium
    lS = -2 * rho1 / D3
    lD = -2 * rho / (3 * D3)
    comp_S = lS * dtau / 2
    comp_D = lD * dtau / 2
    check("fig 3 nu_B = scale + disc", eq(comp_S + comp_D, sol[nu[1]]))
    check("fig 3 nu_C = scale - disc", eq(comp_S - comp_D, sol[nu[2]]))
    check("fig 3 NEER carried entirely by average protection",
          eq(comp_S, (sol[nu[1]] + sol[nu[2]]) / 2))
    # Figure 2, panel (a): the impact point on the shifted TB_C locus
    check("fig 2 impact point sign = sign(rho - rho1*)",
          eq(locC.subs(nu[1], 0), (rho - rho1) * dtau / (2 * D3)))


# --------------------------------------------------------------- Section 6
def section6():
    print("Section 6: trade wars (Proposition 6.1)")
    for N in range(3, 7):
        # (i) bilateral retaliation
        dt = zeros(N)
        dt[0][1] = dtau
        dt[1][0] = dtau
        nu, dTB = build(N, dt)
        sol = sp.solve([sp.Eq(x, 0) for x in dTB[1:]], nu[1:], dict=True)[0]
        check("N=%d eq:N-war e_AB" % N, eq(sol[nu[1]], 0))
        check("N=%d eq:N-war e_AC" % N,
              eq(sol[nu[2]], (rho - rho1) / DN(N) * dtau))
        neer = sum(sol[nu[j]] for j in range(1, N)) / (N - 1)
        check("N=%d eq:N-war NEER" % N,
              eq(neer, sp.Rational(N - 2, N - 1) * (rho - rho1) / DN(N) * dtau))
        # (ii) global retaliation
        dt = zeros(N)
        for j in range(1, N):
            dt[0][j] = dtau
            dt[j][0] = dtau
        nu, dTB = build(N, dt)
        sol = sp.solve([sp.Eq(x, 0) for x in dTB[1:]], nu[1:], dict=True)[0]
        target = (N - 2) * (rho - rho1) / DN(N) * dtau
        check("N=%d eq:globalwar" % N,
              all(eq(sol[nu[j]], target) for j in range(1, N)))


# --------------------------------------------------------------- Appendix B
def appendixB():
    print("Appendix B: real exchange rates")
    for N in range(3, 6):
        dt = zeros(N)
        dt[0][1] = dtau
        b = sp.Rational(1, N - 1)
        nu, dTB = build(N, dt)
        sol = sp.solve([sp.Eq(x, 0) for x in dTB[1:]], nu[1:], dict=True)[0]
        nuv = [sp.Integer(0)] + [sol[nu[j]] for j in range(1, N)]
        # own-currency tradable price indices
        dPM = []
        for i in range(N):
            dPM.append(sum(b * (nuv[j] - nuv[i] + dt[i][j])
                           for j in range(N) if j != i))
        q = [sp.simplify(nuv[j] + aT * (1 - aD) * (dPM[j] - dPM[0]))
             for j in range(N)]
        for j in (1, 2):
            check("N=%d eq:qgen j=%d" % (N, j),
                  eq(q[j], (1 - m * N / (N - 1)) * nuv[j] - m * dtau / (N - 1)))
        qE = sum(q[j] for j in range(1, N)) / (N - 1)
        check("N=%d eq:N-reer" % N,
              eq(qE, -(1 - m * N / (N - 1)) * rho1 / DN(N) * dtau
                 - m * dtau / (N - 1)))
        # eq:N-rhoq: the real bystander threshold
        r = sp.solve(sp.Eq(q[2] / dtau, 0), rho)[0]
        target = (((N - 1) - m * N) * N * rho1
                  + m * N * (N * aD * (eta - 1) + 1)) / ((N - 1) * (1 - m * N))
        check("N=%d eq:N-rhoq" % N, eq(r, target))


if __name__ == "__main__":
    section3()
    section51()
    section52()
    section53()
    section54()
    section55()
    section6()
    appendixB()
    bad = [n for n, ok in CHECKS if not ok]
    print("\n%d checks, %d failures" % (len(CHECKS), len(bad)))
    for n in bad:
        print("  FAILED:", n)
    assert not bad
