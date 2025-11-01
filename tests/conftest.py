"""
Pytest Configuration and Shared Fixtures
"""

import os
import sys
import pytest
import tempfile
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import Database
from agents.sentiment_analyzer import SentimentAnalyzer
from agents.macro_detector import MacroRegimeDetector
from backend.orchestrator import AnalysisOrchestrator


@pytest.fixture(scope="session")
def sample_transcript():
    """Sample earnings call transcript for testing."""
    return """
    We had an outstanding quarter with record revenue growth of 45%.
    Our new product launches exceeded all expectations and customer satisfaction is at an all-time high.
    The management team is extremely confident about the upcoming fiscal year.
    However, we do face some challenges in supply chain management.
    Overall, the outlook is very positive and we expect continued strong performance.
    """


@pytest.fixture(scope="session")
def bearish_transcript():
    """Bearish earnings call transcript for testing."""
    return """
    This quarter was disappointing with revenue declining 15% year-over-year.
    We missed our earnings targets due to weak demand and pricing pressure.
    The competitive environment remains challenging and margins are under pressure.
    We are seeing significant headwinds in our core markets.
    Management expects continued difficulties in the near term.
    """


@pytest.fixture(scope="session")
def neutral_transcript():
    """Neutral earnings call transcript for testing."""
    return """
    Results were in line with expectations this quarter.
    Revenue was flat compared to last year.
    We continue to monitor market conditions closely.
    The business environment remains stable.
    We are maintaining our full-year guidance.
    """


@pytest.fixture(scope="function")
def temp_database():
    """Create a temporary database for testing."""
    # Create temporary database file
    temp_db = tempfile.NamedTemporaryFile(mode='w', suffix='.db', delete=False)
    temp_db_path = temp_db.name
    temp_db.close()

    # Initialize database
    db = Database(temp_db_path)
    db.create_tables()

    yield db

    # Cleanup
    db.close()
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)


@pytest.fixture(scope="session")
def sentiment_analyzer():
    """Create a sentiment analyzer instance."""
    return SentimentAnalyzer()


@pytest.fixture(scope="session")
def macro_detector():
    """Create a macro regime detector instance."""
    return MacroRegimeDetector()


@pytest.fixture(scope="function")
def orchestrator_with_temp_db():
    """Create an orchestrator with temporary database."""
    temp_db = tempfile.NamedTemporaryFile(mode='w', suffix='.db', delete=False)
    temp_db_path = temp_db.name
    temp_db.close()

    orchestrator = AnalysisOrchestrator(db_path=temp_db_path)

    yield orchestrator

    # Cleanup
    orchestrator.close()
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)


@pytest.fixture(scope="session")
def mock_transcript_data():
    """Mock earnings transcript data."""
    return {
        'company': 'Test Corporation',
        'ticker': 'TEST',
        'date': '2025-10-15',
        'quarter': 'Q3',
        'fiscal_year': 2025,
        'sector': 'Technology',
        'transcript': """
        We delivered exceptional results this quarter with revenue up 40%.
        Our innovation pipeline is stronger than ever.
        Customer engagement metrics are at record highs.
        The team executed flawlessly on our strategic initiatives.
        We are very optimistic about the future.
        """
    }


@pytest.fixture(scope="session")
def mock_sentiment_result():
    """Mock sentiment analysis result."""
    return {
        'overall_label': 'positive',
        'sentiment_score': 0.75,
        'overall_confidence': 0.85,
        'sentiment_distribution': {
            'positive': 0.80,
            'neutral': 0.15,
            'negative': 0.05
        },
        'weighted_scores': {
            'positive': 0.68,
            'neutral': 0.05,
            'negative': -0.02
        }
    }


@pytest.fixture(scope="session")
def mock_macro_regime():
    """Mock macro regime data."""
    return {
        'regime': 'BULL',
        'confidence': 0.78,
        'indicators': {
            'vix': 18.5,
            'unemployment': 3.8,
            'inflation': 3.2,
            'fed_rate': 5.25,
            'gdp_growth': 2.5
        },
        'reasoning': 'Low VIX and unemployment indicate bullish conditions',
        'signals': {
            'vix_signal': 'bullish',
            'unemployment_signal': 'bullish',
            'inflation_signal': 'neutral'
        }
    }


@pytest.fixture(scope="session")
def mock_analysis_report():
    """Mock complete analysis report."""
    return {
        'success': True,
        'ticker': 'TEST',
        'company': 'Test Corporation',
        'analysis_timestamp': datetime.now().isoformat(),
        'earnings_call': {
            'date': '2025-10-15',
            'quarter': 'Q3',
            'fiscal_year': 2025,
            'transcript_length': 500,
            'sentences_analyzed': 10
        },
        'sentiment_analysis': {
            'overall_label': 'positive',
            'sentiment_score': 0.75,
            'confidence': 0.85,
            'distribution': {
                'positive': 0.80,
                'neutral': 0.15,
                'negative': 0.05
            }
        },
        'macro_regime': {
            'regime': 'BULL',
            'confidence': 0.78,
            'indicators': {
                'vix': 18.5,
                'unemployment': 3.8
            }
        },
        'recommendation': {
            'action': 'FAVORABLE',
            'risk_level': 'MODERATE'
        },
        'overall_assessment': {
            'verdict': 'STRONG BUY',
            'reasoning': 'Bullish regime + positive sentiment'
        }
    }


@pytest.fixture(scope="session")
def mock_market_data():
    """Mock market data from yfinance."""
    return {
        'ticker': 'TEST',
        'current_price': 150.25,
        'change': 5.50,
        'change_percent': 3.80,
        'volume': 10500000,
        'market_cap': 500000000000,
        'pe_ratio': 25.5,
        'week_52_high': 165.00,
        'week_52_low': 120.00,
        'volatility': 0.25,
        'sharpe_ratio': 1.5,
        'historical_data': {
            'dates': ['2025-10-01', '2025-10-15', '2025-10-30'],
            'closes': [145.00, 148.50, 150.25]
        }
    }


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment before each test."""
    # This ensures each test starts with a clean state
    yield
    # Cleanup code can go here if needed


@pytest.fixture(scope="session")
def api_test_client():
    """Create FastAPI test client."""
    from fastapi.testclient import TestClient
    from run_api import app
    return TestClient(app)
