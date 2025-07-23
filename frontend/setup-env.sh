#!/bin/bash

# Environment Setup Script for Web Scraper Frontend
# This script helps create environment files for different environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}🔧 Environment Setup Script${NC}"
    echo "================================"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running in Docker
is_docker() {
    [ -f /.dockerenv ] || [ -f /proc/1/cgroup ] && grep -q docker /proc/1/cgroup
}

# Get backend URL
get_backend_url() {
    if is_docker; then
        echo "http://backend:8000"
    else
        echo "http://localhost:8001"
    fi
}

# Create development environment file
create_dev_env() {
    print_info "Creating development environment file..."
    
    cat > .env.development << EOF
# Development Environment Configuration
VITE_API_BASE_URL=$(get_backend_url)
VITE_APP_TITLE=Web Scraper (Development)
VITE_APP_VERSION=1.0.0
EOF
    
    print_success "Development environment file created: .env.development"
}

# Create production environment file
create_prod_env() {
    print_info "Creating production environment file..."
    
    cat > .env.production << EOF
# Production Environment Configuration
VITE_API_BASE_URL=$(get_backend_url)
VITE_APP_TITLE=Web Scraper
VITE_APP_VERSION=1.0.0
EOF
    
    print_success "Production environment file created: .env.production"
}

# Create local environment file
create_local_env() {
    print_info "Creating local environment file..."
    
    cat > .env.local << EOF
# Local Development Environment Configuration
VITE_API_BASE_URL=http://localhost:8001
VITE_APP_TITLE=Web Scraper (Local)
VITE_APP_VERSION=1.0.0
EOF
    
    print_success "Local environment file created: .env.local"
}

# Main execution
main() {
    print_header
    
    # Check if we're in the frontend directory
    if [ ! -f "package.json" ]; then
        print_error "Please run this script from the frontend directory"
        exit 1
    fi
    
    # Create environment files
    create_dev_env
    create_prod_env
    create_local_env
    
    print_info "Environment files created successfully!"
    print_info "Backend URL: $(get_backend_url)"
    
    if is_docker; then
        print_warning "Running in Docker environment"
    else
        print_info "Running in local environment"
    fi
    
    echo ""
    print_success "Setup complete! You can now start the development server."
}

# Run main function
main "$@" 