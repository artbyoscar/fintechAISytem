import { useState, useEffect } from 'react'
import StatsCard from './StatsCard'
import SentimentCardCompact from './SentimentCardCompact'
import MacroRegimeCardCompact from './MacroRegimeCardCompact'
import StockChart from './StockChart'

// Safe number formatting helpers
const formatPrice = (value) => {
  const num = parseFloat(value)
  return !isNaN(num) ? num.toFixed(2) : '0.00'
}

const formatPercent = (value) => {
  const num = parseFloat(value)
  return !isNaN(num) ? num.toFixed(2) : '0.00'
}

/**
 * AnalysisResults Component - Modern Hybrid Design
 * Robinhood minimalism + Bloomberg Terminal information density
 * 70/30 split: Chart hero + Sidebar
 */
export default function AnalysisResultsNew({ result }) {
  const [currentPrice, setCurrentPrice] = useState(null)
  const [priceChange, setPriceChange] = useState(null)
  const [timeframeChange, setTimeframeChange] = useState({
    change: 0,
    changePercent: 0,
    timeframe: '3M'
  })

  if (!result) return null

  // Fetch real-time current price from Yahoo Finance on mount
  useEffect(() => {
    const fetchCurrentPrice = async () => {
      if (!result || !result.ticker) return

      try {
        const response = await fetch(
          `http://localhost:8000/current-price/${result.ticker}`
        )

        const responseData = await response.json()

        // Backend wraps response in {success: true, data: {...}}
        const data = responseData.data || responseData

        // Parse as numbers
        const price = parseFloat(data.price)
        const change = parseFloat(data.change || 0)
        const changePercent = parseFloat(data.change_percent || 0)

        if (isNaN(price)) {
          throw new Error('Invalid price')
        }

        console.log(`✅ Yahoo: $${price.toFixed(2)}`)

        setCurrentPrice(price)
        setPriceChange({
          amount: change,
          percent: changePercent
        })

      } catch (error) {
        console.error('Price error:', error)
      }
    }

    if (result?.ticker) {
      fetchCurrentPrice()
    }
  }, [result])

  // Callback to receive price data from StockChart
  // IMPORTANT: Only used as fallback if Yahoo Finance fails
  // Always use the most recent date's price, not the last item in the array
  const handlePriceUpdate = (priceData) => {
    // Only use chart data if Yahoo Finance price hasn't been set
    if (currentPrice === null && priceData && priceData.length > 0) {
      // Sort by date to ensure we always get the most recent price
      // regardless of which timeframe is selected
      const sortedData = [...priceData].sort((a, b) =>
        new Date(b.date) - new Date(a.date)
      )

      // Use the most recent date's price (index 0 after sorting descending)
      const mostRecent = sortedData[0]
      const previous = sortedData[1] || mostRecent

      console.log(`📊 Fallback to chart data: ${mostRecent.date} = $${mostRecent.close.toFixed(2)}`)

      setCurrentPrice(mostRecent.close)

      // Calculate change from previous trading day
      const change = mostRecent.close - previous.close
      const changePercent = (change / previous.close) * 100

      setPriceChange({
        amount: change,
        percent: changePercent
      })
    }
  }

  // Handler for timeframe-specific price changes from StockChart
  const handleTimeframeChange = (changeData) => {
    setTimeframeChange(changeData)
  }

  // Calculate price change based on available data
  const isPositive = priceChange ? priceChange.percent > 0 : (result.sentiment_analysis?.sentiment_score || 0) > 0

  return (
    <div className="min-h-screen bg-fintech-bg">
      {/* Header with Ticker Info */}
      <div className="bg-fintech-card border-b border-fintech-border sticky top-0 z-10">
        <div className="max-w-[1600px] mx-auto px-6 py-4">
          <div className="flex items-baseline justify-between">
            <div className="flex items-baseline gap-4">
              <h1 className="text-3xl font-bold text-white">
                {result.ticker}
              </h1>
              {result.company && (
                <span className="text-lg text-gray-400">
                  {result.company}
                </span>
              )}
            </div>

            {/* Price Display - Modern Hero Price with Gradient */}
            <div className="flex items-baseline gap-4">
              <div className="text-right">
                <div className="price-hero">
                  {currentPrice != null ? `$${formatPrice(currentPrice)}` : 'Loading...'}
                </div>

                {/* Timeframe-specific price change */}
                {timeframeChange && timeframeChange.change !== 0 && (
                  <div className="flex items-baseline gap-2 mt-1">
                    <span className={`text-lg font-bold ${timeframeChange.change >= 0 ? 'text-fintech-green' : 'text-fintech-red'}`}>
                      {timeframeChange.change >= 0 ? '+' : ''}${formatPrice(Math.abs(timeframeChange.change))}
                    </span>
                    <span className={`text-sm font-semibold ${timeframeChange.change >= 0 ? 'text-fintech-green' : 'text-fintech-red'}`}>
                      ({timeframeChange.change >= 0 ? '+' : ''}{formatPercent(timeframeChange.changePercent)}%)
                    </span>
                    <span className="text-xs text-gray-400 font-mono">
                      {timeframeChange.timeframe}
                    </span>
                  </div>
                )}

                {/* Fallback to daily price change if no timeframe data yet */}
                {(!timeframeChange || timeframeChange.change === 0) && priceChange && (
                  <div className={`text-sm font-semibold mt-1 ${priceChange.percent >= 0 ? 'text-fintech-green' : 'text-fintech-red'}`}>
                    {priceChange.percent >= 0 ? '+' : ''}${formatPrice(Math.abs(priceChange.amount))} ({priceChange.percent >= 0 ? '+' : ''}{formatPercent(priceChange.percent)}%)
                  </div>
                )}

                {!priceChange && !timeframeChange && currentPrice == null && (
                  <div className="text-xs text-gray-500 mt-1">
                    Fetching price...
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Quick Stats Bar */}
          <div className="flex items-center gap-6 mt-3 text-sm">
            <div className="flex items-center gap-2">
              <span className="text-gray-500">Sentiment:</span>
              <span className={`font-semibold ${
                result.sentiment_analysis?.overall_label?.toLowerCase() === 'positive' ? 'text-fintech-green' :
                result.sentiment_analysis?.overall_label?.toLowerCase() === 'negative' ? 'text-fintech-red' :
                'text-fintech-orange'
              }`}>
                {result.sentiment_analysis?.overall_label?.toUpperCase() || 'N/A'}
              </span>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-gray-500">Macro:</span>
              <span className={`font-semibold ${
                result.macro_regime?.regime === 'BULL' ? 'text-fintech-green' :
                result.macro_regime?.regime === 'BEAR' ? 'text-fintech-red' :
                'text-fintech-orange'
              }`}>
                {result.macro_regime?.regime || 'N/A'}
              </span>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-gray-500">Action:</span>
              <span className={`font-semibold ${
                result.recommendation?.action === 'FAVORABLE' ? 'text-fintech-green' :
                result.recommendation?.action === 'AVOID' ? 'text-fintech-red' :
                'text-fintech-orange'
              }`}>
                {result.recommendation?.action || 'N/A'}
              </span>
            </div>

            <div className="flex items-center gap-2 ml-auto">
              <span className="text-gray-500">Analyzed:</span>
              <span className="text-gray-400 font-mono text-xs">
                {result.analysis_timestamp ? new Date(result.analysis_timestamp).toLocaleString() : 'N/A'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content: 70/30 Split */}
      <div className="max-w-[1600px] mx-auto px-6 py-6">
        <div className="flex gap-6">
          {/* Left Column: Chart (70%) */}
          <div className="flex-[7] min-w-0">
            <StockChart
              ticker={result.ticker}
              onPriceUpdate={handlePriceUpdate}
              onTimeframeChange={handleTimeframeChange}
            />

            {/* Trading Recommendation Below Chart */}
            {result.recommendation && (
              <div className="mt-6 bg-fintech-card border border-fintech-orange/30 rounded-lg p-6">
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                      result.recommendation.action === 'FAVORABLE' ? 'bg-fintech-green/20' :
                      result.recommendation.action === 'AVOID' ? 'bg-fintech-red/20' :
                      'bg-fintech-orange/20'
                    }`}>
                      <span className="text-2xl">
                        {result.recommendation.action === 'FAVORABLE' ? '✓' :
                         result.recommendation.action === 'AVOID' ? '✗' : '!'}
                      </span>
                    </div>
                  </div>

                  <div className="flex-1">
                    <div className="flex items-baseline gap-3 mb-2">
                      <h3 className="text-xl font-bold text-fintech-orange">
                        Trading Recommendation
                      </h3>
                      <span className={`text-2xl font-bold ${
                        result.recommendation.action === 'FAVORABLE' ? 'text-fintech-green' :
                        result.recommendation.action === 'AVOID' ? 'text-fintech-red' :
                        'text-fintech-orange'
                      }`}>
                        {result.recommendation.action}
                      </span>
                      {result.recommendation.risk_level && (
                        <span className="text-sm px-3 py-1 bg-fintech-bg rounded-full text-gray-400">
                          {result.recommendation.risk_level} risk
                        </span>
                      )}
                    </div>

                    <p className="text-gray-300 leading-relaxed mb-4">
                      {result.recommendation.rationale || 'No rationale available'}
                    </p>

                    {result.recommendation.suggested_actions && result.recommendation.suggested_actions.length > 0 && (
                      <div className="mt-4">
                        <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Suggested Actions:</p>
                        <ul className="space-y-2">
                          {result.recommendation.suggested_actions.map((action, idx) => (
                            <li key={idx} className="flex items-start gap-3 text-sm text-gray-300">
                              <span className="text-fintech-orange mt-0.5">→</span>
                              <span>{action}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Performance Breakdown */}
            {result.performance?.timings && (
              <div className="mt-6 bg-fintech-card border border-fintech-border rounded-lg p-6">
                <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-4">
                  Performance Breakdown
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {Object.entries(result.performance.timings).map(([key, value]) => (
                    <div key={key} className="text-center">
                      <div className="text-xs text-gray-500 mb-1 capitalize">
                        {key.replace(/_/g, ' ')}
                      </div>
                      <div className="text-lg font-mono font-semibold text-fintech-orange">
                        {typeof value === 'number' ? `${value.toFixed(3)}s` : value}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right Column: Sidebar (30%) */}
          <div className="flex-[3] space-y-4">
            {/* Quick Stats */}
            <StatsCard result={result} />

            {/* Sentiment Analysis */}
            {result.sentiment_analysis && (
              <SentimentCardCompact sentiment={result.sentiment_analysis} />
            )}

            {/* Macro Regime */}
            {result.macro_regime && (
              <MacroRegimeCardCompact macro={result.macro_regime} />
            )}

            {/* Additional Info Card */}
            <div className="bg-fintech-card border border-fintech-border rounded-lg p-4">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
                About This Analysis
              </h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Data Source:</span>
                  <span className="text-gray-300">Earnings Transcript</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">AI Model:</span>
                  <span className="text-gray-300">FinBERT</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Total Time:</span>
                  <span className="text-fintech-orange font-mono">
                    {result.performance?.total_time?.toFixed(2) || 'N/A'}s
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
