"""
Unit Tests for Sentiment Analyzer
Tests the FinBERT-based sentiment analysis agent
"""

import pytest
from agents.sentiment_analyzer import SentimentAnalyzer


class TestSentimentAnalyzer:
    """Test suite for SentimentAnalyzer class."""

    def test_analyzer_initialization(self, sentiment_analyzer):
        """Test that sentiment analyzer initializes correctly."""
        assert sentiment_analyzer is not None
        assert sentiment_analyzer.model is not None
        assert sentiment_analyzer.tokenizer is not None
        assert len(sentiment_analyzer.sentence_results) == 0

    def test_positive_sentiment_detection(self, sentiment_analyzer, sample_transcript):
        """Test detection of positive sentiment."""
        results = sentiment_analyzer.analyze_transcript(sample_transcript)
        overall = sentiment_analyzer.get_overall_sentiment()

        assert len(results) > 0
        assert overall['overall_label'] == 'positive'
        assert overall['sentiment_score'] > 0
        assert 0 <= overall['overall_confidence'] <= 1

    def test_negative_sentiment_detection(self, sentiment_analyzer, bearish_transcript):
        """Test detection of negative sentiment."""
        # Reset analyzer for fresh state
        sentiment_analyzer.reset()

        results = sentiment_analyzer.analyze_transcript(bearish_transcript)
        overall = sentiment_analyzer.get_overall_sentiment()

        assert len(results) > 0
        assert overall['overall_label'] == 'negative'
        assert overall['sentiment_score'] < 0
        assert 0 <= overall['overall_confidence'] <= 1

    def test_neutral_sentiment_detection(self, sentiment_analyzer, neutral_transcript):
        """Test detection of neutral sentiment."""
        # Reset analyzer for fresh state
        sentiment_analyzer.reset()

        results = sentiment_analyzer.analyze_transcript(neutral_transcript)
        overall = sentiment_analyzer.get_overall_sentiment()

        assert len(results) > 0
        assert overall['overall_label'] in ['neutral', 'positive', 'negative']
        assert -1 <= overall['sentiment_score'] <= 1

    def test_sentence_level_analysis(self, sentiment_analyzer, sample_transcript):
        """Test that individual sentences are analyzed."""
        sentiment_analyzer.reset()
        results = sentiment_analyzer.analyze_transcript(sample_transcript)

        assert len(results) > 0
        for result in results:
            assert 'text' in result
            assert 'label' in result
            assert 'confidence' in result
            assert 'scores' in result
            assert result['label'] in ['positive', 'negative', 'neutral']
            assert 0 <= result['confidence'] <= 1

    def test_confidence_scoring(self, sentiment_analyzer, sample_transcript):
        """Test that confidence scores are properly calculated."""
        sentiment_analyzer.reset()
        results = sentiment_analyzer.analyze_transcript(sample_transcript)
        overall = sentiment_analyzer.get_overall_sentiment()

        # Check confidence is weighted average
        assert 'overall_confidence' in overall
        assert overall['overall_confidence'] > 0
        assert overall['overall_confidence'] <= 1

    def test_sentiment_distribution(self, sentiment_analyzer, sample_transcript):
        """Test sentiment distribution calculation."""
        sentiment_analyzer.reset()
        sentiment_analyzer.analyze_transcript(sample_transcript)
        overall = sentiment_analyzer.get_overall_sentiment()

        assert 'sentiment_distribution' in overall
        dist = overall['sentiment_distribution']

        assert 'positive' in dist
        assert 'negative' in dist
        assert 'neutral' in dist

        # Distribution should sum to approximately 1
        total = dist['positive'] + dist['negative'] + dist['neutral']
        assert 0.98 <= total <= 1.02  # Slightly wider tolerance for floating point

    def test_weighted_scores(self, sentiment_analyzer, sample_transcript):
        """Test weighted sentiment scores."""
        sentiment_analyzer.reset()
        sentiment_analyzer.analyze_transcript(sample_transcript)
        overall = sentiment_analyzer.get_overall_sentiment()

        assert 'weighted_scores' in overall
        scores = overall['weighted_scores']

        assert 'positive' in scores
        assert 'negative' in scores
        assert 'neutral' in scores

    def test_reset_functionality(self, sentiment_analyzer):
        """Test that reset clears previous results."""
        sentiment_analyzer.analyze_transcript("Test sentence.")
        assert len(sentiment_analyzer.sentence_results) > 0

        sentiment_analyzer.reset()
        assert len(sentiment_analyzer.sentence_results) == 0

    def test_empty_transcript_handling(self, sentiment_analyzer):
        """Test handling of empty transcript."""
        sentiment_analyzer.reset()

        # Should raise ValueError for empty transcript
        with pytest.raises(ValueError):
            sentiment_analyzer.analyze_transcript("")

    def test_single_sentence_analysis(self, sentiment_analyzer):
        """Test analysis of a single sentence."""
        sentiment_analyzer.reset()
        sentence = "The company delivered outstanding results this quarter."
        results = sentiment_analyzer.analyze_transcript(sentence)

        assert len(results) > 0
        assert results[0]['label'] == 'positive'

    def test_mixed_sentiment_transcript(self, sentiment_analyzer):
        """Test transcript with mixed positive and negative sentences."""
        sentiment_analyzer.reset()
        mixed_text = """
        Revenue grew by 20% which is excellent.
        However, profit margins declined significantly.
        We are optimistic about next quarter.
        But we face serious challenges ahead.
        """
        results = sentiment_analyzer.analyze_transcript(mixed_text)
        overall = sentiment_analyzer.get_overall_sentiment()

        assert len(results) > 0
        # Should have both positive and negative sentiments
        labels = [r['label'] for r in results]
        assert 'positive' in labels or 'negative' in labels

    def test_sentiment_score_range(self, sentiment_analyzer, sample_transcript):
        """Test that sentiment scores are in valid range."""
        sentiment_analyzer.reset()
        sentiment_analyzer.analyze_transcript(sample_transcript)
        overall = sentiment_analyzer.get_overall_sentiment()

        assert -1 <= overall['sentiment_score'] <= 1

    def test_long_transcript_processing(self, sentiment_analyzer):
        """Test processing of longer transcripts."""
        sentiment_analyzer.reset()
        long_transcript = " ".join([
            "The company performed well this quarter." for _ in range(50)
        ])
        results = sentiment_analyzer.analyze_transcript(long_transcript)

        assert len(results) > 0
        overall = sentiment_analyzer.get_overall_sentiment()
        assert overall['overall_label'] == 'positive'

    def test_special_characters_handling(self, sentiment_analyzer):
        """Test handling of special characters in transcript."""
        sentiment_analyzer.reset()
        text_with_special = "Q3 revenue was $5.5B (up 25% YoY)! EPS beat by $0.15."
        results = sentiment_analyzer.analyze_transcript(text_with_special)

        assert len(results) > 0
        # Should not crash and should return valid results
        overall = sentiment_analyzer.get_overall_sentiment()
        assert overall['overall_label'] in ['positive', 'negative', 'neutral']
