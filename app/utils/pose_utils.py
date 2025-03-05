import mediapipe as mp
import cv2

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def detect_pose(frame):
    """
    Detect pose landmarks in a frame using MediaPipe.
    """
    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Pose
    results = pose.process(rgb_frame)

    # Draw pose landmarks on the frame
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,  # Image to draw on
            results.pose_landmarks,  # Detected landmarks
            mp_pose.POSE_CONNECTIONS  # Connections between landmarks
        )

    return frame, results.pose_landmarks

def are_arms_raised(landmarks):
    """
    Check if both arms are raised based on landmark positions.
    """
    if not landmarks:
        return False

    # Access landmarks using the `landmark` attribute
    left_shoulder = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_elbow = landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
    right_elbow = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]

    # Check if elbows are above shoulders
    return (left_elbow.y < left_shoulder.y) and (right_elbow.y < right_shoulder.y)