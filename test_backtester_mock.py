"""
Backtest Engine Test with Mock Data
Demonstrates backtesting functionality with simulated price data
"""

import sys
import os
import json
from datetime import datetime, timedelta
from backend.backtester import BacktestEngine

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Override price movement method with mock data
original_get_price = BacktestEngine._get_price_movement

def mock_get_price_movement(self, ticker, earnings_date, days_after):
    """Generate realistic mock price movements."""
    import random
    random.seed(f"{ticker}{earnings_date}{days_after}")

    # Simulate realistic price movements
    # Avg move is small, but some are large
    if random.random() < 0.2:  # 20% chance of large move
        return random.uniform(-8, 12)
    else:
        return random.uniform(-3, 3)

# Monkey patch for testing
BacktestEngine._get_price_movement = mock_get_price_movement

print("\n" + "="*80)
print("BACKTEST ENGINE - MOCK DATA TEST")
print("="*80 + "\n")

# Initialize engine
engine = BacktestEngine()

# Backtest parameters
ticker = "AAPL"
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 10, 31)

print(f"Backtesting {ticker} from {start_date.date()} to {end_date.date()}")
print("Using mock price data for demonstration\n")

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
    if metrics['count'] > 0:
        print(f"  {label.capitalize():8s}: {metrics['accuracy']:.1f}% "
              f"({metrics['count']} events, avg move: {metrics['avg_price_move']:+.2f}%)")

print("\nAverage Returns:")
print(f"  Positive Sentiment: {report['average_returns']['positive_sentiment']:+.2f}%")
print(f"  Negative Sentiment: {report['average_returns']['negative_sentiment']:+.2f}%")
print(f"  All Events:         {report['average_returns']['all_events']:+.2f}%")

print("\nBest Predictions:")
for i, pred in enumerate(report['best_predictions'], 1):
    print(f"  {i}. {pred['date'][:10]}: Sentiment {pred['sentiment']:+.3f}, "
          f"Actual {pred['actual_move']:+.2f}%")

print("\nWorst Predictions:")
for i, pred in enumerate(report['worst_predictions'], 1):
    print(f"  {i}. {pred['date'][:10]}: Sentiment {pred['sentiment']:+.3f}, "
          f"Actual {pred['actual_move']:+.2f}%")

print(f"\nSummary:")
print(report['summary'])

# Save report
print("\n" + "-"*80)
results_file, report_file = engine.save_backtest_report(ticker, backtest_result, report)
print(f"\n✓ Results saved to: {results_file}")
print(f"✓ Report saved to: {report_file}")

# Show detailed results
print("\n" + "-"*80)
print("Detailed Event Analysis:")
print("-"*80)

for event in backtest_result['results'][:5]:  # Show first 5
    print(f"\n{event['date'][:10]} ({event['quarter']})")
    print(f"  Sentiment: {event['sentiment']['sentiment_score']:+.3f} ({event['sentiment']['sentiment_label']})")
    print(f"  Price Moves: 1d={event['price_movements']['1_day']:+.2f}%, "
          f"5d={event['price_movements']['5_day']:+.2f}%, "
          f"30d={event['price_movements']['30_day']:+.2f}%")
    print(f"  Predictions: 1d={'✓' if event['predictions']['1_day_correct'] else '✗'}, "
          f"5d={'✓' if event['predictions']['5_day_correct'] else '✗'}, "
          f"30d={'✓' if event['predictions']['30_day_correct'] else '✗'}")

print("\n" + "="*80)
print("✓ BACKTEST ENGINE TEST COMPLETE")
print("="*80)
print("\nNote: This demo used mock price data.")
print("In production, the engine will use real historical prices from yfinance.")
print("="*80 + "\n")
