import logging
import time
import random
import threading
import itertools
import sys
import requests
import json

CONFIG_URL = 'http://127.0.0.1:5000/config'

def get_config(section):
    response = requests.get(f"{CONFIG_URL}/{section}")
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Failed to retrieve config section: {section}")

def update_config(section, data):
    response = requests.post(f"{CONFIG_URL}/{section}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Failed to update config section: {section}")

# Example usage
def get_spinner_config():
    return get_config('spinner')

def update_spinner_config(new_config):
    return update_config('spinner', new_config)

def get_logging_config():
    return get_config('logging')

def update_logging_config(new_config):
    return update_config('logging', new_config)

# Utility function to convert hex to ANSI escape code
def hex_to_ansi_escape(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'\033[38;2;{r};{g};{b}m'

# Colour config
COLOR_TIMESTAMP = hex_to_ansi_escape('#FFFBBD')  # Chiffon Lemon
COLOR_MESSAGE = hex_to_ansi_escape('#7FB069')    # Asparagus
COLOR_FUNCTION = hex_to_ansi_escape('#36C9C6')   # Rob egg blue
RESET_COLOR = '\033[0m'

# Custom logging formatter
class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_message = super().format(record)
        timestamp, message = log_message.split(' - ', 1)
        colored_timestamp = f"{COLOR_TIMESTAMP}{timestamp}{RESET_COLOR}"
        colored_message = f"{COLOR_MESSAGE}{message}{RESET_COLOR}"
        return f"{colored_timestamp} - {colored_message}"

# Logging config
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = CustomFormatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Logging function
def enable_logging(func, *args, **kwargs):
    func_name = func.__name__
    start_time = time.time()
    logger.info(f"Starting {COLOR_FUNCTION}{func_name}{RESET_COLOR}...")
    spinning_thread = start_spinning()
    result = func(*args, **kwargs)
    stop_spinning()
    spinning_thread.join()
    elapsed_time = time.time() - start_time
    logger.info(f"{COLOR_FUNCTION}{func_name}{RESET_COLOR} completed in {elapsed_time:.2f} seconds!")
    return result

# Spinner functions
def start_spinning():
    lunation_loop = itertools.cycle(['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'])
    spinner = lunation_loop
    global spinning
    spinning = True

    def spin_thread():
        while spinning:
            sys.stdout.write(next(spinner) + '\r')
            sys.stdout.flush()
            time.sleep(0.3)

    t = threading.Thread(target=spin_thread)
    t.start()
    return t

def stop_spinning():
    global spinning
    spinning = False

# Threading function
def run_threads(func):
    def inner_run(*args, **kwargs):
        threads = []
        for thread_index in range(5):
            individual_thread = threading.Thread(target=func, args=(thread_index,), daemon=True)
            threads.append(individual_thread)
            individual_thread.start()

        logger.info("Main flow of application")
        for individual_thread in threads:
            individual_thread.join()

    return inner_run
