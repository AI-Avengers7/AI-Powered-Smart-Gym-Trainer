"""
Authentication Controller
Handles user registration, login, and authentication logic.
"""
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models import db
from app.models.user_model import User
from datetime import timedelta


class AuthController:
    """Controller for authentication operations."""
    
    @staticmethod
    def register_user(name, email, password):
        """
        Register a new user.
        
        Args:
            name: User's name
            email: User's email
            password: User's password
            
        Returns:
            tuple: (success: bool, message: str, status_code: int)
        """
        try:
            # Validate input
            if not name or not email or not password:
                return False, "All fields are required", 400
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return False, "Email already registered", 409
            
            # Hash the password
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            
            # Create new user
            new_user = User(
                name=name,
                email=email,
                password=hashed_password
            )
            
            # Add to database
            db.session.add(new_user)
            db.session.commit()
            
            return True, "User registered successfully", 201
            
        except Exception as e:
            db.session.rollback()
            return False, f"Registration failed: {str(e)}", 500
    
    @staticmethod
    def login_user(email, password):
        """
        Authenticate user login.
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            tuple: (success: bool, data: dict, status_code: int)
        """
        try:
            # Validate input
            if not email or not password:
                return False, {"message": "Email and password are required"}, 400
            
            # Find user by email
            user = User.query.filter_by(email=email).first()
            
            if not user:
                return False, {"message": "Invalid email or password"}, 401
            
            # Check password
            if not check_password_hash(user.password, password):
                return False, {"message": "Invalid email or password"}, 401
            
            # Create JWT tokens
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(hours=1)
            )
            refresh_token = create_refresh_token(
                identity=user.id,
                expires_delta=timedelta(days=30)
            )
            
            # Store user ID in session
            session['user_id'] = user.id
            session['user_name'] = user.name
            
            return True, {
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                },
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
            
        except Exception as e:
            return False, {"message": f"Login failed: {str(e)}"}, 500
    
    @staticmethod
    def logout_user():
        """
        Logout user by clearing session.
        
        Returns:
            tuple: (success: bool, message: str, status_code: int)
        """
        try:
            session.clear()
            return True, "Logout successful", 200
        except Exception as e:
            return False, f"Logout failed: {str(e)}", 500
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user information by ID.
        
        Args:
            user_id: User's ID
            
        Returns:
            tuple: (success: bool, data: dict, status_code: int)
        """
        try:
            user = User.query.get(user_id)
            
            if not user:
                return False, {"message": "User not found"}, 404
            
            return True, {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }, 200
            
        except Exception as e:
            return False, {"message": f"Error fetching user: {str(e)}"}, 500
    
    @staticmethod
    def update_user(user_id, name=None, email=None, password=None):
        """
        Update user information.
        
        Args:
            user_id: User's ID
            name: New name (optional)
            email: New email (optional)
            password: New password (optional)
            
        Returns:
            tuple: (success: bool, message: str, status_code: int)
        """
        try:
            user = User.query.get(user_id)
            
            if not user:
                return False, "User not found", 404
            
            # Update fields if provided
            if name:
                user.name = name
            
            if email:
                # Check if email is already taken by another user
                existing_user = User.query.filter_by(email=email).first()
                if existing_user and existing_user.id != user_id:
                    return False, "Email already in use", 409
                user.email = email
            
            if password:
                user.password = generate_password_hash(password, method='pbkdf2:sha256')
            
            db.session.commit()
            
            return True, "User updated successfully", 200
            
        except Exception as e:
            db.session.rollback()
            return False, f"Update failed: {str(e)}", 500
    
    @staticmethod
    def delete_user(user_id):
        """
        Delete a user account.
        
        Args:
            user_id: User's ID
            
        Returns:
            tuple: (success: bool, message: str, status_code: int)
        """
        try:
            user = User.query.get(user_id)
            
            if not user:
                return False, "User not found", 404
            
            db.session.delete(user)
            db.session.commit()
            
            return True, "User deleted successfully", 200
            
        except Exception as e:
            db.session.rollback()
            return False, f"Delete failed: {str(e)}", 500
