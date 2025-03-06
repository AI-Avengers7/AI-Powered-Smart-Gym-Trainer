from flask import Flask
from config import config  

from app.routes.workout_routes import workout_bp


def create_app():
    """
    Factory function to create and configure the Flask application.
    """

    app = Flask(__name__, template_folder='app/views/templates', static_folder="views/static")


    # Load configuration
    app.config.from_object(config)

    app.register_blueprint(workout_bp, url_prefix='/workout')

   

    return app
