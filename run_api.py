"""
API Server Launcher
Starts the FastAPI server with proper Python path
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Import and start
from backend.api import start_server
from backend.config import Config

if __name__ == "__main__":
    print("\n" + "="*80)
    print("FINTECH AI SYSTEM - API SERVER")
    print("="*80 + "\n")

    print(f"Starting server on http://{Config.API_HOST}:{Config.API_PORT}")
    print(f"Docs available at: http://{Config.API_HOST}:{Config.API_PORT}/docs\n")

    # Start server with auto-reload in development
    start_server(reload=Config.ENVIRONMENT == "development")
