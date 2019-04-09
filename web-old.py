import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_file, render_template
from convert_kmz_to_kml import kmz_to_kml
from convert_geoJson_to_sct import geoJSON_to_sct
import kml2geojson as kg

UPLOAD_FOLDER = 'uploads/'
JSON_FOLDER = 'json_files/'
ALLOWED_EXTENSIONS = set(['kmz',])

app = Flask(__name__, template_folder="web")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_FOLDER'] = JSON_FOLDER

def convert(file):
    fname = "{}".format(file.split('.')[0])
    kmz_to_kml(file)
    kg.convert((app.config['UPLOAD_FOLDER'] + fname + ".kml"), "json_files")
    geoJSON_to_sct((app.config['JSON_FOLDER'] + fname + ".geojson"))

    return return_files_tut("converted/" + fname + ".sct")

def return_files_tut(file):
	try:     
		return send_file(file, attachment_filename=file)
	except Exception as e:
		return str(e)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return convert(file.filename)
        else:
            return "File extension not allowed. Send only .kmz files"

    return render_template('kmztosct_converter.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0")