# -*- coding: utf-8 -*-
"""Symbolic reduced 2x2 system for the symmetric N-country model, N symbolic.

Conventions (common currency = A's): nu_B, nu_C = d log e_AB, d log e_AC;
dtau = A's tariff on B. Within-import shares 1/(N-1). m = aT(1-aD).
Flows valued at producer prices in A's currency; baseline flow value m/(N-1).
"""
import sympy as sp

N, eta, rho, aD, aT, nuB, nuC, dtau = sp.symbols('N eta rho alpha_D alpha_T nu_B nu_C dtau')
m = aT * (1 - aD)

# price changes in own currency: dp[i][j], i in {A,B,C,Cp} (Cp = other bystander)
# nu_A = 0; bystanders share nu_C
nu = {'A': 0, 'B': nuB, 'C': nuC, 'Cp': nuC}
def dp(i, j, t=0):
    return nu[j] - nu[i] + t

# import price indices (own currency), weights 1/(N-1)
dPM = {
    'A': (dp('A', 'B', dtau) + (N - 2) * dp('A', 'C')) / (N - 1),
    'B': (dp('B', 'A') + (N - 2) * dp('B', 'C')) / (N - 1),
    'C': (dp('C', 'A') + dp('C', 'B') + (N - 3) * dp('C', 'Cp')) / (N - 1),
}
dPM['Cp'] = dPM['C']

def ds(i, j, t=0):
    return (1 - rho) * (dp(i, j, t) - dPM[i]) + (1 - eta) * aD * dPM[i]

# incomes in A's currency
dI = {'A': m / (N - 1) * dtau, 'B': nuB, 'C': nuC, 'Cp': nuC}

# dTB_B * (N-1)/m :
TB_B = (ds('A', 'B', dtau) + dI['A'] - dtau) \
     + (N - 2) * (ds('C', 'B') + dI['C']) \
     - (ds('B', 'A') + dI['B']) \
     - (N - 2) * (ds('B', 'C') + dI['B'])

# dTB_C * (N-1)/m :  (inflows: from A, from B, from N-3 other bystanders)
TB_C = (ds('A', 'C') + dI['A']) \
     + (ds('B', 'C') + dI['B']) \
     + (N - 3) * (ds('Cp', 'C') + dI['Cp']) \
     - (ds('C', 'A') + dI['C']) \
     - (ds('C', 'B') + dI['C']) \
     - (N - 3) * (ds('C', 'Cp') + dI['C'])

JBB = sp.simplify(sp.expand(TB_B).coeff(nuB)); JBC = sp.simplify(sp.expand(TB_B).coeff(nuC))
JCB = sp.simplify(sp.expand(TB_C).coeff(nuB)); JCC = sp.simplify(sp.expand(TB_C).coeff(nuC))
FB = sp.simplify(sp.expand(TB_B).coeff(dtau)); FC = sp.simplify(sp.expand(TB_C).coeff(dtau))
print("coeff nu_B in TB_B:", sp.factor(JBB))
print("coeff nu_C in TB_B:", sp.factor(JBC))
print("coeff nu_B in TB_C:", sp.factor(JCB))
print("coeff nu_C in TB_C:", sp.factor(JCC))
print("coeff dtau in TB_B:", sp.factor(FB))
print("coeff dtau in TB_C:", sp.factor(FC))

# solve
sol = sp.solve([sp.Eq(TB_B, 0), sp.Eq(TB_C, 0)], [nuB, nuC])
r1s = 1 + aD * (eta - 1) - aT * (1 - aD)
DN = N * aD * (eta - 1) + (N - 2) * rho + 1
eAB = sp.simplify(sol[nuB] / dtau)
eAC = sp.simplify(sol[nuC] / dtau)
print("\n e_AB slope:", sp.factor(eAB))
print(" check vs -(N r1* + (N-2) rho)/(N D_N):",
      sp.simplify(eAB + (N * r1s + (N - 2) * rho) / (N * DN)))
print(" e_AC slope:", sp.factor(eAC))
print(" check vs (rho - N r1*)/(N D_N):",
      sp.simplify(eAC - (rho - N * r1s) / (N * DN)))

# real bilateral rates, symmetric N: d log q_Aj = nu_j + aT*(dPT_j^own - dPT_A^own)
# dPT_i^own = (1-aD)*dPM_i (own currency)
for j, nuj in (('B', nuB), ('C', nuC)):
    dq = nuj + aT * ((1 - aD) * dPM[j] - (1 - aD) * dPM['A'])
    dq = dq.subs({nuB: sol[nuB], nuC: sol[nuC]})
    # express as x*nu_j + y*dtau form BEFORE substitution:
    dq_form = nuj + aT * (1 - aD) * (dPM[j] - dPM['A'])
    print(f"\n d log q_A{j} =", sp.simplify(sp.collect(sp.expand(dq_form), [nuB, nuC, dtau])))
    # conjecture: (1 - m*N/(N-1)) nu_j - m/(N-1) dtau
    conj = (1 - m * N / (N - 1)) * nuj - m / (N - 1) * dtau
    print(f" conjecture check q_A{j}:", sp.simplify(sp.expand(dq_form - conj)))
