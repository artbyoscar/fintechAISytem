# Deployment Guide

Complete guide for deploying the Fintech AI System to production.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Development Deployment](#development-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Checklist](#production-checklist)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

- **Python 3.11+** - Backend runtime
- **Node.js 18+** - Frontend development
- **Git** - Version control
- **Docker** (optional) - Containerization
- **Docker Compose** (optional) - Multi-container orchestration

### Required API Keys

You'll need API keys for the following services:

1. **FRED API** (Federal Reserve Economic Data)
   - Free, no credit card required
   - Sign up: https://fred.stlouisfed.org/docs/api/api_key.html
   - Used for: Macroeconomic indicators (VIX, CPI, unemployment)

2. **Alpha Vantage API**
   - Free tier: 25 requests/day
   - Sign up: https://www.alphavantage.co/support/#api-key
   - Used for: Market data and earnings transcripts (future feature)

3. **Anthropic API** (optional)
   - Used for: Advanced NLP features (future feature)
   - Sign up: https://www.anthropic.com/

## Environment Configuration

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/fintech-ai-system.git
cd fintech-ai-system
```

### 2. Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# API Keys
FRED_API_KEY=your_fred_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Database
DATABASE_PATH=data/fintech_ai.db

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=2
DEBUG=False

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Email Alerts (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL_FROM=alerts@yourdomain.com
ALERT_EMAIL_TO=your-email@gmail.com

# Security
SECRET_KEY=generate-a-random-secret-key-here
API_KEY_SALT=another-random-salt
```

**Generate Secret Keys:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Environment Variables Explanation

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `FRED_API_KEY` | FRED API key for macro data | Yes | None |
| `ALPHA_VANTAGE_API_KEY` | Alpha Vantage API key | Yes | None |
| `ANTHROPIC_API_KEY` | Anthropic API key | No | None |
| `DATABASE_PATH` | SQLite database file path | No | `data/fintech_ai.db` |
| `API_HOST` | Server bind address | No | `127.0.0.1` |
| `API_PORT` | Server port | No | `8000` |
| `API_WORKERS` | Number of Uvicorn workers | No | `1` |
| `DEBUG` | Enable debug mode | No | `False` |
| `CORS_ORIGINS` | Allowed CORS origins | No | `*` |

## Development Deployment

### Backend Setup

1. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate Virtual Environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Initialize Database:**
   ```bash
   python -c "from backend.database import Database; db = Database(); db.create_tables()"
   ```

5. **Start Backend Server:**
   ```bash
   python run_api.py
   ```

   Server will start on http://localhost:8000
   - API docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

### Frontend Setup

1. **Install Dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server:**
   ```bash
   npm run dev
   ```

   Frontend will start on http://localhost:3000

3. **Build for Production:**
   ```bash
   npm run build
   ```

   Output in `frontend/dist/`

## Docker Deployment

### Using Docker Compose (Recommended)

**1. Build and Start All Services:**
```bash
./deploy.sh
```

This script will:
- Build Docker images
- Run tests
- Start all services
- Display service URLs

**2. Manual Docker Compose:**

Start services:
```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f
```

Stop services:
```bash
docker-compose down
```

**3. Access Services:**
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Nginx (production): http://localhost:80

### Using Docker Manually

**Build Backend Image:**
```bash
docker build -t fintech-ai-backend .
```

**Run Backend Container:**
```bash
docker run -d \
  --name fintech-backend \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e FRED_API_KEY=$FRED_API_KEY \
  -e ALPHA_VANTAGE_API_KEY=$ALPHA_VANTAGE_API_KEY \
  fintech-ai-backend
```

**Build Frontend:**
```bash
cd frontend
npm run build
```

**Serve Frontend with Nginx:**
```bash
docker run -d \
  --name fintech-frontend \
  -p 80:80 \
  -v $(pwd)/frontend/dist:/usr/share/nginx/html \
  nginx:alpine
```

## Cloud Deployment

### Option 1: DigitalOcean Droplet

**1. Create Droplet:**
- Ubuntu 22.04 LTS
- 2 GB RAM minimum (4 GB recommended)
- $12-24/month

**2. SSH into Droplet:**
```bash
ssh root@your-droplet-ip
```

**3. Install Dependencies:**
```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Install git
apt install git -y
```

**4. Deploy Application:**
```bash
# Clone repository
git clone https://github.com/yourusername/fintech-ai-system.git
cd fintech-ai-system

# Create .env file
nano .env
# (paste your environment variables)

# Start services
docker-compose up -d --build

# Check logs
docker-compose logs -f
```

**5. Configure Domain (optional):**
```bash
# Install Nginx
apt install nginx -y

# Configure reverse proxy
nano /etc/nginx/sites-available/fintech-ai
```

Nginx config:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/fintech-ai /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

**6. SSL with Let's Encrypt:**
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d yourdomain.com
```

### Option 2: AWS EC2

**1. Launch EC2 Instance:**
- AMI: Amazon Linux 2 or Ubuntu 22.04
- Instance Type: t3.medium (2 vCPU, 4 GB RAM)
- Security Group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)

**2. Connect to Instance:**
```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

**3. Install Docker:**
```bash
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo usermod -a -G docker ec2-user
```

**4. Deploy (same as DigitalOcean steps 4-6)**

### Option 3: Google Cloud Run (Serverless)

**1. Build Container:**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/fintech-ai-backend
```

**2. Deploy Service:**
```bash
gcloud run deploy fintech-ai-backend \
  --image gcr.io/PROJECT_ID/fintech-ai-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FRED_API_KEY=$FRED_API_KEY \
  --memory 2Gi
```

**3. Deploy Frontend to Cloud Storage + CDN:**
```bash
# Build frontend
cd frontend && npm run build

# Upload to bucket
gsutil -m rsync -r dist/ gs://your-bucket-name

# Enable CDN
gcloud compute backend-buckets create fintech-frontend \
  --gcs-bucket-name=your-bucket-name \
  --enable-cdn
```

### Option 4: Heroku

**1. Create Heroku Apps:**
```bash
heroku create fintech-ai-backend
heroku create fintech-ai-frontend
```

**2. Add Buildpacks:**
```bash
# Backend
cd backend
heroku buildpacks:set heroku/python -a fintech-ai-backend

# Frontend
cd frontend
heroku buildpacks:set heroku/nodejs -a fintech-ai-frontend
```

**3. Set Environment Variables:**
```bash
heroku config:set FRED_API_KEY=your_key -a fintech-ai-backend
heroku config:set ALPHA_VANTAGE_API_KEY=your_key -a fintech-ai-backend
```

**4. Deploy:**
```bash
git push heroku main
```

## Production Checklist

### Security

- [ ] Set `DEBUG=False` in environment
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure CORS origins (no wildcards)
- [ ] Enable HTTPS/TLS encryption
- [ ] Implement API authentication (JWT/API keys)
- [ ] Set up rate limiting
- [ ] Configure security headers
- [ ] Enable database encryption
- [ ] Set up firewall rules
- [ ] Implement audit logging

### Performance

- [ ] Enable gzip compression
- [ ] Set up CDN for frontend assets
- [ ] Configure caching (Redis)
- [ ] Optimize database indexes
- [ ] Enable connection pooling
- [ ] Set up load balancing (if needed)
- [ ] Configure auto-scaling
- [ ] Optimize model inference (GPU/ONNX)

### Monitoring

- [ ] Set up application monitoring (Datadog/New Relic)
- [ ] Configure log aggregation (CloudWatch/Elasticsearch)
- [ ] Set up uptime monitoring (UptimeRobot/Pingdom)
- [ ] Configure error tracking (Sentry)
- [ ] Set up performance monitoring (APM)
- [ ] Create dashboard for key metrics
- [ ] Configure alerts for critical errors
- [ ] Set up backup monitoring

### Backup & Recovery

- [ ] Automated database backups (daily)
- [ ] Backup encryption
- [ ] Offsite backup storage
- [ ] Test restore procedures
- [ ] Document recovery steps
- [ ] Set up disaster recovery plan

### Documentation

- [ ] Update API documentation
- [ ] Document deployment process
- [ ] Create runbooks for common issues
- [ ] Document monitoring dashboards
- [ ] Create on-call playbook

## Monitoring

### Health Checks

**Backend Health:**
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "database_connected": true,
    "models_loaded": true
  }
}
```

**Frontend Health:**
```bash
curl -I http://localhost:3000
```

Expected: `200 OK`

### Log Monitoring

**View Backend Logs:**
```bash
# Docker
docker-compose logs -f backend

# Direct
tail -f logs/api.log
```

**View Frontend Logs:**
```bash
# Docker
docker-compose logs -f frontend

# Browser console
# Open DevTools (F12) → Console
```

### Performance Metrics

**Monitor Resource Usage:**
```bash
# CPU and Memory
docker stats

# Disk usage
df -h

# Network
netstat -tuln
```

**API Response Times:**
```bash
# Test endpoint latency
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/analyze
```

Create `curl-format.txt`:
```
   time_namelookup:  %{time_namelookup}\n
      time_connect:  %{time_connect}\n
   time_appconnect:  %{time_appconnect}\n
  time_pretransfer:  %{time_pretransfer}\n
     time_redirect:  %{time_redirect}\n
time_starttransfer:  %{time_starttransfer}\n
                   ----------\n
        time_total:  %{time_total}\n
```

### Uptime Monitoring

**Using UptimeRobot (Free):**
1. Sign up at https://uptimerobot.com
2. Add monitor:
   - Type: HTTP(s)
   - URL: https://yourdomain.com/health
   - Interval: 5 minutes
3. Configure alerts (email, SMS, Slack)

## Troubleshooting

### Backend Won't Start

**Issue:** ImportError or module not found
```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Issue:** Database locked
```bash
# Solution: Stop all processes using DB
lsof data/fintech_ai.db
kill -9 <PID>
```

**Issue:** Port already in use
```bash
# Solution: Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Frontend Build Fails

**Issue:** Node version mismatch
```bash
# Solution: Use correct Node version
nvm install 18
nvm use 18
```

**Issue:** Out of memory
```bash
# Solution: Increase Node memory
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

### Docker Issues

**Issue:** Permission denied
```bash
# Solution: Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

**Issue:** Container exits immediately
```bash
# Solution: Check logs
docker logs <container-id>
```

**Issue:** Cannot connect to containers
```bash
# Solution: Restart Docker network
docker network prune
docker-compose down && docker-compose up
```

### Performance Issues

**Issue:** Slow API responses
```bash
# Check: Model loading time
# Solution: Enable GPU inference or model quantization
```

**Issue:** High memory usage
```bash
# Check: Number of Uvicorn workers
# Solution: Reduce API_WORKERS in .env
```

**Issue:** Database slow
```bash
# Check: Database size and indexes
# Solution: Vacuum database
sqlite3 data/fintech_ai.db "VACUUM;"
```

### SSL Certificate Issues

**Issue:** Certificate expired
```bash
# Solution: Renew certificate
certbot renew
systemctl reload nginx
```

**Issue:** Mixed content warnings
```bash
# Solution: Update CORS origins to HTTPS
# Check nginx proxy settings
```

## Rollback Procedure

If deployment fails:

1. **Stop new version:**
   ```bash
   docker-compose down
   ```

2. **Restore previous version:**
   ```bash
   git checkout <previous-commit>
   docker-compose up -d
   ```

3. **Restore database backup:**
   ```bash
   cp data/backups/fintech_ai_<timestamp>.db data/fintech_ai.db
   ```

4. **Verify health:**
   ```bash
   curl http://localhost:8000/health
   ```

## Continuous Deployment (CI/CD)

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /app/fintech-ai-system
            git pull
            docker-compose up -d --build
```

## Support

For deployment issues:
- **Documentation:** https://docs.yourdomain.com
- **GitHub Issues:** https://github.com/yourusername/fintech-ai/issues
- **Email:** support@yourdomain.com
- **Discord:** https://discord.gg/yourserver
