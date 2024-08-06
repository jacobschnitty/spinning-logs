import threading
import itertools
import time
import sys
import logging
from ascii_magic import AsciiArt, from_image

"""
**************************************************
                Custom Logging
**************************************************
"""

# enable_logging takes in another function (func) and its name (func_name) as parameters. 
# It logs the start time, starts the spinner, runs the given function, stops the spinner, 
# logs the elapsed time, and logs when the task is completed.

def enable_logging(func, func_name):
    start_time = time.time()
    logger.info(f"Starting {func_name}...")
    spinner_thread = spin()
    func()
    stop_spin()
    spinner_thread.join()  # Ensure the spinner thread is properly terminated
    elapsed_time = time.time() - start_time
    logger.info(f"{func_name} completed in {elapsed_time:.2f} seconds!")

COLOR_TIMESTAMP = '\033[38;2;255;251;189m'  # #FFFBBD - Chiffon Lemon
COLOR_MESSAGE = '\033[38;2;127;176;105m'    # #7FB069 - Asparagus
RESET_COLOR = '\033[0m'

# Custom logging formatter
class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_message         = super().format(record)
        timestamp, message  = log_message.split(' - ', 1)
        colored_timestamp   = f"{COLOR_TIMESTAMP}{timestamp}{RESET_COLOR}"
        colored_message     = f"{COLOR_MESSAGE}{message}{RESET_COLOR}"
        return f"{colored_timestamp} - {colored_message}"

# Configure logging
logger      = logging.getLogger()
handler     = logging.StreamHandler()
formatter   = CustomFormatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

"""
**************************************************
                    Spinner
**************************************************
"""

def spin():
    
    # Define the spinner symbols with ASCII characters
    lunation_loop = itertools.cycle(['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'])
    
    # Set the spinner 
    spinner = lunation_loop
    
    # Define a flag to stop the spinner
    global spinning
    spinning = True

    def spin_thread():
        while spinning:
            sys.stdout.write(next(spinner) + '\r')
            sys.stdout.flush()
            time.sleep(0.3)  # Adjust the speed of the spinner

    # Create and start the spinner thread
    t = threading.Thread(target=spin_thread)
    t.start()
    return t

def stop_spin():
    global spinning
    spinning = False

def long_running_task():
    time.sleep(5)  # Simulate a long-running task

"""
**************************************************
    Main Execution
        1. Image to ASCII
**************************************************
"""

image_path = r"C:\Users\jacobs\Pictures\snake.jpg"
my_art = from_image(image_path)

# Execute the function with logging and spinner
enable_logging(my_art.to_terminal, "my_art.to_terminal")
# Create an AsciiArt object from the image file
my_art.to_terminal()
