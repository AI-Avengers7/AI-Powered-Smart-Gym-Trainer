"""
Workout Controller
Handles workout logging, retrieval, and management operations.
"""
from flask import jsonify
from app.models import db
from app.models.workout_model import Workout
from app.models.user_model import User
from datetime import datetime


class WorkoutController:
    """Controller for workout operations."""
    
    @staticmethod
    def log_workout(user_id, exercise, reps, sets, feedback=None):
        """
        Log a new workout session.
        
        Args:
            user_id: ID of the user
            exercise: Name of the exercise
            reps: Number of repetitions
            sets: Number of sets
            feedback: Optional feedback/corrections
            
        Returns:
            tuple: (success: bool, message/data: str/dict, status_code: int)
        """
        try:
            # Validate input
            if not user_id or not exercise or reps is None or sets is None:
                return False, "Missing required fields", 400
            
            # Verify user exists
            user = User.query.get(user_id)
            if not user:
                return False, "User not found", 404
            
            # Create new workout entry
            new_workout = Workout(
                exercise=exercise,
                reps=reps,
                sets=sets,
                user_id=user_id
            )
            
            db.session.add(new_workout)
            db.session.commit()
            
            return True, {
                "message": "Workout logged successfully",
                "workout": {
                    "id": new_workout.id,
                    "exercise": new_workout.exercise,
                    "reps": new_workout.reps,
                    "sets": new_workout.sets
                }
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to log workout: {str(e)}", 500
    
    @staticmethod
    def get_user_workouts(user_id, limit=None):
        """
        Get all workouts for a specific user.
        
        Args:
            user_id: ID of the user
            limit: Optional limit on number of workouts to return
            
        Returns:
            tuple: (success: bool, data: dict, status_code: int)
        """
        try:
            # Verify user exists
            user = User.query.get(user_id)
            if not user:
                return False, {"message": "User not found"}, 404
            
            # Query workouts
            query = Workout.query.filter_by(user_id=user_id).order_by(Workout.id.desc())
            
            if limit:
                query = query.limit(limit)
            
            workouts = query.all()
            
            # Format workout data
            workout_list = [
                {
                    "id": workout.id,
                    "exercise": workout.exercise,
                    "reps": workout.reps,
                    "sets": workout.sets,
                    "user_id": workout.user_id
                }
                for workout in workouts
            ]
            
            return True, {
                "workouts": workout_list,
                "count": len(workout_list)
            }, 200
            
        except Exception as e:
            return False, {"message": f"Failed to retrieve workouts: {str(e)}"}, 500
    
    @staticmethod
    def get_workout_by_id(workout_id):
        """
        Get a specific workout by ID.
        
        Args:
            workout_id: ID of the workout
            
        Returns:
            tuple: (success: bool, data: dict, status_code: int)
        """
        try:
            workout = Workout.query.get(workout_id)
            
            if not workout:
                return False, {"message": "Workout not found"}, 404
            
            return True, {
                "id": workout.id,
                "exercise": workout.exercise,
                "reps": workout.reps,
                "sets": workout.sets,
                "user_id": workout.user_id
            }, 200
            
        except Exception as e:
            return False, {"message": f"Failed to retrieve workout: {str(e)}"}, 500
    
    @staticmethod
    def update_workout(workout_id, exercise=None, reps=None, sets=None):
        """
        Update an existing workout.
        
        Args:
            workout_id: ID of the workout
            exercise: New exercise name (optional)
            reps: New number of reps (optional)
            sets: New number of sets (optional)
            
        Returns:
            tuple: (success: bool, message: str, status_code: int)
        """
        try:
            workout = Workout.query.get(workout_id)
            
            if not workout:
                return False, "Workout not found", 404
            
            # Update fields if provided
            if exercise:
                workout.exercise = exercise
            if reps is not None:
                workout.reps = reps
            if sets is not None:
                workout.sets = sets
            
            db.session.commit()
            
            return True, "Workout updated successfully", 200
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to update workout: {str(e)}", 500
    
    @staticmethod
    def delete_workout(workout_id):
        """
        Delete a workout entry.
        
        Args:
            workout_id: ID of the workout
            
        Returns:
            tuple: (success: bool, message: str, status_code: int)
        """
        try:
            workout = Workout.query.get(workout_id)
            
            if not workout:
                return False, "Workout not found", 404
            
            db.session.delete(workout)
            db.session.commit()
            
            return True, "Workout deleted successfully", 200
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete workout: {str(e)}", 500
    
    @staticmethod
    def get_workouts_by_exercise(user_id, exercise):
        """
        Get all workouts for a specific exercise.
        
        Args:
            user_id: ID of the user
            exercise: Name of the exercise
            
        Returns:
            tuple: (success: bool, data: dict, status_code: int)
        """
        try:
            workouts = Workout.query.filter_by(
                user_id=user_id,
                exercise=exercise
            ).order_by(Workout.id.desc()).all()
            
            workout_list = [
                {
                    "id": workout.id,
                    "exercise": workout.exercise,
                    "reps": workout.reps,
                    "sets": workout.sets,
                }
                for workout in workouts
            ]
            
            return True, {
                "exercise": exercise,
                "workouts": workout_list,
                "count": len(workout_list)
            }, 200
            
        except Exception as e:
            return False, {"message": f"Failed to retrieve workouts: {str(e)}"}, 500
    
    @staticmethod
    def get_total_reps(user_id, exercise=None):
        """
        Calculate total reps for a user (optionally for a specific exercise).
        
        Args:
            user_id: ID of the user
            exercise: Optional exercise name to filter by
            
        Returns:
            tuple: (success: bool, data: dict, status_code: int)
        """
        try:
            query = Workout.query.filter_by(user_id=user_id)
            
            if exercise:
                query = query.filter_by(exercise=exercise)
            
            workouts = query.all()
            total_reps = sum(workout.reps * workout.sets for workout in workouts)
            
            return True, {
                "total_reps": total_reps,
                "exercise": exercise if exercise else "all",
                "workout_count": len(workouts)
            }, 200
            
        except Exception as e:
            return False, {"message": f"Failed to calculate total reps: {str(e)}"}, 500
