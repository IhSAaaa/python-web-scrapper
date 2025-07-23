# 🐳 Docker Guide - Web Scraper

## Overview

This project is now fully containerized with Docker, eliminating the need for local Python or Node.js dependencies.

## 🚀 Quick Start with Docker

### Prerequisites
- Docker
- Docker Compose

### Development Mode
```bash
# Start development environment
chmod +x docker-start.sh
./docker-start.sh
```

### Production Mode
```bash
# Start production environment
chmod +x docker-prod.sh
./docker-prod.sh
```

## 📁 Docker Files Structure

```
├── Dockerfile.backend              # Development backend
├── Dockerfile.backend.prod         # Production backend
├── frontend/Dockerfile.frontend    # Development frontend
├── frontend/Dockerfile.frontend.prod # Production frontend
├── docker-compose.yml              # Development compose
├── docker-compose.prod.yml         # Production compose
├── docker-start.sh                 # Development start script
├── docker-prod.sh                  # Production start script
├── .dockerignore                   # Backend build exclusions
└── frontend/.dockerignore          # Frontend build exclusions
```

## 🔧 Docker Commands

### Development Commands
```bash
# Build and start development containers
make docker-run

# View logs
make docker-logs

# Stop containers
make docker-stop

# Clean up
make docker-clean
```

### Production Commands
```bash
# Build and start production containers
make docker-prod

# Stop production containers
make docker-prod-stop

# View production logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Manual Docker Commands
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v
```

## 🌐 Access Points

### Development Mode
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

### Production Mode
- **Frontend**: http://localhost (port 80)
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

## 🔍 Container Details

### Backend Container
- **Base Image**: Python 3.11-slim
- **Dependencies**: CairoSVG, BeautifulSoup4, FastAPI, etc.
- **Security**: Non-root user (scraper:1000)
- **Health Check**: `/api/health` endpoint
- **Port**: 8000

### Frontend Container (Development)
- **Base Image**: Node.js 18-alpine
- **Dependencies**: Vue 3, Tailwind CSS, Vite
- **Security**: Non-root user (vuejs:1001)
- **Health Check**: Port 3000 availability
- **Port**: 3000

### Frontend Container (Production)
- **Base Image**: Nginx alpine
- **Build**: Multi-stage build with Node.js
- **Security**: Non-root user (nginx:1001)
- **Features**: Gzip compression, security headers
- **Port**: 80

## 📊 Volume Mounts

### Development
```yaml
volumes:
  - ./output:/app/output  # Shared output directory
```

### Production
```yaml
volumes:
  - ./output:/app/output  # Shared output directory
```

## 🔒 Security Features

### Backend Security
- Non-root user execution
- Minimal base image (slim)
- Health checks
- Input validation
- CORS configuration

### Frontend Security
- Non-root user execution
- Security headers (XSS, CSRF protection)
- Content Security Policy
- Nginx security configuration

## 🚀 Performance Optimizations

### Development
- Hot reload for frontend
- FastAPI auto-reload
- Shared volumes for development

### Production
- Multi-stage builds
- Nginx for static file serving
- Gzip compression
- Optimized Docker layers
- Health checks for reliability

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Check what's using the port
lsof -i :3000
lsof -i :8001

# Stop conflicting services
sudo systemctl stop nginx  # if needed
```

**Container Won't Start**
```bash
# Check logs
docker-compose logs

# Check container status
docker-compose ps

# Rebuild containers
docker-compose build --no-cache
```

**Permission Issues**
```bash
# Fix output directory permissions
sudo chown -R $USER:$USER output/
chmod 755 output/
```

**Docker Daemon Issues**
```bash
# Start Docker daemon
sudo systemctl start docker

# Check Docker status
sudo systemctl status docker
```

### Debug Commands
```bash
# Enter running container
docker-compose exec backend bash
docker-compose exec frontend sh

# View container resources
docker stats

# Check container logs
docker-compose logs backend
docker-compose logs frontend

# Inspect container
docker-compose exec backend python -c "import sys; print(sys.path)"
```

## 🔄 Environment Variables

### Backend Environment
```bash
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
PYTHONPATH=/app
LOG_LEVEL=INFO
```

### Frontend Environment
```bash
VITE_API_URL=http://localhost:8001
VITE_APP_TITLE=Web Scraper
```

## 📈 Monitoring

### Health Checks
- Backend: `curl http://localhost:8001/api/health`
- Frontend: `curl http://localhost:3000` (dev) or `curl http://localhost` (prod)

### Logs
```bash
# Follow all logs
docker-compose logs -f

# Follow specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Production logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🎯 Best Practices

1. **Always use Docker for deployment**
2. **Use production images for production**
3. **Monitor container health**
4. **Regularly update base images**
5. **Use volume mounts for persistent data**
6. **Implement proper logging**
7. **Use health checks**
8. **Run as non-root users**

## 🚀 Next Steps

1. **Deploy to cloud platform** (AWS, GCP, Azure)
2. **Set up CI/CD pipeline**
3. **Add monitoring and alerting**
4. **Implement backup strategies**
5. **Scale horizontally with load balancer** 