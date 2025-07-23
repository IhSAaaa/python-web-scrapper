# URL Handling for Downloads

## Overview
This document explains how the frontend handles URLs for downloading files from the backend API.

## Problem
Previously, the frontend was using relative URLs returned by the backend (e.g., `/api/download/{session_id}/{filename}`) directly, which would cause downloads to hit the frontend domain instead of the backend domain.

## Solution
The frontend now uses a `getFullUrl()` function that converts relative URLs to absolute URLs pointing to the backend.

## Implementation

### `getFullUrl()` Function
```javascript
const getFullUrl = (relativeUrl) => {
  if (!relativeUrl) return ''
  
  // If URL is already absolute, return as is
  if (relativeUrl.startsWith('http://') || relativeUrl.startsWith('https://')) {
    return relativeUrl
  }
  
  // If URL starts with /, it's a relative URL from backend
  if (relativeUrl.startsWith('/')) {
    const fullUrl = `${API_BASE_URL}${relativeUrl}`
    console.log(`Converting relative URL: ${relativeUrl} -> ${fullUrl}`)
    return fullUrl
  }
  
  // Otherwise, assume it's relative to current domain
  return relativeUrl
}
```

### Usage in Template
```vue
<!-- CSV Download -->
<a :href="getFullUrl(results.excel_file)" download>
  Download CSV
</a>

<!-- Images Download -->
<a :href="getFullUrl(results.images_folder)" target="_blank">
  Download Images
</a>
```

## URL Conversion Examples

### Development Environment
- **Backend URL**: `http://localhost:8001`
- **Relative URL**: `/api/download/abc123/links.csv`
- **Full URL**: `http://localhost:8001/api/download/abc123/links.csv`

### Production Environment
- **Backend URL**: `https://api.example.com`
- **Relative URL**: `/api/images/abc123`
- **Full URL**: `https://api.example.com/api/images/abc123`

## Backend Response Format
The backend returns relative URLs in the scraping response:

```json
{
  "success": true,
  "message": "Scraping completed successfully!",
  "links_count": 25,
  "images_count": 10,
  "excel_file": "/api/download/abc123/links.csv",
  "images_folder": "/api/images/abc123"
}
```

## Environment Configuration
The `API_BASE_URL` is configured through environment variables:

- **Development**: `VITE_API_BASE_URL=http://localhost:8001`
- **Production**: `VITE_API_BASE_URL=https://api.example.com`

## Debugging
The function logs URL conversions to the console for debugging:

```
Converting relative URL: /api/download/abc123/links.csv -> http://localhost:8001/api/download/abc123/links.csv
Converting relative URL: /api/images/abc123 -> http://localhost:8001/api/images/abc123
```

## Benefits
1. **✅ Correct Domain**: Downloads now hit the backend domain
2. **✅ Environment Flexible**: Works in development and production
3. **✅ Backward Compatible**: Handles both relative and absolute URLs
4. **✅ Debuggable**: Logs URL conversions for troubleshooting
5. **✅ Secure**: Uses environment variables for configuration 