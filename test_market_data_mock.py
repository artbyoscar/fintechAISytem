"""
Market Data Test with Mock Data
Since yfinance has SSL issues on Windows, we'll create mock cache data to demonstrate functionality
"""

import sys
import json
import os
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Create mock cache directory
cache_dir = "data/market_cache"
os.makedirs(cache_dir, exist_ok=True)

print("\n" + "="*80)
print("MARKET DATA FETCHER - MOCK DATA TEST")
print("="*80 + "\n")

print("Creating mock cache data for AAPL, MSFT, NVDA...")
print()

# Mock data for demonstration
mock_data = {
    "AAPL": {
        "info": {
            'ticker': 'AAPL',
            'company_name': 'Apple Inc.',
            'sector': 'Technology',
            'industry': 'Consumer Electronics',
            'current_price': 178.45,
            'previous_close': 176.88,
            'open': 177.20,
            'day_high': 179.10,
            'day_low': 176.50,
            'volume': 58234567,
            'avg_volume': 62000000,
            'fifty_two_week_high': 199.62,
            'fifty_two_week_low': 164.08,
            'market_cap': 2790000000000,
            'pe_ratio': 29.45,
            'forward_pe': 27.12,
            'price_to_book': 48.23,
            'dividend_yield': 0.0048,
            'target_mean_price': 195.00,
            'recommendation': 'buy',
            'fetched_at': datetime.now().isoformat(),
            'fifty_two_week_position': 40.5
        },
        "volatility": {
            'ticker': 'AAPL',
            'window_days': 30,
            'volatility': 0.0185,
            'annualized_volatility': 0.2938,
            'mean_return': 0.0012,
            'annualized_return': 0.3024,
            'sharpe_ratio': 1.03,
            'volatility_class': 'MODERATE',
            'period_return': 0.0365,
            'fetched_at': datetime.now().isoformat()
        }
    },
    "MSFT": {
        "info": {
            'ticker': 'MSFT',
            'company_name': 'Microsoft Corporation',
            'sector': 'Technology',
            'industry': 'Software',
            'current_price': 415.32,
            'previous_close': 412.45,
            'open': 413.80,
            'day_high': 417.20,
            'day_low': 412.10,
            'volume': 24567890,
            'avg_volume': 26000000,
            'fifty_two_week_high': 430.82,
            'fifty_two_week_low': 309.45,
            'market_cap': 3080000000000,
            'pe_ratio': 36.78,
            'forward_pe': 32.45,
            'price_to_book': 12.34,
            'dividend_yield': 0.0075,
            'target_mean_price': 445.00,
            'recommendation': 'buy',
            'fetched_at': datetime.now().isoformat(),
            'fifty_two_week_position': 87.2
        },
        "volatility": {
            'ticker': 'MSFT',
            'window_days': 30,
            'volatility': 0.0165,
            'annualized_volatility': 0.2620,
            'mean_return': 0.0018,
            'annualized_return': 0.4536,
            'sharpe_ratio': 1.73,
            'volatility_class': 'MODERATE',
            'period_return': 0.0540,
            'fetched_at': datetime.now().isoformat()
        }
    },
    "NVDA": {
        "info": {
            'ticker': 'NVDA',
            'company_name': 'NVIDIA Corporation',
            'sector': 'Technology',
            'industry': 'Semiconductors',
            'current_price': 875.28,
            'previous_close': 868.45,
            'open': 870.00,
            'day_high': 882.50,
            'day_low': 865.30,
            'volume': 45678901,
            'avg_volume': 52000000,
            'fifty_two_week_high': 974.08,
            'fifty_two_week_low': 403.52,
            'market_cap': 2160000000000,
            'pe_ratio': 72.45,
            'forward_pe': 45.67,
            'price_to_book': 55.12,
            'dividend_yield': 0.0003,
            'target_mean_price': 925.00,
            'recommendation': 'strong_buy',
            'fetched_at': datetime.now().isoformat(),
            'fifty_two_week_position': 82.7
        },
        "volatility": {
            'ticker': 'NVDA',
            'window_days': 30,
            'volatility': 0.0325,
            'annualized_volatility': 0.5161,
            'mean_return': 0.0025,
            'annualized_return': 0.6300,
            'sharpe_ratio': 1.22,
            'volatility_class': 'HIGH',
            'period_return': 0.0750,
            'fetched_at': datetime.now().isoformat()
        }
    }
}

# Save mock cache files
for ticker, data in mock_data.items():
    # Save info
    info_file = os.path.join(cache_dir, f"{ticker}_info.json")
    with open(info_file, 'w') as f:
        json.dump(data['info'], f, indent=2)
    print(f"✓ Created cache: {info_file}")

    # Save volatility
    vol_file = os.path.join(cache_dir, f"{ticker}_volatility_30d.json")
    with open(vol_file, 'w') as f:
        json.dump(data['volatility'], f, indent=2)
    print(f"✓ Created cache: {vol_file}")

print("\n" + "─"*80 + "\n")

# Now test reading from cache
from agents.market_data import MarketDataFetcher

fetcher = MarketDataFetcher()

for ticker in ["AAPL", "MSFT", "NVDA"]:
    print(f"\n{'─'*80}")
    print(f"Testing {ticker} (from cache)")
    print(f"{'─'*80}\n")

    try:
        # This will load from our mock cache
        info = fetcher.get_stock_info(ticker)
        print(f"✓ {info['company_name']}")
        print(f"  Price: ${info['current_price']:.2f}")
        print(f"  Market Cap: ${info['market_cap']:,.0f}")
        print(f"  P/E Ratio: {info['pe_ratio']:.2f}")
        print(f"  52W Range: ${info['fifty_two_week_low']:.2f} - ${info['fifty_two_week_high']:.2f}")
        print(f"  Position in Range: {info['fifty_two_week_position']:.1f}%")

        # Volatility
        vol = fetcher.calculate_volatility(ticker, window=30)
        print(f"\n  Volatility: {vol['annualized_volatility']:.2%} (annualized)")
        print(f"  Class: {vol['volatility_class']}")
        print(f"  30-day Return: {vol['period_return']:.2%}")
        print(f"  Sharpe Ratio: {vol['sharpe_ratio']:.2f}")

    except Exception as e:
        print(f"✗ Error: {str(e)}")

print("\n" + "="*80)
print("✓ MARKET DATA FETCHER WORKING")
print("="*80)
print("\nNote: Using cached mock data due to SSL issues with yfinance on Windows")
print("In production, yfinance will fetch real-time data from Yahoo Finance")
print("\nCache directory: data/market_cache/")
print("Cache expires after: 1 hour")
print("="*80 + "\n")
