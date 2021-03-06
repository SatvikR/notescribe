import json
from flask import Flask
import os.path

UPLOAD_FOLDER = os.path.join('object_storage', 'uploads')
WAV_FOLDER = os.path.join('object_storage', 'wav')
MIDI_FOLDER = os.path.join('object_storage', 'midi')
LILYPOND_FOLDER = os.path.join('object_storage', 'lilypond')
IMAGES_FOLDER = os.path.join('object_storage', 'images')
PDF_FOLDER = os.path.join('object_storage', 'pdf')
JSON_FOLDER = os.path.join('object_storage', 'json')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

settings = None
with open(os.path.join('settings.json')) as f:
   settings = json.load(f) 

from notescribe.views import *
