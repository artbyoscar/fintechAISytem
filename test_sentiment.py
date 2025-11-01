"""
Test script for SentimentAnalyzer
Tests with bullish, bearish, and neutral earnings call excerpts
"""

import json
import os
import sys
from datetime import datetime
from agents.sentiment_analyzer import SentimentAnalyzer

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def print_separator(char="=", length=80):
    """Print a separator line."""
    print(char * length)


def print_result(label: str, text: str, result: dict):
    """Print formatted sentiment analysis result."""
    print_separator()
    print(f"\n{label.upper()} SAMPLE")
    print_separator("-")
    print(f"\nText:\n{text}\n")
    print(f"Overall Sentiment: {result['overall_label'].upper()}")
    print(f"Sentiment Score: {result['sentiment_score']:.3f} (-1=bearish, +1=bullish)")
    print(f"Confidence: {result['overall_confidence']:.3f}")
    print(f"\nSentiment Distribution:")
    for sentiment, percentage in result['sentiment_distribution'].items():
        bar_length = int(percentage / 2)  # Scale to 50 chars max
        bar = "█" * bar_length
        print(f"  {sentiment.capitalize():8s}: {bar} {percentage:.1f}%")
    print(f"\nWeighted Scores:")
    for sentiment, score in result['weighted_scores'].items():
        print(f"  {sentiment.capitalize():8s}: {score:.3f}")
    print(f"\nTotal Sentences Analyzed: {result['total_sentences']}")
    print()


def main():
    """Run sentiment analysis tests."""
    print_separator("=")
    print("FINTECH AI SYSTEM - SENTIMENT ANALYZER TEST")
    print_separator("=")
    print()

    # Initialize analyzer
    print("Initializing SentimentAnalyzer...")
    try:
        analyzer = SentimentAnalyzer()
        print("✓ SentimentAnalyzer loaded successfully\n")
    except Exception as e:
        print(f"✗ Failed to load SentimentAnalyzer: {e}")
        return

    # Test samples
    test_samples = {
        "bullish": """Revenue exceeded expectations at $5.2B, up 47% YoY. Our cloud business
        is accelerating with record customer adoption. We're seeing unprecedented demand across
        all segments. Profit margins expanded to 28%, demonstrating operational excellence.
        We're raising full-year guidance based on this strong momentum. Customer retention
        rates hit an all-time high of 98%. Our AI initiatives are driving significant
        efficiency gains. We expect this growth trajectory to continue into next quarter.""",

        "bearish": """We're implementing cost reduction measures and expect headcount reductions
        of 15%. Margins are under pressure due to rising input costs and competitive dynamics.
        Revenue came in below expectations at $2.1B, down 8% YoY. We're seeing significant
        headwinds in our core markets. Customer churn increased to 12% this quarter.
        We're lowering full-year guidance due to deteriorating macro conditions. Several
        key product launches have been delayed. We anticipate continued challenges in the near term.""",

        "neutral": """Revenue was in line with guidance at $3.1B. We maintain our full year outlook.
        Performance varied across segments with some showing growth while others declined slightly.
        Operating margins remained stable at 22%. We continue to invest in product development
        while managing costs prudently. Market conditions remain mixed with both opportunities
        and challenges. Customer acquisition costs were flat quarter-over-quarter. We're
        executing on our strategic plan as expected."""
    }

    # Store all results
    all_results = {}

    # Analyze each sample
    for label, text in test_samples.items():
        try:
            print(f"Analyzing {label} sample...")

            # Analyze transcript
            sentence_results = analyzer.analyze_transcript(text)

            # Get overall sentiment
            overall_result = analyzer.get_overall_sentiment()

            # Store results
            all_results[label] = {
                'text': text,
                'sentence_count': len(sentence_results),
                'sentence_results': sentence_results,
                'overall_result': overall_result,
                'timestamp': datetime.now().isoformat()
            }

            # Print formatted result
            print_result(label, text, overall_result)

            # Reset analyzer for next sample
            analyzer.reset()

        except Exception as e:
            print(f"✗ Error analyzing {label} sample: {e}\n")
            continue

    # Summary statistics
    print_separator("=")
    print("SUMMARY STATISTICS")
    print_separator("=")
    print()

    for label, data in all_results.items():
        overall = data['overall_result']
        print(f"{label.upper():8s}: "
              f"{overall['overall_label']:8s} "
              f"(score: {overall['sentiment_score']:+.3f}, "
              f"confidence: {overall['overall_confidence']:.3f}, "
              f"sentences: {overall['total_sentences']})")

    # Validate results
    print("\n")
    print_separator("=")
    print("VALIDATION")
    print_separator("=")
    print()

    validations = []
    validations.append(("Bullish sample detected as positive",
                       all_results['bullish']['overall_result']['sentiment_score'] > 0.2))
    validations.append(("Bearish sample detected as negative",
                       all_results['bearish']['overall_result']['sentiment_score'] < -0.2))
    validations.append(("Neutral sample has balanced sentiment",
                       abs(all_results['neutral']['overall_result']['sentiment_score']) < 0.3))

    all_passed = True
    for check, passed in validations:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check}")
        if not passed:
            all_passed = False

    # Save results to JSON
    print("\n")
    print_separator("=")
    print("SAVING RESULTS")
    print_separator("=")
    print()

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    output_file = "data/sentiment_test_results.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"✓ Results saved to: {output_file}")
    except Exception as e:
        print(f"✗ Failed to save results: {e}")

    # Final status
    print("\n")
    print_separator("=")
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print_separator("=")
    print()


if __name__ == "__main__":
    main()
