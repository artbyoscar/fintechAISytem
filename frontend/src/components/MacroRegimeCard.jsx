/**
 * MacroRegimeCard Component
 * Displays macro economic regime with visual indicators
 */
export default function MacroRegimeCard({ macro }) {
  if (!macro) return null

  const getRegimeColor = (regime) => {
    if (regime === 'BULL') return 'text-terminal-green-light'
    if (regime === 'BEAR') return 'text-terminal-red-light'
    return 'text-terminal-yellow-light'
  }

  const getRecommendationColor = (recommendation) => {
    if (recommendation === 'FAVORABLE') return 'text-terminal-green-light'
    if (recommendation === 'AVOID') return 'text-terminal-red-light'
    return 'text-terminal-yellow-light'
  }

  const getRegimeIcon = (regime) => {
    if (regime === 'BULL') {
      return (
        <svg className="w-8 h-8 text-terminal-green-light" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2L2 19h20L12 2zm0 4.84L18.16 17H5.84L12 6.84z"/>
        </svg>
      )
    }
    if (regime === 'BEAR') {
      return (
        <svg className="w-8 h-8 text-terminal-red-light" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 22L22 5H2l10 17zm0-4.84L5.84 7h12.32L12 17.16z"/>
        </svg>
      )
    }
    return (
      <svg className="w-8 h-8 text-terminal-yellow-light" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
      </svg>
    )
  }

  const getRegimeEmoji = (regime) => {
    if (regime === 'BULL') return '🐂'
    if (regime === 'BEAR') return '🐻'
    return '⚖️'
  }

  const getRecommendationIcon = (recommendation) => {
    if (recommendation === 'FAVORABLE') {
      return (
        <svg className="w-6 h-6 text-terminal-green-light" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
        </svg>
      )
    }
    if (recommendation === 'AVOID') {
      return (
        <svg className="w-6 h-6 text-terminal-red-light" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
        </svg>
      )
    }
    return (
      <svg className="w-6 h-6 text-terminal-yellow-light" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
      </svg>
    )
  }

  return (
    <div className="card animate-fade-in">
      <div className="flex items-center gap-3 mb-4">
        {getRegimeIcon(macro.regime)}
        <h3 className="text-lg font-semibold text-terminal-text">
          Macro Regime Analysis
        </h3>
      </div>

      {/* Main Regime Display */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <p className="text-xs text-terminal-text-dim mb-2">Current Regime</p>
          <div className="flex items-center gap-3">
            <span className="text-3xl">{getRegimeEmoji(macro.regime)}</span>
            <p className={`text-2xl font-bold ${getRegimeColor(macro.regime)}`}>
              {macro.regime}
            </p>
          </div>
          {macro.confidence && (
            <div className="mt-2">
              <div className="flex items-center justify-between text-xs text-terminal-text-dim mb-1">
                <span>Confidence</span>
                <span>{(macro.confidence * 100).toFixed(0)}%</span>
              </div>
              <div className="h-2 bg-terminal-border rounded-full overflow-hidden">
                <div
                  className={`h-full ${getRegimeColor(macro.regime)} bg-current transition-all duration-500`}
                  style={{ width: `${macro.confidence * 100}%` }}
                />
              </div>
            </div>
          )}
        </div>

        <div>
          <p className="text-xs text-terminal-text-dim mb-2">Trading Recommendation</p>
          <div className="flex items-center gap-2">
            {getRecommendationIcon(macro.recommendation)}
            <p className={`text-2xl font-bold ${getRecommendationColor(macro.recommendation)}`}>
              {macro.recommendation}
            </p>
          </div>
          {macro.risk_level && (
            <div className="mt-3 inline-flex items-center gap-2 px-3 py-1 bg-terminal-border rounded-full">
              <span className="text-xs text-terminal-text-dim">Risk Level:</span>
              <span className={`text-xs font-semibold ${
                macro.risk_level === 'LOW' ? 'text-terminal-green' :
                macro.risk_level === 'HIGH' ? 'text-terminal-red' :
                'text-terminal-yellow'
              }`}>
                {macro.risk_level}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Macro Indicators Grid */}
      {macro.indicators && (
        <div className="pt-6 border-t border-terminal-border">
          <p className="text-xs text-terminal-text-dim mb-4">Market Indicators</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(macro.indicators).map(([key, value]) => {
              const isGood = (key === 'vix' && value < 20) ||
                            (key === 'unemployment' && value < 4.5) ||
                            (key === 'inflation' && value < 3.5)

              return (
                <div key={key} className="bg-terminal-bg rounded-md p-3 border border-terminal-border">
                  <p className="text-xs text-terminal-text-dim mb-1 capitalize">
                    {key.replace(/_/g, ' ')}
                  </p>
                  <p className={`text-lg font-bold font-mono ${
                    isGood ? 'text-terminal-green' : 'text-terminal-yellow'
                  }`}>
                    {typeof value === 'number' ? value.toFixed(2) : value}
                    {key.includes('rate') || key.includes('inflation') || key.includes('unemployment') ? '%' : ''}
                  </p>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Regime Reasoning */}
      {macro.reasoning && (
        <div className="mt-6 pt-6 border-t border-terminal-border">
          <p className="text-xs text-terminal-text-dim mb-2">Analysis Reasoning</p>
          <p className="text-sm text-terminal-text leading-relaxed">
            {macro.reasoning}
          </p>
        </div>
      )}

      {/* Signal Breakdown */}
      {macro.signals && (
        <div className="mt-4 grid grid-cols-3 gap-3">
          <div className="text-center p-2 bg-terminal-bg rounded">
            <p className="text-xs text-terminal-text-dim mb-1">Bullish Signals</p>
            <p className="text-xl font-bold text-terminal-green">{macro.signals.bullish || 0}</p>
          </div>
          <div className="text-center p-2 bg-terminal-bg rounded">
            <p className="text-xs text-terminal-text-dim mb-1">Neutral Signals</p>
            <p className="text-xl font-bold text-terminal-yellow">{macro.signals.neutral || 0}</p>
          </div>
          <div className="text-center p-2 bg-terminal-bg rounded">
            <p className="text-xs text-terminal-text-dim mb-1">Bearish Signals</p>
            <p className="text-xl font-bold text-terminal-red">{macro.signals.bearish || 0}</p>
          </div>
        </div>
      )}
    </div>
  )
}
