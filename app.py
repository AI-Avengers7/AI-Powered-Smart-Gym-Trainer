"""
AI-Powered Smart Gym Trainer
Main application file with Flask server setup and WebSocket handling.
"""
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import base64
import cv2
import numpy as np
import os
from datetime import timedelta

# Import configuration
from config import config

# Import database and models
from app.models import db
from app.models.user_model import User
from app.models.workout_model import Workout

# Import routes
from app.routes.auth_routes import auth_bp
from app.routes.workout import workout_bp, process_frame
from app.routes.analytics_routes import analytics_bp

# Initialize Flask app
app = Flask(
    __name__,
    static_folder=os.path.abspath('app/views/static'),
    template_folder=os.path.abspath('app/views/templates')
)

# Configuration
app.config.from_object(config)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-this')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(workout_bp)
app.register_blueprint(analytics_bp)

# Create database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")


# Main routes
@app.route('/')
def index():
    """Render the main landing page."""
    return render_template('index.html')


@app.route('/routes')
def list_routes():
    """List all available routes for debugging."""
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
        line = f"{rule.endpoint:50s} {methods:20s} {rule.rule}"
        output.append(line)
    
    return '<pre>' + '\n'.join(sorted(output)) + '</pre>'


@app.route('/setup-camera')
def setup_camera():
    """Render camera setup page."""
    return render_template('setup_camera.html')


@app.route('/suggestions')
def suggestions():
    """Render workout suggestions page."""
    return render_template('suggestions.html')


@app.route('/analyze-frame')
def analyze_frame():
    """Render frame analysis page."""
    return render_template('analyze_frame.html')


@app.route('/test-analytics')
def test_analytics():
    """Render analytics test page."""
    return render_template('test_analytics.html')


# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    print(f'Client connected: {request.sid}')
    socketio.emit('connection_response', {
        'status': 'success',
        'message': 'Connected to AI Gym Trainer',
        'session_id': request.sid
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection."""
    print(f'Client disconnected: {request.sid}')


@socketio.on('frame')
def handle_frame(data):
    """
    Handle incoming video frames from the client for real-time pose detection.
    
    Args:
        data: Base64 encoded image data
    """
    user_id = request.sid
    
    try:
        # Decode the base64 image
        if ',' in data:
            header, encoded = data.split(",", 1)
        else:
            encoded = data
            
        binary_data = base64.b64decode(encoded)
        image_array = np.frombuffer(binary_data, dtype=np.uint8)
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        if frame is None:
            print(f"❌ Invalid frame from {user_id}")
            socketio.emit('response', {
                'status': 'error',
                'message': 'Invalid frame data'
            }, room=request.sid)
            return
        
        # Process the frame for pose detection
        count, stage = process_frame(frame, user_id)
        
        # Log every 30th frame to avoid spam
        if count % 5 == 0 or stage == 'up':
            print(f"🏋️ User {user_id}: Count={count}, Stage={stage}")
        
        # Send response back to client
        socketio.emit('response', {
            'status': 'success',
            'count': count,
            'stage': stage
        }, room=request.sid)
        
    except Exception as e:
        print(f"Error processing frame: {e}")
        socketio.emit('response', {
            'status': 'error',
            'message': str(e)
        }, room=request.sid)


@socketio.on('start_workout')
def handle_start_workout(data):
    """Handle workout start event."""
    try:
        exercise = data.get('exercise', 'Bicep Curl')
        user_id = request.sid
        
        print(f"User {user_id} started workout: {exercise}")
        
        socketio.emit('workout_started', {
            'status': 'success',
            'exercise': exercise,
            'message': f'Started {exercise} workout'
        }, room=request.sid)
        
    except Exception as e:
        print(f"Error starting workout: {e}")
        socketio.emit('workout_started', {
            'status': 'error',
            'message': str(e)
        }, room=request.sid)


@socketio.on('stop_workout')
def handle_stop_workout(data):
    """Handle workout stop event."""
    try:
        user_id = request.sid
        
        print(f"User {user_id} stopped workout")
        
        socketio.emit('workout_stopped', {
            'status': 'success',
            'message': 'Workout stopped'
        }, room=request.sid)
        
    except Exception as e:
        print(f"Error stopping workout: {e}")
        socketio.emit('workout_stopped', {
            'status': 'error',
            'message': str(e)
        }, room=request.sid)


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return {"error": "Internal server error"}, 500


# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired JWT tokens."""
    return {"error": "Token has expired"}, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid JWT tokens."""
    return {"error": "Invalid token"}, 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing JWT tokens."""
    return {"error": "Authorization token is missing"}, 401


if __name__ == '__main__':
    # Run the application with SocketIO
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )