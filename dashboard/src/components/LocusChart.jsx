/**
 * Animated equilibrium locus chart.
 *
 * Draws the TB_B = 0 and TB_C = 0 balanced-trade loci in (e_AB, e_AC) log space,
 * animating from the free-trade baseline (all tau = 0) to the current tariff params.
 *
 * The intersection of the two loci is the equilibrium exchange rate pair.
 */

import { useEffect, useRef, useCallback } from 'react'
import { computeGrid, zeroContour, tariffMatrix } from '../lib/modelJs.js'

// Grid resolution and range
const N_GRID   = 90
const LOG_MIN  = -0.60
const LOG_MAX  =  0.60
const ANIM_MS  = 900          // animation duration when params change

function linspace(lo, hi, n) {
  return Array.from({ length: n }, (_, i) => lo + (i / (n - 1)) * (hi - lo))
}

const LOG_EAB_VEC = linspace(LOG_MIN, LOG_MAX, N_GRID)
const LOG_EAC_VEC = linspace(LOG_MIN, LOG_MAX, N_GRID)

// Free-trade grid (tau = 0 everywhere) — computed once
const FREE_TRADE_TAU = [[0,0,0],[0,0,0],[0,0,0]]

function buildContours(tau, sigma) {
  const { TB_B, TB_C } = computeGrid(LOG_EAB_VEC, LOG_EAC_VEC, tau, sigma)
  return {
    locusB: zeroContour(TB_B, N_GRID, N_GRID, LOG_EAB_VEC, LOG_EAC_VEC),
    locusC: zeroContour(TB_C, N_GRID, N_GRID, LOG_EAB_VEC, LOG_EAC_VEC),
  }
}

// Map log-exchange-rate value to SVG coordinate (0–400)
const SVG_SIZE = 400
function toSVG(logE) {
  return ((logE - LOG_MIN) / (LOG_MAX - LOG_MIN)) * SVG_SIZE
}
function fromSVG(svgX) {
  return LOG_MIN + (svgX / SVG_SIZE) * (LOG_MAX - LOG_MIN)
}

function pointsToPath(pts) {
  if (!pts.length) return ''
  return (
    'M ' +
    pts.map(p => `${toSVG(p.x).toFixed(2)},${(SVG_SIZE - toSVG(p.y)).toFixed(2)}`).join(' L ')
  )
}

function lerp(a, b, t) { return a + (b - a) * t }

function lerpTau(from, to, t) {
  return from.map((row, i) => row.map((v, j) => lerp(v, to[i][j], t)))
}

function easeInOut(t) {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t
}

export default function LocusChart({ params, equilibrium }) {
  const svgRef       = useRef(null)
  const animRef      = useRef(null)
  const startRef     = useRef(null)
  const fromTauRef   = useRef(FREE_TRADE_TAU)
  const targetTauRef = useRef(FREE_TRADE_TAU)
  const curTauRef    = useRef(FREE_TRADE_TAU)

  // Pre-compute free-trade loci (never change)
  const ftContoursRef = useRef(null)
  if (!ftContoursRef.current) {
    ftContoursRef.current = buildContours(FREE_TRADE_TAU, 2)
  }

  const drawFrame = useCallback((tau) => {
    const svg = svgRef.current
    if (!svg) return

    const sigma = params.sigma
    const { locusB, locusC } = buildContours(tau, sigma)
    const ft = ftContoursRef.current

    // Update path elements
    svg.querySelector('#ft-locus-b').setAttribute('d', pointsToPath(ft.locusB))
    svg.querySelector('#ft-locus-c').setAttribute('d', pointsToPath(ft.locusC))
    svg.querySelector('#locus-b').setAttribute('d', pointsToPath(locusB))
    svg.querySelector('#locus-c').setAttribute('d', pointsToPath(locusC))

    // Equilibrium point from interpolated grid data
    if (equilibrium) {
      const ex = toSVG(Math.log(equilibrium.e_AB))
      const ey = SVG_SIZE - toSVG(Math.log(equilibrium.e_AC))
      const dot = svg.querySelector('#eq-dot')
      dot.setAttribute('cx', ex.toFixed(2))
      dot.setAttribute('cy', ey.toFixed(2))
      dot.setAttribute('visibility', 'visible')
    }
  }, [params.sigma, equilibrium])

  // Animate when params change
  useEffect(() => {
    const newTau = tariffMatrix(params)
    targetTauRef.current = newTau
    fromTauRef.current   = curTauRef.current

    if (animRef.current) cancelAnimationFrame(animRef.current)
    startRef.current = null

    function step(ts) {
      if (!startRef.current) startRef.current = ts
      const elapsed = ts - startRef.current
      const t       = easeInOut(Math.min(elapsed / ANIM_MS, 1))

      const interpolated = lerpTau(fromTauRef.current, targetTauRef.current, t)
      curTauRef.current  = interpolated
      drawFrame(interpolated)

      if (t < 1) animRef.current = requestAnimationFrame(step)
    }

    animRef.current = requestAnimationFrame(step)
    return () => { if (animRef.current) cancelAnimationFrame(animRef.current) }
  }, [
    params.tau_AB, params.tau_BA, params.tau_AC,
    params.tau_CA, params.tau_BC, params.tau_CB,
    params.sigma,
    drawFrame,
  ])

  // Tick labels for axes
  const axisTicks = [-0.6, -0.3, 0, 0.3, 0.6]

  return (
    <div className="card p-4 flex flex-col gap-2 lg:flex-1">
      <div className="flex flex-col gap-1.5 sm:flex-row sm:items-center sm:justify-between">
        <span className="label">Balanced-trade loci</span>
        <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs">
          <span className="flex items-center gap-1.5">
            <span className="inline-block w-5 h-0.5 bg-indigo-400 opacity-30 border-dashed border-t border-indigo-400" />
            <span className="text-slate-600">Free trade</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="inline-block w-4 h-0.5 bg-indigo-400" />
            <span className="text-indigo-400">TB<sub>B</sub>=0</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="inline-block w-4 h-0.5 bg-amber-400" />
            <span className="text-amber-400">TB<sub>C</sub>=0</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="inline-block w-2.5 h-2.5 rounded-full bg-white" />
            <span className="text-slate-300">Equilibrium</span>
          </span>
        </div>
      </div>

      <div className="relative pl-6 lg:pl-0">
        {/* Y-axis label */}
        <div className="absolute left-0 lg:-left-1 top-1/2 -translate-y-1/2 lg:-translate-x-full">
          <span
            className="label text-slate-600 whitespace-nowrap"
            style={{ writingMode: 'vertical-rl', transform: 'rotate(180deg)' }}
          >
            log e<sub>AC</sub>  (+ = A depreciates vs C)
          </span>
        </div>

        <svg
          ref={svgRef}
          viewBox={`0 0 ${SVG_SIZE} ${SVG_SIZE}`}
          className="w-full"
          style={{ aspectRatio: '1 / 1' }}
        >
          {/* Background */}
          <rect width={SVG_SIZE} height={SVG_SIZE} fill="#0f172a" rx="4" />

          {/* Grid lines */}
          {axisTicks.map(v => (
            <g key={v}>
              <line
                x1={toSVG(v)} y1={0} x2={toSVG(v)} y2={SVG_SIZE}
                stroke="#1e293b" strokeWidth="1"
              />
              <line
                x1={0} y1={SVG_SIZE - toSVG(v)} x2={SVG_SIZE} y2={SVG_SIZE - toSVG(v)}
                stroke="#1e293b" strokeWidth="1"
              />
            </g>
          ))}

          {/* Axis lines through origin */}
          <line
            x1={toSVG(0)} y1={0} x2={toSVG(0)} y2={SVG_SIZE}
            stroke="#334155" strokeWidth="1.5" strokeDasharray="4 4"
          />
          <line
            x1={0} y1={SVG_SIZE - toSVG(0)} x2={SVG_SIZE} y2={SVG_SIZE - toSVG(0)}
            stroke="#334155" strokeWidth="1.5" strokeDasharray="4 4"
          />

          {/* Free-trade loci (faint reference) */}
          <path id="ft-locus-b" fill="none" stroke="#6366f1" strokeWidth="1"
            strokeDasharray="4 3" opacity="0.35" />
          <path id="ft-locus-c" fill="none" stroke="#f59e0b" strokeWidth="1"
            strokeDasharray="4 3" opacity="0.35" />

          {/* Current loci */}
          <path id="locus-b" fill="none" stroke="#818cf8" strokeWidth="2.5"
            strokeLinecap="round" strokeLinejoin="round" />
          <path id="locus-c" fill="none" stroke="#fbbf24" strokeWidth="2.5"
            strokeLinecap="round" strokeLinejoin="round" />

          {/* Free-trade equilibrium dot */}
          <circle
            cx={toSVG(0)} cy={SVG_SIZE - toSVG(0)}
            r="4" fill="#475569" stroke="#94a3b8" strokeWidth="1"
          />
          <text
            x={toSVG(0) + 7} y={SVG_SIZE - toSVG(0) - 6}
            fill="#64748b" fontSize="9" fontFamily="monospace"
          >
            FT
          </text>

          {/* Equilibrium dot (updated by drawFrame) */}
          <circle id="eq-dot" cx={toSVG(0)} cy={SVG_SIZE - toSVG(0)}
            r="6" fill="white" stroke="#0f172a" strokeWidth="1.5"
            visibility="hidden"
          />

          {/* Axis tick labels */}
          {axisTicks.filter(v => v !== 0).map(v => (
            <g key={v}>
              <text
                x={toSVG(v)} y={SVG_SIZE - 4}
                fill="#475569" fontSize="8.5" textAnchor="middle" fontFamily="monospace"
              >
                {v > 0 ? `+${v}` : v}
              </text>
              <text
                x={4} y={SVG_SIZE - toSVG(v) + 3}
                fill="#475569" fontSize="8.5" textAnchor="start" fontFamily="monospace"
              >
                {v > 0 ? `+${v}` : v}
              </text>
            </g>
          ))}
        </svg>
      </div>

      {/* X-axis label */}
      <div className="text-center">
        <span className="label text-slate-600">
          log e<sub>AB</sub>  (+ = A depreciates vs B)
        </span>
      </div>
    </div>
  )
}
