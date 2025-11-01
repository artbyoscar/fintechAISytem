"""
Fintech AI System - Main CLI Interface
Professional earnings intelligence terminal
"""

import argparse
import logging
import sys
import os
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn

from backend.orchestrator import AnalysisOrchestrator
from agents.earnings_fetcher import EarningsFetcher

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Initialize rich console
console = Console()


def setup_logging(verbose: bool = False):
    """
    Configure logging.

    Args:
        verbose: Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('data/fintech_ai.log'),
            logging.StreamHandler() if verbose else logging.NullHandler()
        ]
    )


def print_banner():
    """Print application banner."""
    banner_text = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║               MACRO-AWARE EARNINGS INTELLIGENCE SYSTEM                        ║
║                                                                               ║
║                   AI-Powered Financial Analysis Platform                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    console.print(banner_text, style="bold cyan")
    console.print(f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", style="dim")


def display_sentiment(sentiment_data: dict):
    """
    Display sentiment analysis results.

    Args:
        sentiment_data: Sentiment analysis results
    """
    score = sentiment_data['sentiment_score']
    label = sentiment_data['overall_label']
    confidence = sentiment_data['confidence']

    # Determine color based on sentiment
    if label == 'positive':
        color = "green"
        emoji = "📈"
    elif label == 'negative':
        color = "red"
        emoji = "📉"
    else:
        color = "yellow"
        emoji = "➡️"

    # Create sentiment display
    sentiment_text = f"{emoji} {label.upper()} (Score: {score:+.3f}, Confidence: {confidence:.1%})"

    table = Table(title="Sentiment Analysis", box=box.ROUNDED, show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style=color)

    table.add_row("Overall Sentiment", sentiment_text)
    table.add_row("Sentiment Score", f"{score:+.3f} (-1=bearish, +1=bullish)")
    table.add_row("Confidence", f"{confidence:.1%}")

    # Distribution
    dist = sentiment_data['distribution']
    dist_text = (f"Positive: {dist['positive']:.1f}% | "
                f"Negative: {dist['negative']:.1f}% | "
                f"Neutral: {dist['neutral']:.1f}%")
    table.add_row("Distribution", dist_text)

    console.print(table)
    console.print()

    # Key quotes
    if sentiment_data.get('key_quotes'):
        console.print("[bold]Key Quotes:[/bold]")
        for quote in sentiment_data['key_quotes'][:4]:  # Show top 4
            if quote.startswith("[POSITIVE]"):
                console.print(f"  [green]✓[/green] {quote[11:]}")
            elif quote.startswith("[NEGATIVE]"):
                console.print(f"  [red]✗[/red] {quote[11:]}")
        console.print()


def display_macro_regime(macro_data: dict):
    """
    Display macro regime analysis.

    Args:
        macro_data: Macro regime results
    """
    regime = macro_data['regime']
    confidence = macro_data['confidence']

    # Determine color based on regime
    if regime == "BULL":
        color = "green"
        emoji = "🐂"
    elif regime == "BEAR":
        color = "red"
        emoji = "🐻"
    else:
        color = "yellow"
        emoji = "⚖️"

    table = Table(title="Macro Regime Analysis", box=box.ROUNDED, show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style=color)

    table.add_row("Regime", f"{emoji} {regime}")
    table.add_row("Confidence", f"{confidence:.1%}")

    # Indicators
    indicators = macro_data['indicators']
    table.add_row("VIX", f"{indicators['VIX']}")
    table.add_row("Unemployment", f"{indicators['unemployment_rate']}%")
    table.add_row("Inflation", f"{indicators['inflation_rate']}%")
    table.add_row("Fed Funds Rate", f"{indicators['fed_funds_rate']}%")

    console.print(table)
    console.print()

    # Reasoning
    console.print("[bold]Regime Reasoning:[/bold]")
    for reason in macro_data['reasoning'][:5]:  # Show top 5
        console.print(f"  {reason}")
    console.print()


def display_recommendation(rec_data: dict, assessment: dict):
    """
    Display trading recommendation.

    Args:
        rec_data: Recommendation data
        assessment: Overall assessment
    """
    action = rec_data['action']
    verdict = assessment['verdict']

    # Determine color
    if "BUY" in verdict:
        color = "green"
        emoji = "🚀"
    elif "SELL" in verdict:
        color = "red"
        emoji = "⚠️"
    else:
        color = "yellow"
        emoji = "⏸️"

    table = Table(title="Trading Recommendation", box=box.ROUNDED, show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value")

    table.add_row("Overall Verdict", f"[bold {color}]{emoji} {verdict}[/bold {color}]")
    table.add_row("Recommendation", f"[{color}]{action}[/{color}]")
    table.add_row("Risk Level", rec_data['risk_level'])
    table.add_row("Rationale", rec_data['rationale'])
    table.add_row("Alignment", assessment['sentiment_macro_alignment'])

    console.print(table)
    console.print()

    # Suggested actions
    console.print("[bold]Suggested Actions:[/bold]")
    for action in rec_data['suggested_actions']:
        console.print(f"  • {action}")
    console.print()


def analyze_ticker(ticker: str, orchestrator: AnalysisOrchestrator):
    """
    Run analysis for a single ticker.

    Args:
        ticker: Stock ticker symbol
        orchestrator: Analysis orchestrator instance
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task(f"Analyzing {ticker}...", total=None)

        try:
            result = orchestrator.analyze_company(ticker)

            if not result['success']:
                console.print(f"\n[red]✗ Analysis failed: {result.get('error')}[/red]\n")
                return

            # Clear progress
            progress.stop()

            # Display results
            console.print("\n")
            console.rule(f"[bold cyan]Analysis Results: {result['company']} ({ticker})[/bold cyan]")
            console.print()

            # Company info
            earnings_info = result['earnings_call']
            console.print(f"[bold]Earnings Call:[/bold] {earnings_info['date']} - "
                         f"{earnings_info.get('quarter', 'N/A')} {earnings_info.get('fiscal_year', '')}")
            console.print(f"[bold]Sentences Analyzed:[/bold] {earnings_info['sentences_analyzed']}")
            console.print()

            # Sentiment analysis
            display_sentiment(result['sentiment_analysis'])

            # Macro regime
            display_macro_regime(result['macro_regime'])

            # Recommendation
            display_recommendation(result['recommendation'], result['overall_assessment'])

            # Performance
            perf = result['performance']
            console.print(f"[dim]Analysis completed in {perf['total_time']:.2f}s[/dim]")

            # Report location
            console.print()
            console.print(Panel(
                f"[bold green]Report saved to:[/bold green]\n{result.get('report_path', 'N/A')}",
                box=box.ROUNDED,
                border_style="green"
            ))
            console.print()

        except Exception as e:
            progress.stop()
            console.print(f"\n[red]✗ Error during analysis: {str(e)}[/red]\n")
            if '--verbose' in sys.argv:
                import traceback
                console.print(traceback.format_exc())


def analyze_all(orchestrator: AnalysisOrchestrator):
    """
    Analyze all available companies.

    Args:
        orchestrator: Analysis orchestrator instance
    """
    fetcher = EarningsFetcher()
    calendar = fetcher.get_earnings_calendar()

    tickers = [event['ticker'] for event in calendar]

    console.print(f"\n[bold]Analyzing {len(tickers)} companies:[/bold] {', '.join(tickers)}\n")

    for ticker in tickers:
        analyze_ticker(ticker, orchestrator)
        console.print("\n" + "─"*80 + "\n")


def show_earnings_calendar():
    """Display upcoming earnings calendar."""
    fetcher = EarningsFetcher()
    calendar = fetcher.get_earnings_calendar()

    table = Table(title="Upcoming Earnings Calendar", box=box.ROUNDED)
    table.add_column("Ticker", style="cyan", justify="center")
    table.add_column("Company", style="white")
    table.add_column("Date", style="yellow")
    table.add_column("Time", style="magenta")
    table.add_column("Quarter", style="green")

    for event in calendar:
        table.add_row(
            event['ticker'],
            event['company'],
            event['date'],
            event['time'],
            event.get('quarter', 'N/A')
        )

    console.print()
    console.print(table)
    console.print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Macro-Aware Earnings Intelligence System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --ticker AAPL              Analyze Apple earnings
  python main.py --ticker NVDA --verbose    Analyze NVIDIA with verbose logging
  python main.py --analyze-all              Analyze all companies
  python main.py --calendar                 Show earnings calendar
        """
    )

    parser.add_argument('--ticker', type=str, help='Stock ticker symbol to analyze')
    parser.add_argument('--analyze-all', action='store_true', help='Analyze all companies in calendar')
    parser.add_argument('--calendar', action='store_true', help='Show earnings calendar')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    # Setup
    setup_logging(args.verbose)
    os.makedirs("data", exist_ok=True)

    # Print banner
    print_banner()

    # Show calendar
    if args.calendar:
        show_earnings_calendar()
        return

    # Initialize orchestrator
    with console.status("[bold cyan]Initializing AI agents...", spinner="dots"):
        try:
            orchestrator = AnalysisOrchestrator()
        except Exception as e:
            console.print(f"\n[red]✗ Failed to initialize: {str(e)}[/red]\n")
            return

    # Run analysis
    if args.ticker:
        analyze_ticker(args.ticker.upper(), orchestrator)
    elif args.analyze_all:
        analyze_all(orchestrator)
    else:
        parser.print_help()

    # Cleanup
    orchestrator.close()


if __name__ == "__main__":
    main()
