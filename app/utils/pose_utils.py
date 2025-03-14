import mediapipe as mp
import cv2
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
count = 0
stage = ''

def detect_pose(frame):
    """
    Detect pose landmarks in a frame using MediaPipe.
    """
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Pose
        results = pose.process(rgb_frame)

        # Return landmarks if detected, otherwise return None
        if results.pose_landmarks:
            return results.pose_landmarks
        else:
            return None

def calculate_angle(a, b, c):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180/np.pi)

    return angle%180


def bicep_curl(landmarks):
    """
    Calculate the angles for bicep curls.
    """
    if landmarks is None:
        return None, None  # Return None if no landmarks are detected

    # Access landmarks using the `landmark` attribute
    left_shoulder = [landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_wrist = [landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    right_wrist = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    right_shoulder = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    left_elbow = [landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    right_elbow = [landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

    # Calculate angles
    left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

    return left_angle, right_angle

# def caputure_video():
#     capture = cv2.VideoCapture(0)

#     while capture.isOpened():
#         _, frame = capture.read()

#         image = detect_pose(frame)

#         cv2.imshow("AI Trainer", image)

#         if cv2.waitKey(10) & 0xFF == ord("q"):
#             break

#     capture.release()
#     cv2.destroyAllWindows()
# if __name__ == "__main__":
#     caputure_video()
