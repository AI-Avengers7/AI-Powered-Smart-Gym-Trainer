from flask import Flask
from config import config  

def create_app():
    """
    Factory function to create and configure the Flask application.
    """

    app = Flask(__name__, template_folder='/app/views/templates', static_folder="views/static")
    app.secret_key = "vdsvfdvdfgvfdvdsvgrsvg"

    # Load configuration
    app.config.from_object(config)


   

    return app
