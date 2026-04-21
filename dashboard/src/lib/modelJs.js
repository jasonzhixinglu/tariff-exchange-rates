/**
 * Three-country model in JavaScript — mirrors economy.py exactly.
 *
 * Symmetric parameterisation (fixed for the theory panel):
 *   L_i = 1, A_T_i = A_N_i = 1, P_T_i = 1 for all i
 *   alpha_T = [0.25, 0.25, 0.25], alpha_N = 0.25
 *
 * Convention: countries 0=A, 1=B, 2=C
 *   E[i][j] = units of i's currency per unit of j's currency
 *   tau[i][j] = ad valorem tariff imposed by i on j (diagonal = 0)
 *
 * Returns trade balances TB[i] in country i's own currency.
 * Equilibrium requires TB[1] = TB[2] = 0 (Walras: TB[0] then follows).
 */

const ALPHA_T = [0.25, 0.25, 0.25]
const ALPHA_N = 0.25

/**
 * Build the 3×3 exchange rate matrix from the two free rates.
 *   r = [1, eAB, eAC]   E[i][j] = r[j] / r[i]
 */
function exchangeMatrix(eAB, eAC) {
  const r = [1, eAB, eAC]
  return r.map(ri => r.map(rj => rj / ri))
}

/**
 * Build the 3×3 tariff matrix from the params object.
 */
export function tariffMatrix(params) {
  return [
    [0,            params.tau_AB, params.tau_AC],
    [params.tau_BA, 0,            params.tau_BC],
    [params.tau_CA, params.tau_CB, 0           ],
  ]
}

/**
 * Compute trade balances for all three countries given log exchange rates
 * and tariffs.
 *
 * logEAB, logEAC: log of the two free bilateral rates
 * tau: 3×3 tariff matrix (tau[i][j] = rate imposed by i on j)
 * sigma: CES elasticity
 *
 * Returns { TB_A, TB_B, TB_C }
 */
export function computeTB(logEAB, logEAC, tau, sigma) {
  const eAB = Math.exp(logEAB)
  const eAC = Math.exp(logEAC)
  const E   = exchangeMatrix(eAB, eAC)

  // Consumer prices: Pc[i][j] = (1 + tau[i][j]) * E[i][j]  (P_T = 1)
  const Pc = tau.map((row, i) => row.map((t, j) => (1 + t) * E[i][j]))

  // Disposable income (wages * L = 1 for all i in symmetric case)
  //   I[i] = 1 / (1 - sum_j alpha_T[j] * tau[i][j] / (1 + tau[i][j]))
  const income = tau.map((row, i) => {
    let wedge = 0
    for (let j = 0; j < 3; j++) {
      if (i !== j) wedge += ALPHA_T[j] * row[j] / (1 + row[j])
    }
    return 1 / (1 - wedge)
  })

  // Tradable demand: demand[i][j] = country i's quantity demand for j's good
  //
  // CES:  demand[i][j] = income[i] * alpha_T[j]^sigma * Pc[i][j]^(-sigma)
  //                      / sum_k( alpha_T[k]^sigma * Pc[i][k]^(1-sigma) )
  //
  // CD (sigma=1): demand[i][j] = income[i] * alpha_T[j] / Pc[i][j]
  let demand
  if (Math.abs(sigma - 1) < 1e-9) {
    demand = Pc.map((row, i) =>
      row.map((p, j) => income[i] * ALPHA_T[j] / p)
    )
  } else {
    demand = Pc.map((row, i) => {
      // denominator of CES weight
      let denom = 0
      for (let k = 0; k < 3; k++) {
        denom += Math.pow(ALPHA_T[k], sigma) * Math.pow(Pc[i][k], 1 - sigma)
      }
      return row.map((p, j) =>
        income[i] * Math.pow(ALPHA_T[j], sigma) * Math.pow(p, -sigma) / denom
      )
    })
  }

  // Trade balance: TB[i] = exports_i - imports_i (in i's currency)
  //   exports[i]  = sum_k demand[k][i]          (world demand for i's good, valued at P_T=1)
  //   imports[i]  = sum_j E[i][j] * demand[i][j] (i's spending on all goods, in i's currency)
  const TB = [0, 1, 2].map(i => {
    let exports_i = 0
    let imports_i = 0
    for (let k = 0; k < 3; k++) exports_i += demand[k][i]
    for (let j = 0; j < 3; j++) imports_i += E[i][j] * demand[i][j]
    return exports_i - imports_i
  })

  return { TB_A: TB[0], TB_B: TB[1], TB_C: TB[2] }
}

/**
 * Evaluate TB_B and TB_C over a 2-D grid of (logEAB, logEAC) values.
 *
 * Returns { TB_B: Float64Array, TB_C: Float64Array } where each array is
 * stored in row-major order: index = row * nCols + col,
 * row = logEAC index (0 = bottom), col = logEAB index (0 = left).
 */
export function computeGrid(logEAB_vec, logEAC_vec, tau, sigma) {
  const nR = logEAC_vec.length
  const nC = logEAB_vec.length
  const TB_B = new Float64Array(nR * nC)
  const TB_C = new Float64Array(nR * nC)

  for (let r = 0; r < nR; r++) {
    for (let c = 0; c < nC; c++) {
      const { TB_B: b, TB_C: cv } = computeTB(logEAB_vec[c], logEAC_vec[r], tau, sigma)
      TB_B[r * nC + c] = b
      TB_C[r * nC + c] = cv
    }
  }
  return { TB_B, TB_C }
}

/**
 * Extract zero-contour polyline by scanning row-by-row (fixed y, sweep x).
 *
 * For each y-row, finds where the scalar field crosses zero along x via
 * linear interpolation. Returns an array of {x, y} points ordered bottom
 * to top — suitable as a direct SVG polyline for smooth, single-valued loci.
 *
 * Falls back to a column scan if the row scan yields too few points (e.g.
 * nearly-horizontal loci).
 */
export function zeroContour(values, nR, nC, xVec, yVec) {
  const rowPts = []

  for (let r = 0; r < nR; r++) {
    for (let c = 0; c < nC - 1; c++) {
      const v0 = values[r * nC + c]
      const v1 = values[r * nC + c + 1]
      if (isFinite(v0) && isFinite(v1) && Math.sign(v0) !== Math.sign(v1) && v0 !== v1) {
        const t = v0 / (v0 - v1)
        rowPts.push({ x: xVec[c] + t * (xVec[c + 1] - xVec[c]), y: yVec[r] })
        break  // one crossing per row keeps the polyline single-valued
      }
    }
  }

  // If the contour is nearly horizontal, column scan gives more points
  const colPts = []
  for (let c = 0; c < nC; c++) {
    for (let r = 0; r < nR - 1; r++) {
      const v0 = values[r * nC + c]
      const v1 = values[(r + 1) * nC + c]
      if (isFinite(v0) && isFinite(v1) && Math.sign(v0) !== Math.sign(v1) && v0 !== v1) {
        const t = v0 / (v0 - v1)
        colPts.push({ x: xVec[c], y: yVec[r] + t * (yVec[r + 1] - yVec[r]) })
        break
      }
    }
  }

  // Use whichever scan produced more points
  return rowPts.length >= colPts.length ? rowPts : colPts
}
