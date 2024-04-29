from flask import Flask, render_template, request, url_for, redirect, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user
from detect import generate_frames
import csv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

db.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

# Initialize video feed flag
video_feed_active = False

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                    password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/class')
def class_page():
    return render_template('class.html')

@app.route('/video_feed')
def video_feed():
    # Check if the video feed is active before generating frames
    if video_feed_active:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Video feed is not active."

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("class_page")) 
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route("/start_feed")
def start_feed():
    global video_feed_active
    video_feed_active = True
    return redirect(url_for("index"))  # Redirect to the page with video feed

@app.route("/stop_feed")
def stop_feed():
    global video_feed_active
    video_feed_active = False
    return redirect(url_for("process_names"))  # Redirect to process the recognized names

@app.route("/process_names")
def process_names():
    class_presence = {}  # Initialize an empty dictionary
    try:
        # Loop over frames to get the latest class presence information
        for frame in generate_frames():
            pass  # This loop will execute until the generator stops
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Process the class presence information for attendance
    recognized_names = [class_name for class_name, presence in class_presence.items() if presence == 1]
    # Load the predefined CSV file
    with open("predefined_attendance.csv", mode='r') as file:
        csv_reader = csv.DictReader(file)
        lines = list(csv_reader)
        fieldnames = csv_reader.fieldnames

    # Update attendance status based on recognized names
    for line in lines:
        # Check if 'name' key exists in the current row
        if 'name' in line:
            # Check if the name is in recognized_names list
            if line['name'] in recognized_names:
                line['attendance'] = 'Present'
            else:
                line['attendance'] = 'Absent'
        else:
            # Handle case where 'name' key is missing in the row
            line['attendance'] = 'Unknown'

    # Write updated attendance to a new CSV file
    with open("updated_attendance.csv", mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lines)

    return "Attendance processed and updated in CSV file."

@app.route("/download_attendance")
def download_attendance():
    return send_file("updated_attendance.csv", as_attachment=True)

if __name__ == "__main__":
    app.run()
