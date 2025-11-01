"""
Sentiment Analyzer for Financial Text using FinBERT
Production-ready sentiment analysis agent for earnings call transcripts
"""

import logging
import re
from typing import Dict, List, Optional
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Financial sentiment analyzer using ProsusAI/finbert model.
    Analyzes earnings call transcripts and financial text for sentiment signals.
    """

    def __init__(self, model_name: str = "ProsusAI/finbert"):
        """
        Initialize the sentiment analyzer with FinBERT model.

        Args:
            model_name: HuggingFace model identifier (default: ProsusAI/finbert)

        Raises:
            RuntimeError: If model fails to load
        """
        try:
            logger.info(f"Loading FinBERT model: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.eval()  # Set to evaluation mode

            # Move to GPU if available
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            logger.info(f"Model loaded successfully on {self.device}")

            # FinBERT label mapping
            self.labels = ['positive', 'negative', 'neutral']

            # Store sentence-level results for aggregation
            self.sentence_results = []

        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise RuntimeError(f"Model initialization failed: {str(e)}")

    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text snippet.

        Args:
            text: Financial text to analyze

        Returns:
            Dict containing:
                - label: predicted sentiment (positive/negative/neutral)
                - scores: probability distribution across all labels
                - confidence: probability of predicted label

        Raises:
            ValueError: If text is empty or invalid
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            # Tokenize input text
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            ).to(self.device)

            # Get model predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            # Convert to numpy for easier handling
            scores = predictions.cpu().numpy()[0]

            # Get predicted label
            predicted_idx = np.argmax(scores)
            predicted_label = self.labels[predicted_idx]
            confidence = float(scores[predicted_idx])

            result = {
                'label': predicted_label,
                'confidence': confidence,
                'scores': {
                    'positive': float(scores[0]),
                    'negative': float(scores[1]),
                    'neutral': float(scores[2])
                }
            }

            logger.debug(f"Analyzed text (length: {len(text)}): {predicted_label} ({confidence:.3f})")
            return result

        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            raise RuntimeError(f"Analysis failed: {str(e)}")

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences for granular analysis.

        Args:
            text: Input text to split

        Returns:
            List of sentence strings
        """
        # Simple sentence splitting using regex
        # Handles common abbreviations in financial text
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

        # Filter out empty sentences and very short ones (likely noise)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

        logger.debug(f"Split text into {len(sentences)} sentences")
        return sentences

    def analyze_transcript(self, transcript: str) -> List[Dict]:
        """
        Analyze entire earnings call transcript sentence-by-sentence.

        Args:
            transcript: Full earnings call transcript text

        Returns:
            List of dicts, each containing:
                - text: original sentence
                - label: sentiment label
                - confidence: confidence score
                - scores: full probability distribution

        Raises:
            ValueError: If transcript is empty
        """
        if not transcript or not transcript.strip():
            raise ValueError("Transcript cannot be empty")

        logger.info(f"Analyzing transcript (length: {len(transcript)} chars)")

        try:
            sentences = self._split_into_sentences(transcript)
            results = []

            for idx, sentence in enumerate(sentences):
                try:
                    sentiment = self.analyze_sentiment(sentence)
                    results.append({
                        'sentence_index': idx,
                        'text': sentence,
                        'label': sentiment['label'],
                        'confidence': sentiment['confidence'],
                        'scores': sentiment['scores']
                    })
                except Exception as e:
                    logger.warning(f"Failed to analyze sentence {idx}: {str(e)}")
                    continue

            # Store for aggregation
            self.sentence_results = results

            logger.info(f"Successfully analyzed {len(results)}/{len(sentences)} sentences")
            return results

        except Exception as e:
            logger.error(f"Transcript analysis failed: {str(e)}")
            raise RuntimeError(f"Transcript analysis failed: {str(e)}")

    def get_overall_sentiment(self) -> Dict:
        """
        Aggregate sentence-level sentiments into overall sentiment score.

        Uses weighted average based on confidence scores to compute
        overall sentiment distribution and label.

        Returns:
            Dict containing:
                - overall_label: dominant sentiment across transcript
                - overall_confidence: aggregated confidence score
                - sentiment_distribution: percentage breakdown
                - total_sentences: number of sentences analyzed
                - sentiment_counts: raw counts per label

        Raises:
            RuntimeError: If no sentences have been analyzed yet
        """
        if not self.sentence_results:
            raise RuntimeError("No sentences analyzed yet. Call analyze_transcript first.")

        try:
            total_sentences = len(self.sentence_results)

            # Initialize counters
            label_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
            weighted_scores = {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0}

            # Aggregate scores with confidence weighting
            for result in self.sentence_results:
                label = result['label']
                confidence = result['confidence']

                label_counts[label] += 1

                # Weight each label's score by the sentence confidence
                for lbl in self.labels:
                    weighted_scores[lbl] += result['scores'][lbl] * confidence

            # Normalize weighted scores
            total_weight = sum(weighted_scores.values())
            if total_weight > 0:
                weighted_scores = {k: v/total_weight for k, v in weighted_scores.items()}

            # Determine overall label
            overall_label = max(weighted_scores, key=weighted_scores.get)
            overall_confidence = weighted_scores[overall_label]

            # Calculate distribution percentages
            sentiment_distribution = {
                label: (count / total_sentences) * 100
                for label, count in label_counts.items()
            }

            # Calculate sentiment score (-1 to +1 scale)
            sentiment_score = (
                weighted_scores['positive'] - weighted_scores['negative']
            )

            result = {
                'overall_label': overall_label,
                'overall_confidence': float(overall_confidence),
                'sentiment_score': float(sentiment_score),  # -1 (bearish) to +1 (bullish)
                'sentiment_distribution': sentiment_distribution,
                'weighted_scores': weighted_scores,
                'sentiment_counts': label_counts,
                'total_sentences': total_sentences
            }

            logger.info(
                f"Overall sentiment: {overall_label} "
                f"(score: {sentiment_score:.3f}, confidence: {overall_confidence:.3f})"
            )

            return result

        except Exception as e:
            logger.error(f"Overall sentiment calculation failed: {str(e)}")
            raise RuntimeError(f"Aggregation failed: {str(e)}")

    def reset(self):
        """Clear stored sentence results for fresh analysis."""
        self.sentence_results = []
        logger.debug("Reset sentence results")


if __name__ == "__main__":
    # Quick test
    analyzer = SentimentAnalyzer()

    test_text = "Revenue exceeded expectations and margins are expanding significantly."
    result = analyzer.analyze_sentiment(test_text)

    print(f"\nTest Analysis:")
    print(f"Text: {test_text}")
    print(f"Label: {result['label']}")
    print(f"Confidence: {result['confidence']:.3f}")
    print(f"Scores: {result['scores']}")
