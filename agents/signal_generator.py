"""
Trading Signal Generator
Combines sentiment analysis, macro regime, and market data to generate actionable trading signals
"""

import sys
import logging
from datetime import datetime
from typing import Dict, Optional, Tuple
import math

# Fix Windows encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)


class TradingSignalGenerator:
    """
    Generates trading signals by combining multiple data sources.

    Signal Logic:
    - BUY: Positive sentiment + bullish regime + favorable technicals
    - SELL: Negative sentiment + bearish regime + weak technicals
    - HOLD: Mixed signals or low confidence

    Risk Management:
    - Never recommend aggressive positions in BEAR regime with low confidence
    - Scale position size based on signal confidence and risk score
    - Account for volatility and sentiment-macro divergence
    """

    def __init__(self):
        """Initialize trading signal generator."""
        self.signal_history = []
        logger.info("TradingSignalGenerator initialized")

    def generate_signal(
        self,
        sentiment_data: Dict,
        macro_data: Dict,
        market_data: Optional[Dict] = None
    ) -> Dict:
        """
        Generate trading signal from analysis data.

        Args:
            sentiment_data: Sentiment analysis results
            macro_data: Macro regime classification
            market_data: Optional market data (price, volatility, etc.)

        Returns:
            Dict with signal, confidence, reasoning, position_size
        """
        logger.info("Generating trading signal...")

        # Extract key metrics
        sentiment_score = sentiment_data.get('sentiment_score', 0)
        sentiment_label = sentiment_data.get('overall_label', 'neutral')
        sentiment_confidence = sentiment_data.get('confidence', 0)

        regime = macro_data.get('regime', 'TRANSITION')
        macro_confidence = macro_data.get('confidence', 0)

        # Calculate risk score
        risk_score = self.calculate_risk_score(
            sentiment_data, macro_data, market_data
        )

        # Determine signal based on multi-factor analysis
        signal, confidence, reasoning = self._determine_signal(
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            sentiment_confidence=sentiment_confidence,
            regime=regime,
            macro_confidence=macro_confidence,
            risk_score=risk_score,
            market_data=market_data
        )

        # Calculate position size (1-10 scale)
        position_size = self._calculate_position_size(
            signal=signal,
            confidence=confidence,
            risk_score=risk_score,
            regime=regime
        )

        # Check signal validation rules
        validated_signal, validation_notes = self._validate_signal(
            signal=signal,
            confidence=confidence,
            regime=regime,
            macro_confidence=macro_confidence,
            risk_score=risk_score
        )

        result = {
            'signal': validated_signal,
            'confidence': round(confidence, 3),
            'reasoning': reasoning,
            'position_size': position_size,
            'risk_score': round(risk_score, 3),
            'validation_notes': validation_notes,
            'factors': {
                'sentiment_score': sentiment_score,
                'sentiment_label': sentiment_label,
                'sentiment_confidence': sentiment_confidence,
                'macro_regime': regime,
                'macro_confidence': macro_confidence
            },
            'timestamp': datetime.now().isoformat()
        }

        # Add to history
        self.signal_history.append(result)

        logger.info(f"Signal generated: {validated_signal} (confidence: {confidence:.2%}, position: {position_size}/10)")

        return result

    def _determine_signal(
        self,
        sentiment_score: float,
        sentiment_label: str,
        sentiment_confidence: float,
        regime: str,
        macro_confidence: float,
        risk_score: float,
        market_data: Optional[Dict] = None
    ) -> Tuple[str, float, str]:
        """
        Determine trading signal using multi-factor analysis.

        Returns:
            Tuple of (signal, confidence, reasoning)
        """
        # Calculate alignment score (-1 to +1)
        alignment_score = self._calculate_alignment_score(
            sentiment_score, regime
        )

        # Strong BUY signals
        if (regime == 'BULL' and
            sentiment_score > 0.5 and
            sentiment_confidence > 0.7 and
            alignment_score > 0.5):

            confidence = min(0.95, (sentiment_confidence + macro_confidence) / 2)
            reasoning = (
                f"Strong BUY: Bullish regime ({macro_confidence:.0%} confidence) "
                f"aligned with very positive sentiment ({sentiment_score:+.2f}). "
                f"High conviction setup with alignment score {alignment_score:.2f}."
            )
            return 'BUY', confidence, reasoning

        # Moderate BUY signals
        elif (regime == 'BULL' and
              sentiment_score > 0.2 and
              sentiment_confidence > 0.5):

            confidence = (sentiment_confidence + macro_confidence + alignment_score + 1) / 4
            reasoning = (
                f"Moderate BUY: Bullish regime with positive sentiment ({sentiment_score:+.2f}). "
                f"Favorable macro conditions support upside potential."
            )
            return 'BUY', confidence, reasoning

        # Strong SELL signals
        elif (regime == 'BEAR' and
              sentiment_score < -0.5 and
              sentiment_confidence > 0.7 and
              alignment_score > 0.5):

            confidence = min(0.95, (sentiment_confidence + macro_confidence) / 2)
            reasoning = (
                f"Strong SELL: Bearish regime ({macro_confidence:.0%} confidence) "
                f"aligned with very negative sentiment ({sentiment_score:+.2f}). "
                f"High risk of downside with alignment score {alignment_score:.2f}."
            )
            return 'SELL', confidence, reasoning

        # Moderate SELL signals
        elif (regime == 'BEAR' and
              sentiment_score < -0.2 and
              sentiment_confidence > 0.5):

            confidence = (sentiment_confidence + macro_confidence + alignment_score + 1) / 4
            reasoning = (
                f"Moderate SELL: Bearish regime with negative sentiment ({sentiment_score:+.2f}). "
                f"Unfavorable macro conditions suggest caution."
            )
            return 'SELL', confidence, reasoning

        # Contrarian BUY (positive sentiment in bear market - opportunity?)
        elif (regime == 'BEAR' and
              sentiment_score > 0.4 and
              sentiment_confidence > 0.75):

            confidence = sentiment_confidence * 0.7  # Reduced for contrarian
            reasoning = (
                f"Contrarian BUY: Strong positive sentiment ({sentiment_score:+.2f}) "
                f"diverges from bearish regime. Potential opportunity if sentiment proves correct. "
                f"HIGHER RISK - divergence trade."
            )
            return 'BUY', confidence, reasoning

        # Contrarian SELL (negative sentiment in bull market - warning?)
        elif (regime == 'BULL' and
              sentiment_score < -0.4 and
              sentiment_confidence > 0.75):

            confidence = sentiment_confidence * 0.7  # Reduced for contrarian
            reasoning = (
                f"Contrarian SELL: Strong negative sentiment ({sentiment_score:+.2f}) "
                f"diverges from bullish regime. Warning signal despite favorable macro. "
                f"HIGHER RISK - divergence trade."
            )
            return 'SELL', confidence, reasoning

        # TRANSITION regime handling
        elif regime == 'TRANSITION':
            if sentiment_score > 0.3 and sentiment_confidence > 0.7:
                confidence = sentiment_confidence * 0.6
                reasoning = (
                    f"Cautious BUY: Positive sentiment ({sentiment_score:+.2f}) "
                    f"in transitioning market. Wait for regime clarity for higher conviction."
                )
                return 'BUY', confidence, reasoning

            elif sentiment_score < -0.3 and sentiment_confidence > 0.7:
                confidence = sentiment_confidence * 0.6
                reasoning = (
                    f"Cautious SELL: Negative sentiment ({sentiment_score:+.2f}) "
                    f"in transitioning market. Macro uncertainty adds risk."
                )
                return 'SELL', confidence, reasoning

        # Default: HOLD
        confidence = max(0.4, (sentiment_confidence + macro_confidence) / 2)
        reasoning = (
            f"HOLD: Mixed signals - sentiment {sentiment_score:+.2f} ({sentiment_label}), "
            f"regime {regime}. Insufficient conviction for directional bet. "
            f"Wait for clearer setup."
        )
        return 'HOLD', confidence, reasoning

    def _calculate_alignment_score(
        self,
        sentiment_score: float,
        regime: str
    ) -> float:
        """
        Calculate alignment between sentiment and macro regime.

        Returns:
            Score from -1 (max divergence) to +1 (perfect alignment)
        """
        if regime == 'BULL':
            # Bullish regime: positive sentiment is aligned
            return sentiment_score
        elif regime == 'BEAR':
            # Bearish regime: negative sentiment is aligned
            return -sentiment_score
        else:  # TRANSITION
            # Neutral regime: any strong signal is partial alignment
            return abs(sentiment_score) * 0.5

    def calculate_risk_score(
        self,
        sentiment_data: Dict,
        macro_data: Dict,
        market_data: Optional[Dict] = None
    ) -> float:
        """
        Calculate overall risk score (0-1, higher = more risk).

        Factors:
        - Sentiment uncertainty (1 - confidence)
        - Macro regime instability
        - Stock volatility
        - Sentiment-macro divergence

        Returns:
            Risk score from 0 (low risk) to 1 (high risk)
        """
        risk_factors = []

        # 1. Sentiment uncertainty
        sentiment_confidence = sentiment_data.get('confidence', 0.5)
        sentiment_uncertainty = 1 - sentiment_confidence
        risk_factors.append(sentiment_uncertainty)

        # 2. Macro regime instability
        macro_confidence = macro_data.get('confidence', 0.5)
        regime_instability = 1 - macro_confidence
        risk_factors.append(regime_instability)

        # 3. Sentiment-macro divergence
        sentiment_score = sentiment_data.get('sentiment_score', 0)
        regime = macro_data.get('regime', 'TRANSITION')

        divergence_risk = self._calculate_divergence_risk(
            sentiment_score, regime
        )
        risk_factors.append(divergence_risk)

        # 4. Market volatility (if available)
        if market_data and 'volatility' in market_data:
            # Normalize volatility (typical range 0.1-0.5)
            volatility = market_data['volatility']
            normalized_volatility = min(1.0, volatility / 0.5)
            risk_factors.append(normalized_volatility)

        # 5. Regime-specific risk
        if regime == 'BEAR':
            risk_factors.append(0.7)  # Base risk in bear market
        elif regime == 'TRANSITION':
            risk_factors.append(0.5)  # Moderate risk in transition
        else:  # BULL
            risk_factors.append(0.3)  # Lower risk in bull market

        # Calculate weighted average
        risk_score = sum(risk_factors) / len(risk_factors)

        return max(0.0, min(1.0, risk_score))

    def _calculate_divergence_risk(
        self,
        sentiment_score: float,
        regime: str
    ) -> float:
        """
        Calculate risk from sentiment-macro divergence.

        Returns:
            Divergence risk from 0 (aligned) to 1 (max divergence)
        """
        if regime == 'BULL':
            # In bull market, negative sentiment is divergence
            if sentiment_score < 0:
                return abs(sentiment_score)  # 0 to 1
            else:
                return 0  # Aligned

        elif regime == 'BEAR':
            # In bear market, positive sentiment is divergence
            if sentiment_score > 0:
                return abs(sentiment_score)  # 0 to 1
            else:
                return 0  # Aligned

        else:  # TRANSITION
            # Any strong signal creates divergence risk
            return abs(sentiment_score) * 0.5

    def _calculate_position_size(
        self,
        signal: str,
        confidence: float,
        risk_score: float,
        regime: str
    ) -> int:
        """
        Calculate suggested position size (1-10 scale).

        Higher confidence + lower risk = larger position

        Returns:
            Position size from 1 (minimal) to 10 (maximum)
        """
        if signal == 'HOLD':
            return 0  # No position

        # Base size on confidence
        base_size = confidence * 10

        # Adjust for risk
        risk_adjustment = (1 - risk_score) * 5

        # Regime adjustment
        if regime == 'BULL' and signal == 'BUY':
            regime_multiplier = 1.2
        elif regime == 'BEAR' and signal == 'SELL':
            regime_multiplier = 1.1  # Slightly less aggressive on sells
        elif regime == 'TRANSITION':
            regime_multiplier = 0.7
        else:  # Contrarian trades
            regime_multiplier = 0.6

        # Calculate final size
        position_size = (base_size + risk_adjustment) / 2 * regime_multiplier

        # Clamp to 1-10
        return max(1, min(10, round(position_size)))

    def _validate_signal(
        self,
        signal: str,
        confidence: float,
        regime: str,
        macro_confidence: float,
        risk_score: float
    ) -> Tuple[str, str]:
        """
        Validate signal against risk management rules.

        Rules:
        1. Never recommend aggressive trades in BEAR regime with low confidence
        2. Downgrade to HOLD if risk score is very high (>0.8)
        3. Downgrade contrarian trades if macro confidence is very high

        Returns:
            Tuple of (validated_signal, validation_notes)
        """
        notes = []
        validated_signal = signal

        # Rule 1: BEAR regime + low confidence
        if (regime == 'BEAR' and
            signal == 'BUY' and
            (confidence < 0.6 or macro_confidence > 0.8)):

            validated_signal = 'HOLD'
            notes.append(
                "OVERRIDE: BUY signal downgraded to HOLD - "
                "bearish regime with insufficient confidence for contrarian position"
            )

        # Rule 2: Very high risk
        if risk_score > 0.8 and signal != 'HOLD':
            validated_signal = 'HOLD'
            notes.append(
                f"OVERRIDE: {signal} signal downgraded to HOLD - "
                f"risk score too high ({risk_score:.2f})"
            )

        # Rule 3: Contrarian trade with high macro confidence
        if regime == 'BULL' and signal == 'SELL' and macro_confidence > 0.85:
            validated_signal = 'HOLD'
            notes.append(
                "OVERRIDE: SELL signal downgraded to HOLD - "
                f"contrarian to strong bullish regime ({macro_confidence:.0%} confidence)"
            )

        if regime == 'BEAR' and signal == 'BUY' and macro_confidence > 0.85:
            validated_signal = 'HOLD'
            notes.append(
                "OVERRIDE: BUY signal downgraded to HOLD - "
                f"contrarian to strong bearish regime ({macro_confidence:.0%} confidence)"
            )

        # Rule 4: Low confidence signals
        if confidence < 0.4 and signal != 'HOLD':
            validated_signal = 'HOLD'
            notes.append(
                f"OVERRIDE: {signal} signal downgraded to HOLD - "
                f"confidence too low ({confidence:.0%})"
            )

        if not notes:
            notes.append("Signal passed validation - no overrides applied")

        return validated_signal, '; '.join(notes)

    def generate_report(
        self,
        signal_data: Dict,
        ticker: str,
        company_name: str = None
    ) -> str:
        """
        Generate human-readable trading thesis report.

        Args:
            signal_data: Signal generation results
            ticker: Stock ticker symbol
            company_name: Company name (optional)

        Returns:
            Formatted trading thesis as string
        """
        company = company_name or ticker
        signal = signal_data['signal']
        confidence = signal_data['confidence']
        reasoning = signal_data['reasoning']
        position_size = signal_data['position_size']
        risk_score = signal_data['risk_score']
        factors = signal_data['factors']
        validation_notes = signal_data.get('validation_notes', '')

        # Build report
        lines = []
        lines.append("=" * 80)
        lines.append(f"TRADING SIGNAL REPORT: {company} ({ticker})")
        lines.append("=" * 80)
        lines.append("")

        # Signal summary
        lines.append("SIGNAL SUMMARY")
        lines.append("-" * 80)
        signal_emoji = {
            'BUY': '🟢',
            'SELL': '🔴',
            'HOLD': '🟡'
        }.get(signal, '⚪')

        lines.append(f"{signal_emoji} Signal: {signal}")
        lines.append(f"   Confidence: {confidence:.0%}")
        lines.append(f"   Position Size: {position_size}/10")
        lines.append(f"   Risk Score: {risk_score:.0%}")
        lines.append("")

        # Reasoning
        lines.append("THESIS")
        lines.append("-" * 80)
        lines.append(reasoning)
        lines.append("")

        # Factors breakdown
        lines.append("ANALYSIS FACTORS")
        lines.append("-" * 80)
        lines.append(f"Sentiment Score: {factors['sentiment_score']:+.3f} ({factors['sentiment_label']})")
        lines.append(f"Sentiment Confidence: {factors['sentiment_confidence']:.0%}")
        lines.append(f"Macro Regime: {factors['macro_regime']}")
        lines.append(f"Macro Confidence: {factors['macro_confidence']:.0%}")
        lines.append("")

        # Risk assessment
        lines.append("RISK ASSESSMENT")
        lines.append("-" * 80)
        risk_level = 'LOW' if risk_score < 0.3 else 'MODERATE' if risk_score < 0.6 else 'HIGH'
        lines.append(f"Risk Level: {risk_level} ({risk_score:.0%})")

        if position_size > 7:
            lines.append("Position Sizing: AGGRESSIVE - High conviction setup")
        elif position_size > 4:
            lines.append("Position Sizing: MODERATE - Standard position")
        elif position_size > 0:
            lines.append("Position Sizing: CONSERVATIVE - Lower conviction or higher risk")
        else:
            lines.append("Position Sizing: ZERO - No position recommended")
        lines.append("")

        # Validation notes
        if "OVERRIDE" in validation_notes:
            lines.append("⚠️  RISK MANAGEMENT OVERRIDES")
            lines.append("-" * 80)
            lines.append(validation_notes)
            lines.append("")

        # Action items
        lines.append("SUGGESTED ACTIONS")
        lines.append("-" * 80)

        if signal == 'BUY':
            lines.append(f"1. Consider buying {ticker} with {position_size*10}% of intended allocation")
            lines.append("2. Set stop-loss based on recent support levels")
            lines.append("3. Monitor sentiment trends for confirmation")
            if risk_score > 0.6:
                lines.append("4. ⚠️  HIGH RISK: Consider scaling into position")

        elif signal == 'SELL':
            lines.append(f"1. Consider selling or reducing {ticker} position")
            if position_size > 5:
                lines.append("2. Exit aggressively - high conviction bearish signal")
            else:
                lines.append("2. Scale out gradually to reduce risk")
            lines.append("3. Monitor for trend reversal signals")

        else:  # HOLD
            lines.append("1. Maintain current position or stay sidelined")
            lines.append("2. Wait for clearer signals before taking action")
            lines.append("3. Monitor for sentiment or macro regime changes")
            lines.append("4. Set alerts for key technical levels")

        lines.append("")
        lines.append("=" * 80)
        lines.append(f"Report Generated: {signal_data['timestamp']}")
        lines.append("=" * 80)

        return '\n'.join(lines)

    def get_signal_history(self, limit: int = 10) -> list:
        """Get recent signal history."""
        return self.signal_history[-limit:]

    def reset(self):
        """Reset signal history."""
        self.signal_history = []
        logger.info("Signal history reset")


if __name__ == "__main__":
    # Test the signal generator
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("\n" + "="*80)
    print("TESTING TRADING SIGNAL GENERATOR")
    print("="*80 + "\n")

    generator = TradingSignalGenerator()

    # Test case 1: Strong bullish signal
    print("\n--- Test 1: Strong Bullish Setup ---")
    sentiment = {
        'sentiment_score': 0.75,
        'overall_label': 'positive',
        'confidence': 0.85
    }
    macro = {
        'regime': 'BULL',
        'confidence': 0.80
    }

    signal = generator.generate_signal(sentiment, macro)
    print(generator.generate_report(signal, "AAPL", "Apple Inc."))

    # Test case 2: Bearish divergence
    print("\n--- Test 2: Bearish Divergence (Contrarian) ---")
    sentiment = {
        'sentiment_score': -0.6,
        'overall_label': 'negative',
        'confidence': 0.90
    }
    macro = {
        'regime': 'BULL',
        'confidence': 0.75
    }

    signal = generator.generate_signal(sentiment, macro)
    print(generator.generate_report(signal, "TSLA", "Tesla Inc."))

    # Test case 3: High risk scenario
    print("\n--- Test 3: High Risk (Should Downgrade to HOLD) ---")
    sentiment = {
        'sentiment_score': 0.3,
        'overall_label': 'positive',
        'confidence': 0.45
    }
    macro = {
        'regime': 'BEAR',
        'confidence': 0.85
    }

    signal = generator.generate_signal(sentiment, macro)
    print(generator.generate_report(signal, "GME", "GameStop Corp."))

    print("\n" + "="*80)
    print("✓ SIGNAL GENERATOR TEST COMPLETE")
    print("="*80 + "\n")
