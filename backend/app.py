from flask import Flask, request, jsonify
import sys
sys.path.append('../access')
import vehicles
import utils
import urllib.parse

app = Flask(__name__)

cars = vehicles.Vehicles()

"""Endpoint to add a new vehicle. Accepts JSON payload with car attributes and saves to XML."""
@app.route('/add-car', methods=['POST'])
def add_car():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()
    car_name = data.get('name')
    if not car_name:
        return jsonify({'error': 'Missing car name (name)'}), 400
    attrdic = dict(data)
    attrdic.pop('name', None)
    try:
        cars.addcar(car_name, attrdic)
        cars.save()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

"""Endpoint to get list of car names. Returns all vehicle names in the database."""
@app.route('/car-list', methods=['GET'])
def get_car_list():
    car_names = cars.show()
    return jsonify({'cars': car_names})

"""Endpoint to get info for a vehicle. Requires car name as query argument."""
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


"""Endpoint to get event report text for a vehicle by name. Returns formatted report."""
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

"""Endpoint to add a new event for a vehicle. Accepts JSON payload with event details."""
@app.route('/add-event', methods=['POST'])
def add_event():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()

    # ...existing code...

    # Save the event using utils.add_record()
    car_name = data.get('car-name') or data.get('car') or None
    if not car_name:
        return jsonify({'error': 'Missing car name (car-name or car)'}), 400
    event_dic = dict(data)
    event_dic.pop('car-name', None)
    event_dic.pop('car', None)
    try:
        utils.add_record(car_name, event_dic)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Start the Flask development server
    app.run(debug=True)
