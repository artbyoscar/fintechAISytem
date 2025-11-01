"""
Macro Regime Detector Agent V2
Real-time macro data from VIX and FRED API with intelligent fallbacks
"""

import sys
import logging
import os
import json
from typing import Dict, Optional
from datetime import datetime, timedelta
from pathlib import Path

# Disable curl_cffi for yfinance
os.environ["YF_NO_CURL"] = "1"

import yfinance as yf

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)


class MacroRegimeDetector:
    """
    Detects and classifies macro market regimes based on key indicators.

    Data Sources:
    - VIX: Yahoo Finance (^VIX ticker)
    - Unemployment: FRED API (UNRATE series)
    - Inflation: FRED API (CPIAUCSL for CPI)
    - Fed Funds Rate: FRED API (DFF series)
    - GDP Growth: FRED API (GDP series)

    Regime Classification:
    - BULL: Low volatility, low unemployment, moderate inflation, strong growth
    - BEAR: High volatility, rising unemployment, high inflation or deflation, contraction
    - TRANSITION: Mixed signals, regime shifting, elevated uncertainty
    """

    # Regime classification thresholds
    THRESHOLDS = {
        "VIX": {
            "low": 15,
            "moderate": 20,
            "elevated": 25,
            "high": 30
        },
        "UNEMPLOYMENT": {
            "low": 4.0,
            "normal": 4.5,
            "elevated": 5.0,
            "high": 6.0
        },
        "INFLATION": {
            "low": 2.0,
            "target": 3.5,
            "elevated": 4.0,
            "high": 5.0
        },
        "FED_RATE": {
            "accommodative": 2.0,
            "neutral": 4.0,
            "restrictive": 5.0,
            "very_restrictive": 6.0
        }
    }

    def __init__(self, cache_dir: str = "data/macro_cache", fred_api_key: Optional[str] = None):
        """
        Initialize macro regime detector.

        Args:
            cache_dir: Directory to cache macro data
            fred_api_key: FRED API key (optional)
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.cache_duration = timedelta(hours=24)  # Cache for 24 hours
        self.fred_api_key = fred_api_key
        self.current_regime = None
        self.current_indicators = None

        # Try to import fredapi if key is provided
        self.fred_client = None
        if fred_api_key:
            try:
                from fredapi import Fred
                self.fred_client = Fred(api_key=fred_api_key)
                logger.info("FRED API client initialized")
            except ImportError:
                logger.warning("fredapi not installed. Install with: pip install fredapi")
            except Exception as e:
                logger.warning(f"FRED API initialization failed: {e}")

        logger.info("MacroRegimeDetector initialized")

    def _get_cache_path(self, indicator: str) -> str:
        """Get cache file path for an indicator."""
        return os.path.join(self.cache_dir, f"{indicator}.json")

    def _is_cache_valid(self, cache_path: str) -> bool:
        """Check if cached data is still valid."""
        if not os.path.exists(cache_path):
            return False
        file_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return datetime.now() - file_time < self.cache_duration

    def _load_from_cache(self, indicator: str) -> Optional[Dict]:
        """Load indicator from cache."""
        cache_path = self._get_cache_path(indicator)
        try:
            if self._is_cache_valid(cache_path):
                with open(cache_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Cache load failed for {indicator}: {e}")
        return None

    def _save_to_cache(self, indicator: str, data: Dict):
        """Save indicator to cache."""
        cache_path = self._get_cache_path(indicator)
        try:
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Cache save failed for {indicator}: {e}")

    def fetch_vix(self) -> float:
        """
        Fetch current VIX (volatility index) from Yahoo Finance.

        Returns:
            Current VIX value

        Raises:
            RuntimeError: If VIX data unavailable
        """
        cache_key = "vix"
        cached = self._load_from_cache(cache_key)
        if cached:
            logger.info(f"Using cached VIX: {cached['value']}")
            return cached['value']

        logger.info("Fetching VIX from Yahoo Finance...")
        try:
            vix = yf.Ticker("^VIX")
            hist = vix.history(period="1d")

            if hist.empty:
                raise RuntimeError("No VIX data available")

            vix_value = float(hist['Close'].iloc[-1])

            # Cache the result
            cache_data = {
                'value': vix_value,
                'fetched_at': datetime.now().isoformat(),
                'source': 'Yahoo Finance'
            }
            self._save_to_cache(cache_key, cache_data)

            logger.info(f"VIX fetched: {vix_value:.2f}")
            return vix_value

        except Exception as e:
            logger.error(f"Failed to fetch VIX: {e}")
            # Fallback to reasonable default
            logger.warning("Using fallback VIX value: 18.5")
            return 18.5

    def fetch_fred_indicator(self, series_id: str, indicator_name: str) -> Optional[float]:
        """
        Fetch indicator from FRED API.

        Args:
            series_id: FRED series ID
            indicator_name: Human-readable name for logging

        Returns:
            Most recent value or None if unavailable
        """
        cache_key = f"fred_{series_id.lower()}"
        cached = self._load_from_cache(cache_key)
        if cached:
            logger.info(f"Using cached {indicator_name}: {cached['value']}")
            return cached['value']

        if not self.fred_client:
            logger.warning(f"FRED API not available for {indicator_name}")
            return None

        logger.info(f"Fetching {indicator_name} from FRED (series: {series_id})...")
        try:
            series = self.fred_client.get_series(series_id)
            value = float(series.iloc[-1])

            # Cache the result
            cache_data = {
                'value': value,
                'series_id': series_id,
                'fetched_at': datetime.now().isoformat(),
                'source': 'FRED API'
            }
            self._save_to_cache(cache_key, cache_data)

            logger.info(f"{indicator_name} fetched: {value:.2f}")
            return value

        except Exception as e:
            logger.error(f"Failed to fetch {indicator_name} from FRED: {e}")
            return None

    def fetch_macro_indicators(self) -> Dict:
        """
        Fetch current macro economic indicators from real sources.

        Returns:
            Dict with VIX, unemployment, inflation, Fed funds rate, and metadata
        """
        logger.info("Fetching macro indicators from real sources...")

        indicators = {
            'fetched_at': datetime.now().isoformat(),
            'data_sources': []
        }

        # 1. Fetch VIX (always available from Yahoo Finance)
        try:
            indicators['VIX'] = self.fetch_vix()
            indicators['data_sources'].append('Yahoo Finance (VIX)')
        except Exception as e:
            logger.error(f"VIX fetch failed: {e}")
            indicators['VIX'] = 18.5  # Fallback
            indicators['data_sources'].append('Fallback (VIX)')

        # 2. Fetch Unemployment Rate (UNRATE)
        unemployment = self.fetch_fred_indicator('UNRATE', 'Unemployment Rate')
        if unemployment is not None:
            indicators['unemployment_rate'] = unemployment
            indicators['data_sources'].append('FRED API (Unemployment)')
        else:
            indicators['unemployment_rate'] = 3.8  # Fallback
            indicators['data_sources'].append('Fallback (Unemployment)')
            logger.warning("Using fallback unemployment rate: 3.8%")

        # 3. Fetch Inflation Rate (CPI Year-over-Year)
        # FRED series CPIAUCSL gives us CPI, we calculate YoY change
        inflation = self.fetch_fred_indicator('CPIAUCSL', 'CPI')
        if inflation is not None and self.fred_client:
            try:
                # Get CPI from a year ago to calculate YoY change
                cpi_series = self.fred_client.get_series('CPIAUCSL')
                current_cpi = cpi_series.iloc[-1]
                year_ago_cpi = cpi_series.iloc[-13]  # Approximately 12 months ago
                inflation_rate = ((current_cpi - year_ago_cpi) / year_ago_cpi) * 100
                indicators['inflation_rate'] = float(inflation_rate)
                indicators['data_sources'].append('FRED API (Inflation)')
            except:
                indicators['inflation_rate'] = 3.2  # Fallback
                indicators['data_sources'].append('Fallback (Inflation)')
                logger.warning("Using fallback inflation rate: 3.2%")
        else:
            indicators['inflation_rate'] = 3.2  # Fallback
            indicators['data_sources'].append('Fallback (Inflation)')
            logger.warning("Using fallback inflation rate: 3.2%")

        # 4. Fetch Fed Funds Rate (DFF - Effective Federal Funds Rate)
        fed_rate = self.fetch_fred_indicator('DFF', 'Fed Funds Rate')
        if fed_rate is not None:
            indicators['fed_funds_rate'] = fed_rate
            indicators['data_sources'].append('FRED API (Fed Rate)')
        else:
            indicators['fed_funds_rate'] = 5.25  # Fallback
            indicators['data_sources'].append('Fallback (Fed Rate)')
            logger.warning("Using fallback Fed funds rate: 5.25%")

        # 5. Fetch GDP Growth (optional, uses fallback)
        gdp = self.fetch_fred_indicator('GDP', 'GDP')
        if gdp is not None and self.fred_client:
            try:
                # Calculate GDP growth rate
                gdp_series = self.fred_client.get_series('GDP')
                current_gdp = gdp_series.iloc[-1]
                previous_gdp = gdp_series.iloc[-5]  # ~1 year ago (quarterly data)
                gdp_growth = ((current_gdp - previous_gdp) / previous_gdp) * 100
                indicators['gdp_growth'] = float(gdp_growth)
                indicators['data_sources'].append('FRED API (GDP)')
            except:
                indicators['gdp_growth'] = 2.8  # Fallback
                indicators['data_sources'].append('Fallback (GDP)')
        else:
            indicators['gdp_growth'] = 2.8  # Fallback
            indicators['data_sources'].append('Fallback (GDP)')

        # S&P 500 relative to 200-day MA (from Yahoo Finance)
        try:
            sp500 = yf.Ticker("^GSPC")
            hist = sp500.history(period="1y")
            current_price = hist['Close'].iloc[-1]
            ma_200 = hist['Close'].rolling(window=200).mean().iloc[-1]
            indicators['sp500_200ma_ratio'] = float(current_price / ma_200)
            indicators['data_sources'].append('Yahoo Finance (S&P 500)')
        except:
            indicators['sp500_200ma_ratio'] = 1.05  # Fallback
            indicators['data_sources'].append('Fallback (S&P 500)')

        self.current_indicators = indicators

        logger.info(f"Macro indicators fetched from: {', '.join(set(indicators['data_sources']))}")
        logger.info(f"VIX={indicators['VIX']:.2f}, "
                   f"Unemployment={indicators['unemployment_rate']:.2f}%, "
                   f"Inflation={indicators['inflation_rate']:.2f}%")

        return indicators

    def get_macro_summary(self) -> Dict:
        """
        Get formatted summary of all macro indicators.

        Returns:
            Dict with formatted macro data
        """
        if not self.current_indicators:
            self.fetch_macro_indicators()

        return {
            'indicators': self.current_indicators,
            'formatted': {
                'VIX': f"{self.current_indicators['VIX']:.2f}",
                'Unemployment': f"{self.current_indicators['unemployment_rate']:.2f}%",
                'Inflation': f"{self.current_indicators['inflation_rate']:.2f}%",
                'Fed Rate': f"{self.current_indicators['fed_funds_rate']:.2f}%",
                'GDP Growth': f"{self.current_indicators['gdp_growth']:.2f}%",
                'S&P 500 vs 200MA': f"{(self.current_indicators['sp500_200ma_ratio'] - 1) * 100:+.2f}%"
            },
            'data_quality': {
                'real_data_sources': len([s for s in self.current_indicators['data_sources'] if 'Fallback' not in s]),
                'fallback_sources': len([s for s in self.current_indicators['data_sources'] if 'Fallback' in s]),
                'total_indicators': 6
            }
        }

    def historical_regime(self, date: datetime) -> Dict:
        """
        Determine macro regime at a historical date.

        Args:
            date: Historical date to check

        Returns:
            Dict with historical regime classification

        Note: Requires FRED API for historical data
        """
        if not self.fred_client:
            raise RuntimeError("FRED API required for historical regime analysis")

        logger.info(f"Fetching historical regime for {date.strftime('%Y-%m-%d')}")

        try:
            # Fetch historical data for the given date
            vix_hist = yf.Ticker("^VIX").history(start=date - timedelta(days=7), end=date + timedelta(days=1))
            vix_value = float(vix_hist['Close'].iloc[-1]) if not vix_hist.empty else None

            # FRED series with historical data
            unrate = self.fred_client.get_series('UNRATE', observation_start=date, observation_end=date)
            cpi_series = self.fred_client.get_series('CPIAUCSL', observation_start=date - timedelta(days=365), observation_end=date)
            dff = self.fred_client.get_series('DFF', observation_start=date, observation_end=date)

            # Calculate inflation YoY
            current_cpi = cpi_series.iloc[-1]
            year_ago_cpi = cpi_series.iloc[0]
            inflation_rate = ((current_cpi - year_ago_cpi) / year_ago_cpi) * 100

            historical_indicators = {
                'VIX': float(vix_value) if vix_value else None,
                'unemployment_rate': float(unrate.iloc[-1]) if not unrate.empty else None,
                'inflation_rate': float(inflation_rate),
                'fed_funds_rate': float(dff.iloc[-1]) if not dff.empty else None,
                'date': date.isoformat(),
                'data_source': 'FRED API + Yahoo Finance'
            }

            # Store temporarily and classify
            original_indicators = self.current_indicators
            self.current_indicators = historical_indicators
            regime = self.classify_regime()
            self.current_indicators = original_indicators

            return regime

        except Exception as e:
            logger.error(f"Failed to fetch historical regime: {e}")
            raise RuntimeError(f"Historical regime fetch failed: {e}")

    # Keep all the existing classification logic from original file
    def classify_regime(self) -> Dict:
        """Classify regime (same logic as original)."""
        if not self.current_indicators:
            self.fetch_macro_indicators()

        indicators = self.current_indicators
        vix = indicators["VIX"]
        unemployment = indicators["unemployment_rate"]
        inflation = indicators["inflation_rate"]
        fed_rate = indicators["fed_funds_rate"]
        gdp_growth = indicators.get("gdp_growth", 0)

        logger.info("Classifying macro regime...")

        bullish_signals = 0
        bearish_signals = 0
        reasoning = []

        # VIX Analysis
        if vix < self.THRESHOLDS["VIX"]["moderate"]:
            bullish_signals += 2
            reasoning.append(f"✓ Low volatility (VIX: {vix}) indicates stable bull market")
        elif vix > self.THRESHOLDS["VIX"]["elevated"]:
            bearish_signals += 2
            reasoning.append(f"✗ Elevated volatility (VIX: {vix}) signals market stress")
        else:
            reasoning.append(f"○ Moderate volatility (VIX: {vix}) is neutral")

        # Unemployment Analysis
        if unemployment < self.THRESHOLDS["UNEMPLOYMENT"]["normal"]:
            bullish_signals += 2
            reasoning.append(f"✓ Strong labor market (Unemployment: {unemployment}%)")
        elif unemployment > self.THRESHOLDS["UNEMPLOYMENT"]["elevated"]:
            bearish_signals += 2
            reasoning.append(f"✗ Weak labor market (Unemployment: {unemployment}%)")
        else:
            bullish_signals += 1
            reasoning.append(f"○ Healthy labor market (Unemployment: {unemployment}%)")

        # Inflation Analysis
        if inflation <= self.THRESHOLDS["INFLATION"]["target"]:
            bullish_signals += 2
            reasoning.append(f"✓ Inflation near target (Inflation: {inflation}%)")
        elif inflation > self.THRESHOLDS["INFLATION"]["elevated"]:
            bearish_signals += 2
            reasoning.append(f"✗ High inflation pressures (Inflation: {inflation}%)")
        else:
            bearish_signals += 1
            reasoning.append(f"○ Elevated but manageable inflation (Inflation: {inflation}%)")

        # Fed Rate Analysis
        if fed_rate < self.THRESHOLDS["FED_RATE"]["neutral"]:
            bullish_signals += 1
            reasoning.append(f"✓ Accommodative Fed policy (Rate: {fed_rate}%)")
        elif fed_rate > self.THRESHOLDS["FED_RATE"]["restrictive"]:
            bearish_signals += 1
            reasoning.append(f"✗ Restrictive Fed policy (Rate: {fed_rate}%)")
        else:
            reasoning.append(f"○ Neutral Fed policy (Rate: {fed_rate}%)")

        # GDP Growth Analysis
        if gdp_growth > 2.5:
            bullish_signals += 1
            reasoning.append(f"✓ Strong economic growth (GDP: {gdp_growth}%)")
        elif gdp_growth < 1.0:
            bearish_signals += 1
            reasoning.append(f"✗ Weak economic growth (GDP: {gdp_growth}%)")
        else:
            reasoning.append(f"○ Moderate economic growth (GDP: {gdp_growth}%)")

        total_signals = bullish_signals + bearish_signals
        bullish_ratio = bullish_signals / total_signals if total_signals > 0 else 0

        if bullish_ratio >= 0.65:
            regime = "BULL"
            confidence = bullish_ratio
        elif bullish_ratio <= 0.35:
            regime = "BEAR"
            confidence = 1 - bullish_ratio
        else:
            regime = "TRANSITION"
            confidence = 1 - abs(0.5 - bullish_ratio) * 2

        result = {
            "regime": regime,
            "confidence": round(confidence, 3),
            "reasoning": reasoning,
            "signals": {
                "bullish": bullish_signals,
                "bearish": bearish_signals,
                "bullish_ratio": round(bullish_ratio, 3)
            },
            "indicators": indicators,
            "timestamp": datetime.now().isoformat()
        }

        self.current_regime = result
        logger.info(f"Regime classified: {regime} (confidence: {confidence:.3f})")

        return result

    def get_trading_recommendation(self) -> Dict:
        """Generate trading recommendation (same logic as original)."""
        if not self.current_regime:
            self.classify_regime()

        regime_data = self.current_regime
        regime = regime_data["regime"]
        confidence = regime_data["confidence"]

        logger.info("Generating trading recommendation...")

        if regime == "BULL":
            if confidence > 0.75:
                recommendation = "FAVORABLE"
                rationale = "Strong bullish signals across multiple indicators support risk-on positioning"
                actions = [
                    "Consider increasing equity exposure",
                    "Focus on growth and cyclical sectors",
                    "Earnings beats likely to be rewarded by market",
                    "Look for momentum in high-beta names"
                ]
                risk_level = "MODERATE"
            else:
                recommendation = "FAVORABLE"
                rationale = "Moderate bullish signals suggest selective risk-taking"
                actions = [
                    "Maintain equity exposure with quality bias",
                    "Balance growth and value exposure",
                    "Monitor earnings closely for confirmation",
                    "Consider defensive hedges"
                ]
                risk_level = "MODERATE-LOW"

        elif regime == "BEAR":
            if confidence > 0.75:
                recommendation = "AVOID"
                rationale = "Strong bearish signals indicate significant downside risk"
                actions = [
                    "Reduce equity exposure significantly",
                    "Focus on defensive sectors (utilities, staples)",
                    "Earnings misses likely to be heavily punished",
                    "Consider cash or fixed income allocation"
                ]
                risk_level = "HIGH"
            else:
                recommendation = "CAUTION"
                rationale = "Bearish signals warrant defensive positioning"
                actions = [
                    "Reduce equity exposure moderately",
                    "Favor quality and dividend-paying stocks",
                    "Be selective with earnings plays",
                    "Maintain hedges and downside protection"
                ]
                risk_level = "MODERATE-HIGH"

        else:  # TRANSITION
            recommendation = "CAUTION"
            rationale = "Mixed signals and regime uncertainty suggest reducing risk"
            actions = [
                "Maintain neutral positioning",
                "Focus on high-conviction ideas only",
                "Earnings reactions may be unpredictable",
                "Wait for clearer regime confirmation",
                "Consider barbell strategy (quality + opportunistic)"
            ]
            risk_level = "MODERATE"

        result = {
            "recommendation": recommendation,
            "rationale": rationale,
            "suggested_actions": actions,
            "risk_level": risk_level,
            "regime": regime,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"Trading recommendation: {recommendation} (risk level: {risk_level})")

        return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("\n" + "="*80)
    print("MACRO REGIME DETECTOR V2 - REAL DATA TEST")
    print("="*80 + "\n")

    # Initialize (without FRED API key for now)
    detector = MacroRegimeDetector()

    # Fetch indicators
    print("Fetching macro indicators from real sources...\n")
    indicators = detector.fetch_macro_indicators()

    # Get summary
    summary = detector.get_macro_summary()

    print("Current Macro Indicators:")
    print("-" * 80)
    for name, value in summary['formatted'].items():
        print(f"  {name:20s}: {value}")

    print(f"\nData Quality:")
    print(f"  Real data sources: {summary['data_quality']['real_data_sources']}/{summary['data_quality']['total_indicators']}")
    print(f"  Fallback sources:  {summary['data_quality']['fallback_sources']}/{summary['data_quality']['total_indicators']}")

    print("\nData Sources:")
    for source in set(indicators['data_sources']):
        print(f"  • {source}")

    # Classify regime
    print("\n" + "-"*80)
    regime = detector.classify_regime()

    print(f"\nRegime Classification:")
    print(f"  Regime:     {regime['regime']}")
    print(f"  Confidence: {regime['confidence']:.1%}")
    print(f"\nSignal Breakdown:")
    print(f"  Bullish signals: {regime['signals']['bullish']}")
    print(f"  Bearish signals: {regime['signals']['bearish']}")
    print(f"\nReasoning:")
    for reason in regime['reasoning']:
        print(f"  {reason}")

    # Get recommendation
    print("\n" + "-"*80)
    recommendation = detector.get_trading_recommendation()

    print(f"\nTrading Recommendation:")
    print(f"  Recommendation: {recommendation['recommendation']}")
    print(f"  Risk Level:     {recommendation['risk_level']}")
    print(f"\nRationale:")
    print(f"  {recommendation['rationale']}")
    print(f"\nSuggested Actions:")
    for action in recommendation['suggested_actions']:
        print(f"  • {action}")

    print("\n" + "="*80)
    print("✓ MACRO DETECTOR V2 TEST COMPLETE")
    print("="*80 + "\n")
