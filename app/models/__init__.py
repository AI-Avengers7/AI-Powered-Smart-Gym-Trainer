from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Import models so they are recognized when the database is created
from .user_model import User
from .workout_model import Workout
