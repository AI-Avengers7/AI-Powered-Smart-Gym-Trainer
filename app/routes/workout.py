"""
Workout Routes
Defines API endpoints for workout operations and real-time pose detection.
"""
from flask import Blueprint, request, jsonify, render_template, session
from app.controllers.workout_controller import WorkoutController
from app.utils.auth import login_required



from app.utils.errors import handle_exceptions



# Create Blueprint

workout_bp = Blueprint('workout', __name__, url_prefix='/workout')



# Store user states for real-time tracking

user_states = {}







@workout_bp.route('/', methods=['GET'])

@login_required

@handle_exceptions

def workout_page():

    """Render workout page."""

    return render_template('workout.html')





@workout_bp.route('/log', methods=['POST'])

@login_required

@handle_exceptions

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





@workout_bp.route('/history', methods=['GET'])

@login_required

@handle_exceptions

def get_workout_history():

    """

    Get workout history for the current user.

    

    Query Parameters:

        limit (optional): Maximum number of workouts to return

    """

    user_id = session.get('user_id')

    limit = request.args.get('limit', type=int)

    

    success, data, status_code = WorkoutController.get_user_workouts(user_id, limit)

    

    if success:

        return jsonify(data), status_code

    else:

        return jsonify(data), status_code





@workout_bp.route('/<int:workout_id>', methods=['GET'])

@login_required

@handle_exceptions

def get_workout(workout_id):

    """Get a specific workout by ID."""

    success, data, status_code = WorkoutController.get_workout_by_id(workout_id)

    

    if success:

        return jsonify(data), status_code

    else:

        return jsonify(data), status_code





@workout_bp.route('/<int:workout_id>', methods=['PUT'])

@login_required

@handle_exceptions

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





@workout_bp.route('/<int:workout_id>', methods=['DELETE'])

@login_required

@handle_exceptions

def delete_workout(workout_id):

    """Delete a workout."""

    success, message, status_code = WorkoutController.delete_workout(workout_id)

    

    if success:

        return jsonify({"message": message}), status_code

    else:

        return jsonify({"error": message}), status_code





@workout_bp.route('/exercise/<string:exercise>', methods=['GET'])

@login_required

@handle_exceptions

def get_workouts_by_exercise(exercise):

    """Get all workouts for a specific exercise."""

    user_id = session.get('user_id')

    success, data, status_code = WorkoutController.get_workouts_by_exercise(user_id, exercise)

    

    if success:

        return jsonify(data), status_code

    else:

        return jsonify(data), status_code





@workout_bp.route('/total-reps', methods=['GET'])

@login_required

@handle_exceptions

def get_total_reps():

    """

    Get total reps for the current user.

    

    Query Parameters:

        exercise (optional): Filter by specific exercise

    """

    user_id = session.get('user_id')

    exercise = request.args.get('exercise')

    

    success, data, status_code = WorkoutController.get_total_reps(user_id, exercise)

    

    if success:

        return jsonify(data), status_code

    else:

        return jsonify(data), status_code





@workout_bp.route('/reset-count', methods=['POST'])

@login_required

@handle_exceptions

def reset_count():

    """Reset the rep count for the current user."""

    user_id = session.get('user_id')

    

    if user_id in user_states:

        user_states[user_id] = {'count': 0, 'stage': ''}

    

    return jsonify({"message": "Count reset successfully"}), 200
