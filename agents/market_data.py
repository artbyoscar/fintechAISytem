"""
Market Data Fetcher
Real-time stock data using yfinance with intelligent caching
"""

import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import os

# Disable curl_cffi to avoid SSL certificate issues on Windows
os.environ["YF_NO_CURL"] = "1"

import yfinance as yf
import pandas as pd
import numpy as np

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)


class MarketDataFetcher:
    """
    Fetches real-time market data using yfinance.

    Features:
    - Current stock prices and fundamentals
    - Historical price data
    - Volatility calculations
    - Intelligent caching (1 hour)
    - Error handling for invalid tickers
    """

    def __init__(self, cache_dir: str = "data/market_cache"):
        """
        Initialize market data fetcher.

        Args:
            cache_dir: Directory to store cached data
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        logger.info("MarketDataFetcher initialized")

    def _get_cache_path(self, ticker: str, data_type: str) -> str:
        """
        Get cache file path for ticker and data type.

        Args:
            ticker: Stock ticker
            data_type: Type of data (info, history, volatility)

        Returns:
            Cache file path
        """
        return os.path.join(self.cache_dir, f"{ticker}_{data_type}.json")

    def _is_cache_valid(self, cache_path: str) -> bool:
        """
        Check if cached data is still valid.

        Args:
            cache_path: Path to cache file

        Returns:
            True if cache is valid, False otherwise
        """
        if not os.path.exists(cache_path):
            return False

        # Check file modification time
        file_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return datetime.now() - file_time < self.cache_duration

    def _load_from_cache(self, cache_path: str) -> Optional[Dict]:
        """
        Load data from cache.

        Args:
            cache_path: Path to cache file

        Returns:
            Cached data or None
        """
        try:
            if self._is_cache_valid(cache_path):
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                logger.debug(f"Loaded from cache: {cache_path}")
                return data
        except Exception as e:
            logger.warning(f"Cache load failed: {e}")
        return None

    def _save_to_cache(self, cache_path: str, data: Dict):
        """
        Save data to cache.

        Args:
            cache_path: Path to cache file
            data: Data to cache
        """
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.debug(f"Saved to cache: {cache_path}")
        except Exception as e:
            logger.warning(f"Cache save failed: {e}")

    def get_stock_info(self, ticker: str) -> Dict:
        """
        Get current stock information and fundamentals.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dict with current price, volume, PE ratio, market cap, etc.

        Raises:
            ValueError: If ticker is invalid or data unavailable
        """
        ticker = ticker.upper()
        cache_path = self._get_cache_path(ticker, "info")

        # Try cache first
        cached_data = self._load_from_cache(cache_path)
        if cached_data:
            logger.info(f"Using cached data for {ticker}")
            return cached_data

        logger.info(f"Fetching stock info for {ticker}")

        try:
            # Fetch data from yfinance
            stock = yf.Ticker(ticker)
            info = stock.info

            # Check if ticker is valid
            if not info or 'regularMarketPrice' not in info:
                raise ValueError(f"Invalid ticker or no data available for {ticker}")

            # Extract key information
            stock_data = {
                'ticker': ticker,
                'company_name': info.get('longName', info.get('shortName', ticker)),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),

                # Price data
                'current_price': info.get('regularMarketPrice', info.get('currentPrice')),
                'previous_close': info.get('regularMarketPreviousClose', info.get('previousClose')),
                'open': info.get('regularMarketOpen', info.get('open')),
                'day_high': info.get('regularMarketDayHigh', info.get('dayHigh')),
                'day_low': info.get('regularMarketDayLow', info.get('dayLow')),

                # Volume
                'volume': info.get('regularMarketVolume', info.get('volume')),
                'avg_volume': info.get('averageVolume'),
                'avg_volume_10d': info.get('averageVolume10days'),

                # 52-week range
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow'),

                # Fundamentals
                'market_cap': info.get('marketCap'),
                'enterprise_value': info.get('enterpriseValue'),
                'pe_ratio': info.get('trailingPE'),
                'forward_pe': info.get('forwardPE'),
                'peg_ratio': info.get('pegRatio'),
                'price_to_book': info.get('priceToBook'),
                'price_to_sales': info.get('priceToSalesTrailing12Months'),

                # Profitability
                'profit_margins': info.get('profitMargins'),
                'operating_margins': info.get('operatingMargins'),
                'return_on_equity': info.get('returnOnEquity'),
                'return_on_assets': info.get('returnOnAssets'),

                # Dividends
                'dividend_yield': info.get('dividendYield'),
                'dividend_rate': info.get('dividendRate'),
                'payout_ratio': info.get('payoutRatio'),

                # Analyst recommendations
                'target_mean_price': info.get('targetMeanPrice'),
                'target_high_price': info.get('targetHighPrice'),
                'target_low_price': info.get('targetLowPrice'),
                'recommendation': info.get('recommendationKey'),
                'number_of_analyst_opinions': info.get('numberOfAnalystOpinions'),

                # Metadata
                'exchange': info.get('exchange'),
                'currency': info.get('currency'),
                'fetched_at': datetime.now().isoformat(),
            }

            # Calculate derived metrics
            if stock_data['current_price'] and stock_data['fifty_two_week_low']:
                range_span = stock_data['fifty_two_week_high'] - stock_data['fifty_two_week_low']
                current_from_low = stock_data['current_price'] - stock_data['fifty_two_week_low']
                stock_data['fifty_two_week_position'] = (current_from_low / range_span) * 100 if range_span > 0 else None

            # Cache the results
            self._save_to_cache(cache_path, stock_data)

            logger.info(f"Successfully fetched data for {ticker}: ${stock_data['current_price']:.2f}")
            return stock_data

        except Exception as e:
            logger.error(f"Failed to fetch stock info for {ticker}: {str(e)}")
            raise ValueError(f"Failed to fetch data for {ticker}: {str(e)}")

    def get_price_history(self, ticker: str, days: int = 90) -> pd.DataFrame:
        """
        Get historical price data.

        Args:
            ticker: Stock ticker symbol
            days: Number of days of history (default: 90)

        Returns:
            DataFrame with columns: Date, Open, High, Low, Close, Volume

        Raises:
            ValueError: If ticker is invalid or data unavailable
        """
        ticker = ticker.upper()
        cache_path = self._get_cache_path(ticker, f"history_{days}d")

        # Try cache first
        cached_data = self._load_from_cache(cache_path)
        if cached_data:
            logger.info(f"Using cached price history for {ticker}")
            df = pd.DataFrame(cached_data['data'])
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            return df

        logger.info(f"Fetching {days}-day price history for {ticker}")

        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Fetch data
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)

            if hist.empty:
                raise ValueError(f"No historical data available for {ticker}")

            # Reset index to make Date a column
            hist_reset = hist.reset_index()

            # Cache the results
            cache_data = {
                'ticker': ticker,
                'days': days,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'data': hist_reset.to_dict('records'),
                'fetched_at': datetime.now().isoformat()
            }
            self._save_to_cache(cache_path, cache_data)

            logger.info(f"Successfully fetched {len(hist)} days of history for {ticker}")
            return hist

        except Exception as e:
            logger.error(f"Failed to fetch price history for {ticker}: {str(e)}")
            raise ValueError(f"Failed to fetch price history for {ticker}: {str(e)}")

    def calculate_volatility(self, ticker: str, window: int = 30) -> Dict:
        """
        Calculate stock volatility metrics.

        Args:
            ticker: Stock ticker symbol
            window: Window for volatility calculation (default: 30 days)

        Returns:
            Dict with volatility metrics

        Raises:
            ValueError: If ticker is invalid or insufficient data
        """
        ticker = ticker.upper()
        cache_path = self._get_cache_path(ticker, f"volatility_{window}d")

        # Try cache first
        cached_data = self._load_from_cache(cache_path)
        if cached_data:
            logger.info(f"Using cached volatility for {ticker}")
            return cached_data

        logger.info(f"Calculating {window}-day volatility for {ticker}")

        try:
            # Get price history (need more days for accurate volatility)
            hist = self.get_price_history(ticker, days=window + 30)

            if len(hist) < window:
                raise ValueError(f"Insufficient data for {window}-day volatility calculation")

            # Calculate daily returns
            hist['Returns'] = hist['Close'].pct_change()

            # Calculate volatility metrics
            recent_returns = hist['Returns'].tail(window)

            volatility_data = {
                'ticker': ticker,
                'window_days': window,

                # Standard deviation (volatility)
                'volatility': float(recent_returns.std()),
                'annualized_volatility': float(recent_returns.std() * np.sqrt(252)),  # 252 trading days

                # Average return
                'mean_return': float(recent_returns.mean()),
                'annualized_return': float(recent_returns.mean() * 252),

                # Risk metrics
                'sharpe_ratio': float((recent_returns.mean() / recent_returns.std()) * np.sqrt(252)) if recent_returns.std() > 0 else None,

                # Range metrics
                'max_daily_return': float(recent_returns.max()),
                'min_daily_return': float(recent_returns.min()),
                'return_range': float(recent_returns.max() - recent_returns.min()),

                # Statistical measures
                'skewness': float(recent_returns.skew()),
                'kurtosis': float(recent_returns.kurtosis()),

                # Price metrics
                'current_price': float(hist['Close'].iloc[-1]),
                'period_high': float(hist['High'].tail(window).max()),
                'period_low': float(hist['Low'].tail(window).min()),
                'period_return': float((hist['Close'].iloc[-1] / hist['Close'].iloc[-window] - 1)),

                # Metadata
                'start_date': hist.index[-window].isoformat(),
                'end_date': hist.index[-1].isoformat(),
                'fetched_at': datetime.now().isoformat(),
            }

            # Classify volatility
            ann_vol = volatility_data['annualized_volatility']
            if ann_vol < 0.15:
                volatility_data['volatility_class'] = 'LOW'
            elif ann_vol < 0.30:
                volatility_data['volatility_class'] = 'MODERATE'
            elif ann_vol < 0.50:
                volatility_data['volatility_class'] = 'HIGH'
            else:
                volatility_data['volatility_class'] = 'VERY_HIGH'

            # Cache the results
            self._save_to_cache(cache_path, volatility_data)

            logger.info(f"Volatility for {ticker}: {ann_vol:.2%} (annualized)")
            return volatility_data

        except Exception as e:
            logger.error(f"Failed to calculate volatility for {ticker}: {str(e)}")
            raise ValueError(f"Failed to calculate volatility for {ticker}: {str(e)}")

    def get_comprehensive_data(self, ticker: str) -> Dict:
        """
        Get comprehensive market data including info, history, and volatility.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dict with all market data

        Raises:
            ValueError: If ticker is invalid
        """
        ticker = ticker.upper()
        logger.info(f"Fetching comprehensive data for {ticker}")

        try:
            return {
                'stock_info': self.get_stock_info(ticker),
                'price_history': self.get_price_history(ticker, days=90).tail(10).to_dict('records'),  # Last 10 days
                'volatility': self.calculate_volatility(ticker, window=30)
            }
        except Exception as e:
            logger.error(f"Failed to fetch comprehensive data for {ticker}: {str(e)}")
            raise

    def clear_cache(self, ticker: Optional[str] = None):
        """
        Clear cached data.

        Args:
            ticker: Specific ticker to clear, or None to clear all
        """
        if ticker:
            ticker = ticker.upper()
            # Remove all cache files for this ticker
            for file in os.listdir(self.cache_dir):
                if file.startswith(f"{ticker}_"):
                    os.remove(os.path.join(self.cache_dir, file))
            logger.info(f"Cleared cache for {ticker}")
        else:
            # Clear all cache files
            for file in os.listdir(self.cache_dir):
                if file.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, file))
            logger.info("Cleared all cache")


if __name__ == "__main__":
    # Test the market data fetcher
    logging.basicConfig(level=logging.INFO)

    print("\n" + "="*80)
    print("MARKET DATA FETCHER - TEST")
    print("="*80 + "\n")

    fetcher = MarketDataFetcher()

    # Test with multiple tickers
    test_tickers = ["AAPL", "MSFT", "NVDA"]

    for ticker in test_tickers:
        print(f"\n{'─'*80}")
        print(f"Testing {ticker}")
        print(f"{'─'*80}\n")

        try:
            # Test stock info
            print(f"[1/3] Fetching stock info...")
            info = fetcher.get_stock_info(ticker)
            print(f"✓ {info['company_name']}")
            print(f"  Price: ${info['current_price']:.2f}")
            print(f"  Market Cap: ${info['market_cap']:,.0f}" if info['market_cap'] else "  Market Cap: N/A")
            print(f"  P/E Ratio: {info['pe_ratio']:.2f}" if info['pe_ratio'] else "  P/E Ratio: N/A")
            print(f"  52W Range: ${info['fifty_two_week_low']:.2f} - ${info['fifty_two_week_high']:.2f}")

            # Test price history
            print(f"\n[2/3] Fetching price history (90 days)...")
            history = fetcher.get_price_history(ticker, days=90)
            print(f"✓ Retrieved {len(history)} days of data")
            print(f"  Oldest: {history.index[0].strftime('%Y-%m-%d')}")
            print(f"  Latest: {history.index[-1].strftime('%Y-%m-%d')}")

            # Test volatility
            print(f"\n[3/3] Calculating volatility...")
            vol = fetcher.calculate_volatility(ticker, window=30)
            print(f"✓ Volatility: {vol['annualized_volatility']:.2%} (annualized)")
            print(f"  Class: {vol['volatility_class']}")
            print(f"  30-day Return: {vol['period_return']:.2%}")
            print(f"  Sharpe Ratio: {vol['sharpe_ratio']:.2f}" if vol['sharpe_ratio'] else "  Sharpe Ratio: N/A")

        except ValueError as e:
            print(f"✗ Error: {str(e)}")
        except Exception as e:
            print(f"✗ Unexpected error: {str(e)}")

    print("\n" + "="*80)
    print("✓ ALL TESTS COMPLETED")
    print("="*80 + "\n")
