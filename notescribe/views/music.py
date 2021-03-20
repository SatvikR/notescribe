from notescribe import app
from flask import render_template

@app.route('/music')
def music():
    return render_template('music.html')
