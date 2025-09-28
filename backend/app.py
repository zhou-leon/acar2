# Imports
import os
from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import sys
sys.path.append('../struct')
import vehicles
import utils

app = Flask(__name__)

cars = vehicles.Vehicles()

# Endpoint to get event report text for a vehicle by name
@app.route('/event-report', methods=['GET'])
def get_event_report():
    import urllib.parse
    car_name = request.args.get('name')
    if not car_name:
        return jsonify({'error': 'Missing car name'}), 400
    car_name = urllib.parse.unquote(car_name)
    car_struct = cars.find(car_name)
    if car_struct is not None:
        report = utils.gen_report(car_name)
        return jsonify({'report': report})
    return jsonify({'report': ''})

# Endpoint to get list of car names
@app.route('/car-list', methods=['GET'])
def get_car_list():
    car_names = cars.show()
    return jsonify({'cars': car_names})

if __name__ == '__main__':
    app.run(debug=True)
