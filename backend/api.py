"""
FastAPI Application for Fintech AI System
RESTful API for earnings intelligence analysis
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import logging

# Add parent directory to path to access agents module
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

from backend.config import Config
from backend.database import Database
from backend.orchestrator import AnalysisOrchestrator

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Pydantic Models for Request/Response
# ============================================================================

class AnalyzeRequest(BaseModel):
    """Request model for analysis endpoint."""
    ticker: str = Field(..., description="Stock ticker symbol", min_length=1, max_length=10)

    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "NVDA"
            }
        }


class APIResponse(BaseModel):
    """Standard API response format."""
    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[Any] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if success=false")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"message": "Operation successful"},
                "error": None,
                "timestamp": "2025-10-31T12:00:00"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    environment: str
    database_connected: bool
    models_loaded: bool
    api_keys_configured: Dict[str, bool]


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Fintech AI System API",
    description="AI-powered earnings intelligence platform with sentiment analysis and macro regime detection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============================================================================
# CORS Middleware
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Global State
# ============================================================================

# These will be initialized on startup
orchestrator: Optional[AnalysisOrchestrator] = None
database: Optional[Database] = None


# ============================================================================
# Exception Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with standard response format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions with standard response format."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "data": None,
            "error": "Internal server error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )


# ============================================================================
# Lifecycle Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    global orchestrator, database

    logger.info("="*80)
    logger.info("FINTECH AI SYSTEM - API STARTUP")
    logger.info("="*80)

    try:
        # Initialize database
        logger.info("Initializing database...")
        database = Database(Config.DB_PATH)
        database.create_tables()
        logger.info("✓ Database initialized")

        # Initialize orchestrator (this loads all AI models)
        logger.info("Initializing orchestrator and AI models...")
        logger.info("  Loading FinBERT model (this may take a moment)...")
        orchestrator = AnalysisOrchestrator(Config.DB_PATH)
        logger.info("✓ Orchestrator initialized")
        logger.info("✓ FinBERT model loaded")

        # Validate configuration
        logger.info("\nValidating configuration...")
        Config.validate_api_keys()

        logger.info("\n" + "="*80)
        logger.info(f"API Server ready on http://{Config.API_HOST}:{Config.API_PORT}")
        logger.info(f"Documentation: http://{Config.API_HOST}:{Config.API_PORT}/docs")
        logger.info("="*80 + "\n")

    except Exception as e:
        logger.error(f"Startup failed: {str(e)}", exc_info=True)
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    global orchestrator, database

    logger.info("Shutting down API server...")

    if orchestrator:
        orchestrator.close()
        logger.info("✓ Orchestrator closed")

    if database:
        database.close()
        logger.info("✓ Database closed")

    logger.info("Shutdown complete")


# ============================================================================
# API Endpoints
# ============================================================================

@app.get(
    "/health",
    response_model=APIResponse,
    summary="Health Check",
    description="Check API health and system status"
)
async def health_check():
    """
    Health check endpoint.

    Returns system status including:
    - API status
    - Database connectivity
    - Model loading status
    - API key configuration
    """
    try:
        # Check database connection
        db_connected = False
        if database:
            try:
                stats = database.get_company_stats()
                db_connected = True
            except Exception as e:
                logger.error(f"Database health check failed: {e}")

        # Check models loaded
        models_loaded = orchestrator is not None

        # Check API keys
        api_keys = Config.validate_api_keys()

        health_data = HealthResponse(
            status="healthy" if db_connected and models_loaded else "degraded",
            environment=Config.ENVIRONMENT,
            database_connected=db_connected,
            models_loaded=models_loaded,
            api_keys_configured=api_keys
        )

        return APIResponse(
            success=True,
            data=health_data.model_dump()
        )

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable"
        )


@app.post(
    "/analyze",
    response_model=APIResponse,
    summary="Analyze Company",
    description="Run full analysis pipeline for a company ticker"
)
async def analyze_company(request: AnalyzeRequest):
    """
    Analyze earnings call for a company.

    Runs the complete analysis pipeline:
    1. Fetches earnings transcript
    2. Analyzes sentiment with FinBERT
    3. Detects macro regime
    4. Generates comprehensive report
    5. Stores results in database

    Returns complete analysis including sentiment, macro regime, and trading recommendation.
    """
    if not orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not initialized"
        )

    ticker = request.ticker.upper()

    try:
        logger.info(f"Starting analysis for {ticker}")

        # Run analysis
        result = orchestrator.analyze_company(ticker)

        # Reset sentiment analyzer for next request
        orchestrator.sentiment_analyzer.reset()

        if not result.get('success', False):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result.get('error', 'Analysis failed')
            )

        logger.info(f"Analysis completed for {ticker}")

        return APIResponse(
            success=True,
            data=result
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed for {ticker}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get(
    "/recent",
    response_model=APIResponse,
    summary="Recent Analyses",
    description="Get most recent earnings call analyses"
)
async def get_recent_analyses(limit: int = 10):
    """
    Get recent analyses from database.

    Args:
        limit: Maximum number of results to return (default: 10, max: 100)

    Returns list of recent analyses with metadata.
    """
    if not database:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )

    # Validate limit
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100"
        )

    try:
        recent_calls = database.get_recent_calls(limit=limit)

        # Enrich with analysis results
        enriched_results = []
        for call in recent_calls:
            analysis = database.get_analysis_by_call_id(call['id'])
            enriched_results.append({
                'call': dict(call),
                'analysis': analysis
            })

        return APIResponse(
            success=True,
            data={
                'count': len(enriched_results),
                'analyses': enriched_results
            }
        )

    except Exception as e:
        logger.error(f"Failed to fetch recent analyses: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recent analyses"
        )


@app.get(
    "/companies",
    response_model=APIResponse,
    summary="List Companies",
    description="Get all companies in the database"
)
async def list_companies():
    """
    List all companies in the database.

    Returns all companies that have been analyzed, including:
    - Ticker symbol
    - Company name
    - Sector
    - Number of analyses
    """
    if not database:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )

    try:
        # Get all unique companies from earnings calls
        cursor = database.conn.cursor()
        cursor.execute("""
            SELECT
                c.ticker,
                c.name,
                c.sector,
                c.market_cap,
                COUNT(ec.id) as analysis_count,
                MAX(ec.call_date) as latest_call_date,
                AVG(ec.sentiment_score) as avg_sentiment
            FROM companies c
            LEFT JOIN earnings_calls ec ON c.ticker = ec.ticker
            GROUP BY c.ticker, c.name, c.sector, c.market_cap
            ORDER BY latest_call_date DESC
        """)

        companies = []
        for row in cursor.fetchall():
            companies.append({
                'ticker': row[0],
                'name': row[1],
                'sector': row[2],
                'market_cap': row[3],
                'analysis_count': row[4],
                'latest_call_date': row[5],
                'avg_sentiment': round(row[6], 3) if row[6] else None
            })

        return APIResponse(
            success=True,
            data={
                'count': len(companies),
                'companies': companies
            }
        )

    except Exception as e:
        logger.error(f"Failed to fetch companies: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch companies"
        )


@app.get(
    "/company/{ticker}",
    response_model=APIResponse,
    summary="Get Company Details",
    description="Get detailed analysis history for a specific company"
)
async def get_company_details(ticker: str):
    """
    Get analysis history for a specific company.

    Args:
        ticker: Stock ticker symbol

    Returns all analyses for the specified company.
    """
    if not database:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )

    ticker = ticker.upper()

    try:
        # Get company earnings calls
        calls = database.get_call_by_ticker(ticker, limit=50)

        if not calls:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data found for ticker: {ticker}"
            )

        # Enrich with analysis results
        detailed_analyses = []
        for call in calls:
            analysis = database.get_analysis_by_call_id(call['id'])
            detailed_analyses.append({
                'call': dict(call),
                'analysis': analysis
            })

        return APIResponse(
            success=True,
            data={
                'ticker': ticker,
                'company_name': calls[0]['company_name'] if calls else None,
                'count': len(detailed_analyses),
                'analyses': detailed_analyses
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch company details for {ticker}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch company details for {ticker}"
        )


@app.get(
    "/stats",
    response_model=APIResponse,
    summary="Database Statistics",
    description="Get overall database statistics"
)
async def get_statistics():
    """
    Get database statistics.

    Returns:
    - Total companies analyzed
    - Total earnings calls
    - Total analyses
    - Regime distribution
    """
    if not database:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )

    try:
        stats = database.get_company_stats()

        return APIResponse(
            success=True,
            data=stats
        )

    except Exception as e:
        logger.error(f"Failed to fetch stats: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch statistics"
        )


@app.get(
    "/",
    response_model=APIResponse,
    summary="API Info",
    description="Get API information and available endpoints"
)
async def root():
    """
    Root endpoint with API information.
    """
    return APIResponse(
        success=True,
        data={
            "name": "Fintech AI System API",
            "version": "1.0.0",
            "description": "AI-powered earnings intelligence platform",
            "endpoints": {
                "health": "/health - Health check",
                "analyze": "/analyze - Analyze company earnings",
                "recent": "/recent - Get recent analyses",
                "companies": "/companies - List all companies",
                "company": "/company/{ticker} - Get company details",
                "stats": "/stats - Get database statistics",
                "docs": "/docs - Interactive API documentation",
            },
            "documentation": f"http://{Config.API_HOST}:{Config.API_PORT}/docs"
        }
    )


# ============================================================================
# Run Server
# ============================================================================

def start_server(
    host: str = Config.API_HOST,
    port: int = Config.API_PORT,
    reload: bool = False
):
    """
    Start the FastAPI server.

    Args:
        host: Host to bind to
        port: Port to bind to
        reload: Enable auto-reload on code changes (development only)
    """
    logger.info(f"Starting Fintech AI System API...")
    logger.info(f"Environment: {Config.ENVIRONMENT}")
    logger.info(f"Debug mode: {Config.DEBUG}")

    uvicorn.run(
        "backend.api:app",
        host=host,
        port=port,
        reload=reload,
        log_level=Config.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    # Run with auto-reload in development
    start_server(reload=Config.ENVIRONMENT == "development")
