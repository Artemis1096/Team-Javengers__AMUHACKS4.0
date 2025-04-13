from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import ee
import geemap
from vegetation import  generate_map 
from urbanclassification import urban_map
# Initialize Earth Engine
try:
    ee.Initialize(project='airgreen-javengers')
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project='airgreen-javengers')

app = Flask(__name__)
CORS(app)

@app.route('/map')
def get_map():
    return send_from_directory(directory='.', path='Map.html')

@app.route('/map2')
def get_map2():
    return send_from_directory(directory='.', path='Map2.html')

@app.route('/send-coordinates', methods=['POST'])
def receive_coordinates():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')

    try:
        print(f"Received Coordinates: Latitude = {lat}, Longitude = {lng}")

        # Call the Earth Engine function to generate the map
        output_html = urban_map(lat, lng)

        if output_html:
            return jsonify({'status': 'success', 'map': '/map'})  # Map is ready to fetch
        else:
            return jsonify({'status': 'processing', 'message': 'Map generation failed. Try again later.'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/send-coordinates-vegetation', methods=['POST'])
def receive_coordinates_vegetation():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')

    try:
        print(f"For vegetation - Received Coordinates: Latitude = {lat}, Longitude = {lng}")

        # Call the Earth Engine function to generate the map
        output_html = generate_map(lat, lng)

        if output_html:
            return jsonify({'status': 'success', 'map2': '/map2'})  # Map is ready to fetch
        else:
            return jsonify({'status': 'processing', 'message': 'Map generation failed. Try again later.'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
