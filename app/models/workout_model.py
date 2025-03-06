from app.models import db  # Import db from app/models/__init__.py

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(100), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to users table

    def __repr__(self):
        return f'<Workout {self.exercise} - {self.reps} reps>'


