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
        vertices = list(graph.vertices.keys())
        return render_template('index.html', vertices=vertices)
    return redirect(request.url)

@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    data = request.get_json()
    start = data['start']
    end = data['end']
    file_path = data['file_path']
    graph = read_map(file_path)
    path, distance = dijkstra(graph, start, end)
    return jsonify({'path': path, 'distance': distance})

if __name__ == '__main__':
    app.run(debug=True)
