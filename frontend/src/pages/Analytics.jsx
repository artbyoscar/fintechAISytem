import { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { getStats, getRecentAnalyses } from '../api'
import jsPDF from 'jspdf'
import 'jspdf-autotable'

const COLORS = {
  primary: '#ff6b35',
  success: '#00c853',
  danger: '#ff1744',
  warning: '#ffc400',
  info: '#2196f3'
}

export default function Analytics() {
  const [stats, setStats] = useState(null)
  const [analyses, setAnalyses] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAnalyticsData()
  }, [])

  const loadAnalyticsData = async () => {
    setLoading(true)
    try {
      const [statsRes, analysesRes] = await Promise.all([
        getStats(),
        getRecentAnalyses(100)
      ])

      if (analysesRes.success && analysesRes.data.analyses.length > 0) {
        setAnalyses(analysesRes.data.analyses)
        calculateStats(analysesRes.data.analyses)
      }
    } catch (error) {
      console.error('Failed to load analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  const calculateStats = (data) => {
    const totalAnalyses = data.length

    // Sentiment distribution
    const sentimentDist = data.reduce((acc, item) => {
      const label = item.analysis?.sentiment_label?.toLowerCase() || 'unknown'
      acc[label] = (acc[label] || 0) + 1
      return acc
    }, {})

    // Regime distribution
    const regimeDist = data.reduce((acc, item) => {
      const regime = item.analysis?.macro_regime || 'UNKNOWN'
      acc[regime] = (acc[regime] || 0) + 1
      return acc
    }, {})

    // Average sentiment score
    const avgSentiment = data.reduce((sum, item) => sum + (item.call?.sentiment_score || 0), 0) / totalAnalyses

    // Top tickers
    const tickerCount = data.reduce((acc, item) => {
      const ticker = item.call?.ticker
      if (ticker) {
        acc[ticker] = (acc[ticker] || 0) + 1
      }
      return acc
    }, {})
    const topTickers = Object.entries(tickerCount)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5)

    // Analyses over time (last 30 days)
    const last30Days = data.slice(0, 30).reverse()
    const timelineData = last30Days.map((item, idx) => ({
      name: `Day ${idx + 1}`,
      sentiment: (item.call?.sentiment_score || 0) * 100,
      confidence: (item.analysis?.confidence || 0) * 100
    }))

    setStats({
      totalAnalyses,
      sentimentDist,
      regimeDist,
      avgSentiment,
      topTickers,
      timelineData
    })
  }

  const exportToCSV = () => {
    const headers = ['Ticker', 'Sentiment', 'Score', 'Regime', 'Confidence', 'Date']
    const rows = analyses.map(item => [
      item.call?.ticker || 'N/A',
      item.analysis?.sentiment_label || 'N/A',
      item.call?.sentiment_score ? (item.call.sentiment_score * 100).toFixed(1) : 'N/A',
      item.analysis?.macro_regime || 'N/A',
      item.analysis?.confidence ? (item.analysis.confidence * 100).toFixed(1) : 'N/A',
      item.analysis?.timestamp ? new Date(item.analysis.timestamp).toLocaleDateString() : 'N/A'
    ])

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `analytics_${new Date().toISOString().split('T')[0]}.csv`
    link.click()
  }

  const exportToPDF = () => {
    const doc = new jsPDF()

    // Title
    doc.setFontSize(20)
    doc.text('Fintech AI Analytics Report', 14, 20)

    // Date
    doc.setFontSize(10)
    doc.text(`Generated: ${new Date().toLocaleString()}`, 14, 30)

    // Summary stats
    doc.setFontSize(12)
    doc.text('Summary Statistics', 14, 45)
    doc.setFontSize(10)
    doc.text(`Total Analyses: ${stats.totalAnalyses}`, 14, 55)
    doc.text(`Average Sentiment: ${(stats.avgSentiment * 100).toFixed(1)}%`, 14, 62)

    // Table
    const tableData = analyses.slice(0, 50).map(item => [
      item.call?.ticker || 'N/A',
      item.analysis?.sentiment_label || 'N/A',
      item.call?.sentiment_score ? (item.call.sentiment_score * 100).toFixed(1) + '%' : 'N/A',
      item.analysis?.macro_regime || 'N/A',
      item.analysis?.confidence ? (item.analysis.confidence * 100).toFixed(1) + '%' : 'N/A',
      item.analysis?.timestamp ? new Date(item.analysis.timestamp).toLocaleDateString() : 'N/A'
    ])

    doc.autoTable({
      head: [['Ticker', 'Sentiment', 'Score', 'Regime', 'Confidence', 'Date']],
      body: tableData,
      startY: 75,
      theme: 'grid',
      headStyles: { fillColor: [255, 107, 53] }
    })

    doc.save(`analytics_${new Date().toISOString().split('T')[0]}.pdf`)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-terminal-bg flex items-center justify-center">
        <div className="text-terminal-text-dim text-xl">Loading analytics...</div>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="min-h-screen bg-terminal-bg flex items-center justify-center">
        <div className="text-terminal-text-dim">No data available</div>
      </div>
    )
  }

  const sentimentPieData = Object.entries(stats.sentimentDist).map(([name, value]) => ({
    name: name.toUpperCase(),
    value
  }))

  const regimeBarData = Object.entries(stats.regimeDist).map(([name, value]) => ({
    name,
    count: value
  }))

  const topTickersData = stats.topTickers.map(([ticker, count]) => ({
    ticker,
    count
  }))

  return (
    <div className="min-h-screen bg-terminal-bg py-8 px-6">
      <div className="container mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-terminal-text mb-2">
              Analytics Dashboard
            </h1>
            <p className="text-terminal-text-dim">
              System performance metrics and insights
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={exportToCSV}
              className="px-4 py-2 bg-terminal-border hover:bg-terminal-orange transition-colors rounded-md text-terminal-text text-sm font-medium"
            >
              📊 Export CSV
            </button>
            <button
              onClick={exportToPDF}
              className="px-4 py-2 bg-terminal-orange hover:bg-terminal-orange-light transition-colors rounded-md text-white text-sm font-medium"
            >
              📄 Export PDF
            </button>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="text-terminal-text-dim text-sm mb-2">Total Analyses</div>
            <div className="text-3xl font-bold text-terminal-orange">{stats.totalAnalyses}</div>
          </div>

          <div className="card">
            <div className="text-terminal-text-dim text-sm mb-2">Avg Sentiment</div>
            <div className={`text-3xl font-bold ${stats.avgSentiment > 0 ? 'text-terminal-green' : 'text-terminal-red'}`}>
              {(stats.avgSentiment * 100).toFixed(1)}%
            </div>
          </div>

          <div className="card">
            <div className="text-terminal-text-dim text-sm mb-2">Most Common Regime</div>
            <div className="text-2xl font-bold text-terminal-text">
              {Object.entries(stats.regimeDist).sort(([,a], [,b]) => b - a)[0][0]}
            </div>
          </div>

          <div className="card">
            <div className="text-terminal-text-dim text-sm mb-2">Positive Ratio</div>
            <div className="text-3xl font-bold text-terminal-green">
              {((stats.sentimentDist.positive || 0) / stats.totalAnalyses * 100).toFixed(0)}%
            </div>
          </div>
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Sentiment Timeline */}
          <div className="card">
            <h2 className="text-xl font-semibold text-terminal-text mb-4">
              Sentiment Over Time
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={stats.timelineData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                <XAxis dataKey="name" stroke="#999" />
                <YAxis stroke="#999" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #444' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Legend />
                <Line type="monotone" dataKey="sentiment" stroke={COLORS.primary} name="Sentiment %" />
                <Line type="monotone" dataKey="confidence" stroke={COLORS.info} name="Confidence %" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Sentiment Distribution */}
          <div className="card">
            <h2 className="text-xl font-semibold text-terminal-text mb-4">
              Sentiment Distribution
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={sentimentPieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => `${entry.name}: ${entry.value}`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {sentimentPieData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={entry.name === 'POSITIVE' ? COLORS.success : entry.name === 'NEGATIVE' ? COLORS.danger : COLORS.warning}
                    />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #444' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Charts Row 2 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Macro Regime Distribution */}
          <div className="card">
            <h2 className="text-xl font-semibold text-terminal-text mb-4">
              Macro Regime Distribution
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={regimeBarData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                <XAxis dataKey="name" stroke="#999" />
                <YAxis stroke="#999" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #444' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Bar dataKey="count" fill={COLORS.primary} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Top Analyzed Tickers */}
          <div className="card">
            <h2 className="text-xl font-semibold text-terminal-text mb-4">
              Most Analyzed Tickers
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topTickersData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                <XAxis type="number" stroke="#999" />
                <YAxis dataKey="ticker" type="category" stroke="#999" width={60} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #444' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Bar dataKey="count" fill={COLORS.success} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Analyses Table */}
        <div className="card">
          <h2 className="text-xl font-semibold text-terminal-text mb-4">
            Recent Analyses
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-terminal-border text-sm text-terminal-text-dim">
                  <th className="text-left py-3 px-4">Ticker</th>
                  <th className="text-left py-3 px-4">Sentiment</th>
                  <th className="text-left py-3 px-4">Score</th>
                  <th className="text-left py-3 px-4">Regime</th>
                  <th className="text-left py-3 px-4">Confidence</th>
                  <th className="text-left py-3 px-4">Date</th>
                </tr>
              </thead>
              <tbody>
                {analyses.slice(0, 10).map((item, idx) => (
                  <tr key={idx} className="border-b border-terminal-border hover:bg-terminal-border transition-colors">
                    <td className="py-3 px-4">
                      <span className="font-mono font-bold text-terminal-orange">{item.call?.ticker || 'N/A'}</span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`font-semibold ${
                        item.analysis?.sentiment_label === 'positive' ? 'text-terminal-green' :
                        item.analysis?.sentiment_label === 'negative' ? 'text-terminal-red' :
                        'text-terminal-yellow'
                      }`}>
                        {item.analysis?.sentiment_label?.toUpperCase() || 'N/A'}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="font-mono text-terminal-text">
                        {item.call?.sentiment_score ? (item.call.sentiment_score * 100).toFixed(1) : 'N/A'}%
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`font-semibold ${
                        item.analysis?.macro_regime === 'BULL' ? 'text-terminal-green' :
                        item.analysis?.macro_regime === 'BEAR' ? 'text-terminal-red' :
                        'text-terminal-yellow'
                      }`}>
                        {item.analysis?.macro_regime || 'N/A'}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-terminal-text">
                        {item.analysis?.confidence ? (item.analysis.confidence * 100).toFixed(0) : 'N/A'}%
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-terminal-text-dim text-sm">
                        {item.analysis?.timestamp ? new Date(item.analysis.timestamp).toLocaleDateString() : 'N/A'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}
