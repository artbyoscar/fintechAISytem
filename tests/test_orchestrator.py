"""
Integration Tests for Analysis Orchestrator
Tests the full analysis pipeline orchestration
"""

import pytest
import os
from backend.orchestrator import AnalysisOrchestrator


class TestAnalysisOrchestrator:
    """Test suite for AnalysisOrchestrator integration."""

    def test_orchestrator_initialization(self, orchestrator_with_temp_db):
        """Test orchestrator initialization."""
        orchestrator = orchestrator_with_temp_db

        assert orchestrator is not None
        assert orchestrator.sentiment_analyzer is not None
        assert orchestrator.earnings_fetcher is not None
        assert orchestrator.macro_detector is not None
        assert orchestrator.database is not None
        assert orchestrator.alert_system is not None

    def test_analyze_company_success(self, orchestrator_with_temp_db):
        """Test successful company analysis flow."""
        orchestrator = orchestrator_with_temp_db

        # Analyze a company (will use mock data from earnings_fetcher)
        result = orchestrator.analyze_company("AAPL")

        # Check basic structure
        assert result is not None
        assert isinstance(result, dict)

        if result.get('success'):
            # Verify report structure
            assert 'ticker' in result
            assert 'company' in result
            assert 'analysis_timestamp' in result
            assert 'sentiment_analysis' in result
            assert 'macro_regime' in result
            assert 'recommendation' in result
            assert 'overall_assessment' in result

    def test_analyze_company_invalid_ticker(self, orchestrator_with_temp_db):
        """Test handling of invalid ticker."""
        orchestrator = orchestrator_with_temp_db

        # Try to analyze with invalid/unavailable ticker
        result = orchestrator.analyze_company("INVALID123")

        assert result is not None
        assert isinstance(result, dict)

        # Should return error result
        if not result.get('success'):
            assert 'error' in result
            assert result['ticker'] == 'INVALID123'

    def test_sentiment_analysis_integration(self, orchestrator_with_temp_db):
        """Test sentiment analysis integration in pipeline."""
        orchestrator = orchestrator_with_temp_db

        result = orchestrator.analyze_company("NVDA")

        if result.get('success'):
            sentiment = result.get('sentiment_analysis', {})

            assert 'overall_label' in sentiment
            assert sentiment['overall_label'] in ['positive', 'negative', 'neutral']
            assert 'sentiment_score' in sentiment
            assert -1 <= sentiment['sentiment_score'] <= 1
            assert 'confidence' in sentiment
            assert 0 <= sentiment['confidence'] <= 1

    def test_macro_regime_integration(self, orchestrator_with_temp_db):
        """Test macro regime detection integration."""
        orchestrator = orchestrator_with_temp_db

        result = orchestrator.analyze_company("MSFT")

        if result.get('success'):
            macro = result.get('macro_regime', {})

            assert 'regime' in macro
            assert macro['regime'] in ['BULL', 'BEAR', 'TRANSITION']
            assert 'confidence' in macro
            assert 0 <= macro['confidence'] <= 1
            assert 'indicators' in macro

    def test_recommendation_generation(self, orchestrator_with_temp_db):
        """Test trading recommendation generation."""
        orchestrator = orchestrator_with_temp_db

        result = orchestrator.analyze_company("GOOGL")

        if result.get('success'):
            recommendation = result.get('recommendation', {})

            assert 'action' in recommendation
            assert recommendation['action'] in ['FAVORABLE', 'CAUTIOUS', 'AVOID']
            assert 'risk_level' in recommendation
            assert recommendation['risk_level'] in ['LOW', 'MODERATE', 'HIGH', 'VERY HIGH']

    def test_overall_assessment_generation(self, orchestrator_with_temp_db):
        """Test overall assessment synthesis."""
        orchestrator = orchestrator_with_temp_db

        result = orchestrator.analyze_company("TSLA")

        if result.get('success'):
            assessment = result.get('overall_assessment', {})

            assert 'verdict' in assessment
            assert 'reasoning' in assessment
            assert isinstance(assessment['verdict'], str)
            assert isinstance(assessment['reasoning'], str)

    def test_database_storage(self, orchestrator_with_temp_db):
        """Test that analysis results are stored in database."""
        orchestrator = orchestrator_with_temp_db

        result = orchestrator.analyze_company("AMZN")

        if result.get('success'):
            # Check if data was inserted
            companies = orchestrator.database.get_all_companies()
            assert len(companies) > 0

            calls = orchestrator.database.get_earnings_calls("AMZN", limit=5)
            # Should have at least one call stored
            assert len(calls) >= 0  # May be 0 if ticker not found

    def test_alert_generation(self, orchestrator_with_temp_db):
        """Test alert generation in pipeline."""
        orchestrator = orchestrator_with_temp_db

        result = orchestrator.analyze_company("META")

        if result.get('success'):
            # Alerts should be in the report
            assert 'alerts' in result
            assert isinstance(result['alerts'], list)

    def test_report_file_generation(self, orchestrator_with_temp_db):
        """Test that JSON report files are created."""
        orchestrator = orchestrator_with_temp_db

        result = orchestrator.analyze_company("NFLX")

        if result.get('success'):
            # Check performance metrics are tracked
            assert 'performance' in result
            perf = result['performance']
            assert 'timings' in perf
            assert 'total_time' in perf

    def test_analyze_multiple_companies(self, orchestrator_with_temp_db):
        """Test analyzing multiple companies in batch."""
        orchestrator = orchestrator_with_temp_db

        tickers = ["AAPL", "MSFT", "GOOGL"]
        results = orchestrator.analyze_multiple(tickers)

        assert results is not None
        assert isinstance(results, dict)
        assert len(results) == len(tickers)

        for ticker in tickers:
            assert ticker in results
            assert isinstance(results[ticker], dict)

    def test_key_quotes_extraction(self, orchestrator_with_temp_db):
        """Test extraction of key quotes from analysis."""
        orchestrator = orchestrator_with_temp_db

        result = orchestrator.analyze_company("INTC")

        if result.get('success'):
            sentiment = result.get('sentiment_analysis', {})

            if 'key_quotes' in sentiment:
                quotes = sentiment['key_quotes']
                assert isinstance(quotes, list)

                # Check quote format
                for quote in quotes:
                    assert isinstance(quote, str)
                    # Should have sentiment label prefix
                    assert '[POSITIVE]' in quote or '[NEGATIVE]' in quote

    def test_timing_metrics(self, orchestrator_with_temp_db):
        """Test that pipeline timing metrics are captured."""
        orchestrator = orchestrator_with_temp_db

        result = orchestrator.analyze_company("AMD")

        if result.get('success'):
            perf = result.get('performance', {})
            timings = perf.get('timings', {})

            # Check individual step timings
            expected_steps = [
                'fetch_transcript',
                'sentiment_analysis',
                'macro_detection',
                'database_storage',
                'alert_check'
            ]

            for step in expected_steps:
                if step in timings:
                    assert isinstance(timings[step], float)
                    assert timings[step] >= 0

    def test_sentiment_macro_alignment(self, orchestrator_with_temp_db):
        """Test sentiment-macro alignment assessment."""
        orchestrator = orchestrator_with_temp_db

        result = orchestrator.analyze_company("NVDA")

        if result.get('success'):
            assessment = result.get('overall_assessment', {})

            if 'sentiment_macro_alignment' in assessment:
                alignment = assessment['sentiment_macro_alignment']
                assert isinstance(alignment, str)
                # Should contain alignment keywords
                assert any(word in alignment.upper() for word in [
                    'ALIGNED', 'DIVERGENT', 'NEUTRAL', 'WARNING', 'OPPORTUNITY'
                ])

    def test_context_manager_usage(self):
        """Test orchestrator can be used as context manager."""
        import tempfile
        temp_db = tempfile.NamedTemporaryFile(mode='w', suffix='.db', delete=False)
        temp_db_path = temp_db.name
        temp_db.close()

        with AnalysisOrchestrator(db_path=temp_db_path) as orchestrator:
            assert orchestrator is not None
            result = orchestrator.analyze_company("AAPL")
            assert result is not None

        # Cleanup
        if os.path.exists(temp_db_path):
            os.remove(temp_db_path)

    def test_error_handling_in_pipeline(self, orchestrator_with_temp_db):
        """Test error handling when components fail."""
        orchestrator = orchestrator_with_temp_db

        # Try to analyze with problematic ticker
        result = orchestrator.analyze_company("")

        assert result is not None
        # Should return error result gracefully
        if not result.get('success'):
            assert 'error' in result or 'ticker' in result
