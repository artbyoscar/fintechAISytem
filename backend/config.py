"""
Configuration Management for Fintech AI System
Handles environment variables and API keys
"""

import os
import sys
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
import logging

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    """
    Configuration class for managing API keys and system settings.

    All API keys should be stored in a .env file in the project root.
    Never commit the .env file to version control!
    """

    # ============================================================================
    # API Keys - Add your keys to .env file
    # ============================================================================

    # Alpha Vantage - For earnings calendar and stock data
    # Get your free key at: https://www.alphavantage.co/support/#api-key
    ALPHA_VANTAGE_KEY: Optional[str] = os.getenv("ALPHA_VANTAGE_KEY")

    # FRED (Federal Reserve Economic Data) - For macro indicators
    # Get your free key at: https://fredaccount.stlouisfed.org/apikeys
    FRED_API_KEY: Optional[str] = os.getenv("FRED_API_KEY")

    # Anthropic (Claude) - For advanced NLP features (optional)
    # Get your key at: https://console.anthropic.com/settings/keys
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")

    # ============================================================================
    # Database Configuration
    # ============================================================================

    DB_PATH: str = os.getenv("DB_PATH", "data/fintech_ai.db")

    # ============================================================================
    # Model Configuration
    # ============================================================================

    # FinBERT model for sentiment analysis
    FINBERT_MODEL: str = os.getenv("FINBERT_MODEL", "ProsusAI/finbert")

    # Cache directory for downloaded models
    MODEL_CACHE_DIR: str = os.getenv("MODEL_CACHE_DIR", ".cache/huggingface")

    # ============================================================================
    # API Rate Limiting
    # ============================================================================

    # Alpha Vantage: 25 requests per day (free tier)
    ALPHA_VANTAGE_RATE_LIMIT: int = int(os.getenv("ALPHA_VANTAGE_RATE_LIMIT", "25"))

    # FRED: 120 requests per minute
    FRED_RATE_LIMIT: int = int(os.getenv("FRED_RATE_LIMIT", "120"))

    # ============================================================================
    # Application Settings
    # ============================================================================

    # Environment (development, production, testing)
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Debug mode
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Logging level
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Data directory
    DATA_DIR: str = os.getenv("DATA_DIR", "data")

    # Reports directory
    REPORTS_DIR: str = os.getenv("REPORTS_DIR", "data/analysis_reports")

    # ============================================================================
    # FastAPI Settings (for future web dashboard)
    # ============================================================================

    # API host and port
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # CORS settings
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")

    # ============================================================================
    # Feature Flags
    # ============================================================================

    # Enable real-time data fetching (requires API keys)
    ENABLE_REALTIME_DATA: bool = os.getenv("ENABLE_REALTIME_DATA", "False").lower() == "true"

    # Enable caching
    ENABLE_CACHING: bool = os.getenv("ENABLE_CACHING", "True").lower() == "true"

    # Cache expiration (in seconds)
    CACHE_EXPIRATION: int = int(os.getenv("CACHE_EXPIRATION", "3600"))  # 1 hour

    @classmethod
    def validate_api_keys(cls) -> dict:
        """
        Validate that required API keys are configured.

        Returns:
            Dict with validation status for each key
        """
        validation = {
            "alpha_vantage": cls.ALPHA_VANTAGE_KEY is not None,
            "fred_api": cls.FRED_API_KEY is not None,
            "anthropic": cls.ANTHROPIC_API_KEY is not None,
        }

        logger.info("API Key Validation:")
        for service, is_valid in validation.items():
            status = "✓ Configured" if is_valid else "✗ Missing"
            logger.info(f"  {service}: {status}")

        return validation

    @classmethod
    def get_api_key(cls, service: str) -> Optional[str]:
        """
        Get API key for a specific service.

        Args:
            service: Service name (alpha_vantage, fred_api, anthropic)

        Returns:
            API key if configured, None otherwise
        """
        keys = {
            "alpha_vantage": cls.ALPHA_VANTAGE_KEY,
            "fred_api": cls.FRED_API_KEY,
            "anthropic": cls.ANTHROPIC_API_KEY,
        }

        key = keys.get(service.lower())
        if not key:
            logger.warning(f"API key not configured for: {service}")

        return key

    @classmethod
    def is_ready_for_production(cls) -> bool:
        """
        Check if all required configuration is present for production use.

        Returns:
            True if ready for production, False otherwise
        """
        required_keys = [
            cls.ALPHA_VANTAGE_KEY,
            cls.FRED_API_KEY,
        ]

        return all(key is not None for key in required_keys)

    @classmethod
    def print_config_summary(cls):
        """Print configuration summary."""
        print("\n" + "="*80)
        print("FINTECH AI SYSTEM - CONFIGURATION")
        print("="*80)
        print(f"\nEnvironment: {cls.ENVIRONMENT}")
        print(f"Debug Mode: {cls.DEBUG}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"\nDatabase: {cls.DB_PATH}")
        print(f"Data Directory: {cls.DATA_DIR}")
        print(f"Reports Directory: {cls.REPORTS_DIR}")
        print(f"\nModel: {cls.FINBERT_MODEL}")
        print(f"Model Cache: {cls.MODEL_CACHE_DIR}")

        print("\nAPI Keys:")
        validation = cls.validate_api_keys()

        print(f"\nFeature Flags:")
        print(f"  Real-time Data: {cls.ENABLE_REALTIME_DATA}")
        print(f"  Caching: {cls.ENABLE_CACHING}")
        print(f"  Cache Expiration: {cls.CACHE_EXPIRATION}s")

        print(f"\nFastAPI Settings:")
        print(f"  Host: {cls.API_HOST}")
        print(f"  Port: {cls.API_PORT}")
        print(f"  CORS Origins: {cls.CORS_ORIGINS}")

        production_ready = cls.is_ready_for_production()
        status = "✓ READY" if production_ready else "✗ NOT READY (Missing API keys)"
        print(f"\nProduction Status: {status}")
        print("="*80 + "\n")


def create_env_template():
    """
    Create a template .env file if it doesn't exist.
    This helps users understand what keys they need to configure.
    """
    env_template = """# Fintech AI System - Environment Variables
# Copy this file to .env and fill in your API keys

# =============================================================================
# API Keys - Get your free keys from:
# =============================================================================

# Alpha Vantage (Required)
# Get your free key at: https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_KEY=your_alpha_vantage_key_here

# FRED API (Required)
# Get your free key at: https://fredaccount.stlouisfed.org/apikeys
FRED_API_KEY=your_fred_api_key_here

# Anthropic Claude (Optional - for advanced features)
# Get your key at: https://console.anthropic.com/settings/keys
ANTHROPIC_API_KEY=your_anthropic_key_here

# =============================================================================
# Database Configuration
# =============================================================================

DB_PATH=data/fintech_ai.db

# =============================================================================
# Model Configuration
# =============================================================================

FINBERT_MODEL=ProsusAI/finbert
MODEL_CACHE_DIR=.cache/huggingface

# =============================================================================
# Application Settings
# =============================================================================

ENVIRONMENT=development
DEBUG=False
LOG_LEVEL=INFO

DATA_DIR=data
REPORTS_DIR=data/analysis_reports

# =============================================================================
# API Settings
# =============================================================================

API_HOST=127.0.0.1
API_PORT=8000
CORS_ORIGINS=*

# =============================================================================
# Feature Flags
# =============================================================================

# Set to True once you have API keys configured
ENABLE_REALTIME_DATA=False

ENABLE_CACHING=True
CACHE_EXPIRATION=3600

# =============================================================================
# Rate Limiting
# =============================================================================

ALPHA_VANTAGE_RATE_LIMIT=25
FRED_RATE_LIMIT=120
"""

    env_file = Path(__file__).parent.parent / ".env.template"

    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(env_template)
        logger.info(f"Created .env.template file: {env_file}")
        print(f"\n✓ Created .env.template file")
        print(f"  Copy it to .env and add your API keys:")
        print(f"  cp .env.template .env")

    # Also create .env if it doesn't exist
    actual_env = Path(__file__).parent.parent / ".env"
    if not actual_env.exists():
        with open(actual_env, "w") as f:
            f.write(env_template)
        logger.info(f"Created .env file: {actual_env}")
        print(f"\n✓ Created .env file")
        print(f"  Edit it and add your API keys")


if __name__ == "__main__":
    # Test configuration
    logging.basicConfig(level=logging.INFO)

    # Create template files
    create_env_template()

    # Print configuration summary
    Config.print_config_summary()

    # Check if ready for production
    if not Config.is_ready_for_production():
        print("\n⚠️  WARNING: System not ready for production")
        print("   Please configure API keys in .env file")
        print("\n   Required keys:")
        print("   - ALPHA_VANTAGE_KEY (get at https://www.alphavantage.co/support/#api-key)")
        print("   - FRED_API_KEY (get at https://fredaccount.stlouisfed.org/apikeys)")
