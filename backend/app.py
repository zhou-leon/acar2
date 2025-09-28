# Imports
import os
from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import sys
sys.path.append('../struct')
import vehicles
import utils
import urllib.parse

app = Flask(__name__)

cars = vehicles.Vehicles()

# Endpoint to get list of car names
@app.route('/car-list', methods=['GET'])
def get_car_list():
    car_names = cars.show()
    return jsonify({'cars': car_names})

# Endpoint to get info for a vehicle when name is given as an argument
@app.route('/car-info', methods=['GET'])
def get_car_info():
    car_name = request.args.get('name')
    if not car_name:
        return jsonify({'error': 'Missing car name'}), 400
    car_name = urllib.parse.unquote(car_name)
    car_struct = cars.find(car_name)
    if car_struct is not None:
        info = cars.get_info(car_name)
        return jsonify({'info': info})
    return jsonify({'info': ''})


# Endpoint to get event report text for a vehicle by name
@app.route('/event-report', methods=['GET'])
def get_event_report():
    car_name = request.args.get('name')
    if not car_name:
        return jsonify({'error': 'Missing car name'}), 400
    car_name = urllib.parse.unquote(car_name)
    car_struct = cars.find(car_name)
    if car_struct is not None:
        report = utils.gen_report(car_name)
        return jsonify({'report': report})
    return jsonify({'report': ''})

if __name__ == '__main__':
    app.run(debug=True)
