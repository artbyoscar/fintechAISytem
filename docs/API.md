# API Documentation

## Base URL

```
Development: http://localhost:8000
Production: https://api.yourdomain.com
```

## Authentication

Currently, the API is open for development. Production deployment should implement API keys or JWT tokens.

**Future Authentication Header:**
```
Authorization: Bearer YOUR_API_KEY
```

## Response Format

All API responses follow this standard format:

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

### Success Response
```json
{
  "success": true,
  "data": {
    // Response payload here
  },
  "error": null,
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

### Error Response
```json
{
  "success": false,
  "data": null,
  "error": "Error message describing what went wrong",
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

## Endpoints

### 1. Health Check

Check API server health and configuration status.

**Endpoint:** `GET /health`

**Request:**
```bash
curl -X GET http://localhost:8000/health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "environment": "development",
    "database_connected": true,
    "models_loaded": true,
    "api_keys_configured": {
      "alpha_vantage": true,
      "fred_api": true,
      "anthropic": true
    }
  },
  "error": null,
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

**Status Codes:**
- `200 OK` - System is healthy
- `503 Service Unavailable` - System is degraded

---

### 2. Analyze Company

Analyze a company's earnings call and generate sentiment + trading signals.

**Endpoint:** `POST /analyze`

**Request Body:**
```json
{
  "ticker": "AAPL"
}
```

**Request Example:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "ticker": "AAPL",
    "company_name": "Apple Inc.",
    "call_date": "2024-10-28",
    "quarter": "Q4 2024",
    "fiscal_year": 2024,
    "sentiment": {
      "overall_label": "positive",
      "sentiment_score": 0.8949,
      "confidence": 0.9102,
      "sentiment_distribution": {
        "positive": 100.0,
        "negative": 0.0,
        "neutral": 0.0
      },
      "key_quotes": [
        "[POSITIVE] Revenue grew by 20% year over year...",
        "[POSITIVE] Our Services gross margin expanded to 72%...",
        "[POSITIVE] iPhone revenue was $43.8 billion, up 3%..."
      ]
    },
    "macro_regime": {
      "regime": "BULL",
      "confidence": 0.875,
      "indicators": {
        "vix": 18.5,
        "unemployment_rate": 3.8,
        "inflation_rate": 3.2
      },
      "recommendation": "FAVORABLE"
    },
    "trading_signal": {
      "signal": "BUY",
      "confidence": 0.89,
      "position_size": 8,
      "risk_score": 0.23,
      "reasoning": "Strong positive sentiment (89.5%) combined with bullish macro regime. High confidence trade.",
      "validation_notes": "Signal approved - all risk checks passed"
    },
    "alerts": [],
    "analysis_timestamp": "2025-11-01T12:00:00",
    "performance": {
      "total_time": 0.52,
      "fetch_time": 0.00,
      "sentiment_time": 0.51,
      "macro_time": 0.00,
      "signal_time": 0.01
    }
  },
  "error": null,
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

**Status Codes:**
- `200 OK` - Analysis completed successfully
- `400 Bad Request` - Invalid ticker or missing parameters
- `404 Not Found` - No earnings data found for ticker
- `500 Internal Server Error` - Analysis failed

---

### 3. Get Recent Analyses

Retrieve the most recent earnings analyses.

**Endpoint:** `GET /recent`

**Query Parameters:**
- `limit` (optional, default: 10) - Number of results to return (max: 100)

**Request:**
```bash
curl -X GET "http://localhost:8000/recent?limit=5"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "count": 5,
    "analyses": [
      {
        "call": {
          "id": 1,
          "ticker": "AAPL",
          "call_date": "2024-10-28",
          "quarter": "Q4 2024",
          "fiscal_year": 2024,
          "sentiment_score": 0.8949,
          "macro_regime": "BULL",
          "company_name": "Apple Inc.",
          "sector": "Technology"
        },
        "analysis": {
          "id": 1,
          "call_id": 1,
          "sentiment_label": "positive",
          "confidence": 0.9102,
          "sentiment_distribution": {
            "positive": 100.0,
            "negative": 0.0,
            "neutral": 0.0
          },
          "key_quotes": ["..."],
          "macro_regime": "BULL",
          "macro_confidence": 0.875,
          "recommendation": "FAVORABLE",
          "timestamp": "2025-11-01T12:00:00"
        }
      }
      // ... 4 more analyses
    ]
  },
  "error": null,
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

**Status Codes:**
- `200 OK` - Results returned
- `400 Bad Request` - Invalid limit parameter

---

### 4. Get Company Details

Retrieve detailed information and analysis history for a specific company.

**Endpoint:** `GET /company/{ticker}`

**Path Parameters:**
- `ticker` (required) - Stock ticker symbol (e.g., "AAPL")

**Query Parameters:**
- `limit` (optional, default: 5) - Number of analyses to return

**Request:**
```bash
curl -X GET "http://localhost:8000/company/AAPL?limit=3"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "company": {
      "ticker": "AAPL",
      "name": "Apple Inc.",
      "sector": "Technology",
      "market_cap": 3000000000000,
      "last_updated": "2025-11-01T12:00:00"
    },
    "analyses_count": 15,
    "recent_analyses": [
      {
        "call_date": "2024-10-28",
        "quarter": "Q4 2024",
        "sentiment_label": "positive",
        "sentiment_score": 0.8949,
        "macro_regime": "BULL",
        "recommendation": "FAVORABLE"
      }
      // ... 2 more analyses
    ],
    "sentiment_trend": {
      "avg_sentiment": 0.72,
      "sentiment_volatility": 0.15,
      "positive_ratio": 0.80,
      "recent_direction": "improving"
    }
  },
  "error": null,
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

**Status Codes:**
- `200 OK` - Company found
- `404 Not Found` - Company not in database

---

### 5. List All Companies

Get list of all companies in the database.

**Endpoint:** `GET /companies`

**Request:**
```bash
curl -X GET http://localhost:8000/companies
```

**Response:**
```json
{
  "success": true,
  "data": {
    "count": 50,
    "companies": [
      {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "analyses_count": 15,
        "last_analysis": "2025-11-01T12:00:00"
      },
      {
        "ticker": "MSFT",
        "name": "Microsoft Corporation",
        "sector": "Technology",
        "analyses_count": 12,
        "last_analysis": "2025-10-30T10:00:00"
      }
      // ... more companies
    ]
  },
  "error": null,
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

**Status Codes:**
- `200 OK` - Companies list returned

---

### 6. Get Database Statistics

Retrieve overall system statistics and performance metrics.

**Endpoint:** `GET /stats`

**Request:**
```bash
curl -X GET http://localhost:8000/stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_companies": 50,
    "total_earnings_calls": 200,
    "total_analyses": 200,
    "total_signals": 180,
    "sentiment_distribution": {
      "positive": 120,
      "negative": 40,
      "neutral": 40
    },
    "regime_distribution": {
      "BULL": 150,
      "BEAR": 30,
      "SIDEWAYS": 20
    },
    "signal_distribution": {
      "BUY": 100,
      "SELL": 30,
      "HOLD": 50
    },
    "avg_sentiment_score": 0.65,
    "avg_confidence": 0.82,
    "database_size_mb": 45.2,
    "last_analysis": "2025-11-01T12:00:00"
  },
  "error": null,
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

**Status Codes:**
- `200 OK` - Statistics returned

---

### 7. Run Backtest

Run historical backtest for a ticker to validate prediction accuracy.

**Endpoint:** `POST /backtest/{ticker}`

**Path Parameters:**
- `ticker` (required) - Stock ticker symbol

**Request Body (optional):**
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

**Request:**
```bash
curl -X POST http://localhost:8000/backtest/AAPL \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2024-01-01", "end_date": "2024-12-31"}'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "ticker": "AAPL",
    "period": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    },
    "metrics": {
      "total_predictions": 15,
      "accuracy_1d": 73.3,
      "accuracy_5d": 80.0,
      "accuracy_30d": 86.7,
      "win_rate": 75.0,
      "sharpe_ratio": 1.85,
      "max_drawdown": -12.5
    },
    "performance_by_sentiment": {
      "positive": {
        "count": 10,
        "accuracy": 80.0,
        "avg_return": 3.2
      },
      "negative": {
        "count": 3,
        "accuracy": 66.7,
        "avg_return": -2.1
      },
      "neutral": {
        "count": 2,
        "accuracy": 50.0,
        "avg_return": 0.5
      }
    },
    "best_predictions": [
      {
        "date": "2024-07-15",
        "sentiment": "positive",
        "prediction": "BUY",
        "actual_return_5d": 8.5
      }
    ],
    "worst_predictions": [
      {
        "date": "2024-03-22",
        "sentiment": "positive",
        "prediction": "BUY",
        "actual_return_5d": -3.2
      }
    ]
  },
  "error": null,
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

**Status Codes:**
- `200 OK` - Backtest completed
- `404 Not Found` - No data for ticker in date range
- `400 Bad Request` - Invalid date range

---

### 8. Get Trading Signals

Retrieve trading signals for a specific ticker.

**Endpoint:** `GET /signals/{ticker}`

**Path Parameters:**
- `ticker` (required) - Stock ticker symbol

**Query Parameters:**
- `limit` (optional, default: 10) - Number of signals to return
- `signal_type` (optional) - Filter by signal type: "BUY", "SELL", "HOLD"

**Request:**
```bash
curl -X GET "http://localhost:8000/signals/AAPL?limit=5&signal_type=BUY"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "ticker": "AAPL",
    "count": 5,
    "signals": [
      {
        "id": 1,
        "signal": "BUY",
        "confidence": 0.89,
        "position_size": 8,
        "risk_score": 0.23,
        "reasoning": "Strong positive sentiment combined with bullish regime",
        "sentiment_score": 0.8949,
        "sentiment_label": "positive",
        "macro_regime": "BULL",
        "validation_notes": "Signal approved",
        "timestamp": "2025-11-01T12:00:00"
      }
      // ... 4 more signals
    ],
    "signal_stats": {
      "total_signals": 25,
      "buy_signals": 15,
      "sell_signals": 5,
      "hold_signals": 5,
      "avg_confidence": 0.82,
      "avg_position_size": 6.5
    }
  },
  "error": null,
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

**Status Codes:**
- `200 OK` - Signals returned
- `404 Not Found` - No signals found for ticker

---

### 9. API Root

Get API information and available endpoints.

**Endpoint:** `GET /`

**Request:**
```bash
curl -X GET http://localhost:8000/
```

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "Fintech AI System API",
    "version": "1.0.0",
    "description": "Earnings sentiment analysis with macro-aware trading signals",
    "environment": "development",
    "documentation": "http://localhost:8000/docs",
    "endpoints": {
      "health": "/health",
      "analyze": "/analyze",
      "recent": "/recent",
      "company": "/company/{ticker}",
      "companies": "/companies",
      "stats": "/stats",
      "backtest": "/backtest/{ticker}",
      "signals": "/signals/{ticker}"
    }
  },
  "error": null,
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

---

## Interactive Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These interfaces allow you to:
- Test all API endpoints directly from the browser
- View detailed request/response schemas
- Understand parameter requirements
- See example requests and responses

## Rate Limiting

**Current:** No rate limiting (development)

**Production Recommendations:**
- 100 requests per minute per IP
- 1000 requests per day per API key
- Burst allowance: 10 requests per second

## Error Codes

| Status Code | Meaning | Common Causes |
|-------------|---------|---------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters, malformed JSON |
| 404 | Not Found | Ticker not in database, no data |
| 422 | Validation Error | Missing required fields |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error, model failure |
| 503 | Service Unavailable | Database offline, model not loaded |

## Common Error Messages

### Invalid Ticker
```json
{
  "success": false,
  "data": null,
  "error": "Invalid ticker symbol. Must be 1-5 uppercase letters.",
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

### Database Error
```json
{
  "success": false,
  "data": null,
  "error": "Database connection failed. Please try again.",
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

### Model Not Loaded
```json
{
  "success": false,
  "data": null,
  "error": "ML models not initialized. Server is starting up.",
  "timestamp": "2025-11-01T12:00:00.000000"
}
```

## Client SDKs

### Python

```python
import requests

class FintechAIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def analyze(self, ticker):
        response = requests.post(
            f"{self.base_url}/analyze",
            json={"ticker": ticker}
        )
        return response.json()

    def get_recent(self, limit=10):
        response = requests.get(
            f"{self.base_url}/recent",
            params={"limit": limit}
        )
        return response.json()

# Usage
client = FintechAIClient()
result = client.analyze("AAPL")
print(result["data"]["sentiment"]["overall_label"])
```

### JavaScript

```javascript
class FintechAIClient {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
  }

  async analyze(ticker) {
    const response = await fetch(`${this.baseURL}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ticker })
    });
    return response.json();
  }

  async getRecent(limit = 10) {
    const response = await fetch(
      `${this.baseURL}/recent?limit=${limit}`
    );
    return response.json();
  }
}

// Usage
const client = new FintechAIClient();
const result = await client.analyze('AAPL');
console.log(result.data.sentiment.overall_label);
```

### cURL Examples

**Analyze Multiple Companies:**
```bash
#!/bin/bash
for ticker in AAPL MSFT GOOGL AMZN; do
  echo "Analyzing $ticker..."
  curl -s -X POST http://localhost:8000/analyze \
    -H "Content-Type: application/json" \
    -d "{\"ticker\": \"$ticker\"}" | python -m json.tool
  sleep 1
done
```

**Export Recent Analyses:**
```bash
curl -s "http://localhost:8000/recent?limit=100" | \
  python -c "
import sys, json, csv
data = json.load(sys.stdin)
writer = csv.writer(sys.stdout)
writer.writerow(['Ticker', 'Date', 'Sentiment', 'Score', 'Regime'])
for item in data['data']['analyses']:
    call = item['call']
    analysis = item['analysis']
    writer.writerow([
        call['ticker'],
        call['call_date'],
        analysis['sentiment_label'],
        analysis['confidence'],
        analysis['macro_regime']
    ])
" > analyses.csv
```

## Webhooks (Future Feature)

Subscribe to real-time alerts when specific conditions are met.

**Endpoint:** `POST /webhooks/subscribe`

**Request:**
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["extreme_sentiment", "regime_change", "signal_generated"],
  "filters": {
    "tickers": ["AAPL", "MSFT"],
    "min_confidence": 0.8
  }
}
```

## Changelog

### v1.0.0 (2025-11-01)
- Initial API release
- 9 core endpoints
- Sentiment analysis with FinBERT
- Macro regime detection
- Trading signal generation
- Backtesting functionality

### Future Versions
- v1.1.0: Add authentication (API keys)
- v1.2.0: Add rate limiting
- v1.3.0: Add webhooks
- v2.0.0: GraphQL API alongside REST

## Support

- **Documentation:** https://docs.yourdomain.com
- **Issues:** https://github.com/yourusername/fintech-ai/issues
- **Email:** support@yourdomain.com
- **Discord:** https://discord.gg/yourserver
