import requests
from flask import Flask, jsonify
import datetime

app = Flask(__name__)
brew_count = 0

def get_temperature(api_key, lat, lon):
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}'

    response = requests.get(url)
    data = response.json()
    current_weather = data.get('current', {})
    temperature = current_weather.get('temp')
    return temperature


@app.route('/brew-coffee', methods=['GET'])
def brew_coffee():
    global brew_count
    brew_count += 1

    # Check if today is April 1st
    if datetime.date.today().month == 4 and datetime.date.today().day == 1:
        return '', 418  # Return 418 I'm a teapot if it's April 1st

    # Check if it's every fifth call
    if brew_count % 5 == 0:
        return '', 503  # Return 503 Service Unavailable on every fifth call

    api_key = 'Key_of_API'
    lat = -36.84583  # Example
    lon = 174.75611  # Example
    temperature = get_temperature(api_key, lat, lon)

    # Determine message based on temperature
    if temperature is not None and temperature > 30:
        message = "Your refreshing iced coffee is ready"
    else:
        message = "Your piping hot coffee is ready"

    response_data = {
        "message": message,
        "prepared": datetime.datetime.now().isoformat()
    }

    return jsonify(response_data), 200  # Return 200 OK with JSON response

if __name__ == '__main__':
    app.run(debug=True)
