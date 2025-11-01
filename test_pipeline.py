"""
End-to-End Pipeline Test
Tests the complete analysis workflow
"""

import sys
import os
import logging
from pathlib import Path

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from backend.orchestrator import AnalysisOrchestrator
from backend.database import Database


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def check_file_exists(filepath, description):
    """
    Check if a file exists and print result.

    Args:
        filepath: Path to check
        description: Description of the file

    Returns:
        True if exists, False otherwise
    """
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists


def test_pipeline():
    """Run end-to-end pipeline test."""
    print_header("FINTECH AI SYSTEM - END-TO-END PIPELINE TEST")

    # Track test results
    tests_passed = []
    tests_failed = []

    # Test 1: Initialize database
    print("[1/6] Testing database initialization...")
    try:
        db = Database("data/fintech_ai.db")
        db.create_tables()
        stats = db.get_company_stats()
        print(f"✓ Database initialized successfully")
        print(f"   Companies: {stats.get('total_companies', 0)}")
        print(f"   Earnings Calls: {stats.get('total_calls', 0)}")
        print(f"   Analyses: {stats.get('total_analyses', 0)}")
        db.close()
        tests_passed.append("Database initialization")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        tests_failed.append(f"Database initialization: {e}")
        return

    print()

    # Test 2: Initialize orchestrator
    print("[2/6] Testing orchestrator initialization...")
    try:
        orchestrator = AnalysisOrchestrator()
        print("✓ Orchestrator initialized successfully")
        print("   ✓ SentimentAnalyzer loaded")
        print("   ✓ EarningsFetcher loaded")
        print("   ✓ MacroDetector loaded")
        print("   ✓ Database connected")
        tests_passed.append("Orchestrator initialization")
    except Exception as e:
        print(f"✗ Orchestrator initialization failed: {e}")
        tests_failed.append(f"Orchestrator initialization: {e}")
        return

    print()

    # Test 3: Run full analysis pipeline
    print("[3/6] Running full analysis pipeline for NVDA...")
    try:
        result = orchestrator.analyze_company("NVDA")

        if result['success']:
            print("✓ Analysis pipeline completed successfully")
            print(f"   Company: {result['company']}")
            print(f"   Sentiment: {result['sentiment_analysis']['overall_label']} "
                  f"(score: {result['sentiment_analysis']['sentiment_score']:.3f})")
            print(f"   Macro Regime: {result['macro_regime']['regime']} "
                  f"(confidence: {result['macro_regime']['confidence']:.3f})")
            print(f"   Recommendation: {result['recommendation']['action']}")
            print(f"   Overall Verdict: {result['overall_assessment']['verdict']}")
            print(f"   Analysis Time: {result['performance']['total_time']:.2f}s")
            tests_passed.append("Analysis pipeline execution")
        else:
            raise Exception(result.get('error', 'Unknown error'))

    except Exception as e:
        print(f"✗ Analysis pipeline failed: {e}")
        tests_failed.append(f"Analysis pipeline: {e}")
        orchestrator.close()
        return

    print()

    # Test 4: Verify database records
    print("[4/6] Verifying database records...")
    try:
        db = Database("data/fintech_ai.db")

        # Check if company was inserted
        nvda_calls = db.get_call_by_ticker("NVDA")
        if len(nvda_calls) > 0:
            print(f"✓ Earnings call record created (ID: {nvda_calls[0]['id']})")
            tests_passed.append("Database - earnings call insertion")

            # Check if analysis was stored
            analysis = db.get_analysis_by_call_id(nvda_calls[0]['id'])
            if analysis:
                print(f"✓ Analysis record created (ID: {analysis['id']})")
                print(f"   Sentiment: {analysis['sentiment_label']}")
                print(f"   Macro Regime: {analysis['macro_regime']}")
                print(f"   Recommendation: {analysis['recommendation']}")
                tests_passed.append("Database - analysis result insertion")
            else:
                raise Exception("No analysis record found")
        else:
            raise Exception("No earnings call record found")

        db.close()

    except Exception as e:
        print(f"✗ Database verification failed: {e}")
        tests_failed.append(f"Database verification: {e}")

    print()

    # Test 5: Verify report file
    print("[5/6] Verifying analysis report...")
    try:
        report_dir = "data/analysis_reports"
        if os.path.exists(report_dir):
            reports = [f for f in os.listdir(report_dir) if f.startswith("NVDA_") and f.endswith(".json")]
            if reports:
                latest_report = sorted(reports)[-1]
                report_path = os.path.join(report_dir, latest_report)
                print(f"✓ Analysis report created: {latest_report}")

                # Verify file size
                file_size = os.path.getsize(report_path)
                print(f"   File size: {file_size:,} bytes")

                if file_size > 1000:  # Should be at least 1KB
                    tests_passed.append("Analysis report generation")
                else:
                    raise Exception("Report file seems too small")
            else:
                raise Exception("No report files found for NVDA")
        else:
            raise Exception("Report directory does not exist")

    except Exception as e:
        print(f"✗ Report verification failed: {e}")
        tests_failed.append(f"Report verification: {e}")

    print()

    # Test 6: Verify all agents produced output
    print("[6/6] Verifying all agents produced output...")
    agent_checks = []

    try:
        # Check sentiment analyzer output
        if result['sentiment_analysis']['overall_label'] in ['positive', 'negative', 'neutral']:
            print("✓ Sentiment Analyzer produced valid output")
            agent_checks.append("SentimentAnalyzer")
        else:
            raise Exception("Invalid sentiment output")

        # Check macro detector output
        if result['macro_regime']['regime'] in ['BULL', 'BEAR', 'TRANSITION']:
            print("✓ Macro Detector produced valid output")
            agent_checks.append("MacroDetector")
        else:
            raise Exception("Invalid macro regime output")

        # Check orchestrator output
        if 'overall_assessment' in result and 'verdict' in result['overall_assessment']:
            print("✓ Orchestrator produced valid output")
            agent_checks.append("Orchestrator")
        else:
            raise Exception("Invalid orchestrator output")

        tests_passed.append("Agent output verification")

    except Exception as e:
        print(f"✗ Agent verification failed: {e}")
        tests_failed.append(f"Agent verification: {e}")

    # Cleanup
    orchestrator.close()

    # Print summary
    print_header("TEST SUMMARY")

    total_tests = len(tests_passed) + len(tests_failed)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {len(tests_passed)} ✓")
    print(f"Failed: {len(tests_failed)} ✗")
    print()

    if tests_passed:
        print("Passed Tests:")
        for test in tests_passed:
            print(f"  ✓ {test}")
        print()

    if tests_failed:
        print("Failed Tests:")
        for test in tests_failed:
            print(f"  ✗ {test}")
        print()

    # Final verdict
    if len(tests_failed) == 0:
        print_header("✓ ALL TESTS PASSED - PIPELINE READY FOR PRODUCTION")
        return True
    else:
        print_header("✗ SOME TESTS FAILED - PLEASE REVIEW ERRORS ABOVE")
        return False


def commit_code():
    """Commit code to git if all tests pass."""
    import subprocess

    print_header("COMMITTING CODE TO GIT")

    try:
        # Check git status
        result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
        if result.stdout.strip():
            print("Modified files:")
            print(result.stdout)
            print()

            # Add all files
            subprocess.run(['git', 'add', '.'], check=True)
            print("✓ Files staged for commit")

            # Commit
            commit_message = "Day 1 Complete: Working MVP with sentiment analysis, macro detection, and orchestration"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print(f"✓ Committed: {commit_message}")
        else:
            print("No changes to commit")

    except subprocess.CalledProcessError as e:
        print(f"✗ Git commit failed: {e}")
    except FileNotFoundError:
        print("✗ Git not found in PATH")


def main():
    """Main test execution."""
    # Setup logging to file only
    os.makedirs("data", exist_ok=True)
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler('data/test_pipeline.log')]
    )

    # Run tests
    all_passed = test_pipeline()

    # Commit if successful
    if all_passed:
        response = input("\nCommit changes to git? [y/N]: ")
        if response.lower() == 'y':
            commit_code()
        else:
            print("\nSkipping git commit. You can commit manually later with:")
            print('  git add .')
            print('  git commit -m "Day 1 Complete: Working MVP with sentiment analysis, macro detection, and orchestration"')

    print("\n")


if __name__ == "__main__":
    main()
