from notescribe import app
from notescribe.process import process_file
from flask import render_template, request
from werkzeug.utils import secure_filename
import hashlib
import os.path
import os

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Normal webpage access
        if 'file' not in request.files:
            print('no file')
            return render_template('index.html')

        # If user uploaded file
        file = request.files['file']
        
        # Calculate SHA-1 hash of file
        file.stream.seek(0)
        data = file.stream.read()
        file_hash = hashlib.sha1(data).hexdigest()

        # Save file
        filename = f'upload_{file_hash}'
        if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'])):
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload successful')
        
        # Process file
        result = process_file(file_hash, filename)
        print('successfully processed file' if result else 'failed to process file')
        return render_template('index.html', message='File processed')
    return render_template('index.html')
