import threading, itertools, time, random, sys, logging
from ascii_magic import AsciiArt, from_image

"""
**************************************************
                Image to ASCII
**************************************************
"""

# Function to convert image to ASCII using ascii-magic
def image_to_ascii(image_path):
    # Create an AsciiArt object from the image file
    art = from_image(image_path)
    # Return the ASCII art as a string
    return art.to_terminal()

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

def enable_logging(func, *args, **kwargs):
    func_name = func.__name__
    start_time = time.time()
    # Use COLOR_FUNCTION to color the function name
    logger.info(f"Starting {COLOR_FUNCTION}{func_name}{RESET_COLOR}...")
    spinner_thread = spin()
    result = func(*args, **kwargs)
    stop_spin()
    spinner_thread.join()  # Ensure the spinner thread is properly terminated
    elapsed_time = time.time() - start_time
    logger.info(f"{COLOR_FUNCTION}{func_name}{RESET_COLOR} completed in {elapsed_time:.2f} seconds!")
    return result

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
**************************************************
"""

# This function simulates waiting time, like waiting on an API response.
def slow_function(thread_index):
    time.sleep(random.randint(1, 5))
    logger.info(f"Thread {thread_index} done!")

def run_threads():
    threads = []

    for thread_index in range(5):
        individual_thread = threading.Thread(target=slow_function, args=(thread_index,))
        threads.append(individual_thread)
        individual_thread.start()
    
    # At this point, threads are running independently from the main flow of the application 
    logger.info("mainflow of application")

    # This ensures that all threads finish before the main flow of application continues. 
    for individual_thread in threads:
        individual_thread.join()

enable_logging(run_threads)
