"""
Backtesting Engine
Tests sentiment analysis predictions against actual price movements
"""

import sys
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Disable curl_cffi for yfinance
os.environ["YF_NO_CURL"] = "1"

import pandas as pd
import yfinance as yf

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)


class BacktestEngine:
    """
    Backtesting engine for sentiment analysis predictions.

    Tests whether sentiment scores correlate with actual price movements
    after earnings calls.
    """

    def __init__(self, output_dir: str = "data/backtests"):
        """
        Initialize backtest engine.

        Args:
            output_dir: Directory to save backtest results
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info("BacktestEngine initialized")

    def _generate_quarterly_dates(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[datetime]:
        """
        Generate quarterly earnings dates (simplified for testing).

        Assumes earnings in late Jan, Apr, Jul, Oct
        (approximation of Q4, Q1, Q2, Q3 reports).

        Args:
            start_date: Start of backtest period
            end_date: End of backtest period

        Returns:
            List of earnings dates
        """
        earnings_dates = []
        current_year = start_date.year

        # Typical earnings months: Jan (Q4), Apr (Q1), Jul (Q2), Oct (Q3)
        earnings_months = [1, 4, 7, 10]
        earnings_day = 25  # Assume late month

        while True:
            for month in earnings_months:
                date = datetime(current_year, month, earnings_day)

                if start_date <= date <= end_date:
                    earnings_dates.append(date)

                if date > end_date:
                    return earnings_dates

            current_year += 1

            if current_year > end_date.year + 1:
                break

        return earnings_dates

    def _get_price_movement(
        self,
        ticker: str,
        earnings_date: datetime,
        days_after: int
    ) -> Optional[float]:
        """
        Calculate price movement after earnings date.

        Args:
            ticker: Stock ticker
            earnings_date: Earnings call date
            days_after: Days to measure movement (1, 5, 30)

        Returns:
            Price change percentage or None if data unavailable
        """
        try:
            # Fetch historical prices
            # Add buffer days to account for weekends
            start = earnings_date - timedelta(days=5)
            end = earnings_date + timedelta(days=days_after + 10)

            stock = yf.Ticker(ticker)
            hist = stock.history(start=start, end=end)

            if hist.empty or len(hist) < days_after + 1:
                logger.warning(f"Insufficient price data for {ticker} at {earnings_date}")
                return None

            # Find closest trading day to earnings date
            hist_dates = hist.index
            earnings_idx = hist_dates.searchsorted(earnings_date)

            if earnings_idx >= len(hist):
                earnings_idx = len(hist) - 1

            # Get prices
            earnings_close = hist['Close'].iloc[earnings_idx]

            # Get price N days after (accounting for trading days)
            future_idx = min(earnings_idx + days_after, len(hist) - 1)
            future_close = hist['Close'].iloc[future_idx]

            # Calculate percentage change
            price_change = ((future_close - earnings_close) / earnings_close) * 100

            return float(price_change)

        except Exception as e:
            logger.error(f"Failed to get price movement: {e}")
            return None

    def _generate_mock_sentiment(self, ticker: str, date: datetime) -> Dict:
        """
        Generate mock sentiment score for testing.

        In production, this would use the actual sentiment analyzer
        with historical earnings transcripts.

        Args:
            ticker: Stock ticker
            date: Earnings date

        Returns:
            Mock sentiment analysis result
        """
        import random

        # Simulate sentiment based on market conditions
        # In production, use actual SentimentAnalyzer with transcript
        random.seed(f"{ticker}{date.isoformat()}")

        sentiment_score = random.uniform(-0.8, 0.8)

        if sentiment_score > 0.3:
            label = "positive"
        elif sentiment_score < -0.3:
            label = "negative"
        else:
            label = "neutral"

        return {
            'sentiment_score': sentiment_score,
            'sentiment_label': label,
            'confidence': random.uniform(0.6, 0.95),
            'ticker': ticker,
            'date': date.isoformat()
        }

    def backtest_ticker(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime
    ) -> Dict:
        """
        Backtest sentiment predictions for a ticker.

        Args:
            ticker: Stock ticker symbol
            start_date: Start of backtest period
            end_date: End of backtest period

        Returns:
            Dict with backtest results
        """
        ticker = ticker.upper()
        logger.info(f"Starting backtest for {ticker} from {start_date.date()} to {end_date.date()}")

        # Generate earnings dates
        earnings_dates = self._generate_quarterly_dates(start_date, end_date)
        logger.info(f"Testing {len(earnings_dates)} earnings events")

        results = []

        for earnings_date in earnings_dates:
            try:
                # Get sentiment prediction
                # In production, use actual sentiment analyzer with historical transcript
                sentiment = self._generate_mock_sentiment(ticker, earnings_date)

                # Get actual price movements
                price_1d = self._get_price_movement(ticker, earnings_date, 1)
                price_5d = self._get_price_movement(ticker, earnings_date, 5)
                price_30d = self._get_price_movement(ticker, earnings_date, 30)

                # Skip if we couldn't get price data
                if price_1d is None:
                    logger.warning(f"Skipping {earnings_date.date()} - no price data")
                    continue

                # Determine if prediction was correct
                # Positive sentiment should correlate with positive price movement
                prediction_correct_1d = (
                    (sentiment['sentiment_score'] > 0.2 and price_1d > 0) or
                    (sentiment['sentiment_score'] < -0.2 and price_1d < 0)
                )

                prediction_correct_5d = (
                    (sentiment['sentiment_score'] > 0.2 and price_5d > 0) or
                    (sentiment['sentiment_score'] < -0.2 and price_5d < 0)
                ) if price_5d is not None else None

                prediction_correct_30d = (
                    (sentiment['sentiment_score'] > 0.2 and price_30d > 0) or
                    (sentiment['sentiment_score'] < -0.2 and price_30d < 0)
                ) if price_30d is not None else None

                # Store result
                result = {
                    'date': earnings_date.isoformat(),
                    'quarter': f"Q{(earnings_date.month - 1) // 3 + 1} {earnings_date.year}",
                    'sentiment': sentiment,
                    'price_movements': {
                        '1_day': price_1d,
                        '5_day': price_5d,
                        '30_day': price_30d
                    },
                    'predictions': {
                        '1_day_correct': prediction_correct_1d,
                        '5_day_correct': prediction_correct_5d,
                        '30_day_correct': prediction_correct_30d
                    },
                    'magnitude_match': abs(sentiment['sentiment_score']) > 0.3 and abs(price_1d) > 2.0
                }

                results.append(result)
                logger.info(f"  {earnings_date.date()}: Sentiment={sentiment['sentiment_score']:.3f}, "
                           f"Price 1d={price_1d:+.2f}%")

            except Exception as e:
                logger.error(f"Failed to process {earnings_date.date()}: {e}")
                continue

        backtest_result = {
            'ticker': ticker,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'total_events': len(results),
            'results': results,
            'timestamp': datetime.now().isoformat()
        }

        logger.info(f"Backtest completed: {len(results)} events analyzed")

        return backtest_result

    def generate_backtest_report(self, backtest_result: Dict) -> Dict:
        """
        Generate comprehensive backtest report with metrics.

        Args:
            backtest_result: Result from backtest_ticker()

        Returns:
            Dict with detailed performance metrics
        """
        results = backtest_result['results']
        ticker = backtest_result['ticker']

        if not results:
            return {
                'error': 'No results to analyze',
                'ticker': ticker
            }

        logger.info(f"Generating backtest report for {ticker}")

        # Overall accuracy
        total = len(results)
        correct_1d = sum(1 for r in results if r['predictions']['1_day_correct'])
        correct_5d = sum(1 for r in results if r['predictions'].get('5_day_correct'))
        correct_30d = sum(1 for r in results if r['predictions'].get('30_day_correct'))

        overall_accuracy = {
            '1_day': (correct_1d / total) * 100 if total > 0 else 0,
            '5_day': (correct_5d / total) * 100 if total > 0 else 0,
            '30_day': (correct_30d / total) * 100 if total > 0 else 0
        }

        # Accuracy by sentiment label
        by_sentiment = {'positive': [], 'negative': [], 'neutral': []}
        for r in results:
            label = r['sentiment']['sentiment_label']
            by_sentiment[label].append(r)

        sentiment_accuracy = {}
        for label, events in by_sentiment.items():
            if events:
                correct = sum(1 for e in events if e['predictions']['1_day_correct'])
                sentiment_accuracy[label] = {
                    'count': len(events),
                    'accuracy': (correct / len(events)) * 100,
                    'avg_price_move': sum(e['price_movements']['1_day'] for e in events) / len(events)
                }

        # Best and worst predictions
        sorted_results = sorted(
            results,
            key=lambda x: abs(x['sentiment']['sentiment_score'] - x['price_movements']['1_day']/100)
        )

        best_predictions = sorted_results[:3]
        worst_predictions = sorted_results[-3:]

        # Average returns by sentiment
        positive_events = [r for r in results if r['sentiment']['sentiment_score'] > 0.2]
        negative_events = [r for r in results if r['sentiment']['sentiment_score'] < -0.2]

        avg_return_positive = (
            sum(r['price_movements']['1_day'] for r in positive_events) / len(positive_events)
            if positive_events else 0
        )

        avg_return_negative = (
            sum(r['price_movements']['1_day'] for r in negative_events) / len(negative_events)
            if negative_events else 0
        )

        # Generate report
        report = {
            'ticker': ticker,
            'period': {
                'start': backtest_result['start_date'],
                'end': backtest_result['end_date'],
                'total_events': total
            },
            'overall_accuracy': overall_accuracy,
            'accuracy_by_sentiment': sentiment_accuracy,
            'average_returns': {
                'positive_sentiment': avg_return_positive,
                'negative_sentiment': avg_return_negative,
                'all_events': sum(r['price_movements']['1_day'] for r in results) / total
            },
            'best_predictions': [
                {
                    'date': p['date'],
                    'sentiment': p['sentiment']['sentiment_score'],
                    'actual_move': p['price_movements']['1_day']
                }
                for p in best_predictions
            ],
            'worst_predictions': [
                {
                    'date': p['date'],
                    'sentiment': p['sentiment']['sentiment_score'],
                    'actual_move': p['price_movements']['1_day']
                }
                for p in worst_predictions
            ],
            'summary': self._generate_summary(overall_accuracy, sentiment_accuracy),
            'timestamp': datetime.now().isoformat()
        }

        return report

    def _generate_summary(
        self,
        overall_accuracy: Dict,
        sentiment_accuracy: Dict
    ) -> str:
        """Generate human-readable summary."""
        acc_1d = overall_accuracy['1_day']

        if acc_1d >= 70:
            performance = "EXCELLENT"
        elif acc_1d >= 60:
            performance = "GOOD"
        elif acc_1d >= 50:
            performance = "FAIR"
        else:
            performance = "NEEDS IMPROVEMENT"

        summary = f"""
Backtest Performance: {performance}

The sentiment analysis achieved {acc_1d:.1f}% accuracy in predicting 1-day price direction
after earnings calls. This is {'above' if acc_1d > 50 else 'at' if acc_1d == 50 else 'below'}
random chance (50%), {'indicating the model has predictive value' if acc_1d > 50 else 'suggesting the model needs improvement'}.

Sentiment-specific performance:
"""

        for label, metrics in sentiment_accuracy.items():
            summary += f"- {label.capitalize()}: {metrics['accuracy']:.1f}% accuracy ({metrics['count']} events)\n"

        return summary.strip()

    def save_backtest_report(
        self,
        ticker: str,
        backtest_result: Dict,
        report: Dict
    ):
        """
        Save backtest results and report to files.

        Args:
            ticker: Stock ticker
            backtest_result: Raw backtest results
            report: Generated report
        """
        ticker = ticker.upper()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save raw results
        results_file = os.path.join(
            self.output_dir,
            f"{ticker}_backtest_raw_{timestamp}.json"
        )

        with open(results_file, 'w') as f:
            json.dump(backtest_result, f, indent=2)

        logger.info(f"Raw results saved: {results_file}")

        # Save report
        report_file = os.path.join(
            self.output_dir,
            f"{ticker}_backtest_report_{timestamp}.json"
        )

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Report saved: {report_file}")

        return results_file, report_file


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("\n" + "="*80)
    print("BACKTEST ENGINE - TEST")
    print("="*80 + "\n")

    # Initialize engine
    engine = BacktestEngine()

    # Backtest parameters
    ticker = "AAPL"
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 10, 31)

    print(f"Backtesting {ticker} from {start_date.date()} to {end_date.date()}\n")

    # Run backtest
    print("Running backtest...")
    backtest_result = engine.backtest_ticker(ticker, start_date, end_date)

    # Generate report
    print("\nGenerating report...")
    report = engine.generate_backtest_report(backtest_result)

    # Display results
    print("\n" + "="*80)
    print("BACKTEST REPORT")
    print("="*80 + "\n")

    print(f"Ticker: {report['ticker']}")
    print(f"Period: {report['period']['start']} to {report['period']['end']}")
    print(f"Total Events: {report['period']['total_events']}\n")

    print("Overall Accuracy:")
    print(f"  1-Day:  {report['overall_accuracy']['1_day']:.1f}%")
    print(f"  5-Day:  {report['overall_accuracy']['5_day']:.1f}%")
    print(f"  30-Day: {report['overall_accuracy']['30_day']:.1f}%\n")

    print("Accuracy by Sentiment:")
    for label, metrics in report['accuracy_by_sentiment'].items():
        print(f"  {label.capitalize():8s}: {metrics['accuracy']:.1f}% "
              f"({metrics['count']} events, avg move: {metrics['avg_price_move']:+.2f}%)")

    print("\nAverage Returns:")
    print(f"  Positive Sentiment: {report['average_returns']['positive_sentiment']:+.2f}%")
    print(f"  Negative Sentiment: {report['average_returns']['negative_sentiment']:+.2f}%")
    print(f"  All Events:         {report['average_returns']['all_events']:+.2f}%")

    print(f"\n{report['summary']}")

    # Save report
    print("\n" + "-"*80)
    results_file, report_file = engine.save_backtest_report(ticker, backtest_result, report)
    print(f"\n✓ Results saved to: {results_file}")
    print(f"✓ Report saved to: {report_file}")

    print("\n" + "="*80)
    print("✓ BACKTEST ENGINE TEST COMPLETE")
    print("="*80 + "\n")
