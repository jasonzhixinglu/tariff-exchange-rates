"""Closed forms at the symmetric benchmark (Section 3) and the composite
bystander of Proposition 3.6."""
import numpy as np

US_LIKE = dict(aD=0.8, aT=0.4, eta=1.5)
FIG2 = dict(aD=0.7, aT=0.6, eta=1.5)


def m(aD, aT):
    """Import share of income, m = alpha_T (1 - alpha_D)."""
    return aT * (1.0 - aD)


def rhoD(aD, aT, eta):
    """Domestic diversion margin, rho_D = alpha_D eta + (1-alpha_D)(1-alpha_T)."""
    return aD * eta + (1.0 - aD) * (1.0 - aT)


def M2(aD, eta):
    return 1.0 + 2.0 * aD * (eta - 1.0)


def MN(N, aD, eta, rho):
    """Multilateral adjustment margin (Theorem 3.2)."""
    return (1.0 + N * aD * (eta - 1.0) + (N - 2) * rho) / (N - 1)


def lamA(N, aD, aT, eta, rho):
    return -rhoD(aD, aT, eta) / MN(N, aD, eta, rho)


def lamR(N, aD, aT, eta, rho):
    return -rho / (N * MN(N, aD, eta, rho))


def unilateral(N, aD, aT, eta, rho):
    """Proposition 3.3: (d nu^E_A, d nu_B, d nu_C) per unit d tau."""
    rD, M = rhoD(aD, aT, eta), MN(N, aD, eta, rho)
    neer = -rD / ((N - 1) * M)
    dB = -(N * rD + (N - 2) * rho) / (N * (N - 1) * M)
    dC = (rho - N * rD) / (N * (N - 1) * M)
    return neer, dB, dC


def k_partners(N, k, aD, aT, eta, rho):
    """Tariff d tau on k partners: (d nu_target, d nu_bystander, d nu^E_A)."""
    rD, M = rhoD(aD, aT, eta), MN(N, aD, eta, rho)
    dB = -(N * k * rD + (N - 1 - k) * rho) / (N * (N - 1) * M)
    dC = k * (rho - N * rD) / (N * (N - 1) * M)
    neer = -k * rD / ((N - 1) * M)
    return dB, dC, neer


def retaliation(N, aD, aT, eta, rho):
    """Proposition 3.5(i): (d nu_B, d nu_C, d nu^E_A) per unit d tau."""
    rD, M = rhoD(aD, aT, eta), MN(N, aD, eta, rho)
    dC = (rho - rD) / ((N - 1) * M)
    return 0.0, dC, (N - 2) / (N - 1) * dC


def multilateral_war(N, aD, aT, eta, rho):
    """Proposition 3.5(ii): common d nu_j = d nu^E_A per unit d tau."""
    rD, M = rhoD(aD, aT, eta), MN(N, aD, eta, rho)
    return (N - 2) * (rho - rD) / ((N - 1) * M)


def bystander_disturbance(N, aD, aT, eta, rho):
    """F_C under a unilateral tariff."""
    return m(aD, aT) * (rho - rhoD(aD, aT, eta)) / (N - 1) ** 2


def rho_q_star(N, aD, aT, eta):
    """Proposition 3.7(i): real bilateral bystander threshold."""
    mm, rD = m(aD, aT), rhoD(aD, aT, eta)
    num = ((N - 1) - mm * N) * N * rD + mm * N * (N * aD * (eta - 1.0) + 1.0)
    return num / ((N - 1) * (1.0 - mm * N))


def real_unilateral(N, aD, aT, eta, rho):
    """(3.12): d log q_{AB}, d log q_{AC}, dq^E_A per unit d tau (unilateral)."""
    mm = m(aD, aT)
    neer, dB, dC = unilateral(N, aD, aT, eta, rho)
    k = 1.0 - mm * N / (N - 1)
    tbar = 1.0 / (N - 1)
    return k * dB - mm * tbar, k * dC - mm * tbar, k * neer - mm * tbar


# ---------------------------------------------------------- Prop. 3.6
def eta_C(N, aD, eta, rho):
    """Effective home-import elasticity of the composite bystander (3.9)."""
    return ((N - 3) * rho + 2.0 * aD * eta) / (N - 3 + 2.0 * aD)


def h_C(N, aD):
    return aD + (1.0 - aD) * (N - 3) / (N - 1)


def composite_base(N, aD, aT, eta, rho, ordinary_eta=False):
    """Three-country baseline {A, B, C} reproducing the symmetric N-country
    economy (Proposition 3.6).  With ordinary_eta=True, C keeps the same
    flows but the primitive eta instead of eta_C."""
    y = np.array([1.0, 1.0, N - 2.0])
    h = np.array([aD, aD, h_C(N, aD)])
    w_other, w_C = 1.0 / (N - 1), (N - 2.0) / (N - 1)
    b = np.array([[0.0, w_other, w_C],
                  [w_other, 0.0, w_C],
                  [0.5, 0.5, 0.0]])
    eC = eta if ordinary_eta else eta_C(N, aD, eta, rho)
    return dict(y=y, h=h, b=b, aT=np.full(3, aT),
                eta=np.array([eta, eta, eC]), rho=np.full(3, rho))


def composite_system(N, aD, aT, eta, rho):
    """(3.10): reduced -J of the composite economy and c = m M_N/(N-1)."""
    c = m(aD, aT) * MN(N, aD, eta, rho) / (N - 1)
    A = c * np.array([[N - 1.0, -(N - 2.0)], [-(N - 2.0), 2.0 * (N - 2.0)]])
    return A, c
