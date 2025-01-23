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
