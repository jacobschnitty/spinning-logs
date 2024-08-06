# spin9.py 11:13

import time
import random
import terminal_tools   # Combined module

# An example of a program
def slow_function(thread_index):
    time.sleep(random.randint(1, 5))    # Time (seconds) of random wait
    terminal_tools.logger.info(f"Thread {thread_index} done!")

# Using the combined module for tarting up the terminal
terminal_tools.enable_logging(terminal_tools.run_threads(slow_function))
