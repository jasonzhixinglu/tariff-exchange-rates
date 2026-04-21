import { useState, useEffect, useMemo, useCallback } from 'react'
import { buildIndex, interpolate, AXES } from '../lib/interpolate.js'
import LocusChart from './LocusChart.jsx'

// ---------------------------------------------------------------------------
// Scenario presets
// ---------------------------------------------------------------------------
const PRESETS = [
  { label: 'Free Trade',
    vals: { tau_AB: 0,    tau_BA: 0,    tau_AC: 0,    tau_CA: 0, tau_BC: 0, tau_CB: 0, sigma: 2 } },
  { label: 'Isolated Tariff',
    vals: { tau_AB: 0.25, tau_BA: 0,    tau_AC: 0,    tau_CA: 0, tau_BC: 0, tau_CB: 0, sigma: 2 } },
  { label: 'Uniform Tariff',
    vals: { tau_AB: 0.25, tau_BA: 0,    tau_AC: 0.25, tau_CA: 0, tau_BC: 0, tau_CB: 0, sigma: 2 } },
  { label: 'Trade War',
    vals: { tau_AB: 0.25, tau_BA: 0.25, tau_AC: 0,    tau_CA: 0, tau_BC: 0, tau_CB: 0, sigma: 2 } },
]

const DEFAULT = PRESETS[1].vals

// ---------------------------------------------------------------------------
// Small helpers
// ---------------------------------------------------------------------------
function SliderRow({ label, dim, value, onChange, min, max, step = 0.01 }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between items-baseline">
        <span className="text-xs text-slate-400">{label}</span>
        <span className="font-mono text-xs text-indigo-300 tabular-nums">{value.toFixed(2)}</span>
      </div>
      <input
        type="range"
        min={min ?? AXES[dim][0]}
        max={max ?? AXES[dim][AXES[dim].length - 1]}
        step={step}
        value={value}
        onChange={e => onChange(dim, parseFloat(e.target.value))}
        className="slider"
      />
    </div>
  )
}

function DeltaCard({ label, sub, value }) {
  if (value == null) return null
  const pos = value >  0.05
  const neg = value < -0.05
  return (
    <div className={`rounded-lg border px-3 py-2.5 flex flex-col gap-0.5 ${
      pos ? 'bg-amber-950/30 border-amber-700/40' :
      neg ? 'bg-sky-950/30  border-sky-700/40'   :
            'bg-slate-800/40 border-slate-700/40'
    }`}>
      <div className="flex justify-between items-baseline gap-2">
        <span className="text-xs text-slate-500 font-mono">{label}</span>
        <span className={`text-base font-mono font-semibold tabular-nums ${
          pos ? 'text-amber-400' : neg ? 'text-sky-400' : 'text-slate-400'
        }`}>
          {value > 0 ? '+' : ''}{value.toFixed(2)}%
        </span>
      </div>
      <span className="text-xs text-slate-600">{sub}</span>
    </div>
  )
}

function CWBadge({ deltaAC }) {
  if (deltaAC == null) return null
  const violated = deltaAC > 0.1
  return (
    <div className={`rounded-lg px-3 py-2 border text-center ${
      violated ? 'bg-amber-900/20 border-amber-600/40' : 'bg-sky-900/20 border-sky-600/40'
    }`}>
      <div className={`text-xs font-bold uppercase tracking-wider ${
        violated ? 'text-amber-400' : 'text-sky-400'
      }`}>
        {violated ? '⚡ CW Violated' : '✓ CW Holds'}
      </div>
      <div className="text-xs text-slate-500 mt-0.5 leading-tight">
        {violated
          ? 'A depreciates vs C — trade diversion dominates'
          : 'A appreciates vs C — conventional result'}
      </div>
    </div>
  )
}


// ---------------------------------------------------------------------------
// Main panel
// ---------------------------------------------------------------------------
export default function TheoryPanel() {
  const [gridIndex,    setGridIndex]    = useState(null)
  const [params,       setParams]       = useState(DEFAULT)
  const [activePreset, setActivePreset] = useState(1)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [loading,      setLoading]      = useState(true)

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/theory_grid.json`)
      .then(r => r.json())
      .then(data => { setGridIndex(buildIndex(data.grid)); setLoading(false) })
  }, [])

  const setParam = useCallback((dim, val) => {
    setParams(p => ({ ...p, [dim]: val }))
    setActivePreset(null)
  }, [])

  const applyPreset = useCallback((idx) => {
    setParams(PRESETS[idx].vals)
    setActivePreset(idx)
    setShowAdvanced(false)
  }, [])

  const eq = useMemo(
    () => (gridIndex ? interpolate(gridIndex, params) : null),
    [gridIndex, params]
  )

  if (loading) {
    return <div className="flex items-center justify-center h-64 text-slate-500">Loading theory grid…</div>
  }

  return (
    <div className="flex flex-col lg:flex-row gap-4 lg:h-full">

      {/* ── Left sidebar: controls ── */}
      <div className="panel p-4 flex flex-col gap-4 lg:overflow-y-auto lg:shrink-0 lg:w-[260px]">

        {/* Presets */}
        <div>
          <div className="label mb-2">Scenario</div>
          <div className="grid grid-cols-2 gap-1">
            {PRESETS.map((p, i) => (
              <button key={p.label} onClick={() => applyPreset(i)}
                className={`text-xs py-1.5 px-2 rounded-md font-medium transition-all ${
                  activePreset === i
                    ? 'bg-indigo-600 text-white'
                    : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >{p.label}</button>
            ))}
          </div>
        </div>

        <div className="border-t border-slate-800" />

        {/* Sigma */}
        <SliderRow label="σ — Elasticity of substitution"
          dim="sigma" value={params.sigma} min={1} max={8} step={0.1} onChange={setParam} />

        <div className="border-t border-slate-800" />

        {/* Main tariffs */}
        <div className="space-y-3">
          <div className="label text-slate-600">Tariff rates</div>
          <SliderRow label="τ_AB  (A tariffs B)" dim="tau_AB" value={params.tau_AB} onChange={setParam} />
          <SliderRow label="τ_BA  (B tariffs A)" dim="tau_BA" value={params.tau_BA} onChange={setParam} />
          <SliderRow label="τ_AC  (A tariffs C)" dim="tau_AC" value={params.tau_AC} onChange={setParam} />
        </div>

        {/* Advanced toggle */}
        <button onClick={() => setShowAdvanced(v => !v)}
          className="flex items-center gap-2 text-xs text-slate-600 hover:text-slate-400 transition-colors"
        >
          <span className={`transition-transform duration-150 ${showAdvanced ? 'rotate-90' : ''}`}>▶</span>
          C-side tariffs
        </button>

        {showAdvanced && (
          <div className="space-y-3 pl-3 border-l border-slate-800">
            <SliderRow label="τ_CA  (C tariffs A)" dim="tau_CA" value={params.tau_CA} onChange={setParam} />
            <SliderRow label="τ_BC  (B tariffs C)" dim="tau_BC" value={params.tau_BC} onChange={setParam} />
            <SliderRow label="τ_CB  (C tariffs B)" dim="tau_CB" value={params.tau_CB} onChange={setParam} />
          </div>
        )}

        <div className="mt-auto pt-3 border-t border-slate-800 text-xs text-slate-700 leading-relaxed">
          Symmetric: L<sub>i</sub>=1, &alpha;<sub>T,i</sub>=0.25 for all i.
        </div>
      </div>

      {/* ── Center: locus chart ── */}
      <div className="flex-1 min-w-0">
        <LocusChart params={params} equilibrium={eq} />
      </div>

      {/* ── Right: results ── */}
      <div className="lg:shrink-0 lg:w-[230px]">
        <div className="label px-1 mb-2">Equilibrium shifts</div>
        <div className="grid grid-cols-3 lg:grid-cols-1 gap-2 lg:gap-2.5">
          <DeltaCard
            label="Δe_AB"
            sub="USD vs B  (− = A appreciates)"
            value={eq?.delta_AB}
          />
          <DeltaCard
            label="Δe_AC"
            sub="USD vs C  (− = A appreciates)"
            value={eq?.delta_AC}
          />
          <DeltaCard
            label="Δe_BC"
            sub="B vs C"
            value={eq?.delta_BC}
          />
        </div>
        <div className="border-t border-slate-800 my-2 lg:my-0.5" />
        <CWBadge deltaAC={eq?.delta_AC} />
      </div>

    </div>
  )
}
