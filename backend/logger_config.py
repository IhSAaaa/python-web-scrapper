import logging
import logging.handlers
import os
from datetime import datetime

def setup_logger():
    """Setup comprehensive logging for the web scraper backend"""
    
    try:
        # Create logs directory if it doesn't exist
        logs_dir = "logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create logger
        logger = logging.getLogger('web_scraper')
        logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 1. Console Handler (INFO and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)
        
        # 2. File Handler for all logs (DEBUG and above)
        all_logs_file = os.path.join(logs_dir, 'web_scraper.log')
        file_handler = logging.handlers.RotatingFileHandler(
            all_logs_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
        
        # 3. Error Handler (ERROR and above)
        error_logs_file = os.path.join(logs_dir, 'web_scraper_errors.log')
        error_handler = logging.handlers.RotatingFileHandler(
            error_logs_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        logger.addHandler(error_handler)
        
        # 4. Scraping Activity Handler (INFO and above)
        activity_logs_file = os.path.join(logs_dir, 'scraping_activity.log')
        activity_handler = logging.handlers.RotatingFileHandler(
            activity_logs_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        activity_handler.setLevel(logging.INFO)
        activity_handler.setFormatter(simple_formatter)
        logger.addHandler(activity_handler)
        
        # 5. Daily rotating handler for detailed logs
        daily_logs_file = os.path.join(logs_dir, f'web_scraper_{datetime.now().strftime("%Y-%m-%d")}.log')
        daily_handler = logging.handlers.TimedRotatingFileHandler(
            daily_logs_file,
            when='midnight',
            interval=1,
            backupCount=30,  # Keep 30 days of logs
            encoding='utf-8'
        )
        daily_handler.setLevel(logging.DEBUG)
        daily_handler.setFormatter(detailed_formatter)
        logger.addHandler(daily_handler)
        
        # Test logging
        logger.info("=== LOGGING SYSTEM INITIALIZED ===")
        logger.info(f"Log files will be saved in: {os.path.abspath(logs_dir)}")
        logger.info(f"Main log file: {all_logs_file}")
        logger.info(f"Error log file: {error_logs_file}")
        logger.info(f"Activity log file: {activity_logs_file}")
        logger.info(f"Daily log file: {daily_logs_file}")
        
        return logger
        
    except Exception as e:
        # Fallback to basic logging if setup fails
        print(f"Error setting up custom logger: {e}")
        basic_logger = logging.getLogger('web_scraper')
        basic_logger.setLevel(logging.INFO)
        
        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        console_handler.setFormatter(formatter)
        basic_logger.addHandler(console_handler)
        
        basic_logger.warning("Using fallback logging system")
        return basic_logger

def get_logger():
    """Get the configured logger"""
    return logging.getLogger('web_scraper')

def log_scraping_activity(message, level='info'):
    """Convenience function to log scraping activities"""
    try:
        logger = get_logger()
        if level.lower() == 'debug':
            logger.debug(message)
        elif level.lower() == 'info':
            logger.info(message)
        elif level.lower() == 'warning':
            logger.warning(message)
        elif level.lower() == 'error':
            logger.error(message)
        elif level.lower() == 'critical':
            logger.critical(message)
    except Exception as e:
        print(f"Error in log_scraping_activity: {e}")
        print(f"Message: {message}")

def log_request_details(url, method, status_code, duration=None):
    """Log HTTP request details"""
    try:
        logger = get_logger()
        duration_str = f" | Duration: {duration:.2f}s" if duration else ""
        logger.info(f"HTTP {method} {url} | Status: {status_code}{duration_str}")
    except Exception as e:
        print(f"Error in log_request_details: {e}")

def log_scraping_session(session_id, url, links_count, images_count, success=True):
    """Log scraping session summary"""
    try:
        logger = get_logger()
        status = "SUCCESS" if success else "FAILED"
        logger.info(f"SCRAPING SESSION | ID: {session_id} | URL: {url} | Status: {status} | Links: {links_count} | Images: {images_count}")
    except Exception as e:
        print(f"Error in log_scraping_session: {e}")

def log_error_with_context(error, context=""):
    """Log errors with additional context"""
    try:
        logger = get_logger()
        context_str = f" | Context: {context}" if context else ""
        logger.error(f"ERROR: {str(error)}{context_str}", exc_info=True)
    except Exception as e:
        print(f"Error in log_error_with_context: {e}")
        print(f"Original error: {error}")
        print(f"Context: {context}") 