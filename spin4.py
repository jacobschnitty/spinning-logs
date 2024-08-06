import threading
import itertools
import time
import sys
import logging
import Image

"""
**************************************************
                Image to ASCII
**************************************************
"""

# Function to convert image to ASCII
def image_to_ascii(image_path, width=100):
    image = Image.open(image_path)
    aspect_ratio = image.height / image.width
    new_height = int(aspect_ratio * width)
    image = image.resize((width, new_height))
    image = image.convert('L')  # Convert to grayscale
    
    pixels = image.getdata()
    chars = "@%#*+=-:. "  # Characters to use for the ASCII art
    ascii_str = ''.join(chars[pixel // 25] for pixel in pixels)
    ascii_str = '\n'.join(ascii_str[i:i+width] for i in range(0, len(ascii_str), width))
    
    return ascii_str

"""
**************************************************
                Custom Logging
**************************************************
"""

# Utility function to convert hex to ANSI escape code
def hex_to_ansi_escape(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'\033[38;2;{r};{g};{b}m'

# Define color codes
COLOR_TIMESTAMP = hex_to_ansi_escape('#FFFBBD')  # Chiffon Lemon
COLOR_MESSAGE = hex_to_ansi_escape('#7FB069')    # Asparagus
COLOR_FUNCTION = hex_to_ansi_escape('#36C9C6')   # Rob egg blue
RESET_COLOR = '\033[0m'

def enable_logging(func):
    func_name = func.__name__
    start_time = time.time()
    # Use COLOR_FUNCTION to color the function name
    logger.info(f"Starting {COLOR_FUNCTION}{func_name}{RESET_COLOR}...")
    spinner_thread = spin()
    func()
    stop_spin()
    spinner_thread.join()  # Ensure the spinner thread is properly terminated
    elapsed_time = time.time() - start_time
    logger.info(f"{COLOR_FUNCTION}{func_name}{RESET_COLOR} completed in {elapsed_time:.2f} seconds!")

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

"""
**************************************************
    Main Execution
        1. Image to ASCII
**************************************************
"""

# Define the image paths
image_paths = [
    r"C:\Users\jacobs\Pictures\snake.jpg",
    # Add more image paths here
]

# Example usage: process the first image in the list
for image_path in image_paths:
    ascii_art = image_to_ascii(image_path)
    enable_logging(lambda: print(ascii_art))
