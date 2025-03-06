from flask import Flask
from config import config  
<<<<<<< HEAD
=======
from app.routes.workout_routes import workout_bp
>>>>>>> 77ecdac7081f6991586675f1bb2d4d743cfd89a8

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
<<<<<<< HEAD
    app = Flask(__name__)
=======

    app = Flask(__name__, template_folder='app/views/templates', static_folder="views/static")

>>>>>>> 77ecdac7081f6991586675f1bb2d4d743cfd89a8

    # Load configuration
    app.config.from_object(config)

<<<<<<< HEAD
=======
    app.register_blueprint(workout_bp, url_prefix='/workout')
>>>>>>> 77ecdac7081f6991586675f1bb2d4d743cfd89a8
   

    return app