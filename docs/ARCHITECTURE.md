# System Architecture

## Overview

The Fintech AI System is a production-grade earnings analysis platform that combines state-of-the-art NLP with macroeconomic intelligence to generate actionable trading signals.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Frontend Layer                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐   │
│  │   Dashboard      │  │   Analytics      │  │   Visualizations│   │
│  │   (React/Vite)   │  │   (Recharts)     │  │   (CSV/PDF)     │   │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬────────┘   │
│           │                     │                      │             │
│           └─────────────────────┴──────────────────────┘             │
│                                 │                                    │
│                          REST API (Axios)                            │
└─────────────────────────────────┼────────────────────────────────────┘
                                  │
┌─────────────────────────────────┼────────────────────────────────────┐
│                          Backend Layer                               │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    FastAPI REST Server                        │  │
│  │  /analyze  /recent  /health  /stats  /backtest  /signals     │  │
│  └────────────────────────────┬──────────────────────────────────┘  │
│                               │                                      │
│  ┌────────────────────────────┴─────────────────────────────────┐  │
│  │              Analysis Orchestrator (Pipeline)                 │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │  │
│  │  │  Step 1  │→ │  Step 2  │→ │  Step 3  │→ │  Step 4  │     │  │
│  │  │ Earnings │  │Sentiment │  │  Macro   │  │ Signal   │     │  │
│  │  │  Fetch   │  │ Analysis │  │ Regime   │  │   Gen    │     │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │  │
│  └────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬──────────────────────────────────┘
                                    │
┌───────────────────────────────────┼──────────────────────────────────┐
│                          AI/ML Layer                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐    │
│  │  FinBERT Model  │  │  Macro Detector │  │  Signal Generator│    │
│  │  (ProsusAI)     │  │  (FRED API)     │  │  (Multi-factor)  │    │
│  │  PyTorch/Transformers│  VIX, CPI, UN │  │  Risk Analysis   │    │
│  └─────────────────┘  └─────────────────┘  └──────────────────┘    │
└───────────────────────────────────┬──────────────────────────────────┘
                                    │
┌───────────────────────────────────┼──────────────────────────────────┐
│                          Data Layer                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐    │
│  │  SQLite DB      │  │  Market Data    │  │  Alert System    │    │
│  │  - Companies    │  │  - yfinance     │  │  - Email SMTP    │    │
│  │  - Earnings     │  │  - Alpha Vantage│  │  - History Log   │    │
│  │  - Analyses     │  │  - FRED         │  │  - Templates     │    │
│  │  - Signals      │  └─────────────────┘  └──────────────────┘    │
│  └─────────────────┘                                                 │
└───────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Frontend (React + Vite)

**Technology Stack:**
- React 18 with Hooks
- Vite for blazing-fast development
- Tailwind CSS for utility-first styling
- Recharts for data visualization
- React Router for navigation
- jsPDF for report generation

**Key Features:**
- Bloomberg Terminal-inspired dark theme
- Real-time API status monitoring
- Interactive sentiment analysis dashboard
- Analytics page with multiple chart types
- CSV/PDF export functionality
- Responsive design for all screen sizes

**Component Architecture:**
```
src/
├── components/          # Reusable UI components
│   ├── TickerSearch.jsx
│   ├── SentimentCard.jsx
│   ├── MacroRegimeCard.jsx
│   ├── AnalysisResults.jsx
│   ├── RecentAnalyses.jsx
│   └── MetricsChart.jsx
├── pages/              # Route-based pages
│   └── Analytics.jsx
├── api.js              # API client with axios
└── App.jsx             # Main app with routing
```

### 2. Backend (FastAPI)

**Technology Stack:**
- FastAPI for async REST API
- Uvicorn ASGI server
- Pydantic for data validation
- SQLite for persistence
- Python 3.11+

**API Endpoints:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | System health check |
| `/analyze` | POST | Analyze company earnings |
| `/recent` | GET | Get recent analyses |
| `/company/{ticker}` | GET | Get company details |
| `/companies` | GET | List all companies |
| `/stats` | GET | Database statistics |
| `/backtest/{ticker}` | POST | Run backtest for ticker |
| `/signals/{ticker}` | GET | Get trading signals |

**Request Flow:**
1. Client sends POST to `/analyze` with ticker
2. Orchestrator coordinates 4-step pipeline
3. Results stored in SQLite database
4. JSON report generated and returned
5. Alert system checks for trigger conditions

### 3. AI/ML Pipeline

**Step 1: Earnings Transcript Fetching**
- Source: Mock data (production: Alpha Vantage/SEC EDGAR)
- Extracts quarterly earnings call transcripts
- Validates data quality and completeness

**Step 2: Sentiment Analysis (FinBERT)**
- Model: `ProsusAI/finbert` (specialized for financial text)
- Architecture: BERT-base fine-tuned on financial corpus
- Processing:
  - Sentence-level sentiment classification
  - Confidence scoring for each prediction
  - Weighted aggregation for overall sentiment
  - Key quote extraction (top 3 most significant)
- Output: Sentiment score (-1 to +1), label, confidence

**Step 3: Macro Regime Detection**
- Indicators:
  - VIX (Volatility Index) - market fear gauge
  - Unemployment Rate - economic health
  - CPI (Inflation) - purchasing power
- Classification Logic:
  ```python
  if vix < 20 and unemployment < 5% and inflation < 3%:
      regime = "BULL"  # Low risk, growing economy
  elif vix > 30 or unemployment > 7% or inflation > 5%:
      regime = "BEAR"  # High risk, contracting economy
  else:
      regime = "SIDEWAYS"  # Mixed signals
  ```
- Confidence: Statistical measure based on indicator strength

**Step 4: Trading Signal Generation**
- Multi-factor analysis combining:
  - Sentiment score and confidence
  - Macro regime classification
  - Market data (price, volume, volatility)
- Signal types: BUY, SELL, HOLD
- Position sizing: 1-10 scale based on conviction
- Risk score: 0-1 continuous measure
- Validation rules prevent risky trades

**Step 5: Alert System**
- Monitors for 5 alert types:
  1. Extreme sentiment (|score| > 0.8)
  2. Sentiment-macro divergence
  3. Regime change detection
  4. High confidence signals (>0.9)
  5. Trading signal triggers
- Email notifications (SMTP)
- Alert history tracking in database

### 4. Data Layer

**Database Schema:**

```sql
-- Companies table
CREATE TABLE companies (
    ticker TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    sector TEXT,
    market_cap REAL,
    last_updated TIMESTAMP
);

-- Earnings calls table
CREATE TABLE earnings_calls (
    id INTEGER PRIMARY KEY,
    ticker TEXT NOT NULL,
    call_date DATE,
    quarter TEXT,
    fiscal_year INTEGER,
    transcript TEXT,
    sentiment_score REAL,
    macro_regime TEXT,
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
);

-- Analysis results table
CREATE TABLE analysis_results (
    id INTEGER PRIMARY KEY,
    call_id INTEGER NOT NULL,
    sentiment_label TEXT,
    confidence REAL,
    sentiment_distribution TEXT,
    key_quotes TEXT,
    macro_regime TEXT,
    macro_confidence REAL,
    recommendation TEXT,
    timestamp TIMESTAMP,
    FOREIGN KEY (call_id) REFERENCES earnings_calls(id)
);

-- Trading signals table
CREATE TABLE trading_signals (
    id INTEGER PRIMARY KEY,
    ticker TEXT NOT NULL,
    call_id INTEGER,
    signal TEXT NOT NULL,
    confidence REAL,
    reasoning TEXT,
    position_size INTEGER,
    risk_score REAL,
    sentiment_score REAL,
    macro_regime TEXT,
    validation_notes TEXT,
    timestamp TIMESTAMP,
    FOREIGN KEY (ticker) REFERENCES companies(ticker),
    FOREIGN KEY (call_id) REFERENCES earnings_calls(id)
);
```

**Data Flow:**
1. Analysis results stored in `analysis_results` table
2. Trading signals stored in `trading_signals` table
3. JSON reports saved to `data/analysis_reports/`
4. Alert history logged to `data/alerts/`

## Design Patterns

### 1. Orchestrator Pattern
The `AnalysisOrchestrator` coordinates all AI agents in a sequential pipeline:
- Separation of concerns (each agent is independent)
- Error handling at each step
- Performance timing for optimization
- Easy to add new analysis steps

### 2. Repository Pattern
The `Database` class abstracts all SQL operations:
- Single source of truth for data access
- Prevents SQL injection
- Easy to switch database backends
- Centralized error handling

### 3. Factory Pattern
Agent initialization in orchestrator:
- Lazy loading of ML models
- Singleton pattern for model instances
- Resource management and cleanup

### 4. Strategy Pattern
Signal generation uses different strategies:
- Sentiment-based strategy
- Macro-based strategy
- Combined multi-factor strategy
- Easy to add new signal strategies

## Performance Characteristics

### Latency
- Cold start (model loading): ~2-3 seconds
- Warm analysis: ~500ms per company
- Sentiment analysis: ~300-500ms (11 sentences)
- Macro regime detection: <50ms
- Database operations: <10ms

### Throughput
- Single-threaded: ~2 analyses per second
- With workers: ~10+ analyses per second
- Batch processing: 100+ companies in <2 minutes

### Resource Usage
- RAM: ~2GB (FinBERT model loaded)
- CPU: Moderate (PyTorch inference)
- Storage: ~50MB per 1000 analyses
- GPU: Optional (10x speedup for batch processing)

## Scalability Considerations

### Horizontal Scaling
- FastAPI supports async/await for concurrency
- Stateless API design allows multiple instances
- Load balancer (nginx) distributes requests
- Shared SQLite → migrate to PostgreSQL for production

### Vertical Scaling
- GPU acceleration for FinBERT inference
- Model quantization (FP16) reduces memory 50%
- Batch processing for multiple tickers
- Caching layer (Redis) for frequent queries

### Future Optimizations
- [ ] Model serving with TensorRT/ONNX
- [ ] Distributed task queue (Celery)
- [ ] CDN for frontend static assets
- [ ] Database connection pooling
- [ ] Rate limiting and API keys

## Security

### Current Implementation
- Environment variables for API keys
- No sensitive data in git repository
- CORS configuration for API access
- Input validation with Pydantic

### Production Recommendations
- [ ] Add JWT authentication
- [ ] Implement rate limiting (per IP/user)
- [ ] HTTPS/TLS encryption
- [ ] API key rotation mechanism
- [ ] Database encryption at rest
- [ ] Audit logging for all operations
- [ ] OWASP security headers

## Testing Strategy

### Unit Tests (pytest)
- `test_sentiment.py`: 15 tests for sentiment analyzer
- `test_macro.py`: 17 tests for macro detector
- `test_orchestrator.py`: 16 tests for pipeline
- `test_api.py`: 28 tests for API endpoints
- `test_backtester.py`: 17 tests for backtest engine

### Test Coverage
- Target: >80% code coverage
- Current: ~75% (run `pytest --cov`)
- Critical paths: 100% coverage

### Integration Testing
- End-to-end API tests with TestClient
- Database transaction rollback for isolation
- Mock external API calls (Alpha Vantage, FRED)

### Performance Testing
- Load testing with locust/k6
- Benchmark model inference times
- Database query optimization

## Deployment Architecture

### Development
```
Local Machine
├── Frontend (Vite dev server) :3000
├── Backend (Uvicorn reload) :8000
└── SQLite database (local file)
```

### Production (Docker)
```
Docker Host
├── Nginx (reverse proxy) :80
├── Backend (2 workers) :8000
├── Frontend (static build) :3000
└── Volumes (SQLite, reports)
```

### Cloud Deployment Options

**Option 1: Single VPS (DigitalOcean/AWS EC2)**
- Cost: $10-50/month
- Setup: Docker Compose
- Scale: Up to 1000 requests/day
- Best for: MVP, small teams

**Option 2: Serverless (AWS Lambda/Cloud Run)**
- Cost: Pay per request
- Setup: Container deployment
- Scale: Auto-scaling to millions
- Best for: Variable traffic

**Option 3: Kubernetes (EKS/GKE)**
- Cost: $100+/month
- Setup: Helm charts
- Scale: Enterprise-grade
- Best for: Production at scale

## Monitoring & Observability

### Logging
- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR
- Centralized logging (CloudWatch/Datadog)

### Metrics
- API response times
- Model inference latency
- Database query performance
- Error rates by endpoint

### Alerts
- Email alerts for extreme sentiment
- Slack notifications for system errors
- PagerDuty for critical failures

## Tech Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 | UI framework |
| Build Tool | Vite | Fast development |
| Styling | Tailwind CSS | Utility-first CSS |
| Charts | Recharts | Data visualization |
| Backend | FastAPI | REST API server |
| AI/ML | PyTorch + Transformers | Deep learning |
| NLP Model | FinBERT | Financial sentiment |
| Database | SQLite | Persistence |
| Testing | pytest | Unit/integration tests |
| Deployment | Docker | Containerization |
| Reverse Proxy | Nginx | Load balancing |
| Market Data | yfinance, Alpha Vantage | Real-time quotes |
| Macro Data | FRED API | Economic indicators |

## Development Workflow

1. **Feature Development**
   ```bash
   git checkout -b feature/new-feature
   # Make changes
   pytest tests/
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

2. **Code Review**
   - Pull request on GitHub
   - Automated tests run (CI/CD)
   - Code review by maintainer
   - Merge to main

3. **Deployment**
   ```bash
   ./deploy.sh
   # Builds Docker images
   # Runs tests
   # Deploys to production
   ```

## Future Architecture Enhancements

### Short Term (1-3 months)
- [ ] WebSocket support for real-time updates
- [ ] PostgreSQL migration for production
- [ ] Redis caching layer
- [ ] Prometheus metrics

### Medium Term (3-6 months)
- [ ] Microservices architecture
  - Sentiment service
  - Macro service
  - Signal service
- [ ] Message queue (RabbitMQ/Kafka)
- [ ] GraphQL API alongside REST

### Long Term (6-12 months)
- [ ] Multi-region deployment
- [ ] Kubernetes orchestration
- [ ] Machine learning pipeline (MLOps)
- [ ] A/B testing framework
- [ ] Data lake for historical analysis

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FinBERT Paper](https://arxiv.org/abs/1908.10063)
- [BERT Model](https://arxiv.org/abs/1810.04805)
- [Twelve-Factor App](https://12factor.net/)
- [REST API Design](https://restfulapi.net/)
