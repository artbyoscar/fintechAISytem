# FastAPI Guide - Fintech AI System

## Quick Start

### Start the Server

```bash
# Activate virtual environment
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Start server
python run_api.py

# Server will be running at:
# http://127.0.0.1:8000
```

### Interactive Documentation

Once the server is running:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## API Endpoints

### 1. Root - API Information

```bash
GET /
```

**Response:**
```json
{
  "success": true,
  "data": {
    "name": "Fintech AI System API",
    "version": "1.0.0",
    "endpoints": {...}
  }
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/
```

---

### 2. Health Check

```bash
GET /health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "database_connected": true,
    "models_loaded": true,
    "api_keys_configured": {
      "alpha_vantage": true,
      "fred_api": true,
      "anthropic": true
    }
  }
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/health
```

---

### 3. Analyze Company

```bash
POST /analyze
Content-Type: application/json
```

**Request Body:**
```json
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
    "company": "Apple Inc.",
    "sentiment_analysis": {
      "overall_label": "positive",
      "sentiment_score": 0.895,
      "confidence": 0.910
    },
    "macro_regime": {
      "regime": "BULL",
      "confidence": 0.875
    },
    "overall_assessment": {
      "verdict": "STRONG BUY"
    }
  }
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'
```

---

### 4. List Companies

```bash
GET /companies
```

**Response:**
```json
{
  "success": true,
  "data": {
    "count": 3,
    "companies": [
      {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "analysis_count": 1,
        "latest_call_date": "2025-10-28",
        "avg_sentiment": 0.895
      }
    ]
  }
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/companies
```

---

### 5. Get Recent Analyses

```bash
GET /recent?limit=10
```

**Query Parameters:**
- `limit` (optional): Number of results (1-100, default: 10)

**Response:**
```json
{
  "success": true,
  "data": {
    "count": 3,
    "analyses": [
      {
        "call": {...},
        "analysis": {...}
      }
    ]
  }
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/recent?limit=5
```

---

### 6. Get Company Details

```bash
GET /company/{ticker}
```

**Path Parameters:**
- `ticker`: Stock ticker symbol

**Response:**
```json
{
  "success": true,
  "data": {
    "ticker": "AAPL",
    "company_name": "Apple Inc.",
    "count": 1,
    "analyses": [...]
  }
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/company/AAPL
```

---

### 7. Database Statistics

```bash
GET /stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_companies": 3,
    "total_calls": 3,
    "total_analyses": 3,
    "regime_distribution": {
      "BULL": 3
    }
  }
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/stats
```

---

## Response Format

All endpoints follow this standard format:

```json
{
  "success": true/false,
  "data": {...},
  "error": "Error message (if success=false)",
  "timestamp": "2025-10-31T18:00:00"
}
```

---

## Error Handling

### Error Response

```json
{
  "success": false,
  "data": null,
  "error": "Detailed error message",
  "timestamp": "2025-10-31T18:00:00"
}
```

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable

---

## Testing

### Run Test Suite

```bash
# Make sure server is running first
python run_api.py

# In another terminal
python test_api.py
```

### Manual Testing with curl

```bash
# Test health
curl http://127.0.0.1:8000/health

# Analyze company
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "NVDA"}'

# Get recent
curl http://127.0.0.1:8000/recent

# Get stats
curl http://127.0.0.1:8000/stats
```

### Testing with Python

```python
import requests

# Health check
response = requests.get("http://127.0.0.1:8000/health")
print(response.json())

# Analyze company
response = requests.post(
    "http://127.0.0.1:8000/analyze",
    json={"ticker": "AAPL"}
)
print(response.json())
```

---

## Development

### Enable Auto-Reload

The server automatically reloads when code changes in development mode:

```python
# In .env
ENVIRONMENT=development
```

### Logging

Logs are written to:
- Console (in development)
- `data/fintech_ai.log` (file)

Control log level in `.env`:
```
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

---

## Configuration

### CORS Settings

Configure allowed origins in `.env`:
```
CORS_ORIGINS=*  # Allow all (development)
CORS_ORIGINS=https://example.com,https://app.example.com  # Production
```

### Server Settings

```
API_HOST=127.0.0.1
API_PORT=8000
```

---

## Production Deployment

### 1. Update Configuration

```bash
# .env
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING
CORS_ORIGINS=https://yourdomain.com
```

### 2. Run with Gunicorn (Linux/Mac)

```bash
pip install gunicorn
gunicorn backend.api:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 3. Run with Docker

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Next Steps

1. **Frontend Integration**: Build React/Vue dashboard
2. **Real-time Updates**: Add WebSocket support
3. **Authentication**: Add JWT authentication
4. **Rate Limiting**: Implement request throttling
5. **Caching**: Add Redis for performance
6. **Monitoring**: Integrate Prometheus/Grafana

---

## Troubleshooting

### Server Won't Start

```bash
# Check if port is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Kill process if needed
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # Linux/Mac
```

### Module Not Found

```bash
# Ensure virtual environment is activated
source venv/Scripts/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Database Errors

```bash
# Reset database
rm data/fintech_ai.db

# Restart server (will recreate tables)
python run_api.py
```

---

## Support

- **Documentation**: http://127.0.0.1:8000/docs
- **Source Code**: Check README.md
- **Issues**: Create GitHub issue

---

**Built with FastAPI, FinBERT, and ❤️**
