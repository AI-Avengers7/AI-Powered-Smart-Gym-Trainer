from flask import Flask
from config import Config
from app.models import db 


"""
Factory function to create and configure the Flask application.
"""
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Import models here to ensure they are registered
from app.models.user_model import User
from app.models.workout_model import Workout

with app.app_context():
    db.create_all()
