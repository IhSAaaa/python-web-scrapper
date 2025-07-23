# 🌐 Web Scraper - Vue 3 + FastAPI

A modern web-based scraping application built with Vue 3, Tailwind CSS, and FastAPI. This project has been migrated from a desktop GUI application to a modern web application.

## ✨ Features

- **Modern Web Interface**: Beautiful, responsive UI built with Vue 3 and Tailwind CSS with glassmorphism design
- **Web Scraping**: Extract links and images from any website
- **Authentication Support**: Login to protected websites with credentials
- **File Downloads**: Download scraped data as CSV files and images as ZIP
- **Image Processing**: Automatic SVG to PNG conversion and image validation
- **Real-time Feedback**: Live progress indicators and error handling
- **Session Management**: Unique session IDs for each scraping job with 24-hour retention
- **Smart Cleanup System**: Intelligent cleanup with user-friendly retention periods
- **Environment Configuration**: Flexible environment variables for different deployments
- **Docker Support**: Complete containerization for easy deployment

## 🏗️ Architecture

```
├── backend/                 # FastAPI backend
│   └── main.py             # Main API server
├── frontend/               # Vue 3 frontend
│   ├── src/
│   │   ├── App.vue         # Main application component
│   │   ├── main.js         # Vue app entry point
│   │   └── style.css       # Tailwind CSS styles
│   ├── package.json        # Frontend dependencies
│   └── vite.config.js      # Vite configuration
├── output/                 # Scraped files storage
├── requirements.txt        # Python dependencies
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

## 📖 Usage

1. **Open the application** in your browser at `http://localhost:3000`

2. **Enter the target URL** you want to scrape

3. **Optional: Enable login** if the website requires authentication
   - Enter the login URL
   - Provide username and password

4. **Click "Start Scraping"** to begin the process

5. **View results** and download files:
   - **CSV file**: All extracted links with metadata (URL, text, title, target, rel)
   - **Images ZIP**: All downloaded images in a compressed archive
   - **Session Info**: Session ID and expiration time (24 hours)

6. **Multiple Downloads**: Files remain available for 24 hours, allowing multiple downloads

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - Health check
- `POST /api/scrape` - Main scraping endpoint
- `GET /api/download/{session_id}/{filename}` - Download individual files
- `GET /api/images/{session_id}` - Download images as ZIP
- `GET /api/health` - API health status

### Session Management
- `GET /api/session/{session_id}/status` - Get session status and info
- `GET /api/files/{session_id}` - List files in session
- `GET /api/images/{session_id}/info` - Get images information

### Maintenance
- `POST /api/maintenance/cleanup/{session_id}` - Clean specific session
- `POST /api/maintenance/cleanup` - Clean old sessions
- `POST /api/maintenance/cleanup-all` - Clean all sessions
- `GET /api/maintenance/stats` - Get cleanup statistics

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework
- **BeautifulSoup4**: HTML parsing
- **Requests**: HTTP client
- **Pandas**: Data manipulation
- **CairoSVG**: SVG to PNG conversion
- **Pydantic**: Data validation

### Frontend
- **Vue 3**: Progressive JavaScript framework
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **Vite**: Build tool and dev server

## 📁 Project Structure

```
python-web-scrapper/
├── backend/
│   ├── main.py                # FastAPI application
│   └── logger_config.py       # Logging configuration
├── frontend/
│   ├── src/
│   │   ├── App.vue           # Main Vue component
│   │   ├── main.js           # App entry point
│   │   └── style.css         # Global styles
│   ├── index.html            # HTML template
│   ├── package.json          # Dependencies
│   ├── vite.config.js        # Vite config
│   ├── tailwind.config.js    # Tailwind config
│   ├── postcss.config.js     # PostCSS config
│   ├── env.development       # Development environment
│   ├── env.production        # Production environment
│   ├── setup-env.sh          # Environment setup script
│   ├── ENVIRONMENT.md        # Environment documentation
│   └── URL_HANDLING.md       # URL handling documentation
├── output/                   # Scraped files storage
├── tests/                    # Test files
├── docker-compose.yml        # Docker Compose configuration
├── docker-compose.prod.yml   # Production Docker Compose
├── Dockerfile.backend        # Backend Dockerfile
├── Dockerfile.frontend       # Frontend Dockerfile
├── requirements.txt          # Python dependencies
├── CLEANUP_IMPROVEMENTS.md   # Cleanup system documentation
├── DOCKER_GUIDE.md          # Docker deployment guide
└── README.md                # This documentation
```

## 🔒 Security Features

- CORS configuration for secure cross-origin requests
- Input validation with Pydantic models
- Error handling and logging
- Session-based file storage

## 🧹 Smart Cleanup System

The application includes an intelligent cleanup system that balances disk space management with user experience:

### Features
- **24-hour retention**: Files remain available for 24 hours after scraping
- **Multiple downloads**: Users can download files multiple times
- **Scheduled cleanup**: Old sessions are cleaned up automatically
- **Manual cleanup**: Admin tools for manual cleanup operations
- **Session tracking**: Real-time session status and expiration info

### Configuration
Current settings in `backend/main.py`:
```python
AUTO_CLEANUP_ENABLED = True          # Enable auto-cleanup for old sessions
CLEANUP_AFTER_DOWNLOAD = False       # Don't delete after download (user-friendly)
DEFAULT_CLEANUP_HOURS = 24          # 24-hour retention period
```

### Usage
```bash
# Check cleanup stats
./cleanup_manual.sh stats

# List current sessions
./cleanup_manual.sh list

# Clean up old sessions
./cleanup_manual.sh old 24

# Clean up all sessions
./cleanup_manual.sh all
```

For detailed cleanup documentation, see [CLEANUP_IMPROVEMENTS.md](CLEANUP_IMPROVEMENTS.md).

## 🚀 Deployment

### Docker Deployment (Recommended)

**Development:**
```bash
# Start development environment
docker compose up -d --build

# View logs
docker compose logs -f

# Stop containers
docker compose down
```

**Production:**
```bash
# Start production environment
docker compose -f docker-compose.prod.yml up -d --build

# View production logs
docker compose -f docker-compose.prod.yml logs -f
```

### Local Deployment

**Backend:**
```bash
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run setup:env  # Setup environment variables
npm run build
npm run preview
```

### Environment Configuration

The application uses environment variables for configuration:

**Frontend Environment:**
```bash
# Development
VITE_API_BASE_URL=http://localhost:8001
VITE_APP_TITLE=Web Scraper (Development)

# Production
VITE_API_BASE_URL=https://api.example.com
VITE_APP_TITLE=Web Scraper
```

For detailed environment setup, see [frontend/ENVIRONMENT.md](frontend/ENVIRONMENT.md).

## 🧪 Testing

The project includes comprehensive testing:

### Backend Tests
```bash
# Run all tests
./run_tests.sh

# Run specific test files
python -m pytest tests/test_csv_download.py
python -m pytest tests/test_images_download.py
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Manual Testing
```bash
# Test scraping without authentication
curl -X POST http://localhost:8001/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Test session status
curl http://localhost:8001/api/session/{session_id}/status
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📚 Documentation

This project includes comprehensive documentation:

- **[CLEANUP_IMPROVEMENTS.md](CLEANUP_IMPROVEMENTS.md)** - Smart cleanup system documentation
- **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Docker deployment guide
- **[frontend/ENVIRONMENT.md](frontend/ENVIRONMENT.md)** - Environment variables configuration
- **[frontend/URL_HANDLING.md](frontend/URL_HANDLING.md)** - URL handling for downloads
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide
- **[SUMMARY.md](SUMMARY.md)** - Project summary and features

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🔄 Recent Improvements

### Version 2.0 Updates
- **Smart Cleanup System**: 24-hour file retention with multiple downloads
- **Environment Configuration**: Flexible environment variables for different deployments
- **Enhanced UI**: Glassmorphism design with better user experience
- **Session Management**: Real-time session tracking and status
- **Docker Optimization**: Improved containerization and health checks
- **URL Handling**: Proper backend domain routing for downloads
- **Comprehensive Testing**: Automated and manual testing suites

### Migration Notes

This project was migrated from a PySimpleGUI desktop application to a modern web application. The core scraping functionality remains the same, but now provides:

- **Better UX**: Modern, responsive web interface with glassmorphism design
- **Scalability**: API-based architecture with Docker support
- **Accessibility**: Web-based access from any device
- **Maintainability**: Modern development practices and comprehensive documentation
- **Extensibility**: Easy to add new features with modular architecture

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the backend CORS settings match your frontend URL
2. **Port Conflicts**: Check if ports 3000 and 8001 are available
3. **Dependencies**: Make sure all Python and Node.js dependencies are installed
4. **File Permissions**: Ensure the `output` directory is writable
5. **Environment Variables**: Check if frontend environment is properly configured
6. **Docker Health Checks**: Ensure containers are healthy before accessing

### Logs

- **Backend logs**: `docker compose logs backend`
- **Frontend logs**: `docker compose logs frontend`
- **Browser console**: Check for JavaScript errors
- **API errors**: Displayed in the UI with detailed messages

### Health Checks

```bash
# Check backend health
curl http://localhost:8001/api/health

# Check frontend
curl http://localhost:3000

# Check session status
curl http://localhost:8001/api/session/{session_id}/status
```
