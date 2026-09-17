# -*- coding: utf-8 -*-
"""Verification for the heterogeneous-bilateral-substitution appendix.

Replaces the common-rho CES import nest by a general homothetic import
aggregator for each importer i, represented locally by a symmetric
substitution matrix S_i on i's origins with S_i 1 = 0 and off-diagonal
entries S_i[j,k] = rho^i_{jk} b_ij b_ik >= 0.  The CES case is
rho^i_{jk} = rho for all (i,j,k).

Claims checked numerically against a brute-force linearization:

  (G)   G = m y_A [ S_A - rho1* b_A b_A' ]                     (rows i != A)
  (J)   Jtilde = Shat - m ( Y K + theta K' Y K ),
        Shat = sum_k m y_k S_k (extended by zeros in row/col k),
        K = B - I,  theta = 1 + aD(eta-1),  Y = diag(y)
  (R)   row sums and column sums of Jtilde vanish
  (C)   under exchangeability both reduce to the paper's formulas
"""
import numpy as np

rng = np.random.default_rng(20260917)


def rho1_star(aD, aT, eta):
    return 1.0 + aD * (eta - 1.0) - aT * (1.0 - aD)


def build_S(N, rho_mat, b):
    """S_k, extended to N x N with zero row/col k. rho_mat[k][j,l] symmetric."""
    S = []
    for k in range(N):
        Sk = np.zeros((N, N))
        for j in range(N):
            if j == k:
                continue
            for l in range(N):
                if l == k or l == j:
                    continue
                Sk[j, l] = rho_mat[k][j, l] * b[k, j] * b[k, l]
        for j in range(N):
            Sk[j, j] = -Sk[j].sum()
        S.append(Sk)
    return S


def dTB_coeffs(N, b, y, aD, aT, eta, S):
    """Brute-force linearization. Returns (Jt, Gfull) with
    dTB_i = sum_l Jt[i,l] nu_l + sum_j Gfull[i,j] dt_Aj  (tariffs by A=0 only)."""
    m = aT * (1.0 - aD)
    f = m * y[:, None] * b
    nvar = N + N                      # [nu_0..nu_{N-1}, dt_A0..dt_A{N-1}]

    def zero():
        return np.zeros(nvar)

    # bilateral consumer log prices
    dp = np.zeros((N, N, nvar))
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            dp[i, j][j] += 1.0
            dp[i, j][i] -= 1.0
            if i == 0:
                dp[i, j][N + j] += 1.0

    # import price index
    dPM = np.zeros((N, nvar))
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            dPM[i] += b[i, j] * dp[i, j]

    # within-nest share: b_ij dlog b_ij = (S_i dp_i)_j + b_ij (dp_ij - dPM_i)
    # total share: dlog s_ij = dlog b_ij + (1-eta) aD dPM_i
    f_dlogs = np.zeros((N, N, nvar))   # f_ij * dlog s_ij
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            Sdp = zero()
            for l in range(N):
                if l == i:
                    continue
                Sdp = Sdp + S[i][j, l] * dp[i, l]
            b_dlogb = Sdp + b[i, j] * (dp[i, j] - dPM[i])
            f_dlogs[i, j] = m * y[i] * (b_dlogb + b[i, j] * (1 - eta) * aD * dPM[i])

    # income (common currency): dlog Itilde_i = nu_i + sum_j s_ij dt_ij
    dI = np.zeros((N, nvar))
    for i in range(N):
        dI[i][i] += 1.0
        if i == 0:
            for j in range(1, N):
                dI[i][N + j] += m * b[0, j]

    dt_vec = np.zeros((N, N, nvar))
    for j in range(N):
        if j != 0:
            dt_vec[0, j][N + j] = 1.0

    dTB = np.zeros((N, nvar))
    for i in range(N):
        acc = zero()
        for k in range(N):
            if k == i:
                continue
            acc = acc + f_dlogs[k, i] + f[k, i] * (dI[k] - dt_vec[k, i])
        for j in range(N):
            if j == i:
                continue
            acc = acc - f_dlogs[i, j] - f[i, j] * (dI[i] - dt_vec[i, j])
        dTB[i] = acc
    return dTB[:, :N], dTB[:, N:]


def closed_form(N, b, y, aD, aT, eta, S):
    m = aT * (1.0 - aD)
    theta = 1.0 + aD * (eta - 1.0)
    K = b - np.eye(N)
    Y = np.diag(y)
    Shat = sum(m * y[k] * S[k] for k in range(N))
    Jt = Shat - m * (Y @ K + theta * K.T @ Y @ K)
    bA = b[0]
    G = m * y[0] * (S[0] - rho1_star(aD, aT, eta) * np.outer(bA, bA))
    return Jt, G


def random_baseline(N, heterogeneous=True):
    """Symmetric, doubly stochastic b with zero diagonal; equal sizes y=1."""
    M = rng.uniform(0.5, 2.0, (N, N))
    M = M + M.T
    np.fill_diagonal(M, 0.0)
    for _ in range(5000):
        M = M / M.sum(axis=1, keepdims=True)
        M = (M + M.T) / 2.0
    return M, _rho_draws(N, heterogeneous)


def _rho_draws(N, heterogeneous):
    if heterogeneous:
        out = []
        for _ in range(N):
            R = rng.uniform(0.3, 4.0, (N, N))
            out.append((R + R.T) / 2.0)
        return out
    return [np.full((N, N), 1.7) for _ in range(N)]


def check(N, heterogeneous, aD=0.62, aT=0.55, eta=1.9):
    b, rho_mat = random_baseline(N, heterogeneous)
    y = np.ones(N)
    S = build_S(N, rho_mat, b)
    Jt_num, G_num = dTB_coeffs(N, b, y, aD, aT, eta, S)
    Jt_cf, G_cf = closed_form(N, b, y, aD, aT, eta, S)
    errJ = np.abs(Jt_num - Jt_cf).max()
    errG = np.abs(G_num[1:, 1:] - G_cf[1:, 1:]).max()
    rowsum = np.abs(Jt_cf.sum(axis=1)).max()
    colsum = np.abs(Jt_cf.sum(axis=0)).max()
    print("N=%d het=%s: |J_num-J_cf|=%.2e |G_num-G_cf|=%.2e rowsum=%.2e colsum=%.2e"
          % (N, heterogeneous, errJ, errG, rowsum, colsum))
    assert errJ < 1e-9 and errG < 1e-9 and rowsum < 1e-9 and colsum < 1e-9


def check_unequal_sizes(N, aD=0.62, aT=0.55, eta=1.9):
    """Balanced baseline with unequal country sizes: take any symmetric flow
    matrix f, then y_i = (sum_j f_ij)/m and b_ij = f_ij/(m y_i)."""
    m = aT * (1 - aD)
    f = rng.uniform(0.2, 2.0, (N, N))
    f = f + f.T
    np.fill_diagonal(f, 0.0)
    y = f.sum(axis=1) / m
    b = f / (m * y[:, None])
    S = build_S(N, _rho_draws(N, True), b)
    Jt_num, G_num = dTB_coeffs(N, b, y, aD, aT, eta, S)
    Jt_cf, G_cf = closed_form(N, b, y, aD, aT, eta, S)
    errJ = np.abs(Jt_num - Jt_cf).max()
    errG = np.abs(G_num[1:, 1:] - G_cf[1:, 1:]).max()
    rowsum = np.abs(Jt_cf.sum(axis=1)).max()
    colsum = np.abs(Jt_cf.sum(axis=0)).max()
    print("unequal sizes N=%d: |J_num-J_cf|=%.2e |G_num-G_cf|=%.2e "
          "rowsum=%.2e colsum=%.2e" % (N, errJ, errG, rowsum, colsum))
    assert max(errJ, errG, rowsum, colsum) < 1e-9


def check_ces_reduction(N, aD=0.62, aT=0.55, eta=1.9, rho=1.7):
    """Exchangeable baseline must reproduce the paper's closed forms."""
    b = (np.ones((N, N)) - np.eye(N)) / (N - 1)
    y = np.ones(N)
    rho_mat = [np.full((N, N), rho) for _ in range(N)]
    S = build_S(N, rho_mat, b)
    Jt, G = closed_form(N, b, y, aD, aT, eta, S)
    m = aT * (1 - aD)
    r1 = rho1_star(aD, aT, eta)
    DN = N * aD * (eta - 1) + (N - 2) * rho + 1
    Jt_paper = (m * DN / (N - 1) ** 2) * (np.ones((N, N)) - N * np.eye(N))
    gS, gD = -m * r1 / (N - 1), -m * rho / (N - 1)
    Gp = gD * np.eye(N - 1) + ((gS - gD) / (N - 1)) * np.ones((N - 1, N - 1))
    errJ = np.abs(Jt - Jt_paper).max()
    errG = np.abs(G[1:, 1:] - Gp).max()
    J = Jt[1:, 1:]
    F = G[1:, 1]
    nu = np.linalg.solve(-J, F)
    nuB = -(N * r1 + (N - 2) * rho) / (N * DN)
    nuC = (rho - N * r1) / (N * DN)
    errnu = abs(nu[0] - nuB)
    if N > 2:
        errnu = max(errnu, np.abs(nu[1:] - nuC).max())
    print("CES N=%d: |J-J_paper|=%.2e |G-G_paper|=%.2e |nu-nu_paper|=%.2e"
          % (N, errJ, errG, errnu))
    assert errJ < 1e-10 and errG < 1e-10 and errnu < 1e-10


def check_laplacian(N):
    """Shat must be minus a weighted Laplacian."""
    b, rho_mat = random_baseline(N, True)
    S = build_S(N, rho_mat, b)
    L = -sum(S[k] for k in range(N))
    assert np.abs(L - L.T).max() < 1e-12
    assert np.abs(L.sum(axis=1)).max() < 1e-12
    off = L - np.diag(np.diag(L))
    assert off.max() <= 1e-12
    w = np.linalg.eigvalsh(L)
    assert w.min() > -1e-10
    print("Laplacian N=%d: eigenvalues %s" % (N, np.round(np.sort(w), 4)))


def check_uniform_tariff(N):
    """G 1 = -m y_A rho1* b_A for any substitution structure."""
    b, rho_mat = random_baseline(N, True)
    y = np.ones(N)
    aD, aT, eta = 0.62, 0.55, 1.9
    S = build_S(N, rho_mat, b)
    _, G = closed_form(N, b, y, aD, aT, eta, S)
    m = aT * (1 - aD)
    err = np.abs(G[1:, 1:] @ np.ones(N - 1)
                 + m * rho1_star(aD, aT, eta) * b[0, 1:]).max()
    print("uniform tariff N=%d: |G1 + m rho1* b_A| = %.2e" % (N, err))
    assert err < 1e-10


def check_circulant(N=6, aD=0.62, aT=0.55, eta=1.9):
    """Circulant baseline: B and Shat circulant, hence simultaneously
    diagonalized by the DFT; lambda_D becomes a spectrum."""
    ws = rng.uniform(0.2, 1.0, N)
    ws[0] = 0.0
    ws = np.array([(ws[k] + ws[(-k) % N]) / 2 for k in range(N)])
    ws = ws / ws.sum()
    b = np.array([[ws[(j - i) % N] for j in range(N)] for i in range(N)])
    rc = rng.uniform(0.5, 3.0, N)
    rc = np.array([(rc[k] + rc[(-k) % N]) / 2 for k in range(N)])
    rho_mat = [np.array([[rc[(l - j) % N] for l in range(N)]
                         for j in range(N)]) for _ in range(N)]
    y = np.ones(N)
    S = build_S(N, rho_mat, b)
    Jt_num, _ = dTB_coeffs(N, b, y, aD, aT, eta, S)
    Jt, _ = closed_form(N, b, y, aD, aT, eta, S)
    assert np.abs(Jt - Jt_num).max() < 1e-9
    circ_err = max(abs(Jt[i, j] - Jt[0, (j - i) % N])
                   for i in range(N) for j in range(N))
    print("circulant N=%d: Jtilde circulant deviation = %.2e" % (N, circ_err))
    assert circ_err < 1e-9
    ev = np.sort(np.real(np.linalg.eigvals(-Jt)))
    print("  eigenvalues of -Jtilde: %s" % np.round(ev, 5))


if __name__ == "__main__":
    for N in (3, 4, 5, 6):
        check(N, heterogeneous=True)
        check(N, heterogeneous=False)
    for N in (3, 4, 5):
        check_unequal_sizes(N)
    for N in (2, 3, 4, 5, 6):
        check_ces_reduction(N)
    for N in (4, 6):
        check_laplacian(N)
        check_uniform_tariff(N)
    check_circulant()
    print("\nAll heterogeneous-substitution checks passed.")
