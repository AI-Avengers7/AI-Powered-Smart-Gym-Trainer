"""
Authentication Routes
Defines API endpoints for user authentication.
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from app.controllers.auth_controller import AuthController
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup_page():
    """
    Handle signup page rendering (GET) and registration (POST).
    """
    if request.method == 'GET':
        # Render signup page
        return render_template('signup.html')
    
    # Handle POST request (registration)
    try:
        data = request.get_json() or request.form.to_dict()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        success, message, status_code = AuthController.register_user(name, email, password)
        
        if success:
            return jsonify({"message": message}), status_code
        else:
            return jsonify({"error": message}), status_code
            
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500


@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Handle login page rendering (GET) and login submission (POST).
    """
    if request.method == 'GET':
        # Render login page
        return render_template('login.html')
    
    # Handle POST request (login submission)
    try:
        data = request.get_json() or request.form.to_dict()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        success, response, status_code = AuthController.login_user(email, password)
        
        if success:
            # Store user info in session for web pages
            session['user_id'] = response.get('user_id')
            session['email'] = email
            return jsonify(response), status_code
        else:
            return jsonify(response), status_code
            
    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Expected JSON:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        success, message, status_code = AuthController.register_user(name, email, password)
        
        if success:
            return jsonify({"message": message}), status_code
        else:
            return jsonify({"error": message}), status_code
            
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500


@auth_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    """Logout user."""
    try:
        success, message, status_code = AuthController.logout_user()
        
        if success:
            return jsonify({"message": message}), status_code
        else:
            return jsonify({"error": message}), status_code
            
    except Exception as e:
        return jsonify({"error": f"Logout failed: {str(e)}"}), 500


@auth_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required(optional=True)
def get_user(user_id):
    """Get user information by ID."""
    try:
        success, data, status_code = AuthController.get_user_by_id(user_id)
        
        if success:
            return jsonify(data), status_code
        else:
            return jsonify(data), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to get user: {str(e)}"}), 500


@auth_bp.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Update user information.
    
    Expected JSON (all fields optional):
    {
        "name": "New Name",
        "email": "newemail@example.com",
        "password": "newpassword123"
    }
    """
    try:
        # Verify the user is updating their own account
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        data = request.get_json()
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        success, message, status_code = AuthController.update_user(
            user_id, name, email, password
        )
        
        if success:
            return jsonify({"message": message}), status_code
        else:
            return jsonify({"error": message}), status_code
            
    except Exception as e:
        return jsonify({"error": f"Update failed: {str(e)}"}), 500


@auth_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete user account."""
    try:
        # Verify the user is deleting their own account
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        success, message, status_code = AuthController.delete_user(user_id)
        
        if success:
            return jsonify({"message": message}), status_code
        else:
            return jsonify({"error": message}), status_code
            
    except Exception as e:
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500


@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """Get current user profile."""
    try:
        user_id = session.get('user_id')
        success, data, status_code = AuthController.get_user_by_id(user_id)
        
        if success:
            return jsonify(data), status_code
        else:
            return jsonify(data), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to get profile: {str(e)}"}), 500
