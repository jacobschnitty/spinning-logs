from flask import Flask, request, jsonify
import threading
import itertools
import sys
import time

app = Flask(__name__)

# Example configuration data
config_data = {
    "spinner": {
        "name": "kims_dots",
        "symbols": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
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

# Spinner Code
def start_spinning():
    symbols = itertools.cycle(config_data["spinner"]["symbols"])
    global spinning
    spinning = True

    def spin_thread():
        while spinning:
            sys.stdout.write(next(symbols) + '\r')
            sys.stdout.flush()
            time.sleep(config_data["spinner"]["speed"])

    # Create and start the spinner thread
    t = threading.Thread(target=spin_thread, daemon=True)
    t.start()
    return t

def stop_spinning():
    global spinning
    spinning = False

@app.route('/config/spinner', methods=['PUT'])
def update_spinner_config():
    global config_data
    new_config = request.json
    name = new_config.get("name")
    symbols = new_config.get("symbols")
    speed = new_config.get("speed")
    
    if name in symbol_sets and symbols == symbol_sets[name] and speed is not None:
        config_data["spinner"] = new_config
        return jsonify({"message": "Configuration updated successfully"}), 200
    else:
        return jsonify({"message": "Invalid configuration"}), 400

@app.route('/config/spinner', methods=['GET'])
def get_spinner_config():
    return jsonify(config_data["spinner"])

if __name__ == '__main__':
    spinner_thread = start_spinning()  # Start the spinner
    try:
        app.run(debug=True)  # Run the Flask server
    finally:
        stop_spinning()  # Stop the spinner when the server shuts down
        spinner_thread.join()  # Ensure the spinner thread has finished
