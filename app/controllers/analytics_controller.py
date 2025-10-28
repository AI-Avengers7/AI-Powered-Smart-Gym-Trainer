"""
Analytics Controller
Handles workout analytics, statistics, and progress tracking.
"""
from app.models.workout_model import Workout
from app.models.user_model import User
from collections import defaultdict


class AnalyticsController:
    """Controller for analytics and statistics operations."""
    
    @staticmethod
    def get_workout_summary(user_id):
        """
        Get overall workout summary for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            tuple: (success: bool, data: dict, status_code: int)
        """
        try:
            # Verify user exists
            user = User.query.get(user_id)
            if not user:
                return False, {"message": "User not found"}, 404
            
            # Get all workouts
            workouts = Workout.query.filter_by(user_id=user_id).all()
            
            if not workouts:
                return True, {
                    "total_workouts": 0,
                    "total_reps": 0,
                    "total_sets": 0,
                    "exercises_performed": 0,
                    "exercises": []
                }, 200
            
            # Calculate statistics
            total_workouts = len(workouts)
            total_reps = sum(w.reps * w.sets for w in workouts)
            total_sets = sum(w.sets for w in workouts)
            
            # Get unique exercises
            exercises = list(set(w.exercise for w in workouts))
            
            return True, {
                "total_workouts": total_workouts,
                "total_reps": total_reps,
                "total_sets": total_sets,
                "exercises_performed": len(exercises),
                "exercises": exercises
            }, 200
            
        except Exception as e:
            return False, {"message": f"Failed to get workout summary: {str(e)}"}, 500
    
    @staticmethod
    def get_exercise_breakdown(user_id):
        """
        Get breakdown of workouts by exercise type.
        
        Args:
            user_id: ID of the user
            
        Returns:
            tuple: (success: bool, data: dict, status_code: int)
        """
        try:
            # Verify user exists
            user = User.query.get(user_id)
            if not user:
                return False, {"message": "User not found"}, 404
            
            # Query workouts grouped by exercise
            workouts = Workout.query.filter_by(user_id=user_id).all()
            
            if not workouts:
                return True, {"breakdown": []}, 200
            
            # Calculate breakdown
            exercise_stats = defaultdict(lambda: {"count": 0, "total_reps": 0, "total_sets": 0})
            
            for workout in workouts:
                exercise_stats[workout.exercise]["count"] += 1
                exercise_stats[workout.exercise]["total_reps"] += workout.reps * workout.sets
                exercise_stats[workout.exercise]["total_sets"] += workout.sets
            
            # Format breakdown
            breakdown = [
                {
                    "exercise": exercise,
                    "workout_count": stats["count"],
                    "total_reps": stats["total_reps"],
                    "total_sets": stats["total_sets"],
                    "avg_reps_per_workout": round(stats["total_reps"] / stats["count"], 2)
                }
                for exercise, stats in exercise_stats.items()
            ]
            
            # Sort by workout count
            breakdown.sort(key=lambda x: x["workout_count"], reverse=True)
            
            return True, {"breakdown": breakdown}, 200
            
        except Exception as e:
            return False, {"message": f"Failed to get exercise breakdown: {str(e)}"}, 500
    
    @staticmethod
    def get_progress_data(user_id, exercise):
        """
        Get progress data for a specific exercise over time.
        
        Args:
            user_id: ID of the user
            exercise: Name of the exercise
            
        Returns:
            tuple: (success: bool, data: dict, status_code: int)
        """
        try:
            # Verify user exists
            user = User.query.get(user_id)
            if not user:
                return False, {"message": "User not found"}, 404
            
            # Get workouts for the specific exercise
            workouts = Workout.query.filter_by(
                user_id=user_id,
                exercise=exercise
            ).order_by(Workout.id.asc()).all()
            
            if not workouts:
                return True, {
                    "exercise": exercise,
                    "progress": [],
                    "total_sessions": 0
                }, 200
            
            # Format progress data
            progress = [
                {
                    "session": idx + 1,
                    "workout_id": workout.id,
                    "reps": workout.reps,
                    "sets": workout.sets,
                    "total_reps": workout.reps * workout.sets
                }
                for idx, workout in enumerate(workouts)
            ]
            
            return True, {
                "exercise": exercise,
                "progress": progress,
                "total_sessions": len(workouts)
            }, 200
            
        except Exception as e:
            return False, {"message": f"Failed to get progress data: {str(e)}"}, 500
    
    @staticmethod
    def get_recent_activity(user_id, limit=10):
        """
        Get recent workout activity for a user.
        
        Args:
            user_id: ID of the user
            limit: Maximum number of recent workouts to return
            
        Returns:
            tuple: (success: bool, data: dict, status_code: int)
        """
        try:
            # Verify user exists
            user = User.query.get(user_id)
            if not user:
                return False, {"message": "User not found"}, 404
            
            # Get recent workouts
            workouts = Workout.query.filter_by(user_id=user_id)\
                .order_by(Workout.id.desc())\
                .limit(limit)\
                .all()
            
            if not workouts:
                return True, {"recent_activity": []}, 200
            
            # Format activity data
            activity = [
                {
                    "id": workout.id,
                    "exercise": workout.exercise,
                    "reps": workout.reps,
                    "sets": workout.sets,
                    "total_reps": workout.reps * workout.sets
                }
                for workout in workouts
            ]
            
            return True, {"recent_activity": activity}, 200
            
        except Exception as e:
            return False, {"message": f"Failed to get recent activity: {str(e)}"}, 500
    
    @staticmethod
    def get_personal_records(user_id):
        """
        Get personal records for each exercise.
        
        Args:
            user_id: ID of the user
            
        Returns:
            tuple: (success: bool, data: dict, status_code: int)
        """
        try:
            # Verify user exists
            user = User.query.get(user_id)
            if not user:
                return False, {"message": "User not found"}, 404
            
            # Get all workouts
            workouts = Workout.query.filter_by(user_id=user_id).all()
            
            if not workouts:
                return True, {"personal_records": []}, 200
            
            # Calculate personal records
            records = defaultdict(lambda: {"max_reps": 0, "max_sets": 0, "max_total_reps": 0})
            
            for workout in workouts:
                exercise = workout.exercise
                total_reps = workout.reps * workout.sets
                
                if workout.reps > records[exercise]["max_reps"]:
                    records[exercise]["max_reps"] = workout.reps
                
                if workout.sets > records[exercise]["max_sets"]:
                    records[exercise]["max_sets"] = workout.sets
                
                if total_reps > records[exercise]["max_total_reps"]:
                    records[exercise]["max_total_reps"] = total_reps
            
            # Format records
            personal_records = [
                {
                    "exercise": exercise,
                    "max_reps": stats["max_reps"],
                    "max_sets": stats["max_sets"],
                    "max_total_reps": stats["max_total_reps"]
                }
                for exercise, stats in records.items()
            ]
            
            return True, {"personal_records": personal_records}, 200
            
        except Exception as e:
            return False, {"message": f"Failed to get personal records: {str(e)}"}, 500
    
    @staticmethod
    def get_workout_stats_by_exercise(user_id, exercise):
        """
        Get detailed statistics for a specific exercise.
        
        Args:
            user_id: ID of the user
            exercise: Name of the exercise
            
        Returns:
            tuple: (success: bool, data: dict, status_code: int)
        """
        try:
            # Verify user exists
            user = User.query.get(user_id)
            if not user:
                return False, {"message": "User not found"}, 404
            
            # Get workouts for the exercise
            workouts = Workout.query.filter_by(
                user_id=user_id,
                exercise=exercise
            ).all()
            
            if not workouts:
                return True, {
                    "exercise": exercise,
                    "stats": {
                        "total_sessions": 0,
                        "total_reps": 0,
                        "avg_reps": 0,
                        "max_reps": 0,
                        "total_sets": 0,
                        "avg_sets": 0,
                        "max_sets": 0
                    }
                }, 200
            
            # Calculate statistics
            total_sessions = len(workouts)
            all_reps = [w.reps * w.sets for w in workouts]
            all_sets = [w.sets for w in workouts]
            
            stats = {
                "total_sessions": total_sessions,
                "total_reps": sum(all_reps),
                "avg_reps": round(sum(all_reps) / total_sessions, 2),
                "max_reps": max(all_reps),
                "total_sets": sum(all_sets),
                "avg_sets": round(sum(all_sets) / total_sessions, 2),
                "max_sets": max(all_sets)
            }
            
            return True, {
                "exercise": exercise,
                "stats": stats
            }, 200
            
        except Exception as e:
            return False, {"message": f"Failed to get exercise stats: {str(e)}"}, 500
