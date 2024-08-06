import requests
import json

# Constants
PYPI_URL = 'https://pypi.org/simple'

def fetch_library_list():
    """
    Fetch the list of library names from PyPI.
    """
    response = requests.get(PYPI_URL)
    if response.status_code == 200:
        # Extract library names from the HTML response
        lines = response.text.splitlines()
        libraries = [line.split('/')[0] for line in lines if line]
        return libraries
    else:
        raise Exception(f"Failed to fetch library list: {response.status_code}")

def fetch_library_data(library_name):
    """
    Fetch data for a given library from PyPI.
    """
    info_url = f'https://pypi.org/pypi/{library_name}/json'
    response = requests.get(info_url)
    if response.status_code == 200:
        data = response.json()
        return {
            'name': data.get('name', 'N/A'),
            'description': data.get('description', 'No description available.'),
            'downloads': data.get('info', {}).get('downloads', {}).get('total', 'N/A')
        }
    else:
        return {
            'name': library_name,
            'description': 'Error fetching details',
            'downloads': 'N/A'
        }

def display_library_info(libraries):
    """
    Display information about libraries and cycle through them.
    """
    index = 0
    while True:
        library = libraries[index]
        data = fetch_library_data(library)
        
        print(f"\nLibrary Name: {data['name']}")
        print(f"Description: {data['description']}")
        print(f"Total Downloads: {data['downloads']}")
        
        user_input = input("\nPress 'n' for next library, 'p' for previous library, 'q' to quit: ").strip().lower()
        if user_input == 'n':
            index = (index + 1) % len(libraries)
        elif user_input == 'p':
            index = (index - 1) % len(libraries)
        elif user_input == 'q':
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == '__main__':
    try:
        print("Fetching library list...")
        library_list = fetch_library_list()
        print(f"Found {len(library_list)} libraries.")
        display_library_info(library_list)
    except Exception as e:
        print(f"An error occurred: {e}")
