from flask import Flask
from config import config  

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config)

   

    return app