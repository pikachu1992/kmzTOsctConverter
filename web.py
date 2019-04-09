import os
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask import send_file, render_template, request, jsonify
from convert_kmz_to_kml import kmz_to_kml
from convert_geoJson_to_sct import geoJSON_to_sct
import kml2geojson as kg
import json
from flask_cors import CORS

UPLOAD_FOLDER = 'uploads/'
JSON_FOLDER = 'json_files/'
ALLOWED_EXTENSIONS = set(['kmz',])

app = Flask(__name__, template_folder="web")
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_FOLDER'] = JSON_FOLDER
app.secret_key = "super secret key"

def convert(file):
    try:
        fname = "{}".format(file.split('.')[0])
        kmz_to_kml(file)
        kg.convert((app.config['UPLOAD_FOLDER'] + fname + ".kml"), "json_files")
        geoJSON_to_sct((app.config['JSON_FOLDER'] + fname + ".geojson"))

        return return_files_tut("converted/" + fname + ".sct")
    except:
        return json.dumps(["This file have errors"])
        
def return_files_tut(file):
    try:
        with open(file, 'r') as f:
            to_split = f.read().split('\n')
            a = json.dumps(to_split)
            return a  
		#return json.dumps(send_file(file, attachment_filename=file))
    except Exception as e:
        return json.dumps(str(e))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            
            return json.dumps(["No have file insert one file first"])
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return json.dumps(["File extension not allowed. Send only .kmz files"])
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return convert(file.filename)
        else:
            return json.dumps(["File extension not allowed. Send only .kmz files"])



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5006)