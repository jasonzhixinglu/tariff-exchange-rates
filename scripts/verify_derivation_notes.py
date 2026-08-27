# -*- coding: utf-8 -*-
"""Verify the three outline checks for the model_derivations rewrite.

Linearized N-country nested-CES system at a balanced free-trade baseline.
Conventions: nu[i] = d log e_{Ai} (depreciation-positive, nu[0]=0, country 0 = A).
Within-import origin shares b[i,j] (zero diagonal, rows sum to 1); balanced
baseline requires b symmetric (columns then also sum to 1). Home share alpha_D,
tradable share alpha_T, incomes 1, wages 1.

d log p_ij (in i's currency) = nu_j - nu_i + dt_ij
dPM_i  = sum_j b_ij dp_ij
dPT_i  = (1-aD) dPM_i                        (home price fixed in own currency)
dlog s_ij = (1-rho)(dp_ij - dPM_i) + (1-eta) aD dPM_i
dlog I_i  = m sum_j b_ij dt_ij               (rebate, first order at tau=0)
flow value f_ij = m b_ij  (i's imports from j), m = aT(1-aD)
dTB_i = sum_k f_ki (dlog s_ki + dI_k + nu_k - dt_ki)
      - sum_j f_ij (dlog s_ij + dI_i + nu_i - dt_ij)
Solve dTB_i = 0, i = 1..N-1 (Walras drops country 0).
"""
import numpy as np

def solve_linear(N, b, aD, aT, eta, rho, tariff_pairs):
    m = aT * (1.0 - aD)
    f = m * b
    dt = np.zeros((N, N))
    for (i, j) in tariff_pairs:
        dt[i, j] = 1.0
    # coefficient vectors of length N+1: [nu_0..nu_{N-1}, dtau]
    def vec():
        return np.zeros(N + 1)
    dp = np.zeros((N, N, N + 1))
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            v = vec()
            v[j] += 1.0
            v[i] -= 1.0
            v[N] += dt[i, j]
            dp[i, j] = v
    dPM = np.einsum('ij,ijk->ik', b, dp)          # (N, N+1)
    ds = np.zeros((N, N, N + 1))
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            ds[i, j] = (1 - rho) * (dp[i, j] - dPM[i]) + (1 - eta) * aD * dPM[i]
    dI = np.zeros((N, N + 1))
    for i in range(N):
        dI[i, N] = m * np.sum(b[i] * dt[i])
    nuvec = np.zeros((N, N + 1))
    for i in range(N):
        nuvec[i, i] = 1.0
    dtvec = np.zeros((N, N, N + 1))
    for i in range(N):
        for j in range(N):
            dtvec[i, j, N] = dt[i, j]
    dTB = np.zeros((N, N + 1))
    for i in range(N):
        acc = vec()
        for k in range(N):
            if k == i:
                continue
            acc += f[k, i] * (ds[k, i] + dI[k] + nuvec[k] - dtvec[k, i])
        for j in range(N):
            if j == i:
                continue
            acc -= f[i, j] * (ds[i, j] + dI[i] + nuvec[i] - dtvec[i, j])
        dTB[i] = acc
    # impose nu_0 = 0, solve dTB_i = 0 for i=1..N-1
    A = dTB[1:, 1:N]
    c = -dTB[1:, N]
    nu = np.zeros(N)
    nu[1:] = np.linalg.solve(A, c)
    return nu

def sym_b(N):
    b = np.full((N, N), 1.0 / (N - 1))
    np.fill_diagonal(b, 0.0)
    return b

def kappa_b(N, kappa):
    """Symmetric weight matrix: A-B link kappa/(N-1); A-C and B-C links equal;
    bystander-bystander links fill the remainder. Doubly stochastic."""
    b = np.zeros((N, N))
    bAB = kappa / (N - 1)
    bAC = (1.0 - bAB) / (N - 2)
    xi = (1.0 - 2 * bAC) / (N - 3)
    b[0, 1] = b[1, 0] = bAB
    for c in range(2, N):
        b[0, c] = b[c, 0] = bAC
        b[1, c] = b[c, 1] = bAC
        for d in range(2, N):
            if d != c:
                b[c, d] = xi
    return b

aD, aT, eta = 0.8, 0.4, 1.5
rho1s = 1 + aD * (eta - 1) - aT * (1 - aD)     # rho_1^*
print(f"rho_1^* = {rho1s:.6f}")

print("\n=== Check 0: validate implementation at N=3 symmetric ===")
N = 3
rho = 2.0
D = 3 * aD * (eta - 1) + rho + 1
rs = 3 * rho1s
nu = solve_linear(N, sym_b(N), aD, aT, eta, rho, [(0, 1)])
print(f"nu_B: numeric {nu[1]:+.8f}  formula {-(rho + rs) / (3 * D):+.8f}")
print(f"nu_C: numeric {nu[2]:+.8f}  formula {(rho - rs) / (3 * D):+.8f}")

print("\n=== Check 0b: N=6 symmetric closed forms ===")
N = 6
rho = 3.0
DN = N * aD * (eta - 1) + (N - 2) * rho + 1
nu = solve_linear(N, sym_b(N), aD, aT, eta, rho, [(0, 1)])
print(f"e_AB: numeric {nu[1]:+.8f}  formula {-(N * rho1s + (N - 2) * rho) / (N * DN):+.8f}")
print(f"e_AC: numeric {nu[2]:+.8f}  formula {(rho - N * rho1s) / (N * DN):+.8f}")
neer = np.sum(sym_b(N)[0] * nu)
print(f"NEER: numeric {neer:+.8f}  formula {-rho1s / DN:+.8f}")

print("\n=== Check 0c: N=6 war, e_AC threshold rho_1^* ===")
nu = solve_linear(N, sym_b(N), aD, aT, eta, rho, [(0, 1), (1, 0)])
print(f"war e_AB: numeric {nu[1]:+.8f}  (should be 0)")
print(f"war e_AC: numeric {nu[2]:+.8f}  formula {(rho - rho1s) / DN:+.8f}")

print("\n=== Check (i): N=2 slope = -rho_1^*/D_2 ===")
nu = solve_linear(2, sym_b(2), aD, aT, eta, rho, [(0, 1)])
D2 = 2 * aD * (eta - 1) + 1
print(f"e_AB: numeric {nu[1]:+.8f}  formula {-rho1s / D2:+.8f}")

print("\n=== Check (ii): impossibility generalization, algebra spot check ===")
for Nn in (2, 3, 5, 10):
    for sig in (0.5, 2.0, 10.0, 100.0):
        gap = Nn * (1 + aD * (sig - 1) - aT * (1 - aD)) - sig
        pred = sig * (Nn * aD - 1) + Nn * (1 - aD) * (1 - aT)
        assert abs(gap - pred) < 1e-10
print("N*rho_1^* - sigma == sigma(N aD - 1) + N(1-aD)(1-aT)  for all spot checks -> OK")
print("(> 0 whenever aD >= 1/N)")

print("\n=== Check (iii): large-N kappa-asymmetric NEER approximation ===")
rho = 2.0
print(f"{'N':>5} {'kappa':>6} {'numeric NEER':>14} {'approx':>14} {'ratio':>8}")
for kappa in (0.5, 1.0, 2.0, 5.0):
    for N in (10, 20, 50, 100, 200):
        b = kappa_b(N, kappa)
        assert np.all(b >= 0), (N, kappa)
        nu = solve_linear(N, b, aD, aT, eta, rho, [(0, 1)])
        neer = np.sum(b[0] * nu)
        approx = -(kappa / (N - 2)) * rho1s / (rho + aD * (eta - 1))
        print(f"{N:>5} {kappa:>6.1f} {neer:>+14.8f} {approx:>+14.8f} {neer/approx:>8.4f}")




print("\n=== Check (iv): general-N real rates, real threshold, REER ===")
rho = 3.0
def q_slopes(N, rho, pairs=((0, 1),)):
    b = sym_b(N)
    nu = solve_linear(N, b, aD, aT, eta, rho, list(pairs))
    dt = np.zeros((N, N))
    for (i, j) in pairs:
        dt[i, j] = 1.0
    dp = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                dp[i, j] = nu[j] - nu[i] + dt[i, j]
    dPT = (1 - aD) * np.sum(b * dp, axis=1)
    return nu, np.array([nu[j] + aT * (dPT[j] - dPT[0]) for j in range(N)])

m = aT * (1 - aD)
N = 6
nu, q = q_slopes(N, rho)
for j, lab in ((1, 'B'), (2, 'C')):
    f = (1 - m * N / (N - 1)) * nu[j] - m / (N - 1)
    print(f"q_A{lab}: numeric {q[j]:+.8f}  formula {f:+.8f}")
DN = N * aD * (eta - 1) + (N - 2) * rho + 1
reer = np.mean(q[1:])
f = -(1 - m * N / (N - 1)) * rho1s / DN - m / (N - 1)
print(f"REER slope: numeric {reer:+.8f}  formula {f:+.8f}")

def rhoq(N):
    return (((N - 1) - m * N) * N * rho1s + m * N * (N * aD * (eta - 1) + 1)) / ((N - 1) * (1 - m * N))
for N in (3, 4, 5, 6, 8):
    lo, hi = 0.01, 200.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if q_slopes(N, mid)[1][2] < 0:
            lo = mid
        else:
            hi = mid
    print(f"N={N}: rho_q* closed form {rhoq(N):.6f}  numeric root {0.5 * (lo + hi):.6f}")

print("\n=== Check (v): broad uniform tariff, all bilaterals -(N-1)rho1*/D_N ===")
for N in (3, 6):
    DN = N * aD * (eta - 1) + (N - 2) * rho + 1
    nu = solve_linear(N, sym_b(N), aD, aT, eta, rho, [(0, j) for j in range(1, N)])
    print(f"N={N}: nu spread {nu[1:].max() - nu[1:].min():.2e}, value {nu[1]:+.8f}  formula {-(N - 1) * rho1s / DN:+.8f}")


print("\n=== Check (vi): kappa-asymmetric NEER, flip threshold and sign preservation ===")
def neer_kappa(N, kappa, rho):
    b = kappa_b(N, kappa)
    nu = solve_linear(N, b, aD, aT, eta, rho, [(0, 1)])
    return np.sum(b[0] * nu)

for (N, kappa) in ((10, 0.5), (20, 0.5), (50, 0.5), (20, 0.2)):
    lo, hi = 0.1, 2000.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if neer_kappa(N, kappa, mid) < 0:
            lo = mid
        else:
            hi = mid
    crude = N * rho1s / (1 - kappa)
    print(f"N={N} kappa={kappa}: NEER flip at rho={0.5*(lo+hi):8.3f}  leading-order N*rho1*/(1-k)={crude:8.3f}")

for (N, kappa) in ((10, 1.0), (10, 2.0), (10, 5.0), (30, 3.0)):
    vals = [neer_kappa(N, kappa, r) for r in (0.2, 1, 5, 20, 100, 1000)]
    print(f"N={N} kappa={kappa}: sign preserved over rho grid: {all(v < 0 for v in vals)}")
