from flask import Flask, Response, render_template
from detect import generate_frames  # Assuming generate_frames() function is defined in generate_frames.py
import pandas as pd
import csv
app = Flask(__name__)

attendance_file = 'updated_attendance.csv'
detected_names = set()
# Route for accessing the video stream and taking attendance
@app.route('/')
def index():
    return render_template('index2.html')

# Function to update attendance
def update_attendance(name):
    global detected_names
    if name not in detected_names:
        with open(attendance_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name])
        detected_names.add(name)

# Video streaming route
@app.route('/video_feed')
def video_feed():
    global attendance_df
    return Response(generate_frames(attendance_callback=update_attendance),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for saving attendance to Excel
@app.route('/save_attendance')
def save_attendance():
    return 'Attendance saved successfully!'
if __name__ == '__main__':
    app.run(debug=True)
