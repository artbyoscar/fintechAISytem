import { useState } from 'react'
import AnalysisResultsNew from './components/AnalysisResultsNew'
import AnalysisResults from './components/AnalysisResults'

/**
 * Test page for comparing old vs new layouts
 * Use this to A/B test before deploying
 */
export default function TestNewLayout() {
  const [useNewLayout, setUseNewLayout] = useState(true)

  // Mock analysis result data
  const mockResult = {
    ticker: 'AAPL',
    company: 'Apple Inc.',
    analysis_timestamp: new Date().toISOString(),
    sentiment_analysis: {
      overall_label: 'Positive',
      confidence: 0.87,
      sentiment_score: 0.42,
      scores: {
        positive: 0.65,
        neutral: 0.25,
        negative: 0.10
      },
      key_quotes: [
        "Strong revenue growth in Services segment",
        "iPhone sales exceeded expectations",
        "Impressive margin expansion"
      ]
    },
    macro_regime: {
      regime: 'BULL',
      confidence: 0.78,
      indicators: {
        gdp_growth: 2.5,
        unemployment_rate: -0.3,
        inflation_rate: 1.2,
        interest_rates: 0.5,
        market_volatility: -1.5
      },
      recommendation: 'FAVORABLE'
    },
    recommendation: {
      action: 'FAVORABLE',
      risk_level: 'Medium',
      rationale: 'Strong fundamentals combined with positive market conditions suggest favorable entry point. The company demonstrates solid revenue growth and margin expansion, while macro indicators support risk-on positioning.',
      suggested_actions: [
        'Consider entry on pullbacks to support levels',
        'Monitor quarterly earnings for continued growth',
        'Set stop loss at 5-7% below entry',
        'Target 15-20% upside over 3-6 months'
      ]
    },
    performance: {
      total_time: 2.456,
      timings: {
        sentiment: 0.876,
        macro_regime: 0.654,
        recommendation: 0.432,
        total: 2.456
      }
    }
  }

  return (
    <div className="min-h-screen bg-terminal-bg">
      {/* Toggle Controls */}
      <div className="sticky top-0 z-50 bg-terminal-bg-light border-b border-terminal-border shadow-lg">
        <div className="max-w-[1600px] mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-white">
              Layout Comparison Test
            </h1>

            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-400">
                Current Layout:
              </span>
              <button
                onClick={() => setUseNewLayout(false)}
                className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                  !useNewLayout
                    ? 'bg-terminal-orange text-white'
                    : 'bg-terminal-bg-light text-gray-400 hover:text-white border border-terminal-border'
                }`}
              >
                Old Layout
              </button>
              <button
                onClick={() => setUseNewLayout(true)}
                className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                  useNewLayout
                    ? 'bg-terminal-orange text-white'
                    : 'bg-terminal-bg-light text-gray-400 hover:text-white border border-terminal-border'
                }`}
              >
                New Layout (70/30)
              </button>
            </div>
          </div>

          {/* Info Banner */}
          <div className="mt-3 p-3 bg-fintech-card border border-fintech-border rounded-lg">
            <div className="flex items-start gap-3">
              <span className="text-2xl">ℹ️</span>
              <div className="flex-1 text-sm">
                <p className="text-gray-300 mb-2">
                  <strong>Testing Mode:</strong> Compare old vs new layout with the same mock data
                </p>
                <div className="grid grid-cols-2 gap-4 text-xs text-gray-400">
                  <div>
                    <strong className="text-gray-300">Old Layout:</strong>
                    <ul className="mt-1 space-y-1 ml-4 list-disc">
                      <li>Stacked cards full width</li>
                      <li>Chart below sentiment</li>
                      <li>Traditional grid layout</li>
                    </ul>
                  </div>
                  <div>
                    <strong className="text-gray-300">New Layout:</strong>
                    <ul className="mt-1 space-y-1 ml-4 list-disc">
                      <li>70/30 chart-first split</li>
                      <li>Sticky header with quick stats</li>
                      <li>Compact sidebar cards</li>
                      <li>Modern fintech palette</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Render Selected Layout */}
      <div className="pt-6">
        {useNewLayout ? (
          <AnalysisResultsNew result={mockResult} />
        ) : (
          <AnalysisResults result={mockResult} />
        )}
      </div>

      {/* Comparison Notes */}
      <div className="max-w-[1600px] mx-auto px-6 py-12">
        <div className="bg-fintech-card border border-fintech-border rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-4">
            Comparison Notes
          </h2>

          <div className="grid md:grid-cols-2 gap-6 text-sm">
            <div>
              <h3 className="text-fintech-orange font-semibold mb-3">Old Layout Pros</h3>
              <ul className="space-y-2 text-gray-300">
                <li>✓ Familiar design</li>
                <li>✓ Full-width sentiment card shows all details</li>
                <li>✓ Simple single-column flow</li>
              </ul>

              <h3 className="text-fintech-red font-semibold mb-3 mt-4">Old Layout Cons</h3>
              <ul className="space-y-2 text-gray-300">
                <li>✗ Chart not prominent enough</li>
                <li>✗ Lots of scrolling required</li>
                <li>✗ Stats spread across top</li>
                <li>✗ Less efficient use of space</li>
              </ul>
            </div>

            <div>
              <h3 className="text-fintech-green font-semibold mb-3">New Layout Pros</h3>
              <ul className="space-y-2 text-gray-300">
                <li>✓ Chart is the hero (70% width)</li>
                <li>✓ Sticky header keeps context visible</li>
                <li>✓ Sidebar shows all key info at once</li>
                <li>✓ More professional/modern look</li>
                <li>✓ Better use of horizontal space</li>
                <li>✓ Compact cards reduce scrolling</li>
              </ul>

              <h3 className="text-fintech-orange font-semibold mb-3 mt-4">New Layout Cons</h3>
              <ul className="space-y-2 text-gray-300">
                <li>⚠ More complex layout (higher maintenance)</li>
                <li>⚠ Some sentiment details in compact view</li>
                <li>⚠ Requires wider screens for optimal view</li>
              </ul>
            </div>
          </div>

          <div className="mt-6 p-4 bg-terminal-bg rounded-lg border-l-4 border-fintech-green">
            <p className="text-sm text-gray-300">
              <strong className="text-fintech-green">Recommendation:</strong> The new layout provides a significantly better user experience for the target audience (traders/analysts) who typically use desktop screens and value chart prominence and information density. The 70/30 split with sticky header offers the best balance of chart focus and contextual information.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
