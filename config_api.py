import threading
import itertools
import sys
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Example configuration data
config_data = {
    "spinners": {
        "name": "lunar",
        "symbols": ["🌑", "🌒", "🌓", "🌔", "🌕"],
        "speed": 0.3
    },
    "logging": {
        "timestamp_color": "#FFFBBD",
        "message_color": "#7FB069",
        "function_color": "#36C9C6"
    }
}

# Predefined symbol sets
symbol_sets = {
    "lunar": ["🌑", "🌒", "🌓", "🌔", "🌕"],
    "kims_dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
}

@app.route('/config/spinner', methods=['PUT'])
def update_spinner_config():
    global config_data
    new_config = request.json
    name = new_config.get("name")
    symbols = new_config.get("symbols")
    speed = new_config.get("speed")
    
    if name in symbol_sets and symbols == symbol_sets[name] and speed is not None:
        config_data["spinners"] = {
            "name": name,
            "symbols": symbols,
            "speed": speed
        }
        return jsonify({"message": "Configuration updated successfully"}), 200
    else:
        return jsonify({"message": "Invalid configuration"}), 400

@app.route('/config/spinner', methods=['GET'])
def get_spinner_config():
    return jsonify(config_data["spinners"])

def hex_to_ansi_escape(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'\033[38;2;{r};{g};{b}m'

# Color definitions
COLOR_AVAILABLE_ROUTES = hex_to_ansi_escape('#7FB069')
COLOR_HEAD = hex_to_ansi_escape('#26A96C')
COLOR_OPTIONS = hex_to_ansi_escape('#D7A2C8')
COLOR_GET = hex_to_ansi_escape('#5AAA95')
COLOR_PATH = hex_to_ansi_escape('#53599A')
RESET_COLOR = '\033[0m'

def print_routes():
    print(f"{COLOR_AVAILABLE_ROUTES}Available routes:{RESET_COLOR}")
    for rule in app.url_map.iter_rules():
        # Create a list of method colors
        method_colors = []
        for method in rule.methods:
            if method == 'HEAD':
                method_colors.append(COLOR_HEAD + method + RESET_COLOR)
            elif method == 'OPTIONS':
                method_colors.append(COLOR_OPTIONS + method + RESET_COLOR)
            elif method == 'GET':
                method_colors.append(COLOR_GET + method + RESET_COLOR)
            else:
                method_colors.append(method)  # No color for other methods
        
        # Join the method colors into a single string
        methods = ', '.join(method_colors)
        path = f"{rule.rule}"
        print(f"{RESET_COLOR}{rule.endpoint:20} {methods:20} {COLOR_PATH}{path}{RESET_COLOR}")

def start_spinner():
    lunation_loop = itertools.cycle(config_data["spinners"]["symbols"])
    spinner = lunation_loop
    
    def spin():
        while True:
            sys.stdout.write(next(spinner) + '\r')
            sys.stdout.flush()
            time.sleep(config_data["spinners"]["speed"])
    
    # Start spinner in a separate thread
    threading.Thread(target=spin, daemon=True).start()

if __name__ == '__main__':
    # Print routes once during server startup
    print_routes()
    
    # Start the spinner
    start_spinner()
    
    # Run the Flask app
    print(f"* Running on http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)  # Disable reloader to avoid duplicate printing
