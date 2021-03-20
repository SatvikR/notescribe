from notescribe import app
from flask import render_template, request
from werkzeug.utils import secure_filename
import os.path
import os

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('no file')
            return render_template('index.html')
        file = request.files['file']
        filename = secure_filename(file.filename)
        if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'])):
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload successful')
        return render_template('index.html')
    return render_template('index.html')
