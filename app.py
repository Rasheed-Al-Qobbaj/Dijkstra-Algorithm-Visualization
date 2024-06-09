from flask import Flask, request, render_template, redirect, url_for, jsonify
from Util import *
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        graph = read_map(file_path)
        # vertices = list(graph.vertices.items())


        # World map image dimensions
        map_width = 1200  # width of the image in pixels
        map_height = 715  # height of the image in pixels

        # Correction factors (derived from manual adjustments)
        x_scale_factor = 0.92  # Adjust this based on the observed shift
        y_scale_factor = 0.9  # Adjust this based on the observed shift
        x_offset = -30  # Adjust this based on the observed shift
        y_offset = 100  # Adjust this based on the observed shift

        # Convert the lat and lon coordinates to x and y coordinates
        converted_vertices = {}
        for country, (lat, lon) in graph.vertices.items():
            # Calculate x and y with respect to the image dimensions
            x = (((lon + 180) / 360) * map_width * x_scale_factor) + x_offset
            y = (((90 - lat) / 180) * map_height * y_scale_factor) + y_offset
            converted_vertices[country] = (x, y)

        vertices = list(converted_vertices.items())

        return render_template('algorithm.html', vertices=vertices, file_path=file_path, path=None, distance=None)
    return redirect(request.url)

@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    start = request.form['start']
    end = request.form['end']
    file_path = request.form['file_path']
    graph = read_map(file_path)
    path, distance = dijkstra(graph, start, end)
    # vertices = list(graph.vertices.items())


    # World map image dimensions
    map_width = 1200  # width of the image in pixels
    map_height = 715  # height of the image in pixels

    # Correction factors (derived from manual adjustments)
    x_scale_factor = 0.92  # Adjust this based on the observed shift
    y_scale_factor = 0.9  # Adjust this based on the observed shift
    x_offset = -30  # Adjust this based on the observed shift
    y_offset = 100  # Adjust this based on the observed shift

    # Convert the lat and lon coordinates to x and y coordinates
    converted_vertices = {}
    for country, (lat, lon) in graph.vertices.items():
        # Calculate x and y with respect to the image dimensions
        x = (((lon + 180) / 360) * map_width * x_scale_factor) + x_offset
        y = (((90 - lat) / 180) * map_height * y_scale_factor) + y_offset
        converted_vertices[country] = (x, y)

    vertices = list(converted_vertices.items())

    return render_template('algorithm.html', vertices=vertices, file_path=file_path, path=path, distance=round(distance, 2))

if __name__ == '__main__':
    app.run(debug=True)
