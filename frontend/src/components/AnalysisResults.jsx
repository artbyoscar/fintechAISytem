import SentimentCard from './SentimentCard'
import MacroRegimeCard from './MacroRegimeCard'

/**
 * AnalysisResults Component
 * Main container for displaying full analysis results
 */
export default function AnalysisResults({ result }) {
  if (!result) return null

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Company Overview Header */}
      <div className="card">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-baseline gap-3 mb-2">
              <h2 className="text-3xl font-bold text-terminal-orange">
                {result.ticker}
              </h2>
              {result.company_name && (
                <span className="text-terminal-text-dim text-sm">
                  {result.company_name}
                </span>
              )}
            </div>
            <p className="text-terminal-text-dim text-sm">
              Analysis completed at {new Date(result.timestamp).toLocaleString()}
            </p>
          </div>

          {/* Performance Badge */}
          {result.performance?.total_time && (
            <div className="text-right">
              <p className="text-xs text-terminal-text-dim mb-1">Processing Time</p>
              <div className="flex items-center gap-2">
                <svg className="w-4 h-4 text-terminal-green" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                </svg>
                <p className="text-lg font-semibold text-terminal-orange">
                  {result.performance.total_time.toFixed(2)}s
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Quick Stats Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-terminal-border">
          <div>
            <p className="text-xs text-terminal-text-dim mb-1">Sentiment</p>
            <p className={`font-semibold ${
              result.sentiment?.sentiment_label?.toLowerCase() === 'positive' ? 'text-terminal-green' :
              result.sentiment?.sentiment_label?.toLowerCase() === 'negative' ? 'text-terminal-red' :
              'text-terminal-yellow'
            }`}>
              {result.sentiment?.sentiment_label?.toUpperCase() || 'N/A'}
            </p>
          </div>
          <div>
            <p className="text-xs text-terminal-text-dim mb-1">Macro Regime</p>
            <p className={`font-semibold ${
              result.macro?.regime === 'BULL' ? 'text-terminal-green' :
              result.macro?.regime === 'BEAR' ? 'text-terminal-red' :
              'text-terminal-yellow'
            }`}>
              {result.macro?.regime || 'N/A'}
            </p>
          </div>
          <div>
            <p className="text-xs text-terminal-text-dim mb-1">Recommendation</p>
            <p className={`font-semibold ${
              result.macro?.recommendation === 'FAVORABLE' ? 'text-terminal-green' :
              result.macro?.recommendation === 'AVOID' ? 'text-terminal-red' :
              'text-terminal-yellow'
            }`}>
              {result.macro?.recommendation || 'N/A'}
            </p>
          </div>
          <div>
            <p className="text-xs text-terminal-text-dim mb-1">Confidence</p>
            <p className="font-semibold text-terminal-blue-light">
              {result.sentiment?.confidence ? `${(result.sentiment.confidence * 100).toFixed(0)}%` : 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Sentiment Analysis Card */}
      {result.sentiment && <SentimentCard sentiment={result.sentiment} />}

      {/* Macro Regime Card */}
      {result.macro && <MacroRegimeCard macro={result.macro} />}

      {/* Trading Recommendation */}
      {result.recommendation && (
        <div className="card border-terminal-orange bg-terminal-orange bg-opacity-5">
          <div className="flex items-start gap-3">
            <svg className="w-6 h-6 text-terminal-orange flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 3.5a1.5 1.5 0 013 0V4a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-.5a1.5 1.5 0 000 3h.5a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-.5a1.5 1.5 0 00-3 0v.5a1 1 0 01-1 1H6a1 1 0 01-1-1v-3a1 1 0 00-1-1h-.5a1.5 1.5 0 010-3H4a1 1 0 001-1V6a1 1 0 011-1h3a1 1 0 001-1v-.5z" />
            </svg>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-terminal-orange mb-2">
                Trading Recommendation
              </h3>
              <p className="text-terminal-text leading-relaxed">
                {result.recommendation}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Performance Breakdown */}
      {result.performance && (
        <div className="card">
          <h3 className="text-sm font-semibold text-terminal-text-dim mb-3">
            Performance Breakdown
          </h3>
          <div className="space-y-2">
            {Object.entries(result.performance)
              .filter(([key]) => key !== 'total_time')
              .map(([key, value]) => (
                <div key={key} className="flex items-center justify-between text-sm">
                  <span className="text-terminal-text-dim capitalize">
                    {key.replace(/_/g, ' ')}
                  </span>
                  <span className="font-mono text-terminal-text">
                    {typeof value === 'number' ? `${value.toFixed(2)}s` : value}
                  </span>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  )
}
