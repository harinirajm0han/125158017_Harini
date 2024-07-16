from flask import Flask, request, jsonify
import requests
import time
import random

app = Flask(__name__)

window_size = 10
numbers = []

@app.route('/number/<numberid>', methods=['GET'])
def fetch_number(numberid):
    global numbers
    if numberid not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": f"Invalid numberid '{numberid}'. Valid ids: p, f, e, r"}), 400

    response = fetch_number_from_server(numberid)
    if response is None:
        return jsonify({"error": f"Failed to fetch number from third-party server for '{numberid}'"}), 500

    current_numbers = numbers[:]
    numbers.append(response)
    if len(numbers) > window_size:
        numbers.pop(0)

    window_prev_state = current_numbers[-window_size:] if len(current_numbers) > window_size else []
    window_curr_state = numbers[-window_size:]

    average = sum(numbers[-window_size:]) / len(numbers[-window_size:])

    return jsonify({
        "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "numbers": numbers[-1],
        "avg": f"{average:.2f}"
    })

def fetch_number_from_server(numberid):
    url = f'https://api.example.com/{numberid}'  # Replace with actual API endpoint
    try:
        start_time = time.time()
        response = requests.get(url, timeout=0.5)  # Timeout set to 500ms
        if response.status_code == 200:
            return response.json()['number']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching number from server: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)