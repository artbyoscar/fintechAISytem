/**
 * SentimentCardCompact Component
 * Compact sidebar version for the new layout
 */
export default function SentimentCardCompact({ sentiment }) {
  if (!sentiment) return null

  const getSentimentColor = (label) => {
    const labelLower = label?.toLowerCase()
    if (labelLower === 'positive' || labelLower === 'bullish') return 'text-fintech-green'
    if (labelLower === 'negative' || labelLower === 'bearish') return 'text-fintech-red'
    return 'text-fintech-orange'
  }

  const getSentimentIcon = (label) => {
    const labelLower = label?.toLowerCase()
    if (labelLower === 'positive' || labelLower === 'bullish') {
      return '↑'
    }
    if (labelLower === 'negative' || labelLower === 'bearish') {
      return '↓'
    }
    return '→'
  }

  return (
    <div className="bg-fintech-card border border-fintech-border rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide">
          Sentiment
        </h3>
        <span className={`text-2xl ${getSentimentColor(sentiment.overall_label)}`}>
          {getSentimentIcon(sentiment.overall_label)}
        </span>
      </div>

      {/* Main Sentiment */}
      <div className="mb-4">
        <p className={`text-2xl font-bold ${getSentimentColor(sentiment.overall_label)} mb-1`}>
          {sentiment.overall_label?.toUpperCase()}
        </p>
        <p className="text-xs text-gray-500">
          {(sentiment.confidence * 100).toFixed(0)}% confidence
        </p>
      </div>

      {/* Sentiment Score Gauge */}
      <div className="mb-4">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>Bearish</span>
          <span>Bullish</span>
        </div>
        <div className="relative h-2 bg-fintech-bg rounded-full overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-fintech-red via-gray-600 to-fintech-green opacity-30" />
          <div
            className="absolute top-0 bottom-0 w-1 bg-white shadow-lg"
            style={{ left: `${((sentiment.sentiment_score + 1) / 2) * 100}%` }}
          />
        </div>
        <div className="flex justify-between text-xs text-gray-600 mt-1">
          <span>-1.0</span>
          <span className="font-mono text-fintech-orange">
            {sentiment.sentiment_score.toFixed(2)}
          </span>
          <span>+1.0</span>
        </div>
      </div>

      {/* Detailed Scores */}
      {sentiment.scores && (
        <div className="space-y-2">
          {Object.entries(sentiment.scores).slice(0, 3).map(([label, score]) => (
            <div key={label} className="flex items-center justify-between text-xs">
              <span className="text-gray-500 capitalize">{label}</span>
              <div className="flex items-center gap-2">
                <div className="w-16 h-1.5 bg-fintech-bg rounded-full overflow-hidden">
                  <div
                    className={`h-full ${getSentimentColor(label)} bg-current`}
                    style={{ width: `${score * 100}%` }}
                  />
                </div>
                <span className="text-gray-400 font-mono w-10 text-right">
                  {(score * 100).toFixed(0)}%
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
