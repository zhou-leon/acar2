from flask import abort
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

# Endpoint to add a new event
@app.route('/add-event', methods=['POST'])
def add_event():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()

    required_fields = [
        "type", "date", "notes", "odometer-reading", "payment-type", "tags", "total-cost",
        "place-name", "place-full-address", "place-street", "place-city", "place-state",
        "place-country", "place-postal-code", "place-google-places-id", "place-longitude",
        "place-latitude", "device-longitude", "device-latitude", "subtypes"
    ]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

    # Validate subtypes
    subtype_keys = [
        "A/C System", "Accident", "Air Filter", "Alternator", "Battery", "Belts", "Body/Chassis",
        "Brake Fluid", "Brakes, Front", "Brakes, Rear", "Cabin Air Filter", "Car Wash",
        "Clutch Hydraulic Fluid", "Clutch Hydraulic System", "Cooling System", "Diesel Exhaust Fluid",
        "Differential Fluid", "Doors", "Engine Antifreeze", "Engine Oil", "Exhaust System", "Fine",
        "Fuel Filter", "Fuel Lines & Pipes", "Fuel Pump", "Fuel System", "Glass/Mirrors",
        "Heating System", "Horns", "Induction", "Inspection", "Insurance", "Lights",
        "Lubricate Chain", "MOT", "New Tires", "Oil Filter", "Parking", "Payment",
        "Power Steering Fluid", "Radiator", "Registration", "Rust Module", "Safety Devices",
        "Spark Plugs", "Steering System", "Suspension System", "Tax", "Timing Belt", "Tire A",
        "Tire B", "Tire C", "Tire D", "Tire Pressure", "Tire Rotation", "Tires", "Toll", "Tow",
        "Transmission Fluid", "Water Pump", "Wheel Alignment", "Windshield Washer Fluid",
        "Windshield Wipers"
    ]
    subtypes = data["subtypes"]
    if not isinstance(subtypes, dict):
        return jsonify({'error': 'subtypes must be a dict of booleans'}), 400
    for k in subtypes:
        if k not in subtype_keys or not isinstance(subtypes[k], bool):
            return jsonify({'error': f'Invalid subtype: {k}'}), 400

    # Here you would save the event to your data store (e.g., XML, DB)
    # For now, just echo back the event
    return jsonify({'status': 'success', 'event': data}), 200

if __name__ == '__main__':
    app.run(debug=True)
