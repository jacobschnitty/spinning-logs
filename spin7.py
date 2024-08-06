# spin7.py 10:10pm

import threading
import time
import random  
import timber                                       # Custom logging module
import lunar                                        # Custom Spinner module

def slow_function(thread_index):                    # Simulating waiting on an API response
    time.sleep(random.randint(1, 5))                # Time (seconds) of random wait
    timber.logger.info(f"Thread {thread_index} done!")

def run_threads():
    threads = []
    for thread_index in range(5):
        individual_thread = threading.Thread(target = slow_function, 
                                             args   = (thread_index,), 
                                             daemon = True)
        threads.append(individual_thread)
        individual_thread.start()
    
    timber.logger.info("Main flow of application")  # Threads now running independently from main flow of program

    for individual_thread in threads:               # All threads finish before main flow of program continues
        individual_thread.join()

spinning_thread = lunar.start_spinning()
timber.enable_logging(run_threads)
lunar.stop_spinning()
spinning_thread.join()
