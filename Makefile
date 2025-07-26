# Web Scraper Makefile
# Comprehensive build and development automation

# Variables
PROJECT_NAME = web-scraper
DOCKER_COMPOSE = docker compose
DOCKER_COMPOSE_PROD = docker compose -f docker-compose.prod.yml
BACKEND_URL = http://localhost:18000
OUTPUT_DIR = output

# Colors for output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

# Help target
.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)Web Scraper Development Commands$(NC)"
	@echo "====================================="
	@echo ""
	@echo "$(BLUE)🔧 DEVELOPMENT COMMANDS:$(NC)"
	@echo "  dev                   Start development environment with hot reload"
	@echo "  dev-emergency         Start development (bypass permission checks)"
	@echo "  stop                  Stop development environment"
	@echo "  restart               Restart development environment"
	@echo ""
	@echo "$(BLUE)🚀 PRODUCTION COMMANDS:$(NC)"
	@echo "  prod                  Start production environment"
	@echo "  prod-emergency        Start production (bypass permission checks)"
	@echo "  stop-prod             Stop production environment"
	@echo "  restart-prod          Restart production environment"
	@echo ""
	@echo "$(BLUE)🧪 TESTING COMMANDS:$(NC)"
	@echo "  test                  Run tests in Docker"
	@echo ""
	@echo "$(BLUE)🔨 BUILD COMMANDS:$(NC)"
	@echo "  build                 Build all services using Docker"
	@echo "  build-frontend        Build frontend for production"
	@echo "  build-backend         Prepare backend for production"
	@echo "  rebuild               Rebuild all Docker images"
	@echo "  install               Install all dependencies in Docker"
	@echo ""
	@echo "$(BLUE)📋 LOGS COMMANDS:$(NC)"
	@echo "  logs                  View development logs (follow mode)"
	@echo "  logs-prod             View production logs (follow mode)"
	@echo "  logs-all              View all logs (no follow)"
	@echo "  logs-backend          View backend logs"
	@echo "  logs-frontend         View frontend logs"
	@echo ""
	@echo "$(BLUE)📊 STATUS COMMANDS:$(NC)"
	@echo "  status                Show status of all services"
	@echo "  health                Check health of all services"
	@echo ""
	@echo "$(BLUE)🔐 PERMISSION COMMANDS:$(NC)"
	@echo "  setup-permissions     Setup proper permissions for the application"
	@echo "  test-permissions      Test if permissions are working correctly"
	@echo "  check-permissions     Quick permission check (basic)"
	@echo "  fix-permissions       Fix permission issues (complete solution)"
	@echo "  force-fix-permissions Force fix permissions (non-interactive, with sudo)"
	@echo "  rebuild-with-permissions Rebuild with permission fix and test"
	@echo ""
	@echo "$(BLUE)🧹 CLEANUP COMMANDS:$(NC)"
	@echo "  cleanup               Show cleanup options"
	@echo "  cleanup-sessions-1h   Clean sessions older than 1 hour"
	@echo "  cleanup-sessions-24h  Clean sessions older than 24 hours"
	@echo "  cleanup-sessions-all  Clean all sessions"
	@echo "  cleanup-files         Clean local output files"
	@echo "  cleanup-docker        Clean Docker resources"
	@echo "  clean                 Clean all containers, volumes, and build artifacts"
	@echo ""
	@echo "$(BLUE)🔧 SETUP COMMANDS:$(NC)"
	@echo "  setup                 Complete project setup"
	@echo "  setup-env             Setup environment variables"
	@echo ""
	@echo "$(BLUE)🛠️ UTILITY COMMANDS:$(NC)"
	@echo "  check-docker          Check if Docker is running"
	@echo "  shell                 Open shell in backend container"
	@echo "  shell-frontend        Open shell in frontend container"
	@echo ""
	@echo "$(BLUE)🔄 DEVELOPMENT WORKFLOW:$(NC)"
	@echo "  dev-full              Full development workflow (setup + dev)"
	@echo "  reset                 Reset everything and start fresh"
	@echo ""
	@echo "$(BLUE)📈 MONITORING:$(NC)"
	@echo "  monitor               Monitor all services and logs"
	@echo ""
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make dev              # Start development environment"
	@echo "  make prod             # Start production environment"
	@echo "  make stop             # Stop development environment"
	@echo "  make logs             # View logs"
	@echo "  make clean            # Clean all containers and volumes"
	@echo ""
	@echo "$(BLUE)Quick Start:$(NC)"
	@echo "  make setup-permissions  # Setup permissions first time"
	@echo "  make dev               # Start development environment"
	@echo "  make test-permissions  # Test if everything works"
	@echo ""
	@echo "$(BLUE)Troubleshooting:$(NC)"
	@echo "  make fix-permissions   # Complete permission fix"
	@echo "  make force-fix-permissions # Force fix with sudo"
	@echo "  make check-permissions # Quick permission check"
	@echo "  make logs-backend      # View backend logs"

# =============================================================================
# DEVELOPMENT COMMANDS
# =============================================================================

.PHONY: dev
dev: ## Start development environment with hot reload
	@echo "$(BLUE)[INFO]$(NC) Starting Web Scraper Development Environment..."
	@$(MAKE) check-docker
	@$(MAKE) setup-env
	@$(MAKE) setup-permissions || $(MAKE) force-fix-permissions
	@echo "$(BLUE)[INFO]$(NC) Stopping existing containers..."
	@$(DOCKER_COMPOSE) down --remove-orphans 2>/dev/null || true
	@echo "$(BLUE)[INFO]$(NC) Building and starting development environment..."
	@$(DOCKER_COMPOSE) up -d --build
	@echo "$(BLUE)[INFO]$(NC) Waiting for services to be ready..."
	@sleep 10
	@echo "$(BLUE)[INFO]$(NC) Checking service status..."
	@if docker ps | grep -q "python-web-scrapper-backend"; then \
		echo "$(GREEN)[SUCCESS]$(NC) Backend development server is running!"; \
		echo "$(GREEN)🌐 Frontend:$(NC) http://localhost:3000"; \
		echo "$(GREEN)🔌 Backend:$(NC) http://localhost:18000"; \
		echo ""; \
		echo "$(BLUE)📝 Development mode enabled with hot reload!$(NC)"; \
		echo "$(BLUE)💡 Any changes to code will automatically reload.$(NC)"; \
		echo ""; \
		echo "To stop the development environment, run: $(YELLOW)make stop$(NC)"; \
		echo "To view logs, run: $(YELLOW)make logs$(NC)"; \
	else \
		echo "$(RED)[ERROR]$(NC) Backend failed to start. Check logs with: $(YELLOW)make logs$(NC)"; \
		exit 1; \
	fi

.PHONY: dev-emergency
dev-emergency: ## Start development environment (bypass permission checks)
	@echo "$(YELLOW)[WARNING]$(NC) Emergency Development Startup (bypassing permission checks)"
	@echo "====================================="
	@$(MAKE) check-docker
	@$(MAKE) setup-env
	@echo "$(BLUE)[INFO]$(NC) Stopping existing containers..."
	@$(DOCKER_COMPOSE) down --remove-orphans 2>/dev/null || true
	@echo "$(BLUE)[INFO]$(NC) Building and starting development environment..."
	@$(DOCKER_COMPOSE) up -d --build
	@echo "$(GREEN)[SUCCESS]$(NC) Emergency development environment started!"
	@echo "$(GREEN)🌐 Frontend:$(NC) http://localhost:3000"
	@echo "$(GREEN)🔌 Backend:$(NC) http://localhost:18000"
	@echo "$(YELLOW)[WARNING]$(NC) Note: Permission issues may still occur"

.PHONY: stop
stop: ## Stop development environment
	@echo "$(BLUE)[INFO]$(NC) Stopping Web Scraper Development Environment..."
	@$(DOCKER_COMPOSE) down
	@echo "$(GREEN)[SUCCESS]$(NC) Development environment stopped!"
	@echo ""
	@echo "To start development environment again, run: $(YELLOW)make dev$(NC)"

.PHONY: restart
restart: ## Restart development environment
	@echo "$(BLUE)[INFO]$(NC) Restarting development environment..."
	@$(MAKE) stop
	@$(MAKE) dev

# =============================================================================
# PRODUCTION COMMANDS
# =============================================================================

.PHONY: prod
prod: ## Start production environment
	@echo "$(BLUE)[INFO]$(NC) Starting Web Scraper Production Environment..."
	@$(MAKE) check-docker
	@$(MAKE) setup-env
	@$(MAKE) setup-permissions || $(MAKE) force-fix-permissions
	@echo "$(BLUE)[INFO]$(NC) Stopping existing containers..."
	@$(DOCKER_COMPOSE_PROD) down --remove-orphans 2>/dev/null || true
	@echo "$(BLUE)[INFO]$(NC) Building and starting production environment..."
	@$(DOCKER_COMPOSE_PROD) up -d --build
	@echo "$(GREEN)[SUCCESS]$(NC) Production environment started!"
	@echo "$(GREEN)🌐 Frontend:$(NC) http://localhost:80"
	@echo "$(GREEN)🔌 Backend:$(NC) http://localhost:8001"

.PHONY: prod-emergency
prod-emergency: ## Start production environment (bypass permission checks)
	@echo "$(YELLOW)[WARNING]$(NC) Emergency Production Startup (bypassing permission checks)"
	@echo "====================================="
	@$(MAKE) check-docker
	@$(MAKE) setup-env
	@echo "$(BLUE)[INFO]$(NC) Stopping existing containers..."
	@$(DOCKER_COMPOSE_PROD) down --remove-orphans 2>/dev/null || true
	@echo "$(BLUE)[INFO]$(NC) Building and starting production environment..."
	@$(DOCKER_COMPOSE_PROD) up -d --build
	@echo "$(GREEN)[SUCCESS]$(NC) Emergency production environment started!"
	@echo "$(GREEN)🌐 Frontend:$(NC) http://localhost:80"
	@echo "$(GREEN)🔌 Backend:$(NC) http://localhost:8001"
	@echo "$(YELLOW)[WARNING]$(NC) Note: Permission issues may still occur"

.PHONY: stop-prod
stop-prod: ## Stop production environment
	@echo "$(BLUE)[INFO]$(NC) Stopping Web Scraper Production Environment..."
	@$(DOCKER_COMPOSE_PROD) down
	@echo "$(GREEN)[SUCCESS]$(NC) Production environment stopped!"

.PHONY: restart-prod
restart-prod: ## Restart production environment
	@echo "$(BLUE)[INFO]$(NC) Restarting production environment..."
	@$(MAKE) stop-prod
	@$(MAKE) prod

# =============================================================================
# TESTING COMMANDS
# =============================================================================

.PHONY: test
test: ## Run tests in Docker
	@echo "$(BLUE)[INFO]$(NC) Running tests..."
	@docker compose run --rm test || (echo "$(RED)[ERROR]$(NC) Tests failed" && exit 1)
	@echo "$(GREEN)[SUCCESS]$(NC) Tests completed!"

.PHONY: test-api-config
test-api-config: ## Test API configuration in production
	@echo "$(BLUE)[INFO]$(NC) Testing API configuration..."
	@echo "$(YELLOW)Testing backend health check...$(NC)"
	@curl -f http://localhost:18000/api/health || echo "$(RED)Backend health check failed$(NC)"
	@echo "$(YELLOW)Testing frontend API proxy...$(NC)"
	@curl -f http://localhost:180/api/health || echo "$(RED)Frontend API proxy failed$(NC)"
	@echo "$(YELLOW)Testing direct API endpoint...$(NC)"
	@curl -f http://localhost:18000/scrape -X POST -H "Content-Type: application/json" -d '{"url":"https://example.com"}' || echo "$(RED)Direct API endpoint failed$(NC)"
	@echo "$(GREEN)[SUCCESS]$(NC) API configuration test completed!"

# =============================================================================
# BUILD COMMANDS
# =============================================================================

.PHONY: build
build: ## Build all services using Docker
	@echo "$(BLUE)[INFO]$(NC) Building all services using Docker..."
	@$(DOCKER_COMPOSE) build
	@$(DOCKER_COMPOSE_PROD) build
	@echo "$(GREEN)[SUCCESS]$(NC) All services built successfully!"

.PHONY: build-frontend
build-frontend: ## Build frontend for production
	@echo "$(BLUE)[INFO]$(NC) Building frontend for production..."
	@docker run --rm -v $(PWD)/frontend:/app -w /app node:18-alpine sh -c "npm install && npm run build"
	@echo "$(GREEN)[SUCCESS]$(NC) Frontend built for production!"

.PHONY: build-frontend-prod
build-frontend-prod: ## Build frontend for production with correct API configuration
	@echo "$(BLUE)[INFO]$(NC) Building frontend for production with API configuration..."
	@docker build \
		--build-arg VITE_API_BASE_URL= \
		-f frontend/Dockerfile.frontend.prod \
		-t web-scraper-frontend:prod \
		./frontend
	@echo "$(GREEN)[SUCCESS]$(NC) Frontend built for production with correct API configuration!"

.PHONY: build-backend
build-backend: ## Prepare backend for production
	@echo "$(BLUE)[INFO]$(NC) Preparing backend for production..."
	@docker compose run --rm backend pip install -r requirements.txt
	@docker compose run --rm backend python -c "import fastapi, uvicorn; print('✅ Backend dependencies verified')"
	@echo "$(GREEN)[SUCCESS]$(NC) Backend prepared for production!"

.PHONY: rebuild
rebuild: ## Rebuild all Docker images
	@echo "$(BLUE)[INFO]$(NC) Rebuilding all Docker images..."
	@$(MAKE) setup-permissions || $(MAKE) force-fix-permissions
	@$(DOCKER_COMPOSE) build --no-cache
	@$(DOCKER_COMPOSE_PROD) build --no-cache
	@echo "$(GREEN)[SUCCESS]$(NC) All images rebuilt"

.PHONY: rebuild-prod
rebuild-prod: ## Rebuild production images with correct configuration
	@echo "$(BLUE)[INFO]$(NC) Rebuilding production images with correct API configuration..."
	@$(MAKE) setup-permissions || $(MAKE) force-fix-permissions
	@$(MAKE) build-frontend-prod
	@$(DOCKER_COMPOSE_PROD) build --no-cache backend
	@echo "$(GREEN)[SUCCESS]$(NC) Production images rebuilt with correct configuration!"

.PHONY: install
install: ## Install all dependencies in Docker
	@echo "$(BLUE)[INFO]$(NC) Installing dependencies in Docker..."
	@echo "$(BLUE)[INFO]$(NC) Installing Python dependencies..."
	@docker compose run --rm backend pip install -r requirements.txt
	@echo "$(BLUE)[INFO]$(NC) Installing Node.js dependencies..."
	@docker compose run --rm frontend npm install
	@echo "$(GREEN)[SUCCESS]$(NC) All dependencies installed in Docker!"

# =============================================================================
# LOGS COMMANDS
# =============================================================================

.PHONY: logs
logs: ## View development logs (follow mode)
	@echo "$(BLUE)[INFO]$(NC) Viewing development logs..."
	@$(DOCKER_COMPOSE) logs -f

.PHONY: logs-prod
logs-prod: ## View production logs (follow mode)
	@echo "$(BLUE)[INFO]$(NC) Viewing production logs..."
	@$(DOCKER_COMPOSE_PROD) logs -f

.PHONY: logs-all
logs-all: ## View all logs (no follow)
	@echo "$(BLUE)[INFO]$(NC) Viewing all logs..."
	@echo "$(YELLOW)Development logs:$(NC)"
	@$(DOCKER_COMPOSE) logs
	@echo ""
	@echo "$(YELLOW)Production logs:$(NC)"
	@$(DOCKER_COMPOSE_PROD) logs

.PHONY: logs-backend
logs-backend: ## View backend logs
	@echo "$(BLUE)[INFO]$(NC) Viewing backend logs..."
	@$(DOCKER_COMPOSE) logs backend

.PHONY: logs-frontend
logs-frontend: ## View frontend logs
	@echo "$(BLUE)[INFO]$(NC) Viewing frontend logs..."
	@$(DOCKER_COMPOSE) logs frontend

# =============================================================================
# STATUS COMMANDS
# =============================================================================

.PHONY: status
status: ## Show status of all services
	@echo "$(BLUE)[INFO]$(NC) Checking service status..."
	@echo "$(BLUE)Development containers:$(NC)"
	@if $(DOCKER_COMPOSE) ps | grep -q "Up"; then \
		echo "  $(GREEN)✅ Running$(NC)"; \
		$(DOCKER_COMPOSE) ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"; \
	else \
		echo "  $(RED)❌ Not running$(NC)"; \
	fi
	@echo ""
	@echo "$(BLUE)Production containers:$(NC)"
	@if $(DOCKER_COMPOSE_PROD) ps | grep -q "Up"; then \
		echo "  $(GREEN)✅ Running$(NC)"; \
		$(DOCKER_COMPOSE_PROD) ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"; \
	else \
		echo "  $(RED)❌ Not running$(NC)"; \
	fi

.PHONY: health
health: ## Check health of all services
	@echo "$(BLUE)[INFO]$(NC) Checking service health..."
	@echo "$(BLUE)Backend Health:$(NC)"
	@if docker compose ps backend | grep -q "Up"; then \
		echo "  $(GREEN)✅ Backend container is running$(NC)"; \
		docker compose exec backend python -c "import requests; import json; r = requests.get('http://localhost:8000/api/health'); print(json.dumps(r.json(), indent=2))" 2>/dev/null || echo "  $(RED)❌ Backend health check failed$(NC)"; \
	else \
		echo "  $(RED)❌ Backend container is not running$(NC)"; \
	fi
	@echo ""
	@echo "$(BLUE)Frontend Health:$(NC)"
	@if docker compose ps frontend | grep -q "Up"; then \
		echo "  $(GREEN)✅ Development frontend container is running$(NC)"; \
	elif docker compose -f docker-compose.prod.yml ps frontend | grep -q "Up"; then \
		echo "  $(GREEN)✅ Production frontend container is running$(NC)"; \
	else \
		echo "  $(RED)❌ Frontend container is not running$(NC)"; \
	fi

# =============================================================================
# PERMISSION COMMANDS
# =============================================================================

.PHONY: setup-permissions
setup-permissions: ## Setup proper permissions for the application
	@echo "$(BLUE)[INFO]$(NC) Setting up Web Scraper permissions..."
	@echo "====================================="
	@if [ ! -d "$(OUTPUT_DIR)" ]; then \
		echo "$(BLUE)[INFO]$(NC) Creating output directory..."; \
		mkdir -p "$(OUTPUT_DIR)"; \
	fi
	@echo "$(BLUE)[INFO]$(NC) Setting proper permissions for output directory..."
	@CURRENT_USER=$$(whoami); \
	CURRENT_UID=$$(id -u); \
	echo "$(BLUE)[INFO]$(NC) Current user: $$CURRENT_USER (UID: $$CURRENT_UID)"; \
	if [ "$$CURRENT_UID" -eq 0 ]; then \
		echo "$(BLUE)[INFO]$(NC) Running as root, setting ownership to 1000:1000"; \
		chown -R 1000:1000 "$(OUTPUT_DIR)"; \
		chmod -R 755 "$(OUTPUT_DIR)"; \
	elif [ -w "$(OUTPUT_DIR)" ]; then \
		echo "$(GREEN)[SUCCESS]$(NC) Current user can write to output directory"; \
		chmod -R 755 "$(OUTPUT_DIR)"; \
	else \
		echo "$(RED)[ERROR]$(NC) Current user cannot write to output directory"; \
		echo "$(BLUE)[INFO]$(NC) Attempting to fix permissions..."; \
		if command -v sudo >/dev/null 2>&1; then \
			echo "$(BLUE)[INFO]$(NC) Using sudo to fix permissions..."; \
			sudo chown -R $$CURRENT_USER:$$CURRENT_USER "$(OUTPUT_DIR)" 2>/dev/null || \
			sudo chown -R 1000:1000 "$(OUTPUT_DIR)" 2>/dev/null || \
			(echo "$(RED)[ERROR]$(NC) Failed to fix permissions with sudo" && exit 1); \
			sudo chmod -R 755 "$(OUTPUT_DIR)" 2>/dev/null || \
			(echo "$(RED)[ERROR]$(NC) Failed to set permissions" && exit 1); \
			echo "$(GREEN)[SUCCESS]$(NC) Permissions fixed with sudo"; \
		else \
			echo "$(RED)[ERROR]$(NC) Sudo not available. Please run manually:"; \
			echo "   chown -R $$CURRENT_USER:$$CURRENT_USER $(OUTPUT_DIR)"; \
			echo "   chmod -R 755 $(OUTPUT_DIR)"; \
			exit 1; \
		fi; \
	fi
	@echo "$(BLUE)[INFO]$(NC) Verifying permissions..."
	@ls -la "$(OUTPUT_DIR)"
	@echo "$(GREEN)[SUCCESS]$(NC) Permission setup completed!"

.PHONY: force-fix-permissions
force-fix-permissions: ## Force fix permissions (non-interactive, with sudo)
	@echo "$(BLUE)[INFO]$(NC) Force fixing permissions..."
	@echo "====================================="
	@if [ ! -d "$(OUTPUT_DIR)" ]; then \
		echo "$(BLUE)[INFO]$(NC) Creating output directory..."; \
		mkdir -p "$(OUTPUT_DIR)"; \
	fi
	@CURRENT_USER=$$(whoami); \
	CURRENT_UID=$$(id -u); \
	echo "$(BLUE)[INFO]$(NC) Current user: $$CURRENT_USER (UID: $$CURRENT_UID)"; \
	if command -v sudo >/dev/null 2>&1; then \
		echo "$(BLUE)[INFO]$(NC) Using sudo to force fix permissions..."; \
		sudo chown -R $$CURRENT_USER:$$CURRENT_USER "$(OUTPUT_DIR)" 2>/dev/null || \
		sudo chown -R 1000:1000 "$(OUTPUT_DIR)" 2>/dev/null || \
		(echo "$(RED)[ERROR]$(NC) Failed to fix permissions with sudo" && exit 1); \
		sudo chmod -R 755 "$(OUTPUT_DIR)" 2>/dev/null || \
		(echo "$(RED)[ERROR]$(NC) Failed to set permissions" && exit 1); \
		echo "$(GREEN)[SUCCESS]$(NC) Permissions force fixed with sudo"; \
	else \
		echo "$(RED)[ERROR]$(NC) Sudo not available. Please run manually:"; \
		echo "   chown -R $$CURRENT_USER:$$CURRENT_USER $(OUTPUT_DIR)"; \
		echo "   chmod -R 755 $(OUTPUT_DIR)"; \
		exit 1; \
	fi
	@echo "$(BLUE)[INFO]$(NC) Verifying permissions..."
	@ls -la "$(OUTPUT_DIR)"

.PHONY: test-permissions
test-permissions: ## Test if permissions are working correctly
	@echo "$(BLUE)[INFO]$(NC) Testing Web Scraper permissions..."
	@echo "====================================="
	@echo ""
	@echo "$(BLUE)[INFO]$(NC) Test 1: Checking if containers are running..."
	@if docker ps | grep -q "python-web-scrapper-backend"; then \
		echo "$(GREEN)[SUCCESS]$(NC) Backend container is running"; \
	else \
		echo "$(RED)[ERROR]$(NC) Backend container is not running"; \
		echo "$(BLUE)[INFO]$(NC) Start containers with: make dev"; \
		exit 1; \
	fi
	@if docker ps | grep -q "python-web-scrapper-frontend"; then \
		echo "$(GREEN)[SUCCESS]$(NC) Frontend container is running"; \
	else \
		echo "$(RED)[ERROR]$(NC) Frontend container is not running"; \
		echo "$(BLUE)[INFO]$(NC) Start containers with: make dev"; \
		exit 1; \
	fi
	@echo ""
	@echo "$(BLUE)[INFO]$(NC) Test 2: Checking container user..."
	@CONTAINER_USER=$$(docker exec python-web-scrapper-backend-1 whoami 2>/dev/null || echo "unknown"); \
	if [ "$$CONTAINER_USER" = "scraper" ]; then \
		echo "$(GREEN)[SUCCESS]$(NC) Container is running as non-root user: $$CONTAINER_USER"; \
	else \
		echo "$(RED)[ERROR]$(NC) Container user is: $$CONTAINER_USER (expected: scraper)"; \
	fi
	@echo ""
	@echo "$(BLUE)[INFO]$(NC) Test 3: Checking output directory permissions in container..."
	@if docker exec python-web-scrapper-backend-1 test -w /app/output; then \
		echo "$(GREEN)[SUCCESS]$(NC) Container can write to /app/output directory"; \
	else \
		echo "$(RED)[ERROR]$(NC) Container cannot write to /app/output directory"; \
	fi
	@echo ""
	@echo "$(BLUE)[INFO]$(NC) Test 4: Checking host output directory permissions..."
	@if [ -w "$(OUTPUT_DIR)" ]; then \
		echo "$(GREEN)[SUCCESS]$(NC) Host can write to output directory"; \
	else \
		echo "$(RED)[ERROR]$(NC) Host cannot write to output directory"; \
	fi
	@echo ""
	@echo "$(BLUE)[INFO]$(NC) Test 5: Checking backend health endpoint..."
	@HEALTH_RESPONSE=$$(curl -s -o /dev/null -w "%{http_code}" $(BACKEND_URL)/api/health 2>/dev/null || echo "000"); \
	if [ "$$HEALTH_RESPONSE" = "200" ]; then \
		echo "$(GREEN)[SUCCESS]$(NC) Backend health endpoint is responding (HTTP $$HEALTH_RESPONSE)"; \
	else \
		echo "$(RED)[ERROR]$(NC) Backend health endpoint is not responding (HTTP $$HEALTH_RESPONSE)"; \
	fi
	@echo ""
	@echo "$(BLUE)[INFO]$(NC) Test 6: Testing scraping functionality..."
	@TEST_RESPONSE=$$(curl -s -X POST $(BACKEND_URL)/api/scrape -H "Content-Type: application/json" -d '{"url": "https://example.com"}' 2>/dev/null | grep -o '"session_id"' | wc -l); \
	if [ "$$TEST_RESPONSE" -gt 0 ]; then \
		echo "$(GREEN)[SUCCESS]$(NC) Scraping functionality is working"; \
	else \
		echo "$(RED)[ERROR]$(NC) Scraping functionality is not working"; \
	fi
	@echo ""
	@echo "$(BLUE)[INFO]$(NC) Test 7: Checking for permission errors in logs..."
	@PERMISSION_ERRORS=$$(docker compose logs backend 2>/dev/null | grep -i "permission denied" | wc -l); \
	if [ "$$PERMISSION_ERRORS" -eq 0 ]; then \
		echo "$(GREEN)[SUCCESS]$(NC) No permission errors found in logs"; \
	else \
		echo "$(RED)[ERROR]$(NC) Found $$PERMISSION_ERRORS permission errors in logs"; \
	fi
	@echo ""
	@echo "$(BLUE)[INFO]$(NC) Test 8: Checking directory ownership..."
	@DIR_OWNER=$$(ls -ld "$(OUTPUT_DIR)" | awk '{print $$3}'); \
	DIR_GROUP=$$(ls -ld "$(OUTPUT_DIR)" | awk '{print $$4}'); \
	echo "$(BLUE)[INFO]$(NC) Output directory owner: $$DIR_OWNER:$$DIR_GROUP"; \
	if [ "$$DIR_OWNER" = "$$(whoami)" ] || [ "$$DIR_OWNER" = "1000" ]; then \
		echo "$(GREEN)[SUCCESS]$(NC) Directory ownership is correct"; \
	else \
		echo "$(RED)[ERROR]$(NC) Directory ownership is incorrect"; \
	fi
	@echo ""
	@echo "$(GREEN)[SUCCESS]$(NC) Permission tests completed!"
	@echo ""
	@echo "$(BLUE)[INFO]$(NC) Useful commands:"
	@echo "   View logs: make logs-backend"
	@echo "   Check status: make status"
	@echo "   Restart: make restart"

.PHONY: check-permissions
check-permissions: ## Quick permission check (basic)
	@echo "$(BLUE)[INFO]$(NC) Quick Permission Check"
	@echo "=========================="
	@echo "$(BLUE)[INFO]$(NC) Checking basic permission status..."
	@if [ -w "$(OUTPUT_DIR)" ]; then \
		echo "$(GREEN)[SUCCESS]$(NC) Host output directory is writable"; \
	else \
		echo "$(RED)[ERROR]$(NC) Host output directory is not writable"; \
	fi
	@if docker ps | grep -q "python-web-scrapper-backend"; then \
		if docker exec python-web-scrapper-backend-1 test -w /app/output 2>/dev/null; then \
			echo "$(GREEN)[SUCCESS]$(NC) Container can write to output directory"; \
		else \
			echo "$(RED)[ERROR]$(NC) Container cannot write to output directory"; \
		fi; \
	else \
		echo "$(YELLOW)[WARNING]$(NC) Backend container is not running"; \
	fi
	@PERMISSION_ERRORS=$$(docker compose logs backend 2>/dev/null | grep -i "permission denied" | wc -l); \
	if [ "$$PERMISSION_ERRORS" -eq 0 ]; then \
		echo "$(GREEN)[SUCCESS]$(NC) No permission errors in logs"; \
	else \
		echo "$(RED)[ERROR]$(NC) Found $$PERMISSION_ERRORS permission errors in logs"; \
	fi

.PHONY: fix-permissions
fix-permissions: ## Fix permission issues (complete solution)
	@echo "$(BLUE)[INFO]$(NC) Fixing permission issues..."
	@echo "====================================="
	@echo "$(BLUE)[INFO]$(NC) This will:"
	@echo "1. Setup proper permissions"
	@echo "2. Rebuild containers"
	@echo "3. Test the fix"
	@echo ""
	@read -p "Continue? (y/N): " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(BLUE)[INFO]$(NC) Step 1: Setting up permissions..."; \
		$(MAKE) setup-permissions; \
		echo "$(BLUE)[INFO]$(NC) Step 2: Rebuilding containers..."; \
		docker compose down; \
		docker compose build --no-cache; \
		docker compose up -d; \
		echo "$(BLUE)[INFO]$(NC) Waiting for containers to start..."; \
		sleep 10; \
		echo "$(BLUE)[INFO]$(NC) Step 3: Testing permissions..."; \
		$(MAKE) test-permissions; \
		echo "$(GREEN)[SUCCESS]$(NC) Permission fix completed!"; \
	else \
		echo "$(YELLOW)[INFO]$(NC) Permission fix cancelled"; \
	fi

.PHONY: rebuild-with-permissions
rebuild-with-permissions: ## Rebuild with permission fix and test
	@echo "$(BLUE)[INFO]$(NC) Rebuilding with permission fix..."
	@$(MAKE) setup-permissions
	@docker compose down
	@docker compose build --no-cache
	@docker compose up -d
	@echo "$(GREEN)[SUCCESS]$(NC) Rebuild completed!"
	@echo "$(BLUE)[INFO]$(NC) Testing permissions..."
	@$(MAKE) test-permissions

# =============================================================================
# CLEANUP COMMANDS
# =============================================================================

.PHONY: cleanup
cleanup: ## Show cleanup options
	@echo "$(BLUE)[INFO]$(NC) Cleanup Options"
	@echo "=================="
	@echo "1. Clean old sessions (1 hour)"
	@echo "2. Clean old sessions (24 hours)"
	@echo "3. Clean all sessions"
	@echo "4. Clean local files"
	@echo "5. Clean Docker resources"
	@echo ""
	@read -p "Choose option (1-5): " choice; \
	case $$choice in \
		1) \
			echo "$(BLUE)[INFO]$(NC) Cleaning sessions older than 1 hour..."; \
			$(MAKE) cleanup-sessions-1h; \
			;; \
		2) \
			echo "$(BLUE)[INFO]$(NC) Cleaning sessions older than 24 hours..."; \
			$(MAKE) cleanup-sessions-24h; \
			;; \
		3) \
			echo "$(YELLOW)[WARNING]$(NC) This will delete ALL sessions!"; \
			read -p "Are you sure? (y/N): " -n 1 -r; \
			echo; \
			if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
				$(MAKE) cleanup-sessions-all; \
			else \
				echo "$(YELLOW)[INFO]$(NC) Cleanup cancelled"; \
			fi; \
			;; \
		4) \
			echo "$(BLUE)[INFO]$(NC) Cleaning local files..."; \
			$(MAKE) cleanup-files; \
			;; \
		5) \
			echo "$(BLUE)[INFO]$(NC) Cleaning Docker resources..."; \
			$(MAKE) cleanup-docker; \
			;; \
		*) \
			echo "$(RED)[ERROR]$(NC) Invalid option"; \
			;; \
	esac

.PHONY: cleanup-sessions-1h
cleanup-sessions-1h: ## Clean sessions older than 1 hour
	@echo "$(BLUE)[INFO]$(NC) Cleaning sessions older than 1 hour..."
	@if docker compose ps backend | grep -q "Up"; then \
		docker compose exec backend python -c "import requests; import json; r = requests.post('http://localhost:8000/api/maintenance/cleanup?older_than_hours=1'); print(json.dumps(r.json(), indent=2))" 2>/dev/null || echo "$(RED)[ERROR]$(NC) Cleanup failed"; \
	else \
		echo "$(RED)[ERROR]$(NC) Backend is not running"; \
	fi

.PHONY: cleanup-sessions-24h
cleanup-sessions-24h: ## Clean sessions older than 24 hours
	@echo "$(BLUE)[INFO]$(NC) Cleaning sessions older than 24 hours..."
	@if docker compose ps backend | grep -q "Up"; then \
		docker compose exec backend python -c "import requests; import json; r = requests.post('http://localhost:8000/api/maintenance/cleanup?older_than_hours=24'); print(json.dumps(r.json(), indent=2))" 2>/dev/null || echo "$(RED)[ERROR]$(NC) Cleanup failed"; \
	else \
		echo "$(RED)[ERROR]$(NC) Backend is not running"; \
	fi

.PHONY: cleanup-sessions-all
cleanup-sessions-all: ## Clean all sessions
	@echo "$(BLUE)[INFO]$(NC) Cleaning all sessions..."
	@if docker compose ps backend | grep -q "Up"; then \
		docker compose exec backend python -c "import requests; import json; r = requests.post('http://localhost:8000/api/maintenance/cleanup-all'); print(json.dumps(r.json(), indent=2))" 2>/dev/null || echo "$(RED)[ERROR]$(NC) Cleanup failed"; \
	else \
		echo "$(RED)[ERROR]$(NC) Backend is not running"; \
	fi

.PHONY: cleanup-files
cleanup-files: ## Clean local output files
	@echo "$(BLUE)[INFO]$(NC) Cleaning local files..."
	@rm -rf $(OUTPUT_DIR)/*
	@echo "$(GREEN)[SUCCESS]$(NC) Local files cleaned"

.PHONY: cleanup-docker
cleanup-docker: ## Clean Docker resources
	@echo "$(BLUE)[INFO]$(NC) Cleaning Docker resources..."
	@docker system prune -f
	@docker volume prune -f
	@echo "$(GREEN)[SUCCESS]$(NC) Docker resources cleaned"

.PHONY: clean
clean: ## Clean all containers, volumes, and build artifacts
	@echo "$(BLUE)[INFO]$(NC) Cleaning all containers and volumes..."
	@$(DOCKER_COMPOSE) down -v --remove-orphans
	@$(DOCKER_COMPOSE_PROD) down -v --remove-orphans
	@echo "$(BLUE)[INFO]$(NC) Cleaning build artifacts..."
	@docker system prune -f
	@docker volume prune -f
	@echo "$(GREEN)[SUCCESS]$(NC) Cleanup completed!"

# =============================================================================
# SETUP COMMANDS
# =============================================================================

.PHONY: setup
setup: ## Complete project setup
	@echo "$(BLUE)[INFO]$(NC) Starting Web Scraper Setup..."
	@echo "$(BLUE)[INFO]$(NC) Checking prerequisites..."
	@if ! command -v docker > /dev/null 2>&1; then \
		echo "$(RED)[ERROR]$(NC) Docker is not installed. Please install Docker first."; \
		exit 1; \
	fi
	@if ! docker info > /dev/null 2>&1; then \
		echo "$(RED)[ERROR]$(NC) Docker is not running. Please start Docker first."; \
		exit 1; \
	fi
	@echo "$(GREEN)[SUCCESS]$(NC) Prerequisites check passed!"
	@echo "$(BLUE)[INFO]$(NC) Setting up environment..."
	@$(MAKE) setup-env
	@echo "$(BLUE)[INFO]$(NC) Setting up permissions..."
	@$(MAKE) setup-permissions
	@echo "$(BLUE)[INFO]$(NC) Building services..."
	@$(MAKE) build
	@echo "$(GREEN)[SUCCESS]$(NC) Web Scraper setup completed!"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "1. Start development environment: $(GREEN)make dev$(NC)"
	@echo "2. Access Frontend at: $(GREEN)http://localhost:3000$(NC)"
	@echo "3. Access Backend at: $(GREEN)http://localhost:18000$(NC)"

.PHONY: setup-env
setup-env: ## Setup environment variables
	@echo "$(BLUE)[INFO]$(NC) Setting up environment variables..."
	@if [ ! -f .env ]; then \
		echo "$(BLUE)[INFO]$(NC) Creating .env file from template..."; \
		cp env.example .env; \
		echo "$(GREEN)[SUCCESS]$(NC) .env file created"; \
	else \
		echo "$(BLUE)[INFO]$(NC) .env file already exists"; \
	fi

# =============================================================================
# UTILITY COMMANDS
# =============================================================================

.PHONY: check-docker
check-docker: ## Check if Docker is running
	@if ! docker info > /dev/null 2>&1; then \
		echo "$(RED)[ERROR]$(NC) Docker is not running"; \
		echo "$(BLUE)[INFO]$(NC) Please start Docker and try again"; \
		exit 1; \
	fi
	@echo "$(GREEN)[SUCCESS]$(NC) Docker is running"

.PHONY: shell
shell: ## Open shell in backend container
	@echo "$(BLUE)[INFO]$(NC) Opening shell in backend container..."
	@$(DOCKER_COMPOSE) exec backend /bin/bash

.PHONY: shell-frontend
shell-frontend: ## Open shell in frontend container
	@echo "$(BLUE)[INFO]$(NC) Opening shell in frontend container..."
	@$(DOCKER_COMPOSE) exec frontend /bin/bash

# =============================================================================
# DEVELOPMENT WORKFLOW
# =============================================================================

.PHONY: dev-full
dev-full: ## Full development workflow (setup + dev)
	@echo "$(BLUE)[INFO]$(NC) Starting full development workflow..."
	@$(MAKE) setup
	@$(MAKE) dev

.PHONY: reset
reset: ## Reset everything and start fresh
	@echo "$(BLUE)[INFO]$(NC) Resetting everything..."
	@$(MAKE) clean
	@$(MAKE) setup
	@$(MAKE) dev

# =============================================================================
# MONITORING
# =============================================================================

.PHONY: monitor
monitor: ## Monitor all services and logs
	@echo "$(BLUE)[INFO]$(NC) Starting monitoring..."
	@echo "$(BLUE)[INFO]$(NC) Service Status:"
	@$(MAKE) status
	@echo ""
	@echo "$(BLUE)[INFO]$(NC) Health Check:"
	@$(MAKE) health
	@echo ""
	@echo "$(BLUE)[INFO]$(NC) Recent Logs:"
	@$(DOCKER_COMPOSE) logs --tail=20 