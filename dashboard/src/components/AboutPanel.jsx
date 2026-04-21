export default function AboutPanel() {
  return (
    <div className="max-w-3xl mx-auto py-6 space-y-8">

      {/* Paper header */}
      <div className="panel p-6 space-y-4">
        <div>
          <div className="label mb-3">Working Paper</div>
          <h2 className="text-xl font-semibold text-slate-100 leading-snug">
            Trade Tariffs and Exchange Rates
            <span className="block text-base font-medium text-slate-300 mt-1">
              Revisiting Conventional Wisdom in a Three-Country Framework
            </span>
          </h2>
        </div>

        <div className="border-t border-slate-800 pt-4 space-y-1.5">
          <div className="text-sm text-slate-300">
            Jason Lu &amp; Dimitre Milkov
          </div>
          <div className="text-xs text-slate-500">
            International Monetary Fund, Research Department
          </div>
          <div className="inline-flex items-center gap-1.5 mt-2 px-2.5 py-1 rounded-md bg-indigo-950/60 border border-indigo-700/40 text-xs text-indigo-300 font-medium">
            Forthcoming IMF Working Paper
          </div>
        </div>
      </div>

      {/* Abstract */}
      <div className="panel p-6 space-y-3">
        <div className="label">Abstract</div>
        <p className="text-sm text-slate-300 leading-relaxed">
          An important feature of standard two-country trade models is the robust theoretical prediction
          that tariffs lead to an appreciation of the tariff-imposing country's currency. We show that
          this prediction is not robust when moving to the smallest multilateral setting with the
          introduction of a third country. When tariffs are applied selectively, imports can be diverted
          toward an untariffed supplier rather than toward domestic goods, generating opposing
          trade-diversion and trade-redirection forces whose relative strength depends on the elasticity
          of substitution across foreign suppliers. As a result, the exchange-rate response to selective
          tariffs becomes ambiguous and the tariff-imposing country's currency may depreciate against
          untariffed trading partners even as it appreciates against the tariffed one. In a bilateral
          trade war, where two countries impose tariffs on one another while a third country remains
          untaxed, the ambiguity is resolved: both tariff-imposing countries' currencies depreciate
          unambiguously against the third country. We calibrate the model to the 2025 US&#8209;China
          tariff episode and show that it correctly predicts the direction of dollar depreciation against
          third-country currencies during the peak escalation period, consistent with the bilateral trade
          war mechanism.
        </p>
      </div>

      {/* Dashboard note */}
      <div className="card p-5">
        <p className="text-xs text-slate-500 leading-relaxed">
          This dashboard is a companion to the working paper. It allows readers to explore the model's
          exchange rate predictions interactively across tariff scenarios and country configurations.
        </p>
      </div>

    </div>
  )
}
