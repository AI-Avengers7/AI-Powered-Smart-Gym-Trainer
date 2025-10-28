"""
Pose Detection Model
This module provides pose detection functionality using MediaPipe for various exercises.
"""
import mediapipe as mp
import cv2
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


class PoseDetector:
    """Class to handle pose detection and exercise tracking."""
    
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """Initialize the pose detector with MediaPipe."""
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.pose = mp_pose.Pose(
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence
        )
    
    def detect_landmarks(self, frame):
        """
        Detect pose landmarks in a frame.
        
        Args:
            frame: Input image frame (BGR format)
            
        Returns:
            landmarks: Detected pose landmarks or None
        """
        if frame is None:
            return None
            
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        return results.pose_landmarks if results.pose_landmarks else None
    
    def draw_landmarks(self, frame, landmarks):
        """
        Draw pose landmarks on the frame.
        
        Args:
            frame: Input image frame
            landmarks: Detected pose landmarks
            
        Returns:
            frame: Frame with drawn landmarks
        """
        if landmarks:
            mp_drawing.draw_landmarks(
                frame,
                landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )
        return frame
    
    @staticmethod
    def calculate_angle(a, b, c):
        """
        Calculate angle between three points.
        
        Args:
            a, b, c: Points as [x, y] coordinates
            
        Returns:
            angle: Angle in degrees
        """
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle
    
    def get_landmark_coords(self, landmarks, landmark_name):
        """
        Get coordinates of a specific landmark.
        
        Args:
            landmarks: Pose landmarks object
            landmark_name: Name of the landmark (e.g., LEFT_SHOULDER)
            
        Returns:
            [x, y]: Landmark coordinates
        """
        landmark = landmarks.landmark[getattr(mp_pose.PoseLandmark, landmark_name).value]
        return [landmark.x, landmark.y]
    
    def detect_bicep_curl(self, landmarks):
        """
        Detect bicep curl exercise and calculate angles.
        
        Args:
            landmarks: Pose landmarks object
            
        Returns:
            (left_angle, right_angle): Angles for both arms
        """
        if landmarks is None:
            return None, None
        
        try:
            # Get landmarks for both arms
            left_shoulder = self.get_landmark_coords(landmarks, 'LEFT_SHOULDER')
            left_elbow = self.get_landmark_coords(landmarks, 'LEFT_ELBOW')
            left_wrist = self.get_landmark_coords(landmarks, 'LEFT_WRIST')
            
            right_shoulder = self.get_landmark_coords(landmarks, 'RIGHT_SHOULDER')
            right_elbow = self.get_landmark_coords(landmarks, 'RIGHT_ELBOW')
            right_wrist = self.get_landmark_coords(landmarks, 'RIGHT_WRIST')
            
            # Calculate angles
            left_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            return left_angle, right_angle
        except Exception:
            return None, None
    
    def detect_squat(self, landmarks):
        """
        Detect squat exercise and calculate knee angles.
        
        Args:
            landmarks: Pose landmarks object
            
        Returns:
            (left_angle, right_angle): Knee angles for both legs
        """
        if landmarks is None:
            return None, None
        
        try:
            # Get landmarks for both legs
            left_hip = self.get_landmark_coords(landmarks, 'LEFT_HIP')
            left_knee = self.get_landmark_coords(landmarks, 'LEFT_KNEE')
            left_ankle = self.get_landmark_coords(landmarks, 'LEFT_ANKLE')
            
            right_hip = self.get_landmark_coords(landmarks, 'RIGHT_HIP')
            right_knee = self.get_landmark_coords(landmarks, 'RIGHT_KNEE')
            right_ankle = self.get_landmark_coords(landmarks, 'RIGHT_ANKLE')
            
            # Calculate knee angles
            left_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
            right_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
            
            return left_angle, right_angle
        except Exception:
            return None, None
    
    def detect_pushup(self, landmarks):
        """
        Detect push-up exercise and calculate elbow angles.
        
        Args:
            landmarks: Pose landmarks object
            
        Returns:
            (left_angle, right_angle): Elbow angles for both arms
        """
        if landmarks is None:
            return None, None
        
        try:
            # Get landmarks for both arms
            left_shoulder = self.get_landmark_coords(landmarks, 'LEFT_SHOULDER')
            left_elbow = self.get_landmark_coords(landmarks, 'LEFT_ELBOW')
            left_wrist = self.get_landmark_coords(landmarks, 'LEFT_WRIST')
            
            right_shoulder = self.get_landmark_coords(landmarks, 'RIGHT_SHOULDER')
            right_elbow = self.get_landmark_coords(landmarks, 'RIGHT_ELBOW')
            right_wrist = self.get_landmark_coords(landmarks, 'RIGHT_WRIST')
            
            # Calculate elbow angles
            left_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            return left_angle, right_angle
        except Exception:
            return None, None
    
    def detect_shoulder_press(self, landmarks):
        """
        Detect shoulder press exercise.
        
        Args:
            landmarks: Pose landmarks object
            
        Returns:
            (left_angle, right_angle): Shoulder angles for both arms
        """
        if landmarks is None:
            return None, None
        
        try:
            # Get landmarks
            left_elbow = self.get_landmark_coords(landmarks, 'LEFT_ELBOW')
            left_shoulder = self.get_landmark_coords(landmarks, 'LEFT_SHOULDER')
            left_hip = self.get_landmark_coords(landmarks, 'LEFT_HIP')
            
            right_elbow = self.get_landmark_coords(landmarks, 'RIGHT_ELBOW')
            right_shoulder = self.get_landmark_coords(landmarks, 'RIGHT_SHOULDER')
            right_hip = self.get_landmark_coords(landmarks, 'RIGHT_HIP')
            
            # Calculate angles
            left_angle = self.calculate_angle(left_elbow, left_shoulder, left_hip)
            right_angle = self.calculate_angle(right_elbow, right_shoulder, right_hip)
            
            return left_angle, right_angle
        except Exception:
            return None, None
    
    def close(self):
        """Close the pose detector."""
        self.pose.close()