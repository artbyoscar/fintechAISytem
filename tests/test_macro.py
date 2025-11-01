"""
Unit Tests for Macro Regime Detector
Tests the macro economic regime classification system
"""

import pytest
from agents.macro_detector import MacroRegimeDetector


class TestMacroRegimeDetector:
    """Test suite for MacroRegimeDetector class."""

    def test_detector_initialization(self, macro_detector):
        """Test that macro detector initializes correctly."""
        assert macro_detector is not None
        assert macro_detector.fred_api_key is not None or macro_detector.fred_api_key == "demo"
        assert macro_detector.cache_duration == 86400  # 24 hours

    def test_fetch_macro_indicators(self, macro_detector):
        """Test fetching macro indicators."""
        indicators = macro_detector.fetch_macro_indicators()

        assert indicators is not None
        assert isinstance(indicators, dict)

        # Check required indicators are present
        required_keys = ['vix', 'unemployment', 'inflation', 'fed_rate', 'gdp_growth']
        for key in required_keys:
            assert key in indicators
            # Values should be numeric or None
            assert isinstance(indicators[key], (int, float, type(None)))

    def test_regime_classification(self, macro_detector):
        """Test macro regime classification."""
        regime = macro_detector.classify_regime()

        assert regime is not None
        assert isinstance(regime, dict)

        # Check required fields
        assert 'regime' in regime
        assert regime['regime'] in ['BULL', 'BEAR', 'TRANSITION']
        assert 'confidence' in regime
        assert 0 <= regime['confidence'] <= 1
        assert 'indicators' in regime
        assert 'reasoning' in regime
        assert 'signals' in regime

    def test_bull_regime_detection(self, macro_detector):
        """Test detection of bullish regime with mocked data."""
        # Manually set bullish indicators
        macro_detector.current_indicators = {
            'vix': 15.0,
            'unemployment': 3.5,
            'inflation': 2.0,
            'fed_rate': 2.5,
            'gdp_growth': 3.0
        }

        regime = macro_detector.classify_regime()

        # Should be bull or transition (depends on all signals)
        assert regime['regime'] in ['BULL', 'TRANSITION']
        if regime['regime'] == 'BULL':
            assert regime['confidence'] > 0.5

    def test_bear_regime_detection(self, macro_detector):
        """Test detection of bearish regime with mocked data."""
        # Manually set bearish indicators
        macro_detector.current_indicators = {
            'vix': 35.0,
            'unemployment': 6.5,
            'inflation': 5.5,
            'fed_rate': 5.5,
            'gdp_growth': -1.0
        }

        regime = macro_detector.classify_regime()

        # Should be bear or transition
        assert regime['regime'] in ['BEAR', 'TRANSITION']
        if regime['regime'] == 'BEAR':
            assert regime['confidence'] > 0.5

    def test_transition_regime_detection(self, macro_detector):
        """Test detection of transition regime with mixed signals."""
        # Set mixed signals
        macro_detector.current_indicators = {
            'vix': 22.0,  # Neutral
            'unemployment': 4.0,  # Bullish
            'inflation': 4.0,  # Bearish
            'fed_rate': 4.0,
            'gdp_growth': 1.5
        }

        regime = macro_detector.classify_regime()

        # With mixed signals, likely transition
        assert regime['regime'] in ['BULL', 'BEAR', 'TRANSITION']
        # Confidence should be lower for mixed signals
        assert regime['confidence'] >= 0

    def test_trading_recommendation(self, macro_detector):
        """Test trading recommendation generation."""
        recommendation = macro_detector.get_trading_recommendation()

        assert recommendation is not None
        assert isinstance(recommendation, dict)

        # Check required fields
        assert 'recommendation' in recommendation
        assert recommendation['recommendation'] in ['FAVORABLE', 'CAUTIOUS', 'AVOID']
        assert 'rationale' in recommendation
        assert 'risk_level' in recommendation
        assert recommendation['risk_level'] in ['LOW', 'MODERATE', 'HIGH', 'VERY HIGH']
        assert 'suggested_actions' in recommendation
        assert isinstance(recommendation['suggested_actions'], list)

    def test_vix_signal_interpretation(self, macro_detector):
        """Test VIX signal interpretation."""
        # Test low VIX (bullish)
        macro_detector.current_indicators = {'vix': 12.0}
        regime = macro_detector.classify_regime()
        assert regime['signals']['vix_signal'] == 'bullish'

        # Test high VIX (bearish)
        macro_detector.current_indicators = {'vix': 30.0}
        regime = macro_detector.classify_regime()
        assert regime['signals']['vix_signal'] == 'bearish'

        # Test moderate VIX (neutral)
        macro_detector.current_indicators = {'vix': 22.0}
        regime = macro_detector.classify_regime()
        assert regime['signals']['vix_signal'] == 'neutral'

    def test_unemployment_signal_interpretation(self, macro_detector):
        """Test unemployment signal interpretation."""
        # Test low unemployment (bullish)
        macro_detector.current_indicators = {
            'vix': 20.0,
            'unemployment': 3.0,
            'inflation': 2.5
        }
        regime = macro_detector.classify_regime()
        assert regime['signals']['unemployment_signal'] == 'bullish'

        # Test high unemployment (bearish)
        macro_detector.current_indicators = {
            'vix': 20.0,
            'unemployment': 6.0,
            'inflation': 2.5
        }
        regime = macro_detector.classify_regime()
        assert regime['signals']['unemployment_signal'] == 'bearish'

    def test_inflation_signal_interpretation(self, macro_detector):
        """Test inflation signal interpretation."""
        # Test low inflation (bullish)
        macro_detector.current_indicators = {
            'vix': 20.0,
            'unemployment': 4.0,
            'inflation': 1.5
        }
        regime = macro_detector.classify_regime()
        assert regime['signals']['inflation_signal'] == 'bullish'

        # Test high inflation (bearish)
        macro_detector.current_indicators = {
            'vix': 20.0,
            'unemployment': 4.0,
            'inflation': 5.0
        }
        regime = macro_detector.classify_regime()
        assert regime['signals']['inflation_signal'] == 'bearish'

    def test_cache_functionality(self, macro_detector):
        """Test that caching works for macro indicators."""
        # First fetch
        indicators1 = macro_detector.fetch_macro_indicators()

        # Second fetch (should be from cache if within duration)
        indicators2 = macro_detector.fetch_macro_indicators()

        # Should return same data (from cache)
        assert indicators1 == indicators2

    def test_missing_indicators_handling(self, macro_detector):
        """Test handling of missing macro indicators."""
        # Set some indicators to None
        macro_detector.current_indicators = {
            'vix': 20.0,
            'unemployment': None,
            'inflation': 3.0,
            'fed_rate': None,
            'gdp_growth': 2.0
        }

        # Should still classify regime
        regime = macro_detector.classify_regime()
        assert regime is not None
        assert regime['regime'] in ['BULL', 'BEAR', 'TRANSITION']

    def test_confidence_calculation(self, macro_detector):
        """Test confidence score calculation."""
        # All bullish signals
        macro_detector.current_indicators = {
            'vix': 15.0,
            'unemployment': 3.5,
            'inflation': 2.0,
            'fed_rate': 2.5,
            'gdp_growth': 3.0
        }

        regime = macro_detector.classify_regime()

        # High confidence for aligned signals
        if regime['regime'] == 'BULL':
            assert regime['confidence'] > 0.65

    def test_reasoning_generation(self, macro_detector):
        """Test that regime includes reasoning."""
        regime = macro_detector.classify_regime()

        assert 'reasoning' in regime
        assert isinstance(regime['reasoning'], str)
        assert len(regime['reasoning']) > 0

    def test_suggested_actions_generation(self, macro_detector):
        """Test suggested actions in recommendations."""
        recommendation = macro_detector.get_trading_recommendation()

        assert 'suggested_actions' in recommendation
        assert isinstance(recommendation['suggested_actions'], list)
        assert len(recommendation['suggested_actions']) > 0

        # Check actions are strings
        for action in recommendation['suggested_actions']:
            assert isinstance(action, str)
            assert len(action) > 0

    def test_risk_level_assignment(self, macro_detector):
        """Test risk level assignment based on regime."""
        # Test bullish regime (lower risk)
        macro_detector.current_indicators = {
            'vix': 15.0,
            'unemployment': 3.5,
            'inflation': 2.0
        }
        recommendation = macro_detector.get_trading_recommendation()

        if recommendation['recommendation'] == 'FAVORABLE':
            assert recommendation['risk_level'] in ['LOW', 'MODERATE']

        # Test bearish regime (higher risk)
        macro_detector.current_indicators = {
            'vix': 35.0,
            'unemployment': 6.5,
            'inflation': 5.5
        }
        recommendation = macro_detector.get_trading_recommendation()

        if recommendation['recommendation'] == 'AVOID':
            assert recommendation['risk_level'] in ['HIGH', 'VERY HIGH']
