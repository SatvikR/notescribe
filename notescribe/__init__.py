from flask import Flask

app = Flask(__name__)

from notescribe.views import *
