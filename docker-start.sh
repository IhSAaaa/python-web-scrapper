#!/bin/bash

echo "🐳 Starting Web Scraper with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker environment check passed!"

# Create output directory if it doesn't exist
mkdir -p output

# Build and start containers
echo "🏗️ Building Docker images..."
docker-compose build

echo "🚀 Starting containers..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "🎉 Web Scraper is running successfully!"
    echo ""
    echo "📱 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8001"
    echo "📚 API Docs: http://localhost:8001/docs"
    echo ""
    echo "📊 Container status:"
    docker-compose ps
    echo ""
    echo "📝 Useful commands:"
    echo "  View logs: docker-compose logs -f"
    echo "  Stop services: docker-compose down"
    echo "  Restart services: docker-compose restart"
    echo "  View logs (backend): docker-compose logs backend"
    echo "  View logs (frontend): docker-compose logs frontend"
else
    echo "❌ Failed to start services. Check logs with: docker-compose logs"
    exit 1
fi 