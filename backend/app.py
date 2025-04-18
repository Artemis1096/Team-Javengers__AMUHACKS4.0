import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import ee
import geemap
from vegetation import  generate_map 
from urbanclassification import urban_map
from aqi_data import get_aqi_insight
from dotenv import load_dotenv
from colorclassification import get_color_class
 
load_dotenv()
# Initialize Earth Engine
ProjectName = os.getenv("PROJECT_NAME")
try:
    ee.Initialize(project=ProjectName)
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project=ProjectName)

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

@app.route('/send-coordinates-aqi', methods=['POST'])
def receive_coordinates_aqi():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')

    try:
        lat = float(lat)
        lng = float(lng)
        print(f"For AQI - Received Coordinates: Latitude = {lat}, Longitude = {lng}")

        result = get_aqi_insight(lat, lng)

        if 'error' not in result:
            return jsonify({
                'status': 'success',
                'city': result['city'],
                'aqi': result['aqi'],
                'insight': result['insight']
            })
        else:
            return jsonify({
                'status': 'error',
                'message': result['error']
            })

    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid latitude or longitude.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
@app.route('/calculate_percentages', methods=['GET'])
def get_percentages():
    percentages = get_color_class()
    return percentages

@app.route('/get-vegetation-timeseries', methods=['POST'])
def get_vegetation_timeseries():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')
    start_date = data.get('start_date')  # format: 'YYYY-MM-DD'
    end_date = data.get('end_date')      # format: 'YYYY-MM-DD'

    try:
        point = ee.Geometry.Point([float(lng), float(lat)])

        # Use Sentinel-2 Surface Reflectance dataset
        collection = (
            ee.ImageCollection('COPERNICUS/S2_SR')
            .filterBounds(point)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
            .map(lambda image: image
                 .normalizedDifference(['B8', 'B4'])
                 .rename('NDVI')
                 .copyProperties(image, ['system:time_start']))
        )

        def extract_ndvi(image):
            mean = image.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point,
                scale=10,
                maxPixels=1e9
            )
            return ee.Feature(None, {
                'date': ee.Date(image.get('system:time_start')).format('YYYY-MM-dd'),
                'NDVI': mean.get('NDVI')
            })

        features = collection.map(extract_ndvi).aggregate_array('properties').getInfo()

        return jsonify({'status': 'success', 'data': features})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
