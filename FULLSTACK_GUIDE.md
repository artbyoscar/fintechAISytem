# Full-Stack Integration Guide

Complete guide for running the Fintech AI System with both backend and frontend.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                    React + Vite + Tailwind                   │
│                   http://localhost:3000                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ HTTP Requests (Axios)
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                         Backend                              │
│                     FastAPI + Uvicorn                        │
│                   http://localhost:8000                      │
├──────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  Sentiment     │  │   Macro      │  │  Market Data   │  │
│  │  Analyzer      │  │   Detector   │  │  Fetcher       │  │
│  │  (FinBERT)     │  │  (VIX+FRED)  │  │  (yfinance)    │  │
│  └────────────────┘  └──────────────┘  └────────────────┘  │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              SQLite Database                         │   │
│  │         (data/fintech_ai.db)                        │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (Both Servers)

### Terminal 1: Backend API

```bash
# Navigate to project root
cd c:\Users\OscarNuñez\Desktop\fintechAISytem

# Activate virtual environment
venv\Scripts\activate

# Start FastAPI server
python run_api.py
```

**Expected Output:**
```
================================================================================
FINTECH AI SYSTEM - API SERVER
================================================================================

Starting server on http://127.0.0.1:8000
Docs available at: http://127.0.0.1:8000/docs

INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Terminal 2: Frontend Dev Server

```bash
# Navigate to frontend directory
cd c:\Users\OscarNuñez\Desktop\fintechAISytem\frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Expected Output:**
```
  VITE v5.0.8  ready in 1234 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Open Browser

Navigate to: **http://localhost:3000**

You should see:
- Bloomberg Terminal-style dark interface
- API status indicator (green = online)
- Search bar with ticker autocomplete
- Recent analyses (if any exist)

---

## 📡 API Integration Details

### Connection Flow

1. **Frontend Starts** → Checks API health
2. **User Searches Ticker** → Sends POST request
3. **Backend Analyzes** → Returns results
4. **Frontend Displays** → Shows in components

### API Client Configuration

**File:** `frontend/src/api.js`

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});
```

**Environment Variable (Optional):**
Create `frontend/.env`:
```
VITE_API_URL=http://localhost:8000
```

### API Endpoints Used

| Endpoint | Method | Frontend Function | Purpose |
|----------|--------|-------------------|---------|
| `/health` | GET | `checkHealth()` | Check API status |
| `/analyze` | POST | `analyzeCompany(ticker)` | Analyze company |
| `/recent` | GET | `getRecentAnalyses(limit)` | Get recent analyses |
| `/stats` | GET | `getStats()` | Database statistics |
| `/companies` | GET | `getCompanies()` | List all companies |

### Request/Response Examples

#### 1. Analyze Company

**Request:**
```javascript
POST /analyze
Content-Type: application/json

{
  "ticker": "AAPL"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "ticker": "AAPL",
    "timestamp": "2025-10-31T18:21:21",
    "sentiment": {
      "sentiment_label": "positive",
      "sentiment_score": 0.836,
      "confidence": 0.852,
      "scores": {
        "positive": 0.892,
        "negative": 0.023,
        "neutral": 0.085
      }
    },
    "macro": {
      "regime": "BULL",
      "recommendation": "FAVORABLE",
      "confidence": 0.875,
      "indicators": {
        "vix": 18.5,
        "unemployment": 3.8,
        "inflation": 3.2,
        "fed_rate": 5.33
      }
    },
    "recommendation": "Strong Buy - Positive sentiment aligns with bullish macro regime...",
    "performance": {
      "total_time": 0.52,
      "sentiment_time": 0.51,
      "macro_time": 0.00,
      "database_time": 0.01
    }
  },
  "timestamp": "2025-10-31T18:21:21.142000"
}
```

#### 2. Check Health

**Request:**
```javascript
GET /health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "database": "connected",
    "model": "loaded",
    "timestamp": "2025-10-31T18:21:09.048000"
  },
  "timestamp": "2025-10-31T18:21:09.048000"
}
```

---

## 🎯 User Flow

### 1. Page Load
```
User opens http://localhost:3000
  ↓
Frontend calls checkHealth()
  ↓
API status indicator: GREEN (online) or RED (offline)
  ↓
Frontend calls getRecentAnalyses()
  ↓
Recent analyses displayed in table
```

### 2. Search Ticker
```
User types "AAPL" in search box
  ↓
Autocomplete shows suggestions
  ↓
User clicks "Analyze" button
  ↓
Frontend sets loading state (spinner appears)
  ↓
Frontend calls analyzeCompany("AAPL")
  ↓
Backend runs analysis (FinBERT + Macro + Database)
  ↓
Backend returns results (~0.5-1.0 seconds)
  ↓
Frontend receives data
  ↓
Components render results:
  - AnalysisResults
  - SentimentCard (green/red/yellow)
  - MacroRegimeCard (bull/bear/transition)
  - Trading recommendation
```

### 3. Error Handling
```
API offline or error occurs
  ↓
Error interceptor catches issue
  ↓
User-friendly error message displayed
  ↓
"Cannot connect to backend. Please ensure the API server is running."
```

---

## 🔧 State Management

### App.jsx State

```javascript
const [darkMode, setDarkMode] = useState(true)
const [loading, setLoading] = useState(false)
const [result, setResult] = useState(null)
const [error, setError] = useState(null)
const [apiStatus, setApiStatus] = useState('checking')
const [recentAnalyses, setRecentAnalyses] = useState([])
```

### State Flow

1. **Initial State:**
   - `apiStatus`: 'checking'
   - `loading`: false
   - `result`: null
   - `error`: null

2. **During Analysis:**
   - `loading`: true
   - `result`: null (cleared)
   - `error`: null (cleared)

3. **On Success:**
   - `loading`: false
   - `result`: { ticker, sentiment, macro, ... }
   - `error`: null

4. **On Error:**
   - `loading`: false
   - `result`: null
   - `error`: "Error message"

---

## 🎨 Component Data Flow

### TickerSearch Component

**Input:**
```javascript
<TickerSearch
  onAnalyze={handleAnalyze}
  loading={loading}
  disabled={apiStatus === 'offline'}
/>
```

**Triggers:**
```javascript
const handleAnalyze = async (ticker) => {
  setLoading(true)
  setError(null)
  setResult(null)

  try {
    const response = await analyzeCompany(ticker)
    if (response.success) {
      setResult(response.data)
      loadRecentAnalyses() // Refresh list
    }
  } catch (err) {
    setError(err.message)
  } finally {
    setLoading(false)
  }
}
```

### AnalysisResults Component

**Input:**
```javascript
<AnalysisResults result={result} />
```

**Renders:**
- Company header (ticker, timestamp, processing time)
- SentimentCard (if `result.sentiment` exists)
- MacroRegimeCard (if `result.macro` exists)
- Trading recommendation (if `result.recommendation` exists)

### RecentAnalyses Component

**Input:**
```javascript
<RecentAnalyses
  analyses={recentAnalyses}
  onTickerClick={handleTickerClick}
/>
```

**Triggers:**
```javascript
const handleTickerClick = (ticker) => {
  handleAnalyze(ticker) // Re-analyze clicked ticker
}
```

---

## 🐛 Debugging

### Check Backend Status

1. **API Health Endpoint:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Interactive API Docs:**
   Open http://localhost:8000/docs in browser

3. **Backend Logs:**
   Check Terminal 1 for logs:
   ```
   INFO:     127.0.0.1:60274 - "POST /analyze HTTP/1.1" 200 OK
   ```

### Check Frontend Status

1. **Browser Console:**
   - F12 → Console tab
   - Look for API errors or network issues

2. **Network Tab:**
   - F12 → Network tab
   - Filter by "Fetch/XHR"
   - Click request to see payload and response

3. **React DevTools:**
   - Install React DevTools extension
   - Inspect component state and props

### Common Issues

#### 1. "API OFFLINE" (Red Indicator)

**Cause:** Backend not running or wrong URL

**Fix:**
```bash
# Start backend
cd c:\Users\OscarNuñez\Desktop\fintechAISytem
venv\Scripts\activate
python run_api.py
```

#### 2. CORS Errors

**Cause:** Backend not allowing frontend origin

**Fix:** Backend already configured with CORS middleware:
```python
# backend/api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3. Port Already in Use

**Backend (8000):**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Frontend (3000):**
```bash
# Kill vite process
npx kill-port 3000
```

#### 4. Analysis Takes Too Long

**Cause:** First-time FinBERT model download or slow CPU

**Fix:**
- Wait for initial model download (~400MB)
- Subsequent analyses are faster (~0.5s)
- Model cached in `~/.cache/huggingface/`

---

## 📊 Performance Metrics

**Typical Analysis Times:**

| Component | Time | Note |
|-----------|------|------|
| FinBERT Sentiment | 0.5s | First run: 2-3s (model load) |
| Macro Regime | 0.01s | Cached data |
| Database Save | 0.01s | Local SQLite |
| **Total** | **~0.52s** | Frontend to backend to response |

**Network Latency:**
- Localhost: <10ms
- Same network: 10-50ms
- Internet deployment: 100-500ms

---

## 🚀 Production Deployment

### Backend

**Option 1: Railway.app**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
railway login
railway init
railway up
```

**Option 2: Render.com**
```yaml
# render.yaml
services:
  - type: web
    name: fintech-ai-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn backend.api:app --host 0.0.0.0 --port $PORT
```

### Frontend

**Option 1: Vercel**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel
```

**Option 2: Netlify**
```bash
# Build
npm run build

# Deploy dist/ folder to Netlify
```

**Update API URL:**
```env
# frontend/.env.production
VITE_API_URL=https://your-backend.railway.app
```

---

## 📝 Testing the Integration

### Manual Test Flow

1. **Start both servers** (backend + frontend)

2. **Check API status indicator:**
   - Should be GREEN "API ONLINE"

3. **Search for AAPL:**
   - Type "AAPL" in search box
   - Click "Analyze" button
   - Should see loading spinner

4. **Verify results:**
   - Company header shows "AAPL"
   - Sentiment card shows color (green/red/yellow)
   - Macro card shows regime (BULL/BEAR)
   - Trading recommendation displayed

5. **Check recent analyses:**
   - Clear results (click MAEI logo)
   - Should see AAPL in recent list
   - Click to re-analyze

6. **Test error handling:**
   - Stop backend server
   - Status indicator turns RED
   - Search disabled with error message

### Automated Test Script

```bash
# Test backend
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'

# Should return 200 OK with JSON data
```

---

## 🎓 Summary

**Frontend → Backend Connection:**
- ✅ API client configured (axios)
- ✅ Health check on page load
- ✅ Error handling with interceptors
- ✅ Loading states in UI
- ✅ Results displayed in components
- ✅ Recent analyses fetched
- ✅ Click to re-analyze

**Complete Integration:**
1. User searches ticker → Frontend
2. POST /analyze → Backend API
3. FinBERT + Macro analysis → Python agents
4. Results saved → SQLite database
5. JSON response → Backend to Frontend
6. Components render → React UI
7. User sees results → Dashboard

**All features working! 🎉**
