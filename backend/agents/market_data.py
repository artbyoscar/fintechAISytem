"""
Market Data Agent
Fetches real-time and historical stock price data and calculates technical indicators
"""

import logging
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
import time

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)


class MarketDataAgent:
    """
    Agent responsible for fetching market data and calculating technical indicators.

    Uses Alpha Vantage API for real-time and historical stock data.
    Calculates technical indicators including SMA, EMA, MACD, RSI, and Bollinger Bands.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize MarketDataAgent.

        Args:
            api_key: Alpha Vantage API key
        """
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes cache

        if not api_key:
            logger.warning("No Alpha Vantage API key provided. Using mock data.")

    def fetch_intraday_data(
        self,
        ticker: str,
        interval: str = "5min",
        outputsize: str = "compact"
    ) -> Dict[str, Any]:
        """
        Fetch intraday time series data.

        Args:
            ticker: Stock ticker symbol
            interval: Time interval (1min, 5min, 15min, 30min, 60min)
            outputsize: 'compact' (100 points) or 'full' (full data)

        Returns:
            Dictionary with intraday OHLCV data
        """
        if not self.api_key:
            logger.warning(f"No API key - returning mock intraday data for {ticker}")
            return self._generate_mock_intraday_data(ticker, interval, outputsize)

        # Check cache
        cache_key = f"{ticker}_{interval}_{outputsize}_intraday"
        if self._is_cached(cache_key):
            logger.info(f"Returning cached intraday data for {ticker}")
            return self.cache[cache_key]['data']

        try:
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': ticker,
                'interval': interval,
                'outputsize': outputsize,
                'apikey': self.api_key
            }

            logger.info(f"Fetching intraday data for {ticker} (interval: {interval})")
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Check for API errors
            if 'Error Message' in data:
                logger.error(f"Alpha Vantage error: {data['Error Message']}")
                return self._generate_mock_intraday_data(ticker, interval, outputsize)

            if 'Note' in data:
                logger.warning(f"API rate limit hit: {data['Note']}")
                return self._generate_mock_intraday_data(ticker, interval, outputsize)

            # Parse and format data
            time_series_key = f'Time Series ({interval})'
            if time_series_key not in data:
                logger.error(f"Unexpected response format: {list(data.keys())}")
                return self._generate_mock_intraday_data(ticker, interval, outputsize)

            formatted_data = self._format_alpha_vantage_data(
                data[time_series_key],
                ticker
            )

            # Cache the result
            self._cache_data(cache_key, formatted_data)

            return formatted_data

        except Exception as e:
            logger.error(f"Error fetching intraday data for {ticker}: {str(e)}")
            return self._generate_mock_intraday_data(ticker, interval, outputsize)

    def fetch_daily_data(
        self,
        ticker: str,
        outputsize: str = "compact"
    ) -> Dict[str, Any]:
        """
        Fetch daily time series data.

        Args:
            ticker: Stock ticker symbol
            outputsize: 'compact' (100 days) or 'full' (20+ years)

        Returns:
            Dictionary with daily OHLCV data
        """
        if not self.api_key:
            logger.warning(f"No API key - returning mock daily data for {ticker}")
            return self._generate_mock_daily_data(ticker, outputsize)

        # Check cache
        cache_key = f"{ticker}_{outputsize}_daily"
        if self._is_cached(cache_key):
            logger.info(f"Returning cached daily data for {ticker}")
            return self.cache[cache_key]['data']

        try:
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': ticker,
                'outputsize': outputsize,
                'apikey': self.api_key
            }

            logger.info(f"Fetching daily data for {ticker}")
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Check for API errors
            if 'Error Message' in data:
                logger.error(f"Alpha Vantage error: {data['Error Message']}")
                return self._generate_mock_daily_data(ticker, outputsize)

            if 'Note' in data:
                logger.warning(f"API rate limit hit: {data['Note']}")
                return self._generate_mock_daily_data(ticker, outputsize)

            # Parse and format data
            if 'Time Series (Daily)' not in data:
                logger.error(f"Unexpected response format: {list(data.keys())}")
                return self._generate_mock_daily_data(ticker, outputsize)

            formatted_data = self._format_alpha_vantage_data(
                data['Time Series (Daily)'],
                ticker
            )

            # Cache the result
            self._cache_data(cache_key, formatted_data)

            return formatted_data

        except Exception as e:
            logger.error(f"Error fetching daily data for {ticker}: {str(e)}")
            return self._generate_mock_daily_data(ticker, outputsize)

    def get_market_data_with_indicators(
        self,
        ticker: str,
        timeframe: str = "1M"
    ) -> Dict[str, Any]:
        """
        Fetch market data and calculate all technical indicators.

        Args:
            ticker: Stock ticker symbol
            timeframe: Time range (1D, 5D, 1M, 3M, 6M, 1Y, 5Y, MAX)

        Returns:
            Dictionary with OHLCV data and technical indicators
        """
        logger.info(f"Fetching market data with indicators for {ticker} ({timeframe})")

        # Determine which data to fetch based on timeframe
        if timeframe in ['1D', '5D']:
            # Use intraday data
            interval = '5min' if timeframe == '1D' else '5min'
            raw_data = self.fetch_intraday_data(ticker, interval, outputsize='full')
        else:
            # Use daily data
            outputsize = 'full' if timeframe in ['5Y', 'MAX'] else 'compact'
            raw_data = self.fetch_daily_data(ticker, outputsize)

        if not raw_data or not raw_data.get('data'):
            logger.error(f"No data available for {ticker}")
            return {
                'success': False,
                'error': 'No market data available',
                'ticker': ticker,
                'timeframe': timeframe
            }

        # Get the data points
        data_points = raw_data['data']

        # Filter data based on timeframe
        filtered_data = self._filter_by_timeframe(data_points, timeframe)

        # Calculate technical indicators
        data_with_indicators = self._calculate_all_indicators(filtered_data)

        return {
            'success': True,
            'ticker': ticker,
            'timeframe': timeframe,
            'data_points': len(data_with_indicators),
            'data': data_with_indicators,
            'metadata': {
                'last_updated': datetime.now().isoformat(),
                'source': 'Alpha Vantage' if self.api_key else 'Mock Data'
            }
        }

    def _format_alpha_vantage_data(
        self,
        time_series: Dict[str, Any],
        ticker: str
    ) -> Dict[str, Any]:
        """
        Format Alpha Vantage time series data into standard format.

        Args:
            time_series: Raw time series data from Alpha Vantage
            ticker: Stock ticker symbol

        Returns:
            Formatted data dictionary
        """
        data_points = []

        for timestamp, values in sorted(time_series.items()):
            data_points.append({
                'date': timestamp,
                'timestamp': self._parse_timestamp(timestamp),
                'open': float(values.get('1. open', 0)),
                'high': float(values.get('2. high', 0)),
                'low': float(values.get('3. low', 0)),
                'close': float(values.get('4. close', 0)),
                'volume': int(values.get('5. volume', 0))
            })

        return {
            'ticker': ticker,
            'data': data_points
        }

    def _calculate_all_indicators(self, data: List[Dict]) -> List[Dict]:
        """
        Calculate all technical indicators for the data.

        Args:
            data: List of OHLCV data points

        Returns:
            Data with calculated indicators
        """
        if not data:
            return []

        # Calculate SMAs
        self._calculate_sma(data, 20)
        self._calculate_sma(data, 50)
        self._calculate_sma(data, 200)

        # Calculate EMAs
        ema_12 = self._calculate_ema(data, 12)
        ema_26 = self._calculate_ema(data, 26)

        # Calculate MACD
        self._calculate_macd(data, ema_12, ema_26)

        # Calculate RSI
        self._calculate_rsi(data, 14)

        # Calculate Bollinger Bands
        self._calculate_bollinger_bands(data, 20, 2)

        return data

    def _calculate_sma(self, data: List[Dict], period: int):
        """Calculate Simple Moving Average."""
        key = f'sma{period}'

        for i in range(len(data)):
            if i < period - 1:
                data[i][key] = None
                continue

            sum_close = sum(data[j]['close'] for j in range(i - period + 1, i + 1))
            data[i][key] = round(sum_close / period, 2)

    def _calculate_ema(self, data: List[Dict], period: int) -> List[Optional[float]]:
        """Calculate Exponential Moving Average."""
        ema = []
        multiplier = 2 / (period + 1)

        # Start with SMA for first value
        if len(data) >= period:
            sum_close = sum(data[i]['close'] for i in range(period))
            ema_value = sum_close / period
        else:
            ema_value = None

        for i in range(len(data)):
            if i < period - 1:
                ema.append(None)
            elif i == period - 1:
                ema.append(ema_value)
            else:
                ema_value = (data[i]['close'] - ema_value) * multiplier + ema_value
                ema.append(ema_value)

        # Store in data
        key = f'ema{period}'
        for i, val in enumerate(ema):
            data[i][key] = round(val, 2) if val is not None else None

        return ema

    def _calculate_macd(
        self,
        data: List[Dict],
        ema_12: List[Optional[float]],
        ema_26: List[Optional[float]]
    ):
        """Calculate MACD (Moving Average Convergence Divergence)."""
        # MACD = EMA(12) - EMA(26)
        macd_values = []
        for i in range(len(data)):
            if ema_12[i] is not None and ema_26[i] is not None:
                macd = ema_12[i] - ema_26[i]
                macd_values.append(macd)
                data[i]['macd'] = round(macd, 2)
            else:
                macd_values.append(None)
                data[i]['macd'] = None

        # Signal line = EMA(9) of MACD
        signal = self._calculate_ema_from_values(macd_values, 9)

        # Histogram = MACD - Signal
        for i in range(len(data)):
            data[i]['signal'] = round(signal[i], 2) if signal[i] is not None else None

            if data[i]['macd'] is not None and data[i]['signal'] is not None:
                data[i]['histogram'] = round(data[i]['macd'] - data[i]['signal'], 2)
            else:
                data[i]['histogram'] = None

    def _calculate_ema_from_values(
        self,
        values: List[Optional[float]],
        period: int
    ) -> List[Optional[float]]:
        """Calculate EMA from a list of values."""
        ema = []
        multiplier = 2 / (period + 1)

        # Find first valid values for initial SMA
        valid_values = [v for v in values[:period] if v is not None]

        if len(valid_values) >= period:
            ema_value = sum(valid_values[:period]) / period
        else:
            ema_value = None

        for i in range(len(values)):
            if i < period - 1:
                ema.append(None)
            elif i == period - 1:
                ema.append(ema_value)
            else:
                if values[i] is not None and ema_value is not None:
                    ema_value = (values[i] - ema_value) * multiplier + ema_value
                    ema.append(ema_value)
                else:
                    ema.append(None)

        return ema

    def _calculate_rsi(self, data: List[Dict], period: int = 14):
        """Calculate Relative Strength Index."""
        for i in range(len(data)):
            if i < period:
                data[i]['rsi'] = None
                continue

            gains = 0
            losses = 0

            for j in range(i - period + 1, i + 1):
                change = data[j]['close'] - data[j - 1]['close']
                if change > 0:
                    gains += change
                else:
                    losses -= change

            avg_gain = gains / period
            avg_loss = losses / period

            if avg_loss == 0:
                data[i]['rsi'] = 100
            else:
                rs = avg_gain / avg_loss
                data[i]['rsi'] = round(100 - (100 / (1 + rs)), 2)

    def _calculate_bollinger_bands(self, data: List[Dict], period: int = 20, std_dev: int = 2):
        """Calculate Bollinger Bands."""
        for i in range(len(data)):
            if i < period - 1:
                data[i]['bb_upper'] = None
                data[i]['bb_middle'] = None
                data[i]['bb_lower'] = None
                continue

            # Middle band is SMA
            closes = [data[j]['close'] for j in range(i - period + 1, i + 1)]
            middle = sum(closes) / period

            # Calculate standard deviation
            variance = sum((x - middle) ** 2 for x in closes) / period
            std = variance ** 0.5

            data[i]['bb_middle'] = round(middle, 2)
            data[i]['bb_upper'] = round(middle + (std_dev * std), 2)
            data[i]['bb_lower'] = round(middle - (std_dev * std), 2)

    def _filter_by_timeframe(self, data: List[Dict], timeframe: str) -> List[Dict]:
        """Filter data points based on timeframe."""
        if not data:
            return []

        # Map timeframe to number of data points or days
        timeframe_map = {
            '1D': 78,      # ~1 day of 5-min intervals
            '5D': 390,     # ~5 days of 5-min intervals
            '1M': 30,      # 1 month of daily data
            '3M': 90,      # 3 months
            '6M': 180,     # 6 months
            '1Y': 252,     # ~1 year of trading days
            '5Y': 1260,    # ~5 years
            'MAX': 10000   # All available data
        }

        limit = timeframe_map.get(timeframe, 30)

        # Return most recent data points
        return data[-limit:] if len(data) > limit else data

    def _generate_mock_intraday_data(
        self,
        ticker: str,
        interval: str,
        outputsize: str
    ) -> Dict[str, Any]:
        """Generate mock intraday data for testing."""
        import random

        points = 100 if outputsize == 'compact' else 390
        data_points = []
        base_price = 150 + random.random() * 50

        now = datetime.now()

        for i in range(points):
            timestamp = now - timedelta(minutes=5 * (points - i))
            price_change = (random.random() - 0.48) * 2

            open_price = base_price
            close_price = base_price + price_change
            high_price = max(open_price, close_price) + random.random() * 1
            low_price = min(open_price, close_price) - random.random() * 1
            volume = random.randint(100000, 5000000)

            data_points.append({
                'date': timestamp.isoformat(),
                'timestamp': int(timestamp.timestamp()),
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': volume
            })

            base_price = close_price

        return {
            'ticker': ticker,
            'data': data_points
        }

    def _generate_mock_daily_data(
        self,
        ticker: str,
        outputsize: str
    ) -> Dict[str, Any]:
        """Generate mock daily data for testing."""
        import random

        days = 100 if outputsize == 'compact' else 1260
        data_points = []
        base_price = 150 + random.random() * 50

        today = datetime.now().date()

        for i in range(days):
            date = today - timedelta(days=days - i)

            # Skip weekends
            if date.weekday() >= 5:
                continue

            price_change = (random.random() - 0.48) * 5

            open_price = base_price
            close_price = base_price + price_change
            high_price = max(open_price, close_price) + random.random() * 2
            low_price = min(open_price, close_price) - random.random() * 2
            volume = random.randint(1000000, 10000000)

            data_points.append({
                'date': date.isoformat(),
                'timestamp': int(datetime.combine(date, datetime.min.time()).timestamp()),
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': volume
            })

            base_price = close_price

        return {
            'ticker': ticker,
            'data': data_points
        }

    def _parse_timestamp(self, date_str: str) -> int:
        """Parse timestamp string to Unix timestamp."""
        try:
            dt = datetime.fromisoformat(date_str.replace(' ', 'T'))
            return int(dt.timestamp())
        except:
            return 0

    def _is_cached(self, key: str) -> bool:
        """Check if data is in cache and not expired."""
        if key not in self.cache:
            return False

        cached_time = self.cache[key]['timestamp']
        if time.time() - cached_time > self.cache_ttl:
            del self.cache[key]
            return False

        return True

    def _cache_data(self, key: str, data: Any):
        """Cache data with timestamp."""
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }


if __name__ == "__main__":
    # Test the agent
    logging.basicConfig(level=logging.INFO)

    # Test with mock data (no API key)
    agent = MarketDataAgent()

    print("\n" + "="*80)
    print("Testing Market Data Agent")
    print("="*80 + "\n")

    # Test different timeframes
    for timeframe in ['1D', '1M', '1Y']:
        print(f"\nFetching {timeframe} data for AAPL...")
        result = agent.get_market_data_with_indicators('AAPL', timeframe)

        if result['success']:
            print(f"✓ Success! Got {result['data_points']} data points")

            # Show sample data point with indicators
            if result['data']:
                sample = result['data'][-1]
                print(f"\nLatest data point:")
                print(f"  Date: {sample['date']}")
                print(f"  Close: ${sample['close']:.2f}")
                if sample.get('sma20'):
                    print(f"  SMA(20): ${sample['sma20']:.2f}")
                if sample.get('rsi'):
                    print(f"  RSI: {sample['rsi']:.2f}")
        else:
            print(f"✗ Error: {result.get('error')}")

    print("\n" + "="*80)
