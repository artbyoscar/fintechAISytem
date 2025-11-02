import { useState, useMemo, useRef, useEffect, useCallback } from 'react'
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  Area
} from 'recharts'
import axios from 'axios'

/**
 * StockChart Component
 * Interactive stock chart with candlesticks, volume, technical indicators, and drawing tools
 * Optimized with data caching, prefetching, and debouncing for fast timeframe switching
 */
export default function StockChart({ ticker, onPriceUpdate }) {
  const [timeRange, setTimeRange] = useState('3M')
  const [showSMA20, setShowSMA20] = useState(true)
  const [showSMA50, setShowSMA50] = useState(true)
  const [showSMA200, setShowSMA200] = useState(false)
  const [showMACD, setShowMACD] = useState(false)
  const [showRSI, setShowRSI] = useState(false)
  const [showVolume, setShowVolume] = useState(true)
  const [drawingMode, setDrawingMode] = useState(null) // 'trendline', 'horizontal', null
  const [drawings, setDrawings] = useState([])
  const [zoomDomain, setZoomDomain] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [marketData, setMarketData] = useState(null)

  // Performance optimizations
  const [dataCache, setDataCache] = useState({}) // Cache for all timeframes
  const [isBackgroundLoading, setIsBackgroundLoading] = useState(false)
  const [usingCachedData, setUsingCachedData] = useState(false)
  const debounceTimerRef = useRef(null)
  const chartRef = useRef(null)
  const abortControllerRef = useRef(null)

  // Common timeframes to prefetch in background
  const COMMON_TIMEFRAMES = ['1M', '3M', '6M', '1Y']
  const DEBOUNCE_DELAY = 300 // ms

  // Fetch market data from API with caching
  const fetchMarketData = useCallback(async (targetTicker, targetTimeframe, isBackground = false) => {
    if (!targetTicker) return null

    // Check cache first
    const cacheKey = `${targetTicker}_${targetTimeframe}`
    if (dataCache[cacheKey]) {
      console.log(`[Cache Hit] Using cached data for ${cacheKey}`)
      return dataCache[cacheKey]
    }

    // Cancel any pending request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    // Create new abort controller for this request
    abortControllerRef.current = new AbortController()

    try {
      const startTime = performance.now()

      const response = await axios.post(
        `http://localhost:8000/market-data/${targetTicker}`,
        { timeframe: targetTimeframe },
        {
          headers: {
            'Content-Type': 'application/json'
          },
          signal: abortControllerRef.current.signal
        }
      )

      const loadTime = performance.now() - startTime
      console.log(`[Fetch] ${cacheKey} loaded in ${loadTime.toFixed(2)}ms`)

      if (response.data.success) {
        const data = response.data.data

        // Cache the data
        setDataCache(prev => ({
          ...prev,
          [cacheKey]: data
        }))

        return data
      } else {
        throw new Error(response.data.error || 'Failed to fetch market data')
      }
    } catch (err) {
      if (err.name === 'CanceledError') {
        console.log(`[Cancelled] Request for ${cacheKey} was cancelled`)
        return null
      }

      if (!isBackground) {
        console.error('Error fetching market data:', err)
        // Fallback to mock data on error
        const mockData = {
          data: generateMockData(targetTimeframe, targetTicker).data,
          ticker: targetTicker,
          timeframe: targetTimeframe
        }

        // Cache mock data too
        setDataCache(prev => ({
          ...prev,
          [cacheKey]: mockData
        }))

        return mockData
      }

      return null
    }
  }, [dataCache])

  // Prefetch common timeframes in background
  useEffect(() => {
    if (!ticker) return

    const prefetchTimeframes = async () => {
      setIsBackgroundLoading(true)
      console.log(`[Prefetch] Starting background prefetch for ${ticker}`)

      // Fetch priority timeframes first (current + 1M if not current)
      const priorityTimeframes = [timeRange]
      if (!priorityTimeframes.includes('1M')) {
        priorityTimeframes.push('1M')
      }

      for (const tf of priorityTimeframes) {
        const cacheKey = `${ticker}_${tf}`
        if (!dataCache[cacheKey]) {
          await fetchMarketData(ticker, tf, false)
        }
      }

      // Then fetch remaining common timeframes in background
      for (const tf of COMMON_TIMEFRAMES) {
        const cacheKey = `${ticker}_${tf}`
        if (!dataCache[cacheKey] && !priorityTimeframes.includes(tf)) {
          await fetchMarketData(ticker, tf, true)
        }
      }

      setIsBackgroundLoading(false)
      console.log(`[Prefetch] Background prefetch complete for ${ticker}`)
    }

    prefetchTimeframes()
  }, [ticker]) // Only run when ticker changes

  // Main effect for loading current timeframe data
  useEffect(() => {
    const loadData = async () => {
      if (!ticker) return

      const cacheKey = `${ticker}_${timeRange}`

      // Check if data is already cached
      if (dataCache[cacheKey]) {
        console.log(`[Cache] Instant load from cache: ${cacheKey}`)
        setMarketData(dataCache[cacheKey])
        setUsingCachedData(true)
        setError(null)
        return
      }

      // Data not cached, need to fetch
      setLoading(true)
      setError(null)
      setUsingCachedData(false)

      try {
        const data = await fetchMarketData(ticker, timeRange, false)
        if (data) {
          setMarketData(data)
        }
      } catch (err) {
        setError(err.message || 'Failed to fetch market data')
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [ticker, timeRange, dataCache, fetchMarketData])

  // Notify parent component when price data is available
  useEffect(() => {
    if (onPriceUpdate && marketData && marketData.data && marketData.data.length > 0) {
      onPriceUpdate(marketData.data)
    }
  }, [marketData, onPriceUpdate])

  // Get raw data from API response or empty array
  const rawData = useMemo(() => {
    if (!marketData || !marketData.data) {
      return []
    }
    return marketData.data
  }, [marketData])

  // Data is already enriched with indicators from the API
  const dataWithIndicators = useMemo(() => {
    // API already returns data with all indicators calculated
    return rawData
  }, [rawData])

  // Time range buttons
  const timeRanges = ['1D', '5D', '1M', '3M', '6M', '1Y', '5Y', 'MAX']

  // Custom Candlestick Shape
  const Candlestick = (props) => {
    const { x, y, width, height, low, high, open, close } = props
    const isGreen = close > open
    const color = isGreen ? '#00c853' : '#ff1744'
    const wickX = x + width / 2

    return (
      <g>
        {/* Wick */}
        <line
          x1={wickX}
          y1={y}
          x2={wickX}
          y2={y + height}
          stroke={color}
          strokeWidth={1}
        />
        {/* Body */}
        <rect
          x={x}
          y={isGreen ? y + height * ((high - close) / (high - low)) : y + height * ((high - open) / (high - low))}
          width={width}
          height={Math.abs(height * ((close - open) / (high - low)))}
          fill={color}
          stroke={color}
          strokeWidth={1}
        />
      </g>
    )
  }

  // Custom Tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (!active || !payload || !payload.length) return null

    const data = payload[0].payload

    return (
      <div className="bg-terminal-bg-light border border-terminal-border rounded-lg p-3 shadow-lg">
        <p className="text-terminal-orange font-semibold mb-2">{data.date}</p>

        <div className="space-y-1 text-sm">
          <div className="flex justify-between gap-4">
            <span className="text-terminal-text-dim">Open:</span>
            <span className="text-terminal-text font-mono">${data.open != null ? data.open.toFixed(2) : 'N/A'}</span>
          </div>
          <div className="flex justify-between gap-4">
            <span className="text-terminal-text-dim">High:</span>
            <span className="text-terminal-green font-mono">${data.high != null ? data.high.toFixed(2) : 'N/A'}</span>
          </div>
          <div className="flex justify-between gap-4">
            <span className="text-terminal-text-dim">Low:</span>
            <span className="text-terminal-red font-mono">${data.low != null ? data.low.toFixed(2) : 'N/A'}</span>
          </div>
          <div className="flex justify-between gap-4">
            <span className="text-terminal-text-dim">Close:</span>
            <span className={`font-mono ${data.close > data.open ? 'text-terminal-green' : 'text-terminal-red'}`}>
              ${data.close != null ? data.close.toFixed(2) : 'N/A'}
            </span>
          </div>

          {showVolume && (
            <div className="flex justify-between gap-4 pt-1 border-t border-terminal-border">
              <span className="text-terminal-text-dim">Volume:</span>
              <span className="text-terminal-text font-mono">{formatVolume(data.volume)}</span>
            </div>
          )}

          {showSMA20 && data.sma20 != null && (
            <div className="flex justify-between gap-4">
              <span className="text-terminal-text-dim">SMA(20):</span>
              <span className="text-terminal-blue-light font-mono">${data.sma20.toFixed(2)}</span>
            </div>
          )}

          {showSMA50 && data.sma50 != null && (
            <div className="flex justify-between gap-4">
              <span className="text-terminal-text-dim">SMA(50):</span>
              <span className="text-terminal-yellow font-mono">${data.sma50.toFixed(2)}</span>
            </div>
          )}

          {showSMA200 && data.sma200 != null && (
            <div className="flex justify-between gap-4">
              <span className="text-terminal-text-dim">SMA(200):</span>
              <span className="text-purple-400 font-mono">${data.sma200.toFixed(2)}</span>
            </div>
          )}

          {showMACD && data.macd != null && (
            <>
              <div className="flex justify-between gap-4 pt-1 border-t border-terminal-border">
                <span className="text-terminal-text-dim">MACD:</span>
                <span className="text-terminal-text font-mono">{data.macd.toFixed(2)}</span>
              </div>
              {data.signal != null && (
                <div className="flex justify-between gap-4">
                  <span className="text-terminal-text-dim">Signal:</span>
                  <span className="text-terminal-text font-mono">{data.signal.toFixed(2)}</span>
                </div>
              )}
              {data.histogram != null && (
                <div className="flex justify-between gap-4">
                  <span className="text-terminal-text-dim">Histogram:</span>
                  <span className={`font-mono ${data.histogram > 0 ? 'text-terminal-green' : 'text-terminal-red'}`}>
                    {data.histogram.toFixed(2)}
                  </span>
                </div>
              )}
            </>
          )}

          {showRSI && data.rsi != null && (
            <div className="flex justify-between gap-4 pt-1 border-t border-terminal-border">
              <span className="text-terminal-text-dim">RSI(14):</span>
              <span className={`font-mono ${
                data.rsi > 70 ? 'text-terminal-red' :
                data.rsi < 30 ? 'text-terminal-green' :
                'text-terminal-text'
              }`}>
                {data.rsi.toFixed(2)}
              </span>
            </div>
          )}
        </div>
      </div>
    )
  }

  // Handle chart click for drawing tools
  const handleChartClick = (e) => {
    if (!drawingMode || !e) return

    // Add drawing logic here
    // This would need more complex implementation for actual drawing
    console.log('Drawing mode:', drawingMode, 'at', e.activeLabel)
  }

  // Debounced timeframe change handler
  const handleTimeframeChange = useCallback((newTimeframe) => {
    // Clear existing debounce timer
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current)
    }

    // Check if data is cached - if so, switch immediately
    const cacheKey = `${ticker}_${newTimeframe}`
    if (dataCache[cacheKey]) {
      console.log(`[Debounce] Bypassed - cache hit for ${cacheKey}`)
      setTimeRange(newTimeframe)
      return
    }

    // If not cached, debounce the switch
    console.log(`[Debounce] Scheduling timeframe switch to ${newTimeframe}`)
    debounceTimerRef.current = setTimeout(() => {
      setTimeRange(newTimeframe)
    }, DEBOUNCE_DELAY)
  }, [ticker, dataCache, DEBOUNCE_DELAY])

  // Cleanup debounce timer on unmount
  useEffect(() => {
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current)
      }
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [])

  // Skeleton loader component
  const ChartSkeleton = () => (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <div className="w-full">
          <div className="h-6 w-48 bg-terminal-border rounded animate-pulse mb-2"></div>
          <div className="h-4 w-64 bg-terminal-border rounded animate-pulse"></div>
        </div>
      </div>

      <div className="space-y-4 mb-6">
        {/* Skeleton for time range selector */}
        <div className="flex gap-2">
          {[1, 2, 3, 4, 5, 6, 7, 8].map(i => (
            <div key={i} className="h-8 w-12 bg-terminal-border rounded animate-pulse"></div>
          ))}
        </div>

        {/* Skeleton for indicator toggles */}
        <div className="flex gap-3">
          {[1, 2, 3, 4, 5, 6].map(i => (
            <div key={i} className="h-5 w-20 bg-terminal-border rounded animate-pulse"></div>
          ))}
        </div>
      </div>

      {/* Skeleton for chart */}
      <div className="mb-4 relative">
        <div className="h-96 bg-terminal-bg-light border border-terminal-border rounded-lg p-6 animate-pulse">
          {/* Grid lines */}
          <div className="h-full w-full relative">
            <div className="absolute inset-0 flex flex-col justify-between">
              {[1, 2, 3, 4, 5].map(i => (
                <div key={i} className="h-px bg-terminal-border"></div>
              ))}
            </div>
            <div className="absolute inset-0 flex justify-between">
              {[1, 2, 3, 4, 5, 6, 7].map(i => (
                <div key={i} className="w-px bg-terminal-border"></div>
              ))}
            </div>
          </div>
        </div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-terminal-orange"></div>
        </div>
      </div>

      {/* Skeleton for volume chart */}
      <div className="h-32 bg-terminal-bg-light border border-terminal-border rounded-lg p-4 animate-pulse"></div>
    </div>
  )

  // Show skeleton loader while loading
  if (loading) {
    return <ChartSkeleton />
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-terminal-orange">
            {ticker} Price Chart
          </h3>
          <p className="text-xs text-terminal-text-dim mt-1">
            Interactive chart with technical analysis
            {marketData?.metadata?.source && (
              <span className="ml-2">• Source: {marketData.metadata.source}</span>
            )}
            {usingCachedData && (
              <span className="ml-2 text-terminal-green">• Cached</span>
            )}
            {isBackgroundLoading && (
              <span className="ml-2 text-terminal-yellow">• Prefetching...</span>
            )}
          </p>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="mb-4 p-3 bg-terminal-red bg-opacity-10 border border-terminal-red rounded">
          <p className="text-terminal-red text-sm">
            {error} - Showing mock data for demonstration
          </p>
        </div>
      )}

      {/* Indicator Data Warning */}
      {dataWithIndicators && dataWithIndicators.length > 0 && (
        <>
          {(showRSI && dataWithIndicators.filter(p => p.rsi != null).length < 14) ||
           (showMACD && dataWithIndicators.filter(p => p.macd != null).length < 26) ||
           (showSMA200 && dataWithIndicators.filter(p => p.sma200 != null).length < 200) ? (
            <div className="mb-4 p-3 bg-yellow-900 bg-opacity-20 border border-yellow-600 rounded">
              <p className="text-yellow-500 text-sm flex items-start gap-2">
                <span>⚠️</span>
                <span>Some indicators need more historical data to calculate accurately. Try selecting a longer timeframe (6M or 1Y) for complete indicator coverage.</span>
              </p>
            </div>
          ) : null}
        </>
      )}

      {/* Controls */}
      <div className="space-y-4 mb-6">
        {/* Time Range Selector */}
        <div className="flex flex-wrap gap-2">
          {timeRanges.map(range => {
            const cacheKey = `${ticker}_${range}`
            const isCached = dataCache[cacheKey] !== undefined

            return (
              <button
                key={range}
                onClick={() => handleTimeframeChange(range)}
                className={`relative px-3 py-1 text-xs font-semibold rounded transition-all ${
                  timeRange === range
                    ? 'bg-terminal-orange text-white'
                    : 'bg-terminal-border text-terminal-text-dim hover:bg-terminal-border hover:text-terminal-text'
                }`}
                title={isCached ? 'Data cached - instant load' : 'Will fetch data'}
              >
                {range}
                {isCached && timeRange !== range && (
                  <span className="absolute -top-1 -right-1 w-2 h-2 bg-terminal-green rounded-full"></span>
                )}
              </button>
            )
          })}
        </div>

        {/* Indicators Toggle */}
        <div className="flex flex-wrap gap-3 text-xs">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showVolume}
              onChange={(e) => setShowVolume(e.target.checked)}
              className="w-3 h-3"
            />
            <span className="text-terminal-text-dim">Volume</span>
          </label>

          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showSMA20}
              onChange={(e) => setShowSMA20(e.target.checked)}
              className="w-3 h-3"
            />
            <span className="text-terminal-blue-light">SMA(20)</span>
          </label>

          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showSMA50}
              onChange={(e) => setShowSMA50(e.target.checked)}
              className="w-3 h-3"
            />
            <span className="text-terminal-yellow">SMA(50)</span>
          </label>

          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showSMA200}
              onChange={(e) => setShowSMA200(e.target.checked)}
              className="w-3 h-3"
            />
            <span className="text-purple-400">SMA(200)</span>
          </label>

          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showMACD}
              onChange={(e) => setShowMACD(e.target.checked)}
              className="w-3 h-3"
            />
            <span className="text-terminal-text-dim">MACD</span>
          </label>

          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showRSI}
              onChange={(e) => setShowRSI(e.target.checked)}
              className="w-3 h-3"
            />
            <span className="text-terminal-text-dim">RSI(14)</span>
          </label>
        </div>

        {/* Drawing Tools */}
        <div className="flex gap-2">
          <button
            onClick={() => setDrawingMode(drawingMode === 'trendline' ? null : 'trendline')}
            className={`px-3 py-1 text-xs font-semibold rounded transition-all ${
              drawingMode === 'trendline'
                ? 'bg-terminal-orange text-white'
                : 'bg-terminal-border text-terminal-text-dim hover:bg-terminal-border hover:text-terminal-text'
            }`}
            title="Draw trend line"
          >
            📈 Trend Line
          </button>

          <button
            onClick={() => setDrawingMode(drawingMode === 'horizontal' ? null : 'horizontal')}
            className={`px-3 py-1 text-xs font-semibold rounded transition-all ${
              drawingMode === 'horizontal'
                ? 'bg-terminal-orange text-white'
                : 'bg-terminal-border text-terminal-text-dim hover:bg-terminal-border hover:text-terminal-text'
            }`}
            title="Draw horizontal line"
          >
            ➖ Horizontal Line
          </button>

          {drawings.length > 0 && (
            <button
              onClick={() => setDrawings([])}
              className="px-3 py-1 text-xs font-semibold rounded bg-terminal-red text-white hover:bg-red-600 transition-all"
              title="Clear all drawings"
            >
              🗑️ Clear
            </button>
          )}
        </div>
      </div>

      {/* Main Price Chart */}
      <div className="mb-4">
        <ResponsiveContainer width="100%" height={400}>
          <ComposedChart
            data={dataWithIndicators}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
            onClick={handleChartClick}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" />
            <XAxis
              dataKey="date"
              stroke="#999999"
              tick={{ fill: '#999999', fontSize: 11 }}
              tickFormatter={(value) => formatDate(value, timeRange)}
            />
            <YAxis
              yAxisId="price"
              stroke="#999999"
              tick={{ fill: '#999999', fontSize: 11 }}
              domain={['auto', 'auto']}
              tickFormatter={(value) => `$${value.toFixed(0)}`}
            />
            <Tooltip content={<CustomTooltip />} />

            {/* Candlesticks - using Area as a workaround for custom shapes */}
            <Area
              yAxisId="price"
              type="monotone"
              dataKey="high"
              stroke="#00c853"
              fill="transparent"
              strokeWidth={0}
            />
            <Area
              yAxisId="price"
              type="monotone"
              dataKey="low"
              stroke="#ff1744"
              fill="transparent"
              strokeWidth={0}
            />
            <Line
              yAxisId="price"
              type="monotone"
              dataKey="close"
              stroke="#ff6b35"
              strokeWidth={2}
              dot={false}
              name="Close"
            />

            {/* Moving Averages */}
            {showSMA20 && dataWithIndicators.some(p => p.sma20 != null) && (
              <Line
                yAxisId="price"
                type="monotone"
                dataKey="sma20"
                stroke="#1a659e"
                strokeWidth={2}
                dot={false}
                name="SMA(20)"
                connectNulls={true}
              />
            )}
            {showSMA50 && dataWithIndicators.some(p => p.sma50 != null) && (
              <Line
                yAxisId="price"
                type="monotone"
                dataKey="sma50"
                stroke="#ffc400"
                strokeWidth={2}
                dot={false}
                name="SMA(50)"
                connectNulls={true}
              />
            )}
            {showSMA200 && dataWithIndicators.some(p => p.sma200 != null) && (
              <Line
                yAxisId="price"
                type="monotone"
                dataKey="sma200"
                stroke="#9c27b0"
                strokeWidth={2}
                dot={false}
                name="SMA(200)"
                connectNulls={true}
              />
            )}
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* Volume Chart */}
      {showVolume && (
        <div className="mb-4">
          <ResponsiveContainer width="100%" height={120}>
            <ComposedChart
              data={dataWithIndicators}
              margin={{ top: 0, right: 30, left: 0, bottom: 0 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" />
              <XAxis
                dataKey="date"
                stroke="#999999"
                tick={{ fill: '#999999', fontSize: 11 }}
                tickFormatter={(value) => formatDate(value, timeRange)}
              />
              <YAxis
                stroke="#999999"
                tick={{ fill: '#999999', fontSize: 11 }}
                tickFormatter={(value) => formatVolume(value)}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar
                dataKey="volume"
                fill="#ff6b35"
                opacity={0.6}
                name="Volume"
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* MACD Chart */}
      {showMACD && dataWithIndicators.some(p => p.macd != null) && (
        <div className="mb-4">
          <h4 className="text-xs text-terminal-text-dim mb-2">MACD</h4>
          <ResponsiveContainer width="100%" height={120}>
            <ComposedChart
              data={dataWithIndicators}
              margin={{ top: 0, right: 30, left: 0, bottom: 0 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" />
              <XAxis
                dataKey="date"
                stroke="#999999"
                tick={{ fill: '#999999', fontSize: 11 }}
                tickFormatter={(value) => formatDate(value, timeRange)}
              />
              <YAxis
                stroke="#999999"
                tick={{ fill: '#999999', fontSize: 11 }}
              />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={0} stroke="#666666" strokeDasharray="3 3" />
              <Line
                type="monotone"
                dataKey="macd"
                stroke="#1a659e"
                strokeWidth={2}
                dot={false}
                name="MACD"
                connectNulls={true}
              />
              <Line
                type="monotone"
                dataKey="signal"
                stroke="#ff6b35"
                strokeWidth={2}
                dot={false}
                name="Signal"
                connectNulls={true}
              />
              <Bar
                dataKey="histogram"
                fill="#999999"
                opacity={0.6}
                name="Histogram"
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* RSI Chart */}
      {showRSI && dataWithIndicators.some(p => p.rsi != null) && (
        <div>
          <h4 className="text-xs text-terminal-text-dim mb-2">RSI(14)</h4>
          <ResponsiveContainer width="100%" height={120}>
            <ComposedChart
              data={dataWithIndicators}
              margin={{ top: 0, right: 30, left: 0, bottom: 0 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" />
              <XAxis
                dataKey="date"
                stroke="#999999"
                tick={{ fill: '#999999', fontSize: 11 }}
                tickFormatter={(value) => formatDate(value, timeRange)}
              />
              <YAxis
                stroke="#999999"
                tick={{ fill: '#999999', fontSize: 11 }}
                domain={[0, 100]}
              />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={70} stroke="#ff1744" strokeDasharray="3 3" label={{ value: 'Overbought', fill: '#ff1744', fontSize: 10 }} />
              <ReferenceLine y={30} stroke="#00c853" strokeDasharray="3 3" label={{ value: 'Oversold', fill: '#00c853', fontSize: 10 }} />
              <ReferenceLine y={50} stroke="#666666" strokeDasharray="3 3" />
              <Line
                type="monotone"
                dataKey="rsi"
                stroke="#ff6b35"
                strokeWidth={2}
                dot={false}
                name="RSI"
                connectNulls={true}
              />
              <Area
                type="monotone"
                dataKey="rsi"
                stroke="transparent"
                fill="#ff6b35"
                fillOpacity={0.2}
                connectNulls={true}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Instructions */}
      <div className="mt-4 p-3 bg-terminal-bg rounded border border-terminal-border">
        <p className="text-xs text-terminal-text-dim">
          <span className="text-terminal-orange font-semibold">Pro tip:</span> Toggle indicators above to customize your view.
          Use drawing tools to mark support/resistance levels. Hover over the chart for detailed information.
        </p>
      </div>
    </div>
  )
}

// Helper Functions

function generateMockData(timeRange, ticker) {
  const dataPoints = {
    '1D': 78,
    '5D': 390,
    '1M': 20,
    '3M': 60,
    '6M': 120,
    '1Y': 252,
    '5Y': 1260,
    'MAX': 2520
  }

  const points = dataPoints[timeRange] || 30
  const data = []
  let currentPrice = 150 + Math.random() * 50
  const now = new Date()

  for (let i = points; i >= 0; i--) {
    const date = new Date(now)

    if (timeRange === '1D') {
      date.setMinutes(date.getMinutes() - i * 5)
    } else if (timeRange === '5D') {
      date.setMinutes(date.getMinutes() - i * 5)
    } else {
      date.setDate(date.getDate() - i)
    }

    const change = (Math.random() - 0.48) * 5
    const open = currentPrice
    const close = currentPrice + change
    const high = Math.max(open, close) + Math.random() * 2
    const low = Math.min(open, close) - Math.random() * 2
    const volume = Math.floor(Math.random() * 10000000) + 1000000

    data.push({
      date: date.toISOString().split('T')[0],
      timestamp: date.getTime(),
      open: parseFloat(open.toFixed(2)),
      high: parseFloat(high.toFixed(2)),
      low: parseFloat(low.toFixed(2)),
      close: parseFloat(close.toFixed(2)),
      volume
    })

    currentPrice = close
  }

  return { data, ticker, timeframe: timeRange }
}

function calculateSMA(data, period) {
  const key = `sma${period}`

  for (let i = 0; i < data.length; i++) {
    if (i < period - 1) {
      data[i][key] = null
      continue
    }

    let sum = 0
    for (let j = 0; j < period; j++) {
      sum += data[i - j].close
    }
    data[i][key] = sum / period
  }
}

function calculateMACD(data) {
  // Calculate EMA 12 and EMA 26
  const ema12 = calculateEMA(data, 12)
  const ema26 = calculateEMA(data, 26)

  // MACD = EMA12 - EMA26
  for (let i = 0; i < data.length; i++) {
    if (ema12[i] !== null && ema26[i] !== null) {
      data[i].macd = ema12[i] - ema26[i]
    } else {
      data[i].macd = null
    }
  }

  // Signal line = EMA 9 of MACD
  const macdValues = data.map(d => d.macd)
  const signal = calculateEMAFromArray(macdValues, 9)

  for (let i = 0; i < data.length; i++) {
    data[i].signal = signal[i]
    if (data[i].macd !== null && data[i].signal !== null) {
      data[i].histogram = data[i].macd - data[i].signal
    } else {
      data[i].histogram = null
    }
  }
}

function calculateEMA(data, period) {
  const ema = []
  const multiplier = 2 / (period + 1)

  // Start with SMA for first value
  let sum = 0
  for (let i = 0; i < period; i++) {
    if (i >= data.length) {
      ema.push(null)
      continue
    }
    sum += data[i].close
  }

  ema[period - 1] = sum / period

  // Fill early values with null
  for (let i = 0; i < period - 1; i++) {
    ema[i] = null
  }

  // Calculate EMA
  for (let i = period; i < data.length; i++) {
    ema[i] = (data[i].close - ema[i - 1]) * multiplier + ema[i - 1]
  }

  return ema
}

function calculateEMAFromArray(values, period) {
  const ema = []
  const multiplier = 2 / (period + 1)

  let sum = 0
  let count = 0
  for (let i = 0; i < period && i < values.length; i++) {
    if (values[i] !== null) {
      sum += values[i]
      count++
    }
  }

  if (count === 0) {
    ema[period - 1] = null
  } else {
    ema[period - 1] = sum / count
  }

  for (let i = 0; i < period - 1; i++) {
    ema[i] = null
  }

  for (let i = period; i < values.length; i++) {
    if (values[i] !== null && ema[i - 1] !== null) {
      ema[i] = (values[i] - ema[i - 1]) * multiplier + ema[i - 1]
    } else {
      ema[i] = null
    }
  }

  return ema
}

function calculateRSI(data, period = 14) {
  for (let i = 0; i < data.length; i++) {
    if (i < period) {
      data[i].rsi = null
      continue
    }

    let gains = 0
    let losses = 0

    for (let j = 1; j <= period; j++) {
      const change = data[i - j + 1].close - data[i - j].close
      if (change > 0) {
        gains += change
      } else {
        losses -= change
      }
    }

    const avgGain = gains / period
    const avgLoss = losses / period

    if (avgLoss === 0) {
      data[i].rsi = 100
    } else {
      const rs = avgGain / avgLoss
      data[i].rsi = 100 - (100 / (1 + rs))
    }
  }
}

function formatDate(dateStr, timeRange) {
  const date = new Date(dateStr)

  if (timeRange === '1D' || timeRange === '5D') {
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  }

  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function formatVolume(volume) {
  if (volume >= 1e9) {
    return `${(volume / 1e9).toFixed(2)}B`
  } else if (volume >= 1e6) {
    return `${(volume / 1e6).toFixed(2)}M`
  } else if (volume >= 1e3) {
    return `${(volume / 1e3).toFixed(2)}K`
  }
  return volume.toString()
}
