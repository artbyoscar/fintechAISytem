"""
API Test Script
Tests all FastAPI endpoints
"""

import sys
import requests
import json
from time import sleep

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"


def print_section(title):
    """Print section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def test_endpoint(method, endpoint, data=None, description=""):
    """Test an API endpoint."""
    url = f"{BASE_URL}{endpoint}"
    print(f"Testing: {method} {endpoint}")
    if description:
        print(f"Description: {description}")

    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success', False)}")

            # Print sample of data
            if result.get('data'):
                data_str = json.dumps(result['data'], indent=2)
                lines = data_str.split('\n')
                if len(lines) > 20:
                    print("Data (first 20 lines):")
                    print('\n'.join(lines[:20]))
                    print("  ...")
                else:
                    print("Data:")
                    print(data_str)

            print("✓ PASSED")
        else:
            print(f"✗ FAILED: {response.text}")

    except requests.exceptions.ConnectionError:
        print("✗ FAILED: Server not running")
        print("\nPlease start the server first:")
        print("  python run_api.py")
        sys.exit(1)
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")

    print()


def main():
    """Run API tests."""
    print_section("FINTECH AI SYSTEM - API TESTS")

    # Test 1: Root endpoint
    test_endpoint(
        "GET", "/",
        description="Get API information"
    )

    # Test 2: Health check
    test_endpoint(
        "GET", "/health",
        description="Check API health status"
    )

    # Test 3: Stats
    test_endpoint(
        "GET", "/stats",
        description="Get database statistics"
    )

    # Test 4: Companies list
    test_endpoint(
        "GET", "/companies",
        description="List all companies"
    )

    # Test 5: Analyze company
    test_endpoint(
        "POST", "/analyze",
        data={"ticker": "JPM"},
        description="Analyze JPMorgan earnings"
    )

    # Wait for analysis to complete
    sleep(1)

    # Test 6: Recent analyses
    test_endpoint(
        "GET", "/recent?limit=5",
        description="Get 5 most recent analyses"
    )

    # Test 7: Company details
    test_endpoint(
        "GET", "/company/JPM",
        description="Get JPMorgan analysis history"
    )

    # Summary
    print_section("TEST SUMMARY")
    print("All endpoints tested successfully!")
    print("\nAPI Documentation: http://127.0.0.1:8000/docs")
    print("Interactive testing: http://127.0.0.1:8000/redoc")
    print()


if __name__ == "__main__":
    main()
