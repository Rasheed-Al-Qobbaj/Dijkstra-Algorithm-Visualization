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
        # Assume these are the dimensions of #map-container in your CSS
        container_width = 1960
        container_height = 700

        # Scale the coordinates
        scaled_vertices = {}
        for country, (original_x, original_y) in graph.vertices.items():
            scaled_x = (original_x / 8800) * container_width
            scaled_y = (original_y / 3800) * container_height
            scaled_vertices[country] = (scaled_x, scaled_y)

        vertices = list(scaled_vertices.items())
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
    # Assume these are the dimensions of #map-container in your CSS
    container_width = 1960
    container_height = 700

    # Scale the coordinates
    scaled_vertices = {}
    for country, (original_x, original_y) in graph.vertices.items():
        scaled_x = (original_x / 8800) * container_width
        scaled_y = (original_y / 3800) * container_height
        scaled_vertices[country] = (scaled_x, scaled_y)

    vertices = list(scaled_vertices.items())
    return render_template('algorithm.html', vertices=vertices, file_path=file_path, path=path, distance=distance)

if __name__ == '__main__':
    app.run(debug=True)
