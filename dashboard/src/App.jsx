import { useState } from 'react'
import TheoryPanel from './components/TheoryPanel.jsx'
import CalibrationPanel from './components/CalibrationPanel.jsx'
import AboutPanel from './components/AboutPanel.jsx'

const TABS = [
  {
    id: 'theory',
    label: '3-Country Model',
    sub: 'Symmetric 3-country · Interactive grid',
  },
  {
    id: 'calibration',
    label: 'Calibrated Examples',
    sub: 'US–China–C · Data-matched parameters',
  },
  {
    id: 'about',
    label: 'About',
    sub: 'Paper · Authors · Abstract',
  },
]

export default function App() {
  const [activeTab, setActiveTab] = useState('theory')

  return (
    <div className="min-h-screen flex flex-col">

      {/* Header */}
      <header className="border-b border-slate-800 px-4 sm:px-6 py-3 sm:py-4">
        <div className="max-w-screen-2xl mx-auto flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 sm:gap-6">
          <div>
            <h1 className="text-base font-semibold text-slate-100 leading-tight">
              Trade Tariffs &amp; Exchange Rates
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">
              Lu &amp; Milkov (2026) · Three-Country Model Dashboard
            </p>
          </div>
          {/* Tabs */}
          <nav className="grid grid-cols-3 gap-1.5 sm:flex sm:flex-wrap">
            {TABS.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`tab-btn text-center sm:text-left px-2 py-2 text-xs sm:px-5 sm:py-2.5 sm:text-sm leading-tight ${activeTab === tab.id ? 'tab-btn-active' : 'tab-btn-inactive'}`}
              >
                <div>{tab.label}</div>
                <div className={`text-xs mt-0.5 font-normal hidden sm:block ${
                  activeTab === tab.id ? 'text-indigo-300' : 'text-slate-600'
                }`}>{tab.sub}</div>
              </button>
            ))}
          </nav>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 px-4 sm:px-6 py-4 sm:py-5 lg:overflow-hidden">
        <div className="max-w-screen-2xl mx-auto lg:h-full">
          {activeTab === 'theory'      && <TheoryPanel />}
          {activeTab === 'calibration' && <CalibrationPanel />}
          {activeTab === 'about'       && <AboutPanel />}
        </div>
      </main>

    </div>
  )
}
