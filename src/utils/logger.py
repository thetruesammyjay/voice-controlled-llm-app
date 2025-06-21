import logging
import os
from src.utils.config import config # Import config to use DEBUG setting

def setup_logging(log_file="app.log", log_dir="data/logs"):
    """
    Configures the global logging for the application.

    Args:
        log_file (str): The name of the log file.
        log_dir (str): The directory where the log file will be saved.
    """
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if config.DEBUG else logging.INFO) # Set level based on debug config

    # Clear existing handlers to prevent duplicate messages if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) # Console generally shows INFO and above
    
    # Create a file handler
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG) # File captures all DEBUG messages and above

    # Define a formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Set formatter for both handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logging.info(f"Logging configured. Logs will be saved to: {log_path}")
    logging.debug(f"Debug mode is {'ON' if config.DEBUG else 'OFF'}.")

# Example usage (for testing purposes)
if __name__ == "__main__":
    # Temporarily set debug for testing purposes if not already set by .env
    # os.environ['DEBUG'] = 'True'
    # Reload config if you modify env vars directly in the same session
    # from importlib import reload
    # reload(config_module) # assuming config is imported as config_module elsewhere
    
    setup_logging(log_file="test_app.log", log_dir="data/logs")
    
    logging.debug("This is a debug message.")
    logging.info("This is an info message.")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")
    try:
        1 / 0
    except ZeroDivisionError:
        logging.exception("An exception occurred!")

    print("\nCheck 'data/logs/test_app.log' for file output.")
