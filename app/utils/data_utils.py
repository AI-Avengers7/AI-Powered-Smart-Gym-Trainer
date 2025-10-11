"""
Data Utilities
Helper functions for data validation, processing, and transformation.
"""
import re
from datetime import datetime


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False
    
    # Simple regex pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password, min_length=6):
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        min_length: Minimum password length
        
    Returns:
        tuple: (bool: valid, str: message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"
    
    return True, "Password is valid"


def validate_workout_data(exercise, reps, sets):
    """
    Validate workout data.
    
    Args:
        exercise: Exercise name
        reps: Number of repetitions
        sets: Number of sets
        
    Returns:
        tuple: (bool: valid, str: message)
    """
    if not exercise or not isinstance(exercise, str):
        return False, "Valid exercise name is required"
    
    if not isinstance(reps, int) or reps <= 0:
        return False, "Reps must be a positive integer"
    
    if not isinstance(sets, int) or sets <= 0:
        return False, "Sets must be a positive integer"
    
    if reps > 1000:
        return False, "Reps cannot exceed 1000"
    
    if sets > 100:
        return False, "Sets cannot exceed 100"
    
    return True, "Workout data is valid"


def sanitize_string(input_string, max_length=100):
    """
    Sanitize and clean input string.
    
    Args:
        input_string: String to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized string
    """
    if not input_string:
        return ""
    
    # Remove leading/trailing whitespace
    sanitized = input_string.strip()
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def format_exercise_name(exercise):
    """
    Format exercise name to consistent format.
    
    Args:
        exercise: Raw exercise name
        
    Returns:
        str: Formatted exercise name
    """
    if not exercise:
        return ""
    
    # Convert to lowercase, strip whitespace, and capitalize words
    formatted = exercise.strip().lower()
    formatted = ' '.join(word.capitalize() for word in formatted.split())
    
    return formatted


def calculate_total_volume(reps, sets, weight=0):
    """
    Calculate total workout volume.
    
    Args:
        reps: Number of repetitions
        sets: Number of sets
        weight: Weight used (optional)
        
    Returns:
        int: Total volume
    """
    return reps * sets * (weight if weight > 0 else 1)


def calculate_workout_duration(start_time, end_time):
    """
    Calculate workout duration.
    
    Args:
        start_time: Start timestamp
        end_time: End timestamp
        
    Returns:
        float: Duration in minutes
    """
    if not start_time or not end_time:
        return 0
    
    try:
        duration = (end_time - start_time).total_seconds() / 60
        return round(duration, 2)
    except:
        return 0


def parse_workout_feedback(feedback_list):
    """
    Parse and format workout feedback.
    
    Args:
        feedback_list: List of feedback strings
        
    Returns:
        str: Formatted feedback
    """
    if not feedback_list:
        return "No feedback available"
    
    if isinstance(feedback_list, list):
        return "; ".join(feedback_list)
    
    return str(feedback_list)


def validate_user_input(data, required_fields):
    """
    Validate that all required fields are present in input data.
    
    Args:
        data: Dictionary of input data
        required_fields: List of required field names
        
    Returns:
        tuple: (bool: valid, list: missing fields)
    """
    if not data:
        return False, required_fields
    
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        return False, missing_fields
    
    return True, []


def format_response(success, data=None, message=None, status_code=200):
    """
    Format API response consistently.
    
    Args:
        success: Whether operation was successful
        data: Response data (optional)
        message: Response message (optional)
        status_code: HTTP status code
        
    Returns:
        tuple: (dict: response, int: status_code)
    """
    response = {
        "success": success
    }
    
    if message:
        response["message"] = message
    
    if data:
        response["data"] = data
    
    return response, status_code


def paginate_results(items, page=1, per_page=10):
    """
    Paginate a list of items.
    
    Args:
        items: List of items to paginate
        page: Page number (1-indexed)
        per_page: Number of items per page
        
    Returns:
        dict: Paginated results with metadata
    """
    if not items:
        return {
            "items": [],
            "total": 0,
            "page": page,
            "per_page": per_page,
            "total_pages": 0
        }
    
    total = len(items)
    total_pages = (total + per_page - 1) // per_page
    
    # Ensure page is within valid range
    page = max(1, min(page, total_pages))
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    return {
        "items": items[start_idx:end_idx],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages
    }


def convert_to_int(value, default=0):
    """
    Safely convert value to integer.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        int: Converted value or default
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def convert_to_float(value, default=0.0):
    """
    Safely convert value to float.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        float: Converted value or default
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
