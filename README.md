# Macro-Aware Earnings Intelligence System

AI-powered financial intelligence platform that analyzes earnings calls with sentiment analysis and macro regime context to generate actionable trading insights.

## Vision
Build a financial intelligence platform that helps investors identify narrative divergences in earnings calls, weighted by macro regime context.

---

## Quick Start

### Backend Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/fintech-ai-system.git
cd fintech-ai-system

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend Installation

```bash
# Install Node.js dependencies
cd frontend
npm install
```

### Run the Application

**Option 1: CLI Interface**
```bash
# Analyze a single company
python main.py --ticker NVDA

# Show earnings calendar
python main.py --calendar

# Analyze all companies
python main.py --analyze-all
```

**Option 2: Web Dashboard**
```bash
# Terminal 1: Start backend API
python run_api.py

# Terminal 2: Start frontend dev server
cd frontend
npm run dev
```

Then open http://localhost:3000 in your browser.

### Run Tests

```bash
python test_pipeline.py
python test_sentiment.py
python test_api.py
```

---

## Example Output

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                 MACRO-AWARE EARNINGS INTELLIGENCE SYSTEM                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Analysis Results: NVIDIA Corporation (NVDA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sentiment Analysis
┌─────────────────────┬────────────────────────────────────────────────────────┐
│ Overall Sentiment   │ 📈 POSITIVE (Score: +0.746, Confidence: 76.3%)        │
│ Sentiment Score     │ +0.746 (-1=bearish, +1=bullish)                        │
│ Confidence          │ 76.3%                                                  │
│ Distribution        │ Positive: 87.5% | Negative: 0.0% | Neutral: 12.5%     │
└─────────────────────┴────────────────────────────────────────────────────────┘

Macro Regime Analysis
┌─────────────────────┬────────────────────────────────────────────────────────┐
│ Regime              │ 🐂 BULL                                                │
│ Confidence          │ 87.5%                                                  │
│ VIX                 │ 18.5                                                   │
│ Unemployment        │ 3.8%                                                   │
│ Inflation           │ 3.2%                                                   │
└─────────────────────┴────────────────────────────────────────────────────────┘

Trading Recommendation
┌─────────────────────┬────────────────────────────────────────────────────────┐
│ Overall Verdict     │ 🚀 STRONG BUY                                          │
│ Recommendation      │ FAVORABLE                                              │
│ Risk Level          │ MODERATE                                               │
└─────────────────────┴────────────────────────────────────────────────────────┘
```

---

## Current Features

### ✅ Completed

#### Day 1: Core Analysis Engine
- **Sentiment Analysis Agent**
  - FinBERT-powered sentiment analysis
  - Sentence-level granular analysis
  - Confidence scoring and aggregation
  - Key quote extraction

- **Macro Regime Detector**
  - Real-time VIX data from Yahoo Finance
  - FRED API integration (unemployment, inflation, Fed rate, GDP)
  - Bull/Bear/Transition regime detection
  - Trading recommendations with risk levels
  - 24-hour caching for performance

- **Analysis Orchestrator**
  - Coordinates all agents in pipeline
  - Comprehensive report generation
  - Performance timing and monitoring
  - Database storage and retrieval

- **SQLite Database**
  - Companies, earnings calls, and analysis results
  - Indexed for fast queries
  - Persistent storage of all analyses

- **Professional CLI Interface**
  - Rich terminal UI with colors
  - Real-time progress indicators
  - Formatted tables and panels
  - Multiple analysis modes

#### Day 2: Real Data & API
- **Market Data Integration**
  - Real-time stock prices via yfinance
  - Historical price data (OHLCV)
  - Volatility calculations and Sharpe ratio
  - 52-week high/low, P/E ratios, market cap
  - 1-hour intelligent caching

- **FastAPI REST API**
  - 7 RESTful endpoints
  - CORS middleware for frontend
  - Standard JSON response format
  - Error handling and validation
  - Health monitoring

- **Backtesting Engine**
  - Historical sentiment prediction validation
  - Accuracy metrics (1-day, 5-day, 30-day)
  - Performance by sentiment label
  - Best/worst predictions analysis
  - JSON report generation

#### Day 3: Web Dashboard
- **React Frontend**
  - Bloomberg Terminal-inspired design
  - Real-time analysis display
  - Dark mode (default) with light mode toggle
  - Sentiment visualization with color coding
  - Macro regime indicators
  - Recent analyses history
  - API health status monitoring
  - Responsive design (desktop & mobile)
  - Professional animations and transitions

---

## Project Structure

```
fintech-ai-system/
│
├── agents/                      # AI Agents
│   ├── __init__.py
│   ├── sentiment_analyzer.py   # FinBERT sentiment analysis
│   ├── earnings_fetcher.py     # Earnings data retrieval
│   ├── macro_detector.py       # Macro regime classification
│   └── market_data.py          # Real-time stock data (yfinance)
│
├── backend/                     # Backend Infrastructure
│   ├── __init__.py
│   ├── database.py             # SQLite database manager
│   ├── orchestrator.py         # Agent orchestration pipeline
│   ├── api.py                  # FastAPI REST API
│   ├── backtester.py           # Backtesting engine
│   └── config.py               # Environment configuration
│
├── frontend/                    # React Web Dashboard
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── main.jsx            # Entry point
│   │   ├── api.js              # API client
│   │   └── index.css           # Tailwind styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── README.md
│
├── data/                        # Data Storage
│   ├── fintech_ai.db           # SQLite database
│   ├── analysis_reports/       # JSON analysis reports
│   ├── backtests/              # Backtest results
│   ├── market_cache/           # Market data cache
│   ├── macro_cache/            # Macro indicators cache
│   └── earnings_cache.json     # Cached earnings data
│
├── main.py                      # CLI entry point
├── run_api.py                   # API server launcher
├── test_sentiment.py            # Sentiment analyzer tests
├── test_pipeline.py             # End-to-end pipeline tests
├── test_api.py                  # API endpoint tests
├── test_backtester_mock.py     # Backtesting tests
├── requirements.txt             # Python dependencies
├── .env.template                # Environment variables template
└── README.md                    # This file
```

---

## Tech Stack

### AI/ML
- **FinBERT** (ProsusAI/finbert) - Financial sentiment analysis
- **Transformers** (HuggingFace) - Model loading and inference
- **PyTorch** - Deep learning framework

### Backend
- **FastAPI** - Modern REST API framework
- **SQLite** - Embedded database
- **Python 3.13+** - Core language
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS
- **Axios** - HTTP client
- **Recharts** - Data visualization (planned)

### Data Sources
- **yfinance** - Real-time stock data
- **FRED API** - Economic indicators
- **Yahoo Finance** - VIX data
- **Alpha Vantage** - Earnings calendar (planned)

### CLI
- **Rich** - Beautiful terminal UI
- **argparse** - Command-line parsing

### Data Processing
- **pandas** - Data manipulation
- **numpy** - Numerical computations
- **python-dotenv** - Configuration management

---

## How It Works

### Analysis Pipeline

1. **Fetch Transcript** - Retrieves earnings call transcript
2. **Sentiment Analysis** - FinBERT analyzes each sentence
3. **Macro Detection** - Classifies current market regime
4. **Synthesis** - Combines insights into actionable report
5. **Storage** - Saves to database and JSON file

### Sentiment Scoring

- Range: -1 (extremely bearish) to +1 (extremely bullish)
- Aggregated from sentence-level analysis
- Weighted by confidence scores

### Macro Regime Classification

**BULL Market** (🐂)
- VIX < 20
- Unemployment < 4.5%
- Inflation < 3.5%
- Confidence > 65%

**BEAR Market** (🐻)
- VIX > 25 OR
- Unemployment > 5% OR
- Inflation > 4%
- Confidence > 65%

**TRANSITION** (⚖️)
- Mixed signals
- Regime uncertainty

### Overall Assessment

Combines sentiment + macro regime:
- **STRONG BUY**: Bull regime + Positive sentiment
- **BUY**: Bull regime + Moderate positive
- **NEUTRAL**: Mixed signals
- **SELL**: Bear regime + Negative sentiment
- **STRONG SELL**: Bear regime + Strong negative

---

## Next Steps (Roadmap)

### Day 2-3: Real Data Integration
- [ ] Alpha Vantage API for earnings calendar
- [ ] SEC EDGAR for transcripts
- [ ] FRED API for macro data
- [ ] Real-time VIX data

### Day 4-5: Advanced Analytics
- [ ] Historical sentiment trends
- [ ] Peer comparison analysis
- [ ] Earnings surprise detection
- [ ] Narrative divergence scoring

### Week 2: Web Dashboard
- [ ] FastAPI backend
- [ ] React frontend
- [ ] Interactive charts (Plotly)
- [ ] Real-time updates

### Week 3: Backtesting
- [ ] Historical performance analysis
- [ ] Strategy optimization
- [ ] Risk metrics
- [ ] Portfolio simulation

### Future Enhancements
- [ ] Multi-language support
- [ ] Sector rotation signals
- [ ] Options strategy recommendations
- [ ] Slack/Discord integration
- [ ] Email alerts

---

## Deployment

### Docker Deployment (Recommended for Production)

#### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM available
- FRED API key ([Get one free](https://fred.stlouisfed.org/docs/api/api_key.html))

#### Quick Deploy

**Step 1: Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your FRED API key
# FRED_API_KEY=your_actual_api_key_here
```

**Step 2: Deploy with Script**
```bash
# Make deploy script executable (Linux/Mac)
chmod +x deploy.sh

# Interactive menu
./deploy.sh

# Or use direct commands:
./deploy.sh dev      # Deploy development environment
./deploy.sh prod     # Deploy production environment
./deploy.sh build    # Build Docker images only
./deploy.sh test     # Run tests
./deploy.sh logs     # View container logs
./deploy.sh status   # Check service health
./deploy.sh clean    # Cleanup containers and images
./deploy.sh stop     # Stop all services
```

**Step 3: Access Application**

Development mode:
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

Production mode (with nginx):
- Application: http://localhost
- API: http://localhost/api

#### Manual Docker Commands

```bash
# Development (backend + frontend dev servers)
docker-compose up -d

# Production (with nginx reverse proxy)
docker-compose --profile production up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

#### Docker Services

**Backend Service**
- Image: `fintech-ai-backend:latest`
- Port: 8000
- Workers: 2 (configurable via `UVICORN_WORKERS`)
- Health check: Every 30s
- Restart policy: unless-stopped

**Frontend Service**
- Image: `node:18-alpine`
- Port: 3000 (dev) or served via nginx (prod)
- Hot reload enabled in dev mode

**Nginx Service** (production only)
- Image: `nginx:alpine`
- Port: 80
- Features: Gzip compression, static asset caching, API proxying
- Configuration: `nginx.conf`

#### Environment Variables

Required:
```bash
FRED_API_KEY=your_key          # FRED API for macro data
```

Optional:
```bash
ENVIRONMENT=production         # Environment mode
LOG_LEVEL=INFO                 # Logging verbosity
VITE_API_URL=http://localhost:8000  # Backend URL for frontend
UVICORN_WORKERS=2              # Number of API workers
CORS_ORIGINS=http://localhost:3000  # Allowed CORS origins
RATE_LIMIT=100                 # API rate limit (req/min)
```

Email alerts (optional):
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=alerts@fintechai.com
```

#### Data Persistence

Docker volumes automatically persist:
- SQLite database: `./data/fintech_ai.db`
- Analysis reports: `./data/analysis_reports/`
- Alert history: `./data/alerts/`
- Backtest results: `./data/backtests/`
- Cache files: `./data/*_cache/`

#### Production Checklist

Before deploying to production:

- [ ] Set `ENVIRONMENT=production` in `.env`
- [ ] Configure real FRED API key
- [ ] Update `CORS_ORIGINS` with your domain
- [ ] Enable rate limiting with `RATE_LIMIT`
- [ ] Configure SMTP for email alerts (optional)
- [ ] Set up SSL/TLS certificates for HTTPS
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Create database backups strategy
- [ ] Test health checks: `curl http://localhost:8000/health`

#### Troubleshooting

**Backend won't start:**
```bash
# Check logs
docker-compose logs backend

# Common issues:
# - Missing FRED_API_KEY in .env
# - Port 8000 already in use
# - Insufficient memory (need 2GB+)
```

**Frontend build fails:**
```bash
# Check Node.js version (need 18+)
docker-compose logs frontend

# Clear cache and rebuild
docker-compose down
docker-compose up --build
```

**Database errors:**
```bash
# Reset database (WARNING: deletes all data)
rm data/fintech_ai.db
docker-compose restart backend
```

**Performance issues:**
```bash
# Increase Uvicorn workers
# In .env: UVICORN_WORKERS=4

# Check resource usage
docker stats
```

### Traditional Deployment (Without Docker)

For local development without Docker:

**Step 1: Backend Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run backend
python run_api.py
```

**Step 2: Frontend Setup**
```bash
# In a new terminal
cd frontend
npm install

# Configure API URL
# Create .env in frontend/ with:
# VITE_API_URL=http://localhost:8000

# Run frontend
npm run dev
```

**Step 3: Access**
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

### Cloud Deployment

#### AWS ECS/Fargate
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ECR_URI
docker build -t fintech-ai-backend .
docker tag fintech-ai-backend:latest YOUR_ECR_URI/fintech-ai-backend:latest
docker push YOUR_ECR_URI/fintech-ai-backend:latest

# Deploy via ECS console or CLI
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/fintech-ai-backend
gcloud run deploy fintech-ai-backend --image gcr.io/PROJECT_ID/fintech-ai-backend --platform managed --region us-central1 --allow-unauthenticated
```

#### DigitalOcean App Platform
```bash
# Use docker-compose.yml directly
# Configure via DigitalOcean console
```

#### Heroku
```bash
# Create app
heroku create fintech-ai-system

# Add buildpack
heroku buildpacks:set heroku/python

# Set environment variables
heroku config:set FRED_API_KEY=your_key

# Deploy
git push heroku main
```

---

## Testing

### Run Full Test Suite

```bash
# Test sentiment analyzer
python test_sentiment.py

# Test end-to-end pipeline
python test_pipeline.py

# Test database
python backend/database.py

# Test individual agents
python agents/sentiment_analyzer.py
python agents/earnings_fetcher.py
python agents/macro_detector.py
```

### Docker Test Environment
```bash
# Run tests in Docker
docker-compose run --rm backend python -m pytest tests/ -v

# Or use deploy script
./deploy.sh test
```

### Current Test Coverage
- ✅ Sentiment analysis (bullish/bearish/neutral)
- ✅ Macro regime detection
- ✅ Database CRUD operations
- ✅ Full pipeline integration
- ✅ Report generation
- ✅ API endpoints
- ✅ Docker builds

---

## Database Schema

### Companies
```sql
ticker (PK), name, sector, market_cap, created_at, updated_at
```

### Earnings Calls
```sql
id (PK), ticker (FK), call_date, quarter, fiscal_year,
transcript_text, sentiment_score, macro_regime, created_at
```

### Analysis Results
```sql
id (PK), call_id (FK), sentiment_label, confidence,
sentiment_distribution, key_quotes, macro_regime,
macro_confidence, recommendation, timestamp
```

---

## Contributing

This is a personal learning project, but feedback and suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## Status

🟢 **Production Ready** - Full-Stack Platform with Docker Deployment!

### Completed
- [x] Project setup
- [x] Sentiment analysis agent (FinBERT)
- [x] Macro regime detector (VIX + FRED)
- [x] Market data integration (yfinance)
- [x] Database infrastructure (SQLite)
- [x] Analysis orchestrator
- [x] CLI interface (Rich)
- [x] FastAPI REST API
- [x] React web dashboard (Bloomberg Terminal design)
- [x] Backtesting engine
- [x] Alert system with email notifications
- [x] Docker containerization
- [x] Docker Compose orchestration
- [x] Automated deployment scripts
- [x] Production nginx configuration
- [x] End-to-end testing

### In Progress
- [ ] Real earnings transcript fetching (Alpha Vantage/SEC EDGAR)
- [ ] Historical sentiment trend charts
- [ ] Portfolio watchlists
- [ ] SSL/TLS for production
- [ ] CI/CD pipeline (GitHub Actions)

**Last Updated:** October 31, 2025

---

## License

MIT License - See LICENSE file for details

---

## Acknowledgments

- **ProsusAI** for FinBERT model
- **HuggingFace** for Transformers library
- **Rich** for beautiful CLI
- Financial Twitter community for inspiration

---

**Built with ❤️ by building in public**
