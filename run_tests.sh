#!/bin/bash

echo "🧪 Running Web Scraper Tests..."

# Check if running in Docker or locally
if [ -f /.dockerenv ]; then
    echo "🐳 Running tests in Docker container..."
    cd /app
else
    echo "💻 Running tests locally..."
    # Check if pytest is installed
    if ! command -v pytest &> /dev/null; then
        echo "📦 Installing test dependencies..."
        pip install pytest httpx
    fi
fi

# Check if tests directory exists
if [ ! -d "tests" ]; then
    echo "❌ Tests directory not found!"
    echo "Current directory: $(pwd)"
    echo "Available files:"
    ls -la
    exit 1
fi

# Run tests
echo "🔍 Running backend tests..."
pytest tests/ -v --tb=short

echo "✅ Tests completed!" 