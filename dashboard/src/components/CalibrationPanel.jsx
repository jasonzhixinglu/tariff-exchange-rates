import { useState, useEffect } from 'react'
import CountryCard from './CountryCard.jsx'

const REGIME_LABELS = {
  regime1: 'Regime 1 — Fentanyl tariffs (Feb–Mar 2025)',
  regime2: 'Regime 2 — Peak escalation (April 2025)',
}

const REGIME_DETAILS = {
  regime1: 'US tariff on China: +20%  ·  No retaliation  ·  No tariff on C',
  regime2: 'US tariff on China: +145%  ·  China retaliation: +125%  ·  Universal baseline on C: +10%',
}

export default function CalibrationPanel() {
  const [calibData, setCalibData] = useState(null)
  const [fxData, setFxData] = useState(null)
  const [activeRegime, setActiveRegime] = useState('regime2')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch('/data/calibration_panel.json').then(r => r.json()),
      fetch('/data/fx_data.json').then(r => r.json()),
    ]).then(([calib, fx]) => {
      setCalibData(calib)
      setFxData(fx.rates)
      setLoading(false)
    })
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-500">
        Loading calibration data…
      </div>
    )
  }

  const countries = calibData.countries
  const countryKeys = Object.keys(countries)

  return (
    <div className="flex flex-col gap-5">

      {/* Regime selector */}
      <div className="panel p-4 flex flex-col gap-2">
        <div className="flex items-center gap-3 flex-wrap">
          <span className="label">Tariff Regime</span>
          <div className="flex gap-2">
            {Object.keys(REGIME_LABELS).map(k => (
              <button key={k}
                onClick={() => setActiveRegime(k)}
                className={`regime-btn ${activeRegime === k ? 'regime-btn-active' : 'regime-btn-inactive'}`}
              >
                {k === 'regime1' ? 'Regime 1' : 'Regime 2'}
              </button>
            ))}
          </div>
          <span className="text-xs text-slate-500">{REGIME_DETAILS[activeRegime]}</span>
        </div>
        <p className="text-xs text-slate-600 leading-relaxed">
          Countries A = US, B = China. Tariffs are incremental above pre-2025 baseline.
          Model columns show % change relative to free-trade equilibrium.
          Data columns show log-point change relative to 2024 annual average (Yahoo Finance).
          Green data = direction agrees with model; red = disagrees.
        </p>
      </div>

      {/* Country grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {countryKeys.map(key => (
          <CountryCard
            key={key}
            countryKey={key}
            meta={countries[key].meta}
            regimes={countries[key].regimes}
            fxData={fxData}
            activeRegime={activeRegime}
          />
        ))}
      </div>

      {/* Data sources note */}
      <div className="panel p-4 text-xs text-slate-600 leading-relaxed grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-1">
        <div><span className="text-slate-500 font-medium">Labor endowments:</span> IMF WEO October 2024 (PPP GDP, US = 1)</div>
        <div><span className="text-slate-500 font-medium">Expenditure shares:</span> WTO Merchandise Trade Statistics 2024</div>
        <div><span className="text-slate-500 font-medium">Tariff rates:</span> USTR executive orders and Federal Register (2025)</div>
        <div><span className="text-slate-500 font-medium">Elasticities (σ):</span> Broda & Weinstein (2006); Feenstra et al. (2018)</div>
        <div><span className="text-slate-500 font-medium">FX data:</span> Yahoo Finance, monthly averages</div>
      </div>
    </div>
  )
}
