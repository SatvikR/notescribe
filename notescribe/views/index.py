from notescribe import app
from notescribe.process import process_file
from flask import render_template, request
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
        file.stream.seek(0)
        # Save file
        filename = f'upload_{file_hash}'
        if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'])):
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']))
        if not os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload successful')
        
        # Process file
        result = process_file(file_hash, filename)
        print(f"Result: {result}")
        return render_template('index.html', message='File processed')
    return render_template('index.html')
