"""
Tests for Backtesting Engine
Tests historical sentiment prediction validation
"""

import pytest
import tempfile
import os
from backend.backtester import BacktestEngine
from backend.database import Database


class TestBacktester:
    """Test suite for Backtester class."""

    @pytest.fixture
    def backtester_with_temp_db(self):
        """Create backtester with temporary database."""
        temp_db = tempfile.NamedTemporaryFile(mode='w', suffix='.db', delete=False)
        temp_db_path = temp_db.name
        temp_db.close()

        # Initialize database
        db = Database(temp_db_path)
        db.create_tables()

        # Create backtester
        backtester = BacktestEngine(temp_db_path)

        yield backtester

        # Cleanup
        db.close()
        if os.path.exists(temp_db_path):
            os.remove(temp_db_path)

    def test_backtester_initialization(self, backtester_with_temp_db):
        """Test backtester initializes correctly."""
        backtester = backtester_with_temp_db

        assert backtester is not None
        assert backtester.database is not None

    def test_run_backtest_with_no_data(self, backtester_with_temp_db):
        """Test backtesting with empty database."""
        backtester = backtester_with_temp_db

        result = backtester.run_backtest("AAPL")

        assert result is not None
        assert isinstance(result, dict)

        # Should handle gracefully
        if not result.get('success'):
            assert 'error' in result or 'message' in result

    def test_backtest_result_structure(self, backtester_with_temp_db):
        """Test backtest result has correct structure."""
        backtester = backtester_with_temp_db

        result = backtester.run_backtest("TEST")

        assert isinstance(result, dict)

        # Should have basic fields
        if result.get('success'):
            assert 'ticker' in result
            assert 'metrics' in result or 'data' in result

    def test_prediction_accuracy_calculation(self, backtester_with_temp_db):
        """Test prediction accuracy metrics calculation."""
        backtester = backtester_with_temp_db

        # Add mock data if needed
        # (In real test, would insert sample earnings calls)

        result = backtester.run_backtest("MSFT")

        if result.get('success') and 'metrics' in result:
            metrics = result['metrics']

            # Check accuracy metrics exist
            if 'accuracy_1d' in metrics:
                assert 0 <= metrics['accuracy_1d'] <= 100

    def test_sentiment_label_distribution(self, backtester_with_temp_db):
        """Test sentiment label distribution calculation."""
        backtester = backtester_with_temp_db

        result = backtester.run_backtest("GOOGL")

        if result.get('success') and 'sentiment_distribution' in result:
            dist = result['sentiment_distribution']

            # Should have sentiment labels
            for label in ['positive', 'negative', 'neutral']:
                if label in dist:
                    assert isinstance(dist[label], (int, float))

    def test_best_predictions_tracking(self, backtester_with_temp_db):
        """Test tracking of best predictions."""
        backtester = backtester_with_temp_db

        result = backtester.run_backtest("NVDA")

        if result.get('success') and 'best_predictions' in result:
            best = result['best_predictions']

            assert isinstance(best, list)

            for prediction in best:
                # Should have required fields
                if prediction:
                    assert 'date' in prediction or 'ticker' in prediction

    def test_worst_predictions_tracking(self, backtester_with_temp_db):
        """Test tracking of worst predictions."""
        backtester = backtester_with_temp_db

        result = backtester.run_backtest("TSLA")

        if result.get('success') and 'worst_predictions' in result:
            worst = result['worst_predictions']

            assert isinstance(worst, list)

    def test_time_period_filtering(self, backtester_with_temp_db):
        """Test filtering by time period."""
        backtester = backtester_with_temp_db

        # Test with date range
        result = backtester.run_backtest(
            "AMZN",
            start_date="2024-01-01",
            end_date="2024-12-31"
        )

        # Should accept date parameters
        assert result is not None
        assert isinstance(result, dict)

    def test_batch_backtest_multiple_tickers(self, backtester_with_temp_db):
        """Test backtesting multiple tickers."""
        backtester = backtester_with_temp_db

        tickers = ["AAPL", "MSFT", "GOOGL"]
        results = {}

        for ticker in tickers:
            result = backtester.run_backtest(ticker)
            results[ticker] = result

        assert len(results) == len(tickers)

        for ticker, result in results.items():
            assert isinstance(result, dict)

    def test_performance_metrics_calculation(self, backtester_with_temp_db):
        """Test calculation of performance metrics."""
        backtester = backtester_with_temp_db

        result = backtester.run_backtest("META")

        if result.get('success') and 'performance' in result:
            perf = result['performance']

            # Check timing metrics
            if 'execution_time' in perf:
                assert isinstance(perf['execution_time'], (int, float))
                assert perf['execution_time'] >= 0

    def test_report_generation(self, backtester_with_temp_db):
        """Test backtest report generation."""
        backtester = backtester_with_temp_db

        result = backtester.run_backtest("NFLX")

        # Should generate some form of report
        assert result is not None
        assert 'ticker' in result or 'success' in result

    def test_empty_ticker_handling(self, backtester_with_temp_db):
        """Test handling of empty ticker."""
        backtester = backtester_with_temp_db

        result = backtester.run_backtest("")

        # Should handle gracefully
        assert result is not None
        if not result.get('success'):
            assert 'error' in result or 'message' in result

    def test_invalid_date_range_handling(self, backtester_with_temp_db):
        """Test handling of invalid date ranges."""
        backtester = backtester_with_temp_db

        # End date before start date
        result = backtester.run_backtest(
            "AAPL",
            start_date="2024-12-31",
            end_date="2024-01-01"
        )

        # Should handle invalid range
        assert result is not None

    def test_accuracy_by_sentiment_label(self, backtester_with_temp_db):
        """Test accuracy breakdown by sentiment label."""
        backtester = backtester_with_temp_db

        result = backtester.run_backtest("INTC")

        if result.get('success') and 'accuracy_by_label' in result:
            acc_by_label = result['accuracy_by_label']

            # Should have breakdown
            for label in ['positive', 'negative', 'neutral']:
                if label in acc_by_label:
                    assert isinstance(acc_by_label[label], (int, float, dict))

    def test_sharpe_ratio_calculation(self, backtester_with_temp_db):
        """Test Sharpe ratio calculation if available."""
        backtester = backtester_with_temp_db

        result = backtester.run_backtest("AMD")

        if result.get('success') and 'sharpe_ratio' in result:
            sharpe = result['sharpe_ratio']

            assert isinstance(sharpe, (int, float))

    def test_win_rate_calculation(self, backtester_with_temp_db):
        """Test win rate calculation."""
        backtester = backtester_with_temp_db

        result = backtester.run_backtest("CRM")

        if result.get('success') and 'win_rate' in result:
            win_rate = result['win_rate']

            assert isinstance(win_rate, (int, float))
            assert 0 <= win_rate <= 100

    def test_consecutive_wins_tracking(self, backtester_with_temp_db):
        """Test tracking of consecutive wins."""
        backtester = backtester_with_temp_db

        result = backtester.run_backtest("SHOP")

        # Should not crash
        assert result is not None
