#!/bin/bash

echo "🧪 Running Web Scraper Tests..."

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "📦 Installing test dependencies..."
    pip install pytest httpx
fi

# Run tests
echo "🔍 Running backend tests..."
pytest tests/ -v

echo "✅ Tests completed!" 