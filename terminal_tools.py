# terminal_tools.py

"""
##############################
    TABLE OF CONTENTS
##############################

1. Import Statements
2. Utility Functions
3. Colour Configurations
4. Custom Logging Formatter
5. Logging Configuration
6. Logging Function
7. Spinner Functions

"""

# 1. Import Statements
import logging
import time
import threading
import itertools
import sys
import requests
import json

"""
##############################
    2. Utility Functions
##############################
"""

# Utility function to convert hex to ANSI escape code
def hex_to_ansi_escape(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'\033[38;2;{r};{g};{b}m'

"""
##############################
    3. Colour Configurations
##############################
"""

# Colour config
COLOR_TIMESTAMP = hex_to_ansi_escape('#FFFBBD')  # Chiffon Lemon
COLOR_MESSAGE = hex_to_ansi_escape('#7FB069')    # Asparagus
COLOR_FUNCTION = hex_to_ansi_escape('#36C9C6')   # Rob egg blue
RESET_COLOR = '\033[0m'

"""
##############################
    4. Custom Logging Formatter
##############################
"""

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_message = super().format(record)
        timestamp, message = log_message.split(' - ', 1)
        colored_timestamp = f"{COLOR_TIMESTAMP}{timestamp}{RESET_COLOR}"
        colored_message = f"{COLOR_MESSAGE}{message}{RESET_COLOR}"
        return f"{colored_timestamp} - {colored_message}"

"""
##############################
    5. Logging Configuration
##############################
"""

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_formatter = CustomFormatter('%(asctime)s - %(message)s')
console_handler.setFormatter(console_formatter)

# File handler
file_handler = logging.FileHandler('app.log')
file_formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

"""
##############################
    6. Logging Function
##############################
"""

# Logging function
def enable_logging(func, *args, **kwargs):
    func_name = func.__name__
    start_time = time.time()
    logger.info(f"Starting {COLOR_FUNCTION}{func_name}{RESET_COLOR}...")
    
    # Start the spinner
    spinner_config = get_spinner_config()
    spinning_thread = start_spinner(spinner_config["symbols"], spinner_config["speed"])
    
    result = func(*args, **kwargs)
    stop_spinner()
    spinning_thread.join()
    
    elapsed_time = time.time() - start_time
    logger.info(f"{COLOR_FUNCTION}{func_name}{RESET_COLOR} completed in {elapsed_time:.2f} seconds!")
    return result

"""
##############################
    7. Spinner Functions
##############################
"""

# Global spinner state
spinning = False

def start_spinner(symbols, speed):
    global spinning
    spinning = True
    spinner = itertools.cycle(symbols)

    def spin():
        while spinning:
            sys.stdout.write(next(spinner) + '\r')
            sys.stdout.flush()
            time.sleep(speed)

    # Start spinner thread
    spinner_thread = threading.Thread(target=spin, daemon=True)
    spinner_thread.start()
    return spinner_thread

def stop_spinner():
    global spinning
    spinning = False

"""
##############################
    Notes
##############################
"""

"""
Changelog

Updated start_spinner Function:
- Modified start_spinner to accept symbols and speed as parameters.
- Created and started the spinner thread correctly.
- Integrated Spinner with enable_logging:

- Fetched spinner configuration using get_spinner_config() inside enable_logging.
- Passed spinner configuration to start_spinner and ensured it starts and stops properly.
- Updated enable_logging Function:

- Added functionality to start and stop the spinner based on configuration fetched from the API.
- Example Function:
    - Added example_function to demonstrate how enable_logging can be used. 
    - Uncomment the function call at the end of the script to test.
"""
