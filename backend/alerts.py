"""
Alert System
Monitors for significant market events and sends notifications
"""

import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)


class AlertSystem:
    """
    Monitors market conditions and generates actionable alerts.

    Alert Types:
    - EXTREME_SENTIMENT: Very bullish or bearish sentiment (>0.8 or <-0.8)
    - SENTIMENT_DIVERGENCE: Sentiment contradicts macro regime
    - REGIME_CHANGE: Macro regime shifted (bull→bear or vice versa)
    - HIGH_CONFIDENCE: Very confident analysis (>90% confidence)
    - EARNINGS_UPCOMING: Company has earnings call within 3 days
    """

    def __init__(self, alert_dir: str = "data/alerts"):
        """
        Initialize alert system.

        Args:
            alert_dir: Directory to store alert history
        """
        self.alert_dir = alert_dir
        self.history_file = os.path.join(alert_dir, "alert_history.json")
        os.makedirs(alert_dir, exist_ok=True)

        # Load previous regime for change detection
        self.previous_regime = self._load_previous_regime()

        logger.info("AlertSystem initialized")

    def _load_previous_regime(self) -> Optional[str]:
        """Load the last known macro regime."""
        regime_file = os.path.join(self.alert_dir, "last_regime.json")
        if os.path.exists(regime_file):
            try:
                with open(regime_file, 'r') as f:
                    data = json.load(f)
                    return data.get('regime')
            except Exception as e:
                logger.warning(f"Failed to load previous regime: {e}")
        return None

    def _save_regime(self, regime: str):
        """Save current regime for future comparison."""
        regime_file = os.path.join(self.alert_dir, "last_regime.json")
        try:
            with open(regime_file, 'w') as f:
                json.dump({
                    'regime': regime,
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save regime: {e}")

    def check_for_alerts(self, analysis_result: Dict) -> List[Dict]:
        """
        Scan analysis results for alert conditions.

        Args:
            analysis_result: Complete analysis data (sentiment + macro + ticker)

        Returns:
            List of alert dictionaries
        """
        alerts = []

        ticker = analysis_result.get('ticker', 'UNKNOWN')
        sentiment = analysis_result.get('sentiment', {})
        macro = analysis_result.get('macro', {})

        logger.info(f"Checking alerts for {ticker}")

        # 1. Extreme Sentiment Alert
        sentiment_score = sentiment.get('sentiment_score', 0)
        if abs(sentiment_score) > 0.8:
            alerts.append({
                'type': 'EXTREME_SENTIMENT',
                'severity': 'HIGH',
                'ticker': ticker,
                'message': f"{ticker} shows {'VERY BULLISH' if sentiment_score > 0 else 'VERY BEARISH'} sentiment",
                'details': {
                    'sentiment_score': sentiment_score,
                    'sentiment_label': sentiment.get('sentiment_label'),
                    'confidence': sentiment.get('confidence')
                },
                'timestamp': datetime.now().isoformat()
            })

        # 2. Sentiment-Macro Divergence Alert
        regime = macro.get('regime')
        if regime and sentiment.get('sentiment_label'):
            is_divergence = (
                (regime == 'BULL' and sentiment.get('sentiment_label').lower() == 'negative') or
                (regime == 'BEAR' and sentiment.get('sentiment_label').lower() == 'positive')
            )

            if is_divergence:
                alerts.append({
                    'type': 'SENTIMENT_DIVERGENCE',
                    'severity': 'MEDIUM',
                    'ticker': ticker,
                    'message': f"{ticker}: Sentiment diverges from macro regime",
                    'details': {
                        'sentiment': sentiment.get('sentiment_label'),
                        'regime': regime,
                        'reason': f"{'Negative' if sentiment.get('sentiment_label').lower() == 'negative' else 'Positive'} sentiment in {regime} market"
                    },
                    'timestamp': datetime.now().isoformat()
                })

        # 3. Regime Change Alert
        if regime and self.previous_regime and regime != self.previous_regime:
            alerts.append({
                'type': 'REGIME_CHANGE',
                'severity': 'CRITICAL',
                'ticker': None,  # Market-wide event
                'message': f"Macro regime changed: {self.previous_regime} → {regime}",
                'details': {
                    'old_regime': self.previous_regime,
                    'new_regime': regime,
                    'confidence': macro.get('confidence')
                },
                'timestamp': datetime.now().isoformat()
            })

            # Update previous regime
            self._save_regime(regime)

        # 4. High Confidence Alert
        confidence = sentiment.get('confidence', 0)
        if confidence > 0.9:
            alerts.append({
                'type': 'HIGH_CONFIDENCE',
                'severity': 'LOW',
                'ticker': ticker,
                'message': f"{ticker}: Very confident analysis ({confidence * 100:.0f}%)",
                'details': {
                    'confidence': confidence,
                    'sentiment': sentiment.get('sentiment_label'),
                    'score': sentiment_score
                },
                'timestamp': datetime.now().isoformat()
            })

        # 5. Trading Recommendation Alert (FAVORABLE or AVOID)
        recommendation = macro.get('recommendation')
        if recommendation in ['FAVORABLE', 'AVOID']:
            alerts.append({
                'type': 'TRADING_SIGNAL',
                'severity': 'MEDIUM' if recommendation == 'FAVORABLE' else 'HIGH',
                'ticker': ticker,
                'message': f"{ticker}: {recommendation} trading conditions",
                'details': {
                    'recommendation': recommendation,
                    'regime': regime,
                    'sentiment': sentiment.get('sentiment_label'),
                    'risk_level': macro.get('risk_level', 'UNKNOWN')
                },
                'timestamp': datetime.now().isoformat()
            })

        # Save regime for next check
        if regime and not self.previous_regime:
            self._save_regime(regime)
            self.previous_regime = regime

        logger.info(f"Found {len(alerts)} alerts for {ticker}")
        return alerts

    def send_email_alert(self, recipient: str, alerts: List[Dict], analysis_result: Dict) -> bool:
        """
        Send email alert with analysis results.

        For now, this logs to console instead of sending real emails.
        In production, configure SMTP server and credentials.

        Args:
            recipient: Email address
            alerts: List of alert dictionaries
            analysis_result: Complete analysis data

        Returns:
            Success status
        """
        if not alerts:
            logger.info("No alerts to send")
            return False

        logger.info(f"Sending {len(alerts)} alerts to {recipient}")

        # Load HTML template
        template_path = os.path.join("data", "alert_templates", "earnings_alert.html")
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                html_template = f.read()
        else:
            html_template = self._get_default_template()

        # Format alert data
        ticker = analysis_result.get('ticker', 'UNKNOWN')
        sentiment = analysis_result.get('sentiment', {})
        macro = analysis_result.get('macro', {})

        # Replace template placeholders
        html_content = html_template.format(
            ticker=ticker,
            sentiment_label=sentiment.get('sentiment_label', 'N/A').upper(),
            sentiment_score=(sentiment.get('sentiment_score', 0) * 100),
            confidence=(sentiment.get('confidence', 0) * 100),
            regime=macro.get('regime', 'N/A'),
            recommendation=macro.get('recommendation', 'N/A'),
            alert_count=len(alerts),
            alerts_html=self._format_alerts_html(alerts),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        # For now, log instead of sending
        logger.info("="*80)
        logger.info("EMAIL ALERT PREVIEW")
        logger.info("="*80)
        logger.info(f"To: {recipient}")
        logger.info(f"Subject: {len(alerts)} Alert(s) for {ticker}")
        logger.info(f"Alerts: {', '.join([a['type'] for a in alerts])}")
        logger.info("="*80)

        # In production, use this code to send:
        # try:
        #     msg = MIMEMultipart('alternative')
        #     msg['Subject'] = f"{len(alerts)} Alert(s) for {ticker}"
        #     msg['From'] = 'alerts@fintechai.com'
        #     msg['To'] = recipient
        #
        #     msg.attach(MIMEText(html_content, 'html'))
        #
        #     with smtplib.SMTP('smtp.gmail.com', 587) as server:
        #         server.starttls()
        #         server.login('your_email@gmail.com', 'your_password')
        #         server.send_message(msg)
        #
        #     logger.info(f"Email sent successfully to {recipient}")
        #     return True
        # except Exception as e:
        #     logger.error(f"Failed to send email: {e}")
        #     return False

        return True  # Simulated success

    def _format_alerts_html(self, alerts: List[Dict]) -> str:
        """Format alerts as HTML list."""
        html = ""
        for alert in alerts:
            severity_color = {
                'CRITICAL': '#ff1744',
                'HIGH': '#ff6b35',
                'MEDIUM': '#ffc400',
                'LOW': '#00c853'
            }.get(alert['severity'], '#999')

            html += f"""
            <div style="padding: 12px; margin: 8px 0; border-left: 4px solid {severity_color}; background: #f5f5f5;">
                <strong style="color: {severity_color};">{alert['type']}</strong><br>
                {alert['message']}<br>
                <small style="color: #666;">{alert['timestamp']}</small>
            </div>
            """
        return html

    def _get_default_template(self) -> str:
        """Get default email template."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Earnings Alert</title>
        </head>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #ff6b35;">Fintech AI Alert</h1>
            <h2>{ticker} Analysis</h2>

            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>Sentiment Analysis</h3>
                <p><strong>Label:</strong> {sentiment_label}</p>
                <p><strong>Score:</strong> {sentiment_score:.1f}%</p>
                <p><strong>Confidence:</strong> {confidence:.1f}%</p>
            </div>

            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>Macro Regime</h3>
                <p><strong>Regime:</strong> {regime}</p>
                <p><strong>Recommendation:</strong> {recommendation}</p>
            </div>

            <div style="margin: 20px 0;">
                <h3>{alert_count} Alert(s)</h3>
                {alerts_html}
            </div>

            <p style="color: #666; font-size: 12px;">
                Generated at {timestamp} by Fintech AI System
            </p>
        </body>
        </html>
        """

    def save_alert_history(self, alerts: List[Dict], analysis_result: Dict):
        """
        Save alert history to JSON file.

        Args:
            alerts: List of alerts
            analysis_result: Analysis data
        """
        if not alerts:
            return

        # Load existing history
        history = []
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load alert history: {e}")

        # Add new alerts
        for alert in alerts:
            history_entry = {
                'alert': alert,
                'ticker': analysis_result.get('ticker'),
                'timestamp': datetime.now().isoformat()
            }
            history.append(history_entry)

        # Keep last 1000 alerts
        history = history[-1000:]

        # Save updated history
        try:
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2, default=str)
            logger.info(f"Saved {len(alerts)} alerts to history")
        except Exception as e:
            logger.error(f"Failed to save alert history: {e}")

    def get_alert_history(self, limit: int = 50, ticker: Optional[str] = None) -> List[Dict]:
        """
        Get alert history.

        Args:
            limit: Maximum number of alerts to return
            ticker: Filter by ticker (optional)

        Returns:
            List of historical alerts
        """
        if not os.path.exists(self.history_file):
            return []

        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)

            # Filter by ticker if specified
            if ticker:
                history = [h for h in history if h.get('ticker') == ticker.upper()]

            # Return most recent
            return history[-limit:][::-1]  # Reverse to show newest first

        except Exception as e:
            logger.error(f"Failed to load alert history: {e}")
            return []

    def get_alert_stats(self) -> Dict:
        """
        Get statistics about alerts.

        Returns:
            Dictionary with alert statistics
        """
        if not os.path.exists(self.history_file):
            return {
                'total_alerts': 0,
                'alerts_by_type': {},
                'alerts_by_severity': {},
                'recent_24h': 0
            }

        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)

            # Count by type
            alerts_by_type = {}
            alerts_by_severity = {}
            recent_24h = 0

            cutoff_time = datetime.now() - timedelta(hours=24)

            for entry in history:
                alert = entry.get('alert', {})
                alert_type = alert.get('type', 'UNKNOWN')
                severity = alert.get('severity', 'UNKNOWN')
                timestamp = datetime.fromisoformat(entry.get('timestamp', datetime.now().isoformat()))

                # Count by type
                alerts_by_type[alert_type] = alerts_by_type.get(alert_type, 0) + 1

                # Count by severity
                alerts_by_severity[severity] = alerts_by_severity.get(severity, 0) + 1

                # Count recent
                if timestamp >= cutoff_time:
                    recent_24h += 1

            return {
                'total_alerts': len(history),
                'alerts_by_type': alerts_by_type,
                'alerts_by_severity': alerts_by_severity,
                'recent_24h': recent_24h
            }

        except Exception as e:
            logger.error(f"Failed to get alert stats: {e}")
            return {
                'total_alerts': 0,
                'alerts_by_type': {},
                'alerts_by_severity': {},
                'recent_24h': 0
            }


if __name__ == "__main__":
    # Test the alert system
    logging.basicConfig(level=logging.INFO)

    print("\n" + "="*80)
    print("ALERT SYSTEM - TEST")
    print("="*80 + "\n")

    # Create alert system
    alert_system = AlertSystem()

    # Mock analysis result
    mock_result = {
        'ticker': 'AAPL',
        'sentiment': {
            'sentiment_label': 'positive',
            'sentiment_score': 0.85,
            'confidence': 0.92,
            'scores': {
                'positive': 0.89,
                'negative': 0.02,
                'neutral': 0.09
            }
        },
        'macro': {
            'regime': 'BULL',
            'recommendation': 'FAVORABLE',
            'confidence': 0.88,
            'risk_level': 'MODERATE'
        }
    }

    # Check for alerts
    print("Checking for alerts...")
    alerts = alert_system.check_for_alerts(mock_result)

    print(f"\nFound {len(alerts)} alert(s):\n")
    for alert in alerts:
        print(f"  [{alert['severity']}] {alert['type']}: {alert['message']}")

    # Save to history
    print("\nSaving to alert history...")
    alert_system.save_alert_history(alerts, mock_result)

    # Send email (logs to console)
    print("\nSending email alert...")
    alert_system.send_email_alert("user@example.com", alerts, mock_result)

    # Get stats
    print("\nAlert Statistics:")
    stats = alert_system.get_alert_stats()
    print(f"  Total Alerts: {stats['total_alerts']}")
    print(f"  Last 24 Hours: {stats['recent_24h']}")
    print(f"  By Type: {stats['alerts_by_type']}")

    print("\n" + "="*80)
    print("✓ ALERT SYSTEM TEST COMPLETE")
    print("="*80 + "\n")
