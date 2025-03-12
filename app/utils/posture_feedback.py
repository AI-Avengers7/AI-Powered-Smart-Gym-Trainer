from pose_utils import *

# Global variables for user states
user_states = {}

def generate_corrections(landmarks):
    """
    Generate real-time corrections based on body landmarks.
    """
    corrections = []

    # Getting relevant landmarks for upper body posture
    left_shoulder = [landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    right_shoulder = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    left_hip = [landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    right_hip = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    left_elbow = [landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    right_elbow = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    left_wrist = [landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    right_wrist = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    
    #Getting relevant landmarks for lower body posture
    left_knee = [landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    right_knee = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    left_ankle = [landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    right_ankle = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

    # Calculate back angle (shoulders to hips)
    left_back_angle = calculate_angle(left_shoulder, left_hip, right_hip)
    right_back_angle = calculate_angle(right_shoulder, right_hip, left_hip)

    # Checking the back straightness:  Adjust thresholds as needed
    if left_back_angle < 160 or left_back_angle > 200: 
        corrections.append("Keep your back straight!")
    if right_back_angle < 160 or right_back_angle > 200:
        corrections.append("Keep your right side straight!")

    # Checking the elbow position: Horizontal distance between elbow and shoulder 
    left_elbow_distance = abs(left_elbow[0] - left_shoulder[0])  
    right_elbow_distance = abs(right_elbow[0] - right_shoulder[0])

    #Adjusting threshold for elbows
    if left_elbow_distance > 0.2: 
        corrections.append("Keep your elbows close to your body!")
    if right_elbow_distance > 0.2:  
        corrections.append("Keep your right elbow close to your body!")

     # Checking wrist position for both sides: # Horizontal distance between both wrists and shoulders
    left_wrist_distance = abs(left_wrist[0] - left_shoulder[0])  
    right_wrist_distance = abs(right_wrist[0] - right_shoulder[0])  
    
    # Adjusting threshold for wrist
    if left_wrist_distance > 0.3:  
        corrections.append("Keep your left wrist aligned with your shoulder!")
    if right_wrist_distance > 0.3: 
        corrections.append("Keep your right wrist aligned with your shoulder!")

    # Check wrist-elbow alignment
    left_wrist_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_wrist_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

    # Adjusting threshold for wrist and elbows
    if left_wrist_elbow_angle < 160 or left_wrist_elbow_angle > 200:  
        corrections.append("Keep your left wrist in line with your elbow!")
    if right_wrist_elbow_angle < 160 or right_wrist_elbow_angle > 200:  
        corrections.append("Keep your right wrist in line with your elbow!")

     # Checking if knees are collapsing inward: Horizontal position of both knees and ankles
    left_knee_position = left_knee[0]  
    right_knee_position = right_knee[0]  
    left_ankle_position = left_ankle[0]  
    right_ankle_position = right_ankle[0]  

    # Adjusting threshold
    if left_knee_position < left_ankle_position - 0.1:  
        corrections.append("Your left knee is collapsing inward!")
    if right_knee_position > right_ankle_position + 0.1:  
        corrections.append("Your right knee is collapsing inward!")
    return corrections

def process_frame(frame, user_id):
    """
    Process a frame to detect bicep curls, update the user's state, and generate corrections.
    """
    # Initialize user state if it doesn't exist
    if user_id not in user_states:
        user_states[user_id] = {'count': 0, 'stage': '', 'corrections': []}

    # Getting the user's state
    state = user_states[user_id]

    # Checking if the frame is valid
    if frame is None:
        return state['count'], state['stage'], state['corrections']

    # Detect landmarks
    landmarks = detect_pose(frame)

    # Checking if landmarks are detected
    if landmarks is None:
        return state['count'], state['stage'], state['corrections']

    # Calculate bicep curl angles
    r_angle, l_angle = bicep_curl(landmarks)

    # Checking if angles are valid
    if l_angle is None or r_angle is None:
        return state['count'], state['stage'], state['corrections']

    # Update stage and count
    if r_angle > 160 or l_angle > 160:
        state['stage'] = 'down'
    if r_angle < 30 and state['stage'] == 'down':
        state['stage'] = 'up'
        state['count'] += 1

    # Generate corrections
    corrections = generate_corrections(landmarks)

    # Checking the lower body posture 
    lower_body_corrections = generate_corrections(landmarks)
    corrections.extend(lower_body_corrections)
    
    state['corrections'] = corrections

    return state['count'], state['stage'], corrections