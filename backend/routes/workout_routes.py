from flask import Flask, render_template

app = Flask(__name__)

#route for the main page to start workout
@app.route("/")
def start_workout():
    return render_template("index.html")

#processes frame data for pose detection(route to analyze pose/frame)
@app.route("/analyze-frame", methods=["POST"])
def analyze_frame():
    return render_template("analyze_frame.html")

#route to log the workout/ stores workout data
@app.route("/log-workout", methods=["POST"])
def log_workout():
    return render_template("workout_logged.html")

#route to show the user's workout history
@app.route("/workout-history")
def show_workout_history():
    return render_template("workout_history.html")

#route to show the workout suggestions based on their data
@app.route("/suggestions")
def suggestions():
    return render_template("suggestions.html")

#route to show workout progress and stats
@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

#route to set up the camera for pose detection
@app.route("/setup-camera", methods=["POST"])
def setup_camera():
    return render_template("setup_camera.html")


if __name__ == "__main__":
    app.run(debug=True)