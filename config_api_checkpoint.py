from flask import Flask, request, jsonify

app = Flask(__name__)

# Example configuration data
config_data = {
    "spinner": {
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
        config_data["spinner"] = new_config
        return jsonify({"message": "Configuration updated successfully"}), 200
    else:
        return jsonify({"message": "Invalid configuration"}), 400

@app.route('/config/spinner', methods=['GET'])
def get_spinner_config():
    return jsonify(config_data["spinner"])

def print_routes():
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        print(f"{rule.endpoint:20} {methods:20} {rule.rule}")

if __name__ == '__main__':
    print_routes()  # Print routes before starting the server
    app.run(debug=True)
