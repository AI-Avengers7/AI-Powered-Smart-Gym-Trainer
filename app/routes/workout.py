"""
Workout Routes
Defines API endpoints for workout operations and real-time pose detection.
"""
from flask import Blueprint, request, jsonify, render_template, session
import cv2
import numpy as np
from app.utils.pose_utils import detect_pose, bicep_curl
from app.controllers.workout_controller import WorkoutController
from functools import wraps

# Create Blueprint
workout_bp = Blueprint('workout', __name__, url_prefix='/workout')

# Store user states for real-time tracking
user_states = {}


def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function


def process_frame(frame, user_id):
    """
    Process a frame to detect bicep curls and update the user's state.
    
    Args:
        frame: Video frame to process
        user_id: ID of the user
        
    Returns:
        tuple: (count, stage)
    """
    # Initialize user state if it doesn't exist
    if user_id not in user_states:
        user_states[user_id] = {'count': 0, 'stage': ''}

    # Get the user's state
    state = user_states[user_id]

    # Check if the frame is valid
    if frame is None:
        return state['count'], state['stage']

    # Detect landmarks
    landmarks = detect_pose(frame)

    # Check if landmarks are detected
    if landmarks is None:
        return state['count'], state['stage']

    # Calculate bicep curl angles
    r_angle, l_angle = bicep_curl(landmarks)

    # Check if angles are valid
    if l_angle is None or r_angle is None:
        return state['count'], state['stage']

    # Update stage and count
    if r_angle > 160 or l_angle > 160:
        state['stage'] = 'down'
    if r_angle < 30 and state['stage'] == 'down':
        state['stage'] = 'up'
        state['count'] += 1

    return state['count'], state['stage']


@workout_bp.route('/', methods=['GET'])
@login_required
def workout_page():
    """Render workout page."""
    return render_template('workout.html')


@workout_bp.route('/log', methods=['POST'])
@login_required
def log_workout():
    """
    Log a new workout.
    
    Expected JSON:
    {
        "exercise": "Bicep Curl",
        "reps": 10,
        "sets": 3
    }
    """
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        exercise = data.get('exercise')
        reps = data.get('reps')
        sets = data.get('sets')
        feedback = data.get('feedback')
        
        success, response, status_code = WorkoutController.log_workout(
            user_id, exercise, reps, sets, feedback
        )
        
        if success:
            return jsonify(response), status_code
        else:
            return jsonify({"error": response}), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to log workout: {str(e)}"}), 500


@workout_bp.route('/history', methods=['GET'])
@login_required
def get_workout_history():
    """
    Get workout history for the current user.
    
    Query Parameters:
        limit (optional): Maximum number of workouts to return
    """
    try:
        user_id = session.get('user_id')
        limit = request.args.get('limit', type=int)
        
        success, data, status_code = WorkoutController.get_user_workouts(user_id, limit)
        
        if success:
            return jsonify(data), status_code
        else:
            return jsonify(data), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to get workout history: {str(e)}"}), 500


@workout_bp.route('/<int:workout_id>', methods=['GET'])
@login_required
def get_workout(workout_id):
    """Get a specific workout by ID."""
    try:
        success, data, status_code = WorkoutController.get_workout_by_id(workout_id)
        
        if success:
            return jsonify(data), status_code
        else:
            return jsonify(data), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to get workout: {str(e)}"}), 500


@workout_bp.route('/<int:workout_id>', methods=['PUT'])
@login_required
def update_workout(workout_id):
    """
    Update a workout.
    
    Expected JSON (all fields optional):
    {
        "exercise": "Push Up",
        "reps": 15,
        "sets": 4
    }
    """
    try:
        data = request.get_json()
        
        exercise = data.get('exercise')
        reps = data.get('reps')
        sets = data.get('sets')
        
        success, message, status_code = WorkoutController.update_workout(
            workout_id, exercise, reps, sets
        )
        
        if success:
            return jsonify({"message": message}), status_code
        else:
            return jsonify({"error": message}), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to update workout: {str(e)}"}), 500


@workout_bp.route('/<int:workout_id>', methods=['DELETE'])
@login_required
def delete_workout(workout_id):
    """Delete a workout."""
    try:
        success, message, status_code = WorkoutController.delete_workout(workout_id)
        
        if success:
            return jsonify({"message": message}), status_code
        else:
            return jsonify({"error": message}), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to delete workout: {str(e)}"}), 500


@workout_bp.route('/exercise/<string:exercise>', methods=['GET'])
@login_required
def get_workouts_by_exercise(exercise):
    """Get all workouts for a specific exercise."""
    try:
        user_id = session.get('user_id')
        success, data, status_code = WorkoutController.get_workouts_by_exercise(user_id, exercise)
        
        if success:
            return jsonify(data), status_code
        else:
            return jsonify(data), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to get workouts: {str(e)}"}), 500


@workout_bp.route('/total-reps', methods=['GET'])
@login_required
def get_total_reps():
    """
    Get total reps for the current user.
    
    Query Parameters:
        exercise (optional): Filter by specific exercise
    """
    try:
        user_id = session.get('user_id')
        exercise = request.args.get('exercise')
        
        success, data, status_code = WorkoutController.get_total_reps(user_id, exercise)
        
        if success:
            return jsonify(data), status_code
        else:
            return jsonify(data), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to get total reps: {str(e)}"}), 500


@workout_bp.route('/reset-count', methods=['POST'])
@login_required
def reset_count():
    """Reset the rep count for the current user."""
    try:
        user_id = session.get('user_id')
        
        if user_id in user_states:
            user_states[user_id] = {'count': 0, 'stage': ''}
        
        return jsonify({"message": "Count reset successfully"}), 200
            
    except Exception as e:
        return jsonify({"error": f"Failed to reset count: {str(e)}"}), 500