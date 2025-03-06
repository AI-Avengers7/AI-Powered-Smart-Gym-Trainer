from flask import Blueprint, request, jsonify
import cv2
import numpy as np
from app.utils.pose_utils import detect_pose, bicep_curl


user_states = {}

def process_frame(frame, user_id):
    """
    Process a frame to detect bicep curls and update the user's state.
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