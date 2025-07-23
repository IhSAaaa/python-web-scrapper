#!/bin/bash

echo "🚀 Starting Web Scraper in Production Mode..."

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

# Build and start production containers
echo "🏗️ Building production Docker images..."
docker-compose -f docker-compose.prod.yml build

echo "🚀 Starting production containers..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 15

# Check if services are running
echo "🔍 Checking service status..."
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo ""
    echo "🎉 Web Scraper is running in production mode!"
    echo ""
    echo "🌐 Frontend: http://localhost"
    echo "🔧 Backend API: http://localhost:8001"
    echo "📚 API Docs: http://localhost:8001/docs"
    echo ""
    echo "📊 Container status:"
    docker-compose -f docker-compose.prod.yml ps
    echo ""
    echo "📝 Useful commands:"
    echo "  View logs: docker-compose -f docker-compose.prod.yml logs -f"
    echo "  Stop services: docker-compose -f docker-compose.prod.yml down"
    echo "  Restart services: docker-compose -f docker-compose.prod.yml restart"
    echo "  View logs (backend): docker-compose -f docker-compose.prod.yml logs backend"
    echo "  View logs (frontend): docker-compose -f docker-compose.prod.yml logs frontend"
else
    echo "❌ Failed to start services. Check logs with: docker-compose -f docker-compose.prod.yml logs"
    exit 1
fi 