from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64
import cairosvg
import uuid
from datetime import datetime
from typing import Optional
import aiofiles
from pydantic import BaseModel
import time
import random
import gc
from urllib.parse import urlparse
import mimetypes
import zipfile
import tempfile
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import custom logging
import sys
import os

# Add current directory to Python path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from logger_config import setup_logger, get_logger, log_scraping_activity, log_request_details, log_scraping_session, log_error_with_context
    
    # Setup logging
    setup_logger()
    logger = get_logger()
    logger.info("=== WEB SCRAPER BACKEND STARTING ===")
    
except ImportError as e:
    # Fallback to basic logging if custom logger fails
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('backend_fallback.log', encoding='utf-8')
        ]
    )
    logger = logging.getLogger(__name__)
    logger.warning(f"Using fallback logging system. Import error: {e}")
    
    # Create fallback functions
    def log_scraping_activity(message, level='info'):
        logger.info(f"[SCRAPING] {message}")
    
    def log_request_details(url, method, status_code, duration=None):
        logger.info(f"[HTTP] {method} {url} | Status: {status_code}")
    
    def log_scraping_session(session_id, url, links_count, images_count, success=True):
        logger.info(f"[SESSION] ID: {session_id} | URL: {url} | Links: {links_count} | Images: {images_count}")
    
    def log_error_with_context(error, context=""):
        logger.error(f"[ERROR] {str(error)} | Context: {context}")

# Configuration constants (defined before lifespan to avoid reference errors)
MAX_RETRIES = 2  # Reduced retries
RETRY_DELAY = 1  # seconds - reduced delay
RATE_LIMIT_DELAY = (0.1, 0.5)  # random delay between 0.1-0.5 seconds - much faster
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
VALID_IMAGE_TYPES = ['jpeg', 'jpg', 'png', 'gif', 'webp', 'svg']
# Performance optimization settings
MAX_CONCURRENT_DOWNLOADS = 10  # Limit concurrent image downloads
CHUNK_SIZE = 32768  # Increased chunk size for faster downloads
TIMEOUT = 10  # Reduced timeout for faster failure detection

# Cleanup configuration
AUTO_CLEANUP_ENABLED = True  # Enable auto-cleanup for old sessions
CLEANUP_AFTER_DOWNLOAD = False  # Don't delete session folder after file download (let user download multiple times)
DEFAULT_CLEANUP_HOURS = 24  # Default hours for cleanup (24 hours = more user-friendly)
AUTO_CLEANUP_INTERVAL = 3600  # Auto-cleanup interval in seconds (1 hour)

# Create output directory with proper permission handling
OUTPUT_DIR = "output"

def ensure_output_directory():
    """Ensure output directory exists with proper permissions"""
    try:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            logger.info(f"Created output directory: {OUTPUT_DIR}")
        
        # Check if we can write to the directory
        if not os.access(OUTPUT_DIR, os.W_OK):
            logger.error(f"Permission denied: Cannot write to output directory: {OUTPUT_DIR}")
            return False
        
        logger.info(f"Output directory ready: {OUTPUT_DIR}")
        return True
    except Exception as e:
        logger.error(f"Error setting up output directory: {str(e)}")
        return False

# Initialize output directory
if not ensure_output_directory():
    logger.error("Failed to initialize output directory. Application may not work properly.")

def cleanup_session_folder(session_id: str, reason: str = "manual"):
    """Clean up a specific session folder"""
    try:
        import shutil
        session_path = os.path.join(OUTPUT_DIR, session_id)
        
        if os.path.exists(session_path) and os.path.isdir(session_path):
            # Calculate size before deletion
            dir_size = sum(
                os.path.getsize(os.path.join(dirpath, filename))
                for dirpath, dirnames, filenames in os.walk(session_path)
                for filename in filenames
            )
            
            # Remove directory
            shutil.rmtree(session_path)
            
            logger.info(f"Cleaned up session folder: {session_id} | Reason: {reason} | Size: {dir_size} bytes")
            return True, dir_size
        else:
            logger.warning(f"Session folder not found for cleanup: {session_id}")
            return False, 0
    except Exception as e:
        logger.error(f"Error cleaning up session {session_id}: {str(e)}")
        return False, 0

def auto_cleanup_old_sessions(hours: int = DEFAULT_CLEANUP_HOURS):
    """Automatically clean up old sessions"""
    try:
        import shutil
        from datetime import timedelta
        
        if not AUTO_CLEANUP_ENABLED:
            return 0, 0
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        cleaned_sessions = []
        total_size_freed = 0
        
        if not os.path.exists(OUTPUT_DIR):
            return 0, 0
        
        for session_dir in os.listdir(OUTPUT_DIR):
            session_path = os.path.join(OUTPUT_DIR, session_dir)
            if os.path.isdir(session_path):
                # Check if directory is older than cutoff time
                dir_creation_time = datetime.fromtimestamp(os.path.getctime(session_path))
                if dir_creation_time < cutoff_time:
                    success, size = cleanup_session_folder(session_dir, "auto-cleanup")
                    if success:
                        cleaned_sessions.append(session_dir)
                        total_size_freed += size
        
        if cleaned_sessions:
            logger.info(f"Auto-cleanup completed: {len(cleaned_sessions)} sessions removed, {total_size_freed} bytes freed")
        
        return len(cleaned_sessions), total_size_freed
    except Exception as e:
        logger.error(f"Error in auto-cleanup: {str(e)}")
        return 0, 0

# Lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Web Scraper API...")
    
    # Run initial cleanup of old sessions
    if AUTO_CLEANUP_ENABLED:
        cleaned_count, freed_size = auto_cleanup_old_sessions(DEFAULT_CLEANUP_HOURS)
        if cleaned_count > 0:
            logger.info(f"Startup cleanup: {cleaned_count} old sessions removed, {freed_size} bytes freed")
        else:
            logger.info("Startup cleanup: No old sessions found")
    
    logger.info("Web Scraper API started successfully!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Web Scraper API...")

app = FastAPI(title="Web Scraper API", version="1.0.0", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:180",
        "http://localhost:80",
        "http://localhost",
        "https://*.ngrok-free.app",
        "https://*.ngrok.io",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mount static files
app.mount("/output", StaticFiles(directory="output"), name="output")

class ScrapingRequest(BaseModel):
    url: str

class ScrapingResponse(BaseModel):
    success: bool
    message: str
    links_count: int = 0
    images_count: int = 0
    excel_file: Optional[str] = None
    images_folder: Optional[str] = None
    session_id: Optional[str] = None
    expires_at: Optional[str] = None

def rate_limit_delay():
    """Add random delay for rate limiting"""
    delay = random.uniform(*RATE_LIMIT_DELAY)
    time.sleep(delay)

def validate_image_data(data, max_size=MAX_IMAGE_SIZE):
    """Validate image data size and format"""
    if len(data) > max_size:
        return False, f"Image too large: {len(data)} bytes (max: {max_size})"
    return True, "OK"

def get_file_extension_from_url(url):
    """Extract file extension from URL"""
    parsed = urlparse(url)
    path = parsed.path
    if '.' in path:
        ext = path.split('.')[-1].lower()
        if ext in VALID_IMAGE_TYPES:
            return ext
    return 'jpg'  # default

def get_file_extension_from_mime_type(mime_type):
    """Extract file extension from MIME type"""
    if '/' in mime_type:
        ext = mime_type.split('/')[-1].split(';')[0].lower()
        if ext in VALID_IMAGE_TYPES:
            return ext
    return 'jpg'  # default

def retry_request(func, max_retries=MAX_RETRIES, delay=RETRY_DELAY):
    """Retry function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2  # exponential backoff

def cleanup_memory():
    """Clean up memory and run garbage collection"""
    gc.collect()

@app.get("/")
async def root():
    return {"message": "Web Scraper API is running!"}

@app.post("/api/scrape", response_model=ScrapingResponse)
async def scrape_website(request: ScrapingRequest):
    start_time = time.time()
    session_id = str(uuid.uuid4())
    
    log_scraping_activity(f"Starting scraping session | ID: {session_id} | URL: {request.url}")
    
    try:
        # Ensure output directory exists and has proper permissions
        if not os.path.exists(OUTPUT_DIR):
            try:
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                log_scraping_activity(f"Created output directory: {OUTPUT_DIR}")
            except PermissionError as e:
                log_error_with_context(e, f"Cannot create output directory: {OUTPUT_DIR}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Server configuration error: Cannot create output directory. Please contact administrator."
                )
        
        # Check if we can write to output directory
        if not os.access(OUTPUT_DIR, os.W_OK):
            log_error_with_context("Permission denied", f"Cannot write to output directory: {OUTPUT_DIR}")
            raise HTTPException(
                status_code=500,
                detail=f"Server configuration error: Cannot write to output directory. Please contact administrator."
            )
        
        session_output_dir = os.path.join(OUTPUT_DIR, session_id)
        try:
            os.makedirs(session_output_dir, exist_ok=True)
            log_scraping_activity(f"Created session directory: {session_output_dir}")
        except PermissionError as e:
            log_error_with_context(e, f"Cannot create session directory: {session_output_dir}")
            raise HTTPException(
                status_code=500,
                detail=f"Server configuration error: Cannot create session directory. Please contact administrator."
            )
        
        # Validate URL
        if not request.url.startswith(('http://', 'https://')):
            request.url = 'https://' + request.url
            log_scraping_activity(f"Added https:// prefix to URL: {request.url}")
        
        # Create session for all requests
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        

        
        # Scrape the website with retry logic
        scrape_start_time = time.time()
        
        def fetch_website():
            rate_limit_delay()  # Add rate limiting
            return session.get(request.url, timeout=30)
        
        response = retry_request(fetch_website)
        scrape_duration = time.time() - scrape_start_time
        
        log_request_details(request.url, "GET", response.status_code, scrape_duration)
        
        if response.status_code != 200:
            log_error_with_context(f"Failed to fetch website. Status code: {response.status_code}", f"Session: {session_id}")
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to fetch website. Status code: {response.status_code}"
            )
        
        log_scraping_activity(f"Successfully fetched website | URL: {request.url} | Duration: {scrape_duration:.2f}s")
        log_scraping_activity(f"Response content type: {response.headers.get('Content-Type', 'unknown')}")
        log_scraping_activity(f"Response content length: {len(response.text)} characters")
        
        # Check if response is actually HTML
        if 'text/html' not in response.headers.get('Content-Type', '').lower():
            log_scraping_activity(f"Warning: Response is not HTML. Content-Type: {response.headers.get('Content-Type')}")
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Debug: Check if we got valid HTML
        title = soup.find('title')
        log_scraping_activity(f"Page title: {title.get_text() if title else 'No title found'}")
        
        # Extract links with more details
        links_data = []
        links = soup.find_all('a')
        
        log_scraping_activity(f"Found {len(links)} anchor tags to process")
        
        for link in links:
            href = link.get('href')
            if href:
                # Clean and validate href
                href = href.strip()
                
                # Skip empty, javascript, mailto, tel links
                if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#', 'data:')):
                    continue
                
                # Resolve relative URLs
                if href.startswith('/'):
                    from urllib.parse import urljoin
                    href = urljoin(request.url, href)
                elif href.startswith('./'):
                    from urllib.parse import urljoin
                    href = urljoin(request.url, href)
                elif not href.startswith(('http://', 'https://')):
                    # Skip relative paths that don't start with /
                    continue
                
                # Clean the URL
                try:
                    from urllib.parse import urlparse, urlunparse
                    parsed = urlparse(href)
                    # Remove fragments and normalize
                    clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, ''))
                    
                    # Skip if URL is invalid
                    if not parsed.netloc:
                        continue
                        
                except Exception as e:
                    logger.warning(f"Invalid URL {href}: {str(e)}")
                    continue
                
                # Get link text and clean it
                link_text = link.get_text(strip=True)
                if not link_text:
                    link_text = link.get('title', '') or link.get('alt', '')
                
                links_data.append({
                    'url': clean_url,
                    'text': link_text[:200],  # Limit text length
                    'title': link.get('title', '')[:100],
                    'target': link.get('target', ''),
                    'rel': ' '.join(link.get('rel', [])) if isinstance(link.get('rel'), list) else link.get('rel', '')
                })
        
        # Remove duplicates based on URL
        unique_links = []
        seen_urls = set()
        for link in links_data:
            if link['url'] not in seen_urls:
                unique_links.append(link)
                seen_urls.add(link['url'])
        
        links_data = unique_links
        
        # Create DataFrame and save to CSV
        if links_data:
            df_links = pd.DataFrame(links_data)
            csv_filename = f'links_{session_id}.csv'
            csv_path = os.path.join(session_output_dir, csv_filename)
            
            # Debug: Log DataFrame info
            log_scraping_activity(f"DataFrame shape: {df_links.shape}")
            log_scraping_activity(f"DataFrame columns: {list(df_links.columns)}")
            log_scraping_activity(f"First few rows of DataFrame:")
            for i, row in df_links.head(3).iterrows():
                log_scraping_activity(f"  Row {i}: URL={row['url'][:50]}... | Text={row['text'][:30]}...")
            
            # Save with proper encoding and format
            df_links.to_csv(csv_path, index=False, encoding='utf-8-sig', quoting=1)  # quoting=1 for QUOTE_ALL
            
            # Verify the saved file
            try:
                with open(csv_path, 'r', encoding='utf-8-sig') as f:
                    first_lines = f.readlines()[:5]
                    log_scraping_activity(f"CSV file content (first 5 lines):")
                    for i, line in enumerate(first_lines):
                        log_scraping_activity(f"  Line {i+1}: {line.strip()}")
            except Exception as e:
                log_error_with_context(e, f"Error reading saved CSV file: {csv_path}")
            
            log_scraping_activity(f"CSV file saved: {csv_path}")
        else:
            # Create empty CSV with headers
            csv_filename = f'links_{session_id}.csv'
            csv_path = os.path.join(session_output_dir, csv_filename)
            
            with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
                import csv
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow(['url', 'text', 'title', 'target', 'rel'])
            
            log_scraping_activity("No links found, created empty CSV with headers")
        
        log_scraping_activity(f"Extracted {len(links_data)} unique links, saved to {csv_filename}")
        
        # Log some sample links for debugging
        if links_data:
            log_scraping_activity("Sample links extracted:")
            for i, link in enumerate(links_data[:5]):
                log_scraping_activity(f"  {i+1}. {link['url']} - {link['text'][:50]}")
            if len(links_data) > 5:
                log_scraping_activity(f"  ... and {len(links_data) - 5} more links")
        
        # Extract and save images with optimized concurrent downloads
        images = soup.find_all('img')
        saved_images = []
        
        log_scraping_activity(f"Found {len(images)} images to process")
        
        # Prepare image URLs for concurrent download
        image_tasks = []
        base64_images = []
        
        for img_index, img in enumerate(images):
            img_url = img.get('src')
            if not img_url:
                continue
                
            try:
                # Resolve relative image URLs
                if img_url.startswith('/'):
                    from urllib.parse import urljoin
                    img_url = urljoin(request.url, img_url)
                elif not img_url.startswith(('http://', 'https://', 'data:')):
                    continue
                
                if img_url.startswith('data:image'):
                    # Handle base64 encoded images (process immediately)
                    try:
                        img_type, img_data = img_url.split(';base64,')
                        img_type = img_type.split(':')[-1]
                        img_data_decoded = base64.b64decode(img_data)
                        
                        # Validate image data
                        is_valid, validation_msg = validate_image_data(img_data_decoded)
                        if not is_valid:
                            logger.warning(f"Base64 image {img_index} validation failed: {validation_msg}")
                            continue
                        
                        img_name = f'image_{img_index}'
                        ext = get_file_extension_from_mime_type(img_type)
                        
                        if ext.lower() in ['svg', 'plain']:
                            # Convert SVG to PNG
                            try:
                                svg_content = img_data_decoded.decode('utf-8')
                                output_path = os.path.join(session_output_dir, f'{img_name}.png')
                                cairosvg.svg2png(bytestring=svg_content, write_to=output_path)
                                saved_images.append(f'{img_name}.png')
                                logger.info(f"Saved SVG image as PNG: {img_name}.png")
                            except Exception as svg_error:
                                logger.error(f"Error converting SVG image {img_index}: {str(svg_error)}")
                                continue
                        else:
                            # Save as original format
                            output_path = os.path.join(session_output_dir, f'{img_name}.{ext}')
                            with open(output_path, 'wb') as img_file:
                                img_file.write(img_data_decoded)
                            saved_images.append(f'{img_name}.{ext}')
                            logger.info(f"Saved base64 image: {img_name}.{ext}")
                    except Exception as e:
                        logger.error(f"Error processing base64 image {img_index}: {str(e)}")
                        continue
                        
                else:
                    # Add to concurrent download queue
                    image_tasks.append((img_index, img_url))
                    
            except Exception as e:
                logger.error(f"Error processing image {img_index}: {str(e)}")
                continue
        
        # Download images concurrently
        if image_tasks:
            log_scraping_activity(f"Starting concurrent download of {len(image_tasks)} images")
            
            def download_single_image(task):
                img_index, img_url = task
                try:
                    # Minimal rate limiting
                    time.sleep(random.uniform(0.05, 0.2))  # 50-200ms delay
                    
                    img_response = session.get(img_url, stream=True, timeout=TIMEOUT)
                    
                    if img_response.status_code == 200:
                        # Get content type and validate
                        content_type = img_response.headers.get('Content-Type', 'image/jpeg')
                        ext = get_file_extension_from_mime_type(content_type)
                        
                        # Check content length if available
                        content_length = img_response.headers.get('Content-Length')
                        if content_length and int(content_length) > MAX_IMAGE_SIZE:
                            logger.warning(f"Image {img_url} too large: {content_length} bytes")
                            return None
                        
                        img_name = f'image_{img_index}.{ext}'
                        output_path = os.path.join(session_output_dir, img_name)
                        
                        # Download with size validation and larger chunks
                        total_size = 0
                        with open(output_path, 'wb') as img_file:
                            for chunk in img_response.iter_content(chunk_size=CHUNK_SIZE):
                                if chunk:
                                    total_size += len(chunk)
                                    if total_size > MAX_IMAGE_SIZE:
                                        logger.warning(f"Image {img_url} exceeded size limit during download")
                                        img_file.close()
                                        os.remove(output_path)
                                        return None
                                    img_file.write(chunk)
                        
                        return img_name
                    else:
                        logger.warning(f"Failed to download image {img_url}: Status {img_response.status_code}")
                        return None
                        
                except Exception as e:
                    logger.error(f"Error downloading image {img_url}: {str(e)}")
                    return None
            
            # Use ThreadPoolExecutor for concurrent downloads
            with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_DOWNLOADS) as executor:
                # Submit all download tasks
                future_to_task = {executor.submit(download_single_image, task): task for task in image_tasks}
                
                # Collect results as they complete
                for future in as_completed(future_to_task):
                    img_name = future.result()
                    if img_name:
                        saved_images.append(img_name)
                        logger.info(f"Downloaded image: {img_name}")
            
            log_scraping_activity(f"Concurrent download completed. Successfully downloaded {len(saved_images)} images")
        
        # Clean up memory
        cleanup_memory()
        
        # Calculate total duration
        total_duration = time.time() - start_time
        
        # Log detailed summary
        log_scraping_activity(f"Successfully saved {len(saved_images)} images")
        log_scraping_activity(f"Memory cleanup completed")
        log_scraping_activity(f"Session directory: {session_output_dir}")
        
        # Log session summary
        log_scraping_session(session_id, request.url, len(links_data), len(saved_images), success=True)
        log_scraping_activity(f"Scraping session completed | Duration: {total_duration:.2f}s | Links: {len(links_data)} | Images: {len(saved_images)}")
        
        # Calculate expiration time (24 hours from now)
        from datetime import timedelta
        expires_at = (datetime.now() + timedelta(hours=DEFAULT_CLEANUP_HOURS)).isoformat()
        
        return ScrapingResponse(
            success=True,
            message="Scraping completed successfully! Your files will be available for 24 hours.",
            links_count=len(links_data),
            images_count=len(saved_images),
            excel_file=f"/api/download/{session_id}/{csv_filename}",
            images_folder=f"/api/images/{session_id}",
            session_id=session_id,
            expires_at=expires_at
        )
        
    except Exception as e:
        total_duration = time.time() - start_time
        log_error_with_context(e, f"Session: {session_id} | URL: {request.url} | Duration: {total_duration:.2f}s")
        log_scraping_session(session_id, request.url, 0, 0, success=False)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{session_id}/{filename}")
async def download_file(session_id: str, filename: str):
    """Download file from scraping session with proper content type and auto-cleanup"""
    try:
        file_path = os.path.join(OUTPUT_DIR, session_id, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File {filename} not found in session {session_id}")
        
        # Determine content type based on file extension
        content_type = "application/octet-stream"
        if filename.endswith('.csv'):
            content_type = "text/csv"
        elif filename.endswith('.xlsx'):
            content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif filename.endswith(('.jpg', '.jpeg')):
            content_type = "image/jpeg"
        elif filename.endswith('.png'):
            content_type = "image/png"
        elif filename.endswith('.gif'):
            content_type = "image/gif"
        elif filename.endswith('.webp'):
            content_type = "image/webp"
        
        # Create response
        if filename.endswith('.csv'):
            response = FileResponse(
                file_path, 
                filename=filename,
                media_type=content_type,
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        else:
            response = FileResponse(
                file_path, 
                filename=filename,
                media_type=content_type
            )
        
        # Auto-cleanup after download if enabled
        if CLEANUP_AFTER_DOWNLOAD:
            # Schedule cleanup after response is sent
            import asyncio
            async def delayed_cleanup():
                await asyncio.sleep(1)  # Wait for response to be sent
                cleanup_session_folder(session_id, "download-complete")
            
            # Start cleanup task in background
            asyncio.create_task(delayed_cleanup())
            logger.info(f"Scheduled cleanup for session {session_id} after download")
        
        return response
            
    except Exception as e:
        logger.error(f"Error downloading file {filename} from session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")

@app.get("/api/files/{session_id}")
async def list_session_files(session_id: str):
    """List all files in a scraping session"""
    try:
        session_path = os.path.join(OUTPUT_DIR, session_id)
        
        if not os.path.exists(session_path):
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        files = []
        for filename in os.listdir(session_path):
            file_path = os.path.join(session_path, filename)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                files.append({
                    "filename": filename,
                    "size_bytes": file_size,
                    "size_mb": round(file_size / (1024 * 1024), 2),
                    "download_url": f"/api/download/{session_id}/{filename}"
                })
        
        return {
            "session_id": session_id,
            "files": files,
            "total_files": len(files),
            "total_size_mb": round(sum(f["size_bytes"] for f in files) / (1024 * 1024), 2)
        }
        
    except Exception as e:
        logger.error(f"Error listing files for session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

@app.get("/api/csv/{session_id}")
async def download_csv(session_id: str):
    """Download CSV file from scraping session with proper encoding"""
    try:
        session_path = os.path.join(OUTPUT_DIR, session_id)
        
        if not os.path.exists(session_path):
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        # Find CSV file in session
        csv_file = None
        for filename in os.listdir(session_path):
            if filename.endswith('.csv'):
                csv_file = filename
                break
        
        if not csv_file:
            raise HTTPException(status_code=404, detail=f"No CSV file found in session {session_id}")
        
        csv_path = os.path.join(session_path, csv_file)
        
        # Create response
        response = FileResponse(
            csv_path,
            filename=csv_file,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={csv_file}",
                "Content-Type": "text/csv; charset=utf-8"
            }
        )
        
        # Auto-cleanup after download if enabled
        if CLEANUP_AFTER_DOWNLOAD:
            # Schedule cleanup after response is sent
            import asyncio
            async def delayed_cleanup():
                await asyncio.sleep(1)  # Wait for response to be sent
                cleanup_session_folder(session_id, "csv-download-complete")
            
            # Start cleanup task in background
            asyncio.create_task(delayed_cleanup())
            logger.info(f"Scheduled cleanup for session {session_id} after CSV download")
        
        return response
        
    except Exception as e:
        logger.error(f"Error downloading CSV for session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading CSV: {str(e)}")

@app.get("/api/images/{session_id}")
async def download_images_zip(session_id: str):
    """Download all images from scraping session as ZIP file"""
    try:
        session_path = os.path.join(OUTPUT_DIR, session_id)
        
        if not os.path.exists(session_path):
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        # Find all image files in session
        image_files = []
        for filename in os.listdir(session_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')):
                image_files.append(filename)
        
        if not image_files:
            raise HTTPException(status_code=404, detail=f"No images found in session {session_id}")
        
        # Create ZIP file in memory
        zip_filename = f"images_{session_id}.zip"
        
        # Create temporary ZIP file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
            temp_zip_path = temp_zip.name
        
        try:
            with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for image_file in image_files:
                    image_path = os.path.join(session_path, image_file)
                    # Add file to ZIP with just the filename (no path)
                    zipf.write(image_path, image_file)
            
            # Create response
            response = FileResponse(
                temp_zip_path,
                filename=zip_filename,
                media_type="application/zip",
                headers={
                    "Content-Disposition": f"attachment; filename={zip_filename}",
                    "Content-Type": "application/zip"
                }
            )
            
            # Auto-cleanup after download if enabled
            if CLEANUP_AFTER_DOWNLOAD:
                # Schedule cleanup after response is sent
                import asyncio
                async def delayed_cleanup():
                    await asyncio.sleep(1)  # Wait for response to be sent
                    cleanup_session_folder(session_id, "images-download-complete")
                
                # Start cleanup task in background
                asyncio.create_task(delayed_cleanup())
                logger.info(f"Scheduled cleanup for session {session_id} after images download")
            
            return response
            
        except Exception as zip_error:
            # Clean up temp file on error
            if os.path.exists(temp_zip_path):
                os.unlink(temp_zip_path)
            raise zip_error
            
    except Exception as e:
        logger.error(f"Error creating images ZIP for session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating images ZIP: {str(e)}")

@app.get("/api/images/{session_id}/info")
async def get_images_info(session_id: str):
    """Get information about images in a session"""
    try:
        session_path = os.path.join(OUTPUT_DIR, session_id)
        
        if not os.path.exists(session_path):
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        # Find all image files in session
        image_files = []
        total_size = 0
        
        for filename in os.listdir(session_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')):
                image_path = os.path.join(session_path, filename)
                file_size = os.path.getsize(image_path)
                image_files.append({
                    "filename": filename,
                    "size_bytes": file_size,
                    "size_mb": round(file_size / (1024 * 1024), 2),
                    "extension": filename.split('.')[-1].lower()
                })
                total_size += file_size
        
        return {
            "session_id": session_id,
            "total_images": len(image_files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "images": image_files,
            "download_url": f"/api/images/{session_id}"
        }
        
    except Exception as e:
        logger.error(f"Error getting images info for session {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting images info: {str(e)}")

@app.get("/api/session/{session_id}/status")
async def get_session_status(session_id: str):
    """Get status and information about a scraping session"""
    try:
        session_path = os.path.join(OUTPUT_DIR, session_id)
        
        if not os.path.exists(session_path):
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        
        # Get session creation time
        creation_time = datetime.fromtimestamp(os.path.getctime(session_path))
        expires_at = creation_time + timedelta(hours=DEFAULT_CLEANUP_HOURS)
        
        # Count files
        files = os.listdir(session_path)
        csv_files = [f for f in files if f.endswith('.csv')]
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'))]
        
        # Calculate total size
        total_size = sum(
            os.path.getsize(os.path.join(session_path, f)) 
            for f in files 
            if os.path.isfile(os.path.join(session_path, f))
        )
        
        return {
            "session_id": session_id,
            "status": "available",
            "created_at": creation_time.isoformat(),
            "expires_at": expires_at.isoformat(),
            "time_remaining_hours": max(0, (expires_at - datetime.now()).total_seconds() / 3600),
            "files": {
                "total": len(files),
                "csv_files": len(csv_files),
                "image_files": len(image_files)
            },
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "download_urls": {
                "csv": f"/api/download/{session_id}/{csv_files[0]}" if csv_files else None,
                "images": f"/api/images/{session_id}" if image_files else None
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting session status for {session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting session status: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint with system info"""
    try:
        import psutil
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage(OUTPUT_DIR)
        
        return {
            "status": "healthy", 
            "timestamp": datetime.now().isoformat(),
            "system_info": {
                "memory_usage_percent": memory_info.percent,
                "disk_usage_percent": (disk_info.used / disk_info.total) * 100,
                "output_dir_size_mb": disk_info.used / (1024 * 1024)
            }
        }
    except ImportError:
        return {
            "status": "healthy", 
            "timestamp": datetime.now().isoformat(),
            "note": "psutil not available for detailed system info"
        }

@app.get("/api/debug/last-session")
async def get_last_session_info():
    """Debug endpoint to get info about the last scraping session"""
    try:
        # Get the most recent session directory
        if not os.path.exists(OUTPUT_DIR):
            return {"error": "No output directory found"}
        
        session_dirs = [d for d in os.listdir(OUTPUT_DIR) if os.path.isdir(os.path.join(OUTPUT_DIR, d))]
        if not session_dirs:
            return {"error": "No sessions found"}
        
        # Get the most recent session
        latest_session = max(session_dirs, key=lambda x: os.path.getctime(os.path.join(OUTPUT_DIR, x)))
        session_path = os.path.join(OUTPUT_DIR, latest_session)
        
        # Get files in the session
        files = os.listdir(session_path)
        
        # Read CSV content if exists
        csv_content = None
        csv_file = None
        for file in files:
            if file.endswith('.csv'):
                csv_file = file
                csv_path = os.path.join(session_path, file)
                try:
                    with open(csv_path, 'r', encoding='utf-8-sig') as f:
                        csv_content = f.read()
                except Exception as e:
                    csv_content = f"Error reading CSV: {str(e)}"
                break
        
        return {
            "latest_session": latest_session,
            "session_path": session_path,
            "files": files,
            "csv_file": csv_file,
            "csv_content": csv_content[:1000] if csv_content else None,  # First 1000 chars
            "csv_size": len(csv_content) if csv_content else 0
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/debug/logs")
async def get_logs_info():
    """Debug endpoint to get info about log files"""
    try:
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            return {"error": "Logs directory not found", "logs_dir": logs_dir}
        
        log_files = {}
        for file in os.listdir(logs_dir):
            if file.endswith('.log'):
                file_path = os.path.join(logs_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        log_files[file] = {
                            "size": len(content),
                            "lines": len(content.splitlines()),
                            "last_modified": os.path.getmtime(file_path),
                            "preview": content[-1000:] if len(content) > 1000 else content  # Last 1000 chars
                        }
                except Exception as e:
                    log_files[file] = {"error": str(e)}
        
        return {
            "logs_dir": os.path.abspath(logs_dir),
            "log_files": log_files,
            "total_files": len(log_files)
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/debug/logs/{filename}")
async def get_log_content(filename: str):
    """Debug endpoint to get content of a specific log file"""
    try:
        logs_dir = "logs"
        file_path = os.path.join(logs_dir, filename)
        
        if not os.path.exists(file_path):
            return {"error": f"Log file {filename} not found"}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "filename": filename,
            "size": len(content),
            "lines": len(content.splitlines()),
            "content": content[-5000:] if len(content) > 5000 else content  # Last 5000 chars
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/maintenance/cleanup")
async def cleanup_old_sessions(older_than_hours: int = DEFAULT_CLEANUP_HOURS):
    """Clean up old scraping sessions to free up disk space"""
    try:
        cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
        cleaned_sessions = []
        total_size_freed = 0
        
        if not os.path.exists(OUTPUT_DIR):
            return {"message": "No output directory found", "cleaned_sessions": 0}
        
        for session_dir in os.listdir(OUTPUT_DIR):
            session_path = os.path.join(OUTPUT_DIR, session_dir)
            if os.path.isdir(session_path):
                # Check if directory is older than cutoff time
                dir_creation_time = datetime.fromtimestamp(os.path.getctime(session_path))
                if dir_creation_time < cutoff_time:
                    success, size = cleanup_session_folder(session_dir, "scheduled-cleanup")
                    if success:
                        cleaned_sessions.append(session_dir)
                        total_size_freed += size
        
        # Clean up memory
        cleanup_memory()
        
        return {
            "message": f"Cleanup completed",
            "cleaned_sessions": len(cleaned_sessions),
            "total_size_freed_mb": round(total_size_freed / (1024 * 1024), 2),
            "cutoff_time": cutoff_time.isoformat(),
            "older_than_hours": older_than_hours
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

@app.post("/api/maintenance/cleanup/{session_id}")
async def cleanup_specific_session(session_id: str):
    """Clean up a specific session folder"""
    try:
        success, size = cleanup_session_folder(session_id, "manual-cleanup")
        
        if success:
            return {
                "message": f"Session {session_id} cleaned up successfully",
                "session_id": session_id,
                "size_freed_mb": round(size / (1024 * 1024), 2)
            }
        else:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found or already cleaned")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

@app.post("/api/maintenance/cleanup-all")
async def cleanup_all_sessions():
    """Clean up all session folders (use with caution)"""
    try:
        cleaned_sessions = []
        total_size_freed = 0
        
        if not os.path.exists(OUTPUT_DIR):
            return {"message": "No output directory found", "cleaned_sessions": 0}
        
        for session_dir in os.listdir(OUTPUT_DIR):
            session_path = os.path.join(OUTPUT_DIR, session_dir)
            if os.path.isdir(session_path):
                success, size = cleanup_session_folder(session_dir, "cleanup-all")
                if success:
                    cleaned_sessions.append(session_dir)
                    total_size_freed += size
        
        # Clean up memory
        cleanup_memory()
        
        return {
            "message": f"All sessions cleaned up",
            "cleaned_sessions": len(cleaned_sessions),
            "total_size_freed_mb": round(total_size_freed / (1024 * 1024), 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

@app.get("/api/maintenance/stats")
async def get_maintenance_stats():
    """Get maintenance statistics"""
    try:
        import shutil
        
        if not os.path.exists(OUTPUT_DIR):
            return {"error": "Output directory not found"}
        
        total_sessions = 0
        total_files = 0
        total_size = 0
        
        for session_dir in os.listdir(OUTPUT_DIR):
            session_path = os.path.join(OUTPUT_DIR, session_dir)
            if os.path.isdir(session_path):
                total_sessions += 1
                for dirpath, dirnames, filenames in os.walk(session_path):
                    total_files += len(filenames)
                    for filename in filenames:
                        file_path = os.path.join(dirpath, filename)
                        total_size += os.path.getsize(file_path)
        
        return {
            "total_sessions": total_sessions,
            "total_files": total_files,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "output_dir": OUTPUT_DIR
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@app.post("/api/debug/test-scrape")
async def test_scrape_debug(request: ScrapingRequest):
    """Debug endpoint to test scraping without saving files"""
    try:
        # Validate URL
        if not request.url.startswith(('http://', 'https://')):
            request.url = 'https://' + request.url
        
        # Simple scraping without login
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        response = session.get(request.url, timeout=30)
        
        if response.status_code != 200:
            return {"error": f"Failed to fetch website. Status code: {response.status_code}"}
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract links for debugging
        links_data = []
        links = soup.find_all('a')
        
        for i, link in enumerate(links[:10]):  # Only first 10 for debugging
            href = link.get('href')
            if href:
                href = href.strip()
                
                # Skip empty, javascript, mailto, tel links
                if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#', 'data:')):
                    continue
                
                # Resolve relative URLs
                if href.startswith('/'):
                    from urllib.parse import urljoin
                    href = urljoin(request.url, href)
                elif href.startswith('./'):
                    from urllib.parse import urljoin
                    href = urljoin(request.url, href)
                elif not href.startswith(('http://', 'https://')):
                    continue
                
                # Clean the URL
                try:
                    from urllib.parse import urlparse, urlunparse
                    parsed = urlparse(href)
                    clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, ''))
                    
                    if not parsed.netloc:
                        continue
                        
                except Exception as e:
                    continue
                
                # Get link text
                link_text = link.get_text(strip=True)
                if not link_text:
                    link_text = link.get('title', '') or link.get('alt', '')
                
                links_data.append({
                    'url': clean_url,
                    'text': link_text[:100],
                    'title': link.get('title', '')[:50],
                    'target': link.get('target', ''),
                    'rel': ' '.join(link.get('rel', [])) if isinstance(link.get('rel'), list) else link.get('rel', '')
                })
        
        return {
            "url": request.url,
            "response_status": response.status_code,
            "total_links_found": len(links),
            "valid_links_extracted": len(links_data),
            "sample_links": links_data,
            "html_preview": response.text[:500] + "..." if len(response.text) > 500 else response.text
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 