# Quick Start Guide - Fintech AI System

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.13+ installed
- Node.js 18+ installed
- Git installed

### Step 1: Clone and Setup Backend

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/fintech-ai-system.git
cd fintech-ai-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Setup Frontend

```bash
# Open a new terminal in the project directory
cd frontend
npm install
```

### Step 3: Configure Environment (Optional)

```bash
# Copy environment template
cp .env.template .env

# Edit .env and add your API keys (optional for demo):
# ALPHA_VANTAGE_KEY=your_key_here
# FRED_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
```

**Note:** The system works with mock data even without API keys!

### Step 4: Start the Application

**Terminal 1: Start Backend API**
```bash
# In project root with venv activated
python run_api.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Terminal 2: Start Frontend**
```bash
# In frontend directory
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 1234 ms

  ➜  Local:   http://localhost:3000/
```

### Step 5: Open in Browser

Navigate to: **http://localhost:3000**

You should see the Bloomberg Terminal-style interface!

---

## 🎯 Try It Out

### Web Dashboard
1. Open http://localhost:3000
2. Enter a ticker symbol (e.g., "AAPL", "MSFT", "NVDA")
3. Click "Analyze"
4. View sentiment analysis and macro regime

### CLI Interface
```bash
# Analyze a single company
python main.py --ticker AAPL

# Show earnings calendar
python main.py --calendar

# Analyze multiple companies
python main.py --analyze-all
```

### API Endpoints

Try these in your browser or with curl:

```bash
# Health check
curl http://localhost:8000/health

# Analyze a company
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'

# Get recent analyses
curl http://localhost:8000/recent

# Get database stats
curl http://localhost:8000/stats
```

---

## 📊 Features Demo

### 1. Sentiment Analysis
The system uses FinBERT to analyze earnings call transcripts:
- **Bullish** (positive sentiment) = Green
- **Bearish** (negative sentiment) = Red
- **Neutral** = Yellow

### 2. Macro Regime Detection
Real-time market indicators:
- **VIX** - Market volatility
- **Unemployment Rate** - Economic health
- **Inflation (CPI)** - Price stability
- **Fed Funds Rate** - Monetary policy

Regime classifications:
- **BULL** 🐂 - Favorable market conditions
- **BEAR** 🐻 - Challenging market conditions
- **TRANSITION** ⚖️ - Mixed signals

### 3. Trading Recommendations
Combines sentiment + macro regime:
- **FAVORABLE** - Strong alignment
- **CAUTION** - Mixed signals
- **AVOID** - Contradictory signals

---

## 🧪 Run Tests

```bash
# Test sentiment analysis
python test_sentiment.py

# Test full pipeline
python test_pipeline.py

# Test API endpoints
python test_api.py

# Test backtesting engine (with mock data)
python test_backtester_mock.py
```

All tests should pass with ✓ marks!

---

## 🛠️ Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux/Mac

# Try a different port
uvicorn backend.api:app --host 0.0.0.0 --port 8080
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### API connection errors in browser
1. Ensure backend is running on port 8000
2. Check browser console for CORS errors
3. Verify API_BASE_URL in `frontend/src/api.js`

### SSL Certificate Errors (Windows)
The system includes workarounds for Windows SSL issues:
- Uses `YF_NO_CURL=1` environment variable
- Falls back to cached mock data
- Still demonstrates full functionality

### FinBERT model download fails
```bash
# Manually download FinBERT
python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; AutoTokenizer.from_pretrained('ProsusAI/finbert'); AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')"
```

---

## 📁 Project Layout

```
fintech-ai-system/
├── frontend/          ← React web dashboard (port 3000)
├── backend/           ← FastAPI + core logic (port 8000)
├── agents/            ← AI agents (sentiment, macro, market data)
├── data/              ← SQLite DB + cache files
├── main.py            ← CLI interface
└── run_api.py         ← API server launcher
```

---

## 🎨 UI Features

### Bloomberg Terminal Design
- **Dark mode by default** (terminal aesthetic)
- **Real-time status indicator** (API online/offline)
- **Color-coded sentiment** (green/red/yellow)
- **Smooth animations** and transitions
- **Recent analyses history**
- **Responsive layout** (works on mobile)

### Theme Toggle
Click the sun/moon icon in the header to switch between light and dark modes.

---

## 📚 Next Steps

1. **Add real earnings data**: Get Alpha Vantage API key
2. **Add economic data**: Get FRED API key (free)
3. **Explore backtesting**: Run historical sentiment validation
4. **Customize styling**: Edit `frontend/tailwind.config.js`
5. **Add charts**: Integrate Recharts for visualizations
6. **Deploy**: Host backend on Railway/Render, frontend on Vercel

---

## 🆘 Need Help?

- **Documentation**: See [README.md](README.md)
- **API Guide**: See [API_GUIDE.md](API_GUIDE.md)
- **Frontend Setup**: See [frontend/README.md](frontend/README.md)
- **Issues**: Open a GitHub issue

---

## 🎉 You're Ready!

Your Fintech AI System is now running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

**Have fun analyzing earnings calls!** 📈
