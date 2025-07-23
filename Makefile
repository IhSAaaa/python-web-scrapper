.PHONY: help install start stop clean build docker-build docker-run

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install all dependencies
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "📦 Installing Node.js dependencies..."
	cd frontend && npm install && cd ..

start: ## Start both backend and frontend
	@echo "🚀 Starting Web Scraper..."
	@echo "🔧 Backend: http://localhost:8001"
	@echo "🎨 Frontend: http://localhost:3000"
	@echo "📚 API Docs: http://localhost:8001/docs"
	@echo ""
	@echo "Starting backend..."
	cd backend && python main.py &
	@sleep 3
	@echo "Starting frontend..."
	cd frontend && npm run dev

stop: ## Stop all running processes
	@pkill -f "python main.py" || true
	@pkill -f "vite" || true
	@echo "✅ All processes stopped"

clean: ## Clean up generated files
	@echo "🧹 Cleaning up..."
	rm -rf output/*
	rm -rf frontend/node_modules
	rm -rf frontend/dist
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "✅ Cleanup completed"

build: ## Build frontend for production
	@echo "🏗️ Building frontend..."
	cd frontend && npm run build

docker-build: ## Build Docker images
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-run: ## Run with Docker Compose
	@echo "🐳 Starting with Docker Compose..."
	docker-compose up -d

docker-stop: ## Stop Docker containers
	@echo "🐳 Stopping Docker containers..."
	docker-compose down

docker-prod: ## Build and run production Docker images
	@echo "🐳 Building production Docker images..."
	docker-compose -f docker-compose.prod.yml build
	@echo "🐳 Starting production containers..."
	docker-compose -f docker-compose.prod.yml up -d

docker-prod-stop: ## Stop production Docker containers
	@echo "🐳 Stopping production containers..."
	docker-compose -f docker-compose.prod.yml down

docker-logs: ## View Docker logs
	@echo "📋 Viewing Docker logs..."
	docker-compose logs -f

docker-clean: ## Clean Docker images and containers
	@echo "🧹 Cleaning Docker resources..."
	docker-compose down -v
	docker system prune -f

dev: ## Start development environment
	@echo "🛠️ Starting development environment..."
	@make install
	@make start

prod: ## Start production environment
	@echo "🚀 Starting production environment..."
	@make build
	@make docker-build
	@make docker-run 