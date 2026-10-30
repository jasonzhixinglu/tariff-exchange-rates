# -*- coding: utf-8 -*-
"""Exact symbolic solution of the kappa-asymmetric N-country system.

Weights: b_AB=b_BA=beta=kappa/(N-1); b_AC=b_CA=b_BC=b_CB=gamma=(1-beta)/(N-2);
b_CC'=xi=(1-2gamma)/(N-3). Types A, B, C (N-2 identical bystanders).
Common currency = A. Unknowns nu_B, nu_C. Tariff dt_AB = dtau.
"""
import sympy as sp

N, eta, rho, aD, aT, nuB, nuC, dtau, kap = sp.symbols(
    'N eta rho alpha_D alpha_T nu_B nu_C dtau kappa', positive=True)
m = aT * (1 - aD)
beta = kap / (N - 1)
gamma = (1 - beta) / (N - 2)
xi = (1 - 2 * gamma) / (N - 3)

nu = {'A': 0, 'B': nuB, 'C': nuC, 'Cp': nuC}
def dp(i, j, t=0):
    return nu[j] - nu[i] + t

dPM = {
    'A': beta * dp('A', 'B', dtau) + (N - 2) * gamma * dp('A', 'C'),
    'B': beta * dp('B', 'A') + (N - 2) * gamma * dp('B', 'C'),
    'C': gamma * dp('C', 'A') + gamma * dp('C', 'B') + (N - 3) * xi * dp('C', 'Cp'),
}
dPM['Cp'] = dPM['C']

def ds(i, j, t=0):
    return (1 - rho) * (dp(i, j, t) - dPM[i]) + (1 - eta) * aD * dPM[i]

dI = {'A': m * beta * dtau, 'B': nuB, 'C': nuC, 'Cp': nuC}

# dTB_B / m: inflow from A (weight beta), from each of N-2 C's (gamma);
# outflow to A (beta), to each C (gamma)
TB_B = beta * (ds('A', 'B', dtau) + dI['A'] - dtau) \
     + (N - 2) * gamma * (ds('C', 'B') + dI['C']) \
     - beta * (ds('B', 'A') + dI['B']) \
     - (N - 2) * gamma * (ds('B', 'C') + dI['B'])

# dTB_C / m: inflow from A (gamma), from B (gamma), from N-3 C' (xi);
# outflow to A (gamma), to B (gamma), to N-3 C' (xi)
TB_C = gamma * (ds('A', 'C') + dI['A']) \
     + gamma * (ds('B', 'C') + dI['B']) \
     + (N - 3) * xi * (ds('Cp', 'C') + dI['Cp']) \
     - gamma * (ds('C', 'A') + dI['C']) \
     - gamma * (ds('C', 'B') + dI['C']) \
     - (N - 3) * xi * (ds('C', 'Cp') + dI['C'])

sol = sp.solve([sp.Eq(TB_B, 0), sp.Eq(TB_C, 0)], [nuB, nuC])
eAB = sp.simplify(sp.cancel(sol[nuB] / dtau))
eAC = sp.simplify(sp.cancel(sol[nuC] / dtau))
print("e_AB slope:")
sp.pprint(sp.factor(eAB))
print("\ne_AC slope:")
sp.pprint(sp.factor(eAC))

# NEER with trade weights w_Aj = b_Aj
neer = sp.simplify(sp.cancel(beta * eAB + (N - 2) * gamma * eAC))
print("\nNEER slope (exact):")
neer_f = sp.factor(neer)
sp.pprint(neer_f)

# check kappa=1 reduces to -rho1*/D_N
r1s = 1 + aD * (eta - 1) - aT * (1 - aD)
DN = N * aD * (eta - 1) + (N - 2) * rho + 1
print("\ncheck kappa=1:", sp.simplify(neer.subs(kap, 1) + r1s / DN))

# numerator/denominator structure
num, den = sp.fraction(sp.cancel(sp.together(neer)))
print("\nNEER numerator (factored):")
sp.pprint(sp.factor(sp.expand(num)))
print("\nNEER denominator (factored):")
sp.pprint(sp.factor(sp.expand(den)))

# sign of numerator: is it -kappa * rho1* * (positive)?
print("\nnum / (-kappa * rho1*):")
sp.pprint(sp.factor(sp.simplify(sp.expand(num / (-kap * r1s)))))

# large-N expansion of NEER
ser = sp.series(neer.subs(N, 1/sp.Symbol('x', positive=True)), sp.Symbol('x', positive=True), 0, 3)
print("\nlarge-N series (x = 1/N):")
sp.pprint(sp.simplify(ser))

# threshold for e_AC (bilateral) as function of kappa: solve numerator of eAC in rho
numC, denC = sp.fraction(sp.cancel(sp.together(eAC)))
polyC = sp.Poly(sp.expand(numC), rho)
print("\ne_AC numerator degree in rho:", polyC.degree())
print("e_AC numerator coeffs (factored):")
for c in polyC.all_coeffs():
    sp.pprint(sp.factor(c))

# numeric sanity: N=10, kappa=2, benchmark params
subs = {N: 10, kap: 2, aD: sp.Rational(4, 5), aT: sp.Rational(2, 5), eta: sp.Rational(3, 2), rho: 2}
print("\nnumeric check N=10 kappa=2: NEER =", float(neer.subs(subs)))
