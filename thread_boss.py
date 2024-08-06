# thread_boss.py

import threading
import timber  # Ensure the custom logging module is imported

def run_threads(slow_function):
    threads = []

    for thread_index in range(5):
        individual_thread = threading.Thread(target=slow_function, 
                                             args=(thread_index,), 
                                             daemon=True)
        threads.append(individual_thread)
        individual_thread.start()
    
    timber.logger.info("Main flow of application")  # Threads now running independently from main flow of program

    for individual_thread in threads:               # Ensure all threads finish before main flow of program continues
        individual_thread.join()
