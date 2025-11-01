# React Components

Modular, reusable components for the Fintech AI dashboard.

## Components Overview

### 1. TickerSearch
Search input with autocomplete for ticker symbols.

**Props:**
- `onAnalyze(ticker)` - Callback when analyze is triggered
- `loading` - Boolean for loading state
- `disabled` - Boolean to disable input (e.g., when API is offline)

**Features:**
- Autocomplete dropdown with 20 popular tickers
- Type-to-filter suggestions
- Click suggestion to auto-analyze
- Handles loading and disabled states
- Offline API warning

**Usage:**
```jsx
<TickerSearch
  onAnalyze={handleAnalyze}
  loading={isLoading}
  disabled={apiStatus === 'offline'}
/>
```

---

### 2. SentimentCard
Displays sentiment analysis results with color-coded UI.

**Props:**
- `sentiment` - Sentiment data object with:
  - `sentiment_label` - "positive", "negative", or "neutral"
  - `sentiment_score` - Number between -1 and 1
  - `confidence` - Confidence percentage (0-1)
  - `scores` - Object with detailed breakdown
  - `key_quotes` (optional) - Array of quote objects

**Features:**
- Color coding (green = bullish, red = bearish, yellow = neutral)
- Sentiment gauge with gradient visualization
- Detailed score breakdown with progress bars
- Icons for each sentiment type
- Key quotes display

**Usage:**
```jsx
<SentimentCard sentiment={analysisResult.sentiment} />
```

---

### 3. MacroRegimeCard
Shows macro economic regime and trading recommendations.

**Props:**
- `macro` - Macro regime object with:
  - `regime` - "BULL", "BEAR", or "TRANSITION"
  - `recommendation` - "FAVORABLE", "CAUTION", or "AVOID"
  - `confidence` (optional) - Confidence percentage
  - `risk_level` (optional) - "LOW", "MODERATE", or "HIGH"
  - `indicators` (optional) - Object with VIX, unemployment, etc.
  - `reasoning` (optional) - Explanation text
  - `signals` (optional) - Bullish/neutral/bearish signal counts

**Features:**
- Regime icons and emojis (🐂 bull, 🐻 bear, ⚖️ transition)
- Confidence progress bar
- Recommendation badges
- Market indicators grid
- Color-coded risk levels
- Signal breakdown

**Usage:**
```jsx
<MacroRegimeCard macro={analysisResult.macro} />
```

---

### 4. AnalysisResults
Main container that displays full analysis results.

**Props:**
- `result` - Complete analysis result object with:
  - `ticker` - Stock ticker symbol
  - `company_name` (optional) - Company name
  - `timestamp` - Analysis timestamp
  - `sentiment` - Sentiment data
  - `macro` - Macro regime data
  - `recommendation` (optional) - Trading recommendation text
  - `performance` (optional) - Timing data

**Features:**
- Company overview header with timestamp
- Processing time badge
- Quick stats bar
- Integrates SentimentCard and MacroRegimeCard
- Trading recommendation callout box
- Performance breakdown

**Usage:**
```jsx
<AnalysisResults result={analysisData} />
```

---

### 5. RecentAnalyses
Table/list of recent analysis history.

**Props:**
- `analyses` - Array of analysis objects
- `onTickerClick(ticker)` - Callback when ticker is clicked

**Features:**
- Responsive design (table on desktop, cards on mobile)
- Click to re-analyze
- Empty state with helpful message
- Color-coded sentiment and regime
- Formatted dates
- Hover effects

**Usage:**
```jsx
<RecentAnalyses
  analyses={recentList}
  onTickerClick={handleTickerClick}
/>
```

---

### 6. MetricsChart
Data visualization using Recharts library.

**Props:**
- `data` - Array of data points with `date` and value fields
- `title` - Chart title (default: "Historical Metrics")
- `dataKey` - Key for the value to plot (default: "value")
- `color` - Line/area color (default: "#ff6b35")

**Features:**
- Area chart with gradient fill
- Custom tooltip styling
- Responsive container
- Empty state handling
- Chart legend
- MultiLineChart variant for comparisons

**Usage:**
```jsx
<MetricsChart
  data={priceHistory}
  title="Price History"
  dataKey="close"
  color="#ff6b35"
/>

<MultiLineChart
  data={comparisonData}
  title="Multi-Metric Comparison"
  lines={[
    { dataKey: 'price', name: 'Price' },
    { dataKey: 'sentiment', name: 'Sentiment' }
  ]}
/>
```

---

## Styling

All components use Tailwind CSS with custom Bloomberg Terminal theme:

**Color Classes:**
- `status-bullish` - Green for positive sentiment
- `status-bearish` - Red for negative sentiment
- `status-neutral` - Yellow for neutral sentiment
- `text-terminal-orange` - Primary orange accent
- `text-terminal-green-light` - Success/bullish
- `text-terminal-red-light` - Error/bearish
- `text-terminal-yellow-light` - Warning/neutral
- `bg-terminal-bg` - Main background (black)
- `bg-terminal-bg-light` - Secondary background
- `border-terminal-border` - Border color

**Common Classes:**
- `card` - Card container with border and padding
- `btn-primary` - Primary button styling
- `btn-secondary` - Secondary button styling
- `input-field` - Input field styling
- `animate-fade-in` - Fade-in animation

---

## Component Architecture

```
App.jsx (Main container)
├── TickerSearch (Search input)
├── AnalysisResults (Results container)
│   ├── SentimentCard (Sentiment display)
│   └── MacroRegimeCard (Macro display)
├── RecentAnalyses (History table)
└── MetricsChart (Data visualization)
```

---

## Future Enhancements

Potential additions:
- [ ] PortfolioWatchlist component
- [ ] BacktestResults component
- [ ] ComparisonView for multiple tickers
- [ ] SettingsPanel component
- [ ] AlertsManager component
- [ ] ExportButton for PDF/CSV
- [ ] StockChart component with candlesticks
- [ ] NewsPanel component
