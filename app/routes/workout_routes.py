from flask import Blueprint, request, jsonify
import cv2
import numpy as np
from app.utils.pose_utils import detect_pose, bicep_curl
from flask import render_template, current_app
import os


workout_bp = Blueprint('workout', __name__, template_folder='../views/templates', static_folder='../views/static')

@workout_bp.route('/')
def workout_home():
    return render_template('workout.html')

count = 0
stage = ''

@workout_bp.route('/process-frame', methods=['POST'])
def process_frame():
    global stage, count
    # Get the frame from the request
    if 'frame' not in request.files:
        return jsonify({'error': 'No frame provided'}), 400

    frame_file = request.files['frame']
    frame = cv2.imdecode(np.frombuffer(frame_file.read(), np.uint8), cv2.IMREAD_COLOR)

   
    landmarks = detect_pose(frame)

    
    r_angle, l_angle = bicep_curl(landmarks)

    if r_angle > 160 or l_angle > 160:
        stage = 'down'
    
    if r_angle < 30 and stage == 'down':
        stage = 'up'
        count += 1

    # Return feedback to the frontend
    return jsonify({'feedback': str(count)})