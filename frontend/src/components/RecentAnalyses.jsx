/**
 * RecentAnalyses Component
 * Table displaying recent analysis history
 */
export default function RecentAnalyses({ analyses, onTickerClick }) {
  if (!analyses || analyses.length === 0) {
    return (
      <div className="card text-center py-12 animate-fade-in">
        <svg className="w-16 h-16 mx-auto mb-4 text-terminal-text-dim" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
        <h3 className="text-xl font-semibold mb-2 text-terminal-text-dim">
          No analyses yet
        </h3>
        <p className="text-terminal-text-dim text-sm">
          Enter a ticker symbol above to analyze an earnings call
        </p>
      </div>
    )
  }

  const getSentimentColor = (label) => {
    const labelLower = label?.toLowerCase()
    if (labelLower === 'positive' || labelLower === 'bullish') return 'status-bullish'
    if (labelLower === 'negative' || labelLower === 'bearish') return 'status-bearish'
    return 'status-neutral'
  }

  const getSentimentIcon = (label) => {
    const labelLower = label?.toLowerCase()
    if (labelLower === 'positive' || labelLower === 'bullish') {
      return '📈'
    }
    if (labelLower === 'negative' || labelLower === 'bearish') {
      return '📉'
    }
    return '➖'
  }

  return (
    <div className="card animate-fade-in">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-terminal-text">
          Recent Analyses
        </h3>
        <span className="text-xs text-terminal-text-dim">
          Last {analyses.length} results
        </span>
      </div>

      {/* Desktop Table View */}
      <div className="hidden md:block overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-terminal-border text-xs text-terminal-text-dim">
              <th className="text-left py-3 px-4">Ticker</th>
              <th className="text-left py-3 px-4">Sentiment</th>
              <th className="text-left py-3 px-4">Score</th>
              <th className="text-left py-3 px-4">Regime</th>
              <th className="text-left py-3 px-4">Recommendation</th>
              <th className="text-left py-3 px-4">Date</th>
              <th className="text-right py-3 px-4">Action</th>
            </tr>
          </thead>
          <tbody>
            {analyses.map((analysis, idx) => (
              <tr
                key={idx}
                className="border-b border-terminal-border hover:bg-terminal-border transition-colors group"
              >
                <td className="py-3 px-4">
                  <div className="flex items-center gap-2">
                    <span className="text-lg font-bold text-terminal-orange font-mono">
                      {analysis.ticker}
                    </span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-center gap-2">
                    <span>{getSentimentIcon(analysis.sentiment_label)}</span>
                    <span className={`font-semibold text-sm ${getSentimentColor(analysis.sentiment_label)}`}>
                      {analysis.sentiment_label?.toUpperCase()}
                    </span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <span className="font-mono text-sm text-terminal-text">
                    {analysis.sentiment_score ? `${(analysis.sentiment_score * 100).toFixed(0)}%` : 'N/A'}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <span className={`text-sm font-semibold ${
                    analysis.macro_regime === 'BULL' ? 'text-terminal-green' :
                    analysis.macro_regime === 'BEAR' ? 'text-terminal-red' :
                    'text-terminal-yellow'
                  }`}>
                    {analysis.macro_regime || 'N/A'}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <span className={`text-sm ${
                    analysis.recommendation?.includes('FAVORABLE') ? 'text-terminal-green' :
                    analysis.recommendation?.includes('AVOID') ? 'text-terminal-red' :
                    'text-terminal-yellow'
                  }`}>
                    {analysis.recommendation || 'N/A'}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <span className="text-xs text-terminal-text-dim">
                    {new Date(analysis.timestamp).toLocaleDateString()}
                  </span>
                </td>
                <td className="py-3 px-4 text-right">
                  <button
                    onClick={() => onTickerClick && onTickerClick(analysis.ticker)}
                    className="text-xs text-terminal-orange hover:text-terminal-orange-light transition-colors opacity-0 group-hover:opacity-100"
                  >
                    Re-analyze →
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile Card View */}
      <div className="md:hidden space-y-3">
        {analyses.map((analysis, idx) => (
          <div
            key={idx}
            className="p-4 bg-terminal-bg rounded-md border border-terminal-border hover:border-terminal-orange transition-colors cursor-pointer"
            onClick={() => onTickerClick && onTickerClick(analysis.ticker)}
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <span className="text-xl font-bold text-terminal-orange font-mono">
                  {analysis.ticker}
                </span>
                <span>{getSentimentIcon(analysis.sentiment_label)}</span>
              </div>
              <span className="text-xs text-terminal-text-dim">
                {new Date(analysis.timestamp).toLocaleDateString()}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <p className="text-xs text-terminal-text-dim mb-1">Sentiment</p>
                <p className={`font-semibold ${getSentimentColor(analysis.sentiment_label)}`}>
                  {analysis.sentiment_label?.toUpperCase()}
                </p>
              </div>
              <div>
                <p className="text-xs text-terminal-text-dim mb-1">Regime</p>
                <p className={`font-semibold ${
                  analysis.macro_regime === 'BULL' ? 'text-terminal-green' :
                  analysis.macro_regime === 'BEAR' ? 'text-terminal-red' :
                  'text-terminal-yellow'
                }`}>
                  {analysis.macro_regime || 'N/A'}
                </p>
              </div>
            </div>

            <div className="mt-3 pt-3 border-t border-terminal-border">
              <p className="text-xs text-terminal-orange">
                Tap to re-analyze →
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
