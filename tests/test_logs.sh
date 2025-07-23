#!/bin/bash

echo "=== TESTING LOGGING SYSTEM IN DOCKER CONTAINER ==="

# Check if containers are running
if ! docker-compose ps | grep -q "backend.*Up"; then
    echo "❌ Backend container is not running. Starting containers..."
    docker-compose up -d --build
    sleep 10
fi

echo "✅ Containers are running"

# Test logging by making a request to the API
echo "📝 Testing logging by making API requests..."

# Test health endpoint
echo "🔍 Testing health endpoint..."
curl -s http://localhost:8001/api/health

# Test debug logs endpoint
echo -e "\n🔍 Testing debug logs endpoint..."
curl -s http://localhost:8001/api/debug/logs | jq . 2>/dev/null || curl -s http://localhost:8001/api/debug/logs

# Check if log files exist in container
echo -e "\n📁 Checking log files in container..."
docker exec python-web-scrapper-backend-1 ls -la /app/logs/ 2>/dev/null || echo "❌ Cannot access container logs directory"

# Check if log files exist on host
echo -e "\n📁 Checking log files on host..."
if [ -d "backend/logs" ]; then
    echo "✅ Logs directory exists on host"
    ls -la backend/logs/
    
    # Show content of log files
    for log_file in backend/logs/*.log; do
        if [ -f "$log_file" ]; then
            echo -e "\n📄 Content of $(basename "$log_file"):"
            echo "--- Last 10 lines ---"
            tail -10 "$log_file" 2>/dev/null || echo "Cannot read file"
        fi
    done
else
    echo "❌ Logs directory not found on host"
fi

echo -e "\n=== LOGGING TEST COMPLETED ===" 