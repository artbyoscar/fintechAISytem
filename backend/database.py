"""
Database module for Fintech AI System
SQLite database for storing companies, earnings calls, and analysis results
"""

import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json

logger = logging.getLogger(__name__)


class Database:
    """SQLite database manager for earnings intelligence system."""

    def __init__(self, db_path: str = "data/fintech_ai.db"):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self._connect()

    def _connect(self):
        """Establish database connection."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def create_tables(self):
        """
        Create all required database tables with proper indexes.

        Tables:
        - companies: Company master data
        - earnings_calls: Earnings call transcripts and metadata
        - analysis_results: Sentiment and macro analysis results
        """
        cursor = self.conn.cursor()

        try:
            # Companies table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    ticker TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    sector TEXT,
                    market_cap REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Earnings calls table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS earnings_calls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL,
                    call_date DATE NOT NULL,
                    quarter TEXT,
                    fiscal_year INTEGER,
                    transcript_text TEXT NOT NULL,
                    sentiment_score REAL,
                    macro_regime TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ticker) REFERENCES companies(ticker)
                )
            """)

            # Analysis results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    call_id INTEGER NOT NULL,
                    sentiment_label TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    sentiment_distribution TEXT,
                    key_quotes TEXT,
                    macro_regime TEXT,
                    macro_confidence REAL,
                    recommendation TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (call_id) REFERENCES earnings_calls(id)
                )
            """)

            # Trading signals table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trading_signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL,
                    call_id INTEGER,
                    signal TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    reasoning TEXT,
                    position_size INTEGER,
                    risk_score REAL,
                    sentiment_score REAL,
                    sentiment_label TEXT,
                    sentiment_confidence REAL,
                    macro_regime TEXT,
                    macro_confidence REAL,
                    validation_notes TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ticker) REFERENCES companies(ticker),
                    FOREIGN KEY (call_id) REFERENCES earnings_calls(id)
                )
            """)

            # Create indexes for better query performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_earnings_ticker
                ON earnings_calls(ticker)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_earnings_date
                ON earnings_calls(call_date DESC)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_earnings_ticker_date
                ON earnings_calls(ticker, call_date DESC)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_analysis_call_id
                ON analysis_results(call_id)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_signals_ticker
                ON trading_signals(ticker)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_signals_timestamp
                ON trading_signals(timestamp DESC)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_signals_ticker_timestamp
                ON trading_signals(ticker, timestamp DESC)
            """)

            self.conn.commit()
            logger.info("Database tables created successfully")

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Failed to create tables: {e}")
            raise

    def insert_company(
        self,
        ticker: str,
        name: str,
        sector: Optional[str] = None,
        market_cap: Optional[float] = None
    ) -> bool:
        """
        Insert or update company information.

        Args:
            ticker: Stock ticker symbol
            name: Company name
            sector: Business sector
            market_cap: Market capitalization in USD

        Returns:
            True if successful, False otherwise
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO companies (ticker, name, sector, market_cap, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(ticker) DO UPDATE SET
                    name = excluded.name,
                    sector = excluded.sector,
                    market_cap = excluded.market_cap,
                    updated_at = CURRENT_TIMESTAMP
            """, (ticker, name, sector, market_cap))

            self.conn.commit()
            logger.info(f"Company inserted/updated: {ticker}")
            return True

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Failed to insert company {ticker}: {e}")
            return False

    def insert_earnings_call(
        self,
        ticker: str,
        call_date: str,
        transcript_text: str,
        sentiment_score: Optional[float] = None,
        macro_regime: Optional[str] = None,
        quarter: Optional[str] = None,
        fiscal_year: Optional[int] = None
    ) -> Optional[int]:
        """
        Insert earnings call transcript.

        Args:
            ticker: Stock ticker symbol
            call_date: Date of earnings call (YYYY-MM-DD)
            transcript_text: Full transcript text
            sentiment_score: Overall sentiment score
            macro_regime: Macro regime classification
            quarter: Fiscal quarter (e.g., "Q1", "Q2")
            fiscal_year: Fiscal year

        Returns:
            Call ID if successful, None otherwise
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO earnings_calls (
                    ticker, call_date, quarter, fiscal_year,
                    transcript_text, sentiment_score, macro_regime
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (ticker, call_date, quarter, fiscal_year,
                  transcript_text, sentiment_score, macro_regime))

            self.conn.commit()
            call_id = cursor.lastrowid
            logger.info(f"Earnings call inserted: {ticker} on {call_date} (ID: {call_id})")
            return call_id

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Failed to insert earnings call: {e}")
            return None

    def insert_analysis_result(
        self,
        call_id: int,
        sentiment_label: str,
        confidence: float,
        sentiment_distribution: Dict,
        key_quotes: List[str],
        macro_regime: Optional[str] = None,
        macro_confidence: Optional[float] = None,
        recommendation: Optional[str] = None
    ) -> Optional[int]:
        """
        Insert analysis results for an earnings call.

        Args:
            call_id: Earnings call ID
            sentiment_label: Overall sentiment label
            confidence: Confidence score
            sentiment_distribution: Distribution of sentiments
            key_quotes: List of important quotes
            macro_regime: Macro regime classification
            macro_confidence: Macro regime confidence
            recommendation: Trading recommendation

        Returns:
            Analysis ID if successful, None otherwise
        """
        cursor = self.conn.cursor()

        try:
            # Convert complex objects to JSON strings
            distribution_json = json.dumps(sentiment_distribution)
            quotes_json = json.dumps(key_quotes)

            cursor.execute("""
                INSERT INTO analysis_results (
                    call_id, sentiment_label, confidence,
                    sentiment_distribution, key_quotes,
                    macro_regime, macro_confidence, recommendation
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (call_id, sentiment_label, confidence,
                  distribution_json, quotes_json,
                  macro_regime, macro_confidence, recommendation))

            self.conn.commit()
            analysis_id = cursor.lastrowid
            logger.info(f"Analysis result inserted for call_id: {call_id}")
            return analysis_id

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Failed to insert analysis result: {e}")
            return None

    def get_recent_calls(self, limit: int = 10) -> List[Dict]:
        """
        Get most recent earnings calls.

        Args:
            limit: Maximum number of calls to return

        Returns:
            List of earnings call records
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    ec.id, ec.ticker, ec.call_date, ec.quarter,
                    ec.fiscal_year, ec.sentiment_score, ec.macro_regime,
                    c.name as company_name, c.sector
                FROM earnings_calls ec
                LEFT JOIN companies c ON ec.ticker = c.ticker
                ORDER BY ec.call_date DESC
                LIMIT ?
            """, (limit,))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except sqlite3.Error as e:
            logger.error(f"Failed to fetch recent calls: {e}")
            return []

    def get_call_by_ticker(
        self,
        ticker: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Get earnings calls for a specific ticker.

        Args:
            ticker: Stock ticker symbol
            limit: Maximum number of calls to return

        Returns:
            List of earnings call records
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    ec.id, ec.ticker, ec.call_date, ec.quarter,
                    ec.fiscal_year, ec.sentiment_score, ec.macro_regime,
                    c.name as company_name, c.sector
                FROM earnings_calls ec
                LEFT JOIN companies c ON ec.ticker = c.ticker
                WHERE ec.ticker = ?
                ORDER BY ec.call_date DESC
                LIMIT ?
            """, (ticker.upper(), limit))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except sqlite3.Error as e:
            logger.error(f"Failed to fetch calls for {ticker}: {e}")
            return []

    def get_analysis_by_call_id(self, call_id: int) -> Optional[Dict]:
        """
        Get analysis results for a specific earnings call.

        Args:
            call_id: Earnings call ID

        Returns:
            Analysis result dict or None
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                SELECT * FROM analysis_results
                WHERE call_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
            """, (call_id,))

            row = cursor.fetchone()
            if row:
                result = dict(row)
                # Parse JSON fields
                if result['sentiment_distribution']:
                    result['sentiment_distribution'] = json.loads(result['sentiment_distribution'])
                if result['key_quotes']:
                    result['key_quotes'] = json.loads(result['key_quotes'])
                return result
            return None

        except sqlite3.Error as e:
            logger.error(f"Failed to fetch analysis for call_id {call_id}: {e}")
            return None

    def get_company_stats(self) -> Dict:
        """
        Get database statistics.

        Returns:
            Dict with count statistics
        """
        cursor = self.conn.cursor()

        try:
            stats = {}

            cursor.execute("SELECT COUNT(*) as count FROM companies")
            stats['total_companies'] = cursor.fetchone()['count']

            cursor.execute("SELECT COUNT(*) as count FROM earnings_calls")
            stats['total_calls'] = cursor.fetchone()['count']

            cursor.execute("SELECT COUNT(*) as count FROM analysis_results")
            stats['total_analyses'] = cursor.fetchone()['count']

            cursor.execute("""
                SELECT macro_regime, COUNT(*) as count
                FROM earnings_calls
                WHERE macro_regime IS NOT NULL
                GROUP BY macro_regime
            """)
            stats['regime_distribution'] = {
                row['macro_regime']: row['count']
                for row in cursor.fetchall()
            }

            return stats

        except sqlite3.Error as e:
            logger.error(f"Failed to get stats: {e}")
            return {}

    def insert_trading_signal(
        self,
        ticker: str,
        signal_data: Dict,
        call_id: Optional[int] = None
    ) -> Optional[int]:
        """
        Insert trading signal into database.

        Args:
            ticker: Stock ticker symbol
            signal_data: Signal generation results
            call_id: Optional earnings call ID

        Returns:
            Signal ID if successful, None otherwise
        """
        cursor = self.conn.cursor()

        try:
            factors = signal_data.get('factors', {})

            cursor.execute("""
                INSERT INTO trading_signals (
                    ticker, call_id, signal, confidence, reasoning,
                    position_size, risk_score,
                    sentiment_score, sentiment_label, sentiment_confidence,
                    macro_regime, macro_confidence, validation_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ticker,
                call_id,
                signal_data['signal'],
                signal_data['confidence'],
                signal_data['reasoning'],
                signal_data['position_size'],
                signal_data['risk_score'],
                factors.get('sentiment_score'),
                factors.get('sentiment_label'),
                factors.get('sentiment_confidence'),
                factors.get('macro_regime'),
                factors.get('macro_confidence'),
                signal_data.get('validation_notes')
            ))

            self.conn.commit()
            signal_id = cursor.lastrowid
            logger.info(f"Trading signal inserted: {ticker} - {signal_data['signal']}")
            return signal_id

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Failed to insert trading signal: {e}")
            return None

    def get_trading_signals(
        self,
        ticker: Optional[str] = None,
        signal_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Retrieve trading signals from database.

        Args:
            ticker: Optional ticker to filter by
            signal_type: Optional signal type (BUY/SELL/HOLD)
            limit: Maximum number of signals to return

        Returns:
            List of signal dictionaries
        """
        cursor = self.conn.cursor()

        try:
            query = "SELECT * FROM trading_signals WHERE 1=1"
            params = []

            if ticker:
                query += " AND ticker = ?"
                params.append(ticker.upper())

            if signal_type:
                query += " AND signal = ?"
                params.append(signal_type.upper())

            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            signals = []
            for row in rows:
                signals.append({
                    'id': row['id'],
                    'ticker': row['ticker'],
                    'call_id': row['call_id'],
                    'signal': row['signal'],
                    'confidence': row['confidence'],
                    'reasoning': row['reasoning'],
                    'position_size': row['position_size'],
                    'risk_score': row['risk_score'],
                    'sentiment_score': row['sentiment_score'],
                    'sentiment_label': row['sentiment_label'],
                    'sentiment_confidence': row['sentiment_confidence'],
                    'macro_regime': row['macro_regime'],
                    'macro_confidence': row['macro_confidence'],
                    'validation_notes': row['validation_notes'],
                    'timestamp': row['timestamp']
                })

            return signals

        except sqlite3.Error as e:
            logger.error(f"Failed to retrieve trading signals: {e}")
            return []

    def get_signal_stats(self) -> Dict:
        """
        Get statistics about trading signals.

        Returns:
            Dictionary with signal statistics
        """
        cursor = self.conn.cursor()

        try:
            stats = {}

            # Total signals
            cursor.execute("SELECT COUNT(*) as total FROM trading_signals")
            stats['total_signals'] = cursor.fetchone()['total']

            # Signals by type
            cursor.execute("""
                SELECT signal, COUNT(*) as count
                FROM trading_signals
                GROUP BY signal
            """)
            stats['by_signal'] = {row['signal']: row['count'] for row in cursor.fetchall()}

            # Average confidence by signal
            cursor.execute("""
                SELECT signal, AVG(confidence) as avg_confidence
                FROM trading_signals
                GROUP BY signal
            """)
            stats['avg_confidence'] = {
                row['signal']: round(row['avg_confidence'], 3)
                for row in cursor.fetchall()
            }

            # Recent 24h
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM trading_signals
                WHERE datetime(timestamp) >= datetime('now', '-1 day')
            """)
            stats['recent_24h'] = cursor.fetchone()['count']

            return stats

        except sqlite3.Error as e:
            logger.error(f"Failed to get signal stats: {e}")
            return {}

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


if __name__ == "__main__":
    # Test database creation
    logging.basicConfig(level=logging.INFO)

    import os
    os.makedirs("data", exist_ok=True)

    with Database() as db:
        db.create_tables()

        # Insert test data
        db.insert_company("AAPL", "Apple Inc.", "Technology", 3000000000000)
        db.insert_company("MSFT", "Microsoft Corporation", "Technology", 2800000000000)

        print("\nDatabase Stats:")
        stats = db.get_company_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")

        print("\n✓ Database created and tested successfully")
