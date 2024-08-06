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

def spin():
    global spinning
    spinning = True
    symbols = config_data["spinner"]["symbols"]
    spinner = itertools.cycle(symbols)

    def spin_thread():
        while spinning:
            sys.stdout.write(next(spinner) + '\r')
            sys.stdout.flush()
            time.sleep(config_data["spinner"]["speed"])

    t = threading.Thread(target=spin_thread, daemon=True)
    t.start()
    return t

def stop_spin():
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

@app._got_first_request
def print_routes():
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:20} {rule.methods} {rule.rule}")

if __name__ == '__main__':
    spinner_thread = spin()
    app.run(debug=True, use_reloader=False)  # use_reloader=False to prevent the spinner from restarting
    stop_spin()
    spinner_thread.join()
