# timber.py 10:15pm

import logging
import time

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

# This is the logging function, it takes the name of the function 
# passed through for increased visibility in terminal feedback. 
def enable_logging(func, *args, **kwargs):
    func_name = func.__name__
    start_time = time.time()
    logger.info(f"Starting {COLOR_FUNCTION}{func_name}{RESET_COLOR}...")
    result = func(*args, **kwargs)
    elapsed_time = time.time() - start_time
    logger.info(f"{COLOR_FUNCTION}{func_name}{RESET_COLOR} completed in {elapsed_time:.2f} seconds!")
    return result

# Formatter
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
