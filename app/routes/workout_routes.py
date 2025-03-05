from flask import Blueprint, request, jsonify
import cv2
import numpy as np
from app.utils.pose_utils import detect_pose, are_arms_raised
from flask import render_template, current_app
import os


workout_bp = Blueprint('workout', __name__, template_folder='../views/templates', static_folder='../views/static')

@workout_bp.route('/')
def workout_home():
    return render_template('workout.html')

@workout_bp.route('/process-frame', methods=['POST'])
def process_frame():
    # Get the frame from the request
    if 'frame' not in request.files:
        return jsonify({'error': 'No frame provided'}), 400

    frame_file = request.files['frame']
    frame = cv2.imdecode(np.frombuffer(frame_file.read(), np.uint8), cv2.IMREAD_COLOR)

   
    processed_frame, landmarks = detect_pose(frame)

    
    feedback = ""
    if are_arms_raised(landmarks):
        feedback = "Arms Raised!"
    else:
        feedback = "Raise your arms"

    # Return feedback to the frontend
    return jsonify({'feedback': feedback})