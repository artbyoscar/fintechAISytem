// Safe number formatting helper
const safeFormat = (val, decimals = 2) => {
  const num = parseFloat(val)
  return isNaN(num) ? '0.00' : num.toFixed(decimals)
}

/**
 * MacroRegimeCardCompact Component
 * Compact sidebar version for the new layout
 */
export default function MacroRegimeCardCompact({ macro }) {
  if (!macro) return null

  const getRegimeColor = (regime) => {
    if (regime === 'BULL') return 'text-fintech-green'
    if (regime === 'BEAR') return 'text-fintech-red'
    return 'text-fintech-orange'
  }

  const getRegimeEmoji = (regime) => {
    if (regime === 'BULL') return '🐂'
    if (regime === 'BEAR') return '🐻'
    return '⚖️'
  }

  const getRecommendationColor = (recommendation) => {
    if (recommendation === 'FAVORABLE') return 'text-fintech-green'
    if (recommendation === 'AVOID') return 'text-fintech-red'
    return 'text-fintech-orange'
  }

  return (
    <div className="bg-fintech-card border border-fintech-border rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide">
          Macro Regime
        </h3>
        <span className="text-2xl">
          {getRegimeEmoji(macro.regime)}
        </span>
      </div>

      {/* Main Regime */}
      <div className="mb-4">
        <p className={`text-2xl font-bold ${getRegimeColor(macro.regime)} mb-1`}>
          {macro.regime}
        </p>
        <p className="text-xs text-gray-500">
          {macro.confidence != null ? safeFormat(macro.confidence * 100, 0) : 'N/A'}% confidence
        </p>
      </div>

      {/* Indicators */}
      {macro.indicators && (
        <div className="space-y-2 mb-4">
          <p className="text-xs text-gray-500 uppercase tracking-wide">Key Indicators</p>
          {Object.entries(macro.indicators).slice(0, 3).map(([key, value]) => (
            <div key={key} className="flex items-center justify-between text-xs">
              <span className="text-gray-500 capitalize">{key.replace(/_/g, ' ')}</span>
              <span className={`font-mono font-semibold ${
                value > 0 ? 'text-fintech-green' : value < 0 ? 'text-fintech-red' : 'text-gray-400'
              }`}>
                {value != null ? `${value > 0 ? '+' : ''}${safeFormat(value)}%` : 'N/A'}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Recommendation */}
      {macro.recommendation && (
        <div className="pt-3 border-t border-fintech-border">
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-500 uppercase tracking-wide">Action</span>
            <span className={`text-sm font-bold ${getRecommendationColor(macro.recommendation)}`}>
              {macro.recommendation}
            </span>
          </div>
        </div>
      )}
    </div>
  )
}
