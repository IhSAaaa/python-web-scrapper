# 🚀 Quick Start Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

## Option 1: Using Make (Recommended)

```bash
# Install dependencies and start development servers
make dev
```

## Option 2: Using Start Script

```bash
# Make script executable
chmod +x start.sh

# Run the application
./start.sh
```

## Option 3: Manual Setup

### Backend
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server
cd backend
python main.py
```

### Frontend
```bash
# Install Node.js dependencies
cd frontend
npm install

# Start development server
npm run dev
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

## Usage

1. Open http://localhost:3000 in your browser
2. Enter a URL to scrape (e.g., https://example.com)
3. Optionally enable login if the site requires authentication
4. Click "Start Scraping"
5. Download the results (Excel file and images)

## Testing

```bash
# Run tests
./run_tests.sh

# Or using make
make test
```

## Docker (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Stop containers
docker-compose down
```

## Troubleshooting

### Port Already in Use
- Backend: Change port in `backend/main.py`
- Frontend: Change port in `frontend/vite.config.js`

### Dependencies Issues
```bash
# Clean and reinstall
make clean
make install
```

### CORS Errors
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [API documentation](http://localhost:8001/docs) when running
- Explore the code structure in `backend/` and `frontend/` directories 