import { useState, useEffect } from 'react'
import { analyzeCompany, checkHealth, getRecentAnalyses } from './api'
import TickerSearch from './components/TickerSearch'
import AnalysisResults from './components/AnalysisResults'
import RecentAnalyses from './components/RecentAnalyses'

function App() {
  const [darkMode, setDarkMode] = useState(true)
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
      const response = await getRecentAnalyses(10)
      if (response.success) {
        setRecentAnalyses(response.data.analyses)
      }
    } catch (err) {
      console.error('Failed to load recent analyses:', err)
    }
  }

  const handleAnalyze = async (ticker) => {
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

  const handleTickerClick = (ticker) => {
    handleAnalyze(ticker)
  }

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-terminal-bg">
        {/* Header */}
        <header className="border-b border-terminal-border bg-terminal-bg-light sticky top-0 z-50">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="text-2xl font-bold text-terminal-orange">
                  MAEI
                </div>
                <div className="hidden sm:block text-terminal-text-dim text-sm">
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
                  <span className="text-xs text-terminal-text-dim hidden sm:inline">
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
          <TickerSearch
            onAnalyze={handleAnalyze}
            loading={loading}
            disabled={apiStatus === 'offline'}
          />

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
          {result && <AnalysisResults result={result} />}

          {/* Recent Analyses (shown when no active result) */}
          {!result && !error && !loading && (
            <RecentAnalyses
              analyses={recentAnalyses}
              onTickerClick={handleTickerClick}
            />
          )}
        </main>

        {/* Footer */}
        <footer className="border-t border-terminal-border bg-terminal-bg-light mt-12">
          <div className="container mx-auto px-6 py-4">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-terminal-text-dim">
              <div>
                Fintech AI System - Powered by FinBERT & Real-time Market Data
              </div>
              <div className="flex items-center gap-4">
                <span>Backend: FastAPI</span>
                <span className="hidden sm:inline">•</span>
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
