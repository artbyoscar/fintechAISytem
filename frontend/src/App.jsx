import { useState, useEffect } from 'react'
import { analyzeCompany, checkHealth, getRecentAnalyses } from './api'

function App() {
  const [darkMode, setDarkMode] = useState(true)
  const [ticker, setTicker] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [apiStatus, setApiStatus] = useState('checking')
  const [recentAnalyses, setRecentAnalyses] = useState([])

  // Check API health on mount
  useEffect(() => {
    checkApiHealth()
    loadRecentAnalyses()
  }, [])

  const checkApiHealth = async () => {
    try {
      const response = await checkHealth()
      if (response.success) {
        setApiStatus('online')
      }
    } catch (err) {
      setApiStatus('offline')
      console.error('API health check failed:', err)
    }
  }

  const loadRecentAnalyses = async () => {
    try {
      const response = await getRecentAnalyses(5)
      if (response.success) {
        setRecentAnalyses(response.data.analyses)
      }
    } catch (err) {
      console.error('Failed to load recent analyses:', err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!ticker.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await analyzeCompany(ticker.toUpperCase())
      if (response.success) {
        setResult(response.data)
        loadRecentAnalyses() // Refresh recent list
      } else {
        setError(response.error || 'Analysis failed')
      }
    } catch (err) {
      setError(err.message || 'Failed to analyze company')
    } finally {
      setLoading(false)
    }
  }

  const getSentimentColor = (label) => {
    const labelLower = label?.toLowerCase()
    if (labelLower === 'positive' || labelLower === 'bullish') return 'status-bullish'
    if (labelLower === 'negative' || labelLower === 'bearish') return 'status-bearish'
    return 'status-neutral'
  }

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

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-terminal-bg">
        {/* Header */}
        <header className="border-b border-terminal-border bg-terminal-bg-light">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="text-2xl font-bold text-terminal-orange">
                  MAEI
                </div>
                <div className="text-terminal-text-dim text-sm">
                  Macro-Aware Earnings Intelligence
                </div>
              </div>

              <div className="flex items-center gap-6">
                {/* API Status Indicator */}
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${
                    apiStatus === 'online' ? 'bg-terminal-green-light animate-pulse-slow' :
                    apiStatus === 'offline' ? 'bg-terminal-red-light' :
                    'bg-terminal-yellow-light animate-pulse'
                  }`} />
                  <span className="text-xs text-terminal-text-dim">
                    {apiStatus === 'online' ? 'API ONLINE' :
                     apiStatus === 'offline' ? 'API OFFLINE' :
                     'CHECKING...'}
                  </span>
                </div>

                {/* Dark Mode Toggle */}
                <button
                  onClick={() => setDarkMode(!darkMode)}
                  className="p-2 rounded-md hover:bg-terminal-border transition-colors"
                  title="Toggle theme"
                >
                  {darkMode ? (
                    <svg className="w-5 h-5 text-terminal-yellow" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5 text-terminal-blue" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                    </svg>
                  )}
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="container mx-auto px-6 py-8">
          {/* Search Section */}
          <div className="card mb-8 animate-fade-in">
            <h2 className="text-xl font-semibold mb-4 text-terminal-orange">
              Analyze Earnings Call
            </h2>
            <form onSubmit={handleSubmit} className="flex gap-4">
              <input
                type="text"
                value={ticker}
                onChange={(e) => setTicker(e.target.value.toUpperCase())}
                placeholder="Enter ticker symbol (e.g., AAPL, MSFT, NVDA)"
                className="input-field flex-1 text-lg"
                disabled={loading || apiStatus === 'offline'}
                maxLength={10}
              />
              <button
                type="submit"
                disabled={loading || !ticker.trim() || apiStatus === 'offline'}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed min-w-[140px]"
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Analyzing...
                  </span>
                ) : (
                  'Analyze'
                )}
              </button>
            </form>

            {apiStatus === 'offline' && (
              <div className="mt-4 p-4 bg-terminal-red bg-opacity-10 border border-terminal-red rounded-md">
                <p className="text-terminal-red text-sm">
                  Cannot connect to API backend. Please ensure the backend server is running at http://localhost:8000
                </p>
              </div>
            )}
          </div>

          {/* Error Display */}
          {error && (
            <div className="card mb-8 border-terminal-red bg-terminal-red bg-opacity-5 animate-fade-in">
              <div className="flex items-start gap-3">
                <svg className="w-6 h-6 text-terminal-red flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <div>
                  <h3 className="text-terminal-red font-semibold mb-1">Error</h3>
                  <p className="text-terminal-text-dim text-sm">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Results Display */}
          {result && (
            <div className="space-y-6 animate-fade-in">
              {/* Company Overview */}
              <div className="card">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h2 className="text-2xl font-bold text-terminal-orange mb-1">
                      {result.ticker}
                    </h2>
                    <p className="text-terminal-text-dim text-sm">
                      Analysis completed at {new Date(result.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-terminal-text-dim mb-1">Processing Time</p>
                    <p className="text-lg font-semibold text-terminal-orange">
                      {result.performance?.total_time?.toFixed(2)}s
                    </p>
                  </div>
                </div>
              </div>

              {/* Sentiment Analysis */}
              {result.sentiment && (
                <div className="card">
                  <h3 className="text-lg font-semibold mb-4 text-terminal-text">
                    Sentiment Analysis
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                      <p className="text-xs text-terminal-text-dim mb-2">Sentiment Label</p>
                      <p className={`text-2xl font-bold ${getSentimentColor(result.sentiment.sentiment_label)}`}>
                        {result.sentiment.sentiment_label?.toUpperCase()}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-terminal-text-dim mb-2">Confidence Score</p>
                      <p className="text-2xl font-bold text-terminal-orange">
                        {(result.sentiment.sentiment_score * 100).toFixed(1)}%
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-terminal-text-dim mb-2">Sentiment Confidence</p>
                      <p className="text-2xl font-bold text-terminal-blue-light">
                        {(result.sentiment.confidence * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>

                  {/* Sentiment Scores Breakdown */}
                  {result.sentiment.scores && (
                    <div className="mt-6 pt-6 border-t border-terminal-border">
                      <p className="text-xs text-terminal-text-dim mb-3">Detailed Scores</p>
                      <div className="space-y-2">
                        {Object.entries(result.sentiment.scores).map(([label, score]) => (
                          <div key={label} className="flex items-center gap-3">
                            <span className="text-sm w-20 text-terminal-text-dim capitalize">{label}</span>
                            <div className="flex-1 h-2 bg-terminal-border rounded-full overflow-hidden">
                              <div
                                className={`h-full ${getSentimentColor(label)} bg-current transition-all duration-300`}
                                style={{ width: `${score * 100}%` }}
                              />
                            </div>
                            <span className="text-sm w-12 text-right text-terminal-text">
                              {(score * 100).toFixed(1)}%
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Macro Regime */}
              {result.macro && (
                <div className="card">
                  <h3 className="text-lg font-semibold mb-4 text-terminal-text">
                    Macro Regime Analysis
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <p className="text-xs text-terminal-text-dim mb-2">Current Regime</p>
                      <p className={`text-2xl font-bold ${getRegimeColor(result.macro.regime)}`}>
                        {result.macro.regime}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-terminal-text-dim mb-2">Trading Recommendation</p>
                      <p className={`text-2xl font-bold ${getRecommendationColor(result.macro.recommendation)}`}>
                        {result.macro.recommendation}
                      </p>
                    </div>
                  </div>

                  {/* Macro Indicators */}
                  {result.macro.indicators && (
                    <div className="mt-6 pt-6 border-t border-terminal-border">
                      <p className="text-xs text-terminal-text-dim mb-3">Market Indicators</p>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {Object.entries(result.macro.indicators).map(([key, value]) => (
                          <div key={key}>
                            <p className="text-xs text-terminal-text-dim mb-1 capitalize">
                              {key.replace(/_/g, ' ')}
                            </p>
                            <p className="text-lg font-semibold text-terminal-text">
                              {typeof value === 'number' ? value.toFixed(2) : value}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Trading Recommendation */}
              {result.recommendation && (
                <div className="card border-terminal-orange bg-terminal-orange bg-opacity-5">
                  <h3 className="text-lg font-semibold mb-3 text-terminal-orange">
                    Trading Recommendation
                  </h3>
                  <p className="text-terminal-text leading-relaxed">
                    {result.recommendation}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Recent Analyses */}
          {recentAnalyses.length > 0 && !result && (
            <div className="card animate-fade-in">
              <h3 className="text-lg font-semibold mb-4 text-terminal-text">
                Recent Analyses
              </h3>
              <div className="space-y-3">
                {recentAnalyses.map((analysis, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-3 bg-terminal-bg rounded-md hover:bg-terminal-border transition-colors cursor-pointer"
                    onClick={() => setTicker(analysis.ticker)}
                  >
                    <div className="flex items-center gap-4">
                      <span className="text-lg font-bold text-terminal-orange w-16">
                        {analysis.ticker}
                      </span>
                      <span className={`text-sm font-semibold ${getSentimentColor(analysis.sentiment_label)}`}>
                        {analysis.sentiment_label?.toUpperCase()}
                      </span>
                      <span className="text-xs text-terminal-text-dim">
                        {new Date(analysis.timestamp).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="text-xs text-terminal-text-dim">
                      Click to analyze
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Empty State */}
          {!result && !error && !loading && recentAnalyses.length === 0 && (
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
          )}
        </main>

        {/* Footer */}
        <footer className="border-t border-terminal-border bg-terminal-bg-light mt-12">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between text-xs text-terminal-text-dim">
              <div>
                Fintech AI System - Powered by FinBERT & Real-time Market Data
              </div>
              <div className="flex items-center gap-4">
                <span>Backend: FastAPI</span>
                <span>•</span>
                <span>Frontend: React + Vite</span>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}

export default App
