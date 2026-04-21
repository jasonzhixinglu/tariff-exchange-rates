/**
 * Multilinear interpolation over the 3^7 theory grid.
 *
 * Grid axes (3 points each):
 *   tau_AB, tau_BA, tau_AC, tau_CA, tau_BC, tau_CB  -> [0, 0.25, 0.75]
 *   sigma                                            -> [1, 2, 8]
 *
 * The grid is stored as a flat array of records. On first call, buildIndex()
 * converts it to a Map keyed by comma-separated dimension indices for O(1)
 * lookup during interpolation.
 */

export const AXES = {
  tau_AB: [0, 0.25, 0.75],
  tau_BA: [0, 0.25, 0.75],
  tau_AC: [0, 0.25, 0.75],
  tau_CA: [0, 0.25, 0.75],
  tau_BC: [0, 0.25, 0.75],
  tau_CB: [0, 0.25, 0.75],
  sigma:  [1, 2, 8],
}

export const DIMS = Object.keys(AXES)

// Snap a query value to the nearest axis grid point
export function snapToGrid(dim, val) {
  const pts = AXES[dim]
  return pts.reduce((best, p) => Math.abs(p - val) < Math.abs(best - val) ? p : best)
}

/**
 * Build a Map<string, record> from the flat grid array.
 * Key format: "i0,i1,i2,i3,i4,i5,i6" (indices into each axis).
 */
export function buildIndex(gridRecords) {
  const index = new Map()
  for (const rec of gridRecords) {
    const key = DIMS.map(dim => {
      const pts = AXES[dim]
      const i = pts.findIndex(v => Math.abs(v - rec[dim]) < 1e-9)
      return i
    }).join(',')
    index.set(key, rec)
  }
  return index
}

/**
 * 7-dimensional multilinear interpolation.
 *
 * query: { tau_AB, tau_BA, tau_AC, tau_CA, tau_BC, tau_CB, sigma }
 * Returns: { e_AB, e_AC, e_BC, delta_AB, delta_AC, delta_BC }
 *
 * delta values are 100 * ln(e) — log-point % changes from the symmetric
 * free-trade baseline where all exchange rates equal 1.
 */
export function interpolate(index, query) {
  const n = DIMS.length

  // Clamp and bracket each dimension
  const brackets = DIMS.map(dim => {
    const pts = AXES[dim]
    const q = Math.max(pts[0], Math.min(pts[pts.length - 1], query[dim]))
    let lo = pts.length - 2
    for (let j = 0; j < pts.length - 1; j++) {
      if (q <= pts[j + 1] + 1e-12) { lo = j; break }
    }
    const span = pts[lo + 1] - pts[lo]
    const t = span > 1e-12 ? (q - pts[lo]) / span : 0
    return { lo, t }
  })

  let eAB = 0, eAC = 0, eBC = 0

  // Sum over all 2^n = 128 corners
  for (let mask = 0; mask < (1 << n); mask++) {
    let weight = 1
    const idxArr = []

    for (let d = 0; d < n; d++) {
      const { lo, t } = brackets[d]
      const bit = (mask >> d) & 1
      idxArr.push(lo + bit)
      weight *= bit === 1 ? t : (1 - t)
    }

    if (weight < 1e-14) continue

    const pt = index.get(idxArr.join(','))
    if (!pt || pt.e_AB == null) continue

    eAB += weight * pt.e_AB
    eAC += weight * pt.e_AC
    eBC += weight * pt.e_BC
  }

  return {
    e_AB: eAB,
    e_AC: eAC,
    e_BC: eBC,
    // Free-trade baseline is always (1,1,1) in the symmetric model
    delta_AB: 100 * Math.log(eAB),
    delta_AC: 100 * Math.log(eAC),
    delta_BC: 100 * Math.log(eBC),
  }
}

/**
 * Sweep tau_AB from 0 to 0.75 (all 3 grid points) while holding other params
 * fixed, returning an array of interpolated equilibria. Used to draw the
 * equilibrium path in (delta_AB, delta_AC) space.
 */
export function sweepTauAB(index, query, nSteps = 40) {
  const [lo, hi] = [AXES.tau_AB[0], AXES.tau_AB[AXES.tau_AB.length - 1]]
  const points = []
  for (let i = 0; i <= nSteps; i++) {
    const t = i / nSteps
    const tau_AB = lo + t * (hi - lo)
    const eq = interpolate(index, { ...query, tau_AB })
    points.push({ tau_AB, ...eq })
  }
  return points
}
