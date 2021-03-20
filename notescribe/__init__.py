import json
from flask import Flask
import os.path

UPLOAD_FOLDER = './object_storage/uploads'
MIDI_FOLDER = './object_storage/midi'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

settings = None
with open(os.path.join('settings.json')) as f:
   settings = json.load(f) 

from notescribe.views import *
