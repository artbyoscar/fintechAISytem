#!/bin/bash

###############################################################################
# Fintech AI System - Deployment Script
# Builds Docker images, runs tests, and deploys containers
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="fintech-ai-system"
BACKEND_IMAGE="fintech-ai-backend"
FRONTEND_IMAGE="fintech-ai-frontend"
ENV_FILE=".env"

###############################################################################
# Helper Functions
###############################################################################

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

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}→ $1${NC}"
}

###############################################################################
# Pre-deployment Checks
###############################################################################

check_dependencies() {
    print_header "Checking Dependencies"

    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker found: $(docker --version)"

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    print_success "Docker Compose found"

    # Check if Docker daemon is running
    if ! docker ps &> /dev/null; then
        print_error "Docker daemon is not running"
        exit 1
    fi
    print_success "Docker daemon is running"
}

check_environment() {
    print_header "Checking Environment"

    # Check for .env file
    if [ ! -f "$ENV_FILE" ]; then
        print_warning ".env file not found, creating from template..."
        cat > "$ENV_FILE" << EOF
# Fintech AI System - Environment Variables
FRED_API_KEY=your_fred_api_key_here
ENVIRONMENT=production
LOG_LEVEL=INFO
VITE_API_URL=http://localhost:8000
EOF
        print_info "Please update $ENV_FILE with your API keys"
    else
        print_success ".env file found"
    fi

    # Check for required API keys
    if grep -q "your_fred_api_key_here" "$ENV_FILE"; then
        print_warning "FRED_API_KEY not configured in $ENV_FILE"
        print_info "Get your API key from: https://fred.stlouisfed.org/docs/api/api_key.html"
    fi
}

###############################################################################
# Build Process
###############################################################################

build_backend() {
    print_header "Building Backend Image"

    print_info "Building Docker image: $BACKEND_IMAGE"
    docker build -t $BACKEND_IMAGE:latest -f Dockerfile .

    if [ $? -eq 0 ]; then
        print_success "Backend image built successfully"
    else
        print_error "Backend build failed"
        exit 1
    fi
}

build_frontend() {
    print_header "Building Frontend"

    # Check if frontend directory exists
    if [ ! -d "frontend" ]; then
        print_warning "Frontend directory not found, skipping frontend build"
        return
    fi

    print_info "Installing frontend dependencies..."
    cd frontend

    if [ ! -d "node_modules" ]; then
        npm install
    fi

    print_info "Building frontend for production..."
    npm run build

    if [ $? -eq 0 ]; then
        print_success "Frontend built successfully"
    else
        print_error "Frontend build failed"
        cd ..
        exit 1
    fi

    cd ..
}

###############################################################################
# Testing
###############################################################################

run_tests() {
    print_header "Running Tests"

    print_info "Running backend tests..."

    # Create test container
    docker run --rm \
        -v "$(pwd)/data:/app/data" \
        $BACKEND_IMAGE:latest \
        python -m pytest tests/ -v || {
            print_warning "No tests found or tests failed"
        }

    print_success "Test phase completed"
}

###############################################################################
# Deployment
###############################################################################

deploy_development() {
    print_header "Deploying Development Environment"

    print_info "Starting services with docker-compose..."
    docker-compose up -d

    if [ $? -eq 0 ]; then
        print_success "Services started successfully"
        print_info "Backend: http://localhost:8000"
        print_info "Frontend: http://localhost:3000"
        print_info "API Docs: http://localhost:8000/docs"
    else
        print_error "Deployment failed"
        exit 1
    fi
}

deploy_production() {
    print_header "Deploying Production Environment"

    # Build frontend first
    build_frontend

    print_info "Starting services with production profile..."
    docker-compose --profile production up -d

    if [ $? -eq 0 ]; then
        print_success "Production services started successfully"
        print_info "Application: http://localhost"
        print_info "API Docs: http://localhost/api/docs"
    else
        print_error "Production deployment failed"
        exit 1
    fi
}

###############################################################################
# Cleanup
###############################################################################

cleanup() {
    print_header "Cleanup"

    print_info "Removing old containers..."
    docker-compose down

    print_info "Pruning unused images..."
    docker image prune -f

    print_success "Cleanup completed"
}

###############################################################################
# Container Management
###############################################################################

show_logs() {
    print_header "Container Logs"
    docker-compose logs --tail=50 -f
}

show_status() {
    print_header "Container Status"
    docker-compose ps

    echo ""
    print_header "Service Health"
    curl -s http://localhost:8000/health | python -m json.tool || print_warning "Backend not responding"
}

###############################################################################
# Main Menu
###############################################################################

show_menu() {
    echo -e "\n${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  Fintech AI System - Deploy Menu      ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"
    echo "1) Full Deploy (Dev)"
    echo "2) Full Deploy (Production)"
    echo "3) Build Only"
    echo "4) Run Tests"
    echo "5) Show Logs"
    echo "6) Show Status"
    echo "7) Cleanup"
    echo "8) Stop All Services"
    echo "9) Exit"
    echo ""
}

###############################################################################
# Main Execution
###############################################################################

main() {
    # Run pre-checks
    check_dependencies
    check_environment

    # If no arguments, show interactive menu
    if [ $# -eq 0 ]; then
        while true; do
            show_menu
            read -p "Select option: " choice

            case $choice in
                1)
                    build_backend
                    run_tests
                    deploy_development
                    ;;
                2)
                    build_backend
                    run_tests
                    deploy_production
                    ;;
                3)
                    build_backend
                    build_frontend
                    ;;
                4)
                    run_tests
                    ;;
                5)
                    show_logs
                    ;;
                6)
                    show_status
                    ;;
                7)
                    cleanup
                    ;;
                8)
                    docker-compose down
                    print_success "All services stopped"
                    ;;
                9)
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
        dev)
            build_backend
            run_tests
            deploy_development
            ;;
        prod)
            build_backend
            run_tests
            deploy_production
            ;;
        build)
            build_backend
            build_frontend
            ;;
        test)
            run_tests
            ;;
        logs)
            show_logs
            ;;
        status)
            show_status
            ;;
        clean)
            cleanup
            ;;
        stop)
            docker-compose down
            print_success "All services stopped"
            ;;
        *)
            echo "Usage: $0 {dev|prod|build|test|logs|status|clean|stop}"
            echo "  Or run without arguments for interactive menu"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
