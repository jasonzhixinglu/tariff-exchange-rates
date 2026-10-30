import { useState } from 'react'

function DeltaRow({ label, model, data }) {
  const fmt = v => v == null ? '—' : `${v > 0 ? '+' : ''}${v.toFixed(2)}%`

  const modelColor = model == null ? 'text-slate-500'
    : model > 0.1 ? 'text-amber-400'
    : model < -0.1 ? 'text-sky-400'
    : 'text-slate-300'

  // For data, show whether direction agrees with model
  const dataColor = data == null ? 'text-slate-600'
    : (model != null && Math.sign(data) === Math.sign(model) && Math.abs(model) > 0.1)
    ? 'text-emerald-400'
    : 'text-rose-400'

  return (
    <div className="flex items-center justify-between text-xs py-0.5 gap-1">
      <span className="text-slate-500 font-mono shrink-0">{label}</span>
      <span className={`font-mono font-medium flex-1 text-right ${modelColor}`}>{fmt(model)}</span>
      <span className={`font-mono flex-1 text-right ${dataColor}`}>{fmt(data)}</span>
    </div>
  )
}

function CWViolationPill({ deltaAC }) {
  if (deltaAC == null) return null
  const violated = deltaAC > 0.1
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
      violated
        ? 'bg-amber-900/40 text-amber-400 border border-amber-700/50'
        : 'bg-sky-900/40 text-sky-400 border border-sky-700/50'
    }`}>
      {violated ? 'CW Violated' : 'CW Holds'}
    </span>
  )
}

export default function CountryCard({ countryKey, meta, regimes, fxData, activeRegime }) {
  const [showAdvanced, setShowAdvanced] = useState(false)

  const regime = regimes[activeRegime]
  if (!regime) return null

  const isError = !!regime.error
  const modelAB = isError ? null : regime.delta_e_AB
  const modelAC = isError ? null : regime.delta_e_AC
  const modelBC = isError ? null : regime.delta_e_BC

  const dataAB = fxData?.RMB?.pct_changes?.[activeRegime]
  const dataAC = fxData?.[countryKey]?.pct_changes?.[activeRegime]
  // e_BC = RMB/C: 100 × ((1 + d_AC/100) / (1 + d_AB/100) − 1)
  const dataBC = (dataAC != null && dataAB != null)
    ? 100 * ((1 + dataAC / 100) / (1 + dataAB / 100) - 1)
    : null

  return (
    <div className="card p-4 flex flex-col gap-3">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2">
          <span className="text-xl leading-none">{meta.flag}</span>
          <div>
            <div className="font-semibold text-sm text-slate-100">{meta.label}</div>
            <div className="text-xs text-slate-500">{meta.currency}</div>
          </div>
        </div>
        <CWViolationPill deltaAC={modelAC} />
      </div>

      {/* Exchange rate table */}
      {isError ? (
        <div className="text-xs text-rose-400">Solver error: {regime.error}</div>
      ) : (
        <>
          <div>
            <div className="flex justify-between text-xs text-slate-600 mb-1 font-medium gap-1">
              <span className="shrink-0">Rate</span>
              <span className="flex-1 text-right">Model</span>
              <span className="flex-1 text-right">Data</span>
            </div>
            <DeltaRow label="Δe_AB" model={modelAB} data={dataAB} />
            <DeltaRow label="Δe_AC" model={modelAC} data={dataAC} />
            <DeltaRow label="Δe_BC" model={modelBC} data={dataBC} />
          </div>
          <div className="text-xs text-slate-600 leading-relaxed">
            Data: % change vs 2024 avg.
            {activeRegime === 'regime1' ? ' March 2025.' : ' April 2025.'}
          </div>
        </>
      )}

      {/* Advanced toggle */}
      <button
        onClick={() => setShowAdvanced(v => !v)}
        className="flex items-center gap-1.5 text-xs text-slate-600 hover:text-slate-400 transition-colors mt-auto"
      >
        <span className={`transition-transform duration-150 ${showAdvanced ? 'rotate-90' : ''}`}>▶</span>
        Calibration details
      </button>

      {showAdvanced && (
        <div className="border-t border-slate-700/50 pt-3 space-y-1.5 text-xs text-slate-500">
          <div className="flex justify-between">
            <span>σ</span>
            <span className="font-mono text-slate-400">{meta.sigma}</span>
          </div>
          <div className="flex justify-between">
            <span>&alpha;<sub>T,A</sub></span>
            <span className="font-mono text-slate-400">{meta.alpha_T_A}</span>
          </div>
          <div className="flex justify-between">
            <span>&alpha;<sub>T,B</sub></span>
            <span className="font-mono text-slate-400">{meta.alpha_T_B}</span>
          </div>
          <div className="flex justify-between">
            <span>&alpha;<sub>T,C</sub></span>
            <span className="font-mono text-slate-400">{meta.alpha_T_C}</span>
          </div>
          <div className="flex justify-between">
            <span>L<sub>C</sub> / L<sub>A</sub></span>
            <span className="font-mono text-slate-400">{meta.L_C?.toFixed(3)}</span>
          </div>
          <p className="text-slate-600 leading-relaxed pt-1">{meta.sigma_note}</p>
        </div>
      )}
    </div>
  )
}
