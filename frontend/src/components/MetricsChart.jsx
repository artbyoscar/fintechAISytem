import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts'

/**
 * MetricsChart Component
 * Line/Area chart for displaying price history and metrics using Recharts
 */
export default function MetricsChart({ data, title, dataKey, color = '#ff6b35' }) {
  if (!data || data.length === 0) {
    return (
      <div className="card">
        <h3 className="text-lg font-semibold text-terminal-text mb-4">
          {title || 'Historical Metrics'}
        </h3>
        <div className="text-center py-12">
          <svg className="w-12 h-12 mx-auto mb-3 text-terminal-text-dim" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
          </svg>
          <p className="text-sm text-terminal-text-dim">
            No chart data available
          </p>
        </div>
      </div>
    )
  }

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-terminal-bg-light border border-terminal-border rounded-md p-3 shadow-lg">
          <p className="text-xs text-terminal-text-dim mb-1">{label}</p>
          <p className="text-sm font-semibold text-terminal-orange">
            {payload[0].name}: {payload[0].value.toFixed(2)}
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-terminal-text mb-4">
        {title || 'Historical Metrics'}
      </h3>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={data}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={color} stopOpacity={0.3}/>
                <stop offset="95%" stopColor={color} stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" />
            <XAxis
              dataKey="date"
              stroke="#999999"
              style={{ fontSize: '12px', fontFamily: 'monospace' }}
            />
            <YAxis
              stroke="#999999"
              style={{ fontSize: '12px', fontFamily: 'monospace' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey={dataKey || 'value'}
              stroke={color}
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorValue)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Chart Legend */}
      <div className="mt-4 pt-4 border-t border-terminal-border">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
            <span className="text-terminal-text-dim capitalize">
              {dataKey || 'Value'}
            </span>
          </div>
          <div className="text-terminal-text-dim">
            {data.length} data points
          </div>
        </div>
      </div>
    </div>
  )
}

/**
 * MultiLineChart Component
 * Multiple lines for comparing metrics
 */
export function MultiLineChart({ data, title, lines }) {
  if (!data || data.length === 0) {
    return <MetricsChart data={data} title={title} />
  }

  const colors = {
    price: '#ff6b35',
    sentiment: '#00c853',
    volume: '#1a659e',
    volatility: '#ffc400'
  }

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-terminal-bg-light border border-terminal-border rounded-md p-3 shadow-lg">
          <p className="text-xs text-terminal-text-dim mb-2">{label}</p>
          {payload.map((entry, index) => (
            <div key={index} className="flex items-center justify-between gap-4 mb-1">
              <span className="text-xs text-terminal-text-dim capitalize">
                {entry.name}:
              </span>
              <span className="text-sm font-semibold" style={{ color: entry.color }}>
                {entry.value.toFixed(2)}
              </span>
            </div>
          ))}
        </div>
      )
    }
    return null
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-terminal-text mb-4">
        {title || 'Multi-Metric Comparison'}
      </h3>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={data}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#1a1a1a" />
            <XAxis
              dataKey="date"
              stroke="#999999"
              style={{ fontSize: '12px', fontFamily: 'monospace' }}
            />
            <YAxis
              stroke="#999999"
              style={{ fontSize: '12px', fontFamily: 'monospace' }}
            />
            <Tooltip content={<CustomTooltip />} />
            {lines && lines.map((line, idx) => (
              <Line
                key={idx}
                type="monotone"
                dataKey={line.dataKey}
                stroke={colors[line.dataKey] || colors.price}
                strokeWidth={2}
                dot={false}
                name={line.name || line.dataKey}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Chart Legend */}
      <div className="mt-4 pt-4 border-t border-terminal-border">
        <div className="flex flex-wrap items-center gap-4 text-xs">
          {lines && lines.map((line, idx) => (
            <div key={idx} className="flex items-center gap-2">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: colors[line.dataKey] || colors.price }}
              />
              <span className="text-terminal-text-dim">
                {line.name || line.dataKey}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
