from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import imutils
import time
import pickle
import numpy as np
from imutils.video import VideoStream
from imutils.video import FPS
from detect import generate_frames

app = Flask(__name__)

# Sample hardcoded username and password for demonstration purposes
VALID_USERNAME = "user"
VALID_PASSWORD = "pass"

def check_credentials(username, password):
    return username == VALID_USERNAME and password == VALID_PASSWORD

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            # If credentials are correct, redirect to class page
            return redirect(url_for('class_page'))
        else:
            error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/class')
def class_page():
    return render_template('class.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
