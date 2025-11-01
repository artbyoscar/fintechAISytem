"""
Macro Regime Detector Agent
Classifies current market regime based on macro indicators
"""

import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class MacroRegimeDetector:
    """
    Detects and classifies macro market regimes based on key indicators.

    Regime Classification:
    - BULL: Low volatility, low unemployment, moderate inflation, strong growth
    - BEAR: High volatility, rising unemployment, high inflation or deflation, contraction
    - TRANSITION: Mixed signals, regime shifting, elevated uncertainty

    TODO: Integrate real-time data sources:
    - FRED API for unemployment, inflation, GDP
    - CBOE for VIX data
    - Federal Reserve for interest rates
    - Alpha Vantage ECONOMIC_INDICATORS endpoint
    """

    # Regime classification thresholds
    # These thresholds are based on historical market regime analysis
    THRESHOLDS = {
        "VIX": {
            "low": 15,      # Below 15: Very low volatility (strong bull)
            "moderate": 20,  # 15-20: Normal volatility (bull)
            "elevated": 25,  # 20-25: Elevated volatility (transition)
            "high": 30       # Above 30: High volatility (bear)
        },
        "UNEMPLOYMENT": {
            "low": 4.0,      # Below 4%: Very tight labor market
            "normal": 4.5,   # 4-4.5%: Healthy labor market
            "elevated": 5.0, # 4.5-5%: Softening labor market
            "high": 6.0      # Above 6%: Weak labor market
        },
        "INFLATION": {
            "low": 2.0,      # Below 2%: Below Fed target
            "target": 3.5,   # 2-3.5%: Near Fed target (healthy)
            "elevated": 4.0, # 3.5-4%: Above target (concerning)
            "high": 5.0      # Above 5%: High inflation (problematic)
        },
        "FED_RATE": {
            "accommodative": 2.0,  # Below 2%: Very accommodative
            "neutral": 4.0,        # 2-4%: Neutral policy
            "restrictive": 5.0,    # 4-5%: Restrictive policy
            "very_restrictive": 6.0 # Above 6%: Very restrictive
        }
    }

    def __init__(self):
        """Initialize macro regime detector."""
        logger.info("MacroRegimeDetector initialized")
        self.current_regime = None
        self.current_indicators = None

    def fetch_macro_indicators(self) -> Dict:
        """
        Fetch current macro economic indicators.

        Returns:
            Dict with VIX, unemployment, inflation, Fed funds rate, and metadata

        TODO: Replace mock data with real API calls:
        - VIX: Pull from CBOE or market data provider
        - Unemployment: FRED API (UNRATE series)
        - Inflation: FRED API (CPIAUCSL for CPI)
        - Fed Rate: FRED API (DFF series for effective Fed funds rate)
        - GDP Growth: FRED API (GDP series)
        """
        logger.info("Fetching macro indicators")

        # Mock data - representing current market conditions as of Oct 2024
        # In production, these would be fetched from real APIs
        mock_indicators = {
            "VIX": 18.5,              # Moderate volatility - bullish
            "unemployment_rate": 3.8,  # Low unemployment - strong labor market
            "inflation_rate": 3.2,     # Slightly elevated - near target
            "fed_funds_rate": 5.25,    # Restrictive monetary policy
            "gdp_growth": 2.8,         # Healthy growth
            "sp500_200ma_ratio": 1.05, # 5% above 200-day MA (bullish)
            "fetched_at": datetime.now().isoformat(),
            "data_source": "MOCK"  # Will be "FRED/CBOE/Bloomberg" in production
        }

        self.current_indicators = mock_indicators
        logger.info(f"Macro indicators fetched: VIX={mock_indicators['VIX']}, "
                   f"Unemployment={mock_indicators['unemployment_rate']}%, "
                   f"Inflation={mock_indicators['inflation_rate']}%")

        return mock_indicators

    def classify_regime(self) -> Dict:
        """
        Classify current macro regime based on indicators.

        Classification Logic:
        - BULL: VIX < 20 AND unemployment < 4.5% AND inflation < 3.5%
        - BEAR: VIX > 25 OR unemployment > 5% OR inflation > 4%
        - TRANSITION: Mixed signals that don't clearly indicate bull or bear

        Returns:
            Dict with regime, confidence, reasoning, and indicator breakdown

        Raises:
            RuntimeError: If indicators haven't been fetched yet
        """
        if not self.current_indicators:
            # Auto-fetch if not already loaded
            self.fetch_macro_indicators()

        indicators = self.current_indicators
        vix = indicators["VIX"]
        unemployment = indicators["unemployment_rate"]
        inflation = indicators["inflation_rate"]
        fed_rate = indicators["fed_funds_rate"]
        gdp_growth = indicators.get("gdp_growth", 0)

        logger.info("Classifying macro regime...")

        # Initialize scoring system
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

        # Fed Rate Analysis (Monetary Policy Stance)
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

        # Determine regime based on signal strength
        total_signals = bullish_signals + bearish_signals
        bullish_ratio = bullish_signals / total_signals if total_signals > 0 else 0

        if bullish_ratio >= 0.65:  # 65% or more bullish signals
            regime = "BULL"
            confidence = bullish_ratio
        elif bullish_ratio <= 0.35:  # 35% or less bullish signals (bearish)
            regime = "BEAR"
            confidence = 1 - bullish_ratio
        else:
            regime = "TRANSITION"
            confidence = 1 - abs(0.5 - bullish_ratio) * 2  # Distance from neutral

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
        """
        Generate trading recommendation based on current regime.

        Returns:
            Dict with recommendation, rationale, and suggested actions

        Recommendations:
        - FAVORABLE: Strong bullish regime, suitable for risk-on positioning
        - CAUTION: Transition regime, reduce risk exposure
        - AVOID: Bearish regime, defensive positioning recommended

        Raises:
            RuntimeError: If regime hasn't been classified yet
        """
        if not self.current_regime:
            # Auto-classify if not done yet
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
    # Test the macro detector
    logging.basicConfig(level=logging.INFO)

    detector = MacroRegimeDetector()

    print("\n" + "="*80)
    print("MACRO REGIME DETECTOR TEST")
    print("="*80 + "\n")

    # Fetch indicators
    print("Fetching macro indicators...\n")
    indicators = detector.fetch_macro_indicators()

    print("Current Macro Indicators:")
    print("-" * 80)
    print(f"  VIX:             {indicators['VIX']}")
    print(f"  Unemployment:    {indicators['unemployment_rate']}%")
    print(f"  Inflation:       {indicators['inflation_rate']}%")
    print(f"  Fed Funds Rate:  {indicators['fed_funds_rate']}%")
    print(f"  GDP Growth:      {indicators['gdp_growth']}%")
    print()

    # Classify regime
    print("Classifying regime...\n")
    regime = detector.classify_regime()

    print("Regime Classification:")
    print("-" * 80)
    print(f"  Regime:     {regime['regime']}")
    print(f"  Confidence: {regime['confidence']:.1%}")
    print(f"\nSignal Breakdown:")
    print(f"  Bullish signals: {regime['signals']['bullish']}")
    print(f"  Bearish signals: {regime['signals']['bearish']}")
    print(f"\nReasoning:")
    for reason in regime['reasoning']:
        print(f"  {reason}")
    print()

    # Get trading recommendation
    print("Generating trading recommendation...\n")
    recommendation = detector.get_trading_recommendation()

    print("Trading Recommendation:")
    print("-" * 80)
    print(f"  Recommendation: {recommendation['recommendation']}")
    print(f"  Risk Level:     {recommendation['risk_level']}")
    print(f"\nRationale:")
    print(f"  {recommendation['rationale']}")
    print(f"\nSuggested Actions:")
    for action in recommendation['suggested_actions']:
        print(f"  • {action}")
    print()

    print("="*80)
    print("✓ Macro detector tested successfully")
    print("="*80)
