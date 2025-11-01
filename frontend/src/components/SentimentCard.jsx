/**
 * SentimentCard Component
 * Displays sentiment analysis results with color-coded indicators
 */
export default function SentimentCard({ sentiment }) {
  if (!sentiment) return null

  const getSentimentColor = (label) => {
    const labelLower = label?.toLowerCase()
    if (labelLower === 'positive' || labelLower === 'bullish') return 'status-bullish'
    if (labelLower === 'negative' || labelLower === 'bearish') return 'status-bearish'
    return 'status-neutral'
  }

  const getSentimentIcon = (label) => {
    const labelLower = label?.toLowerCase()
    if (labelLower === 'positive' || labelLower === 'bullish') {
      return (
        <svg className="w-8 h-8 text-terminal-green-light" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
        </svg>
      )
    }
    if (labelLower === 'negative' || labelLower === 'bearish') {
      return (
        <svg className="w-8 h-8 text-terminal-red-light" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3.586L7.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 10.586V7z" clipRule="evenodd" />
        </svg>
      )
    }
    return (
      <svg className="w-8 h-8 text-terminal-yellow-light" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 000 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
      </svg>
    )
  }

  return (
    <div className="card animate-fade-in">
      <div className="flex items-center gap-3 mb-4">
        {getSentimentIcon(sentiment.sentiment_label)}
        <h3 className="text-lg font-semibold text-terminal-text">
          Sentiment Analysis
        </h3>
      </div>

      {/* Main Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div>
          <p className="text-xs text-terminal-text-dim mb-2">Sentiment Label</p>
          <p className={`text-2xl font-bold ${getSentimentColor(sentiment.sentiment_label)}`}>
            {sentiment.sentiment_label?.toUpperCase()}
          </p>
        </div>
        <div>
          <p className="text-xs text-terminal-text-dim mb-2">Sentiment Score</p>
          <div className="flex items-baseline gap-2">
            <p className="text-2xl font-bold text-terminal-orange">
              {(sentiment.sentiment_score * 100).toFixed(1)}%
            </p>
            <p className="text-xs text-terminal-text-dim">
              {sentiment.sentiment_score > 0 ? 'bullish' : sentiment.sentiment_score < 0 ? 'bearish' : 'neutral'}
            </p>
          </div>
        </div>
        <div>
          <p className="text-xs text-terminal-text-dim mb-2">Confidence</p>
          <div className="flex items-baseline gap-2">
            <p className="text-2xl font-bold text-terminal-blue-light">
              {(sentiment.confidence * 100).toFixed(1)}%
            </p>
            <p className="text-xs text-terminal-text-dim">
              {sentiment.confidence > 0.8 ? 'high' : sentiment.confidence > 0.6 ? 'medium' : 'low'}
            </p>
          </div>
        </div>
      </div>

      {/* Sentiment Score Gauge */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-xs text-terminal-text-dim mb-2">
          <span>Bearish</span>
          <span>Neutral</span>
          <span>Bullish</span>
        </div>
        <div className="relative h-3 bg-terminal-border rounded-full overflow-hidden">
          {/* Gradient background */}
          <div className="absolute inset-0 bg-gradient-to-r from-terminal-red via-terminal-yellow to-terminal-green opacity-30" />

          {/* Score indicator */}
          <div
            className="absolute top-0 bottom-0 w-1 bg-white shadow-lg transition-all duration-500"
            style={{ left: `${((sentiment.sentiment_score + 1) / 2) * 100}%` }}
          />
        </div>
        <div className="flex justify-between text-xs text-terminal-text-dim mt-1">
          <span>-1.0</span>
          <span>0</span>
          <span>+1.0</span>
        </div>
      </div>

      {/* Detailed Scores Breakdown */}
      {sentiment.scores && (
        <div className="pt-6 border-t border-terminal-border">
          <p className="text-xs text-terminal-text-dim mb-3">Detailed Score Distribution</p>
          <div className="space-y-3">
            {Object.entries(sentiment.scores).map(([label, score]) => (
              <div key={label} className="flex items-center gap-3">
                <span className="text-sm w-20 text-terminal-text-dim capitalize">{label}</span>
                <div className="flex-1 h-2 bg-terminal-border rounded-full overflow-hidden">
                  <div
                    className={`h-full ${getSentimentColor(label)} bg-current transition-all duration-500`}
                    style={{ width: `${score * 100}%` }}
                  />
                </div>
                <span className="text-sm w-14 text-right font-mono text-terminal-text">
                  {(score * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Quotes (if available) */}
      {sentiment.key_quotes && sentiment.key_quotes.length > 0 && (
        <div className="mt-6 pt-6 border-t border-terminal-border">
          <p className="text-xs text-terminal-text-dim mb-3">Key Quotes</p>
          <div className="space-y-2">
            {sentiment.key_quotes.slice(0, 3).map((quote, idx) => (
              <div key={idx} className="p-3 bg-terminal-bg rounded-md border-l-2 border-terminal-orange">
                <p className="text-sm text-terminal-text italic">"{quote.text}"</p>
                <p className={`text-xs mt-1 ${getSentimentColor(quote.sentiment)}`}>
                  {quote.sentiment?.toUpperCase()} ({(quote.confidence * 100).toFixed(0)}% confidence)
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
