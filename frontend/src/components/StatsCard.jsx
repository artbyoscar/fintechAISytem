/**
 * StatsCard Component
 * Compact card displaying key metrics in sidebar
 * Modern Robinhood + Bloomberg hybrid design
 */
export default function StatsCard({ result }) {
  if (!result) return null

  const stats = [
    {
      label: 'Sentiment',
      value: result.sentiment_analysis?.overall_label?.toUpperCase() || 'N/A',
      type: result.sentiment_analysis?.overall_label?.toLowerCase(),
      detail: result.sentiment_analysis?.confidence
        ? `${(result.sentiment_analysis.confidence * 100).toFixed(0)}% confidence`
        : null
    },
    {
      label: 'Macro Regime',
      value: result.macro_regime?.regime || 'N/A',
      type: result.macro_regime?.regime === 'BULL' ? 'positive' :
            result.macro_regime?.regime === 'BEAR' ? 'negative' : 'neutral',
      detail: result.macro_regime?.confidence
        ? `${(result.macro_regime.confidence * 100).toFixed(0)}% confidence`
        : null
    },
    {
      label: 'Recommendation',
      value: result.recommendation?.action || 'N/A',
      type: result.recommendation?.action === 'FAVORABLE' ? 'positive' :
            result.recommendation?.action === 'AVOID' ? 'negative' : 'neutral',
      detail: result.recommendation?.risk_level
        ? `${result.recommendation.risk_level} risk`
        : null
    },
    {
      label: 'Analysis Time',
      value: result.performance?.total_time
        ? `${result.performance.total_time.toFixed(2)}s`
        : 'N/A',
      type: 'neutral',
      detail: result.analysis_timestamp
        ? new Date(result.analysis_timestamp).toLocaleTimeString()
        : null
    }
  ]

  const getValueColor = (type) => {
    switch(type) {
      case 'positive':
        return 'text-fintech-green'
      case 'negative':
        return 'text-fintech-red'
      default:
        return 'text-fintech-orange'
    }
  }

  return (
    <div className="bg-fintech-card border border-fintech-border rounded-lg p-4">
      <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-4">
        Quick Stats
      </h3>

      <div className="space-y-4">
        {stats.map((stat, idx) => (
          <div key={idx} className="border-b border-fintech-border last:border-b-0 pb-4 last:pb-0">
            <div className="flex items-baseline justify-between mb-1">
              <span className="text-xs text-gray-400 uppercase tracking-wide">
                {stat.label}
              </span>
            </div>
            <div className="flex items-baseline justify-between">
              <span className={`text-lg font-bold ${getValueColor(stat.type)}`}>
                {stat.value}
              </span>
            </div>
            {stat.detail && (
              <p className="text-xs text-gray-500 mt-1">
                {stat.detail}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
