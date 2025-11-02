import { useState } from 'react'

/**
 * TickerSearch Component
 * Search input for ticker symbols with autocomplete styling
 */
export default function TickerSearch({ onAnalyze, loading, disabled }) {
  const [ticker, setTicker] = useState('')
  const [suggestions] = useState([
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA', 'JPM', 'V', 'JNJ',
    'WMT', 'PG', 'MA', 'HD', 'DIS', 'BAC', 'NFLX', 'ADBE', 'CRM', 'ORCL'
  ])
  const [showSuggestions, setShowSuggestions] = useState(false)

  const filteredSuggestions = ticker
    ? suggestions.filter(s => s.toLowerCase().includes(ticker.toLowerCase()))
    : suggestions

  const handleSubmit = (e) => {
    e.preventDefault()
    if (ticker.trim() && !loading && !disabled) {
      onAnalyze(ticker.toUpperCase())
      setShowSuggestions(false)
    }
  }

  const handleTickerChange = (value) => {
    setTicker(value.toUpperCase())
    setShowSuggestions(true)
  }

  const selectSuggestion = (suggestion) => {
    setTicker(suggestion)
    setShowSuggestions(false)
    onAnalyze(suggestion)
  }

  return (
    <div className="card mb-8 animate-fade-in">
      <h2 className="text-xl font-semibold mb-4 text-terminal-orange">
        Analyze Earnings Call
      </h2>

      <form onSubmit={handleSubmit} className="relative">
        <div className="flex gap-4">
          <div className="flex-1 relative">
            <input
              type="text"
              value={ticker}
              onChange={(e) => handleTickerChange(e.target.value)}
              onFocus={() => setShowSuggestions(true)}
              onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
              placeholder="Enter ticker symbol (e.g., AAPL, MSFT, NVDA)"
              className="input-field w-full text-lg pr-10"
              disabled={loading || disabled}
              maxLength={10}
              autoComplete="off"
            />

            {/* Clear button - only show when there's text */}
            {ticker && (
              <button
                type="button"
                onClick={() => {
                  setTicker('')
                  setShowSuggestions(true)
                }}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                aria-label="Clear"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            )}

            {/* Autocomplete Suggestions */}
            {showSuggestions && filteredSuggestions.length > 0 && (
              <div className="absolute z-10 w-full mt-2 bg-terminal-bg-light border border-terminal-border rounded-md shadow-lg max-h-64 overflow-y-auto">
                <div className="p-2 text-xs text-terminal-text-dim border-b border-terminal-border">
                  Popular Tickers
                </div>
                <div className="grid grid-cols-5 gap-1 p-2">
                  {filteredSuggestions.slice(0, 20).map((suggestion) => (
                    <button
                      key={suggestion}
                      type="button"
                      onClick={() => selectSuggestion(suggestion)}
                      className="px-3 py-2 text-sm font-mono text-terminal-text hover:bg-terminal-border rounded transition-colors text-left"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={loading || !ticker.trim() || disabled}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed min-w-[140px]"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Analyzing...
              </span>
            ) : (
              'Analyze'
            )}
          </button>
        </div>

        {/* Helper Text */}
        <div className="mt-3 text-xs text-terminal-text-dim">
          Click a ticker above or type to search. Press Enter or click Analyze.
        </div>
      </form>

      {disabled && (
        <div className="mt-4 p-4 bg-terminal-red bg-opacity-10 border border-terminal-red rounded-md">
          <p className="text-terminal-red text-sm">
            Cannot connect to API backend. Please ensure the backend server is running at http://localhost:8000
          </p>
        </div>
      )}
    </div>
  )
}
