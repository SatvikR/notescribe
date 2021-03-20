from notescribe import app
from flask import render_template, request
from werkzeug.utils import secure_filename
import os.path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('no file')
            return render_template('index.html')
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload successful')
        return render_template('index.html')
    return render_template('index.html')
