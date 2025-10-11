"""
Analytics Routes
Defines API endpoints for workout analytics and statistics.
"""
from flask import Blueprint, request, jsonify, render_template, session
from app.controllers.analytics_controller import AnalyticsController
from app.controllers.workout_controller import WorkoutController
from functools import wraps

# Create Blueprint
analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')


def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function


@analytics_bp.route('/', methods=['GET'])
def analytics_page():
    """Render analytics page."""
    return render_template('analytics.html')


@analytics_bp.route('/summary', methods=['GET'])
def get_summary():
    """
    Get overall workout summary for the current user.
    
    Returns summary including:
    - Total workouts
    - Total reps
    - Total sets
    - Exercises performed
    """
    try:
        user_id = session.get('user_id') or 1  # Default to user 1 for demo
        
        # Return mock data if no user_id
        if not user_id:
            return jsonify({
                "total_workouts": 0,
                "total_reps": 0,
                "total_sets": 0,
                "week_workouts": 0,
                "streak_days": 0,
                "exercises_performed": 0,
                "exercises": []
            }), 200
        
        success, data, status_code = AnalyticsController.get_workout_summary(user_id)
        
        # Add additional stats
        if success and isinstance(data, dict):
            data['week_workouts'] = 0  # TODO: Calculate from date range
            data['streak_days'] = 0    # TODO: Calculate streak
        
        if success:
            return jsonify(data), status_code
        else:
            return jsonify(data), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to get summary: {str(e)}"}), 500


@analytics_bp.route('/breakdown', methods=['GET'])
def get_breakdown():
    """
    Get workout breakdown by exercise type.
    
    Returns breakdown for each exercise:
    - Workout count
    - Total reps
    - Total sets
    - Average reps per workout
    """
    try:
        user_id = session.get('user_id') or 1  # Default to user 1 for demo
        
        # Return empty breakdown if no user_id
        if not user_id:
            return jsonify({}), 200
        
        success, data, status_code = AnalyticsController.get_exercise_breakdown(user_id)
        
        if success:
            return jsonify(data), status_code
        else:
            return jsonify(data), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to get breakdown: {str(e)}"}), 500


@analytics_bp.route('/progress/<string:exercise>', methods=['GET'])
@login_required
def get_progress(exercise):
    """
    Get progress data for a specific exercise.
    
    Args:
        exercise: Name of the exercise
        
    Returns progress over time with session numbers and reps.
    """
    try:
        user_id = session.get('user_id')
        success, data, status_code = AnalyticsController.get_progress_data(user_id, exercise)
        
        if success:
            return jsonify(data), status_code
        else:
            return jsonify(data), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to get progress: {str(e)}"}), 500


@analytics_bp.route('/recent', methods=['GET'])
def get_recent():
    """
    Get recent workout activity.
    
    Query Parameters:
        limit (optional): Number of recent workouts to return (default: 10)
    """
    try:
        user_id = session.get('user_id') or 1  # Default to user 1 for demo
        limit = request.args.get('limit', 10, type=int)
        
        # Return empty array if no user_id
        if not user_id:
            return jsonify([]), 200
        
        success, data, status_code = AnalyticsController.get_recent_activity(user_id, limit)
        
        if success:
            return jsonify(data), status_code
        else:
            return jsonify(data), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to get recent activity: {str(e)}"}), 500


@analytics_bp.route('/records', methods=['GET'])
def get_records():
    """
    Get personal records for each exercise.
    
    Returns max reps, max sets, and max total reps for each exercise.
    """
    try:
        user_id = session.get('user_id') or 1  # Default to user 1 for demo
        
        # Return empty object if no user_id
        if not user_id:
            return jsonify({}), 200
        
        success, data, status_code = AnalyticsController.get_personal_records(user_id)
        
        if success:
            return jsonify(data), status_code
        else:
            return jsonify(data), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to get records: {str(e)}"}), 500


@analytics_bp.route('/exercise/<string:exercise>/stats', methods=['GET'])
@login_required
def get_exercise_stats(exercise):
    """
    Get detailed statistics for a specific exercise.
    
    Args:
        exercise: Name of the exercise
        
    Returns detailed stats including averages, totals, and maximums.
    """
    try:
        user_id = session.get('user_id')
        success, data, status_code = AnalyticsController.get_workout_stats_by_exercise(
            user_id, exercise
        )
        
        if success:
            return jsonify(data), status_code
        else:
            return jsonify(data), status_code
            
    except Exception as e:
        return jsonify({"error": f"Failed to get exercise stats: {str(e)}"}), 500


@analytics_bp.route('/history', methods=['GET'])
@login_required
def get_history():
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
        return jsonify({"error": f"Failed to get history: {str(e)}"}), 500


@analytics_bp.route('/history_page', methods=['GET'])
@login_required
def history_page():
    """Render workout history page."""
    return render_template('workout_history.html')
