#!/bin/bash

###############################################################################
# Test Suite Runner
# Runs all tests with coverage reporting
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "\n${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}→ $1${NC}"
}

###############################################################################
# Test Configuration
###############################################################################

TEST_DIR="tests"
COVERAGE_DIR="htmlcov"
COVERAGE_MIN=50  # Minimum coverage percentage

###############################################################################
# Pre-test Checks
###############################################################################

check_environment() {
    print_header "Checking Test Environment"

    # Check if virtual environment is activated
    if [ -z "$VIRTUAL_ENV" ]; then
        print_error "Virtual environment not activated"
        print_info "Run: source venv/Scripts/activate (Windows) or source venv/bin/activate (Linux/Mac)"
        exit 1
    fi
    print_success "Virtual environment active: $VIRTUAL_ENV"

    # Check if pytest is installed
    if ! python -m pytest --version &> /dev/null; then
        print_error "pytest not installed"
        print_info "Installing pytest..."
        pip install pytest pytest-cov pytest-asyncio httpx
    fi
    print_success "pytest installed"

    # Check if test directory exists
    if [ ! -d "$TEST_DIR" ]; then
        print_error "Test directory $TEST_DIR not found"
        exit 1
    fi
    print_success "Test directory found"
}

###############################################################################
# Test Runners
###############################################################################

run_all_tests() {
    print_header "Running All Tests"

    python -m pytest $TEST_DIR \
        -v \
        --tb=short \
        --color=yes

    if [ $? -eq 0 ]; then
        print_success "All tests passed"
        return 0
    else
        print_error "Some tests failed"
        return 1
    fi
}

run_tests_with_coverage() {
    print_header "Running Tests with Coverage"

    python -m pytest $TEST_DIR \
        -v \
        --cov=agents \
        --cov=backend \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=term:skip-covered \
        --cov-fail-under=$COVERAGE_MIN \
        --tb=short \
        --color=yes

    if [ $? -eq 0 ]; then
        print_success "Tests passed with coverage >= ${COVERAGE_MIN}%"
        print_info "Coverage report: ${COVERAGE_DIR}/index.html"
        return 0
    else
        print_error "Tests failed or coverage < ${COVERAGE_MIN}%"
        return 1
    fi
}

run_specific_test_file() {
    local test_file=$1
    print_header "Running $test_file"

    python -m pytest $TEST_DIR/$test_file \
        -v \
        --tb=short \
        --color=yes

    if [ $? -eq 0 ]; then
        print_success "$test_file passed"
    else
        print_error "$test_file failed"
    fi
}

run_tests_by_marker() {
    local marker=$1
    print_header "Running tests marked as: $marker"

    python -m pytest $TEST_DIR \
        -v \
        -m "$marker" \
        --tb=short \
        --color=yes

    if [ $? -eq 0 ]; then
        print_success "Tests with marker '$marker' passed"
    else
        print_error "Tests with marker '$marker' failed"
    fi
}

run_unit_tests() {
    print_header "Running Unit Tests"

    python -m pytest $TEST_DIR/test_sentiment.py \
        $TEST_DIR/test_macro.py \
        -v \
        --tb=short \
        --color=yes

    if [ $? -eq 0 ]; then
        print_success "Unit tests passed"
    else
        print_error "Unit tests failed"
    fi
}

run_integration_tests() {
    print_header "Running Integration Tests"

    python -m pytest $TEST_DIR/test_orchestrator.py \
        -v \
        --tb=short \
        --color=yes

    if [ $? -eq 0 ]; then
        print_success "Integration tests passed"
    else
        print_error "Integration tests failed"
    fi
}

run_api_tests() {
    print_header "Running API Tests"

    python -m pytest $TEST_DIR/test_api.py \
        -v \
        --tb=short \
        --color=yes

    if [ $? -eq 0 ]; then
        print_success "API tests passed"
    else
        print_error "API tests failed"
    fi
}

run_fast_tests() {
    print_header "Running Fast Tests (Unit Only)"

    python -m pytest $TEST_DIR \
        -v \
        --tb=short \
        --color=yes \
        -k "not integration and not api"

    if [ $? -eq 0 ]; then
        print_success "Fast tests passed"
    else
        print_error "Fast tests failed"
    fi
}

###############################################################################
# Test Summary
###############################################################################

show_test_summary() {
    print_header "Test Summary"

    python -m pytest $TEST_DIR \
        --collect-only \
        --quiet

    echo ""
    print_info "Test files:"
    ls -1 $TEST_DIR/test_*.py 2>/dev/null || echo "  No test files found"
}

###############################################################################
# Coverage Reports
###############################################################################

open_coverage_report() {
    print_header "Opening Coverage Report"

    if [ ! -d "$COVERAGE_DIR" ]; then
        print_error "Coverage report not found. Run tests with coverage first."
        exit 1
    fi

    # Try to open in browser
    if command -v xdg-open &> /dev/null; then
        xdg-open ${COVERAGE_DIR}/index.html
    elif command -v open &> /dev/null; then
        open ${COVERAGE_DIR}/index.html
    elif command -v start &> /dev/null; then
        start ${COVERAGE_DIR}/index.html
    else
        print_info "Coverage report: ${COVERAGE_DIR}/index.html"
    fi
}

generate_coverage_badge() {
    print_header "Generating Coverage Badge"

    python -m pytest $TEST_DIR \
        --cov=agents \
        --cov=backend \
        --cov-report=term \
        --quiet

    print_success "Coverage calculated"
}

###############################################################################
# Cleanup
###############################################################################

cleanup_test_artifacts() {
    print_header "Cleaning Test Artifacts"

    # Remove coverage files
    rm -rf .coverage
    rm -rf $COVERAGE_DIR
    rm -rf .pytest_cache
    rm -rf $TEST_DIR/__pycache__
    rm -rf $TEST_DIR/.pytest_cache

    # Remove temporary test databases
    find . -name "*.db" -type f -path "*/tmp/*" -delete 2>/dev/null || true

    print_success "Test artifacts cleaned"
}

###############################################################################
# Main Menu
###############################################################################

show_menu() {
    echo -e "\n${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║       Test Suite - Main Menu           ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"
    echo "1) Run All Tests"
    echo "2) Run Tests with Coverage"
    echo "3) Run Unit Tests Only"
    echo "4) Run Integration Tests Only"
    echo "5) Run API Tests Only"
    echo "6) Run Fast Tests (Skip Integration)"
    echo "7) Show Test Summary"
    echo "8) Open Coverage Report"
    echo "9) Clean Test Artifacts"
    echo "10) Exit"
    echo ""
}

###############################################################################
# Main Execution
###############################################################################

main() {
    # Run pre-checks
    check_environment

    # If no arguments, show interactive menu
    if [ $# -eq 0 ]; then
        while true; do
            show_menu
            read -p "Select option: " choice

            case $choice in
                1)
                    run_all_tests
                    ;;
                2)
                    run_tests_with_coverage
                    ;;
                3)
                    run_unit_tests
                    ;;
                4)
                    run_integration_tests
                    ;;
                5)
                    run_api_tests
                    ;;
                6)
                    run_fast_tests
                    ;;
                7)
                    show_test_summary
                    ;;
                8)
                    open_coverage_report
                    ;;
                9)
                    cleanup_test_artifacts
                    ;;
                10)
                    print_info "Exiting..."
                    exit 0
                    ;;
                *)
                    print_error "Invalid option"
                    ;;
            esac
        done
    fi

    # Command line arguments
    case "$1" in
        all)
            run_all_tests
            ;;
        coverage)
            run_tests_with_coverage
            ;;
        unit)
            run_unit_tests
            ;;
        integration)
            run_integration_tests
            ;;
        api)
            run_api_tests
            ;;
        fast)
            run_fast_tests
            ;;
        summary)
            show_test_summary
            ;;
        clean)
            cleanup_test_artifacts
            ;;
        file)
            if [ -z "$2" ]; then
                print_error "Please specify test file"
                exit 1
            fi
            run_specific_test_file "$2"
            ;;
        *)
            echo "Usage: $0 {all|coverage|unit|integration|api|fast|summary|clean|file <filename>}"
            echo "  Or run without arguments for interactive menu"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
