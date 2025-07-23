#!/bin/bash

# Manual Cleanup Script for Web Scraper
# This script provides easy commands for cleaning up output folders

set -e

# Configuration
BACKEND_URL="http://localhost:8001"
OUTPUT_DIR="output"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}🧹 Web Scraper Cleanup Tool${NC}"
    echo "=================================="
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

check_backend() {
    print_info "Checking backend connection..."
    if curl -s -f "$BACKEND_URL/api/health" > /dev/null; then
        print_success "Backend is running"
        return 0
    else
        print_error "Backend is not responding"
        print_info "Make sure the backend is running on $BACKEND_URL"
        return 1
    fi
}

get_stats() {
    print_info "Getting maintenance stats..."
    response=$(curl -s "$BACKEND_URL/api/maintenance/stats")
    
    if [ $? -eq 0 ]; then
        sessions=$(echo "$response" | grep -o '"total_sessions":[0-9]*' | cut -d':' -f2)
        size=$(echo "$response" | grep -o '"total_size_mb":[0-9.]*' | cut -d':' -f2)
        print_success "Current stats: $sessions sessions, ${size}MB total"
    else
        print_error "Failed to get stats"
    fi
}

cleanup_old() {
    local hours=${1:-1}
    print_info "Cleaning up sessions older than $hours hour(s)..."
    
    response=$(curl -s -X POST "$BACKEND_URL/api/maintenance/cleanup?older_than_hours=$hours")
    
    if [ $? -eq 0 ]; then
        cleaned=$(echo "$response" | grep -o '"cleaned_sessions":[0-9]*' | cut -d':' -f2)
        size_freed=$(echo "$response" | grep -o '"total_size_freed_mb":[0-9.]*' | cut -d':' -f2)
        print_success "Cleaned up $cleaned sessions, freed ${size_freed}MB"
    else
        print_error "Failed to cleanup old sessions"
    fi
}

cleanup_all() {
    print_warning "This will delete ALL session folders!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Cleaning up all sessions..."
        response=$(curl -s -X POST "$BACKEND_URL/api/maintenance/cleanup-all")
        
        if [ $? -eq 0 ]; then
            cleaned=$(echo "$response" | grep -o '"cleaned_sessions":[0-9]*' | cut -d':' -f2)
            size_freed=$(echo "$response" | grep -o '"total_size_freed_mb":[0-9.]*' | cut -d':' -f2)
            print_success "Cleaned up $cleaned sessions, freed ${size_freed}MB"
        else
            print_error "Failed to cleanup all sessions"
        fi
    else
        print_info "Cleanup cancelled"
    fi
}

cleanup_specific() {
    local session_id=$1
    if [ -z "$session_id" ]; then
        print_error "Session ID is required"
        print_info "Usage: $0 specific <session_id>"
        exit 1
    fi
    
    print_info "Cleaning up session: $session_id"
    response=$(curl -s -X POST "$BACKEND_URL/api/maintenance/cleanup/$session_id")
    
    if [ $? -eq 0 ]; then
        size_freed=$(echo "$response" | grep -o '"size_freed_mb":[0-9.]*' | cut -d':' -f2)
        print_success "Session cleaned up, freed ${size_freed}MB"
    else
        print_error "Failed to cleanup session"
    fi
}

list_sessions() {
    print_info "Listing current sessions..."
    
    if [ ! -d "$OUTPUT_DIR" ]; then
        print_warning "Output directory does not exist"
        return
    fi
    
    sessions=$(find "$OUTPUT_DIR" -maxdepth 1 -type d -name "*" | grep -v "^$OUTPUT_DIR$" | wc -l)
    
    if [ "$sessions" -eq 0 ]; then
        print_success "No sessions found"
        return
    fi
    
    print_info "Found $sessions session(s):"
    echo
    
    for session_dir in "$OUTPUT_DIR"/*/; do
        if [ -d "$session_dir" ]; then
            session_id=$(basename "$session_dir")
            creation_time=$(stat -c %Y "$session_dir")
            age_hours=$(( ( $(date +%s) - creation_time ) / 3600 ))
            size=$(du -sh "$session_dir" 2>/dev/null | cut -f1)
            file_count=$(find "$session_dir" -type f | wc -l)
            
            echo "  📁 $session_id"
            echo "     Age: ${age_hours}h | Files: $file_count | Size: $size"
            echo
        fi
    done
}

show_help() {
    print_header
    echo "Usage: $0 <command> [options]"
    echo
    echo "Commands:"
    echo "  stats                    Show current maintenance stats"
    echo "  list                     List all current sessions"
    echo "  old [hours]              Clean up sessions older than hours (default: 1)"
    echo "  all                      Clean up ALL sessions (use with caution)"
    echo "  specific <session_id>    Clean up a specific session"
    echo "  help                     Show this help message"
    echo
    echo "Examples:"
    echo "  $0 stats                 # Show current stats"
    echo "  $0 list                  # List all sessions"
    echo "  $0 old 24                # Clean up sessions older than 24 hours"
    echo "  $0 all                   # Clean up all sessions"
    echo "  $0 specific abc123       # Clean up specific session"
    echo
}

# Main script
main() {
    local command=${1:-help}
    
    case $command in
        "stats")
            check_backend && get_stats
            ;;
        "list")
            list_sessions
            ;;
        "old")
            local hours=${2:-1}
            check_backend && cleanup_old "$hours"
            ;;
        "all")
            check_backend && cleanup_all
            ;;
        "specific")
            local session_id=$2
            check_backend && cleanup_specific "$session_id"
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@" 