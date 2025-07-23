# 🌐 Web Scraper - Vue 3 + FastAPI

A modern, high-performance web-based scraping application built with Vue 3, Tailwind CSS, and FastAPI. This project has been migrated from a desktop GUI application to a modern web application with optimized performance.

## ✨ Features

- **🚀 High-Performance Scraping**: Optimized concurrent downloads with ThreadPoolExecutor
- **⚡ Fast Processing**: Reduced scraping time from 4+ minutes to ~30 seconds
- **🎨 Modern Web Interface**: Beautiful, responsive UI built with Vue 3 and Tailwind CSS with glassmorphism design
- **🔗 Web Scraping**: Extract links and images from any website
- **📁 File Downloads**: Download scraped data as CSV files and images as ZIP
- **🖼️ Image Processing**: Automatic SVG to PNG conversion and image validation
- **📊 Real-time Feedback**: Live progress indicators and error handling
- **🆔 Session Management**: Unique session IDs for each scraping job with 24-hour retention
- **🧹 Smart Cleanup System**: Intelligent cleanup with user-friendly retention periods
- **⚙️ Environment Configuration**: Flexible environment variables for different deployments
- **🐳 Docker Support**: Complete containerization for easy deployment
- **🧪 Comprehensive Testing**: 20 test cases with 100% pass rate

## 🏗️ Architecture

```
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API server with performance optimizations
│   └── logger_config.py    # Custom logging configuration
├── frontend/               # Vue 3 frontend
│   ├── src/
│   │   ├── App.vue         # Main application component
│   │   ├── main.js         # Vue app entry point
│   │   └── style.css       # Tailwind CSS styles
│   ├── package.json        # Frontend dependencies
│   └── vite.config.js      # Vite configuration
├── tests/                  # Comprehensive test suite
│   ├── test_scraper.py     # Core scraping tests
│   ├── test_csv_download.py # CSV download tests
│   ├── test_images_download.py # Image download tests
│   ├── test_cleanup.py     # Cleanup functionality tests
│   └── test_improvements.py # Performance and feature tests
├── output/                 # Scraped files storage
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Development Docker configuration
├── docker-compose.prod.yml # Production Docker configuration
├── Makefile               # Development commands
└── README.md              # This file
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker
- Docker Compose

**Development Mode:**
```bash
# Start with Docker Compose
docker compose up -d --build

# View logs
docker compose logs -f

# Run tests
make test-docker

# Stop containers
docker compose down
```

**Production Mode:**
```bash
# Start production environment
docker compose -f docker-compose.prod.yml up -d --build
```

### Option 2: Local Development

**Prerequisites:**
- Python 3.11+
- Node.js 18+
- npm or yarn

**Backend Setup:**
```bash
pip install -r requirements.txt
cd backend
python main.py
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm run setup:env  # Setup environment variables
npm run dev
```

**Run Tests:**
```bash
# Run tests locally
make test-local

# Run tests in Docker
make test-docker
```

## 📖 Usage

1. **Open the application** in your browser at `http://localhost:3000`

2. **Enter the target URL** you want to scrape

3. **Click "Start Scraping"** to begin the process
   - **Fast Processing**: Optimized concurrent downloads for quick results
   - **Real-time Progress**: Live feedback during scraping process

4. **View results** and download files:
   - **CSV file**: All extracted links with metadata (URL, text, title, target, rel)
   - **Images ZIP**: All downloaded images in a compressed archive
   - **Session Info**: Session ID and expiration time (24 hours)

5. **Multiple Downloads**: Files remain available for 24 hours, allowing multiple downloads

## �� API Endpoints

### Core Endpoints
- `POST /api/scrape` - Start scraping a website
- `GET /api/download/{session_id}/{filename}` - Download scraped files
- `GET /api/files/{session_id}` - List session files
- `GET /api/csv/{session_id}` - Download CSV file directly
- `GET /api/images/{session_id}` - Download images as ZIP
- `GET /api/images/{session_id}/info` - Get images information

### Health & Monitoring
- `GET /api/health` - Health check with system metrics
- `GET /api/debug/last-session` - Get last session information
- `GET /api/debug/logs` - View application logs
- `GET /api/maintenance/stats` - System maintenance statistics

### Maintenance
- `POST /api/maintenance/cleanup` - Clean up old sessions
- `POST /api/maintenance/cleanup/{session_id}` - Clean specific session
- `POST /api/maintenance/cleanup-all` - Clean all sessions

## 🧪 Testing

The project includes a comprehensive test suite with 20 test cases:

```bash
# Run all tests
make test-docker

# Test results:
# ✅ 20 passed in 30.68s
# - Core scraping functionality
# - CSV download and processing
# - Image download and ZIP creation
# - Cleanup and maintenance features
# - Health checks and monitoring
```

## ⚡ Performance Optimizations

### Recent Improvements (v2.0)
- **🚀 Concurrent Downloads**: ThreadPoolExecutor for parallel image downloads
- **⚡ Faster Rate Limiting**: Reduced from 1-3s to 0.1-0.5s delays
- **📦 Larger Chunks**: Increased chunk size from 8KB to 32KB
- **⏱️ Aggressive Timeouts**: Reduced timeout from 15s to 10s
- **🔄 Optimized Retries**: Reduced from 3 to 2 retry attempts
- **🧠 Memory Management**: Improved garbage collection and cleanup

### Performance Metrics
- **Scraping Time**: Reduced from 267s to ~30s (89% improvement)
- **Concurrent Downloads**: Up to 10 simultaneous image downloads
- **Memory Usage**: Optimized with automatic cleanup
- **Error Handling**: Faster failure detection and recovery

## 🔧 Configuration

### Environment Variables

**Backend:**
```bash
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8001
LOG_LEVEL=INFO
```

**Frontend:**
```bash
VITE_API_BASE_URL=http://localhost:8001
NODE_ENV=development
```

### Performance Settings
```python
MAX_CONCURRENT_DOWNLOADS = 10    # Concurrent image downloads
CHUNK_SIZE = 32768               # Download chunk size
TIMEOUT = 10                     # Request timeout
RATE_LIMIT_DELAY = (0.1, 0.5)   # Rate limiting delay
```

## 🐳 Docker Configuration

### Development
- **Backend**: Python 3.11 with FastAPI
- **Frontend**: Node.js 18 with Vue 3
- **Test**: Dedicated test container with pytest
- **Networks**: Isolated Docker network
- **Volumes**: Persistent storage for scraped files

### Production
- **Optimized Images**: Multi-stage builds
- **Security**: Non-root users
- **Health Checks**: Automated health monitoring
- **Logging**: Structured logging with rotation

## 📊 Monitoring & Logging

### Health Checks
- **System Metrics**: CPU, memory, disk usage
- **API Status**: Endpoint availability
- **Session Management**: Active sessions count
- **File Storage**: Storage usage and cleanup status

### Logging
- **Structured Logs**: JSON format for easy parsing
- **Log Rotation**: Automatic log file management
- **Error Tracking**: Detailed error context and stack traces
- **Activity Monitoring**: Scraping activity and performance metrics

## 🔒 Security Features

- **Input Validation**: URL validation and sanitization
- **File Size Limits**: Maximum image size restrictions
- **Content Type Validation**: Image format verification
- **Session Isolation**: Separate storage for each session
- **Automatic Cleanup**: Secure file deletion after expiration

## 🛠️ Development Commands

```bash
# Start development environment
make dev

# Run tests
make test-docker

# Build production images
make build-prod

# View logs
make logs

# Clean up
make clean
```

## 📈 Project Status

- ✅ **All Tests Passing**: 20/20 test cases
- ✅ **Performance Optimized**: 89% improvement in scraping speed
- ✅ **Docker Ready**: Complete containerization
- ✅ **Production Ready**: Optimized for production deployment
- ✅ **Well Documented**: Comprehensive documentation
- ✅ **Maintained**: Active development and improvements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
