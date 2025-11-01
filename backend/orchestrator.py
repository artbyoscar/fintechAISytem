"""
Analysis Orchestrator
Coordinates all agents to produce comprehensive earnings analysis
"""

import logging
import time
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path to access agents module
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agents.sentiment_analyzer import SentimentAnalyzer
from agents.earnings_fetcher import EarningsFetcher
from agents.macro_detector import MacroRegimeDetector
from backend.database import Database
from backend.alerts import AlertSystem

logger = logging.getLogger(__name__)


class AnalysisOrchestrator:
    """
    Orchestrates analysis workflow across all agents.

    Pipeline:
    1. Fetch earnings transcript
    2. Analyze sentiment using FinBERT
    3. Detect macro regime
    4. Combine insights into comprehensive report
    5. Store in database
    6. Generate actionable recommendations
    """

    def __init__(self, db_path: str = "data/fintech_ai.db"):
        """
        Initialize orchestrator with all agents.

        Args:
            db_path: Path to SQLite database
        """
        logger.info("Initializing AnalysisOrchestrator...")

        # Initialize agents
        self.sentiment_analyzer = SentimentAnalyzer()
        self.earnings_fetcher = EarningsFetcher()
        self.macro_detector = MacroRegimeDetector()
        self.database = Database(db_path)
        self.alert_system = AlertSystem()

        # Ensure database tables exist
        self.database.create_tables()

        # Report output directory
        self.report_dir = "data/analysis_reports"
        os.makedirs(self.report_dir, exist_ok=True)

        logger.info("AnalysisOrchestrator initialized successfully")

    def analyze_company(self, ticker: str) -> Dict:
        """
        Run full analysis pipeline for a company.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dict with complete analysis results

        Pipeline Timing:
        - Each step is timed for performance monitoring
        - Typical total execution: 5-15 seconds depending on transcript length
        """
        ticker = ticker.upper()
        logger.info(f"="*80)
        logger.info(f"Starting analysis for {ticker}")
        logger.info(f"="*80)

        pipeline_start = time.time()
        timings = {}

        # Step 1: Fetch earnings transcript
        logger.info(f"\n[1/5] Fetching earnings transcript for {ticker}...")
        step_start = time.time()

        transcript_data = self.earnings_fetcher.get_earnings_transcript(ticker)
        if not transcript_data:
            logger.error(f"No transcript available for {ticker}")
            return {
                "success": False,
                "error": f"No transcript data available for {ticker}",
                "ticker": ticker
            }

        timings['fetch_transcript'] = time.time() - step_start
        logger.info(f"✓ Transcript fetched ({timings['fetch_transcript']:.2f}s)")

        # Step 2: Analyze sentiment
        logger.info(f"\n[2/5] Analyzing sentiment...")
        step_start = time.time()

        transcript_text = transcript_data['transcript']
        sentence_results = self.sentiment_analyzer.analyze_transcript(transcript_text)
        overall_sentiment = self.sentiment_analyzer.get_overall_sentiment()

        # Extract key quotes (most confident positive and negative sentences)
        key_quotes = self._extract_key_quotes(sentence_results)

        timings['sentiment_analysis'] = time.time() - step_start
        logger.info(f"✓ Sentiment analyzed: {overall_sentiment['overall_label']} "
                   f"(score: {overall_sentiment['sentiment_score']:.3f}) "
                   f"({timings['sentiment_analysis']:.2f}s)")

        # Step 3: Detect macro regime
        logger.info(f"\n[3/5] Detecting macro regime...")
        step_start = time.time()

        macro_indicators = self.macro_detector.fetch_macro_indicators()
        macro_regime = self.macro_detector.classify_regime()
        trading_recommendation = self.macro_detector.get_trading_recommendation()

        timings['macro_detection'] = time.time() - step_start
        logger.info(f"✓ Macro regime: {macro_regime['regime']} "
                   f"(confidence: {macro_regime['confidence']:.3f}) "
                   f"({timings['macro_detection']:.2f}s)")

        # Step 4: Store in database and generate report
        logger.info(f"\n[4/5] Storing results and generating report...")
        step_start = time.time()

        # Insert company if not exists
        self.database.insert_company(
            ticker=ticker,
            name=transcript_data['company'],
            sector=transcript_data.get('sector')
        )

        # Insert earnings call
        call_id = self.database.insert_earnings_call(
            ticker=ticker,
            call_date=transcript_data['date'],
            transcript_text=transcript_text,
            sentiment_score=overall_sentiment['sentiment_score'],
            macro_regime=macro_regime['regime'],
            quarter=transcript_data.get('quarter'),
            fiscal_year=transcript_data.get('fiscal_year')
        )

        # Insert analysis results
        if call_id:
            self.database.insert_analysis_result(
                call_id=call_id,
                sentiment_label=overall_sentiment['overall_label'],
                confidence=overall_sentiment['overall_confidence'],
                sentiment_distribution=overall_sentiment['sentiment_distribution'],
                key_quotes=key_quotes,
                macro_regime=macro_regime['regime'],
                macro_confidence=macro_regime['confidence'],
                recommendation=trading_recommendation['recommendation']
            )

        timings['database_storage'] = time.time() - step_start
        logger.info(f"✓ Results stored in database ({timings['database_storage']:.2f}s)")

        # Generate comprehensive report
        report = self._generate_report(
            ticker=ticker,
            transcript_data=transcript_data,
            sentiment_result=overall_sentiment,
            sentence_results=sentence_results,
            key_quotes=key_quotes,
            macro_regime=macro_regime,
            trading_recommendation=trading_recommendation,
            timings=timings
        )

        # Save report to file
        report_path = self._save_report(ticker, report)

        # Step 5: Check for alerts
        logger.info(f"\n[5/5] Checking for alerts...")
        step_start = time.time()

        alerts = self.alert_system.check_for_alerts(report)
        if alerts:
            logger.info(f"✓ Found {len(alerts)} alert(s)")
            self.alert_system.save_alert_history(alerts, report)
            # Optionally send email alerts
            # self.alert_system.send_email_alert("user@example.com", alerts, report)
        else:
            logger.info("✓ No alerts triggered")

        timings['alert_check'] = time.time() - step_start

        # Add alerts to report
        report['alerts'] = alerts

        timings['total_pipeline'] = time.time() - pipeline_start

        logger.info(f"\n{'='*80}")
        logger.info(f"Analysis completed in {timings['total_pipeline']:.2f}s")
        logger.info(f"Report saved to: {report_path}")
        if alerts:
            logger.info(f"Alerts triggered: {len(alerts)}")
        logger.info(f"{'='*80}\n")

        return report

    def analyze_multiple(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Analyze multiple companies in sequence.

        Args:
            tickers: List of stock ticker symbols

        Returns:
            Dict mapping ticker to analysis results
        """
        logger.info(f"Analyzing {len(tickers)} companies: {', '.join(tickers)}")

        results = {}
        for ticker in tickers:
            try:
                results[ticker] = self.analyze_company(ticker)
                # Reset sentiment analyzer for next company
                self.sentiment_analyzer.reset()
            except Exception as e:
                logger.error(f"Failed to analyze {ticker}: {e}")
                results[ticker] = {
                    "success": False,
                    "error": str(e),
                    "ticker": ticker
                }

        logger.info(f"Batch analysis complete: {len(results)} companies processed")
        return results

    def _extract_key_quotes(
        self,
        sentence_results: List[Dict],
        num_quotes: int = 3
    ) -> List[str]:
        """
        Extract most significant quotes from sentence analysis.

        Args:
            sentence_results: List of sentence-level sentiment results
            num_quotes: Number of quotes to extract per sentiment

        Returns:
            List of key quote strings
        """
        # Sort by confidence
        sorted_results = sorted(
            sentence_results,
            key=lambda x: x['confidence'],
            reverse=True
        )

        # Get top positive and negative quotes
        positive_quotes = [
            r['text'] for r in sorted_results
            if r['label'] == 'positive'
        ][:num_quotes]

        negative_quotes = [
            r['text'] for r in sorted_results
            if r['label'] == 'negative'
        ][:num_quotes]

        # Combine with labels
        key_quotes = []
        for quote in positive_quotes:
            key_quotes.append(f"[POSITIVE] {quote}")
        for quote in negative_quotes:
            key_quotes.append(f"[NEGATIVE] {quote}")

        return key_quotes

    def _generate_report(
        self,
        ticker: str,
        transcript_data: Dict,
        sentiment_result: Dict,
        sentence_results: List[Dict],
        key_quotes: List[str],
        macro_regime: Dict,
        trading_recommendation: Dict,
        timings: Dict
    ) -> Dict:
        """
        Generate comprehensive analysis report.

        Args:
            ticker: Stock ticker
            transcript_data: Earnings transcript metadata
            sentiment_result: Overall sentiment analysis
            sentence_results: Sentence-level results
            key_quotes: Extracted key quotes
            macro_regime: Macro regime classification
            trading_recommendation: Trading recommendation
            timings: Pipeline execution timings

        Returns:
            Complete analysis report dict
        """
        # Synthesize overall assessment
        sentiment_score = sentiment_result['sentiment_score']
        regime = macro_regime['regime']

        # Determine overall assessment
        if regime == "BULL" and sentiment_score > 0.3:
            assessment = "STRONG BUY"
            assessment_reasoning = "Bullish macro regime + positive earnings sentiment = favorable setup"
        elif regime == "BULL" and sentiment_score > 0:
            assessment = "BUY"
            assessment_reasoning = "Bullish macro regime supports moderately positive earnings"
        elif regime == "BEAR" and sentiment_score < -0.3:
            assessment = "STRONG SELL"
            assessment_reasoning = "Bearish macro regime + negative earnings sentiment = high risk"
        elif regime == "BEAR" and sentiment_score < 0:
            assessment = "SELL"
            assessment_reasoning = "Bearish macro regime amplifies negative earnings sentiment"
        elif regime == "BEAR" and sentiment_score > 0.3:
            assessment = "NEUTRAL/WATCH"
            assessment_reasoning = "Positive earnings may not overcome bearish macro headwinds"
        elif regime == "BULL" and sentiment_score < -0.3:
            assessment = "NEUTRAL/WATCH"
            assessment_reasoning = "Bullish macro offset by disappointing earnings"
        else:
            assessment = "NEUTRAL"
            assessment_reasoning = "Mixed signals warrant cautious approach"

        report = {
            "success": True,
            "ticker": ticker,
            "company": transcript_data['company'],
            "analysis_timestamp": datetime.now().isoformat(),

            # Transcript metadata
            "earnings_call": {
                "date": transcript_data['date'],
                "quarter": transcript_data.get('quarter'),
                "fiscal_year": transcript_data.get('fiscal_year'),
                "transcript_length": len(transcript_data['transcript']),
                "sentences_analyzed": len(sentence_results)
            },

            # Sentiment analysis results
            "sentiment_analysis": {
                "overall_label": sentiment_result['overall_label'],
                "sentiment_score": sentiment_result['sentiment_score'],
                "confidence": sentiment_result['overall_confidence'],
                "distribution": sentiment_result['sentiment_distribution'],
                "weighted_scores": sentiment_result['weighted_scores'],
                "key_quotes": key_quotes[:6]  # Top 6 quotes
            },

            # Macro regime analysis
            "macro_regime": {
                "regime": regime,
                "confidence": macro_regime['confidence'],
                "indicators": macro_regime['indicators'],
                "reasoning": macro_regime['reasoning'],
                "signals": macro_regime['signals']
            },

            # Trading recommendation
            "recommendation": {
                "action": trading_recommendation['recommendation'],
                "rationale": trading_recommendation['rationale'],
                "risk_level": trading_recommendation['risk_level'],
                "suggested_actions": trading_recommendation['suggested_actions']
            },

            # Overall assessment
            "overall_assessment": {
                "verdict": assessment,
                "reasoning": assessment_reasoning,
                "sentiment_macro_alignment": self._assess_alignment(
                    sentiment_score, regime
                )
            },

            # Performance metrics
            "performance": {
                "timings": timings,
                "total_time": timings.get('total_pipeline', 0)
            }
        }

        return report

    def _assess_alignment(self, sentiment_score: float, regime: str) -> str:
        """
        Assess alignment between sentiment and macro regime.

        Args:
            sentiment_score: Sentiment score (-1 to +1)
            regime: Macro regime classification

        Returns:
            Alignment assessment string
        """
        if regime == "BULL" and sentiment_score > 0.2:
            return "ALIGNED - Positive earnings confirm bullish macro environment"
        elif regime == "BEAR" and sentiment_score < -0.2:
            return "ALIGNED - Negative earnings confirm bearish macro concerns"
        elif regime == "BULL" and sentiment_score < -0.2:
            return "DIVERGENT - Negative earnings contradict bullish macro (WARNING)"
        elif regime == "BEAR" and sentiment_score > 0.2:
            return "DIVERGENT - Positive earnings diverge from bearish macro (OPPORTUNITY?)"
        else:
            return "NEUTRAL - No strong alignment or divergence"

    def _save_report(self, ticker: str, report: Dict) -> str:
        """
        Save analysis report to JSON file.

        Args:
            ticker: Stock ticker
            report: Analysis report dict

        Returns:
            Path to saved report file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{ticker}_{timestamp}.json"
        filepath = os.path.join(self.report_dir, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"Report saved: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
            return f"ERROR: {str(e)}"

    def close(self):
        """Clean up resources."""
        if self.database:
            self.database.close()
        logger.info("Orchestrator closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


if __name__ == "__main__":
    # Test orchestrator
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    with AnalysisOrchestrator() as orchestrator:
        print("\n" + "="*80)
        print("TESTING ORCHESTRATOR WITH NVDA")
        print("="*80 + "\n")

        result = orchestrator.analyze_company("NVDA")

        if result['success']:
            print("\n" + "="*80)
            print("ANALYSIS SUMMARY")
            print("="*80)
            print(f"\nCompany: {result['company']} ({result['ticker']})")
            print(f"Earnings Date: {result['earnings_call']['date']}")
            print(f"\n--- SENTIMENT ANALYSIS ---")
            print(f"Overall: {result['sentiment_analysis']['overall_label'].upper()}")
            print(f"Score: {result['sentiment_analysis']['sentiment_score']:.3f}")
            print(f"Confidence: {result['sentiment_analysis']['confidence']:.3f}")
            print(f"\n--- MACRO REGIME ---")
            print(f"Regime: {result['macro_regime']['regime']}")
            print(f"Confidence: {result['macro_regime']['confidence']:.3f}")
            print(f"\n--- RECOMMENDATION ---")
            print(f"Action: {result['recommendation']['action']}")
            print(f"Risk Level: {result['recommendation']['risk_level']}")
            print(f"\n--- OVERALL ASSESSMENT ---")
            print(f"Verdict: {result['overall_assessment']['verdict']}")
            print(f"Reasoning: {result['overall_assessment']['reasoning']}")
            print(f"\nTotal Analysis Time: {result['performance']['total_time']:.2f}s")
            print("="*80)
        else:
            print(f"\n✗ Analysis failed: {result.get('error')}")
