from flask import Flask
from app.models import db  # Import db from app/models/__init__.py
from app.models.user_model import User
from app.models.workout_model import Workout
from config import Config

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from config.py

# Initialize database
db.init_app(app)

# Create database tables before the first request
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

