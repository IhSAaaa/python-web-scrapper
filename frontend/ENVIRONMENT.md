# Environment Variables Configuration

## Overview
This frontend application uses environment variables to configure API endpoints and other settings.

## Environment Files

### Development Environment (`env.development`)
```bash
VITE_API_BASE_URL=http://localhost:8001
VITE_APP_TITLE=Web Scraper (Development)
VITE_APP_VERSION=1.0.0
```

### Production Environment (`env.production`)
```bash
VITE_API_BASE_URL=http://localhost:8001
VITE_APP_TITLE=Web Scraper
VITE_APP_VERSION=1.0.0
```

## Variables

### `VITE_API_BASE_URL`
- **Description**: Base URL for the backend API
- **Default**: `http://localhost:8001`
- **Usage**: Used by axios to make API calls to the backend

### `VITE_APP_TITLE`
- **Description**: Application title displayed in the UI
- **Default**: `Web Scraper`

### `VITE_APP_VERSION`
- **Description**: Application version
- **Default**: `1.0.0`

## Docker Configuration

When running in Docker, environment variables can be set in `docker-compose.yml`:

```yaml
frontend:
  environment:
    - VITE_API_BASE_URL=http://localhost:8001
    - NODE_ENV=development
```

## Local Development

For local development, create a `.env.local` file in the frontend directory:

```bash
VITE_API_BASE_URL=http://localhost:8001
VITE_APP_TITLE=Web Scraper (Local)
VITE_APP_VERSION=1.0.0
```

## Fallback Logic

The application includes fallback logic for API base URL:

1. **Environment Variable**: Uses `VITE_API_BASE_URL` if set
2. **Local Development**: Uses `http://localhost:8001` for localhost
3. **Default**: Falls back to `/api` for production deployments

## Debugging

The application logs the configured API base URL and environment mode to the console for debugging purposes. 