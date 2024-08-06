# spin8.py 11:03pm

import time
import random
import timber              # Custom logging module
import lunar               # Custom spinner module
import thread_boss         # Custom threading module

# An example of a program I might write
def slow_function(thread_index):
    # Simulating waiting on an API response
    time.sleep(random.randint(1, 5))
    timber.logger.info(f"Thread {thread_index} done!")

# Using my modules for tarting up the terminal
spinning_thread = lunar.start_spinning()                            # Start the spinner
timber.enable_logging(thread_boss.run_threads, slow_function)       # Enable logging and run threads
lunar.stop_spinning()                                               # Stop the spinner
spinning_thread.join()
