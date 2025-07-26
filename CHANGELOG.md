# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Async/Await implementation for image downloads
- Connection pooling for better resource management
- Redis-based caching system
- Advanced scraping options with custom selectors

## [v2.1.0] - 2025-07-26

### 🐛 Fixed
- **API Path Redundancy**: Fixed critical `/api/api/` issue in production environment
  - Updated nginx proxy configuration to preserve `/api` prefix
  - Standardized environment variable `VITE_API_BASE_URL` configuration
  - Simplified frontend API endpoint handling for consistency
- **Production Deployment**: Resolved 404 errors for API endpoints
- **Environment Configuration**: Fixed inconsistent API base URL settings

### ✨ Added
- **Troubleshooting Commands**: 
  - `make test-api-config` for automated API configuration testing
  - Enhanced debugging tools for production deployment
- **Build Improvements**: 
  - Enhanced production build with correct environment variables
  - Added build arguments support in Dockerfile
- **Documentation**: 
  - Comprehensive troubleshooting guide
  - API configuration best practices
  - Deployment debugging commands

### 🔧 Changed
- **Frontend API Logic**: 
  - Simplified endpoint handling for consistency
  - Removed conditional logic that caused confusion
- **Production Configuration**: 
  - Updated nginx configuration to preserve `/api` prefix
  - Modified docker-compose.prod.yml environment variables
- **Build Process**: 
  - Improved Dockerfile with build arguments
  - Enhanced Makefile with production-specific commands

### 📚 Documentation
- **Troubleshooting Guide**: Added common issues and solutions
- **API Configuration**: Updated best practices for development and production
- **Deployment Guide**: Enhanced with debugging and testing commands
- **README Updates**: Comprehensive project status and changelog

### 🔍 Technical Details
- **Nginx Proxy**: Changed from `proxy_pass http://backend:8000/` to `proxy_pass http://backend:8000/api/`
- **Environment Variables**: Standardized `VITE_API_BASE_URL` usage across environments
- **Frontend Logic**: Simplified axios endpoint configuration
- **Build Arguments**: Added `ARG VITE_API_BASE_URL=` in Dockerfile

## [v2.0.0] - 2025-07-24

### 🚀 Performance Improvements
- **Concurrent Downloads**: Implemented ThreadPoolExecutor for parallel image downloads
- **Faster Rate Limiting**: Reduced delays from 1-3s to 0.1-0.5s
- **Larger Chunks**: Increased download chunk size from 8KB to 32KB
- **Aggressive Timeouts**: Reduced timeout from 15s to 10s for faster failure detection
- **Optimized Retries**: Reduced retry attempts from 3 to 2
- **Memory Management**: Improved garbage collection and cleanup

### ✨ New Features
- **Modern Web Interface**: Vue 3 with Tailwind CSS and glassmorphism design
- **Session Management**: Unique session IDs with 24-hour retention
- **Smart Cleanup System**: Intelligent cleanup with user-friendly retention periods
- **Comprehensive Testing**: 20 test cases with 100% pass rate
- **Health Monitoring**: Automated health checks and system metrics

### 🔧 Technical Improvements
- **Docker Support**: Complete containerization for easy deployment
- **Structured Logging**: JSON format with rotation and error tracking
- **Security Enhancements**: Non-root users and proper permissions
- **Error Handling**: Faster failure detection and recovery
- **File Management**: Optimized file operations and storage

### 📊 Performance Metrics
- **Scraping Time**: Reduced from 267s to ~30s (89% improvement)
- **Concurrent Downloads**: Up to 10 simultaneous image downloads
- **Memory Usage**: Optimized with automatic cleanup
- **Error Recovery**: Faster failure detection and recovery

## [v1.0.0] - 2025-07-20

### 🎉 Initial Release
- **Web Scraping**: Extract links and images from websites
- **File Downloads**: CSV files and images as ZIP
- **Image Processing**: SVG to PNG conversion
- **Basic UI**: Simple web interface
- **Core Functionality**: Basic scraping and file management

---

## Migration Guide

### From v2.0.0 to v2.1.0
1. **Environment Variables**: Update `VITE_API_BASE_URL` in production to empty string
2. **Nginx Configuration**: Ensure nginx proxy preserves `/api` prefix
3. **Frontend Build**: Rebuild frontend with new configuration
4. **Testing**: Run `make test-api-config` to verify setup

### From v1.0.0 to v2.0.0
1. **Docker Setup**: Use new docker-compose files
2. **Environment**: Set up proper environment variables
3. **Permissions**: Run `make setup-permissions`
4. **Testing**: Execute `make test` to verify functionality

---

## Breaking Changes

### v2.1.0
- **API Endpoints**: All endpoints now consistently use `/api` prefix
- **Environment Variables**: `VITE_API_BASE_URL` behavior changed in production

### v2.0.0
- **Architecture**: Complete rewrite from desktop to web application
- **API Structure**: New RESTful API design
- **File Storage**: Changed from local files to session-based storage

---

## Contributors

- **Development Team**: Core development and architecture
- **Testing Team**: Comprehensive test suite implementation
- **DevOps**: Docker and deployment configuration
- **Documentation**: README and changelog maintenance 