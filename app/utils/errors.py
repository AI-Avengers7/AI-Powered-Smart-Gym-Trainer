"""
Error Handling Utilities
"""
from functools import wraps
from flask import jsonify

def handle_exceptions(f):
    """Decorator to handle exceptions in routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    return decorated_function
